---
title: "Curve Fitting with SciPy: Linear to Nonlinear Models"
date: "2026-06-26"
category: "python-tutorials"
tags: ["scipy", "curve-fitting", "optimization", "regression", "tutorial"]
lang: "en"
slug: "scipy-curve-fitting"
description: "Practical curve fitting with scipy.optimize: linear regression, exponential decay, Hertz model, with confidence intervals."
---

## Why SciPy

Fit stress-strain data, relaxation curves, or any experimental data to extract parameters. SciPy's `curve_fit` handles both linear and nonlinear models.

```python
from scipy.optimize import curve_fit
import numpy as np
```

## Linear Regression

```python
def linear(x, a, b): return a * x + b
popt, pcov = curve_fit(linear, strain, stress)
E, intercept = popt
E_std = np.sqrt(pcov[0, 0])
```

## Exponential Decay

```python
def exp_decay(t, A, tau, y0): return A * np.exp(-t / tau) + y0
popt, pcov = curve_fit(exp_decay, time, force, p0=[1.0, 10.0, 0.0])
relax_time = popt[1]
```

## Hertz Model (Nonlinear)

```python
def hertz(delta, E_star, R):
    return (4/3) * E_star * np.sqrt(R) * np.power(np.maximum(delta, 0), 1.5)
popt, _ = curve_fit(hertz, indent, force, p0=[1000], bounds=(1, 1e9))
```

- docs.scipy.org
