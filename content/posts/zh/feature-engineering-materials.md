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


## 深入探讨：特征缩放与标准化

特征缩放是机器学习预处理中容易被忽视但至关重要的步骤。不同物理量通常具有截然不同的量级——纤维直径可能只有几十纳米，而杨氏模量可能有几个吉帕。如果不进行缩放，依赖距离的模型会将量级大的特征视为更重要，即使它们物理上并不更关键。

StandardScaler将每个特征转换为均值为零标准差为一的分布。这对于线性回归、支持向量机和神经网络等模型至关重要。对于树模型如随机森林，特征缩放不是必需的，因为决策树基于特征值的排序而非距离。了解这一点可以避免不必要的预处理步骤。

特征归一化通过MinMaxScaler将所有特征缩放到给定范围如零到一之间。当你不确定特征分布是否近似正态时，归一化是更安全的选择。但归一化对异常值敏感——单个极端值可以压缩所有其他值到窄小区间。

特征工程的质量远比模型选择重要。在材料科学的小样本场景中，一两个精心构造的物理特征对模型性能的提升往往超过尝试十种不同算法。花时间理解你的数据，与领域专家讨论，让物理直觉指导特征构造——这是任何自动化工具都无法替代的人类价值。

## 参考文献
- Guyon, I. & Elisseeff, A. (2003). An introduction to variable and feature selection. *Journal of Machine Learning Research*, 3, 1157-1182.
