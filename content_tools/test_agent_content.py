from pathlib import Path
import json
import re
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from content_tools.agent_content import convert, generate, validate, Document, Node
ROOT=Path(__file__).resolve().parents[1]
BASE='https://ml-biomat.com'


def page(body, route='/example/', canonical=None):
    return f'<html lang="en"><head><title>Example — ML-Biomat</title><link rel="canonical" href="{BASE}{canonical or route}"></head><body><nav>Global nav</nav><main>{body}</main><footer>Site footer</footer></body></html>'


class MarkdownTests(unittest.TestCase):
    def test_content_and_noise(self):
        source=page('<h1>Page title</h1><nav>Inner nav</nav><aside class="bc-toc">Contents</aside><p>A <strong>result</strong>, x <code>a &lt; b</code>, $x^2$.</p><p><a href="../paper/">Source</a><img src="/plot.svg" alt="Curve"></p><section class="article-support">Donate QR</section><aside class="site-sponsor">Ad</aside><section><h2>Comments</h2><script src="https://giscus.app/client.js"></script></section><footer><a href="/license/">License</a></footer><div class="lab-controls"><label>Size</label><input></div><button>Copy</button><script>SECRET_SCRIPT</script>')
        result=convert(source,BASE+'/example/')['text']
        self.assertEqual(result.count('# Page title'),1)
        for good in ['**result**','`a < b`','$x^2$','[Source](https://ml-biomat.com/paper/)','![Curve](https://ml-biomat.com/plot.svg)','[License](https://ml-biomat.com/license/)']:
            self.assertIn(good,result)
        for bad in ['Global nav','Inner nav','Contents','Donate QR','SECRET_SCRIPT','Comments','Site footer','Copy','Size']:
            self.assertNotIn(bad,result)

    def test_code_whitespace_and_fence(self):
        raw='def x():\n    if a &lt; 2:\n        return "```"\n\n\nprint(x())'
        result=convert(page('<h1>Code</h1><pre><code class="language-python">'+raw+'</code></pre>'),BASE+'/example/')['text']
        self.assertIn('````python\ndef x():\n    if a < 2:\n        return "```"\n\n\nprint(x())\n````',result)

    def test_original_tex_norm_operator(self):
        svg = '<mjx-container display="true"><svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0"/></svg></mjx-container>'
        tex = r"L=\|x-y\|^2"
        result=convert(page('<h1>Norm</h1><div class="equation-display" aria-label="'+tex+'">'+svg+'</div>'),BASE+'/example/')['text']
        self.assertIn(tex,result)

    def test_math_structure(self):
        svg='<mjx-container display="true"><svg><g data-mml-node="math"><g data-mml-node="mfrac"><g data-mml-node="mi"><path data-c="61"></path></g><g data-mml-node="msup"><g data-mml-node="mi"><path data-c="62"></path></g><g data-mml-node="mn"><path data-c="32"></path></g></g><rect></rect></g></g></svg></mjx-container>'
        result=convert(page('<h1>Math</h1>'+svg),BASE+'/example/')
        self.assertEqual(len(result['assets']),1)
        self.assertIn('![Formula](https://ml-biomat.com/static/agent-math/',result['text'])
        self.assertEqual(next(iter(result['assets'].values())),svg[svg.index('<svg>'):svg.index('</svg>')+6])
        self.assertNotIn('\\frac',result['text'])

    def test_authored_formula_sources(self):
        svg='<mjx-container display="true"><svg><g data-mml-node="math"></g></svg></mjx-container>'
        plain='R = √(Rₓ²+Rᵧ²+R_z²)'
        source=page('<h1>Math</h1><div data-plain="'+plain+'">'+svg+'</div><div class="equation-display" aria-label="R_x^2 + R_y^2">'+svg+'</div>')
        result=convert(source,BASE+'/example/')['text']
        self.assertIn(plain,result)
        self.assertIn('$$\nR_x^2 + R_y^2\n$$',result)
        real=(ROOT/'docs/tutorials/polymer-ai/05-chain-dimensions/index.html').read_text(encoding='utf8')
        result=convert(real,BASE+'/tutorials/polymer-ai/05-chain-dimensions/')['text']
        self.assertIn('√(Rₓ²+Rᵧ²+R_z²)',result)
        self.assertNotIn('}_{2}^{',result)

    def test_nested_lists_table_and_hidden(self):
        result=convert(page('<h1>Tables</h1><ol start="3"><li>A<ul><li>B</li></ul></li><li>C</li></ol><table><tr><th>key</th><th>value</th></tr><tr><td>x|y</td><td>2</td></tr></table><p hidden>secret</p>'),BASE+'/example/')['text']
        self.assertIn('3. A\n\n   - B',result)
        self.assertIn('| key | value |\n| --- | --- |\n| x\\|y | 2 |',result)
        self.assertNotIn('secret',result)

    def test_legacy_list_siblings(self):
        result=convert(page('<h1>Legacy</h1><ul><li>Setup</li><pre><code>def f():\n    return 1</code></pre><p>Important explanation.</p><li>Next</li></ul>'),BASE+'/example/')['text']
        self.assertIn('def f():\n    return 1',result)
        self.assertIn('Important explanation.',result)
        self.assertLess(result.index('Setup'),result.index('def f():'))
        self.assertLess(result.index('explanation.'),result.index('Next'))

    def test_wrapped_card_and_svg(self):
        result=convert(page('<h1>Cards</h1><a href="/course/"><h2>Course</h2><p>Summary.</p></a><figure id="diagram"><svg aria-label="Network"><path/></svg></figure>'),BASE+'/example/')['text']
        self.assertIn('## [Course](https://ml-biomat.com/course/)',result)
        self.assertIn('[Figure: Network](https://ml-biomat.com/example/#diagram)',result)

    def test_redirects(self):
        self.assertIsNone(convert(page('<h1>X</h1><p>X</p>',canonical='/other/'),BASE+'/example/'))
        self.assertIsNone(convert(page('<meta http-equiv="refresh" content="0;url=/"><p>X</p>'),BASE+'/example/'))

    def test_generate_contract(self):
        with tempfile.TemporaryDirectory(prefix='agent-md-',dir=ROOT/'.local') as temp:
            root=Path(temp)
            for route in ['example','payments/complete']:
                (root/route).mkdir(parents=True)
                (root/route/'index.html').write_text(page('<h1>Example</h1><p>Content with <a href="/example/">link</a>.</p>',route='/'+route+'/'),encoding='utf8')
            (root/'sitemap.xml').write_text('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>'+BASE+'/example/</loc></url><url><loc>'+BASE+'/payments/complete/</loc></url></urlset>',encoding='utf8')
            search=[{'url':'/example/','title':'Example','lang':'en','category':'python-tutorials','description':'A topic.'}]
            (root/'search.json').write_text(json.dumps(search),encoding='utf8')
            result=generate(root,BASE,search)
            index=json.loads((root/'agent-index.json').read_text(encoding='utf8'))
            self.assertEqual(result['pages'],1)
            self.assertEqual(index,{'version':1,'pages':[{'url':'/example/','markdown':'/example/index.md','title':'Example','lang':'en','category':'python-tutorials'}]})
            self.assertIn('Content with',(root/'llms-full.txt').read_text(encoding='utf8'))
            self.assertIn('/example/index.md',(root/'llms.txt').read_text(encoding='utf8'))
            self.assertFalse((root/'payments/complete/index.md').exists())
            self.assertTrue(validate(root)['ok'])

    def test_real_courses_retain_all_code(self):
        routes=['/tutorials/machine-learning/m01/','/tutorials/machine-learning/m28/en/','/tutorials/python-scientific/p01/','/tutorials/molecular-dynamics/g01/','/tutorials/polymer-ai/01-chains-and-scales/','/posts/scipy-curve-fitting-zh/']
        for route in routes:
            source=(ROOT/'docs'/route.strip('/')/'index.html').read_text(encoding='utf8')
            result=convert(source,BASE+route)['text']
            for node in Document(source).root.walk():
                if node.tag=='pre':
                    code=next((n for n in node.children if isinstance(n,Node) and n.tag=='code'),node)
                    self.assertIn(code.text().strip('\n'),result,route)
            self.assertNotIn('article-support',result)
            self.assertNotIn('请我喝咖啡',result)
            self.assertNotIn('MathJax',result)
            self.assertGreater(len(result),1000)


if __name__=='__main__':
    unittest.main()
