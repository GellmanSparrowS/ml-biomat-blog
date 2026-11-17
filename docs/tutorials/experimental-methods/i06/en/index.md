# XRD: From peak positions to crystal structure

Source: https://ml-biomat.com/tutorials/experimental-methods/i06/en/
Language: en

Connect peak position, width and area to atomic periodicity, coherent length and scattering contributions.

## If calcium and phosphorus are present, why measure diffraction?

A bone-repair material develops a new surface deposit after exposure to solution, and elemental analysis detects calcium and phosphorus. The next question is how those elements are arranged: which crystal structure formed, or did the deposit remain without long-range order? Composition resembles an ingredient list. The same ingredients can be organized differently, with different consequences for material behavior. X-ray diffraction, abbreviated XRD, uses scattering and interference from atomic arrangements to turn spatial periodicity into intensity variations at particular angles. Peak positions, intensities and widths therefore provide distinct kinds of structural information.

Polymers raise similar questions. Heating, cooling, stretching or adding filler can change the amount, orientation and scale of ordered regions, affecting transparency, stiffness or barrier properties. XRD expresses these changes through comparable patterns, but a taller peak does not directly mean more crystallinity, and a broader peak does not directly mean smaller particles. Establishing the origin of each curve feature before selecting a calculation makes the pattern part of a structural explanation. The useful starting point is the measurement question, rather than a list of parameters that software can produce.

This chapter begins with waves reinforcing one another, then develops the Bragg relation, powder patterns, line widths and area decomposition. No prior crystallography is assumed. The central connection is between repeated atomic arrangements and directions where a detector receives stronger signals. Later, explicitly constructed peaks allow position shifts, size broadening, instrument broadening and background choices to be changed independently. Observing their separate effects builds an intuition for the physical question behind each calculation before applying a similar workflow to experimental data.

## When wave crests arrive together, atomic order becomes directional information

Two stones dropped into water produce ripples that reinforce in some places and partly cancel in others. Their combination depends on phase: where each wave is within its repeating cycle when it arrives. When X-rays illuminate matter, electrons scatter the radiation. Waves scattered from many atoms combine at the detector. Regularly repeated atomic positions create directions where path differences let crests arrive together, strengthening the signal. A diffraction pattern records this directional selection. It is therefore different from a directly magnified picture of atoms, even though it can constrain their arrangement.

The discovery of crystal X-ray diffraction in 1912 connected the wave nature of X-rays with internal crystal periodicity. Subsequent work by the Braggs described strong scattering directions through path differences between parallel lattice planes and used angular measurements to investigate structures. This was an important change in how the invisible could be studied: one did not need to see each atom directly to determine spacing from wave interference. The planes drawn in the figure are geometrical constructions. Actual scattering comes from electrons in the material; imagining ordinary stacked mirrors helps sketch the geometry but does not replace that physical mechanism.

![Original Bragg geometry and early angular-measurement concept. Neighboring planes introduce an extra path and integer-wavelength matching reinforces scattering. Planes are geometrical constructions; not to scale. Historical connection: crystal diffraction and structural measurements in 1912–1913.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/2644e7ff6bbcf3a75cf6f2ac.svg?v=2644e7ff6bbc)

Figure 1Original Bragg geometry and early angular-measurement concept. Neighboring planes introduce an extra path and integer-wavelength matching reinforces scattering. Planes are geometrical constructions; not to scale. Historical connection: crystal diffraction and structural measurements in 1912–1913.

Consider waves scattered from two neighboring planes. The wave associated with the deeper plane travels an extra distance both entering and leaving. Together, these contributions equal twice the plane spacing multiplied by the sine of the glancing angle. If that additional path equals one, two or another whole number of wavelengths, the waves align again and reinforce. This gives the Bragg relation. The angle θ is measured between a ray and the lattice plane, whereas a typical powder-pattern axis gives 2θ, the scattering angle between the incident and diffracted beam directions. Drawing the geometry helps prevent this common factor-of-two mistake.

$$
2d\sin\theta=n\lambda
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | Spacing between neighboring parallel lattice planes, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | Angle between ray and lattice plane; patterns usually plot 2θ. Convert to radians for numerical trigonometric functions. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Diffraction order, positive integer; one here. |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | X-ray wavelength, nm; 0.15406 nm here. |

Neighboring planes give an additional path 2d sinθ; an integer wavelength aligns the waves. For d=0.25 nm and n=1, θ=arcsin(0.15406/0.5)≈17.946°, so the plotted peak occurs at 2θ≈35.892°.

With wavelength known, a measured peak angle gives a corresponding plane spacing. For X-rays of wavelength 0.15406 nm, a spacing of 0.25 nm produces a first-order peak near 2θ=35.89°. If the lattice expands uniformly, spacing increases and θ must decrease to retain the required path difference. The peak moves to lower angle, as the interactive experiment demonstrates. Experimental shifts can also arise from specimen height, angular zero or temperature-dependent conditions. Interpreting a lattice change therefore calls for geometrical calibration and specimen-state information together.

## Why many randomly oriented crystallites produce a readable curve

A single crystal has a relatively consistent orientation, so rotation brings different lattice planes into diffraction conditions. A powder contains many crystallites. In the ideal powder approximation, their orientations are sufficiently diverse that some contribute to each allowed reflection. Scattering associated with a given spacing forms a set of directions in space. A two-dimensional detector can record rings, while a scanning detector records intensity as a function of angle and produces an intensity–2θ curve. This turns a collection of differently oriented crystallites into a convenient structural pattern, explaining the broad use of powder diffraction in materials identification.

Crystallographic planes are commonly labeled with three integers called Miller indices, written h, k and l. Initially, think of these as labels for sets of parallel planes with particular orientations and spacings. Different labels describe different geometry, but whether a strong reflection appears also depends on atomic positions and scattering strengths within the unit cell. Contributions can cancel in certain directions, leading to systematic absences. Cell dimensions alone therefore do not predict every intensity. Atomic species and their internal arrangement also determine the pattern, which is why a structural model contains more than a list of lattice spacings.

A randomly oriented powder is an idealization that preparation tries to approach. Plate-shaped particles can lie flat, needles can align, and crystallites in stretched polymers can acquire preferred orientation. Some peaks then strengthen while others weaken without a proportional change in total crystalline material. Films, fibers and bulk specimens may require reflection, transmission or grazing-incidence geometries. Rings that become arcs, or strongly uneven intensity around a ring, directly reveal directional organization. Preserving that information can be more useful than reducing every measurement to one curve and overlooking its orientation dependence.

Preparation also changes peak positions and background. In reflection geometry, a specimen surface displaced from the intended focusing position can shift angles. Packing, particle size and absorption affect the sampled scattering volume. Holders, solvents and air can contribute background. Drying or grinding a hydrated biomaterial may itself alter structure, so preparation should retain the state relevant to the question. An empty holder, a known reference and repeated mounting test different parts of this chain. Together, these comparisons help establish whether two patterns differ because of internal material structure or because of acquisition geometry.

Angular range, step size and counting time serve different purposes. A narrow range may miss a reflection needed to distinguish phases. Coarse steps may inadequately describe a narrow peak. Short counting times make weak features harder to separate from random variation. Increasing counts reduces relative statistical noise but does not correct specimen displacement or improve instrumental angular resolution. Choose a range from the expected structural question, then use a preliminary scan and reference measurements to inspect width and background. This directs measurement effort toward information that actually distinguishes the competing explanations.

## One position gives a spacing; a set of reflections constrains a structure

For a new pattern, identify reproducible peaks, record their positions and widths, and calculate a set of spacings. Combine these with plausible elements, processing history and known structures to find candidate phases that explain several reflections. Open crystallographic structure databases can supply structural files for calculated reference patterns, and public diffraction software connects structural models with measured profiles. A reference pattern should retain its wavelength and calculation conditions. The same spacing appears at different 2θ values under different wavelengths, so comparing unmatched angular lists creates avoidable confusion.

Agreement with one candidate reflection is a beginning. Different crystals can share similar spacings, and mixed phases can overlap. Stronger identification comes from the positions of multiple peaks, reflections that should appear but are absent, intensity tendencies and composition. A bone-like mineral deposit can be examined by combining ordered-structure information from XRD with elemental analysis and chemical-group information from infrared spectroscopy. A filled polymer requires consideration of both the matrix's broad scattering and the inorganic reflections. Each method supplies a different constraint, gradually narrowing the structural explanation.

$$
q=\frac{4\pi\sin\theta}{\lambda},\qquad q_{n=1}=\frac{2\pi}{d}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | Scattering-vector magnitude, nm⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | Half the scattering angle 2θ. |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | X-ray wavelength, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | Plane spacing associated with a first-order Bragg reflection, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Bragg reflection order; dimensionless integer. |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | Pi; dimensionless. |

Substituting the first-order Bragg relation into the q definition gives q=2π/d. A spacing of 0.25 nm gives q≈25.133 nm⁻¹. The q coordinate enables comparison of the same periodicity measured with different wavelengths.

The scattering-vector magnitude q offers another horizontal coordinate, combining wavelength and angle into a quantity connected directly to spatial scale. For a first-order Bragg reflection, q equals 2π divided by spacing: larger spacings correspond to smaller q. This makes comparisons across wavelengths easier and introduces the language used in small-angle scattering. It is not automatically the inverse of particle diameter. A length interpretation requires knowing which periodicity or model produced the feature. At this stage, q is best understood as a scale for the spatial frequency represented by a scattering measurement.

A peak position reported to many decimal places does not establish comparable accuracy in spacing. Angular zero, specimen displacement, wavelength distribution, overlap and background influence the estimated center. When several peaks move, test whether their changes agree with a common lattice change or resemble a geometrical error. For temperature- or humidity-responsive materials, retain acquisition geometry, record equilibration time and check instrumental stability with a suitable reference. The resulting shifts then have an interpretable physical context rather than being summarized only by arrows drawn between curves.

## Finite order, strain and the instrument all contribute to peak width

An infinitely extended, perfectly ordered array concentrates constructive scattering into sharply selected directions. A real ordered region contains a finite number of repeats, broadening the range of angles that gives substantial enhancement. The first interference calculation changes only the number of coherently combined repeats: ten produce a wider peak, while eighty produce a narrower one. A choir that maintains a shared rhythm over a longer interval provides an intuition for stricter phase selection, although the calculation itself comes from adding scattered waves. The key length concerns the extent of coherent periodic organization.

![Teaching calculations. A varies coherently combined repeat count to connect finite order with width. B combines pure-size Gaussian profiles with known instrument broadening and compares corrected and uncorrected size estimates.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/a2b6201a4023ee40eae2246d.svg?v=a2b6201a4023)

Figure 2Teaching calculations. A varies coherently combined repeat count to connect finite order with width. B combines pure-size Gaussian profiles with known instrument broadening and compares corrected and uncorrected size estimates.

The Scherrer relation converts an appropriately isolated size-broadening contribution into a coherent diffraction length. This is not necessarily the outline dimension of an entire particle in a micrograph. A particle may contain several grains, and defects may interrupt periodic coherence within it. The shape factor depends on crystallite geometry, width definition and related choices. A value near 0.9 is a useful teaching approximation rather than a universal constant for all specimens. Specify the reflection, width measure and corrections before interpreting the resulting length. That definition makes comparison with microscopy more informative.

$$
D\approx\frac{K\lambda}{\beta_s\cos\theta},\qquad \beta_s=\sqrt{\beta_o^2-\beta_i^2}\quad\text{(Gaussian profiles)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | Coherent diffraction length estimated from size broadening, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/24733a44cf365eb5e1b92574.svg) | Dimensionless shape/width factor; 0.9 in this teaching example. |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | X-ray wavelength, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/adf8cfc447681bea28281828.svg) | Full width at half maximum on the 2θ axis assigned to specimen size, radians. |
| ![Formula](https://ml-biomat.com/static/agent-math/714bfb9affa05813acb8606a.svg) | Observed full width at half maximum on the 2θ axis, radians. |
| ![Formula](https://ml-biomat.com/static/agent-math/58e8ca623882ae98a67c5493.svg) | Instrumental Gaussian width under matched conditions, radians. |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | Half the peak position 2θ; use radians for the cosine. |

Quadrature subtraction applies to this Gaussian convolution, with specimen broadening assigned entirely to size. Observed width 0.303117° and instrument width 0.12° give specimen width 0.278352°; conversion to radians yields 30 nm. Direct use of observed width gives approximately 27.55 nm.

Work through the example numerically. A spacing of 0.25 nm gives a center at 35.8919°. For a specified coherent length of 30 nm, the size contribution has a full width at half maximum of approximately 0.27835°. Combining it with an instrumental Gaussian width of 0.12° gives an observed width of about 0.30312°. Direct substitution of that larger width returns approximately 27.55 nm. Removing the known instrument contribution in quadrature and converting the remaining width to radians recovers 30 nm. These intermediate values check both units and definitions while showing why a reference measurement belongs inside the calculation.

The instrument also broadens a line through optics, wavelength distribution and detector response. Measuring an appropriate reference establishes the instrumental profile under relevant conditions, allowing sample and instrument contributions to be separated. The teaching example adds Gaussian widths in quadrature because Gaussian convolution has that property. Lorentzian or mixed profiles require different treatment. When observed width is already close to instrumental width, subtracting the two leaves a small difference sensitive to measurement error, making the inferred size unstable. The accompanying plot shows how using observed width directly underestimates the specified coherent length.

Microstrain can broaden peaks as well. Slightly different spacings in different regions resemble a collection of narrowly shifted contributions whose sum is wider. Stacking faults, anisotropic domain dimensions and overlapping phases produce additional complexity. Several reflections and their angular dependence can help distinguish size and strain, provided the model suits the material and the data are adequate. One broad feature offers limited independent information. Converting it immediately into a precise-looking particle diameter can conceal physical contributions that have not yet been separated.

Unit checks prevent a particularly large numerical error. Pattern axes commonly use degrees, while the Scherrer width must be expressed in radians. The width is measured on the 2θ axis. Substituting 0.3 for a width of 0.3° without conversion creates a discrepancy of approximately a factor of 57. Meanwhile θ remains half the peak position, not half the peak width. Mark the center, half-height level and two half-height crossings on a sketch before converting units. This small geometrical exercise is often more effective than memorizing variable names alone.

## Peak area, broad scattering and background need a joint interpretation

A semicrystalline polymer pattern commonly contains narrower reflections together with broad scattering. Narrow components relate to ordered regions, broad contributions contain information from disordered structure, and instrument or specimen environment adds background. Under a defined angular range and decomposition model, one can estimate the fraction of sample scattering assigned to crystalline peaks. Although the final step is an integration, the preceding decisions determine what is treated as sample signal, how broad scattering is represented and how overlap is handled. A consistently defined index supports comparisons within that definition while remaining distinct from quantities such as crystalline mass fraction.

$$
X_A=\frac{A_c}{A_c+A_a}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/61f0812c0240edef2566362b.svg) | Crystalline peak-area index for the specified model and scan range; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/0e856b4c890d783d82136df7.svg) | Total integrated intensity assigned to crystalline peaks after background removal, common intensity×angle units. |
| ![Formula](https://ml-biomat.com/static/agent-math/97cabe215ef9775c31d616d7.svg) | Integrated intensity assigned to the broad component over the same range, in the same units as Ac. |

50000/(50000+35000)=0.588235, or 58.82%. On an equally spaced angular grid, the common step cancels in the ratio of sums. Background, decomposition and orientation define this index; conversion to mass crystallinity requires material-appropriate calibration and scattering models.

The teaching pattern contains three crystalline components, one broad component and a constant background. The crystalline coefficients sum to 50,000 and the broad coefficient is 35,000, giving a model peak-area index of 50,000/85,000, or approximately 58.82%. Each profile is normalized on the same angular grid, so its coefficient represents total counts contributed within the scan range. The program jointly fits the components, then tests how a changed background assumption alters the index. Known shapes make the exercise checkable. Real polymer analyses require a physically suitable treatment of broad scattering, texture, absorption and other material-specific features.

![Constructed teaching pattern with three narrow peaks and one broad component, without assigning a real phase. A compares observations and fit; B decomposes the model; C shows standardized residuals; D refits area indices under changed background assumptions while holding observations fixed.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/853914f734635fa714fa1c7b.svg?v=853914f73463)

Figure 3Constructed teaching pattern with three narrow peaks and one broad component, without assigning a real phase. A compares observations and fit; B decomposes the model; C shows standardized residuals; D refits area indices under changed background assumptions while holding observations fixed.

Subtracting an overly high background before fitting can suppress the broad component and increase the fraction assigned to crystalline peaks. An underestimated background can instead assign excess intensity to the broad contribution. The figure holds observations fixed and changes only the assumed constant background to expose this redistribution. A more flexible background is not automatically better, because it may absorb genuine broad scattering. Use empty-holder measurements, neighboring angular regions and a physical model to establish the background form, then inspect stability across reasonable choices. This makes the effect of analysis choices comparable with the effect attributed to material treatment.

Height and area are different quantities. If a constructed peak retains the same total contribution while becoming broader, its maximum decreases without an area change. A shorter peak can therefore reflect redistribution over angle rather than less ordered material. Conversely, preferred orientation can produce a tall reflection without increasing the specimen's total crystalline mass fraction. Compare curves using consistent acquisition and normalization, then consider position, area, width and two-dimensional orientation together. One visual feature should not substitute for several distinct physical questions.

Residuals are the observed profile minus the modeled profile. A sustained positive or negative residual over an angular interval may indicate an unsuitable background, a missing reflection, mismatched width or an additional phase. Even when a global fit statistic looks small, local systematic structure deserves inspection. Whole-pattern refinement uses structural and instrumental models to explain many observations simultaneously. Its parameters should have physical meanings compatible with the angular range and data quality. Increasing model complexity as the question and evidence require it makes each improvement easier to understand than freeing every parameter at the outset.

## Observe lattice expansion and size change separately

The interactive experiment follows one teaching reflection with an initial spacing of 0.25 nm. Controls change relative spacing, coherent-domain length and instrumental Gaussian width. Intrinsic and instrument-broadened peaks are shown with equal area normalization. Increasing spacing shifts the center; reducing coherent length broadens the peak; increasing instrument width also broadens it. The first change concerns periodicity, while the latter two may look similar and require calibration to distinguish. Numerical readouts compare a size estimated directly from observed width with one obtained after removing the known Gaussian instrument contribution.

## One peak: separate position from broadening

Wavelength 0.15406 nm, initial spacing 0.25 nm, shape factor 0.9. Green: size-only peak; blue: instrument-broadened peak. Both have equal area.

[Figure: Diffraction peak position and width](https://ml-biomat.com/tutorials/experimental-methods/i06/en/#I06-plot)

Begin with a small instrument width and vary coherent length to establish the size–width relationship. Then hold the specimen fixed and increase instrumental width, observing the uncorrected estimate drift. Finally change spacing, check the direction of the peak shift and relate the calculated θ to the 2θ axis. Every contribution in this Gaussian teaching model has a stated origin. The same practice of changing and checking one contribution at a time can guide experimental analysis before adding the strain, orientation or multiphase models required by a particular material.

## Build an interpretable structural argument from the whole pattern

For a polymer cooled at three different rates, keep thickness, measurement geometry and angular range comparable, then examine positions, widths, orientation and area decomposition separately. Slower cooling can change how ordered regions develop, but the actual trend depends on the polymer and conditions. Connect these structural measurements with thermal, mechanical or optical measurements on corresponding specimens to test which change tracks performance. Use independently prepared specimens for each condition, and distinguish their variation from repeated mounting of the same specimen. This separates preparation variability from measurement reproducibility and gives the comparison an appropriate experimental scale.

Whole-pattern analysis of a mixture also needs attention to parameter compensation. Phase abundance, preferred orientation, background and peak widths can alter intensity over overlapping angular regions. An optimizer may use one parameter to compensate for an inadequacy elsewhere in the model. Begin from known composition and a manageable profile description, add physically motivated freedom in stages, and inspect whether values remain stable and plausible. A small fitting error becomes useful when it accompanies a coherent structure, suitable reference information and understandable residuals. It is the combined argument that answers the question, rather than the fit statistic alone.

Peak normalization changes visual emphasis and should match the intended comparison. Scaling every scan to its tallest peak is convenient for comparing positions, but removes the absolute height difference at that peak. Scaling to total area emphasizes relative contributions within the selected range, while exposure normalization retains a different relationship to counts. If specimen amount, absorption or illuminated volume changes, counts per second alone do not establish equal scattering per unit mass. Retain the original counts and document the transformation used for the plotted version. Then a reader can distinguish a change in material from a change in how curves were displayed.

The fixed-seed run estimates the model area index as approximately 59.05%, compared with the specified 58.82%; fitting the noiseless expectation recovers 58.82%. This difference illustrates random counting variation under a correct, known profile model. In a real specimen, uncertain background and component shapes can introduce additional changes that a single statistical error bar does not capture. Repeating the fit over justified ranges or alternative physically plausible descriptions helps identify those contributions. The goal is to understand which assumptions control the result and design the next measurement to distinguish them.

A useful next measurement is often modest: extend the angular range to include an otherwise ambiguous reflection, repeat a mounting to test a suspected position shift, or collect a two-dimensional pattern to inspect orientation. Each addresses a specific unresolved cause. Choosing among them follows from reading the current pattern as evidence about both structure and measurement, rather than treating every unexplained feature as a reason to add another fitted peak.

The complete program generates a Bragg-geometry schematic, finite-repeat interference curves, and a noisy teaching pattern with joint fitting and background-sensitivity analysis. Its table preserves expected counts, constructed observations, fitted counts and standardized residuals at every angle. A numerical summary records positions, widths, lengths and area indices. Change the spacing between peaks to examine growing overlap, or alter the broad component away from the fitting assumption and inspect whether residuals acquire systematic structure. This teaches calculation together with the more important habit of asking what an unexplained feature says about the model.

### Complete Python: positions, broadening and area decomposition

Generate specified physical geometry and fixed-seed teaching counts, preserving angle-level tables, fit residuals and numerical summaries.

```
"""XRD teaching model: Bragg geometry, coherent domains and profile fitting.

Patterns are constructed, with no claimed identity as a measured material.
Peak areas use normalized discrete basis functions over this scan range.
"""
from pathlib import Path
import argparse,json,csv
import numpy as np
from scipy.optimize import nnls
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

def peak_properties(d=.25,D=30.,instrument=.12,wavelength=.15406):
    theta=np.arcsin(wavelength/(2*d));center=np.rad2deg(2*theta)
    beta=np.rad2deg(.9*wavelength/(D*np.cos(theta)))
    observed=np.hypot(beta,instrument)
    naive=.9*wavelength/(np.deg2rad(observed)*np.cos(theta))
    return center,beta,observed,naive

def main(output,language):
    output.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'svg.fonttype':'none','font.size':11,'axes.titleweight':'bold','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','text.color':'#243b45','axes.labelcolor':'#243b45'})
    tr=lambda a,b:a if language=='zh' else b
    green,blue,red,gray='#168477','#3474a8','#bd624b','#788b90'
    def save(fig,name):
        fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');fig.savefig(output/f'{name}-{language}.png',dpi=140,bbox_inches='tight');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,5.5),layout='constrained')
    ax=axes[0];ax.set(xlim=(-5,5),ylim=(-3.8,4.5));ax.set_aspect('equal');ax.axis('off');ax.set_title(tr('A  布拉格几何：比较两条路程','A  Bragg geometry: compare two paths'))
    for y in [0,-1.6,-3.2]:
        ax.plot([-4.8,4.8],[y,y],color=gray,lw=1)
        ax.scatter(np.linspace(-4.5,4.5,10),np.full(10,y),s=23,color=gray)
    for y,col in [(0,green),(-1.6,blue)]:
        ax.annotate('',(0,y),(-4,y+2.8),arrowprops={'arrowstyle':'->','color':col,'lw':2});ax.annotate('',(4,y+2.8),(0,y),arrowprops={'arrowstyle':'->','color':col,'lw':2})
    ax.annotate('',(4.5,0),(4.5,-1.6),arrowprops={'arrowstyle':'<->','color':red});ax.text(4.65,-.8,'d',color=red);ax.text(-2.4,.25,'θ',color=green);ax.text(1.9,.25,'θ',color=green)
    ax.text(0,3.9,tr('额外路程：2d sinθ = nλ','Extra path: 2d sinθ = nλ'),ha='center',fontsize=13)
    ax.text(0,-3.75,tr('原子面为几何构造；电子散射形成干涉','Planes are a geometrical construction; scattering interferes'),ha='center',fontsize=9)
    ax=axes[1];ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off');ax.set_title(tr('B  1912—1913：角度变成结构信息','B  1912–1913: angle becomes structure'))
    ax.plot([1,5,9],[6,2,6],color=blue,lw=3);ax.scatter([5],[2],s=400,marker='D',color=green);ax.text(.5,6.6,tr('X射线','X-rays'));ax.text(4.3,1,tr('晶体','Crystal'));ax.text(8,6.6,tr('探测器','Detector'))
    ax.add_patch(Arc((5,2),5,5,theta1=45,theta2=135,color=red,lw=1.5));ax.text(5,5,tr('扫描散射方向','Scan scattering direction'),ha='center')
    ax.text(5,.1,tr('晶体周期 → 峰位置；内部排列 → 强度','Crystal periodicity → positions; arrangement → intensities'),ha='center',fontsize=10)
    save(fig,'bragg')
    fig,axes=plt.subplots(1,2,figsize=(11,4.5),layout='constrained')
    phase=np.linspace(-.7,.7,2001)
    for N,col in [(10,green),(30,red),(80,blue)]:
        amplitude=np.sum(np.exp(1j*np.outer(phase,np.arange(N))),axis=1)/N
        axes[0].plot(phase,np.abs(amplitude)**2,color=col,label=f'N={N}',lw=2)
    axes[0].set(xlabel=tr('相邻周期相位偏离 / rad','Phase offset per repeat / rad'),ylabel=tr('归一化干涉强度','Normalized interference intensity'),title=tr('A  有序周期越多，峰越窄','A  More coherent repeats, narrower peaks'));axes[0].legend(frameon=False)
    sizes=np.linspace(5,120,200);widths=np.array([peak_properties(D=d)[2] for d in sizes]);naive=np.array([peak_properties(D=d)[3] for d in sizes]);axes[1].plot(sizes,naive,color=red,lw=2,label=tr('直接用观测宽度','Using observed width'));axes[1].plot(sizes,sizes,color=green,ls='--',label=tr('扣除已知仪器高斯宽度','Known Gaussian instrument correction'));axes[1].set(xlabel=tr('设定相干尺寸 / nm','Specified coherent size / nm'),ylabel=tr('估计尺寸 / nm','Estimated size / nm'),title=tr('B  仪器展宽需要标定','B  Instrument broadening needs calibration'));axes[1].legend(frameon=False,fontsize=9)
    save(fig,'coherence')
    angle=np.linspace(10,70,3001);ds=np.array([.4,.25,.2]);centers=np.array([peak_properties(d=d)[0] for d in ds]);widths=np.array([peak_properties(d=d)[2] for d in ds])
    def g(center,width):
        v=np.exp(-4*np.log(2)*((angle-center)/width)**2);return v/v.sum()
    crystalline=np.column_stack([g(c,w) for c,w in zip(centers,widths)]);amorphous=g(23,9);design=np.column_stack([crystalline,amorphous,np.ones(len(angle))]);truth=np.array([16000.,22000.,12000.,35000.,12.]);expected=design@truth;rng=np.random.default_rng(1706);observed=rng.poisson(expected);coef,_=nnls(design,observed);fit=design@coef;residual=(observed-fit)/np.sqrt(np.maximum(fit,1))
    fig,axes=plt.subplots(2,2,figsize=(11,8),layout='constrained')
    axes[0,0].plot(angle,observed,color=gray,lw=.7,label=tr('构造观测','Constructed observation'));axes[0,0].plot(angle,fit,color=green,lw=1.5,label=tr('已知峰形联合拟合','Joint fit with known shapes'));axes[0,0].set(xlabel='2θ / °',ylabel=tr('计数 / 步','Counts / step'),title=tr('A  完整扫描与拟合','A  Full scan and profile fit'));axes[0,0].legend(frameon=False,fontsize=9)
    axes[0,1].plot(angle,crystalline@coef[:3],color=blue,label=tr('晶体峰贡献','Crystalline peaks'));axes[0,1].plot(angle,amorphous*coef[3],color=red,label=tr('宽散射贡献','Broad contribution'));axes[0,1].axhline(coef[4],color=gray,label=tr('常数背景','Constant background'));axes[0,1].set(xlabel='2θ / °',ylabel=tr('计数 / 步','Counts / step'),title=tr('B  区分峰、宽散射与背景','B  Peaks, broad scattering and background'));axes[0,1].legend(frameon=False,fontsize=9)
    axes[1,0].plot(angle,residual,color=green,lw=.6);axes[1,0].axhline(0,color=gray);axes[1,0].set(xlabel='2θ / °',ylabel=tr('标准化残差','Standardized residual'),title=tr('C  检查未解释的角度结构','C  Inspect unexplained angular structure'))
    choices=np.linspace(8,16,80);indices=[]
    for bg in choices:
        a,_=nnls(design[:,:4],observed-bg);indices.append(a[:3].sum()/a[:4].sum())
    axes[1,1].plot(choices,np.array(indices)*100,color=red,lw=2);axes[1,1].axvline(12,color=gray,ls='--');axes[1,1].set(xlabel=tr('固定背景 / 计数每步','Fixed background / counts per step'),ylabel=tr('模型峰面积指数 / %','Model peak-area index / %'),title=tr('D  背景选择改变面积分解','D  Background changes the area decomposition'))
    save(fig,'profile')
    with (output/'data.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['two_theta_deg','expected_counts','constructed_counts','fitted_counts','standardized_residual']);w.writerows(zip(angle,expected,observed,fit,residual))
    center,beta,bobs,naive=peak_properties();exact,_=nnls(design,expected)
    summary={'center_d025_deg':center,'size_fwhm_D30_deg':beta,'observed_fwhm_deg':bobs,'uncorrected_size_nm':naive,'corrected_size_nm':.9*.15406/(np.deg2rad(np.sqrt(bobs*bobs-.12**2))*np.cos(np.deg2rad(center/2))),'true_area_index':50000/85000,'fitted_area_index':float(coef[:3].sum()/coef[:4].sum()),'noiseless_area_index':float(exact[:3].sum()/exact[:4].sum()),'q_d025_invnm':2*np.pi/.25,'peak_positions_deg':centers.tolist(),'data_origin':'Constructed teaching pattern, not an experimental phase or crystallinity measurement.'}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

Return to the calcium–phosphate deposit. An organized analysis connects composition, several diffraction reflections, specimen state and appropriate chemical-structure measurements. For a polymer, connect thermal history, orientation, line-shape changes and mechanical behavior within one investigation. XRD makes atomic-scale periodicity observable through angles and intensities. Understanding how those signals form moves the interpretation beyond counting peaks toward identifying which structural changes can explain the material's behavior.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/I06.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [IUCr — Scope, potential and applications of X-ray analysis](https://www.iucr.org/education/pamphlets/2)

   Introduce structure measurement through scattering and imaging analogies.

   Public educational reference; figures original.
2. [IUCr — Calculation of structure factors](https://www.iucr.org/education/pamphlets/3)

   Phase addition, atomic arrangement and reflection intensity.

   Public educational reference; figures original.
3. [Nobel Foundation — 1915 presentation speech](https://www.nobelprize.org/prizes/physics/1915/ceremony-speech/)

   Bragg plane interpretation and early structure analysis.

   Historical primary record; no historical image reproduced.
4. [NIST — SRM 1979 diffraction line-profile standard](https://www.nist.gov/publications/certification-standard-reference-material-1979-powder-diffraction-line-profile-standard)

   Coherent size, microstrain, stacking faults and profile calibration.

   Government research reference.
5. [NIST SRM 1979 certification paper](https://nvlpubs.nist.gov/nistpubs/jres/125/jres.125.020.pdf)

   Further reading on standard-material profile and background analysis.

   Government research publication; figures not reused.
