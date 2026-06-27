---
title: "Scientific Data Visualization with Python: Publication-Ready Figures"
date: "2026-06-26"
category: "python-tutorials"
tags: ["matplotlib", "visualization", "python", "publication", "figures"]
lang: "en"
slug: "scientific-visualization-python"
description: "How to create publication-quality figures with Matplotlib and Seaborn: multi-panel layouts, color schemes, high-res export, and common chart types for materials research."
---

## Why This Matters

A well-designed figure communicates your results faster than any paragraph. Yet most researchers learn Matplotlib through copy-paste and trial-and-error. This guide gives you **reusable templates** for the four most common figure types in materials science.

```python
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Global style for publication
plt.rcParams.update({
    "font.size": 10, "font.family": "sans-serif",
    "axes.labelsize": 11, "axes.titlesize": 12,
    "xtick.labelsize": 9, "ytick.labelsize": 9,
    "legend.fontsize": 9, "figure.dpi": 150,
    "savefig.dpi": 300, "savefig.bbox": "tight",
})
```

## 1. Multi-Panel Figure Template

The workhorse of any paper: 2x2 subplots comparing different conditions.

```python
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes = axes.flatten()

# Panel A: Stress-strain curves
axes[0].plot(strain, stress_control, "k-", label="Control")
axes[0].plot(strain, stress_treated, "r--", label="Treated")
axes[0].set_xlabel("Strain"); axes[0].set_ylabel("Stress (MPa)")
axes[0].legend(frameon=False)
axes[0].text(-0.1, 1.05, "A", transform=axes[0].transAxes, fontweight="bold", fontsize=12)

# Panel B: Box plot
df.boxplot(column="modulus", by="treatment", ax=axes[1])
axes[1].set_ylabel("Young's Modulus (GPa)")

# Panel C: Scatter with fit
axes[2].scatter(x, y, s=20, alpha=0.6)
axes[2].plot(x_fit, y_fit, "r-", linewidth=2)
axes[2].set_xlabel("Fiber Diameter (nm)"); axes[2].set_ylabel("Modulus (GPa)")

# Panel D: SEM image
axes[3].imshow(sem_image, cmap="gray")
axes[3].axis("off")

plt.tight_layout(pad=2)
plt.savefig("figure1.pdf", dpi=300)
```

## 2. Color Schemes

Avoid default Matplotlib colors. Use perceptually uniform or journal-specific palettes:

```python
# Option A: Seaborn colorblind-friendly
sns.set_palette("colorblind")

# Option B: Custom scientific palette
colors = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a"]

# Option C: Sequential (for heatmaps)
cmap = sns.color_palette("rocket_r", as_cmap=True)
```

## 3. Heatmaps for Matrix Data

```python
fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(correlation_matrix, cmap="RdBu_r", vmin=-1, vmax=1)
cbar = plt.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label("Pearson r")
ax.set_xticks(range(len(labels)))
ax.set_yticks(range(len(labels)))
ax.set_xticklabels(labels, rotation=45, ha="right")
ax.set_yticklabels(labels)
```

## 4. Export for Journals

```python
# Nature/Science: 89 mm (single column) or 183 mm (double)
fig.set_size_inches(3.5, 3.0)  # Single column

# Export formats
plt.savefig("figure.pdf", dpi=300, bbox_inches="tight")  # Vector, editable
plt.savefig("figure.png", dpi=600)  # Raster, high-res
plt.savefig("figure.svg")  # Fully editable in Illustrator/Inkscape
```

## 5. Quick Reference

| Chart Type | Best For | Matplotlib Function |
|-----------|----------|-------------------|
| Line plot | Stress-strain, time series | `plot()` |
| Scatter | Correlation, PCA | `scatter()` |
| Box plot | Group comparisons | `boxplot()` |
| Bar chart | Categorical means + error | `bar()` |
| Heatmap | Correlation, 2D maps | `imshow()` |
| Histogram | Distributions | `hist()` |
| Violin plot | Distribution comparison | `violinplot()` |

## 6. Tips for Reviewers

- **Never use red-green alone**: 8% of males are colorblind
- **Label panels with bold letters**: A, B, C in top-left corner
- **Report n values**: Add sample size in captions
- **Show individual points**: Don’t hide data behind bar charts
- **Use consistent fonts**: Same family, size across all panels

## References

- Rougier, N.P. et al. (2014). Ten simple rules for better figures. *PLoS Computational Biology*, 10(9), e1003833.
- Hunter, J.D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering*, 9(3), 90-95.

## References
- Rougier, N.P. et al. (2014). Ten simple rules for better figures. *PLoS Computational Biology*, 10(9), e1003833.
- Hunter, J.D. (2007). Matplotlib: A 2D graphics environment. *CSE*, 9(3), 90-95.


## Advanced Tips for Publication Figures

When preparing figures for journal submission, consider these guidelines that reviewers appreciate. Font sizes should be consistent across all panels—use the same font family and size for axis labels, tick marks, and annotations throughout the entire figure. A common mistake is having readable labels in one panel but tiny, unreadable labels in another.

Color accessibility matters. Approximately 8% of males have some form of color vision deficiency. Avoid red-green combinations as the sole differentiator between data series. Instead, combine color with different line styles (solid, dashed, dotted) or marker shapes (circles, triangles, squares) as redundant cues. The ColorBrewer palettes via Seaborn provide colorblind-safe options tested for print and digital display.

Figure legends should be positioned to minimize white space while avoiding data occlusion. The bbox_to_anchor parameter in Matplotlib allows precise placement outside the axes. For multi-panel figures, consider placing a single legend that applies to all panels rather than repeating legends in each subplot. This saves space and reduces visual clutter.

## References
- Stone, M. (2006). Choosing colors for data visualization. *Business Intelligence Network*.
- Tufte, E. (2001). *The Visual Display of Quantitative Information*. Graphics Press.
