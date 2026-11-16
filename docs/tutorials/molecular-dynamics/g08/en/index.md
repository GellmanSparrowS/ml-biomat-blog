# Reading protein motion from a trajectory

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g08/en/
Language: en

Separate overall motion, internal deformation, and local fluctuations, then read RMSD, radius of gyration, and RMSF from an actual ubiquitin trajectory.

## One molecular movie, three different questions

Imagine sliding a folded umbrella across a table, turning it through half a revolution, and then opening its canopy. All three actions change where parts of the umbrella appear, but they change different things. Sliding and turning preserve the distances between its parts; opening it changes the internal shape. A protein in water also undergoes several kinds of motion at once. The molecule translates and changes orientation, while loops, termini, and side chains move relative to one another. Combining every coordinate change into one number would mix the distance traveled through the solution with changes inside the protein. The first step in trajectory analysis is therefore to state the question precisely enough to choose a measurement.

The previous lesson prepared a 76-residue ubiquitin molecule in water and recorded 1 ns of motion without protein position restraints. We continue with the first of those trajectories. It contains a saved frame every 1 ps, giving 1001 frames from 0 to 1000 ps. Time zero is the beginning of production, after the temperature and pressure preparation stages. We will ask how far the protein has moved from a common minimized reference structure, how widely its mass is distributed in space, and which positions along its chain fluctuate most during the observation. The corresponding measurements are root-mean-square deviation, RMSD; radius of gyration, Rg; and root-mean-square fluctuation, RMSF.

Each measurement serves a different biological question. Studying whether a mutation changes the mobility of a loop requires locating motion within the structure. Studying whether a chain extends more in one solution than another requires a measure of spatial size. Following departure from an experimental starting conformation requires a fixed structural reference. What a curve can tell us depends on the selected atoms, the motions retained in the analysis, and the duration observed. Specifying those choices gives subsequent comparisons of salt concentration, temperature, or molecular composition a shared ruler.

Think of a trajectory as a three-dimensional photo album arranged in time. Every page stores positions, but its page number does not identify a new, independent conformation or certify that a distribution has been thoroughly sampled. Neighboring pages are usually similar because little time separates them. Some motions occur within picoseconds, while others take much longer than the 1 ns available here. We first learn to extract reproducible geometrical measurements from the pages. The next lesson will examine how much independent information those measurements contain, keeping the geometrical and statistical questions clearly connected.

There is also a practical objective. You will be able to use GROMACS for standard analysis and follow a Python calculation that recomputes the same quantities directly from coordinates. Both routes use the same atoms, units, and reference, so their results can be compared. A number in an output file then has a traceable calculation behind it. Producing a plot becomes part of establishing a measurement for a particular question.

The saving interval determines how rapidly a change can be represented in this album. A 1 ps interval resolves the slower conformational changes discussed here, while the XTC file contains only the sampled coordinates between which the program has continued integrating. Lines connecting plotted observations help the eye follow their order, and the speed of an animation is set by its playback controls. Both differ from the physical time that elapsed in the simulation. To discuss the rate of a molecular motion, return to the recorded timestamps and an appropriate time-dependent analysis.

## Reconstruct the protein across periodic boundaries

Periodic boundaries provide an environment around a finite water box, but their coordinate representation can make a molecular movie misleading. A chain extending beyond the right side of a box may have its remaining atoms displayed on the left, where an equivalent periodic image lies. The screen then appears to show two pieces, even though the chemical topology still connects them. A world map cut along a meridian offers a useful analogy: neighboring places can appear at opposite edges of the sheet. Their separation on the page changes, while their geographical relationship remains. Molecular shape calculations likewise need a continuous image consistent with the chemical bonds.

GROMACS can use the topology and cell vectors to reconstruct whole molecules in each frame. Here, `gmx trjconv -pbc mol -center` processes the production trajectory. Protein is selected as the centering group, and System as the group written to the output. Reconstructing and centering have different purposes. Reconstruction makes the periodic images consistent with molecular connectivity; centering moves the object to a convenient display position. Writing System retains protein, water, and ions together, so solvent-related selections remain available for later analyses.

[Figure: Periodic boundaries and a whole molecule](https://ml-biomat.com/tutorials/molecular-dynamics/g08/en/#en-s2)

Figure 1 · Periodic-image schematic. Selecting consistent images along chemical bonds reconstructs a continuous molecule; centering then changes the molecule’s displayed position.

Why does reconstruction matter for radius of gyration? Consider neighboring atoms separated physically by 0.15 nm but represented near opposite boundaries. A direct Euclidean distance between their stored coordinates could be several nanometers. The center calculated from these split coordinates can also move to an inappropriate position, making the molecule appear much larger. Reconstructing it before measuring internal distances restores consistency between geometry and chemical connectivity. For this finite, single-chain protein, the molecular bonds provide a clear basis for selecting the appropriate images.

Reconstruction for shape analysis also differs from following continuous diffusion. As a protein travels through water, its center may cross the box boundary repeatedly. Moving it back to the center of every displayed frame makes a readable movie, but removes its accumulated displacement from that representation. Measuring center-of-mass diffusion requires following the continuous motion across boundaries. Measuring internal shape instead calls for removing an irrelevant overall position. Our present question concerns conformation, so we use a whole, centered protein and then decide separately whether each observable needs rotational fitting. A transport question should start from the retained raw trajectory and use the corresponding treatment.

Looking at the beginning, middle, and end of a processed trajectory is often more informative than trusting a smooth curve immediately. Check that the chain is continuous, that it does not suddenly become a long line across the cell, and that the selected atom count stays constant. Confirm that the output still spans 0–1000 ps. Covalently periodic chains, multimolecular assemblies, and membranes introduce additional geometrical choices, which later lessons will address. The principle remains the same: the coordinate representation must describe the physical object whose property is being measured.

## Place two structures in a common coordinate frame

Place two transparent drawings of the same shape on top of each other. A small shift or rotation of one sheet prevents their points from overlapping, so point-to-point distances include the placement of the paper. Comparing internal protein shapes requires the equivalent of placing both drawings in a common frame. Usually, the selected centers are first superimposed, followed by a rigid rotation that minimizes the sum of squared differences between corresponding atoms. A rigid transformation preserves every internal distance within either structure. It removes a difference in overall pose while retaining internal deformation.

In 1976, Wolfgang Kabsch published a solution for the best rotation relating two corresponding sets of points, allowing the points to carry different weights. The same geometrical question arises when comparing experimental structures, superimposing protein conformations, and analyzing trajectories: which points correspond, and how should the entire object be turned to separate shape from viewing orientation? The method remains useful across applications because its mathematical target is precise. In the illustration, differences between the teal and orange point sets that remain after rigid superposition are the differences carried forward into structural comparison.

[Figure: Separate structural comparison from viewing orientation](https://ml-biomat.com/tutorials/molecular-dynamics/g08/en/#en-s3)

Figure 2 · Kabsch’s 1976 work determined an optimal rotation from weighted squared deviations. The diagram relates atom correspondence, rigid superposition, and residual deformation.

Correspondence comes from chemical identity. The Cα atom of residue 10 should match that same atom in the reference, rather than whichever carbon happens to be nearest in space. Deleting residues, reordering atoms, or joining different molecules can require an explicit mapping before comparison. Here, the reference and trajectory share the same topology and workflow, preserving atom order. We choose the backbone N, Cα, and carbonyl C atoms, 228 in total, both for fitting and for the RMSD measurement. This focuses the analysis on the peptide skeleton instead of allowing every mobile side-chain end to contribute to the summary.

The fitting and measurement groups can also differ. To study a flexible loop projecting from a protein, one can use a relatively stable core to establish orientation and then measure the loop in that frame. The result describes movement of the loop relative to the core. If the whole protein defines the fit, the moving loop helps determine the optimal orientation, changing how the residual differences are distributed. These choices answer different questions. We initially use the same backbone group twice to keep the definition transparent; a specific local question can later motivate a more selective frame.

A two-dimensional alignment example with four equal masses. Change position and angle, then deform the upper-right point and compare three treatments.

[Figure: Four-point alignment](https://ml-biomat.com/tutorials/molecular-dynamics/g08/en/#en-s3)

A two-dimensional, equally weighted four-point geometry. Rigid translation and rotation preserve internal distances; moving one point leaves deformation after fitting.

The four-point interaction builds an intuition for this operation. With local deformation set to zero, changing translation or angle changes the deviation of the raw coordinates, while a complete rigid fit brings the deviation back to zero. Matching the centers alone leaves the contribution from rotation. Moving the upper-right point then produces a nonzero fitted deviation because a rigid transformation cannot restore altered internal distances. These points have equal weights; the protein analysis uses mass weights where specified. The small geometry isolates the role of fitting before the same operation appears inside a longer molecular calculation.

## RMSD: how far a structure has moved from a reference

After fitting, every selected atom has a displacement from its matched reference position. Displacements have direction: some point left, others right. Simply averaging their signed components could cancel substantial movements. RMSD instead squares the length of each displacement, averages over the atoms with the selected weights, and takes a square root. The result is one nonnegative length summarizing structural differences. These three operations—square, average, and square root—explain the name root-mean-square deviation.

Mass-weighted RMS deviation after fittingEq. 1

![Mass-weighted RMS deviation after fitting](https://ml-biomat.com/static/agent-math/a7ab7931514980b82c13aae2.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| RMSD(t) | Root-mean-square deviation of the frame at t from the reference | nm |
| t | Production time of the saved frame | ps |
| i, N | Atom index and selected atom count; N=228 for the backbone here | 1 |
| mᵢ | Mass assigned to atom i by the topology | u |
| r̃ᵢ(t), rᵢʳᵉᶠ | Current coordinate after rigid translation and rotation, and the matched atom’s fixed reference coordinate; bold type denotes a 3D vector | nm |
| Σᵢ₌₁ᴺ | Sum over atoms 1 through N; the denominator is their total mass | The summation operator has no unit; the denominator mass is in u |
| ‖·‖² | Squared vector length: the sum of three squared coordinate differences | nm² |
| √, /, −, =, × | Nonnegative square root, division, subtraction, defining equality, and multiplication; the square root converts mean squared deviation from nm² to nm | Operators have no units |
| mᵢ‖·‖² | Mass times the atom’s squared distance, one term in the numerator | u nm² |

Reading the relationshipRemove shared translation and rotation, then combine selected atomic deviations into one length. Squaring prevents cancellation between opposite directions; mass weighting matches this gmx rms calculation.

A worked exampleIf two equally weighted atoms have post-fit distances of 0.10 and 0.20 nm from their matched references, the result is √[(0.10²+0.20²)/2]=0.1581 nm. These are distances after a specified fit, rather than two coordinates to fit again.

ConditionsCompare values at fixed atom correspondence, reference, fitting group, measurement group, and weights. Here both fitting and measurement use the 228 N, Cα, and C atoms, against the common minimized structure.

We use mass weighting, consistent with `gmx rms -mw`. Backbone N, Cα, and C atoms do not all have the same mass, so heavier atoms receive more weight in the sum. Division by the total selected mass normalizes it. Mass units cancel between numerator and denominator; coordinates are in nm, leaving RMSD in nm. Equal weighting also defines a useful geometrical measurement, provided the calculation and interpretation both adopt it. When comparing analysis packages, checking their weights is more useful than merely comparing the last few digits of their outputs.

The reference here is the minimized structure shared by all three independent simulation branches. It is a common ruler, and it differs from the first production frame. Before production, that frame has already undergone 100 ps of restrained NVT and 200 ps of restrained NPT preparation. Small adjustments therefore give it an RMSD of approximately 0.0218 nm from the minimized reference. Choosing the first production frame as a new reference would make its own deviation zero and alter the subsequent curve. Each choice describes departure from a different structure. Keeping the shared reference supports the replicate comparison in the next lesson.

What does a value such as 0.15 nm mean? It equals 1.5 Å, but it summarizes mass-weighted displacements of 228 fitted backbone atoms; individual atoms can move by different amounts. A few large displacements and many small displacements can produce similar RMSD values. A modest rotation around a hinge can also create a large movement at a distant end of the molecule. To interpret the result, locate changes in the structure and connect them to local contacts, secondary structure, or distances relevant to the scientific question.

The present curve rises early, reaches larger deviations during the middle of the record, and decreases again near its end. Its time ordering identifies when these changes occur. Averaging the complete record summarizes overall departure within the window, while hiding the sequence of events. The later figure retains the complete trace alongside information about local fluctuations. Examining what happens in the structure before selecting a statistical summary helps turn the curve into an explanation.

A reference is also like the starting city of a journey. Two other cities can both be 100 km from it without being close to one another. Likewise, two frames with the same RMSD can have different conformations. Returning to an earlier RMSD value calls for structural superposition or additional features to determine whether the earlier state has returned. If distinguishing conformational groups is central to the study, a frame-to-frame distance matrix and physically motivated local variables provide further information. This geometrical observation helps us use the one-dimensional curve as a concise summary while preserving the richer structural question behind it.

## Radius of gyration: the size of a mass distribution

Coil a flexible cable into a compact bundle, then loosen some of its loops. Its total mass stays the same, while that mass becomes more widely distributed. Radius of gyration measures this spatial spread. It locates the selected atoms’ center of mass, measures each atom’s distance from that center, and calculates a mass-weighted root mean square. Atoms farther from the center contribute larger squared distances. Unlike RMSD, the measurement requires no external reference structure: every frame supplies its own center.

Center of mass and mass-weighted radius of gyrationEq. 2

![Center of mass and mass-weighted radius of gyration](https://ml-biomat.com/static/agent-math/2b008944c37a86dc9e5d53d2.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| r_{cm} | Center-of-mass coordinate of the selected atoms in this frame; cm denotes center of mass | nm |
| R_{g} | Root-mean-square distance from the center of mass; g denotes gyration | nm |
| i, N | Selected atom index and count; N=1231 for the entire protein | 1 |
| mᵢ, rᵢ | Mass and current three-dimensional coordinate of atom i | u; nm |
| Σ, /, −, = | Summation; normalization by total mass; subtraction of this frame’s center of mass; equality defining the quantities | 1 |
| ‖·‖² | Squared distance of an atom from the center of mass | nm² |
| √ | Nonnegative square root; taking the square root of nm² gives nm | Operator has no unit |
| mᵢrᵢ | Mass times coordinate, one numerator term in the center of mass | u nm |
| mᵢ‖·‖² | Mass times squared distance from the center of mass | u nm² |

Reading the relationshipThe center of mass removes translation. Distances around it describe the spatial spread of mass. Rotation preserves these distances, so scalar Rg needs no fit to another structure.

A worked exampleFor two equal masses at −1 and +1 nm on a line, the center of mass is zero and Rg=1 nm. Moving both to 4 and 6 nm shifts the center to 5 nm while Rg remains 1 nm.

ConditionsThe selected mass distribution of a whole molecule; make the molecule whole across periodic boundaries first. Rg measures a distribution’s extent, rather than a surface radius or the size of the solution box.

The center of mass is the position about which the selected mass distribution balances. It is not generally the midpoint of the coordinates, because atoms can have different masses. Familiar geometric centers coincide with centers of mass for suitable symmetric, uniformly distributed objects. A protein contains different elements arranged unevenly, so using the masses in its topology gives a direct definition. Here, Protein includes all 1231 protein atoms, including hydrogens. Water and ions influence the dynamics as the surrounding solution, while this particular size measurement concerns the protein itself.

Translating a complete protein moves every atom and its center together, preserving their relative distances. Rotating it also preserves those distances. Scalar Rg is therefore naturally insensitive to overall translation and rotation. Periodic reconstruction still matters, because coordinates split across opposite boundaries fail to represent one continuous molecular geometry. This distinction is useful in practice: Rg needs a whole molecule but does not need a pose fitted to a separate reference. Each processing step addresses a particular geometrical requirement.

[Figure: Three lengths, three measurement baselines](https://ml-biomat.com/tutorials/molecular-dynamics/g08/en/#en-s5)

Figure 3 · Conceptual comparison: RMSD uses matched reference positions, Rg measures the spatial spread of mass in one frame, and RMSF measures an atom’s fluctuations around its own mean across frames.

The word radius can suggest the surface of a sphere. For a protein, Rg is an average scale of a mass distribution, whose surface rarely forms such a sphere. Different shapes can have the same Rg. A relatively rounded bundle and a flatter one may give identical mass-weighted mean squared distances from their centers. Distinguishing extension, flattening, and directionality calls for more detailed quantities such as principal axes of a gyration or inertia tensor. Asking whether a molecule can pass through a pore requires the relevant cross-section and conformations. Scalar Rg is a useful starting point for separating the overall size question from those more detailed shape questions.

Across the present window, the mean Rg is approximately 1.19153 nm, with a saved-frame standard deviation of 0.00603 nm. RMSD shows more pronounced changes between periods of the same trajectory. The two measurements illustrate how the spatial extent of mass can remain similar while internal positions rearrange relative to a reference. A cable bundle can change its internal arrangement within a broadly similar outline. The later scatter plot places the RMSD and Rg of each frame together, making this distinction directly visible.

## RMSF: motion around each position’s own time average

Now move attention from the time axis to the protein sequence. RMSD provides one value per frame and describes structural departure over time. RMSF gathers positions of one atom across many frames and asks how widely that location moves. Imagine filming a tree, aligning its trunk between images, and observing the range of positions visited by each branch tip. Each tip has its own mean position and a spread around that center. Protein RMSF similarly measures motion around each atom’s time-averaged position after a specified structural fit.

Time mean and RMS fluctuation of one positionEq. 3

![Time mean and RMS fluctuation of one position](https://ml-biomat.com/static/agent-math/8030f8d29f932ff6a231f387.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| i | Index of the atom being examined; here one Cα per residue | 1 |
| j, M | Frame index and frame count; M=1001 across 0–1000 ps | 1 |
| tⱼ | Production time of frame j; subscript j identifies frames | ps |
| r̃ᵢ(tⱼ) | Atomic coordinate in frame j after the specified rigid fit | nm |
| r̄ᵢ | Time average of the selected fitted coordinates; the overbar denotes averaging | nm |
| RMSFᵢ | Root-mean-square displacement of atom i around its own time-mean position | nm |
| Σⱼ₌₁ᴹ, 1/M, −, √, =, × | Sum over frames, equal-frame averaging, subtraction of the atom’s own mean, nonnegative square root, defining equality, and multiplication; the square root converts nm² to nm | Operators and averaging weights have no units |
| ‖·‖² | Squared distance of this frame’s coordinate from its own time-mean position | nm² |

Reading the relationshipFirst locate an atom’s average position over the observation window, then measure the spread around that position. One value per atom yields a spatial profile along the residue sequence.

A worked exampleFor one fitted coordinate taking −0.10, 0, and +0.10 nm over three frames, the mean is zero and RMSF=√[(0.01+0+0.01)/3]=0.08165 nm. The denominator is three because this is the mean squared displacement of these three frames.

ConditionsHere all 76 Cα atoms define the fit and each Cα RMSF uses the entire 1 ns window. Changing the time window or fitting region changes both the mean positions and the measured fluctuations.

We select one Cα per residue, giving 76 atoms. Cα lies in the amino-acid backbone and provides a convenient representative position along the chain. All 76 Cα atoms determine each frame’s fitted pose, after which the mean position and RMSF of each Cα are calculated. The horizontal axis can then use residue number, with nm on the vertical axis. This fitting group differs from the 228-atom backbone group used for RMSD. Each has an explicit definition; comparisons of a given observable across conditions should preserve that observable’s definition.

The reference structure helps establish the common coordinate frame for RMSF, while the center inside the fluctuation formula is each atom’s own time mean. Consider an atom that moves to a new position and then vibrates narrowly around it. Its deviation from an older reference can be large, yet its RMSF during the later interval can be small. Including both the earlier and later positions in one averaging window increases the spread. The observation window is therefore part of the measurement. Its endpoints belong alongside the fitting specification when recording the analysis.

Over this 1 ns window, the C-terminal Gly76 and Gly75 have Cα RMSF values of approximately 0.4845 and 0.3078 nm. Their neighbors Arg74 and Leu73 also fluctuate more than many core positions. This spatial profile suggests a specific next observation: inspect how the tail moves and what contacts it maintains with water and the protein surface. The terminus is part of the protein, and its local mobility can coexist with a compact main body. Connect the high values to their structural locations to understand the motion they describe.

The experimental B factors discussed in Lesson 05 also concern positional distributions, but their environment, structural refinement, and contributions from disorder differ from those of this solution trajectory. Here the quantity is the fitted coordinate fluctuation under a specified force field, temperature, solvent model, and observation window. Quantitative experimental comparison requires connecting the relevant observable, crystal or solution environment, timescale, and theoretical relationship. The present profile first supports comparisons between locations within this trajectory and identifies residues for closer inspection.

RMSF describes the width of a position distribution; the speed of motion requires further time information. A terminus switching slowly between two locations and one moving rapidly through a similar range can have comparable RMSF. Displacement time series, contact lifetimes, or correlation functions help distinguish these cases. This is why the local fluctuation profile and molecular movie work together: the profile locates active regions, while the temporal record reveals how that activity unfolds.

The RMSF expression takes a direct mean over the M saved frames, giving the denominator M. When describing the spread of a scalar time trace elsewhere in the program, we use the sample-standard-deviation convention, with the number of frames minus one in the denominator. These operations follow their respective definitions of positional fluctuation and scalar spread. Neighboring observations are also correlated, so this small denominator distinction does not calculate the uncertainty of a mean. Time blocks and independently initialized replicas will provide the next steps in that statistical interpretation.

## Turn the trajectory into readable figures with complete programs

The following script makes the processing order executable. Its inputs are the production topology `md.tpr`, the production coordinates `md.xtc`, and the shared minimized reference `reference.tpr`. TPR provides atomic identities and masses, while XTC provides coordinates saved through time. The script first creates a whole, centered trajectory and then calls the RMSD, radius-of-gyration, and RMSF tools. Each selection appears next to its command, making the fitting and measurement groups visible in the workflow.

### Reconstruct the trajectory and calculate three observables

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
python=${PYTHON:-python}
# Run beside md.tpr, md.xtc, and the common minimized reference.tpr.
printf 'Protein\nSystem\n' | "$gmx" trjconv \
  -s md.tpr -f md.xtc -o md-whole.xtc -pbc mol -center
printf 'Backbone\nBackbone\n' | "$gmx" rms \
  -s reference.tpr -f md-whole.xtc -o rmsd.xvg -fit rot+trans -mw
"$gmx" gyrate -s md.tpr -f md-whole.xtc -o gyrate.xvg \
  -sel 'group "Protein"' -mode mass
printf 'C-alpha\n' | "$gmx" rmsf \
  -s reference.tpr -f md-whole.xtc -o rmsf.xvg -res -fit
"$python" analyze_motion.py . --language en --output motion-analysis-en
"$python" analyze_motion.py . --language zh --output motion-analysis-zh
```

Run beside md.tpr, md.xtc, the common reference.tpr, and analyze_motion.py. Protein defines the centering group and System the output group; the two Backbone selections define fitting and measurement groups.

The two Backbone answers serve different purposes. The first chooses atoms used to find the best translation and rotation; the second chooses atoms whose deviation is reported. We use the same group for both. The gyration command selects Protein and explicitly uses mass weighting. The fluctuation command selects C-alpha, requests residue-based output, and enables fitting. The first two outputs are indexed by production time, whereas the third is indexed by residue. Preserving that distinction when reading files prevents a spatial profile from being mistaken for a time series.

The Python program reads the same TPR and the processed XTC, then constructs its backbone selection with explicit atom names. Here, `protein and name N CA C` matches the GROMACS Backbone group. Convenient selection names can have slightly different definitions across programs; writing their composition explicitly makes the correspondence inspectable. The program checks for 228 backbone atoms, 76 Cα atoms, and 1231 protein atoms. A different protein needs corresponding updated counts. Such checks connect the molecular identity to the calculation and reveal a selection mismatch early.

### Recompute, compare, and plot actual coordinates

```
"""Read a protein trajectory, recompute structural observables, and plot them."""
import argparse
import json
from pathlib import Path

import MDAnalysis as mda
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


def read_xvg(path):
    rows = [line.split() for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith(("#", "@"))]
    return np.asarray(rows, dtype=float)


def fit_positions(mobile, reference, masses):
    """Weighted proper rotation; coordinates are rows, with equal atom order."""
    w = masses / masses.sum()
    x = mobile - np.sum(w[:, None] * mobile, axis=0)
    y = reference - np.sum(w[:, None] * reference, axis=0)
    left, singular_values, right = np.linalg.svd((w[:, None] * x).T @ y)
    correction = np.eye(3)
    correction[-1, -1] = np.linalg.det(left @ right)
    rotation = left @ correction @ right
    return x @ rotation, y


def describe(values):
    return {"mean": float(values.mean()), "sample_sd": float(values.std(ddof=1)),
            "min": float(values.min()), "max": float(values.max())}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("directory", type=Path, help="Contains reference.tpr, md-whole.xtc and XVG files")
    p.add_argument("--output", type=Path, default=Path("motion-analysis"))
    p.add_argument("--language", choices=("zh", "en"), default="en")
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    ref = mda.Universe(str(a.directory / "reference.tpr"))
    traj = mda.Universe(str(a.directory / "reference.tpr"),
                        str(a.directory / "md-whole.xtc"))
    backbone = traj.select_atoms("protein and name N CA C")
    ca = traj.select_atoms("protein and name CA")
    protein = traj.select_atoms("protein")
    assert (len(backbone), len(ca), len(protein)) == (228, 76, 1231)
    ref_bb = ref.atoms[backbone.indices].positions.astype(float) / 10
    ref_ca = ref.atoms[ca.indices].positions.astype(float) / 10
    times, rmsd, rg, fitted_ca = [], [], [], []
    for ts in traj.trajectory:
        bb, target = fit_positions(backbone.positions.astype(float) / 10,
                                   ref_bb, backbone.masses)
        rmsd.append(np.sqrt(np.average(np.sum((bb-target)**2, axis=1),
                                       weights=backbone.masses)))
        xyz = protein.positions.astype(float) / 10
        center = np.average(xyz, axis=0, weights=protein.masses)
        rg.append(np.sqrt(np.average(np.sum((xyz-center)**2, axis=1),
                                     weights=protein.masses)))
        fitted, _ = fit_positions(ca.positions.astype(float) / 10, ref_ca, ca.masses)
        fitted_ca.append(fitted)
        times.append(ts.time)
    times, rmsd, rg, fitted_ca = map(np.asarray, (times, rmsd, rg, fitted_ca))
    mean_ca = fitted_ca.mean(axis=0)
    rmsf = np.sqrt(np.mean(np.sum((fitted_ca-mean_ca)**2, axis=2), axis=0))
    native_rmsd = read_xvg(a.directory / "rmsd.xvg")
    native_rg = read_xvg(a.directory / "gyrate.xvg")
    native_rmsf = read_xvg(a.directory / "rmsf.xvg")
    assert len(times) == 1001 and np.allclose(times, np.arange(1001))
    assert np.allclose(times, native_rmsd[:, 0]) and np.allclose(times, native_rg[:, 0])
    differences = {
        "rmsd_nm": float(np.max(np.abs(rmsd-native_rmsd[:, 1]))),
        "rg_nm": float(np.max(np.abs(rg-native_rg[:, 1]))),
        "rmsf_nm": float(np.max(np.abs(rmsf-native_rmsf[:, 1])))}
    assert differences["rmsd_nm"] < 2e-5
    assert differences["rg_nm"] < 2e-5
    assert differences["rmsf_nm"] < 6e-5  # Native RMSF is printed to four decimals.
    largest = np.argsort(rmsf)[-5:][::-1]
    summary = {
        "n_frames": len(times), "time_ps": [float(times[0]), float(times[-1])],
        "selection_counts": {"backbone": len(backbone), "C_alpha": len(ca), "protein": len(protein)},
        "native_rmsd_nm": describe(native_rmsd[:, 1]),
        "native_rg_nm": describe(native_rg[:, 1]),
        "python_minus_native_max_abs": differences,
        "highest_C_alpha_rmsf": [{"residue": int(ca.resids[i]), "name": str(ca.resnames[i]),
                                  "rmsf_nm": float(rmsf[i])} for i in largest],
        "windows": {str(start): {"rmsd_nm": describe(native_rmsd[(times >= start) & (times < start+200), 1]),
                                  "rg_nm": describe(native_rg[(times >= start) & (times < start+200), 1])}
                    for start in range(0, 1000, 200)}}
    (a.output / "motion_summary.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    np.savetxt(a.output / "motion_recomputed.csv", np.column_stack((times, rmsd, rg)),
               delimiter=",", header="time_ps,backbone_rmsd_nm,protein_rg_nm", comments="")
    np.savetxt(a.output / "rmsf_recomputed.csv", np.column_stack((ca.resids, rmsf)),
               delimiter=",", header="residue,C_alpha_rmsf_nm", comments="")
    zh = a.language == "zh"
    candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC",
                  "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else ["DejaVu Sans"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    plt.rcParams.update({"font.family": [name for name in candidates if name in installed],
                         "font.size": 13, "svg.fonttype": "path", "axes.spines.top": False,
                         "axes.spines.right": False, "axes.unicode_minus": False})
    fig, axes = plt.subplots(2, 2, figsize=(13.6, 9.8), constrained_layout=True)
    colors = {"teal": "#087f8c", "orange": "#cb6a36", "ink": "#203446"}
    t_ns = times/1000
    axes[0, 0].plot(t_ns, native_rmsd[:, 1], color=colors["teal"], lw=1.3)
    axes[0, 0].set(xlabel="时间 / ns" if zh else "Time / ns", ylabel="RMSD / nm",
                   title="A  主链相对共同参考的偏离" if zh else "A  Backbone deviation from a common reference")
    axes[0, 1].plot(t_ns, native_rg[:, 1], color=colors["orange"], lw=1.3)
    axes[0, 1].set(xlabel="时间 / ns" if zh else "Time / ns", ylabel="Rg / nm",
                   title="B  全蛋白的质量分布尺度" if zh else "B  Mass-distribution size of the full protein")
    axes[1, 0].plot(ca.resids, native_rmsf[:, 1], color=colors["ink"], lw=1.6)
    axes[1, 0].fill_between(ca.resids, 0, native_rmsf[:, 1], color=colors["teal"], alpha=.15)
    axes[1, 0].set(xlabel="残基编号" if zh else "Residue number", ylabel="Cα RMSF / nm",
                   title="C  对齐后的局部位置波动" if zh else "C  Local positional fluctuations after fitting", xlim=(1, 76), ylim=(0, .55))
    for i in (74, 75):
        axes[1, 0].annotate(str(ca.resids[i]), (ca.resids[i], native_rmsf[i, 1]),
                             xytext=(-22 if i == 74 else 6, 8), textcoords="offset points", fontsize=11)
    dots = axes[1, 1].scatter(native_rmsd[:, 1], native_rg[:, 1], c=t_ns,
                               s=13, cmap="viridis", alpha=.8, edgecolors="none", rasterized=False)
    axes[1, 1].set(xlabel="RMSD / nm", ylabel="Rg / nm",
                   title="D  同一帧的形变与尺寸" if zh else "D  Deviation and size in the same frame")
    bar = fig.colorbar(dots, ax=axes[1, 1], pad=.02)
    bar.set_label("时间 / ns" if zh else "Time / ns")
    for ax in axes.flat:
        ax.grid(alpha=.18)
        ax.tick_params(labelsize=11)
    fig.suptitle("泛素 · 0–1 ns 的三种运动读数" if zh else "Ubiquitin · three structural measurements over 0–1 ns", fontsize=19)
    fig.savefig(a.output / "protein_motion.svg")
    fig.savefig(a.output / "protein_motion.png", dpi=155)
    plt.close(fig)


if __name__ == "__main__":
    main()
```

MDAnalysis, NumPy, and Matplotlib read 1001 frames, taking masses from TPR and coordinates from XTC. The script recomputes all three observables in nm and compares them with GROMACS outputs. --language zh/en chooses figure labels while JSON and CSV retain identical definitions.

MDAnalysis expresses the loaded positions in Å, whereas these GROMACS measurements and the course plots use nm. The program therefore divides coordinates by ten before geometrical calculations. Time is read in ps and divided by 1000 for plots labeled in ns. The fitting function subtracts mass centers and uses the centered coordinate sets to find a rotation that preserves orientation. Its correction term excludes a mirror reflection. Readers unfamiliar with matrix decomposition can first follow the physical sequence—read coordinates, unify units, match centers, find a rigid rotation, measure residual distances—and use the four-point interaction to understand what the function accomplishes.

The program compares its recomputed values with the native XVG outputs at every recorded point. The maximum RMSD difference is approximately 0.00000015 nm, and the maximum Rg difference is approximately 0.0000085 nm. The native RMSF output has four decimal places, with a maximum difference from the recomputation of approximately 0.000050 nm. Algorithmic paths, floating-point arithmetic, and text-output precision leave small numerical differences while the definitions agree. The final figure uses the native records, CSV files retain the independently calculated values, and JSON records the atom counts, time range, and comparisons. A new trajectory can therefore pass through the same clearly specified measurements.

The numerical comparisons are useful because they test more than plotting style. Agreement requires the same coordinate units, matching atom identities, compatible weights, and the intended reference. A tenfold length-unit error or an unintended side-chain selection would affect the underlying values even if the resulting plot looked smooth. Keeping these choices visible in the code makes the analysis easier to adapt when the molecular system changes.

## Bring the three measurements back to the same motion

Start with panel A. Backbone RMSD averages approximately 0.0931 nm during the first 200 ps and 0.1970 nm during 600–800 ps, before declining again. These summaries use 200 ps intervals that include their left endpoint and exclude their right endpoint, so a boundary frame belongs to only one interval. The complete curve still includes the final 1000 ps frame. It shows changing departure from the common reference. Panel B, in contrast, remains mostly around 1.19 nm, with variations small relative to the mean molecular size. Reading the two time axes together shows that internal rearrangement and the extent of the mass distribution do not increase in step.

### Four views of the same ubiquitin trajectory

Replica 1 over 0–1000 ps, with 1001 frames. RMSD uses the common minimized backbone reference, Rg uses full-protein masses, and RMSF uses Cα-fitted coordinates over the whole window. Scatter colors encode saved time.

GROMACS 2026.4; chain A of PDB 1UBQ, 76 residues; AMBER99SB-ILDN with TIP3P. All 602 experimental heavy atoms are retained and 629 hydrogen atoms added. His68 uses neutral NE2 protonation, with charged free termini.

[Download reference data and complete inputs (ZIP) 129.06 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-protein-motion-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g08/en/#en-s8)

Backbone RMSD, full-protein mass-weighted radius of gyration, Cα RMSF and a time-colored RMSD–Rg scatter plot from the same 1 ns trajectory. Backbone RMSD uses the common minimized reference. RMSF is computed after fitting, around each Cα atom’s mean position over the window.

Panel C condenses the temporal record into a position distribution for each Cα, with a conspicuous rise through residues 73–76. It gives a concrete direction for further inspection: compare the terminus during higher and lower RMSD periods while examining contacts and backbone organization in the main body. To quantify the tail’s contribution, one can define a core for fitting or compare measurements of the full chain and a selection excluding the terminus. Retain the atom selections alongside those results. The resulting analysis separates spatial contributions in a physically interpretable coordinate frame.

Panel D places one point per saved frame, with that frame’s RMSD on the horizontal axis and Rg on the vertical axis. Color represents time. Points farther right have departed more from the reference, and points higher up have a more dispersed mass distribution. The colors reveal where different periods lie in this joint description and highlight moments when the observables change differently. Larger reference deviations can occur near the original Rg, while some slightly larger conformations near the end have smaller RMSD. The scatter plot and the time traces help turn a changing number into a question about which geometrical feature changed and when.

The trajectory below shows 51 Cα configurations sampled every 20 ps from this record. Its backbone fitting frame matches the RMSD analysis, helping connect a displayed time to the curves above. Pause at an early configuration, then move toward approximately 700 ps to compare the terminus and main body. Return to the final frames to examine how different regions rearrange as RMSD decreases. The display selects fewer atoms, while the Rg calculation above continues to use masses of all 1231 protein atoms.

### Watch ubiquitin move in a common reference frame

51 actual Cα configurations from replica 1, every 20 ps. A mass-weighted fit of 228 backbone atoms to the common reference connects local deformation with the plotted observables.

For a subsequent temperature or mutation study, specify an equally clear comparison: a common reference, fitting atoms, measurement atoms, observation window, and independently initialized trajectories. The present 1 ns record illustrates the distinctions between these geometrical observables and reveals terminal mobility and structural adjustment within this trajectory. Slower loop exchange, transitions far from the starting conformation, and long-time distributions call for observations on their relevant timescales. Connecting the timescale of the question to the timescale of the trajectory helps determine which additional calculations will provide useful information.

Returning to the molecular movie after this analysis often reveals more. Apparently dramatic motion may mainly be an overall rotation. A nearly unchanged outline can contain continuing internal rearrangement. A moving terminus can leave a clear peak in the residue profile. Animation helps discover and locate events, while geometrical measurements compare them under fixed definitions. The next lesson follows the same data into questions of reliability: how similar neighboring frames are, how a new set of initial velocities changes the observed curve, and how finite records can be organized into stronger comparisons.

## Further Reading and Open Materials

- [Introduction to Molecular Dynamics](https://tutorials.gromacs.org/docs/md-intro-tutorial.html) · Cathrine Bergh; Maryam Majdolhosseini; Alessandra Villa · CC BY 4.0

  Workflow for protein periodic images, RMSD, radius of gyration, and atom selection.

  Uses 1UBQ ubiquitin, explicit mass weights and a common reference, adding RMSF, Kabsch geometry, independent coordinate calculations, and bilingual multipanel figures.
- [From Proteins to Perturbed Hamiltonians: A Suite of Tutorials for the GROMACS-2018 Molecular Simulation Package](https://github.com/jalemkul/gmx_tutorials_livecoms) · Justin A. Lemkul · CC BY 4.0

  Conformational analysis following protein-in-water simulation.

  Developed around three distinct measurement baselines using an actual 2026.4 trajectory.
- [gmx rms — GROMACS 2026.4](https://manual.gromacs.org/2026.4/onlinehelp/gmx-rms.html) · GROMACS developers · GROMACS documentation terms; factual reference

  Reference-based, mass-weighted rigid fitting and RMSD.

  Explained with this example’s selections, units, and complete calculations.
- [gmx rmsf — GROMACS 2026.4](https://manual.gromacs.org/2026.4/onlinehelp/gmx-rmsf.html) · GROMACS developers · GROMACS documentation terms; factual reference

  Positional fluctuations after fitting.

  Explained with this example’s selections, units, and complete calculations.
- [gmx gyrate — GROMACS 2026.4](https://manual.gromacs.org/2026.4/onlinehelp/gmx-gyrate.html) · GROMACS developers · GROMACS documentation terms; factual reference

  Mass-weighted radius of gyration.

  Explained with this example’s selections, units, and complete calculations.
- [A solution for the best rotation to relate two sets of vectors](https://doi.org/10.1107/S0567739476001873) · Wolfgang Kabsch · Publisher copyright; factual historical citation

  The 1976 weighted least-squares alignment problem.

  Explains the geometry with drawings and a four-point interaction, accompanied by a conceptual structural-comparison diagram.
