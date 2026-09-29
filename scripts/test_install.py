#!/usr/bin/env python3
"""Installer tests. Run: python3 scripts/test_install.py (stdlib only)."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_FILES = sorted(
    p.relative_to(ROOT / "skill")
    for p in (ROOT / "skill").rglob("*") if p.is_file()
)


def run_install(*args, home=None):
    env = dict(os.environ)
    if home is not None:
        env["HOME"] = str(home)
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "install.py"), *args],
        capture_output=True, text=True, env=env,
    )


class InstallerTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="noassume-test-")
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.repo = self.tmp / "repo"
        self.repo.mkdir()

    def install(self, *agents):
        return run_install(*agents, "--path", str(self.repo))

    # -- fresh install ---------------------------------------------------------

    def test_fresh_install_creates_everything(self):
        r = self.install("codex", "claude", "cursor")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((self.repo / ".agents/skills/noassume/SKILL.md").exists())
        for f in SKILL_FILES:
            self.assertTrue(
                (self.repo / ".agents/skills/noassume" / f).exists(), f
            )
        self.assertTrue((self.repo / ".noassume/config.yaml").exists())
        self.assertTrue((self.repo / ".noassume/project.md").exists())
        self.assertTrue((self.repo / ".noassume/local").is_dir())
        agents_md = (self.repo / "AGENTS.md").read_text()
        self.assertIn("noassume:begin", agents_md)
        self.assertIn("noassume:end", agents_md)
        claude_md = (self.repo / "CLAUDE.md").read_text()
        self.assertIn("noassume:begin", claude_md)
        stub = (self.repo / ".claude/skills/noassume/SKILL.md").read_text()
        self.assertIn("managed-file", stub)
        rule = (self.repo / ".cursor/rules/noassume.mdc").read_text()
        self.assertIn("alwaysApply: true", rule)
        stub = (self.repo / ".claude/skills/noassume/SKILL.md").read_text()
        self.assertIn("managed-file", stub)
        rule = (self.repo / ".cursor/rules/noassume.mdc").read_text()
        self.assertIn("alwaysApply: true", rule)
        self.assertTrue((self.repo / ".gitignore").exists())
        self.assertIn(".noassume/local/", (self.repo / ".gitignore").read_text())

    def test_second_install_is_idempotent(self):
        self.install("codex", "claude", "cursor")
        r = self.install("codex", "claude", "cursor")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("(create)", r.stdout)
        self.assertNotIn("(update)", r.stdout)

    # -- foreign files are never overwritten --------------------------------------

    def test_foreign_cursor_rule_conflicts(self):
        rule = self.repo / ".cursor/rules/noassume.mdc"
        rule.parent.mkdir(parents=True)
        rule.write_text("# my own rule, hands off\n")
        r = self.install("cursor")
        self.assertEqual(r.returncode, 1)
        self.assertIn("CONFLICT", r.stdout)
        self.assertIn("my own rule", rule.read_text())

    def test_foreign_kiro_rule_conflicts(self):
        rule = self.repo / ".kiro/steering/noassume.md"
        rule.parent.mkdir(parents=True)
        rule.write_text("mine\n")
        r = self.install("kiro")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(rule.read_text(), "mine\n")

    def test_foreign_claude_stub_conflicts(self):
        stub = self.repo / ".claude/skills/noassume/SKILL.md"
        stub.parent.mkdir(parents=True)
        stub.write_text("# my own skill\n")
        r = self.install("claude")
        self.assertEqual(r.returncode, 1)
        self.assertIn("my own skill", stub.read_text())

    def test_conflict_in_one_agent_does_not_block_others(self):
        (self.repo / ".cursor/rules").mkdir(parents=True)
        (self.repo / ".cursor/rules/noassume.mdc").write_text("mine\n")
        r = self.install("cursor", "codex")
        self.assertEqual(r.returncode, 1)
        self.assertIn("CONFLICT", r.stdout)
        self.assertIn("noassume:begin", (self.repo / "AGENTS.md").read_text())

    def test_existing_agents_md_is_appended_not_edited(self):
        (self.repo / "AGENTS.md").write_text("# My project\n\nCustom notes.\n")
        self.install("codex")
        text = (self.repo / "AGENTS.md").read_text()
        self.assertTrue(text.startswith("# My project"))
        self.assertIn("Custom notes.", text)
        self.assertIn("noassume:begin", text)

    def test_reinstall_updates_managed_rule_file(self):
        self.install("cursor")
        rule = self.repo / ".cursor/rules/noassume.mdc"
        rule.write_text(
            '---\ndescription: "NoAssume clarification guardrail"\n'
            "alwaysApply: true\n---\n\n<!-- noassume:begin -->\nstale\n"
            "<!-- noassume:end -->\n"
        )
        r = self.install("cursor")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("read and follow", rule.read_text())
        self.assertNotIn("stale", rule.read_text())

    def test_legacy_stub_without_marker_is_recognized(self):
        stub = self.repo / ".claude/skills/noassume/SKILL.md"
        stub.parent.mkdir(parents=True)
        stub.write_text(
            "---\nname: noassume\ndescription: old\n---\n\n"
            "Read and follow `.agents/skills/noassume/SKILL.md` — that file "
            "is the canonical protocol.\n"
        )
        r = self.install("claude")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Read and follow", stub.read_text())

    # -- uninstall -------------------------------------------------------------------

    def test_uninstall_removes_managed_and_keeps_user_content(self):
        (self.repo / "AGENTS.md").write_text("# My project\n\nCustom notes.\n")
        self.install("codex", "claude", "cursor")
        r = run_install(
            "codex", "claude", "cursor", "--uninstall", "--path", str(self.repo)
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(
            (self.repo / "AGENTS.md").read_text(), "# My project\n\nCustom notes.\n"
        )
        self.assertFalse((self.repo / ".cursor/rules/noassume.mdc").exists())
        self.assertFalse((self.repo / ".claude/skills/noassume").exists())
        self.assertFalse((self.repo / ".agents/skills/noassume").exists())
        self.assertTrue((self.repo / ".noassume/config.yaml").exists())

    def test_uninstall_leaves_foreign_rule_file(self):
        rule = self.repo / ".cursor/rules/noassume.mdc"
        rule.parent.mkdir(parents=True)
        rule.write_text("mine\n")
        self.install("cursor", "--uninstall")
        self.assertEqual(rule.read_text(), "mine\n")

    # -- global install -----------------------------------------------------------------

    def test_global_install_uses_fake_home(self):
        home = self.tmp / "home"
        home.mkdir()
        r = run_install("codex", "claude", "--global", home=home)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((home / ".agents/skills/noassume/SKILL.md").exists())
        self.assertIn(
            "noassume:begin", (home / ".codex/AGENTS.md").read_text()
        )
        stub = (home / ".claude/skills/noassume/SKILL.md").read_text()
        self.assertIn(str(home), stub)


if __name__ == "__main__":
    unittest.main()
