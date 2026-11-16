# A Complete Study: PEG Chain Length, Conformation and Hydration

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g18/en/
Language: en

Compare three PEG lengths and six recorded trajectories, linking molecular dimensions, hydration counts, and sampling variation in one reproducible study.

## What changes when a chain becomes longer?

Joining short pieces of thread makes a longer thread, but the area it occupies on a table also depends on how it bends. Polyethylene glycol in water has a similar distinction between two lengths: the distance followed along its chemical backbone and the spatial extent of the whole molecule. This distinction matters when thinking about flexible chains on material surfaces, molecular linkers, or the way water approaches a polymer. Adding repeat units supplies more atoms, more bonds around which the backbone can turn, and more sites that interact with water. These changes occur together. The resulting spatial dimensions emerge from molecular motion, so a comparison needs both a precise chemical definition and a record of the shapes that the chain visits.

The study compares hydroxyl-ended PEG containing 8, 16, or 32 chemical EO repeat units, with two production trajectories of 2 ns for each length. Here EO means the repeating –CH₂–CH₂–O– chemical fragment; the terminal bookkeeping is developed below. All three systems use the same atomic parameter library, water model, temperature, and pressure settings. We examine chain dimensions, how those dimensions change with repeat count, and the number of nearby water molecules. Each motion history remains visible throughout the comparison. This gives the study a common measuring framework while preserving the variation produced by molecular motion, including the pronounced difference between the two longer-chain histories.

“The same conditions” has a specific meaning in this design. There is one polymer chain per box, the initial box is a cube of side 6 nm, and pressure control allows its volume to change after solvation. The number of chains and the box-construction rule are shared; polymer mass fraction increases with chain length. A comparison at fixed mass fraction would instead adjust the amount of water or the number of chains. Both chain ends remain hydroxyl groups, neither end is attached to a surface, and the water contains no added salt. The present object is therefore a freely moving single-chain solution model. A grafted layer introduces attachment points, neighboring chains, and surface interactions, each of which changes the space available to the polymer.

By the end, you should be able to separate “a longer chain is larger” into questions that can be checked: how many atoms were actually added, which average defines spatial size, whether a higher hydration count mainly reflects a larger number of oxygen sites, and whether two histories give similar answers. The same research sequence is useful when comparing peptide lengths, linker compositions, or carbohydrate branching. First define the chemical variable being changed. Then preserve the other modeling choices, and choose observables that answer the intended question. The value of the comparison comes from linking these decisions: a clear chemical intervention, a reproducible simulation, and measurements whose meaning remains stable across the systems.

## Align repeat units, end groups, and atom counts

Write the chemical molecule as HO–(CH₂–CH₂–O)ₙ–H. Every additional EO fragment contributes two carbon atoms, four hydrogen atoms, and one oxygen atom, while the complete molecule also needs its terminal atoms. The resulting counts are 2n carbons, 4n+2 hydrogens, and n+1 oxygens, giving 7n+3 atoms in total. Doing this accounting before simulation checks the repeat count, terminal chemistry, and explicit inclusion of hydrogen atoms at the same time. PEG8 contains 16 carbons, 34 hydrogens, and 9 oxygens: 59 atoms altogether. PEG32 contains 64 carbons, 130 hydrogens, and 33 oxygens, giving 227 atoms. These are chemical identities that the topology and trajectory should preserve throughout the run.

Check atom counts from chemical repeatsEq. 1

![Check atom counts from chemical repeats](https://ml-biomat.com/static/agent-math/9e1b62b0cd7c6e085ab93c3f.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| n | Number of chemical EO repeats | 1 |
| N_{C}, N_{H}, N_{O} | Carbon, hydrogen, and oxygen atom counts | 1 |
| N_{a} | Total chain atom count | 1 |
| 2, 4, 1, 7, 3 | Integer coefficients obtained from repeat-fragment and terminal compositions | 1 |
| =, +, × | Equality, addition; adjacency of a number and n means multiplication | 1 |

Reading the relationshipCount each element in HO–(CH₂–CH₂–O)ₙ–H, then sum the element counts.

A worked exampleFor n=16: 32 carbons, 66 hydrogens, and 17 oxygens give 115 atoms and 17 software assembly blocks.

ConditionsNeutral linear PEG with two hydroxyl ends and explicit hydrogens; changing end groups changes the count.

The assembly blocks used by software need to be distinguished from chemical repeat units. The oplsaaLigParGen library in Polyply supplies an OHter block with composition CH₃O and an internal PEO block with composition C₂H₄O; linking definitions connect these blocks into a complete backbone. PEGn is therefore built from OHter:1 PEO:(n−1) OHter:1. PEG16 has one terminal block, fifteen internal blocks, and another terminal block: seventeen software residues but sixteen chemical EO repeats. A residue is an organizational grouping of atoms. The horizontal chain-length coordinate in this chapter always uses the chemical count n. Confusing these two counts would change the atom balance, the apparent end-group fraction, and every quantity normalized by repeat number.

Atom counts also connect to the more familiar molar mass. Using atomic molar masses of 12.011, 1.008, and 15.999 g/mol for carbon, hydrogen, and oxygen, each added EO contributes about 44.053 g/mol, with a terminal completion of about 18.015 g/mol for the whole hydroxyl-ended molecule. The three molar masses are therefore approximately 370.439, 722.863, and 1427.711 g/mol. A mole counts an enormous fixed number of identical molecules as one amount of substance, and molar mass describes the mass of that amount. Atom counting describes the composition inside one molecule; molar mass connects the same composition to laboratory weighing. This link helps relate simulated repeat count to a chemically defined molecular sample.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g18/en/#en-s2)

Figure 1 · Chemical repeat count is n and assembly-block count is n+1; the proportion of terminal hydroxyl oxygens changes with length.

The two ends also produce a useful compositional difference between short and long chains. Every molecule has two hydroxyl oxygens, while the remaining n−1 oxygens lie inside ether linkages. Among oxygen sites, the terminal fraction is 2/9, or about 22.2%, for PEG8 and 2/33, or about 6.1%, for PEG32. Hydroxyl and internal ether oxygens have different bonded surroundings, local charges, and hydrogen-bonding roles. The average number of nearby waters per oxygen can therefore change with n through both end-group dilution and changing chain conformations. To separate these contributions, the next analysis would classify terminal and internal oxygens before averaging, so that chemically equivalent sites are compared across lengths.

The complete preparation program copies a common force-field directory and writes the appropriate sequence, random seeds, and simulation settings for each n. Topology generation answers which atoms exist and how they interact; coordinate generation answers where those atoms initially sit. Their responsibilities are separate. A fixed construction seed is used for each length, followed by the same minimization and preparation schedule. The two motion histories share the minimized geometry for that length but receive separate initial velocities and stochastic thermostat seeds. This exposes variation associated with motion histories while retaining their shared starting point. Testing sensitivity to initial conformation would add several independently generated shapes and prepare each through the same sequence.

## From random steps to real chains: why divide by a square root?

A useful statistical picture represents a flexible molecule as a sequence of segments that can change direction. Imagine taking steps of equal length while continually turning. The total distance walked accumulates with every step, whereas the straight-line displacement from start to finish is reduced by cancellation between differently directed steps. An ideal random-chain model uses this geometry in three dimensions. Its object is the end-to-end distance across many possible chain conformations, rather than the speed of a person moving through time. This picture provides a reference for size growth: doubling the number of segments doubles the contour length, while cancellations allow the typical spatial extent to grow more slowly.

Size of independent ideal random segmentsEq. 2

![Size of independent ideal random segments](https://ml-biomat.com/static/agent-math/bd5b2eb5ec6fe72ef03b5229.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| R_{rms} | Root-mean-square end-to-end distance across the conformational ensemble | nm |
| b | Fixed statistical-segment length | nm |
| N | Number of independent isotropically oriented segments | 1 |
| L | Contour length obtained by summing segment lengths | nm |
| √, /, ×, = | Nonnegative square root, division, multiplication, and equality; Nb is a product | 1 |
| 1 | Unit numerator defining a reciprocal | 1 |

Reading the relationshipExpanding the squared total vector leaves N terms b² when cross terms average to zero for independent isotropic segments; taking the square root restores length.

A worked exampleFor b=0.5 nm and N=16, R_rms=2 nm, L=8 nm, and their ratio is 0.25.

ConditionsStatistical relation for ideal independent segments; N is distinct from chemical repeat count n, and individual conformations can differ from the root mean square.

The square root follows from adding vectors. The overall end-to-end vector is the sum of all segment vectors. Squaring that sum produces the squared length of every individual segment together with cross terms between different segments. For independent, isotropically oriented steps, positive and negative cross terms cancel upon averaging over the conformational ensemble. The remaining N terms each contribute b², so the mean squared distance is Nb² and its square root is b√N. Averaging does essential work in this argument: a particular straight conformation can extend to Nb. The result describes the statistical dimensions of an ensemble, which is why the diagram shows several possible chains rather than assigning one shape to every length.

In his 1949 treatment of real polymer chains, Flory brought spatial interference between distant segments into the chain-dimension problem. Work on conformations and solution properties then connected local chemistry with experimentally accessible molecular dimensions. The historical shift asks a concrete question: what happens when distant segments approach, and how does the solvent change the cost of that contact? Atomistic simulation addresses this through repulsion, attraction, and rearrangement of surrounding water. The ideal random chain supplies a transparent reference against which those effects can be examined.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g18/en/#en-s3)

Figure 2 · Independent random segments provide a square-root reference; nonlocal contacts and solvent change conformational weights.

Applying this picture to PEG requires attention to scale. In the equation, N counts statistical segments with approximately independent orientations, and b is their length. They do not automatically equal the number of EO repeats and the length of a chemical bond. Bond angles, torsional preferences, and correlations between neighboring fragments determine how much chain should be grouped into one statistical segment. Dividing the measured dimensions by √n in this chapter examines growth relative to the square root of chemical repeat count. When local structure and the ratio of statistical segments to chemical repeats stabilize across sufficiently long chains, that reference approaches a statistical-chain description. The present range retains appreciable terminal and finite-length effects, so every measured point remains visible.

The interactive exercise expresses size as a simple power law, anchors the size at 0.5 nm when n=8, and varies the growth exponent and repeat count. With an exponent of 0.5, division by √n produces a horizontal curve; an exponent above 0.5 produces an increasing normalized curve. Switching the display to division by n highlights the difference between spatial growth and a constant straight-line contribution per repeat. The exercise evaluates an analytical expression, while the measured PEG trajectories appear separately below. Predict the size ratio on increasing n from 8 to 32 before moving the controls. The exercise makes normalization an explicit mathematical operation rather than a choice made only after seeing a plot.

Power-law guide and normalizationEq. 3

![Power-law guide and normalization](https://ml-biomat.com/static/agent-math/c1eaf8c2ee492e14fd83637b.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| D(n), D₀ | Size at n and reference size, with D₀=0.5 nm in the exercise | nm |
| n, n₀ | Chemical repeat count and reference count, with n₀=8 | 1 |
| ν | Selected growth exponent | 1 |
| α | Normalization exponent: 0 gives raw size, 0.5 divides by √n, and 1 divides by n | 1 |
| Q_α(n) | Normalized dimension | nm |
| ( ), /, ^, =, × | Grouping, division, exponentiation, equality, and multiplication | 1 |

Reading the relationshipUse a dimensionless length ratio to determine the size multiplier, then divide by the chosen power of repeat count to reveal remaining variation.

A worked exampleFor n=32 and ν=0.5, D=0.5×√(32/8)=1 nm and Q₀.₅=1/√32≈0.1768 nm, equal to the value at n=8.

ConditionsThe exercise evaluates an analytical guide with a chosen exponent. Recorded dimensions and local slopes are calculated separately from trajectories.

Analytical power law: D(8)=0.5 nm; vary the exponent and compare normalizations.

[Figure: Analytical dimension versus repeat count](https://ml-biomat.com/tutorials/molecular-dynamics/g18/en/#en-s3)

Analytical power-law comparison. The dot follows the selected n; every curve has a raw dimension of 0.5 nm at n=8.

## Put six trajectories on a common footing

Preparation starts from three explicit chemical sequences. The pinned Polyply parameter library generates PEG topologies and initial coordinates, after which each molecule is centered in a cubic 6 nm box and solvated. The final systems contain 7012, 6996, and 6970 water molecules respectively; the differences arise from polymer-excluded space and overlap handling during construction. Water uses SPC/E, and PEG uses the library OPLS-AA/LigParGen parameters with their stored charges, bonded terms, and nonbonded interactions. Keeping this parameter family common makes the length comparison traceable to chemical composition and conformation. Changing the polymer–water parameter combination would introduce another research variable, to be examined through its effect on local conformations and hydration.

Each length first undergoes energy minimization to relax crowded initial contacts. Its two motion histories then separately receive 100 ps of fixed-volume thermal preparation, 200 ps of pressure-controlled preparation, and 2 ns of pressure-controlled production. The target temperature is 300 K, the target pressure is 1 bar, and the integration step is 2 fs. Covalent bonds involving hydrogen are constrained, and water retains its prescribed geometry during dynamics; minimization uses settings allowing flexible water. Constraints remove some of the fastest bond vibrations from the integration problem, and the timestep is chosen with that treatment in mind. Temperature control uses stochastic velocity rescaling, while isotropic C-rescale pressure coupling changes the three box dimensions by a common scale factor.

### Prepare inputs for three chemical lengths

```
"""Prepare three fresh PEG model directories from the pinned Polyply library.

python prepare_study.py --forcefield oplsaa.ff --out length-runs
Install the pinned Polyply version using the preparation page before running
the generated construction commands. GROMACS 2026.4 supplies oplsaa.ff.
"""
from pathlib import Path
import argparse
import shutil
import subprocess
import sys

POLYMER = '''#include "oplsaa.ff/forcefield.itp"
#include "PEG.itp"
[ system ]
Hydroxyl-ended PEG
[ molecules ]
PEG 1
'''
SOLUTION = '''#include "oplsaa.ff/forcefield.itp"
#include "PEG.itp"
#include "oplsaa.ff/spce.itp"
[ system ]
Hydroxyl-ended PEG in SPC/E water
[ molecules ]
PEG 1
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--forcefield', type=Path, default=Path('oplsaa.ff'))
    parser.add_argument('--out', type=Path, default=Path('length-runs'))
    args = parser.parse_args()
    if not (args.forcefield/'forcefield.itp').is_file() or not (args.forcefield/'spce.itp').is_file():
        raise ValueError('Supply the complete GROMACS oplsaa.ff directory')
    targets=[args.out/f'PEG{n}' for n in (8,16,32)]
    if any(p.exists() for p in targets):
        raise ValueError('Choose a fresh output directory for the three models')
    here=Path(__file__).resolve().parent
    for n,target in zip((8,16,32),targets):
        target.mkdir(parents=True)
        shutil.copytree(args.forcefield,target/'oplsaa.ff')
        for name in ('seeded_polyply.py','run_one.sh'):
            shutil.copyfile(here/name,target/name)
        (target/'polymer.top').write_text(POLYMER,encoding='utf-8',newline='\n')
        (target/'topol.top').write_text(SOLUTION,encoding='utf-8',newline='\n')
        generate=f'''#!/usr/bin/env bash
set -euo pipefail
polyply gen_params -lib oplsaaLigParGen -o PEG.itp -name PEG -seq OHter:1 PEO:{n-1} OHter:1 > topology-generation.log 2>&1
python seeded_polyply.py {20261400+n} gen_coords -p polymer.top -o PEG.gro -name PEG -box 6 6 6 > coordinate-generation.log 2>&1
'''
        (target/'generate.sh').write_text(generate,encoding='utf-8',newline='\n')
        subprocess.run([sys.executable,str(here/'write_parameters.py'),'--n',str(n),'--out',str(target)],check=True)
        print(f'Prepared PEG{n}: {7*n+3} atoms, {n+1} oxygen sites')


if __name__=='__main__':main()
```

Copy the common force field, write the three sequences and construction seeds, and call the parameter writer.

### Write complete simulation parameters

```
"""Write the complete PEG length-study simulation settings for two velocity histories.
Run: python write_parameters.py --n 8|16|32 [--out INPUT_DIRECTORY]
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
    parser.add_argument("--n", type=int, choices=[8, 16, 32], required=True)
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    (args.out/"em.mdp").write_text(EM, encoding="utf-8", newline="\n")
    for replica in [1, 2]:
        replacements = {"20263161": str(20263000+10*args.n+replica),
                        "20264161": str(20264000+10*args.n+replica),
                        "20265161": str(20265000+10*args.n+replica),
                        "20266161": str(20266000+10*args.n+replica)}
        for stage, template in [("nvt", NVT), ("npt", NPT), ("md", MD)]:
            content = template
            for old, new in replacements.items():
                content = content.replace(old, new)
            (args.out/f"{stage}-{replica}.mdp").write_text(content, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
```

Complete minimization and per-history stage settings; n determines the corresponding random seeds.

### Set the coordinate-construction random state

```
import random,sys,runpy,shutil
import numpy as np
seed=int(sys.argv[1]);random.seed(seed);np.random.seed(seed)
entry=shutil.which('polyply');assert entry
sys.argv=[entry,*sys.argv[2:]];runpy.run_path(entry,run_name='__main__')
```

Set the supplied seed for Python and NumPy random generators used during Polyply construction.

After recording coordinates, the first analysis task is to reconstruct molecules that cross periodic boundaries. Think of the box as a map whose opposite faces meet: an atom may be stored on the opposite side while remaining covalently attached to its neighbor. Starting from one terminal oxygen, the program traverses the bond graph and places each neighboring atom using the shortest periodic bond displacement. It then checks every bond, including those beyond the particular traversal path. Radius of gyration and end-to-end distance consequently refer to one continuous molecule. Units are standardized at this step as well: MDAnalysis reads coordinates in ångströms, so lengths are divided by ten before being reported in nanometers.

A continuous molecular representation also allows an image-separation check. The program translates the whole chain into the 26 neighboring periodic cells and finds the closest atom pair between the chain and these translated copies. The smallest recorded separation across the six trajectories is about 2.082 nm, in the first PEG32 history. It exceeds the 1.0 nm short-range nonbonded cutoff used here, establishing a clear geometric gap to periodic copies in the saved frames. Long-range electrostatics still uses periodic PME, and size fluctuations or solvent response can depend on box dimensions. A box-size study would place the same chain model in larger water boxes and compare the same dimension observables and correlation times.

Production coordinates are saved every 5 ps, giving 401 frames from 0 to 2000 ps in each history. The main comparison uses 1000 through 2000 ps inclusive, or 201 frames, while the full time series remains visible. This defines a measurement window and preserves the evidence needed to inspect slower changes. Adjacent frames belong to continuous motion and are temporally correlated. The 500 ps blocks used later reveal how averages change between chronological intervals; they are not a relabeling of every stored frame as an independent experiment. The two histories provide a separate view of variation, although both still begin from the minimized geometry for their particular chain length.

## Three chain lengths and two spatial rulers

When looking at a molecule, the separation between its two ends often attracts attention first. Radius of gyration instead measures how the mass of the entire chain is distributed. The center of mass is the balance point of the atomic masses, with heavier atoms contributing more strongly. To obtain the radius of gyration, square every atom’s distance from that center, weight it by the atom’s mass, divide by total mass, and take the square root. End-to-end distance is the straight-line separation between the two terminal oxygen atoms. The first ruler combines the whole chain; the second focuses on its ends. Local folding and overall bending can therefore affect the two measures differently.

Mass distribution and terminal separationEq. 4

![Mass distribution and terminal separation](https://ml-biomat.com/static/agent-math/fce8efd11f65b25d8badbf12.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| N_{a}, i | Total chain atom count and atom index | 1 |
| mᵢ, M | Atomic mass and total chain mass | u |
| rᵢ, r_{cm} | Atomic position vector in the whole chain and center-of-mass position | nm |
| r_{A}, r_{B} | Position vectors of the two terminal oxygens; A and B identify the ends | nm |
| R_{g}, R_{e} | Mass-weighted radius of gyration and end-to-end distance | nm |
| Σ, =, /, −, √ | Summation, equality, division, vector subtraction, and nonnegative square root | 1 |
| \|rᵢ−r_{cm}\|² | Squared vector length, the sum of squared Cartesian components | nm² |
| mᵢ\|rᵢ−r_{cm}\|² | Mass multiplied by squared distance | u nm² |
| \|r_{B}−r_{A}\| | Length of the terminal displacement vector | nm |
| 1, 2 | Atom indexing starts at 1; superscript 2 denotes squaring | 1 |

Reading the relationshipThe center uses mass weights, and squared distances avoid cancellation between opposite directions. Reconstruct the whole periodic molecule before measuring its internal geometry.

A worked exampleTwo equal-mass points at x=−1 and +1 nm, with other coordinates zero, have their center at zero, R_g=1 nm, and terminal separation R_e=2 nm.

ConditionsR_g includes every PEG atom with masses from its TPR; R_e uses the two terminal oxygens of the same whole molecule.

Consider a chain bent into a horseshoe. Its ends may approach closely while the central portion still occupies a broad region. End-to-end distance then falls strongly even if the radius of gyration remains relatively large. A third quantity, contour length, follows the backbone bond by bond. There are 3n backbone bonds between the terminal oxygens in this model. The recorded mean contour lengths are approximately 3.50, 7.01, and 14.02 nm for PEG8, PEG16, and PEG32, close to proportional growth with n. Their spatial dimensions are much smaller. Most of the additional chemical path is used in changing direction rather than contributing entirely to displacement along one straight line.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g18/en/#en-s5)

Figure 3 · One frame near the median Rg over 1–2 ns from each history, reconstructed along covalent bonds and projected at a common scale; dimension statistics use full three-dimensional coordinates.

The displayed conformations are recorded frames chosen near the median radius of gyration within the 1–2 ns window of each history, shown at a common length scale. Relative atomic positions come from the reconstructed molecule; rigid rotation improves visibility and water is hidden. Median selection answers what a middle-sized conformation in that interval looks like, while retaining its identity as one member of the sampled ensemble. Many different bending patterns can share a similar radius of gyration. The full time traces therefore carry additional information: how long a large fluctuation persists, when the two histories approach each other, and when they explore visibly different ranges.

### Dimensions across six trajectories

Shading marks the 1–2 ns analysis window; each full record contains 401 frames.

Hydroxyl-ended PEG with chemical EO degrees 8, 16 and 32, using pinned Polyply OPLS-AA/LigParGen parameters, SPC/E water, 300 K and 1 bar. Each length has two 2 ns velocity/heat-bath histories sharing a minimized geometry; different lengths are prepared separately.

[Download reference data and complete inputs (ZIP) 178.13 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-peg-lengths-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g18/en/#en-s5)

Six actual 2 ns trajectories, 401 frames each; shading marks the 201-frame main window from 1 to 2 ns. Mass radius of gyration and terminal-oxygen distance follow bond-by-bond chain reconstruction and checks of all bonds.

The PEG8 histories repeatedly enter similar size ranges during the second half, with mean radii of gyration of about 0.485 and 0.473 nm. PEG16 gives about 0.783 and 0.757 nm, while PEG32 gives 1.288 and 1.154 nm. Separation between the longer-chain histories is especially visible around 1.0–1.5 ns. This pattern is consistent with the broader range of internal shapes and the time required for collective rearrangement of a longer chain. Longer records and additional starting conformations would test that interpretation. The present traces already identify where further sampling is most useful, preserving the temporal context that would disappear if each curve were reduced immediately to a single number.

Distinguish the mean distance from the square root of the mean squared distance. If two frames have radii of gyration of 0.4 and 0.6 nm, their ordinary mean is 0.5 nm and their root mean square is about 0.510 nm, because squaring gives larger dimensions more weight. Random-chain theory naturally expresses relations involving mean squared distances, so the main length-comparison plots use root-mean-square dimensions. The accompanying records also retain ordinary means, standard deviations, and full time series. Choosing a different statistic leaves every molecular coordinate unchanged but changes the measurement question being answered. Keeping the names and units explicit makes that choice understandable when comparing theory, simulations, or experiments.

Arithmetic mean and root mean squareEq. 5

![Arithmetic mean and root mean square](https://ml-biomat.com/static/agent-math/cbf32dbc2d5f556c9fb0c55d.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| D_{k} | R_g or R_e in saved frame k | nm |
| m, k | Frame count in the selected window and frame index | 1 |
| D̄, D_{rms} | Arithmetic mean and root mean square | nm |
| D_{k}² | Squared single-frame dimension | nm² |
| Σ, /, √, = | Summation, division, nonnegative square root, and equality | 1 |
| 1, 2 | 1/m gives equal frame weights; superscript 2 means multiplication by itself | 1 |

Reading the relationshipSquaring before averaging gives larger dimensions more weight; the final square root restores length units.

A worked exampleFor D=0.4 and 0.6 nm, the mean is 0.5 nm and the root mean square is √[(0.16+0.36)/2]≈0.510 nm.

ConditionsEach main window is 1000≤t≤2000 ps with 201 frames. Equally spaced frames receive equal weights; temporal correlation affects statistical precision.

## Read growth trends and calculate local slopes

Computing root-mean-square dimensions within each history and then combining their mean squares with equal weight gives approximately 0.481, 0.773, and 1.227 nm for PEG8, PEG16, and PEG32. The combination averages squared distances before taking the square root. Because the two selected windows contain equal numbers of frames, it also equals pooling their squared measurements with equal frame weights. The plot nevertheless retains circles and squares for the individual histories, preserving their differences. Spatial dimensions clearly increase with n. The next question is comparative: how quickly do they increase relative to a precisely specified reference?

### Raw and length-normalized dimensions

Each point represents one history; dashed guides follow √n anchored at the equal-history PEG8 root mean square.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g18/en/#en-s6)

Raw and chemical-EO-normalized dimensions, with one point per history. Dashed √n guides are anchored at the equal-history root mean square for PEG8.

The dashed guide starts at the pooled PEG8 value and then grows as √n. This provides a readable benchmark: increasing n from 8 to 32 multiplies repeat count by four, so the square-root guide doubles the dimension from about 0.481 to 0.962 nm. The recorded PEG32 root-mean-square radii, about 1.290 and 1.159 nm, both lie above it. After division by √n, the two PEG8 values are about 0.172 and 0.168 nm, compared with 0.228 and 0.205 nm for PEG32. The normalized plot places the primary length-growth reference in the denominator and exposes the remaining variation, where local conformations, end groups, and sampled motion can all contribute.

End-to-end distance gives a more differentiated picture. The equal-history root-mean-square values are about 1.085, 2.014, and 2.810 nm across the three lengths, but the two PEG32 histories give approximately 3.333 and 2.163 nm separately. Dividing the latter by √n brings it close to the PEG8 values, while that same longer-chain history still has a higher normalized radius of gyration. Reading both rulers reveals why overall size and separation of the ends need not track each other one to one. For a linker asked to span a gap, terminal separation and its distribution are especially relevant. For the overall spatial spread of the chain, radius of gyration is the more direct descriptor.

Local growth slope between two lengthsEq. 6

![Local growth slope between two lengths](https://ml-biomat.com/static/agent-math/f970df85819488f454b4ee20.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| n₁, n₂ | Two chemical repeat counts, with n₂>n₁>0 | 1 |
| D(n₁), D(n₂) | Dimension statistic with the same definition and sampling window | nm |
| ν₁₂ | Logarithmic growth ratio between these lengths | 1 |
| ln, /, [ ], = | Natural logarithm, division, grouping, and equality; logarithm arguments are dimensionless ratios | 1 |
| 1, 2 | Subscripts identifying the two comparison conditions | 1 |

Reading the relationshipFor an exact power law, taking logarithms of the size ratio recovers the power. Applied to measured points, it gives the local slope over that interval.

A worked exampleFor RMS R_g values D(8)=0.481104 nm and D(16)=0.772702 nm, ν₁₂≈ln(0.772702/0.481104)/ln2≈0.684.

ConditionsHere this describes finite chain lengths and a finite time window; asymptotic scaling requires an extended length regime and stable sampling.

A logarithmic ratio summarizes the change between neighboring lengths. For root-mean-square radius of gyration it is approximately 0.684 between PEG8 and PEG16, and 0.667 between PEG16 and PEG32. The corresponding values for end-to-end distance are about 0.893 and 0.480. These are local growth slopes for two finite length intervals, one parameter set, and one sampling window. A long-chain asymptotic exponent requires an appropriate length regime together with stable sampling and a treatment of finite-size and terminal effects. The useful observation here is that the two dimension measures show different sensitivities in a finite-length comparison. That distinction helps specify what additional data would be most informative.

A useful continuation would add intermediate repeat counts and extend the longest-chain trajectories, then examine whether neighboring-interval slopes stabilize. Keep the histories separate rather than retaining only three pooled points. If longer records bring the PEG32 terminal-distance distributions closer together, their earlier separation can be related to slow conformational sampling. Persistent separation motivates more starting conformations and a broader examination of time scales. Comparisons with experiments also require matching observables: scattering, diffusion, and terminal-label distances weight molecular shape differently. The mass-weighted atomic radius used here is a precisely defined simulation observable, to be connected explicitly to the weighting and measurement protocol of the intended experiment.

## More water overall, or more water near each site?

Water molecules continuously exchange around PEG. To convert this moving neighborhood into comparable data, first specify a geometric rule: a water molecule is nearby when the shortest periodic distance between its oxygen and at least one polymer oxygen is below 0.35 nm. This oxygen–oxygen criterion is simple to evaluate and consistent across chain lengths. Hydrogen-bond analysis would add donor, acceptor, and angular requirements. Residence-time analysis would track the identity of each water molecule through time. Separating these questions lets the present count carry a clear meaning: it measures a geometrically defined instantaneous neighborhood around the polymer oxygen sites.

A water molecule can lie near two or more polymer oxygens at the same instant. If the question is how many distinct waters surround the chain, that molecule is counted once. If the question is how many oxygen–water contacts exist, every qualifying site–water pair contributes. Imagine polymer oxygens as lamps illuminating nearby points that represent water molecules. The union of illuminated regions gives the number of distinct waters. Adding the counts lamp by lamp counts points in overlapping regions more than once. Both quantities are useful because they answer different questions: the number of neighboring molecules and the number of site contacts. The analysis therefore retains both columns.

Distinct waters and contact pairsEq. 7

![Distinct waters and contact pairs](https://ml-biomat.com/static/agent-math/43eca583cd3b469fd2c9509a.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| N_{w}, w | Total water molecule count and water index | 1 |
| N_{O}, j | Polymer oxygen count and site index, with N_O=n+1 | 1 |
| d_{wj} | Shortest periodic distance from the oxygen of water w to polymer oxygen j | nm |
| r_{c} | Neighborhood cutoff, 0.35 nm in the main plot | nm |
| U, C | Distinct neighboring water count and oxygen–water contact-pair count | 1 |
| u, c | The two counts divided by oxygen-site count | per oxygen site |
| Σ, min, 1[ ], < | Summation, minimum, indicator equal to 1 if true and 0 otherwise, and strictly less than | 1 |
| /, =, 1 | Division, equality, and the indexing origin or unit contribution of an indicator | 1 |

Reading the relationshipFor distinct waters, ask whether each water is near at least one oxygen. For contact pairs, count every qualifying site–water combination. Division by oxygen count enables comparisons across lengths.

A worked exampleFor two oxygens with three distinct neighboring waters, one shared by both sites, U=3, C=4, u=1.5, and c=2.

ConditionsDistances use the periodic box of each frame. This is an oxygen–oxygen neighborhood definition; hydrogen-bond analysis additionally requires angular and donor–acceptor criteria.

### Total and per-oxygen hydration counts

Means over 1–2 ns with an O–O cutoff of 0.35 nm. Distinct-water unions and contact pairs are counted separately.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g18/en/#en-s7)

Hydration over 1–2 ns using a 0.35 nm polymer-O–water-O cutoff. The union of distinct waters and the number of contact pairs are counted separately, then compared with counts per oxygen site.

Within the 1–2 ns window, mean distinct-water counts are approximately 11.80 and 11.62 for the two PEG8 histories, 20.22 and 19.44 for PEG16, and 33.79 and 33.29 for PEG32. Longer chains carry more oxygen sites and have more distinct neighboring waters overall. Dividing by oxygen count changes the question: PEG8 gives about 1.311 and 1.291 waters per oxygen, while PEG32 gives about 1.024 and 1.009. An increasing total and a decreasing allocation per site are compatible. The longer chain supplies more sites, but their neighborhoods can overlap, and the mixture of terminal and internal sites changes at the same time.

Contact pairs divided by oxygen count are about 2.357 and 2.346 for PEG8, and 2.176 and 2.162 for PEG32. This quantity permits one water molecule to contribute at several sites, making it the mean site coordination count under the distance criterion. Its difference from distinct waters per oxygen highlights shared neighborhoods. A more resolved interpretation would group oxygen sites by terminal or internal identity and by their chemical distance from an end, then examine whether coiling changes neighborhood overlap. Moving from a total count to site-specific counts and then to conformation turns a broad phrase such as stronger or weaker hydration into local processes that can be measured separately.

The distance threshold is itself part of the measurement definition. Reducing 0.35 nm to 0.30 nm emphasizes closer waters, while increasing it to 0.40 nm includes a more distant shell. The complete program stores all three counts so that sensitivity to the boundary can be inspected. A small motion near the threshold can change an instantaneous count, making time averages and distance distributions useful companions. These geometric measurements describe polymer–water contact. Dissolution free energy additionally involves energetic and entropic contributions relative to a chosen reference state, so a thermodynamic solubility question calls for a corresponding free-energy calculation. The present counts identify local structural changes that such a study may seek to explain.

## Turn the comparison into a reproducible study

The final step connects chemical definitions, run conditions, and analysis choices into a repeatable workflow. The single-system script below performs box construction, solvation, minimization, and preparation and production for both histories. The study script calls it for all three lengths and then generates figures in both languages. Prepare the versions of GROMACS, Polyply, and the analysis environment described on the preparation page, and place the complete oplsaa.ff directory beside the example. The generator requires a fresh output directory so that existing results remain available for comparison. You can also begin with the reference trajectories provided on this page, reproduce the analysis, and then rerun the molecular dynamics stages according to available computing resources.

### Run native simulation for one length

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

Generate two motion histories from the common minimized configuration, retaining temperature, pressure, and energy records.

### Run the three lengths and generate bilingual figures

```
#!/usr/bin/env bash
set -euo pipefail
python prepare_study.py --forcefield oplsaa.ff --out length-runs
for n in 8 16 32; do
  (
    cd "length-runs/PEG$n"
    bash generate.sh
    bash run_one.sh
  )
done
python analyze_lengths.py --peg8 length-runs/PEG8 --peg16 length-runs/PEG16 --peg32 length-runs/PEG32 --out length-study/en --language en
python analyze_lengths.py --peg8 length-runs/PEG8 --peg16 length-runs/PEG16 --peg32 length-runs/PEG32 --out length-study/zh --language zh
```

Start in the example directory; new systems go into length-runs, with analysis outputs separated by language.

The analysis reads each history’s own TPR first, obtaining actual atomic masses, covalent connectivity, and water count before reading coordinates. For every frame it reconstructs PEG, verifies geometric consistency across all bonds, and calculates dimensions, contour length, water neighborhoods, and image separation. Framewise CSV files can be opened directly in spreadsheet software. The summary JSON retains window statistics, normalized quantities, and chronological blocks, while SVG figures preserve labeled axes and units. This combination connects a point in a figure to its averaging interval and then to the corresponding conformations, avoiding manual transcription as the link between evidence and interpretation.

### Build the comparison from native topologies and trajectories

```
"""Compare hydroxyl-ended PEG8, PEG16 and PEG32 under common conditions.

python analyze_lengths.py --peg8 PEG8 --peg16 PEG16 --peg32 PEG32 --out length-study --language en
Each PEG directory contains replica-1 and replica-2, each with md.tpr and md.xtc.
Dependencies: MDAnalysis, NumPy, SciPy and Matplotlib.
"""
from pathlib import Path
from itertools import product
import argparse
import csv
import json
import numpy as np
import MDAnalysis as mda
from MDAnalysis.lib.distances import minimize_vectors, distance_array
from scipy.spatial import cKDTree
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


def bond_plan(group, terminal):
    local = {int(index): k for k, index in enumerate(group.indices)}
    edges = np.asarray([[local[int(a)], local[int(b)]] for a, b in group.bonds.indices])
    graph = [[] for _ in group]
    for edge, (a, b) in enumerate(edges):
        graph[a].append((b, edge, 1)); graph[b].append((a, edge, -1))
    queue, seen, plan = [int(terminal[0])], {int(terminal[0])}, []
    parents = {int(terminal[0]): None}
    for a in queue:
        for b, edge, sign in graph[a]:
            if b not in seen:
                queue.append(b); seen.add(b); plan.append((a, b, edge, sign));parents[b] = a
    if len(seen) != len(group):
        raise ValueError('Polymer bond graph is not connected')
    route = [int(terminal[1])]
    while parents[route[-1]] is not None:
        route.append(parents[route[-1]])
    return edges, plan, np.array(route[::-1])


def reconstruct(raw, box, edges, plan, anchor):
    vectors = minimize_vectors(raw[edges[:,1]]-raw[edges[:,0]], box)
    whole = np.empty_like(raw, dtype=float);whole[anchor] = raw[anchor]
    for parent, child, edge, sign in plan:
        whole[child] = whole[parent]+sign*vectors[edge]
    actual = whole[edges[:,1]]-whole[edges[:,0]]
    if np.max(np.linalg.norm(actual-vectors, axis=1)) > .005:
        raise ValueError('Reconstructed bond cycle is inconsistent')
    longest = float(np.linalg.norm(actual, axis=1).max()/10)
    if longest > .25:
        raise ValueError('Reconstructed covalent bond exceeds 0.25 nm')
    return whole/10, longest


def stats(v):
    return {'mean':float(np.mean(v)), 'sample_sd':float(np.std(v,ddof=1)),
            'rms':float(np.sqrt(np.mean(v*v))), 'minimum':float(np.min(v)), 'maximum':float(np.max(v))}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for n in (8,16,32):parser.add_argument(f'--peg{n}',type=Path,default=Path(f'PEG{n}'))
    parser.add_argument('--out',type=Path,default=Path('length-study'))
    parser.add_argument('--language',choices=['en','zh'],default='en')
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    arrays={};summaries=[];snapshots=[];blocks=[]
    translations=np.array([v for v in product((-1,0,1),repeat=3) if v!=(0,0,0)])
    expected_waters={8:7012,16:6996,32:6970}
    for n in (8,16,32):
        for rep in (1,2):
            folder=getattr(args,f'peg{n}')/f'replica-{rep}'
            u=mda.Universe(str(folder/'md.tpr'),str(folder/'md.xtc'))
            polymer=u.select_atoms('resname OHter PEO');oxygen=polymer.select_atoms('name O*')
            water=u.select_atoms('resname SOL and name OW');terminal=np.flatnonzero(polymer.names=='OA1')
            counts={el:int(sum(str(name).startswith(el) for name in polymer.names))for el in ('C','H','O')}
            if counts!={'C':2*n,'H':4*n+2,'O':n+1} or len(polymer)!=7*n+3 or len(terminal)!=2 or len(water)!=expected_waters[n]:
                raise ValueError(f'PEG{n} composition differs from the specified model')
            if abs(sum(polymer.charges))>1e-5:raise ValueError('Polymer charge is not neutral')
            edges,plan,route=bond_plan(polymer,terminal)
            assert len(route)==3*n+1 and len(edges)==len(polymer)-1
            masses=polymer.masses;totalmass=float(masses.sum());rows=[];coordinates=[];maxbond=0.
            for frame in u.trajectory:
                whole,bondmax=reconstruct(polymer.positions.astype(float),frame.dimensions,edges,plan,int(terminal[0]))
                maxbond=max(maxbond,bondmax);center=np.average(whole,axis=0,weights=masses);pos=whole-center
                rg=float(np.sqrt(np.average(np.sum(pos*pos,axis=1),weights=masses)))
                re=float(np.linalg.norm(whole[terminal[1]]-whole[terminal[0]]))
                contour=float(np.linalg.norm(np.diff(whole[route],axis=0),axis=1).sum())
                assert re<=contour+1e-8
                distances=distance_array(oxygen.positions,water.positions,box=frame.dimensions)/10
                hydration=[]
                for cutoff in (.30,.35,.40):
                    near=distances<cutoff;hydration += [int(np.any(near,axis=0).sum()),int(near.sum())]
                # Explicit translated copies, with no minimum-image operation on their separation.
                if not np.allclose(frame.dimensions[3:],90,atol=.001):raise ValueError('Image check expects the orthogonal simulation cells')
                boxnm=frame.dimensions[:3]/10
                if np.any(np.ptp(pos,axis=0)>=boxnm):raise ValueError('Extend the periodic-image search for this chain span')
                translated=(pos[None,:,:]+translations[:,None,:]*boxnm).reshape(-1,3)
                image_min=float(cKDTree(pos).query(translated,k=1)[0].min())
                volume=float(np.prod(boxnm))
                rows.append([float(frame.time),rg,re,contour,*hydration,image_min,volume]);coordinates.append(pos)
            values=np.array(rows);arrays[(n,rep)]=values
            assert values.shape==(401,12) and np.allclose(values[:,0],np.arange(401)*5)
            late=values[:,0]>=1000
            row={'EO_degree':n,'replica':rep,'polymer_atoms':len(polymer),'oxygen_sites':len(oxygen),
                 'water_molecules':len(water),'mass_u':totalmass,'backbone_bonds':len(route)-1,
                 'frames':401,'main_window_frames':int(late.sum()),'maximum_bond_nm':maxbond,
                 'minimum_image_distance_nm':float(values[:,10].min()),
                 'main_window':{name:stats(values[late,col])for name,col in [('Rg_nm',1),('Re_nm',2),('contour_nm',3),('unique_waters',6),('contact_pairs',7),('volume_nm3',11)]},
                 'cutoff_sensitivity':{str(c):{'unique_mean':float(values[late,4+2*j].mean()),'pairs_mean':float(values[late,5+2*j].mean())}for j,c in enumerate((.30,.35,.40))}}
            row['RMS_Rg_over_sqrt_n_nm']=row['main_window']['Rg_nm']['rms']/np.sqrt(n)
            row['RMS_Re_over_sqrt_n_nm']=row['main_window']['Re_nm']['rms']/np.sqrt(n)
            row['unique_per_oxygen']=row['main_window']['unique_waters']['mean']/(n+1)
            row['pairs_per_oxygen']=row['main_window']['contact_pairs']['mean']/(n+1)
            row['unique_per_EO']=row['main_window']['unique_waters']['mean']/n
            summaries.append(row)
            for q in range(4):
                mask=(values[:,0]>q*500)&(values[:,0]<=(q+1)*500);assert mask.sum()==100
                blocks.append({'EO_degree':n,'replica':rep,'start_ps':q*500,'end_ps':(q+1)*500,
                               'frames':100,'Rg_mean_nm':float(values[mask,1].mean()),'Re_mean_nm':float(values[mask,2].mean()),
                               'unique_mean':float(values[mask,6].mean())})
            pick=np.flatnonzero(late)[np.argmin(abs(values[late,1]-np.median(values[late,1])))]
            snapshots.append({'EO_degree':n,'replica':rep,'time_ps':values[pick,0],'Rg_nm':values[pick,1],
                              'Re_nm':values[pick,2],'coordinates_nm':coordinates[pick].tolist(),
                              'names':polymer.names.tolist(),'masses':masses.tolist(),'bonds':edges.tolist(),'terminal_indices':terminal.tolist()})
            with (args.out/f'PEG{n}-replica-{rep}.csv').open('w',newline='',encoding='utf-8')as stream:
                writer=csv.writer(stream);writer.writerow(['time_ps','Rg_nm','Re_nm','contour_nm','unique_030','pairs_030','unique_035','pairs_035','unique_040','pairs_040','image_min_nm','volume_nm3']);writer.writerows(values)
    pooled={}
    for n in (8,16,32):
        v=np.concatenate([arrays[(n,r)][arrays[(n,r)][:,0]>=1000]for r in (1,2)])
        pooled[n]={'rms_Rg_nm':float(np.sqrt(np.mean(v[:,1]**2))),'rms_Re_nm':float(np.sqrt(np.mean(v[:,2]**2)))}
    slopes=[]
    for lo,hi in [(8,16),(16,32)]:
        slopes.append({'n_low':lo,'n_high':hi,'Rg_log_ratio':float(np.log(pooled[hi]['rms_Rg_nm']/pooled[lo]['rms_Rg_nm'])/np.log(hi/lo)),
                       'Re_log_ratio':float(np.log(pooled[hi]['rms_Re_nm']/pooled[lo]['rms_Re_nm'])/np.log(hi/lo))})
    summary={'model':'Hydroxyl-ended PEG; pinned Polyply oplsaaLigParGen; SPC/E; 300K/1bar',
             'main_window_ps':[1000,2000],'time_block_definition':'(0,500],(500,1000],(1000,1500],(1500,2000]ps,100frames each',
             'replicate_design':'Two velocity and thermostat histories share one minimized geometry per length; different lengths are separate molecular models',
             'image_check':'26 nearest nonzero orthogonal translations of reconstructed full chain, separate from periodic PME effects',
             'records':summaries,'pooled_equal_frame_RMS':pooled,'adjacent_length_log_ratios':slopes,'chronological_blocks':blocks}
    (args.out/'length_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    (args.out/'length_snapshots.json').write_text(json.dumps(snapshots),encoding='utf-8')
    zh=args.language=='zh';tr=lambda z,e:z if zh else e
    available={f.name for f in font_manager.fontManager.ttflist};fonts=['Microsoft YaHei','Noto Sans CJK SC','Source Han Sans SC','WenQuanYi Zen Hei','DejaVu Sans']
    plt.rcParams.update({'font.family':[f for f in fonts if f in available]if zh else['DejaVu Sans'],
                         'font.size':14,'svg.fonttype':'path','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,
                         'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5'})
    colors=['#167d84','#c16b3d'];markers=['o','s']
    def save(fig,name):
        fig.savefig(args.out/f'{name}-{args.language}.svg');fig.savefig(args.out/f'{name}-{args.language}.png',dpi=160);plt.close(fig)
    fig,axes=plt.subplots(3,1,figsize=(12,9.6),sharex=True,constrained_layout=True)
    for n,ax in zip((8,16,32),axes):
        for r in (1,2):
            v=arrays[(n,r)];ax.plot(v[:,0]/1000,v[:,1],color=colors[r-1],lw=1.2,label=tr(f'轨迹{r}',f'History {r}'))
        ax.axvspan(1,2,color='#e9d9ba',alpha=.35);ax.set(ylabel=f'PEG{n}: Rg / nm');ax.grid(alpha=.15)
    axes[0].legend(loc='lower center',bbox_to_anchor=(.5,1.02),ncol=2,frameon=False)
    axes[-1].set_xlabel(tr('生产阶段时间 / ns','Production time / ns'));save(fig,'length-conformations')
    fig,axes=plt.subplots(2,2,figsize=(13,9),constrained_layout=True)
    ns=np.array([8,16,32]);grid=np.linspace(8,32,100)
    for j,(name,label)in enumerate([('Rg_nm','Rg'),('Re_nm','Re')]):
        for rep in (1,2):
            vals=[r['main_window'][name]['rms']for r in summaries if r['replica']==rep]
            axes[0,j].scatter(ns,vals,c=colors[rep-1],marker=markers[rep-1],s=65,label=tr(f'轨迹{rep}',f'History {rep}'))
            axes[1,j].scatter(ns,np.array(vals)/np.sqrt(ns),c=colors[rep-1],marker=markers[rep-1],s=65)
        anchor=pooled[8]['rms_'+label+'_nm']
        axes[0,j].plot(grid,anchor*np.sqrt(grid/8),c='#647b80',ls='--',label=tr('以PEG8为锚的√n参考','√n guide anchored at PEG8'))
        axes[0,j].set_ylabel(tr(f'{label} 均方根 / nm',f'RMS {label} / nm'))
        axes[1,j].set_ylabel(tr(f'{label} 均方根 / √n / nm',f'RMS {label} / √n / nm'))
        for ax in axes[:,j]:ax.set(xticks=ns,xlabel=tr('化学EO重复数 n','Chemical EO repeat count n'));ax.grid(alpha=.15)
    handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='outside upper center',ncol=3,frameon=False,fontsize=12)
    save(fig,'length-normalization')
    fig,axes=plt.subplots(1,3,figsize=(15,5.8),constrained_layout=True);fig.get_layout_engine().set(wspace=.12)
    for rep in (1,2):
        rr=[r for r in summaries if r['replica']==rep]
        axes[0].scatter(ns,[r['main_window']['unique_waters']['mean']for r in rr],c=colors[rep-1],marker=markers[rep-1],s=65,label=tr(f'轨迹{rep}',f'History {rep}'))
        axes[1].scatter(ns,[r['unique_per_oxygen']for r in rr],c=colors[rep-1],marker=markers[rep-1],s=65)
        axes[2].scatter(ns,[r['pairs_per_oxygen']for r in rr],c=colors[rep-1],marker=markers[rep-1],s=65)
    for ax,label in zip(axes,[tr('不同近邻水分子数','Unique nearby waters'),tr('不同水分子数 / 氧位点','Unique waters / oxygen site'),tr('接触对数 / 氧位点','Contact pairs / oxygen site')]):
        ax.set(xticks=ns,xlabel=tr('EO重复数 n','EO repeat count n'),ylabel=label);ax.grid(alpha=.15)
    h,l=axes[0].get_legend_handles_labels();fig.legend(h,l,loc='outside upper center',ncol=2,frameon=False)
    fig.supxlabel(tr('1–2 ns均值；聚合物氧—水氧距离 < 0.35 nm','Means over 1–2 ns; polymer O–water O distance < 0.35 nm'),fontsize=12)
    save(fig,'length-hydration')
    fig,axes=plt.subplots(1,3,figsize=(14,5.8),constrained_layout=True);fig.get_layout_engine().set(wspace=.1)
    for n,ax in zip((8,16,32),axes):
        for rep in (1,2):
            rr=[r for r in blocks if r['EO_degree']==n and r['replica']==rep]
            ax.plot([.25,.75,1.25,1.75],[r['Rg_mean_nm']for r in rr],marker=markers[rep-1],c=colors[rep-1],lw=1.5,label=tr(f'轨迹{rep}',f'History {rep}'))
        ax.set(title=f'PEG{n}',xlabel=tr('区间中点 / ns','Block midpoint / ns'),ylabel=tr('块平均 Rg / nm','Block mean Rg / nm'),xticks=[.25,.75,1.25,1.75]);ax.grid(alpha=.15)
    h,l=axes[0].get_legend_handles_labels();fig.legend(h,l,loc='outside upper center',ncol=2,frameon=False)
    fig.supxlabel(tr('四个连续0.5 ns时间块；每块100帧','Four consecutive 0.5 ns blocks; 100 saved frames per block'),fontsize=12)
    save(fig,'length-sampling')
    print(json.dumps({'runs':len(summaries),'pooled_RMS':pooled,'log_ratios':slopes},indent=2))


if __name__=='__main__':main()
```

Read six TPR/XTC pairs, reconstruct bonded molecules, and calculate dimensions, hydration, image distances, and chronological blocks; write CSV, JSON, and SVG outputs.

Finally, return to time as well as chain length. Divide each 2 ns trajectory into four consecutive intervals of 0.5 ns, each using 100 saved frames, and plot the interval mean radius of gyration. The first PEG32 history becomes larger in the third interval, while the second increases in the fourth; their size changes occur at different times. The PEG8 histories are closer in the later intervals. This plot compresses the time-trace behavior into easily compared blocks while retaining chronological order. The blocks belong to continuous motion histories and may remain correlated, so the figure describes sensitivity to the chosen interval rather than error bars from four independent replicates.

The word repeat also has a hierarchy here. For each n, the two histories share minimized coordinates and differ in their initial velocities and stochastic thermostat histories, revealing motion variation under that preparation. Different lengths have no atom-by-atom matched starting conformation; the same plot color identifies a history number, not a paired experiment that can be subtracted pointwise across lengths. To estimate a length-specific ensemble mean and its uncertainty, add independently prepared starting shapes, assess correlation times when choosing blocks, and report variation between preparations separately from fluctuations within a trajectory. This hierarchy helps direct additional computation toward variation that the existing records have not yet covered.

### Sensitivity across chronological blocks

Four intervals (0,500], (500,1000], (1000,1500], and (1500,2000] ps, each containing 100 frames.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g18/en/#en-s8)

Four successive left-open, right-closed 500 ps windows, each containing 100 frames. Each of the six histories retains its own chronological variation to assess sensitivity to the selected analysis interval.

Together, the six trajectories provide a concrete set of results for this parameter set and the 1–2 ns window: overall dimensions increase with PEG length, the total number of distinct neighboring waters rises, both per-oxygen hydration counts decrease, and PEG32 terminal distance is more sensitive to motion history. These observations suggest specific follow-up questions. Separate terminal and internal oxygens to investigate the per-oxygen hydration change. Increase temporal and conformational coverage, and extend the length range, to examine dimension-growth relations. Introduce terminal attachment and surface separation when studying a surface-bound linker. Each additional system then addresses a measured difference rather than simply expanding the number of simulations.

A report can follow the same order. Introduce the three chemical chains and their shared aqueous environment, show how they move through time, explain what length normalization and site normalization each change about the question, and identify the difference most worth testing next. The atoms in a structure image, the coordinates behind a curve, and the numbers in the text should all follow the same definitions. This is the research skill developed throughout the course: beginning with a materials question, connect a molecular model, actual trajectories, and physically meaningful measurements so that another reader can understand the reasoning and recover the results from the code and records.

## Further Reading and Open Materials

- [Polyply Quick Start and oplsaaLigParGen library](https://github.com/marrink-lab/polyply_1.0/tree/38d4d5424e1ef35c86e7cb8532fbd86ecf997221) · Polyply developers; Marrink group · Apache-2.0

  Topology generation, coordinate construction, and the PEO/OHter atomic parameters and linking rules.

  Compare hydroxyl-ended PEG8, PEG16, and PEG32 with the same pinned library and two native GROMACS histories per length; add length normalization, periodic-image checks, and site-normalized hydration counts.
- [Polyply; a python suite for facilitating simulations of macromolecules and nanomaterials](https://doi.org/10.1038/s41467-021-27627-4) · Fabian Grünewald, Riccardo Alessandri, Peter C. Kroon, Luca Monticelli, Paulo C. T. Souza, Siewert J. Marrink · CC BY 4.0

  Methodological background on separating graph parameterization and coordinate construction.

  Explain the two stages through this PEG example with newly drawn diagrams and analyses.
- [LigParGen web server: an automatic OPLS-AA parameter generator for organic ligands](https://doi.org/10.1093/nar/gkx312) · Leela S. Dodda, Israel Cabeza de Vaca, Julian Tirado-Rives, William L. Jorgensen · Bibliographic reference; no article text or figures reproduced

  LigParGen background cited by the pinned parameter library.

  Retain the library parameters without regenerating charges through the web service.
- [Paul John Flory — Biographical Memoir](https://www.nasonline.org/wp-content/uploads/2024/06/flory-paul.pdf) · William S. Johnson, Walter H. Stockmayer, Henry Taube · Publicly readable scholarly memoir; no open reuse license assumed

  Historical discussion of spatial interference in real chains in 1949 and the development of conformational statistics.

  Briefly paraphrase the research question with an independently drawn conceptual figure.
