# Content Roadmap — ml-biomat.com
Last updated: 2026-06-27 (v10: 26 posts)

## Guiding Principles
- Every article: EN + ZH pair (slug: topic / topic-zh)
- Target audience: biology/materials grad students with minimal coding experience
- Each article: substantial (1000+ words), practical code, real references
- Order: fundamental first, progressively deeper
- Cite well-known GitHub repos and papers

## Phase 1: Foundations (Week 1)
[] 1.1 Python Environment Setup (conda, Jupyter, VS Code, essential packages)
[] 1.2 Command Line Basics for Scientists (navigate, run scripts, pip/conda)
[] 1.3 Git & GitHub for Research (clone, commit, push, collaboration)
[] 1.4 File Formats in Materials Science (.txt, .csv, .xlsx, .hdf5, .data)

## Phase 2: Materials Science Fundamentals (Week 1-2)
[] 2.1 Understanding Stress-Strain Curves (elastic, plastic, fracture)
[] 2.2 Viscoelasticity Basics (creep, relaxation, DMA, Maxwell/Kelvin-Voigt)
[] 2.3 Polymer Physics for Biologists (chain statistics, entanglement, Tg)
[] 2.4 Fiber Network Architecture (connectivity, percolation, orientation)

## Phase 3: Scientific Python (Week 2)
[] 3.1 NumPy Crash Course for Experimentalists (arrays, broadcasting, I/O)
[] 3.2 Pandas for Lab Data (groupby, pivot, merge, export)
[] 3.3 Matplotlib Publication Figures (multi-panel, colors, export)
[] 3.4 Scipy for Curve Fitting (linear, nonlinear, confidence intervals)

## Phase 4: Simulation Tools (Week 2-3)
[] 4.1 LAMMPS Basics: Installation & First Simulation (water box)
[] 4.2 LAMMPS: Running MD on Biomolecules (input script, force fields)
[] 4.3 GROMACS Basics: Installation & Lysozyme in Water
[] 4.4 Trajectory Analysis with MDAnalysis (RMSD, Rg, hydrogen bonds)
[] 4.5 Visualization: VMD & PyMOL Quickstart

## Phase 5: ML for Materials (Week 3-4)
[] 5.1 scikit-learn Crash Course (train/test, CV, metrics)
[] 5.2 Regression for Property Prediction (linear, RF, XGBoost)
[] 5.3 Classification in Materials Science (phase identification, defect detection)
[] 5.4 Feature Engineering for Scientific Data (domain features, encoding)
[] 5.5 Dimensionality Reduction (PCA, t-SNE for materials data)
[] 5.6 Clustering for Pattern Discovery (k-means, DBSCAN)

## Phase 6: Deep Learning (Week 4-5)
[] 6.1 Neural Network Basics with PyTorch (tensors, autograd, training loop)
[] 6.2 CNNs for Microscopy Images (SEM/TEM classification)
[] 6.3 Graph Neural Networks for Materials (molecular graphs, crystal structures)
[] 6.4 Transfer Learning for Small Materials Datasets

## Phase 7: Advanced & Workflows (Week 5+)
[] 7.1 Uncertainty Quantification in ML Predictions
[] 7.2 Active Learning for Experiment Design
[] 7.3 Multiscale Modeling Workflows (MD → CG → FE)
[] 7.4 High-Throughput Screening with Python
[] 7.5 Reproducible Research: Containers & Workflow Managers

## Writing Pipeline
1. Read roadmap -> pick next unchecked item
2. Read INVENTORY.md -> confirm no duplicates
3. Check existing category coverage
4. Write EN article (1000+ words, code, references)
5. Write ZH article (same, Chinese)
6. python build.py -> verify audit (9+ pairs, 0 orphans)
7. git push
8. Mark roadmap item as [x]

## Key References to Cite
- numpy.org, scipy.org, matplotlib.org (official docs)
- LAMMPS manual: docs.lammps.org
- GROMACS tutorials: tutorials.gromacs.org
- MDAnalysis: mdanalysis.org
- scikit-learn: scikit-learn.org
- PyTorch tutorials: pytorch.org/tutorials
- GitHub: deepchem/deepchem, materialsproject/pymatgen
