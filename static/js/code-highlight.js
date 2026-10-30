/* Load locally hosted syntax highlighting only for code that is near the viewport.
 * It is independent of the navigation and automatic network scenes.
 */
(()=>{
 'use strict';
 function ready(){
  const blocks=[...document.querySelectorAll('pre code')].filter(code=>!code.closest('.tutorial-reader')&&!code.dataset.highlighted&&!code.classList.contains('hljs')&&!code.children.length);
  if(!blocks.length)return;
  const script=document.querySelector('script[data-highlight-js]');if(!script)return;
  let library=null;const pending=new Set();let draining=false;
  function drain(){
   if(draining||!window.hljs)return;draining=true;
   const next=()=>{
    const code=pending.values().next().value;
    if(!code){draining=false;return;}
    pending.delete(code);if(code.isConnected&&!code.dataset.highlighted)window.hljs.highlightElement(code);
    if('requestIdleCallback' in window)requestIdleCallback(next,{timeout:500});else setTimeout(next,16);
   };next();
  }
  function load(){
   if(library)return library;
   library=new Promise((resolve,reject)=>{
    const style=document.createElement('link');style.rel='stylesheet';style.href=script.dataset.highlightCss;document.head.append(style);
    const asset=document.createElement('script');asset.src=script.dataset.highlightJs;asset.async=true;
    asset.onload=resolve;asset.onerror=()=>reject(Error('Syntax highlighting unavailable'));document.head.append(asset);
   });return library;
  }
  function enqueue(code){pending.add(code);load().then(drain).catch(()=>{});}
  if('IntersectionObserver' in window){
   const observer=new IntersectionObserver(entries=>{for(const entry of entries)if(entry.isIntersecting){observer.unobserve(entry.target);enqueue(entry.target);}},{rootMargin:'400px'});
   blocks.forEach(code=>observer.observe(code));
  }else blocks.forEach(enqueue);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',ready,{once:true});else ready();
})();
