"""Topic-first catalog shared by original articles and interactive tutorials."""
from html import escape


def entries(posts, curriculum):
    result = [dict(p, url='/posts/'+p['slug']+'/', categories=[p['category']]) for p in posts]
    result += [dict(p, lang='zh', category=p['categories'][0], date='2026-10-28') for p in curriculum['lessons']]
    return result


def category_url(slug='', lang='zh'):
    return '/categories/' + (slug+'/' if slug else '') + ('en/' if lang=='en' else '')


def card(item, categories, show_category=False):
    lang=item['lang']; title=escape(item['title']); desc=escape(item['description'])
    meta=''
    if show_category:
        cat=item['categories'][0]
        meta=f'<a href="{category_url(cat,lang)}">{escape(categories[cat]["name_"+lang])}</a>'
    return f'<article class="catalog-card"><h2><a href="{item["url"]}">{title}</a></h2><p>{desc}</p>'+ (f'<div class="catalog-meta">{meta}</div>' if meta else '')+'</article>'


def grid(items, categories, show_category=False):
    return '<div class="catalog-grid">'+''.join(card(p,categories,show_category) for p in items)+'</div>'


def category_cards(items, categories, lang='zh', bilingual=False):
    result='<div class="post-grid">'
    for slug,info in categories.items():
        count=sum(p['lang']==lang and slug in p['categories'] for p in items)
        if not count: continue
        other=sum(p['lang']!=lang and slug in p['categories'] for p in items)
        name=escape(info['name_'+lang]); hint=escape(info['name_en']) if bilingual else ''
        description=escape(info.get('description_'+lang,''))
        label=(f'{count} 篇 · {other} English' if bilingual else f'{count} 篇' if lang=='zh' else f'{count} articles')
        result+=f'<a class="post-card catalog-category" href="{category_url(slug,lang)}">'+(f'<span class="card-meta">{hint}</span>' if hint else '')+f'<h3>{name}</h3><p class="catalog-scope">{description}</p><span class="card-meta">{label}</span></a>'
    return result+'</div>'


def render(items, categories, make_head, make_footer, write_file, base_url):
    from . import site_layouts
    routes=[]
    for lang in ['zh','en']:
        desc='按研究主题浏览图解、计算与实践。' if lang=='zh' else 'Explore explanations, calculations and practice by research topic.'
        for slug in ['',*[key for key in categories if any(p['lang']==lang and p['category']==key for p in items)]]:
            route=category_url(slug,lang)
            title=categories[slug]['name_'+lang] if slug else ('分类' if lang=='zh' else 'Categories')
            body=site_layouts.collection(items,categories,en=lang=='en',topic=slug or None)
            en=category_url(slug,'en');zh=category_url(slug,'zh')
            alts=f'<link rel="alternate" hreflang="en" href="{base_url+en}"><link rel="alternate" hreflang="zh-CN" href="{base_url+zh}">'
            head=make_head(title=title,desc=desc,url=base_url+route,lang='en' if lang=='en' else 'zh-CN',wide=True,
                           en_href=en,zh_href=zh,navigation_language=lang,alternates=alts)
            write_file(route.lstrip('/')+'index.html',head+body+make_footer(lang));routes.append(route)
    return routes
