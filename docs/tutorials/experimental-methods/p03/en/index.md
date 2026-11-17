# Contact angle: How a drop meets a surface

Source: https://ml-biomat.com/tutorials/experimental-methods/p03/en/
Language: en

Read wetting from a droplet contour while separating interfacial equilibrium, contact-line history and image errors.

## Why does the same drop spread on one surface and bead on another?

Rain leaves different shapes on glass, waxed paper and leaves. Some drops spread rapidly, some remain rounded, and some look nearly spherical while adhering strongly to the surface. These differences matter when printing a continuous ink layer, coating a substrate, filling a microchannel or bringing a biomaterial into contact with water and protein-containing solutions. Contact-angle measurements turn this familiar observation into a defined geometrical quantity. At the location where liquid, solid and surrounding gas meet, the angle is measured through the liquid between the liquid-surface tangent and the solid surface.

The angle is not a label belonging to the solid alone. It results from a particular liquid, surface condition, surrounding environment and measurement process. Changing the liquid, cleaning procedure, storage time or deposition dynamics can change the observed shape. The broad question “What is this surface's contact angle?” therefore becomes more useful when it specifies the probe liquid, the prepared surface state, the time after contact and whether the contact line is resting or moving. Those details make two measurements physically comparable instead of merely giving them the same name.

This chapter begins with a small drop of known geometry, connects its angle to interfacial interactions and then examines how a contour becomes a numerical result. We will see that contour fitting can be highly repeatable while a small baseline error introduces a much larger systematic shift. Adding and withdrawing liquid will reveal why different angles can occur on the same surface. Roughness, trapped gas and absorption into biomaterials then extend the interpretation. A droplet image can consequently guide the next investigation of surface chemistry, texture or time-dependent liquid–material interactions.

Hydrophilic and hydrophobic are commonly used as initial descriptions for water contact angles below and above 90°, respectively. The identity of water matters: a surface that resists water spreading may be readily wetted by an oil. Results close to 90° should also be read together with their measurement variation rather than treating 89° and 91° as entirely opposite material classes. Angle is a continuous geometrical quantity, and practical behaviour often varies continuously as well. Category names help communication, but the original contour, specified liquid and experimental conditions retain the information needed for a useful interpretation.

## Young placed the question where three interfaces meet

In 1805, Thomas Young published an essay on the cohesion of fluids. The historical image reproduces a passage from page 66 in which he associated each solid–liquid combination with an appropriate contact angle. Long before high-speed cameras and automated contour fitting, drops, capillary tubes and curved interfaces provided a route toward a physical theory. This is a useful starting point because the central issue is not the sophistication of the camera. It is how the liquid surface, solid surface and solid–liquid interface together determine the geometry near the contact line.

Surface tension has two connected interpretations: force transmitted along an interface per unit length, and the free-energy cost of increasing interfacial area. Stretching an interface requires energy, and different interfaces have different costs. As a drop spreads, one type of area decreases while others increase. For a smooth, chemically homogeneous, rigid solid in ideal equilibrium, comparing these changes in the horizontal direction gives Young's relation. The arrows in the diagram represent interfacial contributions per unit contact-line length. The angle is read through the liquid, so the exterior supplementary angle is a different geometrical quantity.

$$
\gamma_{SV}-\gamma_{SL}=\gamma_{LV}\cos\theta_Y
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ded793ad5550dae1b42621e0.svg) | Solid–gas interfacial free energy, mJ/m², numerically equivalent to mN/m. |
| ![Formula](https://ml-biomat.com/static/agent-math/7b827ae0be883fb68e689fae.svg) | Solid–liquid interfacial free energy, mJ/m². |
| ![Formula](https://ml-biomat.com/static/agent-math/5f3d1c4c2559796bb2ba336f.svg) | Liquid–gas surface tension, mN/m. |
| ![Formula](https://ml-biomat.com/static/agent-math/d941e2f726e4aeecee316d62.svg) | Equilibrium angle on an ideal smooth, chemically homogeneous rigid surface, measured through liquid. |

Under the stated equilibrium conditions, interfacial contributions balance along the surface. A difference of 36 mN/m divided by 72 mN/m is 0.5, giving θY=60°. One angle constrains a difference between two solid-interface quantities.

If the difference between solid–gas and solid–liquid interfacial free energies is 36 mN/m and liquid–gas surface tension is 72 mN/m, the cosine is 0.5 and the ideal angle is 60°. The value 36 is a difference between two interfacial quantities, not the solid surface free energy by itself. One angle measured with one liquid supplies one relationship and does not independently determine every unknown within it. Several probe liquids with characterized properties can support further analysis under a chosen surface-energy model. The model's allocation of polar and dispersive contributions then becomes part of the definition of the reported result.

Two numerical combinations make this distinction concrete. Solid–gas and solid–liquid values of 50 and 14 have the same difference as values of 80 and 44: both give 36. With the same liquid, both combinations yield the same ideal angle. The angle alone has not distinguished them. Interfacial free energies are often written in mJ/m², numerically equivalent to mN/m because energy equals force multiplied by distance. Checking the units together with the number of unknown quantities helps identify which additional measurements or model assumptions a surface-energy analysis requires. This is a useful habit when comparing values produced by different software packages, since an identical input angle need not imply an identical set of inferred energy components.

![Left: Thomas Young, An Essay on the Cohesion of Fluids (1805), excerpt from p. 66; public-domain scan archived by Wikimedia Commons. The passage connects each solid–liquid combination with contact angle. Right: original interfacial-contribution diagram, with θ measured through liquid; arrow lengths do not represent force magnitudes.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/6385e9b39f619432e7dd8f5b.svg?v=6385e9b39f61)

Figure 1Left: Thomas Young, An Essay on the Cohesion of Fluids (1805), excerpt from p. 66; public-domain scan archived by Wikimedia Commons. The passage connects each solid–liquid combination with contact angle. Right: original interfacial-contribution diagram, with θ measured through liquid; arrow lengths do not represent force magnitudes.

The equilibrium picture also explains why a flatter drop should not automatically be described as more adhesive in every practical sense. A smaller angle indicates a greater tendency to establish contact area under the specified conditions, whereas motion requires the contact line to pass local obstacles. Rough features, chemically different patches and adsorbed layers can temporarily hold it in place. The visible contour may therefore occupy a range of observable states rather than instantly reaching one ideal equilibrium angle. Advancing and receding measurements bring this process dependence into the experiment.

## Locate the contact before asking software to fit the outline

The common sessile-drop method places a small amount of liquid on a specimen and images it from the side. Backlighting separates the contour from the background, while the specimen stage and camera are positioned to view the contact region appropriately. Before analysis, check that the surface is not visibly tilted, both contact points can be identified and the dispensing needle does not obscure the useful outline. Curved, transparent or reflective substrates can make the true contact location differ from the darkest apparent line. The analysis baseline represents the solid surface and should follow an interpretable geometrical location rather than being moved to obtain a preferred number.

Drop volume should match the specimen and research question. Small drops experience less gravitational deformation but are more sensitive to evaporation, local heterogeneity and finite image sampling. Larger drops cover more area while gravity can make their outlines depart from a spherical cap. A spherical cap is like a hat cut from a sphere and is a convenient model when gravity is weak and the drop is approximately axisymmetric. More appreciable gravitational distortion can be treated using a Young–Laplace shape model that includes curvature and hydrostatic effects. Select a model for the physical contributions present in the outline, not solely because it produces the smallest residual.

The Bond number compares gravitational and surface-tension effects by relating a gravitational pressure scale to the pressure associated with interface curvature. Smaller values support the use of a nearly spherical shape. Using the curvature radius as characteristic length, a liquid–gas density difference approximately 1000 kg/m³ and surface tension 72 mN/m gives about 0.0825 for the constructed drop. Gravity is a smaller contribution at this specified scale. This does not assign the same shape error to every 0.5 μL drop: liquid properties, angle and the chosen characteristic length remain part of the comparison. Converting the radius from millimetres to metres before inserting it into the formula keeps the SI units consistent.

$$
\mathrm{Bo}=\frac{\Delta\rho\,gR^2}{\gamma_{LV}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/76f8718fd930ba8aa9f1254c.svg) | Bond number, a dimensionless measure of gravity relative to surface tension. |
| ![Formula](https://ml-biomat.com/static/agent-math/988fbc7bbcda53116494bdef.svg) | Liquid–gas density difference, kg/m³; approximately 1000 here. |
| ![Formula](https://ml-biomat.com/static/agent-math/439e3cc8d431c550923e0870.svg) | Gravitational acceleration, m/s²; 9.81 here. |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | Curvature radius chosen as characteristic length here, metres; convert from mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/5f3d1c4c2559796bb2ba336f.svg) | Liquid–gas surface tension, N/m; 72 mN/m equals 0.072 N/m. |

R=0.000777992 m gives Bo≈0.08247. Dividing gravitational pressure scale ΔρgR by curvature pressure scale γ/R yields the ratio; specify the definition when using another characteristic length.

Surface cleaning requires an experimental definition. Solvent residues, handling, time since treatment and adsorbed airborne material can alter the outermost chemical environment. A polymer measured immediately after plasma treatment and one measured after several days answer questions about different surface ages. Likewise, water on a dry cell-culture material and a material immersed in culture medium represent different interfacial states. Specifying preparation and waiting time turns these differences into controllable experimental variables instead of allowing every discrepancy to be labelled random error afterward.

Preserve both time and position. A sequence after initial contact helps distinguish rapid spreading, slower absorption and evaporation. Drops at different locations characterize spatial heterogeneity; independently prepared specimens characterize preparation variability. Numerous frames of the same drop describe a process rather than numerous independent samples. Examine left and right contact angles separately before averaging them. Asymmetry may reflect stage tilt, directional texture, contamination or contact-line pinning, and can be more informative than an immediately reported mean.

Image calibration has a geometrical detail of its own. If horizontal and vertical pixels correspond to different physical lengths, a circle is stretched into an apparent ellipse, and an angle calculated directly from pixel coordinates becomes biased. Check the scale along both axes and convert coordinates to consistent lengths before fitting. At 5 μm per pixel, a 20 μm baseline shift is only four pixels. It may look inconspicuous in the full image while changing the estimated angle by more than a degree in this example. Accurate localization near the contact therefore contributes more than adding decimal places to a final displayed result.

## A spherical cap connects angle, volume and baseline position

Begin with a geometry that can be checked independently. Let a denote the radius of the circular contact base and h the height from the solid surface to the apex. For an ideal spherical cap, the contact angle equals twice the arctangent of h/a. Circle geometry gives a right-triangle relation for the half-angle, so the ratio is independent of magnification when both lengths use the same units. The quantity a refers to the radius where liquid meets the substrate, not necessarily the greatest horizontal radius anywhere in the drop. That distinction becomes especially important for a bulging drop with contact angle greater than 90°.

$$
\theta=2\arctan(h/a),\qquad V=\frac{\pi h}{6}(3a^2+h^2)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | Contact angle of an ideal spherical cap; inverse trigonometry returns radians, converted to degrees for display. |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | Height from baseline to apex, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Radius of the contact base, mm, not the maximum lateral radius of a bulging drop. |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | Spherical-cap volume, mm³, numerically equal to μL. |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | Pi; dimensionless. |

Circle half-angle geometry gives h/a and integration of the spherical cap gives volume. With a=0.731073 mm and h=0.511903 mm, θ=70° and V=0.5 μL. The model assumes an approximately axisymmetric cap with small gravity effects.

The constructed example has volume 0.5 μL and angle 70°. Because 1 μL equals 1 mm³, lengths and volume can be handled consistently in millimetres. Its curvature radius is approximately 0.7780 mm, contact-base radius 0.7311 mm and height 0.5119 mm. Substituting height and base radius recovers 70° and 0.5 μL. These numbers specify an analytical object rather than measured properties of a material. Independent coordinate perturbations with standard deviation 2 μm are then added to the outline, and a circle is fitted to all contour points to examine how observations depart from the known geometry.

The fitted circle centre and radius determine its intersection with the baseline and the tangent at that intersection. The default fit gives approximately 70.029°, close to the specified angle. Keeping that same fitted circle and raising only the analysis baseline by 20 μm reduces the estimated angle to approximately 68.454°. Neither liquid nor image acquisition has changed; only the assumed location of the solid surface has moved. Because the angle is defined at the contour–surface intersection, changing the baseline changes both the intersection and its tangent. Adding more contour points does not automatically repair this geometrical error.

$$
\theta_{\mathrm{fit}}=\arccos\left(\frac{b-y_c}{R}\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e9dd721598f9326794077013.svg) | Angle from the fitted circle and specified horizontal baseline, displayed in degrees. |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Vertical coordinate of analysis baseline, mm; true surface is zero. |
| ![Formula](https://ml-biomat.com/static/agent-math/024420a1f4a1300a242618c4.svg) | Vertical coordinate of fitted circle centre, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | Radius of the fitted circle, mm. |

A circle radius is perpendicular to its tangent, giving the cosine relation at intersection. The default fitted circle gives about 70.029° at b=0 and 68.454° at b=0.020 mm. The baseline must intersect the fitted circle.

The four-panel figure displays contour and baselines, radial fitting residuals, angle sensitivity to baseline position and 300 independent noise realizations at the same true geometry. The repeated fitted angles have a standard deviation approximately 0.039°, much smaller than the effect of a 20 μm baseline shift. A procedure can therefore be precise across repeats while retaining a shared systematic error. Real measurements additionally involve optics, contact-point localization, specimen heterogeneity and imperfect shape models. The small standard deviation in this idealized calculation is a property of its specified noise model, not the overall accuracy of an instrument. Associate each uncertainty with an inspectable part of the measurement to decide what improvement is useful.

![Constructed 0.5 μL, 70° cap with 2 μm coordinate noise. A compares true and 20 μm-raised baselines; B shows radial residuals; C changes the baseline of one fitted circle; D repeats 300 independent noise simulations. Repeat precision and shared baseline bias are separated.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/e2b3963ddba0b90dd6ed7096.svg?v=e2b3963ddba0)

Figure 2Constructed 0.5 μL, 70° cap with 2 μm coordinate noise. A compares true and 20 μm-raised baselines; B shows radial residuals; C changes the baseline of one fitted circle; D repeats 300 independent noise simulations. Repeat precision and shared baseline bias are separated.

## Adding and removing liquid exposes the contact line's history

Slow addition of liquid does not always move the contact line immediately. The line may remain pinned while the drop height and angle increase at approximately fixed base radius. After reaching a suitable range, it advances and additional liquid mainly expands the contacted area. During withdrawal, the line can again remain fixed while the angle decreases before receding inward. Representative angles associated with these wetting and dewetting processes are called advancing and receding angles. Their difference is contact-angle hysteresis. It carries information about the path followed by the drop that a single stationary image cannot provide.

The teaching model prescribes an advancing threshold of 100° and a receding threshold of 70°. It begins with volume 0.5 μL and angle 85°, adds liquid to 2 μL and then withdraws it to 0.15 μL. While the line is pinned, the program fixes the base radius and solves the spherical-cap volume relation for angle. Once a prescribed threshold is reached, angle remains fixed while the base radius changes. Addition and withdrawal consequently follow different trajectories. The model demonstrates path dependence through explicit rules; it does not infer a real surface's pinning energy or predict its microscopic defects.

Advancing and receding measurements require attention to dosing rate, needle position and whether the contact line actually moves. An angle recorded while volume increases but the line remains pinned identifies a state within the pinned segment, not automatically a steady advancing angle. At higher speeds, viscous flow and other dynamic effects also influence shape. Use corresponding process definitions when comparing surfaces and preserve volume or time sequences so that line motion and angular change can be inspected together. Leading and trailing angles on a tilted substrate, together with sliding behaviour, supply another kind of information with different measurement conditions.

Leaves and petals offer an accessible intuition. Drops on some surfaces are both rounded and easily mobilized; drops on others can be similarly rounded yet strongly retained. A large static angle describes the outline at one moment, while motion depends on how different locations obstruct the contact line. Self-cleaning or low-adhesion designs often require information about advancing, receding and sliding processes. A microarray designed to hold drops at fixed locations may instead benefit from pinning. The useful direction of an experimental indicator follows its connection with function, rather than a universal preference for larger or smaller angles.

## On a textured surface, how much solid does the liquid actually touch?

Texture changes the area contacted by liquid and can retain gas in depressions. A Wenzel state describes liquid following and filling the roughness, creating more actual solid–liquid area per projected area. An idealized relation uses the ratio of actual to projected area as a roughness factor. For a surface already favourable to wetting by the specified liquid, increased actual contact can reduce the apparent angle further; the opposite trend occurs on the other side of the ideal relation. The physical assumption is complete contact with the texture. Merely knowing that a surface is rough does not establish that this state exists.

Cassie–Baxter-type composite contact accounts for different components beneath the drop. A common teaching example has solid tops and gas trapped between them jointly contacting the liquid. Only part of the projected footprint contacts solid; the remainder spans gas. The two illustrated local states use the same texture but different contact arrangements. A large apparent angle can therefore reflect chemistry, texture, composite contact or their combination. To distinguish mechanisms, add observations of morphology, pressure-dependent behaviour or infiltration rather than trying to convert one angle into a unique microscopic structure.

$$
\cos\theta_W=r\cos\theta_Y,\qquad \cos\theta_{CB}=f_s(1+\cos\theta_Y)-1
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4c6f875f1bc533cb7355276e.svg) | Apparent angle for ideal complete wetting of roughness texture. |
| ![Formula](https://ml-biomat.com/static/agent-math/f985068e4f235683ab2c6131.svg) | Simplified apparent angle for composite solid–gas contact. |
| ![Formula](https://ml-biomat.com/static/agent-math/d941e2f726e4aeecee316d62.svg) | Young angle for an ideal smooth surface of the same material. |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | Actual-to-projected solid area ratio; dimensionless and at least one. |
| ![Formula](https://ml-biomat.com/static/agent-math/9112d329658776a27244df88.svg) | Fraction of projected contact area contacting solid; dimensionless, zero to one. |

The two relations assume different contact states. θY=60° and r=1.5 give θW=41.410°; θY=110° and fs=0.2 give θCB=150.274°. Each cosine right-hand side must remain between −1 and 1, with the contact-state assumption supported experimentally.

For an ideal smooth-surface angle of 60° and roughness factor 1.5, the Wenzel relation gives approximately 41.41°. In a separate example with smooth-surface angle 110° and solid-contact fraction 0.2, the simplified solid–gas composite relation gives approximately 150.27°. These numbers correspond to different physical assumptions, not interchangeable algorithms for the same observation. If a relation produces a value outside the allowed cosine range, the assumed finite-angle state cannot be continued in that simple form. Reconsider spreading or a change of contact state rather than hiding the inconsistency by clipping a number.

![Teaching model with prescribed advancing angle 100° and receding angle 70°. Base radius remains fixed during pinning; the relevant angle remains fixed during motion. Lower panels compare locally filled texture and composite solid–gas contact; schematic, not to scale.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/b35937d1c8eca7d162acc10c.svg?v=b35937d1c8ec)

Figure 3Teaching model with prescribed advancing angle 100° and receding angle 70°. Base radius remains fixed during pinning; the relevant angle remains fixed during motion. Lower panels compare locally filled texture and composite solid–gas contact; schematic, not to scale.

Biomaterials can absorb liquid, swell or release soluble components during the measurement. A falling apex can result from outward spreading, infiltration into the material, evaporation, or several processes together. Following base radius, height, volume and time separates possibilities more effectively than plotting only a decreasing angle. For materials used under prolonged immersion, a captive-bubble method or another suitable interfacial measurement may better match the question; specify which phase defines the reported angle. A dry-surface water angle supplies one comparable starting observation, while protein adsorption and cell responses require their own experiments to establish the biological connection.

For example, two polymer films can have similar water angles in air yet develop different adsorbed protein layers after entering a protein-containing solution. Cells subsequently encounter that evolving interface rather than only the chemical groups initially present on a dry film. A study connecting wetting to cell attachment can first record surface treatment and water-angle behaviour, then measure protein adsorption and retention under matched immersion conditions, and finally compare cellular observations. Each step concerns a defined object and time. This gives a stronger mechanistic connection than assigning one supposedly optimal water angle to every biomaterial, regardless of its chemistry, protein environment or intended function.

## Move the baseline slightly and watch the reported angle change

The interactive experiment uses an ideal spherical cap with adjustable true angle, drop volume and analysis-baseline offset. One horizontal reference marks the actual substrate, while the other marks the baseline used for analysis. First set the offset to zero and vary volume. In this gravity-free model the drop grows or shrinks while preserving its specified contact angle. Then fix true angle and volume and move only the analysis baseline. The estimated angle changes although the underlying cap does not. This separates a physical change of shape from a change in interpretation of the same geometry.

Compare smaller and larger drops next. An identical absolute baseline offset occupies a greater fraction of a smaller drop's dimensions and generally produces a larger angular effect. Pixel size, magnification and drop dimensions jointly determine geometrical precision near the contact point. The display also reports base radius and height so angular changes remain connected with physical lengths. When a real drop is substantially flattened by gravity or has a strongly asymmetric contour, choose an analysis model appropriate to that state. The spherical-cap interaction remains an easily checked geometrical reference rather than a substitute for those additional physical effects.

## Cap and baseline: what changes the angle?

Ideal spherical cap, neglecting gravity. Green marks the true surface and purple the analysis baseline. A negative offset extrapolates the circle intersection below the physical contour. Compare volume changes with baseline changes.

[Figure: Spherical cap with true and analysis baselines](https://ml-biomat.com/tutorials/experimental-methods/p03/en/#P03-plot)

## Keep the outline, not only the final angle

The complete Python example generates a cap from volume and angle, adds fixed-seed coordinate noise and fits a circle by least squares. All contour points constrain the centre and radius instead of relying only on the apex and two contact points; a baseline is still needed to obtain the angle. The program exports contour coordinates, radial residuals and baseline sensitivity, then repeats the noise simulation 300 times to show fitting variation at fixed geometry and a specified error model. Contour fitting, baseline selection and repeatability therefore retain separate evidence that can be inspected.

The second part implements the prescribed addition–withdrawal model and saves the entire path of volume, angle and base radius. Its 100° and 70° thresholds are inputs, with 30° hysteresis obtained by subtraction. They illustrate pinning and are not material parameters inferred from the earlier static 70° contour. The final calculations compare two ideal textured-contact examples and illustrate their different states. Keeping these relationships separate makes it clear whether a number was specified, fitted or calculated under a physical assumption.

When organizing repeated measurements, retain the distinction between variation within a specimen and variation among specimens. A standard deviation describes the dispersion of observed repeats. Uncertainty in their mean additionally depends on independent replication and errors shared by the measurements. Reprocessing one image can reveal sensitivity to analysis choices but does not create another independently prepared surface or reveal every contamination problem. Connect each image with its contour, baseline position and specimen identity. An unusual angle can then be investigated as an image-localization issue, local heterogeneity or preparation difference, with a follow-up measurement directed at the relevant cause.

It is also useful to inspect the sign and spatial pattern of contour residuals. Random fluctuations around a fitted circle have a different meaning from a systematic mismatch near the apex or both contact points. A curved pattern can indicate that the spherical-cap approximation is inadequate, while a local mismatch can identify a poorly resolved edge or obstruction. The complete example shows radial residuals because its known contour is circular; another shape model should use a residual definition appropriate to its geometry. Saving these diagnostics makes the reported angle a traceable consequence of a model and an image, rather than an isolated software readout.

The same record structure can support a surface-treatment comparison. Match the probe liquid and measurement process, examine contours at different positions, compare advancing and receding behaviour and connect the results with morphology or surface chemistry. Contact angle offers a rapid interfacial observation whose interpretation also depends on the liquid. Added surfactants, proteins or other solutes may change liquid–gas surface tension with concentration and time. The next chapter shifts attention from a drop meeting a solid to the tension of the liquid interface itself, and how forces and shapes make that quantity measurable.

### Complete Python: cap contours, baselines and contact-angle hysteresis

Generate a specified noisy cap, fit a circle, vary baseline and repeat 300 times, then calculate addition–withdrawal paths under prescribed pinning thresholds.

```
"""Contact-angle geometry, contour fitting and an explicit pinning model.
All droplet observations are constructed teaching data. Historical excerpt:
Thomas Young (1805), An Essay on the Cohesion of Fluids, p. 66; public domain.
Run: python main.py --output results --language en
"""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import brentq
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc,Rectangle

def cap(volume_ul,angle_deg):
    theta=np.deg2rad(angle_deg);R=(3*volume_ul/(np.pi*(1-np.cos(theta))**2*(2+np.cos(theta))))**(1/3)
    return R,R*np.sin(theta),R*(1-np.cos(theta))

def contour(volume_ul,angle_deg,n=180):
    R,a,h=cap(volume_ul,angle_deg);u=np.linspace(-np.deg2rad(angle_deg),np.deg2rad(angle_deg),n)
    return R*np.sin(u),R*np.cos(u)-R*np.cos(np.deg2rad(angle_deg))

def circle_fit(x,y):
    b=np.linalg.lstsq(np.column_stack([2*x,2*y,np.ones(len(x))]),x*x+y*y,rcond=None)[0]
    return b[0],b[1],np.sqrt(b[2]+b[0]**2+b[1]**2)

def apparent_angle(R,cy,baseline):return float(np.rad2deg(np.arccos(np.clip((baseline-cy)/R,-1,1))))

def pinned_volume(a,theta):
    t=np.deg2rad(theta);h=a*np.tan(t/2);return np.pi*h*(3*a*a+h*h)/6

def hysteresis():
    Vup=np.linspace(.5,2,101);Vdown=np.linspace(2,.15,151);initial_a=cap(.5,85)[1]
    up_angles=[];up_a=[]
    for v in Vup:
        if v<=pinned_volume(initial_a,100):theta=brentq(lambda t:pinned_volume(initial_a,t)-v,1,179);a=initial_a
        else:theta=100;a=cap(v,theta)[1]
        up_angles.append(theta);up_a.append(a)
    final_a=up_a[-1];down_angles=[];down_a=[]
    for v in Vdown:
        if v>=pinned_volume(final_a,70):theta=brentq(lambda t:pinned_volume(final_a,t)-v,1,179);a=final_a
        else:theta=70;a=cap(v,theta)[1]
        down_angles.append(theta);down_a.append(a)
    return np.r_[Vup,Vdown],np.r_[up_angles,down_angles],np.r_[up_a,down_a],len(Vup)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args()
    out=args.output;out.mkdir(parents=True,exist_ok=True);tr=lambda z,e:z if args.language=='zh' else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fbfcfc','savefig.facecolor':'#fbfcfc','text.color':'#18344a'})
    blue='#186c94';green='#188777';orange='#d27839'
    def save(f,n):f.savefig(out/f'{n}-{args.language}.svg',bbox_inches='tight');f.savefig(out/f'{n}-{args.language}.png',bbox_inches='tight',dpi=150);plt.close(f)
    volume=.5;angle=70.;R,a,h=cap(volume,angle);x,y=contour(volume,angle)
    rng=np.random.default_rng(1803);xn=x+rng.normal(0,.002,len(x));yn=y+rng.normal(0,.002,len(y))
    cx,cy,rf=circle_fit(xn,yn);fitted=apparent_angle(rf,cy,0)
    residual=np.sqrt((xn-cx)**2+(yn-cy)**2)-rf
    offsets=np.linspace(-.03,.03,121);sensitivity=np.array([apparent_angle(rf,cy,b) for b in offsets])
    monte=[]
    for k in range(300):
        ccx,ccy,rr=circle_fit(x+rng.normal(0,.002,len(x)),y+rng.normal(0,.002,len(y)));monte.append(apparent_angle(rr,ccy,0))
    vols,angles,radii,split=hysteresis()
    summary={'specified_angle_deg':angle,'fitted_angle_deg':fitted,'cap_radius_mm':float(R),'base_radius_mm':float(a),'height_mm':float(h),
       'recovered_volume_ul':float(np.pi*h*(3*a*a+h*h)/6),'height_base_angle_deg':float(np.rad2deg(2*np.arctan(h/a))),
       'baseline_plus20um_angle_deg':apparent_angle(rf,cy,.02),'monte_carlo_sd_deg':float(np.std(monte,ddof=1)),
       'young_angle_deg':float(np.rad2deg(np.arccos(36/72))),'wenzel_60_r15_deg':float(np.rad2deg(np.arccos(1.5*np.cos(np.deg2rad(60))))),
       'cassie_110_f02_deg':float(np.rad2deg(np.arccos(.2*(1+np.cos(np.deg2rad(110)))-1))),
       'hysteresis_deg':30,'bond_R':float(1000*9.81*(R*.001)**2/.072),
       'data_kind':'Constructed spherical-cap observations and prescribed pinning model'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    np.savetxt(out/'data.csv',np.column_stack([xn,yn,residual]),delimiter=',',header='x_mm,y_mm,radial_residual_mm',comments='')
    np.savetxt(out/'hysteresis.csv',np.column_stack([vols,angles,radii]),delimiter=',',header='volume_ul,angle_deg,base_radius_mm',comments='')
    np.savetxt(out/'baseline_sensitivity.csv',np.column_stack([offsets,sensitivity]),delimiter=',',header='baseline_mm,angle_deg',comments='')
    fig,axs=plt.subplots(1,2,figsize=(12,5),gridspec_kw={'width_ratios':[1.1,1]});left,right=axs
    left.imshow(Image.open(Path(__file__).parent/'data/young1805-excerpt.png'));left.axis('off');left.set_title(tr('A  Young，1805年原文第66页','A  Young, 1805, original page 66'),loc='left')
    xx,yy=contour(.5,60);aa=cap(.5,60)[1];right.fill_between(xx,yy,0,color='#c8e4e7');right.plot(xx,yy,color=blue,lw=2);right.axhline(0,color='#576d7b')
    px=aa
    right.annotate('',xy=(px+.35,0),xytext=(px,0),arrowprops={'arrowstyle':'->','color':orange,'lw':2});right.text(px+.12,-.1,'γSV',color=orange)
    right.annotate('',xy=(px-.35,0),xytext=(px,0),arrowprops={'arrowstyle':'->','color':green,'lw':2});right.text(px-.37,-.1,'γSL',color=green)
    right.annotate('',xy=(px-.2,.346),xytext=(px,0),arrowprops={'arrowstyle':'->','color':blue,'lw':2});right.text(px-.14,.38,'γLV',color=blue)
    right.add_patch(Arc((px,0),.35,.35,theta1=120,theta2=180,color=orange,lw=2));right.text(px-.23,.09,'θ')
    right.set_aspect('equal');right.set_xlim(-.9,1.15);right.set_ylim(-.22,.85);right.axis('off');right.set_title(tr('B  在液体一侧读角度','B  Read the angle through the liquid'),loc='left');save(fig,'history')
    fig,axs=plt.subplots(2,2,figsize=(11.5,8.7));p1,p2,p3,p4=axs.ravel()
    p1.scatter(xn,yn,s=7,color=blue,label=tr('构造轮廓点','Constructed contour points'));tt=np.linspace(-np.deg2rad(fitted),np.deg2rad(fitted),300);p1.plot(cx+rf*np.sin(tt),cy+rf*np.cos(tt),color=orange,label=tr('圆拟合','Circle fit'))
    p1.axhline(0,color=green,label=tr('真实基线','True baseline'));p1.axhline(.02,color='#a14e6d',ls='--',label=tr('上移20 μm','Raised by 20 μm'));p1.set_aspect('equal');p1.set_xlabel('x / mm');p1.set_ylabel('y / mm');p1.legend(fontsize=8);p1.set_title(tr('A  轮廓与基线','A  Contour and baseline'),loc='left')
    p2.scatter(np.arange(len(residual)),residual*1000,s=9,color=blue);p2.axhline(0,color='#a1abb2');p2.set_xlabel(tr('轮廓点索引','Contour index'));p2.set_ylabel(tr('径向残差 / μm','Radial residual / μm'));p2.set_title(tr('B  模型与观测的差','B  Model-to-observation differences'),loc='left')
    p3.plot(offsets*1000,sensitivity,color=orange);p3.axhline(70,color=green,ls=':');p3.axvline(0,color='#a1abb2');p3.set_xlabel(tr('基线偏移 / μm','Baseline offset / μm'));p3.set_ylabel(tr('测得接触角 / °','Estimated angle / °'));p3.set_title(tr('C  基线误差的系统影响','C  Systematic effect of baseline error'),loc='left')
    p4.hist(monte,bins=20,color=blue,alpha=.8);p4.axvline(70,color=orange);p4.set_xlabel(tr('重复噪声模拟的角度 / °','Angles across repeated noise simulations / °'));p4.set_ylabel(tr('次数','Count'));p4.set_title(tr('D  300次固定真值重复','D  300 repeats at fixed true geometry'),loc='left')
    fig.tight_layout();save(fig,'measurement')
    fig,axs=plt.subplots(2,2,figsize=(11.5,8));p1,p2,p3,p4=axs.ravel()
    for v,t,aa,col,lab in [(vols[:split],angles[:split],radii[:split],blue,tr('加液','Add liquid')),(vols[split:],angles[split:],radii[split:],orange,tr('抽液','Withdraw liquid'))]:
        p1.plot(v,t,color=col,label=lab);p2.plot(v,aa,color=col,label=lab)
    p1.set_ylabel(tr('角度 / °','Angle / °'));p2.set_ylabel(tr('接触底面半径 / mm','Contact-base radius / mm'))
    for p in [p1,p2]:p.set_xlabel(tr('体积 / μL','Volume / μL'));p.legend()
    p1.set_title(tr('A  规定阈值的钉扎模型','A  Pinning model with prescribed thresholds'),loc='left');p2.set_title(tr('B  角度变化时接触线可不移动','B  The contact line can remain fixed'),loc='left')
    for p,title,filled in [(p3,tr('C  Wenzel：液体填满纹理','C  Wenzel: liquid fills texture'),True),(p4,tr('D  Cassie：纹理间保留气体','D  Cassie: gas remains in the texture'),False)]:
        p.set_xlim(0,6);p.set_ylim(-.3,1.6);p.axis('off');p.add_patch(Rectangle((0,-.3),6,.3,color='#576d7b'))
        if filled:p.add_patch(Rectangle((0,0),6,1.1,color='#c8e4e7'))
        else:p.add_patch(Rectangle((0,.65),6,.45,color='#c8e4e7'))
        for start in np.arange(.3,6,1.2):p.add_patch(Rectangle((start,0),.5,.65,color='#576d7b'))
        p.plot([0,6],[1.1,1.1],color=blue,lw=2);p.set_title(title,loc='left');p.text(3,1.3,tr('局部接触状态示意，非整滴轮廓','Local contact states, not whole-drop outlines'),ha='center',fontsize=9)
    fig.tight_layout();save(fig,'hysteresis')
    print(json.dumps(summary))

if __name__=='__main__':main()
```

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/P03.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Thomas Young — An Essay on the Cohesion of Fluids (1805)](https://upload.wikimedia.org/wikipedia/commons/8/85/Thomas_Young-An_Essay_on_the_Cohesion_of_Fluids.pdf)

   Original pages 65–66 and the historical contact-angle concept.

   Public domain; p. 66 excerpt reproduced.
2. [Wikimedia Commons — Young paper rights and bibliographic record](https://commons.wikimedia.org/wiki/File:Thomas_Young-An_Essay_on_the_Cohesion_of_Fluids.pdf)

   Authorship, date and public-domain status.

   Public Domain Mark 1.0 for the historical scan.
3. [KRÜSS — Contact angle and measurement methods](https://www.kruss-scientific.com/en/know-how/glossary/contact-angle)

   Angle definition, sessile drops and related methods.

   Public manufacturer reference; no illustration copied.
4. [KRÜSS — Young equation](https://www.kruss-scientific.com/en/know-how/glossary/youngs-equation)

   Ideal equilibrium and interfacial contributions.

   Public manufacturer reference; no illustration copied.
5. [KRÜSS — Hysteresis of contact angle](https://www.kruss-scientific.com/en/know-how/glossary/hysteresis-of-the-contact-angle)

   Advancing, receding, pinning and dynamic measurements.

   Public manufacturer reference; original model used.
6. [KRÜSS — Young–Laplace fit](https://www.kruss-scientific.com/en/know-how/glossary/young-laplace-fit)

   Curvature, gravity and contour-model selection.

   Public manufacturer reference; no illustration copied.
7. [KRÜSS — Surface roughness and wetting](https://www.kruss-scientific.com/en/know-how/glossary/roughness)

   Wenzel and Cassie–Baxter states and area definitions.

   Public manufacturer reference; original diagrams used.
8. [KRÜSS — Height-width method](https://www.kruss-scientific.com/en/know-how/glossary/height-width-method)

   Cap geometry and departures from circular outlines.

   Public manufacturer reference; no code copied.
