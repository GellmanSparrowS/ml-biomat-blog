# Grafting Polymers onto a Membrane

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g16/en/
Language: en

Compare two PEG grafting fractions through recorded surface densities, mass distributions, terminal heights, and preparation histories.

## A moving polymer coat on a lipid membrane

A polyethylene glycol chain in water can bend, turn back, and extend. What changes when one end is connected to a lipid? The lipid's two hydrophobic tails remain inside the membrane, while the water-compatible polymer explores the surrounding liquid. A useful picture is a small floating anchor carrying a flexible rope. Many such molecules form a mobile surface covering. Its outward extent, uniformity, and accessibility matter when studying lipid carriers, wetting, or the approach of biological molecules. This system also connects two subjects we have already encountered separately: the conformations of a polymer chain and the organization of a membrane.

Grafting means attaching one end of a chain through a chemical connection to another molecule or a surface. Here the attachment is to a lipid, so the grafting point can still move laterally and fluctuate vertically with that lipid. Its position is free to change in space. Imagine ropes tied to small floating platforms: the platforms move relative to one another, and the ropes continually change shape. The highest endpoint in a snapshot may belong to a single unusually extended chain. To describe the coating, we therefore examine the distribution of polymer mass, terminal positions, and differences among individual chains.

At low grafting density, a chain has considerable room to spread sideways and return toward its attachment point. At higher density, neighboring chains increasingly explore overlapping regions, and both chains and solvent rearrange. The familiar terms “mushroom” and “brush” emphasize these two tendencies: relatively separate coils and outward extension under crowded grafting conditions. A molecular brush remains flexible and thermally active. Drawing it as a set of straight toothbrush bristles captures the name but conceals backfolding, interpenetration, and the broad distribution of terminal heights. Those features are central to interpreting the measurements in this lesson.

We compare two planar membranes containing the same number of lipid-anchored molecules: 200 in total, divided equally between two leaflets. In one membrane, 5% of those molecules carry PEG; in the other, 25% do. Every PEG contains 50 EO model repeat units and a hydroxyl terminal unit, so the chain length is held fixed while the graft count changes. Each system has a recorded 20 ns coarse-grained trajectory at 300 K and 1 bar. We measure membrane area, polymer mass-mean height, terminal height, and radius of gyration to determine how “more chains” appears in distinct observables.

The trajectories also provide a practical exercise in interpreting preparation history. Chains in the denser system begin from a more outwardly extended construction, whereas the sparse system uses unrestricted coordinate growth. Density, starting conformation, and relaxation time therefore all enter the comparison. We examine the full evolution, use the final 10 ns for specified summaries, and retain individual-chain records. The resulting analysis helps choose useful starting structures and durations for subsequent independent simulations. It also helps decide which definition of height best answers a particular surface question.

## From lipid-carrier experiments to molecular construction

The idea of connecting hydrophilic polymers to lipids developed alongside efforts to change how lipid carriers behave in biological environments. In 1990, Klibanov and colleagues investigated liposomes containing PEG-linked lipids, including their behavior in serum and their circulation in vivo. A liposome is a small compartment enclosed by a lipid bilayer, with water on both sides. Changing its outer composition changes the material that first encounters its surroundings. Such experiments raised a specific molecular question: how can modifying a fraction of the surface molecules alter the behavior of a much larger carrier?

Following that question requires a view of the molecular arrangements beneath experimental averages. In 2011, Lee and Pastor used coarse-grained PEG models to study assemblies containing PEG lipids, connecting polymer parameters, composition, and aggregate morphology. The useful historical connection here is between scales. Information at atomic resolution helps define interactions between chain fragments; a coarser representation allows more chains and lipids to move together. Models developed at different times have distinct mappings and parameters. For the present Martini 3 system, the actual topology and interaction files determine both chemical connectivity and the forces used in the calculation.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g16/en/#en-s2)

Figure 1 · Three scales in PEG-lipid research: carrier experiments, coarse-grained assembly, and reproducible molecular construction. Shapes illustrate the associated scientific questions.

As molecular systems became more elaborate, constructing a starting model became an important scientific step. Adding dozens of polymer units to selected membrane lipids requires both correct chemical order and manageable initial overlaps. The Polyply framework, described in 2022, combines molecular connectivity, parameter fragments, and coordinate growth to generate such structures according to explicit rules. We use its PEGylated-membrane construction route: INSANE places the lipids, Polyply adds the chains, and dynamics relaxes the complete system. A growth-direction instruction determines the starting arrangement. Subsequent motion follows the force field and simulation conditions.

To understand why a chain might extend, first consider how many arrangements it can adopt. A flexible rope has many ways to fold around its attachment. Crowding makes some arrangements more costly, so polymer segments redistribute into the surrounding water. Outward extension may relieve local crowding while reducing the freedom to turn back. Solvent compatibility also influences which arrangements are favorable. The competition involves conformational entropy and interaction energy. A picture of mutually repelling rigid rods misses the freedom that allows real chain ends to return close to the membrane.

This history gives us three connected tasks. Experiments identify a surface function worth explaining; molecular modeling specifies the interactions retained at a chosen scale; construction tools specify how a starting structure is assembled. We now turn those tasks into a measurable pair of systems. Our membrane is a periodic planar model with mobile water and ions and covalently attached polymers. Protein adsorption, blood components, carrier curvature, and circulation involve additional physical objects and observation scales. A study directed at those behaviors would introduce the relevant molecules and geometry while retaining clearly defined surface measurements.

## Identify one grafted molecule: beads, mass, and charge

The PEG-linked lipid is called PEL in this example. It consists of one POPE lipid fragment, 50 EO units, and one OHter terminal unit: 63 coarse-grained beads altogether. Twelve belong to the lipid anchor and 51 to the polymer. The surrounding membrane lipid is POPC. The PC and PE names identify different polar headgroups, while the specific connection parameters define how PEG joins its anchor. The Polyply sequence lists the fragments explicitly. Reading that sequence establishes the molecular identity before a rendered structure is used to inspect its geometry.

A bead name, a bead type, and an electric charge are separate fields. The PEL attachment bead retains the name NH3, but its type is P5 and its charge is zero. The neighboring PO4 bead has type Q5 and charge −1 in units of the elementary charge, giving PEL a net charge of −1. Names identify sites in the topology; the charge column controls electrostatic calculation. Ten PEL molecules in the sparse system require ten singly charged sodium ions for neutrality. Fifty PEL molecules in the dense system require fifty. This count helps detect accidental use of the charge state of an unmodified lipid.

Mass must also come from the current model. Each of the 50 EO beads has mass 45 u, and the OH terminal bead has mass 36 u. The selected 51-bead PEG portion therefore has model mass 2286 u. These are the masses used in the dynamics and mass-weighted observables. Treating every bead equally would give the terminal bead a different relative weight. We retain the actual masses when calculating the center of mass, mass-mean height, and radius of gyration. The twelve anchor beads perform their membrane role but remain outside the PEG-only size sums.

The construction route specifies a particular cross interaction: the Lennard–Jones energy parameter between PEG type SN3r and phosphate type Q5 is 3.0 kJ/mol, with length parameter 0.43 nm. The energy parameter controls the well depth and also changes the force at a specified separation. Reducing it makes this pair's attractive well shallower. We retain the prescribed PEGylated-membrane value and leave other parameters unchanged. This lesson uses the lipid-v1 file and its compatible linking rules. The 2025 lipid-v2 definitions used for DSPC in the preceding lesson form a different parameter combination whose connections must be checked before substitution.

A PEG–phosphate nonbonded pairEq. 1

![A PEG–phosphate nonbonded pair](https://ml-biomat.com/static/agent-math/f54c3700fad433a3ffb76d13.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| U(r) | Unshifted LJ pair energy at separation r | kJ/mol |
| r, rₘᵢₙ | Bead separation; distance at the well minimum | nm |
| ε | Pair well depth, set to 3.0 | kJ/mol |
| σLJ | LJ length parameter, 0.43; distinct from graft density | nm |
| σLJ/r | Dimensionless distance ratio | 1 |
| 4, 2, 6, 12, 1/6 | Constants and exponents; superscripts indicate powers | 1 |
| =, −, /, ( ), [ ] | Equality, subtraction, division, grouping; adjacent quantities multiply | 1 |

Reading the relationshipThe positive short-range term rises steeply; the negative term creates attraction at larger separations. Epsilon sets well depth and sigma sets the length scale.

A worked exampleFor sigma = 0.43 nm, the minimum lies near 0.48266 nm, with unshifted energy −3.0 kJ/mol. The run additionally shifts the potential at its cutoff.

ConditionsThis describes the specified pair LJ term; the full model also contains electrostatic and bonded terms, with a 1.1 nm run cutoff.

The following program locates the unique cross-interaction row, checks the length and original energy values, and applies the prescribed correction. An already corrected file remains unchanged; an unexpected value produces a specific diagnostic. The operation is thus inspectable at the parameter level. Complete the Polyply and INSANE installation described in the preparation page, then place the four supplied Martini parameter files in the working directory. Topology generation and dynamics will use the same definitions. Keeping those files with the generated molecule also makes a later comparison of parameter choices straightforward.

### Set the PEG–phosphate cross interaction

```
"""Apply the PEG–phosphate interaction specified by the Polyply tutorial.

The Q5–SN3r Lennard-Jones epsilon becomes 3.0 kJ/mol; sigma stays 0.43 nm.
Running this on an already corrected file leaves its bytes unchanged.
"""
from pathlib import Path
import argparse
import math

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", type=Path, default=Path("martini_v3.0.0.itp"))
    args = parser.parse_args(); lines = args.file.read_text().splitlines()
    matches = []
    for index, line in enumerate(lines):
        fields = line.split(";")[0].split()
        if len(fields) == 5 and set(fields[:2]) == {"Q5", "SN3r"}:
            matches.append((index, fields))
    if len(matches) != 1:
        raise ValueError("Expected exactly one Q5–SN3r pair entry")
    index, fields = matches[0]
    if not math.isclose(float(fields[3]), .43, abs_tol=1e-10):
        raise ValueError("Unexpected pair sigma")
    old = float(fields[4])
    if math.isclose(old, 3.0, abs_tol=1e-10):
        print("Q5–SN3r already uses epsilon 3.0 kJ/mol and sigma 0.43 nm")
    elif math.isclose(old, 4.175, abs_tol=1e-10):
        lines[index] = " ".join([*fields[:4], "3.0"])+" ; PEG-phosphate correction prescribed by original Polyply tutorial"
        args.file.write_text("\n".join(lines)+"\n", encoding="utf-8", newline="\n")
        print("Q5–SN3r epsilon: 4.175 -> 3.0 kJ/mol; sigma retained at 0.43 nm")
    else:
        raise ValueError("Pair parameters differ from both defined input states")
```

Check the unique type pair and original parameters, then apply the prescribed epsilon.

The model contains both bonded and nonbonded parameters. Bonded terms describe connections between adjacent beads, changes in bond angles, and the local geometry linking PEG to its lipid. Nonbonded terms describe attraction and repulsion between sites without a direct chemical connection. Topology bonds maintain the continuity of the chain; its preference for water, phosphate groups, or other segments depends on the associated nonbonded interactions. Changing a pair interaction does not regenerate molecular connectivity. Inspection therefore follows two linked questions: whether the molecule is connected correctly, and whether the chosen interactions describe the intended parameterized model.

## Connect each chain to the correct lipid

Construction begins with an 8 nm by 8 nm membrane. INSANE places POPC and POPE according to their relative amounts, producing 100 lipids in each leaflet: 95 POPC and 5 POPE for the sparse case, or 75 and 25 for the dense case. POPE then becomes the anchor portion of PEL, and Polyply adds PEG from its connection site. Coordinate order must match molecular order in the topology because GROMACS assigns positions to topology entries sequentially. Correct totals with incorrect ordering can still assign polymer parameters to the wrong coordinates.

The next program reads every lipid and writes topology blocks in the order actually present. It also uses headgroup positions to determine the leaflet of each anchor and specifies outward growth for the dense construction. Each restriction refers to the correct system-molecule index, including when molecule types occur in multiple consecutive blocks. The box is orthorhombic: all six off-diagonal values in its nine-number representation are zero. The program writes the equivalent three edge lengths for the coordinate builder. This changes the representation while preserving the membrane positions and box dimensions.

### Build topology in coordinate order

```
from pathlib import Path
from itertools import groupby
from collections import Counter
import json
lines=Path('bilayer.gro').read_text().splitlines();n=int(lines[1]);atoms=lines[2:2+n]
box=[float(v) for v in lines[-1].split()]
if len(box)==9:
    assert all(abs(v)<1e-12 for v in box[3:]),'This construction uses an orthorhombic box'
    lines[-1]=' '.join(f'{v:10.5f}' for v in box[:3]);Path('bilayer.gro').write_text('\n'.join(lines)+'\n')
groups=[list(v) for _,v in groupby(atoms,key=lambda l:l[:10])]
assert all(len(g)==12 for g in groups)
phosphates=[float(l[36:44]) for l in atoms if l[10:15].strip()=='PO4'];mid=sum(phosphates)/len(phosphates)
species=[];report=[];build=[]
for i,g in enumerate(groups):
    name=g[0][5:10].strip();assert name in ['POPC','POPE'];species.append('PEL' if name=='POPE' else name)
    head=next(l for l in g if l[10:15].strip() in ['NC3','NH3']);z=float(head[36:44]);side=1 if z>mid else -1
    report.append(dict(index=i,original=name,molecule=species[-1],head_z_nm=z,leaflet=side))
    if name=='POPE':build.append(f'[ molecule ]\nPEL {i} {i+1}\n[ rw_restriction ]\nEO 0 100 0 0 {side} 90\n')
top=''.join(f'#include "{s}"\n' for s in ['martini_v3.0.0.itp','martini_v3.0.0_ions_v1.itp','martini_v3.0.0_solvents_v1.itp','martini_v3.0.0_phospholipids_v1.itp','PEL.itp'])
top+='[ system ]\nPEGylated membrane\n[ molecules ]\n'
top+=''.join(f'{name} {len(list(g))}\n' for name,g in groupby(species))
Path('system.top').write_text(top);Path('growth.bld').write_text('\n'.join(build))
Path('bilayer-audit.json').write_text(json.dumps(dict(lipids=len(groups),molecules=dict(Counter(species)),midplane_nm=mid,leaflet_counts={str(side):dict(Counter(r['molecule'] for r in report if r['leaflet']==side)) for side in [-1,1]},molecule_order=report),indent=2))
```

Check composition, leaflet membership, and dense-case growth ranges molecule by molecule.

The sparse system uses unrestricted random growth. The dense system uses random growth into the outward half-space, reducing severe initial crowding and interpenetration. Think of this as choosing a manageable starting arrangement for flexible strings. It influences early relaxation, while the later dynamics has no continuing command to point each chain outward. The dense box is 33 nm high and the sparse box 20 nm high, leaving space for initial chains and water. The lipid and polymer construction steps use the same height within each case so that the membrane center and subsequent water placement remain consistent.

Random seeds specify the sampled construction sequence. The small wrapper below sets Python and NumPy random states before calling Polyply. The complete shell script uses fixed INSANE and chain-growth seeds, then combines parameter generation, membrane placement, molecule-order inspection, and chain growth. Seeds govern random choices within a particular implementation; software versions, parameter libraries, and input geometry also contribute to the resulting structure. Follow the file flow through the script: fragment definitions generate PEL parameters, lipid coordinates become a grafted membrane, and full dynamics settings are written for the resulting system.

### Set coordinate-growth random states

```
import random,sys,runpy,shutil
import numpy as np
seed=int(sys.argv[1]);random.seed(seed);np.random.seed(seed)
entry=shutil.which('polyply');assert entry
sys.argv=[entry,*sys.argv[2:]];runpy.run_path(entry,run_name='__main__')
```

Set Python and NumPy seeds before invoking Polyply.

### Generate the complete grafted membrane

```
#!/usr/bin/env bash
set -euo pipefail
fraction=${1:-5}
case "$fraction" in
  5) height=20; other=95; growth=() ;;
  25) height=33; other=75; growth=(-b growth.bld) ;;
  *) echo "Choose 5 or 25 percent PEL" >&2; exit 2 ;;
esac
export INSANE_SEED=$((20261600 + fraction))
python patch_interaction.py
polyply gen_params -f martini_v3.0.0_phospholipids_v1.itp -lib martini3 -o PEL.itp -name PEL -seq POPE:1 EO:50 OHter:1 > topology-generation.log 2>&1
insane -l "POPC:$other" -l "POPE:$fraction" -o bilayer.gro -dz "$height" -x 8 -y 8 -pbc rectangular > insane.log 2>&1
python build_topology.py
python seeded_polyply.py "$((20261650 + fraction))" gen_coords -p system.top -o polymer-bilayer.gro -res EO OHter -c bilayer.gro -name PEGylated -box 8 8 "$height" -split POPE:HEAD-NH3:TAIL-PO4,GL1,GL2,C1A,D2A,C3A,C4A,C1B,C2B,C3B,C4B "${growth[@]}" > coordinate-generation.log 2>&1
python write_parameters.py --fraction "$fraction"
```

Pass 5 or 25 for the sparse or dense construction; first install the modeling tools described on the preparation page.

The split option is worth reading carefully. It identifies the attachment bead separately from the remainder of the lipid during coordinate construction, allowing growth to start from the correct connection while preserving the existing membrane geometry. The final topology retains the chemical connection. The res option identifies residues needing coordinates, while the already placed lipid supplies the structural reference. Matching these options to the 63 beads in the generated molecule shows how a long command separately handles the existing fragment, newly added fragment, and their junction. The topology then gives GROMACS the complete connected molecule.

The reference package also contains both constructed membranes, allowing solvation to begin directly from those structures. For construction from scratch, use separate directories containing the common scripts and parameter files, and pass 5 or 25 to the construction script. To continue from the supplied structures, copy the grafted coordinates, system topology, and leaflet-audit file from the appropriate fraction directory into each working directory. Both routes use the same molecular model. Retain the chosen starting structure when interpreting the trajectory, especially the outward-growth condition in the dense case: its relaxation is visible in the height curves.

## Relax the water, ions, polymers, and membrane together

Geometric water placement around a grafted membrane can leave some water beads inside the hydrophobic tail core. We remove water within 1.5 nm of the initial membrane midplane along the normal and update the topology with the retained count. The procedure changes initial water placement while retaining lipid and polymer coordinates. This 1.5 nm value defines a construction exclusion half-thickness. Polymer heights measured later have a different reference and meaning. During production, the exclusion slab supplies no external wall; water and other particles move according to their interactions.

### Remove initial water from the membrane core

```
from pathlib import Path
import json
lines=Path('water-added.gro').read_text().splitlines();n=int(lines[1]);atoms=lines[2:2+n];box=[float(x) for x in lines[-1].split()]
mid=json.loads(Path('bilayer-audit.json').read_text())['midplane_nm']
kept=[];removed=0;water=0
for l in atoms:
    iswater=l[5:10].strip()=='W'
    dz=float(l[36:44])-mid;dz-=box[2]*round(dz/box[2])
    if iswater and abs(dz)<1.5:removed+=1;continue
    if iswater:water+=1
    kept.append(l[:15]+f'{(len(kept)+1)%100000:5d}'+l[20:])
Path('solvated.gro').write_text('PEGylated membrane with tail core excluded from water placement\n'+f'{len(kept):5d}\n'+'\n'.join(kept)+'\n'+lines[-1]+'\n')
Path('topol.top').write_text(Path('system.top').read_text()+f'W {water}\n')
Path('solvation-audit.json').write_text(json.dumps(dict(water_beads_before=water+removed,water_beads_after=water,removed_tail_core_beads=removed,excluded_half_thickness_nm=1.5,midplane_nm=mid),indent=2))
```

Exclude W beads within the 1.5 nm core half-thickness and update the count.

After water cleanup and charge neutralization, the 5% system contains 10,575 beads: 190 POPC, 10 PEL, 7,655 water beads, and 10 sodium ions. The 25% system contains 16,198 beads: 150 POPC, 50 PEL, 11,198 water beads, and 50 sodium ions. A Martini W bead represents the behavior of several water molecules at this resolution. Different box heights give different water counts. Our comparison focuses on individual chains and leaflet area, with explicit normalization, so increasing the total chain count or solvent volume does not automatically enlarge a plotted height probability density.

Some initial segments may approach closely, so the workflow first minimizes energy and then increases the dynamics step gradually. It uses 20 ps at 2 fs, 100 ps at 5 fs, and 2 ns at 20 fs before recording 20 ns. Minimization finds a nearby lower-potential-energy configuration. Dynamics preparation lets velocities, solvent, and polymer conformations adjust together. The larger timestep relies on the timescales of this coarse-grained potential and the observed stability of this run. A model retaining fast atomic vibrations requires its own integration conditions.

Every dynamics stage uses a 300 K thermostat and semiisotropic pressure coupling at 1 bar. The two lateral directions scale together, while the normal direction responds separately. Electrostatics uses a reaction field with dielectric constant 15 and a 1.1 nm real-space cutoff; the neighbor-list range is 1.35 nm. These settings belong with the Martini parameters. The program below writes all stage inputs, and checkpoint information carries the dynamical and coupling state into each subsequent stage. Production saves 201 structures from 0 to 20 ns at 0.1 ns intervals, exposing both slow changes and chain-to-chain differences in this record.

### Write complete settings for every stage

```
"""Write full MDP inputs for the 5 or 25 percent PEL membrane."""
from pathlib import Path
import argparse

EM = """integrator = steep
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
"""

BASE = """integrator = md
dt = 0.02
nsteps = 1000000
comm-mode = Linear
nstcomm = 100
comm-grps = System
nstxout = 0
nstvout = 0
nstfout = 0
nstlog = 10000
nstenergy = 500
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
ref-t = 300
gen-vel = no
gen-temp = 300
gen-seed = 20261625
pcoupl = c-rescale
pcoupltype = semiisotropic
tau-p = 4.0
ref-p = 1 1
compressibility = 3e-4 3e-4
constraints = none
constraint-algorithm = Lincs
lincs-order = 8
lincs-warnangle = 90
lincs-iter = 2
ld-seed = 20261658
continuation = yes
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fraction", type=int, choices=[5, 25], required=True)
    parser.add_argument("--out", type=Path, default=Path("."))
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    values = dict(line.split(" = ", 1) for line in BASE.splitlines())
    (args.out/"em.mdp").write_text(EM, encoding="utf-8", newline="\n")
    stages = [("preflight", ".002", 10000), ("relax", ".005", 20000),
              ("equil", ".02", 100000), ("md", ".02", 1000000)]
    for index, (stage, dt, steps) in enumerate(stages):
        parameters = dict(values)
        parameters.update(dt=str(float(dt)), nsteps=str(steps))
        parameters["gen-vel"] = "yes" if index == 0 else "no"
        parameters["gen-seed"] = str(20261620+args.fraction)
        parameters["ld-seed"] = str(20261650+args.fraction+index)
        parameters["continuation"] = "no" if index == 0 else "yes"
        content = "".join(f"{key} = {value}\n" for key, value in parameters.items())
        (args.out/f"{stage}.mdp").write_text(content, encoding="utf-8", newline="\n")
    print("Wrote em, preflight, relax, equil, and md parameter files")
```

Use --fraction 5 or 25 to write the five MDP files matching that recorded run.

### Solvate, neutralize, relax, and record

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
python=${PYTHON:-python3}
"$gmx" solvate -cp polymer-bilayer.gro -cs water.gro -radius 0.21 -o water-added.gro > solvate.log 2>&1
"$python" clean_water.py
"$gmx" grompp -f em.mdp -c solvated.gro -p topol.top -o ions.tpr > ions.grompp.log 2>&1
printf 'W\n' | "$gmx" genion -s ions.tpr -o ions.gro -p topol.top -pname NA -nname CL -neutral -seed 20261601 > genion.log 2>&1
"$gmx" grompp -f em.mdp -c ions.gro -p topol.top -o em.tpr > em.grompp.log 2>&1
"$gmx" mdrun -deffnm em -ntmpi 1 -ntomp 2 -pin off > em.stdout.log 2>&1
"$gmx" grompp -f preflight.mdp -c em.gro -p topol.top -o preflight.tpr > preflight.grompp.log 2>&1
"$gmx" mdrun -deffnm preflight -ntmpi 1 -ntomp 2 -pin off > preflight.stdout.log 2>&1
prev=preflight
for stage in relax equil md; do
  "$gmx" grompp -f "$stage.mdp" -c "$prev.gro" -t "$prev.cpt" -p topol.top -o "$stage.tpr" > "$stage.grompp.log" 2>&1
  "$gmx" mdrun -deffnm "$stage" -ntmpi 1 -ntomp 2 -pin off > "$stage.stdout.log" 2>&1
  prev=$stage
done
printf 'Temperature\nPotential\nPressure\nVolume\nDensity\nBox-X\nBox-Y\nBox-Z\n0\n' | "$gmx" energy -f md.edr -o md-properties.xvg > energy.log 2>&1
"$gmx" check -f md.xtc > trajectory-check.log 2>&1
```

Start from grafted membrane coordinates and system topology, passing checkpoints between stages.

### Start a complete calculation from the supplied membrane

```
#!/usr/bin/env bash
set -euo pipefail
fraction=${1:-5}
case "$fraction" in 5|25) ;; *) echo "Choose 5 or 25" >&2; exit 2 ;; esac
mkdir -p "work/$fraction"
cp martini_v3.0.0.itp martini_v3.0.0_ions_v1.itp \
   martini_v3.0.0_solvents_v1.itp martini_v3.0.0_phospholipids_v1.itp \
   PEL.itp water.gro clean_water.py write_parameters.py run.sh "work/$fraction/"
cp "fraction-$fraction/polymer-bilayer.gro" \
   "fraction-$fraction/system.top" "fraction-$fraction/bilayer-audit.json" "work/$fraction/"
cd "work/$fraction"
python3 write_parameters.py --fraction "$fraction"
bash run.sh
```

Run bash start.sh 5 or bash start.sh 25 in the package examples directory; each command copies inputs into its own work subdirectory and runs the stages.

Each stage supplies the next with its output state. Coordinates give positions, checkpoints carry velocities and state information needed for continuation, and a new MDP defines how the next stage proceeds. Production time starts again at zero, so preparation has already taken place before the plotted 0 ns. The 20 ns label describes the recorded stage. Integration and storage have very different intervals: coordinates are advanced every 20 fs, while structural analysis reads a saved frame every 100 ps. One controls numerical propagation; the other controls which details can be examined retrospectively from the saved trajectory.

The production starting point already indicates what deserves attention. In the sparse system, PEG mass-mean height is approximately 0.96 nm and mean terminal height 1.50 nm. In the dense system, the corresponding values are about 3.58 and 6.20 nm, with many chains still extended. The trajectories show sparse chains spreading outward and dense chains partly retracting. Reading these evolutions together explains more than comparing two final numbers. It also motivates independent simulations that begin from several different conformational arrangements when estimating reproducible density-dependent behavior.

## Composition and surface crowding are different quantities

The formulation percentages describe the fraction of lipid-anchored molecules carrying PEG. Surface crowding is described more directly by the number of grafted chains in one leaflet divided by its projected membrane area. The two leaflets face opposite water layers. For the upper surface, use the upper chain count and the lateral membrane area; combining both leaflet counts with that area would double the density. Pressure coupling changes the area with time, so a fixed chain population still produces a time-dependent grafting density.

Composition fraction and graft density per leafletEq. 2

![Composition fraction and graft density per leaflet](https://ml-biomat.com/static/agent-math/1b44044187c226f60392eb3c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| f | Fraction of lipid molecules carrying PEG | 1 |
| NPEL, NPOPC | Counts of both species over the same leaflet or whole-system scope | 1 |
| N g | Grafted chains in one leaflet, 5 or 25 | 1 |
| t | Observation time | ns |
| Lₓ, Lᵧ | Lateral orthorhombic box lengths | nm |
| A | Projected lateral area of one leaflet | nm² |
| Γ | Grafted chains per area of one leaflet | nm⁻² |
| =, +, /, ( ) | Equality, addition, division; parentheses indicate time; adjacent lengths multiply | 1 |

Reading the relationshipA composition fraction has no spatial information; dividing chain count by area connects formulation to actual membrane geometry.

A worked exampleFor five grafts among 100 lipids in a leaflet, f = 0.05. At area 65 nm², Gamma = 5/65 = 0.076923 nm⁻².

ConditionsProjected density for a planar orthorhombic box; count each leaflet separately. Compute Gamma framewise before averaging.

During the final 10 ns, the sparse membrane has mean projected area about 65.358 nm² and five chains per leaflet. Calculating density frame by frame gives a mean of 0.07651 nm⁻². The dense membrane has mean area about 68.738 nm², 25 chains per leaflet, and mean density 0.36374 nm⁻². Chain count increases fivefold, whereas density increases approximately 4.75-fold because the areas differ. Averaging framewise densities differs slightly from dividing the count by mean area. We use the former definition so that the instantaneous geometry enters each measurement consistently.

### Membrane area and graft density

Framewise projected area and graft density per leaflet; shading marks the final 10 ns.

Martini 3 lipid v1 and Polyply PEG50 models. Each membrane has 200 lipids with 5% or 25% PEL, giving 5 or 25 PEG chains per leaflet. Both are sampled for 20 ns at 300 K and 1 bar, retaining distinct water boxes, sodium populations and construction states. Q5–SN3r uses the original tutorial’s epsilon of 3.0 kJ/mol.

[Download reference data and complete inputs (ZIP) 21.26 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-pegmembrane-comparison-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g16/en/#en-s6)

Projected membrane areas and graft densities per leaflet over 201 frames in each system. Shading marks the 101-frame final 10 ns; each density divides the actual graft count per leaflet by that frame’s membrane area.

The inverse area density also supplies an intuitive length. Divide the area among the grafted chains and take the square root of the area per chain. This characteristic spacing is approximately 3.62 nm for the sparse case and 1.66 nm for the dense case. It resembles the spacing obtained by assigning irregular grafting positions to equal square cells. Actual nearest-neighbor distances also depend on spatial organization and lateral lipid motion. The estimate converts an abstract number of chains per square nanometer into a distance that can be compared with a polymer's spatial extent.

Estimate spacing and footprint overlapEq. 3

![Estimate spacing and footprint overlap](https://ml-biomat.com/static/agent-math/fa011b4207454444bd4093ca.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| d | Square root of mean area per chain, a characteristic spacing | nm |
| Γ | Graft density per leaflet | nm⁻² |
| R₀ | Independently specified reference footprint radius | nm |
| π | Pi, approximately 3.14159 | 1 |
| R₀², πR₀² | Squared radius; circular reference footprint area | nm² |
| χ | Reference footprint area divided by area per chain | 1 |
| −1/2, ², = | Power −1/2 means reciprocal square root; square and equality; adjacent quantities multiply | 1 |

Reading the relationshipArea per chain is 1/Gamma; its square root gives a length. Multiplying density by a reference footprint gives a dimensionless overlap measure.

A worked exampleAt Gamma = 0.25 nm⁻² and R0 = 1 nm, d = 2 nm and chi = pi/4 ≈ 0.7854.

ConditionsGeometric estimates using uniformly assigned areas and circular footprints; actual nearest neighbors and conformational changes require molecular trajectories.

[Figure: Reference circular footprints and area per chain](https://ml-biomat.com/tutorials/molecular-dynamics/g16/en/#en-s6)

A geometric model with uniformly placed attachments and circular coil footprints; nine neighboring area cells are shown, while the input count defines density over the complete leaflet.

The interaction draws circular footprints for a chosen reference coil radius and compares their areas with the area available per chain. A larger footprint-to-cell ratio indicates greater potential spatial overlap for that reference size. The reference radius is an input to this geometric example; it would normally be obtained from a separate dilute-chain or sparse-grafting measurement. A dense grafted chain's measured gyration radius already reflects its environment and needs a separate interpretation. Overlapping circles represent overlapping spatial scales. Actual polymers remain flexible, water-filled conformations with internal gaps and backfolds.

Surface mobility also matters. Grafting sites on a solid may be fixed by the underlying material, whereas the PEG-bearing lipids here can move within their leaflet and change neighbors. The dense system can therefore display local density fluctuations as well as a larger mean density. Interactions between PEG and headgroups can influence those local arrangements. A study of clustering or uniform coverage would add two-dimensional distances and spatial distributions of attachment sites, together with the area record. That analysis separates average crowding from the organization of particular neighboring chains.

## A chain has more than one useful height

To measure outward extension, first choose a reference that moves with each chain. We use its PEL NH3 attachment bead, subtract that bead's normal coordinate, and define outward as positive: upward for the upper leaflet and downward for the lower one. Chains pointing into either water layer then have positive outward height, and translating the entire membrane leaves the measure unchanged. Before subtracting coordinates, the program reconstructs each molecule along its topology bonds and checks every bond length. A chain crossing a periodic boundary is thereby represented continuously for geometric measurement.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g16/en/#en-s7)

Figure 2 · Both leaflets define outward into water as positive, measured relative to each chain’s NH3 attachment. Chain shapes and membrane thickness illustrate the coordinate definition.

Outward heights relative to the attachmentEq. 4

![Outward heights relative to the attachment](https://ml-biomat.com/static/agent-math/8538bee70d1ed2fd988fd96c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| c, i, 0, 51 | Chain index, PEG bead index; 0 denotes NH3 attachment, 51 the OH end | 1 |
| s c | +1 in upper leaflet and −1 in lower, so outward is positive | 1 |
| zci, zc0 | Normal coordinates of PEG and attachment in the reconstructed molecule | nm |
| hci, Hc, Hc,end | Bead height, chain mass-mean height, and terminal height | nm |
| mi, M | Bead mass; total selected PEG mass 2286 | u |
| mi hci | Mass times height | u nm |
| Σ, =, −, /, ( ) | Sum over 51 PEG beads, equality, subtraction, division, grouping; adjacent quantities multiply | 1 |

Reading the relationshipSubtracting each attachment removes translation; the leaflet sign unifies outward direction, and mass weights describe polymer mass location.

A worked exampleFor a lower-leaflet attachment at z = 10 nm and endpoint at 7 nm, s = −1 gives outward terminal height 3 nm.

ConditionsFirst reconstruct the complete PEL along its bonds; only 51 PEG beads enter the mass mean, with the attachment as the origin.

Mass-weighting the heights of the 51 PEG beads gives a chain's mass-mean height. Selecting only the terminal OH bead gives terminal height. Measuring all PEG beads around their own three-dimensional center of mass gives the radius of gyration. These observables answer different questions. A chain spread laterally can have a substantial gyration radius while remaining low above its anchor. An extended terminal segment can change the endpoint strongly while moving only a small fraction of the chain's total mass. A label such as “chain height” therefore needs its particle selection, reference position, and averaging definition.

Three-dimensional radius of gyration of PEGEq. 5

![Three-dimensional radius of gyration of PEG](https://ml-biomat.com/static/agent-math/ef2f5f340c0fad7378b4f475.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| c, i, 51 | Chain index, PEG bead index, selected bead count | 1 |
| rci, rc,cm | PEG position vector and its center of mass | nm |
| mi, M | Bead mass and total selected PEG mass | u |
| Rg,c | Radius of gyration of this chain’s PEG portion | nm |
| ‖rci−rc,cm‖² | Squared distance to the center of mass | nm² |
| mi‖rci−rc,cm‖² | Mass times squared distance | u nm² |
| Σ, √, =, −, /, 1 | Sum, square root, equality, vector subtraction, division, constant one; adjacent quantities multiply | 1 |

Reading the relationshipThe center follows PEG as a whole; averaging squared distances measures its spread in all directions.

A worked exampleFor two equal-mass points separated by 2 nm, the center is midway and each is 1 nm away, giving Rg = 1 nm.

ConditionsUse the 51 PEG beads, native masses, and reconstructed coordinates; take the square root per chain before averaging Rg.

### Recorded evolution of three chain dimensions

Measure each chain per frame, then average over all chains in that system.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g16/en/#en-s7)

Each chain’s NH3 grafting site defines zero height. Mass-mean height, terminal height and PEG radius of gyration are measured separately, with directions aligned to the outward normal of each leaflet.

Over the final 10 ns, sparse and dense systems have PEG mass-mean heights of 1.717 and 3.031 nm, terminal mean heights of 2.356 and 4.630 nm, and PEG gyration radii of 1.782 and 2.082 nm. Polymer mass and endpoints extend farther outward in the dense case, while the change in overall gyration radius is smaller. Redistributing a chain along the surface normal need not enlarge every measure of its three-dimensional size by the same factor. The dense-chain curves also show substantial early retraction and continued later variation, so the comparison retains its specified 20 ns observation window.

Another structure lies beneath these means: individual endpoints differ greatly within the same frame. We calculate the population standard deviation of all chain-end heights in each frame, then average that spread over the final 10 ns. The sparse and dense values are approximately 1.739 and 2.156 nm. This describes dispersion across the complete chain population, using the chain count in the denominator. Fluctuations of the time series instead describe changes in the framewise chain mean, for which the summary table uses a sample standard deviation. More chains can yield a smoother mean curve while preserving a broad individual-chain distribution.

### Terminal height of each chain

Zero-based chain indices and one shared color scale display all 201 frames of both systems.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g16/en/#en-s7)

Outward terminal heights of every chain over the full 20 ns, with a common color scale and actual chain indices. Chains and frames within a system share an environment; the two conditions retain their distinct initial conformations, cell heights and solvent compositions.

The heatmap gives each chain a separate row with its fixed zero-based index. A persistent bright band identifies a chain whose endpoint remains high for part of the trajectory; darker regions identify positions nearer the attachment. Transitions reveal extension and backfolding. Reading along a row shows temporal persistence, while reading vertically compares chains at one time. A negative height places the endpoint on the inward side of its own attachment bead. Determining whether a chain actually crosses the membrane additionally requires the full membrane geometry and the positions of the complete polymer.

## Connect distributions, complete analysis, and research questions

To see where the polymer coating places its mass, divide the normal direction into equal-height bins and count the PEG mass in each. Normalize each chain by its own total mass, average chains with equal weight, then divide by bin width. The resulting probability density has units nm⁻¹ and integrates to one, allowing its shape to be compared across different graft counts. Multiplying by the actual graft density and model mass per chain would instead give a mass distribution per unit surface area. Here the normalized density focuses on how each chain allocates mass along the outward direction.

Height probability density normalized per chainEq. 6

![Height probability density normalized per chain](https://ml-biomat.com/static/agent-math/e3165ee4f76890f8f053f0fb.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| p k | Mass-weighted probability density in height bin k | nm⁻¹ |
| k, f, c, i | Height-bin, frame, chain, and PEG bead indices | 1 |
| F, Nc, 51 | 101 frames, 10 or 50 chains, and PEG beads per chain | 1 |
| Δh, hfci | Bin width 0.25 and bead outward height | nm |
| mi/M | Fraction of the PEG mass belonging to the bead | 1 |
| Bk | Height interval of bin k | Interval in nm |
| 𝕀 | One when the condition holds, zero otherwise | 1 |
| Σ, =, /, Δ, ∈, 1 | Sum, equality, division, interval-width notation, membership, constant one; adjacent quantities multiply | 1 |

Reading the relationshipMass fractions sum to one per chain. Averaging over chains and frames and dividing by bin width gives distributions comparable across chain counts.

A worked exampleIf a 0.25 nm bin contains normalized probability 0.10, its density is 0.10/0.25 = 0.40 nm⁻¹.

ConditionsUse 101 frames from the final 10 ns and bins covering every selected sample; terminal distributions weight each chain endpoint equally.

### Mass and terminal-height distributions

101 frames from the final 10 ns; mass distributions normalize per chain, while endpoints have equal chain weights.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g16/en/#en-s8)

Two height distributions over the final 10 ns. The upper panel normalizes each PEG chain by its model mass and counts bead heights from the graft; the lower panel counts terminal heights. Both systems use common bins and each density integrates to one.

The sparse case concentrates more mass near the attachment, while the dense case retains substantial weight at larger outward heights. Endpoint distributions are broader because local backfolding can relocate a terminal bead without moving the entire chain to the same height. Both distributions use the 101 frames from the final 10 ns, and the plotted bins include every sample in that window. A high probability density means greater weight per unit height; changing bin width can change the peak. Both systems therefore use the same bins and normalization for a direct comparison of distribution shape.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g16/en/#en-s8)

Figure 3 · A three-bead normalization example: masses 45, 45, and 36 u occupy separate 1 nm height bins. Actual PEG has 51 beads, and analysis additionally averages all chains and frames.

The complete analysis below reads masses, molecular boundaries, and bonds from the topology. It reconstructs every PEL frame by frame, checks leaflet populations, molecular charges, and maximum bond length, and calculates the observables. Individual-chain records, frame averages, and summaries are written separately so that a feature in an aggregate plot can be traced to a particular chain. MDAnalysis coordinates are read in ångströms and explicitly converted to nanometers; times in picoseconds become nanoseconds. Chain indices, windows, and units match the figure labels, making later changes to selection or observation range inspectable.

### Complete chain-level analysis of both systems

```
"""Measure PEG50 chains on two recorded lipid membranes.

python analyze_brush.py --low records/5 --high records/25 --out analysis --language en
Each record directory contains md.tpr and md.xtc. Dependencies: MDAnalysis,
NumPy, Matplotlib. Lengths read by MDAnalysis are in angstrom.
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


def connection_plan(group):
    local = {int(v): i for i, v in enumerate(group.indices)}
    edges = np.array([[local[int(a)], local[int(b)]] for a, b in group.bonds.indices])
    graph = [[] for _ in group]
    for k, (a, b) in enumerate(edges):
        graph[a].append((b, k, 1)); graph[b].append((a, k, -1))
    queue, seen, plan = [0], {0}, []
    for a in queue:
        for b, k, sign in graph[a]:
            if b not in seen:
                queue.append(b); seen.add(b); plan.append((a, b, k, sign))
    if len(seen) != len(group):
        raise ValueError("A PEL molecule must have one connected bond graph")
    return edges, plan


def reconstruct(raw, box, edges, plan):
    delta = minimize_vectors(raw[edges[:, 1]]-raw[edges[:, 0]], box)
    whole = np.empty_like(raw, dtype=float); whole[0] = raw[0]
    for a, b, k, sign in plan:
        whole[b] = whole[a]+sign*delta[k]
    observed = whole[edges[:, 1]]-whole[edges[:, 0]]
    if np.max(np.linalg.norm(observed-delta, axis=1)) > .005:
        raise ValueError("A reconstructed bond cycle does not close")
    longest = float(np.linalg.norm(observed, axis=1).max()/10)
    if longest > .7:
        raise ValueError("A coarse-grained PEL bond exceeds 0.7 nm")
    return whole/10, longest


def stats(a):
    return {"mean": float(np.mean(a)), "sd": float(np.std(a, ddof=1)),
            "minimum": float(np.min(a)), "maximum": float(np.max(a))}


def save(fig, path):
    fig.savefig(path.with_suffix(".svg")); fig.savefig(path.with_suffix(".png"), dpi=150)
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--low", type=Path, default=Path("records/5"))
    p.add_argument("--high", type=Path, default=Path("records/25"))
    p.add_argument("--out", type=Path, default=Path("analysis"))
    p.add_argument("--language", choices=["zh", "en"], default="en")
    args = p.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    zh = args.language == "zh"
    present = {f.name for f in font_manager.fontManager.ttflist}
    fonts = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC",
             "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else ["DejaVu Sans"]
    plt.rcParams.update({"font.family": [f for f in fonts if f in present],
                         "font.size": 14, "axes.labelsize": 15,
                         "svg.fonttype": "path", "axes.unicode_minus": False,
                         "axes.spines.top": False, "axes.spines.right": False})
    summaries = []; all_arrays = []; all_chains = []; all_heights = []; snapshots = []
    for fraction, folder, count, waters, atoms in [(5, args.low, 10, 7655, 10575),
                                                 (25, args.high, 50, 11198, 16198)]:
        u = mda.Universe(str(folder/"md.tpr"), str(folder/"md.xtc"))
        pel = u.select_atoms("moltype PEL")
        chains = [pel[pel.molnums == number] for number in np.unique(pel.molnums)]
        if len(chains) != count or len(u.atoms) != atoms or len(u.select_atoms("moltype W")) != waters:
            raise ValueError("Composition differs from the selected recorded model")
        if len(u.select_atoms("moltype NA")) != count or abs(sum(u.atoms.charges)) > 1e-5:
            raise ValueError("Counterion count or total charge differs from the model")
        for chain in chains:
            if len(chain) != 63 or list(chain.names[:2]) != ["NH3", "PO4"]:
                raise ValueError("Expected a 63-bead PEL with NH3 and PO4 first")
            if list(chain.resnames[12:]) != ["EO"]*50+["OHter"]:
                raise ValueError("Expected 50 EO beads followed by one OHter bead")
            if abs(sum(chain.charges)+1) > 1e-5 or not np.allclose(chain.masses[12:], [45]*50+[36]):
                raise ValueError("PEL charge or PEG bead masses differ from the model")
        plans = [connection_plan(c) for c in chains]
        records = []; individual = []; height_frames = []; initial_sides = None
        changes = 0; max_bond = 0.; final_shapes = []
        for frame in u.trajectory:
            if not np.allclose(frame.dimensions[3:], 90):
                raise ValueError("The recorded box must be orthorhombic")
            area = float(frame.dimensions[0])*float(frame.dimensions[1])/100
            rows = []; heights = []; sides = []; shapes = []
            for index, (chain, (edges, plan)) in enumerate(zip(chains, plans)):
                xyz, longest = reconstruct(chain.positions.astype(float), frame.dimensions, edges, plan)
                max_bond = max(max_bond, longest)
                side = 1 if xyz[1, 2] > xyz[[7, 11], 2].mean() else -1
                sides.append(side)
                anchor = xyz[0]; peg = xyz[12:]; mass = chain.masses[12:]
                height = side*(peg[:, 2]-anchor[2]); center = np.average(peg, axis=0, weights=mass)
                mean_height = float(np.average(height, weights=mass))
                rg = float(np.sqrt(np.average(np.sum((peg-center)**2, axis=1), weights=mass)))
                rows.append([float(height[-1]), mean_height, rg]); heights.append(height)
                individual.append([float(frame.time), index, side, float(height[-1]), mean_height, rg])
                shapes.append((xyz-anchor)*[1, 1, side])
            if initial_sides is None:
                initial_sides = np.asarray(sides)
                if [sum(initial_sides > 0), sum(initial_sides < 0)] != [count//2, count//2]:
                    raise ValueError("Unexpected graft count per leaflet")
            changes += int(np.sum(np.asarray(sides) != initial_sides))
            rows = np.asarray(rows)
            records.append([float(frame.time), area, (count//2)/area, *rows.mean(axis=0),
                            float(np.std(rows[:, 0], ddof=0))])
            height_frames.append(heights); final_shapes = shapes
        values = np.asarray(records); individuals = np.asarray(individual)
        heights = np.asarray(height_frames)
        if len(values) != 201 or not np.allclose(values[:, 0], np.arange(201)*100):
            raise ValueError("Expected 201 frames from 0 to 20000 ps")
        late = values[:, 0] >= 10000
        labels = ["area_nm2", "graft_density_per_leaflet_nm-2", "tip_height_nm",
                  "mass_mean_height_nm", "PEG_Rg_nm", "within_frame_tip_sd_nm"]
        summary = {"PEL_fraction_percent": fraction, "grafts_per_leaflet": count//2,
                   "total_beads": atoms, "water_beads": waters, "NA": count,
                   "frames": 201, "late_frames": int(late.sum()), "PEG_beads_per_chain": 51,
                   "PEG_model_mass_u": float(sum(chains[0].masses[12:])),
                   "maximum_bond_nm": max_bond, "leaflet_membership_changes": changes,
                   "initial": dict(zip(labels, values[0, 1:].tolist())),
                   "last10ns": {name: stats(values[late, i+1]) for i, name in enumerate(labels)}}
        summaries.append(summary); all_arrays.append(values); all_chains.append(individuals)
        all_heights.append(heights[late])
        with (args.out/f"fraction-{fraction}.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f); writer.writerow(["time_ps", *labels]); writer.writerows(values)
        with (args.out/f"chains-{fraction}.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f); writer.writerow(["time_ps", "chain_index", "leaflet_side", "tip_height_nm", "mass_mean_height_nm", "PEG_Rg_nm"]); writer.writerows(individuals)
        last = individuals[individuals[:, 0] == 20000]
        selected = np.argsort(last[:, 3])[[0, len(last)//2, -1]]
        for index in selected:
            snapshots.append({"fraction_percent": fraction, "chain_index": int(index),
                              "selection": "minimum, median-index, or maximum terminal height at 20 ns",
                              "tip_height_nm": last[index, 3], "mass_mean_height_nm": last[index, 4],
                              "coordinates_relative_to_graft_nm": final_shapes[index].tolist(),
                              "names": chains[index].names.tolist(), "bonds": plans[index][0].tolist()})
    # Normalize each chain by its model mass, then average chains and frames.
    pooled = np.concatenate([v.ravel() for v in all_heights])
    bins = np.arange(np.floor(pooled.min()/.25)*.25-.25, np.ceil(pooled.max()/.25)*.25+.5, .25)
    mass = np.array([45]*50+[36], dtype=float); mass /= mass.sum()
    densities = []
    for heights in all_heights:
        weights = np.broadcast_to(mass, heights.shape).ravel()/np.prod(heights.shape[:2])
        density, _ = np.histogram(heights.ravel(), bins=bins, weights=weights)
        density /= np.diff(bins)
        if not np.isclose(np.sum(density*np.diff(bins)), 1, atol=1e-12):
            raise ValueError("Height probability density must integrate to one")
        densities.append(density)
    summary = {"window_ps": [10000, 20000], "models": summaries,
               "height_reference": "Signed outward displacement from the NH3-named attachment bead",
               "height_distribution": "PEG bead model-mass probability density; normalized per chain, then averaged across chains and saved frames",
               "time_sd": "Sample SD of frame means, ddof=1; chains within a frame are not independent replicates",
               "height_probability_integrals": [float(np.sum(v*np.diff(bins))) for v in densities]}
    (args.out/"summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (args.out/"snapshots.json").write_text(json.dumps(snapshots), encoding="utf-8")
    np.savetxt(args.out/"height-probability.csv", np.column_stack(((bins[:-1]+bins[1:])/2, *densities)),
               delimiter=",", header="height_nm,fraction5_per_nm,fraction25_per_nm", comments="")
    colors = ["#147d92", "#c66b43"]; labels = ["5% PEL", "25% PEL"]
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True, constrained_layout=True)
    for values, color, label in zip(all_arrays, colors, labels):
        axs[0].plot(values[:, 0]/1000, values[:, 1], c=color, label=label)
        axs[1].plot(values[:, 0]/1000, values[:, 2], c=color, label=label)
    axs[0].set_ylabel("膜面投影面积 / nm²" if zh else "Projected area / nm²")
    axs[1].set_ylabel("每叶片接枝密度 / nm⁻²" if zh else "Graft density per leaflet\n/ nm⁻²")
    axs[1].set_xlabel("生产阶段时间 / ns" if zh else "Production time / ns")
    axs[0].legend(ncol=2); axs[0].set_title("接枝数与实际面积共同决定面密度" if zh else "Graft count and actual area jointly define surface density")
    for ax in axs: ax.axvspan(10, 20, color="#e8d5ac", alpha=.2); ax.grid(alpha=.15)
    save(fig, args.out/"graft-geometry")
    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True, constrained_layout=True)
    names = ["PEG质量平均高度 / nm", "末端平均高度 / nm", "PEG平均回转半径 / nm"] if zh else ["Mean PEG mass height\n/ nm", "Mean terminal height\n/ nm", "Mean PEG radius of gyration\n/ nm"]
    for values, color, label in zip(all_arrays, colors, labels):
        for ax, column in zip(axs, [4, 3, 5]):ax.plot(values[:, 0]/1000, values[:, column], c=color, label=label)
    for ax, name in zip(axs, names):ax.set_ylabel(name);ax.axvspan(10, 20, color="#e8d5ac", alpha=.2);ax.grid(alpha=.15)
    axs[0].legend(ncol=2);axs[-1].set_xlabel("生产阶段时间 / ns" if zh else "Production time / ns")
    axs[0].set_title("高度、末端与整体尺寸的不同变化" if zh else "Height, terminal position, and overall size evolve differently")
    save(fig, args.out/"brush-height")
    fig, axs = plt.subplots(2, 1, figsize=(12, 9), constrained_layout=True)
    centers = (bins[:-1]+bins[1:])/2
    tips = [v[v[:, 0] >= 10000, 3] for v in all_chains]
    tip_bins = np.linspace(min(v.min() for v in tips)-.1, max(v.max() for v in tips)+.1, 35)
    for density, tip, color, label in zip(densities, tips, colors, labels):
        axs[0].plot(centers, density, color=color, lw=2.2, label=label)
        axs[1].hist(tip, bins=tip_bins, density=True, histtype="step", color=color, lw=2.2, label=label)
    axs[0].set(xlabel="距接枝点向外高度 / nm" if zh else "Outward height from the attachment bead / nm",
               ylabel="质量加权概率密度 / nm⁻¹" if zh else "Mass-weighted probability\ndensity / nm⁻¹")
    axs[1].set(xlabel="末端高度 / nm" if zh else "Terminal height / nm",
               ylabel="概率密度 / nm⁻¹" if zh else "Probability density / nm⁻¹")
    axs[0].legend(ncol=2); axs[0].set_title("后10ns：逐链归一化后的高度分布" if zh else "Final 10 ns: height distributions normalized per chain")
    for ax in axs:ax.axvline(0, c="#999999", lw=1);ax.grid(alpha=.15)
    save(fig, args.out/"brush-distribution")
    fig, axs = plt.subplots(2, 1, figsize=(12, 9), constrained_layout=True)
    vmin = min(v[:, 3].min() for v in all_chains); vmax = max(v[:, 3].max() for v in all_chains)
    for ax, chain_values, label in zip(axs, all_chains, labels):
        n = len(np.unique(chain_values[:, 1]));matrix = chain_values[:, 3].reshape(201, n).T
        im = ax.imshow(matrix, origin="lower", aspect="auto", extent=[0, 20, -.5, n-.5],
                       vmin=vmin, vmax=vmax, cmap="viridis", interpolation="nearest")
        ax.set_title(label);ax.set_ylabel("链编号" if zh else "Chain index");ax.set_xlabel("时间 / ns" if zh else "Time / ns")
    fig.colorbar(im, ax=axs, label="末端向外高度 / nm" if zh else "Outward terminal height / nm", shrink=.85)
    save(fig, args.out/"brush-chains")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

Read both TPR/XTC pairs and use explicit bond traversal, native masses, and a common statistical window.

### Generate bilingual figures and tables from reference records

```
#!/usr/bin/env bash
set -euo pipefail
python analyze_brush.py --low records/5 --high records/25 --out results-zh --language zh
python analyze_brush.py --low records/5 --high records/25 --out results-en --language en
```

Each records directory contains md.tpr and md.xtc; separate outputs hold Chinese and English figures.

Each input directory needs md.tpr and md.xtc. The topology tells the program which molecule owns a bead, its mass, and its bonded neighbors; the trajectory provides successive coordinates and box dimensions. CSV outputs retain framewise values, the JSON summary records the window and averaging definitions, and figures support comparison. To introduce another grafting fraction, first verify molecular composition and chain length, then update the explicit composition checks and input paths. The comparison changes in an identified way while its geometry and statistical definitions remain traceable through the same analysis procedure.

A useful next investigation would prepare several independent configurations at each grafting fraction, including both compact and extended chains, and examine whether their distributions approach each other with longer observation. A question about protein approach would require a compatibly parameterized protein, specified initial positions and orientations, and a defined approach coordinate, while tracking polymer and water rearrangements. A curved carrier would require geometry with a specified curvature. Each extension adds a physical object and a corresponding measurement; the existing graft-density and height definitions provide a foundation for those comparisons.

After this lesson, the statement “more PEG was attached to the surface” can lead to three precise questions: how many chains occupy each actual surface area, where does their mass lie, and how much do chains and times differ? The two 20 ns records answer those questions for their specified preparations and show how initialization remains visible in the evolution. Connecting molecular identity, spatial reference, and statistical averaging turns a visually fluffy molecular image into a reproducible description of an interface. That description can guide both additional simulation and the design of complementary experimental measurements.

## Further Reading and Open Materials

- [PEGylated Lipid Bilayers](https://polyply.github.io/polyply_1.0/tutorials/pegylated-lipid-bilayers/) · Fabian Grünewald and Polyply contributors · Apache-2.0

  PEG50–POPE connection, 5% and 25% construction, directed growth, and PEG–phosphate interaction specification.

  Read actual molecule order, use a consistent 20 nm sparse starting box, fix seeds, and add staged dynamics and full analysis.
- [Polyply: a Python suite for facilitating simulations of macromolecules and nanomaterials](https://doi.org/10.1038/s41467-021-27627-4) · Fabian Grünewald and colleagues · CC BY 4.0 (paper); Apache-2.0 (software)

  Principles and history of molecular connectivity, parameter fragments, and coordinate generation.

  Use fixed source commit 38d4d5424e1ef35c86e7cb8532fbd86ecf997221.
- [Martini Force Fields](https://github.com/Martini-Force-Field-Initiative/martini-forcefields) · Martini Force Field Initiative · Apache-2.0

  Martini 3 v3.0.0 base and lipid, ion, and solvent v1 parameters.

  Apply the Polyply-prescribed Q5–SN3r epsilon change from 4.175 to 3.0 kJ/mol, retaining sigma 0.43 nm.
- [INSANE](https://github.com/Tsjerk/Insane) · Tsjerk A. Wassenaar and contributors · GPL-2.0 (software)

  Initial POPC/POPE membrane coordinate generation.

  Use fixed seeds, compositions, and box dimensions; topology follows the actual generated molecule order.
- [Amphipathic polyethyleneglycols effectively prolong the circulation time of liposomes (1990)](https://doi.org/10.1016/0014-5793%2890%2981016-H) · Alexander L. Klibanov; Kazuo Maruyama; Vladimir P. Torchilin; Leaf Huang · Copyright publisher; historical facts cited

  Experimental carrier context for PEG-linked lipids.

  Explain the scientific question with independently drawn concept figures.
- [Coarse-grained model for PEGylated lipids: effect of PEGylation on the size and shape of self-assembled structures (2011)](https://doi.org/10.1021/jp2020148) · Hwankyu Lee; Richard W. Pastor · Author manuscript publicly readable; cited historical facts

  History of PEG-lipid coarse graining and aggregate morphology.

  Discuss scale and scientific questions; this example uses its specified Martini 3 parameter combination.
