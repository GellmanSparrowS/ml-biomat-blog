# Where Resistance to Flow Comes From

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l11/en/
Language: en

Drive two walls in opposite directions and connect molecular velocities, wall forces, and temperature to the measured shear response of a confined electrolyte.

## Liquid between two sliding surfaces

A thin layer of water changes the resistance you feel when you slide your palm over glass. Related questions arise in coating, lubrication, and microfluidic devices: how does a surface carry liquid with it, and how does the liquid transmit resistance back to the surface? When a gap becomes a few molecular diameters wide, water can form distinct layers near the solid. Dissolved ions bring their own hydration environments into that confined space. The response of this liquid depends on its surfaces as well as its molecular composition. Molecular dynamics turns those ingredients into positions, velocities, and forces that we can inspect together.

In this lesson, the upper wall moves to the right and the lower wall moves to the left. Their relative motion shears the electrolyte between them. A useful first picture is a stack of cards whose layers slide by different amounts. The cards illustrate relative displacement, but fluid layers are not permanent sheets: molecules continually enter and leave each region. We therefore divide the gap by height and average the velocities of whichever atoms occupy each slice. That spatial average is the bridge between irregular molecular motion and the smoother velocity field used to describe a flowing liquid.

By the end, you will be able to run a complete LAMMPS model containing water, sodium ions, chloride ions, and explicit walls; identify the commands that impose wall motion and control temperature; plot a velocity profile across the gap; and combine wall resistance with the measured fluid velocity gradient. The final number describes a specified experiment in the computer: the chosen interactions and surfaces, a temperature near 300 K, walls moving at ±20 m/s, and a stated observation window. Geometry, temperature, drive, and sampling all belong to the measurement definition.

Three directions organize the calculation. The walls move along x, z runs from the bottom wall toward the top wall, and y lies within the wall plane, perpendicular to x. Periodic boundaries repeat the cell in x and y, so one wall tile represents an extended interface. Explicit wall atoms confine the liquid in z. The cell dimensions remain fixed while wall atoms retain motion in the permitted directions. This loading method transmits momentum through surfaces. It therefore provides a direct route to studying the relationship between an interface and its adjacent liquid, with different geometry from a uniformly sheared periodic bulk cell.

Individual molecules often move much faster than the mean flow, and their instantaneous directions keep changing. Following a few particles by eye can make a simple average flow look confusing. We will measure the different contributions separately. Mean velocity describes directed transport, temperature describes kinetic energy in selected degrees of freedom, wall force describes resistance to the imposed motion, and spatial density describes where atoms spend their time. Before combining them in a figure, we need to know which atoms, components, and times contribute to each quantity.

### The driven confined electrolyte

Actual shearing trajectory, with time measured from the start of wall motion. The spatial statistics below use the same run.

LAMMPS 30 Sep 2026 Update 1; the nanosheared-electrolyte example by Gravelle and colleagues, with TIP4P/2005 water at 300 K in real units, periodic x/y and fixed z boundaries; 30 ps of preparation followed by 200 ps of shear.

[Download reference data and complete inputs (ZIP) 19.29 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-electrolyte-shear-data.zip)

## From rotating cylinders to a nanoslit

Calling a liquid viscous often begins with experience: it pours slowly or takes effort to stir. A comparable physical measurement requires a specified motion and a specified response. In his 1890 study of liquid friction, Maurice Couette asked whether the internal-friction coefficient was a well-defined physical quantity and what rules were needed to measure it. Concentric-cylinder experiments linked controlled rotation to the torque required to hold an inner cylinder at rest. This arrangement turned an everyday impression of resistance into a repeatable relationship between motion, force, and geometry.

Torque describes how strongly a force tends to rotate an object about an axis. A force acting farther from the axis generally has a larger turning effect, so cylinder measurements need the apparatus dimensions as well as the measured mechanical response. Imagine opening a small section of the curved gap into a pair of parallel surfaces. This preserves the measurement idea: move a boundary, let the liquid transmit momentum, and measure the resulting resistance. Cylindrical and planar geometries still require their own equations. We use plates here because slices, gradients, and wall forces are particularly easy to connect in this geometry.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l11/en/#en-s2)

Figure 1 · Couette connected controlled cylinder rotation to measured torque. The plate schematic carries that measurement idea into nanoscale shear; the two drawings represent different geometries.

A liquid transmits resistance without containing a hidden stack of welded sheets. Molecules near the upper wall gain directed momentum through interactions with it. Collisions and intermolecular forces transfer momentum to neighbouring molecules, while the lower wall drives motion in the opposite direction. Molecules move between regions as momentum moves between regions. A macroscopic viscous stress summarizes many such exchanges as a tangential force per unit area. The molecular model also exposes the structural environment in which those exchanges occur, including water orientation, ion hydration, and packing against the wall.

For intuition, picture neighbouring rows of people moving in opposite directions and transmitting pushes through contact. The comparison explains momentum transfer without assigning intentions to molecules. Molecular motion follows forces, masses, and current velocities. The charged sites of water, ionic charges, and wall interactions all contribute to those forces. Averaging over many events organizes the irregular motion into a velocity profile. The profile does not replace the molecular description; it is a measurement extracted from it, much as an average traffic speed is extracted from many individual journeys.

The historical apparatus suggests a practical research sequence: control motion, measure response, and examine the conditions under which a proposed relation holds. A Newtonian liquid in its linear-response regime has stress approximately proportional to velocity gradient at fixed temperature. The proportionality coefficient is viscosity. Interfacial liquids, polymer solutions, or strongly driven fluids may change structure and response as the driving rate changes. One calculation measures a ratio at one drive. A series of drives tests whether that ratio stays constant. These are related questions supported by different sets of observations.

## The molecular details retained by the flow model

The model contains 406 water molecules, 15 sodium ions, 15 chloride ions, and 432 wall atoms: 1680 explicit atoms in total. Water uses TIP4P/2005. Oxygen and two hydrogen positions are explicit, while the negative interaction site M is determined from molecular geometry. Thus four interaction sites and three trajectory atoms describe the same water molecule. Equal numbers of positive and negative ions make the entire cell electrically neutral, but each ion still interacts with the charged sites of surrounding water. Net neutrality describes a sum over the system; it does not remove local electrostatic forces.

SHAKE constrains each O–H distance to 0.9572 Å and the H–O–H angle to 104.52°. The retained motions therefore include molecular translation, rotation, and rearrangement of the surrounding liquid. Water bond stretching, chemical dissociation, and proton transfer belong to models with additional degrees of freedom and appropriate interactions. The fixed connectivity here makes the represented motion explicit. It also determines the constraints that must enter temperature calculations. A force field and its constraint rules form one physical model, rather than a collection of independent settings that can be changed without consequence.

The neutral wall atoms use the masses and Lennard–Jones parameters specified in the input. They form a structured contact surface, experience forces, and exchange momentum with the water. Surface charging, hydroxyl reactions, and electronic response are separate ingredients. This example asks how the specified neutral wall potential and electrolyte cooperate during flow. To study a charged biomaterial interface, define the surface chemistry and charge state first, then retain the velocity, force, and spatial-analysis methods developed here. Renaming the wall material leaves the interaction model unchanged; changing the chemistry requires changing its physical description.

The nonbonded settings also work as a set. Specialized TIP4P electrostatics places the negative charge at the implicit M site during force evaluation. A generic calculation that treats it as a charge at the oxygen position describes a different distribution. The cell repeats in x and y, uses fixed boundaries in z, and applies a slab correction to long-range electrostatics. This numerical treatment concerns periodic-image geometry. Electrostatic forces directed across the actual liquid-filled gap remain part of the molecular calculation. Together, these choices represent a slit extended along its wall plane.

One periodic wall tile is 24.24 Å, or 2.424 nm, on each in-plane side. A nanometre is one billionth of a metre, so the entire model is much smaller than familiar visible objects. Periodic repetition lets that small tile represent a locally uniform interface. Larger surface defects, roughness patterns, or distinct chemical domains must be included on their own spatial scales if they are the research target. The chosen cell dimensions determine which spatial variations can occur within the simulation. This is a useful modelling decision to make before interpreting a number as a property of an entire experimental surface.

The input files connect these ideas to executable definitions. `water.mol` contains the molecular geometry and connectivity template, `parameters.inc` contains masses, charges, and interaction parameters, and `groups.inc` separates water, ions, fluid, and the two walls. Groups determine which atoms receive a thermostat, a constraint, an imposed force rule, or an analysis selection. Reading them carefully makes each later command easier to interpret. It also prevents a common measurement error: including moving wall atoms when the intended quantity is the velocity of the liquid.

### Complete input: water.mol

```
# LAMMPS Molecule File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

3 atoms
2 bonds
1 angles

Coords

1    0 0 0
2    0.9584 0 0
3    -0.23996 0.92787 0

Types

1        O
2        H
3        H

Charges

1       -1.1128
2        0.5564
3        0.5564

Bonds

1   O-H      1      2
2   O-H      1      3

Angles

1   H-O-H    2      1      3

Shake Flags

1 1
2 1
3 1

Shake Atoms

1 1 2 3
2 1 2 3
3 1 2 3

Shake Bond Types

1 O-H O-H H-O-H
2 O-H O-H H-O-H
3 O-H O-H H-O-H

Special Bond Counts

1 2 0 0
2 1 1 0
3 1 1 0

Special Bonds

1 2 3
2 1 3
3 1 2
```

Keep these files together and run bash run.sh to construct, prepare, and shear the system.

### Complete input: parameters.inc

```
# LAMMPS Include File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

mass O 15.9994
mass H 1.008
mass Na+ 22.990
mass Cl- 35.453
mass WALL 26.9815

pair_coeff O O 0.185199 3.1589
pair_coeff H H 0.0 1.0
pair_coeff Na+ Na+ 0.04690 2.4299
pair_coeff Cl- Cl- 0.1500 4.04470
pair_coeff WALL WALL 11.697 2.574
pair_coeff O WALL 0.4 2.86645

bond_coeff O-H 0 0.9572
angle_coeff H-O-H 0 104.52
```

Keep these files together and run bash run.sh to construct, prepare, and shear the system.

### Complete input: groups.inc

```
# LAMMPS Include File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

group H2O type O H
group Na type Na+
group Cl type Cl-
group ions union Na Cl
group fluid union H2O ions

group wall type WALL
region rtop block INF INF INF INF 0 INF
region rbot block INF INF INF INF INF 0
group top region rtop
group bot region rbot
group walltop intersect wall top
group wallbot intersect wall bot
```

Keep these files together and run bash run.sh to construct, prepare, and shear the system.

## Separating mean flow from thermal motion

A region of liquid can flow to the right while a particular molecule moves left at one instant. Mean flow describes a directional tendency across many observations; an individual velocity also contains thermal fluctuations. A moving walkway gives a useful analogy: velocity relative to the ground combines the walkway motion and motion relative to the walkway. A liquid has no literal walkway. Instead, the local mean velocity defines a moving reference for describing fluctuations. The distinction becomes especially important when a simulation both drives the liquid and controls its temperature.

Directed flow and transverse temperatureEq. 3

![Directed flow and transverse temperature](https://ml-biomat.com/static/agent-math/ba77495ddc5483bf11fa11e9.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| vᵢ,ₓ | Complete x velocity of atom i | m/s |
| uₓ(zᵢ) | Mean flow at the atom height | m/s |
| cᵢ,ₓ | Velocity fluctuation relative to mean flow | m/s |
| Tᵧz | Temperature defined with y and z velocity components | K |
| Kᵧz | Total kinetic energy in those velocity components | J |
| fᵧz | Effective degrees of freedom after constraints and translation corrections | dimensionless |
| kB | Boltzmann constant 1.380649×10⁻²³ | J/K |
| i、zᵢ | Atom index and its height | dimensionless; m |
| =、/、+、−、× | Equality; division; addition; subtraction; multiplication. A fraction bar also denotes division. | operators |
| 2 | Each quadratic kinetic degree of freedom contributes kBT/2, so converting kinetic energy to temperature supplies a factor of two. | dimensionless |

Reading the relationshipVelocity splits into a local mean plus a fluctuation. Each classical quadratic kinetic degree of freedom contributes kBT/2 on average, giving the transverse temperature.

A worked exampleFor an arithmetic example with fᵧz=1000 at 300 K, Kᵧz=2.0709735×10⁻¹⁸J. LAMMPS computes the actual constrained degrees of freedom for this water model.

ConditionsThe decomposition explains temperature. The input thermostats y and z using temp/partial 0 1 1; x retains the driven flow and exchanges energy through interactions.

If all directed x motion were treated as thermal motion to be reduced toward a target temperature, a thermostat could interfere with the flow being studied. This example uses a transparent alternative: temperature is evaluated from y and z velocity components, and those components are thermostatted. The imposed x motion remains available, while interactions exchange energy between directions. Temperature control and flow driving then have distinct roles. A complete analysis still checks whether the resulting transverse temperature behaves as intended and whether the flow profile develops under the specified loading.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l11/en/#en-s4)

Figure 2 · Teal and orange arrows illustrate velocity decomposition. The actual input thermostats transverse components of fluid and walls separately while retaining driven x motion.

The three flags in `compute Tfluid fluid temp/partial 0 1 1` refer to x, y, and z. Zero excludes a component from this temperature definition; one includes it. The following `fix_modify mynvt1 temp Tfluid` assigns that temperature computation to the fluid thermostat. Wall atoms use a separate transverse temperature computation and thermostat. Both groups can therefore exchange energy with their respective thermal reservoirs. A thermostat is an algorithmic representation of controlled thermal conditions, with a specified coupling time, rather than an extra collection of water molecules hidden outside the simulation cell.

Rigid-water constraints make the degree-of-freedom count important. Three unconstrained atoms have nine positional degrees of freedom in three dimensions. Fixing two bond lengths and the included angle leaves the translation and rotation of a rigid molecule. Selecting velocity components and accounting for centre-of-mass corrections require further consistent bookkeeping. We therefore read the dedicated constrained temperature calculation instead of replacing its degree count by a guessed multiple of the atom count. The equation explains why kinetic energy relates to temperature; the actual compute supplies the count appropriate to the constraints and selection.

Thermal control also changes what energy records should tell us. Moving walls continually do work, and thermostats exchange energy with the system. Mechanical energy can therefore vary during this driven calculation. The relevant checks are that the walls retain their prescribed speeds, transverse temperature fluctuates around 300 K, a persistent shear profile develops, and the time statistics of resistance can be examined. An isolated trajectory without a thermostat or external drive is appropriate for a separate integration-energy test. Here, temperature and energy records help establish the intended driven conditions.

## Building and driving the electrolyte

Place the complete files in one example directory. `run.sh` executes construction, preparation, and shearing in that order. Construction creates water, ions, and walls and writes `create.data`. Minimization and 30 ps of preparation then produce `equilibrate.data`. The shear stage reads that state and drives the walls for 200 ps. Data files retain atomic state and connectivity, while parameter files are included again so the same interactions remain in use. Checking for these named outputs provides a simple way to follow the progress of a first run.

### Complete input: create.lmp

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

boundary p p f
units real
atom_style full
bond_style harmonic
angle_style harmonic
pair_style lj/cut/tip4p/long O H O-H H-O-H 0.1546 12.0
kspace_style pppm/tip4p 1.0e-5
kspace_modify slab 3.0

lattice fcc 4.04
region box block -3 3 -3 3 -5 5
create_box 5 box &
  bond/types 1 &
  angle/types 1 &
  extra/bond/per/atom 2 &
  extra/angle/per/atom 1 &
  extra/special/per/atom 2
labelmap atom 1 O 2 H 3 Na+ 4 Cl- 5 WALL
labelmap bond 1 O-H
labelmap angle 1 H-O-H

region rbotwall block -3 3 -3 3 -4 -3
region rtopwall block -3 3 -3 3 3 4
region rwall union 2 rbotwall rtopwall
create_atoms WALL region rwall

region rliquid block INF INF INF INF -2 2
molecule h2omol water.mol
create_atoms 0 region rliquid mol h2omol 482793

create_atoms Na+ random 15 5802 rliquid overlap 0.3 maxtry 500
create_atoms Cl- random 15 9012 rliquid overlap 0.3 maxtry 500
set type Na+ charge 1
set type Cl- charge -1

include parameters.inc
include groups.inc

delete_atoms random fraction 0.15 yes H2O NULL 482793 mol yes


write_dump all custom created.lammpstrj id mol type q x y z ix iy iz modify sort id
run 0

write_data create.data nocoeff
```

Keep these files together and run bash run.sh to construct, prepare, and shear the system.

### Complete input: equilibrate.lmp

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

boundary p p f
units real
atom_style full
bond_style harmonic
angle_style harmonic
pair_style lj/cut/tip4p/long O H O-H H-O-H 0.1546 12.0
kspace_style pppm/tip4p 1.0e-5
kspace_modify slab 3.0

read_data create.data

include parameters.inc
include groups.inc

fix myshk H2O shake 1.0e-5 200 0 b O-H a H-O-H kbond 2000


thermo 1
thermo_style custom step temp etotal press

minimize 1.0e-6 1.0e-6 1000 1000
reset_timestep 0

fix mynvt all nvt temp 300 300 100
fix myshk H2O shake 1.0e-5 200 0 b O-H a H-O-H
fix myrct all recenter NULL NULL 0
timestep 1.0


variable walltopz equal xcm(walltop,z)
variable wallbotz equal xcm(wallbot,z)
variable deltaz equal v_walltopz-v_wallbotz

thermo 250
thermo_style custom step temp etotal press v_deltaz

# Numerical trajectory and thermodynamic records added to the original tutorial.
dump course all custom 500 equilibrate.lammpstrj id mol type q x y z vx vy vz ix iy iz
dump_modify course sort id
compute coursePE all pe
compute courseKE all ke
compute courseTemp all temp
compute coursePressure all pressure courseTemp
variable courseTime equal time
variable courseT equal c_courseTemp
variable courseU equal c_coursePE
variable courseK equal c_courseKE
variable courseE equal c_coursePE+c_courseKE
variable courseP equal c_coursePressure
thermo_style custom step v_courseT v_courseU v_courseK v_courseE v_courseP v_deltaz
fix courseRecord all ave/time 250 1 250 v_courseTime v_courseT v_courseU v_courseK v_courseE v_courseP file equilibrate-thermo.dat

run 30000

write_data equilibrate.data nocoeff





write_restart equilibrate.restart
write_dump all custom equilibrate-final.lammpstrj id mol type q x y z ix iy iz modify sort id
```

Keep these files together and run bash run.sh to construct, prepare, and shear the system.

The shear-stage commands form a physical sequence. Define transverse temperature for fluid and walls, attach the corresponding NVT integration and temperature control, and constrain water geometry with SHAKE. Next, `fix setforce` sets the x force on every atom in both wall groups to zero, and `velocity set` assigns equal and opposite x velocities. The combination of this zero-force rule and the retained x motion sustains wall translation. Motion in y and z continues under the selected dynamics. The entire wall is not repositioned at prescribed coordinates on every step; its x motion follows the velocity and force rules in the input.

Convert the velocity units explicitly before running. With `units real`, length is measured in ångströms and time in femtoseconds. One ångström is 10⁻¹⁰m and one femtosecond is 10⁻¹⁵s, so 1 Å/fs equals 10⁵m/s. The input speed 2×10⁻⁴Å/fs is therefore 20 m/s, and the wall-to-wall velocity difference is 40 m/s. This substantial speed difference acts across a nanometre-scale gap, producing a gradient of order 10¹⁰s⁻¹. The drive makes directional response measurable within a short trajectory and remains part of the conditions attached to the reported result.

`fix setforce` also retains the total group force before cancellation. Its reported x components, `f_mysf1[1]` and `f_mysf2[1]`, therefore describe the action that the loading rule counteracts. Cancelling the subsequent force does not erase the resistance that was evaluated. Think of a motor maintaining a cylinder at constant rotation: the motor supplies the torque needed to balance the liquid resistance. Recording the force before cancellation gives access to the analogous resisting action in this imposed-velocity model.

### Complete input: shearing.lmp

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

boundary p p f
units real
atom_style full
bond_style harmonic
angle_style harmonic
pair_style lj/cut/tip4p/long O H O-H H-O-H 0.1546 12.0
kspace_style pppm/tip4p 1.0e-5
kspace_modify slab 3.0

read_data equilibrate.data

include parameters.inc
include groups.inc

compute Tfluid fluid temp/partial 0 1 1
fix mynvt1 fluid nvt temp 300 300 100
fix_modify mynvt1 temp Tfluid

compute Twall wall temp/partial 0 1 1
fix mynvt2 wall nvt temp 300 300 100
fix_modify mynvt2 temp Twall

fix myshk H2O shake 1.0e-5 200 0 b O-H a H-O-H
fix myrct all recenter NULL NULL 0
timestep 1.0

fix mysf1 walltop setforce 0 NULL NULL
fix mysf2 wallbot setforce 0 NULL NULL
velocity wallbot set -2e-4 NULL NULL
velocity walltop set 2e-4 NULL NULL


thermo 250
thermo_modify temp Tfluid
thermo_style custom step temp etotal f_mysf1[1] f_mysf2[1] 

compute cc1 H2O chunk/atom bin/1d z 0.0 0.25
compute cc2 wall chunk/atom bin/1d z 0.0 0.25
compute cc3 ions chunk/atom bin/1d z 0.0 0.25

fix myac1 H2O ave/chunk 10 15000 200000 &
  cc1 density/mass vx file shearing-water.dat
fix myac2 wall ave/chunk 10 15000 200000 &
  cc2 density/mass vx file shearing-wall.dat
fix myac3 ions ave/chunk 10 15000 200000 &
  cc3 density/mass vx file shearing-ions.dat

# Numerical trajectory and thermodynamic records added to the original tutorial.
dump course all custom 500 shearing.lammpstrj id mol type q x y z vx vy vz ix iy iz
dump_modify course sort id
compute coursePE all pe
compute courseKE all ke
compute courseTemp all temp
compute coursePressure all pressure courseTemp
variable courseTime equal time
variable courseT equal c_Tfluid
variable courseU equal c_coursePE
variable courseK equal c_courseKE
variable courseE equal c_coursePE+c_courseKE
variable courseP equal c_coursePressure
thermo_style custom step v_courseT v_courseU v_courseK v_courseE v_courseP f_mysf1[1] f_mysf2[1]
fix courseRecord all ave/time 250 1 250 v_courseTime v_courseT v_courseU v_courseK v_courseE v_courseP file shearing-thermo.dat

run 200000

write_restart shearing.restart
write_dump all custom shearing-final.lammpstrj id mol type q x y z ix iy iz modify sort id
```

Keep these files together and run bash run.sh to construct, prepare, and shear the system.

### Complete input: run.sh

```
#!/usr/bin/env bash
set -euo pipefail
lmp=${LAMMPS:-lmp}
export OMP_NUM_THREADS=4
for stage in create equilibrate shearing; do
  "$lmp" -sf omp -pk omp 4 -in "$stage.lmp" -log "$stage.log" > "$stage.stdout.log" 2>&1
done
```

Keep these files together and run bash run.sh to construct, prepare, and shear the system.

A 1 fs timestep makes 200000 steps equal 200 ps. Coordinates are saved every 500 steps, so successive trajectory frames are 0.5 ps apart and the output contains 401 frames. Global temperature records are written every 250 steps. Native spatial sampling is denser: every 10 steps, during the final 150000 steps, it accumulates 15000 samples and writes one averaged profile. A single run can therefore provide a comparatively sparse playable trajectory and a densely sampled spatial average. Each file has its own sampling interval. The number of displayed molecular frames is not the number of samples in the native profile.

Over 50–200 ps, the actual transverse temperature averages 299.978 K, with a standard deviation of approximately 9.816 K across saved records. The mean and the spread describe different aspects of a small system. Both wall velocities remain at their assigned ±20 m/s in every saved frame. The following figure retains the rapidly fluctuating wall stress alongside 50 ps block means. Showing both makes the averaging operation visible: a smoother summary emerges from many recorded interactions, while the variations that generated it remain available for inspection.

### Temperature and resistance over time

Transverse temperature and wall forces recorded before cancellation; block means retain the measured variation.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l11/en/#en-s5)

Time starts when the walls begin moving. Temperature uses transverse degrees of freedom excluding x streaming. Shear stress is calculated from the two wall forces and projected area; fine lines retain saved records and the heavier line connects 50 ps interval means.

## Slicing the pore to measure velocity and layering

A trajectory shows where atoms are at particular times. A velocity profile organizes many atoms and many times into one spatial description. Imagine dividing a corridor into sections and recording the velocity of everyone currently within each section. Here, we slice the gap along z and accumulate the x velocities of water atoms occupying each slice. Molecules can move between slices. The spatial regions remain fixed while their membership changes, so the average concerns a location rather than a permanent collection of atom IDs.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l11/en/#en-s6)

Figure 3 · Slices organize positions and velocities into spatial statistics. Native bins are 0.25 Å wide and pool 15000 samples over 50.01–200 ps; the central fit covers −8 to 8 Å.

Mean velocity within a sliceEq. 1

![Mean velocity within a slice](https://ml-biomat.com/static/agent-math/4d083dfd2bcd52269169bae6.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| uₓ(zⱼ) | Mean x velocity in z slice j | m/s |
| vᵢ,ₓ(s) | Atom i x velocity in saved sample s | m/s |
| Bⱼ(s) | Atoms occupying slice j in sample s | set |
| Nⱼ(s) | Number of atoms in that slice and sample | dimensionless |
| i、j、s | Atom, slice, and sample indices | dimensionless |
| ∑、∈ | Sum; membership of the given set | operators |
| =、/、+、−、× | Equality; division; addition; subtraction; multiplication. A fraction bar also denotes division. | operators |

Reading the relationshipSum every recorded atom velocity, then divide by the total number of recorded atom instances. More occupied samples contribute more observations, as in native norm all.

A worked exampleTwo samples contain two and one atoms with velocities 10, 30, and 50 m/s. Their pooled mean is 30 m/s; averaging the two sample means gives 35 m/s and uses different weighting.

ConditionsApplies to atomic velocity bins for water, walls, and ions. Molecular-centre bins define a different measurement.

The native profile pools the individual atom observations. A slice containing ten atoms at one sample contributes ten velocities; the same slice containing one atom later contributes one. An alternative method would first average within each sample and then give every sample equal weight. Those definitions differ when occupancy fluctuates. Stating the weighting connects the mathematical expression to the default `norm all` behaviour and to the Python calculation. The distinction is especially relevant near interfaces, where narrow bins can have strongly varying populations.

A density profile uses the same slices but accumulates mass. Convert atomic molar masses to masses, then divide the mass in a slice by its physical volume to obtain units such as g/cm³. Peaks near a wall indicate heights where atoms occur more frequently and can reveal interfacial layering. Peak positions, widths, and heights describe spatial organization. The velocity curve answers a separate question about directed motion. High density does not by itself specify a high or low mean velocity; inspecting the two measured curves together establishes how structure and flow are arranged in this system.

### Measured layering and velocity gradient

Densities and atom-weighted velocities from native ave/chunk output.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l11/en/#en-s6)

Native bins pool 15000 samples over 50.01–200 ps into density and atom-weighted velocity profiles. The walls move at ±20 m/s; a linear fit over |z|≤8 Å gives the measured central gradient. Original spatial bins retain near-wall layering.

The velocity gradient is the slope of the profile with height. In elementary algebra, a straight-line slope is the change in the vertical variable divided by the change in the horizontal variable. With mean x velocity plotted against z, the slope is the shear rate. Actual bins are noisy, so fitting a line to several central points uses more information than subtracting two selected velocities. This analysis fits water velocities within −8 to 8 Å and obtains 2.43529(m/s)/Å. The fitting range is explicit in the program, and changing it provides a direct way to examine how the interface affects a spatial estimate.

The velocity gradient across the gapEq. 2

![The velocity gradient across the gap](https://ml-biomat.com/static/agent-math/e0bc69b7b30fd9b04ba67be5.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| γ̇ | Shear rate, the velocity gradient | s⁻¹ |
| uₓ | Mean flow velocity along x | m/s |
| z | Coordinate normal to the walls | m |
| d、Δ | Local infinitesimal change; change over a chosen interval | operators |
| ≈ | Approximate a derivative by a finite-interval slope | operator |
| =、/、+、−、× | Equality; division; addition; subtraction; multiplication. A fraction bar also denotes division. | operators |

Reading the relationshipDifferent layer velocities create relative sliding. A fitted slope combines the velocity change across multiple slices.

A worked exampleThe measured central slope 2.43529(m/s)/Å equals 2.43529×10¹⁰s⁻¹ because 1 Å=10⁻¹⁰m. A schematic 40 m/s difference across 2 nm gives 2×10¹⁰s⁻¹.

ConditionsThe present fit uses water velocities within −8≤z≤8 Å. A no-slip plate formula additionally needs the actual fluid boundary planes.

Interpreting slip also requires a defined fluid boundary plane. An atomistic wall has thickness. The innermost atomic layer, the centre of the whole wall, and an effective boundary inferred from repulsion need not coincide. The mean distance between wall centres in this trajectory is approximately 27.405 Å, while flowing water occupies the interior region. Dividing 40 m/s by the wall-centre separation produces a geometric estimate. Fitting the actual liquid profile produces a measured internal gradient. A difference between them invites examination of boundary placement before assigning a particular interfacial mechanism.

The interaction below isolates that boundary question in a solvable plate model. Specify a gap H, a wall-speed magnitude U, and an equal slip length b at both surfaces. The displayed fluid velocity is linear. Slip length relates the boundary velocity difference to the fluid gradient and can be pictured by extending the fluid line into the wall. The model supports numerical intuition, while density layering, effective interface placement, and sampling variations in the molecular case remain questions for the recorded trajectory.

A symmetric-slip plate modelEq. 6

![A symmetric-slip plate model](https://ml-biomat.com/static/agent-math/adedf7e7e01e21951203d6e0.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| U | Top-wall speed magnitude; bottom wall is−U | m/s |
| H | Distance between the chosen fluid boundary planes | m |
| b | Equal Navier slip length at both surfaces | m |
| γ̇ | Constant velocity gradient in the plate model | s⁻¹ |
| uₓ、z | Mean velocity and height measured from the gap centre | m/s; m |
| =、/、+、−、× | Equality; division; addition; subtraction; multiplication. A fraction bar also denotes division. | operators |
| 2 | 2U is the difference between the two wall velocities; 2b adds one slip length at each boundary. | dimensionless |

Reading the relationshipAt each boundary, the velocity jump is b times the fluid gradient. The total wall speed difference is therefore shared across H and two additional slip lengths.

A worked exampleWith U=20 m/s, H=2 nm, and b=0, the gradient is 2×10¹⁰s⁻¹. With b=1 nm, it is 1×10¹⁰s⁻¹ and the fluid boundary velocities are ±10 m/s.

ConditionsContinuum schematic for the offline interaction: parallel plates, symmetric slip, and steady linear flow. The reader supplies b independently of the molecular trajectory.

Parallel-plate model: vary wall speed, gap, and slip length to compare fluid gradients at the same drive.

Keyboard-operable sliders for the analytical Navier plate model: b=0 gives no slip, while larger b reduces the fluid gradient at fixed wall speed.

## From wall force to viscosity

The flow profile tells us how rapidly neighbouring liquid regions slide past each other. Wall force tells us the mechanical action needed to maintain that motion. Liquid generally resists the top wall moving in +x with a negative x force and resists the bottom wall moving in −x with a positive x force. Adding the forces directly would cancel much of the signal we seek. We instead subtract the top force from the bottom force and divide by two. This aligns the signs and averages the resisting action measured at the two surfaces.

Shear stress from the forces on both wallsEq. 4

![Shear stress from the forces on both walls](https://ml-biomat.com/static/agent-math/1bd5d65b6b3f6915343f3554.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| τ | Shear stress associated with the resisting force | Pa=N/m² |
| Fb,ₓ、Ft,ₓ | Net x forces of fluid on bottom and top walls | N |
| ⟨ ⟩ | Average over the stated time window | operator |
| A | Projected area of one wall | m² |
| Lₓ、Lᵧ | Periodic cell lengths along x and y | m |
| 2 | Average the resisting force from the two walls | dimensionless |
| =、/、+、−、× | Equality; division; addition; subtraction; multiplication. A fraction bar also denotes division. | operators |

Reading the relationshipThe liquid resists the top wall moving in +x and the bottom wall moving in −x. Align the signs, average the two resisting forces, and divide by one wall area.

A worked exampleThe mean resisting force 2.835339 kcal/(mol·Å) uses the conversion 6.94769546×10⁻¹¹N per unit. With area 24.24²Å²=5.875776×10⁻¹⁸m², the stress is 33.5259 MPa.

ConditionsUses forces saved before setforce cancels x forces, averaged over 50<t≤200 ps. The area is one complete periodic wall tile.

Stress is force per area, so the chosen area must match the force being measured. Each reported group force belongs to one complete periodic wall tile. Its projected area is Lx multiplied by Ly. Multiplying the denominator by another factor of two would dilute the result because the numerator already averages the two walls. Adding imagined surface areas around individual atoms would define a different quantity. The present calculation follows the familiar mechanical definition: a specified net force distributed over a specified projected area.

Converting the force to newtons also clarifies the meaning of a per-mole energy unit. Reporting an energy in kcal/mol scales the corresponding molecular energy by Avogadro's constant. Dividing by that constant gives the microscopic energy scale. Converting its variation per ångström into variation per metre then gives force in newtons. The measured mean resisting force over 50–200 ps is 2.835339 kcal/(mol·Å). Dividing its converted value by the wall area 5.875776×10⁻¹⁸m² gives 33.5259 MPa. The small area and substantial velocity gradient belong to the interpretation of that large stress.

Dividing stress by the measured central gradient gives 1.37667 mPa·s. We call this an effective viscosity at the stated drive: a compact descriptor that retains the confinement and spatial measurement choices. Its definition includes the central fitted gradient, the projected wall stress, the transverse temperature near 300 K, and the 50–200 ps observation window. These details make comparison possible. Changing wall interactions, salt content, or temperature becomes informative when the same measurement rule is applied to each resulting trajectory.

Pairing resistance with the measured gradientEq. 5

![Pairing resistance with the measured gradient](https://ml-biomat.com/static/agent-math/18c9647c9fb4955753ab65eb.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ηeff | Stress-to-gradient ratio at the specified temperature, confinement, and drive | Pa·s |
| τ | Shear stress over the same observation window | Pa |
| γ̇ | Measured shear rate within the fluid | s⁻¹ |
| =、/、+、−、× | Equality; division; addition; subtraction; multiplication. A fraction bar also denotes division. | operators |

Reading the relationshipViscosity relates the stress required to the relative sliding rate. For a Newtonian fluid in its linear-response regime, the ratio stays constant as the rate changes; a rate series tests this condition.

A worked exampleDividing 33.5259×10⁶Pa by 2.43529×10¹⁰s⁻¹ gives 0.00137667 Pa·s=1.37667 mPa·s. Both quantities refer to the same 50–200 ps observation window.

ConditionsThis finite-window ratio describes the specified TIP4P/2005 electrolyte, walls, and ±20 m/s drive. Bulk zero-shear viscosity requires a bulk model and a lower-rate series.

The complete Python program reads native density and velocity profiles and separately reconstructs three consecutive time-block profiles from the more sparsely saved trajectory. It also writes a clean wall-force CSV for reproducible analysis of the reference data. Time, space, and unit conversions are explicit. Begin by reproducing the figures and summary from the supplied records. Then change one analysis choice, such as the central fitting range or block width. This separates two useful activities: asking a different measurement question of existing data and changing the physical model to produce new data.

### Complete Python: flow profiles, wall forces, and time blocks

```
"""Measure the recorded nanoslit shear flow.

python analyze_shear.py --run . --out figures --language en
Dependencies: NumPy and Matplotlib.
"""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

def frames(path):
    with path.open(encoding='utf-8') as f:
        while line:=f.readline():
            if line.strip()!='ITEM: TIMESTEP':raise ValueError('Timestep header expected')
            step=int(f.readline());assert f.readline().strip()=='ITEM: NUMBER OF ATOMS'
            n=int(f.readline());header=f.readline().split();assert header[:3]==['ITEM:','BOX','BOUNDS']
            bounds=np.array([list(map(float,f.readline().split())) for _ in range(3)])
            assert bounds.shape==(3,2)
            names=f.readline().split()[2:]
            a=np.array([list(map(float,f.readline().split())) for _ in range(n)])
            a=a[np.argsort(a[:,names.index('id')])]
            yield step,bounds,{key:a[:,j] for j,key in enumerate(names)}

def force_records(run):
    clean=run/'wall-forces.csv'
    if clean.exists():return np.loadtxt(clean,delimiter=',',skiprows=1)
    rows=[];active=False
    for line in (run/'shearing.log').read_text(encoding='utf-8').splitlines():
        if 'Step' in line and 'f_mysf1[1]' in line:active=True;continue
        if active and line.startswith('Loop time'):break
        if active:
            try:values=list(map(float,line.split()))
            except ValueError:continue
            if len(values)==8:rows.append([values[0]/1000,values[-2],values[-1]])
    a=np.array(rows);assert a.shape==(801,3)
    return a

def chunk(path):
    lines=[line for line in path.read_text().splitlines() if line.strip() and not line.startswith('#')]
    step,n,total=map(float,lines[0].split());a=np.array([list(map(float,s.split())) for s in lines[1:]])
    assert step==200000 and len(a)==int(n) and a.shape[1]==5
    return a

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run',type=Path,default=Path('.'));p.add_argument('--out',type=Path,default=Path('figures'));p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    zh=a.language=='zh';tr=lambda z,e:z if zh else e
    fonts={f.name for f in font_manager.fontManager.ttflist};family=[f for f in ['Microsoft YaHei','Noto Sans CJK SC','Source Han Sans SC','DejaVu Sans'] if f in fonts]
    plt.rcParams.update({'font.family':family if zh else ['DejaVu Sans'],'font.size':13,'axes.titlesize':15,'svg.fonttype':'path','axes.spines.top':False,'axes.spines.right':False,'axes.facecolor':'#f8f7f2','figure.facecolor':'#f8f7f2','axes.unicode_minus':False})
    colors=['#147d85','#c46938','#4876b7'];thermo=np.loadtxt(a.run/'shearing-thermo.dat',comments='#');forces=force_records(a.run)
    np.savetxt(a.out/'wall-forces.csv',forces,delimiter=',',header='time_ps,force_top_kcal_mol_A,force_bottom_kcal_mol_A',comments='')
    history=[];edges=np.arange(-12,12.0001,1.0);mid=(edges[:-1]+edges[1:])/2
    sums=np.zeros((3,len(mid)));counts=np.zeros_like(sums);block_frame_counts=np.zeros(3,dtype=int)
    for step,bounds,d in frames(a.run/'shearing.lammpstrj'):
        typ=d['type'].astype(int);z=d['z'];wall=typ==5;top=wall&(z>0);bottom=wall&(z<0);fluid=typ<5
        assert len(typ)==1680
        area=np.prod(bounds[:2,1]-bounds[:2,0]);gap=z[top].mean()-z[bottom].mean()
        history.append([step/1000,gap,d['vx'][top].mean()*1e5,d['vx'][bottom].mean()*1e5])
        if 50000 < step <= 200000:
            block=int((step-50001)//50000);sel=typ<=2
            block_frame_counts[block]+=1
            sums[block]+=np.histogram(z[sel],edges,weights=d['vx'][sel]*1e5)[0]
            counts[block]+=np.histogram(z[sel],edges)[0]
    h=np.array(history);assert h.shape==(401,4)
    assert np.allclose(h[:,2],20,atol=1e-9) and np.allclose(h[:,3],-20,atol=1e-9)
    water=chunk(a.run/'shearing-water.dat');walls=chunk(a.run/'shearing-wall.dat');ions=chunk(a.run/'shearing-ions.dat')
    fit=(abs(water[:,1])<=8)&(water[:,2]>0)
    slope,intercept=np.polyfit(water[fit,1],water[fit,4]*1e5,1)
    shear_rate=slope*1e10
    last=(forces[:,0]>50)&(forces[:,0]<=200)
    fdrag=(forces[:,2]-forces[:,1])/2
    force_to_newton=4184/(6.02214076e23*1e-10);stress=fdrag*force_to_newton/(area*1e-20)
    native_temp=(thermo[:,1]>50000)&(thermo[:,1]<=200000)
    block_rows=[]
    for i in range(3):
        lo,hi=50+50*i,100+50*i;mask=(forces[:,0]>lo)&(forces[:,0]<=hi)
        profile=np.divide(sums[i],counts[i],out=np.full(len(mid),np.nan),where=counts[i]>0)
        m=(abs(mid)<=8)&np.isfinite(profile);b,c=np.polyfit(mid[m],profile[m],1)
        block_rows.append([lo,hi,float(stress[mask].mean()/1e6),b,b*1e10,float(stress[mask].mean()/(b*1e10)*1e3)])
    blocks=np.array(block_rows)
    assert block_frame_counts.tolist()==[100,100,100]
    summary={'native_averaging_time_ps':[50.01,200],'native_samples':15000,'native_profile_bin_A':.25,'trajectory_frames':len(h),'wall_speeds_m_s':[20,-20],'wall_center_gap_mean_A':float(h[h[:,0]>50,1].mean()),'area_A2':float(area),'temperature_yz_mean_K':float(thermo[native_temp,2].mean()),'temperature_yz_sd_K':float(thermo[native_temp,2].std(ddof=1)),'mean_drag_force_kcal_mol_A':float(fdrag[last].mean()),'mean_shear_stress_MPa':float(stress[last].mean()/1e6),'central_fit_range_A':[-8,8],'central_gradient_m_s_per_A':float(slope),'central_shear_rate_s-1':float(shear_rate),'central_intercept_m_s':float(intercept),'effective_viscosity_mPa_s':float(stress[last].mean()/shear_rate*1e3),'blocks_50ps':[dict(zip(['start_ps','end_ps','stress_MPa','gradient_m_s_per_A','shear_rate_s-1','viscosity_mPa_s'],row)) for row in block_rows],'sampling_definition':'Native profile pools atom velocities over 15000 samples; block profiles pool atoms over saved 0.5 ps frames in 1 Å slices. Blocks describe temporal sensitivity and are not independent confidence intervals. Wall forces are read before x force cancellation; projected wall area is LxLy. The viscosity ratio uses the actual central fitted gradient at this drive and confined model.'}
    (a.out/'shear_summary.json').write_text(json.dumps(summary,indent=2));np.savetxt(a.out/'shear-blocks.csv',blocks,delimiter=',',header='start_ps,end_ps,stress_MPa,slope_m_s_A,shear_rate_s-1,eta_mPa_s',comments='')
    def save(fig,name):
        for ext in ['svg','png']:fig.savefig(a.out/f'{name}.{ext}',dpi=170,bbox_inches='tight')
        plt.close(fig)
    fig,ax=plt.subplots(2,1,figsize=(11,7),sharex=True,layout='constrained');ax[0].plot(thermo[:,1]/1000,thermo[:,2],c=colors[0],lw=.8);ax[0].axhline(300,c='#7d9191',ls='--');ax[0].set_ylabel(tr('横向温度 / K','Transverse temperature / K'));ax[0].set_title(tr('以剪切开始为零时刻','Time starts when wall motion begins'));ax[1].plot(forces[:,0],stress/1e6,c='#aebdbb',lw=.7,label=tr('瞬时记录','Saved samples'));ax[1].plot((blocks[:,0]+blocks[:,1])/2,blocks[:,2],'o-',c=colors[1],lw=2,label=tr('50 ps区间均值','50 ps block means'));ax[1].set(xlabel=tr('时间 / ps','Time / ps'),ylabel=tr('剪切应力 / MPa','Shear stress / MPa'));ax[1].legend(loc='lower left',bbox_to_anchor=(0,1.02),ncol=2,fontsize=10);save(fig,'shear-history')
    fig,ax=plt.subplots(1,2,figsize=(12,5),layout='constrained')
    for data,color,label in [(water,colors[0],tr('水','Water')),(walls,colors[1],tr('壁','Walls')),(ions,colors[2],tr('离子','Ions'))]:
        ax[0].plot(data[:,1],data[:,3],c=color,label=label)
        mask=data[:,2]>.05
        ax[1].plot(data[mask,1],data[mask,4]*1e5,'.',c=color,ms=4,label=label)
    ax[1].plot([-8,8],np.array([-8,8])*slope+intercept,c='#263f42',ls='--',label=tr('中心线性拟合','Central linear fit'))
    for aa in ax:aa.set_xlabel('z / Å')
    ax[0].legend(loc='upper center',fontsize=10);ax[1].legend(loc='upper left',fontsize=10)
    ax[0].set(ylabel=tr('质量密度 / g cm⁻³','Mass density / g cm⁻³'),title=tr('分层结构来自实际分箱','Layering from recorded bins'));ax[1].set(ylabel=tr('平均x速度 / m s⁻¹','Mean x velocity / m s⁻¹'),title=tr('原子数加权速度；50.01–200 ps','Atom-weighted velocity; 50.01–200 ps'));save(fig,'flow-profiles')
    fig,ax=plt.subplots(1,2,figsize=(12,5),layout='constrained')
    for i,color in enumerate(colors):
        prof=np.divide(sums[i],counts[i],out=np.full(len(mid),np.nan),where=counts[i]>0)
        ax[0].plot(mid,prof,'o-',ms=3,c=color,label=f'{50+50*i}–{100+50*i} ps')
    ax[0].set(xlabel='z / Å',ylabel=tr('水原子平均x速度 / m s⁻¹','Mean water-atom x velocity / m s⁻¹'),title=tr('分别读取三个连续时间块','Three consecutive observation blocks'));ax[0].legend(loc='upper right',fontsize=10)
    ax[1].plot((blocks[:,0]+blocks[:,1])/2,blocks[:,5],'o-',c=colors[1]);ax[1].axhline(summary['effective_viscosity_mPa_s'],c=colors[0],ls='--',label=tr('原生全窗口比值','Ratio from full native window'));ax[1].set(xlabel=tr('区间中心时间 / ps','Block midpoint / ps'),ylabel=tr('应力/速度梯度 / mPa s','Stress/velocity-gradient ratio / mPa s'),title=tr('时间窗口怎样影响估计','Sensitivity to the time window'));ax[1].legend(loc='best',fontsize=10);save(fig,'shear-blocks')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
```

From the reference-data directory run python analyze_shear.py --run . --out figures --language en; use zh for Chinese plots.

There is a statistical step between instantaneous motion and a viscosity estimate. A finite-time average is used to describe ongoing flow. A large force in one record may arise from an instantaneous collision, a structural rearrangement, or a slower change. Removing the point by appearance would alter the measured distribution. A better first step is to inspect nearby records and the corresponding motion, then examine whether longer blocks exhibit the same behaviour. Correcting a damaged record and removing a genuine thermal fluctuation are different operations; thermal fluctuations belong to the liquid response.

## Connecting sampling windows with experimental conditions

One 200 ps trajectory supports several averages. The final 150 ps gives a relatively long observation window; splitting it into three 50 ps blocks shows how the summary varies with time. The measured block stresses are approximately 29.924, 35.508, and 35.146 MPa. Rebinning the saved water-atom velocities within each block and fitting the same central region gives stress-to-gradient ratios of approximately 1.182, 1.620, and 1.395 mPa·s. These values give the fluctuations behind the overall estimate a concrete form and identify the quantities to follow as sampling is extended.

All three blocks exclude the left endpoint and include the right: 50<t≤100, 100<t≤150, and 150<t≤200 ps. Each contains 100 coordinate frames. Wall forces use the same intervals, keeping the motion and resistance measurements on a consistent time definition.

### How estimates vary across observation windows

Three consecutive 50 ps windows provide separate profiles and stress-to-gradient ratios, showing temporal sampling sensitivity.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l11/en/#en-s8)

Three consecutive 50 ps intervals have separate force and central-gradient estimates, followed by their ratios. Block profiles are recomputed from trajectories saved every 0.5 ps using 1 Å spatial layers. They show time-window sensitivity and are distinguished from the native 0.25 Å bins pooled over 15000 samples.

Adjacent blocks inherit structure from earlier times. Their variation is therefore first a description of temporal sensitivity. To interpret an uncertainty interval in terms of independent repeats, construct separate velocity histories and apply the same preparation, drive, and analysis rules to each. Ion redistribution can be examined through ionic density profiles and displacement records. Temperature may reach a stable fluctuating range quickly while a slower structural quantity continues evolving. Each measurement has its own correlation time, and different records answer different parts of the sampling question.

A clear material-comparison design can fix water model, salt content, temperature, cell size, and drive while varying the water–wall interaction. Observe density layers, velocity profiles, and wall forces together. Changes in resistance can then be related to changes in interfacial organization. Changing wall chemistry, roughness, ion count, and area simultaneously combines several mechanisms in the same difference. A series with a shared reference and controlled variations gives the physical interpretation a firmer structure than a collection of viscosity numbers obtained under unrelated conditions.

For an experimental comparison, start by stating what the experiment measures. A rotational rheometer infers response from torque and macroscopic geometry. A microfluidic device may infer transport from pressure drop and flow rate. Surface-force measurements probe resistance between nearby materials. These approaches share momentum-transfer physics but use different geometries and drives. The closest target for the present model is nanoscale shear between uniform surfaces. A bulk low-rate electrolyte viscosity study instead calls for a bulk system, a sequence of lower driving rates, and longer sampling to examine the stress–rate relation.

A useful exercise requires no new molecular trajectory. Change the central fitting interval from ±8 Å to ±6 Å and compare the gradient and stress-to-gradient ratio. Then change the trajectory-analysis bin width from 1 Å to 2 Å and inspect the trade-off between local detail and noise. Wall stress retains the same observation window in both exercises. The changed result comes from organizing the spatial observations differently. Saving the selected range, samples, and units alongside the value makes this an exercise in measurement definition rather than an unexplained change in a material property.

The molecular animation can now be read in a physical sequence. Surfaces specify the drive, interactions transmit momentum, transverse thermostats manage heat, spatial bins reveal mean flow, wall forces measure resistance, and time windows describe the variation covered by the observation. A polymer solution, a charged interface, or a wider pore can be investigated through the same sequence of questions. New molecular mechanisms then enter through corresponding structural and dynamical measurements, with the loading and statistical definitions kept visible.

## Further Reading and Open Materials

- [Nanosheared electrolyte](https://lammpstutorials.github.io/sphinx/build/html/tutorial4/nanosheared-electrolyte.html) · Simon Gravelle,Cecilia M.S.Alvares,Jacob R.Gissinger,Axel Kohlmeyer · CC BY4.0

  TIP4P/2005 electrolyte construction, preparation, and moving-wall shear.

  Retains interactions, drive, and native binning; adds numerical trajectories, bilingual explanations, and time-block analysis.
- [Études sur le frottement des liquides(1890)](https://fr.wikisource.org/wiki/Études_sur_le_frottement_des_liquides) · Maurice Couette · Public-domain original scientific text;new schematics

  History of cylinder experiments and viscosity measurement.
- [compute temp/partial](https://docs.lammps.org/compute_temp_partial.html)
- [fix ave/chunk](https://docs.lammps.org/fix_ave_chunk.html)
- [fix setforce](https://docs.lammps.org/fix_setforce.html)
- [units](https://docs.lammps.org/units.html)
