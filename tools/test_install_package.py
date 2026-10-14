"""Tests for install_package.py. Run: python tools/test_install_package.py (or python3).

Uses temporary directories only; nothing is written inside the repository.
"""
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import install_package as ip  # noqa: E402

SKILLS = sorted(p.name for p in (ip.PACKAGE / ".agents/skills").iterdir() if p.is_dir())


class InstallerTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.t = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def run_ip(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            try:
                rc = ip.main([str(self.t)] + list(args))
            except SystemExit as exc:
                rc = exc.code
        return rc, out.getvalue() + err.getvalue()

    def put(self, rel, text):
        p = self.t / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(text.encode("utf-8"))

    def read(self, rel):
        return (self.t / rel).read_text(encoding="utf-8")

    def count(self):
        return sum(1 for p in self.t.rglob("*") if p.is_file())

    # ---- generic harness (behavior that must not regress) -------------------------

    def test_dry_run_changes_nothing_and_reports_conflict(self):
        self.put(".agents/rules/instructions.md", "legacy")
        before = self.count()
        rc, out = self.run_ip()
        self.assertEqual(self.count(), before)
        self.assertIn("CONFLICT  .agents/rules/instructions.md", out)
        self.assertEqual(rc, 1)

    def test_conflict_is_skipped_and_version_marker_withheld(self):
        self.put(".agents/rules/instructions.md", "legacy")
        self.run_ip("--apply")
        self.assertEqual(self.read(".agents/rules/instructions.md"), "legacy")
        self.assertFalse((self.t / ".agents/SDLC_VERSION").exists())

    def test_second_run_is_still_a_conflict_not_a_silent_update(self):
        self.put(".agents/rules/instructions.md", "legacy")
        self.run_ip("--apply")
        rc, out = self.run_ip("--apply")
        self.assertIn("CONFLICT  .agents/rules/instructions.md", out)
        self.assertIn("first install", out)
        self.assertEqual(self.read(".agents/rules/instructions.md"), "legacy")

    def test_force_replaces_with_backup_and_writes_marker(self):
        self.put(".agents/rules/instructions.md", "legacy")
        self.run_ip("--apply")
        rc, out = self.run_ip("--apply", "--force")
        self.assertEqual(rc, 0)
        self.assertEqual(self.read(".agents/rules/instructions.md.bak"), "legacy")
        self.assertTrue((self.t / ".agents/SDLC_VERSION").exists())

    def test_templates_and_project_file_are_never_overwritten(self):
        self.put(".github/pull_request_template.md", "custom")
        self.run_ip("--apply")
        self.put(".agents/rules/project.md", "mine\n")
        rc, out = self.run_ip("--apply")
        self.assertEqual(self.read(".github/pull_request_template.md"), "custom")
        self.assertEqual(self.read(".agents/rules/project.md"), "mine\n")

    def test_update_restores_tampered_package_owned_file(self):
        self.run_ip("--apply")
        self.put(".agents/guides/01-source-control-and-branching.md", "tampered")
        rc, out = self.run_ip("--apply")
        self.assertIn("UPDATE    .agents/guides/01-source-control-and-branching.md", out)

    def test_crlf_only_difference_is_not_a_change(self):
        self.run_ip("--apply")
        src = (ip.PACKAGE / "AGENTS.md").read_bytes()
        (self.t / "AGENTS.md").write_bytes(src.replace(b"\n", b"\r\n"))
        rc, out = self.run_ip("--apply")
        self.assertNotIn("AGENTS.md", out)

    def test_refuses_to_install_into_the_package(self):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err), self.assertRaises(SystemExit) as ctx:
            ip.main([str(ip.PACKAGE)])
        self.assertIn("Refusing", str(ctx.exception))

    def test_generic_harness_creates_no_claude_files(self):
        self.run_ip("--apply")
        self.assertFalse((self.t / "CLAUDE.md").exists())
        self.assertFalse((self.t / ".claude").exists())

    def test_unknown_harness_is_rejected(self):
        rc, out = self.run_ip("--harness", "vim")
        self.assertEqual(rc, 2)

    # ---- claude harness -------------------------------------------------------------

    def test_claude_dry_run_lists_claude_md_and_skills_but_changes_nothing(self):
        rc, out = self.run_ip("--harness", "claude")
        self.assertEqual(self.count(), 0)
        self.assertIn("NEW       CLAUDE.md", out)
        for name in SKILLS:
            self.assertIn(".claude/skills/%s/SKILL.md" % name, out)

    def test_claude_apply_creates_imports_and_identical_skill_copies(self):
        rc, out = self.run_ip("--apply", "--harness", "claude")
        self.assertEqual(rc, 0)
        text = self.read("CLAUDE.md")
        for line in ip.CLAUDE_IMPORTS:
            self.assertIn(line, text)
        self.assertNotIn(b"\r\n", (self.t / "CLAUDE.md").read_bytes())  # LF even on Windows
        for name in SKILLS:
            self.assertEqual(self.read(".claude/skills/%s/SKILL.md" % name),
                             self.read(".agents/skills/%s/SKILL.md" % name))
        self.assertTrue((self.t / "AGENTS.md").exists())  # generic layout stays

    def test_claude_import_targets_exist_after_install(self):
        self.run_ip("--apply", "--harness", "claude")
        for line in ip.CLAUDE_IMPORTS:
            self.assertTrue((self.t / line.lstrip("@")).is_file(), line)

    def test_existing_claude_md_is_not_modified_and_todo_is_printed(self):
        self.put("CLAUDE.md", "my own notes\n")
        rc, out = self.run_ip("--apply", "--harness", "claude")
        self.assertEqual(self.read("CLAUDE.md"), "my own notes\n")
        self.assertIn("TODO", out)
        for line in ip.CLAUDE_IMPORTS:
            self.assertIn("  " + line, out)
        self.assertEqual(rc, 0)

    def test_existing_claude_md_with_imports_needs_nothing(self):
        self.put("CLAUDE.md", "notes\n" + "\n".join(ip.CLAUDE_IMPORTS) + "\n")
        rc, out = self.run_ip("--apply", "--harness", "claude")
        self.assertNotIn("TODO", out)

    def test_claude_skill_copies_are_updated_on_later_runs(self):
        self.run_ip("--apply", "--harness", "claude")
        self.put(".claude/skills/%s/SKILL.md" % SKILLS[0], "tampered")
        rc, out = self.run_ip("--apply", "--harness", "claude")
        self.assertIn("UPDATE    .claude/skills/%s/SKILL.md" % SKILLS[0], out)
        self.assertEqual(self.read(".claude/skills/%s/SKILL.md" % SKILLS[0]),
                         self.read(".agents/skills/%s/SKILL.md" % SKILLS[0]))

    def test_claude_layer_can_be_added_after_a_generic_install(self):
        self.run_ip("--apply")
        rc, out = self.run_ip("--apply", "--harness", "claude")
        self.assertEqual(rc, 0)
        self.assertTrue((self.t / "CLAUDE.md").exists())
        self.assertTrue((self.t / ".claude/skills" / SKILLS[0] / "SKILL.md").exists())


if __name__ == "__main__":
    unittest.main(verbosity=1)
