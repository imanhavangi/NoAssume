# Codex

## Install

```bash
./scripts/install.sh codex            # this repo
./scripts/install.sh codex --global   # every repo
```

## What gets installed

| Path | Purpose |
| --- | --- |
| `.agents/skills/noassume/` | Canonical skill (repo installs). Codex discovers it natively. |
| `AGENTS.md` | Managed `noassume` block added — always-on pointer. |
| `.noassume/config.yaml`, `.noassume/project.md` | Shared policy + project rules (if missing). |
| `.gitignore` | `.noassume/local/` entry added if absent. |

Global installs write the skill to `~/.agents/skills/noassume/` and the
pointer block into `~/.codex/AGENTS.md`.

## Notes

- Codex also reads `.codex/skills/` (legacy) — the installer uses the current
  `.agents/skills/` location.
- The `AGENTS.md` block is what makes NoAssume mandatory. Codex may discover
  the skill on its own, but discovery is discretionary; the block is not.
- Repo `AGENTS.md` files lower in the tree also work — the installer targets
  the repository root.
