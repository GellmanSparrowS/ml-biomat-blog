(()=>{
const layout=document.querySelector('[data-explore-mode]');
if(!layout)return;
const buttons=[...layout.querySelectorAll('[data-topic-filter]')],rows=[...layout.querySelectorAll('.explore-row[data-topic]')],select=layout.querySelector('[data-topic-selection]'),navSelect=layout.querySelector('[data-topic-navigation]');
function apply(key){
 const button=buttons.find(b=>b.dataset.topicFilter===key);if(!button)return;
 layout.dataset.activeTopic=key;
 buttons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
 const overview=layout.querySelector('.topic-overview'),results=layout.querySelector('.explore-results');
 const showOverview=layout.dataset.exploreMode==='overview'&&key==='all';
 if(overview)overview.hidden=!showOverview;if(results)results.hidden=showOverview;
 let n=0;rows.forEach(row=>{row.hidden=key!=='all'&&row.dataset.topic!==key;if(!row.hidden)n++;});
 const title=layout.querySelector('[data-results-title]'),count=layout.querySelector('[data-results-count]');if(title)title.textContent=button.dataset.title;if(count)count.textContent=n;
 if(select)select.value=key;
 const url=new URL(location);if(key==='all')url.searchParams.delete('topic');else url.searchParams.set('topic',key);history.replaceState({},'',url);
 document.querySelectorAll('.lang-switch a[href]').forEach(link=>{const target=new URL(link.getAttribute('href'),location.href);if(key==='all')target.searchParams.delete('topic');else target.searchParams.set('topic',key);link.setAttribute('href',target.pathname+target.search+target.hash);});
}
buttons.forEach(button=>button.addEventListener('click',()=>apply(button.dataset.topicFilter)));
if(select)select.addEventListener('change',()=>apply(select.value));
if(navSelect)navSelect.addEventListener('change',()=>location.assign(navSelect.value));
const key=new URLSearchParams(location.search).get('topic');if(key)apply(key);
})();