# Devin

## Install

```bash
./scripts/install.sh devin           # this repo
./scripts/install.sh devin --global  # every repo
```

## What gets installed

| Path | Purpose |
| --- | --- |
| `.agents/skills/noassume/` | Canonical skill (repo installs). |
| `.devin/rules/noassume.md` | Always-on rule (`trigger: always_on`) pointing at the skill. |
| `.noassume/config.yaml`, `.noassume/project.md` | Shared policy + project rules (if missing). |
| `.gitignore` | `.noassume/local/` entry added if absent. |

Global installs write the skill to `~/.agents/skills/noassume/` and the rule
to `~/.devin/rules/noassume.md`.

## Notes

- Devin also reads `AGENTS.md`, `CLAUDE.md`, and `.cursor/rules/` — the
  `.devin/rules/` file is the native mechanism and is what the installer
  uses.
- Devin's own guidance recommends keeping always-on rules small and pointing
  at skills — which is exactly what this rule does. The heavy content stays
  in the skill's `references/` and loads on demand.
