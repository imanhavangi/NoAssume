# Gemini CLI

## Install

```bash
./scripts/install.sh gemini           # this repo
./scripts/install.sh gemini --global  # every repo
```

## What gets installed

| Path | Purpose |
| --- | --- |
| `.agents/skills/noassume/` | Canonical skill (repo installs). |
| `GEMINI.md` | Managed `noassume` block added — loaded with every prompt. |
| `.noassume/config.yaml`, `.noassume/project.md` | Shared policy + project rules (if missing). |
| `.gitignore` | `.noassume/local/` entry added if absent. |

Global installs write the skill to `~/.agents/skills/noassume/` and the
pointer into `~/.gemini/GEMINI.md`.

## Notes

- If your `settings.json` sets a custom `context.fileName`, the installer
  still writes `GEMINI.md`; rename the file or extend the list to include it.
- `GEMINI.md` files in subdirectories also work — the installer targets the
  repository root.
