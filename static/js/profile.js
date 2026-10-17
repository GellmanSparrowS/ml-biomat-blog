/* Compact album viewer: native details remain usable without JavaScript. */
(function () {
    'use strict';
    var dialog = document.getElementById('photo-viewer');
    if (!dialog || typeof dialog.showModal !== 'function') return;
    var photo = document.getElementById('photo-viewer-image');
    var caption = document.getElementById('photo-viewer-caption');
    var title = document.getElementById('photo-viewer-title');
    var count = document.getElementById('photo-viewer-count');
    var original = document.getElementById('photo-viewer-original');
    var error = document.getElementById('photo-viewer-error');
    var prev = dialog.querySelector('[data-viewer-prev]');
    var next = dialog.querySelector('[data-viewer-next]');
    var links = [], index = 0, opener = null, oldOverflow = '';
    function render(step) {
        index = (step + links.length) % links.length;
        var link = links[index];
        error.hidden = true;
        photo.alt = link.dataset.caption;
        photo.src = link.href;
        caption.textContent = link.dataset.caption;
        original.href = link.href;
        count.textContent = (index + 1) + ' / ' + links.length;
        prev.disabled = next.disabled = links.length < 2;
    }
    document.querySelectorAll('[data-album-link]').forEach(function (link) {
        link.addEventListener('click', function (event) {
            if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
            event.preventDefault();
            var album = link.closest('[data-album]');
            links = Array.from(album.querySelectorAll('[data-album-link]'));
            title.textContent = album.dataset.albumTitle;
            opener = link;
            oldOverflow = document.body.style.overflow;
            render(links.indexOf(link));
            dialog.showModal();
            document.body.style.overflow = 'hidden';
        });
    });
    photo.addEventListener('error', function () { error.hidden = false; });
    photo.addEventListener('load', function () { error.hidden = true; });
    prev.addEventListener('click', function () { render(index - 1); });
    next.addEventListener('click', function () { render(index + 1); });
    dialog.querySelector('[data-viewer-close]').addEventListener('click', function () { dialog.close(); });
    dialog.addEventListener('keydown', function (event) {
        if (event.key === 'ArrowLeft') { event.preventDefault(); render(index - 1); }
        if (event.key === 'ArrowRight') { event.preventDefault(); render(index + 1); }
    });
    dialog.addEventListener('click', function (event) {
        if (event.target !== dialog) return;
        var rect = dialog.getBoundingClientRect();
        if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
    });
    dialog.addEventListener('close', function () {
        document.body.style.overflow = oldOverflow;
        if (opener) opener.focus({preventScroll: true});
    });
})();
