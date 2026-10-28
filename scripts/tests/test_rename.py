#!/usr/bin/env python3
"""Tests for scripts/rename.py — run with: python3 -m unittest tests.test_rename -v"""

import io
import json
import os
import shutil
import tempfile
import unittest

from contextlib import redirect_stdout

import rename


class TestRename(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _write(self, name, content=""):
        path = os.path.join(self.tmp, name)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(content)
        return path

    def test_today_stamp_format(self):
        stamp = rename.today_stamp()
        self.assertRegex(stamp, r"^\d{4}-\d{2}-\d{2}$")

    def test_dry_run_changes_nothing(self):
        self._write("photo.jpg")
        self._write("notes.txt")
        rename.DRY_RUN = True
        plan = rename.plan_renames(self.tmp, r"\.jpg$", None, "trip-", None, False,
                                   files_only=True, include_folders=False, limit=None)
        self.assertEqual(len(plan), 1)
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "photo.jpg")))
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "trip-photo.jpg")))

    def test_apply_prefix(self):
        self._write("photo.jpg")
        self._write("notes.txt")
        rename.DRY_RUN = False
        log = os.path.join(self.tmp, "undo.json")
        plan = rename.plan_renames(self.tmp, r"\.jpg$", None, "trip-", None, False,
                                   files_only=True, include_folders=False, limit=None)
        undo_log = rename.apply_renames(plan, log_path=log, verbose=False)
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "trip-photo.jpg")))
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "photo.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "notes.txt")))
        self.assertTrue(os.path.isfile(log))

    def test_pattern_matches_only_selected_files(self):
        self._write("a.jpg")
        self._write("b.pdf")
        self._write("c.jpg")
        plan = rename.plan_renames(self.tmp, r"\.jpg$", None, "x-", None, False,
                                   files_only=True, include_folders=False, limit=None)
        self.assertEqual(len(plan), 2)

    def test_limit(self):
        for n in ("a.jpg", "b.jpg", "c.jpg"):
            self._write(n)
        plan = rename.plan_renames(self.tmp, r"\.jpg$", None, "x-", None, False,
                                   files_only=True, include_folders=False, limit=2)
        self.assertEqual(len(plan), 2)

    def test_date_prefix(self):
        self._write("photo.jpg")
        rename.DRY_RUN = False
        plan = rename.plan_renames(self.tmp, r"\.jpg$", None, None, None, True,
                                   files_only=True, include_folders=False, limit=None)
        self.assertEqual(len(plan), 1)
        old, new = plan[0]
        self.assertTrue(os.path.basename(new).startswith(rename.today_stamp() + "-"))
        self.assertTrue(os.path.basename(new).endswith(".jpg"))

    def test_undo_log_structure(self):
        self._write("photo.jpg")
        rename.DRY_RUN = False
        log = os.path.join(self.tmp, "undo.json")
        plan = rename.plan_renames(self.tmp, r"\.jpg$", None, "trip-", None, False,
                                   files_only=True, include_folders=False, limit=None)
        rename.apply_renames(plan, log_path=log, verbose=False)
        with open(log, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["from"], os.path.join(self.tmp, "photo.jpg"))
        self.assertEqual(data[0]["to"], os.path.join(self.tmp, "trip-photo.jpg"))

    def test_undo_reverses(self):
        self._write("photo.jpg")
        rename.DRY_RUN = False
        log = os.path.join(self.tmp, "undo.json")
        plan = rename.plan_renames(self.tmp, r"\.jpg$", None, "trip-", None, False,
                                   files_only=True, include_folders=False, limit=None)
        rename.apply_renames(plan, log_path=log, verbose=False)
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "photo.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "trip-photo.jpg")))

        rename.DRY_RUN = False
        rename.undo_renames(log, verbose=False)
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "photo.jpg")))
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "trip-photo.jpg")))

    def test_folders_excluded_by_default(self):
        os.mkdir(os.path.join(self.tmp, "subdir"))
        self._write("a.jpg")
        plan = rename.plan_renames(self.tmp, r".*", None, "x-", None, False,
                                   files_only=True, include_folders=False, limit=None)
        self.assertEqual(len(plan), 1)

    def test_suffix_before_extension(self):
        self._write("draft.docx")
        rename.DRY_RUN = False
        plan = rename.plan_renames(self.tmp, r"\.docx$", None, None, "-final", False,
                                   files_only=True, include_folders=False, limit=None)
        old, new = plan[0]
        self.assertEqual(os.path.basename(new), "draft-final.docx")

    def test_replacement(self):
        new = rename.build_new_name("scan-2026.pdf", r"scan-", "invoice-", None, None, False)
        self.assertEqual(new, "invoice-2026.pdf")

    def test_invalid_pattern_exits(self):
        with self.assertRaises(SystemExit):
            rename.plan_renames(self.tmp, r"[", None, None, None, False,
                                files_only=True, include_folders=False, limit=None)

    def test_no_files_matches_empty_plan(self):
        plan = rename.plan_renames(self.tmp, r"\.jpg$", None, "x-", None, False,
                                   files_only=True, include_folders=False, limit=None)
        self.assertEqual(len(plan), 0)

    def test_undo_dry_run_does_not_change(self):
        self._write("photo.jpg")
        rename.DRY_RUN = False
        log = os.path.join(self.tmp, "undo.json")
        plan = rename.plan_renames(self.tmp, r"\.jpg$", None, "trip-", None, False,
                                   files_only=True, include_folders=False, limit=None)
        rename.apply_renames(plan, log_path=log, verbose=False)
        buf = io.StringIO()
        rename.DRY_RUN = True
        with redirect_stdout(buf):
            rename.undo_renames(log, verbose=True)
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "trip-photo.jpg")))
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "photo.jpg")))


if __name__ == "__main__":
    unittest.main()
