(() => {
  'use strict';
  const config = document.currentScript.dataset;
  const lab = document.getElementById(config.lab);
  if (!lab) return;
  let pending = false;
  function load(src) {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = src;
      script.onload = resolve;
      script.onerror = () => { script.remove(); reject(new Error('Script unavailable')); };
      document.head.append(script);
    });
  }
  async function activate() {
    if (pending) return;
    pending = true;
    try {
      if (!window.Plotly) await load(config.library);
      await load(config.script);
      lab.removeEventListener('pointerdown', activate);
      lab.removeEventListener('focusin', activate);
    } catch {
      pending = false;
    }
  }
  lab.addEventListener('focusin', activate);
  lab.addEventListener('pointerdown', activate);
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      if (!entries.some(entry => entry.isIntersecting)) return;
      observer.disconnect(); activate();
    }, {rootMargin:'1000px'});
    observer.observe(lab);
  } else activate();
})();
