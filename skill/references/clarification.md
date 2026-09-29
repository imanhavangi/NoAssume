# Clarification

Clarification is a loop, not a form. Each round asks a batch of questions,
absorbs the answers, and re-audits what the answers changed. There is no cap on
questions or rounds — the cap is redundancy. A question is only legitimate if
the answer could change the implementation.

## Batching

Ask in one message per round, grouped by domain. Order groups so that
load-bearing questions come first:

    Architecture → Runtime → API/behavior → Data → Security →
    Infrastructure → Compatibility → Testing → Deployment

Never ask a question whose options depend on an unanswered earlier question.
If "which database?" is open, "which migration tool?" waits for the next round.

When evidence gives you a likely answer, put it in the question rather than
hiding it — a question with a recommendation is cheaper to answer than an open
one.

## Question format

Each question carries:

- a severity tag — `[BLOCKING]` or `[MATERIAL]`
- what is undecided and why it changes the implementation
- the evidence, if any — "the other services bind only to the docker network"
- options as a multiple-choice list with a marked recommendation, plus `Other`
- "same as existing pattern" when the repository already has one

```text
[BLOCKING] Database exposure

docker-compose.yml has no rule for whether the new Postgres container is
reachable from the host. This decides whether the port is published.

A. Internal Docker network only — recommended; matches how `cache` is wired
B. Bind to localhost only — reachable for local tooling
C. Publish on all interfaces — reachable from the network
D. Other
```

A recommendation tells the user which option fits the repository. It is not a
decision. If the user ignores it, their answer wins.

## Reading answers

Answers land on a spectrum. Classify each one honestly:

- **Decides** — record as CLARIFIED with the decision text.
- **Delegates** — "your call", "whatever fits" — record as DELEGATED and note
  the scope. See `references/delegation.md`.
- **Partial** — answers the easy half. Re-ask the remainder precisely; do not
  stretch a partial answer into a full one.
- **Contradicts** — conflicts with an earlier answer or with evidence. Surface
  the conflict explicitly; do not average the two.
- **Raises new questions** — absorb, then re-audit. A "yes, add auth" answer
  creates questions about mechanism, scope, and failure modes.

## When the user disengages

If the user says "enough questions, just build it," treat the statement as
blanket delegation for ordinary decisions. Record it. Then check what remains
open: protected decisions still require an explicit, specific confirmation —
see `references/delegation.md`. List the protected items, one short line each,
and ask only for those.

## After the loop

When the last re-audit finds nothing unresolved, move to the gate. Do not
announce "clarification complete" as a victory lap — the ledger files are the
record. The user sees the plan next, not a summary of what they already told
you.
