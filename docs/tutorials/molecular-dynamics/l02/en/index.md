# From an Input File to a First Trajectory

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l02/en/
Language: en

Connect inputs, trajectories, numerical tables and restart states, and turn actual coordinates into interpretable figures.

## Turn motion into a readable record

When recording a growing plant, the video is only one part of the experiment. The frame interval, lighting conditions and time assigned to each image are needed to compare growth rates. A molecular trajectory has the same requirement: moving particles show that a model produced a history, while interpretation depends on the parameters, integration time, particle identities and numerical records behind it. This lesson builds those connections. The familiar binary-particle system becomes a record that can be read again, analysed and continued from a saved state.

By the end, you can locate the definition of a data column in the input, distinguish an instantaneous reading from a time average, separate wrapped display coordinates from continuous coordinates, and run a complete Python analysis. We also distinguish starting again from continuing a saved state. The first operation reconstructs initial conditions; the second inherits positions and velocities already reached. These serve different purposes. Programming experience is not assumed: the analysis is introduced through reading files, selecting records, calculating quantities and drawing figures.

The files from a simulation are different records of one experiment. The input describes preparation and dynamics; the log records execution conditions, stages and values; a trajectory stores selected particle attributes at selected times. A text data file describes one state in a format convenient for inspection and exchange, while a binary restart file preserves additional state for continuation by compatible software. Their contents overlap but their purposes differ. An animation alone retains a visual impression and discards much of the information needed to redefine a measurement or check its units.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l02/en/#en-s1)

Figure 1 · File roles follow their stored information, connected through one run’s definitions and time.

A concrete question helps test an output design: how far did one particle move during the final run interval? Its identity requires an atom ID, its observation times require steps and a time step, and boundary crossings require unwrapped coordinates or image flags. A final screenshot cannot supply that information, nor can a total-energy column. It is therefore useful to work backwards from the intended measurement to the required fields, rather than saving every available quantity without deciding what each will answer.

A useful historical example is Rahman’s 1964 study of liquid argon. It followed 864 particles interacting through a Lennard–Jones potential and obeying classical equations of motion. Their recorded motion was converted into quantities such as spatial correlations and self-diffusion and compared with experiment. One lasting idea is that microscopic motion can become a quantitative observable. Modern graphics make trajectories easier to inspect, while the essential step remains the definition of a measurement that connects a collection of coordinates to a physical question.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l02/en/#en-s1)

Figure 2 · Rahman’s liquid-argon study connected microscopic motion with comparable observables. The path is a conceptual illustration.

The physical system remains the three-dimensional periodic binary-particle box, with reduced units and successive NVE and Langevin intervals. Holding that background fixed lets us focus on recording and analysis. Renaming an output column does not strengthen an attraction; changing the particle group used to calculate temperature changes the meaning of the measurement. Connecting how a file presents data with how the observable is defined is an important step from running an example to designing a study.

## An input is a sequence of actions

An input file is plain text: its characters describe commands, values, names and comments, without a word processor’s font or paragraph formatting. The .lmp extension helps people recognise its purpose; LAMMPS reads the contents. The terminal’s working directory acts like the folder currently open on a desk. Relative names are resolved from that location. Keeping the example input and analysis program together allows short filenames in the commands and helps preserve their relationships when the exercise directory is moved.

LAMMPS normally reads commands from top to bottom and acts on them as it encounters them. Units and atom attributes must be chosen before the box is created, while masses can be assigned after the corresponding atom types exist. This resembles preparing an experiment sheet: define the columns, establish the objects, fill in parameters and begin measurement. Comment headings help a reader but do not control execution. Moving commands within a script therefore requires attention to the information and settings that exist when each command is reached.

Text after a hash character is normally a comment explaining a line or a group of commands. Other names have distinct roles: simbox identifies a region, integrator identifies one fix, records identifies another, and T names a variable. A name does not itself create a thermostat or integrator; the command style defines the action. Stable, meaningful names make operations such as unfix bath easy to follow: that command removes the fix named bath, rather than deleting particles or stopping all dynamical evolution.

The ordinary meaning of fix can be misleading here. In LAMMPS, a fix is an operation that persists during a simulation. The nve style integrates motion, langevin modifies forces to represent a bath, and ave/time records or averages values according to a schedule. They can coexist because their jobs differ. Read fix together with its specific style, and ask whether that operation changes the state, applies a condition or records an observable. It does not generally mean holding particles still.

Variables connect reusable names with values or expressions. An equal-style variable can be evaluated from the current state when needed, for example to obtain temperature, time or energy. The expression pe/atoms explicitly divides the system potential energy by the current particle count. The input first sets thermo_modify norm no to retain thermodynamic totals, then performs this division explicitly in the variables. Each data column is named for the resulting per-particle quantity. Calling a variable U does not establish that it contains a total potential energy; its definition determines that meaning.

The complete input is shown again so that these explanations can be checked against the actual example. Identify the commands that establish objects, those that change state, and those that record observations. The three run commands do not recreate particles: each interval continues from the positions and velocities reached by the previous one. Adding and later removing the bath changes the environment of the existing state. This continuity explains why the three intervals are not three unrelated experiments.

### Create the system, advance the stages and record output

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

The same input is used in Lesson 1. Dump fields ix, iy and iz preserve periodic-unwrapping information. thermo.dat contains the step followed by seven requested values.

## Give numbers units and time an origin

A number gains physical meaning through its unit convention. A length of one might mean a metre, an ångström or one reduced length unit. LJ units choose a reference mass, length and energy and express model values relative to them. Think of choosing a ruler and recording how many rulers span an object. Changing the reference length without changing the number changes the physical interpretation. To express the same physical system in different units, all related parameters must be converted together.

The time scale is not an arbitrary fourth independent number. Energy dimensions connect mass, length and time, so fixing the first three reference quantities also fixes the reduced time unit. Kinetic energy provides the reasoning: velocity has units of length divided by time, and mass times squared velocity has energy units. Equating the energy built from the reference scales to the selected energy scale determines the time unit. For a binary model not mapped to a specific material, reporting reduced time is clearer than assigning an unsupported real-fluid time.

How reduced time relates to physical timeEq. 1

![How reduced time relates to physical time](https://ml-biomat.com/static/agent-math/6c83e924ecd276859ba28f61.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| τ₀ | Time reference determined by three base scales | s |
| σ₀ | Reference length; the tutorial uses type 1 as its reduced reference | m |
| m₀ | Reference mass | kg |
| ε₀ | Reference energy | J |
| t | Physical time in seconds | s |
| t* | Reduced time measured relative to τ₀ | 1 |
| √, / | Square root and division | 1 |
| =, /, × | equality connects expressions for the same quantity; the fraction divides numerator by denominator; adjacent factors multiply. | operators are dimensionless |

Reading the relationshipEnergy has dimensions kg·m²/s², so m₀σ₀²/ε₀ has units of squared time. Taking its square root defines the time reference, and multiplication converts a reduced time to physical time.

A worked exampleFor a unit-conversion exercise, choose m₀ = 10⁻²⁶ kg, σ₀ = 10⁻¹⁰ m and ε₀ = 10⁻²¹ J. Then τ₀ = √(10⁻²⁵ s²) ≈ 3.1623 × 10⁻¹³ s, and a reduced time of 10 corresponds to 3.1623 × 10⁻¹² s.

ConditionsThe numerical scales illustrate unit arithmetic; they do not assign this binary-particle model to a particular material. A material mapping also requires appropriate interactions and validation of the target properties.

Step numbers also need an origin. After minimisation, reset_timestep 0 sets the starting counter for dynamics. Each following step advances 0.005 reduced time units, so the intervals end at steps 5000, 20000 and 30000. Resetting the counter changes labels; it does not return coordinates and velocities to their initial state. Before joining two files that both begin at step zero, determine whether they describe independent runs or different segments of one history that have been renumbered.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l02/en/#en-s3)

Figure 3 · This timeline matches the input. Output intervals select saved states; integration intervals govern advancement of the state.

Recording and integration intervals are separate. The trajectory is saved every 200 steps, giving a frame interval of one reduced time unit. Thermodynamic data are written every 100 steps, or half a time unit. The files therefore have different record counts, and row one hundred must not simply be paired with frame one hundred. Align records by step or time, like synchronising cameras using timestamps. To compare a structure with its energy, select times present in both outputs.

Sparser records reduce file size, but the information lost depends on the question. They may suffice for a slowly developing aggregate while missing the details of rapid velocity changes. Interpolating a smooth curve afterward cannot recover unsaved events. The present schedule serves file reading and continuous-coordinate reconstruction and shows motion over longer intervals. A study of rapid collisions or velocity correlations would choose its output schedule from the time scale of that process, alongside an appropriate integration time step.

When a file reports density, ask what is being counted. There are 1600 particles but a total mass of 2000 reference mass units because the two types have different masses. In a box volume of 64000 reference volume units, number density is 0.025 and mass density is 0.03125. The LAMMPS keyword density reports the latter. This illustrates why quantities sharing an everyday name can only be compared after their numerator, denominator and units have been established.

## A trajectory is a repeated particle table

A custom trajectory contains successive frame records. Each frame gives a step, atom count and box bounds before listing particle attributes. The names following ITEM: ATOMS identify the columns. This example saves IDs, types, coordinates, velocities and three image flags. The reader finds columns by their names rather than permanently assuming that one numerical position contains x. If charge is added or column order changes, the analysis can still verify what it has read instead of silently using the wrong field.

IDs connect records through time. Parallel execution may change output order, and display software may reorder particles by position. Sorting the dump by ID helps human inspection, but the analysis still explicitly locates the requested ID so that physical identity does not depend on a row number. Types distinguish the two particle classes. In this fixed-type model, both ID and type should remain consistent. Duplicate IDs or unexpected changes in particle count call for a data-integrity check before interpreting motion.

Periodic coordinates fold an extended path back onto one map. After a particle exits through the right side, its displayed coordinate returns to the left, while an image flag tracks how many boxes it has crossed. In a fixed orthogonal box, adding the wrapped coordinate to the image count times box length reconstructs the unwrapped coordinate. Positive and negative crossings update the count accordingly. Differences of unwrapped coordinates describe displacement; differences of wrapped coordinates can turn a short crossing into an apparent jump across almost the entire box.

Reconstruct a continuous path from periodic coordinatesEq. 2

![Reconstruct a continuous path from periodic coordinates](https://ml-biomat.com/static/agent-math/6fa6bc506e7f3bdb2261eb69.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| x(t) | Wrapped x coordinate at time t | σ₁₁ |
| xᵤ(t) | Unwrapped coordinate at the same time | σ₁₁ |
| iₓ(t) | Signed integer image flag in x | 1 |
| Lₓ | Fixed orthogonal-box length along x | σ₁₁ |
| t, t₀ | Current and selected initial time | τ |
| Δx | x displacement from the selected origin | σ₁₁ |
| Δ | Difference from the initial value | 1 |
| =, +, −, × | equality connects expressions for the same quantity; addition combines contributions; subtraction takes a difference or sets a negative direction; adjacent factors multiply. | operators are dimensionless |

Reading the relationshipEvery periodic crossing shifts a displayed coordinate by one box length. The image count restores those integer lengths so successive frames belong to one continuous path.

A worked exampleWith bounds −20 to 20, Lₓ = 40. Initially x = 19.8 and iₓ = 0; later x = −19.7 and iₓ = 1. The final unwrapped coordinate is 20.3, giving displacement 0.5 rather than −39.5.

ConditionsThis form applies to the fixed orthogonal periodic box and requires correct recorded image flags. Tilted or deforming boxes require the corresponding box-vector and deformation treatment.

Move a continuous coordinate through periodic boxes of length 40. The map remains between −20 and 20.

[Figure: Position within the periodic box](https://ml-biomat.com/tutorials/molecular-dynamics/l02/en/#en-s4)

At a boundary, the displayed coordinate wraps while the image count preserves the continuous path. Drag the slider or use arrow keys.

Two widely separated wrapped frames do not uniquely reveal the number of intervening crossings. Identical displayed positions could mean little movement or a complete circuit of the box. Inferring crossings from the shortest displacement between frames assumes that each component moved less than half a box length; sparse output can violate that assumption. Recording image flags avoids that particular ambiguity. The analysis checks that the required fields are present and identifies missing fields explicitly, rather than quietly reconstructing an uncertain path.

The reconstruction also has geometrical conditions. This box is orthogonal and fixed, so directions can be handled independently. A tilted box requires image counts combined with box vectors, and a deforming box requires care in separating bulk deformation from motion relative to that deformation. Stretching and flow lessons will revisit those conditions. The simple box makes the relation among identity, position and displacement visible before geometrical complexity is added. An uncomplicated formula is useful when its applicable geometry is understood.

The actual path plot retains both wrapped and unwrapped coordinates for the same named particle. Comparing them reveals jumps at periodic seams while the unwrapped record preserves one continuous history. Selecting another particle shows another path. One path is useful for understanding the record; a diffusion estimate requires suitable averaging over particles and time origins. Keeping these levels distinct prepares us to connect trajectory analysis to material properties without treating the appearance of a single route as a diffusion measurement.

### Wrapped coordinates and continuous path of one particle

Particle 1 x coordinates from the actual trajectory. Recorded image flags reconstruct the unwrapped path, with time matched to thermo.dat.

LAMMPS 30 Sep 2026 update 1; a three-dimensional periodic box with 1,500 type-1 and 100 type-2 particles. Reduced units, time step 0.005 and total duration 150. Physical inputs follow the binary Lennard–Jones tutorial by Gravelle and colleagues, with added NVE comparisons and numerical output.

[Download reference data and complete inputs (ZIP) 6.73 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-lj-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l02/en/#en-s4)

Recorded image flags connect positions on opposite sides of the periodic box into a continuous path. Jumps in the wrapped coordinate and the continuous unwrapped coordinate describe the same particle on the same physical time axis.

## Understand a reading before averaging it

The log is useful for following execution stages, but it mixes headings, warnings, performance information and multiple numerical tables. Reading the entire log as one rectangular array often fails on text lines. The input therefore writes selected values to thermo.dat for a clearer analysis exercise. After its comment header, each row contains step, time, temperature, per-particle potential, kinetic and total energies, pressure and mass density. The log remains part of the record for understanding run conditions and termination.

The three integers following fix ave/time define the sampling and output schedule; the name alone does not imply substantial averaging. Here 100 1 100 samples every 100 steps, includes one sample in each output, and writes every 100 steps. The result is a sequence of instantaneous readings. A schedule of 10 10 100 instead samples every ten steps and combines ten samples in each output interval. The files can contain the same number of rows while describing different temporal resolutions.

Choose a physical interval before calculating its average. The first 25 time units have no bath, the next 75 include a bath, and the final 50 remove it again. Averaging temperature or energy across all stages mixes changes in the environment with fluctuations within a stage. To inspect the latter portion of the bath interval, we can select records with time at least 50 and less than 100. The same interval should appear in the calculation and caption so the average has an explicit temporal scope.

A window mean and the spread of its readingsEq. 3

![A window mean and the spread of its readings](https://ml-biomat.com/static/agent-math/a90ab6cb23a637e3e2e1b784.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Tⱼ | Temperature reading j in the selected window | ε₁₁/k_B |
| T̄ | Arithmetic mean of temperatures in the window | ε₁₁/k_B |
| M, j | Number of records and summation index | 1 |
| s_{T} | Sample standard deviation using denominator M − 1 | ε₁₁/k_B |
| Σ, √, ² | Summation, square root and squaring | 1 |
| =, −, /, × | equality connects expressions for the same quantity; subtraction takes a difference or sets a negative direction; the fraction divides numerator by denominator; adjacent factors multiply. | operators are dimensionless |

Reading the relationshipAverage the readings, then add squared deviations to measure their spread. The square root restores temperature units; M − 1 is the usual sample-variance convention.

A worked exampleReadings 0.9, 1.0 and 1.1 have mean 1.0. Their squared deviations sum to 0.02; dividing by 2 and taking a square root gives s_T = 0.1.

ConditionsM must be at least 2 and readings must share a definition and units. This describes spread within the window, not the standard error of a correlated mean. Using M − 1 does not remove temporal correlation.

A mean compresses readings to a centre, while their standard deviation describes spread around that centre. Here the standard deviation measures fluctuations of instantaneous values within the selected window; it is not automatically the uncertainty of the mean. Adjacent temperatures can be correlated, so a hundred rows contain less information than a hundred independent experiments. The later statistical-design lesson develops correlation times, blocking and independent runs. For now, retaining the curve, interval and spread prevents one decimal number from hiding the temporal structure of the measurement.

Known algebraic relations provide another useful check. Total energy should equal kinetic plus potential energy when the three columns share a time and normalisation. The program evaluates that difference row by row and reports its largest absolute value. Limited decimal output can produce small rounding discrepancies. A difference comparable to the energies themselves calls for checking column order, total versus per-particle values, or accidental alignment of different times. Such a check tests data meaning rather than merely whether a plotting command ran without an error.

Check column consistency through energy additionEq. 4

![Check column consistency through energy addition](https://ml-biomat.com/static/agent-math/455d9e6f35cac1d609db80b5.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| eⱼ, kⱼ, uⱼ | Per-particle total, kinetic and potential energy on row j | ε₁₁ per particle |
| j | Record index | 1 |
| δ_{E} | Largest energy-addition residual over the records | ε₁₁ per particle |
| \| · \| | Absolute value, retaining the magnitude of a difference | 1 |
| max | Select the largest value among the specified records | 1 |
| =, −, × | equality connects expressions for the same quantity; subtraction takes a difference or sets a negative direction; adjacent factors multiply. | operators are dimensionless |

Reading the relationshipAt a common time and normalisation, total energy equals kinetic plus potential energy. A row-wise subtraction followed by a maximum detects possible column, alignment or normalisation errors.

A worked exampleFor e = 0.750001, k = 1.25 and u = −0.5, the row residual is 0.000001. The calculation then finds the largest magnitude across all rows. Output precision affects such small residuals.

ConditionsThis checks algebraic consistency within a record. It is distinct from conservation of energy over time, examined using NVE comparisons in the next lesson.

A line on a plot also carries a reading convention: it joins saved discrete records and does not imply that every intervening point was measured. Excessive smoothing can erase spikes and correlations in thermal fluctuations. We retain a thin line for the raw records and use subdued backgrounds to distinguish stages. Any additional window average should state its interval. Labelling axes with quantities and reduced units, including per-particle energy, makes comparisons more direct than leaving these definitions in an unrelated paragraph.

It is also useful to notice the precision used when writing numbers. Internal floating-point values usually retain more significant digits than a compact text display. Writing and reading a file can therefore introduce rounding in the final digits. A modest precision may be sufficient to display a temperature trend, while a coordinate comparison after restarting benefits from more digits. Increasing the printed precision does not improve the integration algorithm; it preserves more of the values already calculated. Printed precision, numerical integration error and sampling uncertainty are therefore three separate ideas. They answer how much of a number was recorded, how accurately motion was approximated, and how much statistical information was gathered. Distinguishing them makes a small discrepancy easier to interpret.

### Multi-panel record figure from actual numerical data

Generated by the complete analysis program on this page, retaining stage, temperature, per-particle energy and coordinate definitions. Standard deviation describes fluctuations within the selected window.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l02/en/#en-s5)

Generated directly by the complete Python analysis program on this page. All panels come from the same actual run; shading identifies the heat-bath stage, and the position curves follow one particle ID.

## From files to figures with a complete analysis

The program below uses Python to read text, NumPy to handle numerical columns and Matplotlib to draw figures. Their roles can be understood before learning their full syntax: Python arranges reading and decisions, NumPy applies operations to arrays, and Matplotlib maps values to axes and marks. Variable names label the stored quantities, such as time for a time column. Square brackets select part of an array, while Boolean conditions identify selected rows. These roles make much of the program readable as a flow of data.

When reading thermo.dat, the program skips hash-prefixed comments and checks the expected column count. It extracts time, temperature and the three energy terms and verifies strictly increasing time. A repeated or reversed time may result from joining restart segments with a shared endpoint or from resetting a counter. The program treats this as an input condition requiring an explicit decision, rather than sorting it away before understanding the cause. One continuous run of this example should advance according to the chosen recording interval.

The trajectory reader processes one frame at a time instead of treating the file as a single long array. It reads the step and box, identifies attribute names, finds the chosen particle ID, and extracts its x coordinate and x image flag. These fields and the box length determine the unwrapped coordinate. The reading order mirrors the file structure, allowing truncated frames or absent fields to be identified. Streaming also saves memory: a single-particle path does not require retaining every particle in every frame.

### Complete numerical-table and trajectory analysis

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

Reads actual thermo.dat and trajectory.lammpstrj, reconstructs unwrapped coordinates by particle ID, and saves PNG/SVG figures, a CSV path and a JSON summary.

Running the analysis produces a multi-panel figure and a compact numerical summary. The upper panels relate temperature and energy to the run intervals; the lower panel compares wrapped and unwrapped coordinates of one particle. The summary records the number of rows and frames, selected particle, averaging interval and maximum energy-sum discrepancy. These values describe what the figure actually uses. Changing the particle ID or analysis window and rerunning the program makes the consequences of changing a measurement definition directly visible.

### Run the analysis in the exercise directory

```
python analyze_records.py --data-dir . --out-dir analysis --particle 1 --window 50 100 --language zh
python analyze_records.py --data-dir . --out-dir analysis --particle 1 --window 50 100 --language en
```

The directory needs the two simulation outputs and the program above. The left window endpoint is included and the right excluded. NumPy and Matplotlib are required.

The program saves PNG for convenient viewing and SVG for scalable labels and curves. Both formats use the same actual numerical arrays. Changes to analysis rules should update the figure and summary together. Editing a legend or removing a point only in an image editor separates presentation from computation. Maintaining the link among input data, analysis and figure becomes especially useful when later comparing crosslink densities, solution concentrations or other families of simulation conditions.

Simple known relationships help check the program. Over a short interval with no boundary crossing, changes in the two x coordinates should agree. At a crossing, unwrapped and wrapped coordinates differ by an integer number of box lengths. The energy components should sum to the total on each row. These are interpretable physical and file relationships, rather than a requirement to reproduce one computer’s screen text. Satisfying them checks the analysis; sufficient sampling is a further question requiring suitable observation times and statistical design.

## Continue from a saved state

Long simulations are often divided into intervals. A system may first contact a bath and then undergo isolated evolution, or a completed interval may reveal a slow process worth observing longer. A restart file preserves a computational state so that the next run can inherit positions, velocities, box geometry and associated settings. It contains more information than a final image and is more suitable for continuation than coordinates alone. This example writes equilibrated.restart after removing the bath and uses it for deterministic NVE continuation.

Binary restart files are intended for compatible use with the same LAMMPS executable: version, build and platform can affect their interpretation. Text data files are easier to inspect and convert, while restarting from them requires reconstructing settings that they do not contain. The formats complement one another. Restart files support continuation; data files and inputs preserve an inspectable model description. Together they make it easier to examine parameters, move between software versions or reorganise a calculation later.

After reading the restart, the next integrator, computes and outputs must be declared as needed. A restart does not automatically replay the complete original input. The continuation script below re-establishes NVE integration, numerical records and trajectory output while preserving the time step. It does not call velocity create, which would replace velocities and change the state being continued. Reassigning velocities can be useful for a different question, but it creates an explicitly modified branch rather than continuing the existing motion unchanged.

### Split calculation that saves, clears and restores a state

```
units lj
read_restart equilibrated.restart
reset_timestep 0
timestep 0.005
thermo 100
thermo_style custom step temp pe ke etotal
thermo_modify norm yes
fix integrator all nve
run 100
write_restart middle.restart
clear
units lj
read_restart middle.restart
timestep 0.005
thermo 100
thermo_style custom step temp pe ke etotal
thermo_modify norm yes
fix integrator all nve
run 100
write_dump all custom restart-split.lammpstrj id type x y z vx vy vz modify sort id format float %.17g
```

Read the post-bath state, advance 100 steps, save and clear the system, restore it and advance 100 more steps. Total duration is one reduced time unit.

### Continuous-state comparison

```
units lj
read_restart equilibrated.restart
reset_timestep 0
timestep 0.005
thermo 100
thermo_style custom step temp pe ke etotal
thermo_modify norm yes
fix integrator all nve
run 200
write_dump all custom restart-continuous.lammpstrj id type x y z vx vy vz modify sort id format float %.17g
```

Advance 200 steps directly from the same origin and compare coordinates and velocities by particle ID. Final states retain 17 significant digits.

### Run both continuation paths

```
lmp -in restart-continuous.lmp
lmp -in restart-split.lmp
```

Place both inputs and equilibrated.restart in the same exercise directory. They write separate final states, aligned by ID for comparison.

A small continuation check starts both paths from one saved point. One path preserves the running state continuously; the other saves an intermediate state, clears the system, and reads that state back before continuing. Coordinates, velocities and energy are then compared at matching steps. With the same executable, processor arrangement and deterministic settings, this checks restoration of state. Changes that alter floating-point summation, including processor counts, can cause small differences that grow with time. Energy behaviour and statistics then complement coordinate comparisons rather than treating long-time divergence alone as a change of model.

### Compare restart endpoints by particle ID

```
#!/usr/bin/env python3
"""Compare the saved final states of a continuous and split NVE run.

python compare_restart.py restart-continuous.lammpstrj restart-split.lammpstrj
Requires NumPy. Atom IDs identify corresponding particles; row order may differ.
"""
from pathlib import Path
import argparse
import numpy as np


def final_frame(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    frames = []
    i = 0
    while i < len(lines):
        if lines[i] != "ITEM: TIMESTEP":
            raise ValueError("Expected a LAMMPS timestep header.")
        step = int(lines[i + 1])
        if lines[i + 2] != "ITEM: NUMBER OF ATOMS":
            raise ValueError("Expected an atom-count header.")
        count = int(lines[i + 3])
        if not lines[i + 4].startswith("ITEM: BOX BOUNDS"):
            raise ValueError("Expected box bounds.")
        bounds = np.asarray([[float(x) for x in line.split()]
                             for line in lines[i + 5:i + 8]])
        fields = lines[i + 8].split()[2:]
        if not lines[i + 8].startswith("ITEM: ATOMS "):
            raise ValueError("Expected atomic field names.")
        required = ["id", "type", "x", "y", "z", "vx", "vy", "vz"]
        if not all(name in fields for name in required):
            raise ValueError("Missing an identity, position, or velocity field.")
        rows = np.asarray([[float(x) for x in line.split()]
                           for line in lines[i + 9:i + 9 + count]])
        if rows.shape != (count, len(fields)) or not np.all(np.isfinite(rows)):
            raise ValueError("Incomplete or nonfinite atomic records.")
        selected = rows[:, [fields.index(name) for name in required]]
        selected = selected[np.argsort(selected[:, 0])]
        if len(np.unique(selected[:, 0])) != count:
            raise ValueError("Duplicate atom IDs.")
        frames.append((step, bounds, selected))
        i += 9 + count
    if not frames:
        raise ValueError("No frames found.")
    return frames[-1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("continuous", type=Path)
    parser.add_argument("split", type=Path)
    args = parser.parse_args()
    step_a, box_a, a = final_frame(args.continuous)
    step_b, box_b, b = final_frame(args.split)
    if step_a != step_b or a.shape != b.shape:
        raise ValueError("Final step or particle count differs.")
    if not np.array_equal(a[:, :2], b[:, :2]):
        raise ValueError("The atom IDs or their types differ.")
    if not np.array_equal(box_a, box_b):
        raise ValueError("The box bounds differ; inspect coordinate representations.")
    position = float(np.max(np.abs(a[:, 2:5] - b[:, 2:5])))
    velocity = float(np.max(np.abs(a[:, 5:8] - b[:, 5:8])))
    print(f"particles = {len(a)}; final step = {step_a}")
    print(f"maximum absolute saved coordinate difference = {position:.17g} [sigma_11]")
    print(f"maximum absolute saved velocity difference = {velocity:.17g} [sigma_11/tau]")


if __name__ == "__main__":
    main()
```

Run the command in the script header beside the two saved endpoint trajectories. Read positions and velocities by field name, match particles by ID, and report the maximum absolute component differences in reduced length and velocity units.

### Continuous and saved-state continuation compared

Same origin, deterministic NVE model and 0.005 time step over 200 steps; final coordinates and velocities are aligned by particle ID.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l02/en/#en-s7)

Compare 200 uninterrupted steps with 100 steps followed by writing and reading a binary restart and a further 100 steps. Position differences use minimum-image distances; velocity differences are lengths of three-dimensional difference vectors.

A Langevin bath adds another consideration: its random force is sampled over time, and its post-restart random history need not match an uninterrupted run step by step. Reusing the same seed is not the same as restoring a generator that has already advanced through part of its sequence. This is why the strict continuation comparison uses the NVE interval after bath removal. For a stochastic continuation, restore the physical state correctly and then examine the relevant distributions and statistics under an appropriate comparison rule.

The filename equilibrated is a convenient label; adequacy of equilibration is established through observables. Completing a prescribed bath interval records that preparation, while relaxation of slow structure must be assessed from subsequent behaviour. Here the name identifies the state saved at the end of the bath stage. Keeping this distinction becomes particularly important for long chains and networks, whose structural relaxation can be much slower than the adjustment of their instantaneous kinetic temperature.

## Organise records around a clear comparison

After the first analysis, change only the trajectory output interval while retaining the particles, force field, integration step and dynamical conditions. Compare file size and the detail visible in the path. Sparse output retains fewer instants but does not change the number of integration steps actually taken. Comparing this exercise with a change in integration time step separates the approximation of motion from the amount of recorded information. The next lesson examines time-step accuracy; here the distinction is established through the records.

Use one directory per comparison condition to keep each input with its outputs and reduce accidental overwriting or mismatching. A meaningful name can identify the changed temperature or time step, while a compact parameter record specifies software version, seeds, particle count, units, stages and analysis window. Names help locate files; contents establish what they describe. Labels such as final or second-run become ambiguous as comparisons expand. Organising by experimental condition scales more naturally to multiple chains or crosslink densities.

A file hash acts as a fingerprint derived from its contents. A changed file will generally have a different fingerprint, making hashes useful for checking whether the input used for analysis is the same file retained later. A hash does not establish physical correctness or explain parameter choices; it answers a specific content-identity question. Reliable analysis is built from checks with distinct purposes. Together, those checks preserve the connection among model definition, numerical calculation and presentation.

When a plot shows an unexpected jump, trace the data flow. Check whether coordinates are wrapped, then verify particle ID, frame time and box length. If energies differ by roughly the particle count, examine total versus per-particle normalisation. A sudden temperature change after continuation calls for checking velocity reassignment and temperature definitions. This approach links visual symptoms to the fields and operations that produced them. Regenerating the complete figure after a correction keeps its interpretation connected to the actual processing.

A simulation is now an interpretable chain: input defines a model and procedure, calculation records evolving states, analysis converts those records into defined observables, and figures make them comparable. The next lesson follows that chain further into the calculation itself: how potential energy produces force, how an integrator updates coordinates, and why the time step affects the energy trace. The files remain the carriers of that reasoning. Reading them makes numerical accuracy accessible to explicit comparisons rather than judging it from the smoothness of an animation.

## Further Reading and Open Materials

- [LAMMPS Tutorial 1: Lennard-Jones fluid](https://lammpstutorials.github.io/sphinx/build/html/tutorial1/lennard-jones-fluid.html) · Simon Gravelle; Cecilia M. S. Alvares; Jacob R. Gissinger; Axel Kohlmeyer · CC BY 4.0

  Upstream command sequence, monitoring, trajectories and continuation workflow.

  Added unit and file explanations, image flags, standalone analysis and a deterministic continuation comparison.
- [LAMMPS stable manual: dump](https://docs.lammps.org/stable/dump.html) · LAMMPS developers · Official documentation consulted; software source GPL-2.0; no copied figures

  Coordinate fields, image flags and particle identity.

  Original coordinate diagrams and analysis program.
- [LAMMPS stable manual: read_restart](https://docs.lammps.org/stable/read_restart.html) · LAMMPS developers · Official documentation consulted; no copied figures

  Saved state, settings that must be redefined, and stochastic-restart behaviour.

  Complete comparison organised around the same particle model.
- [Correlations in the Motion of Atoms in Liquid Argon](https://doi.org/10.1103/PhysRev.136.A405) · A. Rahman (1964) · Cited paper; no article text or images reproduced

  History of trajectory-based correlation and diffusion measurements.

  Original conceptual illustration, not a reconstruction of the paper’s data.
