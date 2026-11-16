# From preparation to sampling: adapting a protein to water

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g07/en/
Language: en

Use restraints, checkpoints, and actual temperature and pressure records to distinguish geometrical relaxation, environmental adjustment, and protein motion.

## Starting the motion of a newly assembled system

After several liquids are poured into one container, their mixture needs time to reach a common temperature and adjust its distribution. A molecular simulation begins with a related problem. We have placed ubiquitin, water, and ions in a box, but their coordinates came from structure preparation, a solvent template, and randomized replacement. They have not yet adjusted together under the selected interactions. Treating all motion immediately after the first frame as the protein behavior of interest would mix initial relaxation into the result. This chapter follows energy minimization, temperature preparation, volume preparation, and sampling after removal of position restraints, using actual curves to understand each stage.

Preparation has several distinct levels. Closely overlapping atoms can experience strong repulsion and first need positional adjustment. A reasonable geometry then needs velocities so that the system moves near the intended temperature. Cell volume must also adapt to the pressure environment. These processes have different timescales: local vibrations can be rapid, whereas protein rotation, flexible-tail rearrangements, and crossing conformational barriers may take much longer. Distinguishing these levels prevents one vague statement about “equilibration” from replacing separate assessments of geometry, temperature, volume, and conformational sampling.

Our sequence starts from one minimized structure, runs 100 ps of constant-volume temperature preparation, follows with 200 ps of pressure-coupled preparation, and then records 1 ns of production without position restraints. A picosecond is 10⁻¹² s, and 1 ns equals 1000 ps. The dynamics time step is 0.002 ps, or 2 fs, so 100 ps requires 50000 integration steps and 1 ns requires 500000. An integration step is the interval used to advance the computational state. A trajectory-output interval determines which of those states are saved as frames. These intervals serve different purposes and need not be equal.

The composition continues from the preceding chapter: 76-residue ubiquitin from 1UBQ, AMBER99SB-ILDN protein parameters, 5868 TIP3P waters, and 17 each of Na⁺ and Cl⁻. The termini and His68 retain their specified chemical states. This classical model describes local conformation and solvent adjustment at fixed chemical composition; bonding reactions and proton transfer require a suitable alternative description. Initial geometrical preparation, temperature and pressure control, and subsequent structural analysis all refer to this same defined molecular system.

During the first two dynamics stages, ubiquitin's heavy atoms experience elastic restoring forces toward reference positions. This allows water and ions to adjust around a relatively stable protein shape. Production removes these additional forces while retaining the molecular force field and temperature and pressure control. The change must be visible in the inputs and figures: restrained and freely moving protein fluctuations are sampled under different potential-energy conditions. We inspect both preparation and production, but interpret each according to its physical settings.

This workflow supplies a starting point for studying protein conformation, interactions, and solvation. It also helps diagnose common problems: unreasonable contacts, accidentally regenerated velocities, an incorrect reference structure, or a still-adjusting volume reported as a stationary average. Understanding the physical causes is more useful than memorizing a universal preparation duration. Later chapters on trajectory analysis and independent replicas will examine slower structural changes. Here we turn a compositionally consistent box into a dynamical system with defined conditions and interpretable records.

[Figure: Four-stage protein preparation](https://ml-biomat.com/tutorials/molecular-dynamics/g07/en/#en-s1)

Figure 1 · Minimization uses optimization steps; subsequent stages use physical dynamics time. Position restraints are active in the two preparatory dynamics stages.

## Molecules still move around an energy minimum

The first three-dimensional protein structures were naturally represented as definite shapes. Such images reveal folds and chemical groups effectively, while compressing molecular motion into a single view. In 1977, McCammon, Gelin, and Karplus studied molecular dynamics of bovine pancreatic trypsin inhibitor, following fluctuations within a folded protein using an empirical potential and atomic equations of motion. They asked how atoms moved around an average structure, how their motions were correlated, and how those correlations decayed. This extended the structural question from “what shape is present?” to “what activity occurs around that shape?”

A folded protein can preserve its overall architecture while side chains rotate, loops move, and internal atoms undergo correlated displacements. A suspension bridge similarly remains a bridge while vibrating under wind and passing traffic. Proteins have no macroscopic supporting frame; their shapes emerge from many molecular interactions. The useful part of the analogy is the distinction between structural persistence and complete immobility. An average structure does not require every component to occupy the same position at every instant. These motions and their distributions are among the quantities a simulation can examine.

Energy minimization addresses a different question. Given coordinates and a potential-energy function, an optimization algorithm moves atoms in directions that lower the potential until a specified force or convergence criterion is met. Walking downhill toward a nearby valley captures the idea: the procedure can remove unfavorable starting contacts without automatically crossing every ridge to find the lowest point in the entire landscape. A macromolecule's potential depends on many coordinates and usually contains many local minima. We therefore use minimization to prepare geometry, while subsequent dynamics and sampling determine which states the protein visits at finite temperature.

Temperature-control methods also developed from targeting a number toward sampling a distribution. In 2007, Bussi, Donadio, and Parrinello introduced stochastic velocity rescaling, using a carefully chosen random component while adjusting kinetic energy to sample the canonical distribution. In 2020, Bernetti and Bussi developed stochastic cell rescaling, retaining volume fluctuations compatible with pressure-controlled sampling alongside relaxation of the average pressure. The v-rescale and C-rescale methods used here connect to these developments. Their target temperature and pressure describe the environment, while the instantaneous state retains thermal fluctuations.

An equilibrated trace is therefore normally a fluctuating band rather than a straight line pinned to a target. A finite system associated with a 300 K heat bath has an instantaneous temperature that changes, and a small cell at a 1 bar reference pressure can show wide pressure fluctuations. Interpretation asks whether a persistent trend remains, which time interval defines an average, how fluctuations are quantified, and which potential was active. These questions bring the historical insight into practical analysis: the aim is to understand the statistics of motion, rather than tune motion into a static picture.

[Figure: History of protein motion and temperature-pressure sampling](https://ml-biomat.com/tutorials/molecular-dynamics/g07/en/#en-s2)

Figure 2 · The 1977 protein simulation examined fluctuations around an average structure. Later stochastic coupling methods incorporated distributions and fluctuations into sampling. Curves and cells are conceptual schematics.

## Relax close contacts before assigning physical time

Repulsive interactions change steeply at short separation. A newly inserted water too close to a protein atom may therefore experience a force much larger than those typical of ordinary thermal motion. A large integration step can move atoms too far before the next force evaluation, leaving constraints and subsequent calculations with unfavorable geometry. Steepest descent uses the current force direction to seek lower potential energy and adjusts attempted displacements before dynamics begins. Here emstep=0.001 nm sets the scale of an optimization displacement; it is neither a velocity nor a physical time increment.

For this geometrical preparation, we use the supplied flexible-water bond and angle definitions with constraints=none. Internal water geometry and solvent contacts can then relax together. Dynamics restores the rigid TIP3P geometry handled by SETTLE, while LINCS constrains protein bonds involving hydrogen. The stages consequently have different internal degrees of freedom and potential terms. Their energies should be interpreted under their respective settings rather than joined into a single conservation trace for an unchanged potential. Understanding this transition helps explain why geometrical preparation and finite-temperature dynamics have different purposes.

The minimization setting emtol=500 requests a maximum atomic force below 500 kJ mol⁻¹ nm⁻¹. This is the largest force magnitude among all atoms, making it useful for identifying a remaining locally stressed region. The setting nsteps=50000 is a limit on attempted optimization steps; meeting the criterion can stop the process earlier. The actual run converged after 1704 attempts with a maximum force of approximately 452.11 kJ mol⁻¹ nm⁻¹. Its last recorded step number is 1703. Numbering begins at zero, and rejected attempts need not produce an energy record, so record count, final step label, and attempted steps are distinct quantities.

### Flexible geometrical minimization

```
integrator = steep
define = -DFLEXIBLE
constraints = none
emtol = 500
emstep = 0.001
nsteps = 50000
nstenergy = 20
cutoff-scheme = Verlet
nstlist = 20
coulombtype = PME
rcoulomb = 1.0
fourierspacing = 0.12
ewald-rtol = 1e-5
vdwtype = Cut-off
vdw-modifier = Potential-shift
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
```

For the salted solution. FLEXIBLE enables flexible-water preparation; dynamics restores rigid water.

The potential falls from approximately −3069.56 to −319180.06 kJ/mol, rapidly at first and more gradually later. The large negative value is the sum of the relevant interactions throughout the protein solution, with a zero set by the potential convention. Absolute total energy changes with system size and composition. Comparing totals for differently sized systems therefore does not directly rank protein stability. Within this minimization, the trace reveals geometrical relaxation, while the log reports whether the requested maximum-force criterion was reached.

Physical dynamics time begins after minimization. At the NVT starting point, gen-vel=yes generates velocities using a 300 K target distribution and a fixed random seed. Constraints reduce the available independent motions, and the program accounts for this in its temperature degrees of freedom. Positions and velocities then evolve together: kinetic energy can become potential energy, and the heat bath exchanges energy with the system. Velocity generation defines an initial state. Setting gen-temp to 300 K does not make every subsequent temperature record equal to 300 K.

In the actual example, the initial temperature is about 300.56 K, the saved value at 0.2 ps falls to about 166.29 K, and the preparation then returns toward the target. This early change occurs as the prepared geometry begins constrained dynamics and has a different interpretation from the later fluctuations. Keeping the full trace makes that preparation visible. Over the later 50–100 ps interval, the recorded mean is approximately 300.06 K and the sample standard deviation is about 2.34 K. The requested temperature and measured trajectory supply separate, complementary information.

## Position restraints act like springs; constraints fix geometry

Restraints and constraints sound similar but implement different operations in molecular dynamics. A position restraint adds a potential-energy term: moving farther from a reference position usually produces a larger restoring force. The atom can still move, with its displacement determined by the restraint and the surrounding interactions. A bond constraint requires a pair distance to satisfy a specified value, with the integration algorithm correcting the geometry to numerical precision. The first changes the energy landscape; the second changes the allowed degrees of freedom. Both can be active simultaneously while serving different purposes.

Imagine a ball attached by a spring to a point on a wall. The ball can move away, while the spring pulls it back increasingly strongly. Replacing the spring with a fixed-length rod allows motion around the attachment point but fixes the separation. Atomic coordinates are more complex, yet this distinction helps interpret the input: POSRES activates additional positional restoring terms, whereas constraints=h-bonds converts bonds involving hydrogen to fixed-length conditions. Removing POSRES later preserves the protein's chemical connectivity and its bond constraints.

[Figure: Spring restraint and fixed-length connection](https://ml-biomat.com/tutorials/molecular-dynamics/g07/en/#en-s4)

Figure 3 · A position restraint supplies a restoring force on displacement, while a bond constraint maintains a pair distance. x is current position, x₀ the reference, and r₀ the specified distance.

For the equal restraint strength used along all directions here, the added energy depends quadratically on displacement from the reference. Doubling displacement quadruples the energy and doubles the restoring-force magnitude. This quadratic form is common for small displacements and has an intuitive work interpretation: pulling farther requires an increasing force, so accumulated work rises faster than distance. The following expressions give the restraint energy and force along one coordinate, connecting their numerical values to the direction of motion.

Position restraint along one coordinateEq. 1

![Position restraint along one coordinate](https://ml-biomat.com/static/agent-math/4e69228cb98d44164bc7b4b3.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| x, x₀ | Current and reference atomic coordinates; subscript 0 identifies the reference | nm |
| Δx | Signed coordinate difference; positive when the current coordinate exceeds the reference | nm |
| U_{r} | Added restraint energy for one atom along this coordinate; r denotes restraint | kJ/mol |
| k | Restraint force constant controlling the response to a given displacement | kJ mol⁻¹ nm⁻² |
| F_{x} | x component of the restraint force; subscript x identifies the direction | kJ mol⁻¹ nm⁻¹ |
| Δ, =, −, ½, ², × | Δ denotes a difference; equality relates quantities; subtraction gives the displacement; the leading minus directs force toward the reference; ½ is one half; the square multiplies a quantity by itself; adjacent factors multiply | Notation and operations; no units |

Reading the relationshipA restoring force proportional to displacement gives a quadratic energy when work is accumulated. The negative sign directs the force back toward the reference.

A worked exampleFor k=1000 kJ mol⁻¹ nm⁻² and Δx=0.05 nm, U_r=½×1000×0.05²=1.25 kJ/mol and F_x=−50 kJ mol⁻¹ nm⁻¹. At 0.10 nm the energy is 5 and force −100 in the same units.

ConditionsA harmonic restraint on one atom and one coordinate. The full restraint energy sums selected atoms and directions; other force-field interactions remain active.

Our preparation restrains 602 protein heavy atoms with a force constant of 1000 kJ mol⁻¹ nm⁻². Hydrogen atoms, water, and ions are outside this protein-heavy-atom restraint list. A 0.05 nm displacement along one direction adds 1.25 kJ/mol for that coordinate and produces a restoring-force magnitude of 50 kJ mol⁻¹ nm⁻¹. At 0.10 nm, these values become 5 kJ/mol and 100 kJ mol⁻¹ nm⁻¹. This calculation refers to one atom and one direction. The full protein restraint energy sums the selected atoms' contributions over all restrained directions.

Change one atom's coordinate displacement and inspect the added restraint energy and force.

[Figure: Harmonic position-restraint potential](https://ml-biomat.com/tutorials/molecular-dynamics/g07/en/#en-s4)

Analytical harmonic-restraint example. k=0 removes this added term while the molecule's other interactions remain.

The reference positions also matter. Both NVT and restrained NPT use -r em.gro in grompp, retaining the same minimized reference instead of silently redefining zero displacement at each stage. During NPT, refcoord-scaling=com moves the reference-coordinate center of mass with the cell scaling, while reference vectors relative to that center remain unscaled. This preserves the reference protein shape for the preparation. It also gives the restrained stage's pressure and virial a special dependence on reference-coordinate handling. We therefore reserve ordinary pressure-statistics interpretation for production after the position restraints have been removed.

The purpose of these restraints is to organize which parts of the system adjust during preparation. The atom selection, reference structure, and force constant should follow that purpose. If an experiment physically confines a molecule to a support, a restraint may instead belong to the final scientific model. For free ubiquitin in solution, the preparatory restraint is removed in production. Here md.mdp omits define=-DPOSRES, and the resulting unrestrained trajectory becomes our principal record of protein motion.

## Preparing temperature, pressure, and volume together

Temperature describes thermal motion collectively rather than the speed of one atom. At equal kinetic energy a heavier atom moves more slowly, and molecular constraints reduce independent motions. We must therefore relate the kinetic energy of a temperature-coupling group to its degrees of freedom. Our System group contains the whole solution. GROMACS calculates its degrees of freedom from particle count, bond constraints, rigid-water geometry, and treatment of overall translation. The classical relationship between kinetic energy and temperature provides a useful quantitative check.

Checking temperature from kinetic energyEq. 2

![Checking temperature from kinetic energy](https://ml-biomat.com/static/agent-math/0b3e0196bc87aae9d2c1eab6.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| T | Instantaneous temperature defined from the selected group's kinetic energy | K |
| K | Kinetic energy of the complete group in the GROMACS molar-energy convention | kJ/mol; this K is an energy variable, distinct from the temperature unit K |
| f | Degrees of freedom used for kinetic temperature, accounting for constraints and overall-motion treatment | Dimensionless |
| R | Gas constant, approximately 0.008314462618 kJ mol⁻¹ K⁻¹ | kJ mol⁻¹ K⁻¹ |
| =, 2, /, × | Equality, dimensionless factor 2, fraction-bar division, and multiplication of adjacent factors; divide twice the kinetic energy by all of fR | Operations and constant; no units |

Reading the relationshipAt equilibrium, each classical quadratic kinetic degree carries an average molar energy ½RT. The same relationship defines instantaneous kinetic temperature.

A worked exampleFor f=38371 and K=47833.17788 kJ/mol, T≈299.86234 K, matching the production mean over 500–1000 ps. With fixed degrees of freedom, this linear relation also applies to time means.

ConditionsClassical model, specified coupling group, and GROMACS molar-energy units. Constraints reduce degrees of freedom; a position restraint adds potential rather than directly removing a coordinate degree.

The actual System group has 38371 degrees of freedom. Its average kinetic energy during the later production interval is approximately 47833.18 kJ/mol. Combining these values with the gas constant gives about 299.86 K, agreeing with the reported mean temperature. GROMACS expresses the whole-cell energy using a molar energy convention, so this form uses the gas constant R. Using joules for a single physical cell instead would require the Boltzmann constant. Keeping the energy convention and units consistent is more reliable than memorizing a coefficient without its meaning.

NVT fixes particle count and cell volume while v-rescale exchanges energy with a 300 K heat bath, using tau-t=1 ps. This parameter sets a coupling timescale. It is neither a temperature-output interval nor a guarantee that preparation finishes in one picosecond. Local structures and solvent arrangements can continue adjusting after temperature approaches its target. We run 100 ps here and retain the full record to inspect early transients and later fluctuations. A different system requires a duration informed by its own curves and structural changes.

### 100 ps restrained NVT preparation

```
integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
nstenergy = 100
nstlog = 1000
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 300
cutoff-scheme = Verlet
nstlist = 20
coulombtype = PME
rcoulomb = 1.0
fourierspacing = 0.12
ewald-rtol = 1e-5
vdwtype = Cut-off
vdw-modifier = Potential-shift
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
define = -DPOSRES
nsteps = 50000
continuation = no
pcoupl = no
gen-vel = yes
gen-temp = 300
gen-seed = 20261121
ld-seed = 20261201
```

Uses the common minimized reference and generates this trajectory's initial velocities.

C-rescale pressure coupling is then enabled at a reference of 1 bar, with tau-p=5 ps. Isotropic scaling changes the overall cell size while preserving its shape relationships. The compressibility, 4.5×10⁻⁵ bar⁻¹, supplies the scale of volume response used in the coupling. For an approximately isotropic protein solution, this geometrical treatment is convenient. Membranes distinguish their plane from the normal direction and will use separately coupled directions later. The physical geometry of the environment therefore influences pressure-control settings.

### 200 ps restrained NPT preparation

```
integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
nstenergy = 100
nstlog = 1000
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 300
cutoff-scheme = Verlet
nstlist = 20
coulombtype = PME
rcoulomb = 1.0
fourierspacing = 0.12
ewald-rtol = 1e-5
vdwtype = Cut-off
vdw-modifier = Potential-shift
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
continuation = yes
gen-vel = no
define = -DPOSRES
refcoord-scaling = com
nsteps = 100000
ld-seed = 20261301
```

Continues the NVT state and scales the reference center of mass while retaining the reference protein shape.

The initial volume is approximately 193.424 nm³. During the later 100–200 ps of restrained NPT, its mean is approximately 189.422 nm³. The later 500–1000 ps of unrestrained production gives approximately 189.137 nm³, with a sample standard deviation of about 0.670 nm³. Preparation has allowed the same particles to occupy a slightly smaller volume. The production-window mean density is approximately 1012.09 kg/m³ and includes protein, ions, and water. An experimental comparison should therefore use a compositionally appropriate solution rather than treat the mixed-system density as pure-water density.

Unrestrained production pressure fluctuates widely: its later-window mean is approximately 2.45 bar and its sample standard deviation about 183.65 bar. In a small cell, instantaneous contributions from motion and molecular interactions can fluctuate far more than the reference pressure. The figure shows records every 1 ps together with 50 ps block means, distinguishing rapid variation from slower changes. Standard deviation measures the spread of saved records. Uncertainty in the mean also depends on time correlation, which Chapter 9 examines using correlation analysis and independent replicas.

Pressure is often introduced through molecules striking container walls: a greater average force per area gives a greater pressure. Periodic boundaries provide no physical wall, so the program calculates internal stress from particle motion and interactions, then obtains the reported scalar pressure from directional contributions. One bar equals 100000 Pa, and a pascal is a newton per square meter. Large kinetic and interaction contributions can partly cancel instantaneously, making a small-cell pressure record much more variable than a familiar pressure gauge. A gauge averages over macroscopic space and measurement time; the observation scales differ.

Constant-pressure sampling consequently does not force every saved frame to exactly 1 bar. The control method connects the cell to a pressure environment while retaining the allowed finite-system fluctuations. A negative instantaneous internal pressure corresponds to a tensile stress contribution at that moment and is interpreted through its duration, accompanying volume changes, and statistical distribution. Persistent deviations or anomalous contraction motivate checking the model and control conditions. Separating individual records, time averages, and external targets explains how a noisy-looking trace can still contain useful stationary statistical information.

## Continue the state rather than restart it at every stage

Coordinates capture only part of a dynamical state. Future motion also depends on velocities and the internal state of integration and coupling algorithms. A GROMACS checkpoint stores the information needed for continuation. When moving from NVT to NPT, we therefore supply both nvt.gro and nvt.cpt, set continuation=yes, and keep gen-vel=no. The second stage inherits the existing motion rather than drawing new velocities. Production likewise reads npt.cpt while removing the preparatory position restraints.

A coordinate frame resembles a photograph of traffic at a junction, while velocities tell us where each vehicle is going and how quickly. Identical positions can lead to different next moments if one vehicle is braking and another accelerating. A checkpoint retains more of the computational state than the photograph and is particularly useful for continuing dynamics. At a stage transition, we change explicitly selected conditions, such as enabling pressure control or removing restraints, while continuing the remaining state. This makes the purpose of each segment easier to interpret.

The output files have corresponding roles. XTC stores coordinate frames with a specified compression precision and is useful for viewing motion or measuring distances and shapes. EDR stores energy and state records that can be extracted by observable name. CPT retains the state needed for continuation. A frame extracted from XTC can provide coordinates for a new calculation, but using that frame differs from continuing the same dynamics through a checkpoint. Keeping analysis trajectories and checkpoints associated with their inputs supports both convenient inspection and continuation. This distinction also guides file retention: a compact movie is useful for reading a result, while restarting the calculation requires the appropriate state and model files.

The production input retains the 300 K and 1 bar environment, uses a 2 fs time step, and runs 500000 steps. Compressed coordinates are written every 500 steps, giving one frame per picosecond and 1001 frames including both endpoints. Production energy records are also spaced by 1 ps, whereas preparation energy records are saved every 0.2 ps. Analysis reads each file's actual time column. When displaying cumulative dynamics time, it explicitly adds the durations of earlier dynamics stages. Minimization step counts never enter this physical timeline.

### 1 ns production without position restraints

```
integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
nstenergy = 500
nstlog = 1000
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 300
cutoff-scheme = Verlet
nstlist = 20
coulombtype = PME
rcoulomb = 1.0
fourierspacing = 0.12
ewald-rtol = 1e-5
vdwtype = Cut-off
vdw-modifier = Potential-shift
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
continuation = yes
gen-vel = no
nsteps = 500000
ld-seed = 20261401
```

Continues the NPT state without POSRES, saving coordinates and energies every 1 ps.

The complete script below starts from the ion-containing coordinates and matching topology, runs each stage, and extracts the observables we will inspect. The setup directory contains the common minimization, and replica-1 contains the dynamics associated with this velocity seed. This organization distinguishes a shared minimized starting structure from one independently initialized trajectory and extends naturally to later replicas. Four computational threads are an execution choice in this example; the molecular model is defined by the topology and simulation inputs.

### Complete preparation and sampling workflow

```
#!/usr/bin/env bash
set -euo pipefail

# Start beside the solution coordinates, topology, and the four MDP files.
mkdir -p setup replica-1
gmx grompp -f em.mdp -c solvated-ions.gro -p topol.top -o setup/em.tpr
gmx mdrun -deffnm setup/em -ntmpi 1 -ntomp 4 -pin off
printf 'Potential\n0\n' | gmx energy -f setup/em.edr -o setup/em-potential.xvg
cp setup/em.gro topol.top posre.itp nvt.mdp npt.mdp md.mdp replica-1/
(
  cd replica-1
  gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
  gmx mdrun -deffnm nvt -ntmpi 1 -ntomp 4 -pin off
  gmx grompp -f npt.mdp -c nvt.gro -t nvt.cpt -r em.gro -p topol.top -o npt.tpr
  gmx mdrun -deffnm npt -ntmpi 1 -ntomp 4 -pin off
  gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr
  gmx mdrun -deffnm md -ntmpi 1 -ntomp 4 -pin off
  printf 'Temperature\n0\n' | gmx energy -f nvt.edr -o nvt-temperature.xvg
  printf 'Temperature\nPressure\nVolume\nDensity\n0\n' | gmx energy -f npt.edr -o npt-properties.xvg
  printf 'Temperature\nPotential\nKinetic-En.\nTotal-Energy\nPressure\nVolume\nDensity\n0\n' | gmx energy -f md.edr -o md-energy.xvg
)
python analyze_preparation.py . --output preparation-analysis --language en
```

Run beside the previous chapter's solvated-ions.gro, topol.top, and posre.itp, plus the four MDP files and analysis program here.

Inspect constraint deviations, maximum forces, energy records, and final times in the logs. A normally completed command establishes that a computational step finished. Scientific interpretation additionally checks the intended restraints, inherited state, and observables appropriate to the stage. To resume an interrupted segment, continue from its checkpoint rather than feed an already evolved coordinate file to gen-vel=yes and call the result a continuation. Regenerating velocities can be useful for independently initialized trajectories, but that is a separate, deliberate simulation design.

## Four panels answer four specific questions

The analysis program reads XVG legend labels before assigning data columns. This matters because energy-output ordering follows the available energy terms and may differ from the order in which names were entered. The program does not assume that requesting temperature first places temperature in the first data column. It treats the minimization abscissa as optimization steps and verifies each dynamics stage against its own duration. Identifying variables and axes first gives subsequent averages, fluctuations, and figures a consistent meaning.

Panel A plots decreasing minimization potential against optimization step. Panel B places 100 ps of NVT, 200 ps of restrained NPT, and 1000 ps of production on a cumulative dynamics timeline, with stage-specific colors. Panel C starts its clock at NPT preparation and marks restraint removal at 200 ps, showing volume adjustment across that transition. Panel D contains only unrestrained production pressure, preserving the raw fluctuations and adding explicitly defined block means. Each panel addresses one question rather than placing every available quantity on the same axis.

### Complete Python: read stages and plot results

```
"""Inspect the recorded preparation and production of ubiquitin replica 1."""
import argparse
import json
import re
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def xvg(path):
    legends, values = {}, []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r'@\s+s(\d+)\s+legend\s+"([^"]+)"', line)
        if match:
            legends[int(match[1])] = match[2]
        if line and not line.startswith(("#", "@")):
            values.append([float(x) for x in line.split()])
    a = np.asarray(values)
    return a[:, 0], {name: a[:, i+1] for i, name in legends.items()}


def stats(t, series, start, stop):
    select = (t >= start) & (t <= stop)
    return {"start_ps": start, "stop_ps": stop, "n_records": int(select.sum()),
            "observables": {name: {"mean": float(y[select].mean()),
                                   "sample_sd": float(y[select].std(ddof=1))}
                            for name, y in series.items()}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path,
                        help="Contains setup/ and replica-1/ subdirectories")
    parser.add_argument("--output", type=Path, default=Path("preparation-analysis"))
    parser.add_argument("--language", choices=("zh", "en"), default="en")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    em_t, em = xvg(args.directory / "setup/em-potential.xvg")
    rep = args.directory / "replica-1"
    tv, nvt = xvg(rep / "nvt-temperature.xvg")
    tp, npt = xvg(rep / "npt-properties.xvg")
    tm, md = xvg(rep / "md-energy.xvg")
    assert np.isclose(tv[-1], 100) and np.isclose(tp[-1], 200)
    assert np.isclose(tm[-1], 1000)
    log = (args.directory / "setup/em.log").read_text(encoding="utf-8")
    steps = int(re.search(r"converged to Fmax < 500 in (\d+) steps", log)[1])
    fmax = float(re.search(r"Maximum force\s*=\s*([\d.eE+-]+)", log)[1])
    means, centers = [], []
    for start in np.arange(0, 1000, 50):
        selected = (tm >= start) & (tm < start+50)
        means.append(float(md["Pressure"][selected].mean()))
        centers.append(float(tm[selected].mean()))
    summary = {
        "minimization": {"attempted_steps": steps,
                         "last_recorded_step": int(em_t[-1]),
                         "Fmax_kJ_mol_nm": fmax,
                         "initial_potential_kJ_mol": float(em["Potential"][0]),
                         "final_potential_kJ_mol": float(em["Potential"][-1])},
        "nvt_50_100ps": stats(tv, nvt, 50, 100),
        "restrained_npt_100_200ps": stats(tp, {k: npt[k] for k in
            ("Temperature", "Volume", "Density")}, 100, 200),
        "unrestrained_npt_500_1000ps": stats(tm, md, 500, 1000),
        "pressure_blocks": {"window_ps": "0 <= t < 1000", "width_ps": 50,
                            "centers_ps": centers, "means_bar": means},
        "pressure_scope": "Unrestrained production; restrained preparation uses refcoord-scaling=com",
        "sd_definition": "Sample spread of saved records, not an uncertainty of the mean"
    }
    (args.output / "preparation_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    zh = args.language == "zh"
    plt.rcParams.update({"font.family": ["Microsoft YaHei", "Noto Sans CJK SC",
                         "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"]
                         if zh else ["DejaVu Sans"], "font.size": 14,
                         "svg.fonttype": "path", "axes.spines.top": False,
                         "axes.spines.right": False})
    fig, axes = plt.subplots(2, 2, figsize=(15, 10), constrained_layout=True)
    ax = axes[0, 0]
    ax.plot(em_t, em["Potential"]/1000, color="#267b7e", lw=1.6)
    ax.set_xlabel("最小化优化步" if zh else "Minimization step")
    ax.set_ylabel("势能 / (10³ kJ mol⁻¹)" if zh else "Potential / (10³ kJ mol⁻¹)")
    ax.set_title("A  几何松弛" if zh else "A  Geometrical relaxation")
    ax = axes[0, 1]
    ax.plot(tv, nvt["Temperature"], color="#a77747", alpha=.75,
            label="NVT + 位置限制" if zh else "NVT + restraints")
    ax.plot(tp+100, npt["Temperature"], color="#6e8d7a", alpha=.75,
            label="NPT + 位置限制" if zh else "NPT + restraints")
    ax.plot(tm+300, md["Temperature"], color="#267b7e", alpha=.6,
            label="NPT生产" if zh else "NPT production")
    ax.axhline(300, color="#4d5456", ls="--", lw=1)
    ax.set_xlabel("累计动力学时间 / ps" if zh else "Cumulative dynamics time / ps")
    ax.set_ylabel("温度 / K" if zh else "Temperature / K")
    ax.set_title("B  温度与阶段" if zh else "B  Temperature and stages")
    ax.legend(fontsize=11, frameon=False, loc="lower right")
    ax = axes[1, 0]
    ax.plot(tp, npt["Volume"], color="#6e8d7a", label="受限准备" if zh else "Restrained preparation")
    ax.plot(tm+200, md["Volume"], color="#267b7e", alpha=.75,
            label="解除位置限制" if zh else "Position restraints removed")
    ax.axvline(200, color="#4d5456", ls="--", lw=1)
    ax.set_xlabel("自NPT准备开始的时间 / ps" if zh else "Time from NPT preparation / ps")
    ax.set_ylabel("盒体积 / nm³" if zh else "Cell volume / nm³")
    ax.set_title("C  溶液体积的调整" if zh else "C  Solution-volume adjustment")
    ax.legend(fontsize=11, frameon=False)
    ax = axes[1, 1]
    ax.plot(tm, md["Pressure"], color="#a9c8c1", lw=.8,
            label="每1 ps保存值" if zh else "Records every 1 ps")
    ax.plot(centers, means, "o-", color="#b47742", ms=4,
            label="50 ps分块均值" if zh else "50 ps block means")
    ax.axhline(1, color="#34484b", ls="--", lw=1, label="1 bar")
    ax.set_xlabel("生产时间 / ps" if zh else "Production time / ps")
    ax.set_ylabel("压力 / bar" if zh else "Pressure / bar")
    ax.set_title("D  无位置限制的压力波动" if zh else "D  Pressure without position restraints")
    ax.legend(fontsize=11, frameon=False)
    for ax in axes.flat:
        ax.grid(alpha=.2)
        ax.set_axisbelow(True)
    fig.suptitle("泛素：从初始几何到溶液动力学" if zh else
                 "Ubiquitin: from initial geometry to solution dynamics", fontsize=21)
    fig.savefig(args.output / "protein_preparation.svg")
    fig.savefig(args.output / "protein_preparation.png", dpi=140)
    plt.close(fig)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

Requires NumPy and Matplotlib. Reads actual energy files in setup and replica-1; --language zh or en selects figure language.

### Actual ubiquitin preparation and production records

Common minimization followed by 100 ps restrained NVT, 200 ps restrained NPT, and 1000 ps unrestrained NPT. The pressure panel uses unrestrained production, with 50 ps blocks spanning 0≤t<1000 ps; the full pressure trace includes the final 1000 ps frame.

GROMACS 2026.4; chain A of PDB 1UBQ, 76 residues; AMBER99SB-ILDN with TIP3P. All 602 experimental heavy atoms are retained and 629 hydrogen atoms added. His68 uses neutral NE2 protonation, with charged free termini.

[Download reference data and complete inputs (ZIP) 0.37 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-protein-preparation-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g07/en/#en-s7)

Actual minimization, restrained NVT, restrained NPT and unrestrained production records. Minimization uses optimization indices; each dynamical stage measures time from its own start. Restrained preparation with refcoord-scaling=com tracks geometry, temperature and volume adjustment. The pressure panel uses unrestrained production: thin lines show saved values and dark points show 50 ps block means.

Together the panels describe a connected process. Geometrical relaxation first removes unfavorable high-energy contacts. After velocity assignment, the earliest dynamics contains substantial redistribution of energy, followed by temperature control near the requested kinetic-energy scale. Pressure coupling adjusts the cell from its initial geometrical volume toward the region visited by the solution. Removing position restraints then allows the protein and solvent to continue under the production potential. Temperature and volume remain variable, and pressure shows especially wide fluctuations. These features reflect preparation, exchange with the environment, and thermal motion of a finite system.

Each orange pressure point averages saved records within a 50 ps interval using a left-inclusive, right-exclusive boundary. The first block covers 0≤t<50 ps, the next 50≤t<100 ps, and together they cover 0≤t<1000 ps. The raw trace still includes the final 1000 ps frame, while the later-window statistics include both 500 and 1000 ps. Explicit interval definitions let another reader reproduce the numbers from the same files. The block curve makes slower variation easier to see while retaining the original data; it does not automatically establish that the blocks are statistically independent.

These records show an inspectable preparation followed by solution dynamics near the intended temperature and pressure environment. Questions about how far ubiquitin's tail extends, how many conformations a side chain occupies, or whether a larger structural transition occurs require the corresponding structural variables and sampling analysis. Energy, temperature, and volume provide foundational checks with a complementary role to protein conformational statistics. The next chapter turns to the coordinate trajectory itself and defines measurements of that motion.

## Let the observable determine what sufficient preparation means

No universal equilibration duration applies independently of system and observable. Local water positions, solution density, side chains, and long loops can adjust at different rates. A volume trace may fluctuate within a stable range while the protein remains within one region near its starting conformation. Conversely, an active-looking side chain does not establish that temperature or composition was configured correctly. A sound assessment selects observables according to the question and considers the relevant preparation traces, structural changes, and independent trajectories together.

For this introductory purpose, the short trajectory supports practice in organizing inputs, continuing state, distinguishing additional position restraints from chemical bond constraints, and reading basic physical quantities. Studying slower ubiquitin exchange processes calls for extended production and independent replicas, followed by checks on the relevant structural distributions. Keep analysis definitions fixed as sampling grows, including the structural reference, atom selection, and statistical window. Additional calculation then adds evidence about the same question rather than producing quantities that become difficult to compare because their definitions keep changing.

A persistent trend suggests a concrete next check. Temperature deviations lead to velocity generation, coupling groups, degrees of freedom, and energy exchange. Continuing volume changes lead to pressure coupling, composition, and starting density. Abnormal local geometry leads to atom identity, topology connectivity, contacts, and constraints. Each check has a specific input and an observable consequence. Following this causal sequence is usually more informative than changing many parameters at once and losing track of which condition altered the behavior.

This chapter establishes a habit of identifying the physical stage before interpreting its values. The 1704 minimization attempts describe geometrical optimization; 100 ps and 200 ps are restrained preparation durations; approximately 299.86 K, 189.14 nm³, and 2.45 bar are actual averages from a specified production window. Each observable has its own fluctuation amplitude and correlation. Model conditions, time intervals, and statistical definitions together give these values meaning. Applying this habit to the protein trajectory turns a molecular animation into quantities that can support a scientific discussion.

## Further Reading and Open Materials

- [Introduction to Molecular Dynamics](https://tutorials.gromacs.org/docs/md-intro-tutorial.html) · Cathrine Bergh; Maryam Majdolhosseini; Alessandra Villa · CC BY 4.0

  Sequence of minimization, restrained NVT/NPT, and production.

  Uses 1UBQ and explicit 2026.4 inputs, explains references, checkpoints, restraints, and constraints, and adds actual stage-specific analysis.
- [From Proteins to Perturbed Hamiltonians: A Suite of Tutorials for the GROMACS-2018 Molecular Simulation Package](https://github.com/jalemkul/gmx_tutorials_livecoms) · Justin A. Lemkul · CC BY 4.0

  Protein-solution equilibration and continuation workflow.

  Uses current stochastic coupling and ubiquitin, distinguishing restrained preparation from unrestrained production.
- [Restraints — GROMACS 2026.4](https://manual.gromacs.org/2026.4/reference-manual/functions/restraints.html) · GROMACS developers · GROMACS documentation terms; factual reference

  Position-restraint potential, force, and reference definitions.

  Explained through a complete one-coordinate example and interaction.
- [Molecular dynamics parameters — GROMACS 2026.4](https://manual.gromacs.org/2026.4/user-guide/mdp-options.html) · GROMACS developers · GROMACS documentation terms; factual reference

  Meaning of continuation, constraints, velocity generation, and refcoord-scaling.

  Connects options to actual stages and explains COM reference treatment and restrained-pressure conditions.
- [Dynamics of folded proteins](https://doi.org/10.1038/267585a0) · J. Andrew McCammon; Bruce R. Gelin; Martin Karplus · Publisher copyright; factual historical citation

  The scientific question of internal protein fluctuations in 1977.

  Rewritten historical discussion with a conceptual fluctuation diagram.
- [Canonical sampling through velocity rescaling](https://doi.org/10.1063/1.2408420) · Giovanni Bussi; Davide Donadio; Michele Parrinello · Author preprint publicly readable; factual citation

  Stochastic velocity rescaling and canonical sampling in 2007.

  Explains the distinction between a mean and a distribution with a schematic.
- [Pressure control using stochastic cell rescaling](https://doi.org/10.1063/5.0020514) · Mattia Bernetti; Giovanni Bussi · Author preprint publicly readable; factual citation

  Volume fluctuations in stochastic cell rescaling, 2020.

  Connects the method to this solution's pressure and volume records.
