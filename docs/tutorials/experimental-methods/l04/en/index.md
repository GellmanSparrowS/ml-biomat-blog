# EdU assays: Tracking DNA synthesis

Source: https://ml-biomat.com/tutorials/experimental-methods/l04/en/
Language: en

Use a timed molecular label to distinguish DNA synthesis, positive fraction and population growth.

## Before cells become more numerous, ask who is copying genetic information

A material carries more cells on the second day than on the first, suggesting population growth. Another material shows little net change, although division and loss could be occurring together. Final counts alone do not fully describe those processes. An EdU experiment asks a more time-specific question: which cells synthesized new DNA during a chosen interval? DNA is the long molecule that stores genetic information, and cells preparing for ordinary division generally copy that information. Marking newly synthesized material connects a population-level observation to a molecular process occurring within particular cells.

EdU is a nucleoside analogue related to thymidine. A nucleoside can be understood as one form of the raw material used to build DNA. After uptake and metabolic conversion, EdU can become incorporated during DNA synthesis. Its small chemical handle can subsequently be connected to a fluorescent molecule. This separates recording a biological event from making that record visible. The researcher defines the labeling interval, then examines which nuclei retain a detectable record of synthesis during that interval.

The labeling interval is commonly called a pulse. Thirty minutes, two hours, and a full day ask different questions. A short pulse more closely samples the population synthesizing DNA around that moment, while a longer pulse includes cells entering synthesis later. A positive fraction therefore belongs with its pulse start and end times. Comparing materials labeled for different durations combines a biological difference with a changed observation window. Even with equal pulse lengths, culture state and cell-cycle behavior influence the interpretation.

EdU complements live/dead staining. Within a membrane-intact green population, some cells synthesize DNA during the pulse and others do not. EdU negativity does not mean death, and positivity does not establish that one complete division has occurred. Detecting DNA synthesis, observing a division event, and counting the eventual population occupy different positions along the same biological sequence. Selecting the position of interest helps determine the labeling window and follow-up measurements, making a material’s cellular effects more specific than a general claim that cells grew well.

## A small chemical handle connects cell biology to click chemistry

Before EdU became a familiar tool, researchers studied DNA synthesis using labeled thymidine and analogues such as BrdU. Incorporated BrdU can be recognized by antibodies, but its position within double-stranded DNA must become accessible. Common detection procedures consequently include treatments that alter DNA structure. A useful question followed: could a smaller chemical label be incorporated first, then located using a small detection molecule? This connected the biology of DNA replication with selective chemical reactions that join molecules together.

In 2008, Adrian Salic and Timothy Mitchison reported detection of EdU-labeled DNA using fluorescent azides. A terminal alkyne on EdU reacts with an azide group in a copper(I)-catalyzed coupling, one of the reactions associated with click chemistry. Imagine incorporating a tiny connector into a growing polymer and attaching its fluorescent partner afterward. The connector analogy corresponds to real functional groups, while the reaction still requires appropriate reagents, chemical conditions, and access to the target. Separating incorporation from fluorescence detection is the central experimental advantage of that design.

![EdU incorporation and subsequent fluorescent click detection are separate stages. A constructed G1/S/G2/M cycle shows why pulse overlap with S phase matters; the 2008 original study supplies the historical context.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/af7c948f27b56bdaa5487b3f.svg?v=af7c948f27b5)

Figure 1EdU incorporation and subsequent fluorescent click detection are separate stages. A constructed G1/S/G2/M cycle shows why pulse overlap with S phase matters; the 2008 original study supplies the historical context.

The original study compared EdU-labeled cells with samples receiving no EdU and with samples in which DNA synthesis was inhibited. Those controls linked nuclear fluorescence to incorporation rather than merely presenting an attractive stained image. The work also demonstrated applications in cells and tissues and followed labels after the initial pulse. Its experimental logic remains useful: the chemical handle creates a detection capability, while negative and process controls establish what that capability measures in the current sample. A well-chosen control makes the biological event behind the fluorescence more explicit.

A common imaging workflow incorporates EdU during live-cell culture, followed by fixation, permeabilization, and click detection. Fixation preserves structures, while permeabilization provides detection reagents access to intracellular targets. Fluorescence generally appears during the later chemical reaction. Thus incorporation in living cells and visualization in prepared specimens occupy distinct stages. The original work explored additional specimen conditions, and later formulations improved compatibility with certain fluorescent proteins. When combining labels, arrange the workflow around the selected chemistry, including how pre-existing fluorescence behaves during the copper-containing detection step.

## A positive nucleus records a history within the cell cycle

The familiar cell cycle is easier to understand as a sequence than as a list of letters. During G1, cells grow and prepare to copy DNA. During S phase, DNA synthesis occurs. G2 includes further preparation, and M includes mitotic division and associated partitioning. Not every cell continually moves around this cycle: some leave active cycling, while others spend longer in a particular phase. In a conventional proliferation experiment, EdU mainly records cells replicating DNA during the pulse. The label therefore records an interval of experience rather than assigning only the phase occupied at the instant of imaging.

For example, a cell in S phase at the beginning of the pulse may enter G2 before fixation while retaining EdU. Another cell may begin in G1 and enter S during the two-hour window, acquiring a label later. Classifying cells only from DNA content or morphology at the endpoint describes a different aspect of those histories. Combining EdU with an independent DNA-content measurement and the timing record helps distinguish when synthesis occurred from where a cell lies in its cycle when measured.

A deliberately simplified phase model makes pulse duration easier to visualize. Let one cycle last twenty-four hours, with an eight-hour S phase. Starting phases are uniformly distributed among fixed tracking units, three quarters of which participate in the cycle. An extremely short but detectable pulse samples an eight-hour phase interval. Extending the pulse to two hours includes another two hours of starting phases that will enter S before the pulse ends. The covered interval is now ten hours, giving an overall ideal fraction of three quarters multiplied by ten divided by twenty-four, or 31.25 percent.

$$
f_{\mathrm{cover}}=g\,\min\!\left(1,\frac{T_S+T_P}{T_C}\right),\qquad T_P>0
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/12bf2f205cc2df4a17703941.svg) | Ideal fraction of fixed tracking units whose pulse overlaps S phase, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/439e3cc8d431c550923e0870.svg) | Fraction of tracking units participating in the cycle, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/79bf081bc99237d993a45dda.svg) | S-phase duration, h. |
| ![Formula](https://ml-biomat.com/static/agent-math/0e53f812f5b4ea65a73be379.svg) | Positive labeling-pulse duration, h; zero pulse produces no actual incorporation. |
| ![Formula](https://ml-biomat.com/static/agent-math/c671358096b31204cca6d4e0.svg) | Complete cycle duration, h, with 0<T_S≤T_C. |
| ![Formula](https://ml-biomat.com/static/agent-math/6a05d6e83f4c2e8f52c235d7.svg) | Minimum operation limiting coverage of cycling units to one. |

Assume uniform initial phase, fixed stage durations, a denominator not updated by division, and labeling from any positive overlap. With g=0.75, T_S=8 h, T_C=24 h and T_P=2 h, coverage is 0.3125; pulses of 8 and 16 h give 0.50 and 0.75. Detection additionally depends on signal threshold.

A conveyor-belt analogy makes the model concrete. Tracking units begin at different positions around a belt, and acquire a mark only while crossing a colored section. Opening the labeling window briefly records units already nearby. Keeping it open longer includes units arriving later, even if the belt moves at exactly the same speed. A real population also gains and loses members and produces daughters. Holding those processes fixed in the teaching model makes the contribution of the observation window visible before additional biological complexity is introduced.

The model holds tracking units fixed and asks whether their phase trajectories intersect S phase. It does not add newly produced daughter nuclei to the denominator. An expanding biological population has a more complex age distribution, variable cycle durations, and changing cell numbers, particularly during long pulses. This simple model isolates the geometry of the observation window: a longer pulse can increase the positive fraction without accelerating any individual cell’s cycle. Estimating an actual cycle duration requires a model matched to population growth, sampling, and denominator definition, supported by suitable time-resolved observations.

Other biological processes can also separate DNA synthesis from population expansion. DNA repair may involve localized synthesis, and some cells replicate DNA without completing ordinary division. Multinucleated cells and varying ploidy further separate one nucleus from one cell. In those settings, DNA content, morphology, observed divisions, or relevant process markers help interpret EdU. Describing the measured objects as EdU-positive nuclei preserves the immediate observation more accurately than calling them newly produced cells. It also leaves a clear route to the next biological question.

## Choose pulse, concentration, and controls around one question

For a material comparison, first choose the biological stage of interest. Early post-seeding observations may focus on attachment and recovery, with a later DNA-synthesis measurement helping separate attachment delay from replication behavior. Groups need comparable starting abundance, culture history, and density, together with records of material area and retained cells. The sampling time specifies which culture stage is observed, while pulse duration specifies how much time is integrated around that stage. Saying only that EdU was measured after one day leaves the actual labeling window undefined.

Solution preparation follows conservation of the labeling compound. Preparing five milliliters of a twenty-micromolar working solution from a ten-millimolar stock requires ten microliters of stock, with diluent added to a final five milliliters. Mixing this twofold working solution with an equal volume of existing medium produces ten micromolar in the final mixture. This example explains dilution arithmetic; the selected concentration and duration follow the cell system and detection conditions. Confusing working and final concentrations, or millimolar and micromolar units, changes exposure even when the experiment carries the same nominal name.

$$
C_sV_s=C_wV_w,\qquad C_f=\frac{C_wV_w+C_mV_m}{V_w+V_m}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/59e6f76fe7f807e8f04f82ec.svg) | Stock concentration, μmol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/af24cfe08968b9a399cca9b4.svg) | Transferred stock volume, mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/e153ba9e5288ecd5c41453ef.svg) | Prepared working concentration, μmol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/ec72cf11e28fd771d0f29c76.svg) | Working volume, mL; in the second expression, volume entering the mixture. |
| ![Formula](https://ml-biomat.com/static/agent-math/b4840a9faca02419281df787.svg) | EdU concentration in existing medium, μmol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/d26d844b3e76efe75c6582e5.svg) | Existing medium volume entering the mixture, mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/1c47656593144cdd6182f400.svg) | Final mixed concentration, μmol/L. |

Ten mmol/L equals 10000 μmol/L. Preparing 5 mL at 20 μmol/L requires V_s=20×5/10000=0.010 mL, or 10 μL. Equal-volume mixing with EdU-free medium gives 10 μmol/L, assuming negligible reaction or adsorption during preparation.

Dimensional checking makes the preparation easier to verify. Multiplying concentration by volume gives the amount of compound, and that amount is conserved when only solvent is added. The same calculation works whether all volumes are expressed in milliliters or microliters, provided the units remain consistent on both sides. A twofold working solution is useful when it will be mixed one-to-one with existing medium; the working concentration should then be recorded separately from the concentration actually experienced by the cells.

Ending the pulse requires an equally clear timing definition. If medium is changed in the first group and the final group is handled half an hour later, effective labeling duration may follow the processing order. That difference matters especially for short pulses. Small batches with matching intervals, interleaved conditions, and recorded start, stop, and fixation times help maintain the intended comparison. For a thick scaffold, exchanging the external liquid and clearing label from its interior can occur on different timescales, so the nominal window should be connected to actual cellular exposure.

A no-EdU sample undergoing identical fixation and detection establishes nonspecific background. A sample with known replication activity checks that incorporation and detection work together. A process control matched to the question helps connect signal changes with DNA synthesis. Material autofluorescence, probe adsorption, reagent penetration, and specimen retention during preparation require appropriate comparisons as well. If many cells detach during fixation and permeabilization, a clear image of the remaining nuclei still describes a changed denominator. Tracking retention connects sample preparation to the population ultimately measured.

Increasing concentration or extending labeling can improve signal visibility, while also changing exposure to a compound participating in cellular metabolism and DNA. Ligasová and colleagues showed that incorporation efficiency and later responses vary with cell identity, concentration, and exposure schedule. A practical pilot compares several relevant labeling windows while examining signal separation, morphology, and subsequent abundance. The chosen condition should answer the intended question clearly. For extended tracking, retain an unlabeled comparison so that the labeling procedure itself remains an identifiable part of the experimental conditions.

Two-pulse experiments add another temporal distinction. One distinguishable marker can record an earlier synthesis interval and another a later interval, identifying populations with continuing, ending, or newly initiated labeling. Detection compatibility, cross-recognition, and order need their own validation; different display colors do not establish independence of the chemistry. A single well-defined pulse, a reliable total-nucleus denominator, and a fixed observation time already answer many material–cell questions. Mastering that simpler design makes subsequent temporal combinations easier to interpret.

## Find all nuclei before asking which ones contain new-DNA label

An independent nuclear stain establishes the full object population. Locating nuclei only from the EdU channel can omit negative nuclei and inflate the positive fraction. Instead, identify regions from the total-nucleus channel and transfer those same regions to the EdU channel for measurement. Touching nuclei may merge into one object, while fragmented nuclei may be counted more than once. Apply a predefined rule to objects crossing image boundaries. Overlaying segmentation on original images provides a direct check of what each row in the exported table represents.

![Constructed images of 480 nuclei: an independent nuclear channel establishes the denominator, EdU records the pulse, and object signals are compared with DNA signal. Pixel size 1 μm; known central regions measure intensity rather than complete nuclear volume.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/ed82c5afa8a7cb4f12f3c56a.svg?v=ed82c5afa8a7)

Figure 2Constructed images of 480 nuclei: an independent nuclear channel establishes the denominator, EdU records the pulse, and object signals are compared with DNA signal. Pixel size 1 μm; known central regions measure intensity rather than complete nuclear volume.

Background, exposure, and threshold selection follow general fluorescence principles, but EdU introduces a biological source of weak signal. A cell entering S near the end of a pulse incorporates label for only a short interval, whereas another may synthesize DNA throughout the window. A high threshold favors strongly labeled objects; an excessively low threshold includes background. Negative controls and threshold-sensitivity analysis help distinguish those effects. The reported positive fraction then has a clear relationship to both the labeling interval and the measurement’s detection criterion.

The constructed example contains 480 nuclei, of which 360 participate in the ideal cycle. During a two-hour pulse, 150 have any overlap with S phase, giving 31.25 percent. The program assigns EdU signal in proportion to overlap duration, constructs noisy nuclear images, and extracts mean pixel values from known regions. Even before adding noise, a detection threshold excludes some nuclei with only brief overlap. In this example, the ideal signal threshold detects 142 nuclei. The difference makes incorporation and detection distinct, inspectable steps in the measurement.

$$
\mathrm{LI}=\frac{N_{\mathrm{EdU+}}}{N_{\mathrm{nuclei}}},\qquad P_{\mathrm{EdU+}}=100\,\mathrm{LI}\%
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ce82b781069415402958ad88.svg) | Labeling index: positive nuclear fraction under the defined pulse and threshold, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/45b530b2ed4744ea22fcc10d.svg) | Number of independently localized nuclei exceeding the EdU criterion, nuclei. |
| ![Formula](https://ml-biomat.com/static/agent-math/7c6bf26a946440e4ff236342.svg) | All included nuclei within the same sampling scope, nuclei. |
| ![Formula](https://ml-biomat.com/static/agent-math/c71d463a060ff611b7e505ed.svg) | Percentage of EdU-positive nuclei, %. |

The independent nuclear channel establishes the denominator. Sixty positives among 200 nuclei give LI=0.30, or 30%; forty among 100 give 40% but only forty positive nuclei. The example preserves geometric incorporation and image-detected counts separately.

Mean nuclear intensity and integrated intensity answer different questions. A larger region has a larger summed signal at the same mean pixel brightness. Mean intensity therefore describes signal per sampled pixel, while a whole-nucleus integrated value combines signal density with the region’s size. This example uses small known central nuclear regions so that measured intensity can be related clearly to overlap time. Those regions are not intended to estimate complete nuclear volume. An experimental analysis chooses regions and intensity summaries according to its question and preserves those definitions across the comparison.

The independent nuclear channel also makes an unanticipated biological change visible. If treated cells have unusually large, fragmented, or closely packed nuclei, a segmentation method tuned on the control may behave differently in the treated group. Inspect examples from the full range of conditions before applying one analysis procedure. A revised procedure should be evaluated consistently across those conditions. This connects the image-analysis decision to the structures actually present, instead of allowing a treatment-associated shape change to become an unnoticed counting change.

Report total nuclei, positive nuclei, and fraction together. Condition A might contain 200 nuclei, of which sixty are positive, giving thirty percent. Condition B might contain one hundred nuclei with forty positives, giving forty percent. B has the larger fraction but fewer positive nuclei. A question about the size of the replication-active population supported by a material benefits from absolute counts or area density. A question about the fraction of the existing population labeled during a window uses its corresponding denominator. Presenting both retains information that either quantity alone would discard.

Multiple predefined fields can describe spatial variation across one material sample. Those fields share culture and preparation conditions, so analysis should retain the sample level. Three-dimensional scaffolds additionally require depth information, reagent-access assessment, and rules preventing repeated counting of nuclei appearing in neighboring sections. A maximum-intensity projection can display label distribution, while three-dimensional object counting requires a spatial connectivity procedure. Many nuclei within one well provide extensive observation of that well; independent culture preparations provide a different level of replication.

## Change the time window, then read a measured example

The interactive model places cycle duration, S-phase duration, and pulse length within one timing relationship. With the cycling fraction fixed, extending the pulse covers more starting phases. Extending S phase also increases coverage during a given pulse. These changes can produce similar positive fractions through different biological processes. One fraction generally cannot determine the cycling fraction, S-phase duration, and entire cycle duration simultaneously. A time series, independent population information, or other cell-cycle measurements gradually separates those contributions.

## What happens if only the pulse becomes longer?

The cycle is fixed at 24 h, with S phase starting at phase 8 h. Green marks S phase; orange marks starting phases that can overlap it during the pulse. Adjust pulse, S duration and cycling fraction to see how different conditions can produce the same labeled fraction.

[Figure: Pulse and S-phase coverage with fraction curve](https://ml-biomat.com/tutorials/experimental-methods/l04/en/#L04-lab)

![A: uniform-phase fixed-denominator coverage; B: any incorporation versus detection threshold; C: ideal chase dilution; D: total counts, positive counts and fractions shown together. All data are constructed examples.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/0d9a574f8a19626de777dae1.svg?v=0d9a574f8a19)

Figure 3A: uniform-phase fixed-denominator coverage; B: any incorporation versus detection threshold; C: ideal chase dilution; D: total counts, positive counts and fractions shown together. All data are constructed examples.

Replacing EdU-containing medium after the pulse and examining later times creates a chase experiment. Previously labeled DNA can be retained, distributed, and diluted as cells progress. Under ideal stable labeling, symmetric division, and no further incorporation, each division halves the average label per descendant. Two divisions leave approximately one quarter, while four leave one sixteenth. As signal approaches the detection threshold, members of the original labeled lineage may become difficult to identify. Following the signal distribution alongside positive counts helps distinguish this detection effect from a disappearance of the original biological population.

$$
\bar L_k=\frac{\bar L_0}{2^k},\qquad f_k=\frac{\bar L_k}{\bar L_0}=2^{-k}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7cb7ac0bb1fc44085ece8589.svg) | Mean label per descendant after k ideal symmetric divisions, arbitrary label-amount units. |
| ![Formula](https://ml-biomat.com/static/agent-math/45e8eecb99b23d5d75f6affe.svg) | Mean initial label per cell at chase start, same units. |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | Number of divisions, dimensionless nonnegative integer. |
| ![Formula](https://ml-biomat.com/static/agent-math/e86f759b6e0ce297b6383e26.svg) | Mean retained label fraction per descendant, dimensionless. |

With stable label, symmetric partitioning, no further incorporation and no other losses, each division distributes average label among twice as many cells. Two divisions leave 25% and four leave 6.25%. This is a mean per descendant, not a claim of identical spatial label distribution within every nucleus.

A chase can also follow location. Cells labeled near a material surface may later move into its interior. A change in the local positive fraction can then combine population change, migration, and signal dilution. Spatial registration, repeated imaging, or predefined regional analysis can help separate those processes, especially when total nuclei are retained at every time point. The time course and spatial map become complementary observations. A reduction of visible label in one region then leads to a more specific question about where the population went and how its signal changed.

An actual experiment illustrates another layer: equal extracellular concentration does not guarantee equal incorporation signal in different cells. Figure 2 from Ligasová and colleagues compares EdU concentration responses and the effect of adding thymidine. Panel A uses eight-hour labeling and the mean signal of the most strongly labeled five percent of nuclei, normalized to the signal at a high reference concentration. Panel B uses a two-hour interval and the most strongly labeled thirty percent. Its vertical axis therefore describes a defined signal ratio, rather than the positive fraction of the complete population.

![Ligasová et al. (2015), Fig. 2, CC BY 4.0, reproduced intact. A: 8 h labeling, mean signal in brightest 5% of nuclei relative to 50 μM; B: 2 h labeling, thymidine-plus-EdU/EdU-only signal in brightest 30%. Error bars are SEM from triplicate experiments. Percentages denote normalized signals.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/5976c8397b9a49685ca70beb.svg?v=5976c8397b9a)

Figure 4Ligasová et al. (2015), Fig. 2, CC BY 4.0, reproduced intact. A: 8 h labeling, mean signal in brightest 5% of nuclei relative to 50 μM; B: 2 h labeling, thymidine-plus-EdU/EdU-only signal in brightest 30%. Error bars are SEM from triplicate experiments. Percentages denote normalized signals.

Read the concentration axis first, then compare the ranges in which the different cell populations develop detectable signal. Their differences connect uptake, metabolic conversion, and incorporation efficiency to the final readout. Panel B shows how a related substrate changes the EdU response. Error bars represent the standard error of the mean, describing uncertainty in the estimated mean across repeated experiments; this differs from standard deviation describing the spread of individual results. Concentration, duration, object selection, and normalization reference all contribute to the meaning of the plotted curves.

The same reasoning returns to materials research. A material can alter cell density, nutrient availability, or the local environment, so EdU signal can reflect both DNA-synthesis behavior and label access or utilization. Relevant comparisons examine exposure under comparable conditions, whether selected image regions represent the specimen, and whether nuclei are retained through preparation. With those relationships established, EdU becomes time-defined evidence that can be connected to attachment, population expansion, and cellular function on the material.

## Trace each nucleus back to the process changed by the material

The complete program saves raw nuclear and EdU images, region labels, object-level measurements, and summaries. A reader can start from one nucleus, identify its overlap between pulse and S phase, inspect its constructed incorporation signal, compare the measured pixel intensity, and follow its final classification. Additional plots show pulse coverage, threshold sensitivity, chase dilution, and the relationship between count and denominator. Constructed image positions and signals are identified as teaching data, while the real experimental figure retains its separate conditions and attribution.

### Generate nuclear images from pulse overlap and measure detection

The complete example exports two raw image arrays, nuclear regions, object-level CSV, four figures and a summary. Constructed data use a fixed seed; the published figure and license are bundled.

```
"""EdU pulse coverage, nuclear image measurements and labeling decisions."""
from pathlib import Path
import argparse,json
import numpy as np
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


def pulse_overlap(phase,duration,s_start=8.,s_end=16.,cycle=24.):
    phase=np.asarray(phase);overlap=np.zeros_like(phase,dtype=float)
    for k in range(int(np.ceil(duration/cycle))+2):overlap+=np.maximum(0,np.minimum(phase+duration,s_end+k*cycle)-np.maximum(phase,s_start+k*cycle))
    return overlap

def main(output,language):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    from matplotlib import font_manager
    fonts={f.name for f in font_manager.fontManager.ttflist};font=next((f for f in ['Microsoft YaHei','Noto Sans CJK SC','SimHei'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[font,'DejaVu Sans'] if language=='zh' else ['DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','axes.prop_cycle':plt.cycler(color=['#186e83','#cd803f','#8160a1','#3c8a6a'])})
    tr=lambda z,e:z if language=='zh' else _label(e)
    def save(fig,name):fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    rng=np.random.default_rng(404);n=480;cycling=360;phase=(np.arange(cycling)+.5)*24/cycling;overlap=np.r_[pulse_overlap(phase,2),np.zeros(n-cycling)];true_signal=60*overlap;ideal_labeled=overlap>0;ideal_detected=true_signal>=15
    final_phase=np.r_[(phase+2)%24,np.zeros(n-cycling)];dna=np.where(final_phase<8,2,np.where(final_phase<16,2+(final_phase-8)/4,4));order=rng.permutation(n);true_signal=true_signal[order];dna=dna[order];overlap=overlap[order];ideal_labeled=ideal_labeled[order];ideal_detected=ideal_detected[order]
    positions=np.array([(15+24*x,15+24*y) for y in range(20) for x in range(24)],float)+rng.uniform(-2,2,(n,2));yy,xx=np.mgrid[:490,:590];nuclei=np.full(xx.shape,20.);edu=np.full(xx.shape,20.);labels=np.zeros(xx.shape,int)
    for i,((x,y),signal,d) in enumerate(zip(positions,true_signal,dna)):
        kern=np.exp(-((xx-x)**2+(yy-y)**2)/(2*3.4**2));nuclei+=d*35*kern;edu+=signal*kern;labels[(xx-x)**2+(yy-y)**2<2**2]=i+1
    nuclei+=rng.normal(0,1,nuclei.shape);edu+=rng.normal(0,1,edu.shape);measured=np.array([edu[labels==i+1].mean()-20 for i in range(n)]);measured_dna=np.array([nuclei[labels==i+1].mean()-20 for i in range(n)])/35
    detected=measured>=15;np.savetxt(output/'nuclei.csv',np.column_stack([np.arange(1,n+1),overlap,dna,true_signal,measured,detected.astype(int)]),delimiter=',',header='nucleus,overlap_h,relative_DNA_content,true_EdU_au,measured_EdU_au,positive',comments='');np.savez_compressed(output/'nuclear_images.npz',nuclei_raw=nuclei,edu_raw=edu,roi_labels=labels,pixel_um=1.)
    fig,ax=plt.subplots(2,1,figsize=(10.8,7.4));a=ax[0];a.axis('off');a.set(xlim=(0,10),ylim=(0,3));a.text(.4,2.65,tr('活细胞：掺入小标签','Live cells: incorporate a small tag'),fontsize=12);a.text(5.6,2.65,tr('检测阶段：连接荧光标记','Detection: attach a fluorescent reporter'),fontsize=12)
    for left in [.6,5.9]:
        a.plot([left,left+3],[1.15,1.15],color='#186e83',lw=3);a.plot([left,left+3],[1.75,1.75],color='#186e83',lw=3)
        for x in np.linspace(left+.2,left+2.8,7):a.plot([x,x],[1.15,1.75],color='#91bac7',lw=2);a.scatter([x,x],[1.15,1.75],color='#186e83',s=32)
        a.scatter([left+1.5],[1.75],color='#cd803f',s=80,zorder=5)
    a.plot([2.1,2.1],[1.75,2.15],color='#cd803f',lw=2);a.text(2.1,2.28,'EdU',color='#aa6529',ha='center',fontsize=10);a.add_patch(FancyArrowPatch((3.9,1.45),(5.4,1.45),arrowstyle='->',mutation_scale=22));a.text(4.65,1.95,'Cu(I)',ha='center',fontsize=10);a.plot([7.4,7.4,8.05],[1.75,2.1,2.1],color='#8160a1',lw=2);a.scatter([8.05],[2.1],marker='*',s=230,color='#8160a1');a.text(5,.35,tr('DNA 梯形为核苷位置示意；星号为后来连接的荧光探针。','DNA ladder depicts nucleotide positions; the star marks the reporter attached later.'),ha='center',fontsize=10);a.text(5,.05,tr('2008 年 Salic 与 Mitchison：将 DNA 掺入与小分子点击检测相连接。','Salic and Mitchison, 2008: connect DNA incorporation with small-molecule click detection.'),ha='center',fontsize=10)
    a=ax[1];stages=[(0,8,'G1'),(8,8,'S'),(16,6,'G2'),(22,2,'M')];colors=['#b9d8e2','#3c8a6a','#d8c7e5','#d6aa81']
    for (start,width,name),c in zip(stages,colors):a.barh(1.25,width,left=start,height=.3,color=c);a.text(start+width/2,1.25,name,ha='center',va='center')
    for y,start,over in [(.8,6,0),(.5,9,2),(.2,15,1)]:
        a.barh(y,2,left=start,height=.15,color='#e2c5a9')
        if over:a.barh(y,over,left=max(start,8),height=.15,color='#3c8a6a')
        a.text(start+2.4,y,tr(f'2 h 脉冲；重叠 {over} h',f'2 h pulse; overlap {over} h'),fontsize=10,va='center')
    a.set(xlim=(0,24),ylim=(0,1.65),yticks=[],xlabel=tr('构造周期中的位置 / h','Position in a constructed cycle / h'));fig.tight_layout();save(fig,'history')
    fig,ax=plt.subplots(2,2,figsize=(11,8));a=ax[0,0];a.imshow(nuclei,cmap='Blues_r',origin='lower',vmin=20,vmax=160,extent=[0,590,0,490]);a.set_title(tr('A  全部核：独立建立分母','A  All nuclei establish the denominator'));a.set(xlabel='x / μm',ylabel='y / μm')
    a=ax[0,1];a.imshow(edu,cmap='magma',origin='lower',vmin=20,vmax=145,extent=[0,590,0,490]);a.set_title(tr('B  EdU：记录脉冲内的掺入','B  EdU records incorporation during the pulse'));a.plot([430,530],[35,35],color='white',lw=3);a.text(480,50,'100 μm',color='white',ha='center',fontsize=9);a.set(xlabel='x / μm',ylabel='y / μm')
    a=ax[1,0];a.scatter(measured_dna,measured,c=np.where(detected,'#8160a1','#8aa0a8'),s=12,alpha=.65);a.axhline(15,color='#cd803f',ls='--');a.set(xlabel=tr('相对 DNA 信号','Relative DNA signal'),ylabel=tr('核内 EdU 均值 / a.u.','Mean nuclear EdU / a.u.'),title=tr('C  脉冲末端的 DNA 与 EdU','C  DNA and EdU at the end of the pulse'))
    a=ax[1,1];a.hist(measured,bins=40,color='#186e83');a.axvline(15,color='#cd803f',ls='--');a.set(xlabel=tr('扣背景核内 EdU / a.u.','Background-corrected nuclear EdU / a.u.'),ylabel=tr('核数','Nuclei'),title=tr('D  阈值与短暂进入 S 期的弱信号','D  Threshold and weak signal from brief S-phase overlap'));fig.suptitle(tr('固定相位群体的构造图像；每个核定位区域已知','Constructed fixed-cohort images; nuclear measurement regions are known'),fontsize=11);fig.tight_layout();save(fig,'nuclei')
    fig,ax=plt.subplots(2,2,figsize=(11.2,7.5));duration=np.linspace(.05,20,200)
    for fraction in [.5,.75,1.]:ax[0,0].plot(duration,100*fraction*np.minimum(1,(8+duration)/24),label=f'g={fraction}')
    ax[0,0].set(xlabel=tr('脉冲长度 / h','Pulse duration / h'),ylabel=tr('几何覆盖比例 / %','Geometric coverage / %'),title=tr('A  固定追踪单位的相位覆盖模型','A  Phase coverage of fixed tracking units'));ax[0,0].legend(fontsize=9)
    qs=np.linspace(1,125,125);ax[0,1].plot(qs,[100*np.mean(measured>=q) for q in qs]);ax[0,1].axhline(31.25,ls=':',color='#8160a1',label=tr('有任意掺入的比例','Any-incorporation fraction'));ax[0,1].axvline(15,ls='--',color='#cd803f');ax[0,1].set(xlabel=tr('判定阈值 / a.u.','Decision threshold / a.u.'),ylabel=tr('检出阳性比例 / %','Detected positive fraction / %'),title=tr('B  掺入与检出之间的差别','B  Incorporation versus detection'));ax[0,1].legend(fontsize=8)
    divisions=np.arange(5);ax[1,0].plot(divisions,100/2.**divisions,'o-');ax[1,0].set(xticks=divisions,xlabel=tr('理想对称分裂次数','Ideal symmetric divisions'),ylabel=tr('每个后代细胞的平均标记 / %','Mean label per descendant / %'),title=tr('C  脉冲后追踪中的标记稀释','C  Label dilution during a chase'))
    ax[1,1].bar([tr('条件甲','Condition A'),tr('条件乙','Condition B')],[200,100],label=tr('总核数','Total nuclei'),color='#b9d8e2');ax[1,1].bar([tr('条件甲','Condition A'),tr('条件乙','Condition B')],[60,40],label=tr('EdU 阳性核','EdU-positive nuclei'),color='#8160a1');ax[1,1].text(0,210,'30%',ha='center');ax[1,1].text(1,110,'40%',ha='center');ax[1,1].set(ylabel=tr('核数','Nuclei'),ylim=(0,270),title=tr('D  阳性比例与阳性数量同时阅读','D  Read positive fraction and count together'));ax[1,1].legend(fontsize=8);fig.tight_layout();save(fig,'pulse')
    fig,ax=plt.subplots(figsize=(8.2,12.5));ax.imshow(plt.imread(Path(__file__).with_name('ligasova2015-figure2.png')));ax.axis('off');ax.set_title(tr('真实实验：浓度、细胞身份与竞争底物改变掺入信号','Measured example: concentration and competing substrate affect labeling'),fontsize=11);fig.text(.5,.06,tr('Ligasová 等，2015，图 2，CC BY 4.0；均值±SEM。\nA 为 8 h，B 为 2 h 标记；见正文的信号定义。','Ligasová et al., 2015, Fig. 2, CC BY 4.0; mean ± SEM.\nA uses 8 h; B uses 2 h; signal definitions in text.'),ha='center',fontsize=9);save(fig,'published')
    summary={'cohort':{'total':n,'cycling':cycling,'any_incorporation':int(ideal_labeled.sum()),'ideal_detected':int(ideal_detected.sum()),'observed_detected':int(detected.sum()),'any_percent':float(ideal_labeled.mean()*100),'observed_percent':float(detected.mean()*100)},'geometry':{'two_hour_fraction':.75*(8+2)/24,'eight_hour_fraction':.75*(8+8)/24,'sixteen_hour_fraction':.75},'dilution':{'stock_10mM_to_5ml_20uM_ul':10.,'final_after_equal_mix_uM':10.},'chase':{'two_division_fraction':.25,'four_division_fraction':.0625},'comparison':{'a_fraction':.3,'b_fraction':.4,'a_positive':60,'b_positive':40}}
    assert ideal_labeled.sum()==150 and ideal_detected.sum()==142 and abs(pulse_overlap(np.array([6.,7.,8.,15.,16.]),2)-np.array([0.,1.,2.,1.,0.])).max()<1e-10
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();main(a.output,a.language)
```

The image arrays retain numerical background and noise, while the exported table records both the constructed incorporation signal and the measured signal. Comparing those columns reveals the effect of sampling a spatially blurred fluorescent object with a finite region. The measurement can be slightly lower than its central peak without implying that DNA synthesis changed. Because the construction is known, this example provides a controlled way to inspect how imaging and analysis sit between the biological model and the final classification.

First change the pulse from two hours to four and inspect both geometric coverage and detected fraction. Next hold the pulse fixed and raise the threshold, checking which weakly labeled nuclei leave the positive set. Then vary the fraction participating in the cycle and compare its effect with lengthening S phase. Keep total and positive counts together during every change. For experimental data, the same object-table and overlay checks can locate effects of segmentation, detachment, background, and boundary handling before a group comparison is interpreted biologically.

A useful interpretation identifies the culture stage and time window, the number of observed nuclei with detectable new-DNA label, the classification rule, and the relationship to total abundance and spatial distribution. A changed positive fraction can motivate measurements of cycle progression, subsequent population growth, or a specific function. Similar fractions with very different total counts instead direct attention to initial retention and later losses. EdU turns a broad question about cell growth into a set of time-resolved, object-defined questions that can be investigated in sequence.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L04.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Salic and Mitchison (2008): A chemical method for fast and sensitive detection of DNA synthesis in vivo](https://salic.med.harvard.edu/sites/salic.med.harvard.edu/files/publications/Salic_2008_Proc%20Natl%20Acad%20Sci%20U%20S%20A.pdf)

   Original incorporation/click-detection method, controls and chase examples.
2. [Thermo Fisher: Click-iT EdU Imaging Cell Proliferation Protocol](https://www.thermofisher.com/us/en/home/references/protocols/cell-and-tissue-analysis/protocols/click-it-edu-imaging-protocol.html)

   Ordering of labeling, fixation/permeabilization, detection and additional stains.
3. [Thermo Fisher: Click-iT Plus EdU Cell Proliferation Imaging Kits Protocol](https://www.thermofisher.com/us/en/home/references/protocols/cell-and-tissue-analysis/protocols/click-it-plus-edu-imaging-protocol.html)

   Formulation-specific copper detection and fluorescent-protein compatibility.
4. [Ligasová et al. (2015): A Fatal Combination: A Thymidylate Synthase Inhibitor with DNA Damaging Activity](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0117459)

   Cell-dependent incorporation, competing substrate and labeling conditions; Figure 2 reproduced intact.

   CC BY 4.0; Figure 2 reproduced intact with attribution and outer teaching title.
5. [ImageJ: Principles of Scientific Imaging](https://imagej.net/imaging/principles)

   Original pixel values, segmentation inspection and threshold methods.
