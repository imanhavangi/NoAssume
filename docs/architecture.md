# Architecture

NoAssume is deliberately one thing: a guardrail between "the user asked" and
"the agent implemented." This page explains the shape; the normative spec is
`skill/SKILL.md` plus `skill/references/`.

## Two layers, one source of truth

```
agents/pointer.md  ── always-on shim, one per agent mechanism
        │
        ▼  "read and follow this"
.agents/skills/noassume/
        ├── SKILL.md        invariant + operating loop
        ├── references/     detail, loaded on demand
        └── templates/      .noassume/ file formats
```

The pointer is ~10 lines and identical everywhere — an always-on rule that
forces the canonical skill to load. All behavior lives in the skill. This
means protocol changes ship once, not once per agent.

Why always-on instead of a discoverable skill? Because a skill the model may
decline to load is optional, and an optional guardrail is decorative. The
pointer is small on purpose — it carries the invariant itself, so an agent
that can only read instructions (not files mid-task) still gets the core
rule.

## The lifecycle

    DISCOVER → EXTRACT → CHALLENGE → CLARIFY ⇄ ABSORB → GATE → IMPLEMENT → AUDIT

The unusual parts:

- **Discovery precedes questions.** Every question the repo could answer is
  wasted. The evidence hierarchy (`references/discovery.md`) ranks sources;
  generic conventions and model preference are not evidence.
- **Clarification loops.** Answers create second-order ambiguities. Each
  round re-audits the spec; rounds end at zero, not at a budget.
- **The gate is binary.** READY requires zero blocking ambiguities, zero
  material ambiguities, zero unresolved conflicts — plus a written plan and
  Definition of Done. No score, no "close enough."
- **The guard outlives the gate.** After READY the protocol keeps watching:
  mid-flight ambiguities pause work, scope drift gets surfaced, and a final
  audit compares the diff to the ledger.

## State on disk

`.noassume/` splits by audience:

| Path | Committed? | Purpose |
| --- | --- | --- |
| `config.yaml` | yes | Team policy — modes and clarify switches |
| `project.md` | yes | Permanent rules the user promoted from decisions |
| `local/` | no | Ledgers, plan, discovery cache, history |

The split exists because decisions have two lifetimes: this task's
(scrapbook) and this project's (law). Promoting a session decision to
`project.md` is how "don't publish database ports" stops being re-asked.

## Decision classes

Nothing resolves silently. Every decision is labeled SPECIFIED, CLARIFIED,
PROVEN, DELEGATED, INFERENCE, ASSUMPTION, or CONFLICT — the label is the
audit trail. `references/state.md` defines the ledgers.

## Delegation has one wall

Users can delegate anything — per question, per category, or blanket —
**except** the protected list (destructive ops, auth changes, secrets, public
exposure, production, irreversible migrations). Those need an informed
override: the consequence named, the user choosing anyway. `references/
delegation.md` is the spec.

## Strictness is layered

```
mode (config) → clarify switches → task-risk floor
```

Profiles set the baseline; switches delegate whole categories; task risk
escalates automatically for work that can hurt. A `balanced` user touching
auth gets critical-level scrutiny on the auth parts. Users can always go
stricter; the task's risk floor only moves up.

## What NoAssume is not

Not a planner (the plan exists to constrain implementation, not to design
products). Not a spec framework — it works alongside Spec Kit, Kiro specs, or
plain prompting. Not a linter — it gates decisions, not syntax. The scope is
kept narrow because the failure it fixes is narrow and real: agents
implementing assumptions instead of intent.
