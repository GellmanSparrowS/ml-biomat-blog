---
title: "Python科研工具箱：材料科学常用库实战"
date: "2026-06-26"
category: "python-tutorials"
tags: ["python", "numpy", "scipy", "材料科学", "数据分析"]
lang: "zh"
slug: "python-tools-materials-research-zh"
description: "材料科研必备Python库指南：NumPy/SciPy数据处理、Pandas分组统计、Matplotlib科研绘图、ASE/pymatgen原子结构分析。"
---

材料研究产生各种数据：AFM力曲线、SEM图像、MD轨迹、XRD图谱、力学测试日志。Python已成为处理这些数据的万能语言。

```python
import numpy as np
from scipy import signal, optimize
import matplotlib.pyplot as plt
```

## NumPy & SciPy

```python
# 加载AFM力曲线
data = np.loadtxt("force_curve.txt", skiprows=2)
z_piezo, deflection = data[:, 0], data[:, 1]
# 转换为力
k = 2.8  # N/m，悬臂弹性常数
sensitivity = 42.5  # nm/V
force = k * sensitivity * (deflection - np.median(deflection[:100]))
# 寻找粘附峰
peaks, _ = signal.find_peaks(-force, prominence=0.5)
adhesion = -force[peaks[0]] if len(peaks) > 0 else 0
```

## Pandas分组统计

```python
import pandas as pd
df = pd.read_csv("tensile_tests.csv")
summary = df.groupby("treatment").agg({"youngs_modulus": ["mean", "std"], "ultimate_strength": ["mean", "std"]}).round(2)
```

## Matplotlib科研绘图

```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
ax1.plot(strain, stress, "b-", linewidth=1.5)
ax1.set_xlabel("Strain"); ax1.set_ylabel("Stress (MPa)")
ax2.boxplot([group1, group2, group3])
plt.savefig("mechanical_properties.pdf", dpi=300)
```

## ASE原子模拟环境

```python
from ase.io import read
atoms = read("collagen_fibril.data", format="lammps-data")
supercell = atoms * (2, 2, 3)
```

## 图像分析

```python
from skimage import io, filters, measure
img = io.imread("sem_fiber.tif", as_gray=True)
thresh = filters.threshold_otsu(img)
binary = img > thresh
props = measure.regionprops_table(measure.label(binary), properties=["area", "eccentricity"])
```

## 快速安装

```bash
conda create -n matsci python=3.10 numpy scipy pandas matplotlib scikit-learn jupyter ase pymatgen scikit-image -c conda-forge
```

## 参考文献
- Hunter, J.D. (2007). Matplotlib: A 2D graphics environment. *CSE*, 9(3), 90-95.
- van der Walt, S. et al. (2014). scikit-image: image processing in Python. *PeerJ*, 2, e453.
