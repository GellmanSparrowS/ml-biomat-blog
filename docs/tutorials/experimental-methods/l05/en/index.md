# Immunofluorescence: Locating target proteins in cells

Source: https://ml-biomat.com/tutorials/experimental-methods/l05/en/
Language: en

Follow antibody recognition to nuclear localization, and investigate background, exposure and region selection.

## Before asking whether a cell is brighter, ask where its protein went

Cells grown on a soft gel and cells grown on stiff glass can look different. Some spread, some contract, and some redistribute proteins that regulate gene activity between the cytoplasm and the nucleus. An ordinary microscope reveals outlines but does not identify a particular protein. Immunofluorescence adds molecular identity to the image: an antibody recognizes a target, and a fluorescent label reports where that recognition occurred. The question can therefore become more precise: how does the distribution of this protein between two cellular compartments change? Location matters because a molecule encounters different partners and performs different work in different parts of a cell.

Think of a fluorescence image as a measurement table with addresses. Each pixel corresponds to a small region of the specimen, and its value records a detected signal. Green, blue, or magenta is a display choice that makes those values visible. Antibody recognition, fluorescence emission, light collection, and screen rendering are separate stages. More light can result from more target, but also from greater antibody access, longer exposure, or fluorescence from the material itself. A useful experiment therefore establishes both the identity of the signal and the conditions under which its numbers were recorded. Controls and calculations address different links in that same measurement chain.

Two complementary examples guide this chapter. A real Human Protein Atlas image shows the spatial pattern of vimentin and teaches us to read channel identities and cellular structures. A reproducible constructed image experiment keeps each cell's total target signal constant while changing its nuclear distribution. The real image supplies biological complexity; the constructed example supplies a known answer against which processing can be checked. Together they make background correction, region selection, and exposure effects tangible without requiring previous training in immunology or image programming.

Define the measurement before collecting the images. Nuclear enrichment suggests a comparison of nuclear and cytoplasmic mean intensities. Total signal per cell requires a complete cell boundary and integrated intensity. Formation of puncta calls for a definition of a punctum, including the spatial scale at which it is detected. These measurements respond differently to cell size. A larger cell with unchanged mean intensity has a greater integrated signal. A constant amount concentrated into a smaller compartment has greater local intensity. Deciding which change matters determines the masks, image channels, and numerical records that the experiment needs.

## How recognition becomes a visible address

An antibody is a protein with a binding surface that recognizes a particular part of its target, called an epitope. Imagine a shaped clip meeting a compatible surface. The analogy includes an important detail: the surface must be both compatible and accessible. An epitope may be a short sequence of adjacent amino acids or a surface assembled by protein folding. Fixation, unfolding, and association with other molecules can change its accessibility. An antibody that gives a useful result in one assay therefore needs evidence of performance in the preparation used for another assay. The name on the vial alone does not describe the complete measurement.

In 1941, Coons, Creech, and Jones investigated fluorescent antibody conjugates containing an anthryl group. Their experiments compared recognition of different pneumococcal types, linking fluorescence to a specific biological target. They also identified a practical obstacle: blue tissue autofluorescence could obscure their label. The historical problem was consequently twofold—attach a visible reporter while retaining recognition, then distinguish that reporter from its surroundings. Modern dye selection and background controls continue to address this same pair of questions. The diagram illustrates the recognition and reporting arrangement rather than reproducing the original chemistry.

![Original schematic of direct and indirect fluorescent labeling. Stars mark the reporters; their number is illustrative. The historical comparison connects antibody recognition, signal amplification and tissue background.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/29f5166cb3b53a2bbd507630.svg?v=29f5166cb3b5)

Figure 1Original schematic of direct and indirect fluorescent labeling. Stars mark the reporters; their number is illustrative. The historical comparison connects antibody recognition, signal amplification and tissue background.

In direct immunofluorescence, the target-binding primary antibody carries the fluorophore. In an indirect arrangement, an unlabeled primary antibody binds the target and a labeled secondary antibody recognizes that primary. For example, an appropriate anti-rabbit secondary recognizes rabbit immunoglobulin; the phrase does not specify the species from which the specimen was collected. Indirect detection allows different primary antibodies to share a reporting reagent and can place several labels near a target. It also introduces another binding step, making secondary-antibody binding and cross-reactivity relevant experimental variables.

A simple equilibrium model explains why increasing antibody concentration eventually yields diminishing gains. Suppose the binding sites are identical, free antibody is available in excess, and equilibrium has been reached. Increasing free concentration raises the fraction of occupied sites toward a plateau. At a concentration equal to the dissociation constant, half the sites are occupied. Real staining also involves access, diffusion, washing, and heterogeneous binding surfaces, so the model is a conceptual guide rather than a universal calibration. It explains why a tenfold increase in antibody can produce much less than a tenfold increase in useful signal.

$$
\theta=\frac{c}{K_d+c}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | Fraction of sites occupied, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | Equilibrium free antibody concentration, nM |
| ![Formula](https://ml-biomat.com/static/agent-math/b222289350e5e9dd7c2d84e7.svg) | Dissociation constant, nM |

For identical noncooperative equilibrium sites, balancing association and dissociation gives occupancy. Free concentration is known and probe depletion is negligible. With Kd = 2 nM, concentrations of 2 and 18 nM give fractions 0.5 and 0.9, as in the plot.

## Preserve the scene and provide a route to the target

Fixation aims to preserve the cellular arrangement present at sampling. It resembles taking a molecular snapshot, except that the process changes the specimen while preserving it. Crosslinking can retain structures and simultaneously conceal epitopes. Precipitating treatments alter proteins and membranes in another way. Evaluate both target staining and morphology when choosing conditions. A brightness comparison between two fixation procedures combines target detection with preparation effects. For an experimental comparison, matched fixation times and conditions help keep those contributions aligned between groups.

Permeabilization provides antibody access to intracellular structures. An antibody is large relative to many molecules that normally cross membranes, so an intracellular target requires an appropriate route through the specimen. Insufficient access can make the exterior appear strongly stained while deeper regions remain dim. Strong extraction can remove soluble components. A surface-target experiment may instead deliberately preserve membrane integrity. In a three-dimensional gel, the route also includes distance from the material surface. A depth gradient can therefore combine target distribution, probe access, and optical attenuation. Images at several depths help formulate which contribution to investigate next.

Blocking and washing manage binding that is not intended to remain in the final image. Blocking components occupy surfaces that might otherwise adsorb antibody; washing removes free and weakly retained material. This is especially relevant for charged, hydrophobic, or porous substrates. A material-only sample reveals substrate fluorescence, while a sample processed without primary antibody reveals signals remaining through the other parts of the staining pathway. These controls answer different questions even when both are called negative controls. Keeping their identities distinct makes a bright background easier to diagnose.

Dilution calculations connect a desired working concentration to a measurable volume. Suppose the stock contains 1 milligram per milliliter and the experiment requires 500 microliters at 2 micrograms per milliliter. The stock contributes one five-hundredth of the final volume: use 1 microliter and make the final volume 500 microliters. That means adding diluent to the stated final volume. If the required stock volume is too small to transfer reliably, prepare an intermediate dilution and apply the same conservation principle again. Recording stock concentration, final volume, and diluent composition makes the condition more reproducible than recording a dilution ratio alone.

$$
C_sV_s=C_wV_f,\qquad V_s=\frac{C_wV_f}{C_s}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/59e6f76fe7f807e8f04f82ec.svg) | Stock concentration, μg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/af24cfe08968b9a399cca9b4.svg) | Added stock volume, μL |
| ![Formula](https://ml-biomat.com/static/agent-math/e153ba9e5288ecd5c41453ef.svg) | Working concentration, μg/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/4d13c340035341c4ed1de3a2.svg) | Final total volume, μL |

Antibody mass is conserved. Matching volume units cancel their conversion factor. Preparing 500 μL at 2 μg/mL from 1000 μg/mL stock requires 1 μL stock, then diluent to final volume.

Handling time and specimen coverage also influence the result. Local drying concentrates solutes and can create bright edges. Different delays between staining and imaging expose samples to different storage and light histories. Sufficient liquid coverage, matched washing, and a consistent imaging order preserve the intended comparison. Cells that detach during processing deserve particular attention: the population remaining on a surface may differ from the starting population. Wide-field records before and after preparation help reveal whether a treatment preferentially removed weakly attached or damaged cells.

## Give each control a question to answer

A sharp image can arise from a well-localized target or from reproducible off-target binding. One way to investigate identity is to change the target itself and ask whether the corresponding spatial signal decreases. Another is to use an independent antibody recognizing a different epitope, or a separate detection method that does not rely on the same binding reagent. The choice depends on the specimen and question. The common principle is to add evidence linking the observed signal to the proposed target, rather than using visual clarity as a substitute for molecular identity.

A no-primary control addresses a different link. It shows what remains when secondary antibody, specimen, and imaging conditions are present without the primary antibody. A dark result indicates low signal through that pathway; it does not directly test whether the primary recognizes an unrelated protein. An unstained sample reveals specimen and material autofluorescence. A positive sample with an established detectable target helps check the complete staining and imaging chain. If every experimental sample is dim, the positive control helps distinguish a biological change from a detection problem.

Multicolor experiments require both optical and reagent compatibility. Emission from a strong fluorophore can enter another detection window, while two primary antibodies from the same host may be recognized by the same secondary. A single-label specimen investigates optical spillover. Controls designed around antibody hosts and binding partners investigate reagent cross-reactivity. These phenomena occur at different stages, so their solutions differ: excitation and detection settings address one, while antibody pairing, direct labeling, or specialized multiplex procedures address the other. Channel labels should name the biological objects as well as the display colors.

The real example below is from the Human Protein Atlas. It shows ASC52telo cells stained for vimentin, gene symbol VIM, using antibody HPA001762. Green reports the target, red marks microtubules, and blue marks nuclei. Look first at the target-only image and then at the merge. This makes the elongated, filament-like pattern around nuclear regions easier to distinguish from the equally conspicuous red reference structures. A striking color does not change its biological identity. Before computing a statistic, establish which channel corresponds to which object and describe their spatial relationship in ordinary words.

![Real ASC52telo immunofluorescence. Green: VIM; red: microtubules; blue: nuclei. Antibody HPA001762, image 582878. Human Protein Atlas v26, CC BY 4.0; original display images arranged with titles, without protein quantification from these display files.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/66d5f6ff401b5dc10f511ee1.svg?v=66d5f6ff401b)

Figure 2Real ASC52telo immunofluorescence. Green: VIM; red: microtubules; blue: nuclei. Antibody HPA001762, image 582878. Human Protein Atlas v26, CC BY 4.0; original display images arranged with titles, without protein quantification from these display files.

The subcellular atlas published in 2017 extended this type of observation to more than twelve thousand proteins, making localization a systematically searchable property. Here the public display images support structural interpretation. Quantitative exercises use the known pixel arrays below. A research intensity comparison benefits from detector values, bit depth, exposure information, and spatial calibration; a compressed display image carries presentation choices as well. Giving each image an explicit purpose allows us to learn from rich public morphology while organizing numerical measurements around the appropriate underlying data.

## From brightness to localization: correct the background and define the denominator

A nuclear-to-cytoplasmic comparison begins with regions. Nuclear staining helps define a nuclear boundary. A whole-cell boundary requires an appropriate outline marker, transmitted-light information, or a checked segmentation method. Cytoplasm is the cell region excluding the nucleus. A convenient ring around the nucleus can include a neighbor in crowded fields or omit long cellular extensions. If the target signal itself defines the region, dim cells may be selected differently from bright cells. Using an independent channel for geometry and then measuring the target channel reduces this coupling between selection and result.

Background subtraction follows directly from adding pixel values. If a region contains one hundred pixels and each carries twenty-five background units, its integrated signal includes twenty-five hundred background units. Subtract that amount from the integrated signal, or subtract twenty-five from the mean intensity. The nuclear-to-cytoplasmic ratio compares means so that region area is not directly inserted into the brightness comparison. For nuclear and cytoplasmic readings of 145 and 85 with a background of 25, the corrected signals are 120 and 60, giving a ratio of 2. The uncorrected ratio is about 1.71 because the shared offset pulls the values toward equality.

$$
F_{\rm corr}=F_{\rm sum}-n b,\qquad R_{N/C}=\frac{\overline I_N-b}{\overline I_C-b}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0339704ab48f75ba65258899.svg) | Background-corrected integrated region intensity, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/52a6793f1c59e6ada83931d9.svg) | Raw integrated region intensity, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Number of pixels in the region, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Mean background intensity per pixel, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/e43c47c5dbb086eb37f5d1ac.svg) | Nuclear-to-cytoplasmic mean intensity ratio, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/2b58c6da2c0388feb3f570fa.svg) | Raw mean nuclear intensity, a.u. |
| ![Formula](https://ml-biomat.com/static/agent-math/adf60fadcfb41b6537595116.svg) | Raw mean cytoplasmic intensity, a.u. |

Uniform background sums to n times its per-pixel value; the ratio compares corrected means. Assume common background, unsaturated data and positive corrected cytoplasmic signal. Values 145 and 85 with background 25 give (145−25)/(85−25)=2; the raw ratio is about 1.706.

This ratio describes enrichment, not the fraction of all protein located inside the nucleus. A fraction requires compartment sizes, the corresponding integrated signals, and an appropriate optical sampling model. A small bright nucleus can still contain less integrated signal than a large dim cytoplasmic region. Thickness changes also affect how much fluorescent material contributes to a pixel. For a three-dimensional distribution question, consistent volumetric acquisition and segmentation can support compartment totals. For a thin-cell localization comparison, a clearly defined ratio of regional means may answer the intended question more directly.

The constructed experiment assigns each cell a total target signal of ten thousand units. One group favors the cytoplasm and the other favors the nucleus. The program first creates independent geometric masks, distributes the fixed total between them, adds background and noise, and reads the resulting raw pixels back into regional measurements. Every plotted point corresponds to one constructed cell. The total-signal panel remains close to constant while the localization ratio changes. This separates redistribution from an increase in overall amount using an example whose underlying values are known.

![Simulated pixel experiment. Blue masks identify nuclei and orange masks identify cytoplasm. Each point represents one cell, showing how a similar total signal can accompany a different nuclear-to-cytoplasmic ratio. Spatial calibration is 1 μm/pixel.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/1c26b3a3596be1381374d066.svg?v=1c26b3a3596b)

Figure 3Simulated pixel experiment. Blue masks identify nuclei and orange masks identify cytoplasm. Each point represents one cell, showing how a similar total signal can accompany a different nuclear-to-cytoplasmic ratio. Spatial calibration is 1 μm/pixel.

Statistical summaries should preserve the experimental hierarchy. Many cells in one culture well share cultivation, staining, and imaging conditions. They describe the distribution within that well. Separately prepared samples or culture batches reveal how the result varies when the experiment is repeated. One useful presentation combines cell distributions with a summary for each independent sample, such as its median. Treating every cell as an independent treatment replicate increases the apparent sample size without increasing independent treatment events. Store cell, field, well, and batch identifiers so that later analysis retains those relationships.

Background estimates also have uncertainty. A single dark pixel is a poor representation of the offset under a whole cell. A representative cell-free region supplies many measurements, but a nearby material fiber or illumination gradient can make one region unrepresentative. Inspect several candidate background regions and consider whether a spatial correction is needed. When cytoplasmic signal approaches background, a small change in the estimated offset can greatly change the ratio. Displaying the underlying nuclear and cytoplasmic means alongside the ratio reveals this sensitivity and suggests whether more signal, better background control, or another endpoint would be useful.

## What comparable images require from the microscope

Exposure is the time window over which light is collected. Within a linear detector range, doubling it approximately doubles the recorded signal from a stable specimen. At the detector ceiling, stronger input is recorded as the same maximum value. Peaks flatten and ratios change. Consider nuclear and cytoplasmic signals of 120 and 60, a background of 25, and a maximum of 255. At twice the exposure, the nuclear value should be 290 but is clipped to 255, while the cytoplasm reaches 170. Subtracting the doubled background of 50 leaves 205 and 120, a ratio of about 1.71. A brighter-looking image has lost part of the original difference.

Matched exposure and saturation checks therefore belong together. Identical exposure can still saturate the brightest treatment group. Adjusting every image until it looks attractive changes the measurement scale between groups. A preliminary experiment can identify conditions covering the anticipated intensity range, after which acquisition settings remain fixed for the comparison. Display comparable images with a common intensity mapping and retain that range in the record. A separately enhanced structural view can help show morphology while the quantitative analysis continues to use preserved detector values.

The interactive experiment keeps nuclear and cytoplasmic target signals fixed while you change exposure, background, and the amount of cytoplasm accidentally included in the nuclear region. First increase background and compare corrected with uncorrected values. Next increase exposure until a bar reaches the detector ceiling; subtraction cannot recover the discarded peak. Finally enlarge the contaminated fraction of the nuclear region and observe the ratio decline. Acquisition, correction, and segmentation are different operations, yet each can appear in a final table as the same kind of ratio change.

## Why can one protein distribution produce different ratios?

True nuclear and cytoplasmic mean signals remain 120 and 60; the detector ceiling is 255. Change exposure, background and cytoplasmic contamination of the nuclear region to follow each stage of the measurement.

[Figure: Expected signals, recorded intensities and background in nucleus and cytoplasm](https://ml-biomat.com/tutorials/experimental-methods/l05/en/#L05-lab)

![Four diagnostics: binding occupancy, specific signal relative to background, exposure clipping and cytoplasmic contamination of nuclear masks. Curves use the stated teaching models.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/a71a66b06b3ef066ce98f00a.svg?v=a71a66b06b3e)

Figure 4Four diagnostics: binding occupancy, specific signal relative to background, exposure clipping and cytoplasmic contamination of nuclear masks. Curves use the stated teaching models.

When two proteins appear in overlapping colors, a related question is colocalization. Pair the values from the same pixel in two channels and ask whether they rise and fall together. Pearson correlation subtracts each channel's mean and compares their shared variation with their individual variation. If the second channel is always twice the first, the correlation is one even though their intensities differ. Spatial coexistence within an optical resolution element describes a spatial relationship. Investigating direct molecular binding requires an experimental design sensitive to shorter distances or to the interaction itself.

$$
r=\frac{\sum_{i=1}^{m}(x_i-\overline x)(y_i-\overline y)}{\sqrt{\sum_{i=1}^{m}(x_i-\overline x)^2\sum_{i=1}^{m}(y_i-\overline y)^2}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | Pearson correlation, dimensionless, between −1 and 1 |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Number of analyzed pixel pairs, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Pixel-pair index, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/0628201b1fcd40d880b250aa.svg) | Channel intensities at the same position, a.u. for each channel |
| ![Formula](https://ml-biomat.com/static/agent-math/8f4280576ddf56a5d99f652b.svg) | Channel means within the selected region, a.u. for each channel |

Centering isolates covariation; normalization uses each channel variation. Both channels require nonzero variance. For x = 1, 2, 3, 4 and y = 2, 4, 6, 8, numerator and denominator both equal 10, giving r=1. This describes pixel-intensity covariation, not a molecular fraction.

Empty image regions, neighboring-pixel dependence, channel misregistration, and three-dimensional geometry affect colocalization analysis. A large dark background gives many pairs of jointly low values. Structures separated along the optical axis may overlap in a projection. Select a region relevant to the question, inspect single-label controls and registration, and use volumetric data when the question requires it. A nuclear-translocation experiment may already be well described by a nuclear-to-cytoplasmic ratio. The availability of additional software outputs is not a reason to replace a direct endpoint with several less interpretable statistics.

The concentration plots add another practical comparison. The teaching model assigns a saturating specific signal and a background that rises with free antibody concentration. Their ratio can reach a useful range before the specific signal reaches its largest value. The location of that range depends on the assumed background model; it is not a recommended concentration for a real reagent. A dilution series on matched positive and background controls supplies the corresponding evidence for an actual specimen. Keeping acquisition conditions fixed makes that series informative about staining rather than about display adjustment.

## Run the complete example and carry its logic back to a specimen

The complete program exports four figure groups, a table of measurements for every constructed cell, an array archive containing raw pixels and region labels, and a numerical summary. Start with the localization distribution, then use a cell identifier in the table to locate the pixels that produced its ratio. Geometry is known directly in this example so that background correction and measurement remain transparent. In a real image those labels come from segmentation and need field-by-field inspection. Treating segmentation as a visible intermediate measurement makes defects easier to identify than hiding them behind a final average.

### Complete Python: Measuring localization from raw pixels

Runs offline and exports raw arrays, masks, a forty-cell table and four figure groups. Public atlas images are bundled.

```
"""Antibody binding, nuclear localization and image measurement: offline example."""
from pathlib import Path
import argparse,csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Ellipse,FancyArrowPatch
from PIL import Image

BLUE='#186e83';AMBER='#cd803f';PURPLE='#8160a1';GREEN='#3c8a6a'
def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text).replace('ASC52 telo', 'ASC52telo')


def response(exposure=1.,background=25.,contamination=0.):
    nucleus=(1-contamination)*120+contamination*60
    n=min(255,exposure*(nucleus+background));c=min(255,exposure*(60+background))
    return (n-exposure*background)/(c-exposure*background)

def main(output,language='zh'):
    out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh'
    def T(a,b):return a if zh else _label(b)
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5'})
    def save(fig,name):fig.savefig(out/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,5.2))
    for ax,indirect in zip(axes,[False,True]):
        ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off')
        ax.add_patch(Ellipse((5,1.8),3,1,fc=BLUE,ec='none'))
        ax.text(5,.8,T('靶蛋白与可及的表位','Target and accessible epitope'),ha='center')
        ax.plot([5,5,4,5,6],[2.3,3.8,4.8,3.8,4.8],color=AMBER,lw=5)
        if indirect:
            for x in [4.,6.]:
                ax.plot([x,x,x-.6,x,x+.6],[4.8,5.8,6.4,5.8,6.4],color=PURPLE,lw=4)
                ax.scatter([x-.6,x+.6],[6.4,6.4],s=100,marker='*',color=GREEN)
            ax.text(5,7.2,T('间接：一抗识别，带标二抗报告','Indirect: primary recognition, labeled secondary'),ha='center',fontsize=10)
        else:
            ax.scatter([4,6],[4.8,4.8],s=150,marker='*',color=GREEN)
            ax.text(5,6.8,T('直接：识别与发光位于同一抗体','Direct: recognition and label on one antibody'),ha='center',fontsize=10)
            ax.text(5,5.8,T('1941：Coons、Creech、Jones\n荧光化学与特异识别相遇','1941: Coons, Creech and Jones\nFluorescent chemistry meets specific recognition'),ha='center',fontsize=10)
    fig.text(.5,.015,T('原创原理示意；星号代表荧光团，数量不代表真实标记度。','Original mechanism schematic; stars are fluorophores, not measured labeling stoichiometry.'),ha='center',fontsize=9)
    save(fig,'history')
    # Constructed raw images: masks define geometry independently of protein intensity.
    rng=np.random.default_rng(505);yy,xx=np.mgrid[:220,:345]
    cells=np.zeros(xx.shape,int);nuclei=np.zeros(xx.shape,int);truth=np.zeros(xx.shape,float)
    rows=[]
    for i in range(40):
        cy=25+(i//8)*42;cx=25+(i%8)*42
        cell=(xx-cx)**2+(yy-cy)**2<=18**2;nuc=(xx-cx)**2+(yy-cy)**2<=8**2;cyto=cell&~nuc
        ratio=(.6 if i<20 else 2.)*np.exp(rng.normal(0,.12))
        total=10000.;c=total/(cyto.sum()+ratio*nuc.sum());n=c*ratio
        cells[cell]=i+1;nuclei[nuc]=i+1;truth[cyto]=c;truth[nuc]=n
        rows.append([i+1,'control' if i<20 else 'stimulated',ratio,total,int(nuc.sum()),int(cyto.sum())])
    raw=25+truth+rng.normal(0,.8,xx.shape);background=float(raw[cells==0].mean())
    result=[]
    for row in rows:
        i=row[0];nmask=nuclei==i;cmask=(cells==i)&~nmask
        n=raw[nmask].mean()-background;c=raw[cmask].mean()-background
        result.append(row+[float(n),float(c),float(n/c),float((raw[cells==i]-background).sum())])
    with (out/'localization.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['cell_id','group','true_NC_ratio','true_total_au','nuclear_pixels','cytoplasmic_pixels','nuclear_mean_au','cytoplasmic_mean_au','measured_NC_ratio','corrected_total_au']);w.writerows(result)
    np.savez_compressed(out/'images.npz',raw=raw,cell_masks=cells,nuclear_masks=nuclei,true_signal=truth)
    fig,ax=plt.subplots(2,2,figsize=(11,8.2))
    im=ax[0,0].imshow(raw,cmap='magma',vmin=25,vmax=55);ax[0,0].set_title(T('A  构造靶蛋白通道：原始数值','A  Constructed target channel: raw values'))
    ax[0,0].plot([20,70],[200,200],color='white',lw=3);ax[0,0].text(45,191,'50 μm',ha='center',color='white',fontsize=9)
    fig.colorbar(im,ax=ax[0,0],label=T('强度 / a.u.','Intensity / a.u.'),fraction=.035)
    masks=np.zeros((*raw.shape,3));masks[cells>0]=[.8,.5,.24];masks[nuclei>0]=[.18,.5,.65]
    ax[0,1].imshow(masks);ax[0,1].set_title(T('B  独立区域：核（蓝）与胞质（橙）','B  Independent masks: nucleus and cytoplasm'))
    for a in ax[0]:a.axis('off')
    ratios=np.array([r[-2] for r in result]);totals=np.array([r[-1] for r in result])
    for j,colour in enumerate([BLUE,AMBER]):
        indices=np.arange(j*20,(j+1)*20);jitter=np.linspace(-.15,.15,20)
        ax[1,0].scatter(j+jitter,ratios[indices],color=colour,alpha=.8)
        ax[1,1].scatter(j+jitter,totals[indices],color=colour,alpha=.8)
    for a in ax[1]:a.set_xticks([0,1],[T('对照','Control'),T('刺激','Stimulated')]);a.grid(axis='y',alpha=.2)
    ax[1,0].set(ylabel=T('核 / 胞质平均强度比','Nuclear / cytoplasmic mean ratio'),title=T('C  每个点是一枚构造细胞','C  Each point is one constructed cell'))
    ax[1,1].set(ylabel=T('扣背景积分强度 / a.u.','Background-corrected integrated intensity / a.u.'),title=T('D  总量相近，位置改变','D  Similar total, different location'),ylim=(9500,10500))
    fig.tight_layout();save(fig,'localization')
    fig,ax=plt.subplots(2,2,figsize=(11,8.2));c=np.geomspace(.05,100,200);bound=c/(2+c);background_curve=8+.8*c
    ax[0,0].semilogx(c,bound,color=BLUE);ax[0,0].set(xlabel=T('游离抗体浓度 / nM','Free antibody concentration / nM'),ylabel=T('结合占据率','Bound fraction'),title=T('A  单一位点平衡模型，Kd = 2 nM','A  One-site equilibrium model, Kd = 2 nM'))
    ax[0,1].semilogx(c,100*bound/background_curve,color=GREEN);ax[0,1].set(xlabel=T('抗体浓度 / nM','Antibody concentration / nM'),ylabel=T('特异信号 / 背景','Specific signal / background'),title=T('B  背景也随浓度上升的例子','B  Example with concentration-dependent background'))
    exposure=np.linspace(.2,4,200);ax[1,0].plot(exposure,[response(e) for e in exposure],color=AMBER);ax[1,0].axhline(2,color=BLUE,ls='--');ax[1,0].set(xlabel=T('曝光倍数','Exposure multiplier'),ylabel=T('测得核 / 胞质比','Measured N/C ratio'),title=T('C  饱和把真实比值 2 压向 1','C  Clipping compresses a true ratio of 2'))
    q=np.linspace(0,.5,100);ax[1,1].plot(q,[response(contamination=v) for v in q],color=PURPLE);ax[1,1].set(xlabel=T('核区域中混入的胞质比例','Cytoplasm fraction in nuclear region'),ylabel=T('测得核 / 胞质比','Measured N/C ratio'),title=T('D  区域边界也是测量条件','D  Region boundaries affect measurement'))
    for a in ax.flat:a.grid(alpha=.2)
    fig.tight_layout();save(fig,'diagnostics')
    here=Path(__file__).resolve().parent
    fig,ax=plt.subplots(1,2,figsize=(11,6.2))
    for a,name,title in zip(ax,['hpa-vim-asc.jpg','hpa-vim-asc-green.jpg'],[T('A  三通道合并','A  Three-channel merge'),T('B  靶蛋白 VIM：绿色通道','B  Target VIM: green channel')]):
        a.imshow(Image.open(here/name));a.axis('off');a.set_title(title)
    fig.text(.5,.06,T('ASC52telo；HPA001762；绿：VIM，红：微管，蓝：细胞核。\nHuman Protein Atlas v26，图像 582878；CC BY 4.0。','ASC52telo; HPA001762; green: VIM, red: microtubules, blue: nuclei.\nHuman Protein Atlas v26, image 582878; CC BY 4.0.'),ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.14,1,1]);save(fig,'published')
    assert response()==2 and response(4)==1
    assert np.isclose(response(2),205/120)
    summary={'binding':{'half':2/(2+2),'ninety_percent':18/(2+18)},'dilution':{'stock_ul':2*500/1000},'ratios':{'corrected':response(),'raw':145/85,'clipped_two':response(2),'clipped_four':response(4),'contamination_quarter':response(contamination=.25)},'constructed':{'cells':40,'estimated_background':background,'control_median':float(np.median(ratios[:20])),'stimulated_median':float(np.median(ratios[20:])),'mean_total':float(totals.mean())},'correlation':{'proportional':float(np.corrcoef([1,2,3,4],[2,4,6,8])[0,1])}}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

A useful first exercise changes nuclear allocation while keeping noise and total signal fixed. A second raises background and compares raw with corrected ratios. A third reduces the detector ceiling and examines where strong signals become distorted first. The binding and background plots explain why concentration optimization considers both useful signal and background. Public atlas images are bundled with the example, so running it requires no network access. They provide real morphology for interpretation, while the constructed arrays provide exact numerical checks.

There is also a useful exercise involving cell shape. Expand the cytoplasmic mask while retaining the same total target amount and nuclear allocation. The cytoplasmic mean will decrease because the same signal is distributed over more pixels. The nuclear-to-cytoplasmic ratio can rise even though the fraction of total signal inside the nucleus has not changed. This is an especially relevant distinction when a material changes cell spreading. Record area and compartment totals alongside the ratio, then decide which endpoint corresponds to the biological question. If the question concerns redistribution of molecules, a change caused entirely by geometric dilution deserves a different description from movement into the nucleus. If the question concerns local concentration available to binding partners, the change in regional mean may itself be useful. The same measurements can support both interpretations once geometry and signal allocation are made explicit.

For cells on a biomaterial, begin with a target and a localization question. Material-only controls identify substrate signals, staining controls investigate the detection pathway, and independently prepared cultures support biological comparison. Preliminary experiments select fixation, access conditions, antibody concentration, and acquisition range. The main comparison then preserves those conditions and retains full fields and individual channels. Presenting a localization image, a single-cell distribution, and independent-sample summaries together lets a reader follow the route from visible structure to measured values and then to the research question.

Finally, keep the physical scale attached to the analysis. The constructed image uses one micrometer per pixel, making its displayed scale bar a consequence of the specified geometry. The public atlas display is used without an invented scale bar. For new experiments, microscope calibration supplies the conversion from pixels to length, and the acquisition record supplies optical section spacing when volumes are measured. This small distinction becomes important when comparing punctum dimensions, distances to a nucleus, or structures across objectives. Numerical precision is useful when it remains connected to what the instrument actually sampled.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L05.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Coons, Creech & Jones (1941): Immunological Properties of an Antibody Containing a Fluorescent Group](https://www.ebm-journal.org/journals/experimental-biology-and-medicine/articles/10.3181/00379727-47-13084p/pdf)

   Early specific recognition and the tissue-autofluorescence problem.
2. [Abcam: Immunocytochemistry protocol](https://www.abcam.com/en-us/technical-resources/protocols/icc-protocol)

   Selecting fixation, epitope preservation and access conditions.
3. [Thermo Fisher: Application Verification Testing for Immunofluorescence](https://www.thermofisher.com/us/en/home/life-science/antibodies/antibodies-learning-center/antibodies-resource-library/antibody-application-testing-protocols/immunofluorescence-protocol-adherent-suspension-application-testing.html)

   Unstained and no-primary controls along the detection pathway.
4. [Uhlén et al. (2016): A proposal for validation of antibodies](https://pmc.ncbi.nlm.nih.gov/articles/PMC10335836/)

   Application-specific evidence for antibody identity.
5. [Human Protein Atlas v26: VIM subcellular localization](https://v26.proteinatlas.org/ENSG00000026025-VIM/subcellular)

   Actual ASC52telo morphology and channel identities; HPA001762, image 582878.

   CC BY 4.0; images credited to Human Protein Atlas
6. [Thul et al. (2017): A subcellular map of the human proteome](https://doi.org/10.1126/science.aal3321)

   Primary subcellular atlas publication; the scientific development of the atlas.
7. [ImageJ: Colocalization Analysis](https://imagej.net/imaging/colocalization-analysis)

   Correlation versus co-occurrence, image quality, regions and registration.
8. [Human Protein Atlas: Licence and citation](https://www.proteinatlas.org/about/licence)

   Image reuse terms and specific-image attribution.

   CC BY 4.0 for HPA copyrighted content, with stated third-party exceptions
