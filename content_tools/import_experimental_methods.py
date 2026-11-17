"""Import the public experimental-methods course delivery into the existing site shell."""
from pathlib import Path
from html import escape, unescape
import base64, hashlib, json, re, shutil
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path(r'D:/DW/experimental-methods-courses/public')
CONTENT=ROOT/'content/tutorials/experimental-methods'
STATIC=ROOT/'static/tutorials/experimental-methods'
BASE='/static/tutorials/experimental-methods/'
CONTENT.mkdir(parents=True,exist_ok=True)
(STATIC/'figures').mkdir(parents=True,exist_ok=True)
USED_MEDIA=set()

def save_media(raw,extension):
    name=hashlib.sha256(raw).hexdigest()[:24]+extension
    file=STATIC/'figures'/name
    USED_MEDIA.add(name)
    if not file.exists():file.write_bytes(raw)
    return BASE+'figures/'+name

def plain(s):return unescape(re.sub(r'<[^>]*>','',s)).strip()
def page_url(identifier,language):return '/tutorials/experimental-methods/'+identifier.lower()+'/'+('en/' if language=='en' else '')
def fix_links(body,language):
    def change(m):
        prefix,value,quote=m.groups()
        if value.startswith(('downloads/','assets/','licenses/')):value=BASE+value
        elif re.match(r'^(?:[STICPMEL]\d{2}|index)\.html(?:[?#]|$)',value):
            file,*rest=value.split('#',1);key=file.split('?')[0].split('.')[0]
            value=('/categories/wet-lab-data/'+('en/' if language=='en' else '') if key=='index' else page_url(key,language))+('#'+rest[0] if rest else '')
        return prefix+value+quote
    return re.sub(r'((?:href|src)=["\'])([^"\']+)(["\'])',change,body)

def normalize_svg(svg):
    svg=re.sub(r'(?<=\s)viewbox=', 'viewBox=', svg)
    svg=re.sub(r'(<\/?)(clippath)(?=[\s>])', r'\1clipPath', svg)
    def dedup_root(match):
        tag=match[0];seen=set();pieces=[];last=0
        for attribute in re.finditer(r"\s+([\w:-]+)\s*=\s*(?:\"[^\"]*\"|'[^']*')",tag):
            key=attribute[1].lower()
            if key in seen:pieces.append(tag[last:attribute.start()]);last=attribute.end()
            seen.add(key)
        pieces.append(tag[last:]);return ''.join(pieces)
    svg=re.sub(r'<svg\b[^>]*>',dedup_root,svg,count=1)
    ET.fromstring(svg)
    return svg

def media(body):
    def data_image(m):
        mime,data=m.groups();ext={'image/png':'.png','image/jpeg':'.jpg','image/webp':'.webp','image/svg+xml':'.svg'}.get(mime)
        if not ext:raise ValueError(mime)
        return save_media(base64.b64decode(data),ext)
    def figure(m):
        content=m[1]
        match=re.fullmatch(r'\s*(<svg\b.*?</svg>)\s*',content,re.S)
        if match:
            svg=match[1]
            # HTML's SVG parser restores these names; standalone SVG XML needs the canonical casing.
            svg=normalize_svg(svg)
            name=save_media(svg.encode('utf8'),'.svg')
            label=re.search(r'aria-label="([^"]*)"',svg)
            view=re.search(r'viewBox="([^"]+)"',svg)
            size=''
            if view:
                nums=view[1].split();size=' width="'+str(round(float(nums[2])))+'" height="'+str(round(float(nums[3])))+'"'
            content='<img src="'+name+'" data-full-src="'+name+'" alt="'+(label[1] if label else '')+'" loading="lazy" decoding="async"'+size+'>'
        else:
            content=re.sub(r'<img\b[^>]*>',lambda i:i[0][:-1]+(' data-full-src="'+re.search(r'src="([^"]+)"',i[0])[1]+'"' if 'data-full-src=' not in i[0] else '')+(' loading="lazy"' if 'loading=' not in i[0] else '')+' decoding="async">',content)
        return '<div class="figure-stage">'+content+'</div>'
    body=re.sub(r'<div class="figure-stage">\s*(<svg\b.*?</svg>)\s*</div>',figure,body,flags=re.S)
    # SVGs used through <img> must remain self-contained: their nested image data stays embedded.
    # Only standalone HTML image data is externalized here, after whole SVG extraction.
    body=re.sub(r'<img\b[^>]*>',lambda image:re.sub(r'data:(image/[^;,]+);base64,([A-Za-z0-9+/=\r\n]+)',data_image,image[0]),body,flags=re.S)
    body=re.sub(r'<div class="figure-open">.*?</div>','',body,flags=re.S)
    # Source SVG math must remain inline; scope its generic stroke rule to MathJax only.
    body=body.replace('*{stroke-linejoin: round; stroke-linecap: butt}','.python-course svg *{stroke-linejoin: round; stroke-linecap: butt}')
    return body

catalog=json.loads((SOURCE.parent/'COURSES.json').read_text(encoding='utf8'))
assert len(catalog['courses']) == 52 and len({course['id'] for course in catalog['courses']}) == 52
lessons=[]
strand_names={strand['id']:strand['title'] for strand in catalog['strands']}
# Short search titles leave the full scientific title in the visible h1.
short_english={
    'S08':'ICP emission spectrometry: Elemental analysis and calibration',
    'I01':'Optical and fluorescence microscopy: Light paths and images',
    'I02':'Confocal microscopy: Optical sectioning and 3-D images',
    'P05':'Protein adsorption at material–biological interfaces',
    'S04':'Fluorescence spectroscopy: Intensity and lifetime',
}
for course in catalog['courses']:
    identifier=course['id'];source=(SOURCE/course['file']).read_text(encoding='utf8')
    def script(name):return re.search(r'<script[^>]*id="'+name+r'"[^>]*>(.*?)</script>',source,re.S)[1]
    meta=json.loads(script('lesson-meta'));bodies=json.loads(script('lesson-content'))
    assert meta['id'] == identifier and set(bodies) == {'zh','en'}
    assert set(meta['title']) == set(meta['deck']) == {'zh','en'}
    heads={lang:re.findall(r'<section[^>]*id="([^"]+)"[^>]*>\s*<h2[^>]*>(.*?)</h2>',body,re.S) for lang,body in bodies.items()}
    assert [key for key,title in heads['zh']] == [key for key,title in heads['en']], identifier
    english=dict(heads['en']);sections=[{'id':key,'title':{'zh':plain(title),'en':plain(english.get(key,title))}} for key,title in heads['zh']]
    item={'id':identifier,'title':meta['title'],'standfirst':meta['deck'],'category':'wet-lab-data','group':strand_names[course['strand']],'search_title':{'zh':meta['title']['zh'],'en':short_english.get(identifier,meta['title']['en'])},'keywords':meta.get('keywords',[]),'sections':sections,'scripts':meta.get('scripts',[]),'neighbors':{},'prerequisites':meta.get('prerequisites',[])}
    for lang,body in bodies.items():
        body=media(fix_links(body,lang))
        (CONTENT/(identifier.lower()+'-'+lang+'.html')).write_text(body,encoding='utf8')
    lab=script('lab-source')
    # The shared site uses the region-qualified zh-CN HTML language.
    lab=re.sub(r"document\.documentElement\.lang\s*===?\s*(['\"])zh\1", "document.documentElement.lang.startsWith('zh')", lab)
    (STATIC/(identifier.lower()+'.js')).write_text(lab,encoding='utf8')
    lessons.append(item)
for index,item in enumerate(lessons):
    item['neighbors']={'prev':lessons[index-1]['id'] if index else None,'next':lessons[index+1]['id'] if index+1<len(lessons) else None}
(CONTENT/'manifest.json').write_text(json.dumps({'title':{'zh':'实验与表征','en':'Experiments and Characterization'},'lessons':lessons},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for directory in ['assets','downloads','licenses']:
    if (SOURCE/directory).is_dir():shutil.copytree(SOURCE/directory,STATIC/directory,dirs_exist_ok=True)
shutil.copy2(SOURCE/'THIRD_PARTY_NOTICES.txt',STATIC/'THIRD_PARTY_NOTICES.txt')
# Preserve license text while directing its course links to the integrated website.
license_index=STATIC/'licenses/index.html'
license_text=license_index.read_text(encoding='utf8')
license_text=license_text.replace('href="../index.html"','href="/categories/wet-lab-data/"')
license_text=re.sub(r'href="\.\./([STICPMEL]\d{2})\.html"',lambda m:'href="'+page_url(m[1],'zh')+'"',license_text)
license_index.write_text(license_text,encoding='utf8')

print('Imported',len(lessons),'bilingual lessons;',len(list((STATIC/'figures').iterdir())),'external figures')

# Remove only obsolete generated files from this import's dedicated figure directory.
for file in (STATIC/'figures').iterdir():
    assert file.resolve().parent == (STATIC/'figures').resolve()
    if file.is_file() and file.name not in USED_MEDIA:file.unlink()

# Seal new originals for shared click-to-enlarge viewing and integrity QA.
from PIL import Image
preview_path=ROOT/'static/images/previews/manifest.json'
preview=json.loads(preview_path.read_text(encoding='utf8'))
preview['images']={key:item for key,item in preview['images'].items() if not key.startswith(BASE+'figures/') or (ROOT/key.lstrip('/')).is_file()}
for file in sorted((STATIC/'figures').iterdir()):
    raw=file.read_bytes()
    if file.suffix=='.svg':
        view=re.search(r'viewBox=[\"\']([^\"\']+)',raw.decode('utf8'))
        if view:
            width,height=[round(float(value)) for value in view[1].split()[2:]]
        else:
            element=ET.fromstring(raw)
            width,height=[round(float(re.match(r'[0-9.]+',element.attrib[key])[0])) for key in ['width','height']]
    else:
        with Image.open(file) as image:width,height=image.size
    url='/'+file.relative_to(ROOT).as_posix()
    preview['images'][url]={'full':url,'width':width,'height':height,'source_sha256':hashlib.sha256(raw).hexdigest(),'source_bytes':len(raw),'variants':[]}
preview_path.write_text(json.dumps(preview,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Sealed',len(list((STATIC/'figures').iterdir())),'original figure assets')
