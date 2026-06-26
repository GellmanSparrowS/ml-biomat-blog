---
title: "Python科研绘图实战：发表级图表制作"
date: "2026-06-26"
category: "python-tutorials"
tags: ["matplotlib", "可视化", "python", "科研绘图"]
lang: "zh"
slug: "scientific-visualization-python-zh"
description: "Matplotlib发表级图表制作完整指南：多幅布局、色彩方案、高分辨率导出、常见图表类型和审稿建议。"
---

一张好图比一段文字更能说服审稿人。这篇指南给你可复用的Matplotlib模板，直接用于论文。

```python
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 10, "figure.dpi": 150, "savefig.dpi": 300})
```

## 多幅图模板

```python
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
# A: 应力-应变曲线
axes[0,0].plot(strain, stress, "k-")
axes[0,0].text(-0.1, 1.05, "A", transform=axes[0,0].transAxes, fontweight="bold")
axes[0,0].set_xlabel("Strain"); axes[0,0].set_ylabel("Stress (MPa)")
# B: 箱线图
df.boxplot(column="modulus", by="treatment", ax=axes[0,1])
# C: 散点图
axes[1,0].scatter(x, y, s=20, alpha=0.6)
axes[1,0].set_xlabel("Diameter (nm)"); axes[1,0].set_ylabel("Modulus (GPa)")
# D: SEM图像
axes[1,1].imshow(sem_image, cmap="gray"); axes[1,1].axis("off")
plt.tight_layout()
```

## 色彩方案

不要用默认颜色。用色盲友好或期刊特定的调色板：

```python
import seaborn as sns
sns.set_palette("colorblind")  # 色盲友好
colors = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a"]  # 自定义科学配色
```

## 导出格式

```python
plt.savefig("figure.pdf", dpi=300, bbox_inches="tight")  # 矢量，可编辑
plt.savefig("figure.png", dpi=600)  # 位图，高分辨率
```

## 审稿建议

- 红绿配色不要单独用（8%男性色弱）
- 用粗体字母标注幅面（A, B, C）
- 在caption中报告n值
- 展示单个数据点，不要藏在箱线图后面

## 参考文献
- Rougier, N.P. et al. (2014). Ten simple rules for better figures. *PLoS Computational Biology*, 10(9), e1003833.
- Hunter, J.D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering*, 9(3), 90-95.
