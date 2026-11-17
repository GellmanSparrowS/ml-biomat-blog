# CCK-8 and MTT: What a color change tells us

Source: https://ml-biomat.com/tutorials/experimental-methods/l02/en/
Language: en

Cell number, metabolism and material background all contribute to a well’s color. Follow reaction chemistry, plate controls and dose curves to calculate a percentage with a defined meaning.

## 1. A well becomes paler: what happened to the cells?

When developing a hydrogel, an early question is how cells respond to it. Add a color-forming reagent after exposing the cells to the material, wait, and some wells become dark orange while others remain pale. A plate reader converts the differences into absorbance values. This is a common first encounter with a CCK-8 assay. The convenient format encourages an immediate interpretation of darker color as more living cells. To use the numbers well, follow the intermediate steps connecting the cells to the color.

Both CCK-8 and MTT use cell-associated reduction processes to generate a colored product. Reduction can initially be understood as a molecule gaining electrons. Cellular metabolism continually transfers electrons, and the assay recruits part of that activity to produce a detectable signal. Total color consequently depends on cell number, average metabolic state, reaction time and assay conditions. A restaurant provides a helpful analogy: total revenue depends on both the number of customers and the amount each customer spends. Revenue can estimate customer number only when the relationship to spending per customer is understood.

This connection determines useful applications. Comparisons within the same cell type, growth state and detection conditions can use relative metabolic response as an informative initial measurement. Cell counting, membrane-integrity staining or DNA-synthesis measurements then help distinguish changes in number, condition and proliferation. A signal falling to half its original value could reflect fewer cells remaining in the well, or cells that remain present but reduce the reagent more slowly. The latter can be biologically interesting too; its interpretation should follow the process actually measured.

This chapter follows the color reaction into the plate reader, designs a plate with matched blanks and analyzes three independent experiments. The recurring question is how to preserve the biological meaning behind a simple percentage. You will see material-associated color raise the apparent response and discover why two quantities commonly described as “50%” need not occupy the same position on a dose–response curve. The complete program reproduces the plotted values and allows controlled changes to the assumptions.

## 2. From MTT to WST-8: connecting a cell process to a microplate

In 1983, Mosmann published an MTT colorimetric method for comparing responses associated with cellular growth and survival. A microplate made many parallel conditions accessible through a common procedure, helping scale comparisons beyond individually examining every specimen. The method also made a question about interpretation especially important: which cellular process generates the measured response? Radiolabeled thymidine incorporation had provided another route into proliferation studies by following DNA synthesis. Color-forming reduction and DNA synthesis could both contribute to studies of growth, while reporting different biological events.

![Original diagrams connect the MTT microplate approach to soluble-product WST-8 detection. MTT crystals require appropriate solubilization; WST-8 uses an electron mediator. The diagram follows the measurement chain rather than assigning every reaction to one organelle.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/71f9d0ea000d6fe7138446fc.svg?v=71f9d0ea000d)

Figure 1Original diagrams connect the MTT microplate approach to soluble-product WST-8 detection. MTT crystals require appropriate solubilization; WST-8 uses an electron mediator. The diagram follows the measurement chain rather than assigning every reaction to one organelle.

MTT belongs to the tetrazolium family. Cell-associated reduction produces colored formazan. At this stage, “formazan” can be understood as the chemical class of the colored product rather than a name to memorize in full structural detail. MTT formazan has low solubility and forms crystals, so an additional solubilization step normally precedes absorbance measurement. Incomplete dissolution leaves particles and uneven color. This links a chemical property to a practical operation: the same amount of product presents different optical conditions when evenly dissolved and when distributed as irregular crystals.

CCK-8 uses a WST-8 system in which an electron mediator connects cellular reducing activity to production of a soluble formazan. A mediator is an intermediate participant that transfers electrons between reaction partners. Keeping the colored product in the culture medium makes subsequent reading more direct. CCK-8 is commonly read at 450 nm, while dissolved MTT formazan is often measured near 570 nm. The primary wavelength, reference wavelength and handling sequence belong to the particular assay formulation. Choosing a reagent therefore includes considering specimen color, material composition and the cellular process under study.

A diagram placing every reduction event inside one mitochondrion would oversimplify the chemistry. Several enzymes and reducing molecules participate in cellular electron transfer, and their contributions can change with culture state and treatment. Materials can also affect the assay outside the cells. Reducing components may generate color directly, dark particles may absorb or scatter detection light, and surfaces may bind reagent or product. The experiment should separate measurable material contributions from cell-associated signal and use a complementary biological readout when it helps identify the cause of a change.

## 3. The reader measures light; biology is interpreted afterwards

A plate reader sends light of a selected wavelength through the liquid in a well and measures the light reaching the detector. Colored product absorbs part of that light, and absorbance is calculated from the sample-to-reference intensity ratio. Darker liquid transmits less light in the relevant spectral region. Absorbance carries no unit of cells. Converting it into cell number requires a relationship established with known cell numbers under comparable conditions. Cell identity, growth state and reaction time belong to that relationship; a kit name alone does not supply a universal conversion table.

$$
A=-\log_{10}\!\left(\frac{I}{I_0}\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Absorbance, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/112feff6b4d0334226e24d5c.svg) | Intensity measured after passage through the well, in the same units as I₀. |
| ![Formula](https://ml-biomat.com/static/agent-math/6e4f2807ce72e4cab3957130.svg) | Corresponding reference intensity; the ratio is dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/be8ebdecd039424afe275a60.svg) | Base-10 logarithm. |

When transmitted intensity is 50% of reference, A≈0.301. Absorbance is a logarithm of an intensity ratio. Subtracting matched absorbances compares an additional absorption contribution; absorbance itself has no unit of cell number.

The optical path in a microplate depends on liquid volume, well geometry and reading configuration. Unequal final volumes can change both reagent proportions and optical conditions. A bubble introduces another interface into the light path. Keeping final volume, mixing and preparation for reading consistent helps make the comparison reflect the intended specimen differences. For turbid materials, a reference wavelength may help characterize background, but its correction depends on how the material behaves at both wavelengths. A background contribution that changes strongly with wavelength needs a more specific treatment than subtraction of an arbitrary second reading.

Color-development time is an experimental variable. During an appropriate early interval, product can accumulate at an approximately steady rate. Over longer periods, substrate availability, cell condition and the detection range may change. If reagent is added column by column and the entire plate is read together, the first and last columns have different reaction times. Multichannel pipetting, a fixed addition sequence, appropriate batches or a validated stopping procedure can bring the intended time closer to the time each specimen actually experiences.

Cell seeding number and color-development time should therefore be explored together. Few cells with a short incubation may produce a signal barely above background. Many cells with a long incubation may enter a curved or saturated response region. The number–time plots later in the chapter illustrate that tradeoff. A useful working range separates the anticipated specimens reliably while preserving some room above and below them. A small cell-number series read at two or more development times provides a direct way to establish this experimental scale.

The total time under study also has two distinct parts: exposure to the material and incubation with the detection reagent. A 24-hour material exposure followed by a two-hour color-development step answers a different question from a two-hour material exposure. Record both. This distinction becomes especially helpful when comparing papers or planning a sequence of time points, because an assay's detection chemistry can evolve during its own incubation rather than passively reporting a frozen cellular state.

A three-dimensional hydrogel introduces a spatial question as well. Reagent must move from the surrounding solution into the network, and product must accumulate where the readout samples it. Gel thickness, pore structure and cell distribution can affect this process. Two gels containing the same number of cells can give different short-incubation readings if transport differs. A thickness and incubation-time comparison, together with sections or three-dimensional imaging of cell distribution, helps investigate this connection. Transferring a calibration from a thin culture layer to a three-dimensional specimen therefore calls for transport and sampling conditions to enter the calibration design.

## 4. Design blanks that match the material experiment

Imagine a colored material whose absorbance at 450 nm increases with concentration. Subtracting the same medium-plus-reagent blank from every treatment leaves the material's concentration-dependent color in the result. Even while the cell-associated signal declines, the total absorbance may appear to decline less strongly or even rise. Address this at the plate-design stage: include cell-free wells at every material concentration, matching the other ingredients and handling as closely as possible. They measure the combined material and reagent contribution under the corresponding condition.

![Constructed first experiment: 48 active wells are randomized; circles identify matched cell-free blanks. The right panel preserves sample signal, matched background and their difference, showing the material-concentration contribution. Grey wells are unused.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9d049b947eff820cc9d8f00f.svg?v=9d049b947eff)

Figure 2Constructed first experiment: 48 active wells are randomized; circles identify matched cell-free blanks. The right panel preserves sample signal, matched background and their difference, showing the material-concentration contribution. Grey wells are unused.

In the example, sample wells contain cells, material and detection reagent. Matched blanks contain the corresponding material concentration, culture medium and reagent but no cells. The zero-material cell wells provide the reference for that experiment, with zero-material cell-free wells providing their background. Together these measurements supply the numerator and denominator of the calculation. If a solvent is involved, reference wells should reflect the relevant solvent conditions as well. A control known to change the readout can establish that the assay responds to a substantial perturbation, with its purpose and treatment conditions explicitly defined.

Matched blanks directly address additive background. For example, material absorption measured in a cell-free well can be subtracted from a comparable cell-containing well. Product adsorption creates a different problem: the same amount of generated product can have a different signal recovery in the presence of the material. Adding comparable product or signal standards to systems with and without material can test recovery. An additional readout, such as microscopic cell counting, can help separate detection-chemistry effects from changes in the specimen. Each control is most useful when it answers a specific experimental question.

Plate position also matters. Evaporation and temperature at the edge may differ from conditions near the center. Placing all high-concentration specimens on one side of a plate can confound dose with position. The example randomly assigns 48 active wells in a 96-well plate and retains row, column, condition and replicate identifiers. Real experiments can use randomization or balanced blocks alongside measures appropriate to their cell type and incubation period. A plate heatmap helps reveal an unusual row, a localized outlier or a pattern associated with addition order.

$$
R=100\,\frac{A_s-A_{bs}}{A_c-A_{bc}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | Relative metabolic response, expressed as a numerical percentage. |
| ![Formula](https://ml-biomat.com/static/agent-math/33fe913a815d09d9b267ca3d.svg) | Mean absorbance of treated cell wells, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/f4621c2ce242814ee1f6cada.svg) | Mean absorbance of dose-matched cell-free wells, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/0e856b4c890d783d82136df7.svg) | Mean reference-cell absorbance in the same experiment, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/7e60fe3eaa0f62628aab7f65.svg) | Mean cell-free blank absorbance for the reference condition, dimensionless. |

With sample 0.54, matched blank 0.14, reference 0.84 and reference blank 0.04, the result is 100×0.40/0.80=50%. The denominator is a positive, distinguishable reference signal within the same experiment; subtraction assumes the matched blank represents additive background.

A short worked example makes the logic concrete. The treated sample reads 0.54 and its matched material blank reads 0.14. The reference cell well reads 0.84 and its blank reads 0.04. Their cell-associated differences are 0.40 and 0.80, giving a relative response of 50%. Subtracting only 0.04 from the treated sample instead gives 62.5%. Those 12.5 percentage points arise from background handling before any additional cellular mechanism is invoked. Mapping each term in the calculation to an actual type of well is an effective way to find a missing control.

When the cell-associated signal approaches background variation, subtraction can produce a small negative value. This is a measured difference near zero, not a negative number of cells. Retain the original difference and examine blank variation and the range of distinguishable signals. Replacing every negative value with zero shifts the average response upwards and hides information about measurement precision in this region.

## 5. Separate cell number, metabolic response and replication

Within a verified approximately linear regime, signal can be decomposed into cell number, mean per-cell reaction rate and color-development time, multiplied by a factor connecting product formation to absorbance. The purpose is to identify variables, rather than to assume a universal constant for cellular metabolism. If treatment halves cell number while doubling the average reduction rate of the remaining cells, total signal can remain unchanged. A treatment that primarily changes metabolism can be described as a metabolic-response change and followed with measurements addressing cell number or membrane integrity.

$$
S\approx\kappa N q t
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | Matched-blank-corrected absorbance, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/cb154160fd6d330501f6321c.svg) | Signal factor at the reference per-cell activity, in cell⁻¹ h⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Number of participating cells, in cells. |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | Mean per-cell reaction activity relative to a reference state, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Color-development time, in h. |

In a suitable linear regime, κ=4×10⁻⁵ cell⁻¹ h⁻¹, N=5000, q=1 and t=2 h give S=0.40. N=2500 with q=2 gives the same signal. The model assumes compatible reaction-rate, transport and optical conditions and separates the contributions of number and per-cell state.

Activity, viability and proliferation should be connected to their observables. Membrane-integrity staining examines whether cells exclude certain dyes. EdU assays examine DNA synthesis during a defined interval. Counting measures the number of identifiable cells. CCK-8 and MTT examine cell-associated reduction and color formation. Combining them supports more specific interpretations. A reduced color response with similar cell counts and maintained membrane integrity motivates investigation of cellular metabolism or assay chemistry. Changes in all three measurements provide a different combination of evidence to explain.

Replication also has levels. Three wells prepared for one condition during one experiment mainly describe variation associated with dispensing, well state and reading. An independently prepared experiment, with its own cells and treatment preparation, provides information about variation at a different level. Independence depends on what was prepared separately, not simply on whether two files have different dates. The teaching example uses three independently constructed experiments as its statistical units. Three technical wells are averaged within each experiment and dose before matched-blank subtraction and reference normalization.

After normalization, the zero-dose reference is exactly 100% in every experiment because that result is imposed by the definition. It does not mean the original reference wells lacked variation. Their values remain in the absorbance table and affect the denominators for other doses. Error bars in the figure are sample standard deviations across the three independent experiments. Treating nine technical wells as nine independent experiments would ignore the culture and treatment conditions shared within each experiment, giving an uncertainty description that does not match the design.

![Four connected questions: A is a simplified number–time model; B shows identical signals from half the cells with twice the per-cell activity; C compares three independently constructed experiments with common-blank-only analysis; D shows day means with between-day sample SD (n=3). Zero dose participates in analysis but is not plotted on the logarithmic axis.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9666a47c4ea73c15d8b51af2.svg?v=9666a47c4ea7)

Figure 3Four connected questions: A is a simplified number–time model; B shows identical signals from half the cells with twice the per-cell activity; C compares three independently constructed experiments with common-blank-only analysis; D shows day means with between-day sample SD (n=3). Zero dose participates in analysis but is not plotted on the logarithmic axis.

At the highest material concentration, 50 μg/mL, the matched-blank-corrected mean response in this example is approximately 21.45%. Subtracting only the common blank gives approximately 37.46%. Showing the three experiment curves makes agreement and variation easier to judge than an average bar alone. All cell and absorbance values here are constructed, with their generation rules retained. The controlled example isolates the background effect so the analysis can be understood before the same table structure is used with measured data.

Normalization also determines the denominator of any statement about a percentage. A response of 80% here is relative to the corrected cell-associated signal of the reference in the same experiment. It is not a direct count of 80 live cells out of every 100 observed cells. If a fraction of individually classified live cells is required, a counting or imaging method can provide that denominator. Making the denominator explicit usually clarifies the interpretation more efficiently than adding general cautions after reporting a number.

## 6. Two different “50%” positions on a dose–response curve

Plot material concentration against relative response and a common pattern is a high plateau, a descending transition and a lower plateau. A logarithmic concentration axis spreads out low-dose values when the range is broad. Zero cannot appear on a logarithmic axis, so it can participate in normalization and fitting while being separately identified or omitted from that display. Fitting summarizes the response range and its position, allowing comparisons based on defined quantities. The shape alone does not uniquely identify the cellular mechanism that produced it.

$$
y(c)=L+\frac{U-L}{1+(c/K)^h},\qquad y(K)=\frac{U+L}{2},\qquad c_{y=50}=K\left(\frac{U-50}{50-L}\right)^{1/h}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | Material exposure concentration, in μg/mL here. |
| ![Formula](https://ml-biomat.com/static/agent-math/014d06406569aa2ddd6cfa41.svg) | Fitted relative response at that concentration, as a numerical percentage. |
| ![Formula](https://ml-biomat.com/static/agent-math/00d614107d5e3a57ff52ec95.svg) | Fitted upper and lower plateaus on the same percentage scale as y. |
| ![Formula](https://ml-biomat.com/static/agent-math/24733a44cf365eb5e1b92574.svg) | Concentration at the fitted dynamic-range midpoint, in μg/mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | Positive slope parameter controlling steepness, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/6b482d895dca66782c68edea.svg) | Concentration at 50% of reference response, in μg/mL; it exists here when L<50<U. |

The example gives U≈99.81, L≈16.03, K≈7.86 and h≈1.442. The dynamic-range midpoint response is about 57.92%, while y=50 occurs near 10.25 μg/mL. Here 50 means 50% on the response scale. The concentration ratio c/K is dimensionless before exponentiation.

The four-parameter model describes an upper plateau, a lower plateau, a concentration halfway through that dynamic range and a slope. When concentration equals the midpoint parameter, the concentration ratio in the denominator equals one. The response is consequently the average of the two plateaus. If the upper plateau is 100% and the lower is 20%, the dynamic-range midpoint is 60%, not 50%. This simple substitution explains why a fitted half-maximal parameter and the concentration reducing the response to 50% of an untreated reference may differ.

Here the fitted upper plateau is about 99.81%, the lower plateau about 16.03%, and the dynamic-range midpoint concentration about 7.86 μg/mL. The concentration corresponding to 50% of the reference response is about 10.25 μg/mL. Two horizontal lines in the figure show these definitions. Reporting “concentration at the fitted dynamic-range midpoint” or “concentration giving 50% of the reference response” carries the meaning with the number. If the measured concentration range does not approach the lower plateau, additional suitable concentrations or a different summary question can make the analysis better supported by the observations.

The slope parameter describes the steepness of the transition but does not by itself specify what happened inside the cells. Material dispersion, release kinetics, population variation and detection chemistry can all affect the observed shape. Comparisons between materials should therefore retain exposure duration, concentration units, cell identity and whether exposure involved direct contact or an extract. Equal mass concentrations of particles with different sizes can correspond to different surface areas. Those conditions determine what a comparison of the curves actually compares.

Curve fitting should also return to the individual experiment results. A smooth line through average values can conceal a consistent shift between independently prepared experiments. Plotting those curves alongside the summary shows whether the transition location is stable. The example preserves both levels rather than discarding the experiment identifiers after averaging. For a research study, the choice of a model for variation should follow the preparation hierarchy and the question being asked, just as the signal normalization follows the plate controls.

The concentration axis also needs to describe the exposure stage correctly. Adding 10 μL of a 100 μg/mL material suspension to 90 μL of medium produces 10 μg/mL after mixing: the same material amount is distributed through a total volume of 100 μL. Adding detection reagent later changes the reading volume, while the exposure-dose definition should remain explicit. Sedimentation or adsorption at the well bottom can further separate the nominal added concentration from the conditions experienced near the cells. Recording dispersion, mixing and contact geometry helps explain differences between experiments using the same nominal dose.

## 7. From raw well readings to reproducible figures

The complete program creates three independent experiments, each containing eight material concentrations with three cell wells and three matched blanks per concentration. That gives 144 well-level observations. It records well position, concentration, well type, replicate identity and raw absorbance, then groups data by experiment and dose. Technical wells are averaged first, the matching background is removed, and each result is normalized to the reference signal from the same experiment. The three curves are then summarized and the mean response is fitted. The structure keeps the experimental hierarchy available throughout the analysis.

The heatmap shows the first experiment, while the dose plots summarize all three. Output tables preserve both corrected and common-blank-only results. Separate explicitly simplified models produce the cell-number versus incubation-time curves and the example of different cell counts giving the same signal. They explain working ranges and the number–metabolism relationship; they are not presented as measurements of a particular cell line. A numerical summary reports the hand-calculated correction example, highest-dose responses and both half-response concentrations so that plots, tables and equations can be cross-checked.

### Complete example: 144 well readings and three experiment curves

The program generates declared teaching data and exports well-level CSV, experiment summaries, three figure sets and numerical results. Each experiment is corrected before aggregation; language changes figure labels only.

```
"""A constructed CCK-8 plate experiment: matched blanks and independent days.

All assay values are simulated for teaching; no biological measurements are
claimed. Each of three days has its own response, and each condition has three
technical wells. Output includes raw well-level data and day-level summaries.
"""
from pathlib import Path
import argparse,csv,json
import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle,FancyArrowPatch

BLUE,RED,GOLD,GREY='#12687b','#be6047','#b18a35','#758893'

def response(dose,bottom,top,half,hill):
    return bottom+(top-bottom)/(1+(np.asarray(dose)/half)**hill)

def blank_correct(sample,sample_blank,control,control_blank):
    denominator=np.asarray(control)-np.asarray(control_blank)
    if np.any(denominator<=0):raise ValueError('A positive control signal is required.')
    return 100*(np.asarray(sample)-np.asarray(sample_blank))/denominator

def run(out,lang):
    out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],
        'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#b8c9cf',
        'svg.fonttype':'none','axes.unicode_minus':False,'savefig.facecolor':'white'})
    t=lambda z,e:z if lang=='zh' else e
    def save(fig,name):fig.savefig(out/f'{name}-{lang}.svg',bbox_inches='tight');plt.close(fig)
    def arrow(ax,start,end):ax.add_patch(FancyArrowPatch(start,end,arrowstyle='->',mutation_scale=16,lw=2,color=BLUE))
    rng=np.random.default_rng(83)
    doses=np.array([0,.5,1,2,5,10,20,50.])
    records=[];day_ratios=[];naive_ratios=[];means_by_day=[]
    for day in range(3):
        top_signal=.8*(1+.06*(day-1));half=8*(1+.12*(day-1))
        expected=response(doses,15,100,half,1.4)/100
        blank=.04+.0025*doses
        sample=top_signal*expected[:,None]+blank[:,None]+rng.normal(0,.012,(8,3))
        acellular=blank[:,None]+rng.normal(0,.004,(8,3))
        sample_mean=sample.mean(axis=1);blank_mean=acellular.mean(axis=1)
        ratios=blank_correct(sample_mean,blank_mean,sample_mean[0],blank_mean[0])
        naive=100*(sample_mean-blank_mean[0])/(sample_mean[0]-blank_mean[0])
        day_ratios.append(ratios);naive_ratios.append(naive);means_by_day.append((sample_mean,blank_mean))
        positions=rng.choice(96,size=48,replace=False);cursor=0
        for i,dose in enumerate(doses):
            for kind,array in [('cells',sample),('matched_blank',acellular)]:
                for rep in range(3):
                    pos=int(positions[cursor]);cursor+=1
                    records.append({'day':day+1,'well':chr(65+pos//12)+str(pos%12+1),
                        'row':pos//12,'column':pos%12,'dose_ug_ml':dose,'kind':kind,
                        'technical_replicate':rep+1,'absorbance':float(array[i,rep])})
    ratios=np.array(day_ratios);naive=np.array(naive_ratios)
    mean=ratios.mean(axis=0);sd=ratios.std(axis=0,ddof=1)
    parameters,covariance=curve_fit(response,doses,mean,p0=[15,100,8,1.4],
        bounds=([0,90,.01,.2],[50,110,100,4]),maxfev=10000)
    bottom,top,half,hill=parameters
    absolute_50=half*((top-50)/(50-bottom))**(1/hill) if bottom<50<top else None
    dense=np.geomspace(.2,80,300)

    fig,axs=plt.subplots(1,2,figsize=(12.7,5.4),layout='constrained')
    for ax in axs:ax.set(xlim=(0,10),ylim=(0,7));ax.axis('off')
    ax=axs[0];ax.set_title(t('A  MTT：1983年的微孔板比色思路','A  MTT: a microplate color assay in 1983'),loc='left',pad=20)
    ax.add_patch(Circle((2,4.5),1.1,fc='#d9e9e3',ec=BLUE,lw=2));ax.text(2,4.5,t('细胞内\n还原过程','Cellular\nreduction'),ha='center',va='center')
    arrow(ax,(3.2,4.5),(4.7,4.5));ax.text(3.8,5,t('MTT','MTT'),ha='center')
    for x,y in [(5.4,4.6),(5.9,4.2),(6.3,4.7),(5.4,4.0)]:ax.plot(x,y,marker='D',ms=14,color='#765080')
    ax.text(5.9,3.1,t('不溶性甲臜结晶','Insoluble formazan crystals'),ha='center',fontsize=10)
    arrow(ax,(6.8,4.5),(8.3,4.5));ax.add_patch(Rectangle((8.4,3.5),1,2,fc='#baa1c7',ec=GREY));ax.text(8.9,2.7,t('溶解后读数','Dissolve, then read'),ha='center',fontsize=10)
    ax.text(.4,.9,t('把大量平行样品放进一块板里比较\n颜色产生的速度仍与细胞状态有关','Compare many parallel specimens in one plate\nColor production still depends on cellular state'),fontsize=11)
    ax=axs[1];ax.set_title(t('B  WST-8：把产物留在溶液里','B  WST-8: keep the product in solution'),loc='left',pad=20)
    ax.add_patch(Circle((2,4.5),1.1,fc='#d9e9e3',ec=BLUE,lw=2));ax.text(2,4.5,t('细胞还原力','Cellular\nreducing power'),ha='center',va='center')
    arrow(ax,(3.2,4.5),(4.5,4.5));ax.text(4.8,5.4,t('电子介体','Electron mediator'),ha='center',fontsize=10)
    ax.add_patch(Circle((5,4.5),.42,fc=GOLD));arrow(ax,(5.6,4.5),(7.2,4.5))
    ax.add_patch(Rectangle((7.3,3.5),1.5,2,fc='#e8b66c',ec=GREY));ax.text(8,2.7,t('可溶性甲臜','Soluble formazan'),ha='center',fontsize=10)
    ax.text(.4,.9,t('CCK-8通常在450 nm读取\n示意图关注测量链，不表示反应位置的全部细节','CCK-8 is commonly read at 450 nm\nA measurement-chain diagram, not every reaction site'),fontsize=11)
    save(fig,'history-chemistry')

    fig,axs=plt.subplots(1,2,figsize=(12.7,5.8),layout='constrained')
    plate=np.full((8,12),np.nan);kinds={}
    for rec in records:
        if rec['day']==1:plate[rec['row'],rec['column']]=rec['absorbance'];kinds[(rec['row'],rec['column'])]=rec['kind']
    cmap=plt.colormaps['YlOrBr'].copy();cmap.set_bad('#edf1f3')
    im=axs[0].imshow(plate,cmap=cmap,vmin=0,vmax=.9,aspect='equal')
    for (r,c),kind in kinds.items():
        if kind=='matched_blank':axs[0].plot(c,r,marker='o',ms=4,mfc='none',mec=BLUE)
    axs[0].set(xticks=np.arange(12),xticklabels=np.arange(1,13),yticks=np.arange(8),yticklabels=list('ABCDEFGH'),title=t('A  第一次实验的48个随机排布读数','A  Forty-eight randomized wells on day 1'))
    fig.colorbar(im,ax=axs[0],shrink=.7,label=t('吸光度','Absorbance'))
    axs[0].text(.5,-.16,t('圆圈：无细胞匹配空白；灰格：未使用','Circles: matched cell-free blanks; grey: unused'),ha='center',transform=axs[0].transAxes,fontsize=10)
    ax=axs[1]
    a,b=means_by_day[0]
    ax.plot(doses,a,'o-',color=RED,label=t('细胞 + 材料 + 试剂','Cells + material + reagent'))
    ax.plot(doses,b,'o-',color=GOLD,label=t('材料 + 试剂，无细胞','Material + reagent, no cells'))
    ax.plot(doses,a-b,'o-',color=BLUE,label=t('相减后的细胞相关信号','Cell-associated difference'))
    ax.set(xlabel=t('材料浓度 / μg·mL$^{-1}$','Material concentration / μg/mL'),ylabel=t('吸光度','Absorbance'),title=t('B  匹配空白随材料浓度改变','B  Matched blanks change with material dose'));ax.legend(fontsize=9);ax.grid(alpha=.13)
    save(fig,'plate-controls')

    fig,axs=plt.subplots(2,2,figsize=(12.7,8.1),layout='constrained')
    ax=axs[0,0];n=np.linspace(0,20000,200)
    for time,col in [(1,BLUE),(2,RED),(4,GOLD)]:
        signal=1.5*(1-np.exp(-.00004*n*time/1.5))
        ax.plot(n,signal,color=col,label=f'{time} h')
    ax.set(xlabel=t('每孔细胞数','Cells per well'),ylabel=t('构造的校正吸光度','Constructed corrected absorbance'),title=t('A  铺板数量与孵育时间共同影响响应','A  Cell number and incubation time act together'));ax.legend()
    ax=axs[0,1];xx=np.linspace(0,4,200)
    ax.plot(xx,.2*xx,color=BLUE,label=t('数量×单细胞活性：1×1','Number × per-cell activity: 1 × 1'))
    ax.plot(xx,.2*xx,color=RED,ls='--',lw=3,label=t('数量×单细胞活性：0.5×2','Number × per-cell activity: 0.5 × 2'))
    ax.set(xlabel=t('显色时间 / h','Color-development time / h'),ylabel=t('理想线性吸光度','Ideal linear absorbance'),title=t('B  不同细胞数量可能给出相同信号','B  Different cell counts can give the same signal'));ax.legend(fontsize=9)
    ax=axs[1,0]
    for day,col in enumerate([BLUE,RED,GOLD]):ax.plot(doses,ratios[day],'.-',color=col,alpha=.9,label=t(f'独立实验 {day+1}',f'Independent day {day+1}'))
    ax.plot(doses,naive.mean(0),'s--',color=GREY,label=t('只减共同空白','Common blank only'))
    ax.set(xlabel=t('浓度 / μg·mL$^{-1}$','Concentration / μg/mL'),ylabel=t('相对代谢响应 / %','Relative metabolic response / %'),title=t('C  每次实验先校正，再比较重复','C  Correct each day before comparing repeats'));ax.legend(fontsize=9)
    ax=axs[1,1]
    ax.errorbar(doses[1:],mean[1:],yerr=sd[1:],fmt='o',color=BLUE,capsize=4,label=t('日均值 ± 日间SD，n=3','Day means ± between-day SD, n=3'))
    ax.plot(dense,response(dense,*parameters),color=BLUE,lw=2)
    midpoint=(top+bottom)/2
    ax.axhline(midpoint,color=GOLD,ls=':',label=t('拟合动态范围的中点','Halfway through fitted dynamic range'))
    ax.axhline(50,color=RED,ls='--',label=t('对照信号的50%','50% of control signal'))
    ax.set(xscale='log',xlabel=t('浓度 / μg·mL$^{-1}$（对数轴）','Concentration / μg/mL (log axis)'),ylabel=t('相对代谢响应 / %','Relative metabolic response / %'),title=t('D  两种“50%”对应不同浓度','D  Two meanings of “50%” give different concentrations'));ax.legend(fontsize=8)
    save(fig,'response-diagnostics')

    with (out/'well-data.csv').open('w',newline='',encoding='utf8') as f:
        writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    np.savetxt(out/'day-summary.csv',np.c_[doses,ratios.T,mean,sd,naive.mean(0)],delimiter=',',
        header='dose_ug_ml,day1_percent,day2_percent,day3_percent,mean_percent,between_day_sd,common_blank_only_percent',comments='')
    summary={'origin':'Constructed teaching data, seed 83; 3 independent days × 8 doses × 2 well types × 3 technical wells',
        'well_count':len(records),'independent_days':3,'technical_wells_per_condition':3,
        'worked_example_corrected_percent':float(blank_correct(.54,.14,.84,.04)),
        'worked_example_common_blank_percent':100*(.54-.04)/(.84-.04),
        'corrected_high_dose_percent':float(mean[-1]),'common_blank_high_dose_percent':float(naive.mean(0)[-1]),
        'fitted':{'bottom_percent':float(bottom),'top_percent':float(top),'half_dynamic_range_ug_ml':float(half),'hill':float(hill),'absolute_50_control_ug_ml':float(absolute_50)},
        'known_true_half_dynamic_range_ug_ml':8.0,'control_percent_each_day':ratios[:,0].tolist()}
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
    assert len(records)==144 and np.allclose(ratios[:,0],100)
    assert np.isclose(summary['worked_example_corrected_percent'],50,atol=1e-12)
    assert 6<half<10 and absolute_50>half
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();run(a.output,a.language)
```

First set the concentration-dependent material-background coefficient to zero and observe the two analysis paths approach each other. Restore it, increase the measurement noise in the cell-free wells and inspect the spread after correction. This makes the role of blanks a quantitative question. Increasing the number of technical wells while retaining three independent experiments still leaves three experimental units for assessing between-experiment variation. Technical replication improves the estimate within an experiment; independent replication helps characterize variation across separate preparations.

## Interactive experiment: How many cell states can give the same color?

Set the reference cell-associated absorbance to 0.80 and common medium/reagent background to 0.04. Independently change cell number, per-cell activity and additive material background in a linear teaching model. Compare the common-blank-only result with the matched-blank-corrected response.

[Figure: Cell number, corrected response and common-blank-only response, with a number–activity response map](https://ml-biomat.com/tutorials/experimental-methods/l02/en/#L02-plot)

Map color represents the product of number and activity. Different combinations along the dashed curve all give 100% corrected response. The model uses additive material background; adsorption and transport changes call for recovery and reaction-condition checks.

The interactive view provides another controlled comparison. Change the relative number of cells, mean per-cell activity and additive material background independently. The corrected color response follows the product of number and activity in the stated linear model, while the uncorrected response also increases with background. Try a setting with fewer cells and greater per-cell activity, then compare it with the original setting. Two identical color signals can arise from different cellular configurations, which explains why a second biological measurement can be so informative.

## 8. Write a percentage as a clear experimental result

A complete result identifies the cell type and material exposure, states the exposure and development times, defines the matched blank and reference, and reports relative metabolic response with the number of independent experiments. Cell counting or live/dead staining can then help explain the source of a change. Similar cell counts with a changed color response focus attention on per-cell state and detection chemistry. If cell number changes as well, proliferation, detachment and death become different processes to investigate rather than interchangeable labels.

For biomaterials, the way the specimen participates in detection deserves as much attention as the cells. Direct contact can change attachment and the optical path, extracts can introduce soluble components, and particles can change the reading as they mix or settle. Recording these conditions in the design and data table makes the next experiment concrete: add a dose-matched blank, compare signal recovery, or introduce a measurement that observes cells directly. Each additional control then has a defined purpose connected to an unresolved part of the measurement.

Understanding CCK-8 and MTT means being able to trace the path from cellular state through electron transfer, colored product, optical reading and normalization. Color offers a convenient comparison, matched controls and replication establish its interpretation, and complementary measurements connect the signal to more specific biological processes. The live/dead staining chapter moves from a combined signal for an entire well to images of individual cells, introducing another scale on which cellular state can be examined.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L02.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Mosmann (1983): Rapid colorimetric assay for cellular growth and survival](https://pubmed.ncbi.nlm.nih.gov/6606682/)

   Historical paper and abstract for the MTT microplate assay.
2. [Assay Guidance Manual: Cell Viability Assays](https://www.ncbi.nlm.nih.gov/sites/books/NBK144065/?report=classic)

   Tetrazolium chemistry, metabolic readouts, interference and assay design.
3. [Dojindo: Cell Counting Kit-8 product manual](https://www.dojindo.com/manual/CK04/)

   WST-8, electron mediation, reading wavelengths and condition optimization.
4. [Dojindo: Measuring Cell Viability / Cytotoxicity](https://www.dojindo.com/products/pdf/Protocol/Cell_Counting_Kit-8.pdf)

   Material color, cell-free background and assay-interference questions.
5. [GraphPad: Relative versus absolute IC50](https://www.graphpad.com/guides/prism/latest/curve-fitting/reg_50_of_what__relative_vs_absolu.htm)

   Difference between a fitted dynamic-range midpoint and 50% of a reference response.
6. [SciPy: curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

   Bounded nonlinear fitting and residual definitions.
7. [Cell Viability Assays for 3D Cellular Constructs](https://pubmed.ncbi.nlm.nih.gov/37142936/)

   Further reading on viability measurements in three-dimensional cellular constructs.
8. [Huyck et al. (2012): XTT measurements in three-dimensional matrices](https://pmc.ncbi.nlm.nih.gov/articles/PMC3419859/)

   An experimental case of validating assay performance and cellular accessibility in three-dimensional matrices; the paper uses XTT.
