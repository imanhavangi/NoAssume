# AGENTS.md-compatible agents

The generic adapter for any agent that reads `AGENTS.md` at the repository
root — which today includes Codex, Copilot coding agent, Kiro, Devin, and a
growing list of others.

## Install

```bash
./scripts/install.sh agentsmd   # this repo
```

## What gets installed

| Path | Purpose |
| --- | --- |
| `.agents/skills/noassume/` | Canonical skill (repo installs). |
| `AGENTS.md` | Managed `noassume` block added — always-on pointer. |
| `.noassume/config.yaml`, `.noassume/project.md` | Shared policy + project rules (if missing). |
| `.gitignore` | `.noassume/local/` entry added if absent. |

## Notes

- If your agent has a dedicated adapter (Codex, Copilot, Kiro, Devin), prefer
  it — it may cover additional surfaces. `agentsmd` exists for everything
  else.
- No global install: the global `AGENTS.md` location differs per tool. Use
  the agent-specific adapter's `--global` flag instead.
- The only requirement is that the agent can read `.agents/skills/noassume/SKILL.md`
  when the block tells it to. Agents that cannot read files mid-task get the
  core rule from the block, not the full protocol — an honest limitation of
  the format.
