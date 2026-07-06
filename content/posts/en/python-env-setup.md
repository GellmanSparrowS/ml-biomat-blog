---
title: "A Complete Guide to Setting Up a Python Scientific Computing Environment: From Zero to Productivity"
date: "2026-07-06"
category: "python-tutorials"
tags: ["python", "conda", "jupyter", "mamba", "scientific-computing", "environment-setup"]
lang: "en"
slug: "python-env-setup"
description: "A comprehensive three-platform guide covering virtual environments, Conda and Mamba, JupyterLab, and VS Code integration for materials science and biology graduate students."
---
## 1. Why Environment Management Matters — The Version Conflict Problem

Many graduate students have a frustrating first encounter with Python. You find a script online for processing AFM data or XRD diffraction patterns, install the required libraries following a tutorial, and it works. A few weeks later, your supervisor sends a machine learning analysis script. After installing its dependencies, the original script suddenly crashes with a version incompatibility error — and you haven't changed a thing. This experience is almost universal among graduate students, and the root cause is straightforward: when every package is installed into the same global Python environment, conflicting version requirements between projects inevitably cause breakage.

The problem is best illustrated with a laboratory analogy. Imagine sharing a single incubator between two bacterial strains with optimal growth temperatures of 30°C and 37°C — you cannot satisfy both simultaneously without compromising one. Python package conflicts follow the same logic. An older BioPython script may depend on NumPy 1.x interfaces, while a new version of TensorFlow requires NumPy 2.x features; OVITO's Python bindings may require one version of a VTK library, while your finite-element post-processing script needs another. If both tools share a single environment, installing either one tends to break the other. For a graduate student simultaneously working on materials characterization analysis, molecular dynamics simulations, and machine learning predictions, such conflicts are not merely possible but nearly inevitable.

The solution is a **virtual environment** — an isolated Python runtime space with its own independent Python interpreter version and complete package collection, entirely separate from other environments and from the system's default Python. Think of it as a dedicated cleanroom in a laboratory: each cleanroom maintains its own temperature, humidity, and contamination controls; different experiments proceed in their respective spaces without cross-contamination. Creating a virtual environment is equivalent to opening a new cleanroom; deleting an environment dismantles it without affecting anything else.

**Conda** is the de facto standard tool for managing virtual environments in the Python scientific computing community. Compared to Python's built-in `venv` or `virtualenv`, Conda's core advantage is that it manages not only Python packages but also the Python interpreter itself and non-Python binary dependencies — including C/C++ shared libraries, BLAS/LAPACK linear algebra libraries (the actual performance bottleneck of NumPy and SciPy operations), and CUDA toolchains for GPU computing. For research scenarios involving finite-element solvers such as FEniCSx, molecular dynamics interfaces such as LAMMPS's Python bindings, or biological sequence analysis tools, Conda's precise control at this binary dependency layer is something the pip+venv combination simply cannot replicate.

Mastering Conda virtual environment management is the key step between "being able to run Python scripts" and "being able to reproducibly generate scientific computing results" — and it represents the basic professional standard expected when sharing code with supervisors or collaborators.

---

## 2. Anaconda or Miniconda — Choose What Fits, Don't Overthink It

Before installing Conda, it is important to clarify a common source of confusion: Anaconda and Miniconda are two different installer packages, but they install the same core `conda` tool and are functionally identical in terms of environment management. The difference is only in how many packages come pre-installed. Every command in the rest of this guide works identically regardless of which one you choose.

**Anaconda** is the all-in-one distribution. After installation, you have `conda` itself, Python, over two hundred and fifty pre-installed scientific computing packages (NumPy, SciPy, Pandas, Matplotlib, Jupyter, scikit-learn, and many more), and a graphical management interface called Anaconda Navigator. The installer is roughly 800 MB to 1 GB, expanding to 3–5 GB on disk. The advantage is true out-of-the-box readiness: after installation, the packages required for most scientific computing tasks are already present; launching JupyterLab and starting data analysis requires no further installation commands. For graduate students whose first priority is "start processing experimental data as soon as possible" rather than "deeply understand environment management," Anaconda is the more appropriate entry point.

**Miniconda** is the stripped-down version, with an installer of only 60–100 MB. After installation, you have only `conda`, Python, and a few basic tools; no scientific libraries are pre-installed. Everything must be installed manually on demand. The initial configuration requires a few extra installation commands, which imposes a modest learning curve, but the environment is under your complete control from the start — you know exactly what is installed, with no unused packages silently consuming disk space.

How to choose? **Miniconda is generally recommended** — building from scratch gives you full visibility into what is installed, occupies only a few hundred MB, and deploys effortlessly on remote servers. If you have never used a command line and have ample disk space, Anaconda's out-of-the-box experience is also solid. Both can be swapped later, so there is no wrong choice.

One additional option worth introducing: **Mamba**. Mamba is not a standalone installer but a high-performance drop-in replacement for Conda that can be installed on top of any existing Conda setup. It rewrites Conda's dependency solver in C++, making it several times faster at resolving complex dependency trees. If you have ever installed PyTorch with CUDA support and watched `conda install` freeze on "Solving environment..." for several minutes, that is precisely the scenario where Mamba shines. Install it with `conda install -n base -c conda-forge mamba -y`; afterward, any `conda install` or `conda create` command can be replaced with `mamba install` or `mamba create`, with all other syntax remaining identical.

---

## 3. Platform-Specific Installation: Windows, macOS, and Linux

Installation procedures differ meaningfully across operating systems. The most critical distinction is the Apple Silicon versus Intel distinction on macOS. The following covers each platform in full; follow the section that corresponds to your system.

**Windows**

Download the installer (.exe) from the Anaconda website (`https://www.anaconda.com/download`) or, for Miniconda, from `https://docs.conda.io/en/latest/miniconda.html`. Double-click the installer. At the "Installation Type" step, select "Just Me" (no administrator privileges required). At the "Advanced Installation Options" page, **check the box labeled "Add Anaconda3/Miniconda3 to my PATH environment variable"** — without this, the system will not locate the `conda` command and none of the subsequent steps will work.

After installation, do not use the ordinary Command Prompt (CMD) or PowerShell. Instead, open **Anaconda Prompt** from the Start menu and use it as your command-line interface for all `conda` operations. Ordinary CMD and PowerShell may fail to recognize conda's environment activation commands due to default security policies. Verify the installation in Anaconda Prompt:

```bash
conda --version
python --version
```

Both commands returning version numbers (e.g., `conda 24.7.1`, `Python 3.12.4`) confirms a successful installation.

**macOS (Critical: M-Series vs. Intel)**

Macs released after late 2020 mostly use Apple Silicon chips (M1/M2/M3/M4 series), which differ fundamentally in instruction-set architecture from Intel chips (ARM versus x86-64). You **must select the correct architecture version** when downloading — installing the wrong one means all Apple Silicon native performance optimizations (NumPy's Apple Accelerate framework integration, PyTorch's MPS backend, and so on) will be unavailable, with potential performance losses of several times.

To check your chip: click the Apple logo in the top-left corner → About This Mac. If the "Chip" field shows "Apple M1/M2/M3/M4," download the **arm64** version; if it shows "Intel Core," download **x86_64**. Install from the Terminal using the shell script, shown here for Apple Silicon Miniconda:

```bash
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
bash Miniconda3-latest-MacOSX-arm64.sh
```

When asked "Do you wish the installer to initialize Miniconda3 by running conda init?" type `yes`. This modifies `~/.zshrc` (macOS defaults to zsh). After installation, reload the shell:

```bash
source ~/.zshrc
conda --version
```

**Linux (Local and HPC Clusters)**

The procedure mirrors macOS command-line installation:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh    # type "yes" when prompted for conda init
source ~/.bashrc
conda --version
```

If you work on a university or institute HPC cluster, first check whether Conda is already available via the module system: run `module avail anaconda` or `module avail miniconda`. If a module exists, load it with `module load anaconda3` rather than installing a separate copy. If no module is available, install Miniconda into your home directory (set the installation path to `$HOME/miniconda3`) — no root privileges are needed, and other users are unaffected.

---

## 4. Creating and Managing Virtual Environments — Core Isolation Operations

With the motivation for virtual environments established, the actual creation and management commands are quite intuitive. This section covers the full lifecycle of an environment, including the critically important reproducibility workflow.

Creating a new environment always requires an explicit Python version:

```bash
conda create -n matsci python=3.11 -y
```

The `-n matsci` argument specifies the environment name; use descriptive names tied to the project (`afm_analysis`, `ml_fatigue`, `protein_dock`) rather than generic names like `myenv`. Different environments can use different Python versions with no conflict between them. The `-y` flag auto-confirms all prompts.

Activating the environment is a mandatory step before starting work:

```bash
conda activate matsci
```

Once activated, the terminal prompt will show `(matsci)` at the front — the visual confirmation that the environment is active. All packages installed and all Python scripts run in that terminal window will use the isolated `matsci` space. To exit, run `conda deactivate`.

Listing all existing environments (the currently active one is marked with `*`):

```bash
conda env list
```

Listing all packages installed in the current environment:

```bash
conda list
```

**Environment reproducibility** is one of the most important practices in computational research. When your materials characterization analysis or fatigue-life prediction code reaches a stage worth recording in a paper's supplementary section, export the complete environment state:

```bash
conda env export > environment.yml
```

The generated `environment.yml` file records every installed package and its exact version number. A collaborator or a reviewer requesting code validation can reconstruct the identical environment with a single command:

```bash
conda env create -f environment.yml
```

This workflow ensures that your code produces the same output on your supervisor's machine, during peer review, and when you return to the project years later. It is the technical foundation of reproducibility in modern computational science.

| Operation | Command |
|---|---|
| Create new environment | `conda create -n name python=3.11 -y` |
| Activate environment | `conda activate name` |
| Deactivate environment | `conda deactivate` |
| List all environments | `conda env list` |
| Delete an environment | `conda env remove -n name` |
| Export environment config | `conda env export > environment.yml` |
| Rebuild from config file | `conda env create -f environment.yml` |
| List installed packages | `conda list` |
| Update a package | `conda update package-name` |

---

## 5. Installing Core Scientific Computing Packages — Understanding What Each Tool Does

With the target environment activated, you can install the packages needed for scientific computing. The following describes each major package from a functional perspective — understanding what each tool is for helps you reach for the right one when a new analysis task arises, rather than blindly installing everything in sight.

Install the base scientific computing suite:

```bash
conda install numpy scipy pandas matplotlib -y
conda install -c conda-forge jupyterlab seaborn scikit-learn scikit-image ipykernel -y
```

**NumPy** is the numerical computing foundation of the entire Python scientific ecosystem. It provides multidimensional array (ndarray) data structures and vectorized mathematical functions, powered by highly optimized BLAS/LAPACK linear algebra libraries at the C level. Whether you are performing matrix operations on stress-strain data, processing voxel arrays from CT scans, or transforming protein structure coordinates, NumPy is almost always the first tool you will use. A matrix multiplication that would require nested Python loops is expressed as `A @ B` in NumPy and runs orders of magnitude faster.

**SciPy** builds on NumPy to provide higher-level scientific computing algorithms. `scipy.signal` handles signal processing (filtering fatigue test load spectra, computing frequency spectra of electrophysiological signals); `scipy.stats` covers statistical tests (assessing whether the mean values of two groups of material test data differ significantly); `scipy.ndimage` provides image processing operations (morphological operations on CT images for trabecular bone segmentation); `scipy.optimize` supports curve fitting (fitting the Paris crack growth law `da/dN = C(ΔK)^m` to extract parameters C and m); and `scipy.sparse` provides sparse matrix support (efficient storage and solution of finite-element stiffness matrices).

**Pandas** is the standard tool for tabular data. For organizing materials composition-property databases, managing batch biological sample data across multiple experimental conditions, or merging and cleaning multi-channel sensor time series, Pandas is nearly indispensable. Its core data structure, the DataFrame, can be thought of as a "labeled NumPy matrix" that supports SQL-style group-and-aggregate operations, time series resampling, and flexible data alignment.

**Matplotlib** and **Seaborn** are the primary visualization tools. Matplotlib provides fine-grained control over every visual element (axis ranges, font sizes, line styles, legend positions) to meet the stringent figure formatting requirements of journal submissions. Seaborn builds on Matplotlib to provide more polished statistical charts (box plots, heatmaps, pair plot matrices) for rapid exploratory visualization. XRD diffraction patterns, S-N fatigue life curves, and statistical box plots of cell viability can all be produced at publication quality with these two libraries.

**scikit-learn** is the standard library for classical machine learning, covering random forests, support vector machines, principal component analysis (PCA), Lasso/Ridge regression, k-nearest neighbors, and other algorithms commonly used in scientific data analysis. The deep learning chapter of this series emphasizes that not every problem requires deep learning — scikit-learn is the preferred tool when sample sizes are limited and features have well-defined physical meaning.

For research requiring deep learning (image classification, sequence prediction, physics-informed neural networks), install **PyTorch**:

```bash
# CPU-only version (no dedicated GPU, or Apple Silicon — PyTorch uses MPS automatically)
conda install pytorch torchvision torchaudio -c pytorch -y

# NVIDIA GPU version (confirm CUDA version first: nvidia-smi; example for CUDA 12.1)
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia -y
```

Domain-specific libraries worth knowing: for bioinformatics, `conda install -c conda-forge biopython -y` (sequence analysis, PDB protein structure file parsing); for materials science, `conda install -c conda-forge pymatgen -y` (Materials Project API, crystal structure analysis and symmetry operations); for computational mechanics, `conda install -c conda-forge fenics-dolfinx -y` (FEniCSx finite-element framework for custom PDE solving); for simulation data I/O, `conda install -c conda-forge h5py netcdf4 -y` (reading and writing HDF5 and NetCDF files common in large-scale finite-element and molecular dynamics outputs).

---

## 6. JupyterLab — The Core Interactive Scientific Computing Environment

JupyterLab is the most widely used interactive computing environment in modern scientific research. Running in a browser, it integrates in a single interface: code editing and execution, inline figure display, Markdown text with LaTeX mathematical formula rendering, file system browsing, and an embedded terminal. For scientific work that must simultaneously present experimental data, computational logic, visualization results, and scientific interpretation, the Notebook format — a "computational document" — has irreplaceable value. A Notebook is not merely a programming tool; it is a medium for recording the scientific exploration process, making "code as experimental record" a practical reality.

After activating your conda environment, launch JupyterLab:

```bash
conda activate matsci
jupyter lab
```

JupyterLab automatically opens in your default browser at `http://localhost:8888`. When working on a remote server (HPC cluster or cloud instance), direct browser access is not possible; use SSH port forwarding instead:

```bash
# Run on your local machine — maps the server's port 8888 to your local port 8888
ssh -L 8888:localhost:8888 username@server-ip

# Then on the remote server, start JupyterLab without automatically opening a browser
jupyter lab --no-browser --port=8888

# Copy the token URL from the server terminal output into your local browser
```

Understanding the **Kernel** concept is critical for using JupyterLab correctly. The Kernel is the Python process that actually executes the code in the background, completely separate from the JupyterLab interface process. Each Notebook has an associated Kernel, and the Kernel's Python environment determines which packages can be imported. When you encounter `ModuleNotFoundError: No module named 'torch'`, the most common cause is not that PyTorch was never installed, but that the Notebook's current Kernel corresponds to a conda environment different from the one where PyTorch was installed.

Registering a conda environment as an available JupyterLab Kernel:

```bash
conda activate matsci
conda install -c conda-forge ipykernel -y
python -m ipykernel install --user --name matsci --display-name "Python (matsci)"
```

After registration, "Python (matsci)" appears in JupyterLab's Launcher (when creating a new Notebook) and in the Kernel selector at the top-right of any open Notebook. Each conda environment can be registered independently, allowing multiple Notebooks associated with different environments to run simultaneously within one JupyterLab instance.

Practical JupyterLab techniques worth internalizing: **Magic Commands** are Jupyter-specific convenience functions — `%timeit func()` automatically runs a function multiple times and reports execution statistics, useful for benchmarking algorithm efficiency; `%matplotlib inline` embeds figures directly into cell outputs; `%%bash` runs an entire cell as shell commands. **Tab autocompletion** and **inline documentation** (type `function_name?` and press Shift+Enter to display the full docstring) significantly reduce time spent looking up reference documentation. Notebook files are fundamentally JSON and can be tracked with git; installing **nbstripout** (`conda install -c conda-forge nbstripout`) and configuring it as a pre-commit hook strips all output cells before commits, keeping git diffs focused on code changes rather than output data.

---

## 7. VS Code Integration — From Exploratory Analysis to Engineering-Grade Development

JupyterLab is ideal for exploratory analysis: you are uncertain about the data structure, trying things step by step, with each step's output immediately visible. When the analysis logic stabilizes and you need to produce reproducible scripts, build data processing pipelines, or write analysis modules that others can import and reuse, **VS Code (Visual Studio Code)** becomes the more appropriate environment. The two are complementary rather than competing: a common workflow is to explore in JupyterLab, confirm the logic, then refactor into clean `.py` scripts in VS Code.

Download and install VS Code from `https://code.visualstudio.com` (installers available for Windows, macOS, and Linux). In the Extensions panel (shortcut `Ctrl+Shift+X`, or `Cmd+Shift+X` on macOS), search and install the following:

- **Python** (the official Microsoft extension): syntax highlighting, IntelliSense autocompletion, Linting, inline variable inspection during debugging, and integrated test runner
- **Jupyter** (Microsoft): open and edit `.ipynb` files directly in VS Code, and run `.py` scripts with `# %%` comment delimiters as interactive cells — the interactive execution experience of a Notebook without requiring the `.ipynb` format

To decide whether to use conda or pip for a given package: **prefer pip for pure Python packages** (NumPy, Pandas, Matplotlib, scikit-learn) — faster and always up-to-date; use conda only for packages with complex compiled dependencies (PyTorch, FEniCSx, CUDA toolkits). In practice, after installing `Ctrl+Shift+P` (`Cmd+Shift+P` on macOS) to open the Command Palette, type `Python: Select Interpreter`, and choose the Python path corresponding to your conda environment (the path typically contains `envs/matsci`, e.g., `/home/username/miniconda3/envs/matsci/bin/python`). Once selected, all autocompletion, Linting, and debugging will use the packages installed in that environment.

The most valuable VS Code feature for researchers working with remote computation is **Remote Development**. The **Remote - SSH** extension lets you edit and run code stored on a remote server — HPC cluster, institutional computing node, or cloud VM — using VS Code's full IDE interface on your local Mac or Windows machine. You get the benefit of your high-resolution screen and familiar keyboard layout while computation executes on the server's GPU or large-memory resources. This workflow is substantially more efficient than editing code in `vim` or `nano` over SSH. Setup: after installing the extension, press `F1`, select `Remote-SSH: Connect to Host`, enter `username@server-ip`, and VS Code handles the rest automatically.

---

## 8. The conda–pip Relationship and Best Practices

When managing environments with conda, you will eventually encounter packages unavailable in conda channels that can only be installed with pip. Understanding the division of responsibility between conda and pip is key to avoiding dependency conflicts and environment corruption.

**conda** is a **general-purpose package manager** whose scope includes Python packages, the Python interpreter itself, and all non-Python binary dependencies — C/C++ shared libraries, compilers, CUDA runtimes, and so on. When conda installs a package, it performs full dependency resolution across the entire tree of requirements and installs a mutually compatible set of all needed components simultaneously. This holistic resolution is particularly important for scientific computing packages, which often carry complex compiled C extensions with version-sensitive binary dependencies.

**pip** is a **Python-specific package manager** that handles only Python packages and does not manage binary-level dependencies. Pip's dependency resolution is comparatively weaker: it may only discover conflicts after installation, rather than before. However, pip covers far more packages than conda — many newly published research codebases (especially experimental libraries on GitHub) are published only on PyPI, without a corresponding conda package.

Mixing conda and pip within the same environment is entirely reasonable, but a strict ordering principle must be respected: **use conda to install every package that conda can provide first; only use pip for packages that conda cannot supply.** The reason is that conda's dependency solver cannot accurately identify the version information of packages already installed by pip; if large numbers of packages are first installed with pip and conda is then used for additional packages, conda may overwrite or force-downgrade pip-installed packages, corrupting the environment state.

To determine whether a given package should be installed with conda or pip, follow this sequence: first, search conda-forge (`conda search -c conda-forge package-name`); if conda-forge provides the package at an adequate version, install it with conda; only if conda-forge does not carry it or only has an outdated version should you fall back to pip. The conda-forge community repository covers an extremely wide range of packages — BioPython, pymatgen, FEniCSx, NGsolve, and most other scientific computing tools are available there, often with update speeds comparable to PyPI.

```bash
# Recommended operational sequence
conda activate matsci

# Step 1: install everything available via conda
conda install -c conda-forge numpy scipy pandas matplotlib scikit-learn -y
conda install -c conda-forge biopython pymatgen -y

# Final step: only resort to pip for packages not on conda
pip install some-niche-library-only-on-pypi
```

---

## 9. Network Acceleration for Users in China

Users in China frequently encounter very slow download speeds or connection timeouts when installing conda packages, because conda's default download servers are located outside the country. Switching to domestic mirror servers maintained by Chinese universities can increase installation speeds by orders of magnitude. The following configuration uses **Tsinghua University's TUNA mirror**, which is noted for high update frequency and reliability:

```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --set show_channel_urls yes
```

After configuration, the download addresses shown during `conda install` operations will switch to `tuna.tsinghua.edu.cn`. Downloads that previously took several minutes typically complete within seconds. If TUNA is intermittently unavailable, the Beijing Foreign Studies University mirror (`mirrors.bfsu.edu.cn`) is a comparable alternative with identical configuration syntax.

pip can be mirrored as well. For one-time use without modifying the configuration file:

```bash
pip install package-name -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/
```

For permanent configuration, create or edit the pip config file (Windows: `%APPDATA%\pip\pip.ini`; macOS/Linux: `~/.pip/pip.conf` or `~/.config/pip/pip.conf`):

```ini
[global]
index-url = https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/
trusted-host = mirrors.tuna.tsinghua.edu.cn
```

If `conda install` continues to stall on "Solving environment..." even after configuring mirrors — this is a dependency solver performance issue entirely unrelated to network speed — install Mamba (`conda install -n base -c conda-forge mamba -y`) and replace `conda install` with `mamba install`. The C++ solver in Mamba typically reduces resolution time from minutes to seconds.

---

## 10. Troubleshooting Reference

Even with careful adherence to the steps above, environment configuration issues can still arise. The following covers the most frequently encountered failure patterns, organized by symptom, root cause, and solution.

**`conda` command not recognized (Windows CMD or PowerShell)**

Symptom: typing `conda` in CMD or PowerShell returns "'conda' is not recognized as an internal or external command." Root cause: the "Add to PATH" checkbox was not ticked during installation, or ordinary CMD is being used instead of Anaconda Prompt. Resolution: open **Anaconda Prompt** from the Start menu and use it as the standard command-line interface. If you prefer PowerShell, run it as administrator, execute `Set-ExecutionPolicy RemoteSigned`, then `conda init powershell`, and restart PowerShell.

**`conda activate` fails on macOS or Linux**

Symptom: running `conda activate matsci` returns `CommandNotFoundError` or "conda activate is not supported in non-interactive shells." Root cause: conda's shell initialization script was not loaded, typically because the `conda init` step was skipped during installation. Resolution: run `conda init zsh` (macOS default) or `conda init bash` (Linux default), then close and reopen the terminal to load the initialization code written into `~/.zshrc` or `~/.bashrc`.

**`ModuleNotFoundError` when importing a package in Jupyter**

Symptom: a package is visibly installed via conda, but `import` in a Notebook throws ModuleNotFoundError. Root cause: the Notebook's active Kernel corresponds to a different conda environment than the one where the package was installed. Diagnosis: run `import sys; print(sys.executable)` in the first Notebook cell to see the actual Python interpreter path the Kernel is using, and verify it contains the expected conda environment name. Resolution: re-register ipykernel as described in Section 6, then switch the Notebook's Kernel to the correct environment using the selector in the top-right corner.

**`DLL load failed` when importing a package on Windows**

Symptom: after installing a package, `import` throws `ImportError: DLL load failed while importing xxx`. Root cause: the Microsoft Visual C++ Redistributable runtime is missing. Resolution: download and install the latest Visual C++ Redistributable from the Microsoft website (install both x64 and x86 versions), restart the computer, and retry.

**Package installation fails on Apple Silicon Mac due to architecture mismatch**

Symptom: `conda install` on an M-series Mac reports that no arm64 version is available, or the installed package fails to import. Root cause: the package has not yet been compiled for the Apple Silicon architecture. Temporary workaround: create an x86_64 Rosetta 2 environment for the incompatible package (`CONDA_SUBDIR=osx-64 conda create -n compat python=3.10 -y`), noting that performance will be reduced. Better approach: check conda-forge for the arm64 version — community maintainers typically provide Apple Silicon builds quickly, often faster than the default Anaconda channel.

**`conda install` freezes indefinitely on "Solving environment..."**

Root cause: conda's default SAT-based dependency solver becomes computationally expensive with complex dependency graphs — this is a solver performance issue, not a network issue. Resolution: install Mamba (`conda install -n base -c conda-forge mamba -y`) and replace `conda install` with `mamba install`. Under the same dependency conditions, Mamba's C++ solver typically completes in seconds rather than minutes.

For issues not covered here, search Stack Overflow using the complete English-language error message (English search results are typically more numerous and more current). The conda-forge GitHub Issues tracker (`github.com/conda-forge/conda-forge.github.io/issues`) is a comprehensive resource for environment-specific problems that goes beyond what general forums can address.

---

## References

1. Anaconda, Inc. (2024). Anaconda Distribution Documentation. Anaconda, Inc. https://docs.anaconda.com

2. conda Contributors (2024). Conda User Guide (Version 24.x). conda.io. https://docs.conda.io/en/latest/

3. Project Jupyter (2024). JupyterLab Documentation. ReadTheDocs / GitHub. https://jupyterlab.readthedocs.io

4. Microsoft (2024). Python in Visual Studio Code — Getting Started Tutorial. Microsoft Docs. https://code.visualstudio.com/docs/python/python-tutorial

5. Pérez, F., & Granger, B. E. (2007). IPython: A System for Interactive Scientific Computing. *Computing in Science & Engineering*, 9(3), 21–29. https://doi.org/10.1109/MCSE.2007.53

6. Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020). Array programming with NumPy. *Nature*, 585, 357–362. https://doi.org/10.1038/s41586-020-2649-2

7. Virtanen, P., Gommers, R., Oliphant, T. E., et al. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python. *Nature Methods*, 17, 261–272. https://doi.org/10.1038/s41592-019-0686-2

8. McKinney, W. (2010). Data structures for statistical computing in Python. *Proceedings of the 9th Python in Science Conference (SciPy 2010)*, 56–61. https://doi.org/10.25080/Majora-92bf1922-00a