# 05. Dates

Adding dates to file names is one of the best ways to keep files sortable. A file named `2026-10-28 receipt.pdf` sorts neatly next to `2026-10-29 receipt.pdf` in every file browser.

## Use the ISO date format: YYYY-MM-DD

Always write dates as **four-digit year, two-digit month, two-digit day**:

```
2026-10-28
```

**Why:** names starting with `2026-10-28` sort in chronological order in File Explorer, Finder, and Terminal. Formats like `10-28-2026` or `28-10-2026` do not sort correctly (October 2026 would sort after November 2025).

Avoid slashes (`2026/10/28`) — some operating systems do not allow `/` in file names.

## Add today's date with built-in tools

Built-in tools usually cannot insert *today's* date automatically. You type it yourself:

### Windows PowerShell
```powershell
$date = Get-Date -Format "yyyy-MM-dd"
Get-ChildItem *.jpg | Rename-Item -NewName { "$date-" + $_.BaseName + $_.Extension }
```

### macOS / Linux Terminal
```bash
today=$(date +%F)          # %F gives 2026-10-28
for f in *.jpg; do mv "$f" "${today}-$f"; done
```

### macOS Finder
Use **Rename Items → Add Text → Before name**, and type today's date by hand (`2026-10-28-`).

## Add today's date with `scripts/rename.py`

The `--date-prefix` option prepends today's date (YYYY-MM-DD) automatically:

```bash
python3 scripts/rename.py --path ./my-copies --date-prefix --apply
```

`photo.jpg` → `2026-10-28-photo.jpg`

Combine with `--pattern` to date-stamp only certain files:

```bash
python3 scripts/rename.py --path ./my-copies --pattern '\.pdf$' --date-prefix --apply
```

## Add a date from the file itself (advanced)

Sometimes you want the date a photo was taken, not today. That requires reading file metadata (EXIF), which is beyond built-in tools and this beginner script. If you need that often, look at dedicated photo tools — or ask for a script in a future guide.

## Safety reminders for dates

- **Date-stamp copies first.** Renaming 200 photos with the wrong date is easy to undo if you practiced on copies; harder if you stamped the originals.
- **One date per run.** All files renamed in a single `--date-prefix` pass get the same date (today). That is usually what you want for a batch of files from the same day.
- **Do not put dates in folder names you plan to sync to old devices.** Very old Windows versions can struggle with long names, but `YYYY-MM-DD-` is safe everywhere modern.
