# Security

## Reporting

Report vulnerabilities through GitHub's private vulnerability reporting on
this repository, or by opening a security advisory. Please don't file public
issues for exploitable problems.

## Scope notes

NoAssume is a set of instruction files and an installer — it runs inside your
agent's existing permissions. Two honest caveats:

- **Repository content becomes evidence.** The discovery phase reads project
  files, which means a repository containing hostile instructions could steer
  the agent. NoAssume raises the bar for silent decisions but cannot sandbox
  your agent — keep the agent's own permission model as the boundary.
- **The installer writes to your repo and instruction files.** Use
  `--dry-run` to preview every change. Managed content is confined to
  `noassume:begin/end` marker blocks and dedicated `noassume.*` files;
  uninstall removes exactly what it added.

NoAssume never transmits anything: state lives in `.noassume/`, fully local.
