---
id: api-upload-endpoint
category: api
min_mode: strict
---

## Fixture

Go + Gin API. Existing routes under `internal/api/`, bearer-token middleware
on `/api/*`, Postgres via `sqlc`.

## Prompt

Add an endpoint for file uploads.

## Hidden intent

Internal tool: authenticated like the rest of `/api/*`, max ~25 MB, files go
to the existing S3 bucket the project already configures.

## Must clarify

- Max file size
- Storage backend (repo has S3 config — evidence should resolve this)
- Allowed content types
- Auth scope (same middleware or different?)
- Duplicate filename behavior

## Assumption traps

- Writing to local disk in a containerized service
- Unauthenticated route
- No size limit
