---
title: "SciPy曲线拟合完全指南：从线性回归到非线性建模"
date: "2026-06-27"
category: "python-tutorials"
tags: ["scipy", "曲线拟合", "优化", "回归", "Hertz模型"]
lang: "zh"
slug: "scipy-curve-fitting-zh"
description: "面向材料科学和生物学研究生的SciPy曲线拟合完整教程：线性回归、指数衰减、Hertz压痕模型、置信区间估计和模型选择。"
---


在材料科学和生物学实验中，我们经常需要从离散的数据点中提取连续的物理参数。比如从应力-应变曲线中提取杨氏模量、从松弛实验中提取松弛时间、从AFM压痕曲线中提取样品刚度。曲线拟合是连接实验数据和物理模型的桥梁，而SciPy的curve_fit是完成这一任务的利器。

```python
import numpy as np
from scipy.optimize import curve_fit
```

## 一、曲线拟合的基本原理

曲线拟合的本质是找到一个数学模型的参数，使模型的预测值与实验测量值之间的差异最小。这个差异通常用残差平方和来衡量，因此曲线拟合也常被称为最小二乘法。

SciPy的curve_fit不仅给出最优参数，还提供协方差矩阵，用来估计每个参数的不确定度。这对于科研论文中的误差报告非常重要。

## 二、线性回归：力学测试中最常用的方法

```python
strain = np.array([0.000, 0.005, 0.010, 0.015, 0.020])
stress = np.array([0.0, 8.2, 15.8, 23.5, 31.2])

def linear(x, a, b): return a * x + b

popt, pcov = curve_fit(linear, strain, stress)
E, intercept = popt
E_std = np.sqrt(pcov[0, 0])

# R-squared
residuals = stress - linear(strain, *popt)
r2 = 1 - np.sum(residuals**2) / np.sum((stress - np.mean(stress))**2)
print(f"杨氏模量: {E:.1f} +/- {E_std:.1f} MPa, R2={r2:.4f}")
```

## 三、指数衰减模型：应力松弛实验

```python
time_min = np.array([0, 1, 2, 5, 10, 20, 40, 80])
stress_kPa = np.array([12.5, 10.8, 9.3, 7.2, 5.5, 4.1, 3.2, 2.8])

def exp_decay(t, A, tau, y0): return A * np.exp(-t / tau) + y0

# 从数据估计合理的初始猜测值
A_guess = stress_kPa[0] - stress_kPa[-1]
tau_guess = time_min[-1] / 3

popt, pcov = curve_fit(exp_decay, time_min, stress_kPa, p0=[A_guess, tau_guess, stress_kPa[-1]])
A, tau, y0 = popt
print(f"松弛时间: {tau:.1f} min")
```

## 四、Hertz模型：AFM纳米压痕分析

```python
indentation_nm = np.array([0, 10, 20, 30, 40, 50, 60])
force_nN = np.array([0, 1.5, 4.8, 9.2, 14.5, 20.3, 26.8])

def hertz_model(delta, E_star, R=20.0):
    return (4/3) * E_star * np.sqrt(R) * np.power(np.maximum(delta, 0), 1.5)

popt, pcov = curve_fit(hertz_model, indentation_nm, force_nN,
    p0=[1000], bounds=(1, 1e9))
E_modulus = popt[0] * (1 - 0.5**2)  # 转换为杨氏模量
print(f"杨氏模量: {E_modulus/1000:.1f} kPa")
```

Hertz模型假设材料是各向同性线弹性的、压痕深度远小于样品厚度、针尖与样品之间无粘附作用。对于生物材料，这些假设不总是成立，因此得到的模量应视为表观模量而非绝对的本征材料参数。

## 五、置信区间：不要只报一个数字

```python
from scipy import stats
alpha = 0.05; n = len(indentation_nm); p = len(popt)
t_val = stats.t.ppf(1 - alpha/2, max(0, n - p))
for i, (param, name) in enumerate(zip(popt, ['E_star'])):
    std = np.sqrt(pcov[i, i])
    print(f"{name}: {param:.1f} +/- {t_val*std:.1f} (95% CI)")
```

## 六、常见问题和调试技巧

拟合不收敛通常意味着初始猜测值离真实值太远。解决方法是先将数据和模型函数画出来，目测估计合理的参数值作为初始猜测。参数值不物理——比如杨氏模量为负数——可以通过设置合理的边界约束来避免。不确定度异常大时，通常意味着模型过于复杂而数据量太少，此时可以考虑简化模型或收集更多数据。

### 七、延伸工具

```python
from scipy.optimize import minimize
result = minimize(lambda p: np.sum((y - model(x, *p))**2), [1.0, 0.0], args=(x, y), bounds=[(0, None)]*2)
```

### 参考文献
- Virtanen, P. et al. (2020). SciPy 1.0. *Nature Methods*, 17, 261-272.
- Johnson, M.L. & Faunt, L.M. (1992). Parameter estimation. *Methods in Enzymology*, 210, 1-37.
- Lin, D.C. et al. (2007). Robust AFM force curve analysis. *J. Biomech. Eng.*, 129(3), 430-440.
- Hertz, H. (1882). Ueber die Beruehrung fester elastischer Koerper. *J. Reine Angew. Math.*, 92, 156-171.
