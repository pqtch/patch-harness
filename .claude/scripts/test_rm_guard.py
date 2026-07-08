import unittest
from pathlib import Path

import rm_guard as rg


class RmGuardTests(unittest.TestCase):
    def setUp(self):
        self.root = rg.WORKSPACE_ROOT

    def test_allows_rm_inside_workspace(self):
        decision, _ = rg.evaluate("rm projects/foo/scratch.txt", self.root)
        self.assertEqual(decision, "allow")

    def test_denies_rm_under_dot_claude(self):
        decision, reason = rg.evaluate("rm .claude/rules/security.md", self.root)
        self.assertEqual(decision, "deny")
        self.assertIn(".claude", reason)

    def test_denies_rm_memory_md(self):
        decision, _ = rg.evaluate("rm memories/shared/MEMORY.md", self.root)
        self.assertEqual(decision, "deny")

    def test_denies_rmdir_dot_claude_subdir(self):
        decision, _ = rg.evaluate("rmdir .claude/scripts", self.root)
        self.assertEqual(decision, "deny")

    def test_denies_system_path_via_dotdot(self):
        decision, _ = rg.evaluate("rm ../../../../etc/passwd", self.root)
        self.assertEqual(decision, "deny")

    def test_denies_absolute_system_path(self):
        decision, _ = rg.evaluate("rm /etc/passwd", self.root)
        self.assertEqual(decision, "deny")

    def test_asks_on_non_system_path_outside_workspace(self):
        decision, _ = rg.evaluate("rm /tmp/scratch.txt", self.root)
        self.assertEqual(decision, "ask")

    def test_allows_dev_null_redirect(self):
        # regression: >/dev/null must never prompt — ask-fatigue kills the guard
        decision, _ = rg.evaluate("grep foo bar 2>/dev/null", self.root)
        self.assertEqual(decision, "allow")
        decision2, _ = rg.evaluate("some_cmd > /dev/null", self.root)
        self.assertEqual(decision2, "allow")

    def test_denies_redirect_truncation_of_memory_md(self):
        decision, _ = rg.evaluate("echo x > memories/shared/MEMORY.md", self.root)
        self.assertEqual(decision, "deny")

    def test_allows_redirect_inside_project(self):
        decision, _ = rg.evaluate("echo x > projects/foo/notes.md", self.root)
        self.assertEqual(decision, "allow")

    def test_denies_mv_overwriting_dot_claude_file(self):
        decision, _ = rg.evaluate(
            "mv projects/foo/rules.md .claude/rules/conventions.md", self.root
        )
        self.assertEqual(decision, "deny")

    def test_allows_mv_within_workspace(self):
        decision, _ = rg.evaluate("mv projects/foo/a.md projects/foo/b.md", self.root)
        self.assertEqual(decision, "allow")

    def test_ignores_non_destructive_commands(self):
        decision, _ = rg.evaluate("ls .claude/rules", self.root)
        self.assertEqual(decision, "allow")

    def test_chained_command_with_destructive_segment_denied(self):
        decision, _ = rg.evaluate(
            "cd projects && rm ../.claude/settings.json", self.root
        )
        self.assertEqual(decision, "deny")

    def test_unparseable_command_asks(self):
        decision, _ = rg.evaluate("rm 'unterminated", self.root)
        self.assertEqual(decision, "ask")


class EmitProtocolTests(unittest.TestCase):
    """The hook is only real if it speaks the CC protocol: deny -> stderr + exit 2;
    allow/ask -> hookSpecificOutput.permissionDecision JSON + exit 0."""

    def _run_main(self, payload):
        import io
        import sys

        old = sys.stdin, sys.stdout, sys.stderr
        sys.stdin = io.StringIO(payload)
        sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
        try:
            rc = rg.main()
            return rc, sys.stdout.getvalue(), sys.stderr.getvalue()
        finally:
            sys.stdin, sys.stdout, sys.stderr = old

    def test_allow_emits_permission_decision_json_exit_0(self):
        import json

        rc, out, _ = self._run_main('{"tool_input": {"command": "ls"}}')
        self.assertEqual(rc, 0)
        hso = json.loads(out)["hookSpecificOutput"]
        self.assertEqual(hso["hookEventName"], "PreToolUse")
        self.assertEqual(hso["permissionDecision"], "allow")

    def test_deny_exits_2_with_stderr_reason(self):
        rc, out, err = self._run_main(
            '{"tool_input": {"command": "rm .claude/settings.json"}}'
        )
        self.assertEqual(rc, 2)
        self.assertIn("BLOCKED", err)
        self.assertEqual(out, "")

    def test_ask_emits_permission_decision_json_exit_0(self):
        import json

        rc, out, _ = self._run_main('{"tool_input": {"command": "rm /tmp/x"}}')
        self.assertEqual(rc, 0)
        hso = json.loads(out)["hookSpecificOutput"]
        self.assertEqual(hso["permissionDecision"], "ask")


if __name__ == "__main__":
    unittest.main()
