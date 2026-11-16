# Why Molecules Move: Force Fields, Time Steps and Boundaries

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g04/en/
Language: en

Connect attraction, repulsion, and periodic space, then compare fast fluctuations and slow drift in actual 1 fs and 2 fs water calculations.

## The same water can have different computational descriptions

A drop of water on a leaf gathers into a rounded shape. A salt crystal gradually disappears into water. Around a protein, water participates in the motions that change the molecule’s shape. All these behaviours involve interactions between molecules. Molecular dynamics gives those interactions a calculable description: from the current positions, the program determines forces and advances the system through a small interval of time. Once molecules are moving on the screen, three questions become particularly useful. What makes the model attract or repel its neighbours? How far does each numerical update advance? What environment lies beyond the displayed box? Together, these choices specify the computational water we are studying.

Think of planning a journey with a map. The connections between roads resemble the model’s list of atoms and chemical connections. Road gradients influence acceleration, much as changes in potential energy influence molecular motion. The frequency with which a navigation system updates a position resembles the integration time step, while the continuation of the map beyond its edges resembles a boundary condition. The useful distinction is between changing the map and following it more carefully. More frequent position updates give a finer description of travel along a particular road, but they do not repair a road drawn in the wrong place. Similarly, changing a time step from 2 to 1 femtosecond primarily tests how we propagate an existing model; its charges and interaction parameters remain unchanged.

We continue with the prepared system of 884 SPC/E water molecules. Each molecule contains one oxygen site and two hydrogen sites. Its internal geometry remains fixed during molecular dynamics, while the molecule can translate and rotate. This model lets us examine intermolecular organization and fluctuations at a modest computational cost. Describing O–H stretching vibrations or proton transfer between molecules requires additional molecular degrees of freedom and a different interaction description. Naming the motion of interest therefore helps define the model’s purpose. Here, the question concerns how a classical rigid-water model is propagated numerically and how energy changes reveal features of that propagation.

The chapter culminates in a comparison using actual calculations. Two branches begin from the same state prepared under temperature and pressure control. One advances every 1 femtosecond and the other every 2 femtoseconds; both cover 100 picoseconds. We subtract each branch’s own initial energy, then separate a gradual trend from faster fluctuations. Understanding these plots calls for a little mechanics, periodic geometry, and data analysis, introduced where they become useful. By the end, you should be able to explain the roles of the time step, cutoffs, constraints, and PME in the input, and choose a diagnostic that answers a particular numerical or scientific question.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g04/en/#en-s1)

Figure 1 · The analytical pair LJ potential describes distance-dependent attraction and repulsion; rigid water also has an oriented charge distribution.

## Read force-field parameters through attraction and repulsion

The name “force field” can suggest a pre-drawn map of forces. In practice, it is a collection of rules for calculating potential energy from a configuration: which interactions exist, which mathematical forms describe them, and which parameters belong to different atom types. Potential energy is an account of the energy associated with an arrangement. Pushing atoms very close together generally raises that account sharply; attraction at suitable separations can lower it. A force describes how the energy changes with position and acts toward decreasing energy. The analogy with a ball accelerating down a slope is helpful, although a molecule simultaneously feels the contributions of many neighbours in three dimensions.

A common distance-dependent contribution is the Lennard–Jones potential, abbreviated LJ. It combines steep short-range repulsion and longer-range dispersion attraction in one expression. Repulsion is related to quantum effects associated with overlapping electron distributions, represented here by a convenient steep function. Dispersion attraction originates in correlated fluctuations of those distributions and is also reduced to a function of distance. This physical background gives a useful interpretation of molecular pictures. The coloured spheres are representations of spatial relationships; the potential function determines the energetic cost of approaching another site. There is no literal painted shell at the surface of the sphere.

Describe LJ attraction and repulsion through separationEq. 1

![Describe LJ attraction and repulsion through separation](https://ml-biomat.com/static/agent-math/cb02485b464c14b929bd8ac8.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ULJ | Lennard–Jones potential-energy contribution for a site pair | kJ mol⁻¹ |
| r | Separation of the two sites | nm |
| σ | Separation parameter where this expression crosses zero | nm |
| ε | Positive well-depth parameter setting the energy scale | kJ mol⁻¹ |
| 4, 12, 6 | Numerical factor 4 and exponents 12 and 6 | dimensionless |
| =, /, −, [ ], ( ), × | Equality defines energy; divide the lengths; subtraction combines repulsion and attraction; brackets group terms; adjacent factors multiply | operators have no units |

Reading the relationshipThe ratio σ/r is dimensionless. The twelfth power grows faster at short range, while the attractive sixth-power contribution dominates farther away. ε supplies energy units.

A worked exampleFor illustrative σ=0.30 nm and ε=0.65 kJ mol⁻¹, U=0 at r=0.30 nm. The minimum occurs at r=2^(1/6)σ≈0.3367 nm with U=−0.65 kJ mol⁻¹. These values illustrate the curve; the running SPC/E model has its own parameter table.

ConditionsThis is an untruncated, unshifted pairwise LJ term. Water additionally includes electrostatics; actual cutoff, energy-shift, and long-range corrections follow the run settings.

Begin with the ratio inside the brackets. Both the separation r and the parameter σ are lengths, expressed here in nanometres. Their units cancel, so the sixth and twelfth powers operate on a dimensionless number. At r equal to σ, the two powers cancel and the energy is zero. At slightly larger separations, attraction dominates and the energy becomes negative. At separations smaller than σ, the twelfth-power contribution grows particularly rapidly and repulsion dominates. The parameter ε sets the well depth: how far the minimum lies below the zero approached at large separation. The minimum occurs at approximately 1.122σ, so σ and the minimum-energy separation have different meanings. Varying σ primarily changes the distance scale, while varying ε changes the energy scale.

In this SPC/E model, the LJ contribution acts between oxygen sites. Intermolecular electrostatic interactions also act between charged sites. The oxygen carries a negative partial charge and the two hydrogens carry positive partial charges that sum with it to zero. These are model parameters representing the molecular charge distribution. They do not identify the oxygen as a free oxygen ion or the hydrogens as free protons. Two neutral water molecules can nevertheless respond to the spatial arrangement of each other’s charges. Changing their relative orientation changes several charge-pair distances, giving an orientation-dependent total interaction. The hydrogen-bond network that develops among suitably oriented molecules is consequently an important part of liquid-water organization.

The familiar rule that opposite charges attract can be understood from the sign of the electrostatic energy. Opposite charges have a negative product, so approaching lowers that contribution; equal-sign charges have a positive product, so approaching raises it. In a liquid, the complete electrostatic calculation includes many charge pairs and the periodic environment. Explicit water already represents screening through the collective responses of water molecules. In this example, we therefore do not additionally divide every charge interaction by a macroscopic water dielectric constant near 80. That macroscopic quantity summarizes the response of many molecules; adding it indiscriminately to this explicit model would change the physical description associated with the parameters.

Force-field choices are also choices of compatible components. Water charges, oxygen LJ parameters, constrained geometry, and long-range treatment collectively define a model. A protein adds bond, angle, and torsional terms, as well as rules for combining interactions between different atom types. Two files being readable by the same program does not establish that their parameters form a coherent model. When comparing models, specify the complete parameter combinations and choose observations relevant to the question, such as density, conformational distributions, or hydration. A difference in output then refers to a defined scientific comparison, rather than simply to two differently named directories.

## Choose a step that resolves the motions retained in the model

A film creates an impression of continuous motion by displaying many frames. Molecular dynamics also uses discrete times, but it must calculate each new frame from the current forces. Over a sufficiently short interval, a force can be treated as approximately constant while updating a velocity, followed by a position. The updated position changes the forces, and the procedure repeats. A larger time step spans more physical time per update, reducing the number of updates needed for a fixed trajectory duration. It also gives a coarser description of the force changes during that interval. This is the most direct connection between computational speed and temporal resolution.

To understand what sets a suitable step, imagine recording the position of a swinging pendulum at regular intervals. If one oscillation takes a second, recording only every half-second can miss important features around the turning points. A small, rapidly vibrating component attached to the pendulum would require even more frequent observations. Molecules also contain multiple time scales. Stretching of covalent bonds involving hydrogen is fast; water reorientation and neighbour rearrangement are slower; large protein conformational changes can be much slower still. The integration step must stably handle the fast motions retained in the model, even when the scientific question concerns a slow process.

Constraints provide an explicit way to alter those retained degrees of freedom. During SPC/E dynamics, the two O–H distances and the H–H distance remain fixed, preserving the geometry of the three sites. The algorithm calculates the corrections required to maintain these relationships while continuing to calculate intermolecular forces. The model thus omits explicit internal bond-length vibrations and permits a time step suitable for rigid water. The input option named h-bonds concerns constraints on covalent bonds involving hydrogen. For the water in this example, the topology’s SETTLE specification implements the rigid geometry. Intermolecular hydrogen bonds remain free to rearrange as molecules translate and rotate.

In 1967, Loup Verlet studied classical fluids using Lennard–Jones particles. Efficient time integration and the organization of neighbour information became important tools in the development of molecular simulation. The historical problem remains recognizable: how can a computer accumulate a large number of simple local updates into useful fluid statistics? Modern algorithms still have to reconcile computational cost, numerical error, and the definitions of reported physical quantities. The md integrator used here in GROMACS employs a leapfrog formulation, with positions and velocities represented at interleaved times. The name reflects the way one set of variables steps past the other during successive updates.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g04/en/#en-s3)

Figure 2 · Verlet’s 1967 classical-fluid work supplies historical context; the diagram shows the position/velocity timing of the leapfrog integrator used in this GROMACS example.

This timing detail matters when comparing energies. Kinetic energy depends on squared velocities, and leapfrog reports its full-time value using an average of neighbouring half-step kinetic energies. The half-step spacing changes with the integration step. Here the initial reported total energies are −34831.664062 and −34812.765625 kJ mol⁻¹ for the 1 fs and 2 fs branches, respectively. They read the same saved NPT state but have different discrete energy baselines. Interpreting that difference requires the timing and kinetic-energy definitions, rather than treating it as evidence that one branch suddenly received heat. We examine how each branch changes relative to its own starting value. Both energy-change curves therefore begin at zero, allowing their subsequent trends and fluctuations to be compared.

Distinguish the integration step from the output interval as well. Advancing every 2 femtoseconds and saving energy every 100 steps produces one row every 0.2 picoseconds. Advancing every 1 femtosecond while still saving every 100 steps produces one row every 0.1 picoseconds. The second table contains more rows, but that does not imply proportionally more independent configurations or a different physical duration. Both branches here cover 100 picoseconds. The analysis selects the 0.2-picosecond times present in both records, giving each fit 501 measurements at the same physical times. This establishes a common observation window and sampling grid for the numerical comparison.

## Why does a molecule leaving one edge return at the other?

A small cluster of water placed in vacuum contains very different environments at its surface and in its interior. An interior molecule has neighbours in all directions, whereas a surface molecule faces an empty region on one side. For droplets and interfaces, this distinction is part of the scientific question. For a bulk liquid, a large artificial surface complicates the study of an interior environment. Periodic boundary conditions instead treat the simulated box as a unit repeated in three dimensions. A molecule leaving the right side appears at an equivalent position on the left. The boundary is a spatial identification, with no wall that reflects the molecule.

Start with distance in one dimension. In a periodic interval of length 3 nanometres, place one site at 0.1 nanometres and another at 2.9 nanometres. Subtracting the coordinates gives a separation of 2.8 nanometres. Across the periodic edge, however, their closest images are only 0.2 nanometres apart. Short-range interactions require a distance consistent with this geometry. The minimum-image convention chooses the nearest member among equivalent periodic copies. These copies are images of the same simulation unit, rather than additional independent collections of water molecules with their own random motion.

Find the nearest displacement in a one-dimensional periodic intervalEq. 2

![Find the nearest displacement in a one-dimensional periodic interval](https://ml-biomat.com/static/agent-math/e61e73c822f13935af958b4b.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Δx | Direct coordinate difference, x2−x1 in this example | nm |
| ΔxMI | Signed minimum-image displacement; its absolute value gives distance | nm |
| L | Positive periodic interval length | nm |
| round | Nearest-integer operation identifying how many box lengths to subtract | dimensionless |
| Δ, MI, =, −, /, ×, ( ) | Δ denotes a difference; MI labels minimum image; equality defines the result; subtract an integer number of box lengths; divide; multiply adjacent factors; group operations | operators and labels have no units |

Reading the relationshipEquivalent periodic displacements differ by integer box lengths. Subtracting the nearest multiple of L places the displacement in the interval nearest zero.

A worked exampleWith x1=0.1 nm, x2=2.9 nm, and L=3 nm, the direct displacement is 2.8 nm. round(2.8/3)=1 gives −0.2 nm as the minimum-image displacement and 0.2 nm as its distance.

ConditionsThis applies to one dimension or an orthogonal-box component. Skewed cells require full box vectors. At exactly half a box length, two directions are equally near and give the same distance.

[Figure: One-dimensional periodic minimum-image distance](https://ml-biomat.com/tutorials/molecular-dynamics/g04/en/#en-s4)

Grey: direct coordinate separation. Orange: shortest periodic route. A remains at 0.10 nm.

Move a site to compare direct coordinate separation with the shortest periodic distance.

The interactive diagram fixes one site and lets the other move through a 3-nanometre interval. Sometimes the direct coordinate difference and the shortest periodic distance agree; sometimes they differ. When the sites lie near opposite edges, they can appear far apart on the page while being close neighbours in periodic space. This also explains apparent jumps or split molecules in a displayed trajectory. A visualization program may place equivalent coordinates back inside a chosen unit cell. Analysing internal molecular distances, the shape of a whole chain, or a continuous displacement requires suitable reconstruction, centring, or unwrapping so that the coordinates match the observable being calculated.

Periodic boundaries replace a surface problem with finite-size and periodic-repetition effects. The wavelengths of fluctuations that fit within the box are restricted, and a solute can respond to its periodic images through the surrounding environment. For water, increasing the box size helps test whether an observable depends appreciably on system size. For a long polymer, it is also necessary to examine whether the chain approaches its own images during motion. A correctly calculated minimum-image distance establishes the geometric calculation, while a suitable box size establishes whether the represented environment serves the scientific question. Both checks contribute to interpreting a result.

For a simple cubic cell, the short-range cutoff must remain smaller than half the box length to meet the relevant minimum-image condition. The initial box here is 3 nanometres across and the short-range cutoff is 1 nanometre. The box after pressure adjustment must continue to satisfy the corresponding geometric requirement. Later protein examples use a non-cubic cell to reduce the amount of solvent needed. Those cases require reasoning from the actual box vectors; the one-dimensional expression introduced here cannot simply be applied independently to every coordinate of an arbitrary skewed cell. Understanding the cubic case already explains why density, neighbour distances, and displayed positions must all be interpreted together with the boundary conditions.

## Calculate neighbours directly and handle distant charges collectively

Pairing every particle with every other particle at every step becomes expensive as a system grows. For some interactions that decay sufficiently rapidly, a defined short-range region can be calculated explicitly while farther contributions are treated according to the model and algorithm. A cutoff is therefore part of a computational division of work. It is not a distance at which an atom’s influence abruptly ceases in nature. This example uses a 1-nanometre short-range LJ cutoff together with a long-range dispersion correction to energy and pressure. Such a correction assumes an approximately homogeneous far environment, a condition worth remembering when moving from uniform water to strongly heterogeneous interfaces.

A neighbour list further reduces repeated searching. The program first identifies pairs that may enter the interaction range and reuses that information for several subsequent steps. To accommodate motion, the list typically extends beyond the actual short-range interaction cutoff. Imagine a delivery service maintaining a list of addresses surrounding its service area. An address outside the wider list is unlikely to enter the service region during a short interval; an address on the list does not necessarily require delivery at every instant. The interaction cutoff defines where the explicit short-range calculation applies, while the buffer helps the list retain relevant neighbours between updates.

For the present comparison, the neighbour-list radius is fixed at 1.2 nanometres, the short-range interaction radii remain 1 nanometre, and both branches update the list every 10 steps. This avoids an additional change in automatically selected buffer sizes when the time step changes. Ten steps nevertheless represent 10 femtoseconds in one branch and 20 femtoseconds in the other. We have therefore fixed the update rule in integration steps, rather than matching the physical interval exactly. A further comparison could update the 1-femtosecond branch every 20 steps to match physical time. Stating the actual conditions precisely makes the existing result interpretable and suggests a focused next calculation.

Electrostatic interactions decay more slowly, so discarding them all beyond a simple cutoff can produce substantial errors. Particle-mesh Ewald, or PME, separates the periodic electrostatic calculation into a short-range contribution suitable for direct evaluation and a smooth long-range contribution suitable for a grid calculation. The PME method introduced by Darden, York, and Pedersen in 1993 improved the efficiency of long-range electrostatics through a mesh and fast Fourier transforms. This mesh is a numerical device. Water molecules still move through continuous space; their charge information is mapped to the mesh as part of calculating the long-range contribution.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g04/en/#en-s5)

Figure 3 · Conceptual PME division: direct short-range and mesh-based long-range calculations jointly describe periodic electrostatics.

Consequently, setting coulombtype to PME and rcoulomb to 1.0 does not discard charges beyond 1 nanometre. That distance participates in the division between real-space and mesh-based work. Mesh spacing, interpolation order, and accuracy tolerances also influence the numerical calculation. Initially, it is enough to recognize PME as a method for retaining periodic long-range electrostatics, then learn its precision controls as a research question demands them. When changing those controls, examine the effects on energies, forces, or the chosen observable alongside the change in computational cost. Extra precision becomes useful when it addresses the quantity you actually need.

The short labels in an input file now describe a connected calculation. pbc defines repeated space; PME treats its long-range charge interactions; rvdw specifies the explicit LJ short-range extent; rlist and nstlist organize neighbour searching; dt sets the temporal update interval. Each can influence a result through a different mechanism. When a curve looks unexpected, following these relationships is more informative than changing many parameters simultaneously. For example, a starting structure with severe overlaps first needs geometric preparation. Increasing the precision of the mesh calculation does not address the inappropriate initial arrangement that created those large forces.

## Start both branches from the same prepared state

The comparison uses one NPT endpoint structure and checkpoint, retaining the 884 molecules, topology, charges, interaction parameters, and prepared velocity state. Temperature and pressure coupling are then switched off, and the volume is held fixed while energy behaviour is examined. This NVE setup has a specific diagnostic purpose. Without continuing exchange with a heat bath or pressure bath, changes in the system’s total energy are easier to inspect. Instantaneous temperature still fluctuates as kinetic and potential energy exchange. The primary diagnostic is therefore total energy, rather than a requirement that every instantaneous temperature equal 300 kelvin.

The two inputs below preserve the settings used in the actual comparison. The 1-femtosecond branch uses dt of 0.001 picoseconds and 100000 steps; the 2-femtosecond branch uses 0.002 picoseconds and 50000 steps. Both thus cover 100 picoseconds. gen-vel is no, so new random velocities are not generated when branching. continuation is yes and the checkpoint supplies the continuing state. Both temperature and pressure coupling are disabled. The neighbour-list parameters follow the choices just discussed. The files are deliberately similar because a controlled comparison concentrates changes in conditions specified in advance.

### Complete input for the 1 fs branch

```
integrator = md
dt = 0.001
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 100
nstenergy = 100
nstlog = 100
cutoff-scheme = Verlet
nstlist = 10
coulombtype = PME
rcoulomb = 1.0
vdwtype = Cut-off
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
constraints = h-bonds
constraint-algorithm = lincs
nsteps = 100000
verlet-buffer-tolerance = -1
rlist = 1.2
continuation = yes
tcoupl = no
pcoupl = no
gen-vel = no
```

Continue the NPT state for 100 ps at fixed volume without temperature coupling, retaining the comparison’s fixed neighbour-list settings.

### Complete input for the 2 fs branch

```
integrator = md
dt = 0.002
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 100
nstenergy = 100
nstlog = 100
cutoff-scheme = Verlet
nstlist = 10
coulombtype = PME
rcoulomb = 1.0
vdwtype = Cut-off
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
constraints = h-bonds
constraint-algorithm = lincs
nsteps = 50000
verlet-buffer-tolerance = -1
rlist = 1.2
continuation = yes
tcoupl = no
pcoupl = no
gen-vel = no
```

The physical duration is unchanged while the step and number of steps change.

Run the shell script in the prepared water directory containing npt.gro, npt.cpt, and topol.top. These files come from the complete preparation procedure shown in the preceding chapter: coordinates, the state needed for continuation, and molecular composition with its parameter connections. The script creates and runs a separate input for each branch, then exports potential energy, kinetic energy, total energy, and temperature. The -t option of grompp reads the checkpoint, while -c supplies the structure coordinates; their functions are related but distinct. The example uses CPU execution and a consistent parallel configuration to preserve the execution choices of this comparison.

### Run both branches and export energies

```
#!/usr/bin/env bash
set -euo pipefail
# Start in the prepared water case containing npt.gro, npt.cpt, topol.top,
# nve-1fs.mdp and nve-2fs.mdp. G03 displays the complete preparation inputs.
for branch in 1fs 2fs; do
    gmx grompp -f "nve-${branch}.mdp" -c npt.gro -t npt.cpt -p topol.top -o "nve-${branch}.tpr"
    gmx mdrun -deffnm "nve-${branch}" -ntmpi 1 -ntomp 4 -pin off
    printf 'Potential\nKinetic-En.\nTotal-Energy\nTemperature\n0\n' | gmx energy -f "nve-${branch}.edr" -o "nve-${branch}-energy.xvg"
done
python compare_nve.py . --output figures --language en
```

Run in the directory with the preceding chapter’s prepared NPT state and topology, together with the two MDP files and the analysis script.

The Python analysis reads the legend associated with each XVG column and identifies Total Energy by its name rather than assuming a fixed column number. It then checks both time records and identifies saved times shared by the files. The original records contain 1001 and 501 measurements, respectively. Their common grid contains 501 points from 0 through 100 picoseconds at 0.2-picosecond intervals. The procedure selects existing measurements without interpolating additional values between frames. A CSV retains the energy changes and residuals at each shared time, making details in the plots available for independent inspection or alternative plotting.

Separate energy changes into a linear trend and residual amplitudeEq. 3

![Separate energy changes into a linear trend and residual amplitude](https://ml-biomat.com/static/agent-math/8cdb58bbc54f1396f470f1d5.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| E(tk), E(0) | Total energy at saved time tk and at this branch’s start | kJ mol⁻¹ |
| ΔEk | Energy change at saved point k relative to this branch’s start | kJ mol⁻¹ |
| tk | Common saved time k | ps |
| a | Intercept of the least-squares straight-line fit of ΔE against time | kJ mol⁻¹ |
| b | Slope of the same fit describing linear drift over the window | kJ mol⁻¹ ps⁻¹ |
| R | Root-mean-square residual after subtracting the fitted line | kJ mol⁻¹ |
| n, k | n is the number of common times, 501 here; k indexes records, beginning at time 0 ps | dimensionless |
| Σ, √, ², /, −, +, =, [ ], × | Sum all records; square residuals, divide by n, and take the square root; subtract initial value and trend; addition forms the line; equality defines quantities; group terms; multiply adjacent factors | operators have no units |

Reading the relationshipReferencing each branch to its own start separates discrete energy baselines. Least squares chooses a and b to minimize squared residuals; R measures their amplitude and describes a different feature from b.

A worked exampleFor three fitted residuals of −1, 2, and −1 kJ mol⁻¹, R=√[(1+4+1)/3]=√2≈1.414 kJ mol⁻¹. A fitted slope of −0.1 kJ mol⁻¹ ps⁻¹ gives a 10 kJ mol⁻¹ decrease along the fitted line over 100 ps.

ConditionsThese describe a specified window. The denominator n defines RMS rather than a degrees-of-freedom correction for estimating noise variance. These metrics do not by themselves supply confidence intervals for correlated trajectories.

The straight-line fit is descriptive: it summarizes a gradual trend across the full window, while the root-mean-square residual quantifies fluctuations around that line. The slope carries an inverse-time factor, distinguishing a total change from a rate of change. The residual RMS retains energy units and describes a separate feature of the numerical record. The program does not interpret the 501 times as independent experiments or construct a confidence interval from their count. The language option changes the plot labels while preserving the data selection and calculations. This allows the two language versions to present exactly the same numerical comparison.

### Compare drift and fluctuations at shared saved times

```
#!/usr/bin/env python3
"""Compare real 1 fs / 2 fs water records on their common saved-time grid.

python compare_nve.py RUN_DIRECTORY --output figures --language en
Dependencies: numpy, matplotlib.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def read_energy(path):
    legends, rows = {}, []
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('@'):
            match = re.match(r'@\s+s(\d+)\s+legend\s+"([^"]+)"', line)
            if match:
                legends[int(match[1])] = re.sub(r'[^a-z]', '', match[2].casefold())
            continue
        if line == '&':
            raise ValueError('One XVG dataset per file is required.')
        rows.append([float(value) for value in line.split()])
    values = np.asarray(rows)
    matches = [index + 1 for index, name in legends.items() if name == 'totalenergy']
    if len(matches) != 1 or values.ndim != 2 or len(values) < 3:
        raise ValueError('Missing or ambiguous Total Energy column.')
    if matches[0] >= values.shape[1] or not np.all(np.isfinite(values)):
        raise ValueError('Invalid energy table.')
    time, energy = values[:, 0], values[:, matches[0]]
    if np.any(np.diff(time) <= 0):
        raise ValueError('Saved times must increase strictly.')
    return time, energy


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_directory', type=Path)
    parser.add_argument('--output', type=Path, default=Path('figures'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    labels = ['1 fs', '2 fs']
    raw = [read_energy(args.run_directory / f'nve-{step}fs-energy.xvg') for step in (1, 2)]
    # XVG times here have six decimal places; verify rounded times remain unique.
    rounded = [np.round(time, 6) for time, _ in raw]
    if any(len(np.unique(time)) != len(time) for time in rounded):
        raise ValueError('Time rounding merged distinct saved frames.')
    common = np.intersect1d(*rounded)
    if len(common) < 3:
        raise ValueError('Too few common saved times for comparison.')
    changes, trends, residuals, summary = [], [], [], {}
    for label, (time, energy), grid in zip(labels, raw, rounded):
        indices = np.searchsorted(grid, common)
        if not np.allclose(time[indices], common, atol=5e-7, rtol=0):
            raise ValueError('Common-grid matching failed.')
        selected = energy[indices]
        change = selected - selected[0]
        slope, intercept = np.polyfit(common, change, 1)
        trend = intercept + slope * common
        residual = change - trend
        changes.append(change)
        trends.append(trend)
        residuals.append(residual)
        summary[label] = {
            'original_samples': int(len(time)), 'common_samples': int(len(common)),
            'start_ps': float(common[0]), 'end_ps': float(common[-1]),
            'drift_kJ_mol_ps': float(slope),
            'residual_rms_kJ_mol': float(np.sqrt(np.mean(residual ** 2))),
            'end_minus_start_kJ_mol': float(change[-1]),
            'initial_energy_kJ_mol': float(selected[0]),
        }
    zh = args.language == 'zh'
    plt.rcParams.update({'font.family': ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC', 'WenQuanYi Zen Hei', 'DejaVu Sans'],
                         'font.size': 14, 'axes.spines.top': False,
                         'axes.spines.right': False, 'svg.fonttype': 'path',
                         'axes.unicode_minus': False})
    colors = ['#147d92', '#c56a32']
    fig, axes = plt.subplots(2, 2, figsize=(13.5, 8.8), constrained_layout=True)
    for i, label in enumerate(labels):
        axes[0, 0].plot(common, changes[i], color=colors[i], lw=1.2, alpha=.85, label=label)
        axes[0, 0].plot(common, trends[i], color=colors[i], lw=2.1, ls='--')
        axes[1, 0].plot(common, residuals[i], color=colors[i], lw=1.0, label=label)
    axes[0, 0].set(title='相对于各自起点的能量变化' if zh else 'Energy change from each branch’s own start',
                   xlabel='时间 / ps' if zh else 'Time / ps', ylabel='ΔE / kJ mol⁻¹')
    axes[1, 0].set(title='去除线性趋势后的波动' if zh else 'Fluctuations after removing the linear trend',
                   xlabel='时间 / ps' if zh else 'Time / ps', ylabel='残差 / kJ mol⁻¹' if zh else 'Residual / kJ mol⁻¹')
    for ax in axes[:, 0]:
        ax.legend(frameon=False)
        ax.grid(alpha=.16)
    drift = [summary[label]['drift_kJ_mol_ps'] for label in labels]
    rms = [summary[label]['residual_rms_kJ_mol'] for label in labels]
    axes[0, 1].bar(labels, drift, color=colors, width=.52)
    axes[0, 1].axhline(0, color='#333333', lw=.8)
    axes[0, 1].set(title='整个100 ps窗口的线性漂移' if zh else 'Linear drift over the full 100 ps window',
                   ylabel='斜率 / kJ mol⁻¹ ps⁻¹' if zh else 'Slope / kJ mol⁻¹ ps⁻¹')
    axes[0, 1].set_ylim(min(drift) * 1.35, .035)
    for i, value in enumerate(drift):
        axes[0, 1].text(i, value - .012, f'{value:.4f}', ha='center', va='top')
    axes[1, 1].bar(labels, rms, color=colors, width=.52)
    axes[1, 1].set(title='去趋势均方根幅度' if zh else 'Root-mean-square residual amplitude',
                   ylabel='RMS / kJ mol⁻¹', ylim=(0, max(rms) * 1.25))
    for i, value in enumerate(rms):
        axes[1, 1].text(i, value + .045, f'{value:.3f}', ha='center', va='bottom')
    fig.savefig(args.output / 'nve_comparison.svg')
    fig.savefig(args.output / 'nve_comparison.png', dpi=170)
    plt.close(fig)
    with (args.output / 'nve_common_grid.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream)
        writer.writerow(['time_ps', 'deltaE_1fs_kJ_mol', 'deltaE_2fs_kJ_mol',
                         'residual_1fs_kJ_mol', 'residual_2fs_kJ_mol'])
        writer.writerows(zip(common, *changes, *residuals))
    report = {'definition': 'Each branch referenced to its own initial energy; least-squares line and population RMS of its residual on common saved times; no interpolation.',
              'time_grid_ps': float(np.median(np.diff(common))), 'branches': summary}
    (args.output / 'nve_summary.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
```

Requires NumPy and Matplotlib. Reads actual XVG records and saves labelled plots, a common-time CSV, and JSON metrics. Measurements are selected on shared times without interpolation.

## Smaller fast fluctuations can coexist with greater slow drift

Begin with the upper-left energy-change plot. Each curve has its own initial total energy subtracted, so both start at zero. Dashed lines show least-squares fits across the full 100-picosecond window. Both curves gradually descend, but at different rates. In this calculation, the 1-femtosecond branch has a fitted slope of approximately −0.2287 kilojoules per mole per picosecond, compared with −0.0956 for the 2-femtosecond branch. The negative sign describes a gradual decrease according to the stated energy definition. The molar unit follows the GROMACS convention for the system energy; these values have not additionally been divided by 884 to obtain an average per mole of water molecules.

### NVE energy comparison at 1 fs and 2 fs

884 rigid SPC/E water molecules from the same NPT starting state; 100 ps per branch, compared on 501 shared times at 0.2 ps intervals. Curves use each branch’s own initial energy and dashed lines fit the full window.

GROMACS 2026.4; 884 SPC/E waters in an initially 3 nm cubic box, with targets of 300 K and 1 bar. The NPT record spans 100 ps and descriptive statistics use 50–100 ps; the player shows a separate 100 ps NVE stage.

[Download reference data and complete inputs (ZIP) 1.82 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-water-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g04/en/#en-s7)

Two 100 ps NVE branches compared at their 501 common saved times, each referenced to its own initial total energy. The fitted slope describes drift over this record; the lower panels show fluctuations after removing each fitted line, using the population root-mean-square definition.

| Quantity | Value | Unit |
| --- | --- | --- |
| 1 fs energy drift on the common time grid | -0.228706 | kJ mol⁻¹ ps⁻¹ |
| 1 fs detrended energy RMS | 0.488938 | kJ mol⁻¹ |
| 2 fs energy drift on the common time grid | -0.095561 | kJ mol⁻¹ ps⁻¹ |
| 2 fs detrended energy RMS | 1.910275 | kJ mol⁻¹ |

The lower-left plot subtracts each fitted line and reveals a narrower band of fluctuations for the 1-femtosecond branch. Its residual RMS is approximately 0.489 kilojoules per mole, whereas the 2-femtosecond branch gives approximately 1.910. This behaviour is consistent with a finer temporal description reducing fast integration-related fluctuations. It also demonstrates why a single number called “energy error” can omit important information. In this comparison, reducing the time step lowered the detrended fluctuation amplitude while increasing the magnitude of the slow fitted drift. Both observations belong to the same records and deserve an explanation together.

Energy drift depends on more than time discretization. Force approximations, neighbour-list updates, constraint calculations, and floating-point arithmetic also contribute. Over a fixed physical duration, the smaller-step branch performs more updates, allowing numerical rounding and algorithmic details to accumulate along a different trajectory. Many-body motion also causes initially nearby trajectories to separate. Different atomic positions after 100 picoseconds therefore do not, by themselves, identify a program failure. Defined statistical observables and numerical diagnostics provide more useful comparisons than requiring every atom to occupy matching positions at every time.

A sequence of focused comparisons can investigate the slow drift further. Keep the model and starting state fixed while first matching the physical neighbour-list update interval. Separately change the precision of the long-range electrostatic calculation or constraint treatment. If very accurate energy conservation is central to the research question, compare arithmetic precision as well. Preserve the analysis window and metric definitions in each comparison. This creates a sequence of evidence that narrows the causes of a numerical feature, rather than changing many settings at once and selecting whichever curve appears flattest.

The plots also illustrate why axis choices should follow the question. Showing total energy on a very broad vertical scale that includes zero can make changes of tens of kilojoules per mole nearly invisible. Subtracting the starting value reveals those changes clearly. Conversely, an extremely narrow vertical scale can make a small fluctuation look dramatic. The figure therefore accompanies the curves with units, the observation window, slopes, and residual amplitudes. Visual impressions can then be related to specified quantities. The CSV allows you to redraw the results or choose another physically motivated window and examine how the finite observation scale affects the description.

## Carry numerical checks into a molecular research question

Return to the map and its update frequency. A force field describes matter; the time step propagates that description; boundaries and long-range treatment define its computational environment; sampling duration determines how much motion is observed. These choices cooperate in a simulation while answering different questions. Agreement of density with an experimental measurement can inform evaluation of one model property. NVE energy behaviour diagnoses numerical propagation. Whether a polymer adequately explores extended and compact states concerns conformational sampling. Connecting these forms of evidence makes a simulation conclusion specific to the molecular question being asked.

For example, studying whether a PEG chain is more extended or compact in water first requires a coherent description of PEG–water interactions. Check that its bonds and constraints support stable integration at the chosen time step. Then examine whether distances to periodic images suit the conformations being explored. Finally, assess whether chain dimensions and contact distributions receive adequate sampling across time segments and initial conditions. A halved time step does not make a short trajectory cross every conformational barrier. A longer trajectory does not automatically improve an unsuitable interaction model. Each computational change is most informative when connected to a question with an observable answer.

A useful exercise requires no additional simulation: identify the options in the two MDP files that describe matter, temporal propagation, the spatial environment, and output recording, and explain their roles. Next, use the same CSV to analyse 0–50 and 50–100 picoseconds separately. Recalculate slopes and residuals to examine how a finite window influences the summary. A subsequent simulation exercise can change one setting for a stated purpose while preserving original inputs, software version, and analysis definitions. These records make later differences traceable to models or methods rather than dependent on recollection.

The next chapter applies this reasoning to a protein. An experimental structure supplies atomic positions, while constructing a model additionally requires identifying the protein atoms, adding hydrogens, and specifying termini and charged groups. The force field becomes a set of rules for a complex chemical structure. The sequence of questions remains useful: establish the molecule and its environment, determine how they are propagated, and interpret the motion through suitable observables. Reading an input file in this way connects a collection of accepted software options to the physical system those options collectively represent.

## Further Reading and Open Materials

- [GROMACS tutorial 1: Water](https://gaseri.org/en/tutorials/gromacs/1-tip4pew-water/) · Wes Barnett; Vedran Miletić · CC BY-SA 4.0 (English tutorials)

  Foundation for periodic-water parameter choices and staged preparation.

  Adapts the TIP4P/Ew workflow to SPC/E at 300 K and 1 bar; adds a common-start 1 fs/2 fs NVE comparison, bilingual explanation, and independent analysis. Workflow adaptations retain CC BY-SA 4.0.
- [Computer Experiments on Classical Fluids. I. Thermodynamical Properties of Lennard-Jones Molecules](https://doi.org/10.1103/PhysRev.159.98) · Loup Verlet · Scientific citation; no reused figure

  Historical context for 1967 classical-fluid simulation and temporal propagation.

  Timing diagram and explanation independently created.
- [Particle mesh Ewald: An N·log(N) method for Ewald sums in large systems](https://doi.org/10.1063/1.464397) · Tom Darden; Darrin York; Lee Pedersen · Scientific citation; no reused figure

  Historical and computational context for the 1993 PME method.

  Independent short-range/long-range conceptual diagram.
- [GROMACS 2026.4: nonbonded-interactions](https://manual.gromacs.org/2026.4/reference-manual/functions/nonbonded-interactions.html) · GROMACS developers · Technical reference

  Technical definitions of interactions, periodic geometry, and integration.

  Independent explanations and worked examples for this system.
- [GROMACS 2026.4: periodic-boundary-conditions](https://manual.gromacs.org/2026.4/reference-manual/algorithms/periodic-boundary-conditions.html) · GROMACS developers · Technical reference

  Technical definitions of interactions, periodic geometry, and integration.

  Independent explanations and worked examples for this system.
- [GROMACS 2026.4: molecular-dynamics](https://manual.gromacs.org/2026.4/reference-manual/algorithms/molecular-dynamics.html) · GROMACS developers · Technical reference

  Technical definitions of interactions, periodic geometry, and integration.

  Independent explanations and worked examples for this system.
