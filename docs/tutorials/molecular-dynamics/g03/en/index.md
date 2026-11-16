# A First Simulation of a Box of Water

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g03/en/
Language: en

Prepare water geometry, temperature, and volume, then use actual force, energy, and density records to understand what each stage accomplishes.

## Give the water a suitable starting point before it moves

Pour a bag of glass beads into a box and their first arrangement will usually need to settle. A gentle shake releases crowded contacts and lets beads fill nearby gaps. Constructing a molecular model presents a related preparation problem: having coordinates does not establish that the arrangement suits the selected interactions and environment. The previous lesson placed water molecules in a periodic box. This lesson relaxes their geometry, adjusts their motion and volume, and produces records that can be examined as physical observations.

The actual example uses SPC/E water in an initially 3 nm cubic box, with targets of 300 K and 1 bar. Its question is specific: how do temperature, volume, and density change during this preparation, and what observations tell us what each stage accomplished? These fundamentals determine whether later protein, hydrogel, or membrane systems have sensible starting conditions. If the solvent is still contracting noticeably, interpreting a solute's simultaneous movement as a material property can mix preparation changes with the phenomenon under investigation.

Four kinds of operation make up the workflow. Energy minimization adjusts coordinates to reduce large local forces. NVT dynamics holds the box volume fixed while motion adjusts to the temperature conditions. NPT dynamics lets box dimensions respond to pressure control. NVE branches then remove temperature and pressure coupling to examine numerical energy behaviour. Each stage leaves different evidence: potential energy and maximum force for minimization, kinetic energy and temperature for thermal adjustment, volume and fluctuations for pressure adjustment, and total energy over time for approximately isolated dynamics.

NVT lasts 20 ps, NPT lasts 100 ps, and each NVE branch lasts 100 ps. These are observation periods chosen for a small local teaching example whose complete record can be inspected. A slow process does not finish simply because an input file has been labelled “equilibration.” If an observable continues to drift, further sampling or a preparation check is needed. Actual records connect the decision to proceed with the physical quantities being observed.

Mass, molecule number, and spatial scale must remain consistent throughout. Construction determines the molecule count; temperature and pressure control do not create or delete waters. NPT can change the volume, so density changes accordingly. In pure water, the inventory and box volume provide a cross-check on density. When salt or a polymer is introduced later, the same conservation-based reasoning remains useful: establish what is in the box before discussing how its contents rearrange.

All text inputs needed for the example appear on this page, together with the commands and complete analysis program. Save them in one example directory using the file relationships established previously, inspect the engine version, and execute the script. The script performs repetitive stage transitions, while the explanation identifies each stage's purpose and the meaning of its outputs. A first reading can follow one stage at a time; the same files also support a complete repeat of the calculation.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g03/en/#en-s1)

Figure 1 · Stage objectives and evidence. Minimization is optimization; the later stages advance physical time. The two NVE time steps are compared in the next lesson.

### Water topology template

```
; Water-box workflow adapted from Wes Barnett and Vedran Miletic's GASERI tutorial.
; https://gaseri.org/en/tutorials/gromacs/1-tip4pew-water/
; Tutorial adaptations: CC BY-SA 4.0. The supplied force field retains its license.
; This example uses SPC/E rather than TIP4P/Ew and a 3 nm periodic cube.
#include "oplsaa.ff/forcefield.itp"
#include "oplsaa.ff/spce.itp"
[ system ]
SPC/E water in a periodic cube
[ molecules ]
```

Matches the local example input. Keep text files in the same example directory; the specified GROMACS installation supplies the force-field definitions.

## Minimization prepares geometry rather than waiting for water to cool

Potential energy depends on molecular arrangement. If two sites are too close, short-range repulsion can generate a large force, and starting dynamics immediately may produce an excessive displacement in one update. Minimization moves coordinates toward lower potential energy to relieve unsuitable contacts introduced during construction. It resembles removing an uncomfortable stone from beneath a shoe before walking: the operation prepares a usable geometry rather than providing a measurement of normal walking speed.

The example uses steepest descent. Imagine searching for lower ground on an uneven landscape: each attempt follows the local downhill direction, followed by a check of whether the new position is lower. The actual calculation takes place in the high-dimensional space of all atomic coordinates, with potential energy playing the role of height and force related to its change. The emstep parameter sets a displacement scale, which the algorithm adjusts according to the outcome of attempted steps. This is not a dynamics time step, so minimization progress should not be labelled as physical picoseconds.

Water geometry needs particular care. Text precision and construction can leave small differences from the exact geometry required by rigid constraints. Initial minimization therefore uses the supplied water topology's flexible bond and angle branch to relax geometry. NVT, NPT, and NVE dynamics then use rigid SPC/E water with SETTLE constraints. The two treatments have different jobs: one prepares the initial arrangement, and the other specifies the molecular model whose dynamics we observe. Analysis of water motion uses the dynamics trajectory.

### Complete flexible-geometry minimization input

```
integrator = steep
define = -DFLEXIBLE
emtol = 100.0
emstep = 0.001
nsteps = 10000
nstenergy = 10
cutoff-scheme = Verlet
nstlist = 20
coulombtype = PME
rcoulomb = 1.0
vdwtype = Cut-off
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
constraints = none
constraint-algorithm = lincs
```

Matches the local example input. Keep text files in the same example directory; the specified GROMACS installation supplies the force-field definitions.

Check maximum force and the termination reason to establish whether minimization met its target. A substantial decrease in total potential energy indicates rearrangement, but one local contact can still carry a large force even when the energy of a large system changes little. Maximum force focuses attention on the most strongly forced atom. Here, the threshold is 100 kJ mol⁻¹ nm⁻¹, with at most 10,000 updates. The program may reach the force criterion first or exhaust the permitted updates first; the log distinguishes those outcomes.

Find the largest atomic force from its componentsEq. 1

![Find the largest atomic force from its components](https://ml-biomat.com/static/agent-math/f4ef89e41fe66c3553fefa61.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Fmax | Largest force magnitude over the atoms | kJ mol⁻¹ nm⁻¹ |
| i | Atom index | dimensionless |
| Fix, Fiy, Fiz | Force components on atom i along three perpendicular directions | kJ mol⁻¹ nm⁻¹ |
| max, √, ², +, = | max takes the largest value; sum squared components and take the square root for vector magnitude; equality gives the definition | operators have no units |

Reading the relationshipCalculate each atom’s force magnitude and then its maximum, so a strongly forced local contact is not hidden by an average.

A worked exampleComponents of 60, 80, and 0 kJ mol⁻¹ nm⁻¹ give a magnitude of 100. If another atom has magnitude 120, the maximum is 120, above this example’s threshold of 100.

ConditionsThis interprets the minimization maximum force. It differs from total potential energy and does not establish thermal equilibration at the target temperature.

The force unit follows from energy change per distance. Dividing molar energy by nanometres expresses the scale of force associated with changing positions. A value of 100 kJ mol⁻¹ nm⁻¹ corresponds to approximately 1.66×10⁻¹⁰ N, or 166 pN, for a particle, after using Avogadro's constant to convert the molar expression. This conversion explains the stopping criterion's scale. It does not prescribe one threshold for every task: detailed vibrational analysis and ordinary preparation for dynamics can call for different minimization criteria.

Many locally low-energy arrangements can remain after minimization. The algorithm advances from its starting point according to nearby energy changes; it does not enumerate every possible molecular configuration. In a liquid, thermal motion must subsequently exchange neighbours and configurations. We therefore do not seek to lock all waters permanently into one low-energy arrangement. Preparation aims to provide geometry suitable for starting dynamics, with a clear account of how that geometry was obtained.

The sign of potential energy also depends on the chosen reference. Adding a constant to the entire potential leaves energy differences and forces unchanged, so it does not alter the motion. A negative total potential is therefore not sufficient evidence of a suitable structure. The trend within the same model, maximum force, and local geometry are more informative. Different force fields can have different references and energy decompositions, so comparisons between them require a defined common physical quantity.

### Minimization potential and stopping condition

Actual optimization indices and potential from em.log; the horizontal axis is not physical time. Maximum force and stopping information come from the same log.

GROMACS 2026.4; 884 SPC/E waters in an initially 3 nm cubic box, with targets of 300 K and 1 bar. The NPT record spans 100 ps and descriptive statistics use 50–100 ps; the player shows a separate 100 ps NVE stage.

[Download reference data and complete inputs (ZIP) 1.82 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-water-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g03/en/#en-s2)

Potential energy during steepest descent. The horizontal axis is the optimization update index; rejected trial steps are absent from this record. It is not elapsed physical time.

| Quantity | Value | Unit |
| --- | --- | --- |
| Final maximum force | 96.9421 | kJ mol⁻¹ nm⁻¹ |
| Last saved optimization index | 2049 | 1 |
| Maximum force below 100 | ✓ | kJ mol⁻¹ nm⁻¹ |

The final saved minimization index is 2049, with a maximum force of 96.94 kJ mol⁻¹ nm⁻¹, below the requested threshold of 100. Counting from index zero gives 2050 minimization steps, including attempted moves. Potential falls rapidly at first and more slowly later, consistent with large initial contacts being relieved before smaller geometric adjustments. This completes the force-criterion task for the flexible preparation model. Rigid water and motion at the target temperature still need to be established next.

## Temperature control must preserve thermal fluctuations

After geometry preparation, the water needs velocities. At the first dynamics stage, we generate velocities for 300 K, giving particles a distribution suited to the intended thermal conditions. Temperature describes the statistical energy scale of many degrees of freedom, not an identical speed assigned to every molecule. People moving around a field provide a simple analogy: individual speeds differ even when their collective activity has a recognizable average level. Molecular thermal motion likewise contains a distribution of velocities.

Kinetic energy connects mass and velocity. For classical quadratic kinetic degrees of freedom, equilibrium statistics relate average kinetic energy to temperature. A degree of freedom can initially be understood as an independently variable mode of motion. A point moving freely in three dimensions has three translational components. A rigid water molecule can also rotate, while its constrained internal stretching is not an independent fluctuation. The software determines an effective count from the particles, constraints, and treatment of overall motion, and uses that count when reporting temperature.

Connect average kinetic energy with temperatureEq. 2

![Connect average kinetic energy with temperature](https://ml-biomat.com/static/agent-math/89aa7bd20b939a88f3fec6e0.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ⟨K⟩ | Mean total kinetic energy of the relevant degrees of freedom | joules, J, for the complete model |
| f | Number of independent quadratic kinetic degrees of freedom, adjusted for constraints and overall-motion treatment | dimensionless |
| kB | Boltzmann constant, 1.380649×10⁻²³ | J K⁻¹ |
| T | Thermodynamic temperature | kelvin, K |
| ⟨ ⟩, /, ×, = | Angle brackets denote an ensemble mean; the fraction denotes division; adjacent factors multiply; equality states the equilibrium relation | operators have no units |

Reading the relationshipUnder classical equilibrium conditions, each independent quadratic kinetic degree of freedom contributes kBT/2 on average; summing f contributions gives the total.

A worked exampleFor an illustration with f=60 and T=300 K, the mean kinetic energy is 30×1.380649×10⁻²³×300=1.2425841×10⁻¹⁹ J. GROMACS energy tables use their kJ/mol convention; convert consistently to J for this expression, or use the gas constant R in a consistent molar expression.

ConditionsThis applies to the relevant classical quadratic degrees of freedom at equilibrium. Instantaneous kinetic temperature fluctuates; constraints, centre-of-mass treatment, and the discrete kinetic-energy definition must be consistent.

NVT temperature control exchanges energy with an idealized thermal environment. This does not require simulating an enormous external bath explicitly. An algorithm represents the bath's statistical effect on the system. Its application and coupling strength can influence dynamical correlations, so thermostat choices should suit the intended measurement as well as the average temperature. We couple the whole pure-water system as one group with a time constant of 1 ps and examine how its thermal motion adjusts.

In 2007, Bussi, Donadio, and Parrinello introduced stochastic velocity rescaling to address a specific statistical problem: adjust velocities while retaining the kinetic-energy distribution required by the canonical ensemble. That ensemble describes systems with the same particle number and volume in contact with an environment at the same temperature. Their energies fluctuate. Suitable temperature control therefore allows an appropriate distribution rather than forcing every instantaneous temperature to one exact value. The GROMACS v-rescale setting corresponds to this method. [Bussi and colleagues, 2007](https://doi.org/10.1063/1.2408420)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g03/en/#en-s3)

Figure 2 · Stochastic velocity rescaling (2007) addresses kinetic-energy statistics, while stochastic cell rescaling (2020) addresses volume statistics. The conceptual curves illustrate finite distribution widths and fluctuations at equilibrium.

### Complete NVT input: 20 ps

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
nstlist = 20
coulombtype = PME
rcoulomb = 1.0
vdwtype = Cut-off
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
constraints = h-bonds
constraint-algorithm = lincs
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 300
nsteps = 10000
continuation = no
pcoupl = no
gen-vel = yes
gen-temp = 300
gen-seed = 20261110
ld-seed = 20261111
```

Matches the local example input. Keep text files in the same example directory; the specified GROMACS installation supplies the force-field definitions.

The input fixes the seed for initial velocity generation and the seed used by the thermostat's stochastic process, recording this particular calculation. Different seeds can generate different microscopic paths even when average temperatures agree. Molecules need not occupy the same positions at every moment. When independent repetitions are required, we deliberately vary the relevant seeds while retaining the model, temperature, and other controlled conditions. A fixed seed identifies an individual realization; repeated realizations help assess variation between runs.

Read the NVT temperature trace for both fluctuations around its central level and any persistent trend. Rapid early adjustment can reflect the initial state adapting to the conditions. Sustained later drift calls for further observation. Kinetic energy supplies a cross-check: with a fixed degree-of-freedom count, it should vary consistently with temperature. The smaller up-and-down variations are part of thermal behaviour. Stronger coupling or excessive smoothing should not be used simply to make a physically informative trace look quiet.

The relevant thermal statistic also depends on the distinction between collective and internal motion. If the whole box drifts together, that translation contributes kinetic energy without describing the relative thermal motion we intend to measure. Removing centre-of-mass motion affects the degree-of-freedom count and temperature interpretation. The centre of mass is a mass-weighted representative position; its motion describes translation of the system as a whole. Reading temperature together with constraints and overall motion is more informative than judging whether individual particles look fast.

### Temperature, kinetic energy, and potential in NVT

The G03 program reads actual legends in nvt-energy.xvg, preserving its time axis and showing the 300 K target.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g03/en/#en-s3)

Actual temperature, kinetic energy and potential energy during the 20 ps NVT stage. The dashed line marks the 300 K thermostat target. Water enters rigid dynamics from the flexible minimized structure, and the initial energy redistribution remains visible.

In this run, temperature begins near 300 K, drops sharply to approximately 160 K, and then returns toward the target as the thermostat and structure adjust. Kinetic energy falls while potential energy rises during the early interval, showing a redistribution between motion and interactions in the minimized starting state. Generating velocities at 300 K specifies an initial motion distribution; it does not instantly turn the spatial arrangement into an equilibrium liquid at that temperature. The observed transient explains why preparation is retained rather than treating the first frame as representative of the target conditions.

## Allow volume to respond so water can establish its density

Specifying a 3 nm side during construction gives the water an initial space. That volume need not be the average preferred by the selected model at the target temperature and pressure. NVT retains the initial volume, adjusting thermal motion without allowing expansion or contraction. NPT permits box dimensions to change and sample the corresponding volume distribution at fixed molecule count. Density responds inversely to volume, connecting the geometric relationship from the first lesson to a recorded dynamical process.

A container with a movable piston helps explain pressure control. Motion and interactions inside the container contribute forces on its boundary, the surroundings exert pressure, and the piston can move to change volume. A periodic simulation box has no literal wall or piston. The algorithm changes box vectors and coordinates to sample the intended statistical conditions. The analogy explains why volume can change, while the implementation reminds us that barostat settings belong to the computational method rather than describing each scaling event as a physical instrument movement.

We use isotropic pressure coupling for this homogeneous liquid. All spatial directions scale together, preserving the cubic shape. A membrane may require different treatment in its plane and along its normal; a crystal may require cell-shape changes. The choice here follows the bulk-liquid system. This makes it clear why a water-box barostat configuration should not be transferred to every material without considering the physical directions and responses that matter.

In 2020, Bernetti and Bussi studied stochastic cell rescaling with volume fluctuations as part of the objective. The method allows volume to relax toward the pressure conditions while sampling an appropriate distribution. It makes a useful distinction concrete: a plausible mean and a correctly sampled distribution are different tests. Algorithms can give similar average volumes while generating different fluctuations, which matters for properties related to compressibility. GROMACS C-rescale is used in this example's pressure-coupled stage. [Bernetti and Bussi, 2020](https://doi.org/10.1063/5.0020514)

### Complete NPT input: 100 ps

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
nstlist = 20
coulombtype = PME
rcoulomb = 1.0
vdwtype = Cut-off
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
constraints = h-bonds
constraint-algorithm = lincs
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 300
nsteps = 50000
continuation = yes
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
gen-vel = no
ld-seed = 20261112
```

Matches the local example input. Keep text files in the same example directory; the specified GROMACS installation supplies the force-field definitions.

The settings use ref-p of 1 bar, tau-p of 5 ps, and compressibility of 4.5×10⁻⁵ bar⁻¹. The last quantity supplies the barostat with a compressibility scale describing relative volume response to pressure. It is an input to the pressure-control procedure here, not a newly measured property from this short trajectory. Temperature control continues at 300 K. Velocities come from the preceding stage, with gen-vel set to no, so the calculation continues water already in motion rather than randomly restarting at every transition.

Instantaneous pressure fluctuates more strongly than many beginners expect. It is calculated from motion and interactions in a finite nanoscale box, unlike a familiar pressure gauge that averages over larger scales and longer periods. We examine volume and density for preparation changes while retaining pressure as a diagnostic. Judging the target requires the observation window and fluctuations, rather than asking every sample to equal 1 bar. Persistent expansion or contraction indicates that the record still contains substantial adjustment.

Volume fluctuations also have a material interpretation. Materials with different compressibility respond differently to pressure, and statistical mechanics connects certain responses to fluctuations. We do not estimate a precise compressibility from this short teaching record, but can understand why the fluctuations matter. Fixing volume to a supposedly correct value at every step would remove information that NPT sampling is meant to provide. Questions about both average behaviour and variation helped motivate the development of suitable pressure-control methods.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g03/en/#en-s4)

Figure 3 · The same molecule count in a larger volume has lower mass density. Dots illustrate counting rather than actual water structure; measured NPT curves appear in the result panel.

Choose ensemble conditions to see which quantities are controlled and what can be exchanged with the environment.

[Figure: System and its temperature and pressure environment](https://ml-biomat.com/tutorials/molecular-dynamics/g03/en/#en-s4)

Ensemble-condition illustration; a dashed box indicates that volume can respond to pressure coupling.

## How the complete script connects the stages

The topology template and stage-specific MDP files have now been explained. The script copies the template, constructs the water box, preprocesses and minimizes it, and passes each stage's final state to the next. Checkpoints retain positions, velocities, and the state needed by the relevant algorithms, and are supplied together with coordinates during transitions. Thus “continue the preceding stage” has a concrete implementation. Each command reveals which state is being used, rather than leaving the connection implicit in a filename.

After NPT, the example creates two NVE branches for the next lesson's time-step comparison. Both begin from the same npt.gro and npt.cpt, generate no new velocities, and cover 100 ps. Their time steps are 2 fs and 1 fs. Both full inputs are shown below. The step count changes with the integration interval while the physical observation duration remains fixed. Neighbour-list settings are also held according to the comparison design to reduce additional differences.

### Complete NVE input: 2 fs steps

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

Matches the local example input. Keep text files in the same example directory; the specified GROMACS installation supplies the force-field definitions.

### Complete NVE input: 1 fs steps

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

Matches the local example input. Keep text files in the same example directory; the specified GROMACS installation supplies the force-field definitions.

NVE removes temperature and pressure coupling, making the numerical behaviour of molecular total energy easier to interpret. Fixed volume means this branch's density no longer adjusts through a barostat. It is useful for energy diagnostics and certain dynamical observations, while NPT volume statistics still come from the NPT record. Using each stage for its intended purpose prevents a flat density line caused by fixed volume from being interpreted as a density estimate without uncertainty.

### Complete script from construction to observable export

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
cp topol.template.top topol.top
"$gmx" solvate -cs spc216.gro -box 3 3 3 -o water.gro -p topol.top > solvate.log 2>&1
"$gmx" grompp -f em.mdp -c water.gro -p topol.top -o em.tpr -pp em.top -po em.processed.mdp > em.grompp.log 2>&1
"$gmx" mdrun -deffnm em -ntmpi 1 -ntomp 4 -pin off > em.stdout.log 2>&1
"$gmx" grompp -f nvt.mdp -c em.gro -p topol.top -o nvt.tpr -po nvt.processed.mdp > nvt.grompp.log 2>&1
"$gmx" mdrun -deffnm nvt -ntmpi 1 -ntomp 4 -pin off > nvt.stdout.log 2>&1
"$gmx" grompp -f npt.mdp -c nvt.gro -t nvt.cpt -p topol.top -o npt.tpr -po npt.processed.mdp > npt.grompp.log 2>&1
"$gmx" mdrun -deffnm npt -ntmpi 1 -ntomp 4 -pin off > npt.stdout.log 2>&1
for step in 2fs 1fs; do
  "$gmx" grompp -f "nve-$step.mdp" -c npt.gro -t npt.cpt -p topol.top -o "nve-$step.tpr" -po "nve-$step.processed.mdp" > "nve-$step.grompp.log" 2>&1
  "$gmx" mdrun -deffnm "nve-$step" -ntmpi 1 -ntomp 4 -pin off > "nve-$step.stdout.log" 2>&1
done
printf 'Potential\n0\n' | "$gmx" energy -f em.edr -o em-potential.xvg > em-potential.log 2>&1
printf 'Temperature\nPotential\nKinetic-En.\nTotal-Energy\nPressure\n0\n' | "$gmx" energy -f nvt.edr -o nvt-energy.xvg > nvt-energy.log 2>&1
printf 'Density\nVolume\nTemperature\n0\n' | "$gmx" energy -f npt.edr -o npt-density-volume-temperature.xvg > npt-properties.log 2>&1
for step in 2fs 1fs; do
  printf 'Total-Energy\nTemperature\nPotential\nKinetic-En.\n0\n' | "$gmx" energy -f "nve-$step.edr" -o "nve-$step-energy.xvg" > "nve-$step-energy.log" 2>&1
done
printf 'System\n' | "$gmx" trjconv -f nve-2fs.xtc -s nve-2fs.tpr -o trajectory.gro -dt 2 -pbc mol > trajectory-export.log 2>&1
"$gmx" check -f nve-2fs.xtc > trajectory-check.log 2>&1
```

Matches the local example input. Keep text files in the same example directory; the specified GROMACS installation supplies the force-field definitions.

Output redirection saves each command's terminal messages in a corresponding log. grompp checks and assembles inputs, mdrun advances the system, energy extracts observables, and trjconv prepares a trajectory representation for viewing. A final check inspects trajectory frames and times. These tools each perform a defined task, and their combination remains inspectable step by step. A failed earlier operation does not magically supply correct input to the later commands.

The setting constraints = h-bonds can cause a terminology misunderstanding. Here it means constraints on covalent bonds involving hydrogen atoms, not a fixed network of intermolecular hydrogen bonds. Water's rigid geometry follows its topology through SETTLE, while separate water molecules still move and rotate relative to one another. Hydrogen-bond contacts can consequently form and disappear. Covalent bonds, geometric constraints, and intermolecular hydrogen bonding are distinct concepts, and that distinction is essential for interpreting a dynamic water network.

Inspect the minimization log for its stopping condition, then examine the NVT and NPT records. Existing complete trajectories can be reanalysed without rerunning all the dynamics. Changing interactions or dynamics settings, however, requires outputs generated from the new inputs. Altering analysis changes how existing motion is measured; altering simulation changes how the motion is produced. Keeping these operations distinct also helps direct computing effort toward the part of the study that actually needs to be updated.

Elapsed computing time depends on processor, threading, compilation, and system load. The reproducible physical objects are the system size, simulated duration, settings, and actual outputs, with the execution environment recorded alongside them. Increasing thread count changes how work is assigned to the processor; it does not turn 100 ps into a longer molecular observation. Parallelism and acceleration matter for larger systems, but first establish that the chosen model and analysis address the question.

## Plot each stage on an axis with the right meaning

An interpretable figure begins by identifying its horizontal axis. Minimization uses updates, describing progress in coordinate optimization. NVT and NPT use physical time, describing dynamical evolution. Joining these records into one unexplained time trace would imply that the water first underwent a period of physical energy descent before normal motion began. Separate panels retain their different dimensions and meanings, making it possible to compare preparation processes without confusing optimization with dynamics.

Stage times can also restart from a new origin or continue an existing time, depending on the input. An analysis reads the actual recorded values and identifies the stage before applying any explicitly stated offset for a combined display. Energy components also change their definition when flexible minimization gives way to rigid dynamics. Those records should not be joined into a curve that is expected to remain continuous everywhere. Explaining a stage boundary is part of defining the measurement, just as specifying the time and energy units is.

The XVG reader identifies quantities by their series labels rather than the order in which names were entered for selection. The minimization panel shows potential energy, with the final maximum force and termination information reported from the log. NVT panels show temperature and energy; NPT panels connect volume and density. Raw traces retain variation, while summaries identify the part of the record being described. The result shows both preparation changes and the average level of a defined later window.

### Complete Python: read and plot by stage

```
#!/usr/bin/env python3
"""Read actual water-stage records and plot each on its proper axis.

Usage: python analyze_stages.py RUN_DIRECTORY --output figures --language en
The directory contains em.log, nvt-energy.xvg, and
npt-density-volume-temperature.xvg. Dependencies: numpy, matplotlib.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def read_xvg(path: Path):
    legends, rows = {}, []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("@"):
            match = re.match(r'@\s+s(\d+)\s+legend\s+"([^"]+)"', line)
            if match:
                legends[int(match[1])] = re.sub(r"[^a-z]", "", match[2].casefold())
            continue
        if line == "&":
            raise ValueError("Expected one dataset in the XVG file.")
        rows.append([float(value) for value in line.split()])
    values = np.asarray(rows, dtype=float)
    if values.ndim != 2 or len(values) < 2 or not np.all(np.isfinite(values)):
        raise ValueError("Missing or nonfinite XVG data.")
    if np.any(np.diff(values[:, 0]) <= 0):
        raise ValueError("Physical times must increase strictly.")
    columns = {}
    for index, name in legends.items():
        if name in columns or index + 1 >= values.shape[1]:
            raise ValueError("Ambiguous XVG legends.")
        columns[name] = values[:, index + 1]
    return values[:, 0], columns


def read_minimization(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    records = {}
    current_step = None
    for index, line in enumerate(lines[:-1]):
        if re.fullmatch(r"\s*Step\s+Time\s*", line):
            current_step = int(lines[index + 1].split()[0])
        # GROMACS energy tables use 15-character fields.
        headings = [line[j:j + 15].strip() for j in range(0, len(line), 15)]
        if "Potential" in headings and current_step is not None:
            numbers = lines[index + 1].split()
            if len(numbers) != len(headings):
                raise ValueError("Energy-table headings and numbers disagree.")
            records[current_step] = float(numbers[headings.index("Potential")])
    if len(records) < 2:
        raise ValueError("Cannot identify minimization step and potential records.")
    match = re.search(r"Maximum force\s*=\s*([+\-\d.eE]+)", text)
    if not match:
        raise ValueError("Final maximum-force summary is missing.")
    final_force = float(match[1])
    convergence = re.search(r"Steepest Descents converged to Fmax", text) is not None
    steps = np.array(sorted(records), dtype=int)
    potential = np.array([records[int(step)] for step in steps])
    return steps, potential, final_force, convergence


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_directory", type=Path)
    parser.add_argument("--output", type=Path, default=Path("figures"))
    parser.add_argument("--language", choices=("zh", "en"), default="en")
    args = parser.parse_args()
    stage = args.run_directory
    steps, potential, fmax, converged = read_minimization(stage / "em.log")
    tnvt, nvt = read_xvg(stage / "nvt-energy.xvg")
    tnpt, npt = read_xvg(stage / "npt-density-volume-temperature.xvg")
    for key in ("temperature", "potential", "kineticen"):
        if key not in nvt:
            raise ValueError(f"NVT series is missing: {key}")
    for key in ("density", "volume", "temperature"):
        if key not in npt:
            raise ValueError(f"NPT series is missing: {key}")
    mask = tnpt >= tnpt[0] + 0.5 * (tnpt[-1] - tnpt[0])
    count = int(mask.sum())
    if count < 2:
        raise ValueError("Too few samples in the NPT observation window.")
    units = {"density": "kg/m^3", "volume": "nm^3", "temperature": "K"}
    summary = [{"quantity": key, "unit": units[key], "samples": count,
        "start_ps": float(tnpt[mask][0]), "end_ps": float(tnpt[mask][-1]),
        "mean": float(np.mean(npt[key][mask])),
        "sample_standard_deviation": float(np.std(npt[key][mask], ddof=1))}
        for key in ("density", "volume", "temperature")]
    report = {"minimization": {"last_saved_step": int(steps[-1]),
        "final_maximum_force_kJ_mol_nm": fmax,
        "force_criterion_met": converged},
        "npt_window": summary,
        "spread_definition": "Sample SD describes fluctuations, not uncertainty of the mean."}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "stages_summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    with (args.output / "npt_window.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    zh = args.language == "zh"
    tr = lambda chinese, english: chinese if zh else english
    plt.rcParams.update({"font.family": ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else "DejaVu Sans",
        "font.size": 14, "svg.fonttype": "path", "axes.spines.top": False,
        "axes.spines.right": False, "figure.facecolor": "#faf9f4",
        "axes.facecolor": "#faf9f4", "savefig.facecolor": "#faf9f4"})

    def save(fig, name):
        fig.savefig(args.output / (name + ".svg"))
        fig.savefig(args.output / (name + ".png"), dpi=180)
        plt.close(fig)

    fig, axis = plt.subplots(figsize=(11, 5), constrained_layout=True)
    axis.plot(steps, potential, color="#2b7b70", linewidth=1.6)
    axis.set(xlabel=tr("最小化更新步号", "Minimization update index"),
             ylabel=tr("势能 / kJ mol⁻¹", "Potential energy / kJ mol⁻¹"),
             title=tr("初始几何的最速下降整理", "Steepest-descent preparation of the initial geometry"))
    axis.grid(axis="y", alpha=0.2)
    save(fig, "em_minimization")

    fig, axes = plt.subplots(3, 1, figsize=(11, 10), sharex=True, constrained_layout=True)
    fields = [("temperature", tr("温度 / K", "Temperature / K")),
              ("kineticen", tr("动能 / kJ mol⁻¹", "Kinetic energy / kJ mol⁻¹")),
              ("potential", tr("势能 / kJ mol⁻¹", "Potential energy / kJ mol⁻¹"))]
    for axis, (key, label) in zip(axes, fields):
        axis.plot(tnvt, nvt[key], color="#2b7b70", linewidth=1)
        axis.set_ylabel(label)
        axis.grid(axis="y", alpha=0.2)
    axes[0].axhline(300, color="#ad6b40", linestyle="--", label=tr("300 K 目标", "300 K target"))
    axes[0].legend(frameon=False, fontsize=12)
    axes[-1].set_xlabel(tr("NVT 记录时间 / ps", "Recorded NVT time / ps"))
    fig.suptitle(tr("固定体积下的热运动", "Thermal motion at fixed volume"), fontsize=20)
    save(fig, "nvt_preparation")

    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True, constrained_layout=True)
    for axis, key, label in [(axes[0], "volume", tr("体积 / nm³", "Volume / nm³")),
                             (axes[1], "density", tr("密度 / kg m⁻³", "Density / kg m⁻³"))]:
        axis.axvspan(tnpt[mask][0], tnpt[-1], color="#dbe9df", alpha=0.7)
        axis.plot(tnpt, npt[key], color="#2b7b70", linewidth=1)
        axis.axhline(np.mean(npt[key][mask]), color="#ad6b40", linestyle="--",
                     label=tr("后半窗口均值", "Second-half window mean"))
        axis.set_ylabel(label)
        axis.legend(frameon=False, fontsize=12)
        axis.grid(axis="y", alpha=0.2)
    axes[-1].set_xlabel(tr("NPT 记录时间 / ps", "Recorded NPT time / ps"))
    fig.suptitle(tr("固定分子数下的体积与密度", "Volume and density at fixed molecule count"), fontsize=20)
    save(fig, "npt_preparation")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
```

Reads explicit update indices from em.log and dynamics series by XVG legends. Generates bilingual stage figures and window statistics.

The analysis uses the second half of the NPT time record as its descriptive window and calculates the mean and sample standard deviation. The mean adds the selected values and divides by their number. Standard deviation describes their spread around that mean. Correlated observations still have a measurable spread, but uncertainty in the estimated average requires accounting for the amount of effectively independent information. The ninth lesson develops correlation times and block statistics; here, the window and quantity definitions remain explicit.

Mean level and fluctuations within a windowEq. 3

![Mean level and fluctuations within a window](https://ml-biomat.com/static/agent-math/8a1a2bfe926e22e3fe99c0a4.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Ak | Measurement k in the selected window | same as the observable; kg m⁻³ for density |
| Ā | Arithmetic mean within the window | same as Ak |
| sA | Sample standard deviation describing the spread | same as Ak |
| n, k | n is the number of measurements, at least two; k is their index | dimensionless |
| Σ, −, ², √, /, = | Σ sums from k=1 to n; subtract the mean and square; divide by n−1 and take the square root for sample SD; equality defines the quantities | operators have no units |

Reading the relationshipThe mean describes the centre. Squared deviations prevent positive and negative departures from cancelling, and the square root restores the observable’s units. The n−1 denominator gives the conventional sample variance.

A worked exampleIllustrative densities of 998, 1000, and 1002 kg m⁻³ have a mean of 1000 and a sample SD of 2 kg m⁻³. The running example uses all recorded values in its stated window.

ConditionsThese describe the selected record. Frames can be correlated: SD is neither standard error of the mean nor a confidence interval. Uncertainty analysis additionally considers correlation and repetitions.

A statistical window must be interpreted alongside the visible process. The second half is a stated descriptive rule for this example. If that interval still drifts, extend the observation and explain the trend rather than declaring equilibration because a rule has been applied. Splitting the window into two intervals can reveal whether its mean continues to move, while independent repetitions provide another comparison. These checks ask how much the record still reflects its initial preparation, building intuition for more rigorous uncertainty analysis.

### Connected volume and density in NPT

Complete NPT record and its second-half descriptive window; means and sample SD use the same interval.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g03/en/#en-s6)

In the same box at fixed molecule count, density decreases as volume increases. Shading marks the descriptive window of 50–100 ps, used to calculate the dashed mean in each panel.

| Quantity | Value | Unit |
| --- | --- | --- |
| Density window mean | 997.8 | kg m⁻³ |
| Density sample standard deviation | 11.26 | kg m⁻³ |
| Volume window mean | 26.51 | nm³ |
| Volume sample standard deviation | 0.2976 | nm³ |

Over 50–100 ps, mean volume is 26.506 nm³ with a sample standard deviation of 0.298 nm³. Mean density is 997.83 kg m⁻³ with a sample standard deviation of 11.26 kg m⁻³. Peaks and troughs occur in opposite directions because the same water mass occupies changing volumes. Variations persist for several picoseconds or longer, affecting averages from a short window. Keeping the complete trace and its stated window makes the next comparison clear: extend the observation and use independent runs to examine the stability of the average.

When comparing temperature, volume, and density, establish that they come from the same stage and observation range. Volume is fixed in NVT, changes in NPT, and is fixed again in NVE. NVE temperature can fluctuate as energy moves between kinetic and potential forms. Different controls imply different expected behaviours, so a horizontal curve is not a universal success criterion. The accompanying model, target conditions, interval, and measurement definitions supply the context needed to read it.

Total energy also needs this stage context. A thermostat exchanges energy with the system, and pressure control involves changing volume and associated work. The sum of molecular kinetic and potential energies therefore need not remain constant in NVT or NPT as it would in ideal isolated dynamics. Some algorithms have extended or effective conserved quantities that include the controller's contribution. We first examine molecular total energy in NVE, then develop these broader definitions, avoiding confusion between normal controlled energy exchange and numerical instability.

## Specify which observation is stable

A run that finishes establishes that its numerical steps did not terminate prematurely under those settings. A temperature trace fluctuating around its target establishes a corresponding thermal observation. Density without a visible trend in a selected interval describes that observable in that interval. Each supplies part of the picture. Diffusion, dielectric response, or rare hydrogen-bond arrangements need their own sampling and uncertainty checks. An apparently steady density cannot stand in for every other physical timescale.

A classroom at the start of a term provides an analogy. Attendance can stabilize quickly while seating patterns, study groups, and communication continue to develop. Attendance resembles a fast-settling overall quantity, while internal organization may take longer. Liquids also contain motions on different scales. In macromolecules, solvent adjustment, side-chain rotation, and overall conformational changes can have especially different timescales. How long a system has been prepared should therefore be considered together with what is being measured.

Visual jumps across a periodic boundary need a representation-aware interpretation. A molecule leaving one face and reappearing at the opposite face may simply be the same particle crossing the periodic cell. Reconstructed whole water molecules should retain the geometry of the rigid model. Animation can reveal conspicuous gaps, overlaps, and display artefacts, while giving an intuitive view of translation and rotation. Quantitative analysis still needs coordinates appropriate to the question, such as continuous displacement for diffusion and correct periodic distances for local structure.

### Water motion after preparation

Actual nve-2fs trajectory with physical time, periodic box information, and whole-molecule representation.

NVE energy checks further separate different meanings of numerical stability. Energy can show small rapid fluctuations and a slow drift, which should be measured separately. Changing the time step can also change discretized relationships used in reported energies. Comparisons therefore use each branch's own initial energy as its baseline while aligning the initial state and physical duration. The next lesson connects these records to integration algorithms so that time-step choices can be evaluated using the actual evidence.

If a result differs from expectations, work through the data and physical layers. Identify the stage, units, and series labels first, then check the input combination and geometry, followed by coupling, interactions, and sampling duration. This order starts with directly inspectable facts. It also leaves room for new physical findings, because a persistent difference becomes scientifically informative once its data interpretation and numerical setting have been understood.

The model determines which chemical processes can appear. Fixed-connectivity water can translate, rotate, and change intermolecular contacts, but it does not generate water autoionization through electronic rearrangement. Changes in ion count are consequently not an acid–base equilibrium result of this trajectory. Protonation will be an important preparation choice for proteins and nucleic acids. If proton transfer itself is the research question, a method capable of representing that process becomes part of the design.

## Move from a first run to a purposeful comparison

The next calculation can be designed as a clear comparison. Keep the model, molecule count, and target pressure fixed while changing temperature from 300 K to another chosen value, then prepare and compare density distributions. Alternatively, retain the physical conditions and change the time step to inspect numerical behaviour. These answer different questions: one changes thermodynamic conditions, while the other evaluates an approximation. Changing both together makes the reason for a difference harder to identify.

Each comparison should identify the retained objects, deliberately changed conditions, and common measurement definitions. Density comparisons need consistent units, windows, and statistics. Structural comparisons need consistent atom selections and periodic treatment. Dynamical measurements require sufficient physical duration and recording frequency for the motion of interest. Repeated runs then help assess variation. Inputs, trajectories, and figures become connected by the same question rather than accumulating as unrelated outputs.

The water box now supplies a complete starting point: coordinates and topology, preparation stages with defined purposes, actual dynamical and thermodynamic records, and repeatable analysis. Next we examine the interactions and integration process, connecting force fields, time steps, and periodic boundaries to those records. When proteins, nucleic acids, and polymers are added, the choices will still need explicit explanation, but their physical roles will already be recognizable.

## Further Reading and Open Materials

- [GROMACS tutorial 1: Water](https://gaseri.org/en/tutorials/gromacs/1-tip4pew-water/) · Wes Barnett; Vedran Miletić · CC BY-SA 4.0 (English tutorials)

  Adapted staged water preparation, execution, and density observation workflow.

  SPC/E, 300 K, 1 bar, and 2026.4 algorithms; flexible geometry preparation then rigid MD; adds paired NVE diagnostics and original bilingual analysis. Workflow adaptations retain CC BY-SA 4.0.
- [Canonical sampling through velocity rescaling](https://doi.org/10.1063/1.2408420) · Giovanni Bussi; Davide Donadio; Michele Parrinello · Factual scientific citation; no reused figure

  History and statistical objective of the 2007 v-rescale method.

  Original conceptual diagram and explanation.
- [Pressure control using stochastic cell rescaling](https://doi.org/10.1063/5.0020514) · Mattia Bernetti; Giovanni Bussi · Factual scientific citation; no reused figure

  The 2020 C-rescale method and volume fluctuations.

  Independent explanation through the water-box question.
- [Energy minimization, GROMACS2026.4](https://manual.gromacs.org/2026.4/reference-manual/algorithms/energy-minimization.html) · GROMACS developers · Technical reference

  Steepest descent and maximum-force stopping.

  Independent analogy and explanation of example parameters.
