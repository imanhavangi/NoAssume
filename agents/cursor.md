# Cursor

## Install

```bash
./scripts/install.sh cursor   # this repo
```

## What gets installed

| Path | Purpose |
| --- | --- |
| `.agents/skills/noassume/` | Canonical skill. Cursor auto-loads `.agents/skills/`. |
| `.cursor/rules/noassume.mdc` | Always-on rule (`alwaysApply: true`) pointing at the skill. |
| `.noassume/config.yaml`, `.noassume/project.md` | Shared policy + project rules (if missing). |
| `.gitignore` | `.noassume/local/` entry added if absent. |

## Notes

- No global install: Cursor's user-level rules live in Settings, not the
  filesystem. To apply NoAssume everywhere, paste the contents of
  `agents/pointer.md` into Cursor Settings → Rules, adjusting the skill path
  to your global install.
- The `.mdc` rule is what makes NoAssume mandatory. Cursor would find the
  `.agents/skills/` entry on its own, but skill loading is discretionary —
  `alwaysApply` is not.
