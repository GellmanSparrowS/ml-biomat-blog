---
title: "Practical Curve Fitting with SciPy: From Basics to Advanced Models"
date: "2026-06-26"
updated: "2026-10-28"
category: "python-tutorials"
tags: ["scipy", "curve-fitting", "optimization", "regression", "data-analysis", "biomaterials"]
lang: "en"
slug: "scipy-curve-fitting"
description: "Fit linear trends, stress relaxation, and indentation models with SciPy while tracking parameter units and initial guesses. Interpret residuals, covariance matrices, and confidence intervals to turn a fitted curve into an inspectable physical calculation."
---

When you run an experiment, you get data points. To extract meaningful physical parameters from those points, you need to fit a model. SciPy's `optimize.curve_fit` is the workhorse for this task. This guide covers everything from a simple straight-line fit to complex nonlinear models, with worked examples for materials and biology data analysis.

```python
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
```

## Foundations
### 1. What Is Curve Fitting?

Curve fitting means finding the parameters of a mathematical model that best match your data. For example, if you pull on a silk fiber and record force vs. extension, the slope of the initial linear region is the fiber's stiffness. Fitting a line gives you that slope plus an uncertainty estimate.

The general workflow:
1. Define a model function `f(x, param1, param2, ...)`
2. Call `curve_fit(f, x_data, y_data)` which returns optimal parameters and their covariance
3. Extract parameters and uncertainties from the results

### 2. Linear Regression: The Foundation

![The five teaching points are fitted by y = 1.97x + 1.06](/static/images/article-guides/comp-guide-residuals-en.svg)

The five teaching points are fitted by y = 1.97x + 1.06. The lower panel shows observed minus fitted values, separating the remaining errors from the trend so that their signs and magnitudes are easy to compare.


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

## Fitting Physical Models
### 3. Exponential Decay: Stress Relaxation

![Measured stress-relaxation data with an exponential decay fit and equilibrium stress level](/static/images/posts/scipy-curve-fitting/relaxation-en.webp)

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

### 4. Hertz Model: AFM Nanoindentation

Atomic Force Microscopy (AFM) nanoindentation measures the stiffness of tiny sample regions. The Hertz model relates indentation depth to force for an elastic half-space:

F = (4/3) * E* * sqrt(R) * delta^(3/2)

For a probe much stiffer than the sample, E* = E / (1 - nu^2) is the reduced modulus, R is tip radius, and delta is indentation depth. The force–indentation slope is contact stiffness; extracting a modulus also requires the contact geometry. In the teaching calculation below, a 1000 nm spherical radius keeps the 0–40 nm indentation range small relative to the probe radius.

```python
# Teaching indentation values; spherical probe radius = 1000 nm
indentation = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40])  # nm
force = np.array([0, 0.3, 1.1, 2.5, 4.3, 6.8, 9.9, 13.6, 18.0])  # nN

def hertz(delta_nm, E_star_MPa, R_nm=1000.0):
    delta_m = np.maximum(delta_nm, 0) * 1e-9
    E_star_Pa = E_star_MPa * 1e6
    force_N = (4/3) * E_star_Pa * np.sqrt(R_nm * 1e-9) * delta_m**1.5
    return force_N * 1e9  # nN, matching the observations

# Fit in MPa to keep the numerical parameter scale convenient
popt, pcov = curve_fit(hertz, indentation, force, p0=[1.0], bounds=(0, np.inf))
E_star_MPa = popt[0]
E_MPa = E_star_MPa * (1 - 0.5**2)  # Rigid probe, sample Poisson ratio = 0.5
print(f"Young's modulus: {E_MPa * 1000:.1f} kPa")
```

**Important**: The Hertz model assumes linear elasticity, small strains, and a homogeneous material. For biomaterials, validate these assumptions by checking:
- Indentation small relative to both probe radius and sample thickness (check geometry and substrate effects)
- Multiple locations show consistent results
- Loading rate independence (or report the rate)

### 5. Viscoelastic Models

The Standard Linear Solid (SLS) model combines an equilibrium spring with one Maxwell branch. Under a fixed strain, its relaxation modulus is E(t) = E_eq + E_branch exp(−t/τ), with τ = η / E_branch. Multiplying E(t) by the imposed strain gives the stress history. This is a stress-relaxation calculation.

```python
def sls_relaxation(t, E_eq, E_branch, tau):
    return E_eq + E_branch * np.exp(-t / tau)

# Synthetic relaxation-modulus data in kPa; time in seconds
sls_time = np.array([0, 1, 2, 5, 10, 20, 50, 100, 200])
sls_noise = np.array([0.05, -0.03, 0.02, -0.04, 0.03, -0.02, 0.01, -0.01, 0.02])
sls_modulus = sls_relaxation(sls_time, 3.0, 9.0, 40.0) + sls_noise
sls_popt, sls_pcov = curve_fit(
    sls_relaxation, sls_time, sls_modulus,
    p0=[2.5, 8.0, 30.0], bounds=([0, 0, 1e-9], [np.inf, np.inf, np.inf])
)
E_eq, E_branch, tau_sls = sls_popt
print(f"Instantaneous modulus: {E_eq + E_branch:.2f} kPa")
print(f"Equilibrium modulus: {E_eq:.2f} kPa")
print(f"Relaxation time: {tau_sls:.2f} s")
print(f"Branch viscosity: {E_branch * tau_sls:.2f} kPa*s")
```

The separate `sls_popt` and `sls_pcov` variables retain the Hertz-fit results in `popt` and `pcov` for the confidence-interval calculation below. The model relation follows the [COMSOL linear-viscoelasticity formulation](https://doc.comsol.com/6.4/doc/com.comsol.help.sme/sme_ug_theory.06.029.html).

## Uncertainty and Beyond
### 6. Confidence Intervals

![This illustrative covariance matrix gives standard errors of 0.2 for the slope and 0.1 for the intercept, with correlation −0.75](/static/images/article-guides/comp-guide-covariance-en.svg)

This illustrative covariance matrix gives standard errors of 0.2 for the slope and 0.1 for the intercept, with correlation −0.75. Converting these standard errors into confidence intervals also requires a confidence level and an appropriate model-based multiplier.


Never report fitted parameters without uncertainties. The covariance matrix from `curve_fit` gives approximate parameter variances under the local linearization of the model. Square roots of its diagonal give standard errors; the [SciPy documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html) explains how measurement uncertainties and `absolute_sigma` affect their scale:

```python
from scipy import stats

alpha = 0.05  # 95% confidence
n = len(indentation)
p = len(popt)
dof = max(0, n - p)
t_val = stats.t.ppf(1 - alpha/2, dof)

for i, (param, name) in enumerate(zip(popt, ['E_star (MPa)'])):
    std = np.sqrt(pcov[i, i])
    ci = t_val * std
    print(f"{name}: {param:.3f} +/- {ci:.3f} (95% CI)")
```

### 7. Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| "Optimal parameters not found" | Bad initial guess | Visualize data, try different p0 |
| Negative modulus | No bounds | Add `bounds=(0, np.inf)` |
| Huge uncertainties | Too few data points | Collect more data in the region of interest |
| Fit looks wrong at edges | Model doesn't fit extremes | Check if model is appropriate |
| NaN in covariance | Over-parameterized | Simplify model or fix some parameters |

### 8. When curve_fit Is Not Enough

```python
from scipy.optimize import minimize

def objective(params, x, y, model):
    return np.sum((y - model(x, *params))**2)

result = minimize(objective, [1.0], args=(indentation, force, hertz), bounds=[(0, None)])
print(f"Constrained result: {result.x}")
```

## References
- Virtanen, P. et al. (2020). SciPy 1.0. *Nature Methods*, 17, 261-272.
- Lin, D.C. et al. (2007). Robust strategies for automated AFM force curve analysis. *J. Biomech. Eng.*, 129(6), 904-912.
- Oliver, W.C. & Pharr, G.M. (1992). An improved technique for determining hardness and elastic modulus. *J. Mater. Res.*, 7(6), 1564-1583.
- Johnson, M.L. & Faunt, L.M. (1992). Parameter estimation. *Methods in Enzymology*, 210, 1-37.
- Lin, D.C. et al. (2007). Robust AFM force curve analysis. *J. Biomech. Eng.*, 129(6), 904-912.
- Burnham, K.P. & Anderson, D.R. (2002). *Model Selection and Multimodel Inference*. Springer.

## Model Selection and Goodness of Fit

Choosing between competing models requires more than just comparing R-squared values. The Akaike Information Criterion (AIC) penalizes models with more parameters, helping avoid overfitting. For nested models, the F-test provides a formal statistical comparison.

Cross-validation is essential when the goal is prediction rather than description. Leave-one-out cross-validation is appropriate for very small datasets common in materials research. For each data point, fit the model without that point and calculate the prediction error. The average error across all points gives a realistic estimate of predictive performance.

When reporting fitted parameters in publications, include not just the best-fit values and standard errors but also the correlation matrix between parameters. Highly correlated parameters indicate that the model may be overparameterized—different combinations of parameter values produce nearly identical fits. This is a red flag that should be discussed transparently.
