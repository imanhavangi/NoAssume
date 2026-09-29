# "Add an endpoint for file uploads"

Gin API, bearer-auth on `/api/*`, S3 client already configured in
`internal/storage/`.

## Without NoAssume

The agent writes a handler that saves to `./uploads/` on local disk — a
containerized service where local disk is ephemeral and unreplicated. No
size limit. No auth check beyond the route group it happened to land in.

## With NoAssume

Discovery proves two things for free — auth middleware already wraps
`/api/*` (PROVEN, no question) and S3 is configured (PROVEN, with a caveat:
configured doesn't mean intended for this). What remains:

> **[BLOCKING] Storage backend**
> `internal/storage` already wires an S3 client — evidence suggests S3, but
> "configured" isn't "intended."
>
> A. S3 via the existing client — recommended
> B. Postgres blob column
> C. Local disk — flag: ephemeral on this deploy
>
> **[BLOCKING] Size limit**
>
> A. 25 MB — recommended for an internal tool
> B. 100 MB
> C. Configurable via env
>
> **[MATERIAL] Content types**
>
> A. Allowlist: images + PDF
> B. Any type, rely on auth
> C. Other
>
> **[MATERIAL] Duplicate filenames**
>
> A. UUID-prefixed keys — recommended
> B. Overwrite
> C. Reject with 409

Four questions, one round. The handler that gets written streams to S3 with
a 25 MB cap and an allowlist — and `.noassume/local/decisions.md` shows why
every line looks the way it does.
