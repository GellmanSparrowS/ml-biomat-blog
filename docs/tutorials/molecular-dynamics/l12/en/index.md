# Why Molecules Remain at a Surface

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l12/en/
Language: en

Exchange water with a reservoir and read population, spatial distribution, and sampling in a molecular crack.

## From a drying agent to molecular positions

A small packet of drying agent protects many moisture-sensitive products. Its function is connected to the tiny spaces within the material. Water molecules can enter pores and interact with their walls and with other waters, producing a distribution different from that in the surrounding environment. For porous glass, coatings, and separation materials, knowing how much water is present is only part of the question. Whether it stays near a wall or accumulates toward a pore centre, and how pore dimensions and surface chemistry affect that organization, can determine how the material behaves when exposed to moisture.

Adsorption means enrichment near an interface. Absorption emphasizes entry into the interior of a bulk material. Porous solids connect these familiar pictures: their pores lie inside a particle, yet the pore walls are interfaces between solid and fluid. Dividing a solid into smaller pieces can increase exposed area while leaving its total volume similar. At nanometre pore sizes, a substantial fraction of fluid molecules may lie close to a wall. A small macroscopic particle can therefore contain an extensive and varied interfacial environment.

This lesson studies a cracked silica unit containing 720 fixed substrate atoms. Water moves in its available space and exchanges with a virtual reservoir whose state is specified. The initial configuration contains three waters; the actual final record contains 64. We will follow this changing population, connect accepted insertions and deletions to the total count, and calculate how water is distributed across the crack. The aim is to read an adsorption animation as a defined molecular model with explicit exchange rules and measurable results.

The calculation combines molecular dynamics with grand canonical Monte Carlo. Molecular dynamics moves existing molecules under their forces. Monte Carlo proposes adding or removing a complete water molecule and accepts or rejects the proposal according to statistical rules. The population is therefore variable. Imagine a small room communicating with a much larger environment: the question is how many molecules occupy the room and where they tend to be. Temperature and chemical potential specify the environment, allowing it to influence the room without explicitly simulating every molecule outside.

The virtual reservoir is a thermodynamic boundary condition. Here it is specified by 300 K and an ideal-reservoir pressure of 100 bar, while the simulated cell volume stays fixed. Real-water nonideality, atmospheric relative humidity, and detailed surface chemistry can be incorporated through the models appropriate to those questions. The present example establishes a concrete starting point: a small, initially sparsely hydrated pore develops a distribution governed jointly by geometry, molecular interactions, and particle-exchange rules.

### Actual waters in the crack

Actual saved frames with varying populations from whole-water exchange. The substrate is fixed and MD alternates with GCMC.

A fixed 720-atom silica substrate in a fully periodic cell, at 300 K with a 100 bar ideal-gas reservoir; TIP4P/2005 water retains the original tutorial’s 0.008 eV oxygen LJ parameter. Hybrid GCMC/MD accumulates 25 ps with a 1 fs timestep.

[Download reference data and complete inputs (ZIP) 1.45 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-adsorption-reference-data.zip)

## Why a surface deserves its own description

A solid is often introduced through bulk properties, yet changing its exposed area or surface state can change how it takes up gases. In 1918, Langmuir examined adsorption on plane surfaces of glass, mica, and platinum and developed a molecular description based on occupation of surface positions. His 1932 Nobel lecture also introduced adsorption through examples such as gas uptake by finely divided charcoal. The important conceptual step is that an interface has its own population and arrangement of molecules, which deserve to be described separately from the bulk.

Start with a surface that is easy to draw. Suppose it contains equivalent sites, each accommodating at most one molecule, with no additional interaction between occupied sites. Empty sites can receive molecules and occupied sites can lose them. Increasing pressure increases the supply tendency from the environment. As sites fill, the additional occupation produced by further pressure increases becomes smaller. This picture separates capacity from affinity. Capacity concerns the available number of sites; affinity concerns the conditions under which those sites tend to be occupied.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l12/en/#en-s2)

Figure 1 · The Langmuir site picture relates occupation to the balance of arrival and departure. The curve illustrates equivalent independent sites.

An actual crack contains more structure than this site picture. Its walls are irregular, so different positions offer different local environments. Waters interact with one another, and space near the pore centre can also contain fluid. An atomistic model represents these positions and interactions explicitly and samples their resulting distribution. The descriptions complement one another: an ideal-site model explains how finite occupation can shape a curve, while atomistic simulation explores how particular geometry and molecular forces modify that behaviour.

Call the occupied fraction θ, making the empty fraction 1−θ. Suppose arrival at an empty site is proportional to pressure P and to the empty fraction, while departure is proportional to the occupied fraction. At a stationary mean occupation, the two tendencies balance. Writing their coefficient ratio as K and rearranging gives the Langmuir relation below. This reasoning does not require one molecule to remain permanently attached. Individual molecules can exchange while the average occupation stays unchanged, linking microscopic motion with macroscopic adsorption equilibrium.

Mean occupation of equivalent single-layer sitesEq. 5

![Mean occupation of equivalent single-layer sites](https://ml-biomat.com/static/agent-math/60d220a6a60587f40681fe4d.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| θ | Fraction of occupied sites, from 0 to 1 | dimensionless |
| K | Affinity parameter at fixed temperature | bar⁻¹ |
| P | Reservoir pressure | bar |
| 1 | Normalization representing all sites | dimensionless |
| =、+、−、×、/ | Equality, addition, subtraction, multiplication, and division; a fraction bar also denotes division. | operators |

Reading the relationshipArrival is proportional to P(1−θ) and departure to θ. Balancing gives θ = KP(1−θ); collecting terms and dividing by 1+KP yields the expression.

A worked exampleWith K = 0.1 bar⁻¹ and P = 10 bar, KP = 1 and θ = 1/2. At 100 bar, θ = 10/11 ≈ 0.9091.

ConditionsFor equivalent independent sites with at most one molecule per site. This is the analytical teaching interaction; the crack results come from atomistic trajectories.

The interaction below displays that equivalent-site, single-layer model. Changing K changes the affinity parameter at the temperature being considered; changing P changes the reservoir condition. A point on the curve and a site-occupation illustration update together. The display belongs to this analytical model. The actual crack simulation appears later in the trajectory and density figures. First keep K fixed and find the pressure giving half occupation, then hold pressure fixed and vary K. Both can increase occupation, but they describe different physical comparisons.

Analytical equivalent independent-site model. Adjust pressure and affinity to observe mean occupation. Each site fill represents the mean fraction, rather than one random molecular snapshot.

A material comparison also needs consistent normalization. The same number of waters spread over a larger surface area or pore volume has a different meaning. Experiments commonly report adsorption per mass of material and may also use area or pore volume. Simulation starts from molecular counts and converts them using specified masses and geometries. Choosing this denominator precedes interpreting fitted parameters: a capacity expressed per gram, per square metre, or per unit cell answers a different quantitative question, even when the plotted curves have similar shapes.

## How an open system exchanges molecules

In a fixed-population water box, a thermostat exchanges energy but does not add or remove waters. Adsorption introduces another freedom: the simulated region can exchange molecules with its environment. The grand canonical ensemble is commonly written μVT, indicating specified chemical potential, volume, and temperature, with population allowed to vary. An ensemble can be understood as a collection of microscopic states compatible with those conditions. Sampling aims to visit them with the appropriate weights, rather than simply locate the lowest-potential-energy arrangement.

Chemical potential can first be understood as the free-energy scale associated with transferring one molecule from a large environment. It carries the environment's supply tendency into the small system and includes both energy and the number of available states. For an ideal reservoir at fixed temperature, increasing pressure increases chemical potential logarithmically. The logarithm converts multiplicative pressure changes into additive changes. Raising pressure from 1 to 10 bar and from 10 to 100 bar both multiply it by ten and therefore produce the same ideal chemical-potential increment.

How pressure changes chemical potentialEq. 2

![How pressure changes chemical potential](https://ml-biomat.com/static/agent-math/a13d063b19a27a0fb6670903.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| μ(P₁)、μ(P₂) | Ideal-reservoir chemical potentials per molecule at two pressures | eV |
| P₁、P₂ | Two positive pressures expressed in the same unit | bar |
| kB | Boltzmann constant, 8.617333262×10⁻⁵ eV/K | eV/K |
| T | Fixed absolute temperature | K |
| ln | Natural logarithm of a dimensionless pressure ratio | operator |
| 1、2、B | Labels of compared states and the Boltzmann constant | labels |
| =、+、−、×、/ | Equality, addition, subtraction, multiplication, and division; a fraction bar also denotes division. | operators |

Reading the relationshipAt fixed temperature in an ideal reservoir, pressure is proportional to number density. Its multiplicative change becomes an additive chemical-potential change through the logarithm.

A worked exampleAt 300 K, kBT ≈ 0.025852 eV. From 1 to 100 bar, the increment is 0.11905 eV per molecule, approximately 11.49 kJ/mol.

ConditionsThis is an ideal-reservoir difference at fixed temperature. Nonideal reservoirs use fugacity; absolute chemical potential additionally depends on its reference convention.

The input uses `pressure 100`. LAMMPS determines the reservoir chemical potential from that pressure and temperature, so the earlier literal `-0.5` in the same command no longer acts as a directly imposed chemical potential. This input uses `units metal`: time is in ps, length in Å, energy in eV, and pressure in bar. Reading 100 as atmospheres, or 0.001 ps as 0.001 fs, changes the physical interpretation. Establish the unit convention first, then assign meaning to every numerical parameter that follows.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l12/en/#en-s3)

Figure 2 · Reservoir conditions influence the statistical weights for adding and removing molecules. MD progression and GCMC exchange have distinct roles.

An insertion proposal selects a position and orientation for a complete water and evaluates the change in interaction energy. Acceptance also accounts for reservoir supply and the relative number of available states. Accepting every energy decrease and rejecting every energy increase is therefore not the full open-system rule. Some energetically uphill changes belong in finite-temperature sampling. Insertion and deletion obey the corresponding statistical balance so that several populations can be explored. Random numbers decide individual outcomes, while the model specifies the statistical organization of many trials.

Every 100 MD steps of 1 fs, this calculation performs an average of 100 exchange attempts. Insertions and deletions are chosen with equal probability, producing slightly different totals in the actual record. A separate parameter sets ordinary Monte Carlo translation or rotation attempts to zero. Existing molecules instead move mainly through MD between exchange batches. A newly inserted molecule still receives a randomly selected orientation; this is distinct from attempting to rotate a molecule already present. Distinguishing the operations makes the sequence of numerical arguments readable.

The hybrid time axis must be interpreted accordingly. The plotted 25 ps is accumulated MD time, with Monte Carlo exchanges interspersed. A newly accepted water can appear directly inside the pore without tracing a path from outside the material. The population curve therefore describes filling and sampling under this algorithm. Physical uptake rates, diffusion, and molecular residence require a dynamical stage that preserves continuous molecular histories and has boundaries suited to the intended entry, exit, and transport process.

## Defining the crack and its interactions with water

The substrate contains 240 silicon and 480 oxygen atoms, giving the composition of silica. Cell edges are approximately 4.494, 1.716, and 1.698 nm, with periodic boundaries in all three directions. An irregular low-solid-density region forms the crack, and the surrounding structure repeats in neighbouring cells. Water therefore encounters a defined periodic pore geometry. Questions about a distribution of pore widths, transport across a whole particle, or distinct fracture surfaces require models containing those respective geometrical features and length scales.

During adsorption, water receives a time-integration fix while substrate positions remain fixed. Substrate Si and O have zero assigned charge here. Their interactions with water oxygen are specified by Lennard–Jones parameters that provide short-range exclusion and attraction. This makes pore shape and surface attraction clear control variables. The retained mechanisms are water translation, rotation, and intermolecular interaction in a fixed environment. Substrate vibration, crack extension, and surface hydroxylation call for additional motion or chemistry in the model when those processes become the research target.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l12/en/#en-s4)

Figure 3 · The TIP4P negative site is constructed geometrically. Substrate Si/O remain fixed and neutral; specified Lennard–Jones terms couple water to the solid.

Water uses TIP4P/2005 geometry and charge placement. The O–H distance is 0.9572 Å and the H–O–H angle is 104.52°. A coordinate file contains one oxygen and two hydrogens per water. Its negative electrostatic site is a virtual M point, displaced 0.1546 Å from oxygen toward the region between the hydrogens. Each hydrogen carries +0.5564 elementary charges and M carries −1.1128, giving a neutral molecule. The TIP4P interaction routine constructs this virtual location, reconciling three stored atomic positions with four interaction sites.

Water-oxygen Lennard–Jones parameters are ε=0.008 eV and σ=3.1589 Å, retaining the rounded ε in this example. Si–water-oxygen parameters are 0.0057 eV and 4.42 Å; substrate-O–water-oxygen parameters are 0.0043 eV and 3.12 Å. The σ value establishes a distance scale, while ε sets the energy scale. Identical pore coordinates with different validated surface parameters can therefore produce different fluid distributions. Long-range electrostatics uses the TIP4P-compatible PPPM method, with a 10 Å real-space cutoff.

Rigid water requires a constraint algorithm. SHAKE maintains the two covalent O–H lengths and the H–O–H angle and incorporates newly inserted molecules into the same constraint system. The template supplies an initial arrangement, while the constraint parameters specify its subsequent rigid geometry. Zero harmonic force coefficients do not turn the water into three unrelated particles: the topology defines connectivity, SHAKE enforces geometry, and charges and nonbonded terms determine interactions between molecules. Reading these responsibilities separately is more informative than interpreting one coefficient in isolation.

Changing population also affects temperature evaluation. Temperature follows from the kinetic energy associated with active degrees of freedom, and adding or removing waters changes that count. The setting `dynamic/dof yes` updates the water-temperature normalization as population changes, while constraints determine which internal motions are removed. The thermostat acts on the water group at 300 K. Frozen substrate atoms are consequently kept out of that fluid-temperature average. The insertion velocity adjustment factor 5/3 is retained to tune initialization of newly inserted molecules; the target temperature remains 300 K.

## Running an exchange process that can be checked

The complete run uses the substrate coordinates `cracking-mod.data`, water template `H2O.mol`, main input `gcmc.lmp`, and `run.sh` in one directory. The substrate file contains atom types, masses, coordinates, and storage reserved for molecular bonds and angles. The water template defines the atoms, charges, and connectivity of one exchanged molecule. The first program below verifies substrate composition, charges, and cell dimensions before sampling begins, establishing precisely which physical object the subsequent calculation will use.

### Check the fixed substrate

```
"""Check the prepared neutral silica geometry before adding water.

python check_surface.py
"""
from pathlib import Path
import re
import json
import numpy as np

lines = Path('cracking-mod.data').read_text().splitlines()
declared = next(int(s.split()[0]) for s in lines if re.fullmatch(r'\s*\d+ atoms\s*', s))
start = next(i for i, s in enumerate(lines) if s.strip().startswith('Atoms #'))+1
rows = []
for s in lines[start:]:
    if not s.strip():
        continue
    if not s.split()[0].isdigit():
        break
    rows.append(list(map(float, s.split())))
a = np.array(rows)
assert len(a) == declared == 720
assert len(np.unique(a[:, 0])) == 720
assert np.count_nonzero(a[:, 2] == 1) == 240
assert np.count_nonzero(a[:, 2] == 2) == 480
assert np.all(a[:, 3] == 0)
box = np.array([list(map(float, s.split()[:2])) for s in lines
                if s.strip().endswith(('xlo xhi', 'ylo yhi', 'zlo zhi'))])
assert box.shape == (3, 2)
assert np.all((a[:, 4:7] >= box[:, 0]) & (a[:, 4:7] <= box[:, 1]))
print(json.dumps({'Si': 240, 'substrate_O': 480, 'total_charge_e': float(a[:, 3].sum()),
                  'cell_lengths_nm': ((box[:, 1]-box[:, 0])/10).tolist()}, indent=2))
```

Run python check_surface.py in the input directory to verify the actual substrate.

### Complete water molecule template

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

1        OW
2        HW
3        HW

Charges

1       -1.1128
2        0.5564
3        0.5564

Bonds

1   OW-HW      1      2
2   OW-HW      1      3

Angles

1   HW-OW-HW    2      1      3

Shake Flags

1 1
2 1
3 1

Shake Atoms

1 1 2 3
2 1 2 3
3 1 2 3

Shake Bond Types

1 OW-HW OW-HW HW-OW-HW
2 OW-HW OW-HW HW-OW-HW
3 OW-HW OW-HW HW-OW-HW

Special Bond Counts

1 2 0 0
2 1 1 0
3 1 1 0

Special Bonds

1 2 3
2 1 3
3 1 2
```

Three atoms, two bonds, one angle, and SHAKE information define an exchanged molecule.

The main input reads the substrate and places three random waters as the starting population. Substrate velocities are set to zero, and only water is integrated. Parameter commands define water–water and water–surface interactions; SHAKE and the thermostat handle rigid molecular geometry and water temperature; GCMC handles exchange of complete molecules. Reading these roles by model component is more useful than memorizing a command sequence. Changing the surface requires revisiting geometry and cross interactions. Changing the exchanged molecule requires a compatible template, constraints, and reservoir description.

The executable must also provide the corresponding capabilities. GCMC belongs to the Monte Carlo package, rigid water needs SHAKE, and long-range electrostatics needs the appropriate solver. The runner uses four OpenMP threads. Follow the environment preparation page and inspect the software version and enabled features before starting. This separates an unrecognized input command from unstable molecular motion. The first leads back to executable configuration; the second calls for checking geometry, parameters, constraints, and time step. Identifying which situation occurred gives a concrete next diagnostic action.

### Complete adsorption input

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

units metal
boundary p p p
atom_style full

pair_style lj/cut/tip4p/long OW HW OW-HW HW-OW-HW 0.1546 10
kspace_style pppm/tip4p 1.0e-5
bond_style harmonic
angle_style harmonic

read_data cracking-mod.data
molecule h2omol H2O.mol
create_atoms 0 random 3 3245 NULL mol h2omol 4585 overlap 2.0 maxtry 50

group SiO type Si O
group H2O type OW HW
# The frozen substrate has no kinetic motion in this adsorption stage.
velocity SiO set 0.0 0.0 0.0

pair_coeff * * 0 0
pair_coeff Si OW 0.0057 4.42
pair_coeff O OW 0.0043 3.12
pair_coeff OW OW 0.008 3.1589
pair_coeff HW HW 0.0 0.0
bond_coeff OW-HW 0 0.9572
angle_coeff HW-OW-HW 0 104.52

variable oxygen atom type==label2type(atom,OW)
group oxygen dynamic all var oxygen
variable nO equal count(oxygen)

fix shak H2O shake 1.0e-5 200 0 b OW-HW a HW-OW-HW mol h2omol


compute ctH2O H2O temp
compute_modify thermo_temp dynamic/dof yes
compute_modify ctH2O dynamic/dof yes
fix mynvt H2O nvt temp 300 300 0.1
fix_modify mynvt temp ctH2O

timestep 0.001

variable tfac equal 5.0/3.0 
fix fgcmc H2O gcmc 100 100 0 0 65899 300 -0.5 0.1 &
  mol h2omol tfac_insert ${tfac} shake shak full_energy pressure 100

thermo 250
thermo_style custom step c_ctH2O etotal v_nO &
  f_fgcmc[3] f_fgcmc[4] f_fgcmc[5] f_fgcmc[6]

# Numerical records preserve the original 25 ps hybrid GCMC/MD schedule.
dump course all custom 250 adsorption.lammpstrj id mol type q x y z ix iy iz
dump_modify course sort id
variable courseTime equal time
variable courseT equal c_ctH2O
variable courseU equal pe
variable courseE equal etotal
fix courseRecord all ave/time 250 1 250 v_courseTime v_courseT v_courseU v_courseE v_nO f_fgcmc[3] f_fgcmc[4] f_fgcmc[5] f_fgcmc[6] file adsorption-thermo.dat
run 25000
write_data adsorption-final.data
write_restart adsorption-final.restart
```

A 300 K, 100 bar ideal reservoir, a 1 fs step, and 25 ps of hybrid GCMC/MD.

The keyword `full_energy` compares the complete system potential energy before and after a proposed exchange, accommodating the long-range electrostatic calculation. A new water affects more than its nearest pair contacts: it also changes electrostatic energy in the periodic system. Coordinates and numerical records are saved every 250 steps, or 0.25 ps. The 25000-step run therefore saves 101 frames including the initial state. Each trajectory frame carries its own population, atom identifiers, molecule identifiers, and types, supporting analysis of a changing molecular collection.

### Run and retain numerical records

```
#!/usr/bin/env bash
set -euo pipefail
lmp=${LAMMPS:-lmp}
export OMP_NUM_THREADS=4
"$lmp" -sf omp -pk omp 4 -in gcmc.lmp -log adsorption.log > adsorption.stdout.log 2>&1
```

Run bash run.sh in the same directory. LAMMPS requires the MC package, SHAKE, a long-range electrostatic solver, and the OPENMP suffix.

Begin by checking the number of water oxygens and the integrity of each molecular composition. One oxygen represents one water, and every water must also contain two hydrogens. Verify that the 720 substrate atoms retain their positions, then compare population with accepted exchange events. These checks directly establish what the changing collection of points means: newly appearing atoms belong to complete molecules, and population changes agree with the exchange record. They also provide an early diagnosis if a later plotted density looks unexpected.

Checking population through exchangeEq. 1

![Checking population through exchange](https://ml-biomat.com/static/agent-math/85559284361036d4692b16f4.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| N(t)、N₀ | Water populations at time t and initially | molecules |
| Ains(t)、Adel(t) | Cumulative accepted molecular insertions and deletions | events |
| t | Accumulated MD time in the hybrid schedule | ps |
| ins、del、0 | Subscripts for insertion, deletion, and initial state | labels |
| =、+、−、×、/ | Equality, addition, subtraction, multiplication, and division; a fraction bar also denotes division. | operators |

Reading the relationshipEach accepted molecular insertion adds one water and each accepted deletion removes one. Summing the events gives the population at any saved time.

A worked exampleThe final count is 3 + 77 − 16 = 64 waters, giving 720 + 3 × 64 = 912 atoms. Each exchanged water contributes three atoms.

ConditionsApplies to exchange of intact waters with an unchanged substrate.

The final record contains 77 accepted insertions from 12470 attempts and 16 accepted deletions from 12530 attempts. Starting from three waters gives 3+77−16=64, matching the final coordinates. Total atoms are then 720+3×64=912. The same balance holds at every saved time. An accepted molecular insertion adds three atoms, so atomic population changes must be converted before interpreting them as numbers of waters. This elementary bookkeeping connects the thermodynamic algorithm to the chemical identity represented in the trajectory.

The initial three waters are not assigned a separate thermal velocity distribution, giving an initial water-temperature record of 0 K. Subsequent thermostat action, exchange, and interactions bring the temperature near its target. Later-window statistics explicitly use the 50 frames satisfying 12.5<t≤25 ps. Their mean is approximately 294.898 K, with a sample standard deviation of 22.292 K. The small, changing population produces appreciable instantaneous fluctuations. Retaining both the startup trace and a clearly stated later window makes the initial condition and the meaning of the average visible.

### Population, temperature, and potential energy

101 records from 0 to 25 ps. Hollow points reconstruct population from accepted exchanges; the dashed temperature line marks 300 K.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l12/en/#en-s5)

Water population, temperature and system potential energy at 101 saved times. Population is independently reconstructed from three initial waters plus accepted insertions minus accepted deletions. The horizontal axis accumulates MD integration time; insertion and deletion represent reservoir exchanges.

## Using acceptance statistics to read a population curve

As the pore fills, the population curve develops extended flat stretches. Such stretches can have different origins. Frequent insertions and deletions may cancel, or both types of exchange may be difficult to accept. These situations imply different sampling activity, so attempted and accepted counts should accompany the population. It resembles observing a car park: the number of parked cars alone does not reveal whether vehicles are continually exchanging or almost nobody is moving through the entrance. Exchange records supply the missing information.

Separate insertion and deletion acceptanceEq. 3

![Separate insertion and deletion acceptance](https://ml-biomat.com/static/agent-math/55109e38751896b5e68070f3.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ains、adel | Fractions of insertion and deletion attempts accepted | dimensionless |
| Ains、Adel | Accepted attempts within the selected window | events |
| Mins、Mdel | Corresponding total attempts in the same window | attempts |
| ins、del | Labels of the two exchange operations | labels |
| =、+、−、×、/ | Equality, addition, subtraction, multiplication, and division; a fraction bar also denotes division. | operators |

Reading the relationshipDivide successes for each operation by its own attempts. For blocks, subtract cumulative counts at the endpoints first.

A worked example77/12470 ≈ 0.00617482, or 0.617482%; 16/12530 ≈ 0.00127694, or 0.127694%. Multiply the fraction by 100 to express a percentage.

ConditionsAcceptance characterizes exchange proposals in a specified state and window; it is distinct from a physical molecular arrival rate.

Overall insertion acceptance is approximately 0.6175%, while deletion acceptance is approximately 0.1277%. Each divides successes by its own attempt count. In five-ps blocks, the first block accepts 56 insertions, giving about 2.300%; the last accepts three, giving about 0.1226%. As more waters occupy the available space, randomly placing an intact molecule more often encounters short-range repulsion. The energy change also depends on the organization of surrounding water, connecting geometrical crowding with the molecular interaction model.

### Exchange activity by window

Each 5 ps block is left-open and right-closed. Acceptance uses differences of cumulative counts; mean population uses 20 frames per block.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l12/en/#en-s6)

Insertion/deletion acceptance fractions and mean water populations across five successive 5 ps windows. Each left-open, right-closed window contains 20 saved frames; attempts and successes are differences of cumulative counts.

Block populations reveal the corresponding evolution. Mean water counts across the five consecutive windows are approximately 32.9, 53.4, 57.95, 60.45, and 62.55. Growth slows while a directional change remains. The final count of 64 is therefore read as the final state of this 25 ps observation. A study targeting equilibrium uptake can continue exchange sampling from both sparse and more filled initial configurations, compare later distributions and exchange activity, and use independent repeats to decide which observation windows support a stable average.

A high acceptance fraction is not a universal sampling objective. Very small, easily accepted changes may explore a narrow region, while a less frequent successful insertion can provide access to a different population. Evaluate an algorithm by how effectively it visits the relevant molecular and population states for a given computational effort. The current batches of 100 exchanges provide a readable teaching protocol. Dense fluids or more complicated molecules can motivate biased insertion, conformational sampling, and exchange strategies selected for their particular state space.

Temperature and potential energy need separate interpretations. Water temperature measures kinetic motion and fluctuates around the thermostat target. Total potential energy becomes more negative as additional interactions appear and molecules rearrange. Because population changes, the energy trend also includes the presence of more interacting molecules. Converting its slope directly into a physical heat-release rate would conflate that population change with an energy-transfer measurement. Adsorption energies or heats require specified reference states, exchange-energy definitions, and the equilibrium statistics appropriate to those quantities.

Temporal correlation remains relevant throughout. Saving every 0.25 ps reveals the evolution but does not create 101 independent experiments. Block statistics describe sensitivity to the selected time window. Different random seeds and initial configurations add a separate comparison between realizations. These observations guide further sampling: scarce exchange suggests a state-access issue, changing density profiles suggest continuing structural adjustment, and distinct later distributions from different starts reveal initial-state dependence that deserves additional exploration.

## Turning molecular counts into spatial distributions

Total population says how much water is present; a density profile asks where it is. Divide the cell into 60 slices along x, count water oxygens in each slice in every frame, and average over the chosen window. One oxygen per water provides a definite representative position. Dividing the mean count by slice volume gives number density in molecules per cubic nanometre. Slice width, cross-sectional area, and averaging window all belong to this definition, so changing any of them changes how the observable should be read.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l12/en/#en-s7)

Figure 4 · Density uses complete geometrical slice volume. Accessible pore volume is a separate probe- and geometry-dependent quantity; these slices retain a fixed denominator.

From slice counts to number densityEq. 4

![From slice counts to number density](https://ml-biomat.com/static/agent-math/832ed25783cf5882a6aa84c6.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ρj | Time-averaged water number density in slice j | nm⁻³ |
| Nj,k | Water-oxygen count in slice j of frame k | count |
| M、k、j | Number of frames, frame index, and slice index | dimensionless |
| Vj | Full geometrical slice volume | nm³ |
| Ly、Lz、Δx | Cell y and z lengths and x slice width | nm |
| ∑、Δ | Sum over frame counts; interval width | operators |
| =、+、−、×、/ | Equality, addition, subtraction, multiplication, and division; a fraction bar also denotes division. | operators |

Reading the relationshipAverage each slice count with equal frame weights, then divide by its volume. Summing ρjVj recovers the mean total population.

A worked exampleFor a 2 nm² cross-section and 0.1 nm width, the volume is 0.2 nm³. Across 50 frames, 200 observations give a mean count of 4 and a density of 20 nm⁻³.

ConditionsThe cell is fixed and full slice volume is used. Accessible-pore density requires a separately defined denominator.

The cross-sectional area is the product of the fixed y and z cell lengths, and every slice uses that complete area. Its volume therefore includes any part occupied by solid. The reported density is normalized by the full geometrical slice volume. A density per accessible pore volume requires a separate definition of accessibility and probe size. Both can be useful, provided the denominator describes a known region. A substrate number-density profile shares the same x axis below the water curve, revealing dense solid regions and the crack between them.

### Spatial distributions of water and solid

60 equal slices along x; water is averaged over 50 frames with 12.5 < t ≤ 25 ps. Both profiles use full slice volumes.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l12/en/#en-s7)

Number densities in 60 equal slices along x. Water is averaged over 50 frames with 12.5 < t ≤ 25 ps; the solid is fixed. Full slice volumes normalize both profiles, whose integrals recover mean molecule or atom counts.

Across the 50 frames with 12.5<t≤25 ps, mean water population is 60.98 and its sample standard deviation is approximately 1.545. Water density concentrates in the region of low substrate density. Its asymmetric shape corresponds to the irregular molecular geometry. Multiplying each slice density by slice volume and summing over all 60 slices recovers 60.98. This integral links the curve's height, units, and total count and detects errors such as mixing Å with nm, counting each hydrogen as another water, or normalizing every frame by its changing population.

A complementary observable measures proximity to the solid. For every water oxygen, find the shortest periodic distance to any substrate Si or O atom. Count the water once if that distance is no greater than 3.5 Å, even if several substrate atoms are nearby. The later-window mean is approximately 16.9 waters under this rule. It describes a chosen geometrical shell; increasing the cutoff usually includes more space. It differs from the mean total population of 60.98 and does not assign each nearby water a permanent adsorption site.

The neutral substrate has no explicit surface hydroxyl groups, so this count measures geometrical proximity. Surface hydrogen-bond analysis requires the corresponding donor and acceptor chemistry and a directional criterion. Molecular residence analysis also follows identities through time and distinguishes motion out of a region from GCMC deletion. In a variable-population trajectory, the tenth row need not represent the same atom in the next frame. The program reads identifiers, molecule numbers, and types afresh in every frame rather than assuming fixed row identities.

### Three actual states of the same crack

Projections onto xz at 0, 5, and 25 ps show Si, substrate O, and water O. Water H is omitted to make molecular positions readable.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l12/en/#en-s7)

xz projections of native coordinates at 0, 5 and 25 ps, showing fixed Si, substrate O and water O. Hydrogen is omitted for positional clarity; each population comes from the actual trajectory.

Three projected snapshots show 0, 5, and 25 ps, with three, 46, and 64 waters. They connect population growth with actual locations in the crack. Water oxygens share one colour, while substrate Si and O use separate colours. Projection overlays atoms at different y coordinates, so apparently coincident points need not coincide in three dimensions. The numerical analysis retains three-dimensional coordinates and periodic distances; the projection summarizes spatial organization. Together they make the structure readable while keeping measurements physically defined.

### Complete population, exchange, and spatial analysis

```
"""Read a variable-population GCMC/MD trajectory and its exchange record.

python analyze_adsorption.py --run . --out figures --language en
Dependencies: NumPy and Matplotlib.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


def frames(path):
    with path.open(encoding='utf-8') as f:
        while line := f.readline():
            if line.strip() != 'ITEM: TIMESTEP':
                raise ValueError('Expected a timestep header.')
            step = int(f.readline())
            if f.readline().strip() != 'ITEM: NUMBER OF ATOMS':
                raise ValueError('Expected an atom-count header.')
            n = int(f.readline())
            header = f.readline().split()
            if header != ['ITEM:', 'BOX', 'BOUNDS', 'pp', 'pp', 'pp']:
                raise ValueError('This analysis expects the orthogonal periodic cell.')
            box = np.array([list(map(float, f.readline().split())) for _ in range(3)])
            names = f.readline().split()[2:]
            values = np.array([list(map(float, f.readline().split())) for _ in range(n)])
            if values.shape != (n, len(names)) or not np.isfinite(values).all():
                raise ValueError('Incomplete or non-finite atom records.')
            data = {name: values[:, i] for i, name in enumerate(names)}
            if len(np.unique(data['id'])) != n:
                raise ValueError('Atom identifiers must be unique within a frame.')
            yield step, box, data


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run', type=Path, default=Path('.'))
    ap.add_argument('--out', type=Path, default=Path('figures'))
    ap.add_argument('--language', choices=['zh', 'en'], default='en')
    args = ap.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    zh = args.language == 'zh'; tr = lambda z, e: z if zh else e
    names = {f.name for f in font_manager.fontManager.ttflist}
    fonts = [f for f in ['Microsoft YaHei', 'Source Han Sans SC', 'Noto Sans CJK SC',
                         'WenQuanYi Zen Hei', 'DejaVu Sans'] if f in names]
    plt.rcParams.update({'font.family': fonts if zh else ['DejaVu Sans'], 'font.size': 12,
        'svg.fonttype': 'path', 'axes.unicode_minus': False, 'axes.spines.top': False,
        'axes.spines.right': False, 'figure.facecolor': '#f8f7f2', 'axes.facecolor': '#f8f7f2'})
    thermo = np.loadtxt(args.run / 'adsorption-thermo.dat', comments='#')
    if thermo.ndim != 2 or thermo.shape[1] != 10 or not np.isfinite(thermo).all():
        raise ValueError('Expected ten finite thermo columns.')
    if np.any(np.diff(thermo[:, 0]) <= 0):
        raise ValueError('Thermo steps must increase.')
    initial = int(thermo[0, 5]); counts = []; reference = None; bins = None
    hist = []; nearest = []; snapshots = []; boxes = []; water_positions = []
    for step, box, d in frames(args.run / 'adsorption.lammpstrj'):
        typ = d['type'].astype(int); ids = d['id'].astype(int); mol = d['mol'].astype(int)
        xyz = np.column_stack([d[k] for k in ['x', 'y', 'z']])
        substrate = typ <= 2; ow = typ == 3; hw = typ == 4
        order = np.argsort(ids[substrate]); solid = xyz[substrate][order]
        if np.count_nonzero(substrate) != 720 or np.count_nonzero(hw) != 2*np.count_nonzero(ow):
            raise ValueError('Expected 720 substrate atoms and intact three-site water molecules.')
        if reference is None:
            reference = solid.copy(); bounds = box.copy()
            bins = np.linspace(box[0, 0], box[0, 1], 61)
        if not np.array_equal(box, bounds) or not np.array_equal(solid, reference):
            raise ValueError('The substrate and cell must remain fixed.')
        for m in np.unique(mol[ow]):
            if sorted(typ[mol == m].tolist()) != [3, 4, 4]:
                raise ValueError('Water molecule identity or composition changed.')
        water = xyz[ow]; lengths = box[:, 1]-box[:, 0]
        dx = water[:, None, :]-solid[None, :, :]
        dx -= lengths*np.rint(dx/lengths)
        distance = np.sqrt((dx*dx).sum(axis=2)).min(axis=1)
        counts.append([step, step*.001, len(water), len(ids), int(np.count_nonzero(distance <= 3.5))])
        hist.append(np.histogram(water[:, 0], bins)[0]); nearest.append(distance)
        snapshots.append((typ.copy(), xyz.copy())); boxes.append(box)
        water_positions.append(water)
    counts = np.array(counts); hist = np.array(hist)
    if not np.array_equal(counts[:, 0], thermo[:, 0]) or not np.array_equal(counts[:, 2], thermo[:, 5]):
        raise ValueError('Coordinate populations and thermo populations disagree.')
    balance = initial+thermo[:, 7]-thermo[:, 9]
    if not np.array_equal(balance, thermo[:, 5]):
        raise ValueError('Insertion/deletion mass balance failed.')
    times = counts[:, 1]; later = (times > 12.5) & (times <= 25)
    widths = np.diff(bins); area = np.prod(bounds[1:, 1]-bounds[1:, 0])
    rho = hist[later].mean(axis=0)/(area*widths)*1000  # molecules per nm^3
    centres = (bins[:-1]+bins[1:])/2
    solid_rho = np.histogram(reference[:, 0], bins)[0]/(area*widths)*1000
    blocks = []
    for lo, hi in [(0, 5), (5, 10), (10, 15), (15, 20), (20, 25)]:
        start = thermo[np.isclose(times, lo)][0]; end = thermo[np.isclose(times, hi)][0]
        delta = end[6:10]-start[6:10]; mask = (times > lo) & (times <= hi)
        blocks.append([lo, hi, thermo[mask, 5].mean(), thermo[mask, 2].mean(), *delta,
                       delta[1]/delta[0], delta[3]/delta[2]])
    blocks = np.array(blocks)
    summary = {'frames': len(times), 'time_ps': [float(times[0]), float(times[-1])],
        'fixed_substrate_atoms': 720, 'initial_water': initial, 'final_water': int(thermo[-1, 5]),
        'final_atom_count': int(counts[-1, 3]), 'reservoir_pressure_bar': 100, 'temperature_target_K': 300,
        'insertion_attempts': int(thermo[-1, 6]), 'insertion_successes': int(thermo[-1, 7]),
        'deletion_attempts': int(thermo[-1, 8]), 'deletion_successes': int(thermo[-1, 9]),
        'insertion_acceptance': float(thermo[-1, 7]/thermo[-1, 6]),
        'deletion_acceptance': float(thermo[-1, 9]/thermo[-1, 8]),
        'mass_balance_max_error': float(np.max(np.abs(balance-thermo[:, 5]))),
        'box_lengths_A': (bounds[:, 1]-bounds[:, 0]).tolist(), 'box_volume_nm3': float(np.prod(bounds[:, 1]-bounds[:, 0])/1000),
        'later_window_ps': '(12.5,25]', 'later_frames': int(later.sum()),
        'later_water_mean': float(thermo[later, 5].mean()), 'later_water_sd': float(thermo[later, 5].std(ddof=1)),
        'later_temperature_mean_K': float(thermo[later, 2].mean()),
        'later_temperature_sd_K': float(thermo[later, 2].std(ddof=1)),
        'later_near_solid_water_mean': float(counts[later, 4].mean()),
        'near_solid_definition': 'Each water oxygen within 3.5 A of any Si/O atom is counted once, using orthogonal minimum-image distances.',
        'density_integral_water_count': float(np.sum(rho/1000*widths*area)),
        'blocks_5ps': [dict(zip(['start_ps','end_ps','water_mean','temperature_mean_K','insert_attempts','insert_successes','delete_attempts','delete_successes','insert_acceptance','delete_acceptance'], row)) for row in blocks],
        'definition': 'Time follows the hybrid MD clock. GCMC insertions and deletions exchange molecules with the reservoir. Densities use the full slice volume and an average over 50 equally spaced frames; the changing water population is retained in the number density.'}
    (args.out/'adsorption_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    np.savetxt(args.out/'adsorption_counts.csv', counts, delimiter=',', comments='', header='step,time_ps,water_count,atom_count,water_within3p5A_solid')
    np.savetxt(args.out/'adsorption_blocks.csv', blocks, delimiter=',', comments='', header='start_ps,end_ps,water_mean,temperature_mean_K,insert_attempts,insert_successes,delete_attempts,delete_successes,insert_acceptance,delete_acceptance')
    np.savetxt(args.out/'adsorption_density.csv', np.column_stack([centres/10,rho,solid_rho]), delimiter=',', comments='', header='x_nm,water_number_density_nm-3,substrate_number_density_nm-3')
    def save(fig, name):
        fig.savefig(args.out/(name+'.svg'), bbox_inches='tight')
        fig.savefig(args.out/(name+'.png'), dpi=160, bbox_inches='tight'); plt.close(fig)
    teal, orange, blue = '#147d85', '#c46938', '#4876b7'
    fig, ax = plt.subplots(3,1,figsize=(10.5,9),sharex=True,layout='constrained')
    ax[0].step(times,thermo[:,5],where='mid',color=teal,label=tr('水分子数','Water molecules'))
    ax[0].plot(times,balance,'o',ms=2.5,mfc='none',color=orange,label=tr('3 + 接受插入 − 接受删除','3 + accepted insertions − accepted deletions'))
    ax[0].legend(loc='lower left',bbox_to_anchor=(0,1.02),ncol=1,fontsize=10)
    ax[0].set(ylabel=tr('分子数','Molecule count'),ylim=(0,70))
    ax[1].plot(times,thermo[:,2],color=blue);ax[1].axhline(300,color=orange,ls='--')
    ax[1].set(ylabel=tr('水温度 / K','Water temperature / K'))
    ax[2].plot(times,thermo[:,3],color=teal);ax[2].set(ylabel=tr('体系势能 / eV','System potential energy / eV'),xlabel=tr('MD累计时间 / ps','Accumulated MD time / ps'))
    save(fig,'adsorption-history')
    fig,ax=plt.subplots(2,1,figsize=(10.5,7),sharex=True,layout='constrained')
    x=np.arange(5);labels=[f'{int(a)}–{int(b)}' for a,b in blocks[:,:2]]
    ax[0].bar(x-.18,100*blocks[:,-2],.36,color=teal,label=tr('插入','Insertion'))
    ax[0].bar(x+.18,100*blocks[:,-1],.36,color=orange,label=tr('删除','Deletion'))
    ax[0].legend(loc='lower left',bbox_to_anchor=(0,1.02),ncol=2)
    ax[0].set(ylabel=tr('尝试接受比例 / %','Accepted attempts / %'))
    ax[1].bar(x,blocks[:,2],color=blue);ax[1].set(ylabel=tr('窗口平均水分子数','Mean water count in window'),xticks=x,xticklabels=labels,xlabel=tr('MD时间窗口 / ps','MD time window / ps'),ylim=(0,70))
    save(fig,'adsorption-exchanges')
    fig,ax=plt.subplots(2,1,figsize=(10.5,7.5),sharex=True,layout='constrained')
    ax[0].plot(centres/10,rho,color=teal);ax[0].fill_between(centres/10,0,rho,color=teal,alpha=.15)
    ax[0].set(ylabel=tr('水数密度 / nm⁻³','Water number density / nm⁻³'),title=tr('12.5 < t ≤ 25 ps；按完整切片体积归一化','12.5 < t ≤ 25 ps; normalized by full slice volume'))
    ax[1].plot(centres/10,solid_rho,color=orange);ax[1].set(ylabel=tr('固体原子数密度 / nm⁻³','Solid-atom number density / nm⁻³'),xlabel='x / nm')
    save(fig,'adsorption-density')
    fig,ax=plt.subplots(1,3,figsize=(13,2.9),sharex=True,sharey=True,layout='constrained')
    for panel,t in zip(ax,[0,5,25]):
        i=int(np.flatnonzero(np.isclose(times,t))[0]);typ,xyz=snapshots[i]
        panel.scatter(xyz[typ==1,0]/10,xyz[typ==1,2]/10,s=9,c='#b79d62',alpha=.6,label='Si')
        panel.scatter(xyz[typ==2,0]/10,xyz[typ==2,2]/10,s=7,c='#ba7464',alpha=.45,label=tr('固体O','Solid O'))
        panel.scatter(xyz[typ==3,0]/10,xyz[typ==3,2]/10,s=22,c=teal,label=tr('水O','Water O'))
        panel.set(title=f'{t} ps · {int(counts[i,2])} '+tr('个水','waters'),xlabel='x / nm',xlim=bounds[0]/10,ylim=bounds[2]/10);panel.set_aspect('equal')
    ax[0].set_ylabel('z / nm');handles,labels=ax[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='outside lower center',ncol=3)
    save(fig,'adsorption-snapshots')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
```

Run python analyze_adsorption.py --run . --out figures --language en. The two raw records produce figures and CSV tables.

## Developing an adsorption example into a comparison

The example now supports a controlled design: keep crack geometry, water model, and temperature fixed, repeat the calculation at several reservoir conditions, and compare average population with pressure or fugacity. Each point needs its own preparation and sampling assessment. Different times along the single 100 bar trajectory are not different pressure states. An isotherm holds temperature fixed, while each horizontal-axis pressure specifies a separate thermodynamic condition whose population distribution must be sampled.

A real water-vapour reservoir requires an appropriate thermodynamic mapping. The ideal-reservoir setting uses fugacity coefficient one, making pressure enter directly into the chemical-potential relation. A nonideal equation of state supplies a fugacity correction. Relative humidity additionally refers to saturation vapour pressure at the chosen temperature. Connecting these quantities makes the simulation axis comparable with a specified experimental environment. Here, all numerical observations are interpreted under the stated 100 bar ideal-reservoir driving condition.

Material comparisons can separate geometry from chemistry. Changing crack width while preserving interaction parameters emphasizes available space and confinement. Holding coordinates fixed while varying validated surface parameters emphasizes molecular interactions. Actual hydroxylation changes composition, charge distribution, and local geometry and therefore belongs in a complete surface model, rather than an arbitrary charge edit. Controlling these changes individually helps connect differences in population and density to a specific material mechanism and guides which experimental comparison is most informative.

A dynamical study can begin from adequately sampled hydrated configurations, turn off exchange, and follow continuous molecular motion at specified temperature and boundaries. Displacements, orientations, and residence histories then acquire the time interpretation appropriate to that MD stage. Studying substrate softening or fracture-surface deformation also requires a mobile substrate with a suitable potential and checked water–solid cross interactions. Each extension adds the degrees of freedom needed by its scientific question rather than treating complexity as a goal in itself.

Two exercises use the existing record directly. First average over the final five ps and compare both population and density with the longer window. Then reduce the slice count from 60 to 30 and check that a smoother profile preserves the integrated count. The first changes temporal coverage; the second changes spatial resolution. Neither changes the molecular trajectory. Through these exercises, adsorption becomes a set of answerable questions about reservoir conditions, surface interactions, visited states, and the conversion of molecular records into comparable material properties.

## Further Reading and Open Materials

- [Water adsorption in silica](https://lammpstutorials.github.io/sphinx/build/html/tutorial6/water-adsorption-in-silica.html) · Simon Gravelle; Cecilia M. S. Alvares; Jacob R. Gissinger; Axel Kohlmeyer · CC BY4.0

  The prepared crack, TIP4P water, and GCMC/MD workflow

  Retains the parameters and 25 ps protocol; starts from the prepared substrate and adds numerical records and analysis.
- [The adsorption of gases on plane surfaces of glass, mica and platinum](https://doi.org/10.1021/ja02242a004) · Irving Langmuir · Scholarly citation

  Historical background to surface adsorption and site models
- [Surface chemistry: Nobel lecture](https://www.nobelprize.org/uploads/2018/06/langmuir-lecture.pdf) · Irving Langmuir · Scholarly citation

  The 1932 discussion of adsorption and surface effects
- [fix gcmc command](https://docs.lammps.org/fix_gcmc.html) · LAMMPS developers · Official documentation

  Reservoir conditions, pressure overriding chemical potential, molecular constraints, and counter definitions
- [units command](https://docs.lammps.org/units.html) · LAMMPS developers · Official documentation

  The ps, Å, eV, and bar units used with the metal convention
- [TIP4P water models](https://docs.lammps.org/Howto_tip4p.html) · LAMMPS developers · Official documentation

  Four-site geometry and virtual negative-charge position
