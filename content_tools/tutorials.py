"""Render the polymer tutorial series within the shared ML-Biomat site shell."""
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


def listing(lessons, categories, filtered=False):
    result = '<ol class="tutorial-list">'
    for item in lessons:
        title=html.escape(item['title']);desc=html.escape(item['description'])
        topics=' · '.join(categories[c]['name_zh'] for c in item['categories'])
        search=' '.join([item['title'],item['description'],*item['tags'],topics])
        attrs=f' data-tutorial-item data-search="{html.escape(search,quote=True)}" data-categories="{" ".join(item["categories"])}"' if filtered else ''
        result += f'<li{attrs}><a href="{item["url"]}"><span class="tutorial-number">{item["number"]:02d}</span><div><h3>{title}</h3><p>{desc}</p><span class="tutorial-topics">{html.escape(topics)}</span></div></a></li>'
    return result+'</ol>'


def feature(data):
    return f'''<section class="tutorial-feature"><div><small>系列教程 · 20 节</small><h2><a href="{BASE}">{html.escape(data['title'])}</a></h2><p>从分子与构象到网络、实验数据和 AI 设计，结合交互图解与 Python 计算逐步学习。</p></div><a class="tutorial-feature-link" href="{BASE}">查看教程 <span aria-hidden="true">→</span></a></section>'''


def category_section(data, category, categories):
    lessons=[p for p in data['lessons'] if category in p['categories']]
    if not lessons: return ''
    return '<section class="tutorial-category"><h2>系列教程</h2><p><a href="'+BASE+'">高分子与生物大分子 · 完整阅读路线 →</a></p>'+listing(lessons,categories)+'</section>'


def render(data, make_head, make_footer, write_file, versioned_asset, categories, posts, base_url):
    def head(title, description, route, lesson=None):
        metadata={'@context':'https://schema.org','@type':'LearningResource','name':title,
                  'description':description,'url':base_url+route,'inLanguage':'zh-CN',
                  'learningResourceType':'Tutorial','author':{'@type':'Person','name':'Yunhao Yang'}}
        value=make_head(title=title,desc=description,url=base_url+route,lang='zh-CN',wide=True,
                        ld='<script type="application/ld+json">'+json.dumps(metadata,ensure_ascii=False)+'</script>')
        value=value.replace('<main class="container container-wide">','<main class="container tutorial-container">')
        value=value.replace('href="/tutorials/">Tutorials / 教程','href="/tutorials/" class="active">Tutorials / 教程')
        # This series currently has Chinese lessons; do not imply paired translations.
        value=re.sub(r'<span class="lang-switch">.*?</span>','',value)
        value=re.sub(r'<(?:script|link)\b[^>]*(?:highlightjs|adsbygoogle)[^>]*>(?:</script>)?','',value)
        styles=''
        if lesson:
            styles+=f'<link rel="stylesheet" href="{versioned_asset("/static/tutorials/polymer-ai/lesson-%02d.css"%lesson["number"])}">'
        shared=f'<link rel="stylesheet" href="{versioned_asset("/static/css/tutorials.css")}">'
        return value.replace(shared,styles+shared)

    filters='<div class="tutorial-filter"><label class="tutorial-search-label" for="tutorial-search">查找教程</label><input id="tutorial-search" type="search" placeholder="搜索内容、材料或方法" autocomplete="off"><div class="tutorial-filter-buttons" aria-label="按主题筛选"><button type="button" data-tutorial-filter="all" aria-pressed="true" class="active">全部</button>'
    for key, value in categories.items():
        if any(key in p['categories'] for p in data['lessons']):
            filters+=f'<button type="button" data-tutorial-filter="{key}" aria-pressed="false">{html.escape(value["name_zh"])}</button>'
    filters+='</div><p id="tutorial-count" role="status" aria-live="polite">20 节教程</p></div>'
    hub=f'''<div class="tutorial-hub"><header class="tutorial-hero"><p class="tutorial-kicker">ML-BIOMAT · 系列教程</p><h1>高分子与生物大分子<br><span>计算与 AI 实践</span></h1><p>{html.escape(data['description'])}</p><div class="tutorial-actions"><a href="{data['lessons'][0]['url']}">从第 1 节开始 →</a><a href="{DOWNLOAD}" download>下载 Notebook 与代码 ↓</a></div></header>{filters}'''
    for i,group in enumerate(data['groups'],1):
        lessons=[p for p in data['lessons'] if p['group']==group['id']]
        hub+=f'<section class="tutorial-group" data-tutorial-group="{group["id"]}" id="{group["id"]}"><div class="tutorial-group-heading"><small>{i:02d} / 第 {lessons[0]["number"]}–{lessons[-1]["number"]} 节</small><h2>{html.escape(group["title"])}</h2><p>{html.escape(group["description"])}</p></div>'+listing(lessons,categories,True)+'</section>'
    hub+='<p class="tutorial-empty" id="tutorial-empty" hidden>没有找到匹配的教程，试试其他关键词或分类。</p><section class="tutorial-related"><h2>继续阅读</h2><a href="/zh/">全部中文研究笔记 →</a><a href="/categories/">按主题浏览文章 →</a><a href="/fibernet/">FiberNet 研究工具 →</a></section></div>'
    hub+=f'<script src="{versioned_asset("/static/js/tutorials.js")}" defer></script>'
    write_file('tutorials/polymer-ai/index.html',head(data['title'],data['description'],BASE)+hub+make_footer())
    # The main tutorial directory also presents existing topic collections.
    intro='<div class="tutorial-hub"><header class="tutorial-hero"><p class="tutorial-kicker">ML-BIOMAT · TUTORIALS</p><h1>教程与计算实践</h1><p>从科学问题出发，结合图解、模型和代码，理解生物材料的结构与行为。</p></header>'+feature(data)
    intro+='<section class="tutorial-related"><h2>按主题学习</h2>'
    for key,value in categories.items():
        if any(p['category']==key for p in posts):
            intro+=f'<a href="/categories/{key}/">{html.escape(value["name_zh"])} →</a>'
    intro+='</section></div>'
    write_file('tutorials/index.html',head('教程与计算实践','ML-Biomat 系列教程：高分子与生物大分子、机器学习、多尺度模拟、Python 与实验数据处理。','/tutorials/')+intro+make_footer())

    for i,lesson in enumerate(data['lessons']):
        body=(CONTENT/f'{lesson["number"]:02d}.html').read_text(encoding='utf-8')
        toolbar=f'''<div class="tutorial-toolbar"><nav class="tutorial-crumb" aria-label="当前位置"><a href="/tutorials/">教程</a><span aria-hidden="true">/</span><a href="{BASE}">高分子与生物大分子</a><span aria-hidden="true">/</span><span>第 {lesson['number']:02d} 节</span></nav><div><button type="button" id="font-toggle" aria-pressed="false">放大正文</button><a class="tutorial-download" href="{DOWNLOAD}" download>配套代码 ↓</a></div></div>'''
        links=[]
        if i:
            prev=data['lessons'][i-1]
            links.append(f'<a href="{prev["url"]}" rel="prev"><small>← 上一节</small><strong>{html.escape(prev["title"])}</strong></a>')
        else: links.append(f'<a href="{BASE}"><small>阅读路线</small><strong>全部 20 节教程</strong></a>')
        if i+1<len(data['lessons']):
            following=data['lessons'][i+1]
            links.append(f'<a href="{following["url"]}" rel="next"><small>下一节 →</small><strong>{html.escape(following["title"])}</strong></a>')
        else: links.append(f'<a href="{BASE}"><small>回到目录</small><strong>全部 20 节教程</strong></a>')
        neighbors='<nav class="tutorial-neighbors" aria-label="教程顺序">'+''.join(links)+'</nav>'
        # Footer progress control is available before the lesson scripts execute.
        scripts=[]
        def collect(match):
            attrs,content=match.group(1,2)
            if 'application/json' in attrs: return match.group()
            scripts.append(match.group());return ''
        body=re.sub(r'<script\b([^>]*)>(.*?)</script>',collect,body,flags=re.S)
        document=head(lesson['title'],lesson['description'],lesson['url'],lesson)+toolbar+'<div class="tutorial-reader">'+body+'</div>'+neighbors+make_footer()
        document=document.replace('</body>',''.join(scripts)+'</body>')
        write_file(lesson['url'].lstrip('/')+'index.html',document)
    print('  Tutorials: 20 lessons, 5 reading groups, shared site navigation')
