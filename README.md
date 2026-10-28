# Safe Batch File Renaming — Beginner Manual

A plain-English guide to renaming lots of files at once — safely — using the tools already on your computer, plus tiny scripts you can copy and paste.

**Published by Asdale Dynamics, LLC** — beginner-friendly AI education, books, and practical tools.
**Written for Dylan Asdale**, registered nurse turned AI author and founder of Asdale Dynamics, LLC (Indiana, formed October 2026). His book *The Massive AI Manual* and hub site dylanasdale.github.io explain AI "like a friend would": plain English, step by step, never condescending.

## What this is for

You have a folder full of files named `IMG_4829.jpg`, `document-final-v2.pdf`, `scan_001.tif`, and you want them named something useful like `2026-10-28 receipt.pdf`. Doing it one file at a time is slow. Doing it all at once with a single wrong click can scramble a hundred names in seconds.

This manual teaches you how to:

- Rename files in batches using **built-in tools** (Windows File Explorer, PowerShell, macOS Finder, Linux/macOS Terminal)
- Use **patterns** (wildcards and regular expressions) to rename only the files you mean to
- Add **prefixes** and **dates** to file names
- **Undo safely** — test on copies, never touch originals, keep an undo log

## Contents (docs/)

1. [01-safety-first.md](docs/01-safety-first.md) — the golden rules before you rename anything
2. [02-built-in-tools.md](docs/02-built-in-tools.md) — Windows, Mac, and Linux built-in renaming
3. [03-patterns.md](docs/03-patterns.md) — wildcards and regular expressions
4. [04-prefixes.md](docs/04-prefixes.md) — adding prefixes to file names
5. [05-dates.md](docs/05-dates.md) — adding dates to file names
6. [06-undo-precautions.md](docs/06-undo-precautions.md) — dry-runs, undo logs, recovery
7. [07-quick-reference.md](docs/07-quick-reference.md) — cheat sheet you can tape to your monitor

## Scripts

`scripts/rename.py` — a tiny, beginner-friendly Python batch renamer.
- **Dry-run by default:** shows what it would do without changing anything.
- **Undo log:** every run writes a log so you can reverse the renames exactly.
- Works on Windows, Mac, and Linux.

See `scripts/README.md` for usage.

## Worksheet

A printable worksheet is at `site/worksheet.html` (open it in your browser and press `Ctrl+P` / `Cmd+P` to print). It walks you through a real rename exercise step by step with blanks to fill in and safety checks to tick off.

## Static site

A read-only HTML version of this manual lives in `site/`. Open `site/index.html` in any browser — no internet required.

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.

## Credit

Created by Asdale Dynamics, LLC (Indiana, formed October 2026). Learn more at dylanasdale.github.io
