(()=>{
'use strict';
const layout=document.querySelector('[data-explore-mode]');if(!layout)return;
const buttons=[...layout.querySelectorAll('[data-topic-filter]')],rows=[...layout.querySelectorAll('.explore-row[data-topic]')],search=layout.querySelector('[data-directory-search]'),select=layout.querySelector('[data-topic-selection]'),navSelect=layout.querySelector('[data-topic-navigation]'),empty=layout.querySelector('.directory-empty');
const normalize=value=>value.normalize('NFKC').toLocaleLowerCase().trim();
const labels=new Map(rows.map(row=>[row,normalize(row.textContent)]));
let topic=layout.dataset.activeTopic||'all';
function apply(key=topic,updateURL=true){
 const button=buttons.find(b=>b.dataset.topicFilter===key);
 if(buttons.length&&!button)key='all';
 topic=key;layout.dataset.activeTopic=key;
 buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.topicFilter===key)));
 const query=search?.value.trim()||'',terms=normalize(query).split(/\s+/).filter(Boolean);
 let count=0;for(const row of rows){row.hidden=(key!=='all'&&row.dataset.topic!==key)||!terms.every(term=>labels.get(row).includes(term));if(!row.hidden)count++;}
 const heading=layout.querySelector('[data-results-title]'),number=layout.querySelector('[data-results-count]');
 if(heading)heading.textContent=(buttons.find(b=>b.dataset.topicFilter===key)||buttons[0])?.dataset.title||heading.textContent;
 if(number)number.textContent=count;if(empty)empty.hidden=count!==0;if(select)select.value=key;
 const update=url=>{if(buttons.length&&key!=='all')url.searchParams.set('topic',key);else url.searchParams.delete('topic');if(query)url.searchParams.set('q',query);else url.searchParams.delete('q');return url;};
 if(updateURL){const url=update(new URL(location));history.replaceState(history.state,'',url.pathname+url.search+url.hash);}
 document.querySelectorAll('.lang-switch a[href]').forEach(link=>{const url=update(new URL(link.getAttribute('href'),location.href));link.setAttribute('href',url.pathname+url.search+url.hash);});
}
function restore(){const params=new URLSearchParams(location.search);if(search)search.value=params.get('q')||'';apply(params.get('topic')||layout.dataset.activeTopic||'all',false);}
buttons.forEach(button=>button.addEventListener('click',()=>apply(button.dataset.topicFilter)));
search?.addEventListener('input',()=>apply());select?.addEventListener('change',()=>apply(select.value));
navSelect?.addEventListener('change',()=>location.assign(navSelect.value));
addEventListener('popstate',restore);restore();
})();
