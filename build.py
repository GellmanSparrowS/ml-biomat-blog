# -*- coding: utf-8 -*-
"""Static blog generator — outputs to docs/ for GitHub Pages. Bilingual EN+ZH."""
import os, re, json, shutil, html as hm
from datetime import datetime
from pathlib import Path
from config import SITE, CATEGORIES, BUILD_DIR, CONTENT_DIR

ROOT = Path(os.getcwd()) if os.getcwd().endswith("ml-biomat-blog") else Path(__file__).parent.resolve()
os.chdir(str(ROOT))


def parse_frontmatter(text):
    meta, body = {}, text
    if text.startswith("\ufeff"): text = text[1:]
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().split("\n"):
                line = line.strip()
                if ":" in line:
                    k, v = line.split(":", 1)
                    k, v = k.strip(), v.strip().strip('"').strip("'")
                    if v.startswith("[") and v.endswith("]"):
                        v = [x.strip().strip('"').strip("'") for x in v[1:-1].split(",") if x.strip()]
                    meta[k] = v
            body = parts[2].strip()
    return meta, body


def inline_md(t):
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    return t


def md_to_html(text):
    lines = text.split("\n"); out = []; in_code = False; in_list = False; list_tag = ""; i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            if not in_code:
                lang = line.strip()[3:].strip()
                out.append(f'<pre><code class="language-{lang}">' if lang else "<pre><code>")
                in_code = True
            else:
                out.append("</code></pre>"); in_code = False
            i += 1; continue
        if in_code: out.append(hm.escape(line)); i += 1; continue
        if in_list and not re.match(r'^(\d+\.\s|[-*]\s)', line.strip()):
            out.append(f"</{list_tag}>"); in_list = False
        m = re.match(r'^(#{1,6})\s+(.+)$', line)
        if m: lvl = len(m.group(1)); out.append(f"<h{lvl}>{inline_md(m.group(2))}</h{lvl}>"); i += 1; continue
        m = re.match(r'^[-*]\s+(.+)$', line)
        if m:
            if not in_list: out.append("<ul>"); in_list = True; list_tag = "ul"
            out.append(f"<li>{inline_md(m.group(1))}</li>"); i += 1; continue
        m = re.match(r'^\d+\.\s+(.+)$', line)
        if m:
            if not in_list: out.append("<ol>"); in_list = True; list_tag = "ol"
            out.append(f"<li>{inline_md(m.group(1))}</li>"); i += 1; continue
        if re.match(r'^[-*_]{3,}$', line.strip()): out.append("<hr>"); i += 1; continue
        if line.startswith(">"):
            qt = []
            while i < len(lines) and lines[i].startswith(">"):
                qt.append(lines[i][1:].strip() if lines[i][1:2] == " " else lines[i][1:].strip()); i += 1
            out.append(f"<blockquote>{'<br>'.join(inline_md(l) for l in qt)}</blockquote>"); continue
        if "|" in line and line.strip().startswith("|"):
            tl = []
            while i < len(lines) and "|" in lines[i]: tl.append(lines[i]); i += 1
            rows = []
            for ri, rl in enumerate(tl):
                cells = [inline_md(c.strip()) for c in rl.strip().strip("|").split("|")]
                tag = "th" if ri == 0 else "td"
                rows.append("<tr>" + "".join(f"<{tag}>{c}</{tag}>" for c in cells) + "</tr>")
            out.append(f"<table>{''.join(rows)}</table>"); continue
        m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', line.strip())
        if m: out.append(f'<img src="{m.group(2)}" alt="{m.group(1)}" loading="lazy">'); i += 1; continue
        if not line.strip(): out.append(""); i += 1; continue
        out.append(f"<p>{inline_md(line)}</p>"); i += 1
    if in_list: out.append(f"</{list_tag}>")
    if in_code: out.append("</code></pre>")
    return "\n".join(out)


def load_posts():
    posts = []; posts_dir = Path(CONTENT_DIR) / "posts"
    for root, dirs, files in os.walk(posts_dir):
        for f in sorted(files, reverse=True):
            if f.endswith(".md"):
                path = Path(root) / f
                text = path.read_text(encoding="utf-8")
                meta, body = parse_frontmatter(text)
                slug = meta.get("slug", path.stem)
                try: posted = datetime.strptime(meta.get("date", "2025-01-01"), "%Y-%m-%d")
                except ValueError: posted = datetime(2025, 1, 1)
                html_content = md_to_html(body)
                wc = len(body.split()); read_min = max(1, wc // 200)
                posts.append({
                    "title": meta.get("title", slug.replace("-", " ").title()),
                    "slug": slug, "date": posted.strftime("%Y-%m-%d"),
                    "datetime": posted, "category": meta.get("category", "uncategorized"),
                    "tags": meta.get("tags", []), "lang": meta.get("lang", "en"),
                    "description": meta.get("description", ""),
                    "html": html_content, "read_min": read_min,
                })
    posts.sort(key=lambda p: p["datetime"], reverse=True)
    return posts


def og_tags(title, desc, url, og_type="website"):
    return f'''<meta property="og:title" content="{hm.escape(title)}">
<meta property="og:description" content="{hm.escape(desc)}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="ML-Biomat">'''


def ld_json(data):
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def article_ld(post):
    return ld_json({
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": post["title"], "description": post["description"],
        "datePublished": post["date"],
        "author": {"@type": "Person", "name": SITE["author"]},
        "url": f'{SITE["base_url"]}/posts/{post["slug"]}/',
    })


def site_ld():
    return ld_json({
        "@context": "https://schema.org", "@type": "WebSite",
        "name": "ML-Biomat", "url": SITE["base_url"],
        "description": SITE["description_en"],
    })


def write_file(path, content):
    p = Path(BUILD_DIR) / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def cat_name(cat_slug, lang="en"):
    c = CATEGORIES.get(cat_slug, {})
    return c.get(f"name_{lang}", c.get("name_en", cat_slug))


HEAD_TOP = '<!DOCTYPE html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>{title} \u2014 ML-Biomat</title>\n<meta name="description" content="{desc}">\n<meta name="author" content="{author}">\n<link rel="canonical" href="{url}">\n<link rel="alternate" type="application/rss+xml" href="/rss.xml">\n<link rel="stylesheet" href="/static/css/style.css">\n{og}\n{ld}\n</head>\n<body>\n'

HEADER = '''<header class="site-header"><div class="header-inner">
<a href="/" class="site-brand"><span class="site-logo">ML-Biomat<span class="dot">.</span></span></a>
<nav class="nav-links">
<a href="/"{home_active}>Home / 首页</a>
<a href="/categories/">Categories / 分类</a>
<a href="/search/">Search / 搜索</a>
<a href="/about/">About / 关于</a>
</nav>
<input type="text" id="search-input" class="search-input" placeholder="Search..." autocomplete="off">
<span class="lang-switch"><a href="/en/"{en_active}>EN</a><a href="/zh/"{zh_active}>中文</a></span>
</div></header>
<main class="container{wide_class}">'''

FOOT = '</main>\n<footer class="site-footer"><div class="footer-inner">\n<span>\u00a9 {year} ML-Biomat \u00b7 by Yunhao Yang</span>\n<div class="footer-links">\n<a href="/about/">About / 关于</a><a href="/categories/">Categories / 分类</a><a href="/rss.xml">RSS</a><a href="/sitemap.xml">Sitemap</a>\n</div>\n</div></footer>
<div id="progress-bar" style="position:fixed;top:0;left:0;height:3px;background:var(--c-primary);z-index:9999;width:0;transition:width .1s"></div>
<button id="back-to-top" onclick="window.scrollTo({top:0,behavior:'smooth'})" style="position:fixed;bottom:2rem;right:2rem;width:40px;height:40px;border-radius:50%;background:var(--c-primary);color:#fff;border:none;cursor:pointer;display:none;font-size:1.2rem;z-index:999;box-shadow:var(--shadow-md)">↑</button>
<script src="/static/js/main.js" defer></script>
</body>
</html>