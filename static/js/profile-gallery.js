/* Local profile gallery: images and activity titles are the only page-level triggers. */
(() => {
  'use strict';
  const root = document.querySelector('.profile-redesign');
  if (!root) return;
  const dialog = root.querySelector('.pr-viewer');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const image = dialog.querySelector('.pr-viewer-stage img');
  const stage = dialog.querySelector('.pr-viewer-stage');
  const caption = dialog.querySelector('#pr-viewer-caption');
  const title = dialog.querySelector('#pr-viewer-title');
  const count = dialog.querySelector('[data-pr-count]');
  const prev = dialog.querySelector('[data-pr-prev]');
  const next = dialog.querySelector('[data-pr-next]');
  const controls = dialog.querySelector('.pr-viewer-controls');
  const error = dialog.querySelector('.pr-viewer-error');
  let links = [], index = 0, opener = null, overflow = '';
  function render(step) {
    index = (step + links.length) % links.length;
    const link = links[index];
    stage.scrollTo(0, 0);
    stage.setAttribute('aria-busy', 'true');
    error.hidden = true;
    image.hidden = true;
    image.alt = link.dataset.caption || '';
    image.src = link.href;
    if (image.complete && image.naturalWidth) {
      image.hidden = false;
      stage.removeAttribute('aria-busy');
    }
    caption.textContent = image.alt;
    count.textContent = (index + 1) + ' / ' + links.length;
    controls.hidden = links.length < 2;
  }
  function open(gallery, link, trigger) {
    links = [...gallery.querySelectorAll('[data-pr-image]')];
    if (!links.length) return;
    opener = trigger;
    title.textContent = gallery.dataset.title;
    overflow = document.body.style.overflow;
    render(Math.max(0, links.indexOf(link)));
    dialog.showModal();
    document.body.style.overflow = 'hidden';
  }
  function modified(event) {
    return event.ctrlKey || event.metaKey || event.shiftKey || event.altKey;
  }
  root.querySelectorAll('[data-pr-image]').forEach(link => {
    link.addEventListener('click', event => {
      if (modified(event)) return;
      event.preventDefault();
      open(link.closest('[data-pr-gallery]'), link, link);
    });
  });
  root.querySelectorAll('[data-pr-open]').forEach(link => {
    link.addEventListener('click', event => {
      if (modified(event)) return;
      event.preventDefault();
      const gallery = link.closest('[data-pr-gallery]');
      open(gallery, gallery.querySelector('[data-pr-image]'), link);
    });
  });
  image.addEventListener('error', () => {
    image.hidden = true; error.hidden = false; stage.removeAttribute('aria-busy');
  });
  image.addEventListener('load', () => {
    image.hidden = false; error.hidden = true; stage.removeAttribute('aria-busy');
  });
  prev.addEventListener('click', () => render(index - 1));
  next.addEventListener('click', () => render(index + 1));
  dialog.querySelector('[data-pr-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') { event.preventDefault(); render(index - 1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); render(index + 1); }
  });
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const r = dialog.getBoundingClientRect();
    if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.body.style.overflow = overflow;
    if (opener) opener.focus({preventScroll:true});
  });
})();
