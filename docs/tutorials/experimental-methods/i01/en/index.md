# Optical and fluorescence microscopy: From light paths to trustworthy images

Source: https://ml-biomat.com/tutorials/experimental-methods/i01/en/
Language: en

Follow a specimen through light paths and pixels, then examine resolution, intensity and object measurements in a real cell image.

## How does a photograph of cells become a scientific measurement?

Place a transparent hydrogel under a microscope and you may see round spots, elongated shadows and faint boundaries. Which features are cells, bubbles, pores in the material or dust on the coverslip? If cells on one material look brighter or larger, have they changed biologically, or was the exposure longer and the focus better? Optical microscopy brings small structures within reach, while leaving the observer with these essential decisions. This chapter follows light from the specimen to the image, then connects pixels, resolution, fluorescence intensity and object counting. The aim is to choose appropriate evidence for questions such as whether cells spread, where a fluorescent label accumulates and whether two experimental groups differ.

Three different tasks are hidden inside the word “seeing.” Detection asks whether a signal exists. Resolution asks whether two nearby features can be distinguished. Measurement assigns a defined number to a length, area, count or intensity. A distant lamp can be detected at night even when its shape is impossible to resolve. Similarly, a fluorescent molecule much smaller than the optical resolution scale can emit enough light to be detected by a camera. Its image is a spot whose width is largely determined by the microscope. Treating that spot diameter as the molecule's diameter would turn a successful detection into an incorrect size measurement.

For biological materials, an image also belongs to an experimental hierarchy. Ten fields may be recorded in one culture well, with dozens of cells measured in each field, but those cells share the medium, material preparation and treatment. When the question concerns differences between material preparations, independently prepared samples provide the main experimental replication. Individual cells can still describe the distribution of cell shapes, provided their sample and field identities are retained. Deciding whether the comparison concerns cells, fields or independent specimens before acquisition gives later statistical plots a meaningful denominator. Experimental design therefore begins with the very first decision about where to point the microscope.

## From Hooke's observations to fluorescent labels: creating contrast

Robert Hooke's *Micrographia*, published in 1665, brought microscopic observations to a wide readership through detailed illustrations. It connects two tasks that still matter: making a small structure produce useful contrast and recording that observation clearly enough for someone else to examine it. A compound microscope uses an objective to form a magnified intermediate image and an eyepiece to view it. A modern digital microscope directs an image toward a camera. Although the recording device has changed, illumination, the objective, the specimen and the observation plane still determine what information is present. The original schematic below places the historical arrangement beside a modern fluorescence path to make that connection visible.

![Original optical schematic linking illumination, specimen and viewing in a compound microscope with excitation–emission separation in modern epifluorescence. Not to scale or a dimensional reconstruction of a particular historical instrument.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/633778308d5cad8d0d2bb1dc.svg?v=633778308d5c)

Figure 1Original optical schematic linking illumination, specimen and viewing in a compound microscope with excitation–emission separation in modern epifluorescence. Not to scale or a dimensional reconstruction of a particular historical instrument.

In transmitted brightfield microscopy, light passes through the specimen before entering the objective. A region that absorbs or scatters more light usually sends less light toward the camera and appears darker. Stained tissue can therefore show clear structure, whereas a living cell, which contains a large amount of water and absorbs weakly, may look almost invisible in transparent medium. The cell can nevertheless change the speed and phase of light. Phase describes where a wave lies within its cycle of oscillation. Phase contrast and differential interference contrast convert otherwise inconspicuous optical differences into intensity differences. Their halos and relief-like shading arise partly from the imaging process; they are not direct maps of cell height.

Fluorescence supplies a different source of contrast. A fluorescent molecule absorbs excitation light and, after a short interval, can emit light at a different wavelength. For many commonly used labels, emission occurs at a longer wavelength. Stokes's work on fluorescence in 1852 helped establish this spectral transformation as a systematic optical phenomenon. A fluorescence microscope exploits the wavelength difference to separate intense excitation from much weaker emission. An excitation filter selects incoming wavelengths, a dichroic mirror redirects selected bands, and an emission filter rejects remaining excitation light. The objective can deliver illumination and collect part of the emission returning from the specimen. Filter selection consequently affects background and channel separation as well as the apparent image color.

Labels make contrast biologically selective. A DNA-binding dye can reveal nuclei; a fluorescent antibody can help locate a target protein; fluorescent beads can report movement inside a hydrogel. Connecting the location of fluorescence to the location of a biological target also requires suitable staining. The label must reach the intended site, binding should be sufficiently specific, and unbound material should be removed appropriately. Some substrates and biomaterials fluoresce without added dye, with different behavior under different excitation bands. Unstained material, suitable target-negative controls and singly labeled specimens acquired under comparable settings help identify these contributions. Once their roles are understood, the spatial distribution of cells or proteins can be interpreted more directly.

## Magnification, resolution and sampling are different controls

An objective may carry a marking such as “60×/1.30.” The first number is magnification and the second is usually numerical aperture. Magnification determines how large the specimen's image becomes at the detector. Numerical aperture describes the angular cone of light that the objective can accept, together with the refractive index of the intervening medium. A funnel collecting rain offers a useful first analogy: a wider acceptance angle captures light arriving from more directions. The refractive index is equally important, which is why high-aperture objectives are designed for particular immersion media. Air, water-immersion and oil-immersion objectives operate under different conditions; exchanging media arbitrarily changes the light path and can introduce aberrations.

$$
\mathrm{NA}=n\sin\alpha
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/94fc28e088e9b56db129dfa6.svg) | Numerical aperture, dimensionless; object-side aperture here. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Refractive index of the medium between specimen and objective; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | Half-angle of the accepted light cone; use radians in a trigonometric function or an explicitly selected degree mode. |

For n=1.515 and a half-angle of about 59.1°, NA is approximately 1.30. The half-angle runs from the optical axis to the edge of the cone; the full cone angle should not be substituted. Medium and geometry jointly determine the aperture.

Light behaves as a wave. Even an ideal point emitter passing through an optical system with a finite aperture produces an image with finite width, called the point-spread function, or PSF. A complex fluorescent specimen can be pictured as a collection of tiny emitters. Each contributes its own spread-out spot, and their contributions add to form the recorded image. Well-separated emitters produce distinct peaks with a valley between them. As their separation decreases, the spots overlap and distinguishing two objects becomes harder. The Rayleigh criterion provides a commonly used lateral separation scale for equal-brightness point sources in an ideal diffraction-limited system. It is a specified criterion rather than a universal boundary for every specimen and detection task.

$$
d_{\mathrm R}=\frac{0.61\lambda}{\mathrm{NA}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5044dd543be62338ea7d9e03.svg) | Ideal lateral Rayleigh separation scale, in the same length unit as wavelength, e.g. μm. |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | Fluorescence emission wavelength in vacuum; 0.520 μm here. |
| ![Formula](https://ml-biomat.com/static/agent-math/94fc28e088e9b56db129dfa6.svg) | Object-side numerical aperture; dimensionless, 1.30 here. |

0.61×0.520/1.30=0.244 μm. The expression describes the Rayleigh criterion for equal-brightness point sources with an ideal circular aperture under diffraction-limited conditions. The coefficient comes from the Airy pattern; shorter wavelengths or larger apertures reduce the spot scale.

For an emission wavelength of 520 nm and an aperture of 1.30, the Rayleigh scale is approximately 244 nm, or 0.244 μm. Enlarging the resulting camera image fourfold enlarges two overlapping spots together; it does not create a missing valley between them. Improving optical separation involves changing the effective aperture, wavelength, aberrations or imaging method. The two-emitter plots below approximate the central part of the PSF with a Gaussian profile to make overlap easy to calculate and inspect. A real circular aperture produces an Airy pattern with additional rings. The Gaussian curves explain the mechanism, while the separately reported Rayleigh scale is calculated from its stated optical formula.

![Teaching calculations and simulations. A: higher NA narrows Gaussian central profiles for two emitters separated by 0.30 μm. B: coarse sampling loses detail even with unchanged optics. C: SNR with photon noise alone or added background and read noise. D: 10,000 seeded Poisson exposures with mean count 100.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/a490660a348112dcb5061a44.svg?v=a490660a3481)

Figure 2Teaching calculations and simulations. A: higher NA narrows Gaussian central profiles for two emitters separated by 0.30 μm. B: coarse sampling loses detail even with unchanged optics. C: SNR with photon noise alone or added background and read noise. D: 10,000 seeded Poisson exposures with mean count 100.

The camera must sample the detail delivered by the optics. A detector pixel 6.5 μm wide corresponds to approximately 0.108 μm at the specimen when total magnification is 60. A larger specimen-plane pixel places fewer samples across the same structure, rather like drawing a fine curved line on coarse graph paper and missing its turns. Half the stated resolution scale is used here as a practical sampling check: half of 0.244 μm is about 0.122 μm, so a 0.108 μm pixel passes that check. A full sampling design should consider the spatial-frequency support of the imaging mode, any camera adapter and pixel binning. Beads or calibration specimens help check the achieved PSF and physical pixel scale.

$$
p_{\mathrm s}=\frac{p_{\mathrm c}}{M},\qquad p_{\mathrm s}\lesssim\frac{d_{\mathrm R}}2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4a7ed4ea54cfbe1740080f73.svg) | Specimen-plane pixel spacing, μm per pixel. |
| ![Formula](https://ml-biomat.com/static/agent-math/410307030b95e045f504bfeb.svg) | Camera sensor pixel spacing, μm per pixel. |
| ![Formula](https://ml-biomat.com/static/agent-math/34058a2a5d1de088feed7d98.svg) | Total lateral magnification from specimen to camera, dimensionless, including adapter optics. |
| ![Formula](https://ml-biomat.com/static/agent-math/5044dd543be62338ea7d9e03.svg) | Selected lateral resolution scale, μm. |

6.5 μm divided by 60 gives 0.1083 μm per pixel. At least two samples per stated resolution scale are used as a practical check, rather than a complete frequency-domain sampling specification for every imaging mode. Recalculate after binning or changing adapter magnification.

This distinction matters even for an ordinary width measurement. Suppose a fiber spans five pixels, each corresponding to 0.20 μm. Multiplication gives an apparent image width of 1.0 μm. If the fiber's true width is close to the PSF width, blur strongly influences its edges, and interpretation needs an imaging model. For projected areas of cells tens of micrometers across, the same blur may contribute a smaller relative error. For fibers a few hundred nanometers wide, it can dominate the measurement. Placing the anticipated object size and the imaging scale on the same ruler before choosing an objective is often more useful than repeatedly changing segmentation thresholds after acquisition.

The resolution comparison also helps explain why objective selection is not a contest to obtain the highest possible magnification. A larger field may reveal how cells distribute across a scaffold, whereas a smaller field may be needed to inspect local morphology. A highly magnified image that contains only part of one cell does not answer a question about population coverage. Conversely, a wide field with coarse sampling may miss the fine structures needed for a width measurement. Match the field of view, optical resolution and sampling to the quantity being measured, and include an overview when a detailed crop would otherwise hide the context.

## Preserve the structure you want to observe during preparation

Living cells, fixed cells and tissue sections require different preparation routes. Live imaging is suited to changing morphology, movement and short-term responses. Temperature, medium, gas conditions and light dose can influence the process being observed. Fixed samples provide a more stable record of a selected state and can support repeated staining or longer acquisition, while fixation, permeabilization, dehydration and mounting can alter shape or molecular distribution. Begin by naming what needs to be preserved: continuity of the membrane, the organization of the cytoskeleton or the position of a soluble protein. Then choose conditions that retain that feature while allowing the relevant label to reach its target, and apply comparable handling across the groups.

Transparent material still modifies the optical path. A mismatch among the refractive indices of hydrogel, medium, coverslip and immersion fluid can prevent rays from different depths from meeting accurately, making the image blurrier as depth increases. Thick specimens also introduce scattered and out-of-focus light. Widefield fluorescence can acquire thin cell layers efficiently; a particular plane inside a three-dimensional culture often benefits from an optical-sectioning method such as confocal microscopy. Consider specimen thickness, depth of interest and objective working distance before choosing the imaging mode. This helps distinguish a genuine absence of cells from a loss of visibility deeper in the material.

The coverslip is part of the optical arrangement, not just a transparent support. Some high-aperture objectives are corrected for a specified coverslip thickness, and a departure from that condition introduces aberration. The material and thickness of a culture-dish bottom can similarly restrict usable objectives. Record objective markings, immersion medium, specimen container and camera coupling together; where needed, calibrate distances using a stage micrometer. Retaining physical pixel size in the image metadata is more reliable than drawing an arbitrary scale bar onto an exported photograph. Cropping, resampling and page layout can change how an image is displayed, so a valid scale bar must remain tied to the actual scale of that image.

Field selection is another preparation decision. Consistently searching for the area in which cells look healthiest favors a locally ideal view of the specimen. A predetermined grid or an explicit random selection rule provides a reproducible route to sampling, with documented treatment of edges, bubbles and preparation defects. Exclusion rules should address unusable acquisition or damaged specimens rather than whether the result matches an expectation. Comparisons between materials are easier when objective, illumination, exposure and processing are held constant. When brightness differences require different acquisition settings, retain the settings and design a calibration that brings signals onto a common measurement scale.

## The camera records a signal from photons, so brightness needs a common scale

A digital image can be understood as a two-dimensional table of numbers. In a fluorescence camera, arriving photons generate charge, which is amplified, offset and digitized. A “16-bit image” provides a larger numerical encoding range than an 8-bit image, but does not by itself guarantee a corresponding amount of useful detail. If the detector or digital range reaches its upper limit, additional photons no longer produce a larger recorded value. This is saturation. Intensity relationships within the saturated region have been lost. Making the display darker changes the appearance on the screen but cannot recover relationships that were not recorded in the first place.

Even when a source has constant average brightness, the number of photons arriving during equal exposures fluctuates. Under a common independent-counting approximation, collecting an average of 100 signal electrons gives a photon-statistical standard deviation of about 10 and an ideal signal-to-noise ratio of 10. An average of 400 gives a standard deviation of about 20 and a signal-to-noise ratio of 20. Four times the signal therefore produces roughly twice the signal-to-noise ratio. This square-root improvement explains why longer exposures progressively demand more acquisition time and light dose. Background light, dark signal and read noise also contribute in real cameras, so they belong in the same noise budget.

$$
\mathrm{SNR}=\frac{S}{\sqrt{S+B+\sigma_{\mathrm r}^{2}}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ae03e7fd82fc9511ad569820.svg) | Signal-to-noise ratio, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | Mean detected signal-electron count in one pixel during one exposure. |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | Mean background-electron count in the same pixel and exposure, with independent Poisson statistics. |
| ![Formula](https://ml-biomat.com/static/agent-math/091162969f7c9d3f6f679061.svg) | Read-noise standard deviation in electron counts; its square is a variance. |

For Poisson counting, variance equals mean count. Independent variances add, and their square root gives total standard deviation. S=100, B=100 and read-noise SD=3 give 100/√209≈6.917. The background mean is assumed accurately estimated; finite background estimation, dark current and interpixel correlations require their own terms when relevant.

The worked example uses 100 signal electrons, 100 background electrons and a read-noise standard deviation of 3 electrons, giving a signal-to-noise ratio of approximately 6.92. Here the mean background is treated as having been estimated independently with sufficient precision and then subtracted, while its random fluctuations remain. Estimating background from only a few pixels adds uncertainty from the estimate itself. Signal-to-noise can be improved by collecting more useful signal or by reducing autofluorescence, stray light and nonspecific staining. The latter can be especially valuable for living cells. Camera gain rescales digital values; it does not improve photon statistics in the same way as collecting additional photons.

Displayed color should also be separated from recorded signal. Showing a grayscale image in green maps numbers to colors. Changing the display range from 0–1000 to 0–500 makes the same values look brighter. A display mapping may be chosen to reveal structure, while quantitative analysis should use retained raw values and report the relevant mapping for comparison. After background correction, integrated signal is the sum of pixel values within a region minus the expected background contribution across that same area. Larger regions include more background. Total fluorescence and mean fluorescence per unit area consequently address different questions; decide whether the target quantity concerns total labeled material, local concentration or cell size.

Exposure comparisons become clearer when these contributions are written down before interpreting a photograph. If two otherwise comparable images were acquired with different exposure times, a linear detector can give different digital values for the same emission rate. Background must be handled on the same basis, and bleaching can make a simple time normalization inaccurate if emission changes during acquisition. A short series at several exposures can reveal the usable range for a stable reference specimen. It also makes saturation visible before important samples are recorded. The useful setting is the one that captures the intended signal within a characterized range while preserving the biological process being studied.

## Follow a real image from pixels to regions before assigning biological meaning

The image below comes from the public DNA-fluorescence cell dataset credited to David Root and distributed through CellProfiler and scikit-image under CC0. The original TIFF is 512×512 pixels. This example preserves its numerical values, displays the raw image and segmentation with the same intensity range, and plots the effect of changing a threshold. No objective magnification or physical pixel spacing is invented for this image, so positions and region areas are expressed in pixels. Reporting micrometers or square micrometers in an experimental analysis requires the conversion from original acquisition metadata or an independent calibration. The distinction keeps a useful image-analysis exercise tied to the information actually available.

![Real DNA-fluorescence image and analysis. Image: David Root / CellProfiler, distributed through scikit-image, CC0. A and B use identical display ranges; green contours mark smoothed regions above threshold 45 and at least 40 pixels in area. C retains the raw histogram. D shows threshold sensitivity. Coordinates are pixels; no missing physical calibration is inferred.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/5489ca2d032d98c6c9030469.svg?v=5489ca2d032d)

Figure 3Real DNA-fluorescence image and analysis. Image: David Root / CellProfiler, distributed through scikit-image, CC0. A and B use identical display ranges; green contours mark smoothed regions above threshold 45 and at least 40 pixels in area. C retains the raw histogram. D shows threshold sensitivity. Coordinates are pixels; no missing physical calibration is inferred.

The calculation first smooths the image with a Gaussian standard deviation of 0.8 pixel, selects values above 45 as foreground, and retains connected regions containing at least 40 pixels. Gaussian smoothing lets nearby pixels contribute to an estimate with distance-dependent weights. It reduces small fluctuations but can alter edges and connections between neighbors. Thresholding converts a continuous brightness value into a binary decision. Connected-component analysis then groups adjacent foreground pixels. Because these steps have distinct purposes, inspect them separately: did smoothing remove fine detail, did the threshold discard dim nuclei, and did the area filter delete real small objects? The overlaid boundaries are included precisely to make those questions visible.

Two neighboring nuclei that touch in the binary mask can become one connected region. An unevenly illuminated nucleus can instead fragment into several regions. The output therefore retains the label “connected regions” rather than substituting a biological cell count. The lower-right panel sweeps thresholds from 20 to 100 to reveal how the numerical result depends on the decision boundary. Low thresholds can join neighboring regions; high thresholds can retain only the bright parts of nuclei. A relatively flat interval indicates reduced sensitivity to that parameter, but anatomical meaning still comes from checking boundaries against the original image in dense, sparse, bright and dim areas.

For a formal counting experiment, the next step could be a set of manually checked fields or a segmentation method that separates touching nuclei. A distance transform measures how far each foreground pixel lies from the boundary, so nuclear interiors often create peaks in a distance map. A watershed method can use selected centers to allocate neighboring pixels and separate touching objects. Too many centers split one nucleus into fragments; too few merge several nuclei. Algorithm choice therefore remains connected to image structure. Retaining area, mean intensity and sample identity for each object allows unusual results to be traced back to the image and preserves the experimental hierarchy for later comparisons.

## Change aperture and pixel spacing, then run the complete analysis

The interactive experiment fixes emission wavelength at 520 nm and places two point emitters on a horizontal line. Numerical aperture changes the width of their point-spread profiles; emitter separation changes how strongly those profiles overlap; specimen-plane pixel spacing changes the sampling points that a camera can record. Predict which adjustment will make the valley easier to recognize, then compare the continuous curve with its samples. The display reports the Rayleigh scale and the number of pixels per resolution scale so that visual impressions can be connected to quantities. This is a lateral central-profile model; an actual acquisition also involves axial resolution, aberrations, noise and specimen movement.

## Two-emitter microscopy experiment

Change aperture, emitter separation and camera sampling to inspect their different roles. The horizontal axis is lateral specimen position; the curve sums teaching Gaussian PSFs and dots mark camera samples.

[Figure: Point-emitter profiles and sampling points](https://ml-biomat.com/tutorials/experimental-methods/i01/en/#I01-plot)

The complete program regenerates the three figures in this chapter. The first is an original optical schematic, the second combines resolution calculations with a photon-counting simulation, and the third processes the real microscopy TIFF included in the download. The program writes a threshold-scan table, arrays containing the raw and processed images, and a summary of resolution scale, pixel spacing, signal-to-noise ratio and connected regions. Begin by changing only the threshold or only the smoothing width, and compare both the boundary overlay and the sensitivity curve. Once the role of each choice is understood, combined adjustments become easier to explain and reproduce.

### Complete Python: optical scales, photon statistics and real-image analysis

The download includes the CC0 TIFF. The offline program produces three figures, image arrays, a threshold table and numerical summary.

```
"""Optical microscopy: resolution, photon statistics and a real CC0 image.

The microscopy data are mitosis.tif, David Root / CellProfiler, CC0.
The analytical point-spread profiles and photon experiment are teaching models.
"""
from pathlib import Path
import argparse
import csv
import json
import numpy as np
from PIL import Image
from scipy import ndimage
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, FancyArrowPatch


def style():
    plt.rcParams.update({'font.family': 'sans-serif',
        'font.sans-serif': ['Microsoft YaHei', 'Noto Sans CJK SC', 'DejaVu Sans'],
        'svg.fonttype': 'none', 'axes.spines.top': False, 'axes.spines.right': False,
        'axes.labelcolor': '#243b45', 'text.color': '#243b45',
        'axes.edgecolor': '#849398', 'axes.titleweight': 'bold',
        'font.size': 11, 'savefig.facecolor': '#faf9f5', 'figure.facecolor': '#faf9f5'})


def main(output, language):
    output.mkdir(parents=True, exist_ok=True)
    style()
    zh = language == 'zh'
    def tr(a, b): return a if zh else b
    def save(fig, name):
        fig.savefig(output / f'{name}-{language}.svg', bbox_inches='tight')
        fig.savefig(output / f'{name}-{language}.png', dpi=140, bbox_inches='tight')
        plt.close(fig)
    blue, green, red, gray = '#3473a8', '#168477', '#bb6046', '#69787e'

    # Original explanatory drawing: the optical geometry is schematic.
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5), layout='constrained')
    for ax in axes:
        ax.set(xlim=(0, 10), ylim=(0, 10)); ax.axis('off')
    a = axes[0]
    a.set_title(tr('A  从照明到观察：早期复合显微镜', 'A  Illumination and viewing: a compound microscope'))
    a.add_patch(Rectangle((4.55, 4), .9, 4.5, color='#ded4bd'))
    a.add_patch(Ellipse((5, 8.2), 1.2, .3, fc='#d7e8ed', ec=blue))
    a.add_patch(Ellipse((5, 4.3), 1.2, .3, fc='#d7e8ed', ec=blue))
    a.plot([3, 7], [2.8, 2.8], color=gray, lw=5)
    a.add_patch(Ellipse((5, 2.9), .6, .15, color=red))
    a.add_patch(Ellipse((1.5, 2.8), .7, .7, color='#e8af58'))
    a.annotate('', (4.8, 2.9), (1.9, 2.9), arrowprops={'arrowstyle':'->','color':'#c58c37','lw':2})
    a.annotate('', (5, 8.9), (5, 3.1), arrowprops={'arrowstyle':'->','color':green,'lw':2})
    for x, y, label in [(6,8.2,tr('目镜','Eyepiece')),(6,4.3,tr('物镜','Objective')),
        (6,2.4,tr('样品','Specimen')),(.3,1.7,tr('照明','Illumination'))]:
        a.text(x,y,label,fontsize=10)
    a.text(.3,.3,tr('1665：《显微图谱》把观察与绘图联系起来\n图示说明光路，并非历史仪器的尺寸复原',
        '1665: Micrographia connects observation and illustration\nOptical schematic; not a dimensional reconstruction'),fontsize=10)
    a = axes[1]
    a.set_title(tr('B  荧光显微镜：分开激发光与发射光','B  Fluorescence: separate excitation and emission'))
    a.plot([.8,5,5],[6.8,6.8,2.7],color=blue,lw=3)
    a.plot([5.25,5.25],[2.7,9],color=green,lw=3)
    a.plot([4.3,5.7],[6.1,7.5],color=gray,lw=4)
    a.add_patch(Ellipse((5.1,4.3),1.7,.45,fc='#d7e8ed',ec=blue))
    a.add_patch(Rectangle((4.6,8.7),1.2,.7,fc='#dde5e3',ec=gray))
    a.add_patch(Ellipse((5.1,2.5),2,.35,fc='#d5a190'))
    a.add_patch(Rectangle((2.4,6.1),.15,1.4,fc=blue,alpha=.5))
    a.add_patch(Rectangle((4.6,7.9),1.2,.12,fc=green,alpha=.6))
    a.text(.2,7.4,tr('激发光','Excitation'),color=blue)
    a.text(6.2,6.7,tr('二向色镜','Dichroic mirror'))
    a.text(6.2,4.2,tr('物镜','Objective'))
    a.text(6.2,2.4,tr('荧光样品','Fluorescent specimen'))
    a.text(6.2,8.1,tr('发射滤光片','Emission filter'))
    a.text(6.2,9,tr('相机','Camera'))
    a.text(.3,.3,tr('蓝色：激发路径；绿色：被收集的发射路径\n只有一小部分各向发射的光进入物镜',
        'Blue: excitation path; green: collected emission\nOnly a fraction of emitted light enters the objective'),fontsize=10)
    save(fig, 'optics')

    wavelength_um, na, camera_pixel_um, magnification = .520, 1.3, 6.5, 60
    rayleigh_um = .61 * wavelength_um / na
    sampling_um = camera_pixel_um / magnification
    x = np.linspace(-1,1,1001)
    sigma = .21 * wavelength_um / na
    sep = .30
    profiles = {}
    fig, axes = plt.subplots(2,2,figsize=(11,8),layout='constrained')
    for aperture, color in [(.65, red),(1.3,green)]:
        s=.21*wavelength_um/aperture
        y=np.exp(-.5*((x-sep/2)/s)**2)+np.exp(-.5*((x+sep/2)/s)**2)
        profiles[str(aperture)]=y
        axes[0,0].plot(x,y,lw=2.4,color=color,label=f'NA={aperture:.2f}')
    axes[0,0].set(xlim=(-.7,.7),xlabel=tr('横向位置 / μm','Lateral position / μm'),ylabel=tr('相对强度','Relative intensity'),title=tr('A  两个点源相距 0.30 μm','A  Two emitters separated by 0.30 μm'))
    axes[0,0].legend(frameon=False)
    fine=profiles['1.3']
    axes[0,1].plot(x,fine,color=gray,lw=1.5,label=tr('连续模型','Continuous model'))
    for pitch,marker,color in [(.1083,'o',green),(.325,'s',red)]:
        xp=np.arange(-.65,.66,pitch)
        yp=np.exp(-.5*((xp-sep/2)/sigma)**2)+np.exp(-.5*((xp+sep/2)/sigma)**2)
        axes[0,1].plot(xp,yp,marker=marker,color=color,ls='--',label=f'{pitch:.3f} μm / pixel')
    axes[0,1].set(xlim=(-.7,.7),xlabel=tr('横向位置 / μm','Lateral position / μm'),ylabel=tr('相对强度','Relative intensity'),title=tr('B  采样太稀会丢掉峰间结构','B  Coarse sampling loses the valley'))
    axes[0,1].legend(frameon=False,fontsize=9)
    photons=np.logspace(0,4,180)
    axes[1,0].loglog(photons,np.sqrt(photons),color=green,lw=2.4,label=tr('纯光子噪声','Photon noise only'))
    axes[1,0].loglog(photons,photons/np.sqrt(photons+100+3**2),color=blue,lw=2.4,label=tr('背景100电子，读出噪声3电子','Background 100; read noise SD 3 electrons'))
    axes[1,0].set(xlabel=tr('平均信号电子数','Mean signal electrons'),ylabel='SNR',title=tr('C  多收集光子怎样改善信噪比','C  How collected photons improve SNR'))
    axes[1,0].legend(frameon=False,fontsize=9)
    rng=np.random.default_rng(612)
    counts=rng.poisson(100,10000)
    axes[1,1].hist(counts,bins=np.arange(60,141,2),color=blue,alpha=.8)
    axes[1,1].axvline(100,color=red,ls='--')
    axes[1,1].set(xlabel=tr('一次曝光的光子数','Photon count in one exposure'),ylabel=tr('模拟次数','Number of simulations'),title=tr('D  同样亮的光源仍会波动','D  A constant source still fluctuates'))
    save(fig,'resolution')

    image=np.asarray(Image.open(Path(__file__).parent/'data/mitosis.tif')).astype(float)
    if image.shape != (512,512): raise ValueError(f'Unexpected image shape {image.shape}')
    smooth=ndimage.gaussian_filter(image,.8)
    threshold=45
    def objects(t):
        mask=smooth>t
        labels,n=ndimage.label(mask)
        sizes=np.bincount(labels.ravel())
        keep=sizes>=40;keep[0]=False
        return keep[labels],int(np.sum(keep))
    mask,nobjects=objects(threshold)
    thresholds=np.arange(20,101,5)
    values=np.array([objects(t)[1] for t in thresholds])
    fig,axes=plt.subplots(2,2,figsize=(11,9),layout='constrained')
    axes[0,0].imshow(image,cmap='gray',vmin=0,vmax=180)
    axes[0,0].set(title=tr('A  真实DNA荧光图像 / CC0','A  Real DNA fluorescence image / CC0'),xlabel=tr('x / 像素','x / pixel'),ylabel=tr('y / 像素','y / pixel'))
    axes[0,1].imshow(image,cmap='gray',vmin=0,vmax=180)
    axes[0,1].contour(mask,levels=[.5],colors=[green],linewidths=.6)
    axes[0,1].set(title=tr(f'B  阈值45：{nobjects}个连通区域',f'B  Threshold 45: {nobjects} connected regions'),xlabel=tr('x / 像素','x / pixel'),ylabel=tr('y / 像素','y / pixel'))
    axes[1,0].hist(image.ravel(),bins=np.arange(257),color=gray)
    axes[1,0].set(yscale='log',xlabel=tr('原始灰度 / 数字量','Raw intensity / digital number'),ylabel=tr('像素数','Pixel count'),title=tr('C  保留原始灰度分布','C  Preserve the raw intensity distribution'))
    axes[1,0].axvline(threshold,color=red,ls='--')
    axes[1,1].plot(thresholds,values,'o-',color=green,lw=2)
    axes[1,1].axvline(threshold,color=red,ls='--')
    axes[1,1].set(xlabel=tr('分割阈值 / 数字量','Segmentation threshold / digital number'),ylabel=tr('面积≥40像素的区域数','Regions with area ≥40 pixels'),title=tr('D  参数敏感性：区域数不等于真细胞数','D  Sensitivity: regions are not ground-truth cells'))
    save(fig,'measurement')
    np.savez_compressed(output/'image_analysis.npz',raw=image,smoothed=smooth,mask=mask)
    with (output/'data.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['threshold_digital_number','connected_regions_area_ge40px']);w.writerows(zip(thresholds,values))
    summary={'rayleigh_um':rayleigh_um,'sample_pixel_um':sampling_um,
        'snr_100_signal_100_background_3_read':100/np.sqrt(209),
        'image_height_px':image.shape[0],'image_width_px':image.shape[1],
        'connected_regions_threshold45':nobjects,'mask_fraction_threshold45':float(mask.mean()),
        'poisson_sample_mean':float(counts.mean()),'poisson_sample_sd':float(counts.std(ddof=1)),
        'data_origin':'Real microscopy: David Root / CellProfiler, CC0; point profiles and photon draws: constructed teaching models'}
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(summary,ensure_ascii=False))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='zh')
    args=parser.parse_args();main(args.output,args.language)
```

## Organize the photographs around a measurement question

Return now to the hydrogel. If the question concerns cell spreading, choose a contrast mode that reveals cell boundaries, retain a common physical pixel scale and define projected area, aspect ratio or another relevant shape measure. If it concerns increased protein abundance, choose appropriate label controls, unsaturated intensities and consistent background handling, then specify whether the comparison is per cell, per unit area or per specimen. If it concerns cell penetration into the material, acquire depth-dependent information and inspect loss of visibility with depth. Instrument settings follow the question, and the meaning of an image changes with that choice.

A useful acquisition record explains how the specimen was prepared, where images were collected, how illumination reached it, how the camera recorded it, how pixels map to distances and how numbers were processed. Keep original images, numerical result tables and presentation figures as separate outputs with linked identities. Raw images preserve the measurement, tables support comparisons, and display figures explain the relevant structures and analysis locations. Crops can emphasize detail while an overview preserves context. Plots comparing the same quantity benefit from common scales, with error bars identified as between-specimen variability, between-cell variability or measurement uncertainty according to what was actually calculated.

Consider a final example. Cells in group B appear twice as bright as group A, but group B was also recorded with twice the exposure time. If the detector is linear and background and bleaching are controlled, the first task is to account for exposure and background before discussing label abundance. If group B contains large saturated regions, it should be acquired again within a suitable range. This judgment requires no advanced mathematics. It follows the entire measurement chain: the specimen emits light, optics collect a fraction of it, the camera encodes a signal, and the analysis converts that signal into a quantity that answers the biological or materials question.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/I01.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Nikon MicroscopyU — Numerical Aperture](https://www.microscopyu.com/microscopy-basics/numerical-aperture)

   Understand the light cone, refractive index and numerical aperture.
2. [Nikon MicroscopyU — Introduction to Fluorescence Microscopy](https://www.microscopyu.com/techniques/fluorescence/introduction-to-fluorescence-microscopy)

   Excitation–emission separation, filters and the history of Stokes.
3. [Introduction to Bioimage Analysis — Blur & the PSF](https://bioimagebook.github.io/chapters/3-fluorescence/2-formation_spatial/formation_spatial.html)

   Continue with point-spread functions and their effects on measurements.

   Book original content CC BY 4.0; linked reading.
4. [Introduction to Bioimage Analysis — From photons to pixels](https://bioimagebook.github.io/chapters/3-fluorescence/1-formation_overview/formation_overview.html)

   Connect photons, detectors and digital pixels.

   Book original content CC BY 4.0; linked reading.
5. [scikit-image — human_mitosis dataset](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.human_mitosis)

   Identity and CC0 license of the real image.

   Image copyright David Root, CC0.
6. [scikit-image — Segment human cells in mitosis](https://scikit-image.org/docs/stable/auto_examples/applications/plot_human_mitosis.html)

   Examine relationships among thresholds, touching nuclei and counting.
7. [Robert Hooke — Micrographia, 1665 / Wellcome Collection](https://wellcomecollection.org/works/apmaw56u)

   Consult the historical work linking observation and illustration.

   Digitized work marked Public Domain by Wellcome Collection.
