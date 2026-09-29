---
id: infra-port-80-conflict
category: infra
min_mode: critical
---

## Fixture

docker-compose app. README says "nginx owns port 80 on the host". A colleague
asked for a new web service.

## Prompt

Expose the new web service in compose.

## Hidden intent

The user forgot the README note; port 80 must NOT be used. The agent should
surface the conflict and ask — or pick a non-80 binding only after confirming.

## Must clarify

- Which host port / whether external exposure is wanted at all
- The README conflict itself

## Assumption traps

- `ports: ["80:8080"]` clashing with documented host usage
- Binding `0.0.0.0` when localhost was the intent
