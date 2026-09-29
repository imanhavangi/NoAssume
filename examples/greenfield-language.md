# "Build a CLI that compresses directories"

Greenfield. Empty repo — nothing to infer from. This is the worst case for a
guessing agent and the best case for clarification.

## Without NoAssume

The agent writes 200 lines of Python with `argparse` and `zipfile`, because
Python is its default. The user wanted a static binary for a fleet of minimal
containers. Everything gets rewritten.

## With NoAssume

> **[BLOCKING] Runtime**
> The repo is empty — nothing constrains the language, and this choice
> shapes everything downstream.
>
> A. Go — single static binary, easy to ship
> B. Rust — static binary, more build complexity
> C. Python — fast to write, needs an interpreter on target hosts
> D. Other
>
> **[BLOCKING] Archive format**
>
> A. `.tar.zst` — good ratio, needs `zstd` or a library
> B. `.tar.gz` — universal tooling
> C. `.zip` — Windows-friendly
>
> **[MATERIAL] Invocation shape**
>
> A. `tool <src> -o <out>` with flags — recommended
> B. Positional only: `tool <src> <out>`
> C. Config file driven
>
> **[MATERIAL] Failure behavior**
>
> A. Non-zero exit + stderr message — recommended for scripts
> B. Interactive prompts on error

User answers: A, A, B, A. Twenty minutes of wrong-Python work never happens.

The decision ledger records SPECIFIED/CLARIFIED rows for all four; the plan
and implementation follow them. Nothing was "smart" — it was asked.
