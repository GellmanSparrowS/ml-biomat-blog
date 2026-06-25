# ml-biomat-blog Maintenance Skill

## Purpose
Maintain and extend ml-biomat.com bilingual EN/ZH blog, hosted via GitHub Pages.

## Project
E:\Auto_TEST\ml-biomat-blog\

## Build & Deploy
1. Edit content/posts/{en,zh}/*.md
2. Run `python build.py` (generates docs/)
3. Push via GitHub Contents API (batch of 16 per session, 0.3s delay between calls)

## GitHub
- Repo: GellmanSparrowS/ml-biomat-blog
- Token: ask user for current token
- Pages: main branch, /docs folder, custom domain ml-biomat.com

## Post Frontmatter
```yaml
title, date, category, tags, lang: en|zh, slug, description
```

## Key Files
- build.py: static site generator (Python 3.10, stdlib only)
- config.py: SITE metadata, CATEGORIES definitions
- content/posts/{en,zh}/*.md: blog posts
- content/about-body.html: about page HTML body
- content/cv-body.html: CV page HTML body
- static/css/style.css: theme (light/dark/responsive)
- docs/: generated output (auto, do not edit)

## User Preferences
- Python 3.10, stdlib only
- All pages bilingual EN+CN
- No emoji in CV or formal pages
- Categories: machine-learning, multiscale-modeling, biomaterials, python-tutorials, research-notes, wet-lab-data
- Photo: static/images/照片.jpg (CV), static/images/照片-方.jpg (About)

## Content Strategy
When writing articles, browse real web resources for accuracy and citations
Target: non-CS scientists + interdisciplinary researchers
