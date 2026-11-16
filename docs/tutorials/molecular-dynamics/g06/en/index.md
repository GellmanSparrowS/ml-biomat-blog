# Putting a protein in water: topology, solvent, and ions

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g06/en/
Language: en

Build a defined ubiquitin solution while connecting periodic geometry, three-site water, and integer ion counts to their physical meaning.

## Why water belongs in the model

A grain of salt loses its familiar shape when it dissolves in water. A protein also responds to its surroundings, although its response involves changes in molecular interactions and motion rather than simply disappearing from view. Water occupies most of the volume in many biomolecular simulations, yet it is often hidden when we display the protein. This makes the protein easier to see while concealing an active part of the system. In this chapter, we continue with ubiquitin and place the prepared protein in a solution with a specified water model, salt content, and periodic geometry. You will learn what each preparation step adds, how to check agreement between coordinates and topology, and how to calculate salt concentration from the particles actually present.

The electrons in a water molecule are distributed unevenly: the oxygen region is relatively negative and the hydrogen regions are relatively positive. Consequently, a molecule with no net charge can still turn different parts of itself toward charged neighbors. Charged protein side chains, groups that form hydrogen bonds, and surfaces that make less favorable contacts with water all influence the arrangement and motion of nearby solvent. Water molecules also interact with one another, and thermal motion continuously rearranges their neighbors. Protein conformation, exposed surface area, and the positions of chemical groups therefore belong to one coupled system rather than separate descriptions.

Think of people changing their positions in a crowded conversation. One person's turn changes several distances and may prompt nearby people to move. Molecules have no intentions: forces and thermal fluctuations determine their motion. The useful part of the analogy is that the surroundings respond as the central object changes. An explicit-solvent simulation includes the interaction sites of individual water molecules, allowing us to examine where water is located, how it is oriented, and how long it occupies a region. This resolution is useful for hydration layers, ion distributions, and the approach of small molecules to a protein. Its computational cost increases with the number of solvent particles.

Our system combines the AMBER99SB-ILDN protein parameters with TIP3P, a three-site water model used with this force-field family. The object of study is a free ubiquitin monomer surrounded by water and ions. Each water has one oxygen site and two hydrogen sites, with specified molecular geometry maintained during the subsequent dynamics. The selected parameters jointly determine protein–water, water–ion, and other interactions. A classical fixed-topology model describes the motion and contacts of these chemical species. Water dissociation, proton transfer along a hydrogen-bond network, and chemical reactions require a description capable of handling the relevant electronic or bonding changes. Connecting the intended process to the model gives the preparation commands a clear purpose.

Preparing a simulation resembles arranging a solution experiment: the container size, amount of solute, and solvent identity all matter. Here the container is a periodic cell, particle counts are integers, and concentration depends on both count and volume. We will construct an initial system containing one ubiquitin molecule, 5868 water molecules, 17 sodium ions, and 17 chloride ions. The following chapter will minimize its energy and prepare its temperature and pressure. Our task here is to establish a consistent composition and spatial arrangement, so the dynamics starts from a system whose chemical identities and geometry are understood.

[Figure: Protein, water, and ion composition](https://ml-biomat.com/tutorials/molecular-dynamics/g06/en/#en-s1)

Figure 1 · Water and ions are mobile components. Shapes identify component types; counts come from the actual ion-containing structure.

## From conducting salt solutions to charged particles

Why dissolved salts help water conduct electricity was an important question in nineteenth-century physical chemistry. Solid sodium chloride contains an ordered arrangement of positive and negative ions; in solution, charged species can move through the liquid. Arrhenius's work on electrolytic dissociation in the 1880s connected electrical conduction with mobile ions and helped explain why some solution properties did not scale simply with the number of chemical formula units added. The idea most directly relevant to our simulation is the distinction between adding one formula unit and counting the resulting mobile species: one NaCl formula unit supplies one sodium ion and one chloride ion.

The two ion types carry opposite charges. Equal numbers cancel in the total charge, while each ion still interacts with water and the protein. Water oxygen sites tend to face a nearby sodium ion because of their negative partial charge; hydrogen sites participate in favorable orientations around chloride. These hydration arrangements fluctuate, and neighboring waters can exchange. The schematic orientations in the figure illustrate the relationship between charge and orientation. Actual distributions also depend on crowding, water–water interactions, and temperature. Their combined effects are precisely why we allow the environment to move instead of assigning a permanent ring of water to each ion.

Ions also influence a protein through collective distributions rather than simply occupying one matching site for every protein charge. More distant ions contribute to the surrounding electrostatic environment, while nearby ions may make direct contacts with particular surface groups. Ion identity, concentration, protein surface chemistry, and the chosen parameters all affect these arrangements. We begin with monovalent sodium and chloride because their counts, charges, and concentration are relatively easy to connect. Replacing sodium with calcium would change the charge number, hydration behavior, and interaction parameters together. Changing the particle name alone would leave the physical model undefined.

By the later twentieth century, computers could follow the motion of many interacting water molecules. In 1983, Jorgensen and colleagues compared simple potential models for liquid water; TIP3P became an important member of this family of models. Such models reduce a complex electronic distribution to a small number of interaction sites and parameters, making the statistical behavior of a liquid computationally accessible. This simplification helped make explicitly hydrated protein simulations practical. It also made water-model selection part of the scientific method: different models have different performance for quantities such as density, diffusion, and dielectric response. A model name therefore refers to a particular geometry and set of interactions.

The connection between ionic theory and molecular water models is an increasingly precise account of which objects move and interact in a liquid. Writing NA, CL, OW, or HW in a coordinate file identifies sites but does not fully define their properties. Those names must connect to masses, charges, nonbonded parameters, and geometrical constraints in the topology. The historical picture of solution chemistry meets the computational workflow at this point: identify the species, define their interactions, and then study the statistics of their motion. The remaining sections translate these levels into a consistent set of files.

[Figure: Historical concepts of ionic conduction and three-site water](https://ml-biomat.com/tutorials/molecular-dynamics/g06/en/#en-s2)

Figure 2 · Ionic conduction involves mobile charged species. Three-site water uses a compact geometry and parameters to represent molecular charge distribution. δ labels partial-charge signs.

## Coordinates describe positions; topology defines the species

The processed.gro file from the previous chapter contains the positions of ubiquitin's atoms. The accompanying topol.top contains the protein topology and references to force-field definitions. A useful analogy is a numbered seating plan together with a description of each occupant and the rules connecting them. The plan lets us measure distances; the rules determine the forces at those distances. The two descriptions must use matching atom order and molecular composition. Whenever one file gains water or changes its particle count, the other needs a corresponding update so that each position is assigned the correct physical identity.

The reference to amber99sb-ildn.ff/forcefield.itp supplies the general force-field definitions. The protein topology then lists atoms, bonds, angles, and other interaction terms, while water and ions have their own definitions. Near the end of topol.top, the molecules section gives the actual number of each molecular species in the system. This hierarchy avoids defining an identical water model thousands of times: the model is defined once, and the molecules section specifies how many copies exist. In our preparation, the SOL count changes from 5902 to 5868 when ions are added. The water parameters stay the same; their number of occurrences changes.

The solvate command uses a water coordinate template called spc216.gro. Its name can cause confusion because our simulation still uses the TIP3P force field. The template supplies water molecules arranged in a small coordinate box. The program tiles these coordinates across the new cell and removes whole water molecules that overlap too closely with the protein. Such a three-site coordinate template can initialize different three-site water models. The selected water topology determines the charges, molecular geometry, and interaction parameters. Small differences between template geometry and the target model are handled during preparation and equilibration.

This distinction also explains why model parameters should be kept as a coherent set. Oxygen and hydrogen charges, oxygen repulsion and dispersion parameters, internal geometry, and the compatibility of ion parameters jointly influence solution behavior. Protein force fields and water models are normally used and evaluated in particular combinations. Taking charges from one water model while retaining another model's remaining parameters creates a new combination whose properties require evaluation. Here we retain AMBER99SB-ILDN with TIP3P and select NA and CL through the supplied force-field definitions. This keeps the model choice clear while we focus on preparation and interpretation.

Adding water is more subtle than filling a featureless shell outside a protein's outline. Protein surfaces contain grooves, and some internal regions may geometrically accommodate water. The solvate program uses coordinates, atomic size information, and overlap criteria to choose initial positions. This establishes a spatial arrangement; subsequent motion allows that arrangement to adjust collectively. Inspection can reveal obvious overlaps, unusually large empty regions, or close approaches to periodic images. For a system with known tightly associated waters, the structure-preparation decision should identify which experimental waters are retained. In this example, the previous chapter removed all 58 crystallographic water oxygen records before constructing the solvent environment.

When genion adds salt, it replaces selected whole water molecules with single ions and updates the molecular composition. A three-site water contributes three coordinate sites, whereas a monatomic ion contributes one. Each replacement therefore reduces the total site count by two. This gives a convenient independent check: adding 34 ions by replacing 34 waters must reduce the total by 68 sites. A successful command exit and a chemically consistent count address different questions. Combining them lets us confirm that the updated topology and coordinates describe the same solution.

## Leaving room for water with a periodic cell

A protein in a tiny water droplet would experience a substantial liquid surface. Many solution simulations instead aim to describe a bulk-like environment and use periodic boundaries. A cell is repeated by translations in three directions; a molecule leaving one side can be represented at its equivalent position on another side. Neighbors therefore remain available across the boundaries. Only one cell of particles is stored, with image positions defined geometrically. For the protein, this corresponds to a periodic arrangement of protein molecules and solvent, making the distance to its own images an important part of system preparation.

We use editconf to select the periodic geometry associated with a rhombic dodecahedron and set the distance option to 1.0 nm. For this box type, GROMACS obtains the size from the solute's maximum atom-to-atom diameter and adds space on both sides. Ubiquitin's initial diameter here is approximately 4.491 nm, giving a periodic geometrical scale of about 6.491 nm. This provides initial solvent space and is compatible with the chosen 1.0 nm short-range cutoff. Protein rotation, conformational changes, and later pressure-driven box adjustment can alter the nearest image separation, so this separation is also worth examining in the trajectory. The initial option does not fix a permanent gap throughout the simulation.

Why choose this geometry instead of a cube? For a compact solute, a rhombic dodecahedron can reduce the volume that must be filled while maintaining the same periodic image distance. Its volume is approximately 0.707 times that of a cube at the same image spacing, reducing the number of waters and the calculation required. The condition of equal image spacing matters: the ratio does not apply indiscriminately to any two boxes of roughly similar side length. Long fibers, membrane patches, and strongly anisotropic molecules can favor other cell shapes. The geometry should serve the scientific object, with solvent economy as one consideration.

A GRO file records this periodic geometry using three cell vectors rather than a drawing of a twelve-faced shell. Imagine three directed arrows from the same origin. Each arrow specifies a translation that reaches an equivalent cell. Here the vectors are a=(6.49145, 0, 0) nm, b=(0, 6.49145, 0) nm, and c=(3.24572, 3.24572, 4.59015) nm. Vector c has horizontal as well as vertical components and therefore points at an angle. Some viewers display particles inside the associated tilted parallelepiped, while others use a compact dodecahedral representation. These displays can describe the same system when they preserve the same periodic image relationships.

[Figure: Base and perpendicular height of a tilted cell](https://ml-biomat.com/tutorials/molecular-dynamics/g06/en/#en-s4)

Figure 3 · Three cell vectors encode periodic translations. For the specified arrangement, base area times the vertical component of c gives volume. The code reads all nine GRO components.

To calculate volume, the familiar rule “base area times perpendicular height” is more informative than multiplying three edge lengths. Vectors a and b are perpendicular and lie in the horizontal plane, giving a base area of 6.49145×6.49145 nm². The vertical component of c, 4.59015 nm, is the height above that base. Its horizontal components shift the upper face sideways without adding volume. A stack of equal sheets slid sideways illustrates the same geometry: sheet area and total thickness still determine its volume. For this coordinate arrangement, the volume reduces to a product of three components. A general tilted cell is handled by the determinant of its full matrix.

Volume of this tilted cellEq. 1

![Volume of this tilted cell](https://ml-biomat.com/static/agent-math/f2cda83301b667c908567f1f.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| V | Whole periodic-cell volume, including protein and solvent | nm³ |
| a_{x}, b_{y}, c_{z} | The x component of vector a, y component of b, and z component of c; here the perpendicular base edges and height | nm for each component |
| x, y, z | Subscripts identifying Cartesian directions | Direction labels; no units |
| =, × | Equality; adjacent components are multiplied, including their units | Operators; no units |

Reading the relationshipHere a lies along x and b along y, giving base area aₓbᵧ. The vertical component c_z supplies the height. Horizontal tilt adds neither base area nor height.

A worked example6.49145 nm×6.49145 nm×4.59015 nm=193.4239779 nm³. Multiplication by 10⁻²⁴ converts nm³ to L, giving 1.934239779×10⁻²² L.

ConditionsThis product applies to the triangular cell-vector arrangement specified in the text. A general cell uses the absolute determinant of its three-vector matrix.

The resulting volume is approximately 193.424 nm³. This is the initial cell volume used when adding ions; pressure equilibration will subsequently make the volume fluctuate. It includes the space occupied by the protein as well as water and ions. The concentration definition used by genion refers to this whole-cell volume. Making that definition explicit avoids silently replacing it with an estimated solvent-accessible volume and comparing two concentrations that use different denominators.

## How much salt is in this small box?

In the laboratory, we may weigh salt and prepare a specified volume of solution. In a simulation, we directly choose a number of ions. The mole connects these descriptions: one mole contains exactly 6.02214076×10²³ specified entities. This is the numerical value associated with the Avogadro constant. The entity must be identified: it might be a water molecule, a sodium ion, or a NaCl formula unit. A 0.15 mol/L NaCl solution contains the equivalent of 0.15 mol of NaCl formula units per liter. For fully dissociated monovalent salt, it supplies the same amount of sodium ions and chloride ions separately.

Our cell is so small that nanometers are convenient for its dimensions. One nanometer is one billionth of a meter. Cubing this length conversion gives 1 nm³=10⁻²⁷ m³=10⁻²⁴ L, so the cell volume is approximately 193.424×10⁻²⁴ L. Dividing 17 sodium ions by the Avogadro constant converts the particle count to an amount in moles; dividing that amount by the volume gives sodium molarity. There are also 17 chloride ions, giving the same chloride molarity. In this neutral NaCl example, the formula-unit salt concentration equals the concentration of either individual ion species.

Molar concentration from particle countEq. 2

![Molar concentration from particle count](https://ml-biomat.com/static/agent-math/257497979f3e07ea10b6ac21.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| c | Molar concentration of the specified entity; here NaCl formula units or one ion species | mol/L; multiply by 1000 for mM |
| N | Number of counted entities; 17 NaCl pairs correspond to 17 formula units | Integer count; dimensionless |
| N_{A} | Avogadro constant, 6.02214076×10²³ entities per mole | mol⁻¹ |
| V_{L} | Whole-cell volume expressed in liters; subscript L identifies the volume unit | L |
| =, /, × | Equality, division, and multiplication; the fraction divides N by the full denominator, whose adjacent factors multiply | Operators; no units |

Reading the relationshipN/N_A converts entity count to moles, followed by division by solution volume. The denominator has units mol⁻¹×L, giving mol/L.

A worked exampleWith N=17 and V_L=193.4239779×10⁻²⁴ L, c=0.14594449 mol/L=145.94449 mM. Eighteen pairs give 154.52946 mM.

ConditionsThis defines a cell-average concentration at the current volume. Local hydration concentrations require separate measurement. For NaCl formula units, do not add positive and negative ion counts.

Using the actual cell volume, 17 ion pairs correspond to 0.145944 mol/L, or approximately 145.94 mM. The unit mM means millimoles per liter, so 1000 mM equals 1 mol/L. The command requests a nominal 150 mM, but the realized value is slightly lower because particle counts must be integers. Adding one more NaCl pair to this cell changes the concentration by about 8.585 mM, and 18 pairs would give approximately 154.53 mM. The target lies between these two possibilities. In a larger cell, the same one-pair increment changes concentration by less, giving finer concentration resolution.

A second counting distinction is equally useful. Seventeen sodium ions plus seventeen chloride ions give 34 ions in total, but the NaCl concentration is not obtained by replacing 17 with 34 in the preceding calculation. One formula unit supplies both ion species, so the formula-unit count remains 17. If the question concerns total ion particle density, we can add the species and explicitly report total ion concentration. Different physical questions use different counted entities. The definition accompanying a concentration is therefore as important as its numerical value. Ionic strength, osmotic properties, and diffusion will use related but distinct quantities.

Neutralization and salt addition also serve different purposes. Neutralization adjusts the net charge to a chosen value, usually zero; salt addition establishes an environment containing both positive and negative ions. With the selected termini and His68 state, our ubiquitin has zero net charge. Seventeen Na⁺ and seventeen Cl⁻ therefore preserve neutrality. Suppose another protein instead carried −5e. After adding the same 17 NaCl pairs, five extra sodium counterions would be required for neutrality. The resulting counts would be 22 sodium and 17 chloride ions. Their concentrations would differ because the additional counterions compensate the protein charge.

Charge accounting for monovalent saltEq. 3

![Charge accounting for monovalent salt](https://ml-biomat.com/static/agent-math/a5706ea1e858b84d4c286486.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Q, Q_{p} | Total system charge and protein charge; subscript p denotes protein | C, or expressed as multiples of e |
| e | Positive elementary charge, 1.602176634×10⁻¹⁹ C | C |
| N_{Na}, N_{Cl} | Sodium and chloride counts; subscripts identify chemical species | Integer counts; dimensionless |
| Q/e, Q_{p}/e | Total and protein charges measured in elementary-charge units | Dimensionless |
| =, −, +, / | Equality, subtraction, addition, and division; each Na⁺ contributes +1 and each Cl⁻ contributes −1 | Operators; no units |

Reading the relationshipAdd the charges of all components. Each water has zero net charge here, so no water term is needed in this net-charge expression.

A worked exampleThe present system gives 17−17+0=0. For a protein with charge −5e, 22−17−5=0, requiring five additional sodium counterions.

ConditionsApplies to the listed Na⁺, Cl⁻, and neutral waters. Multivalent ions and other charged molecules require their corresponding charge factors.

The -conc option of genion calculates added salt from the whole-cell volume in the input TPR. The -neutral option adds the counterions needed for neutralization on top of that salt. Existing ions require attention: -conc specifies additional salt and does not subtract ions already present to achieve a final total concentration. Repeating the command on an already salted system therefore changes its composition. Keeping counts at each preparation stage and calculating concentration from the resulting system avoids this ambiguity. The interaction below connects cell volume, pair count, and protein charge so that their different roles can be explored directly.

Change pair count and whole-cell volume to compare salt addition with neutralization.

[Figure: Sodium and chloride count comparison](https://ml-biomat.com/tutorials/molecular-dynamics/g06/en/#en-s5)

An integer-count calculation using whole-cell volume. Counterions compensate protein charge; subsequent molecular dynamics describes positions and motion.

## A reproducible sequence for the cell, solvent, and ions

The preparation begins with protein.pdb from the previous chapter, containing the selected protein heavy atoms of chain A in 1UBQ. The script first repeats the same pdb2gmx choices: AMBER99SB-ILDN, TIP3P, explicit selection of HIE for His68, and the free charged termini used in this construction. This makes the chapter's preparation reproducible from its selected structure. The initial printf supplies choice 1 for the histidine state, selecting the neutral form with its ring hydrogen on NE2. This answer depends on the present residues and force field; another protein requires reading the prompts and inspecting its generated topology again.

The editconf command reads processed.gro and places the protein in the selected periodic cell. The -c option centers it, while -d 1.0 and -bt dodecahedron define the initial spacing and box type. Centering changes absolute positions while preserving internal distances and connectivity. Next, solvate takes the protein-containing cell through -cp, the solvent coordinate template through -cs, the output coordinates through -o, and the topology to update through -p. Each stage has a separate output filename, making it straightforward to compare what changed when solvent was added.

Before genion can operate, grompp compiles a TPR containing the system definition. The accompanying ions.mdp sets nsteps to zero. Its purpose at this stage is to combine coordinates, topology, and the required settings into an input that genion can read. No mdrun command is issued here, so the stage does not generate a segment of molecular motion. PME specifies long-range electrostatic treatment, and the short-range cutoffs are 1.0 nm, consistent with the subsequent workflow. Understanding this use of a TPR separates preparation of a computational system from the actual integration of its dynamics.

### System definition for ion replacement

```
integrator = steep
nsteps = 0
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

nsteps=0; grompp uses this file to build ions.tpr for genion.

The genion command specifies NA and CL through -pname and -nname, requests nominal 0.15 mol/L salt, enables neutralization, and fixes the replacement seed at 20261120. Selecting SOL chooses water molecules as the objects to replace. The seed makes this randomized preparation choice traceable, while the initial ion positions remain starting coordinates for subsequent dynamics. An equilibrium spatial distribution develops through motion. The selected solvent molecules must have consistent composition and form a contiguous solvent group. This is why the command selects the complete SOL group rather than an arbitrary collection of oxygen atoms.

### Build a salted aqueous protein system

```
#!/usr/bin/env bash
set -euo pipefail

# protein.pdb contains the complete selected chain A of 1UBQ.
printf '1\n' | gmx pdb2gmx -f protein.pdb -o processed.gro -p topol.top \
    -i posre.itp -ff amber99sb-ildn -water tip3p -his
gmx editconf -f processed.gro -o boxed.gro -c -d 1.0 -bt dodecahedron
gmx solvate -cp boxed.gro -cs spc216.gro -o solvated.gro -p topol.top
gmx grompp -f ions.mdp -c solvated.gro -p topol.top -o ions.tpr
printf 'SOL\n' | gmx genion -s ions.tpr -o solvated-ions.gro -p topol.top \
    -pname NA -nname CL -conc 0.15 -neutral -seed 20261120
python inspect_solution.py . --output solution-analysis --language en
```

Place protein.pdb, ions.mdp, and inspect_solution.py in one example directory. The protein file is the chain A selection from the preceding chapter. With GROMACS 2026.4, the final command creates counts and figures.

After execution, compare solvated.gro, solvated-ions.gro, and topol.top. The first two show the coordinate and particle-count changes; the third gives the updated molecular composition. Keeping each updated topology paired with its corresponding coordinates provides a consistent input for minimization. If their counts disagree, return to the operation that introduced the mismatch and regenerate the pair. Editing a topology count merely to make the total look correct can assign molecular definitions to the wrong sequence of coordinates, even when the final numbers happen to agree.

These commands run sequentially in the prepared GROMACS 2026.4 environment. The complete script stops when a command fails so that later steps do not use missing or incomplete output. For readers new to the command line, a useful approach is to identify each line's input and output, run the small system, and then compare the count report with the expected changes. At this point, solvent molecules, ions, and new cell information all have a physical purpose. The report becomes a record that can be interpreted rather than a collection of unfamiliar numbers.

## Checking composition and concentration in the actual output

The Python program below reads the two GRO files and the molecules section of the topology. In an orthogonal GRO cell, three box components can be placed on the matrix diagonal. A tilted cell supplies six additional components; the program rearranges all nine according to the file format and takes the absolute determinant of the resulting cell matrix. The determinant gives an oriented parallelepiped volume, and its absolute value gives the physical volume. Concentration therefore follows the actual periodic geometry, regardless of whether the structure viewer displays a visually rectangular box.

For counting, the program uses this TIP3P model's OW names to identify water molecules and checks that each water contributes three sites. NA and CL are counted as monatomic ions. It also checks that ion replacement preserves the initial cell, that the number of removed waters equals the number of inserted ions, and that coordinate counts agree with topology counts. These rules follow the names and composition of the present model. Four-site water, different ion names, or multiple protein molecules would require corresponding changes while retaining the same principle: the model determines how particles and molecules are counted.

### Complete Python: composition, volume, and salt concentration

```
"""Count molecules and quantify salt concentration in the prepared solution."""
import argparse
import csv
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AVOGADRO = 6.02214076e23


def gro(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    n = int(lines[1])
    rows = [dict(resid=int(line[:5]), resname=line[5:10].strip(),
                 name=line[10:15].strip(),
                 xyz_nm=[float(line[i:i+8]) for i in (20, 28, 36)])
            for line in lines[2:2+n]]
    v = [float(x) for x in lines[2+n].split()]
    if len(v) == 3:
        cell = np.diag(v)
    elif len(v) == 9:
        cell = np.array([[v[0], v[3], v[4]],
                         [v[5], v[1], v[6]],
                         [v[7], v[8], v[2]]])
    else:
        raise ValueError("A GRO cell requires three or nine components.")
    return rows, cell


def molecule_counts(path):
    counts, section = {}, ""
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split(";", 1)[0].strip()
        if line.startswith("["):
            section = line.strip("[] ")
        elif section == "molecules" and line and not line.startswith("#"):
            name, count = line.split()[:2]
            counts[name] = counts.get(name, 0) + int(count)
    return counts


def main():
    p = argparse.ArgumentParser()
    p.add_argument("directory", type=Path)
    p.add_argument("--output", type=Path, default=Path("solution-analysis"))
    p.add_argument("--language", choices=("zh", "en"), default="en")
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    before, cell0 = gro(args.directory / "solvated.gro")
    after, cell = gro(args.directory / "solvated-ions.gro")
    top = molecule_counts(args.directory / "topol.top")
    if not np.allclose(cell, cell0):
        raise ValueError("Ion replacement should preserve the initial cell.")
    water_before = sum(a["resname"] == "SOL" and a["name"] == "OW" for a in before)
    water_after = sum(a["resname"] == "SOL" and a["name"] == "OW" for a in after)
    water_sites = sum(a["resname"] == "SOL" for a in after)
    na = sum(a["resname"] == "NA" for a in after)
    cl = sum(a["resname"] == "CL" for a in after)
    protein_atoms = len(after) - water_sites - na - cl
    assert water_sites == 3 * water_after
    assert (top["SOL"], top["NA"], top["CL"]) == (water_after, na, cl)
    assert top["Protein_chain_A"] == 1
    assert water_before - water_after == na + cl
    volume = float(abs(np.linalg.det(cell)))
    litre_volume = volume * 1e-24
    pair_increment_mM = 1000 / (AVOGADRO * litre_volume)
    summary = dict(initial_cell_vectors_nm=cell.tolist(),
                   initial_cell_volume_nm3=volume,
                   protein_atoms=protein_atoms, waters_before=water_before,
                   waters_after=water_after, sodium_ions=na, chloride_ions=cl,
                   total_atoms=len(after), topology_molecules=top,
                   sodium_concentration_mM=na*pair_increment_mM,
                   chloride_concentration_mM=cl*pair_increment_mM,
                   one_pair_increment_mM=pair_increment_mM,
                   nominal_added_salt_mM=150,
                   ionic_charge_e=na-cl,
                   atom_count_expected=protein_atoms+3*water_after+na+cl)
    (args.output / "solution_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    with (args.output / "salt_count_concentration.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["NaCl_pairs", "concentration_mM"])
        writer.writerows((n, n*pair_increment_mM) for n in range(36))
    zh = args.language == "zh"
    fonts = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC",
             "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else ["DejaVu Sans"]
    plt.rcParams.update({"font.family": fonts,
                         "font.size": 14, "svg.fonttype": "path",
                         "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), constrained_layout=True)
    axes[0].bar([0, 1], [water_before, water_after], color=["#a9c9c0", "#257d85"])
    axes[0].set_xticks([0, 1], ["加盐前", "加盐后"] if zh else ["Before ions", "After ions"])
    axes[0].set_ylabel("水分子数" if zh else "Water molecules")
    axes[0].set_ylim(0, water_before*1.15)
    for i, n in enumerate([water_before, water_after]):
        axes[0].text(i, n+80, str(n), ha="center")
    axes[1].bar([0, 1], [na, cl], color=["#b6773f", "#567795"])
    axes[1].set_xticks([0, 1], ["Na⁺", "Cl⁻"])
    axes[1].set_ylim(0, max(na, cl)*1.2)
    axes[1].set_ylabel("离子数" if zh else "Ions")
    for i, n in enumerate([na, cl]):
        axes[1].text(i, n+.4, str(n), ha="center")
    n = np.arange(36)
    axes[2].plot(n, n*pair_increment_mM, color="#8fa8a1", lw=1.5)
    axes[2].scatter(n, n*pair_increment_mM, color="#257d85", s=20)
    axes[2].axhline(150, color="#b6773f", linestyle="--", label="150 mM")
    axes[2].scatter([na], [na*pair_increment_mM], color="#b6773f", s=80, zorder=4)
    axes[2].set_xlabel("NaCl离子对数" if zh else "Number of NaCl pairs")
    axes[2].set_ylabel("按整盒体积计算的浓度 / mM" if zh else "Whole-cell concentration / mM")
    axes[2].legend(frameon=False)
    for ax in axes:
        ax.grid(axis="y", alpha=.2)
        ax.set_axisbelow(True)
    fig.suptitle("泛素溶液：组成与整数离子数" if zh else "Ubiquitin solution: composition and integer ion counts", fontsize=19)
    fig.savefig(args.output / "solution_composition.svg")
    fig.savefig(args.output / "solution_composition.png", dpi=150)
    plt.close(fig)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

Requires NumPy and Matplotlib. Reads solvated.gro, solvated-ions.gro, and topol.top from the supplied directory. Use --language zh or en for figure language.

The actual output contains 5902 waters before ion replacement and 5868 afterward. Their difference, 34, equals the combined number of sodium and chloride ions. The protein retains 1231 atoms, giving a final total of 1231+3×5868+17+17=18869 sites. Addition combines the component counts, while multiplication accounts for three sites per water molecule. A second calculation reaches the same total: the solvated structure initially contains 18937 sites, and 34 replacements of three-site water by one-site ions remove 68 sites. Agreement between these two routes provides a transparent check of the molecular replacement.

### Actual composition of the ubiquitin solution

Initial periodic volume: 193.4239779 nm³. Water count changes from 5902 to 5868, with 17 Na⁺ and 17 Cl⁻. The right panel calculates concentration from integer pair counts and whole-cell volume; the orange point marks the actual 17-pair preparation.

GROMACS 2026.4; chain A of PDB 1UBQ, 76 residues; AMBER99SB-ILDN with TIP3P. All 602 experimental heavy atoms are retained and 629 hydrogen atoms added. His68 uses neutral NE2 protonation, with charged free termini.

[Download reference data and complete inputs (ZIP) 0.53 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-protein-solution-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g06/en/#en-s7)

Solution composition checked against the actual GRO coordinates and topology. Seventeen Na⁺ and seventeen Cl⁻ replace 34 whole waters. The right panel converts integer pair counts into concentrations using the initial cell volume of 193.4239779 nm³; adding one pair changes the concentration by a discrete increment.

The left panel shows the small reduction in water count, the middle panel shows equal positive and negative ion counts, and the right panel converts integer NaCl pair counts to whole-cell concentration. The horizontal 150 mM target lies between the points for 17 and 18 pairs; the actual preparation occupies the 17-pair point. Showing the continuous concentration scale alongside discrete particle numbers explains the small system more fully than reporting “150 mM” alone. The numerical report retains extra digits for reproducibility, while approximately 146 mM is an appropriate concise description of the initial realized concentration.

These figures describe composition and geometry at preparation. Local hydration, enrichment of ions near particular protein sites, and the evolution of density and pressure require the subsequent trajectory. In particular, pressure coupling changes volume while particle numbers remain fixed, so concentration calculated from instantaneous volume also fluctuates. A useful scientific account can give the nominal salt setting, actual ion counts, and average volume of the analyzed trajectory. Together they make both the concentration definition and the stage of the simulation clear.

## Matching solution conditions to the research question

The system now has specified chemical composition, periodic geometry, and interaction parameters. Its initial positions next need to adjust under those interactions. Newly placed water and randomly positioned ions have not yet undergone their local rearrangement, and the protein must adapt to its current environment. Energy minimization first resolves unfavorable close contacts, followed by preparation at the chosen temperature and pressure. Treating composition preparation and state preparation as related stages helps locate problems: counts and charge lead back to this chapter, while unusual temperature, volume, or local contacts lead to the procedures examined next.

For an introductory question about ubiquitin's surface motion, this provides a defined starting point: a free monomer, explicit water, monovalent salt, fixed protonation choices, and periodic boundaries. Zero net protein charge still leaves positively and negatively charged surface regions, to which water and ions respond differently. When we later examine structural fluctuations, these interactions remain part of the explanation. The same modeling logic extends to DNA, carbohydrates, and polymer solutions, although the required parameters and scientific questions change with the molecular system.

If the goal becomes measuring how a particular salt affects protein structure, the comparison should be organized around that change. Keep the protein model, temperature, pressure, analysis definitions, and preparation procedures consistent where possible; specify whether ion identity or amount is changing; and verify actual particle numbers and final volumes. In a small cell, concentration increments may cause two nominal settings to produce the same integer number of ions. A larger cell or conditions distinguishable by particle count may then be useful. This check translates an experimental comparison into genuinely different computational systems.

Other questions concern long-lived ion contacts, rare binding events, or slow conformational responses to salt. Their sampling times and independent replicas should match those processes, and ion parameters should suit the relevant coordination environment. These considerations help choose the next observable: rapid local hydration changes, an average spatial distribution, or probabilities spanning several conformational states. A consistently prepared solution supplies the common foundation. Trajectories, statistical analysis, and appropriate model evaluation then connect that foundation to the specific question.

Each number in our preparation now has a physical interpretation. The initial periodic volume is 193.424 nm³; 5868 is the number of remaining water molecules; 17 and 17 are the positive and negative ion counts; approximately 146 mM is the salt concentration calculated from the whole cell; and 18869 is the total number of atomic sites advanced by the program. With these meanings established, defining a cell, solvating, and adding ions become a set of inspectable modeling decisions. The next chapter uses this defined composition to examine how energy, temperature, and volume guide preparation of a protein trajectory.

## Further Reading and Open Materials

- [Introduction to Molecular Dynamics](https://tutorials.gromacs.org/docs/md-intro-tutorial.html) · Cathrine Bergh; Maryam Majdolhosseini; Alessandra Villa · CC BY 4.0

  Cell construction, solvation, TPR preparation, and ion replacement.

  Retains the operation sequence with 1UBQ/AMBER99SB-ILDN/TIP3P; adds cell-volume reasoning, integer salt concentration, and composition checks.
- [From Proteins to Perturbed Hamiltonians: A Suite of Tutorials for the GROMACS-2018 Molecular Simulation Package](https://github.com/jalemkul/gmx_tutorials_livecoms) · Justin A. Lemkul · CC BY 4.0

  Protein-solution preparation and topology-update sequence.

  Uses ubiquitin and GROMACS 2026.4, with bilingual explanation, count figures, and a complete analysis program.
- [gmx editconf — GROMACS 2026.4](https://manual.gromacs.org/2026.4/onlinehelp/gmx-editconf.html) · GROMACS developers · GROMACS documentation terms; factual reference

  Command options and geometrical or counting behavior.

  Independent explanation of the options and output used here.
- [gmx solvate — GROMACS 2026.4](https://manual.gromacs.org/2026.4/onlinehelp/gmx-solvate.html) · GROMACS developers · GROMACS documentation terms; factual reference

  Command options and geometrical or counting behavior.

  Independent explanation of the options and output used here.
- [gmx genion — GROMACS 2026.4](https://manual.gromacs.org/2026.4/onlinehelp/gmx-genion.html) · GROMACS developers · GROMACS documentation terms; factual reference

  Command options and geometrical or counting behavior.

  Independent explanation of the options and output used here.
- [The Nobel Prize in Chemistry: The Development of Modern Chemistry](https://www.nobelprize.org/prizes/themes/the-nobel-prize-in-chemistry-the-development-of-modern-chemistry/) · Bo G. Malmström; Bertil Andersson; Nobel Foundation · Public historical reference; factual discussion

  Historical context of Arrhenius's work on electrolytic dissociation.

  Rewritten discussion of solution species with an ionic-migration schematic.
- [Comparison of simple potential functions for simulating liquid water](https://doi.org/10.1063/1.445869) · William L. Jorgensen; Jayaraman Chandrasekhar; Jeffry D. Madura; Roger W. Impey; Michael L. Klein · Publisher copyright; factual citation

  The 1983 comparison of water models and the context of TIP3P.

  Summarizes the modeling idea with a conceptual water-site diagram.
