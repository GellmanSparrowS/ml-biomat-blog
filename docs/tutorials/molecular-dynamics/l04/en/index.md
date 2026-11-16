# Controlling Temperature, Pressure and Boundaries

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l04/en/
Language: en

Use mass-dependent velocity distributions at one temperature to understand how baths, pressure and boundaries enter molecular simulations.

## The environment determines how a material is simulated

A hydrogel in an open dish, a sealed container and a compression fixture encounters different environments even if its chemical composition is unchanged. Heat exchange, allowed volume changes and nearby solid surfaces affect structure and motion. In a simulation, these conditions are not an implicit laboratory background. They must be expressed through temperature control, pressure control and boundaries. After connecting particles, forces and time, this lesson places the box in an environment and distinguishes externally imposed conditions from quantities produced by the system’s response.

The fixed periodic box of two neutral LJ types remains the working example. It demonstrates thermal motion, temperature fluctuations and interaction contributions to pressure without requiring a chemical structure. A Langevin bath at target temperature one acts during the middle interval, with no bath in the first and final intervals. Volume stays fixed throughout. Pressure is therefore a measured response in this run, not a separately prescribed target. The same actual records show that temperature regulation does not prevent pressure from responding to motion and configuration.

In everyday language, constant temperature may suggest a thermometer that never changes. A microscopic system continually exchanges energy and has natural kinetic-energy fluctuations. Thermostatting aims at a statistical state consistent with the target conditions. An air-conditioned room does not require every small portion of air to move at precisely the same speed at every instant. Means, distributions and structural behaviour are therefore relevant, rather than treating a perfectly flat instantaneous-temperature trace as the ideal outcome.

Pressure requires more than a picture of particles striking container walls: a periodic box has no physical walls and still has pressure. Momentum carried by motion and forces transmitted through interactions together determine the response to volume changes. Plotting these contributions separately reveals why attraction can lower total pressure relative to the kinetic contribution alone. This connection between a macroscopic reading and microscopic mechanisms is useful for understanding swelling, liquid density and material loading.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l04/en/#en-s1)

Figure 1 · Conceptual environmental couplings: a thermal bath exchanges heat, and volume changes involve boundary work. The LJ baseline here keeps volume fixed.

By the end, you should be able to explain which velocities define temperature, why heavier particles have a narrower velocity distribution at the same temperature, what Langevin damping controls, and how fixed and variable boxes differ. The code reads the existing trajectory, separates velocity distributions by type, and decomposes pressure into kinetic and virial terms. Surfaces and flow introduce further choices of definition, preparing the same vocabulary for water, chains and networks.

Starting with the scientific question is more effective than starting with a command. Comparing chain conformations at a fixed concentration suggests controlling composition and volume while varying temperature. Obtaining a bulk density at a prescribed pressure requires freedom for volume to adjust. Surface adsorption makes geometry and inhomogeneous density central. Software offers many combinations, each of which should answer a clear question: what can this material exchange with its surroundings, and what is held fixed?

## Temperature describes thermal motion, not one common speed

In a classical particle model, temperature connects thermal motion with kinetic energy across many degrees of freedom. A degree of freedom can first be understood as an independent direction of motion: a translating particle in three dimensions has three velocity components. Adding mass-weighted squared velocities gives kinetic energy, and division by the appropriate degree count defines instantaneous temperature. This is a statistical description of motion rather than a permanent label on each particle. One temporarily slow particle does not constitute a separate thermal environment.

Calculate temperature from the included motionsEq. 1

![Calculate temperature from the included motions](https://ml-biomat.com/static/agent-math/ec004a10442098247716a218.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| K | Total translational kinetic energy included in the temperature calculation | ε₁₁ |
| mᵢ, vᵢ | Mass and velocity vector of particle i | m₁; σ₁₁/τ |
| T | Instantaneous temperature | ε₁₁/k_B |
| k_{B} | Boltzmann constant, numerically one in reduced LJ units | energy/temperature |
| f, N | Included velocity degrees of freedom and particle count | 1 |
| Σ | Sum over all particles included in the calculation | dimensionless operator |
| \|vᵢ\|² | Sum of squared velocity components of particle i | σ₁₁²/τ² |
| =, −, /, × | equality connects expressions for the same quantity; subtraction takes a difference or sets a negative direction; the fraction divides numerator by denominator; adjacent factors multiply. | operators are dimensionless |

Reading the relationshipAt classical equilibrium each quadratic velocity degree of freedom has mean kinetic energy k_BT/2. Reversing the relation defines an instantaneous temperature that fluctuates with motion.

A worked exampleFor N = 1600, f = 4797. With K = 2398.5, T = 1. Here K is a system total; kinetic energy per particle is 1.4990625.

ConditionsThe present model has no internal constraints or imposed mean flow. Its default three-dimensional temperature convention removes three translational degrees of freedom. Rigid bodies, frozen atoms and flow bias require corresponding definitions.

Type one has mass one and type two mass five. At the same temperature, an independent translational direction has the same mean kinetic-energy scale, so greater mass corresponds to a smaller mean squared velocity. Taking the square root makes the width for the heavier type about one over the square root of five times the lighter width. This compares distributions, not every possible pair of particles. The distributions overlap and individual velocities change; the statistical relationship describes how frequently different values occur.

We plot the x component because it can be positive or negative and reveals symmetry around zero. At classical equilibrium without mean flow, one velocity component has a Gaussian shape: highest in the middle and falling smoothly toward both tails. The height times a small interval width approximates the probability of lying in that interval. The vertical axis is therefore a probability density with inverse-velocity units. Integration over an interval produces a dimensionless probability.

Velocity-component distribution in one thermal environmentEq. 2

![Velocity-component distribution in one thermal environment](https://ml-biomat.com/static/agent-math/088377e2d97fa235099337e6.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| p(vₓ) | Probability density of the x velocity component | τ/σ₁₁ |
| vₓ | Signed velocity component in x | σ₁₁/τ |
| m | Mass of the particle type | m₁ |
| T | Equilibrium reference temperature | ε₁₁/k_B |
| k_{B} | Constant relating temperature and energy | energy/temperature |
| s_{v}ₓ | Standard deviation of the distribution | σ₁₁/τ |
| π, exp, √, ² | Pi, exponential function, square root and square | 1 |
| =, −, /, × | equality connects expressions for the same quantity; subtraction takes a difference or sets a negative direction; the fraction divides numerator by denominator; adjacent factors multiply. | operators are dimensionless |

Reading the relationshipKinetic energy grows as m vₓ²/2, and the equilibrium weight decays exponentially with this energy relative to k_BT. The prefactor normalises the probability over all velocities to one.

A worked exampleAt T = k_B = 1, mass one has width one and mass five has width √0.2 ≈ 0.447214. Both have mean x kinetic energy k_BT/2 = 0.5.

ConditionsThis is a classical equilibrium reference for one component without mean flow, with small finite-system corrections possible from total-momentum constraints. It differs from the distribution of nonnegative three-dimensional speed.

The distinction between a component and speed deserves another look. A particle moving left has negative x velocity. A particle moving rapidly along y can still have an x component close to zero. Three-dimensional speed is instead the square root of the sum of all three squared components and is always nonnegative. Combining absolute component values would change the distribution and its normalisation. We deliberately use vx so that sign, mean flow and mass dependence remain visible together. A later calculation that uses speed must construct and label that different quantity explicitly.

A finite degree count also gives a reference scale for temperature fluctuations. In the classical canonical distribution, the relative standard deviation of kinetic temperature decreases with the square root of the number of independent quadratic velocity degrees of freedom. The current count gives about 0.0204, close in scale to the observed window value of 0.0211. Thus fluctuation is not entirely a numerical error. Increasing the particle population generally makes the aggregate temperature appear steadier while individual particles retain thermal motion. The reference is useful alongside, rather than in place of, inspection of velocity and structural behaviour.

Why finite degrees of freedom fluctuate in temperatureEq. 5

![Why finite degrees of freedom fluctuate in temperature](https://ml-biomat.com/static/agent-math/94604f47d2c04ca8636dcf5e.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| T₀ | Target temperature of the classical canonical distribution | ε₁₁/k_B |
| s_{T} | Standard deviation of kinetic temperature in that distribution | ε₁₁/k_B |
| f | Number of independent quadratic velocity degrees of freedom | 1 |
| √ | Square root | 1 |
| =, /, × | equality connects expressions for the same quantity; the fraction divides numerator by denominator; adjacent factors multiply. | operators are dimensionless |

Reading the relationshipEach squared-velocity contribution fluctuates. Combining f independent quadratic degrees of freedom reduces relative kinetic-energy fluctuations as their count grows.

A worked exampleFor f = 4797 and T₀ = 1, the reference standard deviation is √(2/4797) ≈ 0.020419. The actual readings between time fifty and one hundred have a standard deviation near 0.021081, on a similar scale.

ConditionsThis relation concerns quadratic degrees of freedom in a classical canonical distribution. A finite-window standard deviation has sampling variation and is examined alongside velocities and slower structural observables.

A histogram pools records from particles and times. Divide the velocity axis into bins, count observations, then normalise by the record count and bin width to compare with a probability density. Very narrow bins make sampling variation prominent; broad bins hide shape. Both types use common bins and velocity limits so widths are directly comparable. Records from one trajectory can remain correlated, however numerous they are, and the count is not automatically the number of independent experiments.

Temperature also requires separating thermal motion from collective movement. Translating the whole box adds a common velocity without heating its internal motion. Flowing systems often have a position-dependent mean velocity, so thermal motion is measured relative to the appropriate flow field. LAMMPS provides temperature computations that remove centre-of-mass or streaming bias. The velocity definition used for thermostatting must match the question, or the bath can act on the intended flow as though it were unwanted thermal motion.

No macroscopic flow is imposed here, and initialisation removes overall linear momentum, so the basic translational temperature is an appropriate starting definition. Rigid water removes independent degrees of freedom, frozen substrates need different treatment from mobile fluid, and finite-size particles can carry rotational energy. Later models require those motions to be counted afresh. Reusing the temperature relation means checking both its energy numerator and degree-count denominator each time, rather than applying three times the particle number universally.

## Understand a Langevin bath through Brownian motion

The persistent irregular motion of suspended microscopic particles posed a question: if viscous resistance slows motion, why do particles remain agitated? In his 1908 analysis, Langevin separated the fluid’s action into a velocity-dependent resistance and a continually changing additional force. One dissipates existing motion; the other retains the agitation associated with surrounding molecules. This linked the visible particle with fluid molecules not followed individually and provided a starting point for many later stochastic dynamical methods.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l04/en/#en-s3)

Figure 2 · Langevin’s decomposition motivates the bath: drag dissipates motion and random action retains thermal agitation.

In this simulation, explicit LJ interactions provide conservative particle forces, and the Langevin bath adds drag and random forces. The retained particles interact with one another while also contacting an environment not drawn as individual molecules. That environment does not contain the shapes, charges and hydrogen bonds of explicit water. Selected damping and noise rules represent particular exchange effects. Questions about detailed solvent structure require the explicit water and ion models developed later.

Drag and random forcing represent a thermal environmentEq. 3

![Drag and random forcing represent a thermal environment](https://ml-biomat.com/static/agent-math/e095fcbec0db61a4192d2f8a.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| m, v | Particle mass and one velocity component | m₁; σ₁₁/τ |
| dv/dt | Rate of velocity change: acceleration | σ₁₁/τ² |
| F_{c} | Conservative force in the selected direction | ε₁₁/σ₁₁ |
| τ_{d} | Damping time corresponding to damp | τ |
| ξ(t) | Random force whose statistics are paired with temperature and dissipation | ε₁₁/σ₁₁ |
| t | Time | τ |
| =, +, −, /, × | equality connects expressions for the same quantity; addition combines contributions; subtraction takes a difference or sets a negative direction; the fraction divides numerator by denominator; adjacent factors multiply. | operators are dimensionless |

Reading the relationshipConservative force describes explicit interactions, opposing drag dissipates motion, and random forcing supplies thermal fluctuations. Its statistics are linked to damping and temperature to maintain the thermal state.

A worked exampleFor m = 1, v = 0.2 and τ_d = 0.1, drag is −2. At τ_d = 1 it is −0.2. The corresponding random-force statistics change with damping as well; the two contributions are paired.

ConditionsThis describes one component of the continuous model; corresponding components apply in three dimensions. The fix langevin algorithm specifies discrete random forcing. It modifies forces and is paired with an integrator.

When the time step changes, decide whether damping retains its physical meaning. Halving timestep while keeping damp at 0.1 preserves the bath response time and resolves it with more integration steps. Halving damp as well strengthens the coupling. The first change is suitable for isolating integration effects; the second explores a different bath. A simple proportional change in two input values therefore describes a different experiment from changing only one. Expressing the parameters in time units makes that distinction visible before the run, and prevents a numerical-resolution comparison from unintentionally becoming a dynamical-model comparison.

Drag alone dissipates kinetic energy and tends to stop an otherwise undriven system. Random kicks without the corresponding dissipation can continually add kinetic energy. Their strengths must therefore be related through fluctuation and dissipation to maintain a selected thermal state. Random force can average to zero while still increasing mean squared velocity, because both signs contribute positively when squared. Zero mean random force consequently does not mean an absence of thermal agitation.

The damp parameter has time units; it is not itself the friction coefficient. Its value here is 0.1, or twenty integration steps of size 0.005. The drag coefficient contains mass divided by damp, so a smaller damping time produces stronger drag at a given velocity, with a corresponding adjustment of random forcing. This affects velocity memory and dynamics, not only the visual rate of temperature adjustment. Mapping diffusion or viscosity to a real solvent requires additional justification and checking of that damping choice.

A seed records the starting point of a pseudorandom sequence. Changing it changes the random history of an individual trajectory even when temperature, masses and interactions are fixed. Repeated seeds help examine variation between histories. The option zero yes additionally removes the net random force on the group at each step, limiting unintended random driving of the box’s centre of mass. It does not remove each particle’s random force or eliminate thermal motion along any direction.

Two commands cooperate here: fix nve advances positions and velocities, while fix langevin modifies forces. Together they describe bath-coupled motion rather than an isolated NVE ensemble. In contrast, fix nvt already includes its thermostat and integration operations; adding another integrator to the same atoms duplicates updates. Identifying each operation’s responsibility before combining it is more reliable than inferring the physical ensemble solely from the letters appearing in one command name.

## What NVE, NVT and NPT constrain

An ensemble is a statistical description of possible microscopic states under specified macroscopic conditions. It does not require many boxes to be generated simultaneously; a suitable trajectory can sample states, with adequacy assessed separately. N denotes particle number, V volume, E energy, T temperature and P pressure. Their combinations express the connection to the environment and identify which quantities are controlled and which can fluctuate.

NVE fixes particle number and volume without external energy exchange. Temperature follows instantaneous kinetic energy and can change as kinetic and potential energies exchange. For example, velocities assigned to a low-energy initial structure can move it into higher-potential configurations, reducing kinetic energy and temperature. No hidden cooling device is required. Reading temperature together with potential energy in the first interval traces this redistribution instead of treating the initial velocity temperature as a value that must remain fixed.

NVT fixes particle number and volume while coupling to a thermal environment at a specified temperature. The system energy can fluctuate because the bath exchanges energy with it. The middle interval uses Langevin coupling at target temperature one. After kinetic temperature approaches the target, structure can continue changing and the bath can continue supplying or removing energy. Reaching the target temperature therefore does not establish relaxation of clusters, chain conformations or network structure; those slower variables need their own observables.

NPT also allows the box to change size in response to an imposed pressure and is often used to establish bulk density. A movable piston provides an analogy: external pressure and internal response determine volume, while another channel controls temperature. A simulation barostat generally uses additional dynamical variables to adjust the box rather than setting its length from an ideal-gas expression at every step. Interactions, compressibility and response time together influence the volume evolution.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l04/en/#en-s4)

Figure 3 · The letters specify statistical conditions while instantaneous measurements retain their fluctuations.

Allowing volume to change also changes concentration. With a fixed number of solute particles, an expanding box reduces concentration and compression increases it. A pressure-controlled comparison therefore records the resulting mean volume and composition and specifies whether the materials still share a concentration. When the question requires a strictly fixed concentration, fixed volume is often the more direct arrangement, or a preparation stage must establish the desired state. This connects simulation conditions with experimentally controlled quantities and helps identify when two nominally similar comparisons have changed more than one variable.

An excessively short barostat response time can make the box react too strongly to instantaneous fluctuations, while a long response delays density adjustment. This parameter also has time units. A suggestion expressed in numbers of steps cannot be entered unchanged into a script using femtoseconds, picoseconds or reduced time. Establish the units and integration step, convert the intended response scale, then examine actual volume, pressure, energy and structural behaviour. Controller settings are part of the numerical design.

The actual example retains a fixed volume and demonstrates changes between isolated and bath-coupled intervals. NPT is introduced to distinguish a different research condition; melt and network examples will relate density adjustment to their structural preparation. A free-surface slab or fixed substrate can occupy a box containing vacuum or immobile regions. Applying a bulk isotropic barostat changes that geometry. Environmental controls therefore have to be chosen together with the structure being studied.

One material does not have a single universally correct ensemble. Preparing a bulk state at selected temperature and pressure, then observing fixed-volume motion, is one purposeful sequence. Stress relaxation at fixed strain is another. Each switch should identify the inherited state, changed environmental condition and measurement interval. The restart and staged-recording methods developed earlier keep such transitions consistent across files and physical interpretation.

## Pressure in a periodic box without walls

Pressure is force per area. A piston gives an accessible picture: greater average force transmitted to the same area means greater pressure. A periodic system has no physical piston, but microscopic momentum transport and interactions still define its pressure. Imagine a small uniform change of box volume; the response of the internal state connects to pressure. The fixed box need not actually undergo that change for pressure to be measured. The construction explains the quantity being evaluated.

For this unbonded pair-interaction system, pressure separates into kinetic and virial contributions. The kinetic term comes from momentum carried by motion and involves kinetic energy divided by volume. The virial multiplies each pair separation by the radial force and sums over distinct interacting pairs. This product has energy units; division by volume gives pressure. Division by three averages the diagonal directional contributions in three dimensions. Stretching and shear later require retaining the individual tensor components.

Kinetic and virial contributions to pressureEq. 4

![Kinetic and virial contributions to pressure](https://ml-biomat.com/static/agent-math/ed5131661fd03a90d6868d43.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| P, P_{kin}, P_{vir} | Scalar pressure and its kinetic and virial terms | ε₁₁/σ₁₁³ |
| K | Total translational kinetic energy | ε₁₁ |
| V | Three-dimensional box volume | σ₁₁³ |
| rᵢⱼ | Pair separation using the relevant periodic image | σ₁₁ |
| Fᵣ,ᵢⱼ | Pair radial force, positive toward increasing separation | ε₁₁/σ₁₁ |
| Σᵢ<ⱼ | Sum once over distinct particle pairs | 1 |
| 3 | Average over three diagonal directions | 1 |
| =, +, /, × | equality connects expressions for the same quantity; addition combines contributions; the fraction divides numerator by denominator; adjacent factors multiply. | operators are dimensionless |

Reading the relationshipMomentum transport contributes the kinetic term; separation times force contributes the interaction term. Both numerators have energy units, giving pressure after division by volume.

A worked exampleFor K = 2398.5 and V = 64000, kinetic pressure is about 0.0249844. If an illustrative state has pair-virial sum −960, its virial pressure is −0.005 and total pressure about 0.0199844.

ConditionsThis form applies to the present unbonded three-dimensional pair system for scalar pressure. Constraints, long-range terms and other interactions add contributions; inhomogeneous or loaded systems also require tensor and volume definitions.

For a noninteracting ideal gas the kinetic contribution supplies the full pressure, leading to the familiar relation among pressure, number, temperature and volume. The present model contains attraction and repulsion and has a nonzero virial, so number density times temperature does not replace its measured pressure. Its temperature also uses a convention subtracting three overall degrees of freedom. Computing kinetic pressure directly from total kinetic energy avoids overlooking that count in a finite system. Matching units is necessary, and matching the objects and degree conventions described by the expressions is equally important.

Repulsion acts toward increasing separation and contributes a positive separation-force product; attraction contributes negatively. A population can therefore have positive kinetic pressure partly offset by a negative virial. The latter part of the actual bath interval illustrates this: mean kinetic pressure is about 0.02497, mean virial pressure about −0.00487, and total pressure about 0.02010. Their sum connects the reported pressure with both motion and interactions during that observation window.

Instantaneous pressure often fluctuates more than a beginner expects because it combines many interactions in their current arrangement. A brief close encounter can noticeably affect the virial at one instant. Time averaging helps identify a slower central tendency, while the interval, correlation and units remain relevant. Forcing every recorded pressure to equal a target changes natural fluctuations and can perturb structure. A barostat should be consistent with the ensemble and material response rather than merely producing tidy screen values.

A scalar pressure also hides directional information. In an isotropic equilibrium fluid, adequately averaged normal components reflect the corresponding symmetry. A stretched network, a confined fluid and a sheared system can instead have different normal and tangential responses. One average then discards important structure. Later stress analyses identify the component, sign convention and normalising volume explicitly, so increasing scalar pressure is distinguished from increasing tensile stress in a selected direction.

The displayed virial is obtained from the actual total pressure minus its kinetic contribution, appropriate to the present pair model without internal rigid constraints. Constrained water and long-range electrostatics introduce further virial terms; fixed substrates, walls and fields require their relevant definitions. The decomposition remains useful while the physical terms change. A productive question for each new model is therefore which forces are actually included in its reported pressure.

## Periodic space, free surfaces and walls describe different geometries

Periodic boundaries tile space with copies of the finite box, letting a crossing particle continue into an adjacent image. They suit approximately homogeneous bulk systems but make the model neighbour its own replicas. Large aggregates, long chains or correlations approaching the box length can be affected. Periodicity specifies a surrounding environment; sufficient size remains a separate question examined through box-size comparisons. An image without visible walls still carries geometrical assumptions.

A nonperiodic direction is not repeated. The f boundary option in LAMMPS keeps the box face fixed, but does not itself create a reflecting wall force. A particle crossing it can be removed during an update and trigger a lost-particle problem. Confinement requires an actual wall potential or interactions with explicit substrate atoms. Distinguishing boundary bookkeeping from wall interactions prevents a single boundary letter from being mistaken for a complete physical container.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l04/en/#en-s6)

Figure 4 · Periodic extension, a free surface and explicit walls create different neighbourhoods.

A free surface is another object. A liquid slab adjacent to vacuum lacks neighbours in some directions near its surface, so local density and orientation can differ from the interior. Dividing quantities by the full box volume can change their normalised values when vacuum thickness changes even if the liquid layer is nearly unchanged. Local density, surface tension and membrane lateral pressure therefore need explicit regions and geometrical definitions. Those definitions connect observables to the actual interfacial question.

Walls can produce density layering because attraction and repulsion make the normal distribution nonuniform. Moving walls additionally transfer momentum and energy to the fluid. Thermostat action, subtraction of streaming velocity and the relevant pressure direction must then be coordinated with wall motion. Confined water and ion systems and later flow examples develop these effects in actual models. Establishing the geometry first helps keep local interfacial behaviour distinct from homogeneous bulk properties.

Shrink-wrapped boundaries are also sometimes mistaken for a piston compressing material. Their principal role is to adjust the enclosing box to the particle extent, which is spatial bookkeeping. They are not a pressure controller applying a specified external load. Compression must be identified through actual forces and loading conditions rather than merely changing box bounds. Similar everyday words can describe different physical operations, so the role of the command remains the starting point.

For biomaterials, geometry usually follows the sample: a chain in solution needs adequate solvent space, a bulk melt suits periodic representation, membranes and interfaces retain directional differences, and adsorption requires an explicit surface. The ability to handle many geometries does not make a cubic periodic box the right representation for every object. Later examples change these conditions individually so that each added geometrical feature serves a specific research question.

## Read the three intervals through actual velocities and pressure

The complete input retains the model used earlier. Here the focus is bath insertion and removal and the velocity and thermodynamic fields retained for analysis. The intervals contain 5000, 15000 and 10000 steps, corresponding to times zero to 25, 25 to 100 and 100 to 150. The bath target operates only in the middle interval. Accordingly, the target line in the figure is drawn only there, matching the environmental conditions actually applied.

### Complete fixed-volume input with bath insertion and removal

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

The same executed input is used throughout the introductory lessons. The bath acts only from 25 to 100τ and no barostat is applied.

The analysis reads temperature, per-particle kinetic energy and total pressure from thermo.dat, then computes kinetic pressure using particle count and box volume. It also reads trajectory frames and collects x velocities separately for each type during the interval from fifty to one hundred. Fifty frames provide 75000 type-one and 5000 type-two readings. Probability-density normalisation allows the shapes to be compared without making the more numerous type appear taller simply because it contributes more observations.

### Complete velocity-distribution and pressure-decomposition analysis

```
"""Read actual LJ temperature, pressure and type-resolved velocities.
python analyze_ensemble.py --data-dir . --language en
Requires NumPy and Matplotlib.
"""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def velocities_in_window(filename, start=50.0, end=100.0):
    selected={1:[],2:[]}
    frames=0
    with Path(filename).open(encoding='utf-8') as f:
        while True:
            line=f.readline()
            if line=='':break
            if line.strip()!='ITEM: TIMESTEP':raise ValueError('Expected frame header.')
            time=int(f.readline())*.005
            if f.readline().strip()!='ITEM: NUMBER OF ATOMS':raise ValueError('Missing count.')
            count=int(f.readline())
            if not f.readline().startswith('ITEM: BOX BOUNDS'):raise ValueError('Missing box.')
            for _ in range(3):f.readline()
            fields=f.readline().split()
            if fields[:2]!=['ITEM:','ATOMS']:raise ValueError('Missing particle fields.')
            names=fields[2:]
            ti,vi=names.index('type'),names.index('vx')
            use=start<=time<end
            for _ in range(count):
                row=f.readline().split()
                if len(row)!=len(names):raise ValueError('Truncated trajectory.')
                if use:
                    kind=int(row[ti])
                    if kind not in selected:raise ValueError('Unexpected particle type.')
                    selected[kind].append(float(row[vi]))
            if use:frames+=1
    if frames==0:raise ValueError('No frames in selected window.')
    return {k:np.asarray(v) for k,v in selected.items()},frames


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir',type=Path,default=Path('.'))
    parser.add_argument('--out-dir',type=Path,default=Path('ensemble-analysis'))
    parser.add_argument('--language',choices=['zh','en'],default='en')
    args=parser.parse_args()
    a=np.loadtxt(args.data_dir/'thermo.dat',comments='#',ndmin=2)
    if a.shape[1]!=8 or not np.all(np.isfinite(a)):raise ValueError('Expected eight finite columns.')
    time,T,ke,P=a[:,1],a[:,2],a[:,4],a[:,6]
    velocity,frames=velocities_in_window(args.data_dir/'trajectory.lammpstrj')
    N,V=1600,40**3
    kinetic_pressure=2*ke*N/(3*V)
    virial_pressure=P-kinetic_pressure
    summary={'velocity_window_reduced_time':[50,100],'saved_frames':frames,
             'velocity_reference_temperature_reduced':1.0,'particle_types':{},'stages':{}}
    for kind,mass in [(1,1.0),(2,5.0)]:
        v=velocity[kind]
        summary['particle_types'][str(kind)]={'mass_reduced':mass,'pooled_vx_records':len(v),
            'mean_vx':float(v.mean()),'vx_standard_deviation':float(v.std(ddof=0)),
            'equilibrium_reference_sigma_vx':float(np.sqrt(1/mass))}
    for name,left,right in [('initial_NVE_late',10,25),('bath_late',50,100),('final_NVE_late',120,150.000001)]:
        mask=(time>=left)&(time<right)
        summary['stages'][name]={'start':left,'end':min(right,150),'records':int(mask.sum()),
            'mean_T':float(T[mask].mean()),'std_T_readings':float(T[mask].std(ddof=1)),
            'mean_P':float(P[mask].mean()),'std_P_readings':float(P[mask].std(ddof=1)),
            'mean_kinetic_pressure':float(kinetic_pressure[mask].mean()),
            'mean_virial_pressure':float(virial_pressure[mask].mean())}
    zh=args.language=='zh'
    plt.rcParams.update({'font.family':['Microsoft YaHei','Noto Sans CJK SC','Source Han Sans SC','WenQuanYi Zen Hei','DejaVu Sans'] if zh else ['DejaVu Sans'],
        'font.size':14,'svg.fonttype':'path','axes.spines.top':False,'axes.spines.right':False,
        'axes.labelcolor':'#173c42','text.color':'#173c42'})
    fig,axes=plt.subplots(2,1,figsize=(11.5,8),sharex=True,layout='constrained')
    fig.set_facecolor('#faf9f5')
    for ax in axes:
        ax.set_facecolor('#faf9f5');ax.axvspan(25,100,color='#e4eeeb');ax.grid(axis='y',alpha=.17);ax.set_xlim(0,150)
    axes[0].plot(time,T,color='#167d84',lw=1.2)
    axes[0].hlines(1,25,100,color='#b57448',linestyle='--',lw=1.2)
    axes[0].set_ylabel(('温度 ' if zh else 'Temperature ')+r'$k_BT/\epsilon_{11}$')
    for values,name,color in [(P,'总压力' if zh else 'Total','#173c42'),
        (kinetic_pressure,'动能项' if zh else 'Kinetic','#b57448'),
        (virial_pressure,'位力项' if zh else 'Virial','#4974ac')]:
        axes[1].plot(time,values,label=name,color=color,lw=1.2)
    axes[1].set_ylabel(('压力 / ' if zh else 'Pressure / ')+r'$(\epsilon_{11}/\sigma_{11}^3)$')
    axes[1].set_xlabel(('约化时间 ' if zh else 'Reduced time ')+r'$t/\tau$')
    axes[1].legend(frameon=False,ncol=3)
    fig.suptitle('热浴改变温度；固定盒中压力由状态产生' if zh else 'The bath controls temperature; fixed-volume pressure follows the state',fontsize=16)
    args.out_dir.mkdir(parents=True,exist_ok=True)
    for ext in ['png','svg']:fig.savefig(args.out_dir/f'thermodynamic-stages-{args.language}.{ext}',dpi=200)
    plt.close(fig)
    fig,ax=plt.subplots(figsize=(11.5,6.5),layout='constrained')
    fig.set_facecolor('#faf9f5');ax.set_facecolor('#faf9f5')
    limit=max(4.0,float(np.ceil(max(np.abs(v).max() for v in velocity.values())*2)/2))
    bins=np.linspace(-limit,limit,71);x=np.linspace(-limit,limit,701)
    for kind,mass,color in [(1,1.0,'#167d84'),(2,5.0,'#b57448')]:
        ax.hist(velocity[kind],bins=bins,density=True,histtype='step',linewidth=1.8,color=color,
                label=(f'类型 {kind} 实际记录' if zh else f'Type {kind}: actual records'))
        pdf=np.sqrt(mass/(2*np.pi))*np.exp(-mass*x*x/2)
        ax.plot(x,pdf,color=color,linestyle='--',lw=1.5,
                label=(f'm = {mass:g}，T = 1 参考' if zh else f'm = {mass:g}, T = 1 reference'))
    ax.set_xlabel(('速度分量 ' if zh else 'Velocity component ')+r'$v_x/(\sigma_{11}/\tau)$')
    ax.set_ylabel(('概率密度 / ' if zh else 'Probability density / ')+r'$(\tau/\sigma_{11})$')
    ax.set_title('同一热浴，两种质量的速度宽度' if zh else 'One bath, two mass-dependent velocity widths',loc='left',fontsize=17)
    ax.legend(frameon=False,ncol=1,fontsize=12,loc='upper right');ax.grid(axis='y',alpha=.17)
    for ext in ['png','svg']:fig.savefig(args.out_dir/f'velocity-distributions-{args.language}.{ext}',dpi=200)
    plt.close(fig)
    (args.out_dir/'ensemble-summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
```

Uses the actual numerical table and trajectory, groups velocities by type, and obtains the present model’s virial pressure by subtracting the kinetic contribution from total pressure.

### Reproduce all figures in both languages

```
python analyze_ensemble.py --data-dir . --out-dir ensemble-analysis --language zh
python analyze_ensemble.py --data-dir . --out-dir ensemble-analysis --language en
```

Place the program with thermo.dat and trajectory.lammpstrj in the example directory. NumPy and Matplotlib are required.

The measured standard deviations of x velocity are about 0.9991 and 0.4444. At temperature one, the corresponding Gaussian reference widths are one and 0.4472. Overlaying histograms and references shows the mass dependence of thermal velocity. The smooth reference is calculated from mass and temperature; the stepped curve is measured from the trajectory. Finite particle number, overall-momentum treatment and sampling fluctuations affect finer differences, which should be interpreted within those definitions.

### Measured velocity widths of the two types

Fifty frames at 50≤t<100 contain 75000 type-one and 5000 type-two vx records. Steps show the trajectory histograms; dashed lines are Gaussian references at T = 1.

LAMMPS 30 Sep 2026 update 1; a three-dimensional periodic box with 1,500 type-1 and 100 type-2 particles. Reduced units, time step 0.005 and total duration 150. Physical inputs follow the binary Lennard–Jones tutorial by Gravelle and colleagues, with added NVE comparisons and numerical output.

[Download reference data and complete inputs (ZIP) 6.73 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-lj-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l04/en/#en-s7)

Histograms of x velocity by particle type across 50 saved frames with 50≤t*<100: 75,000 type-1 and 5,000 type-2 records. Dashed curves are Gaussian references at T*=1; velocity width depends on mass.

In the later bath window, 50≤t<100, mean temperature is about 0.9996 and the sample standard deviation of instantaneous readings about 0.0211. That number describes fluctuations within the window, not uncertainty in the mean. After bath removal, kinetic and potential energies continue exchanging, and the final temperature is no longer maintained by the same bath-coupled distribution around one. Interpreting each trace within its energy-exchange conditions explains why removing the bath changes the expected behaviour.

### How motion and interactions contribute to pressure

Actual temperature and pressure; kinetic pressure is 2K/(3V), and virial pressure is total minus kinetic pressure for the fixed box and particle count.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l04/en/#en-s7)

Actual temperature and pressure records. The kinetic pressure contribution is calculated from whole-box kinetic energy and volume; the virial contribution is total pressure minus the kinetic term. Their signed contributions determine total pressure.

The pressure plot exposes another relationship. At fixed particle count and volume, temperature changes the kinetic contribution while configuration and interactions change the virial. The three stages can therefore have different mean pressures even though number density remains 0.025. The program preserves window definitions, record counts and component means so the comparison can be recalculated. Moving or shortening the window reveals the influence of slow change and sampling range, preparing the later treatment of systematic statistical design.

## Make environmental conditions an interpretable research choice

For a polymer in solution, first decide which solvent effects the question requires. Explicit water structure around a chain needs molecular geometry, charges and interactions. Longer-scale chain motion may instead use effective interactions and damping to retain selected solvent effects. The observable structures and dynamical time mappings differ. A Langevin bath is a defined modelling tool whose exchange effects should match the question, rather than being labelled a water environment without specifying what is represented.

For diffusion, viscosity or relaxation times, bath parameters enter the factors requiring examination. Models with different damping can have similar equilibrium conformational distributions while moving between conformations at different rates. Equilibrium and dynamical validation should therefore be organised separately. Temperature and structural distributions can be checked first, followed by displacement or stress correlations under defined dynamics. Changing damping is then recorded as a model change, allowing the bath to support sampling while retaining a clear account of motion.

For stretching or shear, organised velocity fields and applied work enter the interpretation of temperature, energy and stress. The flow component removed from thermal motion, the directions or subspaces thermostatted, and the way boundaries transmit loading must match the problem. A tightly controlled temperature can coexist with excessive damping of the intended flow. Mechanical examples will therefore explain loading, thermostatting and measurement together rather than treating the thermostat as an inconsequential background setting.

The interaction provides a direct check: at fixed temperature, why does increasing mass from one to five narrow the velocity distribution without reducing the corresponding mean kinetic-energy scale? What happens when temperature is increased instead? Watching the distributions and returning to mass times squared velocity connects the changes. This reasoning identifies what is held fixed and explains how groups of different masses can share one thermal environment, beyond simply remembering that heavier objects move more slowly and hotter ones faster.

Explore a Gaussian statistical reference for one velocity component: mass and temperature determine its analytic distribution.

[Figure: Gaussian velocity probability density](https://ml-biomat.com/tutorials/molecular-dynamics/l04/en/#en-s8)

The horizontal axis is a signed velocity component, not nonnegative speed. Mass and temperature separately change its width.

Molecules and chains introduce additional motions and constraints: bonds stretch, angles bend, rigid geometry removes degrees of freedom, and walls create spatial inhomogeneity. The underlying questions about temperature, pressure and boundaries remain, while the participating objects become richer. The next lesson represents a molecule in the computer, connecting particle identities into explicit topology. The environmental and statistical language developed here will explain how those connections change the questions the model can address.

## Further Reading and Open Materials

- [LAMMPS Tutorial 1: Lennard-Jones fluid](https://lammpstutorials.github.io/sphinx/build/html/tutorial1/lennard-jones-fluid.html) · Simon Gravelle; Cecilia M. S. Alvares; Jacob R. Gissinger; Axel Kohlmeyer · CC BY 4.0

  Binary LJ particles, NVE and Langevin workflow, and periodic geometry.

  Added environmental interpretation and complete actual-data velocity and pressure analyses.
- [LAMMPS stable manual: fix langevin](https://docs.lammps.org/stable/fix_langevin.html) · LAMMPS developers · Official documentation consulted; software source GPL-2.0; original figures here

  Damping, random forces, integration responsibilities and zero yes.

  New explanation connecting parameters with the actual model.
- [LAMMPS stable manual: compute pressure](https://docs.lammps.org/stable/compute_pressure.html) · LAMMPS developers · Official documentation consulted; no copied images

  Kinetic and virial pressure, degrees of freedom and tensor definition.

  Worked pair-model example and actual data decomposition.
- [Paul Langevin’s 1908 paper: On the Theory of Brownian Motion](https://www.physik.uni-augsburg.de/theo1/hanggi/History/Langevin1908.pdf) · Paul Langevin; translation by Anthony Gythiel, introduction by Don S. Lemons (1997) · Primary historical text in published translation; cited, no text or figures reproduced

  Historical decomposition into resistance and irregular molecular impacts.

  Original mechanism drawing, with no article figure reused.
