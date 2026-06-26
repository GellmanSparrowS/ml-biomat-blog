---
title: "Python数据处理实战：用Pandas清洗和可视化材料实验数据"
date: "2026-06-26"
category: "python-tutorials"
tags: ["pandas", "python", "数据处理", "实验数据", "可视化"]
lang: "zh"
slug: "pandas-materials-data-zh"
description: "手把手教你用Pandas处理材料实验数据：读取多源数据、合并清洗、分组统计、可视化，适合刚接触编程的实验室同学。"
---

## 为什么学Pandas

做实验的同学经常面对这样的场景：拉力机导出一个Excel、AFM导出一个CSV、SEM数据又是另一个文件夹。手动在Excel里合并、筛选、画图，耗时且容易出错。

**Pandas是Python的数据处理瑞士军刀**。学一次，终身受益。

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

## 1. 读取实验数据

最常见的三种格式：

```python
# Excel（最常见）
df = pd.read_excel("mechanical_tests.xlsx", sheet_name="Sheet1")

# CSV/TXT（AFM、拉力机等导出）
df = pd.read_csv("force_curves.csv")

# 多个文件合并
import glob
files = glob.glob("data/*.csv")
dfs = [pd.read_csv(f) for f in files]
df_all = pd.concat(dfs, ignore_index=True)
```

## 2. 数据清洗

实验数据永远不干净。以下是常见问题和处理：

```python
# 删除完全空的行/列
df = df.dropna(how="all")

# 重命名列（英文方便代码操作）
df = df.rename(columns={
    "纤维直径(nm)": "fiber_diameter_nm",
    "杨氏模量(GPa)": "youngs_modulus_GPa",
    "处理条件": "treatment"
})

# 去除异常值（3-sigma原则）
for col in ["youngs_modulus_GPa", "fiber_diameter_nm"]:
    mean = df[col].mean()
    std = df[col].std()
    df = df[(df[col] > mean - 3*std) & (df[col] < mean + 3*std)]
```

## 3. 分组统计

实验室最常用的分析——按处理条件分组看统计量：

```python
summary = df.groupby("treatment").agg({
    "youngs_modulus_GPa": ["mean", "std", "count"],
    "fiber_diameter_nm": ["mean", "std"],
}).round(2)

print(summary)
```

输出类似：

```
           youngs_modulus_GPa          fiber_diameter_nm
                        mean   std count            mean   std
treatment
ethanol                 1.80  0.14     3           51.67  2.52
methanol                3.48  0.28     3           48.00  3.61
```

## 4. 数据可视化

四种最常用的科研图表：

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# A: 箱线图——比较不同处理的模量分布
df.boxplot(column="youngs_modulus_GPa", by="treatment", ax=axes[0,0])
axes[0,0].set_title("Young's Modulus by Treatment")

# B: 散点图——纤维直径 vs 模量
axes[0,1].scatter(df["fiber_diameter_nm"], df["youngs_modulus_GPa"], alpha=0.6)
axes[0,1].set_xlabel("Fiber Diameter (nm)")
axes[0,1].set_ylabel("Young's Modulus (GPa)")

# C: 柱状图（带误差棒）
means = summary[("youngs_modulus_GPa", "mean")]
stds = summary[("youngs_modulus_GPa", "std")]
axes[1,0].bar(means.index, means.values, yerr=stds.values, capsize=5)
axes[1,0].set_ylabel("Young's Modulus (GPa)")

# D: 相关性热力图
corr = df.select_dtypes(include=np.number).corr()
im = axes[1,1].imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
plt.colorbar(im, ax=axes[1,1])

plt.tight_layout()
plt.savefig("mechanical_analysis.pdf", dpi=150, bbox_inches="tight")
```

## 5. 导出结果

```python
# 导出统计摘要
summary.to_csv("mechanical_summary.csv")

# 导出清洗后的数据
df.to_csv("cleaned_data.csv", index=False)

# 导出为Excel（多个sheet）
with pd.ExcelWriter("results.xlsx") as writer:
    df.to_excel(writer, sheet_name="Raw Data", index=False)
    summary.to_excel(writer, sheet_name="Summary")
```

## 6. 常见坑

| 问题 | 解决 |
|------|------|
| 中文列名报错 | 改成英文列名 |
| 编码错误 | `pd.read_csv("file.csv", encoding="utf-8")` 或 `"gbk"` |
| 大文件读取慢 | 指定`dtype`，或用`chunksize`分批读 |
| 日期格式乱 | `pd.to_datetime(df["date"], format="%Y-%m-%d")` |

## 小结

Pandas解决的是实验室80%的数据处理需求。花一小时学会这五个操作——读取、清洗、分组、画图、导出——你的数据处理效率会提高一个数量级。

## 参考文献
- McKinney, W. (2010). Data Structures for Statistical Computing in Python. *Proc. SciPy*, 56-61.
- pandas.pydata.org
