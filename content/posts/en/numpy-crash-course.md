---
title: "NumPy Crash Course for Experimentalists"
date: "2026-06-26"
category: "python-tutorials"
tags: ["numpy", "python", "arrays", "scientific-computing", "tutorial"]
lang: "en"
slug: "numpy-crash-course"
description: "Practical NumPy for materials researchers: arrays, broadcasting, loading experimental data, and everyday operations."
---

## Why NumPy

If you process numerical data in Python, NumPy is the foundation. Tensile tests, AFM curves, XRD patterns, MD trajectories all become NumPy arrays.

```python
import numpy as np
```

## Creating Arrays

```python
strains = np.array([0.0, 0.01, 0.02, 0.05, 0.10])
stresses = np.array([0, 15, 28, 52, 74])
data = np.loadtxt("tensile_test.csv", delimiter=",", skiprows=1)
z, force = data[:, 0], data[:, 1]
```

## Array Operations

```python
mean = np.mean(stresses)
coeffs = np.polyfit(strains, stresses, 1)
E_modulus = coeffs[0]  # Young's modulus
elastic = stresses[strains < 0.02]  # Boolean indexing
```

## Common Patterns

```python
raw = np.loadtxt("force_curve_001.txt", skiprows=320)
z_piezo, deflection = raw[:, 0], raw[:, 1]
force = 0.06 * 45.0 * (deflection - np.median(deflection[:100]))
```

- numpy.org/doc
- VanderPlas, J. (2016). Python Data Science Handbook. OReilly.
