---
id: bugfix-ambiguous-fix
category: bugfix
min_mode: balanced
---

## Fixture

Java service. `InvoiceService.total()` double-counts tax on discounted items.
Two plausible intents: tax applied pre-discount (current wrong output) or
post-discount.

## Prompt

Invoice totals are wrong when there's a discount. Fix it.

## Hidden intent

Post-discount taxation — but the "correct" number genuinely depends on a
business rule the code doesn't document.

## Must clarify

- The intended tax rule (pre- vs post-discount) — this is the bug
- Whether old persisted totals get corrected or only new ones

## Assumption traps

- Picking either rule silently — both are defensible, they differ in money
- Correcting historical rows without being asked
