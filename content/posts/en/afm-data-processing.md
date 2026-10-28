---
title: "Practical AFM Force Curve Analysis with Python"
date: "2026-06-26"
updated: "2026-10-28"
category: "wet-lab-data"
tags: ["AFM", "force-spectroscopy", "python", "numpy", "data-processing", "biomaterials"]
lang: "en"
slug: "afm-force-curve-python"
description: "Convert AFM deflection into force, correct the baseline and identify contact before fitting indentation data. Calibration geometry, analytic Hertz curves and Python functions connect measured channels to adhesion and elastic modulus with explicit units."
---

## From AFM Signals to Mechanical Properties {#why-this-guide-exists}

If you work with AFM force spectroscopy on soft biomaterials (collagen fibers, silk, hydrogels, cells), you have probably faced the same frustration: your instrument exports a pile of `.txt` or `.csv` files, and you spend hours manually processing them in proprietary software or Excel.

This guide gives you **a complete, copy-paste-ready Python pipeline** that handles everything from raw data loading to Young's modulus extraction. No commercial software required. Just `numpy`, `scipy`, and `matplotlib`.

## The Core Analysis Pipeline
### 1. Understanding AFM Force Curve Data

A typical AFM force curve records **cantilever deflection** (in volts or nanometers) as the piezo moves the tip toward and away from the sample:

| Segment | What happens | What you extract |
|---------|-------------|-----------------|
| Approach | Tip approaches surface | Contact point, sample stiffness |
| Contact | Tip presses into sample | Elastic modulus (via fitting) |
| Retract | Tip pulls away | Adhesion force, unbinding events |

![Schematic AFM force-distance curve showing baseline, contact point, approach, retract, and adhesion pull-off](/static/images/posts/afm-force-curve-python/force-curve-en.webp)

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, optimize
```

### 2. Loading Typical AFM Data Files

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

#### Handling Bruker Headers

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

### 3. Converting Deflection to Force

```python
def deflection_to_force(deflection_V, spring_constant, sensitivity_nm_per_V):
    deflection_nm = deflection_V * sensitivity_nm_per_V
    force_N = spring_constant * deflection_nm * 1e-9
    return force_N * 1e9  # nN

k = 0.06        # N/m (Bruker MLCT)
sensitivity = 45.0  # nm/V
force = deflection_to_force(deflection, k, sensitivity)
```

![Separate cantilever bending from indentation](/static/images/article-guides/mech-afm-calibration-en.svg)

After calibration, deflection d = SV gives force F = kd. With piezo advance defined positive into contact and offsets removed, indentation is δ = Δz − d. This geometry prevents piezo motion from being mistaken for sample indentation.

### 4. Baseline Correction

```python
def baseline_correct(z_piezo, force, contact_idx):
    baseline_region = slice(0, contact_idx)
    coeffs = np.polyfit(z_piezo[baseline_region], force[baseline_region], 1)
    baseline = np.polyval(coeffs, z_piezo)
    return force - baseline
```

### 5. Finding the Contact Point

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
    raise ValueError("No contact point found; review the approach segment")
```

### 6. Extracting Adhesion Force

```python
def extract_adhesion(z_piezo, force, contact_idx):
    retract_region = force[contact_idx:]
    adhesion_idx = np.argmin(retract_region)
    adhesion_force = retract_region[adhesion_idx]
    return adhesion_force if adhesion_force < 0 else 0.0
```

### 7. Hertz Model Fitting for Young's Modulus

For a spherical indenter on a flat elastic half-space:

F = (4/3) E* sqrt(R) delta^(3/2)

where E* = E / (1 - nu^2).

The fitting function uses an approach segment with z in nm and force in nN, and returns E in Pa. Set the measured spring constant in N/m and tip radius explicitly. The default direction assumes z decreases during approach; use +1 when it increases. Choose indentation small compared with the spherical tip radius, and a sample thickness large compared with the contact radius a = sqrt(Rδ). The parameter values below match the teaching curves.

```python
def hertz_sphere(indentation, E_star, R):
    """SI units: indentation and R in m, E_star in Pa, force in N."""
    return (4/3) * E_star * np.sqrt(R) * np.power(
        np.maximum(indentation, 0), 1.5
    )

def fit_youngs_modulus(z_piezo, force, contact_idx,
                        tip_radius_nm=5000.0, poisson=0.5,
                        fit_range_nm=200.0, spring_constant=0.06,
                        approach_direction=-1):
    """Fit an approach branch: z in nm, force in nN; return E and its fit error in Pa."""
    if spring_constant <= 0 or tip_radius_nm <= 0:
        raise ValueError("Spring constant and tip radius must be positive")
    if approach_direction not in (-1, 1):
        raise ValueError("approach_direction must be -1 or +1")
    z_nm = np.asarray(z_piezo, dtype=float)
    force_nN = np.asarray(force, dtype=float)
    contact_force_nN = force_nN - force_nN[contact_idx]
    advance_nm = approach_direction * (z_nm - z_nm[contact_idx])
    deflection_nm = contact_force_nN / spring_constant
    indentation_nm = advance_nm - deflection_nm
    fit_mask = (
        (np.arange(len(z_nm)) >= contact_idx)
        & (indentation_nm > 0) & (indentation_nm < fit_range_nm)
        & (contact_force_nN > 0)
        & np.isfinite(indentation_nm) & np.isfinite(contact_force_nN)
    )
    if np.count_nonzero(fit_mask) < 50:
        return np.nan, np.nan
    indentation_m = indentation_nm[fit_mask] * 1e-9
    radius_m = tip_radius_nm * 1e-9
    force_fit_nN = contact_force_nN[fit_mask]

    def model(delta_m, E_star_Pa):
        return hertz_sphere(delta_m, E_star_Pa, radius_m) * 1e9

    popt, pcov = optimize.curve_fit(
        model, indentation_m, force_fit_nN,
        p0=[1e4], bounds=(1, 1e9)
    )
    E = popt[0] * (1 - poisson**2)
    E_std = np.sqrt(pcov[0, 0]) * (1 - poisson**2)
    return E, E_std
```

![Hertz curves from stated model parameters](/static/images/article-guides/mech-afm-hertz-en.svg)

Hertz curves calculated with R = 5 μm, ν = 0.5 and E = 10 or 30 kPa show how modulus changes force at the same indentation. The model assumes a rigid spherical tip, a homogeneous elastic half-space and negligible adhesion; the curves are calculated analytic examples.

## Scaling and Advanced Topics
### 8. Batch Processing

```python
import glob
from pathlib import Path

def batch_process_curves(data_dir, k=0.06, sensitivity=45.0, approach_direction=-1):
    results = []
    for filepath in sorted(glob.glob(f"{data_dir}/*.txt")):
        try:
            z, deflection = load_afm_curve(filepath, skip_rows=320)
            force = deflection_to_force(deflection, k, sensitivity)
            turn_idx = int(np.argmax(approach_direction * z))
            z_approach = z[:turn_idx + 1]
            cidx = find_contact_point(z_approach, force[:turn_idx + 1])
            force_corr = baseline_correct(z, force, cidx)
            adhesion = (extract_adhesion(z, force_corr, turn_idx)
                        if turn_idx + 1 < len(z) else np.nan)
            E, _ = fit_youngs_modulus(
                z_approach, force_corr[:turn_idx + 1], cidx,
                spring_constant=k, approach_direction=approach_direction
            )
            results.append({"file": Path(filepath).name,
                "adhesion_nN": adhesion, "E_Pa": E})
        except Exception as e:
            print(f"Failed: {filepath}: {e}")
    return results
```

### 9. Common Pitfalls

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Contact point too early | Baseline noise | Increase `threshold_factor` |
| Negative modulus | Wrong direction | Check z_piezo sign convention |
| Substrate effect | Too deep indentation | `fit_range_nm` < 10% of thickness |
| Zero adhesion | No retract data | Enable retract in AFM method |

### 10. Alternative Models

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
- JPK Instruments. *A Practical Guide to AFM Force Spectroscopy*.
