# -*- coding: utf-8 -*-
"""Offline, double-clickable preview of docs/ -> _preview/ (no server needed).

Rewrites absolute internal URLs to relative ones so pages open from file paths.
Usage:
  python snapshot.py [--open] [--zip]
"""
import argparse
import os
import re
import shutil
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
OUT = ROOT / "_preview"


def copy_tree(src, dst):
    for f in src.rglob("*"):
        rel = f.relative_to(src)
        out = dst / rel
        if f.is_dir():
            out.mkdir(parents=True, exist_ok=True)
        else:
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, out)


def fix_html(path):
    depth = len(path.parent.relative_to(OUT).parts)
    prefix = "../" * depth
    text = path.read_text(encoding="utf-8", errors="replace")

    def repl(m):
        path_part = m.group(2)
        if path_part == "/":
            target = "index.html"
        elif path_part.endswith("/"):
            target = path_part[1:] + "index.html"
        else:
            target = path_part[1:]
        return m.group(1) + '="' + prefix + target + '"'

    return re.sub(r'(href|src|action)="(/[^"]*)"', repl, text)


def make():
    if OUT.exists():
        shutil.rmtree(OUT)
    copy_tree(DOCS, OUT)
    n = 0
    for h in OUT.rglob("*.html"):
        h.write_text(fix_html(h), encoding="utf-8")
        n += 1
    return n


def open_file(path):
    try:
        os.startfile(str(path))  # Windows native opener
    except Exception:
        webbrowser.open(path.as_uri())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--open", action="store_true")
    ap.add_argument("--zip", action="store_true")
    a = ap.parse_args()
    if not (DOCS / "index.html").exists():
        raise SystemExit("docs/index.html not found. Run: python build.py")
    n = make()
    print("snapshot:", OUT, "(%d html files rewritten)" % n)
    if a.zip:
        zpath = ROOT / "site_preview.zip"
        if zpath.exists():
            zpath.unlink()
        shutil.make_archive(str(ROOT / "site_preview"), "zip", OUT)
        print("zip:", zpath)
    if a.open:
        open_file(OUT / "index.html")


if __name__ == "__main__":
    main()