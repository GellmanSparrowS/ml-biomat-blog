# Simulating a Protein and a Small Molecule

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g10/en/
Language: en

Build a protein–ligand model from an experimental bound structure and interpret displacement, contacts, and orientation inside its pocket.

## Understanding molecular recognition from an occupied pocket

A sponge takes up many liquids, whereas a protein often has to distinguish molecules that look remarkably similar. Taste receptors respond to particular chemicals, transport proteins capture suitable cargo, and enzymes bring appropriate substrates near the groups involved in a reaction. Materials research encounters related questions: which proteins approach a small molecule attached to a biomaterial surface, or how moving a hydroxyl group changes the interactions around a molecule inside a carrier. Answering these questions requires both a description of molecular proximity and an understanding of how shape, orientation, and surrounding water adjust when the molecules meet.

This chapter starts with an experimentally observed protein–small-molecule complex. The protein is an engineered T4 lysozyme, and the small molecule is 2-propylphenol, identified as JZ4 in the structure record. We will place the pair in salt water, construct compatible force-field descriptions, follow motion inside the binding pocket, and measure which protein residues frequently contact the ligand. A ligand is a molecule that binds the object under study; here it is the small molecule. A pocket is a region on or inside the protein that can accommodate it. This calculation examines local motion around an initial bound pose and identifies atoms and residues worth comparing in a subsequent study.

Think of the experimental structure as a photograph of a hand holding an object. It shows the positions of the fingers and the object, but not how the hand approached, how many arrangements preceded the grip, or how long release takes. Our starting point is this already occupied configuration, followed by a one-nanosecond record of nearby motion. Studying entry from solution requires sampling diffusion, pocket opening, and binding events. Studying affinity requires the statistical weights of bound and solution states. Each question therefore calls for its own sampling design; a record of movement inside a pocket supplies a specific part of that broader description.

Shape complementarity has long guided ideas about protein recognition. The early lock-and-key analogy captures how size, shape, and the arrangement of chemical groups affect access to a site. Koshland's induced-fit proposal in 1958 emphasized that ligand approach can accompany a change in protein conformation, bringing relevant groups into a suitable spatial relationship. A conformation is a molecular shape produced by rotations and bending while chemical connectivity remains unchanged. The question consequently expands from whether two outlines match to how two flexible objects adjust together.

[Figure: Recognition: from shape to coupled adjustment](https://ml-biomat.com/tutorials/molecular-dynamics/g10/en/#en-s1)

Figure 1 · Conceptual comparison of flexible recognition. Induced fit links interaction with conformational adjustment; this example observes local motion from an already bound pose.

Flexibility need not mean a dramatic opening or closing motion. A small side-chain rotation can redirect a hydrogen atom, and water entering or leaving nearby can alter the local environment. Koshland later discussed precisely how small a conformational change can be while still affecting function. When reading a simulation, we therefore examine both whole-protein motion and the relative positions of selected pocket atoms. Describing the direction of a hydroxyl group with a whole-protein average would be like using the displacement of a palm to decide whether one fingertip touches a button. The observation must resolve the feature of interest.

An experimental complex with a small ligand provides a clear setting for these questions. In 3HTB, L99A and M102Q identify substitutions: leucine becomes alanine at position 99, and methionine becomes glutamine at position 102. They create a useful system for examining cavity space and local polarity. We retain the resolved protein and ligand identities and concentrate on converting chemical information into a model, then answering local, measurable questions from its trajectory. The classical model has fixed chemical connectivity. Chemical reactions, proton transfer, and electronic redistribution require appropriate reactive or quantum descriptions.

## Establishing the identity of every component

When inspecting 3HTB, first distinguish the protein, the target ligand, and components of the crystallization environment. The structure was determined by X-ray diffraction at a resolution of 1.81 Å. The angstrom, Å, is one tenth of a nanometre, so this corresponds to a structural resolution scale of 0.181 nm. Resolution describes spatial detail in the experimental information; it is not an identical positional error assigned to every atom. Occupancies and alternate locations provide additional information that matters when selecting one simultaneous set of coordinates for a simulation.

The deposited protein sequence contains 164 residues, while the resolved continuous coordinates cover chain A residues 1–163. Terminal Leu164 has no coordinates. This example retains the resolved chain, assigns a positively charged amino terminus to Met1 and a negatively charged carboxyl terminus to Asn163, and thus defines a specific 163-residue model. The position of the terminal charge is part of that definition. A question involving this terminus would call for building the missing residue and examining the added conformation. Here the focus is the internal pocket, with the terminal treatment retained explicitly in the model description.

Ten residues have alternate positions such as A and B. For each affected residue, we select the alternative with the higher mean occupancy, choosing A in a tie; all ten selections are A in this record. Selection must remain coherent within a residue. Taking one side-chain atom from alternative A and another from B can assemble a geometry that was never supplied as one experimental alternative. After selection, the protein contains 1300 heavy atoms. In this context, a heavy atom means any atom other than hydrogen, conveniently distinguishing the carbon, nitrogen, oxygen, and other atoms usually resolved more clearly from hydrogens added during model preparation.

JZ4 has formula C₉H₁₂O: 22 atoms in total, including ten heavy atoms. Its chemical structure contains a six-membered aromatic carbon ring, a propyl group, and a hydroxyl group. Coordinates and names alone need supplementation with chemical connectivity and bond orders: which carbons connect, which bonds form the aromatic ring, and whether the oxygen bears a hydrogen. We take the bond graph from the Chemical Component Dictionary and associate it with the identically named atoms in the experimental bound coordinates. Chemical identity and spatial placement then come from the information appropriate to each, rather than from guessing every bond by proximity.

[Figure: 3HTB: resolved protein and bound pocket](https://ml-biomat.com/tutorials/molecular-dynamics/g10/en/#en-s2)

Figure 2 · Protein overview and local pocket rendered from actual 3HTB coordinates with the selected A alternatives. The right panel displays JZ4 and selected Gln102 heavy atoms; projection collapses the third dimension.

The hydroxyl oxygen is named OAB, and its added hydrogen is H12. Names serve as indices; the chemical bond must also be confirmed in the topology. The side chain of protein residue Gln102 contains both oxygen OE1 and nitrogen NE2. Although they belong to one residue, they play different chemical roles. We will record the OAB–OE1 and OAB–NE2 distances separately, then examine the orientation of OAB–H12 toward OE1. Representing the entire residue by one point would discard both this directional information and the identity of the atom involved.

The hydrogen placement on His31 also needs a defined choice. Histidine has two ring nitrogens and can adopt different neutral tautomers. We choose HID, with a hydrogen on ND1. One reason for considering this donor geometry is the initial ND1–Asp70 OD2 separation of approximately 2.582 Å. This is a protonation-model choice based on the local environment; the fixed topology does not switch tautomer during the trajectory. Phosphate, beta-mercaptoethanol, and 220 crystallographic water oxygen positions are removed as part of rebuilding the environment. A specified water model and salt composition then establish the simulated solution.

The following programs implement these choices. The first downloads two public structural records and checks their content fingerprints. The second chooses alternate conformations residue by residue, extracts the protein and bound ligand, and writes the ligand with explicit bond orders. The output `protein.pdb` holds the selected protein; `ligand-heavy.sdf` contains ligand coordinates and chemical connectivity; `ligand-bound.pdb` retains the bound heavy-atom pose. The structural checks also measure peptide-bond distances between consecutive residues, helping reveal a chain break or an inconsistent selection.

### Download and check public structures

```
"""Download the public 3HTB structure and JZ4 chemical dictionary record."""
from pathlib import Path
from urllib.request import urlopen
import hashlib

destination = Path("source")
destination.mkdir(exist_ok=True)
files = [
    ("3HTB.pdb", "https://files.rcsb.org/download/3HTB.pdb",
     "69c7b4776c588526160c587e14a36289f5f74b265cb0736fcbed47c4335adfa7"),
    ("JZ4.cif", "https://files.rcsb.org/ligands/download/JZ4.cif",
     "adea84e7352ad38e5210cb555e62b100d692323739f709cfb4901fc7d6620e82"),
]
for filename, url, expected in files:
    data = urlopen(url, timeout=60).read()
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected:
        raise ValueError(f"Public record has changed: {filename}, SHA256={actual}")
    (destination / filename).write_bytes(data)
    print(filename, len(data), "bytes", actual)
```

The filename matches the execution sequence above; inputs and outputs use relative paths.

### Select protein conformers and build the ligand graph

```
from pathlib import Path
import collections,json,shlex,hashlib,math
import argparse
parser=argparse.ArgumentParser(description='Prepare the resolved 3HTB protein and the CCD-defined bound ligand.')
parser.add_argument('--source',type=Path,default=Path('source'))
parser.add_argument('--out',type=Path,default=Path('prepared'))
args=parser.parse_args();src=args.source;out=args.out
out.mkdir(parents=True,exist_ok=True)
lines=(src/'3HTB.pdb').read_text().splitlines();groups=collections.defaultdict(list)
for l in lines:
    if l.startswith('ATOM  ') and l[21]=='A':groups[(int(l[22:26]),l[26],l[17:20])].append(l)
selected=[];alts=[]
for resid,rows in sorted(groups.items()):
    options=sorted(set(l[16] for l in rows if l[16]!=' '))
    if options:
        means={k:sum(float(l[54:60]) for l in rows if l[16]==k)/sum(l[16]==k for l in rows) for k in options}
        chosen=sorted(options,key=lambda k:(-means[k],k))[0]
        alts.append(dict(residue=resid,mean_occupancy=means,chosen=chosen))
    else:chosen=' '
    keep=[l for l in rows if l[16] in (' ',chosen)]
    assert len({l[12:16] for l in keep})==len(keep)
    selected.extend(l[:16]+' '+l[17:] for l in keep)
assert len(groups)==163 and sorted(set(int(l[22:26]) for l in selected))==list(range(1,164))
def xyz(l):return tuple(float(l[i:i+8]) for i in [30,38,46])
def dist(a,b):return math.dist(xyz(a),xyz(b))
peptide=[]
for i in range(1,163):
    a=next(l for l in selected if int(l[22:26])==i and l[12:16].strip()=='C')
    b=next(l for l in selected if int(l[22:26])==i+1 and l[12:16].strip()=='N')
    peptide.append(dist(a,b))
assert max(peptide)<1.6
(out/'protein.pdb').write_text('TITLE     3HTB chain A resolved residues 1-163\n'+'\n'.join(selected)+'\nTER\nEND\n',newline='\n')
lig=[l for l in lines if l.startswith('HETATM') and l[17:20]=='JZ4'];assert len(lig)==10
(out/'ligand-bound.pdb').write_text('TITLE     3HTB JZ4 bound heavy-atom coordinates\n'+'\n'.join(lig)+'\nEND\n',newline='\n')
cif=(src/'JZ4.cif').read_text().splitlines();bonds=[];inside=False
for l in cif:
    if l.startswith('_chem_comp_bond.'):inside=True;continue
    if inside and l.strip()=='#':break
    if inside and l.startswith('JZ4 '):
        x=shlex.split(l);bonds.append((x[1],x[2],x[3]))
names=[l[12:16].strip() for l in lig];heavy=[(a,b,o) for a,b,o in bonds if a in names and b in names]
assert len(heavy)==10
s=['JZ4 bound coordinates','3HTB / RCSB CCD bond orders','',f'{len(lig):3d}{len(heavy):3d}  0  0  0  0            999 V2000']
for l in lig:
    x,y,z=xyz(l);s.append(f'{x:10.4f}{y:10.4f}{z:10.4f} {l[76:78].strip():<3s} 0  0  0  0  0  0  0  0  0  0  0  0')
for a,b,o in heavy:s.append(f'{names.index(a)+1:3d}{names.index(b)+1:3d}{dict(SING=1,DOUB=2,TRIP=3)[o]:3d}  0  0  0  0')
s+=['M  END','$$$$'];(out/'ligand-heavy.sdf').write_text('\n'.join(s)+'\n',newline='\n')
hist=[l for l in selected if l[17:20]=='HIS' and l[12:16].strip() in ['ND1','NE2']]
neighbors=[]
for h in hist:
    neighbors.append(dict(atom=h[12:16].strip(),resid=int(h[22:26]),neighbors=[dict(resname=l[17:20],resid=int(l[22:26]),atom=l[12:16].strip(),distance_A=dist(h,l)) for l in selected if l[22:26]!=h[22:26] and l[76:78].strip() in ['O','N','S'] and dist(h,l)<4]))
audit=dict(pdb='3HTB',pdb_sha256=hashlib.sha256((src/'3HTB.pdb').read_bytes()).hexdigest(),ccd_sha256=hashlib.sha256((src/'JZ4.cif').read_bytes()).hexdigest(),model='T4 lysozyme L99A/M102Q, resolved residues 1-163 + JZ4',missing_terminal='Unresolved Leu164 is omitted; Asn163 is assigned a deprotonated C terminus; Met1 protonated N terminus',protein_atoms=len(selected),protein_residues=163,altlocs=alts,peptide_CN_range_A=[min(peptide),max(peptide)],ligand_names=names,ligand_heavy_bonds=heavy,removed_heterogens=dict(collections.Counter(l[17:20] for l in lines if l.startswith('HETATM') and l[17:20]!='JZ4')),histidine_neighbors=neighbors)
(out/'structure-audit.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit,indent=2))
```

The filename matches the execution sequence above; inputs and outputs use relative paths.

## One interaction model for a protein and its ligand

The protein in the preceding exercise was assembled from common amino acids, for which the force field supplies residue templates. Adding 2-propylphenol requires rules for the new molecule's bonds, angles, torsions, and nonbonded interactions. Protein templates resemble specifications for standard components; the small molecule requires appropriate component types selected from its chemical graph. Appending ligand coordinates to a protein coordinate file supplies positions but no additional interaction rules. A complete model needs both, with an unambiguous correspondence between them.

We use AMBER99SB-ILDN for the protein, GAFF for the organic ligand, and SPC/E for water. GAFF is the General AMBER Force Field. It distinguishes atom types using element and local chemical environment, including aromatic carbon, aliphatic carbon, and hydroxyl oxygen. A carbon in the ring and a saturated carbon in the propyl group have different neighbourhoods and can require different parameters. Parameterization reads connectivity and bond orders, assigns types, and assembles bond, angle, torsion, and nonbonded terms. Unusual functional groups or unfamiliar chemical environments call for further checks of parameter coverage and conformational energetics.

Partial charges supply another essential part of the description. A molecule with zero net charge can still have an uneven electron distribution: oxygen regions may be relatively negative and particular hydrogens relatively positive. A fixed-charge force field approximates that distribution with point charges attached to atomic positions. They move with the atoms while electron density is not recalculated at every step. AM1-BCC obtains charges through a semiempirical quantum calculation followed by bond-charge corrections. The resulting fractional charges describe the internal distribution; the specified formal net charge of zero defines the overall molecular charge state.

Partial charges sum to molecular chargeEq. 1

![Partial charges sum to molecular charge](https://ml-biomat.com/static/agent-math/63f4713fea9a8569f03a999e.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Q | Total molecular charge | C |
| e | Elementary-charge magnitude, 1.602176634×10⁻¹⁹ C | C |
| qᵢ | Numerical partial charge on atom i in units of e | 1 |
| i, N | Atom index and total atom count; N=22 for JZ4 | 1 |
| Σᵢ₌₁ᴺ | Sum all atomic charge values | 1 |
| =, eΣqᵢ | Equality; multiply the sum by e | Equality has no unit; product is C |

Reading the relationshipCharge is additive, so partial charges must sum to the assigned molecular charge. Each qᵢ is numerical in elementary-charge units; multiplication by e yields coulombs.

A worked exampleFor three illustrative sites with q=0.4, −0.2, −0.2, the sum is zero and Q=0 C. JZ4 requires all 22 terms; OAB plus H12 alone gives about −0.081099e, balanced by the remaining atoms.

ConditionsCharge assignment in a fixed-charge model; electronic density is not recomputed at every frame.

In the generated parameters, OAB carries approximately −0.498099e and H12 carries +0.417000e. These two numbers do not sum to zero because charge is distributed across the hydroxyl group and the rest of the molecule together. Summing all 22 atomic charges gives the neutral JZ4 total. Here e denotes the magnitude of an elementary charge, and the negative sign indicates charge relative to the positive convention. It does not turn the oxygen into a separate ion with an integer negative charge. A neutral molecule can consequently have substantial electrostatic interactions with water and polar protein groups.

Compatibility involves more than matching units. Parameter sets must share the appropriate nonbonded combination conventions and correctly handle atoms separated by three chemical bonds, called 1–4 interactions. The AMBER conventions used here apply specific scaling to these pairs, and conversion to GROMACS must retain their meaning. Combining charges from one force field, van der Waals terms from another, and unrelated scaling factors changes the balance of the model. A compatible protein and ligand parameter family gives a defined starting point, followed by inspection of the actual generated topology.

ACPYPE calls AmberTools and produces the GROMACS files used in this exercise. The argument `-a gaff` explicitly chooses GAFF, `-c bcc` selects AM1-BCC, and `-n 0` sets the net charge. GAFF and GAFF2 are different parameter versions, despite their similar names. We use ACPYPE 2026.10.15 with its associated AmberTools 26. Changing the charge method or force-field version should produce a complete new model that passes through preparation and analysis, so any later comparison corresponds to a clearly identified scientific change.

Parameterization also raises a coordinate issue. A free ligand processed for charge calculation or geometry preparation may not retain its original placement in the protein. We add hydrogens around the bound heavy coordinates, then restore those heavy coordinates by atom identity after parameterization and relax the complete complex together. Generated hydrogen positions are retained for this shared minimization. This keeps the initial question centred on motion around the experimental bound pose, while resolving local contacts in the assembled model rather than arbitrarily placing a separately optimized ligand back inside the pocket.

## Connecting chemical identity, coordinate order, and topology

After preparing the modeling environment, generate the ligand parameters in the following order. Complete installation instructions appear in the [molecular modeling section of the environment guide](https://ml-biomat.com/tutorials/molecular-dynamics/s00/en/#en-modeling). Run these commands from the exercise directory; outputs are organized into `prepared` and `run` subdirectories. Keeping public input records separate from generated files preserves the original coordinates and makes it easier to see what hydrogen addition, parameterization, and solvent rebuilding each change.

### From public structures to analysis plots

```
# Run from an exercise directory directly inside the course workspace.
course_workspace=$(cd .. && pwd)
export PATH="$course_workspace/runtime/modeling/bin:$PATH"
python fetch_structure.py
python prepare_structure.py --source source --out prepared
bash parameterize_ligand.sh prepared
python export_model.py --prepared prepared --out run
(cd run && bash run_complex.sh)
# Use the separately prepared analysis environment.
"$course_workspace/runtime/analysis/bin/python" analyze_complex.py --records run --out analysis --language en
```

Place the exercise directory directly inside the environment-guide workspace and first activate the course commands. Modeling and analysis use runtime/modeling and runtime/analysis respectively. The reference-record directory can be passed directly to --records.

### Add hydrogens, preserve identity, and generate GAFF parameters

```
#!/usr/bin/env bash
set -euo pipefail
cd "${1:-prepared}"
obabel ligand-heavy.sdf -O ligand.mol2 -h > obabel.log 2>&1
python - <<'PY'
from pathlib import Path
import json
from openbabel import openbabel as ob
c=ob.OBConversion();c.SetInFormat('mol2');m=ob.OBMol();c.ReadFile(m,'ligand.mol2')
assert m.NumAtoms()==22 and m.GetFormula()=='C9H12O',(m.NumAtoms(),m.GetFormula())
original=json.loads(Path('structure-audit.json').read_text())['ligand_names']
lines=Path('ligand.mol2').read_text().splitlines();section=''
for i,line in enumerate(lines):
    if line.startswith('@<TRIPOS>'):section=line;continue
    if section=='@<TRIPOS>ATOM' and line.strip():
        v=line.split();idx=int(v[0]);v[1]=original[idx-1] if idx<=10 else 'H'+str(idx-10);v[6]='1';v[7]='JZ4';lines[i]=' '.join(v)
Path('ligand.mol2').write_text('\n'.join(lines)+'\n')
PY
acpype -i ligand.mol2 -b JZ4 -c bcc -n 0 -a gaff -o gmx > acpype.log 2>&1
```

The filename matches the execution sequence above; inputs and outputs use relative paths.

Atom names have an operational role throughout this process. The component dictionary identifies the hydroxyl oxygen as OAB, and trajectory analysis uses the same name to select that atom. If format conversion replaces it with a generic O1, a later selection could refer to the wrong object. The program therefore restores the original names of the ten heavy atoms after adding hydrogens, then assigns stable hydrogen names. It also checks the formula and atom count: nine carbons, twelve hydrogens, and one oxygen make 22 atoms. These checks reveal missing hydrogens, duplicated atoms, or an incorrect charge state more directly than visual appearance alone.

The protein and ligand next enter one GROMACS coordinate file. `pdb2gmx` adds protein hydrogens and constructs its topology, producing 2614 protein atoms; the ligand occupies the next 22 coordinate records. The molecule order in `[ molecules ]` must agree with the coordinate order because the program assigns parameters to coordinate rows according to that topology. A theatre seating plan offers a useful analogy: names, ticket numbers, and seats must correspond. A correct total headcount is necessary, but the order still determines who occupies each seat.

[Figure: Coordinate order must match molecular identity](https://ml-biomat.com/tutorials/molecular-dynamics/g10/en/#en-s4)

Figure 3 · A ligand has molecule-local topology indices and positions in the full coordinate sequence. Molecule counts, atom counts, and order together define the parameter–coordinate correspondence.

Include order also matters. `forcefield.itp` first establishes the parameter family's basic conventions. Ligand atom types must appear before molecular definitions that use them. The JZ4 file contains both atom types and molecular topology, so it is included immediately after the force-field entry. Position restraints belong to a particular molecule and use numbering that begins at that molecule's first atom. The 22-atom ligand therefore uses local indices in its restraint file, rather than the global coordinate-row numbers beginning at 2615 in the combined complex.

The export program gathers ligand parameters, bound coordinates, heavy-atom restraints, and simulation inputs in `run`. The file `JZ4.itp` contains the complete molecular topology, while `posre_JZ4.itp` identifies ligand heavy atoms restrained during preparation. The merge program also verifies that His31 contains HD1 and lacks HE2, confirming that the generated model uses the selected HID form. Checking the resulting atom identities connects the chemical decisions discussed earlier with the object that actually enters the simulation.

### Export ligand parameters and bound coordinates

```
from pathlib import Path
import argparse,shutil
import numpy as np
parser=argparse.ArgumentParser(description="Export GAFF parameters and retain the bound ligand pose.")
parser.add_argument("--prepared",type=Path,default=Path("prepared"))
parser.add_argument("--out",type=Path,default=Path("run"))
args=parser.parse_args();prep=args.prepared;out=args.out;params=prep/"JZ4.acpype"
out.mkdir(parents=True,exist_ok=True)
shutil.copy2(prep/'protein.pdb',out/'protein.pdb')
itp=(params/'JZ4_GMX.itp').read_text();itp=itp[itp.index('[ atomtypes ]'):]
itp+='\n#ifdef POSRES\n#include "posre_JZ4.itp"\n#endif\n';(out/'JZ4.itp').write_text('; JZ4 GAFF / AM1-BCC; ACPYPE2026.10.15, AmberTools26.\n'+itp,newline='\n')
pos=(params/'posre_JZ4.itp').read_text();(out/'posre_JZ4.itp').write_text(pos[pos.index('[ position_restraints ]'):],newline='\n')
gro=(params/'JZ4_GMX.gro').read_text().splitlines();gro[0]='JZ4 bound conformation with added hydrogen atoms'
bound={l[12:16].strip():np.array([float(l[i:i+8])/10 for i in [30,38,46]]) for l in (prep/'ligand-bound.pdb').read_text().splitlines() if l.startswith('HETATM')}
errors=[]
for j,l in enumerate(gro[2:-1],2):
    name=l[10:15].strip()
    if name in bound:
        pos=np.array([float(l[i:i+8]) for i in [20,28,36]]);errors.append(float(np.linalg.norm(pos-bound[name])))
        gro[j]=l[:20]+''.join(f'{v:8.3f}' for v in bound[name])
assert max(errors)<.001,errors
(out/'JZ4.gro').write_text('\n'.join(gro)+'\n',newline='\n')
template=Path(__file__).resolve().parent
for name in ['ions.mdp','em.mdp','nvt.mdp','npt.mdp','md.mdp','merge_complex.py','run_complex.sh']:
    (out/name).write_text((template/name).read_text(),encoding='utf8',newline='\n')
print('Exported 22-atom ligand; maximum input-coordinate rounding:',max(errors),'nm')
```

The filename matches the execution sequence above; inputs and outputs use relative paths.

### Merge coordinates and topology

```
from pathlib import Path
import re,json
protein=Path('processed.gro').read_text().splitlines();ligand=Path('JZ4.gro').read_text().splitlines()
n=int(protein[1]);m=int(ligand[1]);assert m==22
atoms=protein[2:2+n]
for j,line in enumerate(ligand[2:2+m],1):atoms.append(f'{164:5d}'+line[5:15]+f'{n+j:5d}'+line[20:])
Path('complex.gro').write_text('3HTB resolved protein + bound JZ4\n'+str(n+m)+'\n'+'\n'.join(atoms)+'\n'+protein[-1]+'\n')
top=Path('topol.top').read_text();anchor='#include "amber99sb-ildn.ff/forcefield.itp"';assert anchor in top
top=top.replace(anchor,anchor+'\n#include "JZ4.itp"');top+='JZ4 1\n';Path('topol.top').write_text(top)
hist=[line[10:15].strip() for line in protein[2:2+n] if int(line[:5])==31]
assert 'HD1' in hist and 'HE2' not in hist
Path('prepared-model.json').write_text(json.dumps(dict(protein_atoms=n,ligand_atoms=m,protein_residues=163,His31='HID, HD1 present and HE2 absent'),indent=2))
```

The filename matches the execution sequence above; inputs and outputs use relative paths.

The final atom inventory provides another useful check. The system contains 33382 atoms: 2614 protein atoms, 22 ligand atoms, 10226 three-site waters, 31 sodium ions, and 37 chloride ions. The protein carries +6e and the ligand is neutral, so six additional chloride ions accompany the paired salt ions and neutralize the system. The water model here is SPC/E. It has three interaction sites, as TIP3P does in the preceding protein exercise, but its parameters differ. The solvent choice must therefore remain part of the recorded model alongside the protein and ligand force fields.

## Relaxing the pocket and solution before releasing restraints

The assembled structure combines experimental heavy coordinates, generated hydrogens, and newly placed water. Since these geometries come from different preparation operations, some local contacts may be too close. Minimization first reduces excessive forces by changing coordinates along directions that lower potential energy. Its iterations do not have the physical-time meaning of a dynamical trajectory. Flexible water is used for this geometrical preparation; all subsequent dynamics restore rigid SPC/E and constrain bonds involving hydrogen. Removing some of the fastest vibrations supports the selected 2 fs integration step.

During preparation, protein and ligand heavy atoms receive position restraints while water, ions, and other unconstrained degrees of freedom can move. Imagine an elastic support holding the main shape while material around it settles: small displacements remain possible, but larger ones produce restoring forces. The restraint coefficient is 1000 kJ mol⁻¹ nm⁻². The units show its role. Squared displacement contributes nm², so multiplication by the coefficient yields an energy. The coefficient is neither a temperature nor a fixed force that acts equally at every position.

Elastic position-restraint energy for one atomEq. 2

![Elastic position-restraint energy for one atom](https://ml-biomat.com/static/agent-math/68225b0a803b586ee4346521.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Upos | Position-restraint energy for this atom | kJ mol⁻¹ |
| kpos | Common Cartesian restraint coefficient, 1000 here | kJ mol⁻¹ nm⁻² |
| α, {x,y,z} | Index and set of the three Cartesian directions | 1 |
| rα, rα,0 | Current and reference coordinate components | nm |
| rα−rα,0 | Displacement along the selected direction | nm |
| (rα−rα,0)² | Squared displacement component | nm² |
| Σ, ½, =, − | Sum over three directions, one half, equality, and subtraction | Operators and constants have no unit |

Reading the relationshipA linear restoring force integrates to a quadratic energy. Contributions from three orthogonal directions add through the squared displacement components.

A worked exampleWith an x displacement of 0.02 nm and zero y/z displacement, U=0.5×1000×0.02²=0.20 kJ/mol. A 0.04 nm displacement gives 0.80 kJ/mol: doubling displacement quadruples the quadratic energy.

ConditionsApplied to protein and ligand heavy atoms during preparation; position restraints are removed in production.

A 100 ps NVT stage couples the system to a 300 K heat bath at fixed volume, followed by 200 ps of NPT preparation at a target pressure of 1 bar. Temperature is controlled by stochastic velocity rescaling with the entire system in one coupling group, and isotropic C-rescale permits volume adjustment. Heavy-atom restraints remain active during both preparation stages, with `refcoord-scaling = com` in NPT. Their purpose is to retain the main geometry while the surrounding solution adjusts. The following 1 ns production stage removes position restraints and records motion with the same temperature, pressure, nonbonded conventions, and 2 fs step.

The complete inputs for these stages appear below. `ions.mdp` prepares the structural and topological description used for ion replacement; it is not a production-sampling stage. Its short-range electrostatics setting serves that preparation, while the actual dynamical stages use PME for long-range electrostatics. In `em.mdp`, the force tolerance has units kJ mol⁻¹ nm⁻¹, and `emstep` is a minimization step length in nm. Keeping these quantities separate from the dynamical time step `dt` avoids confusing the number of coordinate-improvement iterations with elapsed physical time.

### Preprocessing input for ion replacement

```
integrator = steep
nsteps = 0
cutoff-scheme = Verlet
nstlist = 20
coulombtype = Cut-off
rcoulomb = 1.0
fourierspacing = 0.12
ewald-rtol = 1e-5
vdwtype = Cut-off
vdw-modifier = Potential-shift
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
```

The filename matches the execution sequence above; inputs and outputs use relative paths.

### Minimization input

```
integrator = steep
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
```

The filename matches the execution sequence above; inputs and outputs use relative paths.

### 100 ps NVT input

```
integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
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
define = -DPOSRES
nsteps = 50000
continuation = no
pcoupl = no
gen-vel = yes
gen-temp = 300
gen-seed = 20261000
ld-seed = 20261001
```

The filename matches the execution sequence above; inputs and outputs use relative paths.

### 200 ps NPT input

```
integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
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
define = -DPOSRES
refcoord-scaling = com
nsteps = 100000
ld-seed = 20261002
```

The filename matches the execution sequence above; inputs and outputs use relative paths.

### 1 ns production input without position restraints

```
integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
nstenergy = 500
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
nsteps = 500000
ld-seed = 20261003
```

The filename matches the execution sequence above; inputs and outputs use relative paths.

The run script generates the protein topology, merges the ligand, constructs a periodic dodecahedral box with a 1.0 nm solute-to-edge clearance, adds water and ions, and executes the stages in order. Each `grompp` call combines current coordinates, topology, and stage settings into a run input. Consecutive dynamical stages additionally read a checkpoint to transfer velocities and other state information. Initial velocities are generated once in NVT, then continued. In production, `nsteps = 500000` multiplied by 0.002 ps gives 1000 ps, or 1 ns. Compressed coordinates saved every 500 steps therefore have a spacing of 1 ps.

### Build the salt-water system and run the simulation

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
py=${PYTHON:-python3}
printf '0
' | "$gmx" pdb2gmx -f protein.pdb -o processed.gro -p topol.top -i posre.itp -ff amber99sb-ildn -water spce -his > pdb2gmx.log 2>&1
"$py" merge_complex.py
"$gmx" editconf -f complex.gro -o boxed.gro -c -d 1.0 -bt dodecahedron > box.log 2>&1
"$gmx" solvate -cp boxed.gro -cs spc216.gro -o solvated.gro -p topol.top > solvate.log 2>&1
"$gmx" grompp -f ions.mdp -c solvated.gro -p topol.top -o ions.tpr > ions.grompp.log 2>&1
printf 'SOL
' | "$gmx" genion -s ions.tpr -o ions.gro -p topol.top -pname NA -nname CL -conc 0.15 -neutral -seed 20261000 > genion.log 2>&1
"$gmx" grompp -f em.mdp -c ions.gro -p topol.top -o em.tpr > em.grompp.log 2>&1
"$gmx" mdrun -deffnm em -ntmpi 1 -ntomp 2 -pin off > em.stdout.log 2>&1
"$gmx" grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr > nvt.grompp.log 2>&1
"$gmx" mdrun -deffnm nvt -ntmpi 1 -ntomp 2 -pin off > nvt.stdout.log 2>&1
"$gmx" grompp -f npt.mdp -c nvt.gro -t nvt.cpt -r em.gro -p topol.top -o npt.tpr > npt.grompp.log 2>&1
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

The filename matches the execution sequence above; inputs and outputs use relative paths.

After the calculation, inspect constraints and energy behaviour before interpreting geometry. The resulting 1001 frames include both the production starting point and the endpoint at 1000 ps; all enter this chapter's averages and contact fractions. This differs from the preceding chapter's right-exclusive window chosen for complete blocks, with each choice serving a stated statistical task. Thermostats and barostats define environmental conditions. Coverage of relevant conformations still requires trajectory and replication analysis, especially for a pocket side chain whose rearrangement may occur on a longer timescale than this record.

## Giving every contact a precise measurement

In a trajectory, the protein and ligand translate and rotate together, and their coordinates may cross a periodic boundary. Measuring ligand displacement directly in the displayed frame would mix whole-complex drift with local motion. We first reconstruct the bonded protein and ligand, place the ligand in the appropriate nearby periodic image, and fit the protein's 163 Cα atoms to the minimized reference. Cα is the central backbone carbon of an amino acid; one per residue gives a set of reference points distributed along the protein. Every ligand coordinate receives that same protein-based transformation.

Ligand displacement in the protein reference frameEq. 3

![Ligand displacement in the protein reference frame](https://ml-biomat.com/static/agent-math/2c11fb2bac301c7c62531559.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| RMSDL\|P(t) | Ligand RMSD after protein-based alignment | nm |
| t | Production time | ps |
| NL, i | Ligand-heavy-atom count and index; NL=10 here | 1 |
| rᵢ(t), rᵢ,0 | Row vectors of current and minimized-reference ligand positions | nm |
| cP(t), cP,0 | Equal-weight geometric centres of current and reference protein Cα atoms | nm |
| RP(t) | Proper rotation that best aligns centred protein Cα positions | 1 |
| (rᵢ−cP)RP+cP,0−rᵢ,0 | Difference from the ligand reference after applying the protein transform | nm |
| ‖·‖² | Squared displacement-vector length | nm² |
| Σ, /NL, √, =, +, − | Atomwise sum, division by count, square root, equality, addition, and subtraction | Operators have no unit; the square root converts nm² back to nm |

Reading the relationshipRemove protein translation and rotation, average squared ligand displacements from a fixed reference, then take the square root. Squaring prevents opposite displacements from cancelling and the root restores length units.

A worked exampleIf two illustrative ligand atoms are 0.05 and 0.10 nm from their references after protein alignment, RMSD=√[(0.05²+0.10²)/2]=0.07906 nm. The actual calculation uses ten heavy atoms without a further ligand fit.

ConditionsEqual-weight rigid fitting of 163 protein Cα atoms after bonded reconstruction and nearby periodic imaging, with fixed atom-name correspondence.

The ligand is not subsequently fitted on its own. The measurement therefore retains its translation and rotation within the pocket, together with internal conformational changes. An additional ligand-only fit would instead emphasize its internal shape and remove part of the information about reorientation in the pocket. Both measurements can be useful when matched to their questions. Here the ten ligand heavy atoms receive equal weights, and distances are reported in nm. Protein Cα RMSD is measured separately to describe the movement of the reference structure itself.

A residue contact uses a different definition. For each protein residue, calculate distances between all its heavy atoms and all ligand heavy atoms, then retain the smallest distance. If that minimum is below the selected cutoff, the residue counts as contacting the ligand in that frame. Multiple nearby atoms in the same residue still contribute one residue contact. This answers which residues lie close to the ligand without counting a larger side chain repeatedly merely because it has more atoms. Periodic minimum-image distances also prevent a contact from disappearing just because coordinates are written on opposite sides of the box.

Minimum residue-to-ligand distanceEq. 4

![Minimum residue-to-ligand distance](https://ml-biomat.com/static/agent-math/f1fceff237614bbedd0d3bd3.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| da(t) | Minimum heavy-atom distance between residue a and ligand | nm |
| a, L | Selected protein-residue and ligand-heavy-atom sets | 1 |
| i, j | Atom indices in the two sets | 1 |
| rᵢ(t), rⱼ(t) | Column vectors of atomic positions | nm |
| H(t) | Matrix whose columns are the periodic box vectors | nm |
| n, ℤ³ | Three-integer periodic-image index and its set | 1 |
| Hn | Translation vector of the chosen periodic image | nm |
| min, ∈, ‖·‖, =, +, − | Minimum, membership, vector length, equality, addition, and subtraction | Operators have no unit; vector length is nm |
| t | Production time | ps |

Reading the relationshipThe closest heavy-atom pair defines proximity. Periodic images put neighbours across the boundary on the same footing as neighbours inside the box. The implementation uses a minimum-image distance algorithm supporting triclinic cells.

A worked exampleFor candidate minimum distances 0.32, 0.46, and 0.58 nm, da=0.32 nm. At a 0.40 nm cutoff the residue counts once, even if several of its atoms lie close to the ligand.

ConditionsHeavy-atom geometric proximity, counted once per residue with an explicitly chosen cutoff.

Adding the contact indicators over 1001 frames and dividing by the frame count gives the contact fraction in this record. For example, 801 contacting frames yield approximately 0.8002, or 80.0%. This measures the time fraction satisfying the chosen geometry. Neighbouring frames are correlated, so 1001 records are not 1001 independent draws; uncertainty would require blocking or replicated trajectories. We also calculate fractions at 0.35, 0.40, and 0.45 nm to see how strongly a conclusion depends on the distance boundary.

Contact fraction averages framewise indicatorsEq. 5

![Contact fraction averages framewise indicators](https://ml-biomat.com/static/agent-math/acbd78151b8aa8de8af21630.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Ia,m | Contact indicator for residue a in frame m, either 0 or 1 | 1 |
| da(tm), rc | Current minimum distance and chosen contact cutoff | nm |
| tm | Production time of frame m | ps |
| a, m, M | Residue index, frame index, and total frames; M=1001 here | 1 |
| pa | Residue contact fraction in the selected record | 1 |
| Σ, /M, 0, 1, <, ≥, = | Sum and divide by frame count; binary values, less than, greater than or equal, and equality | 1 |

Reading the relationshipA shared criterion assigns zero or one per frame. Summing counts qualifying frames and division gives their fraction. Equal spacing makes this a time fraction over the chosen window.

A worked exampleFor M=1001 and 801 qualifying frames, pa=801/1001=0.80020, about 80.0%. Correlation and independent repeats determine uncertainty in this record-based fraction.

ConditionsAll 1001 frames from 0 to 1000 ps are included, with cutoffs 0.35, 0.40, and 0.45 nm.

A hydrogen-bond analysis additionally requires chemical roles and direction. In OAB–H12···OE1, OAB is the donor heavy atom bonded to hydrogen H12, and glutamine OE1 is the acceptor oxygen. We use an explicit geometric criterion: donor–acceptor distance below 0.35 nm and donor–hydrogen–acceptor angle of at least 150°. The angle vertex is the hydrogen; a value near 180° describes nearly collinear atoms. These thresholds define a reproducible frame classification. Interaction strength still depends on the chemical environment and the model, while this measurement reports a specified geometry.

Defining the donor–hydrogen–acceptor angle at hydrogenEq. 6

![Defining the donor–hydrogen–acceptor angle at hydrogen](https://ml-biomat.com/static/agent-math/c8818eda8feede41f009c61a.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| θ | D–H–A angle with H as the vertex | Arccosine returns rad; output is converted to ° |
| D, H, A | Donor heavy atom, its bonded hydrogen, and acceptor heavy atom | 1 |
| rD, rH, rA | Positions of the three atoms | nm |
| rD−rH, rA−rH | Two vectors originating at H, using nearby periodic images | nm |
| · | Vector dot product | Result here has units nm² |
| ‖rD−rH‖ ‖rA−rH‖ | Product of the two vector lengths | nm² |
| arccos, /, =, − | Inverse cosine recovers the angle; division, equality, and subtraction | Ratio is dimensionless; operators have no unit |

Reading the relationshipThe dot product equals the product of lengths times the cosine of their angle. Dividing out the lengths leaves orientation, and inverse cosine recovers the angle. Numerical cosine values are clipped to −1..1 to handle roundoff.

A worked exampleFor D=(0,0,0), H=(0.10,0,0), A=(0.30,0,0) nm, the vectors are (−0.10,0,0) and (0.20,0,0). Their dot product is −0.02 nm² and length product 0.02 nm², giving cosine −1 and θ=180°. The D–A distance is 0.30 nm, also passing this example’s distance condition.

ConditionsThe selected OAB–H12···OE1 donor–acceptor combination; classification requires D–A<0.35 nm and θ≥150°.

The interaction below separates proximity from orientation. Keep the donor and acceptor close while rotating the O–H direction, and the classification can change even though the two heavy atoms remain nearby. This explains why an O···O distance alone gives an incomplete description, and why a nearby nitrogen should not automatically be assigned an acceptor role. The analysis first verifies from the topology that H12 is bonded to OAB, then calculates the angle. Chemical identity thus precedes geometric filtering.

Fixed O–H length 0.10 nm; D is donor O, H its hydrogen, and A acceptor O. Distance and orientation jointly define the selected geometry.

[Figure: D–H–A geometry](https://ml-biomat.com/tutorials/molecular-dynamics/g10/en/#en-s6)

Analytical geometry with a fixed O–H bond. Rotating the donor–hydrogen direction changes the D–H–A angle even at fixed donor–acceptor distance.

## Visualizing local changes in the recorded trajectory

The analysis reads the run topology, compressed trajectory, and minimized structure directly. The topology supplies masses, bonds, and residue identities; the trajectory supplies framewise positions; the minimized structure supplies the shared comparison reference. MDAnalysis reads distances in Å, so the program explicitly divides by ten before reporting nm. Distances, angles, contacts, and RMSD are measured in the same frame loop, keeping all panels synchronized. The CSV records each frame's values, and a second file retains residue minimum distances so that cutoff changes can be evaluated on the same coordinates.

### Analyze ligand motion, orientation, and residue contacts

```
"""Measure local protein–ligand motion and contacts from the 3HTB trajectory.

python analyze_complex.py --records records --out analysis --language en
Required files: md.tpr, md.xtc, em.gro. Dependencies: MDAnalysis, numpy,
matplotlib. MDAnalysis uses angstrom internally; all plotted distances are nm.
All 1001 equally spaced frames from 0 to 1000 ps enter the reported averages.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import MDAnalysis as mda
from MDAnalysis.lib.distances import distance_array, minimize_vectors
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


class BondReconstruction:
    """Restore one connected molecule by traversing its explicit topology bonds."""
    def __init__(self, group):
        self.group = group
        local = {int(index): i for i, index in enumerate(group.indices)}
        self.edges = np.array([[local[int(a)], local[int(b)]] for a, b in group.bonds.indices])
        neighbours = [[] for _ in group]
        for edge, (a, b) in enumerate(self.edges):
            neighbours[a].append((b, edge, 1))
            neighbours[b].append((a, edge, -1))
        visited = {0}
        queue = [0]
        self.plan = []
        for parent in queue:
            for child, edge, sign in neighbours[parent]:
                if child not in visited:
                    visited.add(child)
                    queue.append(child)
                    self.plan.append((parent, child, edge, sign))
        if len(visited) != len(group):
            raise ValueError("Selected molecule is not a single connected bond graph")

    def restore(self, box):
        raw = self.group.positions.astype(float)
        a, b = self.edges.T
        vectors = minimize_vectors(raw[b] - raw[a], box)
        whole = np.empty_like(raw)
        whole[0] = raw[0]
        for parent, child, edge, sign in self.plan:
            whole[child] = whole[parent] + sign * vectors[edge]
        errors = np.linalg.norm((whole[b] - whole[a]) - vectors, axis=1)
        if np.max(errors) > 0.005:
            raise ValueError("Bond-cycle reconstruction disagreement exceeds 0.005 angstrom")
        longest_nm = float(np.linalg.norm(whole[b] - whole[a], axis=1).max() / 10)
        if longest_nm > 0.25:
            raise ValueError("A reconstructed covalent bond exceeds 0.25 nm")
        self.group.positions = whole
        return longest_nm


def fit_rotation(moving, reference):
    left, _, right = np.linalg.svd(moving.T @ reference)
    correction = np.eye(3)
    correction[-1, -1] = np.linalg.det(left @ right)
    return left @ correction @ right


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, default=Path("records"))
    parser.add_argument("--out", type=Path, default=Path("analysis"))
    parser.add_argument("--language", choices=["zh", "en"], default="en")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    tr = lambda zh, en: zh if args.language == "zh" else en
    available = {f.name for f in font_manager.fontManager.ttflist}
    candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC",
                  "WenQuanYi Zen Hei", "DejaVu Sans"]
    plt.rcParams.update({"font.family": [x for x in candidates if x in available]
                         if args.language == "zh" else ["DejaVu Sans"],
                         "font.size": 13, "axes.titlesize": 14, "svg.fonttype": "path",
                         "axes.spines.top": False, "axes.spines.right": False,
                         "figure.facecolor": "#faf8f2", "axes.facecolor": "#faf8f2"})
    universe = mda.Universe(str(args.records / "md.tpr"), str(args.records / "md.xtc"))
    reference = mda.Universe(str(args.records / "md.tpr"), str(args.records / "em.gro"))
    protein = universe.select_atoms("protein")
    ca = protein.select_atoms("name CA")
    heavy = protein.select_atoms("not name H*")
    ligand = universe.select_atoms("resname JZ4")
    ligand_heavy = ligand.select_atoms("not name H*")
    ref_protein = reference.select_atoms("protein")
    ref_ligand = reference.select_atoms("resname JZ4")
    assert len(ca) == 163 and len(ligand_heavy) == 10
    assert len(ligand) == 22 and len(protein) == 2614
    BondReconstruction(ref_protein).restore(reference.dimensions)
    BondReconstruction(ref_ligand).restore(reference.dimensions)
    protein_reconstruction = BondReconstruction(protein)
    ligand_reconstruction = BondReconstruction(ligand)
    ref_ca = ref_protein.select_atoms("name CA").positions.astype(float)
    ref_center = ref_ca.mean(axis=0)
    ref_ca -= ref_center
    ref_ligand_positions = ref_ligand.positions.astype(float)
    offset = ref_ligand_positions.mean(axis=0) - ref_center
    ref_ligand_positions += minimize_vectors(offset[None, :], reference.dimensions)[0] - offset
    ref_ligand_heavy = ref_ligand_positions[~np.char.startswith(ref_ligand.names.astype(str), "H")] - ref_center
    donor = ligand.select_atoms("name OAB")[0]
    hydrogen = ligand.select_atoms("name H12")[0]
    assert hydrogen.index in donor.bonded_atoms.indices
    acceptor = protein.select_atoms("resid 102 and name OE1")[0]
    amide_n = protein.select_atoms("resid 102 and name NE2")[0]
    residue_numbers = protein.residues.resids
    residue_names = protein.residues.resnames
    row_for_resindex = {r.ix: j for j, r in enumerate(protein.residues)}
    atom_to_residue = np.array([row_for_resindex[a.resindex] for a in heavy])
    records, contact_distances = [], []
    maximum_bond_nm = 0.
    for ts in universe.trajectory:
        maximum_bond_nm = max(maximum_bond_nm, protein_reconstruction.restore(ts.dimensions),
                             ligand_reconstruction.restore(ts.dimensions))
        current_ca = ca.positions.astype(float)
        center = current_ca.mean(axis=0)
        current_ca -= center
        rotation = fit_rotation(current_ca, ref_ca)
        ca_rmsd = np.sqrt(np.mean(np.sum((current_ca @ rotation - ref_ca)**2, axis=1))) / 10
        lig_xyz = ligand_heavy.positions.astype(float)
        offset = ligand.positions.mean(axis=0) - center
        lig_xyz += minimize_vectors(offset[None, :], ts.dimensions)[0] - offset
        lig_rmsd = np.sqrt(np.mean(np.sum(((lig_xyz - center) @ rotation - ref_ligand_heavy)**2, axis=1))) / 10
        pair_distances = distance_array(heavy.positions, ligand_heavy.positions, box=ts.dimensions) / 10
        atom_nearest = pair_distances.min(axis=1)
        res_nearest = np.full(len(residue_numbers), np.inf)
        np.minimum.at(res_nearest, atom_to_residue, atom_nearest)
        contact_distances.append(res_nearest)
        target_distances = distance_array(donor.position[None, :],
                                         np.array([acceptor.position, amide_n.position]),
                                         box=ts.dimensions)[0] / 10
        hd = minimize_vectors((donor.position-hydrogen.position)[None, :], ts.dimensions)[0]
        ha = minimize_vectors((acceptor.position-hydrogen.position)[None, :], ts.dimensions)[0]
        cosine = np.dot(hd, ha) / np.linalg.norm(hd) / np.linalg.norm(ha)
        angle = np.degrees(np.arccos(np.clip(cosine, -1, 1)))
        hbond = target_distances[0] < .35 and angle >= 150
        records.append([ts.time, ca_rmsd, lig_rmsd, *target_distances, angle,
                        int(hbond), np.sum(res_nearest < .4)])
    values = np.array(records)
    distances = np.array(contact_distances)
    assert values.shape == (1001, 8) and np.all(np.isfinite(values))
    assert np.allclose(values[:, 0], np.arange(1001))
    fractions = np.array([(distances < cutoff).mean(axis=0) for cutoff in [.35, .4, .45]])
    ranked = np.argsort(-fractions[1], kind="stable")[:14]
    summary = {"frames": len(values), "time_ps": [0, 1000], "right_endpoint_included": True,
               "maximum_reconstructed_covalent_bond_nm": maximum_bond_nm,
               "CA_rmsd_mean_nm": float(values[:, 1].mean()),
               "ligand_protein_aligned_rmsd_mean_nm": float(values[:, 2].mean()),
               "ligand_protein_aligned_rmsd_range_nm": [float(values[:, 2].min()), float(values[:, 2].max())],
               "OAB_OE1_mean_nm": float(values[:, 3].mean()),
               "OAB_NE2_mean_nm": float(values[:, 4].mean()),
               "OAB_H12_OE1_angle_mean_deg": float(values[:, 5].mean()),
               "OAB_OE1_distance_fraction_below_035": float((values[:, 3] < .35).mean()),
               "OAB_H12_OE1_geometry_fraction": float(values[:, 6].mean()),
               "contact_residue_mean_at_040_nm": float(values[:, 7].mean()),
               "top_contact_residues": [{"resid": int(residue_numbers[i]), "resname": str(residue_names[i]),
                                         "fractions_035_040_045": fractions[:, i].tolist()} for i in ranked],
               "geometry_rule": "OAB donor–OE1 acceptor distance <0.35 nm and OAB–H12–OE1 angle >=150 degrees",
               "contact_rule": "A residue contacts if any of its heavy atoms is within the selected cutoff of any ligand heavy atom; nearest periodic images; one count per residue per frame"}
    (args.out / "complex_summary.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    np.savetxt(args.out / "complex_observations.csv", values, delimiter=",", header=
               "time_ps,CA_RMSD_nm,ligand_RMSD_nm,OAB_OE1_nm,OAB_NE2_nm,DHA_angle_deg,geometry_contact,residue_contacts", comments="")
    np.savez_compressed(args.out / "residue_contacts.npz", time_ps=values[:, 0],
                        nearest_nm=distances, resids=residue_numbers, resnames=residue_names)
    fig, axes = plt.subplots(2, 2, figsize=(14, 9), constrained_layout=True)
    t = values[:, 0]
    axes[0, 0].plot(t, values[:, 1], color="#167d84", label=tr("蛋白质 Cα", "Protein Cα"))
    axes[0, 0].plot(t, values[:, 2], color="#bd7045", label=tr("配体重原子", "Ligand heavy atoms"))
    axes[0, 0].set(title=tr("共同蛋白参照系中的运动", "Motion in the common protein frame"), ylabel="RMSD / nm")
    axes[0, 0].legend()
    axes[0, 1].plot(t, values[:, 3], color="#167d84", label="OAB–Gln102 OE1")
    axes[0, 1].plot(t, values[:, 4], color="#4d6fb0", label="OAB–Gln102 NE2")
    axes[0, 1].axhline(.35, color="#6c7271", lw=1, ls="--", label=tr("几何距离阈值", "Geometric distance cutoff"))
    axes[0, 1].set(title=tr("同一残基上的两种原子", "Two atoms in the same residue"), ylabel=tr("距离 / nm", "Distance / nm"))
    axes[0, 1].legend(fontsize=11)
    axes[1, 0].plot(t, values[:, 5], color="#bd7045", lw=.8)
    axes[1, 0].axhline(150, color="#6c7271", ls="--", lw=1)
    axes[1, 0].scatter(t[values[:, 6] == 1], values[values[:, 6] == 1, 5], s=3, color="#167d84",
                       label=tr("距离与角度同时满足", "Both distance and angle pass"))
    axes[1, 0].set(title="OAB–H12–OE1", ylabel=tr("D–H–A 夹角 / °", "D–H–A angle / °"), ylim=(0, 185))
    axes[1, 0].legend(fontsize=11, loc="lower right")
    axes[1, 1].step(t, values[:, 7], where="mid", color="#4d6fb0", lw=.9)
    axes[1, 1].set(title=tr("0.40 nm 内的不同蛋白残基", "Distinct residues within 0.40 nm"),
                   ylabel=tr("接触残基数", "Contacting residue count"))
    for ax in axes.flat:
        ax.set(xlabel=tr("生产时间 / ps", "Production time / ps"), xlim=(0, 1000))
        ax.grid(alpha=.13)
    for suffix in ["svg", "png"]:
        fig.savefig(args.out / f"complex_motion.{suffix}", dpi=180)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(14, 8), gridspec_kw={"width_ratios": [1.4, 1]}, constrained_layout=True)
    labels = [f"{residue_names[i]} {residue_numbers[i]}" for i in ranked]
    axes[0].imshow((distances[:, ranked] < .4).T, origin="upper", interpolation="nearest", aspect="auto",
                   extent=(-.5, 1000.5, len(ranked)-.5, -.5), cmap=matplotlib.colors.ListedColormap(["#ece8dd", "#167d84"]), vmin=0, vmax=1)
    axes[0].set(yticks=np.arange(len(ranked)), yticklabels=labels, xlabel=tr("生产时间 / ps", "Production time / ps"),
                title=tr("逐帧接触：青色为有接触", "Framewise contacts: teal indicates contact"))
    for j, (cutoff, color) in enumerate(zip([.35, .4, .45], ["#bd7045", "#167d84", "#4d6fb0"])):
        axes[1].plot(fractions[j, ranked], np.arange(len(ranked)), "o-", ms=5, lw=.8, color=color, label=f"{cutoff:.2f} nm")
    axes[1].set(yticks=np.arange(len(ranked)), yticklabels=labels, ylim=(len(ranked)-.5, -.5), xlim=(-.03, 1.03),
                xlabel=tr("1001 帧中的接触比例", "Contact fraction among 1001 frames"),
                title=tr("改变距离阈值后的同一批记录", "The same frames at three cutoffs"))
    axes[1].legend(loc="lower center", bbox_to_anchor=(.5, 1.01), ncol=3, fontsize=11)
    axes[1].set_title(tr("改变距离阈值后的同一批记录", "The same frames at three cutoffs"), pad=48)
    axes[1].grid(alpha=.15)
    for suffix in ["svg", "png"]:
        fig.savefig(args.out / f"complex_contacts.{suffix}", dpi=180)
    plt.close(fig)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

Read md.tpr, md.xtc, and em.gro; verify the actual OAB–H12 bond; include all 1001 frames in averages. Save CSV records, residue-distance arrays, and two plot sets in the chosen language.

The first set of plots combines the global reference with local observations. Mean protein Cα RMSD from the minimized reference is 0.08791 nm. Mean ligand-heavy-atom RMSD in the protein frame is 0.10900 nm, with a range of approximately 0.02807–0.20775 nm. The first quantity describes Cα displacement across the protein; the second retains ligand movement relative to the pocket. Since their atom selections differ, curve heights must be read with those definitions. A local group can reorient enough to change interaction geometry while contributing very little to a whole-protein RMSD.

### Ligand motion and local geometry in the protein frame

1001 frames over 0–1000 ps. Protein Cα atoms are fitted equally to the minimized reference, and the ligand receives that transform; distances, D–H–A angle, and residue-contact counts share the same frames.

GROMACS 2026.4; resolved chain A residues 1–163 of 3HTB with neutral JZ4; AMBER99SB-ILDN/SPC/E and GAFF with AM1-BCC. The 33382-atom system contains 2614 protein atoms, 22 ligand atoms, 10226 waters, 31 Na⁺ and 37 Cl⁻; unrestrained production at 300 K and 1 bar lasts 1000 ps with 1001 saved frames.

[Download reference data and complete inputs (ZIP) 118.20 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-complex-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g10/en/#en-s7)

Protein Cα atoms are fitted equally to the minimized reference, with the same rigid transform applied to the ligand. The same 1001 frames compare Cα and ligand-heavy-atom RMSD, distances from OAB to two Gln102 atoms, the OAB–H12–OE1 angle and residue contacts within 0.40 nm. Molecular coordinates are reconstructed through the bond graph and bond lengths checked first.

The mean OAB–Gln102 OE1 distance is 0.34331 nm, compared with 0.51023 nm for OAB–NE2. The two curves reveal different spatial relationships within the same residue. Approximately 68.13% of frames have OAB···OE1 below 0.35 nm. Requiring the OAB–H12–OE1 angle also to reach at least 150° reduces the fraction satisfying both conditions to approximately 16.78%. This difference comes from orientation information in the very same atomic coordinates. The angle panel marks frames passing both tests, separating residue proximity, proximity to a particular acceptor, and a specified hydrogen-bond geometry.

With a 0.40 nm cutoff, an average of 9.3926 distinct protein residues contact the ligand per frame. The fractional value comes from averaging over time: a frame has an integer number of contacting residues, but many such counts need not average to an integer. Identity matters as well as total count. Two frames can have the same count with different residues surrounding the ligand; loss of one contact and formation of another can leave the total unchanged. The second visualization therefore places residues along rows and time along columns, with the associated contact fractions alongside.

### Contact identity, time, and distance thresholds

Top 14 residues ranked by contact fraction at 0.40 nm. Left: framewise contacts. Right: fractions at 0.35, 0.40, and 0.45 nm on the same 1001 frames. Fractions describe the selected observation window.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g10/en/#en-s7)

The top 14 residues are ranked by contact-time fraction at 0.40 nm. The time map retains contact identity in each frame, while the right panel compares thresholds of 0.35, 0.40 and 0.45 nm on the same trajectory, showing the effect of the measurement definition on the observed fraction.

Continuous coloured regions in the heatmap indicate intervals of frequent proximity, while interrupted bands show contacts entering and leaving the selected geometry. The three cutoff curves use identical frames. By definition, a wider cutoff can only increase a contact fraction or leave it unchanged. A residue that rarely contacts at 0.35 nm but frequently contacts at 0.45 nm has many distances within that interval, directing attention to its distance distribution and local structure. Frequent contact at all three cutoffs provides local-neighbour information that is less sensitive to the selected boundary.

These plots help choose a subsequent scientific comparison. One could modify a functional group and compare hydroxyl orientation distributions under the same reference-frame, temperature, and salt definitions. Alternatively, changing a pocket residue could reveal redistribution of nearby contacts. Before comparing models, fix the fitting selection, distance rule, thresholds, and observation window, and give each model independently randomized repetitions. The difference between models then has a clear measurement meaning, allowing the figures to connect directly to a defined chemical change.

## Designing the next study beyond local motion

Protein–ligand studies often discuss three levels together: the bound pose, the pathway of entry and release, and the free energy of binding relative to solution. This chapter establishes a complete workflow for the first level: identify the structure and chemistry, prepare compatible parameters, construct solution, release position restraints, and measure local motion. The same workflow reveals concrete preparation problems, such as incorrect names producing empty selections, protonation changing donor or acceptor identity, or disagreement between coordinate and topology order. It supplies a physical starting point whose assumptions and measurements can be inspected.

Entry and release require observation windows that cover events and the accompanying environmental changes. A ligand remaining inside a pocket for one nanosecond provides a structural record of that local stay. Estimating a dissociation rate instead requires enough dissociation events, well-defined states, and appropriate dynamical sampling. A single entry or exit is one realization of an event, so repetition and state statistics remain important. The question determines whether to extend ordinary trajectories, add varied starting states, or use a specialized rare-event method.

Binding free energy compares the statistical weights of different states. Intuitively, entering the pocket may provide favourable protein interactions while changing ligand–water interactions and reducing the positions, orientations, and conformations available in solution. An attractive protein–ligand energy measured in one frame omits these coupled changes. A free-energy calculation needs bound and solution reference states, treatment of restraints and standard-state conventions, and checks that relevant degrees of freedom have been sampled. The later free-energy chapter introduces this state-comparison language through reaction coordinates and biased sampling.

The same reasoning helps investigate protein contacts with functional groups on materials. Attaching a small molecule to a polymer restricts accessible positions through the attachment point and chain conformations. Arranging many such groups on a surface introduces density-dependent effects on protein approach and water organization. The atom-identity, contact, and orientation analyses developed here can be retained while the model expands to a specified chain or interface. The measured object changes with the research question, while the central relationship remains: chemical modeling defines the system, and each curve answers an explicit observation about it.

A substantive comparison can begin with one small modification. Keep the protein, temperature, and salt conditions fixed, change one ligand functional group, and generate complete parameters for each molecule. Compare location and orientation within the pocket, then examine which residue contacts persist, are replaced, or change direction. Give each model independently randomized repetitions, analyze matched windows, and distinguish sampling of fast and slow variables. Connecting these results to experimental affinity then adds a state-to-state free-energy calculation or an appropriate experimental observable. Model changes, trajectory measurements, and the experimental question consequently form a clear chain of reasoning.

After this chapter, an animation of a ligand moving inside a pocket carries more specific information. Whole-protein drift can be removed through the reference frame, ligand turning can become a geometric measurement, and a coloured contact cell corresponds to named atom selections and a distance condition. The intuitive ideas of meeting and fitting have become a runnable model, repeatable analysis, and a concrete basis for the next calculation.

## Further Reading and Open Materials

- [Protein Ligand Complex MD Setup tutorial using BioExcel Building Blocks](https://github.com/bioexcel/biobb_wf_protein-complex_md_setup) · BioExcel Building Blocks contributors · Apache-2.0

  3HTB/JZ4 example, AMBER99SB-ILDN/SPC/E/GAFF model, and the parameterize–merge–solvate–equilibrate–produce workflow.

  Rewritten as explicit commands and standalone scripts, with defined structural selections and HID31, retained bound heavy coordinates, GROMACS 2026.4 settings and longer sampling, and added local geometry/contact analyses.
- [3HTB: 2-propylphenol in complex with T4 lysozyme L99A/M102Q](https://doi.org/10.2210/pdb3HTB/pdb) · S. E. Boyce, D. L. Mobley, G. J. Rocklin, A. P. Graves, K. A. Dill, B. K. Shoichet · CC0-1.0 — PDB archive data

  Experimental starting coordinates and JZ4 bound pose; structural illustrations use selected actual coordinates.

  Retained resolved chain A residues 1–163 and JZ4, selected coherent A alternatives, and rebuilt hydrogens, solvent, and ions; termini and His31 states are specified in the text.
- [JZ4 chemical component: 2-propylphenol](https://www.rcsb.org/ligand/JZ4) · wwPDB Chemical Component Dictionary · CC0-1.0 — PDB archive data

  Molecular identity, formula, atom names, and bond orders.

  Combined chemical connectivity with the bound 3HTB coordinates for hydrogen addition and parameterization.
- [Predicting ligand binding affinity with alchemical free energy methods in a polar model binding site](https://doi.org/10.1016/j.jmb.2009.09.049) · Boyce et al. (2009) · Scientific citation; no reused text or figures

  Experimental research context for the 3HTB model pocket.

  This chapter examines local unbiased motion; the original paper supplies the binding-free-energy research context.
- [Application of a Theory of Enzyme Specificity to Protein Synthesis](https://doi.org/10.1073/pnas.44.2.98) · D. E. Koshland Jr. (1958) · Scientific citation; original conceptual illustration

  Historical context for induced fit and flexible recognition.

  New conceptual explanation and illustration; outlines represent a conceptual model.
- [Conformational changes: How small is big enough?](https://laskerfoundation.org/wp-content/uploads/2021/01/1998_koshland.pdf) · D. E. Koshland Jr. (1998) · Scientific citation; no reused text or figures

  The original author’s discussion of local conformational change and function.

  Explained in terms of the scale of local measurements.
- [General AMBER Force Field](https://ambermd.org/antechamber/gaff.html) · Amber developers; Wang et al. · Scientific/software attribution; generated molecular parameters

  GAFF atom types, parameter-family compatibility, and AM1-BCC background.

  Explicit GAFF selection and zero net charge; ACPYPE generates the example-specific ligand parameters.
- [ACPYPE — AnteChamber PYthon Parser interfacE](https://github.com/alanwilter/acpype) · ACPYPE contributors · GPL-3.0 for ACPYPE software

  Calling AmberTools and producing GROMACS topology, version 2026.10.15.

  Invocation scripts are provided; bound coordinates are retained by atom identity after generation.
