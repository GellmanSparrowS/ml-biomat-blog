(() => {
  const dialog = document.querySelector('#pr-contact');
  const trigger = document.querySelector('[data-contact-open]');
  if (!trigger || !dialog || !dialog.showModal || !window.fetch) return;

  const form = dialog.querySelector('form');
  const send = form.querySelector('[type="submit"]');
  const status = form.querySelector('[role="status"]');
  const zh = document.documentElement.lang.startsWith('zh');
  const copy = (chinese, english) => zh ? chinese : english;
  trigger.setAttribute('aria-haspopup', 'dialog');
  trigger.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    dialog.showModal();
  });
  dialog.querySelector('[data-contact-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => trigger.focus());
  form.addEventListener('input', () => { if (!send.disabled) status.textContent = ''; });
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (send.disabled) return;
    const message = form.elements.message.value.trim();
    if (!message) {
      form.elements.message.focus();
      status.textContent = copy('请写下留言内容。', 'Please enter a message.');
      return;
    }
    send.disabled = true;
    form.elements.message.readOnly = true;
    form.elements.email.readOnly = true;
    status.textContent = copy('正在提交…', 'Submitting…');
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000);
    try {
      const data = new FormData(form);
      data.set('message', message);
      if (!data.get('email')) data.delete('email');
      const response = await fetch(form.action, {
        method: 'POST', headers: {Accept: 'application/json', 'Content-Type': 'application/json'},
        body: JSON.stringify(Object.fromEntries(data)), signal: controller.signal
      });
      const result = await response.json();
      if (response.ok && (result.success === true || result.success === 'true')) {
        form.reset();
        status.textContent = copy('留言已提交，谢谢联系。', 'Your message has been submitted. Thank you.');
      } else if (/activat/i.test(String(result.message))) {
        status.textContent = copy('站内留言正在启用。可使用下方邮箱直接联系，或稍后再试。', 'The contact form is being activated. Use the email link below or try again later.');
      } else {
        throw new Error('Submission not confirmed');
      }
    } catch {
      status.textContent = copy('未能确认提交，内容已保留。请稍后重试，或使用下方邮箱联系。', 'Submission could not be confirmed. Your text is still here. Try again later or use the email link below.');
    } finally {
      clearTimeout(timeout);
      send.disabled = false;
      form.elements.message.readOnly = false;
      form.elements.email.readOnly = false;
    }
  });
})();
