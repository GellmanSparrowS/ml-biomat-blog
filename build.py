# -*- coding: utf-8 -*-
"""Static blog generator — outputs to docs/ for GitHub Pages. Bilingual EN+ZH."""
import argparse, hashlib, os, re, json, shutil, html as hm, urllib.parse
from datetime import datetime, timezone, timedelta
from email.utils import format_datetime
from pathlib import Path
from config import SITE, CATEGORIES, BUILD_DIR, CONTENT_DIR
from content_tools import tutorials

ROOT = Path(__file__).resolve().parent
INDEXNOW_KEY = "cbd023642a994753b6b98784c0489ce7"
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

def slugify(text):
    s = hm.unescape(re.sub(r'<[^>]+>', '', text)).lower()
    return re.sub(r'[^a-z0-9\u4e00-\u9fff]+', '-', s).strip('-')

def build_toc(html):
    heads = re.findall(r'<h([23]) id="([^"]+)">(.*?)</h\1>', html)
    if len(heads) < 2:
        return ""
    items = []
    for lvl, hid, inner in heads:
        label = hm.unescape(re.sub(r'<[^>]+>', '', inner))
        cls = "toc-h3" if lvl == "3" else "toc-h2"
        items.append(f'<li class="{cls}"><a href="#{hid}">{label}</a></li>')
    return '<details class="toc" open><summary>Contents / 目录</summary><ul>' + "".join(items) + "</ul></details>"

def md_to_html(text):
    lines = text.split("\n"); out = []; in_code = False; in_mermaid = False; in_list = False; list_tag = ""; i = 0; used_ids = {}
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
        if m:
            lvl = len(m.group(1)); inner = inline_md(m.group(2)); hid = slugify(inner)
            if hid in used_ids:
                used_ids[hid] += 1; hid = f"{hid}-{used_ids[hid]}"
            else:
                used_ids[hid] = 1
            out.append(f'<h{lvl} id="{hid}">{inner}</h{lvl}>'); i += 1; continue
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
                raw_cells = [c.strip() for c in rl.strip().strip("|").split("|")]
                if ri == 1 and all(re.fullmatch(r":?-{3,}:?", cell) for cell in raw_cells):
                    continue
                cells = [inline_md(cell) for cell in raw_cells]
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
                toc = build_toc(html_content)
                wc = len(body.split()); read_min = max(1, wc // 200)
                posts.append({
                    "title": meta.get("title", slug.replace("-", " ").title()),
                    "slug": slug, "date": posted.strftime("%Y-%m-%d"),
                    "datetime": posted, "category": meta.get("category", "uncategorized"),
                    "tags": meta.get("tags", []), "lang": meta.get("lang", "en"),
                    "description": meta.get("description", ""),
                    "html": html_content, "toc": toc, "read_min": read_min, "word_count": wc,
                })
    posts.sort(key=lambda p: p["datetime"], reverse=True)
    return posts


def og_tags(title, desc, url, og_type="website", og_image=None):
    img = ""
    if og_image:
        img = f'\n<meta property="og:image" content="{og_image}">\n<meta name="twitter:card" content="summary_large_image">'
    return f'''<meta property="og:title" content="{hm.escape(title)}">
<meta property="og:description" content="{hm.escape(desc)}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="ML-Biomat">{img}'''


def ld_json(data):
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def article_ld(post):
    url = f'{SITE["base_url"]}/posts/{post["slug"]}/'
    article = {
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": post["title"], "description": post["description"],
        "datePublished": post["date"], "dateModified": post["date"],
        "wordCount": post.get("word_count", 0),
        "inLanguage": "en" if post["lang"] == "en" else "zh-CN",
        "author": {"@type": "Person", "name": SITE["author"], "url": "https://github.com/GellmanSparrowS"},
        "publisher": {"@type": "Organization", "name": "ML-Biomat", "url": SITE["base_url"]},
        "url": url,
    }
    og_path = Path("static/images/og") / f'{post["slug"]}.png'
    if og_path.exists():
        article["image"] = f'{SITE["base_url"]}/static/images/og/{post["slug"]}.png'
    breadcrumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE["base_url"]},
            {"@type": "ListItem", "position": 2, "name": cat_name(post["category"], post["lang"]),
             "item": f'{SITE["base_url"]}/categories/{post["category"]}/'},
            {"@type": "ListItem", "position": 3, "name": post["title"], "item": url},
        ],
    }
    return ld_json(article) + ld_json(breadcrumb)


def site_ld():
    return ld_json({
        "@context": "https://schema.org", "@type": "WebSite",
        "name": "ML-Biomat", "url": SITE["base_url"],
        "description": SITE["description_en"],
    })


def person_ld():
    return ld_json({
        "@context": "https://schema.org", "@type": "Person",
        "name": "Yunhao Yang", "alternateName": "杨云浩",
        "jobTitle": "PhD Student", "affiliation": {"@type": "Organization", "name": "Fudan University"},
        "url": SITE["base_url"] + "/about/",
        "sameAs": [
            "https://github.com/GellmanSparrowS",
            "https://www.researchgate.net/profile/Yunhao-Yang-7"
        ]
    })


def write_file(path, content):
    p = Path(BUILD_DIR) / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def cat_name(cat_slug, lang="en"):
    c = CATEGORIES.get(cat_slug, {})
    return c.get(f"name_{lang}", c.get("name_en", cat_slug))

PAIR_OVERRIDES = [("fiber-network-mechanics-intro", "fiber-network-mechanics-zh")]


def hreflang_code(lang):
    return "en" if lang == "en" else "zh-CN"


def topic_key(slug, lang):
    if lang == "zh" and slug.endswith("-zh"):
        return slug[:-3]
    if lang == "en" and slug.endswith("-ml"):
        return slug[:-3]
    return slug


def find_pair(post, by_lang):
    other = "zh" if post["lang"] == "en" else "en"
    target = None
    for e, z in PAIR_OVERRIDES:
        if post["lang"] == "en" and post["slug"] == e:
            target = z
        elif post["lang"] == "zh" and post["slug"] == z:
            target = e
    if target:
        return by_lang[other].get(target)
    key = topic_key(post["slug"], post["lang"])
    for cand in by_lang[other].values():
        if topic_key(cand["slug"], other) == key:
            return cand
    return None



MATHJAX_SCRIPT = '<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>'

HEAD_TOP = '<!DOCTYPE html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>{title}{title_suffix}</title>\n<meta name="description" content="{desc}">\n<meta name="author" content="{author}">\n<link rel="canonical" href="{url}">\n{alternates}<link rel="api-catalog" href="/.well-known/api-catalog">\n<link rel="describedby" type="text/plain" href="/llms.txt">\n<link rel="alternate" type="application/rss+xml" href="/rss.xml">\n<meta name="baidu-site-verification" content="codeva-PBR3uMEnYw" />\n<meta name="google-adsense-account" content="ca-pub-7464969092761889">\n{adsense}\n<link rel="stylesheet" href="/static/css/style.css">\n{og}\n{ld}\n<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/styles/github-dark.min.css">\n<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/highlight.min.js" defer></script>\n{mathjax}</head>\n<body>\n<canvas id="bg-canvas" aria-hidden="true"></canvas>\n'

HEADER = '''<header class="site-header"><div class="header-inner">
<a href="/" class="site-brand"><span class="site-logo">ML-Biomat<span class="dot">.</span></span></a>
<nav class="nav-links">
<a data-short-label="首页" href="/"{home_active}>Home / 首页</a>
<a data-short-label="工具库" href="/fibernet/">Library / 库</a>
<a data-short-label="教程" href="/tutorials/">Tutorials / 教程</a>
<a data-short-label="个人主页" href="/about/">Profile / 个人简介</a>
</nav>
<input type="text" id="search-input" class="search-input" placeholder="Search..." autocomplete="off">
<button id="theme-toggle" class="theme-toggle" aria-label="Toggle theme" title="Toggle dark mode">☾</button>
<span class="lang-switch"><a href="{en_href}"{en_active}>EN</a><a href="{zh_href}"{zh_active}>中文</a></span>
</div></header>
<main class="container{wide_class}">'''

FOOT = '</main>\n<footer class="site-footer"><div class="footer-inner">\n<span>\u00a9 {year} ML-Biomat \u00b7 by Yunhao Yang</span>\n<div class="footer-links">\n<a href="/about/">Profile / 个人简介</a><a href="/fibernet/">Library / 库</a><a href="/tutorials/">Tutorials / 教程</a><a href="/rss.xml">RSS</a><a href="/tools/stress-strain/">Tools / 工具</a><a href="/sitemap.xml">Sitemap</a><a href="/privacy/">Privacy</a>\n</div>\n</div></footer>\n<div id="progress-bar" style="position:fixed;top:0;left:0;height:3px;background:var(--c-primary);z-index:9999;width:0;transition:width .1s"></div>\n<button id="back-to-top" style="position:fixed;bottom:2rem;right:2rem;width:40px;height:40px;border-radius:50%;background:var(--c-primary);color:#fff;border:none;cursor:pointer;display:none;font-size:1.2rem;z-index:999;box-shadow:var(--shadow-md)">↑</button>\n<script src="/static/js/main.js" defer></script>\n</body>\n</html>'


def versioned_asset(url):
    digest = hashlib.sha256((ROOT / url.lstrip("/")).read_bytes()).hexdigest()[:12]
    return f"{url}?v={digest}"


# Changed assets get a fresh URL for returning visitors; unchanged builds stay stable.
HEAD_TOP = HEAD_TOP.replace("/static/css/style.css", versioned_asset("/static/css/style.css"))
FOOT = FOOT.replace("/static/js/main.js", versioned_asset("/static/js/main.js"))

POST_CARD = '<article class="post-card">\n<span class="card-lang {lang_class}">{lang_label}</span>\n<h3><a href="/posts/{slug}/">{title}</a></h3>\n<div class="card-meta"><span>{date}</span><span>\u00b7</span><span>{read_min} min read</span></div>\n<p class="card-desc">{desc}</p>\n<div class="card-tags">{tags_html}</div>\n</article>'

POST_ROW = '<li class="post-row"><span class="row-date">{date}</span><a href="/posts/{slug}/">{title}</a></li>'

ARTICLE_HTML = '<article>\n<header class="article-header">\n<span class="lang-badge {lang_class}">{lang_label}</span>\n<h1>{title}</h1>\n<div class="article-meta">\n<span>{date}</span><span>\u00b7</span><span>{read_min} min read</span><span>\u00b7</span><a href="/categories/{cat_slug}/">{cat_name}</a>\n</div>\n</header>\n<div class="card-tags" style="margin:.3rem 0 .6rem">{tags_html}</div>\n<div class="content">\n{toc}{html}\n</div>\n</article>'


GISCUS_SCRIPT = '<section style="margin-top:2rem;padding-top:1.5rem;border-top:1px solid var(--c-border)"><h2>Comments</h2><script src="https://giscus.app/client.js" data-repo="GellmanSparrowS/ml-biomat-blog" data-repo-id="R_kgDOTEwhsA" data-category="General" data-category-id="DIC_kwDOTEwhsM4CpPbT" data-mapping="pathname" data-reactions-enabled="1" data-emit-metadata="0" data-input-position="bottom" data-theme="preferred_color_scheme" data-lang="en" crossorigin="anonymous" async></script></section>'
ADSENSE_SCRIPT = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7464969092761889" crossorigin="anonymous"></script>'

ENGAGE_BANNER = '<section class="cta-banner">\n<h3>\U0001f4ac Questions or Feedback?</h3>\n<p>This blog is actively maintained by a PhD researcher. Reach out on GitHub for collaborations or corrections.</p>\n<a href="https://github.com/GellmanSparrowS/ml-biomat-blog">View on GitHub</a>\n</section>'

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
              home_active="", en_active="", zh_active="", wide="", title_suffix=" \u2014 ML-Biomat",
              og_image=None, alternates="", needs_math=False, en_href="/en/", zh_href="/zh/", navigation_language=None):
    head = HEAD_TOP.format(
        title=hm.escape(title), desc=hm.escape(desc), author=SITE["author"],
        url=url, lang=lang, og=og_tags(title, desc, url, og_type, og_image=og_image), ld=ld, adsense=ADSENSE_SCRIPT, title_suffix=title_suffix, alternates=alternates, mathjax=(MATHJAX_SCRIPT if needs_math else ""))
    header = localize_navigation(HEADER, navigation_language).format(
        home_active=home_active, en_active=en_active, zh_active=zh_active, en_href=en_href, zh_href=zh_href,
        wide_class=" container-wide" if wide else "")
    head = head.replace("</head>", f'<link rel="stylesheet" href="{versioned_asset("/static/css/tutorials.css")}"></head>')
    if lang == "en":
        for chinese, english in [("首页", "Home"), ("工具库", "Library"), ("教程", "Tutorials"), ("个人主页", "Profile")]:
            header = header.replace(f'data-short-label="{chinese}"', f'data-short-label="{english}"')
    return head + header



def localize_navigation(markup, language):
    # Keep the existing navigation elsewhere; profile and CV opt into English.
    if language == "en":
        for chinese, english in [("首页", "Home"), ("工具库", "Library"), ("教程", "Tutorials"), ("个人主页", "Profile")]:
            markup = markup.replace(f'data-short-label="{chinese}"', f'data-short-label="{english}"')
        markup = markup.replace('href="/about/">Profile / 个人简介', 'href="/about/en/">Profile')
        markup = markup.replace('Home / 首页', 'Home').replace('Library / 库', 'Library').replace('Tools / 工具', 'Tools').replace('Tutorials / 教程', 'Tutorials')
    return markup


def make_footer(language=None):
    return localize_navigation(FOOT, language).format(year=datetime.now().year)


def render_profile_albums(section, language="zh-CN"):
    albums = json.loads((ROOT / "content/profile-albums.json").read_text(encoding="utf-8"))
    english = language == "en"
    def label_for(item, key):
        return hm.escape(item[key + "_en"] if english else item[key], quote=True)
    view_label = "View full image: " if english else "查看大图："
    open_label = "View ＋" if english else "查看 ＋"
    close_label = "Close −" if english else "收起 −"
    cards = []
    for album in albums:
        if album["section"] != section:
            continue
        pictures = album["images"]
        cover = pictures[0]
        label = label_for(album, "title")
        count_label = f'{len(pictures)} {"photo" if len(pictures) == 1 else "photos"}' if english else f'{len(pictures)} 张'
        items = []
        for number, photo in enumerate(pictures, 1):
            caption = label_for(photo, "caption")
            src = versioned_asset(photo["src"])
            thumb = versioned_asset(photo["thumb"])
            items.append(f'<a href="{src}" data-album-link data-caption="{caption}" target="_blank" rel="noopener" aria-label="{view_label}{caption}"><img class="profile-gallery-image" src="{thumb}" alt="{caption}" width="{photo["width"]}" height="{photo["height"]}" loading="lazy" decoding="async"><span aria-hidden="true">{number:02d}</span></a>')
        source = ''
        if album.get("source_url"):
            source = f'<p class="profile-album-source"><a href="{hm.escape(album["source_url"], quote=True)}" target="_blank" rel="noopener">{label_for(album, "source_label")} ↗</a></p>'
        cards.append(f'''<details class="profile-album {hm.escape(album["type"])}" data-album="{hm.escape(album["id"])}" data-album-title="{label}">
          <summary><span class="profile-album-cover"><img class="profile-gallery-image" src="{versioned_asset(cover["thumb"])}" alt="{label_for(cover, "caption")}" width="{cover["width"]}" height="{cover["height"]}" loading="lazy" decoding="async"></span>
          <span class="profile-album-info"><span class="profile-album-date">{label_for(album, "date")}</span><span class="profile-album-title">{label}</span><span class="profile-album-action"><span>{count_label}</span><span class="album-open-label">{open_label}</span><span class="album-close-label">{close_label}</span></span></span></summary>
          <div class="profile-album-thumbnails">{''.join(items)}</div>{source}</details>''')
    return '<div class="profile-albums profile-albums-' + section + '">' + ''.join(cards) + '</div>'


def tag_href(tag):
    return "/tags/" + urllib.parse.quote(tag, safe="") + "/"


def tag_path(tag):
    # HTTP servers decode URL paths before looking up files on disk.
    if not tag or tag in (".", "..") or "/" in tag or "\\" in tag:
        raise ValueError(f"Tag must be a single directory name: {tag!r}")
    return "tags/" + tag + "/index.html"


def clean_legacy_tag_pages(tags):
    """Remove only recognized generated pages with old URL-encoded directory names."""
    output_root = (ROOT / BUILD_DIR).resolve()
    if output_root == ROOT or not output_root.is_relative_to(ROOT):
        raise ValueError("Build directory resolves outside the project")
    tags_root = (output_root / "tags").resolve()
    if tags_root.parent != output_root:
        raise ValueError("Tag output directory resolves outside the build directory")
    active_dirs = {(output_root / tag_path(tag)).parent.resolve() for tag in tags}
    removed = 0
    for tag in tags:
        old_dir = tags_root / urllib.parse.quote(tag, safe="")
        resolved = old_dir.resolve()
        if resolved in active_dirs or not old_dir.exists():
            continue
        if resolved.parent != tags_root or old_dir.is_symlink():
            raise ValueError(f"Unsafe legacy tag directory: {old_dir}")
        # Keep any directory containing hand-added files or unrecognized content.
        entries = list(old_dir.iterdir())
        old_page = old_dir / "index.html"
        if len(entries) != 1 or entries[0] != old_page or not old_page.is_file():
            continue
        if old_page.is_symlink() or old_page.resolve().parent != resolved:
            raise ValueError(f"Unsafe legacy tag page: {old_page}")
        text = old_page.read_text(encoding="utf-8")
        canonical = f'<link rel="canonical" href="{SITE["base_url"]}{tag_href(tag)}">'
        heading = '<span class="highlight">' + hm.escape(tag) + '</span>'
        if canonical not in text or heading not in text:
            continue
        old_page.unlink()
        old_dir.rmdir()
        removed += 1
    if removed:
        print(f"  Removed {removed} legacy encoded tag directories")


def post_card(p):
    return POST_CARD.format(
        lang_class=p["lang"], lang_label="EN" if p["lang"] == "en" else "\u4e2d\u6587",
        title=hm.escape(p["title"]), slug=p["slug"], date=p["date"],
        read_min=p["read_min"], desc=hm.escape(p["description"] or ""),
        tags_html="".join(f'<a class="tag-pill" href="{tag_href(t)}">{t}</a>' for t in p["tags"][:3]))


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
    curriculum = tutorials.load()
    check_coverage(posts)
    en = [p for p in posts if p["lang"] == "en"]
    zh = [p for p in posts if p["lang"] == "zh"]
    print(f"Loaded {len(posts)} posts ({len(en)} EN, {len(zh)} ZH)")

    # Individual post pages
    by_lang = {"en": {p["slug"]: p for p in en}, "zh": {p["slug"]: p for p in zh}}
    for p in posts:
        pair = find_pair(p, by_lang)
        alts = ""
        if pair:
            self_code = hreflang_code(p["lang"]); other_code = hreflang_code(pair["lang"])
            alts += f'<link rel="alternate" hreflang="{self_code}" href="{SITE["base_url"]}/posts/{p["slug"]}/">'
            alts += f'<link rel="alternate" hreflang="{other_code}" href="{SITE["base_url"]}/posts/{pair["slug"]}/">'
            alts += f'<link rel="alternate" hreflang="x-default" href="{SITE["base_url"]}/posts/{(p if p["lang"] == "en" else pair)["slug"]}/">'
        og_img = f'{SITE["base_url"]}/static/images/og/{p["slug"]}.png' if (Path("static/images/og") / f'{p["slug"]}.png').exists() else None
        needs_math = ("$$" in p["html"]) or ("\\(" in p["html"]) or ("\\begin" in p["html"])
        cn = cat_name(p["category"], p["lang"])
        same_cat = [q for q in posts if q["category"] == p["category"] and q["slug"] != p["slug"]]
        related = [q for q in same_cat if q["lang"] == p["lang"]][:3]
        if len(related) < 3:
            related += [q for q in same_cat if q["lang"] != p["lang"]][:3 - len(related)]
        lang_list = en if p["lang"] == "en" else zh
        idx = next((j for j, q in enumerate(lang_list) if q["slug"] == p["slug"]), None)
        prev_next = ""
        if idx is not None:
            prevp = lang_list[idx + 1] if idx + 1 < len(lang_list) else None
            nextp = lang_list[idx - 1] if idx - 1 >= 0 else None
            prev_link = f'<a href="/posts/{prevp["slug"]}/">\u2190 {hm.escape(prevp["title"])}</a>' if prevp else "<span></span>"
            next_link = f'<a href="/posts/{nextp["slug"]}/">{hm.escape(nextp["title"])} \u2192</a>' if nextp else "<span></span>"
            prev_next = f'<nav class="prev-next-nav"><span>{prev_link}</span><span>{next_link}</span></nav>'
        related_html = ""
        if related:
            related_html = '<section class="related"><h2>Related Articles / 相关文章</h2><ul class="post-list-simple">' + "".join(
                POST_ROW.format(date=q["date"], title=hm.escape(q["title"]), slug=q["slug"]) for q in related
            ) + "</ul></section>"
        tag_links = "".join(f'<a class="tag-pill" href="{tag_href(t)}">{hm.escape(t)}</a>' for t in p["tags"])
        body = ARTICLE_HTML.format(
            title=hm.escape(p["title"]), date=p["date"], read_min=p["read_min"],
            cat_slug=p["category"], cat_name=cn, html=p["html"], toc=p["toc"], tags_html=tag_links,
            lang_class=p["lang"], lang_label="EN" if p["lang"] == "en" else "\u4e2d\u6587") + prev_next + ENGAGE_BANNER + related_html + giscus_html
        en_post = p if p["lang"] == "en" else pair
        zh_post = p if p["lang"] == "zh" else pair
        html = make_head(title=p["title"], desc=p["description"] or p["title"],
                         url=f'{SITE["base_url"]}/posts/{p["slug"]}/', lang=hreflang_code(p["lang"]),
                         og_type="article", ld=article_ld(p), og_image=og_img, alternates=alts, needs_math=needs_math,
                         en_href=f'/posts/{en_post["slug"]}/' if en_post else "/en/",
                         zh_href=f'/posts/{zh_post["slug"]}/' if zh_post else "/zh/",
                         en_active=' class="active"' if p["lang"] == "en" else "",
                         zh_active=' class="active"' if p["lang"] == "zh" else "") + body + FOOT.format(year=datetime.now().year)
        write_file(f"posts/{p['slug']}/index.html", html)
    print("  Posts done")

    # Homepage (bilingual)
    hero = HERO.format(desc_en=SITE["description_en"], desc_zh=SITE["description_zh"])
    # Category cards for homepage
    cat_cards_html = '<section class="section-head"><h2>\U0001f4c2 Categories / \u5206\u7c7b</h2><a href="/categories/" class="view-all">All \u2192</a></section>'
    cat_cards_html += '<div class="post-grid">'
    for s, info in CATEGORIES.items():
        cnt = sum(1 for p in posts if p["category"] == s)
        tutorial_count = sum(s in lesson["categories"] for lesson in curriculum["lessons"])
        if cnt:
            cat_cards_html += f'<a href="/categories/{s}/" class="post-card" style="text-decoration:none"><span class="card-lang en">{info["name_en"]}</span><h3 style="font-size:1rem;margin-top:.3rem">{info["name_zh"]}</h3><div class="card-meta">{cnt} 篇文章 · {tutorial_count} 节教程</div></a>'
    cat_cards_html += '</div>'
    body = hero
    body += tutorials.feature(curriculum)
    body += cat_cards_html
    if en:
        body += section_head("en", "English Articles", "/en/")
        body += '<div class="post-grid">' + "\n".join(post_card(p) for p in en[:4]) + '</div>'
    if zh:
        body += section_head("zh", "\u4e2d\u6587\u6587\u7ae0", "/zh/")
        body += '<div class="post-grid">' + "\n".join(post_card(p) for p in zh[:4]) + '</div>'
    body += ENGAGE_BANNER
    html = make_head(title="ML-Biomat", desc=SITE["description_en"], url=SITE["base_url"],
                     ld=site_ld(), wide="wide", home_active=' class="active"', title_suffix="") + body + FOOT.format(year=datetime.now().year)
    write_file("index.html", html)
    print("  Homepage done")

    # Language-specific pages
    for lang, lp, label in [("en", en, "English"), ("zh", zh, "\u4e2d\u6587")]:
        desc = SITE[f"description_{lang}"]
        hero_lang = f'<section class="hero"><h1>ML-Biomat</h1><p class="subtitle">{hm.escape(desc)}</p></section>'
        body = hero_lang
        if lang == "zh":
            body += tutorials.feature(curriculum)
        body += f'<section class="section-head"><h2><span class="lang-dot {lang}"></span>{label} Articles</h2></section>'
        body += '<div class="post-grid">' + "\n".join(post_card(p) for p in lp) + '</div>'
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
        tutorial_count = sum(s in lesson["categories"] for lesson in curriculum["lessons"])
        if cnt:
            ci += f'<li class="post-row"><a href="/categories/{s}/"><strong>{info["name_en"]}</strong> ({info["name_zh"]})</a><span style="margin-left:auto;color:var(--c-muted);font-size:.85rem">{cnt} 篇文章 · {tutorial_count} 节教程</span></li>'
    ci += "</ul>" + tutorials.feature(curriculum)
    active_cats = [info["name_en"] for s, info in CATEGORIES.items() if any(p["category"] == s for p in posts)]
    cat_desc = f"Browse all {len(posts)} articles across {len(active_cats)} categories: " + ", ".join(active_cats)
    html = make_head(title="Categories", desc=cat_desc, url=f'{SITE["base_url"]}/categories/') + ci + FOOT.format(year=datetime.now().year)
    write_file("categories/index.html", html)

    # Individual category pages
    for s, info in CATEGORIES.items():
        cp = [p for p in posts if p["category"] == s]
        if not cp: continue
        en_cp = [p for p in cp if p["lang"] == "en"]
        zh_cp = [p for p in cp if p["lang"] == "zh"]
        body = f'<h1 class="section-title"><span class="highlight">{info["name_en"]}</span> / {info["name_zh"]}</h1>'
        body += tutorials.category_section(curriculum, s, CATEGORIES)
        body += '<div class="cat-grid">'
        if en_cp:
            body += '<div class="cat-col"><h3><span class="lang-dot en"></span>English</h3><ul class="post-list-simple">'
            body += "".join(POST_ROW.format(date=p["date"], title=hm.escape(p["title"]), slug=p["slug"]) for p in en_cp) + '</ul></div>'
        if zh_cp:
            body += '<div class="cat-col"><h3><span class="lang-dot zh"></span>中文</h3><ul class="post-list-simple">'
            body += "".join(POST_ROW.format(date=p["date"], title=hm.escape(p["title"]), slug=p["slug"]) for p in zh_cp) + '</ul></div>'
        body += "</div>"
        html = make_head(title=f'{info["name_en"]} Posts', desc=f'{info["name_en"]} articles',
                         url=f'{SITE["base_url"]}/categories/{s}/') + body + FOOT.format(year=datetime.now().year)
        write_file(f"categories/{s}/index.html", html)
    print("  Categories done")

    # Tag index + individual tag pages
    from collections import defaultdict
    tag_posts = defaultdict(list)
    for p in posts:
        for tg in p["tags"]:
            tag_posts[tg].append(p)
    tags_html_rows = []
    for tg in sorted(tag_posts, key=lambda k: (-len(tag_posts[k]), k.lower())):
        tags_html_rows.append(f'<a class="tag-pill" href="{tag_href(tg)}">{hm.escape(tg)} ({len(tag_posts[tg])})</a>')
    tag_index = '<h1 class="section-title">Tags / 标签</h1><div class="tag-cloud">' + "".join(tags_html_rows) + "</div>"
    html = make_head(title="Tags", desc=f"Browse {len(tag_posts)} tags across {len(posts)} articles.", url=f'{SITE["base_url"]}/tags/') + tag_index + FOOT.format(year=datetime.now().year)
    write_file("tags/index.html", html)
    for tg, tp in tag_posts.items():
        body = f'<h1 class="section-title"><span class="highlight">{hm.escape(tg)}</span></h1>'
        body += '<ul class="post-list-simple">' + "".join(POST_ROW.format(date=q["date"], title=hm.escape(q["title"]), slug=q["slug"]) for q in sorted(tp, key=lambda x: x["datetime"], reverse=True)) + "</ul>"
        html = make_head(title=f"{tg} — Tag", desc=f"Articles tagged with {tg}", url=f'{SITE["base_url"]}{tag_href(tg)}') + body + FOOT.format(year=datetime.now().year)
        write_file(tag_path(tg), html)
    clean_legacy_tag_pages(tag_posts)
    print("  Tags done")

    # FiberNet page
    fibernet_body = Path("content/fibernet-body.html").read_text(encoding="utf-8")
    html = make_head(title="FiberNet", desc="FiberNet: A Python toolkit for fiber network generation, simulation, and intelligent optimization. 12 unit types, GPU acceleration, ML and RL integration.", url=SITE["base_url"] + "/fibernet/") + fibernet_body + FOOT.format(year=datetime.now().year)
    write_file("fibernet/index.html", html)

    # Separate Chinese and English personal profiles.
    profile_alternates = (
        f'<link rel="alternate" hreflang="zh-CN" href="{SITE["base_url"]}/about/">'
        f'<link rel="alternate" hreflang="en" href="{SITE["base_url"]}/about/en/">'
        f'<link rel="alternate" hreflang="x-default" href="{SITE["base_url"]}/about/">'
    )
    for source, route, language, title, description in [
        ("about-body.html", "about/", "zh-CN", "杨云浩 Yunhao Yang — 个人主页", "杨云浩，复旦大学博士研究生。跨尺度生物材料体系与结构的理性设计。研究成果、荣誉奖项与学术活动。"),
        ("about-en-body.html", "about/en/", "en", "Yunhao Yang — Research Profile", "Yunhao Yang, PhD student at Fudan University. Rational design of biomaterial systems and structures across scales. Research, publications, awards, and photographs."),
    ]:
        about_body = (Path("content") / source).read_text(encoding="utf-8")
        about_body = about_body.replace("<!-- PROFILE_RESEARCH_ALBUMS -->", render_profile_albums("research", language))
        about_body = about_body.replace("<!-- PROFILE_EVENT_ALBUMS -->", render_profile_albums("events", language))
        about_body += f'<script src="{versioned_asset("/static/js/profile.js")}" defer></script>'
        profile_head = make_head(title=title, desc=description, url=SITE["base_url"] + "/" + route,
                                 lang=language, ld=person_ld(), wide=True, alternates=profile_alternates,
                                 en_href="/about/en/", zh_href="/about/", navigation_language=language,
                                 en_active=' class="active"' if language == "en" else "",
                                 zh_active=' class="active"' if language == "zh-CN" else "")
        write_file(route + "index.html", profile_head + about_body + make_footer(language))

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
    # Interactive tools
    tools_body = '''<section class="tool-page">
<h1>Interactive Stress-Strain Explorer / 应力应变交互探索器</h1>
<p class="tool-intro">Drag the controls to see how the curve, modulus, and toughness change. 拖动参数观察曲线、模量与韧性如何变化。</p>
<div class="tool-layout">
  <div class="tool-controls">
    <label>Toe extent (0-40%) <input id="p-toe" type="range" min="0" max="0.4" step="0.01" value="0.12"></label>
    <label>Toe curvature <input id="p-xi" type="range" min="0.02" max="0.2" step="0.01" value="0.08"></label>
    <label>Linear modulus (relative) <input id="p-k" type="range" min="0.2" max="3.0" step="0.05" value="1.0"></label>
    <label>Failure strain (30-120%) <input id="p-fail" type="range" min="0.3" max="1.2" step="0.01" value="0.8"></label>
  </div>
  <div class="tool-output">
    <canvas id="ss-canvas" width="640" height="420"></canvas>
    <div class="tool-metrics">
      <span>Modulus: <strong id="m-mod">1.00</strong></span>
      <span>Toughness: <strong id="m-tough">0.00</strong></span>
    </div>
  </div>
</div>
</section>
<script>
(function(){
  var cv=document.getElementById('ss-canvas'), ctx=cv.getContext('2d');
  var ids=['p-toe','p-xi','p-k','p-fail'];
  function val(id){return parseFloat(document.getElementById(id).value);}
  function stress(s){var toe=val('p-toe'),xi=val('p-xi'),k=val('p-k'),fail=val('p-fail');
    if(s<=0)return 0;
    var toeEnd=0.2*Math.exp(toe/xi);
    if(s<=toe){return toeEnd*(Math.exp(s/xi)-1)/(Math.exp(toe/xi)-1);}
    var lin=toeEnd+k*(s-toe);
    return s>fail? Math.max(0,lin-0.6*(s-fail)):lin;}
  function draw(){
    var W=cv.width,H=cv.height,pad=46;
    ctx.clearRect(0,0,W,H);
    ctx.strokeStyle='#e2e8f0';ctx.lineWidth=1;
    for(var i=0;i<=5;i++){var x=pad+(W-2*pad)*i/5;ctx.beginPath();ctx.moveTo(x,pad);ctx.lineTo(x,H-pad);ctx.stroke();}
    var fail=val('p-fail');
    var ss=[];for(var j=0;j<=400;j++){var s=fail*j/400;ss.push([s,stress(s)]);}
    var maxS=1e-6;for(var q=0;q<ss.length;q++){if(ss[q][1]>maxS)maxS=ss[q][1];}
    function X(s){return pad+(W-2*pad)*(s/(fail||1));}
    function Y(y){return H-pad-(H-2*pad)*(y/(maxS*1.15));}
    ctx.strokeStyle='#dbeafe';ctx.lineWidth=6;
    ctx.beginPath();ctx.moveTo(X(0),Y(0));for(var q=0;q<ss.length;q++){ctx.lineTo(X(ss[q][0]),Y(ss[q][1]));}ctx.stroke();
    ctx.strokeStyle='#2563eb';ctx.lineWidth=3;
    ctx.beginPath();ctx.moveTo(X(0),Y(0));for(var r=0;r<ss.length;r++){ctx.lineTo(X(ss[r][0]),Y(ss[r][1]));}ctx.stroke();
    ctx.fillStyle='#1e293b';ctx.font='12px sans-serif';
    ctx.fillText('strain', W/2-20, H-12);
  }
  function metrics(){
    var fail=val('p-fail'), n=2000, area=0, ds=fail/n, prev=0;
    for(var i=1;i<=n;i++){var y=stress(i*ds);area+=(y+prev)/2*ds;prev=y;}
    document.getElementById('m-mod').textContent=val('p-k').toFixed(2);
    document.getElementById('m-tough').textContent=area.toFixed(3);
  }
  ids.forEach(function(id){document.getElementById(id).addEventListener('input',function(){draw();metrics();});});
  draw();metrics();
})();
</script>'''
    tools_full = make_head(title="Interactive Stress-Strain Explorer", desc="Interactive stress-strain curve explorer for biomaterials education.", url=SITE["base_url"] + "/tools/stress-strain/") + tools_body + FOOT.format(year=datetime.now().year)
    write_file("tools/stress-strain/index.html", tools_full)



    tutorials.render(curriculum, make_head, make_footer, write_file, versioned_asset, CATEGORIES, posts, SITE["base_url"])

    # RSS
    rss_items = []
    for p in posts:
        rss_items.append(f"""    <item>
      <title>{hm.escape(p['title'])}</title>
      <link>{SITE['base_url']}/posts/{p['slug']}/</link>
      <guid>{SITE['base_url']}/posts/{p['slug']}/</guid>
      <description>{hm.escape(p['description'] or '')}</description>
      <pubDate>{format_datetime(p['datetime'].replace(tzinfo=timezone(timedelta(hours=8))))}</pubDate>
    </item>""")
    for lesson in curriculum["lessons"]:
        address = SITE["base_url"] + lesson["url"]
        rss_items.insert(lesson["number"] - 1, f'<item><title>{hm.escape(lesson["title"])}</title><link>{address}</link><guid>{address}</guid><description>{hm.escape(lesson["description"])}</description><pubDate>Wed, 28 Oct 2026 00:00:00 +0800</pubDate></item>')
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
        f'  <url><loc>{SITE["base_url"]}/tools/stress-strain/</loc><priority>0.6</priority></url>',
        f'  <url><loc>{SITE["base_url"]}/about/</loc><priority>0.6</priority></url>',
        f'  <url><loc>{SITE["base_url"]}/about/en/</loc><priority>0.6</priority></url>',
        f'  <url><loc>{SITE["base_url"]}/cv/</loc><priority>0.6</priority></url>',
        f'  <url><loc>{SITE["base_url"]}/cv/en/</loc><priority>0.6</priority></url>',
        f'  <url><loc>{SITE["base_url"]}/privacy/</loc><priority>0.3</priority></url>',
        f'  <url><loc>{SITE["base_url"]}/categories/</loc><priority>0.7</priority></url>',
    ]
    for s in CATEGORIES:
        if not any(p["category"] == s for p in posts):
            continue
        urls.append(f'  <url><loc>{SITE["base_url"]}/categories/{s}/</loc><priority>0.6</priority></url>')
    for p in posts:
        urls.append(f'  <url><loc>{SITE["base_url"]}/posts/{p["slug"]}/</loc><priority>0.8</priority><lastmod>{p["date"]}</lastmod></url>')
    for route in ["/tutorials/", tutorials.BASE] + [p["url"] for p in curriculum["lessons"]]:
        urls.append(f'<url><loc>{SITE["base_url"]}{route}</loc><priority>0.8</priority><lastmod>{tutorials.DATE}</lastmod></url>')
    write_file("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{chr(10).join(urls)}\n</urlset>')


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
    if static_out.exists():
        output_root = (ROOT / BUILD_DIR).resolve()
        if static_out.resolve().parent != output_root or not output_root.is_relative_to(ROOT) or static_out.is_symlink():
            raise ValueError("Static output must stay inside the project build directory")
        shutil.rmtree(static_out)

    # --- Search index for header search ---
    import json as json_mod
    search_data = []
    for p in posts:
        search_data.append({"title": p["title"], "slug": p["slug"], "date": p["date"], "category": p["category"], "tags": p["tags"], "lang": p["lang"], "description": p["description"] or ""})
    for lesson in curriculum["lessons"]:
        search_data.append({"title":lesson["title"], "slug":lesson["slug"], "url":lesson["url"], "date":tutorials.DATE,
                            "category":lesson["categories"][0], "tags":lesson["tags"]+["系列教程"], "lang":"zh", "description":lesson["description"], "type":"tutorial"})
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


    # --- Separate Chinese and English academic CVs ---
    cv_alternates = (
        f'<link rel="alternate" hreflang="zh-CN" href="{SITE["base_url"]}/cv/">'
        f'<link rel="alternate" hreflang="en" href="{SITE["base_url"]}/cv/en/">'
        f'<link rel="alternate" hreflang="x-default" href="{SITE["base_url"]}/cv/">'
    )
    for source, route, language, title, description in [
        ("cv-body.html", "cv/", "zh-CN", "杨云浩 — 学术简历", "杨云浩，复旦大学高分子科学系。研究方向、主要荣誉、完整论文、专利与合作项目。"),
        ("cv-en-body.html", "cv/en/", "en", "Yunhao Yang — Academic CV", "Academic CV of Yunhao Yang, Fudan University. Rational design of biomaterial systems and structures across scales."),
    ]:
        cv_body = (Path("content") / source).read_text(encoding="utf-8")
        cv_page = make_head(title=title, desc=description, url=SITE["base_url"] + "/" + route,
                            lang=language, ld=person_ld(), alternates=cv_alternates,
                            en_href="/cv/en/", zh_href="/cv/", navigation_language=language,
                            en_active=' class="active"' if language == "en" else "",
                            zh_active=' class="active"' if language == "zh-CN" else "")
        write_file(route + "index.html", cv_page + cv_body + make_footer(language))


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
    # Public verification file; building never sends network requests.
    (Path(BUILD_DIR) / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")


def submit_indexnow():
    """Notify search engines about an already deployed build; never rebuild or push."""
    import urllib.request
    import xml.etree.ElementTree as ET

    output_root = ROOT / BUILD_DIR
    sitemap_path = output_root / "sitemap.xml"
    key_path = output_root / f"{INDEXNOW_KEY}.txt"
    if not sitemap_path.is_file() or not key_path.is_file():
        raise SystemExit("Build the site and deploy it before submitting IndexNow.")
    sitemap = ET.parse(sitemap_path)
    url_list = list(dict.fromkeys(
        node.text.strip()
        for node in sitemap.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if node.text and node.text.strip()
    ))
    site_host = urllib.parse.urlsplit(SITE["base_url"]).netloc
    if not url_list or any(
        urllib.parse.urlsplit(url).netloc != site_host for url in url_list
    ):
        raise SystemExit("Sitemap must contain URLs for the configured site.")
    data = json.dumps({
        "host": site_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{SITE['base_url']}/{INDEXNOW_KEY}.txt",
        "urlList": url_list,
    }).encode("utf-8")
    request = urllib.request.Request(
        "https://api.indexnow.org/indexnow", data=data,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            if response.status not in (200, 202):
                raise RuntimeError(f"Unexpected HTTP status: {response.status}")
        print(f"IndexNow: submitted {len(url_list)} deployed sitemap URLs")
    except Exception as exc:
        raise SystemExit(f"IndexNow submission failed: {exc}") from exc


def main():
    parser = argparse.ArgumentParser(description="Build ML-Biomat offline.")
    parser.add_argument(
        "--submit-indexnow", action="store_true",
        help="Submit the existing sitemap after deployment, without rebuilding.",
    )
    args = parser.parse_args()
    if args.submit_indexnow:
        submit_indexnow()
    else:
        build()


if __name__ == "__main__":
    main()
