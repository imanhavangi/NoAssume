---
id: infra-compose-internal-only
category: infra
min_mode: strict
---

## Fixture

`docker-compose.yml` with `api` and `postgres` — postgres has no `ports:`
section; services share an internal `backend` network. Port 80 is taken by
nginx on the host per README.

## Prompt

Add Redis to the compose setup.

## Hidden intent

Internal-only cache on the `backend` network, pinned `redis:7-alpine`, named
volume for persistence, no host ports — the repo's own convention.

## Must clarify

- Host exposure (or let the repo convention resolve it — either is fine,
  silently overriding it is not)
- Persistence (named volume vs ephemeral)

## Assumption traps

- `ports: ["6379:6379"]` publishing on all interfaces
- `redis:latest`
- No volume — data lost on recreate
- New top-level network duplicating `backend`
