# State

NoAssume keeps state on disk so that clarification survives context limits,
session boundaries, and context compaction — and so decisions are inspectable
rather than remembered.

## Layout

```
.noassume/
├── config.yaml          committed — policy and clarify switches
├── project.md           committed — permanent project rules
└── local/               gitignored — everything below
    ├── decisions.md     decision ledger
    ├── ambiguities.md   ambiguity ledger
    ├── assumptions.md   every assumption and inference, resolved or not
    ├── plan.md          current implementation contract
    ├── state.md         task state + cached repository knowledge
    └── history/         ledgers from finished tasks, named by date+slug
```

`.noassume/local/` must be in `.gitignore`. The installer handles this; if it
is missing, add it before writing ledgers.

## Bootstrap

If `.noassume/` does not exist when a task starts, create it:

1. Copy `templates/config.yaml` → `.noassume/config.yaml` (never overwrite an
   existing one).
2. Copy `templates/project.md` → `.noassume/project.md` (never overwrite).
3. Create `.noassume/local/` and ensure it is gitignored.
4. Copy the ledger templates in only as needed — create each file when it
   first gets a row.

## Decision classes

Every row in `decisions.md` carries exactly one class:

| Class | Meaning | Source required |
| --- | --- | --- |
| SPECIFIED | User stated it in this request | quote or paraphrase of the request |
| CLARIFIED | User answered it during clarification | the question ID it resolved |
| PROVEN | Evidence in the repo/project answers it | file path or doc citation |
| DELEGATED | User explicitly let you decide | scope of the delegation |
| INFERENCE | Evidence suggests but does not prove | the evidence + why it falls short |
| ASSUMPTION | Nothing supports it | must be empty at READY |
| CONFLICT | Two sources disagree | both sources cited |

## Ledgers

`decisions.md` — the decisions in force. Format per row:

```markdown
### DEC-001 — Backend runtime
- Class: PROVEN
- Decision: Go 1.23
- Source: go.mod
- Scope: repository
```

`ambiguities.md` — everything found in Challenge and mid-flight, open or
resolved:

```markdown
### AMB-003 — Redis host exposure
- Domain: networking
- Severity: blocking
- Status: resolved → DEC-014
- Asked: round 2
```

`assumptions.md` — every INFERENCE and ASSUMPTION, including ones later
resolved. The point is the audit trail: at READY, no open ASSUMPTION may be
material, and every INFERENCE shows its evidence.

## `project.md` — permanent rules

When the user says a decision should always hold — "never publish database
ports here", "Go for all backend services" — promote it: move the decision
from the session ledger into `.noassume/project.md` under a clear heading.
Project rules outrank repo patterns in the evidence hierarchy and apply to
every future task.

Keep project.md human: short imperative rules, grouped by domain. It is
committed, so it is also the team's interface to NoAssume's behavior.

## `state.md` — session continuity

Tracks the current task: request summary, lifecycle phase, clarification round
count, open items. The `## Repository knowledge` section caches discovery
findings (runtimes, conventions, infra topology) so later tasks can verify
instead of re-scanning from zero — see `references/discovery.md`.

## History

When a task finishes, move its ledgers into `local/history/YYYY-MM-DD-slug.md`
instead of deleting them. Resolved ambiguities teach the next task what this
project cares about.
