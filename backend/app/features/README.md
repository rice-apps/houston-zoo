# `app/features/`

A **feature** is a self-contained vertical slice of the API (e.g. `items`, `users`, `orders`). It owns its database models, request/response schemas, business logic and HTTP routes.

## Required modules

Every package in `app/features/` **must** contain:

| Module | Layer | Responsibility |
| --- | --- | --- |
| `__init__.py` | | Makes the folder a package. |
| `models.py` | Persistence | SQLAlchemy ORM models (tables), inheriting from `app.database.Base`. |
| `schemas.py` | Contract | Pydantic models for request bodies and responses (`ItemCreate`, `ItemUpdate`, `ItemRead`). This is the public API shape, kept separate from the DB model. |
| `service.py` | Business logic | A service class that takes a `Session` and implements the feature's operations. No FastAPI imports: raise `app.core.exceptions` errors instead of `HTTPException`. |
| `router.py` | HTTP | `router = APIRouter(prefix="/<feature>", tags=["<feature>"])`. Thin endpoints that validate input, call the service and return schemas. Also defines the service dependency (`get_item_service`). |

## How a request flows

```
HTTP request
  → router.py   validates input with schemas.py, resolves ItemService via Depends
  → service.py  business rules, queries and commits using models.py
  → router.py   response_model serializes the ORM object through schemas.py
HTTP response
```

## Rules

- **Features are independent.** Avoid importing another feature's `service` or `models`. If something is shared, move it to `app/core/` (cross-cutting logic) or `app/database/` (DB helpers and mixins). If one feature genuinely depends on another, depend on its *service*, never its router.
- **Keep routers thin.** Any logic beyond "call the service and return" belongs in `service.py`.
- **Services are framework-agnostic.** They can be unit-tested or reused from scripts and background jobs without FastAPI.
- **Never return ORM models without a `response_model`.** Schemas are the contract with the frontend.

## Adding a feature

1. Copy `items/` to `app/features/<name>/` and rename the classes.
2. Define the table in `models.py` and the API shapes in `schemas.py`.
3. Implement operations in `service.py`.
4. Expose endpoints in `router.py`.
5. Register the router in `FEATURE_ROUTERS` in `app/main.py`.
6. Add tests in `tests/features/test_<name>.py` and run `pytest`.
