# ml-biomat-blog Maintenance Skill
## Project
E:\Auto_TEST\ml-biomat-blog\
GitHub: GellmanSparrowS/ml-biomat-blog (token: E:\Auto_TEST\.ml-biomat-token)
Domain: ml-biomat.com (GitHub Pages, main /docs)

## Build & Push
cd E:\Auto_TEST\ml-biomat-blog
python build.py
echo ml-biomat.com > docs\CNAME
git add -A; git commit -m "msg"; git push origin main

## Content Pipeline
- content/TODO.json: article queue
- content/INVENTORY.md: content inventory
- auto_writer.py: writer framework
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
- **Git push fails**: Use GitHub Contents API (PUT /contents/{path}) as fallback.

## Critical: Encoding (updated 2026-06-29)
- NEVER use backslash-x hex escapes in Python strings for write_text(encoding=utf-8). They get DOUBLE-ENCODED. Use backslash-u escapes instead.
- For Chinese content through PowerShell python -c: use here-string + base64 OR backslash-uXXXX unicode escapes.
- PowerShell backtick is escape char. Use backslash-u0060 for literal backticks.
- PowerShell does NOT support && for chaining; use ; instead.

## CI Compatibility (Python 3.12+)
- f-strings cannot contain backslashes. Extract re.sub() calls into a variable first.
- Applies to build.py, generate.py, and ALL Python files across repos.


## Auto-Push Rule (updated 2026-06-30)
- After completing articles + python build.py, ALWAYS push the full changeset without waiting for user prompt.
- Push scope: ALL changed files (config.py, content/posts/*.md, docs/*, SKILL.md).
- If git push fails (network), use GitHub Contents API batch upload automatically.
- Priority: push build output (docs/) and source (content/) first; then verify GitHub Pages deployment.
- Do not leave un-pushed local changes at end of session.

## Article Depth Rule (2026-06-30)
- Section count: 4-12 is ideal. Depth over breadth.
- Each section: 900-2000 hanzi, thorough explanation of ONE concept.
- Write for graduate students: plain language intuition first, math second.
- Test: can a non-specialist grad student grasp the core from this section alone?
- Avoid shallow bullet lists; prefer connected paragraphs that build understanding.

## Auto-Completion Rule (2026-06-30)
- If a task (article + build + push) is not complete at end of session, continue in next turn.
- Do not stop at partial work. Complete the full cycle: write -> build -> verify -> push.
- Respect GitHub API rate limits: batch pushes, retry SSL failures, do not hammer.
