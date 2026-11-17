# Confocal microscopy: Revealing a specimen one optical section at a time

Source: https://ml-biomat.com/tutorials/experimental-methods/i02/en/
Language: en

Understand three-dimensional measurement through pinholes and optical sections, then explore depth, projections and volume in a real tissue stack.

## Are cells on the material surface or already inside it?

Imagine culturing cells in a porous scaffold and obtaining a fluorescence image filled with bright spots. It is tempting to conclude that cells occupy the entire scaffold. A two-dimensional image, however, may combine signals from the top surface, the interior and the bottom. Locating the cells requires information along depth. Confocal microscopy selects a relatively thin optical layer from a specimen and records different depths separately, allowing them to be organized into a three-dimensional image. It can help investigate cell penetration into hydrogels, protein distributions in tissue and the arrangement of beads within a material. Suitable reflected signals can also support materials-surface applications.

Optical sectioning can be compared to reading one sheet within a stack of transparent drawings. Looking through the whole stack superimposes all the lines; selectively recording one sheet makes its structures easier to distinguish. Confocal imaging does not physically cut the tissue. Instead, the illumination position and the detection aperture work together to select light. The recorded section still has a finite thickness, rather than being a mathematical plane with zero thickness. This distinction helps explain why a cell can appear in several consecutive images without becoming several cells, and why the spacing between recorded planes is different from the microscope's axial resolution.

The main benefit of three-dimensional data is preservation of spatial relationships. Red and green features that overlap in a projection may lie at different depths. A tube that appears interrupted in one plane may continue in the next. Reading a volume therefore extends familiar two-dimensional inspection in three directions: examine outlines within a horizontal plane, follow continuity through depth, and use vertical sections to check relative positions. This chapter uses a real confocal mouse-kidney dataset to demonstrate that process. An interactive slice viewer makes it possible to examine why an attractive maximum-intensity projection provides a useful overview while the original stack remains necessary for spatial interpretation.

## Why can a pinhole select depth? Minsky's double-focusing idea

Minsky's microscopy-apparatus patent, filed in 1957 and granted in 1961, connected point illumination, scanning and pinhole detection. The underlying motivation included observing complex biological structures such as neural tissue, where signals from different depths obscure the region of interest. The historical design moved the specimen across a small illuminated point and organized detector signals into an image according to their positions. In common modern laser-scanning confocal instruments, scanning optics move the beam while the specimen remains relatively stationary. Improvements in light sources, detectors and digital recording have made this spatial-selection principle more practical for routine imaging.

![Original pinhole-detection schematic: in-focus green light converges near the aperture, while more defocused red light is blocked. Historical connection: Minsky’s microscopy apparatus, filed 1957 and granted 1961. This is a not-to-scale explanation of conjugate detection.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/0bb8a2177d5fa549b4f2cbec.svg?v=0bb8a2177d5f)

Figure 1Original pinhole-detection schematic: in-focus green light converges near the aperture, while more defocused red light is blocked. Historical connection: Minsky’s microscopy apparatus, filed 1957 and granted 1961. This is a not-to-scale explanation of conjugate detection.

Follow the green rays in the diagram. Light from a point in the focal plane is brought by the detection optics to a relatively compact spot in a corresponding image plane. A pinhole at that position transmits a substantial fraction of this light to the detector. Light originating above or below the focal plane generally forms a less concentrated distribution at the pinhole plane, so a larger fraction falls outside the opening and is blocked. The illuminated location and the location selected by the detection system correspond to one another. This conjugate relationship is the essential meaning of “confocal.” The pinhole selects a spatial distribution of light rather than identifying depth from its color.

This selection changes the balance of useful signal and background. Widefield imaging collects light from a relatively large area simultaneously and can be efficient for thin specimens. In thick fluorescent specimens, out-of-focus contributions also enter the image and produce haze. Confocal detection rejects part of that contribution, improving the visibility of structures near a selected depth. A smaller pinhole usually provides a thinner optical section but transmits fewer useful photons. Opening the pinhole increases signal while accepting more out-of-focus light. Pinhole selection therefore depends on specimen brightness, thickness and the quantity being measured, rather than on a rule that the smallest opening is always best.

Instruments often express pinhole size in Airy units. One Airy unit relates to the diameter of the Airy pattern for a specified wavelength and optical magnification, providing a relative description of the aperture. It is neither a universal number of micrometers nor the thickness of an optical section inside the specimen. In multichannel imaging, different wavelengths mean that the same physical pinhole can correspond to different numbers of Airy units. Comparing spatial distributions across channels requires attention to actual section thickness, registration and intensity range, rather than checking only whether the software displays the same numerical aperture setting for each channel.

## From a picture to a volume: pixels, voxels and slice spacing

A two-dimensional image contains pixels. When images at different depths are arranged in order, each location represents a small volume element, or voxel. The order of axes must be explicit; otherwise a program might treat color channels as depth. The source file here contains 16 depths, three channels and 512×512 pixels per plane. The program organizes these into the order depth, channel, vertical position and horizontal position. The distributed calibration gives 1.24 μm lateral spacing and 1.25 μm axial spacing. Although those sampling intervals are similar, optical resolution may still differ laterally and axially. Voxel geometry and PSF geometry describe different parts of the measurement.

$$
z_k=z_0+k\Delta z,\qquad H_{\mathrm{centers}}=(N_z-1)\Delta z
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/216c15b93ccea50c6180bd15.svg) | Depth coordinate of slice-center k, μm. |
| ![Formula](https://ml-biomat.com/static/agent-math/b72465f81bed2e150afe1243.svg) | Reference coordinate of the first slice center, μm; zero here. |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | Zero-based slice index; dimensionless integer. |
| ![Formula](https://ml-biomat.com/static/agent-math/d6e29d9ed67cc12345806818.svg) | Distance between neighboring slice centers, μm; 1.25 μm here. |
| ![Formula](https://ml-biomat.com/static/agent-math/153b6f53bc559dec1e89fd5d.svg) | Number of recorded planes; dimensionless integer, 16 here. |
| ![Formula](https://ml-biomat.com/static/agent-math/dbbb3310c3c3b526400e3f5f.svg) | Distance between the first and last slice centers, μm. |

Slice 15 is at 0+15×1.25=18.75 μm. Sixteen planes contain 15 center-to-center intervals; the corresponding voxel-cell extent is 16×1.25=20 μm. These definitions serve different calculations.

The center of the first plane is assigned depth zero. The center of plane 15 is consequently at 18.75 μm, because 15 intervals separate plane 0 from plane 15. Treating all 16 planes as sampling cells of thickness 1.25 μm instead gives a total voxel extent of 20 μm. One quantity is the distance between the first and last sampling centers; the other is the thickness used when adding voxel volumes. Both definitions are useful if used consistently. A report should not silently exchange the number of planes with the number of intervals when moving between a depth plot and a volume calculation.

Axial spacing should reflect the information that needs to be retained. A structure that changes rapidly with depth may be missed when planes are far apart, much as important passages can be skipped when reading every tenth page of a book. Smaller spacing increases sampling density but does not itself make the optical section thinner. It can produce many strongly overlapping measurements and increase acquisition time and light exposure. Measuring the axial PSF with suitable subresolution beads, consulting the instrument's sampling guidance and considering the intended analysis provide a sounder route to spacing selection. Preserve original spacing in the data rather than supplying only an interpolated volume that appears smoother.

The four real slices below use the same display mapping and spatial scale. Follow one bright outline from the first plane to plane five, then examine whether it shifts, broadens or divides at later depths. The coordinates are referenced to the same starting plane, so these differences describe spatial location rather than a time sequence. A stack is nevertheless usually acquired sequentially. In a living specimen, movement during that acquisition can mix temporal changes with apparent spatial differences. The duration of the stack should therefore be considered alongside the speed of the biological process, especially when interpreting a thin protrusion, a moving vesicle or a changing cell boundary.

![Real confocal mouse-kidney data, channel two at planes 0, 5, 10 and 15. All use a display range of 0–3000 digital numbers and the same physical calibration. Data: Genevieve Buckley / Monash Micro Imaging, via scikit-image, CC0. Interpret brightness with tissue distribution, optical propagation and acquisition conditions.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/e3bab31e470f0fdf8eb5a05a.svg?v=e3bab31e470f)

Figure 2Real confocal mouse-kidney data, channel two at planes 0, 5, 10 and 15. All use a display range of 0–3000 digital numbers and the same physical calibration. Data: Genevieve Buckley / Monash Micro Imaging, via scikit-image, CC0. Interpret brightness with tissue distribution, optical propagation and acquisition conditions.

A voxel display may also distort shape when software stretches all array axes to the same visual length. A volume with 16 depth planes and 512 lateral samples is physically thin in the depth direction for the spacing used here. Enlarging that axis can make internal variation easier to inspect, but then the display should identify the stretch. Measurements must still use physical coordinates. A sphere should not become elongated simply because the number of recorded planes differs from the number of pixels across an image. Checking the dimensions before rendering is an effective way to catch axis-order and calibration mistakes early.

## Scanning time, photon counts and specimen condition determine settings together

A laser-scanning system records successive positions, with the time spent at one position called pixel dwell time. A longer dwell usually collects more photons. Larger images, repeated averaging and sequential channels also extend the acquisition. A simple multiplication reveals the main cost: a 512×512 image with a dwell of 2 μs and two averages takes approximately 1.05 s of ideal scanning. Sixteen planes and three entirely sequential channels take about 50.3 s. Real instruments also need flyback, focus movement, switching and readout. The calculation explains the dominant contributions; actual time stamps remain the appropriate record of when measurements were made.

$$
t_{\mathrm{frame}}\approx N_xN_y\tau N_a,\qquad t_{\mathrm{stack}}\approx t_{\mathrm{frame}}N_zN_c
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9726e175d28ec5900e7f53a8.svg) | Ideal scan time for one plane and one channel, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/1146e9e5c5b8032680acc2c1.svg) | Horizontal and vertical pixel counts; dimensionless integers. |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | Pixel dwell time per pass, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/41233129fdcf45a3b022217c.svg) | Number of repeated averages per location; dimensionless integer. |
| ![Formula](https://ml-biomat.com/static/agent-math/34b25718fdbd7276f8f56589.svg) | Ideal time for the complete sequential stack, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/153b6f53bc559dec1e89fd5d.svg) | Number of depth planes; dimensionless integer. |
| ![Formula](https://ml-biomat.com/static/agent-math/bfeaf6f059c8ef7165e8b680.svg) | Number of channels when all are acquired sequentially; dimensionless integer. |

512×512×2×10⁻⁶×2=1.048576 s; multiplying by 16 planes and three channels gives about 50.33 s. Flyback, motion and switching overheads are excluded. Simultaneously detected channels do not multiply time in the same way; use acquisition timestamps for actual durations.

This timing affects biological interpretation. If a structure moves substantially within tens of seconds, the whole stack is not a simultaneous three-dimensional snapshot. Reducing irrelevant field area or unnecessary planes can bring acquisition speed closer to the process of interest. A different scanning method may also be appropriate. Spinning-disk confocal systems use many pinholes to collect different positions in parallel and can be useful for faster live-cell acquisition. Their aperture layout, scattering behavior and channel arrangements involve their own tradeoffs. The relevant question is how quickly the required spatial information must be recorded, rather than how detailed a single static image can look.

Averaging suppresses random fluctuations but also repeats illumination. Fluorophores can bleach, and living cells can change under light exposure. Higher laser power and longer dwell therefore do not always provide more useful evidence. On representative specimens, establish an unsaturated setting that makes the target interpretable, then inspect whether signal and morphology remain stable over repeated acquisitions. Detector gain amplifies an electronic signal; it does not add photons that were never detected. For comparisons, retain laser power, gain, dwell time, averaging mode and pinhole conditions as an interconnected set of acquisition parameters. Their combined effect matters more than any isolated number.

Mounting should preserve the three-dimensional structure of interest. Pressing a coverslip onto a soft gel or tissue can flatten it, creating an apparent height difference during preparation. Suitable spacing supports, chambers and objective working distance give the specimen room. Refractive-index mismatch can alter the PSF with depth, while scattering and absorption reduce deep signals. A darker interior therefore calls for consideration of label distribution, light propagation and detection conditions together. A reference with a known spatial distribution or observation from another direction can help distinguish these effects. The interpretation should connect the chosen calibration to the actual specimen geometry and optical path.

Multichannel acquisition also requires separation of spectral spillover from genuine colocalization. A dye with broad emission can send photons into more than one detection window, making a singly labeled specimen bright in two channels. Single-label controls reveal this contribution, while unstained controls help identify autofluorescence from tissue or material. Sequential excitation reduces some mixing associated with simultaneous illumination but does not automatically remove overlap between emission windows. Multicolor beads can additionally test spatial registration across wavelengths. Planning these controls with the labeling experiment provides a clearer explanation than guessing the origins of colors in a final merged image.

## What happens when a three-dimensional stack is compressed into one image?

A maximum-intensity projection selects the largest value along depth at each lateral position. It gathers bright features from different planes into one view and is useful for browsing fluorescent networks or locating sparse targets. A mean projection averages all planes at each lateral position and describes the average signal through that recorded depth range. Both retain lateral coordinates while discarding the depth associated with the contributing signal. Structures that appear adjacent or intersecting in a maximum projection may be separated in three dimensions. Questions about contact, colocalization or connectivity therefore require a return to slices or orthogonal views.

$$
P_{\max}(x,y)=\max_k I(x,y,k),\qquad P_{\mathrm{mean}}(x,y)=\frac1{N_z}\sum_{k=0}^{N_z-1}I(x,y,k)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dea8a18a2088323ea180fbb9.svg) | Raw intensity at lateral position (x,y) in slice k, in digital numbers; positions may be pixel indices or calibrated coordinates. |
| ![Formula](https://ml-biomat.com/static/agent-math/e4974840e693fae46f1e9926.svg) | Horizontal and vertical positions in the image plane; plots here use μm. |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | Depth-plane index starting at zero; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/153b6f53bc559dec1e89fd5d.svg) | Number of projected planes; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/842117f33e02cf9f7b56a727.svg) | Maximum-intensity projection, digital numbers. |
| ![Formula](https://ml-biomat.com/static/agent-math/36b205260ddb2b37d4ffbb56.svg) | Mean-intensity projection, digital numbers. |

For intensities 10, 20, 100 and 30, the maximum is 100 and the mean is 40. The maximum selects one value; summation divided by plane count gives the mean. Both operations remove the depth distribution at that lateral position.

For a simple example, suppose four planes at one lateral position contain intensities 10, 20, 100 and 30. The maximum projection is 100 and the mean projection is 40. Adding another bright structure may increase the maximum, which still remains a single number. Maximum projection can also preserve an isolated high noise value; mean projection can dilute a thin feature present in very few planes. Choose a projection according to whether the goal is visibility of structures, average signal or a distribution at a particular depth. Different brightness after applying two projection rules to the same data reflects the rules, not a physical change in the sample.

![Different views of the same real stack. A and B compare maximum and mean projections on a common display scale. C shows plane means across depth for each channel; channel intensities are not directly molecular abundance ratios. D uses a fixed analysis volume to show the fraction of channel-two voxels above threshold.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/6dd31f7aa51841c03e4def22.svg?v=6dd31f7aa518)

Figure 3Different views of the same real stack. A and B compare maximum and mean projections on a common display scale. C shows plane means across depth for each channel; channel intensities are not directly molecular abundance ratios. D uses a fixed analysis volume to show the fraction of channel-two voxels above threshold.

The maximum and mean projections shown here share a display range, so their visual difference follows directly from the operation. The depth profiles separately calculate plane-mean digital values for the three channels. Dyes, detection efficiencies and acquisition settings may differ between channels, so the profiles help inspect within-channel changes across depth. Their absolute values are not automatically molecular abundance ratios across channels. If one profile decreases deeper in the specimen, examine morphology, background and reference signals before deciding whether the cause is biological distribution or optical attenuation. The curve summarizes where values change along depth, while slices reveal the structures responsible for that change.

Volume rendering transforms voxel values into surfaces, translucent clouds or colored volumes. These representations make spatial relationships easier to see, while their appearance depends on thresholds, opacity and interpolation. A smooth surface can be created by connecting discrete samples during rendering; its visual smoothness does not establish equally fine optical detail. A useful presentation can pair an overview rendering with orthogonal sections carrying physical coordinates and a clear segmentation rule. Readers then gain a spatial impression while retaining a route back to the signal that defines a boundary or void. The choice of rendering becomes part of the explanation rather than a substitute for it.

Deconvolution uses a PSF model to redistribute spread-out signal toward its estimated origins. Unlike a contrast adjustment, it makes explicit assumptions about image formation. A PSF that does not match the instrument, wavelength or imaging depth, or an image with saturation or insufficient sampling, can produce ringing or unstable apparent details. Retain the original stack, state how the PSF was obtained and how iteration was stopped, and check recovery with a suitable known structure or bead specimen. Understanding slices, projections and physical calibration first makes it easier to identify what deconvolution changes and which information was already present.

## Volume comes from calibrated voxels and a defined object

The most direct way to calculate volume is to identify the voxels belonging to a target and add their physical volumes. One voxel's volume is the product of horizontal spacing, vertical spacing and axial spacing. Here that value is approximately 1.922 μm³. A target containing 1,000 selected voxels therefore occupies approximately 1,922 μm³ under this segmentation. The biological meaning follows from the selection rule. If the rule is simply “channel-two intensity above 1,000,” the result is a volume of signal above that threshold. Interpreting it as cell volume, lumen volume or a specific protein structure requires checking which object that rule actually selects.

$$
V=N_{\mathrm{mask}}\Delta x\Delta y\Delta z,\qquad f=\frac{N_{\mathrm{mask}}}{N_{\mathrm{ROI}}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | Total volume of selected voxels, μm³. |
| ![Formula](https://ml-biomat.com/static/agent-math/aa0d04a4648049d3ba42d047.svg) | Number of voxels satisfying a fixed segmentation rule; dimensionless integer. |
| ![Formula](https://ml-biomat.com/static/agent-math/ec9221cb3cb38bb1f2a7546d.svg) | Voxel spacings in three directions, μm; 1.24, 1.24 and 1.25 here. |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | Selected fraction of the analysis region; dimensionless, multiplied by 100 for percent. |
| ![Formula](https://ml-biomat.com/static/agent-math/87d0002d8eeb12cf9a4e12cc.svg) | Total voxel count in the fixed region of interest (ROI); dimensionless integer. |

One voxel occupies 1.24×1.24×1.25=1.922 μm³; 1,000 voxels occupy 1,922 μm³. This assumes a consistent rule, uniform voxel sizes and a fixed denominator. Segmentation checks establish the relationship between above-threshold signal volume and a particular biological object.

The program sweeps thresholds from 500 to 2,000 and plots the proportion of the complete analysis volume that qualifies. As a fixed threshold increases, the selected voxel set can only stay the same or shrink. This provides a simple independent calculation check. A fraction that rises under a higher threshold suggests a changed mask, altered denominator or additional processing that differs across the sweep. Here the denominator is always every voxel in the same channel and 16-plane field. If the question concerns the fraction within tissue, establish a fixed tissue mask first and use its voxels as the denominator, distinguishing whole-field fraction from within-tissue fraction.

Objects reaching the image boundary may be truncated. A comparison of complete-cell volumes requires a predefined treatment of truncated objects. A measurement of signal fraction within a fixed spatial window can still include the parts that lie inside it. These questions have different analysis units and need not use the same exclusion rule. Touching cells can also merge into one three-dimensional connected component. Object counting may require nuclear information, a three-dimensional distance transform and checked segmentation rather than division of total signal volume by an assumed average cell volume. The analysis should retain enough object identity to trace an unusual measurement back to the source image.

Replication and variability should preserve the same hierarchy. Sixteen slices belong to one tissue stack; recording more planes improves spatial sampling but does not create 16 independent tissue specimens. Calculate fractions for multiple independently prepared samples when comparing sample-level behavior. Within one specimen, a depth profile can instead describe internal spatial variation. Threshold-related uncertainty can be explored by showing results across a justified threshold interval and including representative boundary overlays. That information identifies robust structures and details that depend more strongly on processing choices without confusing parameter sensitivity with biological variation among independent specimens.

The volume formula also gives a useful dimensional check. Multiplying three distances produces cubic micrometers, whereas counting foreground pixels in a projection gives a projected area after multiplication by two lateral spacings. Multiplying that projected area by the full stack thickness assumes that every selected lateral column is completely filled, which is generally different from adding the occupied voxels. A thin branching network may have a large projected footprint while occupying a small fraction of the stack. Keeping projected area, occupied volume and enclosing volume as distinct quantities prevents this geometric assumption from being hidden in an apparently simple calculation.

## Move through the real sections and rerun the complete analysis

The interactive viewer uses channel two from the same real kidney dataset. Moving the depth slider switches among the 16 sampled planes. Maximum and mean projection modes show what happens when depth is compressed. All views share the same display mapping, so automatic contrast adjustment does not conceal changes in signal. The images are reduced for convenient browsing, while numerical summaries use complete 512×512 planes. Choose a bright outline, follow the planes in which it appears and compare its relationship to nearby structures in the projection. This small exercise makes the distinction between two-dimensional overlap and three-dimensional position tangible.

## Explore a real confocal stack

Channel two, fixed display range of 0–3000 digital numbers. Preview images are reduced to 256×256; numerical means use original 512×512 planes. Data: Genevieve Buckley / Monash Micro Imaging, CC0.

![Real confocal kidney image](https://ml-biomat.com/static/tutorials/experimental-methods/figures/5766842ea164cc2bb0927907.png?v=5766842ea164)

Field width 635 μm; grayscale display.

The complete Python program reads the bundled original TIFF offline, verifies page count and array shape, and organizes the data as depth, channel, vertical position and horizontal position. It then generates the optical schematic, the four-slice figure and the projection diagnostics; exports plane means and threshold fractions; and saves projection arrays. Voxel volume, the distance between first and last slice centers and ideal scan time can all be checked by hand. Begin by changing the selected channel and examining its depth profile, or by changing the fixed threshold. Preserve the original array and avoid independently stretching each plane if the aim is to compare numerical intensities.

### Complete Python: sections, projections and volume from a real stack

Read the bundled CC0 TIFF, preserve axis order and physical spacing, and export figures, plane-level tables and numerical summaries.

```
"""Confocal microscopy: real optical sections, projections and 3D sampling.

The bundled kidney TIFF is CC0, acquired by Genevieve Buckley,
Monash Micro Imaging (2018), and distributed by scikit-image.
Axes are (z, channel, y, x); spatial steps are 1.25, 1.24, 1.24 um.
"""
from pathlib import Path
import argparse,csv,json
import numpy as np
from PIL import Image,ImageSequence
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse,Rectangle

def load_stack():
    with Image.open(Path(__file__).parent/'data/kidney.tif') as im:
        pages=np.stack([np.asarray(page).astype(np.uint16) for page in ImageSequence.Iterator(im)])
    if pages.shape!=(48,512,512):raise ValueError(f'Unexpected TIFF dimensions {pages.shape}')
    return pages.reshape(16,3,512,512)

def main(output,language):
    output.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','Noto Sans CJK SC','DejaVu Sans'],'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'font.size':11,'axes.titleweight':'bold','text.color':'#243b45','axes.labelcolor':'#243b45','figure.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5'})
    zh=language=='zh';tr=lambda a,b:a if zh else b
    green,blue,red,gray='#168477','#3574a8','#bd624b','#73848a'
    def save(fig,name):
        fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');fig.savefig(output/f'{name}-{language}.png',dpi=140,bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(figsize=(11,6),layout='constrained');ax.set(xlim=(0,12),ylim=(0,7));ax.axis('off')
    ax.set_title(tr('从点照明到针孔检测：共轭平面之间的空间筛选','From point illumination to pinhole detection: spatial selection'))
    for x in [1,2,3]:ax.plot([x,x],[1,4.3],color='#c6d2ce',lw=8,alpha=.65)
    ax.text(.7,5,tr('样品的不同深度','Different specimen depths'))
    ax.add_patch(Ellipse((4.4,2.7),.35,4.3,fc='#d8e8ef',ec=blue))
    ax.text(3.8,5.1,tr('检测光学','Detection optics'))
    for y in [.8,4.6]:
        ax.plot([2,4.4,7.5],[2.7,y,2.7],color=green,lw=2)
        defocused_end=2.7+(2.7-y)*(7.5-6.65)/(6.65-4.4)
        ax.plot([1,4.4,6.65,7.5],[2.7,y,2.7,defocused_end],color=red,lw=1.4,ls='--')
    ax.add_patch(Rectangle((7.4,.3),.25,2.15,fc=gray));ax.add_patch(Rectangle((7.4,2.95),.25,2.2,fc=gray))
    ax.text(6.6,5.4,tr('针孔所在平面','Pinhole plane'))
    ax.add_patch(Rectangle((9,2.1),1.3,1.2,fc='#dde7e3',ec=gray))
    ax.annotate('',(9,2.7),(7.7,2.7),arrowprops={'arrowstyle':'->','color':green,'lw':2})
    ax.text(8.7,3.7,tr('探测器','Detector'));ax.text(8.5,1.5,tr('焦平面光通过\n离焦光大部分被挡住','In-focus light passes\nMuch defocused light is blocked'))
    ax.scatter([2,1],[2.7,2.7],color=[green,red],s=80,zorder=10)
    ax.text(.8,.2,tr('绿色：焦平面；红色虚线：另一深度。光线为原理示意，不按比例。','Green: focal plane; red dashes: another depth. Schematic rays, not to scale.'),fontsize=10)
    ax.text(.8,6.2,tr('1957年申请，1961年授权：明斯基的扫描与双重聚焦构想','Filed 1957, granted 1961: Minsky’s scanning and double-focusing concept'),fontsize=11)
    save(fig,'pinhole')
    stack=load_stack();dz,dy,dx=1.25,1.24,1.24
    volume=stack[:,1].astype(float);z=np.arange(16)*dz
    vmax=3000;extent=[0,512*dx,512*dy,0]
    fig,axes=plt.subplots(2,2,figsize=(10,9),layout='constrained')
    for ax,i in zip(axes.ravel(),[0,5,10,15]):
        im=ax.imshow(volume[i],cmap='magma',vmin=0,vmax=vmax,extent=extent)
        ax.set(xlabel='x / μm',ylabel='y / μm',title=tr(f'层 {i}：z={z[i]:.2f} μm',f'Slice {i}: z={z[i]:.2f} μm'))
    cb=fig.colorbar(im,ax=axes,shrink=.7);cb.set_label(tr('原始数字量，共同显示范围','Raw digital number, common display range'))
    save(fig,'sections')
    projection_max=volume.max(axis=0);projection_mean=volume.mean(axis=0)
    fractions=(volume>1000).mean(axis=(1,2));means=volume.mean(axis=(1,2))
    thresholds=np.arange(500,2001,100);vf=np.array([(volume>t).mean() for t in thresholds])
    fig,axes=plt.subplots(2,2,figsize=(11,9),layout='constrained')
    axes[0,0].imshow(projection_max,cmap='magma',vmin=0,vmax=vmax,extent=extent)
    axes[0,0].set(xlabel='x / μm',ylabel='y / μm',title=tr('A  最大强度投影：保留沿z最亮值','A  Maximum projection: brightest value along z'))
    axes[0,1].imshow(projection_mean,cmap='magma',vmin=0,vmax=vmax,extent=extent)
    axes[0,1].set(xlabel='x / μm',ylabel='y / μm',title=tr('B  平均投影：沿z平均信号','B  Mean projection: average signal along z'))
    for c,color in enumerate([blue,green,red]):
        axes[1,0].plot(z,stack[:,c].mean(axis=(1,2)),'o-',color=color,label=tr(f'通道{c+1}',f'Channel {c+1}'))
    axes[1,0].set(xlabel='z / μm',ylabel=tr('平面平均数字量','Plane-mean digital number'),title=tr('C  各通道沿深度的强度变化','C  Intensity across depth in each channel'));axes[1,0].legend(frameon=False)
    axes[1,1].plot(thresholds,vf*100,'o-',color=green)
    axes[1,1].set(xlabel=tr('阈值 / 数字量','Threshold / digital number'),ylabel=tr('超过阈值的体素比例 / %','Voxels above threshold / %'),title=tr('D  分割结果依赖阈值','D  Segmented fraction depends on threshold'))
    save(fig,'projections')
    nz,nc,ny,nx=stack.shape
    voxel_volume=dx*dy*dz;selected=int(np.count_nonzero(volume>1000))
    summary={'shape_zcyx':[nz,nc,ny,nx],'voxel_volume_um3':voxel_volume,'first_last_center_distance_um':(nz-1)*dz,'voxel_extent_z_um':nz*dz,'threshold':1000,'selected_voxels':selected,'selected_volume_um3':selected*voxel_volume,'selected_fraction':selected/volume.size,'nominal_frame_s':512*512*2e-6*2,'nominal_three_channel_stack_s':512*512*2e-6*2*16*3,'max_projection_mean':float(projection_max.mean()),'mean_projection_mean':float(projection_mean.mean()),'slice_mean_values':means.tolist(),'data_origin':'Real CC0 kidney confocal image, Genevieve Buckley / Monash Micro Imaging, via scikit-image'}
    with (output/'data.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['slice_index','z_um','channel2_mean_digital_number','fraction_above1000']);w.writerows(zip(np.arange(nz),z,means,fractions))
    np.savez_compressed(output/'projections.npz',maximum=projection_max,mean=projection_mean,z_um=z)
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in summary.items() if k!='slice_mean_values'},ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

## Build acquisition and presentation around the three-dimensional question

For cell penetration, first identify a material surface or another reproducible reference and calculate positions relative to it. If the specimen is tilted, instrument z coordinates can mix surface-height changes with penetration. A surface label or geometric fit can provide a relative-depth coordinate. For connectivity of a cellular network within pores, acquire a sufficiently large volume and inspect missing sampling or motion between planes. For enrichment of two proteins in the same region, consider spectral spillover, chromatic alignment, label specificity and the analysis scale. Yellow pixels in a merged projection alone do not establish a molecular interaction.

A coherent result can connect overview and detail: show the specimen and sampling location, use consistently scaled sections to explain depth relationships, and then present the distribution or volume measure that answers the question. Retain objective, wavelengths, pinhole, scan settings, layer spacing, stack range, physical pixel size and processing rules. Keeping the original stack lets collaborators choose different sections instead of receiving only a flattened projection. Once spatial information has been discarded during presentation, prose has little ability to restore it. A compact set of linked views is often more informative than a larger collection of attractive but disconnected renderings.

Use a low-dose preview to establish where the target first appears and disappears, then choose start and end planes with appropriate margins. Substantial target signal in the last plane indicates that the acquisition window may truncate volume or maximum-depth measurements. Extending that window and changing the measurement question are different responses. A common boundary definition across specimens gives depth distributions a comparable reference.

Two final questions test the distinction. First, reducing slice spacing from 1 μm to 0.2 μm makes a rendered surface smoother: has axial optical resolution improved fivefold? Sampling is denser, while the optical PSF needs its own assessment. Second, two channels overlap extensively in a maximum projection: do they occupy the same positions at every depth? Slice-by-slice inspection and orthogonal views address that spatial question. Separating sampling, optical selection and display turns confocal microscopy into a measurement method organized around position, structure and time, with each setting serving a defined part of the investigation.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/I02.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Minsky — US3013467A, Microscopy apparatus](https://patents.google.com/patent/US3013467A/en)

   Historical scanning and double-focusing concept; filing and grant years.

   Historical primary source; original explanatory figure here.
2. [Nikon MicroscopyU — Introductory Confocal Concepts](https://www.microscopyu.com/techniques/confocal/introductory-confocal-concepts)

   Pinhole detection, scanning, conjugate foci and historical development.
3. [Nikon MicroscopyU — Specimen Preparation and Imaging](https://www.microscopyu.com/techniques/confocal/specimen-preparation-and-imaging)

   Mounting, working distance and optical conditions in three-dimensional specimens.
4. [Nikon MicroscopyU — Critical Aspects of Confocal Microscopy](https://www.microscopyu.com/techniques/confocal/critical-aspects-of-confocal-microscopy)

   Acquisition choices, bleaching and multichannel design.
5. [Introduction to Bioimage Analysis — Microscopes & detectors](https://bioimagebook.github.io/chapters/3-fluorescence/4-microscope_types/microscope_types.html)

   Compare widefield, point scanning and spinning-disk acquisition.

   Book original content CC BY 4.0; linked reading.
6. [scikit-image — kidney dataset](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.kidney)

   Dataset identity, channels, physical spacing and CC0 license.

   Image: Genevieve Buckley / Monash Micro Imaging, 2018, CC0.
