---
title: "NumPy for Materials Research: From Zero to Productive"
date: "2026-06-26"
updated: "2026-10-28"
category: "python-tutorials"
tags: ["numpy", "python", "arrays", "scientific-computing", "data-analysis", "tutorial"]
lang: "en"
slug: "numpy-crash-course"
description: "Load experimental measurements into arrays and work with slicing, Boolean masks, broadcasting, and summary statistics. Use these operations to align observations, center columns, fit simple relationships, and save processed numerical results."
---

## Why Every Materials Scientist Needs NumPy

If you process experimental data, NumPy is non-negotiable. It turns raw `.txt` files from your tensile tester, AFM, or XRD into Python arrays you can analyze, plot, and export. This guide assumes you have Python installed and takes you from zero to productive with real lab data.

```python
import numpy as np
```

## Core Array Operations
### 1. The NumPy Array: Your Data Container

A NumPy array is a grid of numbers — like a column in Excel, but faster and more powerful:

```python
# From a Python list
strains = np.array([0.0, 0.005, 0.010, 0.020, 0.050, 0.100])
stresses = np.array([0, 8, 15, 28, 52, 74])  # MPa

# Convenience functions
x = np.linspace(0, 0.5, 200)       # 200 points from 0 to 0.5
zeros = np.zeros((10, 3))          # 10x3 matrix of zeros
ones = np.ones(50)                 # 50-element vector of ones
empty = np.empty(100)              # Uninitialized (fast, but fill before use)
```

### Array Properties

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.shape)    # (2, 3) — 2 rows, 3 columns
print(arr.ndim)     # 2 — 2-dimensional
print(arr.dtype)    # int64 — data type
print(arr.size)     # 6 — total elements
```

### 2. Loading Experimental Data

Most lab instruments export tabular data. NumPy handles all common formats:

```python
# Generic: columns separated by spaces or tabs
data = np.loadtxt("tensile_test.txt", skiprows=0)

# CSV with headers
data = np.loadtxt("mechanical_data.csv", delimiter=",", skiprows=1)

# AFM force curve (Bruker: 320-line header)
raw = np.loadtxt("force_curve.001", skiprows=320)

# Column extraction
z_piezo = raw[:, 0]        # First column
deflection = raw[:, 1]     # Second column

# Multiple columns at once
time, force, displacement = data[:, 0], data[:, 1], data[:, 2]

# Genfromtext: handles missing values
data_with_nans = np.genfromtxt("messy_data.csv", delimiter=",", skip_header=1, filling_values=0)
```

### 3. Element-Wise Operations (No Loops)

NumPy's real power: operations apply to every element simultaneously. No `for` loops needed:

```python
# Arithmetic
stress_pascals = stresses * 1e6          # MPa to Pa
strain_percent = strains * 100           # fraction to percent
engineering_stress = force / area        # F/A for every point

# Math functions
log_stress = np.log(stresses)
exp_decay = np.exp(-time / tau)
sqrt_strain = np.sqrt(strains)

# Comparison
yielded = stresses > 30                 # Boolean array: [False, False, False, False, True, True]

# Convert deflection to force (AFM)
k = 0.06             # Spring constant (N/m)
sensitivity = 45.0   # Deflection sensitivity (nm/V)
deflection_nm = deflection * sensitivity
force = k * deflection_nm * 1e-9 * 1e9     # Convert to nN
```

### 4. Statistics and Aggregation

```python
# Basic statistics
mean_stress = np.mean(stresses)         # 29.5 MPa
std_stress = np.std(stresses)           # Standard deviation
median_stress = np.median(stresses)     # Median (robust to outliers)
min_stress = np.min(stresses)
max_stress = np.max(stresses)

# Cumulative
force_sum = np.sum(force)              # Sum of force values; not work or energy
cumulative = np.cumsum(stresses)        # Running total

# Percentiles
q75 = np.percentile(stresses, 75)       # 75th percentile

# Axis operations (for 2D data)
column_means = data.mean(axis=0)        # Mean of each column
row_stds = data.std(axis=1)             # Std of each row
```

## Data Manipulation
### 5. Boolean Indexing (Filter Data)

![The same Boolean mask selects matching entries from the strain and stress arrays](/static/images/article-guides/comp-guide-boolean-mask-en.svg)

The same Boolean mask selects matching entries from the strain and stress arrays. In this teaching subset, strain < 0.02 retains the first three observations and excludes the entry exactly equal to 0.02.


This is probably the NumPy feature you will use most:

```python
# Find all points in the elastic region (strain < 2%)
elastic_mask = strains < 0.02
elastic_stresses = stresses[elastic_mask]

# Combined conditions
valid = (strains > 0) & (strains < 0.1) & (stresses > 0)
valid_data = stresses[valid]

# Count how many points satisfy a condition
n_yielded = np.sum(stresses > 30)       # Count of True values

# Replace values
stresses[stresses < 0] = 0              # No negative stresses
force[force > 100] = 100                # Cap at 100 nN

# Find indices
idx_max = np.argmax(stresses)           # Index of maximum
idx_where = np.where(stresses > 30)[0]  # Indices where condition is True
```

### 6. Reshaping and Combining Arrays

![Subtracting mean(axis=0) centers each column of this teaching array](/static/images/article-guides/comp-guide-broadcasting-en.svg)

Subtracting mean(axis=0) centers each column of this teaching array. NumPy broadcasts the three column means across both rows, producing zero column means without writing a loop.


```python
# Reshape
flat = data.flatten()                   # Any shape -> 1D
matrix = np.arange(12).reshape(3, 4)    # 1D -> 3x4 matrix

# Stacking
combined = np.column_stack([strains, stresses])  # Side by side
stacked = np.vstack([data1, data2])              # Row-wise append

# Transpose
transposed = matrix.T

# Broadcasting: operations between arrays of different shapes
centered = data - data.mean(axis=0)     # Subtract column means
normalized = data / data.max(axis=0)    # Normalize each column
```

### 7. Saving Results

```python
# Simple text export
np.savetxt("results.csv", combined, delimiter=",", header="strain,stress", comments="")

# Binary format (fast, compact)
np.save("processed_data.npy", data)
loaded = np.load("processed_data.npy")

# Multiple arrays
np.savez("experiment.npz", strain=strains, stress=stresses, time=time)
archive = np.load("experiment.npz")
print(archive["strain"])
```

## Putting It Together
### 8. End-to-End Example: AFM Force Curve Processing

This example processes an approach curve into force, indentation, and a local contact stiffness. The first column is assumed to be piezo displacement in nm, increasing toward the sample; match this convention to your instrument export. A force–indentation slope has units of force per length. To obtain Young's modulus, combine the curve with a calibrated probe geometry and a contact model, such as the [Hertz fit](/posts/scipy-curve-fitting/).

```python
import numpy as np

# Load
raw = np.loadtxt("force_curve_001.txt", skiprows=320)
z_piezo, deflection_V = raw[:, 0], raw[:, 1]

# Convert to force
k, sens = 0.06, 45.0
deflection_nm = deflection_V * sens
force = k * deflection_nm * 1e-9 * 1e9  # nN

# Baseline correction (pre-contact region)
baseline_idx = 100  # First 100 points are pre-contact
baseline = np.median(force[:baseline_idx])
force_corrected = force - baseline

# Find contact point
force_derivative = np.gradient(force_corrected)
noise = np.std(force_derivative[:50])
contact_idx = np.argmax(force_derivative > 5 * noise)

# Indentation: z_piezo is in nm and increases toward the sample
# Subtract the cantilever deflection change after contact
indentation = (z_piezo - z_piezo[contact_idx]) - (deflection_nm - deflection_nm[contact_idx])
contact_force = force_corrected - force_corrected[contact_idx]

# Fit a local force-indentation slope
fit_mask = (indentation > 0) & (indentation < 50)
contact_stiffness, _ = np.polyfit(indentation[fit_mask], contact_force[fit_mask], 1)

print(f"Contact stiffness: {contact_stiffness:.3f} nN/nm")
```

### 9. Common Pitfalls

| Problem | Solution |
|---------|----------|
| `np.loadtxt` fails on header lines | Use `skiprows=N` to skip header |
| Missing values cause errors | Use `np.genfromtxt` with `filling_values` |
| Wrong shape from slicing | Check with `.shape` — `data[:, 0]` is 1D, `data[:, :1]` is 2D |
| Operator `*` does element-wise | For matrix multiply, use `@` or `np.dot` |
| NaN from division by zero | Use `np.divide(a, b, where=b!=0)` |

### 10. When to Use What

| Task | NumPy Function |
|------|---------------|
| Load tabular data | `loadtxt`, `genfromtxt` |
| Linear fit | `polyfit(x, y, 1)` |
| Statistics | `mean`, `std`, `median`, `percentile` |
| Filter data | Boolean indexing `arr[mask]` |
| Find peaks | In SciPy: `scipy.signal.find_peaks` |
| FFT (frequency analysis) | `np.fft.fft` |

NumPy is the foundation. Once you are comfortable here, SciPy adds optimization, curve fitting, signal processing — all building on NumPy arrays.

## References

- Harris, C.R. et al. (2020). Array programming with NumPy. *Nature*, 585, 357-362.
- NumPy documentation: [numpy.org/doc](https://numpy.org/doc)
- VanderPlas, J. (2016). *Python Data Science Handbook*. O'Reilly Media.
