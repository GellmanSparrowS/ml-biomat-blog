# -*- coding: utf-8 -*-
"""Site configuration for ml-biomat.com"""

SITE = {
    "title": "ML-Biomat",
    "tagline_en": "Machine Learning and Multiscale Modeling for Biomaterials",
    "tagline_zh": "机器学习与多尺度模拟 — 面向生物·材料·结构研究",
    "base_url": "https://ml-biomat.com",
    "description_en": "Research notes, tutorials, and practical tools for the rational design of biomaterial systems and structures across scales, combining machine learning and multiscale modeling. Home of FiberNet for fiber network research.",
    "description_zh": "围绕跨尺度生物材料体系与结构理性设计的研究笔记、教程与实用工具，结合机器学习和多尺度模拟。FiberNet 纤维网络研究 Python 工具包的官方网站。",
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
