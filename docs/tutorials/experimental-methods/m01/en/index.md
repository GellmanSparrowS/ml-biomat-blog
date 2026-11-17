# Tensile testing: Reading a material through its stress–strain curve

Source: https://ml-biomat.com/tutorials/experimental-methods/m01/en/
Language: en

Start from force and gauge length, distinguish modulus, yield, strength and work, and trace geometry and fixture effects into the result.

## Carrying a large force and resisting extension are different properties

A suture must maintain a connection under tension, packaging film must withstand handling, and a wearable sensor should follow the deformation of skin. Asking whether each material is strong combines several questions: how much force is needed initially, when does persistent deformation develop, what is the largest load, and how far can the material extend before separation? A tensile test puts these questions into a controlled sequence. The specimen is gripped at both ends and stretched while force and extension are recorded. Specimen dimensions then convert those observations into a stress–strain curve. Different parts of the curve carry different information, which makes a complete trace more useful than a single strength value.

Compare two straight strips made from the same material. A thicker strip requires more force for the same relative extension because more cross-sectional area carries load. A longer strip gains more absolute length at the same relative extension because more length participates. Comparing force and millimetres directly therefore mixes geometry with material response. Engineering stress divides force by original cross-sectional area; engineering strain divides the increase in gauge length by original gauge length. This normalisation supports comparisons under defined specimen and loading conditions while retaining the effects of direction, temperature, rate and structure. Direction is especially important for fibres, printed parts and biological tissues.

An elastic band and a slender glass strip provide a useful contrast. The band can stretch far with relatively little initial resistance. The glass strip resists small extension strongly but may break after little elongation. Stiffness, strength and extensibility describe different features. The area under a tensile curve adds the work absorbed along a specified loading path. Biomaterial design often needs these quantities together: compliance can help match tissue deformation, while sufficient load capacity and resistance to failure support connection, containment or structural support.

## From Hooke's spring to two marks on a specimen

In his 1678 discussion of elasticity, Hooke described the proportional response of springs through experiments that added load and observed extension. His interest in springs and timekeeping connected the mechanical relationship to practical devices. The original historical diagram uses single and doubled loads to illustrate that experimental idea. A modern tensile machine still asks how applied force relates to deformation. Improvements concern measurement precision, loading control and interpretation of specimen geometry. A spring's force–extension slope is structural stiffness, while a stress–strain slope removes specified geometric factors to obtain a modulus. Length and area connect the two descriptions.

![Original historical and measurement diagrams: Hooke’s load–extension idea, a dogbone gauge and specimen/machine displacement in series. Conceptual geometry, not a standard specimen drawing.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/18391f9ed8da0bbc1a437bea.svg?v=18391f9ed8da)

Figure 1Original historical and measurement diagrams: Hooke’s load–extension idea, a dogbone gauge and specimen/machine displacement in series. Conceptual geometry, not a standard specimen drawing.

Match load-cell range to the specimen. If the specimen generates a small force while the sensor is designed for much larger loads, resolution in the low-load region may be inadequate exactly where initial modulus is estimated. Check calibration, zero and preload after choosing a suitable range. Zero drift shifts the stress axis, while fixture weight and mounting can influence the unloaded reading. For delicate specimens, gripping and preloading may themselves alter the sample. Treat that preparation as part of its mechanical history rather than assuming the history begins when the recording button is pressed. A useful record identifies the reference state from which extension and load are measured.

A dogbone specimen has wide ends for gripping and a narrower parallel section for observation. Smooth transitions reduce stress concentration at the shoulders. Gauge length is the original distance between two selected measuring positions in the parallel section. It can be shorter than the distance between grips and differs from overall specimen length. The two marks in the diagram represent optical extensometry: a camera tracks their separation to measure local extension. Contacting extensometers measure distance change at prescribed positions as well. The appropriate device depends on stiffness, dimensions, expected extension and the condition of the specimen surface.

Crosshead travel includes the response of the entire load train. The frame, load cell, grips and connections deform slightly, and the specimen can seat or slip at its grips. Thinking of these parts as springs in series explains why total displacement includes their summed contributions. For a short, stiff specimen, its own extension is small and machine deformation may represent a substantial fraction. Treating crosshead travel as gauge extension then makes the curve appear flatter. Local extensometry or a suitable system-compliance correction separates the material deformation from the additional displacement.

Soft hydrogels and biological tissues introduce different gripping challenges. Excessive pressure can damage the specimen at the jaw; insufficient pressure permits slip. Dehydration can change dimensions and response during testing. Select gripping, environment and preparation appropriate to the material, and record hydration and waiting conditions. Comparable specimens need consistent orientation and effective cross section. Edge notches, bubbles and cutting damage belong in the specimen record because they influence where load is transmitted. Geometry preparation directly determines what the area and length in the calculation actually describe.

## Converting newtons and millimetres into stress and strain

Consider a specimen with original gauge length 50 millimetres and cross-sectional area 10 square millimetres. At one instant the load is 100 newtons and the gauge has extended by 0.25 millimetres. Engineering stress is 10 newtons per square millimetre, equal to 10 megapascals. Engineering strain is 0.005, or 0.5 percent. Strain is dimensionless because its numerator and denominator use the same length unit. Percent and decimal notation describe the same ratio, but a slope calculation must handle them consistently: substituting 0.5 where 0.005 is required changes modulus by a factor of one hundred. Plotting percent improves readability, while the program stores strain as a dimensionless decimal.

$$
\sigma_e=\frac{F}{A_0},\qquad\varepsilon_e=\frac{L-L_0}{L_0}=\frac{\Delta L}{L_0}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/38ae99caed83962e3e4ccf80.svg) | Engineering stress, MPa=N/mm². |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | Axial tensile force, N. |
| ![Formula](https://ml-biomat.com/static/agent-math/0c430ee48d22be2e69d0f3ad.svg) | Original cross-sectional area, mm². |
| ![Formula](https://ml-biomat.com/static/agent-math/e68022f53a9d87c881d61c43.svg) | Engineering strain, dimensionless; multiply by 100 to display percent. |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Current gauge length, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/973a201db437d1c712202461.svg) | Original gauge length, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/6ca346d066653af4cd6f62fe.svg) | Gauge extension L−L0, mm. |

Normalise by original geometry. F=100 N, A0=10 mm², ΔL=0.25 mm and L0=50 mm give σe=10 MPa and εe=0.005=0.5%.

The word original fixes the reference geometry. Area and gauge length are measured before deformation. If a small preload straightens the specimen, identify the state at which reference length was established. Measure width and thickness in the effective gauge region, with particular care that a thickness probe does not compress a soft film. Calculating a fibre area from diameter squares that dimension, amplifying its measurement error. For an irregular tissue section, preserve the method used to define area. An incorrectly entered area scales the entire stress curve while leaving no obvious anomaly in the raw force signal.

$$
E=\frac{d\sigma_e}{d\varepsilon_e},\qquad k_s=\frac{EA_0}{L_0}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | Modulus in a linear small-strain interval, MPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/38ae99caed83962e3e4ccf80.svg) | Engineering stress, MPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/e68022f53a9d87c881d61c43.svg) | Engineering strain, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/778e841bd8e233461c668db9.svg) | Axial structural stiffness of uniform specimen, N/mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/0c430ee48d22be2e69d0f3ad.svg) | Original area, mm². |
| ![Formula](https://ml-biomat.com/static/agent-math/973a201db437d1c712202461.svg) | Original gauge length, mm. |

The derivative is a local slope; in a straight interval use stress increment divided by strain increment. E=2000 MPa, A0=10 mm² and L0=50 mm give ks=400 N/mm.

Within a linear small-strain interval, modulus is the increase in stress divided by the corresponding increase in strain. Here 10 megapascals divided by 0.005 gives 2000 megapascals, or 2 gigapascals. The specimen's structural stiffness is 400 newtons per millimetre: 0.25 millimetres of extension requires 100 newtons. Doubling length with material and area unchanged halves structural stiffness while preserving modulus. Doubling area doubles structural stiffness while again preserving modulus. Preserve both raw force–displacement and normalised stress–strain records: the first describes a particular specimen, while the second supports material comparisons with the conditions identified.

An initial trace need not be naturally straight. Straightening a bent specimen, seating grips, taking up slack in a fibre bundle and intrinsic material nonlinearity can all produce an initial curved region. Use observation and mechanism to distinguish these causes before choosing a fitting interval. For an intrinsically nonlinear response, a tangent slope at a stated strain or a secant modulus between two stated strains may be useful. Naming any short fitted segment as the unique Young modulus loses the definition needed for comparison. An explicit interval allows another reader to repeat the same calculation.

## How one specimen can produce two apparent moduli

The example specifies a known response so that analysis effects can be separated from material changes. Initial modulus is 2000 megapascals, giving 40 megapascals at 2 percent engineering strain. Stress then rises more slowly to 50.8 at 20 percent, followed by a declining segment ending at 40 percent strain. This piecewise teaching curve supports slope, peak and work calculations; it is not a measured response of a named commercial material. The program multiplies stress by the 10-square-millimetre area to obtain force, adds small force and local-strain noise, and separately creates crosshead travel containing system compliance. Each signal channel therefore has an explicit physical construction.

$$
\Delta L_x=\Delta L_s+C_mF,\qquad E_x=\frac{E}{1+EA_0C_m/L_0}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5c60cc7d4d1bf6d7386dcb6b.svg) | Crosshead displacement, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/2aef3aeea0e2f9ed660eb869.svg) | Specimen gauge extension, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/b4840a9faca02419281df787.svg) | Series-system compliance, mm/N. |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | Axial force, N. |
| ![Formula](https://ml-biomat.com/static/agent-math/af9e236724ae69e17d4a69bc.svg) | Apparent modulus from crosshead travel divided by gauge length, MPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | True linear modulus, MPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/0c430ee48d22be2e69d0f3ad.svg) | Original area, mm². |
| ![Formula](https://ml-biomat.com/static/agent-math/973a201db437d1c712202461.svg) | Original gauge, mm. |

Linear series model without slip. E=2000, A0=10, L0=50 and Cm=0.001 give denominator 1.4 and Ex=1428.571 MPa; the system adds 0.1 mm at 100 N.

System compliance is 0.001 millimetres per newton, so a 100-newton load adds 0.1 millimetres of machine extension. The specimen itself extends 0.25 millimetres, while the crosshead moves 0.35. Dividing both by the 50-millimetre gauge gives a crosshead-based strain of 0.007. Ten megapascals divided by that value gives only 1428.57 megapascals. Fitting the noisy observations from 0.1 to 0.8 percent imposed strain gives about 2002.02 using local extensometry and 1428.49 using crosshead travel. Both traces arise from the same specified material. Their difference comes from displacement definition and measurement noise.

![Constructed record: raw force/displacements, dimension normalisation, initial-region detail and fit-window scan. Local/crosshead differences come from prescribed compliance; the curve leaves its initial line at 2%.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d54b8bc2604c1eff7877970b.svg?v=d54b8bc2604c)

Figure 2Constructed record: raw force/displacements, dimension normalisation, initial-region detail and fit-window scan. Local/crosshead differences come from prescribed compliance; the curve leaves its initial line at 2%.

The fitting-window scan starts from the same lower strain and progressively extends its upper bound. Windows inside the initial straight region give slopes close to the specified modulus. Once the window passes the 2-percent transition, the flatter response enters the fit and reduces the slope. Window selection is consequently part of the measurement definition. It is not a display preference that can be adjusted solely to improve a goodness-of-fit statistic. Actual tests choose intervals appropriate to material and method, supported by residuals and deformation observations. Comparing materials fitted over different intervals can combine material differences with interval effects.

Synchronisation matters as well. A load cell and camera with different sampling rates or a time delay can pair force with the wrong extension during rapid changes, creating artificial curvature or loops. Retain timestamps and establish the acquisition system's synchronisation procedure. Resampling, when needed, should follow that information. Smoothing can reduce high-frequency noise, but excessive smoothing shifts peaks and obscures abrupt events. Keep processing choices for modulus, peak and failure detection traceable. The aim is to preserve variations relevant to the experiment rather than to make every curve equally smooth.

A useful practical check compares marker motion with grip motion. If markers move smoothly while the grip displacement suddenly jumps, inspect seating or slip. If both markers accelerate locally near a narrowing region, deformation may be localising in the specimen. An image sequence can therefore explain a signal feature that a force trace alone leaves ambiguous. Local measurement supplies both a more appropriate strain and a route to diagnosing unexpected events.

## Reading modulus, yielding, strength and work separately

Beyond initial stiffness, an experiment often asks when persistent deformation becomes appreciable. Some materials have distinct yielding features, while others turn smoothly away from the initial line. The offset construction supplies a conventional reading: draw a line parallel to the selected elastic slope, shift it horizontally by a specified strain and locate its intersection with the measured curve. A common offset is 0.2 percent, or 0.002 dimensionless strain. The adopted definition belongs with the material and test method. Here it illustrates a common construction rather than asserting a universal yield definition for every polymer or soft tissue.

$$
\sigma_{\mathrm{offset}}=E_{\mathrm{fit}}(\varepsilon_e-\varepsilon_0)+b
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e7f86396c182c082f1d21a5f.svg) | Stress on offset line, MPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/a4e517b14dbb473355e98a18.svg) | Slope fitted over the selected interval, MPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/e68022f53a9d87c881d61c43.svg) | Engineering strain, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | Specified offset, 0.002=0.2% here. |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Intercept of the original fitted line, MPa. |

Find intersection with the stress–strain curve. The specified noise-free model has Efit=2000 and b=0, giving 40.123711 MPa. Use an offset definition appropriate to the material method.

The specified curve gives a 0.2-percent offset intersection near 40.124 megapascals; the noisy curve gives about 40.097. This differs from the definition of the initial straight segment ending at 40 megapascals. Ultimate engineering stress is the highest point on the full curve, about 50.8 here, and differs again from the last stress before fracture. A specimen can continue extending after maximum load and separate at a lower engineering stress. When necking develops, deformation concentrates in a local region. The overall curve normalised by initial area remains an engineering record, while local stress and strain require additional geometric information.

![Specified teaching curve: 0.2% offset, true-stress conversion over a uniform constant-volume interval, and tensile work. Integration uses dimensionless strain; percent is a display choice.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/1b11957547db5bab025e87c0.svg?v=1b11957547db)

Figure 3Specified teaching curve: 0.2% offset, true-stress conversion over a uniform constant-volume interval, and tensile work. Integration uses dimensionless strain; percent is a display choice.

$$
\sigma_t=\sigma_e(1+\varepsilon_e),\qquad\varepsilon_t=\ln(1+\varepsilon_e)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/87de164e10556b3dda44460d.svg) | True stress on current area, MPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/38ae99caed83962e3e4ccf80.svg) | Engineering stress on original area, MPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/d66c56edde4f1d59f195d1ee.svg) | Logarithmic true strain for uniform axial extension, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/e68022f53a9d87c881d61c43.svg) | Engineering strain, dimensionless. |

Stress conversion requires uniform uniaxial deformation and approximately conserved volume. εe=0.2 and σe=50.8 MPa give σt=60.96 MPa and εt=0.182322. Necking requires local geometry.

During uniform uniaxial deformation with approximately conserved volume, extension reduces area and true stress exceeds engineering stress. At 20 percent engineering strain, length is 1.2 times its original value. If area falls to its original value divided by 1.2, an engineering stress of 50.8 megapascals corresponds to a true stress of 60.96. The logarithmic true strain is about 0.18232. After necking, different locations no longer extend equally, so the global length ratio cannot automatically provide neck area. The plot confines conversion to the specified uniform interval; later stages require local dimensions or full-field measurements.

$$
W_V=\int_0^{\varepsilon_f}\sigma_e\,d\varepsilon_e
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/104ddb2cc44384e56d1f9bb2.svg) | Tensile work per original volume, MJ/m³. |
| ![Formula](https://ml-biomat.com/static/agent-math/b8ebdb3fc88042909ea28a74.svg) | Endpoint engineering strain of this path, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/38ae99caed83962e3e4ccf80.svg) | Engineering stress, MPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/e68022f53a9d87c881d61c43.svg) | Engineering strain, dimensionless. |

Divide work F dL by original volume A0L0. For the specified endpoint 0.4, three trapezoidal contributions give 0.4+8.172+8.56=17.132 MJ/m³. Crack-growth energy uses a different, newly created area normalisation.

The work interpretation follows from a small extension step. If force changes little during that step, work is force times extension. Replace force with engineering stress times original area, and extension with original gauge length times the strain increment. Area times gauge length is the reference volume. Summing steps and dividing by that volume gives the stress–strain integral. Force and extension must describe the same loaded specimen region. Integrating force against crosshead travel additionally includes work stored or dissipated in the loading system. The resulting area cannot all be assigned to the specimen while ignoring the extra displacement that produced it.

Summing small trapezoids under the curve gives tensile work per original volume. With stress in megapascals and dimensionless strain, the numerical result is megajoules per cubic metre. The three specified linear segments contribute 0.4, 8.172 and 8.56, totalling 17.132. This quantity describes the work absorbed by the specimen along the chosen loading path. Resistance to crack growth uses a cracked specimen and a different area normalisation. Both concern failure, but their objects and denominators differ. Keeping those definitions distinct prevents the integral of an unnotched tensile curve from being treated as a fracture-toughness measurement.

Unloading adds information that monotonic loading does not supply directly. A line that curves upward may represent recoverable nonlinear elasticity, time-dependent deformation or persistent structural change. Observing recovery after load removal helps distinguish these possibilities. In a tissue, a low-load toe region can involve progressive alignment of a fibrous structure; in another specimen, a similar-looking region may be grip seating. Curve shape becomes more informative when accompanied by an experiment that tests the proposed mechanism.

## Making comparisons between specimens useful

Polymers and biological tissues often depend on loading rate. Slow loading gives chain segments, fluid and internal structures more time to adjust; rapid loading may outrun those processes. Temperature and water content also change their time scales. Equal crosshead speeds do not imply equal nominal strain rates when gauge lengths differ. Five millimetres per minute over a 50-millimetre gauge corresponds ideally to 0.1 engineering strain per minute; halving the gauge doubles that ratio. Specify whether the experiment controls crosshead speed, local strain rate or another program, and match environment and preparation across comparisons.

Orientation and microstructure influence the response. Loading along fibres engages them differently from loading across them, where matrix and interfaces may dominate. Printed parts add layer bonding, pores and toolpath orientation; tissues add fibre alignment and hierarchical organisation. Direction and preparation state therefore belong with a reported material modulus. Device performance can motivate testing in the service direction, while constitutive modelling may require several directions, rates or loading modes. One tensile experiment contributes a defined part of that description and can be complemented by compression, cycling and relaxation.

![Separate sensitivities to system compliance and entered area, plus seven independently constructed specimen moduli. Right: line is mean, band is mean ± sample SD, not a confidence interval.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/133713a5db4bf5e8ed706c30.svg?v=133713a5db4b)

Figure 4Separate sensitivities to system compliance and entered area, plus seven independently constructed specimen moduli. Right: line is mean, band is mean ± sample SD, not a confidence interval.

Fracture elongation also depends on how the gauge spans local deformation. Suppose a short neck contributes an additional 2 millimetres of extension while the surrounding region changes little. Averaged over a 20-millimetre gauge, that contribution is 10 percent strain; averaged over 50 millimetres, it is 4 percent. Both numbers can describe the same local extension. Compare ductility using consistent gauge, geometry and post-fracture measurement definitions. Full-field imaging shows localisation more directly, but selecting a region over which to average remains an analysis choice. Keep that region comparable across specimens instead of adjusting it to make their reported strains resemble each other.

The area-sensitivity panel shows that entering 11 square millimetres for an actual area of 10 multiplies every stress and modulus by 10/11. A modulus of 2000 becomes approximately 1818.18. Area error and system compliance have different origins but can both lower an apparent modulus. Repetition reveals random variation, whereas a shared incorrect area can shift every replicate together. Another panel shows seven independent constructed specimen moduli, with mean about 2013.82 and sample standard deviation about 75.74 megapascals. Its band is mean plus or minus one sample standard deviation, describing specimen scatter rather than a confidence interval for the mean.

Record failure location with the curve. Repeated failures at grips or shoulders suggest examining fixture or transition geometry. Failures inside the gauge motivate inspection of local defects and material structure. Post-test photographs, marker trajectories and dimensions connect an unusual trace to a specific event. For a sudden force drop, establish whether the specimen fractured, slipped or reached a stopping condition before assigning the result. These observations help turn a statistical outlier into an interpretable experimental occurrence.

Independent specimens also require a clear sampling unit. Multiple points on one curve are not multiple material samples. Several strips cut from one sheet can assess within-sheet variation, while separate manufacturing batches address batch variation. Match that hierarchy to the claim being tested. Retaining individual curves, dimensions and preparation identifiers permits averaging without losing the source of variation. The scientific comparison then concerns a defined population of specimens under a defined procedure.

## Interactive experiment: can measurement alone make a material look softer?

The model material always has modulus 2000 megapascals, true area 10 square millimetres and gauge length 50 millimetres. Change the entered area, system compliance and the choice between local extensometry and crosshead displacement. Start with correct area and local measurement: the slope remains 2000. Increase compliance next. The local curve stays unchanged while the crosshead-based curve flattens. Entering an area of 11 square millimetres lowers stress in both versions. Separating geometry normalisation from displacement origin makes each change independently checkable with the preceding equations.

## Interactive: material and measurement definition

The actual specimen stays at E=2000 MPa, A=10 mm² and L=50 mm.

[Figure: Initial stress–strain curve](https://ml-biomat.com/tutorials/experimental-methods/m01/en/#M01-plot)

To connect the experiment to design, specify an allowed extension first. In the same linear model, allowing a 50-millimetre gauge to extend by 0.1 millimetres corresponds to 0.2 percent strain, 4 megapascals and 40 newtons. If device operation stays within that small range, initial stiffness is useful. If motion stretches the material by 20 percent or more, the relevant portion of the full curve is needed instead. Marking the operating point on an experimental trace shows where a chosen parameter comes from and which additional deformation range, loading rate or repeated-use condition should be measured.

This exercise also distinguishes changing the specimen from changing the analysis. Doubling the real cross-sectional area doubles the force required for a given strain in the ideal model. Merely doubling the entered area changes the reported stress without changing the physical force. A designer modifies actual geometry; an analyst records that geometry accurately. Keeping these actions separate prevents an apparent improvement created by a denominator change from being mistaken for a material improvement. The original force trace and measured dimensions together provide the information needed to make that distinction.

The observation-point control sets actual material strain. The display reports force, local extension and crosshead travel at that state. At the default actual strain of 0.5 percent, a 100-newton load extends the specimen by 0.25 millimetres while compliance adds 0.1. A crosshead reading of 0.35 alone does not identify those two contributions. Set compliance to zero and the displacement definitions coincide. Restore entered area to the actual value and stress normalisation also recovers. These boundary cases offer simple checks on the calculation and show why preparation and sensor choice directly influence inferred parameters.

Keep the cursor at the same material strain while changing the entered area. Force remains constant because the underlying specimen has not changed, but the displayed stress changes because its denominator has. Keep area fixed while changing compliance, and the underlying force remains constant again while the crosshead-derived strain changes. This distinction between the physical state and the analysis settings is useful whenever a reported material property changes after editing a test-method configuration.

## Complete processing from raw channels to reproducible properties

The program exports imposed strain, measured force, local extension, crosshead travel and both strain definitions. It fits initial slopes, finds an offset intersection, locates peak engineering stress and integrates tensile work. True-stress conversion is output only for the specified uniform interval; later table entries remain missing because additional local information is required. The code scans fitting windows, evaluates area and compliance sensitivity and displays independent constructed specimen scatter. Every analysis has a corresponding plot so that numerical results remain connected to the assumptions and signals that produced them.

### Complete Python: tensile curves and measurement sensitivity

Retain force and two displacement channels, extract modulus, offset, peak and work, then examine windows and geometry.

```
"""Tensile-test analysis with constructed force and local-extension observations.
Run: python main.py --output results --language en
The piecewise engineering curve is a teaching specification, not measured data.
"""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon

def stress(strain,E=2000.):
    e=np.asarray(strain);ey=40/E;peak=40+60*(.2-ey)
    return np.where(e<=ey,E*e,np.where(e<=.2,40+60*(e-ey),peak-80*(e-.2)))

def apparent_modulus(area_entered=10.,compliance=.001,method='crosshead'):
    return 2000*10/area_entered/(1+400*compliance if method=='crosshead' else 1)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();o=a.output;o.mkdir(parents=True,exist_ok=True);tr=lambda z,e:z if a.language=='zh' else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fbfcfc','savefig.facecolor':'#fbfcfc','text.color':'#18344a'})
    blue='#186c94';green='#188777';orange='#d27839';purple='#8a5d92'
    def save(f,n):f.savefig(o/f'{n}-{a.language}.svg',bbox_inches='tight');f.savefig(o/f'{n}-{a.language}.png',bbox_inches='tight',dpi=150);plt.close(f)
    rng=np.random.default_rng(1901);eps=np.unique(np.r_[np.linspace(0,.03,301),np.linspace(.03,.4,371)]);sig=stress(eps);A=10.;L=50.;C=.001
    force=sig*A+rng.normal(0,.3,len(eps));local=eps+rng.normal(0,.00002,len(eps));cross=(L*eps+C*force)/L
    mask=(eps>=.001)&(eps<=.008);E,b=np.polyfit(local[mask],force[mask]/A,1);Ex,bx=np.polyfit(cross[mask],force[mask]/A,1)
    # Use monotonically ordered imposed strain to interpolate a noisy measured curve.
    fy=lambda x:np.interp(x,eps,force/A)-(E*(x-.002)+b)
    offset=brentq(fy,.02,.03);offset_sig=np.interp(offset,eps,force/A)
    offset_exact=brentq(lambda x:float(stress(x))-2000*(x-.002),.02,.03)
    energy=float(np.trapezoid(sig,eps));peak_idx=int(np.argmax(force));valid=eps<=.2
    true_sig=np.where(valid,sig*(1+eps),np.nan);true_eps=np.where(valid,np.log1p(eps),np.nan)
    ends=np.linspace(.002,.035,60);slopes=[np.polyfit(local[(eps>=.001)&(eps<=en)],force[(eps>=.001)&(eps<=en)]/A,1)[0] for en in ends]
    reps=2000+rng.normal(0,80,7)
    summary={'fit_local_modulus_MPa':float(E),'fit_crosshead_modulus_MPa':float(Ex),'analytic_crosshead_modulus_MPa':apparent_modulus(),
      'offset_yield_MPa':float(offset_sig),'offset_strain':float(offset),'noiseless_offset_yield_MPa':float(stress(offset_exact)),
      'specified_peak_MPa':50.8,'observed_peak_MPa':float(force[peak_idx]/A),'observed_peak_strain':float(eps[peak_idx]),
      'specified_work_MJ_m3':energy,'work_hand_integral_MJ_m3':17.132,'true_stress_at_20pct_MPa':60.96,'true_strain_at_20pct':float(np.log(1.2)),
      'area_11mm2_modulus_MPa':apparent_modulus(11,0,'local'),'replicate_mean_MPa':float(reps.mean()),'replicate_sd_MPa':float(reps.std(ddof=1)),'data_kind':'Constructed teaching observations and specified piecewise engineering response'}
    (o/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    np.savetxt(o/'data.csv',np.column_stack([eps,force,local*L,cross*L,force/A,local,cross,true_sig,true_eps]),delimiter=',',header='imposed_strain,force_N,local_extension_mm,crosshead_extension_mm,engineering_stress_MPa,local_strain,crosshead_strain,uniform_true_stress_MPa,uniform_true_strain',comments='')
    np.savetxt(o/'fit_windows.csv',np.column_stack([ends,slopes]),delimiter=',',header='upper_strain,fit_modulus_MPa',comments='')
    np.savetxt(o/'replicates.csv',reps,delimiter=',',header='constructed_modulus_MPa',comments='')
    fig,axs=plt.subplots(1,3,figsize=(14.5,5));
    for ax in axs:ax.set_xlim(0,10);ax.set_ylim(0,10);ax.axis('off')
    ax=axs[0];ax.plot([.8,9.2],[8.8,8.8],lw=4,color='#6b808d')
    for x,le,n in [(3,3,1),(7,5,2)]:
        yy=np.linspace(8.8,8.8-le,180);xx=x+.4*np.sin(np.linspace(0,12*np.pi,180));ax.plot(xx,yy,color=blue);ax.plot([x,x],[8.8-le,8.2-le],color=blue);ax.add_patch(Rectangle((x-.65,7.2-le),1.3,1,facecolor=orange));ax.text(x,6.6-le,f'{n}F',ha='center')
    ax.text(5,9.5,tr('Hooke，1678：负载与伸长','Hooke, 1678: load and extension'),ha='center',fontsize=10);ax.text(5,.3,tr('弹簧长度变化体现结构刚度','Extension reveals structural stiffness'),ha='center',fontsize=9)
    ax=axs[1];pts=[(2,1),(8,1),(8,2.5),(6.2,3.5),(6.2,6.5),(8,7.5),(8,9),(2,9),(2,7.5),(3.8,6.5),(3.8,3.5),(2,2.5)];ax.add_patch(Polygon(pts,facecolor='#cce2e8',edgecolor=blue,lw=2));ax.add_patch(Rectangle((1.5,.4),7,1.1,color='#8f9fa8'));ax.add_patch(Rectangle((1.5,8.5),7,1.1,color='#8f9fa8'))
    ax.scatter([5,5],[4,6],s=45,color=orange);ax.annotate('',xy=(7,6),xytext=(7,4),arrowprops={'arrowstyle':'<->'});ax.text(7.3,5,'L₀',va='center');ax.text(5,.1,tr('标距内直接跟踪材料伸长','Track local extension inside the gauge'),ha='center',fontsize=9)
    ax=axs[2];ax.add_patch(Rectangle((1.5,7),7,1.2,facecolor='#cce2e8',edgecolor=blue));ax.text(5,7.6,tr('试样','Specimen'),ha='center',va='center');ax.add_patch(Rectangle((1.5,3.4),7,1.2,facecolor='#f1d5be',edgecolor=orange));ax.text(5,4,tr('机架与夹具','Frame and grips'),ha='center',va='center');ax.plot([5,5],[4.6,7],color='#6b808d');ax.annotate('',xy=(5,1),xytext=(5,3.4),arrowprops={'arrowstyle':'->','lw':2});ax.text(5,9.4,tr('串联位移：各部分相加','Series displacement: contributions add'),ha='center',fontsize=10);ax.text(5,.3,tr('横梁移动量包含两者变形','Crosshead travel includes both'),ha='center',fontsize=9);save(fig,'geometry')
    fig,axs=plt.subplots(2,2,figsize=(12,9));aa,bb,cc,dd=axs.ravel();aa.plot(local*L,force,color=blue,label=tr('标距伸长','Gauge extension'));aa.plot(cross*L,force,color=orange,label=tr('横梁位移','Crosshead travel'));aa.set_xlabel(tr('位移 / mm','Displacement / mm'));aa.set_ylabel(tr('力 / N','Force / N'));aa.legend(fontsize=9);aa.set_title(tr('A  原始力与两种位移','A  Force and two displacement channels'),loc='left')
    bb.plot(local*100,force/A,color=blue);bb.scatter(eps[peak_idx]*100,force[peak_idx]/A,color=orange,zorder=3);bb.set_xlabel(tr('工程应变 / %','Engineering strain / %'));bb.set_ylabel(tr('工程应力 / MPa','Engineering stress / MPa'));bb.set_title(tr('B  从尺寸归一化到曲线','B  Normalise by specimen dimensions'),loc='left')
    small=eps<=.012;cc.scatter(local[small]*100,force[small]/A,s=8,color=blue,label=tr('标距','Gauge'));cc.plot(cross[small]*100,force[small]/A,color=orange,label=tr('横梁','Crosshead'));cc.plot(local[mask]*100,E*local[mask]+b,color=green,lw=2,label=tr('标距拟合','Gauge fit'));cc.set_xlabel(tr('应变 / %','Strain / %'));cc.set_ylabel(tr('工程应力 / MPa','Engineering stress / MPa'));cc.legend(fontsize=8);cc.set_title(tr('C  小应变处的柔度差异','C  Compliance matters at small strain'),loc='left')
    dd.plot(ends*100,slopes,color=blue);dd.axhline(2000,color=green,ls='--');dd.axvline(2,color=orange,ls=':');dd.set_xlabel(tr('拟合上限应变 / %','Upper fit strain / %'));dd.set_ylabel(tr('拟合斜率 / MPa','Fitted slope / MPa'));dd.set_title(tr('D  拟合窗口跨入非线性区','D  A fit window enters nonlinearity'),loc='left');fig.tight_layout();save(fig,'analysis')
    fig,axs=plt.subplots(1,3,figsize=(14.5,4.7));aa,bb,cc=axs
    aa.plot(eps*100,sig,color=blue);x=np.linspace(.002,.04,100);aa.plot(x*100,2000*(x-.002),color=orange,ls='--');aa.scatter(offset_exact*100,float(stress(offset_exact)),color=green,zorder=5);aa.set_xlim(0,4);aa.set_ylim(0,65);aa.set_xlabel(tr('工程应变 / %','Engineering strain / %'));aa.set_ylabel(tr('应力 / MPa','Stress / MPa'));aa.set_title(tr('A  0.2%偏移交点','A  Intersection at 0.2% offset'),loc='left')
    bb.plot(eps[valid]*100,sig[valid],color=blue,label=tr('工程应力','Engineering stress'));bb.plot(eps[valid]*100,true_sig[valid],color=orange,label=tr('真应力','True stress'));bb.set_xlabel(tr('工程应变 / %','Engineering strain / %'));bb.set_ylabel(tr('应力 / MPa','Stress / MPa'));bb.legend(fontsize=9);bb.set_title(tr('B  均匀、恒体积阶段','B  Uniform constant-volume interval'),loc='left')
    cc.fill_between(eps*100,0,sig,color='#cce2e8');cc.plot(eps*100,sig,color=blue);cc.text(.05,.85,'17.132 MJ/m³',transform=cc.transAxes);cc.set_xlabel(tr('工程应变 / %','Engineering strain / %'));cc.set_ylabel(tr('工程应力 / MPa','Engineering stress / MPa'));cc.set_title(tr('C  体积归一化的拉伸功','C  Tensile work per initial volume'),loc='left');fig.tight_layout();save(fig,'properties')
    fig,axs=plt.subplots(1,3,figsize=(14,4.8));cm=np.linspace(0,.003,100);axs[0].plot(cm,2000/(1+400*cm),color=orange);axs[0].axhline(2000,color=green,ls='--');axs[0].set_xlabel(tr('系统柔度 / mm/N','System compliance / mm/N'));axs[0].set_ylabel(tr('表观模量 / MPa','Apparent modulus / MPa'));axs[0].set_title(tr('A  横梁法中的系统柔度','A  Compliance in crosshead analysis'),loc='left');area=np.linspace(8,12,100);axs[1].plot(area,2000*10/area,color=blue);axs[1].axvline(10,color=green,ls='--');axs[1].set_xlabel(tr('输入面积 / mm²','Entered area / mm²'));axs[1].set_ylabel(tr('表观模量 / MPa','Apparent modulus / MPa'));axs[1].set_title(tr('B  几何分母影响全部应力','B  Area scales every stress value'),loc='left');axs[2].scatter(np.arange(1,8),reps,color=blue,s=35);axs[2].axhline(reps.mean(),color=green);axs[2].axhspan(reps.mean()-reps.std(ddof=1),reps.mean()+reps.std(ddof=1),color=green,alpha=.12);axs[2].set_xlabel(tr('构造试样编号','Constructed specimen number'));axs[2].set_ylabel(tr('模量 / MPa','Modulus / MPa'));axs[2].set_title(tr('C  独立试样：均值±样本标准差','C  Specimens: mean ± sample SD'),loc='left',fontsize=10);fig.tight_layout();save(fig,'sensitivity')
    print(json.dumps(summary))
if __name__=='__main__':main()
```

Inspect missing values and acquisition-state fields when processing an exported table. After an optical marker is lost, software may write a missing value, repeat the last frame or output zero. None of these automatically means that the specimen returned to zero strain. Identify invalid measurements from status information or images, retain their locations and then decide whether interpolation is justified. A fracture event can be genuinely discontinuous, so interpolating across it invents a load-bearing segment that did not occur. Connecting each processing action to a known acquisition event keeps the numerical curve consistent with the physical test.

For an actual record, first connect measured dimensions, time and signal channels, then choose intervals and result definitions appropriate to the material method. Preserving raw data allows recalculation when improved geometry or synchronisation information becomes available. A useful tensile result is a material description with direction, environment, rate and measurement definition: how did this specimen deform, carry load and fail? Such a record supports comparison and provides a starting point for studying compression, crack growth and long-term mechanical response.

The example contains independent arithmetic checks as well as fitted outputs. Machine compliance predicts the apparent slope analytically, the piecewise curve has an exact trapezoidal work integral, and the offset intersection can be solved on its specified linear segment. Comparing these with numerical output separates implementation errors from the deliberately added noise. Those checks also show which numerical differences should remain when noisy observations replace an ideal specification.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/M01.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Hooke — Potentia Restitutiva, or Spring (historical text)](https://doi.org/10.1190/1.9781560801931.ch3a)

   Original account of load and helical-spring extension.

   Historical text excerpt consulted through publisher index; no image reused.
2. [MacTutor — Robert Hooke](https://mathshistory.st-andrews.ac.uk/Biographies/Hooke/)

   1678 presentation and timekeeping context.

   Historical reference; no image reused.
3. [Instron — Tensile testing](https://www.instron.com/en/resources/test-types/tensile-test/)

   Gripping, extensometry, modulus and strength measurements.
4. [Instron — Extensometers](https://www.instron.com/en/products/testing-accessories/extensometers/)

   Gauge length, system compliance and contacting/noncontacting measurement.
5. [Instron — Offset yield strength](https://www.instron.com/en/resources/glossary/offset-yield-strength/)

   Offset, intersection and distinction from elastic limit.
6. [DoITPoMS — True and nominal stresses and strains](https://eng.libretexts.org/Bookshelves/Materials_Science/TLP_Library_II/5:_Mechanical_Testing_of_Metals/5.3:_True_and_Nominal_Stresses_and_Strains)

   Stress/strain definitions using different areas and lengths.

   CC BY-NC-SA source consulted; no text or figures adapted.
7. [DoITPoMS — Tensile testing, necking and failure](https://eng.libretexts.org/Bookshelves/Materials_Science/TLP_Library_II/5:_Mechanical_Testing_of_Metals/5.6:_Tensile_Testing_-_Necking_and_Failure)

   Uniform deformation, necking and local measurement.

   CC BY-NC-SA source consulted; no text or figures adapted.
8. [Lord and Morrell — Elastic modulus measurement (2010)](https://doi.org/10.1088/0026-1394/47/2/s05)

   Primary study abstract identifying strain, alignment, analysis and uncertainty considerations.

   Publisher abstract consulted; no figures reused.
