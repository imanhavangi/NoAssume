# Configuration

All configuration lives in `.noassume/config.yaml`. The file is committed —
it is the team's contract for how hard NoAssume pushes back.

## Effective policy

```
profile (mode)  →  per-option clarify switches  →  behavior flags  →  task-risk escalation
```

- `mode` sets the baseline profile.
- Each `clarify.*` switch delegates one decision category to you (`false`) or
  keeps it gated (`true`).
- `behavior.*` toggles mechanics.
- Task risk can only raise strictness, never lower it below the risk floor.

## Modes

| Mode | Effect |
| --- | --- |
| `balanced` | Default. Blocks and materials must be resolved; defaultable categories follow config. |
| `strict` | Treats weak evidence as no evidence — conventions suggest, they do not prove. More categories become material. |
| `critical` | Near-zero assumptions. Anything the evidence does not prove gets asked, including most defaultable categories. Intended for production, security, data, and destructive work. |

## Task-risk escalation

Regardless of `mode`, certain work runs at a floor:

- `strict` floor — architecture changes, new services, public API changes,
  infrastructure and networking, dependency replacement, migrations.
- `critical` floor — authentication/authorization, secrets, destructive data
  operations, anything touching production, irreversible changes.

A user can always raise the level for a task ("run this one in critical").
Nothing lowers it below the floor. The floor is part of the protocol, not the
config: there is no switch that turns escalation off. The only ways past a
protected decision are the user's explicit instruction or an informed
override — never a configuration change.

## clarify switches

Set a category to `false` to delegate it permanently. `false` means "decide it
yourself and record the decision as DELEGATED, with `.noassume/config.yaml`
as the source" — it never means "don't record it", and it never means
"resolve it by inference". Evidence that suggests but does not prove is still
not authorization; the config switch is.

| Switch | Covers |
| --- | --- |
| `architecture` | component boundaries, service/module placement, patterns |
| `runtime` | language, version, framework, toolchain |
| `dependencies` | adding, replacing, or pinning libraries |
| `public_interfaces` | API contracts, CLI flags, exported signatures, events |
| `data_model` | schemas, types, serialization, ownership |
| `persistence` | databases, volumes, retention, migrations |
| `security` | auth, permissions, secrets, input trust boundaries |
| `networking` | ports, exposure, protocols, TLS, service discovery |
| `deployment` | environments, rollout, rollback, CI/CD changes |
| `testing` | whether/where to test, which framework, what coverage |
| `versions` | exact version pins when the repo doesn't pin them |
| `file_structure` | new files/directories layout beyond repo convention |
| `naming` | names not dictated by convention — usually safe to delegate |
| `logging` | log format, level policy, instrumentation detail |

## behavior flags

| Flag | Effect |
| --- | --- |
| `recommend_options` | Show a recommendation on questions. Off = neutral options. |
| `deep_repository_discovery` | Full discovery pass on first task. Off = quick scan only; expect more questions. |
| `monitor_implementation` | Keep the implementation guard active after READY. Off = gate-only mode; the audit still runs. |

The shipped defaults are opinionated — see `templates/config.yaml`. Teams tune
them per repository; that is the point of the file.
