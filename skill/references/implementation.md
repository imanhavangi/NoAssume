# Implementation guard

Reaching READY does not retire NoAssume — it changes jobs. During
implementation you are a guard, not a gatekeeper: you watch for two failure
modes and stop them early.

## Stay on the ledger

Every material choice in the code should trace to a decision row. When you are
about to do something the ledger does not cover — a new dependency, a new
network binding, a schema tweak that proved necessary, an extra refactor —
that is a new ambiguity discovered mid-flight.

The response is mechanical:

1. Pause that line of work.
2. Record it in the ambiguity ledger.
3. Clarify if it is blocking or material and not already delegated.
4. Update the decision ledger and plan.
5. Resume.

Do not finish the work first and mention it in a summary. The longer an
unverified assumption sits in the diff, the harder it is to see.

## Scope drift

The second failure mode is the diff growing past the request. The test is not
"is this a good change" — it is "is this change required by the clarified
spec."

- **Required collateral** — a fix the change cannot land without (an import, a
  call-site update, a broken assertion the new code exposes). In scope; note it
  in the plan.
- **Tempting collateral** — renaming the module while you are in it, upgrading
  the dependency you are near, fixing an unrelated bug you noticed. Out of
  scope unless trivial and safe; otherwise record it and ask, or leave it and
  report it at the end as a suggestion, not a fait accompli.

When in doubt, the question is cheap: "Found X while implementing — fix it here
or leave it?"

## If reality breaks the plan

Sometimes the clarified design fails against the actual code — the API does
not support it, the data does not look like the docs said. That is a conflict
between the plan and evidence. Treat it like any conflict: stop, surface it,
re-plan. Never silently swap in your own plan B for a decision the user made.

## The audit

Before reporting done, run the audit against `plan.md` and the ledgers:

- every decision in force was honored
- every Definition of Done item was verified or explicitly could not be
- no unclarified ambiguity got implemented anyway
- no scope drift beyond what was recorded

Clean work gets no ceremony — report normally. A deviation gets a specific
report:

```text
Deviation from DEC-014 (internal-only Redis): the compose file currently
publishes 6379 on the host because the internal network did not cover the
CLI container. Fix requires wiring `cli` into the `backend` network or an
explicit override of DEC-014.
```

Deviations are resolved by fixing them or by an explicit user override —
never by hiding them.
