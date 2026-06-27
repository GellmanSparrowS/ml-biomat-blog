---
title: "Practical Curve Fitting with SciPy: From Basics to Advanced Models"
date: "2026-06-26"
category: "python-tutorials"
tags: ["scipy", "curve-fitting", "optimization", "regression", "data-analysis", "biomaterials"]
lang: "en"
slug: "scipy-curve-fitting"
description: "A comprehensive guide to curve fitting with SciPy for materials and biology researchers. Linear regression, exponential decay, Hertz indentation, viscoelastic models, with complete code and real examples."
---

When you run an experiment, you get data points. To extract meaningful physical parameters from those points, you need to fit a model. SciPy's `optimize.curve_fit` is the workhorse for this task. This guide covers everything from a simple straight-line fit to complex nonlinear models, with every example grounded in real materials or biology data.

```python
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
```

## 1. What Is Curve Fitting?

Curve fitting means finding the parameters of a mathematical model that best match your data. For example, if you pull on a silk fiber and record force vs. extension, the slope of the initial linear region is the fiber's stiffness. Fitting a line gives you that slope plus an uncertainty estimate.

The general workflow:
1. Define a model function `f(x, param1, param2, ...)`
2. Call `curve_fit(f, x_data, y_data)` which returns optimal parameters and their covariance
3. Extract parameters and uncertainties from the results

## 2. Linear Regression: The Foundation

Most materials characterization starts with linear fitting. Young's modulus from a stress-strain curve, calibration curves, and many standard analyses use linear regression.

```python
# Example: tensile test on an electrospun PCL fiber
strain = np.array([0.00, 0.01, 0.02, 0.03, 0.04, 0.05])
stress = np.array([0.0, 1.2, 2.5, 3.9, 5.1, 6.4])  # MPa

def linear(x, a, b):
    return a * x + b

popt, pcov = curve_fit(linear, strain, stress)
Youngs_modulus, intercept = popt

# Extract uncertainties
E_std = np.sqrt(pcov[0, 0])
intercept_std = np.sqrt(pcov[1, 1])

print(f"Young's modulus: {Youngs_modulus:.1f} +/- {E_std:.1f} MPa")

# Compute R-squared
residuals = stress - linear(strain, *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((stress - np.mean(stress))**2)
r2 = 1 - (ss_res / ss_tot)
print(f"R-squared: {r2:.4f}")

# Visualize
strain_fit = np.linspace(0, 0.05, 100)
stress_fit = linear(strain_fit, *popt)

plt.figure(figsize=(6, 4))
plt.plot(strain, stress, 'bo', label='Experimental data')
plt.plot(strain_fit, stress_fit, 'r-', label=f'Fit: E = {Youngs_modulus:.1f} MPa')
plt.xlabel('Strain'); plt.ylabel('Stress (MPa)')
plt.legend(); plt.tight_layout()
```

## 3. Exponential Decay: Stress Relaxation

When you hold a biomaterial at constant strain, the stress decays over time. This stress relaxation follows an exponential model. Understanding the relaxation time is critical for applications like tissue scaffolds and drug delivery systems.

```python
# Stress relaxation data: collagen gel held at 10% strain
time = np.array([0, 5, 10, 20, 40, 80, 160, 320])  # seconds
stress = np.array([12.0, 10.2, 8.9, 7.1, 5.5, 4.2, 3.1, 2.5])  # kPa

def exp_decay(t, A, tau, y0):
    return A * np.exp(-t / tau) + y0

# Smart initial guesses from the data
A_guess = stress[0] - stress[-1]   # Total relaxation amplitude
tau_guess = time[-1] / 3           # Relaxation time ~1/3 of total time
y0_guess = stress[-1]              # Equilibrium stress

popt, pcov = curve_fit(exp_decay, time, stress, p0=[A_guess, tau_guess, y0_guess])
A, tau, y0 = popt
print(f"Relaxation amplitude: {A:.2f} kPa")
print(f"Relaxation time: {tau:.1f} s")
print(f"Equilibrium stress: {y0:.2f} kPa")

# Plot
t_fit = np.linspace(0, 350, 200)
plt.figure(figsize=(6, 4))
plt.plot(time, stress, 'bs', markersize=8, label='Data')
plt.plot(t_fit, exp_decay(t_fit, *popt), 'r-', linewidth=2, label=f'tau = {tau:.1f} s')
plt.xlabel('Time (s)'); plt.ylabel('Stress (kPa)')
plt.legend(); plt.tight_layout()
```

## 4. Hertz Model: AFM Nanoindentation

Atomic Force Microscopy (AFM) nanoindentation measures the stiffness of tiny sample regions. The Hertz model relates indentation depth to force for an elastic half-space:

F = (4/3) * E* * sqrt(R) * delta^(3/2)

where E* = E / (1 - nu^2) is the reduced modulus, R is tip radius, and delta is indentation depth.

```python
# AFM indentation on a silk fibroin film
indentation = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40])  # nm
force = np.array([0, 0.3, 1.1, 2.5, 4.3, 6.8, 9.9, 13.6, 18.0])  # nN

def hertz(delta, E_star, R=20.0):
    return (4/3) * E_star * np.sqrt(R) * np.power(np.maximum(delta, 0), 1.5)

# Fit with bounds to prevent non-physical values
popt, pcov = curve_fit(hertz, indentation, force, p0=[1000], bounds=(1, 1e9))
E_star = popt[0]
E = E_star * (1 - 0.5**2)  # Convert reduced modulus to Young's (nu=0.5 for incompressible)
print(f"Young's modulus: {E/1000:.1f} kPa")
```

**Important**: The Hertz model assumes linear elasticity, small strains, and a homogeneous material. For biomaterials, validate these assumptions by checking:
- Indentation depth < 10% of sample thickness (avoid substrate effects)
- Multiple locations show consistent results
- Loading rate independence (or report the rate)

## 5. Viscoelastic Models

Many biomaterials show both elastic and viscous behavior. The Standard Linear Solid (SLS) model captures this:

```python
def sls_model(t, E_instant, E_equilibrium, eta):
    tau = eta / (E_instant - E_equilibrium)
    return E_equilibrium + (E_instant - E_equilibrium) * np.exp(-t / tau)

# Creep test: constant stress, measure strain over time
time = np.array([0, 1, 2, 5, 10, 20, 50, 100, 200])  # s
strain = np.array([0.010, 0.012, 0.013, 0.015, 0.017, 0.018, 0.020, 0.021, 0.022])

# Initial guesses from data
E_inst_guess = 1 / strain[0] * 1000  # kPa (from instantaneous response)
E_eq_guess = 1 / strain[-1] * 1000
eta_guess = 100  # kPa*s

popt, pcov = curve_fit(sls_model, time, strain, p0=[E_inst_guess, E_eq_guess, eta_guess],
                       bounds=([0,0,0], [np.inf, np.inf, np.inf]))
print(f"Instantaneous modulus: {popt[0]:.1f} kPa")
print(f"Equilibrium modulus: {popt[1]:.1f} kPa")
print(f"Viscosity: {popt[2]:.1f} kPa*s")
```

## 6. Confidence Intervals

Never report fitted parameters without uncertainties. The covariance matrix from curve_fit gives standard errors:

```python
from scipy import stats

alpha = 0.05  # 95% confidence
n = len(indentation)
p = len(popt)
dof = max(0, n - p)
t_val = stats.t.ppf(1 - alpha/2, dof)

for i, (param, name) in enumerate(zip(popt, ['E_star'])):
    std = np.sqrt(pcov[i, i])
    ci = t_val * std
    print(f"{name}: {param:.1f} +/- {ci:.1f} (95% CI)")
```

## 7. Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| "Optimal parameters not found" | Bad initial guess | Visualize data, try different p0 |
| Negative modulus | No bounds | Add `bounds=(0, None)` |
| Huge uncertainties | Too few data points | Collect more data in the region of interest |
| Fit looks wrong at edges | Model doesn't fit extremes | Check if model is appropriate |
| NaN in covariance | Over-parameterized | Simplify model or fix some parameters |

## 8. When curve_fit Is Not Enough

```python
from scipy.optimize import minimize

def objective(params, x, y, model):
    return np.sum((y - model(x, *params))**2)

result = minimize(objective, [1.0, 0.1], args=(x, y, linear), bounds=[(0, None)]*2)
print(f"Constrained result: {result.x}")
```

## References

- Virtanen, P. et al. (2020). SciPy 1.0. *Nature Methods*, 17, 261-272.
- Lin, D.C. et al. (2007). Robust strategies for automated AFM force curve analysis. *J. Biomech. Eng.*, 129(6), 904-912.
- Oliver, W.C. & Pharr, G.M. (1992). An improved technique for determining hardness and elastic modulus. *J. Mater. Res.*, 7(6), 1564-1583.

## References
- Virtanen, P. et al. (2020). SciPy 1.0. *Nature Methods*, 17, 261-272.
- Johnson, M.L. & Faunt, L.M. (1992). Parameter estimation. *Methods in Enzymology*, 210, 1-37.
- Lin, D.C. et al. (2007). Robust AFM force curve analysis. *J. Biomech. Eng.*, 129(6), 904-912.


## Model Selection and Goodness of Fit

Choosing between competing models requires more than just comparing R-squared values. The Akaike Information Criterion (AIC) penalizes models with more parameters, helping avoid overfitting. For nested models, the F-test provides a formal statistical comparison.

Cross-validation is essential when the goal is prediction rather than description. Leave-one-out cross-validation is appropriate for very small datasets common in materials research. For each data point, fit the model without that point and calculate the prediction error. The average error across all points gives a realistic estimate of predictive performance.

When reporting fitted parameters in publications, include not just the best-fit values and standard errors but also the correlation matrix between parameters. Highly correlated parameters indicate that the model may be overparameterized—different combinations of parameter values produce nearly identical fits. This is a red flag that should be discussed transparently.

## References
- Burnham, K.P. & Anderson, D.R. (2002). *Model Selection and Multimodel Inference*. Springer.
