import shutil
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

import precompact_note as pn


class PrecompactNoteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.orig_root = pn.ROOT
        pn.ROOT = self.tmp

    def tearDown(self):
        pn.ROOT = self.orig_root
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run(self):
        import io
        import sys

        old = sys.stdout
        sys.stdout = io.StringIO()
        try:
            rc = pn.main()
            return rc, sys.stdout.getvalue()
        finally:
            sys.stdout = old

    def test_appends_marker_to_todays_journal(self):
        rc, out = self._run()
        self.assertEqual(rc, 0)
        now = datetime.now()
        journal = self.tmp / "_ops" / "journal" / now.strftime("%Y-%m") / f"{now.strftime('%Y-%m-%d')}.md"
        self.assertTrue(journal.exists())
        self.assertIn("compaction", journal.read_text())
        self.assertIn("checkpoint", out)

    def test_appends_not_truncates(self):
        now = datetime.now()
        journal = self.tmp / "_ops" / "journal" / now.strftime("%Y-%m") / f"{now.strftime('%Y-%m-%d')}.md"
        journal.parent.mkdir(parents=True)
        journal.write_text("existing entry\n")
        self._run()
        text = journal.read_text()
        self.assertTrue(text.startswith("existing entry"))
        self.assertIn("compaction", text)

    def test_fail_open_on_unwritable_journal(self):
        # point ROOT somewhere the journal dir can't be created under
        pn.ROOT = self.tmp / "not-a-dir.txt"
        (self.tmp / "not-a-dir.txt").write_text("file, not dir")
        rc, _ = self._run()
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
