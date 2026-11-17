# XPS: Reading the outermost layers of a material

Source: https://ml-biomat.com/tutorials/experimental-methods/s07/en/
Language: en

Begin with a spreading water droplet and connect electron energy, surface depth, elemental composition and chemical environments.

## Why does a water droplet suddenly spread?

Place a droplet on an untreated plastic film and it may contract into a rounded bead. After plasma treatment, water may spread across the same kind of film. The two specimens weigh almost the same and feel similar when bent. The important changes can be concentrated within the outermost few nanometres, far thinner than a human hair but exactly where water, proteins, cells and adhesives first meet the material. The questions are concrete: has the surface gained oxygen, which atomic environments have changed, how long does the change last, and does it survive washing? X-ray photoelectron spectroscopy, or XPS, reads chemical information from electrons emitted by these near-surface atoms.

Think of the specimen as a thick book. Weighing it describes the whole book, while XPS gives special attention to the cover and nearby pages. Replacing the cover can change what a reader touches without noticeably changing total mass. The analogy also needs a physical refinement: XPS does not stop at a sharp page boundary. Atoms nearer the outer surface usually contribute more strongly, and contributions decrease progressively with depth. A quoted information depth describes this continuous weighting rather than an impermeable measurement boundary.

In biomaterials research, XPS can track nitrogen appearing after protein adsorption, oxygen-containing environments on polymers or oxide layers on implant materials. The same reasoning supports adhesion, coatings, corrosion, catalysis and electronic devices. A useful research question names an observable change, such as whether the surface nitrogen fraction remains elevated after washing. That wording naturally calls for untreated controls, washing controls and separately prepared specimens. It also helps determine which energy regions and emission angles deserve measurement time.

This chapter connects a binding-energy spectrum to three levels of interpretation: which detectable elements are present, their relative amounts within the sampled region, and whether an element occupies different electronic environments. Elemental composition, the fraction of carbon in a particular environment, and coating thickness can all involve peak areas, but their denominators and physical models differ. Identifying the intended quantity is the first step toward a calculation that answers a scientific question.

## Accounting for the energy needed to remove an electron

An electron in an atom experiences the nucleus and the surrounding electrons. Removing an electron from a bound state requires energy. XPS illuminates a specimen with X-ray photons of known energy; some transfer energy to an electron, which leaves the specimen. The analyzer measures the emitted electron's kinetic energy, the energy associated with its motion. Subtracting this measured energy from the photon budget, while accounting for the analyzer energy reference, gives a binding energy. The calculation resembles an account with identifiable entries: the photon supplies energy, removal uses part of it, and the departing electron carries kinetic energy.

Spectra commonly use electronvolts, abbreviated eV. One electronvolt is the energy associated with moving one elementary charge through a potential difference of one volt. This unit lets us compare atomic energies without repeatedly writing very small numbers in joules. A common aluminum Kα source supplies photons at approximately 1486.6 eV. For a teaching peak with binding energy 284.8 eV and an analyzer work function of 4.5 eV, the measured kinetic energy is 1197.3 eV. A calibrated instrument handles the relevant energy-reference relationships. When working with an exported binding-energy axis, follow its calibration record rather than subtracting the work function again.

$$
E_B=h\nu-E_K-\Phi_{\mathrm{an}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dfd1267e50e10bbc94160d9b.svg) | Binding energy, eV, relative to an appropriately calibrated Fermi-level reference. |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | Planck constant, eV s. |
| ![Formula](https://ml-biomat.com/static/agent-math/5064898bae7c73820eaab47c.svg) | Incident frequency, s⁻¹; hν is photon energy. |
| ![Formula](https://ml-biomat.com/static/agent-math/1d70c8f0e877cac0363c29de.svg) | Kinetic energy measured by the analyzer, eV. |
| ![Formula](https://ml-biomat.com/static/agent-math/83bfd7d1a50c8bb908a1db0d.svg) | Analyzer work function, eV. |

Energy conservation connects known photon energy and measured kinetic energy. For hν=1486.6 eV, EB=284.8 eV and Φan=4.5 eV, EK=1197.3 eV. Insulators require appropriate charge control and referencing; use a calibrated binding-energy axis according to its record.

The historical advance was not simply observing that electrons leave matter, but measuring their energies finely enough to reveal chemical differences. In his 1981 Nobel lecture, Kai Siegbahn described the route from electron focusing and improved resolution toward electron spectroscopy. Small changes associated with chemical environments become useful only when the instrument separates nearby energies. The name ESCA, electron spectroscopy for chemical analysis, captures that connection between an instrumental improvement and a new chemical measurement. The original functional diagram links photon illumination, electron emission and energy analysis, showing how an atomic environment becomes a peak position.

Labels such as C 1s and O 1s combine an element with the orbital involved in emission. C means carbon and 1s identifies a core electronic state; the label does not mean “the first carbon peak.” An element can provide several accessible orbital signals, and some appear as pairs because of spin-orbit coupling. One chemical state can therefore produce more than one line. Carbon bonded to oxygen often has a different electronic environment from carbon bonded only to carbon and hydrogen. For transition-metal compounds, multiplet structure, satellites and the response of the remaining electrons after emission also influence the spectrum. Peak counting becomes chemically useful when these processes are included in the interpretation.

![Original photoemission schematic and energy budget. Depth curves use L=2.5 nm with unit integrated weight and angles measured from the surface normal. The illustrative work function and binding energy complete the 1486.6 eV budget.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/caabf9ed94a3f32d9b362be1.svg?v=caabf9ed94a3)

Figure 1Original photoemission schematic and energy budget. Depth curves use L=2.5 nm with unit integrated weight and angles measured from the surface normal. The illustrative work function and binding energy complete the 1486.6 eV budget.

## Deep illumination, shallow information

X-rays can penetrate much farther into a specimen than the depth that dominates an ordinary XPS spectrum. The emitted electrons still have to travel through matter to reach the surface. An inelastic collision transfers some of their energy to the material. Such electrons may reach the detector with altered energy and contribute to the background, or they may fail to escape. Deeply generated electrons are therefore less likely to retain the characteristic energy used to identify a photoelectron peak. The escape process, rather than the X-ray penetration distance, explains the strong surface sensitivity.

Start with a flat, uniform specimen and approximate the survival of characteristic electrons by exponential attenuation. If the same fraction is lost over every equal path increment, multiplying successive survival fractions produces an exponential. An effective attenuation length, L, summarizes the relevant attenuation for a particular material, electron energy, geometry and analytical application. It is related to the inelastic mean free path, but incorporates the elastic-scattering correction appropriate to the model. When substrate electrons pass through a coating, the relevant value describes those electrons traveling through that coating.

$$
w(z,\theta)=\frac{\exp[-z/(L\cos\theta)]}{L\cos\theta}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/98a7d43466111bfe7c3c78ee.svg) | Normalized depth-signal density, nm⁻¹; integrates to one from zero to infinite depth. |
| ![Formula](https://ml-biomat.com/static/agent-math/9032cb23a878659e74b670d3.svg) | Depth measured along the surface normal, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Effective attenuation length for the electron, material and application model, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | Emission angle from the surface normal; trigonometric evaluation uses radians. |

For a flat uniform specimen, the path is z/cosθ and normalization makes total contribution one. L=2.5 nm, θ=0 and z=2.5 nm give w≈0.14715 nm⁻¹. Elastic scattering and roughness require their appropriate models.

Emission angle changes the path. Here the angle is measured from the surface normal, the direction perpendicular to the surface. Normal emission provides the shortest route from a given vertical depth. An oblique electron must travel farther through material, so the detected signal becomes more strongly weighted toward the surface. Some instruments instead define an angle from the surface plane. The two definitions exchange sine and cosine in the geometry. Checking the definition is a physical part of interpreting an angle series, not merely a notation preference.

We define an information depth containing 95% of the total characteristic signal. It is the depth reached when contributions are accumulated from the surface until their sum reaches 95%, rather than the origin of the deepest detectable electron. For L=2.5 nm, the simple model gives approximately 7.49 nm at normal emission and 3.74 nm at 60°. A small deeper contribution remains. The familiar statement that XPS probes a few nanometres thus becomes a condition-dependent statement involving material, electron energy, surface geometry and the chosen signal fraction.

$$
d_{95}=-L\cos\theta\ln(0.05)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5566087c3ff7062424a56fdd.svg) | Depth containing 95% of characteristic signal, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Effective attenuation length, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | Emission angle from the surface normal. |
| ![Formula](https://ml-biomat.com/static/agent-math/85eb3227c042f8ec4de535b2.svg) | Remaining fraction originating deeper than d95, dimensionless. |

Integrate the normalized depth density to d95 and set the cumulative contribution to 0.95. For L=2.5 nm, d95=7.48933 nm normally and 3.74467 nm at 60°. ln denotes the natural logarithm.

Attenuation can also estimate a coating thickness. Measure a substrate peak before coating, then measure the same peak under matched conditions after coating. A thicker uniform film allows fewer substrate electrons to retain their characteristic energy. In the teaching model with L=2.5 nm, a 2 nm layer leaves about 44.9% of the bare-substrate signal at normal emission and 20.2% at 60°. Measuring several angles tests whether the change follows a uniform-film description. Roughness, pinholes and islands produce different path distributions; those specimens call for a model of coverage or geometry that matches their structure.

$$
r=\frac{I_{\mathrm{sub}}}{I_{\mathrm{bare}}}=\exp\!\left(-\frac{d}{L\cos\theta}\right),\qquad d=-L\cos\theta\ln r
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | Coated-to-bare substrate peak-area ratio, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/1d414a7153e40c5c4b33cda1.svg) | Net areas of the same substrate line with and without coating under matched conditions, common units. |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | Uniform overlayer thickness, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Attenuation length of substrate electrons in the overlayer for this application, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | Emission angle from the surface normal. |

For a continuous flat overlayer, matched acquisition and stable substrate, path attenuation explains signal change. d=2 nm, L=2.5 nm and θ=0 give r=0.449329; at 60°, r=0.201897. Thickness inversion requires 0<r≤1.

The interactive experiment separates three influences: coating thickness, emission angle and attenuation length. Increasing thickness suppresses the substrate, while increasing angle from the normal makes a fixed layer appear more effective at suppressing it. Changing L represents a different electron-material attenuation condition. The plotted depth weighting and the displayed substrate ratio use the same model. This lets you distinguish an experimentally measured ratio from the assumptions used to turn that ratio into a thickness. The simple angle range stops at 60°, where treating L as fixed is a more useful introductory approximation than at extreme grazing emission.

## Change the viewing angle

Thickness, angle and attenuation length determine the surviving substrate peak. The depth contribution integrates to one; angle is measured from the surface normal.

[Figure: Interactive overlayer and signal-depth plot](https://ml-biomat.com/tutorials/experimental-methods/s07/en/#S07-plot)

## How a real specimen enters the measurement

A newly prepared film can change during packaging, transport, handling, washing and drying. Because XPS emphasizes the outer few nanometres, organic residue from handling, salts from washing solutions and siloxanes transferred from mounting materials can become visible signals. First decide whether the target is the as-prepared surface, a washed surface or a surface recovered after use in solution. Each is a legitimate scientific object, and their compositions need not match. Consistent exposure, washing and storage procedures define which surface state is being compared.

Conventional XPS operates in high or ultrahigh vacuum. Vacuum reduces collisions between traveling electrons and gas molecules and slows contamination of the exposed surface by residual gas. Dry films and metal pieces are relatively straightforward specimens. Hydrogels, cells and volatile materials require explicit attention to water loss and structural changes in vacuum. If the scientific question concerns a hydrogel-water interface, distinguish the dried surface from the hydrated interface. Cryogenic transfer, low-temperature measurement and near-ambient-pressure instruments provide different ways of preserving or controlling a desired state, depending on the available electron optics and environmental arrangement.

Insulating specimens introduce another physical effect. As electrons leave, positive charge can accumulate locally. Subsequent electrons experience an additional electric potential, which lowers their measured kinetic energy and raises the apparent binding energy. Uniform charging may shift peaks together. Differences in conductivity, thickness or electrical contact can produce differential charging, broadening peaks or creating shoulders. Charge-neutralization systems supply low-energy electrons or other compensating charge, while specimen mounting and electrical contact also matter. Applying one numerical shift to a carbon peak cannot reverse a distortion caused by different regions shifting by different amounts.

Energy referencing should therefore follow the specimen chemistry. What substance supplies the proposed reference peak? Is it present, and does it retain the same environment after treatment? In a functionalized polymer, the tallest carbon contribution is not automatically a universal contamination reference. Check neutralizer stability and repeated-scan movement, then compare with a suitable reference and known material. When a numerical correction is used, retaining its magnitude and basis keeps the spectrum connected to the specimen and acquisition conditions.

Acquisition usually begins with a broad survey, followed by narrower high-resolution regions. The survey locates expected elements and unexpected contaminants. Narrow scans investigate whether an individual region contains distinguishable contributions. Analyzer pass energy affects the balance between throughput and energy resolution. Reducing the energy step provides denser sampling but does not automatically remove broadening from the source and analyzer. A material that changes under X-ray exposure can be monitored with repeated short scans at one location, comparing composition and line shape over exposure time before selecting the final dose and measurement sequence.

A useful measurement plan connects these choices to the expected difference. For an oxygen-rich surface treatment, collect sufficient carbon and oxygen signal under compatible quantitative conditions, examine the carbon region with adequate resolution, and reserve positions for independent checks. If nitrogen after protein adsorption is expected to be weak, background definition and counting time near N 1s deserve particular attention. The instrument settings are consequences of the question: a small chemical shift and a small elemental fraction require different kinds of evidence. The illuminated area also matters. A spectrum averages over that area, so a narrow stripe of coating and a neighboring bare region may contribute together. Comparing the beam footprint with specimen features helps determine whether a change represents local chemistry, incomplete coverage or averaging across different structures. Mapping several positions can resolve that spatial question before a single averaged percentage is assigned to the whole specimen.

## A larger peak can mean a stronger response

An oxygen peak taller than a carbon peak does not directly establish that oxygen atoms are more numerous. Orbitals differ in their probability of emitting electrons after photon absorption, and transmission and attenuation vary with electron energy. Elemental comparison therefore starts with sensitivity-corrected peak areas. An area sums the signal above background across the energy interval. Multiplying signal by each small energy increment and adding the contributions preserves the electrons spread across a broad peak, making area more suitable than peak height for many quantitative comparisons.

A relative sensitivity factor, or RSF, converts different elemental responses to a comparable scale. The factor must match the instrument, photon source, acquisition mode and selected spectral line. The teaching example assigns carbon, nitrogen and oxygen areas of 5000, 1200 and 9000, with factors 1.0, 1.8 and 3.0. Oxygen accounts for about 59.2% of the raw area. After correction, the three comparable quantities are 5000, 666.7 and 3000, giving an oxygen fraction of approximately 34.6%. These deliberately specified factors illustrate the arithmetic; real analyses use verified instrument information or suitable reference materials.

$$
x_i=\frac{A_i/S_i}{\sum_j A_j/S_j}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/10c16af3229388fdcbca3de7.svg) | Equivalent homogeneous atomic fraction of element i among included detectable elements, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/081841f943a2910bf49ac5b3.svg) | Net line areas after appropriate background removal, in consistent count and energy units. |
| ![Formula](https://ml-biomat.com/static/agent-math/6398be9a730b07210cb4c69e.svg) | Relative sensitivity factors matched to source, line and acquisition mode, on a common scale. |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | Element indices; summation covers all elements included in quantification. |

Divide area by response factor, then normalize comparable signals. C/N/O areas 5000/1200/9000 and teaching factors 1/1.8/3 give oxygen fraction 0.346154, or 34.6154 at.%. Layered specimens have surface weighting, and hydrogen is normally absent from this denominator.

The denominator contains the analyzed elements with usable signals. Routine XPS elemental analysis generally does not directly include hydrogen or helium, so a reported carbon fraction is not automatically a fraction of every atom in the material. If the sampled region is layered, the uniform-composition calculation gives an equivalent composition with surface weighting. A thin oxygen-rich film on a carbon substrate produces a result depending on film chemistry, thickness, substrate contribution and emission angle. The calculation remains useful when the physical meaning of its denominator and weighting is kept explicit.

![Constructed survey and sensitivity correction. Peak positions illustrate elemental regions, and RSFs are teaching factors. Corrected oxygen represents about 34.6% of the included elements, compared with a different raw-area percentage.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/ca80e2c18d7bd0e974fc3a55.svg?v=ca80e2c18d7b)

Figure 2Constructed survey and sensitivity correction. Peak positions illustrate elemental regions, and RSFs are teaching factors. Corrected oxygen represents about 34.6% of the included elements, compared with a different raw-area percentage.

Repeated measurements also need a defined object. Three successive scans at one position mainly describe local counting variation, stability and exposure effects. Three positions on one specimen reveal lateral heterogeneity. Three separately prepared specimens address preparation repeatability more directly. The final figure includes explicitly constructed values for three independent specimens per condition, preserving each point and showing the mean with sample standard deviation. This distinguishes a stable reading on one specimen from a preparation process that consistently produces similar surfaces.

Chemical-state fractions within one elemental region use a different denominator. If a C 1s model has chemically justified contributions, an individual component area divided by total C 1s area describes a depth-weighted fraction of carbon in that environment. It differs from oxygen atomic percentage. A carboxyl group contains one carboxyl carbon and two oxygens, while an ether oxygen may connect two carbons. A component described as oxygen-associated carbon therefore does not translate into oxygen atom count through a universal one-to-one rule. Comparing elemental composition with carbon-environment fractions provides a valuable consistency check on the proposed chemical model.

Units help maintain that consistency. A spectrum in counts per second integrated over eV gives an area in counts per second times eV. Areas collected with different dwell times or analyzer settings become comparable only after the appropriate normalization and transmission handling. If software already applies a correction, applying it again changes the result. Working through one complete numerical example, including background and units, establishes exactly what the software's final percentage represents.

## Peak fitting is a chemical explanation

A broad envelope can contain several chemical environments, but it can also reflect instrumental broadening, disorder, satellite processes or charging. Peak fitting builds a model of these contributions and asks whether it explains the observations. Candidate components should follow molecular structure, treatment chemistry, references and other spectral regions. For an ester-containing polymer, backbone carbon, carbon attached to oxygen and carbonyl-related environments provide a chemically motivated starting point. Adding a component for every small fluctuation makes the curve more flexible while weakening the connection between fitted components and chemistry.

Background is part of the explanation. Electrons that lose energy produce a continuous contribution that changes across the spectrum. A straight line may be adequate for a narrow, slowly varying local background. Shirley and Tougaard methods describe different relationships and must be selected with the spectral shape, energy window and analytical purpose in mind. Endpoint placement and neighboring peaks influence the resulting areas. Retaining both the background and the background-subtracted spectrum makes those choices visible and lets you inspect whether the baseline behaves sensibly on either side of the region.

The complete example constructs three Gaussian contributions at specified energies, with areas 6500, 2200 and 1300, adds a linear background and then generates Poisson counting noise for a stated dwell time. Gaussian shapes and a linear background are declared conditions of this teaching experiment. Because the target is known, we can see what a model gets right and what it leaves unexplained. The fit estimates component areas, a common width and background parameters, and is compared with a model containing only two components. It tests the consequences of omitting a real contribution rather than identifying functional groups automatically in an unknown material.

![Constructed C 1s region with teaching areas 6500, 2200 and 1300 counts s⁻¹ eV, common Gaussian sigma 0.48 eV and 0.4 s dwell per point. Upper panels show observations and fits; lower panels show observed-minus-fitted residuals. The two-component model omits a known contribution.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/f6bd0bb8a24e0378095a3f57.svg?v=f6bd0bb8a24e)

Figure 3Constructed C 1s region with teaching areas 6500, 2200 and 1300 counts s⁻¹ eV, common Gaussian sigma 0.48 eV and 0.4 s dwell per point. Upper panels show observations and fits; lower panels show observed-minus-fitted residuals. The two-component model omits a known contribution.

A residual is the observed signal minus the fitted signal at each energy. The three-component model leaves fluctuations mainly around zero; the incomplete model leaves a coherent feature near the omitted contribution. Structured residuals identify unexplained information, while the next investigation can concern chemistry, background, charging or line shape. In real analysis, constraints on positions, widths and doublet ratios should follow the relevant physics. Allowing every parameter to vary freely can produce several similar-looking fits with different interpretations. Transition-metal spectra with strong multiplet structure benefit from appropriate reference spectra and dedicated models before numerical fitting begins.

Uncertainty follows the same chain. Longer counting reduces relative counting fluctuations and can stabilize a fit. It does not select a correct background or establish the energy reference. Reanalyzing a spectrum across several defensible endpoint choices and width constraints reveals sensitivity to analytical decisions. Compare that sensitivity with the observed treatment effect and the variation between independently prepared specimens. If the desired distinction is small on those scales, improving specimen preparation, controls or acquisition can make the chemical difference more distinguishable. Additional decimal places do not perform that experimental work.

The program exports the survey, component region, fitted and incomplete models, residuals and a compact numerical summary. The summary contains the recovered fraction of oxygen-associated carbon, which should lie near the constructed value of 0.35, as well as the oxygen elemental fraction from the separate survey example. Keeping both quantities in the output makes their different denominators inspectable. The same script creates all four explanatory figures, so the numbers in the plots can be traced to the exported arrays rather than read from an isolated image.

### A complete XPS teaching experiment from depth weighting to peak fitting

Constructed data are fully specified in the script; a fixed seed produces four figure groups, raw and processed tables, and a numerical summary.

```
"""Constructed XPS experiments: surface weighting, composition and peak models."""
from pathlib import Path
import argparse, json
import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Arc

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en')
    args=parser.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True)
    zh=args.language=='zh';T=lambda z,e:z if zh else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,
        'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold',
        'axes.labelcolor':'#243c49','text.color':'#243c49','axes.edgecolor':'#8da0a6',
        'figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','svg.fonttype':'path'})
    blue,green,red,gold='#286488','#008b7b','#dc604d','#c39227'
    def save(fig,name):
        fig.tight_layout(pad=1.6)
        for ext in ['svg','png']:fig.savefig(out/f'{name}-{args.language}.{ext}',dpi=155,bbox_inches='tight')
        plt.close(fig)
    def gaussian(x,mu,sigma):return np.exp(-.5*((x-mu)/sigma)**2)/(sigma*np.sqrt(2*np.pi))

    fig,ax=plt.subplots(1,3,figsize=(14,4.8),gridspec_kw={'width_ratios':[1.1,1,1]})
    a=ax[0];a.set(xlim=(0,10),ylim=(0,10));a.axis('off')
    a.add_patch(Rectangle((.5,.5),9,3.8,color='#dbe5e7'));a.plot([.5,9.5],[4.3,4.3],color=blue,lw=2)
    a.annotate(T('X 射线','X-rays'),xy=(4.3,4.2),xytext=(.6,8.8),arrowprops={'arrowstyle':'->','color':gold,'lw':3},fontsize=13)
    a.add_patch(FancyArrowPatch((4.4,3.8),(7.1,8.3),arrowstyle='->',mutation_scale=15,color=green,lw=3))
    a.text(7.5,7.5,T('电子\n至分析器','Electron\nto analyzer'),fontsize=9,ha='left')
    a.plot([4.4,4.4],[3.8,9],ls=':',color='#7b929a');a.text(4.4,9.4,T('表面法线','Surface normal'),fontsize=10,ha='center')
    a.add_patch(Arc((4.4,3.8),4,4,theta1=58,theta2=90,color=blue));a.text(4.8,6.1,r'$\theta$')
    a.plot([2,2.7,2.2,3.1],[1.5,2.3,2.9,3.6],color=red,lw=2);a.text(.8,.8,T('碰撞损能 → 背景','Energy loss → background'),fontsize=10)
    a.set_title(T('A  从光子到电子','A  From photon to electron'),loc='left')
    z=np.linspace(0,15,400);L=2.5
    for angle,c in [(0,green),(60,blue)]:
        weight=np.exp(-z/(L*np.cos(np.deg2rad(angle))))/(L*np.cos(np.deg2rad(angle)))
        ax[1].plot(z,weight,color=c,label=f'{angle}°')
    ax[1].set(xlabel=T('深度 / nm','Depth / nm'),ylabel=T('归一化信号权重 / 每 nm','Normalized signal weight / per nm'))
    ax[1].legend(title=T('相对法线角度','Angle from normal'));ax[1].set_title(T('B  表面贡献更大','B  Surface-weighted signal'),loc='left')
    ax[2].barh([0,1,2],[284.8,4.5,1197.3],color=[blue,gold,green]);ax[2].set_yticks([0,1,2],[T('结合能','Binding energy'),T('分析器功函数','Analyzer work function'),T('测得动能','Measured kinetic energy')]);ax[2].set_xlabel('eV');ax[2].set_xlim(0,1400)
    for y,v in enumerate([284.8,4.5,1197.3]):ax[2].text(v+25,y,str(v),va='center',fontsize=10)
    ax[2].set_title(T('C  1486.6 eV 的能量账本','C  A 1486.6 eV energy budget'),loc='left')
    save(fig,'photoemission')

    e=np.linspace(0,800,4001);areas=np.array([5000.,1200.,9000.]);rsf=np.array([1.,1.8,3.]);centers=[284.8,400,532];labels=['C 1s','N 1s','O 1s']
    base=50+.035*e;survey=base+sum(a*gaussian(e,m,2.2) for a,m in zip(areas,centers));fractions=(areas/rsf)/sum(areas/rsf)
    fig,ax=plt.subplots(1,2,figsize=(12,4.8),gridspec_kw={'width_ratios':[1.55,1]})
    ax[0].plot(e,survey,color=blue);ax[0].invert_xaxis();ax[0].set(xlabel=T('结合能 / eV','Binding energy / eV'),ylabel=T('教学信号 / counts s⁻¹','Teaching signal / counts per second'))
    for m,l in zip(centers,labels):ax[0].annotate(l,(m,np.interp(m,e,survey)),xytext=(m+40,np.interp(m,e,survey)+100),arrowprops={'arrowstyle':'-','color':blue})
    ax[0].set_ylim(0,2100);ax[0].set_title(T('A  全谱先找到元素','A  Survey identifies elements'),loc='left')
    x=np.arange(3);ax[1].bar(x-.18,areas/areas.sum()*100,.36,label=T('直接按面积','Raw area fraction'),color=gold);ax[1].bar(x+.18,fractions*100,.36,label=T('灵敏度校正后','Sensitivity-corrected'),color=green);ax[1].set_xticks(x,labels);ax[1].set_ylabel('%');ax[1].set_ylim(0,80);ax[1].legend(fontsize=9);ax[1].set_title(T('B  不同元素的响应不同','B  Unequal elemental response'),loc='left')
    save(fig,'composition');np.savetxt(out/'survey.csv',np.c_[e,survey,base],delimiter=',',header='binding_energy_eV,signal_counts_per_s,background_counts_per_s',comments='')
    np.savetxt(out/'composition.csv',np.c_[areas,rsf,fractions],delimiter=',',header='area_counts_per_s_eV,teaching_RSF,atomic_fraction',comments='')

    rng=np.random.default_rng(570);x=np.linspace(282,292,501);mu=np.array([284.8,286.4,288.8]);trueA=np.array([6500,2200,1300]);sigma=.48;dwell=.4
    baseline=110+3*(x-282);true=baseline+sum(a*gaussian(x,m,sigma) for a,m in zip(trueA,mu));observed=rng.poisson(true*dwell)/dwell
    def model(x,a,b,c,w,p,q):return p+q*(x-282)+sum(A*gaussian(x,m,w) for A,m in zip([a,b,c],mu))
    p,cov=curve_fit(model,x,observed,p0=[6000,2000,1000,.5,100,2],sigma=np.sqrt(np.maximum(observed*dwell,1))/dwell,absolute_sigma=True,bounds=([0,0,0,.2,0,-10],[20000,20000,20000,1.2,500,20]))
    def incomplete(x,a,b,w,p,q):return p+q*(x-282)+a*gaussian(x,mu[0],w)+b*gaussian(x,mu[1],w)
    q,_=curve_fit(incomplete,x,observed,p0=[6500,2200,.5,100,2],bounds=([0,0,.2,0,-10],[20000,20000,1.2,1500,100]))
    fitted=model(x,*p);wrong=incomplete(x,*q);fitbase=p[4]+p[5]*(x-282)
    fig,ax=plt.subplots(2,2,figsize=(12,7.4),gridspec_kw={'height_ratios':[2,1]})
    for col,(fit,title) in enumerate([(fitted,T('A  三个已知教学环境','A  Three specified teaching environments')),(wrong,T('B  漏掉一个环境','B  One environment omitted'))]):
        ax[0,col].plot(x,observed,color='#9aa9ac',lw=.8,label=T('计数噪声数据','Count-noise data'));ax[0,col].plot(x,fit,color=green if col==0 else red,lw=2,label=T('拟合','Fit'));ax[0,col].set_title(title,loc='left');ax[0,col].legend(fontsize=9)
        ax[1,col].axhline(0,color='#8b9b9e',lw=1);ax[1,col].plot(x,observed-fit,color=blue if col==0 else red,lw=.9);ax[1,col].set_xlabel(T('结合能 / eV','Binding energy / eV'));ax[1,col].set_ylabel(T('残差 / counts s⁻¹','Residual / counts per second'))
        for row in [0,1]:ax[row,col].invert_xaxis()
    for a,m,c in zip(p[:3],mu,[blue,gold,red]):ax[0,0].fill_between(x,fitbase,fitbase+a*gaussian(x,m,p[3]),color=c,alpha=.2)
    ax[0,0].set_ylabel(T('信号 / counts s⁻¹','Signal / counts per second'));save(fig,'peak-model')
    np.savetxt(out/'carbon_region.csv',np.c_[x,observed,baseline,fitted,wrong,observed-fitted],delimiter=',',header='binding_energy_eV,observed_counts_per_s,true_background,three_component_fit,two_component_fit,residual',comments='')

    fig,ax=plt.subplots(1,3,figsize=(14,4.8));d=np.linspace(0,10,300)
    for ang,c in [(0,green),(30,gold),(60,blue)]:ax[0].plot(d,np.exp(-d/(L*np.cos(np.deg2rad(ang)))),color=c,label=f'{ang}°')
    ax[0].legend();ax[0].set(xlabel=T('均匀覆盖层厚度 / nm','Uniform overlayer thickness / nm'),ylabel=T('基底峰 / 裸基底峰','Substrate peak / bare-substrate peak'));ax[0].set_title(T('A  倾斜使基底更难看见','A  Tilt suppresses the substrate'),loc='left')
    xx=np.linspace(281,290,700);normal=gaussian(xx,284.8,.45);uniform=gaussian(xx,286.3,.45);differential=.6*gaussian(xx,284.8,.45)+.4*gaussian(xx,286.3,.45)
    ax[1].plot(xx,normal,color=green,label=T('无偏移','Unshifted'));ax[1].plot(xx,uniform,color=gold,label=T('整体 +1.5 eV','Uniform +1.5 eV'));ax[1].plot(xx,differential,color=red,label=T('不同区域带电不同','Differential charging'));ax[1].invert_xaxis();ax[1].set(xlabel=T('表观结合能 / eV','Apparent binding energy / eV'),ylabel=T('等面积信号 / 每 eV','Equal-area signal / per eV'));ax[1].legend(fontsize=8);ax[1].set_title(T('B  电势也会移动峰','B  Potential also shifts peaks'),loc='left')
    samples=np.array([8.,9.,7.,18.,20.,17.]);ax[2].scatter([0,0,0,1,1,1],samples,color=[blue]*3+[green]*3,s=45);ax[2].errorbar([0,1],[samples[:3].mean(),samples[3:].mean()],yerr=[samples[:3].std(ddof=1),samples[3:].std(ddof=1)],fmt='_',ms=22,color='#243c49',capsize=5);ax[2].set_xticks([0,1],[T('处理前','Before'),T('处理后','After')]);ax[2].set(xlim=(-.5,1.5),ylim=(0,25),ylabel=T('氧原子百分比 / at.%','Oxygen atomic percentage / at.%'));ax[2].set_title(T('C  三个独立试样','C  Three independent specimens'),loc='left');save(fig,'decisions')
    summary={'example_kinetic_energy_eV':1486.6-284.8-4.5,'information_depth_95_normal_nm':-L*np.log(.05),'information_depth_95_60deg_nm':-L*.5*np.log(.05),'substrate_ratio_2nm_normal':float(np.exp(-2/L)),'substrate_ratio_2nm_60deg':float(np.exp(-2/(L*.5))),'oxygen_atomic_fraction':float(fractions[2]),'fitted_oxygenated_carbon_fraction':float(sum(p[1:3])/sum(p[:3])),'true_oxygenated_carbon_fraction':.35,'fit_rms_counts_per_s':float(np.sqrt(np.mean((observed-fitted)**2))),'incomplete_fit_rms_counts_per_s':float(np.sqrt(np.mean((observed-wrong)**2))),'teaching_data':True}
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':main()
```

## Turning surface chemistry into the next experiment

Return to the water droplet. Suppose treatment increases the measured oxygen fraction and the oxygen-associated contributions to C 1s. More focused questions now follow. Is the change concentrated at the outer surface? Do oxygen signal and wetting behavior evolve together after a week? Does the change survive washing? Has roughness changed as well? An angle series addresses depth distribution, a time series follows rearrangement or contamination, washing controls examine retained surface species, and morphology measurements examine geometry. Each measurement tests a particular explanation, turning a spectrum into a research decision.

![Three teaching diagnostics. A: substrate attenuation through a uniform film, L=2.5 nm. B: equal-area signals under uniform or differential charging show how potential distributions produce shoulders. C: constructed oxygen fractions for three independent specimens per condition; horizontal marks show means and error bars show sample standard deviations.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/3a1440b3023c484ecb9b804c.svg?v=3a1440b3023c)

Figure 4Three teaching diagnostics. A: substrate attenuation through a uniform film, L=2.5 nm. B: equal-area signals under uniform or differential charging show how potential distributions produce shoulders. C: constructed oxygen fractions for three independent specimens per condition; horizontal marks show means and error bars show sample standard deviations.

Protein adsorption offers another natural example. On a substrate initially containing little nitrogen, an emerging N 1s signal supports the appearance of nitrogen-containing material near the surface. Comparing a buffer-treated control with a protein-treated specimen under matched washing conditions helps distinguish contributions from salts, additives and protein-associated coverage. Protein function can then be examined using binding, enzymatic or cellular measurements. Surface chemistry and biological response describe different aspects of the interface; together they can explain why a surface adsorbs substantial protein yet produces an unexpected functional response.

Depth analysis can also remove material progressively by ion sputtering. Because this changes the specimen, interpretation must consider preferential removal, oxide reduction, polymer bond breaking and mixing between layers. If preserving organic chemistry is central, angle-resolved measurements or suitable cluster-ion conditions can be investigated and checked against reference materials. Thickness, composition and chemical state are distinct quantities. Some questions require independent thickness information, some require cross-sectional structure, and others require a more stable energy reference. Naming that missing measurement turns it into a productive next step.

A clear presentation places the survey, relevant narrow regions, backgrounds, components, residuals and specimen repeats where they can be compared. State specimen condition, source, acquisition settings, emission-angle definition, charge handling and energy reference, and define each percentage denominator. A reader can then reconstruct the reasoning: photons excite electrons; escape creates surface weighting; energy positions reveal electronic environments; appropriately corrected areas estimate composition; and controlled comparisons connect composition to material behavior. The same chain applies to a plastic film, a protein-coated sensor and an oxidized metal.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/S07.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Introduction to X-ray photoelectron spectroscopy](https://mmrc.caltech.edu/XPS%20Info/Practical%20Guides%20to%20XPS/Intro%20to%20XPS.pdf)

   Photoelectron energy, instrument, chemical shifts and surface sensitivity.
2. [Practical guides: First steps in planning, conducting and reporting XPS](https://mmrc.caltech.edu/XPS%20Info/XPS%20practical%20guide.pdf)

   Question design, specimen condition, handling and reporting.
3. [XPS guide: Charge neutralization and binding energy referencing](https://mmrc.caltech.edu/XPS%20Info/Practical%20Guides%20to%20XPS/XPS%20guide%20charge%20neutralization.pdf)

   Insulator charging, differential charging and referencing.
4. [Practical guides: Quantitative XPS](https://ywcmatsci.yale.edu/sites/default/files/files/Practical%20guides%20for%20x-ray%20photoelectron%20spectroscopy%20-%20Quantitative%20XPS.pdf)

   Sensitivity factors, background, atomic fractions and film quantification.
5. [NIST: Inelastic mean free paths, effective attenuation lengths and information depths](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=929257)

   Distinguish mean free path, effective attenuation length and information depth.
6. [Kai Siegbahn: Electron spectroscopy for atoms, molecules and condensed matter](https://wiki.epfl.ch/mep/documents/MEP%5B09-10%5D_DOWNLOAD/siegbahn_nobellecture.pdf)

   1981 Nobel lecture: electron focusing, resolution and chemical analysis.
7. [Thermo Fisher: XPS quick guide](https://documents.thermofisher.com/TFS-Assets/MSD/Flyers/xps-quick-guide-fl0163.pdf)

   Source, electron analyzer and common surface applications.
