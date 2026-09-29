# GitHub Copilot

## Install

```bash
./scripts/install.sh copilot           # this repo
./scripts/install.sh copilot --global  # Copilot CLI, every repo
```

## What gets installed

| Path | Purpose |
| --- | --- |
| `.agents/skills/noassume/` | Canonical skill (repo installs). |
| `.github/copilot-instructions.md` | Managed `noassume` block added — repository-wide instructions. |
| `.noassume/config.yaml`, `.noassume/project.md` | Shared policy + project rules (if missing). |
| `.gitignore` | `.noassume/local/` entry added if absent. |

Global installs write the skill to `~/.agents/skills/noassume/` and the
pointer into `~/.copilot/copilot-instructions.md`.

## Notes

- Copilot discovers skills natively, and `.agents/skills/` is one of its
  project skill locations — the vendored skill needs no extra wiring for
  Copilot CLI, the coding agent, code review, and IDE agent modes.
- Native skills load on demand, when the model judges them relevant. The
  repository-wide instructions block remains necessary as the guaranteed
  pre-implementation gate: it is always in context and tells the agent to
  read and follow the skill before writing code.
- The coding agent also reads `AGENTS.md` — installing the `agentsmd`
  adapter alongside `copilot` covers both entry points.
