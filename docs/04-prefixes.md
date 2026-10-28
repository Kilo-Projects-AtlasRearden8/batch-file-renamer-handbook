# 04. Prefixes

A **prefix** is text added to the *front* of a file name:
```
invoice-2026-10.pdf      ← prefix added
2026-10-invoice-2026-10.pdf
```

Prefixes are useful for grouping files, sorting them together, or marking their status (for example `draft-`, `final-`, `archive-`).

## Using built-in tools

### Windows File Explorer / Finder
Select the files, rename the first one with your prefix (for example `trip-1.jpg`), and the operating system numbers the rest: `trip-2.jpg`, `trip-3.jpg`…
- This works well when you want *all* selected files to share one prefix and a number.
- It gives you less control over exactly which number each file gets.

### PowerShell
```powershell
Get-ChildItem *.jpg | Rename-Item -NewName { "trip-" + $_.BaseName + $_.Extension }
```

### macOS Finder "Rename Items"
Right-click → **Rename X Items** → **Add Text** → choose "Before name" → type your prefix → **Rename**.

### Terminal (`mv`)
```bash
for f in *.jpg; do mv "$f" "trip-$f"; done
```

## Using `scripts/rename.py`

The script adds a prefix without touching the rest of the name:

```bash
python3 scripts/rename.py --path ./my-copies --prefix trip- --apply
```

`photo.jpg` → `trip-photo.jpg`

You can combine `--prefix` with `--pattern` so only matching files get the prefix:

```bash
python3 scripts/rename.py --path ./my-copies --pattern '\.pdf$' --prefix invoice- --apply
```

## Prefix do's and don'ts

| Do | Don't |
|----|-------|
| Test on copies first | Add prefixes to open files |
| Use a short, clear prefix (`2026-`, `draft-`, `receipt-`) | Use prefixes with spaces if you work in the Terminal a lot |
| Keep prefixes consistent across a project | Rename the same folder twice with different prefixes (it gets confusing fast) |
| Preview before applying | Forget the file extension stays the same |

## Real-world example

You scanned ten receipts named `scan_001.tif` through `scan_010.tif`. You want them grouped under a `receipt-` prefix:

```bash
python3 scripts/rename.py --path ./receipt-copies --pattern '\.tif$' --prefix receipt- --apply
```

Result: `receipt-scan_001.tif`, …, `receipt-scan_010.tif`

Keep the undo log the script writes — if you decide `receipt-` was the wrong word, you can reverse every rename in one step (section 06).
