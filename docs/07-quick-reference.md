# 07. Quick Reference

Tape this page to your monitor.

## Before you start

```
1. Copy the folder → practice on the copy
2. Close all files you will rename
3. Dry-run / preview first
4. Apply only when the preview looks right
5. Keep the undo log
```

## Built-in commands

| Task | Windows PowerShell | macOS/Linux Terminal |
|------|-------------------|---------------------|
| Preview `.jpg` files | `Get-ChildItem *.jpg` | `ls *.jpg` |
| Add prefix `trip-` | `Get-ChildItem *.js \|\?` | `for f in *.jpg; do mv "$f" "trip-$f"; done` |
| PowerShell apply | `Get-ChildItem *.jpg \| Rename-Item -NewName { "trip-" + $_.BaseName + $_.Extension }` | — |
| Undo | `Ctrl+Z` (File Explorer only) | None |

## `scripts/rename.py`

```bash
# Preview (changes nothing)
python3 scripts/rename.py --path ./folder --prefix trip-

# Apply
python3 scripts/rename.py --path ./folder --prefix trip- --apply

# Add today's date (YYYY-MM-DD)
python3 scripts/rename.py --path ./folder --date-prefix --apply

# Only files matching a pattern
python3 scripts/rename.py --path ./folder --pattern '\.pdf$' --prefix invoice- --apply

# Undo a previous run
python3 scripts/rename.py --undo rename-undo-*.json
```

## Regex cheat sheet

| Pattern | Matches |
|---------|---------|
| `*.jpg` | All JPEG files (wildcard) |
| `\.pdf$` | Names ending in `.pdf` |
| `^IMG_\d{4}` | Names starting with `IMG_` + 4 digits |
| `\d{3}` | Exactly 3 digits |
| `\.jpe?g$` | `.jpg` or `.jpeg` |

## Date format

Always use `YYYY-MM-DD` (for example `2026-10-28`) so files sort in order.

## Emergency

- Renamed the wrong files on a **copy**? Delete the copy and try again.
- Renamed originals and have an **undo log**? Run `scripts/rename.py --undo <log-file>`.
- Renamed originals, no log, File Explorer/Finder? Press `Ctrl+Z` / `Cmd+Z` right away.
- Otherwise: rename each file back by hand. That is why we test on copies.
