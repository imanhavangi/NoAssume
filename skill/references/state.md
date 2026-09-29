# State

NoAssume keeps state on disk so that clarification survives context limits,
session boundaries, and context compaction — and so decisions are inspectable
rather than remembered.

## Layout

```
.noassume/
├── config.yaml            committed — policy and clarify switches
├── project.md             committed — permanent project rules
└── local/                 gitignored — everything below
    ├── repository.md      cached repository knowledge — persists across tasks
    ├── current/           the task in flight
    │   ├── state.md       request summary, phase, round, open items
    │   ├── decisions.md   decision ledger
    │   ├── ambiguities.md ambiguity ledger
    │   ├── assumptions.md every assumption and inference, resolved or not
    │   └── plan.md        current implementation contract
    └── history/           one directory per finished task — audit trail only
        └── 2026-09-29T09-42-11-add-redis/
```

`.noassume/local/` must be in `.gitignore`. The installer handles this; if it
is missing, add it before writing ledgers.

## Bootstrap

If `.noassume/` does not exist when a task starts, create it:

1. Copy `templates/config.yaml` → `.noassume/config.yaml` (never overwrite an
   existing one).
2. Copy `templates/project.md` → `.noassume/project.md` (never overwrite).
3. Create `.noassume/local/`, `local/current/`, and `local/history/`; ensure
   `local/` is gitignored.
4. Copy ledger templates from `templates/` into `local/current/` only as
   needed — create each file when it first gets a row.

## Decision classes

Every row in `decisions.md` carries exactly one class:

| Class | Meaning | Source required |
| --- | --- | --- |
| SPECIFIED | User stated it in this request | quote or paraphrase of the request |
| CLARIFIED | User answered it during clarification | the question ID it resolved |
| PROVEN | Evidence in the repo/project answers it | file path or doc citation |
| DELEGATED | User explicitly let you decide | scope of the delegation |
| INFERENCE | Evidence suggests but does not prove | the evidence + why it falls short |
| ASSUMPTION | Nothing supports it | must be resolved before READY when material |
| CONFLICT | Two sources disagree | both sources cited |

An INFERENCE never closes a material ambiguity by itself. Evidence that
suggests is not authorization: an inference becomes a decision only when the
user answers it (CLARIFIED), explicitly delegates it (DELEGATED), or stronger
evidence proves it (PROVEN).

## Ledgers

`local/current/decisions.md` — the decisions in force. Format per row:

```markdown
### DEC-001 — Backend runtime
- Class: PROVEN
- Decision: Go 1.23
- Source: go.mod
- Scope: repository
```

`local/current/ambiguities.md` — everything found in Challenge and
mid-flight, open or resolved:

```markdown
### AMB-003 — Redis host exposure
- Domain: networking
- Severity: blocking
- Status: resolved → DEC-014
- Asked: round 2
```

`local/current/assumptions.md` — every INFERENCE and ASSUMPTION, including
ones later resolved. The point is the audit trail: at READY, no open
ASSUMPTION may be material, and every INFERENCE shows its evidence.

## `repository.md` — discovery cache

The first task in a repository does a deep discovery pass and records what it
learned in `local/repository.md`: runtimes, conventions, infra topology,
environment constraints — each fact with its evidence and the date it was
verified (format: `templates/repository.md`).

The cache persists across tasks. Later tasks reuse it, but only after
verifying it still holds for the area being touched — see
`references/discovery.md`. When reality disagrees with the cache, re-scan and
update it. It is a cache, not a source of truth.

## `state.md` — session continuity

`local/current/state.md` tracks the current task: request summary, lifecycle
phase, clarification round count, open items.

## Task lifecycle

**Starting.** If `local/current/state.md` already exists and its phase is not
finished, a previous task was interrupted. Ask the user: resume it, or archive
it unfinished into `local/history/` and start fresh. Never silently discard an
interrupted task's ledgers.

**During.** All task records live under `local/current/`. Decision and
ambiguity IDs start at 001 with each task and are unique within it. When you
must cite a decision from an earlier task, cite it with its history directory:
`DEC-014 (2026-09-29T09-42-11-add-redis)`.

**Finishing.** When a task ends, move `local/current/*` into
`local/history/<UTC timestamp>-<slug>/`, then reset `current/` for the next
task: fresh request summary, phase DISCOVER, round 0, IDs from 001.

**What carries forward.** Only two things influence future tasks:
`project.md`, when the user promotes a rule into it, and evidence re-derived
from the repository. `repository.md` is a cache to verify, `history/` is an
audit trail to consult — neither is authority. A repository-scoped decision
that was not promoted does not bind the next task; if it becomes relevant
again, re-derive it from evidence or ask.

## History

`local/history/` is an audit trail, not a source of truth. Reading a past
task's ledgers shows what this project cared about and how similar questions
were answered — useful context for asking better questions. It never decides
anything: yesterday's resolved ambiguity is not today's answer unless the
evidence or a promoted rule in `project.md` still says so.
