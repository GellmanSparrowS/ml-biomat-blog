"""Localized tag UI keeps the tag identity and all original article links."""
from html import escape
from urllib.parse import quote


# Only these existing tag pairs share the same identity. Other tag URLs retain
# their original casing (for example AFM, LAMMPS and NetworkX).
_MERGED_LABELS = {"python": "Python", "mamba": "Mamba"}


def canonical_slug(tag):
    key = tag.casefold()
    return key if key in _MERGED_LABELS else tag


def href(tag, language="zh"):
    return "/tags/" + quote(canonical_slug(tag), safe="") + "/" + ("en/" if language == "en" else "")


def grouped_posts(posts):
    groups = {}
    for post in posts:
        for tag in post['tags']:
            groups.setdefault(canonical_slug(tag), {})[post['slug']] = post
    return {slug: list(items.values()) for slug, items in groups.items()}


def render(posts,make_head,make_footer,write_file,base_url):
    groups=grouped_posts(posts)
    routes=[]
    for lang in ['zh','en']:
        en=lang=='en';suffix='en/' if en else '';label='Tags' if en else '标签'
        route='/tags/'+suffix
        body=f'<header class="catalog-header"><h1>{label}</h1></header><div class="tag-cloud">'
        for slug,items in sorted(groups.items(),key=lambda item:(-len(item[1]),item[0].casefold())):
            tag=_MERGED_LABELS.get(slug,slug)
            url=href(slug,lang)
            body+=f'<a class="tag-pill" href="{url}">{escape(tag)} ({len(items)})</a>'
        body+='</div>'
        description='Browse articles by topic and method.' if en else '按研究主题、材料与方法标签查找文章。'
        head=make_head(title=label,desc=description,url=base_url+route,lang='en' if en else 'zh-CN',en_href='/tags/en/',zh_href='/tags/')
        write_file(route.lstrip('/')+'index.html',head+body+make_footer(lang));routes.append(route)
        for slug,items in groups.items():
            tag=_MERGED_LABELS.get(slug,slug)
            base=href(slug)
            body=f'<a class="catalog-breadcrumb" href="/tags/{suffix}">{label} /</a><header class="catalog-header"><h1><span class="highlight">{escape(tag)}</span></h1></header><ul class="post-list-simple">'
            for post in sorted(items,key=lambda p:p['datetime'],reverse=True):
                badge='EN' if post['lang']=='en' else '中文'
                body+=f'<li class="post-row"><span class="card-lang {post["lang"]}">{badge}</span><a lang="{post["lang"]}" href="/posts/{post["slug"]}/">{escape(post["title"])}</a></li>'
            body+='</ul>'
            page=make_head(title=tag+' — '+label,desc=description,url=base_url+base+suffix,lang='en' if en else 'zh-CN',en_href=base+'en/',zh_href=base)+body+make_footer(lang)
            write_file('tags/'+slug+'/'+suffix+'index.html',page)
    return routes
