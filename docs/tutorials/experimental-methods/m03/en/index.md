# Fracture testing: Why a crack advances

Source: https://ml-biomat.com/tutorials/experimental-methods/m03/en/
Language: en

Follow a small cut into energy release, initiation, stable growth, compliance calibration and gel tearing.

## Why a small cut can change the fate of a whole object

An intact plastic film may be difficult to pull apart, yet a small cut at its edge makes it easy to tear. Dressings, hydrogel patches, flexible sensors and laminated composites face the same practical question: does a high breaking load in an intact specimen imply durability after scratching or damage? A tensile test describes the overall deformation and failure of a specimen. A fracture test focuses on an existing crack, asking when it starts to advance and what drives further growth. The two measurements complement each other because useful materials usually need both load-bearing capacity and some tolerance of defects introduced during manufacture, handling or service.

A crack redistributes load into a small region around its tip. Imagine pedestrians being diverted around a gap in a road: average traffic far away can remain unchanged while the routes beside the gap become crowded. In a material, stress is redistributed, and the local response may involve chain stretching, plastic deformation, cavities, fibre bridging or bond rupture. A sharper tip usually produces greater concentration, but a mathematical prediction of infinite stress at an ideal tip does not by itself tell us when the whole specimen will break. We also need to ask how much mechanical energy becomes available when the crack advances and how much energy that advance requires.

Griffith's 1921 paper connected crack extension with elastic energy and the creation of new surfaces. In 1953, Rivlin and Thomas developed a characteristic tearing-energy description for rubber, bringing the energetic approach into large-deformation polymers. The connection is useful because glass and rubber deform very differently, yet both invite an experiment organised around the energy required to advance a crack. Later tough-hydrogel studies highlighted network bridging and surrounding dissipation. The original diagrams below connect these questions without applying a small-strain glass calculation directly to a highly stretched gel. History here explains why several experimental geometries share a common physical question.

![Original historical and mechanistic diagrams: Griffith’s 1921 crack-energy approach, Rivlin–Thomas rubber tearing energy in 1953, and network bridging with surrounding dissipation. Conceptual diagrams, not historical data.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/c89ff309956913a6ea48c303.svg?v=c89ff3099569)

Figure 1Original historical and mechanistic diagrams: Griffith’s 1921 crack-energy approach, Rivlin–Thomas rubber tearing energy in 1953, and network bridging with surrounding dissipation. Conceptual diagrams, not historical data.

## Three different denominators give three different energy quantities

Mechanical work involves both force and displacement. Slowly opening a linear spring increases force from zero, and the triangular area under its force–displacement curve is stored elastic energy. Its unit is a joule; N·mm is also an energy unit, equal to one thousandth of a joule. Divide work by original specimen volume and the result is energy per volume, often J/m³. Divide the relevant energy change during crack advance by newly added crack-plane area and the result is J/m². Much confusion between tensile toughness, total fracture work and fracture energy begins by treating these different denominators as if they were interchangeable.

$$
G=-\frac{\partial\Pi}{\partial A_c}=-\frac{1}{B}\frac{\partial\Pi}{\partial a},\qquad G\geq G_c
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/86e66d54c5de5fb86d1da06d.svg) | Energy release rate, J/m². |
| ![Formula](https://ml-biomat.com/static/agent-math/51db0c676e18e6a142517806.svg) | System potential energy under the specified loading control, J, including stored energy and external work. |
| ![Formula](https://ml-biomat.com/static/agent-math/0e856b4c890d783d82136df7.svg) | Projected area of one crack plane, m². |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | Out-of-plane width of a straight crack front, m. |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Crack length for one advancing front, m. |
| ![Formula](https://ml-biomat.com/static/agent-math/cb6f84da03b8ec08dfd05485.svg) | Crack-growth resistance under the specified conditions, J/m². |

Quasistatic energetic criterion; projected crack area is paired with resistance accounting for two newly created faces. B=0.02 m, Δa=0.001 m and a potential-energy decrease of 0.006 J give G=300 J/m².

The word rate in energy release rate means change with crack area, not energy released per second. The quantity G measures mechanical energy available for a small increment of crack-plane area. Area is counted as the projected area of one crack plane. The two free faces created by separation are already accounted for in the corresponding resistance definition; adding an extra factor of two changes the convention. For a crack front 20 mm wide advancing 1 mm, the added plane area is 20 mm². If available energy falls by 0.006 J, G is 300 J/m². This normalisation puts energy changes from different specimen sizes onto a comparable area scale.

The resistance to extension is described by a critical value or a resistance curve. In ideal brittle separation, creating new surfaces is central. In a toughened polymer, surrounding processes can also consume energy through chain pull-out, reversible-bond opening, particle cavitation or fibre bridging. A macroscopic resistance therefore often combines several mechanisms. Observing the zone around the tip can be as informative as following the crack itself. Temperature, speed, hydration and loading history alter which processes participate. Those conditions belong to the meaning of the reported value. Assigning all measured energy to backbone-bond rupture would overlook the other mechanisms that a toughening strategy may deliberately introduce.

Available energy also depends on external control. Under a maintained load, crack growth makes the structure more compliant, the load point moves and the loading system continues to do work. With opening held fixed during the increment, external work is zero and stored energy is released instead. Potential energy combines elastic storage and external work in a single calculation. The two controls can give the same G at one instant while producing opposite trends after the crack advances farther. Consequently, reaching an initiation condition and immediately breaking all the way across are separate questions. The interactive experiment makes this distinction visible by comparing both controls at the same initial state.

## Put crack length, force and opening in the same drawing

Begin with a double-cantilever-beam specimen. Two slender arms are joined along an interface, a crack separates them at one end, and opposite forces open the arms like a partly glued book. Crack length is measured from the load line to the tip. Each arm experiences a force of magnitude P, and the relative motion between its loading point and the other arm's loading point is the opening displacement. P is not the sum of the magnitudes of the two opposite forces. Force and displacement form a matched pair. Doubling force while retaining the same total opening changes the definitions used to calculate compliance and energy.

![Matched definitions for an ideal DCB: P is each-arm load, δ is relative opening between load points and a runs from load line to tip. Right shading is stored elastic energy at fixed crack length.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/dffbf7221565c5c2e57e61e7.svg?v=dffbf7221565)

Figure 2Matched definitions for an ideal DCB: P is each-arm load, δ is relative opening between load points and a runs from load line to tip. Right shading is stored elastic energy at fixed crack length.

This geometry is particularly useful for interfacial or interlaminar opening, but not every material can be tested in that form. Compact-tension or notched-bend specimens suit many stiff solids, while notched strips and tear geometries suit thin rubbers and gels. Choose a geometry that directs the crack through the region of interest, permits observation and supports an appropriate analysis. NASA's account of testing a complex ablative material describes a crack wandering away from the specimen mid-plane. That example illustrates a practical point: a fixture that works well for one composite architecture may require reconsideration when the material structure changes. Observe the path rather than assuming it from the drawing.

A notch is also different from a sharp crack. A saw cut or moulded notch has a finite root radius and therefore a different local stress concentration. Depending on the material, experiments use a blade, fatigue precracking or controlled initial extension to prepare a suitable tip. Record that initial state. A blade can compress or damage a gel near the cut, while the end of a release film in a laminate can create a resin-rich region unlike a naturally propagated tip. Keep preparation consistent when comparing materials and distinguish initiation resistance from resistance after appreciable growth. This separates an initial preparation effect from the subsequent propagation behaviour.

Crack length commonly comes from images. Calibrate pixels in the specimen plane, identify the load line and tip, and synchronise image time with force and displacement. A crack visible on one surface may not describe the entire front through the specimen width. The front can curve or advance internally before reaching an observed surface. Compare both sides when useful and combine images with suitable fracture-surface marks or internal observations. If a crack jumps between widely spaced frames, several growth events can appear as one. Choose imaging frequency from the expected motion, because a precise force record cannot compensate for an unobserved crack position at the same instant.

## A longer crack makes a softer structure: measuring energy through compliance

Compliance is displacement divided by force: it measures how easily a structure opens. For double-cantilever arms with fixed material and thickness, a longer crack leaves a longer freely bending segment, so the same load produces more opening. At several known crack lengths, low loads that do not advance the crack can establish an opening–force slope. This gives compliance as a function of crack length. Its derivative then connects measured force to energy release rate. The derivative has a concrete purpose: it asks how much more compliant the specimen becomes when the crack moves a little farther. It is a description of a measurable structural change rather than an additional abstract material constant.

$$
C(a)=\frac{\delta}{P},\qquad G=\frac{P^2}{2B}\frac{dC}{da}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | Specimen opening compliance, mm/N. |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Crack length, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/e5b7c4267da3b3fe02d6ae1a.svg) | Relative opening between load points, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | Magnitude of load on each side, N. |
| ![Formula](https://ml-biomat.com/static/agent-math/86e66d54c5de5fb86d1da06d.svg) | Energy release rate, N/mm; multiply by 1000 for J/m². |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | Crack-front width, mm. |

Linear elasticity with consistent loading geometry and crack path; the derivative measures the increase in compliance with crack length. P=78.881 N, B=20 mm and dC/da=0.00192857 N⁻¹ give G=0.3 N/mm.

For ideal slender, linear elastic arms at small deflection, bending theory makes compliance proportional to the cube of crack length. Arm thickness also enters cubically, in the denominator, which makes its measurement particularly consequential. Consider modulus 70 GPa, width 20 mm, thickness 2 mm for each arm and crack length 30 mm. Compliance is about 0.01929 mm/N. If the prescribed interfacial resistance is 300 J/m², initiation occurs at approximately 78.88 N and a relative opening of 1.521 mm. Each arm moves only half that opening, much less than its 30 mm free length. This geometric comparison helps assess the small-deflection approximation used in the calculation.

$$
C=\frac{8a^3}{EBh^3},\qquad G=\frac{12P^2a^2}{EB^2h^3}=\frac{3P\delta}{2Ba}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | Ideal DCB compliance, mm/N. |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Distance from load line to crack tip, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | Young modulus of arm material, N/mm²=MPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | Out-of-plane width, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | Thickness of each arm, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/86e66d54c5de5fb86d1da06d.svg) | Energy release rate, N/mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | Load magnitude on each arm, N. |
| ![Formula](https://ml-biomat.com/static/agent-math/e5b7c4267da3b3fe02d6ae1a.svg) | Relative opening of specimen load points, mm. |

Slender linear elastic arms, small deflection, without root rotation or shear contributions. E=70000, B=20, h=2 and a=30 give C=0.0192857 mm/N; G=0.3 N/mm gives P=78.881 N and δ=1.52128 mm.

Measured travel can include fixture and frame deformation. The constructed calibration adds a constant system compliance of 0.003 mm/N and a small amount of noise. Fitting a cubic crack-length term together with a constant separates those contributions. The derivative of a constant system compliance with respect to crack length is zero, so it does not directly enter a correctly calibrated compliance-derivative calculation of G. However, substituting total crosshead travel for specimen opening in the ideal-beam shortcut overestimates energy release. The program plots both analyses. The effect is strongest near initiation, where specimen compliance is relatively small, and diminishes as the freely bending arms become longer.

Real specimens provide clear reasons to refine the ideal relation. The arm root can rotate instead of behaving as a perfect clamp, and short thick arms can develop appreciable shear deflection. Loading blocks, hinges and adhesive thickness may change the effective load position or local compliance. A suitable corrected beam relation, an independent compliance calibration or a numerical calibration can address those effects. Choose among them using specimen geometry and available measurements. If substantial plastic deformation creates different loading and unloading paths, the linear-spring energy relation itself must be replaced by an appropriate fracture analysis. Increasing the number of fit parameters in the same elastic formula does not make it describe that different process.

![Constructed calibration and propagation: compliance versus crack length, load versus opening, synchronised crack position and propagation G. Orange shows bias from uncorrected stage travel; green dashed is prescribed resistance 300 J/m².](https://ml-biomat.com/static/tutorials/experimental-methods/figures/c55d3f2a6e44a6ae66c8165c.svg?v=c55d3f2a6e44)

Figure 3Constructed calibration and propagation: compliance versus crack length, load versus opening, synchronised crack position and propagation G. Orange shows bias from uncorrected stage travel; green dashed is prescribed resistance 300 J/m².

## After initiation, does the crack stop or keep advancing?

Before initiation, the constructed beam record is approximately linear. Crack length remains 30 mm while increasing opening raises the force. Once the specified resistance is reached, the crack grows. Under gradually increasing opening, the longer free arms become more compliant, so the force required for continued propagation can decrease. A falling force after the peak therefore does not mean the test has finished. The synchronised crack trace shows that decreasing load and continuing crack extension occur together. Reporting only the peak load would discard the propagation stage and the resistance information obtained from it. This is one reason a fracture experiment needs a crack record as well as the machine's usual force and travel channels.

Now hold the initiation load constant. In the ideal beam model, G grows with the square of crack length, so a small advance creates a larger driving force. Constant resistance then favours continued growth. Hold the initiation opening constant instead, and load falls as the structure becomes more compliant. G decreases with the inverse fourth power of crack length, promoting arrest. The two driving-force curves intersect at initiation and diverge afterward. Stability therefore involves resistance, geometry and loading control together. Finite machine stiffness and controller response influence where a physical test lies between the two ideal controls. The same material can consequently show different crack-growth behaviour in different apparatus arrangements.

![Left: energy trends under fixed load and fixed opening from the same initiation state. Right: centre-crack half-length versus critical stress in a wide thin plate, using specified teaching properties.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/c4a9ad17ba6591f31899fadd.svg?v=c4a9ad17ba65)

Figure 4Left: energy trends under fixed load and fixed opening from the same initiation state. Right: centre-crack half-length versus critical stress in a wide thin plate, using specified teaching properties.

Resistance can itself increase with extension, producing an R-curve. Fibre bridging behind the tip or development of a surrounding dissipation zone can contribute to such a rise. Initiation resistance, resistance after a specified extension and a later plateau need not be equal. Associate each value with its position on the growth record. Labelling all of them simply fracture toughness makes otherwise reasonable measurements difficult to compare. Specimen size also matters when a bridging or process zone approaches a boundary. Check whether the available growth distance and dimensions allow the stage under discussion to develop. A short initiation test and a long propagation test can then be interpreted as complementary measurements.

$$
K_I=Y\sigma\sqrt{\pi a},\qquad G=\frac{K_I^2}{E^{\prime}},\qquad E^{\prime}=\begin{cases}E&\text{plane stress}\\ E/(1-\nu^2)&\text{plane strain}\end{cases}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cd6693efed951c5ba12757b7.svg) | Mode-I stress-intensity factor, Pa·√m. |
| ![Formula](https://ml-biomat.com/static/agent-math/ab4817775494786b06f0b9ce.svg) | Dimensionless factor appropriate to crack and specimen geometry. |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | Remote tensile stress, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Half-length of the centre crack in this example, m. |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | Pi. |
| ![Formula](https://ml-biomat.com/static/agent-math/86e66d54c5de5fb86d1da06d.svg) | Energy release rate, J/m². |
| ![Formula](https://ml-biomat.com/static/agent-math/aafc579e21c51bd7eea76db7.svg) | Effective elastic modulus for the plane condition, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | Young modulus, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/5064898bae7c73820eaab47c.svg) | Poisson ratio, dimensionless. |

Isotropic linear elasticity, mode I and a small near-tip nonlinear zone. A wide thin plate with Y=1, E=3 GPa, Gc=500 J/m² and a=1 mm has critical stress 21.851 MPa; a=4 mm gives 10.925 MPa.

For a material and geometry satisfying linear elastic fracture conditions, stress intensity provides another useful description. It combines remote stress, crack size and geometry into the amplitude of the near-tip field, commonly reported in MPa·√m. For a centre crack in a wide thin plate, take half-length 1 mm, Young's modulus 3 GPa and critical energy 500 J/m². The predicted critical remote stress is approximately 21.85 MPa. Increasing half-length to 4 mm lowers it to about 10.93 MPa. Four times the crack length halves the critical stress. Here a is the half-length, not total length, and the conversion uses plane stress. A thick-specimen plane-strain conversion changes the effective elastic modulus in the energy relation.

## How a soft hydrogel can be tested for fracture energy

A highly deformed gel can extend far beyond the small-strain field assumed by a simple linear elastic stress-intensity calculation. A wide, short pure-shear strip offers another route. Prepare unnotched and notched specimens from comparable material with the same initial grip separation. Use the notched specimen to identify the stretch at crack initiation, then calculate the energy density stored in the unnotched specimen at that stretch. In a sufficiently wide ideal strip, with the crack away from edge and grip effects, multiplying stored energy density by initial height gives energy release rate. The two specimens supply different pieces of the calculation: the critical deformation and the corresponding energy storage.

$$
W(\lambda_c)=\int_1^{\lambda_c}S(\lambda)\,d\lambda,\qquad G_c=H_0W(\lambda_c)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b6053f2ba2b57f6638d0be7f.svg) | Stored energy per original volume of the unnotched elastic strip, J/m³=Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | Current/original grip separation, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/c67cedfd9e1a287c0f930fba.svg) | Stretch at initiation in the corresponding notched strip, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | Nominal tensile stress based on original area, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/cb6f84da03b8ec08dfd05485.svg) | Initiation energy in the pure-shear geometry, J/m². |
| ![Formula](https://ml-biomat.com/static/agent-math/f510273c694c65128635cc0b.svg) | Initial grip separation, m. |

Sufficiently wide elastic pure-shear strip with tip away from grips and edges. The teaching neo-Hookean plane-strain strip with μ=10 kPa and λc=2 gives W=11250 J/m³; H0=0.01 m gives 112.5 J/m².

Why does height appear? Advancing the crack unloads a strip of material behind it. The released volume scales with initial grip separation, specimen thickness and crack advance. The newly added crack-plane area contains only thickness and advance. Their ratio leaves the height. The relation therefore follows from a particular unloading geometry; it is not a universal expression for every notched tensile specimen. Pure shear is the conventional name of this wide-strip test. Away from the tip, the material stretches in the loading direction, has approximately constrained deformation across its large width and contracts through its thickness. It should not be confused with simple shear produced by sliding parallel faces past one another.

The separate gel example uses a fully elastic incompressible neo-Hookean wide strip with shear modulus 10 kPa and initial height 10 mm. Crack initiation is prescribed at stretch two. Integrating the unnotched nominal-stress–stretch curve gives stored energy density 11.25 kPa, equivalent to 11250 J/m³. Multiplication by 0.01 m gives 112.5 J/m². Stretch is dimensionless, and nominal stress uses original cross-sectional area, making their integral work per original volume. Integrating against a percentage-strain axis without dividing by one hundred introduces a hundredfold error. The shaded area in the figure connects this arithmetic directly to the loading curve instead of presenting fracture energy as an unexplained fitted output.

Tough gels can raise resistance through several mechanisms. In their 2012 hydrogel study, Sun and colleagues associated covalent-network bridging with dissipation from unzipping an ionic network. This suggests concrete companion measurements: loading–unloading hysteresis, recovery time and subsequent loading can reveal whether dissipative mechanisms recover. In a strongly hysteretic material, loading work includes energy already dissipated and is not automatically all recoverable elastic storage. State the energy definition, loading history and analysis appropriate to that behaviour. The purely elastic teaching example keeps the integration and geometry transparent first. It provides a starting point for understanding why a dissipative network requires additional information rather than an invitation to ignore its history.

![Separate elastic gel-strip example: integration of the unnotched nominal-stress curve gives stored energy density; multiplying by initial height 10 mm gives 112.5 J/m² at prescribed critical stretch two.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/adae622fc34457827c8a5d95.svg?v=adae622fc344)

Figure 5Separate elastic gel-strip example: integration of the unnotched nominal-stress curve gives stored energy density; multiplying by initial height 10 mm gives 112.5 J/m² at prescribed critical stretch two.

## Connect original signals, crack images and calculation

The complete program first constructs a compliance calibration at nine crack lengths, fitting its cubic coefficient and constant system contribution. It then generates a stable crack path under increasing opening. Independent noise is added to force, opening and crack position with a fixed random seed, and those channels remain together in the exported table. Energy release rate uses the derivative of fitted compliance and is compared with the prescribed 300 J/m² propagation resistance. A second calculation deliberately substitutes crosshead travel for specimen opening, exposing the measurement-definition bias. These outputs make the analysis inspectable at several levels: original channels, calibrated geometry, inferred energy and a known constructed reference.

When processing experimental images, keep the tip criterion consistent. The shadow of an open crack, a whitening-zone boundary, changing surface texture and the location of lost connection may not coincide. Establish the criterion using several clear frames before applying it across the sequence. For an obscured interval, retain its timing and obtain a second view or a more suitable imaging method. Differentiating crack position to obtain velocity amplifies frame-to-frame localisation noise, so report the time window used. For the energy calculation here, correctly pairing force with crack length at the same instant is often more important than assigning many decimal places to every image coordinate.

The executed example gives a mean propagation estimate of about 297.22 J/m², close to the prescribed 300 J/m². Noise in the compliance calibration and measurement channels explains the difference. Using uncorrected stage travel at initiation instead gives approximately 346.67 J/m², illustrating a systematic effect larger than the visible random fluctuations. The gel integration returns about 112.4999 J/m², agreeing with the exact 112.5 J/m². These checks address different steps: the first exposes a displacement-definition bias, while the second checks numerical integration and units.

Simple scaling identifies influential measurements before a full uncertainty analysis. In the ideal-beam expression, G is proportional to load squared, so a uniform 1% load overestimate raises it by about 2.01%. A 1% crack-length overestimate has the same squared effect when other quantities are held fixed. Arm thickness appears cubed in the denominator; overestimating it by 1% lowers G by about 2.94%. These sensitivities guide measurement effort rather than prescribing that every percentage should be added. Errors can also be correlated when one image calibration supplies several dimensions.

Keep the area convention consistent when examining a rough or deflected fracture surface. Its microscopic area can exceed the projected crack-plane area used for G. A separate surface measurement can connect roughness to toughening, provided the relation between the two areas is stated. Changing the denominator silently would turn a structural comparison into a different quantity.

### Complete Python: compliance, crack growth and gel energy

Retain force, opening, crack position and energy calculations; compare control and system compliance.

```
"""Fracture analysis: elastic DCB compliance and a separate pure-shear gel model.
All records are constructed with specified mechanics and a fixed random seed.
python main.py --output results --language en
"""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon,Ellipse

E=70000.;B=20.;h=2.;a0=30.;Gc=.3
def compliance(a):return 8*np.asarray(a)**3/(E*B*h**3)
def release(P,a):return 12*np.asarray(P)**2*np.asarray(a)**2/(E*B**2*h**3)
def force_critical(a):return np.sqrt(Gc*E*B**2*h**3/(12*np.asarray(a)**2))
def gel_stress(lam,mu=10.):return mu*(np.asarray(lam,dtype=float)-np.asarray(lam,dtype=float)**-3)
def gel_energy(lam,mu=10.):return .5*mu*(np.asarray(lam,dtype=float)**2+np.asarray(lam,dtype=float)**-2-2)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--language',choices=['zh','en'],default='en');v=p.parse_args();o=v.output;o.mkdir(parents=True,exist_ok=True);tr=lambda z,e:z if v.language=='zh' else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fbfcfc','savefig.facecolor':'#fbfcfc','text.color':'#18344a'})
    blue='#186c94';green='#188777';orange='#d27839';purple='#8a5d92'
    def save(f,n):f.savefig(o/f'{n}-{v.language}.svg',bbox_inches='tight');f.savefig(o/f'{n}-{v.language}.png',bbox_inches='tight',dpi=150);plt.close(f)
    rng=np.random.default_rng(1903);acal=np.linspace(25,65,9);Csys=.003;Cobs=(compliance(acal)+Csys)*(1+rng.normal(0,.007,len(acal)));kfit,cfit=np.linalg.lstsq(np.c_[acal**3,np.ones_like(acal)],Cobs,rcond=None)[0]
    d0=float(force_critical(a0)*compliance(a0));delta=np.linspace(.05,8,400);crack=np.maximum(a0,(3*E*h**3*delta**2/(16*Gc))**.25);force=delta/compliance(crack);stage=delta+Csys*force
    Pobs=force+rng.normal(0,.15,len(force));dobs=delta+rng.normal(0,.003,len(delta));aobs=crack+rng.normal(0,.12,len(crack));Gobs=Pobs**2/(2*B)*3*kfit*aobs**2*1000;Gexact=release(force,crack)*1000
    post=delta>=d0;Gmean=float(np.mean(Gobs[post]));naive=3*force*stage/(2*B*crack)*1000
    lam=np.linspace(1,2.5,601);sig=gel_stress(lam);critical=lam<=2;Wnum=float(np.trapezoid(sig[critical],lam[critical]));Ggel=Wnum*10
    summary={'analytic_C30_mm_N':float(compliance(30)),'analytic_Pinit_N':float(force_critical(30)),'analytic_delta_init_mm':d0,'specified_Gc_J_m2':300.,'fitted_compliance_cubic_mm_m2N':float(kfit),'fitted_system_compliance_mm_N':float(cfit),'mean_propagation_G_J_m2':Gmean,'naive_G_at_initiation_J_m2':float(3*force_critical(a0)*(d0+Csys*force_critical(a0))/(2*B*a0)*1000),'gel_energy_density_at_lambda2_kPa':float(gel_energy(2)),'gel_G_exact_J_m2':112.5,'gel_G_numeric_J_m2':Ggel,'critical_stress_a1mm_MPa':float(np.sqrt(500*3e9/(np.pi*.001))/1e6),'critical_stress_a4mm_MPa':float(np.sqrt(500*3e9/(np.pi*.004))/1e6)}
    (o/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');np.savetxt(o/'data.csv',np.c_[delta,stage,Pobs,dobs,aobs,Gobs,Gexact,naive],delimiter=',',header='specimen_opening_mm,stage_travel_mm,observed_load_N,observed_opening_mm,observed_crack_mm,estimated_G_J_m2,exact_G_J_m2,uncorrected_stage_G_J_m2',comments='');np.savetxt(o/'compliance.csv',np.c_[acal,Cobs,compliance(acal)+Csys,kfit*acal**3+cfit],delimiter=',',header='crack_mm,observed_total_compliance_mm_N,true_total_compliance_mm_N,fitted_total_compliance_mm_N',comments='');np.savetxt(o/'gel.csv',np.c_[lam,sig,gel_energy(lam),gel_energy(lam)*10],delimiter=',',header='stretch,nominal_stress_kPa,stored_energy_kPa,pure_shear_G_J_m2',comments='')
    f,ax=plt.subplots(1,3,figsize=(13,4.7))
    for x in ax:x.set(xlim=(0,10),ylim=(0,9));x.axis('off')
    ax[0].add_patch(Rectangle((1,2),8,5,facecolor='#d6e8ef',edgecolor=blue,lw=2));ax[0].plot([3,7],[4.5,4.5],color='#233f51',lw=3)
    for xx in [2,5,8]:
        ax[0].annotate('',(xx,8),(xx,7),arrowprops={'arrowstyle':'->','color':orange});ax[0].annotate('',(xx,1),(xx,2),arrowprops={'arrowstyle':'->','color':orange})
    ax[0].text(5,.2,tr('1921  Griffith：裂纹与能量','1921  Griffith: cracks and energy'),ha='center',fontsize=10);ax[0].set_title(tr('a  小缺口改变破坏载荷','a  A flaw changes failure load'),fontsize=12)
    ax[1].add_patch(Rectangle((1,2),8,5,facecolor='#d0e9e2',edgecolor=green,lw=2));ax[1].add_patch(Polygon([(1,4),(5,4.5),(1,5)],facecolor='white'));ax[1].plot([1,5,1],[4,4.5,5],color='#233f51',lw=2);ax[1].text(5,.2,tr('1953  Rivlin–Thomas：撕裂能','1953  Rivlin–Thomas: tearing energy'),ha='center',fontsize=10);ax[1].set_title(tr('b  大变形橡胶也能算能量','b  Energy for large rubber deformation'),fontsize=11)
    for xx in np.linspace(1.5,8.5,6):
        yy=np.linspace(2,7,100);ax[2].plot(xx+.15*np.sin(yy*5),yy,color=green,lw=1.6)
    for yy in [3,4,5,6]:ax[2].plot([1.5,8.5],[yy,yy],color=blue,alpha=.6)
    ax[2].add_patch(Polygon([(1,4),(5,4.5),(1,5)],facecolor='#fbfcfc'));ax[2].plot([1,5,1],[4,4.5,5],color='#233f51',lw=2);ax[2].add_patch(Ellipse((5.7,4.5),3.2,4,facecolor=orange,alpha=.13,edgecolor=orange));ax[2].text(5,.2,tr('网络桥联与周围耗散','Network bridging and surrounding dissipation'),ha='center',fontsize=10);ax[2].set_title(tr('c  裂尖附近不只产生新表面','c  More than new surfaces at a tip'),fontsize=11);f.tight_layout();save(f,'history')
    f,ax=plt.subplots(1,2,figsize=(12,4.8));x=ax[0];x.set(xlim=(0,11),ylim=(-3.5,3.5));x.axis('off');s=np.linspace(0,7,120);bend=(7-s)**2*(14+s)/686
    x.fill_between(s,.15+bend,.7+bend,color=blue,alpha=.3);x.fill_between(s,-.15-bend,-.7-bend,color=blue,alpha=.3);x.add_patch(Rectangle((7,-.7),3,1.4,facecolor='#d0e9e2',edgecolor=green));x.plot([0,7],[.15,-.0],color='#657f8d',ls='--');x.plot([0,7],[-.15,0],color='#657f8d',ls='--')
    for sign in [-1,1]:
        x.annotate('',(0,sign*3),(0,sign*1.7),arrowprops={'arrowstyle':'->','color':orange});x.text(.2,sign*2.5,'P',color=orange)
    x.annotate('',(0,-2.5),(7,-2.5),arrowprops={'arrowstyle':'<->','color':'#18344a'});x.text(3.5,-2.9,'a',ha='center');x.annotate('',(.5,1.15),(.5,-1.15),arrowprops={'arrowstyle':'<->'});x.text(.8,0,'δ',va='center');x.text(8.5,1.4,tr('每臂厚 h；出平面宽 B','Arm thickness h; out-of-plane width B'),ha='center',fontsize=9);x.set_title(tr('a  双悬臂梁：P 是每一侧的力','a  DCB: P is the force on each arm'),fontsize=12)
    xx=np.linspace(0,d0,100);yy=xx/compliance(a0);ax[1].fill_between(xx,0,yy,color=blue,alpha=.2);ax[1].plot(xx,yy,color=blue);ax[1].text(.45,12,tr('储能 = 三角形面积','Stored energy = triangular area'));ax[1].set(xlabel=tr('相对开口 δ / mm','Relative opening δ / mm'),ylabel=tr('载荷 P / N','Load P / N'),title=tr('b  裂纹不增长时，梁像弹簧','b  Before growth, the beams act as a spring'));f.tight_layout();save(f,'geometry')
    f,ax=plt.subplots(2,2,figsize=(12,8));fine=np.linspace(25,65,150);ax[0,0].scatter(acal,Cobs,color=orange,label=tr('构造观测','Constructed observations'));ax[0,0].plot(fine,kfit*fine**3+cfit,color=blue,label=tr('立方项 + 系统柔度','Cubic term + system compliance'));ax[0,0].set(xlabel=tr('裂纹长度 a / mm','Crack length a / mm'),ylabel=tr('总柔度 / mm/N','Total compliance / mm/N'),title=tr('a  标定裂纹与柔度','a  Calibrate crack length and compliance'));ax[0,0].legend(fontsize=9)
    ax[0,1].plot(delta,Pobs,color=blue,lw=1,label=tr('构造力观测','Constructed force observations'));ax[0,1].axvline(d0,color=orange,ls='--',label=tr('起裂','Initiation'));ax[0,1].set(xlabel=tr('试样开口 / mm','Specimen opening / mm'),ylabel=tr('载荷 / N','Load / N'),title=tr('b  力下降时裂纹仍在增长','b  Crack growth accompanies falling load'));ax[0,1].legend(fontsize=9)
    ax[1,0].plot(delta,aobs,color=green,lw=1);ax[1,0].axvline(d0,color=orange,ls='--');ax[1,0].set(xlabel=tr('试样开口 / mm','Specimen opening / mm'),ylabel=tr('裂纹长度 / mm','Crack length / mm'),title=tr('c  与力同步的裂纹记录','c  Crack record synchronised with load'))
    ax[1,1].scatter(aobs[post]-a0,Gobs[post],s=8,color=blue,alpha=.45,label=tr('柔度导数法','Compliance derivative'));ax[1,1].plot(crack[post]-a0,naive[post],color=orange,label=tr('误用横梁位移','Uncorrected stage travel'));ax[1,1].axhline(300,color=green,ls='--',label=tr('规定阻力','Specified resistance'));ax[1,1].set(xlabel=tr('裂纹增量 / mm','Crack extension / mm'),ylabel='G / J m⁻²',title=tr('d  稳定扩展的能量分析','d  Energy during stable propagation'));ax[1,1].legend(fontsize=9);f.tight_layout();save(f,'analysis')
    f,ax=plt.subplots(1,2,figsize=(12,4.8));aa=np.linspace(20,75,250);Pc=force_critical(a0);Gload=release(Pc,aa)*1000;Gdisp=release(d0/compliance(aa),aa)*1000;ax[0].plot(aa,Gload,color=orange,label=tr('保持起裂载荷','Hold initiation load'));ax[0].plot(aa,Gdisp,color=blue,label=tr('保持起裂开口','Hold initiation opening'));ax[0].axhline(300,color=green,ls='--',label=tr('阻力300 J/m²','Resistance 300 J/m²'));ax[0].scatter([30],[300],color='#18344a');ax[0].set(xlim=(25,60),ylim=(0,1300),xlabel=tr('裂纹长度 / mm','Crack length / mm'),ylabel='G / J m⁻²',title=tr('a  加载控制决定增长趋势','a  Loading control changes the trend'));ax[0].legend(fontsize=9)
    flaw=np.linspace(.1,5,250);sc=np.sqrt(500*3e9/(np.pi*flaw/1000))/1e6;ax[1].plot(flaw,sc,color=purple);ax[1].scatter([1,4],np.sqrt(500*3e9/(np.pi*np.array([.001,.004])))/1e6,color=orange);ax[1].set(xlabel=tr('中心裂纹半长 a / mm','Centre-crack half-length a / mm'),ylabel=tr('临界远场应力 / MPa','Critical remote stress / MPa'),title=tr('b  E=3 GPa，Gc=500 J/m²，Y=1','b  E=3 GPa, Gc=500 J/m², Y=1'));f.tight_layout();save(f,'stability')
    f,ax=plt.subplots(1,2,figsize=(12,4.8));ax[0].plot(lam,sig,color=green);ax[0].fill_between(lam[critical],0,sig[critical],color=green,alpha=.25);ax[0].axvline(2,color=orange,ls='--');ax[0].set(xlabel=tr('伸长比 λ','Stretch λ'),ylabel=tr('名义拉应力 / kPa','Nominal tensile stress / kPa'),title=tr('a  无缺口纯剪切条带的储能','a  Stored energy in an unnotched strip'));ax[0].text(1.12,2,'W(2) = 11.25 kPa')
    ax[1].plot(lam,gel_energy(lam)*10,color=blue);ax[1].axhline(112.5,color=orange,ls='--');ax[1].scatter([2],[112.5],color=orange);ax[1].set(xlabel=tr('缺口试样临界伸长比 λc','Critical stretch of notched strip λc'),ylabel=tr('能量释放率 / J m⁻²','Energy release rate / J m⁻²'),title=tr('b  H₀=10 mm，G=H₀W','b  H₀=10 mm, G=H₀W'));f.tight_layout();save(f,'gel')
    print(json.dumps(summary))
if __name__=='__main__':main()
```

The interactive experiment holds beam material and dimensions fixed while changing crack length, loading control and the applied force or opening. Start at the initiation state for a 30 mm crack. Maintain its force and increase the assumed crack length to see the driving force rise. Then maintain the original opening and repeat the comparison. The graph displays G and prescribed resistance together, while numerical outputs give the matched force and opening. This is a comparison of equilibrium driving forces at selected crack positions, not an automatic simulation of a rapid fracture event. It allows each consequence of the control condition to be examined without hiding it inside a dynamic calculation.

## Interactive: one initiation state, two controls

Fixed E=70 GPa, B=20 mm, each-arm h=2 mm and resistance 300 J/m². Load and opening inputs apply to their selected control mode.

[Figure: Energy release rate versus crack length](https://ml-biomat.com/tutorials/experimental-methods/m03/en/#M03-plot)

## Use fracture results to answer a damage-tolerance question

First decide whether the intended process is bulk cracking, separation between two materials or peeling of an attached layer. All involve cracks, but paths and loading modes differ. Opening is mode I, in-plane sliding is mode II and opposite movement along the crack-front direction is mode III. A practical structure can combine them. Show specimen geometry, loading direction and the observed failure location together. This prevents interfacial separation, fracture inside an adhesive and substrate failure from being merged into one parameter. Microscopy of fracture surfaces or material left on the opposite face can provide the evidence needed to identify which path actually carried the crack.

Hydration, speed and sampling direction are particularly consequential for biomaterials. A crack travelling along fibres can behave differently from one cutting across them. Drying changes dimensions and molecular mobility, while waiting can allow reversible networks to recover. Match environment and history to the intended application and retain the propagation record, rather than only a photograph after separation. Distinguish scatter between independent specimens from the many points collected during growth in one specimen. The latter describe one resistance curve; they do not replace independently prepared samples or biological replicates. This distinction helps determine whether a proposed network or processing change produces a reproducible difference.

Finally, place strength, stiffness and resistance to crack extension in their separate roles. A stiff material can be brittle, and a highly extensible material can remain notch-sensitive. Raising the energy of one tear also motivates testing crack growth under repeated loading. An interpretable fracture result identifies the initial crack, force and displacement definitions, growth criterion, analysis geometry, energy or stress-intensity units, and whether resistance refers to initiation or propagation. These details let the number support an actual decision: shaping a dressing edge, comparing network-toughening mechanisms or assessing how a composite interface tolerates an existing defect. The next experiment can then follow the remaining practical question rather than merely producing another peak-load value.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/M03.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Griffith — The phenomena of rupture and flow in solids (1921)](https://doi.org/10.1098/rsta.1921.0006)

   Historical identity of the crack-energy paper.
2. [Rivlin and Thomas — Rupture of rubber I (1953)](https://imechanica.egr.uh.edu/sites/default/files/1953%20Rupture%20of%20rubber%20characteristic%20energy%20for%20tearing.pdf)

   Original first six pages on tearing energy, geometry and initiation criteria.

   Research reading; no figures or data reused.
3. [Bower — Energy methods in fracture mechanics](https://solidmechanics.org/Text/Chapter9_4/Chapter9_4.php)

   Potential energy, compliance derivative and G–K relation.

   Author textbook reference; original calculations and figures here.
4. [NASA — Mode-I fracture toughness with the nDCB test](https://www.nasa.gov/centers-and-facilities/nesc/mode-i-fracture-toughness-of-complex-materials-with-the-ndcb-test/)

   Crack-path and propagation-measurement choices for complex materials.

   Official technical account; no images reused.
5. [Macon — J-integral analysis of tapered double-cantilever beams](https://ntrs.nasa.gov/api/citations/20060026038/downloads/20060026038.pdf)

   Original discussion of beam compliance, root rotation, precracking and nonlinear analysis.

   NASA-hosted technical paper; no figures or data reused.
6. [Sun et al. — Highly stretchable and tough hydrogels (2012)](https://www.nature.com/articles/nature11409)

   Primary abstract on covalent-network bridging and ionic-network dissipation.

   Publisher abstract consulted; no figures or data reused.
