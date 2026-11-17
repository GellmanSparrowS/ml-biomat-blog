# FTIR: Reading materials through molecular vibrations

Source: https://ml-biomat.com/tutorials/experimental-methods/s01/en/
Language: en

Follow molecular vibrations in a transparent film through spectral reading, ATR sampling and calibration, using measured polymer data and a complete computational example.

## 1. Two transparent films, two molecular fingerprints

A piece of food packaging and a dried hydrogel film can both look transparent and flexible. Their appearance gives few clues about the molecules inside. Infrared spectroscopy offers a different way of looking: illuminate a specimen with infrared radiation spanning many wavelengths, then determine which parts of the radiation are reduced. Some molecular motions absorb energy in particular frequency ranges. The instrument arranges that response into a spectrum, where a broad band, a cluster of nearby peaks or an almost featureless region can help identify chemical structures and changes in their surroundings.

Useful research questions are often quite specific. Does a functional group present in the starting material remain after a polymer film is prepared? How does a collagen-coated surface differ from the uncoated substrate? Which changes between a hydrated and a dry specimen arise from water, and which deserve investigation as changes in the polymer? A functional group is a recognizable group of atoms with characteristic chemical behavior, such as the oxygen and hydrogen in a hydroxyl group. Interpreting a spectrum means assembling several such clues in the context of the specimen. A single peak is rarely an adequate description of an entire material.

The history begins with a remarkably accessible measurement. In 1800, William Herschel compared heating at different positions in sunlight dispersed by a prism. A thermometer responded beyond the visible red region. Radiation could therefore affect a detector even where the eye saw no light. Infrared spectroscopy eventually developed a more chemically focused question: how do different substances change this radiation? Early measurements examined wavelengths in sequence and accumulated reference spectra. Modern instruments acquire an encoded optical signal and use computation to recover a broad spectrum. The two arrangements in the figure distinguish discovering radiation from measuring a molecular response.

![From Herschel’s prism-and-thermometer experiment to an FTIR interferometer. The historical panel illustrates the principle; thermometer heights are not historical measurements. The moving mirror changes optical path difference before the specimen signal is detected.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/6fa4536aed62f1960653431a.svg?v=6fa4536aed62)

Figure 1From Herschel’s prism-and-thermometer experiment to an FTIR interferometer. The historical panel illustrates the principle; thermometer heights are not historical measurements. The moving mirror changes optical path difference before the specimen signal is detected.

The familiar abbreviation FTIR means Fourier-transform infrared spectroscopy. It describes how the instrument obtains the spectrum. ATR, attenuated total reflectance, describes how light interacts with the specimen. The two terms can occur together, so ATR-FTIR is a compatible combination of acquisition and sampling methods. An FTIR instrument can use transmission or an ATR accessory, and the same material can show different relative band intensities in those arrangements. When comparing spectra, keep the chemical identity of the material and the method used to sample it in view at the same time.

## 2. Why molecules absorb: restoring forces, masses and charge

Atoms in a molecule are continually moving. A bond length can oscillate around its equilibrium value, and the angle between connected atoms can bend. Imagining two balls connected by a spring captures a useful first principle: a stronger restoring force generally produces faster oscillation, while a greater moving mass generally slows it. Real chemical bonds involve shared electrons and their vibrations obey quantum mechanics. The spring picture is useful because it isolates the competition between restoring force and inertia, particularly for small displacements around an equilibrium structure.

Light has a frequency as well: the number of electric-field cycles per second. A photon can be absorbed when its energy matches an allowed difference between molecular vibrational states and the electric field couples to that motion. Pushing a swing provides an imperfect but useful analogy. The timing must be appropriate, and the applied force must act in a way that can drive the motion. For infrared absorption, the coupling condition involves a change in molecular electric dipole moment during vibration. The dipole moment describes the separation of positive and negative charge. A bond may therefore be present without producing an intense infrared band.

$$
\widetilde\nu=\frac{1}{\lambda},\qquad \widetilde\nu\,[\mathrm{cm}^{-1}]=\frac{10^4}{\lambda\,[\mu\mathrm m]},\qquad \Delta E=h c_0\widetilde\nu
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5c3c839204ef46d63255be41.svg) | Wavenumber, in cm⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | Wavelength; use reciprocal length units consistently in the first expression, and μm in the second. |
| ![Formula](https://ml-biomat.com/static/agent-math/03a061659f8f3f0ea28e1238.svg) | Energy difference for an absorption event, in J. |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | Planck constant, 6.62607015×10⁻³⁴ J s. |
| ![Formula](https://ml-biomat.com/static/agent-math/b1fcf1f7db8487b0faca625a.svg) | Speed of light in vacuum; use 2.99792458×10¹⁰ cm/s when wavenumber is in cm⁻¹. |

One centimetre contains 10⁴ micrometres, so a wavelength of 10 μm corresponds to 1000 cm⁻¹. Its photon energy is approximately 1.986×10⁻²⁰ J. Matching the energy also requires an allowed molecular coupling for absorption.

The horizontal axis of an infrared spectrum usually shows wavenumber rather than wavelength. Wavenumber counts how many wave cycles fit into one centimetre: a shorter wavelength gives a larger count. A common mid-infrared range, 4000 to 400 cm⁻¹, corresponds to wavelengths from 2.5 to 25 μm. A micrometre is one thousandth of a millimetre. Spectra are often drawn with high wavenumbers on the left, so wavelength increases and photon energy decreases as you move right. Check the axis direction before describing a peak as moving to higher or lower frequency.

$$
\mu=\frac{m_1m_2}{m_1+m_2},\qquad \widetilde\nu=\frac{1}{2\pi c_0}\sqrt{\frac{k}{\mu}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | Reduced mass, in kg, representing the relative motion of two atoms. |
| ![Formula](https://ml-biomat.com/static/agent-math/57ad720e8c13de438f8f5ea6.svg) | Masses of the two modeled atoms, in kg. |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | Harmonic restoring-force constant, in N/m. |
| ![Formula](https://ml-biomat.com/static/agent-math/b1fcf1f7db8487b0faca625a.svg) | Vacuum speed of light in cm/s, giving wavenumber in cm⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/5c3c839204ef46d63255be41.svg) | Model vibrational wavenumber, in cm⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | Pi, dimensionless. |

For a simplified carbon–hydrogen oscillator with masses 12 u and 1 u, the reduced mass is 0.923 u, where 1 u is approximately 1.66054×10⁻²⁷ kg. With k=500 N/m, the wavenumber is about 3030 cm⁻¹. This harmonic model explains mass and stiffness trends; polymer modes include collective motion and environmental effects.

The spring model also explains why isotope substitution can help assign bands. Isotopes retain the same elemental identity but have different atomic masses. Replacing hydrogen with the heavier isotope deuterium can change the mass participating in a vibration substantially while causing a much smaller change in the underlying electronic bonding. The vibration then commonly shifts to lower wavenumber. Researchers use this shift to distinguish overlapping motions. In a protein, however, a normal mode often involves several atoms moving together, so assigning every peak to a completely independent bond would miss the collective character of the motion.

The amide I region provides a biological example. Its response is dominated by stretching associated with peptide carbonyl groups, but coupling between peptide units and their local environments also shapes the band. A broad band can contain many slightly different contributions. Hydroxyl groups in a polymer may participate in hydrogen bonds of varying strength; the resulting range of environments contributes to a range of vibrational frequencies. Instrument resolution, temperature and molecular motion also influence line shape. Width is consequently part of the information in a spectrum, rather than a nuisance to remove automatically during processing.

## 3. How an instrument turns light into a curve

Start with transmission. The instrument records a reference intensity without the specimen of interest and a sample intensity after light has passed through it. Their ratio describes the fraction of light remaining at each wavenumber. This ratio compensates for much of the spectral variation already present in the source, optical path and detector. It also explains why the background measurement belongs to a particular set of conditions. If atmospheric water, carbon dioxide or the accessory has changed, an earlier background may no longer describe the current optical path well.

$$
T(\widetilde\nu)=\frac{I(\widetilde\nu)}{I_0(\widetilde\nu)},\qquad A(\widetilde\nu)=-\log_{10}T(\widetilde\nu)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | Fractional transmittance, dimensionless; enter 50% as 0.5. |
| ![Formula](https://ml-biomat.com/static/agent-math/112feff6b4d0334226e24d5c.svg) | Transmitted sample intensity, in the same units as the reference. |
| ![Formula](https://ml-biomat.com/static/agent-math/6e4f2807ce72e4cab3957130.svg) | Reference intensity, in matching instrument signal units. |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Absorbance, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/5c3c839204ef46d63255be41.svg) | Wavenumber, in cm⁻¹; the intensity ratio is taken at each wavenumber. |
| ![Formula](https://ml-biomat.com/static/agent-math/be8ebdecd039424afe275a60.svg) | Base-10 logarithm of a dimensionless ratio. |

With reference intensity 1000 and sample intensity 500, T=0.5 and A=0.30103. Two identical half-transmitting layers give T=0.25 and A=0.60206. The logarithm turns multiplicative transmission into additive absorbance. These are transmission definitions; ATR uses a ratio of reflected sample and reference signals.

Why transform transmittance into absorbance? Imagine two identical layers, each transmitting half the incident light. Together they transmit a quarter, because their transmission fractions multiply. Taking a negative logarithm turns that product into a sum: the absorbances of the layers add under the corresponding transmission assumptions. This is useful for quantitative work. A transmittance of 50% gives an absorbance of approximately 0.301; 10% gives 1; and 1% gives 2. Each additional absorbance unit therefore corresponds to ten times less transmitted light. A tall peak does not automatically provide a more precise measurement, because very little light may remain above detector noise and stray-light contributions.

In FTIR, an interferometer encodes the different wavelengths. A beam splitter sends light along two paths, one towards a fixed mirror and the other towards a moving mirror, and brings the beams together again. Moving the mirror changes their optical path difference. For a given wavelength, the returning waves alternate between reinforcement and cancellation. Different wavelengths produce different patterns as the path difference changes. The detector records an interferogram, and a Fourier transform separates its frequency content to obtain a spectrum. There is a useful parallel with decomposing a musical chord into frequency components: the original measurement contains a superposition rather than a separately recorded value for every component.

Two instrument settings serve different purposes. Averaging more scans reduces uncorrelated random noise; in the ideal case, taking four times as many scans improves the signal-to-noise ratio by about a factor of two. Higher spectral resolution requires information over a larger range of optical path differences and helps separate nearby spectral features. Interpolating an exported spectrum into more points creates a denser numerical grid, not new resolving power. Choose acquisition settings according to the features that matter: broad polymer bands demand a different balance of resolution, measurement time and specimen stability from closely spaced narrow lines.

Check the vertical axis before applying any transformation. A file may contain percentage transmittance, absorbance or normalized intensity. Taking a negative logarithm of data that are already absorbance changes their meaning. Treating 50% transmittance as 50 rather than as the fraction 0.5 also produces the wrong result. The pair 50% and 0.301 is a useful numerical check. Preserving the sample spectrum, reference spectrum, units and processing choices makes it possible to reconstruct what each reported value represents when the analysis is revisited.

## 4. ATR: convenient sampling with an important interface

Transmission requires light to cross the specimen. A thick polymer sheet can absorb almost all the light in some regions, while water can dominate parts of a hydrated sample's spectrum. ATR places the specimen against a crystal of relatively high refractive index. Infrared light reaches the interface from inside the crystal at an oblique angle and returns towards the detector. Refractive index describes an optical property of the medium, and the incidence angle is measured relative to the surface normal. Under suitable conditions, an electromagnetic field extends into the sample near the interface, and the specimen changes the returning light.

![The spring model connects restoring force to mass; the ATR diagram connects the interface to depth weighting. Profiles use real refractive indices at 45° incidence. The labeled dₚ is the amplitude decay length; intensity there is e⁻².](https://ml-biomat.com/static/tutorials/experimental-methods/figures/3aeb8a5896a1a443074b4e1d.svg?v=3aeb8a5896a1)

Figure 2The spring model connects restoring force to mass; the ATR diagram connects the interface to depth weighting. Profiles use real refractive indices at 45° incidence. The labeled dₚ is the amplitude decay length; intensity there is e⁻².

This arrangement makes many solids, powders and soft materials straightforward to examine, provided they contact the crystal well. A thermal probe held against an object offers a useful everyday analogy: an air gap changes how effectively it senses the object. ATR involves optical rather than thermal coupling, but the quality of contact is similarly consequential. A pressure device helps a solid conform to the crystal. Surface roughness, powder particle size and deformation of a soft specimen can all change the actual contact. If nearly all bands become stronger together, compare the sampling conditions before attributing the change to composition.

$$
d_p=\frac{\lambda}{2\pi n_1\sqrt{\sin^2\theta-(n_2/n_1)^2}},\qquad \frac{|E(z)|^2}{|E(0)|^2}=\exp\!\left(-\frac{2z}{d_p}\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f34c990e19a62f93d18d883f.svg) | Amplitude 1/e decay depth, in μm. |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | Vacuum wavelength, in μm. |
| ![Formula](https://ml-biomat.com/static/agent-math/c2652c58d15d116e3ef5414c.svg) | Real refractive indices of crystal and sample, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | Incidence angle inside the crystal, measured from the normal; use radians in trigonometric calculations. |
| ![Formula](https://ml-biomat.com/static/agent-math/9032cb23a878659e74b670d3.svg) | Distance into the sample from the interface, in μm. |
| ![Formula](https://ml-biomat.com/static/agent-math/74335d93aebe185d8164d835.svg) | Electric-field amplitudes at depth z and at the interface, in matching units such as V/m. |
| ![Formula](https://ml-biomat.com/static/agent-math/579aca15d6b056589d293cd9.svg) | Pi is the circle constant; exp is the natural exponential function. |

For n₁=2.4, n₂=1.5 and θ=45°, 1000 cm⁻¹ gives λ=10 μm and dₚ=2.005 μm. At z=dₚ, normalized intensity is exp(−2)=0.1353. This real-index field approximation requires sinθ>n₂/n₁; strong absorption requires the full interface-optics treatment.

The penetration depth in this expression is an amplitude decay length. At that distance, the electric-field amplitude has fallen to 1/e of its interface value. Field intensity is proportional to the amplitude squared, so the corresponding normalized intensity is approximately 0.135. This is a gradually decaying weighting, rather than a sharply defined layer that is fully measured while everything below it is ignored. For the refractive indices and 45° angle in the figure, the amplitude decay length is about 2.01 μm at 1000 cm⁻¹ and 1.00 μm at 2000 cm⁻¹. Wavelength therefore changes the depth weighting and can affect relative band intensities.

The calculation uses real refractive indices and the field distribution appropriate to the nonabsorbing-index approximation, providing useful scale and trend estimates near weak absorption. Actual ATR measures a reflection response. Strong absorption, substantial refractive-index dispersion or operation near a critical angle requires a fuller treatment of interface optics. Quantitative ATR work accordingly benefits from standards measured with the same crystal, contact procedure, temperature and matrix. Substituting a nominal penetration depth for the fixed path length of a transmission cell does not establish an ATR calibration. With a thin coating, include the substrate in the comparison because both coating and substrate can contribute to the optical response.

## Interactive experiment: How deep does ATR sample?

Keep the crystal and sample refractive indices at 2.4 and 1.5. Change wavenumber and incidence angle. The left panel shows the intensity profile into the sample; the right locates the current setting on a depth–wavenumber curve. Compare the effects of longer wavelengths and larger angles.

[Figure: ATR field-intensity profile and wavenumber-dependent decay depth](https://ml-biomat.com/tutorials/experimental-methods/s01/en/#S01-plot)

The curves use a real-index approximation. An amplitude decay length differs from a fixed transmission path. The normalized field intensity illustrates a calculated depth weighting.

In the interactive view, first leave the angle unchanged and increase the wavenumber from 1000 to 2000 cm⁻¹. Watch the entire intensity profile contract towards the surface. Then hold the wavenumber constant and vary the angle. The curve turns sampling depth into a continuous weighting, which is more informative than a single depth value. For a surface coating, it helps formulate the next experimental question: how strongly does the present geometry weight the interface region, and how much substrate contribution should be expected given the coating thickness and optical properties?

Contact and cleanliness also belong in a comparison between specimens. A residual polymer layer on the crystal can produce plausible-looking bands in the next measurement, especially when the specimens contain related materials. A clean-crystal background check is therefore a direct way to test whether the optical interface is ready for the next sample. Record the conditions that affect contact, rather than assuming identical pressure-device settings necessarily produce identical contact areas in a stiff film and a soft gel.

## 5. Read a measured polymer spectrum from overview to detail

The measured example below is the “LDPE in soil” spectrum distributed openly with OpenSpecy. Low-density polyethylene has a carbon–hydrogen chain structure and is familiar from everyday films. The soil background makes this a useful exercise in reading polymer clues alongside other contributions in a mixed specimen. The file provides 1798 signal values and their wavenumber range. The figure preserves the published response values, labeled as original-file signal, rather than assigning concentration or acquisition units that are not fully documented. Here we examine band patterns and smoothing; the next section supplies an explicitly defined transmission experiment for concentration calibration.

![Measured LDPE-in-soil spectrum distributed with OpenSpecy (CC BY 4.0), replotted here. The ordinate preserves the original response values. Shading guides attention to C–H stretching and methylene bending/rocking regions. The enlarged region and residuals show how smoothing changes band shape.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9df28675a34609bdcfaffeae.svg?v=9df28675a346)

Figure 3Measured LDPE-in-soil spectrum distributed with OpenSpecy (CC BY 4.0), replotted here. The ordinate preserves the original response values. Shading guides attention to C–H stretching and methylene bending/rocking regions. The enlarged region and residuals show how smoothing changes band shape.

Begin with the broad regions of the spectrum. Hydroxyl stretching commonly contributes around 3000–3600 cm⁻¹, with hydrogen bonding affecting position and width. Carbon–hydrogen stretching often appears around 2800–3000 cm⁻¹. Lower wavenumbers contain a combination of stretching, bending and coupled motions; their pattern is often useful for identification and is commonly called the fingerprint region. The example has prominent carbon–hydrogen stretching features near 2915 and 2848 cm⁻¹. Lower-wavenumber methylene bending and rocking regions provide additional clues, highlighted by the shaded areas. Contributions from the soil background are considered alongside this pattern of polymer bands. A more specific interpretation develops by comparing several bands, the known chemistry of the specimen and suitable reference spectra acquired with comparable sampling methods.

Water deserves particular attention in biological materials. Its stretching absorption is strong, and its bending contribution lies near the protein amide I region. A change in a hydrated protein specimen can therefore include both water-content changes and changes in the protein environment. Drying reduces water contributions but can also alter conformation and hydrogen bonding. Decide first whether the research question concerns a hydrated material, a dry material or hydration itself, then match the controls to that state. Preparation is part of the experiment's scientific definition, rather than a neutral preliminary step.

The full spectrum is shown together with a lightly smoothed version. Smoothing summarizes the local trend across neighboring points. It can suppress rapid fluctuations, but it can also modify a narrow real feature. Here the Savitzky–Golay method fits a low-degree polynomial within a moving window and uses its central fitted value. An 11-point window has a physical width determined by the wavenumber spacing, so the number 11 alone does not specify how aggressive the processing is. The enlarged region compares 11-point and 41-point windows on identical axes. The larger window visibly modifies the band shape.

The lower-right panel plots the original signal minus the smoothed signal. Structured positive and negative features around a band indicate that the operation removed a recognizable shape, not simply irregular noise. Another important choice is normalization. Scaling every spectrum to a maximum of one makes relative shape easier to compare, while removing information about overall intensity. For a question about the amount of absorption, return to the original scale and examine thickness, contact and reference conditions. Smoothing, baseline correction and normalization solve different problems; deciding which question each step answers helps keep the analysis interpretable.

## 6. Turning a band into an interpretable measurement

Consider an absorbing component in a transmission specimen of fixed optical thickness. Increasing its concentration places more absorbing units along the same path. With suitable control of chemical state, path length and instrumental response, absorbance is approximately proportional to concentration. This is the practical starting point of the Beer–Lambert relationship. Standards with known concentrations establish a scale on which an unknown can be placed. The essential experimental connection is that standards and unknowns share comparable chemistry and sampling conditions, not merely that a straight line can be fitted to a set of numbers.

$$
A=\varepsilon c\ell
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Absorbance at the selected wavenumber, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/9bc08d537f481d038b7b8b9d.svg) | Molar absorption coefficient, in L mol⁻¹ cm⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | Concentration of the absorbing component, in mol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/dac4cdb34a25b3b90b51bf8b.svg) | Transmission path length, in cm. |

With ε=120 L mol⁻¹ cm⁻¹, a 0.005 cm path and c=0.650 mol/L, the band-center absorbance is 0.390. This defines the constructed peak height, assuming a fixed path and chemical state in a suitable linear transmission regime. ATR requires calibration under its own sampling conditions.

A real band occupies an interval rather than a single point. Its highest sampled value can be sensitive to noise, grid spacing and spectral resolution. Integrating over a fixed interval offers another measure. Think of the area as many narrow strips: each strip has a signal height and a small wavenumber width, and their contributions are added. Before integrating, estimate the baseline. In this example, points on both sides of the central band define a straight, slowly varying background. The corrected signal is then integrated from 1660 to 1800 cm⁻¹ using the trapezoidal rule.

$$
Q=\int_{\widetilde\nu_a}^{\widetilde\nu_b}[A(\widetilde\nu)-B(\widetilde\nu)]\,d\widetilde\nu,\qquad Q=mc+b,\qquad \widehat c=\frac{Q_u-b}{m}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/30efb430554daf87861b0459.svg) | Baseline-corrected areas for standards and unknown, in cm⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/f148cd39757f2803a55c933b.svg) | Lower and upper integration limits, 1660 and 1800 cm⁻¹ here. |
| ![Formula](https://ml-biomat.com/static/agent-math/5ef648b1dc468d185ae3f4f4.svg) | Measured absorbance and estimated baseline, both dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/c5a2c12967ff8ea7b23cc316.svg) | An infinitesimal wavenumber interval, in cm⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Area–concentration slope, in cm⁻¹ L/mol. |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Fitted intercept, in cm⁻¹; distinct from each spectrum’s baseline B. |
| ![Formula](https://ml-biomat.com/static/agent-math/aa86a0645aeb94c36638b99e.svg) | Standard concentration and estimated unknown concentration, in mol/L. |

Trapezoidal integration on an ascending grid gives m≈27.088 and b≈−0.00506. Substituting the unknown area yields approximately 0.6468 mol/L. A fixed window, common baseline rule and comparable sampling connect standards and unknown on the same scale.

![Constructed transmission calibration: six concentrations with three independent noise realizations each. Pale-yellow side intervals define the baseline before fixed-window integration. The unknown is estimated at about 0.647 mol/L; residual and transmittance plots help interpret the calibration and acquisition conditions.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d36ca2e3eba4d7269b4a13e0.svg?v=d36ca2e3eba4)

Figure 4Constructed transmission calibration: six concentrations with three independent noise realizations each. Pale-yellow side intervals define the baseline before fixed-window integration. The unknown is estimated at about 0.647 mol/L; residual and transmittance plots help interpret the calibration and acquisition conditions.

The calibration is a declared constructed transmission experiment. There are six concentrations and three independent simulated noisy observations at each concentration. The underlying band is centered at 1730 cm⁻¹, and its width and background form are held constant. The fitted slope is approximately 27.09 cm⁻¹ per mol/L. An unknown created at 0.650 mol/L is recovered at approximately 0.647 mol/L. Their agreement checks the consistency of baseline estimation, integration and inverse calibration within this controlled example. In an actual experiment, independently prepared or independently sampled standards are needed to describe experimental variation; copying one curve three times supplies no such information.

Band area carries units of cm⁻¹ because absorbance is dimensionless while the integration axis has wavenumber units. The calibration slope consequently has area units divided by concentration units. Keeping track of those units makes the inverse calculation transparent: subtract the fitted intercept from the unknown's area, then divide by the slope. The numerator and denominator cancel their area units, leaving concentration. A numerical result is much easier to interpret when its units can be followed through the calculation rather than attached at the end.

Inspect residuals as well as the coefficient of determination. A residual is the measured area minus the area predicted by the fitted line. Consistently negative residuals at high concentration suggest checking strong absorption, changes in chemical state or saturation. A spread that increases with concentration suggests different measurement precision across the range. If all repeats at one concentration shift together, revisit standard preparation. A high coefficient of determination describes the overall arrangement of the points around a line; the residual pattern helps identify which experimental or model assumptions deserve attention.

Uncertainty also passes through the inverse calculation. A smaller calibration slope turns a given area fluctuation into a larger concentration fluctuation. An unknown outside the standard range requires extrapolating a relationship into conditions that the standards did not examine. Adjusting the unknown into the calibrated range, then applying and reporting the dilution factor, provides a more directly tested route. For overlapping bands, also decide whether the extracted area represents the entire mixed region or a component separated by an additional model. That distinction determines the scientific name of the reported quantity.

## 7. A complete program for reading, processing and checking

The program below reproduces the figures and analysis. It reads the bundled LDPE-in-soil data, sorts the wavenumbers into ascending order, applies smoothing and plots the result using the common infrared convention of high wavenumbers on the left. Computational ordering and visual axis direction are separate decisions. Integration uses ascending wavenumbers, while the plotted axis is reversed. Keeping the distinction explicit avoids obtaining a negative area merely because the integration coordinates were supplied in descending order.

The second part generates calibration spectra, estimates their individual baselines, integrates band areas and fits a line. Outputs include the figures, constructed spectra, baselines, calibration areas, residuals and a numerical summary. This makes every plotted point traceable to a saved value. The random seed is fixed at 26, so rerunning the example reproduces the same teaching dataset. Deliberately changing the seed generates another realization of the same specified experiment with different random fluctuations. It does not change the stated physical model or create an independent measured dataset.

### Complete example: measured spectral reading and controlled calibration

The archive includes the published LDPE-in-soil file and its CC BY 4.0 license. Running it produces four figure sets, processed spectra, calibration tables, constructed spectra and summary.json.

```
"""FTIR: measured OpenSpecy LDPE-in-soil spectrum and a constructed calibration.

Run: python main.py --output output --language en
The bundled LDPE-in-soil signal retains its published ordinate; acquisition units were
not fully documented in that ASP file. Calibration data below are a controlled simulation.
"""
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.signal import savgol_filter
from scipy.stats import linregress
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle

BLUE, RED, GOLD, GREY = '#12687b', '#be6047', '#a87d22', '#71828c'


def configure():
    plt.rcParams.update({'font.family': 'sans-serif',
        'font.sans-serif': ['Microsoft YaHei', 'Noto Sans CJK SC', 'DejaVu Sans'],
        'font.size': 11, 'axes.titlesize': 13, 'axes.labelsize': 11,
        'axes.spines.top': False, 'axes.spines.right': False,
        'svg.fonttype': 'none', 'axes.unicode_minus': False,
        'savefig.facecolor': 'white', 'axes.edgecolor': '#c6d0d5'})


def penetration(wavenumber_cm, angle_deg, n_crystal=2.4, n_sample=1.5):
    """Amplitude 1/e depth in micrometres, nonabsorbing-index approximation."""
    term = np.sin(np.deg2rad(angle_deg))**2 - (n_sample/n_crystal)**2
    if np.any(term <= 0):
        raise ValueError('Use an angle above the critical angle.')
    wavelength_um = 10000 / np.asarray(wavenumber_cm)
    return wavelength_um / (2*np.pi*n_crystal*np.sqrt(term))


def main(output, language):
    output.mkdir(parents=True, exist_ok=True)
    configure()
    tr = lambda zh, en: zh if language == 'zh' else en
    def save(fig, name):
        fig.savefig(output/f'{name}-{language}.svg', bbox_inches='tight')
        plt.close(fig)
    def arrow(ax, x1, y1, x2, y2, color=BLUE, lw=2):
        ax.annotate('', (x2,y2), (x1,y1), arrowprops={'arrowstyle':'->','color':color,'lw':lw})

    # A history/optics diagram, not a reconstructed historical measurement.
    fig, axes = plt.subplots(1, 2, figsize=(12.8,5.3), layout='constrained')
    for ax in axes:
        ax.set(xlim=(0,10), ylim=(0,7)); ax.axis('off')
    ax=axes[0]
    ax.set_title(tr('A  从“看不见”到可测量：赫歇尔，1800','A  Making invisible radiation measurable: Herschel, 1800'),loc='left',pad=20)
    arrow(ax,.3,4.5,3.2,4.5,GOLD)
    ax.add_patch(Polygon([[3,3.7],[3.8,5.4],[4.6,3.7]],fc='#dceaf0',ec=BLUE))
    for j,col in enumerate(['#7164a0','#3b8fa5','#5d9c61','#c1a23f','#bd5c47']):
        ax.plot([4.1,7.1],[4.4,5.8-j*.5],color=col,lw=4)
    ax.plot([4.1,7.1],[4.4,2.8],color=RED,lw=2,ls='--')
    ax.text(.3,5,tr('阳光','Sunlight'),color=GOLD)
    ax.text(2.8,3.1,tr('棱镜分光','Prism'),color=BLUE)
    ax.text(7.3,5.7,tr('可见光','Visible light'),va='center')
    ax.text(7.3,3.8,tr('红光','Red light'),va='center')
    ax.text(7.3,2.8,tr('红外区域','Infrared'),va='center',color=RED)
    for j in range(3):
        x=6.8+j*.65; y=1.3
        ax.add_patch(Circle((x,y),.18,fc=RED,ec='none'))
        ax.add_patch(Rectangle((x-.06,y),.12,.9,fc='#f1d7cf',ec=GREY))
        ax.plot([x,x],[y,y+.35+j*.15],color=RED,lw=3)
    ax.text(.3,1.2,tr('温度计比较不同位置的升温\n图示的是实验思路，不是历史数据','Thermometers compare heating at different positions\nConceptual reconstruction, not historical data'),fontsize=10,va='center')
    ax=axes[1]
    ax.set_title(tr('B  FTIR：改变光程差，记录干涉信号','B  FTIR: vary path difference and record interference'),loc='left',pad=20)
    arrow(ax,.3,3.8,3.6,3.8,GOLD)
    ax.plot([3.5,4.2],[3.4,4.2],color=GREY,lw=5)
    arrow(ax,3.85,3.8,3.85,6,BLUE);arrow(ax,4.05,6,4.05,3.8,RED)
    ax.plot([3.1,4.8],[6.2,6.2],color=GREY,lw=5)
    arrow(ax,4.2,3.8,7.6,3.8,BLUE);arrow(ax,7.6,3.6,4.2,3.6,RED)
    ax.plot([7.8,7.8],[3.1,4.5],color=GREY,lw=5)
    arrow(ax,7.6,5,8.7,5,GREY)
    arrow(ax,3.9,3.5,3.9,1.5,RED)
    ax.add_patch(Rectangle((3.3,1.35),1.3,.45,fc='#b6d6d1',ec=BLUE))
    ax.add_patch(Rectangle((3.2,.3),1.5,.6,fc='#e7edf0',ec=GREY))
    arrow(ax,3.9,1.3,3.9,.9,RED)
    labels=[(.3,4.3,'红外源','IR source'),(.4,2.8,'分束器','Beam splitter'),(4.9,6.1,'固定镜','Fixed mirror'),(6.3,5.5,'移动镜','Moving mirror'),(5,1.5,'样品或ATR附件','Sample / ATR accessory'),(5,.55,'探测器','Detector')]
    for x,y,z,e in labels:ax.text(x,y,tr(z,e),fontsize=10)
    save(fig,'history-optics')

    fig=plt.figure(figsize=(12.8,6.8),layout='constrained')
    gs=fig.add_gridspec(2,2,width_ratios=[1,1.15])
    ax=fig.add_subplot(gs[0,0]);ax.set(xlim=(0,10),ylim=(0,5));ax.axis('off')
    ax.set_title(tr('A  键：弹性恢复力与运动质量','A  A bond: restoring force and moving masses'),loc='left')
    for x,r,col,label in [(2,.65,BLUE,'C'),(8,.45,RED,'H')]:
        ax.add_patch(Circle((x,2.6),r,fc=col));ax.text(x,2.6,label,color='white',ha='center',va='center',fontsize=17)
    x=np.linspace(2.7,7.5,120);ax.plot(x,2.6+.23*np.sin(np.linspace(0,16*np.pi,120)),color=GREY,lw=2)
    arrow(ax,1.3,1.3,2.5,1.3);arrow(ax,8.8,1.3,7.6,1.3,RED)
    ax.text(5,.2,tr('运动时电荷分布的变化决定红外活性','Changing charge distribution determines IR activity'),ha='center',fontsize=10)
    ax=fig.add_subplot(gs[1,0]);ax.set(xlim=(0,10),ylim=(0,5));ax.axis('off')
    ax.set_title(tr('B  ATR：在界面附近取样','B  ATR: sampling near an interface'),loc='left')
    ax.add_patch(Rectangle((.4,.4),9,2,fc='#dceaf0',ec='none'))
    ax.add_patch(Rectangle((.4,2.4),9,1.5,fc='#dcece3',ec='none'))
    arrow(ax,1,.6,4,2.4,GOLD);arrow(ax,4,2.4,7,.6,GOLD)
    ax.plot([4,4],[.5,4.3],ls='--',color=GREY,lw=1)
    ax.text(.7,3.3,tr('样品 n2 = 1.5','Sample n2 = 1.5'),fontsize=10)
    ax.text(.7,.1,tr('晶体 n1 = 2.4','Crystal n1 = 2.4'),fontsize=10)
    for z in np.linspace(.05,1.3,16):ax.plot([3,5],[2.4+z]*2,color=RED,alpha=float(np.exp(-z*2)),lw=3)
    ax.text(5.5,3,tr('强度随距离衰减','Intensity decays with distance'),fontsize=10)
    ax=fig.add_subplot(gs[:,1]);z=np.linspace(0,8,300)
    for wn,col in [(1000,BLUE),(2000,RED),(3000,GOLD)]:
        dp=float(penetration(wn,45));ax.plot(z,np.exp(-2*z/dp),color=col,lw=2.5,label=f'{wn} cm$^{-1}$; dp={dp:.2f} μm')
    ax.set(xlabel=tr('距晶体表面的距离 / μm','Distance from crystal surface / μm'),ylabel=tr('归一化强度 |E/E0|²','Normalized intensity |E/E0|²'),title=tr('C  同一入射角下，波长改变取样权重','C  Wavelength changes the depth weighting'),ylim=(0,1.04))
    ax.legend(fontsize=10);ax.grid(alpha=.18)
    save(fig,'vibration-atr')

    asp=np.loadtxt(Path(__file__).parent/'data/openspecy-ldpe-soil.asp')
    assert len(asp)-6 == int(asp[0])
    raw=np.c_[np.linspace(asp[1],asp[2],int(asp[0])),asp[6:]]
    raw=raw[np.argsort(raw[:,0])];wn,signal=raw.T
    smooth=savgol_filter(signal,11,2)
    fig=plt.figure(figsize=(12.8,8.0),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[1.5,1])
    ax=fig.add_subplot(gs[0,:]);ax.plot(wn,signal,color=GREY,lw=1.5,label=tr('公开LDPE光谱原始数值','Published LDPE-in-soil values'));ax.plot(wn,smooth,color=BLUE,lw=1,label=tr('11点二阶平滑','11-point quadratic smoothing'))
    for lo,hi,txt,col in [(2800,3000,'C–H',RED),(1350,1500,'CH2',GOLD),(680,780,'CH2',BLUE)]:
        ax.axvspan(lo,hi,color=col,alpha=.08);ax.text((lo+hi)/2,.59,txt,color=col,ha='center',fontsize=10)
    ax.set(xlim=(4000,650),ylim=(0,.64),xlabel=tr('波数 / cm$^{-1}$','Wavenumber / cm$^{-1}$'),ylabel=tr('原文件信号 / 相对单位','Original-file signal / relative units'),title=tr('A  土壤中LDPE的实测光谱（OpenSpecy）','A  A published measured spectrum: LDPE-in-soil (OpenSpecy)'))
    ax.legend(loc='upper right',bbox_to_anchor=(1,.84),fontsize=10)
    ax=fig.add_subplot(gs[1,0]);keep=(wn>=2800)&(wn<=3000)
    ax.plot(wn[keep],signal[keep],'.-',color=GREY,label=tr('原数值','Original'))
    for window,col in [(11,BLUE),(41,RED)]:ax.plot(wn[keep],savgol_filter(signal,window,2)[keep],color=col,label=tr(f'{window}点窗口',f'{window}-point window'))
    ax.set(xlim=(3000,2800),xlabel=tr('波数 / cm$^{-1}$','Wavenumber / cm$^{-1}$'),ylabel=tr('相对信号','Relative signal'),title=tr('B  窗口变大，也会改变峰形','B  Wider smoothing changes the peak shape'));ax.legend(fontsize=9)
    ax=fig.add_subplot(gs[1,1]);ax.plot(wn,signal-smooth,color=RED,lw=1);ax.axhline(0,color=GREY,lw=1)
    ax.set(xlim=(4000,650),xlabel=tr('波数 / cm$^{-1}$','Wavenumber / cm$^{-1}$'),ylabel=tr('原始值 − 平滑值','Original − smoothed'),title=tr('C  检查被平滑去掉的结构','C  Inspect what smoothing removes'))
    save(fig,'ldpe-measured')

    rng=np.random.default_rng(26)
    x=np.linspace(1580,1880,601);g=np.exp(-.5*((x-1730)/18)**2)
    c=np.repeat(np.arange(6)*.2,3)
    base=.025+.00002*(x-1730)
    y=.6*c[:,None]*g+base+rng.normal(0,.003,(len(c),len(x)))
    anchors=(x<1620)|(x>1840);band=(x>=1660)&(x<=1800)
    baselines=np.array([np.polyval(np.polyfit(x[anchors],row[anchors],1),x) for row in y])
    corrected=y-baselines
    # Integrating a fixed window is less sensitive to a single noisy maximum.
    areas=np.trapezoid(corrected[:,band],x[band],axis=1)
    slope,intercept,r,p,se=linregress(c,areas)
    unknown_c=.65
    unknown=.6*unknown_c*g+base+rng.normal(0,.003,len(x))
    unknown_base=np.polyval(np.polyfit(x[anchors],unknown[anchors],1),x)
    unknown_area=float(np.trapezoid((unknown-unknown_base)[band],x[band]))
    recovered=(unknown_area-intercept)/slope
    residual=areas-(intercept+slope*c)
    # Repeated calibration specimens are independent simulated measurements.
    fig,axs=plt.subplots(2,2,figsize=(12.8,8.4),layout='constrained')
    ax=axs[0,0]
    for i,col in [(0,GREY),(9,BLUE),(15,RED)]:ax.plot(x,y[i],color=col,label=f'c = {c[i]:.1f} mol/L')
    ax.fill_between(x,0,.7,where=anchors,color=GOLD,alpha=.10)
    ax.set(xlim=(1880,1580),ylim=(0,.7),xlabel=tr('波数 / cm$^{-1}$','Wavenumber / cm$^{-1}$'),ylabel=tr('吸光度','Absorbance'),title=tr('A  构造实验：共同的背景与不同浓度','A  Constructed experiment: background and concentration'));ax.legend(fontsize=9)
    ax=axs[0,1];ax.scatter(c,areas,color=BLUE,s=22,label=tr('独立重复测量','Independent simulated repeats'));ax.plot([0,1],[intercept,intercept+slope],color=BLUE,lw=1.4)
    ax.scatter([recovered],[unknown_area],marker='D',s=55,color=RED,label=tr(f'未知样品估计：{recovered:.3f} mol/L',f'Unknown estimate: {recovered:.3f} mol/L'))
    ax.set(xlabel=tr('浓度 / mol/L','Concentration / mol/L'),ylabel=tr('校正后的峰面积 / cm$^{-1}$','Corrected band area / cm$^{-1}$'),title=tr('B  固定窗口的面积校准','B  Calibration using a fixed integration window'));ax.legend(fontsize=9)
    ax=axs[1,0];ax.scatter(c,residual,color=RED,s=26);ax.axhline(0,color=GREY,lw=1)
    ax.set(xlabel=tr('浓度 / mol/L','Concentration / mol/L'),ylabel=tr('面积残差 / cm$^{-1}$','Area residual / cm$^{-1}$'),title=tr('C  残差揭示直线遗漏了什么','C  Residuals inspect what the line misses'))
    ax=axs[1,1];absorb=np.linspace(0,3,200);ax.plot(absorb,100*10**(-absorb),color=BLUE,lw=2.4)
    ax.scatter([0,.30103,1,2],[100,50,10,1],color=RED,zorder=4)
    ax.set(xlabel=tr('吸光度 A','Absorbance A'),ylabel=tr('透过率 / %','Transmittance / %'),title=tr('D  高吸光度意味着探测器收到更少光','D  High absorbance leaves less light at the detector'));ax.grid(alpha=.15)
    save(fig,'calibration')
    np.savetxt(output/'ldpe-processed.csv',np.c_[wn,signal,smooth,signal-smooth],delimiter=',',header='wavenumber_cm-1,published_signal,smoothed_signal,residual',comments='')
    np.savetxt(output/'calibration.csv',np.c_[c,areas,residual],delimiter=',',header='concentration_mol_L,band_area_cm-1,residual_cm-1',comments='')
    np.savez_compressed(output/'spectra.npz',wavenumber_cm=x,absorbance=y,baseline=baselines,unknown=unknown)
    summary={'data_origin':'Measured LDPE-in-soil: OpenSpecy CC BY 4.0; calibration: constructed with seed 26',
        'ldpe_rows':int(len(wn)), 'ldpe_max_wavenumber_cm':float(wn.max()),
        'absorbance_at_half_transmission':float(-np.log10(.5)),
        'penetration_um_1000_45':float(penetration(1000,45)),
        'penetration_ratio_1000_to_2000':float(penetration(1000,45)/penetration(2000,45)),
        'calibration':{'slope':float(slope),'intercept':float(intercept),'r_squared':float(r*r),
        'unknown_true_mol_L':unknown_c,'unknown_estimated_mol_L':float(recovered),
        'residual_sd_cm-1':float(np.std(residual,ddof=2))}}
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
    assert len(wn)==1798 and np.all(np.diff(wn)>0)
    assert abs(recovered-unknown_c)<.01
    assert abs(summary['penetration_ratio_1000_to_2000']-2)<1e-12
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en')
    args=parser.parse_args()
    main(args.output,args.language)
```

Two focused modifications are useful after the first run. Increase the smoothing window from 11 to a larger odd number and compare peak height, width and residual structure together. Then increase the simulated measurement noise and inspect the recovered concentration and residual spread. The smoothing window must fit within the available data, and the polynomial degree must be lower than the window length. Preserve the original curve and compare plots with the same axes so that apparent differences reflect the processing rather than automatic rescaling.

The program also evaluates a few quantities with straightforward independent expectations. Half transmission must give an absorbance near 0.301. Under the stated fixed-index ATR approximation, doubling wavenumber halves the penetration depth. The recovered concentration should be close to the value used to construct the unknown spectrum. These checks connect mathematical operations to physical interpretation. They are especially useful when adapting a working example to a new file format, a different ordinate or a different integration interval.

## 8. Bring the spectrum back to the material question

Return to the transparent films at the beginning. First identify the specimen state and sampling method: dry or hydrated, transmission or ATR, and comparable thickness or contact conditions. Next inspect the background, vertical-axis units and original curves. Compare combinations of bands with candidate structures. Only then extract the peak positions, shapes, areas or ratios that address the research question, using consistent processing and controls. This order connects the final number to a concrete sequence: light meets a specimen, molecular and optical properties shape the response, and a defined calculation summarizes that response.

For protein adsorption on a hydrogel surface, compare the uncoated substrate, treated substrate and a suitable protein reference while considering water and substrate contributions. For consumption of a functional group during polymerization, follow the corresponding spectral region over time and stabilize the sampling conditions or use a suitable internal reference. A band change becomes meaningful through its relationship to composition, reaction pathways and other observations. The experimental question determines which comparison is useful, rather than the most visually prominent peak determining the entire interpretation.

Infrared spectroscopy makes otherwise invisible molecular motion available as a measurable signal. Learning to read it does not begin with memorizing an exhaustive peak table. It begins with understanding which motions couple to light, how acquisition and sampling shape the observed curve, and what a processed quantity actually represents. Those habits transfer directly to the next chapter on Raman spectroscopy. There the observable is an energy change during light scattering, and the coupling rule changes, but the connection between molecular mechanism, instrument signal and interpretation remains central.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/S01.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [ESA: Space infrared astronomy comes of age](https://www.esa.int/Science_Exploration/Space_Science/Exploring_space/Space_infrared_astronomy_comes_of_age)

   Historical context for Herschel’s infrared discovery.
2. [OpenSpecy: package tutorial](https://www.openspecy.org/pkgdown/articles/sop.html)

   Open spectral file formats and preprocessing workflow.

   CC BY 4.0
3. [OpenSpecy: LDPE-in-soil example data](https://github.com/wincowgerDEV/OpenSpecy-package/blob/main/inst/extdata/ftir_ldpe_soil.asp)

   Measured LDPE-in-soil data, identified in the official library-builder tutorial, replotted and processed here; the original file is included.

   OpenSpecy contributors; CC BY 4.0; replotted and smoothed. https://github.com/wincowgerDEV/OpenSpecy-package/blob/main/LICENSE.md
4. [OpenSpecy: Build a Mini Reference Library](https://www.openspecy.org/pkgdown/articles/library-builder.html)

   Documented material labels, file identities and reference-library organization.

   CC BY 4.0
5. [Chemistry LibreTexts: The Harmonic Oscillator and Infrared Spectra](https://chem.libretexts.org/Courses/University_of_California_Davis/UCD_Chem_110A%3A_Physical_Chemistry__I/UCD_Chem_110A%3A_Physical_Chemistry_I_%28Larsen%29/Text/05%3A_The_Harmonic_Oscillator_and_the_Rigid_Rotor/5.05%3A_The_Harmonic_Oscillator_and_Infrared_Spectra)

   Further treatment of oscillators, transitions and infrared activity.
6. [Shimadzu: ATR penetration depth](https://www.shimadzu.co.uk/service-support/technical-support/ftir/faq/atr.html)

   Effects of wavelength, angle and refractive index on ATR depth scales.
7. [Bruker: Attenuated Total Reflectance](https://www.bruker.com/en/products-and-solutions/infrared-and-raman/ft-ir-routine-spectrometer/what-is-ft-ir-spectroscopy/atr-attenuated-total-reflectance.html)

   ATR geometry, interfacial fields and solid contact.
8. [Coblentz Society: Attenuated Total Reflection Spectroscopy](https://www.coblentz.org/field-guide/chapter9/)

   Further reading on ATR reflection, refractive-index dispersion and strong-band line shape.
9. [SciPy: savgol_filter](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html)

   Smoothing windows, polynomial degree and edge treatment.
