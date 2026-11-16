# A Complete Study: Crosslinks, Network Structure and Mechanics

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l16/en/
Language: en

Connect bonding, chain shape, loading and statistics in one complete study, tracing structure and mechanical response within the same network samples.

## Connecting a network material’s structure and response

A gel feels continuous in the hand, yet at molecular scale it contains chains, connections and a surrounding medium. Understanding its softness or recovery calls for several connected questions: which chains are linked, what shapes they adopt, how imposed stretching reaches molecular coordinates, and what continues to change after deformation stops. A structural image or stress curve illuminates part of that sequence. This lesson assembles the observations within one study, so every structural descriptor remains linked to the simulation and mechanical measurement that produced it. The connection between these measurements is as important as any single plot.

The model contains eighty original chains of twenty equal-mass beads, giving 1,600 beads. Neighbouring beads along a chain are linked by finitely extensible springs, while nonbonded approaches are repulsive. Zero, eighty or 160 interchain connections are added to a common melt, followed by rest, extension and holding. Three independent preparations each contain those three branches, creating nine conditions. Explicit solvent and bond-breaking reactions are absent. The model therefore concentrates on permanent connectivity, chain geometry and thermal motion during a specified loading procedure. Those choices make the interpretation concrete while providing a foundation for more chemically detailed network studies.

The complete exercise asks: under common preparation rules, temperature and constant-volume loading history, how does added connectivity change network structure and original-chain geometry, and how do those changes relate to a finite-duration mechanical response? Each condition in that sentence serves a purpose. Shared rules define the comparison, temperature sets the thermal scale, loading history specifies deformation speed and waiting, and finite duration identifies the observation actually made. The figures and code follow this question, allowing the study to be traced from its inputs through structures and time records to the quantities used in interpretation.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l16/en/#en-s1)

Figure 1 · Gelation studies connect bonding with large molecular components; bead–spring dynamics follows chain arrangement and motion. Network mechanics links these observations.

Completeness here means that stages connect: bond identities are retained when models are built, records support reconstruction of shape and stress, analysis uses matching preparation and link-count identifiers, and plots retain all nine conditions. The workflow can begin with an inspectable small system. Establishing these connections makes it clear what must be revisited when particle count, observation time or explicit water is added. By the end, you will have a runnable study and a condition table joining connectivity, chain geometry and mechanical response row by row. This provides a practical basis for extending the scientific question without losing track of how its evidence was generated.

The records show two features together: added connections strongly change connected components, while short-duration mechanical responses retain substantial preparation and temporal variation. Examining both gives more information than expecting every individual reading to rise with link count. Connectivity describes relationships; a mechanical reading describes a particular state and loading history. Spatial chain arrangement and dynamical adjustment connect the two. Understanding that intermediate process turns a sequence of software commands into a materials investigation, because it identifies which molecular observations can explain an outcome and which additional comparisons would clarify it.

## From gel formation to bead–spring models

Gel formation posed a striking question: how can many separately mobile molecules become a connected structure extending across a sample? Flory’s 1941 work considered molecular-size distributions and gelation in three-dimensional polymers; Stockmayer’s 1943 work treated size distributions and gel formation in branched-chain polymers. These studies connected statistical bonding relationships with macroscopic material states. In a present-day simulation, that history motivates identifying who is connected to whom and whether the bonds form many small components or a large one. Visual density alone does not answer the connectivity question, even when a rendered structure appears to fill the entire box.

Chain motion presents another problem. Resolving every atom preserves chemical detail but also spends computation on rapid local vibrations. Bead–spring models retain chain continuity, spatial exclusion and thermal motion with fewer degrees of freedom, supporting observation of more collective changes. Kremer and Grest’s 1990 study of linear polymer-melt dynamics is a classic example of this approach. Our case uses this family of FENE bead–spring interactions with short chains and permanent added links. Its usefulness follows from the mechanisms retained, rather than from assigning each bead an automatic chemical identity or interpreting its reduced length as a measured monomer size.

The two approaches meet in network research. Connection statistics describe the emergence of large components, while molecular dynamics asks how those components arrange themselves, move and carry load in space. A closed route increases graph cycle count, yet differently oriented routes can respond differently to extension. A dangling segment alters local motion while playing a different mechanical role from a strand connecting distant regions. Moving from edge count to loading response therefore requires spatial coordinates and motion history. Graph analysis and dynamics address distinct questions whose combination describes the progression from connectivity to observed mechanics.

Biological networks present related relationships, including connections between extracellular-matrix fibres, protein assemblies and permanent or reversible links in hydrated polymer gels. They may also involve oriented fibres, bending stiffness, solvent exchange and chemical association. Extending this example retains the organization around connectivity, geometry and response while adding the physical mechanisms required by the question. Fibre bending calls for an appropriate angular energy, whereas reversible association calls for a model in which connections can change with specified kinetics or thermodynamics. The intended biological or material process determines which level of detail needs to be introduced next.

The historical ideas lead to concrete measurements here: components and cycles, chain directions, actual cell lengths and the pressure tensor, together with differences between independent preparations. A connectivity threshold is kept distinct from a mechanical measurement. A large connected component can coexist with strongly fluctuating responses over a chosen interval, and similar local connection patterns can have different spatial orientations. The analytical interaction later makes this distinction visible with a few clearly identified nodes before we return to the recorded 1,600-bead systems. This progression connects an accessible geometrical example with the complete simulated study.

## Giving each added connection a physical meaning

The zero-added-link condition already contains nineteen backbone bonds in each of eighty original chains, giving 1,520 bonds. Adding eighty edges brings the total to 1,600; adding 160 brings it to 1,680. Added edges join nearby beads on different original chains, with initial separation no greater than 1.15σ and at most one added edge per bead. These rules make linking spatially local and control the change in bead coordination. The eighty-edge list is the first half of the 160-edge list, retaining a nested relationship for comparisons within each preparation rather than independently replacing all selected connections.

Choosing an added edge introduces a persistent spring-energy term. The FENE potential rises rapidly as bond length approaches its upper bound R₀, limiting separation of bonded beads. The spring coefficient is 30ε/σ² and R₀ is 1.5σ. Original bonds and added edges use the same bonded form, so the comparison changes connectivity and the resulting arrangements without also changing spring stiffness. Bonds persist during loading. The largest recorded bond length is therefore a useful state measurement to inspect relative to R₀; its meaning is distinct from a chemical bond-breaking rate or reaction conversion.

The elastic part of a FENE bondEq. 1

![The elastic part of a FENE bond](https://ml-biomat.com/static/agent-math/9daf9f66ba64c006a5ee3e20.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Uelastic | FENE elastic energy of one bond; the complete bond style also contains short-range repulsion | ε |
| r, R₀ | Bond length and maximum extension scale; R₀=1.5σ | σ |
| K | Elastic coefficient, here 30ε/σ² | ε σ⁻² |
| ln | Natural logarithm of a positive dimensionless argument | operator |
| ², 1, 2 | Squaring, dimensionless constant one and divisor two | operator and constants |
| =, +, −, /, × | Equality, addition, subtraction, division and multiplication; adjacent quantities multiply | operators |

Reading the relationshipAs r approaches R₀, the positive logarithm argument approaches zero; its logarithm becomes strongly negative and the leading minus sign produces a rapidly rising energy.

A worked exampleAt r=1σ, U=−(30×1.5²/2)ln[1−(1/1.5)²]≈19.8378ε. This is the elastic term; the complete bond energy also includes repulsion.

Conditions0≤r<R₀; the fixed-topology FENE model uses the same parameters for original and added bonds.

LAMMPS’s FENE bond implementation also includes short-range repulsion between directly bonded beads, coordinated with special_bonds fene. The bond style supplies this direct-neighbour repulsion, and the nonbonded list avoids counting the same term twice; interactions across two and three bonds retain their specified weights. Added links change the bond table and therefore require special-neighbour relationships to follow the new topology. The complete generator reads a new network.data for each branch so connectivity and interaction counting are updated together. A line added to a structural illustration would change neither the simulation topology nor its forces.

After linking, local bond lengths and surrounding bead arrangements adjust, so each branch rests for 100 time units at fixed volume. A common starting configuration does not require identical coordinates after this rest; different connections guide the branches towards different arrangements. Loading then starts from each branch’s prepared state. In preparation one, adding eighty edges initially raises potential energy by about 1.24037ε per bead, independently recoverable from the added FENE elastic terms. This checks that the new bonds entered the calculation and illustrates why linking changes preparation-stage energy and local forces before any external extension is applied.

All three preparations use density 0.85, temperature one, time step 0.005, thermostat damping time one and unit bead mass. Length, energy and mass scales are σ, ε and m, with the time unit built from them. Mapping the results to a particular polymer requires relevant structural, density, dynamical or mechanical observations. Assigning an arbitrary nanometre value to σ would not by itself establish a physical timescale. The study retains reduced units so its conditions share a defined scale. A subsequent material-specific model can then establish a consistent mapping using the observations relevant to its intended prediction.

Twenty beads per original chain make construction, linking and loading inspectable in a small system. Investigating longer-chain entanglement dynamics makes chain length a deliberate parameter and calls for longer observation of collective motion. Entanglement scales depend on density, stiffness and interactions, so total bead count alone does not establish that regime. Graph cycles here arise from explicit bonds; entanglements involve spatial constraints between chains. Both can affect mechanics, but they refer to distinct structural concepts and require different measurements. Keeping the distinction clear helps identify what a future chain-length study would add to this fixed-connectivity example.

## Reading components, cycles and periodic connections

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l16/en/#en-s4)

Figure 2 · Bond tables, coordinates and pressure records share preparation and link-count identifiers, preserving a one-to-one join.

Treat beads as nodes and bonds as edges to obtain a graph. All beads reachable from one another along bonds form a connected component. Dividing the bead count of the largest component by the total gives its fraction f. Equal bead masses make this also a mass fraction. With zero added edges, every original chain is independent, so the largest component has twenty beads and fraction 0.0125. Added links combine original chains into larger components. A rising fraction describes the extent of connectivity, while leaving the spatial orientation of those connections to a separate geometrical measurement.

Largest-component fractionEq. 2

![Largest-component fraction](https://ml-biomat.com/static/agent-math/8fab9aba4182769e3b97a1bb.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| fmax | Fraction of beads in the largest connected component | 1 |
| Nmax, N | Beads in the largest component and in the full system; N=1600 | 1 |
| max | Label for the largest component, not multiplication | 1 |
| =, +, −, /, × | Equality, addition, subtraction, division and multiplication; adjacent quantities multiply | operators |

Reading the relationshipDividing component size by total size gives its fraction; equal bead masses make number and mass fractions identical.

A worked exampleThe first eighty-link network contains 63 original twenty-bead chains in its largest component: 1260/1600=0.7875.

ConditionsAn undirected graph defined by the actual Bonds table, including original and added bonds.

At eighty added links, the largest components contain sixty-three, sixty-two and sixty-two original chains, giving fractions 0.7875, 0.7750 and 0.7750. At 160 links, they contain seventy-nine, seventy-nine and seventy-eight chains, giving 0.9875, 0.9875 and 0.9750. Equal edge counts can produce different connectivity details because links depend on the prepared arrangements and local candidates. Total component counts are thirteen, thirteen and eighteen for eighty links, and two, two and three for 160 links. Retaining these preparation-specific results reveals the realized variation in network formation instead of replacing all networks at one count with an idealized average structure.

For each added edge, ask whether it joins previously separate components or creates another closed route inside an existing component. The full graph’s number of independent cycles equals edges minus nodes plus components. It is thirteen, thirteen and eighteen for the eighty-link networks, and eighty-two, eighty-two and eighty-three for the 160-link networks. This is a precise graph quantity. Mechanically active strands require additional structural and loading information: cycles have different lengths, positions and orientations, and networks can also contain dangling sections or bottlenecks. Counting cycles is therefore one part of characterizing connectivity rather than a direct measurement of load-bearing strand density.

Independent-cycle countEq. 3

![Independent-cycle count](https://ml-biomat.com/static/agent-math/877650cab8d715b2a8d996ce.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| β | Number of independent cycles in the complete graph | 1 |
| E | Total edge count, including original and added bonds | 1 |
| N | Node count, equal to bead count | 1 |
| C | Connected-component count | 1 |
| =, +, −, /, × | Equality, addition, subtraction, division and multiplication; adjacent quantities multiply | operators |

Reading the relationshipA spanning tree uses one fewer edge than nodes per component. A spanning forest uses N−C edges; each of the remaining E−(N−C) edges adds an independent cycle.

A worked exampleFor the first eighty-link network, E=1600, N=1600 and C=13, so β=13. Two triangles joined by a bridge give E=7, N=6 and C=1, hence β=2.

ConditionsCycle-space dimension of a fixed undirected graph; independent periodic-winding directions additionally require image translations.

Periodic boundaries require an additional check. Beads near opposite cell faces can bond through their minimum-image separation. Following a closed graph route, record the cell translations associated with each edge. Returning to the same bead identifier may leave a nonzero accumulated translation. Independent translation directions define a periodic-winding rank. Every linked network’s largest component in this case has rank three; isolated original-chain components have no such closed winding. This test uses both topology and coordinates, distinguishing a local closed route from a connection that traverses the periodically repeated cell. It adds information beyond the size of the largest component.

A network that winds through a periodic cell generally has no single finite unwrapping that makes every periodic closed route simultaneously short. Our shape analysis therefore retains the identities of the original eighty chains. Each chain uses its bead image flags for unwrapping and its own centre for size measurement. Network connectivity uses the full bond table and periodic edge relations. These analyses have distinct objects: the complete connected graph and the original chains composing it. They are joined through sample identity rather than forced to share one coordinate representation that is unsuitable for a periodically spanning network.

## The same connectivity can have different spatial responses

Consider six nodes forming two triangles joined by one bridge. Rotating the entire drawing preserves six nodes, seven edges, one component, two independent cycles and largest-component fraction one. Now extend horizontal coordinates while contracting vertical coordinates according to a planar slice of a three-dimensional constant-volume mapping. Edges aligned with extension grow more, while transverse edges shorten. Connectivity remains unchanged, yet original orientation affects the energy stored by the springs. This small example makes the missing geometrical information visible: a graph specifies neighbours, whereas distances and directions determine how a prescribed deformation changes its interactions.

Affine quadratic-spring model: six nodes, seven edges, one component and two independent cycles. Rotate the same network before stretching.

[Figure: Rotated and stretched six-node spring network](https://ml-biomat.com/tutorials/molecular-dynamics/l16/en/#en-s5)

Connectivity stays fixed while orientation and stretch change the quadratic spring energy under a prescribed affine deformation.

Quadratic spring energy in the geometry interactionEq. 7

![Quadratic spring energy in the geometry interaction](https://ml-biomat.com/static/agent-math/487088030e84a15a5e28ba91.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Ugeom | Total spring energy after the prescribed affine deformation | ε |
| k | Spring stiffness, one ε/σ² in the interaction | ε σ⁻² |
| e, E | Edge index and edge count E=7 | 1 |
| re, re,0 | Current Euclidean endpoint distance and the undeformed edge length | σ |
| Σ, ², 2 | Sum over seven edges, squaring and divisor two of a quadratic spring | operators and constant |
| =, +, −, /, × | Equality, addition, subtraction, division and multiplication; adjacent quantities multiply | operators |

Reading the relationshipEach edge stores energy when it departs from its equilibrium length. Both extension and compression contribute positively; orientation enters through the deformed distance.

A worked exampleA horizontal bridge of length 2σ becomes 2.4σ at λ=1.2, contributing (1/2)×0.4²=0.08ε. Total energy includes the other six edges.

ConditionsAnalytical geometry with prescribed node motion, before node relaxation and without thermal motion. The native network uses FENE.

The interaction uses quadratic spring energies, each with its undeformed edge length as equilibrium length and unit stiffness. Nodes follow the prescribed deformation together, so the calculated energy belongs to that geometrical operation, before independent node relaxation. At unit stretch all edges have their equilibrium lengths and the energy is zero; stretching or compressing an edge contributes a positive squared deviation. Rotation changes edge orientation relative to loading and thus the resulting energy. This analytical model isolates the role of geometry. The recorded molecular simulations continue to use the FENE interactions and thermal dynamics defined earlier.

The full network cell has an explicit deformation rule. Axial stretch rises linearly from one to 1.2, while both transverse stretches equal the inverse square root of axial stretch, keeping their product one. Final transverse stretch is approximately 0.91287. Loading lasts 100 time units, after which all cell lengths are held fixed. Analysis reads actual recorded cell lengths to check volume and stretch rather than assigning coordinates from requested targets alone. This connects the imposed geometrical operation with the state present at each output time, including the precise order in which deformation and measurements are updated.

Constant-volume deformationEq. 4

![Constant-volume deformation](https://ml-biomat.com/static/agent-math/170d612a42c33b5239e47004.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| λx, λy, λz | Current cell length divided by reference length along each axis | 1 |
| λ | Prescribed axial stretch, one to 1.2 in the simulation and one to 1.5 in the interaction | 1 |
| x, y, z | Loading and transverse coordinate labels | 1 |
| −1/2 | Inverse of the square root | exponent |
| 1 | Unit normalized volume | 1 |
| =, +, −, /, × | Equality, addition, subtraction, division and multiplication; adjacent quantities multiply | operators |

Reading the relationshipOrthogonal-cell volume is the product of its lengths. Unit product of stretch ratios preserves volume; the interaction multiplies coordinates by these same ratios.

A worked exampleAt λ=1.2, each transverse stretch is 1/√1.2≈0.912871, giving product one.

ConditionsThree-dimensional orthogonal geometry with equal transverse scaling. Interactive nodes lie at z=0, a planar slice of this mapping.

Original-chain shape is described by mean-squared extents in three directions. For each chain, find its centre, square each bead’s displacement from that centre along x, y and z, and average over beads. Averaging those quantities over eighty original chains gives Gₓₓ, Gᵧᵧ and Gzz. The x-direction fraction fₓ divides Gₓₓ by their sum. One-third is an isotropic statistical reference; larger fₓ assigns more of the chain’s size to x. This is related to local bond orientation but describes another scale: a chain can extend overall while retaining many locally bent segments along its contour.

Directional extent of the original-chain populationEq. 5

![Directional extent of the original-chain population](https://ml-biomat.com/static/agent-math/60426c1a306412afb2a29ddb.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| M, n | M=80 original chains and n=20 beads per chain | 1 |
| c, i | Original-chain index and bead index | 1 |
| xci, x̄c | Unwrapped x coordinate of bead i in chain c and that chain’s centre coordinate | σ |
| Gxx, Gyy, Gzz | Squared deviations averaged within each chain, then across eighty chains; analogous definitions for y and z | σ² |
| fx | Fraction of population mean-squared extent assigned to x | 1 |
| Σ, ², overbar | Summation, squaring and mean notation | operators |
| 1/M, 1/n | Normalization by chain and bead counts | 1 |
| =, +, −, /, × | Equality, addition, subtraction, division and multiplication; adjacent quantities multiply | operators |

Reading the relationshipMeasuring about each chain’s centre removes translation. Summing directional squared extents gives population mean Rg²; the ratio gives the directional fraction.

A worked exampleFor Gxx=2, Gyy=Gzz=1.5σ², fx=2/5=0.4. The actual preparation-one 160-link value at 200τ is approximately 0.410463.

ConditionsEqual-mass, equal-length original chains unwrapped with image flags; average G before taking the ratio. Uses saved frames at 100, 200 and 300τ.

### Original-chain directional extent at three stages

Saved frames at 100, 200 and 300τ. Average G over eighty chains before calculating the x fraction; the dashed line is the isotropic one-third reference.

LAMMPS 30 Sep 2026 Update 1; official bead–spring interaction model, with 1600 beads in 80 chains of 20, ρ*=0.85 and T*=1, using three initial configurations. The FENE/WCA dynamics time step is 0.005τ.

[Download reference data and complete inputs (ZIP) 48.70 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-network-study-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l16/en/#en-s5)

Compare original-chain shape in saved frames at 100, 200 and 300τ. Gyration tensors are averaged across eighty chains before calculating the x fraction.

For preparation one with 160 links, fₓ is approximately 0.30864 at the end of rest, 0.41046 at the end of loading and 0.39444 at the end of holding. Loading shifts the saved-frame chain extent towards x, followed by partial adjustment. The three plotted times are 100, 200 and 300τ and describe the original-chain population in those saved frames. They are distinct from twenty-time-unit averages. Since stress response Y uses time windows, its temporal definition should be read alongside that of shape. Finer dynamical questions can align the full shape history with stress measurements over matching intervals.

## Joining structure and mechanics in one condition table

Mechanics retains the axial normal-stress difference S and defines Y as its mean over 280<t≤300 minus its mean over 50≤t<100. This response preserves each branch’s pre-loading baseline and has units ε/σ³. Every branch uses the same windows. The program analyses bond tables and pressure records separately, then joins their outputs by the pair of identifiers “preparation” and “added links.” Missing or duplicated conditions trigger an error rather than silent alignment by file order. Reliable sample identity is what allows a structural descriptor to be interpreted beside the mechanical response of the material that actually possessed it.

Finite-duration mechanical responseEq. 6

![Finite-duration mechanical response](https://ml-biomat.com/static/agent-math/c773bd32faf52f1f21d2e703.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Pxx, Pyy, Pzz | Diagonal pressure components, using the pressure sign convention | ε σ⁻³ |
| S | Axial normal-stress difference relative to the transverse mean | ε σ⁻³ |
| S̄hold, S̄rest | Arithmetic means over 280<t≤300 and 50≤t<100, with t in τ | ε σ⁻³ |
| Y | Late-hold response relative to each branch’s own resting baseline | ε σ⁻³ |
| 2, overbar | Divisor two for the transverse mean; overbar denotes a window mean | constant and operator |
| =, +, −, /, × | Equality, addition, subtraction, division and multiplication; adjacent quantities multiply | operators |

Reading the relationshipSubtracting directions removes common isotropic pressure; subtracting windows expresses change relative to the branch baseline.

A worked examplePreparation one at eighty links has baseline≈−0.0114838 and late mean≈0.0407141, giving Y≈0.0521979ε/σ³.

ConditionsRecords are equally spaced by 0.5τ: 100 baseline and forty late-hold records. A finite response under constant-volume loading.

### Connectivity and late response of matching conditions

Each point is one condition; colour denotes added-link count and numbers denote preparations. Structural and mechanical quantities share the same identity.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l16/en/#en-s6)

Each point shares one preparation and link-count identity; structural measurements are joined to the response over specified windows, with preparation numbers beside the points.

The left scatter panel uses largest-component fraction and the right uses independent-cycle count, with Y on both vertical axes. Colour identifies added-link count and nearby numbers identify preparations. Thus the three 160-link points retain their own mechanical responses even when their structural descriptors are close. Preparations one and two both have largest-component fraction 0.9875, yet Y is approximately −0.04285 and 0.15836. Their contrast shows that the fraction does not encode every feature relevant to this measurement: local connection placement, spatial arrangement, thermal motion and finite-window averaging also contribute to the observed response.

Within preparations, the 160-minus-zero paired contrasts are approximately −0.00122, 0.12264 and −0.07388. Common starts are retained within a preparation, and independent generation is retained across preparations. Fitting all nine points to one line could obscure that hierarchy while mixing the joint changes of link count, component fraction and cycle count. The plot instead exposes the relationships observed and motivates more focused comparisons. For example, keeping added-link count fixed while varying local selection rules would investigate connection arrangement through its geometrical and mechanical consequences. Such a design asks a more specific question than treating all co-varying structural descriptors as interchangeable explanations.

### Integrated table of nine study conditions

Each row joins graph structure, shape change and window-defined response for one preparation and link count. CSV and JSON retain full numerical values.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l16/en/#en-s6)

The nine conditions retain their connectivity, periodic winding, local bond lengths, original-chain shape and window-defined stress response in one table.

The condition table places largest-component fraction, component count, cycle count, periodic-winding rank, maximum bond length, loading-induced shape change and Y side by side. Each row represents a complete run, with values traced to its records. Maximum bond length describes the FENE extension range over the procedure; winding rank describes independent cross-cell connection directions; shape change compares two saved times. Their shared row does not give them identical units or temporal meanings. Preserving these definitions prevents one column from becoming an unexamined proxy for another and allows unusual conditions to be traced to the particular run where they occurred.

Temperature, volume and bond-length records also show how the intended procedure was executed. Mean loading and holding temperatures are close to one, relative volume changes are at floating-point recording precision, and maximum bond lengths stay below 1.21σ, separated from the FENE bound of 1.5σ. These quantities check the numerical procedure and the state of the chosen model. Interpretation of the material response still draws on connectivity, direction and stress measurements. Distinguishing execution conditions from scientific observables lets the same condition table support both reproducibility and a clear account of the mechanisms being examined.

The same rested network can receive another loading schedule, such as a larger final stretch or longer hold. Retain that as a distinct procedure while preserving structural identity. Simultaneous changes of amplitude and loading duration define a comparison between procedures; isolating one parameter calls for organized one-factor variations. The present short procedure already supplies starting networks, numerical ranges and observed fluctuations that can guide the next calculation. Its interpretation can remain intact as new measurements are added. In this way each round of computation makes the question more specific and the evidence more informative.

## From complete inputs to a traceable study figure

The complete generator builds initial chains, prepares the melt, selects added edges and writes structures and LAMMPS inputs for each branch. Preparations use different seeds, while zero-, eighty- and 160-link branches within one preparation share the prepared start and nested edge lists. Specify 1,600 beads and a preparation identifier to create clearly named condition directories. Original chain identifiers, selected-edge lists and image information are retained because they support graph analysis, matching and reconstruction of chain dimensions. Each saved item has a role in a later measurement, making the data requirements follow the scientific workflow rather than an indiscriminate output policy.

### Complete construction and simulation

```
"""Prepare, connect, relax and stretch a FENE bead-spring network.

python run_network.py --beads 1600 --replica 1 --out-dir network-runs
The LAMMPS executable is selected by --lmp or the LAMMPS environment variable.
Each independent preparation is followed by zero, one or two links per
original chain in total. The linked cases share nested selected-edge lists.
The output retains the exact selected endpoints, inputs and simulation logs.
"""
from pathlib import Path
import argparse,json,hashlib,subprocess,time,re,math
import numpy as np
import os,shutil
p=argparse.ArgumentParser();p.add_argument('--beads',type=int,default=1600);p.add_argument('--replica',type=int,default=1);p.add_argument('--out-dir',type=Path,default=Path('network-runs'));p.add_argument('--lmp',default=os.environ.get('LAMMPS','lmp'));a=p.parse_args()
N=a.beads;M=N//20;assert N%20==0
base=a.out_dir.resolve();d=base/f'n{N}-rep{a.replica}'
if d.exists():raise SystemExit('Choose a new output directory for this configuration.')
d.mkdir(parents=True)
seed=20263000+a.replica;generator=np.random.default_rng(seed);L=(N/.85)**(1/3);coords=[];bonds=[]
# Pack open chains while retaining the seeded sequence of random draws.
for chain in range(M):
 current=generator.uniform(0,L,3)
 for local in range(20):
  for attempt in range(100000):
   candidate=generator.uniform(0,L,3) if local==0 else current+.97*(v:=generator.normal(size=3))/np.linalg.norm(v)
   if coords:
    dr=np.array(coords)-candidate;dr-=L*np.round(dr/L)
    if np.min(np.sum(dr*dr,axis=1))<.65**2:continue
   break
  else:raise RuntimeError('Chain packing did not find a valid location')
  coords.append(candidate.copy());current=candidate
  if local:bonds.append((len(coords)-1,len(coords)))
lines=['Generated FENE chain starting configuration','',f'{N} atoms',f'{len(bonds)} bonds','','1 atom types','2 bond types','',f'0 {L:.15g} xlo xhi',f'0 {L:.15g} ylo yhi',f'0 {L:.15g} zlo zhi','','Masses','','1 1.0','','Atoms # bond','']
for i,xyz in enumerate(coords):
 image=np.floor(xyz/L).astype(int);wrapped=xyz-L*image;lines.append(f'{i+1} {i//20+1} 1 '+' '.join(f'{x:.15g}' for x in wrapped)+' '+' '.join(str(x) for x in image))
lines+=['','Bonds','']+[f'{j+1} 1 {i} {k}' for j,(i,k) in enumerate(bonds)]
(d/'initial.data').write_text('\n'.join(lines)+'\n')
# Shared reduced-unit, neighbour and special-pair definitions.
header='''units lj
atom_style bond
boundary p p p
special_bonds fene
neighbor 0.4 bin
neigh_modify every 1 delay 0 check yes
'''
# Instantaneous records: time, T, U/N, K/N, E/N, pressure, box and longest bond.
record='''compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cP all pressure cTemp
compute bl all bond/local dist
compute maxbl all reduce max c_bl inputs local
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE/atoms
variable K equal c_cKE/atoms
variable E equal (c_cPE+c_cKE)/atoms
variable pxx equal c_cP[1]
variable pyy equal c_cP[2]
variable pzz equal c_cP[3]
variable bx equal lx
variable by equal ly
variable bz equal lz
variable bmax equal c_maxbl
thermo_style custom step time c_cTemp pe ke etotal c_cP[1] c_cP[2] c_cP[3] lx ly lz c_maxbl
thermo_modify norm no
thermo 1000
fix record all ave/time 100 1 100 v_clock v_T v_U v_K v_E v_pxx v_pyy v_pzz v_bx v_by v_bz v_bmax file thermo.dat format " %.15g"
dump trajectory all custom 500 trajectory.lammpstrj id mol type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
compute chunks all chunk/atom molecule
compute chainRg all gyration/chunk chunks
fix rg all ave/time 100 1 100 c_chainRg file chain-rg.dat mode vector format " %.15g"
'''
# Soft separation, FENE switch, minimization and 100 tau melt preparation.
prepare=header+f'''read_data initial.data
bond_style harmonic
bond_coeff * 100.0 0.97
pair_style soft 1.122462048309373
pair_coeff * * 0
velocity all create 1.0 {seed+100} mom yes rot no dist gaussian
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 {seed+200} zero yes
variable softA equal ramp(0,100)
fix soften all adapt 1 pair soft a * * v_softA
timestep 0.002
thermo 1000
thermo_style custom step temp pe ke etotal
run 20000
unfix soften
unfix dyn
unfix bath
write_data after-soft.data
pair_style lj/cut 1.122462048309373
pair_modify shift yes
pair_coeff * * 1 1 1.122462048309373
bond_style fene
bond_coeff * 30.0 1.5 1.0 1.0
min_style cg
min_modify dmax 0.01
minimize 1e-8 0.01 10000 100000
reset_timestep 0
timestep 0.005
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 {seed+300} zero yes
'''+record+'''run 20000
write_restart melt.restart
write_data melt.data
'''
(d/'prepare.lmp').write_text(prepare,encoding='utf-8',newline='\n')
found=shutil.which(a.lmp);assert found, f'LAMMPS executable not found: {a.lmp}';binary=Path(found).resolve();logs=[]
def run(where,script):
 cmd=[str(binary),'-in',script,'-log','simulation.log']
 r=dict(command=cmd,directory=where.relative_to(base).as_posix(),input_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in where.iterdir() if f.is_file()});t=time.perf_counter()
 with (where/'stdout.log').open('wb') as f:q=subprocess.run(cmd,cwd=where,env={**os.environ,'OMP_NUM_THREADS':'1'},stdout=f,stderr=subprocess.STDOUT)
 r.update(exit_code=q.returncode,wall_seconds=time.perf_counter()-t,output_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in where.iterdir() if f.is_file()});logs.append(r)
 (d/'progress.json').write_text(json.dumps(logs,indent=2));print(json.dumps({'directory':str(where),'exit_code':q.returncode,'wall_seconds':r['wall_seconds']}),flush=True)
 if q.returncode:raise SystemExit(q.returncode)
run(d,'prepare.lmp')
data=(d/'melt.data').read_text();atompart=re.search(r'\nAtoms[^\n]*\n(.*?)(?=\n[A-Z][A-Za-z ]*(?:#.*)?\n|\Z)',data,re.S)[1]
atoms=np.array([[float(x) for x in line.split()] for line in atompart.splitlines() if line.strip()]);atoms=atoms[np.argsort(atoms[:,0])];xyz=atoms[:,3:6];mol=atoms[:,1].astype(int)
# Candidate edges connect nearby beads with different original chain IDs.
candidate=[]
for i in range(N-1):
 dr=xyz[i+1:]-xyz[i];dr-=L*np.round(dr/L);r2=np.sum(dr*dr,1)
 for j in np.flatnonzero((r2<=1.15**2)&(mol[i+1:]!=mol[i])):candidate.append((i,int(i+1+j),float(np.sqrt(r2[j]))))
# Greedy matching uses each bead once; prefixes of one list give nested cases.
edgegen=np.random.default_rng(seed+400);edgegen.shuffle(candidate);edges=[];used=set()
for i,j,dist in candidate:
 if i not in used and j not in used:edges.append((i+1,j+1,dist));used.update((i,j))
target=M*2
if len(edges)<target:raise RuntimeError(f'Only {len(edges)} available edges for {target} target')
# Each branch: 100 tau relaxation, 100 tau extension, 100 tau fixed strain.
choices=[0,M,2*M]
for nc in choices:
 sub=d/f'links-{nc}';sub.mkdir();selected=edges[:nc];text=data
 text=re.sub(r'^\d+ bonds$',f'{len(bonds)+nc} bonds',text,flags=re.M)
 match=re.search(r'\nBonds\s*\n(.*?)(?=\n[A-Z][A-Za-z ]*(?:#.*)?\n|\Z)',text,re.S)
 original=match[1].strip();addition='\n'.join(f'{len(bonds)+j+1} 2 {i} {k}' for j,(i,k,_) in enumerate(selected))
 text=text[:match.start(1)]+original+'\n'+addition+'\n'+text[match.end(1):]
 (sub/'network.data').write_text(text)
 (sub/'selected-crosslinks.json').write_text(json.dumps(dict(seed=seed+400,candidates=len(candidate),selected=selected,definition='Different original chain IDs, minimum-image distance<=1.15, at most one added edge per bead; common ordered candidate list gives nested link sets.'),indent=2))
 protocol=header+f'''bond_style fene
pair_style lj/cut 1.122462048309373
pair_modify shift yes
read_data network.data
bond_coeff * 30.0 1.5 1.0 1.0
pair_coeff * * 1 1 1.122462048309373
reset_timestep 0
timestep 0.005
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 {seed+500} zero yes
'''+record+'''run 20000
write_data relaxed.data
write_restart relaxed.restart
fix stretch all deform 1 x scale 1.2 y volume z volume remap x units box
run 20000
unfix stretch
write_data stretched.data
run 20000
write_data final.data
write_restart final.restart
'''
 (sub/'network.lmp').write_text(protocol,encoding='utf-8',newline='\n');run(sub,'network.lmp')
receipt=dict(case='lammps-network',N=N,chains=M,replica=a.replica,seed=seed,rho=.85,chain_length=20,links=choices,binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),source='Official LAMMPS30Sep2026Update1 bench/in.chain interaction model; independently generated coordinates and explicitly added crosslink/deformation protocols',runs=logs,exit_code=0)
(d/'receipt.json').write_text(json.dumps(receipt,indent=2));print('Network comparison complete',flush=True)
```

Construct three fixed-network branches and retain connectivity, coordinates and native pressure records.

### Complete input for preparation one at eighty links

```
units lj
atom_style bond
boundary p p p
special_bonds fene
neighbor 0.4 bin
neigh_modify every 1 delay 0 check yes
bond_style fene
pair_style lj/cut 1.122462048309373
pair_modify shift yes
read_data network.data
bond_coeff * 30.0 1.5 1.0 1.0
pair_coeff * * 1 1 1.122462048309373
reset_timestep 0
timestep 0.005
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 20263501 zero yes
compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cP all pressure cTemp
compute bl all bond/local dist
compute maxbl all reduce max c_bl inputs local
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE/atoms
variable K equal c_cKE/atoms
variable E equal (c_cPE+c_cKE)/atoms
variable pxx equal c_cP[1]
variable pyy equal c_cP[2]
variable pzz equal c_cP[3]
variable bx equal lx
variable by equal ly
variable bz equal lz
variable bmax equal c_maxbl
thermo_style custom step time c_cTemp pe ke etotal c_cP[1] c_cP[2] c_cP[3] lx ly lz c_maxbl
thermo_modify norm no
thermo 1000
fix record all ave/time 100 1 100 v_clock v_T v_U v_K v_E v_pxx v_pyy v_pzz v_bx v_by v_bz v_bmax file thermo.dat format " %.15g"
dump trajectory all custom 500 trajectory.lammpstrj id mol type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
compute chunks all chunk/atom molecule
compute chainRg all gyration/chunk chunks
fix rg all ave/time 100 1 100 c_chainRg file chain-rg.dat mode vector format " %.15g"
run 20000
write_data relaxed.data
write_restart relaxed.restart
fix stretch all deform 1 x scale 1.2 y volume z volume remap x units box
run 20000
unfix stretch
write_data stretched.data
run 20000
write_data final.data
write_restart final.restart
```

Written by the generator into its branch directory beside network.data.

The connectivity analysis reads network.data and relaxed.data, checks selected edges, calculates components, cycles and winding, and examines bond lengths before and after rest. Mechanical analysis reads thermo.dat and the trajectory, reconstructs original-chain shapes, checks cell lengths and calculates stress-window responses. Both complete programs appear below and can be run separately to inspect their intermediate tables. The study program then joins their numerical outputs by explicit sample keys, producing the three figures and study_conditions.csv. Each plotted quantity follows this traceable path from the appropriate native record through a defined calculation to the integrated result.

### Complete connectivity and periodic-winding analysis

```
"""Measure the actual fixed-topology networks and their initial relaxation.

python analyze_network.py network-runs --out network-analysis --language en
Requires NumPy and Matplotlib. The input directory contains n1600-rep1/2/3.
Each replica contains links-0/80/160 with network.data, relaxed.data,
selected-crosslinks.json and thermo.dat. 
"""
from pathlib import Path
import argparse
import csv
import json
import re

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.collections import LineCollection


def read_data(path):
    """Read the orthogonal atom_style bond files used in this example."""
    text = path.read_text(encoding="utf-8")
    sections, section = {}, None
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        if re.fullmatch(r"[A-Za-z][A-Za-z ]*", line):
            section = line
            sections[section] = []
        elif section:
            sections[section].append(line.split())
    atoms = np.asarray(sections["Atoms"], float)
    atoms = atoms[np.argsort(atoms[:, 0])]
    assert np.array_equal(atoms[:, 0], np.arange(1, len(atoms) + 1))
    bonds = np.asarray(sections["Bonds"], int)
    bounds = []
    for direction in "xyz":
        found = re.search(rf"^([\d.eE+\-]+)\s+([\d.eE+\-]+)\s+{direction}lo {direction}hi", text, re.M)
        bounds.append([float(found[1]), float(found[2])])
    bounds = np.asarray(bounds)
    return {"xyz": atoms[:, 3:6], "mol": atoms[:, 1].astype(int),
            "box": bounds[:, 1]-bounds[:, 0], "bonds": bonds}


def bond_geometry(data):
    ends = data["bonds"][:, 2:4] - 1
    delta = data["xyz"][ends[:, 1]] - data["xyz"][ends[:, 0]]
    shift = -np.rint(delta / data["box"]).astype(int)
    minimum_image = delta + shift * data["box"]
    return ends, shift, np.linalg.norm(minimum_image, axis=1)


def connectivity(data):
    """Graph components, cycle counts and independent periodic directions.

    Integer image offsets are propagated along a spanning tree. A cycle that
    closes at a different periodic image leaves a nonzero integer vector.
    The rank of these vectors counts independent periodic winding directions.
    """
    n = len(data["xyz"])
    ends, shifts, lengths = bond_geometry(data)
    graph = [[] for _ in range(n)]
    for edge_id, ((i, j), shift) in enumerate(zip(ends, shifts)):
        graph[i].append((j, shift, edge_id))
        graph[j].append((i, -shift, edge_id))
    labels = np.full(n, -1, int)
    offsets = np.zeros((n, 3), int)
    components = []
    for root in range(n):
        if labels[root] >= 0:
            continue
        label = len(components)
        labels[root] = label
        stack, vertices, edge_ids, closures = [root], [], set(), []
        while stack:
            i = stack.pop()
            vertices.append(i)
            for j, shift, edge_id in graph[i]:
                edge_ids.add(edge_id)
                trial = offsets[i] + shift
                if labels[j] < 0:
                    labels[j] = label
                    offsets[j] = trial
                    stack.append(j)
                else:
                    assert labels[j] == label
                    closure = trial - offsets[j]
                    if np.any(closure):
                        closures.append(closure.tolist())
        unique_closures = np.unique(closures, axis=0) if closures else np.empty((0, 3), int)
        rank = int(np.linalg.matrix_rank(unique_closures.astype(float), tol=1e-10)) if len(unique_closures) else 0
        components.append({"beads": len(vertices), "edges": len(edge_ids),
                           "original_chains": len(np.unique(data["mol"][vertices])),
                           "independent_cycles": len(edge_ids)-len(vertices)+1,
                           "winding_rank": rank,
                           "integer_closure_vectors": unique_closures.tolist()})
    largest_id = int(np.argmax([c["beads"] for c in components]))
    largest = components[largest_id]
    degree = np.array([len(x) for x in graph])
    return {"components": components, "component_count": len(components),
            "largest": largest, "largest_id": largest_id, "labels": labels,
            "total_cycles": len(ends)-n+len(components), "degree": degree,
            "lengths": lengths, "ends": ends}


def numeric_rows(path):
    return np.loadtxt(path, comments="#")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--out", type=Path, default=Path("network-analysis"))
    parser.add_argument("--language", choices=("en", "zh"), default="en")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    records, raw = [], {}
    for replica in (1, 2, 3):
        base = args.directory / f"n1600-rep{replica}"
        previous_edges = set()
        for count in (0, 80, 160):
            folder = base / f"links-{count}"
            before = read_data(folder / "network.data")
            after = read_data(folder / "relaxed.data")
            graph = connectivity(before)
            later = connectivity(after)
            n = len(before["xyz"])
            assert n == 1600 and len(np.unique(before["mol"])) == 80
            selected = json.loads((folder / "selected-crosslinks.json").read_text(encoding="utf-8"))["selected"]
            chosen = {tuple(sorted((int(x[0]), int(x[1])))) for x in selected}
            assert len(chosen) == count and previous_edges <= chosen
            previous_edges = chosen
            added = before["bonds"][:, 1] == 2
            endpoints = graph["ends"][added]
            assert len(endpoints) == count
            assert len(np.unique(endpoints)) == 2*count
            assert np.all(before["mol"][endpoints[:, 0]] != before["mol"][endpoints[:, 1]])
            assert np.all(graph["lengths"][added] <= 1.15 + 1e-10)
            assert graph["component_count"] == later["component_count"]
            assert graph["largest"]["winding_rank"] == later["largest"]["winding_rank"]
            # Equal masses make the largest bead fraction a mass fraction too.
            largest_fraction = graph["largest"]["beads"] / n
            t = numeric_rows(folder / "thermo.dat")
            t = t[(t[:, 1] >= 0) & (t[:, 1] <= 100)]
            assert len(t) == 201
            elastic_added = float(np.sum(-.5*30*1.5**2*np.log1p(-(graph["lengths"][added]/1.5)**2)))
            if count == 0:
                reference_energy = t[0, 3]
            observed_change = float(t[0, 3]-reference_energy)
            assert abs(observed_change-elastic_added/n) < 1e-9
            assert np.max(graph["degree"]) <= 3
            old_lengths = graph["lengths"][~added]
            new_lengths = graph["lengths"][added]
            relaxed_new = later["lengths"][after["bonds"][:, 1] == 2]
            rec = {"replica": replica, "added_links": count,
                   "beads": n, "total_bonds": len(before["bonds"]),
                   "component_count": graph["component_count"],
                   "largest_component_beads": graph["largest"]["beads"],
                   "largest_component_chains": graph["largest"]["original_chains"],
                   "largest_mass_fraction": largest_fraction,
                   "total_independent_cycles": graph["total_cycles"],
                   "largest_winding_rank": graph["largest"]["winding_rank"],
                   "modified_bead_fraction": 2*count/n,
                   "mean_degree": float(graph["degree"].mean()),
                   "degree_counts": {str(k): int(np.sum(graph["degree"] == k)) for k in (1, 2, 3)},
                   "initial_U_change_per_bead": observed_change,
                   "sum_added_FENE_elastic_per_bead": elastic_added/n,
                   "original_bond_initial_mean": float(old_lengths.mean()),
                   "added_bond_initial_mean": float(new_lengths.mean()) if count else None,
                   "added_bond_after_100tau_mean": float(relaxed_new.mean()) if count else None,
                   "max_bond_before": float(graph["lengths"].max()),
                   "max_bond_after_100tau": float(later["lengths"].max()),
                   "late_50_100tau_temperature_mean": float(t[t[:, 1] >= 50, 2].mean()),
                   "components": graph["components"]}
            records.append(rec)
            raw[(replica, count)] = (before, after, graph, later, t)
    summary = {"case": "fixed FENE networks", "records": records,
               "topology": "All edges retained, including parallel connections between original chains.",
               "winding": "Rank of integer closure vectors; connectivity is distinct from mechanical response.",
               "time_scope": "Topology at insertion; before/after100tau fixed-volume relaxation. All statistics are finite-window descriptors."}
    (args.out / "network_summary.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    table = [{k: v for k, v in rec.items() if k not in ("components", "degree_counts")} for rec in records]
    with (args.out / "network_metrics.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(table[0]))
        writer.writeheader()
        writer.writerows(table)
    zh = args.language == "zh"
    def tr(cn, en):
        return cn if zh else en
    candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else ["DejaVu Sans"]
    installed = {f.name for f in font_manager.fontManager.ttflist}
    plt.rcParams.update({"font.family": [f for f in candidates if f in installed],
                         "font.size": 14, "svg.fonttype": "path", "axes.spines.top": False,
                         "axes.spines.right": False, "axes.unicode_minus": False})
    colors = ["#187e89", "#ca713f", "#7663a0"]
    def save(fig, name):
        fig.savefig(args.out / f"{name}.svg")
        fig.savefig(args.out / f"{name}.png", dpi=150)
        plt.close(fig)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), constrained_layout=True)
    for replica, color in enumerate(colors, 1):
        rr = [x for x in records if x["replica"] == replica]
        for ax, key in zip(axes, ["largest_mass_fraction", "component_count", "total_independent_cycles"]):
            ax.plot([x["added_links"] for x in rr], [x[key] for x in rr], "o-", color=color,
                    label=tr(f"构型 {replica}", f"Configuration {replica}"), alpha=.8)
    axes[0].set_ylabel(tr("最大连通分量质量分数", "Largest-component mass fraction"))
    axes[0].set_ylim(0, 1.05)
    axes[1].set_ylabel(tr("连通分量数", "Connected components"))
    axes[2].set_ylabel(tr("独立环数 E − V + C", "Independent cycles E − V + C"))
    for ax in axes:
        ax.set_xlabel(tr("新增连接数", "Added connections")); ax.set_xticks([0, 80, 160]); ax.grid(alpha=.2)
    axes[0].legend(frameon=False, fontsize=11)
    fig.suptitle(tr("同一熔体逐步加边：哪些链已经连在一起", "Adding edges to each melt: which chains are connected"), fontsize=19)
    save(fig, "network-connectivity")
    # A chain-level circular graph is a connectivity drawing, not a spatial projection.
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.6), constrained_layout=True)
    theta = np.linspace(0, 2*np.pi, 80, endpoint=False)
    positions = np.column_stack([np.cos(theta), np.sin(theta)])
    for ax, count in zip(axes, (0, 80, 160)):
        data, _, graph, _, _ = raw[(1, count)]
        selected = data["bonds"][:, 1] == 2
        chain_ends = data["mol"][graph["ends"][selected]]-1
        segments = positions[chain_ends]
        if len(segments):
            ax.add_collection(LineCollection(segments, colors="#6c9c99", linewidths=.7, alpha=.5))
        chain_labels = graph["labels"][np.arange(80)*20]
        in_largest = chain_labels == graph["largest_id"]
        # At zero links all components are tied; use the same color for all chains.
        node_colors = np.where(in_largest, "#177d88", "#d59564") if count else ["#d59564"]*80
        ax.scatter(positions[:, 0], positions[:, 1], c=node_colors, s=26, zorder=3)
        rr = next(x for x in records if x["replica"] == 1 and x["added_links"] == count)
        ax.set_title(tr(f"{count} 条新增边", f"{count} added edges"))
        ax.text(0, -1.3, tr(f"最大分量：{rr['largest_component_chains']}/80 条链", f"Largest component: {rr['largest_component_chains']}/80 chains"), ha="center", fontsize=12)
        ax.set_aspect("equal"); ax.set_xlim(-1.12, 1.12); ax.set_ylim(-1.46, 1.15); ax.axis("off")
    fig.suptitle(tr("构型 1 的连接图：每个圆点代表一条原始链", "Configuration 1 connectivity: one node per original chain"), fontsize=18)
    save(fig, "network-chain-graph")
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.2), constrained_layout=True)
    bins = np.linspace(.85, 1.20, 36)
    for count, color in zip((80, 160), colors[:2]):
        for stage, linestyle in [(0, "--"), (1, "-")]:
            vals = []
            for replica in (1, 2, 3):
                before, after, graph, later, t = raw[(replica, count)]
                dat, gg = (before, graph) if stage == 0 else (after, later)
                vals.extend(gg["lengths"][dat["bonds"][:, 1] == 2])
            axes[0].hist(vals, bins=bins, density=True, histtype="step", lw=2, color=color, linestyle=linestyle,
                         label=f"{count}: " + (tr("刚加边", "Just connected") if stage == 0 else tr("100τ 后", "After 100τ")))
    for replica, color in enumerate(colors, 1):
        for count, linestyle in [(80, "--"), (160, "-")]:
            t = raw[(replica, count)][4]
            axes[1].plot(t[:, 1], t[:, 12], color=color, ls=linestyle, lw=1.1, alpha=.7,
                         label=tr(f"构型{replica} · {count}边", f"Config. {replica} · {count} links"))
    axes[0].set(xlabel=tr("新增键长 / σ", "Added-bond length / σ"), ylabel=tr("概率密度 / σ⁻¹", "Probability density / σ⁻¹"))
    axes[1].set(xlabel=tr("加边后的时间 / τ", "Time after adding edges / τ"), ylabel=tr("全体系最大键长 / σ", "Largest bond length / σ"))
    for ax in axes:
        ax.legend(frameon=False, fontsize=10, loc="lower center", bbox_to_anchor=(.5, 1.02), ncol=2); ax.grid(alpha=.2)
    fig.suptitle(tr("连接后的局部几何松弛", "Local geometrical relaxation after adding connections"), fontsize=19)
    save(fig, "network-bond-relaxation")
    fig, axes = plt.subplots(2, 1, figsize=(12, 7.4), sharex=True, constrained_layout=True)
    for count, color in zip((0, 80, 160), colors):
        t = raw[(1, count)][4]
        axes[0].plot(t[:, 1], t[:, 2], color=color, lw=1.1, label=tr(f"{count} 条新增边", f"{count} added edges"))
        axes[1].plot(t[:, 1], t[:, 3]-t[0, 3], color=color, lw=1.3)
    axes[0].axhline(1, color="#6d7779", ls="--", lw=1)
    axes[0].set_ylabel(tr("温度 T*", "Temperature T*")); axes[0].legend(frameon=False, loc="lower center", bbox_to_anchor=(.5, 1.02), ncol=3, fontsize=11)
    axes[1].set(xlabel=tr("加边后的时间 / τ", "Time after adding edges / τ"), ylabel=tr("相对各分支起点的 Δ(U/N) / ε", "Δ(U/N) from each branch's start / ε"))
    for ax in axes:
        ax.grid(alpha=.2)
    fig.suptitle(tr("构型 1：固定连接后的温度与势能调整", "Configuration 1: temperature and energy after fixing the connections"), fontsize=18)
    save(fig, "network-preparation")
    print(json.dumps(table, indent=2))


if __name__ == "__main__":
    main()
```

Read bonded and rested structures to compute graph and periodic-connectivity descriptors.

### Complete shape and mechanics analysis

```
"""Read network deformation, stress and original-chain orientation.

python analyze_mechanics.py network-runs --out mechanics --language en
Requires NumPy and Matplotlib. Each n1600-rep1/2/3 directory contains
links-0/80/160 with thermo.dat and trajectory.lammpstrj.
Stress uses the tension-positive normal difference -Pxx+(Pyy+Pzz)/2.
Shading is the sample SD across three independently prepared configurations.
"""
from pathlib import Path
import argparse
import csv
import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


def frames(path):
    """Read orthogonal LAMMPS custom dumps and preserve atom identity."""
    with path.open(encoding="utf-8") as stream:
        while line := stream.readline():
            if not line.strip():
                continue
            assert line.strip() == "ITEM: TIMESTEP"
            step = int(stream.readline())
            assert stream.readline().strip() == "ITEM: NUMBER OF ATOMS"
            n = int(stream.readline())
            assert stream.readline().strip() == "ITEM: BOX BOUNDS pp pp pp"
            bounds = np.array([[float(x) for x in stream.readline().split()] for _ in range(3)])
            columns = stream.readline().split()[2:]
            atoms = np.array([[float(x) for x in stream.readline().split()] for _ in range(n)])
            index = {name: i for i, name in enumerate(columns)}
            atoms = atoms[np.argsort(atoms[:, index["id"]])]
            assert np.array_equal(atoms[:, index["id"]], np.arange(1, n+1))
            xyz = atoms[:, [index[k] for k in ("x", "y", "z")]]
            image = atoms[:, [index[k] for k in ("ix", "iy", "iz")]]
            box = bounds[:, 1]-bounds[:, 0]
            yield step*.005, xyz+image*box, atoms[:, index["mol"]].astype(int), box


def chain_shape(path):
    """Equal-mass original chains: gyration components and bond alignment."""
    rows = []
    for time, xyz, mol, box in frames(path):
        assert len(xyz) == 1600
        assert np.array_equal(mol, np.repeat(np.arange(1, 81), 20))
        chains = xyz.reshape(80, 20, 3)
        relative = chains-chains.mean(axis=1, keepdims=True)
        gyration = np.mean(relative**2, axis=(0, 1))
        vectors = np.diff(chains, axis=1)
        distances = np.linalg.norm(vectors, axis=2)
        assert distances.max() < 1.5
        orientation = np.mean((3*(vectors[:, :, 0]/distances)**2-1)/2)
        rows.append([time, *gyration, orientation, distances.mean(), distances.max()])
    rows = np.asarray(rows)
    assert len(rows) == 121 and np.isclose(rows[-1, 0], 300)
    return rows


def block_means(time, values, start, stop, width):
    """Non-overlapping blocks (left, right], with one mean per block."""
    out = []
    for left in np.arange(start, stop, width):
        mask = (time > left+1e-9) & (time <= left+width+1e-9)
        assert mask.any()
        out.append([left+width/2, np.mean(values[mask])])
    return np.asarray(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--out", type=Path, default=Path("mechanics"))
    parser.add_argument("--language", choices=("zh", "en"), default="en")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    records, raw = [], {}
    for replica in (1, 2, 3):
        for links in (0, 80, 160):
            base = args.directory/f"n1600-rep{replica}"/f"links-{links}"
            thermo = np.loadtxt(base/"thermo.dat", comments="#")
            assert thermo.shape == (601, 13)
            time = thermo[:, 1]
            assert np.allclose(time, np.arange(601)*.5)
            box = thermo[:, 9:12]
            stretches = box/box[0]
            volume_ratio = np.prod(stretches, axis=1)
            # ave/time precedes fix deform in the end-of-step fix order.
            # During loading its recorded box is one integration step behind
            # the post-remap box saved in trajectory/data output.
            recorded_elapsed = np.clip(time-100, 0, 100)
            loading_record = (time > 100) & (time <= 200)
            recorded_elapsed[loading_record] -= .005
            expected_x = 1+.002*recorded_elapsed
            expected_yz = expected_x**(-.5)
            assert np.max(np.abs(stretches[:, 0]-expected_x)) < 1e-12
            assert np.max(np.abs(stretches[:, 1:]-expected_yz[:, None])) < 1e-12
            stress = -thermo[:, 6]+.5*(thermo[:, 7]+thermo[:, 8])
            baseline_mask = (time >= 50) & (time < 100)
            baseline = float(stress[baseline_mask].mean())
            shape = chain_shape(base/"trajectory.lammpstrj")
            start_shape = shape[np.isclose(shape[:, 0], 100)][0]
            end_shape = shape[np.isclose(shape[:, 0], 200)][0]
            final_shape = shape[-1]
            summary = {
                "replica": replica, "added_links": links,
                "initial_box_sigma": box[0].tolist(), "final_box_sigma": box[-1].tolist(),
                "final_stretches": stretches[-1].tolist(),
                "final_engineering_strain": float(stretches[-1, 0]-1),
                "final_hencky_strain": float(np.log(stretches[-1, 0])),
                "engineering_strain_rate_per_tau": .002,
                "max_volume_ratio_error": float(np.max(np.abs(volume_ratio-1))),
                "baseline_stress_50_le_t_lt_100": baseline,
                "loading_end_stress_190_lt_t_le_200": float(stress[(time > 190) & (time <= 200)].mean()),
                "early_hold_stress_200_lt_t_le_220": float(stress[(time > 200) & (time <= 220)].mean()),
                "late_hold_stress_280_lt_t_le_300": float(stress[(time > 280) & (time <= 300)].mean()),
                "loading_temperature_mean": float(thermo[(time > 100) & (time <= 200), 2].mean()),
                "holding_temperature_mean": float(thermo[(time > 200) & (time <= 300), 2].mean()),
                "max_bond_sigma": float(thermo[:, 12].max()),
                "gyration_components_t100": start_shape[1:4].tolist(),
                "gyration_components_t200": end_shape[1:4].tolist(),
                "gyration_components_t300": final_shape[1:4].tolist(),
                "bond_P2_t100": float(start_shape[4]), "bond_P2_t200": float(end_shape[4]),
                "bond_P2_t300": float(final_shape[4]),
                "shape_frames": len(shape), "thermo_records": len(time),
            }
            summary["late_hold_change_from_baseline"] = summary["late_hold_stress_280_lt_t_le_300"]-baseline
            records.append(summary)
            raw[(replica, links)] = {"time": time, "thermo": thermo, "stretches": stretches,
                                     "stress": stress, "baseline": baseline, "shape": shape}
            np.savetxt(args.out/f"shape-rep{replica}-links{links}.csv", shape, delimiter=",",
                       header="time_tau,Gxx_sigma2,Gyy_sigma2,Gzz_sigma2,original_bond_P2,mean_bond_sigma,max_bond_sigma", comments="")
    aggregate = []
    for links in (0, 80, 160):
        group = [row for row in records if row["added_links"] == links]
        row = {"added_links": links, "independent_configurations": 3}
        for key in ("baseline_stress_50_le_t_lt_100", "loading_end_stress_190_lt_t_le_200",
                    "early_hold_stress_200_lt_t_le_220", "late_hold_stress_280_lt_t_le_300",
                    "late_hold_change_from_baseline"):
            values = np.array([g[key] for g in group])
            row[key] = {"mean": float(values.mean()), "sample_sd": float(values.std(ddof=1)), "values": values.tolist()}
        aggregate.append(row)
    result = {"protocol": "100tau fixed volume preparation; 100tau linear Lx ramp to1.2 with constant volume;100tau hold",
              "stress_definition": "S=-Pxx+(Pyy+Pzz)/2, epsilon/sigma^3; tension-positive normal difference",
              "block_definition": "Loading5tau and holding10tau blocks with intervals(left,right]; shading sample SD across3 configurations, not confidence interval",
              "baseline_definition": "50<=t<100, subtracted separately from each branch for holding-change plot",
              "records": records, "aggregate": aggregate}
    (args.out/"mechanics_summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    scalar_keys = [k for k, v in records[0].items() if not isinstance(v, list)]
    with (args.out/"mechanics_metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=scalar_keys, extrasaction="ignore")
        writer.writeheader(); writer.writerows(records)
    zh = args.language == "zh"
    tr = lambda c, e: c if zh else e
    candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"]
    installed = {f.name for f in font_manager.fontManager.ttflist}
    fonts = [f for f in candidates if f in installed] if zh else ["DejaVu Sans"]
    plt.rcParams.update({"font.family": fonts, "font.size": 14, "axes.spines.top": False,
                         "axes.spines.right": False, "svg.fonttype": "path", "text.color": "#193d43",
                         "axes.labelcolor": "#193d43", "figure.facecolor": "#faf9f5", "axes.facecolor": "#faf9f5"})
    colors = ["#167d84", "#c16b3d", "#466eaa"]
    def save(fig, name):
        fig.savefig(args.out/f"{name}-{args.language}.svg")
        fig.savefig(args.out/f"{name}-{args.language}.png", dpi=180)
        plt.close(fig)
    fig, axes = plt.subplots(2, 1, figsize=(12, 7.8), sharex=True, constrained_layout=True)
    first = raw[(1, 160)]
    for i, (label, color, ls) in enumerate(zip(("x", "y", "z"), colors, ("-", "-", "--"))):
        axes[0].plot(first["time"], first["stretches"][:, i], label=label, color=color, ls=ls, lw=2)
    for links, color in zip((0, 80, 160), colors):
        blocks = [block_means(raw[(rep, links)]["time"], raw[(rep, links)]["thermo"][:, 2], 0, 300, 5) for rep in (1, 2, 3)]
        values = np.stack([b[:, 1] for b in blocks]); avg, sd = values.mean(0), values.std(0, ddof=1)
        axes[1].plot(blocks[0][:, 0], avg, color=color, label=tr(f"{links} 条新边", f"{links} links"))
        axes[1].fill_between(blocks[0][:, 0], avg-sd, avg+sd, color=color, alpha=.13)
    for ax in axes:
        ax.axvspan(100, 200, color="#ece4d5", alpha=.5, zorder=0)
        ax.axvline(100, color="#777777", lw=.7, ls=":"); ax.axvline(200, color="#777777", lw=.7, ls=":")
        ax.legend(frameon=False, ncol=3); ax.grid(alpha=.18)
    axes[0].set_ylabel(tr("盒长 / 初始盒长", "Box length / initial length"))
    axes[1].set(xlabel=tr("时间 / τ", "Time / τ"), ylabel=tr("温度 T*", "Temperature T*"))
    axes[1].axhline(1, color="#687574", lw=1, ls="--")
    fig.suptitle(tr("先规定形变，再核对温度和体积", "Specify deformation, then check thermal and geometric conditions"), fontsize=18)
    save(fig, "network-deformation")
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.7), sharey=True, constrained_layout=True)
    fig.get_layout_engine().set(wspace=.12)
    for ax, links, color in zip(axes, (0, 80, 160), colors):
        blocks = [block_means(raw[(rep, links)]["time"], raw[(rep, links)]["stress"], 100, 200, 5) for rep in (1, 2, 3)]
        strain = block_means(raw[(1, links)]["time"], raw[(1, links)]["stretches"][:, 0]-1, 100, 200, 5)[:, 1]
        values = np.stack([b[:, 1] for b in blocks]); avg, sd = values.mean(0), values.std(0, ddof=1)
        for rep, ls in enumerate(("-", "--", ":")):
            ax.plot(strain, values[rep], color=color, ls=ls, alpha=.5, lw=1, label=tr(f"构型{rep+1}", f"Config. {rep+1}"))
        ax.fill_between(strain, avg-sd, avg+sd, color=color, alpha=.13)
        ax.plot(strain, avg, color="#213b40", lw=2.3, label=tr("三组平均", "Mean of three"))
        ax.axhline(0, color="#7c8788", lw=.8); ax.grid(alpha=.15)
        ax.set(title=tr(f"{links} 条新增边", f"{links} added edges"), xlabel=tr("工程应变 e", "Engineering strain e"))
    axes[0].set_ylabel(tr("法向应力差 S / (ε σ⁻³)", "Normal-stress difference S / (ε σ⁻³)"))
    axes[0].legend(frameon=False, fontsize=11)
    fig.suptitle(tr("加载段：5τ 分段平均与三组构型的离散", "Loading: 5τ block means and variation across configurations"), fontsize=18)
    save(fig, "network-stress-strain")
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.7), sharey=True, constrained_layout=True)
    fig.get_layout_engine().set(wspace=.12)
    for ax, links, color in zip(axes, (0, 80, 160), colors):
        blocks = [block_means(raw[(rep, links)]["time"], raw[(rep, links)]["stress"]-raw[(rep, links)]["baseline"], 200, 300, 10) for rep in (1, 2, 3)]
        values = np.stack([b[:, 1] for b in blocks]); avg, sd = values.mean(0), values.std(0, ddof=1)
        for rep, ls in enumerate(("-", "--", ":")):
            ax.plot(blocks[0][:, 0]-200, values[rep], ls=ls, color=color, alpha=.5, lw=1)
        ax.fill_between(blocks[0][:, 0]-200, avg-sd, avg+sd, color=color, alpha=.13)
        ax.plot(blocks[0][:, 0]-200, avg, color="#213b40", lw=2.3)
        ax.axhline(0, color="#7c8788", lw=.8); ax.grid(alpha=.15)
        ax.set(title=tr(f"{links} 条新增边", f"{links} added edges"), xlabel=tr("保持时间 / τ", "Hold time / τ"))
    axes[0].set_ylabel(tr("相对各自静置基线的 ΔS / (ε σ⁻³)", "ΔS from each resting baseline / (ε σ⁻³)"))
    fig.suptitle(tr("固定形变后：10τ 分段平均，阴影为三组间标准差", "Fixed deformation: 10τ blocks; shading is the SD across three configurations"), fontsize=17)
    save(fig, "network-stress-relaxation")
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True, constrained_layout=True)
    for links, color in zip((0, 80, 160), colors):
        shapes = np.stack([raw[(rep, links)]["shape"] for rep in (1, 2, 3)])
        time = shapes[0, :, 0]
        for ax, vals in zip(axes, (shapes[:, :, 4], shapes[:, :, 1]/np.sum(shapes[:, :, 1:4], axis=2))):
            avg, sd = vals.mean(0), vals.std(0, ddof=1)
            ax.plot(time, avg, color=color, label=tr(f"{links} 条新边", f"{links} links"))
            ax.fill_between(time, avg-sd, avg+sd, color=color, alpha=.13)
    for ax in axes:
        ax.axvspan(100, 200, color="#ece4d5", alpha=.5, zorder=0); ax.grid(alpha=.18)
        ax.axvline(100, color="#777777", lw=.7, ls=":"); ax.axvline(200, color="#777777", lw=.7, ls=":")
    axes[0].axhline(0, color="#777777", lw=.8, ls="--")
    axes[1].axhline(1/3, color="#777777", lw=.8, ls="--")
    axes[0].set_ylabel(tr("原链键取向 P₂", "Original-chain bond P₂")); axes[0].legend(frameon=False, ncol=3)
    axes[1].set(xlabel=tr("时间 / τ", "Time / τ"), ylabel=tr("链尺寸的 x 方向占比 Gxx / tr(G)", "Chain-shape x fraction Gxx / tr(G)"))
    fig.suptitle(tr("从局部键取向到整条原链的形状", "From local bond orientation to whole original-chain shape"), fontsize=18)
    save(fig, "network-chain-orientation")
    print(json.dumps(aggregate, indent=2))


if __name__ == "__main__":
    main()
```

Unwrap original chains using image flags; calculate shapes and responses from recorded coordinates, cell lengths and pressure.

### Join structure and mechanics by sample identity

```
"""Join connectivity, chain geometry and mechanics by matched sample identity.

python study_report.py network-runs --out study --language en
Keep analyze_network.py and analyze_mechanics.py beside this file.
Requires NumPy and Matplotlib; each condition supplies the five records
network.data, relaxed.data, selected-crosslinks.json, thermo.dat and
trajectory.lammpstrj.
"""
from pathlib import Path
import argparse
import csv
import json
import subprocess
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


def unique_index(rows):
    keyed = {}
    for row in rows:
        key = (row['replica'], row['added_links'])
        if key in keyed:
            raise ValueError(f'Duplicate sample identity: {key}')
        keyed[key] = row
    expected = {(r, k) for r in (1, 2, 3) for k in (0, 80, 160)}
    if set(keyed) != expected:
        raise ValueError('Expected three preparations with three branches each')
    return keyed


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('records', type=Path)
    p.add_argument('--out', type=Path, default=Path('study'))
    p.add_argument('--language', choices=['zh', 'en'], default='en')
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    here = Path(__file__).resolve().parent
    for script, folder in [('analyze_network.py', 'connectivity'),
                           ('analyze_mechanics.py', 'mechanics')]:
        subprocess.run([sys.executable, str(here/script), str(a.records),
                        '--out', str(a.out/folder), '--language', a.language],
                       check=True, stdout=subprocess.DEVNULL)
    graph = unique_index(json.loads((a.out/'connectivity/network_summary.json').read_text())['records'])
    mechanical = unique_index(json.loads((a.out/'mechanics/mechanics_summary.json').read_text())['records'])
    rows = []
    for key in sorted(graph):
        g, m = graph[key], mechanical[key]
        row = {'replica': key[0], 'added_links': key[1],
               'largest_fraction': g['largest_mass_fraction'],
               'component_count': g['component_count'],
               'independent_cycles': g['total_independent_cycles'],
               'winding_rank_largest': g['largest_winding_rank'],
               'modified_bead_fraction': g['modified_bead_fraction'],
               'initial_added_energy_per_bead': g['initial_U_change_per_bead'],
               'late_response_Y': m['late_hold_change_from_baseline'],
               'max_bond': m['max_bond_sigma'],
               'loading_T': m['loading_temperature_mean'],
               'holding_T': m['holding_temperature_mean'],
               'volume_ratio_error': m['max_volume_ratio_error']}
        for time in (100, 200, 300):
            tensor_diagonal = np.array(m[f'gyration_components_t{time}'])
            row[f'fx_t{time}'] = float(tensor_diagonal[0]/tensor_diagonal.sum())
        row['shape_change_after_load'] = row['fx_t200']-row['fx_t100']
        row['shape_change_after_hold'] = row['fx_t300']-row['fx_t100']
        rows.append(row)
    pairs = []
    for rep in (1, 2, 3):
        at = {r['added_links']: r for r in rows if r['replica'] == rep}
        pairs.append({'replica': rep,
                      'dY_160_minus_0': at[160]['late_response_Y']-at[0]['late_response_Y'],
                      'dfmax_160_minus_0': at[160]['largest_fraction']-at[0]['largest_fraction']})
    summary = {'join_keys': ['replica', 'added_links'],
               'shape_definition': 'fx = mean-chain Gxx / sum of mean-chain diagonal G, original 80 chains, equal bead mass',
               'response_definition': 'Y=meanS(280<t<=300)-meanS(50<=t<100), S=-Pxx+(Pyy+Pzz)/2',
               'scope': 'Nine finite-protocol cases; graph descriptors and geometry joined to their own mechanics. No constitutive regression.',
               'records': rows, 'paired_160_minus_0': pairs}
    (a.out/'study_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    with (a.out/'study_conditions.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    zh = a.language == 'zh'
    tr = lambda x, y: x if zh else y
    available = {f.name for f in font_manager.fontManager.ttflist}
    fonts = ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC', 'WenQuanYi Zen Hei', 'DejaVu Sans']
    plt.rcParams.update({'font.family': [f for f in fonts if f in available] if zh else ['DejaVu Sans'],
                         'font.size': 14, 'svg.fonttype': 'path', 'axes.unicode_minus': False,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'figure.facecolor': '#faf9f5', 'axes.facecolor': '#faf9f5',
                         'text.color': '#193d43', 'axes.labelcolor': '#193d43'})
    colors = {0:'#167d84',80:'#c16b3d',160:'#466eaa'}
    markers = {1:'o',2:'s',3:'^'}
    def save(fig, name):
        fig.savefig(a.out/f'{name}-{a.language}.svg')
        fig.savefig(a.out/f'{name}-{a.language}.png', dpi=160)
        plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.3), constrained_layout=True)
    for row in rows:
        for ax, key in zip(axes, ['largest_fraction', 'independent_cycles']):
            ax.scatter(row[key], row['late_response_Y'], c=colors[row['added_links']],
                       marker=markers[row['replica']], s=85, zorder=3)
            ax.annotate(str(row['replica']), (row[key], row['late_response_Y']),
                        xytext=(7, 3), textcoords='offset points', fontsize=10)
    axes[0].set_xlabel(tr('最大连通分量珠子占比', 'Largest-component bead fraction'))
    axes[1].set_xlabel(tr('全图独立循环数', 'Independent cycles in the full graph'))
    for ax in axes:
        ax.set_ylabel(tr('后段响应 Y / (ε σ⁻³)', 'Late response Y / (ε σ⁻³)'))
        ax.axhline(0, color='#879793', lw=.8);ax.grid(alpha=.18);ax.margins(x=.15)
    handles = [plt.Line2D([], [], marker='o', color='none', markerfacecolor=colors[k],
                         markeredgecolor=colors[k], markersize=8, label=tr(f'{k} 新增边',f'{k} added links')) for k in (0,80,160)]
    fig.legend(handles=handles, loc='outside upper center', ncol=3, frameon=False)
    fig.supxlabel(tr('点旁数字为制备编号；结构与响应来自同一条件',
                     'Numbers identify preparations; each structure is paired with its own response'), fontsize=12)
    save(fig, 'study-structure-response')
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.8), sharey=True, constrained_layout=True)
    fig.get_layout_engine().set(wspace=.1)
    for rep, ax in zip((1,2,3), axes):
        for row in [r for r in rows if r['replica']==rep]:
            k=row['added_links']
            ax.plot([100,200,300], [row[f'fx_t{t}'] for t in (100,200,300)],
                    'o-', color=colors[k], label=tr(f'{k} 边',f'{k} links'), lw=1.7)
        ax.axhline(1/3, color='#879793', ls='--', lw=.8);ax.grid(alpha=.18)
        ax.set(title=tr(f'制备 {rep}',f'Preparation {rep}'), xticks=[100,200,300], xlabel=tr('记录时刻 / τ','Recorded time / τ'))
    axes[0].set_ylabel(tr('原链尺寸 x 方向占比 fₓ','Original-chain shape fraction fₓ'))
    h,l=axes[0].get_legend_handles_labels();fig.legend(h,l,loc='outside upper center',ncol=3,frameon=False)
    fig.supxlabel(tr('100τ：静置末端；200τ：加载末端；300τ：保持末端',
                     '100τ: end of rest; 200τ: end of loading; 300τ: end of hold'), fontsize=12)
    save(fig, 'study-shape-stages')
    fig, ax = plt.subplots(figsize=(14,6.6), constrained_layout=True);ax.axis('off')
    labels = [tr('制备','Prep.'),tr('新边','Links'),tr('最大占比','Largest frac.'),tr('分量数','Components'),
              tr('循环数','Cycles'),tr('绕行秩','Winding rank'),tr('最大键长/σ','Max bond / σ'),
              tr('Δfₓ (200−100τ)','Δfₓ (200−100τ)'),tr('Y / (ε σ⁻³)','Y / (ε σ⁻³)')]
    cells=[]
    for r in rows:
        cells.append([str(r['replica']),str(r['added_links']),f"{r['largest_fraction']:.4f}",str(r['component_count']),
                      str(r['independent_cycles']),str(r['winding_rank_largest']),f"{r['max_bond']:.4f}",
                      f"{r['shape_change_after_load']:+.4f}",f"{r['late_response_Y']:+.5f}"])
    table=ax.table(cellText=cells,colLabels=labels,cellLoc='center',loc='center',
                   colWidths=[.06,.07,.12,.105,.075,.115,.14,.15,.135])
    table.auto_set_font_size(False);table.set_fontsize(12);table.scale(1,2.35)
    for (i,j),cell in table.get_celld().items():
        cell.set_edgecolor('#e1e7e2')
        cell.set_facecolor('#dfeae6' if i==0 else ('#f4f2eb' if ((i-1)//3)%2==0 else '#faf9f5'))
        if i==0:cell.set_text_props(weight='bold')
    ax.set_title(tr('九个条件保留共同身份，逐项连接结构与力学','Nine identified conditions connect structure with mechanics'),fontsize=17,pad=15)
    fig.supxlabel(tr('Δfₓ为两个保存时刻之差；Y为规定窗口的应力差变化',
                     'Δfₓ compares two saved frames; Y compares the specified stress windows'),fontsize=12)
    save(fig,'study-condition-table')
    print(json.dumps({'conditions':len(rows),'paired_differences':pairs},indent=2))


if __name__=='__main__':
    main()
```

Run both analyses, join by preparation and link count, and produce the nine-condition table and three study figures.

The run script completes three preparations and generates Chinese and English study figures. With the reference records, run study_report.py on the parent folder containing the three preparation directories. Each condition supplies network.data, relaxed.data, the selected-edge JSON, thermo.dat and its trajectory. NumPy handles numerical arrays and Matplotlib renders figures, with SVG text converted to paths for offline viewing. Both language versions share the same analysis definitions and numerical results. Filenames and directory relationships preserve sample identity without depending on an absolute location on one person’s computer, allowing the complete example to be moved and reproduced.

### Run the complete three-preparation study

```
#!/usr/bin/env bash
set -euo pipefail
for replica in 1 2 3; do
  python run_network.py --beads 1600 --replica "$replica" --out-dir network-runs
done
python study_report.py network-runs --out study/en --language en
python study_report.py network-runs --out study/zh --language zh
```

Run three preparations, then generate both figure languages; existing reference records can be passed directly to study_report.py.

The table’s fₓ uses the mean G components of eighty original chains: average chain components first, then divide the x component by the sum. This differs from calculating a separate fraction for every chain and averaging those fractions. The former gives larger chains more influence on the population’s directional extent. Text, formula and program consistently use that definition. Other details include counting cycles across all components, reporting winding rank for the largest component, and subtracting each branch’s own baseline in Y. These definitions belong beside formulas and code because they determine what the final numerical entries actually measure.

A useful reproduction exercise follows one row, such as preparation one with eighty links, to recover largest fraction 0.7875, cycle count thirteen and late response about 0.05220. Compare that row first with the zero- and 160-link branches of the same preparation, then with the same link count across preparations. This reading order preserves both matching and material conditions. In a larger study, the same approach can inspect one traceable path before processing remaining conditions in bulk. Scaling the calculation then retains the identities and definitions that made the smaller study interpretable.

## Extending the study towards a particular biomaterial

The useful outcome is a set of relationships from which a more specific question can be developed. These records show how added links enlarge connected components, how chain dimensions respond during loading and how finite-window stresses vary across preparations. A study of connection arrangement can fix edge count and vary local selection rules. A size study can increase chain count while holding density and chain length fixed. A chain-length study must also reconsider relaxation duration and dynamical scales associated with entanglement. Each extension begins with a defined observable and comparison rather than a general expectation detached from the conditions that produced the current result.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l16/en/#en-s8)

Figure 3 · Hydration, fibre bending and reversible connections require different physical mechanisms. Each extension keeps the observable tied to its model conditions.

For a hydrated gel, decide how water enters the model. Explicit solvent supports local hydration, ions and solvent transport, with suitable polymer–water interactions and greater computational cost. An effective-medium description incorporates some solvent influences into interactions or dynamical damping and serves different spatial and temporal questions. Hydration, swelling and exchange of matter through boundaries must then be specified. Constant-volume network loading and an experiment allowing drainage impose different constraints. Connecting simulation with the intended experiment therefore requires its observation conditions to enter the model design, so the chosen representation addresses the physical process actually of interest.

Protein or fibre networks may have directional binding, appreciable bending stiffness and force-dependent connection lifetimes. The same graph analysis can identify connected objects, while mechanics requires energies and evolution rules for those additional degrees of freedom. Records of connection formation and loss can then be linked to structural descriptors and mechanical changes at matching times. The fixed-topology example supplies the organizational pattern. Adding physical mechanisms also expands the records and temporal definitions needed for analysis, ensuring that a changing network is compared using its actual state rather than a connectivity table captured at an unrelated point in the process.

Simulation and experiment can also share observables: mean stress along loading, its evolution during holding, chain or fibre orientation, or volume change under specified conditions. Selecting one principal question helps determine model resolution, system size and statistical replication. It also keeps the resulting study easier to interpret than an unfocused collection of every available descriptor. This example has a clear progression: establish connections, observe geometry and loading response, then interpret differences through matched preparations and defined windows. A subsequent investigation can retain that structure while modifying the physical ingredient most relevant to the chosen material.

From the first particle box to this network study, LAMMPS has performed the same fundamental operations: evaluate forces from specified interactions, advance coordinates and record analysable quantities. A research workflow organizes model choice, units, structure, boundaries, time and statistics around a connected question. Here every added edge is traceable in a bond list, every deformation can be checked against cell-length records, and every structural descriptor belongs to the same row as its mechanical outcome. Preserving these relationships while adding material detail allows the calculation to address progressively more specific questions about polymers and biological materials.

## Further Reading and Open Materials

- [LAMMPS 30 September 2026 Update 1 — bench/in.chain](https://download.lammps.org/tars/lammps-30Sep2026_update1.tar.gz) · LAMMPS developers · GPL-2.0 software source

  FENE bead–spring interactions, reduced units and Langevin/integrator combination.

  Add identity-matched structural/mechanical analysis to the validated 1,600-bead fixed-network workflow, retaining the native dynamics and nine conditions.
- [bond_style fene; special_bonds; read_data](https://docs.lammps.org/bond_fene.html) · LAMMPS developers · Official documentation; cited for definitions

  FENE energy terms, directly bonded repulsion and data topology.

  Explanations, worked examples and diagrams are newly written.
- [special_bonds command](https://docs.lammps.org/special_bonds.html) · LAMMPS developers · Official documentation; cited for command semantics

  The fene weights 0, 1, 1 and bond-topology definitions of special neighbours.

  Explain interaction counting when adding connections.
- [read_data command](https://docs.lammps.org/read_data.html) · LAMMPS developers · Official documentation; cited for command semantics

  Bonds data format and image relationships in periodic connected systems.

  Original route diagrams and periodic-winding analysis.
- [Molecular Size Distribution in Three Dimensional Polymers. I. Gelation (1941)](https://doi.org/10.1021/ja01856a061) · Paul J. Flory · Research article citation; no original text or image reproduced

  Historical connection between gelation and molecular-size distributions.

  Explain the scientific question through original cluster diagrams.
- [Theory of Molecular Size Distribution and Gel Formation in Branched-Chain Polymers (1943)](https://doi.org/10.1063/1.1723803) · Walter H. Stockmayer · Research article citation; no original text or image reproduced

  Statistical treatment of branching and gel formation.

  Historical account checked against a public scholarly memoir.
- [Walter Hugo Stockmayer: A Biographical Memoir (2017)](https://www.nasonline.org/wp-content/uploads/2024/10/Stockmayer_Walter.pdf) · Jeffrey Kovac and Marshall Fixman · National Academy of Sciences memoir; citation and paraphrase, no image reproduced

  Check the context and connections of the 1941–1943 gelation studies.

  Historical information supports the original conceptual explanation.
- [Dynamics of entangled linear polymer melts: A molecular-dynamics simulation (1990)](https://doi.org/10.1063/1.458541) · Kurt Kremer and Gary S. Grest · Scholarly citation; no original text or image reproduced.

  History of bead–spring models and polymer-melt dynamics.

  Original historical concept illustration; the present case uses short-chain fixed networks.
