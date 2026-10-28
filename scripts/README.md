# scripts/rename.py — Safe Batch File Renamer

A tiny, beginner-friendly Python script for renaming many files at once.

**Core safety rule:** the script only *previews* by default. Nothing is renamed unless you pass `--apply`.

## Requirements

Python 3 (already on Windows, Mac, and Linux). No installation needed.

```
python3 rename.py --help
```

## Common examples

All examples assume you are practicing on a **copy** of your files.

### Preview what would happen (changes nothing)
```bash
python3 rename.py --path ./my-copies --prefix trip-
```

### Apply a prefix
```bash
python3 rename.py --path ./my-copies --prefix trip- --apply
```
`photo.jpg` → `trip-photo.jpg`

### Add today's date (YYYY-MM-DD) to .pdf files only
```bash
python3 rename.py --path ./my-copies --pattern '\.pdf$' --date-prefix --apply
```
`receipt.pdf` → `2026-10-28-receipt.pdf`

### Add a suffix before the extension
```bash
python3 rename.py --path ./my-copies --suffix -final --apply
```
`draft.docx` → `draft-final.docx`

### Rename only files matching a pattern
```bash
python3 rename.py --path ./my-copies --pattern '^IMG_\d{4}\.jpg$' --prefix photo- --apply
```

### Undo a previous run
Every applied run writes an undo log like `rename-undo-20261028-143022.json`.
```bash
python3 rename.py --undo rename-undo-20261028-143022.json --apply
```

## Options

| Option | What it does |
|--------|--------------|
| `--path FOLDER` | Folder to work in (default: current folder) |
| `--pattern REGEX` | Only rename files whose names match this regex (default: all files) |
| `--replacement TEXT` | Regex replacement text (optional) |
| `--prefix TEXT` | Add text to the front of each name |
| `--suffix TEXT` | Add text before the file extension |
| `--date-prefix` | Prepend today's date (YYYY-MM-DD) |
| `--apply` | Actually rename files (omitted = preview only) |
| `--log FILE` | Write the undo log to this file |
| `--undo FILE` | Reverse a previous run using its undo log JSON |
| `--include-folders` | Rename folders too (files only by default) |
| `--limit N` | Stop after N files (extra safety) |

## Safety reminders

- Test on copies first.
- Close all files before renaming them.
- Always preview before `--apply`.
- Keep the undo log so you can reverse the run.
