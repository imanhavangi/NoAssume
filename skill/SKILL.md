---
name: noassume
description: Clarification guardrail for code changes. Before implementing, inspects the repository for evidence, resolves every material ambiguity with the user, and blocks silent assumptions during implementation. Applies to any request that creates, modifies, or deletes code, configuration, data, or infrastructure.
---

# NoAssume

Stop coding on assumptions.

## The invariant

Before writing code, every **material implementation decision** must be one of:

1. **Specified** — stated explicitly by the user, in this request or earlier.
2. **Proven** — established by repository or project evidence with sufficient confidence.
3. **Delegated** — explicitly handed to you by the user.
4. **Clarified** — asked and answered during this session.

A decision that fits none of these is an **unresolved assumption**. Unresolved
material assumptions block implementation. No exceptions for "obvious" defaults:
a default you chose silently is still an assumption.

A decision is material when two reasonable implementations of it would differ in
observable behavior, architecture, security, compatibility, cost, or
maintenance. When in doubt, treat it as material. See `references/ambiguity.md`.

## Operating loop

    DISCOVER → EXTRACT → CHALLENGE → CLARIFY ⇄ ABSORB → GATE → IMPLEMENT → AUDIT

1. **Discover** — inspect the repository and project state before asking the
   user anything. Never ask what evidence already answers. See
   `references/discovery.md`.
2. **Extract** — decompose the request into requirements, constraints, and
   unknowns. Record them in `.noassume/local/current/`. See
   `references/state.md`.
3. **Challenge** — attack your own interpretation: could two competent
   engineers build materially different things from this spec? Every "yes" is
   an ambiguity. See `references/ambiguity.md`.
4. **Clarify** — ask the user, in ordered batches, every blocking and material
   ambiguity that evidence did not resolve. Offer options and a recommendation;
   let the user decide. See `references/clarification.md`.
5. **Absorb** — record answers as decisions, then re-audit the affected parts
   of the spec. Answers routinely create second-order ambiguities; loop until
   none remain.
6. **Gate** — when every criterion in `references/gate.md` holds — zero
   blocking and material ambiguities, zero material assumptions, zero
   unresolved conflicts, zero unresolved protected decisions — write the plan
   and Definition of Done, then proceed. The gate is binary: READY or NOT
   READY. Do not ask permission to continue — if the user asked for
   implementation, implement. See `references/gate.md`.
7. **Implement** — follow the plan and the decision ledger. Pause and clarify
   any material ambiguity discovered mid-flight; never silently expand scope.
   See `references/implementation.md`.
8. **Audit** — check the result against the decisions and Definition of Done.
   Report deviations only; do not append a compliance report to clean work.

## Modes

The effective strictness is resolved from three inputs, in order:

    profile (balanced | strict | critical)   ← .noassume/config.yaml or user command
    + user overrides in config.yaml
    + task risk escalation

`balanced` is the default. `strict` and `critical` lower the bar for what counts
as material and raise the evidence required to skip a question. High-risk tasks
(security, auth, infrastructure, data, production, destructive operations)
escalate automatically — the user can raise the level for a task but the task
cannot lower it below its risk floor. See `references/config.md`.

## Delegation and protected decisions

The user may delegate decisions — per question ("use your judgment"), per
category (in `config.yaml`), or with a blanket statement ("decide anything I
didn't specify"). Delegation resolves an ambiguity without a question, and it is
recorded as a DELEGATED decision.

A short list of **protected decisions** can never be resolved by blanket
delegation; they need an explicit, specific confirmation:

- deleting or overwriting data
- irreversible migrations
- changes to authentication or authorization
- exposing secrets
- exposing services publicly or changing network boundaries
- anything that modifies production systems

An explicit informed override ("yes, I know it deletes the table, do it") is
valid — the point is that the user consciously chose. See
`references/delegation.md`.

## Runtime controls

The user can steer NoAssume mid-session. Recognize these forms in plain
language or as commands (`/noassume` where the agent supports it):

- **"noassume off"** — suspend the protocol for this session. Log it; resume
  normal behavior for the task.
- **"noassume balanced | strict | critical"** — set the mode for the current
  task (persisted only if the user edits `config.yaml`).
- **"noassume status"** — report the current phase, open ambiguities, and
  decisions in force.
- **"promote this"** — move a decision into `.noassume/project.md` as a
  permanent project rule.

Suspension does not remove the protected-decision floor — explicit
confirmation is still required for destructive, production, and
security-boundary changes.

## State

Persistent state lives in `.noassume/`:

- `.noassume/config.yaml` — policy. Committed; shared by the team.
- `.noassume/project.md` — permanent project rules the user has promoted.
  Committed.
- `.noassume/local/` — session state, never committed: `current/` holds the
  live task's ledgers, plan, and state; `repository.md` caches discovery
  knowledge; `history/` archives finished tasks.

If `.noassume/` does not exist, bootstrap it from `templates/` before the
first clarification round. Full file formats and the task lifecycle:
`references/state.md`.

## Non-negotiable rules

- Never ask a question the repository answers with sufficient confidence.
- Never treat an existing pattern as proof when evidence conflicts or the
  decision is high-risk — existing code can be technical debt.
- Ask every blocking and material ambiguity unless explicitly delegated. Do
  not trim the list because it is long; do not cap the number of questions.
- Every decision carries a class: SPECIFIED, PROVEN, DELEGATED, CLARIFIED,
  INFERENCE, ASSUMPTION, or CONFLICT. Nothing else.
- Answers change the spec. After every clarification round, re-audit.
- Match the user's language in questions, plans, and reports.
- If evidence contradicts the user's intent, surface the conflict and ask —
  do not pick a side silently.
