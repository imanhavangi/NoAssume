# Claude Code

## Install

```bash
./scripts/install.sh claude           # this repo
./scripts/install.sh claude --global  # every repo
```

## What gets installed

| Path | Purpose |
| --- | --- |
| `.agents/skills/noassume/` | Canonical skill (repo installs). |
| `CLAUDE.md` | Managed `noassume` block added — always-on pointer. |
| `.claude/skills/noassume/SKILL.md` | One-line stub so `/noassume` resolves to the canonical skill. |
| `.noassume/config.yaml`, `.noassume/project.md` | Shared policy + project rules (if missing). |
| `.gitignore` | `.noassume/local/` entry added if absent. |

Global installs write the skill to `~/.agents/skills/noassume/`, the pointer
into `~/.claude/CLAUDE.md`, and the stub into `~/.claude/skills/noassume/`.

## Notes

- The stub is a pointer, not a copy — protocol changes ship with the
  canonical skill, not the stub.
- `/noassume` invokes the skill by name. Mode changes are conversational:
  "run this one in strict" works in any session.
