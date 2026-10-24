# React + Vite / FastAPI Starter

A dockerized full-stack starter with a feature-based, decoupled structure on both sides.

| Layer | Stack |
| --- | --- |
| Frontend | React 19, TypeScript, Vite, React Router, TanStack Query, oxlint |
| Backend | FastAPI, SQLAlchemy 2, Pydantic v2, pytest, ruff |
| Database | PostgreSQL (Docker) / SQLite (local fallback) |
| Infra | Docker Compose for local development (hot reload) |

## Quick start

```bash
cp .env.example .env        # optional for dev, the defaults work
docker compose up --build
```

| Service | URL |
| --- | --- |
| Frontend | http://localhost:5173 |
| API | http://localhost:8000/api |
| API docs | http://localhost:8000/api/docs |
| Postgres | `localhost:5432` (user/password/db: `app`) |

Both apps hot-reload as you edit files. The Vite dev server proxies `/api` to the backend, so there's no CORS setup in development.

The Docker setup is for local development only. A production setup (serving the built frontend and routing `/api` to the backend) can be added once there's a deploy target.

## Repository layout

```
.
├── frontend/               # React + Vite app          → frontend/README.md
│   └── src/
│       ├── pages/          # one component per route   → pages/README.md
│       ├── features/       # self-contained features   → features/README.md
│       └── components/     # shared UI components      → components/README.md
├── backend/                # FastAPI service           → backend/README.md
│   └── app/
│       ├── core/           # config, errors, cross-cutting concerns
│       ├── database/       # engine, session, declarative base
│       └── features/       # self-contained features   → features/README.md
├── docker-compose.yml      # development stack
└── .env.example
```

## Architecture

Both apps are organized **by feature** rather than by technical layer. Every feature follows the same file layout on its side of the stack.

### Frontend feature (`frontend/src/features/<name>/`)

| File | Purpose |
| --- | --- |
| `types.ts` | Data types, mirroring the backend schemas |
| `api.tsx` | API request functions and React Query hooks |
| `<Name>.tsx` | The feature's main component |

Import boundaries (features can't import other features, and shared components can't import features) are enforced by oxlint.

### Backend feature (`backend/app/features/<name>/`)

| File | Purpose |
| --- | --- |
| `models.py` | SQLAlchemy models |
| `schemas.py` | Pydantic request/response schemas |
| `service.py` | Business logic (no FastAPI dependencies) |
| `router.py` | HTTP endpoints |

### End-to-end example

`items` is implemented on both sides as a reference CRUD feature:

```
ItemsPage → features/items/Items.tsx → api.tsx (useItems) → GET /api/items
  → features/items/router.py → service.py → models.py → Postgres
```

## Adding a full-stack feature

1. **Backend:** copy `backend/app/features/items/` to a new name, adapt models, schemas, service and router, then register the router in `backend/app/main.py`.
2. **Frontend:** create `frontend/src/features/<name>/` with `types.ts`, `api.tsx` and `<Name>.tsx`.
3. **Page:** render the feature from a page in `frontend/src/pages/` and add a route in `frontend/src/app/router.tsx`.
4. **Verify:** run `docker compose exec backend pytest` and `cd frontend && npm run lint`.

## Common commands

```bash
docker compose up --build              # start everything
docker compose down                    # stop
docker compose down -v                 # stop and delete the database volume
docker compose logs -f backend         # follow backend logs
docker compose exec backend pytest     # backend tests
docker compose exec frontend npm run lint
```
