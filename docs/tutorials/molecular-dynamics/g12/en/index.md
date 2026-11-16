# Sugar Shape and the Water Around It

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g12/en/
Language: en

Use an atomistic trehalose trajectory to understand glycosidic rotation, circular statistics, and hydration, connecting chemical identity to molecular shape and materials questions.

## Why sugars deserve their own molecular models

Stir a spoonful of sugar into water and the visible crystals gradually disappear. At the molecular scale, this familiar event has a more detailed description: water approaches oxygen and hydrogen sites on the sugar, the sugar’s original neighbours are replaced by moving solvent molecules, and the sugar itself bends and rotates. These details matter in materials research. How does a coating containing sugars contact water? Which parts of a polysaccharide chain are most accessible to solvent? How does changing a linkage alter the chain’s shape? This lesson starts with one trehalose molecule and turns questions about its shape and surrounding water into measurements that can be calculated, plotted, and inspected.

Trehalose contains two connected glucose units and is therefore a disaccharide. It is small enough to identify its important atoms in a drawing, while already containing key features of longer glycans: sugar rings with defined stereochemistry, a glycosidic connection between the rings, and several oxygen sites exposed to water. Here, “sugar” names a chemical family rather than a sensation of sweetness. Connecting many sugar units produces a polysaccharide, whose linkage positions, stereochemical directions, and branches all affect its conformation. Learning to read one disaccharide provides a local structural unit that can be followed repeatedly along a longer chain.

The model is atomistic: all 12 carbon, 22 hydrogen, and 11 oxygen atoms of trehalose are present, together with individual water molecules in a periodic cell. Forces calculated from the interactions advance atomic positions and velocities. Saved coordinates then form a trajectory, much like molecular photographs taken at regular intervals. The chemical identity of the glycosidic linkage remains fixed, while bond angles, rotations about single bonds, and solvent arrangements can change. A question about glycosidic hydrolysis would call for a model of chemical reactions. The present example concerns the local conformation and geometrical hydration environment of an intact trehalose molecule in liquid water.

By the end, you should be able to connect three practical steps: identify precisely how the two sugar units are joined, run trehalose in a box containing 1360 water molecules, and extract two glycosidic dihedrals and a neighbouring-water count from a 1 ns trajectory. Each measurement comes with units, a threshold where needed, and a defined observation interval. The viewer below shows actual saved coordinates. First locate the oxygen bridge between the rings, then watch the modest changes in their relative orientation. Solvent visibility can be adjusted as needed. The later angular and counting plots will then refer to an object you have already located in space.

### Trehalose in water

Saved coordinates from the actual 1 ns trajectory show motion of the sugar rings and glycosidic bridge.

Public GLYCAM06j atomistic trehalose model, converted with ParmEd 4.3.1 and checked term by term. Forty-five sugar atoms and 1360 TIP3P waters at 300 K and 1 bar; 1001 saved frames over 1 ns of production.

[Download reference data and complete inputs (ZIP) 14.25 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-glycan-reference-data.zip)

One nanosecond is 1000 picoseconds, or one billionth of a second. Although brief by everyday standards, this interval includes many molecular collisions and local rotations. The analysis uses a frame saved every 1 ps, giving 1001 frames including the production starting point. Together they form an observation of a specified duration. Questions about slower conformational changes can be addressed with longer records and independent initial conditions. For this record, the immediate task is to read the sampled angular distribution, the identities of neighbouring waters, and the differences between local environments accurately.

## From Fischer’s sugars to molecular identity

Nineteenth-century sugar chemistry faced a fundamental puzzle: substances with the same elemental composition could have different properties and chemical behaviour. A list of carbon, hydrogen, and oxygen atoms did not explain the difference. Emil Fischer connected chemical transformations and synthetic relationships among sugars to their spatial arrangements. His work on sugar and purine syntheses earned the 1902 Nobel Prize in Chemistry. In his Nobel lecture, he discussed asymmetric carbon atoms and sugar isomers, and showed how planar projections could express stereochemical relationships. Composition identifies the atoms present; stereochemistry describes their arrangement. The [original lecture](https://www.nobelprize.org/uploads/2018/06/fischer-lecture-2.pdf) and the [Nobel Prize historical account](https://www.nobelprize.org/prizes/chemistry/1902/speedread/) explain this connection.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g12/en/#en-s2)

Figure 1 · Fischer projections encode stereochemical relationships with a defined drawing convention. The two glyceraldehyde mirror forms share a composition, showing why a sugar’s identity needs spatial information.

Left and right hands provide a useful introduction to chirality. They have the same number of fingers and the same connection pattern, yet translating and rotating a left hand does not make it fit exactly into a glove designed for a right hand. A carbon bonded to four different groups can also participate in a pair of mirror-related arrangements that cannot be superimposed. A group means the atoms reached by following a particular bond. Deciding whether four groups differ may require following those connections beyond the immediately adjacent atom. The hand analogy describes spatial relationships; a molecule also moves thermally, and its solvent and binding partners influence which poses it tends to adopt.

A Fischer projection is a planar notation with a specific spatial convention. An intersection represents the relevant carbon, horizontal bonds point towards the observer, and vertical bonds point away. The figure uses D- and L-glyceraldehyde to show this with a single stereocentre. The labels D and L describe configuration; they do not directly specify the sign of a dihedral in a simulation or the direction of optical rotation. Arbitrarily reflecting a projection can change the identity it expresses. A useful beginner’s habit is therefore to read the drawing together with its convention. Remembering a letter while overlooking its spatial meaning can lead to selecting the wrong structure during model building.

Two related terms need to stay distinct: configuration and conformation. Configuration describes stereochemical identity, such as the alpha or beta arrangement at a sugar’s anomeric carbon. Conformation describes different poses of the same chemical identity, reached through bond rotations and ring deformation. Bending the fingers of a right-handed glove leaves it right-handed. In the present molecule, motion around the glycosidic connection changes conformation; the model starts with the connectivity and stereochemistry of alpha,alpha-trehalose. Its angular histogram therefore describes poses sampled by that particular molecule. The distinction keeps an observed fluctuation from being mistaken for a change of chemical species.

This history has a direct consequence for simulation. A name, molecular formula, coordinate file, and topology provide different kinds of information. The name should identify the sugar and linkage, the formula helps check composition, coordinates describe one starting conformation, and the topology specifies bonds and interaction parameters. All four should refer to the same chemical object. Checking a model therefore begins with identity, rather than with a hexagonal drawing that happens to look like a sugar. Modern trajectories provide thousands of spatial snapshots, while stereochemical reasoning remains essential for understanding which object is being followed through those snapshots.

## Connecting two glucose rings into trehalose

Glucose is represented here in its cyclic form. A glucopyranose ring has six ring members: five carbons and one oxygen. Its sixth carbon lies outside the ring. Thus, “a six-carbon sugar” and “a six-membered ring” describe two different counts. Labels such as C1 and C2 follow the chemical numbering, while the ring oxygen is commonly named O5 because it derives from the oxygen associated with C5. With that numbering in mind, an O5–C1 entry in the topology becomes understandable as part of the sugar ring. It does not mean a fifth monomer or a fifth solvent molecule.

The anomeric carbon is the carbon at which ring formation creates the key stereochemical distinction; in glucose, it is C1. Alpha and beta specify the relative stereochemistry of its substituent with respect to a defined reference group. In conventional drawings of D-glucopyranose, the relative directions of that substituent and the external hydroxymethyl group help identify the arrangement. Trehalose joins the C1 atoms of two glucose units through one oxygen, with both anomeric positions in the alpha configuration. This is written as an alpha,alpha-(1↔1) linkage. The two ones identify the connected carbons. A 1→4 linkage would give another chemical object and rotational environment, requiring the corresponding topology.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g12/en/#en-s3)

Figure 2 · Connectivity of α,α-trehalose. Each ring contains an O5 oxygen; the bridging O1 belongs to 1GA in the topology and joins the two anomeric C1 atoms. Hexagons indicate connectivity around each ring.

The supplied topology names the two residues 1GA and 0GA. A residue is a chemical grouping of atoms within the file; it does not mean the molecule has split into independent pieces. The bridging O1 belongs to 1GA, and the actual inter-residue bond is 1GA:O1–0GA:C1. The first residue’s C1 is also bonded to that O1, giving the complete C1–O1–C1 bridge. Assigning the shared oxygen to one residue is an organizational convention, not an extra free oxygen on one side. GLYCAM names encode sugar identity, ring form, configuration, and occupied linkage positions; the bond table supplies the explicit connectivity. The [official GLYCAM naming documentation](https://glycam.org/docs/forcefield/glycam-naming-2/) explains those roles.

The formula provides an intuitive cross-check. Two free glucose molecules each have composition C₆H₁₂O₆. Expressing their connection as a condensation relationship removes one H₂O from the combined composition, giving trehalose, C₁₂H₂₂O₁₁. This is compositional bookkeeping: the simulation starts with an already connected molecule. Adding 12, 22, and 11 gives 45 atoms, while the model contains 46 covalent bonds. The bond count exceeds the “atoms minus one” value for a simple open connected chain because each sugar ring has a closure. These checks can expose a missing hydrogen, a duplicated bridging oxygen, or a ring closure lost during format conversion.

The connection between the rings is not a completely free hinge. Rotation changes interatomic distances and therefore affects local repulsion, electrostatic interactions, and solvent contacts. Different angles consequently have different energies. Two dihedrals provide a useful description of the bridge. This lesson fixes φ as 1GA:O5–C1–O1–0GA:C1 and ψ as 1GA:C1–O1–0GA:C1–O5. Writing the ordered atoms with their residue identities prevents the two O5 atoms from being confused. The habit becomes especially valuable in a branched glycan, where many residues contain the same atom names and only the combination of identity and connectivity locates a measurement uniquely.

## Carrying the complete parameters into GROMACS

Coordinates describe where atoms are; parameters describe how they interact. Covalent bonds have preferred lengths, angles formed by three consecutive atoms have preferred ranges, and four-atom rotations have torsional energy terms. Atoms without a direct bond can also interact through charges and Lennard–Jones terms. A force field organizes these rules and their numerical parameters into a model. Here, the sugar retains the public GLYCAM06j atomistic trehalose parameters accompanying the disaccharide study by Brandner and colleagues. That study also develops coarse-grained descriptions. This lesson uses its atomistic trehalose input for conformation and hydration measurements. The [public data and scripts](https://zenodo.org/records/14291060) and [research article](https://doi.org/10.1021/acs.jcim.4c01874) identify the molecular system.

The original parameters use Amber file formats. ParmEd 4.3.1 converts them into GROMACS format. Think of translating the notation of a map: the presentation and some numerical units change, while the relationships between the landmarks should remain the same. The quantities to compare include charges, masses, the bond graph, equilibrium lengths, force constants, torsion terms, and nonbonded parameters. The complete program below checks the two source-file hashes, converts the model, and reads the converted files back for comparison. It checks the 46 bonds, 83 angles, and 160 dihedral terms as well. A successful file read is useful, but checking its scientific contents establishes that it still describes the intended model.

### Convert and audit the sugar parameters

```
"""Convert the supplied GLYCAM trehalose parameters and audit the conversion.

Run: python prepare_glycan.py --source . --out prepared
The source directory contains the two Amber files and tip3p.itp.
Dependencies: ParmEd 4.3.1 and NumPy. No parameter fitting is performed.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import numpy as np
import parmed as pmd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=Path('.'))
    parser.add_argument('--out', type=Path, default=Path('prepared'))
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    names = ['glycan_1GA_0GA_nowat.parm7', 'glycan_1GA_0GA_nowat.rst7']
    expected = ['e879a354e9e935cf73142d587dfe691c476ef88cc49846c7dd6aa9dd3b41b401',
                '2c9525820dae93b400b241554e9a301c1b4624e8a91ccc8bc3a826fa10f0b9d3']
    for name, checksum in zip(names, expected):
        if hashlib.sha256((args.source / name).read_bytes()).hexdigest() != checksum:
            raise ValueError('Source checksum differs: ' + name)
    if pmd.__version__ != '4.3.1':
        raise ValueError('Use ParmEd 4.3.1 for this conversion.')
    original = pmd.load_file(str(args.source / names[0]), xyz=str(args.source / names[1]))
    original.save(str(args.out / 'converted.top'), overwrite=True)
    original.save(str(args.out / 'glycan.gro'), overwrite=True, precision=6)
    converted = pmd.load_file(str(args.out / 'converted.top'), xyz=str(args.out / 'glycan.gro'))
    atom_ids = lambda term: tuple(getattr(term, 'atom' + str(i)).idx
                                  for i in range(1, 5) if hasattr(term, 'atom' + str(i)))
    if len(original.atoms) != 45 or len(converted.atoms) != 45:
        raise ValueError('Expected 45 sugar atoms.')
    comparisons = {}
    for attr, tolerance in [('charge', 1e-7), ('mass', 1e-6), ('sigma', 1e-6), ('epsilon', 1e-8)]:
        error = max(abs(getattr(a, attr) - getattr(b, attr))
                    for a, b in zip(original.atoms, converted.atoms))
        comparisons[attr + '_max_abs_difference'] = float(error)
        if error > tolerance:
            raise ValueError('Converted atomic parameter differs: ' + attr)
    fields = [('bonds', [('k', 1e-4), ('req', 1e-7)]),
              ('angles', [('k', 1e-4), ('theteq', 1e-6)]),
              ('dihedrals', [('phi_k', 1e-6), ('per', 0), ('phase', 1e-6)])]
    for collection, parameters in fields:
        left, right = getattr(original, collection), getattr(converted, collection)
        if len(left) != len(right) or [atom_ids(x) for x in left] != [atom_ids(x) for x in right]:
            raise ValueError('Converted connectivity differs: ' + collection)
        for attribute, tolerance in parameters:
            error = max(abs(getattr(a.type, attribute) - getattr(b.type, attribute))
                        for a, b in zip(left, right))
            comparisons[collection + '_' + attribute + '_max_abs_difference'] = float(error)
            if error > tolerance:
                raise ValueError('Converted bonded parameter differs: ' + attribute)
    pairs = {tuple(sorted((d.atom1.idx, d.atom4.idx))) for d in original.dihedrals
             if not d.improper and not d.ignore_end}
    actual_pairs = {tuple(sorted((p.atom1.idx, p.atom2.idx))) for p in converted.adjusts}
    scales = {(d.type.scee, d.type.scnb) for d in original.dihedrals}
    if pairs != actual_pairs or len(pairs) != 126 or scales != {(1.0, 1.0)}:
        raise ValueError('The original unscaled 1-4 interactions must be retained.')
    if (converted.defaults.fudgeLJ, converted.defaults.fudgeQQ) != (1.0, 1.0):
        raise ValueError('GROMACS 1-4 factors must both be one.')
    coordinate_error = float(np.max(np.abs(original.coordinates - converted.coordinates)))
    if coordinate_error > 6e-6:
        raise ValueError('Coordinate conversion exceeds the six-decimal GRO precision.')
    text = (args.out / 'converted.top').read_text()
    text = text[text.index('[ defaults ]'):]
    text = text.replace('[ moleculetype ]',
                        'OW 8 16.000 0.000 A 3.15061e-01 6.36386e-01\n'
                        'HW 1 1.008 0.000 A 0.0 0.0\n\n[ moleculetype ]', 1)
    text = text.replace('[ system ]', '#include "tip3p.itp"\n\n[ system ]')
    text = text.replace('Generic title', 'Trehalose in TIP3P water')
    text = ('; GLYCAM06j public trehalose topology, converted with ParmEd4.3.1.\n'
            '; Original 1-4 electrostatic and LJ factors = 1.\n' + text)
    (args.out / 'topol.top').write_text(text, encoding='utf-8', newline='\n')
    gro = (args.out / 'glycan.gro').read_text().splitlines()
    gro[0] = 'Trehalose, GLYCAM06j'
    (args.out / 'glycan.gro').write_text('\n'.join(gro) + '\n', newline='\n')
    shutil.copyfile(args.source / 'tip3p.itp', args.out / 'tip3p.itp')
    # These stage inputs are supplied with the example and retain the stated protocol.
    for name in ['em.mdp', 'nvt.mdp', 'npt.mdp', 'md.mdp', 'run.sh']:
        shutil.copyfile(args.source / name, args.out / name)
    report = {'parmed_version': pmd.__version__, 'atoms': 45, 'bonds': len(original.bonds),
              'angles': len(original.angles), 'dihedral_terms': len(original.dihedrals),
              'one_four_pairs': len(pairs), 'fudgeLJ': 1, 'fudgeQQ': 1,
              'net_charge_e': float(sum(a.charge for a in original.atoms)),
              'coordinate_max_abs_difference_A': coordinate_error,
              'parameter_comparisons_in_ParmEd_units': comparisons}
    (args.out / 'conversion-check.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
```

Run python prepare_glycan.py --source . --out prepared from the example directory, then run the simulation inside prepared. Requires ParmEd 4.3.1.

The treatment of 1–4 interactions deserves particular attention. Along an ordered four-atom path A–B–C–D, atoms A and D are separated by three covalent bonds. In addition to the bonded terms along the path, they can retain specified nonbonded interactions. Force fields have different conventions for scaling those interactions. The GLYCAM parameters used here leave the electrostatic and Lennard–Jones 1–4 interactions unscaled: both converted factors are one, and the required set contains 126 atom pairs. Substituting scaling factors familiar from another protein force field would change the sugar’s angular energetics even if its atom names, coordinates, and molecular formula appeared unchanged.

The solvent is TIP3P water. Its oxygen has charge −0.834 e, and each hydrogen has +0.417 e, summing to zero; e denotes the elementary charge. A neutral molecule can still have separated positive and negative sites, allowing it to approach different polar sugar sites with different orientations. The water Lennard–Jones term is assigned to oxygen, with zero values on hydrogen. The water topology below specifies an O–H distance of 0.09572 nm and a hydrogen–hydrogen distance that fixes the bent geometry. During production, SETTLE maintains water geometry and LINCS constrains sugar covalent bonds involving hydrogen. Solvent molecules remain free to approach and leave the sugar.

### Water charges and geometry

```
[ moleculetype ]
; molname	nrexcl
SOL		2

[ atoms ]
; id  at type     res nr  res name  at name  cg nr  charge    mass
  1   OW          1       SOL       OW       1      -0.834    16.00000
  2   HW          1       SOL       HW1      1       0.417     1.00800
  3   HW          1       SOL       HW2      1       0.417     1.00800

#ifndef FLEXIBLE

[ settles ]
; OW	funct	doh	dhh
1       1       0.09572 0.15139

[ exclusions ]
1	2	3
2	1	3
3	1	2

#else

[ bonds ]
; i     j       funct   length  force_constant
1       2       1       0.09572 502416.0   0.09572        502416.0 
1       3       1       0.09572 502416.0   0.09572        502416.0 
        

[ angles ]
; i     j       k       funct   angle   force_constant
2       1       3       1       104.52  628.02      104.52  628.02  

#endif
```

TIP3P water and the original GLYCAM sugar parameters are defined separately with consistent nonbonded combination rules.

The prepared directory contains sugar coordinates, a topol.top file holding the complete sugar parameters, the water topology, and four stage settings. The original sugar parameters and the explicitly selected TIP3P solvent together define this example’s solution model. There is one neutral trehalose molecule, so no counterions are added for charge neutralization. This composition supports a study of the local solvent environment around one sugar. Questions about concentrated sugar solutions, salt effects on glycans, or sugar–protein contacts require the corresponding molecules and ions to be introduced explicitly. Additional model contents should follow from the scientific comparison being designed.

## Letting the sugar and its water move together

The calculation begins with a cubic box of side 3.5 nm. Trehalose is placed inside, solvent is added to the remaining space, and overlapping solvent molecules are excluded during construction. The resulting system has 1360 waters and 45 + 3 × 1360 = 4125 atoms. The command’s spc216.gro file provides an initial arrangement of water coordinates. The included TIP3P topology determines the actual water charges, interactions, and constraints. Separating a coordinate template, which supplies positions, from a force-field model, which supplies physics, explains the different name appearing in the construction command. Minimization and preparation then relax this initial arrangement.

Minimization relieves close contacts before ordinary dynamics begins. Coordinates are adjusted along a direction that lowers potential energy until the force criterion or update limit is reached. A minimization update has no ordinary elapsed physical time, so its update index is not a time in picoseconds. The example uses steepest descent with at most 10000 updates, a maximum-force target of 250 kJ mol⁻¹ nm⁻¹, and flexible water geometry during this stage. A 20 ps NVT preparation then brings the system towards 300 K. N, V, and T denote particle number, volume, and temperature. The temperature is a coupling target, while its instantaneous measured value fluctuates.

### Remove close contacts

```
integrator = steep
define = -DFLEXIBLE
nsteps = 10000
emtol = 250
emstep = 0.001
constraints = none
nstenergy = 10
cutoff-scheme = Verlet
nstlist = 20
rlist = 1.1
coulombtype = PME
rcoulomb = 1.1
vdwtype = Cut-off
rvdw = 1.1
DispCorr = EnerPres
pbc = xyz
```

Steepest-descent minimization allows flexible water geometry, with a target maximum force of 250 kJ mol⁻¹ nm⁻¹.

### A 20 ps constant-volume preparation

```
integrator = sd
dt = 0.002
tcoupl = no
tc-grps = System
tau-t = 1.0
ref-t = 300
constraints = h-bonds
constraint-algorithm = lincs
lincs-order = 4
nstlog = 1000
nstenergy = 100
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
compressed-x-precision = 1000
cutoff-scheme = Verlet
nstlist = 20
rlist = 1.1
coulombtype = PME
rcoulomb = 1.1
vdwtype = Cut-off
rvdw = 1.1
DispCorr = EnerPres
pbc = xyz
nsteps = 10000
ld-seed = 20263201
continuation = no
gen-vel = yes
gen-temp = 300
gen-seed = 20263200
pcoupl = no
```

Stochastic dynamics targets 300 K with a 2 fs step and newly generated initial velocities.

The following 100 ps NPT stage keeps particle number fixed and lets volume respond to pressure coupling. P denotes pressure, with a target of 1 bar. Isotropic C-rescale coupling adjusts all cell directions by the same scale, appropriate to this homogeneous solution box. Pressure reflects microscopic momentum transfer and interatomic forces; in a small cell its instantaneous fluctuations can be large. Time averages and volume behaviour help interpret the record. Production continues with the same temperature and pressure targets for 1 ns. Preparation and production name their purposes: the first organizes the initial environment, and the second provides the continuous record analyzed here.

### A 100 ps constant-pressure preparation

```
integrator = sd
dt = 0.002
tcoupl = no
tc-grps = System
tau-t = 1.0
ref-t = 300
constraints = h-bonds
constraint-algorithm = lincs
lincs-order = 4
nstlog = 1000
nstenergy = 100
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
compressed-x-precision = 1000
cutoff-scheme = Verlet
nstlist = 20
rlist = 1.1
coulombtype = PME
rcoulomb = 1.1
vdwtype = Cut-off
rvdw = 1.1
DispCorr = EnerPres
pbc = xyz
nsteps = 50000
ld-seed = 20263202
continuation = yes
gen-vel = no
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5
ref-p = 1
compressibility = 4.5e-5
```

Continue the existing state with isotropic C-rescale pressure coupling targeting 1 bar.

### Parameters for the 1 ns observation

```
integrator = sd
dt = 0.002
tcoupl = no
tc-grps = System
tau-t = 1.0
ref-t = 300
constraints = h-bonds
constraint-algorithm = lincs
lincs-order = 4
nstlog = 1000
nstenergy = 100
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
compressed-x-precision = 1000
cutoff-scheme = Verlet
nstlist = 20
rlist = 1.1
coulombtype = PME
rcoulomb = 1.1
vdwtype = Cut-off
rvdw = 1.1
DispCorr = EnerPres
pbc = xyz
nsteps = 500000
ld-seed = 20263203
continuation = yes
gen-vel = no
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5
ref-p = 1
compressibility = 4.5e-5
```

Coordinates are saved every 1 ps; stochastic dynamics, pressure coupling, and constraints follow the stated protocol.

Dynamics uses the GROMACS sd integrator, which exchanges energy with a 300 K bath through friction and random forces. The friction time parameter is 1 ps. PME handles long-range electrostatics, and the short-range nonbonded cutoff is 1.1 nm. A 2 fs step equals 0.002 ps, so 20, 100, and 1000 ps require 10000, 50000, and 500000 steps, respectively. Constraints remove fast covalent vibrations from the integrated motion, helping support this step size. The script generates velocities at the first NVT start and then continues the existing state between stages, using explicit random seeds. Since stochastic friction affects dynamics, the present measurements focus on conformational distributions and geometrical neighbours.

### From solvation to a production trajectory

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
"$gmx" editconf -f glycan.gro -o boxed.gro -box 3.5 3.5 3.5 -c > box.log 2>&1
"$gmx" solvate -cp boxed.gro -cs spc216.gro -p topol.top -o solvated.gro > solvate.log 2>&1
"$gmx" grompp -f em.mdp -c solvated.gro -p topol.top -o em.tpr > em.grompp.log 2>&1
"$gmx" mdrun -deffnm em -ntmpi 1 -ntomp 2 -pin off > em.stdout.log 2>&1
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
```

Run bash run.sh in a fresh prepared directory. The GMX environment variable can select the GROMACS entry point; its default is gmx.

Run the parameter preparation program from the example directory, enter the newly created prepared directory, and execute bash run.sh. Each stage produces logs, energies, coordinates, and a checkpoint. The final md.tpr contains the topology and production settings, while md.xtc contains compressed coordinates. Reading both lets the analysis associate atom identities and bonds with time-dependent positions. MDAnalysis returns coordinates in angstroms by default, and 1 nm equals 10 Å. Thus, the 0.35 nm hydration threshold is compared with 3.5 Å internally. Making that conversion explicit where the coordinates are read prevents a plausible-looking plot from concealing a tenfold distance error.

## Understanding glycosidic rotation on a circle

A dihedral uses four ordered atoms. A, B, and C define one plane; B, C, and D define another. The planes share the B–C axis, and their relative rotation, viewed according to a fixed convention, gives a signed angle. A three-atom bond angle describes bending, while a dihedral describes rotation around an axis. Two pages joined along the same binding edge provide a useful picture of the two planes. In a molecule the atoms also vibrate, so the actual angle is calculated from all four atomic positions in every frame rather than by treating the pages as permanently rigid objects.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g12/en/#en-s6)

Figure 3 · An ordered set of four atoms defines a dihedral. The two planes share the central B–C axis. Keeping the φ and ψ atom orders fixed makes the measurement comparable across frames.

For this topology, φ uses atoms 17, 2, 1, and 24, and ψ uses atoms 2, 1, 24, and 39. These are one-based atom numbers. Python uses zero-based array indices, so the program subtracts one and additionally checks the residue and atom names at those positions. The calculation uses each frame’s periodic cell so that wrapping across a boundary does not turn neighbouring bonded atoms into an artificially extended chain. In the actual record, φ ranges from about 40.43° to 104.43°, and ψ from 46.27° to 100.26°. Both fluctuate within a local angular region over this saved observation window.

### Time records of the two glycosidic dihedrals

The 1001 frames are spaced by 1 ps. Dashed lines mark the circular means.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g12/en/#en-s6)

Actual 1 ns records of φ and ψ on the two sides of the same glycosidic bridge. Explicit four-atom orderings define the dihedrals; periodic geometry uses the native cell vectors.

Angles return to their starting direction after one complete turn, and their average should respect that geometry. The directions 179° and −179° are separated by 2°, yet adding the signed numbers and dividing by two gives 0°. The numerical discontinuity at ±180° is not a barrier in molecular motion. Circular averaging first represents each angle as an arrow on the unit circle, adds the horizontal and vertical components separately, and reads the resulting direction. The equation below expresses that drawing as an operation. Its two-argument inverse tangent, atan2, reads both components and therefore retains the correct quadrant of the resultant arrow.

Averaging directions to obtain a mean angleEq. 1

![Averaging directions to obtain a mean angle](https://ml-biomat.com/static/agent-math/a472d03ea64242a4a66ce242.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| θⱼ | Dihedral in saved frame j | rad inside trigonometric functions; output may be converted to degrees |
| θ̄ | Angle of the mean direction | rad or degrees, with the output convention stated |
| j、M | Frame index; number of frames | dimensionless |
| sin、cos | Vertical and horizontal components of a direction on the unit circle | dimensionless outputs |
| ∑、j=1、= | Sum frames 1 through M; equality defines the stated quantity | operators |
| atan2(y,x) | Two-argument inverse tangent preserving the quadrant from vertical y and horizontal x | output in rad |

Reading the relationshipTurn each angle into a unit arrow, add the arrows, and read the resulting direction. Dividing both sums by M would leave that direction unchanged.

A worked exampleFor 179° and −179°, the sine terms cancel and the cosine sum is about −1.99970, giving 180°. The arithmetic mean is 0°, half a turn away. The actual trajectory has a circular mean φ of 71.88655°.

ConditionsApplies to equally weighted angular records. A zero resultant has no defined mean direction; a very short resultant calls for examining the angular distribution.

Place two arrows on the circle and compare two ways of averaging.

A geometrical exercise in circular statistics. Sliders set two directions; the red arrow is their vector mean.

The average direction is one part of the description; the spread of directions is another. Nearly parallel arrows produce a mean arrow whose length is close to one. Dispersed directions cancel one another and shorten that arrow. Calling its length R gives a route to the circular standard deviation. The actual circular means of φ and ψ are 71.88655° and 71.85063°, with circular standard deviations of 9.05662° and 8.73675°. These describe typical directions and their spread across the 1001 saved frames. Their similar means are compatible with the chemically similar ends of trehalose. Comparing small differences also calls for examining time blocks and independent repeats.

How concentrated are the directions?Eq. 2

![How concentrated are the directions?](https://ml-biomat.com/static/agent-math/392c31afca4b8f1a74abafe5.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| C、S | Arithmetic means of cos θⱼ and sin θⱼ | dimensionless |
| R | Length of the mean unit arrow, between 0 and 1 | dimensionless |
| s_{circ} | Circular standard deviation; multiply radians by 180/π for degrees | rad |
| π | Pi, approximately 3.14159; half a turn is π rad, equal to 180° | dimensionless |
| 180/π | Radians-to-degrees conversion factor, approximately 57.2958; slash denotes division | °/rad |
| √、²、+ | Nonnegative square root; square; addition | operators |
| ln、−、2、= | Natural logarithm; minus sign; constant two in the definition; equality | operators and dimensionless constant |

Reading the relationshipNearby directions give a resultant close to one; dispersed arrows cancel. The definition converts that length to an angular scale and approaches the ordinary angular standard deviation for a narrow, approximately Gaussian cluster.

A worked exampleFor φ, R = 0.987585. Then −2 ln R is about 0.02499, whose square root is about 0.15807 rad, or 9.05662°.

ConditionsDefined for 0 < R ≤ 1. At R = 0, describe the distribution directly. This spread describes recorded angles; uncertainty of a mean also depends on temporal correlation and independent repeats.

### The sampled cluster in two angular dimensions

Two-dimensional bins are 5° × 5° and one-dimensional bins are 5°. Colours and heights count saved frames.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g12/en/#en-s6)

Joint dihedral distribution and angular statistics from 1001 frames. φ and ψ remain paired within each frame, while circular statistics average unit directions to respect angular periodicity.

The two-dimensional map preserves each frame’s φ and ψ as a paired point. Its axes correspond to the two angles, and colour counts frames in each 5° × 5° bin. Separate one-dimensional histograms discard the pairing, so the map also helps reveal whether the rotations tend to vary together. The sampled local cluster is displayed over 0° to 150° to make its width and shape readable. For a longer trajectory crossing ±180°, a consistent periodic display convention becomes important. If two well-separated conformational clusters appear, describe their occupancies and transitions first, then choose statistics that represent them, rather than relying on a single angle between the clusters.

## How to count the water around a sugar

“How much water surrounds a sugar?” needs a definition of “surrounds.” This lesson uses a geometrical shell: a water is included when its oxygen lies strictly within 0.35 nm of any sugar oxygen, using periodic minimum-image distances. A water can approach two sugar oxygens simultaneously but contributes only once to the whole-molecule count. The definition is reproducible and measures spatial proximity directly. Hydrogen bonding is a more specific classification that adds donor, acceptor, and hydrogen-direction criteria. Measuring how long a water remains nearby also requires following the identity of that same molecule through time. A distance-based count provides a starting point for these more detailed analyses.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g12/en/#en-s7)

Figure 4 · One water oxygen can lie within two sugar-oxygen neighbourhoods. Site counts compare local environments; the union by water identity gives the number of distinct waters around the whole sugar.

Counting the union of overlapping hydration regionsEq. 3

![Counting the union of overlapping hydration regions](https://ml-biomat.com/static/agent-math/106c1bcd0ad06f0ebb159a9c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| N_{water}(t;r_{c}) | Unique neighbouring waters at time t and threshold r_c | dimensionless count |
| t、r_{c} | Frame time; distance threshold | ps; nm |
| w、N_{W} | Water index; total of 1360 waters in the cell | dimensionless |
| o、𝒪 | Sugar-oxygen index; set of the 11 sugar oxygens | index and set |
| d_{ow}(t) | Periodic minimum-image distance from sugar oxygen o to water oxygen w | nm |
| 𝟙[·] | Indicator equal to one when the condition holds and zero otherwise | dimensionless |
| min、∈、∑、<、= | Minimum; set membership; sum; strictly less than; equality | operators |

Reading the relationshipFind each water’s nearest sugar oxygen before testing the threshold. A water near two sugar oxygens still contributes one. Summing over waters counts the union of all site regions.

A worked exampleIf water A is near two sugar oxygens and water B is near one, the sum of site counts is three while the unique-water count is two. At r_c = 0.35 nm, the 1001-frame mean unique count is 23.18282.

ConditionsThis is a geometrical oxygen–oxygen shell. Hydrogen-bond analysis adds donor, acceptor, and direction criteria; exchange analysis also tracks water identity through time.

The program forms a distance matrix between 11 sugar oxygens and 1360 water oxygens. Imagine a table with one sugar oxygen in each row and one water oxygen in each column; an entry gives their distance. Taking the minimum along a column identifies that water’s nearest sugar oxygen. Comparing this minimum with 3.5 Å determines whether the water is in the shell. Adding the successful tests over all columns gives the unique-water count for that frame. The order of operations makes identity explicit and avoids substituting the sum of several overlapping sphere volumes for an actual count of solvent molecules.

### How the distance threshold changes hydration counts

The left panel uses 0.35 nm; the right varies the threshold. Shading shows frame standard deviation.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g12/en/#en-s7)

A geometric hydration shell is defined by the nearest sugar-O–water-O distance. The plots compare frame-wise distinct-water counts and their dependence on shell radius; a water near several sugar oxygens is counted once.

The 1001 saved frames give a mean unique-water count of 23.18282 and a frame standard deviation of 2.33283; the smallest and largest recorded counts are 15 and 30. A mean can be fractional because it summarizes many integer observations. Each frame still contains an integer number of waters. The right panel increases the threshold from 0.25 to 0.50 nm. Within any frame, enlarging that neighbourhood cannot remove previously included waters, so its count is nondecreasing. The 0.35 nm choice defines the observation scale of this comparison. When the scale changes, the definition should accompany the new result. Shading describes frame-to-frame spread at each threshold.

Mean water count and frame-to-frame spreadEq. 4

![Mean water count and frame-to-frame spread](https://ml-biomat.com/static/agent-math/7589de5d9a934c77aeb1bad2.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Nⱼ、⟨N⟩ | Unique-water count in frame j; mean over all frames | dimensionless counts |
| s_{N} | Frame standard deviation using denominator M | dimensionless count |
| j、M | Frame index; number of equally spaced frames | dimensionless |
| ∑、1/M、−、²、√、= | Sum; division by frame count; subtraction; square; nonnegative square root; equality | operators |

Reading the relationshipThe mean gives typical occupancy during the record. Squaring deviations prevents positive and negative changes from cancelling; the final square root restores the count scale.

A worked exampleThree illustrative frames contain 21, 23, and 25 waters. Their mean is 23 and their standard deviation is √(8/3) = 1.633. The actual 1001 frames give 23.18282 and 2.33283.

ConditionsThe denominator M summarizes the saved-frame distribution. Correlated frames require block or independent-repeat analysis for uncertainty of the mean.

Counting around each oxygen asks another question: where on the sugar do waters approach most often? In this record, the bridging 1GA:O1 has about 0.660 neighbours on average, the two ring O5 sites have about 1.419 and 1.421, and the two O6 sites have about 3.454 and 3.430. Local steric accessibility, oxygen charges, and surrounding groups jointly influence these values. They describe different opportunities for close approach in this model. Isolating a charge effect from a geometrical effect would require a controlled change or comparisons at matched conformations. Error bars describe each site’s frame standard deviation; they are a measure of fluctuations around its mean count.

### Water around individual sugar oxygens

Site counts use the same 0.35 nm threshold. Error bars are frame standard deviations; a water can contribute to several sites.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g12/en/#en-s7)

Nearby waters within 0.35 nm of each of the 11 sugar oxygen sites; the figure defines the error bars. Sites may share the same water, so the sum of site counts and the union of distinct waters are interpreted separately.

Adding the mean counts of all 11 oxygen sites gives 29.23377, larger than the whole-molecule value of 23.18282 because some waters contribute at several sites. Both measurements contain useful information. The unique count describes the entire molecular neighbourhood, while site counts locate contacts. The program exports both, allowing a direct check that the site-count sum is never smaller than the union count. The complete analysis below also exports angular records, threshold sensitivity, individual-site counts, and four 250 ps blocks. Each block is left-open and right-closed and contains 250 frames, so a frame at a shared boundary is assigned to one block.

### Complete torsion and hydration analysis

```
"""Analyze trehalose torsions and geometrical hydration from TPR + XTC.

Run: python analyze_glycan.py --run . --out figures --language en
Dependencies: MDAnalysis 2.11, NumPy 2.5, Matplotlib 3.11.
MDAnalysis returns coordinates in angstroms and time in picoseconds.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import MDAnalysis as mda
from MDAnalysis.lib.distances import calc_dihedrals, distance_array, calc_bonds
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


def circular_stats(degrees):
    z = np.exp(1j * np.deg2rad(degrees)).mean()
    length = float(abs(z))
    return {'mean_deg': float(np.rad2deg(np.angle(z))),
            'resultant_length': length,
            'circular_sd_deg': float(np.rad2deg(np.sqrt(-2 * np.log(length))))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', type=Path, default=Path('.'))
    parser.add_argument('--out', type=Path, default=Path('figures'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    tr = lambda zh, en: zh if args.language == 'zh' else en
    fonts = {f.name for f in font_manager.fontManager.ttflist}
    chinese = [f for f in ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC',
                           'WenQuanYi Zen Hei', 'DejaVu Sans'] if f in fonts]
    plt.rcParams.update({'font.family': chinese if args.language == 'zh' else ['DejaVu Sans'],
                         'font.size': 12, 'axes.spines.top': False, 'axes.spines.right': False,
                         'figure.facecolor': '#f8f7f2', 'axes.facecolor': '#f8f7f2',
                         'svg.fonttype': 'path'})
    u = mda.Universe(str(args.run / 'md.tpr'), str(args.run / 'md.xtc'))
    sugar = u.atoms[:45]
    if [(r.resname, len(r.atoms)) for r in sugar.residues] != [('1GA', 23), ('0GA', 22)]:
        raise ValueError('Expected the supplied 45-atom trehalose topology.')
    composition = {e: sum(a.name.startswith(e) for a in sugar) for e in ['C', 'H', 'O']}
    if composition != {'C': 12, 'H': 22, 'O': 11} or abs(sugar.charges.sum()) > 1e-5:
        raise ValueError('Expected neutral C12H22O11.')
    torsions = np.array([[16, 1, 0, 23], [1, 0, 23, 38]])
    expected = [[('1GA', 'O5'), ('1GA', 'C1'), ('1GA', 'O1'), ('0GA', 'C1')],
                [('1GA', 'C1'), ('1GA', 'O1'), ('0GA', 'C1'), ('0GA', 'O5')]]
    for ids, identities in zip(torsions, expected):
        if [(a.resname, a.name) for a in u.atoms[ids]] != identities:
            raise ValueError('Dihedral atom identities differ from the supplied model.')
    oxygen = sugar.select_atoms('name O*')
    water = u.select_atoms('resname SOL and name OW')
    bonds = np.array([b.indices for b in sugar.bonds if np.all(b.indices < 45)])
    if len(bonds) != 46 or not any(set(b) == {0, 23} for b in bonds):
        raise ValueError('Expected both sugar rings and the inter-residue O1-C1 bond.')
    if len(water) != 1360 or len(u.atoms) != 4125:
        raise ValueError('Expected the supplied 1360-water system.')
    radii_nm = np.arange(25, 51, dtype=float) / 100
    selected_radius = int(np.flatnonzero(np.isclose(radii_nm, .35))[0])
    rows = []; threshold_counts = []; site_counts = []; max_bond = 0.
    for ts in u.trajectory:
        if not np.isfinite(ts.positions).all():
            raise ValueError('Non-finite coordinate.')
        angles = [np.rad2deg(calc_dihedrals(*u.atoms[ids].positions, box=ts.dimensions))
                  for ids in torsions]
        distances = distance_array(oxygen.positions, water.positions, box=ts.dimensions)
        # The minimum over sugar oxygens counts each water once at each radius.
        closest = distances.min(axis=0)
        counts = (closest[:, None] < 10 * radii_nm[None, :]).sum(axis=0)
        sites = (distances < 3.5).sum(axis=1)
        rows.append([ts.time, *angles, counts[selected_radius], sites.sum(), ts.volume / 1000])
        threshold_counts.append(counts); site_counts.append(sites)
        max_bond = max(max_bond, float(calc_bonds(u.atoms[bonds[:, 0]].positions,
                       u.atoms[bonds[:, 1]].positions, box=ts.dimensions).max() / 10))
    a = np.asarray(rows); thresholds = np.asarray(threshold_counts); sites = np.asarray(site_counts)
    if len(a) != 1001 or not np.allclose(a[:, 0], np.arange(1001)) or max_bond > .20:
        raise ValueError('Unexpected frame times or sugar bond geometry.')
    if not np.all(np.diff(thresholds, axis=1) >= 0) or not np.all(a[:, 4] >= a[:, 3]):
        raise ValueError('Hydration union and per-site counts are inconsistent.')
    block_results = []
    for lo in range(0, 1000, 250):
        keep = (a[:, 0] > lo) & (a[:, 0] <= lo + 250)
        block_results.append({'time_ps': [lo, lo + 250], 'endpoint_rule': '(start, end]',
                              'frames': int(keep.sum()),
                              'phi': circular_stats(a[keep, 1]), 'psi': circular_stats(a[keep, 2]),
                              'unique_water_mean': float(a[keep, 3].mean())})
    summary = {'frames': len(a), 'time_ps': [float(a[0, 0]), float(a[-1, 0])],
               'atom_count': len(u.atoms), 'sugar_atoms': 45, 'water_count': len(water),
               'formula': 'C12H22O11', 'sugar_mass_u': float(sugar.masses.sum()),
               'sugar_charge_e': float(sugar.charges.sum()), 'sugar_bonds': len(bonds),
               'max_sugar_bond_nm': max_bond, 'torsion_indices_one_based': (torsions + 1).tolist(),
               'phi': circular_stats(a[:, 1]), 'psi': circular_stats(a[:, 2]),
               'angle_min_max_deg': [[float(a[:, i].min()), float(a[:, i].max())] for i in [1, 2]],
               'hydration_radius_nm': .35, 'unique_water_mean': float(a[:, 3].mean()),
               'unique_water_frame_sd': float(a[:, 3].std()),
               'unique_water_min_max': [int(a[:, 3].min()), int(a[:, 3].max())],
               'per_site_count_sum_mean': float(a[:, 4].mean()),
               'oxygen_labels': [f'{o.resname}:{o.name}' for o in oxygen],
               'oxygen_mean_counts': sites.mean(axis=0).tolist(),
               'blocks': block_results,
               'definition': 'All 1001 equally spaced saved frames. A water is in the geometrical '
                             'shell when its oxygen is strictly closer than 0.35 nm to any sugar '
                             'oxygen under periodic minimum-image geometry. Unique water counts '
                             'use the union of sites; per-site counts may repeat a water. '
                             'Frame standard deviations describe fluctuations, not mean uncertainty.'}
    (args.out / 'glycan_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    np.savetxt(args.out / 'glycan_timeseries.csv', a, delimiter=',', comments='',
               header='time_ps,phi_deg,psi_deg,unique_waters_035nm,sum_site_counts,volume_nm3')
    np.savetxt(args.out / 'glycan_thresholds.csv', np.column_stack([radii_nm, thresholds.mean(0),
               thresholds.std(0)]), delimiter=',', comments='', header='radius_nm,mean_unique_water,frame_sd')
    np.savetxt(args.out / 'glycan_sites.csv', np.column_stack([sites.mean(0), sites.std(0)]),
               delimiter=',', comments='', header='mean_count,frame_sd; rows: ' + ','.join(summary['oxygen_labels']))

    def save(fig, name):
        fig.savefig(args.out / (name + '.svg'), bbox_inches='tight')
        fig.savefig(args.out / (name + '.png'), dpi=160, bbox_inches='tight')
        plt.close(fig)

    blue, red, gold = '#176d83', '#b44e3f', '#b28a35'
    fig, ax = plt.subplots(2, 1, figsize=(11.5, 6.3), sharex=True, layout='constrained')
    for i, (symbol, color) in enumerate([('φ', blue), ('ψ', red)]):
        ax[i].plot(a[:, 0], a[:, i + 1], lw=.8, color=color, alpha=.7,
                   label=tr('每 1 ps 保存的角度', 'Angles saved every 1 ps'))
        mean = summary['phi' if i == 0 else 'psi']['mean_deg']
        ax[i].axhline(mean, color='#292f34', ls='--', lw=1.5,
                      label=tr(f'全程圆均值 {mean:.2f}°', f'Circular mean {mean:.2f}°'))
        ax[i].set_ylabel(symbol + tr(' / 度', ' / degrees'))
        ax[i].legend(loc='lower left', bbox_to_anchor=(0, 1.01), ncol=2, frameon=False)
        ax[i].grid(axis='y', alpha=.15)
    ax[-1].set_xlabel(tr('生产阶段时间 / ps', 'Production time / ps'))
    save(fig, 'glycan-torsions')

    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.5), layout='constrained')
    edges = np.arange(0, 151, 5)
    hist = ax[0].hist2d(a[:, 1], a[:, 2], bins=[edges, edges], cmap='YlGnBu', cmin=1)
    fig.colorbar(hist[3], ax=ax[0], label=tr('每个 5° × 5° 格的帧数', 'Frames per 5° × 5° bin'))
    ax[0].set(xlabel='φ / ' + tr('度', 'degrees'), ylabel='ψ / ' + tr('度', 'degrees'),
              xlim=(0, 150), ylim=(0, 150))
    ax[1].hist(a[:, 1], bins=edges, histtype='step', lw=2, color=blue, label='φ')
    ax[1].hist(a[:, 2], bins=edges, histtype='step', lw=2, color=red, label='ψ')
    ax[1].set(xlabel=tr('二面角 / 度', 'Dihedral / degrees'), ylabel=tr('每个 5° 格的帧数', 'Frames per 5° bin'),
              xlim=(0, 150))
    ax[1].legend(loc='lower left', bbox_to_anchor=(0, 1.01), ncol=2, frameon=False)
    save(fig, 'glycan-angle-map')

    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.5), layout='constrained')
    ax[0].plot(a[:, 0], a[:, 3], color=blue, lw=.8, label=tr('0.35 nm 内的去重后的水分子', 'Unique waters within 0.35 nm'))
    ax[0].axhline(a[:, 3].mean(), color=red, ls='--', lw=1.6,
                  label=tr(f'均值 {a[:, 3].mean():.2f}', f'Mean {a[:, 3].mean():.2f}'))
    ax[0].set(xlabel=tr('生产阶段时间 / ps', 'Production time / ps'), ylabel=tr('水分子数', 'Water molecules'))
    mean = thresholds.mean(0); sd = thresholds.std(0)
    ax[1].plot(radii_nm, mean, color=blue, lw=2, label=tr('平均去重后的水分子数', 'Mean unique-water count'))
    ax[1].fill_between(radii_nm, mean - sd, mean + sd, color=blue, alpha=.17,
                        label=tr('逐帧标准差', 'Frame standard deviation'))
    ax[1].axvline(.35, color=red, ls='--', lw=1)
    ax[1].set(xlabel=tr('距离阈值 / nm', 'Distance threshold / nm'), ylabel=tr('水分子数', 'Water molecules'))
    for axis in ax:
        axis.legend(loc='lower left', bbox_to_anchor=(0, 1.01), fontsize=10, frameon=False)
        axis.grid(axis='y', alpha=.15)
    save(fig, 'glycan-hydration')

    fig, ax = plt.subplots(figsize=(11.5, 4.8), layout='constrained')
    colors = [blue if o.resname == '1GA' else gold for o in oxygen]
    ax.bar(np.arange(len(oxygen)), sites.mean(0), color=colors, width=.68)
    # Intervals here describe fluctuations at a site, not statistical confidence.
    ax.errorbar(np.arange(len(oxygen)), sites.mean(0), yerr=sites.std(0), fmt='none',
                 color='#333333', capsize=4, lw=1.2)
    ax.set_xticks(np.arange(len(oxygen)), summary['oxygen_labels'], rotation=30, ha='right')
    ax.set_ylabel(tr('0.35 nm 内的平均水数', 'Mean waters within 0.35 nm'))
    ax.plot([], [], color=blue, lw=8, label='1GA')
    ax.plot([], [], color=gold, lw=8, label='0GA')
    ax.plot([], [], color='#333333', lw=1.2, label=tr('误差线：逐帧标准差', 'Error bars: frame standard deviation'))
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1.01), ncol=3, frameon=False)
    ax.grid(axis='y', alpha=.15)
    save(fig, 'glycan-sites')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
```

Run python analyze_glycan.py --run prepared --out figures --language en. The analysis reads md.tpr and md.xtc.

## From one disaccharide to glycan materials

A trajectory contains information on more than one temporal scale. Rapid fluctuations show local activity, while differences between longer blocks help assess whether that activity has similar statistical characteristics through the record. The four 250 ps blocks give φ circular means of approximately 71.14°, 71.46°, 71.57°, and 73.43°. Their mean unique-water counts are 23.192, 23.104, 23.328, and 23.116. The last angular block shifts somewhat towards larger values, while the four hydration means are close. A study of finer angular differences can extend observation and add independent velocity repeats, comparing their blocks instead of treating every adjacent photograph as a new independent experiment.

Extending from a disaccharide to a polysaccharide first adds a connectivity problem. Each added unit requires a sugar identity, an alpha or beta configuration, a linkage position, and any branching to be specified. Each connection also adds local rotational freedom. Even similar repeating units can favour more extended, bent, or helical arrangements when their linkage pattern changes. The checking sequence remains useful: verify residues and cross-residue bonds, inspect composition, charge, and parameters, and then choose measurements of overall shape. Local φ and ψ angles and a global radius of gyration address different scales. Combining them connects a linkage preference to the shape adopted by a longer chain.

For sugar–protein binding, the site hydration map suggests a concrete question: what happens to nearby waters when a binding site occupies part of the sugar surface? In a complex, one can measure sugar–protein contacts, sugar angular distributions, and water around the same sugar oxygens, comparing defined bound and separated structural conditions. Hydrogen-bond analysis should specify donors, acceptors, and direction criteria. Water-exchange analysis should specify whether residence must be continuous or may include brief departures. These definitions let a line in a structure drawing, an increased contact count, and a solvent residence time each refer to a distinct molecular measurement.

In materials containing sugars, the comparison may instead concern concentration, interactions between chains, or an interface. Increasing concentration changes solvent availability, opportunities for sugar–sugar contact, and the overall solution environment. Tethering a sugar to a surface restricts accessible conformations; longer chains introduce additional shielding and multiple contacts. A useful comparison fixes the force field, water model, temperature, pressure, and counting threshold, then clearly identifies the structural factor being changed. Record actual sugar and water numbers, volume, and observation duration for each condition. Hydration comparisons should also state whether counts refer to a molecule, sugar unit, or oxygen site, so the normalization matches the material’s composition.

The example links three levels of evidence. The topology establishes the chemical identity of alpha,alpha-trehalose; the angular trajectory describes a local cluster of glycosidic conformations; and individual-site and unique-water counts connect that shape to the surrounding solvent. A useful next exercise is to change the distance threshold and time blocks while keeping the trajectory fixed. The same identity checks, parameter comparisons, and measurement definitions can then be carried into a new glycan model. An interpretable sugar simulation lets every curve be traced back to specified atoms and spatial relationships, with each extension of the model answering a new materials question.

## Further Reading and Open Materials

- [Systematic Approach to Parametrization of Disaccharides for the Martini 3 Coarse-Grained Force Field: data and scripts](https://zenodo.org/records/14291060) · Brandner et al. · CC BY 4.0

  Public GLYCAM06j atomistic trehalose parameters and starting coordinates.

  Retain the sugar parameters, convert them with ParmEd, and construct a TIP3P water box with the preparation and 1 ns observation protocol described here.
- [Systematic Approach to Parametrization of Disaccharides for the Martini 3 Coarse-Grained Force Field](https://doi.org/10.1021/acs.jcim.4c01874) · Brandner et al. · Research article; cited for scientific context

  Research context for disaccharide conformations and atomistic reference models.

  This lesson analyzes the public atomistic trehalose model through angular and hydration measurements.
- [GLYCAM naming convention](https://glycam.org/docs/forcefield/glycam-naming-2/) · GLYCAM developers · Official documentation; cited

  Naming principles for sugar identity, ring form, configuration, and linkage positions.

  Explained through the two residues and actual bonds in this example.
- [Syntheses in the purine and sugar group](https://www.nobelprize.org/uploads/2018/06/fischer-lecture-2.pdf) · Emil Fischer, Nobel Lecture, 1902 · Historical lecture; cited, figures drawn independently

  History of sugar stereochemistry and Fischer projections.

  A new schematic uses mirror-related glyceraldehyde projections.
- [Bringing chemistry to biology](https://www.nobelprize.org/prizes/chemistry/1902/speedread/) · Nobel Prize Outreach · Official historical account; cited

  Context for Fischer’s sugar research and the 1902 Nobel Prize in Chemistry.

  Connect the historical question to configuration and conformation in molecular models.
- [MDAnalysis distance and dihedral functions](https://docs.mdanalysis.org/stable/documentation_pages/lib/distances.html) · MDAnalysis developers · Official documentation; cited; MDAnalysis LGPL-3.0

  Periodic minimum-image distances and signed dihedral calculations.

  A complete analysis script fixes atom identities and statistical windows for this example.
- [ParmEd](https://github.com/ParmEd/ParmEd) · ParmEd developers · LGPL-2.1-or-later

  Amber-to-GROMACS parameter conversion with version 4.3.1.

  Add checks of charges, masses, connectivity, potential parameters, and 1–4 interactions.
