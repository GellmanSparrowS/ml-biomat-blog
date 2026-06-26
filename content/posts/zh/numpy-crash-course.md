---
title: "NumPy速成：实验室必备数据处理工具"
date: "2026-06-26"
category: "python-tutorials"
tags: ["numpy", "python", "数组", "科学计算", "教程"]
lang: "zh"
slug: "numpy-crash-course-zh"
description: "NumPy实战指南：数组创建、运算、加载实验数据、常用操作，面向材料研究生。"
---

## 为什么学NumPy

处理数值数据的基础。拉伸测试、AFM曲线、XRD图谱、MD轨迹都变成NumPy数组。

```python
import numpy as np
```

## 创建数组

```python
strains = np.array([0.0, 0.01, 0.02, 0.05, 0.10])
data = np.loadtxt("tensile_test.csv", delimiter=",", skiprows=1)
z, force = data[:, 0], data[:, 1]
```

## 数组运算

```python
mean = np.mean(stresses)
coeffs = np.polyfit(strains, stresses, 1)  # 线性拟合
E = coeffs[0]  # 杨氏模量=斜率
elastic = stresses[strains < 0.02]  # 布尔索引
```

## 加载真实数据

```python
raw = np.loadtxt("force_curve_001.txt", skiprows=320)
force = 0.06 * 45.0 * (raw[:,1] - np.median(raw[:100,1]))
```

- numpy.org/doc
