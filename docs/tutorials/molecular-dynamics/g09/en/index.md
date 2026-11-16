# How Reliable Is a Curve? Replicates, Correlation and Error

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g09/en/
Language: en

Use three ubiquitin trajectories to separate fluctuations, temporal correlation, and uncertainty in an average, then plan the next sampling step.

## Why thousands of saved frames still need a reliability check

Suppose you want to know how hot a city usually becomes in summer. Recording temperature every second for one hour produces 3,600 numbers. Measuring once a day at the same time for a month produces only about 30. The larger record mostly describes the weather during that particular hour; the smaller one may cover a broader range of conditions. Molecular trajectories present a similar question. A file can contain thousands of conformations, but they arise along continuous motion, with neighbouring frames often retaining similar structure. Interpreting a curve requires its observation count, total duration, and the changes actually visited during that duration.

This matters directly for research decisions. Imagine that mean protein gyration radii in two solutions differ by 0.003 nm. We would like to associate that difference with solution conditions. If repeated trajectories under one condition commonly differ by a similar amount, additional sampling and replication become the next useful steps before comparing conditions. Alternatively, a binding pocket may remain open in one trajectory and close early in another. The question then moves from selecting a snapshot toward measuring state populations and transition times. Statistical analysis helps allocate the next calculation to information that distinguishes the physical alternatives of interest.

We continue with ubiquitin in water: 76 amino acid residues, AMBER99SB-ILDN protein parameters, TIP3P water, and the same solvated ion composition at 300 K and 1 bar. Three branches begin from common minimized coordinates, with separate initial velocities and random thermostat seeds. Each receives 100 ps of NVT preparation, 200 ps of NPT preparation, and 1 ns of production without protein position restraints. Protein, water, and ion interactions remain the same. These records therefore answer a defined question: starting from this prepared state under this model, how much short-time variation appears when the random motion is started again?

We first plot the three raw records and their cumulative means, then examine time correlations, block averages, and variation between replicas. RMSD measures displacement from a shared reference, while radius of gyration measures the spread of protein mass about its own centre. Each needs a separate sampling assessment. By the end, you will be able to identify what a plotted uncertainty treats as a repeat, explain why more frequent output differs from longer observation, and design a concrete next sampling step. The uncertainty discussed here concerns finite sampling; integration accuracy, force-field choice, and correspondence with experimental conditions remain separate numerical and modelling questions.

Keep one distinction in mind throughout. Molecular thermal motion fluctuates, and our estimate of its average also has uncertainty because observation is finite. A flexible protein loop can continue moving widely even after extensive observation. More appropriate samples improve knowledge of that distribution; they do not remove the molecule’s physical flexibility. The equations below separate quantities describing how much the molecule moves from quantities describing how precisely its average behaviour has been estimated. Both can have length units while answering different questions.

## Continuous motion retains memory: the origin of blocking

The current coordinates and velocities enter the next integration step, so a trajectory naturally contains temporal relationships. A loop that has just moved outward will often remain nearby in the next saved frame. A slow conformational adjustment can keep many successive frames within a similar region. Memory here has a statistical meaning: knowing the present value helps predict a value a short time later. It implies neither purposeful information storage nor a common memory duration for every observable. Velocity, a local bond angle, overall size, and a conformational state can change on quite different time scales.

As molecular dynamics and Monte Carlo calculations accumulated longer records, researchers recognized that applying an independent-measurement error formula directly to correlated data counts repeated information too generously. In 1989, Flyvbjerg and Petersen studied error estimation for averages of correlated data using successive combinations of neighbouring observations. The historical contribution brought the data-generation process into the analysis. Preserving the order of a set of numbers and shuffling that order can leave its mean and spread unchanged while altering its temporal relationships. An uncertainty calculation needs to account for those relationships.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g09/en/#en-s2)

Figure 1 · Historical concept diagram of neighbouring observations combined into blocks. Values are dimensionless; B₂ and B₄ average two and four observations per block.

Imagine a slowly varying water-level record. Closely spaced observations often belong to the same crest. Their average represents a short time interval; averaging adjacent intervals then represents a longer one. Once a block covers much of the correlated motion, the remaining relationships between block means can weaken. Variation between blocks can then help estimate the sampling scale of the overall mean. The molecular model has not changed. The statistical unit has changed from one frame to the average of a contiguous period, preserving the sequence in which the observations occurred.

Blocking also reveals a trade-off. Short blocks provide many block means, but adjacent blocks may still rise and fall with the same slow change. Long blocks reduce that relationship while leaving fewer means to compare. A 1,000 ps record contains ten blocks of 100 ps or only five blocks of 200 ps. Selecting a single convenient block length can hide this dependence. Plotting the estimate across several lengths, alongside the original time trace, makes the trade-off visible and connects the statistical calculation to the motion actually recorded.

Current simulation practice combines this idea with multiple trajectories. Blocking examines the temporal organization inside one record. Starting another random realization under the same modelling protocol examines variation on restarting. These approaches address different levels of the same question. Several velocity-seeded protein runs can still share one experimental conformation and one initial solvent arrangement. Identifying those common conditions makes the meaning of replication precise and helps decide whether subsequent work should introduce more starting conformations or independently rebuilt solvent environments.

## Design the repetitions before comparing them

A meaningful comparison starts with identical measurement definitions. All three RMSD records use the same 228 backbone N, Cα, and C atoms, a mass-weighted rigid fit, and the same minimized reference. Radius of gyration uses masses and whole-molecule coordinates for all 1,231 protein atoms. If every replica instead used its own first production frame as reference, the curves would separately measure departures from different starting structures. Reference differences would then enter the comparison. A common reference supplies the same ruler, while consistent atom selection and units keep the measured quantities aligned.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g09/en/#en-s3)

Figure 2 · Random realizations conditional on a common start. States continue within each branch; shared reference and atom selections define the comparison.

Each branch begins from the same em.gro coordinates and generates its own velocities at the NVT entry point. The gen-seed setting selects that initial random draw; ld-seed selects the random process used by the corresponding simulation stage. The first initial-velocity seed is 20261121, with the next two incremented by one. NVT, NPT, and production use their own sets of ld-seed values. A seed is an identifier for a reproducible random-number sequence. Its magnitude does not encode temperature, stronger motion, or higher-quality results. The target conditions and dynamics determine those behaviours; the seed chooses another realization under the same rules.

Velocities are generated only at the beginning of NVT. NPT reads the preceding coordinates and checkpoint, and production continues from its NPT state. Both later stages retain gen-vel=no. Each branch therefore follows its own continuous preparation and motion, while the branches begin with separate random realizations. The 100 ps and 200 ps preparation stages restrain protein heavy-atom positions; production releases those restraints. Subsequent conformational analysis should include that release in its understanding of the protocol and examine whether the structure continues adjusting during the recorded interval.

The runner below creates a new set of replica folders. Place em.gro, topol.top, and posre.itp from the preceding preparation in a folder named prepared. The AMBER99SB-ILDN files referenced by the topology come from the matching GROMACS installation. For each replica, the script builds a reference, executes the three stages, and exports RMSD and gyration records. Separate folders retain the connection between each curve and its conditions. Keep the three baseline MDP files and both setup scripts together in the example directory, then run bash run_replicas.sh.

### Run three replicas and export the same observables

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
python make_replicas.py --prepared prepared --output new-replicas
for replica in 1 2 3; do
  (
    cd "new-replicas/replica-${replica}"
    "$gmx" grompp -f md.mdp -c em.gro -p topol.top -o reference.tpr
    "$gmx" grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
    "$gmx" mdrun -deffnm nvt -ntmpi 1 -ntomp 4 -pin off
    "$gmx" grompp -f npt.mdp -c nvt.gro -t nvt.cpt -r em.gro -p topol.top -o npt.tpr
    "$gmx" mdrun -deffnm npt -ntmpi 1 -ntomp 4 -pin off
    "$gmx" grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr
    "$gmx" mdrun -deffnm md -ntmpi 1 -ntomp 4 -pin off
    printf 'Protein\nSystem\n' | "$gmx" trjconv -s md.tpr -f md.xtc -o md-whole.xtc -pbc mol -center
    printf 'Backbone\nBackbone\n' | "$gmx" rms -s reference.tpr -f md-whole.xtc -o rmsd.xvg -fit rot+trans
    "$gmx" gyrate -s md.tpr -f md-whole.xtc -o gyrate.xvg -sel 'group "Protein"'
  )
done
python analyze_replicas.py --records new-replicas --out analysis --language en
```

Run bash run_replicas.sh in the example directory; prepared contains common minimized coordinates, topology and position-restraint file.

The generator locates each seed by its parameter name and replaces exactly that setting. Baseline inputs match the first reference replica; subsequent branches differ at the specified seed entries. Creating a fresh output directory preserves completed calculations. Common coordinates, common topology, and different seeds are thus expressed as an explicit computational design: every branch has the same potential-energy model and its own thermal history. The input files below make preparation lengths, restraints, coupling choices, and production duration available for inspection alongside that design.

### Generate replica inputs and fixed seeds

```
"""Create three independent random realizations from one prepared structure.

python make_replicas.py --prepared prepared --output new-replicas

The prepared folder contains em.gro, topol.top and posre.itp from the protein
preparation. Baseline nvt.mdp, npt.mdp and md.mdp sit beside this script.
"""
from pathlib import Path
import argparse
import re
import shutil


def replace_setting(text, key, value):
    pattern = rf"(?m)^{re.escape(key)}\s*=.*$"
    result, count = re.subn(pattern, f"{key} = {value}", text)
    if count != 1:
        raise ValueError(f"Expected exactly one {key} setting")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepared", type=Path, default=Path("prepared"))
    parser.add_argument("--output", type=Path, default=Path("new-replicas"))
    args = parser.parse_args()
    templates = {stage: Path(f"{stage}.mdp").read_text(encoding="utf-8")
                 for stage in ("nvt", "npt", "md")}
    for name in ("em.gro", "topol.top", "posre.itp"):
        if not (args.prepared/name).is_file():
            raise FileNotFoundError(f"Prepared input missing: {name}")
    args.output.mkdir(exist_ok=False)
    for number in (1, 2, 3):
        folder = args.output/f"replica-{number}"
        folder.mkdir()
        for name in ("em.gro", "topol.top", "posre.itp"):
            shutil.copyfile(args.prepared/name, folder/name)
        for stage, offset in [("nvt", 20261200), ("npt", 20261300), ("md", 20261400)]:
            text = replace_setting(templates[stage], "ld-seed", offset+number)
            if stage == "nvt":
                text = replace_setting(text, "gen-seed", 20261120+number)
            (folder/f"{stage}.mdp").write_text(text, encoding="utf-8", newline="\n")
    print("Prepared three seed-specific folders with the same coordinates and topology.")


if __name__ == "__main__":
    main()
```

Replace gen-seed and ld-seed by parameter name while retaining the other model parameters.

### Baseline NVT input: generate initial velocities

```
integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
nstenergy = 100
nstlog = 1000
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 300
cutoff-scheme = Verlet
nstlist = 20
coulombtype = PME
rcoulomb = 1.0
fourierspacing = 0.12
ewald-rtol = 1e-5
vdwtype = Cut-off
vdw-modifier = Potential-shift
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
define = -DPOSRES
nsteps = 50000
continuation = no
pcoupl = no
gen-vel = yes
gen-temp = 300
gen-seed = 20261121
ld-seed = 20261201
```

100 ps at 300 K with protein heavy-atom restraints; the generator supplies replica seeds.

### Baseline NPT input: continue the state and adjust volume

```
integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
nstenergy = 100
nstlog = 1000
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 300
cutoff-scheme = Verlet
nstlist = 20
coulombtype = PME
rcoulomb = 1.0
fourierspacing = 0.12
ewald-rtol = 1e-5
vdwtype = Cut-off
vdw-modifier = Potential-shift
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
continuation = yes
gen-vel = no
define = -DPOSRES
refcoord-scaling = com
nsteps = 100000
ld-seed = 20261301
```

200 ps at 300 K and 1 bar, retaining position restraints and continuing velocities.

### Baseline production input: release position restraints

```
integrator = md
dt = 0.002
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
nstxout = 0
nstvout = 0
nstfout = 0
nstxout-compressed = 500
nstenergy = 500
nstlog = 1000
tcoupl = v-rescale
tc-grps = System
tau-t = 1.0
ref-t = 300
cutoff-scheme = Verlet
nstlist = 20
coulombtype = PME
rcoulomb = 1.0
fourierspacing = 0.12
ewald-rtol = 1e-5
vdwtype = Cut-off
vdw-modifier = Potential-shift
rvdw = 1.0
DispCorr = EnerPres
pbc = xyz
pcoupl = C-rescale
pcoupltype = isotropic
tau-p = 5.0
ref-p = 1.0
compressibility = 4.5e-5
continuation = yes
gen-vel = no
nsteps = 500000
ld-seed = 20261401
```

1 ns of unrestrained NPT, one saved frame per ps, continuing the preceding state.

Reproduction also has several levels. Parallel execution can change the order of floating-point summations, and small rounding differences can progressively change a particular trajectory. These reference branches use the same GROMACS 2026.4 version and physical parameters, with CPU and accelerated execution among the realizations. The comparison concerns structural and statistical behaviour under common measurement definitions. A study specifically testing execution methods would additionally hold the input, seed, and execution conditions fixed for a numerical comparison. Here we preserve the actual differences between branches while keeping the scientific model explicit.

## What means, fluctuation widths, and cumulative curves describe

Represent one observable as a sequence of values ordered in time, choosing RMSD or gyration radius. Each value has units of nm. The arithmetic mean adds them and divides by their count, assigning equal weight to equally spaced saved times. Sample standard deviation subtracts that mean, squares the deviations, sums them, divides by N−1, and takes a square root. Squaring includes both upward and downward deviations; the final root restores length units. The N−1 denominator accounts for estimating the centre from the same data. It does not, by itself, solve the effective-sample-size problem created by temporal correlation.

Mean and sample standard deviationEq. 1

![Mean and sample standard deviation](https://ml-biomat.com/static/agent-math/60e186597ec69212c30c8b8e.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| xⱼ, x̄ | Observation j and the mean of the selected observations; the bar denotes averaging | nm |
| sₓ | Sample standard deviation of the record, describing spread about its mean | nm |
| N, j | Number of observations and their index; N=1000 here | 1 |
| (xⱼ−x̄)² | Squared deviation of one observation from the mean | nm² |
| N−1 | Denominator of the sample variance estimator; temporal correlation is examined separately | 1 |
| Σ, /, −, +, = | Summation over specified indices, division, subtraction, addition, and defining equality; adjacent factors multiply | Operators have no units |
| √ | Nonnegative square root, converting nm² to nm | Operator has no unit |

Reading the relationshipEqually spaced observations receive equal weights. Squared deviations avoid sign cancellation; the square root restores the original scale.

A worked exampleFor 1.18, 1.20, and 1.22 nm, the mean is 1.20 nm and s=√[(0.0004+0+0.0004)/2]=0.020 nm.

ConditionsDescribes values and spread within a fixed window. Interpreting s/√N as the standard error of a mean requires examination of frame independence.

Consider three lengths: 1.18, 1.20, and 1.22 nm. Their mean is 1.20 nm. Squared deviations are 0.0004, zero, and 0.0004 nm²; dividing their sum by two and taking the square root gives a sample standard deviation of 0.02 nm. That number describes spread about the centre. Copying the same ordered trio ten times makes a longer table without adding a physical observation. Assessing how reliably the mean is known therefore requires the relationships among the numbers, not simply the larger count now entered into a calculator.

The raw plots display all 1,001 saved times from 0 through 1,000 ps. To divide a fixed interval into complete equal-sized blocks, the statistics use 0≤t<1000 ps: exactly 1,000 observations at times zero through 999 ps. The final point remains visible in the raw traces. The first 500 observations cover 0≤t<500 ps and the remaining 500 cover 500≤t<1000 ps. A 100 ps block therefore contains 100 records, giving ten blocks. This convention differs by one endpoint from the preceding lesson’s 1,001-frame description, so the present means retain their own explicit window.

### Three trajectories measured with the same ruler

Raw traces show 0–1000 ps; accumulated and block statistics use 0≤t<1000 ps. RMSD uses a common reference and Rg is mass-weighted over the full protein.

GROMACS 2026.4; chain A of PDB 1UBQ, 76 residues; AMBER99SB-ILDN with TIP3P. All 602 experimental heavy atoms are retained and 629 hydrogen atoms added. His68 uses neutral NE2 protonation, with charged free termini.

[Download reference data and complete inputs (ZIP) 0.36 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-protein-replicate-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g09/en/#en-s4)

Three random realizations share the protein model and minimized reference, with independent initial velocities and stochastic coupling. Raw traces show 0–1000 ps, while accumulated means use 1000 equally spaced records in 0≤t<1000 ps. Each curve retains one realization’s history.

Across these 1,000 observations, the three mean RMSDs are approximately 0.14377, 0.12485, and 0.19556 nm. Mean gyration radii are approximately 1.19152, 1.18785, and 1.18476 nm. The RMSD differences show distinct departures from the common reference, whereas the closer gyration radii show much smaller differences in overall mass-distribution size. Both observations can hold together. Reorientation of a loop or a local conformational change can alter reference-relative displacement without greatly changing global compactness. Residue fluctuations, contacts, and actual structures can then identify the locations responsible.

A cumulative mean uses all observations from production start up to the current point. It usually becomes smoother with time because each new observation contributes a progressively smaller fraction of the accumulated total. A larger existing record is harder for one new value to move. This arithmetic effect alone can make a curve appear to settle. We also examine agreement among cumulative means, the regions visited by raw traces, and means in separate windows. Smoothing aids reading; comparisons across these scales supply information about sampling.

The raw fluctuation widths have their own physical meaning. Replica 1 has an RMSD sample standard deviation of about 0.04167 nm and a gyration-radius standard deviation of about 0.00603 nm. These quantities fluctuate on different scales because their definitions differ. Ranking the numbers directly as grades of protein stability would discard that distinction. RMSD measures departure from one fixed structure; gyration radius measures spread around the current centre of mass. Both compress a complex conformation into a scalar, so structural inspection gives the changes their molecular interpretation.

## How far apart must observations be to add different information?

Imagine printing the same time trace on two transparent sheets. Keep one still, shift the other along the time axis, and compare their overlapping portions. If one tends to lie above its mean when the other does, the relationship is positive. If a high value tends to accompany a low one, it can be negative. Subtract the record mean first so that the comparison concerns fluctuations rather than a large constant background. Comparing different time positions within the same series is called autocorrelation. It turns a visual impression of persistent motion into a quantity with an explicit definition.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g09/en/#en-s5)

Figure 3 · Finite-record pair counting: ten observations yield seven pairs at lag three. Grey entries do not participate in this direction of pairing. Numbers inside cells are record indices.

With observations separated by 1 ps, shifting by k records compares values k ps apart. Multiply each pair of deviations: equal signs contribute positively and opposite signs negatively. Average over the available pairs, then divide by the mean squared deviation at zero lag. This produces a dimensionless correlation value. At zero lag, each deviation multiplies itself, so normalization gives C(0)=1. If the original relationship fades with increasing lag, the curve approaches zero. Negative portions can arise from reversals, a finite record, or slow changes and should be interpreted together with the underlying time trace.

Centered autocorrelation using the available pair countEq. 2

![Centered autocorrelation using the available pair count](https://ml-biomat.com/static/agent-math/9547f4c544bc1594deabd703.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| dⱼ, dⱼ₊ₖ | Two observations k records apart, each minus the same window mean | nm |
| xⱼ, x̄ | Observation j and the window mean | nm |
| v | Zero-lag mean squared deviation, with denominator N | nm² |
| dⱼdⱼ₊ₖ | Product of deviations: positive for equal signs and negative for opposite signs | nm² |
| C(k) | Normalized autocorrelation at lag k; C(0)=1 | 1 |
| N, j, k, N−k | Observation count, starting index, lag in records, and available pair count; one record is 1 ps here | 1 |
| Σ, /, −, +, = | Summation over specified indices, division, subtraction, addition, and defining equality; adjacent factors multiply | Operators have no units |
| ² | Multiply a deviation by itself, giving nm² | Exponent has no unit |

Reading the relationshipCompare deviations separated in time, average over available pairs, and normalize by the mean squared deviation.

A worked exampleFor the centered sequence −1, −1, 1, 1 nm, v=1 nm². At k=1 the product sum is 1 nm² over three pairs, giving C(1)=1/3.

ConditionsA finite-record estimator for equally spaced data with nonzero variance. Equilibrium memory interpretation additionally requires stationary statistics over the selected period.

Four already-centred observations illustrate the arithmetic: −1, −1, 1, 1. Their mean squared deviation at zero lag is one. At a lag of one record, the three pair products are 1, −1, and 1, giving correlation 1/3. Reorder the same values as −1, 1, −1, 1. Their mean and spread remain unchanged, but every one-lag product becomes −1. Order therefore contains information absent from the mean and histogram. Randomly shuffling a trajectory before analysis changes the temporal structure used to assess uncertainty.

Finite-record normalization includes an easily missed detail: a lag of k records leaves only N−k pairs. The program averages over that actual count, then divides by the zero-lag mean square from the whole selected window. Longer lags use fewer pairs and have greater sampling variation. Estimating the mean from the same finite record also affects the tail. We therefore display lags through 200 ps as diagnostics of this record’s time structure, alongside window and replica comparisons. Different software can use slightly different finite-sample conventions; matching formulas and pair counts is the first step in reproducing a result.

A further condition matters when interpreting a correlation curve as equilibrium memory: the average state and fluctuation properties should remain consistent during the analysed interval. If the protein continues moving away from its starting conformation over this nanosecond, that slow trend can also relate observations far apart in time. Integrating such a curve would mix adjustment with equilibrium fluctuations. Here we display the slow relationships and examine their consequences for blocking. Estimating an equilibrium correlation time requires a longer observation window with an appropriate statistical description for the specific conformational quantity.

Output spacing should match the process being observed. Saving every 100 ps skips details needed to study a few-picosecond relationship. Saving every 0.1 ps within the same 100 ps duration resolves that interval more finely while increasing file size. Extending the trajectory can instead encounter slower conformational changes. These are different investments. Estimating the relevant time scale before choosing output frequency and run duration helps retain the detail needed for the question while collecting observations over a useful physical span.

## Combine neighbouring times and watch the error estimate change

Block averaging turns the preceding intuition into an executable calculation. Choose b consecutive observations per block and average them. The whole record divides into M blocks of equal length. Blocks here do not overlap, and each observation belongs to exactly one. Calculate the sample standard deviation of those block means and divide by the square root of the number of blocks. The result is a block-based estimate of the standard error of the overall mean. That final interpretation assumes approximately independent block means, so we vary b and examine the result rather than treating division into blocks as proof of independence.

Equal blocks and the standard error from block meansEq. 3

![Equal blocks and the standard error from block means](https://ml-biomat.com/static/agent-math/82ec1a03ff4bd1513f3eb70c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Bₘ | Mean of contiguous block m | nm |
| b, M, N, m, j | Records per block, block count, total records, block index, and observation index | 1 |
| xⱼ, x̄ | An observation and the overall mean of the complete equal blocks | nm |
| SE_{b} | Standard error of the overall mean under approximate independence of block means | nm |
| (Bₘ−x̄)² | Squared deviation of a block mean from the grand mean | nm² |
| (m−1)b+1, mb | First and last observation indices in block m | 1 |
| Σ, /, −, +, = | Summation over specified indices, division, subtraction, addition, and defining equality; adjacent factors multiply | Operators have no units |
| √ | Nonnegative square root returning a variance to length units | Operator has no unit |

Reading the relationshipAverage neighbouring observations into blocks, then divide the sample variance of block means by the block count; assess independence through block lengths and sampling.

A worked exampleFour block means 1.18, 1.20, 1.22, 1.20 nm have squared-deviation sum 0.0008 nm²; SE=√[0.0008/(4×3)]=0.008165 nm.

ConditionsComplete, equal, non-overlapping blocks with at least two blocks. Long blocks must still leave sufficient block count; dependence on block length is a sampling diagnostic.

Suppose four sufficiently independent block means are 1.18, 1.20, 1.22, and 1.20 nm. Their grand mean is 1.20 nm, their sample standard deviation is about 0.01633 nm, and division by √4 gives a standard error of 0.008165 nm. The standard deviation describes variation among block means; the standard error describes the sampling scale of their combined estimate of the centre. If those blocks still rise and fall with one slow trend, their independence needs further examination. Obtaining a numerical answer and establishing its relevance to the physical question are connected but distinct steps.

### Temporal correlation and sensitivity to block length

A 1 ps recording interval and 1,000 selected values. Blocks range from one to 200 records, evaluated separately by replica; 200 ps leaves five blocks.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g09/en/#en-s6)

The left column shows autocorrelation after centering each record on its own window mean. The right column divides that record into equal, disjoint blocks and computes a standard error from block means. Increasing block duration from 1 to 200 ps reduces the count from 1000 to five; the appearance of a stable region informs the choice of statistical scale.

The actual graph compares block durations from 1 to 200 ps. Treating individual RMSD frames of replica 1 as independent gives a standard error of about 0.00132 nm. At 100 ps per block the estimate rises to approximately 0.01237 nm, and at 200 ps it is about 0.01747 nm. The increase shows that short blocks count nearby observations as too much independent information. There is no clear plateau over the lengths examined, and the longest length leaves only five blocks. Extending observation of the relevant conformational process, while retaining independent replicas, is therefore a concrete next step rather than selecting a final equilibrium error bar from this curve.

Gyration radius gives a more nuanced example. For replica 1, the estimates at 100 and 200 ps per block are both about 0.00104 nm. Replica 2 instead rises from about 0.00198 to 0.00262 nm, and replica 3 continues increasing as well. Displaying the three records together reveals that a local plateau in one branch may not characterize the whole preparation protocol. A small overall gyration change can still contain a slow shift beneath faster fluctuations. Comparing the same observable across branches helps expose such behaviour.

An increasing estimate with block length is not a mathematical requirement. Sampling variation among a small number of blocks can lower a particular point, and negatively correlated processes can behave differently. We seek a physically justified range: blocks cover the important temporal relationships, enough blocks remain, and different windows or replicas give compatible results. If the last two plotted points happen to meet, inspect their constituent block means to see whether a few blocks control the estimate. The purpose of the graph is to make these conditions inspectable, not to prescribe one universal shape.

This implementation divides 1,000 records directly at selected lengths rather than requiring a power-of-two record count. Durations of 1, 2, 5, 10, 20, 25, 50, 100, and 200 ps use every selected observation. Successive merging in the historical method and equal-length blocking share the aim of handling correlation, while their specific partitions and estimation details can differ. The GROMACS gmx analyze tool also offers blocking and optional fits to a correlation-time model. The complete Python implementation here exposes the direct calculation so that frame counts, denominators, and block lengths can be traced from equations to plots.

## How differences between trajectories enter a conclusion

A replica comparison first summarizes each trajectory by a consistently defined mean and then examines variation among those means. This order makes one random realization the statistical unit. Simply concatenating every frame can hide that unit and, if correlations are ignored, produce a very narrow uncertainty. For three equal-length records using the same window, the equal average of replica means has the same centre as pooling all values with equal weight. The important difference lies in how uncertainty around that centre is assessed and which independent units support it.

Using one random realization as the replicate unitEq. 4

![Using one random realization as the replicate unit](https://ml-biomat.com/static/agent-math/bad2ee064032fe065635554e.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Aᵣ | Mean observable for replica r over the common window | nm |
| Ā | Equal-weight average of replica means | nm |
| Q, r | Replica count and index; Q=3 here | 1 |
| s_{rep} | Sample standard deviation among replica means | nm |
| SE_{rep} | Mean standard error treating random realizations as independent units | nm |
| (Aᵣ−Ā)² | Squared deviation of a replica mean from the grand mean | nm² |
| Σ, /, −, +, = | Summation over specified indices, division, subtraction, addition, and defining equality; adjacent factors multiply | Operators have no units |
| √, rep | Nonnegative square root; rep labels between-replica statistics | Operator and label have no units |

Reading the relationshipLet each equal-length branch contribute one mean, then quantify differences on restarting through variation between branches.

A worked exampleThe Rg means are approximately 1.191521, 1.187855, 1.184757 nm; the grand mean is 1.188044 nm, s_rep=0.003386 nm and SE_rep=0.001955 nm.

ConditionsDescribes independent random realizations conditional on common prepared coordinates and the specified short-time protocol; the initial state and model remain shared conditions.

The three gyration means average to about 1.18804 nm. Their between-replica sample standard deviation is approximately 0.00339 nm. Treating these separately seeded, equal-length branches as repetitions gives a mean standard error of 0.00339/√3, about 0.00195 nm. Its target is the mean obtained by starting from the common prepared coordinates and following this short-time protocol. Shared initial conformation, force-field choice, and unvisited conformational regions remain common conditions. Broader starting-state coverage and longer structural sampling extend the scope of the estimate.

### Window means within and between replicas

Triangles denote means of the first and last 500 records; circles show means of all 1,000. Lines connect windows of the same replica.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g09/en/#en-s7)

Triangles mark means over 0≤t<500 ps and 500≤t<1000 ps; circles mark means of all 1000 records. Segments connect the two half-window means. The comparison shows differences associated with temporal windows and independent random histories; the markers denote window means.

Window comparisons connect differences between replicas to changes within them. Replica 1 has mean RMSDs of approximately 0.11445 nm in its first 500 ps and 0.17309 nm in its second 500 ps. Corresponding values are 0.11135 and 0.13834 nm for replica 2, and 0.17679 and 0.21434 nm for replica 3. All three have greater mean departures in the later interval, showing that early adjustment near the common reference still influences the full-window statistics. Replica 2 also changes in gyration radius, from about 1.19242 to 1.18329 nm. Time traces, window means, and blocking thus identify particular processes worth observing further.

These findings suggest a defined continuation. Extend the three existing branches while retaining the model and measurement definitions, then compare RMSD, gyration, and local structural observables in subsequent windows. Also prepare new repetitions from suitably separated, structurally different conformations to examine the influence of the common starting state. For a binding-pocket question, add pocket-specific distances or contacts so that sampling assessment addresses the functional process. A settled global size can coexist with slower local opening and closing, each requiring observation on its own scale.

The scope of uncertainty should match the scientific question. Changing random seeds mainly investigates thermal realizations and finite-time sampling. Changing a force field or protonation state investigates modelling assumptions. Changing the integration time step investigates numerical approximation. These comparisons change different inputs and produce different kinds of evidence. A clear account states what was measured under defined conditions, reports variation between replicas and windows, and places model comparisons within their corresponding designs. The next calculation then has an explicit role in adding a particular kind of information.

A biological macromolecule also interacts with solution composition, temperature, binding partners, and potentially chemical reactions. The present classical model describes conformational motion with fixed chemical identities and connectivity. Reactions, proton transfer, or bond scission require the corresponding model extensions. More precise sampling estimates improve knowledge of the current model’s average behaviour. Relating that behaviour to experimental function additionally requires correspondence between the experimental observable and the simulated measurement. Sampling design and model design jointly determine the question a curve can answer.

## Give output frequency, run duration, and replication separate jobs

Finally, isolate output frequency with a controlled correlation model. A length fluctuates around a fixed mean with a standard deviation of 0.01 nm, and correlations decay exponentially with the separation in time. The correlation time τc is the interval over which that exponential falls to about 37% of its initial value. This statistical model lets us calculate how much information denser output adds within a fixed observation duration. Because its mean and correlation law are specified, the variance of its average follows directly, without estimating an unknown correlation law from a short molecular trajectory.

Exponential correlation at fixed observation durationEq. 5

![Exponential correlation at fixed observation duration](https://ml-biomat.com/static/agent-math/0e3191cbd6d77715042820ff.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| C(k) | Correlation at lag k in the exponential model | 1 |
| δt, τc | Recording interval and exponential correlation time; the displayed exponential applies for τc>0 | ps |
| N, k | Record count and lag in records; Nδt=500 ps in this exercise | 1 |
| e | Base of the natural exponential, approximately 2.71828 | 1 |
| g_{N} | Multiplier of mean variance due to correlation | 1 |
| N_{eff} | Equivalent independent count for the variance of the mean; it may be non-integer | 1 |
| σₓ, SE | Standard deviation of one observation and standard error of the model mean | nm |
| 1−k/N, 2 | Finite-record pair weight and the contribution from both time directions | 1 |
| Σ, /, −, +, = | Summation over specified indices, division, subtraction, addition, and defining equality; adjacent factors multiply | Operators have no units |
| √, −kδt/τc | Nonnegative square root; the exponent is a dimensionless time separation | Operator and exponent have no units |

Reading the relationshipThe variance of the mean sums covariances of observation pairs. There are N−k pairs at each lag and a factor two for the two time directions.

A worked exampleFor τc=20 ps, δt=1 ps, N=500 and σₓ=0.01 nm, gN=38.40867, N_eff=13.01790 and SE=0.00277159 nm.

ConditionsAn analytical statistical model with constant mean and variance and known exponential correlation. The τc=0 option uses the independent limit C(k>0)=0; a real trajectory requires assessment of its correlation law.

In the equation, each lag receives a factor 1−k/N because only N−k pairs are available at separation k. Equivalent contributions in the positive and negative time directions give the factor two. The variance of each observation with itself supplies the initial one. Combining these terms gives gN, and the mean variance is the individual variance multiplied by gN/N. Defining N/gN as an effective independent count expresses equivalence in contribution to the variance of the mean. It can be non-integer; it is a statistical scale, not additional conformations inserted into a trajectory.

Observation window 0≤t<500 ps; single-observation SD σₓ=0.01 nm. Change spacing and correlation time to compare raw and effective counts.

[Figure: Exponential correlation and effective information](https://ml-biomat.com/tutorials/molecular-dynamics/g09/en/#en-s8)

Analytical exponential-correlation model over a fixed 500 ps window, with single-observation standard deviation 0.01 nm. Spacing changes record count; correlation time controls temporal similarity.

The interaction fixes the observation interval at 0≤t<500 ps while allowing correlation time and output spacing to change. With a 20 ps correlation time, reducing spacing from 1 to 0.5 ps doubles the number of records from 500 to 1,000 but barely changes the effective independent count, because the new observations are strongly related to existing ones. Setting correlation time to zero selects the independent-observation limit, where the effective count equals the record count. A slowly changing conformational trace has different statistical conditions from that limit. Its correlation law must be learned from adequate observations before an exponential model is adopted.

The complete program below reads three pairs of RMSD and gyration records, verifies a common 1 ps grid from zero through 1,000 ps, and applies the window, correlation, and blocking definitions used here. It writes three sets of plots and a structured summary: raw and cumulative traces, autocorrelation and block-length curves, and means for the first half, second half, and whole interval. The --language zh option changes labels while preserving numbers and selections. Begin with the supplied reference records, then use new records in the same replica-folder structure to examine what changes after additional observation.

### Complete Python: windows, correlation and blocks

```
"""Compare three protein trajectories at fixed measurement definitions.

python analyze_replicas.py --records records --out analysis --language en

Each records/replica-1, replica-2 and replica-3 contains rmsd.xvg and gyrate.xvg.
Dependencies: numpy, matplotlib. Time is ps and both observables are nm.
The plots display 0--1000 ps. Statistics use 0 <= t < 1000 ps: exactly 1000
equally spaced observations, divided into complete, disjoint blocks.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


def read_xvg(path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if text and not text.startswith(("#", "@")):
            rows.append([float(value) for value in text.split()])
    data = np.asarray(rows, dtype=float)
    if data.ndim != 2 or not np.all(np.isfinite(data)):
        raise ValueError(f"Expected finite two-dimensional data in {path.name}")
    return data


def autocorrelation(values, max_lag=200):
    """Pair-count covariance estimate, centered on this record's mean."""
    centered = values - values.mean()
    variance = np.mean(centered**2)
    if variance <= 0:
        raise ValueError("A constant record has no normalized fluctuation ACF")
    return np.array([np.dot(centered[:len(values)-lag], centered[lag:]) /
                     ((len(values)-lag)*variance)
                     for lag in range(max_lag+1)])


def block_estimates(values, block_sizes):
    rows = []
    for size in block_sizes:
        if len(values) % size:
            raise ValueError("Use complete equal-sized blocks for this exercise")
        means = values.reshape(-1, size).mean(axis=1)
        if len(means) < 2:
            raise ValueError("At least two block means are required")
        # This is an estimate based on treating block means as independent.
        # Plot its dependence on size before making that statistical assumption.
        sem = means.std(ddof=1) / np.sqrt(len(means))
        rows.append({"block_records": int(size), "blocks": int(len(means)),
                     "sem_nm": float(sem), "means_nm": means.tolist()})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, default=Path("records"))
    parser.add_argument("--out", type=Path, default=Path("analysis"))
    parser.add_argument("--language", choices=["zh", "en"], default="en")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    zh = args.language == "zh"
    def tr(cn, en): return cn if zh else en
    fonts = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC",
             "WenQuanYi Zen Hei", "DejaVu Sans"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    plt.rcParams.update({"font.family": [f for f in fonts if f in installed] if zh else ["DejaVu Sans"],
                         "font.size": 14, "axes.titlesize": 16, "svg.fonttype": "path",
                         "figure.facecolor": "#faf8f3", "axes.facecolor": "#faf8f3",
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.unicode_minus": False})
    colors = ["#167d84", "#be7045", "#4c6dab"]
    names = ["RMSD", "Rg"]
    block_sizes = [1, 2, 5, 10, 20, 25, 50, 100, 200]
    series, summaries, correlations = [], [], []
    reference_time = None
    for number in (1, 2, 3):
        folder = args.records / f"replica-{number}"
        rmsd = read_xvg(folder / "rmsd.xvg")
        gyrate = read_xvg(folder / "gyrate.xvg")
        time = rmsd[:, 0]
        if not (np.array_equal(time, gyrate[:, 0]) and
                np.allclose(time, np.arange(1001), rtol=0, atol=1e-9)):
            raise ValueError("Both measurements must have the same 0--1000 ps grid")
        if reference_time is None:
            reference_time = time.copy()
        if not np.array_equal(time, reference_time):
            raise ValueError("Replica time grids differ")
        values = np.column_stack([rmsd[:, 1], gyrate[:, 1]])
        series.append(values)
        selected = values[:-1]
        record = {"replica": number, "samples": len(selected), "observables": {}}
        acfs = []
        for column, name in enumerate(names):
            data = selected[:, column]
            acfs.append(autocorrelation(data))
            record["observables"][name] = {
                "mean_nm": float(data.mean()), "frame_sd_nm": float(data.std(ddof=1)),
                "independent_frame_sem_nm": float(data.std(ddof=1)/np.sqrt(len(data))),
                "first_half_mean_nm": float(data[:500].mean()),
                "second_half_mean_nm": float(data[500:].mean()),
                "blocks": block_estimates(data, block_sizes)}
        correlations.append(np.array(acfs))
        summaries.append(record)
    series = np.array(series)
    summary = {"window_ps": [0, 1000], "right_endpoint_in_statistics": False,
               "record_interval_ps": 1, "replica_count": 3, "replicas": summaries,
               "replica_mean_summary": {},
               "interpretation": "Finite-window estimates conditional on a common prepared coordinate state. Block-size curves and ACF are sampling diagnostics; block independence is assessed, not imposed by dividing data."}
    for column, name in enumerate(names):
        means = series[:, :-1, column].mean(axis=1)
        summary["replica_mean_summary"][name] = {
            "grand_mean_nm": float(means.mean()), "between_replica_sd_nm": float(means.std(ddof=1)),
            "conditional_sem_nm": float(means.std(ddof=1)/np.sqrt(3))}
    (args.out / "replica_summary.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    np.savetxt(args.out / "replica_series.csv", np.column_stack([time, *[x for x in series]]),
               delimiter=",", header="time_ps,r1_RMSD_nm,r1_Rg_nm,r2_RMSD_nm,r2_Rg_nm,r3_RMSD_nm,r3_Rg_nm", comments="")

    def save(fig, basename):
        for extension in ("svg", "png"):
            fig.savefig(args.out / f"{basename}.{extension}", dpi=170, bbox_inches="tight")
        plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(14, 9), layout="constrained")
    for column, name in enumerate(names):
        for number, color in enumerate(colors):
            label = tr(f"副本 {number+1}", f"Replica {number+1}")
            axes[column, 0].plot(time, series[number, :, column], color=color, lw=.8, alpha=.85, label=label)
            running = np.cumsum(series[number, :-1, column])/np.arange(1, 1001)
            axes[column, 1].plot(time[:-1], running, color=color, lw=1.8, label=label)
        axes[column, 0].set(title=tr("逐帧记录", "Frame-by-frame record"), ylabel=f"{name} / nm")
        axes[column, 1].set(title=tr("从生产起点累计的平均", "Mean accumulated from production start"), ylabel=f"{name} / nm")
        for ax in axes[column]:
            ax.set_xlabel(tr("生产时间 / ps", "Production time / ps"))
            ax.set_xlim(0, 1000)
            ax.grid(alpha=.15)
            ax.legend(frameon=False, fontsize=12)
    save(fig, "replica_traces")

    fig, axes = plt.subplots(2, 2, figsize=(14, 9), layout="constrained")
    for column, name in enumerate(names):
        for number, color in enumerate(colors):
            label = tr(f"副本 {number+1}", f"Replica {number+1}")
            axes[column, 0].plot(np.arange(201), correlations[number][column], color=color, label=label)
            errors = [item["sem_nm"] for item in summaries[number]["observables"][name]["blocks"]]
            axes[column, 1].plot(block_sizes, errors, "o-", color=color, ms=5, label=label)
        axes[column, 0].axhline(0, color="#879896", lw=.8)
        axes[column, 0].set(xlabel=tr("时间间隔 / ps", "Lag / ps"), ylabel="C(k)",
                            title=tr(f"{name} 的中心化自相关", f"Centered autocorrelation of {name}"), xlim=(0, 200))
        axes[column, 1].set(xscale="log", xlabel=tr("每块长度 / ps", "Block duration / ps"),
                            ylabel=tr("按块均值计算的标准误差 / nm", "Block-based standard error / nm"),
                            title=tr(f"{name}：每块 1 至 200 个记录", f"{name}: 1 to 200 records per block"))
        for ax in axes[column]:
            ax.grid(alpha=.15)
            ax.legend(frameon=False, fontsize=12)
    fig.suptitle(tr("0≤t<1000 ps；200 ps一块时仅有5块", "0≤t<1000 ps; a 200 ps block leaves only five blocks"), fontsize=17)
    save(fig, "replica_correlation")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), layout="constrained")
    for column, name in enumerate(names):
        for number, color in enumerate(colors):
            record = summaries[number]["observables"][name]
            x = number+1
            axes[column].plot([x-.18, x+.18], [record["first_half_mean_nm"], record["second_half_mean_nm"]], color=color, alpha=.7)
            axes[column].scatter(x-.18, record["first_half_mean_nm"], color=color, marker="<", s=90)
            axes[column].scatter(x+.18, record["second_half_mean_nm"], color=color, marker=">", s=90)
            axes[column].scatter(x, record["mean_nm"], color=color, edgecolor="white", s=130, zorder=3)
        axes[column].set(xlim=(.5, 3.5), xticks=[1, 2, 3], xlabel=tr("独立随机副本", "Random realization"),
                         ylabel=f"{name} / nm", title=tr("前段、全段与后段的均值", "First half, full window,\nand second half"))
        axes[column].grid(axis="y", alpha=.15)
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], color="#445e61", marker=marker, linestyle="None", markersize=9, label=label)
               for marker, label in [("<", "0≤t<500 ps"), ("o", "0≤t<1000 ps"), (">", "500≤t<1000 ps")]]
    fig.legend(handles=handles, loc="outside lower center", ncols=3, frameon=False)
    save(fig, "replica_windows")
    print(json.dumps(summary["replica_mean_summary"], indent=2))


if __name__ == "__main__":
    main()
```

Read rmsd.xvg and gyrate.xvg in three replica directories; --language zh or en selects figure labels.

Plan the next simulation by separating three investments. More frequent output resolves faster changes. Longer trajectories reveal slower adjustment and transitions. More independent repetitions reveal variation on restarting. If output is already dense but the blocking curve continues rising, extending observation of the relevant structural process is a more targeted investment. If distinct initial conformations remain in different regions, expand sampling around those regions and examine their exchange using the research observable. The useful budget follows the missing information rather than the size of the trajectory file.

Protein–ligand complexes, nucleic acids, carbohydrates, and membranes all use the same reasoning. Replacing global size with a contact, glycosidic torsion, or membrane thickness changes the measurement definition, characteristic correlation, and suitable unit of replication. Clear objects and units, preserved time order, and comparisons across windows and branches connect a plotted curve to the motion it records. That foundation supplies a consistent scale for the more complex molecular models and sampling methods developed in the following lessons.

## Further Reading and Open Materials

- [Molecular dynamics simulation of a small protein using GROMACS](https://tutorials.gromacs.org/docs/md-intro-tutorial.html) · GROMACS tutorial contributors · CC BY 4.0

  Protein-in-water preparation, production and RMSD/Rg workflow.

  Use three random realizations of the common 1UBQ model and add matched windows, correlation and blocking.
- [From Proteins to Perturbed Hamiltonians: A Suite of Tutorials for the GROMACS-2018 Molecular Simulation Package](https://github.com/jalemkul/gmx_tutorials_livecoms) · Justin A. Lemkul · CC BY 4.0

  Protein-in-water simulation and structural analysis workflow, including interpretation of RMSD.

  Ubiquitin replaces the original protein; a common reference and selection are fixed, with statistical explanations and actual replicate comparisons added.
- [gmx analyze — GROMACS 2026.4 documentation](https://manual.gromacs.org/2026.4/onlinehelp/gmx-analyze.html) · GROMACS developers · Official technical reference; command conventions cited

  Equally spaced records, autocorrelation and block-error definitions.

  Implement the displayed formulas in newly written Python and display block-length dependence.
- [Error estimates on averages of correlated data](https://doi.org/10.1063/1.457480) · H. Flyvbjerg and H. G. Petersen · Historical research citation; publisher copyright

  Historical context for correlated averages and blocking in 1989.

  A newly drawn adjacent-averaging diagram explains changes in the statistical unit.
- [Best Practices for Quantification of Uncertainty and Sampling Quality in Molecular Simulations [Article v1.0]](https://doi.org/10.33011/livecoms.1.1.5067) · Alan Grossfield, Paul N. Patrone, Daniel R. Roe, Andrew J. Schultz, Daniel W. Siderius and Daniel M. Zuckerman · Publicly accessible methodological article cited; no article text, code or illustration reproduced

  Sampling diagnostics, uncertainty in means and the statistical scope of replicas sharing an initial state.

  Apply the concepts to actual short trajectories with new explanations and diagrams for subsequent sampling design.
