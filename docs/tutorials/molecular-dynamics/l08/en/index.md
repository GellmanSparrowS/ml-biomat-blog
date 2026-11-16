# From One Chain to Melts and Solutions

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l08/en/
Language: en

Follow a chain into a crowded polymer environment and measure concentration, packing, internal dimensions and motion.

## What changes when one chain becomes a crowd?

A shoelace can bend freely on a table. Put many laces together and pulling one may move or displace its neighbours. Polymer materials share this feature: an individual chain acts in an environment occupied by other chains. Heated plastic can flow, concentrated thickener solutions pour slowly, and soft polymer coatings resist the approach of another object. These behaviours require a description of many chains together. A single-chain radius of gyration remains useful, but we also need to ask how many neighbouring chains are present, how they fill the available space, and what restricts the motion of an entire molecule. The surroundings become part of the molecular question.

Two environments must first be distinguished. A polymer solution contains chains and a solvent. In an aqueous solution, water contributes hydration, transfers momentum, and changes the energetic cost of bringing segments together. A polymer melt consists mainly of polymer chains, with nearby space occupied by other segments. The simulated system in this lesson is a box of bead–spring chains without explicit solvent: 80 chains containing 20 beads each, or 1,600 beads altogether. Repulsion between densely packed segments and permanent connectivity let us examine local packing and chain motion in a melt. The earlier atomistic PEG-in-water example provides the complementary case in which water molecules are represented explicitly.

Equal bead counts do not make two models descriptions of the same substance. A bead here is an effective segment carrying a position and a mass; it has not been assigned to one ethylene oxide repeat unit and contains no explicit oxygen, carbon, or hydrogen structure. This representation focuses attention on connectivity, excluded volume, and concentration. Studying PEG hydration shells or ion coordination requires the corresponding chemical resolution. Studying how connected objects change shape in a crowded environment can benefit from the simpler bead–spring representation. The choice begins with the observable: which features of molecular structure are needed to explain that measurement, and which can be represented through effective interactions?

Separate the spatial extent of a coil from the volume excluded by its segments. A loosely wound piece of string encloses gaps that another string can enter. Two coils can overlap in spatial extent without their actual strands occupying the same position. A polymer’s gyration radius likewise describes a distribution of beads rather than the hard boundary of a solid sphere. Increasing chain concentration allows the regions occupied by different conformations to interpenetrate, while short-range repulsion still resists direct bead overlap. Large single-chain dimensions can therefore coexist with a high overall material density.

By the end of this lesson, you will have followed a complete route from generating connected coordinates through gentle overlap removal to measuring melt structure. The analysis proceeds through three levels. First we examine temperature and chain dimensions over time. Next we separate neighbours on the same chain from neighbours belonging to other chains. Finally we distinguish bead displacement from displacement of a whole-chain centre of mass. Three independently generated starting configurations reveal the variation produced by the same modelling rules. Later lessons add permanent crosslinks to these melts, so the present workflow also establishes a practical foundation: a defined starting state that several controlled branches can share.

## Why replace atoms with beads? The historical problem of long-chain motion

Long-chain motion presents an easily underestimated difficulty. A small segment can bend quickly while an entire chain may take much longer to move into a different region. Tracking every atom spends computation on many fast vibrations, whereas the larger rearrangement of interest emerges only over a much longer trajectory. A natural strategy is to combine some local degrees of freedom into fewer effective units while preserving two important constraints: neighbouring units remain connected, and distinct units resist occupying the same space. Coarse graining then shifts the question from the vibration of every chemical bond to the consequences of connecting many mobile units into a chain. The useful level of detail follows the time and length scales being studied.

In their 1990 bead–spring melt study, Kurt Kremer and Gary Grest compared motion across different chain lengths, placing the relatively freer rearrangement of short chains and the constraints on long chains within one modelling framework. A central advance was to make chain length, connectivity, and crowding controllable variables and then test the associated physical pictures against trajectories. The historical concept drawing places local segment motion, whole-chain displacement, and geometrical constraints from surrounding chains side by side. Its tube represents an effective region of motion imposed by neighbouring chains; a hard tube is not an additional object inserted into the material. The drawing explains the mechanism that motivated the comparison, rather than assigning every dense chain system to the same regime.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l08/en/#en-s2)

Figure 1 · Kremer and Grest studied motion across chain lengths in a controlled bead–spring framework. The diagram relates local motion, whole-chain displacement and constraints from neighbours.

This distinction explains why a picture of crossing chains is not enough to diagnose strong entanglement. Three-dimensional curves naturally cross when projected onto a page, and a crossing may not correspond to a contact in space. Short chains can also interpenetrate without displaying the slow relaxation characteristic of much longer chains. With 20 beads per chain, the present analysis concentrates on local packing, the dimensions of finite chains, and displacement over the recorded time window. An entanglement study extends the chain-length range, follows the loss of orientational memory, and applies suitable topological and relaxation analyses. Density, visual interpenetration, and entanglement each describe a different level of information.

Removing degrees of freedom also changes how momentum is exchanged with the surroundings. Explicit water transfers motion through molecular interactions and collisions. Here, the Langevin bath applies friction and random forces directly to beads, maintaining thermal motion through a simpler dynamical description. Both approaches produce a temperature, but their detailed dynamics differ. Deciding whether a coarse-grained model suits a flow, diffusion, or viscosity question therefore requires inspecting its thermostat as well as its potential. A simplified model becomes useful when its retained mechanisms are sufficiently explicit that a comparison addresses a definite physical question.

The simulation uses reduced units, taking the bead-size parameter σ, interaction energy ε, and bead mass m as reference scales. Setting σ to one means expressing lengths in multiples of σ; it does not identify the diameter as one nanometre. Time is measured in τ, constructed from those same reference quantities, and a reduced temperature T*=1 places thermal energy on the scale ε. Comparing with nanometres, seconds, or pascals for a particular polymer requires a mapping based on experimental measurements or a finer model, such as chain dimensions, density, relaxation, or diffusion. Assigning an arbitrary atom name to a bead would bypass the physical calibration that gives such a comparison meaning.

## Connectivity and repulsion: reading the bead–spring model

Begin with two beads that are not connected. Far apart, they exert no force on one another in this model. When they approach too closely, repulsion rises sharply and makes overlap energetically expensive. We use the repulsive part of the Lennard–Jones potential, truncate it at its minimum, and shift it upward so that both energy and force reach zero at the cutoff. This is the WCA repulsion. It retains an effective bead volume without a long-range attractive tail. The high density in this lesson is therefore imposed through the box volume. Closely packed beads describe this constrained dense fluid; a study of liquid–vapour coexistence or a polymer’s cohesive energy would require the corresponding attractive interactions and thermodynamic protocol.

Keeping short-range repulsionEq. 1

![Keeping short-range repulsion](https://ml-biomat.com/static/agent-math/c26582e3fc3c240160a5435b.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| U_{WCA} | WCA potential energy of an ordinary pair | ε |
| r | Distance between bead centres | σ |
| ε | Energy scale; reduced value one | energy |
| σ | Length scale; reduced value one | length |
| 2^(1/6)σ | Cutoff distance, about 1.122462σ | σ |
| 12, 6, 1/6 | Exponents; 1/6 denotes the sixth root | 1 |
| =, +, −, / | Equality, addition, subtraction, division; adjacent quantities multiply | 1 |
| <, ≥, { } | Less than, greater than or equal; choose a branch by distance | 1 |

Reading the relationshipThe original LJ minimum has energy −ε. Adding ε makes it zero, and its zero slope makes the force continuous at this cutoff.

A worked exampleWith ε=σ=1 and r=1, the bracket is 1−1=0 and U=1. At r=2^(1/6), U=0, and it remains zero at larger separation.

ConditionsThe nonbonded interaction here is purely repulsive WCA. Its bonded-neighbour counterpart is already included in the bond potential.

Now consider adjacent beads along a chain. They must resist both collapse onto one another and unlimited separation. The bond interaction therefore combines short-range repulsion with an increasingly strong restoring force at large separation. The LAMMPS FENE bond already includes a short-range WCA term in addition to its nonlinear elastic term. Its parameter R₀ sets the scale of maximum extension, a different concept from the equilibrium bond length. For K=30, R₀=1.5, and ε=σ=1, competition between the two terms places the minimum near 0.96σ. The coordinate generator begins with a neighbouring-bead separation of 0.97σ. Setting every bond to R₀ would instead put it at the rapidly increasing edge of the interaction.

FENE elasticity and repulsion together set the bond lengthEq. 2

![FENE elasticity and repulsion together set the bond length](https://ml-biomat.com/static/agent-math/91873c7546e438279238523f.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| U_{bond} | Complete bond potential energy | ε |
| K | Nonlinear elastic strength, here 30 | ε/σ² |
| R₀ | Maximum-extension scale, here 1.5; distinct from equilibrium length | σ |
| r | Separation of bonded beads | σ |
| U_{WCA} | Short-range repulsion defined above | ε |
| ln | Natural logarithm, requiring a positive dimensionless argument | 1 |
| ² | A quantity multiplied by itself | 1 |
| =, −, +, /, 1/2 | Equality, negative sign or subtraction, addition, division and one half; adjacent quantities multiply | 1 |
| < | Less than; specifies the allowed separation range | 1 |

Reading the relationshipAs r approaches R₀, the logarithm argument approaches zero and the negative logarithm rises sharply. WCA prevents collapse at small r. Their competition creates a finite preferred spacing.

A worked exampleFor K=30, R₀=1.5 and r=1, the elastic term is 19.83780ε and WCA is 1ε, giving 20.83780ε. The combined minimum lies near 0.961σ.

ConditionsA permanent bead–spring bond matching LAMMPS bond_style fene. Resolving motion near R₀ requires a sufficiently small step; chemical rupture uses a separate model.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l08/en/#en-s3)

Figure 2 · Curves are pointwise evaluations of the analytical potentials. The complete bond contains one WCA contribution, and directly bonded pairs have zero weight in the ordinary nonbonded term.

Because bonded neighbours already receive their repulsion through the bond interaction, the ordinary pair interaction must avoid counting it twice. The command special_bonds fene assigns zero ordinary nonbonded weight to directly connected 1–2 pairs, while retaining full weight for 1–3 pairs separated by two bonds and 1–4 pairs separated by three. These numbers describe distances along the connectivity graph, not bead-type labels. More distant members of the same chain and beads belonging to different chains also interact through the ordinary WCA potential. The connectivity table thus determines which neighbours contribute through which energy term, even though this model contains no separate angle or dihedral potentials.

Analytical pair and bond potentials: read energy and force along increasing separation.

[Figure: Analytical potential curve](https://ml-biomat.com/tutorials/molecular-dynamics/l08/en/#en-s3)

The force along separation is the negative energy slope: positive separates, negative restores. The exercise evaluates analytical functions with ε=σ=1 and R₀=1.5σ.

The phrase finite extensibility has a specific computational meaning. As a bond approaches R₀, its energy and restoring force increase sharply, and an adequately resolved trajectory is strongly pulled back before reaching that limit. The bond is not a chemical link that automatically breaks at a selected distance; connectivity remains fixed throughout this calculation. An abnormally long bond calls for examination of initial overlaps, time step, loading rate, and thermal control so that integration resolves rapid force changes. Studying actual bond rupture requires a model capable of changing connectivity or representing reactions, with the associated parameters and energy processes defined accordingly.

The interactive exercise lets you inspect the ordinary pair interaction, the elastic FENE term, and the complete bond potential separately. Start near a separation of σ and examine the competition between repulsion and restoration, then approach 1.5σ to see why the bond becomes increasingly steep. Changing K changes the restoring strength and the location of the combined minimum. The exercise evaluates analytical functions, linking input parameters to energy and force curves. In the actual melt, many neighbours exert forces simultaneously and thermal motion continually changes separations. Bond lengths therefore form a distribution rather than remaining at the minimum of an isolated two-bead interaction.

## How to put 80 chains into one box

Box size is determined first by bead count and number density. Number density asks how many beads occupy a unit volume. It is related to mass density, but the two quantities should retain distinct names and units. With 1,600 beads and a reduced number density of 0.85, the cubic box has a side length of approximately 12.347σ. Chain positions are distributed throughout the box, and successive beads take steps in random directions. Periodic boundaries allow a chain to cross opposite sides of the box. The coordinate file records both wrapped positions and image counts, preserving connectivity and allowing later measurements to reconstruct continuous molecular geometry.

From number density to box sizeEq. 3

![From number density to box size](https://ml-biomat.com/static/agent-math/d03f1fad6700a0503ff8092c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ρ | Bead number density | σ⁻³ |
| N | Total bead count, here 1600 | 1 |
| L | Cubic box side length | σ |
| ³, 1/3 | Cube gives volume; cube root recovers a length | 1 |
| =, / | Equality and division | 1 |

Reading the relationshipA cubic box has volume L cubed. Count divided by volume gives number density, and rearranging obtains the side length.

A worked example1600/0.85=1882.35294σ³; its cube root is L=12.34715838σ. Unit-mass beads have the same numerical mass density, but its unit is m/σ³.

ConditionsAn orthogonal cubic periodic box; σ is the model length scale.

Random placement does not automatically produce a sensible liquid structure. Scattering many flexible threads into a small box can place some segments too close together; the corresponding simulation would begin with very large repulsive forces. The generator first requires every new bead to remain at least 0.65σ from previously placed beads and uses steps of 0.97σ to connect a chain. This removes severe coordinate coincidences while still permitting distances closer than normal WCA contacts. Each proposed position is checked using the nearest periodic-image separation. Otherwise, beads that appear far apart on opposite sides of the displayed box could overlap when its periodic copies are joined.

### Generate 80 initial chains

```
"""Generate 80 chains of 20 beads at reduced number density 0.85.

The default seed reproduces the first reference configuration. A bead is a
coarse-grained segment with mass 1, not a specified chemical repeat unit.
"""
from pathlib import Path
import argparse
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=20263001)
    parser.add_argument('--output', type=Path, default=Path('initial.data'))
    args = parser.parse_args()
    count, chain_length, density = 1600, 20, 0.85
    length = (count/density)**(1/3)
    rng = np.random.default_rng(args.seed)
    coordinates, bonds = [], []
    for chain in range(count//chain_length):
        current = rng.uniform(0, length, 3)
        for local in range(chain_length):
            for attempt in range(100000):
                if local == 0:
                    candidate = rng.uniform(0, length, 3)
                else:
                    direction = rng.normal(size=3)
                    candidate = current + 0.97*direction/np.linalg.norm(direction)
                if coordinates:
                    delta = np.array(coordinates)-candidate
                    delta -= length*np.round(delta/length)
                    if np.min(np.sum(delta*delta, axis=1)) < 0.65**2:
                        continue
                break
            else:
                raise RuntimeError('No acceptable next bead; change the packing protocol.')
            coordinates.append(candidate.copy())
            current = candidate
            if local:
                bonds.append((len(coordinates)-1, len(coordinates)))
    lines = ['Generated FENE chain starting configuration', '',
             f'{count} atoms', f'{len(bonds)} bonds', '',
             '1 atom types', '2 bond types', '',
             f'0 {length:.15g} xlo xhi', f'0 {length:.15g} ylo yhi',
             f'0 {length:.15g} zlo zhi', '', 'Masses', '', '1 1.0', '',
             'Atoms # bond', '']
    for i, position in enumerate(coordinates):
        image = np.floor(position/length).astype(int)
        wrapped = position-length*image
        lines.append(f'{i+1} {i//chain_length+1} 1 ' +
                     ' '.join(f'{v:.15g}' for v in wrapped) + ' ' +
                     ' '.join(str(v) for v in image))
    lines += ['', 'Bonds', '']
    lines += [f'{j+1} 1 {left} {right}' for j, (left, right) in enumerate(bonds)]
    args.output.write_text('\n'.join(lines)+'\n', encoding='utf8', newline='\n')
    print(f'{count} beads, {len(bonds)} bonds, box length {length:.8f} sigma')


if __name__ == '__main__':
    main()
```

Check each new bead with minimum-image distances and save molecule IDs, connectivity and image flags.

The chains next receive a gentle opportunity to reorganize. A preparation stage temporarily uses a finite-height soft repulsion whose strength increases gradually, while harmonic bonds keep adjacent beads near 0.97σ. This stage lasts 40τ with a time step of 0.002τ. The input then switches to the complete WCA and FENE interactions, minimizes the energy, and records 100τ of thermal motion with a time step of 0.005τ. Each stage has a specific role: separate close neighbours gradually, adjust local geometry after the model change, and observe motion under the final interactions. Because the potential changes between stages, the whole preparation sequence is not a single equilibrium trajectory governed by one unchanged Hamiltonian.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l08/en/#en-s4)

Figure 3 · Preparation stages use different potentials for different tasks. The 100τ record begins from the minimized state under the complete FENE/WCA model.

### From soft preparation to FENE melt records

```
units lj
atom_style bond
boundary p p p
special_bonds fene
neighbor 0.4 bin
neigh_modify every 1 delay 0 check yes
read_data initial.data
bond_style harmonic
bond_coeff * 100.0 0.97
pair_style soft 1.122462048309373
pair_coeff * * 0
velocity all create 1.0 20263101 mom yes rot no dist gaussian
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 20263201 zero yes
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
fix bath all langevin 1.0 1.0 1.0 20263301 zero yes
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
write_restart melt.restart
write_data melt.data
```

Complete preparation: 40τ of gentle separation, interaction switch, minimization and a 100τ record.

### Run three independently prepared configurations

```
#!/usr/bin/env bash
set -euo pipefail
lmp=${LAMMPS:-lmp}
export OMP_NUM_THREADS=1
mkdir melt-runs
for replica in 1 2 3; do
  folder="melt-runs/n1600-rep${replica}"
  mkdir "$folder"
  python make_melt.py --seed "$((20263000 + replica))" --output "$folder/initial.data"
  python - "$replica" "$folder" <<'PY'
from pathlib import Path
import sys
replica = int(sys.argv[1])
destination = Path(sys.argv[2])
text = Path('prepare.lmp').read_text(encoding='utf8')
for offset in [100, 200, 300]:
    text = text.replace(str(20263001 + offset), str(20263000 + replica + offset))
(destination/'prepare.lmp').write_text(text, encoding='utf8', newline='\n')
PY
  ( cd "$folder"; "$lmp" -in prepare.lmp -log simulation.log > stdout.log 2>&1 )
done
python analyze_melt.py melt-runs --output figures --language en
```

Run in the folder containing the coordinate generator, preparation input and analysis program. The geometry seed and three velocity/thermostat seeds vary with configuration number while other conditions remain fixed. Outputs go into a new melt-runs folder.

The molecule ID in the generated file deserves attention. A bead ID identifies the same particle throughout the trajectory; its molecule ID identifies its original chain. Every bead has the same atom type here, meaning that it uses the same mass and nonbonded parameters. Bond types separately identify connection parameters. The file reserves two bond types, using only the first in this lesson; the second later distinguishes crosslinks. These integers are neither coordinates nor direct definitions of colours or chemical elements. Separating identity, grouping, and interaction class makes the later network records easier to interpret.

The run produces melt.data and melt.restart, preserving the state in forms useful for inspecting structure and continuing a calculation with the matching software. The file thermo.dat records temperature, energy per bead, pressure components, and box lengths. The file chain-rg.dat retains the radius of gyration of each of the 80 chains, and trajectory.lammpstrj stores positions, velocities, and periodic image counts. Retaining chain-resolved records matters: a few unusually extended molecules can be hidden by a single overall average. Later crosslinking, deformation, and replicate comparisons begin from these defined records, making it possible to connect an observed difference to the operation that produced it.

## After temperature settles, do chains remember their starting shapes?

Read the origin of the time axis before interpreting the curves. Here, 0τ follows soft preparation, the interaction change, and minimization. The next 100τ use the full FENE/WCA model. Minimization primarily changes positions; it does not automatically adjust the velocity distribution to a new equilibrium state. During the initial interval, potential and kinetic energy continue to exchange and the thermostat supplies or removes energy. A temperature transient followed by fluctuations around the target therefore has a physical explanation in the preparation sequence. Marking that transient and the later observation window makes the process clearer than reporting one temperature averaged over the entire run.

### Measured temperature and chain dimensions

Three 1600-bead melt records, beginning at 0τ after FENE/WCA minimization; shading marks the 50–100τ analysis window.

LAMMPS 30 Sep 2026 Update 1; official bead–spring interaction model, with 1600 beads in 80 chains of 20, ρ*=0.85 and T*=1, using three initial configurations. The FENE/WCA dynamics time step is 0.005τ.

[Download reference data and complete inputs (ZIP) 5.92 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-network-melt-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l08/en/#en-s5)

Each of three initial configurations undergoes 40τ of soft repulsion and FENE/WCA minimization before the 100τ bead–spring record begins at 0τ. The plots retain each run’s temperature and the mean radius of gyration of its 80 chains. Shading identifies the 50–100τ statistical window.

Temperature summarizes squared velocities, whereas a change in whole-chain shape requires many beads to move cooperatively. Their adjustment times can differ considerably. The accompanying plot therefore follows the mean radius of gyration of all 80 chains as well as temperature, retaining separate curves for the three starting configurations. If temperature fluctuates near one while chain size continues to evolve, the size record deserves further observation. A seemingly steady average can be examined more closely by comparing distributions in successive time intervals, distances across longer chain segments, and orientational correlations. These measurements ask, at different scales, how much memory of the initial arrangement remains.

To give every statistic a precise observation range, subsequent structural and displacement analyses use 50–100τ. A trajectory frame is saved every 2.5τ, giving 21 frames in this interval. Each contains 80 chains, so there are 1,680 recorded chain conformations. Successive conformations of a given chain are generally correlated, and neighbouring chains share an interacting environment. The number 1,680 therefore counts records, rather than independent experiments. Results from the three starting configurations remain separate in the plots, distinguishing the breadth of conformations within a box from variation after preparing another box. This distinction becomes central when later lessons compare different crosslink conditions.

The vertical axis of a distribution is a probability density, not the probability of one exact size. With a bin width of 0.1σ and a height of 2σ⁻¹, the bin has area 0.2 and contains approximately 20% of the recorded conformations. Changing bin width alters heights and detail, so all three configurations use common bin boundaries. Equal averages need not imply equal distributions: a group concentrated near 3σ and another switching between 2σ and 4σ can share a mean while displaying different conformational freedom. Read the overall breadth before interpreting reproducible peaks or changes in the tails.

For the first configuration in this window, the mean radius of gyration is approximately 2.151σ, its root-mean-square value is 2.184σ, and the root-mean-square end separation is 5.262σ. These values describe different measurements. Gyration samples the distribution of all beads around the chain centre, while end separation selects just the two terminal beads. Squaring before averaging and then taking a square root also gives greater weight to large conformations than averaging lengths directly. The distributions show that chains of the same 20-bead length occupy a range of sizes. Comparisons across models or chain lengths should preserve both the geometrical definition and the order of averaging.

## Who are a bead’s neighbours? Separating internal structure from packing

A crowded melt snapshot makes it difficult to identify the origin of a bead’s closest neighbours. Change the viewpoint: stand on one bead and count how many others occur at different distances. More pairs in a thin spherical shell indicate more frequent neighbours at that separation. Comparing different radii fairly requires division by shell volume, because a larger-radius shell naturally accommodates more points. Comparing those counts with a uniform distribution at the same particle count and volume gives the radial distribution function g(r). It converts a crowded three-dimensional image into a distance statistic with a defined reference, allowing packing at different separations to be compared quantitatively.

Normalize pair counts by spherical-shell volumeEq. 4

![Normalize pair counts by spherical-shell volume](https://ml-biomat.com/static/agent-math/d97e947f56a13d96efd6989d.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| g(r) | Shell-averaged radial distribution | 1 |
| r | Central shell radius | σ |
| V | Box volume | σ³ |
| C(r) | Total unordered-pair count in the shell over J frames; each pair counted once per frame | 1 |
| J | Number of frames, here 21 per configuration | 1 |
| N | Number of beads per frame, here 1600 | 1 |
| N(N−1)/2 | Number of distinct unordered pairs | 1 |
| ΔV | Exact volume of the spherical shell | σ³ |
| r₊, r₋ | Outer and inner shell radii | σ |
| π | Pi, approximately 3.14159 | 1 |
| ³ | Cube | 1 |
| =, /, −, 2, 4/3 | Equality, division, subtraction; factor two matches unordered counting, and 4/3 comes from sphere volume; adjacent quantities multiply | 1 |

Reading the relationshipFor a uniform reference, the chance for a pair separation to fall in the shell is its volume divided by the box volume. Dividing observed counts by that expectation gives relative structure.

A worked exampleFor N=100, J=10, V=1000σ³ and ΔV=1σ³, the uniform reference predicts 49.5 unordered pairs. An observed count of 99 gives g=2.

ConditionsA homogeneous bulk system with shell radius below half the shortest box length. All geometric pairs are counted and separated by connectivity, sharing the total-pair denominator.

We further divide pairs into three classes: directly bonded neighbours, other pairs on the same chain, and pairs belonging to different chains. All three use the same total-pair normalization, so their curves add exactly to the complete g(r). Direct bonds contribute a narrow peak near the typical bond length. The other classes describe folding within a chain and packing by surrounding chains. Our coordinate analysis deliberately includes the geometrical distances of bonded neighbours. This choice is separate from excluding 1–2 pairs from the ordinary nonbonded force calculation: one defines a structural count, while the other prevents duplicate contributions to the interaction energy.

### Structure within and between chains

Pair curves average the 50–100τ records of three configurations. Their identity contributions add to total g(r); internal-distance curves retain the three runs separately.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l08/en/#en-s6)

The left panel decomposes the total pair distribution into directly bonded, other same-chain and different-chain pairs. All contributions share the total-pair normalization and add pointwise to g(r). The right panel compares internal mean-square distances at each bond separation; the dashed line represents independent equal-length steps.

Returning from spatial separation to connectivity, we can count separation along the chain in bonds. Choose beads i and i+s, square their spatial distance, and average over every allowed starting bead, every chain, and every selected frame. This gives the internal-distance function S(s). At s=1 it is the mean squared bond length. At s=19, a 20-bead chain contributes only its two ends, giving the mean squared end separation. Intermediate values progressively enlarge the scale of observation. Even two systems with similar overall gyration radii can then be compared for differences between the arrangement of short segments and the extension of longer portions.

Mean squared separation across s bondsEq. 5

![Mean squared separation across s bonds](https://ml-biomat.com/static/agent-math/ade091bf31e82f669343332a.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| S(s) | Mean squared internal distance | σ² |
| s | Separation in bonds along the chain, one to 19 | 1 |
| J, j | Frame count and frame index | 1 |
| M, a | Chain count and chain index, with M=80 | 1 |
| n | Beads per chain, here 20 | 1 |
| i | Starting bead index along a chain | 1 |
| rₐ,ᵢ⁽ʲ⁾ | Unwrapped position of bead i on chain a in frame j | σ |
| Σ | Sum over the listed frames, chains and starting beads | 1 |
| \| \|² | Sum of squared vector components | σ² |
| =, +, −, / | Equality, addition, subtraction, division; adjacent quantities multiply | 1 |

Reading the relationshipA chain of n beads has n−s eligible pairs at separation s. Multiplying by chain and frame counts gives the averaging denominator.

A worked exampleFor four beads at (0,0), (1,0), (1,1), (2,1), both s=2 pair distances squared equal two, so S(2)=2. At s=3 only the ends remain, giving S(3)=5.

ConditionsLinear chains with fixed order and equal bead count, reconstructed with periodic images. All eligible pairs receive equal statistical weight.

A peak in g(r) also needs its statistical definition. A value above one means that a neighbour is more likely at that distance than in the uniform reference; it does not by itself identify an attractive force. Bonded beads often appear near a characteristic separation even when the ordinary nonbonded potential is entirely repulsive. A nearly empty range can arise from excluded volume or connectivity constraints. The structural distribution combines the effects of interactions and accessible conformations. Separating pair identities before interpreting the peaks makes it easier to relate the measured structure to the model’s mechanisms.

If successive step directions were independent and shared the same step-length statistics, cross terms between their directions would cancel on average and S(s) would be proportional to s. The plot divides S(s) by sS(1), using a horizontal line at one as this simple reference. The observed curves lie above one, showing that directional and excluded-volume correlations extend these finite segments more strongly than the independent-step picture. For the first configuration, S(19) is approximately 27.690σ², compared with about 17.699σ² for 19S(1). Beads in this model therefore cannot be treated individually as independent random steps; a model bead has not automatically been calibrated as a statistically independent Kuhn segment.

## Why can a bead move faster than its whole chain?

A chain displays two kinds of motion at once: beads rearrange around its centre, and the centre itself changes position. Local rearrangement can alter structure without carrying the entire molecule far away. Imagine people holding hands in a line. Each person can shift their feet or turn, while the position of the group’s centre depends on their combined movement. The analogy separates local motion from collective translation, although simulated beads have no intention or active drive; interactions, inertia, and the thermostat produce their motion. Measuring the two displacements separately reveals the scale at which an apparently active trajectory is changing most strongly.

### A distribution of sizes at one chain length

Each configuration contributes 80 chains in 21 frames. Histogram areas are normalized to one; records contain temporal and interchain correlations.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l08/en/#en-s7)

Size distributions for 80 chains at each of 21 saved times over 50–100τ in each run. Each histogram has unit area, and the three configurations remain separate. Adjacent records of one chain and neighboring chains in one box are correlated.

A mean squared displacement begins by choosing a lag time. Positions separated by that interval are subtracted, the displacement-vector length is squared, and the results are averaged. Squaring counts motion in opposite directions positively instead of allowing leftward and rightward movement to cancel. The bead MSD averages over individual beads. The chain-centre MSD first finds each molecular centre and then averages its displacement over chains. Our program also removes translation shared by the entire box, preventing uniform drift from adding a contribution unrelated to internal transport. Periodic image counts unwrap the coordinates, so a bead crossing a box boundary continues along a continuous measured path.

Measure displacement after removing whole-box driftEq. 6

![Measure displacement after removing whole-box drift](https://ml-biomat.com/static/agent-math/56f33b9ed71e4007019c4f13.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| MSD | Mean squared displacement | σ² |
| Δt | Lag between two frames | τ |
| t | Time origin for a displacement | τ |
| rᵢ | Unwrapped bead position; replace by the chain centre for chain-centre analysis | σ |
| R_{box} | Mean position of all equal-mass beads in the frame | σ |
| r̃ᵢ | Position after subtracting the whole-box centre | σ |
| ⟨ ⟩ᵢ,ₜ | Average over objects and all eligible time origins | 1 |
| \| \|² | Sum of squared displacement components | σ² |
| =, +, − | Equality, addition and subtraction | 1 |

Reading the relationshipRemoving common translation isolates relative motion. Squaring counts all directions positively, and averaging measures the scale at a chosen lag.

A worked exampleTwo drift-corrected displacements (1,0,0)σ and (−1,0,0)σ have zero mean displacement but MSD=(1+1)/2=1σ².

ConditionsThe 50–100τ window, equal masses and fixed box, with a maximum lag of 25τ. Overlapping time origins are correlated.

### Bead and chain-centre displacement

Unwrapped coordinates with whole-box drift removed, using all eligible origins in 50–100τ and a maximum lag of 25τ. Each line retains one configuration.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l08/en/#en-s7)

Periodic image flags reconstruct continuous coordinates, then the translation of all beads is removed. Bead and chain-centre mean-square displacements use every eligible origin in 50–100τ, up to a 25τ lag. These short-lag records describe segmental and whole-chain motion within this trajectory window.

Within the 50–100τ interval, evaluating a given lag from every available starting frame makes fuller use of the finite record. Longer lags have fewer possible origins, so the graph stops at 25τ. For the first configuration at that lag, the bead MSD is approximately 2.569σ², compared with 0.568σ² for the chain centre. Beads have travelled through internal bending and rotation while the molecular centre has moved less far. Separate colours retain the different starting configurations, and solid versus dashed lines identify beads and molecular centres.

Multiple time origins describe the recorded trajectory more fully, but they do not create new independent material samples. At a lag of 25τ, displacements from 50 to 75τ and from 52.5 to 77.5τ share neighbouring parts of the same motion. That is why the plot retains three starting configurations instead of presenting only a smooth average with an exceptionally narrow band. Statistical uncertainty can be examined by computing measurements in sufficiently long contiguous time blocks and comparing independently prepared systems. Particles, chains, time blocks, and separate simulations each play a different role in defining independence.

Extracting a diffusion coefficient requires a sufficiently long interval in which displacement is approximately linear in lag time, together with checks on the fitting range, correlations, and variation across runs. Inertia, internal relaxation, and constraints from neighbouring chains can all curve the record at shorter times. We therefore retain the observed lag dependence rather than fitting the entire segment to one straight line. A comparison with a particular material’s diffusion experiment would extend the undeformed trajectory and establish the mapping from reduced to physical time. Langevin damping is also part of the dynamical model: changing it can alter rates even when static chain dimensions remain similar.

## Using the model to ask material questions

The complete analysis program connects the measurements above. It sorts particles by ID, reconstructs continuous coordinates from periodic images, and groups beads by their 20-bead molecule IDs. Recomputed chain radii are checked individually against the native LAMMPS records. Pair statistics use nearest periodic-image distances, whereas internal chain distances and displacements use unwrapped coordinates. The distinction is practical: counting nearby neighbours requires the periodic environment, while measuring a complete chain or accumulated motion requires continuous molecular geometry. Applying one coordinate representation indiscriminately to every task can introduce artificial jumps at a box boundary.

### Complete structure and displacement analysis

```
"""Read chain packing, internal dimensions and motion from FENE melt records.

python analyze_melt.py records --output figures --language en
records may contain one prepare.lmp run, or n1600-rep1/2/3 subdirectories.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


def read_trajectory(file):
    frames, steps, lengths = [], [], []
    with file.open(encoding='utf8') as stream:
        while stream.readline():
            step = int(stream.readline())
            assert stream.readline().startswith('ITEM: NUMBER')
            count = int(stream.readline())
            assert stream.readline().startswith('ITEM: BOX BOUNDS pp pp pp')
            box = np.array([list(map(float, stream.readline().split())) for _ in range(3)])
            fields = stream.readline().split()[2:]
            rows = np.array([list(map(float, stream.readline().split())) for _ in range(count)])
            rows = rows[np.argsort(rows[:, fields.index('id')])]
            assert np.array_equal(rows[:, 0], np.arange(1, count+1))
            assert np.array_equal(rows[:, fields.index('mol')], np.arange(count)//20+1)
            length = box[:, 1]-box[:, 0]
            position = rows[:, [fields.index(q) for q in ['x', 'y', 'z']]]
            images = rows[:, [fields.index(q) for q in ['ix', 'iy', 'iz']]]
            frames.append(position+images*length)
            steps.append(step)
            lengths.append(length)
    return np.array(steps), np.array(frames), np.array(lengths)


def native_rg(file):
    records = {}
    lines = [s for s in file.read_text().splitlines() if s and not s.startswith('#')]
    i = 0
    while i < len(lines):
        step, count = map(int, lines[i].split())
        records[step] = np.array([float(s.split()[1]) for s in lines[i+1:i+count+1]])
        i += count+1
    return records


def inspect(folder):
    steps, positions, lengths = read_trajectory(folder/'trajectory.lammpstrj')
    assert np.allclose(lengths, lengths[0])
    n = positions.shape[1]
    chain_count = n//20
    time = steps*0.005
    chains = positions.reshape(len(steps), chain_count, 20, 3)
    centers = chains.mean(axis=2)
    rg = np.sqrt(np.mean(np.sum((chains-centers[:, :, None])**2, axis=-1), axis=-1))
    end = chains[:, :, -1]-chains[:, :, 0]
    re = np.linalg.norm(end, axis=-1)
    native = native_rg(folder/'chain-rg.dat')
    error = max(np.max(np.abs(native[int(s)]-v)) for s, v in zip(steps, rg))
    if error > 0.0001:
        raise ValueError('Gyration reconstruction differs from the native record.')
    late = time >= 50
    internal = np.array([np.mean(np.sum((chains[late, :, s:]-chains[late, :, :-s])**2,
                                       axis=-1)) for s in range(1, 20)])
    # Geometrical pair distributions include directly bonded neighbors. Divide
    # unordered pair counts by N(N-1)/2 times shell-volume / box-volume.
    left, right = np.triu_indices(n, k=1)
    same = left//20 == right//20
    bonded = same & (right-left == 1)
    edges = np.linspace(0, 6, 121)
    counts = np.zeros((3, len(edges)-1))
    for frame in positions[late]:
        delta = frame[right]-frame[left]
        delta -= lengths[0]*np.round(delta/lengths[0])
        distance = np.linalg.norm(delta, axis=1)
        for row, selection in enumerate([bonded, same & ~bonded, ~same]):
            counts[row] += np.histogram(distance[selection], edges)[0]
    shell = 4*np.pi*(edges[1:]**3-edges[:-1]**3)/3
    pair_g = counts * (2*np.prod(lengths[0])) / (late.sum()*n*(n-1)*shell)
    # Remove whole-box translation before bead and molecular COM displacement.
    pos = positions[late]
    pos = pos-pos.mean(axis=1, keepdims=True)
    com = pos.reshape(len(pos), chain_count, 20, 3).mean(axis=2)
    maxlag = (len(pos)-1)//2
    msd = np.array([[np.mean(np.sum((pos[lag:]-pos[:-lag])**2, axis=-1)),
                     np.mean(np.sum((com[lag:]-com[:-lag])**2, axis=-1))]
                    for lag in range(1, maxlag+1)])
    thermo = np.loadtxt(folder/'thermo.dat')
    summary = dict(beads=n, chains=chain_count, beads_per_chain=20,
                   box_length_sigma=lengths[0].tolist(),
                   density=float(n/np.prod(lengths[0])), frames=len(steps),
                   late_window_tau=[50, 100], late_frames=int(late.sum()),
                   mean_rg_sigma=float(rg[late].mean()),
                   rms_rg_sigma=float(np.sqrt(np.mean(rg[late]**2))),
                   rms_re_sigma=float(np.sqrt(np.mean(re[late]**2))),
                   mean_bond_square_sigma2=float(internal[0]),
                   mean_re2_over_mean_rg2=float(np.mean(re[late]**2)/np.mean(rg[late]**2)),
                   native_rg_max_error_sigma=float(error),
                   late_mean_T=float(thermo[thermo[:, 1] >= 50, 2].mean()),
                   late_max_bond_sigma=float(thermo[thermo[:, 1] >= 50, -1].max()),
                   internal_distance_sigma2=internal.tolist(),
                   lag_tau=(np.arange(1, maxlag+1)*2.5).tolist(),
                   bead_msd_sigma2=msd[:, 0].tolist(), com_msd_sigma2=msd[:, 1].tolist())
    return dict(time=time, rg=rg, re=re, late=late, internal=internal,
                pair_r=(edges[1:]+edges[:-1])/2, pair_g=pair_g, msd=msd,
                thermo=thermo, summary=summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('records', type=Path)
    parser.add_argument('--output', type=Path, default=Path('figures'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args()
    folders = [args.records] if (args.records/'trajectory.lammpstrj').exists() else sorted(args.records.glob('n1600-rep[123]'))
    if not folders:
        raise ValueError('No melt preparation records found.')
    results = [inspect(folder) for folder in folders]
    args.output.mkdir(parents=True, exist_ok=True)
    zh = args.language == 'zh'
    def tr(a, b): return a if zh else b
    installed = {f.name for f in font_manager.fontManager.ttflist}
    fonts = ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC',
             'WenQuanYi Zen Hei', 'DejaVu Sans']
    plt.rcParams.update({'font.family': [f for f in fonts if f in installed],
                         'font.size': 13, 'axes.titlesize': 15,
                         'svg.fonttype': 'path', 'axes.unicode_minus': False,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'figure.facecolor': '#fbfaf6', 'axes.facecolor': '#fbfaf6'})
    colors = ['#167d84', '#c16b3d', '#466eaa']
    def save(fig, name):
        fig.savefig(args.output/f'{name}-{args.language}.svg', bbox_inches='tight')
        fig.savefig(args.output/f'{name}-{args.language}.png', bbox_inches='tight', dpi=150)
        plt.close(fig)
    fig, axes = plt.subplots(2, 1, figsize=(12, 7), layout='constrained')
    for i, record in enumerate(results):
        thermo = record['thermo']
        label = tr(f'初始构型 {i+1}', f'Initial configuration {i+1}')
        axes[0].plot(thermo[:, 1], thermo[:, 2], color=colors[i], lw=1, label=label)
        axes[1].plot(record['time'], record['rg'].mean(axis=1), color=colors[i], label=label)
    axes[0].axhline(1, color='#536168', ls='--', lw=1)
    axes[0].set(ylabel='T*', title=tr('模型切换后的 100τ：温度与链尺寸分别检查',
                                     '100τ after changing the model: temperature and chain size'))
    axes[1].set(ylabel=tr('80 条链的平均 Rg / σ', 'Mean Rg of 80 chains / σ'),
                xlabel=tr('时间 / τ', 'Time / τ'))
    for ax in axes:
        ax.axvspan(50, 100, color='#167d84', alpha=.06)
        ax.legend(frameon=False, fontsize=11)
    save(fig, 'melt-preparation')
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), layout='constrained')
    labels = [tr('直接相连', 'Directly bonded'), tr('同链其余珠对', 'Other same-chain pairs'),
              tr('不同链珠对', 'Different-chain pairs')]
    mean_g = np.mean([r['pair_g'] for r in results], axis=0)
    for j, label in enumerate(labels):
        axes[0].plot(results[0]['pair_r'], mean_g[j], label=label, color=colors[j])
    axes[0].plot(results[0]['pair_r'], mean_g.sum(axis=0), color='#163840', ls='--', label=tr('总和', 'Sum'))
    axes[0].set(xlim=(.7, 3.2), xlabel='r / σ', ylabel=tr('对 g(r) 的贡献', 'Contribution to g(r)'),
                title=tr('近邻既来自自身链，也来自周围链', 'Neighbors within and between chains'))
    axes[0].legend(frameon=False, fontsize=11)
    rg_edges = np.linspace(0, np.ceil(max(r['rg'].max() for r in results)*2)/2, 31)
    re_edges = np.linspace(0, np.ceil(max(r['re'].max() for r in results)*2)/2, 31)
    for i, r in enumerate(results):
        axes[1].plot(np.arange(1, 20), r['internal']/(np.arange(1, 20)*r['internal'][0]),
                     color=colors[i], label=tr(f'构型 {i+1}', f'Configuration {i+1}'))
    axes[1].axhline(1, ls='--', color='#536168', label=tr('独立等长步的参照', 'Independent-step reference'))
    axes[1].set(xlabel=tr('沿链相隔的键数 s', 'Separation along chain, s bonds'),
                ylabel='S(s) / [s S(1)]', xticks=[1, 5, 10, 15, 19],
                title=tr('内部距离：逐段查看链怎样展开', 'Internal distances across chain scales'))
    axes[1].legend(frameon=False, fontsize=11)
    save(fig, 'melt-structure')
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8), layout='constrained')
    for i, r in enumerate(results):
        label = tr(f'构型 {i+1}', f'Configuration {i+1}')
        axes[0].hist(r['rg'][r['late']].ravel(), bins=rg_edges,
                     density=True, histtype='step', lw=2, color=colors[i], label=label)
        axes[1].hist(r['re'][r['late']].ravel(), bins=re_edges,
                     density=True, histtype='step', lw=2, color=colors[i], label=label)
    for ax, name in zip(axes, ['Rg', 'Re']):
        ax.set(xlabel=f'{name} / σ', ylabel=tr('概率密度 / σ⁻¹', 'Probability density / σ⁻¹'))
        ax.legend(frameon=False, fontsize=11)
    axes[0].set_title(tr('50–100τ：回转半径的分布', '50–100τ: distribution of gyration radii'))
    axes[1].set_title(tr('50–100τ：末端距离的分布', '50–100τ: distribution of end distances'))
    save(fig, 'melt-dimensions')
    fig, ax = plt.subplots(figsize=(11, 5), layout='constrained')
    for i, r in enumerate(results):
        lag = np.arange(1, len(r['msd'])+1)*2.5
        label = tr(f'构型 {i+1}', f'Configuration {i+1}')
        ax.plot(lag, r['msd'][:, 0], color=colors[i], label=label+' '+tr('珠子', 'beads'))
        ax.plot(lag, r['msd'][:, 1], '--', color=colors[i], label=label+' '+tr('链质心', 'chain COM'))
    ax.set(xlabel=tr('时间间隔 Δt / τ', 'Lag time Δt / τ'),
           ylabel=tr('平均平方位移 / σ²', 'Mean squared displacement / σ²'),
           title=tr('50–100τ 窗口内的位移：珠子与整链', 'Displacement within 50–100τ: beads and whole chains'))
    ax.legend(frameon=False, ncols=2, fontsize=11)
    save(fig, 'melt-motion')
    summary = {'replica_count': len(results), 'replicas': [r['summary'] for r in results],
               'pair_normalization': '2 V times unordered pair counts / [frames N(N-1) shell volume]; all three pair classes share this denominator and add to total g(r).',
               'msd_definition': 'Unwrapped positions, whole-box translation removed; average over chains/beads and every available time origin in 50–100 tau, maximum lag25tau.'}
    (args.output/'melt_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf8')
    np.savetxt(args.output/'pair_structure.csv', np.c_[results[0]['pair_r'], mean_g.T], delimiter=',',
               header='r_sigma,bonded_contribution,same_chain_other_contribution,different_chain_contribution', comments='')
    print(json.dumps([r['summary'] for r in results], indent=2))


if __name__ == '__main__':
    main()
```

Pass one run folder for one configuration, or the parent containing n1600-rep1, n1600-rep2 and n1600-rep3 to retain three curves. Use --language zh for Chinese figures.

Consider what moving from a melt to a solution would involve. Adding explicit water requires compatible interaction, mass, and connectivity models for the polymer and water, including cross interactions between them. The earlier PEG/SPC/Fw example demonstrates that type of workflow. An implicit-solvent model instead places selected solvent effects into effective segment interactions, friction, and random forces, calibrated against relevant chain dimensions, osmotic properties, or dynamical measurements. Enlarging the present box alone produces a more dilute bead–spring system. It changes bead concentration without automatically introducing water’s hydrogen bonds, ionic screening, or the mechanisms by which a surrounding fluid transports momentum.

A useful material comparison begins by changing a clearly defined factor. For example, changing chain length while keeping total bead count and number density fixed requires a corresponding change in the number of chains. Increasing chain length at fixed chain count and box size also increases density, combining two effects. A solvent-quality comparison needs more than a fixed temperature: it must specify which segment–segment or segment–solvent interactions change. Comparisons between starting configurations instead retain the same preparation and observation protocol, exposing structural and sampling variation under the same conditions. Editing a single line in an input can therefore change more than one physical variable.

A useful extension keeps 20 beads per chain and the same interactions while comparing internal distances and interchain neighbours at several number densities. Rebuild the box for each density, follow the same preparation protocol, and extend observation until the structural quantities of interest are adequately characterized. That isolates crowding. A different question compares motion across chain lengths at fixed density, requiring observation times that grow with slow relaxation rather than an identical step count for every chain. A precise question makes it easier to decide which conditions to retain, which measurements to repeat, and where additional computation will be most informative.

The common starting point established here is a dense model material without explicit solvent and with fixed chain connectivity. It already answers where neighbours come from, how finite chain segments extend, and how local motion differs from whole-chain translation. The next lesson adds crosslinks while retaining the same beads, initial box, and segment interactions, changing the number and placement of permanent connections. The questions then become which chains form a common network, how connectivity changes relaxation, and how a stretched material’s response relates to network structure. Each step builds on a defined preceding level, turning a complex material problem into a sequence of measurable relationships.

## Further Reading and Open Materials

- [FENE bead–spring benchmark: bench/in.chain (30 Sep 2026 Update 1)](https://github.com/lammps/lammps/blob/develop/bench/in.chain) · LAMMPS developers · LAMMPS source repository: GPL-2.0. This lesson uses the interaction model with independently generated coordinates and preparation/analysis scripts.

  Open-source input basis for the FENE bead–spring melt, fixed to bench/in.chain in the official 30 Sep 2026 Update 1 archive.

  1600 beads in 80 chains of 20, ρ*=0.85; exact WCA cutoff and soft preparation; time step reduced from 0.012τ to 0.005τ and Langevin damping time changed from 10τ to 1τ; three initial configurations and structural analysis.
- [LAMMPS 30 Sep 2026 Update 1 source archive](https://download.lammps.org/tars/lammps-30Sep2026_update1.tar.gz) · LAMMPS developers · LAMMPS source software: GPL-2.0.

  Pinned source release used for this lesson; bench/in.chain defines the original bead–spring benchmark.

  Input adaptations and parameter changes are listed in the bead–spring benchmark entry.
- [Dynamics of entangled linear polymer melts: A molecular-dynamics simulation](https://doi.org/10.1063/1.458541) · Kurt Kremer and Gary S. Grest · Research citation; publisher copyright. Figures in this lesson are original conceptual illustrations.

  Historical connection between bead–spring models, chain length and dynamical constraints.

  Developed into a conceptual diagram of segment motion, chain displacement and neighbouring-chain constraints.
- [bond_style fene — LAMMPS documentation](https://docs.lammps.org/bond_fene.html) · LAMMPS developers · Official documentation cited for command definitions; no external illustration reproduced.

  Complete FENE potential, parameters and special-pair settings.

  Added symbol explanations, worked examples, diagrams and links to the executed input.
- [special_bonds — LAMMPS documentation](https://docs.lammps.org/special_bonds.html) · LAMMPS developers · Official documentation cited for command definitions; no external illustration reproduced.

  Weights for 1–2, 1–3 and 1–4 interactions.

  Added symbol explanations, worked examples, diagrams and links to the executed input.
- [pair_style soft — LAMMPS documentation](https://docs.lammps.org/pair_soft.html) · LAMMPS developers · Official documentation cited for command definitions; no external illustration reproduced.

  Prepare nearby particles with adjustable soft repulsion.

  Added symbol explanations, worked examples, diagrams and links to the executed input.
