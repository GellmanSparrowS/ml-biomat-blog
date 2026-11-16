# From an experimental structure to a protein model

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g05/en/
Language: en

Start with ubiquitin's role as a molecular tag, read its sequence and structural records, and define hydrogens, termini, and charges before building the GROMACS model.

## Begin with a molecular tag inside the cell

Cells continually make proteins and organize the removal or redistribution of proteins that are damaged, have completed their task, or need to change in abundance. A busy warehouse provides a useful first comparison: the route taken by an item depends on its labels and on the machinery that recognizes them. Ubiquitin is a small protein involved in this kind of molecular recognition. It can be attached covalently to other proteins, and ubiquitin molecules can themselves form chains with different linkages. Some of these chains participate in targeting proteins to the proteasome for degradation; other forms participate in signalling or transport. The tag analogy leads naturally to a structural question: how do shape, charge, and motion allow the tag to be recognized?

Our first protein model is a free ubiquitin monomer. Its 76 amino-acid residues form a compact body with a tail extending away from that body, making it a useful example for connecting a chemical chain with a three-dimensional fold. We begin with the public experimental structure 1UBQ, identify its protein and water records, and construct a chemical model suitable for GROMACS. Subsequent chapters place this same model in salt water, examine its structural motion, and compare statistics from independent trajectories. Keeping the molecule consistent across these steps gives every preparation choice a later consequence that we can inspect. Atom names, terminal groups, and solvent definitions become parts of one continuous investigation.

Why devote a chapter to preparation before investigating motion? Imagine studying how a folding umbrella opens. A photograph shows its outline, but a mechanical calculation also requires the connections between rods, the locations of hinges, and the attachment of the fabric. A protein structure file contains a similar distinction between visible geometry and the rules needed for calculation. Coordinates specify where atoms are initially placed. A topology specifies their connections, charges, and interactions. Combining the two allows the force and integration rules from the preceding chapters to generate motion. A missing residue or an incorrect terminal group changes the connectivity or forces of this molecular umbrella, even if the starting picture still looks plausible.

The experimental 1UBQ coordinates describe a conformation of ubiquitin in a crystal, whereas our next system will represent a free monomer in solution. Crystal packing, experimental conditions, and the boundary conditions of the solution model differ. We therefore specify which chain is retained, how crystallographic waters are handled, and how hydrogen positions are supplied. The resulting simulation concerns the conformation and fluctuations of this particular chemical model in its chosen environment. Studying ubiquitin covalently attached to another protein, recognized by an enzyme, or participating in degradation requires the relevant partners and connections. The free monomer gives us a manageable foundation for understanding those more elaborate systems.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g05/en/#en-s1)

Figure 1 · Experimental 1UBQ structure: 602 protein heavy atoms and 58 crystallographic water oxygens. The Cα trace reveals the chain path in a projection of the complete structure.

First follow the backbone through the figure, then look at the atoms around it. Two kinds of neighbourhood become apparent. Residues adjacent along the sequence are connected through the chain, while residues far apart in sequence can become close neighbours after folding. A terminal segment can also project outward from the compact body. A protein is therefore both a polymer with a repeating backbone and a biological macromolecule with chemically different side groups arranged along that backbone. Its shape reflects both features. Switching between the chain trace and the atom representation helps connect a recognizable overall fold to the specific chemical sites that will later be selected for measurements.

## Read the chemical language of a protein chain

An amino acid can initially be understood as a small molecule with a common set of connecting groups and a variable side group. In a protein, the backbone repeatedly passes through a nitrogen atom N, a central carbon Cα, and a carbonyl carbon C. Peptide bonds join neighbouring units. An amino-acid unit incorporated into the chain is called a residue: the name reflects its participation in the linked molecule rather than the presence of an intact, isolated amino acid beside its neighbours. The residues in our 1UBQ chain are numbered from 1 to 76. A residue number is an address along the chain, and an atom name identifies a site within that address. CA in residue 3 and CA in residue 4 are distinct atoms.

Side groups extend from this common backbone and give residues different chemical properties. In the model used here, lysine and arginine adopt positively charged states, while aspartate and glutamate adopt negatively charged states. Leucine and isoleucine have substantial nonpolar portions. Folding in water depends on the combined interactions of these groups with water and with one another, together with chain connectivity and the number of accessible conformations. Descriptions such as hydrophilic and hydrophobic provide a useful first reading of a molecular surface. The calculation itself uses atom types, partial charges, geometry, and the surrounding system. Even a charged side chain contains a hydrocarbon segment, so its orientation determines which chemical features are exposed.

Helices, arrows, and smooth ribbons in protein pictures are visual representations of structural organization. An α helix identifies a recurring local arrangement of the backbone; arrows in a β sheet emphasize extended chain segments and their directions; connecting loops adopt other backbone conformations. These shapes are inferred from the atomic structure. GROMACS does not add a separate object called a helix to the molecular model. The calculation still acts on atoms, their connections, and the potential energy. Moving between a ribbon view and an atom view is therefore useful: one reveals how the chain is organized, and the other reveals the actual sites involved in a contact or measurement.

Distances follow from coordinates using the familiar Pythagorean construction. Differences along the three Cartesian directions are the components of the line joining two atoms. Squaring and adding them prevents opposite signs from cancelling; taking the square root returns a length from a squared length. For a complete protein structure that has not been split across periodic boundaries, this gives the separation between adjacent Cα atoms directly. Later, a trajectory may contain a protein wrapped through the boundary of its simulation cell. In that setting, molecular continuity must first be restored before the same geometric expression is applied. The distance definition remains simple, while the coordinate preparation depends on the representation.

Distance between two atomic coordinatesEq. 1

![Distance between two atomic coordinates](https://ml-biomat.com/static/agent-math/8f4bea339fd28c77b7cf71d8.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| dᵢⱼ | Spatial distance between atoms i and j | Å or nm, matching the coordinate units |
| xᵢ, yᵢ, zᵢ; xⱼ, yⱼ, zⱼ | Cartesian position components of the two atoms | Å or nm |
| i, j | Indices identifying the two atoms | 1 (dimensionless) |
| =, −, + | Equality; subtraction forms coordinate differences; addition sums the three squared components | 1 (dimensionless) |
| ², √ | Squaring multiplies a value by itself; the square root gives the nonnegative distance | Squared terms have length²; the root has length |

Reading the relationshipThe coordinate differences are perpendicular components of one spatial displacement. The Pythagorean sum of squares followed by a square root gives its length without cancellation between positive and negative directions.

A worked exampleCoordinate differences of 3, 4, and 0 Å give d=√(9+16+0)=5 Å=0.5 nm. Actual adjacent Cα separations in 1UBQ range from approximately 3.759 to 3.854 Å.

ConditionsApplies directly to the complete, unwrapped structure here. Periodic trajectories require molecular continuity or an appropriate periodic distance treatment. Adjacent Cα separation spans several backbone bonds.

The actual adjacent Cα separations in this structure range from about 3.759 to 3.854 Å, or 0.376 to 0.385 nm. Adjacent Cα atoms are not joined by one direct covalent bond: the backbone path between them also includes a carbonyl carbon and the next nitrogen. This spacing should therefore be distinguished from the length of a single carbon–carbon bond. It is nevertheless a useful geometric check. A large separation between consecutive residue numbers invites inspection for missing residues, numbering discontinuities, or accidentally joined chains. Geometry provides one part of the evidence; checking the heavy atoms expected for each residue and the actual peptide connections supplies the chemical part.

## How experiments connected sequence with three-dimensional structure

Opening a modern structure database can make two hard-won kinds of knowledge appear inseparable: the order of chemical units along a chain and the way that chain folds in space. During the 1950s, Sanger and colleagues studied fragments of insulin to establish its amino-acid sequence and the connections between its chains. The logic resembles reconstructing a long sentence from overlapping phrases. Knowing how many letters of each kind are present is insufficient; the order must be determined. Sequence analysis made that order an experimentally testable chemical description and provided a clear basis for comparing proteins. It also established what a structural model must contain, even before the spatial arrangement of those components is known.

The spatial arrangement required a different measurement. In 1958, Kendrew and colleagues published a three-dimensional model of myoglobin obtained by X-ray analysis. The early, lower-resolution electron-density map revealed the overall path of the folded chain and the region occupied by the haem group. Improvements in data and analysis led to work published in 1960 at 2 Å resolution. The historical sequence matters: investigators first identified the overall fold and then resolved finer features. They did not begin with a sharp photograph of every atom. The progress of protein crystallography also depended on the ability of electronic computers to process the many measurements and calculations involved in diffraction analysis.

[Figure: History of protein sequence, structure, and ubiquitin attachment](https://ml-biomat.com/tutorials/molecular-dynamics/g05/en/#en-s3)

Figure 2 · Sequence determination, X-ray structure analysis, and ubiquitin-conjugation studies address chemical order, spatial arrangement, and biological action. Chains and connections are shown schematically.

X-ray crystallography begins with diffraction observations. Using those observations and phase information, researchers construct electron-density maps, build atomic models consistent with the density, and refine coordinates and other parameters against the data. PDB coordinates express the result of that modelling process. Resolution indicates the spatial detail supported by the diffraction data, but a resolution of 1.8 Å does not mean that every atomic coordinate has an error of exactly 1.8 Å. Local density, occupancy, and disorder can differ substantially across a structure. Reading the overall resolution and inspecting local records are complementary tasks, much as a map scale and the quality of a particular surveyed road provide different information.

The biological history of ubiquitin introduced another question: why does selective protein breakdown inside cells require energy? Through biochemical separation, reconstitution, and labelling experiments, Hershko, Ciechanover, Rose, and their collaborators progressively established ubiquitin-mediated protein degradation. Rose's account describes the unexpected finding that a small protein became covalently attached to a protein targeted for breakdown. This connected molecular identity with biological action. Ubiquitin must present surfaces that can be recognized and a chemical site through which it can be attached to other molecules. A small folded protein thus brings together structure, connectivity, and recognition. These are precisely the features that must be distinguished when a computational model is prepared.

The historical questions suggest a practical preparation order. First match the sequence to the coordinate records and establish which residues are present. Next inspect the regions represented more or less clearly by the experimental model. Then choose chemical states and connections appropriate to the scientific task. Here, all 76 residues enter the model of a free monomer, with charged free termini. In a model of ubiquitin attached to another protein, the terminal connectivity and associated charge distribution would change. The distinction between sequence, fold, and function is therefore useful at the keyboard: each level supplies information that another level alone cannot determine, and each leads to a concrete preparation decision.

## Read the different records in 1UBQ

Begin by counting clearly defined objects. The 1UBQ entry was determined by X-ray crystallography at 1.8 Å resolution. Chain A contains 76 residues and 602 protein heavy atoms, while 58 additional records describe crystallographic water oxygen atoms. Heavy atom here means an atom other than hydrogen; it does not imply a heavy metal. The original file contains no protein hydrogen coordinates and no alternative atom locations. Adding 602 protein atoms and 58 water oxygens gives 660 atom records, while 76 counts residues. Separating these levels avoids confusion when the generated protein later contains 1231 atoms: the increase comes from adding hydrogens, while the number of residues remains unchanged.

The traditional PDB text format uses fixed columns for atom names, residue names, chain identifiers, residue numbers, Cartesian coordinates, occupancies, and B factors. Some spaces therefore carry structural meaning. Splitting every line into whitespace-separated words and assuming that a particular word always identifies the same field is unreliable across different structures. Our script reads the relevant character intervals explicitly. It also retains the coordinate units: PDB coordinates are in ångströms, whereas the GRO files used here express coordinates in nanometres. The numerical length differs by a factor of ten, and the corresponding numerical volume differs by a factor of one thousand. Unit handling belongs in the initial reading step.

Occupancy describes the occupancy of an atomic position in the crystallographic model. It commonly lies between zero and one; partial occupancy may accompany alternative states, disorder, or other details of the experimental model. The B factor is a refinement parameter describing the attenuation of atomic scattering with spatial frequency. It is expressed in Å² and can reflect both thermal motion and static disorder. In this entry, 28 protein atoms have occupancy below one, while another 29 partial-occupancy records belong to water. Their combined total is 57, but that total should not be described as 57 protein atoms. Keeping the categories separate locates the structural feature that deserves closer attention.

### Terminal features in the experimental structure

Minimum atomic occupancy and mean heavy-atom B factor per residue, calculated from the original 1UBQ records. Shading identifies residues 73–76.

GROMACS 2026.4; chain A of PDB 1UBQ, 76 residues; AMBER99SB-ILDN with TIP3P. All 602 experimental heavy atoms are retained and 629 hydrogen atoms added. His68 uses neutral NE2 protonation, with charged free termini.

[Download reference data and complete inputs (ZIP) 0.09 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-protein-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g05/en/#en-s4)

Minimum heavy-atom occupancy and mean heavy-atom B factor for each residue of PDB 1UBQ. Shading marks residues 73–76. Occupancy describes site occupation in the experimental structural model; B factors describe positional spread in the diffraction model. These quantities offer different clues about the terminal region.

The plotted occupancies show that partial occupancy is concentrated at the C-terminal end of the chain, where the mean B factor also rises. The upper panel reports the minimum atomic occupancy within each residue. The lower panel reports the arithmetic mean of the heavy-atom B factors in that residue. The two summaries serve different purposes: the minimum makes a local partial occupancy visible, while the mean supports comparison of the overall refinement parameters along the chain. We retain the terminal atoms in the model and carry this observation into later analysis. When examining terminal motion in solution, we will distinguish the experimental disorder information from the displacement measured in our trajectory.

A crystallographic B-factor profile and a molecular-dynamics RMSF profile are different measurements. The former comes from a diffraction model and depends on the crystal environment, static disorder, and refinement; the latter is calculated from atomic positions in a chosen trajectory, using a specified alignment and time window. They can motivate a shared question about local flexibility, provided those definitions are retained. Partial occupancy also does not become a fractional atomic mass in our simulation. We model one complete ubiquitin molecule, using the masses specified by its chemical force-field definition. Occupancy helps interpret the experimental representation of a position; it does not instruct the simulation to remove a fraction of that atom.

## Choosing what to retain defines the object being studied

A short preparation command sometimes removes every HETATM record from a structure. Before using such a rule, identify the actual components. HETATM is a record category that can contain water, ions, organic ligands, cofactors, or modified residues. In some proteins, a metal ion or a cofactor is central to the biological function, so removing it changes the object under investigation. The composition of 1UBQ is relatively straightforward: chain A contains the complete ubiquitin molecule, and the other atom records describe 58 water oxygens. For our model of free ubiquitin in solution, we retain all 602 heavy atoms of chain A and construct a new bulk-water environment in the next chapter.

Crystallographic water and bulk solvent are not chemically different categories of water. Crystallographic waters are molecules whose positions were modelled and recorded from the experiment; the bulk solvent is the much larger collection surrounding the protein in the simulation. Retaining a particular experimental water may supply a useful initial occupancy for a binding pocket, but that water still requires hydrogen placement, a water model, and checks for overlaps with other components. Here, replacing the recorded waters with a newly constructed solvent bath is a defined initial-condition choice. A study of a specific pocket water would instead examine its structural evidence and compare appropriate retained-water or alternative initial configurations.

Completeness also has a geometric and a chemical meaning. Finding residue numbers 1 through 76 shows that no entire residue is absent from this coordinate sequence. Checking whether each residue has all required side-chain heavy atoms is a further task. A lysine with an intact backbone but a missing terminal nitrogen would still have an important chemical omission. The pdb2gmx program compares residues with templates in the chosen force field and can add hydrogens using the corresponding rules. Missing heavy atoms or internal residues require suitable structural modelling and inspection beforehand. A hydrogen-placement rule contains local geometric information; it does not specify the arbitrary three-dimensional conformation of a missing protein loop.

Adjacent Cα distances, continuous residue numbering, and successful residue-template matching provide complementary checks in this example. We also preserve a correspondence between original atom identities and generated coordinates. GROMACS reorders atoms according to force-field conventions, and some names change. Here, isoleucine CD1 is named CD, while the two C-terminal oxygens are named OC1 and OC2. Subtracting rows in two files without matching their identities would mistake a change of order for molecular movement. The correct comparison first pairs atoms by residue and chemical site, applies the necessary naming correspondence, and then converts units before subtracting coordinates. Comparing address books by person rather than by row number follows the same logic.

All 602 heavy atoms have counterparts in the generated model. The largest coordinate difference after matching is approximately 0.000866 nm, consistent with the three decimal places used to write coordinates in this GRO file. Each Cartesian component can acquire a rounding difference of about 0.0005 nm, so the three-dimensional difference can approach the square root of three such squared differences. This check shows that the conversion preserved the heavy-atom geometry while adding hydrogens and applying naming conventions. Coordinates will subsequently move during energy minimization in response to the model potential. Separating file conversion from geometric relaxation gives the structural changes at each stage a specific, inspectable cause.

## Choose hydrogen positions, terminal groups, and charges

Hydrogen atoms are light and are often difficult to locate individually in conventional protein X-ray structures, yet their chemical role is substantial. Whether a nitrogen carries a hydrogen changes its hydrogen-bonding behaviour. Whether a carboxyl group has lost a proton changes its charge. Adding hydrogens therefore has two parts: choosing a chemical state and placing hydrogen atoms using the geometry appropriate to that state. Protonation state refers to where the relevant protons are present or absent. Solution acidity and the local molecular environment both influence those states, while heavy-atom coordinates commonly provide only part of the information needed to select them. A preparation program must implement an explicit choice.

Residue 68 in ubiquitin is histidine, whose side chain contains a five-membered imidazole ring. Two nitrogen sites in that ring are named ND1 and NE2. The letters and numbers identify positions in an atom-naming convention; they are not electric charges. Neutral histidine can carry its ring proton on ND1 or on NE2. These two tautomers have the same total charge but different arrangements of hydrogen-bond donors and acceptors. Protonating both nitrogen sites generally gives a positively charged side chain. Consequently, specifying neutral histidine alone leaves an important detail unresolved: the simulation must also select the tautomer and its corresponding atomic charges and connections.

[Figure: Histidine nitrogen sites and protonation states](https://ml-biomat.com/tutorials/molecular-dynamics/g05/en/#en-s6)

Figure 3 · HID and HIE have the same formal net charge but different proton positions; HIP has a proton on each ring nitrogen and a formal charge of +1 e. This model selects HIE68.

We explicitly choose the neutral state protonated on NE2, called HIE in AMBER terminology. The processed GROMACS residue may be labelled HISE; the decisive atom check is that HE2 is present and HD1 is absent. The pdb2gmx program can also propose a state using geometric hydrogen-bond criteria, but that proposal follows from the supplied structure and the implemented rules. The experimental heavy-atom coordinates do not directly locate this proton. We therefore retain HIE as a fixed modelling choice and record it through the command selection and the resulting topology. A study focused on binding or acid–base behaviour near His68 could construct another plausible state and compare it under otherwise matched conditions.

Choose a histidine state and follow the ring proton positions and formal side-chain charge.

[Figure: Histidine ring proton positions](https://ml-biomat.com/tutorials/molecular-dynamics/g05/en/#en-s6)

Histidine-state illustration; changing the state changes the hydrogen positions and partial charges required in the topology.

The two chain ends also need chemical definitions. Our free ubiquitin model uses a positively charged amino terminus on Met1 and a negatively charged carboxyl terminus on Gly76. An internal peptide bond and a free terminal group have different connections, so the hydrogen count and charges of an internal residue cannot simply be copied to an end. The original PDB already contains both C-terminal oxygens, which the force-field templates assign to the terminal carboxylate. If the same terminus is later connected to another molecule, the topology must describe that new connectivity, the appropriate removed atoms, and the revised charge distribution. Changing biological context can therefore change chemistry even when most coordinates initially look similar.

Net charge from atomic partial chargesEq. 2

![Net charge from atomic partial charges](https://ml-biomat.com/static/agent-math/40b8f735ba087efc6ef1863c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Q | Net charge of the selected molecule | e (elementary-charge units) |
| qᵢ | Partial charge of atom i in the topology | e |
| N | Number of atoms in the selected molecule; 1231 here | 1 (dimensionless) |
| i, 1 | Summation index i starts at atom 1 | 1 (dimensionless) |
| Σ, = | Σ adds charges from atom 1 through atom N; the equals sign states equality | 1 (dimensionless) |

Reading the relationshipCharge is additive. Individual partial charges may be fractional, while their molecular sum must agree with the chosen chemical state. Spatially separated positive and negative sites still produce local electrostatic interactions when the net charge is zero.

A worked exampleCharges of −0.4 e, +0.2 e, and +0.2 e sum to 0 e. The actual 1231-atom protein topology sums to approximately 3×10⁻¹⁵ e, which is zero to floating-point precision.

ConditionsThe sum includes the atoms of the specified molecule. This model uses fixed protonation states and partial charges; changing chemical states or covalent connections requires the corresponding topology.

Net charge is obtained by summing atomic partial charges. Zero net charge does not mean that the molecular surface has no electric field. This sequence contains seven lysines and four arginines, balanced in formal charge by five aspartates and six glutamates under our choices. The charged free termini also balance, and His68 is neutral. Summing the partial charges of all 1231 protein atoms in the generated topology gives approximately zero; the tiny remaining numerical value is floating-point roundoff. Positive and negative charges nevertheless occupy different locations. Water and ions respond to those local patterns. In the next chapter, electrical neutrality and salt concentration will consequently be checked as two separate properties of the complete solution model.

## A complete example: inspect the structure and generate the topology

The program below turns these questions into repeatable inspections. It reads fixed-column PDB records, explicitly selects the protein atoms of chain A, and counts residues, waters, partial occupancies, and adjacent Cα distances. Because this worked example uses 1UBQ, the program checks for its 602 protein heavy atoms, 76 continuous residues, and 58 water oxygens. A different structure requires a correspondingly different selection and inspection policy. These expectations keep the computational object clearly defined. The program then writes a residue-by-residue table and the selected protein coordinate file, while generating the occupancy and B-factor plot from the same parsed records. Supplying the generated GRO and topology additionally enables the atom-identity comparison.

### Read the structure, summarize residues, and check the generated model

```
"""Inspect 1UBQ records and, optionally, its generated protein model."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def read_pdb(path):
    atoms = []
    for line in path.read_text(encoding="utf-8").splitlines():
        record = line[:6].strip()
        if record not in {"ATOM", "HETATM"}:
            continue
        atoms.append(dict(record=record, name=line[12:16].strip(),
                          altloc=line[16].strip(), resname=line[17:20].strip(),
                          chain=line[21], resid=int(line[22:26]),
                          insertion=line[26].strip(),
                          xyz_A=[float(line[i:i+8]) for i in (30, 38, 46)],
                          occupancy=float(line[54:60]), b_A2=float(line[60:66]),
                          element=line[76:78].strip(), line=line))
    return atoms


def protein_topology_atoms(path):
    rows, section = [], ""
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split(";", 1)[0].strip()
        if line.startswith("["):
            if section == "atoms" and rows:
                break
            section = line.strip("[] ")
        elif section == "atoms" and line and not line.startswith("#"):
            parts = line.split()
            rows.append(dict(index=int(parts[0]), resid=int(parts[2]),
                             resname=parts[3], name=parts[4],
                             charge_e=float(parts[6]), mass_u=float(parts[7])))
    if not rows:
        raise ValueError("The input topology must contain the explicit protein [ atoms ] block.")
    return rows


def read_gro(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    count = int(lines[1])
    return [dict(resid=int(line[:5]), name=line[10:15].strip(),
                 xyz_nm=[float(line[i:i+8]) for i in (20, 28, 36)])
            for line in lines[2:2+count]]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdb", type=Path)
    parser.add_argument("--gro", type=Path)
    parser.add_argument("--topology", type=Path)
    parser.add_argument("--output", type=Path, default=Path("inspection"))
    parser.add_argument("--language", choices=("zh", "en"), default="en")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    atoms = read_pdb(args.pdb)
    protein = [a for a in atoms if a["record"] == "ATOM" and a["chain"] == "A"]
    waters = [a for a in atoms if a["resname"] == "HOH"]
    if len(protein) != 602 or len(waters) != 58:
        raise ValueError("This worked example expects the original 1UBQ: 602 protein atoms and 58 HOH oxygens.")
    if any(a["altloc"] or a["insertion"] for a in protein):
        raise ValueError("Resolve alternative positions or insertion codes explicitly before selection.")
    residues = sorted({a["resid"] for a in protein})
    if residues != list(range(1, 77)):
        raise ValueError("The example requires the continuous chain A, residues 1 to 76.")
    (args.output / "protein.pdb").write_text(
        "\n".join(a["line"] for a in protein) + "\nTER\nEND\n", encoding="utf-8")
    rows = []
    for resid in residues:
        selected = [a for a in protein if a["resid"] == resid]
        rows.append(dict(resid=resid, resname=selected[0]["resname"],
                         heavy_atoms=len(selected),
                         occupancy_min=min(a["occupancy"] for a in selected),
                         b_mean_A2=float(np.mean([a["b_A2"] for a in selected]))))
    with (args.output / "residue_inventory.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    ca = np.array([a["xyz_A"] for a in protein if a["name"] == "CA"], float)
    ca_steps = np.linalg.norm(np.diff(ca, axis=0), axis=1)
    summary = dict(pdb_id="1UBQ", source_sha256=hashlib.sha256(args.pdb.read_bytes()).hexdigest(),
                   protein_heavy_atoms=len(protein), residues=len(residues),
                   crystal_water_oxygens=len(waters), alternative_atom_positions=0,
                   protein_atoms_occupancy_below_one=sum(a["occupancy"] < 1 for a in protein),
                   water_atoms_occupancy_below_one=sum(a["occupancy"] < 1 for a in waters),
                   adjacent_CA_distance_min_A=float(ca_steps.min()),
                   adjacent_CA_distance_max_A=float(ca_steps.max()),
                   sequence_counts=dict(Counter(row["resname"] for row in rows)))
    if bool(args.gro) != bool(args.topology):
        raise ValueError("Supply --gro and --topology together for the generated-model comparison.")
    if args.gro:
        gro, top = read_gro(args.gro), protein_topology_atoms(args.topology)
        if len(gro) != len(top):
            raise ValueError("The GRO and explicit protein topology must contain the same atoms.")
        names = {(a["resid"], a["name"]): a for a in gro}
        errors = []
        for atom in protein:
            name = atom["name"]
            if atom["resname"] == "ILE" and name == "CD1":
                name = "CD"
            if atom["resid"] == 76:
                # The terminal carboxylate oxygens were reordered in this model.
                name = {"O": "OC2", "OXT": "OC1"}.get(name, name)
            generated = names[(atom["resid"], name)]
            errors.append(np.linalg.norm(np.array(atom["xyz_A"])/10 - generated["xyz_nm"]))
        his_names = sorted(a["name"] for a in top if a["resid"] == 68)
        summary["generated_model"] = dict(
            protein_atoms=len(top), hydrogen_atoms=sum(a["mass_u"] < 2 for a in top),
            heavy_atoms_retained=len(errors),
            max_heavy_coordinate_rounding_nm=float(max(errors)),
            total_charge_e=float(sum(a["charge_e"] for a in top)),
            his68_has_HE2="HE2" in his_names, his68_has_HD1="HD1" in his_names,
            n_terminal_atoms=[a["name"] for a in top if a["resid"] == 1],
            c_terminal_atoms=[a["name"] for a in top if a["resid"] == 76])
    (args.output / "inventory.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    zh = args.language == "zh"
    plt.rcParams.update({"font.family": ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"],
                         "font.size": 14, "svg.fonttype": "path",
                         "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True, constrained_layout=True)
    x = [r["resid"] for r in rows]
    axes[0].plot(x, [r["occupancy_min"] for r in rows], color="#137b88", lw=2.2)
    axes[0].set_ylabel("残基最小原子占据率" if zh else "Minimum atom occupancy")
    axes[0].set_ylim(0, 1.06)
    axes[1].plot(x, [r["b_mean_A2"] for r in rows], color="#b16b36", lw=2.2)
    axes[1].set_ylabel("平均B因子 / Å²" if zh else "Mean B factor / Å²")
    axes[1].set_xlabel("残基编号" if zh else "Residue number")
    axes[1].set_xlim(1, 76)
    for ax in axes:
        ax.axvspan(72.5, 76, color="#d7bb8d", alpha=.18)
        ax.grid(axis="y", color="#d7dfdd", alpha=.65)
    fig.suptitle("1UBQ：实验结构的局部信息" if zh else "1UBQ: local information in the experimental structure", fontsize=18)
    fig.savefig(args.output / "pdb_inventory.svg")
    fig.savefig(args.output / "pdb_inventory.png", dpi=160)
    plt.close(fig)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

Reads fixed-column 1UBQ records and writes the protein selection, residue table, and plot. With GRO and TOP inputs, checks atom identities, charge, and heavy-atom geometry. Requires NumPy and Matplotlib.

The variable names xyz_A and xyz_nm retain the coordinate units. Before comparing heavy atoms, the original ångström coordinates are divided by ten and subtracted from the GRO coordinates in nanometres. The resulting difference is consequently in nanometres too. A dictionary indexed by residue number and atom name establishes correspondence without assuming that row order is preserved. The isoleucine and terminal-oxygen naming rules are written explicitly to connect the same chemical sites. This input contains neither alternative positions nor insertion codes, so the program requests explicit handling if such records appear. It does not quietly choose whichever record happens to occur first. These details make the selection rules visible in the computation.

The model-generation command selects the amber99sb-ildn force field and TIP3P water. The force-field name selects the protein residue templates and interaction parameters; the water option determines how subsequently added water molecules are interpreted in the topology. Bulk water is not present at this stage, but its compatible molecular definition is already selected. The -his option requests an explicit histidine choice. In the GROMACS 2026.4 menu for this force field, option 1 selects the neutral NE2-protonated state. With another version or template family, read the actual menu and inspect the generated atom names before using a selection number. A menu index is a software choice, while HIE specifies the intended chemical state.

### Generate the protein model with explicit HIE68

```
#!/usr/bin/env bash
set -euo pipefail

# Run beside the supplied 1UBQ.pdb and inspect_pdb.py.
python inspect_pdb.py 1UBQ.pdb --output inspection --language en
cp inspection/protein.pdb protein.pdb

# In GROMACS 2026.4 with amber99sb-ildn, option 1 places His68 H on NE2.
printf '1\n' | gmx pdb2gmx -f protein.pdb -o processed.gro \
    -p topol.top -i posre.itp -ff amber99sb-ildn -water tip3p -his

python inspect_pdb.py 1UBQ.pdb --gro processed.gro --topology topol.top \
    --output inspection --language en
```

Run beside 1UBQ.pdb and inspect_pdb.py. Menu option 1 selects NE2 protonation for this GROMACS 2026.4/AMBER99SB-ILDN setup; inspect the resulting hydrogen names.

The pdb2gmx command produces three main outputs. The processed.gro file contains the reordered coordinates with hydrogens. The topol.top file contains protein connectivity, atomic charges and types, and force-field references. The posre.itp file specifies position restraints that can be activated during later equilibration. Generating that restraint file does not automatically keep the protein fixed throughout every subsequent simulation; activation depends on the options used when preparing a run. At this stage, no dynamical trajectory has been generated and no equilibration in solution has occurred. The completed object is an initial chemical model with matching coordinates and topology, ready for construction of its environment and subsequent geometric relaxation.

### Atom counts and chemical state of the generated model

Free ubiquitin generated with GROMACS 2026.4 and AMBER99SB-ILDN, with neutral NE2-protonated His68 and oppositely charged free termini.

| Quantity | Value | Unit |
| --- | --- | --- |
| Retained protein heavy atoms | 602 | 1 |
| Generated protein hydrogen atoms | 629 | 1 |
| Total protein atoms | 1231 | 1 |
| Protein residues | 76 | 1 |
| Net charge of the selected chemical state | 0 | e |
| Maximum coordinate difference for matched heavy atoms | 0.000866025 | nm |

The actual processing yields 1231 protein atoms: 602 retained heavy atoms and 629 added hydrogens, with the residue count still equal to 76. His68 contains HE2 and lacks HD1; the N terminus contains H1, H2, and H3; the C terminus contains two carboxylate oxygens. Each observation corresponds to a chemical choice explained above. Net charge and the matched heavy-atom coordinate difference add two further, independent checks. The useful habit is to follow the identity of the input object into the output: additional atoms, changed names, and information in new files should have identifiable chemical or format-related reasons. A successful command is then accompanied by a structural interpretation of what it produced.

## Connect the prepared model to a scientific question

We now have a ubiquitin chain whose chemical definition and coordinates correspond. It retains the experimental fold, includes the hydrogens required by the selected all-atom force field, and explicitly uses HIE68 and charged free termini. This is a starting point for studying structural persistence, terminal motion, and local conformational fluctuations in water. It also defines the reference for later comparisons. A salt-concentration comparison can retain the same protein topology while changing the solution composition. A histidine-state comparison instead treats the chemical state as an explicit change. Keeping these choices separate makes differences in subsequent measurements easier to interpret, because a preparation change is not hidden inside an unrelated set of commands.

Three connected questions provide a useful direction. Does the folded body retain a similar overall shape during the observation period? Does the projecting tail fluctuate more than particular regions of the body? Do trajectories started with different velocities show consistent features in those measurements? The first question calls for structural alignment and coordinate comparisons. The second requires a definition of local fluctuation. The third requires independent simulations and statistical reasoning. Each is more specific than observing that an animation moves, and all can be developed using the same molecule. Clear questions guide practical decisions about saved frames, selected atoms, observation windows, and which results deserve comparison.

The question can also be used to assess what must be added to the model. Recognition by the proteasome calls for the appropriate binding partners and environment. Formation of a covalent linkage calls for a model capable of describing the relevant chemical transformation. The conformational distribution of a free ubiquitin tail in water, in contrast, can begin with the chemical system prepared here, followed by appropriate equilibration, sampling, and analysis. This way of reading model scope turns an additional requirement into a concrete modelling task. System composition and calculation method follow the process being investigated, while the current example keeps the relation between them small enough to inspect directly.

Look again at the occupancy and B-factor panels, then locate the terminal segment in the structural view. The experimental records identify a region with a less sharply defined crystallographic representation. Molecular dynamics will provide positions changing with time in a specified solution model. We will first surround the protein with water and salt, creating an environment that exchanges momentum and energy with it. Energy minimization will address unfavourable initial contacts, followed by equilibration with clearly specified position restraints and their later removal. Each operation connects the computational molecule to the intended solution conditions, so that an experimental conformation becomes an interpretable starting point for dynamics.

The dense letters and numbers in a structure file now have distinct roles. Residue sequence specifies chemical order, coordinates specify an initial conformation, occupancy and B factors help interpret the experimental model, and force-field templates supply connectivity and interactions. Programmatic checks confirm that these descriptions refer to the same molecule after conversion. The next chapter builds on this preparation by defining a simulation cell, adding water and ions, and checking the composition of the complete system. Ubiquitin will then occupy a solution model with a defined volume and concentration, allowing the structural questions developed here to be asked under explicit physical conditions.

## Further Reading and Open Materials

- [Introduction to Molecular Dynamics](https://tutorials.gromacs.org/docs/md-intro-tutorial.html) · Cathrine Bergh; Maryam Majdolhosseini; Alessandra Villa · CC BY 4.0

  Structure-inspection and topology-generation workflow.

  Uses 1UBQ and AMBER99SB-ILDN/TIP3P, explicit HIE68/termini, atom-correspondence checks, and bilingual explanations.
- [From Proteins to Perturbed Hamiltonians: A Suite of Tutorials for the GROMACS-2018 Molecular Simulation Package](https://github.com/jalemkul/gmx_tutorials_livecoms) · Justin A. Lemkul · CC BY 4.0

  Structure-to-topology workflow and molecular-simulation teaching context.

  Uses ubiquitin as a continuous example and adds experimental-record, chemical-state, and count checks.
- [1UBQ: Structure of ubiquitin refined at 1.8 Å resolution](https://www.rcsb.org/structure/1UBQ) · S. Vijay-Kumar; C. E. Bugg; W. J. Cook · PDB archive data: CC0; associated publication retains its own terms

  Actual coordinates, occupancies, and B factors.

  Replotted structural data, selected chain A, and summarized local records; original data supplied separately.
- [gmx pdb2gmx—GROMACS 2026.4](https://manual.gromacs.org/2026.4/onlinehelp/gmx-pdb2gmx.html) · GROMACS developers · GROMACS documentation terms; factual reference

  Residue templates, hydrogen addition, histidine options, and termini.

  Original explanation of the commands used here.
- [1958: Fred Sanger](https://mrclmb.ac.uk/achievements/awards-and-prizes/nobel-prizes/1958-fred-sanger/) · MRC Laboratory of Molecular Biology · Publicly readable historical reference; no image/text reproduction

  Historical facts about insulin sequencing.

  Rewritten historical discussion with a conceptual diagram.
- [A Three-Dimensional Model of the Myoglobin Molecule Obtained by X-Ray Analysis](https://www.nature.com/articles/181662a0) · J. C. Kendrew and colleagues · Publisher copyright; factual citation

  The 1958 myoglobin model and structural hierarchy.

  Historical discussion with a conceptual illustration.
- [Ubiquitin at Fox Chase](https://pmc.ncbi.nlm.nih.gov/articles/PMC1187975/) · Irwin A. Rose · Nobel Foundation copyright; publicly readable, factual citation

  Historical questions about ubiquitin conjugation and protein degradation.

  Factual summary and conceptual molecular-attachment diagram.
