# Mass spectrometry: Identifying molecules through mass and charge

Source: https://ml-biomat.com/tutorials/experimental-methods/c03/en/
Language: en

Use ions to connect mass, charge, fragmentation and concentration in a stepwise molecular investigation.

## Turning “looks like caffeine” into a testable identification

Coffee contains many molecules that absorb ultraviolet light. Liquid chromatography separates them, and a peak appearing near the retention time of a caffeine standard provides a useful clue. Mass spectrometry adds further questions: does the observed ion mass agree with caffeine's composition, do controlled collisions generate a comparable fragment pattern, and what changes when an authentic standard is added? These questions extend the same evidence chain. They are relevant to small molecules in drinks, synthetic peptides, degradation products released by a material, and polymer families whose neighboring members differ by a repeating structural unit.

A mass spectrometer does not place a molecule on a miniature balance. It first produces charged particles, or ions, then uses electric or magnetic fields to control their motion and records signals related to mass-to-charge ratio. Increasing mass and increasing charge affect that motion differently. A large molecule carrying many charges can appear at a relatively low mass-to-charge value. Ten peaks therefore need not mean ten different molecules, and a peak position need not equal the mass of the original neutral molecule. Once these two points are clear, a complicated spectrum becomes a set of questions that can be addressed in a sensible order.

This chapter connects identification and quantitation. Identification asks which candidate molecule agrees with the observed ions and what structural information distinguishes the remaining candidates. Quantitation asks how the response relates to the amount in the specimen and whether extraction or ionization changes that relationship. Mass, isotope patterns, fragments and chromatographic behavior help with the first task. Standards, internal standards, blanks and matrix-effect experiments support the second. This distinction explains why a clean-looking spectrum can coexist with an inaccurate concentration: the efficiency of generating the signal may still require investigation.

We will read an openly shared reference tandem mass spectrum of caffeine, preserving its measured peak positions and intensities. Separate constructed examples isolate charge states, resolving power, extraction of chromatograms and response suppression. The reference record teaches us to inspect actual acquisition information, while controlled models let one measurement condition change at a time. Together they lead from specimen introduction to an interpretable research result. The final program includes the data and displays its outputs within the chapter.

## Getting an intact molecule into the measurable ion population

An electric field readily acts on an ion, but it cannot select a completely neutral molecule in the same way. The ion source is therefore the entrance connecting specimen chemistry to the analyzer. Electron ionization is common for small molecules that can enter the gas phase and often produces informative fragments. Electrospray ionization, or ESI, begins with a solution and generates charged droplets. Solvent evaporation, droplet evolution and ion release bring some analyte into the gas phase, after which an interface transfers ions toward lower pressure. Different ion-release mechanisms describe different kinds of analyte; the shared result is a charged form that the analyzer can manipulate.

This entrance was a central challenge for biological macromolecules. Heating a large, fragile protein enough to vaporize it could alter or decompose it first. In their 1989 paper, Fenn and colleagues described intact large ions and coherent series of multiply charged peaks produced by electrospray. Multiple charging made interpretation more complicated, yet also placed very large molecules within a measurable mass-to-charge range. Our original droplet diagram and charge-series illustration focus on the physical problem that this development addressed: transferring a large molecule from solution into a useful population of gas-phase ions.

Laser desorption offers another route. Analyte is combined with a matrix that supports absorption and transfer of energy, and a laser pulse releases material and produces ions. Koichi Tanaka's team reported soft laser desorption results for high-mass molecules in 1987. Matrix-assisted laser desorption/ionization, MALDI, subsequently became important for proteins, peptides and certain polymers. The diagram illustrates the relationship between matrix, laser and released ions without assigning every modern MALDI implementation to a single discovery. Both approaches aim to deliver sufficiently intact target ions; controlled fragmentation can then be introduced deliberately when structural information is needed.

A time-of-flight analyzer gives an accessible example of mass analysis. Passing through the same accelerating potential gives an ion more electrical energy when it carries more charge. At equal charge, a heavier ion acquires a lower speed because more mass must share that energy. It then takes longer to traverse the same drift distance. Relating electrical energy to kinetic energy gives the following expression. It describes ideal acceleration and field-free drift with negligible initial velocity. Real instruments also account for starting time, energy spread and flight-path design.

$$
zeU=\tfrac12mv^2,\qquad t=\frac{L}{v}=L\sqrt{\frac{m}{2zeU}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9032cb23a878659e74b670d3.svg) | Positive ion charge number, positive integer. |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | Elementary charge, 1.602176634×10⁻¹⁹ C. |
| ![Formula](https://ml-biomat.com/static/agent-math/c3ae10e66e0dee45c359329a.svg) | Magnitude of accelerating potential, V. |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Ion mass, kg; 400 Da≈6.64216×10⁻²⁵ kg. |
| ![Formula](https://ml-biomat.com/static/agent-math/6ea26af94b3e02fd7aa1d744.svg) | Speed after ideal acceleration, m/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Field-free flight distance, m. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Flight time, s; converted to microseconds in the plot. |

Neglecting initial kinetic energy, electrical energy becomes kinetic energy; flight time is distance divided by speed. L=1 m, U=5000 V, z=1 and m=400 Da give t≈20.36 microseconds. Fourfold mass doubles the time.

![Original electrospray, laser/matrix and ideal flight-time diagrams connect Fenn et al. (1989) and the Tanaka team’s 1987 soft-desorption reports. Dimensions are schematic; the calculation uses 1 m, 5 kV and single charge.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/4654fb51734294e73da12d11.svg?v=4654fb517342)

Figure 1Original electrospray, laser/matrix and ideal flight-time diagrams connect Fenn et al. (1989) and the Tanaka team’s 1987 soft-desorption reports. Dimensions are schematic; the calculation uses 1 m, 5 kV and single charge.

Other analyzers implement different ways of controlling or measuring motion. A quadrupole applies electric fields that allow a selected mass-to-charge range to follow suitable trajectories through the rods. Traps retain ions, while other designs infer mass-to-charge ratio from characteristic motion. The useful choice depends on the experiment: quantifying a few known targets, screening unknowns, resolving nearby masses or recording narrow chromatographic peaks impose different demands. Detectors convert arriving ions or their motion into electrical information, and processing maps that signal onto a mass-to-charge axis. Performance belongs to this complete measurement chain, rather than to an instrument name alone.

## Why one molecule can make many peaks

Start with a constructed neutral molecule of mass 12,000 Da. A dalton is a convenient unit for the mass of an individual molecule or ion. Adding six protons produces six positive charges and a mass-to-charge value near 2001.0073. Adding twelve gives a value near 1001.0073. Both peaks arise from the same neutral molecule with different charge states. Charges can be imagined as handles through which the field acts: more handles on the same mass change its response. The analogy explains the need to consider mass and charge together; it is not a picture of literal mechanical handles on the molecule.

$$
\mu=\frac{M_r+zh}{z},\qquad M_r=z(\mu-h)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | Numerical m/z coordinate in the conventional Da/e scale. |
| ![Formula](https://ml-biomat.com/static/agent-math/74c324121c11267490a2341c.svg) | Neutral relative molecular mass: its mass divided by 1 Da, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/9032cb23a878659e74b670d3.svg) | Positive charge number from proton addition, positive integer. |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | Proton mass divided by 1 Da, approximately 1.007276466579, dimensionless. |

For [M+zH]z+, add the mass of z protons and divide by charge. Mᵣ=12,000 and z=12 give μ≈1001.007276, which reconstructs 12,000. Other adducts require the appropriate composition term.

A protonated ion is often written [M+H]⁺, while a deprotonated negative ion is written [M−H]⁻. Sodium adducts, other adducts and ions containing more than one molecule may also occur. The brackets describe the ion actually detected. High-accuracy calculations must distinguish a proton from a neutral hydrogen atom, which also contains an electron. For a singly protonated molecule, add approximately 1.007276 Da to the neutral monoisotopic mass. Adding one to an average molecular mass from a general property table and comparing many decimal places would mix different definitions of mass.

Monoisotopic mass starts with isotopes. Atoms of an element have the same proton count but can differ in neutron count. Carbon is mainly carbon-12, with a smaller amount of carbon-13. In a population of carbon-containing molecules, some contain only carbon-12, some contain one carbon-13 and some contain two. A single chemical composition therefore produces a family of nearby masses. Other elements also contribute isotope patterns. Our simplified illustration varies only the number of carbon-13 atoms among fifty carbon sites so that the influence of charge on spacing can be seen separately from a full molecular isotope calculation.

Replacing carbon-12 by carbon-13 adds approximately 1.003355 Da. The resulting spacing is about 1.003355 in mass-to-charge units for a singly charged ion, 0.501677 for a doubly charged ion and 0.334452 for a triply charged ion. A series near half-unit spacing is therefore evidence for double charging when the peaks are resolved and nearby signals are understood. Once charge is assigned, several peaks can be transformed back to a common neutral mass. Agreement across charge states constrains the interpretation more strongly than simply reading the tallest peak.

![All panels are constructed. A shows charge states 6+ through 12+ for one 12,000 Da molecule. B uses only carbon-13 variation among 50 sites, vertically offset by charge. C compares two ions 0.01435 apart at different FWHM resolving powers, vertically offset.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/e1853d351b3c0d64495ae0bb.svg?v=e1853d351b3c)

Figure 2All panels are constructed. A shows charge states 6+ through 12+ for one 12,000 Da molecule. B uses only carbon-13 variation among 50 sites, vertically offset by charge. C compares two ions 0.01435 apart at different FWHM resolving powers, vertically offset.

Polymers introduce another reason for regular peak series. Neighboring chains may differ by one repeating unit, producing a fixed neutral-mass increment. If the charge state is two, the observed spacing is half that increment. End groups and the attached ion shift the whole series. Interpretation therefore connects repeating unit, end groups, adduct and charge state. A biomolecular charge-state envelope and a polymer homologous series can both look orderly while representing different changing variables. Writing down which variable is changing prevents an attractive regular pattern from becoming an unsupported structural assignment.

## Position, width and fragments provide different information

The horizontal coordinate of a mass spectrum is mass-to-charge ratio, and the vertical coordinate is signal intensity. An instrument may record a continuous profile or produce a processed list of peak positions and intensities, often displayed as vertical sticks. The most intense peak is called the base peak. Setting it to one hundred percent and scaling the others accordingly makes patterns easier to compare. That percentage is an internal plotting reference. It is neither specimen purity nor the fraction of all molecules represented by the peak. Ionization, transmission and fragmentation efficiencies differ, so relative peak heights are not automatically mixture mass fractions.

Mass accuracy and resolving power address different properties. Accuracy concerns the distance between a measured center and the expected position, commonly expressed as a relative error in parts per million. Resolving power concerns peak width at a specified mass-to-charge value and the ability to distinguish nearby ions. In the constructed figure, two close masses form a broad combined feature at lower resolving power and separate at higher resolving power. A narrow peak can still be displaced by calibration error, while a broad feature centered near an expected value can contain more than one ion. Calibration, shape, ion abundance and nearby interference should therefore be inspected together.

$$
R=\frac{\mu}{\Delta\mu_{\mathrm{FWHM}}},\qquad \epsilon_{\mathrm{ppm}}=10^6\frac{\mu_{\mathrm{measured}}-\mu_{\mathrm{theory}}}{\mu_{\mathrm{theory}}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | Resolving power defined at full width at half maximum, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | Numerical m/z coordinate of the peak. |
| ![Formula](https://ml-biomat.com/static/agent-math/8ff1b2b09c124f9145acbad7.svg) | Full width at half maximum on the same coordinate scale as μ. |
| ![Formula](https://ml-biomat.com/static/agent-math/9da3797043bf140e00a4f1c3.svg) | Relative mass error expressed numerically in parts per million. |
| ![Formula](https://ml-biomat.com/static/agent-math/e6c6cab688b1542e9c4cd71c.svg) | Measured and theoretical m/z values for the specified ion composition. |

Position relative to width defines resolving power; center displacement relative to theory defines error. μ≈195.087652 and R=40,000 give FWHM≈0.00487719; a +0.001 shift is about +5.126 ppm. These describe different performance properties.

The real caffeine record gives formula C₈H₁₀N₄O₂. Summing the selected atomic isotope masses gives a neutral monoisotopic mass near 194.080376 Da and a theoretical protonated value near 195.087652. The record's precursor metadata reports 195.0877, whereas a retained peak in the product-ion list is at 195.0873; the example preserves these distinct entries. The strongest recorded product peak is at 138.0657. Positive electrospray, a quadrupole time-of-flight instrument and a 40 V collision setting define the acquisition. It is therefore a reference tandem spectrum under stated conditions, rather than a spectrum of untouched neutral molecules.

![Actual caffeine reference spectrum MSBNK-BAFG-CSL2311094663, positive LC-ESI-QTOF, CID, 40 V. Data: Björn Ehlig, Ole Lessmann, Kevin S. Jewell and Arne Wick, Federal Institute of Hydrology, CC BY. All 23 peaks are retained; original intensity is normalized to 100%. Theory, precursor metadata and retained spectral peak remain distinct.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/cf6fb4cb66ae490ba3350c5d.svg?v=cf6fb4cb66ae)

Figure 3Actual caffeine reference spectrum MSBNK-BAFG-CSL2311094663, positive LC-ESI-QTOF, CID, 40 V. Data: Björn Ehlig, Ole Lessmann, Kevin S. Jewell and Arne Wick, Federal Institute of Hydrology, CC BY. All 23 peaks are retained; original intensity is normalized to 100%. Theory, precursor metadata and retained spectral peak remain distinct.

Tandem mass spectrometry follows a sequence of selection, transformation and analysis. Select a precursor-ion range, induce fragmentation through collisions or another process, then analyze the products. Molecules with the same elemental composition may have different connectivity and produce different fragment combinations. Comparing product spectra can therefore add structural discrimination. Check precursor form, polarity, collision conditions and recording method when comparing a reference: one molecule can redistribute intensity substantially as collision conditions change. If the selected precursor window contains another ion, the products may also have mixed origins, making chromatographic separation and a suitable isolation window valuable.

Accurate mass excludes many incompatible compositions, but connectivity and stereochemistry require additional information. Identification usually narrows progressively: establish a plausible ion form and charge, inspect mass and isotope pattern, compare products and retention behavior, then use a standard or another structural method where the question requires it. Describing agreement with a named reference under specified conditions places the evidence on an inspectable object. Each independent observation narrows the remaining explanations. This is particularly useful when a material produces several chemically related degradation products whose masses alone look convincing.

## LC-MS is a map unfolding in time

Combining liquid chromatography with mass spectrometry creates more than one curve. Each time point has a mass spectrum, and stacking them produces a map of time, mass-to-charge ratio and intensity. A spot means that an ion appears during a particular interval. Summing signals over the acquired mass range gives a total-ion chromatogram. Summing within a selected mass window gives an extracted-ion chromatogram, often abbreviated XIC or EIC. The total shown in our figure covers only the narrow displayed mass interval, which isolates the target and a neighboring interference. An instrument's full total-ion trace covers its actual acquisition range.

An extraction window resembles a narrow corridor drawn through that map. A broad corridor admits nearby ions and can increase area or create a shoulder. A very narrow one can lose target signal when the center drifts or the profile has appreciable width. A window specified in parts per million has an absolute width that changes with mass-to-charge value. Selection should therefore reflect mass stability, resolving power and recording format. Extracting the same constructed dataset with ±5 ppm and ±100 ppm makes the consequence visible: the wider choice includes a neighboring ion that elutes somewhat later.

![Fixed-seed constructed LC-MS data: target at 4.0 min, neighbor at 4.4 min, mass separation 0.01435 and R=40,000. Heatmap uses log₁₀(1+signal). Each right-hand curve is normalized to its own maximum for shape comparison, not absolute area comparison. Total signal covers only the displayed mass window.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/0e41106e5cbefc44d162c353.svg?v=0e41106e5cbe)

Figure 4Fixed-seed constructed LC-MS data: target at 4.0 min, neighbor at 4.4 min, mass separation 0.01435 and R=40,000. Heatmap uses log₁₀(1+signal). Each right-hand curve is normalized to its own maximum for shape comparison, not absolute area comparison. Total signal covers only the displayed mass window.

Time also has resolution. A chromatographic peak only a few seconds wide needs enough scans across its profile for stable shape and area measurements. Longer scans and larger lists of monitored targets reduce the time available for each observation. Acquisition settings should coordinate mass information with chromatographic sampling. For known targets, monitoring selected precursor-to-product transitions can reduce irrelevant signal. For unknown screening, broader coverage and traceable fragmentation information become more important. These strategies optimize different questions; a single claim of higher sensitivity does not describe every tradeoff.

Solvent and salt are part of the electrospray measurement. Nonvolatile buffers, detergents and abundant accompanying solutes in a protein preparation can affect droplet formation, evaporation and target-ion production. Compatible volatile mobile phases, cleanup or dilution may improve the analysis, but each preparation step can also lose analyte. Extraction should be designed around solubility, stability and adsorption. A method suitable for caffeine is not a universal preparation for peptides, polysaccharides and polymers. For time-sensitive specimens, storage conditions and analytical order should make the interval between preparation and measurement comparable.

In a material-release experiment, compare the original material, release liquid, container blank and solvent blank within the same analytical design. A feature also present in the container blank suggests a contribution from the vessel or processing. A feature increasing after treatment becomes a candidate for further chemical interpretation using mass and product ions. Overlaying blanks and samples on the same coordinates exposes these relationships directly. It also helps decide which signals deserve fraction collection, an authentic standard or another structural measurement before the discussion turns to a mechanism of release.

## The same amount can generate less signal

Add the same concentration of caffeine to neat solvent and to a processed specimen extract. The extract may give a weaker response even though the amount added is identical. Accompanying material has altered the response, producing a matrix effect. To separate this from extraction loss, add a known amount after extraction and compare its response with the same concentration in neat solvent. A response equal to fifty-five percent of the neat signal gives a matrix factor of 0.55. Comparing a pre-extraction spike with a corresponding post-extraction spike then addresses recovery through preparation. Keeping the spike timing explicit connects each comparison to the stage it measures.

$$
\mathrm{MF}=\frac{A_{\mathrm{post}}}{A_{\mathrm{neat}}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c7daa1ef3fa0bc9c86be752f.svg) | Matrix factor, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/e9a43225a844d0d4bf10d657.svg) | Net analyte peak area after spiking the extracted matrix. |
| ![Formula](https://ml-biomat.com/static/agent-math/13e8115a017499920ae8842a.svg) | Net peak area at the same analyte concentration in neat solvent, with matching units. |

At equal concentration and matched introduction conditions, compare response after suitable blank correction. Neat area 10,000 and matrix area 5,500 give MF=0.55. This post-extraction comparison addresses a different stage from extraction recovery.

An internal standard supplies a reference that travels with the specimen. Add a known amount of a distinguishable compound to samples and calibration solutions, then divide analyte peak area by internal-standard peak area. If injection and ionization affect both by the same multiplicative factor, that factor cancels. A stable-isotope-labeled version of the target is often useful because it combines similar chemical behavior with a distinguishable mass. Addition timing determines which stages it can track. A standard added after extraction accompanies later measurement changes, while earlier losses need a preparation-stage comparison.

The ratio needs verification too. Suppose the analyte response falls to fifty-five percent while the standard remains at eighty percent. Division retains a bias because the two responses did not change together. The diagnostic figure plots this relationship directly. Choosing an internal standard therefore means more than finding a convenient nearby peak: examine its retention, extraction recovery and matrix response across relevant specimens. Coelution helps the compounds experience similar surroundings, while isotope overlap, channel cross-talk and standard purity also require attention in the specific method.

$$
r=\frac{A}{A_{\mathrm{IS}}}=sc+b,\qquad c=\frac{r-b}{s}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | Analyte/internal-standard peak-area ratio, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Analyte peak area in units consistent with the internal standard. |
| ![Formula](https://ml-biomat.com/static/agent-math/a182fb4a475d2faaa4f36411.svg) | Internal-standard peak area; a fixed known standard amount is used across relevant solutions. |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | Ratio-calibration slope, mL/ng. |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | Analyte concentration in the injected solution, ng/mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Ratio-calibration intercept, dimensionless. |

Shared multiplicative changes cancel in the ratio. s=0.08 mL/ng, b=0.01 and r=0.65 give c=8 ng/mL. The interactive model uses background-corrected b=0; differing analyte and standard response factors leave their ratio as a bias.

![Constructed matrix and calibration experiments. A compares equal-concentration post-extraction spikes. B and D use a true concentration of 8 ng/mL with matched or mismatched suppression. C has three replicates per concentration around the relationship 0.08c+0.01, fitted from noisy responses.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d2eaf35c3898d3ffcc16352e.svg?v=d2eaf35c3898)

Figure 5Constructed matrix and calibration experiments. A compares equal-concentration post-extraction spikes. B and D use a true concentration of 8 ng/mL with matched or mismatched suppression. C has three replicates per concentration around the relationship 0.08c+0.01, fitted from noisy responses.

The interactive experiment varies actual concentration, analyte response factor and internal-standard response factor separately. Neat-solvent external calibration interprets a suppressed response as a lower concentration. A matched response ratio recovers the original concentration when analyte and standard share the same suppression. A mismatch produces a remaining bias. Bar height represents response, while the calculated results show concentration with its own units. Predict which changes should cancel before adjusting the controls. This places detected signal and specimen amount in one experiment while keeping their meanings distinct.

## Same concentration, different response

Signals are background-corrected and internal-standard concentration is fixed. Compare neat-solvent external calibration with analyte/standard ratios. Set both response factors equal, then change one to reveal the remaining bias.

[Figure: Interactive analyte and internal-standard responses](https://ml-biomat.com/tutorials/experimental-methods/c03/en/#C03-plot)

For quantitative work, calibration levels should span the intended range, retain repeated observations and support inspection of residuals. Independently prepared quality-control samples test the back-calculated results. Low-concentration variation, blank contributions and high-concentration saturation affect fitting differently; weighting should follow the observed variance structure. Mass-axis calibration places peaks correctly, whereas concentration calibration translates area or area ratio into amount. One does not replace the other. If the specimen was diluted or extracted, connect the final concentration back to the relevant original volume or material mass.

The constructed calibration uses six concentration levels with three responses at each level. It allows random variation around a simple relationship to remain visible instead of showing only an ideal line. A specimen assigned a true concentration of 8 ng/mL is treated as an unknown and recovered through the fitted ratio relationship. This tests numerical consistency within the example. In a real study, an independent reference preparation and representative matrices would extend that check to specimen handling and chemical response.

## A complete example preserves the questions behind the result

The program reads the bundled reference record, extracts its twenty-three original peaks and converts original intensity to percentage of the largest original intensity. The measured peak list and the plotting normalization remain separately inspectable. The constructed LC-MS branch begins with two ions at different masses and retention positions, adds a fixed-seed background, and stores the complete two-dimensional array. Narrow and wide extraction windows are then applied to the same data. Exported arrays and tables allow the window to change, the apex to be checked or the processing to be replaced with another dataset.

The quantitation branch includes repeated calibration ratios and an unknown with a defined underlying concentration. It separates random calibration variation from the distinct problem of matrix-dependent response. When reading the code, first identify each axis and unit, then find normalization and summation. Normalizing a mass spectrum to its base peak is useful for comparing fragmentation patterns. Using those normalized heights to calculate absolute concentration across specimens would discard the original response magnitude. A useful processing choice follows the scientific question it is meant to answer.

Replicates also need an explicit meaning. Injecting the same vial three times measures repeatability after preparation, including introduction and instrumental variation. Preparing three independent extracts from one material includes more of the handling process. Testing independently produced materials addresses variation between specimens. These observations can all be useful, but their spread answers different questions. A narrow spread between repeat injections does not measure the variation between production batches. Preserve the specimen relationships in the data table so that the plotted error bars correspond to the intended level of comparison.

Run order provides another practical diagnostic. If every untreated specimen is measured first and every treated specimen last, a gradual change in source response can follow the same pattern as the proposed treatment effect. Interleaving groups where appropriate, including periodic quality-control injections and placing blanks after challenging samples helps distinguish drift and carryover from specimen chemistry. A signal remaining in the blank after a concentrated specimen suggests that part of the preceding material persists in the introduction or chromatographic system. Following that observation with a wash or dilution experiment is a concrete way to improve the method. The purpose is to make the comparison track the experimental treatment rather than the order of measurement.

### Complete spectra, LC-MS map and internal-standard quantitation

Reads the bundled CC BY caffeine reference record and generates labeled teaching models, actual plots, scan arrays and calculated results.

```
"""Mass spectrometry: charge, real MS/MS, LC-MS extraction and quantitation.
Run: python main.py --output results --language en
Requires numpy and matplotlib. Reads the bundled CC BY MassBank record offline.
Other signals are explicitly constructed teaching data, seed 630.
"""
from pathlib import Path
import argparse,json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle,Polygon,FancyArrowPatch
P=argparse.ArgumentParser();P.add_argument('--output',type=Path,required=True);P.add_argument('--language',choices=['zh','en'],default='en');a=P.parse_args();O=a.output;O.mkdir(parents=True,exist_ok=True);L=a.language
def t(z,e):return z if L=='zh' else e
plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fcfbf7','axes.facecolor':'#fcfbf7','svg.fonttype':'none','text.color':'#25364a','axes.titleweight':'bold'})
B='#167d9a';R='#d35f47';G='#37967d';Y='#c49b35';D='#25364a'
def save(f,n):f.savefig(O/f'{n}-{L}.svg',bbox_inches='tight');f.savefig(O/f'{n}-{L}.png',bbox_inches='tight',dpi=145);plt.close(f)
def g(x,m,s):return np.exp(-.5*((x-m)/s)**2)
def csv(n,h,x):np.savetxt(O/n,x,delimiter=',',header=','.join(h),comments='',fmt='%.10g')
h=1.0072764665789;u=1.66053906892e-27;e=1.602176634e-19
neutral=8*12+10*1.00782503223+4*14.00307400443+2*15.99491461957;target=neutral+h
fig,axs=plt.subplots(1,3,figsize=(14.4,4.6),layout='constrained')
ax=axs[0];ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off');ax.set_title(t('A  电喷雾：从液滴到离子','A  Electrospray: droplets to ions'))
ax.add_patch(Rectangle((.2,3.2),2,1.2,facecolor='#d3e2e6',edgecolor=B));ax.add_patch(Polygon([[2.2,3.2],[3,3.8],[2.2,4.4]],facecolor='#d3e2e6',edgecolor=B))
for x,y,r in [(3.5,3.8,.48),(4.8,4.3,.32),(5.6,3.4,.23),(6.7,4,.15)]:ax.add_patch(Circle((x,y),r,fc='#bad8df',ec=B));ax.text(x,y,'+',ha='center',va='center',color=B)
for y in [3.4,4,4.6]:ax.text(8,y,'M⁺',fontsize=12,color=R)
ax.annotate('',(9.5,3.9),(7.4,3.9),arrowprops={'arrowstyle':'->','color':R});ax.text(.5,6.4,t('电压 + 溶液\n蒸发与带电液滴演化','Voltage + solution\nEvaporation and charged droplets'),fontsize=10);ax.text(.5,1,t('1989：Fenn 等报告完整生物分子多电荷谱','1989: Fenn et al., multiply charged biomolecules'),fontsize=9,wrap=True)
ax=axs[1];ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off');ax.set_title(t('B  激光解吸：基质帮助能量传递','B  Laser desorption: a supporting matrix'))
ax.add_patch(Rectangle((1,1.4),8,.4,fc='#8f9aab'));ax.add_patch(Polygon([[2,1.8],[3,2.5],[4,1.8],[5,2.7],[6,1.8],[7,2.4],[8,1.8]],fc='#e4c775',ec=Y));ax.annotate('',(4.8,2.6),(2,6.5),arrowprops={'arrowstyle':'->','lw':3,'color':R})
for x,y in [(5.5,3.7),(6.4,4.9),(7.4,5.8)]:ax.text(x,y,'M⁺',color=B)
ax.text(1,7,t('脉冲激光','Pulsed laser'),color=R);ax.text(1,.2,t('基质 + 待测分子；示意不按尺度','Matrix + analyte; schematic dimensions'),fontsize=9);ax.text(1,.95,t('1987：Tanaka 团队的软激光解吸','1987: Tanaka team, soft laser desorption'),fontsize=9)
ax=axs[2];mass=np.array([100,400,1600]);tof=1*np.sqrt(mass*u/(2*e*5000))*1e6;ax.plot(mass,tof,'o-',color=G);ax.set(xlabel=t('单电荷离子质量 / Da','Singly charged ion mass / Da'),ylabel=t('理想飞行时间 / μs','Ideal flight time / μs'),title=t('C  飞行时间：质量越大越慢','C  Flight time: larger mass, slower ion'));ax.text(.04,.83,'L=1 m; U=5 kV; z=1',transform=ax.transAxes,fontsize=10)
save(fig,'ionization')

fig,axs=plt.subplots(1,3,figsize=(14.4,4.8),layout='constrained');charge=np.arange(6,13);mz=12000/charge+h;intens=g(charge,9,1.6)
ax=axs[0];ax.vlines(mz,0,intens,color=B,lw=3)
for x,z,y in zip(mz,charge,intens):ax.text(x,y+.04,f'{z}+',ha='center',fontsize=9)
ax.set(xlabel='m/z',ylabel=t('构造相对强度','Constructed relative intensity'),title=t('A  一个 12,000 Da 分子的电荷系列','A  Charge series of one 12,000 Da molecule'),ylim=(0,1.25))
ax=axs[1];k=np.arange(5);pr=np.array([math.comb(50,int(i))*.0107**i*(1-.0107)**(50-i) for i in k]);pr/=pr.max()
for z,col in [(1,B),(2,R),(3,G)]:ax.vlines(k*1.00335483507/z,z-1,z-1+.65*pr,color=col,lw=3,label=f'z={z}')
ax.set(xlabel=t('相对首峰的 m/z 间隔','m/z displacement from first isotope'),ylabel=t('为比较而上下错开','Vertically offset for comparison'),title=t('B  同位素间距随电荷压缩','B  Charge compresses isotope spacing'),yticks=[]);ax.legend(frameon=False)
ax=axs[2];x=np.linspace(195.02,195.17,3000)
for j,(res,col) in enumerate([(5000,Y),(50000,B)]):
 sig=target/res/2.354820045;yy=g(x,target,sig)+.7*g(x,target+.01435,sig);ax.plot(x,yy+j*1.8,color=col,label=f'R={res:,}')
ax.set(xlabel='m/z',ylabel=t('构造信号，垂直错开','Constructed signal, offset'),title=t('C  分辨本领决定能否分开近邻','C  Resolving nearby ions'));ax.ticklabel_format(useOffset=False,axis='x');ax.legend(frameon=False,fontsize=9)
save(fig,'charge-resolution')

record=(Path(__file__).parent/'data/MSBNK-BAFG-CSL2311094663.txt').read_text(encoding='utf8');peaktext=record.split('PK$PEAK: m/z int. rel.int.')[1].split('//')[0];peaks=np.array([[float(x) for x in ln.split()] for ln in peaktext.splitlines() if ln.strip()]);assert len(peaks)==23
relative=100*peaks[:,1]/peaks[:,1].max();base=peaks[np.argmax(peaks[:,1]),0]
fig,axs=plt.subplots(1,2,figsize=(12.8,4.9),gridspec_kw={'width_ratios':[1.55,1]},layout='constrained');ax=axs[0];ax.vlines(peaks[:,0],0,relative,color=B,lw=1.8)
for i in np.argsort(relative)[-5:]:ax.text(peaks[i,0],relative[i]+3,f'{peaks[i,0]:.4f}',ha='center',fontsize=9,rotation=50)
ax.set(xlabel='m/z',ylabel=t('相对最大峰的强度 / %','Intensity relative to base peak / %'),ylim=(0,130),title=t('A  真实咖啡因 MS/MS：40 V','A  Actual caffeine MS/MS: 40 V'));ax.text(.03,.88,'MSBNK-BAFG-CSL2311094663',transform=ax.transAxes,fontsize=8)
ax=axs[1];ax.axis('off');ax.text(.02,.93,t('B  一个记录里的不同质量信息','B  Different mass information in one record'),weight='bold');lines=[t('分子式：C₈H₁₀N₄O₂','Formula: C₈H₁₀N₄O₂'),t('由同位素质量计算中性质量','Neutral mass calculated from isotope masses')+f'\n{neutral:.6f} Da',t('计算 [M+H]⁺','Calculated [M+H]⁺')+f'\nm/z {target:.6f}',t('记录前体设置：195.0877','Record precursor metadata: 195.0877'),t('谱内保留的峰：195.0873','Retained spectral peak: 195.0873'),t('CC BY；Ehlig, Lessmann, Jewell, Wick / BfG','CC BY; Ehlig, Lessmann, Jewell, Wick / BfG')]
for j,txt in enumerate(lines):ax.text(.02,.79-j*.145,txt,fontsize=10,va='top')
save(fig,'reference-spectrum');csv('reference_peaks.csv',['mz','original_intensity','record_relative_0_999','replotted_percent'],np.c_[peaks,relative])

# Constructed LC-MS scan matrix with target and nearby interfering ion.
rng=np.random.default_rng(630);time=np.linspace(0,8,801);masses=np.linspace(target-.04,target+.04,801);sig=target/40000/2.354820045
lc=g(time,4,.22);inter=g(time,4.4,.28);spectra=1000*lc[:,None]*g(masses,target,sig)[None,:]+800*inter[:,None]*g(masses,target+.01435,sig)[None,:]+rng.uniform(0,1,(len(time),len(masses)))
tic=spectra.sum(axis=1);narrow=np.abs(masses-target)<=target*5e-6;wide=np.abs(masses-target)<=target*100e-6;xic=spectra[:,narrow].sum(axis=1);broad=spectra[:,wide].sum(axis=1)
fig=plt.figure(figsize=(12.8,8),layout='constrained');gs=fig.add_gridspec(2,2);ax=fig.add_subplot(gs[:,0]);im=ax.imshow(np.log10(1+spectra),aspect='auto',origin='lower',extent=[masses[0],masses[-1],time[0],time[-1]],cmap='magma');ax.set(xlabel='m/z',ylabel=t('保留时间 / min','Retention time / min'),title=t('A  每个时间都有一张质谱','A  A spectrum at each time'));ax.ticklabel_format(useOffset=False,axis='x');fig.colorbar(im,ax=ax,label='log₁₀ (1 + signal)')
ax=fig.add_subplot(gs[0,1]);ax.plot(time,tic/tic.max(),color=Y,label=t('所示质量窗口总信号','Total in displayed mass window'));ax.plot(time,xic/xic.max(),color=B,label=t('目标 ±5 ppm','Target ±5 ppm'));ax.set(xlim=(3,5.5),xlabel=t('时间 / min','Time / min'),ylabel=t('各曲线除以自身最大值','Each curve / its own maximum'),title=t('B  提取目标的时间轨迹','B  Extract the target time trace'));ax.legend(frameon=False,fontsize=9)
ax=fig.add_subplot(gs[1,1]);ax.plot(time,xic/xic.max(),color=B,label='±5 ppm');ax.plot(time,broad/broad.max(),color=R,label='±100 ppm');ax.set(xlim=(3,5.5),xlabel=t('时间 / min','Time / min'),ylabel=t('各自归一化信号','Individually normalized signal'),title=t('C  宽窗口混入近邻','C  A wide window admits interference'));ax.legend(frameon=False)
save(fig,'lcms-map');csv('extracted_chromatograms.csv',['time_min','displayed_window_total','target_5ppm','target_100ppm'],np.c_[time,tic,xic,broad]);np.savez_compressed(O/'constructed_lcms.npz',time_min=time,mz=masses,signal=spectra)

c=np.repeat([0,1,2,5,10,20],3);ratio=.08*c+.01+rng.normal(0,.008,len(c));slope,intercept=np.polyfit(c,ratio,1);sample_true=8.;supp=.55;IS=500.;response=1000.;analyte=sample_true*response*supp;internal=IS*supp
# This separate ratio calibration uses response ratio = 0.08*c+0.01.
unknown_ratio=.08*sample_true+.01;estimated=(unknown_ratio-intercept)/slope
fig,axs=plt.subplots(2,2,figsize=(12.8,8),layout='constrained');ax=axs[0,0];ax.bar([0,1],[100,55],color=[G,R]);ax.set_xticks([0,1],[t('纯溶剂','Neat solvent'),t('提取后基质','Post-extraction matrix')]);ax.set(ylabel=t('等浓度目标响应 / %','Equal-concentration response / %'),title=t('A  基质因子 0.55','A  Matrix factor 0.55'),ylim=(0,115))
ax=axs[0,1];supps=np.linspace(.3,1,100);ax.plot(supps,sample_true*supps,color=R,label=t('按纯溶剂外标','Neat external calibration'));ax.plot(supps,np.full_like(supps,sample_true),color=B,label=t('同受抑制的内标比值','Matched internal-standard ratio'));ax.set(xlabel=t('共同响应因子','Common response factor'),ylabel=t('估计浓度 / ng/mL','Estimated concentration / ng/mL'),title=t('B  比值抵消共同变化','B  Ratios cancel shared changes'));ax.legend(frameon=False,fontsize=9)
ax=axs[1,0];ax.scatter(c,ratio,color=B,s=18);ax.plot([0,20],[intercept,20*slope+intercept],color=D);ax.set(xlabel=t('目标浓度 / ng/mL','Analyte concentration / ng/mL'),ylabel=t('目标 / 内标面积比','Analyte / internal-standard area'),title=t('C  构造比值校准与重复值','C  Constructed ratio calibration'))
ax=axs[1,1];xx=np.linspace(.3,1,100);ax.plot(xx,sample_true*.55/xx,color=R);ax.axhline(8,color=B,ls='--');ax.axvline(.55,color=Y,ls='--');ax.set(xlabel=t('内标响应因子','Internal-standard response factor'),ylabel=t('估计浓度 / ng/mL','Estimated concentration / ng/mL'),title=t('D  内标与目标不同步时','D  When the standard does not track analyte'))
save(fig,'quantitation');csv('ratio_calibration.csv',['concentration_ng_per_mL','area_ratio'],np.c_[c,ratio])
summary={'neutral_caffeine_Da':neutral,'protonated_caffeine_mz':target,'reference_peak_count':len(peaks),'reference_base_peak_mz':base,'reference_precursor_metadata_ppm':(195.0877-target)/target*1e6,'reference_retained_peak_ppm':(195.0873-target)/target*1e6,'charge_12_mz':12000/12+h,'isotope_spacing_z2':1.00335483507/2,'tof_400Da_5kV_us':float(tof[1]),'resolution_FWHM_R40000':target/40000,'matrix_factor':.55,'neat_external_apparent_ng_per_mL':8*.55,'matched_internal_standard_ng_per_mL':8.,'ratio_calibration_slope':float(slope),'ratio_calibration_unknown_ng_per_mL':float(estimated),'target_XIC_apex_min':float(time[np.argmax(xic)])}
assert abs(target-195.087652)<1e-6 and base==138.0657
assert abs(estimated-8)<.3 and abs(time[np.argmax(xic)]-4)<=.01
(O/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
```

Protein studies may use intact mass, or digest proteins into peptides and examine fragment series for sequence and modifications. Materials studies may target residual monomer, released compounds, oxidation products or polymer end groups. Each application should identify whether the measured population consists of intact molecules, extracted components, digestion products or collision-generated ions, and preserve the relevant preparation and acquisition conditions. A strong result lets another reader follow the chain from specimen to ion, from mass and fragments to identity, and from response calibration to amount. The spectrum then supports both the present conclusion and a more focused next experiment.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/C03.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Fenn et al. (1989): Electrospray ionization for mass spectrometry of large biomolecules](https://pubmed.ncbi.nlm.nih.gov/2675315/)

   Original paper abstract on intact macromolecules and charge-state sequences.
2. [Shimadzu: Koichi Tanaka research history](https://www.shimadzu.com/about/nobel/noblesoul/re_hstry.html)

   1987 soft-desorption reports and subsequent instrument development.
3. [MassBank: MSBNK-BAFG-CSL2311094663](https://github.com/MassBank/MassBank-data/blob/dev/BAFG/MSBNK-BAFG-CSL2311094663.txt)

   Caffeine reference, 23 peaks, acquisition conditions and original license.

   CC BY as specified in the record; authors and copyright retained; replotted intensities normalized to base peak.
4. [MassBank record format 2.6](https://github.com/MassBank/MassBank-documentation/blob/dev/MassBankRecordFormat.md)

   Record fields, product peaks versus precursor metadata and per-record licenses.
5. [Waters: Mass accuracy and resolution](https://www.waters.com/nextgen/us/en/education/primers/the-mass-spectrometry-primer/mass-accuracy-and-resolution.html)

   Peak width versus center error, calibration and interference.
6. [Waters: Solvents and caveats for LC-MS](https://www.waters.com/nextgen/us/en/education/primers/the-mass-spectrometry-primer/solvents-and-caveats-for-lcms.html)

   Ionization compatibility, matrix response and post-extraction spiking.
7. [Waters: Quantitation and calibration](https://www.waters.com/nextgen/us/en/education/primers/the-mass-spectrometry-primer/quantitation-and-calibration.html)

   Internal standards, isotope labeling and mass-axis calibration.
8. [NIST: Atomic weights and isotopic compositions](https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl)

   Selected C, H, N and O isotope masses and the carbon isotope mass difference.
9. [NIST: CODATA recommended constants 2022](https://physics.nist.gov/cuu/pdf/wall_2022.pdf)

   Proton mass, elementary charge and atomic mass unit.
