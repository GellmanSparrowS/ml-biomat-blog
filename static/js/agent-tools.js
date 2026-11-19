/* Public, read-only WebMCP tools. Specification: https://webmachinelearning.github.io/webmcp/ */
(() => {
  'use strict';
  const context = document.modelContext || navigator.modelContext;
  if (!context || typeof context.registerTool !== 'function') return;

  const origin = location.origin;
  const defaultLanguage = document.documentElement.lang.toLowerCase().startsWith('en') ? 'en' : 'zh';
  const topics = {
    'machine-learning': {zh: '机器学习', en: 'Machine learning'},
    'multiscale-modeling': {zh: '物理建模与模拟', en: 'Physical modeling and simulation'},
    'biomaterials': {zh: '材料与结构', en: 'Materials and structures'},
    'python-tutorials': {zh: 'Python 科学计算', en: 'Scientific Python'},
    'wet-lab-data': {zh: '实验表征与数据分析', en: 'Characterization and data analysis'}
  };
  let lifecycle = null;
  let searchCache = null;
  let pageCache = null;
  const owned = new Set();

  function objectInput(input, keys) {
    if (!input || typeof input !== 'object' || Array.isArray(input)) throw new Error('Expected an input object.');
    if (Object.keys(input).some(key => !keys.includes(key))) throw new Error('Unknown input property.');
  }
  function language(value) {
    const lang = value === undefined ? defaultLanguage : value;
    if (!['zh', 'en', 'any'].includes(lang)) throw new Error('language must be zh, en, or any.');
    return lang;
  }
  function integer(value, fallback, min, max) {
    if (value === undefined) return fallback;
    if (!Number.isInteger(value) || value < min || value > max) throw new Error(`Expected an integer between ${min} and ${max}.`);
    return value;
  }
  function canonical(value) {
    if (typeof value !== 'string' || !value || value.length > 1024 || /[\\\u0000-\u0020]/.test(value)) throw new Error('Provide a public page URL on this site.');
    const url = new URL(value, origin);
    if (url.origin !== origin || url.username || url.password || url.search || !['http:', 'https:'].includes(url.protocol)) throw new Error('Only public same-origin page URLs without query parameters are supported.');
    if (!/^\/(?:[a-zA-Z0-9_-]+\/)*$/.test(url.pathname)) throw new Error('Use the canonical page URL ending in /.');
    return url;
  }
  function readablePath(path) {
    return /^\/(?:en\/)?$/.test(path) || /^\/(?:YunhaoYang|cv|fibernet)(?:\/en)?\/$/.test(path) || /^\/(?:posts|tutorials|categories|articles)\//.test(path);
  }
  function result(value) {
    return {content: [{type: 'text', text: typeof value === 'string' ? value : JSON.stringify(value)}]};
  }
  function wrap(fn) {
    return async (input, options = {}) => {
      const controller = new AbortController();
      const signals = [lifecycle && lifecycle.signal, options.signal].filter(Boolean);
      const abort = () => controller.abort();
      for (const signal of signals) {
        if (signal.aborted) controller.abort();
        else signal.addEventListener('abort', abort, {once: true});
      }
      const timer = setTimeout(abort, 30000);
      try {
        if (controller.signal.aborted) throw new DOMException('Tool execution cancelled.', 'AbortError');
        return result(await fn(input || {}, controller.signal));
      } catch (error) {
        if (controller.signal.aborted || error.name === 'AbortError') throw new DOMException('Tool execution cancelled.', 'AbortError');
        return {isError: true, content: [{type: 'text', text: error.message || 'The public resource could not be read.'}]};
      } finally {
        clearTimeout(timer);
        signals.forEach(signal => signal.removeEventListener('abort', abort));
      }
    };
  }
  async function publicText(path, signal, type) {
    const url = new URL(path, origin);
    if (url.origin !== origin || url.search || url.hash || url.username || url.password) throw new Error('Invalid public resource URL.');
    const response = await fetch(url.href, {method: 'GET', credentials: 'omit', redirect: 'error', signal, headers: {Accept: type === 'json' ? 'application/json' : 'text/markdown, text/plain;q=0.9'}});
    if (!response.ok) throw new Error(`Public resource unavailable (HTTP ${response.status}).`);
    const contentType = (response.headers.get('content-type') || '').toLowerCase();
    if (contentType.includes('text/html')) throw new Error('The requested public text resource returned HTML.');
    const text = await response.text();
    if (text.length > 3000000) throw new Error('Public resource exceeds the supported size.');
    if (/^\s*(?:<!doctype\s+html|<html\b)/i.test(text)) throw new Error('The requested public text resource returned HTML.');
    return text;
  }
  async function searchIndex(signal) {
    if (searchCache) return searchCache;
    const raw = JSON.parse(await publicText('/search.json', signal, 'json'));
    if (!Array.isArray(raw)) throw new Error('The tutorial index is unavailable.');
    searchCache = raw.flatMap(item => {
      if (!item || !['zh', 'en'].includes(item.lang) || !Object.hasOwn(topics, item.category) || typeof item.title !== 'string') return [];
      try {
        const url = canonical(item.url || `/posts/${item.slug}/`);
        if (!/^\/(?:tutorials|posts)\//.test(url.pathname)) return [];
        return [{title: item.title, description: String(item.description || ''), category: item.category, language: item.lang, url: url.href, tags: Array.isArray(item.tags) ? item.tags.filter(tag => typeof tag === 'string') : []}];
      } catch (_) { return []; }
    });
    return searchCache;
  }
  async function pages(signal) {
    if (pageCache) return pageCache;
    const data = JSON.parse(await publicText('/agent-index.json', signal, 'json'));
    if (!data || !Array.isArray(data.pages)) throw new Error('The public Markdown index is unavailable.');
    pageCache = new Map();
    for (const item of data.pages) {
      try {
        const url = canonical(item.url);
        if (!readablePath(url.pathname)) continue;
        const markdown = new URL(item.markdown, origin);
        if (markdown.origin !== origin || markdown.pathname !== `${url.pathname}index.md` || markdown.search || markdown.hash || markdown.username || markdown.password) continue;
        pageCache.set(url.pathname, {url: url.href, markdown: markdown.href, title: String(item.title || ''), language: item.lang});
      } catch (_) { /* Ignore invalid public index records. */ }
    }
    return pageCache;
  }
  const languageSchema = {type: 'string', enum: ['zh', 'en', 'any'], description: 'Default: current page language. any searches both languages.'};
  const annotations = {readOnlyHint: true, untrustedContentHint: true, consequentialHint: false};
  const tools = [
    {
      name: 'search_tutorials', title: defaultLanguage === 'zh' ? '搜索教程' : 'Search tutorials',
      description: 'Search published ML-Biomat tutorial and article titles, descriptions, and topic tags. Returns public links; does not navigate or change the page. This is a metadata search, not a full-text body search.',
      annotations,
      inputSchema: {type: 'object', properties: {query: {type: 'string', maxLength: 200, description: 'Words or a phrase; an empty query lists matching tutorials.'}, language: languageSchema, category: {type: 'string', enum: Object.keys(topics)}, limit: {type: 'integer', minimum: 1, maximum: 30, default: 10}}, additionalProperties: false},
      execute: wrap(async (input, signal) => {
        objectInput(input, ['query', 'language', 'category', 'limit']);
        const query = input.query === undefined ? '' : input.query;
        if (typeof query !== 'string' || query.length > 200) throw new Error('query must be text no longer than 200 characters.');
        const lang = language(input.language);
        if (input.category !== undefined && !Object.hasOwn(topics, input.category)) throw new Error('Unknown tutorial category.');
        const limit = integer(input.limit, 10, 1, 30);
        const normal = text => text.normalize('NFKC').toLowerCase();
        const terms = normal(query).trim().split(/\s+/).filter(Boolean);
        const matches = (await searchIndex(signal)).filter(item => (lang === 'any' || item.language === lang) && (!input.category || item.category === input.category)).map((item, order) => {
          const title = normal(item.title), tags = normal(item.tags.join(' ')), description = normal(item.description);
          const scores = terms.map(term => title.includes(term) ? 30 : tags.includes(term) ? 15 : description.includes(term) ? 5 : 0);
          return {item, order, score: scores.every(Boolean) ? scores.reduce((a, b) => a + b, 0) : -1};
        }).filter(match => match.score >= 0).sort((a, b) => b.score - a.score || a.order - b.order);
        return {query, language: lang, total: matches.length, results: matches.slice(0, limit).map(match => match.item)};
      })
    },
    {
      name: 'list_tutorial_topics', title: defaultLanguage === 'zh' ? '教程主题' : 'Tutorial topics',
      description: 'List the five tutorial topics with public category links and published page counts. Chinese and English translations are counted as separate pages.',
      annotations,
      inputSchema: {type: 'object', properties: {language: languageSchema}, additionalProperties: false},
      execute: wrap(async (input, signal) => {
        objectInput(input, ['language']);
        const lang = language(input.language);
        const entries = await searchIndex(signal);
        return {language: lang, count_unit: 'published pages; translations counted separately', topics: Object.entries(topics).map(([id, labels]) => ({id, name: labels[lang === 'any' ? defaultLanguage : lang], url: `${origin}/categories/${id}/${lang === 'en' ? 'en/' : ''}`, pages: entries.filter(item => item.category === id && (lang === 'any' || item.language === lang)).length}))};
      })
    },
    {
      name: 'read_page', title: defaultLanguage === 'zh' ? '读取公开页面' : 'Read a public page',
      description: 'Read a published ML-Biomat page as Markdown. Accepts canonical same-origin public page links from the site index, without query parameters. Preserves text, links, code and formulas. Large pages can be continued using next_offset. Does not run tutorial code, access payments, navigate, or read authenticated resources.',
      annotations,
      inputSchema: {type: 'object', properties: {url: {type: 'string', maxLength: 1024, description: 'Canonical public page URL ending in /.'}, offset: {type: 'integer', minimum: 0, maximum: 3000000, default: 0}, max_characters: {type: 'integer', minimum: 1000, maximum: 100000, default: 20000}}, required: ['url'], additionalProperties: false},
      execute: wrap(async (input, signal) => {
        objectInput(input, ['url', 'offset', 'max_characters']);
        const url = canonical(input.url);
        if (!readablePath(url.pathname)) throw new Error('This URL is not a supported public reading page.');
        const offset = integer(input.offset, 0, 0, 3000000), size = integer(input.max_characters, 20000, 1000, 100000);
        const page = (await pages(signal)).get(url.pathname);
        if (!page) throw new Error('This page is not in the public Markdown index.');
        const text = await publicText(page.markdown, signal, 'markdown');
        if (offset > text.length) throw new Error(`offset exceeds page length (${text.length} characters).`);
        const end = Math.min(offset + size, text.length);
        return {...page, offset, total_characters: text.length, next_offset: end < text.length ? end : null, text: text.slice(offset, end)};
      })
    }
  ];
  function register() {
    if (lifecycle && !lifecycle.signal.aborted) return;
    lifecycle = new AbortController();
    const registration = lifecycle;
    for (const tool of tools) {
      try {
        const pending = context.registerTool(tool, {signal: registration.signal});
        owned.add(tool.name);
        Promise.resolve(pending).catch(() => { owned.delete(tool.name); });
      } catch (_) { /* Unsupported or unavailable registrations never affect site reading. */ }
    }
  }
  window.addEventListener('pagehide', () => {
    if (lifecycle) lifecycle.abort();
    // Legacy preview implementations use navigator.modelContext.unregisterTool.
    if (typeof context.unregisterTool === 'function') {
      for (const name of owned) {
        try { Promise.resolve(context.unregisterTool(name)).catch(() => {}); } catch (_) {}
      }
    }
    owned.clear();
  });
  window.addEventListener('pageshow', event => { if (event.persisted) register(); });
  register();
})();
