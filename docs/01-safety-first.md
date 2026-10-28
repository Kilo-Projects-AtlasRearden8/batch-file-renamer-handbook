# 01. Safety First

Before you rename a single file, read this page. Batch renaming is fast — and mistakes are fast too. One wrong command can rename a hundred files in a second, and "undo" is not always built in.

## The golden rules

1. **Test on copies, never originals.** Copy your folder to a new folder (or to a USB stick) and practice there first. Only rename the real files when the copy worked exactly as you expected.
2. **Never move originals.** The scripts and commands in this manual rename files in place; they do not move them to another drive or delete them. You should not either, while learning.
3. **Use dry-run mode first.** Every tool here has a "preview only" mode that shows what *would* happen without changing anything. Always run that first.
4. **Keep an undo log.** A good batch rename writes down every old name and every new name so you can reverse it exactly, file by file.
5. **Rename one type of file at a time.** Don't rename photos, PDFs, and spreadsheets in the same pass unless you really mean to. It is easier to spot mistakes when all the files look alike.
6. **Close the files first.** Close any open documents, photos, or spreadsheets before renaming them. Some programs lock files and will refuse to rename them — or worse, lose track of them.

## What can go wrong

| Mistake | What happens | How to avoid it |
|---------|--------------|-----------------|
| Renaming originals instead of copies | Original names are lost | Copy the folder first; practice on the copy |
| A pattern matches too many files | Files you meant to skip get renamed | Preview first; narrow the pattern |
| A typo in the replacement text | All files get the same typo | Preview first; check the preview list carefully |
| No undo log kept | You cannot reverse the rename | Use tools that write an undo log |
| Renaming open files | Errors or corrupted programs | Close all files before renaming |

## If something goes wrong

- **Windows:** open the folder in File Explorer, press `Ctrl+Z` to undo the last rename (works for renames done in File Explorer only).
- **Any tool:** if you kept an undo log, run the undo steps listed there (see section 06).
- **Worst case:** you copied the folder first, so your originals are safe. Delete the copy and try again.

**Remember: there is no shame in testing on copies. The people who lose files are the people who skip this step.**
