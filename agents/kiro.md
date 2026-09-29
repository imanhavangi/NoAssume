# Kiro

## Install

```bash
./scripts/install.sh kiro           # this workspace
./scripts/install.sh kiro --global  # every workspace
```

## What gets installed

| Path | Purpose |
| --- | --- |
| `.agents/skills/noassume/` | Canonical skill (repo installs). |
| `.kiro/steering/noassume.md` | Always-on steering file (`inclusion: always`) pointing at the skill. |
| `.noassume/config.yaml`, `.noassume/project.md` | Shared policy + project rules (if missing). |
| `.gitignore` | `.noassume/local/` entry added if absent. |

Global installs write the skill to `~/.agents/skills/noassume/` and the
steering file to `~/.kiro/steering/noassume.md`.

## Notes

- Kiro CLI loads every file in `.kiro/steering/` automatically; the
  `inclusion: always` frontmatter is what the IDE requires.
- Custom agents do not automatically inherit workspace steering. To use
  NoAssume inside a custom agent, add the steering files to the agent's
  `resources` explicitly:

  ```json
  { "resources": ["file://.kiro/steering/**/*.md"] }
  ```
- Kiro also reads `AGENTS.md` — installing the `agentsmd` adapter alongside
  `kiro` covers both mechanisms.
