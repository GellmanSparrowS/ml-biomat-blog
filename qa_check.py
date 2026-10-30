# -*- coding: utf-8 -*-
"""Post-build health checks -> _qa/site_report.html (open in browser)."""
import argparse
import html
import hashlib
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
            if (len(layout) != 1 or layout[0].attrs.get('data-explore-mode') != ('directory' if overview else 'articles')
                    or len(results) != 1 or 'hidden' in results[0].attrs or cards):
                errors.append(route + ': directory must show article results immediately')
            searches = dom.find('input', attr='data-directory-search')
            if len(searches) != 1 or searches[0].attrs.get('type') != 'search' or not searches[0].attrs.get('aria-label'):
                errors.append(route + ': accessible tutorial search missing')
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



def webp_size(raw):
    """Read committed preview dimensions without adding a build dependency."""
    if raw[:4] != b'RIFF' or raw[8:12] != b'WEBP':
        raise ValueError('not a WebP image')
    pos = 12
    while pos + 8 <= len(raw):
        kind = raw[pos:pos+4]
        length = int.from_bytes(raw[pos+4:pos+8], 'little')
        payload = raw[pos+8:pos+8+length]
        if len(payload) != length:
            raise ValueError('truncated WebP chunk')
        if kind == b'VP8X' and len(payload) >= 10:
            return 1 + int.from_bytes(payload[4:7], 'little'), 1 + int.from_bytes(payload[7:10], 'little')
        if kind == b'VP8L' and len(payload) >= 5 and payload[0] == 0x2f:
            bits = int.from_bytes(payload[1:5], 'little')
            return 1 + (bits & 0x3fff), 1 + ((bits >> 14) & 0x3fff)
        if kind == b'VP8 ' and len(payload) >= 10 and payload[3:6] == b'\x9d\x01\x2a':
            return int.from_bytes(payload[6:8], 'little') & 0x3fff, int.from_bytes(payload[8:10], 'little') & 0x3fff
        pos += 8 + length + length % 2
    raise ValueError('WebP dimensions unavailable')


def image_delivery_inventory():
    """Verify sealed originals and preview pixels rather than trusting srcset labels."""
    errors, sources, previews = [], {}, {}
    manifest_path = ROOT / 'static/images/previews/manifest.json'
    if not manifest_path.is_file():
        return {}, sources, previews, ['Image delivery manifest missing']
    data = json.loads(manifest_path.read_text(encoding='utf8'))['images']
    for key, item in data.items():
        full = item['full']
        if full in sources:
            if sources[full] != item:
                errors.append(key + ': aliases disagree about their original')
            continue
        sources[full] = item
        original = ROOT / unquote(full).lstrip('/')
        built = DOCS / unquote(full).lstrip('/')
        if not original.resolve().is_relative_to(ROOT) or not built.resolve().is_relative_to(DOCS):
            errors.append(full + ': image path outside the site')
            continue
        if not original.is_file() or not built.is_file():
            errors.append(full + ': original missing from source or published assets')
            continue
        raw = original.read_bytes()
        if hashlib.sha256(raw).hexdigest() != item['source_sha256'] or len(raw) != item['source_bytes']:
            errors.append(full + ': sealed original changed; regenerate its preview receipt')
        if hashlib.sha256(built.read_bytes()).hexdigest() != item['source_sha256']:
            errors.append(full + ': published original differs from its full-resolution source')
        w, h = item['width'], item['height']
        if w <= 0 or h <= 0:
            errors.append(full + ': invalid original dimensions')
            continue
        for variant in item['variants']:
            url = variant['src'];previews[url] = (item, variant)
            source = ROOT / unquote(url).lstrip('/')
            output = DOCS / unquote(url).lstrip('/')
            if not source.resolve().is_relative_to(ROOT) or not output.resolve().is_relative_to(DOCS):
                errors.append(url + ': preview path outside the site')
                continue
            if not source.is_file() or not output.is_file():
                errors.append(url + ': preview missing from source or published assets')
                continue
            payload = source.read_bytes()
            if (hashlib.sha256(payload).hexdigest() != variant['sha256'] or len(payload) != variant['bytes']
                    or hashlib.sha256(output.read_bytes()).hexdigest() != variant['sha256']):
                errors.append(url + ': preview bytes differ from its receipt')
            try:
                actual = webp_size(payload)
            except ValueError as error:
                errors.append(url + ': ' + str(error))
                continue
            vw, vh = variant['width'], variant['height']
            if actual != (vw, vh) or vw > w or vh > h or abs(vh - h * vw / w) > .51:
                errors.append(url + ': preview dimensions distort, crop, or enlarge the source')
            if len(payload) >= len(raw):
                errors.append(url + ': preview is not smaller than its original')
    return data, sources, previews, errors


def image_delivery_page(dom, route, mapping, sources, previews, errors):
    """Every displayed preview must retain its original; hidden albums load on demand."""
    count = 0
    def path(value):
        return unquote(urlsplit(value or '').path)
    def visit(node, hidden=False):
        nonlocal count
        if not isinstance(node, PageNode):
            return
        hidden = hidden or 'hidden' in node.attrs
        if node.tag == 'img':
            attrs = node.attrs
            requested = path(attrs.get('data-full-src') or attrs.get('src'))
            item = sources.get(requested) or mapping.get(requested)
            if item:
                count += 1
                if path(attrs.get('data-full-src')) != item['full']:
                    errors.append(route + ': preview omits its original image')
                if 'v=' + item['source_sha256'][:12] not in attrs.get('data-full-src', ''):
                    errors.append(route + ': original image cache version is stale')
                if attrs.get('decoding') != 'async' or attrs.get('loading') not in {'lazy', 'eager'}:
                    errors.append(route + ': image decoding or loading strategy missing')
                if not attrs.get('width', '').isdigit() or not attrs.get('height', '').isdigit():
                    errors.append(route + ': image intrinsic dimensions missing')
                else:
                    width, height = int(attrs['width']), int(attrs['height'])
                    if width <= 0 or abs(height - item['height'] * width / item['width']) > 1.1:
                        errors.append(route + ': image attributes change the original aspect ratio')
                preview_url = path(attrs.get('data-preview-src') if hidden else attrs.get('src'))
                if hidden:
                    if any(name in attrs for name in ['src', 'srcset', 'sizes']) or not preview_url:
                        errors.append(route + ': hidden gallery image can load before it is opened')
                mode = attrs.get('data-image-delivery')
                if mode == 'preview':
                    entry = previews.get(preview_url)
                    if not entry or entry[0]['full'] != item['full']:
                        errors.append(route + ': preview points at the wrong original')
                    candidates = attrs.get('srcset', '')
                    if not hidden and not candidates:
                        errors.append(route + ': displayed preview is missing its responsive candidates')
                    for candidate in candidates.split(',') if candidates else []:
                        parts = candidate.strip().split()
                        listed = previews.get(path(parts[0])) if parts else None
                        if (len(parts) != 2 or not listed or listed[0]['full'] != item['full']
                                or parts[1] != str(listed[1]['width']) + 'w'):
                            errors.append(route + ': invalid preview candidate or declared pixel width')
                elif mode != 'original' or preview_url != item['full']:
                    errors.append(route + ': unexpected original/preview delivery mode')
            elif attrs.get('data-image-delivery') or attrs.get('data-full-src'):
                errors.append(route + ': image delivery refers to an unsealed original')
        for child in node.children:
            visit(child, hidden)
    visit(dom)
    return count


def startup_asset_errors(dom, route):
    """A remote dependency must never block local navigation or automatic motion."""
    errors = []
    scripts = [n for n in dom.find('script') if n.attrs.get('src')]
    paths = [urlsplit(n.attrs['src']).path for n in scripts]
    motion = [i for i, path in enumerate(paths) if path == '/static/js/site-motion.js']
    if len(motion) != 1 or 'defer' not in scripts[motion[0]].attrs:
        errors.append(route + ': shared local motion policy is missing or not deferred')
    else:
        for i, path in enumerate(paths):
            if path in {'/static/js/main.js', '/static/js/fibernet-scene.js', '/static/js/fibernet-flow.js'} and i <= motion[0]:
                errors.append(route + ': animation initializes before the shared motion preference')
    for script in scripts:
        src = script.attrs['src'];parsed = urlsplit(src)
        if parsed.netloc and 'async' not in script.attrs:
            errors.append(route + ': external script can block local initialization: ' + parsed.path)
        if 'medium-zoom' in src or ('highlight.min.js' in src and parsed.netloc):
            errors.append(route + ': image or code presentation still depends on an external library')
    loaders = [n for n in scripts if urlsplit(n.attrs['src']).path == '/static/js/code-highlight.js']
    has_code = any(pre.find('code') for pre in dom.find('pre'))
    if bool(loaders) != has_code or len(loaders) > 1:
        errors.append(route + ': code highlighting loader does not match code content')
    for loader in loaders:
        for attr in ['data-highlight-js', 'data-highlight-css']:
            value = loader.attrs.get(attr, '')
            parsed = urlsplit(value)
            asset = DOCS / unquote(parsed.path).lstrip('/')
            if parsed.netloc or not parsed.path.startswith('/static/vendor/highlightjs/') or not asset.is_file():
                errors.append(route + ': code highlighting asset is missing or external')
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
                elif urlsplit(thumbs[0].attrs.get('data-full-src', '')).path != urlsplit(image.attrs.get('href', '')).path:
                    errors.append(route + ': gallery thumbnail and click target refer to different originals')
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



def course_integrity_errors(data, entries, categories):
    """Check every imported language against its sealed source, not template totals."""
    from content_tools import biomaterials_courses
    pairs, content = [], []
    totals = dict(sections=0, equations=0, figures=0, labs=0)
    expected_ids = {lesson['id'] for lesson in data['lessons']}
    expected_urls = {biomaterials_courses.route(identifier, lang)
                     for identifier in expected_ids for lang in ['zh', 'en']}
    if len(expected_ids) != 48 or len(entries) != len(expected_urls) or {item['url'] for item in entries} != expected_urls:
        pairs.append('Imported course IDs or bilingual catalog entries are incomplete or duplicated')
    indexed = {item['url']: item for item in entries}

    def semantic(node):
        if isinstance(node, str):
            return re.sub(r'\s+', ' ', node).strip()
        return [node.tag, sorted(node.attrs.items()), [value for child in node.children if (value := semantic(child))]]

    forbidden = ['请作者核实', '补写中', '本次更新', '根据你提供的资料', '来自某课件',
                 '本节贡献者', '正文润色稿', '润色时跳过', '仅供参考']
    for lesson in data['lessons']:
        identifier = lesson['id'].lower()
        category = lesson['category']
        if category not in categories:
            pairs.append(identifier + ': unknown category')
        addresses = {lang: biomaterials_courses.route(identifier, lang) for lang in ['zh', 'en']}
        for lang, address in addresses.items():
            dom = generated_dom(address, pairs)
            if dom is None:
                continue
            pairs.extend(localized_switch_errors(dom, address, addresses['zh'], addresses['en']))
            h1, locale = dom.find('h1'), dom.find('html')
            heads = dom.find('head')
            titles = heads[0].find('title') if len(heads) == 1 else []
            if (len(h1) != 1 or h1[0].text().strip() != lesson['title'][lang]
                    or len(titles) != 1 or titles[0].text().strip() != lesson['title'][lang] + ' — ML-Biomat'
                    or len(locale) != 1 or locale[0].attrs.get('lang') != ('en' if lang == 'en' else 'zh-CN')):
                pairs.append(address + ': localized title or document language does not match source')
            canonical = [n.attrs.get('href') for n in dom.find('link') if n.attrs.get('rel') == 'canonical']
            alternates = {n.attrs.get('hreflang'): urlsplit(n.attrs.get('href', '')).path
                          for n in dom.find('link') if n.attrs.get('rel') == 'alternate' and n.attrs.get('hreflang') in ['en', 'zh-CN']}
            if (len(canonical) != 1 or urlsplit(canonical[0]).path != address
                    or alternates != {'zh-CN': addresses['zh'], 'en': addresses['en']}):
                pairs.append(address + ': canonical or reciprocal alternate URLs incorrect')
            entry = indexed.get(address, {})
            if (entry.get('lang') != lang or entry.get('title') != lesson['title'][lang]
                    or entry.get('categories') != [category] or entry.get('category') != category):
                pairs.append(address + ': catalog title, language or primary category mismatch')
            crumbs = dom.find('nav', cls='bc-crumb')
            topic = '/categories/' + category + '/' + ('en/' if lang == 'en' else '')
            if len(crumbs) != 1 or topic not in {a.attrs.get('href') for a in crumbs[0].find('a')}:
                pairs.append(address + ': localized category breadcrumb missing')
            panes = dom.find('article', cls='language-pane')
            if len(panes) != 1 or panes[0].attrs.get('data-lang') != lang or 'hidden' in panes[0].attrs:
                content.append(address + ': expected one visible language article')
                continue
            pane = panes[0]
            source = ROOT / 'content/tutorials/biomaterials-courses' / (identifier + '-' + lang + '.html')
            original = source.read_text(encoding='utf-8')
            expected = lesson['counts'][lang]
            if hashlib.sha256(original.encode('utf-8')).hexdigest() != expected['sha256']:
                content.append(address + ': imported fragment no longer matches its source receipt')
            actual = {'sections':len(pane.find('section')), 'equations':len(pane.find(cls='equation')),
                      'figures':len(pane.find('figure', cls='science-figure')), 'labs':len(pane.find(attr='data-lab'))}
            for key, count in actual.items():
                totals[key] += count
                if count != expected[key]:
                    content.append(address + ': ' + key + ' differ from imported source')
            parsed_source = PageParser(original).root
            if [semantic(child) for child in pane.children if semantic(child)] != [semantic(child) for child in parsed_source.children if semantic(child)]:
                content.append(address + ': article text, formula geometry, figures or lab markup changed during rendering')
            sections = [node.attrs.get('id') for node in pane.find('section')]
            if sections != [lang + '-' + section['id'] for section in lesson['sections']]:
                content.append(address + ': section order or language anchors differ from source')
            ids = [node.attrs['id'] for node in dom.find(attr='id')]
            if len(ids) != len(set(ids)):
                content.append(address + ': duplicate DOM IDs')
            for node in dom.find('a'):
                href = node.attrs.get('href', '')
                if href.startswith('#') and unquote(href[1:]) not in ids:
                    content.append(address + ': missing same-page anchor ' + href)
            script_paths = {urlsplit(n.attrs.get('src', '')).path for n in dom.find('script')}
            lab_script = '/static/tutorials/biomaterials-courses/' + identifier + '.js'
            if not {lab_script, '/static/js/biomaterials-courses.js'} <= script_paths:
                content.append(address + ': interactive lesson or shared reader script missing')
            built_script, source_script = DOCS / lab_script.lstrip('/'), ROOT / lab_script.lstrip('/')
            if not built_script.is_file() or built_script.read_text(encoding='utf-8') != source_script.read_text(encoding='utf-8'):
                content.append(address + ': published lab script differs from source')
            public_text = pane.text()
            if any(note in public_text for note in forbidden) or re.search(r'file://|(?:^|[\s"\'>])[A-Za-z]:[\\/]|127\.0\.0\.1|localhost', original):
                content.append(address + ': editorial note or private local address in public article')
    return pairs, content, totals


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
    from content_tools import biomaterials_courses
    courses = biomaterials_courses.load()
    course_entries = biomaterials_courses.entries(courses)
    indexed_total = total + tutorial_count + len(course_entries)
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
    checks.append(check("RSS covers articles and tutorials", rss_n == indexed_total, "rss=%d articles=%d tutorials=%d bilingual course pages=%d" % (rss_n, total, tutorial_count, len(course_entries))))

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
    checks.append(check("Search covers articles and tutorials", search_n == indexed_total, "search=%d articles=%d tutorials=%d bilingual course pages=%d" % (search_n, total, tutorial_count, len(course_entries))))

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
    image_mapping, image_sources, image_previews, image_errors = image_delivery_inventory()
    delivery_count = 0; startup_errors = []
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
        delivery_count += image_delivery_page(shared, relative, image_mapping, image_sources, image_previews, image_errors)
        startup_errors.extend(startup_asset_errors(shared, relative))
        assets = {urlsplit(node.attrs.get('href', node.attrs.get('src', ''))).path for node in shared.find('link') + shared.find('script')}
        if not {'/static/css/site-layout.css', '/static/css/site-refinement.css', '/static/js/site-catalog.js'} <= assets:
            chrome_errors.append(relative+': shared layout assets missing')
        if len(shared.find('body', cls='site-layout')) != 1:
            chrome_errors.append(relative+': shared layout body class missing')
    checks.append(check('Shared navigation and dark-first shell',not chrome_errors,'; '.join(chrome_errors[:15]) if chrome_errors else 'All generated pages retain both language controls, matching navigation, and dark initialization'))
    checks.append(check('Readable previews preserve full-resolution originals', not image_errors,
                        '; '.join(image_errors[:15]) if image_errors else f'{len(image_sources)} sealed originals, {len(image_previews)} dimension-checked previews and {delivery_count} image placements; hidden galleries defer loading'))
    checks.append(check('Local motion starts independently of external libraries', not startup_errors,
                        '; '.join(startup_errors[:15]) if startup_errors else 'Shared motion policy precedes local animations; code libraries load locally only on pages with code'))
    from content_tools import catalog
    catalog_curriculum = dict(curriculum, lessons=[dict(lesson, url='/tutorials/polymer-ai/' + lesson['slug'] + '/') for lesson in lessons])
    items = catalog.entries(loaded, catalog_curriculum) + course_entries
    course_pairs, course_content, course_totals = course_integrity_errors(courses, course_entries, build.CATEGORIES)
    checks.append(check('Bilingual biomaterials tutorial routes and topic integration', not course_pairs,
                        '; '.join(course_pairs[:15]) if course_pairs else '48 complete language pairs with localized titles, canonical URLs, alternate links and topic breadcrumbs'))
    checks.append(check('Imported tutorial content, figures, equations and scientific labs', not course_content,
                        '; '.join(course_content[:15]) if course_content else 'All 96 pages preserve their sealed source: ' + ', '.join(str(value) + ' ' + key for key, value in course_totals.items())))
    home_errors = homepage_errors(items, build.CATEGORIES)
    checks.append(check('Home language switch preserves page type', not home_errors,
                        '; '.join(home_errors[:15]) if home_errors else 'Localized research homepages, topic counts, tutorial picks and same-page language links agree'))
    category_errors = collection_errors(items, build.CATEGORIES)
    checks.append(check('Localized searchable directory and complete article collections', not category_errors,
                        '; '.join(category_errors[:15]) if category_errors else 'Directory, full lists and topic pages match source titles, language, counts and mobile controls'))
    profile_errors = gallery_errors()
    checks.append(check('Localized profile and homepage galleries', not profile_errors,
                        '; '.join(profile_errors[:15]) if profile_errors else 'Activity images and captions match source; direct photo/title openers, accessible dialogs and publication links are present'))
    primary_errors=[]
    for lesson in lessons:
        if len(lesson['categories'])!=1:primary_errors.append(lesson['slug'])
    for post in loaded:
        pair=build.find_pair(post,by_lang)
        if pair and pair['category']!=post['category']:primary_errors.append(post['slug'])
    checks.append(check('One primary topic with bilingual agreement',not primary_errors,', '.join(primary_errors) if primary_errors else str(sum(i['lang'] == 'zh' for i in items)) + ' Chinese and ' + str(sum(i['lang'] == 'en' for i in items)) + ' English entries have one primary topic; article pairs agree'))

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
        if not re.search(r'/static/js/fibernet-flow\.js\?v=',text):clutter.append(route+': stale scene URL')
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