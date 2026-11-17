# Diffusion and permeation: How molecules cross a material

Source: https://ml-biomat.com/tutorials/experimental-methods/e05/en/
Language: en

Separate entry, internal mobility and complete passage using concentration profiles, time lag and fluorescence recovery.

## Moving inside a material and crossing it are different questions

A contact lens must retain its shape while allowing oxygen to reach the cornea. A food-packaging film may instead be designed to reduce entry of particular gases. Cells embedded in a gel require nutrients to travel through their surroundings. Each problem involves molecular motion, but rapid movement inside a material does not by itself guarantee rapid passage through it. One molecule may enter readily and move slowly; another may move quickly once inside but rarely enter. Diffusion and permeation measurements separate these contributions, helping connect transport behavior to thickness, composition and interfacial design.

A diffusion coefficient describes how rapidly random molecular motion spreads a spatial distribution. Its units are length squared divided by time. A permeation experiment usually places a material between a donor compartment containing more target molecules and a receiver containing fewer, then measures accumulation on the receiving side. It observes the complete route: entry, movement inside and exit. Mixing in the surrounding liquids, specimen thickness and exposed area also affect the result. Converting a receiver-amount curve into a material parameter therefore starts with understanding how the apparatus controls these processes.

Solute permeation also differs from movement of water. Different solution compositions can drive water through a selectively permeable barrier through a chemical-potential difference, commonly called osmosis. Applied pressure can drive bulk liquid through a porous material. This chapter focuses on net solute transfer down a concentration difference without appreciable bulk flow. Comparable liquid levels and pressure conditions help establish that experimental definition. Studies deliberately using pressure-driven filtration or osmotic effects need water-flow measurements alongside solute flux, because the molecules may then travel partly with the moving liquid.

![Original historical diagrams: Fick’s concentration gradient, Daynes’s membrane transient and Axelrod and colleagues’ local photobleaching recovery. Geometry and molecular positions explain the measurement objects rather than reconstructing historical apparatus dimensions.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/6263d248caca2de05437cc56.svg?v=6263d248caca)

Figure 1Original historical diagrams: Fick’s concentration gradient, Daynes’s membrane transient and Axelrod and colleagues’ local photobleaching recovery. Geometry and molecular positions explain the measurement objects rather than reconstructing historical apparatus dimensions.

Several historical measurement ideas meet here. Fick's 1855 work on liquid diffusion connected spatial concentration differences with net flux. Daynes's 1920 work on gases crossing rubber membranes examined the time needed to establish transmission. In 1976, Axelrod and colleagues systematically analyzed fluorescence recovery after photobleaching to study local molecular mobility. Modern membrane, gel and cellular measurements retain these ideas while observing different scales. The original schematic places their measurement objects side by side, allowing us to identify what each method observes before introducing the equations used to interpret it.

## Random steps can produce directional net transport

An individual molecule in a uniform liquid does not know which side has lower concentration. Interactions with surrounding molecules continually change its motion. If more molecules occupy the left side, however, more will on average cross an imaginary dividing plane from left to right than in the reverse direction during a short interval. Net transfer arises from unequal populations, rather than every molecule choosing the same direction. At equal concentrations, crossings continue both ways but their average difference is zero. This picture explains both the direction of diffusion and the dynamic character of equilibrium.

A gradient is a change per distance. The same concentration difference over a shorter distance produces a steeper gradient, whereas spreading it over a longer distance gives a shallower one. Fick's first law connects net flux to this gradient. Flux is measured per area and per time, so increasing exposed area increases total transfer without necessarily changing the behavior per unit area. The negative sign determines direction: if concentration decreases along the chosen positive coordinate, its gradient is negative and net flux is positive. Establishing the coordinate direction first makes the sign physically interpretable.

$$
J=-D\frac{\mathrm{d}c}{\mathrm{d}x}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/70f3dc39744c98269cbe57ad.svg) | Net mass flux in the positive x direction, μg cm^{-2} s^{-1}. |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | Diffusion coefficient within the material, cm²/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | Target concentration within the material, μg/cm³; 1 cm³=1 mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | Position along the transport direction, cm. |
| ![Formula](https://ml-biomat.com/static/agent-math/19c0c9a9adb9595e43d95dfa.svg) | Spatial concentration gradient, μg/cm⁴. |

For the dilute, constant-D, one-dimensional model, net transport follows decreasing concentration. A drop from 50 to 0 μg/cm³ over 0.05 cm gives a gradient of −1000 μg/cm⁴; D=10⁻⁶ cm²/s gives J=0.001 μg cm⁻² s⁻¹.

If more molecules enter a small region than leave it, local concentration rises; if more leave, it falls. Combining this conservation statement with the flux law gives the diffusion equation describing concentration through time. The heatmap uses one uniform material, rather than different materials at different positions. Its left boundary maintains high concentration, its right boundary remains near zero, and initially the interior contains no target. Changes begin near the entrance, propagate inward and eventually approach a straight concentration profile. A straight profile indicates equal net flux through each section, with no continuing accumulation inside the membrane.

![Space–time heatmap and concentration profiles of the same ideal planar membrane: thickness 0.5 mm, D=10⁻⁶ cm²/s, internal upstream concentration 50 μg/mL and zero downstream concentration. Color scale and profile axes use the same concentration definition.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/bc61e993a32639803d9d5a8a.svg?v=bc61e993a326)

Figure 2Space–time heatmap and concentration profiles of the same ideal planar membrane: thickness 0.5 mm, D=10⁻⁶ cm²/s, internal upstream concentration 50 μg/mL and zero downstream concentration. Color scale and profile axes use the same concentration definition.

Random motion produces a useful scaling relationship: characteristic diffusion time grows approximately with distance squared. Doubling the distance while keeping effective diffusivity unchanged increases the timescale roughly fourfold. This concerns a characteristic process, not a promise that every molecule arrives simultaneously. For cells in a gel, it helps explain why a modest increase in construct thickness can create a substantial supply problem. For a measurement device, shortening the transport path can be more effective than simply waiting longer. The numerical coefficient depends on geometry, boundary conditions and the particular definition of characteristic time.

$$
t_{\mathrm{diff}}\propto\frac{\ell^2}{D},\qquad \frac{t_2}{t_1}=\left(\frac{\ell_2}{\ell_1}\right)^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a91f47f932c9f9cb2951264a.svg) | Characteristic diffusion time for a specified geometry and observation criterion, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/dac4cdb34a25b3b90b51bf8b.svg) | Characteristic transport distance, cm. |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | Unchanged diffusion coefficient, cm²/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/4a242ab8839381eab37575ed.svg) | Corresponding characteristic times for two geometrically similar cases, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/354ae30840963888785d34f6.svg) | Characteristic distances in the two cases, cm. |
| ![Formula](https://ml-biomat.com/static/agent-math/d9c6c40f15e6a090e4bcafe4.svg) | Proportionality symbol; the coefficient depends on geometry and the definition of characteristic time. |

At the same D, with similar geometry and the same observation criterion, increasing distance from 0.05 to 0.10 cm gives a time ratio of 4. The scaling does not specify the arrival time of every molecule.

The coefficient also belongs to a specified molecular population. Small dyes, labeled proteins, free ions and molecules that repeatedly bind to a network may display different motion. Temperature, solvent viscosity and network structure can change effective diffusivity. Directional channels may produce different transport along different axes. A uniform, isotropic material with dilute solute and constant diffusivity provides a useful starting model. Directional comparisons, concentration series and time-dependent observations can then establish which aspects of that simple description apply to the specimen under study and which require additional measurements.

## Entry and mobility jointly determine passage

Place a clean material in a solution containing the target and allow partitioning to approach equilibrium. Concentration inside the material need not equal concentration outside. Some molecules favor the material environment and become enriched there; others favor the surrounding water and remain depleted inside. A partition coefficient compares internal concentration with external concentration under specified definitions and conditions. If the bath contains 100 μg/mL while the material contains 50 μg/mL, the coefficient is 0.5. It describes entry or preference, while the diffusion coefficient describes mobility after entry. These are distinct physical contributions.

For a uniform planar membrane with constant concentration difference, no reaction and rapid interfacial equilibration, the steady concentration profile is approximately linear. Substituting the partition relation into Fick's law relates net flux to the concentration difference between the surrounding liquids. Here P includes membrane thickness and has units of length per time: diffusivity multiplied by partition coefficient and divided by thickness. Some literature instead calls the thickness-independent product a permeability, and gas studies often use pressure difference as their driving force. Definitions and units must therefore accompany any numerical comparison.

$$
K=\frac{c_{m,\mathrm{eq}}}{C_{b,\mathrm{eq}}},\qquad P=\frac{DK}{L},\qquad J_{\mathrm{ss}}=P(C_d-C_r),\qquad \dot M=AJ_{\mathrm{ss}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/24733a44cf365eb5e1b92574.svg) | Equilibrium material/bath partition coefficient on the same concentration basis, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/75f0936fa6794f04552ffae1.svg) | Equilibrium concentration inside the material, μg/cm³. |
| ![Formula](https://ml-biomat.com/static/agent-math/11000e938578f6b9d3f45892.svg) | Corresponding equilibrium bath concentration, μg/cm³. |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | Thickness-inclusive permeability coefficient used here, cm/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | Diffusion coefficient in the membrane, cm²/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Membrane thickness, cm. |
| ![Formula](https://ml-biomat.com/static/agent-math/9ac89127e3910a4715ad8104.svg) | Steady net mass flux, μg cm^{-2} s^{-1}. |
| ![Formula](https://ml-biomat.com/static/agent-math/aad6f74707cc379dcf3f69f1.svg) | Donor and receiver bath concentrations, μg/cm³. |
| ![Formula](https://ml-biomat.com/static/agent-math/12d771b3a5eff76e275bd9c0.svg) | Mass-transfer rate, μg/s; the dot denotes a time derivative. |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Effective exposed area, cm². |

Assume a uniform planar membrane, rapid interfacial partitioning, negligible external-layer resistance and no reaction. D=10⁻⁶ cm²/s, K=0.5 and L=0.05 cm give P=10⁻⁵ cm/s. A concentration difference of 100 μg/cm³ and area of 1 cm² give 0.001 μg/s, or 3.6 μg/h.

Consider a membrane 0.5 mm thick, equivalent to 0.05 cm, with diffusivity 10⁻⁶ cm²/s and partition coefficient 0.5. The resulting P is 10⁻⁵ cm/s. At donor concentration 100 μg/mL and near-zero receiver concentration, flux is 0.001 μg per square centimeter per second, or 3.6 μg per square centimeter per hour. With one square centimeter exposed, total transfer rate is 3.6 μg/h. Doubling area doubles that total under otherwise unchanged conditions. The example exports these quantities so that each conversion between centimeters, milliliters, seconds and hours can be checked directly.

The same P can arise from different combinations. Doubling partition coefficient while halving diffusivity preserves their product and can preserve the steady slope, even though membrane storage and the approach to steady state differ. A late straight line alone therefore often cannot identify both entry and mobility. An independent equilibrium partition experiment can supply one contribution. Under suitable conditions, time-lag analysis can supply diffusion information, which can then be combined with steady flux to estimate partitioning. Each independent measurement reduces the range of mechanisms consistent with the same cumulative curve.

Surrounding liquid layers can add resistances in series. Molecules traverse the donor-side layer, membrane and receiver-side layer; at steady state each transmits the same net amount, while the total concentration difference is distributed across the segments. Stronger mixing thins the external layers. A substantial increase in total flux then indicates that some driving force was previously spent across those layers. This contribution is particularly visible for thin or highly permeable materials. Thickness comparisons combined with controlled mixing help distinguish transport in the material from transport near the apparatus interfaces.

## Turn two compartments into an interpretable measurement

For a porous material, abundant pores do not by themselves establish easy passage for a particular molecule. Connectivity, path tortuosity, entrance wetting and adsorption to pore walls all affect effective transport. A large void visible in a micrograph may be a local space that does not connect to the other surface. Combining structural imaging with tracers of different sizes and surface properties helps separate these features. Tracer selection should consequently reflect the molecules relevant to the application, alongside analytical convenience, so that an easily detected dye does not silently replace the transport question originally being asked.

A basic diffusion cell contains donor and receiver compartments with the specimen clamped between them. The relevant area is the exposed opening, not the area of the entire cut specimen. Edge sealing must prevent bypass: target appearing in the receiver after leaking around the specimen has not necessarily crossed the material. Measure thickness in a hydration and loading state relevant to the experiment. Dry thickness, freely swollen thickness and compressed thickness can differ. Soft gels also require checking whether clamping locally compresses, damages or punctures the sample, changing the intended transport geometry.

Remove bubbles from the active region so that receiver liquid contacts the intended surface. A bubble can reduce wetted area and change a local transport path. Allow both compartments to approach the intended temperature before defining the start, because temperature affects both liquid and material. Mixing should maintain uniform compartment concentrations without dislodging the specimen or creating pressure-driven flow. Recording volumes, liquid levels, exposed area, specimen orientation and mixing connects geometry and handling to the subsequent flux calculation. These details become especially informative when nominally identical specimens produce different initial transients.

Barrier integrity can be checked with an independent measurement appropriate to the specimen. Dense films require attention to cracks and pinholes; cell barriers require continuous coverage and a defined barrier state; tissue specimens require consideration of preparation and storage. Electrical resistance, tracer passage and imaging observe different aspects. An ion-sensitive electrical quantity need not track neutral macromolecule flux in a simple ratio. The integrity check identifies damage or bypass outside the intended specimen definition while preserving genuine biological or material variation. Its interpretation should follow the object and measurement conditions rather than a universal threshold borrowed from another system.

Receiver analysis follows the preceding chapter's mass ledger. When sampled liquid is replaced, previously removed target must be added to the current receiver amount before dividing by area. Calibration should match the actual medium, with stability and recovery checked through incubation, filtration and handling. Suitable donor measurements establish whether its concentration is genuinely constant. Endpoint measurements of donor residue, cumulative receiver amount and material-retained target distinguish transmitted molecules from stored molecules and from changes in the molecular form detected by the assay. This accounting is especially useful when the receiver curve appears unexpectedly low.

Finite volumes change the driving force over long times. A finite donor loses concentration as material leaves, while an accumulating receiver gains concentration; their difference shrinks even when membrane properties remain constant. The example connects a 2 mL donor initially containing 100 μg/mL to a 10 mL target-free receiver. In a two-compartment model that neglects membrane storage, both eventually reach the same concentration, while the receiver contains more mass because its volume is larger. Conservation and volume explain this plateau without requiring the membrane to change its transport properties.

The experimental unit matters when specimens have biological variability. Several pieces cut from one tissue donor share that donor's characteristics, and repeated samples from one diffusion cell share the same barrier. Preserving donor, specimen and cell identifiers allows comparisons at their proper levels. For manufactured membranes, independent preparation batches may be the relevant additional level. A balanced allocation of specimens across formulations and measurement positions prevents a systematic apparatus or batch effect from aligning with the treatment being compared. These records support interpretation of differences in both steady transport and transient behavior.

## Extract separate information from slope and time lag

At the start, the membrane has not established its steady concentration distribution. Molecules enter at the upstream boundary while downstream flux gradually develops as the internal distribution spreads. If boundaries remain fixed, cumulative received amount eventually approaches a straight line. Extending that late line to the time axis defines the time lag. This intercept is neither the arrival time of the first molecule nor the moment the instrument first detects a signal. It summarizes the entire transient relative to the eventual constant transfer rate through a geometric construction.

$$
M(t)\simeq AJ_{\mathrm{ss}}(t-t_{\mathrm{lag}}),\qquad t_{\mathrm{lag}}=\frac{L^2}{6D},\qquad D=\frac{L^2}{6t_{\mathrm{lag}}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/46f382af9057c20a2d8676c0.svg) | Cumulative mass crossing into the receiver, μg. |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Effective exposed area, cm². |
| ![Formula](https://ml-biomat.com/static/agent-math/9ac89127e3910a4715ad8104.svg) | Steady flux, μg cm^{-2} s^{-1}. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Elapsed experimental time, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/f8ee0947ec3a7b9f620bb565.svg) | Time-axis intercept of the extrapolated steady line, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Uniform planar membrane thickness, cm. |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | Concentration-independent membrane diffusivity, cm²/s. |

For an initially target-free planar membrane with fixed upstream concentration and near-zero downstream concentration, L=0.05 cm and D=10⁻⁶ cm²/s give 416.667 s, or 6.944 min. The linear expression is a late-time extrapolation; early cumulative amounts require the full transient solution.

For a uniform planar membrane initially free of target, with constant diffusivity, fixed upstream concentration and near-zero downstream concentration, lag scales with thickness squared and inversely with diffusivity. The 0.5 mm membrane gives about 416.7 s, or 6.94 min. Doubling thickness halves the steady flux but quadruples the lag. These changes arise from the effect of distance on the steady gradient and on development of the profile, respectively. Plotting them together provides more structural information than reporting a single coefficient, and suggests a useful thickness-series experiment.

![Constructed four-panel diagnostics: steady line and lag, fit-start sensitivity, thickness series and finite-volume effects. Panel D is a separate two-compartment model neglecting membrane storage to illustrate changing external driving force; A–C retain the fixed-boundary planar-membrane transient.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/1c62fc14dd646dfbbcc28869.svg?v=1c62fc14dd64)

Figure 3Constructed four-panel diagnostics: steady line and lag, fit-start sensitivity, thickness series and finite-volume effects. Panel D is a separate two-compartment model neglecting membrane storage to illustrate changing external driving force; A–C retain the fixed-boundary planar-membrane transient.

Choose a fitting window by examining the curve and residuals. Including early points while the distribution is still developing shifts both fitted slope and intercept. The example moves the starting time progressively later and tracks the estimated lag; stabilization over an appropriate window provides a checkable basis for choosing the steady region. Extending too far can introduce donor depletion, receiver accumulation or specimen swelling. The longest possible interval is therefore not automatically the most physically interpretable one. The selected interval should retain the conditions represented by the equation being fitted.

The apparatus has a time response too. Tubing dead volume, detector response and the time needed for mixing can add delays resembling a membrane lag. An apparatus control without the target membrane, a reference with known transport behavior or an independent response measurement can quantify relevant contributions. Gas and liquid devices differ in driving force, units and detection, but share the same logic: characterize time introduced by the measurement chain before assigning the remaining transient to the material. That separation makes parameters more useful when predicting behavior after thickness or apparatus changes.

## Separate signatures of thickness, diffusion and partitioning

Donor concentration is fixed at 100 μg/mL, receiver concentration at zero and area at 1 cm². The curve uses the full planar-membrane transient; the dashed line is the late steady extrapolation.

[Figure: Cumulative permeation and steady extrapolation](https://ml-biomat.com/tutorials/experimental-methods/e05/en/#E05-plot)

## Observe local movement without waiting for complete passage

Fluorescence recovery after photobleaching takes a different route. A small region is made dark by bleaching fluorescent molecules, then observed with weaker illumination as brightness returns. Recovery generally reflects unbleached molecules entering while bleached molecules leave; it does not require every bleached molecule to become fluorescent again. Axelrod and colleagues' 1976 analysis connected recovery with mobility, flow and the mobile population. In gels and cells, this local method can reveal dynamics at a chosen spatial scale without first imposing a macroscopic concentration difference across the complete specimen.

Begin with three intensities: before bleaching, immediately after bleaching and at the recovery plateau. The recovered fraction of the initial brightness loss estimates the mobile fraction under the relevant model. If normalized brightness is initially 1, falls to 0.2 and recovers to 0.8, bleaching removed 0.8 and recovery restored 0.6, giving a fraction of 0.75. Interpretation depends on observation time. A population that does not recover within the current window may be immobilized or may exchange slowly. Longer observations and altered bleach-region sizes help distinguish these possibilities.

$$
f_{\mathrm{mob}}=\frac{I_{\infty}-I_0}{I_{\mathrm{pre}}-I_0}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/43f47e963875c759940d11ea.svg) | Mobile fraction estimated under this recovery model, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/c59d25a349209f75166a8a12.svg) | Plateau intensity after recovery with consistent background and acquisition-bleach correction, consistent arbitrary intensity units. |
| ![Formula](https://ml-biomat.com/static/agent-math/6e4f2807ce72e4cab3957130.svg) | Intensity immediately after bleaching, in the same units. |
| ![Formula](https://ml-biomat.com/static/agent-math/1056405dcb44d58478d34a61.svg) | Prebleach intensity, in the same units. |

Divide recovered brightness by the initial brightness loss. Ipre=1, I0=0.2 and I∞=0.8 give 0.6/0.8=0.75. Observation must establish the relevant plateau, with background and bleaching handled consistently with the measurement model.

A larger bleached region generally takes longer to refill from its surroundings. The example uses an ideal two-dimensional Gaussian bleaching model to connect central recovery with spatial extent. Increasing the radius from 5 to 10 μm quadruples the time required to reach the same fraction of recovery, illustrating squared-distance scaling in microscopy. If observed timing changes differently with bleach size, binding, dissociation, directed flow or heterogeneous structure can be investigated. Estimating a diffusion coefficient requires a model matched to the actual bleach profile, dimensionality and observed region rather than a universal conversion from a recovery half-time.

![Constructed ideal two-dimensional Gaussian-bleach images and central-intensity curves with a shared 0–1 color range and 5 μm scale bars. Defaults are diffusivity 1 μm²/s, radius 5 μm and mobile fraction 0.75. Curves compare region size and mobile fraction; images are model outputs, not microscopy measurements.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d81176fb9de0649feb5f7926.svg?v=d81176fb9de0)

Figure 4Constructed ideal two-dimensional Gaussian-bleach images and central-intensity curves with a shared 0–1 color range and 5 μm scale bars. Defaults are diffusivity 1 μm²/s, radius 5 μm and mobile fraction 0.75. Curves compare region size and mobile fraction; images are model outputs, not microscopy measurements.

Real images require attention to background, ongoing bleaching during acquisition and specimen drift. A reference region not exposed to the strong bleach can show whether overall brightness declines; a background region estimates non-target signal. Molecules can move during the bleach pulse itself, so the actual post-bleach distribution may differ from an idealized sharp initial boundary. Reversible dark states, label binding and light-induced changes in the local environment can also contribute. Inspecting raw images and spatial profiles before interpreting one averaged intensity curve preserves evidence of these effects and helps determine an appropriate correction.

Local recovery and whole-membrane flux are complementary. Rapid local motion may indicate easy travel within water-filled channels, while unfavorable entry partitioning still produces little net passage. Conversely, a material can retain a large amount while showing slow local mobility. Combining partitioning, local diffusion and macroscopic permeation separates entry, movement and traversal. For molecules consumed by cells or reacting with the network, reaction or consumption measurements add their destinations to this picture. The transport measurements then support an account of both where molecules can move and where they are ultimately used or retained.

## Connect spatial profiles to the receiver curve with complete calculations

Different parameters have different sensitivity to geometric error. Calculating the P defined here directly from steady slope, area and external concentration difference does not require thickness as another input. Estimating diffusivity from time lag does require thickness, and it enters squared. If thickness is overestimated by 10% while other inputs are unchanged, estimated diffusivity is overestimated by about 21%. For swelling specimens, this difference explains why thickness should be measured in a state relevant to transport. Recording variation across the specimen is more informative than relying only on the nominal dimensions of a fabrication mold.

Partition measurements also need a defined molecular population. Total target stored in a material may include both mobile molecules and molecules bound to comparatively immobile sites. Substituting total uptake into a simple mobile-solute model without accounting for binding can therefore change the meaning of the inferred diffusivity. Measuring uptake together with release after transfer to target-free medium helps reveal reversibility and slow exchange. Local fluorescence observations add a further view of mobility. These complementary observations make it possible to choose between a simple solution–diffusion description and a model that explicitly includes storage or binding.

The complete example calculates how an initially target-free planar membrane develops concentration under fixed upstream and zero downstream boundaries. It exports position–time concentration arrays, constructed receiver-mass observations, fitted parameters and four figures. The spatial heatmap and cumulative curve share one parameter set, so the process can be followed between them: concentration first grows near the entrance, downstream flux approaches its steady value, and cumulative mass approaches a straight line. Numerical checks compare the late result with an independent steady expression and verify zero cumulative transfer at the initial instant.

### Complete Python: Membrane concentration fields, time lag and local recovery

The code exports concentration arrays, constructed receiver amounts, fitted values and four figures. Independent initial and late steady conditions check the full membrane solution.

```
"""Planar diffusion, steady permeation, time-lag analysis and idealized FRAP."""
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


def permeated(time,D=1e-6,L=.05,K=.5,C=100.,area=1.):
    t=np.atleast_1d(time).astype(float);n=np.arange(1,201)[:,None]
    correction=np.sum((-1.)**n/n**2*np.exp(-D*n*n*np.pi**2*t[None,:]/L**2),axis=0)
    q=area*D*K*C/L*(t-L**2/(6*D)-2*L**2/(np.pi**2*D)*correction)
    return np.where(t==0,0,np.maximum(q,0))

def profile(x,time,D=1e-6,L=.05,K=.5,C=100.):
    x=np.asarray(x);n=np.arange(1,201)[:,None]
    if time==0:return np.where(x==0,K*C,0.)
    return K*C*(1-x/L-2/np.pi*np.sum(np.sin(n*np.pi*x/L)/n*np.exp(-D*n*n*np.pi**2*time/L**2),axis=0))

def frap_center(time,D=1.,radius=5.,mobile=.75,depth=.8):
    return 1-depth*((1-mobile)+mobile*radius**2/(radius**2+4*D*np.asarray(time)))

def main(output,language):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    from matplotlib import font_manager
    fonts={f.name for f in font_manager.fontManager.ttflist};font=next((f for f in ['Microsoft YaHei','Noto Sans CJK SC','SimHei'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[font,'DejaVu Sans'] if language=='zh' else ['DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','axes.prop_cycle':plt.cycler(color=['#186e83','#cd803f','#8160a1','#3c8a6a'])})
    tr=lambda z,e:z if language=='zh' else _label(e)
    def save(fig,n):fig.savefig(output/f'{n}-{language}.svg',bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(1,3,figsize=(12,4.2))
    for a in ax:a.set(xlim=(0,10),ylim=(0,10));a.axis('off')
    ax[0].add_patch(Rectangle((1,2),8,6,facecolor='#e2eef0'));rng=np.random.default_rng(505)
    ax[0].scatter(rng.uniform(1.5,4.8,40),rng.uniform(2.5,7.5,40),s=12,color='#186e83');ax[0].scatter(rng.uniform(5.2,8.5,12),rng.uniform(2.5,7.5,12),s=12,color='#186e83');ax[0].add_patch(FancyArrowPatch((3,1.5),(7,1.5),arrowstyle='->',mutation_scale=17,color='#cd803f'));ax[0].set_title(tr('1855 · Fick：浓度梯度与通量','1855 · Fick: gradient and flux'));ax[0].text(5,.5,tr('从高浓度到低浓度的净传输','Net transfer from high to low concentration'),ha='center',fontsize=9)
    ax[1].add_patch(Rectangle((1,2),3.5,6,facecolor='#a2cdd9'));ax[1].add_patch(Rectangle((5.5,2),3.5,6,facecolor='#e2eef0'));ax[1].add_patch(Rectangle((4.5,2),1,6,facecolor='#8160a1'));ax[1].text(2.6,5,tr('供体','Donor'),ha='center');ax[1].text(7.3,5,tr('接收体','Receiver'),ha='center');ax[1].add_patch(FancyArrowPatch((3,1.5),(7,1.5),arrowstyle='->',mutation_scale=17,color='#cd803f'));ax[1].set_title(tr('1920 · Daynes：穿膜的时间滞后','1920 · Daynes: permeation time lag'));ax[1].text(5,.5,tr('膜内先建立浓度分布','A concentration profile develops in the membrane'),ha='center',fontsize=8.5)
    ax[2].add_patch(Rectangle((1,2),8,6,facecolor='#3c8a6a'));ax[2].add_patch(Circle((5,5),1.4,color='#123d36'));ax[2].add_patch(FancyArrowPatch((2,5),(4,5),arrowstyle='->',mutation_scale=17,color='white'));ax[2].add_patch(FancyArrowPatch((8,5),(6,5),arrowstyle='->',mutation_scale=17,color='white'));ax[2].set_title(tr('1976 · Axelrod 等：漂白后的恢复','1976 · Axelrod et al.: recovery after bleaching'));ax[2].text(5,1,tr('跟随明亮分子进入暗区','Follow bright molecules entering a bleached region'),ha='center',fontsize=9);fig.tight_layout();save(fig,'history')
    x=np.linspace(0,.05,201);times=np.linspace(0,1800,181);field=np.array([profile(x,t) for t in times]);fig,ax=plt.subplots(1,2,figsize=(11,4.8));im=ax[0].imshow(field,origin='lower',aspect='auto',extent=(0,.5,0,30),cmap='cividis',vmin=0,vmax=50);fig.colorbar(im,ax=ax[0],label=tr('膜内浓度 / μg mL⁻¹','Membrane concentration / μg mL⁻¹'));ax[0].set(xlabel=tr('膜内位置 / mm','Position in membrane / mm'),ylabel=tr('时间 / min','Time / min'),title=tr('A  浓度如何逐渐建立','A  Development of concentration'))
    for t in [30,120,600,1800]:ax[1].plot(x*10,profile(x,t),label=f'{t/60:g} min')
    ax[1].plot(x*10,50*(1-x/.05),'--',color='#8f979a',label=tr('稳态','Steady state'));ax[1].set(xlabel=tr('膜内位置 / mm','Position in membrane / mm'),ylabel=tr('浓度 / μg mL⁻¹','Concentration / μg mL⁻¹'),title=tr('B  从弯曲分布到稳定梯度','B  Curved profiles approach a stable gradient'));ax[1].legend(fontsize=9);fig.tight_layout();save(fig,'profiles')
    t=np.linspace(0,7200,121);q=permeated(t);noisy=q+rng.normal(0,.01,len(t));mask=t>=2400;slope,intercept=np.polyfit(t[mask],noisy[mask],1);lag=-intercept/slope;dfit=.05**2/(6*lag);pfit=slope/100
    np.savetxt(output/'permeation.csv',np.column_stack([t,t/60,q,noisy]),delimiter=',',header='time_s,time_min,ideal_received_ug,constructed_observed_ug',comments='');np.savez(output/'profiles.npz',position_cm=x,time_s=times,concentration_ug_ml=field)
    fig,ax=plt.subplots(2,2,figsize=(11.4,7.3));ax=ax.ravel();ax[0].plot(t/60,noisy,'.',ms=3,label=tr('构造观测','Constructed observations'));ax[0].plot(t/60,slope*t+intercept,label=tr('40 min 后拟合','Fit after 40 min'));ax[0].scatter([lag/60],[0],color='#cd803f',zorder=5);ax[0].set(xlabel=tr('时间 / min','Time / min'),ylabel=tr('接收量 / μg','Received mass / μg'),title=tr('A  稳态斜率与时间轴截距','A  Steady slope and time-axis intercept'));ax[0].legend(fontsize=8)
    starts=np.arange(120,4201,120);fits=[]
    for start in starts:
        m=t>=start;ss,ii=np.polyfit(t[m],noisy[m],1);fits.append(-ii/ss/60)
    ax[1].plot(starts/60,fits);ax[1].axhline(.05**2/6e-6/60,color='#cd803f',ls='--');ax[1].set(xlabel=tr('拟合开始时间 / min','Fit start time / min'),ylabel=tr('估计滞后 / min','Estimated lag / min'),title=tr('B  拟合窗口的敏感性','B  Sensitivity to fitting window'))
    for L in [.025,.05,.1]:ax[2].plot(t/60,permeated(t,L=L),label=f'{L*10:g} mm')
    ax[2].set(xlabel=tr('时间 / min','Time / min'),ylabel=tr('接收量 / μg','Received mass / μg'),title=tr('C  厚度改变速率与滞后','C  Thickness changes rate and lag'));ax[2].legend(fontsize=9)
    finite_t=np.linspace(0,48*3600,300);qfinite=(100*2*10/12)*(-np.expm1(-1e-5*(1/2+1/10)*finite_t));ax[3].plot(finite_t/3600,qfinite,label=tr('有限供体与接收体','Finite donor and receiver'));ax[3].plot(finite_t/3600,.001*finite_t,'--',label=tr('恒定驱动力外推','Constant-driving-force extrapolation'));ax[3].axhline(200,color='#8f979a',ls=':');ax[3].set(xlabel=tr('时间 / h','Time / h'),ylabel=tr('接收量 / μg','Received mass / μg'),title=tr('D  有限容积改变长期驱动力','D  Finite volumes change long-term driving force'));ax[3].legend(fontsize=8);fig.tight_layout();save(fig,'analysis')
    grid=np.linspace(-15,15,181);xx,yy=np.meshgrid(grid,grid);r2=xx**2+yy**2;fig=plt.figure(figsize=(11,7));gs=fig.add_gridspec(2,3,height_ratios=[1,1.1]);axs=[fig.add_subplot(gs[0,j]) for j in range(3)]
    for a,tm in zip(axs,[0,5,30]):
        intensity=1-.8*(.25*np.exp(-r2/25)+.75*25/(25+4*tm)*np.exp(-r2/(25+4*tm)));a.imshow(intensity,origin='lower',extent=(-15,15,-15,15),cmap='viridis',vmin=0,vmax=1);a.plot([5,10],[-12,-12],color='#17333a',lw=3);a.text(7.5,-10,'5 μm',ha='center',color='#17333a',fontsize=8);a.set_title(f'{tm} s');a.set_xticks([]);a.set_yticks([])
    a=fig.add_subplot(gs[1,:]);ft=np.linspace(0,120,241)
    for radius,mobile in [(5,.75),(10,.75),(5,1)]:a.plot(ft,frap_center(ft,radius=radius,mobile=mobile),label=tr(f'半径 {radius} μm，可动比例 {mobile:.2f}',f'Radius {radius} μm, mobile fraction {mobile:.2f}'))
    a.set(xlabel=tr('漂白后时间 / s','Time after bleaching / s'),ylabel=tr('中心归一化亮度','Normalized central brightness'),title=tr('理想二维高斯漂白模型：空间扩散与可动比例','Ideal 2D Gaussian-bleach model: spreading and mobile fraction'));a.legend(fontsize=9);fig.tight_layout();save(fig,'frap')
    summary={'nominal':{'D_cm2_s':1e-6,'partition':.5,'thickness_cm':.05,'P_cm_s':1e-5,'steady_flux_ug_cm2_h':3.6,'lag_s':.05**2/6e-6,'lag_min':.05**2/6e-6/60},'fit':{'slope_ug_s':float(slope),'lag_s':float(lag),'D_cm2_s':float(dfit),'P_cm_s':float(pfit)},'scaling':{'double_thickness_flux_ratio':.5,'double_thickness_lag_ratio':4,'double_distance_time_ratio':4},'frap':{'prebleach':1,'immediate':float(frap_center(0)),'plateau':.8,'mobile_fraction':.75,'half_recovery_s':6.25,'at_half_recovery':float(frap_center(6.25))},'finite_bath':{'initial_mass_ug':200,'equilibrium_received_ug':100*2*10/12},'checks':{'q_at_zero':float(permeated([0])[0]),'late_mass_ug':float(permeated([7200])[0]),'late_linear_ug':.001*(7200-.05**2/6e-6)}}
    assert abs(summary['checks']['late_mass_ug']-summary['checks']['late_linear_ug'])<1e-9;assert abs(frap_center(6.25)-.5)<1e-12;assert np.all(field>=-1e-9)
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

The finite-volume two-compartment model and fixed-boundary membrane model represent different experiments. The former neglects membrane storage and uses an established transfer relation, whereas the latter retains development of concentration inside the membrane. Keeping them distinct makes it clear whether curve bending comes from the internal transient or an evolving external driving force. The fluorescence images are likewise labeled ideal model images. Actual measurements can use the same quantities and units, followed by a model matched to the apparatus, geometry and observation method rather than assuming all illustrated curves describe one specimen.

Change only thickness first, then only partition coefficient, then only diffusivity. Thickness changes both steady slope and lag. Partition coefficient scales the amount transferred in this linear model without changing the profile-development timescale. Diffusivity changes both mobility and final flux. This sequence identifies the different signatures parameters leave in data. If an experiment observes only one signature, the comparison suggests what additional information is useful: a partition measurement, more observations during the transient, or a local mobility experiment. Parameter estimation becomes a question of collecting distinguishable evidence rather than adding more adjustable values.

A useful transport report retains molecular identity, material state, area, thickness, temperature, medium, concentration boundaries and parameter definition. These details allow its result to guide a new thickness design, a carrier comparison or an estimate of cellular supply distance. The cellular experiments that follow begin by establishing comparable starting conditions. Even when material transport is identical, different initial cell numbers, viability and spatial distributions can create different consumption and observations. Making both transport and biological state measurable connects the two parts of the research problem.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/E05.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Fick (1855). On liquid diffusion](https://doi.org/10.1080/14786445508641925)

   Historical original paper on liquid diffusion and concentration gradients.
2. [Daynes (1920). The process of diffusion through a rubber membrane](https://doi.org/10.1098/rspa.1920.0034)

   Historical work on gas transport in rubber and the time-lag method.

   Historical reference; no assets reproduced.
3. [Imperial College London ReCoDe: Time Lag Analysis, A Theoretical Foundation](https://raw.githubusercontent.com/ImperialCollegeLondon/ReCoDe-permeation-analysis-app/main/docs/02-Theoretical-Background.md)

   Boundary conditions, steady extrapolation, units and time-lag analysis.
4. [COMSOL: Diffusion Equation](https://www.comsol.com/multiphysics/diffusion-equation)

   Fick’s laws, local conservation and constant-diffusivity conditions.
5. [COMSOL: Diffusion Length and Timescales](https://www.comsol.com/multiphysics/diffusion-length-and-time-scales)

   Connection between squared distance and diffusion timescale.
6. [Axelrod et al. (1976). Mobility measurement by analysis of fluorescence photobleaching recovery kinetics](https://pubmed.ncbi.nlm.nih.gov/786399/)

   Original analysis of molecular mobility and mobile populations using photobleaching recovery.

   Original abstract reference; no images reproduced.
7. [FDA (2022 draft). In Vitro Permeation Test Studies for Topical Drug Products Submitted in ANDAs](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/in-vitro-permeation-test-studies-topical-drug-products-submitted-andas)

   Experimental design for diffusion cells, barrier integrity, receiving medium and sampling.

   Official draft guidance; technical reading, with no assets reproduced.
