# Configuration

Everything lives in `.noassume/config.yaml`, created by the installer and
committed with your repo — the policy is shared by everyone who works on the
project. The shipped file is fully commented; this page is the short tour.

## Modes

```yaml
mode: balanced   # balanced | strict | critical
```

- **balanced** — ask what evidence can't resolve; let defaults cover the rest.
- **strict** — weak evidence stops counting as evidence; conventions suggest
  but don't decide.
- **critical** — near-zero assumptions, for work where guessing is expensive.

You can also change mode per task in conversation ("run this in strict").
Task risk escalates automatically — auth, production, destructive, and
infrastructure work run at higher floors regardless of the configured mode.
That floor is built into the protocol and has no configuration switch.

## Delegating categories

Each `clarify.*` key is a decision category. `true` means "ask when evidence
is silent"; `false` means "decide it yourself and record the choice as a
DELEGATED decision with `config.yaml` as the source":

```yaml
clarify:
  dependencies: true     # keep asking before adding libraries
  naming: false          # stop asking about names
```

Fourteen categories ship — the template comments say what each covers. The
defaults are opinionated; tuning them per project is the intended workflow.

## Behavior flags

```yaml
behavior:
  recommend_options: true            # show a recommendation on questions
  deep_repository_discovery: true    # deep scan on first task, verify after
  monitor_implementation: true       # keep guarding after the gate opens
```

`monitor_implementation: false` gives you gate-only mode: clarification and
the gate still run, the mid-flight guard stands down, and only the final
audit remains.

## Permanent rules

`config.yaml` is policy; `.noassume/project.md` is law — permanent rules the
agent must treat as top-tier evidence. When a clarification produces a rule
that should always hold ("databases never publish host ports"), ask the agent
to promote it, or write it yourself:

```markdown
## Networking
- Databases never publish host ports.
```

Rules in `project.md` outrank repository conventions and apply to every task.

## Local state

`.noassume/local/` — ledgers, plans, history — is gitignored. It's the
agent's working memory, not team documentation.
