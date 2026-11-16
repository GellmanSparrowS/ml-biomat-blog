# How Polymers Extend and Coil in Water

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g14/en/
Language: en

Build hydroxyl-ended PEG from its chemical connectivity, then use two recorded trajectories to understand chain dimensions, conformational distributions, and hydration.

## How large is a flexible chain?

Place a headphone cable on a table and measure the distance between its ends. Rearranging the cable changes that distance without making the cable itself longer or shorter. A flexible polymer in water has the same distinction: its number of atoms, the distance followed along its backbone, and the space it occupies at a particular moment describe different things. This matters when designing materials. For a water-loving chain attached to a particle or membrane, useful questions include how far it reaches into the water, how many water molecules lie nearby, and where neighboring chains begin to encounter one another. Chemical composition supplies part of the answer; the chain's spatial arrangement supplies another.

Our starting material is polyethylene glycol, usually abbreviated PEG. Its backbone repeatedly contains two carbon atoms and one oxygen atom, with hydrogen atoms attached to the carbons. A chain with two hydroxyl ends can be written HO–(CH₂–CH₂–O)ₙ–H. The subscript n counts the repeated group; the leading HO and final H complete the two ends. Oxygen has a physical role here: it changes the charge distribution and provides sites for directional interactions with water. At the same time, rotations around many single bonds allow the backbone to bend. The dimensions of a dissolved chain therefore emerge from local chemistry, molecular connectivity, and the surrounding solvent acting together.

We will examine one short chain with n equal to 16, surrounded by 6996 explicit water molecules at 300 K and 1 bar. Explicit water means that water molecules have coordinates and move during the calculation, rather than appearing only as a label attached to the polymer environment. The system contains 21103 atomic sites, of which 115 belong to PEG. Its size makes the complete construction and analysis manageable. It also keeps the model easy to identify: there is one chain length, two equivalent hydroxyl ends, and no salt, surface, or second polymer chain. We can first connect the observed changes in size to this particular molecule and its water environment.

Sixteen repeat units make a relatively short oligomeric chain. It nevertheless contains the connectivity, conformational changes, and statistical questions that become central to longer polymers. PEG and PEO are names commonly used for polyethers with the same repeat chemistry, with usage also influenced by molecular weight and application. Here PEG identifies a molecule with specified hydroxyl ends and an exact repeat count; PEO is also the name of an internal building block in the parameter library. Keeping the material name, chemical repeat count, and software block name separate will help us extend the model later without accidentally changing its chemical identity.

By the end of this chapter, you will be able to generate the topology and initial coordinates, explain why two independent simulation branches develop different shape histories, and measure the radius of gyration, end-to-end distance, and number of nearby waters from recorded trajectories. Each measurement should remain connected to a picture: which atoms can change it, why two size measures may suggest different impressions, and how the observation window affects their averages. The cable analogy clarifies geometry. The molecular model adds thermal motion and molecular interactions, which continually reshape a chain in solution.

## Connectivity and flexibility: why a long molecule coils

Drawing a long chain on a screen now seems straightforward. In the early twentieth century, whether rubber and cellulose contained enormous molecules or aggregates of smaller molecules was a substantive chemical question. In 1920, Hermann Staudinger proposed long molecules containing many units connected through ordinary covalent bonds. Chemical transformations and physical measurements helped develop that interpretation. Hydrogenation of rubber addressed an aggregation explanation associated with double bonds: removing those double bonds was expected to disrupt the proposed small-unit aggregates, whereas the experimental behavior encouraged a different account of the material's connectivity. Distinguishing a connected molecule from a collection of neighboring molecules made polymer structure a chemically testable model.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g14/en/#en-s2)

Figure 1 · Staudinger’s long-molecule interpretation distinguished covalent connectivity from small-unit aggregation. The upper panels illustrate the two structural interpretations; the lower panel shows different spatial conformations of one bond graph.

In his 1953 Nobel lecture, Staudinger placed proteins, nucleic acids, polysaccharides, and synthetic polymers within a shared view of macromolecular chemistry. Familiar atoms and bonds create new questions when assembled into large molecular structures. This idea has a direct counterpart in a topology file. Two atoms may appear close together because thermal motion has brought them near each other; the connections explicitly listed in the topology carry the corresponding bonded interactions. When one chain end approaches the other, the molecule does not automatically become a ring. A cyclization study would require the appropriate chemical connectivity and a model for the process being investigated.

Being connected does not make a molecule rigid. Imagine a sequence of short rods with preferred lengths and preferred angles between neighboring rods. Rotation around certain single bonds adds further ways to change the shape. A dihedral angle uses four consecutive atoms to describe the relative orientation of two atomic planes. Changing one dihedral redirects the section of chain beyond it; many local changes can transform an extended chain into a curved one. In real PEG, different torsions have different energies, and atoms occupy space. Consequently, the many lines we can draw on paper are not all equally accessible molecular conformations.

The number of possible arrangements also matters. Keeping many successive segments approximately aligned permits relatively few combinations of directions. Allowing bends provides many more detailed arrangements with similar overall dimensions. This multiplicity is related to entropy, which we can initially understand as the variety of microscopic arrangements compatible with a broader description. A chain can often be curved without an external force compressing it, because thermal motion explores numerous accessible arrangements. A particular curved conformation may still have a relatively high energy. Its statistical weight depends on both interactions and the number of arrangements associated with the state being considered.

Water changes this balance further. PEG oxygen atoms interact with water, while distant parts of the chain can approach each other. One bend may expose sites to solvent, whereas another may crowd a local region. Solvent quality describes how the solvent influences statistical chain dimensions, with chain length, temperature, model chemistry, and sampling all entering the interpretation. An extended snapshot establishes the shape of that frame. A statement about swelling across a family of long chains calls for many conformations and comparisons across lengths. We will first establish the measurements needed for that comparison, then treat chain length as a research variable.

## Specify the repeat units and ends before building the molecule

Polyply separates two connected tasks: generating a topology from molecular blocks and linking rules, and assigning starting coordinates to the atoms. The first determines connectivity and interaction parameters; the second determines the initial spatial arrangement. This distinction is useful. An attractive three-dimensional structure with the wrong terminal chemistry is a different molecule. A correct topology with unfavorable initial contacts can instead be improved through suitable construction and relaxation. We use the oplsaaLigParGen library from a fixed source version, retaining its PEO and OHter blocks and the interaction definitions that connect those blocks.

The sequence deserves particular attention: OHter:1 PEO:15 OHter:1. Each internal PEO block contains two carbons, one oxygen, and four hydrogens, giving C₂H₄O. Each OHter block contains one carbon, one oxygen, and three hydrogens, giving CH₃O. Together, the two terminal blocks contain one C₂H₄O unit plus H₂O. Therefore, 15 internal blocks and these two ends produce a hydroxyl-ended chain with chemical repeat count 16 and formula C₃₂H₆₆O₁₇. The software residue count is 17, the chemical repeat count is 16, and the atom count is 115. These numbers describe different aspects of the same molecule.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g14/en/#en-s3)

Figure 2 · OHter includes a carbon atom as well as oxygen and hydrogen. Combining two terminal blocks with 15 internal PEO blocks yields hydroxyl-ended PEG with chemical repeat count 16.

Check atom count and molar mass firstEq. 1

![Check atom count and molar mass first](https://ml-biomat.com/static/agent-math/8cc9941aa31fd73c5d5fabf6.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| n | Chemical C₂H₄O repeat count | 1 |
| Nₐₜₒₘ | Total atom count of the hydroxyl-ended chain | 1 |
| 7, 3 | Seven atoms per repeat; three additional terminal-completion atoms | 1 |
| M | Molar mass of the complete molecule | g mol⁻¹ |
| Mᴇᴏ | Molar mass of C₂H₄O, 44.053 | g mol⁻¹ |
| Mₑₙd | Molar mass of the H₂O terminal completion, 18.015 | g mol⁻¹ |
| =, +, × | Equality, addition, and multiplication of adjacent symbols; operators are dimensionless | 1 |

Reading the relationshipAdding the element counts in C₂ₙH₄ₙ₊₂Oₙ₊₁ gives 7n+3 atoms; adding their mass contributions gives molar mass.

A worked exampleFor n=16, the atom count is 7×16+3=115 and M=16×44.053+18.015=722.863 g/mol. Two OHter blocks and 15 PEO blocks give the same element counts.

ConditionsFor the neutral linear PEG with two hydroxyl ends used here; recount elements after changing terminal chemistry.

The molar mass can be checked directly from the element counts. One C₂H₄O unit contributes approximately 44.053 g/mol, while the terminal completion contributes 18.015 g/mol. For n equal to 16, the total is approximately 722.863 g/mol. Molar mass describes the mass of one mole of these molecules. The atomic masses used to locate the center of mass of an individual simulated chain are expressed in u. Their numerical connection follows from the definitions of a mole and the atomic mass unit. Within the radius-of-gyration calculation, the important requirement is a consistent set of atomic masses: 115 atoms are not 115 equally weighted beads.

The following two topology files serve the dry construction and solvated simulation stages. The first, polymer.top, contains one PEG molecule so that Polyply can generate its starting coordinates. The second, topol.top, also includes SPC/E water parameters; solvation subsequently supplies the water count. The parameter-generation command writes PEG.itp, containing atom types, partial charges, bonds, angles, and dihedrals. It uses the OPLS-AA interaction family and the LigParGen charges retained in the library. The force-field library, interblock rules, and water model jointly specify the calculation. Changing one of these components changes the model even if the molecule continues to be called PEG.

### System topology for the dry chain

```
#include "oplsaa.ff/forcefield.itp"
#include "PEG.itp"
[ system ]
Hydroxyl-ended PEG
[ molecules ]
PEG 1
```

Defines one PEG molecule for initial coordinate generation.

### System topology for the aqueous model

```
#include "oplsaa.ff/forcefield.itp"
#include "PEG.itp"
#include "oplsaa.ff/spce.itp"
[ system ]
Hydroxyl-ended PEG in SPC/E water
[ molecules ]
PEG 1
```

Solvation adds the actual water count to the molecules section.

Before building the chain, install the pinned Polyply version and its dependencies using the [modeling environment on the preparation page](https://ml-biomat.com/tutorials/molecular-dynamics/s00/en/#en-modeling). This example uses source commit 38d4d5424e1ef35c86e7cb8532fbd86ecf997221. The small wrapper sets both Python and NumPy random seeds before invoking Polyply's coordinate-generation entry point. The seed selects the random sequence used to construct this starting arrangement. Save the following files alongside the topologies and the oplsaa.ff parameter directory, then run bash generate.sh to create PEG.itp and PEG.gro. Recording the coordinate seed makes the starting model traceable; the conformations visited during molecular dynamics are subsequently governed by the force field and simulation conditions.

### Set the coordinate-construction seed

```
import random,sys,runpy,shutil
import numpy as np
seed=int(sys.argv[1]);random.seed(seed);np.random.seed(seed)
entry=shutil.which('polyply');assert entry
sys.argv=[entry,*sys.argv[2:]];runpy.run_path(entry,run_name='__main__')
```

Initialize Python and NumPy random generators before calling the installed Polyply entry point.

### Generate the PEG16 topology and initial coordinates

```
#!/usr/bin/env bash
set -euo pipefail
polyply gen_params -lib oplsaaLigParGen -o PEG.itp -name PEG -seq OHter:1 PEO:15 OHter:1 > topology-generation.log 2>&1
python seeded_polyply.py 20261416 gen_coords -p polymer.top -o PEG.gro -name PEG -box 6 6 6 > coordinate-generation.log 2>&1
```

Run bash generate.sh beside the topologies and oplsaa.ff directory in the prepared Polyply environment.

## Give the same chain two independent motion histories

The generated chain is centered in a cubic box with side length 6 nm and then surrounded by water. Its initial volume is 216 nm³. Periodic boundaries connect the box to neighboring images in all three directions. There must be space for both the chain and its surrounding solvent. A small radius of gyration in one frame alone does not settle the box-size question, because the ends can extend and the molecule can approach its periodic images. The complete chain must be reconstructed before examining its span and image separation. Across the recorded trajectories, the minimum atom-to-atom distances between PEG and a nonzero periodic image were approximately 3.139 and 3.313 nm, exceeding the 1.0 nm short-range cutoff. This check concerns direct short-range contacts; electrostatics still uses a periodic long-range treatment.

Energy minimization first relaxes unfavorable local contacts introduced during construction. This preparation stage uses flexible water geometry and unconstrained steepest descent. Molecular dynamics then restores rigid SPC/E water and constraints on covalent bonds involving hydrogen. These constraints suppress fast bond-length vibrations and support the 2 fs time step used here. Bond angles, dihedrals, and overall molecular motion still allow the chain to change shape. Position restraints are different: they pull selected atoms toward reference positions. The PEG dynamics in this example has no position restraints, so the chain is free to move away from its initially generated outline.

The common minimized structure is divided into two simulation branches. Each branch undergoes 100 ps of constant-volume thermal preparation, 200 ps of temperature-and-pressure preparation, and 2 ns of production dynamics. Chemistry, force field, water count, and target conditions are identical; initial velocities and thermostat random seeds differ. Because the branches share the minimized geometry but undergo separate preparation histories, their first production frames can already have different shapes. This design reveals variability associated with different motion histories. For slower conformational processes, additional branches initialized from substantially different conformations can extend the range of starting conditions being explored.

The v-rescale thermostat maintains temperature near 300 K. An isotropic C-rescale barostat adjusts the volume while sampling around a pressure target of 1 bar. Isotropic scaling changes all three box lengths by the same factor, appropriate for this solution without a prescribed interface direction. PME handles long-range electrostatics; the real-space electrostatic and van der Waals cutoffs are 1.0 nm. The van der Waals potential is shifted, and an energy-and-pressure dispersion correction is included. These settings work together. A different solvent, parameter family, or model resolution calls for checking their compatibility as a set, rather than treating one cutoff value as a universal polymer setting.

### Write every MDP parameter file

```
"""Write the complete PEG16 simulation settings for two velocity histories.
Run: python write_parameters.py [--out INPUT_DIRECTORY]
"""
from pathlib import Path
import argparse

EM = """integrator = steep
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
"""

NVT = """integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 2500
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
nsteps = 50000
continuation = no
pcoupl = no
gen-vel = yes
gen-temp = 300
gen-seed = 20263161
ld-seed = 20264161
"""

NPT = """integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 2500
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
nsteps = 100000
ld-seed = 20265161
"""

MD = """integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 2500
nstenergy = 1000
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
nsteps = 1000000
ld-seed = 20266161
"""

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("."))
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    (args.out/"em.mdp").write_text(EM, encoding="utf-8", newline="\n")
    for replica in [1, 2]:
        replacements = {"20263161": str(20263160+replica),
                        "20264161": str(20264160+replica),
                        "20265161": str(20265160+replica),
                        "20266161": str(20266160+replica)}
        for stage, template in [("nvt", NVT), ("npt", NPT), ("md", MD)]:
            content = template
            for old, new in replacements.items():
                content = content.replace(old, new)
            (args.out/f"{stage}-{replica}.mdp").write_text(content, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
```

Run python write_parameters.py. Complete minimization, NVT, NPT and production parameters are included, with specified seeds for each replica.

The parameter-writing script creates the minimization file and all MDP files needed for both branches, assigning their specified random seeds. During production, coordinates are saved every 2500 steps. Multiplying 2500 by 2 fs gives a 5 ps interval, so a 2 ns record contains 401 frames from 0 to 2000 ps, including both endpoints. The run script then creates the box, solvates it, minimizes the system, and executes both branches using relative paths. Run python write_parameters.py followed by bash run.sh in the example directory, or use the supplied reference records for analysis. Use a fresh example directory for a new run so that each collection of outputs retains a clear relationship to its inputs.

### Run box preparation, solvation and both branches

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
"$gmx" editconf -f PEG.gro -o boxed.gro -box 6 6 6 -c > box.log 2>&1
"$gmx" solvate -cp boxed.gro -cs spc216.gro -o solvated.gro -p topol.top > solvate.log 2>&1
"$gmx" grompp -f em.mdp -c solvated.gro -p topol.top -o em.tpr > em.grompp.log 2>&1
"$gmx" mdrun -deffnm em -ntmpi 1 -ntomp 2 -pin off > em.stdout.log 2>&1
for rep in 1 2; do
  mkdir "replica-$rep"
  cp em.gro topol.top PEG.itp "replica-$rep/"
  cp -r oplsaa.ff "replica-$rep/"
  for stage in nvt npt md; do cp "$stage-$rep.mdp" "replica-$rep/$stage.mdp"; done
  (
    cd "replica-$rep"
    "$gmx" grompp -f nvt.mdp -c em.gro -p topol.top -o nvt.tpr > nvt.grompp.log 2>&1
    "$gmx" mdrun -deffnm nvt -ntmpi 1 -ntomp 2 -pin off > nvt.stdout.log 2>&1
    "$gmx" grompp -f npt.mdp -c nvt.gro -t nvt.cpt -p topol.top -o npt.tpr > npt.grompp.log 2>&1
    "$gmx" mdrun -deffnm npt -ntmpi 1 -ntomp 2 -pin off > npt.stdout.log 2>&1
    "$gmx" grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr > md.grompp.log 2>&1
    "$gmx" mdrun -deffnm md -ntmpi 1 -ntomp 2 -pin off > md.stdout.log 2>&1
    printf 'Temperature
Potential
Pressure
Volume
Density
0
' | "$gmx" energy -f md.edr -o md-properties.xvg > energy.log 2>&1
    "$gmx" check -f md.xtc > trajectory-check.log 2>&1
  )
done
```

Run bash run.sh in a fresh example directory. Each stage supplies coordinates and checkpoint state to the next.

## Radius of gyration and end-to-end distance: two rulers for one chain

Before measuring chain dimensions, reconnect portions split by periodic boundaries into one whole molecule. Atoms at opposite edges of the displayed box can be covalent neighbors; subtracting their wrapped coordinates directly produces a separation close to the box length instead of the short bond distance. The analysis traverses the topology's bonds, reconstructs each neighboring displacement, and checks every resulting bond length. This provides a consistent geometry for the center of mass and squared distances. Across the 802 frames in the two records, the longest reconstructed covalent bond was approximately 0.1653 nm.

The radius of gyration, Rg, measures how the atoms are distributed around the center of mass. To locate that center, multiply every atomic position by its mass, sum the contributions, and divide by total mass. Heavier atoms have a greater influence. Next, measure each atom's distance from the center, square it, take a mass-weighted average, and finally take the square root. Squaring prevents contributions in opposite directions from canceling and gives more influence to distant atoms. Despite the word radius, the molecule need not be spherical: an elongated chain and a curved chain both have a well-defined Rg.

All atoms contribute to the radius of gyrationEq. 2

![All atoms contribute to the radius of gyration](https://ml-biomat.com/static/agent-math/f0ddad2cd53c7894acade735.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| i, Nₐ | Atom index and selected atom count, 115 here | 1 |
| mᵢ | Mass of atom i | u |
| Mₐ | Total selected atomic mass, distinguished from molar mass M | u |
| rᵢ, r꜀ₘ | Atomic position and center-of-mass vectors for the whole chain | nm |
| Rg | Mass-weighted radius of gyration | nm |
| Σ | Sum over selected atoms; the operation is dimensionless | 1 |
| ‖rᵢ − r꜀ₘ‖² | Squared displacement magnitude | nm² |
| mᵢ‖rᵢ − r꜀ₘ‖² | Atomic mass multiplied by squared distance | u nm² |
| =, −, /, √, × | Equality, vector subtraction, division, square root and adjacent multiplication; the square root converts nm² to nm | Operators are dimensionless |

Reading the relationshipFind the center of mass, then average squared distances with mass weights. Mass units cancel between numerator and denominator, leaving a length after taking the square root.

A worked exampleFor two equal-mass nodes at x=−1 and +1 nm with y=z=0, the center of mass is zero and Rg=√[(1²+1²)/2]=1 nm.

ConditionsUse all atoms and their actual masses in one complete molecule. Reconstruct periodic continuity along chemical bonds before calculating dimensions.

The end-to-end distance, Re, considers just two specified endpoints. Here they are the two terminal hydroxyl oxygens. This measure is intuitive but particularly sensitive to where those ends happen to lie. A broad U-shaped chain can bring its ends close together while keeping the middle spread over a substantial region. Another conformation can separate the ends while concentrating more of its internal mass. Contour length is a third quantity, obtained by adding distances along a defined backbone path. Re measures the straight shortcut between its endpoints, whereas contour length follows the route itself; the shortcut cannot exceed that route. Endpoint and path definitions must remain fixed when comparing results.

End distance follows a shortcut; contour length follows the backboneEq. 3

![End distance follows a shortcut; contour length follows the backbone](https://ml-biomat.com/static/agent-math/030abfabaea5214015e8d7a5.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Re | Straight distance between the selected terminal oxygens | nm |
| rᴏ,ʀ, rᴏ,ʟ | Whole-chain coordinates of the right and left hydroxyl oxygens | nm |
| L꜀ | Length along the backbone path joining the same endpoints | nm |
| j, Nᵦ | Path-segment index and number of segments | 1 |
| ℓⱼ | Length of segment j | nm |
| Σ, =, −, ‖·‖, ≤ | Segment sum, equality, vector subtraction, magnitude, and less than or equal to; operators are dimensionless | 1 |

Reading the relationshipThe straight line is the shortest route between the same endpoints. Bending changes that shortcut while segment addition retains the path length.

A worked exampleThree 1 nm segments have contour length 3 nm. At a 90° turning angle in the interaction, the endpoint displacement is (2,1,0) nm, so Re=√5≈2.236 nm, below 3 nm.

ConditionsThe path must join the specified endpoints. This example uses terminal oxygens; terminal carbons define a different end distance.

[Figure: Geometric dimensions of four equal-mass nodes](https://ml-biomat.com/tutorials/molecular-dynamics/g14/en/#en-s5)

A planar geometric chain of four equal-mass nodes: rotate the middle of three fixed-length segments to compare contour length, end distance, and radius of gyration.

The geometric interaction uses four equal-mass nodes connected by three equal-length segments. Changing the middle direction preserves contour length while changing both end distance and radius of gyration by different amounts. With a segment length of 1 nm and a turning angle of 90°, the end distance is approximately 2.236 nm and Rg is approximately 0.866 nm. At 0°, they become 3.000 and 1.118 nm. This controlled planar construction clarifies the measurements. Real PEG contains 115 atoms of different masses and interacts in three dimensions; the following curves use its actual atomic masses and reconstructed coordinates frame by frame.

### Recorded radius of gyration and terminal-oxygen distance

Two 2 ns production records, 401 frames each; the shaded region marks the 1000–2000 ps analysis window.

Hydroxyl-ended PEG with chemical EO degree 16 and 115 atoms; pinned Polyply OPLS-AA/LigParGen parameters and SPC/E water. Initial 6 nm cube, 300 K and 1 bar; two velocity/heat-bath histories from a common minimized geometry, 2 ns each.

[Download reference data and complete inputs (ZIP) 59.40 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-peg16-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g14/en/#en-s5)

The complete chain is reconstructed along chemical bonds and every bond is checked; curves show mass-weighted radius of gyration and terminal-oxygen distance in both histories.

Both trajectories repeatedly contract and extend, with changes occurring at different times. Over the full 2 ns, replica 1 has a mean Rg of approximately 0.7738 nm and replica 2 a mean of 0.7638 nm. These values are close, while their mean terminal-oxygen distances are approximately 1.8845 and 2.1859 nm. Similar overall mass dispersion therefore does not require similar endpoint statistics. Follow the upper and lower traces over the same interval to find periods when Rg changes modestly while the ends move substantially. Returning to the corresponding coordinates then identifies which part of the chain produced that difference.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g14/en/#en-s5)

Figure 3 · The actual minimum- and maximum-Rg conformations are selected from all 401 frames of each replica. Backbone carbon, oxygen and their chemical bonds are shown, with terminal oxygens circled; hydrogen and water participated in the simulation. Each conformation uses its own principal-plane projection at a common scale; projected distances can be shorter than three-dimensional distances.

## An average acquires meaning from many shapes

The most extended or compact frame helps illustrate the range of observed shapes. Learning how often a dimension occurs requires a collection of frames. We use the final 1 ns of production, from 1000 through 2000 ps, giving 201 frames per branch. Equal-duration windows allow the distributions to be compared under the same statistical definition. This is an explicit analysis choice that examines the later part of each record. Different molecular motions relax over different times, and slowly changing conformations may still produce differences between windows. Those differences are useful information when planning further sampling.

A histogram divides the size axis into adjacent intervals and counts frames in each interval. Raw counts increase with record length. Probability density instead divides the count by both the total number of frames and the interval width. The height of a histogram step multiplied by its width then gives the fraction of frames within that interval. With dimensions in nm, the density has units nm⁻¹. A height greater than one is entirely possible: normalization concerns the sum of interval areas, which equals one, rather than requiring every height to lie below one. A narrow distribution can have a tall probability density.

Represent probability by histogram areaEq. 4

![Represent probability by histogram area](https://ml-biomat.com/static/agent-math/484a99912c114acffc6e9f7f.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| k | Histogram interval index | 1 |
| pₖ | Probability density in interval k | nm⁻¹ |
| cₖ | Number of frames in that interval | 1 |
| F | Total analyzed frames, 201 in the final 1 ns | 1 |
| Δxₖ | Width of the dimension interval | nm |
| pₖΔxₖ | Frame fraction in that interval, its empirical probability | 1 |
| Σ, =, /, ×, 1 | Sum over all intervals, equality, division, multiplication, and normalization constant one; operators are dimensionless | 1 |

Reading the relationshipDivide counts by total frames to obtain probability, then by interval width to obtain density. If every frame is included in a bin, the interval areas sum to one.

A worked exampleIf 20 of 100 frames lie in a 0.05 nm interval, its density is 20/(100×0.05)=4 nm⁻¹ and its probability is 4×0.05=0.20.

ConditionsUse common bin edges covering all selected values in both replicas; temporal correlation is addressed separately when estimating uncertainty.

### Dimension distributions over the final 1 ns

Each replica contributes 201 frames, using common bins covering all selected values; height multiplied by width gives interval probability.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g14/en/#en-s6)

Observed conformational distributions over the final 1 ns, 201 frames per history, with common bins and probability-density normalization.

Over the final 1 ns, the mean Rg values are 0.7833 and 0.7570 nm, with sample standard deviations of approximately 0.0668 and 0.0560 nm. Mean end distances are 1.9055 and 2.0590 nm, with standard deviations of approximately 0.3724 and 0.3262 nm. Here the standard deviation describes the spread of shapes visited within the chosen window. The mean locates the distribution, while the spread describes its breadth. Together, these give a basic statistical meaning to the size of this chain. The two distributions overlap substantially, while preserving differences in the conformational regions visited by each branch.

Frames separated by 5 ps need not have lost memory of one another. A recently rotated chain segment usually remains related to its previous position, so 201 saved frames contain less independent information than 201 completely independent draws. Estimating uncertainty in a mean requires accounting for this temporal correlation, for example through sufficiently long blocks and additional independent runs. We retain separate averages, standard deviations, and traces for each branch so that their differences remain visible. Their common minimized starting geometry also identifies the particular range of initial conditions represented by these repeats.

You can compare the first and second nanoseconds using the same analysis, or change the number of histogram intervals from 25 to 12 or 40. Changing the time window changes which molecular history enters the statistics; changing bin number changes display resolution. If finer bins produce many sharp peaks, first inspect the number of frames per bin. Assigning a distinct conformational state to each peak would require further evidence from internal torsions and time continuity. Size distributions help locate interesting behavior, while the original trajectory retains the local structural information needed to investigate it.

## Hydration is a changing neighborhood

How many water molecules surround PEG? Before counting, define what surrounding means. Our geometric criterion includes a water molecule whenever its oxygen lies within 0.35 nm of at least one PEG oxygen. The 17 PEG oxygens comprise two terminal hydroxyl sites and 15 internal ether sites, while each water oxygen represents the position of its water molecule. This definition connects the local aqueous environment to chain geometry and can be recomputed directly from every recorded frame. Changing the cutoff selects a different spatial neighborhood, so comparisons should retain the same criterion or explicitly examine its sensitivity.

Two counts are easy to confuse. A water molecule may lie close to two or more polymer oxygens. Counting oxygen–water-oxygen contact pairs includes that molecule multiple times; counting distinct nearby waters requires combining repeated molecular identities. Consider two neighboring shops counting people near their entrances. Someone standing in the overlap between the two entrance regions appears on both lists, but a count of people on the street should include that person once. The molecular problem has the same bookkeeping issue, with distances evaluated in three dimensions under periodic boundaries.

Count water molecules and contact pairs separatelyEq. 5

![Count water molecules and contact pairs separately](https://ml-biomat.com/static/agent-math/ba060b9dffcbf6fe0bc9863b.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| t | Recorded time | ps |
| Nw(t) | Number of distinct qualifying water molecules | 1 |
| C(t) | Number of qualifying polymer-O–water-O contact pairs | 1 |
| j, Nᴡ | Water index and total water count, 6996 | 1 |
| i, 𝒪 | PEG oxygen index and the set of 17 PEG oxygens | 1 |
| dᵢⱼ(t) | Minimum-image oxygen–oxygen distance | nm |
| r꜀ | Geometric-neighbor cutoff, 0.35 here | nm |
| 𝟙[·] | Indicator: one when the condition holds, zero otherwise | 1 |
| Σ, min, ∈, <, = | Sum, minimum, set membership, less than, and equality; operators are dimensionless | 1 |

Reading the relationshipTaking the minimum distance to all PEG oxygens counts a water shared by several sites once. The double sum retains every qualifying contact pair.

A worked exampleWater A lies 0.30 and 0.32 nm from two PEG oxygens; water B lies 0.34 and 0.50 nm away. At a 0.35 nm cutoff, there are two unique waters and three contact pairs.

ConditionsThis is a geometric-neighbor definition. Hydrogen-bond analysis adds donor/acceptor, hydrogen-position and angular criteria; residence analysis tracks molecular identities over time.

The program first calculates a periodic distance matrix between all polymer oxygens and all water oxygens. Rows correspond to polymer sites and columns to water molecules. Testing whether a column contains at least one distance below the cutoff, then counting such columns, gives the unique-water count. Counting every matrix element below the cutoff gives the contact-pair count. Both quantities are useful, but they answer different questions. The first describes how many water molecules occupy the neighborhood; the second retains multiple simultaneous site contacts. Their difference measures repeated contributions from counting by site, rather than a separate collection of additional waters.

### Unique waters and repeated site contributions

A water oxygen lies within 0.35 nm of any PEG oxygen. The upper panel counts unique waters; the lower shows contact pairs minus unique waters.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g14/en/#en-s7)

Neighbors are defined by polymer-oxygen to water-oxygen distance below 0.35 nm; unique water molecules and atom contact pairs are counted separately.

In the final 1 ns, the mean unique-water counts are 20.219 and 19.443, with sample standard deviations of approximately 1.950 and 2.206. Mean contact-pair counts are substantially larger, at 38.826 and 37.478. The difference makes the spatial overlap tangible: neighboring polymer oxygens can share nearby waters, so adding site-by-site counts repeats some molecular identities. Each individual frame still contains an integer number of nearby waters. Fractional averages arise from combining frames; for example, counts of 20 and 21 in two frames have a mean of 20.5.

The neighborhood definition is reevaluated as the molecules move. To determine how long a particular water remains nearby, track its identity across time and specify how brief departures followed by returns are handled. To measure hydrogen bonds, additionally define donor and acceptor atoms, include hydrogen positions, and apply an angular criterion. The 0.35 nm oxygen distance used here specifies geometric proximity. Local orientation and exposure can vary even when the overall Rg is similar, so hydration counts may fluctuate without a large change in chain size. Studying these two measurements together turns a water-loving flexible chain into two defined questions about global shape and local environment.

## Use the complete analysis to design the next comparison

The Python program below reads md.tpr and md.xtc from both branches. TPR supplies atom names, masses, charges, and connectivity; XTC supplies coordinates over time. Together they specify the molecule being measured. The program checks atom and element counts, charge, and water count, reconstructs the complete chain, and then evaluates dimensions and nearby waters. MDAnalysis uses Å for coordinates by default. The code divides chain coordinates by ten to obtain nm, while the water-neighbor calculation uses the equivalent distance of 3.5 Å. Keeping conversion beside the calculation makes it easier to compare code with the equations.

### Complete shape and hydration analysis

```
"""Measure PEG shape and geometric hydration in two recorded trajectories.

python analyze_peg.py --records records --out analysis --language en
Each records/replica-1 and replica-2 contains md.tpr and md.xtc.
Dependencies: MDAnalysis, NumPy, Matplotlib. Native coordinates are in angstrom.
"""
from pathlib import Path
import argparse
import csv
import json
import numpy as np
import MDAnalysis as mda
from MDAnalysis.lib.distances import minimize_vectors, distance_array
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


def bond_plan(group):
    local = {int(index): k for k, index in enumerate(group.indices)}
    edges = np.asarray([[local[int(a)], local[int(b)]] for a, b in group.bonds.indices])
    graph = [[] for _ in group]
    for edge, (a, b) in enumerate(edges):
        graph[a].append((b, edge, 1)); graph[b].append((a, edge, -1))
    queue, seen, plan = [0], {0}, []
    for a in queue:
        for b, edge, sign in graph[a]:
            if b not in seen:
                queue.append(b); seen.add(b); plan.append((a, b, edge, sign))
    if len(seen) != len(group):
        raise ValueError("The polymer must have one connected bond graph")
    return edges, plan


def whole_chain(raw, box, edges, plan):
    vectors = minimize_vectors(raw[edges[:, 1]]-raw[edges[:, 0]], box)
    whole = np.empty_like(raw, dtype=float); whole[0] = raw[0]
    for parent, child, edge, sign in plan:
        whole[child] = whole[parent]+sign*vectors[edge]
    actual = whole[edges[:, 1]]-whole[edges[:, 0]]
    if np.max(np.linalg.norm(actual-vectors, axis=1)) > .005:
        raise ValueError("A reconstructed bond cycle is inconsistent")
    longest = float(np.linalg.norm(actual, axis=1).max()/10)
    if longest > .25:
        raise ValueError("A reconstructed covalent bond exceeds 0.25 nm")
    return whole/10, longest


def statistics(values):
    return {"mean": float(np.mean(values)), "sd": float(np.std(values, ddof=1)),
            "minimum": float(np.min(values)), "maximum": float(np.max(values))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, default=Path("records"))
    parser.add_argument("--out", type=Path, default=Path("analysis"))
    parser.add_argument("--language", choices=["zh", "en"], default="en")
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    zh = args.language == "zh"
    available = {f.name for f in font_manager.fontManager.ttflist}
    candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC",
                  "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else ["DejaVu Sans"]
    plt.rcParams.update({"font.family": [n for n in candidates if n in available],
                         "font.size": 14, "axes.labelsize": 15, "axes.titlesize": 16,
                         "svg.fonttype": "path", "axes.unicode_minus": False,
                         "axes.spines.top": False, "axes.spines.right": False})
    arrays = []; summaries = []; snapshots = []; maximum_bond = 0.
    for rep in [1, 2]:
        folder = args.records/f"replica-{rep}"
        u = mda.Universe(str(folder/"md.tpr"), str(folder/"md.xtc"))
        polymer = u.select_atoms("resname OHter PEO")
        oxygen = polymer.select_atoms("name O*")
        water = u.select_atoms("resname SOL and name OW")
        terminal = np.flatnonzero(polymer.names == "OA1")
        if len(polymer) != 115 or len(oxygen) != 17 or len(water) != 6996 or len(terminal) != 2:
            raise ValueError("Expected one hydroxyl-ended PEG16 and 6996 SPC/E waters")
        counts = {element: int(sum(n.startswith(element) for n in polymer.names)) for element in ["C", "H", "O"]}
        if counts != {"C": 32, "H": 66, "O": 17} or abs(sum(polymer.charges)) > 1e-5:
            raise ValueError("Polymer formula or charge differs from the defined model")
        edges, plan = bond_plan(polymer)
        rows = []; shapes = []
        for frame in u.trajectory:
            pos, longest = whole_chain(polymer.positions.astype(float), frame.dimensions, edges, plan)
            maximum_bond = max(maximum_bond, longest)
            center = np.average(pos, axis=0, weights=polymer.masses)
            centered = pos-center
            rg = np.sqrt(np.average(np.sum(centered**2, axis=1), weights=polymer.masses))
            end = np.linalg.norm(pos[terminal[1]]-pos[terminal[0]])
            # A water contributes once to unique hydration, even near several polymer O atoms.
            near = distance_array(oxygen.positions, water.positions, box=frame.dimensions) < 3.5
            unique = int(np.any(near, axis=0).sum())
            pairs = int(near.sum())
            rows.append([float(frame.time), float(rg), float(end), unique, pairs])
            shapes.append(centered)
        values = np.asarray(rows); arrays.append(values)
        if values.shape != (401, 5) or not np.allclose(values[:, 0], np.arange(401)*5):
            raise ValueError("Expected 401 saved frames from 0 to 2000 ps")
        late = values[:, 0] >= 1000
        names = ["Rg_nm", "Re_nm", "unique_waters", "oxygen_water_pairs"]
        summaries.append({"replica": rep, "frames": len(values), "late_frames": int(late.sum()),
                          "all": {n: statistics(values[:, k+1]) for k, n in enumerate(names)},
                          "last_1ns": {n: statistics(values[late, k+1]) for k, n in enumerate(names)}})
        with (args.out/f"replica-{rep}.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle); writer.writerow(["time_ps", *names]); writer.writerows(values)
        for label, index in [("minimum-Rg", int(np.argmin(values[:, 1]))), ("maximum-Rg", int(np.argmax(values[:, 1])))]:
            snapshots.append({"replica": rep, "selection": label, "time_ps": values[index, 0],
                              "Rg_nm": values[index, 1], "Re_nm": values[index, 2],
                              "coordinates_nm": shapes[index].tolist(), "names": polymer.names.tolist(),
                              "bonds": edges.tolist(), "terminal_indices": terminal.tolist()})
    summary = {"model": "HO-(CH2-CH2-O)16-H; OPLS-AA/LigParGen; SPC/E; 300 K; 1 bar",
               "window_ps": [1000, 2000], "sd_definition": "sample SD, ddof=1; not uncertainty of the mean",
               "hydration_cutoff_nm": .35, "maximum_bond_nm": maximum_bond, "replicas": summaries}
    (args.out/"summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (args.out/"snapshots.json").write_text(json.dumps(snapshots), encoding="utf-8")
    colors = ["#147d92", "#c46b3c"]
    labels = ["副本 1", "副本 2"] if zh else ["Replica 1", "Replica 2"]
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True, constrained_layout=True)
    for k, (ax, ylabel) in enumerate(zip(axes, ["回转半径 Rg / nm", "端氧间距 Re / nm"] if zh else ["Radius of gyration Rg / nm", "Terminal-O distance Re / nm"])):
        for i, values in enumerate(arrays):
            ax.plot(values[:, 0]/1000, values[:, k+1], color=colors[i], lw=1.2, label=labels[i])
        ax.axvspan(1, 2, color="#e7d8b4", alpha=.2); ax.set_ylabel(ylabel); ax.grid(alpha=.15)
    axes[0].legend(ncol=2); axes[-1].set_xlabel("生产阶段时间 / ns" if zh else "Production time / ns")
    axes[0].set_title("相同链长，两条构象历史" if zh else "One chain length, two conformational histories")
    save(fig, args.out/"peg-shape")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.8), constrained_layout=True)
    pooled = np.concatenate([v[v[:, 0] >= 1000] for v in arrays])
    bins = [np.linspace(pooled[:, k].min()-.01, pooled[:, k].max()+.01, 26) for k in [1, 2]]
    for k, ax in enumerate(axes):
        for i, values in enumerate(arrays):
            v = values[values[:, 0] >= 1000, k+1]
            ax.hist(v, bins=bins[k], density=True, histtype="step", linewidth=2.3, color=colors[i], label=labels[i])
        ax.set_xlabel(["Rg / nm", "Re / nm"][k]); ax.set_ylabel("概率密度 / nm⁻¹" if zh else "Probability density / nm⁻¹"); ax.grid(alpha=.15)
    axes[0].legend(); fig.suptitle("后 1 ns 的构象分布：每条 201 帧" if zh else "Conformational distributions over the final 1 ns: 201 frames each")
    save(fig, args.out/"peg-distributions")
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True, constrained_layout=True)
    for i, values in enumerate(arrays):
        axes[0].plot(values[:, 0]/1000, values[:, 3], color=colors[i], lw=1.2, label=labels[i])
        axes[1].plot(values[:, 0]/1000, values[:, 4]-values[:, 3], color=colors[i], lw=1.2, label=labels[i])
    axes[0].set_ylabel("不同近邻水分子数" if zh else "Unique nearby water molecules")
    axes[1].set_ylabel("接触对数 − 不同水分子数" if zh else "Contact pairs − unique waters")
    axes[0].set_title("氧—水氧距离小于 0.35 nm 的几何近邻" if zh else "Geometric neighbors: polymer O–water O distance < 0.35 nm")
    axes[0].legend(ncol=2); axes[-1].set_xlabel("生产阶段时间 / ns" if zh else "Production time / ns")
    for ax in axes: ax.axvspan(1, 2, color="#e7d8b4", alpha=.2); ax.grid(alpha=.15)
    save(fig, args.out/"peg-hydration")
    print(json.dumps(summary, indent=2))


def save(fig, path):
    fig.savefig(path.with_suffix(".svg")); fig.savefig(path.with_suffix(".png"), dpi=150); plt.close(fig)


if __name__ == "__main__":
    main()
```

Read both recorded trajectories, reconstruct the chain along its bond graph, verify every bond, and produce frame data, distributions, and hydration plots.

Place the reference files in records/replica-1 and records/replica-2, then run python analyze_peg.py --records records --out analysis --language en. The program produces three figure groups, two frame-by-frame CSV files, and a statistical summary. Choosing zh changes the figure language while retaining the same calculations. Each CSV row contains time, radius of gyration, terminal-oxygen distance, unique-water count, and contact-pair count. You can therefore connect a point of interest on a curve to a specific saved time. The program also saves the actual conformations with the smallest and largest Rg in each branch for structural inspection.

A useful starting model for future chain-length comparisons is the freely jointed chain. Imagine N equal segments of length b whose directions are independent. The end-to-end vector is the sum of the segment vectors. Squaring its magnitude produces each segment's squared length together with cross terms between different segments. Averaging many isotropic, independent directions makes those cross terms cancel, producing the relation below. A typical end distance consequently grows with the square root of segment number, whereas the contour length grows directly with segment number. The two meanings of length have different growth laws.

Typical end distance of a freely jointed chainEq. 6

![Typical end distance of a freely jointed chain](https://ml-biomat.com/static/agent-math/9ef8a802f33a136168b4ab44.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| N | Number of independently oriented statistical segments | 1 |
| b | Fixed length of each segment | nm |
| Re² | Squared end-to-end distance | nm² |
| ⟨Re²⟩ | Ensemble mean squared end distance | nm² |
| Re,rms | Root-mean-square end distance, distinct from the mean end distance | nm |
| L꜀ | Contour length | nm |
| ⟨·⟩, =, √, ×, ² | Conformational average, equality, square root, multiplication and squaring; squaring changes the length unit to nm² | Operators are dimensionless |

Reading the relationshipThe end vector is a sum of N segment vectors. Independent isotropic directions give zero average cross terms, leaving N contributions of b².

A worked exampleAn ideal chain with N=16 and b=0.5 nm has mean squared end distance 4 nm², root-mean-square end distance 2 nm, and contour length 8 nm. N counts model segments.

ConditionsIdeal equal-length freely jointed segments with independent isotropic directions. The PEG chemical repeat count is not automatically the statistical segment count; the atomistic example retains angles, torsional potentials, and solvent.

PEG has specific bond angles, torsional preferences, excluded atomic volume, and solvent interactions, all of which can correlate neighboring directions. Applying the ideal relation therefore requires stating how the real molecule is represented by statistical segments. A chemical repeat count n of 16 does not automatically equal the independent-segment count N. Determining a statistical segment length from atomistic trajectories requires further conformational and chain-length information. This distinction gives the simple model a useful explanatory role while identifying what must be measured from the molecular system. Comparing PEG8, PEG16, and PEG32 will retain end chemistry, force field, solvent, and measurement definitions while varying chemical length.

The present records show that a short chain can have similar average mass dispersion while following different endpoint histories, accompanied by fluctuations in its local water neighborhood. A next study can ask whether longer chains shift their size distributions, whether more distinct waters lie nearby, and how hydration changes after normalization by oxygen-site count. End-group modification or surface attachment introduces additional chemical or spatial conditions that belong in a new model. Following molecular identity, motion conditions, measurement definitions, and statistical comparison in that order helps connect a material change to the molecular process it actually alters.

## Further Reading and Open Materials

- [Polyply Quick Start and oplsaaLigParGen library](https://github.com/marrink-lab/polyply_1.0/tree/38d4d5424e1ef35c86e7cb8532fbd86ecf997221) · Polyply developers; Marrink group · Apache-2.0

  Topology generation, coordinate construction, and the PEO/OHter atomic parameters and linking rules.

  Adapt the general workflow to hydroxyl-ended PEG16 in water; fix the construction seed and add two GROMACS 2026.4 histories, element accounting, and complete analysis.
- [Polyply; a python suite for facilitating simulations of macromolecules and nanomaterials](https://doi.org/10.1038/s41467-021-27627-4) · Fabian Grünewald, Riccardo Alessandri, Peter C. Kroon, Luca Monticelli, Paulo C. T. Souza, Siewert J. Marrink · CC BY 4.0

  Methodological background on separating graph parameterization and coordinate construction.

  Explain the two stages through this PEG example with newly drawn diagrams and analyses.
- [LigParGen web server: an automatic OPLS-AA parameter generator for organic ligands](https://doi.org/10.1093/nar/gkx312) · Leela S. Dodda, Israel Cabeza de Vaca, Julian Tirado-Rives, William L. Jorgensen · Bibliographic reference; no article text or figures reproduced

  LigParGen background cited by the pinned parameter library.

  Retain the library parameters without regenerating charges through the web service.
- [Macromolecular Chemistry — Nobel Lecture, 1953](https://www.makro.uni-freiburg.de/dateien_neu/document-pdf-word-excel-usw/geschichte/vorlesung_hs) · Hermann Staudinger · Publicly readable lecture; no open reuse license assumed

  Historical discussion of covalent macromolecular connectivity and natural and synthetic materials.

  Brief historical paraphrase with an independently drawn connectivity schematic.
- [Hermann Staudinger and the Foundation of Polymer Science](https://www.acs.org/education/whatischemistry/landmarks/staudingerpolymerscience.html) · American Chemical Society, National Historic Chemical Landmarks · Publicly readable history; no site text or image reproduced

  The 1920 long-chain proposal and the question addressed by rubber hydrogenation.

  Brief factual paraphrase linked to topology and conformation in this chapter.
