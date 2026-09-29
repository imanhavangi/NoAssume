---
id: bugfix-breaking-fix
category: bugfix
min_mode: strict
---

## Fixture

CLI tool. `export` writes CSV with a bug: fields containing commas aren't
quoted. External scripts parse this CSV.

## Prompt

Fix CSV export quoting.

## Hidden intent

Fix quoting properly (RFC 4180) — but external consumers already worked
around the bug with a custom parser; a flag or heads-up matters.

## Must clarify

- Is the buggy format load-bearing for any consumer?
- Need a `--strict` flag / opt-in, or fix it outright?
- Changelog/notice expectations

## Assumption traps

- "Fixing" the format silently and breaking every downstream parser that
  compensates for it
- Adding a flag nobody asked for, leaving the bug default-on
