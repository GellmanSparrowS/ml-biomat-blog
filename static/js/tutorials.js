/* Search and topic filters progressively enhance the complete lesson list. */
(function(){
  'use strict';
  var input=document.getElementById('tutorial-search');
  if(!input)return;
  var items=Array.from(document.querySelectorAll('[data-tutorial-item]'));
  var buttons=Array.from(document.querySelectorAll('[data-tutorial-filter]'));
  var category='all';
  function apply(){
    var words=input.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean),count=0;
    items.forEach(function(item){
      var matches=words.every(function(word){return item.dataset.search.toLocaleLowerCase().includes(word);});
      var included=category==='all'||item.dataset.categories.split(' ').includes(category);
      item.hidden=!(matches&&included);if(!item.hidden)count++;
    });
    document.querySelectorAll('[data-tutorial-group]').forEach(function(group){group.hidden=!group.querySelector('[data-tutorial-item]:not([hidden])');});
    document.getElementById('tutorial-count').textContent=count+' 节教程';
    document.getElementById('tutorial-empty').hidden=count!==0;
    buttons.forEach(function(button){var active=button.dataset.tutorialFilter===category;button.classList.toggle('active',active);button.setAttribute('aria-pressed',String(active));});
  }
  input.addEventListener('input',apply);
  buttons.forEach(function(button){button.addEventListener('click',function(){category=button.dataset.tutorialFilter;apply();});});
})();
