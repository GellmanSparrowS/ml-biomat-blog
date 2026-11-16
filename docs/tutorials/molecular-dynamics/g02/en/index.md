# From Files to Trajectories: Preparing a Simulation

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g02/en/
Language: en

Open the water box coordinates, topology, and parameters, understand how they define a run, and inspect molecular identities, site counts, and box geometry with a complete program.

## Make a calculation understandable on another computer

When making coffee, the amount of water, amount of coffee, water temperature, and brewing time all affect the result. A photograph of the finished cup does not provide enough information to reproduce its flavour. Recording the conditions makes it possible to change one of them deliberately. Molecular simulation needs a similar kind of preparation. An attractive animation does not immediately reveal the water model, box size, interactions, or physical interval between frames. Those details are stored in different files. Understanding their roles means understanding how a calculation is defined.

We continue with the SPC/E water box from the previous lesson. Instead of introducing every force equation at once, we follow the path from input files to trajectories. By the end, you should be able to distinguish coordinates, topology, and run parameters, check that the water count agrees with the atom count, and identify which outputs support restarting, viewing motion, or plotting temperature and density. These skills transfer directly to proteins and polymers because more complicated systems still separate the same kinds of information.

Example filenames follow a simple convention. The part before the dot identifies the stage, while the extension identifies a common format. Thus npt.gro holds coordinates associated with the NPT stage, and npt.edr holds its energy and thermodynamic records. Extensions are conventions; the actual contents determine what a file means. Renaming a photograph as a spreadsheet does not turn it into numerical data. Similarly, renaming an old input does not change its temperature or molecular model. Clear names support reading, while inspecting contents establishes meaning.

The example uses GROMACS 2026.4. Recording the version fixes the context for command behaviour, defaults, and input interpretation. The execution environment also affects speed, available devices, and numerical details, so the example preserves engine and run information. When following it on another computer, first inspect the reported version and consult its matching documentation. Microscopic trajectories can progressively diverge between runs or machines. The comparison concerns the statistical behaviour of the same model and protocol, supported by enough recorded information to investigate differences.

The commands use Bash-style shell syntax. They can run in an appropriate Linux or macOS environment, or a local Linux environment on Windows. The terminal is a text interface that passes instructions to programs; GROMACS performs the molecular calculation. We introduce the few shell conventions needed repeatedly and connect every command to a specific change in files. This makes a command an understandable description of inputs, an action, and outputs, rather than a line that must be memorized without explanation.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g02/en/#en-s1)

Figure 1 · Three inputs describe geometry, model, and observation, then grompp assembles a TPR. Arrows indicate information flow, not physical time.

## Why science needs exchangeable atomic coordinates

The three-dimensional shape of a biological molecule is established through a relationship between experimental information and a structural model. Diffraction, nuclear magnetic resonance, and cryogenic electron microscopy provide different kinds of evidence, from which researchers construct models that account for the data. A model can be drawn as a protein image or stored as atomic coordinates. Images help people recognize an overall shape. Coordinates let other researchers recalculate distances, compare structures, inspect local environments, and ask new questions about the same object. Exchangeable numerical records connect these activities.

The Protein Data Bank, or PDB, was established in 1971 with seven structures. Its beginning illustrates that sharing a structure involves more than displaying a picture. Preserving atomic positions and associated information lets different laboratories inspect, analyse, and reuse the same model. As structures became more numerous and complex, formats and data conventions developed with them. Opening a downloaded structure immediately in a molecular viewer relies on this accumulated agreement about how structural information is represented. [PDB history](https://www.rcsb.org/pages/about-us/history)

A coordinate record can be understood as a spatial address book. Each entry identifies an atom and gives its position relative to a chosen coordinate system. Rotating the entire molecule changes those coordinate values without changing internal distances. A viewer can freely alter the viewing direction, while an analysis must decide which measurements should be unaffected by overall translation or rotation. That distinction becomes important when comparing protein conformations. A molecule pointing in a different direction on the screen has not necessarily changed its internal shape.

An experimental structure does not contain all the conditions needed for a molecular simulation. Some hydrogens may not be explicitly located in the deposited model. Protonation states must be considered in the intended environment, and missing segments or crystallographic waters need appropriate treatment. The fifth lesson examines those choices. Pure water avoids much of this structural-preparation complexity, allowing us to learn the file relationships first: coordinates supply starting geometry, the force field supplies interactions, and run parameters determine how motion is advanced and observed.

This separation also makes changes easier to explain. Extending an observation from one hundred to two hundred picoseconds mainly concerns run settings and continuation state. Changing the water model requires checking interaction sites, topology, and compatible parameters. Adding a protein changes both coordinates and the molecular inventory. Each scientific operation acts on a particular kind of information. File formats may appear technical, but they carry the meaning of exactly which part of the physical model an operation changes.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g02/en/#en-s2)

Figure 2 · The PDB began sharing seven structures in 1971. Coordinate records support reanalysis; molecular simulation additionally needs interactions and run conditions. The circles represent structure records.

## Read a coordinate line: identity, position, and length units

The example's water.gro is a text coordinate file. Its first line gives a description, the second gives the atom count, the following lines describe individual atoms, and the final line gives the box. Standard-precision GRO atom records use fixed-width fields for residue number, residue name, atom name, atom number, and three coordinates. Fixed width means that fields can touch without a separating space. A reader cannot always assume that splitting a line wherever it finds whitespace will recover all the fields correctly.

In proteins, a residue usually identifies an amino-acid unit. In the water file, a residue record also organizes the three atoms of each water molecule. SOL is the water residue name, while OW, HW1, and HW2 identify its oxygen and hydrogens. Numbers help locate an entry; names help identify it. The atom type used for interactions belongs to the topology and is a separate concept from the displayed atom name. Naming an atom OW does not automatically assign the correct charge. Coordinate order must still match the corresponding topology order.

The three coordinates, usually called x, y, and z, describe distances along three perpendicular directions from an origin. A position written as 0.500, 1.000, and 1.500 gives those three distances in the GRO length unit, nanometres. A negative coordinate, or a coordinate beyond a box face, is not automatically wrong. Periodic systems can represent equivalent positions in different images. Geometry must therefore be interpreted together with the box vectors and periodic rules, rather than by requiring every value to fall inside an aesthetically tidy interval.

Length units deserve attention on the first reading. GRO coordinates use nanometres, while traditional PDB coordinates use ångströms, written Å; 1 nm equals 10 Å. Interpreting a structure that is 30 Å long as 30 nm would enlarge its length tenfold and its volume a thousandfold. Format-aware conversion tools normally handle this distinction. Use a tool that understands both formats and check the resulting dimensions, rather than multiplying every number manually and then passing it to a converter that performs the conversion again.

Two units for the same lengthEq. 1

![Two units for the same length](https://ml-biomat.com/static/agent-math/553e7ab04459713db651b865.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| nm | Nanometre, one billionth of a metre | unit of length |
| Å | Ångström, one ten-billionth of a metre | unit of length |
| 1, 10, = | Numbers count units; the equality identifies the same physical length on both sides | numbers and equality have no units |

Reading the relationshipA nanometre contains ten ångströms. Changing the unit changes the numerical value while preserving the physical distance.

A worked exampleA side length of 3 nm is 30 Å; a coordinate of 0.500 nm is 5.00 Å. A volume of 27 nm³ equals 27,000 Å³ because all three lengths are converted.

ConditionsStandard GRO lengths use nm and traditional PDB lengths use Å. Use the format conventions during conversion to avoid converting twice.

The interactive example below uses one illustrative position to distinguish changing a unit from moving an atom. Switching units preserves the physical position and changes its numerical description. Moving the slider changes the position itself. The relationship is familiar from describing the same desk as 180 cm or 1.8 m long. Molecular coordinates require the same habit: read the value and unit together. A bare number does not fully specify a physical distance, even if it appears in a neatly formatted table.

Moving the particle changes its position; changing units only changes its numerical description.

[Figure: The same position described in nanometres and ångströms](https://ml-biomat.com/tutorials/molecular-dynamics/g02/en/#en-s3)

Unit-conversion illustration: changing the display unit preserves the physical position.

The box record is also more than a border drawn around the molecules. Three lengths describe the orthogonal cube used here. More general cells require three box vectors that can contain off-diagonal components. These vectors determine how periodic images are arranged, affecting neighbour searches, shortest distances, and density calculations. Our inspection script converts the box record into a three-by-three matrix and calculates its volume. In the present cube, the result can be checked by multiplying the side lengths. The matrix representation also supports the later interpretation of tilted cells.

Decimal precision has a physical meaning too. Coordinates printed to three decimal places in nanometres have a last digit corresponding to 0.001 nm, or 0.01 Å. Rounding introduces small differences from the values held internally during computation. A convenient text representation of the final positions is therefore not automatically a full-precision continuation state. Use checkpoints when continuing a run and an appropriate coordinate precision when inspecting a structure. The intended next operation should determine the output choice, rather than choosing solely by file size.

## A topology turns names and positions into a physical model

Opening topol.top reveals include directives and sections named system and molecules. An include directive brings definitions from another file into the input, rather like an assembly manual referring to a specification before listing the parts to be assembled. Here, forcefield.itp from oplsaa.ff establishes the parameter framework, and spce.itp defines the SPC/E water molecule. The combined definitions determine the model. The name of the outermost file alone does not identify every interaction that will be applied.

The system section provides a human-readable description, while molecules lists the molecule types and their counts. Our box contains only SOL, so the inventory is short. Before construction, it has no water count. After gmx solvate places the molecules, it updates the corresponding inventory. That count must agree with the sequence of molecules in the coordinates. A coordinate file containing many waters paired with an empty inventory does not give preprocessing enough molecular definitions to assign to those coordinates.

### Topology template before constructing the water box

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

After gmx solvate adds water, the molecules section contains its actual SOL count. The named force-field files come with the specified GROMACS installation; spce.itp defines the water model.

The SPC/E molecule definition lists three sites in oxygen–hydrogen–hydrogen order, with the appropriate atom types and partial charges. Constraint definitions maintain the rigid geometry during dynamics, while nonbonded interactions use their associated parameters. A simple consistency check follows immediately: every molecule should correspond to three coordinate records. This does not replace a complete chemical check, but it quickly detects missing sites, duplicated water, or an inventory that was not updated. For a mixture, the same idea becomes a sum over the site count and abundance of each molecule type.

The count relationship for pure three-site waterEq. 2

![The count relationship for pure three-site water](https://ml-biomat.com/static/agent-math/2d92f9d8f093d6e9ab198232.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Nsite | Number of coordinate interaction sites; each site corresponds to an atom here | count, dimensionless |
| Nwater | Number of SOL water molecules in the topology inventory | count, dimensionless |
| 3 | Sites per SPC/E molecule: one oxygen and two hydrogens | dimensionless |
| =, × | Equality requires matching counts; adjacent factors multiply sites per molecule by molecule count | operators have no units |

Reading the relationshipEvery complete water contributes three sites; repeating this definition Nwater times gives the total.

A worked exampleAn illustration specified to contain 900 SPC/E waters requires 2700 sites. The actual example uses the construction count, read directly by the script rather than assuming 900.

ConditionsThis applies to the pure three-site water example. Sum over molecule types in mixtures, and distinguish physical atoms from interaction sites in four-site water with a virtual site.

A matching total can still hide an incorrect arrangement. Exchanging a hydrogen coordinate between two neighbouring waters preserves the atom count while potentially creating unsuitable internal geometry. Shuffling atom order also preserves the count while assigning topology identities to the wrong positions. Counting therefore works together with checks of name order, local geometry, and the processed topology. Each observation answers a different question: how many entries exist, which identity each entry represents, and where each one has been placed.

Charge provides another understandable check. SPC/E assigns −0.8476 e to oxygen and +0.4238 e to each hydrogen, where e is the elementary charge. These three contributions sum to zero, so any integer number of complete molecules remains electrically neutral. The zero refers to total charge; it does not remove the consequences of separated positive and negative partial charges within each molecule. When ions are added later, checking the total charge helps establish whether the composition matches the intended design. Salt concentration additionally depends on ion count and solution volume.

Force-field selection also involves compatibility between parameters. Different parameter sets can use different charges, nonbonded combination rules, water models, or corrections. Copying their files into one directory does not make a consistent model automatically. Our pure-water example uses the supplied SPC/E definition, making the relationship straightforward. Later examples with proteins, small molecules, and sugars explain why a parameter family is selected and how solute and solvent are paired. Following include relationships now makes it easier to identify the definitions that control physical behaviour in those examples.

The -pp option of grompp writes a processed topology after include directives and conditional choices have been resolved. This helps identify what the program actually receives. The short original topol.top remains convenient to read and edit, while the expanded file exposes more of the final definitions. Changes should be made to the intended source input and followed by preprocessing again. Editing an expanded diagnostic file has no effect if the next command still reads the unchanged original input.

## Run parameters describe how an observation is performed

An MDP file contains run parameters, usually as lines of the form “name = value,” with comments following semicolons. A name identifies a setting and its value selects the behaviour for this run. In a dynamics stage, integrator selects the motion-update algorithm, dt specifies the time step, and nsteps specifies the number of updates. Other settings describe neighbour searches, interactions, temperature and pressure control, and output frequency. Grouping these by their roles in an observation is more useful initially than trying to memorize every option.

The preparation stages have different purposes. em.mdp performs energy minimization to relieve large forces associated with the initial arrangement. nvt.mdp lets the motion adjust to the target temperature at fixed volume. npt.mdp then allows the volume to respond to pressure control. Two final NVE inputs start from the same state and cover the same physical duration, using 1 fs and 2 fs time steps to compare numerical integration behaviour. Separate stage files make the conditions readable and let us inspect one stage before moving to the next.

The complete em.mdp used by this lesson's preparation command is shown below. FLEXIBLE in the define setting selects the supplied water topology's flexible bond and angle branch so the initial geometry can relax. NVT, NPT, and NVE dynamics then restore rigid water. During minimization, nsteps is a maximum number of updates, with earlier termination when the force criterion is met. Multiplying it by a dynamics time step would not describe physical motion. Here we identify where each setting lives; the next lesson explains the force threshold, minimization step, and convergence trace.

### Complete minimization input em.mdp

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

Initial minimization uses the supplied flexible water branch, followed by rigid-water dynamics. The maximum is 10,000 updates, force threshold 100 kJ mol⁻¹ nm⁻¹, and minimization step parameter 0.001 nm. The actual stopping point comes from the run.

Output frequency is part of the observation design. Updating motion every step does not mean writing coordinates, energies, and detailed logs every step. nstxout-compressed controls the compressed coordinate interval, nstenergy controls energy records, and nstlog controls detailed log output. If one file saves frames every 1 ps and another saves measurements every 0.2 ps, their row numbers do not identify matching times. Combining such records requires their physical time values. This is also why a smooth-looking animation does not tell us how frequently the underlying positions were saved.

Initial velocities change the meaning of a run. At the beginning of dynamics, velocities may be generated for a target temperature. Continuing equilibrated motion instead calls for preserving the preceding state. A fixed random seed records one reproducible choice of generation or stochastic sequence, making comparisons easier. It does not eliminate physical fluctuations. Different seeds can support independent repetitions, whose variation helps assess statistical behaviour. Later lessons connect seeds and repetitions to uncertainty; here, distinguish stages that create a state from stages intended to continue one.

Similar-looking numbers can carry different units. A dt value of 0.002 is a time in picoseconds, an output interval of 500 is a step count, and a ref-t value of 300 is a temperature in kelvin. A thermostat coupling time is another physical duration, describing an algorithmic response scale rather than the total simulation length. Read every setting as four connected pieces: name, value, unit, and purpose. This makes it possible to identify whether a change alters time resolution, recording frequency, or coupling to the environment.

Many options not explicitly listed in an MDP receive default values. Defaults keep inputs readable, but the final settings still matter. The -po option of grompp writes the processed parameter file, exposing what was actually interpreted. The original and processed files are complementary. One expresses the choices deliberately entered by the author; the other helps establish the complete settings received by the program. This distinction is useful when changing software versions, comparing two runs, or examining why an observable has changed.

Settings must also fit together physically. Cutoffs relate to box dimensions, time steps relate to fast motion and constraints, and coupling algorithms relate to the statistical conditions being sampled. An MDP that ran successfully for a protein does not automatically have the same meaning for a membrane or a coarse-grained polymer. Each new system will identify the shared principles and the choices that require reconsideration. The present water files have a precise initial purpose: establish consistent, inspectable conditions for the actual run developed next.

## Connect preprocessing, running, and continuation

The gmx grompp tool assembles the inputs for a run. It reads coordinates, topology, and parameters, resolves included definitions, expands molecule types to their requested counts, and performs consistency checks before writing a tpr file. That binary file holds the structure and model information needed by mdrun. Preprocessing is comparable to checking the itinerary, passengers, and vehicle before departure; mdrun advances the actual motion. Passing the technical checks establishes that the input can be processed. Whether its physical choices answer the research question remains a matter of model and protocol design.

### Construct, preprocess, and minimize the box

```
#!/usr/bin/env bash
set -euo pipefail
# Run inside the water example directory with its supplied input files.
gmx --version
cp topol.template.top topol.top
gmx solvate -cs spc216.gro -box 3 3 3 -o water.gro -p topol.top
gmx grompp -f em.mdp -c water.gro -p topol.top \
  -o em.tpr -pp em.top -po em.processed.mdp
gmx mdrun -deffnm em -ntmpi 1 -ntomp 4 -pin off
```

Run in the example directory containing this page’s topology template and em.mdp. The shell settings stop after undefined variables or failed commands so incomplete inputs are not silently propagated. The local command uses four CPU threads.

The command lists the roles explicitly. The -f argument identifies parameters, -c identifies coordinates, -p identifies topology, and -o specifies the generated TPR. The -pp and -po options save the processed topology and parameters. The following mdrun command uses -deffnm em to give stage outputs the common em prefix. A prefix does not change the molecules' motion, but it makes em.gro, em.edr, and em.log easy to associate. Consistent stage names let a reader follow the calculation and find the right kind of information.

Commands resolve relative filenames from their current working directory. The name water.gro refers to that directory, while input/water.gro refers to a file in its input subdirectory. Relative locations let a complete example move between computers while preserving these relationships. In Bash, a backslash at the end of a line continues the same command onto the following line, so those lines must be executed together. Text printed in the terminal and files written to storage serve different roles. Visible progress messages alone do not establish that all required output has been saved completely.

After a run, a GRO file stores coordinates at a particular time and can include velocities. XTC stores a time sequence of compressed coordinates. EDR holds energy and thermodynamic records, while LOG contains settings, progress, and diagnostics. A CPT checkpoint preserves more of the running state, including internal variables needed by particular algorithms. Saving final coordinates and saving a state suitable for continuation therefore serve different purposes. Keeping only coordinates and generating new velocities can start a new calculation, but it does not directly continue the original trajectory.

To move between stages, we commonly provide both coordinates and a checkpoint, such as nvt.gro and nvt.cpt when preparing NPT. The coordinate input makes the structural starting point explicit, while the checkpoint transfers state information. Whether velocities are regenerated and how constraints or coupling are continued still follows the protocol. Restarting an interrupted instance of the same stage instead uses the checkpoint continuation options of mdrun. One operation begins a new stage with changed conditions; the other completes the remaining time under the existing run settings.

Diagnostic messages should be interpreted through these input relationships. A mismatch between coordinate count and topology count is not repaired by continuing the calculation. An option that no longer applies to the current version calls for identifying and correcting the relevant setting. Ignoring warnings is not a general preparation step, and messages do not all indicate the same problem. Logs identify particular objects, settings, and locations. Returning from that information to the input usually resolves a problem more effectively than trying unrelated command variations.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g02/en/#en-s6)

Figure 3 · Outputs from the same run preserve different information. XTC does not contain full continuation state, and a text GRO has different precision and content from a checkpoint.

## Use a complete program to inspect the water box

We can now express the reading process as a repeatable check. The program takes water.gro and topol.top, reads the declared atom count, and compares it with the coordinate records. It finds the SOL inventory in the molecules section and checks the total expected for three-site water. It then examines atom-name order within each molecule and calculates the box volume. Every step has a purpose: identify inconsistent file combinations before dynamics and turn information hidden in text into visible numerical and graphical descriptions.

This reader targets the standard three-decimal-place GRO coordinates and pure-water topology used in our example. Fixed-position fields recover names and coordinates more faithfully than splitting the entire line at spaces. GRO can use other precisions, and complex topologies can be organized more extensively. Those cases require a format-aware library or an appropriately expanded reader. Stating the intended input at the beginning of the program makes the reuse decision clear: a reader can identify when the script applies directly and when parsing needs to be adjusted first.

### Complete Python: inspect coordinates, topology, and geometry

```
#!/usr/bin/env python3
"""Inspect this example's standard-precision GRO and pure-SOL topology.

Usage: python inspect_water.py water.gro topol.top --output inspection --language en
Dependencies: numpy, matplotlib. Input files are never modified.
The reader targets GRO coordinate fields with three decimal places (width 8).
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def read_gro(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    if len(lines) < 3:
        raise ValueError("Incomplete GRO file.")
    n_atoms = int(lines[1].strip())
    if n_atoms < 3 or len(lines) != n_atoms + 3:
        raise ValueError("Declared atom count does not match coordinate lines.")
    coordinates, names, residues = [], [], []
    for line in lines[2:2 + n_atoms]:
        if len(line) < 44:
            raise ValueError("An atom record is too short for standard GRO fields.")
        residues.append((int(line[0:5]), line[5:10].strip()))
        names.append(line[10:15].strip())
        coordinates.append([float(line[20:28]), float(line[28:36]), float(line[36:44])])
    xyz = np.asarray(coordinates, dtype=float)
    box_values = [float(value) for value in lines[-1].split()]
    if len(box_values) == 3:
        box = np.diag(box_values)
    elif len(box_values) == 9:
        b = box_values
        box = np.array([[b[0], b[3], b[4]], [b[5], b[1], b[6]], [b[7], b[8], b[2]]])
    else:
        raise ValueError("A GRO box must contain three or nine components.")
    if not np.all(np.isfinite(xyz)) or not np.all(np.isfinite(box)):
        raise ValueError("Nonfinite coordinate or box component.")
    volume = float(np.linalg.det(box))
    if volume <= 0:
        raise ValueError("Box volume must be positive.")
    return xyz, names, residues, box, volume


def read_water_count(path: Path) -> int:
    section = ""
    inventory = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split(";", 1)[0].strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip().casefold()
        elif section == "molecules":
            fields = line.split()
            if len(fields) != 2:
                raise ValueError("Expected molecule name and count.")
            inventory.append((fields[0], int(fields[1])))
    if len(inventory) != 1 or inventory[0][0] != "SOL" or inventory[0][1] <= 0:
        raise ValueError("This reader requires one positive SOL entry in [ molecules ].")
    return inventory[0][1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("gro", type=Path)
    parser.add_argument("topology", type=Path)
    parser.add_argument("--output", type=Path, default=Path("inspection"))
    parser.add_argument("--language", choices=("zh", "en"), default="en")
    args = parser.parse_args()
    xyz, names, residues, box, volume = read_gro(args.gro)
    n_water = read_water_count(args.topology)
    if len(xyz) != 3 * n_water:
        raise ValueError("Coordinate sites do not equal three times the SOL count.")
    for i in range(n_water):
        begin = 3 * i
        if names[begin:begin + 3] != ["OW", "HW1", "HW2"]:
            raise ValueError(f"Water {i + 1}: expected OW, HW1, HW2 order.")
        group = residues[begin:begin + 3]
        if not (group[0] == group[1] == group[2] and group[0][1] == "SOL"):
            raise ValueError(f"Water {i + 1}: inconsistent residue identity.")
    oxygen = xyz[::3]
    summary = {
        "coordinate_file": args.gro.name,
        "topology_file": args.topology.name,
        "coordinate_sha256": hashlib.sha256(args.gro.read_bytes()).hexdigest(),
        "topology_sha256": hashlib.sha256(args.topology.read_bytes()).hexdigest(),
        "molecules_SOL": n_water, "sites_from_coordinates": len(xyz),
        "sites_from_topology": 3 * n_water, "atom_order": "OW, HW1, HW2",
        "box_vectors_nm": box.tolist(), "volume_nm3": volume,
        "structure_stage": "initial solvent construction",
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "water_input_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    with (args.output / "water_input_summary.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["quantity", "value", "unit"])
        writer.writerows([
            ["SOL molecules", n_water, "count"],
            ["coordinate sites", len(xyz), "count"],
            ["topology sites", 3 * n_water, "count"],
            ["box volume", volume, "nm^3"],
        ])
    zh = args.language == "zh"
    tr = lambda chinese, english: chinese if zh else english
    plt.rcParams.update({"font.family": ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else "DejaVu Sans",
        "font.size": 14, "svg.fonttype": "path", "figure.facecolor": "#faf9f4",
        "axes.facecolor": "#faf9f4", "savefig.facecolor": "#faf9f4",
        "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(2, 2, figsize=(12, 9), constrained_layout=True)
    corners = {bits: np.asarray(bits) @ box for bits in itertools.product((0, 1), repeat=3)}
    for axis, (a, b) in zip(axes.flat, ((0, 1), (0, 2), (1, 2))):
        axis.scatter(oxygen[:, a], oxygen[:, b], s=10, alpha=0.55, color="#387d70", linewidths=0)
        for bits, origin in corners.items():
            for dimension in range(3):
                if bits[dimension] == 0:
                    target_bits = list(bits)
                    target_bits[dimension] = 1
                    target = corners[tuple(target_bits)]
                    axis.plot([origin[a], target[a]], [origin[b], target[b]],
                              color="#b06b41", linewidth=1.0)
        axis.set(xlabel=f"{'xyz'[a]} / nm", ylabel=f"{'xyz'[b]} / nm", aspect="equal")
        axis.set_title(tr("初始水氧投影", "Initial oxygen projection"), fontsize=14)
    axis = axes[1, 1]
    labels = [tr("坐标记录", "Coordinate records"), tr("拓扑预期", "Topology expectation")]
    counts = [len(xyz), 3 * n_water]
    bars = axis.bar(labels, counts, color=["#387d70", "#b06b41"], width=0.56)
    axis.bar_label(bars, padding=5, fontsize=15)
    axis.set_ylim(0, max(counts) * 1.2)
    axis.set_ylabel(tr("位点数", "Number of sites"))
    axis.set_title(tr("三位点水的数量核对", "Three-site water count check"), fontsize=14)
    fig.suptitle(tr("初始结构：坐标、拓扑与盒子", "Initial structure: coordinates, topology, and box"), fontsize=20)
    fig.savefig(args.output / "water_input_inspection.svg")
    fig.savefig(args.output / "water_input_inspection.png", dpi=180)
    plt.close(fig)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

Use the command in the script header with the constructed water.gro and topol.top; --language selects zh or en plots. The input files remain unchanged. Projections describe the initial structure, and counts and volume come directly from those files.

The program plots initial water-oxygen coordinates in three planar projections and compares two ways of counting the sites. A projection resembles casting a three-dimensional object's shadow onto a wall: two coordinate directions remain visible while depth is superimposed. Two nearby points on the plot are therefore not necessarily oxygen atoms in close contact in three dimensions. The projections help inspect overall filling, box extent, and conspicuous gaps. Precise neighbour distances require three-dimensional calculations with periodicity. The figure identifies the positions as an initial structure, rather than an equilibrium distribution.

### Actual coordinates and topology counts of the initial box

Produced by G02/inspect_water.py from the final example’s constructed water.gro and topol.top. Three panels project oxygen positions; another compares coordinate sites with the topology expectation. These describe the initial constructed state.

GROMACS 2026.4; 884 SPC/E waters in an initially 3 nm cubic box, with targets of 300 K and 1 bar. The NPT record spans 100 ps and descriptive statistics use 50–100 ps; the player shows a separate 100 ps NVE stage.

[Download reference data and complete inputs (ZIP) 1.82 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-water-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g02/en/#en-s7)

Three orthogonal projections of the actual initial structure, with one point per water oxygen. The final panel compares coordinate records with the site count specified by the three-site-water topology. These are starting coordinates immediately after solvation.

| Quantity | Value | Unit |
| --- | --- | --- |
| Water molecules | 884 | 1 |
| Coordinate sites | 2652 | 1 |
| Topology sites | 2652 | 1 |
| Initial box volume | 27.0 | nm³ |

Construction produced 884 water molecules and 2652 coordinate sites, exactly three sites per SPC/E molecule. The topology expectation agrees with the coordinate count. The initial volume is 27 nm³, corresponding to three 3 nm sides. Projections inspect filling from different directions, while the count panel establishes the correspondence between inventory and coordinates. The subsequent NPT mean volume changes, so 27 nm³ describes the constructed starting point rather than every later trajectory frame.

Once counts agree, inspect the first few molecules manually, confirm the organization of oxygen and hydrogen records, and examine the processed topology written by grompp. The script complements this physical reading by standardizing steps that are easy to overlook repeatedly. Adding salt would require extending the inventory, site counts, and graphical categories. Switching to four-site water would also require explaining the relationship between interaction sites and physical atoms. The present check is deliberately tied to the stated three-site system.

The JSON and CSV outputs store relative filenames, measured counts, box geometry, and consistency results. They are descriptions extracted from existing inputs, rather than new molecular dynamics observations. Temperature, density fluctuations, and motion still come from the files generated by an actual run. Separating input description from run observation prevents an initial-coordinate figure from being used as evidence of equilibration. It also helps identify which layer of information to inspect first when an unexpected curve appears.

File digests support a direct content comparison. A digest algorithm transforms file bytes into a fixed-length identifier, and changing the contents normally changes that identifier. This helps verify a download, copy, or archived input. It answers whether the byte content changed, rather than whether the molecular model suits a scientific question. The latter still requires examining composition, parameters, geometry, and observation conditions. Separating these checks supports reliable file management while keeping physical judgment where it belongs.

## Organize an input set that can support further research

At this point, each file can be described by its role. Coordinates give the starting geometry; topology defines particles and interactions; parameters determine advancement and observation; TPR assembles the run; checkpoints preserve continuation state; trajectories and energy files store different observations. This understanding lasts longer than a memorized list of extensions. When a new format or tool appears, its information can still be placed within the same structure, and the questions to ask remain recognizable.

Preserving the inputs means preserving the complete resolvable combination, rather than retaining topol.top alone. Its force-field version, local ITP files, coordinates, and parameter files all contribute to the model. File digests can identify whether an input changed between comparisons, while clear stage names identify the run order. An inspectable calculation relies on these specific pieces being recombined, without requiring someone to guess which of several similarly named files was actually used. This becomes increasingly useful as a project grows beyond its first example.

Consider a short reasoning exercise. Suppose the target temperature in npt.mdp is changed to 310 K, but the old npt.tpr is passed directly to mdrun. Which temperature setting is used? The file relationship supplies the answer: mdrun reads the already generated TPR, so preprocessing must be repeated to incorporate the edited text. Now suppose more waters are added to the coordinates but the molecules inventory remains unchanged. The inconsistency belongs to model assembly and should be found before dynamics. Understanding the flow makes both answers predictable.

The next lesson uses these inputs to advance the water molecules. We will read minimization, temperature adjustment, pressure adjustment, and observation records in sequence, explaining why their purposes differ and how to judge progression from the actual curves. Knowing where each setting is stored will let us connect parameter changes to the physical process they influence.

## Further Reading and Open Materials

- [GROMACS tutorial 1: Water](https://gaseri.org/en/tutorials/gromacs/1-tip4pew-water/) · Wes Barnett; Vedran Miletić · CC BY-SA 4.0 (English tutorials)

  Adaptation of the coordinate–topology–parameter organization and water-box preparation workflow.

  Uses SPC/E and 2026.4 settings; adds introductory explanations, bilingual diagrams, a unit interaction, and an independently written inspection script. Adapted workflow material retains CC BY-SA 4.0.
- [GROMACS 2026.4 file formats](https://manual.gromacs.org/2026.4/reference-manual/file-formats.html) · GROMACS developers · Technical reference; no copied figure or extended prose

  GRO fixed fields and output format definitions.

  Independent explanations and an example-specific reader.
- [gmx grompp, GROMACS 2026.4](https://manual.gromacs.org/2026.4/onlinehelp/gmx-grompp.html) · GROMACS developers · Technical reference

  Preprocessing, includes, and output options.

  Explained through this example’s file relationships.
- [PDB History](https://www.rcsb.org/pages/about-us/history) · RCSB Protein Data Bank · Factual historical citation; no image reuse

  Establishment in 1971 with seven structures.

  Original historical schematic.
