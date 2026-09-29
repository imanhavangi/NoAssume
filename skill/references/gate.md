# The readiness gate

The gate is a binary check, not a score. Scores invite "close enough." A gate
either opens or it does not.

## Criteria

```
READY requires, simultaneously:

  blocking ambiguities          = 0
  material ambiguities          = 0
  unresolved conflicts          = 0
  unprotected-decision attempts = 0
  plan written                  = yes
  Definition of Done written    = yes
```

Everything unresolved at this point must be either delegated or defaultable
under the active config. If any row in `.noassume/local/ambiguities.md` is
still `open` at blocking or material severity, the gate is NOT READY and you
return to Clarify.

## The plan

Write `.noassume/local/plan.md` from `templates/plan.md`. Keep it operational —
the plan is the contract you will be audited against, not a design document:

- **Goal** — one paragraph, the user-visible outcome.
- **Decisions in force** — the decision IDs this implementation depends on.
- **Changes** — files/components touched, what changes in each.
- **Constraints** — negative requirements and protected lines.
- **Validation** — what proves the work: tests, checks, manual verification.
- **Definition of Done** — the checklist an auditor could run mechanically.

## Definition of Done

Derive it from the clarified spec, not from habit:

- functional criteria ("endpoint returns 409 on duplicate slug")
- constraints ("no new host ports", "no new runtime dependencies")
- verification ("`go test ./internal/auth` passes", "compose config validates")
- environment limits ("no docker build run — user constraint")

If the existing project's test culture is unclear, that was an ambiguity —
it should already be resolved or delegated before the gate. "Prototype"
explicitly lowers the bar when the user says so; record that decision too.

## Proceeding

If the user asked for implementation, READY means go. Do not ask "shall I
proceed?" — that question was already answered by the request. Show the plan
compactly and start.

If the user asked only for clarification or planning, stop at the plan and
present it.
