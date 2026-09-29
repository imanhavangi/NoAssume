#!/usr/bin/env python3
"""NoAssume installer.

Vendors the canonical skill into a repository and writes a thin always-on
pointer into the mechanism each agent already reads. Idempotent, additive,
and conservative: it never overwrites user files — managed content lives
inside `<!-- noassume:begin/end -->` markers or in dedicated files.

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


def write_file(path: Path, content: str, rep: Reporter, kind: str) -> None:
    if path.exists() and path.read_text() == content:
        rep.record(kind, path, "unchanged")
        return
    rep.record(kind, path, "update" if path.exists() else "create")
    if rep.dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


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
    write_file(path, upsert_block(existing, block), rep, "pointer block")


def copy_skill(dest: Path, rep: Reporter) -> None:
    src_files = sorted(p for p in SKILL_SRC.rglob("*") if p.is_file())
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
    rep.record(
        "vendor skill",
        dest,
        "unchanged" if changed == 0 else f"{changed} file(s)",
    )


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
    write_file(gi, content, rep, "gitignore")


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
    rep.record("init state", local, "create" if not local.exists() else "unchanged")
    if not rep.dry_run:
        local.mkdir(parents=True, exist_ok=True)


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

    if not args.uninstall:
        copy_skill(skill_dest, rep)
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
                    if path.exists():
                        rep.record("remove file", path, "delete")
                        if not rep.dry_run:
                            path.unlink()
                    else:
                        rep.record("remove file", path, "absent")
                else:
                    write_file(path, act.frontmatter + pointer, rep, "rule file")
            elif isinstance(act, Stub):
                if args.uninstall:
                    if path.exists():
                        rep.record("remove file", path, "delete")
                        if not rep.dry_run:
                            path.unlink()
                    else:
                        rep.record("remove file", path, "absent")
                else:
                    # project stubs must stay relocatable → repo-relative path;
                    # global stubs need the absolute install location
                    rendered = str(skill_dest / "SKILL.md") if args.global_ \
                        else str(PROJECT_SKILL_REL / "SKILL.md")
                    write_file(path, STUB_TEMPLATE.format(
                        skill_path=rendered), rep, "skill stub")

    if args.uninstall:
        if skill_dest.exists():
            rep.record("remove skill", skill_dest, "delete")
            if not rep.dry_run:
                shutil.rmtree(skill_dest)
                # prune empty parents we created (.agents/skills, .agents)
                for parent in (skill_dest.parent, skill_dest.parent.parent):
                    try:
                        parent.rmdir()  # only removes if empty
                    except OSError:
                        break
        if not args.global_:
            ensure_gitignore(base, rep, uninstall=True)
        print(rep.summary())
        print("noassume: kept .noassume/ project data (config.yaml, project.md,"
              " local history) — delete it manually if unwanted.")
        return 0

    print(rep.summary())
    return 0


if __name__ == "__main__":
    sys.exit(main())
