"""Import public bilingual MD lessons, retaining source scientific content."""
from pathlib import Path
import hashlib, json, re, shutil, sys
ROOT=Path(__file__).resolve().parents[1]
BASE='/tutorials/molecular-dynamics/'
ASSET='/static/tutorials/molecular-dynamics/'
RELEASE='https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/'
def digest(b):return hashlib.sha256(b).hexdigest()
def run(source):
    from qa_check import PageParser
    content=ROOT/'content/tutorials/molecular-dynamics';content.mkdir(parents=True,exist_ok=True)
    assets=ROOT/ASSET.lstrip('/');assets.mkdir(parents=True,exist_ok=True)
    bundles=ROOT/'.local/md-course-downloads';bundles.mkdir(parents=True,exist_ok=True)
    files=[source/'courses/getting-started.html']+sorted((source/'courses').glob('g[0-9][0-9].html'))+sorted((source/'courses').glob('l[0-9][0-9].html'))
    assert len(files)==35
    manifest={'lessons':[],'assets':{},'downloads':{}}
    ids={f.name:('s00' if f.stem=='getting-started' else f.stem) for f in files}
    common=None
    for file in files:
        raw=file.read_bytes();text=raw.decode('utf-8-sig').replace('\r\n','\n')
        scripts=re.findall(r'<script([^>]*)>(.*?)</script>',text,re.S)
        meta=json.loads(next(s for a,s in scripts if s.startswith('window.COURSE_META=')).removeprefix('window.COURSE_META=').rstrip(';'))
        ident=meta['id'].lower();meta['category']='multiscale-modeling';meta['source_sha256']=digest(raw);meta['source_file']=file.name;meta['counts']={}
        meta['neighbors']={rel:ids[href].upper() for href,rel in re.findall(r'<a href="([^"]+)" rel="(prev|next)"',text) if href in ids}
        runtime=next(s for a,s in scripts if "const language=root=>" in s)
        if common is None:common=runtime
        assert common==runtime,'Shared scientific runtime diverged'
        labs=[s for a,s in scripts if not a.strip() and s!=runtime and not s.startswith('window.COURSE_META=') and "const meta=window.COURSE_META" not in s]
        (assets/(ident+'.js')).write_text('\n'.join(labs) or '// No interactive parameter lab in this lesson.\n',encoding='utf-8')
        panes=re.findall(r'<article\b[^>]*data-lang="(zh|en)"[^>]*>(.*?)</article>',text,re.S);assert {l for l,b in panes}=={'zh','en'}
        for lang,body in panes:
            before=PageParser(body).root
            def rewrite_link(m):
                from html import unescape
                attr,value=m.groups()
                if value.startswith(('#','https:','http:','data:','mailto:')):return m[0]
                if value=='index.html':value='/categories/multiscale-modeling/'+('en/' if lang=='en' else '')
                elif value.split('#')[0] in ids:
                    name,sep,anchor=value.partition('#');value=BASE+ids[name]+'/'+('en/' if lang=='en' else '')+(sep+anchor if sep else '')
                else:
                    local=(file.parent/unescape(value)).resolve()
                    assert local.is_relative_to(source.resolve()) and local.is_file(),value
                    if local.suffix=='.zip':
                        name=local.parent.name+'-'+local.name;value=RELEASE+name
                        if name not in manifest['downloads']:
                            dest=bundles/name;shutil.copyfile(local,dest)
                            manifest['downloads'][name]={'url':value,'sha256':digest(local.read_bytes()),'bytes':local.stat().st_size,'source':local.relative_to(source).as_posix()}
                    else:
                        name='files/'+local.relative_to(source).as_posix();dest=assets/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(local,dest);value=ASSET+name
                        manifest['assets'][value]={'sha256':digest(local.read_bytes()),'bytes':local.stat().st_size}
                return attr+'="'+value+'"'
            body=re.sub(r'\b(href|src)="([^"]*)"',rewrite_link,body)
            def externalize(m):
                data=json.loads(m[1]);packed=json.dumps(data,ensure_ascii=False,separators=(',',':')).encode('utf-8');name='trajectories/'+digest(packed)+'.json';dest=assets/name;dest.parent.mkdir(exist_ok=True);dest.write_bytes(packed)
                url=ASSET+name;manifest['assets'][url]={'sha256':digest(packed),'bytes':len(packed)}
                return '<script type="application/json" class="trajectory-data" data-src="'+url+'"></script>'
            body=re.sub(r'<script type="application/json" class="trajectory-data">(.*?)</script>',externalize,body,flags=re.S)
            parsed=PageParser(body).root
            counts=lambda d:{'sections':len(d.find('section')),'equations':len(d.find(cls='equation')),'figures':len(d.find('figure',cls='science-figure')),'labs':len(d.find(attr='data-lab')),'result_figures':len(d.find('figure',cls='result-figure')),'trajectories':len(d.find(cls='trajectory-player'))}
            assert counts(before)==counts(parsed)
            meta['counts'][lang]=dict(counts(parsed),sha256=digest(body.encode('utf-8')))
            (content/(ident+'-'+lang+'.html')).write_text(body,encoding='utf-8')
        manifest['lessons'].append(meta)
    # Transport only: source coordinates and scientific player equations are unchanged.
    common=common.strip()
    common=common.replace("document.querySelectorAll('.trajectory-player').forEach(root=>{",'function initializeTrajectory(root){')
    common=common.replace("const data=JSON.parse(root.querySelector('.trajectory-data').textContent),", "const data=root.trajectoryPayload,")
    assert common.endswith('});\n})();')
    common=common[:-len('});\n})();')]+r'''}
async function loadTrajectory(root){
 if(root.dataset.loading||root.dataset.loaded)return;root.dataset.loading='true';root.setAttribute('aria-busy','true');
 const controls=[...root.querySelectorAll('button,input')];controls.forEach(el=>el.disabled=true);
 try{
  const script=root.querySelector('.trajectory-data');
  if(script.dataset.src){const response=await fetch(script.dataset.src);if(!response.ok)throw new Error('Trajectory load');root.trajectoryPayload=await response.json();}
  else{root.trajectoryPayload=JSON.parse(script.textContent);}initializeTrajectory(root);root.dataset.loaded='true';observer?.unobserve(root);
  root.querySelector('[data-retry-trajectory]')?.remove();
 }catch(error){
  if(!root.querySelector('[data-retry-trajectory]')){const retry=document.createElement('button');retry.type='button';retry.dataset.retryTrajectory='';retry.textContent=language(root)==='zh'?'重新加载轨迹':'Reload trajectory';retry.onclick=()=>loadTrajectory(root);root.append(retry);}
 }finally{delete root.dataset.loading;root.removeAttribute('aria-busy');controls.forEach(el=>el.disabled=false);}
}
const observer='IntersectionObserver' in window?new IntersectionObserver(entries=>{for(const entry of entries)if(entry.isIntersecting)loadTrajectory(entry.target);},{rootMargin:'600px'}):null;
document.querySelectorAll('.trajectory-player').forEach(root=>{root.querySelectorAll('button,input').forEach(el=>el.disabled=true);if(observer)observer.observe(root);else loadTrajectory(root);});
})();
'''
    (ROOT/'static/js/molecular-dynamics.js').write_text(common,encoding='utf-8')
    (content/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Imported',len(manifest['lessons']),'bilingual lessons;',len(manifest['assets']),'assets;',len(manifest['downloads']),'download bundles')
if __name__=='__main__':run(Path(sys.argv[1]))
