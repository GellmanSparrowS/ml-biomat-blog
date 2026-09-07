# -*- coding: utf-8 -*-
"""Sectioned Markdown writer for ml-biomat-blog (anti-truncation).

Writes one section per part file, then assembles + validates the final post.
Resume-safe by design: each part is on disk as soon as it is written.

Usage:
  python article_writer.py new <slug> --lang en --category python-tutorials \
      --title "Title" --date 2026-09-05 --desc "..." --tags a,b,c [--root REPO]
  python article_writer.py part <slug> --n 1 --file part-01.md [--root REPO]
  python article_writer.py list [slug] [--root REPO]
  python article_writer.py assemble <slug> [--check-only] [--min-words 800]
                                            [--max-h2 7] [--clean] [--root REPO]

Draft layout: <root>/_drafts/<slug>/meta.json + part-01.md ... part-NN.md
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path


def count_words_en(text):
    return len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text))


def count_hanzi(text):
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def extract_images(body):
    srcs = []
    srcs += re.findall(r"!\[[^\]]*\]\(([^)\s]+?)(?:[\s\"'][^)]*)?\)", body)
    srcs += re.findall(r"<img[^>]+src=[\"']([^\"']+)[\"']", body)
    return srcs


class Draft:
    def __init__(self, root, slug):
        self.root = Path(root)
        self.slug = slug
        self.dir = self.root / "_drafts" / slug

    def meta_path(self):
        return self.dir / "meta.json"

    def load_meta(self):
        return json.loads(self.meta_path().read_text(encoding="utf-8"))

    def parts(self):
        return sorted(self.dir.glob("part-*.md"), key=lambda p: int(p.stem.split("-")[1]))

    def save_meta(self, meta):
        self.dir.mkdir(parents=True, exist_ok=True)
        self.meta_path().write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    def write_part(self, n, text):
        self.dir.mkdir(parents=True, exist_ok=True)
        p = self.dir / ("part-%02d.md" % n)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text.rstrip() + "\n")
            f.flush()
            os.fsync(f.fileno())
        return p

    def delete_part(self, n):
        p = self.dir / ("part-%02d.md" % n)
        if p.exists():
            p.unlink()

    def assemble(self, check_only=False, min_words=800, max_h2=7, lang=None):
        meta = self.load_meta()
        lang = lang or meta.get("lang", "en")
        parts = [p.read_text(encoding="utf-8").rstrip() for p in self.parts()]
        body = "\n\n".join(parts)
        errors = self.validate(meta, body, lang, min_words, max_h2)
        if check_only or errors:
            if errors:
                print("[validate] FAIL:")
                for e in errors:
                    print("  -", e)
            else:
                print("[validate] OK")
            return errors
        tags = meta.get("tags", [])
        tags_s = ", ".join('"%s"' % t for t in tags) if tags else ""
        fm = "---\n"
        fm += 'title: "%s"\n' % meta["title"]
        fm += 'date: %s\n' % meta.get("date", "2026-01-01")
        fm += "category: %s\n" % meta["category"]
        fm += "tags: [%s]\n" % tags_s
        fm += "lang: %s\n" % lang
        fm += 'slug: "%s"\n' % self.slug
        fm += 'description: "%s"\n' % meta.get("description", "")
        fm += "---\n"
        out = self.root / "content" / "posts" / lang / (meta.get("filename", self.slug) + ".md")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(fm + "\n" + body + "\n", encoding="utf-8")
        print("[assemble] wrote", out)
        return []

    def validate(self, meta, body, lang, min_words, max_h2):
        errs = []
        for k in ("title", "category", "lang", "slug"):
            if not meta.get(k):
                errs.append("missing frontmatter: " + k)
        if not self.parts():
            errs.append("no parts written")
        wc = count_words_en(body) if lang == "en" else count_hanzi(body)
        if wc < min_words:
            errs.append("%s length %d < min %d" % ("words" if lang == "en" else "hanzi", wc, min_words))
        h2 = len(re.findall(r"^##\s", body, re.M))
        if h2 > max_h2:
            errs.append("%d H2 > max %d" % (h2, max_h2))
        for src in extract_images(body):
            if not (src.startswith("http") or src.startswith("//")):
                clean = src.split("#")[0].split("?")[0]
                rel = clean.lstrip("/") if clean.startswith("/static/") else clean
                if not (self.root / rel).exists() and not (self.root / "docs" / rel).exists():
                    errs.append("missing local image: " + src)
        return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("new", "part", "list", "assemble"))
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--root", default=os.getcwd())
    ap.add_argument("--lang", default="en")
    ap.add_argument("--category")
    ap.add_argument("--title")
    ap.add_argument("--date")
    ap.add_argument("--desc")
    ap.add_argument("--tags")
    ap.add_argument("--n", type=int)
    ap.add_argument("--file")
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--clean", action="store_true")
    ap.add_argument("--min-words", type=int)
    ap.add_argument("--max-h2", type=int, default=7)
    a = ap.parse_args()
    d = Draft(a.root, a.slug)
    if a.cmd == "new":
        if not (a.title and a.category):
            sys.exit("--title and --category are required for new")
        meta = {
            "slug": a.slug, "lang": a.lang, "category": a.category, "title": a.title,
            "date": a.date or None, "description": a.desc or "", "tags": [],
            "filename": a.slug,
        }
        if a.tags:
            meta["tags"] = [t.strip() for t in a.tags.split(",") if t.strip()]
        d.save_meta(meta)
        print("[new] created", d.meta_path())
    elif a.cmd == "part":
        if not a.file or not a.n:
            sys.exit("--n and --file are required for part")
        text = Path(a.file).read_text(encoding="utf-8")
        d.write_part(a.n, text)
        print("[part] wrote part-%02d (%d chars)" % (a.n, len(text)))
    elif a.cmd == "list":
        if d.dir.exists():
            for p in d.parts():
                print(p.name, len(p.read_text(encoding="utf-8")), "chars")
        else:
            for p in sorted((d.root / "_drafts").glob("*/meta.json")) if (d.root / "_drafts").exists() else []:
                print(p.parent.name)
    elif a.cmd == "assemble":
        minw = a.min_words or (800 if (d.load_meta().get("lang") == "en") else 3000)
        errs = d.assemble(a.check_only, minw, a.max_h2)
        if a.clean and not errs and not a.check_only:
            import shutil
            shutil.rmtree(d.dir)
            print("[clean] removed draft", d.dir)
        if errs:
            sys.exit(1)


if __name__ == "__main__":
    main()