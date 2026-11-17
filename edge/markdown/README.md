# Public Markdown negotiation

Activated on ml-biomat.com on 2026-11-17. The static build generates `index.md` files and `agent-index.json` from published pages. The `ml-biomat-markdown` Worker returns these files when a client requests Markdown; browsers keep HTML. Content updates flow through the existing GitHub Pages publication without redeploying this Worker.

## Deployed configuration

- ES module: `worker.mjs`; reproducible Worker configuration: `wrangler.jsonc`.
- Explicit `global_fetch_private_origin` compatibility flag: same-zone fetches reach the origin rather than re-entering this Worker. Do not enable `global_fetch_strictly_public`.
- `ml-biomat.com/*` invokes the Worker with `request_limit_fail_open: true`.
- The more specific `ml-biomat.com/static/*` route has no Worker and bypasses invocation. Preserve this route when deploying.
- The workers.dev endpoint and preview URLs are disabled. No runtime secrets, databases or conversion models are used.
- Both HTML and Markdown responses vary on Accept. Separate origin paths keep their cache entries distinct. Authorization, Range and non-GET/HEAD requests pass through; unavailable derivatives fall back to the original response. Payment paths keep their original behavior.

The route failure mode is configured in Cloudflare's Routes API/dashboard, separately from Wrangler's script configuration. Read back `request_limit_fail_open: true` after changing routes. If the daily Worker quota is exhausted, Cloudflare serves the origin directly. Do not upgrade account plans automatically.

## Validation

On 2026-11-17, 21 live checks passed: alternating HTML/Markdown at the same URL, Chinese and English tutorials, encoded Chinese and space-containing tags, HEAD, Accept quality preferences, 404 responses, redirects, static files, public access documentation, payment completion and the existing payment service health check. The agent-readiness scan passed Markdown negotiation, WebMCP (three read-only tools), and Agent Skills discovery.

Run `node edge/markdown/test_worker.mjs` for the negotiation regression checks. After deployment, request the homepage and representative tutorials with default Accept, `text/html`, `text/markdown`, and `text/markdown;q=0`. Compare Markdown to its published `index.md`, verify Vary and Content-Type, then confirm that unknown pages still return 404 and static/payment resources remain unchanged.
