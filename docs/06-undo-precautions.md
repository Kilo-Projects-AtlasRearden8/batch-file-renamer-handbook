# 06. Undo Precautions

Undo is the most important part of batch renaming. Every tool in this manual has limits on what it can reverse. Know them before you start.

## What can be undone, and how

| Tool | Undo method | Limits |
|------|-------------|--------|
| Windows File Explorer | `Ctrl+Z` immediately after | Only renames done in File Explorer; only the most recent action |
| macOS Finder | `Cmd+Z` immediately after | Only renames done in Finder; only the most recent action |
| PowerShell `Rename-Item` | No built-in undo | You must reverse each rename by hand |
| Terminal `mv` | No built-in undo | You must reverse each rename by hand |
| `scripts/rename.py` | Undo log written by the script | Reverses exactly what that run did |

## Dry-run mode — always run it first

`scripts/rename.py` does **nothing** unless you pass `--apply`. Without it, the script only prints what it would do:

```bash
python3 scripts/rename.py --path ./my-copies --prefix trip-
```

Output example:
```
DRY RUN — no files were changed
photo.jpg   →   trip-photo.jpg
vacation.jpg   →   trip-vacation.jpg
```

Look the list over. Does every arrow look right? Did any file you wanted to skip appear? If something looks wrong, change the pattern or prefix and dry-run again. Only when the preview looks perfect do you add `--apply`.

## The undo log

Every `--apply` run of `scripts/rename.py` writes a file like `rename-undo-20261028-143022.json` in the folder you ran it from. It looks like:

```json
[
  { "from": "/path/my-copies/photo.jpg", "to": "/path/my-copies/trip-photo.jpg" },
  { "from": "/path/my-copies/vacation.jpg", "to": "/path/my-copies/trip-vacation.jpg" }
]
```

To reverse that exact run:

```bash
python3 scripts/rename.py --undo rename-undo-20261028-143022.json
```

The script renames every `to` name back to its `from` name, in reverse order. It checks that each file still has the expected `to` name before moving it — if a file has changed since, it stops and warns you instead of guessing.

## How to undo without the script

If you used File Explorer, Finder, PowerShell, or Terminal, there is no log file. Your undo options:

1. **Immediately after:** `Ctrl+Z` (Windows) or `Cmd+Z` (Mac) — only in the same window/app you used.
2. **By hand:** rename each file back to its old name. If you renamed many files, write the old→new pairs down on paper before you start (the worksheet at `site/worksheet.html` has a table for this).
3. **Restore from the copy:** if you tested on copies and something went wrong with the originals (you shouldn't have — golden rule!), delete the damaged folder and copy the originals back.

## The undo checklist

Before you apply any batch rename:

- [ ] I am working on a **copy** of my files
- [ ] I ran a **dry-run / preview** first
- [ ] The preview list shows exactly the changes I expect
- [ ] All files to be renamed are **closed**
- [ ] I know how to undo: `Ctrl+Z`, `Cmd+Z`, by hand, or `scripts/rename.py --undo`
- [ ] I saved the undo log somewhere I can find it

**If you cannot answer "yes" to every item, stop and copy your folder first.**
