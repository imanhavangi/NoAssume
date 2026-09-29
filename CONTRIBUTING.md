# Contributing

Thanks for helping make NoAssume better. The contributions that move the
project most:

## Eval scenarios — easiest, most valuable

The suite only gets stronger with real failures. If an agent guessed wrong on
something NoAssume should have caught, encode it:

1. Copy any file in `evals/scenarios/` as a template.
2. Fill in the prompt (realistic, under-specified), hidden intent,
   `must clarify`, and assumption traps.
3. The trap list is the test — write what a reasonable agent would
   plausibly ship, not a strawman.

## Ambiguity rules

Domain knowledge belongs in the taxonomy and severity rules — the tables in
`skill/references/ambiguity.md`, `discovery.md`, and `clarification.md`. Good
contributions name a concrete decision agents get wrong (e.g. "lock files in
libraries") and say where it belongs. Keep prose imperative and short — these
files are prompts, not essays.

## Agent adapters

Adding an agent means three things:

1. A row in `ADAPTERS` in `scripts/install.py` — a `Block`, `RuleFile`, or
   `Stub`, chosen to match the agent's native always-on mechanism.
2. A doc page in `agents/` describing what gets installed and any honest
   limitation (e.g. no file-based global config).
3. A matrix row in `agents/README.md`.

Never copy protocol content into an adapter. If the agent can only be reached
through an always-on file, that file carries `agents/pointer.md` verbatim —
the pointer *is* the adapter.

## Config options

New `clarify.*` categories need a real decision domain that isn't covered by
an existing switch, a default that fits the shipped philosophy, and matching
documentation in `templates/config.yaml`, `references/config.md`, and
`docs/configuration.md` — all three, or none.

## Mechanics

- Python 3.9+, no dependencies beyond the stdlib. No build step.
- Run `python3 scripts/check_repo.py` and `python3 scripts/test_install.py`
  before submitting — the first validates internal links, scenario fields,
  config keys, and adapter table integrity; the second covers the installer
  (fresh install, idempotency, conflict handling, uninstall, `--dry-run`,
  `--global`).
- Keep terminology exact: it's "ambiguity", "decision class", "protected
  decision", "informed override" — check `references/` before inventing
  synonyms.
- Small PRs. One adapter, one scenario, or one rule per PR beats a bundle.

## Questions

Open an issue. For "should X be an ambiguity?" discussions, show the two
divergent implementations a competent engineer would produce — that is the
test.
