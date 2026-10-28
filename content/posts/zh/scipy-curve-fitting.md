---
title: "SciPy曲线拟合完全指南：从线性回归到非线性建模"
date: "2026-06-27"
updated: "2026-10-28"
category: "python-tutorials"
tags: ["scipy", "曲线拟合", "优化", "回归", "Hertz模型"]
lang: "zh"
slug: "scipy-curve-fitting-zh"
description: "从线性趋势、应力松弛到压痕模型，演示 SciPy 曲线拟合中的函数定义、初值、单位与参数边界。通过残差、协方差矩阵和置信区间，理解拟合参数的含义，并检查模型与测量数据是否匹配。"
---


在材料科学和生物学实验中，我们经常需要从离散的数据点中提取连续的物理参数。比如从应力-应变曲线中提取杨氏模量、从松弛实验中提取松弛时间、从AFM压痕曲线中提取样品刚度。曲线拟合是连接实验数据和物理模型的桥梁，而SciPy的curve_fit是完成这一任务的利器。

```python
import numpy as np
from scipy.optimize import curve_fit
```

## 一、曲线拟合的基本原理

| 问题类型 | 模型函数 | SciPy 工具 |
|---|---|---|
| 线性关系 | y = ax + b | np.polyfit 或 linregress |
| 指数衰减 | a·exp(-t/τ) + c | curve_fit |
| 幂律关系 | a·x^b | curve_fit（先取对数给出初猜） |
| Hertz 压痕 | F = k·δ^n | curve_fit + 参数边界 |
| 参数置信区间 | 由协方差矩阵估计 | curve_fit 返回的 pcov |

曲线拟合的本质是找到一个数学模型的参数，使模型的预测值与实验测量值之间的差异最小。这个差异通常用残差平方和来衡量，因此曲线拟合也常被称为最小二乘法。

SciPy的curve_fit不仅给出最优参数，还提供协方差矩阵，用来估计每个参数的不确定度。这对于科研论文中的误差报告非常重要。

## 二、线性回归：力学测试中最常用的方法

![五个教学数据点拟合得到 y = 1.97x + 1.06](/static/images/article-guides/comp-guide-residuals-zh.svg)

五个教学数据点拟合得到 y = 1.97x + 1.06。下图将观测值减去拟合值，使剩余误差脱离整体趋势，便于比较残差的正负与大小。


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

保持应变不变时，标准线性固体模型的松弛模量可写为 E(t) = E_eq + E_branch·exp(−t/τ)，其中 τ = η/E_branch。乘以施加的应变，就得到应力随时间的衰减；下面代码拟合的 A 和 y0 分别是应力衰减幅值与平衡应力，单位为 kPa。这个关系对应 [COMSOL 线性黏弹性模型中的单 Maxwell 支路](https://doc.comsol.com/6.4/doc/com.comsol.help.sme/sme_ug_theory.06.029.html)。

![应力松弛数据与指数衰减拟合及平衡应力水平](/static/images/posts/scipy-curve-fitting/relaxation-zh.webp)

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

力–压痕曲线的局部斜率是接触刚度。要提取杨氏模量，还需结合探针几何和接触模型：对比样品刚得多的球形探针，Hertz 关系为 F = (4/3)E*√R·δ^(3/2)，E* = E/(1−ν²)。下面的教学计算取球半径 1000 nm，使 0–60 nm 的压痕范围相对半径较小，并在函数内部统一为 SI 单位。

```python
# 教学压痕数值；球形探针半径为 1000 nm
indentation_nm = np.array([0, 10, 20, 30, 40, 50, 60])
force_nN = np.array([0, 1.5, 4.8, 9.2, 14.5, 20.3, 26.8])

def hertz_model(delta_nm, E_star_MPa, R_nm=1000.0):
    delta_m = np.maximum(delta_nm, 0) * 1e-9
    E_star_Pa = E_star_MPa * 1e6
    force_N = (4/3) * E_star_Pa * np.sqrt(R_nm * 1e-9) * delta_m**1.5
    return force_N * 1e9  # 返回 nN，与观测数据单位一致

popt, pcov = curve_fit(hertz_model, indentation_nm, force_nN,
    p0=[1.0], bounds=(0, np.inf))
E_modulus_MPa = popt[0] * (1 - 0.5**2)  # 刚性探针，样品泊松比取 0.5
print(f"杨氏模量: {E_modulus_MPa * 1000:.1f} kPa")
```

Hertz模型假设材料是各向同性线弹性的、压痕深度远小于样品厚度、针尖与样品之间无粘附作用。对于生物材料，这些假设不总是成立，因此得到的模量应视为表观模量而非绝对的本征材料参数。

## 五、置信区间：不要只报一个数字

`curve_fit` 返回的 `pcov` 在模型的局部线性近似下估计参数协方差；对角元开平方得到参数标准误。其数值还受观测误差设置及 `absolute_sigma` 影响，可结合 [SciPy 文档](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html) 选择误差定义。

![该教学协方差矩阵给出斜率标准误 0.2、截距标准误 0.1，以及参数相关系数 −0.75](/static/images/article-guides/comp-guide-covariance-zh.svg)

该教学协方差矩阵给出斜率标准误 0.2、截距标准误 0.1，以及参数相关系数 −0.75。计算置信区间还需指定置信水平，并结合模型选取相应的分位数。


```python
from scipy import stats
alpha = 0.05; n = len(indentation_nm); p = len(popt)
t_val = stats.t.ppf(1 - alpha/2, max(0, n - p))
for i, (param, name) in enumerate(zip(popt, ['E_star (MPa)'])):
    std = np.sqrt(pcov[i, i])
    print(f"{name}: {param:.3f} +/- {t_val*std:.3f} (95% CI)")
```

## 六、常见问题和调试技巧

拟合不收敛通常意味着初始猜测值离真实值太远。解决方法是先将数据和模型函数画出来，目测估计合理的参数值作为初始猜测。参数值不物理——比如杨氏模量为负数——可以通过设置合理的边界约束来避免。不确定度异常大时，通常意味着模型过于复杂而数据量太少，此时可以考虑简化模型或收集更多数据。

### 七、延伸工具

```python
from scipy.optimize import minimize
result = minimize(
    lambda p, x, y: np.sum((y - hertz_model(x, *p))**2),
    [1.0], args=(indentation_nm, force_nN), bounds=[(0, None)]
)
print(f"约束优化得到的约化模量: {result.x[0]:.3f} MPa")
```

### 参考文献
- Virtanen, P. et al. (2020). SciPy 1.0. *Nature Methods*, 17, 261-272.
- Johnson, M.L. & Faunt, L.M. (1992). Parameter estimation. *Methods in Enzymology*, 210, 1-37.
- Lin, D.C. et al. (2007). Robust AFM force curve analysis. *J. Biomech. Eng.*, 129(3), 430-440.
- Hertz, H. (1882). Ueber die Beruehrung fester elastischer Koerper. *J. Reine Angew. Math.*, 92, 156-171.
