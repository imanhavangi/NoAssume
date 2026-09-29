# NoAssume

Stop coding on assumptions.

Coding agents are optimized to start working, not to ask questions. Give one a
prompt like "add Redis to the compose setup" and it will happily publish
`6379` on every interface, pin `redis:latest`, and skip the volume — three
decisions you never made, shipped without a word.

NoAssume is a skill that puts a gate in front of that. Before implementing,
the agent inspects your repo for evidence, asks you about every decision the
evidence can't settle, and refuses to proceed while material ambiguity
remains. During implementation, it keeps guarding: new questions pause work,
scope drift gets surfaced, and the diff is audited against the decisions.

## What it looks like

```text
You:   Add Redis to the compose setup.

Agent: [BLOCKING] Host exposure — postgres publishes no ports and services
       share the internal `backend` network, which suggests Redis should be
       internal-only. But publishing is a real choice:

         A. Internal backend network only — recommended, matches postgres
         B. Bind 127.0.0.1:6379 for local tooling
         C. Publish on all interfaces

       [MATERIAL] Persistence — named volume + appendonly, or ephemeral cache?
       [MATERIAL] Image — pin redis:7-alpine to match convention, or latest?
```

Three questions replace three wrong guesses. More in `examples/`.

## Quick start

Clone this repo, then point the installer at yours:

```bash
git clone https://github.com/imanhavangi/NoAssume.git
cd NoAssume
./scripts/install.sh codex --path ~/code/my-project
./scripts/install.sh codex claude cursor --path ~/code/my-project   # several
./scripts/install.sh codex --global                                 # all repos
```

Windows: `scripts/install.ps1` with the same arguments. Remove with
`--uninstall`; preview with `--dry-run`. Python 3.9+ is the only requirement
(CI checks 3.9–3.13).

The installer vendors the canonical skill into `.agents/skills/noassume/`,
creates `.noassume/` for configuration and state, and writes one always-on
pointer into whatever mechanism your agent reads — `AGENTS.md`, `CLAUDE.md`,
a Cursor rule, a Kiro steering file, etc. It never edits existing lines of
your files; it manages one marked block you can delete cleanly, plus
dedicated files it owns and will not touch if it did not create them.

## Updating

Pull a newer NoAssume and re-run the installer; it refreshes the vendored
skill and pointers in place:

```bash
cd NoAssume && git pull
./scripts/install.sh codex --path ~/code/my-project
```

Your `.noassume/config.yaml`, `project.md`, and `local/` history are never
touched by an update.

## Supported agents

Codex, Claude Code, Cursor, GitHub Copilot, Gemini CLI, Kiro, Devin, and any
agent that reads `AGENTS.md`. Per-agent specifics and honest limitations:
`agents/README.md`.

## How it works

```text
DISCOVER → EXTRACT → CHALLENGE → CLARIFY ⇄ ABSORB → GATE → IMPLEMENT → AUDIT
```

- **Discover** — the repo is read first; questions it can answer never reach you.
- **Challenge** — the spec is attacked on purpose: could two engineers build
  different things from it? Each "yes" becomes a question.
- **Clarify** — batched questions with options and a recommendation. Answers
  are absorbed, then the spec is re-audited — answers create new questions.
- **Gate** — binary: zero blocking and material ambiguities, or it doesn't
  open. Then a plan and Definition of Done are written and work starts —
  no "shall I proceed?" ceremony.
- **Guard** — during implementation, new ambiguity pauses work, drift is
  flagged, and the result is audited against the recorded decisions.

Full lifecycle spec: `skill/SKILL.md` + `skill/references/`. Design
rationale: `docs/architecture.md`.

One honest caveat: NoAssume is an instruction-layer guardrail. It strongly
steers every agent it is installed into, but it cannot technically block a
file write when a host or model ignores its instructions.

## Configure it

`.noassume/config.yaml` is committed and shared by the team. Fourteen
categories can be delegated wholesale, three modes set the baseline, and task
risk escalates automatically:

```yaml
mode: balanced          # balanced | strict | critical
clarify:
  dependencies: true    # ask before adding libraries
  naming: false         # stop asking about names
```

Permanent project rules ("databases never publish host ports") live in
`.noassume/project.md`. Session state stays in `.noassume/local/`, which is
gitignored. Details: `docs/configuration.md`.

One boundary can't be configured away: destructive operations, auth changes,
secrets, public exposure, and production changes need an explicit yes —
"use your judgment" doesn't cover them.

## Evals

`evals/` holds 24 scenarios — realistic prompts with hidden intent and the
assumption traps a guessing agent hits — plus the rubric for scoring bare vs.
NoAssume runs. The suite is a methodology and fixtures; no benchmark results
are published yet. Contributions of scenarios that encode real failures are
especially welcome.

## Contributing & license

`CONTRIBUTING.md` covers new ambiguity rules, agent adapters, and eval
scenarios. MIT — see `LICENSE`.
