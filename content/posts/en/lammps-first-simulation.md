---
title: "Molecular Dynamics Basics: Your First LAMMPS Simulation"
date: "2026-06-26"
category: "multiscale-modeling"
tags: ["molecular-dynamics", "LAMMPS", "simulation", "tutorial", "force-fields"]
lang: "en"
slug: "lammps-first-simulation"
description: "A hands-on guide to running your first molecular dynamics simulation with LAMMPS: installation, input script structure, force fields, water box simulation, and trajectory analysis."
---

## What is Molecular Dynamics?

MD simulates the motion of atoms by solving Newton's equations (F=ma) at each timestep. Given initial positions, velocities, and a force field (potential energy function), MD predicts how a system evolves over time.

For biomaterials research, MD answers questions like:
- What is the Young's modulus of a collagen microfibril?
- How do water molecules interact with silk fibroin surfaces?
- What happens to a protein under tensile load?

## Installing LAMMPS

LAMMPS (Large-scale Atomic/Molecular Massively Parallel Simulator) from Sandia National Labs is the most widely used open-source MD code.

**Option 1: Pre-built binary (recommended for beginners)**
```bash
# Linux (Ubuntu/Debian)
sudo apt install lammps

# macOS
brew install lammps

# Windows: download from https://packages.lammps.org/windows.html
```

**Option 2: Conda (cross-platform)**
```bash
conda create -n lammps -c conda-forge lammps -y
conda activate lammps
```

Verify installation:
```bash
lmp_serial -h
```

## Anatomy of a LAMMPS Input Script

A LAMMPS input file has four essential sections:

```bash
# ===== 1. Initialization =====
units           real        # Energy: kcal/mol, Distance: Angstrom
atom_style      full        # Atoms have charge, molecule ID
boundary        p p p       # Periodic in all directions

# ===== 2. System Setup =====
region          box block 0 30 0 30 0 30
create_box      2 box       # 2 atom types
create_atoms    1 random 500 12345 box

# ===== 3. Force Field =====
pair_style      lj/cut 10.0
pair_coeff      1 1 0.155 3.166  # O-O Lennard-Jones parameters

# ===== 4. Run =====
velocity        all create 300.0 12345
fix             nvt all nvt temp 300.0 300.0 100.0
thermo          100
thermo_style    custom step temp press etotal
dump            traj all custom 100 dump.lammpstrj id type x y z
run             10000
```

## Your First Simulation: Water Box

Let's simulate 500 water molecules at room temperature using the TIP3P model:

```bash
# water.lammps
units           real
atom_style      full
bond_style      harmonic
angle_style     harmonic
dihedral_style  opls

# Read TIP3P water box
read_data       water_box.data

# Assign force field
pair_style      lj/cut/coul/long 10.0 10.0
kspace_style    pppm 1e-5
include         par_oplsaa.in

# Energy minimization
minimize        1e-4 1e-6 1000 10000

# Equilibration (NVT)
velocity        all create 300.0 12345
fix             nvt all nvt temp 300.0 300.0 100.0
run             50000

# Production (NPT)
unfix           nvt
fix             npt all npt temp 300.0 300.0 100.0 iso 1.0 1.0 1000.0
run             100000
```

## Key Parameters Explained

| Parameter | Meaning | Typical Value |
|-----------|---------|---------------|
| timestep | Integration step size | 1.0-2.0 fs |
| cutoff | Non-bonded interaction cutoff | 10-12 Angstrom |
| temperature | System temperature | 300 K (room temp) |
| NVT | Constant particle number, volume, temperature | Equilibration |
| NPT | Constant particle number, pressure, temperature | Production |

## Common Force Fields

| Force Field | Best For | Reference |
|------------|---------|-----------|
| OPLS-AA | Proteins, organic molecules | Jorgensen et al. (1996) |
| CHARMM36 | Proteins, nucleic acids | Best et al. (2012) |
| AMBER ff19SB | Proteins | Tian et al. (2020) |
| ReaxFF | Reactive systems, bond breaking | van Duin et al. (2001) |
| Martini | Coarse-grained biomolecular | Marrink et al. (2007) |

## Trajectory Analysis with Python

After the simulation finishes, analyze the trajectory:

```python
import numpy as np
import MDAnalysis as mda
from MDAnalysis.analysis import rmsd, rdf

# Load trajectory
u = mda.Universe("water_box.data", "dump.lammpstrj")

# Temperature over time
temps = []
for ts in u.trajectory:
    velocities = u.atoms.velocities
    ke = 0.5 * np.sum(u.atoms.masses[:, None] * velocities**2)
    temps.append(ke * 2 / (3 * len(u.atoms) * 0.001987))

# Radial distribution function
oxygen = u.select_atoms("type O")
rdf_oo = rdf.InterRDF(oxygen, oxygen, nbins=200, range=(0, 10.0))
rdf_oo.run()
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Lost atoms" error | Decrease timestep or increase neighbor list skin |
| Energy not converging | Run longer minimization or use softer initial conditions |
| Simulation too slow | Use GPU (Kokkos package) or coarser force field |
| Segfault | Check atom type consistency in input script |

## References

- LAMMPS documentation: [docs.lammps.org](https://docs.lammps.org)
- MDAnalysis: [mdanalysis.org](https://www.mdanalysis.org)
- Allen, M.P. & Tildesley, D.J. (2017). *Computer Simulation of Liquids*. Oxford.
- GitHub: [lammps/lammps](https://github.com/lammps/lammps)
