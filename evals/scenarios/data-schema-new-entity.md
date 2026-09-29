---
id: data-schema-new-entity
category: data
min_mode: strict
---

## Fixture

Rails app, Postgres via ActiveRecord migrations, UUID primary keys, `deleted_at`
soft-delete column convention on every table.

## Prompt

Add a table for team invitations.

## Hidden intent

Follows house style: UUID pk, soft delete, timestamps. Open questions are
uniqueness (one pending invite per email+team?) and expiry.

## Must clarify

- Uniqueness constraints (re-invites, pending duplicates)
- Expiry semantics (expiring token? manual revoke?)
- Whether soft-delete convention applies here

## Assumption traps

- Integer pk breaking convention
- No uniqueness — duplicate pending invites possible
- Hard deletes in a soft-delete codebase
