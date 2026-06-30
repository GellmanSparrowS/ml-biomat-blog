# -*- coding: utf-8 -*-
"""Site configuration for ml-biomat.com"""

SITE = {
    "title": "ML-Biomat",
    "tagline_en": "Machine Learning and Multiscale Modeling for Biomaterials",
    "tagline_zh": "机器学习与多尺度模拟 — 面向生物·材料·结构研究",
    "base_url": "https://ml-biomat.com",
    "description_en": "Tutorials, research notes, and practical guides on ML and multiscale modeling for fiber-based biomaterials.",
    "description_zh": "纤维生物·材料·结构的机器学习与多尺度模拟教程、研究笔记和实战指南。",
    "author": "Yunhao Yang",
    "author_affiliation": "Fudan University",
    "lang": "en",
}
BUILD_DIR = "docs"
CONTENT_DIR = "content"

CATEGORIES = {
    "machine-learning": {"name_en": "Machine Learning", "name_zh": "机器学习", "slug": "machine-learning"},
    "multiscale-modeling": {"name_en": "Multiscale Modeling", "name_zh": "多尺度模拟", "slug": "multiscale-modeling"},
    "biomaterials": {"name_en": "Bio-Materials-Structures", "name_zh": "生物·材料·结构", "slug": "biomaterials"},
    "python-tutorials": {"name_en": "Python Tutorials", "name_zh": "Python教程", "slug": "python-tutorials"},
    "research-notes": {"name_en": "Research Notes", "name_zh": "研究笔记", "slug": "research-notes"},
    "wet-lab-data": {"name_en": "Wet-lab Data Processing", "name_zh": "湿实验数据处理", "slug": "wet-lab-data"},
}
