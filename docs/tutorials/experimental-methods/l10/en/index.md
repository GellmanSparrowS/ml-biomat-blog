# Scratch and Transwell assays: How cells move and cross barriers

Source: https://ml-biomat.com/tutorials/experimental-methods/l10/en/
Language: en

Connect gap area, cell trajectories, gradients and membrane counts to distinguish movement, spreading and division.

## When a gap narrows, what have the cells actually done?

After skin is injured, surrounding cells rearrange, move and divide as the exposed region becomes covered. A researcher studying a dressing or material surface may similarly ask whether it supports cells entering an empty region. Leave a gap in a confluent cell layer and record it through time: the microscope reveals how the opposing edges approach. This scratch or wound-healing assay supports several questions. How fast does the edge advance? Do cells remain connected, or do isolated cells enter first? When do spreading and division occur relative to movement?

A different question asks whether cells can cross a barrier. Immune cells may move toward a soluble cue, or cells may pass through a matrix layer. A Transwell places cells and a test environment on opposite sides of a porous membrane, then counts cells that cross. The geometry resembles replacing an open road with a partition containing doorways. Cells must move, encounter a pore, pass through it and remain in the compartment being counted. This endpoint complements planar gap closure because it includes different spatial constraints and recovery steps.

Breaking migration into observable behavior makes both assays easier to understand. A cell extends its front, forms adhesions, pulls its body forward and releases attachments behind it. The cytoskeleton and adhesive structures continually reorganize, while neighboring cells, matrix organization and soluble cues influence movement. Covered area reflects these movements together with changes in cell shape and number. We therefore retain three observation levels: gap geometry, individual trajectories and cross-membrane counts. Each number then has a defined question to answer.

The complete example segments constructed image pixels, calculates closure, tracks two populations with the same speed but different directional distributions, and examines the denominator in a Transwell result. An openly licensed published figure adds actual edge, morphology and division phenotypes. Known geometric and motion conditions make the constructed calculations independently checkable. The aim is to turn an image that appears to close better into a result with explicit time, space, sample and behavioral definitions.

## Putting movement into a comparable geometry

In 1962, Boyden described a device for investigating how soluble substances attract leukocytes. A filter membrane separated two compartments, with cells on one side and a test solution on the other. The geometry connected the chemical environment with cells crossing a membrane and made different solutions comparable. The original experiments also varied antibody, antigen and serum combinations to investigate what generated the attractive activity. The historical lesson is experimental decomposition: a visible accumulation of moving cells becomes a set of testable conditions.

Modern culture inserts retain the two-compartment relationship while offering different membranes, pores and readouts. An uncoated membrane examines migration through pores. An added extracellular-matrix layer includes the ability to negotiate that layer as well. Extracellular matrix comprises surrounding material that supplies support, adhesion sites and signals; an experimental coating introduces selected aspects of that environment. Its composition, thickness, batch and pore geometry describe the obstacle encountered by the cells and belong with the result.

![Original diagrams of a planar cell layer and a modern membrane insert. The right panel connects Boyden’s 1962 two-compartment experiment with the present-day use of a concentration difference across a membrane.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/58786b1266c83db59b6a1664.svg?v=58786b1266c8)

Figure 1Original diagrams of a planar cell layer and a modern membrane insert. The right panel connects Boyden’s 1962 two-compartment experiment with the present-day use of a concentration difference across a membrane.

The planar scratch assay fixes another geometry: a previously connected cell layer acquires open space. Edge cells gain a free boundary, and neighboring cells can change arrangement and division. In 2004, Yarrow and colleagues adapted the assay to multiwell plates and compared what different imaging methods reveal. Their actual images include closure, reduced migration, altered morphology and increased mitotic cells. The experiment's expansion to larger screens retained a central interpretive problem: a picture contains more biological information than a single gap-width value.

How the gap is created affects its starting state. Mechanical scratching removes cells but can also disturb the underlying coating and leave debris. A removable barrier exposes a preformed region after cells have grown around it, reducing scraping-related changes. Equal initial widths do not make these edge conditions identical. For a material-surface study, inspect whether scratching also removes the material being tested. The cells may otherwise enter exposed substrate instead of the intended coating. Preserve the initial image and surface information alongside the subsequent closure curve.

## From pixels to closure, with the denominator made visible

The first image-analysis task is usually to identify the region still uncovered by cells. A binary mask assigns each pixel to gap or non-gap. Counting gap pixels and multiplying by the physical area represented by each gives a measured area. The calibration is squared: a pixel edge of 2 micrometers represents 4 square micrometers, not 2. The camera and objective combination determines this spatial scale; enlarging an image on a screen does not change the original physical size represented by its pixels.

$$
A=n_p s_xs_y
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Segmented gap area, μm² |
| ![Formula](https://ml-biomat.com/static/agent-math/4773c6daf0d996bad65e1235.svg) | Number of gap pixels, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/45e9f2faccf8bb8a3297984f.svg) | Pixel edge lengths in x and y, μm |

Pixel area is the product of its edge lengths. With 60000 pixels and 2 μm along each edge, total area is 240000 μm². Use acquisition-specific calibration; pixels are square in this example.

Each field supplies its own initial gap area, against which later remaining areas are compared. An initial 240000 square micrometers and a remaining 96000 after 24 hours give 144000 covered, or 60% closure. This percentage normalizes the area scale but does not remove every effect of starting geometry. Gaps 200 and 800 micrometers wide close by different percentages over the same time even when their edges advance at identical speeds. Retaining initial area and width distributions lets those geometric differences remain visible in the interpretation.

$$
C(t)=100\%\,\frac{A_0-A(t)}{A_0}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c4e857df82e09ece3691e350.svg) | Gap closure at time t, % |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time since initial image, h |
| ![Formula](https://ml-biomat.com/static/agent-math/0c430ee48d22be2e69d0f3ad.svg) | Initial gap area in the same field, μm² |
| ![Formula](https://ml-biomat.com/static/agent-math/fb60620bc9b2f7378081e24b.svg) | Remaining gap area at time t, μm² |

Subtract the remaining area and divide by the initial area of that field. (240000−96000)/240000 gives 60%. Initial and later images must share a field and consistent gap definition.

For an approximately long rectangular gap with similar inward movement from both sides, width change estimates an average one-edge speed. Division by two accounts for the two contributing boundaries. A width decrease from 400 to 160 micrometers over 24 hours means 240 micrometers of combined advance, or 120 per edge, giving 5 micrometers per hour. This describes a cell-layer boundary. An individual cell can turn, pause or move parallel to that boundary, so its trajectory speed is a separate measured quantity.

$$
v_{\rm edge}=\frac{w_0-w_t}{2t}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/457582f1a6cb86d77424cc8c.svg) | Mean one-edge advance speed, μm/h |
| ![Formula](https://ml-biomat.com/static/agent-math/9aa2b69e898db5e9d56207e0.svg) | Initial mean gap width, μm |
| ![Formula](https://ml-biomat.com/static/agent-math/49296f174f7d0afdfa8fd6c8.svg) | Mean gap width at time t, μm |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Observation duration, h |

For approximately parallel, similarly advancing boundaries, each side contributes half the narrowing. Width 400 to 160 μm over 24 h gives 240/(2×24)=5 μm/h. Boundary speed and individual path speed are distinct quantities.

Real scratches are often curved and irregular. Local widths sampled along the gap or area within a fixed field provide different summaries. A long thin protrusion can strongly affect the narrowest local width while occupying little area. Isolated cells can enter the center without forming continuous coverage. Show how the mask handles protrusions, isolated cells and debris, then apply that definition consistently across conditions and times. A visible contour overlay connects the algorithm's numerical choice to the biological object being measured.

![Simulated images and segmented gap contours with a pixel size of 2 μm. The lower panels compare the known geometry, the effect of starting width and sensitivity to the segmentation threshold.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/3fa35962a8ee38c851042eac.svg?v=3fa35962a8ee)

Figure 2Simulated images and segmented gap contours with a pixel size of 2 μm. The lower panels compare the known geometry, the effect of starting width and sensitivity to the segmentation threshold.

The constructed field has 2 micrometers per pixel, a height of 600 micrometers and an initial mean gap width of 400 micrometers. Both boundaries move at 5 micrometers per hour. The program smooths textured noisy images, segments the gap and retains the largest connected gap region. It exports the contour overlays and closure curve, then varies the intensity threshold to examine boundary sensitivity. If a small measured group difference changes direction under reasonable boundary choices, inspect segmentation and imaging conditions before treating additional decimal places as additional evidence.

## The same sixty-percent closure can contain different processes

Several processes reduce uncovered area. Existing cells can migrate inward, cell bodies can spread over larger footprints, and division can increase the number of cells contributing coverage. Record nuclear positions, cell contours and division events within the same sequence to investigate those contributions. Nuclear positions help track body movement, outlines show spreading, and division events add cell-number information. Their combination explains how similar closure curves can arise from different cellular behavior.

The observation window matters as well. A shorter interval can make the movement of starting cells easier to follow; a longer interval accumulates division, death and detachment. A short duration does not automatically eliminate proliferation, which depends on the cells and conditions. Reducing serum or applying an antiproliferative treatment changes the environment and can also affect movement, adhesion and survival. Relevant controls therefore record those behaviors alongside closure. Cell counts, proliferation measurements and time-lapse observations connect the attempted control of one process to its actual effects.

Starting density introduces another distinction. Layers with different densities contain different numbers of available edge cells and different contact and nutrient conditions. A material's adhesion efficiency can establish such a difference before the scratch is made. Confirm initial confluence and viable cell input to distinguish an effect on retaining cells at a surface from an effect on moving them. Confluence describes coverage, rather than proving that all cells share the same physiological state. The time-zero image records this starting relationship directly.

## Interactive experiment: Same closure, different movement

Adjust initial width, time, existing-cell movement and extra coverage-front speed. Their sum advances the gap boundary; arrows follow only original-cell movement. Extra coverage is a schematic spreading/additional-coverage velocity, not a cell-division rate.

[Figure: Gap geometry, cell movement and closure curve](https://ml-biomat.com/tutorials/experimental-methods/l10/en/#L10-lab)

The interactive geometry separates one-edge advancement into movement of existing cells and an additional contribution from spreading or newly supplied coverage. Both have units of micrometers per hour and their sum determines gap narrowing. Arrows attached to the starting cells depend only on the movement contribution. Changing 5 plus 0 to 2 plus 3 preserves 60% closure after 24 hours but shortens those arrows. The additional-coverage parameter is a schematic front velocity, not a cell-division rate. Its purpose is to show which extra observation would distinguish identical area results.

## Crossing a membrane: cues, pores and counting locations

In a Transwell, an upper compartment receives a specified cell input and a lower compartment receives the test solution. Soluble molecules exchange through a porous membrane. A concentration gradient means that concentration depends on position, potentially biasing cell movement. A higher lower-compartment concentration at setup does not establish a constant gradient throughout the experiment. Diffusion redistributes molecules, cells consume or release them, and membranes or coatings can adsorb them. Compartment volumes, exchange geometry, molecular properties and duration together determine the environment encountered by cells.

The exchange illustration simplifies this to two well-mixed liquid compartments. The upper 0.1 milliliters initially contains no cue, while the lower 0.6 milliliters contains 10 nanograms per milliliter, giving 6 nanograms total. Exchange brings both concentrations toward total mass divided by total volume, approximately 8.571 nanograms per milliliter. The program exports both concentrations and checks that total mass remains 6 nanograms. These volume-averaged curves explain why a gradient evolves. Local concentrations near an actual membrane depend on its geometry and transport properties and can be investigated with corresponding tracer measurements or models.

If a lower-compartment cue increases the number of crossing cells, compare additional conditions: no cue on either side, equal cue concentrations on both sides, lower-only cue and upper-only cue. A uniform cue can increase motility without supplying the same directional gradient. Directional bias in response to a chemical gradient is chemotaxis; a change in nondirectional motility is commonly called chemokinesis. These arrangements help separate directional effects from changes in general activity. Cells can also respond to surface-bound ligand patterns, which call for a separately defined surface-cue experiment.

The exchange conductance g converts a concentration difference into mass transferred per unit time. One compartment gains the mass that the other loses. The same transferred mass changes concentration more strongly in the smaller volume, which explains why both compartment volumes enter the rate at which their difference declines. With g equal to 0.02 milliliters per hour, the model gives a remaining difference of about 4.966 nanograms per milliliter after three hours. This parameter belongs to the constructed illustration; an actual membrane requires an experimentally established transport relationship.

$$
\Delta c(t)=\Delta c_0\exp\!\left[-g\left(\frac{1}{V_u}+\frac{1}{V_l}\right)t\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6f8ef384ada27708b9205032.svg) | Lower-minus-upper volume-averaged concentration difference, ng/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/d3f36c525113c3e9bd33a306.svg) | Initial concentration difference, ng/mL |
| ![Formula](https://ml-biomat.com/static/agent-math/439e3cc8d431c550923e0870.svg) | Intercompartment exchange conductance, mL/h |
| ![Formula](https://ml-biomat.com/static/agent-math/424f1a1571bd30409c6a3740.svg) | Upper and lower compartment volumes, mL |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Exchange time, h |

Assume well-mixed compartments of constant volume, no external production or loss, and an exchange rate proportional to the concentration difference. Opposing changes in the two compartments produce exponential decay of that difference. With conductance 0.02 mL/h, volumes 0.1 and 0.6 mL, and an initial difference of 10 ng/mL, the difference after 3 h is 10 exp(−0.7), or approximately 4.966 ng/mL. The exponent is dimensionless.

![Constructed compartment-mean concentrations and passage counts. Each point is an independent insert; orange bars are means of 3 counts. All conditions start with 50000 viable cells.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/5bb2e197c99af0fbee465657.svg?v=5bb2e197c99a)

Figure 3Constructed compartment-mean concentrations and passage counts. Each point is an independent insert; orange bars are means of 3 counts. All conditions start with 50000 viable cells.

Pore size participates in the selection. Very small pores can make cell and nuclear deformation the dominant obstacle; large pores can introduce settling and passive passage. Excess input can block pores or form a crowded layer. Establish useful ranges of cell number, duration and pore size for the actual system. Bubbles beneath the membrane, liquid-level differences and inconsistent volumes can alter contact and flow. For coated materials, verify coverage and uniformity so local coating gaps are distinguished from passage through the intended matrix.

An endpoint count must state where cells are collected. Adherent cells can remain on the membrane underside after crossing, while nonadherent cells may enter the lower liquid. Counting either location describes recovery at that location. If 600 cells cross from 50000 viable input cells, the input-normalized percentage is 1.2%. Comparing 180 cells through a coated membrane with 600 through a matched uncoated membrane gives 30%. That second percentage expresses coated passage relative to baseline migration. The different denominators answer different questions even though both are percentages.

$$
P_{\rm input}=100\%\frac{N_{\rm crossed}}{N_{\rm input}},\qquad P_{\rm coating}=100\%\frac{\overline N_{\rm coated}}{\overline N_{\rm uncoated}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/455d2073f7b2c579e45d7588.svg) | Crossed-cell fraction relative to viable input, % |
| ![Formula](https://ml-biomat.com/static/agent-math/88d4394861a8d67deaa914e2.svg) | Crossed cells counted at the defined recovery location |
| ![Formula](https://ml-biomat.com/static/agent-math/05257314088d7512596a9f14.svg) | Viable seeded-cell count |
| ![Formula](https://ml-biomat.com/static/agent-math/7a63829e7be0525729a1c9d4.svg) | Coated passage relative to uncoated passage, % |
| ![Formula](https://ml-biomat.com/static/agent-math/7a5c20b532080055cc6f5c74.svg) | Mean crossed counts of independent coated/uncoated inserts under matched conditions |

Input normalization gives 600/50000=1.2%. Coated-relative passage gives 180/600=30%. The denominators represent viable input and uncoated migration baseline respectively; match volume, time, pores and recovery location.

A coating ratio also contains interactions with adhesion and recovery. A treatment that changes attachment to the underside can change the final count even if the number entering pores remains similar. Where this distinction matters, examine cell positions on both surfaces and recovery into the lower compartment. Preserve input viability and endpoint survival as part of the experiment. A membrane-passage result is most informative when its sampling location and retention processes are made explicit rather than absorbed into a generic migration label.

## Fast, straight and commonly directed are different properties

A time series provides a sequence of coordinates for each tracked cell. Add the straight-line distances between consecutive frames to obtain recorded path length, then divide by total duration to obtain mean path speed. The straight-line distance from the first to last position is net displacement length and ignores detours. A person walking a loop through a park can travel far while ending near the starting point. Retaining both quantities distinguishes active turning from sustained movement in one direction.

$$
L=\sum_{j=1}^{m}\sqrt{(x_j-x_{j-1})^2+(y_j-y_{j-1})^2},\qquad v=L/(t_m-t_0)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Summed path between sampled positions, μm |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | Segment index, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Number of segments, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/96477b2fe2e7ddc7328f97cc.svg) | Coordinates at position j, μm |
| ![Formula](https://ml-biomat.com/static/agent-math/6ea26af94b3e02fd7aa1d744.svg) | Mean recorded path speed, μm/h |
| ![Formula](https://ml-biomat.com/static/agent-math/af01f97a1ec46052fc2a4305.svg) | Last and first observation times, h |

Use the Pythagorean theorem for each segment, then add the segment lengths. Positions (0, 0), (3, 4) and (6, 4) give segments of 5 and 3 μm. The 8 μm path covered in 2 h gives a mean recorded speed of 4 μm/h. Changing the sampling interval changes how much curvature the recorded path captures.

Dividing net displacement length by path length gives directness between zero and one. A straight path to the left and a straight path to the right both approach one, so directness alone does not establish a shared direction. Define the anticipated gradient as the positive x-axis and project net displacement onto that axis before dividing by path length. This forward migration index has a sign: positive means net progress along the chosen direction, negative means progress against it, and near zero means little net progress along that axis.

$$
D=\frac{\sqrt{(x_m-x_0)^2+(y_m-y_0)^2}}{L},\qquad \mathrm{FMI}_x=\frac{x_m-x_0}{L}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | Track directness, dimensionless, 0 to 1 |
| ![Formula](https://ml-biomat.com/static/agent-math/eb985d0dd107c86347098e80.svg) | Forward migration index along predefined positive x, dimensionless, −1 to 1 |
| ![Formula](https://ml-biomat.com/static/agent-math/3c267702472a95afa49a186f.svg) | Endpoint coordinates, μm |
| ![Formula](https://ml-biomat.com/static/agent-math/640d1781cec644e3d742caf9.svg) | Starting coordinates, μm |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Total path length of the same track, μm, greater than 0 |

Divide the net displacement by path length to obtain directness; divide the signed x displacement by path length to retain the direction along x. The worked track has a net displacement of √52 μm, a directness of approximately 0.901 and an x-directed migration index of 6/8 = 0.75. A stationary track has zero path length, so its speed is recorded as zero and its directional ratios are recorded separately as undefined.

Consider a cell beginning at the origin, reaching 3 micrometers horizontally and 4 vertically after one hour, then 6 horizontally and 4 vertically after two hours. The first segment has length 5 by the Pythagorean theorem and the second has length 3. Total path length is 8 micrometers and mean speed is 4 micrometers per hour. Net displacement is the square root of 52, about 7.211 micrometers, giving directness 0.901 and an x-directed index of 6 divided by 8, or 0.75. The same track supplies each number, but each emphasizes a different aspect of movement.

![Twenty simulated tracks per group, each sampled every 0.5 h with a path speed of 20 μm/h. The panels distinguish directional bias from the effect of coarser sampling on measured movement.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9a19eb5a59604233d7160332.svg?v=9a19eb5a5960)

Figure 4Twenty simulated tracks per group, each sampled every 0.5 h with a path speed of 20 μm/h. The panels distinguish directional bias from the effect of coarser sampling on measured movement.

Both constructed populations move 10 micrometers every half-hour, so their recorded mean speed is 20 micrometers per hour. One chooses headings uniformly; the other has headings concentrated around positive x. Trajectory plots and forward indices differ despite their equal speed. If images are sampled only every two hours, a curved route between observations is replaced by one straight segment and estimated path length decreases. Frequent-turning cells usually lose more recorded distance. Temporal resolution, like spatial calibration, is part of a speed measurement's definition.

Tracking must also address stage drift, cell division and cells leaving the field. Stationary background features can help correct drift that would otherwise move every apparent trajectory together. Decide whether division ends a parent track or begins a lineage record. Selecting only cells that remain inside the image can favor slower cells; retain departure information and choose a suitable observation region. Many tracks describe the distribution within one experiment. Repeated independently prepared cultures reveal how those distributions vary between experimental preparations.

## Preserving enough biological information in the image

The measured figure below shows several possible meanings of change in a scratch assay. Panel A presents edge movement in a time sequence, B follows gaps from 0 to 24 hours, and D compares distinct phenotypes. Edge continuity, elongated cells and rounded mitotic cells provide clues beyond an area statistic. Locate the original scale bars and time points first, then compare spatial patterns at the same scale before connecting them to a numerical measure. This preserves the whole image while making quantification visually accountable.

![Yarrow et al. (2004), Fig. 1, reproduced in full under CC BY 2.0. A shows BS-C-1 cells over time; B covers 0–24 h; D compares cellular phenotypes. Original scale bars are retained: 20 μm in A, 100 μm in B and D, and 500 μm in the lower part of C.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/7a98456593600f98c9137c6e.svg?v=7a9845659360)

Figure 5Yarrow et al. (2004), Fig. 1, reproduced in full under CC BY 2.0. A shows BS-C-1 cells over time; B covers 0–24 h; D compares cellular phenotypes. Original scale bars are retained: 20 μm in A, 100 μm in B and D, and 500 μm in the lower part of C.

Return to the same field over time and maintain suitable focus, illumination and acquisition settings. Photographing the center initially and a narrower end later mixes position with closure. Saved stage coordinates or a consistent positioning scheme make repeated sampling possible. Material scattering, color and autofluorescence can alter contrast between cells and gap, motivating an appropriate imaging mode or additional channel. Higher magnification supplies detail but should still capture enough of the boundary to represent the intended region.

Transwell counting similarly needs spatial coverage. The center and edge of a membrane can contain different cell densities. Prespecified fields or whole-membrane imaging reduce selection of unusually dense regions. Fields are subsamples of one insert: combine them at the insert level before comparing independent repetitions. Clusters can place several nuclei inside one bright object, and staining intensity can change with treatment. Define the counted object and retain representative images with segmentation overlays so altered brightness is distinguished from altered number.

For released material components, conditioned medium can enter the relevant compartment. For a contact effect, specify whether cells encounter a coating, membrane or extracted substrate. Those arrangements ask different questions. If treatment reduces both viable cell number and crossing count, combine initial input, endpoint survival and trajectories to identify the next experiment on toxicity, adhesion or motility. A coordinated set of observations explains where the material acts more effectively than repeatedly reporting a closure percentage.

## A complete example connecting areas, tracks and membrane counts

The complete Python program exports five bilingual figure sets and inspectable data. The scratch example retains original constructed images, known gap masks and actually segmented masks, then exports time-resolved area. The tracking example records each cell's coordinates, time and population. The membrane example records each independent constructed insert's crossing count and viable input, alongside the two-compartment mass balance. The published figure retains its original annotations. The displayed computational figures are the actual outputs of this runnable example.

### Complete Python: Segmentation, tracks and membrane denominators

Exports image arrays, gap masks, cell tracks, insert-level counts, compartment mass balance and bilingual figures.

```
"""Offline constructed scratch, tracking and Transwell examples with a licensed measured figure."""
from pathlib import Path
import argparse,csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle
from scipy.ndimage import gaussian_filter,label
from PIL import Image
BLUE='#186e83';AMBER='#cd803f';PURPLE='#8160a1';GREEN='#3c8a6a'

def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def metrics(track,dt):
    track=np.asarray(track,dtype=float)
    if track.ndim!=2 or track.shape[1]!=2 or len(track)<2 or not np.isfinite(track).all() or not np.isfinite(dt) or dt<=0:
        raise ValueError('Provide at least two finite x/y positions and a positive sampling interval.')
    length=float(np.linalg.norm(np.diff(track,axis=0),axis=1).sum());displacement=track[-1]-track[0]
    stationary=length==0
    return {'path_um':length,'speed_um_per_h':float(length/((len(track)-1)*dt)),'stationary':stationary,'directness':None if stationary else float(np.linalg.norm(displacement)/length),'fmi_x':None if stationary else float(displacement[0]/length)}

def population_metrics(tracks,dt):
    values=[metrics(track,dt) for track in tracks]
    directional=[value['fmi_x'] for value in values if not value['stationary']]
    return {'mean_fmi_x':float(np.mean(directional)) if directional else None,'mean_speed_um_h':float(np.mean([value['speed_um_per_h'] for value in values])),'stationary_fraction':float(np.mean([value['stationary'] for value in values])),'directional_track_count':len(directional)}
def main(output,language='zh'):
    out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh';T=lambda a,b:a if zh else _label(b)
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5'})
    def save(fig,n):fig.savefig(out/f'{n}-{language}.svg',bbox_inches='tight');plt.close(fig)
    rng=np.random.default_rng(1010);px=2.;yy,xx=np.mgrid[:300,:480];x=xx*px;y=yy*px;center=480+12*np.sin(y/60);times=np.array([0,6,12,18,24]);images=[];masks=[];truth_masks=[];areas=[]
    for t in times:
        width=400-10*t;gap=abs(x-center)<width/2;raw=np.where(gap,30.,120.)+rng.normal(0,5,gap.shape)+8*np.sin(x/13)*np.cos(y/17)*(~gap);raw=gaussian_filter(raw,.7)
        candidate=gaussian_filter(raw,1)<75;labs,n=label(candidate);sizes=np.bincount(labs.ravel());sizes[0]=0;mask=labs==np.argmax(sizes)
        images.append(raw);masks.append(mask);truth_masks.append(gap);areas.append(mask.sum()*px**2)
    areas=np.array(areas);closure=100*(1-areas/areas[0]);np.savez_compressed(out/'scratch_images.npz',time_h=times,image=np.array(images),segmented_gap=np.array(masks),known_gap=np.array(truth_masks),pixel_um=px)
    with(out/'closure.csv').open('w',newline='',encoding='utf8')as f:
        w=csv.writer(f);w.writerow(['time_h','segmented_area_um2','closure_percent','ideal_width_um']);w.writerows(zip(times,areas,closure,400-10*times))
    tracksets={};trackrows=[]
    for name in ['random','directed']:
        tracks=[]
        for j in range(20):
            angle=rng.uniform(-np.pi,np.pi,24)if name=='random'else rng.normal(0,.35,24)
            step=10*np.column_stack([np.cos(angle),np.sin(angle)]);track=np.vstack([np.zeros(2),np.cumsum(step,axis=0)]);tracks.append(track)
            for k,(tx,ty)in enumerate(track):trackrows.append([name,j+1,k*.5,tx,ty])
        tracksets[name]=tracks
    with(out/'tracks.csv').open('w',newline='',encoding='utf8')as f:
        w=csv.writer(f);w.writerow(['group','cell_id','time_h','x_um','y_um']);w.writerows(trackrows)
    counts={'no_cue':[180,200,220],'lower_cue':[540,600,660],'uniform_cue':[360,400,440],'upper_cue':[135,150,165],'coated_lower_cue':[150,180,210]}
    with(out/'transwell_counts.csv').open('w',newline='',encoding='utf8')as f:
        w=csv.writer(f);w.writerow(['condition','independent_insert','whole_membrane_count','input_cells']);w.writerows([k,i+1,v,50000]for k,vals in counts.items()for i,v in enumerate(vals))
    t=np.linspace(0,12,121);vu=.1;vl=.6;k=.02;equilibrium=10*vl/(vu+vl);decay=np.exp(-k*(1/vu+1/vl)*t);cu=equilibrium*(1-decay);cl=equilibrium+(10-equilibrium)*decay
    with(out/'gradient.csv').open('w',newline='',encoding='utf8')as f:
        w=csv.writer(f);w.writerow(['time_h','upper_ng_ml','lower_ng_ml','total_ng']);w.writerows(zip(t,cu,cl,vu*cu+vl*cl))
    fig,ax=plt.subplots(1,2,figsize=(11,5.3))
    for a in ax:a.axis('off');a.set(xlim=(0,10),ylim=(0,7))
    ax[0].add_patch(Rectangle((.5,1.1),9,4,fc=BLUE,alpha=.1));ax[0].add_patch(Rectangle((4,1.1),2,4,fc='#faf9f5'))
    for j in range(4):
        for i in range(3):
            for shift in[0,6]:ax[0].add_patch(Circle((1+i*.8+shift,1.6+j*.9),.28,fc=BLUE,alpha=.7))
    ax[0].annotate('',xy=(4.7,3),xytext=(3.1,3),arrowprops={'arrowstyle':'->','lw':2,'color':AMBER});ax[0].annotate('',xy=(5.3,3),xytext=(6.9,3),arrowprops={'arrowstyle':'->','lw':2,'color':AMBER});ax[0].text(5,6,T('同一平面：空隙如何闭合','One plane: how a gap closes'),ha='center',fontsize=12);ax[0].text(5,.3,T('迁移、铺展与增殖共同改变覆盖面积','Migration, spreading and division change coverage'),ha='center',fontsize=9)
    ax[1].add_patch(Rectangle((1,1),8,4.7,fill=False,ec=BLUE,lw=2));ax[1].add_patch(Rectangle((2.2,3),5.6,3,fill=False,ec=PURPLE,lw=2));
    for i in range(6):ax[1].plot([2.2+i*.95,2.7+i*.95],[3,3],color=PURPLE,lw=4)
    for xx0 in[3,4.4,6,7]:ax[1].add_patch(Circle((xx0,3.6),.22,fc=BLUE))
    for xx0 in[2,3,4,5,6,7,8]:ax[1].add_patch(Circle((xx0,1.8),.07,fc=AMBER))
    ax[1].annotate('',xy=(5,2.3),xytext=(5,3.6),arrowprops={'arrowstyle':'->','lw':2,'color':AMBER});ax[1].text(5,6.6,T('1962 Boyden：用膜连接两个室','1962 Boyden: two compartments and a membrane'),ha='center',fontsize=12);ax[1].text(5,.3,T('现代插入式装置原创示意，非历史原件','Original modern-insert schematic, not the historical apparatus'),ha='center',fontsize=9);fig.tight_layout();save(fig,'history')
    fig,ax=plt.subplots(2,3,figsize=(12,7.7))
    for j,idx in enumerate([0,2,4]):
        a=ax[0,j];a.imshow(images[idx],cmap='gray',vmin=20,vmax=140,extent=[0,960,600,0]);a.contour(x,y,masks[idx],levels=[.5],colors=[AMBER],linewidths=.7);a.set(title=f'{times[idx]} h',xlabel='x / μm',ylabel='y / μm')
    ax[1,0].plot(times,closure,'o-',color=BLUE);ax[1,0].plot(times,100*10*times/400,'--',color=AMBER);ax[1,0].set(xlabel=T('时间 / h','Time / h'),ylabel=T('空隙闭合 / %','Gap closure / %'),title=T('A  分割值与几何真值','A  Segmentation and geometric truth'))
    width=np.linspace(200,800,100);ax[1,1].plot(width,np.minimum(100,100*240/width),color=PURPLE);ax[1,1].set(xlabel=T('初始宽度 / μm','Initial width / μm'),ylabel=T('24小时闭合 / %','Closure at24 h / %'),title=T('B  同一边缘速度，起始宽度不同','B  Same edge speed, different initial widths'))
    th=np.arange(50,101,5);sensitivity=[]
    for q in th:
        aa=[(gaussian_filter(im,1)<q).sum()*px**2 for im in[images[0],images[-1]]];sensitivity.append(100*(1-aa[1]/aa[0]))
    ax[1,2].plot(th,sensitivity,'o-',color=GREEN);ax[1,2].axhline(60,color='gray',ls='--');ax[1,2].set(xlabel=T('分割阈值 / a.u.','Segmentation threshold / a.u.'),ylabel=T('24小时闭合 / %','Closure at24 h / %'),title=T('C  边界判断的敏感性','C  Sensitivity to boundary definition'));fig.tight_layout();save(fig,'scratch')
    fig,ax=plt.subplots(2,2,figsize=(11,8.7))
    for j,name in enumerate(['random','directed']):
        a=ax[0,j]
        for track in tracksets[name]:a.plot(track[:,0],track[:,1],alpha=.6,lw=1.2,color=BLUE if j==0 else AMBER);a.scatter(*track[-1],s=8,color=PURPLE)
        a.set_aspect('equal');a.set(xlim=(-130,260),ylim=(-140,140),xlabel='x / μm',ylabel='y / μm',title=T('A  无偏方向，步长相同','A  Unbiased headings, equal step length')if j==0 else T('B  方向偏向正x，步长仍相同','B  Headings biased toward+x, same steps'));a.axhline(0,color='gray',lw=.5);a.axvline(0,color='gray',lw=.5)
    for j,name in enumerate(['random','directed']):
        ms=[metrics(q,.5)for q in tracksets[name]];ax[1,0].scatter(np.full(20,j),[m['fmi_x']for m in ms],color=BLUE if j==0 else AMBER,alpha=.65)
        for stride,col in[(1,BLUE),(4,AMBER)]:ax[1,1].scatter(j+(.12 if stride==4 else-.12),np.mean([metrics(q[::stride],.5*stride)['speed_um_per_h']for q in tracksets[name]]),color=col,s=60)
    for a in ax[1]:a.set_xticks([0,1],[T('随机方向','Random'),T('定向','Directed')]);a.grid(alpha=.15)
    ax[1,0].set(ylabel=T('沿x前向迁移指数','Forward migration index along x'),title=T('C  方向性由投影位移体现','C  Projected displacement measures bias'))
    ax[1,1].set(ylabel=T('估计平均速度 / μm/h','Estimated mean speed / μm/h'),title=T('D  蓝：0.5h采样；橙：2h采样','D  Blue:0.5h sampling; orange:2h'));fig.tight_layout();save(fig,'tracks')
    fig,ax=plt.subplots(1,2,figsize=(11,4.8));ax[0].plot(t,cu,color=BLUE,label=T('上室','Upper'));ax[0].plot(t,cl,color=AMBER,label=T('下室','Lower'));ax[0].set(xlabel=T('时间 / h','Time / h'),ylabel=T('体积平均浓度 / ng/mL','Volume-averaged concentration / ng/mL'),title=T('A  两室交换的构造模型','A  Constructed two-compartment exchange'));ax[0].legend()
    labels=[T('无信号','No cue'),T('下室信号','Lower cue'),T('均匀信号','Uniform cue'),T('上室信号','Upper cue'),T('涂层+下室','Coated+lower')]
    for i,(name,values)in enumerate(counts.items()):ax[1].scatter(np.full(3,i),values,color=BLUE);ax[1].plot([i-.15,i+.15],[np.mean(values)]*2,color=AMBER,lw=3)
    ax[1].set_xticks(range(5),labels,rotation=20,ha='right');ax[1].set(ylabel=T('每张膜通过的细胞数','Crossed cells per membrane'),title=T('B  构造计数：每点是独立插入件','B  Constructed counts: each dot is an insert'))
    for a in ax:a.grid(alpha=.15)
    fig.tight_layout();save(fig,'transwell')
    fig,ax=plt.subplots(figsize=(11,10));ax.imshow(Image.open(Path(__file__).resolve().parent/'yarrow2004-figure1.jpg').convert('RGB'));ax.axis('off');ax.set_title(T('真实划痕实验：闭合之外还有形态与分裂信息','Measured scratch assay: closure, morphology and division'),fontsize=12);fig.text(.5,.015,T('Yarrow等2004，图1；CC BY2.0，完整转载。\n原图比例尺：A20μm；B、D100μm；C底部500μm。','Yarrow et al.2004,Fig1; CC BY2.0, reproduced in full.\nOriginal scale bars:A20μm;B/D100μm;Cbottom500μm.'),ha='center',fontsize=9);fig.tight_layout(rect=[0,.07,1,1]);save(fig,'published')
    simple=metrics(np.array([[0.,0.],[3.,4.],[6.,4.]]),1)
    stationary=metrics(np.zeros((3,2)),1)
    assert stationary['speed_um_per_h']==0 and stationary['directness'] is None and stationary['fmi_x'] is None
    summary={'geometry':{'initial_area_um2':400*600,'final_area_um2':160*600,'closure_percent':60,'one_edge_speed_um_h':(400-160)/(2*24),'equivalent_area_from_60000_pixels_um2':60000*2**2},'tracking':simple,'stationary_tracking':stationary,'stationary_population':population_metrics([np.zeros((3,2))],1),'transwell':{'migration_percent':600/50000*100,'coated_to_uncoated_percent':180/600*100,'initial_total_ng':.6*10,'final_total_ng':float(vu*cu[-1]+vl*cl[-1]),'equilibrium_ng_ml':equilibrium},'segmentation':{'initial_area_um2':float(areas[0]),'final_closure_percent':float(closure[-1])},'populations':{name:population_metrics(tracks,.5) for name,tracks in tracksets.items()}}
    assert abs(closure[-1]-60)<.15
    (out/'summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False),encoding='utf8');print(json.dumps(summary,allow_nan=False))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

Double the initial gap width while preserving boundary speed and inspect the 24-hour closure percentage. Change the segmentation threshold and inspect the contour as well as the percentage. Increase the trajectory sampling interval and compare path speed with net displacement. Finally, change input cell number, uncoated counts and coated counts separately, checking which denominator serves each question. Keeping the inputs and outputs together reveals whether a change originates in assumed behavior, sampling geometry or analysis rules.

For a material intended to support tissue coverage, emphasize initial density, closure through time, edge organization, survival and proliferation. For chemotaxis, bring gradient controls and directional trajectories into the central comparison. For matrix passage, retain the coating definition and matched uncoated migration result. These questions can be connected, while each keeps its primary measurement clear. The result then describes how cells change position and coverage in a specified environment and geometry, rather than ending with an unexplained claim of more or faster movement.

When closure approaches 100%, retain timing information. Two groups can both be completely closed at the endpoint even though one reaches that state much earlier. Multiple time points or an explicitly defined arrival time preserve the difference. Once opposing edges meet, the geometry changes: a gap can no longer narrow through the same two-boundary process. Fitting the resulting flat segment as though it represented an unchanged front velocity mixes this geometric endpoint with the speed estimate. Choose a clearly visible pre-closure interval and identify what feature of the image the fitted slope describes.

Keep a hierarchy connecting culture preparation, insert, field and cell track. Three inserts with five fields each produce fifteen images, but the independent experimental units are initially the three inserts. Independently prepared cultures on different days provide another level of variation. Repeated images from one field share the same starting population. This hierarchy guides a suitable statistical model and makes unusual images traceable. More numerical observations provide better description only when the experimental conditions they share remain visible.

Matrix passage also benefits from retaining the raw counts behind a ratio. Suppose treatment reduces the coated count from 180 to 90 and the uncoated count from 600 to 300. The coated-to-uncoated percentage remains 30%, while both absolute passage counts halve. Reporting only that percentage would conceal the common change. Conversely, an unchanged coated count combined with a higher uncoated count lowers the ratio through its denominator. Plot paired coated and uncoated counts beside the normalized result so the reader can identify which component changed and choose a mechanistic follow-up.

Collective movement offers a related distinction in planar assays. Neighboring cells can move coherently while individual trajectories show small lateral differences, or a few fast cells can enter the gap ahead of a relatively stationary sheet. An area curve summarizes coverage, while an aligned trajectory display reveals how movement is distributed among cells. Retaining a view of the original spatial positions alongside trajectories shifted to a common origin helps connect local edge behavior with population direction. A common-origin plot emphasizes displacements; the original image preserves who was next to whom.

These comparisons lead to focused next experiments. A change dominated by cell loss calls for matched survival measurements; a change in track direction with preserved speed calls for a gradient-focused comparison; a change confined to coated inserts points toward interactions with that coating. Each follow-up adds an observation that distinguishes competing explanations already visible in the data. The sequence keeps the biological question connected to an experimentally measurable behavior.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L10.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Boyden (1962): The chemotactic effect of mixtures of antibody and antigen on polymorphonuclear leucocytes](https://pmc.ncbi.nlm.nih.gov/articles/PMC2137509/)

   Original membrane-separated compartments and experimental variable design.

   Historical technical reference; original figure not reproduced
2. [Yarrow et al. (2004): A high-throughput cell migration assay using scratch wound healing](https://pmc.ncbi.nlm.nih.gov/articles/PMC521074/)

   Measured closure, morphology and division; imaging readouts.

   CC BY 2.0; Fig. 1 reproduced in full.
3. [Justus et al. (2023): Transwell In Vitro Cell Migration and Invasion Assays](https://pmc.ncbi.nlm.nih.gov/articles/PMC10335869/)

   Adherent/nonadherent recovery, membrane counting and assay conditions.
4. [Corning: Assay Methods—Cell Invasion Assay](https://www.corning.com/catalog/cls/documents/protocols/protocol_DL_031_Cell_Invasion_Assay.pdf)

   Coated/uncoated pairing, independent inserts and passage denominators.
5. [ibidi: Chemotaxis and Migration Tool 2.0 manual](https://ibidi.com/img/cms/products/software/chemotaxis_tool/Manual_ChemotaxisTool_2_0_eng.pdf)

   Track calibration, path length, directness and forward migration index.
6. [ImageJ: Analyze menu](https://imagej.net/ij/docs/menus/analyze.html)

   Spatial calibration, area and retained regions.
