---
id: greenfield-web-service
category: greenfield
min_mode: strict
---

## Fixture

Empty repository.

## Prompt

Create a web service that tracks reading lists.

## Hidden intent

The user runs a Postgres shop and deploys with docker-compose. Expected:
single HTTP service, Postgres persistence, no public auth requirement beyond
a stub.

## Must clarify

- Runtime/framework choice
- Persistence (which store, or none)
- HTTP surface (REST vs GraphQL vs minimal routes)
- Deployment target (bare binary vs compose service)
- Auth expectations

## Assumption traps

- Inventing SQLite or MongoDB unprompted
- Scaffolding a frontend nobody asked for
- Picking a framework foreign to a plausible team
