# Live/dead staining: Turning cell state into readable images

Source: https://ml-biomat.com/tutorials/experimental-methods/l03/en/
Language: en

Follow probe entry and retention through background, spillover, object classification and spatial interpretation in materials.

## What does a green image of cells actually tell us?

Cells are placed on a newly prepared hydrogel, and the following day many green objects appear in a fluorescence image. That is encouraging, but useful questions remain. How many cells do those objects represent? Are they evenly distributed? Do cells inside the material have the same appearance as those near the surface? Where are the red objects located? Live/dead staining turns selected physiological properties into signals that can be located in space. It connects cell state to surfaces, pores, and local environments, rather than reducing the whole material to one average reading. The spatial pattern can then guide the next experiment.

This chapter uses a common mammalian-cell combination, calcein AM and ethidium homodimer-1, abbreviated EthD-1. Intracellular esterases convert the first probe into a fluorescent product that can be retained by cells. The second mainly enters cells with compromised membrane integrity and becomes strongly fluorescent when associated with nucleic acids. Although the procedure is called live/dead staining, its measured properties are more specific: esterase activity, product retention, and membrane permeability. Defining those properties gives meaning to the colors, thresholds, and percentages. DNA replication, continued population growth, and specialized cellular functions can then be examined using measurements appropriate to those questions.

A common first impression is that brighter cells are healthier cells. Brightness also depends on probe loading, enzyme activity, cell volume, exposure settings, and imaging depth. Halving cell number or halving the average fluorescence per cell can both halve a whole-well green signal. Before collecting images, decide whether the main comparison concerns object-level classification, cells per unit area, spatial distribution, or total fluorescence. These quantities can support one another, but they retain different denominators and biological meanings. A clearly stated measurement allows the image to answer a focused question.

Images also preserve morphology. Cell spreading, aggregation, and proximity to a material crack can suggest a useful follow-up. A green population that becomes rounded may prompt examination of attachment and cytoskeletal organization. Red objects concentrated near the center of a scaffold may lead to checks of local supply, probe access, and imaging depth. Morphology and staining describe related aspects of state without needing to be compressed into one score. Let the spatial information help formulate a question, then choose an additional assay that addresses it.

## Let the cell perform part of the fluorescence reaction

A conventional dye colors an object directly, whereas a fluorogenic precursor makes a chemical conversion visible. In 1966, Boris Rotman and Ben Papermaster studied esters that yielded fluorescent products after enzymatic modification. Their work connected intracellular accumulation and retention of fluorescein with membrane integrity. The central idea was elegant: allow an accessible precursor to enter, let intracellular enzymes change its properties, and observe whether the resulting fluorescent material remains inside. The historical question concerned molecular entry and retention, providing a route to investigate cell state rather than a permanent label defining every future behavior of a cell.

![Entry, enzymatic conversion and retention connect to the 1966 fluorogenic-ester study. The right panel depicts modern permeability/nucleic-acid staining; these are explanatory diagrams, not historical reconstructions.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/39d874d90da5d4ca68ca2546.svg?v=39d874d90da5)

Figure 1Entry, enzymatic conversion and retention connect to the 1966 fluorogenic-ester study. The right panel depicts modern permeability/nucleic-acid staining; these are explanatory diagrams, not historical reconstructions.

Calcein AM follows this measurement logic. Acetoxymethyl groups facilitate entry of the precursor. Intracellular esterases remove the relevant groups, generating strongly green-fluorescent calcein, which crosses an intact membrane less readily. Imagine a package wearing a temporary entry coat: the coat is removed after entry, leaving contents that remain more easily inside the room. The analogy explains entry and retention, while the real behavior also depends on molecular charge, enzyme activity, transport, and exposure time. Green fluorescence therefore requires several conditions to work together. Its magnitude reflects both population abundance and the reaction state of individual cells.

EthD-1 provides a second measurement. An intact plasma membrane normally excludes the probe; increased permeability permits entry and association with nucleic acids, producing strong red fluorescence. Nucleic acids include DNA and RNA, with DNA storing genetic information, so signal often appears around nuclear regions. The red color belongs to the probe and detection channel, rather than an intrinsic color acquired by a dying cell. Other live/dead combinations use different molecules, entry mechanisms, and spectral bands. A familiar green-and-red display does not establish that their conditions or interpretation are interchangeable.

Two signals can place objects into four classes: green-only positive, red-only positive, double positive, and double negative. Positive means exceeding a defined decision criterion. Green-only objects are consistent with formation and retention of the esterase product while showing little red-probe entry. Red-only objects show increased permeability with low green signal. Double-positive objects can arise from changing biological state, retained product, overlapping objects, or optical spillover. Double-negative objects may have weak signal, insufficient labeling, depth attenuation, or a noncellular identity. Retaining all four classes and the original images helps distinguish those possibilities in subsequent analysis.

This conventional probe pair is observed within an appropriate live-sample staining interval. Fixation and permeabilization change the membrane property being measured and can redistribute noncovalently retained dyes. Applying the same assay after those treatments measures permeability partly created by preparation itself. Experiments requiring subsequent fixation can instead select a suitable validated fixable probe and interpret its own reaction mechanism. Connecting preparation order to the measured property explains why a successful staining step cannot simply be moved anywhere in another workflow.

## Prepare images that explain where the colors come from

When applying a probe to a new material, begin by examining the material without cells or dye. Polymers, crosslinking products, surface treatments, and medium components may produce autofluorescence. A material-only sample with dye then tests additional adsorption or accumulation in pores. These comparisons answer different questions: one measures existing optical background, while the other includes material–probe interactions. An empty glass background can miss both material-specific effects. Controls matching the actual scaffold are especially helpful when a bright feature follows fibers or pores rather than recognizable cell shapes.

Cell controls establish the staining response. Healthy untreated cells provide a common green-signal range, and an appropriately validated membrane-compromised control establishes that the red probe can enter and be detected. Single-stained controls reveal whether either probe contributes to the other detection channel. Controls should resemble experimental samples in cell identity, material, labeling interval, and acquisition settings because those conditions jointly determine background and response. Each control connects a particular observation to a possible source of signal. Planning those comparisons beforehand makes them useful for interpreting every subsequent image.

Three-dimensional materials introduce two journeys: the dye must reach a cell, and emitted light must reach the detector. Probe diffusion through a scaffold takes time, so internal cells may encounter different concentrations or exposure durations from surface cells. Absorption, scattering, and optical collection then affect the returning fluorescence. Weak green signal can reflect either journey as well as biological state. Comparing responses across depth, examining labeling-time dependence, and using suitable optical controls can separate these contributions. A clear surface image characterizes its observed region; information about the full scaffold requires an appropriate spatial sampling design.

Sample handling may also select which cells remain available for imaging. Membrane-compromised or weakly attached cells can enter the supernatant and be removed during liquid changes. An image acquired after washing then describes the retained population. If the question concerns the whole treated system, the design can include supernatant, attached cells, and a defined way to combine their observations. The denominator follows that collection strategy. This source of selection can strongly affect a final percentage even when the surviving image is sharp, well exposed, and correctly classified.

## The detector records numbers; color is a display choice

A fluorescence microscope excites a probe with selected wavelengths and collects emission through its optical filters. A detector converts the received light into pixel values, after which software assigns display colors. Here, the composite uses green and magenta to help distinguish the two channels. Changing that palette does not change the underlying signals. Preserve the original channels separately, together with exposure, gain, illumination, pixel size, and depth information. A composite is useful for spatial relationships, while separate channels retain the numerical information needed for processing and classification.

![Two raw constructed channels, composite and object-level signals. Pixel size is 1 μm; known central regions provide intensity measurements. All four classes are retained; dashed thresholds are 40 a.u.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/06ed8f773964b15e55e7ea7a.svg?v=06ed8f773964)

Figure 2Two raw constructed channels, composite and object-level signals. Pixel size is 1 μm; known central regions provide intensity measurements. All four classes are retained; dashed thresholds are 40 a.u.

Insufficient exposure can bury weak signal in noise, while excessive exposure may drive pixels to the detector maximum. Once saturated, stronger illumination produces the same recorded value. Dimming the displayed image afterward cannot restore those lost differences. For intensity comparisons, choose a common usable acquisition range using representative weak and strong samples, and examine the original pixel distributions. Automatically rescaling every image can improve visual appearance while disguising numerical differences. Display adjustments and quantitative processing should therefore remain separate operations, with calculations performed on preserved numerical data.

Background subtraction must match the region being measured. Suppose a cell region contains one hundred pixels with a summed intensity of twelve thousand units. Nearby cell-free background averages twenty units per pixel, contributing an estimated two thousand units over that region. The corrected integrated signal is ten thousand. Larger regions accumulate more background because more pixels contribute. If background varies across the image, a justified local estimate or flat-field correction may be appropriate. Comparing the original and corrected images helps reveal whether processing has removed genuine cellular structure along with background.

$$
F_{\mathrm{corr}}=\sum_{j=1}^{n_p} I_j-n_p\bar B,\qquad \bar I_{\mathrm{corr}}=\frac{F_{\mathrm{corr}}}{n_p}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e75ccac71f13631e1c7c90f9.svg) | Background-corrected integrated intensity in an object region, a.u. (arbitrary intensity units). |
| ![Formula](https://ml-biomat.com/static/agent-math/2182e4a63941864596054a3f.svg) | Raw intensity of pixel j, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | Pixel index, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/4773c6daf0d996bad65e1235.svg) | Number of pixels in the object region, dimensionless integer. |
| ![Formula](https://ml-biomat.com/static/agent-math/9744967524d2194c13c2ad4e.svg) | Mean background per pixel under matching acquisition conditions, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/a7fd434c3ba79d2fe36f71b7.svg) | Background-corrected mean pixel intensity in the region, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | Summation over pixels in the object region. |

For approximately uniform additive background, subtract mean background multiplied by pixel count. A 100-pixel region with total intensity 12000 and background 20 has corrected sum 10000 and corrected mean 100.

Optical spillover connects the two channels. Part of the green probe’s emission can pass through the red detection window, making a green cell appear in both channels. Single-stained controls estimate that contribution, allowing correction when detection is approximately linear and unsaturated. In a simple one-direction model, a corrected green signal of one hundred units and a spillover coefficient of 0.4 contribute forty units to the red channel. Adding a true red signal of five yields forty-five, potentially exceeding the red threshold. Subtracting the estimated green contribution distinguishes this optical effect from genuine double-positive labeling.

$$
G=G_{\mathrm{obs}}-B_G,\qquad R=R_{\mathrm{obs}}-B_R-\alpha G
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8602e0bdcf66b1b2ee9fa0fc.svg) | Mean corrected green and red signals after background subtraction and one-way spillover correction, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/9a32cfa1933f9b284de73c20.svg) | Observed mean green and red signals in the object region, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/50bcf82ce5fdf10817b8563e.svg) | Mean backgrounds in the corresponding channels, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | Green-to-red spillover coefficient, dimensionless, estimated from a single-stained control under the same settings. |

Assume linear unsaturated detection and negligible red-to-green spillover. Corrected green 100, true red 5 and α=0.4 produce background-subtracted observed red 45; subtracting 40 restores 5. Two-way spillover requires the corresponding two-channel model.

The complete example generates a teaching image with known construction parameters. It saves two raw channels containing background and noise, together with measurement regions around known object positions. Mean pixel values are extracted for each region, background is removed, and spillover is corrected to produce an object-level signal table. Positions are intentionally supplied so that signal processing can be examined separately. Real images require object localization through an appropriate nuclear marker, cell boundary, or inspected segmentation method. Separating localization from classification identifies whether a discrepancy begins with finding objects or with assigning their states.

## The denominator turns an image into a defined percentage

A broadly spread green cell covers more fluorescent area than a small rounded cell, yet each can represent one cell. Dividing green pixel area by combined red and green area therefore usually measures an area fraction, not a cell-number fraction. A question about cell proportions requires object-level identification before classification. Touching cells may be merged into one object, while fragments may split one biological object into several detections. Overlaying detected boundaries on the original channels makes these errors visible and connects the final table to recognizable structures.

The constructed example contains 120 localized objects. After correction and thresholding, 84 are green-only, 24 red-only, six double positive, and six double negative. Green-only objects constitute 70 percent of all objects, all red-positive objects constitute 25 percent, and double negatives contribute the remaining five percent. Restricting the denominator to the two single-positive classes gives 84 divided by 108, or approximately 77.8 percent. That value describes the green-only fraction among objects resolved into those two classes. It differs from the 70 percent fraction of all localized objects because twelve objects have been excluded from its denominator.

$$
N=N_{G}+N_{R}+N_{GR}+N_{0},\qquad p_G=\frac{N_G}{N},\qquad p_{R+}=\frac{N_R+N_{GR}}{N},\qquad p_{G\mid\mathrm{single}}=\frac{N_G}{N_G+N_R}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Total localized objects included in analysis, objects. |
| ![Formula](https://ml-biomat.com/static/agent-math/0356a29120b1d61c171a4944.svg) | Green-only positive count, objects. |
| ![Formula](https://ml-biomat.com/static/agent-math/682d716020f3a5d1a3665231.svg) | Red-only positive count, objects. |
| ![Formula](https://ml-biomat.com/static/agent-math/4e18d96696d9fb378aec36d4.svg) | Double-positive count, objects. |
| ![Formula](https://ml-biomat.com/static/agent-math/358eaab52fd29057e6b95399.svg) | Double-negative count, objects. |
| ![Formula](https://ml-biomat.com/static/agent-math/0d6a3f0d3a47869a3a5eb7ae.svg) | Green-only fraction of all objects, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/bc86242e9123e8782d45a318.svg) | Red-positive fraction of all objects, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/0489dadaffb1d9203979c6a0.svg) | Green-only fraction restricted to the two single-positive classes, dimensionless. |

Counts 84, 24, 6 and 6 sum to 120; p_G=70% and p_R+=25%. Restricting to single-positive classes gives 84/108=77.78%, so classification scope and excluded classes accompany that result. Each object belongs to exactly one of the four classes.

A threshold should not be adjusted image by image to obtain a preferred result. Negative controls, single-stained controls, background distributions, and representative samples can establish a decision procedure that is then applied consistently. Spatially variable backgrounds may require local segmentation information, but the chosen method and parameters still need verification. Examining results over a reasonable threshold range reveals whether the conclusion reflects well-separated populations or many objects crowded near a decision boundary. The sensitivity curve retains a fixed total-object denominator, making classification changes easier to interpret.

![Class counts, threshold sensitivity, constructed depth attenuation and alternative origins of total signal. A/B share denominator 120; C uses teaching parameters; D separates cell abundance from per-cell intensity.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d49ce6cfd549bb7d12f89f66.svg?v=d49ce6cfd549)

Figure 3Class counts, threshold sensitivity, constructed depth attenuation and alternative origins of total signal. A/B share denominator 120; C uses teaching parameters; D separates cell abundance from per-cell intensity.

Combining fields introduces another denominator decision. Suppose one field contains eighty green-only objects among one hundred total, while another contains five among ten. The unweighted average of the two percentages is 65 percent; pooling the counts gives 85 divided by 110, approximately 77.3 percent. The former summarizes field percentages equally, while the latter describes all observed objects together. Within a well, decide whether the target is the distribution across fields or the pooled sampled population. Across independently cultured wells or batches, retain the biological replication level rather than allowing many images from one well to replace independent preparations.

Read proportions alongside absolute abundance. Material A might retain ninety green-only and ten red-only cells, while material B retains nine and one. Both have a green fraction of ninety percent among those single-positive classes, yet their retained populations differ tenfold. A question about cell carrying capacity or retention can therefore include objects per unit area or volume, with the actual sampled area and depth specified. This paired description preserves a substantial population loss that an attractive percentage could otherwise conceal.

Small observed populations also produce more variable proportions. Preserve counts for each field and independent sample, then summarize them according to the design instead of reporting only a pooled percentage. Cells within one aggregate may share a local environment, so counting more members of that same aggregate provides different information from sampling additional locations or independent cultures. Distributing observations across regions helps describe both the overall response and local heterogeneity. A plot showing individual sample results can make that structure visible without implying that every detected cell is an independent experimental replicate.

## Why do double positives increase when the cells stay unchanged?

Four circles represent constructed groups with shared signals; numbers inside give object counts, totaling 120. Adjust one-way spillover and the common threshold, then toggle correction. These groups form a noiseless example; the complete Python exercise separately analyzes noisy pixel images.

[Figure: Green and red signals with counts in four object classes](https://ml-biomat.com/tutorials/experimental-methods/l03/en/#L03-lab)

Use the interactive signal plot to separate threshold decisions from spillover correction. Increasing the spillover coefficient moves objects upward in the observed red direction. A valid correction using the matching coefficient moves them back, while changing the threshold changes the classification boundary itself. These are distinct operations. The numerical example keeps population sizes fixed, making it possible to see a large apparent change in double-positive counts even though no biological state has changed. That is precisely the kind of discrepancy a single-stained control can help explain.

## Preserve depth and abundance when interpreting a material

Three-dimensional scaffold images can be examined by depth. A simplified attenuation model assumes that each additional equal thickness retains the same fraction of the remaining signal, producing exponential decay with depth. Even unchanged cells can therefore appear dimmer farther from the imaging surface. In the constructed example, effective attenuation coefficients are 0.006 per micrometer for green and 0.003 per micrometer for red. At a depth of two hundred micrometers, approximately thirty and fifty-five percent of their initial intensities remain. Unequal attenuation moves an otherwise identical cell to a different location in the two-signal plot.

$$
I(z)=I_0\exp(-\mu z),\qquad f(z)=\frac{I(z)}{I_0}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/51a5b62ee59924de23f8e7a8.svg) | Measured signal at depth z, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/6e4f2807ce72e4cab3957130.svg) | Reference signal at zero depth, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/9032cb23a878659e74b670d3.svg) | Observation depth, μm. |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | Effective attenuation coefficient in the simplified model, μm⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/64460da0d752153c52e1bd62.svg) | Natural exponential; its argument μz is dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/c2298a29bae4706e73396095.svg) | Fraction of reference signal retained, dimensionless. |

Equal added thickness multiplies remaining signal by the same fraction, giving exponential attenuation. This uniform effective model illustrates depth dependence. With μ=0.006 μm⁻¹ and z=200 μm, f=e⁻¹·²≈0.301; μ=0.003 gives f≈0.549.

A depth stack also creates a counting problem: one cell can appear in several neighboring optical sections. Adding the counts from every section would then count that same cell repeatedly. A three-dimensional object-connectivity procedure or a clearly defined spatial sampling method can address the problem. Maximum-intensity projections are useful for displaying structures, but can superimpose cells located at different depths. Three-dimensional counts, layer-specific fractions, and projected areas describe different objects. Select the representation that matches the question, rather than assuming that all stack summaries estimate the same quantity.

Spatial measurements require calibration as well. Micrometers per pixel depend on the objective, camera, and acquisition settings. Enlarging an image on a document page changes its displayed size, not that original relationship. A calibrated pixel size is needed to convert counts into area density or to compare depth with a scaffold dimension. A scale bar must remain attached to the image when resized. Copying a bar from a photograph acquired at another magnification can produce a visually plausible but incorrect physical interpretation.

Real microscopy combines illumination, emission collection, scattering, and instrument geometry, so this simplified relationship explains direction and scale rather than prescribing a universal correction. For an actual material, record object numbers and intensity by depth, inspect probe access, and evaluate optical depth response with suitable references. Independently brightening every optical section can make a presentation readable while hiding original differences between sections. Numerical comparisons should preserve the original scale, and figure descriptions should identify the sampled plane, depth range, and spatial calibration.

Time also changes observation. Repeated illumination can photobleach fluorescent molecules, and imaging itself may affect live-cell state. A fixed plate-reading order can give early and late samples different intervals between staining and acquisition. Interleaving or randomizing observation order, recording those intervals, reducing unnecessary illumination, and examining time dependence help organize these effects. Tracking the same cell over time additionally requires attention to its accumulated light and probe exposure. The recorded state belongs to an observation window, not to an object permanently labeled as unchanged.

A real experimental comparison illustrates why measurement levels should remain distinct. In 2022, Sazonova and colleagues compared metabolic readouts, calcein/EthD-1 signals, flow cytometry, and protein measurements. Their green signal was normalized to a control and measured whole-well fluorescence, rather than individual cells counted in images. A treatment suppressing a particular death process did not restore red and green readouts in the same way. Placing the signals side by side separates reduced cell death from recovery of population expansion. Additional measurements in the figure help investigate those different responses.

![Sazonova et al. (2022), Fig. 2, CC BY 4.0, reproduced in full. Panel a: MTS; b: whole-well dual-probe signals; c: flow classification; d: protein measurements. Original points and mean ± SD retained; a/c N=5, b N=6. Contr denotes control, Cis cisplatin, and Q-VD the caspase inhibitor used.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/c02a46c03a71cefbe5110544.svg?v=c02a46c03a71)

Figure 4Sazonova et al. (2022), Fig. 2, CC BY 4.0, reproduced in full. Panel a: MTS; b: whole-well dual-probe signals; c: flow classification; d: protein measurements. Original points and mean ± SD retained; a/c N=5, b N=6. Contr denotes control, Cis cisplatin, and Q-VD the caspase inhibitor used.

Begin reading panel b by comparing its green measurement on the left and red measurement on the right. Check group names and each vertical-axis definition before comparing changes. Each point is a repeat from the original study, and lines with whiskers show mean and standard deviation; both channels have six repeats. Panels a and c then add other measurements, each based on five repeats. Red values below average background reflect the study’s signal normalization and background reference, rather than a negative number of dead cells. Reading axis definitions makes a complex experimental figure accessible one comparison at a time.

## Make every classification traceable to the original image

The complete example exports raw channel arrays, object-region labels, an object-level signal table, and classification summaries. Fixed-seed background noise and variable cellular signals allow reproducible inspection of each step: which pixels belong to a region, how their mean is calculated, how much background is removed, how green spillover is subtracted from red, and where the result lies relative to the thresholds. Double-positive and double-negative classes are retained rather than silently discarded. The reproduced research figure provides a separate example of actual measurements, clearly distinguished from the constructed image exercise.

### Two-channel images, object signals and classification

Construct raw images with a fixed seed, measure pixel intensities from known regions, and export NPZ, CSV, four figures and classification summaries. The real research figure and license are bundled.

```
"""Constructed two-channel cell images: background, spillover and denominators."""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,FancyArrowPatch,Rectangle

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
    def save(fig,name):fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    rng=np.random.default_rng(303);classes=np.repeat(np.arange(4),[84,24,6,6]);rng.shuffle(classes)
    xy=np.array([(18+25*x,18+25*y) for y in range(10) for x in range(12)],float)+rng.uniform(-3,3,(120,2))
    green=np.choose(classes,[100,5,70,5])+rng.normal(0,4,120);red=np.choose(classes,[5,100,70,5])+rng.normal(0,3,120);alpha=.15;bg=np.array([25.,20.]);gobs=green+bg[0];robs=red+alpha*green+bg[1]
    gc=gobs-bg[0];rc=robs-bg[1]-alpha*gc;threshold=40.;gp=gc>=threshold;rp=rc>=threshold
    counts=np.array([np.sum(gp&~rp),np.sum(~gp&rp),np.sum(gp&rp),np.sum(~gp&~rp)]);assert list(counts)==[84,24,6,6]
    yy,xx=np.mgrid[:270,:320];G=np.full(xx.shape,bg[0]);R=np.full(xx.shape,bg[1]);labels=np.zeros(xx.shape,int)
    for i,((x,y),g,r) in enumerate(zip(xy,green,red)):
        kernel=np.exp(-((xx-x)**2+(yy-y)**2)/(2*4**2));G+=g*kernel;R+=(r+alpha*g)*kernel;labels[(xx-x)**2+(yy-y)**2<=2**2]=i+1
    G+=rng.normal(0,1.2,G.shape);R+=rng.normal(0,1.2,R.shape)
    np.savez_compressed(output/'constructed_channels.npz',green_raw=G,red_raw=R,roi_labels=labels,pixel_um=1.,class_truth=classes,centers_xy=xy)
    gobs=np.array([G[labels==i+1].mean() for i in range(120)]);robs=np.array([R[labels==i+1].mean() for i in range(120)])
    gc=gobs-bg[0];rc=robs-bg[1]-alpha*gc;gp=gc>=threshold;rp=rc>=threshold
    counts=np.array([np.sum(gp&~rp),np.sum(~gp&rp),np.sum(gp&rp),np.sum(~gp&~rp)]);assert list(counts)==[84,24,6,6]
    np.savetxt(output/'cell_signals.csv',np.column_stack([np.arange(1,121),classes,gobs,robs,gc,rc]),delimiter=',',header='id,constructed_class,green_observed_au,red_observed_au,green_corrected_au,red_unmixed_au',comments='')
    fig,ax=plt.subplots(1,2,figsize=(11.5,4.7))
    for a in ax:a.set(xlim=(0,10),ylim=(0,7));a.axis('off')
    a=ax[0];a.add_patch(Circle((6,3.5),2,facecolor='#d9eee5',edgecolor='#3c8a6a',lw=3));a.text(6,4.1,tr('胞内酯酶','Intracellular esterase'),ha='center');a.text(6,3,tr('发光产物保留','Fluorescent product retained'),ha='center',fontsize=10);a.text(1.7,4.7,tr('可进入的前体','Permeant precursor'),ha='center');a.add_patch(FancyArrowPatch((2.5,3.5),(5,3.5),arrowstyle='->',mutation_scale=18));a.set_title(tr('A  进入 → 转化 → 保留','A  Entry → conversion → retention'));a.text(5,.4,tr('1966：Rotman 与 Papermaster\n用荧光酯研究细胞膜与产物保留。','1966: Rotman and Papermaster\nconnect fluorogenic esters to membrane retention.'),ha='center',fontsize=10)
    a=ax[1];a.add_patch(Circle((6,3.5),2,facecolor='#f0e2ed',edgecolor='#8160a1',lw=3,ls='--'));a.add_patch(Circle((6,3.5),.8,facecolor='#cd803f',alpha=.6));a.text(6,3.5,tr('核酸','Nucleic acids'),ha='center');a.text(1.8,4.7,tr('膜受损后可进入','Entry after membrane damage'),ha='center',fontsize=10);a.add_patch(FancyArrowPatch((2.5,3.5),(5,3.5),arrowstyle='->',mutation_scale=18));a.set_title(tr('B  进入 → 核酸结合 → 发光','B  Entry → nucleic-acid binding → fluorescence'));a.text(5,.4,tr('现代双参数染色：\n酯酶活性与膜通透性分别提供信息。','Modern two-parameter staining:\nesterase activity and permeability provide distinct information.'),ha='center',fontsize=10);fig.tight_layout();save(fig,'mechanism')
    fig,ax=plt.subplots(2,2,figsize=(10.8,8));rgb=np.zeros((*G.shape,3));rgb[:,:,1]=np.clip((G-bg[0])/120,0,1);rgb[:,:,0]=np.clip((R-bg[1])/120,0,1);rgb[:,:,2]=rgb[:,:,0]*.65
    for a,im,title,cmap in [(ax[0,0],G,tr('A  原始绿色通道','A  Raw green channel'),'viridis'),(ax[0,1],R,tr('B  原始红色通道','B  Raw red channel'),'magma')]:
        image=a.imshow(im,cmap=cmap,vmin=0,vmax=160,origin='lower',extent=[0,320,0,270]);fig.colorbar(image,ax=a,label=tr('强度 / a.u.','Intensity / a.u.'));a.set_title(title);a.set(xlabel='x / μm',ylabel='y / μm')
    a=ax[1,0];a.imshow(rgb,origin='lower',extent=[0,320,0,270]);a.plot([240,290],[22,22],color='white',lw=3);a.text(265,32,'50 μm',color='white',ha='center',fontsize=9);a.set_title(tr('C  合并显示；紫红色帮助区分通道','C  Composite; magenta distinguishes the red channel'));a.set(xlabel='x / μm',ylabel='y / μm')
    a=ax[1,1];palette=['#3c8a6a','#cd803f','#8160a1','#7c8990'];
    for k,name in enumerate([tr('绿单阳','Green only'),tr('红单阳','Red only'),tr('双阳','Double positive'),tr('双阴','Double negative')]):a.scatter(gc[classes==k],rc[classes==k],s=23,color=palette[k],label=name)
    a.axvline(40,c='#89989d',ls='--');a.axhline(40,c='#89989d',ls='--');a.set(xlabel=tr('扣背景绿色 / a.u.','Background-corrected green / a.u.'),ylabel=tr('校正串色红色 / a.u.','Unmixed red / a.u.'),title=tr('D  每个对象保留两个信号','D  Retain both signals per object'));a.legend(fontsize=8);fig.suptitle(tr('构造的双通道教学图像；从已知对象区域提取像素均值','Constructed two-channel images; mean pixel signals extracted from known object regions'),fontsize=11);fig.tight_layout();save(fig,'channels')
    fig,ax=plt.subplots(2,2,figsize=(11.4,7.5));names=[tr('绿单阳','Green only'),tr('红单阳','Red only'),tr('双阳','Double +'),tr('双阴','Double −')];ax[0,0].bar(names,counts,color=palette);ax[0,0].set(ylabel=tr('对象数','Object count'),title=tr('A  保留四类与共同分母 120','A  Preserve four classes and denominator 120'))
    thresholds=np.linspace(20,115,96);single=[np.sum((gc>=q)&~rp)/120*100 for q in thresholds];ax[0,1].plot(thresholds,single);ax[0,1].axvline(40,c='#cd803f',ls='--');ax[0,1].set(xlabel=tr('绿色阈值 / a.u.','Green threshold / a.u.'),ylabel=tr('绿单阳占全部对象 / %','Green-only fraction of all objects / %'),title=tr('B  阈值敏感性保留分母','B  Threshold sensitivity with fixed denominator'))
    z=np.linspace(0,400,201);ax[1,0].plot(z,100*np.exp(-.006*z),label=tr('绿色 μ=0.006 μm⁻¹','Green μ=0.006 μm⁻¹'));ax[1,0].plot(z,100*np.exp(-.003*z),label=tr('红色 μ=0.003 μm⁻¹','Red μ=0.003 μm⁻¹'));ax[1,0].set(xlabel=tr('深度 / μm','Depth / μm'),ylabel=tr('保留强度 / %','Retained intensity / %'),title=tr('C  构造的深度衰减','C  Constructed depth attenuation'));ax[1,0].legend(fontsize=8)
    ax[1,1].bar([tr('100 个 × 100','100 cells × 100'),tr('100 个 × 50','100 cells × 50'),tr('50 个 × 100','50 cells × 100')],[10000,5000,5000],color=['#186e83','#cd803f','#8160a1']);ax[1,1].set(ylabel=tr('总荧光 / a.u.','Total fluorescence / a.u.'),title=tr('D  一样的总强度有不同原因','D  Equal total intensity can have different causes'));fig.tight_layout();save(fig,'diagnostics')
    fig,ax=plt.subplots(figsize=(9.2,10.5));ax.imshow(plt.imread(Path(__file__).with_name('sazonova2022-figure2.jpg')));ax.axis('off');ax.set_title(tr('真实实验：信号降低可以包含增殖停滞与细胞死亡','Measured example: reduced signal can combine growth arrest and death'),fontsize=12);fig.text(.5,.03,tr('Sazonova 等，2022，图 2，CC BY 4.0。完整原图；a、c 为 N=5，b 为 N=6，均值±标准差。','Sazonova et al., 2022, Fig. 2, CC BY 4.0. Complete original; a,c N=5; b N=6; mean ± SD.'),ha='center',fontsize=9);save(fig,'published')
    summary={'classification':{'green_only':84,'red_only':24,'double_positive':6,'double_negative':6,'total':120,'green_only_all_percent':70.,'red_positive_all_percent':25.,'resolved_viability_percent':84/108*100},'background':{'corrected_sum_example':12000-100*20},'spillover':{'green':100.,'red_true':5.,'red_measured_at_04':45.,'red_unmixed_at_04':5.},'depth':{'green_200_fraction':float(np.exp(-1.2)),'red_200_fraction':float(np.exp(-.6))},'pooling':{'pooled_percent':85/110*100,'equal_field_average_percent':65.},'sampling':{'ideal_se_fraction':float(np.sqrt(.7*.3/120))}}
    assert sum(counts)==120 and abs(rc+alpha*gc+bg[1]-robs).max()<1e-10 and 84/120==.7
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();main(a.output,a.language)
```

The saved arrays retain their numerical scale, so a new display palette can be tested without changing measured values or reclassifying the cells.

For the constructed example, one pixel corresponds to one micrometer, and the measurement labels identify small central regions of each object. Those regions provide an intensity estimate; they are not intended to estimate the full area of a spread cell. The distinction explains why a region suitable for fluorescence classification need not be suitable for measuring cell size. In an experimental workflow, the same object may legitimately have separate nuclear, cytoplasmic, and whole-cell regions, provided each exported quantity records which region generated it.

First raise the green threshold and identify the objects whose classifications change earliest. Next increase green-to-red spillover and compare corrected and uncorrected double-positive counts. If the image background changes but the old background estimate is retained, the population shifts in signal space. If only the display palette changes, the numerical classification should remain unchanged. Varying one condition at a time separates an altered appearance from a changed measurement or decision rule. For experimental images, preserving channels, boundaries, and analysis settings provides the same route for later inspection.

A clear live/dead result identifies the cells, material, time point, probes, classification procedure, sampled spatial regions, and count denominator. The next experiment follows the question that remains. DNA-synthesis measurements or longitudinal counts examine whether the green population is expanding. Cytoskeletal and attachment measurements investigate rounded morphology. Molecular markers and time-resolved observations help study a death process. In this way, staining becomes a located, countable part of a research argument, with each image contributing information about where a biological response occurs and what property has actually changed.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L03.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Rotman and Papermaster (1966): Membrane properties of living mammalian cells as studied by enzymatic hydrolysis of fluorogenic esters](https://doi.org/10.1073/pnas.55.1.134)

   Original historical work on fluorogenic precursors, enzymatic conversion and membrane retention; the development of the original method.
2. [Thermo Fisher: Molecular Probes Handbook, Section 15.3](https://www.thermofisher.com/us/en/home/references/molecular-probes-the-handbook/assays-for-cell-viability-proliferation-and-function/viability-and-cytotoxicity-assay-kits-for-diverse-cell-types.html)

   Mechanisms and sample scope of calcein AM and EthD-1.
3. [Thermo Fisher: LIVE/DEAD Viability/Cytotoxicity Kit for mammalian cells protocol](https://www.thermofisher.com/us/en/home/references/protocols/cell-and-tissue-analysis/protocols/live-dead-viability-cytotoxicity-kit-for-mammalian-cells.html)

   Probe-specific timing, background and fixation compatibility.
4. [ImageJ: Principles of Scientific Imaging](https://imagej.net/imaging/principles)

   Pixel data, original-image preservation, illumination and threshold segmentation.
5. [Sazonova et al. (2022): Drug toxicity assessment: cell proliferation versus cell death](https://pmc.ncbi.nlm.nih.gov/articles/PMC9568594/)

   Real Figure 2 and methods comparing bulk signals, cell state and population change.

   CC BY 4.0; Figure 2 reproduced intact with attribution and added outer teaching title.
