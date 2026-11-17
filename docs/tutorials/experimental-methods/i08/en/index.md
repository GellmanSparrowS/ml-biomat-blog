# Micro-CT: Reconstructing three-dimensional structure from projections

Source: https://ml-biomat.com/tutorials/experimental-methods/i08/en/
Language: en

Recover internal sections from angular projections, then distinguish pore volume from spanning pathways.

## Are the pores inside a sponge rooms or connected corridors?

The openings on a sponge's surface are easy to see, but they do not fully explain how water travels through the entire piece. Some pores connect, while others resemble enclosed rooms. Tissue-engineering scaffolds, polymer foams, battery electrodes and bone raise related questions: how much volume is empty, which directions contain continuous pathways, how thick are the load-bearing struts, and does a surface crack extend deep inside? Cutting a specimen exposes one section, but the answer may depend on the cutting position, and cutting destroys some of the original spatial relationships. X-ray micro-computed tomography reconstructs an internal volume from projections acquired at many directions, allowing those relationships to be examined throughout the specimen.

Computed tomography, abbreviated CT, does not physically slice the object into sheets. Its reconstructed volume can be inspected as a stack of virtual sections, much like turning through a collection of spatial maps. An ordinary radiograph combines contributions along each X-ray path, so structures at different depths can overlap. CT changes the viewing direction to obtain many different combinations, then estimates a spatial distribution capable of explaining them together. Micro-CT applies this idea to smaller specimens and finer spatial scales. Its subjects include trabecular bone, insects, seeds, composites, small manufactured components and porous scaffolds.

Two explicitly constructed teaching objects connect the principles in this chapter. The first is a circular section containing regions with different attenuation, whose known geometry lets us inspect changes introduced by projection and reconstruction. The second is a three-dimensional block containing a through-channel, a narrow throat, a side branch and an isolated pore. It separates the questions of porosity and connectivity. One object teaches how overlapping information becomes a section; the other teaches how a reconstructed volume can answer a materials question. The complete code generates both datasets and the displayed results, with clearly specified dimensions, gray levels and analysis conditions.

## Separating overlapping structures changed the purpose of an image

Early X-ray imaging already revealed bones and metal, but structures at different depths often overlapped. A central step in CT was to combine measurements from multiple directions with numerical recovery of a section. Cormack investigated reconstruction of internal attenuation from transmission measurements, while Hounsfield advanced practical scanning equipment. They shared the 1979 Nobel Prize in Physiology or Medicine for the development of computer-assisted tomography. The important conceptual change was a willingness to acquire many directional measurements in exchange for separating structures in depth. Improved usefulness did not depend solely on making a conventional projection sharper.

The left-hand illustration uses parallel rays, translation and a change of direction to explain the idea of early line-by-line acquisition. The right-hand illustration shows a common laboratory micro-CT arrangement: X-rays diverge from a small focal spot, a specimen rotates on a stage, and a flat detector records projections. The drawing shows one side view; the beam also spreads out of the page, producing a cone. A small focal spot and geometrical magnification support fine detail, while increased magnification generally reduces the specimen extent that fits completely within the field of view. Parallel-beam instruments and other trajectories also exist, so reconstruction software must use the actual acquisition geometry.

Imagine two small beads aligned one behind the other along your line of sight. A single projection may merge them, whereas another viewing direction separates them. For a complex specimen, reconstruction resembles solving many connected addition problems. Each ray tells us its accumulated attenuation without directly specifying the contribution from every short segment. A sufficiently informative set of directions constrains the possible allocations. Reconstruction therefore estimates internal numerical values from a collection of measurement relationships. It does not simply add three-dimensional shading to an ordinary photograph.

![Original principle diagram connecting 1970s CT development with laboratory geometry. A illustrates translated line measurements at multiple directions; B shows a side view of a divergent cone beam and rotating specimen. Not to scale or a replica of a historical device.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/68eeb7a1917fb277db0a1e86.svg?v=68eeb7a1917f)

Figure 1Original principle diagram connecting 1970s CT development with laboratory geometry. A illustrates translated line measurements at multiple directions; B shows a side view of a divergent cone beam and rotating specimen. Not to scale or a replica of a historical device.

## The detector measures weakened radiation before we obtain internal gray levels

As X-rays pass through matter, absorption and scattering remove some photons from the original detected path. For monochromatic radiation under a suitable narrow-beam approximation, transmission through a uniform material decreases exponentially with thickness. The linear attenuation coefficient describes the reduction per unit path length and has inverse-length units. It depends on composition, density and photon energy. A brighter reconstructed region therefore first indicates greater attenuation under the specified conditions. Converting gray level into mineral density or component concentration requires suitable standards and calibration rather than simply renaming brightness as mass.

$$
I=I_0e^{-\mu L},\qquad p=-\ln(I/I_0)=\mu L
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5f9665f604056f523b647279.svg) | Transmitted and incident intensities in the same detector units. |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | Linear attenuation coefficient of the uniform material, mm⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Ray path length, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/48c7b594e8628a17b991d4e6.svg) | Negative log transmission, equal to the path attenuation integral here; dimensionless. |

For a monochromatic narrow beam through uniform material after background normalization, μ=0.4 mm⁻¹ and L=2 mm give I/I0=0.449329 and p=0.8. Along a nonuniform path, contributions μΔL from short segments add.

A uniform material with attenuation coefficient 0.4 mm⁻¹ transmits approximately 44.93% of the incident intensity through a thickness of 2 mm. The negative natural logarithm of that transmission is 0.8, equal to attenuation coefficient multiplied by thickness. For a path crossing several materials, the corresponding contributions from each segment add. Taking a logarithm converts the successive multiplication of transmission fractions into addition, which is useful for reconstruction. A processed detector reading therefore represents attenuation accumulated along a path, not the density of one small location immediately in front of that detector element.

Real detectors also have dark signals and unequal pixel responses. An exposure without incident radiation estimates the dark field; an illuminated exposure without the specimen supplies a flat field. Subtracting the dark signal from both specimen and flat-field readings before taking their ratio produces a more useful transmission estimate. A detector element that remains systematically bright or dark can leave an error at a fixed position across many projections. Reconstruction propagates that error around the rotation axis, potentially creating a ring. This connects a calibration problem with a recognizable image feature and explains why an attractive three-dimensional rendering cannot replace inspection of projection quality.

For example, a specimen reading of 510, a dark reading of 10 and a flat-field reading of 1010 give corrected transmission of 500 divided by 1000, or one half. The corresponding negative logarithm is approximately 0.693. Dividing 510 directly by 1010 would retain the detector offset and give a different path value. Although the discrepancy looks small for these numbers, its relative importance increases when the transmitted specimen signal approaches the dark level, as can occur along strongly attenuating paths.

$$
T=\frac{S-D}{F-D},\qquad p=-\ln T
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | Corrected transmission; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | Reading of a detector pixel with specimen present, common detector units. |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | Matched dark-field reading, in the same units as S. |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | Illuminated flat-field reading without specimen, same units as S. |
| ![Formula](https://ml-biomat.com/static/agent-math/48c7b594e8628a17b991d4e6.svg) | Negative log transmission for that ray; dimensionless. |

For S=510, D=10 and F=1010, T=500/1000=0.5 and p=0.693147. The flat field exceeds dark signal and readings fall within the valid dynamic range; response and exposure conditions must match.

Laboratory sources usually emit a range of photon energies. Lower-energy photons are often attenuated more strongly, so the transmitted beam becomes enriched in higher-energy photons after crossing substantial material. This is beam hardening. Interpreting such data with the simplest monochromatic model can make the centre and edge of a uniform object appear to have different attenuation, producing a cupping pattern. Suitable filtration, acquisition conditions, reference objects and reconstruction corrections help address the effect. Correction strength should be chosen using sections, intensity profiles and known objects. Increasing it indiscriminately can introduce a different bias. Decide whether the experiment targets geometry, porosity or density so the relevant calibration receives appropriate attention.

## From sinogram to section: sparse directions leave streaks

Arranging one-dimensional projections beside one another produces a sinogram. Its name comes from the trajectory of a small object during rotation: the object's projected detector position changes approximately sinusoidally with angle. One axis is detector position, another is acquisition direction, and brightness represents the line-integrated attenuation. This is neither a specimen section nor a simple overlay of photographs. It is a map of measurement relationships used for reconstruction. Recognizing its coordinates prevents a band in projection data from being mistaken for a fibre or layer inside the material.

The most intuitive reconstruction procedure is backprojection. Spread each measured ray value back along its original path and add contributions from different directions. Real structures receive support from many directions and begin to emerge, but each ray also distributes values into locations where the object did not contribute. Simple backprojection consequently creates a blurred halo. Filtered backprojection adjusts spatial-frequency contributions in each projection before spreading it back, compensating for this blur. The filter is part of the reconstruction mathematics, not an arbitrary cosmetic treatment. Emphasizing rapid spatial variation also affects noise, so practical choices balance edge definition with noise in a task-dependent way.

The six-panel figure places these steps together. The known section is followed by its analytical projections and unfiltered backprojection. The lower row compares filtered reconstructions from 12 and 180 directions and displays the denser reconstruction minus the known section. Detector noise is absent from this teaching experiment, so the pronounced streaks in the 12-direction image primarily illustrate insufficient angular sampling. The 180-direction result is closer to the object, while boundaries still reflect the discrete grid, interpolation and finite sampling. A signed difference image locates overestimation and underestimation more directly than an apparently smooth grayscale reconstruction alone.

![Analytical projections and executed reconstructions of a constructed teaching section. A, D, E and difference F express attenuation in mm⁻¹; sinogram B and unfiltered backprojection C are dimensionless. The 12- and 180-direction cases use matched geometry and filtering, without detector noise; the difference image shows finite-sampling and interpolation effects.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/2f7970164f69127a60d10b67.svg?v=2f7970164f69)

Figure 2Analytical projections and executed reconstructions of a constructed teaching section. A, D, E and difference F express attenuation in mm⁻¹; sinogram B and unfiltered backprojection C are dimensionless. The 12- and 180-direction cases use matched geometry and filtering, without detector noise; the difference image shows finite-sampling and interpolation effects.

On the same 128-by-128 comparison grid, the root-mean-square error is approximately 0.050 mm⁻¹ for 180 directions and 0.212 mm⁻¹ for 12 directions. This measure squares each pixel difference, averages those squares and takes a square root, giving greater influence to larger local errors while retaining attenuation units. The comparison isolates the role of direction count for this object and algorithm. It does not prescribe 180 views for every instrument. The required angular sampling also depends on desired detail, field of view, detector sampling and noise. Plan acquisition around the smallest feature relevant to the question, then examine reconstructions and reference objects to determine whether the measurement supports that task.

## Small voxels and fine resolved detail are related but distinct

A reconstructed volume consists of small spatial elements called voxels, the three-dimensional counterparts of pixels. Voxel spacing specifies how densely values are placed in space, but it does not determine resolved detail on its own. Source focal size, detector blur, mechanical stability, specimen motion and reconstruction filtering can spread an edge across several voxels. Enlarging a blurred photograph into more pixels does not recover a missing fine line; likewise, choosing a small reconstruction grid requires corresponding information in the measurement. Edge responses, fine wires or other suitable reference objects can help characterize spatial resolution. Report voxel spacing alongside that measured performance rather than treating the two quantities as interchangeable.

This distinction is particularly useful when moving between materials and biological specimens. Bone mineral often has appreciable attenuation contrast with its surroundings, making fine trabeculae easier to distinguish. Hydrated soft tissue or a water-rich hydrogel can have attenuation closer to that of water. Contrast agents or staining may improve visibility of selected components, while uneven penetration, shrinkage and chemical processing can change the specimen. A clearer image of a dried sample may no longer preserve the wet pore geometry that motivated the experiment. Strongly attenuating metal inclusions create a different challenge, often producing conspicuous streaks. Specimen state and imaging conditions should answer the same physical question.

Acquisition time also has spatial consequences. Longer exposure provides more photons and can reduce some random fluctuations, but it allows more opportunity for slow movement, drying or temperature changes. A mount must stabilize the specimen without compressing a soft material or obscuring the useful field. Adequate transmission and field coverage should persist throughout rotation: a specimen that fits at one angle may be truncated at another. Direction count, angular range, exposure, filtration, source–specimen distance and reconstruction conditions all help connect the final numerical volume to the measurement. A single rendered image cannot preserve those relationships.

Spatial-unit mistakes become especially consequential in three dimensions. If the true spacing is 10 μm in every direction but is entered as 20 μm, each voxel's calculated volume becomes eight times larger, not twice as large. Porosity may remain unchanged because the same voxel volume cancels from its numerator and denominator, while absolute pore volume, surface area and diameter change in different ways. A plausible percentage therefore does not validate the spatial calibration. When an array is resampled onto another grid, update its spacing consistently. Interpolation changes the number and arrangement of stored values; it does not physically expand or shrink the specimen. For anisotropic data, keep the three spacings separately rather than assuming that the distance between slices equals the in-plane pixel spacing.

Partial volume is another important effect. A voxel containing both solid and pore can take an intermediate gray value, so its assigned class depends on the segmentation rule. For a thick strut, these mixed voxels occupy a relatively small boundary layer. For a narrow passage or a feature only a few voxels wide, they may occupy most of the feature. The same threshold change can therefore shift a broad boundary slightly while breaking a thin connection completely. This explains how connectivity may change dramatically even when the overall porosity changes only modestly.

## Define the region before counting pores and following pathways

Before calculating porosity, identify the denominator. Including air outside the specimen makes the result depend on the size of the crop box even though the material has not changed. The region of interest should correspond to a defined specimen volume: a fixed internal scaffold region, an anatomical region in bone, or an envelope representing the whole specimen after excluding exterior air. Gray levels or another suitable segmentation procedure then assign voxels to pore, solid or additional components. Porosity is pore volume divided by total region volume. On a grid of equally sized voxels, the shared voxel volume cancels and the calculation reduces to a ratio of voxel counts.

$$
V_v=\Delta x\Delta y\Delta z,\qquad \phi=\frac{V_p}{V_{\mathrm{ROI}}}=\frac{N_p}{N_{\mathrm{ROI}}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1b2d60b2f55270f4079ede68.svg) | Volume of one voxel, mm³. |
| ![Formula](https://ml-biomat.com/static/agent-math/ec9221cb3cb38bb1f2a7546d.svg) | Voxel spacings along the three axes, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/9aef9010291adb65d70e58b4.svg) | Porosity; dimensionless, multiplied by 100 for percent. |
| ![Formula](https://ml-biomat.com/static/agent-math/0aab7bc1436cffc0257cb238.svg) | Pore volume and total region-of-interest volume, mm³. |
| ![Formula](https://ml-biomat.com/static/agent-math/a0a1fa56c4155ae51682658e.svg) | Pore and region-of-interest voxel counts; dimensionless. |

Equal voxel volumes cancel. Spacing 0.01 mm gives voxel volume 10⁻⁶ mm³; 3213/48³=0.0290527, or 2.90527%. Absolute pore volume is 0.003213 mm³.

The teaching block contains 48 by 48 by 48 voxels with spacing 0.01 mm in each direction. Each voxel occupies 0.000001 mm³, and the whole region occupies 0.110592 mm³. At the specified blur and gray threshold of 128, 3213 voxels are classified as pore. Their volume is 0.003213 mm³ and the resulting porosity is approximately 2.905%. The constructed geometrical porosity is approximately 3.266%. Blur, noise, gray quantization and threshold selection account for the difference. Keeping a known geometry allows us to examine what the analysis recovers instead of assuming that any one segmentation exactly locates the material boundary.

Connectivity asks whether a continuous route exists between pore voxels. This chapter uses six-neighbour connectivity: a voxel connects to neighbours sharing one of its six faces, while contact at an edge or corner alone does not count. The program labels separate pore clusters, then identifies clusters touching both opposite faces normal to z. Their total volume divided by all pore volume defines the spanning-pore fraction used here. Its denominator differs from that of porosity. One quantity asks how much of the entire region is pore; the other asks how much of the pore space belongs to clusters that span a specified direction.

$$
f_{\mathrm{span},z}=\frac{V_{\mathrm{pore\ clusters\ touching\ both}\ z\mathrm{\ faces}}}{V_p}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/eaef2a2f98497936fa9a3119.svg) | Fraction of pore volume belonging to clusters spanning z; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/ebf93f58e7d2b4164904cc55.svg) | Total pore-cluster volume touching both z faces under six-neighbour connectivity, mm³. |
| ![Formula](https://ml-biomat.com/static/agent-math/fcf999839bc2e4b6bb4754e8.svg) | All pore volume inside the region, mm³. |
| ![Formula](https://ml-biomat.com/static/agent-math/9032cb23a878659e74b670d3.svg) | Specified volume axis; direction label. |

Connect voxels through shared faces and identify clusters touching both ends. Defaults give 3003/3213=0.9346405, or 93.464%. This describes geometric spanning, without fluid viscosity or hydraulic resistance.

Under the default conditions, the spanning-pore fraction is approximately 93.46%; the remaining pore volume does not connect the two chosen faces. This is not a permeability measurement. Connected paths with different throat widths, tortuosity or surface interactions can still offer very different resistance to fluid flow. The narrow throat in the example makes the distinction visible. Green regions belong to clusters connecting both z faces, while orange identifies other pores. With greater blur or a changed threshold, a small connection may disappear and the spanning fraction can fall abruptly to zero. The material itself has not fractured during the interaction; image formation and segmentation have changed the recovered pathway.

![Constructed 3D block with channel, throat, side branch and isolated pore. A and B show the section at y index 20; statistics use the full 48³ volume. Green pores span both z faces. Curves compare blur standard deviations σ of 0.5, 1 and 1.5 voxels and distinguish threshold effects on volume fraction and spanning fraction.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/2c9c2d6ad4cc081c9cf540ad.svg?v=2c9c2d6ad4cc)

Figure 3Constructed 3D block with channel, throat, side branch and isolated pore. A and B show the section at y index 20; statistics use the full 48³ volume. Green pores span both z faces. Curves compare blur standard deviations σ of 0.5, 1 and 1.5 voxels and distinguish threshold effects on volume fraction and spanning fraction.

## Move the threshold and watch a throat control the whole pathway

The interactive experiment uses the same three-dimensional teaching block with three specified blur levels, an adjustable gray threshold and a section-position control. Lower gray values are more pore-like; increasing the threshold includes additional boundary voxels. The left view shows section gray levels and the right view shows pore classification. Porosity and spanning fraction are calculated from the entire volume, not only the displayed section. Start with the lowest blur and browse through the narrow-throat region. Then increase blur to see how a geometrical connection becomes progressively harder to distinguish in the image.

At fixed blur, move the threshold slowly. Porosity generally changes gradually, but the spanning fraction can jump because a pathway depends on its narrowest connection. Once a small segment is assigned to solid, two much larger pore regions may become separated. This matters when a scaffold study reports stable overall porosity without examining whether transport-controlling throats approach the resolution limit. Compare nearby thresholds together with local sections to identify where a conclusion is sensitive. Those locations guide a concrete next step, such as a finer scan, complementary measurement or a better-supported segmentation rule.

## Three-dimensional pores: threshold and spanning

Constructed 48³ volume, voxel spacing 0.01 mm. Gray values below threshold are pore; green spans both z faces and orange marks other pores. Statistics use the complete volume; slice position changes only the view.

When comparing two scaffolds, avoid separately adjusting thresholds until each rendering looks most attractive. First establish whether their gray scales are comparable under matched acquisition and reconstruction. Then select a rule supported by standards, phase distributions and local boundaries. If composition produces genuinely different attenuation, each material may require an appropriate physical calibration. Examine how plausible rule changes affect the comparison. Display brightness and colour can assist interpretation, while the measured gray values, region definition and segmentation rule preserve the quantitative result. This connects image differences to structure rather than to separate display preferences.

## Keep geometry, reconstruction and three-dimensional statistics connected

The complete Python example contains two related experiments. The two-dimensional part calculates analytical ray contributions from circular regions, generates directional projections and reconstructs the section by filtered backprojection. This makes angular undersampling especially clear. The three-dimensional part constructs a volume with a throat and isolated pore, applies specified Gaussian blur and small fixed-seed noise, quantizes the gray values and performs segmentation with six-neighbour connectivity. Separate arrays preserve the two experiments. The two-dimensional projections are not presented as an actual scan of the later three-dimensional block.

Outputs include reusable numbers as well as figures. Projection arrays retain direction and detector coordinates. Volume arrays retain gray values, the constructed pore geometry and voxel spacing. A table lists porosity, spanning fraction and component count across blur and threshold choices. The numerical summary also checks transmission through a known slab, the analytical central line integral of a disk and the volume of one voxel. These tests concern attenuation physics, projection geometry and spatial units, respectively. They make it harder for an earlier inconsistency to remain hidden behind a convincing image. Real data should undergo the same initial checks of units and coordinates before statistical analysis begins.

A useful micro-CT result combines located sections, an appropriate three-dimensional view, quantitative definitions and comparisons that answer the research question. The three-dimensional view explains pathway organization, the sections expose boundary quality, and the statistics quantify changes in pore space and connectivity. To understand why one scaffold wets more readily, another property enters: the interaction between liquid and the material surface. Pores provide spatial routes, while wetting helps determine the interfacial conditions for entering those routes. Contact-angle measurements turn that next question into an observable droplet shape.

A comparison also needs a clear distinction between specimens and sampled regions. Ten small cubes cropped from one scaffold describe spatial variation within that scaffold, but they are not automatically ten independently manufactured scaffolds. To compare manufacturing conditions, preserve variation between independent specimens and define how regions are selected within each one. This prevents a large number of nearby image samples from creating an exaggerated impression of experimental replication. The same principle applies when several slices pass through the same pore: they provide spatial information about that pore, not a new pore at every section.

For scans acquired before and after loading, register the two volumes to a common coordinate system before deciding that a particular strut or cavity has changed. Registration estimates how locations correspond despite specimen translation or rotation. Inspect local sections to ensure that a claimed broken strut is the same structure in both scans. Rendering choices such as colour, opacity and viewing direction can communicate those correspondences, but a thin feature may disappear from a rendered image simply because it is obscured or assigned low opacity. Return to the numerical mask and original sections to determine whether the structural change is present in the measured volume.

These distinctions make the example useful beyond its small constructed block. The block contains a known bottleneck, so its segmentation sensitivity is easy to locate. In a real scaffold, map sensitive connections back to their spatial positions instead of reducing every choice to one global number. A cluster that spans the region in z may fail to span it in x or y, and cropping can remove a connection that exists outside the chosen region. Direction and region boundaries therefore belong in the definition of a connectivity result. Recording them makes later comparisons with fluid transport, mechanical loading or another imaging method much more informative.

### Complete Python: reconstruction and 3D pore connectivity

Generate projections from known geometry, compare angular sampling, then analyze gray values, pores and spanning paths in a separately constructed volume. Save arrays and sensitivity tables.

```
"""Original parallel-beam CT and porous-volume teaching experiment.
Run: python main.py --output results --language en
All specimens and signals in this example are constructed, with known geometry.
"""
from pathlib import Path
import argparse,json
import numpy as np
from scipy import ndimage
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle

def make_volume(sigma=1.0):
    z,y,x=np.indices((48,48,48));radius=np.where((z>=22)&(z<=25),1.2,4.)
    channel=(x-16)**2+(y-20)**2<=radius**2
    branch=(y-20)**2+(z-12)**2<=3**2
    isolated=(x-35)**2+(y-35)**2+(z-35)**2<=4**2
    pores=channel|branch|isolated
    field=ndimage.gaussian_filter((~pores).astype(float),sigma=sigma,mode='nearest')
    field+=np.random.default_rng(1708).normal(0,.015,field.shape)
    return np.rint(np.clip(field,0,1)*255).astype(np.uint8),pores

def metrics(gray,threshold=128):
    pore=gray<threshold
    labels,n=ndimage.label(pore,structure=ndimage.generate_binary_structure(3,1))
    connected=np.intersect1d(np.unique(labels[0]),np.unique(labels[-1]));connected=connected[connected>0]
    spans=np.isin(labels,connected);count=int(pore.sum())
    return {'pore_voxels':count,'porosity':float(pore.mean()),'components':int(n),
       'spanning_fraction':float(spans.sum()/count) if count else 0.,
       'pore_volume_mm3':count*.01**3},spans

def project(detector,angles,circles):
    result=np.zeros((len(detector),len(angles)))
    for cx,cy,r,mu in circles:
        distances=detector[:,None]-cx*np.cos(angles)-cy*np.sin(angles)
        result+=2*mu*np.sqrt(np.maximum(r*r-distances**2,0))
    return result

def reconstruct(sino,detector,angles,X,Y,filtered=True):
    if filtered:
        nfft=2**int(np.ceil(np.log2(len(detector)*2)))
        frequency=np.fft.rfftfreq(nfft,d=detector[1]-detector[0])
        filtered_sino=np.fft.irfft(np.fft.rfft(sino,n=nfft,axis=0)*2*np.abs(frequency[:,None]),n=nfft,axis=0)[:len(detector)]
    else:filtered_sino=sino
    recon=np.zeros(X.shape)
    for k,theta in enumerate(angles):
        recon+=np.interp((X*np.cos(theta)+Y*np.sin(theta)).ravel(),detector,filtered_sino[:,k],left=0,right=0).reshape(X.shape)
    return recon*np.pi/(2*len(angles))

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args()
    out=args.output;out.mkdir(parents=True,exist_ok=True);tr=lambda z,e:z if args.language=='zh' else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fbfcfc','savefig.facecolor':'#fbfcfc','text.color':'#18344a'})
    def save(f,n):
        f.savefig(out/f'{n}-{args.language}.svg',bbox_inches='tight');f.savefig(out/f'{n}-{args.language}.png',bbox_inches='tight',dpi=150);plt.close(f)
    blue='#186c94';orange='#d27839';green='#188777'
    coord=(np.arange(128)-63.5)*.01;X,Y=np.meshgrid(coord,coord)
    circles=[(0,0,.45,1),(-.16,.08,.12,-.8),(.2,-.12,.08,.6)]
    truth=np.zeros(X.shape)
    for cx,cy,r,mu in circles:truth+=mu*((X-cx)**2+(Y-cy)**2<=r*r)
    detector=(np.arange(256)-127.5)*.01;angles=np.arange(180)*np.pi/180
    sino=project(detector,angles,circles)
    full=reconstruct(sino,detector,angles,X,Y);sparse=reconstruct(sino[:,::15],detector,angles[::15],X,Y)
    back=reconstruct(sino,detector,angles,X,Y,False)
    gray,pores=make_volume(1.);stats,spans=metrics(gray)
    series=[]
    for sigma in [.5,1.,1.5]:
        g,_=make_volume(sigma)
        for t in range(50,206,5):series.append([sigma,t,*[metrics(g,t)[0][k] for k in ['porosity','spanning_fraction','components']]])
    np.savetxt(out/'data.csv',series,delimiter=',',header='blur_sigma_voxels,threshold_uint8,porosity,spanning_fraction,components',comments='')
    np.savez_compressed(out/'volume.npz',gray=gray,truth_pores=pores,voxel_spacing_mm=.01)
    np.savez_compressed(out/'tomography.npz',truth=truth,sinogram=sino,angles_rad=angles,detector_mm=detector,reconstruction=full)
    summary={**stats,'truth_porosity':float(pores.mean()),'fbp_rmse_180':float(np.sqrt(np.mean((full-truth)**2))),
       'fbp_rmse_12':float(np.sqrt(np.mean((sparse-truth)**2))),
       'slab_transmission':float(np.exp(-.4*2)),'slab_log_projection':.8,
       'voxel_volume_mm3':.01**3,'roi_volume_mm3':(48*.01)**3,
       'analytic_disk_center_projection':float(project(np.array([0.]),np.array([0.]),[(0,0,.45,1)])[0,0]),
       'specimen':'Constructed teaching geometries; not a measured CT scan'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    fig,axs=plt.subplots(1,2,figsize=(12,4.7));a,b=axs
    a.set_xlim(-1,8);a.set_ylim(-2,2);a.axis('off');a.add_patch(Circle((3,0),1,facecolor='#cee3e7',edgecolor=blue))
    for yy in [-.65,0,.65]:a.annotate('',xy=(6.5,yy),xytext=(0,yy),arrowprops={'arrowstyle':'->','color':blue})
    a.add_patch(Rectangle((6.5,-1),.3,2,color=orange));a.text(3,1.4,tr('平移 + 改变方向','Translate + change direction'),ha='center')
    a.text(3,-1.45,tr('早期逐线测量的思想','Early line-by-line acquisition'),ha='center');a.set_title(tr('A  从叠影到断层：1970年代','A  From superposition to sections: 1970s'),loc='left')
    b.set_xlim(-1,8);b.set_ylim(-2,2);b.axis('off');b.scatter([0],[0],s=80,color=orange)
    b.add_patch(Circle((3,0),.7,facecolor='#cee3e7',edgecolor=blue));b.plot([6.7,6.7],[-1.7,1.7],lw=5,color=blue)
    for yy in np.linspace(-1.5,1.5,7):b.plot([0,6.7],[0,yy],color=orange,lw=1,alpha=.65)
    b.annotate('',xy=(3.7,.8),xytext=(2.3,.8),arrowprops={'arrowstyle':'->','connectionstyle':'arc3,rad=-.5','color':green})
    b.text(3,-1.35,tr('样品旋转','Rotating sample'),ha='center');b.set_title(tr('B  实验室锥束几何的侧视','B  Side view of laboratory cone-beam geometry'),loc='left',fontsize=11)
    save(fig,'geometry')
    fig,ax=plt.subplots(2,3,figsize=(13,8));extent=[-.64,.64,-.64,.64]
    items=[(truth,'A  已知衰减分布','A  Known attenuation'),(sino,'B  多角度投影：正弦图','B  Angular projections: sinogram'),(back,'C  未滤波反投影','C  Unfiltered backprojection'),(sparse,'D  12方向滤波重建','D  FBP: 12 directions'),(full,'E  180方向滤波重建','E  FBP: 180 directions'),(full-truth,'F  重建减真值','F  Reconstruction minus truth')]
    for k,(a,(arr,z,e)) in enumerate(zip(ax.ravel(),items)):
        if k==1:im=a.imshow(arr,extent=[0,180,detector[-1],detector[0]],aspect='auto',cmap='magma');a.set_xlabel(tr('方向 / °','Direction / °'));a.set_ylabel(tr('探测位置 / mm','Detector coordinate / mm'))
        else:
            kw={'cmap':'coolwarm','vmin':-.25,'vmax':.25} if k==5 else {'cmap':'gray','vmin':0,'vmax':float(back.max()) if k==2 else 1.6}
            im=a.imshow(arr,extent=extent,origin='lower',**kw);a.set_xlabel('x / mm');a.set_ylabel('y / mm')
        a.set_title(tr(z,e),loc='left',fontsize=11)
        cb=fig.colorbar(im,ax=a,shrink=.7);cb.set_label('1' if k in [1,2] else 'mm⁻¹')
    fig.tight_layout();save(fig,'reconstruction')
    fig,ax=plt.subplots(2,2,figsize=(11,9));a,b,c,d=ax.ravel()
    a.imshow(gray[:,20,:],origin='lower',extent=[0,.48,0,.48],cmap='gray',vmin=0,vmax=255);a.set_title(tr('A  y=20截面：窄颈与分支','A  Section y=20: throat and branch'),loc='left');a.set_xlabel('x / mm');a.set_ylabel('z / mm')
    colors=np.zeros(gray.shape+(3,));colors[gray<128]=[.82,.47,.22];colors[spans]=[.09,.53,.47]
    b.imshow(colors[:,20,:],origin='lower',extent=[0,.48,0,.48]);b.set_title(tr('B  绿色孔隙连接z两端','B  Green pores connect both z faces'),loc='left');b.set_xlabel('x / mm');b.set_ylabel('z / mm')
    series=np.asarray(series)
    for sig,color in zip([.5,1,1.5],[blue,green,orange]):
        r=series[series[:,0]==sig];c.plot(r[:,1],r[:,2]*100,color=color,label=f'σ={sig:g} voxel');d.plot(r[:,1],r[:,3],color=color,label=f'σ={sig:g} voxel')
    c.axhline(pores.mean()*100,color='#a1abb2',ls=':',label=tr('构造真值','Constructed truth'));c.set_xlabel(tr('灰度阈值','Gray threshold'));c.set_ylabel(tr('孔隙率 / %','Porosity / %'));c.legend(fontsize=9);c.set_title(tr('C  体积分数随分割变化','C  Volume fraction changes with segmentation'),loc='left')
    d.set_xlabel(tr('灰度阈值','Gray threshold'));d.set_ylabel(tr('贯通孔隙 / 全部孔隙','Spanning pore volume / all pore volume'));d.set_ylim(-.03,1.03);d.legend(fontsize=9);d.set_title(tr('D  窄颈连接可突然改变','D  Throat connectivity can change abruptly'),loc='left')
    fig.tight_layout();save(fig,'porosity')
    print(json.dumps(summary))

if __name__=='__main__':main()
```

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/I08.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [scikit-image — Radon transform example](https://scikit-image.org/docs/stable/auto_examples/transform/plot_radon_transform.html)

   Projections, sinograms, filtered backprojection and discrete reconstruction.

   BSD-licensed open-source project; independent original implementation and figures here.
2. [ASTRA Toolbox — 2D geometries](https://astra-toolbox.com/docs/geom2d.html)

   Parallel and fan beams, detector spacing and spatial coordinates.

   Public technical reference; no code or figure copied.
3. [Bruker — Overview of NRecon, method note MCT-62](https://www.bruker.com/content/dam/bruker/int/en/resources/bbio/pci-community/microct-notes/MN062_NRecon%20overview.pdf)

   Projection/section distinction, beam hardening, rings and correction conditions.

   Public manufacturer manual; figures not reproduced.
4. [IBSI — Image processing](https://ibsi.readthedocs.io/en/latest/02_Image_processing.html)

   Voxels, spatial spacing, interpolation and region definitions.

   Public technical reference; no image reproduced.
5. [Nobel Foundation — 1979 CT development perspective](https://www.nobelprize.org/prizes/medicine/1979/perspectives/?print=1)

   Early tomography, multidirectional measurement and the history of Hounsfield and Cormack.

   Historical institutional account; original illustration used.
6. [Kak and Slaney — Principles of Computerized Tomographic Imaging](https://www.slaney.org/pct/pct-toc.html)

   Further reading on ray integrals, reconstruction and sampling.

   Authors permit personal use of electronic book; link only, no book pages or figures reused.
