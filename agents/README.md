# Agent integrations

NoAssume has one canonical implementation — `skill/` — and a thin always-on
adapter per agent. Adapters never contain protocol logic; they only make sure
the agent loads the canonical skill before implementing.

## How it works

`scripts/install.sh` does two things:

1. Vendors the canonical skill into the target repository at
   `.agents/skills/noassume/` (a location Codex and Cursor discover natively)
   and initializes `.noassume/` (config + project rules).
2. Writes a small always-on pointer — the text in `pointer.md` — into the
   mechanism each agent already reads every session, so the skill is
   mandatory rather than discoverable.

## Support matrix

| Agent | Always-on mechanism | Skill location | Global install |
| --- | --- | --- | --- |
| Codex | managed block in `AGENTS.md` | `.agents/skills/noassume/` (native) | `~/.codex/AGENTS.md` + `~/.agents/skills/` |
| Claude Code | managed block in `CLAUDE.md` + `.claude/skills/noassume/` stub | `.agents/skills/noassume/` | `~/.claude/CLAUDE.md` |
| Cursor | `.cursor/rules/noassume.mdc` (`alwaysApply`) | `.agents/skills/noassume/` (native) | not file-based — see `cursor.md` |
| GitHub Copilot | managed block in `.github/copilot-instructions.md` | `.agents/skills/noassume/` | `~/.copilot/copilot-instructions.md` (CLI) |
| Gemini CLI | managed block in `GEMINI.md` | `.agents/skills/noassume/` | `~/.gemini/GEMINI.md` |
| Kiro | `.kiro/steering/noassume.md` (`inclusion: always`) | `.agents/skills/noassume/` | `~/.kiro/steering/` |
| Devin | `.devin/rules/noassume.md` (`trigger: always_on`) | `.agents/skills/noassume/` | `~/.devin/rules/` |
| Any AGENTS.md agent | managed block in `AGENTS.md` | `.agents/skills/noassume/` | tool-dependent |

Per-agent notes live next to this file. If your agent reads `AGENTS.md`,
`CLAUDE.md`, or `GEMINI.md` and can follow a file reference, the `agentsmd`
adapter covers it.

## Adding an adapter

See `CONTRIBUTING.md`. An adapter is: one row in the installer's agent table,
a doc page here, and honest notes on what the agent cannot guarantee.
