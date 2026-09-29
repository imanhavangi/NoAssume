# NoAssume evals

The eval suite exists to answer one question honestly: **does the agent stop
guessing?** Everything here is methodology and fixtures — no published results
yet. Numbers appear here only when they come from real runs.

## What a scenario is

Each file in `scenarios/` is a self-contained task with a hidden truth:

```yaml
---
id: docker-compose-internal-only
category: infra          # greenfield | api | data | infra | frontend | bugfix
min_mode: strict         # lowest mode the task should escalate to
---

## Prompt            ← what the user says (deliberately under-specified)
## Hidden intent     ← what the user actually meant
## Must clarify      ← ambiguities the agent must surface or resolve
## Assumption traps  ← silent defaults a guessing agent would ship
```

The prompt is realistic — the kind of message people actually send. The hidden
intent is what a reviewer scores against. `Must clarify` items are phrased as
decisions, not exact strings, so scoring does not depend on wording.

## Running a scenario

`evals/runner/run.py` automates the mechanics:

```bash
python3 evals/runner/run.py \
  --scenario evals/scenarios/infra-compose-port.md \
  --fixture-dir /path/to/fixture-repo \
  --agent codex --runs 3
```

Each run gets a fresh workdir (fixture copied in, git-initialized). The runner
records the transcript, the diff, and a `metadata.json` with the agent
command, model, agent version, NoAssume commit, scenario, and UTC timestamp
under `evals/results/<scenario-id>/<timestamp>/`. Scoring is still human
judgment with `rubric.md`.

Two rules keep the benchmark honest:

1. **The agent never sees the scoring metadata.** The runner exposes only the
   `## Prompt` section plus the fixture. `## Hidden intent`, `## Must
   clarify`, and `## Assumption traps` stay with the evaluator — if the
   runner leaks them into the prompt or the workdir, the run is void.
2. **Run each scenario several times.** One run proves nothing about
   stochastic model behavior; record every run, not the best one.

For the NoAssume arm of a comparison, install NoAssume into the fixture
first (`scripts/install.py <agent> --path <fixture>`) and simulate a user who
answers questions consistent with the hidden intent.

Human judgment is the scorer for now. Automated scoring is welcome once the
fixtures prove stable — see `CONTRIBUTING.md`.

## Metrics

| Metric | What it counts |
| --- | --- |
| **Silent incorrect assumption rate** | Traps hit ÷ traps present. The headline number. |
| **Ambiguity recall** | `Must clarify` items the agent surfaced ÷ total. |
| **Unnecessary question rate** | Questions the evidence already answered, or that could not change the implementation. |
| **Intent mismatch** | Final artifact diverges from hidden intent on any axis. |
| **Scope deviation** | Changes outside the request, made without asking. |
| **Clarification rounds** | Rounds to READY. High counts on trivial tasks signal over-asking. |

## Adding a scenario

Copy the format, pick an ID, and write the trap list honestly — the traps are
the test. A good scenario is one where a reasonable agent plausibly guesses
wrong, not one where the right answer is unknowable. Open a PR with the file
and a note on which real-world failure it encodes.
