"""Bilingual illustrated biomaterials lessons integrated with the shared site."""
from __future__ import annotations
from html import escape
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content/tutorials/biomaterials-courses'
BASE = '/tutorials/biomaterials-courses/'
DATE = '2026-10-29'


def route(identifier, lang='zh'):
    return BASE + identifier.lower() + '/' + ('en/' if lang == 'en' else '')


def load():
    data=json.loads((CONTENT/'manifest.json').read_text(encoding='utf-8-sig'))
    assert len(data['lessons']) == 48
    assert len({item['id'] for item in data['lessons']}) == 48
    return data


def entries(data):
    result=[]
    labels={'BM':{'zh':'生物大分子','en':'Biomacromolecules'},
            'CP':{'zh':'高分子物理','en':'Polymer physics'},
            'PE':{'zh':'反应与加工','en':'Reaction and processing'},
            'PM':{'zh':'高分子材料','en':'Polymer materials'}}
    for item in data['lessons']:
        for lang in ['zh','en']:
            result.append({'title':item['title'][lang], 'description':item['standfirst'][lang],
                           'category':item['category'], 'categories':[item['category']],
                           'tags':[labels[item['group']][lang]], 'lang':lang, 'date':DATE,
                           'slug':'biomaterials-'+item['id'].lower()+('-en' if lang=='en' else ''),
                           'url':route(item['id'],lang), 'type':'tutorial'})
    return result


def render(data, make_head, make_footer, write_file, versioned_asset, categories, base_url):
    routes=[]
    by_id={item['id']:item for item in data['lessons']}
    for item in data['lessons']:
        for lang in ['zh','en']:
            en=lang=='en'; address=route(item['id'],lang)
            category=item['category']; category_name=categories[category]['name_'+lang]
            catalog='/categories/'+('en/' if en else '')
            topic='/categories/'+category+'/'+('en/' if en else '')
            title=item['title'][lang]; description=item['standfirst'][lang]
            alternates=''.join(f'<link rel="alternate" hreflang="{code}" href="{base_url+route(item["id"],key)}">' for code,key in [('zh-CN','zh'),('en','en')])
            metadata={'@context':'https://schema.org','@type':'LearningResource','name':title,
                      'description':description,'url':base_url+address,'inLanguage':'en' if en else 'zh-CN',
                      'learningResourceType':'Tutorial','author':{'@type':'Person','name':'Yunhao Yang'}}
            head=make_head(title=title,desc=description,url=base_url+address,lang='en' if en else 'zh-CN',wide=True,
                           ld='<script type="application/ld+json">'+json.dumps(metadata,ensure_ascii=False)+'</script>',
                           en_href=route(item['id'],'en'),zh_href=route(item['id'],'zh'),
                           navigation_language=lang,alternates=alternates)
            head=head.replace('<main class="container container-wide">','<main class="container biomat-container">')
            head=re.sub(r'<script\b[^>]*src="[^\"]*(?:highlightjs|adsbygoogle)[^\"]*"[^>]*>.*?</script>','',head,flags=re.S)
            head=re.sub(r'<link\b[^>]*href="[^\"]*highlightjs[^\"]*"[^>]*>','',head)
            head=head.replace('</head>','<link rel="stylesheet" href="'+versioned_asset('/static/css/biomaterials-courses.css')+'"></head>')
            links=''.join('<a href="#'+lang+'-'+s['id']+'">'+escape(s['title'][lang])+'</a>' for s in item['sections'])
            toc_title='Contents' if en else '本页目录'
            crumb='<nav class="bc-crumb" aria-label="'+('Breadcrumb' if en else '当前位置')+'"><a href="'+catalog+'">'+('Categories' if en else '分类')+'</a><span aria-hidden="true">/</span><a href="'+topic+'">'+escape(category_name)+'</a></nav>'
            intro='<header class="bc-hero"><h1>'+escape(title)+'</h1><p>'+escape(description)+'</p></header>'
            toc='<aside class="bc-toc"><details open><summary>'+toc_title+'</summary><nav aria-label="'+toc_title+'">'+links+'</nav></details></aside>'
            body=(CONTENT/(item['id'].lower()+'-'+lang+'.html')).read_text(encoding='utf-8')
            article='<article class="language-pane" data-lang="'+lang+'" lang="'+('en' if en else 'zh-CN')+'">'+body+'</article>'
            neighbors=[]
            for key in ['prev','next']:
                if item['neighbors'].get(key) in by_id:
                    other=by_id[item['neighbors'][key]]
                    neighbors.append('<a rel="'+key+'" href="'+route(other['id'],lang)+'">'+escape(other['title'][lang])+'</a>')
            related=('<nav class="bc-related" aria-label="'+('Related tutorials' if en else '相关教程')+'">'+''.join(neighbors)+'</nav>') if neighbors else ''
            body='<div class="biomat-course" data-course="'+item['id']+'" data-lang="'+lang+'">'+crumb+'<div class="bc-layout">'+toc+'<div class="bc-main">'+intro+article+related+'</div></div></div>'
            scripts='<script src="'+versioned_asset('/static/tutorials/biomaterials-courses/'+item['id'].lower()+'.js')+'" defer></script><script src="'+versioned_asset('/static/js/biomaterials-courses.js')+'" defer></script>'
            page=head+body+make_footer(lang)
            page=page.replace('</body>',scripts+'</body>')
            write_file(address.lstrip('/')+'index.html',page)
            routes.append(address)
    print('  Biomaterials: 48 illustrated bilingual lessons / 96 topic-integrated pages')
    return routes
