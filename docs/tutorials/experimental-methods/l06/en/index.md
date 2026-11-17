# ELISA: Turning molecular recognition into concentration

Source: https://ml-biomat.com/tutorials/experimental-methods/l06/en/
Language: en

Connect recognition, nonlinear calibration, dilution and recovery to a complete concentration measurement.

## What can a drop of culture medium tell us about cellular communication?

Place immune cells on two materials and collect a small amount of medium the next day. The liquids may look identical even when the cells have released different amounts of signaling proteins. Those proteins can recruit other cells or alter nearby tissue behavior. The analytical question concerns one molecular target within a complex mixture. ELISA, the enzyme-linked immunosorbent assay, combines antibody recognition with enzyme reporting: retain the target, generate a measurable product through an enzyme reaction, and compare the resulting signal with standards of known concentration.

Imagine selecting one kind of nut from a box containing many different mechanical parts. A recognition tool selects the object, while a reporting tool makes the number selected easier to measure. A plate reader measures an optical signal rather than counting protein molecules directly. Antibodies determine which molecules participate in detection, while enzyme activity, substrate, reaction time, and reading conditions determine the final color. The calibration curve connects this complete measurement process to concentration. Understanding an ELISA table therefore means following the route from recognition through calibration rather than treating absorbance as a concentration label.

This chapter begins with a common sandwich format and builds a complete concentration calculation. We examine why standard curves bend, why a diluted sample can yield a higher concentration after correction back to the original sample, and why a smooth fitted line still benefits from independent controls. A published figure reveals real differences between reagent lots. Reproducible constructed data provide known starting values for the numerical exercises. Together they connect one colored well, one calibration curve, and one biological interpretation.

Define the final quantity before choosing the sampling procedure. Picograms per milliliter describes concentration in the collected liquid. Multiplying by the liquid volume gives the amount present in that liquid at collection. Comparing secretion per cell additionally requires cell numbers, their changes over time, collection duration, and medium replacement history. These denominators represent different questions. Decide whether the endpoint is accumulated amount per well, concentration, or a cell-normalized quantity so that the experiment preserves the information needed for that endpoint.

## Recognition, washing, and color development perform different jobs

A sandwich assay begins with a capture antibody immobilized on a surface. Target molecules in the sample bind to it, and washing removes material that has not been retained. A detection antibody then recognizes another accessible part of the target. It may carry an enzyme directly or recruit the enzyme through another binding arrangement. Adding substrate allows the enzyme to generate a measurable product repeatedly. Both antibodies must be able to bind the target in the chosen arrangement. A small molecule with few accessible binding features may require a different assay architecture.

A competitive assay follows another logic. Sample target competes with a labeled molecule, or with an immobilized binding partner, for a limited number of recognition opportunities. In a common competitive arrangement, more sample target leaves less reporter bound, producing a decreasing concentration-response curve. Signal direction therefore follows the molecular arrangement. Draw what is immobilized, what carries the reporter, and what remains after washing. That drawing explains whether more target should produce more or less measured signal before a fitting function is selected.

In 1971, Engvall and Perlmann published an immunoglobulin quantification method using the name ELISA. In the same year, van Weemen and Schuurs published immunoassay work with antigen-enzyme conjugates. These developments connected enzyme reporting with immune recognition. The illustration below depicts a modern sandwich arrangement to explain that connection. It is an original mechanism diagram rather than a reconstruction of every detail of either historical experiment. Retaining the recognized material, removing unbound reporter, and controlling the reporting reaction are the steps that turn recognition into a quantitative measurement.

![Original modern sandwich schematic: capture, target, detection and enzyme product, connected to two 1971 enzyme-immunoassay publications.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/61d35d87504bf568cc4f90ac.svg?v=61d35d87504b)

Figure 1Original modern sandwich schematic: capture, target, detection and enzyme product, connected to two 1971 enzyme-immunoassay publications.

Washing removes reporting molecules that have not passed through the intended recognition pathway. Free enzyme or enzyme-bearing antibody left in a well can still produce color, raising the blank signal. Development time determines how long product accumulates. A well receiving substrate several minutes earlier can become darker simply because it has reacted longer. Coordinated addition and stopping sequences help standards and unknowns share the same reaction history. Substrate choice, stopping conditions, and measurement wavelength depend on the particular assay chemistry.

Absorbance describes the reduction in transmitted light relative to a reference. It is a logarithmic ratio and has no mass or length unit. For a fixed optical path and a particular colored product, it can track product concentration. Product concentration, however, depends on the enzyme reaction, which in turn depends on the preceding binding steps. This sequence explains why absorbance need not be a straight-line function of target concentration. Even well-behaved optical detection can accompany a curved overall immunoassay response.

$$
A=-\log_{10}\left(\frac{I}{I_0}\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Absorbance, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/112feff6b4d0334226e24d5c.svg) | Transmitted light intensity, same unit as reference |
| ![Formula](https://ml-biomat.com/static/agent-math/6e4f2807ce72e4cab3957130.svg) | Reference light intensity, same unit as transmitted intensity |

Absorbance expresses transmission on a logarithmic scale. Under matched wavelength and instrument conditions, transmission fractions 0.1 and 0.01 give absorbances 1 and 2. Intensity units cancel. Target concentration is obtained through the complete assay calibration.

## Put standards, samples, and controls on one map before pipetting

Standards contain known target concentrations and establish the relationship between concentration and response. A zero standard still contains the relevant diluent and assay reagents, revealing the baseline response without added target. An independent quality-control sample tests the resulting calibration without participating in its fit. Think of it as a new question answered with an already established rule. Standards prepared with a shared concentration error can still form a very smooth curve. A separately prepared control is more informative about that common error than agreement between those standards alone.

Serial dilution often produces standards separated by a constant concentration factor. Mixing equal volumes of a previous solution and diluent gives a twofold dilution. Mix each tube before taking the next transfer, because incomplete mixing propagates through later standards. Also consider the sample matrix: everything surrounding the target, such as medium components, serum proteins, salts, or material-derived solutes. Matrix components can affect binding, target stability, and reporting. Two solutions with the same target concentration can therefore produce different responses if their matrices interact differently with the assay.

Replicate wells reveal variation introduced by repeated handling and measurement of one sample. Large differences prompt inspection of pipetting, bubbles, washing, position, and reaction timing. Agreement shows that these technical repetitions are close; it does not create independent cultures or independent material specimens. A useful plate map records sample identity, dilution, standard concentration, and replicate relationships. Retaining spatial position makes edge patterns, column effects, and errors associated with an addition step easier to identify.

Collection time is part of sample identity. A concentration may result from fewer cells accumulating protein over a longer interval or more cells accumulating it over a shorter interval. A material may adsorb the target, lowering the amount remaining in solution, while degradation can occur during culture or storage. Distinguish release into the whole experimental system from detectable target remaining in the liquid at collection. A known target added to a cell-free material system and recovered after the same contact period can investigate one contribution to this difference.

For multiple dilution stages, multiply the stage factors. A twofold dilution followed by a fourfold dilution produces an eightfold dilution before the assay. Fixed reagent-mixing steps shared by standards and samples belong to the assay's concentration definition and should not be counted twice. Record sample dilution separately from routine reaction assembly. Keep concentration units consistent throughout the calculation: picograms, nanograms, and micrograms differ by factors of one thousand. Additional decimal places do not repair an unrecognized unit conversion.

## Why the curve bends and how to follow it back to concentration

At low concentration, response approaches the blank and small target-dependent differences compete with baseline variation. In a middle region, concentration changes produce clear signal changes. At high concentration the response approaches an upper plateau. A four-parameter logistic curve, or 4PL, describes this shape with a lower plateau, an upper plateau, a midpoint concentration, and a steepness parameter. It is an empirical calibration model rather than a complete chemical account of antibody and enzyme behavior. Its practical value depends on recovering known concentrations accurately within the intended working region.

The teaching example uses a lower plateau of 0.05, an upper plateau of 2.05, a midpoint of 100 picograms per milliliter, and a shape parameter of 1.2. At the midpoint, response lies halfway between the plateaus, giving 1.05. The concentration ratio in the equation is dimensionless, so changing concentration units requires changing the midpoint units as well. A logarithmic horizontal axis spreads out multiplicative concentration changes; it does not give zero concentration an ordinary logarithmic position. The program retains zero standards in the fit while handling their display separately.

$$
y=a+(d-a)\frac{c^b}{m^b+c^b}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1d9b846cface9f9348e4081a.svg) | Assay absorbance, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/0aa7bfcc5af82046a01fa888.svg) | Lower and upper response plateaus, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | Analyte concentration on the assay scale, pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Concentration at half response range, pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Positive shape parameter, dimensionless |

This increasing four-parameter calibration uses nonnegative concentration, d greater than a, and positive m and b. With a=0.05, d=2.05, m=100 and b=1.2, c=100 gives y=1.05. Matching concentration powers cancel dimensionally. It is an empirical calibration relationship.

For an unknown sample, move from its vertical-axis response to the calibration curve and then to the concentration axis. The inverse function expresses that graphical operation as a repeatable calculation. A response of 1.05 corresponds to 100 picograms per milliliter. If the measured solution was an eightfold dilution, the original sample contained 800 picograms per milliliter under the matched-response assumption. Apply the dilution factor to the inferred concentration. Multiplying absorbance by eight before inversion would assume a straight-line scaling that the curved calibration does not possess.

$$
c=m\left(\frac{y-a}{d-y}\right)^{1/b},\qquad C_0=Dc
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | Inferred diluted-sample concentration, pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Half-response concentration, pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/1d9b846cface9f9348e4081a.svg) | Unknown-sample absorbance, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/0aa7bfcc5af82046a01fa888.svg) | Calibration lower and upper plateaus, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Curve shape parameter, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/8e1f255f71ebe5898eee968b.svg) | Back-corrected original-sample concentration, pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | Cumulative pre-assay sample dilution factor, dimensionless |

Algebraically invert the 4PL, then restore dilution by concentration conservation. The inverse requires a<y<d and an established working region. y=1.05 gives c=100; eightfold dilution gives C0=800. The example fits raw absorbance with baseline in a, without subtracting the blank again.

Each standard has measurement variation. When high responses vary more than low responses, equal weighting can allow high-response observations to dominate the fit. Weighted fitting adjusts their influence using an appropriate error model or sufficiently informative repeated measurements. The example generates data from a stated noise model and uses those known standard deviations as fitting weights. For a real assay, two replicate wells alone provide little information about a complicated variance pattern. Multiple calibration runs and independent controls can help evaluate the chosen weighting and model.

![Simulated calibration data, fitting residuals, inverse-calibration sensitivity and a plate map. Zero-concentration standards enter the fit but are omitted from the logarithmic axis in A. Gray wells in D are unused.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9008f889414bf4fb1d445867.svg?v=9008f889414b)

Figure 2Simulated calibration data, fitting residuals, inverse-calibration sensitivity and a plate map. Zero-concentration standards enter the fit but are omitted from the logarithmic axis in A. Gray wells in D are unused.

Read the calibration figure in stages. Check that standards cover the region containing the samples, then inspect residuals—the observed response minus its fitted value. Residuals consistently positive in one region and negative in another suggest a shape mismatch. An isolated outlier calls for a return to its well position and handling record. The 4PL has a symmetric shape on a log-concentration scale; some assays benefit from a five-parameter curve allowing asymmetry. Additional flexibility should improve independent concentration prediction, rather than merely making a line pass closer to the fitted points.

Blank handling must also remain consistent. This example fits the raw response with a lower plateau instead of subtracting a separately measured blank first. Another workflow may subtract the same blank estimate from standards and samples, then fit the corrected responses. The fitted plateau and inverse equation must correspond to the chosen representation. Subtracting the blank twice, or subtracting it only from unknown samples, shifts the sample relative to the calibration. Preserve both raw and processed columns so that the transformation can be traced without reconstructing it from a final concentration.

## Use dilution and added target to test the sample's response

If twofold, fourfold, and eightfold dilutions return similar original-sample concentrations after inversion and dilution correction, the sample behaves consistently over that dilution range. Dilutional linearity concerns calibrated concentration, not proportionality of raw absorbance. If the corrected estimate rises with dilution, consider an interference that is itself weakened by dilution. First inspect whether the responses occupy a useful calibration region, then combine dilution behavior with a recovery experiment. The largest corrected value is a clue to investigate, not an automatic definition of the true value.

The constructed example fixes the original concentration at 800 picograms per milliliter and introduces a suppression that weakens with dilution. An undiluted sample has sixty percent effective response in concentration terms, while an eightfold dilution reaches ninety-five percent. The calibration model is correct, yet altered sample response produces a low estimate. Without added noise, undiluted, eightfold-diluted, and sixteenfold-diluted samples return original-sample estimates of 480, 760, and 780. The example separates mathematical inversion from the biological assumption that sample target responds like the standard.

## Why does dilution change the inferred concentration of one sample?

The calibration is the chapter's fixed 4PL. Constructed matrix suppression multiplies effective concentration by “1−suppression/dilution”. Invert the signal first, then restore dilution. Add a response offset to explore sensitivity near plateaus.

[Figure: Calibration, effective concentration and inverse concentration after a response offset](https://ml-biomat.com/tutorials/experimental-methods/l06/en/#L06-lab)

A spike-recovery experiment adds a known amount of target and asks how much additional concentration the assay detects. Suppose an unspiked sample contains 40 picograms per milliliter, a spike contributes 25 at the final volume, and the spiked sample measures 62. The measured increase is 22, giving eighty-eight percent recovery. Subtracting the original 40 isolates the newly added target. Prepare an unspiked control with the same volume change, or adjust its concentration to the final volume, so dilution caused by spike addition is not confused with loss of recovery.

$$
\mathrm{Recovery}=100\%\,\frac{C_{\rm spiked}-C_{\rm unspiked}}{C_{\rm added}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/da2911810e849da2f484a127.svg) | Spike recovery, % |
| ![Formula](https://ml-biomat.com/static/agent-math/855aac15c18924e953f833e0.svg) | Measured spiked concentration, pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/b1bbfaaddb07df7e6f4b2bd5.svg) | Unspiked concentration at matched final volume, pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/556105106ab656f403037742.svg) | Added target concentration contribution at final volume, pg/mL |

Subtract the pre-existing amount to isolate recovered addition, then compare with the known spike. 62−40=22, and adding 25 gives 88%. Match final-volume changes and use the same dilution scale for every concentration.

![Simulated matrix suppression weakens as the sample is diluted; the true original concentration is 800 pg/mL. Orange bars show the sample SD of three technical wells. The right panel compares an unspiked sample at 40 pg/mL, the expected spiked value of 65 pg/mL and the measured value of 62 pg/mL.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/b8114f942abef9f9723a8103.svg?v=b8114f942abe)

Figure 3Simulated matrix suppression weakens as the sample is diluted; the true original concentration is 800 pg/mL. Orange bars show the sample SD of three technical wells. The right panel compares an unspiked sample at 40 pg/mL, the expected spiked value of 65 pg/mL and the measured value of 62 pg/mL.

Where the spike is added determines what the experiment tests. Adding it to already prepared culture supernatant mainly investigates assay-stage matrix response. Adding it before material contact or extraction also includes adsorption, processing, and storage losses. Both designs can answer useful questions when their timing is explicit. A purified standard may differ from native target in binding partners, modifications, or fragment state. Combining spike recovery with dilution behavior of natural samples provides complementary evidence about collection, preparation, and detection.

Dilution has a cost as well as a benefit. It can reduce interference while pushing target concentration toward the low-response region. Excessive dilution then makes the response harder to distinguish from baseline variation. In the interactive experiment, hold original concentration fixed and increase dilution to watch the point move along the curve. Add a small absorbance offset and compare its effect near the middle and near a plateau. Selecting a dilution becomes a balance between matrix compatibility and a concentration region supported by standards and controls.

The suppression model is deliberately simple: it changes the effective target concentration by a fraction that depends on dilution. Real interference can also alter the plateau, slope, baseline, or time dependence of the response. Consequently, dilution curves that fail to agree should lead to a specific follow-up experiment. Comparing compatible diluents, testing a material-only matrix, or moving the spike before and after extraction can distinguish several possible causes. A correction factor estimated from one condition should not replace checking whether the response relationship remains consistent across the samples being compared.

## Precision, reagent lots, and measurements that can be compared

An identical absorbance error produces different concentration errors along the curve. Where the curve is steep, a small vertical movement corresponds to a small horizontal displacement. Near a plateau, the same vertical change can span a broad concentration interval. At the teaching model's midpoint, the local slope is 0.006 absorbance per picogram per milliliter. A response change of 0.02 therefore corresponds approximately to 3.33 picograms per milliliter. The figure also uses exact inversion to show the interval produced by the same positive and negative response offsets.

Standard deviation and coefficient of variation describe replicate precision. Standard deviation expresses spread around a mean; dividing it by the mean gives a relative measure that can be compared across concentration scales. For concentrations of 98, 100, and 102, the mean is 100, sample standard deviation is 2, and coefficient of variation is two percent. This describes how closely those results agree. If all three share a preparation bias, they can agree closely while missing the true concentration together.

$$
\overline C=\frac{1}{n}\sum_{i=1}^{n}C_i,\quad s=\sqrt{\frac{\sum_{i=1}^{n}(C_i-\overline C)^2}{n-1}},\quad \mathrm{CV}=100\%\,\frac{s}{\overline C}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cd0d870dfc8efaf0a79af99d.svg) | Mean replicate concentration, pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/971aeb8f6c70c0afe2138963.svg) | Inferred concentration of replicate i, pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Replicate index, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Replicate count, at least 2, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | Sample standard deviation, pg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/dbd8c772d1a9221850e1289c.svg) | Coefficient of variation, % |

Sample SD uses n−1 to estimate replicate dispersion; CV normalizes by a positive mean. For 98, 100 and 102 the mean is 100, squared deviations sum to 8, s=√(8/2)=2, and CV=2%. It describes replicate precision; independent-sample and batch variation are retained separately.

Real between-lot variation can exceed variation among wells. Feng and colleagues compared standard curves from several reagent lots in a 2019 study. Panel A below shows different absorbances at the same labeled concentration, while panel B displays variation within and between lots. Error bars in panel A are standard deviations, and the numbers of curves differ between lots. Follow a horizontal line at a fixed response: its intersections with different curves give different inferred concentrations. A common control carried across batches helps identify this change in the measurement scale.

![Feng et al. (2019), Fig. 2, reproduced in full under CC BY 4.0. A shows mean optical density ± SD at each standard concentration, using 28, 19, 8, 4 and 9 calibration curves for lots 1–5, respectively. B shows individual curves from lots 1 and 5.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/eaa69ef05702db45df547dba.svg?v=eaa69ef05702)

Figure 4Feng et al. (2019), Fig. 2, reproduced in full under CC BY 4.0. A shows mean optical density ± SD at each standard concentration, using 28, 19, 8, 4 and 9 calibration curves for lots 1–5, respectively. B shows individual curves from lots 1 and 5.

A shared control can be prepared as a well-mixed batch divided into aliquots, using a fresh aliquot for each run to reduce additional variation from repeated freeze-thaw cycles. When changing reagent lots, a panel of samples measured across both lots helps reveal whether differences resemble an offset, a proportional shift, or a concentration-dependent change. Distribute experimental groups across plates where feasible. If all controls occupy one plate and all treatments another, plate effects become inseparable from the biological comparison.

Detection and quantification describe different capabilities. A low sample may produce a distinguishable signal while its inferred concentration remains too variable for the intended comparison. Lower-range samples evaluated for bias and precision establish a quantitative lower boundary. High-range samples and dilution recovery help establish the upper boundary. A computer can extrapolate far beyond the standards, but the experimental design can instead place samples in a region supported by actual calibration and control observations. Retain the raw signal and range identity of low samples rather than silently replacing every such result with zero.

Uncertainty also comes from the calibration itself. The fixed-curve sensitivity exercise isolates response error, while fitted parameters carry additional uncertainty from the finite standard dataset. Sample preparation, dilution volumes, and between-run variation add further contributions. These can be investigated by repeated complete experiments or by an uncertainty analysis matched to the study. Keeping technical replicates, independent samples, and batches separately identified makes those contributions estimable. A narrow spread among three wells is one part of that evidence, not the complete precision of a long-term study.

## Run the calculation chain, then interpret the biology

The complete program generates replicated standards, fits the calibration, and analyzes a dilution series from one original sample. It exports the standards, dilution results, an illustrative plate map, and a numerical summary. Actual calculations produce the residual, sensitivity, and matrix-effect figures. Start with the eightfold dilution and follow its raw response, inferred diluted concentration, and original-sample estimate. Independent checks cover the midpoint, inverse function, dilution conservation, recovery, and replicate coefficient of variation, so each stage can be checked with simple arithmetic.

### Complete Python: Calibration, inversion, dilution and diagnostics

Offline constructed data, weighted 4PL fitting, per-well CSV, numerical summary and actual figures; the measured publication figure is bundled.

```
"""Offline ELISA calibration, matrix effects and dilution experiment."""
from pathlib import Path
import argparse,csv,json
import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Ellipse
from PIL import Image
BLUE='#186e83';AMBER='#cd803f';GREEN='#3c8a6a';PURPLE='#8160a1'
PARAMS=(.05,2.05,100.,1.2)
def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def fourpl(c,a=.05,d=2.05,m=100.,b=1.2):
    c=np.asarray(c,dtype=float);return a+(d-a)*c**b/(m**b+c**b)
def inverse(y,a=.05,d=2.05,m=100.,b=1.2):
    y=np.asarray(y,dtype=float)
    with np.errstate(invalid='ignore',divide='ignore'):return m*((y-a)/(d-y))**(1/b)
def main(output,language='zh'):
    out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh'
    def T(a,b):return a if zh else _label(b)
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5'})
    def save(fig,name):fig.savefig(out/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    rng=np.random.default_rng(606);levels=np.array([0,6.25,12.5,25,50,100,200,400,800,1600]);x=np.repeat(levels,3)
    sigma=.006+.008*fourpl(x);raw=fourpl(x)+rng.normal(0,sigma)
    fit,cov=curve_fit(fourpl,x,raw,p0=PARAMS,sigma=sigma,absolute_sigma=True,bounds=([0,1,1,.3],[.3,4,1000,3]),maxfev=10000)
    with (out/'standards.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['concentration_pg_ml','replicate','absorbance','constructed_noise_sd']);w.writerows(zip(x,np.tile([1,2,3],len(levels)),raw,sigma))
    dilutions=np.array([1,2,4,8,16,32]);original=800.;effective=original/dilutions*(1-.4/dilutions)
    sample_signal=fourpl(effective);sample_raw=sample_signal[:,None]+rng.normal(0,.01,(len(dilutions),3));back=inverse(sample_raw,*fit)*dilutions[:,None]
    with (out/'dilutions.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['dilution','replicate','true_original_pg_ml','matrix_fraction','absorbance','estimated_original_pg_ml'])
        for i,dil in enumerate(dilutions):
            for j in range(3):w.writerow([dil,j+1,original,1-.4/dil,sample_raw[i,j],back[i,j]])
    fig,ax=plt.subplots(figsize=(11,5));ax.set(xlim=(0,12),ylim=(0,6));ax.axis('off')
    for x0,stage in [(1.5,0),(5.5,1),(9.5,2)]:
        ax.add_patch(Rectangle((x0-1,1),2,.15,fc=BLUE));ax.plot([x0,x0,x0-.5,x0,x0+.5],[1.1,2,2.5,2,2.5],color=BLUE,lw=4)
        if stage>=1:ax.add_patch(Ellipse((x0,2.65),1,.6,fc=AMBER))
        if stage>=2:
            ax.plot([x0,x0,x0-.4,x0,x0+.4],[2.95,3.5,4,3.5,4],color=PURPLE,lw=4);ax.add_patch(Ellipse((x0+.55,4.2),.8,.55,fc=GREEN));ax.text(x0+.55,4.2,'E',ha='center',va='center',color='white')
            ax.scatter([x0+.4,x0+.8,x0+1.2],[4.9,5.2,4.8],color='#d7ac3f',s=70)
    for a,b in [(2.8,4.1),(6.8,8.1)]:ax.annotate('',xy=(b,2.5),xytext=(a,2.5),arrowprops={'arrowstyle':'->','lw':1.5})
    for x0,label in [(1.5,T('固定捕获抗体','Immobilized capture')),(5.5,T('结合样品中的靶标','Bind sample target')),(9.5,T('检测抗体、酶与产物','Detector, enzyme and product'))]:ax.text(x0,.45,label,ha='center',fontsize=10)
    fig.text(.5,.94,T('1971：Engvall–Perlmann 与 van Weemen–Schuurs 的酶免疫分析工作','1971: enzyme immunoassay work by Engvall–Perlmann and van Weemen–Schuurs'),ha='center',fontsize=12)
    fig.text(.5,.015,T('现代夹心法的原创示意；酶 E 把分子识别转成可积累的颜色信号。','Original modern sandwich schematic: enzyme E converts recognition into accumulating color.'),ha='center',fontsize=10);save(fig,'history')
    grid=np.geomspace(2,3000,300);fig,ax=plt.subplots(2,2,figsize=(11,8.4))
    ax[0,0].scatter(x[x>0],raw[x>0],s=18,color=BLUE,label=T('构造标准复孔','Constructed standard wells'));ax[0,0].semilogx(grid,fourpl(grid,*fit),color=AMBER,label='4PL');ax[0,0].legend(fontsize=8);ax[0,0].set(xlabel=T('浓度 / pg/mL','Concentration / pg/mL'),ylabel=T('吸光度','Absorbance'),title=T('A  信号随浓度上升后逐渐变平','A  Response approaches a plateau'))
    ax[0,1].scatter(x,raw-fourpl(x,*fit),color=PURPLE,s=20);ax[0,1].set_xscale('symlog',linthresh=5);ax[0,1].axhline(0,color='grey',lw=1);ax[0,1].set(xlabel=T('浓度 / pg/mL','Concentration / pg/mL'),ylabel=T('实测构造值 − 拟合值','Constructed observation − fit'),title=T('B  残差保留误差的方向','B  Residuals retain error direction'))
    y=fourpl(grid);low=inverse(y-.02);high=inverse(y+.02);ax[1,0].semilogx(grid,100*(high-low)/(2*grid),color=GREEN);ax[1,0].set(xlabel=T('真实浓度 / pg/mL','True concentration / pg/mL'),ylabel=T('±0.02 信号误差对应的半宽 / %','Concentration half-width from ±0.02 signal / %'),title=T('C  同样的信号误差，不同的浓度误差','C  Equal signal error, unequal concentration error'),ylim=(0,50))
    plate=np.full((8,12),np.nan);plate_levels=np.array([0,12.5,25,50,100,200,400,800]);plate[:,:2]=fourpl(plate_levels)[:,None]+rng.normal(0,.01,(8,2));plate[:6,3:6]=sample_raw;plate[6:,3:6]=fourpl([50,300])[:,None]+rng.normal(0,.01,(2,3))
    plate_cmap=plt.get_cmap('cividis').copy();plate_cmap.set_bad('#e1e5e6')
    im=ax[1,1].imshow(plate,cmap=plate_cmap,vmin=0,vmax=2);ax[1,1].set_xticks(range(12),range(1,13));ax[1,1].set_yticks(range(8),list('ABCDEFGH'));ax[1,1].set_title(T('D  示例板：标准、稀释系列、质控','D  Example plate: standards, dilution series, QC'));fig.colorbar(im,ax=ax[1,1],label=T('吸光度','Absorbance'),fraction=.04)
    fig.tight_layout();save(fig,'calibration')
    np.savetxt(out/'plate.csv',plate,delimiter=',',header='constructed demonstration plate; NaN unused')
    fig,ax=plt.subplots(1,2,figsize=(11,4.8));ideal=inverse(sample_signal)*dilutions
    ax[0].plot(dilutions,ideal,'o-',color=BLUE,label=T('无噪声、含基质效应','Noiseless, matrix effect'));ax[0].errorbar(dilutions,back.mean(axis=1),yerr=back.std(axis=1,ddof=1),fmt='s',color=AMBER,label=T('拟合反算，3 复孔均值 ± SD','Fitted inversion, mean ± SD of 3 wells'));ax[0].axhline(800,color=GREEN,ls='--',label=T('真实原样浓度','True original concentration'));ax[0].set_xscale('log',base=2);ax[0].set_xticks(dilutions,dilutions);ax[0].set(xlabel=T('稀释倍数','Dilution factor'),ylabel=T('折算原样浓度 / pg/mL','Back-corrected concentration / pg/mL'),title=T('A  稀释减弱构造的基质抑制','A  Dilution reduces constructed matrix suppression'));ax[0].legend(fontsize=8)
    ax[1].bar([0,1,2],[40,65,62],color=[BLUE,GREEN,AMBER]);ax[1].set_xticks([0,1,2],[T('未加标','Unspiked'),T('理论加标后','Expected spiked'),T('测得加标后','Measured spiked')]);ax[1].set(ylabel=T('浓度 / pg/mL','Concentration / pg/mL'),title=T('B  加入 25，测得增加 22：回收 88%','B  Add 25, recover 22: 88% recovery'));fig.tight_layout();save(fig,'matrix')
    fig,ax=plt.subplots(figsize=(8.2,12.6));ax.imshow(Image.open(Path(__file__).resolve().parent/'feng2019-figure2.png'));ax.axis('off');ax.set_title(T('真实实验：试剂批次改变标准曲线','Measured experiment: lot-dependent standard curves'),fontsize=12)
    fig.text(.5,.012,T('Feng 等，2019，图 2；CC BY 4.0。\nA：均值 ± SD；批次 1–5 的曲线数分别为 28、19、8、4、9。','Feng et al., 2019, Fig. 2; CC BY 4.0.\nA: mean ± SD; lots 1–5 contain 28, 19, 8, 4, 9 curves.'),ha='center',fontsize=9);fig.tight_layout(rect=[0,.07,1,1]);save(fig,'published')
    assert np.isclose(fourpl(100),1.05) and np.isclose(inverse(1.05),100)
    assert np.allclose(ideal,800*(1-.4/dilutions))
    cv=np.std([98,100,102],ddof=1)/100*100
    summary={'model':{'midpoint_signal':float(fourpl(100)),'inverse_midpoint':float(inverse(1.05)),'midpoint_slope':2*1.2/(4*100),'midpoint_delta_c_for_002':.02/(2*1.2/(4*100))},'dilution':{'no_matrix_original':float(inverse(fourpl(100))*8),'one_matrix':float(ideal[0]),'eight_matrix':float(ideal[3]),'sixteen_matrix':float(ideal[4])},'spike':{'recovery_percent':(62-40)/25*100},'precision':{'cv_percent':float(cv)},'fit':{'a':float(fit[0]),'d':float(fit[1]),'m':float(fit[2]),'b':float(fit[3]),'sample_eightfold_mean':float(back[3].mean())}}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

For a first exercise, set matrix suppression to zero and inspect agreement across dilution factors. Next increase only the response noise and examine instability near the lower and upper regions. Then change the calibration midpoint and compare the concentrations assigned to one signal. Changing one part of the measurement chain at a time keeps the explanation specific. Unused wells in the plate illustration are marked as missing, not as zero concentration. No measurement, a zero standard, and a measured zero response are different states worth preserving in the data table.

Use a concrete normalization example to check the endpoint. Two wells both contain 800 picograms per milliliter. One contains one milliliter of medium and the other two milliliters, so the amounts present are 800 and 1600 picograms. If the second well also contains twice as many cells, the amounts divided by endpoint cell count may be equal. If cells multiplied or died during collection, however, the endpoint count differs from their average number over that interval. Retain concentration, volume, duration, and cell count separately rather than preserving only one final normalized value. This makes later biological explanations possible without repeating the experiment.

Comparisons between successive collection intervals need similar care. Replacing all medium starts a new accumulation interval; removing only a fraction leaves some previously accumulated target in the well. A later concentration then includes retained material as well as newly released target, modified by degradation and adsorption. The sampling record determines which mass-balance calculation is appropriate. This is closely related to repeated sampling in a release experiment: the volume removed and replaced is part of the measurement, even when the analytical assay itself is unchanged. An accurate ELISA concentration becomes more informative when the surrounding collection process is equally explicit.

Finally, consider what molecular form the assay recognizes. An intact protein, a cleaved fragment retaining both epitopes, and a complex that conceals one epitope can give different responses despite related molecular origins. If a treatment changes protein processing or binding partners, an altered immunoassay result may reflect the amount of the recognized form. A complementary measurement of size, activity, or another epitope can address that possibility. Define the reported target according to the recognition system and specimen preparation, then select the complementary experiment that answers the remaining biological question.

For a materials-and-cells study, connect the full chain: collect at a defined time and volume, investigate adsorption and matrix response, estimate concentration using same-plate standards and independent controls, then choose a total-amount or cell-related denominator that matches the question. Present independent-sample values together with technical precision and relevant dilution-recovery observations. The reader can then see which experimental object differs and how its concentration was obtained. ELISA makes molecular recognition quantitatively useful by turning an apparently unremarkable drop of liquid into a traceable measurement.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L06.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Engvall & Perlmann (1971): Quantitative assay of immunoglobulin G](https://pubmed.ncbi.nlm.nih.gov/5135623/)

   Authors, title and year of the original 1971 ELISA publication.
2. [van Weemen & Schuurs (1971): Immunoassay using antigen-enzyme conjugates](https://pubmed.ncbi.nlm.nih.gov/11945853/)

   Contemporary antigen-enzyme conjugate immunoassay publication.
3. [Cox et al.: Immunoassay Methods, Assay Guidance Manual](https://www.ncbi.nlm.nih.gov/sites/books/NBK92434/)

   Assay formats, independent controls, model selection and weighted calibration.
4. [Thermo Fisher: Spike-and-recovery and linearity-of-dilution assessment](https://documents.thermofisher.com/TFS-Assets/LSG/Application-Notes/TR0058-Spike-and-Recovery.pdf)

   Matrix response, spike design and dilution assessment on calibrated concentrations.
5. [Feng et al. (2019): A computational solution to improve biomarker reproducibility during long-term projects](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0209060)

   Measured lot effects and shared controls across plates; Fig 2.

   CC BY 4.0; Fig. 2 reproduced without cropping
6. [SciPy: scipy.optimize.curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

   Standard-deviation weights, bounds and nonlinear fitting interface.
