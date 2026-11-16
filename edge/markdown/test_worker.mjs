import assert from 'node:assert/strict';
import {handle, prefersMarkdown, markdownPath} from './worker.mjs';
const base = 'https://ml-biomat.com';
const html = '<!doctype html><h1>公开教程</h1>';
const markdown = '# 公开教程\n\n```python\nprint(1)\n```\n';
const results = [];
async function test(name, run) {
  try { await run(); results.push({name, pass: true}); }
  catch (error) { results.push({name, pass: false, error: error.message}); }
}
function origin({missing = false, derivativeError = false, derivativeRedirect = false, derivativeHTML = false} = {}) {
  const calls = [], cache = new Map();
  const fetch = async request => {
    calls.push(request);
    const url = new URL(request.url), isMD = url.pathname.endsWith('/index.md') || url.pathname === '/auth.md';
    if (isMD && derivativeError) throw new Error('origin unavailable');
    if (isMD && derivativeRedirect) return new Response(null, {status: 302, headers: {Location: 'https://external.invalid/'}});
    if (isMD && derivativeHTML) return new Response('<html>Challenge</html>', {headers: {'content-type': 'text/html'}});
    const cacheKey = request.method + ' ' + request.url;
    if (!cache.has(cacheKey)) cache.set(cacheKey, {body: isMD ? markdown : html, headers: {'content-type': isMD ? 'text/plain; charset=utf-8' : 'text/html; charset=utf-8', 'cache-control': 'public, max-age=600', vary: 'Accept-Encoding', 'strict-transport-security': 'max-age=31536000', 'content-security-policy': "default-src 'self'", etag: isMD ? '"markdown"' : '"html"'}});
    const response = cache.get(cacheKey);
    return new Response(request.method === 'HEAD' ? null : response.body, {status: missing ? 404 : 200, headers: response.headers});
  };
  return {fetch, calls, cache};
}
function request(path = '/tutorials/machine-learning/m01/', options = {}) { return new Request(base + path, options); }
await test('HTML remains default, including wildcard browser requests', async () => {
  for (const accept of [undefined, '*/*', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,*/*;q=0.8']) {
    const server = origin();
    const response = await handle(request(undefined, accept ? {headers: {Accept: accept}} : {}), server.fetch);
    assert.equal(await response.text(), html); assert.equal(server.calls.length, 1); assert.match(response.headers.get('vary'), /Accept/);
  }
});
await test('Explicit Markdown, parameters, upper case and q=0', () => {
  assert.equal(prefersMarkdown('text/markdown'), true);
  assert.equal(prefersMarkdown('TEXT/MARKDOWN; charset=utf-8; q=0.8,text/html;q=0.5'), true);
  for (const accept of ['text/markdown;q=0', 'text/markdown;q=0.001,text/html;q=1', 'text/markdown;q=abc', 'text/markdown;q=1.001', 'text/markdown;q=0.1234']) assert.equal(prefersMarkdown(accept), false, accept);
});
await test('Wildcard quality does not outrank an explicit HTML exclusion', () => {
  assert.equal(prefersMarkdown('text/markdown;q=0.2, text/html;q=0, */*;q=1'), true);
});
await test('Wildcard quality prefers HTML when explicitly higher', () => {
  assert.equal(prefersMarkdown('text/markdown;q=0.2, */*;q=1'), false);
  assert.equal(prefersMarkdown('text/markdown;q=0.2, text/*;q=0.9'), false);
});
await test('Markdown metadata and origin security headers', async () => {
  const server = origin();
  const response = await handle(request(undefined, {headers: {Accept: 'text/markdown'}}), server.fetch);
  assert.equal(await response.text(), markdown); assert.match(response.headers.get('content-type'), /^text\/markdown/);
  assert.equal(response.headers.get('etag'), '"markdown"'); assert.equal(response.headers.get('x-robots-tag'), 'noindex');
  assert.equal(response.headers.get('x-content-type-options'), 'nosniff');
  assert.equal(response.headers.get('strict-transport-security'), 'max-age=31536000');
  assert.equal(response.headers.get('content-security-policy'), "default-src 'self'");
  assert.match(response.headers.get('link'), /\/tutorials\/machine-learning\/m01\/>; rel="canonical"; type="text\/html"/);
  assert.equal(response.headers.get('vary'), 'Accept-Encoding, Accept');
  assert.equal(new URL(server.calls[0].url).pathname, '/tutorials/machine-learning/m01/index.md');
});
await test('HTML and Markdown never share the same origin cache entry', async () => {
  const server = origin();
  const md = await handle(request(undefined, {headers: {Accept: 'text/markdown'}}), server.fetch);
  const browser = await handle(request(), server.fetch);
  const again = await handle(request(undefined, {headers: {Accept: 'text/markdown'}}), server.fetch);
  assert.equal(await md.text(), markdown); assert.equal(await browser.text(), html); assert.equal(await again.text(), markdown);
  assert.equal(server.cache.size, 2); assert.equal(browser.headers.get('etag'), '"html"');
});
await test('HEAD has Markdown metadata and no body', async () => {
  const server = origin();
  const response = await handle(request(undefined, {method: 'HEAD', headers: {Accept: 'text/markdown'}}), server.fetch);
  assert.equal(await response.text(), ''); assert.match(response.headers.get('content-type'), /^text\/markdown/); assert.equal(server.calls[0].method, 'HEAD');
});
await test('Authorization, Range and POST bypass transformation intact', async () => {
  for (const options of [{headers: {Authorization: 'Bearer synthetic-test-only', Accept: 'text/markdown'}}, {headers: {Range: 'bytes=0-3', Accept: 'text/markdown'}}, {method: 'POST', headers: {Accept: 'text/markdown'}, body: 'example'}]) {
    const server = origin(), incoming = request(undefined, options);
    const response = await handle(incoming, server.fetch);
    assert.equal(server.calls.length, 1); assert.equal(server.calls[0], incoming); assert.match(response.headers.get('content-type'), /^text\/html/);
  }
});
await test('Missing derivative preserves the origin 404', async () => {
  const server = origin({missing: true});
  const response = await handle(request('/tutorials/not-published/', {headers: {Accept: 'text/markdown'}}), server.fetch);
  assert.equal(response.status, 404); assert.match(response.headers.get('content-type'), /^text\/html/); assert.equal(server.calls.length, 2);
});
await test('Unavailable, redirected or HTML derivatives fall back to HTML', async () => {
  for (const options of [{derivativeError: true}, {derivativeRedirect: true}, {derivativeHTML: true}]) {
    const server = origin(options);
    const response = await handle(request(undefined, {headers: {Accept: 'text/markdown'}}), server.fetch);
    assert.equal(await response.text(), html); assert.equal(server.calls.length, 2);
    assert(server.calls.every(call => new URL(call.url).hostname === 'ml-biomat.com'));
  }
});
await test('Direct Markdown has correct type and canonical HTML companion', async () => {
  const server = origin();
  const response = await handle(request('/tutorials/machine-learning/m01/index.md'), server.fetch);
  assert.match(response.headers.get('content-type'), /^text\/markdown/); assert.match(response.headers.get('link'), /m01\/>; rel="canonical"/); assert.equal(server.calls.length, 1);
});
await test('Auth discovery document does not claim to be an HTML page', async () => {
  const response = await handle(request('/auth.md'), origin().fetch);
  assert.match(response.headers.get('content-type'), /^text\/markdown/);
  assert(!/type="text\/html"/.test(response.headers.get('link') || ''));
});
await test('Query strings and cookies do not reach Markdown derivative requests', async () => {
  const server = origin();
  await handle(request('/tutorials/machine-learning/m01/?utm_source=example', {headers: {Accept: 'text/markdown', Cookie: 'example=not-a-real-cookie'}}), server.fetch);
  assert.equal(new URL(server.calls[0].url).search, ''); assert.equal(server.calls[0].headers.get('cookie'), null);
});
await test('Hostile or unsupported paths cause no derivative or external fetch', async () => {
  for (const path of ['/payment/', '/static/secret/', '/.well-known/anything/', '//external.invalid/', '/tutorials/a%2Fb/', '/tutorials//evil/', '/tutorials/a/../../payment/']) {
    const server = origin();
    await handle(request(path, {headers: {Accept: 'text/markdown'}}), server.fetch);
    assert.equal(server.calls.length, 1, path); assert.equal(new URL(server.calls[0].url).hostname, 'ml-biomat.com', path);
  }
  const server = origin();
  const other = new Request('https://example.invalid/tutorials/a/', {headers: {Accept: 'text/markdown'}});
  await handle(other, server.fetch);
  assert.equal(server.calls.length, 1); assert.equal(server.calls[0], other);
});
await test('Home, index.html and article collections have Markdown paths', () => {
  assert.equal(markdownPath('/'), '/index.md');
  assert.equal(markdownPath('/tutorials/machine-learning/m01/index.html'), '/tutorials/machine-learning/m01/index.md');
  assert.equal(markdownPath('/articles/'), '/articles/index.md');
});
await test('Encoded Unicode topics remain readable without accepting encoded separators', () => {
  assert.equal(markdownPath('/tags/%E4%B8%9D%E7%B4%A0/'), '/tags/%E4%B8%9D%E7%B4%A0/index.md');
  assert.equal(markdownPath('/tutorials/%2e%2e/payment/'), null);
  assert.equal(markdownPath('/tutorials/%2fprivate/'), null);
  assert.equal(markdownPath('/tags/MD%20simulation/'), '/tags/MD%20simulation/index.md');
  assert.equal(markdownPath('/tags/%zz/'), null);
});
console.log(JSON.stringify({passed: results.filter(x => x.pass).length, failed: results.filter(x => !x.pass), cases: results.length}, null, 2));
process.exitCode = results.some(x => !x.pass) ? 1 : 0;
