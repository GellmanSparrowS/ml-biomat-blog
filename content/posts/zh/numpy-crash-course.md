---
title: "NumPy完全指南：从零到生产力"
date: "2026-06-26"
category: "python-tutorials"
tags: ["numpy", "python", "数组", "科学计算", "数据分析", "教程"]
lang: "zh"
slug: "numpy-crash-course-zh"
description: "从零学习NumPy，用真实的材料科学数据示例：加载实验数据、数组运算、统计分析、曲线拟合、批量处理。"
---

## 为什么每个材料人都需要NumPy

处理实验数据的基础工具。把拉伸机、AFM、XRD导出的txt文件变成可以分析、绘图、导出的Python数组。

```python
import numpy as np
```

## 1. NumPy数组：你的数据容器

```python
strains = np.array([0.0, 0.005, 0.010, 0.020, 0.050, 0.100])
stresses = np.array([0, 8, 15, 28, 52, 74])

# 便捷函数
x = np.linspace(0, 0.5, 200)       # 0到0.5均匀分布200个点
zeros = np.zeros((10, 3))          # 10行3列全零矩阵

# 数组属性
print(arr.shape)  # (2, 3) — 2行3列
print(arr.ndim)   # 2 — 二维
print(arr.dtype)  # int64 — 数据类型
```

## 2. 加载实验数据

```python
# 通用：空格或制表符分隔
data = np.loadtxt("tensile_test.txt", skiprows=0)

# CSV文件
data = np.loadtxt("mechanical_data.csv", delimiter=",", skiprows=1)

# AFM力曲线（Bruker：320行头部）
raw = np.loadtxt("force_curve.001", skiprows=320)
z_piezo = raw[:, 0]        # 第一列
deflection = raw[:, 1]     # 第二列

# 处理缺失值
data = np.genfromtxt("messy_data.csv", delimiter=",", skip_header=1, filling_values=0)
```

## 3. 逐元素运算（无需循环）

NumPy的真正威力：操作同时应用于每个元素：

```python
# 算术
stress_pa = stresses * 1e6          # MPa转Pa
strain_pct = strains * 100          # 转为百分比

# 数学函数
log_stress = np.log(stresses)
exp_decay = np.exp(-time / tau)

# 比较
yielded = stresses > 30             # 布尔数组

# AFM偏转转力
k, sensitivity = 0.06, 45.0
force = k * sensitivity * deflection * 1e-9 * 1e9  # nN
```

## 4. 统计和聚合

```python
mean = np.mean(stresses)         # 平均值
std = np.std(stresses)           # 标准差
median = np.median(stresses)     # 中位数（抗异常值）
max_val = np.max(stresses)
total = np.sum(force)            # 求和

# 沿轴操作（二维数据）
col_means = data.mean(axis=0)    # 每列均值
row_stds = data.std(axis=1)      # 每行标准差
```

## 5. 布尔索引（数据过滤）

你可能最常用的NumPy特性：

```python
# 弹性区数据
elastic = stresses[strains < 0.02]

# 组合条件
valid = (strains > 0) & (strains < 0.1) & (stresses > 0)

# 计数
n_yielded = np.sum(stresses > 30)

# 替换值
stresses[stresses < 0] = 0

# 找索引
idx_max = np.argmax(stresses)
idx_where = np.where(stresses > 30)[0]
```

## 6. 重塑和合并数组

```python
flat = data.flatten()                   # 展平
matrix = np.arange(12).reshape(3, 4)    # 1D -> 3x4
combined = np.column_stack([strains, stresses])  # 并排
stacked = np.vstack([data1, data2])              # 按行追加
centered = data - data.mean(axis=0)              # 每列减均值
```

## 7. 保存结果

```python
np.savetxt("results.csv", combined, delimiter=",", header="strain,stress")
np.save("processed.npy", data)           # 二进制格式
loaded = np.load("processed.npy")
```

## 8. 完整示例：AFM力曲线处理

```python
import numpy as np
raw = np.loadtxt("force_curve_001.txt", skiprows=320)
z_piezo, deflection_V = raw[:, 0], raw[:, 1]

# 转力
k, sens = 0.06, 45.0
force = k * sens * deflection_V * 1e-9 * 1e9

# 基线校正
baseline = np.median(force[:100])
force_corr = force - baseline

# 找接触点
derivative = np.gradient(force_corr)
noise = np.std(derivative[:50])
contact_idx = np.argmax(derivative > 5 * noise)

# 拟合
indent = z_piezo[contact_idx] - z_piezo
mask = (indent > 0) & (indent < 50)
E, _ = np.polyfit(indent[mask], (force_corr-force_corr[contact_idx])[mask], 1)
print(f"杨氏模量: {E:.1f}")
```

## 9. 常见问题

| 问题 | 解决 |
|------|------|
| 加载失败 | `skiprows=N` 跳过头部行 |
| 缺失值 | `np.genfromtxt` + `filling_values` |
| 形状错误 | 用`.shape`检查，`data[:,0]`是1D |
| NaN | `np.divide(a, b, where=b!=0)` |

- Harris, C.R. et al. (2020). Array programming with NumPy. *Nature*, 585, 357-362.
