"""Research homepage and topic catalog compositions."""
from html import escape as e
from pathlib import Path
import re
from content_tools import catalog

ICONS={
'machine-learning':'<path d="M8 9 22 5 34 16 23 31 8 25 8 9 23 31M8 9 34 16 8 25 22 5"/><circle cx="8" cy="9" r="2"/><circle cx="22" cy="5" r="2"/><circle cx="34" cy="16" r="2"/><circle cx="23" cy="31" r="2"/><circle cx="8" cy="25" r="2"/>',
'multiscale-modeling':'<rect x="4" y="4" width="29" height="29" rx="2"/><rect x="12" y="12" width="21" height="21" rx="2"/><rect x="21" y="21" width="12" height="12" rx="2"/>',
'biomaterials':'<path d="M4 5C28 4 8 30 34 31M3 16C28 4 13 34 34 20M4 30C8 5 25 32 32 5M15 3C5 27 37 10 24 35"/>',
'python-tutorials':'<path d="m12 8-8 11 8 11M27 8l8 11-8 11M24 5l-9 29"/>',
'wet-lab-data':'<path d="M5 4v29h30M8 28c8 0 6-20 14-20s5 16 13 5"/><circle cx="22" cy="8" r="2"/>'}

def icon(key):return '<svg class="topic-icon" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+ICONS.get(key,ICONS['biomaterials'])+'</svg>'
def active_topics(items,categories,lang):
    return [(k,v,sum(i['lang']==lang and i['category']==k for i in items)) for k,v in categories.items() if any(i['lang']==lang and i['category']==k for i in items)]
def paper_card(profile,key,venue,title,summary):
    image='paper-nc-2026.webp' if key=='nc' else 'paper-as-2025.webp'
    return f'<article class="home-work"><a href="{profile}#paper-{key}"><figure><img src="/static/images/profile/{image}" alt="{e(venue)}" loading="lazy"></figure><div class="home-work-copy"><p class="home-venue">{venue}</p><h3>{title}</h3><p class="site-prose">{summary}</p></div></a></article>'

def home_activities(en=False):
    lang='en' if en else 'zh-CN'
    profile='/about/en/' if en else '/about/'
    source=(Path(__file__).resolve().parents[1]/'content'/('about-en-body.html' if en else 'about-body.html')).read_text(encoding='utf8')
    section=re.search(r'<section\b[^>]*\bid="activities"[^>]*>.*?</section>',source,re.S)
    dialog=re.search(r'<dialog\b[^>]*class="pr-viewer"[^>]*>.*?</dialog>',source,re.S)
    assert section and dialog,'Profile activity and gallery markup required'
    content=re.sub(r'(<h2 id="activities-title">)(.*?)(</h2>)',lambda m:m[1]+'<a href="'+profile+'#activities">'+m[2]+'</a>'+m[3],section[0])
    return '<section class="profile-redesign home-activity-section" lang="'+lang+'">'+content+dialog[0]+'</section>'

def homepage(items,categories,en=False):
    lang='en' if en else 'zh';profile='/about/en/' if en else '/about/';cats=catalog.category_url(lang=lang)
    identity='Yunhao Yang · Fudan University' if en else '杨云浩 · 复旦大学'
    heading='Rational design of biomaterial systems and structures across scales' if en else '跨尺度生物材料体系与结构的理性设计'
    desc='Physics-informed artificial intelligence and multiscale simulation.' if en else '主要研究方向为物理人工智能与多尺度模拟。'
    body=f'<section class="home-intro"><div class="home-intro-copy"><p class="home-identity">{identity}</p><h1>{heading}</h1><p class="home-description site-prose">{desc}</p><div class="home-links"><a href="{profile}">{"Research profile" if en else "个人主页"} ↗</a><a href="{cats}">{"Research tutorials" if en else "研究教程"} →</a><a href="/fibernet/{"en/" if en else ""}">FiberNet →</a></div></div><div class="home-scene"><canvas class="fn-scene-canvas" aria-hidden="true"></canvas></div></section>'
    body+=f'<section class="preview-section home-research"><div class="preview-section-head"><h2>{"Selected research" if en else "代表研究"}</h2><a href="{profile}#publications">{"Publications" if en else "论文与成果"} ↗</a></div><div class="home-work-grid">'
    body+=paper_card(profile,'nc','Nature Communications · 2026','Manufacturability-informed design of fibrous networks' if en else '可制造纤维网络的智能设计','Connecting continuous fiber paths, topology generation and mechanics to guide the design of printable network materials.' if en else '将连续纤维路径、拓扑生成与力学分析结合，让结构设计与实际制造相衔接。')
    body+=paper_card(profile,'as','Advanced Science · 2025','Lightweight three-dimensional fibrous networks' if en else '轻量高强三维无序纤维网络','Deep reinforcement learning for the design of biomimetic three-dimensional fibrous networks.' if en else '通过深度强化学习优化仿生三维无序纤维网络，研究结构组织与轻量高强性能之间的关系。')
    body+='</div></section>'
    body+=f'<section class="preview-section home-learning"><div class="preview-section-head"><h2>{"Research tutorials" if en else "研究教程"}</h2><a href="{cats}">{"Browse topics" if en else "全部分类"} ↗</a></div><div class="home-learning-layout"><nav class="home-topic-index" aria-label="{"Topics" if en else "主题"}">'
    for key,info,count in active_topics(items,categories,lang):
        body+=f'<a href="{catalog.category_url(key,lang)}" data-color="{key}">{icon(key)}<span>{e(info["name_"+lang])}</span><small>{count}</small><span class="topic-arrow" aria-hidden="true">↗</span></a>'
    body+='</nav><div class="home-lesson-picks">'
    pick_slugs=['biomaterials-cp09-en','ml-predict-fiber-mechanics','python-env-setup'] if en else ['biomaterials-cp09','19-selecting-the-next-experiment','python-env-setup-zh']
    selected=[]
    for slug in pick_slugs:
        match=next((i for i in items if i['lang']==lang and i['slug']==slug),None)
        if match:selected.append(match)
    if len(selected)<3:selected+=[i for i in items if i['lang']==lang and i not in selected][:3-len(selected)]
    for item in selected:
        body+=f'<a class="home-lesson" href="{item["url"]}"><h3>{e(item["title"])}</h3><p>{e(item["description"])}</p><span aria-hidden="true">↗</span></a>'
    body+='</div></div></section>'
    body+=home_activities(en)
    return body


def collection(items,categories,en=False,topic=None,full=False):
    lang='en' if en else 'zh';topics=active_topics(items,categories,lang)
    selected=[i for i in items if i['lang']==lang and (topic is None or i['category']==topic)]
    title=categories[topic]['name_'+lang] if topic else ('Research tutorials' if en else '研究教程')
    description=categories[topic].get('description_'+lang,'') if topic else ''
    mode='overview' if not topic and not full else 'articles'
    all_label=('All articles' if en else '全部教程') if full else ('All topics' if en else '全部主题')
    total=(f'<span class="topic-total">{len(selected)} '+('articles' if en else '篇')+'</span>') if topic else ''
    body=f'<header class="explore-header"><h1>{e(title)}{total}</h1>'+(f'<p>{e(description)}</p>' if description else '')+'</header>'
    active=f' data-active-topic="{topic}"' if topic else ''
    body+=f'<div class="explore-layout" data-explore-mode="{mode}"{active}><aside class="topic-sidebar"><nav class="topic-filters" aria-label="{"Topics" if en else "主题分类"}">'
    if topic:body+=f'<a href="{catalog.category_url(lang=lang)}">{all_label}</a>'
    else:body+=f'<button type="button" data-topic-filter="all" aria-pressed="true" data-title="{all_label}"><span>{all_label}</span><small>{len(selected)}</small></button>'
    for key,info,count in topics:
        label=e(info['name_'+lang]);inner=icon(key)+f'<span>{label}</span><small>{count}</small>'
        if topic:body+=f'<a href="{catalog.category_url(key,lang)}" data-color="{key}"'+(' aria-current="page"' if topic==key else '')+f'>{inner}</a>'
        else:body+=f'<button type="button" data-topic-filter="{key}" data-title="{label}" data-color="{key}" aria-pressed="false">{inner}</button>'
    body+='</nav><select class="topic-select" aria-label="'+('Topic' if en else '选择主题')+'"'+(' data-topic-navigation' if topic else ' data-topic-selection')+'>'
    all_value=catalog.category_url(lang=lang) if topic else 'all'
    body+=f'<option value="{all_value}">{all_label}</option>'
    for key,info,count in topics:
        value=catalog.category_url(key,lang) if topic else key
        body+=f'<option value="{value}"'+(' selected' if topic==key else '')+f'>{e(info["name_"+lang])} · {count}</option>'
    body+='</select></aside><div class="explore-content">'
    if mode=='overview':
        body+='<div class="topic-overview">'
        for key,info,count in topics:
            examples=[i for i in selected if i['category']==key][:2]
            body+=f'<section class="topic-overview-card" data-color="{key}"><a class="topic-cover" href="{catalog.category_url(key,lang)}">{icon(key)}<h2>{e(info["name_"+lang])}</h2><span>{count} {"articles" if en else "篇"}</span><p>{e(info.get("description_"+lang,""))}</p><b aria-hidden="true">↗</b></a><div class="topic-examples">'
            for item in examples:body+=f'<a href="{item["url"]}">{e(item["title"])}</a>'
            body+='</div></section>'
        body+='</div>'
    body+='<div class="explore-results"'+(' hidden' if mode=='overview' else '')+'>'
    if not topic:body+='<div class="explore-results-head"><h2 data-results-title>'+e(all_label)+'</h2><span data-results-count>'+str(len(selected))+'</span></div>'
    body+='<div class="explore-list">'
    for item in sorted(selected,key=lambda i:(list(categories).index(i['category']),i['title'].casefold())):
        category=e(categories[item['category']]['name_'+lang]);title=e(item['title'])
        body+=f'<article class="explore-row tutorial-card" data-topic="{item["category"]}"><a class="tutorial-card-main" href="{item["url"]}"><span class="topic-name">{category}</span><h2>{title}</h2><p>{e(item["description"])}</p><span class="tutorial-arrow" aria-hidden="true">↗</span></a></article>'
    body+='</div></div>'
    if mode=='overview':body+=f'<a class="all-tutorials-link" href="/articles/{"en/" if en else ""}">{"All research tutorials" if en else "全部研究教程"} <span aria-hidden="true">↗</span></a>'
    return body+'</div></div>'
