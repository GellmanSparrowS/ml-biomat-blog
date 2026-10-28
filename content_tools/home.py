"""Paired home pages and complete article collections are distinct destinations."""
from html import escape
from . import catalog


def render(items, categories, site, make_head, make_footer, write_file, site_ld):
    routes=[]
    for lang in ['zh','en']:
        en=lang=='en';home='/en/' if en else '/';collection='/articles/en/' if en else '/articles/'
        all_items=[p for p in items if p['lang']==lang]
        recent=sorted(all_items,key=lambda p:p.get('modified',p.get('date','')),reverse=True)[:6]
        title='Home' if en else '首页';description=site['description_'+lang]
        categories_url=catalog.category_url(lang=lang)
        heading='Categories' if en else '分类';latest='Recent articles' if en else '近期更新';all_label='View all →' if en else '查看全部 →'
        body=f'<section class="hero"><h1>ML-Biomat</h1><p class="subtitle">{escape(description)}</p></section>'
        body+=f'<section class="section-head"><h2>{heading}</h2><a class="view-all" href="{categories_url}">{all_label}</a></section>'
        body+=catalog.category_cards(items,categories,lang)
        body+=f'<section class="section-head"><h2>{latest}</h2><a class="view-all" href="{collection}">{all_label}</a></section>'
        body+=catalog.grid(recent,categories,show_category=True)
        alternatives=f'<link rel="alternate" hreflang="zh-CN" href="{site["base_url"]}/"><link rel="alternate" hreflang="en" href="{site["base_url"]}/en/">'
        page=make_head(title=title,desc=description,url=site['base_url']+home,lang='en' if en else 'zh-CN',ld=site_ld(),wide=True,
                       en_href='/en/',zh_href='/',alternates=alternatives)+body+make_footer(lang)
        write_file(home.lstrip('/')+'index.html',page);routes.append(home)
        if not en:
            # /zh/ remains a working Chinese homepage alias for existing language links.
            write_file('zh/index.html',page)
        label='Articles & tutorials' if en else '文章与教程'
        body=f'<header class="catalog-header"><h1>{label}</h1><p>{len(all_items)} '+('articles' if en else '篇')+'</p></header>'
        body+=catalog.category_cards(items,categories,lang)+catalog.grid(all_items,categories,show_category=True)
        alts=f'<link rel="alternate" hreflang="zh-CN" href="{site["base_url"]}/articles/"><link rel="alternate" hreflang="en" href="{site["base_url"]}/articles/en/">'
        page=make_head(title=label,desc=description,url=site['base_url']+collection,lang='en' if en else 'zh-CN',wide=True,
                       en_href='/articles/en/',zh_href='/articles/',alternates=alts)+body+make_footer(lang)
        write_file(collection.lstrip('/')+'index.html',page);routes.append(collection)
    return routes
