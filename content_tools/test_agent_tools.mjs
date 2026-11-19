import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const source = fs.readFileSync('static/js/agent-tools.js', 'utf8');
const index = JSON.parse(fs.readFileSync('docs/search.json', 'utf8'));
const pageText = '# Tutorial\n\nA formula: $E=mc^2$.\n\n```python\nprint(1)\n```\n\n' + '研究方法与完整代码。'.repeat(2400);
let checks = 0;
function check(condition, message) { assert(condition, message); checks++; }
function setup({legacy = false, supported = true, language = 'zh-CN', failRegistration = false, markdown = pageText, html = false} = {}) {
  const registered = new Map(), registrations = [], calls = [], events = new Map(), unregistered = [];
  const api = {
    registerTool(tool, options) {
      registrations.push({tool, options});
      if (failRegistration) return Promise.reject(new Error('permission denied'));
      registered.set(tool.name, tool);
      options.signal.addEventListener('abort', () => registered.delete(tool.name), {once: true});
      return legacy ? undefined : Promise.resolve();
    },
    unregisterTool(name) { unregistered.push(name); registered.delete(name); }
  };
  const manifest = {version: 1, pages: [
    {url: '/tutorials/machine-learning/m22/', markdown: '/tutorials/machine-learning/m22/index.md', title: '图神经网络', lang: 'zh'},
    {url: '/YunhaoYang/', markdown: '/YunhaoYang/index.md', title: '个人主页', lang: 'zh'},
    {url: '/fibernet/', markdown: 'https://external.invalid/data.md'},
    {url: '/payment/', markdown: '/payment/index.md'},
    {url: '/cv/', markdown: '/not-public.md'}
  ]};
  const document = {documentElement: {lang: language}}, navigator = {};
  if (supported) (legacy ? navigator : document).modelContext = api;
  const window = {addEventListener(name, handler) { events.set(name, handler); }};
  const fetch = async (url, options) => {
    calls.push({url, options});
    if (options.signal.aborted) throw new DOMException('aborted', 'AbortError');
    const path = new URL(url).pathname;
    if (path === '/search.json') return new Response(JSON.stringify(index), {headers: {'content-type': 'application/json'}});
    if (path === '/agent-index.json') return new Response(JSON.stringify(manifest), {headers: {'content-type': 'application/json'}});
    if (path.endsWith('/index.md')) return new Response(html ? '<!DOCTYPE html><html>Not found</html>' : markdown, {headers: {'content-type': html ? 'text/html' : 'text/plain'}});
    throw new Error('Unexpected fetch ' + path);
  };
  vm.runInNewContext(source, {document, navigator, window, location: {origin: 'https://ml-biomat.com'}, URL, AbortController, DOMException, setTimeout, clearTimeout, fetch});
  async function run(name, input, options) {
    const raw = await registered.get(name).execute(input, options);
    if (raw.isError) return raw;
    return JSON.parse(raw.content[0].text);
  }
  return {registered, registrations, calls, events, unregistered, run};
}
const absent = setup({supported: false});
check(absent.registrations.length === 0 && absent.calls.length === 0 && absent.events.size === 0, 'Unsupported browsers do no work');
const app = setup();
check(app.registered.size === 3 && app.calls.length === 0, 'Registers exactly three tools without eager network requests');
check(app.registrations.every(({tool, options}) => tool.annotations.readOnlyHint && !tool.annotations.consequentialHint && options.signal), 'Read-only annotations and registration signals');
const topics = await app.run('list_tutorial_topics', {language: 'any'});
check(topics.topics.reduce((n, t) => n + t.pages, 0) === index.length && topics.topics.length === 5, 'All 390 public pages counted across five topics');
const search = await app.run('search_tutorials', {query: '图神经网络', category: 'machine-learning', limit: 2});
check(search.results.length > 0 && search.results.every(item => item.language === 'zh' && item.category === 'machine-learning') && search.results.some(item => item.url.endsWith('/m22/')), 'Actual Chinese tutorial query returns graph neural networks');
const english = await app.run('search_tutorials', {query: 'graph neural', language: 'en'});
check(english.results.some(item => item.url.endsWith('/m22/en/')), 'English query finds corresponding translation');
const legacyPost = await app.run('search_tutorials', {query: 'Coarse-Grained', language: 'en'});
check(legacyPost.results.some(item => item.url === 'https://ml-biomat.com/posts/coarse-grained-biomolecular-networks/'), 'Legacy article slug resolves to public URL');
check(app.calls.filter(c => c.url.endsWith('/search.json')).length === 1, 'Successful search data cached');
for (const input of [{limit: 31}, {limit: '2'}, {language: 'fr'}, {category: '__proto__'}, {query: 'x'.repeat(201)}, {evil: true}, []]) {
  check((await app.run('search_tutorials', input)).isError, 'Rejects invalid search arguments');
}
const first = await app.run('read_page', {url: '/tutorials/machine-learning/m22/', max_characters: 1000});
const second = await app.run('read_page', {url: first.url, offset: first.next_offset, max_characters: 100000});
check(first.text + second.text === pageText && second.next_offset === null && first.total_characters === pageText.length, 'Markdown pagination preserves exact complete text, code and formula');
for (const url of ['https://external.invalid/YunhaoYang/', 'https://user:pass@ml-biomat.com/YunhaoYang/', '/YunhaoYang/?token=secret', '/payment/', '/cv/', '/fibernet/', '/unknown/', 'javascript:alert(1)', '/YunhaoYang/index.html']) {
  const before = app.calls.length;
  check((await app.run('read_page', {url})).isError, 'Rejects unsafe or unlisted URL ' + url);
  check(app.calls.length === before, 'Rejecting URL triggers no content fetch');
}
check(app.calls.every(call => call.options.method === 'GET' && call.options.credentials === 'omit' && call.options.redirect === 'error' && new URL(call.url).origin === 'https://ml-biomat.com'), 'Every request is same-origin GET, no cookies, no redirects');
const aborted = new AbortController(); aborted.abort();
await assert.rejects(app.run('search_tutorials', {}, {signal: aborted.signal}), {name: 'AbortError'}); checks++;
app.events.get('pagehide')();
check(app.registrations.every(entry => entry.options.signal.aborted) && app.registered.size === 0, 'Page departure aborts all registrations');
app.events.get('pageshow')({persisted: true});
check(app.registered.size === 3 && app.registrations.length === 6, 'Back-forward cache restoration registers tools again');
const legacy = setup({legacy: true, language: 'en'});
check(legacy.registered.size === 3 && (await legacy.run('list_tutorial_topics', {})).language === 'en', 'Legacy navigator implementation and English page default');
const invalid = setup({html: true});
check((await invalid.run('read_page', {url: '/YunhaoYang/'})).isError, 'HTML error pages never returned as Markdown');
const denied = setup({failRegistration: true});
await new Promise(resolve => setTimeout(resolve, 10));
check(denied.registered.size === 0 && denied.calls.length === 0, 'Rejected registrations are handled without network requests');
console.log(JSON.stringify({passed: checks, indexed_pages: index.length, tools: [...app.registered.keys()]}));
