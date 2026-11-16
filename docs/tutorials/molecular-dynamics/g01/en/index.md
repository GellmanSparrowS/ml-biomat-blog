# What Molecular Simulation Can Tell Us

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g01/en/
Language: en

Start with a box of water to understand how a model produces motion, how motion connects to measurable density, and how a curve answers a specific scientific question.

## Start with a glass of water and a question molecules can answer

Place a sugar cube in a glass of water. Its edges are clear at first, then the cube becomes smaller, and eventually the sweetness is no longer confined to the bottom of the glass. Everyday experience tells us that sugar dissolves, but it does not show how water molecules approach the crystal, which parts of a sugar molecule attract their attention, or how molecules move after leaving the crystal. Related questions appear in the water retention of contact lenses, the dispersion of a medicine in solution, and the stability of a protein. Molecular simulation turns a small region into a computational model, follows its particles for a specified time, and organizes their positions into quantities we can examine.

We begin with a simpler system than sugar solution: pure water. The aim is to understand a complete line of reasoning. What representation of water do we choose? What makes its molecules move? How can their changing arrangement produce a density? Under which conditions does that density apply? Water also prepares us for later examples, because proteins, nucleic acids, glycans, and polymers are often surrounded by it. Understanding the solvent helps explain a large fraction of the atoms in these systems. It also reveals why results may change when the solute is unchanged but the water model, salt concentration, or thermodynamic conditions differ.

Imagine a video of people crossing a sports field, recorded from above. The video contains many positions, but answering which exit becomes crowded requires additional choices: define the exit region, count the people passing through it, and specify the observation period. A molecular trajectory has the same relationship to a research question. The frames provide positions; the question determines the measurement. Density concerns mass within a volume. Diffusion concerns how far particles travel from earlier positions. Hydration concerns how water is arranged around another molecule. A single trajectory can support several measurements, each answering a different question.

Our example contains water represented by the SPC/E model. The initial simulation box is a cube with a side length of 3 nm; the construction step determines the actual number of molecules. The target temperature is 300 K and the target pressure is 1 bar. A nanometre, abbreviated nm, is one billionth of a metre. Kelvin, K, measures absolute temperature; 300 K is about 26.85 degrees Celsius. One bar is 100,000 pascals. We will examine preparation and observation stages together, reading temperature, volume, and density curves as related records. Their connection explains more than an isolated final number.

A real drop of water contains far more molecules than this small computational box. Every question therefore has a spatial and temporal scale. A short trajectory of our box is useful for learning about files, motion, density fluctuations, and analysis. Freezing, evaporation, chemical degradation, and rare structural changes require their own choices of model, boundary conditions, and sampling duration. Choosing these is rather like choosing a microscope's magnification and field of view: one determines which details can be resolved, while the other determines how many objects can be observed. The computational representation must suit the phenomenon being studied.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g01/en/#en-s1)

Figure 1 · Model, trajectory, measurement, and interpretation have distinct roles in the conceptual workflow.

## Turning invisible motion into a testable model of a liquid

A liquid can look smooth and quiet while its molecules remain in motion. A single drawing of their positions tells us little about which neighbours remain together and which exchange rapidly. An important step in early molecular dynamics was to connect such drawings through time. Computers advanced particles according to specified interactions, allowing researchers to ask whether one interaction model could account for both liquid structure and liquid motion. That question still guides force-field selection and validation. Producing a trajectory is one part of the work; connecting it to a measurable physical quantity is another.

In 1964, Aneesur Rahman studied a model of liquid argon containing 864 particles. Argon is a noble-gas element, so a particle could represent an atom without first introducing a complex network of chemical bonds. The model used a continuous Lennard–Jones interaction. Particle motion was connected to structural and dynamical measurements, including the distribution of neighbouring atoms and self-diffusion. The study illustrates the move from calculating many positions to organizing those positions into quantities that can be compared with experiment. Its material, temperature, and density were specified, giving the comparison a concrete physical setting. [Rahman, 1964](https://doi.org/10.1103/PhysRev.136.A405)

Argon's simplicity helps us understand the method, while water introduces additional needs. A water molecule contains one oxygen atom and two hydrogen atoms, with an uneven electronic charge distribution. Different parts of the molecule therefore interact differently with nearby charges. Water also has an orientation. Rotating two molecules can change their interaction even when the oxygen–oxygen distance stays the same. A water model must account for more than the positions of featureless spherical particles if it is to describe the directional organization associated with hydrogen bonding. This is why molecular identity matters before any trajectory is generated.

The SPC/E water model belongs to this development. In 1987, Berendsen, Grigera, and Straatsma examined effective pair potentials and the role of polarization-related energy in comparisons with thermodynamic quantities, leading to SPC/E as a development of SPC. The word “effective” matters. The calculation does not follow the electrons as they respond to every changing environment. Instead, selected fixed parameters incorporate some average effects. This makes simulations of many molecules over useful periods practical. It also gives the model a definite interpretation: its charges do not redistribute explicitly in response to the environment in each frame. [Berendsen and colleagues, 1987](https://doi.org/10.1021/j100308a038)

This history is connected by physical questions. A simple atomic liquid leads to questions about attraction, repulsion, and rearrangement. Water introduces molecular orientation and charge distribution. Further developments ask how the environment changes that distribution. When we use an established model, the same sequence of questions remains helpful. What counts as a particle? Which properties are assigned to it? Which changes are generated during the simulation, and which have already been represented by fixed parameters? We will return to these questions when discussing protein charges, glycan conformations, and polymer hydration.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g01/en/#en-s2)

Figure 2 · Liquid-argon models connect atomic motion with structure and diffusion; three-site water models introduce molecular orientation and charge distribution.

## What the computational box of water actually contains

Think of preparing a molecular model as assembling three complementary sheets of information. The first says where the atoms are now: the coordinates. The second says what they are and how they interact: the topology and force field. The third says how this particular observation will be performed: the run parameters. An oxygen coordinate identifies a location, but it does not determine the atom's charge. A parameter file can request 300 K, but it cannot supply missing water molecules. These pieces must agree before the software can calculate what happens next.

In this setting, topology mainly describes molecular identity and connectivity: which atoms belong to the same molecule, which are connected, and which interaction parameters apply. Road connections on a map provide a useful analogy. The road network and the current positions of cars are separate kinds of information. Water coordinates change during the simulation while the molecular connectivity remains fixed. Our classical model can therefore follow translation, rotation, and molecular arrangements. Water dissociation or proton transfer would bring changing connectivity and electronic states into the research question, calling for an appropriate reactive or electronic-structure treatment.

SPC/E represents one water molecule with three interaction sites, located on oxygen and the two hydrogens. Each site has a mass and a partial charge; the oxygen site also carries the model's Lennard–Jones nonbonded interaction. Partial charges describe an uneven charge distribution within an overall neutral molecule. They do not make each water molecule an ion. The two positive hydrogen charges and the negative oxygen charge sum to zero. Their arrangement nevertheless creates directional interactions with charged or polar groups. This provides a route to understanding why water surrounds ions and forms structured layers near hydrophilic surfaces.

In our dynamics settings, the internal geometry of a water molecule is constrained, giving a rigid molecule that can still translate and rotate. Imagine a small rigid frame: you can move and turn the whole frame while the distances defining its shape remain fixed. Removing rapid internal vibrations permits a larger integration time step than would otherwise be appropriate. It also identifies the motions represented in the trajectory. These water molecules do not have independent bond-stretching vibrations, so the trajectory is not a direct representation of the complete vibrational spectrum of real water. Initial minimization first uses the supplied flexible bond and angle definitions to relax geometry before rigid-water dynamics begins; this preparation is not interpreted as physical time evolution.

It is also useful to separate the coordinates used to build the initial box from the water model selected for the calculation. The GROMACS file spc216.gro supplies starting coordinates suitable for three-site water models. The spce.itp topology included in this example specifies SPC/E interactions. The letters “spc” in the coordinate filename do not override that topology choice. A floor plan can provide an initial arrangement for rooms whose functions are assigned later; similarly, starting positions and interaction definitions play different roles. Minimization and equilibration allow the initial arrangement to adapt to the selected model and conditions.

The box uses periodic boundary conditions. A molecule leaving through one side has a periodic image at the opposite side, and neighbouring images are considered according to the periodic interaction rules. Repeating tiles help visualize this construction, but the copies are not independent new samples: they all represent the same basic box, with corresponding motion. Periodicity lets us study bulk water without introducing a free surface. It also introduces finite-size and repetition effects. Box dimensions, interaction cutoffs, and the treatment of long-range electrostatics must be chosen together, a connection developed in later lessons.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g01/en/#en-s3)

Figure 3 · SPC/E partial charges follow spce.itp in GROMACS 2026.4 and are expressed in elementary charge e. Spheres do not show actual electron-cloud boundaries. The periodic sketch is a two-dimensional section of a three-dimensionally periodic box.

## Why the next position can be calculated

To predict a particle's position a moment later, we need its current position, velocity, and the force acting on it. Pushing an empty shopping trolley and a loaded one with the same force produces different changes in velocity. A larger mass gives a smaller acceleration under the same force. Newton's relationship used in molecular dynamics has this familiar structure, with the trolley replaced by a model particle and the force obtained from the chosen interactions. Understanding this relationship gives the many simulation settings a physical context.

How force changes the motion of a particleEq. 1

![How force changes the motion of a particle](https://ml-biomat.com/static/agent-math/853ef63f52b532f6977494a6.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| i | Particle index identifying the particle, not a multiplier | dimensionless |
| Fᵢ | Net force vector on particle i; bold type denotes direction | newton, N = kg m s⁻² |
| mᵢ | Mass of particle i | kilogram, kg |
| aᵢ | Acceleration vector of particle i: change in velocity per unit time | metres per second squared, m s⁻² |
| =, × | Equality relates both sides; multiplying mass by acceleration applies to each of the three vector components | operators have no units |

Reading the relationshipMass measures inertia. A larger mass has a smaller acceleration under the same net force. Applying the relation to each particle connects interactions to changes in motion.

A worked exampleFor an illustrative particle of mass 3.0×10⁻²⁶ kg under an x-directed force of 6.0×10⁻¹² N, dividing force by mass gives an x acceleration of 2.0×10¹⁴ m s⁻². Very small molecular masses can produce large numerical accelerations. These values illustrate the calculation; they are not measurements from the water run.

ConditionsThis is classical particle dynamics. With constraints, the net force includes the effect required to preserve the constrained geometry. Thermostats and barostats alter motion or box evolution, so conservation properties depend on the stage.

A vector represents a quantity with both magnitude and direction. Pushing east and pushing north can involve equally strong forces but produce different position changes. Three components describe these directions in a three-dimensional simulation box. Acceleration describes how velocity changes with time; velocity describes how position changes. During each short interval, the program calculates forces and advances the motion using an integration algorithm. At this stage, integration can be understood as joining many small changes into a longer trajectory. A full course in calculus is not required to understand why the steps must be small.

The forces come from a model that assigns potential energies to molecular arrangements. Bringing two like magnetic poles closer requires effort, providing an everyday illustration of a relationship between arrangement, energy, and force. Molecular force fields use mathematical expressions for repulsion, dispersion, electrostatics, and other interactions. Together they specify how energy changes when positions change. The program uses this variation to calculate forces. Lower-energy arrangements are often visited more readily, but thermal motion continually carries the system between configurations. A liquid at thermal equilibrium does not place every molecule at one motionless minimum.

The time step is the physical interval advanced in each update. Our dynamics use 0.002 ps, or 2 fs. A picosecond is one trillionth of a second, and a femtosecond is one quadrillionth of a second. This physical time differs from the time the computer spends running. Ten minutes of computing may correspond to tens or hundreds of simulated picoseconds, depending on the system, hardware, and settings. Time axes in molecular plots must use the simulated physical time rather than the duration measured by the operating system.

Convert integration steps into physical timeEq. 2

![Convert integration steps into physical time](https://ml-biomat.com/static/agent-math/133b8e3a1a3c1adeaeaa8352.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| tₛᵢₘ | Physical duration covered by the run | picosecond, ps |
| Nₛₜₑₚ | Number of integration steps, a nonnegative integer | dimensionless |
| Δt | Time advanced per integration step; Δ denotes an increment | picosecond, ps |
| =, × | Multiply the step count by duration per step to obtain total duration | operators have no units |

Reading the relationshipFor a constant time step, advancing N times adds the same interval N times, which is multiplication.

A worked exampleAn NVT run of 10,000 steps at 0.002 ps per step covers 20 ps. A 100 ps NVE run needs 50,000 steps at 2 fs or 100,000 steps at 1 fs.

ConditionsThis assumes a constant time step and gives a duration, excluding any initial time offset. It is not wall-clock computing time. Read recorded times when stages are joined.

A larger time step covers the same physical duration with fewer updates. That seems attractive until particles move across important changes in force between updates, making the numerical approximation less accurate. Reconstructing a rapidly moving hand from widely spaced photographs presents a similar problem: important motion occurs between the recorded positions. Constraining rapid internal vibrations helps make a 2 fs step practical here. The suitable step still depends on the model, temperature, constraint accuracy, and numerical method. In the fourth lesson we will examine energy changes from a common initial state to evaluate this choice.

The program does not need to save a picture at every integration step. Motion can be updated frequently while coordinates are written less frequently to keep the output manageable. Saving every 500 steps at 2 fs per step gives one frame every 1 ps. Those frames can describe slower movements, while faster events between frames may be missed. Total simulated duration, integration time step, and trajectory saving interval are therefore three separate settings. Each answers a different question about what the calculation covers and what information remains available afterwards.

## How density connects molecular motion to an everyday measurement

Density makes a useful first measurement. Fill two identical measuring cups with water and cooking oil and weigh their contents. Different masses in the same volume indicate different densities. The simulation uses the same idea: divide total mass by box volume. The mass follows from the number of molecules and the mass of each molecule. Volume follows from the box dimensions and can change during pressure control. We do not assign a separate desired density to every molecule. A measurable density emerges from their collective arrangement under the interactions and external conditions.

Calculate density from molecule count and box dimensionsEq. 3

![Calculate density from molecule count and box dimensions](https://ml-biomat.com/static/agent-math/ebf7b509d88b138b00b1accd.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ρ | Mass density, Greek letter rho | kg m⁻³ |
| m | Total mass of water in the box | kg |
| V | Box volume | m³ |
| Nw | Number of water molecules | dimensionless |
| Mw | Molar mass of water, taken as 0.01801528 for the illustration | kg mol⁻¹ |
| NA | Avogadro constant, 6.02214076×10²³, the number of particles per mole | mol⁻¹ |
| L | Side length of a cubic box | m; multiply an input in nm by 10⁻⁹ first |
| /, ³, =, × | The fraction bar denotes division; the cube multiplies three side lengths; equality connects equivalent forms; adjacent factors multiply | operators have no units |

Reading the relationshipDivide molar mass by molecules per mole to obtain molecular mass, multiply by the molecule count, and divide by volume. A cube has a volume equal to the third power of its side length.

A worked exampleGeometric illustration: 900 water molecules in a 3.000 nm cube give approximately 997.17 kg m⁻³. Increasing the side length by 10% multiplies volume by 1.1³ = 1.331 and density by approximately 0.7513. The count of 900 is specified for this illustration; the actual simulation count comes from box construction.

ConditionsThis form assumes pure water and a cubic box. Sum component masses for a mixture and use the full box vectors for noncubic cells. Exact reproduction of simulated density uses the atom masses in the topology.

This expression joins several scales. Chemistry uses the mole to count large numbers of particles, rather as a dozen counts twelve objects, although the number in a mole is vastly larger. Water's molar mass of approximately 18.01528 g/mol means that one mole of water molecules has approximately that mass. Dividing by Avogadro's constant gives a molecular mass; multiplying by the number of molecules gives the mass in our box. When converting a volume measured in cubic nanometres to cubic metres, the length conversion must be applied three times. Following the units through each step makes the calculation inspectable.

During the constant-temperature, constant-pressure stage, the molecule count remains unchanged while the box volume can vary. Contraction places the same mass in less space and raises the density. Expansion lowers it. The molecules have not become heavier or lighter: the denominator has changed. The interactive example below fixes the molecule count and allows the side length of a cubic box to change. It calculates the geometric mass-to-volume relationship rather than integrating molecular motion. This provides a simple intuition that can then be compared with the actual trajectory.

Geometric illustration: calculate mass density from the molecule count, molar mass, and cubic box volume.

[Figure: Cubic-box geometric illustration and density readout](https://ml-biomat.com/tutorials/molecular-dynamics/g01/en/#en-s5)

Adjust molecule count and box size to see how mass and volume determine density.

Temperature and pressure also require a statistical interpretation. An individual atom does not have a stable private temperature resembling a thermometer reading. System temperature relates the kinetic energy of many degrees of freedom to a thermodynamic description. Pressure involves particle motion and the response of interactions to volume. In a small box, instantaneous pressure can fluctuate strongly. Setting a target of 1 bar does not require every saved measurement to equal 1.000 bar. We examine the distribution, average behaviour, and any sustained drift over an appropriate observation window.

Preparation begins with minimization to relieve unsuitable close contacts. Temperature control at fixed volume then allows motion to adjust to the target conditions, followed by pressure control so the box dimensions can respond. NVT denotes fixed particle number, volume, and temperature conditions; NPT denotes fixed particle number, pressure, and temperature conditions. Controlled temperature and pressure refer to statistical conditions and targets, while instantaneous measurements still fluctuate. A separate NVE stage fixes particle number and volume and removes temperature and pressure coupling to examine approximately isolated dynamics. Its constant box density is a consequence of fixed volume, not evidence that pressure equilibration was sufficient.

Selecting the single density value closest to experiment would produce an attractive number while discarding the rest of the record. A more informative approach is to inspect the complete trace, specify an observation window, and describe both its centre and its fluctuations. In this introductory analysis, the second half of the NPT record is a clearly defined, reproducible window. We compare the original trace, a cumulative average, and a distribution. This rule explains where the statistics come from. Assessing equilibration more fully also requires longer observations, independent repetitions, and attention to correlation times, which will be developed in the ninth lesson.

## Turn the recorded data into a figure you can explain

GROMACS writes energies and thermodynamic quantities to an edr file. This binary record is designed for software to read, rather than for direct reading as ordinary text. The gmx energy tool extracts selected quantities into an xvg text file. Lines beginning with a hash sign or @ usually contain comments, titles, axes, and series labels. Other lines hold numerical values. We select Density, Volume, and Temperature to obtain time and three observables. The output may arrange columns according to its internal numbering, so the analysis reads the actual series labels instead of assuming that typing names in a particular order determines their output order.

Run the following command in the directory containing this lesson's water results. A command line is a text interface for asking a program to perform a task. Here, gmx is the program entry point, energy selects the tool, -f identifies the input file, and -o identifies the output file. The pipe sends text produced by the first command into the second, supplying the quantity names that would otherwise be typed interactively. The final zero ends the selection. This extracts recorded information; it does not change the simulation conditions or regenerate molecular motion.

### Extract three observables from the NPT energy file

```
#!/usr/bin/env bash
set -euo pipefail
printf 'Density\nVolume\nTemperature\n0\n' | gmx energy \
  -f npt.edr -o npt-density-volume-temperature.xvg
```

Run in the example result directory containing npt.edr. The XVG @ sN legend entries identify the actual data columns; the following program looks them up by name.

The complete Python program below reads valid data, selects the second half of the recorded time interval, and creates a figure preserving both raw variation and statistical summaries. Python is a programming language useful for writing analysis steps that can be repeated. NumPy handles numerical arrays, and Matplotlib produces the plots. An array can initially be understood as an ordered collection of numbers. Taking the cumulative sum of density values and dividing by the number included so far shows how the running average changes as more of the observation is considered.

The output table records the sample count, time range, mean, and sample standard deviation. Standard deviation describes how widely values in this window are spread. It is different from uncertainty in the estimated mean. Consecutive frames come from continuous motion and are often correlated; treating them as independent experiments would underestimate the uncertainty of an average. We therefore display variation directly and retain time order. If the trace drifts slowly, longer observation or a preparation check is more useful than smoothing the drift out of sight.

### Complete Python analysis: time traces, distributions, and the observation window

```
#!/usr/bin/env python3
"""Analyze the recorded NPT water box and plot its thermodynamic observables.

From a directory containing this script and the exported XVG:
    python analyze_water.py npt-density-volume-temperature.xvg --output figures

Dependencies: numpy, matplotlib. The output window is the second half in time.
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


def read_xvg(path: Path) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    legends: dict[int, str] = {}
    rows: list[list[float]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("@"):
            match = re.match(r'@\s+s(\d+)\s+legend\s+"([^"]+)"', line)
            if match:
                legends[int(match[1])] = match[2]
            continue
        if line.startswith("#"):
            continue
        if line == "&":
            raise ValueError("Expected one XVG dataset, found a dataset separator.")
        rows.append([float(value) for value in line.split()])
    if len(rows) < 4:
        raise ValueError("At least four saved samples are required.")
    if len({len(row) for row in rows}) != 1:
        raise ValueError("The number of columns changes inside the XVG file.")
    values = np.asarray(rows, dtype=float)
    if not np.all(np.isfinite(values)):
        raise ValueError("The data contain a nonfinite value.")
    time_ps = values[:, 0]
    if not np.all(np.diff(time_ps) > 0):
        raise ValueError("Saved times must increase strictly.")
    columns: dict[str, np.ndarray] = {}
    for index, label in legends.items():
        if index + 1 >= values.shape[1]:
            raise ValueError(f"Legend {label!r} refers to a missing column.")
        key = re.sub(r"[^a-z]", "", label.casefold())
        if key in columns:
            raise ValueError(f"Duplicate series label: {label}")
        columns[key] = values[:, index + 1]
    for key in ("density", "volume", "temperature"):
        if key not in columns:
            raise ValueError(f"Required XVG legend missing: {key}")
    if np.any(columns["volume"] <= 0) or np.any(columns["density"] <= 0):
        raise ValueError("Volume and density must be positive.")
    return time_ps, columns


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xvg", type=Path)
    parser.add_argument("--output", type=Path, default=Path("figures"))
    parser.add_argument("--language", choices=("zh", "en"), default="en")
    args = parser.parse_args()
    time_ps, data = read_xvg(args.xvg)
    start = time_ps[0] + 0.5 * (time_ps[-1] - time_ps[0])
    selected = time_ps >= start
    n = int(selected.sum())
    if n < 2:
        raise ValueError("The observation window contains fewer than two samples.")
    args.output.mkdir(parents=True, exist_ok=True)
    units = {"density": "kg/m^3", "volume": "nm^3", "temperature": "K"}
    stats = []
    for quantity in ("density", "volume", "temperature"):
        y = data[quantity][selected]
        stats.append({
            "quantity": quantity, "unit": units[quantity],
            "samples": n, "start_ps": float(time_ps[selected][0]),
            "end_ps": float(time_ps[selected][-1]),
            "mean": float(np.mean(y)),
            "sample_standard_deviation": float(np.std(y, ddof=1)),
        })
    with (args.output / "water_summary.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(stats[0]))
        writer.writeheader()
        writer.writerows(stats)
    report = {
        "input": args.xvg.name,
        "window_rule": "second half of the recorded physical-time interval",
        "spread_definition": "sample standard deviation; not uncertainty of the mean",
        "series": stats,
    }
    (args.output / "water_summary.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )

    zh = args.language == "zh"
    label = lambda chinese, english: chinese if zh else english
    plt.rcParams.update({
        "font.family": ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else "DejaVu Sans",
        "font.size": 14,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.labelcolor": "#173534", "text.color": "#173534",
        "axes.edgecolor": "#75918c", "svg.fonttype": "path",
        "figure.facecolor": "#faf9f4", "axes.facecolor": "#faf9f4",
        "savefig.facecolor": "#faf9f4",
    })
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
    panels = [(axes[0, 0], "density", label("密度 / kg m⁻³", "Density / kg m⁻³")),
              (axes[0, 1], "volume", label("体积 / nm³", "Volume / nm³")),
              (axes[1, 0], "temperature", label("温度 / K", "Temperature / K"))]
    for axis, key, ylabel in panels:
        axis.axvspan(time_ps[selected][0], time_ps[-1], color="#dbe9e0", alpha=0.6)
        axis.plot(time_ps, data[key], color="#598a89", lw=0.7, alpha=0.7,
                  label=label("逐帧记录", "Recorded samples"))
        running = np.cumsum(data[key][selected]) / np.arange(1, n + 1)
        axis.plot(time_ps[selected], running, color="#994b2a", lw=2.0,
                  label=label("窗口内累积均值", "Window cumulative mean"))
        axis.set(xlabel=label("物理时间 / ps", "Physical time / ps"), ylabel=ylabel)
        axis.grid(axis="y", color="#c9d7cf", linewidth=0.5)
    axes[0, 0].legend(frameon=False, fontsize=11, loc="best")
    axis = axes[1, 1]
    density = data["density"][selected]
    axis.hist(density, bins="fd", density=True, color="#4f8980",
              edgecolor="#faf9f4", linewidth=1.0)
    axis.axvline(np.mean(density), color="#994b2a", lw=2,
                 label=label("窗口均值", "Window mean"))
    axis.set(xlabel=label("密度 / kg m⁻³", "Density / kg m⁻³"),
             ylabel=label("概率密度 / m³ kg⁻¹", "Probability density / m³ kg⁻¹"))
    axis.legend(frameon=False, fontsize=11)
    fig.suptitle(label("SPC/E 水：NPT 阶段的实际记录", "SPC/E water: the recorded NPT window"), fontsize=19)
    for panel_label, axis in zip("ABCD", axes.flat):
        axis.set_title(panel_label, loc="left", fontweight="bold", pad=9)
    fig.savefig(args.output / "water_observables.svg")
    fig.savefig(args.output / "water_observables.png", dpi=180)
    plt.close(fig)
    for row in stats:
        print(f"{row['quantity']}: mean={row['mean']:.6g} {row['unit']}; "
              f"sample SD={row['sample_standard_deviation']:.6g}; "
              f"n={row['samples']}; "
              f"window={row['start_ps']:g}–{row['end_ps']:g} ps")


if __name__ == "__main__":
    main()
```

With NumPy and Matplotlib installed, run the command in the script header. The script creates SVG, PNG, CSV, and JSON outputs from the recorded GROMACS data. Shading identifies the second half of the record, and the stronger line is its cumulative mean. Reported standard deviations describe fluctuations.

A useful time plot identifies physical time and its units on the horizontal axis, and the measured quantity on the vertical axis. The density panel keeps a thin line for the raw record and uses a stronger line for the selected window's cumulative average. A distribution panel shows where values from that same window lie. A histogram groups continuous values into intervals; a taller bin indicates more observations there. We normalize it as a probability density, so the combined bar area is one and the vertical units are the inverse of the density units. It describes measured box densities, not the spatial arrangement of water molecules.

### Density, volume, and temperature in the NPT water box

Generated by G01/analyze_water.py from the actual legends in npt-density-volume-temperature.xvg. The figure retains the complete record and marks its second-half window. The table identifies the time range, means, and sample standard deviations; these spreads are not confidence intervals for the means.

GROMACS 2026.4; 884 SPC/E waters in an initially 3 nm cubic box, with targets of 300 K and 1 bar. The NPT record spans 100 ps and descriptive statistics use 50–100 ps; the player shows a separate 100 ps NVE stage.

[Download reference data and complete inputs (ZIP) 1.82 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-water-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g01/en/#en-s6)

Actual NPT record. Shading marks the second half, 50–100 ps. Thin lines retain saved samples; dark lines show cumulative means starting at 50 ps. The histogram is normalized to probability density using the density samples in that window.

| Quantity | Value | Unit |
| --- | --- | --- |
| Density window mean | 997.8 | kg m⁻³ |
| Density sample standard deviation | 11.26 | kg m⁻³ |
| Volume window mean | 26.51 | nm³ |
| Volume sample standard deviation | 0.2976 | nm³ |
| Temperature window mean | 300.9 | K |
| Temperature sample standard deviation | 5.612 | K |

The 50–100 ps window contains 251 recorded samples, with a mean density of 997.83 kg m⁻³ and a sample standard deviation of 11.26 kg m⁻³. Mean volume is 26.506 nm³. When volume rises, density falls because the box still contains the same 884 water molecules. Mean temperature is 300.86 K, fluctuating around the 300 K target. Density variations persist across several picoseconds, so neighbouring records share information from the same motion: 251 samples are not 251 independent experiments. These numbers describe this model and window and provide a starting point for longer sampling and repeated comparisons.

Read these panels together. First examine whether temperature fluctuates around the intended range. Then check the opposite responses of volume and density. Finally consider whether the average within the selected window continues to move systematically. Every plotted value should connect to a defined input, stage, and time interval. A new water model or control setting requires a new simulation and analysis of its records. The same analysis program lets us compare those datasets using consistent measurement definitions.

## What an animation shows, and what statistics add

In an animated water trajectory, translation and rotation are immediately visible. Sphere sizes and colours are display choices: a larger oxygen sphere and smaller hydrogen spheres help identify molecules, but do not show the full electronic clouds. Thin connecting rods also help identify molecular connectivity. A useful visualization includes the box extent, physical time, and representation so that the viewer can interpret what moves and over what distance. Colour and smooth motion alone cannot establish a molecular scale.

Periodicity can produce an apparent visual puzzle. If atoms are individually wrapped into the box, an oxygen may appear near the right face while one of its hydrogens appears near the left face. Drawing a line between those coordinates creates an apparently enormous bond. This is a coordinate-representation issue rather than a stretched chemical bond. Reconstructing whole molecules and centring them can improve viewing. Diffusion analysis, however, needs continuous displacement across boundary crossings. Coordinate processing should therefore suit its purpose: an attractive wrapped display and a displacement analysis may require different representations of the same trajectory.

### Water translation, rotation, and periodic representation

Taken from the nve-2fs trajectory of the same SPC/E box. Physical time, box extent, and the periodic representation of whole molecules are shown. Playback, pause, and frame controls help distinguish motion from boundary representation.

Seeing two molecules approach one another establishes an arrangement at that moment. Saying that water occurs more often at a particular distance requires statistics over many reference molecules and many times. Saying that molecular motion is faster requires a definition of displacement over time and a comparison with other conditions. Such measurements combine many frames to identify recurring behaviour. They retain a connection to microscopic motion while preventing one visually striking segment from carrying an entire scientific claim.

Two trajectories may look similar while having different densities. Conversely, similar average densities can accompany different local orientations or diffusion. Density compresses a great deal of information into one number. Two classrooms can contain the same number of people per square metre while differing in furniture layout, movement, and opportunities for interaction. Density is consequently one useful model test alongside quantities such as radial distributions, diffusion, dielectric response, and other thermodynamic properties. The research question should determine which measurements matter.

This choice becomes particularly useful in biomaterials. A coating's hydration layer may call for measurements of local water occupancy, residence behaviour, and orientation. A polymer's extension in water may require both chain dimensions and chain–water contacts. Protein conformational analysis must separate overall translation and rotation from internal structural changes. The same approach—define the objects, follow their motion, and calculate the relevant observable—continues through those topics. The water box is simple enough to make the reasoning visible while supporting meaningful checks.

## Turn curiosity into a calculable research question

“Is this a good material?” combines many different judgments and does not directly specify a molecular dynamics calculation. We can narrow it to a concrete comparison: at the same temperature, salt concentration, and chain length, do two surface chemistries produce different water distributions near the surface? Composition, controlled conditions, and measurement now have defined roles. Experiments and larger-scale descriptions connect these molecular observations to macroscopic performance. The simulation contributes a traceable relationship between structure and motion within that wider investigation.

Writing one complete question before building the system is helpful. For example: “How does density fluctuate in the second half of the NPT record for a periodic SPC/E water box at 300 K and 1 bar?” This identifies the object, model, conditions, stage, observation window, and observable. Replacing “density” with “freezing rate” changes the task substantially. Nucleation, supercooling, system size, and longer sampling become part of the design. The model and protocol must follow the revised physical question, rather than simply repeating the same calculation more often.

Comparisons also require choices about what stays the same. Changing temperature, water model, box size, and analysis window together makes the reasons for a curve's movement difficult to separate. An initial study can hold other choices fixed while changing the factor directly relevant to the question, then use repeated simulations to assess variation. Our later time-step comparison will keep the initial state and physical observation duration aligned as closely as possible. The PEG chain-length study will retain consistent chemical and solvent definitions so that chain length remains the central comparison.

Return to the glass of sugar solution. Molecular simulation can turn everyday observations into local, measurable questions: where water spends time, how a molecule turns, how long a contact persists, or over what range a chain changes shape. Each question needs a suitable representation and a way to summarize the trajectory. Next we will open the coordinate, topology, and parameter files that define the water box, understand how they fit together, and then use them to start its motion.

## Further Reading and Open Materials

- [GROMACS tutorial 1: Water](https://gaseri.org/en/tutorials/gromacs/1-tip4pew-water/) · Wes Barnett; Vedran Miletić · CC BY-SA 4.0 (English tutorials)

  Adapted workflow for constructing a water box, staged equilibration, and density measurement.

  Uses SPC/E, an initial 3 nm cube, 300 K and 1 bar; updates coupling and adds NVE checks. Explanations, diagrams, interaction, and statistical analysis were newly written. Adapted workflow material retains CC BY-SA 4.0.
- [GROMACS 2026.4: Water solvation](https://manual.gromacs.org/2026.4/how-to/topology.html#water-solvation) · GROMACS developers · Consult GROMACS documentation distribution license

  Technical reference for three-site water coordinates and topology selection.

  Independent explanation of coordinates versus model parameters.
- [Correlations in the Motion of Atoms in Liquid Argon](https://doi.org/10.1103/PhysRev.136.A405) · A. Rahman · Publisher copyright; bibliographic and factual citation

  History of the 1964 liquid-argon simulation and measurable observables.

  The historical mechanism diagram is original; no paper figure or dataset is reproduced.
- [The missing term in effective pair potentials](https://doi.org/10.1021/j100308a038) · H. J. C. Berendsen; J. R. Grigera; T. P. Straatsma · Publisher copyright; bibliographic and factual citation

  Historical context for SPC/E effective interactions and polarization energy.

  Independent explanation and original three-site water schematic.
