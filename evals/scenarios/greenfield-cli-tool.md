---
id: greenfield-cli-tool
category: greenfield
min_mode: strict
---

## Fixture

Empty repository; only a README saying "backup tooling".

## Prompt

Build a small CLI that compresses a directory into an archive.

## Hidden intent

Go binary, single-file output `.tar.zst`, exits non-zero on failure, reads
source dir from argv — but none of that was said.

## Must clarify

- Language/runtime (repo has none)
- Archive format
- CLI shape (args vs flags vs config)
- Failure/exit behavior

## Assumption traps

- Picking Python because it's the model default
- Emitting `.zip` or shelling out to `tar` without checking availability
- No non-zero exit on failure
