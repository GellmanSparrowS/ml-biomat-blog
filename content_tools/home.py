"""Paired research homepages and separate tutorial collections."""
from . import catalog, site_layouts


def render(items, categories, site, make_head, make_footer, write_file, site_ld, versioned_asset):
    routes=[]
    for lang in ['zh','en']:
        en=lang=='en'; route='/en/' if en else '/'
        description=site['description_'+lang]
        body=site_layouts.homepage(items,categories,en=en)
        for script in ['fibernet-scene.js','profile-gallery.js']:
            body+='<script src="'+versioned_asset('/static/js/'+script)+'" defer></script>'
        alternatives=f'<link rel="alternate" hreflang="zh-CN" href="{site["base_url"]}/"><link rel="alternate" hreflang="en" href="{site["base_url"]}/en/">'
        page=make_head(title='Home' if en else '首页',desc=description,url=site['base_url']+route,lang='en' if en else 'zh-CN',ld=site_ld(),wide=True,
                       en_href='/en/',zh_href='/',alternates=alternatives)+body+make_footer(lang)
        write_file(route.lstrip('/')+'index.html',page);routes.append(route)
        if not en:write_file('zh/index.html',page)
        collection='/articles/en/' if en else '/articles/'
        label='Research tutorials' if en else '研究教程'
        body=site_layouts.collection(items,categories,en=en,full=True)
        alts=f'<link rel="alternate" hreflang="zh-CN" href="{site["base_url"]}/articles/"><link rel="alternate" hreflang="en" href="{site["base_url"]}/articles/en/">'
        page=make_head(title=label,desc=description,url=site['base_url']+collection,lang='en' if en else 'zh-CN',wide=True,
                       en_href='/articles/en/',zh_href='/articles/',alternates=alts)+body+make_footer(lang)
        write_file(collection.lstrip('/')+'index.html',page);routes.append(collection)
    return routes
