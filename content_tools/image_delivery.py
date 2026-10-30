"""Deliver bounded raster previews while keeping original images for inspection.

Only img start tags change. SVG, formulas, links, lesson text, scripts and styles
retain their original bytes. Preview generation is a separate Pillow task; the
regular site build uses only the standard library and the committed manifest.
"""
from __future__ import annotations
from functools import lru_cache
from html import escape,unescape
from pathlib import Path
from urllib.parse import unquote,urlsplit
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'static/images/previews/manifest.json'
ATTR=re.compile(r'\b([\w:-]+)\s*=\s*([\"\'])(.*?)\2',re.S)
TOKENS=re.compile(r'<script\b[^>]*>.*?</script\s*>|<style\b[^>]*>.*?</style\s*>|<img\b[^>]*>',re.I|re.S)

@lru_cache(maxsize=1)
def manifest():
    return json.loads(MANIFEST.read_text(encoding='utf8'))['images'] if MANIFEST.is_file() else {}

@lru_cache(maxsize=None)
def valid_source(url,digest):
    path=ROOT/unquote(urlsplit(url).path).lstrip('/')
    return path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==digest

def set_attr(tag,name,value):
    pattern=re.compile(r'(?<![\w:-])'+re.escape(name)+r'\s*=\s*([\"\']).*?\1',re.I|re.S)
    replacement=name+'="'+escape(str(value),quote=True)+'"'
    if pattern.search(tag):return pattern.sub(lambda _:replacement,tag,count=1)
    return re.sub(r'\s*/?>$',lambda m:' '+replacement+m[0],tag,count=1)

def remove_attr(tag,name):
    return re.sub(r'\s+'+re.escape(name)+r'\s*=\s*([\"\']).*?\1','',tag,flags=re.I|re.S)

def rewrite_html(content,route=''):
    data=manifest()
    if not data or '<img' not in content:return content
    homepage=route.strip('/') in {'','index.html','en','en/index.html','zh','zh/index.html'}
    def image(match):
        tag=match[0]
        if not tag.lower().startswith('<img'):return tag
        attrs={name.lower():unescape(value) for name,_,value in ATTR.findall(tag)}
        source=attrs.get('data-full-src') or attrs.get('src','')
        key=unquote(urlsplit(source).path)
        item=data.get(key)
        if not item or not valid_source(item['full'],item['source_sha256']):return tag
        full=item['full'];is_profile='/images/profile/' in full
        is_portrait=full.endswith('/photo-sq.jpg')
        limit=640 if is_portrait or is_profile and not homepage else 960 if is_profile else 1280
        variants=[v for v in item['variants'] if v['width']<=limit]
        # The fallback is intentionally a clear medium preview, never a blurry placeholder.
        if variants:
            selected=variants[-1]
            tag=set_attr(tag,'src',selected['src'])
            tag=set_attr(tag,'srcset',', '.join(v['src']+' '+str(v['width'])+'w' for v in variants))
            if is_portrait:sizes='(max-width:760px) 96px, 200px'
            elif homepage and is_profile and '/paper-' not in full:
                sizes='(max-width:360px) 90px, (max-width:760px) 116px, (min-width:1160px) 333px, calc((100vw - 162px) / 3)'
            elif is_profile:sizes='(max-width:760px) calc(100vw - 34px), '+('520px' if homepage else '360px')
            else:sizes='(max-width:760px) calc(100vw - 34px), (max-width:1100px) calc(100vw - 90px), 960px'
            tag=set_attr(tag,'sizes',sizes)
        tag=set_attr(tag,'data-full-src',full+'?v='+item['source_sha256'][:12])
        tag=set_attr(tag,'data-image-delivery','preview' if variants else 'original')
        if 'width' not in attrs:tag=set_attr(tag,'width',item['width'])
        if 'height' not in attrs:tag=set_attr(tag,'height',item['height'])
        tag=set_attr(tag,'decoding','async')
        if is_portrait and '/about' in '/'+route:tag=set_attr(tag,'loading','eager')
        else:tag=set_attr(tag,'loading','lazy')
        return tag
    content=TOKENS.sub(image,content)
    # Hidden gallery alternatives need no network request before they are opened.
    def hidden(match):
        opening,inside,closing=match.groups()
        if 'data-pr-image' not in inside:return match[0]
        def defer(image_match):
            tag=image_match[0];attrs={n:unescape(v) for n,_,v in ATTR.findall(tag)}
            if 'src' not in attrs:return tag
            tag=set_attr(tag,'data-preview-src',attrs['src'])
            for name in ('src','srcset','sizes'):tag=remove_attr(tag,name)
            return tag
        return opening+re.sub(r'<img\b[^>]*>',defer,inside,flags=re.I)+closing
    return re.sub(r'(<div\b[^>]*\bhidden\b[^>]*>)(.*?)(</div>)',hidden,content,flags=re.I|re.S)
