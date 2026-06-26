---
title: "Setting Up Your Python Environment for Scientific Computing: A Step-by-Step Guide"
date: "2026-06-27"
category: "python-tutorials"
tags: ["python", "conda", "jupyter", "venv", "scientific-computing", "setup"]
lang: "en"
slug: "python-env-setup"
description: "Complete guide to setting up a Python environment for materials and biology research: Miniconda, Jupyter, VS Code, package management, and troubleshooting common issues."
---

## Who Is This For?

You are a graduate student in biology, chemistry, or materials science. You have heard that Python can help with your data, but you have never set up a programming environment. This guide walks you through every step—no prior experience assumed.

By the end, you will have a working Python setup with Jupyter notebooks, essential scientific packages, and VS Code as your editor.

## Step 1: Install Miniconda

**Why Miniconda instead of Anaconda?** Miniconda is lightweight (~50 MB vs ~500 MB), installs faster, and gives you full control over which packages you need.

1. Go to [docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
2. Download the installer for your OS (Windows: `.exe`, macOS: `.pkg`, Linux: `.sh`)
3. Run the installer. **Important: check "Add Miniconda to PATH"** on Windows
4. Verify installation:

```bash
conda --version
# Expected: conda 24.x.x
```

## Step 2: Create Your First Environment

Environments isolate project dependencies. Think of them as separate toolboxes—one for AFM analysis, one for MD simulations, one for ML projects.

```bash
# Create an environment with Python 3.10 (most packages support this)
conda create -n matsci python=3.10 -y

# Activate it
conda activate matsci

# Your prompt should now show (matsci)
```

## Step 3: Install Essential Packages

For materials/biomaterials research, here are the packages you need right away:

```bash
# Core scientific stack
conda install numpy scipy pandas matplotlib jupyter -y

# Additional useful libraries
conda install -c conda-forge seaborn scikit-learn scikit-image -y

# For atomic/molecular simulations (install as needed)
# conda install -c conda-forge ase pymatgen mdanalysis -y
```

Verify everything works:

```python
# test_env.py
import numpy as np
import scipy
import pandas as pd
import matplotlib.pyplot as plt
import sklearn

print(f"NumPy: {np.__version__}")
print(f"SciPy: {scipy.__version__}")
print(f"Pandas: {pd.__version__}")
print(f"scikit-learn: {sklearn.__version__}")
print("All packages OK!")
```

## Step 4: Set Up Jupyter Notebook

Jupyter is the interactive coding environment most scientists use for exploration:

```bash
# Start Jupyter in your project folder
cd path/to/your/project
jupyter notebook

# Or use JupyterLab (more modern interface)
jupyter lab
```

**Pro tip:** Create a shortcut command for quick launch. On Windows, create `jupyter_lab.bat`:

```batch
@echo off
call conda activate matsci
jupyter lab
```

## Step 5: VS Code for Serious Development

When notebooks get too messy (and they will), switch to VS Code:

1. Download from [code.visualstudio.com](https://code.visualstudio.com)
2. Install the **Python extension** (Microsoft)
3. Open your project folder: `File > Open Folder`
4. Select your conda environment: `Ctrl+Shift+P` > "Python: Select Interpreter" > choose `matsci`

Essential VS Code extensions for scientists:
- **Python** (Microsoft): IntelliSense, debugging
- **Jupyter** (Microsoft): Notebook support inside VS Code
- **Rainbow CSV**: Color-coded CSV files
- **GitLens**: Git integration

## Step 6: Package Management Reference

```bash
# List installed packages
conda list

# Install a specific version
conda install numpy=1.24.3

# Install from conda-forge (community-maintained channel)
conda install -c conda-forge package_name

# Use pip when conda does not have the package
pip install package_name

# Export your environment (for sharing/reproducibility)
conda env export > environment.yml

# Recreate from file
conda env create -f environment.yml
```

## Step 7: Common Problems and Solutions

| Problem | Solution |
|---------|----------|
| `conda not recognized` | Restart terminal or reinstall with "Add to PATH" checked |
| Package install hangs | Use `conda install -c conda-forge` instead of defaults |
| `DLL load failed` on Windows | Install [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe) |
| Jupyter kernel not found | `python -m ipykernel install --user --name matsci` |
| Conda slow on Windows | Use `mamba` instead: `conda install mamba -c conda-forge` then `mamba install ...` |

## Step 8: Quick Start Template

Save this as `start_project.bat` (Windows) or `start_project.sh` (macOS/Linux):

```bash
# Windows: start_project.bat
conda activate matsci
jupyter lab
```

Double-click to start working. That is it—you are ready to code.

## References

- Conda documentation: [docs.conda.io](https://docs.conda.io)
- Jupyter documentation: [docs.jupyter.org](https://docs.jupyter.org)
- VS Code Python setup: [code.visualstudio.com/docs/python/python-tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- Scientific Python ecosystem: [scientific-python.org](https://scientific-python.org)
