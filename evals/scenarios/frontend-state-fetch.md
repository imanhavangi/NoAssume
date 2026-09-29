---
id: frontend-data-fetching
category: frontend
min_mode: balanced
---

## Fixture

Next.js app router project. Some pages use `fetch` in server components; one
island uses bare `useEffect` fetch — inconsistent.

## Prompt

Load the dashboard stats from the new endpoint.

## Hidden intent

Server component fetch matching the dominant pattern; loading + error
states required; 30s revalidate is fine.

## Must clarify

- Server vs client fetch (RSC vs SWR/React Query/client component)
- Loading and error state requirements
- Caching/revalidation expectations

## Assumption traps

- Pulling in React Query for one component
- `useEffect` fetch copy-pasting the one outlier as if it were the pattern
- No error state — blank panel on API failure
