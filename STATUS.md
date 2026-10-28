STATUS — Safe Batch File Renaming Handbook
==========================================

What was built
--------------
A beginner-friendly guide to safe batch file renaming, published by Asdale Dynamics, LLC.

Contents:
- docs/ — seven-part beginner manual (Markdown):
    - 01-safety-first.md — golden rules (test on copies, never originals, preview first, undo log)
    - 02-built-in-tools.md — Windows File Explorer/PowerShell, macOS Finder, macOS/Linux Terminal mv
    - 03-patterns.md — wildcards and regular expressions with a pattern playground
    - 04-prefixes.md — adding prefixes to file names
    - 05-dates.md — ISO YYYY-MM-DD dates so files sort in order
    - 06-undo-precautions.md — dry-run mode, undo log, undo checklist
    - 07-quick-reference.md — cheat sheet
- scripts/rename.py — tiny Python batch renamer:
    - Dry-run by default (nothing changes unless --apply is passed)
    - Writes an undo log JSON for every applied run
    - --undo reverses a previous run, checking each file before restoring
    - Supports --pattern, --prefix, --suffix, --date-prefix, --replacement, --limit
- scripts/README.md — usage and examples for the script
- tests/test_rename.py — 14 unit tests (unittest, stdlib only)
- site/index.html — static HTML version of the full manual (no build step, open in any browser)
- site/worksheet.html — printable worksheet with safety checklist and fill-in blanks (Ctrl+P / Cmd+P to print)
- site/style.css — shared styles for the static site
- LICENSE — MIT License, copyright line exactly "Copyright (c) 2026 Asdale Dynamics, LLC"
- README.md — project overview crediting Asdale Dynamics, LLC

Who it's for
------------
Dylan Asdale, registered nurse turned AI author and founder of Asdale Dynamics, LLC (Indiana, formed October 2026). Plain English, step by step, never condescending. Local-first, no secrets, no personal data.

How to run it
-------------
1. Copy a folder of files to a practice location (test on copies first).
2. Open a terminal in the practice folder.
3. Preview (changes nothing):
       python3 scripts/rename.py --path ./my-copies --prefix trip-
4. When the preview looks right, apply:
       python3 scripts/rename.py --path ./my-copies --prefix trip- --apply
5. Keep the undo log written by the script. To reverse:
       python3 scripts/rename.py --undo rename-undo-<timestamp>.json --apply

Open the static site:
- site/index.html — full manual
- site/worksheet.html — printable worksheet (print via browser)

No installation required beyond Python 3 (already on Windows, Mac, Linux).

Verification results
--------------------
- Unit tests: 14/14 pass (python3 -m unittest tests.test_rename), run from scripts/
  - dry-run changes nothing
  - apply renames files and writes an undo log
  - pattern matching, limit, date-prefix, suffix-before-extension, regex replacement
  - folders excluded by default
  - invalid pattern exits cleanly
  - undo reverses an applied run; undo dry-run changes nothing
- py_compile rename.py: OK (no SyntaxWarnings)
- python3 rename.py --help: OK
- End-to-end smoke test: dry-run → apply prefix → undo restores all files exactly
- End-to-end smoke test: --date-prefix produces 2026-10-28-<name>.jpg style names
- Static site files present: site/index.html, site/worksheet.html, site/style.css

Known gaps
----------
- No automated HTML validation (no build step; files are plain HTML/CSS, verified by opening in a browser)
- No CI/CD configuration (intentionally: no .github/workflows per project rules)
- Script does not read photo metadata (EXIF) for "date taken" — uses today's date only; documented in docs/05-dates.md
- Undo log reversal stops and warns if a file no longer has the expected name; it does not guess
- Manual is Markdown + HTML only; no PDF export yet (worksheet is printable from browser)

Credit
------
Created by Asdale Dynamics, LLC (Indiana, formed October 2026). Learn more at dylanasdale.github.io
