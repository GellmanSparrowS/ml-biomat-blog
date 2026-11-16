# Public Markdown negotiation

The static build generates page `index.md` files and `agent-index.json` from the published HTML. The Worker returns those files when a public page is requested with a positive `Accept: text/markdown` preference. Ordinary browsers keep the HTML page. Both representations vary on Accept; origin requests use separate paths so HTML and Markdown cannot share an origin cache entry.

Deploy `worker.mjs` as an ES module named `ml-biomat-markdown`, compatibility date `2026-11-16`, using the existing account and zone for `ml-biomat.com`. Route `ml-biomat.com/*` through the Worker after the static derivatives are live. Preserve existing more-specific Worker routes, especially payment services. Static asset routes may bypass this Worker. Configure fail-open so the origin remains available if the Worker quota is exhausted. Do not upgrade plans automatically.

No secrets, API bindings, database or conversion model are needed at runtime. Requests carrying Authorization, Range, or a method other than GET/HEAD pass directly to the origin. Missing derivatives fall back to the original response. Payment routes never negotiate Markdown.

Validate the homepage and a Chinese/English tutorial with default Accept, `text/html`, `text/markdown`, `text/markdown;q=0`, and HEAD. Check status, body, Content-Type and Vary. Unknown pages must still return 404. Static assets and payment routes must remain unchanged.
