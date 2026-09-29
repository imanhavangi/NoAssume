# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/).

## [Unreleased]

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
