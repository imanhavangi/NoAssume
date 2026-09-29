# "Add Redis to the compose setup"

The repository already has `api` and `postgres` on an internal `backend`
network. Postgres publishes no host ports.

## Without NoAssume

```yaml
redis:
  image: redis:latest
  ports:
    - "6379:6379"
```

Three silent decisions: `latest` tag, a published host port on every
interface, and no volume — data gone on `docker compose down`.

## With NoAssume

> **[BLOCKING] Host exposure**
> `postgres` publishes no ports and services share the internal `backend`
> network, which suggests Redis should be internal-only — but `ports:` is a
> choice with real consequences.
>
> A. Internal `backend` network only — **recommended**, matches `postgres`
> B. Bind `127.0.0.1:6379` for local tooling
> C. Publish on all interfaces
> D. Other
>
> **[MATERIAL] Persistence**
> Named volume for appendonly data, or ephemeral cache?
>
> A. Ephemeral — it's a cache
> B. Named volume + `appendonly yes` — survives recreation
>
> **[MATERIAL] Image pinning**
> The repo pins `postgres:16-alpine`.
>
> A. `redis:7-alpine` — **recommended**, matches convention
> B. `redis:latest`

User answers: A, B, A.

```yaml
redis:
  image: redis:7-alpine
  command: ["redis-server", "--appendonly", "yes"]
  volumes:
    - redis-data:/data
  networks: [backend]
```

No host port. Persistent. Convention-pinned. The three traps are now three
recorded decisions.
