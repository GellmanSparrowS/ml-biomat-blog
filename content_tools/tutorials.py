"""Render topic-based tutorial articles while retaining their published URLs."""
from __future__ import annotations
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content/tutorials/polymer-ai'
BASE = '/tutorials/polymer-ai/'
DOWNLOAD = '/static/tutorials/polymer-ai/polymer-ai-notebooks.zip'
DATE = '2026-10-28'


def load():
    data = json.loads((CONTENT/'manifest.json').read_text(encoding='utf-8-sig'))
    assert [p['number'] for p in data['lessons']] == list(range(1,21))
    assert len({p['slug'] for p in data['lessons']}) == 20
    for lesson in data['lessons']:
        lesson['url'] = BASE + lesson['slug'] + '/'
    return data


def contextual_links(body, lesson, lessons):
    """Replace sequence-only prose references with article names; keep code and data exact."""
    chunks = re.split(r'(<script\b.*?</script>|<pre\b.*?</pre>|<style\b.*?</style>|<svg\b.*?</svg>|<code\b.*?</code>)', body, flags=re.S)
    by_number={p['number']:p for p in lessons}
    def ref(number):
        item=by_number.get(number)
        return f'<a href="{item["url"]}">《{html.escape(item["title"])}》</a>' if item else None
    for index in range(0,len(chunks),2):
        segments=re.split(r'(<[^>]+>)',chunks[index])
        in_link=False
        for j,segment in enumerate(segments):
            if segment.startswith('<a '): in_link=True
            elif segment.startswith('</a'): in_link=False
            if segment.startswith('<') or in_link: continue
            segment=re.sub(r'第\s*(\d{1,2})\s*节',lambda m:ref(int(m[1])) or m[0],segment)
            for text,number in [('下一节',lesson['number']+1),('上一节',lesson['number']-1),('前一节',lesson['number']-1)]:
                if ref(number): segment=segment.replace(text,ref(number))
            segments[j]=segment
        chunks[index]=''.join(segments)
    return ''.join(chunks)


def render(data, make_head, make_footer, write_file, versioned_asset, categories, posts, base_url):
    # Existing bookmarks enter the topic catalog; there is no separate course directory.
    for route in ['/tutorials/',BASE]:
        alias='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>分类 — ML-Biomat</title><link rel="canonical" href="'+base_url+'/categories/"><meta http-equiv="refresh" content="0; url=/categories/"></head><body><a href="/categories/">浏览分类</a></body></html>'
        write_file(route.lstrip('/')+'index.html',alias)

    for lesson in data['lessons']:
        primary=lesson['categories'][0]
        category_name=html.escape(categories[primary]['name_zh'])
        category_url='/categories/'+primary+'/'
        metadata={'@context':'https://schema.org','@type':'LearningResource','name':lesson['title'],
                  'description':lesson['description'],'url':base_url+lesson['url'],'inLanguage':'zh-CN',
                  'learningResourceType':'Tutorial','author':{'@type':'Person','name':'Yunhao Yang'}}
        head=make_head(title=lesson['title'],desc=lesson['description'],url=base_url+lesson['url'],lang='zh-CN',wide=True,
                       ld='<script type="application/ld+json">'+json.dumps(metadata,ensure_ascii=False)+'</script>')
        head=head.replace('<main class="container container-wide">','<main class="container tutorial-container">')
        # Chinese-only articles have no equivalent translation link.
        head=re.sub(r'<span class="lang-switch">.*?</span>','',head)
        head=re.sub(r'<(?:script|link)\b[^>]*(?:highlightjs|adsbygoogle)[^>]*>(?:</script>)?','',head)
        shared=f'<link rel="stylesheet" href="{versioned_asset("/static/css/tutorials.css")}">'
        own=f'<link rel="stylesheet" href="{versioned_asset("/static/tutorials/polymer-ai/lesson-%02d.css"%lesson["number"])}">'
        head=head.replace(shared,own+shared)
        body=(CONTENT/f'{lesson["number"]:02d}.html').read_text(encoding='utf-8')
        body=re.sub(r'<p class="eyebrow">第\s*\d+\s*节\s*·\s*(.*?)</p>',r'<p class="eyebrow">\1</p>',body,count=1)
        body=re.sub(r'<h1>.*?</h1>','<h1>'+html.escape(lesson['title'])+'</h1>',body,count=1,flags=re.S)
        body=re.sub(r'<p class="lesson-label">.*?</p>',f'<p class="lesson-label">{category_name}</p>',body,count=1,flags=re.S)
        body=re.sub(r'(<aside\b[^>]*>)(.*?)(</aside>)',r'\1<details class="lesson-toc" open><summary>本页目录</summary>\2</details>\3',body,count=1,flags=re.S)
        body=body.replace('aria-label="本节阅读路线"','aria-label="本页目录"')
        body=contextual_links(body,lesson,data['lessons'])
        toolbar=f'<div class="tutorial-toolbar"><nav class="tutorial-crumb" aria-label="当前位置"><a href="/categories/">分类</a><span aria-hidden="true">/</span><a href="{category_url}">{category_name}</a></nav><div><button type="button" id="font-toggle" aria-pressed="false">放大正文</button><a class="tutorial-download" href="{DOWNLOAD}" download>下载代码合集 ↓</a></div></div>'
        related=sorted([p for p in data['lessons'] if p['number']!=lesson['number'] and p['group']==lesson['group']],key=lambda p:abs(p['number']-lesson['number']))[:2]
        links=''.join(f'<a href="{p["url"]}"><strong>{html.escape(p["title"])}</strong></a>' for p in related)
        neighbors='<section class="tutorial-related"><h2>相关阅读</h2><nav class="tutorial-neighbors" aria-label="相关阅读">'+links+'</nav></section>'
        scripts=[]
        def collect(match):
            attrs,content=match.group(1,2)
            if 'application/json' in attrs: return match.group()
            scripts.append(match.group());return ''
        body=re.sub(r'<script\b([^>]*)>(.*?)</script>',collect,body,flags=re.S)
        document=head+toolbar+'<div class="tutorial-reader">'+body+'</div>'+neighbors+make_footer()
        document=document.replace('</body>',''.join(scripts)+'</body>')
        write_file(lesson['url'].lstrip('/')+'index.html',document)
    print('  Tutorials: 20 complete articles integrated into topic categories')
