---
title: "GROMACS MD Tutorial: Structure Prep to Trajectory Analysis"
date: "2026-06-29"
category: "multiscale-modeling"
tags: ["GROMACS", "molecular dynamics", "MD simulation", "protein simulation", "trajectory analysis", "lysozyme"]
lang: "en"
slug: "gromacs-md-tutorial"
description: "A complete hands-on tutorial for GROMACS molecular dynamics simulation, covering installation, system preparation, energy minimization, equilibration, production MD, and trajectory analysis (RMSD/RMSF/Rg/H-bonds) using lysozyme as a worked example."
---

Biomaterials research increasingly relies on molecular dynamics (MD) simulation to understand the atomic-scale behavior of proteins, fibers, and polysaccharides. Among the many MD packages available, GROMACS (GROningen MAchine for Chemical Simulations) stands out for its open-source nature, exceptional computational efficiency, and active community. This tutorial walks through a complete GROMACS MD workflow using hen egg-white lysozyme (PDB: 1AKI) as a concrete example.

## Why GROMACS

GROMACS offers several key advantages over other MD engines:

- **Extreme computational efficiency**: Highly optimized CPU and GPU kernels deliver 2-5x speedup over comparable packages on a single GPU
- **Open source and free**: GPL-licensed, freely usable in both academic and industrial settings
- **Complete workflow toolkit**: Built-in commands for topology construction, solvation, ion addition, energy minimization, equilibration, and production MD
- **Rich analysis suite**: Built-in modules for RMSD, RMSF, radius of gyration, hydrogen bonds, SASA, and dozens more
- **Active community**: Excellent documentation and Justin Lemkul's classic tutorials (http://www.mdtutorials.com/gmx/) provide outstanding learning resources

For biomaterials researchers, GROMACS enables simulation of silk fibroin beta-sheet transitions, collagen mechanical stretching, cellulose solvent effects, and protein-ligand interactions.

## Installation

GROMACS supports Linux, macOS, and Windows (via WSL). The recommended installation uses conda:

```bash
conda create -n gromacs -c conda-forge -c bioconda gromacs
conda activate gromacs
gmx --version
```

For GPU-accelerated installations (NVIDIA):

```bash
conda install -c conda-forge -c bioconda gromacs="2024.*=*cuda*"
```

Verify your installation with `gmx --version`, which reports the version number and GPU support status.

## MD Simulation Workflow

A complete MD simulation proceeds through the following stages:

| Step | Command | Purpose | Typical Time |
|------|---------|---------|-------------|
| 1. Structure | wget PDB | Acquire initial coordinates | manual |
| 2. Topology | gmx pdb2gmx | Generate topology and force field | < 1 s |
| 3. Box | gmx editconf | Define simulation box | < 1 s |
| 4. Solvate | gmx solvate | Fill with water molecules | seconds |
| 5. Ions | gmx genion | Neutralize system charge | seconds |
| 6. EM | gmx grompp + mdrun | Eliminate atomic clashes | minutes |
| 7. NVT | gmx grompp + mdrun | Stabilize temperature | hours |
| 8. NPT | gmx grompp + mdrun | Stabilize pressure/density | hours |
| 9. Production | gmx grompp + mdrun | Collect trajectory data | hours-days |
| 10. Analysis | gmx rms/rmsf/... | Extract observables | minutes |

## Worked Example: Lysozyme in Water

### Step 1: Acquire the Structure

Download the lysozyme structure from the Protein Data Bank (https://www.rcsb.org/):

```bash
wget https://files.rcsb.org/download/1AKI.pdb
grep -v HOH 1AKI.pdb > protein.pdb
```

### Step 2: Generate Topology

`pdb2gmx` converts the PDB file into a topology with force field parameters. We use the well-validated AMBER99SB-ILDN force field:

```bash
gmx pdb2gmx -f protein.pdb -o processed.gro -water spc -ff amber99sb-ildn -ignh
```

This produces three files: `processed.gro` (coordinates), `topol.top` (topology), and `posre.itp` (position restraints).

### Step 3: Define the Simulation Box

```bash
gmx editconf -f processed.gro -o box.gro -c -d 1.0 -bt cubic
```

The `-d 1.0` flag places the protein at least 1.0 nm from the box edges, preventing self-interaction under periodic boundary conditions.

### Step 4: Solvate the System

Fill the box with SPC water molecules:

```bash
gmx solvate -cp box.gro -cs spc216.gro -o solv.gro -p topol.top
```

### Step 5: Add Counter-Ions

Neutralize the system charge. Create a minimal `ions.mdp` file:

```
; ions.mdp
integrator = steep
nsteps = 0
```

```bash
gmx grompp -f ions.mdp -c solv.gro -p topol.top -o ions.tpr
gmx genion -s ions.tpr -o neutral.gro -p topol.top -pname NA -nname CL -neutral
```

Use `-conc 0.15` to simulate physiological (150 mM) NaCl conditions.

### Step 6: Energy Minimization (EM)

Create the EM parameter file `em.mdp`:

```
; em.mdp
integrator      = steep
emtol           = 1000.0
emstep          = 0.01
nsteps          = 50000
cutoff-scheme   = Verlet
coulombtype     = PME
rcoulomb        = 1.0
rvdw            = 1.0
pbc             = xyz
```

Run EM:

```bash
gmx grompp -f em.mdp -c neutral.gro -p topol.top -o em.tpr
gmx mdrun -v -deffnm em
```

Check convergence: `gmx energy -f em.edr -o potential.xvg`

### Step 7: NVT Equilibration

Create `nvt.mdp` with the V-rescale thermostat at 300 K:

```
; nvt.mdp
integrator      = md
dt              = 0.002
nsteps          = 50000
nstxout-compressed = 1000
tcoupl          = V-rescale
tc-grps         = Protein Non-Protein
tau_t           = 0.1 0.1
ref_t           = 300 300
pcoupl          = no
cutoff-scheme   = Verlet
coulombtype     = PME
rcoulomb        = 1.0
rvdw            = 1.0
constraints     = h-bonds
```

```bash
gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
gmx mdrun -v -deffnm nvt
```

### Step 8: NPT Equilibration

Add pressure coupling with the Parrinello-Rahman barostat. Create `npt.mdp`:

```
; npt.mdp
integrator      = md
dt              = 0.002
nsteps          = 50000
tcoupl          = V-rescale
tc-grps         = Protein Non-Protein
tau_t           = 0.1 0.1
ref_t           = 300 300
pcoupl          = Parrinello-Rahman
pcoupltype      = isotropic
tau_p           = 2.0
ref_p           = 1.0
compressibility = 4.5e-5
continuation    = yes
```

```bash
gmx grompp -f npt.mdp -c nvt.gro -t nvt.cpt -r nvt.gro -p topol.top -o npt.tpr
gmx mdrun -v -deffnm npt
```

Verify density converges to ~1000 kg/m^3: `gmx energy -f npt.edr -o density.xvg`

### Step 9: Production MD

Create `md.mdp` with position restraints removed:

```
integrator      = md
dt              = 0.002
nsteps          = 5000000
nstxout-compressed = 5000
tcoupl          = V-rescale
tc-grps         = Protein Non-Protein
tau_t           = 0.1 0.1
ref_t           = 300 300
pcoupl          = Parrinello-Rahman
pcoupltype      = isotropic
tau_p           = 2.0
ref_p           = 1.0
compressibility = 4.5e-5
continuation    = yes
```

```bash
gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr
gmx mdrun -v -deffnm md -nb gpu
```

The `-nb gpu` flag offloads non-bonded calculations to the GPU, delivering 5-10x speedup on modern hardware.

## Trajectory Analysis

### RMSD

RMSD measures overall conformational deviation from a reference structure. For globular proteins, RMSD typically stabilizes around 0.1-0.3 nm.

```bash
gmx rms -s md.tpr -f md.xtc -o rmsd.xvg -tu ns
# Select backbone (group 4) for fitting and calculation
```

### RMSF

RMSF reveals per-residue flexibility. High RMSF regions correspond to flexible loops; low RMSF regions indicate stable secondary structure elements.

```bash
gmx rmsf -s md.tpr -f md.xtc -o rmsf.xvg -res
# Select backbone (group 4)
```

### Radius of Gyration (Rg)

Rg describes overall protein compactness and serves as a reliable folding-state indicator.

```bash
gmx gyrate -s md.tpr -f md.xtc -o gyrate.xvg
```

### Hydrogen Bond Analysis

Hydrogen bonds maintain protein secondary structure. GROMACS can quantify both intra-protein and protein-solvent H-bonds.

```bash
# Intra-protein H-bonds
gmx hbond -s md.tpr -f md.xtc -num hbond_num.xvg

# All H-bonds (including protein-water)
gmx hbond -s md.tpr -f md.xtc -num hbond_all.xvg
```

### Python Analysis Code

Below is a self-contained Python script for visualizing key trajectory observables:

```python
import numpy as np
import matplotlib.pyplot as plt

# RMSD analysis
data = np.loadtxt('rmsd.xvg', comments=('#', '@'))
time_ns = data[:, 0] / 1000
rmsd_nm = data[:, 1]
print(f"Equilibrated RMSD: {np.mean(rmsd_nm[1000:]):.4f} +/- {np.std(rmsd_nm[1000:]):.4f} nm")

# Radius of gyration
data_rg = np.loadtxt('gyrate.xvg', comments=('#', '@'))
rg = data_rg[:, 1]
print(f"Mean Rg: {np.mean(rg[1000:]):.4f} nm, Stability: {np.std(rg[1000:]):.4f} nm")

# Hydrogen bonds
data_hb = np.loadtxt('hbond_num.xvg', comments=('#', '@'))
hbonds = data_hb[:, 1]
print(f"Average intra-protein H-bonds: {np.mean(hbonds[1000:]):.1f}")

# Multi-panel plot
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
axes[0].plot(time_ns, rmsd_nm)
axes[0].set_xlabel('Time (ns)'); axes[0].set_ylabel('RMSD (nm)')
axes[1].plot(time_ns[:len(rg)], rg)
axes[1].set_xlabel('Time (ns)'); axes[1].set_ylabel('Rg (nm)')
axes[2].plot(time_ns[:len(hbonds)], hbonds)
axes[2].set_xlabel('Time (ns)'); axes[2].set_ylabel('H-bonds')
plt.tight_layout()
plt.savefig('analysis_summary.png', dpi=150)
```

## Performance Optimization

1. **GPU acceleration**: Use `-nb gpu -pme gpu` to offload both non-bonded and PME calculations to GPU
2. **Periodic boundary conditions**: For non-globular systems (fibers, membranes), use a rhombic dodecahedron box (`-bt dodecahedron`) which saves ~30% of water molecules compared to cubic
3. **Time step**: With H-bond constraints (LINCS), safely increase the time step from 1 fs to 2 fs, or 4-5 fs with virtual sites
4. **Force field selection**: AMBER99SB-ILDN or CHARMM36m for proteins, OL15 for nucleic acids
5. **PME grid spacing**: Recommended 0.12-0.16 nm; box dimensions should be powers of 2 for efficient FFT

## Common Issues and Troubleshooting

**Simulation crashes immediately?**
1. Verify EM convergence: Fmax should be below 1000 kJ/(mol*nm)
2. Reduce time step to 1 fs if crashes persist
3. Check PBC settings: ensure `-d` is large enough
4. Confirm force field compatibility with your system

**NPT density unstable?**
- Ensure `tau_p` is in the 1-5 ps range
- Verify `compressibility` matches your solvent (water: 4.5e-5 bar^-1)
- Consider pre-equilibrating with the Berendsen barostat before switching to Parrinello-Rahman

## GROMACS in Multiscale Biomaterials Research

GROMACS occupies a pivotal position in multiscale modeling:

- **Upward**: Mechanical parameters extracted from MD trajectories (elastic moduli, bond strengths, contact maps) feed coarse-grained models (Martini) and finite element analysis (Abaqus, FEniCS)
- **Downward**: QM calculations (Gaussian, ORCA) provide electrostatic potentials for force field parameterization
- **ML integration**: MD trajectories serve as training data for machine-learned force fields (ANI, NequIP, MACE)

For fiber biomaterials, GROMACS can simulate silk fibroin conformational transitions, collagen mechanics under tension, and cellulose-solvent interactions. The basic workflow demonstrated here is the first step toward these more specialized applications.

## Summary

This tutorial demonstrated a complete GROMACS molecular dynamics workflow using lysozyme as an example: structure acquisition, topology generation, solvation, ion addition, energy minimization, NVT/NPT equilibration, production MD, and trajectory analysis (RMSD, RMSF, Rg, H-bonds). This pipeline applies to most soluble proteins and many biopolymer systems. For fiber biomaterials such as silk, collagen, and cellulose, special attention to periodic boundary conditions and force field selection is required, topics to be covered in subsequent articles.

## References

1. Abraham, M.J., Murtola, T., Schulz, R., Pall, S., Smith, J.C., Hess, B., & Lindahl, E. (2015). GROMACS: High performance molecular simulations through multi-level parallelism from laptops to supercomputers. *SoftwareX*, 1-2, 19-25.
2. Van Der Spoel, D., Lindahl, E., Hess, B., Groenhof, G., Mark, A.E., & Berendsen, H.J.C. (2005). GROMACS: Fast, flexible, and free. *Journal of Computational Chemistry*, 26(16), 1701-1718.
3. Lemkul, J.A. (2018). GROMACS Tutorial: Lysozyme in Water. http://www.mdtutorials.com/gmx/lysozyme/index.html
4. GROMACS Development Team. (2024). GROMACS Reference Manual. https://manual.gromacs.org/
5. Lindorff-Larsen, K., Piana, S., Palmo, K., Maragakis, P., Klepeis, J.L., Dror, R.O., & Shaw, D.E. (2010). Improved side-chain torsion potentials for the Amber ff99SB protein force field. *Proteins*, 78(8), 1950-1958.
6. Berman, H.M., Westbrook, J., Feng, Z., Gilliland, G., Bhat, T.N., Weissig, H., Shindyalov, I.N., & Bourne, P.E. (2000). The Protein Data Bank. *Nucleic Acids Research*, 28(1), 235-242.
