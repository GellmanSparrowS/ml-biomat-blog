/* Automatic motion for every new visitor, with optional off / system-following choices.
 * ?motion=on / off / auto applies once, is remembered, and is removed from the URL.
 */
(()=>{
 'use strict';
 const key='ml-biomat-motion',system=matchMedia('(prefers-reduced-motion: reduce)');
 const listeners=new Set(),valid=value=>['on','off','auto'].includes(value);
 const defaultMode='on';
 let mode=defaultMode;
 try{const saved=localStorage.getItem(key);if(valid(saved))mode=saved;}catch(_){}
 const url=new URL(location.href),requested=url.searchParams.get('motion');
 if(valid(requested)){
  mode=requested;try{localStorage.setItem(key,mode);}catch(_){}
  url.searchParams.delete('motion');
  try{history.replaceState(history.state,'',url.pathname+url.search+url.hash);}catch(_){}
 }
 const matches=()=>mode==='off'||(mode==='auto'&&system.matches);
 function notify(){
  document.documentElement.dataset.motion=matches()?'reduced':'full';
  document.documentElement.dataset.motionPreference=mode;
  const event={type:'change',matches:matches(),mode,systemReduced:system.matches};
  for(const callback of listeners)try{callback(event);}catch(error){console.error(error);}
 }
 window.siteMotion={
  get matches(){return matches();},get mode(){return mode;},get systemReduced(){return system.matches;},
  addEventListener(type,callback){if(type==='change')listeners.add(callback);},
  removeEventListener(type,callback){if(type==='change')listeners.delete(callback);},
  addListener(callback){listeners.add(callback);},removeListener(callback){listeners.delete(callback);},
  set(value){if(!valid(value))return;mode=value;try{localStorage.setItem(key,value);}catch(_){}notify();}
 };
 if(system.addEventListener)system.addEventListener('change',notify);else system.addListener(notify);
 addEventListener('storage',event=>{if(event.key===key||event.key===null){mode=valid(event.newValue)?event.newValue:defaultMode;notify();}});
 notify();
})();
