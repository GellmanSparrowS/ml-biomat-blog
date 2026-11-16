# How Molecules Assemble into Aggregates

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l13/en/
Language: en

Run a two-dimensional amphiphile model, follow its actual assembly trajectory, and measure aggregates using periodic distances and graph connectivity.

## From detergents to molecules that assemble

When clean water meets an oily surface, the water and oil often remain in separate regions. A suitable surfactant changes the situation because different parts of the same molecule prefer different surroundings. One part interacts favourably with water, while another favours a less polar environment. A molecule with these two tendencies is called an amphiphile. Under suitable conditions, many amphiphiles can organize into aggregates that concentrate their less water-friendly parts and expose more of their water-friendly parts to the surrounding solution. This organization connects a molecular idea to familiar uses in washing, dispersion, emulsification, and the design of soft materials.

Self-assembly describes the emergence of a larger organization through molecular interactions and thermal motion. Each molecule continues to move, collide, separate, and change its neighbours; no controller assigns its final position. A rough everyday analogy is a moving crowd carrying objects with different surface preferences: local contacts can influence how the crowd organizes even though nobody directs the complete arrangement. Molecules also have fixed internal connections, and temperature and concentration influence which arrangements are accessible. The present example makes those ingredients explicit in a simple head-and-tail model, then follows an actual trajectory to measure the aggregates that appear.

The case is adapted from the two-dimensional micelle example distributed with LAMMPS. Each amphiphile contains one head bead and two tail beads, accompanied by separate solvent beads. There are 150 amphiphiles and 750 solvent beads moving in the xy plane. The model retains connectivity, thermal motion, and differences in the interactions of heads and tails with their surroundings. These ingredients make it useful for studying segregation, aggregation, and geometric statistics. The beads are effective interaction centres without charges or a chemical mapping to a particular detergent. A study of a named surfactant, its salt response, or its specific chemistry would add the corresponding molecular mapping and interaction parameters.

### The actual planar assembly trajectory

Starts at t = 0 after soft preparation and continues to 505τ, preserving particle and molecular identities.

The official planar micelle model: 750 solvent beads and 150 three-bead amphiphiles, 1200 beads in total. After soft-potential preparation, the original LJ parameters, velocity-rescaling temperature control and planar constraint are retained: T*=0.45, timestep 0.005τ, production time 0–505τ.

[Download reference data and complete inputs (ZIP) 4.93 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-micelle-reference-data.zip)

Every frame in the player comes from the LAMMPS calculation. First look for regions where tails accumulate, then examine whether heads tend to face the surrounding solvent. Also watch the box edges: an aggregate crossing one edge continues through the opposite edge. The analysis turns these observations into three reproducible questions. How many connected groups are present? How many molecules belong to the largest group? How many solvent neighbours surround a head or a tail bead? These measurements describe the overall organization, its larger aggregates, and its local environment, giving complementary information about the same coordinates.

The calculation uses reduced units. A common length scale is denoted by σ, an energy scale by ε, and all bead masses have the numerical value 1. Together these scales define the time unit τ. The reduced temperature of 0.45 specifies thermal energy relative to ε. Reduced units let us examine relationships between interactions before assigning physical units to a particular material. This trajectory reaches 505τ, so the plots retain τ on their time axes. Conversion to nanoseconds requires an additional physical calibration. The aim is to follow the complete route from a model definition to a trajectory, a clustering algorithm, and a clear statement of what the resulting statistics count.

## Why soap solutions prompted the study of micelles

Soap solutions posed a concrete problem for early colloid chemistry. They displayed some properties associated with electrolytes, yet also contained organization larger than ordinary individual molecules. What objects were actually moving through the solution? In their 1920 work on soap solutions, McBain and Salmon discussed colloidal electrolytes and considered charged aggregates together with their associated solvent. McBain's subsequent discussion of colloids also addressed the relationship between ordinary molecules and larger colloidal particles. Electrical measurements, solution properties, and structural ideas had to be interpreted together. The [original 1920 paper](https://doi.org/10.1021/ja01448a010) and [the 1921 discussion](https://www.nature.com/articles/107046a0) provide a historical route into this question.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l13/en/#en-s2)

Figure 1 · Soap solutions prompted discussion of charged aggregates and their hydration. The apparatus and aggregate are principle schematics linking measurable properties to units of organization in solution.

This history helps clarify why the word “particle” can mean different things in different measurements. In a chemical formula, one surfactant molecule has a defined composition. In solution, several such molecules may form a common aggregate. A structural measurement may then treat that aggregate as a larger object. Aggregation does not automatically turn the constituent molecules into a new covalent macromolecule: noncovalent contacts can maintain their organization while molecular identities remain intact. Counting molecules and counting aggregates therefore answers questions at different levels. Later, a single saved frame will contain both 150 amphiphile molecules and 12 connected components. Those numbers describe different objects in the same configuration.

The familiar head-and-tail picture gives a spatial interpretation of this organization. In an aqueous environment, hydrophilic parts tend to maintain contact with the solvent, while grouping hydrophobic parts reduces their exposure to water. Molecular shape, interactions, temperature, and composition all help determine the resulting structure. In real water, solvent organization and entropy contribute to hydrophobic effects. Here, simple solvent beads and selected pair interactions express effective preferences, making the associated segregation easier to follow. The charged soap discussed historically and the uncharged model used here serve two related purposes: one introduces a phenomenon requiring explanation, while the other isolates a small set of mechanisms in controlled conditions.

Spatial dimension also matters when naming structures. An ordinary three-dimensional micelle has an interior and an outer surface. A bilayer has two solvent-facing sides around a hydrophobic region. An aggregate in the present model has an inside and an outside within a plane. Interpreting that planar object as a three-dimensional sphere would add assumptions about volume, curvature, and molecular packing. We therefore describe the measured structures as two-dimensional aggregates and use “micelle model” for the head-and-tail segregation problem being represented. Questions about spherical aggregation numbers, membrane thickness, or three-dimensional curvature call for a three-dimensional system and measurements appropriate to that geometry.

The historical task of inferring structure from observations remains relevant when analysing coordinates. A picture can suggest that molecules are together, but a numerical count requires a definition of “together.” A brief contact between two smaller groups may join them under one distance criterion. Conversely, a large group crossing a periodic edge may look like two pieces on a flat image. The calculation must specify its observation scale and examine how the conclusion changes when that scale changes. The interactive example later in the chapter lets you alter a contact threshold while keeping the actual molecular coordinates fixed, making this distinction visible.

## What one head and two tail beads retain

The model contains four bead types. Type 1 comprises 750 solvent beads. Type 2 comprises 150 heads, while types 3 and 4 comprise 150 middle-tail and 150 terminal-tail beads. Each amphiphile follows the sequence 2–3–4. Thus, the 150 molecules contain 450 beads and 300 bonds. A molecule identifier groups its three beads; an atom identifier tracks a particular bead through the trajectory; a type identifier selects its interaction parameters. These identifiers serve separate purposes. Keeping their roles clear is especially useful when sorting trajectory records, reconstructing molecules, or assigning a cluster colour to all beads belonging to the same molecule.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l13/en/#en-s3)

Figure 2 · The model retains head–tail contrast, different tail size parameters, and molecular connectivity. Beads are effective interaction centres; colours identify types, and drawn circles are symbols.

The two connections within each molecule use harmonic bonds with an equilibrium length of 0.75σ and a LAMMPS coefficient of 50 ε/σ². A harmonic bond behaves like a spring near its preferred length: compressing or stretching it raises the energy, and larger deviations cost more. There are no additional angle or torsion potentials, so the three-bead molecule can bend in the plane. Nonbonded interactions and its surroundings still influence which folded shapes are accessible. Although this molecule is short, it already possesses an internal head-to-tail organization. That organization distinguishes it from a fluid made of separate, unconnected particles.

Two bonds connect three beads into one moleculeEq. 2

![Two bonds connect three beads into one molecule](https://ml-biomat.com/static/agent-math/b9f78e87a55b157cf86cc200.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| U_{b} | Potential energy of one harmonic bond | reference ε |
| K_{b} | LAMMPS harmonic coefficient, including the usual one-half factor | ε/σ² |
| r、r₀ | Current bond length; equilibrium length 0.75σ | σ |
| −、²、= | Length difference; square; equality; multiplication of the coefficient and squared difference | operators |

Reading the relationshipDepartures from the equilibrium length raise energy. Equal extensions and compressions have the same energy cost. Each amphiphile has two such connections.

A worked exampleWith K_b = 50 ε/σ² and r₀ = 0.75σ, r = 0.85σ gives U_b = 50 × 0.10² = 0.5ε. The energy is the same at r = 0.65σ.

ConditionsNo angle or dihedral potential is used here. The special_bonds fene setting specifies nonbonded weights; it does not change these harmonic bonds into FENE bonds.

The command `special_bonds fene` can be confusing on a first reading. In this input, “fene” names a preset for nonbonded weighting along a bond graph. The weights for pairs separated by one, two, and three bonds are 0, 1, and 1. The actual bond potential remains the one specified by `bond_style harmonic`. Consequently, directly connected head–middle-tail and middle-tail–terminal-tail pairs omit the ordinary LJ contribution, while the head and terminal tail retain their nonbonded interaction. Bond energy and nonbonded exclusions are separate settings. Reading them separately reveals which terms control stretching, bending freedom, and close approaches within the molecule.

Both in-plane box lengths are 35.85686σ. Dividing 1200 beads by the box area gives an actual bead number density of approximately 0.933333 σ⁻². The corresponding amphiphile number density is approximately 0.116667 σ⁻². The original construction description also contains a density of 0.7. That value concerns 900 initial lattice sites: 150 sites become heads, after which 300 tail beads are added. Adding those tails increases the total bead density. All these quantities are areal densities. The narrow z extent written into the two-dimensional data file is a geometric setting; the physical organization examined here occupies a plane.

The preparation check reads the supplied `data.micelle` file directly. It verifies its checksum, the population of each bead type, the three-bead composition of each amphiphile, the two bonds forming every 2–3–4 chain, and zero z coordinates. These checks establish a stable molecular identity for the subsequent analysis. A cluster algorithm can then treat each molecule as a well-defined node instead of repeatedly guessing which beads belong together. The example package retains the original data file. The simulation starts from these coordinates, first prepares nearby contacts with a soft repulsion, and then changes to the interactions used for the main observation period.

### Check molecules and connectivity

```
"""Inspect the supplied micelle data before running LAMMPS.

python check_micelle.py --data data.micelle
Uses only the Python standard library.
"""
from pathlib import Path
from collections import Counter, defaultdict
import argparse
import hashlib
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, default=Path('data.micelle'))
    args = parser.parse_args()
    expected = '35d33cbc97b1862bc46dd18ee52fec5f6dd879436cf12fbc6d0bb6ba9a803c8c'
    actual = hashlib.sha256(args.data.read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError('The data.micelle checksum differs from the supplied example.')
    atoms = {}; bonds = []; box = []; section = None
    for raw in args.data.read_text().splitlines():
        line = raw.split('#', 1)[0].strip()
        if not line:
            continue
        fields = line.split()
        if fields[-1] in ['xhi', 'yhi', 'zhi']:
            box.append([float(fields[0]), float(fields[1])])
        elif line in ['Masses', 'Atoms', 'Bonds', 'Angles', 'Dihedrals', 'Velocities']:
            section = line
        elif section == 'Atoms' and fields[0].isdigit():
            aid, mol, typ = map(int, fields[:3])
            if aid in atoms:
                raise ValueError('Duplicate atom identifier.')
            atoms[aid] = (mol, typ, tuple(map(float, fields[3:6])))
        elif section == 'Bonds' and fields[0].isdigit():
            bonds.append(tuple(map(int, fields)))
    counts = Counter(a[1] for a in atoms.values())
    molecules = defaultdict(list)
    for aid, (mol, typ, xyz) in atoms.items():
        if xyz[2] != 0:
            raise ValueError('Every particle must start in the xy plane.')
        if typ != 1:
            molecules[mol].append(aid)
    if counts != {1: 750, 2: 150, 3: 150, 4: 150} or len(molecules) != 150 or len(bonds) != 300:
        raise ValueError('Unexpected particle or bond counts.')
    for mol, ids in molecules.items():
        if sorted(atoms[i][1] for i in ids) != [2, 3, 4]:
            raise ValueError('Each molecule needs a head and two distinct tail types.')
        local = [b for b in bonds if b[2] in ids or b[3] in ids]
        pairs = {tuple(sorted([atoms[b[2]][1], atoms[b[3]][1]])) for b in local}
        if len(local) != 2 or pairs != {(2, 3), (3, 4)}:
            raise ValueError('The two bonds must form a head-middle-tail chain.')
        if any(atoms[b[2]][0] != mol or atoms[b[3]][0] != mol for b in local):
            raise ValueError('A bond crosses molecular identities.')
    area = (box[0][1] - box[0][0]) * (box[1][1] - box[1][0])
    print(json.dumps({'data_sha256': actual, 'particles': len(atoms), 'types': dict(counts),
                      'amphiphiles': len(molecules), 'bonds': len(bonds),
                      'bead_areal_density': len(atoms) / area,
                      'amphiphile_areal_density': len(molecules) / area,
                      'dimensions': 2}, indent=2))


if __name__ == '__main__':
    main()
```

Run python check_micelle.py --data data.micelle to inspect the supplied data, 150 three-bead chains, and planar number density.

## From a soft preparation to the main interactions

A newly constructed arrangement can contain beads that are very close together. Applying a steep LJ repulsion immediately can generate large local forces and make integration difficult. The original example therefore begins with a bounded soft potential. Its strength increases from 1 to 20 over 1000 steps, gradually separating close neighbours while harmonic bonds maintain molecular connectivity. This stage prepares the geometry under a nonbonded potential different from that of the main simulation. Afterwards, the soft-strength control is removed and the pair style changes to `lj/cut`, retaining the particle identities and the coordinates reached during preparation.

The Lennard–Jones potential contains two competing contributions. Repulsion grows more rapidly at short separation, whereas attraction dominates over a somewhat longer range. Each type pair has its own size parameter σᵢⱼ, which sets both the zero of the potential and the position of its minimum. The cutoff r_{c,ij} determines how far the interaction is retained. All pair energy parameters in this example have the numerical value 1, but the sizes and cutoffs differ. Solvent–solvent, head–head, and solvent–head interactions use σᵢⱼ = 1 and a cutoff of 2.5σ, retaining a substantial attractive region. Tail pairs 3–3, 4–4, and 3–4 use size parameters 0.75, 0.50, and 0.67 respectively, all with the same absolute cutoff of 2.5σ.

Reading the LJ interaction between bead typesEq. 1

![Reading the LJ interaction between bead types](https://ml-biomat.com/static/agent-math/1063501ec3d59262028abc37.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Uᵢⱼ(r) | Nonbonded potential of two beads of types i and j at separation r | energy in units of the reference ε |
| i、j | Particle-type indices 1 through 4 | dimensionless |
| r、σᵢⱼ、r_{c,ij} | Centre separation; zero-crossing length of that pair; pair cutoff | length in units of the reference σ |
| εᵢⱼ | Well-depth parameter, equal to one reference ε for all pairs here | energy |
| 4、12、6 | Constants in the LJ form; twelfth and sixth powers | dimensionless |
| /、−、[ ]、=、< | Division; subtraction; grouping; equality; strictly less than; multiplication of adjacent factors | operators |

Reading the relationshipThe twelfth-power term grows faster at short separation and produces repulsion; the sixth-power term gives attraction farther out. The cutoff selects the part of the interaction that remains active.

A worked exampleFor σᵢⱼ = 1 and εᵢⱼ = 1, r = 1 gives U = 0. At r = 2^(1/6) ≈ 1.122462, U = −1. For σᵢⱼ = 0.88, the minimum moves to about 0.987767.

ConditionsApplies to nonbonded pairs retained by special_bonds. This example uses unshifted lj/cut, with zero potential beyond the cutoff. Interpret the energy discontinuity separately from the attractive or repulsive direction of the force.

Solvent–tail pairs use σᵢⱼ = 1 and a cutoff of 1.12246σ, close to the minimum of that LJ potential. The retained force is consequently repulsive over almost the entire retained interval. Head–middle-tail and head–terminal-tail pairs use the same absolute cutoff, but their size parameters are 0.88 and 0.75. Their minima are approximately 0.987767σ and 0.841847σ, so an attractive interval remains between each minimum and the cutoff. A common numerical cutoff therefore does not retain the same portion of every pair potential. The diagram compares these intervals directly, helping connect the actual parameters to the direction of the force.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l13/en/#en-s4)

Figure 3 · Here σ denotes the shared reference length. Pair-specific σᵢⱼ values are 1, 0.88, and 0.75 reference units, so the same absolute cutoff retains different force ranges. The diagram begins at 0.5σ.

The main stage keeps the original velocity-rescaling thermostat. Every 100 steps it checks the temperature against a target of 0.45 and a permitted window of 0.02; when correction is required, a fraction of 1.0 restores the target. The `fix nve` command integrates positions and velocities, `temp/rescale` adjusts temperature, and `enforce2d` maintains zero z velocity and force. The name of the integration fix does not specify the thermodynamic behaviour of every other operation in the input. This combined protocol supports the original demonstration of segregation and assembly. A study of equilibrium fluctuations or dynamical transport would choose and test a thermostat suited to those measurements and their time scales.

### Complete input for planar assembly

```
# 2d micelle simulation

dimension	2

neighbor	0.3 bin
neigh_modify	delay 5

atom_style	bond

# Soft potential push-off

read_data	data.micelle
special_bonds	fene

pair_style	soft 1.12246
pair_coeff	* * 0.0 1.12246

bond_style 	harmonic
bond_coeff	1 50.0 0.75

velocity	all create 0.45 2349852

variable	prefactor equal ramp(1.0,20.0)

fix		1 all nve
fix		2 all temp/rescale 100 0.45 0.45 0.02 1.0
fix		3 all adapt 1 pair soft a * * v_prefactor
fix		4 all enforce2d

thermo		50

# Whole-system energies; LJ reduced units, a two-dimensional model.
compute cTemp all temp
compute cPE all pe
compute cKE all ke
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE
variable K equal c_cKE
variable E equal c_cPE+c_cKE
thermo_style custom step time c_cTemp c_cPE c_cKE etotal
thermo_modify norm no
fix record all ave/time 50 1 50 v_clock v_T v_U v_K v_E file soft-thermo.dat format " %.15g"
dump trajectory all custom 250 soft.lammpstrj id mol type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
run 1000
unfix record
undump trajectory
write_data after-soft.data pair ij

unfix		3

# Main run

pair_style	lj/cut 2.5

# solvent/head - full-size and long-range

pair_coeff	1 1 1.0 1.0 2.5
pair_coeff	2 2 1.0 1.0 2.5
pair_coeff	1 2 1.0 1.0 2.5

# tail/tail - size-averaged and long-range

pair_coeff	3 3 1.0 0.75 2.5
pair_coeff	4 4 1.0 0.50 2.5
pair_coeff	3 4 1.0 0.67 2.5

# solvent/tail - full-size and repulsive

pair_coeff	1 3 1.0 1.0 1.12246
pair_coeff	1 4 1.0 1.0 1.12246

# head/tail - smaller sigma and short absolute cutoff;
# the interval between the pair-specific minimum and cutoff is attractive

pair_coeff	2 3 1.0 0.88 1.12246
pair_coeff	2 4 1.0 0.75 1.12246

thermo		50

#dump		1 all atom 2000 dump.micelle

#dump		2 all image 2000 image.*.jpg type type zoom 1.6
#dump_modify	2 pad 5 adiam 1 0.5 adiam 2 1.5 adiam 3 1.0 adiam 4 0.75

#dump		3 all movie 2000 movie.mpg type type zoom 1.6
#dump_modify	3 pad 5 adiam 1 0.5 adiam 2 1.5 adiam 3 1.0 adiam 4 0.75

reset_timestep 0
fix record all ave/time 100 1 100 v_clock v_T v_U v_K v_E file micelle-thermo.dat format " %.15g"
dump trajectory all custom 500 micelle.lammpstrj id mol type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
run 1000
write_restart original-example.restart
write_data original-example.data pair ij
# Extend observation with the same Hamiltonian, integrator and thermostat.
run 100000
write_restart micelle.restart
write_data micelle.data pair ij
```

Retains the official parameters, preparation, and original 1000-step main interval, followed by 100000 additional steps. Records whole-system energies and coordinates with molecular identities.

The complete input runs 1000 soft-preparation steps and then resets the main step counter to zero. The LJ stage first runs the original 1000 steps, followed by another 100000 steps with the same interactions, temperature settings, and integrator. At a timestep of 0.005τ, the original main segment ends at 5τ and the complete main segment at 505τ. Soft preparation took another 5τ before this plotted time origin. A trajectory frame is saved every 500 steps, or every 2.5τ, yielding 203 frames including the initial frame. The shell script saves the LAMMPS log so that the executed settings and numerical messages remain available alongside the trajectory.

### Run the model and retain its logs

```
#!/usr/bin/env bash
set -euo pipefail
lmp=${LAMMPS:-lmp}
export OMP_NUM_THREADS=2
"$lmp" -in in.micelle -log micelle.log > micelle.stdout.log 2>&1
```

Run bash run.sh, which calls lmp by default. The executable needs the MOLECULE package and the soft, lj/cut, adapt, temp/rescale, and enforce2d commands.

## Reading the actual temperature and structural changes

Before interpreting a trajectory, it is useful to check a numerical relation involving degrees of freedom. Each two-dimensional point particle has x and y velocity components. The default temperature calculation subtracts two degrees of freedom for overall translation, leaving 2398 translational degrees of freedom for 1200 beads. At a temperature of 0.45, the total kinetic energy is consequently 539.55ε, or approximately 0.449625ε per bead. The output records total potential, kinetic, and total energies; division by 1200 occurs during plotting. Establishing this order prevents a second normalization and ensures that the temperature is interpreted using the actual two-dimensional degrees of freedom.

Temperature and total kinetic energy in two dimensionsEq. 3

![Temperature and total kinetic energy in two dimensions](https://ml-biomat.com/static/agent-math/8b93bd1a92f84d0ea8bb2e48.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| K | Total translational kinetic energy | ε |
| N | Total of 1200 particles, including solvent, heads, and tails | dimensionless |
| k_{B}、T | Boltzmann constant; temperature, with k_B numerically one in LJ units | k_B T has energy units |
| 2N−2 | Two directions per bead, minus two collective translational degrees of freedom | dimensionless degree-of-freedom count |
| 2、−、/、= | Each quadratic degree contributes k_B T/2; subtraction; division; equality; multiplication of adjacent factors | constant and operators |

Reading the relationshipThe temperature computation distributes kinetic energy over the counted degrees of freedom. Each planar point particle has x and y velocity components, with collective translation removed from the default count.

A worked exampleAt T* = 0.45, K = 1199 × 0.45 = 539.55ε, or 0.449625ε per particle. A three-dimensional 3N−3 count would add a direction that this model does not have.

ConditionsApplies to the unconstrained planar point beads and default temperature degrees of freedom here. Periodic velocity rescaling is the thermostat; this identity checks the record definitions.

### Temperature control and potential-energy change

Temperature is in LJ units and energies are normalized by all 1200 beads. Velocity rescaling remains active.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l13/en/#en-s5)

Native temperature and per-bead potential and kinetic energies in LJ reduced units. Temperature rescaling remains active throughout production and is part of the interpretation of energy relaxation and fluctuations.

The recorded mean temperature is approximately 0.451128, with fluctuations around the target. Potential energy decreases relatively quickly early in the main stage and changes more slowly later, as arrangements and interacting neighbours continue to adjust. Kinetic energy stays on a similar scale under temperature control. The energy curves describe this thermostatted evolution with an unshifted truncated potential. Relevant checks include the target temperature, the sum of potential and kinetic energies, and the consistency of identities and geometry. The analysis verifies the energy sum and the two-dimensional kinetic-energy relation for every saved thermodynamic record, connecting the plotted quantities to the settings that generated them.

The four coordinate panels show distinct stages of the actual calculation. At t = 0, soft preparation has just finished and the larger late-stage tail-rich regions have not yet developed. The frame at 5τ is the end of the original main segment, where some small neighbouring groups are already apparent. At 100τ and 505τ, tail-rich regions are more pronounced and many heads lie around them, with solvent occupying the remaining plane. Colour identifies bead type in these panels. It provides a structural view, while the quantitative membership of a cluster is assigned using the molecular identities and periodic distances defined in the next section.

### From a dispersed structure to larger aggregates

Actual coordinates at 0, 5, 100, and 505τ, coloured by solvent, head, and the two tail types in the periodic plane.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l13/en/#en-s5)

Actual planar coordinates at 0, 5, 100 and 505τ. Solvent is grey, heads teal, and the two tail types gold and red. Periodic box edges can split an aggregate in the picture; clustering uses periodic distances.

Periodic edges need careful attention. The left and right edges meet, as do the top and bottom, so a single aggregate can appear as separate pieces in a flat image. This display cut leaves actual neighbouring beads connected through the periodic geometry. To calculate a separation, the analysis chooses the shortest in-plane displacement between a bead and the periodic images of another. For example, in a box about 35.86σ wide, beads at x = 0.2σ and x = 35.6σ are only about 0.46σ apart along x. Their apparent separation across most of the displayed box would miss that close contact.

Different processes also have different time scales. Short-range repulsion can quickly resolve excessively close contacts, and a few molecules may form a small group early. Encounters between established groups, exchange of members, and internal rearrangement can take longer. A temperature curve fluctuating around its target therefore provides information distinct from the stability of an aggregate-size distribution. Showing both the original 5τ segment and the extended trajectory makes these different levels of organization visible. Local motion can remain controlled while larger structures continue to evolve. The cluster curves next quantify one aspect of that structural evolution.

## Recognizing a cluster from coordinates

A clustering calculation begins by choosing what one graph node represents. Here, each complete amphiphile is a node, giving 150 nodes; solvent beads are excluded. Two molecules receive an edge whenever any pair of their tail beads has a periodic minimum-image distance at or below the chosen threshold. Heads retain their molecular membership but do not define this tail-contact rule. The resulting graph records geometric proximity in a particular frame. The physical bonds remain the two harmonic connections inside each molecule. An edge in the analysis graph classifies a contact without adding a new bond to the simulation.

Connecting molecules by their tail-bead distanceEq. 4

![Connecting molecules by their tail-bead distance](https://ml-biomat.com/static/agent-math/f762e2d0bdfc39929fbdd0fd.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| A、B | Two different amphiphile molecules | molecular identities |
| 𝒯_A、𝒯_B | The two tail beads belonging to each molecule | sets |
| i、j | Tail-bead indices belonging to A and B, respectively | dimensionless |
| dᵢⱼ^PBC | Minimum-image xy distance between two tail beads | σ |
| d_{AB}、r_* | Nearest tail distance between the molecules; analysis threshold | σ |
| min、∈、≤、∼、if、= | Minimum; membership; less than or equal; graph adjacency; conditional rule; equality | operators |

Reading the relationshipAn edge is added when at least one tail pair is sufficiently close. Following these edges gives all reachable molecules. The threshold changes the grouping rule applied to the same coordinates.

A worked exampleIf the nearest A–B, B–C, and A–C tail distances are 1.1σ, 1.0σ, and 2.1σ, a threshold of 1.2σ still puts all three molecules in one component: A reaches C through B.

ConditionsAll 150 molecules are graph nodes; an isolated molecule is a size-one component. Interpret this geometrical definition together with morphology and threshold sensitivity.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l13/en/#en-s6)

Figure 4 · Each node is a complete amphiphile. Solid edges satisfy the nearest-tail distance threshold. A and C connect through B and share a component; D remains a size-one component.

A connected component consists of nodes reachable through a path of edges. If A contacts B and B contacts C, all three belong to one component even when A and C are farther apart than the threshold. Requiring every pair in a component to be close would instead split many extended aggregates. The implementation starts with 150 separate molecular sets, identifies tail pairs that satisfy the distance rule, and merges their corresponding sets. It then counts the molecules in each connected component. Summing all component sizes must return 150 in every frame, which provides a simple and useful conservation check for the analysis.

At a threshold of 1.2σ, the main-stage initial frame has 100 components, the largest containing 4 molecules. At 5τ there are 72 components, with 6 molecules in the largest. At 100τ the values are 35 and 10; at the final 505τ frame they are 12 and 36. These component counts include isolated molecules as components of size 1. The initial count is below 150 because some tail contacts already satisfy the 1.2σ criterion after soft preparation. Keeping the time origin and contact definition explicit explains this initial proximity without equating it with the larger structures seen at the end.

### Aggregation statistics at three thresholds

Connected components include size-one molecules. Each curve analyzes the same 203 frames.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l13/en/#en-s6)

Cluster counts and largest-cluster molecular populations in the same 203 frames at tail-contact thresholds of 0.9, 1.2 and 1.5σ. Each amphiphile is one node and size-one molecules are included; the curves show dependence on time and contact definition.

Changing the threshold to 0.9σ gives 15 final components, with a largest size of 23 molecules. At 1.5σ, the final counts are 12 and 36. A tighter rule can remove a loose bridge between groups, whereas a more permissive rule can join neighbouring regions. The interaction below uses the actual coordinates saved at 0, 5, 100, and 505τ. Moving the slider recomputes connectivity while every bead remains in its saved position. Colour identifies the current connected component. The same colour at opposite edges often reveals a periodic connection, showing how a classification rule acts on an unchanged molecular configuration.

Recompute clusters in the same actual saved frame by changing the tail-distance threshold.

Geometrical reclassification of four actual saved frames. Solvent beads are hidden, while all 450 beads of the 150 amphiphiles retain their coordinates. Colours follow components computed at the selected threshold.

Sensitivity to the threshold helps guide further analysis. If several nearby thresholds identify the same large aggregate, its internal head-and-tail distribution and shape become natural next measurements. If the largest size repeatedly jumps between two values, inspect whether a few transient contacts are joining two groups. A study of lifetimes could require contacts to persist for a specified duration or compare membership sets over time. Each additional rule defines a more specific observable. The present interaction keeps the basic instantaneous geometric rule visible, providing a clear starting point for those temporal measurements and helping avoid confusing a classification change with molecular movement.

## Why mean aggregate size has more than one meaning

Imagine a frame containing just two aggregates, one with 2 molecules and another with 8. Choosing an aggregate at random gives both equal weight, so their mean size is 5. Choosing a molecule at random instead gives an 80% chance of finding it in the larger aggregate; the mean size of the aggregate containing that molecule becomes 6.8. Both results are averages, but they answer different questions. The first emphasizes how aggregates are distributed by count, while the second emphasizes where molecules reside. Similar differences appear in materials measurements weighted by object number, mass, or scattering intensity. A mean aggregation number therefore needs its weighting rule alongside its value.

Choosing a cluster or a molecule as the observation unitEq. 5

![Choosing a cluster or a molecule as the observation unit](https://ml-biomat.com/static/agent-math/214afd67e71cd11cdbf80cf6.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| n、c_{n} | Number of molecules in a cluster; count of clusters of that size | dimensionless counts |
| n̄_cluster | Mean size with equal weight per cluster | molecules |
| n̄_molecule | Mean containing-cluster size for a randomly selected molecule | molecules |
| ∑ₙ、n²、/、= | Sum over all sizes; square; division; equality; multiplication of adjacent quantities | operators |

Reading the relationshipEach cluster contributes once to the first mean. A size-n cluster contains n molecules that can be selected, giving the extra factor n in the second mean.

A worked exampleFor clusters of sizes two and eight, the cluster mean is (2+8)/2 = 5, while the molecule mean is (2²+8²)/10 = 6.8. The final actual frame at r_* = 1.2σ gives 12.5 and 21.25333.

ConditionsSize-one components are included. Introducing a minimum aggregate size requires stating the selected population and both normalization denominators.

For the actual final frame at 1.2σ, the component sizes are 36, 23, 23, 22, 11, 10, 7, 6, 5, 3, 3, and 1. They sum to 150. Equal weighting of components gives 150/12 = 12.5 molecules per component. Weighting by molecules gives a sum of squared sizes of 3188, divided by 150, or 21.25333. Larger components contain more molecules and therefore contribute more strongly to the second average. The plot also shows the corresponding two normalized distributions: the fraction of components at a given size and the fraction of molecules belonging to components of that size. Each distribution separately sums to 1.

These bars describe the frame at 505τ and answer how molecules are distributed at that time. To describe a time interval, calculate distributions for individual frames and compare successive time blocks. Another weighting choice then appears. Normalizing each frame before averaging gives equal weight to each recorded time. Pooling all components across frames before normalization gives greater weight to times containing more components. Choose the definition that fits the question. The saving interval of 2.5τ is also a recording frequency: one aggregate may persist through many frames, so 203 frames follow one assembly history. Reproducibility of a late-stage distribution can be examined using different initial velocities and arrangements, then comparing matched observation windows.

### Aggregate size and different head–tail environments

Left: two weighted size distributions in the final frame at a 1.2σ threshold. Right: mean solvent neighbours per bead within 1.5σ.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l13/en/#en-s7)

Left: cluster-size distributions at 505τ and a 1.2σ threshold, weighted equally by cluster or by molecule. Right: mean solvent neighbours within 1.5σ of each head, middle tail and end tail. The two distributions correspond to different sampling questions.

The right-hand plot connects aggregate organization to local surroundings. In every frame, the analysis counts solvent beads within 1.5σ of each head, middle-tail, and terminal-tail bead, then averages over beads of the same type. At 505τ these values are approximately 2.14667, 0.52667, and 0.23333. Heads retain more solvent neighbours, while tails, especially terminal tails, have fewer. These counts support the visual picture of tail-rich regions with heads facing the surrounding environment. The solvent here consists of simple beads, and the measurement is a geometric neighbour count. A directional hydrogen-bond analysis for molecular water would additionally specify donor and acceptor identities and their angular geometry.

Bead sizes also influence these comparisons. A common radius keeps the geometric measurement range fixed, but the number of solvent beads that can approach a particular type depends on its exclusion range and the arrangement of surrounding particles. The three curves therefore describe how solvent access changes within this particular model. To separate size effects from interaction preferences, one could compare models with equal sizes and different attraction strengths, or examine type-specific radial distributions and select corresponding contact shells. Retaining the measurement definition alongside the parameters gives such comparisons a stable reference and makes their interpretation more precise.

The complete program reads both the thermodynamic records and the trajectory. It checks the identities, molecular composition, fixed box, and zero z coordinates of all 203 frames, then calculates three cluster thresholds, two size distributions, and solvent-neighbour counts. CSV files support further plotting, JSON files retain definitions and summaries, and the four coordinate panels use the same saved frames. After reproducing the default analysis, changing a threshold or displayed time provides a focused exercise. With the underlying trajectory fixed, each new result can be traced to a specific change in what the analysis measures.

### Complete cluster, size-distribution, and solvent-contact analysis

```
"""Analyze the official two-dimensional micelle model.

python analyze_micelle.py --run . --out figures --language en
Requires NumPy, SciPy, and Matplotlib.
All distances and times remain in the model's LJ reduced units.
"""
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.spatial import cKDTree
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


def frames(path):
    with path.open() as stream:
        while line := stream.readline():
            if line.strip() != 'ITEM: TIMESTEP':
                raise ValueError('Expected a timestep header.')
            step = int(stream.readline())
            if stream.readline().strip() != 'ITEM: NUMBER OF ATOMS':
                raise ValueError('Expected an atom-count header.')
            count = int(stream.readline())
            if stream.readline().split() != ['ITEM:', 'BOX', 'BOUNDS', 'pp', 'pp', 'pp']:
                raise ValueError('Expected an orthogonal periodic cell.')
            box = np.array([list(map(float, stream.readline().split())) for _ in range(3)])
            names = stream.readline().split()[2:]
            values = np.array([list(map(float, stream.readline().split())) for _ in range(count)])
            if values.shape != (count, len(names)) or not np.isfinite(values).all():
                raise ValueError('Incomplete or non-finite atom records.')
            order = np.argsort(values[:, names.index('id')]); values = values[order]
            yield step, box, {name: values[:, i] for i, name in enumerate(names)}


def components(xy, mol, cutoff, lengths):
    ids = np.unique(mol); parent = {int(m): int(m) for m in ids}
    def find(m):
        while parent[m] != m:
            parent[m] = parent[parent[m]]; m = parent[m]
        return m
    for i, j in sorted(cKDTree(xy, boxsize=lengths).query_pairs(cutoff)):
        a, b = find(int(mol[i])), find(int(mol[j]))
        if a != b:
            parent[max(a, b)] = min(a, b)
    groups = {}
    for m in ids:
        groups.setdefault(find(int(m)), []).append(int(m))
    return sorted(groups.values(), key=lambda g: (-len(g), g[0]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', type=Path, default=Path('.'))
    parser.add_argument('--out', type=Path, default=Path('figures'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    tr = lambda zh, en: zh if args.language == 'zh' else en
    names = {f.name for f in font_manager.fontManager.ttflist}
    fonts = [f for f in ['Microsoft YaHei', 'Source Han Sans SC', 'Noto Sans CJK SC',
                         'WenQuanYi Zen Hei', 'DejaVu Sans'] if f in names]
    plt.rcParams.update({'font.family': fonts if args.language == 'zh' else ['DejaVu Sans'],
        'font.size': 12, 'svg.fonttype': 'path', 'axes.spines.top': False,
        'axes.spines.right': False, 'figure.facecolor': '#f8f7f2', 'axes.facecolor': '#f8f7f2'})
    records = []; snapshots = {}; identities = None; maximum_z = 0.; final_groups = None
    thresholds = [.9, 1.2, 1.5]
    for step, box, data in frames(args.run / 'micelle.lammpstrj'):
        ids = data['id'].astype(int); typ = data['type'].astype(int); mol = data['mol'].astype(int)
        identity = np.column_stack([ids, typ, mol])
        if identities is None:
            identities = identity.copy(); initial_box = box.copy()
        if not np.array_equal(identity, identities) or not np.array_equal(box, initial_box):
            raise ValueError('Particle identity or the fixed cell changed.')
        if dict(zip(*np.unique(typ, return_counts=True))) != {1: 750, 2: 150, 3: 150, 4: 150}:
            raise ValueError('Expected 750 solvent beads and 150 three-bead amphiphiles.')
        for m in np.unique(mol[typ == 2]):
            if sorted(typ[mol == m].tolist()) != [2, 3, 4]:
                raise ValueError('Each amphiphile must contain types 2, 3, and 4.')
        xy = np.column_stack([data['x'], data['y']]) - box[:2, 0]
        lengths = box[:2, 1] - box[:2, 0]; xy %= lengths
        maximum_z = max(maximum_z, float(abs(data['z']).max()))
        tail = typ >= 3; row = [step, step * .005]
        for cutoff in thresholds:
            groups = components(xy[tail], mol[tail], cutoff, lengths)
            sizes = np.array([len(g) for g in groups])
            if sizes.sum() != 150:
                raise ValueError('Cluster membership must conserve all 150 amphiphiles.')
            row.extend([len(groups), int(sizes.max()), int((sizes == 1).sum()),
                        float(np.sum(sizes * sizes) / 150)])
            if cutoff == 1.2:
                final_groups = groups
        # Contacts count solvent beads using one common geometrical radius.
        distance = xy[typ == 1, None, :] - xy[None, typ >= 2, :]
        distance -= lengths * np.rint(distance / lengths)
        close = (np.sum(distance * distance, axis=2) <= 1.5 ** 2).sum(axis=0)
        amph_type = typ[typ >= 2]
        row.extend([float(close[amph_type == t].mean()) for t in [2, 3, 4]])
        records.append(row)
        if step in [0, 1000, 20000, 101000]:
            snapshots[str(step)] = {'time_tau': step * .005, 'xy': xy.tolist(),
                                    'types': typ.tolist(), 'mol': mol.tolist(),
                                    'lengths': lengths.tolist()}
    a = np.asarray(records); thermo = np.loadtxt(args.run / 'micelle-thermo.dat')
    if len(a) != 203 or not np.allclose(a[:, 0], np.arange(0, 101001, 500)) or maximum_z > 1e-10:
        raise ValueError('Expected 203 planar frames spanning 0 to 505 tau.')
    if thermo.shape[1] != 6 or not np.isfinite(thermo).all():
        raise ValueError('Expected six finite thermodynamic columns.')
    kinetic_error = float(abs(thermo[:, 4] - 1199 * thermo[:, 2]).max())
    total_error = float(abs(thermo[:, 3] + thermo[:, 4] - thermo[:, 5]).max())
    if kinetic_error > 1e-8 or total_error > 1e-8:
        raise ValueError('Whole-system energy normalization or 2D temperature is inconsistent.')
    sizes = np.array([len(g) for g in final_groups]); n = np.arange(1, 151)
    multiplicity = np.bincount(sizes, minlength=151)[1:]
    number_fraction = multiplicity / len(sizes); molecule_fraction = n * multiplicity / 150
    summary = {'frames': len(a), 'time_tau': [float(a[0, 1]), float(a[-1, 1])],
        'particle_types': {'solvent': 750, 'heads': 150, 'middle_tails': 150, 'end_tails': 150},
        'molecules': 150, 'dimensions': 2, 'cell_lengths_sigma': lengths.tolist(),
        'bead_areal_density': float(1200 / np.prod(lengths)),
        'amphiphile_areal_density': float(150 / np.prod(lengths)),
        'maximum_abs_z': maximum_z, 'mean_temperature_reduced': float(thermo[:, 2].mean()),
        'kinetic_identity_max_error': kinetic_error, 'energy_sum_max_error': total_error,
        'thresholds_sigma': thresholds,
        'initial_clusters': [int(a[0, 2 + 4*i]) for i in range(3)],
        'initial_largest': [int(a[0, 3 + 4*i]) for i in range(3)],
        'final_clusters': [int(a[-1, 2 + 4*i]) for i in range(3)],
        'final_largest': [int(a[-1, 3 + 4*i]) for i in range(3)],
        'final_singletons': [int(a[-1, 4 + 4*i]) for i in range(3)],
        'final_molecule_weighted_size': [float(a[-1, 5 + 4*i]) for i in range(3)],
        'final_sizes_at_1p2': sizes.tolist(),
        'final_number_mean_at_1p2': float(sizes.mean()),
        'final_molecule_mean_at_1p2': float(np.sum(sizes * sizes) / 150),
        'mean_solvent_contacts_at_1p5': a[:, -3:].mean(axis=0).tolist(),
        'final_solvent_contacts_at_1p5': a[-1, -3:].tolist(),
        'definition': 'Graph nodes are whole amphiphiles. An edge joins two different molecules '
                      'if any pair of their tail beads is within the stated periodic xy cutoff. '
                      'Connected components include isolated molecules. Time zero follows the soft '
                      'preparation; the original LJ interval ends at 5 tau and the extension ends at '
                      '505 tau. Contact counts measure solvent-bead proximity, not hydrogen bonds.'}
    (args.out / 'micelle_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    (args.out / 'micelle_snapshots.json').write_text(json.dumps(snapshots, separators=(',', ':')), encoding='utf-8')
    header = 'step,time_tau,' + ','.join(f'{v}_r{r}' for r in thresholds for v in
        ['clusters', 'largest', 'singletons', 'molecule_weighted_size']) + ',solvent_contacts_head,solvent_contacts_middle_tail,solvent_contacts_end_tail'
    np.savetxt(args.out / 'micelle_clusters.csv', a, delimiter=',', comments='', header=header)
    np.savetxt(args.out / 'micelle_size_distribution.csv', np.column_stack([n, multiplicity,
               number_fraction, molecule_fraction]), delimiter=',', comments='',
               header='size,multiplicity,cluster_number_fraction,molecule_fraction')

    def save(fig, name):
        fig.savefig(args.out / (name + '.svg'), bbox_inches='tight')
        fig.savefig(args.out / (name + '.png'), dpi=160, bbox_inches='tight'); plt.close(fig)
    colors = ['#976c25', '#176d83', '#b44e3f']
    fig, ax = plt.subplots(2, 1, figsize=(11.5, 6), sharex=True, layout='constrained')
    ax[0].plot(thermo[:, 1], thermo[:, 2], color=colors[1], lw=.8, label=tr('保存的温度', 'Recorded temperature'))
    ax[0].axhline(.45, color=colors[2], ls='--', label=tr('目标 0.45', 'Target 0.45'))
    ax[0].set_ylabel('T*')
    ax[1].plot(thermo[:, 1], thermo[:, 3] / 1200, color=colors[1], label='U/N')
    ax[1].plot(thermo[:, 1], thermo[:, 4] / 1200, color=colors[0], label='K/N')
    ax[1].set(xlabel=tr('LJ 阶段时间 / τ', 'Time in the LJ stage / τ'), ylabel=tr('能量 / (Nε)', 'Energy / (Nε)'))
    for axis in ax:
        axis.legend(loc='lower left', bbox_to_anchor=(0, 1.01), ncol=2, frameon=False)
        axis.grid(alpha=.15, axis='y')
    save(fig, 'micelle-thermo')

    fig, ax = plt.subplots(2, 1, figsize=(11.5, 6.5), sharex=True, layout='constrained')
    for i, cutoff in enumerate(thresholds):
        for j in range(2):
            ax[j].step(a[:, 1], a[:, 2 + 4*i + j], where='post', color=colors[i], lw=1.5,
                       label=f'r = {cutoff:.1f} σ')
    ax[0].set_ylabel(tr('连通团簇数（含单分子）', 'Clusters\n(including single molecules)'))
    ax[1].set(xlabel=tr('LJ 阶段时间 / τ', 'Time in the LJ stage / τ'),
              ylabel=tr('最大团簇的分子数', 'Largest cluster\n(molecules)'))
    for axis in ax:
        axis.legend(loc='lower left', bbox_to_anchor=(0, 1.01), ncol=3, frameon=False)
        axis.grid(alpha=.15, axis='y')
    save(fig, 'micelle-clusters')

    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.4), layout='constrained')
    occupied = multiplicity > 0
    ax[0].bar(n[occupied]-.2, number_fraction[occupied], width=.4, color=colors[1],
               label=tr('按团簇等权', 'Equal weight per cluster'))
    ax[0].bar(n[occupied]+.2, molecule_fraction[occupied], width=.4, color=colors[0],
               label=tr('按分子等权', 'Equal weight per molecule'))
    ax[0].set(xlabel=tr('团簇中的分子数 n', 'Molecules per cluster n'), ylabel=tr('比例', 'Fraction'))
    ax[0].legend(loc='lower left', bbox_to_anchor=(0, 1.01), fontsize=10, frameon=False)
    for i, label in enumerate([tr('头', 'Head'), tr('中间尾珠', 'Middle tail'), tr('末端尾珠', 'End tail')]):
        ax[1].plot(a[:, 1], a[:, -3+i], color=colors[i], label=label, lw=1)
    ax[1].set(xlabel=tr('LJ 阶段时间 / τ', 'Time in the LJ stage / τ'),
               ylabel=tr('每珠平均溶剂近邻数（1.5σ）', 'Solvent neighbours / bead\n(within 1.5σ)'))
    ax[1].legend(loc='lower left', bbox_to_anchor=(0, 1.01), ncol=3, fontsize=9, frameon=False)
    save(fig, 'micelle-size-environment')

    fig, ax = plt.subplots(1, 4, figsize=(14, 4.1), layout='constrained')
    for axis, snap in zip(ax, snapshots.values()):
        xy = np.array(snap['xy']); types = np.array(snap['types']); mol = np.array(snap['mol'])
        for t, color, size, label in [(1,'#b7c4bf',4,tr('溶剂','Solvent')),(2,'#176d83',14,tr('头','Head')),
                                      (3,'#b28a35',10,tr('中间尾珠','Middle tail')),(4,'#b44e3f',7,tr('末端尾珠','End tail'))]:
            axis.scatter(xy[types == t,0],xy[types == t,1],s=size,color=color,label=label,linewidths=0)
        axis.set(xlim=(0,lengths[0]),ylim=(0,lengths[1]),xlabel='x / σ',title=f"t = {snap['time_tau']:g} τ")
        axis.set_aspect('equal')
    ax[0].set_ylabel('y / σ')
    handles, labels = ax[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='outside lower center',ncol=4,frameon=False,markerscale=2)
    save(fig, 'micelle-snapshots')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
```

Run python analyze_micelle.py --run . --out figures --language en. The required inputs are micelle-thermo.dat and micelle.lammpstrj.

## Using self-assembly simulations for materials questions

The most direct result of this example is a view of how head-and-tail preferences combine with molecular connectivity to promote segregation in a plane. Tail-rich regions have fewer solvent contacts, heads remain more exposed to their surroundings, and numerous small components develop into fewer, larger components. Thermal motion continually changes contacts, so component counts and the largest component fluctuate during this process. This trajectory supports questions about structural development, geometric contact, and membership rearrangement. Quantitative diffusion coefficients or assembly rates for a material would additionally require a physical time mapping and a temperature-control protocol appropriate for dynamical measurements.

A critical micelle concentration is another familiar research target, and it requires information along a concentration axis. One fixed-composition box describes aggregation under that condition. To investigate a concentration-dependent transition, construct several compositions and compare free-molecule fractions, aggregate-size distributions, and their stability over time, using independent starting arrangements. The present two-dimensional model uses areal concentration; a three-dimensional solution usually uses volume or molar concentration. Connecting those descriptions requires an explicit mapping of the model and its spatial dimension. With those choices established, a change across the concentration series can be interpreted in terms of the intended material.

Molecular shape offers another useful direction. Adding tail segments, changing head size, introducing a second tail, or increasing bending stiffness changes how a molecule occupies space inside an aggregate. A controlled comparison keeps common energy and length scales, specifies the changed bonds, pair parameters, and composition, and checks for close contacts in the new initial arrangement. The present three-bead molecule has no explicit angle potential. Adding one to represent stiffness requires an equilibrium angle, its strength, and the ordered triplet to which it applies. The resulting trajectories can then reveal how local restrictions on molecular shape influence larger-scale organization.

Box size becomes relevant when an aggregate approaches the dimensions of its periodic environment. A larger box can accommodate more molecules and more separate aggregates, while also increasing the sampling and computational work. One practical comparison holds areal concentration and molecular parameters fixed, increases the area and particle numbers proportionally, and examines whether aggregate distributions and local solvent contacts retain similar features. Independent starting arrangements help compare aggregation pathways. Observation time should likewise follow the chosen question: temperature control, slowly changing potential energy, and a stable size distribution describe different levels of behaviour and require their respective records.

This workflow turns an assembly animation into an interpretable structural analysis. The data file defines 150 three-bead molecules; the interactions specify their environmental preferences; the trajectory supplies changing coordinates; a contact graph converts proximity into connected components; and two weighted distributions describe aggregates and molecules from different perspectives. A useful starting exercise is to reproduce the final 12 components, compare the 0.9σ and 1.5σ criteria, and then choose one parameter comparison tied to a materials question. Preserving molecular identity, dimension, units, and statistical definitions throughout each extension makes the resulting structural interpretation both understandable and reproducible.

## Further Reading and Open Materials

- [LAMMPS examples/micelle, 30Sep2026 update1](https://download.lammps.org/tars/lammps-30Sep2026_update1.tar.gz) · LAMMPS developers · GPL-2.0-or-later

  The planar amphiphile model, original coordinates, interactions, and preparation.

  Add extensive numerical outputs and trajectories, extend the original 1000-step main interval by 100000 steps, and provide new analysis and explanatory figures.
- [Colloidal electrolytes: Soap solutions and their constitution](https://doi.org/10.1021/ja01448a010) · James W. McBain and C. S. Salmon, 1920 · Historical research article; cited

  Historical discussion of charged aggregates in soap solutions.

  Draw a new schematic linking measurements to structural hypotheses.
- [Colloids and Colloidal Electrolytes](https://www.nature.com/articles/107046a0) · J. W. McBain, 1921 · Historical research article; cited

  The scale relationship between molecules and colloidal assemblies.

  Connect the historical question to the descriptive scale of a modern coarse-grained model.
- [LAMMPS lj/cut pair style](https://docs.lammps.org/pair_lj.html) · LAMMPS developers · Official documentation; cited

  LJ potential, pair-specific parameters, and absolute cutoffs.

  Compare the minima and retained force ranges of the actual head–tail parameters.
- [LAMMPS two-dimensional simulations](https://docs.lammps.org/Howto_2d.html) · LAMMPS developers · Official documentation; cited

  Planar motion, cell definition, and enforce2d.

  Check kinetic-energy records against the actual planar degrees of freedom.
- [LAMMPS temp/rescale](https://docs.lammps.org/fix_temp_rescale.html) · LAMMPS developers · Official documentation; cited

  Temperature window, rescaling interval, and the separate integrator.

  Explain the actual settings of 100 steps, a 0.02 window, and fraction 1.0.
- [LAMMPS harmonic bonds and special_bonds](https://docs.lammps.org/bond_harmonic.html) · LAMMPS developers · Official documentation; cited

  The harmonic coefficient convention and the distinction between nonbonded exclusions and bond potentials.

  Explain with a three-bead molecule and a 0.1σ bond extension.
