/* A page is selected before checkout; a verified PayPal transaction enables export. */
(()=>{
'use strict';
const SERVICE='https://ml-biomat-paypal.gellmansparrow-8d4.workers.dev',KEY='ml-biomat-paypal-checkout';
const en=document.documentElement.lang==='en';
function read(){try{return JSON.parse(localStorage.getItem(KEY)||'null')}catch{return null}}
document.querySelectorAll('.support-paypal').forEach(link=>link.addEventListener('click',async event=>{
 event.preventDefault();if(link.dataset.busy)return;link.dataset.busy='true';link.setAttribute('aria-busy','true');
 try{
  const health=await fetch(SERVICE+'/health',{signal:AbortSignal.timeout(8000)});
  if(!health.ok||!(await health.json()).ready)throw Error('unavailable');
  const claim=Array.from(crypto.getRandomValues(new Uint8Array(32))).map(b=>b.toString(16).padStart(2,'0')).join('');
  localStorage.setItem(KEY,JSON.stringify({page:location.pathname,title:document.querySelector('h1')?.textContent||document.title,lang:document.documentElement.lang,claim,created:Date.now()}));
  location.assign(link.href);
 }catch{
  let note=link.parentElement.querySelector('[data-paypal-error]');
  if(!note){note=document.createElement('p');note.dataset.paypalError='';note.setAttribute('role','status');link.after(note)}
  note.textContent=en?'PayPal download is temporarily unavailable. Please try again shortly.':'PayPal 下载暂时不可用，请稍后重试。';
 }finally{delete link.dataset.busy;link.removeAttribute('aria-busy')}
}));
const status=document.getElementById('payment-status');if(!status)return;
const pending=read(),query=new URLSearchParams(location.search),tx=query.get('tx');
if(pending?.lang==='en'&&!location.pathname.endsWith('/en/')){location.replace('/support/complete/en/'+location.search);return}
history.replaceState(null,'',location.pathname);
const text=(zh,enText)=>en?enText:zh;
if(!pending||Date.now()-pending.created>3*86400000){
 status.textContent=text('请从需要下载的教程页进入 PayPal。','Start from the PayPal link on the tutorial you want to download.');return;
}
const back=document.getElementById('payment-back');
if(!/^\/(?:posts|tutorials)\/[a-z0-9/-]+\/$/.test(pending.page)||pending.page.includes('//')||!pending.claim?.match(/^[a-f0-9]{64}$/)){status.textContent=text('请重新从教程页进入。','Please return to the tutorial and try again.');return}
back.href=pending.page;back.textContent=pending.title;
if(!tx){status.textContent=text('尚未收到付款确认。若已付款，请从 PayPal 的付款结果页返回本站。','Payment confirmation has not arrived. If you have paid, return here from your PayPal receipt.');return}
status.textContent=text('正在确认付款…','Confirming your payment…');
async function asData(url){
 const r=await fetch(url);if(!r.ok)throw Error('asset');
 const blob=await r.blob();return await new Promise((resolve,reject)=>{const f=new FileReader();f.onload=()=>resolve(f.result);f.onerror=reject;f.readAsDataURL(blob)});
}
async function exportPage(path){
 const address=new URL(path,location.origin),response=await fetch(address);
 if(!response.ok)throw Error('page');
 const doc=new DOMParser().parseFromString(await response.text(),'text/html');
 const base=doc.createElement('base');base.href=address.href;doc.head.prepend(base);
 // Keep links useful while making local styles, scripts and diagrams self-contained.
 const styles=[...doc.querySelectorAll('link[rel=stylesheet]')];
 for(const link of styles){
  const url=new URL(link.getAttribute('href'),address);if(url.origin!==location.origin)continue;
  const r=await fetch(url);if(!r.ok)throw Error('style');
  const style=doc.createElement('style');style.textContent=(await r.text()).replace(/url\((['"]?)([^'")]+)\1\)/g,(whole,quote,value)=>value.startsWith('data:')||value.startsWith('#')?whole:'url('+JSON.stringify(new URL(value,url).href)+')');
  link.replaceWith(style);
 }
 for(const data of doc.querySelectorAll('.trajectory-data[data-src]')){
  const r=await fetch(new URL(data.dataset.src,address));if(!r.ok)throw Error('trajectory');
  data.textContent=await r.text();delete data.dataset.src;
 }
 for(const image of doc.querySelectorAll('img[src]')){
  const url=new URL(image.getAttribute('src'),address);if(url.origin!==location.origin)continue;
  image.setAttribute('src',await asData(url));image.removeAttribute('srcset');image.removeAttribute('loading');
 }
 for(const script of [...doc.querySelectorAll('script[src]')]){
  const url=new URL(script.getAttribute('src'),address);
  if(url.hostname.includes('googlesyndication')||url.hostname.includes('google-analytics')||url.pathname.endsWith('/paypal-support.js')){script.remove();continue}
  if(url.origin!==location.origin)continue;
  const r=await fetch(url);if(!r.ok)throw Error('script');
  const code=(await r.text()).replace(/<\/script/gi,'<\\/script');
  // Inline defer scripts must wait for the full document.
  script.removeAttribute('src');script.removeAttribute('defer');script.removeAttribute('async');
  script.textContent='document.addEventListener("DOMContentLoaded",()=>{\n'+code+'\n});';
 }
 doc.querySelectorAll('.article-support').forEach(el=>el.remove());
 for(const link of doc.querySelectorAll('a[href]')){const value=link.getAttribute('href');if(value&&!value.startsWith('#'))link.setAttribute('href',new URL(value,address).href)}
 return '<!doctype html>\n'+doc.documentElement.outerHTML;
}
(async()=>{
 try{
  const response=await fetch(SERVICE+'/verify',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({tx,claim:pending.claim,page:pending.page})});
  if(!response.ok){status.textContent=response.status===402?text('付款尚未确认完成，请稍后从 PayPal 的付款结果页返回。','Payment is not confirmed as completed. Return from your PayPal receipt once it has completed.'):text('暂时无法确认付款，请稍后从 PayPal 的付款结果页重试。','Payment confirmation is temporarily unavailable. Please retry from your PayPal receipt.');return}
  const result=await response.json();if(!result.ok)throw Error('verification');
  status.textContent=text('正在准备 HTML…','Preparing your HTML…');
  const content=await exportPage(pending.page),blob=new Blob([content],{type:'text/html;charset=utf-8'}),url=URL.createObjectURL(blob);
  const download=document.getElementById('payment-download');download.href=url;download.download=pending.page.split('/').filter(Boolean).join('-')+'.html';download.textContent=text('下载 HTML','Download HTML');download.hidden=false;download.click();
  status.textContent=text('感谢支持。HTML 已准备好。','Thank you for your support. Your HTML is ready.');
 }catch{status.textContent=text('下载准备中断，请稍后从 PayPal 的付款结果页重试。','The download was interrupted. Please retry from your PayPal receipt.')}
})();
})();
