# `src/features/`

A **feature** is a self-contained slice of the product (e.g. `items`, `auth`, `user-profile`). It owns its types, its API calls and data-fetching hooks, and the UI for that slice.

## Required files

Every folder in `src/features/` **must** contain these three files:

| File | Purpose |
| --- | --- |
| `types.ts` | TypeScript types for the feature's data: API response shapes and request payloads. Keep them in sync with the backend's `schemas.py`. |
| `api.tsx` | All server communication for the feature: plain request functions (built on `@/lib/apiClient`) plus the React Query hooks that wrap them (`useItems`, `useCreateItem`, ...). |
| `<FeatureName>.tsx` | The feature's main component, named after the folder in PascalCase: `items/` → `Items.tsx`, `user-profile/` → `UserProfile.tsx`. This is what pages render. |

You can add more files as a feature grows, such as sub-components, feature-specific hooks, or utilities:

```
features/items/
├── types.ts
├── api.tsx
├── Items.tsx          # main component (required)
├── ItemForm.tsx       # optional sub-component
└── useItemFilters.ts  # optional feature-specific hook
```

## Rules

- **Features don't import other features or pages.** If two features need the same thing, move it to `src/components/` (UI) or `src/lib/` (logic). If a screen needs two features, compose them in a page. The lint config (`.oxlintrc.json`) enforces this.
- **Inside a feature, use relative imports** (`./api`, `./types`).
- **Only `api.tsx` talks to the backend.** Components call the hooks, never `fetch` directly.
- **Name query keys per feature** (e.g. `itemKeys`) so cache invalidation stays local to the feature.

## Adding a feature

1. Create `src/features/<name>/`.
2. Add `types.ts` with the data shapes.
3. Add `api.tsx` with request functions and hooks.
4. Add `<Name>.tsx` with the main component.
5. Render it from a page in `src/pages/`.
6. Run `npm run lint` to check import boundaries.

See `items/` for a full CRUD example and `health/` for a minimal read-only one.
