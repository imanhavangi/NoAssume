# Assumption log

Every INFERENCE and ASSUMPTION made during the task, including ones later
resolved. This file exists so "what did the agent quietly decide?" is always
answerable. At READY, no open ASSUMPTION may be material.

## Format

```markdown
### ASMP-NNN — <short name>
- Kind: inference | assumption
- Status: open | resolved → DEC-NNN
- Claim: <what was taken as true>
- Evidence: <supporting evidence, or "none">
- Risk if wrong: <what breaks>
```

## Entries
