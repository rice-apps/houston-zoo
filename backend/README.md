# Backend

FastAPI service using SQLAlchemy 2 for persistence and Pydantic v2 for validation and settings. It uses Postgres in Docker and falls back to SQLite for quick local runs.

## Getting started

### With Docker (recommended)

From the repository root:

```bash
docker compose up --build
```

- API: http://localhost:8000/api
- Interactive docs (Swagger UI): http://localhost:8000/api/docs
- Code in `backend/` is mounted into the container and reloads on change.

Run tests or lint inside the container:

```bash
docker compose exec backend pytest
docker compose exec backend ruff check .
```

### Without Docker

Requires Python 3.12+.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env      # defaults to SQLite (./app.db)
uvicorn app.main:app --reload
```

## Project structure

```
backend/
├── app/
│   ├── main.py              # app factory: middleware, exception handlers, router registration
│   ├── core/                # cross-cutting concerns shared by all features
│   │   ├── config.py        # Settings loaded from env vars / .env
│   │   └── exceptions.py    # domain errors (NotFoundError, ...) mapped to HTTP responses
│   ├── database/            # database infrastructure, no business logic
│   │   ├── base.py          # DeclarativeBase and shared mixins (TimestampMixin)
│   │   └── session.py       # engine, SessionLocal, get_db dependency
│   └── features/            # one package per feature (see features/README.md)
│       └── items/
│           ├── models.py    # SQLAlchemy models
│           ├── schemas.py   # Pydantic request/response schemas
│           ├── service.py   # business logic
│           └── router.py    # HTTP endpoints
├── tests/
│   ├── conftest.py          # in-memory SQLite + TestClient fixtures
│   ├── test_health.py
│   └── features/            # tests per feature
├── Dockerfile
├── pyproject.toml           # pytest and ruff config
├── requirements.txt         # runtime dependencies
└── requirements-dev.txt     # + test and lint tools
```

### Layers

| Folder | Depends on | Purpose |
| --- | --- | --- |
| `core/` | nothing in `app/` | Configuration, errors, and later things like security/auth helpers and logging. |
| `database/` | `core/` | Engine, sessions, declarative base. Knows nothing about specific features. |
| `features/*` | `core/`, `database/` | Business functionality, one self-contained package per feature. |
| `main.py` | everything | Wires it all together. |

Every feature must contain `models.py`, `schemas.py`, `service.py` and `router.py`. See [`app/features/README.md`](app/features/README.md) for what goes in each file and how to add a feature.

## Error handling

Services raise domain errors from `app/core/exceptions.py`:

```python
raise NotFoundError(f"Item {item_id} not found")
```

A global handler turns them into `{"detail": "..."}` JSON responses with the matching status code (`NotFoundError` → 404, `ConflictError` → 409, `BadRequestError` → 400). This keeps services free of HTTP concerns, and the error shape matches FastAPI's own errors, which the frontend `apiClient` already understands.

## Configuration

Settings live in `app/core/config.py` and are read from environment variables (or `backend/.env`):

| Variable | Default | Description |
| --- | --- | --- |
| `APP_NAME` | `Starter API` | Shown in the docs and the health endpoint. |
| `ENVIRONMENT` | `development` | Free-form environment name. |
| `DEBUG` | `false` | FastAPI debug mode. |
| `API_PREFIX` | `/api` | Prefix for all routes, docs and the OpenAPI schema. |
| `DATABASE_URL` | `sqlite:///./app.db` | SQLAlchemy URL. Use `postgresql+psycopg://user:pass@host:5432/db` for Postgres. |
| `CORS_ORIGINS` | `["http://localhost:5173"]` | JSON list of allowed origins. |

## Database and migrations

On startup, `Base.metadata.create_all()` creates any missing tables for registered models. That's convenient for a starter, but it never alters existing tables. Once your schema needs to evolve, add [Alembic](https://alembic.sqlalchemy.org/) and replace the `create_all` call in `app/main.py` with migrations.

## Testing

```bash
pytest
```

Tests use an in-memory SQLite database and override the `get_db` dependency, so they need no running database.

## Lint and format

```bash
ruff check .
ruff format .
```
