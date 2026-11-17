# Flow cytometry: Reading multiple signals from individual cells

Source: https://ml-biomat.com/tutorials/experimental-methods/l09/en/
Language: en

Connect optical pulses, spillover and gates to population distributions, fractions and absolute counts.

## The same average can hide very different cell populations

Suppose the fluorescence of a culture doubles after you add a labeled material. Every cell might have become a little brighter, a small group might have become exceptionally bright, or damaged cells might have accumulated material that adheres to exposed surfaces. An average cannot distinguish these situations, just as the average height of a class does not describe all its students. Flow cytometry moves suspended objects through a detection region and records several signals for each passage. It turns a question about a whole tube into questions about individual events: which are bright, how bright they are, and which other properties accompany that brightness. This makes it useful for studying immune populations, protein expression, cell state and interactions between cells and materials.

The word event matters. One detected pulse does not automatically identify one intact living cell. Debris, two attached cells, counting beads and material particles can also trigger acquisition. The detector supplies measurements, while sample preparation, staining and controls establish their interpretation. After identifying a suitable population of live singlets, we can describe its phenotype: a combination of observable features, such as two proteins expressed together or a probe signal that changes after treatment. The connection between an event and a biological object is therefore part of the experiment, rather than a label the instrument already knows.

A flow file resembles a long table. Each row represents one recorded event; each column represents a parameter, perhaps integrated forward scatter or fluorescence collected in a particular wavelength band. Plot two columns and each row becomes a point. Change the axes and you inspect the same rows from another perspective. Point colors often represent density or a selected population, rather than the physical color emitted by a cell. Gating becomes easier to understand in this table view: drawing a region marks the rows that satisfy its conditions, while retaining a connection to their other recorded measurements.

This chapter follows two generic markers, X and Y, without assigning them a particular cell identity. The complete example constructs 12,000 events with known signals, noise and an acquisition disturbance, then writes and reads a standard FCS file. A separate, openly licensed figure shows measured distributions from published research. The constructed data let us trace each calculation; the measured figure shows the overlap and variation encountered in an experimental population. Their different roles help connect a transparent numerical model to the more complicated appearance of a real sample.

## A cell crossing a light beam leaves a pulse

Fluidic focusing helps suspended objects pass through a repeatable part of the illumination region. Picture a stream that narrows a queue toward a common observation point. This describes control of the trajectory, rather than a guarantee that objects never arrive together. Concentrated suspensions, adherent cells and unstable flow can place several objects within one detection window. Optical components distribute collected light among detectors, which convert it into electrical signals. During a passage, a signal rises and falls, producing a pulse whose area, height and width can be stored as separate parameters.

Forward scatter, or FSC, collects light near the incident direction; side scatter, or SSC, collects light at another angle. Under fixed optical conditions they often help distinguish populations with different dimensions and internal structures. Scattering also depends on refractive index, shape and collection geometry, however. FSC is consequently not already a ruler marked in micrometers, and SSC does not directly count intracellular granules. This distinction is useful in material-uptake experiments: attached particles, changed optical contrast or cell shrinkage can all alter scatter. Microscopy, preparation details and fluorescent labels provide complementary evidence for interpreting the population.

Pulse height is the maximum signal, while pulse area accumulates signal over the transit. Two neighboring cells may produce a broader pulse with considerably more area but a similar maximum height. The right panel illustrates this with two adjacent Gaussian pulses: their combined area is approximately twice that of one pulse, although the height remains close to the single-pulse value. Area–height relationships can therefore identify many paired events. Actual instruments apply their own electronic scaling and width definitions, so a singlet region should follow the relevant sample distribution rather than a universal diagonal copied from another experiment.

$$
A=\int s(t)\,dt,\qquad H=\max_t s(t),\qquad W_{\mathrm{eq}}=A/H
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a2e2af48082172a695b27ad4.svg) | Baseline-corrected pulse signal, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Transit time, μs in the figure. |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Integrated pulse area, a.u.·μs in this model. |
| ![Formula](https://ml-biomat.com/static/agent-math/6d6950da29507eb4f6b78d53.svg) | Maximum pulse height, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/19536a0d407aa5450fc4a393.svg) | Area-to-height equivalent width, μs; H must be positive. |

Area accumulates the passage; height retains the maximum. A Gaussian with height 1 a.u. and temporal standard deviation 2 μs has area 5.0133 a.u.·μs and equivalent width 5.0133 μs. Two neighboring identical pulses have total area 10.0265. Instrument W need not use A/H, and A/H channels can have separate electronic scaling; the main example gates normalized constructed coordinates.

![Original detection/sorting principle and constructed pulse geometry. The right panel integrates signal in a.u.·μs; a broader pulse can have more area without a proportional height increase.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/2fc87772aca8eb7481fcc6a6.svg?v=2fc87772aca8)

Figure 1Original detection/sorting principle and constructed pulse geometry. The right panel integrates signal in a.u.·μs; a broader pulse can have more area without a proportional height increase.

The history of sorting explains why these measurements became so useful. During the 1960s, individual-object detection was coupled to droplet deflection, allowing an object to be physically separated according to its measured properties. Fluorescent labeling then connected selection to cellular molecules. The historical account by the Herzenberg group describes the coordination of detection, droplet formation and charge-dependent deflection. The original schematic here emphasizes that causal sequence: identify an event, then separate its droplet at the appropriate time. An analytical cytometer primarily produces a data table; a sorter additionally recovers selected populations. A gate drawn on a plot selects rows in data, whereas obtaining a tube containing those cells requires sorting hardware and an assessment of recovery and purity.

## When two colors enter one detector, separate their contributions

Attaching a fluorophore to an antibody makes the structures it binds visible under suitable excitation. Emission extends across a wavelength band, and each detector also collects a band, so a dye and detector rarely correspond exclusively. Suppose X is mainly detected in the first channel but some of its light reaches the second. An X-only cell can then appear bright in the channel intended for Y. It resembles two microphones picking up one speaker: sound in the second recording does not establish that a second person spoke. Compensation resolves the linear mixture of signal contributions; its coefficients should come from controls rather than a desired population percentage.

Single-stained controls characterize this mixing. With X alone present, compare appropriately matched positive and negative populations in both detectors. The secondary-channel change divided by the primary-channel change estimates spillover. Positive and negative populations should have comparable autofluorescence, and the fluorophore, tandem-dye condition and instrument settings must match the experiment. A very dim positive population makes the slope harder to estimate, while detector saturation breaks the linear relationship. Panel C shows the event cloud underlying this slope. Estimating optical mixing is a different task from locating the positivity boundary in a fully stained sample.

The example retains spillover in both directions: 25% of X enters detector two, and 5% of Y enters detector one. After removing a known fixed electronic background, we solve two simultaneous equations. True contributions X = 1,000 and Y = 200 produce background-corrected measurements of 1,010 and 450. Of the second-channel signal, 250 comes from X. Meanwhile the first channel contains 10 contributed by Y, so subtracting each contaminating contribution once without accounting for their coupling leaves an error. A matrix is simply an organized way to write these simultaneous equations; the program uses a linear solver to recover the two components.

$$
\begin{bmatrix}y_1\\y_2\end{bmatrix}=\begin{bmatrix}1&b\\a&1\end{bmatrix}\begin{bmatrix}x_X\\x_Y\end{bmatrix},\qquad x_X=\frac{y_1-by_2}{1-ab},\quad x_Y=\frac{y_2-ay_1}{1-ab}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/759961a30d68d6c3c8e3b71a.svg) | Linear signals in two detectors after known fixed-background correction, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/710ad7c128e0717b76d57b53.svg) | Estimated X and Y primary-channel contributions, a.u.; each source is scaled to its primary detector. |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | X-to-second-detector spillover coefficient, dimensionless in the specified channel scaling. |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Y-to-first-detector spillover coefficient, dimensionless in the same convention. |

Assume linear unsaturated response, detector rows and source columns, with 1−ab nonzero. With a = 0.25 and b = 0.05, true contributions (1000, 200) produce (1010, 450), and simultaneous solution restores (1000, 200). Noisy data yield estimates and retain noise. Background treatment follows controls and instrument conventions; it does not assume identical autofluorescence for every cell.

Some weak signals become negative after background correction and compensation. Fluorophores do not emit negative light: the values are estimates relative to background, affected by measurement fluctuations. Replacing every negative value with zero piles the distribution against an artificial boundary and changes averages, quantiles and counts near gates. Compensation corrects mean spillover relationships but does not remove photon statistics or detector noise. A bright marker can also broaden the negative distribution in other channels. Panel D retains that width and the values below zero, separating a correctly centered distribution from one whose negative and positive populations are easy to distinguish.

![Constructed mixtures, compensated distributions, a single-stain slope and negative-signal noise. A and B use the same asinh scale; dashed thresholds correspond to 200 a.u. Each histogram in D integrates to one and retains negative values. All arrays come from the complete example.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/b120a98a292cc3867abe09a7.svg?v=b120a98a292c)

Figure 2Constructed mixtures, compensated distributions, a single-stain slope and negative-signal noise. A and B use the same asinh scale; dashed thresholds correspond to 200 a.u. Each histogram in D integrates to one and retains negative values. All arrays come from the complete example.

An ordinary logarithm cannot display zero or negative values. Cytometry therefore often uses scales that are gentle near zero and logarithm-like at larger magnitudes. This example uses an asinh transformation, with a cofactor c controlling how much of the near-zero region is expanded. Changing c changes the map scale, not the amount of protein on a cell. A threshold of 200 must also be transformed using the same rule so that it continues selecting the same events. Linear compensation precedes this nonlinear display transformation: bending each number before subtraction generally produces a different result from separating the contributions before changing coordinates.

$$
u=\operatorname{asinh}(x/c),\qquad u_g=\operatorname{asinh}(x_g/c)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | Compensated signal, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | Positive display cofactor, in the same units as x. |
| ![Formula](https://ml-biomat.com/static/agent-math/4620fefc72ebf96810ce9f34.svg) | Transformed coordinate, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/dfae5713ceb32386a507bad7.svg) | Gate threshold on the original signal scale, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/5c20f9bf1d88cc73e738ac44.svg) | Position of the same gate in display coordinates, dimensionless. |

Asinh retains both sides of zero and compresses large magnitudes. Because it is monotone, transforming points and thresholds together preserves membership. xg = 200 with c = 50 gives ug ≈ 2.09471; c = 100 gives 1.44364. Compensate on the linear scale first. For the example, transforming before compensation gives Y coordinate 1.99350 instead of 2.09471.

## Follow a selection path with an explicit denominator

Start by inspecting acquisition time. A sudden interval of lower scatter may reflect a bubble, altered flow or interrupted sample delivery, and it provides context for every subsequent fluorescence gate. The program introduces a defined disturbance from 45 to 48 seconds, then retains the stable intervals before and after it. In experiments, time selection should follow the acquisition record and signal behavior. A genuine biological response can also vary with time, especially during stimulation experiments. Preserving the original time parameter helps distinguish an acquisition problem from a process the experiment is intended to observe.

A scatter gate next identifies candidate cellular events and reduces obvious debris, followed by a pulse-geometry gate for singlets. For transparent calculations, the example uses a rectangular scatter region and a narrow area-to-height band. These constructed columns have been scaled to comparable numerical units. In a real sample, activated cells may enlarge and dissociated tissue populations may spread across scatter space. An excessively tight gate can remove the very population changed by treatment. Backgating projects the final selected events onto earlier plots, revealing whether they accumulate at an upstream boundary or whether an important subpopulation was excluded at the start.

Singlet selection also depends on morphology. Attached cells can orient differently in the stream, so one FSC width or area relationship may miss some combinations. SSC pulse parameters, other evidence of singlets and microscopy can help assess the selection. A viability dye then identifies the cell state relevant to the question. Intact membranes generally exclude certain nucleic-acid dyes, while membrane-compromised events stain strongly. If fixation and permeabilization follow, an appropriate fixable viability dye used at the correct stage can preserve information about the earlier membrane state. A dye-negative event meets that measurement definition; broader cellular function can be investigated with additional readouts.

![Gating path for the same 12,000 events. A marks the constructed disturbance; B–E use successive parents; F reports full counts. Scatter plots show subsets for readability, while all counts use complete arrays. Pulse axes use this example’s normalized scale.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/40d2c29a1df36956cc538a71.svg?v=40d2c29a1df3)

Figure 3Gating path for the same 12,000 events. A marks the constructed disturbance; B–E use successive parents; F reports full counts. Scatter plots show subsets for readability, while all counts use complete arrays. Pulse axes use this example’s normalized scale.

Every selection has a parent population: the events allowed to enter that stage. Suppose 10,000 acquired events yield 6,000 live singlets, including 3,000 X-positive events, of which 900 are also Y-positive. Dividing 900 by 3,000 gives 30%, the Y-positive fraction within X-positive events. Dividing by 6,000 gives 15%, the double-positive fraction among live singlets. Dividing by all 10,000 gives 9%. These answers can all be correct because they describe different populations. Exporting counts, parents and percentages together lets a reader reconstruct the selection path and understand the question answered by each ratio.

$$
p_{G\mid P}=N_G/N_P,\qquad p_{G\mid A}=\prod_{j=1}^{m}\frac{N_j}{N_{j-1}}=N_G/N_A
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5d37ecc8a3cfa64f17cb687e.svg) | Child population, its specified parent, and all events. |
| ![Formula](https://ml-biomat.com/static/agent-math/6ca1407bb5d26b15142bac1d.svg) | Event counts in those populations; denominators must be nonzero. |
| ![Formula](https://ml-biomat.com/static/agent-math/e030e3c0b33e809fab494344.svg) | Fractions relative to the parent or all events, dimensionless; multiply by 100 for percent. |
| ![Formula](https://ml-biomat.com/static/agent-math/5a4fe308f7124fa593b4bb53.svg) | Nested-gate index and number of stages. |
| ![Formula](https://ml-biomat.com/static/agent-math/5595bec7d02a56853e57f907.svg) | Counts retained at stage j and the preceding stage; N0 = NA and Nm = NG. |

For nested populations, intermediate counts cancel when successive fractions are multiplied. All 10,000 → 6,000 live singlets → 3,000 X-positive → 900 double-positive gives 0.6 × 0.5 × 0.3 = 0.09. The 30% and 15% fractions use different parents. Overlapping, non-nested gates do not form this same product chain.

The complete simulation differs from that round-number illustration because scatter, fluorescence and noise have continuous distributions. From 12,000 events it retains 11,700 stable events, 10,530 candidates, 9,754 singlets and 8,792 live events, with 866 double-positive events at the end. These represent about 9.85% of the live population and 7.22% of all events. Boolean masks record whether each row passes each gate, making it possible to return to particular events rather than relying exclusively on a rounded percentage displayed on screen.

## Give the positivity boundary an experimental basis

Different controls answer different questions about positivity. An unstained sample reveals autofluorescence and instrument background. A single-stained sample characterizes spillover. A fluorescence-minus-one control, or FMO, contains the other stains in the panel while omitting the marker currently being assessed. A Y-FMO therefore retains broadening associated with X and the other dyes, approximating the measurement environment experienced by Y-negative events in the full panel. Comparing the FMO with the fully stained sample helps locate signal extending beyond the background distribution created by the other stains together.

The omitted antibody is absent from the FMO, so the FMO cannot measure that antibody's nonspecific binding. Appropriate biological negative, positive or blocking controls address target recognition. Comparing cells known to lack a target with cells expressing it, for example, tests whether staining follows the target. In material-treatment experiments, also examine whether the material fluoresces, adsorbs antibodies or changes cellular autofluorescence. These controls provide complementary pieces of evidence. Treating one of them as a universal correction can miss changes linked specifically to the treatment condition, even when the resulting plot looks orderly.

Positivity does not always separate two distinct peaks. Some molecules vary continuously across a population, and a threshold converts that continuous variation into categories. In such cases, retain the distribution, a suitable location statistic such as median fluorescence, and the fraction above a predefined threshold. Readers can then see whether the conclusion depends on moving a boundary slightly. Antibody titration is similarly informative: more reagent may increase specific signal or elevate background, and useful conditions depend on separation and the experimental objective. Comparable detector settings, staining conditions and batches allow meaningful comparisons across samples.

The interactive example holds 240 constructed events fixed while changing compensation, threshold and display scale. Actual X-to-Y spillover is 25%, with 5% in the reverse direction. Correct compensation gives 50% Y-positive and 25% double-positive events. Skipping X-to-Y compensation makes some X-only events appear Y-positive. Changing the display cofactor moves both points and gate lines while preserving the selected fraction. Raising the Y threshold changes the biological classification rule instead. Following individual clouds through these operations separates correction of mixed signals, presentation of coordinates and the analyst's chosen boundary.

## Interactive experiment: Spillover, threshold and display scale

The same 240 constructed events are retained. Change X-to-Y compensation, then the Y threshold; finally change display scale alone and check that fractions stay fixed. X positivity is fixed at 400 a.u.; both percentages use all 240 events. Arrow keys adjust sliders; the plot scrolls horizontally on small screens.

[Figure: diagram](https://ml-biomat.com/tutorials/experimental-methods/l09/en/#L09-lab)

## A percentage needs both a denominator and a sampling scale

Two samples can each contain 10% target cells while containing very different total numbers. One may hold 100,000 live cells and the other 10,000. In toxicity studies, the composition of survivors should therefore be read alongside survival and total recovery: a population's fraction can rise because it expands or because other populations decline. The number of rows in a flow file depends on acquisition time, concentration and stopping conditions. Recording 20,000 events alone does not establish the volume of original sample that those events represent.

Counting beads supply a known reference. Add a known bead number to a defined volume of sample, mix thoroughly, then identify target cells and beads within the same acquisition. If both are sampled by the same fraction, the ratio of acquired cells to acquired beads equals their number ratio in the tube. The unknown sampling fraction cancels. Multiply the observed ratio by the added bead number and divide by the original sample volume to obtain the target concentration. Extra staining buffer dilutes beads and cells together; it should not be mistaken for the original sample volume in this calculation.

$$
C_{\mathrm{cell}}=\frac{n_{\mathrm{cell}}}{n_b}\frac{C_bV_b}{V_s}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cc5689fe165be4f85d6d561b.svg) | Target-cell concentration in the original aliquot, cells/μL. |
| ![Formula](https://ml-biomat.com/static/agent-math/914da3c1b6e03f18548e56ec.svg) | Target-cell and bead event counts within the same acquisition interval. |
| ![Formula](https://ml-biomat.com/static/agent-math/9a2c7455873446449e6636a4.svg) | Bead concentration before addition, beads/μL. |
| ![Formula](https://ml-biomat.com/static/agent-math/4c2fa541a1b8466dacbc3550.svg) | Added bead-suspension volume, μL. |
| ![Formula](https://ml-biomat.com/static/agent-math/af24cfe08968b9a399cca9b4.svg) | Original sample volume added to the counting mixture, μL. |

Uniformly mixed cells and beads with the same effective sampling fraction cancel unknown acquisition volume. With 6000 target events, 1000 bead events, Cb = 1000 beads/μL, Vb = 20 μL and Vs = 100 μL, the result is 1200 cells/μL. Quantities refer to the sample at bead addition; earlier dilution requires its own factor, and earlier preparation losses require recovery measurements.

For example, 20 μL of beads at 1,000 beads per μL contributes 20,000 beads to 100 μL of sample. Acquiring 6,000 target events and 1,000 bead events gives 1,200 target cells per μL of original sample. Doubling acquisition while collecting twice as many cells and beads gives the same concentration. This cancellation assumes uniform mixing, correct identification and no differential loss after adding the reference. A trigger threshold that excludes beads lowers their recorded count and inflates the calculated cell concentration. Washing after mixing can alter the ratio. The result describes the sample represented when the reference was introduced; earlier losses during tissue digestion or transfer require separate recovery records.

A calibrated volumetric acquisition system provides another route: divide target counts by the volume actually analyzed and apply the relevant dilution and recovery relationships. Either approach needs both a population definition and a volume definition. Beads have their own gate rather than belonging inside the live-singlet gate, and both counts must refer to a consistent acquisition interval. A study of relative composition may not need counting beads in every tube. A claim about target cells per milliliter, however, requires a measured volume or known reference to complete the calculation.

![Three separate worked examples: denominators for the same 900 events, a Poisson rare-count approximation, and invariant 1200 cells/μL as acquisition increases at a fixed cell/bead ratio. These illustrate counting definitions, rather than additional biological experiments.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/578ae4a7e3eccb8a7c7e6b13.svg?v=578ae4a7e3ec)

Figure 4Three separate worked examples: denominators for the same 900 events, a Poisson rare-count approximation, and invariant 1200 cells/μL as acquisition increases at a fixed cell/bead ratio. These illustrate counting definitions, rather than additional biological experiments.

Collecting more events also reduces sampling fluctuation. Under independent sampling with correct classification, the standard error of a proportion depends on both its value and the parent count. A 25% fraction among 1,000 parent events has a standard error of approximately 1.37 percentage points. This is not the variability between independent culture batches. For rare populations, the actual target count is particularly informative: a Poisson approximation gives about 20% relative counting variation at 25 target events and 10% at 100. At a stable target frequency, raising the expected target count from 25 to 100 requires approximately four times the total acquisition to halve this relative fluctuation. Planning around the expected target count makes that cost visible; a modest addition to an already large parent population may contribute very few rare events. Additional acquisition improves this component of precision, while preparation, compensation and gating biases require their own controls.

$$
\operatorname{SE}(\hat p)\simeq\sqrt{\frac{\hat p(1-\hat p)}{N}},\qquad\operatorname{CV}_{\mathrm{rare}}\simeq\frac{1}{\sqrt{k}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8e2a7a0b6724724df048ccba.svg) | Observed positive fraction, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Number of events in the specified parent population. |
| ![Formula](https://ml-biomat.com/static/agent-math/e7a5ba0e6907d996a32a35b0.svg) | Approximate standard error of the proportion under independent binomial sampling. |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | Rare-target count under a Poisson approximation. |
| ![Formula](https://ml-biomat.com/static/agent-math/1e15735a378a68af881e41dc.svg) | Approximate relative standard deviation of rare counts, dimensionless. |

With classification fixed, these expressions describe sampling fluctuation, not independent-preparation variation. p = 0.25 and N = 1000 give SE ≈ 0.01369, or 1.37 percentage points. Rare counts k = 25 and 100 give CV ≈ 20% and 10%. The relative-error expression does not apply at zero or extremely few events, and near-boundary proportions need suitable sparse-count intervals.

## Read measured distributions as populations with internal variation

Experimental populations rarely resemble four perfectly separated clouds. The published figure below compares CD4-positive and CD8-positive T cells across several measured parameters. Each row shows one signal, and the red and blue distributions correspond to the two identified populations. Comparing within a row reveals which markers separate the groups and which overlap substantially. The horizontal coordinate is transformed: 0.6 means neither 60% of the cells nor a molecular count that can be compared directly between different antibodies. Curve height helps display distribution shape; comparing peak heights alone does not establish the relative abundance of the two cell populations.

![White et al. (2021), Figure 2, CC BY 4.0, reproduced in full with an external title. Red denotes CD4-positive and blue CD8-positive T cells, comparing one parameter per row. The horizontal axis is transformed; peak heights do not directly give population counts. Data originate from the paper’s EQAPOL study.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/a597d462a950c1ef73f61f0c.svg?v=a597d462a950)

Figure 5White et al. (2021), Figure 2, CC BY 4.0, reproduced in full with an external title. Red denotes CD4-positive and blue CD8-positive T cells, comparing one parameter per row. The horizontal axis is transformed; peak heights do not directly give population counts. Data originate from the paper’s EQAPOL study.

This arrangement supports more specific questions. Two groups may have similar main peaks for a functional marker, but one may contain a larger high-signal tail. The whole-population median could change little even though the tail fraction changes substantially. Conversely, a modest shift of nearly all cells may move the median while producing little change in the fraction above a fixed threshold. The useful summary depends on whether the question concerns population composition, overall expression position or a minority of strong responders. Inspecting distributions before choosing a summary preserves information that would disappear if every channel became an identical bar chart.

Fluorescence is also separated from molecule number by several experimental steps. Binding-site availability, saturation, fluorophore brightness, detection efficiency and autofluorescence all influence the recorded signal. Changes in the same marker under comparable conditions can be informative; translating them into molecules per cell requires appropriate calibration and a binding model. Fluorescent materials create a related issue: surface attachment and internal uptake can both increase cell-associated signal. Imaging, suitable surface quenching or removal procedures can help distinguish those locations. Cytometry supplies a high-throughput distribution across individual events, while complementary experiments add spatial interpretation.

The unit of replication must follow the experimental design. Ten thousand measured cells in one tube do not constitute ten thousand independent cultures: they share culture conditions, treatment and preparation. Group comparisons usually retain a predefined statistic or set of statistics for each independent sample, together with representative distributions and gating. Event-level information describes variation within a sample, while variation between independently prepared samples tests the consistency of a treatment effect. These two levels provide different evidence and should remain visible in the analysis.

## Keep every result connected to its event table

The complete program constructs scatter, pulse and fluorescence measurements, adds known spillover, fixed background and noise, then uses FlowIO to write and read an FCS file. FCS stores metadata as well as event values, including channel names, recording conventions and time scaling. Gains and storage scales in acquired files require interpretation according to their definitions. The example deliberately writes linear floating-point data and verifies event number, channel order and numerical agreement after reading. FlowKit's documentation distinguishes uncompensated, compensated and transformed event states; the same distinction structures this analysis.

The mixing matrix explicitly uses detector rows and fluorophore columns, and its coefficients are exported with that convention. Another application's matrix may use the transpose. Testing the direction with a known single-stained event is therefore more informative than copying numbers without checking their meaning. Reading an FCS file does not by itself establish whether compensation has already been applied. Acquisition settings, metadata and analysis records should establish that state before another correction is added. Display parameters, the coordinate scale of each gate and its parent relationship also belong together: identical numerical gate coordinates can select different events under different transformations.

### From FCS events to compensation, gates and counts

Complete offline example with seed 909. Writes and reads a 12,000 × 8 FCS file, then compensates and gates the decoded values. Exports events, controls, gate counts, NPZ arrays and figures. Unmodified FlowIO 1.4.0 is bundled with its BSD license; external dependencies are NumPy, Matplotlib and Pillow.

```
"""Flow cytometry: constructed events, FCS round trip, compensation and gates.

The event cloud is simulated. The separately reproduced Figure 2 from White
et al. (2021) contains published experimental distributions; see NOTICE.txt.
Run offline: python main.py --output results --language en
"""
from pathlib import Path
import argparse, csv, json, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from PIL import Image

# Unmodified BSD-3-Clause FlowIO is bundled for portable FCS reading/writing.
sys.path.insert(0, str(Path(__file__).resolve().parent / 'data' / 'vendor'))
import flowio

BLUE='#186e83'; AMBER='#cd803f'; PURPLE='#8160a1'; GREEN='#3c8a6a'
MATRIX=np.array([[1., .05], [.25, 1.]])  # rows: detectors; columns: fluorophores
BACKGROUND=np.array([80., 100.])

def compensate(measured, matrix=MATRIX, background=BACKGROUND):
    """Solve the linear signal mixture before applying a display transform."""
    return np.linalg.solve(matrix, (np.asarray(measured)-background).T).T

def gate_events(events, corrected):
    time,area,height,width,side,dead=events[:,:6].T
    stable=(time<45)|(time>=48)
    cells=stable&(area>50)&(area<300)&(side>20)&(side<140)
    singlets=cells&(area/height>.85)&(area/height<1.15)
    live=singlets&(dead<200)
    positive=live&(corrected[:,0]>200)&(corrected[:,1]>200)
    return dict(all=np.ones(len(events),dtype=bool),stable=stable,cells=cells,singlets=singlets,live=live,double_positive=positive)

def main(output,language='zh'):
    out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh';T=lambda z,e:z if zh else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5'})
    def save(fig,name):
        fig.savefig(out/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    def table(name,header,rows):
        with(out/name).open('w',newline='',encoding='utf8')as f:
            writer=csv.writer(f);writer.writerow(header);writer.writerows(rows)
    rng=np.random.default_rng(909);N=12000
    kinds=np.repeat(['debris','doublet','dead','live'],[1200,800,1000,9000]);rng.shuffle(kinds)
    time=np.arange(N)/100.;height=rng.lognormal(np.log(100),.17,N);side=rng.normal(60,13,N)
    height[kinds=='debris']=rng.uniform(15,35,(kinds=='debris').sum());side[kinds=='debris']=rng.uniform(5,18,(kinds=='debris').sum())
    width=rng.normal(1,.035,N);width[kinds=='doublet']=rng.normal(1.8,.06,(kinds=='doublet').sum())
    area=height*width;artifact=(time>=45)&(time<48);area[artifact]*=.45
    viability=rng.normal(50,15,N);viability[kinds=='dead']=rng.lognormal(np.log(900),.25,(kinds=='dead').sum())
    phenotype=rng.choice(4,N,p=[.35,.35,.20,.10]);truth=rng.exponential(12,(N,2))+15
    for channel,groups in [(0,[1,3]),(1,[2,3])]:
        mask=np.isin(phenotype,groups);truth[mask,channel]=rng.lognormal(np.log(800),.3,mask.sum())
    truth[kinds=='debris']*=.1;truth[kinds=='dead']+=500
    ideal=truth@MATRIX.T;measured=ideal+BACKGROUND+rng.normal(size=(N,2))*(18+.5*np.sqrt(ideal))
    original=np.column_stack([time,area,height,width,side,viability,measured])
    labels=['Time','FSC-A','FSC-H','FSC-W','SSC-A','Viability-A','FL1-A','FL2-A']
    with(out/'constructed-events.fcs').open('wb')as handle:
        flowio.create_fcs(handle,original.ravel().tolist(),labels,metadata_dict={'timestep':'1','comment':'Constructed teaching events; linear signals; external compensation matrix'})
    fcs=flowio.FlowData(out/'constructed-events.fcs');events=fcs.as_array(preprocess=True)
    assert fcs.event_count==N and fcs.channel_count==8 and fcs.pnn_labels==labels
    assert np.allclose(events,original,rtol=1e-6,atol=1e-5)
    corrected=compensate(events[:,6:8]);gates=gate_events(events,corrected);live=gates['live']
    table('events.csv',labels+['X_compensated','Y_compensated','simulated_kind','selected_double_positive'],[list(row)+list(c)+[kind,int(gates['double_positive'][i])]for i,(row,c,kind)in enumerate(zip(events,corrected,kinds))])
    table('gate_counts.csv',['gate','parent','events','percent_parent','percent_all'],[[name,'none'if j==0 else list(gates)[j-1],int(mask.sum()),100*mask.sum()/(N if j==0 else list(gates.values())[j-1].sum()),100*mask.mean()]for j,(name,mask)in enumerate(gates.items())])
    table('mixing_matrix.csv',['detector','X_coefficient','Y_coefficient'],[['FL1-A',1,.05],['FL2-A',.25,1]])
    np.savez_compressed(out/'flow_data.npz',events=events,corrected=corrected,truth=truth,kind=kinds,**{f'gate_{k}':v for k,v in gates.items()})
    # Independent single-stain controls estimate spillover on a linear scale.
    negative=BACKGROUND+rng.normal(0,12,(1000,2));controls=[];estimates=[]
    for ch in [0,1]:
        x=np.zeros((1000,2));x[:,ch]=rng.lognormal(np.log(1800),.28,1000)
        y=x@MATRIX.T+BACKGROUND+rng.normal(0,15,(1000,2));controls.append(y)
        delta=np.median(y,axis=0)-np.median(negative,axis=0);estimates.append(delta[1-ch]/delta[ch])
    table('single_stain_controls.csv',['control','FL1_A','FL2_A'],[[name,*row]for name,data in zip(['unstained','X_only','Y_only'],[negative,*controls])for row in data])
    # Same X-positive control gives the Y-FMO spreading example, after compensation.
    fmo=compensate(controls[0]);unstained=compensate(negative)
    cofactor=50.;transform=lambda x:np.arcsinh(x/cofactor)
    t=np.linspace(-15,15,1201);pulse=np.exp(-t*t/(2*2**2));double=np.exp(-(t-3)**2/8)+np.exp(-(t+3)**2/8)
    fig,axs=plt.subplots(1,2,figsize=(12,5.6));ax=axs[0];ax.set(xlim=(0,10),ylim=(0,9));ax.axis('off')
    ax.add_patch(Polygon([[3,8],[7,8],[5.7,5],[5.7,3],[4.3,3],[4.3,5]],closed=True,fc=BLUE,alpha=.12))
    ax.plot([5,5],[8,3],color=BLUE,lw=1)
    for y in [7.5,6.5,5.5,4.5,3.5]:ax.add_patch(Circle((5,y),.18,fc=BLUE))
    ax.annotate('',xy=(6.4,4.5),xytext=(1,4.5),arrowprops={'arrowstyle':'->','color':AMBER,'lw':2})
    ax.text(.8,5,T('激光','Laser'),color=AMBER);ax.text(7,4.5,T('散射与荧光\n成为同一行记录','Scatter and fluorescence\nbecome one event row'),fontsize=10,va='center')
    for x,y in [(5,2.6),(4.5,1.8),(4,1),(5.5,1.8),(6,1)]:ax.add_patch(Circle((x,y),.16,fc=PURPLE if x<5 else GREEN))
    ax.text(.3,8.7,T('1960年代：从逐个检测到按信号分选','1960s: from individual detection to signal-based sorting'),fontsize=11)
    ax.text(.3,.1,T('原创原理图；分选需另有液滴识别与偏转。','Original principle; sorting adds timed droplet deflection.'),fontsize=9)
    ax=axs[1];ax.plot(t,pulse,color=BLUE,label=T('一个高斯脉冲','One Gaussian pulse'));ax.plot(t,double,color=AMBER,label=T('相邻两脉冲','Two adjacent pulses'));ax.fill_between(t,0,pulse,color=BLUE,alpha=.12)
    ax.set(xlabel=T('经过光束的时间 / μs','Transit time / μs'),ylabel=T('扣基线信号 / a.u.','Baseline-corrected signal / a.u.'),title=T('高度接近，积分面积明显不同','Similar height, different integrated area'));ax.legend(frameon=False,fontsize=9);fig.tight_layout();save(fig,'history-pulses')
    fig,axs=plt.subplots(2,2,figsize=(11.5,8.7));sample=np.flatnonzero(live)[::3]
    for ax,data,title in [(axs[0,0],events[:,6:8]-BACKGROUND,T('A  扣基线后仍混有串色','A  Baseline subtraction leaves spillover')),(axs[0,1],corrected,T('B  线性补偿后，再用asinh显示','B  Linear compensation, then asinh display'))]:
        v=transform(data[sample]);ax.scatter(v[:,0],v[:,1],s=3,alpha=.22,color=BLUE,rasterized=True);ax.axvline(transform(200),color=AMBER,ls='--');ax.axhline(transform(200),color=AMBER,ls='--');ax.set(xlim=(-2,5),ylim=(-2,5),xlabel='asinh(detector 1 / 50)' if ax is axs[0,0] else 'asinh(X / 50)',ylabel='asinh(detector 2 / 50)' if ax is axs[0,0] else 'asinh(Y / 50)',title=title)
    ax=axs[1,0];ax.scatter(controls[0][:,0]-80,controls[0][:,1]-100,s=3,alpha=.2,color=AMBER);xx=np.array([0,4500]);ax.plot(xx,.25*xx,color=BLUE);ax.set(xlabel=T('X单染：主通道 / a.u.','X-only: primary detector / a.u.'),ylabel=T('次通道 / a.u.','Secondary detector / a.u.'),title=T('C  单染斜率给出串色比例','C  Single stain estimates spillover'))
    ax=axs[1,1];bins=np.linspace(-70,70,50);ax.hist(unstained[:,1],bins=bins,density=True,histtype='step',lw=2,color=GREEN,label=T('未染色对照','Unstained'));ax.hist(fmo[:,1],bins=bins,density=True,histtype='step',lw=2,color=PURPLE,label=T('X单染，Y缺失','X stained, Y omitted'));ax.axvline(0,color='gray',lw=.7);ax.set(xlabel=T('补偿Y / a.u.','Compensated Y / a.u.'),ylabel=T('概率密度 / (a.u.)⁻¹','Probability density / (a.u.)⁻¹'),title=T('D  负值保留，噪声仍存在','D  Retain negative values and noise'));ax.legend(frameon=False,fontsize=9)
    fig.tight_layout();save(fig,'compensation')
    fig,axs=plt.subplots(2,3,figsize=(13,8.1));idx=np.arange(0,N,4)
    axs[0,0].scatter(events[idx,0],events[idx,1],s=2,color=BLUE,alpha=.2);axs[0,0].axvspan(45,48,color=AMBER,alpha=.2);axs[0,0].set(xlabel=T('采集时间 / s','Acquisition time / s'),ylabel='FSC-A / a.u.',title=T('A  先检查时间稳定性','A  Check stability over time'))
    ids=np.flatnonzero(gates['stable'])[::3];axs[0,1].scatter(events[ids,1],events[ids,4],s=2,color=BLUE,alpha=.2);axs[0,1].add_patch(Rectangle((50,20),250,120,fill=False,ec=AMBER,lw=1.5));axs[0,1].set(xlabel='FSC-A / a.u.',ylabel='SSC-A / a.u.',title=T('B  散射门定义候选事件','B  Scatter gate defines candidates'))
    ids=np.flatnonzero(gates['cells'])[::3];axs[0,2].scatter(events[ids,2],events[ids,1],s=2,color=BLUE,alpha=.2);xx=np.array([40,200]);axs[0,2].plot(xx,.85*xx,color=AMBER);axs[0,2].plot(xx,1.15*xx,color=AMBER);axs[0,2].set(xlabel='FSC-H / a.u.',ylabel='FSC-A / a.u.',title=T('C  单事件脉冲几何','C  Singlet pulse geometry'))
    ids=np.flatnonzero(gates['singlets']);axs[1,0].hist(events[ids,5],bins=np.linspace(0,1600,70),color=BLUE,alpha=.7);axs[1,0].axvline(200,color=AMBER);axs[1,0].set(xlabel=T('死亡染料 / a.u.','Viability-dye signal / a.u.'),ylabel=T('事件数','Events'),title=T('D  选定存活状态','D  Select the live population'))
    axs[1,1].scatter(transform(corrected[sample,0]),transform(corrected[sample,1]),s=2,alpha=.2,color=BLUE);axs[1,1].axvline(transform(200),color=AMBER);axs[1,1].axhline(transform(200),color=AMBER);axs[1,1].set(xlabel='asinh(X / 50)',ylabel='asinh(Y / 50)',title=T('E  活单细胞中读取表型','E  Phenotype within live singlets'))
    names=[T(z,e)for z,e in [('全部','All'),('稳定','Stable'),('候选','Cells'),('单细胞','Singlets'),('活细胞','Live'),('双阳性','X+Y+')]];counts=[int(v.sum())for v in gates.values()];axs[1,2].barh(np.arange(6),counts,color=[BLUE]*5+[AMBER]);axs[1,2].set_yticks(np.arange(6),names);axs[1,2].invert_yaxis();axs[1,2].set(xlabel=T('通过事件数','Passing events'),title=T('F  每一步保留数量与分母','F  Preserve counts and denominators'))
    for i,c in enumerate(counts):axs[1,2].text(c+100,i,str(c),va='center',fontsize=9)
    axs[1,2].set_xlim(0,15000);fig.tight_layout();save(fig,'gating')
    fig,axs=plt.subplots(1,3,figsize=(13,4.7));denoms=[10000,6000,3000];numerator=900
    axs[0].bar(T(['全部事件','活单细胞','X阳性'],['All events','Live singlets','X-positive']),[100*numerator/d for d in denoms],color=[BLUE,GREEN,AMBER]);axs[0].set(ylabel=T('同一900事件所占比例 / %','Fraction of the same 900 events / %'),title=T('A  分母改变，问题改变','A  Denominators change the question'))
    k=np.logspace(0,4,200);axs[1].loglog(k,100/np.sqrt(k),color=PURPLE);axs[1].scatter([25,100,400],[20,10,5],color=AMBER);axs[1].set(xlabel=T('稀有目标事件数 k','Rare-target count k'),ylabel=T('泊松计数近似CV / %','Poisson counting CV / %'),title=T('B  多采集改善抽样精度','B  More events improve sampling precision'))
    beads=np.array([500,1000,2000]);cells=6*beads;concentration=cells/beads*1000*20/100
    axs[2].plot(beads,concentration,'o-',color=GREEN);axs[2].set(xlabel=T('采到的计数珠数','Acquired bead events'),ylabel=T('原样目标浓度 / cells μL⁻¹','Original target concentration / cells μL⁻¹'),ylim=(0,1600),title=T('C  采集份额消去','C  Sampling fraction cancels'));fig.tight_layout();save(fig,'counts')
    fig,ax=plt.subplots(figsize=(13,8.2));ax.imshow(Image.open(Path(__file__).resolve().parent/'flowkit2021-figure2.webp').convert('RGB'));ax.axis('off');ax.set_title(T('真实测量分布：在同一标记内比较两群细胞','Measured distributions: compare two populations within each marker'),fontsize=12);fig.text(.5,.015,T('White等，2021，图2；CC BY 4.0，完整转载。原图横轴是变换坐标。','White et al., 2021, Figure 2; CC BY 4.0, reproduced in full. Original x-axis shows transformed coordinates.'),ha='center',fontsize=9);fig.tight_layout(rect=[0,.04,1,1]);save(fig,'published')
    exact=compensate(np.array([[1010.,450.]])+BACKGROUND)
    wrong=compensate(transform(np.array([[1010.,450.]])),background=np.zeros(2))
    summary={'fcs':{'events':fcs.event_count,'channels':fcs.channel_count,'maximum_absolute_roundtrip_error':float(abs(events-original).max())},'compensation':{'example_X':float(exact[0,0]),'example_Y':float(exact[0,1]),'estimated_X_to_Y':float(estimates[0]),'estimated_Y_to_X':float(estimates[1]),'negative_Y_live_events':int((corrected[live,1]<0).sum()),'transform_then_compensate_Y':float(wrong[0,1]),'compensate_then_transform_Y':float(transform(exact)[0,1])},'pulse':{'single_area':float(np.trapezoid(pulse,t)),'double_area':float(np.trapezoid(double,t)),'area_ratio':float(np.trapezoid(double,t)/np.trapezoid(pulse,t))},'gates':dict(zip(gates,counts)),'fractions':{'double_positive_percent_live':100*counts[-1]/counts[-2],'double_positive_percent_all':100*counts[-1]/N},'counting':{'conditional_percent':900/3000*100,'all_percent':900/10000*100,'bead_based_cells_per_uL':6000/1000*1000*20/100,'binomial_se_at_p025_N1000':float(np.sqrt(.25*.75/1000)),'rare_cv_at25':1/np.sqrt(25),'rare_cv_at100':1/np.sqrt(100)}}
    assert np.allclose(exact,[[1000,200]])
    assert abs(estimates[0]-.25)<.01 and abs(estimates[1]-.05)<.01
    assert summary['compensation']['negative_Y_live_events']>0
    assert all(a>=b for a,b in zip(counts,counts[1:]))
    assert abs(summary['pulse']['area_ratio']-2)<1e-7
    assert not np.isclose(wrong[0,1],transform(exact)[0,1])
    (out/'summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False),encoding='utf8');print(json.dumps(summary,allow_nan=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);parser.add_argument('--language',choices=['zh','en'],default='zh');args=parser.parse_args();main(args.output,args.language)
```

Outputs include the constructed FCS, an event table, single-stain controls, gate counts and all figures. The event table retains compensated X and Y and the final selection flag, enabling a double-positive event to be traced back to its time, scatter and viability measurements. Scatter plots use a subset for readability, while every count uses the complete event set. This distinction matters when files become large: displaying 2,000 points should not silently change the statistical denominator to 2,000. The same record structure can be used with experimental files once channel identities, controls and population definitions are established.

A clear result names its object, state and denominator. For example, the double-positive fraction among live singlets after stable-time, scatter and pulse-geometry selection conveys much more than a statement that positivity increased. Independent-sample results, corresponding distributions, controls and any absolute-counting reference then show whether the change concerns composition, signal position or quantity. Flow cytometry connects these questions through individual event records, allowing a mixed suspension to be investigated as populations whose measured properties remain linked to the same objects.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L09.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Herzenberg et al. (2002). The History and Future of the Fluorescence Activated Cell Sorter and Flow Cytometry](https://herzenberglab.stanford.edu/sites/g/files/sbiybj27506/files/media/file/lah490.pdf)

   History of detection, fluorescence labeling and timed droplet deflection.

   Historical reference; no artwork reproduced.
2. [Cossarizza et al. (2019). Guidelines for the use of flow cytometry and cell sorting in immunological studies, second edition](https://pmc.ncbi.nlm.nih.gov/articles/PMC7350392/)

   Single-stain controls, FMO, viability staining, doublet pulse geometry and analysis definitions.
3. [FlowKit tutorial 1: Sample class](https://flowkit.readthedocs.io/en/latest/notebooks/flowkit-tutorial-part01-sample-class.html)

   FCS metadata, preprocessing and raw/comp/xform event states.
4. [FlowKit tutorial 2: transforms and Matrix](https://flowkit.readthedocs.io/en/latest/notebooks/flowkit-tutorial-part02-transforms-module-matrix-class.html)

   Compensation, display transformations, negative values and coordinate scales.
5. [FlowKit tutorial 3: GatingStrategy and GatingResults](https://flowkit.readthedocs.io/en/latest/notebooks/flowkit-tutorial-part03-gating-strategy-and-gating-results-classes.html)

   Hierarchical gates and parent-relative versus overall statistics.
6. [FlowIO API and source](https://flowio.readthedocs.io/en/latest/api.html)

   Writing and reading FCS with FlowIO; channel and preprocessing interpretation.

   FlowIO 1.4.0 source bundled under BSD-3-Clause; full license included.
7. [CountBright Plus Absolute Counting Beads User Guide, MAN0018850 B.0](https://documents.thermofisher.com/TFS-Assets/LSG/manuals/MAN0018850_CountBrightPlus_UG.pdf)

   Cell/bead ratios, original sample volume, mixing and post-addition losses.
8. [White et al. (2021). FlowKit: A Python Toolkit for Integrated Manual and Automated Cytometry Analysis Workflows](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2021.768541/full)

   Measured CD4/CD8 distributions in Figure 2 and organization of event/gate information.

   Figure 2: CC BY 4.0, credited and reproduced in full; code license separately BSD-3-Clause.
