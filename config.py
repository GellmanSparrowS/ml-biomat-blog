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
    "lang": "zh-CN",
}
BUILD_DIR = "docs"
CONTENT_DIR = "content"

CATEGORIES = {
    "machine-learning": {
        "name_en": "Machine Learning",
        "name_zh": "机器学习",
        "slug": "machine-learning",
        "description_zh": "回归、分类、表示学习与实验选样的方法，结合材料问题练习模型训练、验证和不确定性分析。",
        "description_en": "Regression, classification, representation learning and experiment selection, with materials examples for training, validation and uncertainty analysis."
    },
    "multiscale-modeling": {
        "name_en": "Physical Modeling & Simulation",
        "name_zh": "物理建模与模拟",
        "slug": "multiscale-modeling",
        "description_zh": "从分子动力学、单链统计到粗粒化和连续介质，学习物理模型、数值计算与尺度之间的参数传递。",
        "description_en": "Physical models and numerical methods, from molecular dynamics and chain statistics to coarse-graining, continuum mechanics and parameter transfer across scales."
    },
    "biomaterials": {
        "name_en": "Materials & Structures",
        "name_zh": "材料与结构",
        "slug": "biomaterials",
        "description_zh": "从生物大分子的组成与连接，到凝胶、纤维网络和工程超结构，理解结构、加工与性能之间的联系。",
        "description_en": "Biomolecular composition and connectivity, gels, fiber networks and architected materials, connecting structure and processing with material properties."
    },
    "python-tutorials": {
        "name_en": "Scientific Computing with Python",
        "name_zh": "Python科学计算",
        "slug": "python-tutorials",
        "description_zh": "学习科学计算工具和常用编程方法，涵盖环境搭建、数组、表格、拟合、绘图与网络分析。",
        "description_en": "Scientific computing tools and programming methods for environments, arrays, tables, curve fitting, visualization and network analysis."
    },
    "research-notes": {
        "name_en": "Research Notes",
        "name_zh": "研究笔记",
        "slug": "research-notes",
        "description_zh": "记录具体研究问题、方法比较与阶段性认识，连接相关论文、代码和下一步工作。",
        "description_en": "Research questions, method comparisons and developing findings, connected to relevant papers, code and further work."
    },
    "wet-lab-data": {
        "name_en": "Experimental Characterization & Data Analysis",
        "name_zh": "实验表征与数据分析",
        "slug": "wet-lab-data",
        "description_zh": "围绕力学测试、AFM、显微图像与散射信号，学习标定、数据处理、性能提取与误差分析。",
        "description_en": "Calibration, processing, property extraction and error analysis for mechanical tests, AFM measurements, microscopy images and scattering signals."
    }
}
