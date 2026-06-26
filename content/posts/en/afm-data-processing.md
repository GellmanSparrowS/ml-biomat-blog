---
title: "Practical AFM Force Curve Analysis with Python: From Raw Data to Mechanical Properties"
date: "2026-06-26"
category: "wet-lab-data"
tags: ["AFM", "force-spectroscopy", "python", "numpy", "data-processing", "biomaterials"]
lang: "en"
slug: "afm-force-curve-python"
description: "A step-by-step guide to processing AFM force curves in Python: baseline correction, contact point detection, adhesion force, and Young's modulus fitting with Hertz/Sneddon models."
---

## Why This Guide Exists

If you work with AFM force spectroscopy on soft biomaterials (collagen fibers, silk, hydrogels, cells), you have probably faced the same frustration: your instrument exports a pile of `.txt` or `.csv` files, and you spend hours manually processing them in proprietary software or Excel.

This guide gives you **a complete, copy-paste-ready Python pipeline** that handles everything from raw data loading to Young's modulus extraction. No commercial software required. Just `numpy`, `scipy`, and `matplotlib`.

## 1. Understanding AFM Force Curve Data

A typical AFM force curve records **cantilever deflection** (in volts or nanometers) as the piezo moves the tip toward and away from the sample:

| Segment | What happens | What you extract |
|---------|-------------|-----------------|
| Approach | Tip approaches surface | Contact point, sample stiffness |
| Contact | Tip presses into sample | Elastic modulus (via fitting) |
| Retract | Tip pulls away | Adhesion force, unbinding events |

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, optimize
```

## 2. Loading Typical AFM Data Files

Most AFM instruments export tabular data. Common formats:

- **Bruker/Veeco**: `.txt` with header lines starting with `\`
- **JPK/Nanowizard**: `.txt` or `.jpk-force` with metadata header
- **Asylum/AR**: `.txt` or `.ibw` (use `igorpro` package)
- **Generic**: `.csv` with columns: Z_piezo, Deflection

```python
def load_afm_curve(filepath, skip_rows=0):
    data = np.loadtxt(filepath, skiprows=skip_rows)
    return data[:, 0], data[:, 1]

# Example: Bruker force curve
z_piezo, deflection = load_afm_curve("force_curve_001.txt", skip_rows=320)
```

### Handling Bruker Headers

```python
def load_bruker_curve(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()
    skip = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("\\*") or "Ciao" in line:
            skip = i + 1
    data = np.loadtxt(filepath, skiprows=skip)
    return data[:, 0], data[:, 1]
```

## 3. Converting Deflection to Force

```python
def deflection_to_force(deflection_V, spring_constant, sensitivity_nm_per_V):
    deflection_nm = deflection_V * sensitivity_nm_per_V
    force_N = spring_constant * deflection_nm * 1e-9
    return force_N * 1e9  # nN

k = 0.06        # N/m (Bruker MLCT)
sensitivity = 45.0  # nm/V
force = deflection_to_force(deflection, k, sensitivity)
```

## 4. Baseline Correction

```python
def baseline_correct(z_piezo, force, contact_idx):
    baseline_region = slice(0, contact_idx)
    coeffs = np.polyfit(z_piezo[baseline_region], force[baseline_region], 1)
    baseline = np.polyval(coeffs, z_piezo)
    return force - baseline
```

## 5. Finding the Contact Point

```python
def find_contact_point(z_piezo, force, window=50, threshold_factor=5):
    force_smooth = signal.savgol_filter(force, window_length=21, polyorder=3)
    dz = np.gradient(z_piezo)
    df = np.gradient(force_smooth)
    derivative = df / dz
    noise_region = slice(0, len(force) // 5)
    noise_std = np.std(derivative[noise_region])
    threshold = threshold_factor * noise_std
    above_threshold = np.abs(derivative) > threshold
    for i in range(len(above_threshold) - window):
        if np.all(above_threshold[i:i + window]):
            return i + window // 2
    return len(force) // 2
```

## 6. Extracting Adhesion Force

```python
def extract_adhesion(z_piezo, force, contact_idx):
    retract_region = force[contact_idx:]
    adhesion_idx = np.argmin(retract_region)
    adhesion_force = retract_region[adhesion_idx]
    return adhesion_force if adhesion_force < 0 else 0.0
```

## 7. Hertz Model Fitting for Young's Modulus

For a spherical indenter on a flat elastic half-space:

F = (4/3) E* sqrt(R) delta^(3/2)

where E* = E / (1 - nu^2).

```python
def hertz_sphere(indentation, E_star, R):
    return (4/3) * E_star * np.sqrt(R) * np.power(np.maximum(indentation, 0), 1.5)

def fit_youngs_modulus(z_piezo, force, contact_idx, tip_radius_nm=20.0,
                        poisson=0.5, fit_range_nm=50.0):
    indent = z_piezo[contact_idx] - z_piezo
    contact_force = force - force[contact_idx]
    fit_mask = (indent > 0) & (indent < fit_range_nm) & (contact_force > 0)
    indent_fit = indent[fit_mask]
    force_fit = contact_force[fit_mask]
    if len(indent_fit) < 50:
        return np.nan, np.nan
    def model(delta, E_star):
        return hertz_sphere(delta, E_star, tip_radius_nm)
    popt, pcov = optimize.curve_fit(model, indent_fit, force_fit,
        p0=[1000], bounds=(1, 1e9))
    E_star = popt[0]
    E = E_star * (1 - poisson**2)
    E_std = np.sqrt(pcov[0, 0]) * (1 - poisson**2)
    return E, E_std
```

## 8. Batch Processing

```python
import glob
from pathlib import Path

def batch_process_curves(data_dir, k=0.06, sensitivity=45.0):
    results = []
    for filepath in sorted(glob.glob(f"{data_dir}/*.txt")):
        try:
            z, deflection = load_afm_curve(filepath, skip_rows=320)
            force = deflection_to_force(deflection, k, sensitivity)
            cidx = find_contact_point(z, force)
            force_corr = baseline_correct(z, force, cidx)
            adhesion = extract_adhesion(z, force_corr, cidx)
            E, _ = fit_youngs_modulus(z, force_corr, cidx)
            results.append({"file": Path(filepath).name,
                "adhesion_nN": adhesion, "E_Pa": E})
        except Exception as e:
            print(f"Failed: {filepath}: {e}")
    return results
```

## 9. Common Pitfalls

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Contact point too early | Baseline noise | Increase `threshold_factor` |
| Negative modulus | Wrong direction | Check z_piezo sign convention |
| Substrate effect | Too deep indentation | `fit_range_nm` < 10% of thickness |
| Zero adhesion | No retract data | Enable retract in AFM method |

## 10. Alternative Models

- **Sneddon model**: for conical indenters: F = (2/pi) E* tan(alpha) delta^2
- **JKR model**: includes adhesion in contact mechanics
- **Ting's model**: for viscoelastic relaxation

```python
def sneddon_cone(indentation, E_star, alpha_deg=18):
    alpha = np.radians(alpha_deg)
    return (2 / np.pi) * E_star * np.tan(alpha) * np.power(indentation, 2)
```

## References

- Cappella, B. & Dietler, G. (1999). Force-distance curves by AFM. *Surface Science Reports*, 34(1-3), 1-104.
- Hertz, H. (1882). On the contact of elastic solids. *J. Reine Angew. Math.*, 92, 156-171.
- Sneddon, I.N. (1965). The relation between load and penetration. *Int. J. Eng. Sci.*, 3(1), 47-57.