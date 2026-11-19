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
  let links = [], index = 0, opener = null, overflow = '', version = 0, pending = null;
  // Coordinates are relative to the centre of the fitted image.
  let scale = 1, dx = 0, dy = 0;
  const fingers = new Map();
  image.draggable = false;
  function resetZoom() {
    scale = 1; dx = dy = 0; fingers.clear();
    image.style.transform = '';
    stage.classList.remove('is-zoomed');
  }
  function move(from, to, factor) {
    if (image.hidden || !image.naturalWidth) return;
    const bounds = stage.getBoundingClientRect();
    const cx = bounds.left + bounds.width / 2, cy = bounds.top + bounds.height / 2;
    const nextScale = Math.max(1, Math.min(12, scale * factor));
    const ratio = nextScale / scale;
    const fit = Math.min(image.clientWidth / image.naturalWidth, image.clientHeight / image.naturalHeight);
    const limitX = Math.max(0, (image.naturalWidth * fit * nextScale - bounds.width) / 2);
    const limitY = Math.max(0, (image.naturalHeight * fit * nextScale - bounds.height) / 2);
    dx = Math.max(-limitX, Math.min(limitX, to.x - cx - (from.x - cx - dx) * ratio));
    dy = Math.max(-limitY, Math.min(limitY, to.y - cy - (from.y - cy - dy) * ratio));
    scale = nextScale;
    image.style.transform = `translate(${dx}px,${dy}px) scale(${scale})`;
    stage.classList.toggle('is-zoomed', scale > 1);
  }
  function gesture() {
    const [a, b] = fingers.values();
    return b ? {x:(a.x+b.x)/2, y:(a.y+b.y)/2, distance:Math.hypot(a.x-b.x,a.y-b.y)} : {...a, distance:0};
  }
  stage.addEventListener('wheel', event => {
    if (image.hidden) return;
    event.preventDefault();
    const point = {x:event.clientX, y:event.clientY};
    const unit = event.deltaMode === 1 ? 16 : event.deltaMode === 2 ? stage.clientHeight : 1;
    move(point, point, Math.exp(-Math.max(-500, Math.min(500, event.deltaY * unit)) * .002));
  }, {passive:false});
  stage.addEventListener('pointerdown', event => {
    if (event.button !== 0 || fingers.size >= 2 || image.hidden) return;
    fingers.set(event.pointerId, {x:event.clientX, y:event.clientY});
    stage.setPointerCapture(event.pointerId);
  });
  stage.addEventListener('pointermove', event => {
    if (!fingers.has(event.pointerId)) return;
    const before = gesture();
    fingers.set(event.pointerId, {x:event.clientX, y:event.clientY});
    const after = gesture();
    move(before, after, before.distance && after.distance ? after.distance / before.distance : 1);
  });
  stage.addEventListener('lostpointercapture', event => fingers.delete(event.pointerId));
  stage.addEventListener('pointerup', event => fingers.delete(event.pointerId));
  stage.addEventListener('pointercancel', event => fingers.delete(event.pointerId));
  window.addEventListener('resize', resetZoom);
  function render(step) {
    resetZoom();
    index = (step + links.length) % links.length;
    const link = links[index], thumbnail = link.querySelector('img');
    const ticket = ++version;
    if (pending) pending.removeAttribute('src');
    stage.scrollTo(0, 0);
    stage.setAttribute('aria-busy', 'true');
    error.hidden = true;
    image.alt = link.dataset.caption || '';
    const preview = thumbnail && thumbnail.complete && thumbnail.naturalWidth ? thumbnail.currentSrc : '';
    if (preview) { image.src = preview; image.hidden = false; }
    else { image.removeAttribute('src'); image.hidden = true; }
    // Retain a cached preview while decoding the requested original in the background.
    const full = thumbnail && thumbnail.dataset.fullSrc || link.href;
    const original = new Image();
    pending = original; original.decoding = 'async';
    original.onload = async () => {
      try { if (original.decode) await original.decode(); } catch (_) {}
      if (ticket !== version || !dialog.open) return;
      image.src = full; image.hidden = false; error.hidden = true;
      stage.removeAttribute('aria-busy'); pending = null;
    };
    original.onerror = () => {
      if (ticket !== version || !dialog.open) return;
      image.hidden = !preview; error.hidden = !!preview;
      stage.removeAttribute('aria-busy'); pending = null;
    };
    original.src = full;
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
    version++; if (pending) pending.removeAttribute('src'); pending = null;
    image.removeAttribute('src'); image.hidden = true; stage.removeAttribute('aria-busy');
    document.body.style.overflow = overflow;
    if (opener) opener.focus({preventScroll:true});
  });
})();
