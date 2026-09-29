# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Fixed
- Installer: dedicated files (rule files, skill stubs, vendored skill) are now
  ownership-checked via `<!-- noassume:managed-file -->` markers. A foreign
  file at a managed path is never overwritten or deleted — the installer
  reports a conflict and exits 1. Uninstall removes only NoAssume-owned
  files; foreign files are left untouched with a warning. Re-installing now
  prunes stale files left in the vendored skill by older versions.
- `clarify.*: false` now resolves decisions as DELEGATED (source:
  `config.yaml`) instead of the contradictory "INFERENCE/DELEGATED".
  Inference alone never closes a material ambiguity.
- Readiness gate criteria rewritten: zero blocking ambiguities, zero material
  ambiguities, zero material assumptions, zero unresolved conflicts, zero
  unresolved protected decisions, plus written plan and Definition of Done
  (replaces the ill-defined "unprotected-decision attempts").
- Removed `behavior.auto_escalate`. The task-risk floor is part of the
  protocol, not the config — there is no switch that turns escalation off.
- Task state lifecycle fully specified: live ledgers moved to
  `.noassume/local/current/`, discovery cache moved to
  `.noassume/local/repository.md` (persists across tasks), finished tasks
  archived under `local/history/<UTC timestamp>-<slug>/`. History is an audit
  trail, never a source of truth.
- GitHub Copilot adapter docs corrected: Copilot discovers skills natively
  from `.agents/skills/`; the instructions block remains the always-on gate.
- Kiro adapter docs now note that custom agents do not inherit workspace
  steering and need `"resources": ["file://.kiro/steering/**/*.md"]`.
- README: real Quick Start, Updating section, and an explicit
  instruction-layer (non-enforcement) limitation.
- `scripts/check_repo.py`: removed dead frontmatter check.

### Added
- Installer test suite (`scripts/test_install.py`), wired into CI.
- Minimal eval runner (`evals/runner/run.py`) with per-run transcripts,
  diffs, and metadata; results gitignored under `evals/results/`.

## [0.1.0] - 2026-09-29

Initial release.

- Canonical skill: invariant, eight-phase lifecycle, binary readiness gate,
  implementation guard, and audit (`skill/`).
- Persistent state layout under `.noassume/` with committed `config.yaml`
  and `project.md`, gitignored `local/` ledgers.
- Modes (`balanced` / `strict` / `critical`) with automatic task-risk
  escalation; delegation with a protected-decision list and informed
  overrides.
- Adapters for Codex, Claude Code, Cursor, GitHub Copilot, Gemini CLI, Kiro,
  Devin, and generic AGENTS.md agents (`agents/`).
- Cross-platform installer (`scripts/install.py` with `install.sh` /
  `install.ps1` wrappers): vendored skill, managed pointer blocks,
  idempotent, `--dry-run`, `--uninstall`, `--global`.
- Eval suite: 24 scenarios across six categories plus scoring rubric
  (`evals/`).
- Four worked examples (`examples/`).
