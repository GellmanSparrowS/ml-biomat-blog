---
title: "Python科研工具箱：材料科学常用Python库实战"
date: "2026-06-26"
category: "python-tutorials"
tags: ["python", "numpy", "scipy", "材料科学", "数据分析"]
lang: "zh"
slug: "python-tools-materials-research-zh"
description: "材料科研必备Python库指南：NumPy/SciPy数据处理、Pandas分组统计、Matplotlib科研绘图、ASE/pymatgen原子结构分析。"
---

## 为什么用Python

材料研究产生各种数据：AFM力曲线、SEM图像、MD轨迹、XRD图谱、力学测试日志。Python已成为处理这些数据的万能语言。

```python
import numpy as np
from scipy import signal, optimize
import matplotlib.pyplot as plt
```

## 核心工具栈

### NumPy & SciPy

```python
data = np.loadtxt("force_curve.txt", skiprows=2)
z_piezo, deflection = data[:, 0], data[:, 1]
k = 2.8  # N/m
sensitivity = 42.5  # nm/V
force = k * sensitivity * (deflection - np.median(deflection[:100]))
peaks, _ = signal.find_peaks(-force, prominence=0.5)
adhesion = -force[peaks[0]] if len(peaks) > 0 else 0
```

### Pandas

```python
import pandas as pd
df = pd.read_csv("tensile_tests.csv")
summary = df.groupby("treatment").agg({"youngs_modulus": ["mean", "std"], "ultimate_strength": ["mean", "std"]}).round(2)
```

### Matplotlib

```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
ax1.plot(strain, stress, "b-", linewidth=1.5)
plt.savefig("mechanical_properties.pdf", dpi=300)
```

## 材料科学专用库

### ASE（原子模拟环境）

```python
from ase.io import read
atoms = read("collagen_fibril.data", format="lammps-data")
supercell = atoms * (2, 2, 3)
```

- Hunter, J.D. (2007). Matplotlib: A 2D graphics environment. *CSE*, 9(3), 90-95.
