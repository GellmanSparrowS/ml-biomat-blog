# Compression testing: How soft materials carry load

Source: https://ml-biomat.com/tutorials/experimental-methods/m02/en/
Language: en

Start from contact and lateral expansion to understand nonlinear load support, end constraints and drainage time.

## Why a soft material sometimes supports a load and sometimes gives way

Press a wet sponge with a finger. It initially pushes back, then water escapes and the finger can move farther down. An eraser also becomes shorter under compression, but its sides spread outward without an obvious stream of liquid. Both objects feel soft, yet their load-bearing processes differ. When studying cartilage replacements, cell-culture hydrogels or cushioning foams, compression testing separates this familiar sensation into measurable quantities: force, shortening, elapsed time and the directions in which the specimen is allowed to deform or drain. These quantities connect a material description to a particular use. A scaffold that supports a brief touch may behave quite differently during a sustained load.

The machine performs a simple action. A specimen sits between two platens, one platen approaches the other, and a load cell records the reaction force. Force and displacement provide a stiffness measurement, but the machine does not know whether the object is a straight cylinder, an uneven piece of tissue or a drying film. Geometry, contact and friction all enter the record. Begin by choosing the question. Comparing initial softness between two gel formulations requires comparable geometry, hydration and loading history. Evaluating a cushion at large deformation calls for working stress, recovery and changes during repeated compression. A single slope taken from the first few points answers only one part of either investigation.

Articular cartilage adds a useful historical perspective. Its solid matrix and interstitial fluid interact while carrying load. In 1980, Mow, Kuei, Lai and Armstrong published a study of biphasic creep and stress relaxation in cartilage compression. Here, biphasic refers to solid and fluid constituents. This framework makes the fluid contribution part of the mechanical problem, helping explain why a force can decrease while displacement remains fixed. The original diagram below places that conceptual development beside three mechanical boundary conditions. Knowing that water is present is only the beginning: its escape routes, and the freedom of the solid matrix to move sideways, also belong in the experiment.

![Original diagrams of free expansion, frictional barrelling, rigid confinement and solid–fluid load sharing highlighted by the 1980 biphasic cartilage study. Shapes compare boundary conditions, not photographs of an experiment.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/f4c149fdab05f3e9d308491c.svg?v=f4c149fdab05)

Figure 1Original diagrams of free expansion, frictional barrelling, rigid confinement and solid–fluid load sharing highlighted by the 1980 biphasic cartilage study. Shapes compare boundary conditions, not photographs of an experiment.

## A contact point separates platen travel from specimen compression

Imagine a cylindrical gel with two flat, parallel ends. Its original height is the distance between those ends, and its original area is the circular cross-section perpendicular to loading. Engineering compression strain is the fraction of height lost. Shortening a 2 mm specimen by 0.2 mm gives a strain of 0.1, displayed as 10%. This chapter assigns positive signs to compression strain and compressive stress so that the loading curves rise to the right. Another common convention assigns positive values to tension and negative values to compression. The physical experiment is unchanged, but the definitions should be checked before combining files from different instruments or software packages.

$$
\varepsilon_c=\frac{H_0-H}{H_0},\qquad\lambda=\frac{H}{H_0}=1-\varepsilon_c,\qquad P=\frac{F}{A_0}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1953a63a6cc4d667632db12b.svg) | Engineering compression strain, dimensionless and positive in compression. |
| ![Formula](https://ml-biomat.com/static/agent-math/f510273c694c65128635cc0b.svg) | Original height, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/6d6950da29507eb4f6b78d53.svg) | Current height, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | Axial height ratio, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | Nominal compressive stress, N/mm²; multiply by 1000 for kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | Axial compressive reaction, N. |
| ![Formula](https://ml-biomat.com/static/agent-math/0c430ee48d22be2e69d0f3ad.svg) | Original cross-sectional area, mm². |

H0=2 mm and H=1.8 mm give εc=0.1 and λ=0.9. Dividing force by the area perpendicular to loading gives mean nominal stress.

The platen may initially move through a gap before touching the specimen. Once contact begins, small surface irregularities can flatten before the full end face carries load. Consequently, travel measured from the first saved row is not automatically specimen shortening. The teaching record places actual contact at a stage closure of 0.06 mm. Relative to a 2 mm height, that distance is already 3% strain, enough to dominate an initial modulus estimate. Defining contact as the first positive force is also sensitive to noise, a force offset and sometimes a liquid meniscus. Retain measurements before contact, estimate the baseline and use the curve together with an image of the interface to identify a plausible contact interval.

Soft specimens require suitable dimensional measurements. Closing a caliper firmly around a gel can compress it before the reading is taken. An oblique cut produces early contact on one side and an apparently compliant initial response. Calibrated images in the chosen liquid can provide lateral dimensions, while parallel cutting tools help produce reproducible end faces. Measure individual specimens rather than assigning the nominal mould diameter to all of them. Diameter is squared when calculating circular area: overestimating diameter by 5% overestimates area by 10.25% and lowers the calculated stress by about 9.3%. This error rescales the whole curve. Collecting more force points does not average it away because the same incorrect denominator appears in every point.

Height also determines the meaning of a prescribed stage speed. A speed of 0.2 mm per minute corresponds to 10% engineering strain per minute for a 2 mm specimen, but 5% per minute for a 4 mm specimen. Record the speed and the corresponding strain rate, including whether they remain constant during the test. Short specimens reduce some instability problems but make contact uncertainty, uneven surfaces and machine deformation larger fractions of total travel. Taller specimens can reduce end effects while becoming more vulnerable to tilting or buckling. Select the height-to-diameter ratio for the material and fixture, then inspect the actual deformation. A ratio recommended for a metal specimen does not automatically resolve the competing issues in a compliant hydrogel.

## Whether the sides can expand changes what compression measures

Incompressible does not mean that an object cannot be shortened. It means that its volume changes very little. If a uniform cylinder retains its volume while its height falls to 0.8 of the original value, its area must increase to 1.25 of the original value. A circular cross-section therefore increases its radius by a factor of about 1.118. With sliding end faces, the specimen can become shorter and wider relatively uniformly. Put the same material inside a rigid sleeve and prevent lateral expansion, and the same axial shortening now demands volume change or another internal process. The resulting load belongs to a different boundary-value problem even though the material formulation is identical.

Platen friction lies between free sliding and complete lateral confinement. The end faces resist outward motion while material farther from the platens can expand, producing a barrel-shaped side profile. Stress and strain then vary through the specimen. Force divided by original area remains a useful average nominal stress, but it is no longer a direct measurement of a uniform uniaxial response. A side-view image can reveal this change more clearly than an extra decimal place in the reported modulus. Lubrication changes sliding conditions, yet the lubricant must be compatible with the material. Penetration, swelling and expulsion during loading can all change the interface. A slippery surface at the beginning does not establish a constant friction condition throughout a large compression.

$$
M=\frac{E(1-\nu)}{(1+\nu)(1-2\nu)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/34058a2a5d1de088feed7d98.svg) | Constrained compression modulus at zero transverse strains, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | Young modulus for free uniaxial small deformation, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/5064898bae7c73820eaab47c.svg) | Poisson ratio, dimensionless; this comparison uses 0≤ν<0.5. |

Isotropic linear elasticity with both transverse strains zero. E=60 kPa and ν=0.45 give M=227.586 kPa. Lateral constraints create lateral stresses.

Poisson's ratio relates transverse and axial strains at small deformation. For an isotropic linear elastic solid with free lateral expansion, the axial modulus is Young's modulus. When both transverse strains are constrained to zero, the relevant quantity is the constrained compression modulus. For Young's modulus 60 kPa and Poisson's ratio 0.45, the latter is approximately 227.6 kPa, nearly 3.8 times larger. No change of material was needed. As Poisson's ratio approaches 0.5, the constrained modulus rises rapidly because a nearly volume-preserving solid has difficulty becoming shorter with all lateral expansion blocked. The limiting expression also explains why inserting exactly 0.5 into its denominator is not a valid calculation of an ordinary finite modulus.

Unconfined compression, confined compression and indentation serve different questions. The first exposes overall shape changes, the second controls lateral deformation and can provide a well-defined drainage geometry, and a spherical indenter probes a smaller region around its contact. All three may produce numbers in kPa, but their sampled volumes and inverse models differ. In a heterogeneous tissue, local indentation and whole-specimen compression can therefore supply complementary information. Draw the specimen and the directions of force, displacement and drainage before choosing a parameter name. That drawing makes it easier to decide whether a difference between methods reflects heterogeneity, boundary conditions or an actual disagreement in measurement.

![Left: constrained modulus of an isotropic linear elastic material. Right: area and radius changes of a uniform constant-volume cylinder. The panels separately explain boundaries and geometry; they are not a strain-dependent Poisson-ratio model.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/bffc0c9de90b063e21323751.svg?v=bffc0c9de90b)

Figure 2Left: constrained modulus of an isotropic linear elastic material. Right: area and radius changes of a uniform constant-volume cylinder. The panels separately explain boundaries and geometry; they are not a strain-dependent Poisson-ratio model.

## A steepening curve can arise from changing shape

Over a sufficiently small strain interval, many compliant solids have an approximately proportional stress–strain response. Its slope defines an initial modulus. Extending that straight line to 40% compression is a separate modelling decision. Height, cross-sectional area and network configuration all change substantially during such a deformation. The example uses an incompressible neo-Hookean solid to construct a fully reproducible curved response. A single shear modulus sets its elastic scale, while finite deformation changes the relation between load and shortening. The model returns to linear elasticity at small strains. It is especially useful for separating two statements that are often confused: the curve has become nonlinear, and the specimen has accumulated irreversible damage.

$$
P=\mu(\lambda^{-2}-\lambda),\qquad E_0=3\mu,\qquad \sigma_c=\lambda P
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | Nominal compressive stress, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | Shear modulus, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | Current/original height, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/89ba16e9e7f11a7da33694e2.svg) | Initial small-strain Young modulus, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/23ed93a4937fe7721e1ddcf7.svg) | True compressive stress on current area, kPa. |

Uniform uniaxial deformation of an incompressible neo-Hookean solid with free lateral motion; area A=A0/λ. μ=20 and λ=0.8 give P=15.25, E0=60 and σc=12.2 kPa.

Set the shear modulus to 20 kPa. The initial Young's modulus is then 60 kPa. At 20% compression, the height ratio is 0.8 and the nominal compressive stress is 15.25 kPa. Extending the initial tangent would instead predict 12 kPa. A cylinder of radius 3 mm has an original area of about 28.274 mm², so the nonlinear prediction corresponds to approximately 0.431 N. Units are crucial in this step: 1 kPa is 0.001 N/mm². Missing that factor of one thousand still produces a smooth graph in a plotting program, but the graph no longer represents the stated specimen. Checking one force by hand is a quick and powerful safeguard against this kind of error.

The same state can also be described by true stress, using current rather than original area. Under uniform volume-preserving compression, current area is larger, so true compressive stress is lower than nominal compressive stress. The 20% example gives 12.2 kPa instead of 15.25 kPa. Uniform tension produces the opposite ordering because its current area becomes smaller. In both cases the explanation is simply the denominator. The figure plots both definitions using the same force and deformation. They are two descriptions of one state, not conflicting experiments. Once a specimen barrels, collapses locally or loses fluid, current area and volume need their own measurements or an appropriate spatial model.

The fitting example estimates shear modulus, contact position and force baseline together. Each parameter has a different role: modulus mainly changes load level, contact position shifts the onset horizontally, and baseline shifts the force vertically. Measurements before contact help determine the baseline, while a useful deformation range helps separate stiffness from contact location. Fitting only a narrow segment can allow several parameter combinations to look almost identical. Independent contact or dimensional evidence then becomes more valuable than another optimiser setting. The residual plot shows what the selected model has left unexplained. Systematic curvature, a jump or a changing residual spread suggests a different issue from the small unstructured noise deliberately added here.

![Constructed record and full fit: precontact baseline, contact location, force residuals, initial tangent and two stress definitions for the same incompressible neo-Hookean response.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/6b9cc092dccfb141e1a92e13.svg?v=6b9cc092dccf)

Figure 3Constructed record and full fit: precontact baseline, contact location, force residuals, initial tangent and two stress definitions for the same incompressible neo-Hookean response.

## When force falls during a hold, where does the water go?

During rapid compression of a hydrated network, fluid cannot necessarily leave the pores immediately. Elevated internal pressure can support part of the applied load. With displacement held fixed, pressure redistributes toward draining boundaries and the measured force can decrease. A useful analogy is a reservoir connected to drainage routes: a longer route generally takes longer to equilibrate. The analogy concerns transport through space. Real tissues also contain elastic networks, changing permeability, oriented fibres and molecular relaxation. To isolate the effect of drainage length, the following calculation specifies a one-dimensional pressure-diffusion problem whose assumptions, initial state and boundaries can all be inspected.

$$
\frac{\partial p}{\partial t}=D\frac{\partial^2p}{\partial z^2},\qquad p(0,t)=p(H,t)=0,\qquad\tau_1=\frac{H^2}{\pi^2D}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/48c7b594e8628a17b991d4e6.svg) | Excess pressure relative to the bath, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time from the specified initial state, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | Constant pressure diffusivity, mm²/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/9032cb23a878659e74b670d3.svg) | Axial position in the layer, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/6d6950da29507eb4f6b78d53.svg) | Thickness of the layer with two drained faces, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/f59c766cfefc407124903879.svg) | Decay time scale of the slowest spatial mode, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | Pi, dimensionless. |

One-dimensional constant-D diffusion with zero excess pressure at both faces and initial interior pressure 10 kPa. H=2 mm and D=0.01 mm²/s give τ1=40.528 s; H=4 mm gives 162.114 s. Spatial pressure curvature drives temporal change.

The layer is 2 mm thick and drains through both faces. Excess pressure is maintained at zero on those faces, begins at 10 kPa in the interior and evolves with a pressure diffusivity of 0.01 mm²/s. Excess pressure is measured relative to the surrounding bath, so zero at the boundary does not mean zero absolute pressure. The equation says that the curvature of the pressure profile controls how quickly local pressure changes. Near a draining face, pressure first falls while the interior remains elevated. Later the entire profile declines. Several spatial profiles show this progression explicitly, giving a physical picture of drainage that a single falling force trace does not provide on its own.

The slowest exponential time scale for these two drained faces is approximately 40.53 s. Doubling thickness to 4 mm while retaining the same diffusivity increases that scale to approximately 162.11 s, a factor of four. This length-squared dependence comes from spatial diffusion, not from making every molecular process four times slower. Plotting average pressure against diffusivity times time divided by thickness squared collapses the two responses onto the same curve. In an experiment, a systematic size series can therefore help identify a transport contribution. Geometry-dependent relaxation and relaxation governed mainly by local network rearrangement suggest different follow-up measurements, even when both initially produce a declining force.

$$
\bar p(t)=\frac{1}{H}\int_0^H p(z,t)\,dz,\qquad F(t)=A_0\left[\sigma_s+\bar p(t)\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/541ba1aae0dc9ef838f71ad2.svg) | Spatially averaged excess pressure, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/6d6950da29507eb4f6b78d53.svg) | Layer thickness, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/9032cb23a878659e74b670d3.svg) | Position, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/48c7b594e8628a17b991d4e6.svg) | Local excess pressure, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | Total compressive force, N. |
| ![Formula](https://ml-biomat.com/static/agent-math/0c430ee48d22be2e69d0f3ad.svg) | Fixed load-bearing area, mm²; apply a factor 0.001 when using kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb8516549f964d260f28c111.svg) | Prescribed constant solid stress in the teaching model, 5 kPa. |

For area 28.274 mm² and initial mean pressure 10 kPa, F=0.424115 N; after pressure decay F=0.141372 N. Solid stress and pressure initial state are separately prescribed to demonstrate load sharing.

To connect pressure with load, the teaching model separately prescribes a constant solid contribution of 5 kPa. Adding the mean excess pressure and multiplying by the 28.274 mm² area gives an initial total force of about 0.424 N and a long-time force of about 0.141 N. The solid term and pressure initial condition are specified so that the load-sharing arithmetic is transparent. A full cartilage biphasic solution also couples solid deformation, fluid motion and mechanical boundaries. Drainage direction deserves particular attention: this example drains through top and bottom faces. A free cylinder between impermeable platens commonly drains mainly through its side, making the radial path relevant. Substituting specimen height into the present formula would describe the wrong geometry.

![Specified one-dimensional two-face drainage model: spatial profiles, thickness effect, dimensionless collapse and load sharing between fixed solid stress and pressure. Points are noisy constructed force observations.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/be177865b77232397cf54363.svg?v=be177865b772)

Figure 4Specified one-dimensional two-face drainage model: spatial profiles, thickness effect, dimensionless collapse and load sharing between fixed solid stress and pressure. Points are noisy constructed force observations.

## Match the experimental conditions to the material question

For a hydrogel or tissue, hydration is part of the mechanical state. Evaporation after removal from a bath changes dimensions and polymer concentration. A bath with a different salt concentration can alter swelling. Establish a reproducible condition in the selected medium and temperature, then record the timing of equilibration, handling and testing. Testing in liquid reduces evaporation but introduces other contributions: buoyancy, meniscus forces, temperature drift and the changing immersion of fixtures. Obtain the unloaded baseline in the same immersion configuration. A zero measured in air is not automatically suitable for interpreting millinewton-level changes after the fixture enters a bath.

Select the load cell using the expected specimen force. A large-capacity cell suitable for hard plastics may resolve the initial contact of a soft gel poorly. Estimate load from specimen area and an anticipated stress range, then choose adequate resolution, capacity and stopping conditions. Sampling must capture the fastest part of the experiment. If initial contact occupies only a few saved frames, a sophisticated fit cannot reconstruct all the information that was never recorded. Conversely, thousands of closely spaced points during a slow hold are strongly related in time. They improve description of that trace but do not count as thousands of independent specimens when comparing formulations.

Preloading and conditioning cycles change the reference state. A small preload can establish reproducible contact, yet adopting the height after preload as the original height defines a new strain reference. State that choice explicitly. Some networks soften after their first large deformation, and foams may retain a collapsed structure. In such cases the difference between the first and second cycles is material information. Show initial loading, subsequent cycles and the recovery interval separately rather than averaging them into one apparently smooth response. When a product is intended to be conditioned before use, its testing history should reproduce that state. When the first use matters, retaining the first cycle is essential.

Repeatability also has a hierarchy. Compressing one specimen three times investigates cycling and instrument repeatability, while three independently prepared specimens sample preparation variability. Multiple pieces from one tissue region may resemble each other more than samples from different individuals. Keep those levels visible in the data organisation and explain which units generate the plotted spread. Individual curves or parameter points often reveal more than a bar with an unexplained error bar. Balance batches and measurement order where possible, and record geometry for each specimen. A carefully arranged comparison can clarify a material difference more effectively than adding complexity to the fitted constitutive equation.

Observe the specimen while collecting numbers. A sudden force drop accompanied by a visible split has a different interpretation from a smooth fall during drainage. A sample sliding sideways, a platen touching the bath container or a bubble trapped at the interface can also alter the trace. Synchronised images need not be elaborate: an identifiable time correspondence and a calibrated field of view are often enough to connect a curve feature to an event. Preserve the original record when assigning those events. Removing a suspicious segment without retaining its timing makes it harder to decide later whether the event belonged to the material or the apparatus.

## Calculate contact, elasticity and drainage as distinct questions

The complete program contains two independent teaching records. The first generates force from a known contact position and neo-Hookean response, adds noise using a fixed random seed and jointly estimates contact, shear modulus and baseline. Its output retains stage closure, observed force, predicted force and residual. This makes it possible to inspect the analysis starting from the original measurement channels. The second generates a time series from the specified pressure model, adds the fixed solid contribution and estimates diffusivity from noisy total force. The two examples explain finite-deformation geometry and drainage timing separately; they are not presented as measurements of a particular tissue.

The pressure calculation expresses a spatial profile as components of different wavelengths. Short-wavelength components disappear quickly, while long-wavelength components persist. A first reading does not require a full series derivation. Check three accessible conditions instead: pressure remains zero at the drained faces, its spatial average declines with time, and doubling thickness delays a given degree of decay. At the initial instant, the code assigns the specified interior pressure directly. This avoids a small finite-series approximation error at the abrupt boundary change. The exported arrays retain positions, times and pressures, supporting a second plot or a direct check of values against the figure legend.

The executed example recovers the specified 20 kPa shear modulus as about 20.006 kPa and contact position as about 0.06013 mm. Its force residual has an RMS of about 1.99 mN, consistent with the added 2 mN noise scale. The drainage fit recovers approximately 0.009996 mm²/s from a specified 0.01 mm²/s. Known inputs make these comparisons possible in the constructed record. With experimental files, calibration, independent specimens and boundary checks provide the corresponding evidence. A small residual alone does not establish correct contact, and an expected-looking modulus does not replace inspection of specimen shape and the original force trace.

### Complete Python: contact inversion, compression geometry and drainage

Run two separate teaching models and retain records, fits, pressure fields and four bilingual figures.

```
"""Compression geometry, contact identification and a specified drainage model.
All numerical records are constructed teaching examples, not tissue measurements.
python main.py --output results --language en
"""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon

def nominal(e,mu=20.):
    lam=1-np.asarray(e)
    return mu*(lam**-2-lam)

def pressure_mean(t,H=2.,D=.01,p0=10.):
    t=np.asarray(t,dtype=float);n=np.arange(1,400,2,dtype=float)
    y=8*p0/np.pi**2*np.sum(np.exp(-np.outer(t.ravel(),n*n)*np.pi**2*D/H**2)/(n*n),axis=1)
    return np.where(t.ravel()==0,p0,y).reshape(t.shape)

def pressure_field(z,t,H=2.,D=.01,p0=10.):
    z=np.asarray(z);n=np.arange(1,400,2,dtype=float)
    if t==0:return np.where((z>0)&(z<H),p0,0.)
    return 4*p0/np.pi*np.sum(np.sin(np.outer(z,n)*np.pi/H)*np.exp(-n*n*np.pi**2*D*t/H**2)/n,axis=1)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();o=a.output;o.mkdir(parents=True,exist_ok=True);tr=lambda z,e:z if a.language=='zh' else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fbfcfc','savefig.facecolor':'#fbfcfc','text.color':'#18344a'})
    B='#186c94';G='#188777';O='#d27839';P='#8a5d92'
    def save(f,n):f.savefig(o/f'{n}-{a.language}.svg',bbox_inches='tight');f.savefig(o/f'{n}-{a.language}.png',bbox_inches='tight',dpi=150);plt.close(f)
    rng=np.random.default_rng(1902);R=3.;H=2.;A=np.pi*R*R;u=np.linspace(-.1,.8,241);contact=.06;baseline=.0015
    model=lambda v:nominal(np.maximum(u-v[1],0)/H,v[0])*A/1000+v[2]
    force=model([20,contact,baseline])+rng.normal(0,.002,len(u))
    fit=least_squares(lambda v:model(v)-force,[18,.04,0],bounds=([1,-.05,-.02],[100,.15,.02])).x;pred=model(fit)
    t=np.linspace(0,300,301);pmean=pressure_mean(t);F=(5+pmean)*A/1000;Fobs=F+rng.normal(0,.0005,len(t))
    Dfit=float(np.exp(least_squares(lambda q:((5+pressure_mean(t,D=np.exp(q[0])))*A/1000-Fobs),[np.log(.02)]).x[0]))
    summary={'fit_mu_kPa':float(fit[0]),'fit_contact_mm':float(fit[1]),'fit_baseline_N':float(fit[2]),'residual_rms_mN':float(np.sqrt(np.mean((pred-force)**2))*1000),'nominal_at_20pct_kPa':float(nominal(.2)),'true_at_20pct_kPa':float(.8*nominal(.2)),'force_at_20pct_N':float(nominal(.2)*A/1000),'free_modulus_kPa':60.,'confined_modulus_nu045_kPa':60*.55/(1.45*.1),'tau_H2_s':4/(np.pi**2*.01),'tau_H4_s':16/(np.pi**2*.01),'fit_diffusivity_mm2_s':Dfit,'initial_force_N':float(15*A/1000),'equilibrium_force_N':float(5*A/1000),'mean_pressure_40s_kPa':float(pressure_mean(40.))}
    (o/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');np.savetxt(o/'data.csv',np.c_[u,force,pred,force-pred],delimiter=',',header='stage_closure_mm,observed_force_N,fitted_force_N,residual_N',comments='');np.savetxt(o/'drainage.csv',np.c_[t,pmean,F,Fobs],delimiter=',',header='time_s,mean_excess_pressure_kPa,model_force_N,observed_force_N',comments='')
    z=np.linspace(0,H,201);times=np.array([0,2,10,40,100,300]);fields=np.array([pressure_field(z,tt) for tt in times]);np.savez(o/'pressure_fields.npz',z_mm=z,time_s=times,pressure_kPa=fields)
    f,ax=plt.subplots(2,2,figsize=(12,8));labels=[tr('a  自由侧向膨胀','a  Free lateral expansion'),tr('b  端面摩擦与鼓肚','b  End friction and barrelling'),tr('c  刚性侧壁约束','c  Rigid lateral confinement'),tr('d  1980：固体网络与流体共同承载','d  1980: solid network and fluid support')]
    for i,x in enumerate(ax.flat):
        x.set(xlim=(0,10),ylim=(0,7));x.axis('off');x.set_title(labels[i],loc='left',fontweight='bold',fontsize=12)
        if i<3:
            for yy in [1,5]:x.add_patch(Rectangle((1,yy),8,.45,facecolor='#8b9ca7'))
            if i==1:
                yy=np.linspace(1.45,5,80);left=3-.8*np.sin(np.pi*(yy-1.45)/3.55);right=7+.8*np.sin(np.pi*(yy-1.45)/3.55);x.fill(np.r_[left,right[::-1]],np.r_[yy,yy[::-1]],color=G,alpha=.28);x.plot(left,yy,color=G);x.plot(right,yy,color=G)
            else:x.add_patch(Rectangle((2.7 if i==0 else 3,1.45),4.6 if i==0 else 4,3.55,facecolor='#d0e9e4',edgecolor=G,lw=2))
            if i==2:
                for xx in [2.5,7]:x.add_patch(Rectangle((xx,1),.5,4.4,facecolor='#526b7a'))
            x.annotate('',(5,5.5),(5,6.6),arrowprops={'arrowstyle':'->','color':O,'lw':2})
            x.text(5,.3,[tr('侧面自由；端面滑动','Free sides; sliding ends'),tr('端部受阻；中部更宽','Restrained ends; wider middle'),tr('横向应变为零','Zero lateral strain')][i],ha='center')
        else:
            for xx in np.linspace(2,8,5):x.plot([xx,xx],[1.7,5.3],color=G,lw=2)
            for yy in np.linspace(1.7,5.3,4):x.plot([2,8],[yy,yy],color=G,lw=2)
            for xx in np.linspace(2.6,7.4,4):
                for yy in [2.3,3.5,4.7]:x.scatter(xx,yy,s=70,color=B,alpha=.55)
            x.annotate('',(8.9,3.5),(7.8,3.5),arrowprops={'arrowstyle':'->','color':B,'lw':2});x.text(5,.5,tr('Mow、Kuei、Lai、Armstrong：双相力学','Mow, Kuei, Lai, Armstrong: biphasic mechanics'),ha='center',fontsize=10)
    f.tight_layout();save(f,'geometry')
    f,ax=plt.subplots(2,2,figsize=(12,8));ax[0,0].scatter(u,force,s=9,color=B,alpha=.55,label=tr('构造观测','Constructed observations'));ax[0,0].plot(u,pred,color=O,label=tr('接触点与材料联合拟合','Joint contact/material fit'));ax[0,0].axvline(contact,color=G,ls='--');ax[0,0].set(xlabel=tr('平台闭合位移 / mm','Stage closure / mm'),ylabel=tr('力 / N','Force / N'),title=tr('a  先找到接触，再计算压缩','a  Find contact before compression'));ax[0,0].legend(fontsize=9)
    ax[0,1].scatter(u,(force-pred)*1000,s=9,color=B);ax[0,1].axhline(0,color='#82939c');ax[0,1].set(xlabel=tr('平台闭合位移 / mm','Stage closure / mm'),ylabel=tr('残差 / mN','Residual / mN'),title=tr('b  剩下的是怎样的误差','b  What remains after fitting'))
    e=np.linspace(0,.4,201);ax[1,0].plot(e*100,nominal(e),color=B,label='Neo-Hookean');ax[1,0].plot(e*100,60*e,color=G,ls='--',label=tr('初始切线 E₀=60 kPa','Initial tangent E₀=60 kPa'));ax[1,0].scatter([20],[15.25],color=O);ax[1,0].set(xlabel=tr('压缩工程应变 / %','Engineering compression / %'),ylabel=tr('名义压应力 / kPa','Nominal compression stress / kPa'),title=tr('c  弯曲曲线仍可完全弹性','c  A curved response can be elastic'));ax[1,0].legend(fontsize=9)
    ax[1,1].plot(e*100,nominal(e),label=tr('原始面积','Original area'),color=B);ax[1,1].plot(e*100,(1-e)*nominal(e),label=tr('当前面积','Current area'),color=O);ax[1,1].set(xlabel=tr('压缩工程应变 / %','Engineering compression / %'),ylabel=tr('压应力 / kPa','Compression stress / kPa'),title=tr('d  分母面积改变数值','d  Area definition changes the value'));ax[1,1].legend();f.tight_layout();save(f,'contact')
    f,ax=plt.subplots(1,2,figsize=(12,4.8));nu=np.linspace(0,.49,200);M=60*(1-nu)/((1+nu)*(1-2*nu));ax[0].plot(nu,M,color=P);ax[0].axhline(60,color=G,ls='--',label=tr('自由压缩 E=60 kPa','Free compression E=60 kPa'));ax[0].scatter([.45],[60*.55/(1.45*.1)],color=O);ax[0].set(xlabel=tr('泊松比 ν','Poisson ratio ν'),ylabel=tr('约束压缩模量 / kPa','Constrained modulus / kPa'),title=tr('a  同一材料，不同侧向约束','a  Same material, different constraint'));ax[0].legend()
    ax[1].plot(e*100,1/(1-e),color=B,label=tr('面积 / 原始面积','Area / original area'));ax[1].plot(e*100,1/np.sqrt(1-e),color=O,label=tr('半径 / 原始半径','Radius / original radius'));ax[1].set(xlabel=tr('压缩工程应变 / %','Engineering compression / %'),ylabel=tr('几何比值','Geometric ratio'),title=tr('b  不可压缩指体积守恒','b  Incompressible means constant volume'));ax[1].legend();f.tight_layout();save(f,'constraint')
    f,ax=plt.subplots(2,2,figsize=(12,8));colors=plt.cm.viridis(np.linspace(.05,.85,5))
    for tt,c in zip([2,10,40,100,300],colors):ax[0,0].plot(z,pressure_field(z,tt),color=c,label=f'{tt} s')
    ax[0,0].set(xlabel=tr('层内位置 / mm','Position in layer / mm'),ylabel=tr('超额压力 / kPa','Excess pressure / kPa'),title=tr('a  两端排液的压力分布','a  Pressure with two drained faces'));ax[0,0].legend(ncol=2,fontsize=9)
    for hh,c in [(2,B),(4,O)]:ax[0,1].plot(t,pressure_mean(t,H=hh),color=c,label=f'H={hh} mm')
    ax[0,1].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('平均超额压力 / kPa','Mean excess pressure / kPa'),title=tr('b  厚度翻倍，时间尺度乘四','b  Double thickness, four times the scale'));ax[0,1].legend()
    for hh,c,st in [(2,B,'-'),(4,O,'--')]:ax[1,0].plot(t*.01/hh**2,pressure_mean(t,H=hh)/10,color=c,ls=st,label=f'H={hh} mm')
    ax[1,0].set(xlim=(0,.5),xlabel='Dt / H²',ylabel=tr('平均压力 / 初始压力','Mean / initial pressure'),title=tr('c  用排液长度归一化','c  Scale time by drainage length'));ax[1,0].legend()
    ax[1,1].fill_between(t,0,np.full_like(t,5*A/1000),color=G,alpha=.35,label=tr('指定固体部分','Specified solid contribution'));ax[1,1].fill_between(t,5*A/1000,F,color=B,alpha=.3,label=tr('压力部分','Pressure contribution'));ax[1,1].plot(t,F,color=B);ax[1,1].scatter(t[::10],Fobs[::10],s=12,color=O,label=tr('构造观测','Constructed observations'));ax[1,1].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('合力 / N','Total force / N'),title=tr('d  一个明确规定的载荷分担模型','d  A specified load-sharing model'));ax[1,1].legend(fontsize=9);f.tight_layout();save(f,'drainage')
    print(json.dumps(summary))
if __name__=='__main__':main()
```

The interactive experiment changes thickness, diffusivity and observation time independently. Keep diffusivity fixed, double thickness from 2 to 4 mm and find when the same mean pressure is reached. Then restore thickness and change diffusivity. The coloured field displays the current pressure distribution, while the trace displays mean pressure through time and the numeric output gives total force. Initial pressure, area and solid contribution stay fixed. These comparisons therefore isolate drainage length and transport rate without quietly changing specimen area or elastic strength. The controls also make the square-law scaling visible through a direct experiment rather than requiring it to be accepted as a detached formula.

## Interactive: drainage path and time

Two drained faces; initial pressure 10 kPa, solid contribution 5 kPa, radius 3 mm. Change thickness and compare the time needed for the same pressure decay.

[Figure: Mean pressure through time and current spatial field](https://ml-biomat.com/tutorials/experimental-methods/m02/en/#M02-plot)

## Turn a compression curve into an interpretable material comparison

When two gels have different initial slopes, follow the measurement chain before assigning a molecular explanation. Check hydration, contact identification, individual geometry, end sliding and the selected fitting interval. If curves separate only at large strain, examine working stress, unloading recovery and side shape. If their forces decay differently during a hold, compare loading duration, drainage paths and specimen dimensions together. Each pattern then leads to a physical question and a useful additional observation. A single adjective such as harder conceals these distinctions, whereas a defined slope, a stress at a stated compression or a force after a stated hold gives the comparison a reproducible meaning.

Compression combines naturally with microscopy, swelling measurements and structural characterisation. Pores can close under load, fibres can create directional responses, and changes in swelling alter both network concentration and original dimensions. Mark the loading direction on a sampling sketch and connect before-and-after images to the same specimen. Mechanical parameters then remain connected to the structure that produced them. For a scaffold exposed to repeated daily loads, one compression test describes an initial response. Cycling, fatigue and recovery experiments extend the question to how that response evolves. The transition is motivated by the intended use rather than by an arbitrary list of available machine functions.

A complete result allows a reader to reconstruct the scene: specimen shape, reference height and area, platen contact, freedom of lateral movement, drainage routes, loading duration and hold duration. It also identifies the extracted quantity, whether an initial tangent, a secant at a specified strain, a working stress or an equilibrium response. Place these definitions next to the curves and numerical values. Load bearing in a soft material emerges from material structure, geometry, boundaries and time acting together. Compression testing becomes especially informative when those factors are made observable and adjustable, so that a change in a curve leads to a specific mechanical explanation and a well-chosen next experiment.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/M02.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Mow et al. — Biphasic creep and stress relaxation (1980)](https://pubmed.ncbi.nlm.nih.gov/7382457/)

   Verify authors, title and date of the 1980 biphasic cartilage compression study.
2. [CellScale — Compression testing methods for soft materials and biomaterials](https://cellscale.com/applications/testing-methods/compression/)

   Examples of cylinder, sphere and indentation geometries with low-force measurement.

   Copyright CellScale; technical reading only, no data or figures reused.
3. [DoITPoMS — Compression, friction and barrelling](https://eng.libretexts.org/Bookshelves/Materials_Science/TLP_Library_II/5:_Mechanical_Testing_of_Metals/5.7:_Compression_Testing_-_Practical_Basics_Friction_and_Barrelling)

   End friction, barrelling and the uniform-stress assumption.

   CC BY-NC-SA reference consulted; no figures or text adapted.
4. [Lakes — Meaning of Poisson ratio](https://lakeslab.ep.wisc.edu/PoissonIntro2.html)

   Relation between free and fully constrained compression moduli.

   University teaching reference; original derivation and diagrams here.
5. [Sandia LAMÉ manual — Neo-Hookean model](https://www.sandia.gov/files/sierra/SM_LAME_5_24/main/models/neo_hookean.html)

   Finite-deformation elasticity, uniaxial stress and the small-strain limit.

   Official technical reference; no figures reused.
