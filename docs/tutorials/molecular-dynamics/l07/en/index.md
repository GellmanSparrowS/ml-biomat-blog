# The Shape and Motion of a Polymer Chain

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l07/en/
Language: en

Distinguish endpoint, contour, and whole-chain size in an actual PEG trajectory, follow the response to constant forces, and calculate work from endpoint displacements.

## How do we measure a flexible molecular linker?

Lay a shoelace on a table and arrange it as a straight line, a curved arc, or a loose coil. The lace itself has not become shorter, yet the straight-line separation between its ends has changed. A polymer chain has analogous geometric freedom: the same connectivity can support many spatial shapes in water. This flexibility allows polymers to act as molecular linkers and spacers. A linker can accommodate changes in the separation of the objects it connects, while a chain attached to a surface occupies space around that surface. Both applications concern molecular size, but the most useful definition of “size” depends on the question.

We return to the short PEG chain previously inserted into water. It has eight ethylene oxide repeat units, the formula C₁₆H₃₄O₉, and 59 explicit atoms, surrounded by 670 flexible SPC/Fw waters. First we observe changes in shape without an externally applied pulling force. We then apply equal and opposite constant forces along x to the two terminal oxygen atoms. Four measurements follow the same trajectory: terminal separation, its projection onto the pulling direction, backbone contour length, and mass-weighted radius of gyration. Comparing them reveals the difference between turning the whole molecule, bending it locally, and extending its spatial arrangement.

Motion has several levels here. The entire chain can translate through water, rotate without changing its internal shape, or change conformation through bond-angle and dihedral motion. A camera that follows the chain removes overall translation from the picture while leaving internal changes visible. The present input translates PEG and its surrounding water together to keep the chain centred, making it suitable for studying relative geometry and internal conformation. Our analysis therefore concentrates on those internal measurements. A later study of diffusion in a laboratory frame would use records retaining overall displacement and the appropriate periodic unwrapping, matching the coordinate record to the motion being measured.

Water participates throughout the motion. When a chain segment turns, nearby waters may leave and new ones approach, changing local interactions. Collisions with water also continually alter atomic velocities along the chain. The chain therefore does not remain in one particularly tidy conformation even without an applied pulling force. A fixed temperature sets a thermal energy scale rather than prescribing the same shape in every frame. A flexible thread continually changing posture in water is closer to this model than a motionless spring in a vacuum. Size fluctuations should first be treated as motion to characterize statistically, followed by checks for ongoing preparation or a systematic response to forcing.

The length and time scales are easy to translate. One ångström is 0.1 nm, and the terminal separation in this example ranges from a few ångströms to roughly 30 Å, a scale of only a few nanometres. One picosecond is 1,000 femtoseconds. The time step is 1 fs and each of the two observation stages lasts 15 ps. A short chain over these windows is sufficient to demonstrate force application, conformational measurements, and interpretation of changes. Describing the average dimensions, slow relaxation, or experimental force spectrum of longer polymers adds chain-length coverage, longer sampling, and independent repeats. Precise definitions in this small example establish the basis for those comparisons.

## Why one chain needs many pictures: from connectivity to conformational statistics

Once macromolecules are understood as covalently connected chains, another question follows: what shapes do those chains usually adopt in space? A chemical formula identifies atoms and a connectivity table identifies neighbours, but neither fixes one unique three-dimensional arrangement. Rotation near single bonds, variations in bond angles, and repulsion between atoms allow many conformations of the same molecular graph. Representing all of them by one picture would resemble describing a season using one weather snapshot. We need the instantaneous shape, the frequency with which different shapes occur, and the time required to move between them.

Paul Flory chose the spatial configuration of macromolecular chains as the theme of his 1974 Nobel lecture, connecting chemical architecture with the rich range of spatial arrangements available to a chain. That perspective extends molecular structure from a static structural formula to an ensemble of conformations. The historical concept drawing below keeps the connection order unchanged while bending the chain in different places. Each image represents another arrangement of the same connectivity. The accompanying distribution emphasizes that an average size arises from the weights of many conformations. Before averaging, we must identify which conformations were collected, under what conditions, and how the observations are counted.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l07/en/#en-s2)

Figure 1 · Historical concept drawing from static connectivity to a conformational ensemble; the distribution illustrates the statistical viewpoint.

A flexible chain generally has many bent arrangements, whereas arrangements close to full extension face stronger geometric restrictions. Imagine connected short rods whose directions can vary. Allowing each rod many directions creates many combinations; requiring all of them to point together sharply reduces the available combinations. This relates to conformational entropy, which concerns the multiplicity of accessible arrangements. Pulling changes their statistical weights, so a restoring tendency need not arise primarily from strongly stretching every chemical bond like a metal spring. For a particular molecule, torsional energies, excluded contacts, and solvent reorganization also contribute to the response.

PEG in water is particularly useful for understanding the solvent’s role. The single-molecule force-spectroscopy and simulation study by Liese and colleagues examined how hydration participates in the response of strongly stretched PEG, illustrating the coupling between chain conformation and nearby water. The present example develops the modelling and measurement steps needed to investigate such questions: the same chain first moves in water without an applied pulling force and then experiences a constant force, allowing its geometry to be compared. We retain the supplied PEG/SPC/Fw parameter combination and distinguish its short-time response from equilibrium statistics. Resolving energetic and entropic hydration contributions adds solvent analysis, sampling across conditions, and the corresponding thermodynamic calculations.

## What terminal distance, projection, and contour length measure

First define the endpoints precisely. The applied forces act on the oxygen atoms in the terminal hydroxyl groups, identified by the OAlc atom type. These endpoints are neither water oxygens nor the hydrogens of the terminal hydroxyl groups. Subtract the left endpoint position from the right endpoint position to obtain the end-to-end vector. The vector retains direction, while its magnitude is the straight-line terminal distance. Its x component is the projection along the pulling axis. Distance is nonnegative; the projection can have either sign according to endpoint ordering and axis direction. The analysis determines endpoint identities in the first frame and follows that same pair throughout.

End-to-end vector, distance, and projection along the forceEq. 1

![End-to-end vector, distance, and projection along the force](https://ml-biomat.com/static/agent-math/d263004afb198becaf6a3559.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| rR, rL | Position vectors of the fixed right and left terminal oxygens | Å |
| R | End-to-end vector pointing from left to right | Å |
| Re | Magnitude of the end-to-end vector, the straight-line endpoint distance | Å |
| Rx, Ry, Rz, X | Vector components and the signed projection along the x force axis | Å |
| R, L, e, x, y, z | Subscripts identify right, left, endpoint distance, and coordinate directions | 1 |
| −, \|…\|, √, ², +, = | Subtract positions for displacement; bars denote magnitude; square components, add, and take the nonnegative square root; equalities connect definitions | 1 |

Reading the relationshipSquared components along three orthogonal directions add to the squared three-dimensional distance; a projection retains one component.

A worked exampleFor R = (3, 4, 0) Å, Re = √(9 + 16) = 5 Å and X = 3 Å. Rotation onto x can give X = 5 Å while preserving Re.

ConditionsUse unwrapped positions of the same terminal oxygen pair throughout the trajectory.

If the end-to-end vector is (3, 4, 0) Å, its magnitude is 5 Å but its x projection is only 3 Å. Rotating the whole chain toward x without changing its internal shape can increase that projection to 5 Å while the terminal distance remains 5 Å. This simple example shows why an increasing x extent should be checked for whole-chain reorientation. In the actual trajectory, the terminal distance and x projection approach one another after the force is applied, indicating alignment of the end-to-end direction with the pulling axis. Their simultaneous increase additionally shows that the endpoints move farther apart. Plotting both quantities gives a fuller interpretation than one coordinate difference alone.

Sum a specified backbone path to obtain contour lengthEq. 2

![Sum a specified backbone path to obtain contour length](https://ml-biomat.com/static/agent-math/316255eb74598990c876772f.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Lc | Total length along the covalent path between terminal oxygens | Å |
| ra, rₐ₊₁ | Position vectors of neighbouring atoms along that path | Å |
| Nb, a | Number of path bonds and bond index | 1 |
| Re | Straight-line distance between the same endpoints | Å |
| Σ, \|…\|, −, +, ≤, = | Sum segment lengths; bars take magnitude; subtract positions; a + 1 denotes the next point; straight distance is no larger than path length; equality defines | 1 |

Reading the relationshipAccumulate actual segment lengths along the bent route; the triangle inequality bounds the endpoint separation.

A worked exampleTwo perpendicular segments of length 1 Å have contour length 2 Å and endpoint distance √2 Å, approximately 1.414 Å.

ConditionsThe example has a unique 25-atom, 24-bond backbone path; flexible bonds allow small contour-length variations.

Contour length instead follows the backbone one bond at a time. The program traces covalent connectivity from one terminal oxygen to the other, finding a path of 25 backbone atoms and 24 connections, and sums the actual bond lengths along that path. Side hydrogens are not all part of this endpoint-to-endpoint route and therefore do not contribute additional contour segments. Contour length resembles measuring along the shoelace, whereas terminal distance resembles placing a straight ruler between its ends. A polygonal path is at least as long as its straight-line endpoint separation, with equality requiring all segments to align. That geometric relationship also provides a useful analysis check.

Following a path and joining its endpoints are related through vector addition. Add the bond vectors head to tail: every intermediate atomic position appears once positively and once negatively, so it cancels, leaving the end-to-end vector. If each segment is first replaced by its positive length, the direction information is removed and their sum gives contour length. The two additions preserve different information and therefore produce different numbers. The PEG backbone route is uniquely determined by its connectivity here. A branched or cyclic molecule requires the chosen endpoints and chemical route to be stated before contour length has an equally clear meaning. The same principle will matter in a crosslinked network.

The mean backbone contour length is about 35.20 Å in the unforced window and 35.39 Å in the constant-force window. Meanwhile, the mean terminal distance increases from approximately 7.39 Å to 28.29 Å. The markedly different changes show that endpoint separation in this run is dominated by spatial rearrangement of an existing backbone path, rather than stretching each bond to several times its original length. Identifying individual dihedral changes and accompanying solvent rearrangement would add more detailed analyses. Contour length itself is not an immutable mathematical constant here: the bonds are flexible and fluctuate, so it is calculated from each actual frame and examined statistically.

Nearby endpoints do not imply that the entire chain has contracted into a small point. A long bent chain can bring its ends together while its middle extends far away; other folded arrangements may remain much more compact. Terminal distance is therefore especially useful for asking how far apart the two objects connected by a linker can be, but it omits the positions of the intervening atoms. To characterize the spatial spread of the whole chain, as when considering access by neighbouring molecules, we need a size measure using all its atoms. The radius of gyration provides such a measurement.

## Radius of gyration: including every atom in the size measurement

Begin the radius-of-gyration calculation by locating the chain’s centre of mass. Think of it as the balance point of the molecular mass distribution: heavier atoms influence it more strongly. Multiply every atomic position by its mass, add those weighted positions, and divide by total mass. Carbon, oxygen, and hydrogen have different masses in this model, so giving all 59 positions equal weight produces a geometric centroid that generally differs from the centre of mass. LAMMPS compute gyration uses mass weighting, and an independent calculation must use the same convention to reproduce its result.

Locate the chain centre of mass by mass weightingEq. 3

![Locate the chain centre of mass by mass weighting](https://ml-biomat.com/static/agent-math/efb9ee4e815e85ed580ab7a2.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| M, mi | Total chain molar mass and the molar mass assigned to atom i | g mol⁻¹ |
| ri, rcm | Position of atom i and the mass-weighted centre of mass | Å |
| N, i | Number of selected chain atoms and atom index | 1 |
| cm | Centre-of-mass subscript | 1 |
| Σ, /, ×, = | Sum masses or mass times position; divide by total mass; equality defines | 1 |

Reading the relationshipWeight each position by mass and divide by total mass so the weights sum to one.

A worked exampleFor positions 0 Å and 4 Å with mass ratio 1:3, the centre is (1 × 0 + 3 × 4)/4 = 3 Å.

ConditionsUse one consistent unwrapped coordinate representation and the corresponding carbon, oxygen, and hydrogen masses.

After locating the centre of mass, calculate each atom’s distance from it, square that distance, average with mass weights, and take the square root. Squaring makes contributions nonnegative in every direction and gives greater weight to atoms farther from the centre. The final square root returns the unit from length squared to length. The result is a root-mean-square scale of the mass distribution around its centre. It is not the radius of the smallest sphere enclosing all atoms; some atoms can lie farther away than this value. “Radius” here denotes an overall scale rather than a hard boundary containing the entire chain.

Root-mean-square spread of mass about the centreEq. 4

![Root-mean-square spread of mass about the centre](https://ml-biomat.com/static/agent-math/79cf2c37cc2dc098dd703113.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Rg | Mass-weighted radius of gyration | Å |
| Rg,x, Rg,y, Rg,z | Mass-weighted RMS size along each coordinate direction | Å |
| ri, rcm | Atomic and centre-of-mass position vectors | Å |
| mi, M | Atomic and total chain masses in a consistent unit | g mol⁻¹ |
| N, i | Atom count and summation index | 1 |
| g, x, y, z | g denotes gyration; x, y, z identify coordinate directions | 1 |
| Σ, −, \|…\|, ², √, /, ×, +, = | Subtract the centre, square the magnitude, sum with mass weights, divide by total mass, and take the square root; squared directional contributions add | 1 |

Reading the relationshipSquaring gives nonnegative contributions from deviations in every direction; the square root of the mass-weighted mean gives a length.

A worked exampleFor points at 0 Å and 4 Å with mass ratio 1:3 and centre at 3 Å, Rg = √[(1 × 9 + 3 × 1)/4] = √3 Å ≈ 1.732 Å.

ConditionsThe scalar is invariant to translation and rotation; directional sizes depend on the axes. This matches the LAMMPS mass-weighted definition.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l07/en/#en-s4)

Figure 2 · Contour, endpoints, and mass spread on one polygonal chain. The dashed circle has the radius of gyration of the equal-mass points; a cross marks the centre of mass.

Two points illustrate the effect of weighting. Put equal masses at 0 Å and 4 Å: their centre of mass is at 2 Å and their radius of gyration is 2 Å. Make the right mass three times the left mass: the centre moves to 3 Å and the mass-weighted radius becomes √3 Å, approximately 1.732 Å. The geometric separation is unchanged, but the spatial mass distribution has changed. For PEG, reading the atomic masses from the parameterized system gives a total molar mass of approximately 370.4426 g/mol. Its mass-weighted radius and a radius defined for equal-weight coarse-grained beads follow different measurement conventions, so a comparison should retain the weighting definition.

The calculation itself shows why translation leaves radius of gyration unchanged. Adding the same displacement to every atomic position adds that displacement to the centre of mass as well; subtracting the centre removes the common term. A rigid rotation preserves every atom’s distance from the centre, and consequently preserves the mass-weighted mean squared distance. These properties separate where a molecule is and how it points from how its internal mass distribution is spread. Although atomic masses are expressed in g/mol, using the same mass unit in numerator and denominator makes it cancel. The final radius therefore retains a length unit.

Geometric exercise: five points joined by four segments of 1 Å. Fold, rotate, or change the mass of point 5.

[Figure: Five-point chain geometry and centre of mass](https://ml-biomat.com/tutorials/molecular-dynamics/l07/en/#en-s4)

Each segment in the five-point geometric model has fixed length. The folding parameter controls alternating segment directions, rotation preserves scalar size, and the mass selection changes weighting.

The interactive exercise separates these geometric effects with a five-point chain. Changing its folding angle preserves the four segment lengths while changing terminal distance and radius of gyration. Rotating the entire chain preserves both scalar sizes while changing the x projection. Changing the last point’s mass moves the centre of mass and changes the mass-weighted radius while leaving endpoint separation unchanged. These operations reveal which features each measurement depends on. In the actual analysis, squared radius of gyration can also be decomposed into x, y, and z contributions. Their sum gives the total squared radius, while the square root of each component describes the directional root-mean-square size.

Periodic geometry also determines whether a size measurement is correct. A chain crossing a boundary appears split in wrapped coordinates, and a direct centre calculation may place it incorrectly near the middle of the box. The saved xu, yu, and zu coordinates are unwrapped using periodic-image information, preserving the chain’s continuity. Recalculating radius of gyration from them and comparing with LAMMPS gives a maximum difference of approximately 1.39 × 10⁻⁵ Å, consistent with finite coordinate-recording precision. This comparison checks atom selection, mass weighting, periodic geometry, and formula implementation together; mixing any of those conventions can produce a much larger discrepancy.

## Letting the same chain fluctuate before applying a defined constant force

The prepared merge.restart contains chain and solvent, coordinates, velocities, box dimensions, and interaction settings. The pulling input reads it, restores the long-range solver setting, and selects the two OAlc terminal oxygens. Their initial x positions determine which is right and which is left, creating two groups with fixed membership. Subsequent bending or rotation does not change which atoms receive the forces. The atom-style variables determine membership when the groups are created; the input does not reassign endpoints every step according to which is currently farther right. That detail keeps the force protocol consistent with the endpoint identities used in analysis.

### Complete two-stage chain-motion and constant-force input

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

kspace_style pppm 1e-5
read_restart merge.restart

group ends type OAlc
variable xcm equal xcm(ends,x)
variable oxies atom type==label2type(atom,OAlc)
variable end1 atom v_oxies*(x>v_xcm)
variable end2 atom v_oxies*(x<v_xcm)
group topull1 variable end1
group topull2 variable end2


timestep 1.0
fix mynvt all nvt temp 300 300 100
fix myrct PEG recenter 0 0 0 shift all

compute rgyr PEG gyration
compute dphi PEG dihedral/local phi

thermo_style custom step temp etotal c_rgyr
thermo 250

dump mydmp all local 50 pull.dat index c_dphi


# Numerical diagnostics; all energies are whole-system kcal/mol.
compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cPress all pressure cTemp
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE
variable K equal c_cKE
variable E equal c_cPE+c_cKE
variable P equal c_cPress
variable V equal vol
variable rho equal density
thermo_style custom step time c_cTemp c_cPE c_cKE etotal c_cPress vol density
thermo_modify norm no
thermo 250
compute rg PEG gyration
fix record all ave/time 50 1 50 v_clock v_T v_U v_K v_E v_P v_V v_rho c_rg file pull-thermo.dat format " %.15g"
dump trajectory all custom 250 pull.lammpstrj id mol type q x y z vx vy vz ix iy iz
dump_modify trajectory sort id
dump chain PEG custom 50 pull-peg.lammpstrj id mol type q xu yu zu vx vy vz
dump_modify chain sort id

run 15000

write_restart unforced.restart
write_data unforced.data

fix myaf1 topull1 addforce 10 0 0
fix myaf2 topull2 addforce -10 0 0

run 15000
write_restart pulled.restart
write_data pulled.data
```

Continue from merge.restart: 15 ps without added force, followed by 15 ps under constant endpoint forces.

The trajectory continues from the prepared state at 25 ps. It first runs 15,000 NVT steps to 40 ps without an applied pulling force. The right endpoint then receives +10 kcal/(mol Å) along x and the left receives the opposite force, followed by another 15,000 steps to 55 ps. Each force has magnitude approximately 694.77 pN. Constant force means that this externally added contribution remains specified at each step, while velocities and displacements follow all forces acting on the atoms. It differs from dragging an endpoint at a prescribed speed. The extension rate emerges from the response of the chain, solvent, thermostat, and applied forces together.

Read the force command together with group size. The addforce command adds its specified components to every atom in the group. If a group contains ten atoms, a force value of ten means ten on each atom rather than ten shared across the group. Here each pulling group contains exactly one terminal oxygen, so the force on each end equals the command parameter directly. Applying the same method to a larger end group or chain segment requires deciding whether to control force per atom or total force on the selected region. Recording the loaded atom IDs also preserves their identities as molecular shape and orientation change.

NVT targets 300 K and retains the volume reached during preparation, so the density in this segment is fixed at approximately 0.94018 g/cm³. That actual preparation state belongs with the results: changing the water model, allowing longer pressure relaxation, or changing volume can alter hydration and chain response. The supplied parameter combination provides a clear atomistic workflow. Comparison with a particular experimental force spectrum would examine parameters and sampling against its temperature, solvent composition, chain length, and pulling protocol, while recording the prepared density and conformation. Those measurable conditions connect the model to the intended comparison.

### Run the complete example starting from water

```
#!/usr/bin/env bash
set -euo pipefail
lmp=${LAMMPS:-lmp}
export OMP_NUM_THREADS=2
"$lmp" -in water.lmp -log water.log > water.stdout.log 2>&1
"$lmp" -in merge.lmp -log merge.log > merge.stdout.log 2>&1
"$lmp" -in pull.lmp -log pull.log > pull.stdout.log 2>&1
```

Run bash run.sh in the example directory; the LAMMPS environment variable can specify the executable.

The complete runner calls the water preparation, PEG insertion, and chain-motion inputs in that order. Separate logs make the atom count, time, and state of each stage inspectable. All supporting inputs are included below; keep them in the same example directory for a fresh run. The water and PEG templates define initial geometry and connectivity, the parameter file supplies the coefficients required by the interaction styles, and preparation writes the state read by the later stage. The dependencies form an executable sequence from water, to PEG in water, to the two-stage trajectory examined here.

### Complete water preparation input

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

units real
atom_style full
bond_style harmonic
angle_style harmonic
dihedral_style harmonic
pair_style lj/cut/coul/long 10
kspace_style ewald 1e-5
special_bonds lj 0.0 0.0 0.5 coul 0.0 0.0 1.0 angle yes

region box block -30 30 -15 15 -15 15
  create_box 8 box &
  bond/types 7 &
  angle/types 8 &
  dihedral/types 4 &
  extra/bond/per/atom 3 &
  extra/angle/per/atom 6 &
  extra/dihedral/per/atom 10 &
  extra/special/per/atom 14

include parameters.inc

molecule h2omol water.mol
create_atoms 0 random 700 87910 NULL mol h2omol 454756 overlap 1.0 maxtry 50

group H2O type OW HW
minimize 1.0e-4 1.0e-6 100 1000
reset_timestep 0

fix mynpt all npt temp 300 300 100 iso 1 1 1000


thermo 500
thermo_style custom step temp etotal vol density


# Numerical diagnostics; all energies are whole-system kcal/mol.
compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cPress all pressure cTemp
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE
variable K equal c_cKE
variable E equal c_cPE+c_cKE
variable P equal c_cPress
variable V equal vol
variable rho equal density
thermo_style custom step time c_cTemp c_cPE c_cKE etotal c_cPress vol density
thermo_modify norm no
thermo 250
fix record all ave/time 50 1 50 v_clock v_T v_U v_K v_E v_P v_V v_rho file water-thermo.dat format " %.15g"
dump trajectory all custom 250 water.lammpstrj id mol type q x y z vx vy vz ix iy iz
dump_modify trajectory sort id

timestep 1.0
run 15000

write_restart water.restart
# write_data water.data # uncomment to write a .data file as well
write_data water.data
```

Construct 700 waters and save water.restart.

### Complete PEG insertion and preparation input

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

kspace_style pppm 1e-5
read_restart water.restart

molecule pegmol peg.mol
create_atoms 0 single 0 0 0 mol pegmol 454756

group PEG type C CPos H HC OAlc OE

delete_atoms overlap 2.0 H2O PEG mol yes


fix mynpt all npt temp 300 300 100 x 1 1 1000
fix myrct PEG recenter 0 0 0 shift all
timestep 1.0

thermo 500

# Numerical diagnostics; all energies are whole-system kcal/mol.
compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cPress all pressure cTemp
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE
variable K equal c_cKE
variable E equal c_cPE+c_cKE
variable P equal c_cPress
variable V equal vol
variable rho equal density
thermo_style custom step time c_cTemp c_cPE c_cKE etotal c_cPress vol density
thermo_modify norm no
thermo 250
compute rg PEG gyration
fix record all ave/time 50 1 50 v_clock v_T v_U v_K v_E v_P v_V v_rho c_rg file merge-thermo.dat format " %.15g"
dump trajectory all custom 250 merge.lammpstrj id mol type q x y z vx vy vz ix iy iz
dump_modify trajectory sort id
dump chain PEG custom 50 merge-peg.lammpstrj id mol type q xu yu zu vx vy vz
dump_modify chain sort id

run 10000

write_restart merge.restart
# write_data merge.data # uncomment to write a .data file as well
write_data merge.data
```

Insert PEG, remove overlapping whole waters, and save merge.restart.

### Complete PEG and SPC/Fw parameters

```
# LAMMPS Include File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

labelmap atom 1 OE 2 C 3 HC 4 H 5 CPos 6 OAlc 7 OW 8 HW
labelmap bond 1 g4 2 g18 3 g26 4 g27 5 g56 6 g71 7 OW-HW
labelmap angle 1 g12 2 g13 3 g14 4 g15 5 g51 6 g56 7 g102 8 HW-OW-HW
labelmap dihedral 1 g23 2 g34 3 g46 4 glj14

mass OE 15.9994 # PEG O (GROMOS 54A7)
mass C 12.011 # PEG C (GROMOS 54A7)
mass HC 1.008 # PEG H (GROMOS 54A7)
mass H 1.008 # PEG H (GROMOS 54A7)
mass CPos 12.011 # PEG C (GROMOS 54A7)
mass OAlc 15.9994 # PEG O (GROMOS 54A7)
mass OW 15.9994 # H2O O (SPC/Fw)
mass HW 1.008 # H2O H (SPC/Fw)

pair_coeff OE OE 0.2526 2.8492
pair_coeff C C 0.0663 3.5812
pair_coeff HC HC 0.0283 2.3734
pair_coeff H H 0.0 0.0
pair_coeff CPos CPos 0.2450 2.8114
pair_coeff OAlc OAlc 0.1195 3.1000
pair_coeff OW OW 0.155 3.165
pair_coeff HW HW 0.0 0.0

bond_coeff g4 1109.2926 1.12
bond_coeff g18 399.7916 1.43
bond_coeff g26 299.8440 1.52
bond_coeff g27 400.0343 1.53
bond_coeff g56 310.7075 1.41
bond_coeff g71 179.2543 0.971
bond_coeff OW-HW 529.581 1.012

angle_coeff g12 47.6940 109.5
angle_coeff g13 55.1271 109.5
angle_coeff g14 47.6350 109.6
angle_coeff g15 55.1139 111.0
angle_coeff g51 54.9931 110.3
angle_coeff g56 180.4602 109.0
angle_coeff g102 30.1731 110.0
angle_coeff HW-OW-HW 37.95 113.24

dihedral_coeff g23 0.3011 1 3
dihedral_coeff g34 1.4149 1 3
dihedral_coeff g46 0.2390 -1 3
dihedral_coeff glj14 0.0 1 1
```

Geometry, interaction conventions, and parameter combinations match the actual run.

### Complete flexible-water template

```
# LAMMPS Molecule File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

3 atoms
2 bonds
1 angles

Coords

1 0 0 0 # H2O O
2 1.012 0 0	# H2O H
3 -0.4 0.929 0 # H2O H

Types

1 OW
2 HW
3 HW

Charges

1 -0.82 # H2O O (SPC/Fw)
2 0.41 # H2O H (SPC/Fw)
3 0.41 # H2O H (SPC/Fw)

Bonds

1 OW-HW 1 2
2 OW-HW 1 3

Angles

1 HW-OW-HW 2 1 3
```

Use this water template with the accompanying parameters.

### Complete 59-atom PEG template

```
# LAMMPS Molecule File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

# PEG molecule

59 atoms
58 bonds
104 angles
116 dihedrals

Coords

1 -3.0661409 -3.1122069 -1.2331413
2 -3.0905955 -3.1901295 -0.3069935
3 -1.7871211 -3.4628029 0.1677571
4 -1.7892607 -3.9757321 1.1640826
5 -1.4364998 -2.4400568 0.4558979
6 -0.9585523 -4.2486658 -0.9052389
7 -1.5905948 -5.0815649 -1.3120303
8 -0.0526673 -4.7456765 -0.4700128
9 -0.63208 -3.3539891 -2.0115812
10 0.2145577 -4.0010762 -2.9207664
11 -0.3729619 -4.5629487 -3.6922491
12 1.0240761 -4.5117416 -2.3388433
13 0.9711505 -2.8357534 -3.5251923
14 0.3408715 -1.9581318 -3.822669
15 1.6180273 -3.1186311 -4.3940263
16 1.8975644 -2.4613039 -2.5075514
17 3.0585685 -1.8075132 -3.006783
18 2.8443427 -0.8083913 -3.4607034
19 3.6249113 -2.4323449 -3.7466593
20 3.992363 -1.7272376 -1.8733916
21 4.9511518 -1.186389 -2.07637
22 4.254519 -2.795933 -1.6625937
23 3.423965 -1.0901105 -0.7496133
24 3.8947239 -1.659389 0.516987
25 3.9258208 -0.8841055 1.3251652
26 4.9554296 -2.0063238 0.4150401
27 3.0359709 -2.8971462 1.0103722
28 3.8185678 -3.6568248 1.2752906
29 2.4917984 -3.195833 0.0744643
30 2.0725911 -2.848428 2.0760021
31 1.638817 -1.4838974 2.5253139
32 2.5752075 -1.0062795 2.9080422
33 0.9012089 -1.6500344 3.3573053
34 0.8815328 -0.5306711 1.5538689
35 0.5519052 -1.1815579 0.7041188
36 1.6224746 0.2331944 1.1997508
37 -0.2989756 -0.0199954 2.1694908
38 -0.3033598 1.4095408 2.1280825
39 0.0521263 1.761717 1.1273303
40 0.4747811 1.7876458 2.8392599
41 -1.6030958 1.9523106 2.4553161
42 -1.5646386 2.9988577 2.8519616
43 -1.9732467 1.2583804 3.2576206
44 -2.5225735 1.8953969 1.3081864
45 -3.3669469 3.0741107 1.0973018
46 -3.0220368 3.8450892 1.8318384
47 -4.4858675 3.0095129 1.1439484
48 -3.0599689 3.6382723 -0.3005937
49 -3.982976 3.5193791 -0.9249329
50 -2.1988642 3.09917 -0.7700861
51 -2.7010767 5.025878 -0.199455
52 -1.3877664 5.5169363 -0.1698399
53 -0.8882234 5.1431508 -1.0995853
54 -0.935725 4.957068 0.6896982
55 -1.3304483 7.055419 0.0381237
56 -2.0611646 7.6166778 -0.601446
57 -0.3436857 7.3639388 -0.3955144
58 -1.5631742 7.5380082 1.3714558
59 -2.4256234 7.9039402 1.5299768

Types

1 H 
2 OAlc 
3 CPos 
4 HC 
5 HC 
6 C 
7 HC 
8 HC 
9 OE 
10 C 
11 HC 
12 HC 
13 C 
14 HC 
15 HC 
16 OE 
17 C 
18 HC 
19 HC 
20 C 
21 HC 
22 HC 
23 OE 
24 C 
25 HC 
26 HC 
27 C 
28 HC 
29 HC 
30 OE 
31 C 
32 HC 
33 HC 
34 C 
35 HC 
36 HC 
37 OE 
38 C 
39 HC 
40 HC 
41 C 
42 HC 
43 HC 
44 OE 
45 C 
46 HC 
47 HC 
48 C 
49 HC 
50 HC 
51 OE 
52 C 
53 HC 
54 HC 
55 CPos 
56 HC 
57 HC 
58 OAlc 
59 H 

Charges

1 0.211 
2 -0.328 
3 -0.019 
4 0.093 
5 0.093 
6 -0.063 
7 0.079 
8 0.079 
9 -0.295 
10 -0.021 
11 0.084 
12 0.084 
13 -0.023 
14 0.083 
15 0.083
16 -0.283 
17 -0.023 
18 0.083 
19 0.083 
20 -0.023 
21 0.083
22 0.083 
23 -0.283 
24 -0.023 
25 0.082 
26 0.082 
27 -0.023 
28 0.082 
29 0.082 
30 -0.283 
31 -0.023 
32 0.082 
33 0.082 
34 -0.023 
35 0.082 
36 0.082 
37 -0.283 
38 -0.023 
39 0.082 
40 0.083
41 -0.023 
42 0.083 
43 0.083 
44 -0.283 
45 -0.023 
46 0.083 
47 0.083
48 -0.021 
49 0.084 
50 0.084 
51 -0.295 
52 -0.063 
53 0.079 
54 0.079 
55 -0.019 
56 0.093 
57 0.093 
58 -0.328 
59 0.211 

Bonds

1 g18 13 16 
2 g18 16 17 
3 g18 20 23 
4 g18 23 24 
5 g18 27 30 
6 g18 30 31 
7 g18 34 37 
8 g18 37 38 
9 g18 41 44 
10 g18 44 45 
11 g18 48 51 
12 g18 51 52 
13 g18 6 9 
14 g18 9 10 
15 g26 17 20 
16 g26 24 27 
17 g26 31 34 
18 g26 38 41 
19 g27 10 13 
20 g27 3 6 
21 g27 45 48 
22 g27 52 55 
23 g4 10 11 
24 g4 10 12 
25 g4 13 14 
26 g4 13 15 
27 g4 17 18 
28 g4 17 19 
29 g4 20 21 
30 g4 20 22 
31 g4 24 25 
32 g4 24 26 
33 g4 27 28 
34 g4 27 29 
35 g4 3 4 
36 g4 3 5 
37 g4 31 32 
38 g4 31 33 
39 g4 34 35 
40 g4 34 36 
41 g4 38 39 
42 g4 38 40 
43 g4 41 42 
44 g4 41 43 
45 g4 45 46 
46 g4 45 47 
47 g4 48 49 
48 g4 48 50 
49 g4 52 53 
50 g4 52 54 
51 g4 55 56 
52 g4 55 57 
53 g4 6 7 
54 g4 6 8 
55 g56 2 3 
56 g56 55 58 
57 g71 1 2 
58 g71 58 59 

Angles

1 g102 14 13 16 
2 g102 15 13 16 
3 g102 2 3 4 
4 g102 2 3 5 
5 g102 21 20 23 
6 g102 22 20 23 
7 g102 23 24 25 
8 g102 23 24 26 
9 g102 30 31 32 
10 g102 30 31 33 
11 g102 35 34 37 
12 g102 36 34 37 
13 g102 37 38 39 
14 g102 37 38 40 
15 g102 4 3 5 
16 g102 4 3 6 
17 g102 44 45 46 
18 g102 44 45 47 
19 g102 5 3 6 
20 g102 52 55 56 
21 g102 52 55 57 
22 g102 56 55 57 
23 g102 56 55 58 
24 g102 57 55 58 
25 g12 1 2 3 
26 g12 13 16 17 
27 g12 20 23 24 
28 g12 27 30 31 
29 g12 34 37 38 
30 g12 41 44 45 
31 g12 48 51 52 
32 g12 55 58 59 
33 g12 6 9 10 
34 g13 10 13 16 
35 g13 16 17 20 
36 g13 17 20 23 
37 g13 23 24 27 
38 g13 3 6 9 
39 g13 30 31 34 
40 g13 31 34 37 
41 g13 37 38 41 
42 g13 38 41 44 
43 g13 44 45 48 
44 g13 45 48 51 
45 g13 51 52 55 
46 g13 9 10 13 
47 g14 11 10 12 
48 g14 14 13 15 
49 g14 18 17 19 
50 g14 21 20 22 
51 g14 25 24 26 
52 g14 28 27 29 
53 g14 32 31 33 
54 g14 35 34 36 
55 g14 39 38 40 
56 g14 42 41 43 
57 g14 46 45 47 
58 g14 49 48 50 
59 g14 51 52 53 
60 g14 51 52 54 
61 g14 53 52 54 
62 g14 7 6 8 
63 g14 7 6 9 
64 g14 8 6 9 
65 g15 2 3 6 
66 g15 3 6 7 
67 g15 3 6 8 
68 g15 52 55 58 
69 g15 53 52 55 
70 g15 54 52 55 
71 g51 10 13 14 
72 g51 10 13 15 
73 g51 11 10 13 
74 g51 12 10 13 
75 g51 16 17 18 
76 g51 16 17 19 
77 g51 17 20 21 
78 g51 17 20 22 
79 g51 18 17 20 
80 g51 19 17 20 
81 g51 24 27 28 
82 g51 24 27 29 
83 g51 25 24 27 
84 g51 26 24 27 
85 g51 28 27 30 
86 g51 29 27 30 
87 g51 31 34 35 
88 g51 31 34 36 
89 g51 32 31 34 
90 g51 33 31 34 
91 g51 38 41 42 
92 g51 38 41 43 
93 g51 39 38 41 
94 g51 40 38 41 
95 g51 42 41 44 
96 g51 43 41 44 
97 g51 45 48 49 
98 g51 45 48 50 
99 g51 46 45 48 
100 g51 47 45 48 
101 g56 49 48 51 
102 g56 50 48 51 
103 g56 9 10 11 
104 g56 9 10 12 

Dihedrals

1 g23 1 2 3 6 
2 g23 10 13 16 17 
3 g23 13 16 17 20 
4 g23 17 20 23 24 
5 g23 20 23 24 27 
6 g23 27 30 31 34 
7 g23 3 6 9 10 
8 g23 31 34 37 38 
9 g23 34 37 38 41 
10 g23 38 41 44 45 
11 g23 41 44 45 48 
12 g23 45 48 51 52 
13 g23 48 51 52 55 
14 g23 52 55 58 59 
15 g23 6 9 10 13 
16 g34 2 3 6 9 
17 g34 51 52 55 58 
18 g46 16 17 20 23 
19 g46 30 31 34 37 
20 g46 37 38 41 44 
21 g46 44 45 48 51 
22 g46 9 10 13 16 
23 glj14 1 2 3 4 
24 glj14 1 2 3 5 
25 glj14 11 10 13 14 
26 glj14 11 10 13 15 
27 glj14 11 10 13 16 
28 glj14 12 10 13 14 
29 glj14 12 10 13 15 
30 glj14 12 10 13 16 
31 glj14 13 16 17 18 
32 glj14 13 16 17 19 
33 glj14 14 13 16 17 
34 glj14 15 13 16 17 
35 glj14 16 17 20 21 
36 glj14 16 17 20 22 
37 glj14 18 17 20 21 
38 glj14 18 17 20 22 
39 glj14 18 17 20 23 
40 glj14 19 17 20 21 
41 glj14 19 17 20 22 
42 glj14 19 17 20 23 
43 glj14 2 3 6 7 
44 glj14 2 3 6 8 
45 glj14 20 23 24 25 
46 glj14 20 23 24 26 
47 glj14 21 20 23 24 
48 glj14 22 20 23 24 
49 glj14 23 24 27 28 
50 glj14 23 24 27 29 
51 glj14 25 24 27 28 
52 glj14 25 24 27 29 
53 glj14 26 24 27 28 
54 glj14 26 24 27 29 
55 glj14 27 30 31 32 
56 glj14 27 30 31 33 
57 glj14 28 27 30 31 
58 glj14 29 27 30 31 
59 glj14 30 31 34 35 
60 glj14 30 31 34 36 
61 glj14 32 31 34 35 
62 glj14 32 31 34 36 
63 glj14 32 31 34 37 
64 glj14 33 31 34 35 
65 glj14 33 31 34 36 
66 glj14 33 31 34 37 
67 glj14 34 37 38 39 
68 glj14 34 37 38 40 
69 glj14 35 34 37 38 
70 glj14 36 34 37 38 
71 glj14 37 38 41 42 
72 glj14 37 38 41 43 
73 glj14 39 38 41 42 
74 glj14 39 38 41 43 
75 glj14 39 38 41 44 
76 glj14 4 3 6 7 
77 glj14 4 3 6 8 
78 glj14 4 3 6 9 
79 glj14 40 38 41 42 
80 glj14 40 38 41 43 
81 glj14 40 38 41 44 
82 glj14 41 44 45 46 
83 glj14 41 44 45 47 
84 glj14 42 41 44 45 
85 glj14 43 41 44 45 
86 glj14 44 45 48 49 
87 glj14 44 45 48 50 
88 glj14 46 45 48 49 
89 glj14 46 45 48 50 
90 glj14 46 45 48 51 
91 glj14 47 45 48 49 
92 glj14 47 45 48 50 
93 glj14 47 45 48 51 
94 glj14 48 51 52 53 
95 glj14 48 51 52 54 
96 glj14 49 48 51 52 
97 glj14 5 3 6 7 
98 glj14 5 3 6 8 
99 glj14 5 3 6 9 
100 glj14 50 48 51 52 
101 glj14 51 52 55 56 
102 glj14 51 52 55 57 
103 glj14 53 52 55 56 
104 glj14 53 52 55 57 
105 glj14 53 52 55 58 
106 glj14 54 52 55 56 
107 glj14 54 52 55 57 
108 glj14 54 52 55 58 
109 glj14 56 55 58 59 
110 glj14 57 55 58 59 
111 glj14 6 9 10 11 
112 glj14 6 9 10 12 
113 glj14 7 6 9 10 
114 glj14 8 6 9 10 
115 glj14 9 10 13 14 
116 glj14 9 10 13 15 
```

All atomic and connectivity definitions are included on this page.

Define the window boundaries before comparing curves. The unforced mean uses 25 ≤ t < 40 ps and the constant-force mean uses 40 < t ≤ 55 ps, each containing 300 frames separated by 0.05 ps. The frame at 40 ps marks the force switch. It remains in the time plots and provides the displacement reference for external work, but is excluded from both phase means. This avoids assigning the same transition state twice. Frequent recording resolves a rapid response, but it does not turn strongly correlated neighbouring frames into independent repeats. Observation frequency and independent sample count remain distinct.

## Reading actual conformations: how shape changes as size grows

Begin with the actual conformations at 35, 40, and 55 ps. All three drawings use the same length scale and place each frame’s centre of mass at the origin, so their spatial extents can be compared directly. They show xy projections; the full three-dimensional coordinates remain in the size calculations. Circles identify the terminal oxygens, distinguishing them from terminal hydrogens or surrounding water. The 35 ps frame belongs to the unforced stage, 40 ps marks the force switch, and 55 ps is the end of the constant-force stage. These particular snapshots show the transition from a bent conformation toward one extended primarily along x.

### Three actual conformations at a shared scale

xy projections at 35, 40, and 55 ps, centred on each frame’s centre of mass while retaining actual conformation.

LAMMPS 30 Sep 2026 Update 1; the open PEG/SPC-Fw example by Gravelle and colleagues, at 300 K in real units. The original staged preparation and constant-force pulling protocol is retained with added numerical records.

[Download reference data and complete inputs (ZIP) 4.47 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-peg-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l07/en/#en-s6)

Actual PEG conformations at 35, 40 and 55 ps, drawn as xy projections at a shared scale. Each frame is translated by the mass-weighted centre of all 59 atoms. Orange rings identify the pulled oxygen atoms; backbone connectivity follows the actual bond table.

A two-dimensional projection has its own reading rules. Two atoms that overlap in the drawing may be separated along z, and two bonds crossing in the plane may pass at different depths in three dimensions. The pictures help identify overall arrangement, while distances and contacts are evaluated from full three-dimensional coordinates. Each snapshot has the same scale rather than being independently enlarged to fill its panel, so a visually longer chain is measured with the same ruler. A more complicated shape can be inspected from additional directions or with a trajectory viewer; the numerical analysis should retain the same atom identities and three-dimensional geometry throughout.

The complete record of 601 frames reveals what happens between snapshots. In the unforced window, radius of gyration varies from approximately 4.00 to 6.15 Å with a mean near 4.91 Å. Terminal distance varies more widely, from about 2.84 to 13.01 Å. The endpoints can therefore approach or separate substantially while the overall mass distribution changes less dramatically. After force application, terminal distance rises quickly and then fluctuates around a larger value. Its mean in the forced window is approximately 28.29 Å, while mean radius of gyration is about 8.65 Å. The two measurements describe the same extension response from endpoint and whole-molecule perspectives.

### Complete records of endpoint, contour, and mass spread

Unwrapped trajectory frames are spaced by 0.05 ps. Force starts at 40 ps; shading marks the constant-force stage.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l07/en/#en-s6)

Mass-weighted radius of gyration, terminal-oxygen distance, projected x separation and backbone contour length over 25–55 ps. Constant-force pulling begins at 40 ps. The contour sums consecutive backbone bond lengths, distinguishing it from straight-line end separation.

Directional sizes clarify the shape change further. If the x contribution grows strongly while y and z remain relatively small, the increased total radius reflects a mass distribution elongated along the force, rather than an isotropic expansion. Directional components depend on the chosen axes, and whole-chain rotation can redistribute them; the scalar radius remains unchanged by rotation. Here the applied force establishes x as a physical reference direction, giving the components a clear interpretation. Stating the axes first allows anisotropy in the size measurement to be connected to the forcing protocol.

### Actual unforced and constant-force PEG trajectory in water

No added pulling force from 25–40 ps; constant endpoint forces from 40–55 ps. PEG and water translate together to centre the chain, while actual coordinates retain internal conformation.

The trajectory can be read by following both the endpoints and the backbone. Extension involves many local reorientations rather than requiring every atom to lie on one straight line. Backbone angles and side groups remain present, and water continues moving around the chain. At 55 ps the terminal oxygen separation is approximately 29.124 Å, whereas the backbone contour is about 35.359 Å, reflecting the polygonal geometry of the covalent route. Connectivity remains fixed in this model, so the applied force deforms that existing molecular graph. Studying scission requires interactions and conditions that describe bond breaking; prolonged extension of a fixed harmonic connection has a different physical meaning.

## Why opposite endpoint forces can still do work

Equal and opposite applied forces give the chain zero net external force. This directs the loading toward endpoint separation rather than pushing the entire chain with a net force in one direction. Zero resultant force nevertheless does not imply zero work. Imagine two hands stretching a rubber band: the left hand moves left under a leftward force and the right hand moves right under a rightward force. Both forces can do positive work. Work depends on the force and displacement at each point of application. Adding forces acting at different points and discarding their separate displacements would lose that information.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l07/en/#en-s7)

Figure 3 · Opposite constant forces do work at their respective endpoints; the change in projected separation already includes both displacements.

Total work of constant opposite endpoint forcesEq. 5

![Total work of constant opposite endpoint forces](https://ml-biomat.com/static/agent-math/5f06fc4847d97773c1e34c43.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| W | Signed accumulated external work from force onset to the current time | kcal mol⁻¹ |
| F | Magnitude of force at each end: +F on the right, −F on the left | kcal mol⁻¹ Å⁻¹ |
| ΔxR, ΔxL | x displacements of the fixed right and left terminal oxygens | Å |
| X(t), X(t₀) | Projected right-minus-left separations at current and initial times | Å |
| t, t₀ | Current time and force onset, 40 ps in this example | ps |
| Δ, −, [], ×, = | Δ means final minus initial; combine work at both ends; brackets evaluate the projection difference first; adjacent factors multiply; equalities connect equivalent forms | 1 |

Reading the relationshipEvaluate force times displacement at each loaded point; the projection difference already includes both endpoint movements.

A worked exampleWith F = 10 kcal/(mol Å) at each end, outward motion of 1 Å per end gives ΔX = 2 Å and W = 20 kcal/mol. The actual 40–55 ps interval gives 178.7617 kcal/mol ≈ 1,241.98 pN nm.

ConditionsForce direction, magnitude, and endpoint identities are fixed. Common translation cancels in the separation; heat exchange and force-field energy are tracked separately.

For the constant forces here, right-end work is F times its x displacement and left-end work is −F times its x displacement. Their sum is exactly F times the increase in projected endpoint separation. F is the magnitude of the force on each end, so no additional factor of two is needed: both endpoint movements are already contained in the separation change. If each endpoint moves outward by 1 Å, the projected separation increases by 2 Å and the work is F times 2 Å. If both translate together by the same amount, the projection is unchanged and the two work contributions cancel. This also explains why common recentering leaves the separation-based work unchanged.

### Applied force protocol and accumulated external work

Force magnitudes follow the input protocol; work uses the actual change in projected endpoint separation relative to 40 ps.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l07/en/#en-s7)

Constant forces begin at 40 ps, with magnitude 694.77 pN at each end. Accumulated work is one force magnitude times the change in projected end separation relative to 40 ps; the difference already accounts for the two opposing forces. This is external work along the nonequilibrium pulling process.

Using the actual projected separation at 40 ps as the reference, accumulated external work at 55 ps is approximately 178.762 kcal/mol, equivalent to about 1,241.98 pN nm per molecular event. The curve rises rapidly during extension and subsequently follows smaller fluctuations of projected separation. Work need not increase during every small interval: a temporary inward motion opposes the applied force and contributes negative work. Retaining these signed increments gives the accumulated work for this protocol. Constant force simplifies the displacement integral to a difference in projected endpoint separation, so it can be evaluated directly from the coordinate record.

This external work is distinct from the potential-energy change in the log. The recorded potential energy comes from the molecular force field, and addforce does not include its external-force potential in thermodynamic output by default. The NVT thermostat also exchanges energy with the system. Applied work can therefore accompany changes in chain conformation, solvent arrangement, kinetic energy, and heat exchange. An energy balance needs explicit definitions for the force-field energy, external work, and thermostat exchange. Equating the work of a dissipative pulling realization with an equilibrium free-energy difference would omit the necessary sampling and thermodynamic conditions; those conditions are developed in the free-energy lesson.

## Turning a trajectory into results that support the next question

The complete Python program reads masses, types, and connectivity from the actual prepared data file, then reads the unwrapped chain trajectory. It follows the covalent route between terminal oxygens for contour length and uses masses and positions of all 59 atoms for radius of gyration. Frame-by-frame values are aligned with the LAMMPS output. It also retains the switch frame, exact phase-selection conditions, and the reference for external work. Every plot consequently uses the same endpoint and weighting definitions. Choosing oxygens in one figure and hydrogens in another, or changing mass weights silently, would change the measurement. These choices in the analysis code are part of the scientific method itself.

### Complete Python: sizes, conformations, and external work

```
"""Reproduce chain geometry and pulling plots from the actual PEG example.

python analyze_chain.py --run . --out analysis --language en

Dependencies: numpy, matplotlib. Inputs: merge.data, pull-peg.lammpstrj,
pull-thermo.dat. The dump supplies unwrapped xu,yu,zu coordinates.
"""
from pathlib import Path
from collections import deque
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


def read_data(path):
    sections, current = {}, None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line in {"Masses", "Atoms", "Bonds", "Atom Type Labels"}:
            current = line
            sections[current] = []
        elif line[0].isalpha():
            current = None
        elif current:
            sections[current].append(line.split())
    masses = {int(r[0]): float(r[1]) for r in sections["Masses"]}
    labels = {int(r[0]): r[1] for r in sections["Atom Type Labels"]}
    atoms = {int(r[0]): {"mol": int(r[1]), "type": int(r[2])} for r in sections["Atoms"]}
    bonds = [(int(r[2]), int(r[3])) for r in sections["Bonds"]]
    return masses, labels, atoms, bonds


def read_frames(path):
    with path.open(encoding="utf-8") as handle:
        while line := handle.readline():
            assert line.strip() == "ITEM: TIMESTEP"
            step = int(handle.readline())
            assert handle.readline().strip() == "ITEM: NUMBER OF ATOMS"
            n = int(handle.readline())
            assert handle.readline().startswith("ITEM: BOX BOUNDS")
            box = np.array([list(map(float, handle.readline().split())) for _ in range(3)])
            keys = handle.readline().split()[2:]
            a = np.array([list(map(float, handle.readline().split())) for _ in range(n)])
            a = a[np.argsort(a[:, keys.index("id")])]
            yield step, box, {key: a[:, i] for i, key in enumerate(keys)}


def shortest_path(edges, start, end):
    neighbours = {}
    for a, b in edges:
        neighbours.setdefault(a, []).append(b)
        neighbours.setdefault(b, []).append(a)
    queue, previous = deque([start]), {start: None}
    while queue:
        i = queue.popleft()
        if i == end:
            break
        for j in neighbours[i]:
            if j not in previous:
                previous[j] = i
                queue.append(j)
    if end not in previous:
        raise ValueError("Terminal oxygens are disconnected")
    result = [end]
    while result[-1] != start:
        result.append(previous[result[-1]])
    return result[::-1]


def stats(x):
    return {"frames": int(len(x)), "mean": float(np.mean(x)),
            "frame_sd": float(np.std(x, ddof=1)),
            "min": float(np.min(x)), "max": float(np.max(x))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path, default=Path("analysis"))
    parser.add_argument("--language", choices=["zh", "en"], default="en")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    zh = args.language == "zh"
    tr = lambda cn, en: cn if zh else en
    candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC",
                  "WenQuanYi Zen Hei", "DejaVu Sans"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    plt.rcParams.update({"font.family": [f for f in candidates if f in installed] if zh else ["DejaVu Sans"],
                         "font.size": 14, "axes.titlesize": 16, "svg.fonttype": "path",
                         "figure.facecolor": "#f8f7f2", "axes.facecolor": "#f8f7f2",
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.unicode_minus": False})
    masses_by_type, labels, all_atoms, all_bonds = read_data(args.run / "merge.data")
    records, coordinates = [], []
    reference_ids, atom_masses, end_indices, edges, backbone = None, None, None, None, None
    for step, box, data in read_frames(args.run / "pull-peg.lammpstrj"):
        ids = data["id"].astype(int)
        types = data["type"].astype(int)
        xyz = np.column_stack([data[k] for k in ("xu", "yu", "zu")])
        if reference_ids is None:
            reference_ids = ids.copy()
            row = {int(atom_id): i for i, atom_id in enumerate(ids)}
            atom_masses = np.array([masses_by_type[int(t)] for t in types])
            terminal = [i for i, t in enumerate(types) if labels[int(t)] == "OAlc"]
            assert len(terminal) == 2
            # Match the source's fixed membership established before the first run.
            left, right = sorted(terminal, key=lambda i: xyz[i, 0])
            end_indices = (left, right)
            chain_edges = [(a, b) for a, b in all_bonds if a in row and b in row]
            edges = [(row[a], row[b]) for a, b in chain_edges]
            backbone_ids = shortest_path(chain_edges, int(ids[left]), int(ids[right]))
            backbone = np.array([row[i] for i in backbone_ids])
            assert len(ids) == 59 and len(edges) == 58
        assert np.array_equal(ids, reference_ids)
        centre = np.sum(atom_masses[:, None] * xyz, axis=0) / atom_masses.sum()
        centred = xyz - centre
        rg_components_sq = np.sum(atom_masses[:, None] * centred**2, axis=0) / atom_masses.sum()
        rg = np.sqrt(rg_components_sq.sum())
        end = xyz[end_indices[1]] - xyz[end_indices[0]]
        re = np.linalg.norm(end)
        contour = np.linalg.norm(np.diff(xyz[backbone], axis=0), axis=1).sum()
        assert re <= contour + 1e-8
        records.append([step, step / 1000, rg, re, end[0], contour, *rg_components_sq])
        coordinates.append(centred)
    records = np.array(records)
    coordinates = np.array(coordinates)
    time = records[:, 1]
    unforced = time < 40
    pulled = time > 40
    switch = np.flatnonzero(time == 40)
    assert len(switch) == 1 and len(time) == 601
    switch = int(switch[0])
    thermo = np.loadtxt(args.run / "pull-thermo.dat", comments="#")
    assert np.array_equal(thermo[:, 0], records[:, 0])
    rg_error = np.max(abs(thermo[:, -1] - records[:, 2]))
    assert rg_error < 2e-5, rg_error
    # Equal/opposite constant endpoint forces: W = F * Delta(x_right-x_left).
    force_per_end = 10.0
    work = np.zeros(len(time))
    work[switch:] = force_per_end * (records[switch:, 4] - records[switch, 4])
    work_pN_nm = work * 6.947695457055374
    np.savetxt(args.out / "chain_shape.csv", np.column_stack([records, work]), delimiter=",",
               header="step,time_ps,Rg_A,terminal_O_distance_A,terminal_O_x_A,backbone_contour_A,Rgx_squared_A2,Rgy_squared_A2,Rgz_squared_A2,external_work_kcal_mol", comments="")
    summary = {"atoms": len(reference_ids), "mass_g_mol": float(atom_masses.sum()),
               "terminal_oxygen_ids_left_right": [int(reference_ids[i]) for i in end_indices],
               "backbone_atom_ids": backbone_ids,
               "native_Rg_max_error_A": float(rg_error), "switch_time_ps": 40,
               "force_per_end_pN": force_per_end * 69.47695457055374,
               "fixed_density_g_cm3": float(thermo[0, 8]),
               "unforced_window": "25 <= t < 40 ps", "pulled_window": "40 < t <= 55 ps",
               "transition_frame": "t=40 ps retained on time plots and as the work reference; excluded from phase means",
               "unforced": {}, "pulled": {},
               "final": {"Rg_A": float(records[-1, 2]), "terminal_O_distance_A": float(records[-1, 3]),
                         "terminal_O_x_A": float(records[-1, 4]), "contour_A": float(records[-1, 5]),
                         "external_work_kcal_mol": float(work[-1]), "external_work_pN_nm": float(work_pN_nm[-1])}}
    for phase, mask in [("unforced", unforced), ("pulled", pulled)]:
        for name, col in [("Rg_A", 2), ("terminal_O_distance_A", 3), ("terminal_O_x_A", 4), ("contour_A", 5)]:
            summary[phase][name] = stats(records[mask, col])
    (args.out / "chain_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    def finish(fig, name):
        for ext in ("svg", "png"):
            fig.savefig(args.out / f"{name}.{ext}", dpi=180, bbox_inches="tight")
        plt.close(fig)

    colors = ["#167d84", "#c16b3d", "#466eaa"]
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True, layout="constrained")
    axes[0].plot(time, records[:, 3], color=colors[0], label=tr("两端氧距离", "Terminal O distance"))
    axes[0].plot(time, records[:, 4], color=colors[1], linestyle="--", label=tr("沿x的端点投影", "Endpoint projection on x"))
    axes[0].plot(time, records[:, 5], color="#98a5a5", label=tr("主链轮廓长", "Backbone contour"))
    axes[0].set_ylabel(tr("长度 / Å", "Length / Å"))
    axes[1].plot(time, records[:, 2], color=colors[0], label=tr("质量加权回转半径", "Mass-weighted Rg"))
    axes[1].set_ylabel("Rg / Å")
    for k, col in enumerate([6, 7, 8]):
        axes[2].plot(time, np.sqrt(records[:, col]), color=colors[k], label=f"Rg,{['x','y','z'][k]}")
    axes[2].set_ylabel(tr("分方向均方根尺寸 / Å", "Directional RMS size / Å"))
    axes[2].set_xlabel(tr("从最初水准备开始的时间 / ps", "Time from the initial water preparation / ps"))
    for ax in axes:
        ax.axvline(40, color="#809393", linestyle=":")
        ax.axvspan(40, 55, alpha=.06, color=colors[1])
        ax.legend(frameon=False, loc="best", ncol=1)
        ax.grid(axis="y", alpha=.15)
        ax.set_xlim(25, 55)
    axes[0].set_title(tr("40 ps起，两端氧分别受±694.77 pN恒力", "Constant forces of ±694.77 pN act on terminal oxygens from 40 ps"))
    finish(fig, "chain-shape-records")

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.4), layout="constrained")
    type_colors = {1: "#c16b3d", 2: "#254952", 3: "#a0b2b4", 4: "#a0b2b4", 5: "#254952", 6: "#c16b3d"}
    for ax, target in zip(axes, [35, 40, 55]):
        idx = int(np.flatnonzero(time == target)[0])
        xy = coordinates[idx, :, :2]
        for a, b in edges:
            ax.plot(xy[[a, b], 0], xy[[a, b], 1], color="#90a3a2", linewidth=1, zorder=1)
        ax.scatter(xy[:, 0], xy[:, 1], s=[22 if masses_by_type[int(t)] < 2 else 60 for t in types],
                   c=[type_colors[int(t)] for t in types], zorder=2)
        ax.scatter(xy[list(end_indices), 0], xy[list(end_indices), 1], s=160,
                   facecolors="none", edgecolors="#c16b3d", linewidths=1.5, zorder=3)
        ax.axhline(0, color="#d3dcda", linewidth=.5)
        ax.axvline(0, color="#d3dcda", linewidth=.5)
        ax.set_xlim(-17, 17)
        ax.set_ylim(-10, 10)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel(tr("相对质心的x / Å", "x relative to COM / Å"))
        ax.set_ylabel(tr("相对质心的y / Å", "y relative to COM / Å"))
        ax.set_title(f"{target} ps\nRg = {records[idx,2]:.2f} Å, Re = {records[idx,3]:.2f} Å")
    fig.suptitle(tr("实际构象的xy投影；所有图采用相同长度比例", "Actual conformations projected onto xy; the length scale is shared"), fontsize=17)
    finish(fig, "chain-conformations")

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), layout="constrained")
    for ax, col, label in [(axes[0], 3, tr("两端氧距离 / Å", "Terminal O distance / Å")),
                           (axes[1], 2, "Rg / Å")]:
        bins = np.linspace(records[:, col].min(), records[:, col].max(), 26)
        for mask, color, name in [(unforced, colors[0], tr("25≤t<40 ps，无外加拉力", "25≤t<40 ps, unforced")),
                                  (pulled, colors[1], tr("40<t≤55 ps，恒力阶段", "40<t≤55 ps, constant force"))]:
            ax.hist(records[mask, col], bins=bins, density=True, histtype="step", color=color, linewidth=2, label=name)
        ax.set_xlabel(label)
        ax.set_ylabel(tr("概率密度 / Å⁻¹", "Probability density / Å⁻¹"))
        ax.legend(frameon=False, fontsize=12)
        ax.grid(axis="y", alpha=.15)
    fig.suptitle(tr("两个实际时间窗口内的尺寸分布", "Size distributions in the two actual observation windows"), fontsize=17)
    finish(fig, "chain-shape-distributions")

    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True, layout="constrained")
    force = np.where(time >= 40, 694.7695457055374, 0.0)
    axes[0].step(time, force, where="post", color=colors[1], label=tr("右端氧：+x", "Right oxygen: +x"))
    axes[0].step(time, -force, where="post", color=colors[2], label=tr("左端氧：−x", "Left oxygen: −x"))
    axes[0].set_ylabel(tr("施加力的x分量 / pN", "Applied x force / pN"))
    axes[0].legend(frameon=False)
    axes[1].plot(time, work_pN_nm, color=colors[0])
    axes[1].set_ylabel(tr("累计外力功 / pN nm", "Accumulated external work / pN nm"))
    axes[1].set_xlabel(tr("从最初水准备开始的时间 / ps", "Time from the initial water preparation / ps"))
    for ax in axes:
        ax.axvline(40, color="#809393", linestyle=":")
        ax.set_xlim(25, 55)
        ax.grid(axis="y", alpha=.15)
    axes[0].set_title(tr("两端力相反；功由端点投影变化计算", "Opposite endpoint forces; work follows the change in projected separation"))
    finish(fig, "pulling-work")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

Analyze the recorded output with the command in the file header; --language zh or en selects figure labels.

A size distribution presents the time record from another perspective: which sizes occur frequently within a selected window and which occur rarely? The histogram is normalized as a probability density, so the total bin area is one and the vertical-axis unit is inverse length. Shifts between the two distributions display the change in size range, while their widths describe variation within each window. The constant-force window includes the initial extension transient, leaving some smaller-size observations on its low-value side. Returning to the time trace helps distinguish persistent fluctuations from broadening produced by startup.

### Size distributions in the two finite observation windows

The windows 25 ≤ t < 40 ps and 40 < t ≤ 55 ps each contain 300 frames; probability-density areas are normalized to one.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l07/en/#en-s8)

Descriptive size distributions from 300 frames in each window: 25≤t<40 ps and 40<t≤55 ps. Every probability-density curve has unit area. The windows include actual conformational fluctuations and pulling response, with temporal correlations between frames.

A mean also depends on the order of operations. The reported mean radius is obtained by calculating a radius in each frame and then averaging those radii. Averaging squared radii first and taking a square root gives a different, usually somewhat larger quantity. Endpoint vectors have a related distinction: opposite directions can cancel in the mean vector, while averaging their magnitudes retains their sizes. A freely reorienting chain can have a mean end-to-end vector near zero even though individual frames have substantial terminal separation. Stating what is calculated before averaging resolves many apparent numerical contradictions, especially when comparing experiment, theory, and simulation.

When comparing phase means, distinguish fluctuation width from uncertainty in the mean. A standard deviation describes how much the size varies within the window, whereas uncertainty in its mean depends on the amount of effectively independent information. Saving every 0.05 ps does not make the chain forget its previous shape at that interval, so using the raw record count to reduce an error estimate can understate correlation. Divide the trajectory into progressively longer blocks, compare block means, and check them against independent repeats. If block means continue to drift systematically, extend preparation and sampling to establish a stable statistical description at the observation scale.

To turn the example into a force–extension study, prepare independent repeats at several forces under matching conditions, allow each condition to adjust, and compare projected separation and fluctuations within suitable stable windows. Keep chain length, water model, temperature, and composition definitions consistent across force conditions. Check whether the box along the stretching direction permits appropriate separation from periodic images. A chain-length study instead varies the number of repeat units and records end groups and total mass for each chain. Each curve then corresponds to a defined physical variable, connecting observed differences to the intended change in conditions.

Single-chain dimensions are the starting point for understanding many-chain materials. When several chains share a box, each experiences both its own interactions and contacts or crowding from other chains. Radius of gyration, contour length, and endpoint definitions remain useful, but the analysis becomes chain-resolved and incorporates relationships between chains. The next lesson develops that step with a traceable bead–spring model, examining how density, overlap removal, and preparation affect the resulting structure. The same sequence remains useful: define the objects and geometry, inspect their actual motion, and compare statistics chosen for the physical question.

## Further Reading and Open Materials

- [Polymer in water — A Set of Tutorials for the LAMMPS Simulation Package](https://lammpstutorials.github.io/sphinx/build/html/tutorial3/polymer-in-water.html) · Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, Axel Kohlmeyer · CC BY 4.0

  Construction, preparation, and constant endpoint pulling of PEG in SPC/Fw water.

  Model and run parameters retained; unwrapped-coordinate analysis, mass-weighted dimensions, backbone paths, external work, and bilingual explanations added.
- [compute gyration](https://docs.lammps.org/compute_gyration.html) · LAMMPS developers · Official technical documentation; referenced for mathematical definitions

  Mass-weighted radius of gyration, squared directional contributions, and periodic unwrapping.

  Added atom-resolved independent calculations, worked examples, and a geometric interaction.
- [fix addforce](https://docs.lammps.org/fix_addforce.html) · LAMMPS developers · Official technical documentation; referenced for force and output conventions

  Per-atom constant force and default energy-output conventions.

  Derived two-endpoint work and evaluated it from actual displacements.
- [Spatial Configuration of Macromolecular Chains — Nobel Lecture, 1974](https://www.nobelprize.org/uploads/2018/06/flory-lecture.pdf) · Paul J. Flory · Historical lecture cited; figures are newly drawn

  Historical transition from chemical connectivity to spatial chain conformations.

  An original concept drawing depicts a conformational ensemble.
- [Hydration Effects Turn a Highly Stretched Polymer from an Entropic into an Energetic Spring](https://doi.org/10.1021/acsnano.6b07071) · Susanne Liese and colleagues · Research article cited; no article figures reproduced

  Research context for coupled PEG stretching and hydration.

  The research question is distinguished from measurements of the present short teaching simulation.
