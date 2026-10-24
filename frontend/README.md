# Frontend

React 19 + TypeScript app built with Vite, using React Router for routing and TanStack Query for server state.

## Getting started

### With Docker (recommended)

From the repository root:

```bash
docker compose up --build
```

The app runs at http://localhost:5173 with hot reload. Requests to `/api` are proxied to the backend container.

### Without Docker

Requires Node 22+.

```bash
cd frontend
npm install
cp .env.example .env   # optional, defaults work for local dev
npm run dev
```

Run the backend on http://localhost:8000 (see `../backend/README.md`) so the `/api` proxy has somewhere to go.

## Scripts

| Command | Description |
| --- | --- |
| `npm run dev` | Start the Vite dev server on port 5173. |
| `npm run build` | Type-check and build to `dist/`. |
| `npm run preview` | Serve the production build locally. |
| `npm run lint` | Run oxlint, including the import-boundary rules. |
| `npm run typecheck` | Run the TypeScript compiler without emitting. |

## Project structure

```
frontend/
├── src/
│   ├── app/                 # app wiring: providers, router, query client
│   ├── pages/               # one component per route          (see pages/README.md)
│   ├── features/            # self-contained product features   (see features/README.md)
│   ├── components/          # shared, reusable UI components     (see components/README.md)
│   ├── lib/                 # shared non-UI code (API client, utilities)
│   ├── index.css            # global styles
│   └── main.tsx             # entry point
├── Dockerfile               # Vite dev server image used by docker-compose.yml
└── vite.config.ts
```

### Dependency direction

Code may only import "downwards":

```
app  →  pages  →  features  →  components / lib
```

- `pages` compose `features` and `components`.
- `features` use `components` and `lib`, but never other features or pages.
- `components` and `lib` never import features or pages.

These rules are enforced by `no-restricted-imports` overrides in `.oxlintrc.json`, so `npm run lint` fails on a violating import. This keeps features decoupled: you can add, change or delete one without touching the others.

### Imports

Use the `@/` alias for anything outside the current folder (`@/components/Button`, `@/lib/apiClient`). It maps to `src/` via `vite.config.ts` and `tsconfig.app.json`. Within a feature, use relative imports (`./api`).

## Talking to the API

All HTTP calls go through `src/lib/apiClient.ts`, which:

- prefixes paths with `VITE_API_BASE_URL` (default `/api`),
- sends and parses JSON,
- throws an `ApiError` (with `status` and the response body) for non-2xx responses, using FastAPI's `detail` as the message.

Each feature wraps the client in its own `api.tsx`:

```tsx
export const itemsApi = {
  list: () => apiClient.get<Item[]>('/items'),
}

export function useItems() {
  return useQuery({ queryKey: itemKeys.all, queryFn: itemsApi.list })
}
```

## Environment variables

| Variable | Default | Description |
| --- | --- | --- |
| `VITE_API_BASE_URL` | `/api` | Base URL used by the browser for API calls. Baked in at build time. |
| `API_PROXY_TARGET` | `http://localhost:8000` | Dev server only: where `/api` is proxied. Set to `http://backend:8000` in Docker. |

Only variables prefixed with `VITE_` are exposed to browser code.
