# How Lipids Assemble into a Membrane

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g15/en/
Language: en

Represent chemical fragments as beads, follow recorded DSPC self-assembly, and interpret the bilayer through leaflet area, density, and orientation.

## How a membrane emerges from dispersed molecules

A little detergent helps disperse grease in dishwater, while a thin lipid membrane separates the inside of a cell from its surroundings. Both phenomena involve molecules with an unusual combination of properties: one part interacts favorably with water, whereas another favors an oily environment. Depending on molecular shape, composition, and concentration, such molecules can organize into small aggregates, sheets, or water-filled vesicles. Understanding this organization helps us study how drug carriers form, how membrane materials remain intact, and why changing lipid composition changes their structure. Here we begin with randomly placed lipids, observe their aggregation in water beads, and turn the resulting membrane into an object we can measure.

The lipid is DSPC, short for distearoylphosphatidylcholine. Its name identifies a phosphatidylcholine head and two stearoyl tails, each containing eighteen carbon atoms and no carbon–carbon double bond. The head carries separated positive and negative charges, while the complete molecule is electrically neutral. Most of each tail consists of hydrocarbon material. Two opposing rows can place their tails together while leaving their heads exposed to water, producing a bilayer. Each row is called a leaflet. Two rows of umbrellas with handles pointing toward each other provide a useful picture of the orientation, although real lipid tails are flexible and the molecules continuously move.

The terms hydrophilic and hydrophobic summarize interactions with the surrounding environment. Water, lipid heads, and lipid tails all contribute to changes in energy and molecular arrangements. Aggregation reduces many direct contacts between hydrocarbon tails and water while changing the configurations available to both components. A coarse-grained model collects part of this molecular detail into effective interactions. Consequently, the program can produce aggregation without assigning a destination to each lipid. The observed organization develops under a particular model, temperature, composition, and initial condition. Intermediate structures can also persist while molecules search for rearrangements that are difficult to reach within a short trajectory.

This example contains 128 DSPC molecules and 768 water beads, giving 2304 simulated particles. The first stage runs for 30 ns at 340 K and a target pressure of 1 bar, allowing the dispersed lipids to organize. The membrane that forms is then rotated into a convenient orientation and simulated for another 30 ns to examine its area, thickness, and tail alignment. A temperature of 340 K corresponds to about 66.85 °C and specifies the state studied with this lipid model. Each stage contains 301 saved frames separated by 100 ps. The plotted times are the times advanced by the model.

Three questions guide the lesson. How can a model reduce atomic detail while retaining the head–tail distinction and the tendency to form a membrane? How can an increasingly orderly picture become a reproducible structural measurement? And how should area and thickness be defined when the two leaflets contain different numbers of molecules? The questions belong together: model resolution determines what information is available, periodic boundaries determine how coordinates are read, and molecular counts determine the interpretation of an average. Following this sequence provides a practical way to select a suitable resolution and build a coherent analysis of a membrane system.

## From atoms to beads: what is retained and averaged

The preceding PEG model retained every carbon, hydrogen, and oxygen atom. We now change the level of description. A city map offers a useful analogy: locating a shop requires streets and addresses, while understanding travel between cities benefits from a broader view. Coarse graining changes resolution to emphasize selected questions. A bead represents a chemical fragment containing several atoms, and its coordinate describes the fragment's overall position. Many rapid internal vibrations are averaged out. This allows computational effort to follow collective rearrangements of more molecules. Here the main questions concern head–tail segregation and bilayer organization, for which we use a twelve-bead lipid representation.

Lipid simulation provides a concrete historical example of this reasoning. In 2004, Marrink, de Vries, and Mark published a coarse-grained model for lipids and surfactants that represented chemical fragments with a small set of interaction types and demonstrated spontaneous bilayer assembly. Starting with an already arranged membrane makes it convenient to study fluctuations; observing how a membrane forms requires many molecules to rearrange collectively. Reducing the number of degrees of freedom helped bring the latter process into computational reach. It also sharpened the central modeling question: which information must remain in the effective interactions for the desired organization to emerge?

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g15/en/#en-s2)

Figure 1 · Lipid coarse graining develops from fragment representation to finer chemical types and tail parameters. The 2025 panel uses equal bead counts and different spacings to illustrate parameter distinctions; spacings are schematic.

Martini 3, published in 2021, expanded the descriptions of bead size and chemical interaction types so that the framework could distinguish a wider range of molecular environments. Bead types are connected to physical behavior, including how compounds partition between environments, rather than assigned as arbitrary visual categories. The 2025 lipid update further refined tail mapping and bonded parameters to distinguish chains differing by two carbon atoms. This progression concerns both how much detail is removed and how accurately the retained variables express chemical differences. Our example uses the Martini 3 base interactions together with the updated DSPC lipid parameters.

The twelve beads have identifiable roles. NC3 describes the positively charged choline region, PO4 the negatively charged phosphate region, and GL1 and GL2 the glycerol and connecting regions. C1A through C4A represent one tail, while C1B through C4B represent the other. The letters distinguish tails, and the numbers follow their sequence. A bead name identifies a location within the molecule; a bead type specifies which interaction parameters it uses. Thus, the bead named C1A has type C1 in the current DSPC topology. The connecting lines describe coarse-grained connectivity, with lengths and stiffness parameters appropriate to fragments rather than individual carbon–carbon bonds.

The solvent representation changes as well. One W bead corresponds to a coarse-grained description of four water molecules. Therefore, 768 W beads give a nominal count of 3072 waters, or 24 waters per lipid. This count describes overall hydration; it does not supply four separately trackable water molecules inside each bead. Atomic O–H directions, hydrogen-bond angles, and single-water rotations require a model that retains those degrees of freedom. At the present resolution, we can instead measure how water beads distribute around the membrane and how water-rich and tail-rich regions separate. The observable should be matched to the information the model actually carries.

Count beads and their mapped compositionEq. 1

![Count beads and their mapped composition](https://ml-biomat.com/static/agent-math/10d931ff75583216629feae3.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Nbead | Total simulated particle count | 1 |
| NL | DSPC molecule count, 128 here | 1 |
| NW | W bead count, 768 here | 1 |
| Nwater | Nominal water-molecule count under the mapping | 1 |
| h | Nominal water molecules per lipid | 1 |
| 12, 4 | Twelve beads per lipid; four mapped waters per W | 1 |
| =, +, ×, / | Equality, addition, multiplication and division; adjacent symbols multiply | 1 |

Reading the relationshipCount lipid and water representations separately, then divide mapped waters by lipids to describe overall hydration.

A worked example12×128+768=2304 beads; 4×768=3072 nominal waters; 3072/128=24 waters per lipid.

ConditionsFor the twelve-bead DSPC and four-water W mapping used here; mapped water count describes composition.

## Match parameter files to molecular composition

Begin by distinguishing the four parameter files. The base file defines bead types and nonbonded interactions. The bonded file supplies constants used by lipid connections. The phosphatidylcholine file describes the twelve DSPC beads and their connectivity, and the solvent file defines W. The system topology includes these files in the required order and then specifies 128 DSPC molecules and 768 W beads. This resembles assembling a vocabulary and grammar before writing a complete sentence: every referenced type and parameter must already be defined. The v2 labels identify the lipid parameter revision, separately from the Martini 3 base version used with it.

### DSPC system topology

```
#include "martini_v3.0.0.itp"
#include "martini_v3.0.0_ffbonded_v2.itp"
#include "martini_v3.0.0_phospholipids_PC_v2.itp"
#include "martini_v3.0.0_solvents_v1.itp"

[ system ]
DSPC BILAYER SELF-ASSEMBLY

[ molecules ]
DSPC 128
W    768
```

Four compatible ITP files define the model; molecules lists 128 DSPC and 768 W in coordinate order.

Starting coordinates and force-field parameters have different jobs. Coordinates specify where twelve points begin, while the topology determines what those points represent and how they interact. We use the twelve-bead starting geometry from the official workflow, label its residue DSPC, and run it with the DSPC tail parameters. DPPC and DSPC can share a twelve-bead geometrical starting representation in this scheme, while their chemical tail lengths and appropriate parameters differ. Renaming a residue is therefore one preparation step within a complete model definition. When inspecting an initial molecular picture, also check the types, connections, bond lengths, and angles assigned by the topology.

Random insertion places 128 copies of the starting lipid into a cube with 7.5 nm sides. The insertion procedure tries different positions and orientations and uses geometrical separation to avoid obvious overlaps. A fixed random seed specifies a reproducible preparation choice. Solvation then adds up to 768 water beads. Because the initial box is relatively large and the water count is limited, some regions initially contain little water. Minimization and pressure coupling subsequently adjust contacts and volume. This is a low-hydration assembly setting, and water content itself influences the accessible aggregate structures. A comparison at another water content defines another physical condition whose structural evolution should be examined.

Three MDP files separate geometrical relaxation, self-assembly, and subsequent membrane adjustment. Steepest-descent minimization permits up to 10000 steps with a force tolerance of 100 kJ mol⁻¹ nm⁻¹. Its optimization steps improve contacts rather than define dynamical time. Both molecular-dynamics stages use a 0.02 ps, or 20 fs, step and 1500000 steps, giving 30000 ps per stage. Averaging out rapid atomic vibrations makes this step compatible with the chosen coarse-grained model. It belongs to the complete parameter set: the preceding atomistic PEG and protein models retain faster motions and require a time step suited to those degrees of freedom.

### Write the three complete MDP files

```
"""Write the three full parameter files used for DSPC assembly and relaxation."""
from pathlib import Path
import argparse

FILES = {
'em.mdp': """integrator = steep
nsteps = 10000
nstxout = 0
nstvout = 0
nstfout = 0
cutoff-scheme = Verlet
nstlist = 20
nsttcouple = 20
nstpcouple = 20
rlist = 1.35
verlet-buffer-tolerance = -1
pbc = xyz
coulombtype = reaction-field
rcoulomb = 1.1
epsilon-r = 15
epsilon-rf = 0
vdw-type = cutoff
vdw-modifier = Potential-shift-verlet
rvdw = 1.1
constraints = none
constraint-algorithm = Lincs
lincs-order = 8
lincs-warnangle = 90
lincs-iter = 2
emtol = 100
emstep = 0.01
""",
'assembly.mdp': """integrator = md
dt = 0.02
nsteps = 1500000
comm-mode = Linear
nstcomm = 100
comm-grps = System
nstxout = 0
nstvout = 0
nstfout = 0
nstlog = 10000
nstenergy = 1000
nstxout-compressed = 5000
compressed-x-precision = 100
compressed-x-grps = 
energygrps = System
cutoff-scheme = Verlet
nstlist = 20
nsttcouple = 20
nstpcouple = 5
rlist = 1.35
verlet-buffer-tolerance = -1
pbc = xyz
coulombtype = reaction-field
rcoulomb = 1.1
epsilon-r = 15
epsilon-rf = 0
vdw-type = cutoff
vdw-modifier = Potential-shift-verlet
rvdw = 1.1
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 340
gen-vel = yes
gen-temp = 340
gen-seed = 20261501
pcoupl = c-rescale
pcoupltype = isotropic
tau-p = 4.0
ref-p = 1.0
compressibility = 3e-4
constraints = none
constraint-algorithm = Lincs
lincs-order = 8
lincs-warnangle = 90
lincs-iter = 2
ld-seed = 20261502
""",
'bilayer.mdp': """integrator = md
dt = 0.02
nsteps = 1500000
comm-mode = Linear
nstcomm = 100
comm-grps = System
nstxout = 0
nstvout = 0
nstfout = 0
nstlog = 10000
nstenergy = 1000
nstxout-compressed = 5000
compressed-x-precision = 100
compressed-x-grps = 
energygrps = System
cutoff-scheme = Verlet
nstlist = 20
nsttcouple = 20
nstpcouple = 5
rlist = 1.35
verlet-buffer-tolerance = -1
pbc = xyz
coulombtype = reaction-field
rcoulomb = 1.1
epsilon-r = 15
epsilon-rf = 0
vdw-type = cutoff
vdw-modifier = Potential-shift-verlet
rvdw = 1.1
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 340
gen-vel = no
gen-temp = 340
gen-seed = 20261501
pcoupl = c-rescale
pcoupltype = semiisotropic
tau-p = 4.0
ref-p = 1.0 1.0
compressibility = 3e-4 3e-4
constraints = none
constraint-algorithm = Lincs
lincs-order = 8
lincs-warnangle = 90
lincs-iter = 2
ld-seed = 20261503
continuation = yes
""",
}

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, default=Path("."))
    args = p.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    for name, content in FILES.items():
        (args.out/name).write_text(content, encoding="utf-8", newline="\n")
    print("Wrote em.mdp, assembly.mdp, and bilayer.mdp")
```

Run python write_parameters.py to generate complete minimization, assembly, and bilayer parameters.

The nonbonded treatment is also part of the model. This example uses reaction-field electrostatics with relative dielectric constant 15, a 1.1 nm cutoff, and a conducting external reaction-field limit. The van der Waals interaction uses the specified potential shift and the same cutoff. The v-rescale thermostat acts on the complete system, while C-rescale controls pressure. In larger membrane systems, examining solvent and membrane temperatures and their collective drift helps determine whether phase-specific coupling groups are appropriate. Pressure coupling is updated every five steps with a 4 ps time constant, a combination compatible with the current integration settings. The complete inputs make these choices inspectable.

## Read assembly through positions and collective orientation

Run the following script in an assembly directory containing the initial coordinates, topology, and parameter files. It performs insertion, solvation, minimization, and 30 ns of motion, then extracts temperature, potential energy, pressure, volume, and box lengths. Each operation uses the actual output of the preceding step. The minimized configuration becomes the initial state for dynamics, and grompp combines that state with the topology and parameters in a TPR file. The assembly prefix groups the resulting records. You can analyze the provided trajectory or generate another realization; floating-point operations and parallel execution can eventually separate detailed trajectories even with specified inputs and seeds.

### Insert lipids and run assembly

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
"$gmx" insert-molecules -ci DSPC-em.gro -box 7.5 7.5 7.5 -nmol 128 -radius 0.21 -try 500 -seed 20261500 -o lipids.gro > insert.log 2>&1
"$gmx" solvate -cp lipids.gro -cs water.gro -o solvated.gro -maxsol 768 -radius 0.21 > solvate.log 2>&1
"$gmx" grompp -f em.mdp -c solvated.gro -p topol.top -o em.tpr > em.grompp.log 2>&1
"$gmx" mdrun -deffnm em -ntmpi 1 -ntomp 2 -pin off > em.stdout.log 2>&1
"$gmx" grompp -f assembly.mdp -c em.gro -p topol.top -o assembly.tpr > assembly.grompp.log 2>&1
"$gmx" mdrun -deffnm assembly -ntmpi 1 -ntomp 2 -pin off > assembly.stdout.log 2>&1
printf 'Temperature
Potential
Pressure
Volume
Density
Box-X
Box-Y
Box-Z
0
' | "$gmx" energy -f assembly.edr -o assembly-properties.xvg > energy.log 2>&1
"$gmx" check -f assembly.xtc > trajectory-check.log 2>&1
```

Run bash run_assembly.sh in the assembly input directory, with all required inputs beside it.

In the recorded snapshots, teal points mark phosphate heads, gold points mark tail beads, and pale blue points mark water. Each panel projects three-dimensional coordinates onto the xy plane and maps particles into the current periodic box, so its displayed range follows the box dimensions. The initially dispersed components gradually develop distinct head-rich, tail-rich, and water-rich regions. At 30 ns, tail beads occupy both the top and bottom edges of the image. Joining those edges through the periodic boundary reveals one continuous membrane interior. The prominent water-rich region between the two headgroup bands is the intermembrane water layer, a useful reminder when reading periodic pictures.

### Four snapshots from dispersion to layered organization

Recorded xy projections at 0, 5, 15, and 30 ns: teal PO4, gold tail beads, pale-blue W. Points are mapped into each periodic box; GL and NC3 are omitted.

128 Martini 3 DSPC lipids and 768 W beads at 340 K and 1 bar. Thirty ns of isotropic self-assembly is followed by rotation of all positions and velocities to a z-normal membrane and 30 ns of semi-isotropic sampling. Uses PC/bonded v2 lipid parameters.

[Download reference data and complete inputs (ZIP) 5.97 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-dspc-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g15/en/#en-s4)

xy projections of native coordinates at 0, 5, 15 and 30 ns. Teal denotes PO4, gold tail beads and pale blue W. Each bead is mapped into its periodic cell; NC3 and GL are omitted.

To quantify collective orientation, assign each lipid a vector from the midpoint of its two terminal tail beads toward its PO4 head, then normalize its length to one. Normalization retains direction and gives each molecule equal weight. Lipids in opposing leaflets point in opposite directions, although both sets align with the same membrane normal. Simply adding the arrows would therefore cancel their contributions. Squared projections provide a more useful measurement: pointing upward or downward along one axis contributes equally, while lying sideways contributes less. This construction separates shared axial alignment from the distinction between the two directions along that axis.

Find the common lipid-alignment axisEq. 2

![Find the common lipid-alignment axis](https://ml-biomat.com/static/agent-math/bc3925c0d735aae09e536b9a.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| i, NL | Lipid index and total lipid count | 1 |
| a, b | Cartesian component indices x, y, z | 1 |
| uᵢ,ₐ, uᵢ,ᵦ | Components of the unit vector from terminal-tail midpoint to PO4 | 1 |
| δₐᵦ | One when a=b and zero otherwise | 1 |
| Qₐᵦ, Q | An element of the alignment matrix and the complete three-by-three matrix | 1 |
| S, λmax(Q) | Largest matrix eigenvalue, measuring the strongest common alignment axis | 1 |
| Σ, 1/NL | Sum over lipids and divide by their count for an equal-weight average | 1 |
| 3/2, 1/2 | Constants setting perfect axial alignment to one and the isotropic limit to zero | 1 |
| =, −, ×, /, max | Equality, subtraction, multiplication, division and maximum | 1 |

Reading the relationshipComponent products treat opposite directions along one axis equally. The largest eigenvalue identifies the most concentrated squared projections.

A worked exampleIf every direction is ±z, Q has diagonal entries −0.5, −0.5, 1 and S=1. The isotropic three-dimensional limit gives a zero matrix.

ConditionsComputed per frame from complete-lipid head–tail directions. S describes shared orientation; spatial distributions identify morphology. Finite isotropic samples fluctuate.

The matrix in the equation collects products of the three directional components across all lipids. Finding its largest eigenvalue identifies the axis with the strongest squared projections and measures their concentration through S. Initially the directions are dispersed, although a finite collection of 128 molecules still produces some random alignment. In this record, S rises toward about 0.8 after roughly 9 ns and reaches 0.799 at 30 ns. The final principal axis has absolute components approximately 0.028, 0.9995, and 0.012, placing it almost along y. Reversing the sign of an axis describes the same alignment, so the plot shows absolute components.

### Collective orientation and principal axis

301 frames; unit vectors from terminal-tail midpoint to PO4 define the alignment matrix. Axis signs are equivalent, so absolute components are plotted.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g15/en/#en-s4)

Largest alignment-tensor eigenvalue and absolute components of its principal axis over 301 frames. Molecular directions run from terminal-tail midpoint to PO4; the two signs of the axis are equivalent.

The orientation curve converts a visual impression into a reproducible measurement, while spatial information establishes the aggregate's structure. Parallel molecular axes can occur in more than one kind of assembly. Here the two headgroup layers, continuous tail region, and water distribution together identify the bilayer. Snapshots show where the components are, whereas the alignment statistic measures how consistently the molecules point along a common axis. A further step is still useful: allowing the membrane plane and its normal to adjust independently. Measuring area immediately after assembly would otherwise mix the newly formed structure with the dimensional relaxation that follows it.

## Rotate the membrane and release its lateral area

Once a membrane forms, the three spatial directions have different physical roles. Motion within the plane mainly encounters other molecules in the same leaflet, while motion along the normal passes through water, heads, tails, and the opposite heads. Isotropic pressure coupling in the assembly stage applies a common scale factor to all three box lengths. For a formed membrane, semiisotropic coupling lets the two in-plane directions scale together while the normal direction changes separately. This provides distinct freedoms for lateral area and normal dimension, making it a suitable choice for studying how a membrane adjusts its shape under specified temperature and pressure conditions.

The coupling convention treats xy as the membrane plane and z as its normal. Our assembled membrane is almost normal to y, so it must first be rotated. The program below transforms all coordinates to x, Lz−z, y, changes velocities to vx, −vz, vy, and exchanges the y and z box lengths. The translation places the rotated coordinates conveniently in the box; the rotation preserves distances and speeds. Imagine turning the entire transparent container through a quarter turn. The direction previously near y now lies near z, while the relative molecular structure remains the same and the pressure settings act along the intended directions.

### Rotate all coordinates and velocities

```
"""Rotate the recorded y-normal DSPC bilayer, retaining its velocities.

python rotate_bilayer.py --source assembly/assembly.gro --out bilayer/start.gro
The mapped box is orthorhombic: (x,y,z) becomes (x,Lz-z,y).
"""
from pathlib import Path
import argparse
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("assembly/assembly.gro"))
    parser.add_argument("--out", type=Path, default=Path("bilayer/start.gro"))
    args = parser.parse_args()
    lines = args.source.read_text().splitlines()
    count = int(lines[1]); atoms = lines[2:2+count]
    box = np.array([float(x) for x in lines[2+count].split()])
    if count != 2304 or len(box) != 3:
        raise ValueError("Expected 2304 beads in the recorded orthorhombic box")
    if any(len(line) < 68 for line in atoms):
        raise ValueError("The source must contain all three velocity components")
    xyz = np.array([[float(line[20+8*k:28+8*k]) for k in range(3)] for line in atoms])
    velocity = np.array([[float(line[44+8*k:52+8*k]) for k in range(3)] for line in atoms])
    transformed = xyz[:, [0, 2, 1]].copy(); transformed[:, 1] = box[2]-transformed[:, 1]
    vnew = velocity[:, [0, 2, 1]].copy(); vnew[:, 1] *= -1
    if not np.allclose(np.sum(vnew*vnew, axis=1), np.sum(velocity*velocity, axis=1)):
        raise ValueError("The rotation changed a bead speed")
    output = ["DSPC bilayer, membrane normal rotated from y to z", lines[1]]
    output += [line[:20]+"".join(f"{v:8.3f}" for v in pos)+"".join(f"{v:8.4f}" for v in vel)
               for line, pos, vel in zip(atoms, transformed, vnew)]
    output += [" ".join(f"{v:10.5f}" for v in box[[0, 2, 1]])]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(output)+"\n", encoding="utf-8", newline="\n")
    print("Rotated 2304 positions and velocities; all bead speeds preserved.")


if __name__ == "__main__":
    main()
```

Run python rotate_bilayer.py --source assembly/assembly.gro --out bilayer/start.gro.

The second stage retains the rotated coordinates and velocities, with gen-vel=no preventing a new velocity draw. Thermostat and barostat states are initialized for this new stage. Prepare a separate bilayer directory containing start.gro, bilayer.mdp, and the same topology and ITP files, then run the following script. Temperature remains 340 K, the step remains 20 fs, and the duration remains 30 ns. Pressure coupling changes to semiisotropic, with 1 bar targets in both the plane and normal direction. Each stage has its own time origin, so the assembly trajectory and the subsequent membrane trajectory should be read as separate 30 ns records.

### Run the semiisotropic continuation

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
"$gmx" grompp -f bilayer.mdp -c start.gro -p topol.top -o bilayer.tpr > bilayer.grompp.log 2>&1
"$gmx" mdrun -deffnm bilayer -ntmpi 1 -ntomp 2 -pin off > bilayer.stdout.log 2>&1
printf 'Temperature
Potential
Pressure
Volume
Density
Box-X
Box-Y
Box-Z
0
' | "$gmx" energy -f bilayer.edr -o bilayer-properties.xvg > energy.log 2>&1
"$gmx" check -f bilayer.xtc > trajectory-check.log 2>&1
```

Place start.gro, bilayer.mdp, topol.top, and the four ITP files in the bilayer directory, then run bash run_bilayer.sh.

Equal planar and normal pressure targets specify a condition without an imposed pressure difference between those directions. Instantaneous pressure still fluctuates in a finite system, and the two leaflets may carry different internal stresses. In particular, this assembly places 66 lipids on one side and 62 on the other. Changing box area does not automatically equalize their populations. Moving a lipid between leaflets requires its head to traverse an unfavorable membrane environment and constitutes another rearrangement process. Leaflet identities remain unchanged across the saved frames of this continuation, so the area analysis retains the actual membership as part of the studied system.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g15/en/#en-s5)

Figure 2 · Side-view schematic with heads outward and tails inward. Labels 66/62 give actual leaflet populations; circles schematically represent each leaflet. Area is the projection viewed along z.

The semiisotropic record still fluctuates as the membrane and box dimensions adjust. We use the 151 frames from 15 to 30 ns of this second stage for the structural summaries and display the complete time series alongside them. The common interval ensures that the different observables refer to the same records, with explicit duration, sampling interval, and leaflet populations. Future comparisons involving temperature, hydration, or lipid chemistry should examine the dimensional relaxation of each system before selecting corresponding analysis intervals. Matching definitions and understanding the state being sampled are what make differences between resulting distributions interpretable.

## One membrane and two areas per lipid

Viewed from above, a planar membrane has projected area equal to the product of the x and y box lengths. Picture two shelves occupying the same footprint but carrying different numbers of books. The common footprint divided by the number on each shelf gives a different average area allocation. Similarly, both membrane leaflets cover the same projected area, but area per lipid must use each leaflet's own molecular count. Dividing 128 by two assumes equal populations of 64. The actual populations here are 66 and 62, so the two denominators should be retained when describing the membrane's two sides.

Use each leaflet’s actual populationEq. 3

![Use each leaflet’s actual population](https://ml-biomat.com/static/agent-math/e8854a3a726d249227fd94d3.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Lx, Ly | Orthogonal box lengths in the membrane plane | nm |
| A | Projected membrane area | nm² |
| N+, N− | Fixed positive-z and negative-z leaflet populations, 66 and 62 | 1 |
| a+, a− | Mean projected area per lipid in each leaflet | nm² |
| +, − | Subscripts distinguish leaflet orientation | 1 |
| =, +, ×, / | Equality, addition, multiplication and division; adjacent symbols multiply | 1 |

Reading the relationshipBoth leaflets share the projected box area; dividing by their own counts gives different mean allocations.

A worked exampleAt A=38.4734 nm², a+=38.4734/66≈0.58293 nm² and a−=38.4734/62≈0.62054 nm².

ConditionsFor projected area of a planar membrane; local molecular area and curved surface area require additional definitions.

The mean projected area over the final 15 ns is 38.473 nm². Division by 66 gives 0.583 nm² for the positive-z leaflet, while division by 62 gives 0.621 nm² for the other leaflet. Their curves rise and fall together because every frame contributes one shared box area and two fixed denominators. The corresponding standard deviations across saved frames are about 0.022 and 0.024 nm². These values describe fluctuations within the record. Area per lipid is an average allocation of a leaflet's total area; individual molecules move through a shared membrane rather than occupy fixed little squares. Local packing requires an additional spatial partitioning definition.

### Leaflet area, phosphate separation, and collective alignment

Fixed 66/62 leaflet memberships; shading marks the 151-frame interval from 15 to 30 ns.

128 Martini 3 DSPC lipids and 768 W beads at 340 K and 1 bar. Thirty ns of isotropic self-assembly is followed by rotation of all positions and velocities to a z-normal membrane and 30 ns of semi-isotropic sampling. Uses PC/bonded v2 lipid parameters.

[Download reference data and complete inputs (ZIP) 5.97 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-dspc-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g15/en/#en-s6)

Thirty ns after rotation: projected areas per lipid using fixed 66/62 memberships, PO4-plane separation and collective alignment. The 15–30 ns interval contains 151 saved times.

Thickness also requires specifying where the ruler is placed. Here it is the separation of the mean PO4 positions in the two leaflets. The program first finds the membrane's periodic midplane from terminal tail positions, places the headgroup coordinates on either side of that center, and then subtracts their leaflet averages. This resolves the seam visible in the assembly snapshots. The shorter straight interval between headgroup layers inside the displayed box can be the water layer, so selecting that interval would measure the wrong region. Locating the tail-rich interior ensures that the measurement follows the same membrane as it crosses a boundary.

Measure headgroup planes across the membrane interiorEq. 4

![Measure headgroup planes across the membrane interior](https://ml-biomat.com/static/agent-math/d32f0d6867dbb3521dbef182.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| dPP | Separation of leaflet mean PO4 planes | nm |
| zᵢ, zⱼ | PO4 normal coordinates unfolded about the periodic terminal-tail midplane | nm |
| i, j | Lipid indices in the two leaflets | 1 |
| N+, N− | Leaflet membership counts, 66 and 62 | 1 |
| Σ, ∈, +, − | Sum over the specified leaflet; set membership; + and − in summation labels identify leaflets, while the central − subtracts | 1 |
| =, / | Equality and division; dividing a sum by population gives its mean | 1 |

Reading the relationshipAverage head coordinates on each side and subtract. Tail-midplane centering makes the separation cross the membrane interior.

A worked exampleIf the mean coordinates are +2.1 and −2.2 nm, dPP=2.1−(−2.2)=4.3 nm.

ConditionsFor this nearly planar membrane, fixed leaflet memberships, and z normal; the observable is specifically PO4-plane separation.

The resulting mean phosphate-plane separation is 4.321 nm, with a frame-to-frame standard deviation of 0.122 nm. Portions of the time series with larger area often have a smaller headgroup separation, consistent with the geometrical idea that lateral spreading can accompany thinning. Molecular tilt, tail bending, and hydration participate as well. A quantitative relationship between these observables would require their joint distribution and temporal correlations; the shapes of two curves alone do not reduce membrane deformation to one fixed-volume mechanism. Here they serve as connected structural measurements whose coordinates, directions, and averaging populations have been specified.

Experimental and computational thicknesses can refer to different boundaries: headgroup density peaks, the hydrophobic core, or a length inferred from fitting scattering data. A useful comparison begins by asking which material the experiment detects and then constructing a corresponding simulated observable. The mean PO4 planes are convenient for following changes within this model. The bead-density profile in the next section adds information beyond two mean positions, including the widths of headgroup layers and the transitions between tail-rich and water-rich regions. Centering each frame also separates internal structure from translation of the membrane as a whole.

## Read the membrane interior through density and orientation

A density profile is built much like counting people in equal sections of a long corridor. Divide the membrane-normal coordinate into 0.1 nm slices. Each slice has volume equal to the current membrane area multiplied by its thickness; the number of beads in the slice divided by that volume gives number density. We count PO4, all tail beads, and W separately, centering every frame on the terminal-tail midplane before averaging over the final 15 ns. This keeps the membrane interior at zero and avoids broadening the headgroup peaks through collective translation. Each frame uses its own area because pressure coupling changes the box.

Divide counts by slice volume, then average framesEq. 5

![Divide counts by slice volume, then average frames](https://ml-biomat.com/static/agent-math/9e894015e70b4cb954e7f164.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| k, f, F | Slice index, frame index, and analysis frame count, 151 | 1 |
| nₖ, f | Selected bead count in slice k of frame f | 1 |
| Af | Projected membrane area in that frame | nm² |
| Δz | Slice width, 0.1 here | nm |
| AfΔz | Slice volume in that frame | nm³ |
| ρ̄ₖ | Mean bead number density | nm⁻³ |
| Σ, 1/F, =, /, × | Frame summation, frame averaging, equality, division and multiplication | 1 |

Reading the relationshipNormalize each frame by its actual slice volume before averaging, retaining area changes under pressure coupling.

A worked exampleWith area 40 nm², slice width 0.1 nm and eight beads, density is 8/(40×0.1)=2 nm⁻³.

ConditionsCount PO4, all tail beads, or W separately after centering. Integration over z gives mean bead count per area; W is counted as beads.

The profile places tail beads in the center, PO4 peaks on both sides, and most water beads farther outside, matching the chemical organization of a bilayer. Curve heights reflect both spatial concentration and the total number of selected beads. Each lipid has one PO4 bead but eight tail beads, so their integrated densities differ accordingly. Integrating number density over z gives the number of beads per projected area, a relation checked by the program. W density counts water beads; nominal water-molecule density requires a factor of four. Electron density and mass density would instead require the corresponding electron or mass weights.

### Bead density and tail alignment inside the membrane

Final 15 ns, centered on the periodic terminal-tail midplane. Density is in nm⁻³; P₂ bars show sample standard deviations of frame-wise molecular averages.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g15/en/#en-s7)

Bead number densities relative to the periodic terminal-tail midplane and P₂ of six adjacent tail-bead links over the final 15 ns. Error bars are sample standard deviations of frame-wise molecular means; link alignment and the molecular-axis eigenvalue are distinct definitions.

Tail orientation supplies another view of the interior. Take a line joining two neighboring tail beads, measure its angle to the z normal, and convert that angle to P₂. A bond parallel or antiparallel to the normal gives 1, while a bond lying in the membrane plane gives −0.5. For an isotropic three-dimensional distribution, the average squared cosine is one third, giving average P₂ equal to zero. Calculate the squared cosine for each bond before averaging over molecules and frames. Averaging angles first and then squaring their cosine produces a different quantity, particularly when opposing leaflets contribute opposite directions.

Average squared projections of individual bondsEq. 6

![Average squared projections of individual bonds](https://ml-biomat.com/static/agent-math/fd8cee8e4e7ddfbb77f3af22.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| P₂ | Second-rank orientation parameter relative to the membrane normal | 1 |
| θ | Angle between a coarse-grained tail-bond vector and the +z normal | ° |
| b, bz | Vector joining adjacent tail beads and its z component | nm |
| ‖b‖ | Vector magnitude | nm |
| cos θ, cos² θ | Cosine formed from the length ratio and its square | 1 |
| ⟨·⟩ | Compute for each bond, then average over selected molecules and frames | 1 |
| 3, 1, 2 | Dimensionless constants setting the orientation scale | 1 |
| =, −, /, ², ‖·‖ | Equality, subtraction, division, squaring and vector magnitude | 1 |

Reading the relationshipSquaring treats opposite directions equally. The isotropic mean squared cosine is 1/3, so the expression gives zero in that limit.

A worked exampleBoth 0° and 180° give one; 90° gives −0.5. Equal 0° and 180° directions have mean P₂=1 although their mean angle is 90°.

ConditionsComputed separately for six tail connections with z as the membrane normal; averaging angles first changes the observable.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g15/en/#en-s7)

Figure 3 · Directions at 0° and 180° both follow the normal and give P₂=1. A 90° direction lies in the plane and gives −0.5. The three-dimensional isotropic average is zero.

For the two tails, the C1–C2 bonds nearer the connecting region have mean P₂ values of approximately 0.571 and 0.597. The terminal C3–C4 bonds give about 0.432 and 0.430. The lower terminal values indicate more dispersed squared projections onto the normal, consistent with greater freedom for the ends to bend. The plotted bars show the standard deviation among 151 frame means, each already averaged over 128 molecules. They describe fluctuations in the sampled record; temporal correlation also enters uncertainty of the mean. Local tail-bond P₂ and the earlier whole-lipid alignment S use different vectors and should retain those separate definitions.

Four equal-weight directions: compare averaging evaluated orientations with evaluating an average angle.

[Figure: Four directions relative to the membrane normal](https://ml-biomat.com/tutorials/molecular-dynamics/g15/en/#en-s7)

The dashed line indicates the membrane plane and vertical lines its normal. Vectors have equal weight; 0° and 180° share the same squared axial projection.

The interaction places four equally weighted directions in one plane to make the order of operations visible. In the same-angle setting, all four directions have angle θ. In the opposing setting, half have angle θ and half have angle 180°−θ. At zero degrees, two arrows point upward and two downward, yet P₂ remains 1. At 90°, all lie in the membrane plane and P₂ becomes −0.5. This is a geometrical example of the angular definition. Recorded molecular directions occupy three-dimensional space, and applying the same operation to each selected vector handles both leaflets and different positions along each tail.

## Turn an assembly record into a model for further study

The complete analysis requires the TPR and XTC files from the two stages. It first checks the 128 twelve-bead DSPC molecules, 768 W beads, and their bead ordering. It then follows the topology connections to reconstruct each molecule across periodic boundaries. Checking every connection and cycle prevents a boundary-cut tail from being interpreted as an unusually stretched molecule. Whole-molecule coordinates supply directions and bond angles, while periodic centering supplies positions for density calculations. Time series, numerical summaries, and plots are saved together, linking area, thickness, and orientation to the same frames and stated analysis window.

### Complete assembly and bilayer analysis

```
"""Read DSPC assembly and bilayer trajectories and measure their organization.

python analyze_lipids.py --assembly records/assembly --bilayer records/bilayer \
    --out analysis --language en
The two directories contain assembly.tpr/xtc and bilayer.tpr/xtc respectively.
Dependencies: MDAnalysis, NumPy, Matplotlib. MDAnalysis lengths are angstrom.
"""
from pathlib import Path
import argparse
import csv
import json
import numpy as np
import MDAnalysis as mda
from MDAnalysis.lib.distances import minimize_vectors
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


def plans(group):
    index = {int(x): i for i, x in enumerate(group.indices)}
    edges = np.array([[index[int(a)], index[int(b)]] for a, b in group.bonds.indices])
    graph = [[] for _ in group]
    for k, (a, b) in enumerate(edges):
        graph[a].append((b, k, 1)); graph[b].append((a, k, -1))
    queue, seen, plan = [0], {0}, []
    for a in queue:
        for b, k, sign in graph[a]:
            if b not in seen:
                queue.append(b); seen.add(b); plan.append((a, b, k, sign))
    if len(seen) != 12:
        raise ValueError("Each DSPC molecule must have a connected 12-bead graph")
    return edges, plan


def reconstruct(raw, box, edges, plan):
    # Apply one identical molecular topology to all 128 lipids in this frame.
    delta = raw[:, edges[:, 1]]-raw[:, edges[:, 0]]
    delta = minimize_vectors(delta.reshape(-1, 3), box).reshape(delta.shape)
    xyz = np.empty_like(raw, dtype=float); xyz[:, 0] = raw[:, 0]
    for a, b, k, sign in plan:
        xyz[:, b] = xyz[:, a]+sign*delta[:, k]
    actual = xyz[:, edges[:, 1]]-xyz[:, edges[:, 0]]
    if np.max(np.linalg.norm(actual-delta, axis=-1)) > .005:
        raise ValueError("Periodic bond-cycle closure failed")
    longest = float(np.linalg.norm(actual, axis=-1).max()/10)
    if longest > .8:
        raise ValueError("A coarse-grained bonded distance exceeds 0.8 nm")
    return xyz/10, longest


def statistics(a):
    return {"mean": float(np.mean(a)), "sd": float(np.std(a, ddof=1))}


def save(fig, path):
    fig.savefig(path.with_suffix(".svg"))
    fig.savefig(path.with_suffix(".png"), dpi=150)
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--assembly", type=Path, default=Path("records/assembly"))
    p.add_argument("--bilayer", type=Path, default=Path("records/bilayer"))
    p.add_argument("--out", type=Path, default=Path("analysis"))
    p.add_argument("--language", choices=["zh", "en"], default="en")
    args = p.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    zh = args.language == "zh"
    available = {f.name for f in font_manager.fontManager.ttflist}
    families = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC",
                "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else ["DejaVu Sans"]
    plt.rcParams.update({"font.family": [n for n in families if n in available],
                         "font.size": 14, "axes.labelsize": 15,
                         "svg.fonttype": "path", "axes.unicode_minus": False,
                         "axes.spines.top": False, "axes.spines.right": False})
    expected_names = ["NC3", "PO4", "GL1", "GL2", "C1A", "C2A", "C3A", "C4A",
                      "C1B", "C2B", "C3B", "C4B"]
    tail_pairs = [(4, 5), (5, 6), (6, 7), (8, 9), (9, 10), (10, 11)]
    arrays = {}; snapshots = []; maximum_bond = 0.; initial_side = None
    density_edges = np.linspace(-4, 4, 81)
    density = np.zeros((3, 80)); expected_integral = np.zeros(3)
    order = []; leaflet_changes = 0; late_frames = 0
    for name, folder in [("assembly", args.assembly), ("bilayer", args.bilayer)]:
        u = mda.Universe(str(folder/f"{name}.tpr"), str(folder/f"{name}.xtc"))
        lipids = u.select_atoms("resname DSPC")
        water = u.select_atoms("resname W")
        if len(u.atoms) != 2304 or len(lipids) != 1536 or len(water) != 768:
            raise ValueError("Expected 128 DSPC molecules and 768 W beads")
        if list(lipids.names) != expected_names*128 or abs(sum(lipids.charges)) > 1e-5:
            raise ValueError("DSPC bead ordering or charge differs from this model")
        edges, plan = plans(lipids[:12]); rows = []
        for frame in u.trajectory:
            if not np.allclose(frame.dimensions[3:], 90):
                raise ValueError("This analysis uses the recorded orthorhombic boxes")
            box = frame.dimensions[:3].astype(float)/10
            xyz, longest = reconstruct(lipids.positions.astype(float).reshape(128, 12, 3), frame.dimensions, edges, plan)
            maximum_bond = max(maximum_bond, longest)
            head = xyz[:, 1]; tail = xyz[:, [7, 11]]
            direction = head-tail.mean(axis=1)
            direction /= np.linalg.norm(direction, axis=1)[:, None]
            q = 1.5*direction.T@direction/128-.5*np.eye(3)
            eig, axes = np.linalg.eigh(q); axis = axes[:, -1]
            row = [float(frame.time), float(eig[-1]), *np.abs(axis)]
            if name == "assembly" and frame.frame in [0, 50, 150, 300]:
                snapshots.append({"time_ps": float(frame.time), "box_nm": box.tolist(),
                                  "lipid_coordinates_nm": (xyz % box).tolist(),
                                  "water_coordinates_nm": (water.positions/10 % box).tolist()})
            if name == "bilayer":
                side = direction[:, 2] > 0
                if initial_side is None:
                    initial_side = side.copy()
                    if [int(side.sum()), int((~side).sum())] != [66, 62]:
                        raise ValueError("Expected the recorded 66/62 leaflet membership")
                leaflet_changes += int(np.sum(side != initial_side))
                # A circular mean locates the tail midplane across the periodic seam.
                phase = np.mean(np.exp(2j*np.pi*tail[:, :, 2]/box[2]))
                if abs(phase) < .1:
                    raise ValueError("Tail positions do not define one clear midplane")
                center = np.angle(phase)*box[2]/(2*np.pi)
                hz = head[:, 2]-center; hz -= box[2]*np.round(hz/box[2])
                area = box[0]*box[1]
                thickness = hz[initial_side].mean()-hz[~initial_side].mean()
                row += [float(area), float(area/66), float(area/62), float(thickness)]
                if frame.time >= 15000:
                    late_frames += 1
                    groups = [xyz[:, 1, 2], xyz[:, 4:, 2].ravel(), water.positions[:, 2]/10]
                    for k, z in enumerate(groups):
                        centered = z-center; centered -= box[2]*np.round(centered/box[2])
                        counts, _ = np.histogram(centered, bins=density_edges)
                        if counts.sum() != len(z):
                            raise ValueError("Density interval does not cover all selected beads")
                        density[k] += counts/(area*np.diff(density_edges))
                        expected_integral[k] += len(z)/area
                    bond = np.stack([xyz[:, b]-xyz[:, a] for a, b in tail_pairs], axis=1)
                    cos2 = bond[:, :, 2]**2/np.sum(bond*bond, axis=-1)
                    order.append((1.5*cos2-.5).mean(axis=0))
            rows.append(row)
        values = np.asarray(rows)
        if len(values) != 301 or not np.allclose(values[:, 0], np.arange(301)*100):
            raise ValueError("Expected 301 saved frames spanning 0–30000 ps")
        arrays[name] = values
        fields = ["time_ps", "nematic_eigenvalue", "axis_abs_x", "axis_abs_y", "axis_abs_z"]
        if name == "bilayer":
            fields += ["area_nm2", "area_positive_nm2", "area_negative_nm2", "phosphate_separation_nm"]
        with (args.out/f"{name}.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f); writer.writerow(fields); writer.writerows(values)
    density /= late_frames; expected_integral /= late_frames
    actual_integral = np.sum(density*np.diff(density_edges), axis=1)
    if not np.allclose(actual_integral, expected_integral, rtol=1e-12):
        raise ValueError("Density integral check failed")
    order = np.asarray(order); late = arrays["bilayer"][150:]
    summary = {"model": "128 DSPC, Martini 3 regular v3.0.0 + PC/bonded v2; 768 W; 340 K",
               "frames_per_stage": 301, "bilayer_late_frames": late_frames,
               "bilayer_window_ps": [15000, 30000], "leaflet_counts": [66, 62],
               "leaflet_orientation_changes": leaflet_changes, "maximum_bond_nm": maximum_bond,
               "assembly_final_nematic_eigenvalue": arrays["assembly"][-1, 1],
               "assembly_final_axis_absolute": arrays["assembly"][-1, 2:5].tolist(),
               "bilayer_last15ns": {n: statistics(late[:, j]) for n, j in [
                   ("nematic_eigenvalue", 1), ("area_nm2", 5), ("area_positive_nm2", 6),
                   ("area_negative_nm2", 7), ("phosphate_separation_nm", 8)]},
               "tail_bond_labels": [f"{expected_names[a]}–{expected_names[b]}" for a, b in tail_pairs],
               "tail_bond_P2_mean": order.mean(axis=0).tolist(),
               "tail_bond_P2_frame_sd": order.std(axis=0, ddof=1).tolist(),
               "density_integral_per_nm2": actual_integral.tolist(),
               "density_expected_mean_count_over_area_per_nm2": expected_integral.tolist(),
               "sd_definition": "Sample standard deviation across saved frames, ddof=1"}
    (args.out/"summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (args.out/"snapshots.json").write_text(json.dumps(snapshots), encoding="utf-8")
    np.savetxt(args.out/"density.csv", np.column_stack(((density_edges[:-1]+density_edges[1:])/2, density.T)),
               delimiter=",", header="z_nm,PO4_per_nm3,tail_beads_per_nm3,W_per_nm3", comments="")
    fig, axs = plt.subplots(2, 2, figsize=(12, 10), constrained_layout=True)
    for ax, frame in zip(axs.ravel(), snapshots):
        xyz = np.asarray(frame["lipid_coordinates_nm"]); w = np.asarray(frame["water_coordinates_nm"])
        ax.scatter(w[:, 0], w[:, 1], s=7, c="#aabfce", alpha=.35)
        ax.scatter(xyz[:, 4:, 0], xyz[:, 4:, 1], s=8, c="#d2974f", alpha=.45)
        ax.scatter(xyz[:, 1, 0], xyz[:, 1, 1], s=27, c="#147d92", edgecolors="none")
        ax.set(xlabel="x / nm", ylabel="y / nm", xlim=(0, frame["box_nm"][0]),
               ylim=(0, frame["box_nm"][1]), aspect="equal", title=f'{frame["time_ps"]/1000:g} ns')
    fig.suptitle("自组装轨迹：磷酸头基、尾珠与水珠的 xy 投影" if zh else
                 "Assembly trajectory: xy projections of phosphate heads, tails, and water", fontsize=16)
    save(fig, args.out/"assembly-structure")
    a = arrays["assembly"]
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True, constrained_layout=True)
    axs[0].plot(a[:, 0]/1000, a[:, 1], c="#147d92", lw=1.8)
    axs[0].set_ylabel("最大取向特征值 S" if zh else "Largest alignment\neigenvalue S")
    for j, color in enumerate(["#c66b43", "#147d92", "#7566a8"]):
        axs[1].plot(a[:, 0]/1000, a[:, j+2], label=f"|n{'xyz'[j]}|", color=color, lw=1.4)
    axs[1].set_ylabel("主轴单位向量的绝对分量" if zh else "Principal-axis components\n(absolute values)")
    axs[1].set_xlabel("自组装阶段时间 / ns" if zh else "Assembly-stage time / ns")
    axs[1].legend(ncol=3); axs[0].set_title("共同朝向随聚集逐渐出现" if zh else "A common orientation develops during aggregation")
    for ax in axs: ax.grid(alpha=.15)
    save(fig, args.out/"assembly-order")
    b = arrays["bilayer"]
    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True, constrained_layout=True)
    for j, color, label in [(6, "#147d92", "+z: 66"), (7, "#c66b43", "−z: 62")]:
        axs[0].plot(b[:, 0]/1000, b[:, j], c=color, lw=1.5, label=label)
    axs[0].set_ylabel("每脂质投影面积 / nm²" if zh else "Projected area per lipid\n/ nm²"); axs[0].legend(ncol=2)
    axs[1].plot(b[:, 0]/1000, b[:, 8], c="#7566a8", lw=1.5)
    axs[1].set_ylabel("磷酸面间距 / nm" if zh else "Phosphate-plane\nseparation / nm")
    axs[2].plot(b[:, 0]/1000, b[:, 1], c="#147d92", lw=1.5)
    axs[2].set_ylabel("最大取向特征值 S" if zh else "Largest alignment\neigenvalue S")
    axs[2].set_xlabel("半各向同性阶段时间 / ns" if zh else "Semiisotropic-stage time / ns")
    axs[0].set_title("同一片膜，两种叶片分母" if zh else "One membrane area, two leaflet populations")
    for ax in axs: ax.axvspan(15, 30, color="#e8d5ac", alpha=.2); ax.grid(alpha=.15)
    save(fig, args.out/"bilayer-geometry")
    fig, axs = plt.subplots(2, 1, figsize=(12, 9), constrained_layout=True)
    centers = (density_edges[:-1]+density_edges[1:])/2
    labels = ["磷酸珠 PO4", "全部尾珠", "水珠 W"] if zh else ["Phosphate beads PO4", "All tail beads", "Water beads W"]
    for values, label, color in zip(density, labels, ["#147d92", "#c59148", "#7896b0"]):
        axs[0].plot(centers, values, label=label, c=color, lw=2)
    axs[0].set(xlabel="距尾端中面的 z / nm" if zh else "z from terminal-tail midplane / nm",
               ylabel="珠数密度 / nm⁻³" if zh else "Bead number density / nm⁻³")
    axs[0].legend(ncol=3, loc="lower center", bbox_to_anchor=(.5, 1.01), fontsize=12)
    positions = np.arange(6)
    axs[1].errorbar(positions, order.mean(axis=0), yerr=order.std(axis=0, ddof=1), fmt="o", c="#147d92", capsize=5)
    axs[1].set_xticks(positions, summary["tail_bond_labels"], rotation=15)
    axs[1].set_ylim(-.5, 1); axs[1].set_ylabel("尾链键取向 P₂" if zh else "Tail-bond orientation P₂")
    axs[1].set_title("误差棒为逐帧均值的标准差" if zh else "Bars show the standard deviation of frame means")
    for ax in axs: ax.grid(alpha=.15)
    save(fig, args.out/"bilayer-profile-order")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

Read both native TPR/XTC pairs, reconstruct molecular connectivity, and produce bilingual plots and numerical records.

Place assembly.tpr and assembly.xtc in records/assembly, and bilayer.tpr and bilayer.xtc in records/bilayer, then run the analysis command below. The program produces four sets of figures: assembly snapshots, the development of collective orientation, membrane geometry through time, and density with local tail orientation. Language selection changes labels while preserving numerical definitions. All 602 frames across the two stages pass the connectivity checks, and the density integrals agree with the frame-averaged bead counts divided by area. These relationships remain useful when changing the analysis interval or slice thickness because they connect the output directly to counting and units.

### Generate figures in both languages

```
python analyze_lipids.py --assembly records/assembly --bilayer records/bilayer --out analysis-zh --language zh
python analyze_lipids.py --assembly records/assembly --bilayer records/bilayer --out analysis-en --language en
```

The record directories contain assembly.tpr/xtc and bilayer.tpr/xtc respectively; both runs calculate the same numerical values.

The recorded model yields a nearly planar bilayer containing 128 lipids, with 66 in one leaflet and 62 in the other. Over the final 15–30 ns interval of the continuation, its mean projected area is 38.473 nm², phosphate-plane separation is 4.321 nm, and whole-lipid alignment S is about 0.836. Bead-density profiles resolve the water, headgroup, and tail regions. Together, these measurements connect morphology, molecular populations, and internal arrangement. They provide an inspectable starting point for adding polymer chains to the membrane, changing headgroup composition, or studying crowding at a membrane surface.

The meaning of coarse-grained time follows from the retained degrees of freedom. Averaging out rapid internal motions changes friction, energy variations, and some rearrangement pathways, with effects that can differ between processes. Each reported 30 ns stage is an integration-time record. Relating diffusion or assembly rates to a real material requires a process-specific comparison with suitable experiments or a finer-resolution model. Structural comparisons also depend on matched conditions: temperature, hydration, lipid parameter version, leaflet populations, and pressure treatment jointly specify this membrane. Keeping these quantities explicit makes it possible to connect a material modification to a clearly defined scientific question.

A useful next comparison can be small and specific. Keeping lipid chemistry and temperature fixed while adding water would test changes in area, density, and tail orientation. Alternatively, preparing two equally populated leaflets would examine the effect of population asymmetry. These designs change different physical conditions and call for their own replicates and statistical comparisons. The following grafted-polymer example adds flexible chains to a defined membrane surface, extending the question of area per lipid into the number of chains attached per unit area. Resolution, leaflet membership, and the membrane-normal coordinate established here will continue to determine what those new measurements mean.

## Further Reading and Open Materials

- [Lipid bilayers – Part I: Self-assembly](https://cgmartini.nl/docs/tutorials/Martini3/LipidsI/index.html) · Luís Borges-Araújo; Manuel N. Melo; Martini Force Field Developers Team · MIT (website source and documentation)

  DSPC random assembly, normal rotation, semiisotropic continuation, structural workflow, and inputs.

  Fixed seeds and output interval; pressure update every five steps; actual 66/62 populations; periodic centering, full bilingual analysis, and symbol explanations.
- [Martini force fields and Martini 3 Lipid Parameters](https://github.com/Martini-Force-Field-Initiative/M3-Lipid-Parameters) · Martini Force Field Initiative; Kasper B. Pedersen and contributors · Apache-2.0

  DSPC from the 2025 bonded-v2 and PC-v2 files, combined with Martini 3 base v3.0.0 and solvent v1.

  Force-field numerical parameters retained; composition and run settings follow this example.
- [Martini Force Fields](https://github.com/Martini-Force-Field-Initiative/martini-forcefields) · Martini Force Field Initiative · Apache-2.0

  Martini 3 base bead interactions and W solvent parameters.

  Numerical parameters unchanged.
- [Coarse Grained Model for Semiquantitative Lipid Simulations (2004)](https://doi.org/10.1021/jp036508g) · Siewert J. Marrink; Alex H. de Vries; Alan E. Mark · Copyright American Chemical Society; cited historical facts

  History of lipid coarse graining and self-assembly models.

  Concept diagrams drawn for this lesson; history organized around the scientific question.
- [Martini 3: A General Purpose Force Field for Coarse-Grained Molecular Dynamics (2021)](https://doi.org/10.1038/s41592-021-01098-3) · Paulo C. T. Souza and colleagues · Article cited; author manuscript publicly accessible

  Background on Martini 3 resolution, bead types, and effective interactions.

  Concepts explained through the present model.
- [The Martini 3 Lipidome: Expanded and Refined Parameters Improve Lipid Phase Behavior (2025)](https://doi.org/10.1021/acscentsci.5c00755) · Kasper B. Pedersen and colleagues · CC BY 4.0

  Physical meaning of revised lipid-tail mapping and parameters.

  Explanations and conceptual diagrams written for this lesson.
