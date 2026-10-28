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
from urllib.parse import quote, unquote, urlsplit

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


def tag_integrity_errors(posts):
    """Check source-tag unions and case-sensitive routes on every platform."""
    expected = {}
    for post in posts:
        for tag in post['tags']:
            # Independent expected identity for the two known alias pairs.
            slug = tag.casefold() if tag.casefold() in {'python', 'mamba'} else tag
            expected.setdefault(slug, set()).add(post['slug'])
    files = {path.relative_to(DOCS).as_posix(): path for path in DOCS.rglob('*.html')}
    errors = []
    for slug, members in expected.items():
        for language in ['zh', 'en']:
            suffix = 'en/' if language == 'en' else ''
            relative = 'tags/' + slug + '/' + suffix + 'index.html'
            if relative not in files:
                errors.append(relative + ': missing exact-case path')
                continue
            page = files[relative].read_text(encoding='utf-8')
            actual = re.findall(r'<a[^>]+href="/posts/([^"/]+)/"', page)
            if set(actual) != members or len(actual) != len(members):
                errors.append(relative + ': tag union incomplete or duplicated')
            route = '/tags/' + quote(slug, safe='') + '/' + suffix
            canonical = re.search(r'<link rel="canonical" href="([^"]+)"', page)
            if not canonical or urlsplit(html.unescape(canonical[1])).path != route:
                errors.append(relative + ': incorrect canonical route')
    for language in ['zh', 'en']:
        suffix = 'en/' if language == 'en' else ''
        relative = 'tags/' + suffix + 'index.html'
        if relative not in files:
            errors.append(relative + ': missing tag directory')
            continue
        page = files[relative].read_text(encoding='utf-8')
        actual = re.findall(r'<a class="tag-pill" href="([^"]+)">.*?\((\d+)\)</a>', page)
        expected_cloud = {'/tags/' + quote(slug, safe='') + '/' + suffix: len(members)
                          for slug, members in expected.items()}
        actual_cloud = {html.unescape(url): int(count) for url, count in actual}
        if actual_cloud != expected_cloud or len(actual) != len(expected_cloud):
            errors.append(relative + ': tag directory counts or routes differ from source')
    for relative, path in files.items():
        parser = LocalLinks()
        parser.feed(path.read_text(encoding='utf-8'))
        for url in parser.urls:
            parsed = urlsplit(url)
            if parsed.netloc and parsed.netloc != 'ml-biomat.com':
                continue
            decoded = unquote(parsed.path)
            if not decoded.startswith('/tags/'):
                continue
            target = decoded.lstrip('/')
            if decoded.endswith('/'):
                target += 'index.html'
            if target not in files:
                errors.append(relative + ': tag URL casing or target missing: ' + url)
            parts = decoded.strip('/').split('/')
            if len(parts) >= 2 and parts[1].casefold() in {'python', 'mamba'} and parts[1] != parts[1].casefold():
                errors.append(relative + ': noncanonical tag alias: ' + url)
    return sorted(set(errors))


def run():
    checks = []
    posts = []
    for lang in ("en", "zh"):
        for p in sorted((CONTENT / lang).glob("*.md")):
            posts.append((lang, p.stem, parse_fm(p)))
    curriculum = json.loads((CONTENT.parent / "tutorials/polymer-ai/manifest.json").read_text(encoding="utf-8-sig"))
    lessons = curriculum["lessons"]
    tutorial_count = len(lessons)
    total = len(posts)
    indexed_total = total + tutorial_count
    en = sum(1 for x in posts if x[0] == "en")
    zh = total - en
    checks.append(check("EN/ZH articles balanced", en == zh, "en=%d zh=%d" % (en, zh)))

    req = ["CNAME", ".nojekyll", "ads.txt", "robots.txt", "sitemap.xml", "rss.xml",
           "search.json", "404.html", "index.html", "llms.txt", "llms-full.txt",
           "about/index.html", "about/en/index.html", "cv/index.html", "cv/en/index.html", "tutorials/index.html", "tutorials/polymer-ai/index.html"]
    missing = [f for f in req if not (DOCS / f).exists()]
    checks.append(check("Required files", not missing,
                        "missing=" + ",".join(missing) if missing else "all present"))

    cname = (DOCS / "CNAME").read_text(encoding="utf-8").strip() if (DOCS / "CNAME").exists() else ""
    checks.append(check("CNAME = ml-biomat.com", cname == "ml-biomat.com", cname))

    rss = (DOCS / "rss.xml").read_text(encoding="utf-8") if (DOCS / "rss.xml").exists() else ""
    rss_n = rss.count("<item>")
    checks.append(check("RSS covers articles and tutorials", rss_n == indexed_total, "rss=%d articles=%d tutorials=%d" % (rss_n, total, tutorial_count)))

    try:
        rss_dates = ET.fromstring(rss).findall("./channel/item/pubDate")
        valid_dates = len(rss_dates) == indexed_total and all(parsedate_to_datetime(node.text).tzinfo is not None for node in rss_dates)
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
    checks.append(check("Search covers articles and tutorials", search_n == indexed_total, "search=%d articles=%d tutorials=%d" % (search_n, total, tutorial_count)))

    docs_n = len(list((DOCS / "posts").glob("*/index.html")))
    checks.append(check("Generated post pages == posts", docs_n == total, "pages=%d posts=%d" % (docs_n, total)))

    tutorial_errors = []
    for i, lesson in enumerate(lessons):
        page = DOCS / "tutorials/polymer-ai" / lesson["slug"] / "index.html"
        if not page.is_file():
            tutorial_errors.append(lesson["slug"] + ": missing page")
            continue
        body = page.read_text(encoding="utf-8")
        if 'class="tutorial-reader"' not in body or 'id="python-code"' not in body:
            tutorial_errors.append(lesson["slug"] + ": reader or code missing")
        for category in lesson['categories'][:1]:
            if '/categories/' + category + '/' not in body:
                tutorial_errors.append(lesson['slug'] + ': category missing')
        category_page = DOCS / 'categories' / lesson['categories'][0] / 'index.html'
        if lesson['slug'] not in category_page.read_text(encoding='utf8'):
            tutorial_errors.append(lesson['slug'] + ': absent from category')
        if re.search(r'(?:src|href)=["\']data:', body) or "正文润色稿" in body or "润色时跳过" in body:
            tutorial_errors.append(lesson["slug"] + ": import residue")
    checks.append(check("Tutorial category integration", len(lessons) == 20 and not tutorial_errors,
                        "; ".join(tutorial_errors) if tutorial_errors else "20 articles, code and category links present"))

    # Translation links are reciprocal and each page has its own localized title.
    import build
    loaded = build.load_posts()
    tag_errors = tag_integrity_errors(loaded)
    checks.append(check('Tag unions and case-sensitive URLs', not tag_errors,
                        '; '.join(tag_errors[:15]) if tag_errors else 'Merged tag aliases retain every article; tag counts, canonical URLs and link casing agree'))
    by_lang = {lang:{p['slug']:p for p in loaded if p['lang']==lang} for lang in ['en','zh']}
    pair_errors=[]; figure_errors=[]
    for post in loaded:
        pair=build.find_pair(post,by_lang)
        page=(DOCS/'posts'/post['slug']/'index.html').read_text(encoding='utf8')
        expected_title='<title>'+html.escape(post['title'])+' — ML-Biomat</title>'
        switch=re.search(r'<span class="lang-switch">(.*?)</span>',page,re.S)
        if not pair or not switch or '/posts/'+pair['slug']+'/' not in switch[1] or expected_title not in page:
            pair_errors.append(post['slug'])
        figure_paths=re.findall(r'<img[^>]+src="(/static/images/article-guides/[^"]+)"',page)
        if len(figure_paths)<2 or any(not src.endswith('-'+post['lang']+'.svg') for src in figure_paths):
            figure_errors.append(post['slug'])
    checks.append(check('Reciprocal localized article navigation',not pair_errors, ', '.join(pair_errors) if pair_errors else '48 pages, 24 reciprocal pairs and localized titles'))
    checks.append(check('Bilingual illustrated articles',not figure_errors, ', '.join(figure_errors) if figure_errors else 'At least two explanatory figures in each of 48 articles'))
    old_blocks=[]
    for path in [DOCS/'index.html',DOCS/'zh/index.html',DOCS/'categories/index.html']:
        if '系列教程' in path.read_text(encoding='utf8'): old_blocks.append(str(path.relative_to(DOCS)))
    checks.append(check('Topic-first browsing',not old_blocks, ', '.join(old_blocks) if old_blocks else 'No separate series blocks on home, categories or language collections'))

    # Site-wide UI contract, including untranslated articles.
    chrome_errors=[]
    from content_tools import chrome
    for page_path in DOCS.rglob('*.html'):
        relative=page_path.relative_to(DOCS).as_posix()
        if relative.startswith('static/'):continue
        page=page_path.read_text(encoding='utf8')
        if 'class="site-header"' not in page:continue  # redirects and ownership verification files
        locale=re.search(r'<html lang="([^"]+)"',page)[1]
        english=locale=='en'
        header=re.search(r'<header class="site-header">(.*?)</header>',page,re.S)[1]
        nav=re.findall(r'<a data-nav="([^"]+)"[^>]*>([^<]+)</a>',header)
        expected=[(key,en_label if english else zh_label) for key,zh_label,en_label in chrome.NAV]
        switch=re.search(r'<span class="lang-switch">(.*?)</span>',header,re.S)
        if nav!=expected or not switch or len(re.findall(r'data-language=',switch[1]))!=2:
            chrome_errors.append(relative+': inconsistent header')
        if 'data-theme="dark"' not in page[:180] or chrome.THEME_INIT not in page:
            chrome_errors.append(relative+': missing pre-paint default')
        home='/en/' if english else '/'
        if f'href="{home}" class="site-brand"' not in header:
            chrome_errors.append(relative+': home loses locale')
    checks.append(check('Shared navigation and dark-first shell',not chrome_errors,'; '.join(chrome_errors[:15]) if chrome_errors else 'All generated pages retain both language controls, matching navigation, and dark initialization'))
    home_errors=[]
    for path,language in [('index.html','zh-CN'),('en/index.html','en'),('zh/index.html','zh-CN')]:
        page=(DOCS/path).read_text(encoding='utf8')
        if '<h1>ML-Biomat</h1>' not in page or '<html lang="'+language+'"' not in page:
            home_errors.append(path)
        header=re.search(r'<span class="lang-switch">(.*?)</span>',page,re.S)[1]
        if 'href="/en/"' not in header or 'href="/"' not in header:home_errors.append(path+': wrong counterpart')
    for path in ['articles/index.html','articles/en/index.html']:
        if not (DOCS/path).is_file():home_errors.append(path)
    checks.append(check('Home language switch preserves page type',not home_errors,', '.join(home_errors) if home_errors else 'Chinese and English homepages remain homepages; article collections have separate routes'))
    primary_errors=[]
    for lesson in lessons:
        if len(lesson['categories'])!=1:primary_errors.append(lesson['slug'])
    for post in loaded:
        pair=build.find_pair(post,by_lang)
        if pair and pair['category']!=post['category']:primary_errors.append(post['slug'])
    checks.append(check('One primary topic with bilingual agreement',not primary_errors,', '.join(primary_errors) if primary_errors else '44 Chinese and 24 English entries have one primary topic; article pairs agree'))

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