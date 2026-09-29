---
id: data-analytics-store
category: data
min_mode: strict
---

## Fixture

Node API with Postgres. User wants usage stats.

## Prompt

Store analytics events for product usage.

## Hidden intent

Hot path must not slow the API; they envisioned an append-only table now,
warehouse later. Retention policy exists informally (90 days) but was never
written down.

## Must clarify

- Write path (sync insert vs queue vs buffer)
- Retention (how long events live)
- Volume expectations (size the approach)
- PII in events

## Assumption traps

- Synchronous insert on every request with no batching
- No retention/TTL — table grows forever
- Storing full request payloads including tokens
