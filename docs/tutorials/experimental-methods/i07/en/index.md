# SAXS: Seeing nanoscale structure in an ensemble

Source: https://ml-biomat.com/tutorials/experimental-methods/i07/en/
Language: en

Follow a clear protein solution into scattering profiles, radius of gyration and fitting-window decisions.

## A clear protein solution can still hide a structural change

A vial of protein solution may look as clear as water. Clarity tells us that little visible light is scattered toward our eyes; it does not tell us whether the proteins remain compact, extend into more open conformations, form pairs, or develop a small population of much larger aggregates. These differences matter when storing a protein medicine, changing an enzyme's solution conditions, or preparing polymer micelles. Small-angle X-ray scattering, usually abbreviated SAXS, addresses such questions by sending X-rays through a sample and measuring weak scattering close to the original beam direction. “Small angle” describes the observation geometry. Compared with the larger-angle features associated with atomic spacings, scattering near the direct beam often reports on larger structural scales.

Imagine observing a group of small lamps from a distance. Their arrangement affects the distribution of light that reaches an observer. X-ray scattering also combines contributions from many locations, with the additional requirement that waves have phases: their peaks and troughs can reinforce or cancel. Electrons in both the protein and its surrounding liquid scatter the beam. The useful contrast is therefore a difference between the object and the solution around it. SAXS can describe overall molecular dimensions, shape and association in solution, as well as density variations in gels and the organization of nanoparticles or micelles. The signal averages over many objects in the illuminated volume. It is a statistical structural measurement rather than a sharply outlined photograph of one molecule.

This chapter follows a public scattering profile for lysozyme, a protein that cuts particular chemical connections in bacterial cell walls and is also present in egg white. We will read the measured curve, understand why its initial decline contains a size measure, and change the fitting interval to see why one dataset can produce somewhat different numerical estimates. The aim is to connect each step: what enters the sample cell, what the detector records, how background processing produces a curve, and which features support a particular structural interpretation. A familiar transparent liquid becomes a useful setting for learning how a measurement reveals otherwise invisible organization.

## From the hardening of an alloy to structure in a liquid

The development of small-angle scattering was closely connected with a practical materials question. Some aluminium–copper alloys become harder during ageing even when ordinary microscopy reveals little obvious change. In his personal reminiscences, Guinier described being asked in 1938 to examine ageing aluminium–copper alloys while he was studying low-angle scattering. Unusual scattering helped connect a change in mechanical properties with very fine internal organization. The useful shift in thinking was to stop requiring every structural change to appear as an easily visible particle. Small differences in composition or electron density could alter wave interference and leave a measurable signal. Modern studies of proteins and polymers use the same broad idea to examine internal organization that affects function.

The apparatus illustration translates that idea into a beam path. Slits or other optical elements define a sufficiently narrow incident beam. After crossing a sample held in a cell or capillary, most radiation continues forward while a smaller fraction is deflected. A relatively long sample-to-detector distance helps separate small angular differences. A beamstop blocks the intense direct beam so that nearby weak scattering can be recorded. This necessary component also means that the very smallest scattering angles are normally inaccessible. The “zero-angle intensity” encountered later is usually an extrapolation from a model, not simply the intensity of a central detector pixel. Understanding the physical obstruction makes the extrapolation easier to interpret.

Scattering experiments commonly replace angle with the scattering-vector magnitude q. For an introductory understanding, treat q as a coordinate that combines angle and wavelength. A shorter wavelength gives a larger q at the same deflection angle, and a direction closer to the direct beam gives a smaller q. Small q is sensitive to relationships over larger distances; larger q progressively adds finer structural information. The tempting rule that every q corresponds to one separate size is only a scale intuition. A well-defined periodic structure can produce a peak that converts into a repeat distance, whereas a smooth protein curve combines contributions from many internal distances.

$$
q=\frac{4\pi\sin\theta}{\lambda}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | Scattering-vector magnitude, nm⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | Half the total deflection angle 2θ; numerical trigonometry uses radians. |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | X-ray wavelength, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | Pi; dimensionless. |

At wavelength 0.15 nm and total deflection 1°, the half-angle 0.5° gives q=0.731073 nm⁻¹. This combines wavelength and angle into a common scattering coordinate.

For a wavelength of approximately 0.15 nm and a total deflection angle of 1°, the half-angle in the formula is 0.5°, giving q about 0.731 nm⁻¹. Using the full degree in the half-angle position would almost double the result and systematically change inferred lengths. Units deserve similar attention: 1 nm equals 10 Å, so 0.1 Å⁻¹ equals 1 nm⁻¹. Confirming units when reading a file is more reliable than deciding afterward that a fitted size looks plausible. The second panel of the illustration also introduces an important distinction: two arrangements can have the same mean-square distance from their centres without having the same shape or internal organization.

![Original concept illustration. A connects the 1930s question of fine internal heterogeneity to modern SAXS geometry; angles exaggerated, direct beam stopped by the beamstop. B uses schematic side views of a uniform solid sphere and separated elements with the same mean-square radius to show that Rg does not specify a unique structure.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/ba56b9b5c23a048ca930f34c.svg?v=ba56b9b5c23a)

Figure 1Original concept illustration. A connects the 1930s question of fine internal heterogeneity to modern SAXS geometry; angles exaggerated, direct beam stopped by the beamstop. B uses schematic side views of a uniform solid sphere and separated elements with the same mean-square radius to show that Rg does not specify a unique structure.

## Measure the liquid and container before interpreting the protein

A solution exposure includes contributions from protein, buffer, the sample container and other backgrounds. Buffer is not another word for pure water. It may contain salts, pH-controlling compounds, glycerol or reducing agents, all of which can change electron density and protein interactions. A useful reference closely matches the sample liquid while lacking the target protein, for example a suitable dialysate or appropriately selected buffer frames from a size-exclusion chromatography experiment. Preparing another liquid with an approximately matching recipe can leave small composition differences that become conspicuous after subtraction, particularly at high q where the protein contribution is weak.

Exposure duration, incident-beam intensity, transmission and detector response must also be handled consistently. After bringing the measurements onto a common scale, a suitably scaled buffer curve is subtracted from the solution curve. The resulting difference can then be interpreted as scattering associated with the object relative to its surroundings. Subtraction does not remove random error. Both measurements fluctuate, and both fluctuations enter the difference. When their errors are independent, the variances add; scaling the background also scales its uncertainty. This is why a small protein signal can retain a substantial error bar even after careful background processing.

$$
I_p=I_s-aI_b,\qquad \sigma_p^2=\sigma_s^2+a^2\sigma_b^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/44d9fad31d63f36e8d73e778.svg) | Processed object-relative-to-solvent intensity, common intensity units. |
| ![Formula](https://ml-biomat.com/static/agent-math/d3bc1f47b81d56c2b85373af.svg) | Normalized solution intensity on the same scale as background. |
| ![Formula](https://ml-biomat.com/static/agent-math/c826a1b7cf2ddf4418889fa6.svg) | Normalized matched-buffer intensity. |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Specified background scale factor; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/b40cd07d2c7b2ebebd2a46c9.svg) | Standard errors of difference, solution and background, each in intensity units. |

For independent measurements and a specified exact scale factor, variances add. Subtracting 1000±10 from 1050±10 with a=1 gives 50±14.142, where ± denotes one standard error. An uncertain scale factor requires its additional propagated contribution.

Consider one q value with normalized solution intensity 1050 and standard error 10, and matched buffer intensity 1000 with standard error 10. With a scaling factor of one, subtraction gives 50 with standard error approximately 14.14. The uncertainty is neither zero nor the difference between the two errors. The signal-to-error ratio is only about 3.54. If the true difference were smaller, random fluctuations could readily produce a negative value. Such a value describes the difference between measurements, not a negative number of detected photons. Keep these values in the data table and inspect them on a linear intensity axis instead of replacing them with tiny positive numbers to make a logarithmic plot look tidy.

Preparation also concerns concentration, uniformity and time. A concentration series tests whether profiles divided by concentration overlap. Systematic low-q changes can reveal attraction or repulsion between particles rather than a change in each particle alone. Dividing a long exposure into short frames helps detect aggregation or structural changes during irradiation. Centrifugation and filtration can remove some dust or large particles, but they may also alter the population under study. Decide whether the question concerns the whole dispersion or its soluble fraction. Temperature, buffer composition, concentration and exposure history belong to the measurement definition because they determine what is actually present in the illuminated volume.

## How the beginning of a curve gives a measure of molecular extent

At sufficiently small q, phase differences among contributions from within a particle remain small. The initial intensity decline can then be approximated by a simple exponential, the Guinier approximation. Taking the natural logarithm turns that exponential into a straight line when plotted against q squared. Its slope is proportional to the negative square of the radius of gyration. A logarithm changes multiplicative variation into additive spacing; you do not need to calculate it by hand to understand the plot. If the approximation describes the selected region, points approach a straight line, and a steeper decline corresponds to a more spatially extended scattering distribution.

$$
I(q)\simeq I(0)e^{-q^2R_g^2/3},\qquad \ln I(q)=b+mq^2,\quad R_g=\sqrt{-3m}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | Scattering-vector magnitude, nm⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/a9c085d6657ea9c3c169083b.svg) | Intensity at q and model-extrapolated zero-angle intensity, common intensity units. |
| ![Formula](https://ml-biomat.com/static/agent-math/742acc50d5d386b6c8461bed.svg) | Radius of gyration of the scattering-contrast distribution, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Numerical log-intensity intercept ln I(0), with intensity expressed in specified units. |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Slope of log intensity against q², nm². |

At sufficiently small q, the initial decline primarily reflects a mean-square extent. Weighted fitting over 0.087–0.8 nm⁻¹ gives slope −0.588695 nm² and Rg=1.328942 nm. Logarithmic fitting uses the first-order relative-error approximation σI/I.

The name radius of gyration, Rg, can suggest a ball rotating around its centre. Here it describes how scattering contrast is distributed around a centre. For an object with uniform internal contrast, divide it into many small pieces, square each piece's distance from the centre, average those squared distances and take the square root. Distant pieces have a larger effect because their distances are squared. For a uniform solid sphere, Rg is approximately 0.775 times its geometrical radius. A thin rod, flexible chain and sphere can have the same Rg while differing greatly in maximum dimension and outline. Calling every Rg a “particle radius” would discard that distinction.

$$
R_g^2=\frac{\sum_j w_j r_j^2}{\sum_j w_j},\qquad R_{g,\mathrm{sphere}}=\sqrt{\frac35}\,R
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/742acc50d5d386b6c8461bed.svg) | Radius of gyration for the same-sign contrast object considered here, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | Index of a scattering element; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/f6264b954f8fef8d9872def7.svg) | Scattering weight of element j relative to solvent, common units; same sign for the uniform object here. |
| ![Formula](https://ml-biomat.com/static/agent-math/ac93bfc1786051ffd5b120d4.svg) | Distance of element j from the contrast-weighted centre, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | Geometrical radius of a uniform solid sphere, nm. |

Average squared distances before taking the square root. Volume integration for a uniform sphere gives 3R²/5; Rg=1.328942 nm corresponds to an equivalent uniform-sphere radius of 1.715656 nm. Further information describes the actual object shape.

For the archived lysozyme profile, this chapter selects q from 0.087 to 0.8 nm⁻¹ and performs a weighted linear fit to the logarithms of positive intensities. Weights use the approximate propagation of each reported intensity error into logarithmic coordinates: points with smaller relative errors contribute more strongly. The slope is approximately −0.5887 nm², yielding Rg about 1.329 nm and an extrapolated zero-angle intensity about 11.64 in the archived intensity units. Converting this Rg into the radius of a uniform equivalent sphere gives about 1.72 nm. That conversion supplies a geometrical comparison; it does not turn the molecular surface of lysozyme into an actual sphere.

The fitted result must be used to check the selected range. A commonly used starting criterion for compact particles is qRg below approximately 1.3, while extended or internally nonuniform particles may require a smaller upper bound. This is not a switch that guarantees a valid structural interpretation: an apparently straight low-q region can still contain effects of interactions or a small amount of larger material. Here the chosen upper q multiplied by fitted Rg is approximately 1.063. Residuals, window sensitivity and independent sample conditions provide additional checks. The earliest points remain visible even though they have large reported errors, preserving information about measurement quality near the beamstop.

## Read the real curve together with its experimental definition

The SASBDB entry SASDAC2 was deposited by Darja Ruskule and describes chicken lysozyme in sodium acetate buffer. The entry specifies 40 mmol/L buffer at pH 3.8. Its intensity file contains 2168 rows of q, intensity and uncertainty, with q in nm⁻¹. The curve has already undergone solution/background processing, so our analysis starts from a processed scattering profile rather than raw detector pixels. The database page reports a Guinier Rg of 1.5 nm; the explicitly defined simplified fit in this chapter gives approximately 1.329 nm. The difference is a useful analysis question. It is more informative to inspect the window and weighting than to adjust our procedure until it reproduces the displayed entry value.

The first data panel retains the full q-dependent trend, from relatively strong low-angle scattering to weak high-q intensity. The second transforms the low-q region into Guinier coordinates, distinguishing fitted points from neighbouring points retained for context. The third displays observed minus predicted intensity divided by the corresponding archived error. A sequence of residuals above or below zero indicates directional mismatch, even when an overall correlation coefficient is high. The fourth panel changes the upper fitting bound and plots the resulting Rg. The inferred size is therefore displayed beside the analysis choices that generated it, rather than detached from them as a single polished number.

The logarithmic error approximation is most suitable when relative errors are modest. Initial points whose errors are comparable to their intensities remain in the display but contribute very little to the weighted fit. The complete example also fits the same exponential directly in intensity coordinates, using the same points and archived uncertainties, to examine the effect of linearization. These are two analyses of one experiment, not independent measurements. Independently prepared samples, concentration changes, exposure comparisons and complementary methods provide different kinds of evidence. Keeping computational cross-checks separate from experimental replication makes agreement easier to evaluate.

![Measured data: Darja Ruskule, SASBDB SASDAC2, credited under the database unrestricted-reuse policy. A plots positive intensities over the full range; B retains points inside and outside the fit; C scales residuals by archived errors; D varies the upper fit bound. Large initial errors remain visible; this chapter specifies its own analysis window.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/38b5f99ddfb2affe696a444d.svg?v=38b5f99ddfb2)

Figure 2Measured data: Darja Ruskule, SASBDB SASDAC2, credited under the database unrestricted-reuse policy. A plots positive intensities over the full range; B retains points inside and outside the fit; C scales residuals by archived errors; D varies the upper fit bound. Large initial errors remain visible; this chapter specifies its own analysis window.

Suppose the research question is whether a treatment unfolds a protein. Measuring one profile before treatment and one afterward, then comparing two Rg values, leaves several explanations entangled. Matched buffers, concentration series and exposure frames establish a clearer comparison. Next examine Rg, the full profile and features associated with flexibility. An increase in Rg could reflect unfolding of individual molecules or association into larger objects, with very different biological implications. Size-exclusion chromatography coupled to SAXS follows scattering through an elution peak and can help separate populations, especially when combined with concentration and mass information. Experimental design supplies conditions that distinguish mechanisms; fitting describes the signals obtained under those conditions.

## Compactness, flexibility, association and background leave different clues

Multiplying each curve's horizontal coordinate by its own Rg and dividing intensity by its own zero-angle value removes an overall size and intensity scale. Multiplying the normalized intensity by the square of the normalized horizontal coordinate gives the dimensionless Kratky representation. This makes shape differences easier to see when they would otherwise be overshadowed by large low-angle intensities. The illustrated uniform sphere and ideal Gaussian chain have the same Rg but produce different curves. The sphere shows decay and oscillations, while the ideal chain approaches a different trend. Real proteins have more complicated shapes, flexibility and internal contrast. Read their curves together with sample state, accessible q range and error, rather than classifying every peaked profile as a properly folded protein.

Each element of this representation has a specific role. The horizontal quantity qRg is dimensionless and measures the observation scale relative to object size. The ratio I(q)/I(0) is also dimensionless and expresses the decline relative to zero angle. Their combination leaves neither a length unit nor an intensity unit on the vertical axis. The sphere and Gaussian-chain calculations illustrate consequences of geometry and are labelled separately from the measured lysozyme data. The adjacent high-q panel uses a linear axis so negative values and their errors remain visible. Together, the panels encourage simultaneous attention to structural patterns and measurement quality rather than replacing observations with an idealized curve.

![A compares teaching models of a uniform sphere and ideal Gaussian chain at the same Rg, using dimensionless axes. B shows actual high-q SASDAC2 observations on a linear scale, retaining negative values. The panels distinguish shape information from weak-signal quality.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/70368f19dac6614bc72972f1.svg?v=70368f19dac6)

Figure 3A compares teaching models of a uniform sphere and ideal Gaussian chain at the same Rg, using dimensionless axes. B shows actual high-q SASDAC2 observations on a linear scale, retaining negative values. The panels distinguish shape information from weak-signal quality.

A further analysis can estimate the pair-distance distribution P(r), which collects contrast-weighted contributions associated with distances between scattering elements. Its shape helps distinguish more compact from more extended objects. Because the measured q range is finite and noisy, deriving P(r) requires choices involving smoothing and maximum dimension. Think of reconstructing a room from a limited recording of echoes: the signal contains spatial information, but recording bandwidth and noise constrain what can be recovered. Examine whether the distribution approaches zero sensibly at its upper end, whether the fit is stable and how changes in the selected range affect the result. Adjusting parameters solely to force agreement with the Guinier Rg would turn a potentially independent consistency check into mutual tuning.

Polymer gels and micelles introduce additional possibilities, including correlation peaks, interfaces and contrast among components. A peak can describe average organization between objects rather than the diameter of each object. Changing salt concentration can alter particle dimensions, interparticle interactions, or both. A useful sequence of questions is therefore: which objects are present, how is material distributed inside them, and how are they arranged relative to one another? SAXS combines these contributions in one signal. Concentration series, contrast changes and complementary experiments help separate them. A specific physical question provides a reason to select a model instead of choosing whichever mathematical curve gives an attractive fit.

Why does a small population of large objects deserve attention? At sufficiently low q, contributions within one object add approximately in phase. Wave amplitudes add first, and intensity depends on the square of the resulting amplitude. For comparable composition, the low-angle contribution of one larger compact object can therefore grow faster than its volume. An aggregate containing many protein molecules may noticeably affect the curve even when aggregates represent a small fraction of the particle count. Keep the comparison denominator explicit: fixed particle number and fixed total protein mass are different conditions. Combining the same total amount of protein into larger objects also decreases their number. A complete interpretation must account for both changes, which is one reason concentration information and measurements across an elution peak are useful.

## Move the fitting window and watch the evidence change

The interactive experiment uses the low-q portion of the same public profile. The lower control sets where inclusion begins; the upper control sets where it ends. Filled blue points enter the fit, while other observations remain visible. Start with a fixed lower bound and increase the upper bound from 0.4 to 1.2 nm⁻¹. Watch the fitted line, Rg and the product of upper q with Rg. A broader interval contains more observations but may extend beyond the approximation. A narrower interval is closer to the small-angle limit but can make the slope more sensitive to noise or local variation. Neither “more points are always better” nor “a shorter straight line is always safer” resolves this tradeoff.

Next move the lower bound to inspect the influence of the earliest observations. Before removing inconvenient-looking points, consider their errors, geometry near the beamstop, background subtraction and possible sample changes. Each adjustment recalculates both the number of included points and the fitted parameters, making the effect of a seemingly minor exclusion visible. Observations outside the fitting window stay on the plot so the local fit can be read within the broader curve. A useful record saves the interval, units, uncertainty treatment and result together. A radius reported to many decimal places without those choices is less reproducible than a sensibly rounded estimate accompanied by its complete definition.

## Measured curve: move the Guinier fitting window

Data: Darja Ruskule, SASBDB SASDAC2. Blue points enter the weighted fit; open points retain context. Read Rg, point count and qmax Rg together as the window changes.

[Figure: Guinier fit of measured SAXS data](https://ml-biomat.com/tutorials/experimental-methods/i07/en/#I07-plot)

## Save the curve, its errors and the decisions that shaped the result

The complete Python example reads the bundled SASDAC2 file without a network connection. Four header lines precede 2168 numerical rows, followed by additional text, so the reader explicitly selects the data rows. The program preserves the original q, archived intensity and error columns and adds a fitting-selection flag and predicted intensity. Every fitted point can therefore be traced back to its table entry, while excluded and negative-intensity observations remain available. A separate window-sensitivity table records how Rg changes across upper bounds. This retains a sequence of analysis choices rather than only the one result closest to an expectation.

One numerical check uses a noiseless Guinier curve with prescribed Rg of 1.5 nm and zero-angle intensity of 10. The fitting function must recover those values. This tests the relationship among formula, units and implementation. The lysozyme profile serves a different purpose: it exposes the relation between an actual measured curve and a simplified analytical approximation. Keeping those purposes separate prevents successful parameter recovery from a constructed curve being mistaken for confirmation of a protein structure. Executed outputs include the linearized and direct-intensity fits, the low-q window analysis and the weak high-q signal, leaving a record that can be examined further.

A practical extension is to repeat this exact analysis on a second concentration after confirming that the solvent and intensity normalization match. Compare the profiles divided by concentration across their full common q range, then examine the low-q residuals and fitted dimensions. If the high-q curves overlap while their beginnings differ systematically, interparticle organization becomes a useful hypothesis to investigate. If the whole curve changes shape, consider changes within the objects as well as population mixtures. Save both the unscaled and concentration-normalized tables so that an apparent agreement can be traced to the operation that produced it. This exercise turns a numerical fit into a reproducible comparison between physically defined samples.

Return now to the transparent vial. SAXS turns a broad question about molecular change into several measurable ones: how does overall contrast distribution change, does the profile retain its shape, do larger objects contribute, and do concentration or exposure time affect the result? The same measurement language connects biomolecules in solution with nanoscale organization in materials. When the question instead concerns how pores connect throughout a three-dimensional scaffold, a method retaining spatial position becomes valuable. SAXS supplies ensemble structural information; X-ray micro-computed tomography reconstructs a volume from projections acquired at many directions. That transition introduces the next chapter.

### Complete Python: public lysozyme profile and Guinier windows

Read bundled measured data, perform two weighted fits, examine window sensitivity and model shapes, and export observations, selection flags and results.

```
"""Read the openly reusable SASBDB SASDAC2 profile and teach SAXS inference.

python main.py --output results --language en
Data credit: Darja Ruskule, SASBDB SASDAC2 (lysozyme in sodium acetate).
https://www.sasbdb.org/data/SASDAC2/ ; https://www.sasbdb.org/about/
The archive permits unrestricted reuse with attribution. The archived profile
is processed solution-minus-buffer intensity, not a raw detector exposure.
"""
from pathlib import Path
import argparse, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from scipy.optimize import curve_fit

def fit_guinier(q, intensity, sigma, lo=.087, hi=.8):
    m=(q>=lo)&(q<=hi)&(intensity>0)&(sigma>0)
    x=q[m]**2; y=np.log(intensity[m]); weights=intensity[m]/sigma[m]
    X=np.column_stack([np.ones(m.sum()),x])
    coeff=np.linalg.lstsq(X*weights[:,None],y*weights,rcond=None)[0]
    rg=np.sqrt(-3*coeff[1]) if coeff[1]<0 else np.nan
    return {'rg_nm':float(rg),'i0':float(np.exp(coeff[0])),
            'points':int(m.sum()),'slope_nm2':float(coeff[1]),
            'intercept':float(coeff[0]),'qmax_rg':float(hi*rg)},m

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args()
    out=args.output;out.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
    tr=lambda a,b:a if zh else b
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,
        'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#18344a',
        'text.color':'#18344a','axes.edgecolor':'#8295a2','svg.fonttype':'none',
        'savefig.facecolor':'#fbfcfc','figure.facecolor':'#fbfcfc'})
    blue='#186c94';green='#188777';orange='#d27839';gray='#a1abb2'
    def save(fig,name):
        fig.savefig(out/f'{name}-{args.language}.svg',bbox_inches='tight')
        fig.savefig(out/f'{name}-{args.language}.png',bbox_inches='tight',dpi=150);plt.close(fig)
    # The historical ATSAS file has four header lines, 2168 rows, then a footer.
    data=np.loadtxt(Path(__file__).parent/'data'/'SASDAC2.dat',skiprows=4,max_rows=2168)
    q,I,sigma=data.T
    result,mask=fit_guinier(q,I,sigma)
    nonlinear,_=curve_fit(lambda x,i0,rg:i0*np.exp(-x*x*rg*rg/3),q[mask],I[mask],
                         sigma=sigma[mask],p0=[12,1.4],absolute_sigma=True)
    windows=np.arange(.4,1.201,.025)
    sensitivity=np.array([fit_guinier(q,I,sigma,hi=h)[0]['rg_nm'] for h in windows])
    testq=np.linspace(.1,.8,80);testI=10*np.exp(-testq**2*1.5**2/3)
    reference,_=fit_guinier(testq,testI,np.ones(80)*.1)
    summary={**result,'nonlinear_rg_nm':float(nonlinear[1]),'nonlinear_i0':float(nonlinear[0]),
       'rows':len(q),'nonpositive_rows':int(np.sum(I<=0)),
       'noiseless_rg_nm':reference['rg_nm'],'noiseless_i0':reference['i0'],
       'q_for_1deg_invnm':float(4*np.pi*np.sin(np.deg2rad(.5))/.15),
       'equivalent_sphere_radius_nm':float(np.sqrt(5/3)*result['rg_nm']),
       'intensity_units':'archived intensity units; absolute calibration not asserted',
       'data_credit':'Darja Ruskule; SASBDB SASDAC2'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    predicted=result['i0']*np.exp(-q*q*result['rg_nm']**2/3)
    np.savetxt(out/'data.csv',np.column_stack([q,I,sigma,mask.astype(int),predicted]),delimiter=',',
         header='q_invnm,intensity,reported_sigma,guinier_selected,guinier_prediction',comments='')
    np.savetxt(out/'window_sensitivity.csv',np.column_stack([windows,sensitivity]),delimiter=',',
         header='qmax_invnm,rg_nm',comments='')
    # Original apparatus illustration; not a replica of a historical camera.
    fig,axs=plt.subplots(1,2,figsize=(12,4.5),gridspec_kw={'width_ratios':[1.55,1]})
    a=axs[0];a.set_xlim(0,10);a.set_ylim(-2,2);a.axis('off')
    a.plot([.3,8.45],[0,0],color=blue,lw=2)
    for x in [1.5,2.4]:
        a.add_patch(Rectangle((x,-.8),.16,.72,color=gray));a.add_patch(Rectangle((x,.08),.16,.72,color=gray))
    a.add_patch(Rectangle((3.8,-.6),.3,1.2,facecolor='#b5dddb',edgecolor=green))
    a.plot([8.8,8.8],[-1.8,1.8],color=blue,lw=5)
    a.add_patch(Rectangle((8.45,-.18),.3,.36,color='#394d5c'))
    for s in [-1,1]:a.plot([4,8.8],[0,s*1.3],color=orange,lw=2)
    for x,y,z,e in [(1.9,1.25,'准直狭缝','Collimation'),(4,-1.2,'溶液样品','Solution'),(8.4,-.7,'挡光片','Beamstop'),(8.7,1.6,'探测器','Detector')]:a.text(x,y,tr(z,e),ha='center',fontsize=10)
    a.annotate('',xy=(8.8,-1.65),xytext=(4,-1.65),arrowprops={'arrowstyle':'<->','color':blue})
    a.text(6.3,-1.95,tr('较长距离：分开很小的角度','Long distance resolves small angles'),ha='center',fontsize=10)
    a.set_title(tr('A  1930年代的小角问题 → 现代几何','A  A 1930s question → modern geometry'),loc='left')
    b=axs[1];b.set_xlim(-3,3);b.set_ylim(-2.1,2.1);b.set_aspect('equal');b.axis('off')
    b.add_patch(Circle((-1.5,0),1,facecolor='#b5dddb',edgecolor=green))
    theta=np.linspace(0,2*np.pi,10,endpoint=False)
    b.scatter(1.5+.775*np.cos(theta),.775*np.sin(theta),s=35,color=orange)
    b.plot([-1.5,-.5],[0,0],color=green);b.text(-1.5,-1.45,tr('均匀实心圆球','Uniform solid sphere'),ha='center',fontsize=10)
    b.text(1.5,-1.45,tr('分散散射单元','Separated scatterers'),ha='center',fontsize=10)
    b.set_title(tr('B  相同均方距离，不同内部排列','B  Same mean-square distance, different structure'),loc='left',fontsize=11)
    save(fig,'geometry')
    fig,ax=plt.subplots(2,2,figsize=(12,9));a,b,c,d=ax.ravel()
    positive=I>0
    a.errorbar(q[positive][::8],I[positive][::8],yerr=sigma[positive][::8],fmt='.',ms=3,lw=.5,color=blue,alpha=.65)
    a.set_yscale('log');a.set_ylim(.01,30);a.set_xlabel('q / nm⁻¹');a.set_ylabel(tr('归档强度','Archived intensity'))
    a.set_title(tr('A  真实溶菌酶溶液曲线','A  Measured lysozyme solution profile'),loc='left')
    a.text(.97,.96,tr('非正强度见下一幅线性坐标图','Nonpositive intensities shown on linear axis next'),transform=a.transAxes,ha='right',va='top',fontsize=9)
    low=(q<=1.2)&positive
    b.errorbar(q[low]**2,np.log(I[low]),yerr=sigma[low]/I[low],fmt='o',ms=2,mfc='white',mec=gray,color=gray,lw=.5,alpha=.6)
    b.scatter(q[mask]**2,np.log(I[mask]),s=8,color=blue)
    x=np.linspace(0,.8**2,100);b.plot(x,result['intercept']+result['slope_nm2']*x,color=orange,lw=2)
    b.set_ylim(1.65,2.7);b.set_xlabel('q² / nm⁻²');b.set_ylabel('ln I');b.set_title(tr('B  Guinier区域：实心点参与拟合','B  Guinier region: filled points fitted'),loc='left')
    c.scatter(q[mask],(I[mask]-predicted[mask])/sigma[mask],s=10,color=blue)
    c.axhline(0,color=gray);c.set_xlabel('q / nm⁻¹');c.set_ylabel(tr('(观测−预测) / σ','(Observed − predicted) / σ'))
    c.set_title(tr('C  以归档误差为单位的残差','C  Residuals in reported-error units'),loc='left')
    d.plot(windows,sensitivity,color=green,lw=2);d.axvline(.8,color=orange,ls='--')
    d.axhline(1.5,color=gray,ls=':',label=tr('归档页面报告值1.5 nm','Entry-reported value 1.5 nm'))
    d.set_xlabel('qmax / nm⁻¹');d.set_ylabel('Rg / nm');d.set_title(tr('D  改变上限，检查估计稳定性','D  Change upper bound; inspect stability'),loc='left');d.legend(fontsize=9)
    fig.suptitle(tr('真实数据：Darja Ruskule · SASBDB SASDAC2','Measured data: Darja Ruskule · SASBDB SASDAC2'),fontsize=13)
    fig.tight_layout();save(fig,'guinier')
    fig,axs=plt.subplots(1,2,figsize=(12,4.8));a,b=axs
    x=np.linspace(.001,7,900);u=np.sqrt(5/3)*x
    sphere=(3*(np.sin(u)-u*np.cos(u))/u**3)**2
    chain=2*(np.exp(-x*x)-1+x*x)/x**4
    a.plot(x,x*x*sphere,color=green,label=tr('均匀圆球模型','Uniform sphere model'))
    a.plot(x,x*x*chain,color=orange,label=tr('理想高斯链模型','Ideal Gaussian-chain model'))
    a.set_xlabel('q Rg');a.set_ylabel('(q Rg)² I(q) / I(0)');a.legend();a.set_title(tr('A  同一Rg下的模型形状','A  Model shapes at the same Rg'),loc='left')
    high=np.unique(np.r_[np.flatnonzero(q>4.5)[::3],np.flatnonzero((q>4.5)&(I<=0))])
    b.errorbar(q[high],I[high],yerr=sigma[high],fmt='.',color=blue,lw=.5,alpha=.65)
    b.axhline(0,color=gray);b.set_xlabel('q / nm⁻¹');b.set_ylabel(tr('归档强度，线性坐标','Archived intensity, linear scale'))
    b.set_title(tr('B  高q端：负值也属于测量结果','B  High q: negative values remain data'),loc='left')
    fig.tight_layout();save(fig,'shape')
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':main()
```

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/I07.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [SASBDB SASDAC2 — Lysozyme in sodium acetate](https://www.sasbdb.org/data/SASDAC2/)

   Measured curve, sample conditions and entry-reported dimensions; depositor Darja Ruskule.

   SASBDB unrestricted reuse policy; attribution required by community guidance.
2. [SASBDB — About and data-use policy](https://www.sasbdb.org/about/)

   Data-reuse conditions and archive context.

   Data and models free of copyright restrictions, with original-author attribution requested.
3. [BioXTAS RAW — Guinier analysis](https://bioxtas-raw.readthedocs.io/en/latest/saxs/saxs_guinier.html)

   Low-q windows, errors, aggregation and fit assessment.

   Public technical reference; no figure reproduced.
4. [SSRL — SAXS data analysis primer](https://www-ssrl.slac.stanford.edu/smb-saxs/content/data-analysis-primer)

   Buffer matching and connections between profiles and structural questions.

   Public facility educational reference; no figure reproduced.
5. [Trewhella et al. — 2017 biomolecular SAS reporting guidelines](https://journals.iucr.org/d/issues/2017/09/00/jc5010/index.html)

   Guinier range, residuals, P(r) and evidence supporting structural interpretation.

   Open scientific reference; no paper figure reproduced.
6. [André Guinier — Personal reminiscences](https://www.iucr.org/what-we-do/publications/books/Fifty-Years-of-X-ray-Diffraction/guinier)

   Historical connection between small-angle scattering and aluminium–copper ageing in 1938.

   Historical primary account; original explanatory illustration used.
