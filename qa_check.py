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



class PageNode:
    """Small standard-library DOM for semantic checks, independent of CSS layout."""
    def __init__(self, tag='', attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def text(self):
        return ''.join(child.text() if isinstance(child, PageNode) else child for child in self.children)

    def find(self, tag=None, cls=None, attr=None, value=None):
        result = []
        for child in self.children:
            if not isinstance(child, PageNode):
                continue
            if ((tag is None or child.tag == tag)
                    and (cls is None or cls in child.attrs.get('class', '').split())
                    and (attr is None or attr in child.attrs)
                    and (value is None or child.attrs.get(attr) == value)):
                result.append(child)
            result.extend(child.find(tag, cls, attr, value))
        return result


class PageParser(HTMLParser):
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = PageNode()
        self.stack = [self.root]
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = PageNode(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, text):
        self.stack[-1].children.append(text)


def generated_dom(route, errors):
    path = DOCS / route.lstrip('/') / 'index.html'
    if not path.is_file():
        errors.append(route + ': missing page')
        return None
    return PageParser(path.read_text(encoding='utf-8')).root


def localized_switch_errors(dom, route, zh, en):
    switches = dom.find(cls='lang-switch')
    links = switches[0].find('a') if len(switches) == 1 else []
    actual = {node.attrs.get('data-language'): node.attrs.get('href') for node in links}
    return [] if actual == {'zh': zh, 'en': en} else [route + ': language switch loses page type or topic']


def homepage_errors(items, categories):
    errors = []
    for route, lang in [('/', 'zh'), ('/zh/', 'zh'), ('/en/', 'en')]:
        dom = generated_dom(route, errors)
        if dom is None:
            continue
        title = ('Rational design of biomaterial systems and structures across scales' if lang == 'en'
                 else '跨尺度生物材料体系与结构的理性设计')
        h1 = dom.find('h1')
        locale = dom.find('html')
        if len(h1) != 1 or h1[0].text().strip() != title or h1[0].find('br'):
            errors.append(route + ': research statement missing, duplicated or forcibly broken')
        if not locale or locale[0].attrs.get('lang') != ('en' if lang == 'en' else 'zh-CN'):
            errors.append(route + ': wrong document language')
        identity = dom.find(cls='home-identity')
        if len(identity) != 1 or ('Yunhao Yang' if lang == 'en' else '杨云浩') not in identity[0].text():
            errors.append(route + ': personal identity missing')
        errors.extend(localized_switch_errors(dom, route, '/', '/en/'))
        expected_topics = {key: sum(i['lang'] == lang and i['category'] == key for i in items)
                           for key in categories}
        expected_topics = {key: n for key, n in expected_topics.items() if n}
        navs = dom.find(cls='home-topic-index')
        links = navs[0].find('a') if len(navs) == 1 else []
        expected_links = {'/categories/' + key + ('/en/' if lang == 'en' else '/'): (key, count)
                          for key, count in expected_topics.items()}
        if len(links) != len(expected_links) or {a.attrs.get('href') for a in links} != set(expected_links):
            errors.append(route + ': home topic routes incomplete or wrong language')
        for link in links:
            key_count = expected_links.get(link.attrs.get('href'))
            if key_count:
                key, count = key_count
                counts = link.find('small')
                if categories[key]['name_' + lang] not in link.text() or len(counts) != 1 or counts[0].text().strip() != str(count):
                    errors.append(route + ': home topic label/count mismatch: ' + key)
        allowed = {i['url']: i for i in items if i['lang'] == lang}
        picks = dom.find('a', cls='home-lesson')
        if len(picks) != 3 or len({a.attrs.get('href') for a in picks}) != 3:
            errors.append(route + ': three distinct tutorial picks required')
        for pick in picks:
            item = allowed.get(pick.attrs.get('href'))
            heading = pick.find('h3')
            if not item or len(heading) != 1 or heading[0].text().strip() != item['title']:
                errors.append(route + ': tutorial pick title or language mismatch')
        direct = dom.find(cls='home-links')
        expected = {'/about/en/', '/categories/en/', '/fibernet/en/'} if lang == 'en' else {'/about/', '/categories/', '/fibernet/'}
        if len(direct) != 1 or {a.attrs.get('href') for a in direct[0].find('a')} != expected:
            errors.append(route + ': primary home links lose locale')
    for route in ['/articles/', '/articles/en/']:
        if not (DOCS / route.lstrip('/') / 'index.html').is_file():
            errors.append(route + ': separate article collection missing')
    return errors


def collection_errors(items, categories):
    """Every catalog row must match its source and occur once in its primary topic."""
    errors = []
    for lang in ['zh', 'en']:
        suffix = 'en/' if lang == 'en' else ''
        localized = [i for i in items if i['lang'] == lang]
        topics = {key: [i for i in localized if i['category'] == key] for key in categories}
        topics = {key: group for key, group in topics.items() if group}
        routes = [('/categories/' + suffix, None, True), ('/articles/' + suffix, None, False)]
        routes += [('/categories/' + key + '/' + suffix, key, False) for key in topics]
        for route, topic, overview in routes:
            dom = generated_dom(route, errors)
            if dom is None:
                continue
            selected = topics[topic] if topic else localized
            expected = {item['url']: item for item in selected}
            rows = dom.find('article', cls='explore-row')
            seen = []
            for row in rows:
                links = row.find('a', cls='tutorial-card-main')
                headings = row.find('h2')
                url = links[0].attrs.get('href') if len(links) == 1 else None
                seen.append(url)
                item = expected.get(url)
                labels = row.find(cls='topic-name')
                if (not item or row.attrs.get('data-topic') != item['category'] or len(headings) != 1
                        or headings[0].text().strip() != item['title'] or len(labels) != 1
                        or labels[0].text().strip() != categories[item['category']]['name_' + lang]):
                    errors.append(route + ': row language/title/topic mismatch: ' + str(url))
            if len(seen) != len(expected) or set(seen) != set(expected):
                errors.append(route + ': missing, duplicated or foreign-language articles')
            layout = dom.find(attr='data-explore-mode')
            results = dom.find(cls='explore-results')
            cards = dom.find(cls='topic-overview-card')
            if (len(layout) != 1 or layout[0].attrs.get('data-explore-mode') != ('overview' if overview else 'articles')
                    or len(results) != 1 or ('hidden' in results[0].attrs) != overview):
                errors.append(route + ': incorrect initial overview/list state')
            if overview:
                if len(cards) != len(topics) or {c.attrs.get('data-color') for c in cards} != set(topics):
                    errors.append(route + ': overview must cover each active primary topic once')
                for card in cards:
                    key = card.attrs.get('data-color')
                    covers = card.find('a', cls='topic-cover')
                    if key not in topics or len(covers) != 1:
                        errors.append(route + ': invalid topic overview card')
                        continue
                    cover = covers[0]
                    heading, count = cover.find('h2'), cover.find('span')
                    if (cover.attrs.get('href') != '/categories/' + key + '/' + suffix or len(heading) != 1
                            or heading[0].text().strip() != categories[key]['name_' + lang]
                            or len(count) != 1 or count[0].text().strip() != str(len(topics[key])) + (' articles' if lang == 'en' else ' 篇')):
                        errors.append(route + ': overview label/count/route mismatch: ' + key)
            elif cards:
                errors.append(route + ': overview unexpectedly duplicated inside article list')
            select = dom.find('select', cls='topic-select')
            expected_values = ({'/categories/' + suffix} | {'/categories/' + key + '/' + suffix for key in topics}
                               if topic else {'all'} | set(topics))
            options = select[0].find('option') if len(select) == 1 else []
            if len(options) != len(expected_values) or {o.attrs.get('value') for o in options} != expected_values:
                errors.append(route + ': native mobile topic choices incomplete or wrong language')
            elif topic:
                selected_options = [o.attrs.get('value') for o in options if 'selected' in o.attrs]
                if 'data-topic-navigation' not in select[0].attrs or selected_options != [route]:
                    errors.append(route + ': native topic navigation not initialized')
            else:
                buttons = dom.find('button', attr='data-topic-filter')
                if ('data-topic-selection' not in select[0].attrs or len(buttons) != len(expected_values)
                        or {b.attrs['data-topic-filter'] for b in buttons} != expected_values
                        or [b.attrs['data-topic-filter'] for b in buttons if b.attrs.get('aria-pressed') == 'true'] != ['all']):
                    errors.append(route + ': topic filter controls not initialized')
            if topic:
                total = dom.find(cls='topic-total')
                headings = dom.find('h1')
                if (len(total) != 1 or total[0].text().strip() != str(len(selected)) + (' articles' if lang == 'en' else ' 篇')
                        or len(headings) != 1 or not headings[0].text().startswith(categories[topic]['name_' + lang])
                        or dom.find(attr='data-results-title')):
                    errors.append(route + ': topic title/count missing or repeated')
            base = '/categories/' + topic + '/' if topic else ('/categories/' if overview else '/articles/')
            errors.extend(localized_switch_errors(dom, route, base, base + 'en/'))
    return errors


def gallery_errors():
    """Photo inventories, localized captions and direct openers agree with their source."""
    errors = []
    albums = json.loads((ROOT / 'content/profile-albums.json').read_text(encoding='utf-8'))
    events = {album['id']: album for album in albums if album.get('section') == 'events'}
    for route, lang in [('/', 'zh'), ('/zh/', 'zh'), ('/en/', 'en'), ('/about/', 'zh'), ('/about/en/', 'en')]:
        dom = generated_dom(route, errors)
        if dom is None:
            continue
        activities = dom.find('article', cls='pr-activity')
        if len(activities) != len(events) or {a.attrs.get('id') for a in activities} != {'activity-' + key for key in events}:
            errors.append(route + ': activity inventory missing or duplicated')
        for activity in activities:
            album = events.get(activity.attrs.get('id', '').removeprefix('activity-'))
            if not album:
                continue
            title = album['title_en' if lang == 'en' else 'title']
            images = activity.find('a', attr='data-pr-image')
            expected = [(i['src'], i['caption_en' if lang == 'en' else 'caption']) for i in album['images']]
            actual = [(i.attrs.get('href'), i.attrs.get('data-caption')) for i in images]
            opener = activity.find('a', attr='data-pr-open')
            if actual != expected or activity.attrs.get('data-title') != title or 'data-pr-gallery' not in activity.attrs:
                errors.append(route + ': activity photos or localized captions differ: ' + album['id'])
            if len(opener) != 1 or opener[0].attrs.get('href') != expected[0][0] or opener[0].text().strip() != title:
                errors.append(route + ': activity title must open its own gallery: ' + album['id'])
        dialogs = dom.find('dialog', cls='pr-viewer')
        if len(dialogs) != 1:
            errors.append(route + ': one native gallery dialog required')
        else:
            dialog = dialogs[0]
            ids = {n.attrs['id'] for n in dialog.find(attr='id')}
            if any(dialog.attrs.get(a) not in ids for a in ['aria-labelledby', 'aria-describedby']):
                errors.append(route + ': gallery accessible name/caption missing')
            for attr in ['data-pr-close', 'data-pr-prev', 'data-pr-next', 'data-pr-count']:
                if len(dialog.find(attr=attr)) != 1:
                    errors.append(route + ': gallery control missing or duplicated: ' + attr)
        for gallery in dom.find(attr='data-pr-gallery'):
            for image in gallery.find('a', attr='data-pr-image'):
                thumbs = image.find('img')
                if len(thumbs) != 1 or not thumbs[0].attrs.get('alt') or thumbs[0].attrs.get('alt') != image.attrs.get('data-caption'):
                    errors.append(route + ': gallery thumbnail/caption missing')
        if route.startswith('/about/'):
            for anchor in ['research', 'publications', 'projects', 'honors', 'activities']:
                if len(dom.find(attr='id', value=anchor)) != 1:
                    errors.append(route + ': profile section missing or duplicated: ' + anchor)
            for paper in dom.find('article', cls='pr-paper'):
                citation = paper.find(cls='pr-paper-title')
                linked = citation[0].find('a') if citation else []
                headings = paper.find('h3')
                links = headings[0].find('a') if headings else []
                if linked and linked[0].attrs.get('href') not in {a.attrs.get('href') for a in links}:
                    errors.append(route + ': paper heading omits its publication link')
        if dom.find(cls='pr-scope') or dom.find(cls='pr-project'):
            errors.append(route + ': removed scope/tool blocks returned')
        for node in dom.find('a') + dom.find('button'):
            if re.search(r'^(?:阅读全文|方法与结果|查看\s*\d+\s*张照片|图片出处|Read paper|Methods.*results|View \d+ photos|Photo source)\b', node.text().strip(), re.I):
                errors.append(route + ': redundant page-level action returned')
        assets = {urlsplit(node.attrs.get('href', node.attrs.get('src', ''))).path for node in dom.find('link') + dom.find('script')}
        if not {'/static/css/profile-layout.css', '/static/js/profile-gallery.js'} <= assets:
            errors.append(route + ': profile/gallery assets missing')
        for node in dom.find('link') + dom.find('script'):
            url = node.attrs.get('href', node.attrs.get('src', ''))
            if '/.local/' in url or '/static/preview/' in url or 'site-preview' in url or '/redesign/' in url:
                errors.append(route + ': preview-only asset URL in production: ' + url)
    return errors


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
        shared = PageParser(page).root
        assets = {urlsplit(node.attrs.get('href', node.attrs.get('src', ''))).path for node in shared.find('link') + shared.find('script')}
        if not {'/static/css/site-layout.css', '/static/css/site-refinement.css', '/static/js/site-catalog.js'} <= assets:
            chrome_errors.append(relative+': shared layout assets missing')
        if len(shared.find('body', cls='site-layout')) != 1:
            chrome_errors.append(relative+': shared layout body class missing')
    checks.append(check('Shared navigation and dark-first shell',not chrome_errors,'; '.join(chrome_errors[:15]) if chrome_errors else 'All generated pages retain both language controls, matching navigation, and dark initialization'))
    from content_tools import catalog
    catalog_curriculum = dict(curriculum, lessons=[dict(lesson, url='/tutorials/polymer-ai/' + lesson['slug'] + '/') for lesson in lessons])
    items = catalog.entries(loaded, catalog_curriculum)
    home_errors = homepage_errors(items, build.CATEGORIES)
    checks.append(check('Home language switch preserves page type', not home_errors,
                        '; '.join(home_errors[:15]) if home_errors else 'Localized research homepages, topic counts, tutorial picks and same-page language links agree'))
    category_errors = collection_errors(items, build.CATEGORIES)
    checks.append(check('Localized topic overview and complete article collections', not category_errors,
                        '; '.join(category_errors[:15]) if category_errors else 'Each active topic appears once; overview, full lists and topic pages match source titles, language, counts and mobile controls'))
    profile_errors = gallery_errors()
    checks.append(check('Localized profile and homepage galleries', not profile_errors,
                        '; '.join(profile_errors[:15]) if profile_errors else 'Activity images and captions match source; direct photo/title openers, accessible dialogs and publication links are present'))
    primary_errors=[]
    for lesson in lessons:
        if len(lesson['categories'])!=1:primary_errors.append(lesson['slug'])
    for post in loaded:
        pair=build.find_pair(post,by_lang)
        if pair and pair['category']!=post['category']:primary_errors.append(post['slug'])
    checks.append(check('One primary topic with bilingual agreement',not primary_errors,', '.join(primary_errors) if primary_errors else '44 Chinese and 24 English entries have one primary topic; article pairs agree'))

    # Keep production pages free of the redundant display notes removed by review.
    clutter=[]
    forbidden_notes=['代码与运行结果在本页完整展开','图像与公式可以离线阅读','页面中的公式、图像和交互已经嵌入，离线也能阅读','本页已经展示实际运行结果']
    for page_path in DOCS.rglob('*.html'):
        text=page_path.read_text(encoding='utf8')
        if 'class="site-header"' not in text:continue
        if any(note in text for note in forbidden_notes):clutter.append(str(page_path.relative_to(DOCS)))
    for route in ['fibernet/index.html','fibernet/en/index.html']:
        text=(DOCS/route).read_text(encoding='utf8')
        hero=re.search(r'<header class="fn-hero">(.*?)</header>',text,re.S)
        if not hero or 'fn-scene-canvas' not in hero[1] or re.search(r'<button|id="(?:nodes|motion|reset|readout)"',hero[1]):clutter.append(route)
        if not re.search(r'/static/js/fibernet-scene\.js\?v=',text):clutter.append(route+': stale scene URL')
    checks.append(check('Concise page copy and automatic FiberNet scene',not clutter,', '.join(clutter) if clutter else 'Redundant display notes absent; both project pages have automatic decoration without display controls'))

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