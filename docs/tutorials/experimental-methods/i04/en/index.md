# TEM: What electrons reveal after crossing a thin specimen

Source: https://ml-biomat.com/tutorials/experimental-methods/i04/en/
Language: en

Begin with a dark spot and connect thin specimens, projections, diffraction and particle dimensions.

## Is a dark spot a particle, a cavity, or two overlapping objects?

A drop containing nanoparticles can leave many small dark circles on a transmission electron microscopy grid. A researcher may want to know their sizes, whether they aggregate, whether they contain cavities, and how their crystals are arranged. Although these questions seem to ask for one highly magnified photograph, they involve different information. Outlines depend on image contrast, cavities concern material distributed along the beam direction, and crystal arrangement requires diffraction. Asking why a spot appears dark is a useful starting point. Transmission electron microscopy, abbreviated TEM, sends electrons through a sufficiently thin specimen and uses the emerging electrons to form an image or a diffraction pattern.

Shadows provide a familiar introduction to projection. Two leaves at different depths may cast overlapping shadows on a wall, even though the leaves never touch. A single shadow does not reveal their depth separation. TEM likewise maps structures distributed along the beam into a two-dimensional view. Electron scattering and wave interference make its contrast richer than an ordinary shadow, so the analogy explains geometry without reducing every micrograph to a silhouette. This chapter follows the path from electron imaging to specimen preparation, particle measurements and diffraction, then uses a tilt experiment to show how one three-dimensional arrangement produces different apparent relationships in two dimensions.

In biomaterials research, this connects several scales. Inorganic filler dimensions affect dispersion within a polymer, vesicle membranes relate to encapsulation, and ultrathin cell sections reveal organelles and local structures near a material. Before selecting magnification, decide whether the question concerns dried particles, a resin-embedded section, or a frozen hydrated layer. All can be examined by TEM, but they preserve different specimen states through different preparation routes. Matching the target structure to the preparation method gives the resulting image a clear role in the investigation.

## Why electrons can form a magnified image

An optical microscope bends light with glass lenses. An electron microscope controls charged electrons using electric and magnetic fields. An accelerating voltage gives electrons kinetic energy, magnetic lenses bring trajectories together, and later lenses magnify the image. In 1931, early work by Ruska and Knoll demonstrated that successive magnetic lenses could form a magnified electron image. The magnification was modest compared with a modern instrument, but the experiment established an essential engineering possibility: electron beams could support several stages of imaging. Improvements in sources, lenses, vacuum and stability subsequently turned that principle into a practical method for studying very small structures.

Electrons also behave as waves, with wavelength related to momentum. A wavelength is the spatial distance over which a wave repeats. Shorter wavelengths provide a condition for distinguishing smaller structures. Raising the accelerating voltage increases electron momentum and shortens the wavelength. At 200 kV, the wavelength is approximately 2.508 pm, or 0.002508 nm. This is much shorter than visible-light wavelengths, but image resolution also depends on lens aberrations, mechanical and electrical stability, the detector, specimen thickness and beam damage. Wavelength supplies one physical ingredient; the whole imaging chain determines how much information survives in the final image.

$$
\lambda=\frac{h}{\sqrt{2m_e e V\left(1+\frac{eV}{2m_ec^2}\right)}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | Electron wavelength, m; 1 pm=10⁻¹² m. |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | Planck constant, 6.62607015×10⁻³⁴ J·s. |
| ![Formula](https://ml-biomat.com/static/agent-math/250412b4badc287fd481e758.svg) | Electron rest mass, approximately 9.1093837×10⁻³¹ kg. |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | Elementary charge, 1.602176634×10⁻¹⁹ C. |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | Accelerating voltage, V; 200 kV=200000 V. |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | Speed of light in vacuum, 299792458 m/s. |

Charge times voltage gives kinetic energy; the denominator is relativistically corrected momentum. Wavelength is Planck constant divided by momentum. At 200000 V this gives about 2.507934×10⁻¹² m, or 2.508 pm. Initial kinetic energy is taken as negligible relative to acceleration energy.

The relativistic correction in this equation has a practical reason. Electrons at common TEM voltages travel at an appreciable fraction of the speed of light, so a low-speed momentum relation produces a measurable discrepancy. To understand the trend, first inspect the voltage–wavelength curve generated by the example: increasing voltage decreases wavelength. To calibrate diffraction spacings, use the wavelength appropriate to the actual accelerating voltage. Separating these two tasks makes the calculation purposeful. The initial idea is simply that the specimen scatters electron waves; more detailed electron optics can then be introduced as the measurement requires it.

![Original electron-optical and preparation concepts. A connects to magnetic-lens imaging in 1931; B shows a bright-field aperture accepting near-axis electrons and blocking off-axis electrons; C explains how vitrification developed in the 1980s enabled frozen hydrated observation. Schematics are not to scale.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/189d3148c5a91f8ff6cd7cd5.svg?v=189d3148c5a9)

Figure 1Original electron-optical and preparation concepts. A connects to magnetic-lens imaging in 1931; B shows a bright-field aperture accepting near-axis electrons and blocking off-axis electrons; C explains how vitrification developed in the 1980s enabled frozen hydrated observation. Schematics are not to scale.

Electrons emerging from a specimen do not all continue in their original direction. Some are deflected through small angles, others through larger angles, and some transfer energy to the specimen. Bright-field imaging mainly accepts the transmitted beam near the optical axis, so regions that scatter more electrons outside that acceptance can appear darker. Dark-field imaging selects a scattered beam, making regions that contribute to it bright. An aperture acts like a gate for propagation directions: changing its position or size changes which electrons form the image. Interpreting a darker region therefore requires the imaging mode, aperture, thickness and composition, rather than treating gray level as a direct chemical concentration.

## Make the specimen transmissive while preserving the structure of interest

Electrons interact with atoms as they pass through matter. Excessive thickness increases multiple scattering and makes structural information harder to interpret. TEM therefore requires an electron-transparent region, with suitable thickness depending on composition, voltage and the intended observation. Resin-embedded biological sections commonly have thicknesses from several tens of nanometers to around one hundred nanometers, while dense metals or high-resolution lattice imaging can call for different conditions. Thinking of thinness as a condition for electron propagation is more useful than memorizing one thickness for every material. Support films, grids, contamination and thickness variations also influence the usable region.

Dispersed particles are often observed after depositing a drop on a support film. During evaporation, flow, capillary forces and surface interactions can concentrate particles near a droplet edge or produce arrangements different from those in suspension. If the question concerns aggregation in water, connect dried images with a hydrated-state method such as dynamic light scattering or cryo-TEM. If the question concerns an inorganic core's outline, dried TEM can provide direct geometrical information. Dilution, cleaning and dispersion steps can alter the observed population too. Recording them helps explain why nominally identical material appears different on separate grids.

Tissues and cells commonly undergo fixation, dehydration, embedding, ultrathin sectioning and contrast enhancement. Fixation helps retain molecular structures during subsequent processing. Resin provides support for cutting, thin sections permit transmission, and stains containing heavier elements increase scattering differences between selected structures and their surroundings. Each step addresses a specific difficulty while potentially introducing shrinkage, extraction, compression or precipitates. A dark membrane-like boundary should therefore be interpreted as a structure expressed through this preparation and imaging route. Its pixels are not a direct map of every molecule in an untreated living cell.

Negative staining uses a different route: a strongly scattering surrounding layer makes small particles or macromolecular outlines easier to recognize. It is useful for rapid inspection of shape and sample uniformity, although drying, flattening and stain distribution influence the result. Cryo-TEM instead rapidly cools a thin aqueous layer so that water forms vitreous ice without a long-range crystalline lattice, then keeps the specimen cold during observation. Growing ice crystals can rearrange nearby material. Vitrification helps retain hydrated structures by avoiding that large-scale crystallization. Its development during the 1980s addressed the longstanding incompatibility between water-rich biological specimens and the microscope vacuum, becoming a foundation for later cryo-electron microscopy.

Retaining water does not mean that the specimen continues behaving like a culture in a dish. Vitrification immobilizes structures in a frozen state. Film thickness, air–water interfaces, preferred orientation and irradiation still affect the data. Vesicle studies can compare outlines across regions with different ice thickness, while protein studies examine orientation distributions and aggregation. If the question is an inorganic particle's lattice, a complex cryogenic route may not be the most useful choice. If it concerns a hydrated membrane, preparation becomes central to the measurement. Choosing from the information needed gives later interpretation a coherent basis.

## Gray levels carry information about thickness, scattering and orientation

The beam supplies information while also transferring energy to the specimen. Polymers and biological materials can undergo bond breaking, mass loss, shrinkage or bubbling. Some inorganic materials are affected by displacement of atoms, heating or contamination deposition. A feature that changes after repeated focusing may therefore reflect the observation process itself. Focusing partly on a neighboring region, using a planned exposure on the target and comparing early with later images helps distinguish structural information from irradiation-related change. Acquisition order becomes part of the interpretation, instead of attention being restricted to the sharpest image eventually saved.

Reducing exposure also reduces electron counts and makes random variation more conspicuous. The detector converts arriving electrons into digital data; detection efficiency, pixel size, readout and saturation range influence the recorded signal. Dividing a total exposure into short frames can help correct drift, although the corrected detail still needs support from the underlying observations. Comparing early frames with an accumulated image exposes the tradeoff: early frames have less dose but more noise, whereas accumulated frames contain more counts and potentially more irradiation-related change. Longer observation can improve counting while simultaneously altering the object being measured.

This tradeoff matters when comparing treatment groups. If one specimen is fragile and changes rapidly under the beam, repeatedly adjusting conditions until it resembles a more stable specimen can make the images represent different stages of irradiation. Define comparable acquisition conditions or explicitly investigate the evolution with exposure. For a crystalline material, following the persistence of diffraction spots may reveal loss of order; for a vesicle, following outline and projected area may reveal deformation. The appropriate indicator comes from the structure of interest. A matched exposure series then becomes a small, interpretable experiment about stability rather than an accidental collection of images.

For some thin amorphous specimens under comparable conditions, thicker or more strongly scattering regions remove more electrons from bright-field acceptance and can appear darker. This is commonly described as mass–thickness contrast. Here, mass refers to material and scattering strength accumulated along the beam, rather than weighing each image pixel. Thickness, elemental composition and staining can all alter the signal. A solid sphere presents a longer path through its center than near its edge, potentially producing a radial gray-level variation; a hollow shell has a different path-length distribution. Such trends suggest structural interpretations that can be examined through tilting, thickness information or complementary measurements.

Crystals add strong orientation dependence. Their repeated atomic arrangement allows scattered waves to reinforce one another in certain directions, creating diffracted beams. A small tilt can move a grain into or out of a strong diffraction condition and substantially change its bright-field intensity. Two grains with the same composition can therefore appear different in brightness. Diffraction contrast is valuable when studying bending, boundaries or defects. For a simple outline measurement, however, its local variations may complicate threshold segmentation. Recognizing the contrast mechanism helps decide whether a bright or dark variation belongs to the desired measurement.

Lattice fringes in high-resolution TEM also involve phase interference between transmitted and scattered waves. Phase can initially be understood as a wave's position within its cycle: aligned crests can reinforce, while a crest meeting a trough can cancel. Defocus and aberrations change the relative relationships between those waves. Bright or dark dots consequently do not always correspond one-to-one with a particular atom. Establishing atomic arrangements requires imaging conditions, orientation and suitable image simulations. A useful first description is that an image contains periodic fringes with a measured spacing; diffraction and structural knowledge then help determine which planes may produce them.

Processing affects these judgments. Contrast adjustment can reveal weak structures, while saturation discards intensity differences. Smoothing suppresses high-frequency noise but can erase narrow gaps. Sharpening emphasizes boundaries and may create artificial light and dark bands beside them. Keep the raw image alongside presentation versions, and base measurements on data with known calibration and processing. If the measured diameter changes substantially with smoothing strength, the boundary remains dependent on that choice. Return to signal quality, calibration and the segmentation rule rather than repeatedly adjusting the image until the outlines look regular.

## A small tilt can separate objects that overlap in projection

Imagine two spheres, each with a radius of 12 nm. Their centers differ by 16 nm horizontally and 50 nm in depth. Their true center-to-center distance is approximately 52.5 nm, so the spheres are separated in space. Viewed along the initial beam direction, depth collapses into the image plane and the centers appear only 16 nm apart. The radii sum to 24 nm, so their projected outlines overlap. Calling this apparent overlap particle fusion would turn a two-dimensional relationship into an unsupported three-dimensional one. The geometry alone demonstrates the issue without requiring the mathematics of electron waves.

$$
x^{\prime}=x\cos\theta+z\sin\theta,\qquad y^{\prime}=y
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/eeaf78722a7e7f8494b85137.svg) | Original specimen coordinates, nm; z is depth along the initial beam direction. |
| ![Formula](https://ml-biomat.com/static/agent-math/ded7fb3f94b5eed0963dc345.svg) | Coordinates in the projected plane after tilt, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | Tilt about the y axis; use radians in numerical trigonometric functions. |

Rotation mixes lateral and depth components, then projection discards the new beam-direction component. For center differences of 16 nm laterally and 50 nm in depth, a 60° tilt gives 16×0.5+50×0.866025≈51.30 nm. The three-dimensional distance remains √(16²+50²)≈52.50 nm.

![Projections of the same two teaching spheres of radius 12 nm at 0°, 30° and 60°. Their true center distance remains about 52.5 nm, while projected distance changes. Colors distinguish objects rather than elements or real TEM intensity.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/cc2ca1be4c4a55877452e0e6.svg?v=cc2ca1be4c4a)

Figure 2Projections of the same two teaching spheres of radius 12 nm at 0°, 30° and 60°. Their true center distance remains about 52.5 nm, while projected distance changes. Colors distinguish objects rather than elements or real TEM intensity.

Tilting changes the direction from which the same spatial arrangement is viewed. When rotation is about the vertical axis, both the original horizontal coordinate and depth contribute to the new horizontal projection. For these two spheres, a 30° tilt gives a projected center separation of about 38.9 nm, while 60° gives about 51.3 nm. The overlap disappears. A genuine connecting neck should instead produce a compatible geometrical relationship across suitable directions. Two or three views can already test a simple overlap explanation. A full three-dimensional reconstruction requires more angles, alignment and an appropriate reconstruction model.

Electron tomography combines a series of tilted projections to recover three-dimensional structure. One can imagine collecting many shadows around an object, then finding a shape that explains them together. In practice, holder geometry and obstruction commonly limit accessible angles. The absent range produces a missing wedge of information, weakening reconstruction along certain directions and potentially elongating objects. Tilting also increases the effective path through the specimen and accumulates irradiation. Angular coverage, thickness, drift correction and dose allocation therefore jointly affect reconstruction quality. A visually convincing volume rendering is most informative when these acquisition properties remain connected to it.

The interactive experiment retains the spheres' three-dimensional coordinates while allowing changes in tilt and depth separation. It displays the projection together with true center distance, projected center distance and an overlap indicator. First set depth separation to zero, then increase it while viewing at 0°. Notice how similar the projected outlines can remain. Rotate the viewing direction and observe the hidden difference becoming visible. Colors identify the two teaching objects; they do not encode elements or electron density. The experiment isolates projection geometry, while a complete TEM intensity model would additionally include scattering and interference.

## Tilt two spheres to expose hidden depth

Radius 12 nm; lateral center separation 16 nm. Colors track objects; the display models projection geometry.

[Figure: Projection of two spheres](https://ml-biomat.com/tutorials/experimental-methods/i04/en/#I04-plot)

## A diffraction pattern records periodicity rather than object position

In imaging mode, a location in the image corresponds to a location in the specimen. In diffraction mode, pattern position mainly represents scattering direction. Periodically arranged atoms reinforce scattered waves in directions where their phases match, creating spots or rings. A crystal with a relatively uniform orientation commonly produces discrete spots; many differently oriented small crystallites can produce rings; disordered material often contributes broad diffuse scattering. These are characteristic tendencies rather than a complete classification from one feature. Thickness, texture and the selected region also shape the measured pattern and belong in its interpretation.

Selected-area electron diffraction uses an aperture in an image plane to define the contributing specimen region, then changes lens settings to project the diffraction plane onto the detector. This connects a region's morphology with its crystallographic information. A ring farther from the center represents a larger scattering angle. Under the small-angle approximation, a larger ring radius corresponds to a smaller lattice-plane spacing. The apparent reversal relative to ordinary images occurs because diffraction expresses reciprocal spatial scales. Distinguishing specimen coordinates from scattering coordinates prevents a ring diameter from being mistaken for a particle diameter.

$$
rd\approx L\lambda,\qquad d\approx\frac{L\lambda}{r}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | Radius from the transmitted spot to a diffraction ring, mm here. |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | Lattice-plane spacing, nm here. |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Effective camera length calibrated with a reference, mm here. |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | Electron wavelength at the accelerating voltage, nm here. |

This camera-constant relation applies at small scattering angles. Use the same length unit for L and r, and the same for d and λ. At 200 kV, λ≈0.002507934 nm; with L=500 mm and d=0.25 nm, r≈5.015868 mm.

For 200 kV electrons and an effective camera length of 500 mm, a 0.25 nm spacing gives a ring radius of approximately 5.016 mm. The camera length is an effective optical quantity determined by the lens system and calibrated with a known standard. It is not simply a distance measured from specimen to camera with a ruler. One ring or fringe spacing supplies candidate structural information; phase identification should compare several reflections, their relative positions, allowed reflections and composition. For a multiphase specimen, retain the selected-area location and ring measurements, then use additional evidence to distinguish contributions.

Particle size, grain size and coherent diffraction-domain size also describe different objects. One particle may contain several grains with different orientations, while defects within a grain can shorten the extent over which periodic scattering remains coherent. An outline measurement describes projected geometry. Diffraction broadening concerns coherent periodic structure together with other broadening mechanisms. Define both quantities before comparing them in a table. Their difference can then reveal internal organization instead of prompting an immediate search for one supposedly correct size. This distinction becomes useful when TEM is combined with X-ray diffraction or solution-based size measurements.

## Turn particle outlines into an interpretable size distribution

A noncircular outline can be described by several lengths. The longest distance emphasizes elongation, a minor axis describes transverse width, and the equivalent-circle diameter assigns the diameter of a circle with the same projected area. The last definition converts a complex outline into a comparable number while discarding some shape information. A disk and a slender rod can have the same equivalent-circle diameter. Depending on the question, retain an aspect ratio or representative shape images alongside it. Defining diameter before discussing an average gives comparisons between instruments and specimens a clear meaning.

$$
d_{\mathrm{eq}}=2\sqrt{\frac{A}{\pi}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Calibrated particle projected area, nm². |
| ![Formula](https://ml-biomat.com/static/agent-math/636f64febcd4b6a8b2831455.svg) | Diameter of a circle with the same area, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | Pi, approximately 3.14159265; dimensionless. |

A circle has area π times radius squared. Invert that relation for radius and multiply by two. An area of 314.159 nm² gives approximately 20 nm. This describes an equal-area circle rather than restoring aspect ratio or three-dimensional volume.

Before measuring, establish pixel calibration, boundary rules and how touching objects will be treated. An object cut by the image edge has an underestimated area, while overlapping particles merged into one region may have an overestimated single-particle area. One possible rule excludes truncated objects from individual-area statistics and records aggregation separately. For overlaps that cannot be separated reliably, examine sparser regions or obtain additional views. Apply the same rules across specimen groups. Otherwise, a comparison may measure isolated particles in one group and entire clusters in another while labeling both results particle diameter.

The teaching example contains ten diameters: 18, 19, 20, 20, 21, 22, 23, 25, 27 and 35 nm. Each particle receives one vote in the number average, giving 23.0 nm. Area weighting gives large particles progressively greater influence because projected area scales with diameter squared, so the weighted mean rises. The two averages answer different questions: what size belongs to a randomly selected particle, and what particle size is more likely to contribute a randomly selected piece of projected area? Comparison with dynamic light scattering additionally requires attention to intensity weighting, hydration and inversion models, beyond placing software-reported mean diameters side by side.

![Teaching calculations generated by the complete code. A gives relativistically corrected electron wavelengths. B gives ring geometry at 200 kV and 500 mm effective camera length. C and D use the same ten specified particles to compare number distributions and differently weighted means.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/1aa7b338af9a9d225e45821a.svg?v=1aa7b338af9a)

Figure 3Teaching calculations generated by the complete code. A gives relativistically corrected electron wavelengths. B gives ring geometry at 200 kV and 500 mm effective camera length. C and D use the same ten specified particles to compare number distributions and differently weighted means.

A large particle count still has a sampling hierarchy. Hundreds of particles in one image describe that field. Variations between regions, grids or independent preparations require corresponding sampling. Begin with low-magnification location information, select fields according to a predefined rule, and retain the prevalence of dispersed and aggregated regions. Present representative images, measurement definitions, object count and independent specimen count together. This reveals which level of variation the result describes. A small tail of large particles or clusters can matter for a nanomaterial's later use, making the full distribution more informative than one average alone.

## Connect images, geometry and structure through reproducible calculations

The complete program generates three bilingual figures: electron imaging and vitrification concepts; three projections of the same sphere pair; and a four-panel comparison of electron wavelength, diffraction rings and size statistics. Geometries and particle dimensions are explicitly specified teaching data. The program exports diameters, projected areas and area weights in a table. Change depth separation to see how projected outlines respond, or replace the 35 nm particle with a 25 nm particle and compare the change in number-weighted and area-weighted means. These controlled changes turn abstract measurement definitions into visible numerical consequences.

### Complete Python: projections, diffraction rings and size distributions

All teaching objects are explicitly defined; export bilingual figures, particle tables and checkable numerical results.

```
"""TEM teaching experiment: projection ambiguity, calibration and diffraction.

All images and particle coordinates here are constructed teaching models.
Projection maps describe geometry, not a full coherent electron-optical simulation.
"""
from pathlib import Path
import argparse,csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Ellipse,Circle

def wavelength(voltage):
    h,e,m,c=6.62607015e-34,1.602176634e-19,9.1093837139e-31,299792458.
    return h/np.sqrt(2*m*e*voltage*(1+e*voltage/(2*m*c*c)))

def main(output,language):
    output.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'svg.fonttype':'none','font.size':11,'axes.titleweight':'bold','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','text.color':'#243b45','axes.labelcolor':'#243b45'})
    tr=lambda a,b:a if language=='zh' else b
    green,blue,red,gray='#168477','#3474a8','#bd624b','#788b90'
    def save(fig,name):
        fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');fig.savefig(output/f'{name}-{language}.png',dpi=140,bbox_inches='tight');plt.close(fig)
    fig,axes=plt.subplots(1,3,figsize=(13,6),layout='constrained')
    for ax in axes:ax.axis('off');ax.set(xlim=(-3,3),ylim=(0,10))
    ax=axes[0];ax.set_title(tr('A  1931：磁透镜形成放大像','A  1931: magnetic-lens magnification'),fontsize=12)
    for y,label in [(8.8,tr('薄样品','Thin specimen')),(6.4,tr('物镜','Objective lens')),(3.8,tr('投影系统','Projector system')),(1,tr('探测器','Detector'))]:
        ax.add_patch(Rectangle((-1.4,y-.12),2.8,.24,fc=gray if y>8 else '#a9c6d1',ec=gray));ax.text(0,y+.4,label,ha='center')
    for dx in [-.9,0,.9]:ax.plot([.5,dx,-.5*1.4/2.4],[8.8,6.4,5],color=blue,lw=1.5)
    for dx in [-1,0,1]:ax.plot([-.5*1.4/2.4,dx,.5*1.4/2.4*2.8/1.2],[5,3.8,1],color=blue,lw=1.5)
    ax.text(0,.1,tr('原创电子光路概念图；不按比例','Original electron-optical concept; not to scale'),ha='center',fontsize=9)
    ax=axes[1];ax.set_title(tr('B  选择电子，改变图像对比','B  Select electrons, change contrast'),fontsize=12)
    ax.add_patch(Rectangle((-2,7),4,.3,fc='#ccbda9'));ax.text(0,8,tr('薄片散射电子','Thin section scatters electrons'),ha='center')
    ax.annotate('',(0,2),(0,7),arrowprops={'arrowstyle':'->','color':green,'lw':2})
    for end in [-1.14,1.14]:ax.annotate('',(end,4.15),(0,7),arrowprops={'arrowstyle':'->','color':red,'lw':2})
    ax.add_patch(Rectangle((-2.7,3.9),2.2,.25,fc=gray));ax.add_patch(Rectangle((.5,3.9),2.2,.25,fc=gray));ax.text(0,4.6,tr('物镜光阑','Objective aperture'),ha='center')
    ax.text(0,.7,tr('明场：主要接收近轴透射束\n散射、厚度和取向共同影响明暗','Bright field: mainly near-axis electrons\nScattering, thickness and orientation matter'),ha='center',fontsize=10)
    ax=axes[2];ax.set_title(tr('C  玻璃态冰保留水合环境','C  Vitreous ice preserves hydration'),fontsize=12)
    ax.add_patch(Rectangle((-2.5,4),5,2,fc='#dce8ec',ec=blue));rng=np.random.default_rng(44)
    for x,y in rng.uniform([-2.3,4.2],[2.3,5.8],(35,2)):ax.add_patch(Circle((x,y),.05,color=blue,alpha=.5))
    for x,y in [(-1.4,5.3),(.1,4.7),(1.5,5.2)]:ax.add_patch(Ellipse((x,y),.8,.45,angle=x*40,fc=green))
    ax.text(0,7.3,tr('20世纪80年代：玻璃化制样发展','1980s: development of vitrification'),ha='center',fontsize=10)
    ax.text(0,2.5,tr('无规则排列的水分子\n避免大冰晶重排样品','Disordered water arrangement\nAvoid large ice crystals rearranging specimens'),ha='center',fontsize=10)
    save(fig,'principle')
    pts=np.array([[-8.,0.,-25.],[8.,0.,25.]])
    def project(angle):
        a=np.deg2rad(angle);return np.column_stack([pts[:,0]*np.cos(a)+pts[:,2]*np.sin(a),pts[:,1]])
    fig,axes=plt.subplots(1,3,figsize=(12,4.5),layout='constrained')
    for ax,angle in zip(axes,[0,30,60]):
        pr=project(angle)
        for i,(x,y) in enumerate(pr):ax.add_patch(Circle((x,y),12,fc=[green,red][i],alpha=.65,ec='white'))
        sep=np.linalg.norm(pr[1]-pr[0]);ax.set(xlim=(-50,50),ylim=(-35,35),xlabel=tr('投影位置 / nm','Projected position / nm'),ylabel='y / nm',title=tr(f'倾转 {angle}°：中心距 {sep:.1f} nm',f'Tilt {angle}°: centers {sep:.1f} nm'));ax.set_aspect('equal');ax.axhline(0,color=gray,lw=.6,ls=':')
    fig.suptitle(tr('相同的两个球：重叠随观察方向改变','The same two spheres: overlap changes with viewing angle'),fontsize=15)
    save(fig,'projection')
    fig,axes=plt.subplots(2,2,figsize=(11,8),layout='constrained')
    voltage=np.linspace(60,300,300);lam=wavelength(voltage*1000)*1e12
    axes[0,0].plot(voltage,lam,color=blue,lw=2);axes[0,0].set(xlabel=tr('加速电压 / kV','Accelerating voltage / kV'),ylabel=tr('电子波长 / pm','Electron wavelength / pm'),title=tr('A  波长很短，成像仍受透镜与样品影响','A  Short wavelength is only one ingredient'))
    ds=np.array([.2,.25,.35]);camera_mm=500.;lam_nm=wavelength(200e3)*1e9;rings=camera_mm*lam_nm/ds
    ax=axes[0,1]
    for r,d,col in zip(rings,ds,[green,blue,red]):ax.add_patch(Circle((0,0),r,fill=False,lw=2,color=col,label=f'd = {d:.2f} nm'))
    ax.plot(0,0,'o',color=gray);ax.set(xlim=(-7.5,7.5),ylim=(-7.5,7.5),xlabel=tr('屏上位置 / mm','Screen position / mm'),ylabel=tr('屏上位置 / mm','Screen position / mm'),title=tr('B  晶面间距越小，衍射环越外','B  Smaller spacings give outer rings'));ax.set_aspect('equal');ax.legend(frameon=False,fontsize=9,loc='upper left')
    diam=np.array([18,19,20,20,21,22,23,25,27,35.]);weights=diam**2
    edges=np.arange(15,41,5);axes[1,0].hist(diam,bins=edges,color=green,alpha=.8,edgecolor='white');axes[1,0].set(xlabel=tr('等效圆直径 / nm','Equivalent-circle diameter / nm'),ylabel=tr('颗粒数','Particle count'),title=tr('C  数目分布保留大颗粒尾部','C  Number distribution retains the large tail'))
    definitions=[tr('数目平均','Number mean'),tr('面积加权平均','Area-weighted mean')];means=[diam.mean(),np.average(diam,weights=weights)]
    axes[1,1].bar(definitions,means,color=[green,red],width=.55)
    for i,v in enumerate(means):axes[1,1].text(i,v+.6,f'{v:.2f} nm',ha='center')
    axes[1,1].set(ylabel=tr('平均直径 / nm','Mean diameter / nm'),ylim=(0,33),title=tr('D  权重改变，回答的问题也改变','D  Different weights answer different questions'))
    save(fig,'measurement')
    with (output/'data.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['particle','diameter_nm','projected_area_nm2','area_weight']);w.writerows((i+1,d,np.pi*d*d/4,weights[i]/weights.sum()) for i,d in enumerate(diam))
    summary={'wavelength_200kV_pm':float(wavelength(200e3)*1e12),'ring_radius_d025_nm_mm':float(camera_mm*lam_nm/.25),'projected_separation_0_nm':float(np.linalg.norm(project(0)[1]-project(0)[0])),'projected_separation_60_nm':float(np.linalg.norm(project(60)[1]-project(60)[0])),'true_center_distance_nm':float(np.linalg.norm(pts[1]-pts[0])),'number_mean_nm':float(diam.mean()),'area_weighted_mean_nm':float(np.average(diam,weights=weights)),'diameter_from_area_314159_nm2':float(2*np.sqrt(314.1592653589793/np.pi)),'data_origin':'Constructed geometric and numerical teaching examples; no experimental TEM image claimed.'}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

The generated summary connects the calculations to independent checks. At 200 kV, the relativistic wavelength is about 2.508 pm, consistent with the tabulated electron-optical value. The initial projected center separation is 16 nm, while the three-dimensional separation is about 52.5 nm. A circular projected area of 314.159 nm² corresponds to a 20 nm equivalent-circle diameter. Each check isolates a different part of the measurement chain: electron physics, viewing geometry or the definition of size. Inspecting them together makes it easier to locate an error in units or interpretation before applying a calculation to experimental images.

For a new TEM investigation, first name the desired quantity: an inorganic core's projected size, a vesicle membrane's morphology, or a local crystal's plane spacing. Choose a preparation route that preserves that information, establish imaging and diffraction conditions, and include the relevant comparison specimens. If an unexpected feature appears, follow specimen state, projection geometry, scattering mechanism and processing in turn. TEM makes fine structures observable and measurable. Understanding how those observations are formed lets a sharp micrograph become a clear account of material and biological structure.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/I04.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Ernst Ruska — Nobel lecture](https://www.nobelprize.org/uploads/2018/06/ruska-lecture.pdf)

   Early magnetic lenses and multistage electron imaging in 1931.

   Historical primary source; original diagram here.
2. [JEOL Bionote — TEM specimen preparation](https://www.jeol.com/applications/pdf/others/1462_en.pdf)

   Ultrathin sections, negative staining, cryogenic observation and tomography.
3. [JEOL — wavelength of electron](https://www.jeol.com/words/emterms/20121023.071258.php)

   Relativistic wavelength relation and tabulated value at 200 kV.
4. [JEOL — selected-area diffraction](https://www.jeol.com/words/emterms/20121023.052558.php)

   Selected-area aperture, image planes and diffraction mode.
5. [EMBL — Jacques Dubochet and vitrification](https://www.embl.org/news/science/jacques-dubochet-awarded-nobel-prize-for-chemistry/)

   History of vitrification and hydrated-specimen observation.

   Institutional historical reference; original illustration.
6. [Royal Swedish Academy of Sciences — cryo-EM scientific background](https://www.nobelprize.org/uploads/2018/06/advanced-chemistryprize2017-1.pdf)

   Development of cryo-EM, irradiation and three-dimensional structural work.

   Public scientific background; no figures reused.
