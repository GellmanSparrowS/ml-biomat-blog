---
title: "材料科学中的特征工程：从实验数据到机器学习就绪数据"
date: "2026-06-26"
category: "machine-learning"
tags: ["特征工程", "机器学习", "材料科学", "数据预处理"]
lang: "zh"
slug: "feature-engineering-materials-zh"
description: "如何将零散的实验数据转化为结构化的特征矩阵，含分类编码、交互特征、缺失值处理和小样本特征选择。"
---

## 真正的瓶颈

大多数材料ML教程从干净的CSV直接跳到模型拟合。现实中，你的数据分散在实验本、仪器导出文件和Excel表格里。特征工程是将原始观测转化为结构化特征矩阵的过程，占实际工作量的80%。

```python
import pandas as pd; import numpy as np
df = pd.DataFrame({"纤维直径_nm": [45,52,48], "交联密度_pct": [2.5,1.8,3.2], "处理": ["甲醇","乙醇","水"], "杨氏模量_GPa": [2.8,1.9,2.3]})
```

## 分类变量编码

```python
from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder(sparse_output=False, drop="first")
encoded = encoder.fit_transform(df[["处理"]])
```

## 域知识驱动的交互特征

```python
def engineer_features(df):
    df = df.copy()
    df["crosslink_x_diameter"] = df["交联密度_pct"] * df["纤维直径_nm"]
    df["orient_diameter_ratio"] = df.get("取向标准差_deg", 15) / (df["纤维直径_nm"] + 1e-6)
    return df
```

## 小样本特征选择

样本少于100时避免自动化特征选择。改用：相关性分析（去除|r|>0.95的特征）、方差阈值（去除近常数特征）、域知识筛选（只保留物理上合理的特征）。

## 检查清单

所有特征已数值化、没有特征泄露目标变量、缺失值已处理、分类变量已编码、交互特征有物理依据。

## 参考文献
- Kuhn, M. & Johnson, K. (2019). *Feature Engineering and Selection*. CRC Press.
- Ramprasad, R. et al. (2017). Machine learning in materials informatics. *npj Computational Materials*, 3, 54.
