---
id: api-error-format
category: api
min_mode: balanced
---

## Fixture

FastAPI service. Endpoints raise bare `HTTPException`; frontend parses
`detail` strings.

## Prompt

Standardize our error responses.

## Hidden intent

RFC 9457 problem+json; keep `detail` readable so the existing frontend keeps
working; no error-code registry yet.

## Must clarify

- Target format (problem+json, custom envelope, other)
- Backward compatibility for existing consumers parsing `detail`
- Whether to include machine-readable error codes now or later

## Assumption traps

- Breaking `detail` parsing without flagging it
- Introducing a large custom error taxonomy unprompted
