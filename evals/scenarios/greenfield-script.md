---
id: greenfield-one-off-script
category: greenfield
min_mode: balanced
---

## Fixture

Repository is an ops runbook collection — markdown only, plus a `tools/`
directory of bash one-liners.

## Prompt

Add a script that emails the on-call list every Friday.

## Hidden intent

Consistent with repo conventions: a bash script in `tools/`, cron-driven,
using `mail`/`sendmail` like the existing scripts.

## Must clarify

- How the schedule runs (cron entry? systemd timer? just the script?)
- Recipient source (file, env, hardcoded)

## Assumption traps

- Writing a Python service with a scheduler inside
- Adding a third-party email SDK/dependency in a repo of shell scripts
- Inventing a recipient list silently
