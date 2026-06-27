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