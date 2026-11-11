"""PayPal completion page; private transaction URLs stay out of search indexes."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def render(make_head,make_footer,write_file,asset,base_url,items):
    paths=sorted({item.get('url') or '/posts/'+item['slug']+'/' for item in items})
    (ROOT/'payment/routes.mjs').write_text('export const ALLOWED=new Set('+json.dumps(paths)+');\n',encoding='utf-8')
    for lang in ['zh','en']:
        en=lang=='en';url='/support/complete/'+('en/' if en else '')
        title='Thank you' if en else '感谢支持'
        description='Your PayPal payment confirmation and the HTML download for your selected ML-Biomat tutorial.' if en else '确认 PayPal 付款，并下载所选教程的 HTML 文件。'
        head=make_head(title=title,desc=description,url=base_url+url,lang='en' if en else 'zh-CN',en_href='/support/complete/en/',zh_href='/support/complete/',navigation_language=lang)
        head=head.replace('</head>','<meta name="robots" content="noindex,nofollow"><meta name="referrer" content="no-referrer"></head>')
        body='<section class="payment-complete" style="max-width:680px;margin:4rem auto;min-height:40vh"><h1>'+title+'</h1><p id="payment-status" role="status" aria-live="polite"></p><a id="payment-download" hidden download></a><p><a id="payment-back" href="/categories/'+('en/' if en else '')+'">'+('Back to tutorials' if en else '返回教程')+'</a></p></section>'
        page=head+body+make_footer(lang)
        page=page.replace('</body>','<script src="'+asset('/static/js/paypal-support.js')+'" defer></script></body>')
        write_file(url.lstrip('/')+'index.html',page)
