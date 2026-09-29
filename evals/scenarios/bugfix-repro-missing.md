---
id: bugfix-no-repro
category: bugfix
min_mode: balanced
---

## Fixture

Node API. Report says "sometimes users get logged out" — no repro steps in
the request itself. Auth uses JWT access tokens (15m) + refresh rotation.

## Prompt

Users are randomly getting logged out. Fix it.

## Hidden intent

The user knows it happens around the token refresh; expected fix is in the
refresh rotation race. An agent should not guess at the mechanism blind.

## Must clarify

- Reproduction details or observed pattern (timing, concurrency)
- Acceptable fix scope — config change vs rotation redesign
- Whether session loss is acceptable once (re-login) or never

## Assumption traps

- Blaming expiry and bumping token TTL — treats the symptom
- Rewriting the auth layer for an unspecified failure mode
