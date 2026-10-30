"""Generate readable image previews; original assets remain untouched.

Run this maintenance command after adding raster images, using the last complete
build as the reference inventory. Website builds use image_delivery.py and this
committed manifest, so Pillow is not a build dependency.
"""
from __future__ import annotations
from pathlib import Path
from urllib.parse import unquote,urlsplit
from PIL import Image,ImageOps
import argparse,hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'static/images/previews'

def references():
    refs=set()
    pages=list((ROOT/'docs').rglob('*.html'))+list((ROOT/'content').rglob('*.html'))
    for page in pages:
        text=page.read_text(encoding='utf8')
        for tag in re.findall(r'<img\b[^>]*>',text,re.I):
            # Rebuilding from already optimized pages retains the full source.
            attrs=dict(re.findall(r'([\w-]+)="([^\"]*)"',tag))
            value=attrs.get('data-full-src') or attrs.get('src') or attrs.get('data-preview-src','')
            path=unquote(urlsplit(value).path)
            if path.startswith('/static/') and '/previews/' not in path:refs.add(path)
    return refs

def generate():
    OUT.mkdir(parents=True,exist_ok=True)
    refs=references();aliases={}
    for src in sorted(refs):
        canonical=src
        if '/profile/' in src and '-thumb.' in src:
            candidate=src.replace('-thumb.','.')
            if (ROOT/candidate.lstrip('/')).is_file():canonical=candidate
        aliases[src]=canonical
    entries={};total_original=0;total_preview=0
    for canonical in sorted(set(aliases.values())):
        path=ROOT/canonical.lstrip('/')
        if path.suffix.lower() not in {'.jpg','.jpeg','.png','.webp'} or not path.is_file():continue
        raw=path.read_bytes();digest=hashlib.sha256(raw).hexdigest()
        with Image.open(path) as source:
            if getattr(source,'n_frames',1)>1:continue
            original=ImageOps.exif_transpose(source)
            width,height=original.size
            entry={'full':canonical,'width':width,'height':height,'source_sha256':digest,'source_bytes':len(raw),'variants':[]}
            # Tiny already-compressed charts retain their original pixels.
            if len(raw)>45000 or width>1280:
                targets=sorted({min(width,n) for n in (400,640,960,1280)})
                scientific='/fibernet/' in canonical or '/posts/' in canonical or '/tutorials/' in canonical or '/paper-' in canonical
                quality=90 if scientific else 84
                for target in targets:
                    size=(target,max(1,round(height*target/width)))
                    rendered=original.resize(size,Image.Resampling.LANCZOS) if size!=original.size else original.copy()
                    if rendered.mode not in ('RGB','RGBA'):rendered=rendered.convert('RGBA' if 'A' in rendered.getbands() else 'RGB')
                    name=path.stem+'-'+digest[:10]+'-'+str(target)+'.webp'
                    file=OUT/name
                    rendered.save(file,'WEBP',quality=quality,method=6)
                    count=file.stat().st_size
                    if count<len(raw)*.97:
                        entry['variants'].append({'src':'/static/images/previews/'+name,'width':size[0],'height':size[1],'bytes':count,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
                    else:
                        # Only remove this exact just-generated preview inside OUT.
                        assert file.resolve().parent==OUT.resolve()
                        file.unlink()
            entries[canonical]=entry
            total_original+=len(raw)
            usable=[v for v in entry['variants'] if v['width']<=960]
            total_preview+=(usable[-1]['bytes'] if usable else len(raw))
    mapping={alias:entries[canonical] for alias,canonical in aliases.items() if canonical in entries}
    for key,value in entries.items():mapping[key]=value
    manifest={'version':1,'images':mapping}
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'referenced_rasters':len(aliases),'unique_originals':len(entries),'preview_files':sum(len(e['variants']) for e in entries.values()),'original_bytes':total_original,'medium_960_bytes':total_preview,'saving_percent':round(100*(1-total_preview/total_original),1)}))

if __name__=='__main__':generate()
