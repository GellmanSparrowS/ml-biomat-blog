# -*- coding: utf-8 -*-
"""
Static blog generator for ml-biomat.com
Reads Markdown posts from content/, generates SEO-optimized HTML in output/.
"""
import os, re, json, shutil, html as html_mod
from datetime import datetime
from pathlib import Path
from config import SITE, CATEGORIES, BUILD_DIR, CONTENT_DIR

SCRIPTS_DIR = Path(os.getcwd()) if os.getcwd().endswith("ml-biomat-blog") else Path(__file__).parent
os.chdir(str(SCRIPTS_DIR))


def parse_frontmatter(text):
    """Extract YAML-ish frontmatter from Markdown. Returns (meta dict, body)."""
    meta = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().split("\n"):
                line = line.strip()
                if ":" in line:
                    key, val = line.split(":", 1)
                    key, val = key.strip(), val.strip()
                    val = val.strip('"').strip("'")
                    if val.startswith("[") and val.endswith("]"):
                        val = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",") if v.strip()]
                    meta[key] = val
            body = parts[2].strip()
    return meta, body


def md_to_html(text):
    """Simple Markdown-to-HTML converter. Handles headings, code, lists, links, bold, italic."""
    lines = text.split("\n")
    out = []
    in_code = False
    in_list = False
    list_tag = ""
    i = 0
    while i < len(lines):
        line = lines[i]
        # Fenced code blocks
        if line.strip().startswith("```"):
            if not in_code:
                lang = line.strip()[3:].strip()
                out.append(f'<pre><code class="language-{lang}">' if lang else "<pre><code>")
                in_code = True
            else:
                out.append("</code></pre>")
                in_code = False
            i += 1
            continue
        if in_code:
            out.append(html_mod.escape(line))
            i += 1
            continue
        # Close list if needed
        if in_list and not re.match(r'^(\d+\.\s|[-*]\s)', line.strip()):
            out.append(f"</{list_tag}>")
            in_list = False
        # Headings
        m = re.match(r'^(#{1,6})\s+(.+)$', line)
        if m:
            level = len(m.group(1))
            txt = inline_md(m.group(2))
            out.append(f"<h{level}>{txt}</h{level}>")
            i += 1
            continue
        # Unordered list
        m = re.match(r'^[-*]\s+(.+)$', line)
        if m:
            if not in_list:
                out.append("<ul>")
                in_list = True
                list_tag = "ul"
            out.append(f"<li>{inline_md(m.group(1))}</li>")
            i += 1
            continue
        # Ordered list
        m = re.match(r'^\d+\.\s+(.+)$', line)
        if m:
            if not in_list:
                out.append("<ol>")
                in_list = True
                list_tag = "ol"
            out.append(f"<li>{inline_md(m.group(1))}</li>")
            i += 1
            continue
        # Horizontal rule
        if re.match(r'^[-*_]{3,}$', line.strip()):
            out.append("<hr>")
            i += 1
            continue
        # Blockquote
        if line.startswith(">"):
            qt_lines = []
            while i < len(lines) and lines[i].startswith(">"):
                qt_lines.append(lines[i][1:].strip() if lines[i][1:2] == " " else lines[i][1:].strip())
                i += 1
            out.append(f"<blockquote>{'<br>'.join(inline_md(l) for l in qt_lines)}</blockquote>")
            continue
        # Table (simple: | col | col |)
        if "|" in line and line.strip().startswith("|"):
            table_lines = []
            while i < len(lines) and "|" in lines[i]:
                table_lines.append(lines[i])
                i += 1
            out.append(_table_to_html(table_lines))
            continue
        # Image
        m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', line.strip())
        if m:
            out.append(f'<img src="{m.group(2)}" alt="{m.group(1)}" loading="lazy">')
            i += 1
            continue
        # Empty line
        if not line.strip():
            out.append("")
            i += 1
            continue
        # Paragraph
        out.append(f"<p>{inline_md(line)}</p>")
        i += 1
    if in_list:
        out.append(f"</{list_tag}>")
    if in_code:
        out.append("</code></pre>")
    return "\n".join(out)


def _table_to_html(lines):
    rows = []
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        cells = [inline_md(c) for c in cells]
        tag = "th" if i == 0 else "td"
        rows.append("<tr>" + "".join(f"<{tag}>{c}</{tag}>" for c in cells) + "</tr>")
        if i == 0 and len(lines) > 1 and re.match(r'^[\s|:\-]+$', lines[1].strip()):
            continue  # skip separator row; handled by the loop
    # Remove separator row if present
    if len(rows) > 1:
        # Check second line of original for separator pattern
        pass
    return f"<table>{''.join(rows)}</table>"


def inline_md(text):
    """Convert inline Markdown: bold, italic, code, links, images."""
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    t = re.sub(r'__(.+?)__', r'<strong>\1</strong>', t)
    t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
    t = re.sub(r'_(.+?)_', r'<em>\1</em>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    return t


def load_posts():
    """Load all posts from content/posts/"""
    posts = []
    posts_dir = Path(CONTENT_DIR) / "posts"
    for root, dirs, files in os.walk(posts_dir):
        for f in sorted(files, reverse=True):
            if f.endswith(".md"):
                path = Path(root) / f
                rel = path.relative_to(posts_dir)
                text = path.read_text(encoding="utf-8")
                meta, body = parse_frontmatter(text)
                slug = meta.get("slug", path.stem)
                date_str = meta.get("date", "2025-01-01")
                try:
                    posted = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    posted = datetime(2025, 1, 1)
                posts.append({
                    "title": meta.get("title", slug.replace("-", " ").title()),
                    "slug": slug,
                    "date": posted.strftime("%Y-%m-%d"),
                    "datetime": posted,
                    "category": meta.get("category", "uncategorized"),
                    "tags": meta.get("tags", []),
                    "lang": meta.get("lang", "en"),
                    "description": meta.get("description", ""),
                    "body": body,
                    "html": md_to_html(body),
                })
    posts.sort(key=lambda p: p["datetime"], reverse=True)
    return posts


# ---- HTML Templates ----

HEAD = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — {site_title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="{author}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="{site_title}">
<link rel="canonical" href="{url}">
<link rel="alternate" type="application/rss+xml" title="{site_title} RSS" href="/rss.xml">
<link rel="stylesheet" href="/static/css/style.css">
<script type="application/ld+json">{structured_data}</script>
{extra_head}
</head>
<body>
<header><div class="container">
<a href="/" class="site-title">{site_title}</a>
<nav>
<a href="/">Home</a>
<a href="/categories/">Categories</a>
<a href="/about/">About</a>
</nav>
</div></header>
<main class="container">"""

FOOT = """</main>
<footer><div class="container">
&copy; {year} {site_title}. Built with care.
· <a href="/rss.xml">RSS</a>
· <a href="/sitemap.xml">Sitemap</a>
</div></footer>
</body>
</html>"""

POST_TEMPLATE = """<article>
<header class="post-header">
<h1>{title}</h1>
<div class="post-date">{date}</div>
<div class="post-tags">
<a href="/categories/{cat_slug}/" class="post-category">{cat_name}</a>
{tags_html}
</div>
</header>
<div class="content">
{html}
</div>
</article>"""

INDEX_POST = """<li class="post-item">
<h2 class="post-title"><a href="/posts/{slug}/">{title}</a></h2>
<div class="post-meta">{date} · <a href="/categories/{cat_slug}/" class="post-category">{cat_name}</a></div>
<p class="post-desc">{desc}</p>
</li>"""

CAT_TAG_PAGE = """<section class="post-list-section">
<h1 class="section-title">Posts in <span>{name}</span></h1>
<ul class="post-list">
{items}
</ul>
</section>"""

PAGINATION = """<nav class="pagination">
{prev_link}{next_link}
</nav>"""


def render_page(title, desc, body, lang="en", url="", og_type="website", structured_data="{}", extra_head=""):
    h = HEAD.format(
        title=html_mod.escape(title),
        site_title=SITE["title"],
        desc=html_mod.escape(desc or SITE["description"]),
        author=SITE["author"],
        og_type=og_type,
        url=url or SITE["base_url"],
        lang=lang,
        structured_data=structured_data,
        extra_head=extra_head,
    )
    f = FOOT.format(year=datetime.now().year, site_title=SITE["title"])
    return h + body + f


def structured_article(post):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "description": post["description"],
        "datePublished": post["date"],
        "author": {"@type": "Person", "name": SITE["author"]},
        "url": f'{SITE["base_url"]}/posts/{post["slug"]}/',
    }, ensure_ascii=False)


def structured_website():
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE["title"],
        "url": SITE["base_url"],
        "description": SITE["description"],
    }, ensure_ascii=False)


def write_file(path, content):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def build():
    posts = load_posts()
    print(f"Loaded {len(posts)} posts")

    # ---- Individual post pages ----
    for p in posts:
        cat_name = CATEGORIES.get(p["category"], {}).get("name", p["category"])
        tags_html = "".join(f'<span class="tag">{t}</span>' for t in p["tags"])
        body = POST_TEMPLATE.format(
            title=html_mod.escape(p["title"]),
            date=p["date"],
            cat_slug=p["category"],
            cat_name=cat_name,
            tags_html=tags_html,
            html=p["html"],
        )
        html = render_page(
            title=p["title"],
            desc=p["description"] or p["title"],
            body=body,
            lang=p["lang"],
            url=f'{SITE["base_url"]}/posts/{p["slug"]}/',
            og_type="article",
            structured_data=structured_article(p),
        )
        write_file(f"{BUILD_DIR}/posts/{p['slug']}/index.html", html)

    # ---- Homepage with pagination ----
    posts_per_page = 10
    total_pages = max(1, (len(posts) + posts_per_page - 1) // posts_per_page)
    for page_num in range(1, total_pages + 1):
        start = (page_num - 1) * posts_per_page
        chunk = posts[start:start + posts_per_page]
        items = []
        for p in chunk:
            cat_name = CATEGORIES.get(p["category"], {}).get("name", p["category"])
            items.append(INDEX_POST.format(
                title=html_mod.escape(p["title"]),
                slug=p["slug"],
                date=p["date"],
                cat_slug=p["category"],
                cat_name=cat_name,
                desc=html_mod.escape(p["description"] or ""),
            ))
        prev_link = ""
        next_link = ""
        if page_num > 1:
            href = "/" if page_num == 2 else f"/page/{page_num - 1}/"
            prev_link = f'<a href="{href}">&larr; Newer</a>'
        if page_num < total_pages:
            next_link = f'<a href="/page/{page_num + 1}/">Older &rarr;</a>'
        body = f'<ul class="post-list">{"".join(items)}</ul>'
        body += PAGINATION.format(prev_link=prev_link, next_link=next_link)
        title = SITE["title"] if page_num == 1 else f"{SITE['title']} — Page {page_num}"
        desc = SITE["description"] if page_num == 1 else f"{SITE['description']} Page {page_num}"
        url = SITE["base_url"] if page_num == 1 else f'{SITE["base_url"]}/page/{page_num}/'
        html = render_page(title=title, desc=desc, body=body, url=url, structured_data=structured_website())
        dest = f"{BUILD_DIR}/index.html" if page_num == 1 else f"{BUILD_DIR}/page/{page_num}/index.html"
        write_file(dest, html)
    print(f"  Homepage: {total_pages} page(s)")

    # ---- Categories index ----
    cat_items = ""
    for slug, info in CATEGORIES.items():
        cat_posts = [p for p in posts if p["category"] == slug]
        if not cat_posts:
            continue
        cat_items += f'<li class="post-item"><h2 class="post-title"><a href="/categories/{slug}/">{info["name"]}</a></h2><p class="post-desc">{len(cat_posts)} post(s)</p></li>'
    body = f'<h1 class="section-title">Categories</h1><ul class="post-list">{cat_items}</ul>'
    write_file(f"{BUILD_DIR}/categories/index.html", render_page(
        title="Categories", desc="All categories", body=body,
        url=f'{SITE["base_url"]}/categories/', structured_data=structured_website()))

    # ---- Individual category pages ----
    for slug, info in CATEGORIES.items():
        cat_posts = [p for p in posts if p["category"] == slug]
        if not cat_posts:
            continue
        items = []
        for p in cat_posts:
            items.append(INDEX_POST.format(
                title=html_mod.escape(p["title"]), slug=p["slug"], date=p["date"],
                cat_slug=p["category"], cat_name=info["name"], desc=html_mod.escape(p["description"] or "")))
        body = CAT_TAG_PAGE.format(name=info["name"], items="".join(items))
        write_file(f"{BUILD_DIR}/categories/{slug}/index.html", render_page(
            title=info["name"], desc=f"Posts about {info['name']}", body=body,
            url=f'{SITE["base_url"]}/categories/{slug}/'))
    print(f"  Categories: {len(CATEGORIES)}")

    # ---- RSS feed ----
    items = []
    for p in posts[:20]:
        items.append(f"""    <item>
      <title>{html_mod.escape(p['title'])}</title>
      <link>{SITE['base_url']}/posts/{p['slug']}/</link>
      <guid>{SITE['base_url']}/posts/{p['slug']}/</guid>
      <description>{html_mod.escape(p['description'] or '')}</description>
      <pubDate>{p['date']}T00:00:00+08:00</pubDate>
    </item>""")
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{SITE['title']}</title>
    <link>{SITE['base_url']}</link>
    <description>{SITE['description']}</description>
    <language>en</language>
    <atom:link href="{SITE['base_url']}/rss.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>"""
    write_file(f"{BUILD_DIR}/rss.xml", rss)

    # ---- Sitemap ----
    urls = [f"""  <url><loc>{SITE['base_url']}/</loc><priority>1.0</priority></url>"""]
    urls.append(f"""  <url><loc>{SITE['base_url']}/about/</loc><priority>0.6</priority></url>""")
    urls.append(f"""  <url><loc>{SITE['base_url']}/categories/</loc><priority>0.7</priority></url>""")
    for slug in CATEGORIES:
        urls.append(f"""  <url><loc>{SITE['base_url']}/categories/{slug}/</loc><priority>0.6</priority></url>""")
    for p in posts:
        urls.append(f"""  <url><loc>{SITE['base_url']}/posts/{p['slug']}/</loc><priority>0.8</priority><lastmod>{p['date']}</lastmod></url>""")
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""
    write_file(f"{BUILD_DIR}/sitemap.xml", sitemap)

    # ---- Robots.txt ----
    robots = f"""User-agent: *
Allow: /
Sitemap: {SITE['base_url']}/sitemap.xml
"""
    write_file(f"{BUILD_DIR}/robots.txt", robots)

    # ---- About page ----
    about_body = """<article class="about-content">
<h1 class="section-title">About</h1>
<p>This blog explores the intersection of <strong>machine learning</strong>, <strong>multiscale modeling</strong>, and <strong>fiber-based biomaterials</strong>.</p>
<p>Written by a PhD researcher who believes in making computational methods accessible to scientists across disciplines.</p>
<h2>Topics</h2>
<ul>
<li>Python tutorials for scientific computing</li>
<li>Multiscale simulation techniques (MD, FE, coarse-graining)</li>
<li>Machine learning applications in materials science</li>
<li>Data analysis for biomaterials research</li>
<li>Research workflows and reproducibility</li>
</ul>
<h2>Contact</h2>
<p>For questions, collaborations, or feedback, reach out via <a href="https://github.com/GellmanSparrowS">GitHub</a>.</p>
</article>"""
    write_file(f"{BUILD_DIR}/about/index.html", render_page(
        title="About", desc="About ML-Biomat — Machine Learning & Multiscale Modeling for Biomaterials",
        body=about_body, url=f'{SITE["base_url"]}/about/'))

    # ---- 404 ----
    write_file(f"{BUILD_DIR}/404.html", render_page(
        title="404 — Not Found", desc="Page not found",
        body="<h1>404</h1><p>Page not found. <a href='/'>Back to home</a>.</p>",
        url=f'{SITE["base_url"]}/404.html'))

    # ---- Copy static files ----
    static_out = Path(BUILD_DIR) / "static"
    if static_out.exists():
        shutil.rmtree(static_out)
    shutil.copytree("static", static_out)

    print("Build complete. Site is in output/")


if __name__ == "__main__":
    build()
