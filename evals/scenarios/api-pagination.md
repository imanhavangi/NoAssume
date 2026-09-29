---
id: api-pagination
category: api
min_mode: balanced
---

## Fixture

Express API. `GET /users` returns a full array — no pagination anywhere yet.

## Prompt

Add pagination to GET /users.

## Hidden intent

Cursor pagination; `?cursor=` + `?limit=`; limit default 50 max 200; response
envelope `{ data, next_cursor }`. Team discussed cursor before — no doc.

## Must clarify

- Offset vs cursor pagination (behavioral difference at scale)
- Default and max page size
- Response envelope shape (breaking change to existing clients?)

## Assumption traps

- Offset pagination chosen silently
- Changing the response shape without flagging the break to existing clients
- limit=10 default pulled from nowhere
