---
title: "Practical Curve Fitting with SciPy: Linear, Nonlinear, and Beyond"
date: "2026-06-26"
category: "python-tutorials"
tags: ["scipy", "curve-fitting", "optimization", "regression", "data-analysis"]
lang: "en"
slug: "scipy-curve-fitting"
description: "Master curve fitting with SciPy: linear and nonlinear regression, confidence intervals, bounds, multiple models (Hertz, exponential, power-law), and real materials examples."
---

Once you have experimental data, extracting meaningful parameters requires fitting. SciPy curve_fit handles everything from simple linear regression to complex nonlinear models, with uncertainty estimation built in.

```python
import numpy as np
from scipy.optimize import curve_fit
```

## 1. Linear Regression

```python
def linear(x, a, b): return a * x + b

popt, pcov = curve_fit(linear, strain, stress)
E_modulus, intercept = popt

# Uncertainty
E_std = np.sqrt(pcov[0, 0])

# R-squared
residuals = stress - linear(strain, *popt)
r2 = 1 - np.sum(residuals**2) / np.sum((stress - np.mean(stress))**2)
print(f"E = {E_modulus:.1f} +/- {E_std:.1f}, R2 = {r2:.3f}")
```

## 2. Exponential Decay: Stress Relaxation

```python
def exp_decay(t, A, tau, y0): return A * np.exp(-t / tau) + y0

# Smart initial guesses
A_guess = force[0] - force[-1]
tau_guess = time[-1] / 3
y0_guess = force[-1]

popt, pcov = curve_fit(exp_decay, time, force, p0=[A_guess, tau_guess, y0_guess])
A, tau, y0 = popt
print(f"Relaxation time: {tau:.1f} s, Amplitude: {A:.1f} nN")
```

## 3. Hertz Model: AFM Indentation

```python
def hertz(delta, E_star, R=20.0):
    """Spherical indenter Hertz model."""
    return (4/3) * E_star * np.sqrt(R) * np.power(np.maximum(delta, 0), 1.5)

popt, pcov = curve_fit(hertz, indentation, force, p0=[1000], bounds=(1, 1e9))
E_star = popt[0]
E = E_star * (1 - 0.5**2)  # Reduced to Young's modulus
print(f"Young's modulus: {E/1000:.1f} kPa")
```

## 4. Confidence Intervals

```python
from scipy import stats
alpha = 0.05; n = len(x); p = len(popt)
t_val = stats.t.ppf(1 - alpha/2, max(0, n - p))
for i, (param, std) in enumerate(zip(popt, np.sqrt(np.diag(pcov)))):
    ci = t_val * std
    print(f"Param {i}: {param:.3f} +/- {ci:.3f} (95% CI)")
```

## 5. Model Comparison with AIC

```python
def aic(n_params, residuals):
    n = len(residuals)
    return n * np.log(np.sum(residuals**2) / n) + 2 * n_params

print(f"AIC linear: {aic(2, residuals_lin):.1f}")
print(f"AIC exp: {aic(3, residuals_exp):.1f}")
```

## 6. Common Failures

| Problem | Cause | Fix |
|---------|-------|-----|
| Optimal parameters not found | Bad initial guess | Try different p0, visualize first |
| Unrealistic parameters | No bounds | Add bounds=(low, high) |
| Huge uncertainties | Overparameterized | Fewer params or fix known values |
| NaN in covariance | Singular matrix | Check for redundant parameters |

## 7. Beyond curve_fit

```python
from scipy.optimize import minimize
result = minimize(lambda p: np.sum((y - model(x, *p))**2), [1.0, 0.1], args=(x, y), bounds=[(0, None)]*2)
```

## References
- Virtanen, P. et al. (2020). SciPy 1.0. *Nature Methods*, 17, 261-272.
- Johnson, M.L. & Faunt, L.M. (1992). Parameter estimation. *Methods in Enzymology*, 210, 1-37.
