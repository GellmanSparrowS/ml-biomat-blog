---
title: "Data Processing with Pandas: From Lab Measurements to Analysis-Ready Data"
date: "2026-06-26"
category: "python-tutorials"
tags: ["pandas", "python", "data-processing", "experimental-data"]
lang: "en"
slug: "pandas-materials-data"
description: "A practical guide to using Pandas for materials research data: loading multi-source files, cleaning, group statistics, and visualization."
---

## Why Pandas

Most researchers manually merge, filter, and plot experimental data in Excel -- error-prone and time-consuming. Pandas handles all of this with a few lines of code.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

## Reading Experimental Data

```python
df = pd.read_excel("mechanical_tests.xlsx", sheet_name="Sheet1")
df = pd.read_csv("force_curves.csv")

# Merge multiple files
import glob
files = glob.glob("data/*.csv")
dfs = [pd.read_csv(f) for f in files]
df_all = pd.concat(dfs, ignore_index=True)
```

## Data Cleaning

```python
df = df.dropna(how="all")  # Remove fully empty rows
df = df.rename(columns={"fiber_diameter_nm": "diameter", "youngs_modulus_GPa": "modulus"})

# Remove outliers (3-sigma)
for col in ["modulus", "diameter"]:
    mean, std = df[col].mean(), df[col].std()
    df = df[(df[col] > mean - 3*std) & (df[col] < mean + 3*std)]
```

## Group Statistics

```python
summary = df.groupby("treatment").agg({
    "modulus": ["mean", "std", "count"],
    "diameter": ["mean", "std"],
}).round(2)
```

## Visualization

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
df.boxplot(column="modulus", by="treatment", ax=axes[0,0])
axes[0,1].scatter(df["diameter"], df["modulus"], alpha=0.6)
corr = df.select_dtypes(include=np.number).corr()
axes[1,0].imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
plt.tight_layout()
```

## Export Results

```python
summary.to_csv("mechanical_summary.csv")
df.to_csv("cleaned_data.csv", index=False)
with pd.ExcelWriter("results.xlsx") as writer:
    df.to_excel(writer, sheet_name="Raw Data")
    summary.to_excel(writer, sheet_name="Summary")
```

## Quick Troubleshooting

| Problem | Fix |
|---------|-----|
| Encoding error | `pd.read_csv("file.csv", encoding="utf-8")` or `"gbk"` |
| Large file slow | Specify `dtype` or use `chunksize` |
| Date format wrong | `pd.to_datetime(df["date"], format="%Y-%m-%d")` |
