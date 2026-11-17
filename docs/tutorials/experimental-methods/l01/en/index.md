# Cell culture and counting: Establishing comparable starting conditions

Source: https://ml-biomat.com/tutorials/experimental-methods/l01/en/
Language: en

Connect a counting-chamber square to culture history, sampling precision and the number seeded in each well.

## Before comparing materials, establish comparable starting populations

After one day of culture, one material appears crowded with cells while another carries only a few. The difference could reflect the material, but it could also have existed before the experiment began: more cells were delivered to the first surface, a droplet collected in one corner, or the two suspensions came from cultures at different stages of growth. Culture and counting establish what entered the experiment, how much entered, and the condition of that starting population. Those facts connect later changes in color, fluorescence, protein abundance, or gene expression to the biological question.

Think of cell culture as providing an environment for a living population outside the body. Medium supplies nutrients, salts, and buffering components; a container or material provides space and attachment conditions; temperature and the gas environment influence metabolism and acidity. Cells consume substances, release products and signals, and modify their surroundings. Equal numbers therefore need not behave identically when their earlier culture history, density, or interface differs. Counting measures abundance, while the culture record helps explain the biological state behind that abundance. Both are needed when a researcher asks whether a material supports cell attachment or changes growth.

This chapter uses common mammalian-cell examples to develop transferable reasoning. Adherent cells require a suitable attachment surface, whereas suspension cells grow mainly dispersed in liquid. Primary cells are obtained directly from tissue and often retain features associated with that origin. Continuous cell lines can be expanded over extended periods and provide established experimental models. Medium, temperature, gas conditions, and passaging procedures should follow conditions validated for the particular cells. Recognizing the biological identity and growth mode comes before choosing a convenient counting procedure or applying a familiar culture recipe.

The counted object also needs a definition. Total intact cells, cells with intact membranes, cells capable of further division, and cells that actually attach to a material describe different populations. Dye-exclusion measurements classify cells by membrane permeability within a specified observation interval. That classification is relevant to viability, but differs from measuring long-term proliferation, metabolic activity, or a particular cellular function. When seeding is based on viable-cell number, record how viability was defined, then examine attachment, recovery, and morphology at an appropriate later time. This makes the biological meaning of the initial number explicit.

## Culture has a history: one passage does not mean one doubling

As a culture grows, its population, available space, and nutrient conditions change. Transferring part of the population into fresh vessels is called passaging. A passage number counts such transfers; it does not directly count how often the population has doubled. Consider two transfers that eventually return to the same original cell number. Retaining half the population requires one ideal doubling to recover that number, whereas retaining one eighth requires three. Both operations add one passage to the record. Their expansion histories differ, which is why passage number and population doublings should be understood separately.

![One passage can correspond to different population doublings: ideal recovery after 1:2 and 1:8 splits. Hayflick and Moorhead’s work introduces culture history as a variable.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/8c67918b82076b1930b529b4.svg?v=8c67918b8207)

Figure 1One passage can correspond to different population doublings: ideal recovery after 1:2 and 1:8 splits. Hayflick and Moorhead’s work introduces culture history as a variable.

In 1961, Leonard Hayflick and Paul Moorhead described the finite proliferative capacity of normal human diploid cell cultures. Their observations made the history of an expanded population an essential biological variable. The result does not assign every type of cell an identical stopping point; cell identity, conditions, and population state influence the observed behavior. Its practical lesson is that populations change during culture. Two bottles carrying the same cell-line label, sampled at different stages of expansion, do not automatically provide interchangeable starting material. Recording culture history helps a later investigator interpret changes in growth or morphology.

Population doublings translate a multiplication factor into the equivalent number of repeated twofold increases. A fourfold increase is two doublings, and an eightfold increase is three. The logarithm in the calculation is simply the mathematical tool that asks how many times two must be multiplied by itself to obtain the observed ratio. A population increasing from twenty thousand to eighty thousand cells in forty-eight hours has undergone two net doublings, giving an average doubling time of twenty-four hours. The word net matters: division, death, detachment, and losses during collection can all contribute to the two measured population sizes.

$$
\mathrm{PD}=\log_2\!\left(\frac{N_t}{N_0}\right),\qquad T_d=\frac{t}{\mathrm{PD}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/39f01eb55d50f92c89f7cf5d.svg) | Net population doublings between measurements, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/3d5bc3f33c6bf9779e0abdb9.svg) | Measured final cell count, cells. |
| ![Formula](https://ml-biomat.com/static/agent-math/358eaab52fd29057e6b95399.svg) | Measured initial cell count, cells. |
| ![Formula](https://ml-biomat.com/static/agent-math/14ae3fefbbf822ee29c5d5c8.svg) | Base-two logarithm converting a fold change to equivalent doublings. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Interval between measurements, h. |
| ![Formula](https://ml-biomat.com/static/agent-math/e6d3ee28e801518c3f5199bb.svg) | Average net doubling time over the interval, h; defined here for PD>0. |

With N_0=20000, N_t=80000 and t=48 h, the ratio is 4, PD=2 and T_d=24 h. Comparable growth phases and count definitions make comparisons biologically interpretable.

A growth curve provides context for that average. Immediately after seeding, cells may recover and attach before entering more rapid expansion. Later, crowding or nutrient changes may slow growth. Comparing doubling times is most informative when the populations occupy comparable growth phases. On a semilogarithmic graph, ideal exponential growth appears as a straight line because equal time intervals produce equal multiplication factors. A bend indicates a changing net growth rate. When evaluating two materials, a difference in attachment delay can place the populations in different phases on the same measurement day, even if their later division behavior is similar.

A master cell bank and working bank can provide traceable starting points for successive experiments. After recovery from storage, examine morphology, abundance, and growth before beginning a comparison. Unexpected changes suggest specific checks of culture conditions, identity, and contamination. Useful records include the cell name and identifier, source batch, passage or doubling history, medium and important supplements, recovery information, and seeding details. These are biological conditions linking experiments across time. A comparison becomes easier to interpret when a new batch can be connected to an earlier one through those recorded conditions.

## Separate environmental changes from the intended treatment

A colored culture medium often contains an acidity indicator. Its appearance can reveal environmental change, but direct examination of the cells still provides different information. Cellular metabolism changes nutrient availability and acidity, while buffering components interact with the gas environment. Changing the vessel, liquid volume, or time spent outside controlled conditions may therefore change the culture. Serum and other supplements also provide complex mixtures of proteins and signals; batch differences can affect attachment and growth. Material comparisons should use common conditions, or intentionally vary them within a defined design, so that handling changes do not become indistinguishable from treatment effects.

Density is itself part of the environment. For adherent cells, seeding density is often expressed per unit area; for suspension cultures, it is commonly expressed per unit volume. The actual area or volume must accompany the number. Confluence describes the fraction of a surface covered by cells, rather than a direct count. Cells that spread widely may cover more surface than an equal number of rounded cells. Seventy percent coverage on two different materials can therefore correspond to different cell populations. Keeping images of coverage alongside cell counts separates abundance from changes in cell size, shape, and spreading.

Aseptic practice preserves the biological system being studied. Other organisms can consume nutrients, release products, and alter cellular responses. Appropriate equipment and protective practice, brief opening of vessels, and clear separation of cultures and reagents help maintain that system. Clear medium does not establish that every form of contamination is absent. Mycoplasma can affect growth and expression without conspicuous cloudiness, so suitable testing is part of culture quality control. Routine antibiotics do not replace that assessment or careful handling. A sudden change in growth should lead to examination of several relevant causes rather than automatic attribution to the experimental material.

Identity and microbial contamination are separate questions. A culture can test negative for mycoplasma while carrying an incorrect label; it can also match its expected identity and still contain a contaminant. Human-cell authentication often uses short tandem repeat profiles, which compare a set of genetic markers. Morphology offers frequent, accessible observations during routine work, but similar appearance alone does not establish identity. Combining authentication records, contamination testing, and morphology describes the actual biological object used in an experiment and helps locate changes that require investigation.

Materials introduce local environmental effects as well. A surface or scaffold may change medium acidity, adsorb nutrients, release small molecules, or draw a droplet into a restricted region. Cells can also enter pores and become difficult to see from above. Recording the material state before seeding and examining distribution afterward helps distinguish failure to deliver cells, poor retention, movement into depth, and a genuine later decrease. That distinction often resolves an apparently confusing result more effectively than adding several new endpoint assays without first establishing where the cells went.

## A counting chamber works because its observed volume is known

A hemocytometer is a glass chamber with controlled geometry. Developed for counting blood cells, it is also used for many cell suspensions. A grid defines area, and the correctly seated coverslip fixes the depth above it. Multiplying area by depth gives the volume containing the counted cells. In a common improved Neubauer chamber, one large square has an area of one square millimeter and a depth of 0.1 millimeter. Its volume is therefore 0.1 cubic millimeter, or one ten-thousandth of a milliliter. Multiplying the average count in that square by ten thousand converts it to cells per milliliter.

![Real hemocytometer and associated equipment, photograph by Todd, CC BY-SA 2.0. The complete photograph is presented with bilingual annotations; this composed figure is also CC BY-SA 2.0.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/fd63802f23baf22909905be9.svg?v=fd63802f23ba)

Figure 2Real hemocytometer and associated equipment, photograph by Todd, CC BY-SA 2.0. The complete photograph is presented with bilingual annotations; this composed figure is also CC BY-SA 2.0.

![Area and chamber depth determine sampled volume. Green boundaries are included and orange boundaries excluded; the drawn cells illustrate geometry rather than reproduce the four-square dataset.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/742cd0c638ebb5fbcf7381fc.svg?v=742cd0c638eb)

Figure 3Area and chamber depth determine sampled volume. Green boundaries are included and orange boundaries excluded; the drawn cells illustrate geometry rather than reproduce the four-square dataset.

$$
V_s=Ah,\qquad C=\frac{d\sum_{i=1}^{n}N_i}{nV_s}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/af24cfe08968b9a399cca9b4.svg) | Volume of each observed region, mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Area of each observed region, mm². |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | Chamber depth, mm; Ah gives mm³, divided by 1000 to obtain mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | Concentration of the defined cell population in the original suspension, cells/mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | Total dilution factor from original suspension to counted mixture, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Number of equal-volume observed regions, dimensionless integer. |
| ![Formula](https://ml-biomat.com/static/agent-math/b26e60e55288c9229968cad0.svg) | Defined cell count in region i, cells. |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Region index from 1 to n, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | Operation summing counts over regions. |

Divide the total count by observed volume, then reverse dilution. A=1 mm² and h=0.1 mm give V_s=10⁻⁴ mL. Four squares contain 308 membrane-intact cells; d=2 gives C=2×308/(4×10⁻⁴)=1.54×10⁶ cells/mL.

The familiar conversion factor comes from geometry, rather than a universal convention shared by every counting device. Other chambers or automated consumables may have different effective depths and counted regions. Calculations should use their actual observed volume. Incorrect coverslip placement, excessive loading, bubbles, or uneven filling can break the connection between count and volume. Mix the suspension gently and thoroughly before sampling because cells settle and may form aggregates. A long delay between mixing, sampling, and loading can produce different concentrations at the top and bottom of the tube. Comparing regions or chamber sides can reveal systematic filling or mixing differences.

Cells crossing grid boundaries require a consistent ownership rule. For example, include cells touching the upper and left edges while excluding those touching the lower and right edges. Adjacent regions can then be combined without systematically counting boundary objects twice or omitting all of them. The chosen pair of adjacent included edges can follow the counting procedure; consistency is the essential feature. The observer must also distinguish cells from fragments and bubbles, and determine how aggregates are handled. Counting a cluster of several cells as one object biases abundance downward, while counting debris as cells biases it upward. Original images or square-level records allow those decisions to be revisited.

Staining often dilutes the sample at the same time that it classifies cells. Mixing equal volumes of suspension and dye produces a twofold dilution, so the measured mixture concentration must be multiplied by two to recover the original concentration. Earlier dilution steps contribute additional multiplicative factors. Observation timing also matters because membrane permeability and dye exposure may change during waiting. Recording the original sample volume, added volumes, final volume, and observation interval keeps classification and concentration conversion connected. A number with many decimal places still depends on those basic definitions being correct.

Consider four large squares containing 72, 81, 76, and 79 unstained cells, alongside 8, 9, 7, and 8 stained cells. The mean unstained count is 77 per square, while the mean total is 85. With a twofold staining dilution, the original suspension contains 1.54 million membrane-intact cells per milliliter and 1.70 million total cells per milliliter. Across all four squares, 308 of 340 counted cells are unstained, giving a membrane-intact fraction of approximately 90.6 percent. Concentration and fraction answer different questions: suspensions with identical viability percentages can supply very different numbers of viable cells in the same transferred volume.

$$
f_v=\frac{N_v}{N_v+N_d},\qquad P_v=100f_v\%
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33fc340055a349697fda4777.svg) | Cell fraction classified by membrane integrity, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/a4913ae2411f1cd97def0a6b.svg) | Membrane-intact count across observed regions, cells. |
| ![Formula](https://ml-biomat.com/static/agent-math/909a1770cd343bb9acb32947.svg) | Dye-positive count in the same regions, cells. |
| ![Formula](https://ml-biomat.com/static/agent-math/704f9911f7e55073fd93e910.svg) | Membrane-intact percentage, %. |

With a common classification and sampling scope, the denominator includes both classes. Counts of 308 unstained and 32 stained cells give 308/340=0.905882, or 90.59%. Shared volume and dilution factors cancel.

## Counting more and checking dilutions solve different problems

Estimating a population from a tiny field is like estimating city traffic from a short stretch of road: random sampling can strongly influence the result. If cells are uniformly dispersed and enter the sampled volume approximately independently, accumulating more counted objects reduces relative random variation. Under a simple Poisson sampling model, counting one hundred objects gives a relative standard-deviation scale of ten percent; counting four hundred reduces it to five percent. This explains the benefit of observing more area or additional chamber loads. More counting does not repair an incorrect chamber depth, persistent aggregate undercounting, or an omitted dilution factor.

$$
\sigma_N=\sqrt{\mu},\qquad \mathrm{CV}\approx\frac{1}{\sqrt{N}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c80d13437e108b7ecd5e7468.svg) | Standard deviation of an ideal Poisson count, cells. |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | Expected count under the same sampling conditions, cells. |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Observed accumulated count used to estimate the expected count, cells. |
| ![Formula](https://ml-biomat.com/static/agent-math/dbd8c772d1a9221850e1289c.svg) | Relative standard deviation, dimensionless; multiply by 100% for a percentage. |

For approximately independent sampling from a uniform suspension, Poisson variance equals its mean. Counts of 100 and 400 give estimated CV values of 0.10 and 0.05. This random scale excludes systematic mixing, depth, dilution and classification errors.

Precision and accuracy should therefore be distinguished. An automated counter with unsuitable settings may return very similar numbers repeatedly while consistently missing one cell population. Manual observers can also differ systematically because they use different boundary or morphology rules. Inspecting object outlines, size selection, and staining classification links automated results back to the actual image. Parameters appropriate for one cell size or treatment state may become unsuitable after cells swell, fragment, or aggregate. Comparing complete counting processes, including preparation and recognition, is more informative than comparing only instrument names.

![A retains square-level raw counts; B shows ideal counting relative SD; C uses constructed crowding undercounting to illustrate a dilution test of proportional response.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/79834e63454ddcce36a93412.svg?v=79834e63454d)

Figure 4A retains square-level raw counts; B shows ideal counting relative SD; C uses constructed crowding undercounting to illustrate a dilution test of proportional response.

A dilution series provides a complementary internal check. When known fractions of a uniform stock are prepared, measured concentration should change proportionally with those fractions. Multiplying each result back to its stock-equivalent concentration should produce similar estimates. If concentrated samples read systematically low but appropriately diluted samples recover a higher stock estimate, overlap, aggregates, or recognition saturation become plausible explanations. If very dilute samples read high, background objects deserve attention. In 2017, a NIST-led study combined controlled dilution, replication, and statistical analysis to evaluate counting precision and proportionality without first assigning a routine method as an unquestioned reference.

The dilution experiment has its own requirements. Stock suspension must remain uniform during sampling, delivered volumes must be accurate, and dilution should not itself substantially change aggregation or cell state. Otherwise the measured trend includes preparation effects as well as counting behavior. Independently preparing replicate dilutions probes variation in preparation, whereas repeatedly reading the same dilution probes another part of the measurement process. Recording results over the waiting interval can reveal sedimentation or staining-time effects. Locating variation in a particular step turns a vague concern about unreliable counts into a practical adjustment.

Another distinction concerns the level of replication. Counting four squares from one suspension does not create four independent cultures. Those squares help estimate counting variation within a shared sample, whose cells have the same culture history. Four independently prepared culture batches can reveal variation between biological preparations. A useful analysis first summarizes square-level observations within each batch and then compares batches. The same logic will matter in microscopy: ten fields from one well improve spatial sampling of that well, but do not automatically represent ten independent culture experiments.

Combining percentages requires equal attention to denominators. Suppose one field contains fifty classified cells and another contains five hundred. Averaging their viability percentages directly gives the small field and large field equal weight. If the question concerns the pooled population, add the membrane-intact counts and divide by the sum of total counts. If the question compares independently prepared samples, preserve sample-level results before summarizing the distribution across samples. The appropriate aggregation follows the scientific question. Keeping counts alongside percentages lets a reader understand both the population represented and the amount of observation supporting each estimate.

## What changes when more area is counted?

Each square represents 10⁻⁴ mL. Adjust accumulated count, square count and dilution to compare stock concentration with ideal random variation. “Double area” increases expected count and area at the same ideal density; it is a model comparison, not another observation.

[Figure: Accumulated count versus ideal relative sampling standard deviation](https://ml-biomat.com/tutorials/experimental-methods/l01/en/#L01-lab)

The interactive comparison keeps the meaning of sampled area visible. Increasing area at the same ideal density increases the expected number counted, while the inferred concentration remains unchanged. The relative sampling fluctuation becomes smaller because more objects contribute to the estimate. Changing dilution instead changes how a measured chamber concentration is converted back to stock concentration. Try these operations separately before combining them: they may both change the arithmetic, but they represent different physical actions in the experiment.

## Convert a concentration into what each well actually receives

After counting, seeding is a conservation calculation involving cell number, concentration, and volume. Suppose each well should receive ten thousand membrane-intact cells in one hundred microliters. The working suspension must then contain one hundred thousand cells per milliliter. Using the previously measured stock concentration of 1.54 million per milliliter, a small stock volume can be diluted with medium. For twelve wells and ten percent additional volume to cover handling losses, prepare 1.32 milliliters in total: approximately 85.7 microliters of stock and 1.234 milliliters of medium. The allowance increases the amount available for dispensing while keeping the target concentration unchanged.

$$
C_w=\frac{N_w}{V_w},\qquad V_f=n_wV_w(1+r),\qquad C_sV_s=C_wV_f,\qquad V_m=V_f-V_s
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e153ba9e5288ecd5c41453ef.svg) | Target working concentration, cells/mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/324c7d23fe8b6b2221fa0192.svg) | Target cell count per well, cells. |
| ![Formula](https://ml-biomat.com/static/agent-math/ec72cf11e28fd771d0f29c76.svg) | Volume dispensed per well, mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/4d13c340035341c4ed1de3a2.svg) | Final working volume prepared, mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/5b794cb38c00fee5cea77f6d.svg) | Number of planned wells, dimensionless integer. |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | Additional preparation fraction, dimensionless; 10% is 0.1. |
| ![Formula](https://ml-biomat.com/static/agent-math/59e6f76fe7f807e8f04f82ec.svg) | Membrane-intact stock concentration, cells/mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/af24cfe08968b9a399cca9b4.svg) | Stock transfer volume in this preparation equation, mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/d26d844b3e76efe75c6582e5.svg) | Added medium volume, mL. |

Conservation assumes no substantial population change during preparation and uniform dispersion. A target of 10⁴ cells in 0.1 mL for 12 wells with 10% extra gives C_w=10⁵ cells/mL and V_f=1.32 mL. With C_s=1.54×10⁶, V_s=0.085714 mL=85.714 μL and V_m=1.234286 mL. Here V_s denotes stock volume, distinct from the square volume defined in E1.

Keep units visible during this calculation. One milliliter contains one thousand microliters, so the working volume of one hundred microliters is 0.1 milliliter. Multiplying cells per milliliter by milliliters leaves cells, which is the desired quantity. A mistake between these volume units introduces a thousandfold error even when every displayed digit looks plausible. Checking whether the calculated transfer fits the expected physical scale is a useful companion to dimensional arithmetic: a concentrated stock should contribute less volume than the final diluted suspension.

The required volume can also guide preparation. If a calculation produces a transfer too small for reliable handling with the available equipment, an intermediate dilution can make the operation more manageable. Its factor must be included in the record, and the final cell-number balance should remain the same. This changes how the target suspension is prepared without changing its intended concentration. Counting uncertainty and dispensing variation then remain identifiable contributions rather than disappearing inside a single reported number.

Correct arithmetic still needs consistent delivery. Cells may settle during dispensing, producing a gradient from the first well to the last if the suspension is never mixed again. Liquid retained in a tip, bubbles, and small-volume handling can also influence delivery. For larger plates, suitable batches of mixing and dispensing, with representative checks near the beginning and end, help evaluate the process. Movement of an adherent-cell plate after seeding can concentrate cells toward the center or edge. Examine the actual distribution before deciding where later images should be acquired.

A plate is a spatial object, not merely a list of independent labels. Edge and central wells may experience different evaporation or temperature histories. Placing every control on one side and every treatment on the other makes position and treatment inseparable. The constructed heatmap illustrates this problem, while the adjacent example distributes treatments across positions. Actual designs can use randomization or row-and-column blocking, with necessary controls represented across relevant regions. Image acquisition also benefits from a predefined field-selection rule, so dense, attractive, or expected-looking regions are not preferentially sampled.

![A and B read constructed growth on linear and semilog axes. C shows a constructed position effect; D randomly distributes treatments among wells without imposing equal edge allocation.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/cf7e5812f2be62a422b32eb6.svg?v=cf7e5812f2be)

Figure 5A and B read constructed growth on linear and semilog axes. C shows a constructed position effect; D randomly distributes treatments among wells without imposing equal edge allocation.

Delivered cells and attached cells remain different quantities. For a surface experiment, an early measurement can examine unattached cells in the medium, image their distribution, or use a validated collection method to estimate the attached population. Within a three-dimensional scaffold, cells can move into depth, so a surface image should be connected to depth information or an appropriate whole-sample measurement. If two materials retain different fractions initially, their later abundance difference combines initial retention with subsequent population change. Adding an early post-seeding baseline can separate those stages and sharpen the question asked by later assays.

## Connect abundance, condition, and the next experiment

The complete example begins with square-level counts and calculates concentration, membrane-intact fraction, and working-suspension volumes. It then displays the scale of sampling variation, dilution diagnostics, growth behavior, and plate layout. Constructed curves are identified as teaching examples; the photograph shows a real counting instrument. The exported count table preserves unstained, stained, and total counts for every square. Independent numerical checks verify observed volume, viable-cell concentration, cell conservation during preparation, and the relation between growth ratio and population doublings. Each final per-well number can therefore be traced back to the objects actually counted.

### From raw counts to comparable seeding

The complete example exports square-level CSV, counting and preparation results, and five figures. Growth and position effects are labeled constructed examples; the photograph and licensing notice are bundled.

```
"""Counting-volume arithmetic, sampling variation and comparable culture starts."""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,FancyArrowPatch

def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def main(output,language):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    from matplotlib import font_manager
    fonts={f.name for f in font_manager.fontManager.ttflist};font=next((f for f in ['Microsoft YaHei','Noto Sans CJK SC','SimHei'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[font,'DejaVu Sans'] if language=='zh' else ['DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','axes.prop_cycle':plt.cycler(color=['#186e83','#cd803f','#8160a1','#3c8a6a'])})
    tr=lambda z,e:z if language=='zh' else _label(e)
    def save(fig,n):fig.savefig(output/f'{n}-{language}.svg',bbox_inches='tight');plt.close(fig)
    rng=np.random.default_rng(1010);live=np.array([72,81,76,79]);dead=np.array([8,9,7,8]);dilution=2;volume=1e-4;live_c=live.mean()*dilution/volume;total_c=(live+dead).mean()*dilution/volume;viability=100*live.sum()/(live+dead).sum()
    np.savetxt(output/'counts.csv',np.column_stack([np.arange(1,5),live,dead,live+dead]),delimiter=',',header='square,membrane_intact_count,stained_count,total_count',comments='',fmt='%d')
    fig,ax=plt.subplots(1,2,figsize=(11.3,4.4))
    for a in ax:a.set(xlim=(0,10),ylim=(0,8));a.axis('off')
    for a,ratio in zip(ax,[2,8]):
        a.add_patch(Rectangle((.5,3),2,2,facecolor='#a2cdd9'));a.text(1.5,4,tr('起始细胞','Starting cells'),ha='center',va='center',fontsize=9);a.add_patch(FancyArrowPatch((2.8,4),(5,4),arrowstyle='->',mutation_scale=20));a.add_patch(Rectangle((5.5,2),4,4,facecolor='#a2cdd9'));a.text(7.5,4,tr(f'扩增 {ratio} 倍',f'{ratio}-fold expansion'),ha='center',va='center');a.set_title(tr(f'一次传代，分配比例 1:{ratio}',f'One passage, split ratio 1:{ratio}'));a.text(5,1,tr(f'理想净群体倍增数：{np.log2(ratio):g}',f'Ideal net population doublings: {np.log2(ratio):g}'),ha='center');
    fig.text(.5,.01,tr('1961 年 Hayflick 与 Moorhead 的有限增殖研究，让培养历史成为生物学变量。','Hayflick and Moorhead’s 1961 finite-proliferation work made culture history a biological variable.'),ha='center',fontsize=10);save(fig,'history')
    fig,ax=plt.subplots(1,2,figsize=(10.6,4.8));a=ax[0]
    for z in np.linspace(0,1,5):a.axvline(z,color='#a6b8bf');a.axhline(z,color='#a6b8bf')
    pos=rng.uniform(.03,.97,(45,2));a.scatter(pos[:,0],pos[:,1],s=40,facecolor='#a2cdd9',edgecolor='#186e83');a.scatter([.2,.66,.84],[.3,.57,.8],s=45,color='#8160a1');a.set(xlim=(-.1,1.1),ylim=(-.1,1.1),aspect='equal',xlabel=tr('宽度 / mm','Width / mm'),ylabel=tr('高度 / mm','Height / mm'),title=tr('A  一大格面积为 1 mm²','A  One large square has area 1 mm²'))
    a.plot([0,1],[1,1],color='#3c8a6a',lw=3);a.plot([0,0],[0,1],color='#3c8a6a',lw=3);a.plot([0,1],[0,0],color='#cd803f',lw=3);a.plot([1,1],[0,1],color='#cd803f',lw=3)
    a=ax[1];a.axis('off');a.add_patch(Rectangle((.1,.35),.8,.2,facecolor='#c9e3e9',edgecolor='#186e83'));a.plot([.05,.95],[.57,.57],color='#8160a1',lw=5);a.text(.5,.7,tr('盖玻片固定深度：0.1 mm','Coverslip fixes depth: 0.1 mm'),ha='center',fontsize=11);a.text(.5,.2,'1 mm × 1 mm × 0.1 mm\n= 0.1 mm³ = 10⁻⁴ mL',ha='center',fontsize=14);a.set_title(tr('B  从面积到已知体积','B  From area to a known volume'));fig.tight_layout();save(fig,'chamber')
    fig,ax=plt.subplots(1,3,figsize=(12,4.4));ax[0].bar(np.arange(1,5),live,label=tr('未染色','Unstained'));ax[0].bar(np.arange(1,5),dead,bottom=live,label=tr('染色','Stained'));ax[0].set(xlabel=tr('计数大格','Counting square'),ylabel=tr('细胞计数','Cell count'),title=tr('A  四格的原始计数','A  Raw counts in four squares'));ax[0].legend(fontsize=9)
    events=np.array([25,100,400,1600]);ax[1].plot(events,100/np.sqrt(events),'o-');ax[1].set(xscale='log',xlabel=tr('累计计入的细胞数','Total counted cells'),ylabel=tr('理想相对标准差 / %','Ideal relative SD / %'),title=tr('B  随机计数的不确定性尺度','B  Scale of random counting uncertainty'))
    fraction=np.array([.1,.25,.5,1]);truth=1.7e6*fraction;biased=truth/(1+truth/3e6);ax[2].plot(fraction,truth/1e6,'o-',label=tr('成比例响应','Proportional response'));ax[2].plot(fraction,biased/1e6,'s-',label=tr('构造的高密度漏计','Constructed crowding undercount'));ax[2].set(xlabel=tr('原液所占体积分数','Stock fraction in dilution'),ylabel=tr('计数浓度 / 10⁶ mL⁻¹','Counted concentration / 10⁶ mL⁻¹'),title=tr('C  稀释检验响应是否成比例','C  Dilution tests proportionality'));ax[2].legend(fontsize=8);fig.tight_layout();save(fig,'counting')
    t=np.linspace(0,120,241);exp=20000*2**(t/24);logistic=200000/(1+9*np.exp(np.log(2)*(-t)/24));fig,ax=plt.subplots(2,2,figsize=(11.2,7.2));ax=ax.ravel();ax[0].plot(t,exp,label=tr('持续指数增长','Continued exponential growth'));ax[0].plot(t,logistic,label=tr('构造的容量受限增长','Constructed capacity-limited growth'));ax[0].set(xlabel=tr('培养时间 / h','Culture time / h'),ylabel=tr('细胞数','Cell number'),title=tr('A  同一起点，不同后期条件','A  Same start, different later conditions'));ax[0].legend(fontsize=8)
    ax[1].semilogy([0,24,48,72],[20000,40000,80000,160000],'o-');ax[1].set(xlabel=tr('培养时间 / h','Culture time / h'),ylabel=tr('细胞数（对数轴）','Cell number (log scale)'),title=tr('B  等时间倍增在半对数图上成直线','B  Equal-time doubling gives a straight semilog line'))
    plate=np.ones((8,12));plate[[0,-1],:]=1.15;plate[:,[0,-1]]=1.15;plate+=rng.normal(0,.025,plate.shape);im=ax[2].imshow(plate,cmap='cividis',vmin=.9,vmax=1.2);fig.colorbar(im,ax=ax[2],label=tr('相对读数','Relative readout'));ax[2].set(xticks=range(12),xticklabels=range(1,13),yticks=range(8),yticklabels=list('ABCDEFGH'),title=tr('C  构造的板边位置效应','C  Constructed plate-edge position effect'))
    treatments=np.tile(np.arange(4),24);rng.shuffle(treatments);layout=treatments.reshape(8,12);ax[3].imshow(layout,cmap=plt.colormaps['Set2'].resampled(4),vmin=-.5,vmax=3.5)
    for row in range(8):
        for col in range(12):ax[3].text(col,row,'ABCD'[layout[row,col]],ha='center',va='center',fontsize=8)
    ax[3].set(xticks=range(12),xticklabels=range(1,13),yticks=range(8),yticklabels=list('ABCDEFGH'),title=tr('D  处理组分散到不同位置','D  Treatments distributed across positions'));fig.tight_layout();save(fig,'culture')
    from PIL import Image
    fig,ax=plt.subplots(figsize=(9,5.9));ax.imshow(Image.open(Path(__file__).with_name('hemocytometer-todd.jpg')));ax.axis('off');ax.set_title(tr('真实计数板：精确体积来自玻璃结构与盖玻片','A real counting chamber: geometry and coverslip define volume'),fontsize=12,pad=10);fig.text(.5,.01,'Todd · Hemocytometer · Wikimedia Commons · CC BY-SA 2.0',ha='center',fontsize=9);save(fig,'instrument')
    final_volume=12*.1*1.1;stock_volume=final_volume*1e5/live_c;summary={'counting':{'volume_per_square_ml':volume,'mean_live_per_square':float(live.mean()),'live_concentration_ml':float(live_c),'total_concentration_ml':float(total_c),'viability_percent':float(viability),'live_cells_in_2ml':float(live_c*2)},'seeding':{'target_per_well':10000,'final_volume_ml':final_volume,'stock_volume_ul':float(stock_volume*1000),'medium_volume_ml':float(final_volume-stock_volume)},'growth':{'initial_cells':20000,'cells_at_48h':80000,'doublings':2,'doubling_time_h':24},'sampling':{'relative_sd_100':.1,'relative_sd_400':.05},'dilution':{'true_stock_ml':1700000,'crowded_stock_measured_ml':float(biased[-1])}}
    assert abs(live_c-1540000)<1e-8;assert abs(stock_volume*live_c-final_volume*1e5)<1e-8;assert abs(np.log2(80000/20000)-2)<1e-12
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

Start exploring by changing the dilution factor from two to four while holding chamber counts fixed, and examine the inferred stock concentration. Next, keep that stock concentration fixed and change the target number per well; the required stock volume should change proportionally. Finally, consider datasets with the same overall mean but different distributions among squares. Their average concentration can match while their spatial pattern suggests different mixing or filling quality. For real work, preserve culture-batch, material, and well identifiers, then attach later staining, metabolic, or DNA-synthesis results to the same identifiers.

The resulting starting point has several connected properties: a defined cell identity, documented culture state, measured abundance and membrane integrity, and an observed spatial distribution on the material. Live/dead imaging will next place cellular state into a spatial picture, while DNA-synthesis experiments will ask which cells are replicating genetic material. Their measurements differ, but both benefit from clear quantity, time, and location records. Building those records into the experiment makes it possible to follow how a material changes a living population instead of treating each later assay as an isolated number.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L01.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [ATCC: Animal Cell Culture Guide](https://www.atcc.org/resources/culture-guides/animal-cell-culture-guide)

   Culture, population doublings, counting geometry and sample preparation.
2. [ATCC: Cell Line Authentication Test Recommendations](https://www.atcc.org/resources/technical-documents/cell-line-authentication-test-recommendations)

   Authentication alongside morphology and culture records.
3. [ATCC: Mycoplasma Contamination](https://www.atcc.org/the-science/authentication/mycoplasma-contamination)

   Why visual clarity and routine antibiotics do not replace mycoplasma assessment.
4. [Thermo Fisher: Manually Counting Cells in a Hemocytometer](https://www.thermofisher.com/us/en/home/references/gibco-cell-culture-basics/cell-culture-protocols/counting-cells-in-a-hemacytometer.html)

   Observed volume, dilution and stock-concentration conversion.
5. [Sarkar et al. (2017): Evaluating the quality of a cell counting measurement process via a dilution series experimental design](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=921053)

   Independent dilutions, repeated observations, proportional response and precision.
6. [Hayflick and Moorhead (1961): The serial cultivation of human diploid cell strains](https://doi.org/10.1016/0014-4827%2861%2990192-6)

   Historical investigation of finite proliferative capacity in normal diploid cultures.
7. [Hayflick: Citation Classic retrospective](https://garfield.library.upenn.edu/classics1978/A1978FC39200002.pdf)

   The original investigator’s recollection of the finite-culture research.
8. [Todd: Hemocytometer photograph](https://commons.wikimedia.org/wiki/File:Hemocytometer.jpg)

   Real counting instrument photograph, author and license record.

   CC BY-SA 2.0 photograph by Todd; composed figure also CC BY-SA 2.0.
