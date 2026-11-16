# Connecting Force, Energy and Time

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l03/en/
Language: en

Follow an energy slope through one full time step, then use a common-state comparison to distinguish integration error, cutoff effects and sampling.

## Smooth animation and accurate motion

A phone video of a rapidly vibrating string can show slow motion or an apparent shape that differs from the actual vibration. The observation interval matters. Molecular simulation adds another interval: the computer itself advances motion in discrete time steps. If one step spans much of a strong encounter, the particles may reach very different positions before the next force calculation. This lesson connects potential energy, force and time integration, then uses actual comparisons to examine the suitability of a time step for the selected model.

Two related questions must be separated. Is the interaction model appropriate for the object, for example which attractions and repulsions neutral LJ particles retain? And how accurately does the computer advance the equations of that selected model? Changing the force field addresses the first question; reducing the integration step mainly addresses the second. Water, chains and crosslinked materials require both kinds of examination. Understanding the distinction in a simple system helps prevent numerical instability from being interpreted as a physical transformation.

Three NVE runs start from the same saved state without a stochastic bath and with a fixed box. Their time steps are 0.0025, 0.005 and 0.01, and each advances twenty reduced time units. Particle populations, initial coordinates and velocities, the potential and cutoff convention are retained. The comparison focuses on energy and temperature as the time step changes. Equal elapsed time matters: using the same step count would let the larger-step run evolve longer and introduce another difference into the comparison.

To interpret the curves, we first unpack the statement that force comes from an energy slope, then follow a particle through a velocity-Verlet update. Mathematics enters where it serves a concrete purpose. A slope describes energy change per change in position; a square root connects vibration time with mass and stiffness; a maximum extracts the largest recorded departure from an energy trace. Each symbol refers to an interpretable quantity. Complete inputs and analysis then connect these relationships to actual simulation records.

Accuracy also depends on the target observable. A brief collision can be examined through forces and path details; equilibrium structure through separation distributions and energy statistics; rheology through stresses and long-time correlations. An overly large step can affect several quantities, while a fairly steady energy trace answers only part of the accuracy question. Energy is the first observable studied here because, in this interval without a bath or applied work, it has a direct relation to the equations being integrated.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l03/en/#en-s1)

Figure 1 · Maintain correspondence from model definition through data interpretation.

The original unshifted truncated LJ potential is retained. That makes the comparison informative: observed energy changes can contain both integration error and energy jumps when pairs cross the cutoff. Rather than predicting in advance which contribution dominates, we examine the definitions and comparisons. Bringing the actual input details into the interpretation turns “try a smaller time step” into a numerical experiment with a defined object, reference and decision criterion.

## Read force from an energy slope

Imagine a ball on a smooth hillside. The push along the slope depends on local steepness, not simply altitude. Two points at the same height can have different slopes, and zero altitude can lie on a steep incline. The same distinction applies to potential energy and force. With particle separation on the horizontal axis, an increase in separation that raises energy corresponds to an attractive tendency toward smaller separation. If increasing separation lowers energy, the tendency is to separate.

Begin with two nearby points. Divide their energy difference by their separation difference to obtain an average slope; bringing the points closer defines the local slope, called a derivative. Force is its negative, expressing a tendency down the energy landscape. We define positive radial force as increasing separation and negative radial force as decreasing separation. Stating that direction first prevents a negative energy value from being confused with a force acting in a particular spatial direction.

Force and the local energy slopeEq. 1

![Force and the local energy slope](https://ml-biomat.com/static/agent-math/f09df8fc30a513a541af562c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Fᵣ | Radial force, positive toward increasing separation | ε₁₁/σ₁₁ |
| U | Pair potential energy | ε₁₁ |
| r | Particle separation | σ₁₁ |
| h | Small distance increment for estimating the slope | σ₁₁ |
| dU/dr | Local rate of energy change with distance: a derivative | ε₁₁/σ₁₁ |
| ≈, − | Approximate equality; minus sign gives the downhill tendency | 1 |
| =, +, −, /, × | equality connects expressions for the same quantity; addition combines contributions; subtraction takes a difference or sets a negative direction; the fraction divides numerator by denominator; adjacent factors multiply. | operators are dimensionless |

Reading the relationshipThe energy difference between points separated by 2h estimates the local slope. Its negative gives a force directed toward lower energy.

A worked exampleIf points separated by 0.02 have energies −0.50 and −0.48, the estimated slope is 0.02/0.02 = 1. The radial force is approximately −1, tending to reduce the separation.

ConditionsThis describes conservative force in a smooth interval. A finite difference spanning the unshifted energy jump is not the definition of the truncated force used by LAMMPS.

Differentiating the LJ potential gives a related force curve with a different shape. Repulsion grows rapidly at short distances; at the energy minimum the two contributions balance and radial force vanishes; farther away the force is attractive and weakens with separation. At r = σ the potential is zero while the force is still positive. For type-1 reduced parameters its value there is twenty-four. Distinguishing energy from its rate of change resolves much of the confusion surrounding equilibrium separation.

Estimating a slope numerically introduces another resolution choice. A large increment measures an average across a curved region rather than the local slope. An extremely small increment subtracts nearly equal energies and can lose significant digits. The actual LJ force uses an analytic expression; the two-point estimate explains the derivative and can independently check a custom potential. Varying the increment across a sensible range reveals whether the estimate is stable. This is another example of distinguishing the mathematical quantity from the finite numerical operation used to approximate it.

Lennard–Jones radial forceEq. 2

![Lennard–Jones radial force](https://ml-biomat.com/static/agent-math/4cf7a53bed184bd96196cbe0.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Fᵣ | Radial force: positive repulsion and negative attraction | ε₁₁/σ₁₁ |
| ε | Well depth | ε₁₁ |
| σ | Potential zero-crossing length scale | σ₁₁ |
| r, r_{c} | Separation and pair cutoff distance | σ₁₁ |
| 12, 6 | Powers of the dimensionless ratio | 1 |
| =, −, /, × | equality connects expressions for the same quantity; subtraction takes a difference or sets a negative direction; the fraction divides numerator by denominator; adjacent factors multiply. | operators are dimensionless |

Reading the relationshipDifferentiate the two distance-dependent terms of the 12/6 potential and negate the result. The bracket is dimensionless and ε/r supplies force units.

A worked exampleFor ε = σ = 1 and r = 1, Fᵣ = 24. At r = 2^(1/6), the bracket becomes 2 × 1/4 − 1/2 = 0. At r = 1.5, Fᵣ ≈ −1.15803.

ConditionsThis is the ordinary LJ force inside the cutoff; outside it the force is zero. Multiplication by the unit direction along the pair gives the corresponding vector force.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l03/en/#en-s2)

Figure 2 · Zero energy and zero force occur at different separations. These values are calculated analytically.

In three dimensions the radial force is distributed along the line connecting the pair. Using a unit direction from particle one to particle two, positive radial force pushes particle two outward and particle one experiences the opposite force. The unit vector supplies direction; multiplying it by radial force supplies magnitude. Each particle has many neighbours, so the program sums force components separately. Equal and opposite contributions can cancel. Zero net force can therefore describe several balanced interactions rather than an absence of interactions.

The relationship also explains why shifting a smooth potential by a constant does not change its local force. Raising the entire curve leaves its slope unchanged. Truncated interactions require an additional check of which pairs are included and whether the function joins continuously at the cutoff, discussed below. For now the chain of meaning is clear: potential energy describes the energetic cost of an arrangement, its derivative describes sensitivity to displacement, and force acts through mass to change velocity.

Bonds, angles and dihedrals use the same idea, though their energies depend on more than one pair separation. Stretching a bond, changing an angle formed by three particles, or rotating a torsion defined by four particles changes energy. The software obtains forces from those coordinate dependencies. The molecule lesson introduces these connections. Starting here with a pair potential makes the sequence—define energy, determine how it changes, obtain force—visible within one simple diagram.

## Connect position and velocity over one step

Given position and velocity, the simplest idea is to estimate displacement as velocity times time and update velocity from the force. This explains the task of integration, but a crude update can accumulate substantial error. Velocity Verlet uses a more symmetric arrangement: update velocity by half a step using the old force, advance position by a full step with that half-step velocity, evaluate force at the new position, and complete the velocity update with the new force. Both ends of the step contribute.

The half-step velocity is an intermediate quantity used by the algorithm; it does not require a separate physical trajectory to be generated. Its purpose is to provide a suitable velocity estimate for the position update. At the end, the new position and final velocity refer to the same full time. LAMMPS fix nve uses this velocity form of Verlet integration. Additional thermostat operations can modify forces or velocities, so the complete settings determine which dynamics is actually being advanced.

One full velocity-Verlet updateEq. 3

![One full velocity-Verlet update](https://ml-biomat.com/static/agent-math/e48170fbae5cd8d47b96eb9e.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| rₙ, rₙ₊₁ | Particle positions at the current and next full step | σ₁₁ |
| vₙ, vₙ₊₁ | Velocities at the two full-step times | σ₁₁/τ |
| vₙ₊₁/₂ | Intermediate half-step velocity used to update position | σ₁₁/τ |
| Fₙ, Fₙ₊₁ | Net force evaluated at old and new positions | ε₁₁/σ₁₁ |
| m | Particle mass | m₁ |
| Δt | Fixed integration step | τ |
| n, n+1, n+1/2 | Current step, next full step and intermediate update labels | 1 |
| =, +, /, × | equality connects expressions for the same quantity; addition combines contributions; the fraction divides numerator by denominator; adjacent factors multiply. | operators are dimensionless |

Reading the relationshipAdvance velocity by half a step with the old force, advance position, evaluate the new force, and complete the velocity update. Both endpoint forces enter symmetrically.

A worked exampleFor a one-dimensional spring with m = 1 and F = −x, start at x = 1, v = 0 and Δt = 0.1. The half-step velocity is −0.05, the new x is 0.995, the new force is −0.995, and the final velocity is −0.09975.

ConditionsThis is the basic update for fixed mass and position-dependent forces. Rigid constraints, stochastic baths and pressure control require their full algorithmic treatment.

Follow one update for a one-dimensional spring with mass one, stiffness one, initial position one, zero initial velocity and step 0.1. The spring pulls toward the origin. Initial acceleration is −1, giving a half-step velocity of −0.05. The new position is 0.995, so the new acceleration is −0.995. Completing the update gives velocity −0.09975. Each number uses information already available. The example shows why force must be recalculated at the new position rather than retaining the initial force indefinitely.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l03/en/#en-s3)

Figure 3 · Historical classical-fluid calculations required repeated dynamical updates; the diagram develops one update in the modern velocity form.

Units provide a useful check on the update. Acceleration times time is velocity and can be added to velocity; velocity times time is length and can be added to position. Adding force directly to a coordinate combines incompatible dimensions. The computer performs numerical operations and does not interpret the physical rationale for a user’s unit choices. Dimensional checks are particularly helpful when defining custom forces. They do not detect every modelling error, but immediately identify some incompatible additions and products.

Verlet’s 1967 classical-fluid study used 864 LJ particles to investigate equilibrium properties at different temperatures and densities. It exemplified the organisation of repeated force evaluation and time advancement into computational experiments. The widely used velocity form and the classical position recurrence belong to the same time-symmetric family, while expressing and storing velocity differently. Following the old force, half-step velocity, new position and new force turns an abstract time update into an explicit sequence of calculations.

The symmetric update gives this family useful long-time numerical properties in conservative systems, while a finite-step trajectory remains approximate. With a sufficiently smooth potential and a stable step, energy error often oscillates within bounds rather than simply growing in one direction. Actual drift and excursion still depend on the model, cutoff and numerical record. We therefore inspect the complete trace alongside several measures. A small final energy difference can occur even when substantially larger departures happened earlier.

## How fast motion constrains the time step

A material often contains processes on very different time scales. A whole polymer may rearrange slowly while local bonds vibrate rapidly; water rotation and solute diffusion also occur on different scales. Explicit integration must resolve the fast motion retained by the model, not merely the slow process of interest. Increasing the time step to watch slow chain diffusion does not slow bond vibrations. Constraints or coarse graining can remove selected fast degrees of freedom, after which the modified model requires its own time-scale assessment.

Spring motion provides an accessible starting point. A heavier mass responds more slowly to the same spring, while a stiffer spring pulls the same mass back more rapidly. Their ratio determines the oscillation period, the time for a complete cycle. If a step occupies a substantial fraction of that period, the algorithm can skip changes in direction between force evaluations. Dividing the cycle into sufficiently small steps allows the changing force and motion to be followed more accurately.

Spring time scale and linear stability intervalEq. 4

![Spring time scale and linear stability interval](https://ml-biomat.com/static/agent-math/72270c1b9cec6da61bd257f6.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| F, x | Restoring force and displacement from equilibrium | ε₁₁/σ₁₁; σ₁₁ |
| k | Spring stiffness: force per displacement | ε₁₁/σ₁₁² |
| m | Mass of the moving object | m₁ |
| ω | Angular frequency: phase accumulated per time | τ⁻¹ |
| P | Period of one full oscillation | τ |
| Δt | Integration step | τ |
| π, √, < | Pi, square root and less-than relation | 1 |
| =, −, /, × | equality connects expressions for the same quantity; subtraction takes a difference or sets a negative direction; the fraction divides numerator by denominator; adjacent factors multiply. | operators are dimensionless |

Reading the relationshipIncreasing mass slows the response and increasing stiffness speeds restoration. The harmonic equation gives frequency and period; linear stability of the discrete update requires ωΔt below 2.

A worked exampleFor m = k = 1, ω = 1 and P ≈ 6.283. A step of 0.1 gives about 62.8 steps per period and ωΔt = 0.1. A step of 2.1 is outside the stability interval. Within it, phase and energy accuracy still require examination.

ConditionsThe condition applies specifically to an undamped linear harmonic oscillator integrated with velocity Verlet. Many-body LJ encounters, constraints and baths have their own time-scale requirements.

For a harmonic oscillator, velocity Verlet also has an analytically derived linear stability limit. Beyond that limit, discrete motion develops a growing amplitude even though the true undamped oscillator has a fixed amplitude. Stability prevents that form of growth; accurate phase and energy generally require a smaller step. The interaction below separates these ideas using a labelled spring exercise. It illustrates the algorithm, while the LJ results later on the page come from actual LAMMPS runs.

A numerical spring demonstration: m = k = 1, initial x = 1 and v = 0. It is separate from the LAMMPS data.

[Figure: Spring displacement versus time](https://ml-biomat.com/tutorials/molecular-dynamics/l03/en/#en-s4)

Only the step changes. Analytic and numerical spring solutions share initial position and velocity. This is an algorithm demonstration; actual LJ comparisons appear below.

An LJ encounter has no single spring stiffness valid at all separations. Near the minimum the curve can be approximated locally by a spring, but closer approaches encounter sharply increasing repulsion and faster force changes. Near overlaps in a random initial configuration can therefore be more demanding than small equilibrium vibrations. Appropriate minimisation improves the starting geometry and reduces extreme initial encounters. The subsequent dynamics still needs examination at the selected time step and parameter conditions.

Mass also affects rapid motion. The two types differ in both interaction parameters and mass, so the statement that type two is heavier does not determine a suitable step for the entire system. Fast type-one encounters, unlike-pair approaches and interactions among large particles all contribute. One common time step must accommodate the relevant demanding motion of the model. When hydrogen, rigid water or FENE chains are introduced later, mass, force variation and constraints will again guide that assessment.

A numerical comparison should reduce one principal uncertainty at a time. Here the force field and initial state are fixed while the step changes over equal observation durations. Clear convergence as the step decreases provides evidence about time discretisation. If the measured discrepancy changes little, cutoff discontinuities, output precision and other settings become useful next checks. The purpose is not to force a particular scaling relationship onto the results, but to let the defined calculation determine the informative next comparison.

## Why a cutoff leaves a signature in energy

The LJ expression retains a gradually weakening attractive tail at large distances. Treating that interaction without a finite cutoff would change the computational organisation and boundary treatment. This example stops the pair interaction at distance four. The cutoff is part of the model and also affects interpretation of the numerical energy trace. Its absolute value is only part of the information: comparing it with each pair’s σ locates it on the corresponding potential curve.

For type one, σ equals one, so the cutoff lies at four σ. For type two, σ equals three, so the same absolute distance is only about 1.333 σ. Its energy minimum lies near 3.367, leaving the cutoff in an appreciably attractive region. Sharing one absolute cutoff does not retain the same relative extent of attraction for every type. This detail of the actual input explains why a cutoff of four cannot be interpreted as equally distant for all interactions without examining their parameters.

The upstream unshifted form retains the original LJ energy inside the cutoff and sets it to zero outside. Because the inner value generally has not reached zero, a pair crossing produces a jump in reported potential energy. The ordinary truncated-force calculation does not add an impulse corresponding to that energy step. Reducing the integration step can therefore leave changes associated with the unshifted energy convention. This is distinct from inadequately resolving an encounter in time.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l03/en/#en-s5)

Figure 4 · Energy shifting removes the energy step at the cutoff while retaining the force discontinuity.

One common treatment subtracts the cutoff value from the energy inside the cutoff, joining the energy continuously to zero. This is an energy shift. Subtracting a constant leaves the interior pair force unchanged while improving continuity at the boundary. The force can still jump from a nonzero value to zero, so shifting energy is distinct from smoothing force. Force shifting or switching generally changes interactions over some distance interval and must be included in the model definition.

Join the energy continuously to zero at the cutoffEq. 5

![Join the energy continuously to zero at the cutoff](https://ml-biomat.com/static/agent-math/de3322fb083f1775bc032237.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Uₛ | Energy-shifted pair potential | ε₁₁ |
| U_{LJ} | Original 12/6 Lennard–Jones expression | ε₁₁ |
| r, r_{c} | Current separation and cutoff distance | σ₁₁ |
| U_{LJ}(r_{c}) | Original value at the cutoff, constant for a given pair type | ε₁₁ |
| <, ≥ | Choose a branch according to separation | 1 |
| =, −, × | equality connects expressions for the same quantity; subtraction takes a difference or sets a negative direction; adjacent factors multiply. | operators are dimensionless |

Reading the relationshipSubtracting the cutoff value makes the inner energy approach zero at the boundary. The derivative of that interior constant is zero, preserving the local force.

A worked exampleFor type two, ε = 0.5, σ = 3 and r_c = 4 give U_LJ(r_c) ≈ −0.292604. The original minimum −0.5 becomes about −0.207396. Its position and the interior force are unchanged.

ConditionsEnergy becomes continuous while force can still jump at the cutoff. This is shift yes for the present lj/cut model, distinct from force shifting, switching or extending the cutoff.

The three principal comparisons retain the same cutoff convention. Energy changes are interpreted alongside the time step with the unshifted cutoff explicitly retained. A further labelled comparison could shift the energy and repeat the same step sequence to investigate the cutoff contribution. Changing the cutoff length also calls for examining pressure, structure and other equilibrium properties. Numerical analysis is more than making a trace flatter: it identifies whether a modification changes the reported quantity, the actual dynamics, or both.

The same care matters in more complex biomaterial force fields. Short-range dispersion, long-range electrostatics, bond constraints and external walls have their own treatments. An energy check must include the relevant model terms and account for applied work and finite constraint tolerances. The habit learned from the LJ model transfers directly: establish the composition of energy, identify numerical approximations that affect it, and construct comparisons targeting those factors.

## Neighbour lists accelerate a changing calculation

A particle interacts through short-range forces only with neighbours inside the cutoff, but the program must identify potential neighbours. Checking every possible pair at every step becomes expensive as the system grows. A neighbour list collects candidates within a slightly larger range, and subsequent force calculations inspect that list. It resembles listing nearby shops before deciding which are within a particular walking distance. The extra shell beyond the interaction range allows particles to move between list rebuilds.

The extra distance is called the skin. Candidate range extends to the force cutoff plus skin, while the actual pair force still uses the physical cutoff. A larger skin generally increases the number of candidates inspected each step while potentially reducing rebuild frequency; a smaller skin makes the opposite tradeoff. The setting organises computation and should not be confused with extending the physical interaction range. Neighbour counts and rebuild statistics in the log help explain the computational cost.

The candidate list extends beyond the force rangeEq. 6

![The candidate list extends beyond the force range](https://ml-biomat.com/static/agent-math/14ce6948f10439ee18739497.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| r_{list} | Range used to construct the candidate list | σ₁₁ |
| r_{c} | Physical pair-force cutoff | σ₁₁ |
| s | Skin: the extra candidate distance | σ₁₁ |
| =, +, × | equality connects expressions for the same quantity; addition combines contributions; adjacent factors multiply. | operators are dimensionless |

Reading the relationshipThe extra shell retains candidates that can move between rebuilds. Actual forces still use r_c.

A worked exampleWith r_c = 4 and s = 0.3, candidates extend to 4.3. A pair separated by 4.2 can appear in the list while its truncated LJ force is zero.

ConditionsThis explains a short-range neighbour list; timely rebuilding and communication remain part of correctly updating neighbours.

A stale list can omit a particle that has moved from outside the candidate shell into interaction range. With displacement checking enabled, the program considers movement since the previous build when deciding to rebuild, subject to schedules such as every and delay. This example retains dynamic updates so that changing neighbourhoods are followed. Disabling updates simply to save time can affect completeness of the force calculation rather than only its speed.

Larger time steps often produce larger movements per step, so integration and neighbour-update problems can appear together. Lost particles, extreme energies or neighbour-related messages call for examining geometry, velocity scales, time steps and list schedules. A large skin does not repair an integration step that leaps across a strongly repulsive region, and a small step does not make a permanently stale list suitable. The settings address distinct tasks even though their effects can interact.

Understanding these mechanisms in a simple case makes later chain and network calculations easier to diagnose. Bonded atoms retain topological connections even when assigned to different processor regions, and crosslinks change which neighbours receive special treatment. Geometry, connectivity and communication then all matter. The present unbonded system establishes the distinction between a candidate list and an actual interaction, which becomes a foundation for checking force completeness in more complex models.

## Run three comparisons from a common origin

Each comparison reads the same positions and velocities from equilibrated.restart, saved after the bath interval. Resetting the counter then expresses all curves as elapsed time from this common origin. A run 0 evaluates quantities at the current state without advancing dynamics and provides the initial energy. That reference matters because subsequent numerical records are written every ten steps: different step sizes give different first-record times. Those first saved records must not all be silently treated as the same zero-time state.

### Compare time steps from a common state

```
# Same tutorial-derived state and interaction model at several time steps.
# Run with: lmp -var dt 0.005 -in timestep.lmp
variable dt index 0.005
units lj
read_restart equilibrated.restart
reset_timestep 0
timestep ${dt}
variable count equal round(20.0/v_dt)
variable t equal time
variable T equal temp
variable E equal etotal/atoms
thermo 100
thermo_style custom step time temp pe ke etotal press
thermo_modify norm no flush yes
fix integrator all nve
run 0
print "$(step) $(time) $(temp) $(etotal/atoms)" file timestep-${dt}-initial.dat screen no
fix records all ave/time 10 1 10 v_t v_T v_E file timestep-${dt}.dat
run ${count}
write_dump all custom timestep-${dt}-final.lammpstrj id type x y z vx vy vz modify sort id
```

Reads one restart, records initial temperature and per-particle energy at t = 0, then advances twenty reduced time units.

Dividing twenty by the selected step gives 8000, 4000 and 2000 steps. The -var command-line option supplies the time step to one input, avoiding three near-duplicate scripts that could acquire unintended differences. Output names retain the selected step size. Every branch reads the common restart rather than continuing from the previous branch’s final state. This creates parallel comparisons from a common origin rather than consecutive intervals with different starting conditions.

### Three step sizes, equal elapsed time

```
lmp -var dt 0.0025 -in timestep.lmp
lmp -var dt 0.005 -in timestep.lmp
lmp -var dt 0.01 -in timestep.lmp
```

The directory needs equilibrated.restart from Lesson 1. Each branch rereads that state and names outputs by time step.

The analysis reads both the initial-state file and the time series, subtracting the initial per-particle total energy from each recorded value. The vertical axis then shows energy change directly instead of requiring small differences to be read against a large baseline. It uses an absolute reduced-energy difference rather than dividing by a possibly near-zero initial total energy. Cancellation between kinetic and potential terms can make percentage errors unusually sensitive without clarifying the magnitude of the numerical change.

Define energy departures from a common initial stateEq. 7

![Define energy departures from a common initial state](https://ml-biomat.com/static/agent-math/30b63b613d40933f954aa913.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| e(t), e(0) | Per-particle total energy at time t and at the common origin | ε₁₁ |
| Δe(t) | Energy change relative to the initial state | ε₁₁ |
| t_{end}, tⱼ | End time and time of saved record j | τ |
| Δe_{end} | Final-minus-initial energy | ε₁₁ |
| A_{e} | Largest absolute energy departure among saved records | ε₁₁ |
| max, \| · \| | Maximum; absolute value | 1 |
| =, −, × | equality connects expressions for the same quantity; subtraction takes a difference or sets a negative direction; adjacent factors multiply. | operators are dimensionless |

Reading the relationshipSubtracting a defined initial value makes small changes visible. Endpoint change and maximum saved excursion then describe different aspects of the trace.

A worked exampleIf e(0) = 1.10 and later records are 1.10003, 1.09998 and 1.10001, the endpoint change is 0.00001 while A_e = 0.00003. Closely matching endpoints can coexist with a larger interior excursion.

ConditionsRuns share an initial state and end time. A_e applies to saved values; different output intervals resolve rapid extrema differently.

The program reports the final-minus-initial energy and the largest absolute departure among saved records. The former describes the endpoint change; the latter describes the observed excursion. With output every ten steps, recording intervals are 0.025, 0.05 and 0.1. The plot retains these actual sampling times rather than disguising them as equally dense records. Its maximum is explicitly a maximum over saved values. Comparing unsaved rapid extrema would require a suitably dense, common physical recording interval.

### Complete initial-state alignment and energy analysis

```
"""Compare actual LAMMPS NVE energy traces at equal elapsed time.

python analyze_timestep.py --data-dir . --shifted-dir shifted --language en
Requires NumPy and Matplotlib.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def load_series(directory, prefix, label):
    initial = np.loadtxt(directory / f'{prefix}-{label}-initial.dat', ndmin=1)
    table = np.loadtxt(directory / f'{prefix}-{label}.dat', comments='#', ndmin=2)
    if initial.shape != (4,) or table.shape[1] != 4:
        raise ValueError('Expected step,time,temperature,energy_per_particle.')
    if not np.all(np.isfinite(initial)) or not np.all(np.isfinite(table)):
        raise ValueError('All recorded values must be finite.')
    # Use the explicitly recorded common initial state, never a later first sample.
    table = table[table[:, 1] > initial[1]]
    table = np.vstack((initial, table))
    time = table[:, 1] - initial[1]
    if not np.all(np.diff(time) > 0) or not np.isclose(time[-1], 20.0):
        raise ValueError('Each comparison must advance monotonically to time 20.')
    delta = table[:, 3] - initial[3]
    return time, delta, {
        'step_size': float(label),
        'initial_energy_per_particle': float(initial[3]),
        'elapsed_reduced_time': float(time[-1]),
        'saved_values_including_initial_state': len(time),
        'final_energy_change_per_particle': float(delta[-1]),
        'max_absolute_recorded_energy_change_per_particle': float(np.abs(delta).max()),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=Path('.'))
    parser.add_argument('--shifted-dir', type=Path)
    parser.add_argument('--out-dir', type=Path, default=Path('comparison'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args()
    zh = args.language == 'zh'
    plt.rcParams.update({'font.family': ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC', 'WenQuanYi Zen Hei', 'DejaVu Sans'] if zh else ['DejaVu Sans'],
                         'font.size': 14, 'svg.fonttype': 'path',
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.labelcolor': '#173c42', 'text.color': '#173c42'})
    sources = [('unshifted', args.data_dir, 'timestep')]
    if args.shifted_dir is not None:
        sources.append(('shifted', args.shifted_dir, 'shifted'))
    fig, axes = plt.subplots(len(sources), 1, figsize=(11.5, 4.8 * len(sources)),
                             squeeze=False, layout='constrained')
    fig.set_facecolor('#faf9f5')
    summary = {}
    for ax, (name, directory, prefix) in zip(axes[:, 0], sources):
        ax.set_facecolor('#faf9f5')
        rows = []
        initial_values = []
        for label, color in [('0.0025', '#167d84'), ('0.005', '#bb7448'), ('0.01', '#486fa9')]:
            time, delta, row = load_series(directory, prefix, label)
            rows.append(row)
            initial_values.append(row['initial_energy_per_particle'])
            ax.plot(time, delta, color=color, linewidth=1.5, label=f'Δt = {label}')
        if not np.allclose(initial_values, initial_values[0], rtol=0, atol=1e-10):
            raise ValueError('Initial energies must agree across step sizes for each model.')
        summary[name] = rows
        if name == 'unshifted':
            title = '原截断模型：保留未平移势能' if zh else 'Original cutoff: unshifted energy'
        else:
            title = '势能平移对照：相同的截断力' if zh else 'Energy-shift comparison: unchanged truncated forces'
        ax.set_title(title, loc='left', fontsize=16, pad=15)
        ax.axhline(0, color='#879995', linewidth=0.7)
        ax.set_xlim(0, 20)
        ax.set_xlabel(('约化时间 ' if zh else 'Reduced time ') + r'$t/\tau$')
        ax.set_ylabel(('每粒子能量变化 ' if zh else 'Energy change per particle ') + r'$\Delta e/\epsilon_{11}$')
        ax.ticklabel_format(axis='y', style='sci', scilimits=(-3, 3), useMathText=True)
        ax.grid(axis='y', alpha=0.16)
        ax.legend(frameon=False, ncol=3)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out_dir / f'timestep-comparison-{args.language}.png', dpi=200)
    fig.savefig(args.out_dir / f'timestep-comparison-{args.language}.svg')
    plt.close(fig)
    (args.out_dir / 'timestep-summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
```

Reads each explicitly saved initial energy and checks common initial energies within a model and equal endpoints at twenty.

### Time-step comparison for the original cutoff model

Three time steps advance from one initial state to 20τ. Each curve subtracts its explicitly saved initial per-particle energy and retains the unshifted-cutoff effect.

LAMMPS 30 Sep 2026 update 1; a three-dimensional periodic box with 1,500 type-1 and 100 type-2 particles. Reduced units, time step 0.005 and total duration 150. Physical inputs follow the binary Lennard–Jones tutorial by Gravelle and colleagues, with added NVE comparisons and numerical output.

[Download reference data and complete inputs (ZIP) 6.73 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-lj-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l03/en/#en-s7)

Each run starts from the same equilibrated restart and ends at t* = 20. Its total energy is referenced to the separately recorded common initial time t* = 0 and divided by particle count.

The additional comparison retains the restart, three time steps and twenty-unit duration, adding only pair_modify shift yes to the interaction settings. It changes how each pair energy joins at the cutoff while retaining the interior forces. Final coordinates and velocities, compared by ID at matched step sizes, agree with those saved in the original branches. The energy records nevertheless vary on different scales. Displaying both sets therefore examines the effect of the energy convention on numerical diagnosis while retaining the same model motion for each matched branch.

In these actual twenty-time-unit records, the shifted comparison has maximum per-particle energy departures of about 1.34 × 10⁻⁴ at step 0.01, 4.00 × 10⁻⁵ at 0.005, and 1.45 × 10⁻⁵ at 0.0025. These values refer to this initial state and its recording intervals, and show smaller observed excursions with decreasing step size. The maxima in the unshifted records are instead all near 0.005. Changes associated with the cutoff energy step obscure the smaller differences exposed by the shifted-energy diagnostic.

### Complete input adding only an energy shift

```
# Same checkpoint as the unshifted branches; potential shifted to zero at rc.
# Forces retain the original cutoff discontinuity.
# Same tutorial-derived state and interaction model at several time steps.
# Run with: lmp -var dt 0.005 -in timestep.lmp
variable dt index 0.005
units lj
read_restart equilibrated.restart
pair_modify shift yes
reset_timestep 0
timestep ${dt}
variable count equal round(20.0/v_dt)
variable t equal time
variable T equal temp
variable E equal etotal/atoms
thermo 100
thermo_style custom step time temp pe ke etotal press
thermo_modify norm no flush yes
fix integrator all nve
run 0
print "$(step) $(time) $(temp) $(etotal/atoms)" file shifted-${dt}-initial.dat screen no
fix records all ave/time 10 1 10 v_t v_T v_E file shifted-${dt}.dat format " %.15g"
run ${count}
write_dump all custom shifted-${dt}-final.lammpstrj id type x y z vx vy vz modify sort id
```

pair_modify shift yes retains the forces and cutoff rule while changing the energy connection at the cutoff. Numerical output precision is also increased.

### Run the energy-shift comparison and generate bilingual plots

```
lmp -var dt 0.0025 -in shifted.lmp
lmp -var dt 0.005 -in shifted.lmp
lmp -var dt 0.01 -in shifted.lmp
python analyze_timestep.py --data-dir . --shifted-dir . --out-dir comparison --language zh
python analyze_timestep.py --data-dir . --shifted-dir . --out-dir comparison --language en
```

The timestep and shifted prefixes distinguish the two sets of outputs within one exercise directory.

### An energy shift makes time-step differences clearer

Upper: original unshifted energy. Lower: shifted energy. For each matched time step, final coordinates and velocities agree at the saved precision; forces are unchanged.

LAMMPS 30 Sep 2026 update 1; 1,600 binary Lennard–Jones particles; NVE at Δt* = 0.0025, 0.005 and 0.01. The comparison adds pair_modify shift yes. Forces within the cutoff are unchanged and the force remains unsmoothed at the cutoff.

[Download reference data and complete inputs (ZIP) 0.29 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-lj-shifted-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l03/en/#en-s7)

One restart state, the same three step sizes and an observation time of 20τ. The upper panel uses the original truncated energy and the lower panel the shifted energy, each with its own readable vertical scale. Final coordinates and velocities agree at saved precision for each step size; the energy definition explains the difference between panels.

The vertical scales of the two panels consequently differ substantially. Read the axis magnitude before comparing the visual height of fluctuations. Equal screen distances can represent very different energy changes. The force still has its original cutoff discontinuity, and these finite-duration traces are not forced into an assumed power-law fit. The comparison answers a more specific question: with the original forces retained, does making energy continuous at the cutoff expose distinctions among time steps? In these records, that distinction becomes clearly visible.

The diagnostic also illustrates the value of retaining both the original model and the changed condition. A different switching function would call for checking effects on structure, pressure and target dynamics. A change of output precision or units instead calls for verifying that the recorded quantity retains its intended meaning. Each modification has its own comparison. Keeping the inputs, common origin and analysis definition together lets another reader repeat the reasoning, rather than treating a smoother-looking line as self-contained evidence.

First confirm a common initial state and an endpoint of twenty, then compare overall changes and short-time fluctuations. Features that shrink with the step can be discussed in relation to integration resolution. Persistent jumps or baseline changes invite examination of the unshifted cutoff. Temperature provides a complementary view of kinetic behaviour. Interpretation follows the relationships in the actual curves, rather than prescribing a squared-step scaling solely because a particular integration algorithm was used.

Computational cost matters under comparable conditions. Smaller steps require more updates over a fixed elapsed time, while actual runtime also depends on neighbour rebuilds, hardware, parallel settings and output. The practical choice seeks adequate accuracy in the target quantities together with enough observation time. Extremely fine resolution of already well-resolved fast motion can consume time needed to sample slow structure. Numerical accuracy and sufficient sampling therefore belong in the same design rather than being optimised independently.

## Carry numerical evidence into more complex materials

The comparison can now be described in three connected ways. Physically, particles exchange kinetic and potential energy under selected interactions in a fixed box. Algorithmically, velocity Verlet advances coordinates and velocities using old and new forces, while an updated neighbour list supplies candidates. In the data, energy departures are measured relative to a common initial state. These descriptions connect but have distinct concepts. Software parameters become conditions whose rationale can be explained rather than numbers to memorise.

Adding chemical bonds can introduce rapid stretching vibrations; constraining selected bond lengths changes the time-scale considerations. Coarse graining several atoms into a bead removes internal degrees of freedom and requires reconsidering interaction parameters and dynamical mapping. These operations involve more than increasing the current timestep command. They reconnect model, algorithm and target properties. The comparison structure remains useful as complexity grows: define a common origin, change one choice, and inspect quantities relevant to that choice.

With a thermostat, total energy changes can reflect physical exchange with the bath, so the isolated-interval criterion must be adjusted. Stretching a network introduces applied work, and a pressure-controlled box exchanges energy through volume changes. A numerical check first identifies the channels connecting system and surroundings and then selects suitable conserved or statistical quantities. The next lesson develops this point by examining how temperature, pressure and boundaries represent an environment and influence observed motion.

Consider two checks of understanding. Why can shifting the energy inside a cutoff leave a trajectory unchanged while changing its reported energy trace? The answer combines the zero derivative of an interior constant with the changing number of pairs inside the interaction range. Why is halving the step while retaining the step count not an endpoint comparison at equal time? The modified calculation covers only half the duration. These questions connect mathematics with experimental design and transfer more readily than memorising one recommended step.

For each later material model, numerical choices should connect to the same complete explanation: which motions are retained, which forces vary fastest, which quantities check the result, how much elapsed time is compared, and whether output resolves the relevant change. Complexity makes these questions more specific rather than removing them. Connecting force, energy and time in the particle box prepares us to explain the numerical evidence behind curves for molecules, chains and networks.

## Further Reading and Open Materials

- [LAMMPS Tutorial 1: Lennard-Jones fluid](https://lammpstutorials.github.io/sphinx/build/html/tutorial1/lennard-jones-fluid.html) · Simon Gravelle; Cecilia M. S. Alvares; Jacob R. Gissinger; Axel Kohlmeyer · CC BY 4.0

  Original binary-particle model, LJ interactions and NVE workflow.

  Added force derivation, integration steps, equal-duration step comparisons and an energy-shift diagnostic.
- [LAMMPS stable manual: fix nve](https://docs.lammps.org/stable/fix_nve.html) · LAMMPS developers · Official technical documentation; software source GPL-2.0; no copied figures

  Velocity-Verlet algorithm and NVE conditions.

  Original worked examples and algorithm diagram.
- [LAMMPS stable manual: pair_style lj/cut](https://docs.lammps.org/stable/pair_lj.html) · LAMMPS developers · Official technical documentation; no copied figures

  Potential, cutoff, mixing and shift option.

  Analytic figures and actual-run comparisons for the two parameter sets.
- [Computer Experiments on Classical Fluids. I. Thermodynamical Properties of Lennard-Jones Molecules](https://doi.org/10.1103/PhysRev.159.98) · Loup Verlet (1967) · Cited paper; no article text or figures reproduced

  History of computational experiments on classical fluids.

  Original diagram connects the historical task with the present integration exercise.
