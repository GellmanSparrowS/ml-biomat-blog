"""Shared navigation, locale destinations, and dark-first theme bootstrap."""
from html import escape

THEME_INIT = '''<script>(function(){var theme='dark';try{var saved=localStorage.getItem('ml-biomat-theme');if(saved==='light'||saved==='dark')theme=saved;}catch(e){}document.documentElement.dataset.theme=theme;})();</script>'''
NAV = [('home','首页','Home'),('library','工具库','Library'),('categories','分类','Categories'),('profile','个人主页','Profile')]


def paths(language):
    en=language=='en'
    return {'home':'/en/' if en else '/', 'library':'/fibernet/en/' if en else '/fibernet/',
            'categories':'/categories/en/' if en else '/categories/', 'profile':'/about/en/' if en else '/about/'}


def section(route):
    route=route.strip('/')
    if route in ('','en','zh'):return 'home'
    if route.startswith(('about','cv')):return 'profile'
    if route.startswith(('fibernet','tools/')):return 'library'
    if route.startswith(('categories','posts/','articles','tags','tutorials')):return 'categories'
    return None


def header(language, route, en_href=None, zh_href=None, wide=False):
    language='en' if language=='en' else 'zh'
    en=language=='en'; destinations=paths(language);current=section(route)
    if route.strip('/') in ('','en','zh'):en_href='/en/';zh_href='/'
    if not en_href and en:en_href=route
    if not zh_href and not en:zh_href=route
    links=[]
    for key,zh_label,en_label in NAV:
        label=en_label if en else zh_label
        active=' class="active" aria-current="page"' if key==current else ''
        links.append(f'<a data-nav="{key}" data-short-label="{label}" href="{destinations[key]}"{active}>{label}</a>')
    switches=[]
    for code,label,address in [('en','EN',en_href),('zh','中文',zh_href)]:
        active=' class="active" aria-current="true"' if language==code else ''
        if address:
            switches.append(f'<a data-language="{code}" href="{escape(address,quote=True)}"{active}>{label}</a>')
        else:
            title='Translation not available' if en else '该页暂无英文版'
            switches.append(f'<a data-language="{code}" role="link" aria-disabled="true" tabindex="-1" title="{title}">{label}</a>')
    search='Search…' if en else '搜索…'
    theme='Switch to light mode' if en else '切换到亮色'
    navigation='Main navigation' if en else '主导航'
    return f'''<header class="site-header"><div class="header-inner">
<a href="{destinations['home']}" class="site-brand"><span class="site-logo">ML-Biomat<span class="dot">.</span></span></a>
<nav class="nav-links" aria-label="{navigation}">{''.join(links)}</nav>
<input type="search" id="search-input" class="search-input" placeholder="{search}" aria-label="{search}" autocomplete="off">
<button type="button" id="theme-toggle" class="theme-toggle" aria-label="{theme}" title="{theme}">☀</button>
<span class="lang-switch">{''.join(switches)}</span>
</div></header><main class="container{' container-wide' if wide else ''}">'''


def footer_links(language):
    en=language=='en';p=paths(language)
    links=[(p['profile'],'Profile' if en else '个人主页'),(p['library'],'Library' if en else '工具库'),
           (p['categories'],'Categories' if en else '分类'),('/rss.xml','RSS'),
           ('/tools/stress-strain/'+('en/' if en else ''),'Tools' if en else '交互工具'),
           ('/sitemap.xml','Sitemap' if en else '站点地图'),('/privacy/'+('en/' if en else ''),'Privacy' if en else '隐私政策')]
    return '<div class="footer-links">'+''.join(f'<a href="{url}">{label}</a>' for url,label in links)+'</div>'
