# FAQ

**Won't this flood me with questions?**

It asks every *material* ambiguity — and material has a definition (the
two-engineer test in `references/ambiguity.md`), not a vibe. Two things keep
the volume honest: discovery answers questions before they're asked, and
`config.yaml` lets you delegate whole categories permanently. If a question
couldn't change the implementation, it shouldn't have been asked — that's a
bug worth filing.

**Can't I just write a better prompt?**

You can, for decisions you already know you care about. NoAssume exists for
the ones you don't know to mention — the port you forgot compose would
publish, the library swap you didn't notice. It also makes the discipline
consistent across a team and across agents, which a prompt can't.

**Does it work with Spec Kit / BMAD / my existing workflow?**

Yes — it sits in front of them. Spec-driven tools answer "how do we structure
the work"; NoAssume answers "did anyone actually decide this." Install it
alongside and they don't conflict.

**What if I just want the agent to decide?**

Say so — per question, per category in `config.yaml`, or blanket ("decide
anything I didn't specify"). Delegation is recorded, so "what did the agent
choose" is always answerable. The only wall is the protected list:
destructive, auth, secrets, public-exposure, and production decisions need an
explicit, specific yes — never a shrug.

**Where does state live?**

`.noassume/` in the repo: `config.yaml` and `project.md` are committed;
`local/` is gitignored working memory. Nothing is sent anywhere — NoAssume
is files, not a service.

**Does it work in monorepos?**

Discovery runs from wherever the task points. `.noassume/` belongs at the
repo root; if subprojects need different policy, that's a known edge — file
an issue describing the layout.

**What languages does it ask questions in?**

Yours. The protocol matches the user's language in questions, plans, and
reports.

**The agent ignored the guardrail anyway.**

The pointer block is a strong instruction, not a sandbox — an agent can still
violate it, same as any rule file. If it happens with a specific agent, open
an issue with the model and the transcript; per-agent quirks belong in the
adapter docs.
