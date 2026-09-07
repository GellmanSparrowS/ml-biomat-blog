# ml-biomat-blog Maintenance Skill
## Project
E:\Auto_TEST\ml-biomat-blog\
GitHub: GellmanSparrowS/ml-biomat-blog (token: E:\Auto_TEST\.ml-biomat-token)
Domain: ml-biomat.com (GitHub Pages, main /docs)

## Build & Commit (NO AUTO-PUSH)
cd E:\Auto_TEST\ml-biomat-blog
python build.py
git add -A; git commit -m "msg"
# NEVER `git push` unless the user explicitly authorizes it.

## Content Pipeline
- content/TODO.json: article queue
- content/INVENTORY.md: content inventory
- article_writer.py: sectioned anti-truncation writer (preferred)
- chart_gen.py: chart + table helpers (run with anaconda python)
- auto_writer.py: legacy queue reader
- Coverage check auto-runs on build

## BOM Warning
PowerShell Set-Content adds BOM. Use apply_patch or Python write for .md files.
## Photos: photo.jpg (CV), photo-sq.jpg (About)

## Troubleshooting
- **Unicode escapes**: NEVER use apply_patch for Chinese content. Use Python write_text().
- **Actions spam**: Delete .github/workflows/deploy.yml. Pages deploys from branch directly.
- **Deep nesting**: Keep H2 count <= 7 per article. Use ### for sub-sections.
- **BOM**: PowerShell Set-Content adds BOM. Use Python write for .md files.
- **.nojekyll**: Always auto-generate .nojekyll in docs/ to bypass Jekyll.
- **Push is disabled by default**: only push when the user explicitly asks.

## Critical: Encoding (updated 2026-06-29)
- NEVER use backslash-x hex escapes in Python strings for write_text(encoding=utf-8). They get DOUBLE-ENCODED. Use backslash-u escapes instead.
- For Chinese content through PowerShell python -c: use here-string + base64 OR backslash-uXXXX unicode escapes.
- PowerShell backtick is escape char. Use backslash-u0060 for literal backticks.
- PowerShell does NOT support && for chaining; use ; instead.

## CI Compatibility (Python 3.12+)
- f-strings cannot contain backslashes. Extract re.sub() calls into a variable first.
- Applies to build.py, generate.py, and ALL Python files across repos.


## Push Policy (updated 2026-09-07)
- NEVER push to GitHub unless the user explicitly authorizes it.
- Local commits are allowed and recommended for rollback.
- `git status` may show "ahead of origin/main" after prior API-based uploads; ignore it.
- The live site already mirrors the local tree; verify against https://ml-biomat.com/.

## Article Depth Rule (2026-06-30)
- Section count: 4-12 is ideal. Depth over breadth.
- Each section: 900-2000 hanzi, thorough explanation of ONE concept.
- Write for graduate students: plain language intuition first, math second.
- Test: can a non-specialist grad student grasp the core from this section alone?
- Avoid shallow bullet lists; prefer connected paragraphs that build understanding.

## Auto-Completion Rule (2026-06-30)
- Complete the full LOCAL cycle: write -> build -> verify -> local commit.
- Do not stop at partial work; use _drafts/ part files so an interrupted write resumes cleanly.

## Long-Form Writing (updated 2026-09-07)
- Do NOT write articles as one giant here-string; it truncates around ~800 hanzi.
- Use article_writer.py: one section per part file, then assemble + validate.
  1) python article_writer.py new <slug> --lang <en|zh> --category <cat> --title "..." --desc "..." --tags a,b
  2) write each section to _drafts/<slug>/part-NN.md (Python write_text, utf-8)
  3) python article_writer.py assemble <slug> --check-only   # validate length/H2/images
  4) python article_writer.py assemble <slug>                # write the final post
- Validation defaults: EN >= 800 words, ZH >= 3000 hanzi, H2 <= 7. Override with --min-words / --max-h2.
- Keep one concept per section; prefer connected paragraphs over bullet lists.

## MathJax / LaTeX Rendering (2026-07-03)
MathJax 3 auto-injected in build.py for post pages. After LaTeX-heavy articles, clear browser cache (Ctrl+Shift+R). If formulas fail, check backslash escaping.

## Cache and Deployment (2026-07-03)
GitHub Pages deploys 1-2 min after the user pushes local commits. Hard refresh to verify. Stale content: check the Pages deployment status.

## Figures & Tables (2026-09-07)
- Generate charts from data with chart_gen.py (run with anaconda python):
  python chart_gen.py line --csv data.csv --x x --y y --out static/images/posts/<slug>/fig.webp --webp
  (also: bar, scatter; `table` prints a Markdown table from CSV)
- Put figures in static/images/posts/<slug>/ and reference them in the .md:
  ![alt](/static/images/posts/<slug>/fig.webp)
- Prefer WebP; article_writer.py assemble validates that local image references exist.

## Post-Frontmatter Checklist
title, date, category, tags[], lang, slug, description. Bilingual: same category, EN slug xxx-ml, ZH xxx-zh.

## IndexNow (2026-07-03)
- Key: cbd023642a994753b6b98784c0489ce7 stored at docs/{key}.txt and E:\\Auto_TEST\\cbd023642a994753b6b98784c0489ce7.txt
- Auto-submitted in build.py after each build (all post URLs + homepage).
- API: POST https://api.indexnow.org/indexnow with JSON {host, key, keyLocation, urlList}.
- If submission fails, site still works via normal crawling; IndexNow just accelerates indexing.

## Meta Descriptions (2026-07-03)
- Bing flags descriptions < 150 chars; Chinese is judged by raw char count.
- Target: 60-100 Chinese chars, 150-250 English chars.
- Use description field in YAML frontmatter; build.py reads it directly.
