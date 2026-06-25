# -*- coding: utf-8 -*-
"""Site configuration for ml-biomat.com"""

SITE = {
    "title": "ML-Biomat",
    "base_url": "https://ml-biomat.com",
    "description": "Machine Learning &amp; Multiscale Modeling for Biomaterials — tutorials, research notes, practical guides for scientists.",
    "author": "GellmanSparrow",
    "lang": "en",
    "google_analytics": "",  # Fill after GA setup
    "adsense_pub_id": "",   # Fill after AdSense approval: ca-pub-XXXXXXXXXXXXXXXX
}

CATEGORIES = {
    "machine-learning": {"name": "Machine Learning", "slug": "machine-learning"},
    "multiscale-modeling": {"name": "Multiscale Modeling", "slug": "multiscale-modeling"},
    "biomaterials": {"name": "Biomaterials", "slug": "biomaterials"},
    "python-tutorials": {"name": "Python Tutorials", "slug": "python-tutorials"},
    "research-notes": {"name": "Research Notes", "slug": "research-notes"},
}

BUILD_DIR = "output"
CONTENT_DIR = "content"
