"""Import the supplied bilingual biomaterials lessons without changing their science."""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content/tutorials/biomaterials-courses'
ASSETS = ROOT / 'static/tutorials/biomaterials-courses'
BASE = '/tutorials/biomaterials-courses/'
DATE = '2026-10-29'


def category(identifier):
    if identifier in {'BM03', 'PM03', 'PM12', 'PE03'}:
        return 'wet-lab-data'
    if identifier.startswith('CP') or identifier in {'PE01','PE02','PE04','PE05'}:
        return 'multiscale-modeling'
    return 'biomaterials'


def route(identifier, lang):
    return BASE + identifier.lower() + '/' + ('en/' if lang == 'en' else '')


def import_courses(source):
    CONTENT.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    lessons = []
    for file in sorted(source.glob('*.html')):
        if file.name == 'index.html':
            continue
        original = file.read_bytes()
        text = original.decode('utf-8-sig').replace('\r\n', '\n')
        scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', text, re.S)
        assert scripts and scripts[0].startswith('window.COURSE_META='), file
        meta = json.loads(scripts[0].removeprefix('window.COURSE_META=').strip().rstrip(';'))
        identifier = meta['id']
        assert re.fullmatch(r'(BM|CP|PE|PM)\d{2}', identifier), identifier
        assert len(scripts) >= 3 and 'setLanguage' in scripts[1], identifier
        labs = '\n\n'.join(scripts[2:])
        (ASSETS / (identifier.lower() + '.js')).write_text(labs, encoding='utf-8', newline='\n')
        pages = re.findall(r'<article class="language-pane"[^>]*data-lang="(zh|en)"[^>]*>(.*?)</article>', text, re.S)
        assert [lang for lang, _ in pages] == ['zh', 'en'], identifier
        counts = {}
        for lang, body in pages:
            # Keep inner content byte-for-byte apart from navigation addresses.
            def relink(match):
                target = match[1]
                if target == 'index.html':
                    target = '/categories/' + ('en/' if lang == 'en' else '')
                else:
                    m = re.fullmatch(r'([a-z]{2}\d{2})\.html(#[^\"]*)?', target)
                    if m:
                        target = route(m[1], lang) + (m[2] or '')
                return 'href="' + target + '"'
            body = re.sub(r'href="([^\"]+)"', relink, body)
            (CONTENT / f'{identifier.lower()}-{lang}.html').write_text(body, encoding='utf-8', newline='\n')
            counts[lang] = {'sections':len(re.findall(r'<section\b',body)),
                            'equations':body.count('class="equation"'),
                            'figures':body.count('class="science-figure"'),
                            'labs':len(re.findall(r'data-lab=',body)),
                            'sha256':hashlib.sha256(body.encode()).hexdigest()}
        assert all(counts['zh'][key] == counts['en'][key] for key in ['sections','equations','figures','labs']), identifier
        neighbors = {}
        nav = re.search(r'<nav class="course-nav"[^>]*>(.*?)</nav>', text, re.S)
        if nav:
            for href, rel in re.findall(r'<a href="([a-z]{2}\d{2})\.html" rel="(prev|next)"',nav[1]):
                neighbors[rel] = href.upper()
        lessons.append(dict(meta, category=category(identifier), date=DATE, neighbors=neighbors,
                            source_file=file.name, source_sha256=hashlib.sha256(original).hexdigest(), counts=counts))
    assert len(lessons) == 48
    manifest = {'version':1, 'date':DATE, 'source':'User-supplied bilingual biomaterials courses', 'lessons':lessons}
    (CONTENT / 'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(f'Imported {len(lessons)} bilingual lessons; 96 article fragments and 48 unchanged laboratory scripts.')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('source', type=Path, help='Folder containing the 48 supplied course HTML files')
    args=parser.parse_args()
    import_courses(args.source)


