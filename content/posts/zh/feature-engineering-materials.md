---
title: "材料科学中的特征工程：从实验数据到ML就绪数据"
date: "2026-06-26"
category: "machine-learning"
tags: ["特征工程", "机器学习", "材料科学", "数据预处理"]
lang: "zh"
slug: "feature-engineering-materials-zh"
description: "如何将零散的实验数据转化为结构化的特征矩阵，含编码、交互特征、缺失值处理和小样本特征选择。"
---

## 真正的瓶颈

大多数材料ML教程从一个干净的CSV直接跳到模型拟合。现实中，你的数据分散在实验本、仪器导出文件和合并单元格的Excel表格里。**特征工程**——将原始观测转化为结构化的特征矩阵——是80%工作量的所在。

```python
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
```

## 从原始数据到特征矩阵

```python
df = pd.DataFrame({
    "纤维直径_nm": [45, 52, 48, 55, 50, 47],
    "取向标准差_deg": [12, 22, 8, 18, 15, 20],
    "交联密度_pct": [2.5, 1.8, 3.2, 2.0, 4.1, 1.5],
    "处理": ["甲醇", "乙醇", "甲醇", "水", "甲醇", "乙醇"],
    "杨氏模量_GPa": [2.8, 1.9, 3.5, 2.3, 4.0, 1.7],
})
```

## 分类变量编码

```python
encoder = OneHotEncoder(sparse_output=False, drop="first")
encoded = encoder.fit_transform(df[["处理"]])
cols = encoder.get_feature_names_out(["处理"])
df_enc = pd.concat([df.drop("处理", axis=1), pd.DataFrame(encoded, columns=cols)], axis=1)
```

## 域知识驱动的交互特征

```python
def engineer_materials_features(df):
    df = df.copy()
    df["crosslink_x_diameter"] = df["交联密度_pct"] * df["纤维直径_nm"]
    df["orient_diameter_ratio"] = df["取向标准差_deg"] / (df["纤维直径_nm"] + 1e-6)
    for col in ["交联密度_pct", "纤维直径_nm"]:
        if col in df.columns: df[f"log_{col}"] = np.log1p(df[col])
    return df
```

## 缺失值处理

小样本数据不要盲目用均值填充：

```python
def smart_impute(df, group_col="处理"):
    df = df.copy()
    for col in df.select_dtypes(include=np.number).columns:
        if df[col].isna().sum() == 0: continue
        if group_col in df.columns:
            df[col] = df.groupby(group_col)[col].transform(lambda x: x.fillna(x.median()))
        df[col] = df[col].fillna(df[col].median())
    return df
```

## 小样本特征选择

当样本少于100时，避免自动化特征选择。改用：

1. **相关性分析**：去除|r|>0.95的特征
2. **方差阈值**：去除近常数特征
3. **域知识筛选**：只保留物理上合理的特征

## 检查清单

- 所有特征已数值化
- 没有特征泄漏目标变量
- 缺失值已处理
- 分类变量已编码
- 交互特征有物理依据

## 参考文献

- Kuhn, M. & Johnson, K. (2019). *Feature Engineering and Selection*. CRC Press.
- Ramprasad, R. et al. (2017). Machine learning in materials informatics. *npj Computational Materials*, 3, 54.
