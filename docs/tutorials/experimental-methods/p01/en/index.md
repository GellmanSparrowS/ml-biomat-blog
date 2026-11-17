# DLS: Measuring particle size through Brownian motion

Source: https://ml-biomat.com/tutorials/experimental-methods/p01/en/
Language: en

Connect random motion and fluctuating light to hydrodynamic size, rare aggregates and different averages.

## Measuring particles that cannot be seen individually

A freshly prepared protein solution may look clear even after a small population of aggregates develops. A nanocarrier dispersion can likewise remain visually unchanged after transfer into buffer while its particles move more slowly. Dynamic light scattering, or DLS, uses that motion to investigate size. A laser illuminates the dispersion, a detector records fluctuations in scattered intensity, and their timescale yields a diffusion coefficient. That coefficient is then converted to a hydrodynamic diameter. The instrument does not photograph each particle boundary. Instead, the random motion of many particles contributes to an ensemble optical signal from which size-related information is inferred.

Hydrodynamic diameter is an equivalent size defined through motion and drag. Imagine an ideal sphere that diffuses at the same rate as the object in the same liquid at the same temperature. Its diameter is the object’s hydrodynamic diameter. Surface polymers, adsorbed layers, solvation and shape can all influence drag, so this size need not equal a dried core width in a microscope image. Moving through a crowd in a bulky coat offers an analogy: the coat changes how motion interacts with the surroundings. The equivalent diameter is nevertheless not a rigid outline drawn around every solvated molecule. Soft layers and surrounding liquid may interpenetrate; the measurement summarizes their effect on translational motion.

This definition determines useful applications. DLS can compare dispersion states, detect slower-diffusing contributions in a protein preparation, examine changes following surface modification and assess consistency between relatively narrow particle populations. For rods, sheets or soft networks, one diameter summarizes a particular motion-related property, while imaging supplies complementary shape information. Sedimentation, convection or rapid transformation adds motion beyond ordinary Brownian diffusion. Establishing the specimen and measurand first helps select the appropriate result rather than allowing the largest number in a software report to define the research question. A hydrodynamic value is most informative when its medium and analysis are stated alongside it.

The chapter follows the instrument’s chain of reasoning. We first ask why small objects diffuse more rapidly, then why their movement makes scattered light fluctuate and how a correlation curve becomes a diameter. A deliberately constructed mixture shows why a very small number of larger objects can contribute strongly to the optical signal. Sample preparation, viscosity and concentration checks then connect the model to laboratory decisions. The complete example starts from constructed photon counts and reconstructs their correlation, preserving the intermediate evidence. By the end, a reported diameter should be understandable together with its signal, physical environment and averaging convention, rather than as an isolated property attached permanently to a particle.

## From Brown’s observations to a quantitative random walk

In the nineteenth century, botanist Robert Brown observed persistent irregular motion of small suspended particles. The effect does not require living objects. Molecules of the surrounding liquid exchange momentum through thermal motion, and their actions on a small particle do not cancel perfectly over short intervals. In the early twentieth century, Einstein and Smoluchowski developed testable statistical descriptions, while Perrin connected molecular ideas to observations of colloids. His 1926 Nobel lecture discussed particle displacements and emulsion distributions. The intellectual advance was to stop demanding a prediction of every turn and instead identify relations shared by many random trajectories. Modern DLS applies that statistical viewpoint through a different measurement channel.

A particle can move left or right, so averaging signed displacement often gives a result close to zero. That does not mean it stayed still. Squaring displacement before averaging retains a measure of the explored distance and gives positive contributions from both directions. In two dimensions, horizontal and vertical mean squared displacements each grow linearly with elapsed time; their sum gives the relationship below. The diffusion coefficient has units of area divided by time, rather than velocity. Brownian motion has no persistent forward direction, so describing diffusion as meters traveled per second would confuse a statistical spreading law with directed motion.

$$
\left\langle [x(t)-x(0)]^2+[y(t)-y(0)]^2\right\rangle=4Dt
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3b231539d50d3e8aaff9e854.svg) | Two-dimensional coordinates, m. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Elapsed time, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | Translational diffusion coefficient, m²/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/e0e6630a6cb958dd089f42cf.svg) | Average over independent displacements; 2048 paths in this simulation. |

For isotropic drift-free two-dimensional Brownian diffusion, each coordinate contributes 2Dt. D=6.1343277 μm²/s and t=0.3 s give 7.36119 μm². Its square root 2.71 μm is a displacement scale, not path length.

![Original numerical illustration connecting Brown’s observations to statistical work by Einstein, Smoluchowski and Perrin; not historical measured paths. 25 °C, viscosity 0.890 mPa·s, 2048 two-dimensional paths per size, 0.001 s steps. Solid: sample mean; dashed: theory 4Dt.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/f60d4ab96b1931e60dd2befc.svg?v=f60d4ab96b19)

Figure 1Original numerical illustration connecting Brown’s observations to statistical work by Einstein, Smoluchowski and Perrin; not historical measured paths. 25 °C, viscosity 0.890 mPa·s, 2048 two-dimensional paths per size, 0.001 s steps. Solid: sample mean; dashed: theory 4Dt.

The left panel shows one constructed two-dimensional path for each of two particle sizes during the same 0.3-second interval. The right panel averages 2048 independent paths per size. One path may wander unusually far or repeatedly double back; averaging reveals the reproducible difference between 80 nm and 240 nm particles. Dashed lines are theoretical expectations rather than straightened individual paths. For the liquid and temperature used here, the 80 nm sphere has a diffusion coefficient near 6.134 μm²/s and an expected two-dimensional mean squared displacement of 7.361 μm² after 0.3 seconds. Its square root, about 2.71 μm, is a statistical displacement scale, not the total length of the irregular route.

The Stokes–Einstein relation connects diffusion to size. Thermal energy scales with absolute temperature, while viscosity and sphere diameter determine drag in the corresponding fluid model. Tripling diameter at fixed temperature and viscosity reduces diffusion by a factor of three. Doubling viscosity likewise halves diffusion. Dilute, near-equilibrium specimens dominated by Brownian motion provide a straightforward setting for this conversion. Particle interactions in concentrated dispersions, viscoelastic media and complex boundary conditions can require additional physical descriptions. Calling the result an equivalent hydrodynamic diameter keeps the measured diffusion and the assumed drag model connected. It also explains why changing a solvent can alter motion even when the particle’s solid core remains unchanged.

$$
D=\frac{k_BT}{3\pi\eta d_H},\qquad d_H=\frac{k_BT}{3\pi\eta D}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | Translational diffusion coefficient, m²/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/2600a50cd45c9994bcd80b30.svg) | Boltzmann constant, 1.380649×10⁻²³ J/K. |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | Absolute temperature, K. |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | Dynamic viscosity of the medium, Pa·s. |
| ![Formula](https://ml-biomat.com/static/agent-math/3b6a97fbe00a64ed7f5753e9.svg) | Equivalent-sphere hydrodynamic diameter, m. |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | Circle constant, dimensionless. |

Thermal motion related to spherical Stokes drag under the corresponding continuum-fluid and Brownian conditions. T=298.15 K, η=0.000890 Pa·s, dH=80×10⁻⁹ m give D≈6.13433×10⁻¹² m²/s. A 240 nm sphere in the same medium has one third that diffusion coefficient.

## Moving particles change the interference of scattered waves

The historical-principle figure illustrates trajectories, but DLS does not directly output those coordinates. Suitable microscopy can track individual visible particles, while correlation measurements conveniently assess ensemble diffusion of nanoscale objects. Both connect to diffusion, yet their detection weights, sampled objects and resolution differ. Comparing a tracking-derived number distribution with a DLS intensity distribution therefore requires attention to the measured quantity. Complementary methods need not produce identical histograms to provide mutually useful information about the same specimen.

Laser light supplies a stable phase relationship to the incident field. Many particles scatter waves toward the detector, where their amplitudes combine. Some positional arrangements favor reinforcement, while others produce partial cancellation. A small particle displacement changes path lengths and phases, so the interference pattern evolves and the detected intensity fluctuates. This is not simply a sequence of individual particles entering a beam and producing separate flashes. Many scattered waves contribute simultaneously. The changing pattern carries information about how rapidly the configuration loses memory of its earlier arrangement, even when individual particle outlines remain unresolved.

Imagine watching an unresolved collection of reflecting points through a translucent screen. The detailed positions may be hidden, yet the overall bright and dark pattern changes. Faster rearrangement generally means shorter memory of the original pattern. An autocorrelation function quantifies this idea by pairing an intensity record with a delayed copy, multiplying paired values and averaging over many starting times. At short delays, a bright moment is likely to remain relatively bright, giving an elevated average product. At sufficiently long delays, the two intensities become approximately independent and their product approaches the square of the mean intensity. Normalization by that mean-square quantity sets the long-delay baseline near one.

$$
g_2(\tau)=\frac{\langle I(t)I(t+\tau)\rangle}{\langle I\rangle^2}=1+\beta|g_1(\tau)|^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/60518fc66e22af7805986728.svg) | Normalized intensity autocorrelation, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/9b4a2d5741b5fa9e74f2c3b8.svg) | Detected intensity or counts in equal bins; use consistent units in numerator and denominator. |
| ![Formula](https://ml-biomat.com/static/agent-math/665d0053bb3deb2475f4a302.svg) | Acquisition time and delay time, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/e0e6630a6cb958dd089f42cf.svg) | Average over starting times in a stationary record. |
| ![Formula](https://ml-biomat.com/static/agent-math/f27acf6959fc15846a7239da.svg) | Coherence factor governed by collection optics and mode averaging, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/3b22342888bb056c49f5396e.svg) | Normalized field correlation, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/bc92b5f15067fde73c490894.svg) | Magnitude of a complex quantity. |

Right side is the Siegert relation for the applicable Gaussian scattered-field statistics. Two independent modes give β=0.5. Ideal zero-delay field correlation 1 gives g2=1.5; long-delay g1→0 gives g2→1. Photon counts add a zero-lag shot-noise term, excluded from fitting.

![Constructed scattering from 80 nm spheres, seed 810, 633 nm, 90°, medium index 1.333. Two independent complex Gaussian modes plus Poisson counts; 1048576 bins of 2 μs. Display: first 10 ms; correlation uses full record. Fit delays ≤6 ms, excluding zero lag. Panel D includes all displayed delays.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/7a7f3e47d71758ac78dccfe7.svg?v=7a7f3e47d717)

Figure 2Constructed scattering from 80 nm spheres, seed 810, 633 nm, 90°, medium index 1.333. Two independent complex Gaussian modes plus Poisson counts; 1048576 bins of 2 μs. Display: first 10 ms; correlation uses full record. Fit delays ≤6 ms, excluding zero lag. Panel D includes all displayed delays.

Different software displays use different conventions. A normalized intensity correlation approaches one; subtracting one moves the baseline to zero; converting to field correlation gives another function again. The figure uses constructed photon counts from two independent optical modes with Poisson detection fluctuations. Only the first ten milliseconds are displayed to make temporal structure visible, whereas the correlation calculation uses the complete record of approximately 2.10 seconds. This duration belongs to a reproducible teaching model rather than a universal acquisition recommendation. Real acquisition should resolve the relevant relaxation and establish repeatability for the specimen and instrument configuration.

The coherence factor describes how collection optics and mode averaging affect the correlation amplitude. Two equally weighted independent modes give an ideal amplitude of 0.5 in this model; the finite-record fit returns about 0.489. That value does not mean half the particles moved. Photon counts also contain a special zero-delay contribution from counting noise, so the program excludes zero lag from the fit. Actual detectors may introduce afterpulsing, background or drift that requires inspection of short- and long-delay regions. Reading amplitude, baseline and decay time separately prevents every change in a correlation curve from being interpreted as a size change. These features describe different parts of the measurement chain and can respond differently to sample or instrument conditions.

## The steps between a decay time and a diameter

For dilute, identical, approximately spherical particles undergoing translational Brownian diffusion, field correlation decays exponentially with delay. The decay rate depends on diffusion and on observation geometry. Laser wavelength, liquid refractive index and scattering angle determine the magnitude of the scattering vector. This vector describes the spatial scale at which position changes affect the scattering measurement. Changing angle changes the correlation timescale for the same particles, while applying the correct geometry recovers the corresponding diffusion coefficient. Comparing the horizontal positions of curves from different instruments without checking angle can therefore mistake an optical change for a particle change.

$$
g_1(\tau)=e^{-\Gamma\tau},\qquad\Gamma=Dq^2,\qquad q=\frac{4\pi n}{\lambda_0}\sin\frac{\theta}{2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3b22342888bb056c49f5396e.svg) | Field correlation of one diffusive component, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | Delay time, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/b5919a287af415ef85d8991d.svg) | Field-correlation decay rate, s⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | Translational diffusion coefficient, m²/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | Scattering-vector magnitude, m⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Liquid refractive index at the laser wavelength, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/0a322167c6031b3ba1406fb9.svg) | Vacuum laser wavelength, m. |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | Angle between incident and scattered directions; use radians in the sine. |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | Circle constant. |

Dilute single-size translational Brownian model. 633 nm, n=1.333, θ=90° give q≈1.8712×10⁷ m⁻¹. The 80 nm model has D≈6.13433×10⁻¹² m²/s and Γ≈2148 s⁻¹. Excess intensity correlation decays as exp(−2Γτ), retaining the factor 2.

The example uses a vacuum wavelength of 633 nm, liquid refractive index 1.333, a ninety-degree scattering angle and temperature of 25 °C. These give a scattering-vector magnitude near 1.8712×10⁷ m⁻¹. The program fits the intensity correlation calculated from photon counts, divides the fitted decay rate by the squared scattering vector to obtain diffusion, then applies the correct viscosity to calculate diameter. The prescribed particle diameter is 80 nm; this finite record gives approximately 80.90 nm. The difference illustrates how sampling enters the estimate. Longer records and repeated measurements can investigate stability, whereas extra decimal places printed by a fitting routine do not establish experimental precision.

Why does the intensity-correlation exponential contain a factor of two that is absent from field correlation? The detector measures intensity. Under the relevant scattering-statistical conditions, intensity correlation above baseline is proportional to the squared magnitude of field correlation. Squaring an exponential doubles its exponent. Treating intensity correlation directly as field correlation therefore introduces a factor-of-two error into diffusion and diameter conversion. This apparently small algebraic detail reflects a fundamental distinction between measured quantities. Before fitting an exported file, identify whether it contains normalized intensity correlation, baseline-subtracted intensity correlation or a transformed field quantity, and preserve the stated time units.

Inspect residuals as well as the fitted curve. A residual is data minus model; systematic structure may indicate that a single exponential misses part of the signal, or that background and drift need attention. Correlation points at neighboring delays reuse the same photon record, so their errors are generally correlated. Formal uncertainty from ordinary least squares is not equivalent to variability among independently prepared specimens. Here fitting reconstructs a known constructed model and retains a residual plot. Laboratory interpretation should additionally compare repeated records, loading replicates and reasonable fitting regions. These checks connect uncertainty to the actual experimental level at which variation occurs, rather than assigning every source of variation to one fitted standard error.

## A few larger particles can contribute much of the light

If everyone spoke equally loudly, the fraction of sound from a group might roughly track its fraction of people. A few people using loudspeakers would change that relationship. Small-particle scattering has a comparable imbalance. For homogeneous spheres of the same optical contrast in the Rayleigh regime, where particle dimensions are sufficiently small relative to wavelength, single-particle scattering intensity scales as diameter to the sixth power. Tripling diameter increases the contribution by a factor of 729. This scaling belongs to its optical approximation. Once dimensions approach the wavelength, angular structure and material properties require a more complete scattering description; the sixth-power rule is not a universal law for arbitrarily large particles.

$$
w_i=\frac{N_i d_i^6}{\sum_jN_jd_j^6},\qquad g_1(\tau)=\sum_iw_i e^{-\Gamma_i\tau}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cec5f0994a4bad5c3ac4a9a4.svg) | Scattered-intensity fraction of population i, dimensionless, summing to 1. |
| ![Formula](https://ml-biomat.com/static/agent-math/2e48d6441cb55e92796c4f28.svg) | Particle counts or consistently normalized number fractions. |
| ![Formula](https://ml-biomat.com/static/agent-math/c3bf1aa96ca6a8b183630c1e.svg) | Corresponding homogeneous-sphere diameters in consistent length units. |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | Population indices. |
| ![Formula](https://ml-biomat.com/static/agent-math/3b22342888bb056c49f5396e.svg) | Mixture field correlation, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/7cb77d3624bf5ffc46257fb9.svg) | Decay rate of population i, s⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | Delay time, s. |

Rayleigh approximation for equal-contrast homogeneous spheres, single scattering and independent diffusion. 10 and 30 nm with number fractions 0.999 and 0.001 give large-particle weight 0.001×729/(0.999+0.001×729)=0.421875. Sixth-power weighting is not a universal large-particle scattering model.

The constructed mixture contains 99.9% particles of 10 nm diameter and only 0.1% particles of 30 nm diameter, with equal optical contrast. The larger particles nevertheless contribute about 42.19% of total scattered intensity. The number-average diameter is 10.02 nm, the intensity-weighted arithmetic diameter is 18.44 nm, and the z-average inferred from the initial correlation decay is about 13.91 nm. All three arise from the same explicit model. Their difference is the averaging rule, not a numerical contradiction. Reporting number mean, distribution peak or z-average by name is therefore essential when comparing techniques or software outputs.

![Constructed homogeneous equal-contrast spheres, 10 and 30 nm, number fractions 99.9% and 0.1%, using Rayleigh sixth-power weights. PDI is normalized decay-rate variance. C fits a second-order expansion of noiseless log field correlation to expose truncation error, not instrument performance.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/3c4a18f2b3ebc01a76c995ef.svg?v=3c4a18f2b3eb)

Figure 3Constructed homogeneous equal-contrast spheres, 10 and 30 nm, number fractions 99.9% and 0.1%, using Rayleigh sixth-power weights. PDI is normalized decay-rate variance. C fits a second-order expansion of noiseless log field correlation to expose truncation error, not instrument performance.

The z-average starts with the intensity-weighted mean decay rate, converts that to diffusion and finally converts diffusion to diameter. For spheres in the same environment, this produces a harmonic intensity average of diameter rather than its arithmetic intensity average. Cumulant analysis also measures departure from a single exponential through the relative variance of decay rates, giving the DLS polydispersity index, PDI. This PDI differs from the molar-mass dispersity used in size-exclusion chromatography and is not the fraction of unacceptable particles. It summarizes distribution breadth without automatically specifying how many separate size populations exist. The equation below makes the weighting and the measured rate distribution explicit.

$$
\begin{aligned}\bar\Gamma&=\sum_iw_i\Gamma_i,\quad\mu_2=\sum_iw_i(\Gamma_i-\bar\Gamma)^2\\\mathrm{PDI}&=\frac{\mu_2}{\bar\Gamma^2},\quad d_z=\left(\sum_i\frac{w_i}{d_i}\right)^{-1}\\\ln g_1(\tau)&\simeq-\bar\Gamma\tau+\frac{\mu_2\tau^2}{2}\end{aligned}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a3181f4c55adf168086b94ad.svg) | Intensity-weighted mean and population decay rates, s⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/cec5f0994a4bad5c3ac4a9a4.svg) | Population intensity fractions, dimensionless, summing to 1. |
| ![Formula](https://ml-biomat.com/static/agent-math/a21f07d3948532bb6aa91995.svg) | Variance of decay-rate distribution, s⁻². |
| ![Formula](https://ml-biomat.com/static/agent-math/018a3249e5c08bf1bcdc9076.svg) | DLS polydispersity index, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/8ce6179638f66a34b72be421.svg) | z-average and population hydrodynamic diameters, consistent length units. |
| ![Formula](https://ml-biomat.com/static/agent-math/7af7845460cf4b819947dd4b.svg) | Field correlation(dimensionless) and delay time(s). |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Population index. |

Common medium, temperature and geometry; harmonic size follows Γ proportional to 1/d. The 10/30 nm example gives dz=13.9130 nm and PDI≈0.20983, versus number mean 10.02 nm and intensity arithmetic mean 18.4375 nm. Final expression is a second-order short-delay cumulant expansion; longer delays require higher terms. It does not recover two physical peaks automatically.

The mixture’s correlation is smooth, yet it differs from a single exponential with the same initial rate. A truncated cumulant expansion fitted over different delay windows gives different estimates because omitted higher terms become more influential. Distribution algorithms attempt to recover more detail through sums of exponentials, but similar exponentials can compensate for one another. Small uncertainties can consequently produce large changes in recovered peak shapes. Two sharp software peaks deserve checks across repeated records and reasonable analysis settings, followed by complementary evidence when their identities matter. Splitting a broad curve into additional peaks does not create information that the measurement never resolved.

## How do rare large particles and one input field change size?

Constructed equal-contrast 10 and 30 nm spheres, 25 °C, 633 nm, 90°. Change the larger-particle number fraction, then actual and entered viscosity separately. The curve uses actual viscosity; reported diameter uses the entered value.

[Figure: Mixture correlation and viscosity conversion](https://ml-biomat.com/tutorials/experimental-methods/p01/en/#P01-plot)

The interactive experiment separates the number fraction of larger particles from actual and entered viscosity. First keep both viscosities equal and add a small fraction of 30 nm particles. Observe the correlation tail, z-average and PDI together. Then hold composition fixed and change only the software viscosity input. The correlation remains unchanged while the reported diameter changes. The first operation changes the scattering specimen; the second changes its numerical interpretation. Distinguishing these causes is fundamental when using a size trend to explain a biological or materials result. It also provides a useful way to diagnose an unexpected shift before proposing a structural mechanism.

## The liquid and sample preparation belong to the measurement

Biological media introduce another practical issue: light does not identify which component is the research target. Serum proteins, micelles, medium particulates and added carriers can all scatter. A medium blank is informative, but two normalized correlation curves generally cannot be subtracted as though they were separate mass contributions. Normalization and the field-to-intensity relation are nonlinear, and components may interact through adsorption. Appropriate separation, labeled imaging or additional controls can connect a slow contribution to the carrier. An extra fitted peak alone does not assign molecular identity, even if its apparent size seems plausible.

Viscosity often changes substantially with temperature. The public NIST protocol lists pure-water viscosities of 1.002, 0.890 and 0.692 mPa·s at 20, 25 and 37 °C. In the figure, a hypothetical particle remains 80 nm while its physical diffusion follows the correct temperature and viscosity. If temperature is entered correctly but the analysis always uses the 25 °C viscosity, it reports about 90.07 nm at 20 °C and 62.20 nm at 37 °C. An apparent temperature-responsive size change has been produced entirely by an incorrect input. Real responsive particles may shrink or swell, but accounting for liquid properties is necessary to separate structural changes from the conversion itself.

![A retains pure-water viscosity values from Hackley and Clogston, NIST SP1200-6, p. 9. B computes an unchanged 80 nm particle with correct temperature but a fixed erroneous viscosity input 0.890 mPa·s. C is a conceptual hydrodynamic-equivalence diagram, not to scale.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/229a593ce519a3e38b418bb2.svg?v=229a593ce519)

Figure 4A retains pure-water viscosity values from Hackley and Clogston, NIST SP1200-6, p. 9. B computes an unchanged 80 nm particle with correct temperature but a fixed erroneous viscosity input 0.890 mPa·s. C is a conceptual hydrodynamic-equivalence diagram, not to scale.

Refractive index also has two distinct roles. The medium’s refractive index enters the scattering vector and therefore the conversion from decay rate to diffusion. The particle refractive index mainly enters an optical model when an intensity distribution is transformed into volume or number distributions. That transformation additionally assumes shape, absorption and composition. Clicking number distribution does not make the instrument count particles individually. Media containing substantial protein, sugar or salt may require properties other than those of pure water. After temperature equilibration, inspect for convection, evaporation and sedimentation so that the recorded fluctuations describe a reasonably stationary dispersion rather than a progressively changing specimen.

Dust and occasional large contaminants can contribute strong scattering, making clean cells, covered specimens, bubble checks and medium blanks valuable. Filtration, however, can change the object being studied. A membrane may adsorb protein, retain aggregates that are part of the research question or alter soft particles. If the question concerns aggregation in an untreated preparation, filtered and unfiltered material should be treated as different specimen states. If the aim is to characterize an isolated narrow population, specify the preparation that produced it. Recovery, concentration checks and complementary imaging can establish the effect of treatment more meaningfully than judging success solely by a smoother correlation curve.

Low concentration weakens analyte scattering relative to background and rare contaminants. High concentration can introduce multiple scattering and particle interactions that change apparent diffusion. A dilution series using composition-matched medium helps identify a region with consistent size, correlation quality and count behavior. Adding pure water alone may simultaneously change salt, pH and adsorption equilibria, altering the particles themselves. Dilution can also shift reversible protein association or self-assembly. Such concentration dependence may be scientifically informative rather than an inconvenience to remove. Design the comparison around that possibility instead of selecting the one concentration that produces the expected diameter. The resulting analysis distinguishes optical concentration effects from genuine changes in molecular or colloidal equilibrium.

## Keep the correlation so that the size remains interpretable

Appropriate reference particles test whether the instrument and procedure behave as expected. Check the measurement definition, medium and temperature associated with a reference value before comparing mean and repeatability. A nominal hundred-nanometer label does not require exactly one hundred under every medium and averaging convention. Reference dispersions also age or aggregate. DLS has a physical basis for conversion; reference material verifies the combined optical, thermal, cell and analysis chain rather than supplying an arbitrary factor that forces unknown specimens toward a preferred size.

When distribution software requests smoothness or regularization settings, it is balancing agreement with noisy correlation data against restrictions on the recovered distribution. A smoother answer can suppress unstable fine structure, while weak restrictions may produce narrow peaks that shift between records. Preserve the settings and compare changes that matter to the scientific interpretation. A stable overall mean alongside unstable fine peaks suggests that the measurement supports an ensemble statement more strongly than a detailed population assignment. That distinction guides whether further separation or imaging would add useful information.

The complete program first simulates two-dimensional Brownian paths and checks mean squared displacement. It then constructs complex fields for two independent scattering modes, converts them to intensity and generates Poisson photon counts. Correlation is calculated from the entire record, with zero-delay counting noise excluded from fitting. Diameter, amplitude, baseline and residuals are exported. A separate deterministic mixture compares number, volume and intensity weights and demonstrates sensitivity to a truncated cumulant fitting window. Finally, the program reads the bundled public water-viscosity table and calculates the size bias caused by an incorrect input. Published property values and constructed particle observations are identified separately in captions and outputs.

### Reconstruct size from Brownian paths and photon records

Runs paths, complex fields and photon counts, correlation, fitting, mixture weights, window diagnostics and viscosity-bias calculations, exporting all figures and data.

```
"""DLS: Brownian motion, photon correlation, mixtures and solvent inputs.

All particle traces are constructed. Bundled water viscosities are published
NIST SP1200-6 values, retained with attribution in data/README.txt.
Run: python main.py --output results --language en
"""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.signal import lfilter
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle

p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();O=args.output;O.mkdir(parents=True,exist_ok=True)
ZH=args.language=='zh'
def L(z,e):return z if ZH else e
plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.facecolor':'#fcfbf7','figure.facecolor':'#fcfbf7','svg.fonttype':'none','text.color':'#20333e','axes.labelcolor':'#20333e','axes.titleweight':'bold'})
B='#167d9a';R='#d35f47';G='#37967d';Y='#c49b35';K='#20333e'
def save(f,n):
 for e in ['svg','png']:f.savefig(O/f'{n}-{args.language}.{e}',dpi=145,bbox_inches='tight')
 plt.close(f)
def csv(n,heads,cols):np.savetxt(O/n,np.column_stack(cols),delimiter=',',header=','.join(heads),comments='',fmt='%.10g')
kB=1.380649e-23;TK=298.15;eta=.000890;nmed=1.333;wave=633e-9;theta=np.pi/2
q=4*np.pi*nmed/wave*np.sin(theta/2)
def diffusion(d_nm,visc=eta,T=TK):return kB*T/(3*np.pi*visc*d_nm*1e-9)
def diameter(D,visc=eta,T=TK):return kB*T/(3*np.pi*visc*D)*1e9
rng=np.random.default_rng(810);D80=diffusion(80);D240=diffusion(240)
dtpath=.001;tp=np.arange(301)*dtpath
paths={};msds={}
for d in [80,240]:
 step=rng.normal(size=(2048,300,2))*np.sqrt(2*diffusion(d)*dtpath)*1e6
 xy=np.concatenate([np.zeros((2048,1,2)),np.cumsum(step,axis=1)],axis=1);paths[d]=xy[:3];msds[d]=np.mean(np.sum(xy*xy,axis=2),axis=0)
csv('brownian_msd.csv',['time_s','msd80_um2','theory80_um2','msd240_um2','theory240_um2'],[tp,msds[80],4*D80*tp*1e12,msds[240],4*D240*tp*1e12])
fig,axs=plt.subplots(1,2,figsize=(12,5.2),layout='constrained')
a=axs[0]
for d,c in [(80,B),(240,R)]:
 xy=paths[d][0];a.plot(xy[:,0],xy[:,1],color=c,lw=1.3,label=f'{d} nm');a.scatter(*xy[-1],color=c,s=35)
a.scatter(0,0,color=K,marker='x',s=55);a.set(aspect='equal',xlabel=L('x 位移 / μm','x displacement / μm'),ylabel=L('y 位移 / μm','y displacement / μm'),title=L('A  相同 0.3 s，不同扩散尺度','A  Same 0.3 s, different diffusion scales'));a.legend(frameon=False)
a=axs[1]
for d,c in [(80,B),(240,R)]:a.plot(tp,msds[d],color=c,lw=2,label=L(f'{d} nm：2048 条轨迹',f'{d} nm: 2048 paths'));a.plot(tp,4*diffusion(d)*tp*1e12,color=c,ls='--',lw=1)
a.set(xlabel=L('经过时间 / s','Elapsed time / s'),ylabel=L('二维平均平方位移 / μm²','Two-dimensional mean squared displacement / μm²'),title=L('B  杂乱路径可以有清楚的统计规律','B  Irregular paths have a statistical law'));a.legend(frameon=False,fontsize=9)
fig.suptitle(L('从 Brown 的观察，到 Einstein、Smoluchowski 与 Perrin 的定量研究\n原创数值示意；不是历史测量轨迹','From Brown’s observations to Einstein, Smoluchowski and Perrin\nOriginal numerical illustration, not historical measured trajectories'),fontsize=11);save(fig,'brownian-history')

# Two independent complex Gaussian optical modes give coherence factor 1/2.
# Poisson counts model photon detection; the zero-lag shot-noise spike is excluded.
N=1048576;dt=2e-6;burn=8192;Gamma=D80*q*q;a=np.exp(-Gamma*dt);intensity=np.zeros(N)
for _ in range(2):
 noise=(rng.normal(size=N+burn)+1j*rng.normal(size=N+burn))*np.sqrt((1-a*a)/2)
 field=lfilter([1],[1,-a],noise)[burn:];intensity+=np.abs(field)**2/2
counts=rng.poisson(.8*intensity).astype(np.int16);center=counts-counts.mean();pad=1<<(2*N-1).bit_length()
fft=np.fft.rfft(center,pad);cov=np.fft.irfft(fft*np.conj(fft),pad)[:6001]/(N-np.arange(6001))
lags=np.unique(np.geomspace(1,6000,250).astype(int));tau=lags*dt;g2=1+cov[lags]/counts.mean()**2
def mono(t,beta,rate,base):return base+beta*np.exp(-2*rate*t)
mask=tau<=.006;fit,_=curve_fit(mono,tau[mask],g2[mask],p0=[.5,Gamma,1],bounds=([.05,1,.9],[1.5,1e6,1.1]),maxfev=20000)
beta_fit,rate_fit,base_fit=fit;dfit=diameter(rate_fit/q**2);fitted=mono(tau,*fit)
np.savez_compressed(O/'photon_counts.npz',counts=counts,bin_seconds=dt,diameter_nm=80,seed=810)
csv('correlation.csv',['delay_s','g2_from_counts','single_exponential_fit','fit_residual'],[tau,g2,fitted,g2-fitted])
block=25;preview=counts[:5000].reshape(-1,block).sum(axis=1);tprev=(np.arange(preview.size)+.5)*block*dt
csv('photon_preview.csv',['time_s','counts_per50us'],[tprev,preview])
fig,axs=plt.subplots(2,2,figsize=(12,8.6),layout='constrained')
ax=axs[0,0];ax.axis('off');ax.set(xlim=(0,10),ylim=(0,7));ax.set_title(L('A  接收一个方向的散射波动','A  Collect fluctuations in one direction'))
ax.add_patch(Rectangle((.3,2.4),1.8,1.2,fc=R,alpha=.8));ax.text(1.2,3,L('激光','Laser'),ha='center',va='center',color='white');ax.add_patch(Rectangle((4,1.7),2,2.7,fc='#d9e9e8',ec=B));ax.text(5,1.1,L('样品池','Cuvette'),ha='center');ax.annotate('',xy=(4.8,3),xytext=(2.1,3),arrowprops={'arrowstyle':'->','lw':2,'color':R});ax.plot([5,8.8],[3,3],ls='--',color='#8d9ba3');ax.annotate('',xy=(5,5.6),xytext=(5,3),arrowprops={'arrowstyle':'->','lw':2,'color':B});ax.add_patch(Rectangle((4,5.7),2,1,fc=B));ax.text(5,6.2,L('探测器','Detector'),ha='center',va='center',color='white');ax.text(5.4,3.5,'90°',color=B);ax.text(7.3,2,L('干涉随位置改变\n记录光子数随时间变化','Positions change interference\nRecord photons versus time'),ha='center',fontsize=9)
ax=axs[0,1];ax.plot(tprev*1e3,preview,color=B,lw=1);ax.set(xlabel=L('记录时间 / ms','Acquisition time / ms'),ylabel=L('每 50 μs 的光子数','Photons per 50 μs'),title=L('B  同一构造记录的前 10 ms','B  First 10 ms of the constructed record'))
ax=axs[1,0];ax.semilogx(tau*1e6,g2,'o',ms=3,color='#9bb9c0',label=L('由光子记录计算','Computed from photon record'));ax.semilogx(tau*1e6,fitted,color=R,lw=2,label=L(f'拟合直径 {dfit:.2f} nm',f'Fitted diameter {dfit:.2f} nm'));ax.set(xlabel=L('延迟时间 τ / μs','Delay time τ / μs'),ylabel='g₂(τ)',title=L('C  相关曲线衰减到约 1','C  Correlation decays toward about 1'));ax.legend(frameon=False,fontsize=9)
ax=axs[1,1];ax.semilogx(tau*1e6,g2-fitted,color=B);ax.axhline(0,color=K,lw=.8);ax.set(xlabel=L('延迟时间 τ / μs','Delay time τ / μs'),ylabel=L('数据 − 拟合','Data − fit'),title=L('D  残差保留有限采样的起伏','D  Residuals retain finite-record fluctuations'));save(fig,'photon-correlation')

# Ideal Rayleigh mixture: homogeneous spheres of the same optical contrast.
ds=np.array([10.,30.]);num=np.array([.999,.001]);w=num*ds**6;w/=w.sum();rates=np.array([diffusion(d)*q*q for d in ds]);meanrate=np.dot(w,rates);variance=np.dot(w,(rates-meanrate)**2);PDI=variance/meanrate**2;z=diameter(meanrate/q**2)
tmix=np.geomspace(1e-7,.003,450);g1=np.exp(-tmix[:,None]*rates)@w;gmix=1+.5*g1*g1
cuts=np.array([.15,.3,.6,1.,1.5]);winz=[];winp=[]
for cut in cuts:
 m=tmix*meanrate<=cut;coef=np.polyfit(tmix[m]*meanrate,np.log(g1[m]),2);gr=-coef[1]*meanrate;mu2=2*coef[0]*meanrate**2;winz.append(diameter(gr/q**2));winp.append(mu2/gr**2)
csv('mixture.csv',['delay_s','field_correlation','intensity_correlation','matched_first_cumulant_g2'],[tmix,g1,gmix,1+.5*np.exp(-2*meanrate*tmix)])
csv('cumulant_window.csv',['maximum_scaled_delay','fitted_z_nm','fitted_PDI'],[cuts,winz,winp])
fig,axs=plt.subplots(2,2,figsize=(12,8.2),layout='constrained')
ax=axs[0,0];weightings=[num,num*ds**3/(num*ds**3).sum(),w];lab=L(['数量','体积','光强'],['Number','Volume','Intensity'])
for i,ww in enumerate(weightings):ax.barh(i,100*ww[0],color=B);ax.barh(i,100*ww[1],left=100*ww[0],color=R);ax.text(101,i,f'{100*ww[1]:.2f}%',va='center',fontsize=9)
ax.set(yticks=range(3),yticklabels=lab,xlim=(0,122),ylim=(-.5,3.1),xlabel=L('各类比例 / %','Fraction on each basis / %'),title=L('A  30 nm 颗粒只占数量的 0.1%','A  30 nm particles are only 0.1% by number'));ax.text(1,2.73,L('蓝：10 nm；红：30 nm','Blue: 10 nm; red: 30 nm'),fontsize=9)
ax=axs[0,1];ax.semilogx(tmix*1e6,gmix,color=B,lw=2,label=L('双粒径混合物','Two-size mixture'));ax.semilogx(tmix*1e6,1+.5*np.exp(-2*meanrate*tmix),color=R,ls='--',label=L('同一初始衰减率的单指数','Single exponential, same initial rate'));ax.set(xlabel=L('延迟时间 / μs','Delay time / μs'),ylabel='g₂(τ)',title=L('B  一条平滑曲线里可以藏着混合物','B  A smooth curve can conceal a mixture'));ax.legend(frameon=False,fontsize=8)
ax=axs[1,0];ax.plot(cuts,winz,'o-',color=B);ax.axhline(z,color=R,ls='--',label=L('精确初始矩','Exact initial moment'));ax.set(xlabel=L('拟合窗上限 Γ̄τ','Fit-window upper limit Γ̄τ'),ylabel=L('二阶展开给出的直径 / nm','Diameter from second-order expansion / nm'),title=L('C  截断展开依赖拟合区间','C  Truncated expansion depends on its window'));ax.legend(frameon=False,fontsize=9)
ax=axs[1,1];means=[np.dot(num,ds),z,np.dot(w,ds)];ax.bar(L(['数量均值','z 均值','光强算术均值'],['Number mean','z-average','Intensity arithmetic']),means,color=[G,B,R]);ax.set(ylabel=L('直径 / nm','Diameter / nm'),ylim=(0,24),title=L('D  三个“平均”回答不同问题','D  Three averages answer different questions'))
for j,v in enumerate(means):ax.text(j,v+.5,f'{v:.3f}',ha='center')
save(fig,'mixture-weighting')

tab=np.genfromtxt(Path(__file__).parent/'data/water_viscosity.csv',delimiter=',',names=True);temps=tab['temperature_C'];viscosities=tab['viscosity_mPa_s'];dapp=80*viscosities/.890
csv('viscosity_bias.csv',['temperature_C','published_viscosity_mPa_s','true_diameter_nm','inferred_with_fixed0890_nm'],[temps,viscosities,np.full(3,80),dapp])
fig,axs=plt.subplots(1,3,figsize=(14,4.8),gridspec_kw={'width_ratios':[1,1.1,1]},layout='constrained')
ax=axs[0];ax.plot(temps,viscosities,'o-',color=B);ax.set(xlabel=L('温度 / °C','Temperature / °C'),ylabel=L('水的黏度 / mPa·s','Water viscosity / mPa·s'),title=L('A  公开的水黏度数值','A  Published water viscosities'));ax.text(20.2,.72,'NIST SP1200-6, p.9',fontsize=9)
ax=axs[1];ax.plot(temps,dapp,'o-',color=R,label=L('误用固定 0.890 mPa·s','Fixed0.890 mPa·s input'));ax.axhline(80,color=B,ls='--',label=L('正确黏度：80 nm','Correct viscosity:80 nm'));ax.set(xlabel=L('真实温度 / °C','Actual temperature / °C'),ylabel=L('推算直径 / nm','Inferred diameter / nm'),ylim=(55,100),title=L('B  颗粒没变，错误输入制造变化','B  Wrong inputs create a size change'));ax.legend(frameon=False,fontsize=8)
ax=axs[2];ax.set(xlim=(-1.6,1.6),ylim=(-1.7,1.7),aspect='equal');ax.axis('off');ax.add_patch(Circle((0,.25),1.05,fc='#d9e9e8',ec=B,ls='--',lw=2));ax.add_patch(Circle((0,.25),.65,fc=Y,ec=K));ax.text(0,.25,L('核心','Core'),ha='center',va='center');ax.text(0,-1.18,L('溶剂化与表面层影响阻力\n水动力等效边界不是硬壳','Solvation and surface layers affect drag\nHydrodynamic equivalence is not a rigid shell'),ha='center',fontsize=9);ax.set_title(L('C  扩散测的是带环境的颗粒','C  Diffusion includes the environment'));save(fig,'viscosity-measurand')
summary={'data_kind':'constructed particle traces; published water-viscosity values','seed':810,'temperature_K':TK,'viscosity_Pa_s':eta,'q_per_m':float(q),'diffusion80_m2_per_s':float(D80),'diffusion240_m2_per_s':float(D240),'diffusion_size_ratio':float(D80/D240),'two_dimensional_msd80_at03s_um2':float(4*D80*.3*1e12),'photon_record_seconds':N*dt,'photon_mean_count_per_bin':float(counts.mean()),'fitted_diameter_nm':float(dfit),'fitted_coherence':float(beta_fit),'fitted_baseline':float(base_fit),'mixture_large_number_percent':.1,'mixture_large_intensity_percent':float(w[1]*100),'mixture_number_mean_nm':float(np.dot(num,ds)),'mixture_z_average_nm':float(z),'mixture_intensity_arithmetic_nm':float(np.dot(w,ds)),'mixture_PDI':float(PDI),'wrong_viscosity_diameter_at20C_nm':float(dapp[0]),'wrong_viscosity_diameter_at37C_nm':float(dapp[-1]),'published_water_viscosity25_mPa_s':float(viscosities[1])}
assert abs(D80/D240-3)<1e-12
assert abs(w[1]-.421875)<1e-12
assert abs(z-320/23)<1e-10
assert abs(summary['mixture_number_mean_nm']-10.02)<1e-12
assert 74<dfit<86 and .9<base_fit<1.1
assert abs(dapp[-1]-80*.692/.890)<1e-12
(O/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary,ensure_ascii=False,indent=2))
```

The full photon sequence is retained in a compressed data file alongside correlation tables, mixture results and pointwise figure data. To connect this workflow to an instrument export, first identify the correlation convention and time unit, preserve the original file and replace the corresponding input step. A baseline-subtracted function should not be fitted again as though its baseline were one. Replicate design also matters: consecutive acquisitions in one cell, fresh cell loading and independently prepared batches address progressively different sources of variation. The first mostly tests short-term repeatability; the latter introduce handling and preparation variability. Report the level relevant to the question rather than treating all repeated numbers as interchangeable evidence.

A useful result presents medium, concentration, temperature, viscosity, angle and wavelength together with z-average, PDI, replicate count, variation and representative correlation curves. A slow tail in a protein specimen can motivate comparison of fresh and stored material, separated fractions and independent structural observations. A size change after surface modification invites examination of aggregation and altered solvation or surface-layer drag as separate explanations. DLS describes particles in motion within a liquid environment. Connecting that definition to complementary measurements turns a nanometer value into a research conclusion that supports the next experiment, while preserving what the optical signal actually measured.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/P01.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Perrin: Nobel Lecture, Discontinuous Structure of Matter (1926)](https://www.nobelprize.org/prizes/physics/1926/perrin/lecture/)

   History of Brownian motion, displacement statistics and colloid experiments.
2. [Hackley & Clogston: NIST SP1200-6, Batch-Mode DLS (2015)](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1200-6.pdf)

   Specimens, concentration, medium parameters, reporting and water viscosities on p. 9.

   Published numerical water-property facts retained with attribution; no source artwork reproduced.
3. [Malvern: Dynamic Light Scattering, An Introduction](https://www.malvernpanalytical.com/en/learn/knowledge-center/technical-notes/tn101104dynamiclightscatteringintroduction)

   Interference, correlation, optical geometry and hydrodynamic equivalence.
4. [Mailer, Clegg & Pusey: Particle Sizing by DLS, Non-linear Cumulant Analysis](https://arxiv.org/pdf/1504.06502)

   Decay-rate moments, truncation windows and inverse problems.
5. [Malvern: Dynamic Light Scattering, Common Terms Defined](https://www.malvernpanalytical.com/en/learn/knowledge-center/whitepapers/wp111214dlstermsdefined)

   Harmonic z-average and PDI definitions.
6. [Malvern: Cumulants and Distribution Algorithms](https://www.malvernpanalytical.com/en/learn/knowledge-center/faqs/faq160705cumulantsnnls)

   Distribution peaks versus cumulant results.
