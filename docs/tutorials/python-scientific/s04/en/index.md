# From Molecular Strings to Chemical Structure Tables

Source: https://ml-biomat.com/tutorials/python-scientific/s04/en/
Language: en

Trace atoms, verify masses, and distinguish text, stereochemistry, and molecular identity with RDKit.

## A molecular table starts with knowing what each row represents

A materials spreadsheet may contain a compound name, a structural string, a molecular mass, and an experiment identifier. It resembles an ordinary data-cleaning task, but several different questions are hidden inside the structure column. One molecule can have several valid strings. Two substances with the same molecular formula can have different connectivity. Even when connectivity is identical, spatial configuration can distinguish the compounds. Deduplicating the strings directly can therefore retain duplicate structures or merge records that deserve separate analysis. This chapter uses RDKit to turn strings into molecular graphs and then into an inspectable table. You will follow individual atoms and their neighbors, check formulas and masses, locate functional groups, and explain exactly why a particular comparison rule merges two records.

Two complementary sets of examples make these distinctions tangible. The first is a series of hydroxyl-terminated ethylene-glycol molecules, beginning with ethylene glycol and extending to six ethylene-glycol units. Each added unit changes the carbon, hydrogen, and oxygen counts in a predictable way, providing a useful independent check on calculated mass. The second set contains two specified configurations of lactic acid, lactic acid with unspecified configuration, lactate, and two representations of benzene. Together, these separate different spelling, different composition, and different structural information. All property values in this example are calculated from explicitly defined molecular graphs. When experimental properties are added, temperature, solvent, concentration, and measurement method belong in their own columns.

An RDKit `Mol` is rather like a molecular connection register. It records the atoms, the bonds connecting them, the bond types, and attributes such as charge and stereochemistry. A two-dimensional chemical drawing is one arrangement of that register; SMILES is a textual representation; CSV stores scalar information extracted from it. Understanding these relationships gives the functions a common purpose: read the graph, inspect it, describe it, and associate the result with the original record.

## Reading SMILES: branches, rings, and omitted hydrogens

Consider `CC(O)C(=O)O` as instructions for walking through a molecular graph. The first `C` creates a carbon atom, and the second creates another carbon bonded to it. The `O` inside parentheses creates a branch from the current, second carbon. Closing the parentheses returns the walk to the main path. The next `C` creates another carbon; `(=O)` attaches an oxygen through a double bond; the final `O` attaches through a single bond. Six element tokens create six non-hydrogen atoms. Parentheses control the walk, while the equals sign specifies a bond type. The atom indices in the figure begin at zero and allow the reading order to be checked directly.

Hydrogens still belong to the molecule even when they are omitted from the drawing. For the ordinary neutral carbon and oxygen environments used here, RDKit determines hydrogen counts from the element, existing bonds, and valence rules. The first carbon has one single bond to carbon and carries three hydrogens. The second has three single bonds and carries one hydrogen. The carbonyl carbon has two single bonds and one double bond, leaving no attached hydrogen. Each hydroxyl oxygen carries one hydrogen; the carbonyl oxygen carries none. The total gives C₃H₆O₃. Accordingly, `GetNumHeavyAtoms()` returns 6, while `Chem.AddHs(mol).GetNumAtoms()` returns 12. The first counts non-hydrogen atoms; the second counts all nodes after hydrogens have been added explicitly to the graph.

![Follow one lactic-acid graph through SMILES branches, atom indices, hydrogen counts, and canonicalization; the 1988 line-notation idea becomes an inspectable connection register.](https://ml-biomat.com/static/tutorials/python-scientific/figures/df2eb1e83facecc7a8b1478c.svg?v=df2eb1e83fac)

Figure 1Follow one lactic-acid graph through SMILES branches, atom indices, hydrogen counts, and canonicalization; the 1988 line-notation idea becomes an inspectable connection register.

David Weininger’s 1988 SMILES paper described encoding molecular connectivity in a line of text that computers could handle. This made a chemical structure suitable for storage, transmission, and searching alongside other kinds of data. The figure connects that historical problem to a present-day parsing operation. Starting elsewhere in lactic acid and walking through the same connections can produce `OC(=O)C(O)C`. A canonicalization algorithm chooses a consistent output order for the graph attributes that have been retained, so these two inputs produce the same canonical SMILES in this example. Atom indices, however, depend on the order in which the current object was constructed. Matching atoms across independent records requires an atom correspondence, rather than assuming that “atom 3” refers to the same chemical position in both.

Ring notation also describes connectivity. In benzene’s `c1ccccc1`, lowercase `c` denotes aromatic carbon, and the two occurrences of 1 request a closing bond between the corresponding positions. The digit does not create an additional atom. The alternative input `C1=CC=CC=C1` initially specifies alternating single and double bonds. During chemical checking, RDKit recognizes the aromatic system and produces `c1ccccc1` as the canonical output. Aromaticity is assigned through rules applied to the molecular graph; it is not determined by whether a drawing uses a circle or alternating double lines. More complex fused rings, coordination compounds, and unusual valences require attention to the relevant aromaticity and valence models. Familiar organic molecules provide a clear starting point for these operations.

The connection register can also be represented as a matrix. Its rows and columns use the same atom indices: enter 1 when a bond exists and 0 otherwise. Row 1 of the lactic-acid matrix contains ones in columns 0, 2, and 3, corresponding to that carbon’s three heavy-atom neighbors. An ordinary covalent bond connects both endpoints, so this adjacency matrix is symmetric. With no self-bonds, its diagonal is zero. Summing the row gives three heavy-atom neighbors; hydrogens remain in the atom attributes, so this sum does not give the carbon’s complete valence. A bond-order matrix or the bond objects themselves can distinguish single and double bonds. The page begins with binary adjacency so that every colored cell can be followed back to an edge in the molecular drawing.

## From an input record to a traceable structure table

`Chem.MolFromSmiles()` does more than separate a string into characters. It constructs atoms and bonds and performs chemical checks, including valence and aromaticity handling. The example deliberately includes `C(C)(C)(C)(C)C`. Its central carbon has five single bonds without a charge annotation, violating the neutral-carbon valence rule applicable here, so parsing returns `None`. Immediately applying a mass function would move the failure away from the original input. A clearer approach checks the parsing result at once and retains the identifier, original string, and reason in the same row. Thirteen input rows consequently yield twelve valid structures and one explicitly identified record to correct; the table does not silently lose an observation.

A useful structure table retains three different kinds of information: the source record identifier, the original representation, and the representation generated by the software. The identifier connects to experimental records, the original string supports input inspection, and the canonical representation supports comparison under a stated rule. Because these roles differ, canonicalization does not replace the original string. The example CSV also includes formula, average molar mass, monoisotopic mass, atom counts, formal charge, and several structural descriptors. Column names such as `mass_g_mol` and `tpsa_A2` retain units when the results are joined or plotted in pandas.

CSV is convenient for a scalar table, while SDF can preserve atoms, bonds, two-dimensional coordinates, and molecular properties. The program writes the valid molecules to SDF, reads the file back, and compares each recovered canonical isomeric SMILES with its pre-write value. This is analogous to unpacking a shipment and checking its contents. A file’s existence establishes that bytes were written; the structural round trip checks that the connectivity and specified configurations of interest survived. The coordinates here are generated for a two-dimensional depiction. A longer drawn bond does not establish a longer physical bond. Investigating conformations or molecular energies requires a separate three-dimensional model and the corresponding computational method.

Successful parsing and correct identification of the intended substance are separate checks. A string with a bond attached at the wrong position may obey all valence rules and successfully describe a different molecule. When introducing a dataset, draw representative records and compare their functional groups, end groups, and charges with the intended structures. The formula-mass check can expose a missing atom, but compounds with the same molecular formula can still have different connectivity. Substructure matching examines that local connectivity, while stereochemical attributes add information about spatial configuration. These checks complement one another because each answers a specific question; a disagreement can then be located at the appropriate structural level.

## Check automatic descriptors with a mass you can calculate by hand

A descriptor compresses one aspect of a molecular graph into a number. Average molar mass is particularly convenient to check: count the atoms of each element, multiply by the corresponding atomic weight, and sum. This chapter uses the average atomic-weight convention in RDKit, with carbon, hydrogen, and oxygen contributing approximately 12.011, 1.008, and 15.999 to a molar mass expressed in g/mol. For ethylene glycol, C₂H₆O₂, the two carbons contribute 24.022, the six hydrogens contribute 6.048, and the two oxygens contribute 31.998. Their sum is 62.068 g/mol. The program checks all six series members against this independent formula calculation.

$$
M=\sum_e N_e A_e,\qquad M(n)=(44.053n+18.015)\ \mathrm{g\,mol^{-1}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/34058a2a5d1de088feed7d98.svg) | Average molar mass of the specified molecule, g/mol |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | Index identifying an element, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/2244f89c20614334f7d67053.svg) | Number of atoms of element e in one molecule, dimensionless integer |
| ![Formula](https://ml-biomat.com/static/agent-math/db201892debabce52fc649b2.svg) | Molar contribution associated with the average atomic weight of element e, g/mol |
| ![Formula](https://ml-biomat.com/static/agent-math/acf5fc4aba87dc0808b830d5.svg) | Sum over the contributions from all elements present |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Number of repeated units in HO–(CH₂CH₂O)ₙ–H, 1–6 here, dimensionless |

Each repeated C₂H₄O unit contributes 2×12.011+4×1.008+15.999=44.053 g/mol. The H₂O end-group remainder contributes 18.015 g/mol. For n=3, the formula is C₆H₁₄O₄ and M=3×44.053+18.015=150.174 g/mol, checked against RDKit. This counts a defined molecule rather than averaging a chain-length distribution.

The end groups must be included. In HO–(CH₂CH₂O)ₙ–H, the repeated portion contributes n copies of C₂H₄O, and the two ends together contribute an additional H₂O in the atom count. The full formula is therefore C₂ₙH₄ₙ₊₂Oₙ₊₁. This H₂O term is a bookkeeping remainder for the terminal atoms; it does not mean that a water molecule is mixed into the sample or identify a particular synthesis route. Adding one unit increases molar mass by 44.053 g/mol. From n = 1 to n = 6, the mass rises from 62.068 to 282.333 g/mol. Every point represents a specific molecule. A commercial polyethylene-glycol sample commonly contains a chain-length distribution, whose number-average or weight-average molar mass requires the corresponding molecular counts or mass fractions.

`ExactMolWt` and `MolWt` have different definitions. The former generally uses specified isotopes or the most abundant isotope of each element and returns monoisotopic mass, expressed in Da. The latter uses average atomic weights. Ethylene glycol consequently gives 62.036779432 Da and 62.068 g/mol here; their numerical difference follows from those definitions. A mass-spectrometry peak additionally depends on the ion, any adduct, and charge state. Keeping both columns provides explicit starting quantities for the subsequent calculation.

![Six molecules with defined end groups, with separate axes and units for each descriptor. Orange crosses show formula-derived mass; terminal donor count stays constant while internal ether oxygens add acceptor sites.](https://ml-biomat.com/static/tutorials/python-scientific/figures/e06bb2b68a6797f57b76c96a.svg?v=e06bb2b68a67)

Figure 2Six molecules with defined end groups, with separate axes and units for each descriptor. Orange crosses show formula-derived mass; terminal donor count stays constant while internal ether oxygens add acceptor sites.

The other descriptors reveal different aspects of the same molecular series. Hydrogen-bond donors, HBD, count sites capable of donating an appropriate hydrogen. Each molecule retains two terminal hydroxyl groups, so its donor count remains 2. Hydrogen-bond acceptors, HBA, follow chemical rules for atom environments that can accept a hydrogen bond. The additional internal ether oxygens raise this count from 2 to 7. These are site counts, rather than the number of hydrogen bonds actually present at a particular instant in water. Topological polar surface area, TPSA, sums contributions associated with polar atom environments and has units of Å². It rises from 40.46 to 86.61 Å² across the series. It is calculated from structural environments without requiring a three-dimensional conformation, and its definition differs from directly measuring the area of a particular molecular surface.

## Equal mass still leaves configuration, charge, and grouping to examine

The central carbon of lactic acid connects to four different groups, allowing two mirror-related spatial configurations. Left and right gloves provide a useful analogy: their components and overall arrangement resemble one another, but translation and rotation alone cannot make them coincide. The SMILES markers `@` and `@@` describe this distinction relative to the local neighbor order. They cannot be translated into R and S independently of the surrounding string. RDKit assigns the CIP configurations in this example: `C[C@H](O)C(=O)O` gives S, while the other specified input gives R. Wedge bonds in the drawing convey the spatial orientation; the remaining lines show connectivity in the plane.

![Lactic-acid configuration, protonation state, and two benzene inputs illustrate different layers of structural information. Table entries count distinct comparison keys under each rule.](https://ml-biomat.com/static/tutorials/python-scientific/figures/9a3c713ddba9eefdb2729421.svg?v=9a3c713ddba9)

Figure 3Lactic-acid configuration, protonation state, and two benzene inputs illustrate different layers of structural information. Table entries count distinct comparison keys under each rule.

The two specified configurations have identical formulas and molar masses. Their HBD, HBA, TPSA, and fragment logP values in this chapter are also identical. Using these numerical columns as a structural identifier would therefore merge them. Canonical SMILES with stereochemistry retained distinguishes them. The third lactic-acid record, with configuration unspecified, remains separate as well: an unfilled stereochemical field describes missing information, rather than automatically describing an equal mixture of the two configurations. When the research question intentionally compares connectivity alone, `isomericSmiles=False` supplies an explicit alternative key. The choice should remain attached to the resulting table. This option also omits isotope labels. No isotopes are specified in this dataset, so its grouping changes arise entirely from stereochemical information. To retain isotopes while ignoring configuration, copy the molecule, call `Chem.RemoveStereochemistry()`, and then write an isomeric SMILES. The twelve valid records produce eleven isomeric keys and nine keys when stereochemical information is omitted. Benzene’s two inputs merge in both cases; the three lactic-acid records additionally merge under the second rule.

Changing lactic acid into lactate changes both composition and charge. The acidic hydroxyl loses a proton, taking C₃H₆O₃ to C₃H₅O₃⁻. Formal charge changes from 0 to −1, and average molar mass decreases by approximately 1.008 g/mol. HBD falls from 2 to 1, while HBA rises from 2 to 3 because the carboxylic-acid and carboxylate environments follow different recognition rules. Formal charge is an integer assigned by an electron-bookkeeping convention in the graph, distinct from a computed atomic partial charge. When comparing experiments at different pH values, connect the molecular protonation state with the experimental conditions. Canonicalization alone does not select the dominant solution species or decide that salts, tautomers, and different protonation states should all share one record.

Fragment-model logP needs a similarly precise interpretation. Its physical background is the concentration ratio of a neutral solute between octanol and water at equilibrium, expressed as a base-ten logarithm. RDKit’s `MolLogP` estimates this quantity from atom-fragment rules. The glycol series changes from about −1.029 to −0.946 in the calculation, a small numerical change under this model. An axis covering roughly one tenth of a log unit nevertheless produces a visibly rising line, so the axis range matters when interpreting the trend. The program also produces a fragment value for charged lactate. For pH-dependent partitioning, the relative abundance and partitioning of the different species must be included in a quantity such as logD that matches the experimental definition.

$$
P=\frac{c_{\mathrm{oct}}}{c_{\mathrm{water}}},\qquad \log P=\log_{10}P
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | Equilibrium partition coefficient of the neutral solute, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/183d49ffc49fec8f7907e9d8.svg) | Concentration of that neutral solute in octanol, for example mol/L |
| ![Formula](https://ml-biomat.com/static/agent-math/cd4e6f8a69162522cc831012.svg) | Concentration of the same neutral solute in water, in the same units as the numerator |
| ![Formula](https://ml-biomat.com/static/agent-math/be8ebdecd039424afe275a60.svg) | Base-ten logarithm operation |

Equal concentration units cancel. Concentrations of 0.01 and 0.1 mol/L give P=0.1 and logP=−1. RDKit gives a fragment-model value of −1.029 for ethylene glycol, corresponding to 10^(−1.029)≈0.0935. The plotted values use this structural-model definition throughout.

## The complete program: retain records and build the results in layers

The `inputs()` function constructs the six glycol-series structures with a short rule and then adds the identity-comparison group. The main processing stages reside in `process()`: parse the string, check success, generate two-dimensional coordinates and stereochemical labels, traverse the atoms, match substructures, and calculate descriptors. Each atom becomes a dictionary containing its index, element, hydrogen count, charge, neighbors, and assigned R/S label. A list of these dictionaries supports an atom-by-atom table. Whole-molecule descriptors live in the surrounding dictionary and can be written directly to CSV. The program’s hierarchy therefore follows the data hierarchy: a collection contains molecules, and each molecule contains atoms.

Functional-group searches use SMARTS. This notation resembles SMILES but expresses matching rules. Here, `[OX2H]` seeks oxygen with connectivity two and one attached hydrogen. The pattern `[OD2]([#6])[#6]` seeks an oxygen with two explicit neighbors, both carbon, identifying the ether environments in the glycol series. Matches return tuples of atom indices, which can directly highlight the corresponding parts of a drawing. One carboxyl match contains three atoms, so the number of matches and the number of highlighted atoms should be counted separately. The hydroxyl pattern explains why the terminal-group count remains two as the chain grows; switching to the ether pattern follows the internal connections introduced by the added units.

### Complete structure parsing, tabulation, and plotting program

The script reads molecular graphs, retains invalid records, matches functional groups, generates descriptors, and verifies formula masses and an SDF round trip.

```
"""Build molecular identity tables and figures with RDKit.

Run: python main.py --output results --language en
All molecular inputs are defined below; no network service is required.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
from rdkit import Chem, RDLogger, rdBase
from rdkit.Chem import Descriptors, Lipinski, rdDepictor, rdMolDescriptors
from rdkit.Chem.Draw import rdMolDraw2D


BLUE, ORANGE, GREEN, INK = "#235b89", "#bf5635", "#177d72", "#192b3a"
PATTERNS = {
    "hydroxyl": "[OX2H]",
    "ether": "[OD2]([#6])[#6]",
    "carboxyl": "[CX3](=[OX1])[OX2H1,O-]",
    "aromatic": "a",
}



def available_plot_fonts():
    """Choose installed fonts; keep a Latin fallback on every platform."""
    choices = ["Noto Sans CJK SC", "Noto Sans SC", "Microsoft YaHei", "SimHei", "DejaVu Sans"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    return [name for name in choices if name in installed]



def inputs():
    rows = [{"id": f"EG{n}", "smiles": "O" + "CCO" * n, "n": n,
             "zh": f"乙二醇系列 n={n}", "en": f"Glycol series n={n}"}
            for n in range(1, 7)]
    rows.extend([
        {"id": "LA1", "smiles": "C[C@H](O)C(=O)O", "zh": "乳酸：指定构型 1", "en": "Lactic acid: stereo 1"},
        {"id": "LA2", "smiles": "C[C@@H](O)C(=O)O", "zh": "乳酸：指定构型 2", "en": "Lactic acid: stereo 2"},
        {"id": "LA?", "smiles": "CC(O)C(=O)O", "zh": "乳酸：构型未指定", "en": "Lactic acid: unspecified"},
        {"id": "LAC", "smiles": "CC(O)C(=O)[O-]", "zh": "乳酸根：构型未指定", "en": "Lactate: unspecified"},
        {"id": "BZ1", "smiles": "c1ccccc1", "zh": "苯：芳香写法", "en": "Benzene: aromatic input"},
        {"id": "BZ2", "smiles": "C1=CC=CC=C1", "zh": "苯：单双键写法", "en": "Benzene: Kekule input"},
        {"id": "BAD", "smiles": "C(C)(C)(C)(C)C", "zh": "五键中性碳测试", "en": "Neutral five-bond carbon test"},
    ])
    return rows


def depiction(mol, highlight=()):
    drawer = rdMolDraw2D.MolDraw2DSVG(640, 360)
    opt = drawer.drawOptions()
    opt.addAtomIndices = True
    opt.baseFontSize = 0.85
    opt.minFontSize = 20
    opt.maxFontSize = 28
    opt.padding = 0.13
    rdMolDraw2D.PrepareAndDrawMolecule(drawer, mol, highlightAtoms=list(highlight),
                                     highlightAtomColors={i: (0.99, 0.78, 0.36) for i in highlight})
    positions = [[drawer.GetDrawCoords(i).x, drawer.GetDrawCoords(i).y]
                 for i in range(mol.GetNumAtoms())]
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText()
    svg = svg[svg.find("<svg"):]
    return svg, positions


def process(row):
    # Keep a rejected row visible in the output table instead of silently dropping it.
    with rdBase.BlockLogs():
        mol = Chem.MolFromSmiles(row["smiles"])
    if mol is None:
        return {**row, "valid": False, "reason": "invalid neutral carbon valence"}, None
    rdDepictor.Compute2DCoords(mol)
    Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
    atoms = [{"index": a.GetIdx(), "element": a.GetSymbol(),
              "hydrogens": a.GetTotalNumHs(), "charge": a.GetFormalCharge(),
              "aromatic": a.GetIsAromatic(),
              "neighbors": [x.GetIdx() for x in a.GetNeighbors()],
              "cip": a.GetProp("_CIPCode") if a.HasProp("_CIPCode") else None}
             for a in mol.GetAtoms()]
    hits = {name: [list(match) for match in mol.GetSubstructMatches(Chem.MolFromSmarts(pattern))]
            for name, pattern in PATTERNS.items()}
    drawings = {}
    for pattern in ["none", *PATTERNS]:
        indices = sorted({i for match in hits.get(pattern, []) for i in match})
        drawings[pattern], xy = depiction(mol, indices)
    canonical = Chem.MolToSmiles(mol, canonical=True, isomericSmiles=True)
    plain = Chem.MolToSmiles(mol, canonical=True, isomericSmiles=False)
    restored = Chem.MolFromSmiles(canonical)
    assert restored is not None
    assert Chem.MolToSmiles(restored, isomericSmiles=True) == canonical
    result = {**row, "valid": True, "canonical": canonical, "without_stereo": plain,
              "formula": rdMolDescriptors.CalcMolFormula(mol),
              "mass_g_mol": Descriptors.MolWt(mol),
              "monoisotopic_mass_Da": Descriptors.ExactMolWt(mol),
              "heavy_atoms": mol.GetNumHeavyAtoms(),
              "total_atoms_with_H": Chem.AddHs(mol).GetNumAtoms(),
              "formal_charge": Chem.GetFormalCharge(mol),
              "hbd": Lipinski.NumHDonors(mol), "hba": Lipinski.NumHAcceptors(mol),
              "tpsa_A2": rdMolDescriptors.CalcTPSA(mol),
              "logP_model": Descriptors.MolLogP(mol),
              "atoms": atoms, "bonds": Chem.GetAdjacencyMatrix(mol).tolist(),
              "matches": hits, "drawings": drawings, "xy": xy}
    return result, mol


def molecule_image(ax, mol, highlighted=()):
    drawer = rdMolDraw2D.MolDraw2DCairo(800, 380)
    opt = drawer.drawOptions()
    opt.addAtomIndices = True
    opt.minFontSize = 20
    opt.maxFontSize = 29
    opt.padding = 0.12
    rdMolDraw2D.PrepareAndDrawMolecule(drawer, mol, highlightAtoms=list(highlighted),
                                     highlightAtomColors={i: (.99, .78, .36) for i in highlighted})
    drawer.FinishDrawing()
    ax.imshow(plt.imread(io.BytesIO(drawer.GetDrawingText()), format="png"))
    ax.axis("off")


def figures(records, mols, out, language):
    zh = language == "zh"
    tr = lambda cn, en: cn if zh else en
    plt.rcParams.update({"font.family": available_plot_fonts() if zh else ["DejaVu Sans"],
        "font.size": 13, "axes.titlesize": 15, "axes.labelsize": 14,
        "figure.facecolor": "#faf9f6", "axes.spines.top": False,
        "axes.spines.right": False, "svg.fonttype": "path"})
    byid = {r["id"]: r for r in records}
    def save(fig, name):
        for ext in ("svg", "png"):
            fig.savefig(out / f"{name}-{language}.{ext}", dpi=165, bbox_inches="tight")
        plt.close(fig)

    # F1: the same numbered molecular graph explains the branch tokens and atom table.
    fig = plt.figure(figsize=(13, 8.2), layout="constrained")
    gs = fig.add_gridspec(2, 2, height_ratios=[1.15, 1], width_ratios=[1.15, 1])
    ax = fig.add_subplot(gs[0, 0])
    molecule_image(ax, mols["LA?"], [2, 3, 4, 5])
    ax.set_title(tr("同一张图：6 个重原子，6 个隐含氢", "One graph: 6 heavy atoms and 6 implicit H"))
    ax = fig.add_subplot(gs[0, 1]); ax.axis("off")
    ax.text(0, .95, "CC(O)C(=O)O", fontsize=23, family="monospace", color=BLUE, va="top")
    lines = [tr("0–1–3–5：主路径", "0–1–3–5: main traversal"),
             tr("(O)：在原子 1 处分支到原子 2", "(O): branch from atom 1 to atom 2"),
             tr("(=O)：原子 3 与原子 4 形成双键", "(=O): double bond from atom 3 to atom 4"),
             tr("括号控制连接；不增加原子", "Parentheses control connectivity"),
             tr("H 由价态补足，保存在原子属性中", "Hydrogens follow the atom valences")]
    for k, line in enumerate(lines): ax.text(0, .70-k*.125, line, fontsize=14, color=INK)
    ax = fig.add_subplot(gs[1, 0]); ax.axis("off")
    r = byid["LA?"]
    table = ax.table(cellText=[[a["index"], a["element"], a["hydrogens"],
                               ", ".join(map(str, a["neighbors"]))] for a in r["atoms"]],
                     colLabels=[tr("索引", "Index"), tr("元素", "Element"), "H", tr("邻接原子", "Neighbors")],
                     loc="center", cellLoc="center", bbox=[0, .06, 1, .9])
    table.auto_set_font_size(False); table.set_fontsize(14)
    for (i, j), cell in table.get_celld().items():
        cell.set_edgecolor("#d6e1e5")
        if i == 0: cell.set_facecolor("#dce9ee")
    ax = fig.add_subplot(gs[1, 1]); ax.axis("off")
    ax.text(0, .92, tr("1988：SMILES 把分子图写进一行文字", "1988: SMILES encodes a graph in one line"),
            fontsize=15, weight="bold", va="top")
    ax.text(0, .72, "CC(O)C(=O)O\nOC(=O)C(O)C", family="monospace", fontsize=20, color=BLUE, linespacing=1.6, va="top")
    ax.annotate("", xy=(.45, .32), xytext=(.45, .43), arrowprops={"arrowstyle": "->", "color": INK})
    ax.text(0, .25, tr("RDKit 规范表示：CC(O)C(=O)O", "RDKit canonical form: CC(O)C(=O)O"), fontsize=14)
    ax.text(0, .10, tr("不同遍历顺序 → 相同连接关系", "Different traversals → the same connectivity"), fontsize=14)
    save(fig, "graph-and-string")

    # F2: values have separate axes and retain their scientific units.
    fig, axes = plt.subplots(2, 2, figsize=(13, 8), layout="constrained")
    series = [r for r in records if r.get("n")]
    n = np.array([r["n"] for r in series])
    mass = np.array([r["mass_g_mol"] for r in series])
    axes[0, 0].plot(n, mass, "o-", color=BLUE, lw=2.5)
    axes[0, 0].plot(n, 44.053*n+18.015, "+", color=ORANGE, ms=15, mew=2,
                    label=tr("按分子式加和", "Formula sum"))
    axes[0, 0].set_ylabel(tr("摩尔质量 / g mol⁻¹", "Molar mass / g mol⁻¹")); axes[0, 0].legend()
    for i in (0, 5): axes[0, 0].annotate(f"{mass[i]:.3f}", (n[i], mass[i]), xytext=(4, 8), textcoords="offset points")
    axes[0, 1].plot(n, [r["tpsa_A2"] for r in series], "o-", color=GREEN, lw=2.5)
    axes[0, 1].set_ylabel(tr("拓扑极性表面积 / Å²", "Topological polar surface area / Å²"))
    axes[1, 0].plot(n, [r["hba"] for r in series], "o-", lw=2.5, color=BLUE, label=tr("受体位点 HBA", "Acceptor sites HBA"))
    axes[1, 0].plot(n, [r["hbd"] for r in series], "s-", lw=2.5, color=ORANGE, label=tr("供体位点 HBD", "Donor sites HBD"))
    axes[1, 0].set_ylabel(tr("位点数", "Site count")); axes[1, 0].legend()
    axes[1, 1].plot(n, [r["logP_model"] for r in series], "o-", lw=2.5, color=ORANGE)
    axes[1, 1].set_ylabel(tr("片段模型 logP / 无量纲", "Fragment-model logP / dimensionless"))
    for ax in axes.flat:
        ax.set_xlabel(tr("链中乙二醇单元数 n", "Number of ethylene-glycol units n"))
        ax.set_xticks(n); ax.grid(alpha=.18)
    fig.suptitle(tr("明确端基的六个分子：HO–(CH₂CH₂O)ₙ–H", "Six molecules with defined end groups: HO–(CH₂CH₂O)ₙ–H"), fontsize=18)
    save(fig, "oligomer-descriptors")

    # F3: molecular identity depends on which structural attributes are retained.
    fig = plt.figure(figsize=(13, 8.2), layout="constrained")
    gs = fig.add_gridspec(3, 3, height_ratios=[1, 1, .65])
    ids = ["LA1", "LA2", "LA?", "LAC", "BZ1", "BZ2"]
    for k, ident in enumerate(ids):
        ax = fig.add_subplot(gs[k//3, k%3]); r = byid[ident]
        molecule_image(ax, mols[ident])
        stereo = ",".join(a["cip"] for a in r["atoms"] if a["cip"])
        ax.set_title(r[language]+(f" ({stereo})" if stereo else ""), fontsize=14)
        ax.text(.5, -.02, f"{r['formula']}  |  {r['mass_g_mol']:.3f} g mol⁻¹\n{r['canonical']}",
                transform=ax.transAxes, ha="center", va="top", fontsize=12.5)
    ax = fig.add_subplot(gs[2, :]); ax.axis("off")
    cols = [tr("去重时保留的属性", "Attributes retained in the key"), tr("三种乳酸记录", "Three lactic-acid records"), tr("两种苯写法", "Two benzene inputs")]
    cells = [[tr("连接关系、键型、形式电荷、指定构型", "Connectivity, bond type, charge, specified stereo"), "3", "1"],
             [tr("连接关系、键型、形式电荷", "Connectivity, bond type, charge"), "1", "1"]]
    tab = ax.table(cellText=cells, colLabels=cols, cellLoc="center", bbox=[0, .03, 1, .65], colWidths=[.55, .25, .20])
    tab.auto_set_font_size(False); tab.set_fontsize(13)
    for (i, j), cell in tab.get_celld().items():
        cell.set_edgecolor("#d6e1e5")
        if i == 0: cell.set_facecolor("#dce9ee")
    save(fig, "identity-and-stereo")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("results"))
    parser.add_argument("--language", choices=["zh", "en"], default="en")
    args = parser.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    records, molecules = [], {}
    for row in inputs():
        result, mol = process(row); records.append(result)
        if mol is not None: molecules[row["id"]] = mol
    valid = [r for r in records if r["valid"]]
    columns = ["id", "smiles", "valid", "canonical", "without_stereo", "formula", "mass_g_mol",
               "monoisotopic_mass_Da", "heavy_atoms", "total_atoms_with_H", "formal_charge",
               "hbd", "hba", "tpsa_A2", "logP_model", "reason"]
    with (args.output / "structures.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader(); writer.writerows(records)
    writer = Chem.SDWriter(str(args.output / "structures.sdf"))
    for r in valid:
        mol = molecules[r["id"]]; mol.SetProp("_Name", r["id"])
        mol.SetProp("input_smiles", r["smiles"]); writer.write(mol)
    writer.close()
    roundtrip = [m for m in Chem.SDMolSupplier(str(args.output / "structures.sdf")) if m is not None]
    assert len(roundtrip) == len(valid)
    assert [Chem.MolToSmiles(m, isomericSmiles=True) for m in roundtrip] == [r["canonical"] for r in valid]
    series = [r for r in valid if r.get("n")]
    mass_error = max(abs(r["mass_g_mol"]-(44.053*r["n"]+18.015)) for r in series)
    assert mass_error < 1e-10
    summary = {"rdkit_version": rdBase.rdkitVersion, "input_rows": len(records), "valid_rows": len(valid),
               "unique_isomeric": len({r["canonical"] for r in valid}),
               "unique_without_stereo": len({r["without_stereo"] for r in valid}),
               "formula_mass_max_error_g_mol": mass_error,
               "rows": [{k: v for k, v in r.items() if k not in ("drawings", "xy", "atoms", "bonds", "matches")} for r in records]}
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (args.output / "lab-data.json").write_text(json.dumps({"records": records, "patterns": PATTERNS}, ensure_ascii=False), encoding="utf-8")
    figures(valid, molecules, args.output, args.language)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

Run the following command from the directory containing the script. The result directory contains `structures.csv`, `structures.sdf`, a numerical summary, and three figures. The CSV retains the invalid input and its reason, while SDF contains the twelve successfully constructed molecules. The read-back checks verify both molecule count and each recovered canonical isomeric SMILES. The independent mass check uses the manually derived formula for the six series members. The interaction data also contain atom positions, indices, and substructure matches, so the page’s drawings, tables, and descriptors derive from the same calculation. When extending the input set, retain these layers of checking and add examples that cover the new chemical environments.

### Run the complete example

Use zh instead of en for Chinese figures. All generated files are written to results.

```
python main.py --output results --language en
```

A useful way to read the program is to follow one record through the whole calculation before examining the loop over the table. EG3 enters as `OCCOCCOCCO` and produces ten heavy atoms. Including hydrogens gives twenty-four atoms and the formula C₆H₁₄O₄. Of its four oxygens, two occupy terminal positions and two lie internally, giving two hydroxyl matches and two ether-environment matches. The resulting HBD is 2, HBA is 4, and molar mass is 150.174 g/mol. Each result can be traced back to the structure. Extending this inspection from n=1 to n=6 then separates changes that follow directly from atom counts from changes that depend on the chemical rules underlying a descriptor.

## Inspect the structure, atom table, and grouping together

Select a molecule in the experiment to display its numbered structure alongside an atom table and adjacency information. Changing the selected atom simultaneously marks its position, its neighbors, and its table row. The index acts as an address within the current molecular object, allowing a descriptor or property to be traced to a particular atom. Changing the functional-group pattern connects a chemical name with an actual match. Locate the two hydroxyl groups in EG1, then switch to EG6: the terminal hydroxyl count remains two, while the internal ether count grows to five.

The descriptor plot places all valid molecules on common coordinates. The three neutral lactic-acid entries occupy the same point for the available descriptors; the accompanying record table identifies which records overlap. Toggling whether the comparison retains stereochemistry changes the grouping table. The molecular drawing and mass stay unchanged because the toggle changes the comparison key, rather than performing a chemical reaction. Selecting lactate instead changes charge, hydrogen count, and descriptors together, revealing a different level of structural change. Returning to the benzene inputs then demonstrates the complementary case: different input text leads to the same graph after applying the same aromaticity rules.

## Molecular identity workbench

Choose a molecule and functional group, then move the atom index. The structure, adjacency matrix, properties, and grouping table update together. The grouping toggle changes the comparison rule while preserving the original graph.

Yellow: pattern match. Blue ring: selected atom. Dashed blue rings: neighbors. Coordinates serve a 2D depiction.

[Figure: Molecular adjacency matrix](https://ml-biomat.com/tutorials/python-scientific/s04/en/#S04-matrix)

Rows and columns use the same atom indices. Blue cells indicate a bond, white cells no bond. This adjacency matrix does not distinguish single and double bonds.

[Figure: Molecular mass versus descriptor](https://ml-biomat.com/tutorials/python-scientific/s04/en/#S04-scatter)

Common axes preserve the numerical scale. Records sharing coordinates have their identifiers displayed together.

When applying this approach to your own table, begin with a molecule whose formula is easy to calculate. Check hydrogens, charge, composition, and units, then inspect how duplicate records are grouped. If an input contains multiple fragments, such as a molecule and a counterion separated by a dot, establish an explicit rule for retaining or processing the salt form. Preserve relevant isotope and unspecified-stereochemistry fields as well. RDKit makes the operations repeatable, while the research question determines which objects should be compared. Once structural identity is clear, joining experimental batches, properties, and uncertainty columns gives the later statistical analysis a stable basis.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/S04.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [RDKit: Getting Started in Python](https://www.rdkit.org/docs/GettingStartedInPython.html)

   Official open tutorial covering molecular I/O, atom operations, substructure matching, and descriptors.

   Greg Landrum documentation: CC BY-SA 4.0; RDKit software: BSD 3-Clause.
2. [The RDKit Book](https://www.rdkit.org/docs/RDKit_Book.html)

   Specific rules for aromaticity, SMILES support, stereochemistry, and chemical sanitization.

   RDKit documentation; consult the page license and project license for reuse.
3. [Weininger (1988), SMILES: methodology and encoding rules](https://doi.org/10.1021/ci00057a005)

   Original methodological and historical reference, JCICS 28(1), 31–36.

   American Chemical Society journal article.
