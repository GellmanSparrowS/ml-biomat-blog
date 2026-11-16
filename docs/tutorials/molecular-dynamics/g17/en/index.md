# Visiting Rare Conformations: Umbrella Sampling and Free Energy

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g17/en/
Language: en

Place observation windows along a ten-residue peptide’s end distance and interpret bias, overlap, conformational history, and recorded free-energy profiles.

## Why does a molecule favor some shapes?

Fold a flexible ribbon and slowly separate its ends. At the same end-to-end distance, the ribbon can still have many different bends. A short peptide behaves similarly: nearby ends may accompany an organized fold or simply a chance return, while separating them can change backbone angles, side-chain contacts, and surrounding water. Researchers want to know which conformations occur frequently and which distances are difficult to visit between compact and extended arrangements. These questions connect protein folding, molecular recognition, and mechanical response. They take us from observing motion to explaining how conformations are distributed.

Previous trajectories allowed us to measure averages and fluctuations, but a molecule can remain near one family of conformations for a long time. Imagine a large room reached through a narrow doorway. Someone watching briefly from outside may see nobody enter, leaving the size and occupancy of the room uncertain. Sampling molecular conformations faces a similar problem: some regions are readily occupied, while connecting regions are visited rarely. A finite trajectory may therefore struggle to establish their relative probabilities. We need a way to distribute observation opportunities across chosen regions and recover the original statistical weights during analysis.

This lesson uses chignolin, a peptide with only ten amino acids, and performs umbrella sampling along the distance between the first and last residues' Cα atoms. A moving spring bias first generates starting conformations at different distances. Separate simulations then sample around fixed spring centers, and their biased records are combined into a free-energy profile. Each stage produces something interpretable: a pulling curve identifies the starting structures, window distributions reveal how neighboring records connect, and time-segment comparisons identify where longer sampling would be most informative.

Free energy combines interaction energy with the number of accessible conformations. If many molecular arrangements share a particular end distance, that distance can occur frequently even when no individual arrangement has exceptionally low potential energy. Potential energy belongs to a particular configuration; a free-energy profile collects the many configurations corresponding to the same coordinate value. For consistently defined equilibrium probability densities, the free-energy difference between two positions follows from the logarithm of their density ratio. Logarithms turn multiplicative probability ratios into additive energy differences and make large probability contrasts easier to compare.

Convert relative frequency into relative free energyEq. 1

![Convert relative frequency into relative free energy](https://ml-biomat.com/static/agent-math/8d8b418525882e0881b9b260.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| W(ξa), W(ξb) | Profile values at coordinate positions a and b | kJ/mol |
| ξa, ξb | Two end distances; a and b label positions | nm |
| p₀(ξ) | Unbiased equilibrium distance density; subscript 0 denotes removal of sampling bias | nm⁻¹ |
| R | Molar gas constant, 0.008314462618 | kJ mol⁻¹ K⁻¹ |
| T | Absolute temperature, 298 in this example | K |
| p₀(ξb)/p₀(ξa) | Density ratio; its units cancel before taking the logarithm | 1 |
| ln | Natural logarithm, with base e | 1 |
| =, −, /, ( ), [ ] | Equality, subtraction or negation, division, grouping; RT is a product | 1 |

Reading the relationshipEquilibrium probabilities decrease exponentially with free energy. A density ratio cancels normalization; its logarithm gives a difference.

A worked exampleAt 298 K, RT = 2.47771 kJ/mol. If b has one tenth the density at a, Wb − Wa = 5.70514 kJ/mol.

ConditionsApplies to the specified coordinate and a consistent density definition; distance-dependent conformational multiplicity is included.

Probability density means occurrence per unit distance. If a bin 0.01 nm wide contains five percent of the records, its density is 0.05 divided by 0.01, or 5 nm⁻¹. A density can exceed one because multiplying it by bin width gives the bin probability. When comparing two positions, their densities use the same units; taking the ratio cancels those units before applying a logarithm. This establishes a traceable route from counts to density and then to a free-energy difference, with units and statistical meanings attached to every step.

At 298 K, RT is approximately 2.478 kJ/mol, so a tenfold density ratio corresponds to about 5.705 kJ/mol in relative free energy. More probable positions have lower profile values, and the energy zero can be chosen for convenient comparison. This relation concerns the specified end-distance distribution, including the number of conformations associated with that coordinate. Its profile has a different meaning from the interaction potential of an isolated atom pair. Several internal shapes can share a distance, so interpreting a minimum also requires inspecting the molecular structures contributing to it.

## A ten-residue peptide connects several scientific questions

The umbrella-sampling idea is associated with Torrie and Valleau's 1977 work: deliberately choose a sampling distribution that visits relevant regions more effectively, then recover the desired information through statistical weighting. The bias allocates observation opportunities. In 1992, Kumar and colleagues developed the weighted histogram analysis method, WHAM, for biomolecular free-energy calculations, connecting multiple overlapping records. The two methods perform complementary tasks. One changes where a simulation spends its time; the other explains how records obtained with different sampling preferences can be combined.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g17/en/#en-s2)

Figure 1 · Umbrella sampling in 1977, WHAM in 1992, and chignolin in 2004 connect sampling methods, statistical combination, and a biomolecular question.

The molecular example arose from a different question: how short can an amino-acid sequence be while forming an organized fold? Honda and colleagues reported chignolin in 2004. Its ten-residue sequence, GYDPETGTWG, forms an experimentally characterized β-hairpin. The name describes a backbone that turns back to place two extended segments beside one another. Backbone interactions, side chains, and the aqueous environment contribute to that organization. This small system retains folding, backfolding, and internal-contact changes while allowing us to identify individual residues and define an end-distance coordinate clearly.

The structure entry 1UAO comes from solution nuclear magnetic resonance and contains 18 submitted conformers. We start from its first model. Those conformers form a structural ensemble from the experimental determination; their order carries no time sequence. The subsequent molecular-dynamics record provides the actual time evolution. In the figure, ten Cα positions outline the backbone, and a dashed segment marks the selected end distance. Other backbone atoms lie between neighboring Cα atoms, so the connecting lines guide the overall shape while the complete topology defines chemical bonds and angles.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g17/en/#en-s2)

Figure 2 · Cα positions from model 1 are shown in a principal-axis orthographic projection. Numbers are residue indices. Connecting lines trace the backbone, with other atoms between adjacent Cα sites; model order carries no time sequence.

Define end distance using two Cα atomsEq. 2

![Define end distance using two Cα atoms](https://ml-biomat.com/static/agent-math/f428f40e44da901dc2e5d976.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ξ | End distance, a nonnegative length | nm |
| r₁, r₁₀ | Cα position vectors of Gly1 and Gly10; subscripts are residue numbers | nm |
| Δr; Δx, Δy, Δz | Minimum-image displacement and its three orthogonal components | nm |
| ‖Δr‖ | Displacement-vector norm | nm |
| √ | Square-root operation, converting nm² to nm here | 1 |
| (Δx)², (Δy)², (Δz)² | Squared components; exponent 2 means multiplication by itself | nm² |
| min.image | Choose the unambiguous nearest displacement among periodic images | 1 |
| =, +, −, ( ) | Equality, addition, subtraction, and grouping | 1 |

Reading the relationshipOrthogonal components obey the Pythagorean relation. Correct the displacement for periodicity before computing its length. A one-atom group has its center of mass at that atom.

A worked exampleA minimum-image displacement of (0.3, 0.4, 0) nm gives distance 0.5 nm.

ConditionsCheck actual box dimensions for compatibility with the nearest-image definition. This scalar retains end-distance information.

Choosing a reaction coordinate also chooses how to compress information. A complete configuration contains coordinates for tens of thousands of atoms, while end distance retains one number. If shapes sharing that distance exchange sufficiently during observation, collecting their records describes the statistics of that coordinate. A persistent side-chain arrangement may instead evolve slowly while distance fluctuates repeatedly. Each window therefore saves structural trajectories as well as distance and bias force. A particular part of a histogram can then be connected back to the molecular shapes that contributed to it, allowing the coordinate-based explanation to be developed with additional structural evidence.

Water contributes to the relative probabilities of different end distances. As the peptide extends, parts previously contacting one another can contact water, changing solvent orientations and arrangements. The statistical description therefore includes configurations of the entire solvated system at a specified peptide distance. Subtracting peptide internal energies from two snapshots would omit solvent reorganization and the multiplicity of accessible configurations. Explicitly simulating water and organizing the resulting ensemble by peptide end distance provides one route to include those environmental contributions in the free-energy description.

The model uses CHARMM36m protein parameters and the CHARMM TIP3P water definition in that parameter package. Its N terminus is positive, its C terminus negative, and the Asp3 and Glu5 side chains each carry one negative charge. The peptide therefore has net charge −2 and is neutralized by two sodium ions. The final system contains 138 peptide atoms, 9,276 water molecules, and two ions: 27,968 atoms altogether. pdb2gmx rebuilds the deposited hydrogen positions according to the selected force field. CHARMM's water hydrogens also have defined Lennard–Jones parameters, making the precise water parameter file part of the model.

The initial periodic box is a 6.6 nm cube, providing space for distances approaching 3 nm. End distance uses the three-dimensional minimum-image convention, so the actual box dimensions and sampled separations must preserve an unambiguous nearest-image relationship. Each pulling group contains one Cα atom, from Gly1 or Gly10; its group center of mass is consequently that atom's position. This coordinate measures backbone end separation. Distinguishing different folds at similar end distances would require additional structural quantities, such as backbone hydrogen bonds, side-chain contacts, or internal angles.

## How a virtual spring changes sampling

An umbrella window behaves like a spring encouraging observation near a chosen distance. All ordinary molecular interactions remain active, and an additional energy rises as the end distance departs from the center. Larger deviations generate stronger restoring forces. The center selects the region to examine, while the spring constant controls confinement. The spring acts on a distance defined by selected atoms. GROMACS differentiates that distance-dependent energy and distributes the corresponding forces to the endpoints; the rest of the molecule responds through its existing interactions.

Bias energy, restoring force, and a moving centerEq. 3

![Bias energy, restoring force, and a moving center](https://ml-biomat.com/static/agent-math/137bedfae3ecbb0efbaf3777.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| i | Window index | 1 |
| Uᵢ | Harmonic bias energy in that window | kJ/mol |
| ξ, ξᵢ, ξᵢ(0) | Observed end distance, current center, and initial center | nm |
| kᵢ | Spring constant; 1000 in fixed windows and 2000 during pulling | kJ mol⁻¹ nm⁻² |
| Fᵢ | Bias force defined toward increasing distance; negative values reduce distance | kJ mol⁻¹ nm⁻¹ |
| v, t | Center speed and elapsed time | nm/ps; ps |
| (ξ−ξᵢ)² | Squared displacement | nm² |
| 1/2, ² | Numerical factor and square exponent | 1 |
| =, −, +, ( ) | Equality, negation or subtraction, addition, grouping; adjacent quantities multiply | 1 |

Reading the relationshipForce magnitude grows linearly from zero, so work done against the restoring force is the triangular area under its magnitude–displacement curve, giving the factor 1/2. Force is the negative energy derivative and points toward the center.

A worked exampleFor k = 1000 and displacement 0.05 nm, U = 1.25 kJ/mol and F = −50 kJ mol⁻¹ nm⁻¹. At v = 0.005 nm/ps, the center advances 0.5 nm in 100 ps.

ConditionsFixed windows have v = 0 while retaining restoring force. A moving bias generates conformations; window statistics supply the subsequent equilibrium reweighting.

The fixed-window spring constant is 1,000 kJ mol⁻¹ nm⁻². A deviation of 0.05 nm gives bias energy 1.25 kJ/mol and restoring-force magnitude 50 kJ mol⁻¹ nm⁻¹. Doubling the deviation doubles the force and quadruples the energy. The force sign identifies whether it acts toward increasing or decreasing distance. Below the center, the bias tends to separate the ends; above it, the bias tends to bring them together. Reading a force output therefore requires both the sign convention and the coordinate definition.

Moving and fixed springs use the same energy form, with different center histories. During starting-structure generation, the center begins at the initial distance and increases by 0.005 nm per picosecond, with spring constant 2,000. This external drive progressively extends the peptide. In production windows, the centers are specified explicitly as 0.5, 0.6, and subsequent distances, the center speed is zero, and the spring constant is 1,000. Zero speed fixes the center while retaining the instantaneous restoring force. A window's mean distance can differ from its center because molecular conformational preferences also shape the sampled distribution.

A thermal estimate helps interpret spring stiffness. If the underlying free-energy profile is approximately flat over a small distance region, a harmonic bias produces a distribution whose standard deviation is the square root of the ratio RT/k. At 298 K with the present fixed-window constant, this is about 0.0498 nm. A stronger spring narrows that reference distribution, potentially reducing overlap between neighboring windows. The peptide's own free-energy landscape can shift, broaden, or distort its actual distribution, so the recorded histograms remain essential.

A thermal-width reference for the springEq. 4

![A thermal-width reference for the spring](https://ml-biomat.com/static/agent-math/251c05489e28f289a6b3d3a7.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ξ, ξᵢ | Current end distance and spring center | nm |
| σξ | Reference standard deviation of distance under a harmonic bias | nm |
| R, T | Molar gas constant and absolute temperature | kJ mol⁻¹ K⁻¹; K |
| k | Spring constant | kJ mol⁻¹ nm⁻² |
| RT/k | Thermal energy divided by stiffness, with dimensions of length squared | nm² |
| √, ≃, / | Square root, approximate equality, division; RT is a product | 1 |

Reading the relationshipFor a locally flat underlying profile, the weight exp[−k(ξ−ξi)²/(2RT)] has the Gaussian form.

A worked exampleAt 298 K and k = 1000, σξ is approximately 0.04978 nm. Quadrupling stiffness halves the reference width.

ConditionsThe molecular free-energy slope and curvature change the mean and width; recorded histograms establish actual coverage.

The force unit can also connect to molecular mechanics experiments. One kJ mol⁻¹ nm⁻¹ is approximately 1.66054 pN, so a magnitude of 50 in those simulation units corresponds to about 83.0 pN. This conversion expresses the molar-energy convention as a force on an individual molecule. Actual end distance still responds to the peptide and water environment together. During moving-spring pulling, the measured force depends on speed and conformational history. Studying a near-reversible response would require a separate design around pulling speed, relaxation, and repeated histories.

[Figure: Harmonic bias energy and thermal-width reference](https://ml-biomat.com/tutorials/molecular-dynamics/g17/en/#en-s3)

Left: harmonic bias energy. Right: peak-normalized probability reference for a locally flat underlying profile. Black points mark the current displacement; width follows the specified temperature and stiffness.

The interaction displays harmonic bias energy, restoring force, and the reference width for a locally flat underlying profile. At zero deviation, both bias energy and force vanish. Reversing the deviation preserves energy and reverses force. Increasing stiffness raises the force at the same displacement and narrows the thermal reference width. These relations provide a physical starting point for window placement. They also explain why equally spaced input centers need not produce evenly distributed observations: the molecule's underlying conformational landscape participates in determining where the simulation spends time.

## Generate twenty-six observation windows

We first prepare the solvated peptide at the target conditions using 100 ps of restrained NVT and 100 ps of restrained NPT, at 298 K and 1 bar. Position restraints are then removed for the 500 ps moving-spring stage. Covalent bonds involving hydrogen are constrained, the integration step is 2 fs, electrostatics uses PME, and Lennard–Jones forces are switched between 1.0 and 1.2 nm. The full input generator below exposes the temperature, pressure, output intervals, and pulling settings together, allowing the protocol to be read directly from its complete parameter definitions.

### Download and verify the specified parameter archive

```
"""Download the specified official CHARMM GROMACS parameter archive."""
from pathlib import Path
import argparse,hashlib,tarfile,urllib.request

URL='https://mackerell.umaryland.edu/download.php?filename=CHARMM_ff_params_files%2Fcharmm36-jul2022.ff.tgz'
SHA256='9f31db8502852bc8fcf36497c27db14f1b6509b33701e7cafc2187840b7d2f09'

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=Path('.'))
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    archive=args.out/'charmm36-jul2022.ff.tgz'
    if not archive.exists():
        request=urllib.request.Request(URL,headers={'User-Agent':'MD-course-parameter-download'})
        with urllib.request.urlopen(request,timeout=120) as response:
            archive.write_bytes(response.read())
    actual=hashlib.sha256(archive.read_bytes()).hexdigest()
    if actual!=SHA256:raise ValueError('The archive differs from the specified parameter release')
    with tarfile.open(archive) as handle:
        handle.extractall(args.out,filter='data')
    if not (args.out/'charmm36-jul2022.ff/forcefield.itp').is_file():
        raise ValueError('Expected GROMACS force-field directory missing')
    print('Official CHARMM July 2022 GROMACS parameter archive verified and extracted')
```

Download from the parameter maintainer, verify the archive hash, and extract.

### Build endpoint groups by atom identity

```
from pathlib import Path
s=Path('ions.gro').read_text().splitlines();n=int(s[1]);groups={}
for i,line in enumerate(s[2:2+n],1):
    resid=int(line[:5]);resname=line[5:10].strip();name=line[10:15].strip()
    if resid in (1,10) and name=='CA':
        assert resname=='GLY'
        groups[f'Gly{resid}_CA']=i
assert groups=={'Gly1_CA':5,'Gly10_CA':133}
all_atoms='\n'.join(' '.join(str(i) for i in range(start,min(start+15,n+1))) for start in range(1,n+1,15))
Path('index.ndx').write_text('[ System ]\n'+all_atoms+'\n'+''.join(f'[ {k} ]\n{v}\n' for k,v in groups.items()))
```

Check Gly1, Gly10, and their Cα identities before writing index groups.

### Generate all preparation, pulling, and sampling parameters

```
"""Write complete inputs for chignolin pulling, 26 umbrellas, and two bridge trials."""
from pathlib import Path
import argparse

BASE = {
'ions.mdp': """integrator = steep
emtol = 1000.0
emstep = 0.01
nsteps = 50000
nstlist = 1
cutoff-scheme = Verlet
coulombtype = cutoff
rcoulomb = 1.2
rvdw = 1.2
pbc = xyz
""",
'em.mdp': """integrator = steep
emtol = 250
emstep = 0.001
nsteps = 10000
nstlist = 1
cutoff-scheme = Verlet
coulombtype = PME
rcoulomb = 1.2
vdw-modifier = force-switch
rvdw-switch = 1.0
rvdw = 1.2
rlist = 1.4
pbc = xyz
define = -DFLEXIBLE
constraints = none
""",
'nvt.mdp': """define = -DPOSRES
integrator = md
nsteps = 50000
dt = 0.002
nstxout = 0
nstvout = 0
nstenergy = 100
nstlog = 1000
continuation = no
constraint-algorithm = lincs
constraints = h-bonds
lincs-iter = 1
lincs-order = 4
cutoff-scheme = Verlet
vdwtype = cutoff
vdw-modifier = force-switch
nstlist = 10
rvdw-switch = 1.0
rvdw = 1.2
rlist = 1.4
dispcorr = no
coulombtype = PME
rcoulomb = 1.2
pme-order = 4
fourierspacing = 0.16
tcoupl = V-rescale
tc-grps = System
tau-t = 1.0
ref-t = 298
pcoupl = no
pbc = xyz
gen-vel = yes
gen-temp = 298
gen-seed = 20261700
nstfout = 0
nstxout-compressed = 500
ld-seed = 20261701
""",
'npt.mdp': """define = -DPOSRES
integrator = md
nsteps = 50000
dt = 0.002
nstxout = 0
nstvout = 0
nstenergy = 100
nstlog = 1000
continuation = yes
constraint-algorithm = lincs
constraints = h-bonds
lincs-iter = 1
lincs-order = 4
cutoff-scheme = Verlet
vdwtype = cutoff
vdw-modifier = force-switch
nstlist = 10
rvdw-switch = 1.0
rvdw = 1.2
rlist = 1.4
dispcorr = no
coulombtype = PME
rcoulomb = 1.2
pme-order = 4
fourierspacing = 0.16
tcoupl = V-rescale
tc-grps = System
tau-t = 1.0
ref-t = 298
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
refcoord-scaling = com
pbc = xyz
gen-vel = no
nstfout = 0
nstxout-compressed = 500
ld-seed = 20261702
""",
'pull.mdp': """integrator = md
nsteps = 250000
dt = 0.002
nstxout = 0
nstvout = 0
nstenergy = 100
nstlog = 1000
nstxout-compressed = 500
continuation = yes
constraint-algorithm = lincs
constraints = h-bonds
lincs-iter = 1
lincs-order = 4
cutoff-scheme = Verlet
vdwtype = cutoff
vdw-modifier = force-switch
nstlist = 10
rvdw-switch = 1.0
rvdw = 1.2
rlist = 1.4
dispcorr = no
coulombtype = PME
rcoulomb = 1.2
pme-order = 4
fourierspacing = 0.16
tcoupl = V-rescale
tc-grps = System
tau-t = 1.0
ref-t = 298
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
pbc = xyz
gen-vel = no
pull = yes
pull-ngroups = 2
pull-ncoords = 1
pull-group1-name = Gly1_CA
pull-group2-name = Gly10_CA
pull-coord1-type = umbrella
pull-coord1-geometry = distance
pull-coord1-dim = Y Y Y
pull-coord1-groups = 1 2
pull-coord1-start = yes
pull-coord1-rate = 0.005
pull-coord1-k = 2000
nstfout = 0
ld-seed = 20261703
pull-nstxout = 500
pull-nstfout = 500
""",
}


UMBRELLA = """integrator = md
nsteps = 50000
dt = 0.002
nstxout = 0
nstvout = 0
nstenergy = 100
nstlog = 1000
nstxout-compressed = 500
continuation = yes
constraint-algorithm = lincs
constraints = h-bonds
lincs-iter = 1
lincs-order = 4
cutoff-scheme = Verlet
vdwtype = cutoff
vdw-modifier = force-switch
nstlist = 10
rvdw-switch = 1.0
rvdw = 1.2
rlist = 1.4
dispcorr = no
coulombtype = PME
rcoulomb = 1.2
pme-order = 4
fourierspacing = 0.16
tcoupl = V-rescale
tc-grps = System
tau-t = 1.0
ref-t = 298
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
pbc = xyz
gen-vel = no
pull = yes
pull-ngroups = 2
pull-ncoords = 1
pull-group1-name = Gly1_CA
pull-group2-name = Gly10_CA
pull-coord1-type = umbrella
pull-coord1-geometry = distance
pull-coord1-dim = Y Y Y
pull-coord1-groups = 1 2
pull-coord1-start = no
pull-coord1-init = 0.5
pull-coord1-rate = 0.0
pull-coord1-k = 1000
nstfout = 0
ld-seed = 20261900
pull-nstxout = 50
pull-nstfout = 50
"""

EQUILIBRATION = """integrator = md
nsteps = 10000
dt = 0.002
nstxout = 0
nstvout = 0
nstenergy = 100
nstlog = 1000
nstxout-compressed = 500
continuation = no
constraint-algorithm = lincs
constraints = h-bonds
lincs-iter = 1
lincs-order = 4
cutoff-scheme = Verlet
vdwtype = cutoff
vdw-modifier = force-switch
nstlist = 10
rvdw-switch = 1.0
rvdw = 1.2
rlist = 1.4
dispcorr = no
coulombtype = PME
rcoulomb = 1.2
pme-order = 4
fourierspacing = 0.16
tcoupl = V-rescale
tc-grps = System
tau-t = 1.0
ref-t = 298
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
pbc = xyz
gen-vel = yes
pull = yes
pull-ngroups = 2
pull-ncoords = 1
pull-group1-name = Gly1_CA
pull-group2-name = Gly10_CA
pull-coord1-type = umbrella
pull-coord1-geometry = distance
pull-coord1-dim = Y Y Y
pull-coord1-groups = 1 2
pull-coord1-start = no
pull-coord1-init = 0.5
pull-coord1-rate = 0.0
pull-coord1-k = 1000
nstfout = 0
ld-seed = 20261850
pull-nstxout = 50
pull-nstfout = 50
gen-temp = 298
gen-seed = 20261800
"""

BRIDGE_EQ = """integrator = md
nsteps = 50000
dt = 0.002
nstxout = 0
nstvout = 0
nstenergy = 100
nstlog = 1000
nstxout-compressed = 2500
continuation = no
constraint-algorithm = lincs
constraints = h-bonds
lincs-iter = 1
lincs-order = 4
cutoff-scheme = Verlet
vdwtype = cutoff
vdw-modifier = force-switch
nstlist = 10
rvdw-switch = 1.0
rvdw = 1.2
rlist = 1.4
dispcorr = no
coulombtype = PME
rcoulomb = 1.2
pme-order = 4
fourierspacing = 0.16
tcoupl = V-rescale
tc-grps = System
tau-t = 1.0
ref-t = 298
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
pbc = xyz
gen-vel = yes
pull = yes
pull-ngroups = 2
pull-ncoords = 1
pull-group1-name = Gly1_CA
pull-group2-name = Gly10_CA
pull-coord1-type = umbrella
pull-coord1-geometry = distance
pull-coord1-dim = Y Y Y
pull-coord1-groups = 1 2
pull-coord1-start = no
pull-coord1-init = 0.65
pull-coord1-rate = 0.0
pull-coord1-k = 1000
nstfout = 0
ld-seed = 20267101
pull-nstxout = 50
pull-nstfout = 50
gen-temp = 298
gen-seed = 20267301
"""

BRIDGE_US = """integrator = md
nsteps = 250000
dt = 0.002
nstxout = 0
nstvout = 0
nstenergy = 100
nstlog = 1000
nstxout-compressed = 2500
continuation = yes
constraint-algorithm = lincs
constraints = h-bonds
lincs-iter = 1
lincs-order = 4
cutoff-scheme = Verlet
vdwtype = cutoff
vdw-modifier = force-switch
nstlist = 10
rvdw-switch = 1.0
rvdw = 1.2
rlist = 1.4
dispcorr = no
coulombtype = PME
rcoulomb = 1.2
pme-order = 4
fourierspacing = 0.16
tcoupl = V-rescale
tc-grps = System
tau-t = 1.0
ref-t = 298
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
pbc = xyz
gen-vel = no
pull = yes
pull-ngroups = 2
pull-ncoords = 1
pull-group1-name = Gly1_CA
pull-group2-name = Gly10_CA
pull-coord1-type = umbrella
pull-coord1-geometry = distance
pull-coord1-dim = Y Y Y
pull-coord1-groups = 1 2
pull-coord1-start = no
pull-coord1-init = 0.65
pull-coord1-rate = 0.0
pull-coord1-k = 1000
nstfout = 0
ld-seed = 20267201
pull-nstxout = 50
pull-nstfout = 50
"""

def replace_values(template, updates):
    rows=[]
    for line in template.splitlines():
        if '=' in line:
            key=line.split('=',1)[0].strip()
            if key in updates:line=f'{key} = {updates[key]}'
        rows.append(line)
    return '\n'.join(rows)+'\n'

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=Path('.'));a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    for name,content in BASE.items():(a.out/name).write_text(content,encoding='utf8',newline='\n')
    for i in range(26):
        center=round(.5+.1*i,1)
        us=replace_values(UMBRELLA,{'pull-coord1-init':center,'ld-seed':20261900+i})
        eq=replace_values(EQUILIBRATION,{'pull-coord1-init':center,'gen-seed':20261800+i,'ld-seed':20261850+i})
        (a.out/f'us{i}.mdp').write_text(us,encoding='utf8',newline='\n');(a.out/f'eq{i}.mdp').write_text(eq,encoding='utf8',newline='\n')
    for letter,delta in [('a',0),('b',1)]:
        d=a.out/f'bridge-{letter}';d.mkdir(exist_ok=True)
        eq=replace_values(BRIDGE_EQ,{'gen-seed':20267301+delta,'ld-seed':20267101+delta})
        us=replace_values(BRIDGE_US,{'ld-seed':20267201+delta})
        (d/'eq.mdp').write_text(eq,encoding='utf8',newline='\n');(d/'us.mdp').write_text(us,encoding='utf8',newline='\n')

if __name__=='__main__':main()
```

Define complete templates and window-specific seeds for all 61 MDP files.

### Complete entry from structure to bilingual figures

```
#!/usr/bin/env bash
set -euo pipefail
py=${PYTHON:-python3}
root=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$root/work/original"
for name in chignolin.pdb build_index.py select_windows.py run.sh; do
  cp "$root/$name" "$root/work/original/$name"
done
(cd "$root/work/original" && "$py" "$root/fetch_forcefield.py")
"$py" "$root/write_parameters.py" --out "$root/work/original"
(cd "$root/work/original" && bash run.sh)
"$py" "$root/prepare_bridges.py" --original "$root/work/original" --out "$root/work"
for letter in a b; do
  (cd "$root/work/bridge-$letter" && bash run.sh)
done
"$py" "$root/run_wham.py" --original "$root/work/original" --bridge-a "$root/work/bridge-a" --bridge-b "$root/work/bridge-b" --out "$root/work/wham"
for language in zh en; do
  "$py" "$root/analyze_umbrella.py" --original "$root/work/original" --bridge-a "$root/work/bridge-a" --bridge-b "$root/work/bridge-b" --wham "$root/work/wham" --out "$root/work/results-$language" --language "$language"
done
```

Run bash start.sh in the configured GROMACS and analysis environment. It runs 26 windows, two bridge trials, six WHAM analyses, and both plotting languages in sequence.

The generator writes common preparation, pulling, 26 window preparations and productions, and the two later bridge trials. Fixed windows use pull-coord1-start=no, so the init field specifies the spring center directly. Moving-spring pulling uses the starting separation as its initial center. A selected structure might have distance 0.598 nm while its window center is exactly 0.600 nm. Separating the coordinate value from the center gives each window a clear target and lets WHAM read the correct bias definition from its TPR.

### Run the original 26-window workflow

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
py=${PYTHON:-python3}
"$gmx" pdb2gmx -f chignolin.pdb -o processed.gro -p topol.top -ff charmm36-jul2022 -water tip3p -ignh > pdb2gmx.log 2>&1
"$gmx" editconf -f processed.gro -o boxed.gro -box 6.6 6.6 6.6 -c > box.log 2>&1
"$gmx" solvate -cp boxed.gro -cs spc216.gro -p topol.top -o solvated.gro > solvate.log 2>&1
"$gmx" grompp -f ions.mdp -c solvated.gro -p topol.top -o ions.tpr > ions.grompp.log 2>&1
printf 'SOL\n' | "$gmx" genion -s ions.tpr -o ions.gro -p topol.top -pname SOD -nname CLA -neutral -seed 20261700 > genion.log 2>&1
"$py" build_index.py
"$gmx" grompp -f em.mdp -c ions.gro -p topol.top -o em.tpr > em.grompp.log 2>&1
"$gmx" mdrun -deffnm em -ntmpi 1 -ntomp 2 -pin off > em.stdout.log 2>&1
"$gmx" grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr > nvt.grompp.log 2>&1
"$gmx" mdrun -deffnm nvt -ntmpi 1 -ntomp 2 -pin off > nvt.stdout.log 2>&1
"$gmx" grompp -f npt.mdp -c nvt.gro -t nvt.cpt -r em.gro -p topol.top -o npt.tpr > npt.grompp.log 2>&1
"$gmx" mdrun -deffnm npt -ntmpi 1 -ntomp 2 -pin off > npt.stdout.log 2>&1
"$gmx" grompp -f pull.mdp -c npt.gro -t npt.cpt -p topol.top -n index.ndx -o pull.tpr > pull.grompp.log 2>&1
"$gmx" mdrun -deffnm pull -ntmpi 1 -ntomp 2 -pin off > pull.stdout.log 2>&1
"$py" select_windows.py
for i in $(seq 0 25); do
  win=$(printf '%02d' "$i")
  "$gmx" grompp -f "eq$i.mdp" -c "window-$win.gro" -p topol.top -n index.ndx -o "eq$i.tpr" > "eq$i.grompp.log" 2>&1
  "$gmx" mdrun -deffnm "eq$i" -ntmpi 1 -ntomp 2 -pin off > "eq$i.stdout.log" 2>&1
  "$gmx" grompp -f "us$i.mdp" -c "eq$i.gro" -t "eq$i.cpt" -p topol.top -n index.ndx -o "us$i.tpr" > "us$i.grompp.log" 2>&1
  "$gmx" mdrun -deffnm "us$i" -ntmpi 1 -ntomp 2 -pin off > "us$i.stdout.log" 2>&1
done
for i in $(seq 0 25); do printf 'us%s.tpr\n' "$i"; done > tpr-files.dat
for i in $(seq 0 25); do printf 'us%s_pullf.xvg\n' "$i"; done > pullf-files.dat
"$gmx" wham -it tpr-files.dat -if pullf-files.dat -o pmf.xvg -hist histograms.xvg -temp 298 -b 0 -bins 150 > wham.log 2>&1
```

Run minimization, NVT, NPT, pulling, frame selection, and window preparation and production in sequence.

The driven distance generally increases but fluctuates and can lag behind the moving center. For every desired window center, we locate the saved frame with the closest observed distance and extract the full-system coordinates. This resembles selecting candidate starting frames from a continuous stretching sequence. A matching distance identifies a starting structure; each window subsequently undergoes its own preparation. Points on the pulling plot identify those selected frames, while the dashed line shows the moving center. Their separation reveals the response of the peptide to a spring with finite stiffness.

### Pulling records and starting frames

Actual distance, moving center, and 26 selected frames from 500 ps of pulling.

Ten-residue chignolin with CHARMM36 July 2022 and TIP3P water, at 298 K and 1 bar with a 2 fs timestep. The original 26 windows span centers of 0.5–3.0 nm in 0.1 nm increments, each with 100 ps production. Two 0.65 nm bridges start from the final 0.60 and 0.70 nm states and each have 500 ps production. The fixed-window spring constant is 1000 kJ mol⁻¹ nm⁻².

[Download reference data and complete inputs (ZIP) 19.37 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-chignolin-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g17/en/#en-s4)

Actual pulling distance, the bias center moving at 0.005 nm/ps, and native starting frames selected for 26 fixed windows. Pulling generates the conformations; records at fixed centers support the later statistics.

### Select starting frames from the recorded pulling series

```
from pathlib import Path
import json,os,subprocess
import numpy as np
rows=np.loadtxt([s for s in Path('pull_pullx.xvg').read_text().splitlines() if s and s[0] not in '#@'])
assert rows.shape[1]==2 and np.isfinite(rows).all()
gmx=os.environ.get('GMX','gmx');report=[]
for i in range(26):
    center=.5+.1*i;j=int(np.argmin(abs(rows[:,1]-center)));t=float(rows[j,0]);actual=float(rows[j,1])
    assert abs(actual-center)<.08,(center,actual)
    with open(f'window-{i:02d}-extract.log','w') as log:
        subprocess.run([gmx,'trjconv','-s','pull.tpr','-f','pull.xtc','-dump',str(t),'-o',f'window-{i:02d}.gro'],input='System\n',text=True,stdout=log,stderr=subprocess.STDOUT,check=True)
    report.append(dict(index=i,center_nm=center,selected_time_ps=t,saved_distance_nm=actual))
Path('window-selection.json').write_text(json.dumps(report,indent=2))
```

Find the nearest saved distance to each center and extract full coordinates.

Each fixed window generates new velocities, prepares for 20 ps under its own bias, and records 100 ps. The 26 centers span 0.5–3.0 nm in 0.1 nm increments. Distance and bias force are saved every 0.1 ps, giving 1,001 values per window. Structure frames are saved separately at 1 ps intervals. During the moving-spring stage, distance output used for frame selection matches the saved structure times. Distinguishing integration steps, coordinate-storage intervals, and scalar-output intervals establishes what each row in a time series represents.

The run script combines topology, index groups, and MDP settings into TPR files and executes the stages. The endpoint atoms are Gly1 Cα and Gly10 Cα, numbered 5 and 133 in the current topology. The index program finds their identities from residue and atom names before writing the groups. The force-field download is checked against the specified archive hash. For statistical interpretation, neighboring observations among the 1,001 saved values are generally correlated. Row count measures saved observations, while temporal correlation and independent simulations determine how much independent statistical information they provide.

## Do neighboring windows observe common regions?

A sequence of window centers does not automatically form a connected body of sampling data. We place every window's distances into the same 0.01 nm bins, calculate the fraction of records in each bin, and inspect the distributions together. Each heatmap row corresponds to a spring center, with bright regions marking frequently visited actual distances. The dashed line identifies equality between distance and center. Many distributions lie to one side of it, revealing the effect of molecular preferences. Connectivity is assessed from those observed distributions rather than from the input center list alone.

### Original windows and the bridge region

Shared 0.01 nm bins; each distribution normalizes by its own record count.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g17/en/#en-s5)

Left: measured distance distributions of the original 26 windows, normalized separately. The dashed line marks prescribed centers and circles mark observed means. Right: the original 0.60 and 0.70 nm windows and both 0.65 nm bridges, on common 0.01 nm bins.

The 0.6 nm window has mean distance about 0.5181 nm, while the 0.7 nm window has mean about 0.6509 nm. Their distributions connect weakly. Summing the smaller probability from each pair of matching bins measures shared coverage: identical distributions give one, and distributions without common occupied bins give zero. For these two windows, the coefficient is 0.04296. At the stated bin width, this directly identifies limited common coverage and gives a specific location for additional computation.

Quantify shared coverage between windowsEq. 5

![Quantify shared coverage between windows](https://ml-biomat.com/static/agent-math/0e466cca6e003d8ce6aede08.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| i, j, b | Two window indices and a common bin index | 1 |
| Hᵢb, nᵢ | Count in bin b and total count for window i | count |
| Pᵢb, Pⱼb | Probabilities of the same bin in the two windows | 1 |
| Oᵢⱼ | Overlap coefficient, between zero and one | 1 |
| Σb, min | Sum over bins; take the smaller of the two probabilities in each bin | 1 |
| =, /, ( ), , | Equality, division, grouping; comma separates function arguments | 1 |

Reading the relationshipThe smaller bin probability is shared by both distributions. Summing gives their common probability mass.

A worked exampleFor bin probabilities (0.7, 0.3) and (0.2, 0.8), overlap is 0.2 + 0.3 = 0.5.

ConditionsAll distributions use shared 0.01 nm bins covering every observation. This measures overlap projected onto end distance.

The overlap coefficient depends on binning and available sampling, so comparisons retain a common grid and definition. Very fine bins make short records look fragmented; very coarse bins can merge regions that are actually separated. Our 0.01 nm bins are smaller than the roughly 0.05 nm harmonic reference width, resolving details of this connection. The result measures coverage projected onto end distance. Similar distances can still contain different internal angles or side-chain contacts, motivating structural inspection and records from different starting configurations.

The original windows show why one spring constant and spacing can work smoothly in some regions while requiring denser observation elsewhere. Local free-energy slopes, conformational transitions, and slow internal variables can all contribute. Possible responses include adding an intermediate center, changing stiffness, or extending relevant records. Here we add a center at 0.65 nm and start it separately from the two neighboring configurations. This examines both the distance gap and the persistence of preparation history.

WHAM later reweights each window using its known bias, and overlapping regions connect their relative normalizations. An analogy is joining photographs that share part of a scene: common content helps establish how they fit, while little shared content makes the connection sensitive to local noise. In the calculation, known spring energies additionally correct for the different preferences imposed on each distance. Counts, bias definitions, and overlap together provide the basis for combining the records.

## One center, two starting conformations

Bridge A starts from the final state of the original 0.6 nm window; bridge B starts from the 0.7 nm window's final state. Both use center 0.65 nm and spring constant 1,000. Each generates new velocities, prepares under that bias for 100 ps, and records 500 ps. This increases observation in the intermediate region while retaining the identities of the two starting histories. The preparation script copies the original topology, index, and appropriate coordinates into separate directories and writes the corresponding seeds and settings. Each trial can run separately and later be combined under its explicit label.

### Prepare bridge trials from two starting histories

```
"""Prepare the two 0.65 nm windows from the 0.6 and 0.7 nm final states."""
from pathlib import Path
import argparse,shutil
from write_parameters import BRIDGE_EQ,BRIDGE_US,replace_values

RUN='''#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
"$gmx" grompp -f eq.mdp -c start.gro -p topol.top -n index.ndx -o eq.tpr > eq.grompp.log 2>&1
"$gmx" mdrun -deffnm eq -ntmpi 1 -ntomp 2 -pin off > eq.stdout.log 2>&1
"$gmx" grompp -f us.mdp -c eq.gro -t eq.cpt -p topol.top -n index.ndx -o us.tpr > us.grompp.log 2>&1
"$gmx" mdrun -deffnm us -ntmpi 1 -ntomp 2 -pin off > us.stdout.log 2>&1
'''

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original',type=Path,default=Path('original'))
    parser.add_argument('--out',type=Path,default=Path('.'))
    args=parser.parse_args()
    for letter,index,delta in [('a',1,0),('b',2,1)]:
        folder=args.out/f'bridge-{letter}';folder.mkdir(parents=True,exist_ok=True)
        for name in ['topol.top','posre.itp','index.ndx']:
            shutil.copy2(args.original/name,folder/name)
        shutil.copytree(args.original/'charmm36-jul2022.ff',folder/'charmm36-jul2022.ff',dirs_exist_ok=True)
        shutil.copy2(args.original/f'us{index}.gro',folder/'start.gro')
        eq=replace_values(BRIDGE_EQ,{'gen-seed':20267301+delta,'ld-seed':20267101+delta})
        us=replace_values(BRIDGE_US,{'ld-seed':20267201+delta})
        (folder/'eq.mdp').write_text(eq,encoding='utf8',newline='\n')
        (folder/'us.mdp').write_text(us,encoding='utf8',newline='\n')
        (folder/'run.sh').write_text(RUN,encoding='utf8',newline='\n')
    print('Run bash run.sh separately inside bridge-a and bridge-b')
```

Build 0.65 nm biased trials from the final states of the 0.6 and 0.7 nm windows.

Each bridge supplies 5,001 distance records. A has mean distance about 0.55005 nm and B about 0.58478 nm, despite sharing exactly the same center. Their time series shows B visiting larger distances during part of its record before returning closer to the compact region. A also fluctuates, with different proportions of time spent in particular ranges. The spring supplies a common bias without making trajectories identical. Starting conformation and finite observation time remain visible in these actual histories.

### Two histories under the same bias

Each bridge spans 500 ps; half-means use its 250 ps division.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g17/en/#en-s6)

Two 500 ps bridge records at the same 0.65 nm center, initialized from opposite sides. The lower panel compares mean distances in the first and second 250 ps of each window, retaining information about starting history and temporal changes.

Splitting at 250 ps gives A mean distances of 0.56049 and 0.53961 nm, and B means of 0.58331 and 0.58624 nm. A shifts toward shorter distances during this record. B's half-means are similar, although its trajectory contains persistent higher and lower regions. Half-means expose broad changes, while the full time series retains dwell periods and transitions. When internal conformational changes are slow, similar coordinate means need additional structural comparison to establish whether the same families of configurations have been visited.

The additional records improve connectivity along distance. Combining the normalized A and B distributions with equal weights gives overlap 0.56125 with the original 0.6 nm window and 0.36203 with the 0.7 nm window. A and B overlap by 0.76025. Compared with the original neighboring-window value of 0.04296, the intermediate region now has substantially more common coverage. At the same time, history-dependent means and temporal distributions remain visible. Retaining both observations identifies what the extra computation improved and what the next sampling stage should examine.

The bridges are five times longer than the original windows and contribute more records to WHAM. All windows retain the same 0.1 ps scalar-output interval. The native combination uses recorded counts without an additional autocorrelation-weight correction. More stored points can improve a histogram's resolution, while their independent information still depends on correlation time. A study seeking reliable uncertainty estimates would compare additional preparations and longer records, including internal structural observables, with sampling units chosen to reflect those correlations.

## Remove the bias and combine the windows

Each spring favors its own center, so adding raw histograms would mix different sampling preferences. WHAM uses the known biases to account for how each position is encouraged or discouraged and simultaneously solves for relative window normalizations. A position frequently observed despite an unfavorable bias contributes different information from one that the spring strongly favors. Overlapping windows constrain those comparisons, allowing relative probabilities along the common coordinate to be reconstructed.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g17/en/#en-s7)

Figure 3 · Counts and biases are known, while common probabilities and window normalizations depend on one another. The matrix and curve illustrate that statistical relationship.

WHAM jointly solves probabilities and window normalizationsEq. 6

![WHAM jointly solves probabilities and window normalizations](https://ml-biomat.com/static/agent-math/9f7b43ced8f3d517d7607f72.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| i, b | Window index and common bin index | 1 |
| p_{b} | Unbiased probability mass in bin b; division by bin width gives density | 1 |
| Hᵢb, nᵢ | Raw count in bin b and total observations for window i | count |
| wᵢb | Known bias energy of window i in bin b | kJ/mol |
| fᵢ | Window normalization free-energy offset, determined self-consistently | kJ/mol |
| R, T | Molar gas constant; common absolute temperature | kJ mol⁻¹ K⁻¹; K |
| (fᵢ−wᵢb)/(RT), −fᵢ/(RT), −wᵢb/(RT) | Energies divided by thermal energy, giving dimensionless exponents | 1 |
| exp | Natural exponential function, with base e | 1 |
| Σi, Σb | Sum over windows or bins | 1 |
| =, −, /, [ ], ( ), 1 | Equality, subtraction or negation, division, grouping; 1 is total normalized probability, and adjacency denotes multiplication | 1 |

Reading the relationshipKnown biases alter bin visitation. Common probabilities and window normalizations depend on one another; iteration makes all windows consistent with one statistical description.

A worked exampleOne zero-bias window with counts 2 and 3 gives p = (0.4, 0.6) and normalization f = 0. Multiple harmonic windows require position-dependent weights.

ConditionsThis form uses common temperature, bins, and raw-count weights. The native analysis applies no autocorrelation correction. Numerical convergence and conformational sampling are assessed separately.

A histogram stores distance counts while compressing away their time order. Keeping the time series is therefore useful before WHAM: similar aggregate counts can arise from different long residence periods. Segment comparisons and bridges from distinct starting structures restore some of the historical information hidden by that compression. Later uncertainty estimation should use resampling units appropriate to temporal correlations, such as sufficiently long blocks or independent simulations, rather than treating every saved observation as independent.

For a simple limiting case, imagine one window with zero bias throughout two bins. If its counts are two and three, the recovered probabilities are 0.4 and 0.6. The normalization constant then has no distance-dependent correction to make. A harmonic window requires a different correction in each bin because its bias changes with distance. Multiple windows add the requirement that their corrected estimates describe one common probability distribution. This small counting example gives the coupled equations a concrete starting point before interpreting a full set of molecular histograms.

The unknowns in the WHAM equations depend on one another. Unbiased bin probabilities require window-normalization constants, while those constants require the current probability estimate. The program iterates from an initial guess until successive changes fall below a tolerance, here 10⁻⁷. This controls numerical solution of the equations. Adequate conformational sampling is assessed through histories, overlap, and independent records. Successful numerical termination means that the equations for the supplied histograms have been solved to the chosen tolerance; time-segment comparisons then examine variation in those input statistics.

The script below prepares six matching list pairs: the original 26 windows, either bridge separately, both bridges together, and the first and second halves of all 28 windows. Each TPR line matches the force record from that same window. WHAM reads the center and stiffness from the TPR and reconstructs coordinate information from the bias force. Every analysis uses 298 K and 150 bins over 0.35–3.2 nm. Original windows split at 50 ps and bridges at 250 ps, each according to its own duration.

### Combine complete and segmented native WHAM inputs

```
"""Recompute six native WHAM profiles with matching grids and window lists."""
from pathlib import Path
import argparse,os,subprocess
import numpy as np


def read_xvg(path):
    return np.loadtxt([s for s in Path(path).read_text().splitlines() if s.strip() and not s.lstrip().startswith(('#','@'))])


def relative(path,folder):
    return os.path.relpath(path.resolve(),folder.resolve()).replace('\\','/')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original',type=Path,default=Path('records/original'))
    parser.add_argument('--bridge-a',type=Path,default=Path('records/bridge-a'))
    parser.add_argument('--bridge-b',type=Path,default=Path('records/bridge-b'))
    parser.add_argument('--out',type=Path,default=Path('wham-recomputed'))
    parser.add_argument('--gmx',default=os.environ.get('GMX','gmx'))
    parser.add_argument('--prepare-only',action='store_true')
    args=parser.parse_args()
    datasets=[(f'original-{i:02d}',args.original/f'us{i}.tpr',args.original/f'us{i}_pullf.xvg',100) for i in range(26)]
    datasets += [(f'bridge-{letter}',folder/'us.tpr',folder/'us_pullf.xvg',500) for letter,folder in [('a',args.bridge_a),('b',args.bridge_b)]]
    configurations=[('original26',datasets[:26],None),('bridge-a27',datasets[:27],None),
                    ('bridge-b27',datasets[:26]+[datasets[27]],None),('both28',datasets,None),
                    ('both28-first-half',datasets,0),('both28-second-half',datasets,1)]
    for name,selected,half in configurations:
        folder=args.out/name;folder.mkdir(parents=True,exist_ok=True)
        tpr_lines=[];force_lines=[]
        for label,tpr,force,duration in selected:
            if not tpr.is_file() or not force.is_file():raise FileNotFoundError(label)
            tpr_lines.append(relative(tpr,folder))
            if half is not None:
                data=read_xvg(force)
                mask=data[:,0]<duration/2 if half==0 else data[:,0]>=duration/2
                selected_force=folder/(label+'-pullf.xvg')
                np.savetxt(selected_force,data[mask],fmt='%.8g')
            else:selected_force=force
            force_lines.append(relative(selected_force,folder))
        (folder/'tpr-files.dat').write_text('\n'.join(tpr_lines)+'\n',encoding='utf8',newline='\n')
        (folder/'pullf-files.dat').write_text('\n'.join(force_lines)+'\n',encoding='utf8',newline='\n')
        command=[args.gmx,'wham','-it','tpr-files.dat','-if','pullf-files.dat','-o','pmf.xvg','-hist','histograms.xvg',
                 '-b','0','-temp','298','-bins','150','-min','0.35','-max','3.2','-tol','1e-7']
        if not args.prepare_only:
            with (folder/'wham.log').open('wb') as log:
                subprocess.run(command,cwd=folder,stdout=log,stderr=subprocess.STDOUT,check=True)
        print(name,'inputs prepared' if args.prepare_only else 'native WHAM completed')
```

Match TPR and force files line by line and run six native analyses on a common grid.

A profile's energy zero can be shifted. To compare the six curves, we set their mean over bins from 0.8 up to 1.0 nm to zero, then inspect other regions relative to that common reference. The left plot enlarges the bridge region and shows how the two histories influence shorter distances. The right compares complete records with the two temporal halves of the same 28 windows. Differences remain across a substantial distance range, providing concrete evidence of sensitivity to record length and conformational visitation and a basis for further sampling.

### Relative profiles and temporal differences

Six native WHAM analyses; mean over 0.8–1.0 nm is set to zero, and unsampled bins remain gaps.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g17/en/#en-s7)

Native GROMACS WHAM profiles use the same 150-bin grid and are shifted so that the mean over 0.8≤r<1.0 nm is zero. Left: local changes when different bridges are added. Right: all 28 windows and their chronological halves. Bins with no native histogram counts are left unconnected; shading marks the two fixed comparison bands.

The fixed grid also includes empty edge bins. Native output can contain finite placeholder values there, so the analysis reads the corresponding histograms and plots only bins with positive combined counts. Empty bins remain gaps. The resulting curve represents the sampled range; sparsely visited distances near its outer end can still produce steep, sensitive tails. Extending an axis does not add observations. Expanding the interpretable interval requires accumulating relevant configurations in that additional region.

## Turn a profile into an assessable research result

The complete analysis starts from the 28 distance and force records, checks times, sample counts, and the force–displacement relation, and computes means, half-means, overlap, and the six native WHAM profiles. In a fixed window, scalar bias force equals minus the spring constant times displacement from its center. Finite output precision leaves a small rounding residual. Checking this identity helps detect mismatched files, incorrect centers, or sign conventions, connecting each plotted measurement to a specific underlying record.

### Analyze overlap, histories, and profile variation

```
"""Analyze recorded chignolin windows and native GROMACS WHAM profiles."""
from pathlib import Path
import argparse,json,csv,logging
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)


def xvg(path):
    lines=Path(path).read_text(encoding='utf-8').splitlines()
    data=np.loadtxt([line for line in lines if line.strip() and not line.lstrip().startswith(('#','@'))])
    if data.ndim!=2 or data.shape[1]<2 or not np.isfinite(data).all():
        raise ValueError(f'Expected finite two-column XVG: {Path(path).name}')
    return data


def save(fig,path):
    fig.savefig(path.with_suffix('.svg'))
    fig.savefig(path.with_suffix('.png'),dpi=150)
    plt.close(fig)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original',type=Path,default=Path('records/original'))
    parser.add_argument('--bridge-a',type=Path,default=Path('records/bridge-a'))
    parser.add_argument('--bridge-b',type=Path,default=Path('records/bridge-b'))
    parser.add_argument('--wham',type=Path,default=Path('records/wham'))
    parser.add_argument('--out',type=Path,default=Path('analysis'))
    parser.add_argument('--language',choices=['zh','en'],default='en')
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    zh=args.language=='zh'
    fonts=['Microsoft YaHei','Noto Sans CJK SC','Source Han Sans SC','WenQuanYi Zen Hei','DejaVu Sans'] if zh else ['DejaVu Sans']
    plt.rcParams.update({'font.family':fonts,'font.size':14,'axes.titlesize':16,'axes.labelsize':15,'svg.fonttype':'path','axes.unicode_minus':False})
    datasets=[(f'original-{i:02d}',args.original/f'us{i}_pullx.xvg',args.original/f'us{i}_pullf.xvg',100,.5+.1*i) for i in range(26)]
    datasets += [(f'bridge-{letter}',folder/'us_pullx.xvg',folder/'us_pullf.xvg',500,.65) for letter,folder in [('a',args.bridge_a),('b',args.bridge_b)]]
    edges=np.arange(.3,3.3001,.01);mids=(edges[1:]+edges[:-1])/2;hist=[];raw=[];rows=[]
    for name,path,forcepath,duration,center in datasets:
        data=xvg(path);force=xvg(forcepath)
        if len(data)!=duration*10+1 or data[0,0]!=0 or data[-1,0]!=duration or not np.all(np.diff(data[:,0])>0):
            raise ValueError(f'Unexpected times or sample count: {name}')
        if force.shape!=data.shape or not np.array_equal(force[:,0],data[:,0]):
            raise ValueError('Coordinate and force records must share time points')
        values=data[:,1];counts=np.histogram(values,edges)[0]
        if counts.sum()!=len(values):raise ValueError('Histogram range excludes recorded samples')
        probabilities=counts/counts.sum();hist.append(probabilities);raw.append(data)
        # GROMACS scalar pull force is -k times displacement from the fixed center.
        residual=float(np.max(np.abs(force[:,1]+1000*(values-center))))
        if residual>.02:raise ValueError('Force/coordinate/spring relation differs from the recorded bias')
        rows.append({'name':name,'center_nm':center,'samples':len(values),'duration_ps':duration,
                     'mean_nm':float(values.mean()),'population_sd_nm':float(values.std()),
                     'first_half_mean_nm':float(values[data[:,0]<duration/2].mean()),
                     'second_half_mean_nm':float(values[data[:,0]>=duration/2].mean()),
                     'max_force_rounding_residual_kJ_mol_nm':residual})
    hist=np.asarray(hist);combined=(hist[26]+hist[27])/2
    overlap=lambda a,b:float(np.minimum(a,b).sum())
    overlaps={'old_0.6_vs_0.7':overlap(hist[1],hist[2]),'bridge_a_vs_b':overlap(hist[26],hist[27]),
              '0.6_vs_combined_bridge':overlap(hist[1],combined),'combined_bridge_vs_0.7':overlap(combined,hist[2])}
    configurations=['original26','bridge-a27','bridge-b27','both28','both28-first-half','both28-second-half']
    profiles={};profile_rows=[]
    for name in configurations:
        arr=xvg(args.wham/name/'pmf.xvg')
        if len(arr)!=150:raise ValueError('Expected 150 native WHAM bins')
        if profiles and not np.array_equal(arr[:,0],next(iter(profiles.values()))[:,0]):raise ValueError('WHAM grids differ')
        native_hist=xvg(args.wham/name/'histograms.xvg')
        if not np.array_equal(native_hist[:,0],arr[:,0]):raise ValueError('Native histogram and PMF grids differ')
        sampled=native_hist[:,1:].sum(axis=1)>0
        ref=(arr[:,0]>=.8)&(arr[:,0]<1.);target=(arr[:,0]>=2.4)&(arr[:,0]<2.6)
        if not sampled[ref|target].all():raise ValueError('Comparison interval contains unsampled bins')
        offset=float(arr[ref,1].mean());arr[:,1]-=offset;profiles[name]=arr
        profile_rows.append({'name':name,'reference_offset_kJ_mol':offset,'band_difference_kJ_mol':float(arr[target,1].mean()),
                             'sampled_bins':int(sampled.sum()),'unsampled_bins':int((~sampled).sum()),
                             'sampled_range_nm':[float(arr[sampled,0].min()),float(arr[sampled,0].max())]})
        # Native WHAM writes finite placeholders in empty bins; omit these from
        # interpreted profiles while retaining the unmodified native XVG inputs.
        arr[~sampled,1]=np.nan
        np.savetxt(args.out/(name+'-aligned.csv'),arr,delimiter=',',header='distance_nm,relative_profile_kJ_mol',comments='')
    pull=xvg(args.original/'pull_pullx.xvg');selected=[]
    for center in np.linspace(.5,3.,26):
        j=int(np.argmin(np.abs(pull[:,1]-center)))
        selected.append({'center_nm':float(center),'time_ps':float(pull[j,0]),'distance_nm':float(pull[j,1])})
    summary={'temperature_K':298,'spring_kJ_mol_nm2':1000,'histogram_bin_width_nm':.01,
             'windows':rows,'overlap_coefficients':overlaps,'native_profiles':profile_rows,
             'pulling_selected_frames':selected,
             'definitions':{'window_sd':'Population dispersion of all recorded coordinates; not standard error',
                            'half':'Time < duration/2 and time >= duration/2 for each window separately',
                            'profile_alignment':'Mean of bins with 0.8 <= distance < 1.0 nm set to zero',
                            'band_comparison':'Mean profile over 2.4 <= distance < 2.6 nm after alignment; a fixed band comparison',
                            'overlap':'Sum of minimum normalized bin probabilities on common 0.01 nm bins',
                            'empty_profile_bins':'Masked using zero total native histogram counts; original XVG remains unchanged'}}
    (args.out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    with (args.out/'window-statistics.csv').open('w',newline='',encoding='utf-8') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    teal='#117f92';orange='#c56b3b';purple='#70629b';gray='#7f898e'
    fig,ax=plt.subplots(figsize=(11,5),constrained_layout=True)
    ax.plot(pull[:,0],pull[:,1],color=teal,label='记录端距' if zh else 'Recorded end distance')
    ax.plot(pull[:,0],pull[0,1]+.005*pull[:,0],ls='--',color=gray,label='移动弹簧中心' if zh else 'Moving spring center')
    ax.scatter([r['time_ps'] for r in selected],[r['distance_nm'] for r in selected],s=28,color=orange,zorder=4,label='26个窗口的初始帧' if zh else 'Initial frames for 26 windows')
    ax.set(xlabel='拉伸时间 / ps' if zh else 'Pulling time / ps',ylabel='端距 / nm' if zh else 'End distance / nm',title='移动偏置生成一组起始构象' if zh else 'A moving bias generates starting conformations')
    ax.legend(loc='upper center',bbox_to_anchor=(.5,1.34),ncol=1,fontsize=12);ax.set_title(ax.get_title(),pad=88);ax.grid(alpha=.15);save(fig,args.out/'pulling-selection')
    fig,axs=plt.subplots(1,2,figsize=(13,6),constrained_layout=True)
    im=axs[0].imshow(hist[:26]/.01,origin='lower',aspect='auto',extent=[edges[0],edges[-1],.45,3.05],cmap='magma',interpolation='nearest')
    axs[0].plot([.5,3],[.5,3],'w--',lw=1.2,label='中心位置' if zh else 'Bias centers')
    axs[0].plot([r['mean_nm'] for r in rows[:26]],[r['center_nm'] for r in rows[:26]],'o',ms=3,color='#71d6e1',label='实际平均端距' if zh else 'Recorded mean distances')
    axs[0].set(xlabel='实际端距 / nm' if zh else 'Recorded distance / nm',ylabel='弹簧中心 / nm' if zh else 'Bias center / nm',title='26个原始窗口' if zh else 'The original 26 windows')
    legend=axs[0].legend(fontsize=11,loc='upper center',bbox_to_anchor=(.5,1.18));legend.legend_handles[0].set_color('#555555');axs[0].set_title(axs[0].get_title(),pad=75);fig.colorbar(im,ax=axs[0],label='概率密度 / nm⁻¹' if zh else 'Probability density / nm⁻¹',shrink=.8)
    for i,color,label in [(1,teal,'0.60 nm'),(2,orange,'0.70 nm'),(26,purple,'0.65 nm A'),(27,gray,'0.65 nm B')]:axs[1].plot(mids,hist[i]/.01,color=color,label=label)
    axs[1].set(xlim=(.4,.85),xlabel='实际端距 / nm' if zh else 'Recorded distance / nm',ylabel='概率密度 / nm⁻¹' if zh else 'Probability density / nm⁻¹',title='薄弱连接处与新增桥接窗' if zh else 'A weak connection and the bridge windows')
    axs[1].legend(fontsize=12,loc='upper center',bbox_to_anchor=(.5,1.2),ncol=2);axs[1].set_title(axs[1].get_title(),pad=75);axs[1].grid(alpha=.15);save(fig,args.out/'window-overlap')
    fig,axs=plt.subplots(2,1,figsize=(11,8),constrained_layout=True)
    for index,color,label in [(26,teal,'A：从0.60 nm窗起步' if zh else 'A: start from the 0.60 nm window'),(27,orange,'B：从0.70 nm窗起步' if zh else 'B: start from the 0.70 nm window')]:
        a=raw[index];axs[0].plot(a[:,0],a[:,1],color=color,alpha=.65,lw=.7,label=label)
        for x0,x1,key in [(0,250,'first_half_mean_nm'),(250,500,'second_half_mean_nm')]:axs[1].plot([x0,x1],[rows[index][key]]*2,color=color,lw=3)
        axs[1].scatter([125,375],[rows[index]['first_half_mean_nm'],rows[index]['second_half_mean_nm']],color=color,s=40)
    axs[0].axhline(.65,color=gray,ls='--',label='共同偏置中心0.65 nm' if zh else 'Shared bias center 0.65 nm')
    axs[0].legend(loc='upper center',bbox_to_anchor=(.5,1.31),ncol=1,fontsize=12)
    axs[0].set(ylabel='瞬时端距 / nm' if zh else 'Instantaneous distance / nm')
    axs[1].set(ylabel='各半段平均端距 / nm' if zh else 'Mean distance\nin each half / nm')
    for ax in axs:ax.set_xlabel('桥接窗记录时间 / ps' if zh else 'Bridge production time / ps');ax.axvline(250,color='#bbb',ls=':');ax.grid(alpha=.15)
    save(fig,args.out/'bridge-history')
    fig,axs=plt.subplots(1,2,figsize=(13,6),constrained_layout=True)
    for name,color,label in [('original26',gray,'原26窗' if zh else 'Original 26'),('bridge-a27',teal,'加桥A' if zh else 'Add A'),('bridge-b27',orange,'加桥B' if zh else 'Add B'),('both28',purple,'加两桥' if zh else 'Add both')]:
        arr=profiles[name];axs[0].plot(arr[:,0],arr[:,1],color=color,label=label)
    for name,color,label in [('both28',purple,'完整记录' if zh else 'Complete records'),('both28-first-half',teal,'各窗前半段' if zh else 'First half of each window'),('both28-second-half',orange,'各窗后半段' if zh else 'Second half of each window')]:
        arr=profiles[name];axs[1].plot(arr[:,0],arr[:,1],color=color,label=label)
    for ax in axs:
        ax.axvspan(.8,1,color=teal,alpha=.10);ax.axvspan(2.4,2.6,color=orange,alpha=.12);ax.axhline(0,color='#bbb',lw=1)
        ax.set(xlabel='端距 / nm' if zh else 'End distance / nm',ylabel='相对自由能剖面 / kJ mol⁻¹' if zh else 'Relative free-energy profile / kJ mol⁻¹');ax.grid(alpha=.15)
    axs[0].set_xlim(.4,1.05)
    local=np.concatenate([a[(a[:,0]>=.4)&(a[:,0]<=1.05),1] for a in list(profiles.values())[:4]])
    axs[0].set_ylim(float(np.nanmin(local))-2,float(np.nanmax(local))+3)
    axs[0].legend(fontsize=12,loc='upper center',bbox_to_anchor=(.5,1.29),ncol=2)
    axs[1].legend(fontsize=12,loc='upper center',bbox_to_anchor=(.5,1.29),ncol=1)
    axs[0].set_title('桥接区域的相对剖面' if zh else 'Relative profiles in the bridge region',pad=100)
    axs[1].set_title('相同28窗的分段比较' if zh else 'Time-segment comparison of the same 28 windows',pad=100)
    save(fig,args.out/'wham-profiles')
    print(json.dumps({'overlap':overlaps,'profiles':profile_rows,'bridges':rows[-2:]},indent=2))


if __name__=='__main__':main()
```

Compute statistics from original XVG records, check bias force, and mask empty bins using actual histograms.

### Reproduce the Chinese and English result plots

```
#!/usr/bin/env bash
set -euo pipefail
python analyze_umbrella.py --out results-zh --language zh
python analyze_umbrella.py --out results-en --language en
```

Use the packaged records directory with the same analysis definitions.

For the complete records including both bridges, the mean profile over 2.4–2.6 nm lies 20.7188 kJ/mol above the 0.8–1.0 nm reference-band mean. Analyses of the first and second halves give 23.4533 and 17.6447 kJ/mol. This compares average profile heights in two predefined distance bands, providing a convenient measure of temporal variation. A folded-versus-unfolded free-energy difference requires structurally defined states, integration of their respective probabilities, and a logarithm of the state-probability ratio. That operation differs from averaging profile heights in two intervals.

Likewise, minima and high regions along end distance require structural interpretation. Several backbone angles and side-chain contacts can generate similar compact separations, allowing multiple internal conformations in one distance bin. A useful extension would record backbone hydrogen bonds or selected side-chain contacts and compare their distributions at similar distances. Different starting structures would reveal whether these internal arrangements exchange. If their exchange is slower than distance fluctuations, adding a second observation coordinate or further sampling can address the missing conformational information directly.

The workflow also helps allocate computation. Short exploratory records identify connected regions and windows whose actual means differ substantially from their centers. Further work can then focus on a defined sampling problem. After adding records, compare histories and profiles again. The complete scripts support longer windows or additional preparations, while fixed binning, temperature, bias definitions, and reference intervals make it easier to distinguish changes caused by new sampling from changes caused by measurement definitions.

Moving springs, fixed windows, bridges, and WHAM answer distinct questions: how to generate starting structures, how to observe a selected region, how to connect neighboring records, and how to recover relative probabilities. The actual example shows improved local overlap alongside persistent history effects in the profile. Reading both turns the free-energy curve into a result that can guide the next calculation. Molecular motion, statistical weighting, and the research question become connected through definitions and measurements that can be checked and reproduced.

## Further Reading and Open Materials

- [GROMACS tutorials: chignolin umbrella sampling](https://github.com/Lemkul-Lab/gmx_tutorials_jpcb/tree/main/inputs/03_chignolin) · Justin A. Lemkul / Lemkul Lab · MIT

  Initial structure, distance coordinate, 26-window workflow, and input settings.

  Retain the scientific question; use a 6.6 nm cubic box, shorter teaching records, dual-start bridges, segmented analysis, and updated complete scripts.
- [Introductory Tutorials for Simulating Protein Dynamics with GROMACS](https://doi.org/10.1021/acs.jpcb.4c04901) · Justin A. Lemkul · CC BY 4.0

  Scientific design and objectives of Exercise 3.

  Reorganize explanations, symbol tables, history graphics, interaction, and recorded results; short windows emphasize sampling behavior.
- [CHARMM July 2022 GROMACS force-field archive](https://mackerell.umaryland.edu/charmm_ff.shtml) · MacKerell laboratory and CHARMM parameter contributors · Publicly downloadable parameter archive; separate open license not stated in the archived package

  CHARMM36m protein and CHARMM TIP3P parameters.

  Fetch from the maintainer and verify the hash; retain original terms and citation instructions for the parameter package.
- [1UAO: ten-residue peptide chignolin](https://www.rcsb.org/structure/1UAO) · S. Honda, K. Yamasaki, Y. Sawada, H. Morii · wwPDB data: CC0

  Experimental identity, sequence, and NMR conformer ensemble.

  Redraw model 1 Cα coordinates as an orthographic projection.
- [Nonphysical sampling distributions in Monte Carlo free-energy estimation: Umbrella sampling](https://doi.org/10.1016/0021-9991%2877%2990121-8) · G. M. Torrie and J. P. Valleau · Citation; no source text or figures reproduced

  History and statistical idea of umbrella sampling.

  Explain biased allocation of observations through the peptide problem.
- [The weighted histogram analysis method for free-energy calculations on biomolecules. I. The method](https://doi.org/10.1002/jcc.540130812) · S. Kumar, D. Bouzida, R. H. Swendsen, P. A. Kollman, J. M. Rosenberg · Citation; no source text or figures reproduced

  WHAM history and self-consistent normalization equations.

  Explain discrete bin probabilities and a zero-bias counting example.
- [GROMACS 2026.4: gmx wham](https://manual.gromacs.org/2026.4/onlinehelp/gmx-wham.html) · GROMACS development team · Official documentation; linked for command definitions

  Native command, histograms, correlation, and input-pairing requirements.

  Use a shared grid with empty-bin checks and temporal comparisons.
