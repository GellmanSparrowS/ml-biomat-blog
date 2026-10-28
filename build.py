# -*- coding: utf-8 -*-
"""Static blog generator — outputs to docs/ for GitHub Pages. Bilingual EN+ZH."""
import argparse, hashlib, os, re, json, shutil, html as hm, urllib.parse
from datetime import datetime, timezone, timedelta
from email.utils import format_datetime
from pathlib import Path
from config import SITE, CATEGORIES, BUILD_DIR, CONTENT_DIR
from content_tools import tutorials, catalog, chrome, home, utility_pages, tag_pages

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
        m = re.match(r'^!\[(.*)\]\(([^)]+)\)$', line.strip())
        if m: out.append(f'<img src="{hm.escape(m.group(2), quote=True)}" alt="{hm.escape(m.group(1), quote=True)}" loading="lazy">'); i += 1; continue
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
                reading_text = re.sub(r'```.*?```', '', body, flags=re.S)
                chinese = len(re.findall(r'[\u4e00-\u9fff]', reading_text))
                words = len(re.findall(r"[A-Za-z0-9]+(?:[’'-][A-Za-z0-9]+)*", reading_text))
                wc = chinese + words; read_min = max(1, round(chinese / 400 + words / 200))
                posts.append({
                    "title": meta.get("title", slug.replace("-", " ").title()),
                    "slug": slug, "date": posted.strftime("%Y-%m-%d"), "modified": meta.get("updated", posted.strftime("%Y-%m-%d")),
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
        "datePublished": post["date"], "dateModified": post.get("modified",post["date"]),
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
            {"@type": "ListItem", "position": 1, "name": "Home" if post["lang"] == "en" else "首页", "item": SITE["base_url"] + ("/en/" if post["lang"] == "en" else "/")},
            {"@type": "ListItem", "position": 2, "name": cat_name(post["category"], post["lang"]),
             "item": SITE["base_url"] + catalog.category_url(post["category"],post["lang"])},
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

HEAD_TOP = '<!DOCTYPE html>\n<html lang="{lang}" data-theme="dark">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>{title}{title_suffix}</title>\n<meta name="description" content="{desc}">\n<meta name="author" content="{author}">\n<link rel="canonical" href="{url}">\n{alternates}<link rel="api-catalog" href="/.well-known/api-catalog">\n<link rel="describedby" type="text/plain" href="/llms.txt">\n<link rel="alternate" type="application/rss+xml" href="/rss.xml">\n<meta name="baidu-site-verification" content="codeva-PBR3uMEnYw" />\n<meta name="google-adsense-account" content="ca-pub-7464969092761889">\n{adsense}\n<link rel="stylesheet" href="/static/css/style.css">\n{og}\n{ld}\n<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/styles/github-dark.min.css">\n<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/highlight.min.js" defer></script>\n{mathjax}</head>\n<body>\n<canvas id="bg-canvas" aria-hidden="true"></canvas>\n'

# Shared headers are rendered by content_tools.chrome.

FOOT = '</main>\n<footer class="site-footer"><div class="footer-inner">\n<span>\u00a9 {year} ML-Biomat \u00b7 by Yunhao Yang</span>\n<div class="footer-links">\n<a href="/about/">Profile / 个人简介</a><a href="/fibernet/">Library / 库</a><a href="/categories/">Categories / 分类</a><a href="/rss.xml">RSS</a><a href="/tools/stress-strain/">Tools / 工具</a><a href="/sitemap.xml">Sitemap</a><a href="/privacy/">Privacy</a>\n</div>\n</div></footer>\n<div id="progress-bar" style="position:fixed;top:0;left:0;height:3px;background:var(--c-primary);z-index:9999;width:0;transition:width .1s"></div>\n<button id="back-to-top" style="position:fixed;bottom:2rem;right:2rem;width:40px;height:40px;border-radius:50%;background:var(--c-primary);color:#fff;border:none;cursor:pointer;display:none;font-size:1.2rem;z-index:999;box-shadow:var(--shadow-md)">↑</button>\n<script src="/static/js/main.js" defer></script>\n</body>\n</html>'


def versioned_asset(url):
    digest = hashlib.sha256((ROOT / url.lstrip("/")).read_bytes()).hexdigest()[:12]
    return f"{url}?v={digest}"


# Changed assets get a fresh URL for returning visitors; unchanged builds stay stable.
HEAD_TOP = HEAD_TOP.replace("/static/css/style.css", versioned_asset("/static/css/style.css"))
FOOT = FOOT.replace("/static/js/main.js", versioned_asset("/static/js/main.js"))

POST_CARD = '<article class="post-card">\n<span class="card-lang {lang_class}">{lang_label}</span>\n<h3><a href="/posts/{slug}/">{title}</a></h3>\n<div class="card-meta"><span>{date}</span><span>\u00b7</span><span>{read_min} min read</span></div>\n<p class="card-desc">{desc}</p>\n<div class="card-tags">{tags_html}</div>\n</article>'

POST_ROW = '<li class="post-row"><span class="row-date">{date}</span><a href="/posts/{slug}/">{title}</a></li>'

ARTICLE_HTML = '<article><nav class="article-breadcrumb" aria-label="{breadcrumb_label}"><a href="{categories_url}">{categories_label}</a><span aria-hidden="true">/</span><a href="{cat_url}">{cat_name}</a></nav>\n<header class="article-header">\n<span class="lang-badge {lang_class}">{lang_label}</span>\n<h1>{title}</h1>\n<div class="article-meta">\n<span>{date}</span><span>\u00b7</span><span>{read_min} min read</span><span>\u00b7</span><a href="{cat_url}">{cat_name}</a>\n</div>\n</header>\n<div class="card-tags" style="margin:.3rem 0 .6rem">{tags_html}</div>\n<div class="content">\n{toc}{html}\n</div>\n</article>'


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


def make_head(title, desc, url, lang="zh-CN", og_type="website", ld="",
              home_active="", en_active="", zh_active="", wide="", title_suffix=" — ML-Biomat",
              og_image=None, alternates="", needs_math=False, en_href=None, zh_href=None, navigation_language=None):
    language = 'en' if lang == 'en' else 'zh-CN'
    head = HEAD_TOP.format(
        title=hm.escape(title), desc=hm.escape(desc), author=SITE["author"],
        url=url, lang=language, og=og_tags(title, desc, url, og_type, og_image=og_image), ld=ld,
        adsense=ADSENSE_SCRIPT, title_suffix=title_suffix, alternates=alternates,
        mathjax=(MATHJAX_SCRIPT if needs_math else ""))
    head = head.replace('<meta charset="utf-8">','<meta charset="utf-8">'+chrome.THEME_INIT)
    head = head.replace("</head>", f'<link rel="stylesheet" href="{versioned_asset("/static/css/tutorials.css")}"></head>')
    route = urllib.parse.urlsplit(url).path or '/'
    return head + chrome.header(language, route, en_href, zh_href, bool(wide))


def make_footer(language='zh-CN'):
    footer=FOOT.format(year=datetime.now().year)
    footer=re.sub(r'<div class="footer-links">.*?</div>',chrome.footer_links(language),footer,flags=re.S)
    footer=footer.replace('id="back-to-top"', 'id="back-to-top" aria-label="'+('Back to top' if language=='en' else '返回顶部')+'"')
    return footer


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


def tag_href(tag, language="zh"):
    return tag_pages.href(tag, language)


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
        tags_html="".join(f'<a class="tag-pill" href="{tag_href(t,p["lang"])}">{t}</a>' for t in p["tags"][:3]))


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

    by_lang = {'en': en_posts, 'zh': zh_posts}
    for post in posts:
        pair = find_pair(post, by_lang)
        if not pair or find_pair(pair, by_lang)['slug'] != post['slug']:
            raise ValueError('Missing reciprocal translation: '+post['slug'])

def build():
    # Load Giscus HTML for article pages
    giscus_html = Path("static/giscus.html").read_text(encoding="utf-8") if Path("static/giscus.html").exists() else ""
    giscus_html = giscus_html.replace('data-theme="preferred_color_scheme"', 'data-theme="dark"')

    posts = load_posts()
    curriculum = tutorials.load()
    catalog_items = catalog.entries(posts, curriculum)
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
            related_html = '<section class="related"><h2>' + ("Related articles" if p["lang"]=="en" else "相关阅读") + '</h2><ul class="post-list-simple">' + "".join(
                POST_ROW.format(date=q["date"], title=hm.escape(q["title"]), slug=q["slug"]) for q in related
            ) + "</ul></section>"
        tag_links = "".join(f'<a class="tag-pill" href="{tag_href(t,p["lang"])}">{hm.escape(t)}</a>' for t in p["tags"])
        body = ARTICLE_HTML.format(
            title=hm.escape(p["title"]), date=p["date"], read_min=p["read_min"],
            cat_url=catalog.category_url(p["category"], p["lang"]), cat_name=cn,
            breadcrumb_label="Breadcrumb" if p["lang"]=="en" else "当前位置", categories_url=catalog.category_url(lang=p["lang"]), categories_label="Categories" if p["lang"]=="en" else "分类", html=p["html"], toc=p["toc"].replace("Contents / 目录", "Contents" if p["lang"] == "en" else "目录"), tags_html=tag_links,
            lang_class=p["lang"], lang_label="EN" if p["lang"] == "en" else "\u4e2d\u6587") + prev_next + related_html + (giscus_html if p["lang"]=="en" else giscus_html.replace("<h2>Comments</h2>", "<h2>讨论</h2>").replace('data-lang="en"', 'data-lang="zh-CN"'))
        if p["lang"] == "zh":
            body = body.replace(f'{p["read_min"]} min read', f'{p["read_min"]} 分钟阅读')
        en_post = p if p["lang"] == "en" else pair
        zh_post = p if p["lang"] == "zh" else pair
        html = make_head(title=p["title"], desc=p["description"] or p["title"],
                         url=f'{SITE["base_url"]}/posts/{p["slug"]}/', lang=hreflang_code(p["lang"]),
                         og_type="article", ld=article_ld(p), og_image=og_img, alternates=alts, needs_math=needs_math,
                         en_href=f'/posts/{en_post["slug"]}/' if en_post else "/en/",
                         zh_href=f'/posts/{zh_post["slug"]}/' if zh_post else "/zh/",
                         en_active=' class="active"' if p["lang"] == "en" else "",
                         zh_active=' class="active"' if p["lang"] == "zh" else "", navigation_language=p["lang"]) + body + make_footer(p["lang"])
        write_file(f"posts/{p['slug']}/index.html", html)
    print("  Posts done")

    home_routes = home.render(catalog_items, CATEGORIES, SITE, make_head, make_footer, write_file, site_ld)
    print("  Paired home pages and separate article collections done")

    category_routes = catalog.render(catalog_items, CATEGORIES, make_head, make_footer, write_file, SITE['base_url'])
    print("  Categories done")

    tag_routes = tag_pages.render(posts, make_head, make_footer, write_file, SITE['base_url'])
    clean_legacy_tag_pages({tag for post in posts for tag in post['tags']})
    print("  Localized tag pages done")

    # FiberNet shares the same Chinese/English page contract as profiles and articles.
    for language, source, route in [('zh-CN','fibernet-body.html','/fibernet/'),('en','fibernet-en-body.html','/fibernet/en/')]:
        body = (Path('content')/source).read_text(encoding='utf-8')
        desc='纤维网络生成、建模与分析的 Python 工具包。安装、示例与项目资源。' if language=='zh-CN' else 'A Python toolkit for fiber network generation, modeling and analysis. Installation, examples and project resources.'
        alts=f'<link rel="alternate" hreflang="zh-CN" href="{SITE["base_url"]}/fibernet/"><link rel="alternate" hreflang="en" href="{SITE["base_url"]}/fibernet/en/">'
        document=make_head(title='FiberNet',desc=desc,url=SITE['base_url']+route,lang=language,wide=True,en_href='/fibernet/en/',zh_href='/fibernet/',alternates=alts)+body+make_footer(language)
        document=document.replace('</head>', f'<link rel="stylesheet" href="{versioned_asset("/static/css/fibernet.css")}"></head>')
        write_file(route.lstrip('/')+'index.html',document)

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

    utility_routes = utility_pages.render(make_head, make_footer, write_file, SITE['base_url'], versioned_asset)

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
    for route in category_routes + [p for p in home_routes if p not in ('/','/en/')] + ['/fibernet/en/'] + tag_routes + [p for p in utility_routes if p not in ('/privacy/','/tools/stress-strain/')]:
        if route == '/categories/': continue
        urls.append(f'<url><loc>{SITE["base_url"]}{route}</loc><priority>0.7</priority></url>')
    for p in posts:
        urls.append(f'  <url><loc>{SITE["base_url"]}/posts/{p["slug"]}/</loc><priority>0.8</priority><lastmod>{p["modified"]}</lastmod></url>')
    for route in [p["url"] for p in curriculum["lessons"]]:
        urls.append(f'<url><loc>{SITE["base_url"]}{route}</loc><priority>0.8</priority><lastmod>{tutorials.DATE}</lastmod></url>')
    write_file("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{chr(10).join(urls)}\n</urlset>')


    # ads.txt for Google AdSense
    write_file("ads.txt", "google.com, pub-7464969092761889, DIRECT, f08c47fec0942fa0")

# Robots.txt
    write_file("robots.txt", f"User-agent: *\nContent-Signal: ai-train=yes, search=yes, ai-input=yes\nAllow: /\nSitemap: {SITE['base_url']}/sitemap.xml\n")

    # 404
    not_found = make_head(title="页面未找到", desc="页面未找到", url=f'{SITE["base_url"]}/404.html')
    not_found += '<h1 style="font-size:3rem;margin-top:3rem">404</h1><p>页面未找到。<a href="/">返回首页</a></p>' + make_footer()
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
                            "category":lesson["categories"][0], "tags":lesson["tags"], "lang":"zh", "description":lesson["description"], "type":"tutorial"})
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
