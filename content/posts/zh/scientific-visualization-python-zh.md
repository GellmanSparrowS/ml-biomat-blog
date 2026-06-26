---
title: "Python科研绘图实战：发表级图表制作"
date: "2026-06-26"
category: "python-tutorials"
tags: ["matplotlib", "可视化", "python", "科研绘图"]
lang: "zh"
slug: "scientific-visualization-python-zh"
description: "Matplotlib发表级图表制作指南：多幅布局、色彩方案、高分辨率导出。"
---

## 多幅图模板

```python
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0,0].plot(strain, stress, "k-")
axes[0,0].text(-0.1, 1.05, "A", transform=axes[0,0].transAxes, fontweight="bold")
df.boxplot(column="modulus", by="treatment", ax=axes[0,1])
axes[1,0].scatter(x, y, s=20, alpha=0.6)
axes[1,1].imshow(sem_image, cmap="gray")
plt.tight_layout()
```

## 色彩方案

```python
import seaborn as sns
sns.set_palette("colorblind")
colors = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a"]
```

## 导出格式

```python
plt.savefig("figure.pdf", dpi=300, bbox_inches="tight")  # 矢量
plt.savefig("figure.png", dpi=600)  # 高分辨率
```

## 审稿建议
- 不要单独用红绿配色
- 用粗体字母标注幅面
- 在caption中报告n值

- Rougier, N.P. et al. (2014). *PLoS CB*, 10(9), e1003833.
