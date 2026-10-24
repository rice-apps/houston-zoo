# `src/components/`

**Shared, reusable UI components** that are used across multiple pages or features: buttons, inputs, modals, layout shells, loading and error states.

## What belongs here

- Generic, presentational components driven entirely by props (`Button`, `ErrorMessage`).
- App-wide shells (`Layout`, which renders the header, nav and `<Outlet />` for routes).

## What doesn't belong here

- Components tied to one domain concept (e.g. an `ItemCard`). Keep those inside the owning feature, such as `src/features/items/ItemCard.tsx`.
- Data fetching. Shared components receive data via props and never call feature hooks or the API.

A good test: if the component would make sense in a completely different app, it belongs here.

## Rules

- **Never import from `@/features/*` or `@/pages/*`.** Shared code sits below features in the dependency graph. The lint config (`.oxlintrc.json`) enforces this.
- Use **named exports** (`export function Button`) and one component per file, named after the file.
- Accept and forward native props where it makes sense (see `Button.tsx`, which extends `ComponentProps<'button'>`).
- If a component grows sub-parts or its own styles, give it a folder: `components/Modal/Modal.tsx`.

## Current components

| Component | Description |
| --- | --- |
| `Layout` | App shell with header, navigation and the routed page outlet. |
| `Button` | Styled `<button>` with `primary` / `danger` variants. |
| `ErrorMessage` | Displays an error (`Error` instance or unknown) with `role="alert"`. |
