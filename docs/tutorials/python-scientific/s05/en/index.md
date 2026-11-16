# Connecting Protein Sequences and Structures

Source: https://ml-biomat.com/tutorials/python-scientific/s05/en/
Language: en

Use an internal gap in a real crystal structure to connect sequence positions with coordinates, distances, and structural comparisons.

## Why sequence position 64 can be absent from a structure

A protein sequence contains 89 letters, yet reading its structure yields only 87 carbon atoms representing the backbone. This is a common situation. Pairing the sequence and coordinate lists by row may initially appear correct, but an internal gap shifts the correspondence for every subsequent position. The error can then propagate into mutation labels, distance calculations, and contact maps: the arithmetic runs successfully while the annotations refer to the wrong residues. This chapter uses Biopython with a real public crystal structure to build an explicit map from the complete deposited sequence to observed coordinates. The same map supports structural drawings, gap inspection, distance calculations, and comparison of crystallographic copies of the same protein.

The example is PDB 1BRS, the barnase–barstar complex studied by Buckle, Schreiber, and Fersht in 1994, with X-ray diffraction data at 2.00 Å resolution. Barnase is an enzyme that cleaves RNA; barstar inhibits it by binding to the enzyme. The original study used a barstar variant with C40A and C82A substitutions, and this chapter consistently uses the sequence deposited in the entry. Chains A, B, and C are three crystallographic copies of barnase, while D, E, and F are copies of barstar. They make an easily overlooked issue concrete: the same deposited sequence can have different coordinate coverage in different copies.

The learning goal begins with correspondence. By the end, you should be able to follow a sequence position to an atom in the structure and retain that position when its coordinates are absent. You should also be able to explain a broken trace, a blank row in a distance matrix, and the conditions behind a contact count. Biopython reads and organizes biological objects, NumPy operates on coordinates, and Matplotlib displays the relationships. Connecting these stages provides a practical foundation for handling protein data beyond memorizing a file-reading function.

The chain count in a structural file also differs from the composition of a biological complex. A crystallographic asymmetric unit can contain several molecular copies, describing one independent set of coordinates within the crystal. A biological assembly addresses how molecules form a functional complex. Six protein chains in the coordinate file therefore do not automatically define a biological hexamer. This chapter analyzes sequence positions and Cα coordinates within each of the six chains and keeps their identifiers. Studying the barnase–barstar binding interface would additionally require an appropriate assembly and an explicit cross-chain pairing.

## Letters, residues, and Cα: identify the objects first

A protein can be understood as a chain of connected amino acids. Once incorporated into the chain, an amino-acid unit is called a residue. A sequence letter generally identifies a residue type, rather than an individual atom. For example, A denotes alanine, G glycine, E glutamate, and N asparagine. Each residue contains several atoms. Cα is the central backbone carbon associated with the amino side, carbonyl side, and side-chain environment. Representing each residue by one Cα turns a model containing hundreds of atoms into a readable backbone trace. In this protein context, the atom name `CA` denotes Cα; the two letters alone should not be interpreted as the element calcium.

The complete deposited polymer sequence and the residues appearing in the coordinate model carry different information. The sequence describes the ordered composition of the chain studied, while the coordinate records identify atoms assigned positions in the structural model. Crystal diffraction measures scattering from many molecules, and a model is constructed using electron density and chemical constraints. Some regions may have insufficiently clear density for coordinates to be modeled, while their sequence positions remain part of the deposited chain. An address register with photographs available for some addresses offers a useful analogy: the absence of a photograph does not remove an address from the register. We therefore read sequence and coordinate information separately and connect them through explicit position identifiers.

Biopython’s `Seq` represents a sequence. A `SeqRecord` adds an identifier, description, and annotations around it. FASTA is a compact text representation: a line beginning with `>` contains the record identifier and description, followed by the sequence letters. Line wrapping is formatting and does not create another chain. The program creates six records, identified as `1BRS_A` through `1BRS_F`, writes them with `SeqIO.write()`, and reads them back with `SeqIO.parse()`. Identifiers retain chain identity, and the letters retain the complete deposited order. The FASTA record for chain D consequently has length 89 rather than being shortened to 87 by coordinate coverage.

![Cα coverage of six 1BRS chains and an enlarged comparison of barstar positions 64 E and 65 N. Gray cells beyond the chain length are outside its sequence, rather than missing coordinates.](https://ml-biomat.com/static/tutorials/python-scientific/figures/e3a626ae577ecf5c49b202a4.svg?v=e3a626ae577e)

Figure 1Cα coverage of six 1BRS chains and an enlarged comparison of barstar positions 64 E and 65 N. Gray cells beyond the chain length are outside its sequence, rather than missing coordinates.

The figure first lays out all six chains along their full sequence positions. Chains A and C lack Cα coordinates at positions 1 and 2. Chain D lacks positions 64 and 65, and chain E additionally lacks position 1. Chains B and F have complete Cα coverage. The enlarged internal segment of D, E, and F retains E at position 64 and N at position 65, but the corresponding cells in D and E are orange to indicate absent coordinates. Coverage expresses this information as a compact proportion, while the gap positions remain essential. Two missing terminal residues and two missing internal residues have different consequences for connectivity and annotation.

$$
f_{\mathrm{CA}}=\frac{N_{\mathrm{CA}}}{L}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a49fa40efbf0c96a3ae9ae8f.svg) | Cα coordinate coverage of the selected chain, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/d11a0dfd93acda6605806f9c.svg) | Number of distinct sequence positions with a selected Cα coordinate, dimensionless integer |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Length of the complete deposited polymer sequence, a dimensionless residue count |

Chain D contains 89 deposited positions, 87 with Cα coordinates. Its coverage is 87/89≈0.977528, or 97.75%. The denominator counts sequence positions rather than molecules or all atoms, and each position contributes at most one selected Cα.

## Join by position identifiers, not by list-row numbers

The example uses PDBx/mmCIF. This format organizes different categories of information into named fields. `_entity_poly.pdbx_seq_one_letter_code_can` supplies the polymer sequence, `_struct_asym` associates chain instances with polymer entities, and `_atom_site` contains atomic coordinates and identity fields. An entity describes the molecular type, while a chain instance identifies a particular copy in the file. Thus A, B, and C share one barnase entity, and D, E, and F share one barstar entity. Two dictionaries—entity to sequence and chain to entity—provide the correct complete sequence for every chain.

Within the atom table, `label_seq_id` points to the sequence position in the polymer entity, while `label_asym_id` identifies the chain instance. Together they locate a polymer position within this entry. The file also retains `auth_seq_id` and `auth_asym_id` for the authors’ numbering convention, with an additional insertion-code field. Author numbering can preserve positions from a full-length protein, include gaps or insertions, and need not start at 1 or equal the standardized sequence position. Most observed positions in this example have matching numerical values, but the code retains the fields separately so that the method can be extended to more complicated numbering schemes.

Chain D provides a direct counterexample to joining by row. After sequence position 63, the next observed Cα belongs to position 66. If the observed residues are compressed into a list and counted from 1, list row 64 is already the glycine at sequence position 66, whereas sequence position 64 should be glutamate. Python index 63 in that compressed list therefore gives the wrong residue identity for sequence position 64. The program instead traverses the complete sequence from 1 to 89 and looks up coordinates at each position. An observed position receives its coordinates and atomic attributes; an unobserved position receives a missing value. The map keeps 89 rows, with the gaps at their actual positions, 64 and 65.

`MMCIFParser` additionally organizes the file into a structure–model–chain–residue–atom hierarchy. Setting `auth_chains=False` and `auth_residues=False` explicitly makes the example use standardized chain labels and sequence positions for polymer access. The file’s model numbering begins at 1, while Python index 0 selects the first parsed model; these are also separate numbering systems. Coordinates read directly from the decimal mmCIF fields are checked against the parser’s Atom objects. The two paths examine field identity and structural hierarchy from complementary directions. Their largest coordinate difference here is approximately 3.7×10⁻⁶ Å, arising from the floating-point precision used for parser coordinates.

Atom serial numbers, residue positions, and model numbers should also remain separate. A residue contains multiple atoms, so atom-record numbers increase much faster than sequence positions. A file may contain several models, each reusing chain and residue labels. A complete address for an atom therefore includes its model, chain, residue position, and atom name, with insertion and alternate-location identifiers where applicable. The program fixes the first model and the polymer chains before selecting atoms named CA, keeping other molecular types out of the backbone selection. Specifying each layer makes the same selection interpretable when applied to another file.

## Turn three-dimensional positions into distances and contacts

Each observed Cα has x, y, and z coordinates in Å, where 1 Å equals 0.1 nm. These locate the atom within the structural coordinate system. Translating or rotating the entire coordinate set leaves internal distances unchanged. The distance between two points is the square root of the sum of the squared coordinate differences: the three-dimensional Pythagorean theorem. Squaring gives positive contributions from either direction, and the square root converts the units from Å² back to Å. Calculating one pair directly before expanding to all pairs helps check broadcasting directions and units.

$$
d_{ij}=\sqrt{(x_i-x_j)^2+(y_i-y_j)^2+(z_i-z_j)^2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | Indices of two sequence positions in the same chain, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/6061515e1359986403f43ece.svg) | Cartesian coordinates of the Cα at position i, Å; the corresponding quantities for j have the same meaning |
| ![Formula](https://ml-biomat.com/static/agent-math/4ce29d83e8648088fa2af7b9.svg) | Euclidean distance between the two Cα atoms, Å |

D:63 has coordinates (34.404,25.607,−7.294) Å and D:66 has (32.590,30.124,−6.906) Å. Their differences are 1.814,−4.517,−0.388 Å; squaring, summing, and taking the square root gives 4.883076 Å. A distance is calculated when both endpoints have coordinates; absent positions retain missing values.

The Cα distance between positions 62 and 63 in chain D is about 3.774 Å; between positions 63 and 66 it is about 4.883 Å. The latter pair is adjacent in the compressed coordinate list, but two unobserved sequence positions lie between them. Their relatively short distance does not turn them into an observed continuous backbone segment. The drawing retains the complete position array and uses missing values to interrupt the trace at the gap. Similarly, a residue without coordinates gives an absent row and column in the distance matrix. Filling those missing distances with zero would change “no position available for this calculation” into “every atom coincides with this one.”

![A fixed orthographic view of chain D, a distance matrix in full sequence coordinates, and Cα B factors for three barstar copies. Missing positions remain absent across the views.](https://ml-biomat.com/static/tutorials/python-scientific/figures/639b6002f795821c49ad4b5b.svg?v=639b6002f795)

Figure 2A fixed orthographic view of chain D, a distance matrix in full sequence coordinates, and Cα B factors for three barstar copies. Missing positions remain absent across the views.

A distance matrix provides numerical distances between known positions. An explicitly defined rule can then turn it into a contact map. Here, a contact requires a Cα distance no greater than 8 Å and a separation of at least four sequence positions. The distance cutoff defines geometric proximity for this analysis, while the sequence-separation condition removes immediately local backbone neighbors and emphasizes segments brought together by folding. The matrix is symmetric, so counting its upper triangle counts each residue pair once. Under these conditions, chain D has 177 contacts. When either condition changes, retain it with the result so that the count can be reproduced.

$$
C=\sum_{1\leq i<j\leq L}\mathbf{1}\!\left[d_{ij}\leq r_c\ \mathrm{and}\ |i-j|\geq s\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | Number of distinct residue pairs satisfying the conditions, dimensionless integer |
| ![Formula](https://ml-biomat.com/static/agent-math/47a94dd73f392576cd118ab0.svg) | Sum over distinct index pairs in the chain, with i |
| ![Formula](https://ml-biomat.com/static/agent-math/c97f2f705aae6fe904ed2b60.svg) | L is full sequence length; i and j are sequence positions, all dimensionless integers |
| ![Formula](https://ml-biomat.com/static/agent-math/22ebe45a4378fbd0f4467250.svg) | Indicator: one when both coordinates exist and the conditions hold, zero otherwise |
| ![Formula](https://ml-biomat.com/static/agent-math/4ce29d83e8648088fa2af7b9.svg) | Cα distance between positions i and j, Å |
| ![Formula](https://ml-biomat.com/static/agent-math/35f9cc01c0330718f02f18d2.svg) | Contact distance cutoff, 8 Å by default |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | Minimum separation in sequence positions, four by default |
| ![Formula](https://ml-biomat.com/static/agent-math/bdbedbda53a69f23422a688c.svg) | Absolute difference between sequence position indices, dimensionless |

D:63 and D:66 are 4.883 Å apart, satisfying the 8 Å cutoff, but their index separation is three, below the default four, so this pair is excluded. Applying the same conditions to every observed pair with i

A Cα contact measures coarse spatial proximity. Hydrogen-bond analysis additionally requires appropriate donors and acceptors, distances, and directions. Studying a protein–protein interface requires an explicit cross-chain selection and often uses minimum side-chain heavy-atom distances. This chapter counts intrachain Cα pairs. The B factors shown alongside the structure are atomic displacement parameters from the crystallographic model, with units of Å². They relate to thermal motion, static disorder, and refinement choices. They help examine local differences within a structure, while their definition differs from a per-residue measurement error bar or a molecular-dynamics trajectory. Gray gaps and interrupted B-factor curves preserve the connection between each numerical value and an atom actually present in the model.

A projection is one view of three-dimensional coordinates. In a photograph of a string of beads, beads at different depths can appear adjacent and then separate when the camera turns. Their image-plane distance changes with the view. Here, u and v are the two screen-plane components after rotating the coordinates, while the third component controls front-to-back ordering. Actual point distances still use all three original coordinate components. The contact matrix and distance profile provide numerical companions to the projection: two points can overlap on screen and remain unmarked as a contact when their three-dimensional separation exceeds the cutoff.

## Align copies of the same sequence before comparing their positions

Protein sequences and three-dimensional structures developed historically as two complementary forms of evidence. In his 1958 Nobel lecture, Sanger described how insulin fragments were used to establish the order of amino acids. Knowing which amino acids a protein contains is already a different level of information from knowing their order. Kendrew and colleagues’ 1960 myoglobin study at 2 Å resolution placed spatial arrangement into an atomic structural model. In 1971, the PDB began as a public archive containing seven structures. Sequence, identity fields, and coordinates could increasingly be preserved, compared, and reused together.

Chains D, E, and F in 1BRS bring these kinds of information together in one modern file. Their deposited sequences are identical, while coordinate coverage and local conformation differ. The copies occupy different locations in the crystal coordinate system, so subtracting their coordinates directly would count overall translation and rotation as conformational change. Comparison first requires corresponding residues and then a common rotation and translation that minimize the summed squared deviations between their selected atoms. Biopython’s `Superimposer` performs this rigid-body alignment. Rigid-body means moving the whole chain together, rather than stretching a segment or changing internal distances during alignment.

![Correspondence between sequence positions and coordinate-list rows, with D/F aligned on 87 common Cα atoms. Coordinates shown at positions 64 and 65 belong to F.](https://ml-biomat.com/static/tutorials/python-scientific/figures/47313697e1718c8616f84394.svg?v=47313697e171)

Figure 3Correspondence between sequence positions and coordinate-list rows, with D/F aligned on 87 common Cα atoms. Coordinates shown at positions 64 and 65 belong to F.

The program uses chain D as the reference, selects the 87 Cα positions observed in both D and F, pairs them by sequence position, and aligns F to D. The green F trace still has coordinates at positions 64 and 65, while the blue D trace keeps its interruption. These F positions help locate the structural region corresponding to the gap, but they remain observations from copy F. Inserting them into D would constitute a separate modeling operation to record explicitly. The root-mean-square deviation, RMSD, after alignment is approximately 0.244 Å over the 87 corresponding Cα atoms. This average does not mean that every residue differs by the same distance.

$$
\mathrm{RMSD}=\sqrt{\frac{1}{N}\sum_{k=1}^{N}\left\|\mathbf{x}_k-\left(\mathbf{y}_k R+\mathbf{t}\right)\right\|^2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b17228ca39adc15eff866b18.svg) | Root-mean-square positional deviation after rigid-body alignment, Å |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Number of common Cα atoms used for alignment and comparison, 87 here, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | Index of a selected corresponding atom pair, 1 through N, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/7f1258f7427282b1fcec9cc5.svg) | Coordinate row vector for selected Cα k in reference chain D, Å |
| ![Formula](https://ml-biomat.com/static/agent-math/7821703b8b24f2cff25e51f4.svg) | Coordinate row vector for the corresponding Cα in chain F, Å |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | 3×3 rigid-body rotation matrix applied to F, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/37323ddd9fc7a290f4c2ada8.svg) | Translation row vector applied after rotation, Å |
| ![Formula](https://ml-biomat.com/static/agent-math/a26a4df582a01989203b6838.svg) | Euclidean length of a three-dimensional vector; its square has units Å² |
| ![Formula](https://ml-biomat.com/static/agent-math/610b8056963a095c3539df1f.svg) | Sum over the N selected atom pairs |

Superimposer chooses R and t to minimize the summed squared deviations. For 87 common D/F Cα pairs, RMSD=0.243970 Å, corresponding to a mean squared deviation of about 0.0595214 Å². For a simple two-pair example with aligned distances 0.1 and 0.3 Å, RMSD=√[(0.01+0.09)/2]≈0.223607 Å.

RMSD depends on the selected atoms. Excluding flexible termini, including the whole backbone, or adding side chains changes the comparison. Save the selection and reference structure with the alignment. The diffraction resolution of 2.00 Å describes the overall spatial detail supported by the data, whereas 0.244 Å describes the relative deviation of two constructed models over the specified atom set. They are different quantities. D, E, and F are also copies within the same crystal entry, rather than three independent solution experiments. These distinctions keep the numerical comparison tied to the question it actually answers.

## The complete program carries sequence positions through every calculation

`read_chains()` first reads entity sequences and chain labels, then searches the first model’s atom rows for polymer Cα atoms. It retains standardized position, author numbering, insertion code, alternate-location identifier, occupancy, coordinates, and B factor. If an atom has alternative positions, the program selects the one with higher occupancy; equal occupancies retain the earlier file record. The Cα correspondence is checked again against parser coordinates. Extending the program to new structure types requires inspecting modified residues and alternate conformations, because a single sequence letter does not necessarily express all their chemical details.

The program then builds its residue list along the complete sequence, rather than traversing observed residues alone. The coordinate array keeps the shape “sequence length × 3,” with `NaN` at missing positions. Broadcasting all pairwise coordinate differences produces an array with shape “sequence length × sequence length × 3.” Taking the norm along its final coordinate axis yields the distance matrix. `contacts()` applies the distance and sequence-separation conditions together and returns upper-triangle indices. Array indices begin at zero; adding one when writing sequence positions keeps the figures, tables, and source fields in the same sequence coordinate system.

### Complete sequence mapping, distances, and rigid-body alignment

Use the included public mmCIF file to retain complete sequence positions and generate FASTA, a residue map, numerical results, and figures.

```
"""Connect deposited protein sequences to observed alpha-carbon coordinates.

Public input: PDB 1BRS (CC0), Buckle, Schreiber and Fersht (1994),
doi:10.1021/bi00196a004. Run: python main.py --output results --language en
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import ListedColormap
import numpy as np
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqUtils import seq1
from Bio.PDB import MMCIFParser, Superimposer
from Bio.PDB.MMCIF2Dict import MMCIF2Dict

BLUE,ORANGE,GREEN,INK='#235b89','#bf5635','#177d72','#192b3a'
INPUT=Path(__file__).resolve().parent/'data'/'1BRS.cif'


def available_plot_fonts():
    choices=['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans']
    installed={font.name for font in font_manager.fontManager.ttflist}
    return [name for name in choices if name in installed]


def read_chains(path):
    data=MMCIF2Dict(str(path))
    sequence={entity:''.join(text.split()) for entity,text in zip(
        data['_entity_poly.entity_id'],data['_entity_poly.pdbx_seq_one_letter_code_can'])}
    chains={chain:{'id':chain,'entity':entity,'sequence':sequence[entity],
        'protein':'barnase' if entity=='1' else 'barstar', 'residues':[]}
        for chain,entity in zip(data['_struct_asym.id'],data['_struct_asym.entity_id']) if entity in sequence}
    parser=MMCIFParser(QUIET=True,auth_chains=False,auth_residues=False)
    structure=parser.get_structure('1BRS',str(path))
    selected={}
    count=len(data['_atom_site.id'])
    for row in range(count):
        get=lambda name:data['_atom_site.'+name][row]
        if get('pdbx_PDB_model_num')!='1' or get('label_atom_id')!='CA': continue
        chain,position=get('label_asym_id'),get('label_seq_id')
        if chain not in chains or position in ('.','?'): continue
        position=int(position)
        candidate={'position':position,'resname':get('label_comp_id'),
            'letter':seq1(get('label_comp_id')),'author_chain':get('auth_asym_id'),
            'author_number':get('auth_seq_id'),'insertion_code':get('pdbx_PDB_ins_code'),
            'altloc':get('label_alt_id'),'occupancy':float(get('occupancy')),
            'xyz_A':[float(get('Cartn_'+axis)) for axis in 'xyz'],
            'bfactor_A2':float(get('B_iso_or_equiv'))}
        key=(chain,position)
        if key not in selected or candidate['occupancy']>selected[key]['occupancy']:
            selected[key]=candidate
    maximum_error=0.
    for chain,record in chains.items():
        for position,letter in enumerate(record['sequence'],1):
            observed=selected.get((chain,position))
            if observed:
                assert observed['letter']==letter
                atom=structure[0][chain][position]['CA']
                maximum_error=max(maximum_error,float(np.max(np.abs(atom.coord-np.array(observed['xyz_A'])))))
            record['residues'].append(observed or {'position':position,'letter':letter,'xyz_A':None,'bfactor_A2':None})
        record['observed_count']=sum(r['xyz_A'] is not None for r in record['residues'])
        record['missing']=[r['position'] for r in record['residues'] if r['xyz_A'] is None]
        xyz=np.array([r['xyz_A'] if r['xyz_A'] is not None else [np.nan]*3 for r in record['residues']])
        record['xyz']=xyz
        record['distances']=np.linalg.norm(xyz[:,None,:]-xyz[None,:,:],axis=-1)
    assert maximum_error<1e-5  # Parser coordinates are float32; mmCIF decimals are read as float64.
    return chains,structure,maximum_error


def contacts(record,cutoff=8.,separation=4):
    n=len(record['sequence']);positions=np.arange(1,n+1)
    mask=(record['distances']<=cutoff)&(np.abs(positions[:,None]-positions[None,:])>=separation)
    return np.argwhere(np.triu(mask,1))


def projection(xyz):
    # One fixed orthographic view, shared by each pair of overlaid structures.
    a,b=np.deg2rad([35.,25.])
    rz=np.array([[np.cos(a),-np.sin(a),0],[np.sin(a),np.cos(a),0],[0,0,1]])
    rx=np.array([[1,0,0],[0,np.cos(b),-np.sin(b)],[0,np.sin(b),np.cos(b)]])
    return xyz@rz.T@rx.T


def draw_trace(ax,xyz,color=BLUE,lw=1.8):
    p=projection(xyz)
    # NaN positions break the drawn trace at a missing coordinate.
    ax.plot(p[:,0],p[:,1],color=color,lw=lw)
    ax.set_aspect('equal');ax.set_xlabel('u / Å');ax.set_ylabel('v / Å')


def compare_copies(chains,structure):
    common=[i for i in range(1,90) if i not in chains['D']['missing']]
    fixed=[structure[0]['D'][i]['CA'] for i in common]
    moving=[structure[0]['F'][i]['CA'] for i in common]
    fit=Superimposer();fit.set_atoms(fixed,moving)
    rot,tran=fit.rotran
    transformed=chains['F']['xyz']@rot+tran
    delta=np.linalg.norm(chains['D']['xyz']-transformed,axis=1)
    rms=float(np.sqrt(np.nanmean(delta**2)))
    assert abs(rms-fit.rms)<1e-5
    return {'common_positions':common,'rotation':rot.tolist(),'translation_A':tran.tolist(),
            'rmsd_A':rms,'F_aligned_xyz_A':transformed.tolist(),
            'residue_deviation_A':[None if np.isnan(x) else float(x) for x in delta]}


def make_figures(chains,comparison,out,language):
    zh=language=='zh';tr=lambda cn,en:cn if zh else en
    plt.rcParams.update({'font.family':available_plot_fonts() if zh else ['DejaVu Sans'],
        'font.size':13,'axes.titlesize':15,'axes.labelsize':14,'svg.fonttype':'path',
        'figure.facecolor':'#faf9f6','axes.spines.top':False,'axes.spines.right':False})
    def save(fig,name):
        for ext in ('svg','png'):fig.savefig(out/f'{name}-{language}.{ext}',dpi=165,bbox_inches='tight')
        plt.close(fig)
    fig=plt.figure(figsize=(13,7.5),layout='constrained')
    gs=fig.add_gridspec(2,1,height_ratios=[1,.85])
    ax=fig.add_subplot(gs[0]);arr=np.full((6,110),np.nan)
    for row,record in enumerate(chains.values()):
        arr[row,:len(record['sequence'])]=1
        arr[row,np.array(record['missing'],dtype=int)-1]=0
    cm=ListedColormap([ORANGE,BLUE]);cm.set_bad('#e7e9e9')
    ax.imshow(arr,aspect='auto',interpolation='nearest',cmap=cm,vmin=0,vmax=1,extent=[.5,110.5,5.5,-.5])
    ax.set_yticks(range(6),[f"{r['id']} · {r['protein']}  {r['observed_count']}/{len(r['sequence'])}" for r in chains.values()])
    ax.set_xlabel(tr('沉积序列位置 label_seq_id','Deposited sequence position label_seq_id'))
    ax.set_title(tr('蓝：有 Cα 坐标；橙：缺少坐标；灰：超出该链序列','Blue: Cα present; orange: absent; gray: beyond this chain'))
    ax=fig.add_subplot(gs[1]);ax.set_xlim(59.5,70.5);ax.set_ylim(-.7,2.6)
    for row,chain in enumerate(['D','E','F']):
        r=chains[chain]
        for pos in range(60,71):
            missing=pos in r['missing']
            ax.add_patch(plt.Rectangle((pos-.46,row-.32),.92,.64,facecolor=ORANGE if missing else BLUE))
            ax.text(pos,row,r['sequence'][pos-1],color='white',ha='center',va='center',fontsize=16,weight='bold')
    ax.set_yticks(range(3),['D','E','F']);ax.set_xticks(range(60,71));ax.set_xlabel(tr('序列位置；字母仍保留在缺坐标的位置','Sequence position; letters remain at positions without coordinates'))
    ax.set_title(tr('放大内部缺口：64 E 与 65 N','Internal-gap detail: 64 E and 65 N'))
    save(fig,'sequence-coverage')

    r=chains['D'];fig=plt.figure(figsize=(13,9),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[1.25,.65])
    ax=fig.add_subplot(gs[0,0]);draw_trace(ax,r['xyz']);p=projection(r['xyz'])
    values=np.array([x['bfactor_A2'] for x in r['residues']],dtype=float)
    dots=ax.scatter(p[:,0],p[:,1],c=values,cmap='viridis',vmin=0,vmax=70,s=25,zorder=3)
    for pos in (63,66):ax.scatter(*p[pos-1,:2],s=80,facecolor=ORANGE,edgecolor='white',zorder=5);ax.annotate(str(pos),p[pos-1,:2],xytext=(6,6),textcoords='offset points')
    ax.set_title(tr('D 链：Cα 轨迹与晶体模型 B 因子','Chain D: Cα trace and crystallographic B factor'))
    fig.colorbar(dots,ax=ax,shrink=.65,label='B / Å²')
    ax=fig.add_subplot(gs[0,1]);distance=np.ma.masked_invalid(r['distances']);cmap=plt.get_cmap('magma_r').copy();cmap.set_bad('#cbd3d8')
    im=ax.imshow(distance,origin='lower',extent=[.5,89.5,.5,89.5],cmap=cmap,vmin=0,vmax=45,interpolation='nearest')
    ax.set_xlabel(tr('序列位置 j','Sequence position j'));ax.set_ylabel(tr('序列位置 i','Sequence position i'))
    ax.set_title(tr('两点的真实三维距离','Actual three-dimensional point distance'))
    fig.colorbar(im,ax=ax,shrink=.65,label='d / Å')
    ax=fig.add_subplot(gs[1,:]);positions=np.arange(1,90)
    for chain,color in [('D',BLUE),('E',ORANGE),('F',GREEN)]:
        ax.plot(positions,[x['bfactor_A2'] for x in chains[chain]['residues']],color=color,lw=1.8,label=chain)
    ax.axvspan(63.5,65.5,color='#dbe1e5',alpha=.7);ax.set_xlabel(tr('barstar 序列位置','Barstar sequence position'));ax.set_ylabel('Cα B / Å²');ax.legend(ncol=3);ax.grid(alpha=.16)
    save(fig,'structure-and-distance')

    fig=plt.figure(figsize=(13,8),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[.62,1])
    ax=fig.add_subplot(gs[0,:]);ax.axis('off')
    columns=['label_seq_id',tr('序列字母','Sequence letter'),tr('D 链有 Cα？','Cα in D?'),tr('坐标列表行号（从 1 开始）','Coordinate-list row (one-based)')]
    cell=[]
    observed=[x['position'] for x in r['residues'] if x['xyz_A'] is not None]
    for pos in range(62,68):cell.append([pos,r['sequence'][pos-1],tr('有','Yes') if pos in observed else tr('缺少','Absent'),observed.index(pos)+1 if pos in observed else '—'])
    table=ax.table(cellText=cell,colLabels=columns,cellLoc='center',bbox=[0,.03,1,.94],colWidths=[.19,.18,.18,.45]);table.auto_set_font_size(False);table.set_fontsize(13)
    for (i,j),c in table.get_celld().items():
        c.set_edgecolor('#d4dde2')
        if i==0:c.set_facecolor('#dce9ee')
        elif i in (3,4):c.set_facecolor('#f5dfd7')
    ax=fig.add_subplot(gs[1,0]);fxyz=np.array(comparison['F_aligned_xyz_A']);draw_trace(ax,r['xyz'],BLUE);draw_trace(ax,fxyz,GREEN,lw=1.3)
    p=projection(fxyz)
    for pos in (64,65):ax.scatter(*p[pos-1,:2],color=ORANGE,s=90,zorder=8);ax.annotate(f'F:{pos}',p[pos-1,:2],xytext=(7,7 if pos==64 else -17),textcoords='offset points',color=ORANGE)
    ax.set_title(tr('D（蓝）与对齐后的 F（绿）','D (blue) and aligned F (green)'))
    ax=fig.add_subplot(gs[1,1]);ax.axis('off')
    lines=[(tr('序列位置 ↔ 空间坐标','Sequence positions ↔ coordinates'),15),
           (tr('1958 · Sanger：胰岛素序列','1958 · Sanger: insulin sequence'),14),
           (tr('1960 · Kendrew 等：肌红蛋白结构','1960 · Kendrew: myoglobin structure'),14),
           (tr('1971 · PDB：初始收录 7 个结构','1971 · PDB: seven initial structures'),14),
           (tr('1BRS D/F：沉积序列相同','1BRS D/F: same deposited sequence'),14),
           (tr(f'D/F：87 个共同 Cα；RMSD {comparison["rmsd_A"]:.3f} Å',f'D/F: 87 common Cα; RMSD {comparison["rmsd_A"]:.3f} Å'),14),
           (tr('橙色 64/65：F 链有坐标，D 链空缺','F:64/65 have coordinates; D:64/65 absent'),14)]
    for k,(text,size) in enumerate(lines):ax.text(0,.97-k*.135,text,fontsize=size,va='top',color=INK,weight='bold' if k==0 else 'normal')
    save(fig,'mapping-and-history')


def clean(value):
    if isinstance(value,np.ndarray):return clean(value.tolist())
    if isinstance(value,dict):return {k:clean(v) for k,v in value.items()}
    if isinstance(value,list):return [clean(v) for v in value]
    if isinstance(value,float) and not np.isfinite(value):return None
    return value


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('results'));parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    chains,structure,coordinate_error=read_chains(INPUT)
    records=[SeqRecord(Seq(r['sequence']),id='1BRS_'+r['id'],description=r['protein']+' deposited polymer sequence') for r in chains.values()]
    fasta=args.output/'deposited-sequences.fasta';SeqIO.write(records,fasta,'fasta')
    reread=SeqIO.to_dict(SeqIO.parse(fasta,'fasta'));assert all(str(reread[r.id].seq)==str(r.seq) for r in records)
    fields=['chain','position','letter','observed_CA','author_chain','author_number','insertion_code','bfactor_A2','x_A','y_A','z_A']
    with (args.output/'residue-map.csv').open('w',encoding='utf8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=fields);writer.writeheader()
        for chain,record in chains.items():
            for r in record['residues']:
                row={k:r.get(k) for k in fields};row.update(chain=chain,observed_CA=r['xyz_A'] is not None)
                for axis,v in zip('xyz',r['xyz_A'] or [None]*3):row[axis+'_A']=v
                writer.writerow(row)
    comparison=compare_copies(chains,structure)
    summary={'pdb_id':'1BRS','source_sha256':hashlib.sha256(INPUT.read_bytes()).hexdigest(),
        'parser_coordinate_max_difference_A':coordinate_error,
        'chains':{key:{'length':len(r['sequence']),'observed_CA':r['observed_count'],'missing':r['missing'],
                  'coverage':r['observed_count']/len(r['sequence']),'contacts_8A_sep4':len(contacts(r))} for key,r in chains.items()},
        'D_62_63_distance_A':float(chains['D']['distances'][61,62]),
        'D_63_66_distance_A':float(chains['D']['distances'][62,65]),'DF_common_CA':87,'DF_rmsd_A':comparison['rmsd_A']}
    (args.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
    payload={'chains':chains,'comparison':comparison,'bfactor_colors':(plt.get_cmap('viridis')(np.linspace(0,1,256))[:,:3]*255).round().astype(int).tolist()}
    (args.output/'lab-data.json').write_text(json.dumps(clean(payload),ensure_ascii=False),encoding='utf8')
    make_figures(chains,comparison,args.output,args.language)
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
```

After execution, `deposited-sequences.fasta` contains the six complete sequences, `residue-map.csv` maps every position to its observed atom where available, and `summary.json` reports coverage, gaps, distances, and alignment results. FASTA is read back to check every identifier and sequence. Coordinates are compared between dictionary fields and structural Atom objects. RMSD is recalculated directly from the transformed coordinates. These checks take place before data enter the next stage, helping locate sequence shifts, incorrect chain selections, and unit mismatches at the point where they occur.

### Run the complete example

Use zh for Chinese figures. The input path is resolved relative to the script.

```
python main.py --output results --language en
```

Five rows of the output map provide a compact end-to-end check: D:63 is T with coordinates, D:64 is E without them, D:65 is N without them, D:66 is G with coordinates, and D:67 is A with coordinates. Empty coordinate cells in CSV should be read as missing values rather than as numerical zero. The corresponding FASTA fragment remains TENGA, showing that missing coordinates did not shorten the sequence. For calculations requiring observed coordinates alone, construct a filtered array while retaining the original sequence-position column. Results can then be joined back to the full sequence by position, without reconstructing an offset from the number of deleted rows.

## Follow one residue through sequence, structure, and the contact map

The experiment begins with chain D. Select position 63 to follow the same residue in the sequence cells, the projection of its three-dimensional coordinates, and the contact matrix. Move to position 64: the letter E remains, while coordinates, distances, and contact neighbors are absent. Continue to position 66 and the structure reappears, explicitly associated with sequence position 66. This makes the gap more informative than a total of “two missing residues,” because its consequences can be followed across three representations without changing the sequence coordinate system.

Rotating the view may make projected points overlap or separate, while their three-dimensional distances and the contact count remain unchanged. The view controls change observation direction; the cutoff changes the analysis definition. Reducing the cutoff from 8 Å to 6 Å removes contacts and updates both the matrix and the selected residue’s neighbor table. Changing the minimum sequence separation exposes the contribution of local backbone neighbors. Switching to F and visiting positions 64 and 65 reveals coordinates for the same sequence letters in another copy, making it clear that missing coordinates do not imply the absence of those amino acids from the deposited sequence.

## Residue correspondence and contact experiment

Move from D:63 to D:64 and then D:66 to follow the same position through sequence, structure, and matrix. Rotating the view preserves actual three-dimensional distances.

[Figure: Complete deposited sequence and coordinate coverage](https://ml-biomat.com/tutorials/python-scientific/s05/en/#S05-sequence)

Blue cells have coordinates; orange cells do not. The black outline marks the selected position.

[Figure: Orthographic projection of actual three-dimensional coordinates](https://ml-biomat.com/tutorials/python-scientific/s05/en/#S05-view)

The trace breaks at gaps; orange lines connect the selected residue to its current contact neighbors. Color shows the Cα B factor.

[Figure: Contact matrix](https://ml-biomat.com/tutorials/python-scientific/s05/en/#S05-matrix)

Blue indicates a qualifying contact, pale cells other known distances, and gray cells missing coordinates. Orange outlines identify the selected position.

[Figure: Distance from the selected position to all sequence positions](https://ml-biomat.com/tutorials/python-scientific/s05/en/#S05-profile)

The dashed line is the distance cutoff. Orange points also satisfy the sequence-separation condition.

For your own protein, first establish whether the sequence comes from an experimental construct, a database reference, or the sequence deposited with a structure. Choose the model and chain explicitly. Mapping a UniProt position onto a truncated construct generally requires sequence alignment or an existing database mapping; equal position numbers alone do not establish correspondence. The current program handles correspondence inside one mmCIF entry using its standardized identifiers. Mutation labels, local structural inspection, and later trajectory analysis can then share the same residue map, allowing every numerical result to be traced to a defined sequence position.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/S05.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Biopython Tutorial: Going 3D](https://biopython.org/docs/latest/Tutorial/chapter_pdb.html)

   mmCIF, structural hierarchy, coordinates, and alignment.

   Biopython License Agreement covers software and documentation; some files offer BSD 3-Clause as an alternative.
2. [Biopython Tutorial: Sequence Input/Output](https://biopython.org/docs/latest/Tutorial/chapter_seqio.html)

   SeqRecord and FASTA input/output.

   Biopython License Agreement.
3. [PDB 1BRS: barnase–barstar complex](https://www.rcsb.org/structure/1BRS)

   Public structure and deposited sequences; 2.00 Å X-ray crystallographic model.

   PDB archive data: CC0 1.0.
4. [Buckle, Schreiber and Fersht (1994)](https://doi.org/10.1021/bi00196a004)

   Primary structural study of 1BRS, Biochemistry 33, 8878–8889.

   American Chemical Society journal article.
5. [wwPDB: label_seq_id and author numbering](https://mmcif.wwpdb.org/dictionaries/mmcif_pdbx_v50.dic/Items/_atom_site.auth_seq_id.html)

   Meaning of standardized sequence positions and author numbering.

   wwPDB dictionary reference.
6. [Sanger (1958): The Chemistry of Insulin](https://www.nobelprize.org/prizes/chemistry/1958/sanger/lecture/)

   Historical account of protein-sequence determination.

   Nobel lecture; historical reference.
7. [Kendrew et al. (1960): Structure of Myoglobin](https://doi.org/10.1038/185422a0)

   Original study of the myoglobin three-dimensional structure at 2 Å.

   Nature journal article.
8. [RCSB PDB History](https://www.rcsb.org/pages/about-us/history)

   Establishment of the PDB in 1971 with seven initial structures.

   RCSB website content: CC BY 4.0.
