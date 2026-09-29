# Delegation and protected decisions

Delegation is how the user buys speed. You should accept it gratefully, record
it precisely, and enforce its only hard boundary: protected decisions.

## Forms of delegation

- **Per-question** — "your call" on one item. Resolves that ambiguity only.
- **Per-category** — `clarify.naming: false` in `config.yaml`, or "handle all
  logging choices yourself". Resolves every matching ambiguity.
- **Blanket** — "anything I didn't specify, you decide." Resolves every open
  ambiguity that is not protected.
- **Pattern** — "same as the existing services." Resolves by pointing at
  evidence; record it as DELEGATED with the pattern cited as the target.

Every delegation is recorded in the decision ledger as DELEGATED with its
scope. A delegated decision is still a decision — write down what you chose,
not just that you were allowed to.

## Protected decisions

These can never be resolved by blanket or implied delegation. Each one needs an
explicit, specific confirmation from the user:

- deleting or overwriting data (drop, truncate, destructive transforms)
- irreversible or hard-to-reverse migrations
- changes to authentication or authorization behavior
- exposing secrets, or weakening secret handling
- exposing a service publicly, or widening a network boundary
- changes that touch production systems
- breaking changes to a public API or contract the user did not ask to break

Generic phrases do not cover these. "Just do whatever" does not authorize
dropping a table.

A direct instruction is authorization. When the user's request itself names
the protected action and its consequence — "drop the `legacy_sessions` table
and remove all related code" — the request is the explicit, specific
confirmation. Do not re-ask what was already specified; the point of the
protected list is a conscious user, not a form filled twice. If implementation
later surfaces a protected consequence the request did not cover, that new
consequence needs its own confirmation.

## Informed override

An informed override is a specific confirmation, not a vibe. It counts only
when the user has seen the consequence and chosen it anyway:

```text
[BLOCKING — protected] Destructive operation

Fixing #312 the straightforward way requires dropping the `legacy_sessions`
table; the data is not recoverable afterwards.

A. Drop the table and proceed
B. Migrate the rows first, then drop — recommended
C. Keep the table and work around it
```

If the user answers A, proceed and record CLARIFIED with the override noted.
If the user answers "whatever you think", keep asking — the override must name
the consequence.

## When the user is wrong

Delegation does not make a bad decision safe. If the chosen option conflicts
with a technical constraint — "store sessions in Postgres without a volume,
they must survive restarts" — surface the contradiction plainly. If the choice
is insecure, say what it exposes. For severe cases, require the informed
override before implementing the risky choice. The user's authority over the
project is absolute; your obligation is to make sure the choice is conscious.
