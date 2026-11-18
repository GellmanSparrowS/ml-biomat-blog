"""Public, build-time Markdown representations of canonical website pages.

This module never requests remote content. HTML remains the browser source; the
sidecars are used by agent discovery and the edge content-negotiation worker.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from html.parser import HTMLParser
import json
import hashlib
from pathlib import Path
import re
from typing import Iterator
from urllib.parse import quote, unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET


VOID = frozenset('area base br col embed hr img input link meta param source track wbr'.split())
SKIP_TAGS = frozenset('script style noscript template nav button input select textarea form fieldset label output dialog canvas iframe object embed'.split())
SKIP_CLASSES = frozenset('site-header site-footer toc bc-toc tutorial-toc lesson-toc skip skip-link article-support site-sponsor adsbygoogle giscus cta-banner lang-switch lang-badge card-tags article-breadcrumb bc-crumb code-actions lab-controls trajectory-controls trajectory-player tutorial-related bc-related tutorial-neighbors fn-language home-scene fn-scene'.split())
BLOCK_TAGS = frozenset('article main section div header aside footer figure figcaption address details summary dl dt dd'.split())
EXCLUDED_ROUTES = ('/payment/', '/payments/', '/download/', '/downloads/', '/checkout/')


@dataclass
class Node:
    tag: str
    attrs: dict[str, str | None] = field(default_factory=dict)
    children: list[Node | str] = field(default_factory=list)
    raw: str = field(default="", repr=False)
    start: int = field(default=0, repr=False)

    def walk(self) -> Iterator[Node]:
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()

    def text(self) -> str:
        return ''.join(c.text() if isinstance(c, Node) else c for c in self.children)

    @property
    def classes(self) -> set[str]:
        return set((self.attrs.get('class') or '').split())


class Document(HTMLParser):
    def __init__(self, source: str):
        super().__init__(convert_charrefs=True)
        self.source = source
        self.line_offsets = [0]
        for line in source.splitlines(keepends=True):
            self.line_offsets.append(self.line_offsets[-1] + len(line))
        self.root = Node('document')
        self.stack = [self.root]
        self.feed(source)
        self.close()

    def handle_starttag(self, tag, attrs):
        # Preserve the browser's first occurrence of a duplicate HTML attribute.
        attr_map = {}
        for key, value in attrs:
            attr_map.setdefault(key, value)
        node = Node(tag, attr_map)
        if tag == "svg":
            line, column = self.getpos()
            node.start = self.line_offsets[line - 1] + column
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                if tag == 'svg':
                    line, column = self.getpos()
                    position = self.line_offsets[line - 1] + column
                    end = self.source.find('>', position) + 1
                    self.stack[index].raw = self.source[self.stack[index].start:end]
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def _compact(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def _escape_label(text: str) -> str:
    return _compact(text).replace('\\', '\\\\').replace('[', '\\[').replace(']', '\\]')


def _url(value: str | None, source_url: str) -> str:
    if not value:
        return ''
    target = urljoin(source_url, value.strip())
    if urlsplit(target).scheme not in ('http', 'https', 'mailto'):
        return ''
    # Parentheses and spaces must not terminate Markdown link destinations.
    return target.replace(' ', '%20').replace('(', '%28').replace(')', '%29')




class Markdown:
    def __init__(self, source_url: str, omit_heading: Node | None = None, root: Node | None = None):
        self.source_url = source_url
        self.omit_heading = omit_heading
        self.code_blocks: list[str] = []
        self.svg_anchors: dict[int, str] = {}
        self.math_records: dict[int, dict] = {}
        self.math_assets: dict[str, str] = {}
        if root:
            def record(node: Node, anchor: str, ancestors: list[Node]):
                anchor = node.attrs.get('id') or anchor
                if node.tag == 'svg':
                    self.svg_anchors[id(node)] = anchor
                if node.tag == 'mjx-container':
                    # Author-provided expressions are the source of truth. SVG
                    # presentation group order is NOT logical MathML order.
                    plain = next((a.attrs['data-plain'] for a in reversed(ancestors) if a.attrs.get('data-plain')), None)
                    tex = next((a.attrs.get('data-tex') or a.attrs.get('data-latex') for a in reversed(ancestors[-2:]) if a.attrs.get('data-tex') or a.attrs.get('data-latex')), None)
                    if not tex and ancestors and 'equation-display' in ancestors[-1].classes:
                        tex = ancestors[-1].attrs.get('aria-label')
                    if plain:
                        self.math_records[id(node)] = {'kind': 'plain', 'value': plain}
                    elif tex:
                        self.math_records[id(node)] = {'kind': 'tex', 'value': tex}
                    else:
                        svg = next((n for n in node.walk() if n.tag == 'svg'), None)
                        label = next((a.attrs['aria-label'] for a in reversed(ancestors[-2:]) if a.attrs.get('aria-label')), 'Formula')
                        if svg and svg.raw:
                            raw = svg.raw
                            digest = hashlib.sha256(raw.encode('utf-8')).hexdigest()[:24]
                            path = '/static/agent-math/' + digest + '.svg'
                            self.math_assets[path] = raw
                            self.math_records[id(node)] = {'kind': 'image', 'path': path, 'label': label, 'raw': raw}
                        else:
                            self.math_records[id(node)] = {'kind': 'link', 'label': label, 'anchor': anchor}
                for child in node.children:
                    if isinstance(child, Node):
                        record(child, anchor, ancestors + [node])
            record(root, '', [])

    def skipped(self, node: Node) -> bool:
        if node.tag in SKIP_TAGS or node.classes & SKIP_CLASSES:
            return True
        if any(c == 'controls' or c.endswith('-controls') or c == 'code-actions' for c in node.classes):
            return True
        if any(isinstance(c, Node) and c.tag == 'script' and 'giscus.app/' in (c.attrs.get('src') or '') for c in node.children):
            return True
        if 'hidden' in node.attrs or node.attrs.get('aria-hidden') == 'true':
            return True
        if node.tag == 'aside' and (node.attrs.get('aria-label') or '') in {'本页目录', 'Table of contents'}:
            return True
        if node.tag == 'p' and any(isinstance(c, Node) and c.tag == 'output' for c in node.children):
            return True
        if node.attrs.get('role') in {'navigation', 'dialog'}:
            return True
        style = node.attrs.get('style') or ''
        return bool(re.search(r'(?:^|;)\s*(?:display\s*:\s*none|visibility\s*:\s*hidden)\b', style, re.I))

    def render(self, node: Node | str) -> str:
        if isinstance(node, str):
            return re.sub(r'\s+', ' ', node)
        if node is self.omit_heading or self.skipped(node):
            return ''
        tag = node.tag
        if tag == 'pre':
            code = next((child for child in node.children if isinstance(child, Node) and child.tag == 'code'), node)
            value = code.text().replace('\r\n', '\n').strip('\n')
            language = next((x.removeprefix('language-') for x in code.classes if x.startswith('language-')), '')
            language = re.sub(r'[^a-zA-Z0-9_+.-]', '', language)
            fence = '`' * max(3, max((len(x) + 1 for x in re.findall(r'`+', value)), default=3))
            block = '\n\n' + fence + language + '\n' + value + '\n' + fence + '\n\n'
            marker = '\x00CODE' + str(len(self.code_blocks)) + '\x00'
            self.code_blocks.append(block)
            return '\n\n' + marker + '\n\n'
        if tag == 'mjx-container':
            record = self.math_records.get(id(node), {})
            kind = record.get('kind')
            if kind == 'plain':
                return '\n\n' + record['value'] + '\n\n'
            if kind == 'tex':
                value = record['value']
                return '\n\n$$\n' + value + '\n$$\n\n' if node.attrs.get('display') == 'true' else '$' + value + '$'
            if kind == 'image':
                return '![' + _escape_label(record['label']) + '](' + _url(record['path'], self.source_url) + ')'
            target = self.source_url + ('#' + quote(record.get('anchor', ''), safe='-._~') if record.get('anchor') else '')
            return '[' + _escape_label(record.get('label', 'Formula')) + '](' + target + ')'
        if tag == 'math':
            annotation = next((n for n in node.walk() if n.tag == 'annotation' and n.attrs.get('encoding') in {'application/x-tex', 'application/x-latex'}), None)
            value = annotation.text() if annotation else node.text()
            return '$' + value.strip() + '$'
        if tag == 'svg':
            label = node.attrs.get('aria-label') or next((n.text() for n in node.walk() if n.tag == 'title'), '')
            anchor = self.svg_anchors.get(id(node), '')
            target = self.source_url + ('#' + quote(anchor, safe='-._~') if anchor else '')
            return '\n\n[Figure: ' + _escape_label(label or 'diagram') + '](' + target + ')\n\n'
        if tag == 'img':
            href = _url(node.attrs.get('data-full-src') or node.attrs.get('src'), self.source_url)
            return '![' + _escape_label(node.attrs.get('alt') or '') + '](' + href + ')' if href else ''
        if tag == 'table':
            rows = []
            for row in (n for n in node.walk() if n.tag == 'tr'):
                cells = [c for c in row.children if isinstance(c, Node) and c.tag in {'th', 'td'}]
                if cells:
                    rows.append([_compact(self.render(c)).replace('|', r'\|') for c in cells])
            if not rows:
                return ''
            width = max(map(len, rows))
            rows = [row + [''] * (width - len(row)) for row in rows]
            lines = ['| ' + ' | '.join(row) + ' |' for row in rows]
            lines.insert(1, '| ' + ' | '.join(['---'] * width) + ' |')
            return '\n\n' + '\n'.join(lines) + '\n\n'
        if tag in {'ul', 'ol'}:
            items = node.children
            result = []
            try:
                start = int(node.attrs.get('start') or 1)
            except ValueError:
                start = 1
            index = start
            for item in items:
                # Older source HTML places paragraphs and code directly in lists.
                # Keep those siblings in order instead of dropping their content.
                if not isinstance(item, Node) or item.tag != 'li':
                    rendered = self.render(item).strip()
                    if rendered:
                        result.append('\n' + rendered + '\n')
                    continue
                if self.skipped(item):
                    continue
                rendered = ''.join(self.render(c) for c in item.children).strip()
                if rendered:
                    prefix = f'{index}. ' if tag == 'ol' else '- '
                    lines = rendered.splitlines()
                    result.append(prefix + lines[0] + ''.join('\n' + ' ' * len(prefix) + line for line in lines[1:]))
                index += 1
            return '\n\n' + '\n'.join(result) + '\n\n' if result else ''
        if 'symbol-key' in node.classes:
            return '\n\n' + '\n'.join('- ' + self.render(c).strip() for c in node.children if isinstance(c, Node)) + '\n\n'
        inner = ''.join(self.render(child) for child in node.children)
        if tag == 'a':
            href = _url(node.attrs.get('href'), self.source_url)
            text = inner.strip()
            if not text:
                return ''
            heading = next((n for n in node.walk() if re.fullmatch('h[1-6]', n.tag)), None)
            if heading is not None and href:
                old = self.render(heading).strip()
                label = _compact(''.join(self.render(c) for c in heading.children))
                new = '#' * int(heading.tag[1]) + ' [' + label + '](' + href + ')'
                return '\n\n' + text.replace(old, new, 1) + '\n\n'
            return '[' + _compact(text) + '](' + href + ')' if href else text
        if tag in {'strong', 'b'}:
            return '**' + inner.strip() + '**' if inner.strip() else ''
        if tag in {'em', 'i'}:
            return '*' + inner.strip() + '*' if inner.strip() else ''
        if tag == 'code':
            raw = node.text().strip()
            fence = '`' * max(1, max((len(x) + 1 for x in re.findall(r'`+', raw)), default=1))
            return fence + (' ' if '`' in raw else '') + raw + (' ' if '`' in raw else '') + fence
        if tag in {'sub', 'sup'}:
            return ('_{' if tag == 'sub' else '^{') + inner + '}'
        if re.fullmatch('h[1-6]', tag):
            return '\n\n' + '#' * int(tag[1]) + ' ' + _compact(inner) + '\n\n'
        if tag == 'blockquote':
            return '\n\n' + '\n'.join('> ' + line for line in inner.strip().splitlines()) + '\n\n'
        if tag == 'br':
            return '\n'
        if tag == 'hr':
            return '\n\n---\n\n'
        if tag == 'p' or tag in BLOCK_TAGS:
            return '\n\n' + inner.strip() + '\n\n' if inner.strip() else ''
        return inner

    def finish(self, text: str) -> str:
        text = re.sub(r'[ \t]+\n', '\n', text)
        text = re.sub(r'\n[ \t]+\n', '\n\n', text)
        text = re.sub(r'\n{3,}', '\n\n', text).strip()
        for index, block in enumerate(self.code_blocks):
            text = text.replace('\x00CODE' + str(index) + '\x00', block.strip('\n'))
        return text + '\n'


def profile_summary(source: str) -> str:
    """Read the displayed biography from a profile page or its body fragment."""
    doc = Document(source)
    reader = Markdown('')
    summaries = []

    def visit(node: Node) -> None:
        if reader.skipped(node):
            return
        if node.tag == 'p' and 'pr-summary' in node.classes:
            summaries.append(_compact(reader.render(node)))
            return
        for child in node.children:
            if isinstance(child, Node):
                visit(child)

    visit(doc.root)
    if len(summaries) != 1 or not summaries[0]:
        raise ValueError('Expected one visible, non-empty p.pr-summary in the author profile.')
    return summaries[0]


def _heading_title(heading: Node) -> str:
    parts = []
    for child in heading.children:
        if isinstance(child, str):
            parts.append(child)
        elif 'topic-total' not in child.classes:
            text = child.text()
            parts.append(' ' + text + ' ' if child.attrs.get('lang') else text)
    return _compact(''.join(parts))


def convert(source: str, source_url: str) -> dict | None:
    """Convert one canonical page; return None for redirects/non-content pages."""
    doc = Document(source)
    nodes = list(doc.root.walk())
    canonical = next((n.attrs.get('href') for n in nodes if n.tag == 'link' and n.attrs.get('rel') == 'canonical'), None)
    if not canonical or urljoin(source_url, canonical).rstrip('/') != source_url.rstrip('/'):
        return None
    if any(n.tag == 'meta' and (n.attrs.get('http-equiv') or '').lower() == 'refresh' for n in nodes):
        return None
    main = next((n for n in nodes if n.tag == 'main'), None)
    if not main:
        return None
    heading = next((n for n in main.walk() if n.tag == 'h1'), None)
    title = _heading_title(heading) if heading else next((_compact(n.text()).removesuffix(' — ML-Biomat') for n in nodes if n.tag == 'title'), 'ML-Biomat')
    language = next((n.attrs.get('lang') or 'zh-CN' for n in nodes if n.tag == 'html'), 'zh-CN')
    converter = Markdown(source_url, heading, main)
    body = converter.finish(converter.render(main)).strip()
    if not body:
        return None
    markdown = f'# {title}\n\nSource: {source_url}\nLanguage: {language}\n\n{body}\n'
    return {'title': title, 'lang': 'en' if language.startswith('en') else 'zh', 'text': markdown, 'assets': converter.math_assets}


def _route(url: str, base_url: str) -> str | None:
    parsed = urlsplit(urljoin(base_url + '/', url))
    base = urlsplit(base_url)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc or parsed.query or parsed.fragment:
        return None
    route = parsed.path or '/'
    if not route.endswith('/') or route.startswith(EXCLUDED_ROUTES) or '..' in unquote(route).split('/') or '\\' in unquote(route):
        return None
    return route


def generate(build_root: Path, base_url: str, search_data: list) -> dict:
    """Write Markdown siblings and discovery indexes from the current build."""
    root = Path(build_root).resolve()
    base_url = base_url.rstrip('/')
    sitemap = ET.parse(root / 'sitemap.xml')
    routes = sorted({route for loc in sitemap.findall('.//{*}loc') if loc.text and (route := _route(loc.text, base_url))})
    search = {}
    for item in search_data:
        item_route = _route(item.get('url') or '/posts/' + item['slug'] + '/', base_url)
        if item_route:
            search[item_route] = item
    pages, texts = [], {}
    profiles = {}
    html_bytes = 0
    for route in routes:
        path = (root / unquote(route.lstrip('/')) / 'index.html').resolve()
        if not path.is_relative_to(root) or not path.is_file():
            continue
        source = path.read_text(encoding='utf-8')
        result = convert(source, base_url + route)
        if not result:
            continue
        if route in ('/about/', '/about/en/'):
            profiles[route] = profile_summary(source)
        target = path.with_suffix('.md')
        target.write_text(result['text'], encoding='utf-8', newline='\n')
        for asset, raw in result['assets'].items():
            destination = root / asset.lstrip('/')
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(raw, encoding='utf-8', newline='\n')
        entry = {'url': route, 'markdown': route + 'index.md', 'title': result['title'], 'lang': result['lang']}
        if route in search:
            entry['category'] = search[route]['category']
        pages.append(entry)
        texts[route] = result['text']
        html_bytes += len(source.encode('utf-8'))
    (root / 'agent-index.json').write_text(json.dumps({'version': 1, 'pages': pages}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    catalog = ['# ML-Biomat', '', '> Bilingual research tutorials, scientific computing and biomaterials resources.', '',
               'Public reading requires no account or credentials. Follow the license and attribution notices in each resource.', '']
    if profiles:
        catalog.extend(['## 作者 / Author', ''])
        for route, label in [('/about/', '中文个人主页'), ('/about/en/', 'English research profile')]:
            if route in profiles:
                catalog.extend([profiles[route], '', f'[{label}]({base_url}{route})', ''])
        catalog.extend(['[复旦大学课题组档案 / Fudan University profile](https://swdfz.fudan.edu.cn/fd/36/c54394a785718/page.htm)', ''])
    catalog.extend(['## Reading and search', '',
               f'- [Page and Markdown index]({base_url}/agent-index.json)',
               f'- [Search index]({base_url}/search.json)',
               f'- [Complete text]({base_url}/llms-full.txt)',
               f'- [Public access]({base_url}/auth.md)', '',
               'Each page below has a Markdown sibling named `index.md`. HTML remains the browser representation.', ''])
    core = [entry for entry in pages if entry['url'] not in search]
    articles = [entry for entry in pages if entry['url'] in search]
    for heading, entries in [('Site pages and catalogs', core), ('Articles and tutorials', articles)]:
        catalog.extend(['## ' + heading, ''])
        for entry in entries:
            item = search.get(entry['url'], {})
            suffix = ' — ' + _compact(item.get('description') or '') if item.get('description') else ''
            catalog.append(f'- [{entry["lang"]}] [{_escape_label(entry["title"])}]({base_url}{entry["markdown"]}){suffix}')
        catalog.append('')
    (root / 'llms.txt').write_text('\n'.join(catalog), encoding='utf-8', newline='\n')
    full = '# ML-Biomat public content\n\nCanonical public pages, including their source URLs and individual license notices.\n\n' + '\n\n---\n\n'.join(texts[entry['url']].rstrip() for entry in pages) + '\n'
    (root / 'llms-full.txt').write_text(full, encoding='utf-8', newline='\n')
    return {'pages': len(pages), 'articles': len(articles), 'markdown_bytes': sum(len(t.encode('utf-8')) for t in texts.values()), 'html_bytes': html_bytes, 'full_bytes': len(full.encode('utf-8'))}


def validate(build_root: Path) -> dict:
    """Check published discovery coverage and scientific-text preservation."""
    root = Path(build_root).resolve()
    errors = []
    index = json.loads((root / 'agent-index.json').read_text(encoding='utf-8'))
    pages = index.get('pages', [])
    if index.get('version') != 1 or not isinstance(pages, list):
        return {'ok': False, 'errors': ['Invalid agent index schema'], 'pages': 0, 'articles': 0, 'code_blocks': 0, 'math_blocks': 0}
    seen = set()
    sources = {}
    counts = {'pages': 0, 'articles': 0, 'code_blocks': 0, 'math_blocks': 0}
    for entry in pages:
        route = entry.get('url', '')
        markdown_path = entry.get('markdown', '')
        if not route.startswith('/') or not route.endswith('/') or route in seen or markdown_path != route + 'index.md':
            errors.append(f'Invalid or duplicate route: {route}')
            continue
        seen.add(route)
        target = (root / unquote(markdown_path.lstrip('/'))).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            errors.append(f'Missing Markdown: {route}')
            continue
        text = target.read_text(encoding='utf-8')
        if not text.startswith('# ' + entry.get('title', '') + '\n') or entry.get('lang') not in {'zh', 'en'}:
            errors.append(f'Invalid title or language: {route}')
        source = re.search(r'^Source: (https?://[^\n]+)$', text, re.M)
        if not source or urlsplit(source[1]).path != route:
            errors.append(f'Invalid source URL: {route}')
            continue
        sources[route] = source[1]
        html_path = target.with_suffix('.html')
        if not html_path.is_file():
            errors.append(f'Missing HTML: {route}')
            continue
        doc = Document(html_path.read_text(encoding='utf-8'))
        main = next((n for n in doc.root.walk() if n.tag == 'main'), None)
        converter = Markdown(source[1], root=main)
        def content_nodes(node):
            if converter.skipped(node):
                return
            yield node
            for child in node.children:
                if isinstance(child, Node):
                    yield from content_nodes(child)
        if main:
            for node in content_nodes(main):
                if node.tag == 'pre':
                    code = next((c for c in node.children if isinstance(c, Node) and c.tag == 'code'), node)
                    value = code.text().replace('\r\n', '\n').strip('\n')
                    if value and value not in text:
                        errors.append(f'Code content changed: {route}')
                    counts['code_blocks'] += 1
                if node.tag == 'mjx-container':
                    record = converter.math_records.get(id(node), {})
                    if record.get('kind') in {'plain', 'tex'}:
                        if record['value'] not in text and record['value'] not in text.replace(r'\|', '|'):
                            errors.append(f'Authored formula missing: {route}')
                    elif record.get('kind') == 'image':
                        asset = root / record['path'].lstrip('/')
                        if record['path'] not in text or not asset.is_file() or asset.read_text(encoding='utf-8') != record['raw']:
                            errors.append(f'Original formula image missing or changed: {route}')
                    else:
                        errors.append(f'Formula has no authored text or original image: {route}')
                    counts['math_blocks'] += 1
        if route.startswith(('/tutorials/', '/posts/')):
            counts['articles'] += 1
            if re.search(r'(?:https://www\.paypal\.com/ncp/payment/|/static/images/(?:wechat\.png|alipay\.jpg))', text):
                errors.append(f'Support controls leaked into Markdown: {route}')
        counts['pages'] += 1
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    for item in search:
        route = item.get('url') or '/posts/' + item['slug'] + '/'
        if route not in seen:
            errors.append(f'Search entry omitted: {route}')
    catalog = (root / 'llms.txt').read_text(encoding='utf-8')
    full = (root / 'llms-full.txt').read_text(encoding='utf-8')
    for entry in pages:
        if entry['markdown'] not in catalog:
            errors.append(f'Catalog entry missing: {entry["url"]}')
        # Each full document includes its title and canonical source URL.
        if '# ' + entry['title'] + '\n' not in full or 'Source: ' + sources.get(entry['url'], '') + '\n' not in full:
            errors.append(f'Full text missing page: {entry["url"]}')
    return {'ok': not errors, 'errors': errors[:40], 'error_count': len(errors), **counts}
