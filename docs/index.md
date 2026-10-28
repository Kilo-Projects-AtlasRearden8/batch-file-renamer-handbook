# Safe Batch File Renaming — Beginner Manual

Welcome. This manual teaches you how to rename lots of files at once — safely — using the tools already on your computer, plus a tiny script you can copy and paste.

**Published by Asdale Dynamics, LLC** — beginner-friendly AI education, books, and practical tools.
Written for Dylan Asdale, registered nurse turned AI author and founder of Asdale Dynamics, LLC (Indiana, formed October 2026).

## The one rule to remember

**Test on copies, never originals.** Copy your folder, practice there, and only rename the real files when the copy worked exactly as expected.

## Sections

- [01 Safety First](docs/01-safety-first.md) — golden rules before you rename anything
- [02 Built-In Tools](docs/02-built-in-tools.md) — Windows, Mac, Linux renaming without installing anything
- [03 Patterns](docs/03-patterns.md) — wildcards and regular expressions
- [04 Prefixes](docs/04-prefixes.md) — adding text to the front of file names
- [05 Dates](docs/05-dates.md) — adding `YYYY-MM-DD` dates so files sort in order
- [06 Undo Precautions](docs/06-undo-precautions.md) — dry-runs, undo logs, recovery
- [07 Quick Reference](docs/07-quick-reference.md) — cheat sheet

## Script

A tiny, beginner-friendly Python batch renamer lives in `scripts/rename.py`. It runs in preview mode by default and writes an undo log for every change. See `scripts/README.md`.

## Worksheet

A printable worksheet is at `site/worksheet.html`. Open it in your browser and print (`Ctrl+P` / `Cmd+P`).

## Static site

This manual is also available as a read-only HTML site in `site/`. Open `site/index.html` — no internet required.

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.

## Credit

Created by Asdale Dynamics, LLC (Indiana, formed October 2026). Learn more at dylanasdale.github.io
