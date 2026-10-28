"""Import the user-supplied polymer tutorial HTML without changing scientific assets.
One-time importer dependency: Playwright (Chromium). Site builds remain stdlib-only.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path
from urllib.parse import unquote
from html.parser import HTMLParser
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'content/tutorials/polymer-ai'
ASSETS = ROOT / 'static/tutorials/polymer-ai'
URL = '/static/tutorials/polymer-ai/'

class ProseAdapter(HTMLParser):
    """Edit prose text positions only; retain source markup, code, SVG and data verbatim."""
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.starts = [0] + [m.end() for m in re.finditer('\n', source)]
        self.protected = []
        self.edits = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'pre', 'code', 'svg', 'math'):
            self.protected.append(tag)
    def handle_endtag(self, tag):
        if self.protected and tag == self.protected[-1]:
            self.protected.pop()
    def handle_data(self, data):
        if self.protected: return
        changed = re.sub(r'9\.8\.(\d+)', lambda m: '第 ' + m[1] + ' 节', data)
        changed = changed.replace('本章', '本教程').replace('本书', '本系列教程')
        if changed != data:
            line, col = self.getpos()
            start = self.starts[line - 1] + col
            assert self.source[start:start+len(data)] == data
            self.edits.append((start, start + len(data), changed))
    def result(self):
        for start, end, value in reversed(self.edits):
            self.source = self.source[:start] + value + self.source[end:]
        return self.source

SCOPE_CSS = r'''css => {
 const sheet=new CSSStyleSheet();sheet.replaceSync(css);
 function selectors(value){let result=[],start=0,depth=0,quote='';
  for(let i=0;i<value.length;i++){const c=value[i];if(quote){if(c===quote&&value[i-1]!=='\\')quote='';continue;}if(c==='"'||c==="'"){quote=c;continue;}if(c==='('||c==='[')depth++;if(c===')'||c===']')depth--;if(c===','&&!depth){result.push(value.slice(start,i));start=i+1;}}
  result.push(value.slice(start));return result;
 }
 function scoped(selector){
  let s=selector.trim().replace(/:root\b/g,'.tutorial-reader').replace(/\b(?:html|body)\b/g,'.tutorial-reader').replace(/\bmain\b/g,'.lesson-main');
  return s.startsWith('.tutorial-reader')?s:'.tutorial-reader '+s;
 }
 function walk(rules){return [...rules].map(rule=>{
  if(rule.type===CSSRule.STYLE_RULE)return selectors(rule.selectorText).map(scoped).join(',')+'{'+rule.style.cssText+'}';
  if(rule.type===CSSRule.MEDIA_RULE)return '@media '+rule.conditionText+'{'+walk(rule.cssRules)+'}';
  throw Error('Unexpected CSS rule: '+rule.cssText.slice(0,60));
 }).join('\n');}
 return walk(sheet.cssRules);
}'''


def main(archive):
    manifest = json.loads((SOURCE / 'manifest.json').read_text(encoding='utf-8-sig'))
    SOURCE.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    unique = set()
    total_bytes = 0
    with zipfile.ZipFile(archive) as z, sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        sources = {int(re.search(r'(\d{2})_', n)[1]): n for n in z.namelist() if n.endswith('.html') and re.match(r'(?:样章|章节)\d{2}_', n)}
        routes = {sources[item['number']]: '/tutorials/polymer-ai/' + item['slug'] + '/' for item in manifest['lessons']}
        for item in manifest['lessons']:
            number = item['number']
            s = z.read(sources[number]).decode('utf-8-sig').replace('\r\r\n','\n').replace('\r\n','\n')
            css = '\n'.join(re.findall(r'<style\b[^>]*>(.*?)</style>', s, re.S))
            scoped = page.evaluate(SCOPE_CSS, css)
            (ASSETS / f'lesson-{number:02d}.css').write_text(scoped+'\n', encoding='utf-8')
            body = re.search(r'<body\b[^>]*>(.*?)</body>', s, re.S)[1]
            body = re.sub(r'<header\b[^>]*>.*?</header>', '', body, count=1, flags=re.S)
            body = re.sub(r'<footer\b[^>]*>.*?</footer>', '', body, flags=re.S)
            body = re.sub(r'<div class="next-reading">.*?</div>', '', body, flags=re.S)
            body = re.sub(r'<nav id="curriculum-neighbors".*?</nav>', '', body, flags=re.S)
            body = body.replace('<main id="main">', '<div class="lesson-main" id="main">').replace('</main>', '</div>')
            assert '<main' not in body
            byline = '<div class="byline">杨云浩 · 复旦大学 · 高分子与生物大分子教程</div>'
            if 'class="byline"' in body:
                body = re.sub(r'<div class="byline">.*?</div>', byline, body, flags=re.S)
            else:
                body = re.sub(r'(</h1>)',r'\1\n'+byline,body,count=1)
            body = body.replace('class="book-label"','class="lesson-label"')
            scoped = scoped.replace('.book-label', '.lesson-label')
            (ASSETS / f'lesson-{number:02d}.css').write_text(scoped+'\n', encoding='utf-8')
            # Keep the explicit source attribution in lesson 1; remove book packaging only.
            body = body.replace('本节沿着原书', '本教程参考').replace('>第9章“材料科学”</a>', '>AI4S in Hand 的材料科学讨论</a>')
            adapter = ProseAdapter(body); adapter.feed(body); body = adapter.result()
            body = body.replace("document.body.classList.toggle('large')", "document.querySelector('.tutorial-reader').classList.toggle('large')")
            body = body.replace('document.body.classList.toggle("large")', 'document.querySelector(".tutorial-reader").classList.toggle("large")')
            body = body.replace("$('progress')", "document.getElementById('progress-bar')")
            body = body.replace('document.getElementById("progress")', 'document.getElementById("progress-bar")')
            body = body.replace('（此处为Python代码，润色时跳过。）', '（Python代码请见本教程网页。）').replace('（此处为代码运行输出，润色时跳过。）', '（运行结果请见本教程网页。）')
            body = re.sub(r'(?:样章|章节)\d{2}_正文润色稿(?:_杨云浩)?\.txt', f'教程{number:02d}_正文.txt', body)
            body = body.replace('下载正文TXT（代码略去）', '下载本节文字')
            def resource(match):
                nonlocal total_bytes
                key, quote, value = match.group(1,2,3)
                if value.startswith('data:'):
                    mime, payload = value[5:].split(',',1)
                    extension={'image/svg+xml':'svg','image/png':'png','image/jpeg':'jpg','application/json':'json','text/x-python':'py','text/csv':'csv'}[mime.split(';')[0]]
                    assert ';base64' in mime
                    data=base64.b64decode(payload,validate=True)
                    digest=hashlib.sha256(data).hexdigest()
                    name='assets/'+digest[:24]+'.'+extension
                    path=ASSETS/name;path.parent.mkdir(exist_ok=True)
                    if digest not in unique:
                        path.write_bytes(data);total_bytes+=len(data);unique.add(digest)
                    value=URL+name
                elif unquote(value).split('#')[0] in routes:
                    decoded=unquote(value)
                    value=routes[decoded.split('#')[0]]+('#'+decoded.split('#',1)[1] if '#' in decoded else '')
                return key+'='+quote+value+quote
            body = re.sub(r'\b(href|src)=([\"\'])(.*?)\2',resource,body,flags=re.S)
            # Images load when approached; downloadable full-size assets stay intact.
            body = re.sub(r'<img\b([^>]*?)>', lambda m:'<img'+m[1]+(' loading="lazy" decoding="async"' if 'loading=' not in m[1] else '')+'>',body)
            # Scripts execute after the reader DOM and cannot leak declarations between components.
            body = re.sub(r'<script(?![^>]*type="application/json")[^>]*>(.*?)</script>',lambda m:'<script>\n(function(){\n'+m[1]+'\n})();\n</script>',body,flags=re.S)
            (SOURCE / f'{number:02d}.html').write_text(body.strip()+'\n',encoding='utf-8')
        browser.close()
        # Preserve runnable notebooks, examples, requirements and data; only reframe the package README.
        raw=z.read('20节配套计算包.zip')
        out=io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(raw)) as source, zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as target:
            for entry in source.infolist():
                data=source.read(entry.filename)
                if entry.filename=='README.txt':
                    data=data.decode('utf-8-sig').replace('AI4S in Hand','ML-Biomat 高分子与生物大分子教程').replace('本章','本系列教程').replace('本书','本系列教程').encode('utf-8')
                target.writestr(entry,data)
        (ASSETS/'polymer-ai-notebooks.zip').write_bytes(out.getvalue())
    print(f'Imported 20 lessons; {len(unique)} unchanged assets; {total_bytes/1e6:.1f} MB assets.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive',type=Path)
    main(parser.parse_args().archive)
