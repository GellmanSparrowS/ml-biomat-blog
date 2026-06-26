---
title: "SciPy曲线拟合完全指南：线性、非线性与进阶"
date: "2026-06-26"
category: "python-tutorials"
tags: ["scipy", "曲线拟合", "优化", "回归", "数据分析"]
lang: "zh"
slug: "scipy-curve-fitting-zh"
description: "掌握SciPy曲线拟合：线性和非线性回归、置信区间、参数约束、多模型选择和真实材料数据案例。"
---

拿到实验数据后，提取参数需要曲线拟合。SciPy的curve_fit从简单线性回归到复杂非线性模型都能处理，内置参数不确定性估计。

```python
import numpy as np
from scipy.optimize import curve_fit
```

## 1. 线性回归

```python
def linear(x, a, b): return a * x + b
popt, pcov = curve_fit(linear, strain, stress)
E, intercept = popt
E_std = np.sqrt(pcov[0, 0])
residuals = stress - linear(strain, *popt)
r2 = 1 - np.sum(residuals**2) / np.sum((stress - np.mean(stress))**2)
print(f"E = {E:.1f} +/- {E_std:.1f}, R2 = {r2:.3f}")
```

## 2. 指数衰减：应力松弛

```python
def exp_decay(t, A, tau, y0): return A * np.exp(-t / tau) + y0
A_guess = force[0] - force[-1]
tau_guess = time[-1] / 3
popt, pcov = curve_fit(exp_decay, time, force, p0=[A_guess, tau_guess, force[-1]])
print(f"松弛时间: {popt[1]:.1f} s")
```

## 3. Hertz模型：AFM压痕

```python
def hertz(delta, E_star, R=20.0):
    return (4/3) * E_star * np.sqrt(R) * np.power(np.maximum(delta, 0), 1.5)
popt, pcov = curve_fit(hertz, indentation, force, p0=[1000], bounds=(1, 1e9))
E = popt[0] * (1 - 0.5**2)
print(f"杨氏模量: {E/1000:.1f} kPa")
```

## 4. 置信区间

```python
from scipy import stats
alpha = 0.05; t_val = stats.t.ppf(1 - alpha/2, max(0, len(x) - len(popt)))
for i, (p, s) in enumerate(zip(popt, np.sqrt(np.diag(pcov)))):
    print(f"参数{i}: {p:.3f} +/- {t_val*s:.3f} (95%置信区间)")
```

## 5. 模型比较：AIC

```python
def aic(n_params, residuals):
    n = len(residuals)
    return n * np.log(np.sum(residuals**2) / n) + 2 * n_params
print(f"AIC: 越小越好")
```

## 6. 常见失败

| 问题 | 原因 | 解决 |
|------|------|------|
| 拟合不收敛 | 初始值不好 | 可视化后调整p0 |
| 参数不合理 | 无约束 | 加bounds |
| 不确定度过大 | 过参数化 | 减少参数或固定已知值 |

## 参考文献
- Virtanen, P. et al. (2020). SciPy 1.0. *Nature Methods*, 17, 261-272.

## 参考文献
- Virtanen, P. et al. (2020). SciPy 1.0. *Nature Methods*, 17, 261-272.
- Johnson, M.L. & Faunt, L.M. (1992). Parameter estimation. *Methods in Enzymology*, 210, 1-37.
