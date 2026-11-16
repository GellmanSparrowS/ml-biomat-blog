# Why a Box of Particles Moves

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l01/en/
Language: en

Start with diffusion and liquid motion, build a box containing two particle types, and connect interactions, time evolution and thermal motion to a complete input, an actual trajectory and energy curves.

## From a drop of liquid to particles in a computer

Place a drop of ink gently in clear water. Even without continuous stirring, its colour gradually spreads. Cooling the liquid changes molecular motion, viscosity and the rate at which dissolved substances move. Our eyes see colour and shape, while the underlying process involves enormous numbers of changes in position and interactions. Molecular dynamics builds an explicit microscopic model, follows its evolution in time, and turns those changes into quantities related to material behaviour. This first lesson follows that entire route using a simple box of particles.

A particle is first of all an object in a model. It has a position, a mass and a velocity, and it interacts with neighbours according to specified rules. It may represent an atom or an effective unit combining several atoms. The radius of a sphere drawn on the screen is a display choice; the distance at which interactions become strong is set by the model parameters. Enlarging a rendered sphere changes the image. Increasing the repulsive length parameter changes the calculated motion. Here we use two neutral particle types with translational motion and short-range attraction and repulsion.

This model lets us examine aggregation, mixing and energy exchange, and see how a local interaction rule produces collective behaviour. Its simplicity also makes the calculation itself easier to understand. The bent shape of a water molecule, its charge distribution and the directional character of hydrogen bonding are absent from this neutral-particle description. Later lessons add the appropriate molecular structure when studying water and ions. By the end of this lesson, you should be able to explain the role of each input, distinguish structural relaxation from evolution in physical time, and interpret trajectories together with energy curves.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l01/en/#en-s1)

Figure 1 · The ID tracks one particle; its type selects parameters. Arrows show information links rather than forces.

Giving particles identification numbers resembles numbering people on a playing field: a number lets us recognise the same object at another time, but does not determine its material properties. A particle type instead indexes a parameter table. Particles of a type share the corresponding mass and interaction parameters. The tenth displayed point need not have the same identity in every frame, because file ordering can change. Tracking a particle therefore requires matching its ID, while comparing species requires grouping by type. This distinction continues to matter for molecules, long chains and networks.

A simulation links three questions: which objects are retained, how they interact, and how their motion is observed. An input file expresses those choices as commands. Coordinates and velocities describe the state at one instant. A potential function describes the energetic cost of changing that state. An integration method then advances it through a short interval. Output files record selected observations. A compact script can consequently contain a complete set of assumptions about the material, its environment and the quantities being measured. Understanding those roles is more useful than memorising the order of command names.

The exercise places two particle types in a three-dimensional periodic box, prepares their initial arrangement, and then follows motion and energy. One set of particle parameters is used throughout three consecutive stages: first the system evolves without a heat bath; next it exchanges energy with a bath at a prescribed temperature; finally the bath is removed. Following the same objects across these environments makes the role of the simulation conditions visible in an actual trajectory.

## Putting a large world inside a finite box

A real liquid contains far more molecules than an introductory calculation can track individually. One mole contains approximately 6.022 times ten to the power of twenty-three specified objects. A mole is a counting unit for a very large collection, just as a dozen counts twelve. We begin with a finite region whose particle number and density are explicit. Whether that region answers a particular question depends on the size of the structures and the time they need to change. A chain approaching the box size, for example, can interact with its periodic images, making box size an experimental variable in the simulation.

The example box extends from minus twenty to plus twenty in all three directions, so each side is forty units long, not twenty. It contains 1,500 particles of type 1 and 100 of type 2, giving 1,600 altogether. Multiplying the three side lengths gives the volume. Dividing particle number by volume gives number density: the average number assigned to a unit of volume. This starting number density is low, and the initial configuration is not a closely packed solid. Calling the model a fluid describes its ability to rearrange; it does not assign the density or phase of a particular real liquid in advance.

Number density: particles per unit volumeEq. 1

![Number density: particles per unit volume](https://ml-biomat.com/static/agent-math/1f1a9874b459f146bf7f5d3e.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ρₙ | Number density; the script keyword density instead reports mass density | σ₁₁⁻³ |
| N | Total number of particles | 1 |
| V | Simulation-box volume | σ₁₁³ |
| Lₓ, Lᵧ, L_{z} | Box lengths in the three directions | σ₁₁ |
| /, × | Division; adjacent lengths are multiplied | 1 |
| = | Equality defines number density and geometric volume. | operators and numerical coefficients are dimensionless |

Reading the relationshipMultiply the three lengths to obtain volume, then divide the particle count by that volume. Number density counts particles without weighting them by mass.

A worked exampleN = 1500 + 100 = 1600 and V = 40 × 40 × 40 = 64000, giving ρₙ = 0.025. Total mass is 1500 × 1 + 100 × 5 = 2000, so the mass density printed by LAMMPS is 2000 / 64000 = 0.03125.

ConditionsThis expression uses a three-dimensional orthogonal box and the first particle type as the reduced length reference. It is a box average; local regions may be denser.

Hard walls would give particles near a boundary a different environment from particles in the interior. To study an approximately uniform bulk system, we often use periodic boundaries: repeat the box in every direction and let a particle leaving one face re-enter through the opposite face. Interactions account for the corresponding images. Seamlessly repeating wallpaper is a useful analogy, extended here to three dimensions. A particle may appear to jump across the display, although its physical path remains continuous. Displacement analysis must retain boundary crossings so that the continuous path can be reconstructed.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l01/en/#en-s2)

Figure 2 · One particle follows a continuous path across the seam. Periodic wrapping maps coordinates into the box and can create a visual jump.

Periodicity also affects distance calculations. In a one-dimensional box of length ten, particles at 0.2 and 9.8 differ by 9.6 if their displayed coordinates are subtracted directly. Across the periodic seam, however, their nearest separation is 0.4. Short-range forces use an appropriate neighbouring image. The interaction cutoff must be compatible with the box geometry so that images of the same neighbour are not treated as independent nearby particles. In our cubic example, a side length of forty and a global cutoff of four leave a clear separation between the interaction range and half the box length.

Once particle number, box geometry and boundaries are explicit, changes to the simulation have an interpretable meaning. Shrinking the box at fixed particle number raises the number density and increases opportunities for encounters. Increasing particle number together with volume at fixed density mainly changes the structural scales and sampling capacity available. These are different comparisons. The first examines a denser system; the second examines finite-size effects. Naming the controlled quantity prevents a change in particle count from being mistaken for an explanation of a material mechanism.

## Writing attraction and repulsion as an energy landscape

Before particles can move, the computer needs a rule for what happens when they approach. Potential energy is energy associated with an arrangement of positions. Separating two attracting particles requires work from outside, and forcing strongly repelling particles together also requires work. Plot separation horizontally and potential energy vertically to obtain an energy curve. A low point corresponds to a favourable arrangement for that pair. A whole system also contains other neighbours, thermal motion and geometric constraints, so the minimum of a single pair potential does not by itself determine the arrangement of all particles.

The Lennard–Jones potential combines short-range repulsion and longer-range attraction in a simple expression. The ratio sigma divided by separation has no units. Its twelfth power rises rapidly as separation decreases, while the sixth-power term provides attraction. The twelfth power is convenient computationally; it does not describe a literal mechanical spring inside an electron cloud. The function represents an effective interaction. Epsilon sets the depth of the potential well and sigma its distance scale. Mass supplies different information: it determines acceleration under a given force, whereas potential parameters determine the interaction generated by a configuration.

The truncated Lennard–Jones potential used hereEq. 2

![The truncated Lennard–Jones potential used here](https://ml-biomat.com/static/agent-math/589524aba471288945c63ef5.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| U(r) | Potential energy of this particle pair | ε₁₁ |
| r | Distance between particle centres | σ₁₁ |
| ε | Well depth for this pair of types | ε₁₁ |
| σ | Zero-crossing distance scale for this pair | σ₁₁ |
| r_{c} | Interaction cutoff; 4 for every pair in this example | σ₁₁ |
| 12, 6 | Powers of the dimensionless distance ratio | 1 |
| <, ≥ | Conditions selecting the appropriate branch | 1 |
| =, /, −, ×, [ ], 4, 0 | Equality defines the piecewise energy; division forms a dimensionless ratio; subtraction combines repulsion and attraction; adjacent factors multiply; brackets group terms;4 is a numerical coefficient and0 the energy assigned beyond the cutoff. | operators and numerical coefficients are dimensionless |

Reading the relationshipThe twelfth-power term grows rapidly at short distances; subtracting the sixth-power term produces an attractive well. The ratio σ/r is dimensionless, so multiplication by ε gives an energy.

A worked exampleFor type 1, ε = σ = 1. At r = 1, U = 4(1 − 1) = 0. At r = 2^(1/6) ≈ 1.122462, the twelfth- and sixth-power terms equal 1/4 and 1/2, so U = −1.

ConditionsThis example uses neither an energy shift nor a long-range tail correction. The energy is generally discontinuous at the cutoff, which can affect the energy trace when pairs cross it. A pair minimum does not prescribe every separation in a many-particle system.

At a separation equal to sigma, the potential is zero. Its minimum lies at about 1.122 sigma, with energy minus epsilon. Zero potential is a reference value, not a statement that the force vanishes there. A hillside offers a useful analogy: the same altitude can occur on an uphill slope, a downhill slope or level ground. The local tendency to move depends on slope. Similarly, the potential minimum has zero slope. Very close particles are pushed apart because approaching raises energy sharply; at suitable larger separations, attraction favours approach. We will repeatedly use this distinction between energy and slope.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l01/en/#en-s3)

Figure 3 · The zero crossing is at σ and the minimum near 1.122σ. Zero force corresponds to a horizontal tangent. The curve is evaluated from the analytical LJ expression.

Two particle types require three pair interactions: type 1 with itself, type 2 with itself, and the cross interaction. The example specifies the first two and obtains cross parameters from geometric means. A geometric mean multiplies two positive values and then takes the square root; it is not their arithmetic midpoint. Type 2 has five times the mass, three times sigma and half epsilon of type 1. These alter inertia, effective size and attraction separately. Their combined effect cannot be compressed into the claim that larger particles are simply slower. Speed comparisons also involve temperature, mass and local surroundings.

Geometric mixing for unlike particle typesEq. 3

![Geometric mixing for unlike particle types](https://ml-biomat.com/static/agent-math/3042936304a31731d2dde39b.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ε₁₁, ε₂₂, ε₁₂ | Like-pair and unlike-pair well depths | ε₁₁ |
| σ₁₁, σ₂₂, σ₁₂ | Like-pair and unlike-pair length scales | σ₁₁ |
| 11, 22, 12 | The two interacting particle types | 1 |
| √ | The nonnegative square root | 1 |
| =, × | Equality specifies cross parameters; multiply the adjacent like-pair parameters under the square root. | operators and numerical coefficients are dimensionless |

Reading the relationshipMultiplication followed by a square root gives an unlike-pair value between the two positive like-pair values, with the correct units. The input explicitly selects it with pair_modify mix geometric.

A worked exampleε₁₂ = √(1 × 0.5) ≈ 0.707107 and σ₁₂ = √(1 × 3) ≈ 1.732051. The unlike-pair minimum is consequently at a distance of about 1.94416.

ConditionsThis is a choice made by this model. Other force fields use arithmetic mixing, fitted unlike-pair parameters or other rules; their mixing convention travels with the model.

A calculation also specifies how far an interaction extends. Here the Lennard–Jones term is cut off at a distance of four, so that pair contribution is omitted beyond that range. A cutoff reduces computational cost and changes the model relative to the infinite-range expression. Whether the energy is shifted or a long-range tail correction is added is also part of the model definition; those choices must stay explicit in comparisons. This lesson retains the public example’s cutoff convention. The third lesson uses energy histories to examine its numerical behaviour alongside the choice of time step.

Move the separation and read the pair energy and radial force. Positive force increases the separation.

[Figure: Schematic pair at adjustable separation](https://ml-biomat.com/tutorials/molecular-dynamics/l01/en/#en-s3)

Analytic pair exercise with ε = σ = 1. Radial force is minus the slope of energy against separation and describes the tendency to approach or separate. The current separation determines the displayed analytic values.

## How local rules advance a moving system

Coordinates tell us where a particle is. Velocity tells us its direction of motion and how rapidly it moves, usually through three components along the coordinate axes. Force also has direction and changes velocity; mass relates force to the rate of that change. A particle can continue moving with its existing velocity even when its instantaneous net force is zero. Conversely, a particle initially at rest begins accelerating if its net force is nonzero. Having no initial velocity therefore does not imply remaining motionless forever. The initial arrangement and the forces it generates matter as well.

How force changes velocity along one directionEq. 4

![How force changes velocity along one direction](https://ml-biomat.com/static/agent-math/8b6ddbbb9024ecb737b7d256.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| aₓ | Acceleration along x: velocity change per unit time | σ₁₁/τ² |
| Fₓ | Net force component along x | ε₁₁/σ₁₁ |
| m | Particle mass | m₁ |
| τ | Reduced time reference, developed in the next lesson | time |
| =, /, x | Equality gives the component of Newton’s second law; divide force by mass; subscript x identifies the spatial direction. | operators and numerical coefficients are dimensionless |

Reading the relationshipNewton’s second law links motion to net force. Under the same force, a larger mass produces a smaller rate of velocity change. The other two directions obey corresponding equations.

A worked exampleIn reduced units, Fₓ = 2 and m = 4 give aₓ = 0.5. If the force is approximately constant over 0.1 time units, the x velocity increases by about 0.05.

ConditionsThis is classical translational dynamics with positive mass. Net force combines the vector components of all relevant interactions and applied forces. Zero force permits a nonzero velocity.

A computer does not record an infinite sequence of infinitesimal instants. It approximates motion through small time intervals. After each step, it updates positions and velocities, recalculates interactions and continues. Like photographing an action, a coarse interval can miss rapid changes. An integrator also uses force information to predict motion, so it is more than drawing a straight line between two photographs. The step must resolve the fastest relevant motion retained in the model. Its suitability is established through numerical comparisons rather than inferred from a simulation reaching the end of its input file.

Multiplying the number of steps by their duration gives the simulated elapsed time. The output interval instead determines how many records are saved. Saving one frame every hundred steps does not mean that forces are calculated only at those saved times. Motion advances through all the intervening integration steps; the trajectory simply omits most of them. Sparse output loses details of rapid processes, whereas very dense output increases storage and analysis work. The observation frequency should follow the time scale of the motion being studied and the temporal resolution needed to answer the question.

Steps, elapsed time and recording intervalsEq. 5

![Steps, elapsed time and recording intervals](https://ml-biomat.com/static/agent-math/6ecf085e071d0a4986257f68.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| t | Simulated time elapsed from the selected origin | τ |
| n | Number of integration steps | 1 |
| Δt | Time advanced by one integration step | τ |
| q | Integration steps between records | 1 |
| Δt_{out} | Time between saved records | τ |
| Δ | Denotes an interval or increment | 1 |
| =, ×, out | Equality connects counts and time; adjacent factors multiply; subscript out labels output records. | operators and numerical coefficients are dimensionless |

Reading the relationshipFor equal time steps, adding the same interval n times is multiplication. Output selects only some of those integrated states for storage.

A worked exampleHere Δt = 0.005. The initial 5000 steps span 25, the 15000-step bath interval spans 75, and the final 10000 steps span 50, totalling 150. Trajectory frames saved every 200 steps are 1 time unit apart; thermodynamic records every 100 steps are 0.5 apart.

ConditionsA fixed time step is assumed. Minimization iterations have no corresponding dynamical time, and the exact frame count depends on saved initial and interval endpoints. Read the file to determine it.

Checking every pair becomes expensive as particle number grows. Short-range interactions offer an opportunity: maintain candidate neighbours near the cutoff and update them as particles move. [Plimpton’s 1995 paper on parallel algorithms](https://doi.org/10.1006/jcph.1995.1039) compared assigning work by particles, by forces and by spatial regions. With spatial decomposition, processors work on nearby particles and exchange the boundary information they need. This history explains a central design choice: computational work is organised around the locality of interactions, rather than around the spheres displayed by a visualisation program.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l01/en/#en-s4)

Figure 4 · The historical problem was efficient calculation of many short-range interactions. Spatial decomposition distributes regions while exchanging neighbour information at their boundaries. The regions illustrate the spatial-decomposition concept.

Small differences between parallel runs also become understandable in this picture. Summing the same forces in a different order can slightly change floating-point rounding. As dynamics evolves, those small differences may eventually alter individual particle paths. Comparisons between valid runs therefore examine conservation, statistical distributions and relevant observables together. Requiring every coordinate to remain bitwise identical at long times serves some tightly defined regression tests, but is not the sole general test of a material’s statistics. Recording versions, inputs and seeds, then comparing physical statistics, gives a fuller approach to reproducibility.

For now, think of integration as advancing time from a state and its forces. The third lesson develops the two half-step updates of velocity Verlet and explains how positions, velocities and old and new forces connect. This sequence lets you understand the roles of the quantities during a first run, then examine the algorithm when analysing energy errors. The chain of reasoning is direct: a potential supplies forces, masses determine the response, an integrator advances the state, and output records observations. Together they turn an initial structure into a trajectory with a defined time axis.

## Minimisation and dynamics answer different questions

Random placement is convenient, but can put some particles too close together. The steep short-range Lennard–Jones potential then produces large repulsive forces. Advancing immediately with an ordinary time step may move a particle too far in one update, turning an initial-placement problem into a numerical one. Energy minimisation first changes coordinates to reduce potential energy and relieve unfavourable close contacts. Arranging objects that were carelessly packed into a drawer is a useful analogy: it prepares a starting configuration, but does not assign a physical duration in seconds to the rearrangement.

Minimisation iterations count optimisation updates, while dynamics steps count advances of a time integrator. Both can appear as numbered rows in a log, but they should not be joined into one physical time axis. During minimisation, potential energy generally moves downward. The algorithm may stop because forces are sufficiently small, energy changes are sufficiently small, or an iteration limit has been reached. Read the stopping reason. Reaching the iteration limit calls for inspection of remaining forces and close contacts; the fact that an optimisation stopped does not by itself identify an equilibrated thermodynamic state.

A deeper distinction is that a finite-temperature system continually explores many configurations. A locally minimal potential-energy structure need not be the most frequently visited overall state, because the number of configurations available to a state also affects its probability. Imagine one region with a single exceptionally comfortable seat and another with many moderately comfortable seats. Asking for the best individual seat differs from asking where a crowd is commonly found. Minimisation prepares a starting point; thermal motion and sampling reveal a finite-temperature distribution. This distinction becomes especially useful for chain conformations, membranes and free energies.

The following NVE calculation keeps particle number N and volume V fixed, while tracking energy E under the chosen conservative model and numerical approximation. Potential and kinetic energy can exchange. For example, particles approaching through an attractive region may lose potential energy while gaining speed. Looking only at increasing kinetic energy can suggest unexplained heating. Plotting potential energy beside it shows where the energy came from. Cutoff treatment, time-step size and rounding affect the numerical energy history; the third lesson separates those effects through controlled comparisons.

Kinetic energy and total model energyEq. 6

![Kinetic energy and total model energy](https://ml-biomat.com/static/agent-math/2b0d19028fd552c116fc074f.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| K | Total translational kinetic energy | ε₁₁ |
| N, i | Particle count and summation index | 1 |
| mᵢ | Mass of particle i | m₁ |
| vᵢ | Three-dimensional velocity of particle i | σ₁₁/τ |
| \|vᵢ\|² | Sum of squared velocity components | σ₁₁²/τ² |
| Σ | Add contributions for particles i = 1 through N | 1 |
| U, E | Total potential and total energy | ε₁₁ |
| =, +, ×, 1/2 | Equality defines energies; addition combines kinetic and potential terms; adjacent factors multiply;1/2 is the kinetic-energy coefficient. | operators and numerical coefficients are dimensionless |

Reading the relationshipEach particle has kinetic energy determined by its mass and squared speed. Summing those contributions and adding the interaction energy gives the mechanical energy of this model.

A worked exampleFor two particles of mass 1 with speeds 1 and 2, K = 0.5 × 1² + 0.5 × 2² = 2.5. If U = −1, E = 1.5. Per-particle values are 1.25, −0.5 and 0.75, respectively.

ConditionsThis model contains translational degrees of freedom. An NVE energy check requires consistent normalization and attention to cutoff and integration errors. A thermostat additionally exchanges energy with the surroundings.

A heat bath lets the model exchange energy with an environment at a specified temperature. Langevin thermostatting represents that contact with velocity-dependent drag and random forces. Drag removes kinetic energy, while random forcing supplies thermal motion; their strengths are linked through temperature and damping. It does not force every particle to move at one speed, and the measured temperature fluctuates around its target. In this example, the Langevin command modifies forces while a separate NVE integrator updates positions and velocities. The name of that integrator does not make the thermostatted system isolated from energy exchange.

When reading staged results, identify both the horizontal axis and the environment. A minimisation plot uses optimisation iterations. An NVE plot uses integration time and highlights energy exchange and numerical conservation. An NVT calculation exchanges energy with a heat bath, so attention shifts to the temperature distribution and evolving structural and energetic statistics. Showing the stages together helps explain the workflow, while each retains its own interpretation. The actual results below keep coordinate relaxation, isolated evolution and contact with a heat bath distinct.

## Read the complete input, then run it

A LAMMPS input file is plain text executed in order. A command line is an entry point for concrete tasks: provide a program name and arguments, and the program reads files, computes and writes information to the screen or disk. Here lmp names the executable, and the value following -in identifies its input file. Relative filenames are resolved from the current working directory. Running from a clearly defined exercise directory makes outputs easier to associate with their inputs. Confirm the program version from its help text or log header; the course compares inputs and results using one fixed version.

### Check the executable and run the example

```
lmp -help
lmp -in initial.lmp
```

Run from the exercise directory containing initial.lmp. The first command reports the version and available capabilities; the second reads the full input and creates a log, thermo.dat, trajectory and restart files.

The beginning of the complete script defines units, dimensionality, particle attributes and boundaries. The lj unit style uses reduced scales: reference values for mass, length and energy are chosen, and quantities are expressed relative to them. Dimension 3 specifies motion in three dimensions. Atom_style atomic represents particles without explicit bonds, charges or molecular topology. Boundary p p p makes all three directions periodic. Writing these settings explicitly, including defaults, exposes the model assumptions and gives later changes to the system a clearly identifiable place in the input.

Region describes a geometric region; create_box constructs a simulation box and allocates types; create_atoms then inserts particles. The two random insertions use fixed seeds so the initialisation procedure can be repeated. A seed is the starting point of a pseudorandom generator, not a temperature or material property. Enforcing a minimum insertion distance reduces very close contacts, but the two particle types have different effective sizes. A single geometric separation still needs to be assessed together with potential energy and minimisation. Read geometric conditions and interaction length scales as connected choices.

Mass, pair_style and pair_coeff connect numerical values to physical roles. Naming a potential does not complete its definition: the existing types, parameters for each pair, mixing rule and cutoff all matter together. Thermo and thermo_style choose the quantities and intervals written to the log; dump chooses particle attributes and trajectory frequency. These generally change observation rather than the underlying model. If changing only recording frequency appears to change the physics substantially, investigate whether integration, randomness or another associated setting also changed.

### Complete input for the binary-particle system

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

# PART A - ENERGY MINIMIZATION
# 1) Initialization
units lj
dimension 3
atom_style atomic
boundary p p p

# 2) System definition
region simbox block -20 20 -20 20 -20 20
create_box 2 simbox
create_atoms 1 random 1500 34134 simbox overlap 0.3
create_atoms 2 random 100 12756 simbox overlap 0.3

# 3) Settings
mass 1 1.0
mass 2 5.0
pair_style lj/cut 4.0
pair_coeff 1 1 1.0 1.0
pair_coeff 2 2 0.5 3.0


# Tutorial extension: numerical records, NVE/NVT comparison and restart files.
# Original particle population, box, pair coefficients and random seeds are kept.
# Output units: reduced LJ; energy values below are per atom.
pair_modify mix geometric
thermo 10
thermo_style custom step pe press
minimize 1.0e-6 1.0e-6 1000 10000
reset_timestep 0
velocity all create 1.0 49284 mom yes dist gaussian
timestep 0.005
thermo 100
thermo_style custom step time temp pe ke etotal press density
thermo_modify norm no flush yes
variable t equal time
variable T equal temp
variable U equal pe/atoms
variable K equal ke/atoms
variable E equal etotal/atoms
variable P equal press
variable rho equal density
fix records all ave/time 100 1 100 v_t v_T v_U v_K v_E v_P v_rho file thermo.dat
dump coordinates all custom 200 trajectory.lammpstrj id type x y z vx vy vz ix iy iz
dump_modify coordinates sort id
fix integrator all nve
# First NVE interval: 25 reduced time units.
run 5000
# NVT interval: 75 reduced time units, Langevin bath from the original tutorial.
fix bath all langevin 1.0 1.0 0.1 10917 zero yes
run 15000
unfix bath
write_restart equilibrated.restart
# Final isolated interval: 50 reduced time units.
run 10000
write_restart final.restart
write_data final.data
```

The upstream particle populations, box, masses, pair parameters and positional seeds are retained. Numerical records and restart files are added. Dynamics spans 25, 75 and 50 reduced time units, with a Langevin bath during the middle interval.

During a run, locate the starting particle count, minimisation stopping reason, output tables for the dynamics stages and final completion information. The log records what the calculation did, while the trajectory records which particles were where. Preserve both. Reusing the same output names can overwrite earlier files, so parameter comparisons should retain separate directories and copies of their inputs. Names that describe physical conditions are more dependable than reconstructing a curve’s meaning from memory. This lesson establishes one complete run; the next makes the relationships between its files explicit.

If a command is unrecognised, first check the version and spelling. If a file is missing, check the working directory and relative path. If particles are lost or energies become enormous, inspect initial geometry, parameter units, time step and neighbour updates. These checks address syntax, file organisation and physical numerics respectively. This order turns errors into identifiable questions and avoids extending a simulation whose initial overlaps remain unresolved. Each correction should identify the layer it changes and the observable that will reveal its effect after rerunning.

## Read trajectories and curves together

A trajectory supplies spatial information: are particles dispersed, do transient clusters form, do the two types occupy similar environments, and has a periodic seam split a cluster in the display? Energy histories reveal collective changes. Smooth-looking animation can hide continuing energy drift, while a single average can conceal slowly changing structure. Connecting a trajectory to statistics from the same time interval turns visible motion into an explanation of a specified model. The trajectory below comes from the lesson’s actual run. Colour identifies particle type, and its legend separates display size from interaction parameters.

### Trajectory from the binary-particle run

Actual coordinates are coloured by particle type. Playback identifies simulation time and stage, with wrapped positions shown in the periodic box.

LAMMPS 30 Sep 2026 update 1; a three-dimensional periodic box with 1,500 type-1 and 100 type-2 particles. Reduced units, time step 0.005 and total duration 150. Physical inputs follow the binary Lennard–Jones tutorial by Gravelle and colleagues, with added NVE comparisons and numerical output.

[Download reference data and complete inputs (ZIP) 6.73 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-lj-reference-data.zip)

Before reading an energy axis, determine whether it shows a total for the entire system or a quantity divided by particle number. With LJ units, LAMMPS normally normalises some extensive thermodynamic outputs by particle count; potential and kinetic energy are examples. Temperature and pressure follow their own definitions. A total potential energy of minus eight hundred for sixteen hundred particles corresponds to minus one half per particle. Both describe the same state. Adding a total-energy curve directly to a per-particle curve, however, would mix incompatible normalisations.

Temperature also needs a definition in terms of motion. Translational degrees of freedom count independent velocity components; an unconstrained particle in three dimensions normally contributes three. Overall translation, rigid constraints and other removed motions alter that count. Our model has no molecular constraints. Its default temperature calculation subtracts three degrees of freedom for overall translation, leaving 4,797 for 1,600 particles rather than 4,800. The difference is small here, but making it explicit prepares us for water, rigid bodies and small particle groups, where degree-of-freedom choices can have more visible effects.

This input explicitly sets thermo_modify norm no so that pe, ke and etotal in the log retain system totals. The recording variables divide each by the particle count to write per-particle energies to thermo.dat. Log energies therefore differ from the figure values by the particle-count factor, rather than describing different physics. Reading the setting before the column names prevents automatic normalisation from being combined unintentionally with another division.

Defining instantaneous temperature from motionEq. 7

![Defining instantaneous temperature from motion](https://ml-biomat.com/static/agent-math/3727bd68d879c192724c8c0b.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| T | Instantaneous temperature defined by this compute | ε₁₁/k_B |
| K | Total translational kinetic energy included in the temperature calculation | ε₁₁ |
| f | Number of velocity degrees of freedom | 1 |
| k_{B} | Boltzmann constant connecting temperature and energy; numerically 1 in reduced LJ units | energy/temperature |
| N | Number of particles | 1 |
| 3N − 3 | Three velocity components per particle, less the default three translational degrees of freedom | 1 |
| =, /, ×, −, 2, 3 | Equality defines temperature and degrees of freedom; divide numerator by denominator; adjacent factors multiply; subtract overall translation;2 comes from equipartition and3 counts spatial directions. | operators and numerical coefficients are dimensionless |

Reading the relationshipAt classical equilibrium, each quadratic velocity degree of freedom contributes k_BT/2 to the mean kinetic energy. Reversing that relation defines an instantaneous temperature estimator, which fluctuates with kinetic energy.

A worked exampleFor N = 1600, f = 4797. At T = 1 and k_B = 1, K = 4797/2 = 2398.5, or 1.4990625 per particle. Substituting a per-particle energy for K would omit a factor of 1600.

ConditionsThis is the default LAMMPS degree-of-freedom convention for an unconstrained three-dimensional system. Rigid constraints, flow bias, selected particle groups and custom temperature computes require corresponding treatment.

### Exchange between potential and kinetic energy

Per-particle potential, kinetic and total energies plus temperature from the same input. Stage boundaries occur at t = 25 and t = 100; the run ends at t = 150.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l01/en/#en-s7)

All saved records, with energies divided by particle count. Shading marks the Langevin bath at t* = 25–100; the surrounding stages are NVE. The target-temperature line appears only while the bath is active.

### Reproduce energy and coordinate plots from the same run

```
"""Read the binary-particle tutorial outputs and reproduce the record plots.

Requires Python 3, NumPy and Matplotlib. All paths are relative by default.
Run: python analyze_records.py --data-dir . --out-dir analysis
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def read_selected_path(filename, particle_id, timestep=0.005):
    rows = []
    with Path(filename).open(encoding='utf-8') as stream:
        while True:
            first = stream.readline()
            if first == '':
                break
            if first.strip() != 'ITEM: TIMESTEP':
                raise ValueError('Expected a TIMESTEP frame header.')
            step = int(stream.readline())
            if stream.readline().strip() != 'ITEM: NUMBER OF ATOMS':
                raise ValueError('Missing particle-count header.')
            count = int(stream.readline())
            box_header = stream.readline().split()
            if box_header[:3] != ['ITEM:', 'BOX', 'BOUNDS']:
                raise ValueError('Missing box-bounds header.')
            if any(name in box_header for name in ('xy', 'xz', 'yz', 'abc')):
                raise ValueError('This reader expects the fixed orthogonal tutorial box.')
            bounds = np.array([list(map(float, stream.readline().split()))
                               for _ in range(3)])
            if bounds.shape != (3, 2):
                raise ValueError('Expected three lower/upper box bounds.')
            names_line = stream.readline().split()
            if names_line[:2] != ['ITEM:', 'ATOMS']:
                raise ValueError('Missing particle-column header.')
            names = names_line[2:]
            required = ['id', 'x', 'ix']
            missing = [name for name in required if name not in names]
            if missing:
                raise ValueError('Required trajectory fields: ' + ', '.join(missing))
            columns = {name: names.index(name) for name in required}
            chosen = None
            ids = set()
            for _ in range(count):
                fields = stream.readline().split()
                if len(fields) != len(names):
                    raise ValueError('Incomplete particle record.')
                atom_id = int(fields[columns['id']])
                if atom_id in ids:
                    raise ValueError('Duplicate particle ID in one frame.')
                ids.add(atom_id)
                if atom_id == particle_id:
                    x = float(fields[columns['x']])
                    image = int(fields[columns['ix']])
                    length = bounds[0, 1] - bounds[0, 0]
                    chosen = (step * timestep, x, x + image * length)
            if chosen is None:
                raise ValueError(f'Particle {particle_id} absent from a frame.')
            rows.append(chosen)
    data = np.asarray(rows, dtype=float)
    if data.ndim != 2 or data.shape[1] != 3 or len(data) < 2:
        raise ValueError('At least two complete trajectory frames are required.')
    if not np.all(np.diff(data[:, 0]) > 0):
        raise ValueError('Trajectory times must increase strictly.')
    return data


def load_thermo(filename):
    table = np.loadtxt(filename, comments='#', ndmin=2)
    if table.shape[1] != 8 or len(table) < 2:
        raise ValueError('Expected eight columns: step,time,T,U/N,K/N,E/N,P,mass_density.')
    if not np.all(np.isfinite(table)) or not np.all(np.diff(table[:, 1]) > 0):
        raise ValueError('Thermodynamic data must be finite and strictly ordered in time.')
    return table


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=Path('.'))
    parser.add_argument('--out-dir', type=Path, default=Path('analysis'))
    parser.add_argument('--particle', type=int, default=1)
    parser.add_argument('--window', type=float, nargs=2, default=[50.0, 100.0])
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args()
    if args.window[0] >= args.window[1]:
        raise ValueError('The analysis window must have positive duration.')
    table = load_thermo(args.data_dir / 'thermo.dat')
    step, time, temperature, potential, kinetic, energy, pressure, density = table.T
    path = read_selected_path(args.data_dir / 'trajectory.lammpstrj', args.particle)
    selected = (time >= args.window[0]) & (time < args.window[1])
    if np.count_nonzero(selected) < 2:
        raise ValueError('The selected window needs at least two records.')
    residual = energy - kinetic - potential
    summary = {
        'thermodynamic_rows': int(len(table)),
        'trajectory_frames': int(len(path)),
        'particle_id': args.particle,
        'window_reduced_time_left_inclusive_right_exclusive': args.window,
        'window_records': int(np.count_nonzero(selected)),
        'mean_temperature_reduced': float(temperature[selected].mean()),
        'temperature_sample_standard_deviation_not_standard_error':
            float(temperature[selected].std(ddof=1)),
        'max_energy_sum_residual_per_particle': float(np.max(np.abs(residual))),
        'x_displacement_reduced': float(path[-1, 2] - path[0, 2]),
        'mean_mass_density_reduced': float(density.mean()),
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / 'record-summary.json').write_text(
        json.dumps(summary, indent=2), encoding='utf-8')
    np.savetxt(args.out_dir / 'selected-particle-path.csv', path, delimiter=',',
               header='time_reduced,x_wrapped,x_unwrapped', comments='')
    zh = args.language == 'zh'
    plt.rcParams.update({'font.family': ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC', 'WenQuanYi Zen Hei', 'DejaVu Sans'] if zh else ['DejaVu Sans'], 'font.size': 14,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.labelcolor': '#173c42', 'text.color': '#173c42',
                         'xtick.color': '#50656a', 'ytick.color': '#50656a',
                         'svg.fonttype': 'path'})
    fig, axes = plt.subplots(3, 1, figsize=(11.5, 10), sharex=True,
                             layout='constrained')
    fig.set_facecolor('#faf9f5')
    for ax in axes:
        ax.set_facecolor('#faf9f5')
        ax.axvspan(25, 100, color='#e4eeeb', zorder=0)
        ax.grid(axis='y', alpha=0.18)
        ax.set_xlim(0, 150)
    axes[0].plot(time, temperature, color='#177c83', linewidth=1.0)
    axes[0].hlines(1, 25, 100, color='#a76d45', linewidth=1, linestyle='--',
                    label='热浴目标：25 ≤ t < 100' if zh else 'Bath target: 25 ≤ t < 100')
    axes[0].set_ylabel(('温度 ' if zh else 'Temperature ') + r'$k_B T / \epsilon_{11}$')
    axes[0].legend(frameon=False, loc='best')
    for values, name, color in [(potential, '势能 U/N' if zh else 'Potential U/N', '#496fa8'),
                                (kinetic, '动能 K/N' if zh else 'Kinetic K/N', '#bd7548'),
                                (energy, '总能量 E/N' if zh else 'Total E/N', '#177c83')]:
        axes[1].plot(time, values, label=name, color=color, linewidth=1.1)
    axes[1].set_ylabel(('每粒子能量 / ' if zh else 'Energy per particle / ') + r'$\epsilon_{11}$')
    axes[1].legend(frameon=False, ncol=3, loc='best')
    axes[2].plot(path[:, 0], path[:, 1], color='#bb754a', linewidth=0.9,
                 alpha=0.75, label='显示坐标 x' if zh else 'Wrapped x')
    axes[2].plot(path[:, 0], path[:, 2], color='#177c83', linewidth=1.5,
                 label='展开坐标 x' if zh else 'Unwrapped x')
    axes[2].set_ylabel(('位置 / ' if zh else 'Position / ') + r'$\sigma_{11}$')
    axes[2].set_xlabel(('约化时间 ' if zh else 'Reduced time ') + r'$t/\tau$')
    axes[2].legend(frameon=False, loc='lower center', bbox_to_anchor=(.5, 1.02), ncol=2, title=f'粒子编号 {args.particle}' if zh else f'Particle ID {args.particle}')
    fig.suptitle('同一次运动，不同记录\n两类 LJ 粒子 · NVE → Langevin 热浴 → NVE' if zh else
                 'One run, several records\nLJ binary particles · NVE → Langevin bath → NVE',
                 fontsize=17, x=0.07, ha='left')
    fig.savefig(args.out_dir / f'records-{args.language}.png', dpi=200)
    fig.savefig(args.out_dir / f'records-{args.language}.svg')
    # The first two panels reproduce the figure embedded in Lesson 1.
    axes[2].set_visible(False)
    axes[1].tick_params(labelbottom=True)
    axes[1].set_xlabel(('约化时间 ' if zh else 'Reduced time ') + r'$t/\tau$')
    axes[0].set_position([0.11, 0.55, 0.86, 0.31])
    axes[1].set_position([0.11, 0.13, 0.86, 0.33])
    fig.set_layout_engine(None)
    fig.set_size_inches(11.5, 8.0)
    fig.suptitle('温度与能量如何随阶段改变' if zh else 'Temperature and energy across the run stages',
                 fontsize=17, x=0.11, y=0.96, ha='left')
    fig.savefig(args.out_dir / f'energy-temperature-{args.language}.png', dpi=200)
    fig.savefig(args.out_dir / f'energy-temperature-{args.language}.svg')
    plt.close(fig)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    run()
```

Place the program with thermo.dat and trajectory.lammpstrj and run python analyze_records.py --language en or --language zh. It reads the numerical output and reproduces temperature, per-particle energy and continuous-coordinate plots. Lesson 2 develops the reading method.

In the NVE stage, opposing changes in potential and kinetic energy reveal exchange between configuration and motion. Examine total energy in relation to the step size, cutoff and recording precision. In NVT, temperature approaches the prescribed range and fluctuates around it. The useful objects are a distribution and an average over a suitable interval, not a demand that every printed value equal the target. If mean potential energy still differs strongly between successive intervals, inspect continued structural adjustment and distinguish the initial transient from the data used for statistics. Temperature alone does not track every slow structural process.

An average is computed by adding readings from a selected interval and dividing by their number. Adjacent records are often correlated, however, so a thousand saved rows need not provide a thousand independent observations. Watching an unchanged posture every second adds records faster than it adds new information. For now, state which stage and time interval supply an average. Lesson fifteen develops block averages, correlation times and independent repetitions, connecting error bars to the amount of information actually obtained rather than simply to the number of lines in a file.

## Use one small change to build a useful comparison

After a first run, a useful next step is to change one clearly identified condition. For example, keep particle number, box size and potential parameters fixed, raise the heat-bath target temperature, then compare speed distributions, energies and clustering. Higher temperature increases the scale of thermal motion, while the resulting structure depends jointly on interaction strength, density and sampling. Changing the box, particle count and interaction strength at the same time would make even a large difference difficult to attribute. A controlled comparison begins with a precise statement of what was changed and what was held fixed.

Another comparison changes the mass of type 2 while keeping its interaction parameters and the temperature fixed. At the same kinetic-energy scale, a larger mass usually corresponds to a smaller speed scale, so dynamical processes can slow down. The configurational potential has not changed, however, and neither has its role in the classical equilibrium distribution. This separates the speed of motion from the preference among configurations. Over a short observation period, a slower system may explore less configuration space, causing finite sampling to affect the observed distribution. Even this simple exercise connects dynamics with equilibrium statistics.

Keep units and normalisations consistent in every comparison. After changing particle number, check whether energy is total or per particle. After changing the box, check density. After changing the time step, compare equal simulated durations rather than equal step counts. A random seed introduces another kind of variation: model parameters stay fixed while initial positions or the random thermostat history change. Results from several seeds reveal between-run variability, helping distinguish a persistent trend from a feature peculiar to one trajectory.

For biomaterials, the value of this first example is an observational language that can grow. Connecting particles into polymer chains adds connectivity constraints. Introducing water and ions adds charges, molecular geometry and long-range interactions. Building a crosslinked network makes system-spanning connectivity important. Every model still needs explicit objects, interactions, boundaries, time evolution and observables. The basic case separates those ingredients, so each later increase in complexity can be understood as a specific addition rather than as an entirely new collection of unexplained commands.

Three questions help test your understanding. Why are minimisation iterations not converted into seconds? Why does a jump at a periodic boundary not imply a physical teleportation? Why can total energy change after adding a heat bath while temperature still fluctuates around its target? Answering requires connections between computational steps and physical meaning, beyond recalling command names. Write your own explanation first, then compare it with the relevant figures and equations. The answers below also provide a compact conceptual check before repeating the calculation.

Read the explanation

Minimisation searches for coordinates with lower potential energy rather than advancing physical time with the dynamics equations. Periodic display maps a continuous path back into the box, so wrapped coordinates jump while the path can be unwrapped. A heat bath exchanges energy through drag and random forces. Temperature is a statistical measure of kinetic energy over many degrees of freedom, so its instantaneous value fluctuates. Interpret each comparison using its stage, model conditions and sampling interval.

The next lesson starts from these files and connects inputs, logs, trajectories, structures and restarts. You will locate the conditions of a run, choose particle properties to save, and use a complete analysis program to turn records into plots. Getting particles to move then develops into being able to trace, continue and compare a simulation. The same skill applies to a chain, a membrane or a network, because a scientific interpretation must remain connected to the data that support it.

## Further Reading and Open Materials

- [A Set of Tutorials for the LAMMPS Simulation Package — Tutorial 1: Lennard-Jones fluid](https://lammpstutorials.github.io/sphinx/build/html/tutorial1/lennard-jones-fluid.html) · Simon Gravelle; Cecilia M. S. Alvares; Jacob R. Gissinger; Axel Kohlmeyer · CC BY 4.0

  Three-dimensional binary-particle case, minimization and NVE/Langevin workflow, and open inputs.

  New bilingual teaching, analytic diagrams, interaction, staged statistics and restart output; runtime 30Sep2026 update1.
- [LAMMPS stable manual: Lennard-Jones, units, temperature and output normalization](https://docs.lammps.org/stable/pair_lj.html) · LAMMPS developers · Official technical documentation; software source is GPL-2.0, independently drawn figures here

  Equations, mixing conventions, temperature degrees of freedom and command semantics.

  New worked examples and drawings; no manual images reproduced.
- [Fast Parallel Algorithms for Short-Range Molecular Dynamics](https://doi.org/10.1006/jcph.1995.1039) · Steve Plimpton (1995) · Cited scientific paper; no copied figures or article text

  History of spatial decomposition.

  New conceptual diagram of spatial regions and neighbour exchange.
