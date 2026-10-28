"""Bilingual utility pages with shared navigation and an unchanged teaching model."""
from html import escape
import json


TOOL_COPY = {
    'zh': {
        'title': '应力—应变探索',
        'description': '调节教学曲线的参数，观察应力—应变曲线、线性段斜率与曲线面积。',
        'intro': '调节趾区、线性段斜率和终止应变，观察曲线与积分面积的变化。曲线采用教学示例函数，应力及面积以相对量显示。',
        'labels': ['趾区范围（0–40%）', '趾区曲率参数', '线性段斜率（相对值）', '终止应变（30–120%）'],
        'reset': '恢复默认参数', 'modulus': '线性段斜率', 'area': '曲线面积',
        'x': '应变', 'y': '相对应力', 'canvas': '应力—应变教学曲线；下方显示当前线性段斜率和曲线面积。',
    },
    'en': {
        'title': 'Stress–Strain Explorer',
        'description': 'Adjust a teaching curve to explore stress–strain behaviour, linear slope and area under the curve.',
        'intro': 'Adjust the toe region, linear slope and end strain to explore the curve and its integrated area. The teaching function expresses stress and area in relative units.',
        'labels': ['Toe extent (0–40%)', 'Toe curvature parameter', 'Linear slope (relative)', 'End strain (30–120%)'],
        'reset': 'Reset parameters', 'modulus': 'Linear slope', 'area': 'Area under curve',
        'x': 'Strain', 'y': 'Relative stress', 'canvas': 'Stress–strain teaching curve. The current linear slope and area under the curve appear below.',
    },
}

TOOL_STYLE = '''<style>
.tool-page .tool-control-heading{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.tool-page .tool-control-heading output{font-variant-numeric:tabular-nums;color:var(--c-fg);font-weight:600;white-space:nowrap}
.tool-page .tool-controls input[type=range]{width:100%;min-height:30px;margin:0}
.tool-page .tool-reset{align-self:flex-start;min-height:40px;padding:8px 12px;border:1px solid var(--c-border);border-radius:6px;background:var(--c-surface);color:var(--c-primary);font:600 13px/1.5 var(--font-sans);cursor:pointer}
.tool-page .tool-reset:hover{border-color:var(--c-primary)}
.tool-page .tool-reset:focus-visible{outline:2px solid var(--c-primary);outline-offset:3px}
.tool-page .tool-output{min-width:0}
.tool-page .tool-metrics{flex-wrap:wrap;line-height:1.7}
.tool-page .tool-metrics strong{font-variant-numeric:tabular-nums}
.tool-page #ss-canvas{display:block;max-width:100%;aspect-ratio:32/21}
</style>'''

TOOL_SCRIPT = r'''<script>
(function(){
  function init(){
    var cv=document.getElementById('ss-canvas');
    if(!cv) return;
    var ctx=cv.getContext('2d');
    if(!ctx) return;
    var copy=__COPY__;
    var ids=['p-toe','p-xi','p-k','p-fail'];
    function val(id){return parseFloat(document.getElementById(id).value);}
    // Keep the original educational curve and numerical integration unchanged.
    function stress(s){var toe=val('p-toe'),xi=val('p-xi'),k=val('p-k'),fail=val('p-fail');
      if(s<=0)return 0;
      var toeEnd=0.2*Math.exp(toe/xi);
      if(s<=toe){return toeEnd*(Math.exp(s/xi)-1)/(Math.exp(toe/xi)-1);}
      var lin=toeEnd+k*(s-toe);
      return s>fail? Math.max(0,lin-0.6*(s-fail)):lin;}
    function draw(){
      var W=Math.max(260,cv.clientWidth),H=W*420/640,dpr=Math.min(window.devicePixelRatio||1,3);
      var pixelW=Math.round(W*dpr),pixelH=Math.round(H*dpr);
      if(cv.width!==pixelW||cv.height!==pixelH){cv.width=pixelW;cv.height=pixelH;}
      ctx.setTransform(dpr,0,0,dpr,0,0);
      ctx.clearRect(0,0,W,H);
      var palette=getComputedStyle(document.documentElement);
      var fg=palette.getPropertyValue('--c-fg-soft').trim()||'#475569';
      var grid=palette.getPropertyValue('--c-border').trim()||'#dbe2ec';
      var primary=palette.getPropertyValue('--c-primary').trim()||'#2563eb';
      var left=58,right=18,top=20,bottom=43;
      var fail=val('p-fail');
      var ss=[];for(var j=0;j<=400;j++){var s=fail*j/400;ss.push([s,stress(s)]);}
      var maxS=1e-6;for(var q=0;q<ss.length;q++){if(ss[q][1]>maxS)maxS=ss[q][1];}
      function tickLabel(y){return y>=1000?y.toExponential(1):y.toFixed(y>=10?0:1);}
      ctx.font='12px "Microsoft YaHei",sans-serif';
      for(var t=0;t<=4;t++){left=Math.max(left,Math.ceil(ctx.measureText(tickLabel(maxS*1.15*t/4)).width)+28);}
      function X(s){return left+(W-left-right)*(s/(fail||1));}
      function Y(y){return H-bottom-(H-top-bottom)*(y/(maxS*1.15));}
      ctx.font='12px "Microsoft YaHei",sans-serif';
      ctx.lineWidth=1;ctx.strokeStyle=grid;ctx.fillStyle=fg;
      for(var i=0;i<=4;i++){
        var sx=fail*i/4,x=X(sx),sy=maxS*1.15*i/4,y=Y(sy);
        ctx.beginPath();ctx.moveTo(x,top);ctx.lineTo(x,H-bottom);ctx.stroke();
        ctx.beginPath();ctx.moveTo(left,y);ctx.lineTo(W-right,y);ctx.stroke();
        ctx.textAlign='center';ctx.textBaseline='top';ctx.fillText((sx*100).toFixed(0)+'%',x,H-bottom+8);
        ctx.textAlign='right';ctx.textBaseline='middle';
        ctx.fillText(tickLabel(sy),left-8,y);
      }
      ctx.strokeStyle=primary;ctx.lineWidth=2.5;
      ctx.beginPath();ctx.moveTo(X(0),Y(0));for(var r=0;r<ss.length;r++){ctx.lineTo(X(ss[r][0]),Y(ss[r][1]));}ctx.stroke();
      ctx.fillStyle=fg;ctx.font='13px "Microsoft YaHei",sans-serif';
      ctx.textAlign='center';ctx.textBaseline='bottom';ctx.fillText(copy.x,(left+W-right)/2,H-3);
      ctx.save();ctx.translate(17,(top+H-bottom)/2);ctx.rotate(-Math.PI/2);ctx.textBaseline='bottom';ctx.fillText(copy.y,0,0);ctx.restore();
    }
    function metrics(){
      var fail=val('p-fail'), n=2000, area=0, ds=fail/n, prev=0;
      for(var i=1;i<=n;i++){var y=stress(i*ds);area+=(y+prev)/2*ds;prev=y;}
      document.getElementById('m-mod').textContent=val('p-k').toFixed(2);
      document.getElementById('m-tough').textContent=area.toFixed(3);
    }
    function update(){
      ids.forEach(function(id){
        var text=(id==='p-toe'||id==='p-fail')?(val(id)*100).toFixed(0)+'%':val(id).toFixed(2);
        document.getElementById(id+'-value').textContent=text;
        document.getElementById(id).setAttribute('aria-valuetext',text);
      });
      draw();metrics();
    }
    ids.forEach(function(id){document.getElementById(id).addEventListener('input',update);});
    document.getElementById('ss-reset').addEventListener('click',function(){
      ids.forEach(function(id){var input=document.getElementById(id);input.value=input.defaultValue;});update();
    });
    var frame=0;
    function redraw(){cancelAnimationFrame(frame);frame=requestAnimationFrame(draw);}
    new MutationObserver(redraw).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
    var media=window.matchMedia('(prefers-color-scheme: dark)');
    if(media.addEventListener)media.addEventListener('change',redraw);
    if(window.ResizeObserver)new ResizeObserver(redraw).observe(cv);
    else window.addEventListener('resize',redraw);
    update();
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);
  else init();
})();
</script>'''


def tool_body(lang):
    text=TOOL_COPY[lang]
    controls=[]
    for label, (key, lower, upper, step, value, display) in zip(text['labels'], [
        ('p-toe','0','0.4','0.01','0.12','12%'),
        ('p-xi','0.02','0.2','0.01','0.08','0.08'),
        ('p-k','0.2','3.0','0.05','1.0','1.00'),
        ('p-fail','0.3','1.2','0.01','0.8','80%'),
    ]):
        controls.append(f'<label for="{key}"><span class="tool-control-heading"><span>{escape(label)}</span><output id="{key}-value" for="{key}">{display}</output></span><input id="{key}" type="range" min="{lower}" max="{upper}" step="{step}" value="{value}"></label>')
    return TOOL_STYLE+f'''<section class="tool-page">
<h1>{escape(text['title'])}</h1>
<p class="tool-intro">{escape(text['intro'])}</p>
<div class="tool-layout">
<div class="tool-controls">{''.join(controls)}<button id="ss-reset" class="tool-reset" type="button">{escape(text['reset'])}</button></div>
<div class="tool-output"><canvas id="ss-canvas" width="640" height="420" role="img" aria-label="{escape(text['canvas'],quote=True)}">{escape(text['canvas'])}</canvas>
<div class="tool-metrics" aria-live="polite" aria-atomic="true"><span>{escape(text['modulus'])}: <strong id="m-mod">1.00</strong></span><span>{escape(text['area'])}: <strong id="m-tough">0.00</strong></span></div></div>
</div></section>'''+TOOL_SCRIPT.replace('__COPY__',json.dumps({'x':text['x'],'y':text['y']},ensure_ascii=False))


PRIVACY = {
    'zh': ("隐私政策", "ML-Biomat 的广告、评论、Cookie 与浏览器本地偏好说明。", '''<article class="content utility-privacy">
<h1>隐私政策</h1>
<p><em>更新日期：2026年10月28日</em></p>
<h2>1. 关于本网站</h2>
<p>ML-Biomat（ml-biomat.com）是由复旦大学杨云浩维护的个人学术网站。</p>
<h2>2. 第三方服务</h2>
<p>阅读本网站无需注册账号。页面集成的第三方服务可能处理访问相关信息：</p>
<ul>
<li><strong>Google AdSense</strong>：通过 Cookie 等技术展示广告，可能处理 IP 地址、浏览器类型和浏览行为，并根据广告设置提供个性化广告。</li>
<li><strong>Giscus 评论</strong>：使用 GitHub 进行账号认证，相关 GitHub 个人资料由 GitHub 处理。</li>
</ul>
<h2>3. Cookie 与本地偏好</h2>
<p>Google AdSense 可能使用 Cookie，根据读者此前对本网站或其他网站的访问展示广告。可以在 <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google 广告设置</a>中管理个性化广告。</p>
<p>网站使用浏览器本地存储保存亮色或暗色主题偏好，便于在切换页面后保留所选主题。</p>
<h2>4. 数据使用</h2>
<p>网站运营者不出售或交易读者的个人信息。第三方服务所处理的数据受其各自隐私政策约束。</p>
<h2>5. 管理偏好</h2>
<p>可以在浏览器设置中限制或清除 Cookie 及网站本地数据，也可以通过 Google 广告设置调整个性化广告偏好。清除网站本地数据后，主题将恢复默认设置。</p>
<h2>6. 联系方式</h2>
<p>有关隐私的问题，请联系 <a href="mailto:Gellmansparrow@outlook.com">Gellmansparrow@outlook.com</a>。</p>
</article>'''),
    'en': ("Privacy Policy", "How ML-Biomat uses advertising, comments, cookies and local browser preferences.", '''<article class="content utility-privacy">
<h1>Privacy Policy</h1>
<p><em>Last updated: October 28, 2026</em></p>
<h2>1. About This Site</h2>
<p>ML-Biomat (ml-biomat.com) is a personal academic website maintained by Yunhao Yang at Fudan University.</p>
<h2>2. Third-Party Services</h2>
<p>You can read this site without registering an account. Third-party services embedded in its pages may process information about your visit:</p>
<ul>
<li><strong>Google AdSense</strong>: Uses cookies and similar technologies to display advertisements. Google may process your IP address, browser type and browsing activity, and provide personalised advertisements according to your ad settings.</li>
<li><strong>Giscus comments</strong>: Uses GitHub for account authentication. GitHub processes the associated GitHub profile information.</li>
</ul>
<h2>3. Cookies and Local Preferences</h2>
<p>Google AdSense may use cookies to display advertisements based on previous visits to this or other websites. You can manage personalised advertising in <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google Ads Settings</a>.</p>
<p>The site uses browser local storage to remember your light or dark theme preference when you move between pages.</p>
<h2>4. Data Use</h2>
<p>The site operator does not sell or trade readers' personal information. Data processed by third-party services is governed by their respective privacy policies.</p>
<h2>5. Managing Your Preferences</h2>
<p>You can restrict or clear cookies and local site data in your browser settings, and manage personalised advertising through Google Ads Settings. Clearing local site data restores the default theme.</p>
<h2>6. Contact</h2>
<p>For privacy-related questions, contact <a href="mailto:Gellmansparrow@outlook.com">Gellmansparrow@outlook.com</a>.</p>
</article>'''),
}


def render(make_head, make_footer, write_file, base_url, versioned_asset):
    """Write both language versions and return their public routes for the sitemap."""
    routes=[]
    base_url=base_url.rstrip('/')
    for section in ('tools/stress-strain','privacy'):
        zh_href=f'/{section}/';en_href=f'/{section}/en/'
        alternates=(f'<link rel="alternate" hreflang="zh-CN" href="{base_url+zh_href}">'
                    f'<link rel="alternate" hreflang="en" href="{base_url+en_href}">'
                    f'<link rel="alternate" hreflang="x-default" href="{base_url+zh_href}">')
        for lang in ('zh','en'):
            route=en_href if lang=='en' else zh_href
            if section=='privacy':title,description,body=PRIVACY[lang]
            else:title,description,body=TOOL_COPY[lang]['title'],TOOL_COPY[lang]['description'],tool_body(lang)
            head=make_head(title=title,desc=description,url=base_url+route,
                           lang='en' if lang=='en' else 'zh-CN',navigation_language=lang,
                           en_href=en_href,zh_href=zh_href,alternates=alternates,
                           en_active=' class="active"' if lang=='en' else '',
                           zh_active=' class="active"' if lang=='zh' else '')
            write_file(route.lstrip('/')+'index.html',head+body+make_footer(lang))
            routes.append(route)
    return routes