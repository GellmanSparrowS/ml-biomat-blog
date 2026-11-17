# SEC/GPC: How large are polymer molecules

Source: https://ml-biomat.com/tutorials/experimental-methods/c02/en/
Language: en

Follow dissolved chains through porous spaces to understand size separation, mass weighting and molecular distributions.

## The same polymer name can hide very different chains

Dissolve equal masses of two hyaluronic acid powders in equal volumes of water. One solution may feel considerably thicker than the other. The chemical name identifies the repeating building blocks, but it does not tell us how many blocks are connected in each chain. Think of necklaces made from identical beads: a box of short necklaces and a box containing some very long ones can have the same total mass while tangling and flowing differently. Real solutions also respond to concentration, salt, temperature and interactions between chains. To investigate whether chain length contributes to a change, we need a measurement that separates dissolved molecules according to their size. Size-exclusion chromatography, abbreviated SEC, provides that part of the investigation.

A related question appears in protein research. A vial may contain individual proteins, pairs of associated proteins and larger aggregates. Gel filtration can separate these populations and allow useful fractions to be collected. In a degradable polymer, chains may have broken into shorter pieces while the material still looks intact. Comparing SEC distributions before and after treatment connects the visible object to changes in its soluble molecular population. The word soluble defines the population that enters the measurement. A network that only swells, or a fraction that precipitates during preparation, needs its own observation and mass accounting so that the chromatogram can be interpreted within the complete material.

The names gel permeation chromatography, or GPC, and gel filtration chromatography, or GFC, reflect historical applications of the same size-exclusion mechanism. GPC is commonly used for polymer analysis in organic solvents; GFC is common in aqueous biomolecular separation. A column contains porous particles. Dissolved molecules of different sizes can access different amounts of solvent inside those particles, so they leave the column at different average positions. The first output is detector response against elution time or volume. Converting that position to molar mass is a further step requiring calibration or additional detectors. Keeping these two steps distinct makes a molecular-mass axis much easier to understand.

We will follow a specimen through that sequence: why large molecules emerge first, how standards establish a scale, why a population requires more than one average, and how specimen preparation changes what reaches the column. A published polyethylene distribution provides a real example of a cumulative mass curve. A complete computational experiment then connects pore accessibility, calibration, detector-like signals and integration decisions. The aim is to read both axes of a chromatogram, explain plausible causes of a shift or shoulder, and choose a control that makes the next experiment more informative.

## Large molecules emerge first because they visit fewer side rooms

Imagine a corridor with many small rooms along its sides. One group of visitors stays in the corridor, while another also enters the rooms. Even if they move similarly in the corridor, the second group takes longer, on average, to reach the exit. In SEC, solvent between the packing particles resembles the corridor, and solvent inside their pores resembles the side rooms. Large dissolved molecules can access less of the internal space. Smaller molecules can explore more of it and therefore elute later. The mechanism does not require forcing a large molecule through a membrane pore. Nor are small molecules blocked at the outlet. Separation follows from their distribution between accessible solvent regions.

The history helps correct the familiar intuition that a sieve always lets small objects through first. In his retrospective account, Jerker Porath described separation in starch columns even without the electrical current used for electrophoresis. Work with Per Flodin on crosslinked dextran gels led to a 1959 publication and an influential approach to separating macromolecules from small solutes. Our original diagram connects that idea to desalting: a macromolecular band emerges before the salt band, allowing the first fraction to be collected. The plotted curves are teaching constructions representing this mechanism, rather than reconstructed measurements from the historical experiments.

Two measured reference volumes make the side-room analogy quantitative. An appropriate noninteracting marker that is completely excluded from the pores provides the exclusion volume, V₀. A small marker that accesses the relevant internal solvent provides the total accessible volume, Vₜ. This latter quantity is a chromatographic reference, not the external cylindrical volume calculated from the column casing. A target eluting at Vₑ has accessed an additional volume above V₀. Dividing that increment by the available pore volume gives the dimensionless accessibility measure Kₐᵥ. With V₀=3 mL, Vₜ=18 mL and Vₑ=9 mL, the increment is 6 mL out of 15 mL, giving 0.4.

$$
K_{\mathrm{av}}=\frac{V_e-V_0}{V_t-V_0}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/17929f84b05c9c9ee6b7954d.svg) | Apparent accessible pore-volume fraction, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/daa1e83231d13f3a99351353.svg) | Target elution volume, mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/454606841ec20ef0f43cd9f6.svg) | Volume measured by a suitable fully excluded marker, mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/ad460123890fe451611439a3.svg) | Total accessible volume from a suitable fully included marker, mL. |

When size exclusion dominates and markers are appropriate, divide extra accessed volume by accessible pore volume. Vₑ=9, V₀=3 and Vₜ=18 mL give 6/15=0.4. Zero and one describe reference limits; additional adsorption or repulsion changes this interpretation.

![Original pore-access and desalting diagrams; dimensions are schematic. B uses constructed desalting bands to illustrate the mechanism associated with 1959 gel filtration. C uses V₀=3 and Vₜ=18 mL.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/cc78e80d8339979b32c57812.svg?v=cc78e80d8339)

Figure 1Original pore-access and desalting diagrams; dimensions are schematic. B uses constructed desalting bands to illustrate the mechanism associated with 1959 gel filtration. C uses V₀=3 and Vₜ=18 mL.

At either end of the useful range, size discrimination becomes weak. Several very large molecules may all be excluded and emerge near V₀. Several very small molecules may all access essentially the same internal space and emerge near Vₜ. The fractionation range lies between those limits. This explains why a column that works well for separating protein from salt is not automatically suitable for resolving two similarly sized proteins. Desalting requires group separation across a large size difference. Resolving nearby molecular populations requires enough position difference within a narrower range, together with a suitably narrow injected band and adequate column efficiency.

Real molecules may also interact with pore surfaces through charge, hydrophobicity or other chemistry. A charged polysaccharide at low salt concentration may adopt an extended conformation and experience electrostatic interactions with the packing. Both effects can move a peak. Changing salt and observing a different elution volume therefore calls for interpretation of the solution conditions. Buffer composition, ionic strength and packing chemistry are chosen to make size exclusion the principal retention mechanism. Concentration series and known reference specimens then help test that choice. The analogy explains the intended physical mechanism; controls establish whether the actual system follows it closely enough for the research question.

## Calibration builds a bridge from elution position to molar mass

A detector cannot know whether a peak at 10 mL contains chains of ten thousand or one hundred thousand grams per mole. Conventional calibration passes a series of known, relatively narrow polymer standards through the same system and records their peak positions. Within a useful working range, the base-ten logarithm of molar mass often changes approximately linearly with elution volume. A logarithmic scale puts successive factors of ten at equal distances, allowing thousands, tens of thousands and hundreds of thousands to share a readable graph. Larger standards appear at smaller elution volumes, consistent with their reduced pore accessibility.

John Moore's 1964 work with crosslinked polystyrene gels helped establish GPC as a continuous instrumental approach to polymer distributions. This development made calibration central: recording the effluent curve was valuable only when its positions could be related to molecular properties. Our teaching calibration uses a straight line whose slope describes the change in logarithmic molar mass per milliliter. Its intercept locates the scale vertically. In an experimental method, standards should span the distribution of interest, and residuals and end-region curvature should be inspected. A convenient straight equation is useful within the region supported by those measurements; a broad column range may require a different calibration form.

$$
\log_{10}\!\left(\frac{M}{1\,\mathrm{g\,mol^{-1}}}\right)=a-bV_e
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/34058a2a5d1de088feed7d98.svg) | Calibration-assigned molar mass, g/mol. |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Linear calibration intercept, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Magnitude of the decreasing calibration slope, mL⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/daa1e83231d13f3a99351353.svg) | Elution volume, mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/be8ebdecd039424afe275a60.svg) | Base-ten logarithm; division by the unit quantity makes its argument dimensionless. |

Within the standards-covered approximately linear fractionation range, logarithms connect position to standard mass. a=7, b=0.25 mL⁻¹ and Vₑ=10 mL give log₁₀ M=4.5, or approximately 31,623 g/mol; 12 mL gives 10,000 g/mol. The conversion depends on chemical series and solution conditions.

![Constructed standards and population: the number distribution of log₁₀ M has mean 4.2 and SD 0.35; mass weighting changes its center. Extra chromatographic broadening is σV=0.25 mL and area is normalized to one. D accumulates in elution order, from large to small.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/6692e4e6e3bfe98fd37317af.svg?v=6692e4e6e3bf)

Figure 2Constructed standards and population: the number distribution of log₁₀ M has mean 4.2 and SD 0.35; mass weighting changes its center. Extra chromatographic broadening is σV=0.25 mL and area is normalized to one. D accumulates in elution order, from large to small.

The identity and conformation of the standards matter. Two chains with the same mass can occupy different effective sizes in a solvent. Branching may make a chain more compact than a linear chain of equal mass, while a change in solvent can alter expansion. An unknown polymer calibrated against polystyrene therefore receives a polystyrene-equivalent molar mass under the stated conditions. The term equivalent tells the reader how the ruler was constructed. It also helps comparisons between laboratories. If the research question asks whether a branching reaction changed actual mass, a size-based calibration benefits from an additional measurement that addresses that distinction.

A differential refractive-index detector is a common companion to SEC. It compares the refractive index of the eluting solution with that of the mobile phase. For a given polymer, solvent and temperature in an appropriate dilute range, response can be related to concentration. The area in a small elution-volume slice then represents mass in that slice. A UV detector instead responds to absorption at its selected wavelength. Different components can have very different absorptivities: a protein and a weakly absorbing polysaccharide do not automatically contribute equal signal per unit mass. Before interpreting peak areas as composition, establish what the detector senses and whether its response factor is comparable across the relevant populations.

Adding multi-angle light scattering and concentration detection allows molar mass to be inferred from scattering and concentration in successive slices, reducing dependence on conventional polymer standards. Refractive-index increment, detector alignment, band broadening and contributions from dust or aggregates remain part of that inference. Understanding this as a calibration-standard-independent mass measurement is more useful than treating the word absolute as the disappearance of experimental assumptions. Conventional calibration and concentration weighting provide a clear foundation; additional detectors then extend the information available from the same separation.

## One population, two averages and two different voting rules

Consider a deliberately simple population: ninety chains each have a molar mass of 10,000 g/mol, and ten chains each have a molar mass of 100,000 g/mol. Short chains account for ninety percent of the number, but the ten long chains contribute slightly more mass than all ninety short chains. Molar mass is the mass of a mole of the specified chains, expressed here in grams per mole. We can give every chain one vote and calculate number-average molar mass, Mₙ. Alternatively, we can let each unit of mass carry equal weight and calculate weight-average molar mass, M𝑤. Both calculations describe the same population, using different weighting rules.

The number average resembles an ordinary arithmetic mean. Multiply the count of each type by its molar mass, add those contributions and divide by the total chain count. Our example gives 19,000 g/mol. This is not the threshold with half the chains on each side; that threshold is a median. In the discrete example, the number median is 10,000 g/mol because ninety percent of the chains have that value. The distinction matters for broad distributions: a relatively small number of long chains can increase a mean while most individual chains remain shorter.

$$
M_n=\frac{\sum_i N_iM_i}{\sum_i N_i}=\left(\sum_i\frac{w_i}{M_i}\right)^{-1},\qquad w_i=\frac{N_iM_i}{\sum_j N_jM_j}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4f3c9d3ab8208b50c9e81e73.svg) | Number-average molar mass, g/mol. |
| ![Formula](https://ml-biomat.com/static/agent-math/2e48d6441cb55e92796c4f28.svg) | Counts of chains in the corresponding classes, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/80f8ce36f42008dae6d1d510.svg) | Molar masses of the corresponding classes, g/mol. |
| ![Formula](https://ml-biomat.com/static/agent-math/cec5f0994a4bad5c3ac4a9a4.svg) | Mass fraction of class i, dimensionless; fractions sum to one. |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | Indices covering all relevant chain classes or mass slices. |

Average with equal weight per chain. For mass slices, mass divided by molar mass gives a count-proportional weight. Ninety chains at 10,000 and ten at 100,000 g/mol give Mn=19,000 g/mol; mass fractions are 9/19 and 10/19.

The weight average first asks how much mass each class contributes, then uses those mass fractions to average molar mass. Long chains contribute both a larger molar mass and a larger mass-based weight. Consequently, the high-mass tail has a stronger influence on M𝑤. The same ninety-to-ten example gives approximately 57,368 g/mol. Dividing M𝑤 by Mₙ gives dispersity, written Đ, which compares these two weighted averages. Identical chains give a value of one. Heterogeneity generally raises the weight average above the number average; here the ratio is approximately 3.019. Different distribution shapes can share that ratio, so the full curve still contains useful information.

$$
M_w=\sum_i w_iM_i=\frac{\sum_iN_iM_i^2}{\sum_iN_iM_i},\qquad \mathit{Đ}=\frac{M_w}{M_n}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/584328b60ee68abee6861462.svg) | Weight-average molar mass, g/mol. |
| ![Formula](https://ml-biomat.com/static/agent-math/cec5f0994a4bad5c3ac4a9a4.svg) | Mass fraction of class i, dimensionless, summing to one. |
| ![Formula](https://ml-biomat.com/static/agent-math/b26e60e55288c9229968cad0.svg) | Count of chains in class i. |
| ![Formula](https://ml-biomat.com/static/agent-math/9b5817fb0c0bac5188945802.svg) | Molar mass of class i, g/mol. |
| ![Formula](https://ml-biomat.com/static/agent-math/4f3c9d3ab8208b50c9e81e73.svg) | Number-average molar mass, g/mol. |
| ![Formula](https://ml-biomat.com/static/agent-math/40bf2c4da5241a580e5118bc.svg) | Dispersity, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Chain-class or mass-slice index. |

Average with equal weight per unit mass, giving long chains greater influence. The same 90:10 example gives Mw≈57,368.42 g/mol and Đ≈3.01939. For the same complete population with nonnegative weights, Đ≥1; broadening and integration truncation affect apparent values.

A concentration-sensitive SEC detector normally provides mass information before it provides anything related to molecule count. To calculate Mₙ from mass slices, divide each slice's mass by its assigned molar mass, obtaining a quantity proportional to the number of molecules. The total mass can then be divided by that total count-related quantity. A low-mass tail may contain little mass but many chains, making it influential for Mₙ. The constructed number and mass distributions in the figure therefore have different peak positions. This is a consequence of weighting. When software exports a distribution, check whether it is normalized by number or mass and whether the density is expressed per linear or logarithmic mass interval.

The real dataset comes from Ross and Frolen's 1972 NBS study of polyethylene SRM 1475. Points in the figure reproduce the published cumulative mass table: the vertical coordinate gives the percentage of mass below the indicated molar mass. Interpolation between neighboring entries on the logarithmic axis estimates a mass median. That statistic differs from the paper's reported Mₙ and M𝑤. The cumulative direction also differs from adding detector signal in elution order, where large molecules arrive first. Reading the axis direction is what makes a new plot of the historical table scientifically faithful.

![A replots published cumulative mass data from Ross and Frolen, NBS (1972), Table 4; the mass median uses linear interpolation in log M, preserving all printed values. B is a separate constructed population of 90 chains at 10,000 g/mol and 10 at 100,000 g/mol, compared by number and mass.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/b5b7cc9e6accd00e2e731172.svg?v=b5b7cc9e6acc)

Figure 3A replots published cumulative mass data from Ross and Frolen, NBS (1972), Table 4; the mass median uses linear interpolation in log M, preserving all printed values. B is a separate constructed population of 90 chains at 10,000 g/mol and 10 at 100,000 g/mol, compared by number and mass.

The complete example retains the table's printed values and rounding. It quotes the paper's moments for the aggregate distribution rather than deriving exact moments from a sparse cumulative table. The table answers a particularly intuitive question: what fraction of the material lies below a chosen mass threshold? Such thresholds can be useful when comparing release fragments or selecting fractions for another experiment. Number averages, weight averages, medians and threshold fractions each summarize a different feature. Choosing among them follows the research question, rather than a rule that one summary is universally the best.

## The column receives a prepared specimen, not an abstract material

A powder disappearing into liquid does not guarantee that every chain has reached a stable, uniformly dissolved state. High-mass material may dissolve slowly; crosslinked microgels may swell rather than dissolve; a protein may aggregate during the waiting period. Preparation therefore requires a solvent that dissolves the intended population while remaining compatible with the packing and detector. Temperature, dissolution time and mixing method help define that population. Strong mechanical treatment can change particularly vulnerable macromolecules, while temperature and buffer conditions can alter protein conformation and association. Preparation belongs within the measurement description because it determines what is actually measured.

Filtration removes particles that might obstruct a column, but it can also select the molecular population. An aggregate retained by a membrane will be absent from the subsequent chromatogram. Adsorption to the membrane can reduce recovery. Comparing concentration before and after preparation, inspecting sediment, and recording filter material help connect cleanliness with mass recovery. If soluble aggregates are the research target, choose a clarification procedure appropriate to that target and examine what it removes. For partially soluble network materials, the soluble mass fraction is similarly important: a clean SEC trace describes what entered the liquid phase, while the remaining network carries additional structural information.

Injection volume sets the initial width of the sample band. A long plug can make nearby populations overlap even when their mean retention differs. Excess concentration can also change viscosity, intermolecular interactions or local flow. A useful preliminary experiment changes concentration or injection volume while holding the other conditions fixed. Compare normalized profiles as well as total areas. Stable position and shape, together with a concentration-sensitive area that scales with loading, support the selected conditions. If an early peak decreases upon dilution, consider a shifting association equilibrium alongside reduced instrumental loading. Dilution is both a measurement adjustment and a possible change to the specimen.

A solvent blank, a narrow standard and a stable reference specimen answer different questions. The blank reveals disturbances associated with solvent and injection. A narrow standard checks position and system broadening. A stable reference monitors the method over time. Refractive-index detection responds to temperature and solvent differences, making equilibration and baseline stability especially valuable. Preparing a sample in a solvent unlike the mobile phase can introduce a disturbance near the low-mass tail. Automated integration may treat that disturbance as polymer. Comparing blank, standard and specimen traces exposes the problem before it is amplified by the calculation of a number average.

Keep the original time signal and the measured flow conditions. Time and volume are related but are not interchangeable labels: at stable flow, elapsed volume follows from flow rate multiplied by elapsed time. Comparing runs performed at different flows is clearer after expressing position on a consistent volume axis. Higher flow can change broadening and, for susceptible very large chains, introduce shear-related effects. Method selection balances separation, specimen stability and useful analysis time. A shorter run is valuable when it preserves the distinctions that the experiment is meant to measure.

## Broadening and shifting a peak tell different stories

The instrument spreads molecules that would otherwise arrive at nearly the same position. Different flow paths, exchange with pores, connecting tubes and the detector cell can all contribute. Observed width therefore includes both the specimen's distribution and the system's broadening. This is conspicuous for a narrow standard and may be a smaller relative contribution for a broad specimen. Our diagnostic model passes the same underlying population through three extra-broadening conditions, preserving total area and mean elution position. Interpreting all the added width as chain-length variation raises the apparent dispersity even though the molecular population has not changed.

A whole-peak shift creates a different effect. Suppose equal-mass chains become more compact and elute 0.5 mL later, while analysis continues to use the original calibration. The assigned masses are then multiplied by approximately 0.750. No bond is broken in this constructed operation, yet the apparent mass falls by about a quarter. When investigating degradation, comparable solvent, salt, temperature and calibration help separate this possibility from actual chain scission. Reaction chemistry, end-group information or additional detectors can then address the mechanism. When conformation itself is the research target, the position shift is useful information about size under the stated solution conditions.

Integration boundaries affect the answer as well. The late-eluting region corresponds to smaller molecules. Removing it discards many short chains and raises Mₙ. A relatively small early high-mass tail can strongly influence M𝑤. A reviewable analysis therefore shows the detector signal, baseline, integration boundaries and calibration, then examines reasonable changes to those choices. The endpoint scan in the figure holds the early boundary fixed and progressively includes the low-mass tail. The two averages converge at different rates. This transforms an isolated software result into a number whose sensitivity can be understood and discussed.

![Four diagnostics for the same constructed population. A and B add Gaussian instrumental broadening; C shifts elution while retaining the original calibration; D changes only the integration endpoint. The curves show how measurement choices change apparent distributions.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/28e37efc29d98b8dab05034b.svg?v=28e37efc29d9)

Figure 4Four diagnostics for the same constructed population. A and B add Gaussian instrumental broadening; C shifts elution while retaining the original calibration; D changes only the integration endpoint. The curves show how measurement choices change apparent distributions.

The interactive experiment retains two actual chain masses, 10,000 and 100,000 g/mol. First change the number fraction of long chains and observe when a small minority already contributes substantial mass. Next add system broadening and compare actual and apparent averages. Finally move the whole elution pattern to simulate a uniform mismatch between size and the calibration standard. These controls affect different parts of the measurement. Similar-looking changes in a curve do not always imply the same underlying population. Changing one control at a time and predicting the direction before reading the result develops a more useful understanding than moving every slider together.

## How the same chains acquire different apparent distributions

Chains have molar masses of 10,000 and 100,000 g/mol. Change one control at a time and compare actual and apparent averages. Gaussian broadening and a uniform position shift define this measurement model.

[Figure: Interactive mass-weighted chromatogram](https://ml-biomat.com/tutorials/experimental-methods/c02/en/#C02-plot)

An early shoulder in a new specimen suggests concrete follow-up work. Check whether it approaches the exclusion boundary, reduce loading to inspect peak shape, vary appropriate solution conditions to investigate reversible association, and collect the fraction for another method. A stable shift of the entire main peak suggests checking standards and flow conditions before testing degradation or conformational explanations. Each action distinguishes a particular hypothesis. SEC then becomes a decision point within a research sequence, linking preparation and fraction collection to structural and functional measurements.

## A complete analysis keeps the reasoning available for inspection

The example contains both constructed models and a published dataset, identified separately in the captions and data documentation. The constructed population has a normally distributed logarithmic molar mass. From that population, the program calculates a mass-weighted chromatogram and adds a controllable amount of instrument broadening. Known input averages can then be compared with apparent output averages to locate the bias. The published-data branch reads the NBS cumulative mass table, preserving nonuniform positions and printed rounding. It treats the table as a reported cumulative distribution. Standard points, chromatograms, broadening scans and integration scans are exported so that each step can be examined independently.

When reading the code, begin with the volume coordinate and calibration function, then locate normalization and the two moment calculations. Each small slice first has a mass weight. Dividing by the assigned molar mass produces the corresponding count-related weight. Numerical integration approximates the area under a continuous curve and includes coordinate spacing. If you replace the constructed grid with irregularly sampled measurements, provide the actual coordinates to the integration function. Adding heights alone has the appropriate meaning only when sampling intervals are equal and the omitted proportional factor cancels in the intended ratio.

### Complete SEC distribution, calibration and diagnostic example

Constructed models and the published cumulative dataset are processed separately, with four figures and inspectable calibration, chromatogram, broadening and integration tables.

```
"""SEC/GPC: porous exclusion, calibration, mass weighting and real NBS data.

Run: python main.py --output results --language en
Dependencies: numpy, scipy, matplotlib. Only bundled data are read.
All chromatograms are constructed teaching models. The cumulative SRM curve
is a transcription of the published NBS 1972 table, identified in data/README.md.
"""
from pathlib import Path
import argparse, csv, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch

P=argparse.ArgumentParser();P.add_argument('--output',type=Path,required=True);P.add_argument('--language',choices=['zh','en'],default='en');args=P.parse_args()
O=args.output;O.mkdir(parents=True,exist_ok=True);L=args.language
def t(z,e):return z if L=='zh' else e
plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#25364a','text.color':'#25364a','axes.titleweight':'bold','figure.facecolor':'#fcfbf7','axes.facecolor':'#fcfbf7','svg.fonttype':'none','savefig.facecolor':'#fcfbf7'})
blue='#167d9a';red='#d35f47';gold='#c49b35';dark='#25364a';green='#37967d'
def save(fig,n):
    fig.savefig(O/f'{n}-{L}.svg',bbox_inches='tight');fig.savefig(O/f'{n}-{L}.png',dpi=145,bbox_inches='tight');plt.close(fig)
def gauss(x,m,s):return np.exp(-.5*((x-m)/s)**2)/(s*np.sqrt(2*np.pi))
def csvsave(n,h,a):np.savetxt(O/n,a,delimiter=',',header=','.join(h),comments='',fmt='%.10g')

# Original mechanism drawing. Side pores hold solvent; macromolecules exchange
# with accessible pore volume. They are not forced through a sieve membrane.
fig,axs=plt.subplots(1,3,figsize=(14.4,4.5),gridspec_kw={'width_ratios':[1.1,1,1]},layout='constrained')
ax=axs[0];ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off')
ax.add_patch(Rectangle((.4,1),9.1,5.5,facecolor='#e8f0f0',edgecolor='#9aafaf',lw=1.5))
for x,y in [(2,2.4),(5,5),(8,2.4)]:
    ax.add_patch(Circle((x,y),1.1,facecolor='#d6dfd9',edgecolor='#829a8b'))
    for dx,dy in [(-.3,.3),(.35,.1),(0,-.4)]:ax.add_patch(Circle((x+dx,y+dy),.20,facecolor='#fcfbf7',edgecolor='#b4c5bb'))
ax.plot([.5,2,3.3,4,6,7.2,9.3],[4,4,4,3.3,3.3,4.6,4.6],color=red,lw=3)
ax.scatter([.7,9],[4,4.6],s=120,color=red,zorder=5)
ax.plot([.5,2,2,3.4,5,5,6.4,8,8,9.3],[3.4,3.4,2.3,3.4,3.4,4.7,3.6,3.6,2.3,3.6],color=blue,lw=1.8,ls='--')
ax.scatter([.7,9],[3.4,3.55],s=20,color=blue,zorder=5)
ax.text(.5,7.25,t('A  多孔填料中的两种可达空间','A  Two accessible solvent spaces'),weight='bold')
ax.text(.55,.35,t('大分子：孔外较多  /  小分子：也进入孔内','Large: mostly outside  /  Small: also inside'),fontsize=10)
v=np.linspace(0,22,1000);ax=axs[1]
ax.plot(v,gauss(v,8,.6),color=red,label=t('大分子','Macromolecule'));ax.plot(v,gauss(v,16,.8),color=blue,label=t('小分子盐','Small solute / salt'))
ax.axvspan(6,10,color=red,alpha=.09);ax.set(xlabel=t('洗脱体积 / mL','Elution volume / mL'),ylabel=t('归一化检测信号 / mL⁻¹','Normalized signal / mL⁻¹'),title=t('B  脱盐：先收集大分子','B  Desalting: collect the first band'));ax.legend(frameon=False,fontsize=9)
ax=axs[2];vol=np.linspace(3,18,100);ax.plot(vol,(vol-3)/15,color=green,lw=2.5)
ax.scatter([3,9,18],[0,.4,1],color=[red,gold,blue],zorder=5);ax.set(xlabel=t('洗脱体积 / mL','Elution volume / mL'),ylabel=t('孔体积可达比例 Kav','Accessible fraction Kav'),ylim=(-.06,1.1),title=t('C  在两个参照体积之间','C  Between two reference volumes'))
ax.annotate(t('完全排阻','Excluded'),(3,0),(5,.07),arrowprops={'arrowstyle':'-','color':dark},fontsize=9);ax.annotate(t('完全进入','Fully included'),(18,1),(12,.82),arrowprops={'arrowstyle':'-','color':dark},fontsize=9)
save(fig,'pores')

# Constructed narrow-standard calibration and lognormal molecular population.
a,b=7.,.25;standards=np.array([1e3,3e3,1e4,3e4,1e5,3e5,1e6]);ve=(a-np.log10(standards))/b
mu,s=4.2,.35;ln10=np.log(10);mass_mu=mu+ln10*s*s
V=np.linspace(2,20,6001);M=10**(a-b*V);ideal=gauss(V,(a-mass_mu)/b,s/b)
def moments(signal):
    area=np.trapezoid(signal,V)
    return float(area/np.trapezoid(signal/M,V)),float(np.trapezoid(signal*M,V)/area)
Mn=10**mu*np.exp(.5*(ln10*s)**2);Mw=10**mu*np.exp(1.5*(ln10*s)**2);disp=Mw/Mn
sig=.25;observed=gauss(V,(a-mass_mu)/b,np.sqrt((s/b)**2+sig**2));mn_obs,mw_obs=moments(observed)
fig,axs=plt.subplots(2,2,figsize=(12.8,8),layout='constrained')
ax=axs[0,0];ax.plot(ve,standards,'o-',color=blue);ax.set_yscale('log');ax.set(xlabel=t('标准样峰位 / mL','Standard peak volume / mL'),ylabel=t('摩尔质量 / (g/mol)','Molar mass / (g/mol)'),title=t('A  先校准位置','A  Calibrate position first'));ax.text(.04,.1,'log₁₀ M = 7 − 0.25 V',transform=ax.transAxes)
ax=axs[0,1];ax.plot(V,observed,color=blue);ax.fill_between(V,observed,where=(V>10)&(V<11),color=gold,alpha=.5);ax.set(xlim=(4,17),xlabel=t('洗脱体积 / mL','Elution volume / mL'),ylabel=t('质量响应 / mL⁻¹','Mass response / mL⁻¹'),title=t('B  面积切片包含质量','B  Each slice contains mass'))
x=np.linspace(2.5,6.5,1000);ax=axs[1,0];ax.plot(x,gauss(x,mu,s),color=green,label=t('按链数归一化','Number density'));ax.plot(x,gauss(x,mass_mu,s),color=red,label=t('按质量归一化','Mass density'));ax.set(xlabel=t('log₁₀ [M / (g/mol)]','log₁₀ [M / (g/mol)]'),ylabel=t('每单位 log₁₀ M 的概率密度','Density per unit log₁₀ M'),title=t('C  同一群链，两种加权','C  Same chains, two weightings'));ax.legend(frameon=False)
ax=axs[1,1];ax.plot(V,np.cumsum(observed)/np.sum(observed)*100,color=blue);ax.set(xlim=(4,17),xlabel=t('洗脱体积 / mL','Elution volume / mL'),ylabel=t('已流出质量 / %','Eluted mass / %'),title=t('D  先流出的是大分子','D  Larger molecules elute first'));ax.text(.03,.84,t('此累计方向：大 → 小','This cumulative direction: large → small'),transform=ax.transAxes)
save(fig,'calibration')
csvsave('calibration.csv',['elution_volume_mL','molar_mass_g_per_mol'],np.c_[ve,standards])
csvsave('constructed_chromatogram.csv',['elution_volume_mL','assigned_molar_mass_g_per_mol','ideal_mass_response_per_mL','broadened_mass_response_per_mL'],np.c_[V,M,ideal,observed])

raw=np.genfromtxt(Path(__file__).parent/'data/srm1475_table4.csv',delimiter=',',names=True)
logm=raw['log10_molar_mass_g_per_mol'];cdf=raw['cumulative_mass_percent'];median=10**np.interp(50,cdf,logm)
assert np.all(np.diff(logm)>0) and np.all(np.diff(cdf)>=0) and cdf[0]==0 and cdf[-1]==100
fig,axs=plt.subplots(1,2,figsize=(12.8,4.9),layout='constrained')
ax=axs[0];ax.semilogx(10**logm,cdf,'o-',color=blue,ms=3);ax.axhline(50,color=gold,ls='--',lw=1);ax.axvline(median,color=gold,ls='--',lw=1)
ax.set(xlabel=t('摩尔质量 / (g/mol)','Molar mass / (g/mol)'),ylabel=t('低于横坐标的累计质量 / %','Cumulative mass below M / %'),title=t('A  真实公开数据：聚乙烯 SRM 1475','A  Published data: polyethylene SRM 1475'),ylim=(-2,103))
ax.text(.05,.68,t('1972 年 NBS，表 4\n按质量的中位数 ≈ ','NBS 1972, Table 4\nMass median ≈ ')+f'{median:,.0f} g/mol',transform=ax.transAxes,fontsize=10)
ax=axs[1];xx=np.arange(2);nw=np.array([.9,.1]);ww=np.array([.9*1e4,.1*1e5]);ww/=ww.sum()
ax.bar(xx-.18,nw*100,.34,color=green,label=t('链数占比','Number fraction'));ax.bar(xx+.18,ww*100,.34,color=red,label=t('质量占比','Mass fraction'))
ax.set_xticks(xx,['10,000 g/mol','100,000 g/mol']);ax.set(ylim=(0,110),ylabel=t('占比 / %','Fraction / %'),title=t('B  构造例：90 条短链与 10 条长链','B  Constructed: 90 short and 10 long chains'));ax.legend(frameon=False,ncol=2,loc='upper right',fontsize=9)
for p in ax.patches:ax.text(p.get_x()+p.get_width()/2,p.get_height()+2,f'{p.get_height():.1f}',ha='center',fontsize=10)
save(fig,'mass-distribution')

widths=np.linspace(0,1.2,61);factor=np.exp((ln10*b*widths)**2);rows=[]
fig,axs=plt.subplots(2,2,figsize=(12.8,8),layout='constrained')
ax=axs[0,0]
for w,c in zip([0,.6,1.2],[blue,gold,red]):
    y=gauss(V,(a-mass_mu)/b,np.sqrt((s/b)**2+w*w));ax.plot(V,y,color=c,label=f'σV = {w:.1f} mL')
ax.set(xlim=(4,17),xlabel=t('洗脱体积 / mL','Elution volume / mL'),ylabel=t('质量响应 / mL⁻¹','Mass response / mL⁻¹'),title=t('A  仪器把同一分布展宽','A  Instrument broadening'));ax.legend(frameon=False,fontsize=9)
ax=axs[0,1];ax.plot(widths,disp*factor,color=red);ax.axhline(disp,color=green,ls='--',label=t('真实分散系数','True dispersity'));ax.set(xlabel=t('额外展宽 σV / mL','Extra broadening σV / mL'),ylabel=t('表观分散系数','Apparent dispersity'),title=t('B  展宽被误读为链长差异','B  Width becomes apparent heterogeneity'));ax.legend(frameon=False)
shifts=np.linspace(0,1.2,100);ax=axs[1,0];ax.plot(shifts,100*10**(-b*shifts),color=blue);ax.set(xlabel=t('向后移动的峰位 / mL','Later elution shift / mL'),ylabel=t('表观质量 / 真值 × 100%','Apparent / true mass × 100%'),title=t('C  同一质量，构象变紧凑','C  Same mass, more compact conformation'),ylim=(45,105))
ax=axs[1,1];cuts=np.linspace(12,18,70);mns=[];mws=[]
for cut in cuts:
    keep=V<=cut;ar=np.trapezoid(ideal[keep],V[keep]);mns.append(ar/np.trapezoid((ideal/M)[keep],V[keep]));mws.append(np.trapezoid((ideal*M)[keep],V[keep])/ar)
ax.plot(cuts,np.array(mns)/Mn,color=green,label='Mn');ax.plot(cuts,np.array(mws)/Mw,color=red,label='Mw');ax.axhline(1,color=dark,lw=.8,ls='--');ax.set(xlabel=t('积分终点 / mL','Integration endpoint / mL'),ylabel=t('截取值 / 完整值','Truncated / full value'),title=t('D  删掉小分子尾部的代价','D  Cost of deleting the low-mass tail'));ax.legend(frameon=False)
save(fig,'diagnostics')
csvsave('broadening.csv',['extra_sigma_mL','apparent_dispersity_analytic'],np.c_[widths,disp*factor])
csvsave('integration_sensitivity.csv',['integration_endpoint_mL','Mn_g_per_mol','Mw_g_per_mol'],np.c_[cuts,mns,mws])
toy_mn=.9*1e4+.1*1e5;toy_mw=(.9*1e8+.1*1e10)/toy_mn
summary={'Kav_example':.4,'toy_Mn_g_per_mol':toy_mn,'toy_Mw_g_per_mol':toy_mw,'toy_dispersity':toy_mw/toy_mn,'lognormal_true_Mn':float(Mn),'lognormal_true_Mw':float(Mw),'lognormal_true_dispersity':float(disp),'broadened_Mn':mn_obs,'broadened_Mw':mw_obs,'broadened_dispersity':mw_obs/mn_obs,'NBS_table_rows':len(raw),'NBS_mass_median_log_interpolation_g_per_mol':float(median),'NBS_reported_Mn_g_per_mol':17900,'NBS_reported_Mw_g_per_mol':52900,'NBS_reported_dispersity':52900/17900,'half_mL_shift_mass_ratio':10**(-.25*.5)}
assert abs(toy_mn-19000)<1e-8 and abs(toy_mw-57368.42105263158)<1e-7
assert abs(mn_obs/(Mn*np.exp(-.5*(ln10*b*sig)**2))-1)<1e-5
assert abs(mw_obs/(Mw*np.exp(.5*(ln10*b*sig)**2))-1)<1e-5
(O/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
```

A useful final statement answers a specific experiment: under matched solvent, temperature, standards and integration rules, did the soluble distribution change, and was the change concentrated in the main peak, low-mass tail or early shoulder? For a protein separation, which collected fraction contains the size population needed for the next experiment, and how much material was recovered? Retaining the distribution, both averages and the measurement conditions supports those questions better than preserving a single molecular-weight number. Mass spectrometry, in the next chapter, approaches molecules through ion mass-to-charge ratios, providing a complementary separation principle to the solution-size distribution studied here.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/C02.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Waters: Calibration of the GPC system](https://www.waters.com/nextgen/us/en/education/primers/beginners-guide-to-size-exclusion-chromatography/calibration-of-the-gpc-system1.html)

   Conditions behind conventional, relative and universal calibration.
2. [Cytiva: Size exclusion chromatography selection guide](https://cdn.cytivalifesciences.com/api/public/content/digi-13947-pdf)

   Pores, desalting versus high-resolution fractionation, sample volume.
3. [Porath: Citation Classic retrospective on gel filtration](https://garfield.library.upenn.edu/classics1981/A1981LM54000002.pdf)

   Porath’s firsthand retrospective on starch columns and crosslinked dextran.
4. [NIST author manuscript: Size-exclusion chromatography](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=933552)

   SEC history, equilibrium size partitioning, extra interactions and broadening.
5. [Malvern Panalytical: An introduction to SEC/GPC](https://www.malvernpanalytical.com/en/learn/knowledge-center/whitepapers/wp150625introtosecgpc)

   Solution size, detectors and interpretation of molar mass.
6. [Ross and Frolen (1972): Polyethylene SRM 1475, gel permeation chromatography](https://nvlpubs.nist.gov/nistpubs/jres/76A/jresv76An2p163_A1b.pdf)

   Real cumulative mass data from Table 4 and reported moments for that distribution.

   NBS government-authored numerical table; reproduced with attribution under NIST public-information policy.
