# Discovery

Discovery answers one question: **what is already known?** It runs before any
question is asked. A question the repository can answer is a wasted question —
and wasted questions train users to dismiss the ones that matter.

## What to inspect

Scan the surfaces that can constrain the implementation, not just the code you
expect to touch:

- **Entry points and structure** — directory layout, package manifests
  (`package.json`, `go.mod`, `pyproject.toml`, `Cargo.toml`, `pom.xml`), build
  files, workspace configuration.
- **Agent and project instructions** — `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
  `.cursor/rules/`, `.devin/`, `.kiro/`, `.github/copilot-instructions.md`, and
  `.noassume/project.md` itself.
- **Documentation** — `README*`, `docs/`, architecture decision records,
  `CONTRIBUTING.md`, wikis vendored in the repo.
- **Tests** — test layout, frameworks, fixtures, CI-required checks. The test
  culture of the project is itself evidence.
- **Infrastructure** — `Dockerfile*`, `docker-compose*.y*ml`, `.github/` and CI
  configs, Kubernetes manifests, Helm, Terraform, Pulumi, Nginx/Caddy configs,
  `Procfile`, systemd units.
- **Runtime configuration** — `.env.example`, `config/` files, feature flags,
  settings modules. These reveal ports, endpoints, and integration points.
- **Git history** — `git log` for recent patterns, `git blame` on files you will
  touch, commit message conventions. History often reveals intent the code
  hides.
- **Comments and TODOs** — inline rationale, `TODO`, `FIXME`, `HACK`, `NOTE`.
- **Existing implementations** — the strongest evidence for conventions. If
  three services in the repo log JSON via the same helper, that is a pattern,
  not a coincidence.
- **Remote context** — issues, PRs, and discussions when the environment
  exposes them. Optional; never required.

Generic web research is not discovery. Do not search the internet to answer a
question about this repository.

## Incremental discovery

The first task in a repository does a deep pass. Record what you learned in
`.noassume/local/repository.md`.

Later tasks reuse that knowledge — but only after verifying it still holds for
the area you are touching. Manifests change; conventions drift. Re-scan deeply
when the task is architectural, when prior knowledge conflicts with what you
see, or when the cached facts are stale.

Depth is the requirement; redundancy is not. Skipping a re-scan of an unchanged
area is efficient. Skipping discovery is a violation.

## Evidence hierarchy

When you claim a decision is resolved by evidence, know what kind of evidence
you are standing on:

1. Explicit instruction in the current request
2. Explicit instruction earlier in the session
3. A permanent rule in `.noassume/project.md`
4. Current documentation or architecture records
5. The actual implementation you are extending
6. An established convention repeated across the repository
7. A generic ecosystem convention ("this is how it's usually done")
8. Your own preference

Levels 7 and 8 are not evidence for material decisions. Level 6 earns
confidence proportional to how consistently the pattern repeats. Levels 4–5 are
strong but can be stale or wrong — code can be technical debt and docs can be
aspirational.

## Conflicts

When two sources disagree — the README says Node 20 and the Dockerfile says
`node:22` — that is a **CONFLICT**, not a fact. Record it in the ambiguity
ledger. Surface it to the user with both sources cited. Never silently pick the
source you prefer.

The same applies when the user's request contradicts repository evidence.
Surface the conflict. The user decides whether the request overrides the
pattern or was based on a wrong assumption.

## Confidence

Evidence resolves an ambiguity only when it does so with **sufficient
confidence**. Sufficient means: you could defend the answer to the user with a
citation, not a hunch.

The confidence bar rises with risk. For `naming: false` trivia, a consistent
convention is enough. For a destructive or security-sensitive decision, nothing
short of an explicit statement or permanent rule is enough — no amount of
pattern-matching substitutes for the user's answer.

When evidence is suggestive but not conclusive, you may ask the question with
your inference attached:

> Session storage is unclear. The existing code stores auth tokens in Redis
> (`internal/auth/store.go`), which suggests Redis is intended for ephemeral
> state. Should the new session store use the same?

That is a question backed by evidence, not an assumption wearing a costume.

## Output

Discovery produces facts, not conclusions. Every fact enters the decision
ledger as PROVEN with its source. Everything the evidence suggested but could
not prove enters as INFERENCE. Everything unresolved stays open for Challenge.
