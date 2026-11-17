"""Bilingual experimental-methods tutorials integrated with the shared site."""
from __future__ import annotations
from html import escape, unescape
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content/tutorials/experimental-methods'
BASE = '/tutorials/experimental-methods/'
DATE = '2026-11-17'
# Enable after these course routes are deployed to the payment verifier.
PAYPAL_ENABLED = False


def route(identifier, lang='zh'):
    return BASE + identifier.lower() + '/' + ('en/' if lang == 'en' else '')


def load():
    data=json.loads((CONTENT/'manifest.json').read_text(encoding='utf-8-sig'))
    assert len(data['lessons']) == 51
    assert len({item['id'] for item in data['lessons']}) == 51
    return data


def entries(data):
    result=[]
    for index,item in enumerate(data['lessons']):
        for lang in ['zh','en']:
            result.append({'title':item['title'][lang], 'description':item['standfirst'][lang],
                           'category':item['category'], 'categories':[item['category']],
                           'tags':[item['group'][lang]], 'lang':lang, 'date':DATE,
                           'slug':'experimental-methods-'+item['id'].lower()+('-en' if lang=='en' else ''),
                           'url':route(item['id'],lang), 'type':'tutorial', 'tutorial_order':index})
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
            source_body=(CONTENT/(item['id'].lower()+'-'+lang+'.html')).read_text(encoding='utf-8')
            first_paragraph=re.search(r'<p\b[^>]*>(.*?)</p>',source_body,re.S)
            opening=unescape(re.sub(r'<[^>]+>','',first_paragraph[1])) if first_paragraph else description
            opening=' '.join(opening.split())
            limit=155 if en else 85
            search_description=opening if len(opening)<=limit else (opening[:limit].rsplit(' ',1)[0]+'…' if en else opening[:limit]+'…')
            alternates=''.join(f'<link rel="alternate" hreflang="{code}" href="{base_url+route(item["id"],key)}">' for code,key in [('zh-CN','zh'),('en','en')])
            metadata={'@context':'https://schema.org','@type':'LearningResource','name':title,
                      'description':search_description,'url':base_url+address,'inLanguage':'en' if en else 'zh-CN',
                      'learningResourceType':'Tutorial','author':{'@type':'Person','name':'Yunhao Yang'}}
            search_title=title if len(title)<=70 else item['search_title'][lang]
            head=make_head(title=search_title,desc=search_description,title_suffix=" — ML-Biomat" if len(search_title)<=58 else "",url=base_url+address,lang='en' if en else 'zh-CN',wide=True,
                           ld='<script type="application/ld+json">'+json.dumps(metadata,ensure_ascii=False)+'</script>',
                           en_href=route(item['id'],'en'),zh_href=route(item['id'],'zh'),
                           navigation_language=lang,alternates=alternates)
            head=head.replace('<main class="container container-wide">','<main class="container biomat-container">')
            head=re.sub(r'<script\b[^>]*src="[^\"]*(?:highlightjs|adsbygoogle)[^\"]*"[^>]*>.*?</script>','',head,flags=re.S)
            head=re.sub(r'<link\b[^>]*href="[^\"]*highlightjs[^\"]*"[^>]*>','',head)
            head=head.replace('</head>','<link rel="stylesheet" href="'+versioned_asset('/static/css/biomaterials-courses.css')+'"></head>')
            head=head.replace('</head>','<link rel="stylesheet" href="'+versioned_asset('/static/css/python-scientific.css')+'"></head>')
            links=''.join('<a href="#'+s['id']+'">'+escape(s['title'][lang])+'</a>' for s in item['sections'])
            toc_title='Contents' if en else '本页目录'
            crumb='<nav class="bc-crumb" aria-label="'+('Breadcrumb' if en else '当前位置')+'"><a href="'+catalog+'">'+('Tutorials' if en else '教程')+'</a><span aria-hidden="true">/</span><a href="'+topic+'">'+escape(category_name)+'</a></nav>'
            intro='<header class="bc-hero"><h1>'+escape(title)+'</h1><p>'+escape(description)+'</p></header>'
            toc='<aside class="bc-toc"><details open><summary>'+toc_title+'</summary><nav aria-label="'+toc_title+'">'+links+'</nav></details></aside>'
            body=(CONTENT/(item['id'].lower()+'-'+lang+'.html')).read_text(encoding='utf-8')
            article='<article class="language-pane python-article" data-lang="'+lang+'" lang="'+('en' if en else 'zh-CN')+'">'+body+'</article>'
            neighbors=[]
            for key in ['prev','next']:
                if item['neighbors'].get(key) in by_id:
                    other=by_id[item['neighbors'][key]]
                    neighbors.append('<a rel="'+key+'" href="'+route(other['id'],lang)+'">'+escape(other['title'][lang])+'</a>')
            related=('<nav class="bc-related" aria-label="'+('Related tutorials' if en else '相关教程')+'">'+''.join(neighbors)+'</nav>') if neighbors else ''
            body='<div class="biomat-course python-course experimental-course" data-course="'+item['id']+'" data-lang="'+lang+'">'+crumb+'<div class="bc-layout">'+toc+'<div class="bc-main">'+intro+article+related+'</div></div></div>'
            dependencies=''.join('<script src="'+versioned_asset('/static/tutorials/experimental-methods/'+dependency)+'" defer></script>' for dependency in item.get('scripts',[]))
            scripts=dependencies+'<script src="'+versioned_asset('/static/tutorials/experimental-methods/'+item['id'].lower()+'.js')+'" defer></script><script src="'+versioned_asset('/static/js/biomaterials-courses.js')+'" defer></script><script src="'+versioned_asset('/static/js/python-scientific.js')+'" defer></script>'
            footer=make_footer(lang, article_support=True)
            if not PAYPAL_ENABLED:
                footer=re.sub(r'<a\b[^>]*class="support-paypal"[^>]*>.*?</a>', '', footer, flags=re.S)
            page=head+body+footer
            page=page.replace('</body>',scripts+'</body>')
            write_file(address.lstrip('/')+'index.html',page)
            routes.append(address)
    print('  Experimental methods: 51 bilingual lessons / 102 topic-integrated pages')
    return routes
