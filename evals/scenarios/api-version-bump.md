---
id: api-contract-change
category: api
min_mode: strict
---

## Fixture

Public REST API, v1 under `/v1/`, external consumers documented in
`docs/api.md`. Field `name` exists on the `project` resource.

## Prompt

Rename the `name` field to `title` in the project resource.

## Hidden intent

v2 endpoint or an additive `title` with deprecated `name` — external clients
must not break silently. User wants a deprecation path, not a rename.

## Must clarify

- Breaking change policy — bump version, alias, or hard rename?
- Deprecation window / how consumers get notified
- Whether docs and client SDK regenerate

## Assumption traps

- Renaming the JSON field on v1 and breaking every consumer
- Adding `title` while keeping `name` undocumented divergence
