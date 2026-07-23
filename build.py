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
    lines = text.split("\n"); out = []; in_code = False; in_mermaid = False; in_list = False; list_tag = ""; i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            lang = line.strip()[3:].strip() if not in_code else ""
            if in_mermaid:
                out.append('</div>'); in_mermaid = False
            elif not in_code:
                if lang == "mermaid":
                    out.append('<div class="mermaid">')
                    in_mermaid = True
                else:
                    out.append(f'<pre><code class="language-{lang}">' if lang else "<pre><code>")
                    in_code = True
            else:
                out.append("</code></pre>"); in_code = False
            i += 1; continue
        if in_code: out.append(hm.escape(line)); i += 1; continue
        if in_list and not re.match(r'^(\d+\.\s|[-*]\s)', line.strip()) and line.strip():
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


HEAD_TOP = '<!DOCTYPE html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>{title} \u2014 ML-Biomat</title>\n<meta name="description" content="{desc}">\n<meta name="author" content="{author}">\n<link rel="canonical" href="{url}">\n<link rel="api-catalog" href="/.well-known/api-catalog">\n<link rel="describedby" type="text/plain" href="/llms.txt">\n<link rel="alternate" type="application/rss+xml" href="/rss.xml">\n<meta name="baidu-site-verification" content="codeva-PBR3uMEnYw" />\\n<meta name="google-adsense-account" content="ca-pub-7464969092761889">\\n{adsense}\n{adsense}\n<link rel="stylesheet" href="/static/css/style.css">\n{og}\n{ld}\n<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/styles/github-dark.min.css">\n<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/highlight.min.js"></script>\n<script>hljs.highlightAll();</script>\n<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script></head>\n<body>\n'

HEADER = '''<header class="site-header"><div class="header-inner">
<a href="/" class="site-brand"><span class="site-logo">ML-Biomat<span class="dot">.</span></span></a>
<nav class="nav-links">
<a href="/"{home_active}>Home / 首页</a>
<a href="/fibernet/">Library / 库</a>
<a href="/about/">About / 关于</a>
</nav>
<input type="text" id="search-input" class="search-input" placeholder="Search..." autocomplete="off">
<span class="lang-switch"><a href="/en/"{en_active}>EN</a><a href="/zh/"{zh_active}>中文</a></span>
</div></header>
<main class="container{wide_class}">'''

FOOT = '</main>\n<footer class="site-footer"><div class="footer-inner">\n<span>\u00a9 {year} ML-Biomat \u00b7 by Yunhao Yang</span>\n<div class="footer-links">\n<a href="/about/">About / 关于</a><a href="/fibernet/">Library / 库</a><a href="/rss.xml">RSS</a><a href="/sitemap.xml">Sitemap</a><a href="/privacy/">Privacy</a><a href="/privacy/">Privacy</a>\n</div>\n</div></footer>\n<div id="progress-bar" style="position:fixed;top:0;left:0;height:3px;background:var(--c-primary);z-index:9999;width:0;transition:width .1s"></div>\n<button id="back-to-top" style="position:fixed;bottom:2rem;right:2rem;width:40px;height:40px;border-radius:50%;background:var(--c-primary);color:#fff;border:none;cursor:pointer;display:none;font-size:1.2rem;z-index:999;box-shadow:var(--shadow-md)">↑</button>\n<script src="/static/js/main.js" defer></script>\n</body>\n</html>'

POST_CARD = '<article class="post-card">\n<span class="card-lang {lang_class}">{lang_label}</span>\n<h3><a href="/posts/{slug}/">{title}</a></h3>\n<div class="card-meta"><span>{date}</span><span>\u00b7</span><span>{read_min} min read</span></div>\n<p class="card-desc">{desc}</p>\n<div class="card-tags">{tags_html}</div>\n</article>'

POST_ROW = '<li class="post-row"><span class="row-date">{date}</span><a href="/posts/{slug}/">{title}</a></li>'

ARTICLE_HTML = '<article>\n<header class="article-header">\n<span class="lang-badge {lang_class}">{lang_label}</span>\n<h1>{title}</h1>\n<div class="article-meta">\n<span>{date}</span><span>\u00b7</span><span>{read_min} min read</span><span>\u00b7</span><a href="/categories/{cat_slug}/">{cat_name}</a>\n</div>\n</header>\n<div class="content">\n{html}\n</div>\n</article>'


GISCUS_SCRIPT = '<section style="margin-top:2rem;padding-top:1.5rem;border-top:1px solid var(--c-border)"><h2>Comments</h2><script src="https://giscus.app/client.js" data-repo="GellmanSparrowS/ml-biomat-blog" data-repo-id="R_kgDOTEwhsA" data-category="General" data-category-id="DIC_kwDOTEwhsM4CpPbT" data-mapping="pathname" data-reactions-enabled="1" data-emit-metadata="0" data-input-position="bottom" data-theme="preferred_color_scheme" data-lang="en" crossorigin="anonymous" async></script></section>'
ADSENSE_SCRIPT = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7464969092761889" crossorigin="anonymous"></script>'

ENGAGE_BANNER = '<section class="cta-banner">\n<h3>\U0001f4ac Questions or Feedback?</h3>\n<p>This blog is actively maintained by a PhD researcher. Reach out on GitHub for collaborations or corrections.</p>\n<a href="https://github.com/GellmanSparrowS/ml-biomat-blog">View on GitHub</a>\n</section>'

ADSENSE_SCRIPT = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7464969092761889" crossorigin="anonymous"></script>'

HERO = '''<section class="hero">
<h1>ML-Biomat</h1>
<p class="subtitle">{desc_en}</p>
<p class="subtitle" style="margin-top:.3rem;font-size:.95rem">{desc_zh}</p>
<div class="badge-row">
<span class="badge">\U0001f9ae ML for Science</span>
<span class="badge">\U0001f52c Multiscale Methods</span>
<span class="badge">\U0001f9aa Fiber Biomaterials</span>
</div>
</section>'''


def make_head(title, desc, url, lang="en", og_type="website", ld="",
              home_active="", en_active="", zh_active="", wide=""):
    head = HEAD_TOP.format(
        title=hm.escape(title), desc=hm.escape(desc), author=SITE["author"],
        url=url, lang=lang, og=og_tags(title, desc, url, og_type), ld=ld, adsense=ADSENSE_SCRIPT)
    header = HEADER.format(
        home_active=home_active, en_active=en_active, zh_active=zh_active,
        wide_class=" container-wide" if wide else "")
    return head + header


def post_card(p):
    return POST_CARD.format(
        lang_class=p["lang"], lang_label="EN" if p["lang"] == "en" else "\u4e2d\u6587",
        title=hm.escape(p["title"]), slug=p["slug"], date=p["date"],
        read_min=p["read_min"], desc=hm.escape(p["description"] or ""),
        tags_html="".join(f'<span class="tag-pill">{t}</span>' for t in p["tags"][:3]))


def section_head(lang, label, href):
    return f'<section class="section-head"><h2><span class="lang-dot {lang}"></span>{label}</h2><a href="{href}" class="view-all">View all \u2192</a></section>'




def check_coverage(posts):
    """Validate EN/ZH article pairing coverage. Prints a table at build time."""
    en_posts = {p["slug"]: p for p in posts if p["lang"] == "en"}
    zh_posts = {p["slug"]: p for p in posts if p["lang"] == "zh"}
    
    # Category-level stats
    from collections import defaultdict
    cat_stats = defaultdict(lambda: {"EN": 0, "ZH": 0})
    for p in posts:
        cat_stats[p["category"]]["EN" if p["lang"]=="en" else "ZH"] += 1
    
    print("\n  Coverage Report:")
    print(f"  {'Category':<25} {'EN':>4} {'ZH':>4} {'Status'}")
    print(f"  {'-'*25} {'-'*4} {'-'*4} {'-'*10}")
    for cat in sorted(set(p["category"] for p in posts)):
        stats = cat_stats[cat]
        status = "OK" if stats["EN"] > 0 and stats["ZH"] > 0 else "MISSING"
        print(f"  {cat:<25} {stats['EN']:>4} {stats['ZH']:>4} {status}")
    
    # Slug-based pair check disabled - use category-level coverage above
    # New articles should follow slug convention: EN {topic}, ZH {topic}-zh

def build():
    # Load Giscus HTML for article pages
    giscus_html = Path("static/giscus.html").read_text(encoding="utf-8") if Path("static/giscus.html").exists() else ""

    posts = load_posts()
    check_coverage(posts)
    en = [p for p in posts if p["lang"] == "en"]
    zh = [p for p in posts if p["lang"] == "zh"]
    print(f"Loaded {len(posts)} posts ({len(en)} EN, {len(zh)} ZH)")

    # Individual post pages
    for p in posts:
        cn = cat_name(p["category"], p["lang"])
        body = ARTICLE_HTML.format(
            title=hm.escape(p["title"]), date=p["date"], read_min=p["read_min"],
            cat_slug=p["category"], cat_name=cn, html=p["html"],
            lang_class=p["lang"], lang_label="EN" if p["lang"] == "en" else "\u4e2d\u6587") + ENGAGE_BANNER + giscus_html
        html = make_head(title=p["title"], desc=p["description"] or p["title"],
                         url=f'{SITE["base_url"]}/posts/{p["slug"]}/', lang=p["lang"],
                         og_type="article", ld=article_ld(p)) + body + FOOT.format(year=datetime.now().year)
        write_file(f"posts/{p['slug']}/index.html", html)
    print("  Posts done")

    # Homepage (bilingual)
    hero = HERO.format(desc_en=SITE["description_en"], desc_zh=SITE["description_zh"])
    # Category cards for homepage
    cat_cards_html = '<section class="section-head"><h2>\U0001f4c2 Categories / \u5206\u7c7b</h2><a href="/categories/" class="view-all">All \u2192</a></section>'
    cat_cards_html += '<div class="post-grid">'
    for s, info in CATEGORIES.items():
        cnt = sum(1 for p in posts if p["category"] == s)
        if cnt:
            cat_cards_html += f'<a href="/categories/{s}/" class="post-card" style="text-decoration:none"><span class="card-lang en">{info["name_en"]}</span><h3 style="font-size:1rem;margin-top:.3rem">{info["name_zh"]}</h3><div class="card-meta">{cnt} post(s)</div></a>'
    cat_cards_html += '</div>'
    body = hero
    body += cat_cards_html
    if en:
        body += section_head("en", "English Articles", "/en/")
        body += '<div class="post-grid">' + "\n".join(post_card(p) for p in en[:4]) + '</div>'
    if zh:
        body += section_head("zh", "\u4e2d\u6587\u6587\u7ae0", "/zh/")
        body += '<div class="post-grid">' + "\n".join(post_card(p) for p in zh[:4]) + '</div>'
    body += ENGAGE_BANNER
    html = make_head(title="ML-Biomat", desc=SITE["description_en"], url=SITE["base_url"],
                     ld=site_ld(), wide="wide", home_active=' class="active"') + body + FOOT.format(year=datetime.now().year)
    write_file("index.html", html)
    print("  Homepage done")

    # Language-specific pages
    for lang, lp, label in [("en", en, "English"), ("zh", zh, "\u4e2d\u6587")]:
        desc = SITE[f"description_{lang}"]
        hero_lang = HERO.format(desc_en=SITE["description_en"] if lang == "en" else desc,
                                 desc_zh=SITE["description_zh"] if lang == "zh" else desc)
        body = hero_lang
        body += f'<section class="section-head"><h2><span class="lang-dot {lang}"></span>{label} Articles</h2></section>'
        body += '<div class="post-grid">' + "\n".join(post_card(p) for p in lp[:12]) + '</div>'
        body += ENGAGE_BANNER
        ha = ' class="active"' if lang == "en" else ""
        za = ' class="active"' if lang == "zh" else ""
        html = make_head(title=f"{label} Articles", desc=desc,
                         url=f'{SITE["base_url"]}/{lang}/', lang=lang, ld=site_ld(),
                         wide="wide", en_active=ha, zh_active=za) + body + FOOT.format(year=datetime.now().year)
        write_file(f"{lang}/index.html", html)
    print("  Language pages done")

    # Categories index
    ci = '<h1 class="section-title">Categories</h1><ul class="post-list-simple">'
    for s, info in CATEGORIES.items():
        cnt = sum(1 for p in posts if p["category"] == s)
        if cnt:
            ci += f'<li class="post-row"><a href="/categories/{s}/"><strong>{info["name_en"]}</strong> ({info["name_zh"]})</a><span style="margin-left:auto;color:var(--c-muted);font-size:.85rem">{cnt} posts</span></li>'
    ci += "</ul>"
    html = make_head(title="Categories", desc="Browse all 44 articles across 6 categories: Machine Learning, Multiscale Modeling, Biomaterials, Python Tutorials, Wet-lab Data, Research Notes", url=f'{SITE["base_url"]}/categories/') + ci + FOOT.format(year=datetime.now().year)
    write_file("categories/index.html", html)

    # Individual category pages
    for s, info in CATEGORIES.items():
        cp = [p for p in posts if p["category"] == s]
        if not cp: continue
        en_cp = [p for p in cp if p["lang"] == "en"]
        zh_cp = [p for p in cp if p["lang"] == "zh"]
        body = f'<h1 class="section-title"><span class="highlight">{info["name_en"]}</span> / {info["name_zh"]}</h1>'
        body += '<div class="cat-grid">'
        if en_cp:
            body += '<div class="cat-col"><h3><span class="lang-dot en"></span>English</h3><ul class="post-list-simple">'
            body += "".join(POST_ROW.format(date=p["date"], title=hm.escape(p["title"]), slug=p["slug"]) for p in en_cp) + '</ul></div>'
        if zh_cp:
            body += '<div class="cat-col"><h3><span class="lang-dot zh"></span>中文</h3><ul class="post-list-simple">'
            body += "".join(POST_ROW.format(date=p["date"], title=hm.escape(p["title"]), slug=p["slug"]) for p in zh_cp) + '</ul>'
        html = make_head(title=f'{info["name_en"]} Posts', desc=f'{info["name_en"]} articles',
                         url=f'{SITE["base_url"]}/categories/{s}/') + body + FOOT.format(year=datetime.now().year)
        write_file(f"categories/{s}/index.html", html)
    print("  Categories done")

    # FiberNet page
    fibernet_body = Path("content/fibernet-body.html").read_text(encoding="utf-8")
    html = make_head(title="FiberNet", desc="FiberNet: A Python toolkit for fiber network generation, simulation, and intelligent optimization. 12 unit types, GPU acceleration, ML and RL integration.", url=SITE["base_url"] + "/fibernet/") + fibernet_body + FOOT.format(year=datetime.now().year)
    write_file("fibernet/index.html", html)

    # About page
    about_body = Path("content/about-body.html").read_text(encoding="utf-8")
    html = make_head(title="About", desc="About ML-Biomat: A bilingual technical blog exploring machine learning and multiscale modeling for fiber-based biomaterials. By Yunhao Yang at Fudan University.", url=f'{SITE["base_url"]}/about/') + about_body + FOOT.format(year=datetime.now().year)
    write_file("about/index.html", html)

    # Privacy Policy page (required for AdSense)
    privacy_body = """<article class="content">
<h1>Privacy Policy</h1>
<p><em>Last updated: 2026-07-23</em></p>

<h2>1. Who We Are</h2>
<p>ML-Biomat (ml-biomat.com) is a personal academic blog operated by Yunhao Yang, affiliated with Fudan University.</p>

<h2>2. What Data We Collect</h2>
<p>This site itself does not directly collect personal data. However, third-party services integrated into this site may collect information:</p>
<ul>
<li><strong>Google AdSense</strong>: Uses cookies to serve personalized ads based on your browsing history. Google may collect your IP address, browser type, and browsing behavior on this site.</li>
<li><strong>Giscus (comments)</strong>: Uses GitHub OAuth for authentication. Your GitHub profile information is processed by GitHub.</li>
<li><strong>Cloudflare CDN</strong>: May collect anonymized traffic data for performance and security purposes.</li>
</ul>

<h2>3. Cookies</h2>
<p>Google AdSense uses cookies (such as the DoubleClick cookie) to serve ads based on your prior visits to this or other websites. You may opt out of personalized advertising by visiting <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google Ads Settings</a>.</p>

<h2>4. How We Use Data</h2>
<p>We do not sell, trade, or share your personal data. Any data collected by third-party services is governed by their respective privacy policies.</p>

<h2>5. Your Rights</h2>
<p>You can disable cookies in your browser settings. You can also opt out of Google Analytics and personalized ads through Google's opt-out tools.</p>

<h2>6. Contact</h2>
<p>For privacy-related inquiries, contact: <a href="mailto:Gellmansparrow@outlook.com">Gellmansparrow@outlook.com</a></p>
</article>"""
    privacy_full = make_head(title="Privacy Policy", desc="Privacy policy for ML-Biomat: how we handle cookies, ads, and data.", url=SITE["base_url"] + "/privacy/") + privacy_body + FOOT.format(year=datetime.now().year)
    write_file("privacy/index.html", privacy_full)


    # Privacy Policy page (required for AdSense)
    privacy_body = """<article class="content">
<h1>Privacy Policy</h1>
<p><em>Last updated: 2026-07-23</em></p>

<h2>1. Who We Are</h2>
<p>ML-Biomat (ml-biomat.com) is a personal academic blog operated by Yunhao Yang, affiliated with Fudan University.</p>

<h2>2. What Data We Collect</h2>
<p>This site itself does not directly collect personal data. However, third-party services integrated into this site may collect information:</p>
<ul>
<li><strong>Google AdSense</strong>: Uses cookies to serve personalized ads based on your browsing history. Google may collect your IP address, browser type, and browsing behavior on this site.</li>
<li><strong>Giscus (comments)</strong>: Uses GitHub OAuth for authentication. Your GitHub profile information is processed by GitHub.</li>
<li><strong>Cloudflare CDN</strong>: May collect anonymized traffic data for performance and security purposes.</li>
</ul>

<h2>3. Cookies</h2>
<p>Google AdSense uses cookies (such as the DoubleClick cookie) to serve ads based on your prior visits to this or other websites. You may opt out of personalized advertising by visiting <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google Ads Settings</a>.</p>

<h2>4. How We Use Data</h2>
<p>We do not sell, trade, or share your personal data. Any data collected by third-party services is governed by their respective privacy policies.</p>

<h2>5. Your Rights</h2>
<p>You can disable cookies in your browser settings. You can also opt out of Google Analytics and personalized ads through Google's opt-out tools.</p>

<h2>6. Contact</h2>
<p>For privacy-related inquiries, contact: <a href="mailto:Gellmansparrow@outlook.com">Gellmansparrow@outlook.com</a></p>
</article>"""
    privacy_full = make_head(title="Privacy Policy", desc="Privacy policy for ML-Biomat: how we handle cookies, ads, and data.", url=SITE["base_url"] + "/privacy/") + privacy_body + FOOT.format(year=datetime.now().year)
    write_file("privacy/index.html", privacy_full)


    # RSS
    rss_items = []
    for p in posts[:20]:
        rss_items.append(f"""    <item>
      <title>{hm.escape(p['title'])}</title>
      <link>{SITE['base_url']}/posts/{p['slug']}/</link>
      <guid>{SITE['base_url']}/posts/{p['slug']}/</guid>
      <description>{hm.escape(p['description'] or '')}</description>
      <pubDate>{p['date']}T00:00:00+08:00</pubDate>
    </item>""")
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>ML-Biomat</title>
    <link>{SITE['base_url']}</link>
    <description>{SITE['description_en']} | {SITE['description_zh']}</description>
    <language>en</language>
    <atom:link href="{SITE['base_url']}/rss.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(rss_items)}
  </channel>
</rss>"""
    write_file("rss.xml", rss)

    # Sitemap
    urls = [
        f'  <url><loc>{SITE["base_url"]}/</loc><priority>1.0</priority></url>',
        f'  <url><loc>{SITE["base_url"]}/en/</loc><priority>0.9</priority></url>',
        f'  <url><loc>{SITE["base_url"]}/zh/</loc><priority>0.9</priority></url>',
        f'  <url><loc>{SITE["base_url"]}/fibernet/</loc><priority>0.7</priority></url>',
        f'  <url><loc>{SITE["base_url"]}/about/</loc><priority>0.6</priority></url>',
        f'  <url><loc>{SITE["base_url"]}/privacy/</loc><priority>0.3</priority></url>',
        f'  <url><loc>{SITE["base_url"]}/privacy/</loc><priority>0.3</priority></url>',
        f'  <url><loc>{SITE["base_url"]}/categories/</loc><priority>0.7</priority></url>',
    ]
    for s in CATEGORIES:
        urls.append(f'  <url><loc>{SITE["base_url"]}/categories/{s}/</loc><priority>0.6</priority></url>')
    for p in posts:
        urls.append(f'  <url><loc>{SITE["base_url"]}/posts/{p["slug"]}/</loc><priority>0.8</priority><lastmod>{p["date"]}</lastmod></url>')
    write_file("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{chr(10).join(urls)}\n</urlset>')

    
    # ads.txt for Google AdSense
    write_file("ads.txt", "google.com, pub-7464969092761889, DIRECT, f08c47fec0942fa0")


    # ads.txt for Google AdSense
    write_file("ads.txt", "google.com, pub-7464969092761889, DIRECT, f08c47fec0942fa0")

# Robots.txt
    write_file("robots.txt", f"User-agent: *\nContent-Signal: ai-train=yes, search=yes, ai-input=yes\nAllow: /\nSitemap: {SITE['base_url']}/sitemap.xml\n")

    # 404
    not_found = make_head(title="404 Not Found", desc="Page not found", url=f'{SITE["base_url"]}/404.html')
    not_found += '<h1 style="font-size:3rem;margin-top:3rem">404</h1><p>Page not found. <a href="/">Go home</a>.</p>' + FOOT.format(year=datetime.now().year)
    write_file("404.html", not_found)

    # Copy static files
    static_out = Path(BUILD_DIR) / "static"
    if static_out.exists(): shutil.rmtree(static_out)

    # --- Search index for header search ---
    import json as json_mod
    search_data = []
    for p in posts:
        search_data.append({"title": p["title"], "slug": p["slug"], "date": p["date"], "category": p["category"], "tags": p["tags"], "lang": p["lang"], "description": p["description"] or ""})
    write_file("search.json", json_mod.dumps(search_data, ensure_ascii=False))
    shutil.copytree("static", static_out)
    # Google verification
    gv = Path(BUILD_DIR) / "google4f70fafcd20d5909.html"
    gv.write_text("google-site-verification: google4f70fafcd20d5909.html", encoding="utf-8")
    # CV photo
    cv_photo = Path("static/images/photo.jpg")
    cv_photo_sq = Path("static/images/photo-sq.jpg")
    if not cv_photo.exists():
        src = Path("../\U00007667\U00007247.jpg")
        if src.exists():
            cv_photo.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, cv_photo)

    
    # --- CV Page ---
    cv_body = Path("content/cv-body.html").read_text(encoding="utf-8")
    cv_page = make_head(title="CV \u2014 Yunhao Yang", desc="Academic CV of Yunhao Yang, PhD student at Fudan University, Dept. of Macromolecular Science. Research in AI-driven multiscale modeling for biomaterials design.", url=SITE["base_url"] + "/cv/") + cv_body + FOOT.format(year=datetime.now().year)
    write_file("cv/index.html", cv_page)


    # --- llms.txt for AI crawlers ---
    wk_src = Path("content") / ".well-known"
    if wk_src.exists():
        wk_dst = Path(BUILD_DIR) / ".well-known"
        if wk_dst.exists():
            shutil.rmtree(wk_dst)
        shutil.copytree(wk_src, wk_dst)

    # Copy auth.md
    auth_src = Path("content") / "auth.md"
    if auth_src.exists():
        shutil.copy2(auth_src, Path(BUILD_DIR) / "auth.md")

    for llms_file in ['llms.txt', 'llms-full.txt']:
        src = Path('content') / llms_file
        if src.exists():
            shutil.copy2(src, Path(BUILD_DIR) / llms_file)

    # --- CNAME for custom domain ---
    (Path(BUILD_DIR) / ".nojekyll").write_text("", encoding="utf-8")
    (Path(BUILD_DIR) / "CNAME").write_text("ml-biomat.com", encoding="utf-8")
    # --- Bing Webmaster verification ---
    (Path(BUILD_DIR) / "BingSiteAuth.xml").write_text(
        '<?xml version="1.0"?>\n<users>\n\t<user>CBF04BCC82F5CD300324A057BE99494C</user>\n</users>',
        encoding="utf-8"
    )
    # --- Baidu verification ---
    (Path(BUILD_DIR) / 'baidu_verify_codeva-PBR3uMEnYw.html').write_text(
        'baidu-site-verification: codeva-PBR3uMEnYw',
        encoding='utf-8'
    )
    print(f"  {len(posts)} posts, {len(en)} EN + {len(zh)} ZH")
    print(f"  Pages generated: posts/{len(posts)}, en, zh, about, categories, rss, sitemap")
    # --- IndexNow key file ---
    indexnow_key = "cbd023642a994753b6b98784c0489ce7"
    (Path(BUILD_DIR) / f"{indexnow_key}.txt").write_text(indexnow_key, encoding="utf-8")

    # --- IndexNow auto-submission ---
    import urllib.request
    url_list = [f"{SITE['base_url']}/posts/{p['slug']}/" for p in posts]
    url_list.append(f"{SITE['base_url']}/")
    data = json.dumps({
        "host": "ml-biomat.com",
        "key": indexnow_key,
        "keyLocation": f"{SITE['base_url']}/{indexnow_key}.txt",
        "urlList": url_list
    }).encode('utf-8')
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req, timeout=10)
        print(f"  IndexNow: submitted {len(url_list)} URLs")
    except Exception as e:
        print(f"  IndexNow: submission error ({e})")



if __name__ == "__main__":
    build()