// Serve prebuilt public Markdown without changing the browser's HTML representation.
const HOST = 'ml-biomat.com';
const PUBLIC_ROOTS = new Set(['', 'en', 'zh', 'about', 'cv', 'fibernet', 'categories', 'articles', 'posts', 'tutorials', 'tags', 'privacy', 'tools']);

export function prefersMarkdown(accept) {
  let markdown = 0;
  const htmlQualities = new Map();
  for (const item of (accept || '').toLowerCase().split(',')) {
    const [rawType, ...params] = item.trim().split(';');
    const type = rawType.trim();
    let q = 1;
    for (const param of params) {
      const match = param.trim().match(/^q\s*=\s*(.*)$/);
      if (match) q = /^(?:0(?:\.\d{0,3})?|1(?:\.0{0,3})?)$/.test(match[1]) ? Number(match[1]) : 0;
    }
    if (type === 'text/markdown') markdown = Math.max(markdown, q);
    if (['text/html', 'text/*', '*/*'].includes(type)) htmlQualities.set(type, Math.max(htmlQualities.get(type) || 0, q));
  }
  const html = htmlQualities.get('text/html') ?? htmlQualities.get('text/*') ?? htmlQualities.get('*/*') ?? 0;
  return markdown > 0 && markdown >= html;
}

export function markdownPath(path) {
  let decoded;
  try { decoded = decodeURIComponent(path); } catch (_) { return null; }
  if (/%(?:2f|5c|2e|25|3f|23)/i.test(path) || /[\\%?#\u0000-\u001f]|\/\//.test(decoded) || decoded.split('/').some(part => part === '.' || part === '..') || !PUBLIC_ROOTS.has(decoded.split('/')[1])) return null;
  if (path.endsWith('/index.html')) return path.slice(0, -10) + 'index.md';
  if (path.endsWith('/')) return path + 'index.md';
  return null;
}

function withVary(headers) {
  const vary = headers.get('Vary');
  if (vary !== '*' && !(vary || '').split(',').some(x => x.trim().toLowerCase() === 'accept')) {
    headers.set('Vary', vary ? vary + ', Accept' : 'Accept');
  }
}

function markdownResponse(response, request, canonical) {
  const headers = new Headers(response.headers);
  headers.set('Content-Type', 'text/markdown; charset=utf-8');
  headers.set('X-Content-Type-Options', 'nosniff');
  if (new URL(request.url).pathname.endsWith('.md')) {
    const policy = headers.get('X-Robots-Tag');
    if (!(policy || '').split(',').some(rule => rule.trim().toLowerCase() === 'noindex')) {
      headers.set('X-Robots-Tag', policy ? policy + ', noindex' : 'noindex');
    }
  }
  if (canonical) headers.set('Link', `<${canonical}>; rel="canonical"; type="text/html"`);
  headers.set('Cache-Control', 'public, max-age=300');
  withVary(headers);
  return new Response(request.method === 'HEAD' ? null : response.body, {status:response.status, headers});
}

export async function handle(request, fetchOrigin = fetch) {
  const url = new URL(request.url);
  const safeRead = ['GET', 'HEAD'].includes(request.method) && url.hostname === HOST && !request.headers.has('Authorization') && !request.headers.has('Range');
  const legacyTag = safeRead && /^\/tags\/(Mamba|Python)(\/en)?\/?$/.exec(url.pathname);
  if (legacyTag) {
    url.pathname = '/tags/' + legacyTag[1].toLowerCase() + (legacyTag[2] || '') + '/';
    return Response.redirect(url.href, 301);
  }
  const path = markdownPath(url.pathname);
  if (safeRead && path && prefersMarkdown(request.headers.get('Accept'))) {
    const alternate = new URL(request.url);
    alternate.pathname = path;
    alternate.search = '';
    const headers = new Headers({'Accept':'text/plain, text/markdown', 'User-Agent':request.headers.get('User-Agent') || 'ML-Biomat-Markdown'});
    try {
      const result = await fetchOrigin(new Request(alternate, {method:request.method,headers,redirect:'manual'}));
      if (result.status === 200 && /^(?:text\/plain|text\/markdown)(?:;|$)/i.test(result.headers.get('Content-Type') || '')) {
        return markdownResponse(result, request, url.origin + url.pathname.replace(/index\.html$/, ''));
      }
      if (result.body) await result.body.cancel();
    } catch (_) { /* An unavailable derivative must never take the HTML page offline. */ }
  }
  const response = await fetchOrigin(request);
  if (!safeRead) return response;
  const type = response.headers.get('Content-Type') || '';
  if (response.status === 200 && (url.pathname === '/auth.md' || url.pathname.endsWith('/index.md')) && /^text\/(plain|markdown)(;|$)/i.test(type)) {
    return markdownResponse(response, request, url.pathname === '/auth.md' ? null : url.origin + url.pathname.replace(/index\.md$/, ''));
  }
  if (/^text\/html(?:;|$)/i.test(type) && path) {
    const headers = new Headers(response.headers);
    withVary(headers);
    return new Response(response.body, {status:response.status, statusText:response.statusText, headers});
  }
  return response;
}

export default {fetch(request) {return handle(request);}};
