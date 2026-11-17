# Release experiments: How drugs and proteins leave their carriers

Source: https://ml-biomat.com/tutorials/experimental-methods/e04/en/
Language: en

Reconstruct cumulative release from molecular routes, calibration and sampling balances, separating material, medium and apparatus effects.

## The same molecular cargo can follow different timetables

A tea bag gradually colors the surrounding water. A hydrogel containing a protein can undergo a similar transfer without any visible color change. In either case we can ask how much has entered the surroundings, how much remains inside, and how quickly the next portion will emerge. A release experiment turns these questions into a time course. For a local delivery material, the useful result concerns whether molecules become available during the intended period. For an antimicrobial coating, the balance between early availability and sustained delivery may matter. These purposes determine which parts of the curve deserve attention.

A carrier is the material storing the target molecules: a microsphere, film, gel or porous scaffold. The receiving medium is the surrounding liquid that accepts released molecules. A typical experiment begins with a measured loading, determines concentrations at several times and reconstructs the amount transferred. Concentration is the amount per volume, whereas mass describes the amount in the entire liquid. Sweetness offers a useful analogy: a sweeter cup does not necessarily contain more sugar than a less sweet but much larger cup. We need both concentration and volume, and this distinction becomes essential whenever liquid is sampled or replaced.

Dissolution, release and permeation emphasize different steps. Dissolution converts solid drug into dissolved molecules. Release concerns departure from a carrier. Permeation concerns passage through a barrier to its other side. One experiment can contain all three. If loaded particles are placed inside a dialysis bag, molecules detected outside have both left the particles and crossed the membrane. Drawing that route reveals which additional controls are needed. We begin with direct immersion of a carrier, then examine how membranes, protein stability and changing material structure alter the meaning of the measured time course.

![Original diagrams connect direct immersion, sampling/replacement and the Higuchi moving depletion front. The 1961 historical concept explains the spatial process behind square-root time behavior; geometry is schematic.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/333835b459231947214bacb0.svg?v=333835b45923)

Figure 1Original diagrams connect direct immersion, sampling/replacement and the Higuchi moving depletion front. The 1961 historical concept explains the spatial process behind square-root time behavior; geometry is schematic.

Before choosing the assay, define what counts as released material. Chromatography may quantify the intact peak of a stable small molecule. A protein color assay may measure the amount capable of reacting with its reagent, while fluorescence follows labeled species. A cleaved protein fragment can remain fluorescent even after the intact protein and its activity have changed. Released amount, molecular integrity and biological function therefore correspond to distinct measurements. A target such as cumulative intact protein or cumulative fluorescent material makes the intended quantity explicit and helps explain why two detection methods can produce different curves.

## Which parts of the journey shape the curve?

Molecules inside a carrier undergo continual thermal motion. In the absence of bulk flow, a region containing more molecules sends more of them toward a region containing fewer, producing net diffusion. A gel resembles a city with passages and places to pause: passage size affects movement, while affinity for the network affects residence time. That pause can correspond to electrostatic attraction, hydrophobic interactions or reversible binding. Two proteins of similar molecular size can consequently have different release rates. Molecular weight offers a structural clue, but shape, surface chemistry and medium composition help explain how molecules actually travel through the network.

After reaching the material surface, a molecule must cross the nearby liquid layer before joining the well-mixed bath. Stirring mainly changes this external transport path; it does not remove every internal resistance. Faster release with stronger mixing suggests that the surrounding liquid participates in control. If excessive mixing breaks a fragile gel, however, the change also includes altered surface area and structure. Choosing mixing conditions requires attention to both specimen integrity and bath uniformity. Vessel geometry, liquid height, specimen position and mixing mode therefore belong alongside rotational speed when comparing formulations or repeating an experiment.

In 1961, Higuchi connected drug dissolution and outward diffusion in ointments containing suspended solid drug. Material near the surface becomes depleted first, while solid drug deeper inside continues replenishing the dissolved fraction. The depletion boundary progressively moves inward. As the transport distance grows, the amount emerging per unit time decreases; under the corresponding assumptions, cumulative release is proportional to the square root of time. The illustrated moving front captures this historical idea. It shows how a recognizable curve shape can arise from a spatial process, with a particular geometry, loading state and external boundary condition.

$$
Q(t)=k_H\sqrt{t}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/152cda6bbc8d048536474158.svg) | Cumulative released mass per exposed area, μg/cm². |
| ![Formula](https://ml-biomat.com/static/agent-math/3a60ad9059bb079f3031bcf0.svg) | Higuchi coefficient for fixed geometry and conditions, μg cm^{-2} h^{-1/2}. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time from the model's relevant starting point, h. |

Use over a stage meeting the relevant diffusion assumptions, such as approximately planar geometry, negligible swelling, internal solid-drug supply and low external concentration. With coefficient 10 μg cm⁻² h⁻¹ᐟ², Q is 10 μg/cm² at 1 h and 20 μg/cm² at 4 h: quadrupling time doubles cumulative amount.

The square-root relationship describes an appropriate diffusion-controlled stage. Substantial swelling, evolving mesh size, strong drug binding or rising external concentration changes the governing process. Later work solved diffusion equations with suitable boundary conditions to investigate cases such as initial drug concentrations close to solubility in the base. When selecting a model, ask whether solid drug remains, whether geometry is stable and whether the surroundings continually accept molecules. These questions make the equation physically interpretable. A square-root fit applied to every increasing curve can conceal different processes behind visually similar lines.

An early rapid portion is often called burst release. Surface-associated loading, cracks introduced during drying and unbound soluble material can all contribute. Its apparent size also depends on the experimental starting point: excluding a preliminary wash may omit the fastest stage entirely. Useful comparisons include analysis of wash liquid, changes in specimen size, surface loading and more frequent early sampling. An application needing early availability may use this component, whereas sustained delivery may require reducing it. The intended timing gives the burst its practical meaning; its presence alone does not determine whether the design is successful.

## Match the receiving medium and assay to the question

Bath volume has two roles. It converts concentration into amount, and it determines how much target material the surroundings can accept. For a solubility-limited compound, an increasingly saturated bath reduces the driving force for further dissolution or transfer. Slow release may then partly reflect external capacity rather than internal transport. Sink conditions describe an environment with sufficient accepting capacity. Measure solubility in the actual temperature, pH and medium, then compare anticipated release with that capacity. Protein partitioning and binding may require additional checks that the bath concentration remains sufficiently low for the intended boundary condition.

Different purposes justify different boundaries. A relatively large, adequately mixed bath helps investigate internal material transport by reducing external restrictions. A study of a small local fluid compartment may deliberately use finite volume and include that volume in its model. Medium replacement removes released molecules but can also remove degradation products and restore buffering capacity. Replacement frequency is consequently an experimental variable. Surfactants can increase the apparent solubility of hydrophobic compounds while also changing material structure, protein conformation or assay response. Medium selection therefore connects solubility, stability, material behavior and analytical compatibility rather than simply maximizing the final release percentage.

Actual loading must be measured. Suppose preparation begins with 100 μg of drug and the final carrier contains 80 μg. Encapsulation efficiency is 80%, because its denominator is the amount originally supplied. If total dry formulation mass is 1000 μg, loading content on that total-mass basis is 8%. One quantity describes preparation retention; the other describes cargo per amount of formulation. Release percentage normally uses the cargo actually present at the start of the experiment. Substituting the preparation feed combines manufacturing losses with release behavior and makes a low plateau harder to interpret.

$$
\mathrm{EE}=\frac{M_0}{M_{\rm feed}},\qquad \mathrm{LC}=\frac{M_0}{m_{\rm formulation}},\qquad F_n=\frac{M_n}{M_0}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e74566520b2ff9dc2654ee32.svg) | Encapsulation efficiency, dimensionless; multiply by 100 for percent. |
| ![Formula](https://ml-biomat.com/static/agent-math/fe3f0356dce96af85bcb9aa5.svg) | Loading content defined here using total dry formulation mass, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/d39d4c6ec0676acff39eb9eb.svg) | Cumulative release fraction at sample n relative to measured initial loading, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/d0d1f9424f5849a25d3f4fc5.svg) | Target mass actually loaded at the start of release, μg. |
| ![Formula](https://ml-biomat.com/static/agent-math/a287a1335b8b0aa8e20296d1.svg) | Target mass supplied during preparation, μg. |
| ![Formula](https://ml-biomat.com/static/agent-math/907e414ff4732c512fcc64d7.svg) | Dry mass of the entire formulation including cargo, μg. |
| ![Formula](https://ml-biomat.com/static/agent-math/4f3c9d3ab8208b50c9e81e73.svg) | Cumulative target mass released at sample n, μg. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Sample index, dimensionless. |

The ratios describe preparation retention, formulation composition and release progress. A feed of 100 μg, measured loading of 80 μg and formulation mass of 1000 μg give EE=80% and LC=8%. In the separate release example with 100 μg initial loading, 60 μg cumulative release gives Fn=60%.

Loading can be measured by extracting the carrier directly or by subtracting material recovered in preparation and washing liquids. Direct extraction requires a recovery experiment: add a known amount and establish how much the complete procedure retrieves. Indirect calculation requires checking adsorption to vessels, filters and tubing. Medium exposed to an unloaded carrier reveals background absorption, fluorescence or color chemistry from the material. A known target concentration carried through the same storage and filtration checks handling losses. For proteins, freeze–thaw cycles, prolonged incubation and surface adsorption can alter recovery even when the instrument itself performs consistently.

Sampling times should follow the expected process. If the first hour changes rapidly, collect more observations there; later slow changes permit wider spacing. Repeated samples from one carrier form one trajectory, and its time points belong to the same experimental unit. Comparing formulations requires independent carriers or independently prepared batches, with each trajectory retained before calculating time-point summaries. Eight observations along one trajectory are not eight independent specimens. Maintaining specimen and batch identifiers separates the continuity of a release process from variation introduced by material preparation and sample handling.

## Previously collected samples remain part of cumulative release

An instrument first supplies a signal, which calibration converts into concentration. Standards should resemble the samples in medium and handling because buffer components, salts and material leachates can affect background or response. Within a linear range, slope describes signal change per concentration unit and intercept describes the zero-concentration background. Subtracting the intercept and dividing by slope is analogous to correcting a ruler with an offset zero. Any prior dilution must then be reversed. With absorbance 0.090, intercept 0.030 and slope 0.012 mL/μg, measured concentration is 5 μg/mL. A twofold prior dilution makes the original sample concentration 10 μg/mL.

$$
C=d\frac{A-b}{a}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | Concentration in the original sample, μg/mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | Dilution factor between sampling and analysis, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Measured absorbance of the analytical solution, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Intercept of the matrix-matched calibration, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Calibration slope, mL/μg. |

Within the linear calibration range, subtract background, divide by sensitivity and restore dilution. A=0.090, b=0.030, a=0.012 mL/μg and d=2 give 5 μg/mL in the measured liquid and C=10 μg/mL in the original sample.

Consider a bath maintained at 10 mL. Each sample removes 2 mL and is replaced by fresh medium. At the first observation, 20 μg has been released, giving 2 μg/mL, and sampling removes 4 μg. By the second observation, cumulative release reaches 40 μg, but only 36 μg remains in the bath because the earlier 4 μg is already in a collection tube. Concentration is now 3.6 μg/mL and the second sample removes another 7.2 μg. At cumulative release of 60 μg, the current bath contains 48.8 μg. Adding the previously collected 11.2 μg restores the complete 60 μg ledger.

$$
M_n=VC_n+\sum_{i=1}^{n-1}v_iC_i
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4f3c9d3ab8208b50c9e81e73.svg) | Cumulative released mass immediately before sample n, μg. |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | Total receiving volume maintained after replacement, mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/dd358f69abfbebbae37cb3dc.svg) | Mixed-bath concentration before sample n, μg/mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/03fe412bc6d88c2f14c43e45.svg) | Volume removed in earlier sample i, mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/971aeb8f6c70c0afe2138963.svg) | Bath concentration at earlier sample i, μg/mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Current sample index, dimensionless positive integer. |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Earlier sample index; the sum includes 1 through n−1 only. |

Assume target-free replacement, a mixed bath and preservation of the measured molecular form during collection. For a 10 mL bath, earlier 2 mL samples and concentrations 2, 3.6 and 4.88 μg/mL, M3=10×4.88+2×2+2×3.6=60 μg.

The summation includes samples collected before the current observation. Immediately before the current sample is removed, it is already part of the entire bath amount; adding it again would count it twice. Equal aliquots permit one fixed sampling volume, while unequal aliquots require their individual volumes. Without replacement, the current bath volume decreases and the first term must use that actual volume. With complete replacement, add the amount in each collected interval. Continuous-flow experiments instead integrate outlet concentration multiplied by flow over time. These forms share one bookkeeping rule: each portion of target material enters the total exactly once.

![Constructed data with a fixed random seed: calibration, cumulative sampling correction, mass ledger and aliquot-volume sensitivity. Correction adds current bath mass to previously removed mass; the gray line is the known signal-generating process.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/efeab2db8bde3c4847603cde.svg?v=efeab2db8bde)

Figure 2Constructed data with a fixed random seed: calibration, cumulative sampling correction, mass ledger and aliquot-volume sensitivity. Correction adds current bath mass to previously removed mass; the gray line is the known signal-generating process.

This correction explains why bath concentration can decrease while a carrier continues releasing. Late in the experiment, little new cargo may emerge, while sampling and replacement keep diluting the bath. In the figure, changing aliquot volume changes the uncorrected curve even though the underlying constructed release is identical. Concentration, mass currently present in the bath and cumulative released mass are therefore three separate quantities. Naming the relevant quantity on the axis makes the experiment much easier to interpret than applying the same generic label to all three.

Cumulative calculation also propagates errors through time. An early concentration measured too high contributes an excessive removed amount to every subsequent cumulative point. A calibration-slope error affects the whole trajectory. Individual error bars consequently do not establish independence between time points. Retaining raw signals, dilution factors, sampling volumes and independent specimen trajectories allows these effects to be reconsidered. Values slightly above 100% should prompt examination of loading, calibration, volume and recovery. Automatically clipping them to 100% removes evidence that could identify a systematic mismatch between the measured numerator and its denominator.

The timing of mixing matters within each sampling event. The concentration used to represent a whole bath must come from a sufficiently uniform liquid, with the sampling location specified and the carrier handled consistently. Replacement medium should have the intended composition and temperature; otherwise sampling repeatedly changes the experimental environment. Small evaporative losses can become relevant during a long experiment, especially in small vessels. Recording actual volumes or checking evaporation with matched blanks preserves the connection between concentration and amount. These details are particularly useful when two nominally identical trajectories begin to diverge only late in the measurement.

## Does a larger sample reduce cumulative release?

True cumulative release is fixed at 20, 40 and 60 μg. Each sample is replaced with the same volume of target-free medium. Compare the current bath with corrected cumulative release.

[Figure: Mass in the current bath and previous samples](https://ml-biomat.com/tutorials/experimental-methods/e04/en/#E04-plot)

## Read the rate, plateau and residuals together

Choose a comparison quantity that matches the intended use. An early delivery requirement can be assessed using absolute mass at a specified time. Sustained availability can be examined through interval rates across the desired window. Remaining reserve can be measured by extracting the carrier at the endpoint. Reaching half of a formulation's own final release earlier does not necessarily mean delivering more absolute material at the same time, because actual loading can differ. Showing the application question, absolute amounts and normalized curves together makes the comparison more informative than ranking formulations by one characteristic time alone.

A cumulative curve tells us how much has emerged by a time, while a release rate tells us how quickly it emerges over an interval. The simplest average rate divides the difference between adjacent cumulative amounts by elapsed time. If release rises from 20 to 40 μg between one and two hours, the interval-average rate is 20 μg/h. Long sampling intervals average away short rapid events. Very short intervals make small measurement errors more prominent after subtraction. Rate plots therefore belong beside cumulative curves, sampling times and information about measurement precision.

$$
\overline{r}_n=\frac{M_n-M_{n-1}}{t_n-t_{n-1}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4ab9018ce0331a4605783315.svg) | Average release rate between adjacent observations, μg/h. |
| ![Formula](https://ml-biomat.com/static/agent-math/99086759c8e6738285d27c72.svg) | Current and previous cumulative released masses, μg. |
| ![Formula](https://ml-biomat.com/static/agent-math/93d9aabfdc04713b7cefd665.svg) | Current and previous sampling times, h. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Current sampling index, n≥2. |

The difference in cumulative amounts is material released during the interval. Amounts of 20 μg at 1 h and 40 μg at 2 h give (40−20)/(2−1)=20 μg/h, an interval average.

A plateau needs a material balance to explain it. Accessible cargo may be exhausted, remaining molecules may bind strongly, the bath may approach saturation, the target may degrade, or concentrations may fall outside the assay's quantitative range. At the endpoint, extract residual carrier cargo and account for collected samples and vessel rinses. This separates released material, retained material and material lost or transformed during handling. Deliberately changing bath volume, mixing or pH after an apparent plateau can also test whether external capacity, binding equilibrium or a transport path controls the remaining fraction.

Fit a model to answer a particular question, such as comparing characteristic times at fixed geometry and medium or testing an early diffusion description. Then plot residuals: observed values minus model predictions. The constructed example combines a small rapid component with a larger slow component, but fits one exponential timescale. Its fitted line can follow the overall increase while early residuals show a directional pattern. That pattern identifies information omitted by the model. Small irregular deviations and extended deviations on one side of zero have different meanings; the latter can guide investigation of model structure or changing experimental conditions.

![Constructed diagnostics: a single-timescale fit to a two-timescale release process leaves early residual structure. The right panel fixes the carrier timescale at 4 h and varies the sequential membrane timescale to show apparatus effects on the external curve.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/b23ec972d40336dfdb9e1228.svg?v=b23ec972d403)

Figure 3Constructed diagnostics: a single-timescale fit to a two-timescale release process leaves early residual structure. The right panel fixes the carrier timescale at 4 h and varies the sequential membrane timescale to show apparatus effects on the external curve.

Dialysis requires particular attention to two sequential transport processes. Cargo first leaves the carrier into the bag and then crosses the membrane into the outside bath. If membrane transport is slow, the external curve mainly reflects that additional step and differences between carriers may be compressed. Place an equivalent amount of free target material in the same device to measure passage time, and check membrane adsorption and total recovery. The illustrated two-stage model fixes the carrier timescale and changes only membrane transport. The resulting curve differences directly connect an apparatus control to a measurable diagnostic.

Model parameters also depend on which normalization was chosen. A fractional curve based on measured initial loading retains incomplete recovery as part of the result. A curve divided by its measured final amount describes the timing of the recoverable fraction. A curve divided by a fitted asymptote additionally depends on the fitted model. All three can finish near 100% after plotting, despite answering different questions. Keep absolute amounts and the chosen reference alongside fitted parameters so that an apparent change in timescale is not actually a change in denominator or in the fraction being observed.

## Connect material change to independent release evidence

Swelling, network connectivity and degradation alter the routes available to cargo. Swelling can increase space for movement while also increasing the distance from the interior to the surface. Degradation can loosen a network while changing specimen shape and exposed area. These contributions do not necessarily act in the same direction. Faster or slower release alone therefore does not uniquely identify a mesh size. Measuring thickness, water uptake, molecular motion and structural integrity over the same period provides a more informative explanation of how the available transport routes evolve.

Sheth and colleagues in 2019 measured protein diffusion and gel thickness during degradation, then used those independent measurements to predict bulk release. The useful experimental logic is that the model inputs were measured separately before comparison with release observations. The reproduced figure retains observed points and model curves for two proteins. It lets the reader inspect where differences emerge rather than reducing the comparison to a single agreement label. The study also examined time-varying and averaged parameters, illustrating how changes in geometry and mobility can partly compensate when determining a bulk release profile.

![Actual published Figure 5 reproduced in full from Sheth et al. (2019), Frontiers in Bioengineering and Biotechnology 7:410, DOI 10.3389/fbioe.2019.00410, CC BY 4.0. Original BSA and IgG observations and model lines are retained; the source reports n=9 and one-standard-deviation errors. Only an external title and credit are added.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/a98aacfa3da1442d2922eef9.svg?v=a98aacfa3da1)

Figure 4Actual published Figure 5 reproduced in full from Sheth et al. (2019), Frontiers in Bioengineering and Biotechnology 7:410, DOI 10.3389/fbioe.2019.00410, CC BY 4.0. Original BSA and IgG observations and model lines are retained; the source reports n=9 and one-standard-deviation errors. Only an external title and credit are added.

There is a further distinction between measurement scales. Local tracer motion and net transport through an entire material under a concentration gradient need not provide identical diffusion information. Labeling, binding, heterogeneity and molecular interactions can affect their relationship. Released proteins can additionally be examined for size distribution, retained binding capacity or the relevant biological response. These measurements turn a general statement about delivery into several connected questions: has the molecule left the carrier, is its structure preserved, and does the needed function remain? Each question points to a suitable observation and an interpretable comparison.

When reading a published figure, begin with the measured quantity, the normalization and the definition of the error bars. A mean with a standard deviation summarizes a particular set of observations, whose independence still depends on how specimens and batches were prepared. Different assays can emphasize different molecular populations. Compare study conditions before transferring a fitted parameter between materials. The transferable lesson from an experiment is often its measurement logic: independently characterize an evolving transport path, predict its consequence, and identify the next measurement that can explain the remaining discrepancy.

## Reconstruct a release trajectory from raw absorbance

Filtration is another step that can be tested separately. Compare signals before and after passing known target concentrations through the filter, and run blank medium to identify filter-derived background. Repeating this comparison across concentration can reveal proportionally greater adsorption losses in dilute samples. If the collected liquid contains cargo-bearing particles, filtration also changes the measured population: filtrate may represent dissolved material, while unseparated liquid includes particle-associated cargo or scattering. Select the separation step according to the intended quantity and maintain that definition throughout calibration, recovery experiments and interpretation of the final curve.

Finally, inspect whether the earliest recorded time captures the process of interest. Moving a specimen into the bath, mixing it and obtaining the first aliquot all require time. A very rapid surface-associated fraction may be largely transferred before the first measurement, so the first data point contains an unresolved early interval. Recording the transfer and sampling times makes this interval explicit. An additional set of short-time observations can resolve it, while a separately measured wash fraction can establish how much material was removed before the main experiment began. These observations clarify the origin of an apparent initial jump.

The complete example starts with a known constructed release process, simulates sampling and replacement, creates a calibration curve, adds small measurement noise and reconstructs concentration and cumulative amount from absorbance. It exports current bath mass, previously removed mass and the corrected total as separate columns. Each column corresponds to an entry in the earlier ledger. The four-panel output shows calibration, corrected and uncorrected trajectories, mass composition and aliquot-volume sensitivity. A second diagnostic figure shows residuals from a single-timescale fit and the effect of a dialysis step. The published image and its license notice are bundled for offline use.

### Complete Python: From absorbance to cumulative release and model diagnostics

The code exports raw signals, calibration data, mass balances, residuals and four figures. Sampling correction is checked against independent mass conservation.

```
"""Serial-sampling release accounting and constructed transport diagnostics."""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyArrowPatch,Circle

def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def sampled_concentration(cumulative,bath=10.,aliquot=2.):
    removed=0.;concentrations=[]
    for released in cumulative:
        c=(released-removed)/bath;concentrations.append(c);removed+=aliquot*c
    return np.asarray(concentrations)

def correct(concentration,bath=10.,aliquot=2.):
    c=np.asarray(concentration);return bath*c+aliquot*np.r_[0,np.cumsum(c[:-1])]

def main(output,language):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    from matplotlib import font_manager
    fonts={f.name for f in font_manager.fontManager.ttflist};font=next((f for f in ['Microsoft YaHei','Noto Sans CJK SC','SimHei'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[font,'DejaVu Sans'] if language=='zh' else ['DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','axes.prop_cycle':plt.cycler(color=['#186e83','#cd803f','#8160a1','#3c8a6a'])})
    tr=lambda z,e:z if language=='zh' else _label(e)
    def save(fig,n):fig.savefig(output/f'{n}-{language}.svg',bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(1,3,figsize=(12,4.5))
    for a in ax:a.set(xlim=(0,10),ylim=(0,10));a.axis('off')
    for i,a in enumerate(ax[:2]):
        a.add_patch(Rectangle((1,2),8,6,facecolor='#c9e3e9',edgecolor='#186e83',lw=2));a.add_patch(Rectangle((3.3,3),3.4,1.7,facecolor='#8160a1',alpha=.65));a.text(5,3.8,tr('载体','Carrier'),ha='center',va='center',color='white');a.add_patch(FancyArrowPatch((5,5),(5,7),arrowstyle='->',mutation_scale=16,color='#186e83'));a.text(5,1,tr('混匀的接收液','Mixed receiving medium'),ha='center',fontsize=10)
    ax[0].set_title(tr('A  载体中储存的分子','A  Molecules stored in a carrier'));ax[1].set_title(tr('B  取出样液，补入新液','B  Sample out, fresh medium in'))
    for x,direction,label,color in [(2.5,1,tr('取样','Sample'),'#cd803f'),(7.5,-1,tr('补液','Replace'),'#3c8a6a')]:ax[1].add_patch(FancyArrowPatch((x,7 if direction==1 else 9),(x,9 if direction==1 else 7),arrowstyle='->',mutation_scale=15,color=color));ax[1].text(x,9.3,label,ha='center',fontsize=9)
    ax[2].add_patch(Rectangle((1,2),8,6,facecolor='#e6dcc7'));ax[2].add_patch(Rectangle((1,6),8,2,facecolor='#c9e3e9'))
    for x,y in [(2,3),(4,3.4),(7,2.8),(3,4.8),(6,4.7),(8,4)]:ax[2].add_patch(Circle((x,y),.2,color='#8160a1'))
    ax[2].plot([1,9],[5.8,5.8],'--',color='#cd803f');ax[2].text(5,7,tr('已耗尽区域','Depleted region'),ha='center',fontsize=10);ax[2].text(5,1,tr('1961：Higuchi 的移动前沿思想','1961: Higuchi’s moving-front idea'),ha='center',fontsize=9);ax[2].set_title(tr('C  固体药物逐步溶出','C  Solid drug dissolves progressively'));fig.tight_layout();save(fig,'apparatus')
    rng=np.random.default_rng(404);time=np.array([.25,.5,1,2,4,8,12,24]);truth=100*(.2*(-np.expm1(-time/.25))+.8*(-np.expm1(-time/8)));raw=sampled_concentration(truth)
    standards=np.linspace(0,10,7);abs_std=.03+.012*standards+rng.normal(0,.0004,len(standards));slope,intercept=np.polyfit(standards,abs_std,1)
    absorbance=.03+.012*raw+rng.normal(0,.0007,len(raw));estimated=(absorbance-intercept)/slope;corrected=correct(estimated);naive=10*estimated;observed_removed=2*np.r_[0,np.cumsum(estimated[:-1])]
    np.savetxt(output/'release.csv',np.column_stack([time,truth,raw,absorbance,estimated,naive,observed_removed,corrected]),delimiter=',',header='time_h,true_cumulative_ug,true_bath_ug_ml,absorbance,estimated_ug_ml,bath_mass_ug,previously_removed_ug,corrected_cumulative_ug',comments='')
    np.savetxt(output/'calibration.csv',np.column_stack([standards,abs_std]),delimiter=',',header='concentration_ug_ml,absorbance',comments='')
    fig,ax=plt.subplots(2,2,figsize=(11.4,7.3));ax=ax.ravel();ax[0].scatter(standards,abs_std);ax[0].plot(standards,slope*standards+intercept);ax[0].set(xlabel=tr('浓度 / μg mL⁻¹','Concentration / μg mL⁻¹'),ylabel=tr('吸光度','Absorbance'),title=tr('A  同介质标准曲线','A  Matrix-matched calibration'))
    ax[1].plot(time,truth,color='#a4abad',ls='--',label=tr('构造真值','Constructed truth'));ax[1].plot(time,corrected,'o-',label=tr('累计取样校正','Sampling corrected'));ax[1].plot(time,naive,'s-',label=tr('只算当前溶液','Current bath only'));ax[1].set(xlabel=tr('时间 / h','Time / h'),ylabel=tr('药物质量 / μg','Drug mass / μg'),title=tr('B  校正把已取走的量加回来','B  Correction restores removed mass'));ax[1].legend(fontsize=8)
    x=np.arange(len(time));ax[2].bar(x,naive,label=tr('当前溶液','Current bath'));ax[2].bar(x,observed_removed,bottom=naive,label=tr('此前取样','Earlier samples'));ax[2].set(xticks=x,xticklabels=[f'{t:g}' for t in time],xlabel=tr('时间 / h','Time / h'),ylabel=tr('累计质量 / μg','Cumulative mass / μg'),title=tr('C  每个时间点的质量账本','C  Mass ledger at each time'));ax[2].legend(fontsize=8)
    for v in [0,1,2,4]:ax[3].plot(time,10*sampled_concentration(truth,aliquot=v),label=f'{v:g} mL')
    ax[3].set(xlabel=tr('时间 / h','Time / h'),ylabel=tr('未校正的当前质量 / μg','Uncorrected current mass / μg'),title=tr('D  同一释放过程，不同取样体积','D  Same release, different aliquots'));ax[3].legend(title=tr('每次取样','Sample volume'),fontsize=8);fig.tight_layout();save(fig,'sampling')
    tt=np.linspace(0,24,241);single=lambda t,tau:100*(-np.expm1(-t/tau));tau=float(curve_fit(single,time,corrected,p0=[5],bounds=(.01,100))[0][0]);pred=single(time,tau)
    fig,ax=plt.subplots(1,3,figsize=(12,4.2));ax[0].plot(time,corrected,'o',label=tr('构造数据','Constructed data'));ax[0].plot(tt,single(tt,tau),label=tr('单时间尺度拟合','Single-timescale fit'));ax[0].set(xlabel=tr('时间 / h','Time / h'),ylabel=tr('累计释放 / %','Cumulative release / %'),title=tr('A  拟合曲线','A  Fitted curve'));ax[0].legend(fontsize=8)
    ax[1].axhline(0,color='#a4abad');ax[1].plot(time,corrected-pred,'o-');ax[1].set(xlabel=tr('时间 / h','Time / h'),ylabel=tr('数据−拟合 / 百分点','Data − fit / percentage points'),title=tr('B  残差保留了早期快过程','B  Residuals reveal the early fast process'))
    for tau_m in [.5,2,8]:
        tau_c=4.;fraction=1-(tau_c*np.exp(-tt/tau_c)-tau_m*np.exp(-tt/tau_m))/(tau_c-tau_m);ax[2].plot(tt,100*fraction,label=f'{tau_m:g} h')
    ax[2].plot(tt,100*(-np.expm1(-tt/4)),color='#a4abad',ls='--',label=tr('载体自身','Carrier alone'));ax[2].set(xlabel=tr('时间 / h','Time / h'),ylabel=tr('外液累积量 / %','Cumulative outer-bath amount / %'),title=tr('C  透析膜增加第二道传质过程','C  Dialysis adds a transport step'));ax[2].legend(title=tr('膜过程时间尺度','Membrane timescale'),fontsize=8);fig.tight_layout();save(fig,'diagnostics')
    from PIL import Image
    fig,ax=plt.subplots(figsize=(11,4.6));ax.imshow(Image.open(Path(__file__).with_name('sheth2019-figure5.webp')));ax.axis('off');ax.set_title(tr('真实研究：独立测得扩散与厚度，再预测释放','Published study: measured diffusion and thickness predict release'),fontsize=12,pad=12);fig.text(.5,.015,'Sheth et al. (2019), Figure 5 · Frontiers in Bioengineering and Biotechnology · CC BY 4.0',ha='center',fontsize=8.5);save(fig,'published')
    worked=sampled_concentration([20,40,60]);wcorrect=correct(worked);summary={'worked_example':{'concentrations_ug_ml':worked.tolist(),'third_bath_mass_ug':float(10*worked[-1]),'third_removed_ug':float(2*sum(worked[:-1])),'third_corrected_ug':float(wcorrect[-1]),'release_percent':60,'loading_efficiency_percent':80,'loading_content_percent':8,'calibration_concentration_ug_ml':(.09-.03)/.012,'diluted_original_ug_ml':10},'calibration':{'slope':float(slope),'intercept':float(intercept)},'fit':{'single_tau_h':tau,'residual_rmse':float(np.sqrt(np.mean((corrected-pred)**2)))},'mass_balance':{'max_exact_error_ug':float(np.max(np.abs(correct(raw)-truth)))},'final':{'true_ug':float(truth[-1]),'corrected_ug':float(corrected[-1]),'naive_ug':float(naive[-1])}}
    assert abs(wcorrect[-1]-60)<1e-12;assert abs(10*worked[-1]-48.8)<1e-12;assert summary['mass_balance']['max_exact_error_ug']<1e-10
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

First check conservation without measurement noise: correction should recover the constructed cumulative amount. Next change aliquot volume and examine the uncorrected trajectory. Then change calibration background and observe how the reconstructed values shift. This sequence separates accounting errors from instrumental errors. With real measurements, retain the same column structure while replacing the constructed signals, and preserve specimen and preparation-batch identifiers. To compare fitted parameters, fit independent trajectories before combining estimates according to the experimental design. This keeps variation between materials distinct from repeated readings of one sample.

A useful release result states how much target material becomes available, over what period, in which environment and with what integrity or function. Cumulative amount, interval rate, residual loading, recovery and independent replication each support part of that statement. The next chapter resolves the spatial process further into concentration difference, material thickness, interfacial partitioning and flux per area. Those quantities help turn a release curve into a transport experiment and guide the choice of an additional measurement that can discriminate among plausible mechanisms.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/E04.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Higuchi (1961). Rate of release of medicaments from ointment bases containing drugs in suspension](https://doi.org/10.1002/jps.2600501018)

   Historical paper connecting a moving depletion front with square-root time behavior.
2. [Koizumi et al. (1975). Rate of Release of Medicaments from Ointment Bases Containing Drugs in Suspension](https://www.jstage.jst.go.jp/article/cpb1958/23/12/23_12_3288/_article)

   Effects of initial concentration, solubility and boundary conditions on the Higuchi approximation.
3. [FDA. Compilation of Guidance and Resources for in vitro Dissolution Testing](https://www.fda.gov/animal-veterinary/new-animal-drug-applications/compilation-fda-guidance-and-resources-in-vitro-dissolution-testing-immediate-release-solid-oral-dosage)

   Measurement principles for sampling, replacement, medium, stability, filtration and analytical validation.

   Official technical reference; no assets reproduced.
4. [Sheth et al. (2019). Predicting Drug Release From Degradable Hydrogels Using Fluorescence Correlation Spectroscopy and Mathematical Modeling](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2019.00410/full)

   Independent diffusion and thickness measurements connected to protein release, including Figure 5.

   CC BY 4.0; Figure 5 reproduced with attribution.
5. [SciPy documentation: curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

   Nonlinear least squares, parameter bounds and residual definitions.
