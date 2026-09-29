#!/usr/bin/env python3
"""Repository consistency checks for NoAssume.

Catches the rot that accumulates in a docs-heavy repo: broken internal links,
references that don't exist, scenario files missing required fields, config
keys documented but not shipped, adapter rows without doc pages.

    python3 scripts/check_repo.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


# --- 1. SKILL.md sanity ---------------------------------------------------

skill = ROOT / "skill" / "SKILL.md"
if not skill.exists():
    err("skill/SKILL.md missing")
else:
    s = text(skill)
    if not s.startswith("---"):
        err("SKILL.md: missing YAML frontmatter")
    else:
        fm = s.split("---", 2)[1]
        for key in ("name:", "description:"):
            if key not in fm:
                err(f"SKILL.md frontmatter missing '{key}'")

# --- 2. Referenced files exist ---------------------------------------------

# Every `references/x.md` / `templates/x` path mentioned in skill + docs must exist.
for md in list((ROOT / "skill").rglob("*.md")) + list((ROOT / "docs").glob("*.md")) + \
          list((ROOT / "agents").glob("*.md")) + [ROOT / "README.md"]:
    if not md.exists():
        continue
    for m in re.finditer(r"`((?:references|templates)/[^`\s)]+)`", text(md)):
        target = md.parent / m.group(1)
        if not target.exists():
            # resolve relative to skill/ root for skill files
            alt = ROOT / "skill" / m.group(1)
            if not alt.exists():
                err(f"{md.relative_to(ROOT)}: references '{m.group(1)}' which does not exist")

# Internal markdown links: [text](relative/path)
for md in ROOT.rglob("*.md"):
    if ".git" in md.parts or ".noassume" in md.parts:
        continue
    for m in re.finditer(r"\]\(([^)\s]+)\)", text(md)):
        link = m.group(1)
        if link.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = (md.parent / link).resolve()
        if not target.exists():
            err(f"{md.relative_to(ROOT)}: broken link '{link}'")

# --- 3. Every references/ file is cited somewhere ---------------------------

cited = set()
for md in [skill, *ROOT.rglob("docs/*.md"), ROOT / "README.md"]:
    if md.exists():
        cited.update(re.findall(r"references/([a-z-]+\.md)", text(md)))
for f in sorted((ROOT / "skill" / "references").glob("*.md")):
    if f.name not in cited:
        err(f"skill/references/{f.name} is never referenced")

# --- 4. Eval scenarios -------------------------------------------------------

scenarios = sorted((ROOT / "evals" / "scenarios").glob("*.md"))
if len(scenarios) < 20:
    err(f"only {len(scenarios)} eval scenarios (expected >= 20)")

required_sections = ["## Prompt", "## Hidden intent", "## Must clarify",
                     "## Assumption traps"]
for f in scenarios:
    body = text(f)
    fm = body.split("---", 2)[1] if body.startswith("---") else ""
    for key in ("id:", "category:", "min_mode:"):
        if key not in fm:
            err(f"{f.name}: frontmatter missing '{key}'")
    for sec in required_sections:
        if sec not in body:
            err(f"{f.name}: missing section '{sec}'")
    if f"../" in fm and not (f.parent / fm).exists():
        pass

# --- 5. Config keys consistent across shipped files --------------------------

cfg = text(ROOT / "skill" / "templates" / "config.yaml")
keys = set(re.findall(r"^  (\w+):", cfg, re.M)) | {"mode"}
for doc in (ROOT / "skill" / "references" / "config.md",
            ROOT / "docs" / "configuration.md"):
    d = text(doc)
    for m in re.finditer(r"`(?:clarify\.|behavior\.)?(\w+)`", d):
        k = m.group(1)
        if k in {"balanced", "strict", "critical", "true", "false", "yaml",
                 "config", "noassume", "begin", "end"}:
            continue
        if k.startswith("yaml"):
            continue
        if (f"clarify.{k}" in d or f"behavior.{k}" in d) and k not in keys:
            err(f"{doc.name}: documents key '{k}' not in templates/config.yaml")

# --- 6. Adapter table ↔ docs ↔ matrix ---------------------------------------

install_py = text(ROOT / "scripts" / "install.py")
adapter_names = set(re.findall(r'^    "(\w+)": Adapter', install_py, re.M))
agent_docs = {p.stem for p in (ROOT / "agents").glob("*.md")
              if p.stem not in {"README", "pointer", "pointer-global"}}
doc_for = {"claude": "claude-code", "copilot": "github-copilot",
           "agentsmd": "agents-md"}
for name in adapter_names:
    doc = doc_for.get(name, name)
    if doc not in agent_docs:
        err(f"adapter '{name}' in install.py has no agents/{doc}.md")
matrix = text(ROOT / "agents" / "README.md")
for name in adapter_names:
    label = {"agentsmd": "AGENTS.md"}.get(name, name)
    if label.lower() not in matrix.lower():
        err(f"agents/README.md matrix missing adapter '{name}'")

# --- 7. Pointer files ---------------------------------------------------------

for p in ("agents/pointer.md", "agents/pointer-global.md"):
    t = text(ROOT / p)
    if "<!-- noassume:begin -->" not in t or "<!-- noassume:end -->" not in t:
        err(f"{p}: missing noassume markers")

# --- 8. Placeholder scan --------------------------------------------------------

BAD = re.compile(r"\b(TODO|FIXME|XXX|lorem ipsum|OWNER/REPO)\b")
skip = {".git", ".noassume"}
for f in ROOT.rglob("*"):
    if f.is_file() and f.suffix in {".md", ".py", ".sh", ".ps1", ".yml", ".yaml"} \
            and not skip & set(f.parts):
        if f.name == "check_repo.py":
            continue
        for ln in text(f).splitlines():
            # ignore mentions inside inline code spans (docs legitimately
            # discuss TODO/FIXME markers as repo signals)
            stripped = re.sub(r"`[^`]*`", "", ln)
            if BAD.search(stripped):
                err(f"{f.relative_to(ROOT)}: placeholder marker → {ln.strip()[:80]}")

# ------------------------------------------------------------------------------

if errors:
    print(f"check_repo: {len(errors)} problem(s)")
    for e in errors:
        print(f"  ✗ {e}")
    sys.exit(1)
print("check_repo: all checks passed")
