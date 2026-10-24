# `src/pages/`

A **page** is a top-level screen that maps to a route. Every route in `src/app/router.tsx` renders exactly one page component from this folder.

## What belongs here

- One file per route, named `<Name>Page.tsx` (e.g. `HomePage.tsx`, `ItemsPage.tsx`).
- Page-level layout: headings, arrangement of sections, reading route params (`useParams`) and passing them down.
- Composition: pages render one or more **features** and shared **components**.

## What doesn't belong here

- **Data fetching or API calls.** Put these in a feature's `api.tsx`.
- **Business logic or feature state.** Put this in the feature.
- **Reusable UI.** Put it in `src/components/`.

Pages should stay thin. If a page starts getting large, the extra code most likely belongs in a feature.

## Example

```tsx
import { Items } from '@/features/items/Items'

export function ItemsPage() {
  return (
    <>
      <h1>Items</h1>
      <Items />
    </>
  )
}
```

## Adding a page

1. Create `src/pages/<Name>Page.tsx`.
2. Register its route in `src/app/router.tsx`.
3. Optionally add a link in `src/components/Layout.tsx`.

## Import rules

Pages are the top layer, so they can import from `@/features/*`, `@/components/*` and `@/lib/*`. Nothing else should import from pages.
