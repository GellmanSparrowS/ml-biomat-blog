---
title: "Python Tools for Scientific Computing in Materials Research"
date: "2026-06-25"
category: "python-tutorials"
tags: ["python", "numpy", "scipy", "materials-science", "data-analysis", "visualization"]
lang: "en"
slug: "python-tools-materials-research"
description: "A curated guide to Python libraries for materials science: from data loading with ASE/pymatgen to ML with scikit-learn, plus practical AFM/SEM data analysis scripts."
---

## Why Python for Materials Science

Materials research generates data everywhere: AFM force curves, SEM images, MD trajectories, XRD patterns, mechanical testing logs. Python has become the lingua franca for processing this data—and for good reason: it's free, readable, and has an ecosystem purpose-built for scientific computing.

This post covers the essential Python stack for a materials researcher, with concrete code examples you can copy into your Jupyter notebook.

## The Core Stack

### NumPy &amp; SciPy

The foundation. If you're processing experimental data, these two cover 80% of your needs:

```python
import numpy as np
from scipy import signal, optimize, interpolate

# Load AFM force curve (typical .txt with column format)
data = np.loadtxt("force_curve.txt", skiprows=2)
z_piezo, deflection = data[:, 0], data[:, 1]

# Convert to force using spring constant and sensitivity
k = 2.8  # N/m, cantilever spring constant
sensitivity = 42.5  # nm/V
force = k * sensitivity * (deflection - np.median(deflection[:100]))

# Find adhesion peak using scipy
peaks, properties = signal.find_peaks(-force, prominence=0.5)
adhesion_force = -force[peaks[0]] if len(peaks) > 0 else 0
print(f"Adhesion force: {adhesion_force:.2f} nN")
```

### Pandas

When your data is tabular (mechanical tests with multiple samples, conditions, repeats):

```python
import pandas as pd
import seaborn as sns

df = pd.read_csv("tensile_tests.csv")
# Group by treatment, compute statistics
summary = df.groupby("treatment").agg({
    "youngs_modulus": ["mean", "std"],
    "ultimate_strength": ["mean", "std"],
    "strain_at_break": ["mean", "std"]
}).round(2)
print(summary)
```

### Matplotlib &amp; Seaborn

Publication-quality figures with minimal code:

```python
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Stress-strain with elastic fit
ax1.plot(strain, stress, 'b-', linewidth=1.5, label='Experiment')
ax1.plot(strain[:elastic_idx], elastic_fit, 'r--', label='Elastic fit')
ax1.set_xlabel("Strain"); ax1.set_ylabel("Stress (MPa)")
ax1.legend(frameon=False)

# Boxplot comparing groups
df.boxplot(column="youngs_modulus", by="treatment", ax=ax2)
ax2.set_ylabel("Young's Modulus (GPa)")

plt.tight_layout()
plt.savefig("mechanical_properties.pdf", dpi=300)
```

## Materials-Specific Libraries

### ASE (Atomic Simulation Environment)

For atomistic data—reading structure files, building supercells, computing properties:

```python
from ase.io import read, write
from ase.build import make_supercell

# Read LAMMPS data file
atoms = read("collagen_fibril.data", format="lammps-data")

# Create supercell for larger simulation
supercell = make_supercell(atoms, [[2, 0, 0], [0, 2, 0], [0, 0, 3]])

# Compute radial distribution function
from ase.geometry.analysis import Analysis
ana = Analysis(supercell)
rdf = ana.get_rdf(rmax=15.0, nbins=200)
```

### pymatgen (Python Materials Genomics)

For crystal structures, phase diagrams, and materials informatics:

```python
from pymatgen.core import Structure
from pymatgen.analysis.elasticity import ElasticTensor

# Build a collagen-like structure (simplified)
structure = Structure.from_spacegroup("P1", lattice, ["C", "N", "O"], coords)

# Compute elastic tensor from DFT-calculated stress-strain
elastic_tensor = ElasticTensor.from_stress_strain_dict(stress_strain_data)
print(f"Bulk modulus: {elastic_tensor.k_voigt:.2f} GPa")
```

## Machine Learning for Materials

### scikit-learn — Your First ML Model

Predicting mechanical properties from composition/processing features:

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler

# Features: composition, processing params
# Target: Young's modulus
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

model = RandomForestRegressor(n_estimators=100, max_depth=10)
scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
print(f"CV R²: {scores.mean():.3f} ± {scores.std():.3f}")

model.fit(X_train_scaled, y_train)
train_score = model.score(X_train_scaled, y_train)
test_score = model.score(scaler.transform(X_test), y_test)
```

### Feature Importance — What Drives Performance?

```python
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

for i in range(min(10, len(feature_names))):
    print(f"{feature_names[indices[i]]}: {importances[indices[i]]:.4f}")
```

## Image Analysis for Microscopy

Processing SEM/TEM images to quantify fiber morphology:

```python
from skimage import io, filters, measure, morphology

# Load SEM image, threshold, measure fibers
img = io.imread("sem_fiber_network.tif", as_gray=True)
thresh = filters.threshold_otsu(img)
binary = img > thresh
cleaned = morphology.remove_small_objects(binary, min_size=50)

# Label fibers and measure properties
labels = measure.label(cleaned)
props = measure.regionprops_table(labels, properties=[
    "area", "perimeter", "eccentricity", "orientation",
    "major_axis_length", "minor_axis_length"
])
df_fibers = pd.DataFrame(props)
print(f"Mean fiber diameter: {df_fibers['minor_axis_length'].mean():.1f} px")
print(f"Fiber orientation std: {np.std(df_fibers['orientation']):.2f} rad")
```

## Putting It Together: A Research Workflow

Here's how a typical multiscale project flows with Python:

1. **Load raw data** (NumPy, Pandas) — from instruments, simulations
2. **Clean &amp; preprocess** (SciPy signal processing, outlier removal)
3. **Extract features** (skimage for images, custom functions for MD data)
4. **Build models** (scikit-learn, XGBoost, or PyTorch if deep learning)
5. **Visualize &amp; export** (Matplotlib for figures, pandas to_csv for tables)
6. **Version control everything** (Git + DVC for data)

## Quick Setup

```bash
# Create a conda environment with everything you need
conda create -n matsci python=3.10 numpy scipy pandas matplotlib \
    scikit-learn seaborn jupyter ase pymatgen scikit-image -c conda-forge
conda activate matsci
```

## What's Next

In future posts, I'll cover:
- Deep learning for materials property prediction with PyTorch
- Automated AFM data processing pipelines
- Integrating MD simulation output with ML feature extraction
- Building interactive dashboards with Streamlit for lab data
