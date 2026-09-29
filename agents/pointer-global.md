<!-- noassume:begin -->
## NoAssume

This machine uses NoAssume. Before creating, modifying, or deleting code,
configuration, or infrastructure, read and follow `SKILL.md` in the installed
NoAssume skill directory (`NOASSUME_SKILL_PATH`).

Core rule: never make a material implementation decision on an assumption.
If a decision is not specified by the user, proven by repository evidence, or
explicitly delegated, ask first. Maintain state in `.noassume/` inside the
project; keep `.noassume/local/` out of git.
<!-- noassume:end -->
