# How Membranes Organize Molecules: Lipids and Interfaces

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g13/en/
Language: en

Start with the two lipid leaflets and read area, thickness, density and molecular orientation around a membrane protein.

## How can a thin membrane separate water and organize molecules?

Pour cooking oil into water and the two liquids separate after standing. Add detergent and shake, and the oil can disperse into many small droplets. One ingredient of this behaviour is the way different parts of a molecule interact with water. Cell membranes use related molecular differences for more specialized tasks: separating the inside from the outside, allowing selected substances to pass, and providing an environment in which membrane proteins function. When studying delivery particles, artificial vesicles or surface coatings, we often ask whether an added molecule remains outside a membrane, enters it, or changes the arrangement of its neighbours. Molecular simulation turns these questions into observable distributions and motion.

This lesson examines a phospholipid called POPC. It has a headgroup that interacts readily with water and two tails made largely of carbon and hydrogen. These chemically different regions make the molecule amphiphilic. Many such molecules can arrange their tails inside an assembly while exposing headgroups to water on either side, forming a lipid bilayer. The two layers contain lipids pointing in opposite directions, with water outside the membrane. A soap bubble has a different arrangement: water lies between two layers of surfactant molecules whose tails face air. Locating the water first helps distinguish these structures more effectively than drawing every thin film as two rows of circles.

Picture a bilayer as two groups standing back to back, each facing the surrounding environment. The analogy helps identify opposite sides, while the molecular system adds motion: lipids rotate, fluctuate and exchange neighbours, and their tails bend. Headgroups tend to occupy the interfacial region, yet their positions are distributed over a range of heights. Membrane thickness therefore needs a measurable definition, such as the difference between the average heights of phosphorus atoms in the two layers. Density also requires a counting rule: atom number, mass and the population of a selected chemical group describe different things. Choosing that rule establishes what a plotted curve can answer.

The example membrane contains a trimeric protein. This channel structure occupies part of a flexible molecular layer, and surrounding lipids must arrange themselves around it. By the end of the lesson, you will be able to check membrane-system composition, explain why lateral and normal box dimensions use different pressure-scaling factors, measure projected area and thickness, and plot water, protein and lipid distributions along the membrane normal. We will also quantify the overall orientation of the two lipid tails. These measurements come from the same recorded trajectory, linking the spatial organization in a structure image to changes over time rather than judging a system from an attractive snapshot alone.

## From spread-out lipids to a moving molecular mosaic

Before individual membrane molecules could be resolved, researchers used area measurements to investigate membrane structure. In 1925, Gorter and Grendel extracted lipids from red blood cells, spread them as a monolayer on water, and compared the spread area with the cells’ total surface area. Ratios near two supported a bilayer interpretation. The reasoning converted a thickness question into an area comparison: the same molecules require more area when spread in one layer than when divided between two layers.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g13/en/#en-s2)

Figure 1 · Conceptual area comparison and fluid-mosaic view. Equal molecule counts illustrate one layer versus two; the lower diagram places a protein within the bilayer.

A geometrical exercise makes this reasoning accessible. Suppose two hundred identical tiles each occupy one square. Spreading all the tiles across a table covers two hundred squares. Placing one hundred below and one hundred above makes two layers covering one hundred squares. The exercise separates molecule number, footprint per molecule and layer count. Real lipids can change their packing, tilt and compression, while the historical measurements also involved estimating extracted lipid amounts and cell surface area. The approximate area ratio was consequently a structural clue with measurement conditions. Simulation analysis benefits from the same habit: before inferring a structure from a number, establish exactly how that number was obtained.

In 1972, Singer and Nicolson’s fluid mosaic model placed proteins and lipids within one dynamic picture. Amphipathic proteins were embedded in a lipid environment, with polar regions exposed to water and nonpolar regions compatible with the membrane interior; components could move laterally. This viewpoint replaced a fixed-partition picture with an interface whose molecular arrangement and motion matter. The channel and surrounding lipids in our example fit naturally into that framework: the protein defines local spatial boundaries, while lipid organization and fluctuations provide its environment.

Fluidity also needs a direction. A lipid changing neighbours within one leaflet undergoes a different motion from moving its polar headgroup through the hydrophobic interior to the opposite leaflet. The latter changes the leaflet assignment and traverses a different molecular environment. “Upper” and “lower” name the two leaflets relative to the chosen coordinate axis; they do not automatically mean extracellular and intracellular. Actual cells can place different lipids, glycans and proteins on their two sides. The present single-POPC composition allows us to concentrate on planar-membrane geometry and measurement definitions before introducing chemical asymmetry and the additional questions it creates.

On a computer, the area question becomes more detailed. Molecule identities are known, positions can be followed, and a configuration can be divided into slices in which protein, lipid and water are counted separately. This description requires an explicit interaction model and observation time. The classical all-atom model used here retains atomic motion, lipid conformations and nonbonded interactions with fixed chemical connectivity. Chemical reactions, environment-dependent protonation changes and the architecture of a whole cell require additional modeling choices. Defining observables around the motions retained by the current model keeps the molecular structure, the calculation and the scientific question aligned.

## Meet the system: channel, lipids, water and ions

The protein originates from public structure 1MAL, the maltoporin LamB. Three chains of 421 amino-acid residues form a trimer; the experimental structure was determined by X-ray diffraction at 3.10 Å resolution. Each subunit has a beta-barrel framework forming a channel through the membrane. Its biological context involves sugar transport, while the present simulation contains no transported sugar and applies no transmembrane concentration difference. Our question concerns the membrane environment and local protein–lipid motion around a prepared configuration. Measuring a transport rate would additionally require defining entry, passage and exit events and collecting enough of them under specified driving conditions.

The complete model has 138,195 atoms: 19,260 protein atoms, 37,118 atoms in 277 POPC molecules, 81,612 atoms in 27,204 water molecules, and 131 sodium plus 74 chloride ions. The protein trimer carries a total charge of −57 elementary charges. The excess 57 sodium ions neutralize it, while the remaining 74 sodium–chloride pairs supply additional salt. A POPC headgroup contains both positively and negatively charged regions, although the whole molecule has zero net charge. Such a zwitterionic molecule differs from one without electrostatic interactions: nearby water and ions respond to the different charged atoms even though their charges sum to zero.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g13/en/#en-s3)

Figure 2 · Orthographic projections of the first frame of this production segment. Cα connections guide the backbone path; phosphorus-to-terminal-carbon lines guide lipid orientation. Water, ions and other atoms participate in the underlying simulation.

The topology specifies the protein’s chemical states. Each chain retains the disulfide bond between cysteines 22 and 38. Its six histidines use the neutral HSD form, with a hydrogen on the ring’s Nδ1 atom. The N terminus has three terminal hydrogens, and the C terminus is a negatively charged carboxylate. The same residue and terminal definitions apply to all three chains. Continuing this model preserves those choices; a thermostat does not change protonation in response to the solution. For a question involving a site’s protonation state, construct and compare the relevant chemical models before interpreting changes in local interactions or channel behaviour.

Protein, POPC and water use the supplied, internally consistent CHARMM topology and parameter set. The water residue is named TIP3 and uses the CHARMM TIP3P form associated with this parameterization. Other three-site water models with similar names have different parameters, so changing a filename alone changes more than a label. Van der Waals forces are switched between 1.0 and 1.2 nm, electrostatics use PME with a 1.2 nm short-range cutoff, bonds involving hydrogen are constrained, and the integration step is 2 fs. Together these settings define the energy and motion in this example. Altering one requires checking its compatibility with the others.

The starting files already contain coordinates and velocities from preparation of the combined membrane–protein system. Such preparation commonly begins by relieving close contacts, followed by progressively weaker restraints that allow water, headgroups and tails to adjust around the protein. Here we continue from the saved state of the last NPT preparation stage, run a 20 ps unrestrained pilot, and record another 200 ps. This starting point focuses the exercise on analysis of a complete membrane. The membrane organization already exists when recording begins, so the trajectory describes local fluctuations. A later coarse-graining lesson examines a separate trajectory in which dispersed lipids assemble into a membrane.

The composition table also clarifies the level of the model. The protein structure belongs to a bacterial outer-membrane channel, while its surroundings here are a specified POPC environment. The immediate question is local organization in that lipid environment. Studying the permeability of a complete bacterial outer membrane would require its relevant complex composition, differences between the two sides and solution conditions. A single-component environment also supports controlled comparisons: lipid type can be changed while protein chemical states and temperature–pressure settings are retained. State the simplification together with the question it is intended to isolate.

## A membrane has two kinds of direction

Place the membrane in the xy plane and its normal along z. The box width and height then have different physical roles. Increasing the lateral area changes the space available to proteins and lipids within each leaflet; changing the z length primarily changes the surrounding water layer and separation in the normal direction. Scaling all three directions together is often natural for a nearly homogeneous box of water. For a membrane, allowing lateral area and normal dimensions to respond separately to pressure expresses their different roles. The example therefore uses semiisotropic pressure coupling: x and y share one scaling factor, while z has another.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g13/en/#en-s4)

Figure 3 · Geometrical view of semiisotropic pressure coupling. The x and y lengths share a scaling factor and z has its own; the barostat determines the actual factors.

Semiisotropic coupling allows the membrane dimensions to change. The lateral box lengths can expand or contract together, and the normal length can respond independently. Both pressure targets are set to 1 bar. Box volume is the product of three lengths, whereas projected area is the product of the two lateral lengths. A lateral linear increase of one part in a thousand acts in both x and y, producing an area increase of approximately two parts in a thousand. Considering length, area and volume within one worked example prevents a linear change from being mistaken for the same fractional area change.

Box lengths, area and semiisotropic scalingEq. 1

![Box lengths, area and semiisotropic scaling](https://ml-biomat.com/static/agent-math/61873ca8714f13c97d68c885.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Lₓ, Lᵧ, L𝓏 | Orthogonal box lengths in the three directions | nm |
| A, A′ | Projected membrane-plane box area before and after scaling | nm² |
| V, V′ | Box volume before and after scaling | nm³ |
| s∥, s⊥ | Lateral and normal length-scaling factors | 1 |
| ′, ∥, ⊥ | Prime marks the scaled value; parallel and perpendicular refer to the membrane plane | 1 |
| ² | Square: multiply the factor by itself | 1 |
| =, ×, /, −, + | Equality, multiplication, division, subtraction and addition; adjacent quantities multiply | 1 |

Reading the relationshipRectangle area multiplies its two sides, and volume multiplies the height; scaling both lateral lengths multiplies area by s∥².

A worked exampleWith Lₓ=Lᵧ=10 nm and L𝓏=8 nm, A=100 nm² and V=800 nm³. For s∥=1.01 and s⊥=0.99, A′=102.01 nm² and V′=807.9192 nm³.

ConditionsOrthogonal box with membrane normal along z; scaling factors illustrate geometry.

The barostat changes the box in response to pressure, while molecular motion continues under thermal fluctuations and interparticle forces. Instantaneous pressure can fluctuate much more visibly than temperature because it includes contributions from motion and interactions. Between 100 and 200 ps, the recorded mean temperature is 300.069 K with a sample standard deviation across saved points of 0.766 K. The pressure mean over that interval is about −1.60 bar, with a pointwise sample standard deviation of about 119.71 bar. These standard deviations describe fluctuations in the saved record, rather than confidence intervals on its mean. Statistical assessment of the pressure target also involves correlation times and longer segmented records.

Temperature uses v-rescale coupling with a 1 ps time constant, and pressure uses C-rescale with a 5 ps time constant. The thermostat treats the whole system as one temperature-coupling group. Translational centre-of-mass motion is handled using the specified protein–membrane and solvent groups. These settings describe how the modeled system exchanges energy with its thermal surroundings and adjusts its dimensions. For a first exercise, reading the inputs one parameter at a time is more informative than changing many values together. Identify the target conditions, response times and integration step separately, then compare the actual trajectories produced by a deliberate change.

### Complete parameters for the 20 ps pilot

```
;;Preprocessing
title                   = Production

;; no position constraints

;;Run and Output control
integrator              = md
dt                      = 0.002      ;0.002 ps or 2 fs
nsteps = 10000
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
nstcalcenergy = 100
nstenergy = 100
nstlog = 1000
;
nstcomm = 100
comm_mode               = linear
comm_grps               = SOLU_MEMB SOLV 

;;VdW
cutoff-scheme           = Verlet
nstlist                 = 20
rlist                   = 1.2

;;VdW
vdwtype                 = Cut-off
vdw-modifier            = Force-switch
rvdw_switch             = 1.0
rvdw                    = 1.2

;;Electrostatics
coulombtype             = pme
rcoulomb                = 1.2

;;Bonds
constraints             = h-bonds
constraint_algorithm    = LINCS
continuation            = yes

;;Temperature coupling
tcoupl                  = V-rescale 
tc_grps                 = SYSTEM
tau_t                   = 1.0 
ref_t                   = 300

;;Pressure coupling is on
pcoupl                  = C-rescale 
pcoupltype              = semiisotropic
tau_p                   = 5.0
compressibility         = 4.5e-5  4.5e-5
ref_p                   = 1.0     1.0
refcoord_scaling        = com


; periodic boundary condition
;pbc                     = xyz       

ld-seed = 20263131
```

Continue from the prepared state with bond constraints and released position restraints.

### Complete parameters for 200 ps production

```
;;Preprocessing
title                   = Production

;; no position constraints

;;Run and Output control
integrator              = md
dt                      = 0.002      ;0.002 ps or 2 fs
nsteps = 100000
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
nstcalcenergy = 100
nstenergy = 100
nstlog = 1000
;
nstcomm = 100
comm_mode               = linear
comm_grps               = SOLU_MEMB SOLV 

;;VdW
cutoff-scheme           = Verlet
nstlist                 = 20
rlist                   = 1.2

;;VdW
vdwtype                 = Cut-off
vdw-modifier            = Force-switch
rvdw_switch             = 1.0
rvdw                    = 1.2

;;Electrostatics
coulombtype             = pme
rcoulomb                = 1.2

;;Bonds
constraints             = h-bonds
constraint_algorithm    = LINCS
continuation            = yes

;;Temperature coupling
tcoupl                  = V-rescale 
tc_grps                 = SYSTEM
tau_t                   = 1.0 
ref_t                   = 300

;;Pressure coupling is on
pcoupl                  = C-rescale 
pcoupltype              = semiisotropic
tau_p                   = 5.0
compressibility         = 4.5e-5  4.5e-5
ref_p                   = 1.0     1.0
refcoord_scaling        = com


; periodic boundary condition
;pbc                     = xyz       

ld-seed = 20263131
```

300 K, semiisotropic 1 bar, 2 fs steps; coordinates every 1 ps.

The complete run script combines coordinates, topology, index groups and parameters into binary input, executes dynamics, and selects energy observables by name. Coordinates are saved every 1 ps and energies every 0.2 ps, giving 201 configurations and 1,001 energy records over 200 ps when the starting point is included. Continuation uses a saved state file so that velocities and associated state enter the next stage. Run the script in the directory containing the prepared inputs. Its md.tpr, md.xtc and md-properties.xvg outputs are the three files read by the analysis program below, keeping the connection between simulation and plotted quantities explicit.

### Complete simulation and energy extraction

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
"$gmx" grompp -f pilot.mdp -c prepared.gro -t prepared.cpt -p topol.top -n index.ndx -o pilot.tpr > pilot.grompp.log 2>&1
"$gmx" mdrun -deffnm pilot -ntmpi 1 -ntomp 4 -pin off > pilot.stdout.log 2>&1
"$gmx" grompp -f md.mdp -c pilot.gro -t pilot.cpt -p topol.top -n index.ndx -o md.tpr > md.grompp.log 2>&1
"$gmx" mdrun -deffnm md -ntmpi 1 -ntomp 4 -pin off > md.stdout.log 2>&1
printf 'Temperature
Potential
Pressure
Volume
Density
Box-X
Box-Y
Box-Z
0
' | "$gmx" energy -f md.edr -o md-properties.xvg > energy.log 2>&1
"$gmx" check -f md.xtc > trajectory-check.log 2>&1
```

Run beside prepared.gro, prepared.cpt, topol.top, index.ndx and the toppar directory.

Bond-length constraints and preparation-stage position restraints have different roles. A bond constraint fixes a selected interatomic distance, removing that rapid stretching motion from the freely integrated degrees of freedom. A position restraint instead draws selected atoms toward reference locations and affects their displacement through space. This production segment retains constraints on covalent bonds involving hydrogen while releasing the preparation restraints. Lipids and protein can translate, rotate and change many internal angles while respecting the constrained distances. Seeing the constraints entry in an input therefore does not mean that an entire molecule has been pinned in place.

## Find the leaflets before defining area and thickness

The displayed box boundary is one way to cut a periodic space. A small translation can move part of a molecule through the top face and back through the bottom. Averaging raw z coordinates can then place two nearby positions far apart. Analysis first restores each molecule along its explicit bonds and establishes a consistent membrane centre. Here a circular mean of the terminal-carbon positions from both lipid tails locates the midplane. Imagine rolling the z axis into a circle so that its two endpoints meet: positions just above zero and just below the box length remain neighbours rather than being treated as opposite ends of a line.

Each phosphorus atom is assigned its nearest periodic displacement from this midplane. At the first saved frame, positive displacements define the upper leaflet and negative displacements define the lower one; those assignments are checked throughout the trajectory. The system contains 137 upper-leaflet lipids and 140 lower-leaflet lipids, with unchanged assignments in all 201 frames. Unequal counts can be compatible with the different cross-sections occupied by an embedded protein on the two sides and with the geometry established during preparation. Retain the actual counts when analyzing the system. Dividing 277 by two and pretending that each leaflet contains 138.5 molecules would lose that structural information.

Expressing heights around one membrane centreEq. 2

![Expressing heights around one membrane centre](https://ml-biomat.com/static/agent-math/c9a17b7e0182a21bcd7b88eb.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| zᵢ | Raw height of atom i | nm |
| z₀ | Chosen periodic membrane-midplane position | nm |
| L𝓏 | Box length in z | nm |
| δzᵢ | Nearest periodic height relative to the midplane | nm |
| i, 0 | Atom index; midplane reference label | 1 |
| round | Round to the nearest integer to count box-length shifts | 1 |
| ( ), / | Parentheses group operations; a fraction bar denotes division | 1 |
| =, ×, /, −, + | Equality, multiplication, division, subtraction and addition; adjacent quantities multiply | 1 |

Reading the relationshipSubtract the closest integer number of box lengths from the relative height, placing it within half a box length of the midplane.

A worked exampleFor L𝓏=10 nm, z₀=0.2 nm and zᵢ=9.8 nm, the raw difference is 9.6 nm; round(0.96)=1, giving δzᵢ=−0.4 nm.

ConditionsFor z in an orthogonal periodic box; the two images are equidistant at exactly half a box length.

One thickness definition subtracts the lower leaflet’s mean phosphorus height from the upper leaflet’s mean height. This measures the separation between two average phosphate-headgroup planes. Hydrophobic-core thickness, the distance between locations where water density reaches a chosen threshold, and the separation between electron-density peaks have related but distinct definitions. Headgroups fluctuate in height, and a protein can deform the nearby interface. Naming the current measurement precisely makes comparison with an experiment or another simulation more useful. Apparent disagreements in “membrane thickness” can partly reflect differences in which molecular feature was used to locate the two boundaries.

Distance between mean phosphate planesEq. 3

![Distance between mean phosphate planes](https://ml-biomat.com/static/agent-math/f5bbe5e6120a5b5899a95abf.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| dPP | Difference between mean upper- and lower-leaflet phosphorus heights | nm |
| N₊, N₋ | Upper- and lower-leaflet phosphorus counts; one phosphorus per POPC | 1 |
| δzᵢ, δzⱼ | Atom heights relative to the same membrane midplane | nm |
| i, j, +, − | Atom indices and upper/lower leaflet labels | 1 |
| Σ, ∈ | Sum over atoms in the specified leaflet; membership in that set | 1 |
| 1 | Constant one in the reciprocal count forming an arithmetic mean | 1 |
| =, ×, /, −, + | Equality, multiplication, division, subtraction and addition; adjacent quantities multiply | 1 |

Reading the relationshipAverage each set of heights separately and subtract; a common shift of the reference midplane cancels.

A worked exampleUpper heights 1.8 and 2.0 nm average 1.9 nm. Lower heights −2.0, −1.8 and −1.9 nm average −1.9 nm, giving 3.8 nm separation.

ConditionsFor identifiable leaflets in a nearly planar membrane; measures the separation of mean phosphorus planes.

From 100 to 200 ps, the projected box area averages 139.065 nm², with a sample standard deviation across frames of 0.190 nm². The phosphate-plane distance averages 3.8516 nm, with a frame standard deviation of 0.0117 nm. These curves describe lateral dimensions and organization along the normal respectively. The protein RMSD uses all 1,263 Cα atoms, aligns the trimer by one rigid translation and rotation to the first configuration of this production segment, and then measures positional differences. Its mean in the later interval is about 0.0846 nm. Membrane geometry and local protein change thus have separate observables, while temperature records their common thermal environment.

### Membrane geometry and protein motion

Actual 0–200 ps record; shading marks the 100–200 ps statistics interval.

Official prepared 1MAL/POPC model: 138195 atoms, three 421-residue protein chains and 277 POPC. Archived CHARMM parameters, 300 K and semiisotropic 1 bar; 20 ps pilot followed by 200 ps production, coordinates every 1 ps.

[Download reference data and complete inputs (ZIP) 110.85 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-membrane-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g13/en/#en-s5)

Projected area, phosphate-plane separation and aligned trimer Cα RMSD in the same 0–200 ps trajectory; shading marks the 100–200 ps analysis window.

Dividing 139.065 nm² by the 137 upper-leaflet lipids gives about 1.015 nm². This arithmetic distributes the protein’s occupied area among the lipids as well, so the quotient is total projected area apportioned by lipid count. For a planar pure-lipid bilayer, leaflet area divided by its lipid count is often a useful mean molecular area. A protein-containing membrane additionally requires a definition of protein cross-section and lipid-accessible area. Protein cross-section can vary with height, and nearby lipids can have different local areas. The subtraction method therefore belongs to the scientific analysis. The following interaction illustrates the distinction using a geometrical model with a specified protein footprint.

How a protein footprint changes area allocationEq. 4

![How a protein footprint changes area allocation](https://ml-biomat.com/static/agent-math/7b7bd4af48baa5ee0ef32051.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| aℓ | Lipid-accessible leaflet area per lipid for the specified protein footprint | nm² |
| atotal,ℓ | Total projected box area apportioned by that leaflet lipid count | nm² |
| A | Projected box area in the membrane plane | nm² |
| Aprot,ℓ | Protein footprint under the chosen height and geometrical definition | nm² |
| Nℓ | Number of lipids in the chosen leaflet | 1 |
| ℓ, prot, total | Leaflet label; protein footprint; total-area label | 1 |
| =, ×, /, −, + | Equality, multiplication, division, subtraction and addition; adjacent quantities multiply | 1 |

Reading the relationshipSubtract the protein footprint defined in the same plane, then distribute the remaining area among lipids.

A worked exampleGeometrical example: A=100 nm², Aprot,ℓ=20 nm² and Nℓ=100 give aℓ=0.8 nm² and atotal,ℓ=1.0 nm².

ConditionsThe footprint requires an additional definition. The interaction supplies a geometrical footprint; trajectory results report total projected area and actual leaflet counts.

[Figure: Geometrical area allocation for a specified protein footprint](https://ml-biomat.com/tutorials/molecular-dynamics/g13/en/#en-s5)

Planar geometry with a specified protein footprint: compare total-area allocation with allocation after subtracting the occupied area.

## Slice the membrane to reveal molecular layering

To ask what occupies the middle of the membrane, divide the box into thin slabs along z. Within each slab, sum the atomic masses of protein, lipid, water and ions separately, then divide each sum by the slab volume. This gives the component mass densities. It resembles taking successive slices through a layered cake, except that each slab here is 0.1 nm thick and its molecules continue to move. Repeating the count over many frames gives the mean distribution within the observation interval. Water-rich outer regions, a lipid-rich centre and protein extending across interfaces then appear in one common coordinate system.

Normalize each slab before averaging over timeEq. 5

![Normalize each slab before averaging over time](https://ml-biomat.com/static/agent-math/a1aaec612369a18c2bb27e89.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ρ̄b | Time-averaged mass density in slab b | kg m⁻³ |
| M, t | Saved-frame count and frame index | 1 |
| b(t), i∈b(t) | Atoms in the relative-height slab at frame t, and an atom belonging to that set | 1 |
| mᵢ | Mass of atom i, expressed in kg in this SI formula | kg |
| Aₜ | Projected box area at frame t, expressed in m² in SI | m² |
| Δz | Fixed slab thickness, expressed in m in SI | m |
| Σ, /, =, 1 | Summation, division, equality and constant one; adjacent quantities multiply | 1 |
| b, Δ, ¯ | Slab label, width marker and averaging mark | 1 |

Reading the relationshipDensity is mass divided by volume. The slab volume is that frame’s area times thickness; average the frame densities afterward.

A worked exampleA slab containing 3,000 u with area 140 nm² and width 0.1 nm has density (3000/14)×1.660539=355.830 kg m⁻³. Here 1 u=1.66053906660×10⁻²⁷ kg and 1 nm³=10⁻²⁷ m³.

ConditionsAlign each frame using the same midplane definition and normalize by its own volume; suitable for the changing orthogonal box used here.

Each frame is aligned to the membrane midplane before relative heights are placed into fixed-width bins. Translation of the entire membrane is consequently separated from broadening of its interfaces. Meanwhile the NPT box area changes, so every slab uses that frame’s lateral area multiplied by 0.1 nm for its volume, rather than retaining the first frame’s volume. The plotted range extends from −4.5 to 4.5 nm relative to the midplane and lies within half the box height in every frame. The program normalizes each frame’s mass counts before averaging the 101 configurations between 100 and 200 ps. This sequence specifies exactly what is meant by mean density.

### Mass density and headgroup positions

Relative to the periodic midplane in fixed 0.1 nm slabs; average of 101 frames over 100–200 ps.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g13/en/#en-s6)

Frames are centered on the periodic membrane midplane. Mass in 0.1 nm slabs is normalized by each frame’s projected area and slab width, then averaged over 101 frames.

Water mass density is near one thousand kilograms per cubic metre outside the membrane and falls substantially toward its interior. The protein profile crosses the membrane centre and extends further into water on one side, reflecting the channel’s spatial asymmetry. A small water density remains near the centre. Interpreting it requires the three-dimensional geometry: averaging over the entire lateral area places water inside a channel and water near lipid regions into the same slab. To locate water in individual pores, restrict the spatial selection around a channel or examine a two-dimensional lateral map. A one-dimensional profile organizes the data while combining information from different lateral positions.

The right panel counts phosphorus atoms and divides by slab volume, giving number density in atoms per cubic nanometre. These atoms mark the lipid headgroups and produce two separated peaks. Peak width reflects the spread of headgroup heights, local surface variation and changes over time. The two heights need not match because leaflet populations and molecular environments can differ. Number density and mass density use different weights, so their vertical values should not be compared directly. Their common spatial coordinate is useful: examine which components occur at the same height and how the phosphorus peaks relate to the phosphate-plane separation.

Profiles can also help define a subsequent question. If an added molecule occupies the water–headgroup region, examine interfacial residence and contacts. If it enters the hydrophobic region, measure penetration depth, orientation and nearby lipid organization. For strongly curved membranes or large undulations, a global z profile combines regions with different local heights; a local midplane and local normal then provide more appropriate coordinates. The planar system and short record used here offer a clear starting point for global analysis. Spatial resolution can subsequently be increased to distinguish the particular interface, pore or neighbourhood relevant to the research question.

## How do the tails orient, and what does one angle leave out?

POPC has two chemically different tails: an eighteen-carbon oleoyl chain with a cis double bond and a saturated sixteen-carbon palmitoyl chain. The double bond restricts neighbouring geometry, giving local conformations different from those available to a saturated chain. The full tail also responds to adjacent lipids, protein and thermal motion. Identify these chemical differences before discussing which part bends or which tail tilts. Drawing both tails as equal straight lines is useful for recognizing a bilayer, while the actual molecule contains additional structural detail that matters when connecting chemistry with conformational distributions.

We use a readily interpreted whole-tail measure of direction. Draw an arrow from the carbonyl carbon to the terminal carbon and measure its angle to z. An arrow close to the normal indicates that the tail extends inward in that overall sense; an arrow closer to the membrane plane indicates a more tilted axis. Upper- and lower-leaflet tails point in opposite directions, so directly averaging a signed cosine would make their contributions cancel. Squaring the cosine and applying a simple shift and scaling gives parallel and antiparallel axes the same value while assigning a zero average to uniformly distributed three-dimensional directions.

Whole-tail axis orientation relative to the normalEq. 6

![Whole-tail axis orientation relative to the normal](https://ml-biomat.com/static/agent-math/1c1e99943c77eda7ae0a4d6a.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| S | Mean chain-axis order in the current frame | 1 |
| N, i | Number of tail axes and chain index | 1 |
| θᵢ | Angle of the carbonyl-to-terminal-carbon vector to z | rad; worked examples use ° |
| cos, ² | Cosine; square the cosine value | 1 |
| Σ | Sum the individual chain-axis values | 1 |
| 1, 2, 3 | Constants setting normal alignment to 1 and the isotropic mean to 0 | 1 |
| =, ×, /, −, + | Equality, multiplication, division, subtraction and addition; adjacent quantities multiply | 1 |

Reading the relationshipSquaring treats opposite leaflet directions equally; isotropic directions have mean cos²=1/3 and therefore mean S=0.

A worked exampleIf every axis has θ=60°, cosθ=0.5 and S=(3×0.25−1)/2=−0.125. Angles 0° or 180° give S=1, while 90° gives S=−0.5.

ConditionsMeasures whole-tail end-to-end axes; segmental C–H order parameters require selecting those bond vectors.

This order parameter equals one for an axis along the normal and minus one half for an axis entirely within the membrane plane. Its zero reference has a geometrical explanation. For directions uniformly distributed in three dimensions, the mean squared direction cosine is the same along all three coordinate axes. The three squared cosines sum to one, so each mean is one third. Substitution into the formula gives zero. Particular mixtures of a few directions can also yield zero, which is why an angular histogram can complement the average. One order parameter compresses many directions into a convenient comparison, while their full distribution retains additional structure.

### Tail-axis order and pressure fluctuations

Each tail-type order averages over 277 axes per frame; pressure comes from the native energy record.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g13/en/#en-s7)

Second-order orientation of carbonyl-to-terminal-carbon axes relative to the membrane normal, together with instantaneous pressure from native energy records.

Over the later half of the record, the mean oleoyl-axis order is 0.5295 and the mean palmitoyl-axis order is 0.5449. Their sample standard deviations across frame means are 0.0068 and 0.0063. Each frame first averages over 277 lipids, and the reported statistics then use 101 frames. These values describe whole-tail end-to-end axes relative to the membrane normal. A segmental deuterium order parameter instead uses specified carbon–hydrogen bond directions. Comparison with an NMR chain-order measurement requires selecting corresponding C–H vectors and matching the angular, averaging and sign conventions at each carbon position. Matching definitions establishes a common observable for the comparison.

Similar mean axis orders do not make the two tails structurally identical. They can bend at different positions, have different end-to-end lengths, or reach similar overall directions through different local conformations. Likewise, nearly constant membrane thickness can coexist with rapid local conformational exchange, and a temperature fluctuating around its target can accompany slower lateral rearrangement. Read orientation, thickness, density and three-dimensional structure together to separate these motions. The 200 ps record describes local organization near the prepared state. Questions about long-term lateral diffusion or lipid rearrangement call for displacement records and independent repeats spanning the relevant longer times.

The order of calculation matters: evaluate the squared cosine for each chain and then average over chains. Suppose half the arrows point upward and half downward. Their vector average is zero, yet every arrow is aligned with the membrane normal, so the present order parameter is one. Averaging angles first and then squaring their cosine also generally gives a different answer from averaging the individual squared cosines. The program retains chain identities, constructs each direction in a frame, and then forms a frame mean. This example illustrates why nonlinear geometrical operations and averaging cannot usually be exchanged.

## Connect the structure, curves and complete analysis

The program reads atom names, masses, residues and chemical bonds from the same topology before processing the trajectory frame by frame. It reconstructs molecules by following their specified bonds and checks every reconstructed covalent-bond length. For the trimer, individual protein chains are restored first, then placed in neighbouring periodic images before a single overall Cα alignment. For lipids, one checked POPC bond graph supports batched reconstruction of all 277 molecules. This separates the displayed boundary from internal molecular geometry. Thickness, tail orientation and protein RMSD can then use coordinate representations suited to their different definitions while retaining the same underlying trajectory.

### Complete membrane geometry, density and orientation analysis

```
"""Measure a membrane-protein trajectory in its membrane coordinate frame.

python analyze_membrane.py --records records --out analysis --language en
Inputs: md.tpr, md.xtc, md-properties.xvg. Dependencies: MDAnalysis, NumPy,
Matplotlib. Coordinates are converted from angstrom to nm explicitly.
"""
from pathlib import Path
import argparse
import csv
import json
import re
import numpy as np
import MDAnalysis as mda
from MDAnalysis.lib.distances import minimize_vectors
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


def xvg(path):
    legends = {}
    rows = []
    for line in path.read_text().splitlines():
        found = re.search(r'@\s+s(\d+)\s+legend\s+"([^"]+)"', line)
        if found:
            legends[int(found[1])] = found[2]
        if line.strip() and not line.startswith(("@", "#")):
            rows.append([float(x) for x in line.split()])
    values = np.asarray(rows)
    return {"time": values[:, 0], **{label: values[:, i+1] for i, label in legends.items()}}


def bond_plan(group):
    local = {int(x): i for i, x in enumerate(group.indices)}
    edges = np.asarray([[local[int(a)], local[int(b)]] for a, b in group.bonds.indices])
    graph = [[] for _ in group]
    for k, (a, b) in enumerate(edges):
        graph[a].append((b, k, 1)); graph[b].append((a, k, -1))
    queue, seen, plan = [0], {0}, []
    for a in queue:
        for b, k, sign in graph[a]:
            if b not in seen:
                seen.add(b); queue.append(b); plan.append((a, b, k, sign))
    if len(seen) != len(group):
        raise ValueError("A molecule selection must have one connected bond graph")
    return edges, plan


def restore_batch(raw, edges, plan, box):
    """Traverse every bond; raw has shape (molecules, atoms, 3), in angstrom."""
    vectors = raw[:, edges[:, 1]] - raw[:, edges[:, 0]]
    vectors = minimize_vectors(vectors.reshape(-1, 3), box).reshape(vectors.shape)
    whole = np.empty_like(raw, dtype=float)
    whole[:, 0] = raw[:, 0]
    for parent, child, k, sign in plan:
        whole[:, child] = whole[:, parent] + sign*vectors[:, k]
    actual = whole[:, edges[:, 1]] - whole[:, edges[:, 0]]
    if np.max(np.linalg.norm(actual-vectors, axis=2)) > .005:
        raise ValueError("Bond-cycle reconstruction differs by more than 0.005 angstrom")
    maximum = np.linalg.norm(actual, axis=2).max()/10
    if maximum > .25:
        raise ValueError("A reconstructed covalent bond exceeds 0.25 nm")
    return whole/10, float(maximum)


def circular_center(z, length):
    phase = np.mean(np.exp(2j*np.pi*z/length))
    if abs(phase) < .2:
        raise ValueError("Tail markers do not define one localized membrane midplane")
    return float(np.angle(phase)*length/(2*np.pi) % length)


def wrap(dz, length):
    return (dz+length/2) % length-length/2


def fit_rmsd(moving, reference):
    moving = moving-moving.mean(axis=0)
    target = reference-reference.mean(axis=0)
    left, _, right = np.linalg.svd(moving.T@target)
    correction = np.eye(3); correction[-1, -1] = np.linalg.det(left@right)
    return float(np.sqrt(np.mean(np.sum((moving@left@correction@right-target)**2, axis=1))))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, default=Path("records"))
    parser.add_argument("--out", type=Path, default=Path("analysis"))
    parser.add_argument("--language", choices=["zh", "en"], default="en")
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    u = mda.Universe(str(args.records/"md.tpr"), str(args.records/"md.xtc"))
    lipid = u.select_atoms("resname POPC")
    groups = [u.select_atoms(s) for s in ["protein", "resname POPC", "resname TIP3", "resname SOD CLA"]]
    assert [len(x) for x in groups] == [19260, 37118, 81612, 205]
    residues = lipid.residues
    assert len(residues) == 277 and all(len(r.atoms) == 134 for r in residues)
    edges, plan = bond_plan(residues[0].atoms)
    for residue in residues:
        assert np.array_equal(bond_plan(residue.atoms)[0], edges)
    names = residues[0].atoms.names.tolist()
    P, tail1, tail2, start1, start2 = [names.index(n) for n in ["P", "C218", "C316", "C21", "C31"]]
    protein_segments = groups[0].segments
    protein_plans = [bond_plan(s.atoms) for s in protein_segments]
    ca_local = [np.flatnonzero(s.atoms.names == "CA") for s in protein_segments]
    bins = np.linspace(-4.5, 4.5, 91)
    mass_profiles = np.zeros((4, 90))
    phosphate_profile = np.zeros(90)
    records = []; late_frames = 0; maximum_bond = 0.
    for frame, ts in enumerate(u.trajectory):
        box_nm = ts.dimensions[:3]/10
        if not np.allclose(ts.dimensions[3:], 90) or box_nm[2]/2 < 4.5:
            raise ValueError("This analysis expects an orthogonal box with Lz >= 9 nm")
        whole, longest = restore_batch(lipid.positions.astype(float).reshape(277, 134, 3), edges, plan, ts.dimensions)
        maximum_bond = max(maximum_bond, longest)
        z0 = circular_center(whole[:, [tail1, tail2], 2].ravel(), box_nm[2])
        pz = wrap(whole[:, P, 2]-z0, box_nm[2])
        if frame == 0:
            upper = pz > 0
        if np.any((pz > 0) != upper):
            raise ValueError("A phosphate changes assigned leaflet; inspect that event")
        thickness = pz[upper].mean()-pz[~upper].mean()
        order = []
        for start, end in [(start1, tail1), (start2, tail2)]:
            v = whole[:, end]-whole[:, start]
            cos = v[:, 2]/np.linalg.norm(v, axis=1)
            order.append(float(np.mean((3*cos*cos-1)/2)))
        cas = []
        for segment, (pe, pp), indices in zip(protein_segments, protein_plans, ca_local):
            protein, longest = restore_batch(segment.atoms.positions.astype(float)[None], pe, pp, ts.dimensions)
            maximum_bond = max(maximum_bond, longest)
            ca = protein[0, indices]
            if cas:
                ca -= np.rint((ca.mean(axis=0)-cas[0].mean(axis=0))/box_nm)*box_nm
            cas.append(ca)
        ca = np.concatenate(cas)
        if frame == 0:
            reference = ca.copy()
            snapshot = {"box_nm": box_nm.tolist(), "ca_nm": ca.tolist(),
                        "lipid_P_nm": whole[:, P].tolist(),
                        "lipid_tail_nm": whole[:, [tail1, tail2]].tolist(),
                        "midplane_nm": z0, "upper_leaflet": upper.tolist()}
        records.append([float(ts.time), float(box_nm[0]*box_nm[1]), float(box_nm[2]),
                        float(thickness), order[0], order[1], fit_rmsd(ca, reference)])
        if ts.time >= 100:
            late_frames += 1
            volume_slice = box_nm[0]*box_nm[1]*(bins[1]-bins[0])
            for k, group in enumerate(groups):
                z = wrap(group.positions[:, 2]/10-z0, box_nm[2])
                mass_profiles[k] += np.histogram(z, bins, weights=group.masses)[0]/volume_slice*1.66053906660
            phosphate_profile += np.histogram(pz, bins)[0]/volume_slice
    a = np.asarray(records)
    assert len(a) == 201 and np.allclose(a[:, 0], np.arange(201)) and late_frames == 101
    mass_profiles /= late_frames; phosphate_profile /= late_frames
    columns = ["time_ps", "projected_area_nm2", "Lz_nm", "phosphate_plane_distance_nm",
               "oleoyl_axis_order", "palmitoyl_axis_order", "trimer_CA_RMSD_nm"]
    with (args.out/"membrane_observations.csv").open("w", encoding="utf8", newline="") as handle:
        writer = csv.writer(handle); writer.writerow(columns); writer.writerows(records)
    energy = xvg(args.records/"md-properties.xvg")
    stats = lambda v: {"mean": float(np.mean(v)), "frame_sd": float(np.std(v, ddof=1))}
    summary = {"frames": len(a), "time_ps": [0, 200], "profile_frames": late_frames,
               "leaflet_counts": {"upper": int(sum(upper)), "lower": int(sum(~upper))},
               "late_100_200ps": {key: stats(a[a[:, 0] >= 100, i]) for i, key in enumerate(columns) if i},
               "energy_100_200ps": {key: stats(v[energy["time"] >= 100]) for key, v in energy.items() if key != "time"},
               "maximum_reconstructed_bond_nm": maximum_bond,
               "density_definition": "Mass in fixed 0.1 nm slabs divided by instantaneous xy area times slab width; mean over 101 frames. Window -4.5 to4.5 nm about circular tail-terminal midplane.",
               "orientation_definition": "P2 of each carbonyl-carbon to terminal-carbon chain axis versus z; distinct from segmental C-H deuterium order.",
               "rmsd_definition": "All 1263 C-alpha atoms, equal weights, one proper rigid fit to first local production frame."}
    (args.out/"membrane_summary.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf8")
    (args.out/"membrane_snapshot.json").write_text(json.dumps(snapshot)+"\n", encoding="utf8")
    np.savez(args.out/"membrane_profiles.npz", z_nm=(bins[1:]+bins[:-1])/2,
             mass_density_kg_m3=mass_profiles, phosphate_number_density_nm3=phosphate_profile)
    tr = lambda zh, en: zh if args.language == "zh" else en
    installed = {f.name for f in font_manager.fontManager.ttflist}
    fonts = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"]
    plt.rcParams.update({"font.family": [f for f in fonts if f in installed] if args.language == "zh" else ["DejaVu Sans"],
                         "font.size": 14, "svg.fonttype": "path", "axes.spines.top": False, "axes.spines.right": False,
                         "figure.facecolor": "#faf8f2", "axes.facecolor": "#faf8f2"})
    colors = ["#995a42", "#177e89", "#537dbb", "#9067a0"]
    def save(fig, name):
        fig.savefig(args.out/f"{name}.svg"); fig.savefig(args.out/f"{name}.png", dpi=150); plt.close(fig)
    fig, axes = plt.subplots(2, 2, figsize=(13, 8), constrained_layout=True)
    for ax, i, label in zip(axes.flat, [1, 3, 6], [tr("盒投影面积 / nm²", "Projected box area / nm²"),
                           tr("磷酸平面间距 / nm", "Phosphate-plane distance / nm"), tr("三聚体 Cα RMSD / nm", "Trimer Cα RMSD / nm")]):
        ax.plot(a[:, 0], a[:, i], color=colors[i % 4]); ax.set_ylabel(label)
    axes[1, 1].plot(energy["time"], energy["Temperature"], color=colors[2], lw=.8)
    axes[1, 1].axhline(300, color="#777", ls="--", lw=1); axes[1, 1].set_ylabel(tr("温度 / K", "Temperature / K"))
    for ax in axes.flat:
        ax.set_xlabel(tr("本段记录时间 / ps", "Local production time / ps")); ax.axvspan(100, 200, color="#e2e9dc", alpha=.4); ax.grid(alpha=.15)
    fig.suptitle(tr("膜、蛋白与水共同运动：0–200 ps", "Membrane, protein and water: 0–200 ps"), fontsize=19)
    save(fig, "membrane-geometry")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.8), constrained_layout=True)
    z = (bins[1:]+bins[:-1])/2
    for density, color, label in zip(mass_profiles, colors, [tr("蛋白", "Protein"), "POPC", tr("水", "Water"), tr("离子", "Ions")]):
        axes[0].plot(z, density, color=color, label=label, lw=2)
    axes[1].plot(z, phosphate_profile, color=colors[1], lw=2)
    axes[0].set_ylabel(tr("质量密度 / kg m⁻³", "Mass density / kg m⁻³")); axes[0].legend(frameon=False)
    axes[1].set_ylabel(tr("磷原子数密度 / nm⁻³", "Phosphorus number density / nm⁻³"))
    for ax in axes:
        ax.set_xlabel(tr("相对膜中面的位置 / nm", "Position relative to membrane midplane / nm")); ax.axvline(0, color="#888", ls=":"); ax.grid(alpha=.15)
    fig.suptitle(tr("沿膜法线切薄片：100–200 ps 的平均分布", "Slices along the membrane normal: mean over 100–200 ps"), fontsize=18)
    save(fig, "membrane-profiles")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.8), constrained_layout=True)
    for i, label, color in [(4, tr("油酰链端到端轴", "Oleoyl chain axis"), colors[0]), (5, tr("棕榈酰链端到端轴", "Palmitoyl chain axis"), colors[1])]:
        axes[0].plot(a[:, 0], a[:, i], color=color, label=label, lw=1.5)
    axes[0].set(xlabel=tr("本段记录时间 / ps", "Local production time / ps"), ylabel=tr("链轴取向参数 S", "Chain-axis order S")); axes[0].legend(frameon=False, fontsize=11)
    axes[1].plot(energy["time"], energy["Pressure"], color=colors[3], lw=.8)
    axes[1].axhline(1, color="#777", ls="--"); axes[1].set(xlabel=tr("本段记录时间 / ps", "Local production time / ps"), ylabel=tr("瞬时平均压力 / bar", "Instantaneous mean pressure / bar"))
    for ax in axes: ax.grid(alpha=.15)
    fig.suptitle(tr("局部取向与整体热力学量的不同变化", "Local orientation and a fluctuating thermodynamic observable"), fontsize=18)
    save(fig, "membrane-orientation")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

Read md.tpr, md.xtc and md-properties.xvg; write three figure groups and framewise data.

Outputs include three figure groups, a frame-by-frame CSV table, a numerical summary and density arrays. The geometry figure contains projected area, headgroup separation, protein RMSD and temperature. The profile figure separates mass density from phosphorus number density. The orientation figure retains both tail types beside the pressure trace. Shading in the geometry figure marks the 100–200 ps statistics window. Energy records are saved every 0.2 ps and coordinates every 1 ps, so their sample counts differ even over the same physical interval. The program selects records by actual time in each file, avoiding the assumption that a shared row number means a shared instant.

Two small changes make useful further exercises. Increasing density-bin width from 0.1 to 0.2 nm generally smooths peaks while merging spatial detail. Using the first hundred picoseconds instead of the later interval shows whether the geometry and distributions change across this short record. These modifications alter the analysis while retaining the same trajectory. State the new bin width, time window and atom selections before comparing the resulting figures, then identify which part of the measurement caused each difference. A smoother line can result from coarser spatial averaging; its appearance alone does not establish that the underlying molecular motion became more stable.

Returning to biomaterials, a membrane’s behaviour depends on the organization of several molecular components. Lipids connect aqueous surroundings with a hydrophobic interior, proteins occupy local space and provide channels, and ions respond to the environment around charged atoms. The example lets these components move within one model and uses explicit geometrical and statistical definitions to examine their positions and changes. For a new formulation, keep temperature, parameter compatibility, protein chemical states and analysis definitions consistent, then deliberately alter one lipid type or added molecule. Independent repeats help relate observed differences to that chosen chemical change rather than to one starting configuration.

The next polymer lesson follows a chain extending and coiling in water. Later we will attach polymers to membranes and examine how grafting density changes organization outside the interface. The coordinate habits established here will remain useful: locate the midplane and outward direction before measuring chain height, and retain actual leaflet populations and area before calculating grafting density on each side. Carrying those definitions across the examples brings membrane, polymer and water into one coherent, computable picture of an interface, with each new measurement tied to a specific molecular question.

## Further Reading and Open Materials

- [A Beginner’s Guide to Perform Molecular Dynamics Simulation of a Membrane Protein using GROMACS](https://tutorials.gromacs.org/docs/membrane-protein.html) · Farzaneh Jalalypour, Maryam Majdolhosseini, Alessandra Villa · CC BY 4.0; archived tutorial and supplied inputs

  1MAL/POPC model, complete CHARMM topology, staged preparation and revised production settings.

  Continue from the public final preparation state with GROMACS 2026.4 for a 20 ps pilot and 200 ps record; add leaflet, area, density and orientation analysis and bilingual explanations.
- [1MAL: Structural basis for sugar translocation through maltoporin channels](https://www.rcsb.org/structure/1MAL) · T. Schirmer, T. A. Keller, Y. F. Wang, J. P. Rosenbusch · PDB structural data: CC0; original article cited for scientific context

  Trimer structure identity, 3.10 Å resolution and channel context.

  Use the prepared membrane model; structure diagrams show the actual local record.
- [On bimolecular layers of lipoids on the chromocytes of the blood (1925)](https://doi.org/10.1084/jem.41.4.439) · E. Gorter and F. Grendel · Historical article citation; new conceptual illustration

  Historical comparison of lipid-monolayer area with cell surface area.

  Explain the reasoning through molecule counts and covered-area geometry.
- [The fluid mosaic model of the structure of cell membranes (1972)](https://doi.org/10.1126/science.175.4023.720) · S. J. Singer and G. L. Nicolson · Research citation; independently drawn conceptual diagram

  Historical view of proteins organized within a fluid lipid environment.

  Connect the view to an embedded protein and local lipid organization.
- [GROMACS 2026.4: gmx density](https://manual.gromacs.org/2026.4/onlinehelp/gmx-density.html) · GROMACS development team · Official documentation citation

  Membrane-centred density and effects of periodic boundaries and box fluctuations.

  Provide a full Python implementation with fixed-width slabs and framewise volume normalization.
