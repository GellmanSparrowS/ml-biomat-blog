# How Water and Ions Interact

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l06/en/
Language: en

From the origins of electrolyte theory to rigid water, ions, and interfaces: measure hydration neighbours and molecular orientation in an actual confined solution.

## What remains in the water after a grain of salt disappears

Stir a grain of table salt into water and the white solid gradually disappears from view. The liquid nevertheless acquires different properties: it conducts electrical current more readily and changes the environment around dissolved macromolecules. These changes matter in hydrated materials. A hydrogel often takes up a salt solution, a separation membrane must accommodate water and ions inside narrow passages, and the extension of a charged polymer depends on how nearby charges arrange themselves. Understanding such behaviour begins with identifying the particles left in solution and asking why water reorganizes around them. This lesson follows an aqueous sodium chloride solution confined between two solid walls, turning the familiar phrase “salt water” into particles whose numbers, distances, and orientations can be measured.

The sodium and chloride in a sodium chloride crystal already form an ionic lattice. Dissolution releases ions from that ordered arrangement into a liquid in which they can move. We write sodium as Na⁺ and chloride as Cl⁻; the signs describe electrical charge, rather than a direction of travel. Nearby water molecules rotate and exchange places, creating a local hydration environment around each ion. A useful analogy is a moving crowd of neighbours: people may remain close to a particular person even while individual members enter and leave the crowd. Counting neighbours at an instant and measuring how long the same neighbours remain are different questions. The first describes structure; the second requires an additional analysis of exchange and dynamics.

Nineteenth-century studies of conduction and osmotic behaviour asked a fundamental question: which particles actually exist in a solution? In his doctoral work in 1884 and the theory developed afterwards, Svante Arrhenius connected electrolyte behaviour with mobile charged particles through electrolytic dissociation. This historical change in interpretation helps explain the charges in a present-day simulation input. Sodium and chloride have their own positions and motion; they need not remain adjacent as permanent pairs, even when the complete solution is electrically neutral. The conceptual drawing below follows the transition from an ordered ionic lattice to a solution. It also introduces our two structural questions: how many waters surround an ion, and which part of each water molecule faces it?

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l06/en/#en-s1)

Figure 1 · Electrolytic dissociation connects conduction with mobile ions; water orientations illustrate local electrostatic interactions.

The example contains 406 water molecules, 15 sodium ions, 15 chloride ions, and 432 neutral wall atoms: 1,680 explicitly represented atoms in total. The lateral directions are periodic, while two walls confine the liquid along z. This geometry introduces solvent structure in a nanoscale passage and supplies the same physical system for a later investigation of resistance to flow. Here we examine preparation near 300 K before shear is applied. Actual trajectories provide water-neighbour counts and molecular orientations. Every reported count will retain its distance threshold and observation window, so that a visual impression of waters “surrounding an ion” becomes a measurement with a reproducible meaning.

## From neutrality to attraction: distinguishing charge from energy

Electrical neutrality means that the algebraic sum of the charges in a chosen object is zero. “Algebraic” means keeping each sign: positive and negative charges are added together rather than replaced by their magnitudes. Fifteen Na⁺ ions contribute fifteen positive elementary charges, and fifteen Cl⁻ ions contribute fifteen negative ones. Each water molecule is also neutral overall, and the wall atoms carry zero charge, so the complete box is neutral. The charges nevertheless occupy different positions. Equal income and expenditure need not occur at the same location; similarly, a zero net charge does not erase the electric field or interactions throughout a molecular system.

Add the charges of the selected particlesEq. 1

![Add the charges of the selected particles](https://ml-biomat.com/static/agent-math/40b8f735ba087efc6ef1863c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Q | Total charge of the selected object | e |
| qᵢ | Signed charge of particle i | e |
| i, N | Particle index and total selected particle count | 1 |
| Σ, =, 1 | Sum from index 1 through N; equality defines the total; 1 is the starting index | 1 |

Reading the relationshipAdd charges with their signs, allowing opposite signs to cancel.

A worked exampleFifteen +1e and fifteen −1e ions sum to zero; each water also gives −1.1128e + 2 × 0.5564e = 0.

ConditionsNet charge and spatial charge distribution describe overall composition and the local electrostatic environment, respectively.

The charges within water need one further explanation. Oxygen and hydrogen share chemical bonds, but the electronic charge is distributed unevenly. A model can approximate the resulting electrostatic interaction using positive and negative partial charges placed at selected positions. “Partial” emphasizes that these assigned values may be fractional; it does not require a whole electron to move from one atom to another during every time step. In this example sodium carries +1e, chloride carries −1e, and each positive water site carries +0.5564e, where e is the magnitude of the elementary charge. Charges alone are still insufficient to determine an interaction energy. We also need the separation between the charged sites.

Direct Coulomb energy between two specified charge sitesEq. 2

![Direct Coulomb energy between two specified charge sites](https://ml-biomat.com/static/agent-math/3ca18331aa01f2b1bc0a93f1.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Uᵢⱼ | Direct electrostatic energy of these two charge sites | kcal mol⁻¹ |
| qᵢ, qⱼ | Signed model charges | e |
| rᵢⱼ | Separation between the charge sites | Å |
| εᵣ | Relative dielectric constant, set to 1 here | 1 |
| C | Unit conversion constant, approximately 332.06371 | kcal mol⁻¹ Å e⁻² |
| i, j | Charge-site indices | 1 |
| =, /, × | Equality defines energy; the fraction divides; adjacent factors multiply | 1 |

Reading the relationshipThe charge product determines the sign; division by distance weakens the term as separation grows.

A worked exampleFor +1e and −1e separated by 5 Å with εᵣ = 1, U ≈ −332.06371/5 = −66.4127 kcal/mol.

ConditionsThis is a direct term for a specified pair. Short- and long-range solvers together evaluate periodic electrostatics, with explicit water charges contributing to the collective response.

The unit kcal/mol deserves attention as well. Molecular simulations use molar energy units to keep microscopic interactions consistent with chemical parameter conventions. Dividing a pair energy expressed in that convention by Avogadro’s constant converts it to the energy of one interaction, which can then be expressed in joules. A negative potential energy means a position below the chosen energy reference, rather than a negative amount of motion. Kinetic energy is a different quantity determined by mass and velocity. Distinguishing potential energy, kinetic energy, temperature, and charge helps identify the appropriate relationships to inspect when a log contains negative energies or a fluctuating temperature. The first step in reading a number is identifying both its units and the object it describes.

The charge product determines the sign of Coulomb energy. Opposite signs give a negative product, so bringing those charges closer lowers this contribution. Equal signs give a positive product, so bringing them closer raises it. Distance appears in the denominator because the interaction weakens as separation increases. For point charges of +1e and −1e separated by 5 Å, the direct electrostatic term in the units used here is about −66.41 kcal/mol. That number describes one contribution at a specified separation. Ions in solution simultaneously interact with many waters and other ions, and their arrangements depend on the energy and entropy of that complete environment. Ion pairing therefore calls for a distribution of ion–ion distances and their changes, considered together with hydration.

An explicit-water model already places molecular orientations and partial charges inside the calculation. Collective solvent reorganization emerges from those interactions. This example therefore leaves the relative dielectric constant in LAMMPS at its default value of one. Entering the familiar macroscopic dielectric constant of water, approximately 78 near room temperature, would superimpose a continuum screening description on the existing explicit model and change the meaning of its parameters. The distinction is between levels of description: explicit solvent represents individual molecules, whereas a continuum treatment summarizes the response of solvent that is not individually represented. We use the former throughout this example, because molecular orientation is itself one of the quantities we want to observe.

## Three atoms and four interaction sites: understanding TIP4P/2005

The flexible water in the previous lesson allowed bond lengths and the bond angle to fluctuate around preferred values. Here we use rigid TIP4P/2005 water. Rigid means that the two oxygen–hydrogen distances and the hydrogen–oxygen–hydrogen angle are maintained; the entire molecule can still translate and rotate. The “four points” refer to interaction sites. Each hydrogen carries positive charge, the oxygen position carries the main short-range Lennard–Jones interaction, and an additional M site carries the negative charge. M lies 0.1546 Å from oxygen along the angle bisector toward the hydrogens. It is a massless interaction location calculated from molecular geometry. The saved trajectory consequently contains only three explicit atoms per water: one oxygen and two hydrogens.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l06/en/#en-s3)

Figure 2 · TIP4P/2005 geometry and interaction sites. M is displaced from oxygen toward the hydrogens along the bisector; the Lennard–Jones centre remains at oxygen.

Why move the negative charge slightly away from oxygen? The history of water models reflects a choice between computational cost and the properties that a representation should describe. TIP4P/2005, introduced by Abascal and Vega in 2005, combines a four-site geometry with parameters developed for condensed phases of water. Moving the negative site changes the spatial charge distribution and therefore the orientation-dependent interactions between waters and between water and ions. Models all called “water” can have different geometries, partial charges, and Lennard–Jones parameters. Those choices belong together as a parameter set. Here the O–H length is 0.9572 Å, the H–O–H angle is 104.52°, each hydrogen carries +0.5564e, and M carries −1.1128e.

Reconstruct the M site from oxygen and hydrogen positionsEq. 3

![Reconstruct the M site from oxygen and hydrogen positions](https://ml-biomat.com/static/agent-math/4277c9bc5ad17c35117962d6.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| rO, rHₐ, rM | Position vectors of oxygen, hydrogen a, and M | Å |
| a, 1, 2 | Hydrogen index a is 1 or 2 | 1 |
| uₐ | Unit vector from oxygen toward hydrogen a | 1 |
| b | Unit bisector pointing between the two hydrogens | 1 |
| dOM | O–M distance, 0.1546 Å here | Å |
| \|…\| | Vector magnitude; division by a magnitude with the same units gives a unit vector | Inherited from the enclosed vector |
| +, −, /, =, × | Add and subtract vectors; divide by length to normalize; equality defines; adjacent factors multiply | 1 |

Reading the relationshipAdding the unit bond directions gives the bisector; move the specified distance from oxygen along its normalized direction.

A worked exampleWith oxygen at the origin and the hydrogens symmetric about positive x, b = (1, 0, 0) and M = (0.1546, 0, 0) Å.

ConditionsFirst reconstruct molecular geometry using x and y periodic images. The rigid target angle is 104.52° and both bond lengths are 0.9572 Å.

The bisector can be constructed from the two O–H directions. Dividing each bond vector by its own length produces a unit vector that specifies direction alone. Adding the two unit vectors points between the bonds; normalizing that sum gives a unit bisector. Moving 0.1546 Å along it takes us from oxygen to M. This construction also explains why the analysis must handle periodic boundaries before calculating molecular directions. A hydrogen displayed across the opposite side of the box would otherwise appear to form a bond spanning the entire box. The program first selects its nearest periodic image relative to oxygen. Because z is nonperiodic in this geometry, that reconstruction is applied only in x and y.

Electric dipole moment of neutral waterEq. 4

![Electric dipole moment of neutral water](https://ml-biomat.com/static/agent-math/2e060d62f5574bfbeee732e7.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| μ | Water electric dipole vector | e Å |
| qH, qM | Charge on each hydrogen and on M: +0.5564e and −1.1128e | e |
| rH₁, rH₂, rM, rO | Position vectors of the two hydrogens, M, and oxygen | Å |
| H₁, H₂, M, O | Site labels; 1 and 2 distinguish the hydrogens | 1 |
| +, −, =, × | Position differences give relative displacement; add charge times displacement; equality defines the dipole | 1 |

Reading the relationshipCharge times position measures charge separation. For zero net charge, translating the coordinate origin leaves this vector unchanged.

A worked exampleThe magnitude along the bisector is 2 × 0.5564 × [0.9572 cos(52.26°) − 0.1546] ≈ 0.479931 e Å. Using 1 e Å ≈ 4.803205 D gives 2.305206 D.

ConditionsEvaluate the negative charge at the TIP4P/2005 M site. The dipole points from the negative side toward the positive side.

The electric dipole moment expresses charge separation as a vector. For a neutral water molecule, choose oxygen as the coordinate origin, multiply each charge by its position vector, and add the contributions. The result points from the negative side toward the positive side. The sideways components of the hydrogen contributions cancel, their bisector components add, and the negative M-site contribution points oppositely. These parameters give a dipole magnitude of approximately 2.305 D, where D denotes the debye, a common molecular dipole unit. The input stores −1.1128 in the oxygen atom’s charge field, but the specialized TIP4P interaction evaluates it at M. An independent dipole calculation must reconstruct the same site.

Isolated ion–water electrostatics: rotate one rigid TIP4P/2005 molecule at a fixed ion–oxygen distance.

[Figure: Molecular geometry and analytic Coulomb energy](https://ml-biomat.com/tutorials/molecular-dynamics/l06/en/#en-s3)

Analytic electrostatic orientation exercise using this example’s rigid water geometry and charges. The complete liquid structure is measured separately from the actual trajectory.

The interactive diagram isolates one ion and one water, rotates the water at a fixed ion–oxygen distance, and evaluates the direct Coulomb energy between the ion and the three charged sites. A positive ion favours the negative side of water, while a negative ion favours the hydrogen side; the detailed curve retains the finite bond lengths and molecular angle. The exercise explains an orientational preference. In the complete liquid, neighbouring waters, short-range repulsion, and thermal motion also contribute, producing an orientation distribution. The O, H, H ordering in the complete template below has a practical role as well: the implicit TIP4P implementation requires consecutive atom IDs for a water molecule, with oxygen first.

### Complete rigid-water template

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

1    0 0 0
2    0.9584 0 0
3    -0.23996 0.92787 0

Types

1        O
2        H
3        H

Charges

1       -1.1128
2        0.5564
3        0.5564

Bonds

1   O-H      1      2
2   O-H      1      3

Angles

1   H-O-H    2      1      3

Shake Flags

1 1
2 1
3 1

Shake Atoms

1 1 2 3
2 1 2 3
3 1 2 3

Shake Bond Types

1 O-H O-H H-O-H
2 O-H O-H H-O-H
3 O-H O-H H-O-H

Special Bond Counts

1 2 0 0
2 1 1 0
3 1 1 0

Special Bonds

1 2 3
2 1 3
3 1 2
```

The O, H, H ordering and constraint information define each water.

## Maintaining water geometry and a consistent parameter set

Rigid water still needs O–H bonds and an H–O–H angle listed in its input, because the program must identify which atoms are constrained. In this example the harmonic bond and angle coefficients are zero, followed by target geometry values of 0.9572 and 104.52. Zero means that ordinary harmonic springs do not supply the restoring forces. During dynamics, SHAKE calculates additional constraint forces that maintain the specified geometry. A movable small triangle is a helpful analogy: the entire triangle can translate and rotate while distances between its vertices follow the shape constraints. Disabling those constraints while retaining zero harmonic coefficients would therefore change the model itself.

SHAKE originated in the 1977 work of Ryckaert, Ciccotti, and Berendsen on constrained molecular motion. It addresses a computational difficulty: very rapid bond vibrations demand short integration steps, whereas many questions concern slower translation, rotation, or structural rearrangement. Constraining selected internal coordinates concentrates the calculation on the motions retained by the model. This example still uses a 1 fs time step and iteratively satisfies the constraints during dynamics. The constraint tolerance, maximum iteration count, and precision of saved coordinates are separate settings. Recalculating bond lengths from coordinates written with a finite number of digits introduces small recording deviations, so those deviations must be distinguished from the precision of the constraint solver itself.

Constraint treatment also differs between minimization and dynamics. During minimization, this input supplies SHAKE with kbond 2000 so that strong harmonic restraints approximately preserve water geometry while initial crowding is reduced. Dynamics then uses geometric constraints. The original template coordinates give bond lengths near 0.9584 Å, slightly different from the 0.9572 Å target. This illustrates the distinction between a placement template and the geometry specified by parameters and constraints. In the later part of the actual trajectory, the mean O–H distance is 0.9571999 Å and the mean H–O–H angle is 104.51999°, consistent with the target. Checking these elementary measurements establishes the intended model behaviour before interpreting a more complicated hydration structure.

### Complete water, ion, and wall parameters

```
# LAMMPS Include File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

mass O 15.9994
mass H 1.008
mass Na+ 22.990
mass Cl- 35.453
mass WALL 26.9815

pair_coeff O O 0.185199 3.1589
pair_coeff H H 0.0 1.0
pair_coeff Na+ Na+ 0.04690 2.4299
pair_coeff Cl- Cl- 0.1500 4.04470
pair_coeff WALL WALL 11.697 2.574
pair_coeff O WALL 0.4 2.86645

bond_coeff O-H 0 0.9572
angle_coeff H-O-H 0 104.52
```

Use geometry, charges, and interaction parameters as a consistent set.

The parameter file also supplies ion and wall masses and the Lennard–Jones parameters of the atom types. Charged ions still need short-range interactions: repulsion prevents unlimited approach, and dispersion contributes another part of the interaction. Unlike pairs without an explicit coefficient use the default geometric mixing rule in this example, while the oxygen–wall pair has its own explicitly specified parameters. The wall consists of atoms with masses, positions, and interactions, arranged into confining layers. Its numerical atomic mass is close to that of aluminium, but its interaction model here is the specified Lennard–Jones wall. Interfacial behaviour should therefore be discussed in terms of these wall parameters, wetting, and layering rather than assigned to all real metallic surfaces.

Another common term is the hydrogen bond in water. A hydrogen on one water can point toward the electron-rich side of another, forming an orientation-dependent neighbouring relationship. This is a different structural level from the covalent O–H connections inside one water molecule. In the present fixed-charge model, the tendency toward such arrangements follows from the assigned charges and short-range interactions; it does not require adding permanent covalent bonds between waters. Counting hydrogen bonds is an additional analysis that specifies donor and acceptor atoms together with distance and angle criteria. Those criteria identify relationships that form, disappear, and exchange while each water retains its own two O–H connections.

## Placing salt water in a slit: boundaries and long-range electrostatics

System construction first places the two solids on a lattice, adds water in the intervening region, and inserts fifteen ions of each sign. The lattice spacing is 4.04 Å, and the x and y dimensions each span six lattice units, giving physical side lengths of 24.24 Å. The region command uses lattice units here: a range from −3 to 3 does not mean −3 Å to 3 Å. The full z dimension is 40.4 Å, with wall atoms occupying two thinner regions inside it. Translating these input values into physical lengths makes it possible to assess crowding, choose meaningful neighbour distances, and calculate the slice volumes needed for a density profile.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l06/en/#en-s5)

Figure 3 · Left: an x–z confinement schematic, with y perpendicular to the page. Right: empty extension for electrostatic treatment; physical interactions within the slab remain present in every direction.

The boundary setting p p f means periodic x and y directions and fixed, nonperiodic boundaries in z. “Fixed boundary” refers to the box boundary, rather than pinning every atom inside a wall. During the preparation stage, the NVT integrator acts on all atoms, so the walls can vibrate and rearrange. Confinement comes from interactions with actual wall atoms; the letter f does not create a reflecting mathematical surface. Periodicity laterally tiles equivalent copies of the slit, requiring nearest-image distances in those directions. Along z, the physical upper and lower sides remain distinct and must not be joined as they would be in a fully periodic liquid.

### Construct the confined electrolyte

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

boundary p p f
units real
atom_style full
bond_style harmonic
angle_style harmonic
pair_style lj/cut/tip4p/long O H O-H H-O-H 0.1546 12.0
kspace_style pppm/tip4p 1.0e-5
kspace_modify slab 3.0

lattice fcc 4.04
region box block -3 3 -3 3 -5 5
create_box 5 box &
  bond/types 1 &
  angle/types 1 &
  extra/bond/per/atom 2 &
  extra/angle/per/atom 1 &
  extra/special/per/atom 2
labelmap atom 1 O 2 H 3 Na+ 4 Cl- 5 WALL
labelmap bond 1 O-H
labelmap angle 1 H-O-H

region rbotwall block -3 3 -3 3 -4 -3
region rtopwall block -3 3 -3 3 3 4
region rwall union 2 rbotwall rtopwall
create_atoms WALL region rwall

region rliquid block INF INF INF INF -2 2
molecule h2omol water.mol
create_atoms 0 region rliquid mol h2omol 482793

create_atoms Na+ random 15 5802 rliquid overlap 0.3 maxtry 500
create_atoms Cl- random 15 9012 rliquid overlap 0.3 maxtry 500
set type Na+ charge 1
set type Cl- charge -1

include parameters.inc
include groups.inc

delete_atoms random fraction 0.15 yes H2O NULL 482793 mol yes


write_dump all custom created.lammpstrj id mol type q x y z ix iy iz modify sort id
run 0

write_data create.data nocoeff
```

Place water.mol, parameters.inc, and groups.inc in the example directory and run lmp -in create.lmp.

Electrostatic interactions decay slowly enough that identifying nearby neighbours alone is insufficient. The lj/cut/tip4p/long style handles the short-range part and works with pppm/tip4p to include long-range electrostatics. An analogy is resolving both a nearby street and the wider city: nearby contributions use particle separations directly, while a smoother long-range contribution is handled on a mesh, and the parts combine into the same electrostatic calculation. Both must use the M-site charge locations consistently, which is why the TIP4P-specific pair style and long-range solver are used together. The setting 1.0e−5 controls a target accuracy for the long-range force calculation; it serves a different purpose from the 1 fs time step and the SHAKE tolerance.

Slab geometry also needs an appropriate treatment of periodic images inside the long-range algorithm. The command kspace_modify slab 3.0 inserts empty space into the extended electrostatic domain and applies a slab correction to reduce coupling between repeated layers above and below. The factor 3.0 is the ratio of extended volume to the physical simulation volume; it does not triple the liquid thickness. Attractions and repulsions directed along z within the physical slab remain present, as required for hydration and wall structure. This setting represents a slab that is periodic in two directions and approximately isolated along its normal. A numerical refinement can increase the extension and compare forces or structural observables to assess residual image coupling for the chosen geometry.

### Groups for water, ions, and walls

```
# LAMMPS Include File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

group H2O type O H
group Na type Na+
group Cl type Cl-
group ions union Na Cl
group fluid union H2O ions

group wall type WALL
region rtop block INF INF INF INF 0 INF
region rbot block INF INF INF INF INF 0
group top region rtop
group bot region rbot
group walltop intersect wall top
group wallbot intersect wall bot
```

Groups provide selections for constraints, integration, and analysis.

The group file organizes water, ions, fluid, and the upper and lower walls into selectable atom sets. A group assigns a name to a collection; integration, constraints, and force commands determine how that collection moves. Construction also removes a specified fraction of whole water molecules to prepare the initial packing for relaxation. The mol yes option makes that deletion molecular, avoiding a broken water left behind by deleting just one hydrogen. Final counts should be read from the generated system; this realization contains 406 intact waters. Keeping names, groups, particle counts, and motion rules conceptually separate makes later changes to salt content or wall conditions much easier to interpret.

Concentration also requires a defined denominator. In a beaker, salt concentration usually refers to a solution volume. This simulation box contains liquid, solids, and empty space. Dividing fifteen ions by the complete box volume gives a box-averaged number density, whereas using a specified region between the walls gives the concentration associated with that region. The numbers answer different questions and must retain their volume definitions. Local water-neighbour counts do not require a macroscopic solution volume, so this lesson first reports composition and local structure. A concentration comparison can subsequently adopt a consistent accessible region or another explicitly defined composition measure, allowing changes in salt content and geometry to be discussed separately.

## Inspecting preparation before interpreting molecular structure

Run create.lmp first to generate create.data, then run equilibrate.lmp to read it. The second file performs minimization, resets the step counter, and advances 30,000 steps of 1 fs each, producing 30 ps of preparation. A picosecond is 1,000 femtoseconds. The NVT target is 300 K and the box dimensions remain fixed, while the separation between mobile walls can change. The input also recentres all atoms together along z. This common translation changes the coordinate origin while preserving separations. Local hydration geometry and wall separation are therefore retained, even though absolute z coordinates are expressed in the recentered frame.

### Complete minimization and 30 ps preparation input

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

boundary p p f
units real
atom_style full
bond_style harmonic
angle_style harmonic
pair_style lj/cut/tip4p/long O H O-H H-O-H 0.1546 12.0
kspace_style pppm/tip4p 1.0e-5
kspace_modify slab 3.0

read_data create.data

include parameters.inc
include groups.inc

fix myshk H2O shake 1.0e-5 200 0 b O-H a H-O-H kbond 2000


thermo 1
thermo_style custom step temp etotal press

minimize 1.0e-6 1.0e-6 1000 1000
reset_timestep 0

fix mynvt all nvt temp 300 300 100
fix myshk H2O shake 1.0e-5 200 0 b O-H a H-O-H
fix myrct all recenter NULL NULL 0
timestep 1.0


variable walltopz equal xcm(walltop,z)
variable wallbotz equal xcm(wallbot,z)
variable deltaz equal v_walltopz-v_wallbotz

thermo 250
thermo_style custom step temp etotal press v_deltaz

# Numerical trajectory and thermodynamic records added to the original tutorial.
dump course all custom 500 equilibrate.lammpstrj id mol type q x y z vx vy vz ix iy iz
dump_modify course sort id
compute coursePE all pe
compute courseKE all ke
compute courseTemp all temp
compute coursePressure all pressure courseTemp
variable courseTime equal time
variable courseT equal c_courseTemp
variable courseU equal c_coursePE
variable courseK equal c_courseKE
variable courseE equal c_coursePE+c_courseKE
variable courseP equal c_coursePressure
thermo_style custom step v_courseT v_courseU v_courseK v_courseE v_courseP v_deltaz
fix courseRecord all ave/time 250 1 250 v_courseTime v_courseT v_courseU v_courseK v_courseE v_courseP file equilibrate-thermo.dat

run 30000

write_data equilibrate.data nocoeff





write_restart equilibrate.restart
write_dump all custom equilibrate-final.lammpstrj id mol type q x y z ix iy iz modify sort id
```

After generating create.data, run lmp -in equilibrate.lmp.

Read the temperature and wall-separation curves together. In the actual record, the system warms from its initially low temperature to approximately 300 K and then fluctuates. The 61 temperature records from 15 to 30 ps have a mean of about 299.74 K. Over the same interval, 31 trajectory frames give an average separation of approximately 28.33 Å between wall centres, with continued slower variation. Temperature near its target establishes the scale of thermal motion, while the wall curve reveals ongoing structural adjustment. Wall-centre separation includes the positions of the solid layers themselves. The width accessible to liquid also depends on wall thickness, atomic size, and interactions, so a local-density analysis should inspect the actual fluid distribution.

### Actual preparation in a fixed box

Whole-system temperature and wall-centre separation come from the 0–30 ps preparation; shading marks the 15–30 ps structural window.

LAMMPS 30 Sep 2026 Update 1; the nanosheared-electrolyte example by Gravelle and colleagues, with TIP4P/2005 water at 300 K in real units, periodic x/y and fixed z boundaries; 30 ps of preparation followed by 200 ps of shear.

[Download reference data and complete inputs (ZIP) 3.17 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-electrolyte-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l06/en/#en-s6)

Actual 0–30 ps preparation records: whole-system temperature and wall-centre separation. Cell lengths are fixed while the wall atoms can move. Shading identifies the 15–30 ps structural-analysis window.

The structural analysis uses 15–30 ps and describes the local environment in that preparation window. Adjacent observations are generally correlated: an ion can remain near the same location, and a water molecule may appear repeatedly in its neighbourhood. Multiplying 31 frames by fifteen ions produces many observations, but not the same number of independent experiments. We retain averages and distributions and state the time window on the plots. A study comparing salts or surfaces quantitatively would extend the trajectories, compare successive time blocks, and repeat the calculation from independent initial arrangements. Those steps improve temporal coverage and independent replication through different, complementary routes.

### Preparation trajectory of electrolyte and mobile walls

Actual 0–30 ps preparation. Water, ions, and walls are translated together in z to remain centred, preserving relative geometry.

The coloured atoms offer an intuitive entry into the trajectory. Waters change orientation near an ion, and their arrangement beside a wall differs from that in the middle. Pausing at one instant reveals local packing; advancing through time shows how it evolves. Molecular connectivity and assigned ion charges remain fixed in this model, so the question concerns the spatial organization of specified chemical species. Hydrolysis, proton transfer, or chemical reaction at a surface requires a model that describes those processes. For the present problem, understanding the geometry, charges, and statistics of the fixed species already explains important features of hydration.

## Measuring hydration: neighbour counts and molecular orientation

A direct hydration measurement draws a sphere of radius r around an ion and counts the water oxygens inside it. Using oxygen to represent each water avoids counting its two hydrogens as two extra molecules. Repeat that operation for every ion and every recorded time, then average to obtain the mean number of neighbouring waters within radius r. Increasing r gives a cumulative curve: first it crosses a region rarely occupied by oxygen, then includes the nearer waters, and eventually includes increasingly distant molecules. Changes in the slope and shape of this curve reveal differences in local packing around the ions more clearly than a single snapshot can.

Cumulative water-neighbour count averaged over ions and framesEq. 5

![Cumulative water-neighbour count averaged over ions and frames](https://ml-biomat.com/static/agent-math/db88778fdc6e3bf7154ee436.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| n̄(r) | Mean neighbouring waters per ion within radius r | 1 |
| r, dᵢⱼ⁽ᶠ⁾ | Reporting radius and ion i to water oxygen j distance in frame f | Å |
| Nf, NI, NW | Numbers of frames, selected ions, and waters | 1 |
| f, i, j | Summation indices for frame, ion, and water | 1 |
| 1[…], ≤ | Count 1 when the condition holds, otherwise 0; ≤ includes equality | 1 |
| Σ, /, ×, = | Sum pair counts; divide by the product of frame and ion counts to average; equality defines | 1 |

Reading the relationshipEach water satisfying the distance condition contributes one; accumulate and average over ions and frames.

A worked exampleFor 31 frames and 15 Na⁺ ions, 2,283 pair observations within 3.3 Å give 2,283/(31 × 15) ≈ 4.90968.

ConditionsUse nearest images in x and y and nonperiodic z distances. Frames and recurring pairs may be correlated; the mean retains its 15–30 ps window.

The indicator function in the formula acts as a counting switch: it returns one when the distance condition is satisfied and zero otherwise. The inner sum counts waters around a particular ion; the outer sums combine ions and times. Distances must respect this geometry, using the nearest periodic image in x and y and the physical separation in z. To attach reproducible numbers to the curves, the reported radii are 3.3 Å for Na⁺ and 3.9 Å for Cl⁻. These are explicitly chosen analysis thresholds whose effects can be inspected on the full cumulative curve. A threshold-dependent count is different from assigning every ion an immutable number of waters irrespective of temperature, composition, model, and interface.

In this 15–30 ps window, Na⁺ has approximately 4.91 neighbouring waters within 3.3 Å, while Cl⁻ has approximately 7.15 within 3.9 Å. The radii differ, so each value should be read together with its own cumulative curve. We have not divided shell counts by a box-averaged water density and labelled the result a bulk radial distribution function. The box contains solids and empty regions, and a shell near a wall is not uniformly accessible to water. Direct counts retain the actual geometry of this system. Comparison with a homogeneous bulk radial distribution requires a separate homogeneous system or an explicit treatment of spatial inhomogeneity and accessible volume.

Think of the cumulative neighbour curve as an observation circle expanding around an ion. At very small radii it usually contains no water oxygens. When it reaches the nearest waters, the count rises quickly. A less populated region between nearby and more distant waters produces a flatter stretch. A reporting radius in a flat region tends to be less sensitive to a small change in threshold than a radius on a steep rise. This is a practical way to read threshold sensitivity directly from the curve. When the layers are poorly separated, retaining the entire curve allows structural differences at several distances to remain visible instead of compressing the comparison into a single coordination number.

Use a directional cosine to describe how water faces an ionEq. 6

![Use a directional cosine to describe how water faces an ion](https://ml-biomat.com/static/agent-math/0c760e4df4e117811c5f9910.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| s | Dot product of unit directions, the orientation cosine | 1 |
| μ̂ | Unit vector in the water dipole direction | 1 |
| R, rO, rI | Ion-to-oxygen vector and positions of oxygen and ion | Å |
| R̂, ^ | Unit direction of R; the hat denotes division by vector magnitude | 1 |
| β | Angle between the water dipole and outward ion-to-oxygen direction | rad |
| ·, cos, =, − | The dot product compares directions; cos is cosine; equality links definitions; subtract positions for displacement | 1 |

Reading the relationshipThe dot product of unit vectors equals their angle cosine, giving a range from −1 to +1.

A worked exampleAt β = 0°, s = +1 and the positive side points outward; at 90°, s = 0; at 180°, s = −1 and the positive side points toward the ion.

ConditionsSelect pairs using the stated ion–oxygen distance threshold. The quantity describes instantaneous orientation.

Counts describe whether a water is nearby; orientation describes which side is nearby. Draw a radial arrow from the ion toward the water oxygen and compare it with the water dipole direction. A cosine near +1 means the arrows align: the positive side of water points outward and its negative side lies nearer the ion. A cosine near −1 means the positive side points toward the ion. Values near zero describe approximately perpendicular directions. A histogram of all ion–water pairs satisfying the stated distance condition shows the distribution under thermal motion. The Na⁺ distribution favours positive values and the Cl⁻ distribution favours negative ones, connecting the trajectory back to the earlier electrostatic picture.

### Complete Python: hydration, orientation, and local density

```
"""Analyze the actual confined electrolyte preparation trajectory.

python analyze_hydration.py --run . --out analysis --language en

Dependencies: numpy and matplotlib. Inputs: equilibrate.lammpstrj,
equilibrate-thermo.dat. Times are absolute preparation times in fs.
The 15--30 ps window describes this finite preparation segment.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

AVOGADRO = 6.02214076e23
MASS = {1: 15.9994, 2: 1.008, 3: 22.990, 4: 35.453, 5: 26.9815}


def frames(path):
    """Read orthogonal LAMMPS custom dumps without assuming row order."""
    with path.open(encoding="utf-8") as handle:
        while line := handle.readline():
            if line.strip() != "ITEM: TIMESTEP":
                raise ValueError("Expected a timestep header")
            step = int(handle.readline())
            assert handle.readline().strip() == "ITEM: NUMBER OF ATOMS"
            n = int(handle.readline())
            header = handle.readline().split()
            assert header[:3] == ["ITEM:", "BOX", "BOUNDS"]
            bounds = np.array([list(map(float, handle.readline().split())) for _ in range(3)])
            assert bounds.shape == (3, 2), "This analysis expects an orthogonal box"
            keys = handle.readline().split()[2:]
            arr = np.array([list(map(float, handle.readline().split())) for _ in range(n)])
            order = np.argsort(arr[:, keys.index("id")])
            yield step, bounds, {key: arr[order, j] for j, key in enumerate(keys)}


def in_plane_image(delta, lengths):
    """Nearest periodic image in x and y; z is physically nonperiodic."""
    result = np.array(delta, copy=True)
    result[..., :2] -= lengths[:2] * np.rint(result[..., :2] / lengths[:2])
    return result


def sample_stats(values):
    a = np.asarray(values, dtype=float)
    return {"count": int(a.size), "mean": float(a.mean()),
            "frame_or_pair_sd": float(a.std(ddof=1)) if a.size > 1 else 0.0,
            "minimum": float(a.min()), "maximum": float(a.max())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path, default=Path("analysis"))
    parser.add_argument("--language", choices=["zh", "en"], default="en")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    zh = args.language == "zh"
    font_candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC",
                       "WenQuanYi Zen Hei", "DejaVu Sans"]
    installed_fonts = {font.name for font in font_manager.fontManager.ttflist}
    chinese_fonts = [name for name in font_candidates if name in installed_fonts]
    plt.rcParams.update({"font.family": chinese_fonts if zh else ["DejaVu Sans"],
                         "font.size": 14, "axes.titlesize": 16,
                         "svg.fonttype": "path", "axes.spines.top": False,
                         "axes.spines.right": False, "figure.facecolor": "#f8f7f2",
                         "axes.facecolor": "#f8f7f2", "axes.unicode_minus": False})
    tr = lambda cn, en: cn if zh else en
    radii = np.linspace(1.0, 6.0, 101)
    zedges = np.arange(-20.5, 20.5001, .5)
    zmid = (zedges[:-1] + zedges[1:]) / 2
    neighbour_records = {3: [], 4: []}
    orientation = {3: [], 4: []}
    cutoffs = {3: 3.3, 4: 3.9}
    profiles = {"water": [], "Na": [], "Cl": [], "wall": []}
    geometry = []
    history = []
    selection_times = []
    last = None
    for step, bounds, data in frames(args.run / "equilibrate.lammpstrj"):
        ids = data["id"].astype(int)
        typ = data["type"].astype(int)
        xyz = np.column_stack([data[k] for k in ("x", "y", "z")])
        lengths = bounds[:, 1] - bounds[:, 0]
        oi = np.flatnonzero(typ == 1)
        id_to_row = {int(atom_id): i for i, atom_id in enumerate(ids)}
        # Implicit TIP4P requires O,H,H consecutive atom IDs with O first.
        h1 = np.array([id_to_row[int(ids[i] + 1)] for i in oi])
        h2 = np.array([id_to_row[int(ids[i] + 2)] for i in oi])
        assert np.all(typ[h1] == 2) and np.all(typ[h2] == 2)
        assert np.all(data["mol"][oi] == data["mol"][h1])
        assert np.all(data["mol"][oi] == data["mol"][h2])
        v1 = in_plane_image(xyz[h1] - xyz[oi], lengths)
        v2 = in_plane_image(xyz[h2] - xyz[oi], lengths)
        l1 = np.linalg.norm(v1, axis=1)
        l2 = np.linalg.norm(v2, axis=1)
        u1, u2 = v1 / l1[:, None], v2 / l2[:, None]
        bisector = u1 + u2
        bisector /= np.linalg.norm(bisector, axis=1)[:, None]
        angle = np.degrees(np.arccos(np.clip(np.sum(u1 * u2, axis=1), -1, 1)))
        # The negative site is M, not the oxygen location.
        m_relative = .1546 * bisector
        dipole_eA = .5564 * (v1 + v2) - 1.1128 * m_relative
        dipole_magnitude = np.linalg.norm(dipole_eA, axis=1)
        dipole_direction = dipole_eA / dipole_magnitude[:, None]
        dipole_D = dipole_magnitude * 4.80320471257
        wall = typ == 5
        top = wall & (xyz[:, 2] > 0)
        bottom = wall & (xyz[:, 2] < 0)
        wall_gap = xyz[top, 2].mean() - xyz[bottom, 2].mean()
        history.append([step / 1000, wall_gap, angle.mean(), dipole_D.mean()])
        if 15000 <= step <= 30000:
            selection_times.append(step / 1000)
            geometry.extend(np.column_stack([l1, l2, angle, dipole_D]).tolist())
            for ion_type in (3, 4):
                ion_xyz = xyz[typ == ion_type]
                # delta points from the ion toward oxygen.
                delta = in_plane_image(xyz[oi][None, :, :] - ion_xyz[:, None, :], lengths)
                distance = np.linalg.norm(delta, axis=2)
                assert distance.min() > 0
                counts = (distance[..., None] <= radii).sum(axis=1)
                neighbour_records[ion_type].append(counts.mean(axis=0))
                # Normalize the reconstructed charge-weighted dipole itself.
                cosine = np.einsum("ijk,jk->ij", delta, dipole_direction) / distance
                orientation[ion_type].extend(cosine[distance <= cutoffs[ion_type]].tolist())
            for name, selection in {"water": typ <= 2, "Na": typ == 3,
                                    "Cl": typ == 4, "wall": wall}.items():
                masses = np.array([MASS[int(t)] for t in typ[selection]])
                mass_in_slice = np.histogram(xyz[selection, 2], bins=zedges, weights=masses)[0]
                # 1 A^3 = 1e-24 cm^3; input atomic masses are g/mol.
                volume_cm3 = lengths[0] * lengths[1] * np.diff(zedges) * 1e-24
                profiles[name].append(mass_in_slice / AVOGADRO / volume_cm3)
        last = (ids, typ, data)
    if not selection_times:
        raise ValueError("The selected 15--30 ps window contains no frames")
    ids, typ, data = last
    assert len(ids) == 1680
    counts = {str(t): int((typ == t).sum()) for t in range(1, 6)}
    assert counts == {"1": 406, "2": 812, "3": 15, "4": 15, "5": 432}
    assert abs(data["q"].sum()) < 1e-8
    hist = np.array(history)
    geom = np.array(geometry)
    thermo = np.loadtxt(args.run / "equilibrate-thermo.dat", comments="#")
    late = (thermo[:, 1] >= 15000) & (thermo[:, 1] <= 30000)
    summary = {
        "analysis_window_ps": [15, 30], "frames": len(selection_times),
        "type_counts": counts, "total_charge_e": float(data["q"].sum()),
        "temperature_K": sample_stats(thermo[late, 2]),
        "wall_center_gap_A": sample_stats(hist[hist[:, 0] >= 15, 1]),
        "OH_A": sample_stats(geom[:, :2].ravel()),
        "HOH_deg": sample_stats(geom[:, 2]), "water_dipole_D": sample_stats(geom[:, 3]),
        "geometry_count_water_frames": int(geom.shape[0]),
        "neighbour_counts": {}, "orientation_cosine": {},
        "interpretation": "Correlated finite-window descriptors. No independent-sample error bars or bulk homogeneous RDF normalization."
    }
    for it, name in [(3, "Na"), (4, "Cl")]:
        index = int(np.argmin(abs(radii - cutoffs[it])))
        assert abs(radii[index] - cutoffs[it]) < 1e-12
        summary["neighbour_counts"][name] = {"radius_A": cutoffs[it],
                                              **sample_stats(np.array(neighbour_records[it])[:, index])}
        summary["orientation_cosine"][name] = {"radius_A": cutoffs[it], **sample_stats(orientation[it])}
    (args.out / "hydration_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    def finish(fig, stem):
        for suffix in ("svg", "png"):
            fig.savefig(args.out / f"{stem}.{suffix}", dpi=180, bbox_inches="tight")
        plt.close(fig)

    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True, layout="constrained")
    axes[0].plot(thermo[:, 1] / 1000, thermo[:, 2], color="#167d84")
    axes[0].axhline(300, color="#819394", linestyle="--")
    axes[0].set_ylabel(tr("全体系温度 / K", "Whole-system T / K"))
    axes[1].plot(hist[:, 0], hist[:, 1], color="#c16b3d")
    axes[1].set_ylabel(tr("两壁质心间距 / Å", "Wall-centre separation / Å"))
    axes[1].set_xlabel(tr("准备时间 / ps", "Preparation time / ps"))
    for ax in axes:
        ax.axvspan(15, 30, alpha=.08, color="#167d84")
        ax.set_xlim(0, 30)
        ax.grid(axis="y", alpha=.15)
    axes[0].set_title(tr("固定盒子中的升温与壁面重排；阴影为结构统计窗口", "Heating and mobile walls in a fixed box; shading marks the structural window"))
    finish(fig, "electrolyte-preparation")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), layout="constrained")
    for it, name, color in [(3, "Na⁺", "#466eaa"), (4, "Cl⁻", "#c16b3d")]:
        neighbour = np.array(neighbour_records[it]).mean(axis=0)
        axes[0].plot(radii, neighbour, label=name, color=color, linewidth=2)
        axes[0].scatter([cutoffs[it]], [np.interp(cutoffs[it], radii, neighbour)], color=color)
        axes[1].hist(orientation[it], bins=np.linspace(-1, 1, 31), density=True,
                     histtype="step", linewidth=2, color=color,
                     label=f"{name}, r ≤ {cutoffs[it]:.1f} Å")
    axes[0].set_xlabel(tr("离子—氧距离阈值 / Å", "Ion–oxygen distance threshold / Å"))
    axes[0].set_ylabel(tr("每个离子的平均邻近水数", "Mean neighbouring waters per ion"))
    axes[0].set_title(tr("直接计数的累积邻近水", "Cumulative water-neighbour counts"))
    axes[1].set_xlabel(tr("水的偶极方向与离子向外径向的余弦", "Cosine: water dipole vs outward radial direction"))
    axes[1].set_ylabel(tr("概率密度", "Probability density"))
    axes[1].set_title(tr("给定距离窗口内的水朝向", "Water orientation within stated distance windows"))
    for ax in axes:
        ax.legend(frameon=False)
        ax.grid(axis="y", alpha=.15)
    finish(fig, "hydration-structure")
    np.savetxt(args.out / "neighbour_counts.csv",
               np.column_stack([radii, np.array(neighbour_records[3]).mean(axis=0),
                                np.array(neighbour_records[4]).mean(axis=0)]),
               delimiter=",", header="radius_A,Na_mean_waters,Cl_mean_waters", comments="")

    fig, axes = plt.subplots(2, 1, figsize=(12, 7.5), sharex=True, layout="constrained")
    pmean = {k: np.array(v).mean(axis=0) for k, v in profiles.items()}
    axes[0].plot(zmid, pmean["water"], label=tr("水", "Water"), color="#167d84")
    axes[0].plot(zmid, pmean["wall"], label=tr("壁原子", "Wall atoms"), color="#89999c")
    axes[1].plot(zmid, pmean["Na"], label="Na⁺", color="#466eaa")
    axes[1].plot(zmid, pmean["Cl"], label="Cl⁻", color="#c16b3d")
    axes[1].set_xlabel("z / Å")
    for ax in axes:
        ax.set_ylabel(tr("质量密度 / g cm⁻³", "Mass density / g cm⁻³"))
        ax.legend(frameon=False)
        ax.grid(axis="y", alpha=.15)
        ax.set_xlim(-20.2, 20.2)
    axes[0].set_title(tr("沿限域方向的切片密度：15–30 ps，切片宽0.5 Å", "Density across confinement: 15–30 ps, 0.5 Å slices"))
    finish(fig, "electrolyte-density")
    np.savetxt(args.out / "density_profiles.csv",
               np.column_stack([zmid] + [pmean[k] for k in ("water", "Na", "Cl", "wall")]),
               delimiter=",", header="z_A,water_g_cm3,Na_g_cm3,Cl_g_cm3,wall_g_cm3", comments="")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

Use the command in the file header to analyze the example directory; --language zh or en selects figure labels.

The complete program connects reading, geometric reconstruction, statistics, and plotting. It sorts by atom ID, checks that the two IDs following each oxygen belong to hydrogens in the same water, and verifies charge and atom-type counts. It then calculates constrained geometry, dipole directions, neighbour counts, and mass density along z. The Na⁺ distance window contains 2,283 ion–water pair observations with a mean orientation cosine near 0.680; the Cl⁻ window contains 3,324 with a mean near −0.426. These are observations of local pairs that may reappear, so their count does not provide an independent sample count. Summary values and curve data are saved together, preserving the distance and time definitions behind each displayed result.

### Water counts and orientation distributions around ions

Statistics use 31 frames from 15–30 ps and 15 ions of each type. Reporting radii are 3.3 Å for Na⁺ and 3.9 Å for Cl⁻, giving 2,283 and 3,324 orientation-pair observations.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l06/en/#en-s7)

Water-oxygen neighbour counts and the cosine between ion-to-water and water-dipole directions in 31 frames from 15–30 ps. Radii are 3.3 Å for Na⁺ and 3.9 Å for Cl⁻. Each ion–neighbour-water pair contributes an orientation observation; a water can appear at several saved times.

## From local hydration to interfaces: returning averages to space

Next divide the slit into thin slices along z, each 0.5 Å thick with a cross-sectional area equal to the x length multiplied by the y length. For every frame, add the masses of water, sodium, chloride, and wall atoms in each slice separately, divide by its physical volume, and average over the selected time window. The result is a mass-density profile across confinement. Thinner slices resolve finer spatial detail but contain fewer particles and therefore fluctuate more strongly. Choosing slice thickness balances spatial resolution and statistical variation. A sharper peak is not automatically a more faithful description; its persistence should be examined as the bin width and observation window change.

Measure mass density within a physical slice volumeEq. 7

![Measure mass density within a physical slice volume](https://ml-biomat.com/static/agent-math/faa289b21865b52afc9a2080.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ρk | Mean mass density of selected particles in slice k | g cm⁻³ |
| mi | Molar mass assigned to atom i | g mol⁻¹ |
| NA | Avogadro constant, 6.02214076 × 10²³ | mol⁻¹ |
| A | Slice cross-sectional area, converted to cm² here | cm² |
| Δz | Slice thickness, converted to cm here | cm |
| Nf, f, i, k(f) | Frame count, frame index, atom index, and atoms occupying slice k in frame f | 1 |
| Σ, ∈, /, ×, = | Sum over frames and atoms belonging to the slice; divide by frame count, Avogadro constant, and volume; adjacent factors multiply; equality defines | 1 |

Reading the relationshipDivide molar mass by Avogadro’s constant for one-atom mass, divide by slice volume, and average over frames.

A worked exampleA 24.24 Å × 24.24 Å × 0.5 Å slice has volume 293.7888 Å³ = 2.937888 × 10⁻²² cm³. Ten complete waters have mass 10 × 18.0154/NA grams, giving about 1.01826 g/cm³.

ConditionsAssign mass atom by atom and analyze water, ions, and walls separately. A charge-density analysis must additionally place the TIP4P negative charge at M.

Avogadro’s constant enters because input atomic masses are expressed in g/mol, while a slice contains a finite number of atoms. Dividing molar mass by the number of particles in a mole gives the mass of one atom in grams. Length units must also agree: 1 Å equals 10⁻⁸ cm, so 1 Å³ equals 10⁻²⁴ cm³. A slice measuring 24.24 Å by 24.24 Å by 0.5 Å has a volume of about 293.789 Å³. If it contains exactly ten complete water molecules at one instant, its water mass density is approximately 1.018 g/cm³. The program actually assigns mass atom by atom, so a water spanning two slices contributes oxygen and hydrogen masses to their respective slices while preserving total mass.

### Actual mass density across the slit

Slices are 0.5 Å thick and normalized by the physical cross-sectional area. Water, walls, and both ions are shown separately, averaged over 15–30 ps.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l06/en/#en-s8)

Mass density in 0.5 Å slices along z, averaged over 15–30 ps. Each slice uses the actual cross-sectional area and thickness. Water, walls and the two ion types are shown separately, preserving the inhomogeneous slit distribution.

The actual profiles show narrow layers of wall atoms and stronger water layering near the walls than in the central region. The smaller ion population produces more irregular sodium and chloride profiles, and the two sides are not perfectly symmetric within this finite observation window. Mass density also includes differences in particle mass: chloride is heavier than sodium, so equal ion counts can still produce a higher chloride mass density. Comparing ion enrichment calls for number density or slice counts; comparing the distribution of water and solid mass suits the present mass-density definition. Identifying exactly what the vertical axis measures is essential before interpreting a change in peak height.

The same measurement sequence can be carried into a biomaterials problem. Establish the charge state of the polymer or surface, select the water and ion parameter set, and choose either a bulk box or a pore geometry. With those conditions defined, compare water neighbours, orientation distributions, and spatial concentration. If salt content is the variable, record actual ion counts, the volume used to define concentration, and the neutrality condition. When the material itself is charged, distinguish counterions required for neutralization from additional salt. This makes it possible to separate how an ionic environment changes local chain structure instead of grouping every change under an imprecise statement that salt was added.

The salt solution now has several connected descriptions. Charges and parameters define its interactions; constraints define the internal shape of water; the trajectory supplies actual arrangements; neighbour counts and orientations describe hydration; and slice densities locate structure relative to the interface. These solvent concepts remain useful when we turn to a polymer chain. Extension, coiling, and response to an external force all occur within an interacting molecular environment. The next lesson focuses on the chain itself, using end-to-end distance and radius of gyration to distinguish how far it extends from how much space its atoms occupy, and relating those geometric measures to molecular interactions.

## Further Reading and Open Materials

- [Nanosheared electrolyte — A Set of Tutorials for the LAMMPS Simulation Package](https://lammpstutorials.github.io/sphinx/build/html/tutorial4/nanosheared-electrolyte.html) · Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, Axel Kohlmeyer · CC BY 4.0

  Construction and preparation of a TIP4P/2005 confined electrolyte.

  Original model and preparation parameters retained; numerical trajectories, local hydration analysis, and bilingual explanations added. Shear is developed in a later lesson.
- [TIP4P and OPC water models; lj/cut/tip4p pair styles](https://docs.lammps.org/Howto_tip4p.html) · LAMMPS developers · Official technical documentation; referenced for definitions and parameters

  Verification of TIP4P/2005 geometry, charges, and implicit M-site treatment.

  Geometry figures and formula explanations are newly developed.
- [pair_style lj/cut/tip4p/long](https://docs.lammps.org/pair_lj_cut_tip4p.html) · LAMMPS developers · Official technical documentation; referenced for implementation definitions

  Consecutive O/H/H IDs, M-site charge handling, and geometric mixing.

  Explained through the complete input and an analytic orientation exercise.
- [fix shake and kspace_modify commands](https://docs.lammps.org/fix_shake.html) · LAMMPS developers · Official technical documentation; referenced for algorithm definitions

  Constraints, strong harmonic restraints during minimization, and algorithm history.

  Added checks of initial geometry against actual records.
- [kspace_modify — slab geometry](https://docs.lammps.org/kspace_modify.html) · LAMMPS developers · Official technical documentation; referenced for numerical geometry

  Extended slab volume and the approximation to two-dimensional periodic electrostatics.

  New schematic distinguishes physical and extended regions.
- [Svante Arrhenius — Facts; The development of modern chemistry](https://www.nobelprize.org/prizes/themes/the-nobel-prize-in-chemistry-the-development-of-modern-chemistry/) · Nobel Prize Outreach · Historical source cited; archival images are not reused

  Historical context of the 1884 work and electrolytic dissociation.

  An original conceptual drawing illustrates ionic lattices and hydration.
- [A general purpose model for the condensed phases of water: TIP4P/2005](https://doi.org/10.1063/1.2121687) · J. L. F. Abascal and C. Vega · Research article citation; model parameters cross-checked against official documentation

  Identity, authorship, and 2005 context of the water model.

  Original illustrations explain molecular geometry and charge distribution.
