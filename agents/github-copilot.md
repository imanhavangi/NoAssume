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

- Repository-wide instructions reach Copilot chat, the coding agent, and code
  review. The coding agent also reads `AGENTS.md` — installing the `agentsmd`
  adapter alongside `copilot` covers both entry points.
- Copilot has no native skills mechanism; the instructions block tells the
  agent to read `.agents/skills/noassume/SKILL.md` directly. Any Copilot
  surface that cannot read repository files during a turn gets the core rule
  from the block itself, not the full protocol.
