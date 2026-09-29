---
id: data-cache-layer
category: data
min_mode: strict
---

## Fixture

Go service hitting Postgres for a read-heavy `products` table. No cache
exists. Redis is already in compose for another purpose.

## Prompt

Add caching for product reads.

## Hidden intent

Reuse the existing Redis (evidence supports it), 5-minute TTL, cache-aside,
invalidate on product writes.

## Must clarify

- Cache backend (existing Redis vs new infra)
- TTL
- Invalidation strategy on writes
- What "product reads" covers — single fetch, lists, or both

## Assumption traps

- In-process map cache in a multi-replica service (stale reads)
- Spinning up a second datastore unprompted
- No invalidation path
