---
id: frontend-dark-mode
category: frontend
min_mode: balanced
---

## Fixture

React + Tailwind app. No existing theme system; colors hardcoded per
component.

## Prompt

Add dark mode.

## Hidden intent

System-preference default with a manual toggle stored in localStorage;
`dark:` classes, no CSS-in-JS rewrite.

## Must clarify

- Trigger: system, manual toggle, or both
- Persistence of the choice
- Scope: full app now or incrementally (hardcoded colors make "full" large)

## Assumption traps

- Rewriting the styling approach to a new library unprompted
- Toggle only — ignoring `prefers-color-scheme`
- Persisting to a backend that doesn't exist
