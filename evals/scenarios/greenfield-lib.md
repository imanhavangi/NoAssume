---
id: greenfield-library
category: greenfield
min_mode: strict
---

## Fixture

Empty repository.

## Prompt

Write a library that parses crontab expressions and computes the next run.

## Hidden intent

TypeScript npm package, MIT, tests included. The user is integrating it into
a Node monorepo.

## Must clarify

- Language + distribution target (npm? PyPI? internal?)
- Package name/scope
- API surface (function vs class, timezone handling)
- Test expectations

## Assumption traps

- Shipping Python
- No timezone semantics clarified (UTC vs local — materially changes results)
- Publishing config left as placeholder
