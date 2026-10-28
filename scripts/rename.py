#!/usr/bin/env python3
r"""Safe batch file renamer for beginners.

Safety design:
  * Dry-run by default: nothing is renamed unless you pass --apply.
  * Every applied run writes an undo log (JSON) so changes can be reversed.
  * Undo checks each file still has the expected new name before reversing it.
  * Works on copies: we never touch anything outside the folder you point us at.

Usage examples:

  # Preview only (default) - shows what would happen, changes nothing
  python3 rename.py --path ./my-copies --prefix trip-

  # Apply the preview
  python3 rename.py --path ./my-copies --prefix trip- --apply

  # Add today's date (YYYY-MM-DD) to the front of every .pdf file
  python3 rename.py --path ./my-copies --pattern '\.pdf$' --date-prefix --apply

  # Undo a previous run using its undo log
  python3 rename.py --undo rename-undo-20261028-143022.json
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime

DEFAULT_PATTERN = ".*"


def today_stamp():
    return datetime.now().strftime("%Y-%m-%d")


def split_name(filename):
    """Return (stem, extension) where extension includes the leading dot."""
    return os.path.splitext(filename)


def build_new_name(filename, pattern, replacement, prefix, suffix, date_prefix):
    """Compute the new name for a single file. Returns None if unchanged."""
    stem, ext = split_name(filename)
    new = filename

    # 1. Pattern match (must match for anything to change)
    if not re.search(pattern, filename):
        return None

    # 2. Regex replacement, if requested
    if replacement is not None:
        new = re.sub(pattern, replacement, filename)
        stem, ext = split_name(new)

    # 3. Date prefix (today's date, YYYY-MM-DD)
    if date_prefix:
        stem = today_stamp() + "-" + stem

    # 4. Text prefix / suffix (suffix goes before the extension)
    if prefix:
        stem = prefix + stem
    if suffix:
        stem = stem + suffix

    new = stem + ext
    return new if new != filename else None


def plan_renames(folder, pattern, replacement, prefix, suffix, date_prefix,
                 files_only, include_folders, limit):
    """Build a list of (old_path, new_path) tuples without renaming anything."""
    if not os.path.isdir(folder):
        print(f"Error: not a folder: {folder}", file=sys.stderr)
        sys.exit(1)

    try:
        compiled = re.compile(pattern)
    except re.error as exc:
        print(f"Error: invalid pattern '{pattern}': {exc}", file=sys.stderr)
        sys.exit(1)

    entries = sorted(os.listdir(folder))
    plan = []
    count = 0

    for name in entries:
        full = os.path.join(folder, name)
        is_dir = os.path.isdir(full)
        if is_dir and not include_folders:
            continue
        if (not is_dir) and not files_only:
            continue

        # Re-compile check already done; use search on the file name
        if not compiled.search(name):
            continue

        new_name = build_new_name(
            name, pattern, replacement, prefix, suffix, date_prefix
        )
        if new_name is None:
            continue

        new_path = os.path.join(folder, new_name)
        if os.path.abspath(full) == os.path.abspath(new_path):
            continue

        plan.append((full, new_path))
        count += 1
        if limit is not None and count >= limit:
            break

    return plan


def apply_renames(plan, log_path=None, verbose=True):
    """Rename files according to plan. Optionally write an undo log."""
    if not plan:
        print("No files would be renamed.")
        return []

    if verbose:
        print(f"{'DRY RUN' if DRY_RUN else 'APPLY'} — {len(plan)} file(s):")
        for old, new in plan:
            print(f"  {os.path.basename(old)}  →  {os.path.basename(new)}")

    if DRY_RUN:
        print("DRY RUN — no files were changed. Add --apply to rename for real.")
        return []

    undo_log = []
    for old, new in plan:
        try:
            os.rename(old, new)
            undo_log.append({"from": old, "to": new})
            print(f"  renamed {os.path.basename(old)} → {os.path.basename(new)}")
        except OSError as exc:
            print(f"  ERROR renaming {os.path.basename(old)}: {exc}", file=sys.stderr)

    if log_path:
        with open(log_path, "w", encoding="utf-8") as handle:
            json.dump(undo_log, handle, indent=2)
        print(f"Undo log written: {log_path}")

    print(f"Done — {len(undo_log)} file(s) renamed.")
    return undo_log


# Flip this to True when --apply is passed.
DRY_RUN = True


def undo_renames(log_path, verbose=True):
    """Reverse a previous run using its undo log."""
    if not os.path.isfile(log_path):
        print(f"Error: undo log not found: {log_path}", file=sys.stderr)
        sys.exit(1)

    with open(log_path, "r", encoding="utf-8") as handle:
        log = json.load(handle)

    if not log:
        print("Undo log is empty. Nothing to reverse.")
        return

    print(f"Undoing {len(log)} rename(s) from {log_path}:")
    fixed = 0
    skipped = 0
    # Reverse order so the last rename is undone first.
    for entry in reversed(log):
        old_name = entry["from"]
        new_name = entry["to"]
        if not os.path.exists(new_name):
            print(f"  SKIP (not found): {os.path.basename(new_name)}")
            skipped += 1
            continue
        if DRY_RUN:
            print(f"  [dry run] {os.path.basename(new_name)} → {os.path.basename(old_name)}")
            fixed += 1
            continue
        try:
            os.rename(new_name, old_name)
            print(f"  restored  {os.path.basename(new_name)} → {os.path.basename(old_name)}")
            fixed += 1
        except OSError as exc:
            print(f"  ERROR restoring {os.path.basename(new_name)}: {exc}", file=sys.stderr)
            skipped += 1

    if DRY_RUN:
        print("DRY RUN — nothing was restored. Add --apply to undo for real.")
    else:
        print(f"Done — {fixed} restored, {skipped} skipped.")


def main(argv=None):
    global DRY_RUN

    parser = argparse.ArgumentParser(
        description="Safely batch-rename files. Dry-run by default; use --apply to change files."
    )
    parser.add_argument("--path", default=".", help="Folder containing the files (default: current folder)")
    parser.add_argument("--pattern", default=DEFAULT_PATTERN,
                        help="Regex pattern a file name must match (default: matches everything)")
    parser.add_argument("--replacement", default=None,
                        help="Regex replacement text (optional)")
    parser.add_argument("--prefix", default=None, help="Text to add to the front of each name")
    parser.add_argument("--suffix", default=None, help="Text to add before the file extension")
    parser.add_argument("--date-prefix", action="store_true",
                        help="Add today's date (YYYY-MM-DD) to the front of each name")
    parser.add_argument("--apply", action="store_true",
                        help="Actually rename files. Without this, the script only previews.")
    parser.add_argument("--log", default=None, help="Path for the undo log (auto-created if omitted)")
    parser.add_argument("--undo", default=None, help="Undo a previous run using its undo log JSON")
    parser.add_argument("--include-folders", action="store_true",
                        help="Include folders in the rename (files only by default)")
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of files to rename")

    args = parser.parse_args(argv)

    if args.undo:
        DRY_RUN = not args.apply
        undo_renames(args.undo, verbose=True)
        return

    DRY_RUN = not args.apply

    log_path = args.log
    if (not DRY_RUN) and log_path is None:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_path = os.path.join(os.path.abspath(args.path), f"rename-undo-{stamp}.json")

    plan = plan_renames(
        folder=args.path,
        pattern=args.pattern,
        replacement=args.replacement,
        prefix=args.prefix,
        suffix=args.suffix,
        date_prefix=args.date_prefix,
        files_only=not args.include_folders,
        include_folders=args.include_folders,
        limit=args.limit,
    )

    apply_renames(plan, log_path=log_path, verbose=True)


if __name__ == "__main__":
    main()
