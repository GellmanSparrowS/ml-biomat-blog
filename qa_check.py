# -*- coding: utf-8 -*-
"""Post-build health checks -> _qa/site_report.html (open in browser)."""
import argparse
import html
import os
import json
import re
import webbrowser
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from datetime import datetime
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
CONTENT = ROOT / "content" / "posts"


def parse_fm(path):
    t = path.read_text(encoding="utf-8")
    meta = {}
    if t.startswith("---"):
        parts = t.split("---", 2)
        for line in parts[1].strip().split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
    return meta


def check(name, ok, detail=""):
    return {"name": name, "ok": bool(ok), "detail": detail}


class LocalLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src", "action") and value:
                self.urls.append(value)


def broken_local_links():
    """Resolve internal links as an HTTP server does, including URL decoding."""
    docs_root = DOCS.resolve()
    broken = set()
    for page in sorted(DOCS.rglob("*.html")):
        parser = LocalLinks()
        parser.feed(page.read_text(encoding="utf-8"))
        for url in parser.urls:
            try:
                parsed = urlsplit(url)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                decoded = unquote(parsed.path)
                target = (docs_root / decoded.lstrip("/")) if decoded.startswith("/") else (page.parent / decoded)
                target = target.resolve()
                if not target.is_relative_to(docs_root):
                    broken.add((str(page.relative_to(DOCS)), url))
                    continue
                if target.is_dir() or decoded.endswith("/"):
                    target = target / "index.html"
                if not target.is_file():
                    broken.add((str(page.relative_to(DOCS)), url))
            except ValueError:
                broken.add((str(page.relative_to(DOCS)), url))
    return sorted(broken)


def run():
    checks = []
    posts = []
    for lang in ("en", "zh"):
        for p in sorted((CONTENT / lang).glob("*.md")):
            posts.append((lang, p.stem, parse_fm(p)))
    total = len(posts)
    en = sum(1 for x in posts if x[0] == "en")
    zh = total - en
    checks.append(check("EN/ZH articles balanced", en == zh, "en=%d zh=%d" % (en, zh)))

    req = ["CNAME", ".nojekyll", "ads.txt", "robots.txt", "sitemap.xml", "rss.xml",
           "search.json", "404.html", "index.html", "llms.txt", "llms-full.txt",
           "about/index.html", "about/en/index.html", "cv/index.html", "cv/en/index.html"]
    missing = [f for f in req if not (DOCS / f).exists()]
    checks.append(check("Required files", not missing,
                        "missing=" + ",".join(missing) if missing else "all present"))

    cname = (DOCS / "CNAME").read_text(encoding="utf-8").strip() if (DOCS / "CNAME").exists() else ""
    checks.append(check("CNAME = ml-biomat.com", cname == "ml-biomat.com", cname))

    rss = (DOCS / "rss.xml").read_text(encoding="utf-8") if (DOCS / "rss.xml").exists() else ""
    rss_n = rss.count("<item>")
    checks.append(check("RSS items == posts", rss_n == total, "rss=%d posts=%d" % (rss_n, total)))

    try:
        rss_dates = ET.fromstring(rss).findall("./channel/item/pubDate")
        valid_dates = len(rss_dates) == total and all(parsedate_to_datetime(node.text).tzinfo is not None for node in rss_dates)
    except (ValueError, TypeError, ET.ParseError):
        valid_dates = False
    checks.append(check("RSS publication dates", valid_dates, "reader-compatible dates" if valid_dates else "invalid or missing dates"))

    sm = (DOCS / "sitemap.xml").read_text(encoding="utf-8") if (DOCS / "sitemap.xml").exists() else ""
    locs = re.findall(r"<loc>(.*?)</loc>", sm)
    dups = sorted({u for u in locs if locs.count(u) > 1})
    checks.append(check("Sitemap has no duplicated URLs", not dups,
                        "dups=" + ",".join(dups) if dups else "unique urls=%d" % len(locs)))

    missing_sitemap = []
    for url in locs:
        path = unquote(urlsplit(url).path).lstrip("/")
        target = (DOCS / path).resolve()
        if not target.is_relative_to(DOCS.resolve()):
            missing_sitemap.append(url)
            continue
        if target.is_dir() or urlsplit(url).path.endswith("/"):
            target = target / "index.html"
        if not target.is_file():
            missing_sitemap.append(url)
    checks.append(check("Sitemap destinations", not missing_sitemap, ", ".join(missing_sitemap) if missing_sitemap else "all listed pages exist"))

    try:
        search_n = len(json.loads((DOCS / "search.json").read_text(encoding="utf-8")))
    except Exception:
        search_n = -1
    checks.append(check("search.json items == posts", search_n == total, "search=%d posts=%d" % (search_n, total)))

    docs_n = len(list((DOCS / "posts").glob("*/index.html")))
    checks.append(check("Generated post pages == posts", docs_n == total, "pages=%d posts=%d" % (docs_n, total)))

    broken = broken_local_links()
    link_detail = (
        "%d broken references: " % len(broken)
        + "; ".join("%s -> %s" % item for item in broken[:12])
    ) if broken else "all internal links resolve"
    checks.append(check("Internal links and assets", not broken, link_detail))

    issue_rows = []
    for lang, stem, m in posts:
        errs = []
        title = m.get("title", "")
        desc = m.get("description", "")
        if lang == "en" and desc and len(desc) < 150:
            errs.append("desc %d<150" % len(desc))
        if lang == "zh" and desc and len(desc) < 60:
            errs.append("desc %d<60" % len(desc))
        if len(title) > 70:
            errs.append("title %d>70" % len(title))
        for k in ("title", "date", "category", "tags", "lang", "slug", "description"):
            if k not in m:
                errs.append("missing " + k)
        if errs:
            issue_rows.append((lang, stem, ", ".join(errs)))
    checks.append(check("No per-post SEO/frontmatter issues", not issue_rows,
                        "%d posts with issues" % len(issue_rows) if issue_rows else "clean"))
    return checks, issue_rows, {"total": total, "en": en, "zh": zh}


def render(checks, issue_rows, summary):
    rows = "\n".join(
        '<tr class="%s"><td>%s</td><td>%s</td><td>%s</td></tr>'
        % ("ok" if c["ok"] else "bad", html.escape(c["name"]),
           "PASS" if c["ok"] else "FAIL", html.escape(c["detail"]))
        for c in checks)
    issues = "\n".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (html.escape(l), html.escape(s), html.escape(d))
        for l, s, d in issue_rows) or '<tr><td colspan="3">none</td></tr>'
    return """<!doctype html><html><head><meta charset="utf-8"><title>Site QA Report</title>
<style>body{font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;margin:2rem;max-width:920px;line-height:1.5;color:#1e293b}
h1{font-size:1.4rem}h2{font-size:1.1rem;margin-top:1.4rem}
table{border-collapse:collapse;width:100%%;margin:.7rem 0}th,td{border:1px solid #e2e8f0;padding:.4rem .6rem;text-align:left;font-size:.9rem}
tr.ok td:nth-child(2){color:#15803d;font-weight:600}tr.bad td:nth-child(2){color:#b91c1c;font-weight:600}
.summary{color:#475569}</style></head><body>
<h1>Site QA Report</h1><p class="summary">Generated %s &middot; posts=%d (en=%d, zh=%d)</p>
<h2>Checks</h2><table><tr><th>Check</th><th>Result</th><th>Detail</th></tr>%s</table>
<h2>Per-post issues</h2><table><tr><th>Lang</th><th>File</th><th>Issues</th></tr>%s</table>
</body></html>""" % (datetime.now().isoformat(timespec="seconds"), summary["total"], summary["en"], summary["zh"], rows, issues)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--open", action="store_true")
    a = ap.parse_args()
    checks, issue_rows, summary = run()
    outdir = ROOT / "_qa"
    outdir.mkdir(exist_ok=True)
    out = outdir / "site_report.html"
    out.write_text(render(checks, issue_rows, summary), encoding="utf-8")
    fails = [c for c in checks if not c["ok"]]
    print("QA report:", out)
    print("summary: %d/%d checks passing" % (len(checks) - len(fails), len(checks)))
    for c in checks:
        print(("PASS " if c["ok"] else "FAIL "), c["name"], "-", c["detail"])
    if a.open:
        try:
            os.startfile(str(out))
        except Exception:
            webbrowser.open(out.as_uri())
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())