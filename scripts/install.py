#!/usr/bin/env python3
"""NoAssume installer.

Vendors the canonical skill into a repository and writes a thin always-on
pointer into the mechanism each agent already reads. Idempotent, additive,
and conservative: shared files are only touched inside
`<!-- noassume:begin/end -->` markers, and dedicated files (rule files,
skill stubs, the vendored skill) are only created, updated, or removed when
NoAssume wrote them. A foreign file at a managed path is never overwritten
or deleted — the installer reports a conflict and leaves it untouched.

Usage:
    install.py AGENT [AGENT ...] [--path DIR] [--global] [--uninstall]
               [--dry-run]

Agents: codex claude cursor copilot gemini kiro devin agentsmd all
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_SRC = REPO_ROOT / "skill"
POINTER_SRC = REPO_ROOT / "agents" / "pointer.md"
POINTER_GLOBAL_SRC = REPO_ROOT / "agents" / "pointer-global.md"

BEGIN = "<!-- noassume:begin -->"
END = "<!-- noassume:end -->"
MANAGED_FILE = "<!-- noassume:managed-file -->"
LEGACY_STUB_SNIPPET = "that file is the canonical protocol"
GITIGNORE_STANZA = "# NoAssume local state\n.noassume/local/\n"

SKILL_DIR_NAME = "noassume"
PROJECT_SKILL_REL = Path(".agents/skills") / SKILL_DIR_NAME
GLOBAL_SKILL_DIR = Path.home() / ".agents" / "skills" / SKILL_DIR_NAME
GLOBAL_SKILL_PLACEHOLDER = "NOASSUME_SKILL_PATH"

CURSOR_FRONTMATTER = (
    "---\n"
    'description: "NoAssume clarification guardrail"\n'
    "alwaysApply: true\n"
    "---\n\n"
)
KIRO_FRONTMATTER = "---\ninclusion: always\n---\n\n"
DEVIN_FRONTMATTER = (
    "---\n"
    'description: "NoAssume clarification guardrail"\n'
    "trigger: always_on\n"
    "---\n\n"
)

STUB_TEMPLATE = """---
name: noassume
description: NoAssume clarification guardrail. Resolves material ambiguity with the user before implementing; blocks silent assumptions.
---

<!-- noassume:managed-file -->
Read and follow `{skill_path}` — that file is the canonical protocol.
"""


@dataclass(frozen=True)
class Block:
    """Managed marker block inside an existing-or-new markdown file."""
    relpath: str


@dataclass(frozen=True)
class RuleFile:
    """Dedicated always-on file owned entirely by NoAssume."""
    relpath: str
    frontmatter: str


@dataclass(frozen=True)
class Stub:
    """Skill stub that points the agent's native skill loader at the canonical file."""
    relpath: str


@dataclass(frozen=True)
class Adapter:
    project: tuple
    global_: tuple | None  # None = global install unsupported


ADAPTERS: dict[str, Adapter] = {
    "codex": Adapter(
        project=(Block("AGENTS.md"),),
        global_=(Block("~/.codex/AGENTS.md"),),
    ),
    "claude": Adapter(
        project=(
            Block("CLAUDE.md"),
            Stub(".claude/skills/noassume/SKILL.md"),
        ),
        global_=(
            Block("~/.claude/CLAUDE.md"),
            Stub("~/.claude/skills/noassume/SKILL.md"),
        ),
    ),
    "cursor": Adapter(
        project=(RuleFile(".cursor/rules/noassume.mdc", CURSOR_FRONTMATTER),),
        global_=None,
    ),
    "copilot": Adapter(
        project=(Block(".github/copilot-instructions.md"),),
        global_=(Block("~/.copilot/copilot-instructions.md"),),
    ),
    "gemini": Adapter(
        project=(Block("GEMINI.md"),),
        global_=(Block("~/.gemini/GEMINI.md"),),
    ),
    "kiro": Adapter(
        project=(RuleFile(".kiro/steering/noassume.md", KIRO_FRONTMATTER),),
        global_=(RuleFile("~/.kiro/steering/noassume.md", KIRO_FRONTMATTER),),
    ),
    "devin": Adapter(
        project=(RuleFile(".devin/rules/noassume.md", DEVIN_FRONTMATTER),),
        global_=(RuleFile("~/.devin/rules/noassume.md", DEVIN_FRONTMATTER),),
    ),
    "agentsmd": Adapter(
        project=(Block("AGENTS.md"),),
        global_=None,
    ),
}

BLOCK_RE = re.compile(
    r"[^\S\n]*" + re.escape(BEGIN) + r".*?" + re.escape(END) + r"[^\S\n]*\n?",
    re.S,
)


class Reporter:
    def __init__(self, dry_run: bool):
        self.dry_run = dry_run
        self.rows: list[tuple[str, str, str]] = []

    def record(self, action: str, path: Path, status: str) -> None:
        self.rows.append((action, str(path), status))

    def summary(self) -> str:
        if not self.rows:
            return "nothing to do"
        width = max(len(a) for a, _, _ in self.rows)
        lines = [f"  {a:<{width}}  {p}  ({s})" for a, p, s in self.rows]
        header = "planned changes:" if self.dry_run else "applied changes:"
        return header + "\n" + "\n".join(lines)


def load_pointer(global_: bool, skill_dir: Path) -> str:
    if global_:
        text = POINTER_GLOBAL_SRC.read_text()
        return text.replace(GLOBAL_SKILL_PLACEHOLDER, str(skill_dir))
    return POINTER_SRC.read_text()


def upsert_block(existing: str, block: str) -> str:
    if BEGIN in existing and END in existing:
        return BLOCK_RE.sub(block, existing, count=1)
    if existing and not existing.endswith("\n"):
        existing += "\n"
    sep = "\n" if existing.strip() else ""
    return existing + sep + block


def remove_block(existing: str) -> str | None:
    """Return new text, or None to delete the file entirely."""
    if BEGIN not in existing:
        return existing
    out = BLOCK_RE.sub("", existing)
    out = re.sub(r"\n{3,}", "\n\n", out).strip()
    return (out + "\n") if out else None


def is_managed(content: str) -> bool:
    """True when NoAssume wrote (or previously wrote) this dedicated file."""
    return (BEGIN in content or MANAGED_FILE in content
            or "name: noassume" in content
            or LEGACY_STUB_SNIPPET in content)


def write_managed_file(path: Path, content: str, rep: Reporter,
                       kind: str) -> bool:
    """Create or update a NoAssume-owned file. Never touches foreign files.

    Returns False when the path holds a file NoAssume did not write.
    """
    if path.exists():
        current = path.read_text()
        if current == content:
            rep.record(kind, path, "unchanged")
            return True
        if not is_managed(current):
            rep.record(kind, path, "CONFLICT — not managed by NoAssume")
            print(
                f"noassume: refusing to overwrite {path}: it exists and was "
                f"not written by NoAssume. Merge or move it manually, then "
                f"re-run the installer.",
                file=sys.stderr,
            )
            return False
        rep.record(kind, path, "update")
    else:
        rep.record(kind, path, "create")
    if rep.dry_run:
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return True


def remove_managed_file(path: Path, rep: Reporter, kind: str) -> bool:
    """Delete a dedicated file only when NoAssume owns it."""
    if not path.exists():
        rep.record("remove file", path, "absent")
        return True
    if not is_managed(path.read_text()):
        rep.record("remove file", path, "kept — not managed by NoAssume")
        print(
            f"noassume: leaving {path} untouched: it was not written by "
            f"NoAssume. Delete it manually if unwanted.",
            file=sys.stderr,
        )
        return True
    rep.record("remove file", path, "delete")
    if not rep.dry_run:
        path.unlink()
    return True


def prune_empty_dirs(path: Path, stop: Path) -> None:
    d = path.parent
    while d != stop and d != d.parent:
        try:
            d.rmdir()  # only succeeds when empty
        except OSError:
            break
        d = d.parent


def apply_block(path: Path, block: str, rep: Reporter, uninstall: bool) -> None:
    existing = path.read_text() if path.exists() else ""
    if uninstall:
        new = remove_block(existing)
        if new is None:
            rep.record("remove file", path, "empty after unblocking")
            if not rep.dry_run:
                path.unlink()
        elif new != existing:
            rep.record("remove block", path, "update")
            if not rep.dry_run:
                path.write_text(new)
        else:
            rep.record("remove block", path, "no block found")
        return
    updated = upsert_block(existing, block)
    if updated == existing:
        rep.record("pointer block", path, "unchanged")
        return
    rep.record("pointer block", path, "update" if existing else "create")
    if not rep.dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(updated)


def copy_skill(dest: Path, rep: Reporter) -> bool:
    src_files = sorted(p for p in SKILL_SRC.rglob("*") if p.is_file())
    rels = {p.relative_to(SKILL_SRC) for p in src_files}
    marker = dest / "SKILL.md"
    if dest.exists() and any(dest.iterdir()):
        if not marker.exists():
            rep.record("vendor skill", dest,
                       "CONFLICT — directory not managed by NoAssume")
            print(
                f"noassume: refusing to vendor the skill into {dest}: the "
                f"directory exists and has no NoAssume SKILL.md. Inspect it "
                f"and resolve the conflict manually.",
                file=sys.stderr,
            )
            return False
        if not is_managed(marker.read_text()):
            rep.record("vendor skill", dest,
                       "CONFLICT — SKILL.md not managed by NoAssume")
            print(
                f"noassume: refusing to update {dest}: its SKILL.md was not "
                f"written by NoAssume. If it is a stale copy from an older "
                f"NoAssume, delete it and re-run.",
                file=sys.stderr,
            )
            return False
    changed = 0
    for src in src_files:
        rel = src.relative_to(SKILL_SRC)
        dst = dest / rel
        if dst.exists() and dst.read_bytes() == src.read_bytes():
            continue
        changed += 1
        if not rep.dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    removed = 0
    if not rep.dry_run and dest.exists():
        for dst in sorted(dest.rglob("*"), key=lambda p: len(p.parts),
                          reverse=True):
            if dst.is_file() and dst.relative_to(dest) not in rels:
                dst.unlink()
                removed += 1
                changed += 1
        for d in sorted((p for p in dest.rglob("*") if p.is_dir()),
                        key=lambda p: len(p.parts), reverse=True):
            try:
                d.rmdir()  # only succeeds when empty
            except OSError:
                pass
    rep.record(
        "vendor skill",
        dest,
        "unchanged" if changed == 0 else f"{changed} file(s)",
    )
    return True


def ensure_gitignore(repo: Path, rep: Reporter, uninstall: bool) -> None:
    gi = repo / ".gitignore"
    existing = gi.read_text() if gi.exists() else ""
    if uninstall:
        if GITIGNORE_STANZA in existing:
            new = existing.replace(GITIGNORE_STANZA, "")
            rep.record("gitignore", gi, "remove stanza")
            if not rep.dry_run:
                if new.strip():
                    gi.write_text(new)
                else:
                    gi.unlink()
        else:
            rep.record("gitignore", gi, "no stanza found")
        return
    if ".noassume/local/" in existing:
        rep.record("gitignore", gi, "unchanged")
        return
    content = existing
    if content and not content.endswith("\n"):
        content += "\n"
    content += ("\n" if content.strip() else "") + GITIGNORE_STANZA
    rep.record("gitignore", gi, "update" if existing else "create")
    if not rep.dry_run:
        gi.write_text(content)


def init_state(repo: Path, rep: Reporter) -> None:
    for name in ("config.yaml", "project.md"):
        src = SKILL_SRC / "templates" / name
        dst = repo / ".noassume" / name
        if dst.exists():
            rep.record("init state", dst, "exists — kept")
            continue
        rep.record("init state", dst, "create")
        if not rep.dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    local = repo / ".noassume" / "local"
    for d in (local, local / "current", local / "history"):
        rep.record("init state", d, "create" if not d.exists() else "unchanged")
        if not rep.dry_run:
            d.mkdir(parents=True, exist_ok=True)


def resolve(relpath: str, base: Path) -> Path:
    p = Path(relpath).expanduser()
    return p if p.is_absolute() else base / p


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="install.py",
        description="Install NoAssume into a repository (or globally).",
    )
    ap.add_argument("agents", nargs="+", choices=[*ADAPTERS, "all"])
    ap.add_argument("--path", default=".", help="target repository (default: cwd)")
    ap.add_argument("--global", dest="global_", action="store_true",
                    help="install for every project instead of one repo")
    ap.add_argument("--uninstall", action="store_true",
                    help="remove NoAssume pointers and the vendored skill; "
                         "keeps .noassume/ project data")
    ap.add_argument("--dry-run", action="store_true",
                    help="print planned changes without writing")
    args = ap.parse_args()

    names = sorted(ADAPTERS) if "all" in args.agents else args.agents
    rep = Reporter(args.dry_run)
    base = Path(args.path).expanduser().resolve()
    if not args.global_ and not base.is_dir():
        ap.error(f"target is not a directory: {base}")

    skill_dest = GLOBAL_SKILL_DIR if args.global_ else base / PROJECT_SKILL_REL
    pointer = load_pointer(args.global_, skill_dest)
    conflicts = 0

    if not args.uninstall:
        if not copy_skill(skill_dest, rep):
            conflicts += 1
        if not args.global_:
            init_state(base, rep)
            ensure_gitignore(base, rep, uninstall=False)

    for name in names:
        actions = ADAPTERS[name].global_ if args.global_ else ADAPTERS[name].project
        if actions is None:
            print(f"noassume: {name}: no file-based global install — "
                  f"see agents/{name.replace('agentsmd','agents-md')}.md",
                  file=sys.stderr)
            continue
        for act in actions:
            path = resolve(act.relpath, base)
            if isinstance(act, Block):
                apply_block(path, pointer, rep, args.uninstall)
            elif isinstance(act, RuleFile):
                if args.uninstall:
                    remove_managed_file(path, rep, "rule file")
                else:
                    if not write_managed_file(path, act.frontmatter + pointer,
                                              rep, "rule file"):
                        conflicts += 1
            elif isinstance(act, Stub):
                if args.uninstall:
                    remove_managed_file(path, rep, "skill stub")
                    prune_empty_dirs(path, base)
                else:
                    # project stubs must stay relocatable → repo-relative path;
                    # global stubs need the absolute install location
                    rendered = str(skill_dest / "SKILL.md") if args.global_ \
                        else str(PROJECT_SKILL_REL / "SKILL.md")
                    if not write_managed_file(path, STUB_TEMPLATE.format(
                            skill_path=rendered), rep, "skill stub"):
                        conflicts += 1

    if args.uninstall:
        marker = skill_dest / "SKILL.md"
        if skill_dest.exists():
            if marker.exists() and is_managed(marker.read_text()):
                rep.record("remove skill", skill_dest, "delete")
                if not rep.dry_run:
                    shutil.rmtree(skill_dest)
                    # prune empty parents we created (.agents/skills, .agents)
                    for parent in (skill_dest.parent, skill_dest.parent.parent):
                        try:
                            parent.rmdir()  # only removes if empty
                        except OSError:
                            break
            else:
                rep.record("remove skill", skill_dest,
                           "kept — not managed by NoAssume")
                print(
                    f"noassume: leaving {skill_dest} untouched: its SKILL.md "
                    f"was not written by NoAssume. Inspect and delete "
                    f"manually if unwanted.",
                    file=sys.stderr,
                )
        if not args.global_:
            ensure_gitignore(base, rep, uninstall=True)
        print(rep.summary())
        print("noassume: kept .noassume/ project data (config.yaml, project.md,"
              " local history) — delete it manually if unwanted.")
        return 0

    print(rep.summary())
    return 1 if conflicts else 0


if __name__ == "__main__":
    sys.exit(main())
