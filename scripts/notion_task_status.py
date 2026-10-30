"""Move Notion tasks forward as their matching GitHub branches and PRs progress.


"""

import json
import os
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_ROOT = "https://api.notion.com/v1"
NOTION_VERSION = "2026-03-11"
STATUS_ORDER = ("Not Started", "In Progress", "In Review", "Completed")


def extract_task_number(branch: str, prefix: str) -> int | None:
    """Find ZOO-12 in names like feature/ZOO-12-animal-search."""
    pattern = rf"(?<![A-Za-z0-9]){re.escape(prefix)}-(\d+)(?![A-Za-z0-9])"
    match = re.search(pattern, branch, re.IGNORECASE)
    return int(match.group(1)) if match else None


def desired_status(event: str, action: str, merged: str, draft: str) -> str | None:
    if event == "create":
        return "In Progress"
    if event != "pull_request_target":
        return None
    if action == "closed":
        return "Completed" if merged.lower() == "true" else None
    if action in {"opened", "reopened", "ready_for_review"}:
        return "In Progress" if draft.lower() == "true" else "In Review"
    return None


def notion_request(method: str, path: str, token: str, body: dict | None = None) -> dict:
    raw = json.dumps(body).encode("utf-8") if body is not None else None
    request = Request(
        API_ROOT + path,
        data=raw,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    try:
        with urlopen(request, timeout=20) as response:
            return json.load(response)
    except HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Notion API returned HTTP {exc.code}: {details}") from exc
    except URLError as exc:
        raise RuntimeError(f"Notion API request failed: {exc.reason}") from exc


def resolve_data_source_id(token: str) -> str:
    explicit = os.getenv("NOTION_DATA_SOURCE_ID", "").strip()
    if explicit:
        return explicit
    database_id = os.environ["NOTION_DATABASE_ID"].strip()
    database = notion_request("GET", f"/databases/{database_id}", token)
    sources = database.get("data_sources", [])
    if len(sources) != 1:
        raise RuntimeError(
            f"Expected one data source in database; found {len(sources)}. "
            "Set NOTION_DATA_SOURCE_ID to the intended source's id."
        )
    return sources[0]["id"]


def sync_status() -> None:
    event = os.getenv("GITHUB_EVENT_NAME", "")
    action = os.getenv("PR_ACTION", "")
    target = desired_status(
        event,
        action,
        os.getenv("PR_MERGED", "false"),
        os.getenv("PR_DRAFT", "false"),
    )
    if target is None:
        print("Event does not call for a Notion status change.")
        return

    branch = os.getenv("BRANCH_NAME", "")
    prefix = os.getenv("NOTION_TASK_PREFIX", "ZOO").strip().upper()
    number = extract_task_number(branch, prefix)
    if number is None:
        print(f"No {prefix}-<number> task ID in branch {branch!r}; skipping.")
        return

    token = os.environ["NOTION_TOKEN"].strip()
    data_source_id = resolve_data_source_id(token)
    found = notion_request(
        "POST",
        f"/data_sources/{data_source_id}/query",
        token,
        {"filter": {"property": "ID", "unique_id": {"equals": number}}, "page_size": 2},
    )["results"]
    if len(found) != 1:
        raise RuntimeError(f"Expected exactly one Notion task for {prefix}-{number}; found {len(found)}.")

    page = found[0]
    unique_id = page["properties"]["ID"]["unique_id"]
    if (unique_id.get("prefix") or "").upper() != prefix:
        raise RuntimeError(f"The matching Notion ID doesn't have the expected prefix {prefix}.")

    current = (page["properties"].get("Status", {}).get("status") or {}).get("name")
    if current in STATUS_ORDER and STATUS_ORDER.index(current) >= STATUS_ORDER.index(target):
        print(f"{prefix}-{number} is already {current}; not moving backwards to {target}.")
        return

    notion_request(
        "PATCH",
        f"/pages/{page['id']}",
        token,
        {"properties": {"Status": {"status": {"name": target}}}},
    )
    print(f"Updated {prefix}-{number}: {current or '(unset)'} -> {target}")


if __name__ == "__main__":
    try:
        sync_status()
    except (KeyError, ValueError, RuntimeError) as error:
        print(f"Notion sync failed: {error}", file=sys.stderr)
        sys.exit(1)
