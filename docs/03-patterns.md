# 03. Patterns

A **pattern** is how you tell the computer "only rename files that look like this." Patterns keep you from accidentally renaming files you meant to leave alone.

This page covers two kinds:
1. **Wildcards** — simple, built into every operating system
2. **Regular expressions (regex)** — more powerful, used by the `rename.py` script

## Wildcards (built-in)

| Wildcard | Meaning | Example matches |
|----------|---------|-----------------|
| `*` | Any text, any length | `*.jpg` matches every `.jpg` file |
| `?` | Exactly one character | `photo?.jpg` matches `photo1.jpg`, not `photo12.jpg` |
| `[abc]` | One of those letters | `file[12].txt` matches `file1.txt` and `file2.txt` |

**Example:** rename only the invoices:
```powershell
Get-ChildItem invoice-*.pdf | Rename-Item -NewName { "2026-" + $_.Name }
```

## Regular expressions (regex)

Regular expressions let you match patterns like "exactly three digits" or "anything before the date." They look scary but are built from a few simple pieces.

### The most useful pieces

| Piece | Meaning | Example |
|-------|---------|---------|
| `.` | Any single character | `a.c` matches `abc`, `a2c` |
| `*` | Zero or more of the thing before it | `ab*` matches `a`, `ab`, `abb` |
| `+` | One or more of the thing before it | `ab+` matches `ab`, `abb`, not `a` |
| `?` | Zero or one of the thing before it | `colou?r` matches `color` and `colour` |
| `\d` | Any digit (0–9) | `\d\d\d` matches `123`, `007` |
| `\D` | Anything that is not a digit | |
| `\w` | Any letter, digit, or underscore | |
| `^` | Start of the text | `^IMG` matches names starting with `IMG` |
| `$` | End of the text | `\.jpg$` matches names ending in `.jpg` |
| `(...)` | A group you can reuse | `(\d{4})-(\d{2})-(\d{2})` |
| `\1`, `\2` | Text matched by group 1, 2 | Use in the replacement |

### Examples

Find photos named `IMG_1234.jpg`:
```regex
^IMG_\d{4}\.jpg$
```
(`\d{4}` means exactly four digits.)

Find files that start with a date like `2026-10-28`:
```regex
^\d{4}-\d{2}-\d{2}
```

Find anything with a space in the name:
```regex
\s
```

## How to use patterns safely

1. **List first, rename second.** Show the list of matching files before changing anything. `scripts/rename.py` does this automatically in dry-run mode.
2. **Test your pattern on copies.** A pattern that looks right on paper can match more files than you expect on a real folder.
3. **Start narrow.** Match too few files rather than too many. You can always run a second pass.
4. **Watch the extension.** `\.jpg$` matches only `.jpg` files — the backslash before the dot matters because `.` alone means "any character."

## Pattern playground

Before renaming real files, test your pattern here:

| I want to match | Try this pattern |
|-----------------|------------------|
| All PDFs | `\.pdf$` or `*.pdf` |
| Files starting with `scan` | `^scan` or `scan*` |
| `IMG_` followed by 4 digits | `^IMG_\d{4}` |
| Names containing `draft` | `draft` |
| Exactly 3 digits anywhere | `\d{3}` |
| Names ending in `.jpg` or `.jpeg` | `\.jpe?g$` |
