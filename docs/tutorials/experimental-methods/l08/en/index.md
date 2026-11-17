# qPCR: Understanding gene expression through amplification curves

Source: https://ml-biomat.com/tutorials/experimental-methods/l08/en/
Language: en

Connect copying, fluorescence crossings, efficiency, references and low-copy sampling.

## Why a cell's answer appears as a rising fluorescence curve

Cells cultured on soft and stiff materials can acquire different shapes. A researcher may then ask whether genes involved in adhesion, inflammation or tissue formation have changed their expression. Begin by giving expression a measurable object: RNA molecules corresponding to a selected gene. RNA serves as a working copy of genetic information, and the abundance of particular copies reflects aspects of the cell's current activity. Comparing those abundances asks a more specific question than whether the cells look different. RT-qPCR converts RNA into DNA suitable for amplification, then uses the fluorescence recorded during amplification to estimate an initial target quantity.

The basic intuition resembles watching two portions of dough rise at the same proportional rate. The portion that starts larger reaches a shared height sooner. In qPCR, the shared height is a fluorescence threshold and the waiting time is measured in amplification cycles. The crossing position is called Cq; instruments also use names such as Ct. It can be fractional because the intersection is calculated between recorded cycles. An earlier crossing generally indicates more starting target, but that crossing also depends on the growth factor, threshold and baseline. Understanding those dependencies gives the later subtractions and powers a physical meaning.

RT and real-time are easily confused. In RT-qPCR, RT means reverse transcription, the conversion of RNA into complementary DNA. Real-time describes monitoring fluorescence while amplification proceeds. A DNA target can enter qPCR directly; an RNA study adds extraction, RNA integrity and reverse-transcription yield to the measurement chain. Equal Cq values therefore need not mean equal RNA copies per cell. Cell number, total RNA per cell, extraction recovery and the fraction added to a reaction all affect the target quantity that finally reaches a well.

This chapter follows a materials-related question: how much does target RNA change relative to an experimentally stable reference? We first explain copying, then turn curves into quantities, and finally examine references, replication and low-copy sampling. Executed code retains every cycle of a constructed dataset and every independent sample's result. A licensed published figure shows amplification and melting information from an actual reaction. Together, these let a reported fold change be traced back to its measured curve and denominator.

## From copying DNA to watching the copies accumulate

The two DNA strands can act as templates for one another through complementary base pairing. PCR repeats three operations: heat separates the strands, cooling permits short DNA primers to bind at corresponding positions, and polymerase extends those primers along the templates. Two primers define opposite ends of the target region, which becomes increasingly abundant over successive cycles. Think of them as two directional bookmarks that specify where copying begins. The temperature program and reagent composition determine whether those bookmarks bind appropriately and whether extension proceeds efficiently; their numerical settings are established for the target and reaction chemistry.

In 1985, Saiki and colleagues reported enzymatic amplification of specific beta-globin sequences and combined it with sequence analysis associated with sickle-cell anemia. Amplification made a small amount of selected DNA accessible to subsequent identification. In 1992, Higuchi and colleagues monitored amplification in closed tubes through fluorescence associated with double-stranded DNA. Copying and observing now occupied the same timeline. This history explains the quantitative opportunity: two reactions can finish with abundant product while having different starting quantities. Continuous observation preserves their different times of emergence.

![Original copying schematic connects 1985 specific amplification and 1992 closed-tube fluorescence; short colored segments denote primers and green denotes extension.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/f450e1ac609d48408b0fa435.svg?v=f450e1ac609d)

Figure 1Original copying schematic connects 1985 specific amplification and 1992 closed-tube fluorescence; short colored segments denote primers and green denotes extension.

Ideally, one amplifiable template becomes two after each cycle, but a reaction does not necessarily achieve complete doubling. Here efficiency eta means the newly produced fraction per cycle:100% efficiency means eta equals 1, giving a multiplication factor of 2. Some sources instead use E for the multiplication factor itself and report 1.9 where another source reports 90%. Check the definition before using the number. Adding 1 to a factor that already includes the original template would change the mathematical meaning of the experiment.

$$
N_n=N_0(1+\eta)^n=N_0f^n
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/194f19b40ecc87035bc06fa5.svg) | Target amount after cycle n, same unit as N0 |
| ![Formula](https://ml-biomat.com/static/agent-math/358eaab52fd29057e6b95399.svg) | Initial target quantity in the exponential model, copies or relative signal units |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Cycle count, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | Fraction newly added per cycle, dimensionless; 1 means 100% efficiency |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | Per-cycle multiplication factor 1+eta, dimensionless |

Assume the same proportional increase during each cycle of the analyzed interval. Starting with 100 units, ten cycles with a multiplication factor of 2 give 102400 units. A factor of 1.9 adds 90% of the existing amount per cycle, corresponding to an efficiency of 0.9. Apply this relationship within the exponential region.

Exponential growth occupies one part of the amplification curve. Initially, product-dependent fluorescence is hidden by baseline and noise. A region of approximately constant multiplication becomes measurable, followed by a transition toward a plateau as reaction conditions and detection response change. Quantification uses a region with measurable signal and an appropriate growth relationship. To make the constructed example transparent, its exponential curves are capped at a high signal rather than fitted to a biochemical plateau model. Real transitions are usually smoother. The cap illustrates why endpoint brightness can lose initial differences; calculations use crossings well before it.

## What specimen does the small reaction volume represent?

A comparison of cells on two materials starts by defining sampling. Equal material areas, equal initial cell numbers and equal culture durations describe different aspects of an experiment and may yield different cell numbers at collection. If equal total RNA masses enter reverse transcription, the comparison concerns target abundance within those RNA inputs. A per-cell quantity additionally requires cell information and appropriate external calibration. Materials can adsorb nucleic acids or contribute substances that affect enzymes. Extraction blanks and controls following the actual sample path help investigate those recovery and interference processes.

RNA can degrade during preparation and storage. A continuous molecule then becomes fragments, and whether the amplified region survives depends on fragment location. Total RNA concentration alone does not establish that a selected target region remains intact and amplifiable. Use integrity measurements suited to the specimen, keep sampling-to-preservation conditions consistent, and retain the RNA input to reverse transcription. Splitting the same RNA into separate reverse-transcription reactions can reveal variation introduced by that step, which would be invisible if only the final PCR were repeated.

Reverse transcriptase produces complementary DNA, or cDNA, from RNA. Priming can target a particular sequence or a broader population of RNAs, and these strategies need not recover every transcript equally. Taking and diluting a portion of the cDNA determines the material entering PCR. A DNA standard curve examines amplification but bypasses extraction and reverse transcription. For absolute RNA copies in the original specimen, connect an appropriate RNA reference material and recovery information to the volume chain. The number in a reaction well acquires a per-cell meaning only after those relationships have been established.

Two common blanks examine different stages. A no-template control replaces the sample template with the appropriate blank and helps detect contamination or products formed between primers. A no-reverse-transcription control uses the sample without reverse transcriptase and reveals whether residual DNA can also be amplified. They act like observation points at separate junctions: a signal at each one points toward a different cause. A positive control demonstrates that the assay can detect the target. Together with input quantity and inhibition assessment, these controls guide the next experiment when a sample shows little amplification.

## Read the curve before converting cycles into quantity

The instrument records a fluorescence value each cycle. Raw fluorescence contains amplification-dependent signal plus baseline contributions from reagents, consumables and optics. Baseline correction asks what the well would read without increasing product; its purpose is not simply to make a curve look smooth. Over-subtraction reduces early net signals, while under-subtraction leaves an extra offset. Both can bend a growth region that should appear approximately straight on a logarithmic axis. Our constructed dataset has an explicitly known baseline of 10000 units so this contribution can be removed directly. Actual experiments require a documented method appropriate to their observed curves.

A threshold is a common horizontal line placed in the useful quantitative region. Its intersection with each curve defines Cq. Raising the threshold generally delays crossing, but the delay depends on growth rate. Combining Cq values obtained under different threshold settings therefore loses the common scale. The equation below connects crossing, multiplication and threshold quantity: divide the quantity reached at the threshold by the multiplication accumulated over those cycles to recover the starting quantity. This is repeated reversal of growth, rather than a special statistical trick.

$$
C_q=\frac{\ln(N_q/N_0)}{\ln f},\qquad N_0=N_qf^{-C_q}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/612fc124ab16c82e17432359.svg) | Fractional cycle at the quantification threshold, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/99f414f1f400292a1cc8fff5.svg) | Net target-signal quantity at threshold, same unit as N0 |
| ![Formula](https://ml-biomat.com/static/agent-math/358eaab52fd29057e6b95399.svg) | Initial quantity inferred from the exponential model, relative signal units |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | Multiplication per cycle, greater than 1, dimensionless |

At the threshold, the initial quantity multiplied by the per-cycle factor raised to Cq equals the threshold quantity. Taking logarithms isolates Cq; the threshold-to-initial quantity ratio is dimensionless. With a threshold of 1000000 units, an initial quantity of 100 units and a multiplication factor of 2, Cq is about 13.288. Starting with 400 units gives 11.288, two cycles earlier. Converting relative quantities to copy numbers requires suitable standards and a consistent definition of the template.

A quantity expressed in fluorescence units is relative to a detection system. Known standards connect that scale to copy number. Different amplicons can have different lengths, dye binding or probe responses, so fluorescence-unit ratios between genes do not automatically equal molecular copy ratios. Expression studies can first compare each assay with its own common calibrator, then combine those relative changes. Fixed assay-specific response factors cancel in the relevant ratios. Explaining what cancels and what remains gives normalization a more precise meaning than the instruction to divide everything by a reference.

![Simulated raw/log curves, calibration and residuals. Three technical wells per level; the high-signal cap is an explicit teaching convention.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/5324d678a966bd8a253dac34.svg?v=5324d678a966)

Figure 2Simulated raw/log curves, calibration and residuals. Three technical wells per level; the high-signal cap is an explicit teaching convention.

A standard curve provides another entry point. Prepare known initial quantities, measure their Cq values using the same assay, and put the decimal logarithm of initial quantity on the horizontal axis. Each tenfold dilution delays crossing by a certain number of cycles. With perfect doubling the delay is about 3.322 cycles, since ten is not an integer power of two. The negative regression slope therefore determines the multiplication factor. Replicate concentrations and residuals expose structure associated with low-quantity sampling, pipetting or inhibition at high input.

$$
C_q=a+s\log_{10}(N_0/N_*),\quad f=10^{-1/s},\quad \eta=f-1
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/612fc124ab16c82e17432359.svg) | Quantification-cycle position, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Calibration intercept, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | Cq change per tenfold initial quantity, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/358eaab52fd29057e6b95399.svg) | Known initial standard quantity, relative units or copies |
| ![Formula](https://ml-biomat.com/static/agent-math/a1357c231e808ab781f04f48.svg) | Fixed reference amount in the same units as N0; 1 unit here |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | Per-cycle multiplication factor, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | Newly added fraction per cycle, dimensionless |

Taking base-ten logarithms gives a calibration slope of −1/log₁₀(f). A multiplication factor of 2 gives a slope of approximately −3.322; a factor of 1.9 gives approximately −3.587. Inserting the latter slope into the inverse relation recovers 1.9. Standards and unknowns use the established working range and correctly recorded input quantities.

The constructed standards contain 10,100,1000 and 10000 initial signal units, each with three technical wells. Their true per-cycle factor is 1.9. The program interpolates crossings logarithmically between adjacent noisy measurements and fits a slope near the theoretical value of minus 3.587. These are signal units, explicitly distinguished from measured molecular copies. A systematic error in preparing a dilution can produce an orderly regression with an incorrect efficiency. Agreement with a straight line examines one relationship; accurate standards and independently checked dilution examine additional parts of the calibration.

Uncertainty also has more than one layer. A confidence interval for a fitted slope describes how precisely the calibration determines that slope. Predicting an unknown quantity additionally includes the dispersion of a new measurement, so its prediction interval is wider. An unknown near the edge of the calibrated range relies more heavily on the established response model than one surrounded by well-characterized standards. Preserve replicate observations and the calibrated range instead of reporting only a fitted line. The example's residual panel makes this distinction visible before more elaborate interval calculations are introduced.

## Why subtract twice, and why is the base not always two?

Consider a control with target Cq 25 and reference Cq 20. Treatment gives target 23 while reference remains 20. The target crosses two cycles earlier, with an unchanged reference. If both assays double per cycle and conditions match, target abundance relative to reference increases fourfold. The first subtraction links each target to its own sample reference; the second compares treatment with control. The negative sign reverses the direction because a larger starting quantity gives a smaller cycle number. The familiar calculation follows directly from those relationships.

$$
\Delta C_{q,i}=C_{q,t,i}-C_{q,r,i},\quad \Delta\Delta C_q=\Delta C_{q,T}-\Delta C_{q,C},\quad F=2^{-\Delta\Delta C_q}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/abc03db846fac332025557a4.svg) | Within-sample target-minus-reference cycle difference, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Sample index, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/9e784fcda0647d6b9c48e034.svg) | Target and reference Cq for sample i, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/bfecbeb29196c3f7ea9907ed.svg) | Treatment and control condition labels |
| ![Formula](https://ml-biomat.com/static/agent-math/718ed6d7a0bf7ddb894c75d1.svg) | Treatment-minus-control normalized cycle difference, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | Condition fold change of target relative to reference, dimensionless |

This simplification applies when both assays approximately double their target each cycle, thresholds remain consistent within each assay, and the reference is suitable for the comparison. A control difference of 25 − 20 = 5 and a treatment difference of 23 − 20 = 3 give a difference of −2, corresponding to a fourfold change. Measured efficiency-corrected quantities provide the more general calculation.

The base 2 comes from doubling. Suppose the target assay instead multiplies by 1.8 and the reference by 1.9. If treatment advances target crossing by two cycles and reference crossing by one, the corrected relative change is 1.8 squared divided by 1.9, about 1.705. Assuming 2 throughout gives 2. The disagreement reflects a different growth assumption. Actual analysis should use established assay efficiencies to convert reactions into quantities before reference normalization and comparison. The 2025 MIQE update similarly treats Cq as an intermediate value and emphasizes efficiency-corrected quantities with their quantitative ranges.

$$
F=\frac{f_t^{C_{q,t,C}-C_{q,t,T}}}{f_r^{C_{q,r,C}-C_{q,r,T}}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | Fold change of target relative to reference, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/4fe32bcaed367c9f18c66248.svg) | Target and reference assay multiplication factors, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/a3eeab9ca584e4a0d4cab9ea.svg) | Target Cq in control and treatment, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/5e237c6d8d9032b8f025d1d4.svg) | Reference Cq in control and treatment, dimensionless |

When each assay retains its efficiency and threshold across conditions, convert its cycle difference into a quantity ratio, then divide the target ratio by the reference ratio. A two-cycle target advance with a factor of 1.8 and a one-cycle reference advance with a factor of 1.9 give 1.8²/1.9 = 3.24/1.9, or approximately 1.705. If efficiencies vary between samples, first infer quantities using the appropriate model for each reaction.

A reference gene supplies the denominator. Familiar names do not establish stability under every treatment: stiffness, nutrition, differentiation and stress can affect common reference genes. If the target truly increases fourfold but the selected reference doubles, the normalized result is twofold. The arithmetic answers the target's change relative to that moving reference. Evaluate candidates from different regulatory pathways across the study conditions. Multiple references are commonly combined through a geometric mean on a quantity scale, which matches multiplicative changes and allows fixed gene-specific scaling factors to cancel in comparisons.

For example, relative reference quantities of 0.5 and 2 have a product of 1 and a geometric mean of 1. Reciprocal fold changes cancel on this multiplicative scale. Their arithmetic mean is 1.25, describing an additive average instead. Cancellation itself does not establish biological stability: two treatment-responsive references can still produce an orderly combined value. Reference selection remains an experimental question. In tissue or mixed culture, altered proportions of cell types can also change RNA composition. Interpret the normalized quantity together with specimen composition before attributing the entire change to regulation inside an individual cell.

## Interactive experiment: Same input difference, different growth rates

Blue starts at 100 units and multiplies by 1.9 per cycle. Orange input follows the true ratio. Change orange efficiency and the common threshold to inspect Cq differences. Ideal exponential signals use cycle on the horizontal axis and logarithmic signal vertically.

[Figure: Two exponential growth curves and threshold](https://ml-biomat.com/tutorials/experimental-methods/l08/en/#L08-lab)

The interactive experiment temporarily isolates two target reactions to examine input, efficiency and threshold. The blue reaction has a fixed multiplication factor of 1.9; the orange factor is adjustable. Their actual starting ratio remains visible. Powers of 2 produce a changing estimate when the orange efficiency changes, while inversion using each known factor recovers the selected input ratio. Moving the threshold further changes the timing difference between reactions growing at different rates. A Cq difference becomes a complete quantitative observation when its threshold and efficiency remain attached.

## What became fluorescent, and what entered an unlit well?

A dye that binds double-stranded DNA can respond to the intended product and to unwanted products. Melting analysis gradually heats the amplified reaction while observing the fluorescence loss as strands separate. Plotting the negative rate of fluorescence change with temperature turns the steepest decline into a peak. Its position depends on sequence, length, solution composition and heating conditions. Comparison with an identity-checked positive control can reveal new low-temperature peaks or mixed products. Primer design and, where appropriate, sequence checking connect those thermal features to molecular identity.

Different sequences can share similar melting temperatures, and a single longer fragment can melt in separate domains. Peak count therefore needs molecular interpretation. Probe-based assays add another sequence-recognition step and bring their own signal and background checks. The published LinRegPCR figure places raw amplification, baseline correction, efficiency information and melting results from the same reaction together. First identify the region supporting quantity estimation; then examine whether the fluorescent product has the expected behavior. Its tables preserve this connection between measurement quality and numerical output.

![Untergasser et al. (2021), Fig. 1, reproduced in full under CC BY 4.0. A and B analyze measured amplification and melting data from well D8, sample A75_CRE25. C–E show the result tables and corrections.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/a3b6d33b30254bdd9f1fd612.svg?v=a3b6d33b3025)

Figure 3Untergasser et al. (2021), Fig. 1, reproduced in full under CC BY 4.0. A and B analyze measured amplification and melting data from well D8, sample A75_CRE25. C–E show the result tables and corrections.

At low abundance, replicate variation has a simpler additional origin: molecules are discrete. An average of one copy per well does not place exactly one in every well. Some receive none, and others receive two or more. Under uniform independent random allocation, the Poisson model predicts about 36.8% empty wells at a mean of one copy and about 5.0% at a mean of three. Increasing effective sampled volume or replicate number adds information about this allocation. Assigning every non-crossing well an arbitrary last-cycle value instead converts an absent detection into an invented exact quantity.

$$
P(K=0)=e^{-\lambda}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/065cbeda1c8b4a2279014fa8.svg) | Probability of zero target copies in a well, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/24733a44cf365eb5e1b92574.svg) | Actual input copies in a well, nonnegative integer |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | Mean input copies per well, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | Natural exponential base, about 2.718, dimensionless |

For independent random molecular allocation in a uniform sample, Poisson sampling gives 0.3679 empty probability at lambda 1 and 0.04979 at lambda 3. This concerns input allocation, separately from amplification failure.

A detection limit concerns how consistently a specified amount is detected under defined conditions. A quantification limit additionally requires the quantity estimate to satisfy established precision and accuracy criteria. Occasionally detecting a late curve and reliably distinguishing a 1.2-fold change are different experimental tasks. Characterize the low-copy region with suitable replicate numbers and positive controls, preserving non-detection frequencies and decision rules. Additional cycles extend observation, but cannot recover target from a well into which no target molecule entered.

![Simulation diagnostics. In A, each bar represents an independent sample after combining three technical wells. Each target-to-reference ratio is divided by the geometric mean of the three control-sample ratios, giving a control geometric mean of 1 and an arithmetic mean of about 1.003. B shows simulated melting curves; C shows the theoretical probability of an empty well; D compares efficiency effects when the true starting amount is fourfold higher.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/07ff0c6032f686fb3d147c50.svg?v=07ff0c6032f6)

Figure 4Simulation diagnostics. In A, each bar represents an independent sample after combining three technical wells. Each target-to-reference ratio is divided by the geometric mean of the three control-sample ratios, giving a control geometric mean of 1 and an arithmetic mean of about 1.003. B shows simulated melting curves; C shows the theoretical probability of an empty well; D compares efficiency effects when the true starting amount is fourfold higher.

Inhibition and dilution can interact with that sampling problem. Dilution reduces both target and inhibitors. If the inhibitor had substantially slowed amplification, a diluted reaction may cross earlier than the undiluted one despite containing less target. Examine the dilution pattern with curve shape and suitable spike controls rather than interpreting it through target dilution alone. Excessive dilution can eventually move the sample into a region dominated by random molecular allocation. The useful working dilution balances these effects for the actual specimen and assay.

## A complete example that keeps every fold linked to its curve

The complete program generates the calibration series and six independent constructed samples. Each sample has target and reference assays with three technical wells. Input amount varies between samples; treated target-to-reference proportions are around fourfold above controls, with retained sample variation. The program exports per-cycle fluorescence arrays, standard measurements, per-well Cq values and inferred starting quantities. It compares efficiency correction with a direct powers-of-two calculation. Because the constructed starting quantities are known, the analysis can be checked against an independently specified answer.

### Complete Python: Amplification, efficiency, normalization and melting

Offline per-cycle constructed fluorescence, per-well quantities, fitting and diagnostics; the actual publication figure is bundled.

```
"""Offline qPCR teaching experiment; constructed arrays and a licensed measured figure."""
from pathlib import Path
import argparse,csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from PIL import Image
BLUE='#186e83';AMBER='#cd803f';PURPLE='#8160a1';GREEN='#3c8a6a'

def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def cq(n0,factor=1.9,threshold=1e6):return np.log(threshold/n0)/np.log(factor)
def crossing(cycles,signal,threshold):
    j=np.flatnonzero(signal>=threshold)[0]
    return float(cycles[j-1]+(np.log(threshold)-np.log(signal[j-1]))/(np.log(signal[j])-np.log(signal[j-1])))
def main(output,language='zh'):
    out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh';T=lambda a,b:a if zh else _label(b)
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5'})
    def save(fig,n):fig.savefig(out/f'{n}-{language}.svg',bbox_inches='tight');plt.close(fig)
    rng=np.random.default_rng(808);cycles=np.arange(41);threshold=1e6;baseline=10000;standard_n=np.array([10,100,1000,10000]);standard=[];curves=[]
    for n0 in standard_n:
        for rep in range(3):
            # The cap is a drawing convention, not a biochemical plateau fit.
            raw=baseline+np.minimum(n0*1.9**cycles,2e7)+rng.normal(0,500,len(cycles));curves.append(raw)
            standard.append([n0,rep+1,crossing(cycles,raw-baseline,threshold)])
    standard=np.array(standard);slope,intercept=np.polyfit(np.log10(standard[:,0]),standard[:,2],1)
    with(out/'standards.csv').open('w',newline='',encoding='utf8')as f:
        w=csv.writer(f);w.writerow(['initial_target_units','technical_replicate','Cq']);w.writerows(standard)
    rows=[];sample_curves=[];truth=np.array([1,1.1,.9,4,4.4,3.6]);loads=np.array([.85,1,1.2,.9,1.1,1.25])
    for i in range(6):
        for gene,factor,n0 in [('target',1.9,100*loads[i]*truth[i]),('reference',1.95,1000*loads[i])]:
            for rep in range(3):
                raw=baseline+np.minimum(n0*factor**cycles,2e7)+rng.normal(0,500,len(cycles));sample_curves.append(raw);c=crossing(cycles,raw-baseline,threshold)
                rows.append([i+1,'control'if i<3 else'treated',gene,rep+1,factor,c,threshold/factor**c])
    with(out/'samples.csv').open('w',newline='',encoding='utf8')as f:
        w=csv.writer(f);w.writerow(['sample','group','assay','technical_replicate','amplification_factor','Cq','inferred_initial_units']);w.writerows(rows)
    ratios=[];naive=[]
    for i in range(6):
        target=[r for r in rows if r[0]==i+1 and r[2]=='target'];ref=[r for r in rows if r[0]==i+1 and r[2]=='reference']
        # Geometric mean summarizes multiplicative quantities within technical replicates.
        ratios.append(np.exp(np.mean(np.log([r[-1]for r in target]))-np.mean(np.log([r[-1]for r in ref]))))
        naive.append(2**(-np.mean([r[-2]for r in target])+np.mean([r[-2]for r in ref])))
    ratios=np.array(ratios);naive=np.array(naive);normalized=ratios/np.exp(np.mean(np.log(ratios[:3])));naive/=np.exp(np.mean(np.log(naive[:3])))
    np.savez_compressed(out/'amplification.npz',cycles=cycles,standard_raw=np.array(curves),sample_raw=np.array(sample_curves),known_baseline=baseline,threshold=threshold)
    temperature=np.linspace(65,95,301);single=1/(1+np.exp((temperature-82)/.65));mixed=.75*single+.25/(1+np.exp((temperature-73)/.6))
    with(out/'melting.csv').open('w',newline='',encoding='utf8')as f:
        w=csv.writer(f);w.writerow(['temperature_C','single_normalized','mixed_normalized','single_negative_derivative_per_C','mixed_negative_derivative_per_C']);w.writerows(zip(temperature,single,mixed,-np.gradient(single,temperature),-np.gradient(mixed,temperature)))
    fig,ax=plt.subplots(figsize=(11,5));ax.axis('off');ax.set(xlim=(0,12),ylim=(0,6))
    labels=[T('分开双链','Separate strands'),T('引物定位','Primers locate target'),T('酶延伸复制','Polymerase extends')]
    for j,label in enumerate(labels):
        x=1+j*3.6;ax.add_patch(FancyBboxPatch((x,.9),2.7,3.5,boxstyle='round,pad=.1',fc=[BLUE,PURPLE,GREEN][j],alpha=.12));ax.text(x+1.35,3.9,label,ha='center')
        for y in [2,2.7]:ax.plot([x+.3,x+2.4],[y,y],color=BLUE,lw=3)
        if j:ax.plot([x+.3,x+.8],[2.7,2.7],color=AMBER,lw=6);ax.plot([x+1.9,x+2.4],[2,2],color=AMBER,lw=6)
        if j==2:
            ax.plot([x+.8,x+2.4],[2.7,2.7],color=GREEN,lw=3);ax.plot([x+.3,x+1.9],[2,2],color=GREEN,lw=3)
        if j<2:ax.annotate('',xy=(x+3.4,2.6),xytext=(x+2.9,2.6),arrowprops={'arrowstyle':'->','lw':2})
    ax.text(6,5.3,T('1985：特定DNA扩增 → 1992：在封闭反应管中观察荧光','1985: specific DNA amplification →1992: fluorescence in closed reaction tubes'),ha='center',fontsize=12)
    ax.text(6,.2,T('原创机制图；每轮的复制比例决定达到同一亮度要多久。','Original mechanism: per-cycle multiplication controls time to a shared fluorescence threshold.'),ha='center');save(fig,'history')
    fig,ax=plt.subplots(2,2,figsize=(11,8.5))
    for j,n0 in enumerate(standard_n):
        color=[BLUE,AMBER,PURPLE,GREEN][j];raw=curves[3*j]
        ax[0,0].plot(cycles,raw,color=color,label=str(n0));ax[0,1].plot(cycles,np.maximum(raw-baseline,1),color=color)
    ax[0,0].set(xlabel=T('循环数','Cycle'),ylabel=T('原始荧光 / a.u.','Raw fluorescence / a.u.'),title=T('A  构造原始扩增曲线','A  Constructed raw amplification'));ax[0,0].legend(title=T('初始单位','Initial units'),fontsize=8)
    ax[0,1].set_yscale('log');ax[0,1].set_ylim(1e3,3e7);ax[0,1].axhline(threshold,color='gray',ls='--');ax[0,1].set(xlabel=T('循环数','Cycle'),ylabel=T('扣基线荧光 / a.u.','Baseline-corrected fluorescence / a.u.'),title=T('B  对数轴显出指数增长段','B  Log axes reveal exponential growth'))
    x=np.log10(standard[:,0]);ax[1,0].scatter(x,standard[:,2],color=BLUE);ax[1,0].plot([1,4],np.polyval([slope,intercept],[1,4]),color=AMBER);ax[1,0].set(xlabel=T('初始量的log10','log10(initial units)'),ylabel=T('Cq / 循环','Cq / cycle'),title=T('C  三个技术复孔的校准','C  Calibration with3technical replicates'))
    ax[1,1].scatter(x,standard[:,2]-np.polyval([slope,intercept],x),color=PURPLE);ax[1,1].axhline(0,color='gray',lw=1);ax[1,1].set(xlabel=T('初始量的log10','log10(initial units)'),ylabel=T('Cq残差 / 循环','Cq residual / cycle'),title=T('D  检查拟合剩下的结构','D  Examine residual structure'))
    for a in ax.flat:a.grid(alpha=.18)
    fig.tight_layout();save(fig,'amplification')
    fig,ax=plt.subplots(2,2,figsize=(11,8.4));x=np.arange(6)
    ax[0,0].bar(x-.18,normalized,.36,color=BLUE,label=T('各自效率校正','Assay-specific correction'));ax[0,0].bar(x+.18,naive,.36,color=AMBER,label=T('统一假设每轮2倍','Assume2×per cycle'));ax[0,0].set_xticks(x,range(1,7));ax[0,0].set(xlabel=T('样品1–3对照，4–6处理','Samples1–3control;4–6treated'),ylabel=T('归一化倍数','Normalized fold'),title=T('A  保留独立样品的差异','A  Preserve individual-sample differences'));ax[0,0].legend(fontsize=8)
    ax[0,1].plot(temperature,-np.gradient(single,temperature),color=BLUE,label=T('一种构造产物','One constructed product'));ax[0,1].plot(temperature,-np.gradient(mixed,temperature),color=AMBER,label=T('两种构造产物','Two constructed products'));ax[0,1].set(xlabel=T('温度 / °C','Temperature / °C'),ylabel=T('负导数 / °C⁻¹','Negative derivative / °C⁻¹'),title=T('B  熔解曲线提供产物线索','B  Melting informs product interpretation'));ax[0,1].legend(fontsize=8)
    lam=np.linspace(.01,8,200);ax[1,0].plot(lam,np.exp(-lam)*100,color=PURPLE);ax[1,0].scatter([1,3],[100/np.e,100*np.exp(-3)],color=AMBER);ax[1,0].set(xlabel=T('每孔平均进入拷贝数','Mean input copies per well'),ylabel=T('没有拷贝的孔 / %','Wells with zero copies / %'),title=T('C  少量分子如何分配到小体积','C  Low-copy sampling into small volumes'))
    eff=np.linspace(1.6,2,100);cqcontrol=cq(100);cqtreat=cq(400,eff);ax[1,1].plot(eff,2**(cqcontrol-cqtreat),color=AMBER);ax[1,1].axhline(4,color=BLUE,ls='--');ax[1,1].set(xlabel=T('处理样品每轮扩增倍数','Treated-sample multiplication per cycle'),ylabel=T('直接用2的幂得到的倍数','Fold inferred with powers of2'),title=T('D  真实4倍遇到不同扩增效率','D  True4×change with changing efficiency'));ax[1,1].set_ylim(0,10)
    for a in ax.flat:a.grid(alpha=.18)
    fig.tight_layout();save(fig,'diagnostics')
    fig,ax=plt.subplots(figsize=(11,10.7));ax.imshow(Image.open(Path(__file__).resolve().parent/'linreg2021-figure1.jpg').convert('RGB'));ax.axis('off');ax.set_title(T('真实反应D8：把扩增与熔解结果一起读','Measured reactionD8: read amplification and melting together'),fontsize=12);fig.text(.5,.015,T('Untergasser等2021，图1；CC BY4.0。完整转载，外加双语标题。','Untergasser et al.2021,Fig1; CC BY4.0. Full reproduction with an added external title.'),ha='center',fontsize=9);fig.tight_layout(rect=[0,.04,1,1]);save(fig,'published')
    ideal_slope=-1/np.log10(1.9);summary={'growth':{'hundred_after_ten_doublings':100*2**10,'tenfold_delay_at_two':np.log(10)/np.log(2),'fourfold_delay_at_19':float(cq(100)-cq(400))},'calibration':{'ideal_slope':float(ideal_slope),'factor_from_ideal_slope':float(10**(-1/ideal_slope)),'fitted_slope':float(slope),'fitted_factor':float(10**(-1/slope))},'normalization':{'ideal_ddcq_fold':2**(-(23-20-(25-20))),'efficiency_example':1.8**2/1.9,'reference_doubled_fold':4/2,'observed_control_mean':float(normalized[:3].mean()),'observed_treated_mean':float(normalized[3:].mean())},'sampling':{'empty_at_one':float(np.exp(-1)),'empty_at_three':float(np.exp(-3))}}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

Technical wells are combined through geometric means of their inferred quantities before each sample's target-to-reference ratio is calculated. Independent samples retain separate values. All six ratios are then divided by the geometric mean of the three control-sample ratios, placing every bar on a shared fold-change scale. The controls consequently have a geometric mean of 1, while their arithmetic mean can be slightly higher: about 1.003 in this example. This difference follows from calibration on a multiplicative scale, rather than an additional biological change. Six bars represent six samples, rather than treating eighteen technical wells as independent biological replicates. For experimental inference, use the normalized efficiency-corrected quantities or an appropriate transformation in a model that preserves pairing, batches and sampling structure. The magnitude of the group change and the dispersion between biological samples both contribute to its interpretation.

Try doubling the treated reference along with the target and observe the normalized result move from approximately fourfold to twofold. Then keep starting biological quantities fixed while changing target amplification efficiency, comparing the raw curves with the direct Cq calculation. Move the threshold and check whether quantities inferred through a consistent growth model remain stable. Changing one part at a time connects input, curve, inferred amount and final denominator. The calculation becomes something that can be reasoned through, rather than a sequence of symbols to memorize.

A shared calibrator also helps join separate runs. Run a consistent aliquoted sample across plates and express each target quantity relative to the corresponding calibrator measurement before combining appropriate normalized results. Balance groups across plates so treatment and run are not the same classification. Preserve instrument exports, sample identities, primer information, analysis settings and the calibration relationship. Raw curves contain features that a Cq-only spreadsheet cannot reconstruct, making later reanalysis possible when a baseline method or quality criterion changes.

RNA changes describe transcript abundance. Protein abundance also depends on translation and degradation, while cell behavior depends on protein location, activity and environment. Protein detection, microscopy and functional assays can extend the same research question to those levels. A useful result identifies the cells or tissue, sampling point, target, reference, quantity conversion and sample variation. This connects the information in a fluorescence curve to the biological process that motivated the experiment and to the next observation needed to understand it.

Plate position also belongs to experimental design. Putting all controls on one plate and all treatments on another makes treatment and run differences coincide. Balance the groups and include the same aliquoted calibrator on separate runs so their quantitative scales can be linked. The calibrator should remain stable during storage and lie within suitable ranges for target and reference assays. It has a different purpose from a no-template control: one connects quantitative scales, while the other investigates unwanted signal or contamination. Both can be present in the same design without duplicating one another's role.

The averaging rule deserves equal attention. Taking the arithmetic mean of two Cq values from the same assay and then converting to quantity gives the geometric mean of the corresponding quantities. For inferred amounts of 100 and 400, that geometric mean is 200, whereas their arithmetic mean is 250. Each summary has a defined meaning, and the chosen rule should remain consistent throughout the analysis. Independent samples additionally retain their biological dispersion and pairing. Measurements before and after treatment in the same subject have a different sampling structure from measurements in separate subjects. Every spreadsheet row should remain connected to a sample, reaction and raw curve.

Absolute calibration adds another accounting layer. If 2 microliters of a tenfold diluted cDNA preparation enter a reaction, that aliquot represents 0.2 microliters of the undiluted preparation. An inferred 100 copies in the aliquot corresponds to 500 copies per microliter on that preparation's calibrated scale. Extending this to the original RNA requires the reverse-transcription volume, template definition and yield information. A single-stranded cDNA template and a double-stranded DNA standard also enter the earliest copying steps differently, so their calibration relationship should be established explicitly. The simple exponential model defines its starting quantity at a consistent effective starting state; it does not automatically resolve every preceding molecular conversion.

Finally, an apparent efficiency above 100% prompts an investigation into calibration and reaction composition. Incorrect planned dilution values can change the standard-curve slope, and dilution may relieve an inhibitor at the same time that it removes target. Inspect independent dilution preparation, sample matrix, raw curve shape and product identity together. Reporting a very precise slope cannot identify which of these mechanisms produced it. A small follow-up series with controlled additions or matched dilutions can distinguish them and determine which quantitative range is appropriate for the biological samples.

A replicate that disagrees with its neighbors invites inspection of its curve, well identity and dispensing record. Retain the original observation while investigating it. A predetermined exclusion criterion connects any removal to a measured defect, such as an incompatible melting product, rather than to the desired group result.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L08.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Saiki et al. (1985): Enzymatic amplification of beta-globin genomic sequences](https://pubmed.ncbi.nlm.nih.gov/2999980/)

   Early amplification work and its research purpose.

   Abstract and bibliographic reference
2. [Higuchi et al. (1992): Simultaneous amplification and detection of specific DNA sequences](https://pubmed.ncbi.nlm.nih.gov/1368485/)

   Continuous fluorescence observation in closed tubes.

   Abstract and bibliographic reference
3. [Bustin et al. (2010): MIQE precis](https://pmc.ncbi.nlm.nih.gov/articles/PMC2955025/)

   Specimens, reverse transcription, controls and reference selection.
4. [Bustin et al. (2025): MIQE 2.0](https://doi.org/10.1093/clinchem/hvaf043)

   Efficiency-corrected quantities, quantitative ranges, raw data and prediction intervals.
5. [Untergasser et al. (2021): Web-based LinRegPCR](https://link.springer.com/article/10.1186/s12859-021-04306-1)

   Actual amplification/melting analysis, baseline and result tables; Fig. 1.

   CC BY 4.0; Fig. 1 reproduced in full
