/* The publisher/account identifiers are public, not credentials.
 * Only request the single manual footer unit on the production domain.
 * Responsive sizing and unfilled collapse follow Google's published examples.
 */
(() => {
  'use strict';
  const panel = document.querySelector('.site-sponsor');
  if (!panel || !['ml-biomat.com', 'www.ml-biomat.com'].includes(location.hostname)) return;
  const unit = panel.querySelector('.adsbygoogle');
  if (!unit || panel.dataset.initialized) return;
  panel.dataset.initialized = 'true';

  const sync = () => {
    const status = unit.getAttribute('data-ad-status');
    panel.hidden = status === 'unfilled' || status === 'unfill-optimized';
  };
  const observer = new MutationObserver(sync);
  observer.observe(unit, {attributes: true, attributeFilter: ['data-ad-status']});

  function requestAd() {
    // Make the unit measurable before requesting it; never hide a filled ad.
    panel.hidden = false;
    const loader = document.createElement('script');
    loader.async = true;
    loader.crossOrigin = 'anonymous';
    loader.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7464969092761889';
    loader.onload = () => {
      try {
        (window.adsbygoogle = window.adsbygoogle || []).push({});
      } catch (error) {
        if (unit.getAttribute('data-ad-status') !== 'filled') panel.hidden = true;
      }
    };
    loader.onerror = () => { panel.hidden = true; observer.disconnect(); };
    document.head.appendChild(loader);
  }
  const footer = document.querySelector('.site-footer');
  if (unit.dataset.adSlot === '7246054217' && footer && 'IntersectionObserver' in window) {
    const nearFooter = new IntersectionObserver(entries => {
      if (!entries.some(entry => entry.isIntersecting)) return;
      nearFooter.disconnect();
      requestAd();
    }, {rootMargin:'800px'});
    nearFooter.observe(footer);
  } else {
    requestAd();
  }
})();
