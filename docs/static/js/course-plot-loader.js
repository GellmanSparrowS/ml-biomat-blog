(() => {
  'use strict';
  const config = document.currentScript.dataset;
  const lab = document.getElementById(config.lab) || document.querySelector('.science-lab');
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
      for (const src of (config.libraries || config.library || '').split(/\s+/).filter(Boolean)) {
        if (!src.includes('/plotly.min.js') || !window.Plotly) await load(src);
      }
      await load(config.script);
      lab?.removeEventListener('pointerdown', activate);
      lab?.removeEventListener('focusin', activate);
    } catch {
      pending = false;
    }
  }
  lab?.addEventListener('focusin', activate);
  lab?.addEventListener('pointerdown', activate);
  if (lab && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      if (!entries.some(entry => entry.isIntersecting)) return;
      observer.disconnect(); activate();
    }, {rootMargin:'320px 0px'});
    observer.observe(lab);
  } else activate();
})();
