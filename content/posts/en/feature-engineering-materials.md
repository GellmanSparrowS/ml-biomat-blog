---
title: "Feature Engineering for Materials Science: From Experimental Logs to ML-Ready Data"
date: "2026-06-26"
category: "machine-learning"
tags: ["feature-engineering", "machine-learning", "materials-science", "data-preprocessing"]
lang: "en"
slug: "feature-engineering-materials-ml"
description: "How to transform scattered experimental data into structured feature matrices for ML, with Python examples."
---

## The Real Bottleneck

Most materials ML tutorials start with a clean CSV and jump straight to model fitting. In reality, your data lives in lab notebooks, instrument exports, and Excel sheets. **Feature engineering** is where 80% of the work happens.

```python
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
```

## From Raw Data to Feature Matrix

Typical raw data from a biomaterials experiment:

| Sample | Fiber_dia(nm) | Orientation(deg) | Crosslink(%) | Treatment | Youngs_mod(GPa) |
|--------|--------------|-----------------|-------------|-----------|-----------------|
| A1 | 45 | 12 | 2.5 | methanol | 2.8 |
| A2 | 52 | 22 | 1.8 | ethanol | 1.9 |

```python
df = pd.DataFrame({
    "fiber_diameter_nm": [45, 52, 48, 55, 50, 47],
    "orientation_std_deg": [12, 22, 8, 18, 15, 20],
    "crosslink_density_pct": [2.5, 1.8, 3.2, 2.0, 4.1, 1.5],
    "treatment": ["methanol", "ethanol", "methanol", "water", "methanol", "ethanol"],
    "youngs_modulus_GPa": [2.8, 1.9, 3.5, 2.3, 4.0, 1.7],
})
```

## Encoding Categorical Variables

```python
encoder = OneHotEncoder(sparse_output=False, drop="first")
treatment_encoded = encoder.fit_transform(df[["treatment"]])
treatment_cols = encoder.get_feature_names_out(["treatment"])

df_encoded = pd.concat([
    df.drop("treatment", axis=1),
    pd.DataFrame(treatment_encoded, columns=treatment_cols)
], axis=1)
```

## Domain-Driven Interaction Features

This is where materials knowledge adds value:

```python
def engineer_materials_features(df):
    df = df.copy()
    # Crosslink x fiber diameter synergy
    df["crosslink_x_diameter"] = (
        df["crosslink_density_pct"] * df["fiber_diameter_nm"]
    )
    # Orientation disorder vs diameter ratio
    df["orient_diameter_ratio"] = (
        df["orientation_std_deg"] / (df["fiber_diameter_nm"] + 1e-6)
    )
    # Log-transform skewed features
    for col in ["crosslink_density_pct", "fiber_diameter_nm"]:
        if col in df.columns:
            df[f"log_{col}"] = np.log1p(df[col])
    return df
```

## Handling Missing Values

For small datasets, avoid blind mean imputation:

```python
def smart_impute(df, group_col="treatment"):
    df = df.copy()
    numeric_cols = df.select_dtypes(include=np.number).columns
    for col in numeric_cols:
        if df[col].isna().sum() == 0: continue
        if group_col in df.columns:
            df[col] = df.groupby(group_col)[col].transform(
                lambda x: x.fillna(x.median())
            )
        df[col] = df[col].fillna(df[col].median())
    return df
```

## Feature Selection for Small Datasets

With <100 samples, avoid automated selection:

1. **Correlation analysis**: drop |r| > 0.95
2. **Variance threshold**: drop near-constant features
3. **Domain curation**: only physically justified features

```python
corr_matrix = df_feat[feature_cols].corr().abs()
upper_tri = corr_matrix.where(
    np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
)
to_drop = [col for col in upper_tri.columns 
           if any(upper_tri[col] > 0.95)]
```

## Checklist

- All features numeric
- No target leakage
- Missing values handled
- Categoricals encoded
- Interaction features have physical justification

## References

- Kuhn, M. & Johnson, K. (2019). *Feature Engineering and Selection*. CRC Press.
- Ramprasad, R. et al. (2017). Machine learning in materials informatics. *npj Computational Materials*, 3, 54.


## Advanced Feature Engineering Strategies

Domain-specific feature engineering can dramatically improve model performance with limited data. For fiber biomaterials, consider these physics-informed features that capture known structure-property relationships.

The persistence length of semiflexible fibers can be estimated from orientation correlation functions and used as a feature that captures the intrinsic flexibility of the fiber material independent of network architecture. Similarly, the excluded volume interaction parameter derived from the second virial coefficient provides a measure of fiber-fiber interactions that influences network mechanics.

For data with strong hierarchical structure (fiber -> bundle -> network), hierarchical features that aggregate properties at each level can help models capture multi-scale effects. Calculate fiber-level features first, then aggregate to bundle-level means and variances, and finally to network-level descriptors.

When experimental measurements are limited, simulation-informed features can bridge the gap. Run coarse-grained simulations across a parameter space, extract features from the simulation outputs, and use these as supplementary features alongside experimental data. The simulations capture the underlying physics while the experimental data anchors the predictions to reality.

## References
- Ramprasad, R. et al. (2017). Machine learning in materials informatics: Recent applications and prospects. *npj Computational Materials*, 3, 54.
