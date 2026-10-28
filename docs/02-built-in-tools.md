# 02. Built-In Tools

You do not need to install anything to start batch renaming. Every computer comes with tools that can do it. Here is how to use the built-in tools on Windows, Mac, and Linux — and when to switch to a tiny script instead.

## Windows — File Explorer (easiest, safest for beginners)

1. Open the folder with your files.
2. Select the files you want to rename:
   - Click one file, then `Ctrl+A` to select all, or hold `Ctrl` and click to pick several.
   - To select a range, click the first file, hold `Shift`, click the last file.
3. Right-click and choose **Rename** (or press `F2`).
4. Type the new name and press `Enter`.

**What happens:** Windows renames the first file to exactly what you typed, and numbers the rest automatically:
- `vacation.jpg` → `vacation (1).jpg`, `vacation (2).jpg`, …

**Undo:** press `Ctrl+Z` right after renaming. This only works for renames done inside File Explorer, and only immediately after.

## Windows — PowerShell (more control)

PowerShell is built into Windows. Open PowerShell in the folder (type `powershell` in the folder's address bar and press `Enter`), then run:

```powershell
# Preview only: show what would happen, changes nothing
Get-ChildItem *.jpg | ForEach-Object { $_.Name, $_.BaseName + "-copy" + $_.Extension }

# Apply: add a prefix to every .jpg file
Get-ChildItem *.jpg | Rename-Item -NewName { "trip-" + $_.BaseName + $_.Extension }
```

**Safety tip:** run the preview version first. When the list looks right, add the rename command.

**Undo:** PowerShell does not keep an undo log by default. That is why the golden rule (test on copies) matters even more here.

## macOS — Finder

1. Open the folder in Finder.
2. Select the files (`Cmd+A` for all, or hold `Cmd` and click).
3. Right-click (or `Ctrl`+click) and choose **Rename X Items**.
4. In the window that opens choose:
   - **Replace Text** — swap one piece of text for another
   - **Add Text** — add text before or after the name
   - **Format** — give all files the same name with numbers (`trip-1.jpg`, `trip-2.jpg`…)
5. Click **Rename**.

**Undo:** press `Cmd+Z` immediately after renaming (Finder only).

## macOS / Linux — Terminal (`mv`)

The Terminal (macOS) or console (Linux) has the `mv` command ("move," used for renaming too).

Rename one file:
```bash
mv "old-name.jpg" "new-name.jpg"
```

Rename many at once with a loop:
```bash
# Preview first: echo shows what would happen
for f in *.jpg; do echo "mv \"$f\" \"trip-$f\""; done

# Then apply (remove the echo when the preview looks right)
for f in *.jpg; do mv "$f" "trip-$f"; done
```

**Important:** always put file names in quotes (`"$f"`) so names with spaces do not break the command.

**Undo:** the Terminal has no undo. Test on copies.

## When built-in tools are not enough

Built-in tools are great for simple jobs (add a prefix, number a series, replace one word). Use a tiny script when you need:

- Dates added automatically (see section 05)
- Complex patterns, like "only files with three digits in the name" (section 03)
- An undo log written automatically (section 06)
- The same rename repeated every week (automation)

That is what `scripts/rename.py` is for — see its README for examples.

## Quick choice guide

| Job | Best tool |
|-----|-----------|
| Rename 5–20 files by hand | File Explorer / Finder |
| Add same prefix to many files | File Explorer / Finder / PowerShell |
| Replace one word in many names | PowerShell / Finder / Terminal loop |
| Add today's date to every name | `scripts/rename.py` |
| Complex pattern (only certain files) | `scripts/rename.py` |
| Want an automatic undo log | `scripts/rename.py` |
