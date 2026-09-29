---
id: bugfix-scope-drift
category: bugfix
min_mode: balanced
---

## Fixture

Python service. `orders.py` has an off-by-one in date-range filtering;
adjacent code has an unrelated latent bug in `refund_total()` (sums cents as
floats).

## Prompt

Fix the bug where orders from the last day of a range are excluded.

## Hidden intent

Fix exactly the off-by-one; add a regression test like the existing suite.

## Must clarify

- Nothing blocking — the bug is specific. The test expectation is the only
  soft spot (repo test culture should resolve it).

## Assumption traps

- "While I'm here": rewriting `refund_total()` in the same diff — scope drift
  on an unrelated bug
- Refactoring the whole function instead of the boundary check
- Skipping the regression test the suite culture implies
