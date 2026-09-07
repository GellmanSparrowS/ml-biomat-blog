# -*- coding: utf-8 -*-
"""Insert long UTF-8 markdown prose into a post at a line anchor.

Usage:
  python content_tools/insert_after.py POST.md --after "## Heading" BLOCK.md
  python content_tools/insert_after.py POST.md --before "## Heading" BLOCK.md

This avoids the friction of embedding large blocks of prose inside ad-hoc
scripts and keeps article edits auditable and encoding-safe.
"""
import argparse
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("post")
    ap.add_argument("block")
    ap.add_argument("--after")
    ap.add_argument("--before")
    a = ap.parse_args()
    if bool(a.after) == bool(a.before):
        raise SystemExit("supply exactly one of --after or --before")
    anchor = a.after or a.before
    post = Path(a.post); block = Path(a.block)
    text = post.read_text(encoding="utf-8")
    n = text.count(anchor)
    if n != 1:
        raise SystemExit(f"anchor found {n} time(s), expected exactly 1: {anchor!r}")
    content = block.read_text(encoding="utf-8").strip()
    newline = "\n"
    if a.after:
        text = text.replace(anchor, anchor + newline + content, 1)
    else:
        text = text.replace(anchor, content + newline + anchor, 1)
    post.write_text(text, encoding="utf-8")
    print(f"inserted {block.name} into {post.name} -> {len(text.split())} words total")

if __name__ == "__main__":
    main()