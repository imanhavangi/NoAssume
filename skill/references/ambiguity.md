# Ambiguity

An ambiguity is a decision the implementation needs but nobody has made. Your
job in **Challenge** is to find all of them before the user finds them for you —
usually after the code is written.

## The materiality test

A decision is **material** when two competent engineers, given the same request
and the same repository, could implement it differently in a way the user would
notice or pay for:

- observable behavior, API shape, error semantics
- architecture, placement, boundaries
- data model, persistence, retention, migration safety
- security, permissions, secret handling
- network exposure, ports, protocols
- compatibility — breaking changes, version support
- dependencies added or replaced
- deployment, rollout, rollback
- cost — paid APIs, cloud resources, license-restricted libraries

A decision is **not material** when every reasonable choice is equivalent for
the user: local variable names, comment style, internal helper structure —
unless the repository itself lacks a convention and the choice would be
visible.

The test to run on every open decision: **the two-engineer test**. Write the
specification as it stands. If two competent engineers could walk away and
build materially different things, the spec still contains ambiguity.

## Severity

Every ambiguity gets one of three severities:

- **blocking** — the implementation cannot start without it, or getting it
  wrong is expensive to undo: runtime choice for a greenfield service, a data
  model, anything touching a protected decision, any unresolved CONFLICT.
- **material** — the implementation will pick one branch or the other and the
  branches differ in ways the user cares about.
- **defaultable** — a choice the active config delegates or that repository
  convention settles with sufficient confidence. Recorded as DELEGATED
  (source: `config.yaml`) or PROVEN (source: the convention) — never silent.
  A choice that is neither delegated nor proven stays material and gets
  asked.

Blocking and material ambiguities must reach zero before the gate opens.

## Finding ambiguities

Work the request against the taxonomy below. For each domain, ask: *does the
request or the evidence decide this?*

| Domain | Questions it hides |
| --- | --- |
| Scope | What changes, what must not change, what is out of scope? |
| Behavior | Happy path, edge cases, empty/error/loading states? |
| Architecture | New or existing component? Boundary placement? |
| Runtime | Language, version, framework — or does the repo already decide? |
| API | Contract, status codes, pagination, versioning, breaking changes? |
| Data | Schema, ownership, retention, migration, existing rows? |
| Security | Auth required? Authorization model? Secret handling? |
| Networking | Host exposure, ports, protocols, TLS, internal-only? |
| Infrastructure | New services, volumes, networks, resource limits, healthchecks? |
| Dependencies | Add, replace, pin? License constraints? |
| Compatibility | Backward compatibility window? Consumers to keep working? |
| Reliability | Timeouts, retries, ordering, failure behavior? |
| Observability | Logs, metrics, tracing — or existing conventions suffice? |
| Testing | What proves it works? Which suite owns the test? |
| Deployment | How does it ship, roll back, get configured per environment? |
| Environment constraints | Things the agent may not run: builds, migrations, deploys. |

This list is a floor, not a ceiling. Any domain the task touches is in scope.

## Assumption traps

Hunt your own reasoning for decision-shaped claims wearing default costumes:
"probably", "typically", "the standard way", "it makes sense to", "by default",
"I'll use", "we can just". Each one is either a decision with evidence behind
it or an assumption. Check which.

Also hunt **implicit choices**: decisions the request forces without stating
them. "Add a search endpoint" implies an indexing strategy, a query language, a
relevance model, and an authorization boundary — none of which were said out
loud.

And hunt **second-order ambiguities**: decisions created by earlier answers.
"Use PostgreSQL" spawns version, schema ownership, migration tooling,
connection lifecycle, and persistence questions. Absorbing answers is not the
end of clarification; it is the input to the next audit.

## Negative requirements

What must *not* change is as load-bearing as what must. Extract prohibitions
explicitly: no new dependencies, no public ports, no schema changes, no API
contract changes, no refactor beyond the touched code. When the request is
silent on scope boundaries and the task could plausibly spill, ask.

## Recording

Every ambiguity is a row in `.noassume/local/current/ambiguities.md` with an
ID, the question, domain, severity, and status. Never track ambiguity only in
your head — the ledger is what makes the loop auditable.
