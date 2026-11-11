"""Shared article support section, using the owner's original payment images."""
from html import escape


def render(language, asset):
    en = language == 'en'
    heading = 'Buy me a coffee' if en else '请我喝咖啡'
    cards = []
    for path, label, size in [('/static/images/wechat.png', 'WeChat' if en else '微信', 423),
                               ('/static/images/alipay.jpg', 'Alipay' if en else '支付宝', 666)]:
        src = escape(asset(path), quote=True)
        alt = label + (' support QR code' if en else '赞赏二维码')
        cards.append(f'<figure><a href="{src}" target="_blank" rel="noopener" aria-label="{alt}"><img src="{src}" alt="{alt}" width="{size}" height="{size}" loading="lazy" decoding="async"></a><figcaption>{label}</figcaption></figure>')
    return '<section class="article-support" aria-labelledby="article-support-heading"><h2 id="article-support-heading">'+heading+'</h2><div class="article-support-codes">'+''.join(cards)+'</div><a class="support-paypal" href="https://www.paypal.com/ncp/payment/BH5JZ28J2BSQL" rel="noopener">PayPal</a></section>'
