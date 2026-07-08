import shutil
import tempfile
import unittest
from datetime import date
from pathlib import Path

import health_check as hc


class HealthCheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.orig_root = hc.ROOT
        hc.ROOT = self.tmp

    def tearDown(self):
        hc.ROOT = self.orig_root
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_find_paths_in_ignores_placeholders(self):
        text = "See `projects/foo/CONTEXT.md` and `<placeholder>` and `http://x`."
        found = hc.find_paths_in(text)
        self.assertIn("projects/foo/CONTEXT.md", found)
        self.assertEqual(len(found), 1)

    def test_check_referenced_paths_missing(self):
        (self.tmp / "CLAUDE.md").write_text("See `projects/ghost/CONTEXT.md`.")
        results = hc.check_referenced_paths()
        self.assertTrue(any(m == "✗" for m, _ in results))

    def test_check_referenced_paths_ok(self):
        (self.tmp / "projects").mkdir()
        (self.tmp / "CLAUDE.md").write_text("See `projects/`.")
        results = hc.check_referenced_paths()
        self.assertTrue(all(m == "✓" for m, _ in results))

    def test_check_referenced_paths_missing_file_in_existing_dir(self):
        # regression: a missing FILE must fail even when its parent dir exists
        (self.tmp / "projects").mkdir()
        (self.tmp / "CLAUDE.md").write_text("See `projects/ghost.md`.")
        results = hc.check_referenced_paths()
        self.assertTrue(any(m == "✗" for m, _ in results))

    def test_check_memory_index_missing_file(self):
        (self.tmp / "memories" / "shared").mkdir(parents=True)
        (self.tmp / "memories" / "shared" / "MEMORY.md").write_text(
            "- [Fact](detail.md)\n"
        )
        results = hc.check_memory_index()
        self.assertTrue(any(m == "✗" for m, _ in results))

    def test_check_memory_index_covers_agent_lanes(self):
        # regression: broken links in an AGENT lane's MEMORY.md must be caught too
        shared = self.tmp / "memories" / "shared"
        shared.mkdir(parents=True)
        (shared / "MEMORY.md").write_text("")
        lane = self.tmp / "memories" / "agents" / "helper"
        lane.mkdir(parents=True)
        (lane / "MEMORY.md").write_text("- [Fact](ghost.md)\n")
        results = hc.check_memory_index()
        self.assertTrue(any(m == "✗" for m, _ in results))

    def test_check_memory_index_resolves(self):
        d = self.tmp / "memories" / "shared"
        d.mkdir(parents=True)
        (d / "detail.md").write_text("content")
        (d / "MEMORY.md").write_text("- [Fact](detail.md)\n")
        results = hc.check_memory_index()
        self.assertTrue(all(m == "✓" for m, _ in results))

    def test_check_recent_journal_found(self):
        jdir = self.tmp / "_ops" / "journal"
        jdir.mkdir(parents=True)
        (jdir / f"{date.today().isoformat()}.md").write_text("today")
        results = hc.check_recent_journal()
        self.assertEqual(results[0][0], "✓")

    def test_check_recent_journal_stale(self):
        # entries exist but none recent -> ✗ (this vault has gone quiet)
        from datetime import timedelta

        jdir = self.tmp / "_ops" / "journal"
        jdir.mkdir(parents=True)
        old_day = date.today() - timedelta(days=30)
        (jdir / f"{old_day.isoformat()}.md").write_text("long ago")
        results = hc.check_recent_journal()
        self.assertEqual(results[0][0], "✗")

    def test_check_recent_journal_fresh_vault(self):
        # no journal at all -> ✓ (fresh workspace, first /wrap creates it)
        (self.tmp / "_ops" / "journal").mkdir(parents=True)
        results = hc.check_recent_journal()
        self.assertEqual(results[0][0], "✓")
        self.assertIn("fresh", results[0][1])

    def test_check_no_dated_status_flags_dates(self):
        (self.tmp / "CLAUDE.md").write_text("status: active as of 2026-07-07")
        results = hc.check_no_dated_status()
        self.assertTrue(any(m == "✗" for m, _ in results))

    def test_check_no_dated_status_clean(self):
        (self.tmp / "CLAUDE.md").write_text("no dates here")
        results = hc.check_no_dated_status()
        self.assertTrue(all(m == "✓" for m, _ in results))

    def test_check_memory_structure(self):
        d = self.tmp / "memories" / "shared"
        d.mkdir(parents=True)
        (d / "MEMORY.md").write_text("- [Fact](detail.md)\n")
        results = hc.check_memory_structure()
        self.assertTrue(all(m == "✓" for m, _ in results))

    def test_memory_rot_flags_oversized_index(self):
        d = self.tmp / "memories" / "shared"
        d.mkdir(parents=True)
        (d / "MEMORY.md").write_text("".join(f"- [f{i}](f{i}.md)\n" for i in range(61)))
        results = hc.check_memory_rot()
        self.assertTrue(any(m == "⚠" and "routing lines" in msg for m, msg in results))

    def test_memory_rot_flags_missing_curate(self):
        from datetime import timedelta

        jdir = self.tmp / "_ops" / "journal"
        jdir.mkdir(parents=True)
        old_day = date.today() - timedelta(days=40)
        (jdir / f"{old_day.isoformat()}.md").write_text("worked on things")
        results = hc.check_memory_rot()
        self.assertTrue(any(m == "⚠" and "curate" in msg for m, msg in results))

    def test_memory_rot_silent_on_young_vault(self):
        # a vault younger than 30 days shouldn't nag about curate
        jdir = self.tmp / "_ops" / "journal"
        jdir.mkdir(parents=True)
        (jdir / f"{date.today().isoformat()}.md").write_text("worked on things")
        results = hc.check_memory_rot()
        self.assertFalse(any("curate" in msg for m, msg in results if m == "⚠"))

    def test_memory_rot_clean_when_recent_curate(self):
        d = self.tmp / "memories" / "shared"
        d.mkdir(parents=True)
        (d / "MEMORY.md").write_text("- [f](f.md)\n")
        jdir = self.tmp / "_ops" / "journal"
        jdir.mkdir(parents=True)
        (jdir / f"{date.today().isoformat()}.md").write_text("ran /curate today")
        results = hc.check_memory_rot()
        self.assertTrue(all(m == "✓" for m, _ in results))

    def test_rot_warnings_do_not_fail_main(self):
        # ⚠ is advisory: a repo with only rot warnings still reports pass via main()
        d = self.tmp / "memories" / "shared"
        d.mkdir(parents=True)
        (d / "MEMORY.md").write_text("".join(f"- [f{i}](f{i}.md)\n" for i in range(61)))
        import io, sys
        old = sys.stdout
        sys.stdout = io.StringIO()
        try:
            rc = hc.main()
            out = sys.stdout.getvalue()
        finally:
            sys.stdout = old
        self.assertEqual(rc, 0)
        self.assertIn("⚠", out)

    def test_main_exits_zero_even_with_failures(self):
        # empty ROOT: everything should fail, but main must still return 0
        self.assertEqual(hc.main(), 0)


if __name__ == "__main__":
    unittest.main()
