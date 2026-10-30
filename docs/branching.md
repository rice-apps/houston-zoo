# GitHub Workflow & Branch Naming Guidelines

We use **Notion to track tasks** and **GitHub to track development**. Our GitHub–Notion automation updates a task's status when its branch is created, a pull request is opened, and the PR is merged.

## 1. Start with a Notion task

Before writing code, make sure you have an assigned task in our Notion task database. Each task has an automatically generated ID, such as **`ZOO-12`**.

**Use the exact ID from Notion.** Don't invent a new number or reuse another task's ID.

## 2. Name your branch correctly

Use this format for all feature branches:

```text
feature/ZOO-<TASK_NUMBER>-<short-description>
```

Examples:

```text
feature/ZOO-12-animal-search
feature/ZOO-13-login-page
feature/ZOO-14-exhibit-models
```

Rules:

- Include the **exact Notion task ID** (e.g., `ZOO-12`).
- Use **lowercase words separated by hyphens** for the description.
- Keep the description short but meaningful.
- Use **one Notion task ID per branch**.
- Do not create generic branches such as `feature/login`, `my-changes`, or `test-branch` for tracked work.

> The automation identifies the task by its `ZOO-<number>` in the branch name. Following the full naming format keeps our branches consistent.

## 3. Create and push your branch

Start from an up-to-date `main` branch:

```bash
git checkout main
git pull origin main
git checkout -b feature/ZOO-12-animal-search
git push -u origin feature/ZOO-12-animal-search
```

Replace `ZOO-12-animal-search` with your own task ID and description.

**Important:** Creating a branch locally is not enough. You must **push it to GitHub** for the automation to run.

## 4. Open a pull request

When you have changes to review:

1. Push your commits to the same feature branch.
2. Open a pull request into `main`.
3. Include the Notion ID in the PR title, for example: **`[ZOO-12] Add animal search`**.
4. Briefly describe what changed and how you tested it.
5. Request review and address feedback before merging.

Open a **draft PR** if your work is still in progress. Mark it **Ready for review** when it's ready.

## 5. How Notion status updates work

| GitHub action | Notion status |
|---|---|
| Task created in Notion | Not Started (set in Notion) |
| Matching branch pushed to GitHub | In Progress |
| Draft PR opened | In Progress |
| Regular PR opened, or draft marked ready for review | In Review |
| PR merged | Completed |
| PR closed without merging | No automatic change |

**You do not need to manually move the Notion task** when these GitHub events happen, provided the automation is configured and running successfully.

## 6. Example workflow

Suppose your Notion task is **`ZOO-12 — Implement animal search`**:

1. Create `feature/ZOO-12-animal-search` and push it → Notion moves to **In Progress**.
2. Open PR `[ZOO-12] Implement animal search` → Notion moves to **In Review** (unless it's a draft).
3. Get the PR reviewed and merged → Notion moves to **Completed**.

## A few important notes

- The automation reads the **branch name**, so adding the task ID only to the PR title is not enough.
- Do **not** merge a PR until its task is ready to be marked Completed.
- Our current automation assumes **one final PR per Notion task**. If a task needs multiple PRs, coordinate with the team lead so it isn't marked Completed too early.
- If a status doesn't update, check the repository's **Actions** tab and confirm that your branch includes a valid Notion ID.

