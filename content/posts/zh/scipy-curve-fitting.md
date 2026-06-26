---
title: "SciPy曲线拟合实战：线性回归到非线性模型"
date: "2026-06-26"
category: "python-tutorials"
tags: ["scipy", "曲线拟合", "优化", "回归", "教程"]
lang: "zh"
slug: "scipy-curve-fitting-zh"
description: "SciPy曲线拟合实战：线性回归、指数衰减、Hertz模型，含置信区间估计。"
---

## 为什么用SciPy

拉伸数据或松弛曲线需要提取参数。SciPy的curve_fit支持线性和非线性模型。

```python
from scipy.optimize import curve_fit
import numpy as np
```

## 线性回归

```python
def linear(x, a, b): return a * x + b
popt, pcov = curve_fit(linear, strain, stress)
E, intercept = popt
E_std = np.sqrt(pcov[0, 0])
```

## 指数衰减

```python
def exp_decay(t, A, tau, y0): return A * np.exp(-t / tau) + y0
popt, _ = curve_fit(exp_decay, time, force, p0=[1.0, 10.0, 0.0])
relax_time = popt[1]
```

## Hertz模型

```python
def hertz(delta, E_star, R):
    return (4/3) * E_star * np.sqrt(R) * np.power(np.maximum(delta, 0), 1.5)
popt, _ = curve_fit(hertz, indent, force, p0=[1000], bounds=(1, 1e9))
```

- docs.scipy.org
