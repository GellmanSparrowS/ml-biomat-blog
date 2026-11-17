# Zeta potential: Electricity and motion around particles

Source: https://ml-biomat.com/tutorials/experimental-methods/p02/en/
Language: en

Follow phase, velocity and mobility to understand salt, slipping planes and interfacial electrical behavior.

## Why can changing the water make a dispersion clump?

Imagine a suspension of protein-coated nanoparticles that looks uniform immediately after preparation. After transfer into a salt-containing buffer, visible flocs gradually appear. Microscopy can reveal the clumps, and dynamic light scattering can follow changes in size. A zeta-potential measurement asks a question closer to the particle surface: how are nearby ions organized, how does the particle move in an electric field, and what does that motion reveal about the interface? An interface is the region where two materials meet, such as a solid particle and water. Although thin, this region helps determine whether approaching particles remain separated or stick together.

The same question appears in familiar applications. Pigments should remain dispersed to produce a uniform color. Water treatment often aims to collect small suspended objects into flocs that settle readily. A protein formulation needs an appropriate dispersed state during storage and use. Aggregation is therefore useful or troublesome according to the application. Measurements of interfacial electrical behavior help researchers choose acidity, salts and additives, while the final goals remain concrete: coating uniformity, transport through a device, storage performance or retained biological activity. This chapter connects the electrical measurement to size and time rather than assigning every performance question to one number.

Zeta is written with the Greek letter ζ. An electrical potential is an energy-per-charge scale, measured in volts; a millivolt is one thousandth of a volt. A difference in potential tells us how the electrical potential energy of a unit positive charge changes between two positions. A negative reported value does not mean that a particle has a negative amount of energy. It means that the potential near the moving interface is lower than the chosen reference in the distant liquid. The sign also connects to motion in a field, so our diagrams state the field direction and retain signed velocities throughout the calculations.

Three quantities deserve separate names: surface charge, surface potential and zeta potential. Surface charge concerns charged groups and ions associated with the interface. Surface potential refers to a position at the material surface. Zeta potential refers to the boundary involved in relative motion between the particle and its surrounding liquid. They are related, but converting between them requires additional information. A hydrated polymer coating can change both the ion distribution and the hydrodynamic boundary even when the core material is unchanged. We will first follow observable motion, then use that foundation to interpret salt, pH and coating experiments.

## Which part of the surrounding liquid moves with the particle?

Many surfaces acquire charge in contact with water. An acidic group can release a hydrogen ion and leave a negatively charged group behind. A basic group can become positively charged by accepting a hydrogen ion. Adsorption of ions provides another route to interfacial charge. Dissolved ions continue their thermal motion while responding to the electric field: a negative surface usually has an excess of positive ions nearby and a relative depletion of negative ions. Electrical attraction favors proximity, while thermal motion favors dispersal. Their statistical balance produces the electrical double layer, comprising the surface charge and the compensating distribution in the liquid.

The name “double layer” can suggest two perfectly bounded sheets. Some ions close to a surface can indeed be specifically or tightly associated, but the outer distribution usually changes continuously with distance. A city whose population density decreases toward its outskirts is a useful analogy for this gradual change. The analogy concerns a density profile, not immobile inhabitants: ions continually exchange positions, while their average distribution can remain steady. The electrical potential likewise approaches the bulk value gradually. Salt concentration changes the distance over which this approach occurs, a feature we will calculate rather than representing the diffuse layer as a shell with a fixed outer edge.

When a particle moves, nearby liquid and associated material partly accompany it, while more distant liquid moves relative to it. For a particle that admits a sharp-boundary approximation, we draw a slipping plane, also called a shear plane. Zeta potential is the potential at this plane relative to the bulk liquid. A coat changes the boundary at which someone moving through a crowd encounters other people; similarly, a coating can move the effective hydrodynamic boundary away from a particle core. Real polymer layers are permeable to water and ions, however. For soft particles and swollen brushes, flow occurs through a region, requiring a model richer than an impermeable hard sphere with one slipping plane.

Early electrophoresis measurements used microscopes to observe particle displacement and convert distance traveled over a known interval into velocity. Henry's 1931 work connected mobility conversion to the relative scales of the particle and its electrical double layer. That historical issue remains present in modern software: motion is measured first, and a physical model then connects it to potential. The diagram illustrates the observation principle rather than reconstructing a particular historical instrument. Its field points from the positive toward the negative electrode, while negative-mobility particles move in the opposite direction.

![A is an original principle diagram of microscopic electrophoresis linked to Henry’s 1931 work, not a reconstruction of a particular historical apparatus. B is a planar low-potential model at 25 °C and 1 mmol/L ionic strength, surface potential −15 mV; the slipping plane selects the reading position.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/f2f23cc6fbdd1e65cecc7054.svg?v=f2f23cc6fbdd)

Figure 1A is an original principle diagram of microscopic electrophoresis linked to Henry’s 1931 work, not a reconstruction of a particular historical apparatus. B is a planar low-potential model at 25 °C and 1 mmol/L ionic strength, surface potential −15 mV; the slipping plane selects the reading position.

The second panel places the material surface and slipping plane on the same potential profile. Holding the surface potential fixed while moving the slipping plane outward decreases the magnitude of ζ in this model. The surface has not become electrically neutral. This separates two experimental questions: did surface chemistry change, and did an adsorbed or hydrated layer change the flow boundary? When protein exposure changes a nanoparticle's mobility, measurements of adsorbed protein, size and medium composition help develop a structural explanation for that interfacial change.

## From visible motion to the phase of scattered light

Velocity is displacement divided by elapsed time. Electrophoretic mobility divides the velocity relative to the liquid by electric-field strength. Within a linear response regime, doubling the field doubles the mean electrophoretic velocity; dividing by the field produces a coefficient that can be compared across settings. Field strength has units of volts per meter and describes how rapidly potential changes with position. For an ideal uniform field it equals the voltage difference divided by electrode separation. Real cell geometries require the appropriate field calibration. Equal applied voltages in two differently shaped cells need not produce equal fields.

$$
\mu_e=\frac{v_e}{E},\qquad v_{\mathrm{obs}}=\mu_eE+v_b,\qquad E=\frac{\Delta V}{L}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/30854555fd9f63edbc653606.svg) | Signed electrophoretic mobility, m²/(V·s). |
| ![Formula](https://ml-biomat.com/static/agent-math/faaaf4cbacd278edd00b6bef.svg) | Particle electrophoretic velocity relative to the liquid, m/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | Electric-field component along the chosen direction, V/m. |
| ![Formula](https://ml-biomat.com/static/agent-math/446a2b5c06840d79dbea4391.svg) | Observed mean velocity, m/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/e0b1d31d4957d48699797e34.svg) | Constant field-independent background-fluid velocity, m/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/d734398b2cf2660032fdbf86.svg) | Voltage drop defined along the field direction, V. |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Electrode separation in the uniform-field approximation, m. |

Linear response and steady velocity, with electrophoresis referenced to the liquid. An ideal 10 V drop over 0.01 m gives 1000 V/m. μe=−1.949911×10⁻⁸ m²/(V·s) gives ve=−19.49911 μm/s; adding 3 μm/s constant flow gives −16.49911 μm/s. Nonuniform or folded cells use their field calibration.

Brownian motion continues while the field is applied. A tracked particle can wander left and right around its mean directed motion, especially over short intervals. Averaging suitable observations estimates the drift. Electrophoretic light scattering measures an ensemble through scattered light rather than requiring every particle to be resolved as a visible object. Motion changes the phase of scattered light relative to a reference and can appear as a small frequency shift. Think of two clock hands: when they rotate at the same rate, their angular separation remains constant; a small difference in rate produces an accumulating phase difference.

Phase analysis light scattering, or PALS, uses this accumulation to estimate small movements. A plot of phase difference against time has a slope related to velocity. One complete cycle corresponds to two pi radians. Recorded angles are often wrapped into a single cycle, and phase unwrapping joins successive cycles into a continuous progression. Successful unwrapping requires sufficiently small and sufficiently well-resolved changes between samples. Our example creates a complex optical signal with a specified projected scattering coefficient, adds noise, unwraps its phase and fits a straight line. This is a teaching signal for the phase-to-velocity calculation, not a recreation of all the statistical and electronic processing in a commercial instrument.

$$
\phi(t)=\phi_0+q_{\parallel}v_{\mathrm{obs}}t,\qquad v_{\mathrm{obs}}=\frac{1}{q_{\parallel}}\frac{d\phi}{dt}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/05b88f36b3fde196e67c87eb.svg) | Unwrapped and initial phase, rad. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/9a08ebf776281e4521428c39.svg) | Signed scattering-vector projection along the velocity direction, m⁻¹; fixed by optical geometry. |
| ![Formula](https://ml-biomat.com/static/agent-math/446a2b5c06840d79dbea4391.svg) | Observed velocity component, m/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/fe11c3232bceca2eab4e659c.svg) | Phase slope versus time, rad/s. |

Constant-velocity optical phase model with a consistent reference-phase sign. q∥=3×10⁶ m⁻¹ and vobs=−16.49911 μm/s give −49.49733 rad/s, a −12.37433 rad change in 0.25 s. The example adds noise to a complex signal before unwrapping and fitting.

The six fields in the figure combine three magnitudes with both polarities. A model potential of −25 mV gives a mobility of approximately −1.950 × 10⁻⁸ m²/(V s). At 1000 V/m, the particle's velocity relative to the liquid is about −19.50 μm/s. We also add a constant background flow of 3 μm/s. The observed velocity is consequently about −16.50 μm/s; reversing the field gives about 22.50 μm/s. Fitting observed velocity against signed field strength recovers mobility from the slope and constant flow from the intercept. Retaining direction is essential to this separation.

![Constructed signals, seed 820: ζ=−25 mV, viscosity 0.89 mPa·s, relative permittivity 78.4, constant flow 3 μm/s, projected optical coefficient 3×10⁶ m⁻¹. A shows two phase records; B fits six fields; C retains phase residuals. D adds an electro-osmotic slope 0.5×10⁻⁸ m²/(V·s), illustrating a term that polarity reversal alone leaves in the result.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/2cceabab4926d78ddd076915.svg?v=2cceabab4926)

Figure 2Constructed signals, seed 820: ζ=−25 mV, viscosity 0.89 mPa·s, relative permittivity 78.4, constant flow 3 μm/s, projected optical coefficient 3×10⁶ m⁻¹. A shows two phase records; B fits six fields; C retains phase residuals. D adds an electro-osmotic slope 0.5×10⁻⁸ m²/(V·s), illustrating a term that polarity reversal alone leaves in the result.

Liquid flow can itself reverse with the field. Charged cell walls have electrical double layers, and the applied field can drive liquid along them through electro-osmosis. A closed cell also develops return flow. If local fluid velocity is proportional to field strength, simply comparing positive and negative fields leaves that contribution in the measured slope. Panel D shows this explicitly. Instruments address electro-osmosis through their observation position, cell design or a fast reversal sequence exploiting the different response times of particles and developing fluid flow. Polarity reversal and a validated electro-osmotic correction are therefore distinct parts of the measurement.

## How does mobility become a value in millivolts?

Electrical forcing produces motion opposed by viscous resistance. A more viscous medium generally gives slower motion for the same interfacial electrical state and applied field. The medium's permittivity also enters the relation between charge and electric field. Converting mobility therefore requires dynamic viscosity and permittivity at the measurement temperature. Dynamic viscosity is expressed in Pa s; water near 25 °C has a value around 0.00089 Pa s, or 0.89 mPa s. Relative permittivity is a dimensionless ratio to vacuum. The absolute permittivity in our equations is that ratio multiplied by the vacuum permittivity, with units F/m. Confusing the two produces a large numerical error.

The Henry relation includes a function of κa. Here a is particle radius, while the reciprocal of κ is a characteristic screening length. Their product compares particle size with the extent of the electrical double layer. In the Hückel limit of a double layer much larger than the particle, the Henry function tends to 1. In the Smoluchowski limit of a much smaller double-layer scale, with the relevant electrokinetic conditions satisfied, it tends to 1.5. Intermediate cases require an appropriate function or fuller model. Calling a sample “aqueous” does not by itself settle this choice.

$$
\mu_e=\frac{2\varepsilon\zeta f(\kappa a)}{3\eta},\quad\varepsilon=\varepsilon_0\varepsilon_r,\qquad\zeta_{\mathrm{Smol}}=\frac{\eta\mu_e}{\varepsilon}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/30854555fd9f63edbc653606.svg) | Electrophoretic mobility, m²/(V·s). |
| ![Formula](https://ml-biomat.com/static/agent-math/35264eff6bf21304fbf59624.svg) | Zeta potential and its Smoluchowski conversion, V. |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | Dynamic viscosity, Pa·s. |
| ![Formula](https://ml-biomat.com/static/agent-math/9bc08d537f481d038b7b8b9d.svg) | Absolute permittivity of the liquid, F/m. |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | Vacuum permittivity, 8.8541878128×10⁻¹² F/m in this example. |
| ![Formula](https://ml-biomat.com/static/agent-math/f1d4e2d001f572c0acb3f119.svg) | Relative permittivity of the liquid, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/cb154160fd6d330501f6321c.svg) | Inverse Debye length, m⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Particle radius, m. |
| ![Formula](https://ml-biomat.com/static/agent-math/c38ceecfc9d2ffb270e214f3.svg) | Dimensionless Henry function; 1 in the Hückel limit, 1.5 in the Smoluchowski limit. |

The classical Henry relation uses the corresponding dilute rigid-particle, low-potential approximation; assess double-layer scale, relaxation and surface-conduction conditions. Setting f=1.5 gives the right-hand relation. With μe=−4.5×10⁻⁸, η=0.00089 Pa·s, εr=78.4, it gives −0.05769494 V; f=1 gives −0.08654241 V. The reference example retains the report’s Smoluchowski convention and rounded certified values.

Consider a mobility of −4.5 × 10⁻⁸ m²/(V s). Using 25 °C, a viscosity of 0.89 mPa s and relative permittivity 78.4, the Smoluchowski conversion gives about −57.69 mV. The Hückel limiting conversion gives about −86.54 mV, a magnitude 50% larger. These are two model outputs from the same measured mobility, not evidence that the specimen changed. In the reference-material example later in the chapter, we use the Smoluchowski convention adopted by its certification report and retain the certified rounded value of −58 mV. Reporting mobility alongside the conversion model preserves the path from observation to interpretation.

The classical Henry treatment concerns the corresponding dilute, rigid-particle, low-potential approximation and omits certain relaxation and surface-conduction effects. Larger potentials, appreciable surface conduction or permeable coatings call for models that include those processes. This also explains why a zeta value is not converted directly into a simple count of electrons on a particle. The applied field acts on the coupled particle, surrounding ions and liquid. If the objective is to determine numbers of surface groups, acid–base titration, surface chemical analysis or adsorption measurements can supply complementary information with their own defined quantities.

A useful way to inspect a software result is to follow the chain of inputs. Medium composition determines suitable viscosity and permittivity values; temperature changes them; particle radius and ionic strength help assess the model; optical data yield mobility; and the chosen relation converts mobility into potential. When two instruments disagree, compare their mobilities and these inputs first. Agreement in mobility with disagreement in ζ points toward conversion choices. A difference already present in mobility directs attention to preparation, field conditions, liquid flow, acquisition time or the population remaining suspended during measurement.

## Salt changes the spatial range of electrical interactions

Adding sodium chloride increases the supply of positive and negative ions that can rearrange near a surface. Counterions around a negative surface screen its electrical influence at greater distances. The Debye length describes this decay scale: in a simplified low-potential model, increasing distance by one Debye length reduces the potential amplitude to about 37% of its previous value. It is not the thickness of a sharply bounded liquid shell. At fixed temperature and permittivity in the dilute-electrolyte approximation, the length varies inversely with the square root of ionic strength. A hundredfold increase in ionic strength shortens the scale tenfold.

Ionic strength accounts for every ion's concentration and squared charge number. Sodium and chloride contribute positively because the charge is squared. Divalent ions carry a larger weighting at equal molar concentration and can also introduce specific adsorption or bridging. Changing salt identity can therefore affect both screening and surface chemistry. Buffer ions count as well. Conductivity is useful for checking consistency of the liquid, but it also depends on how rapidly each ion moves. Conductivity and ionic strength are related quantities, not universally interchangeable measurements.

$$
I=\frac12\sum_i c_i z_i^2,\qquad\lambda_D=\kappa^{-1}=\sqrt{\frac{\varepsilon k_BT}{2e^2N_A\,1000I}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/112feff6b4d0334226e24d5c.svg) | Ionic strength, mol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/29928b2adca455a1420619c0.svg) | Molar concentration of ionic species i, mol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/51874f02b4c579417c89ce04.svg) | Charge number of ionic species i, e.g.+1 for Na⁺, +2 for Ca²⁺, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Index over ionic species. |
| ![Formula](https://ml-biomat.com/static/agent-math/e0a253a79b8148f73aac3fcc.svg) | Debye length(m) and its inverse(m⁻¹). |
| ![Formula](https://ml-biomat.com/static/agent-math/9bc08d537f481d038b7b8b9d.svg) | Absolute liquid permittivity, F/m. |
| ![Formula](https://ml-biomat.com/static/agent-math/2600a50cd45c9994bcd80b30.svg) | Boltzmann constant, 1.380649×10⁻²³ J/K. |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | Absolute temperature, K. |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | Elementary charge, 1.602176634×10⁻¹⁹C. |
| ![Formula](https://ml-biomat.com/static/agent-math/160ee348aa1d6f945e161c12.svg) | Avogadro constant, 6.02214076×10²³ mol⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/11e3e740ee2e42f3954f5b75.svg) | Unit-conversion factor from mol/L to mol/m³, L/m³. |

Debye screening scale for an ideal dilute electrolyte in a continuum medium. 1 mmol/L NaCl contains 1 mmol/L of each ion, so I=0.001 mol/L. T=298.15 K and εr=78.4 give λD≈9.61370 nm. A 100-fold I increase reduces λD tenfold. Code input is mmol/L, numerically equal to mol/m³, so it does not multiply by 1000 again.

Panel A calculates Debye lengths of about 30.40, 9.61, 3.04 and 0.96 nm at ionic strengths of 0.1, 1, 10 and 100 mmol/L in the specified 25 °C aqueous medium. Panel C adds particle radius. At the same 1 mmol/L, objects with radii of 1 and 1000 nm differ in κa by a factor of one thousand. The contour lines mark scale ratios rather than acceptance limits for instrument accuracy. Proximity to a theoretical limit must be judged together with required accuracy and the remaining model conditions. A single salt-concentration threshold cannot select the correct conversion for every nanoparticle.

![Ideal electrolyte at 25 °C with fixed aqueous permittivity. A shows inverse-square-root screening length; B fixes surface potential at −15 mV and places the dashed slipping plane 1 nm out; C shows κa, not measurement accuracy. Contours 1 and 100 are scale references.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/da94ba17efe3dc302732c206.svg?v=da94ba17efe3)

Figure 3Ideal electrolyte at 25 °C with fixed aqueous permittivity. A shows inverse-square-root screening length; B fixes surface potential at −15 mV and places the dashed slipping plane 1 nm out; C shows κa, not measurement accuracy. Contours 1 and 100 are scale references.

To isolate screening, take a planar low-potential model with fixed surface potential −15 mV. Place the slipping plane 1 nm from the surface. At 1 mmol/L the potential there is approximately −13.52 mV; at 100 mmol/L it is approximately −5.30 mV. Surface potential stayed fixed while the reported interfacial value approached zero because spatial decay became faster. The calculation deliberately separates boundary conditions, screening length and reading position. A real surface can regulate its charge as salt or pH changes, making its response richer than this fixed-potential illustration.

$$
\psi(x)=\psi_0\exp\left(-\frac{x}{\lambda_D}\right),\qquad\zeta=\psi(\delta)=\psi_0\exp\left(-\frac{\delta}{\lambda_D}\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f24b70e332dca9c1dbcbb320.svg) | Potential at distance x and at the surface; use consistently V or mV. |
| ![Formula](https://ml-biomat.com/static/agent-math/74f5bfc58ab11608a49c92ee.svg) | Distance from surface and slipping-plane position, consistent length units. |
| ![Formula](https://ml-biomat.com/static/agent-math/ae336c0d5d10c0c71e8df08c.svg) | Debye length, in the same length units as x and δ. |
| ![Formula](https://ml-biomat.com/static/agent-math/00f4c72c0a43d6a0501d3d63.svg) | Slipping-plane potential relative to bulk, in the same potential units as ψ. |

Linearized planar low-potential model at fixed surface potential and zero bulk potential; omits specific adsorption and charge regulation. ψ0=−15 mV, δ=1 nm give ζ=−13.51813 mV at 1 mmol/L and −5.30085 mV at 100 mmol/L. This illustrates screening and reading position rather than predicting a real material’s titration.

The interactive experiment varies ionic strength, slipping-plane distance and surface potential independently. Keep surface potential fixed and compare two ways of reducing the magnitude of ζ: stronger screening and moving the plane outward. Then choose a positive surface potential and examine the sign reversal. At low salt, a profile displayed out to 40 nm still has a tail rather than ending exactly at zero. The experiment concerns an explicitly defined planar potential profile. It does not turn a small ζ into proof of vanishing surface charge or simulate the titration curve of an unspecified real material.

## Why can one surface give different zeta values?

Planar low-potential model at 25 °C, fixed relative permittivity 78.4. Vary ionic strength, slipping-plane distance and surface potential to inspect the profile and reading. κa uses a 100 nm radius as a scale reference.

[Figure: Potential versus distance from the surface](https://ml-biomat.com/tutorials/experimental-methods/p02/en/#P02-plot)

## Connect pH, adsorption and dispersion stability through experiments

Changing pH changes the protonation state of surface groups. A zeta-versus-pH curve may cross zero at an isoelectric point, where electrophoretic mobility approaches zero under the stated conditions. A point of zero charge concerns net surface charge. Specific ion adsorption can make these points differ. Proteins and protein-coated particles add charge patches, conformational changes and evolving adsorbed layers. A near-zero average electrokinetic potential does not require every surface region to be uncharged. A pH series is consequently a map of changing interfacial behavior, rather than a search for one universally desirable number.

A useful pH experiment controls other changes caused by titration. Acid or base addition changes volume and ionic composition. A locally concentrated addition may alter a protein or aggregate particles before mixing is complete. Separate specimens prepared at different pH values can maintain comparable background electrolyte. Alternatively, a stepwise titration can record added volume, equilibration time and conductivity, with upward and downward pH paths compared. Hysteresis encourages investigation of irreversible adsorption, aggregation or structural change. If large clumps settle at one pH, optical measurements may preferentially describe the fraction still suspended; appearance and size measurements help identify that change in the measured population.

The DLVO framework developed in the 1940s brought electrical double-layer repulsion and van der Waals attraction into a common description of particle interactions. Imagine approaching particles traversing an energy landscape. Repulsion can create a barrier, while attraction favors closer contact. Salt changes the range of repulsion, and thermal motion repeatedly brings particles together. This picture helps explain why many electrically stabilized dispersions aggregate after salt addition. A zeta measurement supplies electrokinetic information about the interface; the interaction barrier also depends on particle geometry, separation, medium and surface conditions. Storage time determines how repeated encounters accumulate into visible changes.

Hydrated polymer and protein coatings provide additional routes to stabilization. As particles approach, overlapping and compressed chains lose accessible configurations and alter local solvent conditions, creating steric interactions. A modest zeta magnitude can therefore coexist with a well-dispersed sample. Uneven coverage or a chain binding two particles can instead promote bridging. When comparing formulations, use ζ to describe one dimension of the interface and place it alongside size over time, turbidity, sedimentation and functional measurements. Each observable then has a clear mechanistic role, while formulation performance is judged under its intended conditions.

Before acquisition, equilibrate specimen and liquid to the chosen temperature and record pH, composition, particle concentration and conductivity. Dilution should preserve the relevant liquid environment, and its effect on adsorption equilibria should be considered. Adding pure water can change the state being studied. Very dilute suspensions can give weak scattering; concentrated suspensions can introduce multiple scattering and particle interactions. A concentration series made with matching medium helps identify a useful measurement range. Inspect optical windows, electrodes and bubbles as well as the displayed number. A phase slope that drifts during repeated records points toward changing temperature, aggregation, flow or electrode processes.

Field strength itself provides a diagnostic. In a stable linear-response regime, mobility remains consistent across an appropriate field range. Systematic field dependence encourages inspection of Joule heating, polarization and liquid motion. Suitable voltage depends on conductivity, cell geometry and the validated instrument method. Independent preparations, separate aliquots and repeated measurements of the same aliquot address different sources of variation. Planning these levels makes it possible to distinguish a formulation effect from sampling differences or short-term instrumental scatter, and to identify which experimental step should be adjusted next.

## Use real reference data and complete calculations to interpret a result

A reference material supplies a shared object for evaluating a measurement system. The NIST/JRC colloidal silica material SRM 1992/ERM-FD305 has a certified electrophoretic mobility of −4.5 × 10⁻⁸ m²/(V s) in its specified borate buffer at 25 °C, with expanded uncertainty 0.4 × 10⁻⁸ m²/(V s) and coverage factor k = 2. The certification report converts this mobility using specified medium properties to obtain −58 ± 5 mV. These certified quantities are mathematically connected; they are not two independent measurements that can validate each other.

The figure redraws the 15 accepted datasets in Table E1.1. Each contains six independent aliquot means, and each aliquot was measured five times in the original study. Those aliquots came from three ampoules and were measured across three days, incorporating sampling and between-day factors. The datasets came from 12 laboratories, with one laboratory contributing four instrument or cell combinations. The points therefore represent aliquot means, not 90 independent preparations or 90 laboratories. Gold points show variation within each dataset. Blue error bars indicate one sample standard deviation of the six aliquot means. The shaded band represents the certified value plus or minus expanded uncertainty. Their definitions differ, allowing within-dataset dispersion of aliquot means, differences between datasets and the reference range to be read separately.

![Measured numerical data redrawn from Ramaye et al., NIST SP260-208, Table E1.1 and Tables 11–12. Fifteen datasets from 12 laboratories, six aliquot means each. Gold: aliquot means; blue: mean ± 1 sample SD; band: certified mobility ± expanded uncertainty (k=2). L11a–d are different configurations from one laboratory. B contains certification uncertainty components, not laboratory error bars. Published numerical facts are transcribed into an original plot.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/c31b4af588dab196e6e74451.svg?v=c31b4af588da)

Figure 4Measured numerical data redrawn from Ramaye et al., NIST SP260-208, Table E1.1 and Tables 11–12. Fifteen datasets from 12 laboratories, six aliquot means each. Gold: aliquot means; blue: mean ± 1 sample SD; band: certified mobility ± expanded uncertainty (k=2). L11a–d are different configurations from one laboratory. B contains certification uncertainty components, not laboratory error bars. Published numerical facts are transcribed into an original plot.

Using the rounded numbers printed in the table gives a mean of dataset means of approximately −4.53478 in units of 10⁻⁸ m²/(V s). Certification also included homogeneity, shipping and storage studies. The spread of these 90 values therefore does not replace the full certification uncertainty. The four relative standard uncertainty components displayed on the right are 1.39%, 3.40%, 0.42% and 1.80%. Under the stated independent-component approximation, their squared values add, the square root gives a combined standard uncertainty, and a coverage factor gives expanded uncertainty. This differs from directly adding percentages.

$$
u_{c,\mathrm{rel}}=\sqrt{u_{\mathrm{char,rel}}^2+u_{\mathrm{bb,rel}}^2+u_{\mathrm{sts,rel}}^2+u_{\mathrm{lts,rel}}^2},\qquad U_{\mathrm{rel}}=k u_{c,\mathrm{rel}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7ee35732f6e138b09fc67bda.svg) | Combined relative standard uncertainty, in consistent fractions or percent. |
| ![Formula](https://ml-biomat.com/static/agent-math/ad4038a42317ce1bbc0c4683.svg) | Relative standard uncertainty from characterization. |
| ![Formula](https://ml-biomat.com/static/agent-math/81fd171c2ddcdbf497fb6c1f.svg) | Relative standard uncertainty from between-ampoule heterogeneity. |
| ![Formula](https://ml-biomat.com/static/agent-math/520c56af957880e974d91b05.svg) | Relative standard uncertainties from short-term and long-term stability. |
| ![Formula](https://ml-biomat.com/static/agent-math/2a2c9da525563eccc6f917ad.svg) | Expanded relative uncertainty, in the same representation as u. |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | Dimensionless coverage factor, 2 here. |

Root-sum-of-squares under the corresponding independent-component approximation. Printed 1.39%, 3.40%, 0.42%, 1.80% give uc, rel≈4.112% and Urel≈8.224% for k=2; the report retains 8.3% from its full calculation. Certified mobility uncertainty is rounded to 0.4×10⁻⁸ m²/(V·s). Dataset ± 1 SD bars have a different definition from expanded uncertainty.

The printed rounded components give about 8.22% after applying k = 2, while the report gives 8.3% from its full calculation. Preserving that distinction avoids manufacturing agreement by changing a published number. A narrow spread from repeated readings of one aliquot addresses a different question from possible differences between ampoules or changes during storage. A small technical standard deviation can therefore be useful and accurate while remaining only one component of the broader measurement uncertainty.

The complete Python example follows two paths. First, random seed 820 generates six noisy complex optical signals. Phase unwrapping and line fitting recover velocities; a second fit separates mobility from constant drift. Execution recovers approximately −25.005 mV and 3.0003 μm/s from the specified −25 mV and 3 μm/s. Residuals retain the noise so that the line model can be inspected. The second path reads the bundled measured mobility data, calculates dataset means and standard deviations, and plots them with the certified range and uncertainty components. Constructed signals explain the algorithm, while measured data illustrate the hierarchy of an experimental study.

The code also calculates Debye lengths, fixed-potential spatial profiles and the difference between limiting Henry conversions. CSV outputs preserve field–velocity pairs, selected phase traces, screening calculations and reference statistics. A compressed array retains all phase records and residuals for alternative fitting windows. To explore further, make the background flow proportional to field strength and inspect why intercept correction no longer removes it. Increasing noise or shortening acquisition provides a separate way to test the stability of the estimated slope. Each change corresponds to a specific physical or processing step.

### From phase to mobility, then measured reference data

Runs complex-signal generation, phase unwrapping, velocity and mobility fitting, screening calculations, measured aliquot statistics and uncertainty combination; all figures and data are produced offline.

```
"""Zeta potential: from constructed optical phase to mobility and conversion.
Real reference-material aliquot means are bundled in data/mobility.csv.
Run offline: python main.py --output results --language en
"""
from pathlib import Path
import argparse,json,csv as csvlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle

p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();O=args.output;O.mkdir(parents=True,exist_ok=True)
ZH=args.language=='zh'
def L(z,e):return z if ZH else e
plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.facecolor':'#fcfbf7','figure.facecolor':'#fcfbf7','svg.fonttype':'none','text.color':'#20333e','axes.labelcolor':'#20333e','axes.titleweight':'bold'})
B='#167d9a';R='#d35f47';G='#37967d';Y='#c49b35';K='#20333e'
def save(f,n):
 for e in ['svg','png']:f.savefig(O/f'{n}-{args.language}.{e}',dpi=145,bbox_inches='tight')
 plt.close(f)
def csv(n,heads,cols):np.savetxt(O/n,np.column_stack(cols),delimiter=',',header=','.join(heads),comments='',fmt='%.10g')
eps0=8.8541878128e-12;epsr=78.4;eps=eps0*epsr;eta=.00089;T=298.15;kb=1.380649e-23;e=1.602176634e-19;NA=6.02214076e23
def debye(I_mM):return np.sqrt(eps*kb*T/(2*e**2*NA*np.asarray(I_mM)))
rng=np.random.default_rng(820);zeta=-.025;mu=eps*zeta/eta;vbg=3e-6;q=3e6
fields=np.array([-1500,-1000,-500,500,1000,1500.]);t=np.linspace(0,.25,501);fitted=[];phases=[];residuals=[]
for E in fields:
 velocity=mu*E+vbg;phase=.4+q*velocity*t
 signal=np.exp(1j*phase)+.035*(rng.normal(size=t.size)+1j*rng.normal(size=t.size))
 unwrapped=np.unwrap(np.angle(signal));coef=np.polyfit(t,unwrapped,1);fit=np.polyval(coef,t)
 fitted.append(coef[0]/q);phases.append(unwrapped);residuals.append(unwrapped-fit)
fitted=np.array(fitted);phases=np.array(phases);residuals=np.array(residuals)
mf,bf=np.polyfit(fields,fitted,1);zf=mf*eta/eps
np.savez_compressed(O/'phase_records.npz',time_s=t,fields_V_m=fields,phase_rad=phases,phase_residual_rad=residuals)
csv('field_velocity.csv',['field_V_m','true_velocity_m_s','fitted_velocity_m_s'],[fields,mu*fields+vbg,fitted])
csv('phase_pair.csv',['time_s','phase_minus1000_rad','phase_plus1000_rad'],[t,phases[1],phases[4]])

# A historical principle illustration, not a reconstruction of a named apparatus.
fig,axs=plt.subplots(1,2,figsize=(12.8,5.4),layout='constrained',gridspec_kw={'width_ratios':[1.1,1]})
ax=axs[0];ax.set(xlim=(0,10),ylim=(0,7));ax.axis('off');ax.set_title(L('A  从显微观察到迁移率','A  From microscope observation to mobility'),loc='left')
ax.add_patch(Rectangle((.7,2),8.6,2.4,facecolor='#e6f1f2',edgecolor=B,lw=2))
for x,sign in [(1,'+'),(9,'−')]:ax.plot([x,x],[2.2,4.2],color=R,lw=5);ax.text(x,4.65,sign,ha='center',fontsize=22)
ax.annotate('',xy=(7.6,3.8),xytext=(2.4,3.8),arrowprops={'arrowstyle':'->','color':R,'lw':2});ax.text(5,4.05,L('电场 E','Electric field E'),ha='center',color=R)
for x in [3.8,4.5,5.2]:ax.add_patch(Circle((x,2.9),.16,color=B))
ax.annotate('',xy=(2.4,2.9),xytext=(3.4,2.9),arrowprops={'arrowstyle':'->','color':B,'lw':2});ax.text(5.6,2.85,L('负迁移率颗粒','Negative-mobility particles'),fontsize=10)
ax.plot([4.1,4.1],[5.1,6],color=K,lw=9);ax.plot([3.5,4.7],[5.1,5.1],color=K,lw=3);ax.plot([4.1,4.1],[4.4,5.05],color=K,ls=':');ax.text(4.7,5.6,L('显微镜观察位移','Microscope observes displacement'),fontsize=10)
ax.text(.8,1.35,L('1931 · Henry 将颗粒曲率与双电层尺度\n接入迁移率—电位的关系。','1931 · Henry links particle curvature and\ndouble-layer extent to mobility conversion.'),va='center',fontsize=11)
ax.text(.8,.4,L('原理示意；电极方向与符号明确','Principle illustration; explicit field and sign'),fontsize=10,color='#61717b')
ax=axs[1];x=np.linspace(0,25,400);lam=debye(1)*1e9;psi=-15*np.exp(-x/lam);slip=1.;ax.plot(x,psi,color=B,lw=2.5);ax.fill_between(x,psi,0,color=B,alpha=.08);ax.axvline(slip,color=R,ls='--');ax.scatter([0,slip],[-15,-15*np.exp(-slip/lam)],color=[B,R],zorder=5);ax.axhline(0,color=K,lw=.7)
ax.annotate(L('表面电位 −15 mV','Surface potential −15 mV'),(0,-15),(7,-14.3),arrowprops={'arrowstyle':'->','color':B},color=B)
ax.annotate(L('滑移面处 ζ','ζ at slipping plane'),(slip,-15*np.exp(-slip/lam)),(9,-10.2),arrowprops={'arrowstyle':'->','color':R},color=R)
ax.text(9,-.8,L('远处液体取零电位','Bulk liquid sets zero potential'),fontsize=10)
ax.set(xlabel=L('距表面距离 / nm','Distance from surface / nm'),ylabel=L('电位 / mV','Potential / mV'),title=L('B  运动的边界决定读哪个电位','B  The motion boundary defines which potential'),ylim=(-17,1))
save(fig,'history-interface')

fig,axs=plt.subplots(2,2,figsize=(12.8,9),layout='constrained')
for j,c in [(1,B),(4,R)]:axs[0,0].plot(t,phases[j],color=c,lw=1.2,label=f'E = {fields[j]:.0f} V/m')
axs[0,0].set(xlabel=L('时间 / s','Time / s'),ylabel=L('展开相位 / rad','Unwrapped phase / rad'),title=L('A  构造的光学相位记录','A  Constructed optical phase records'));axs[0,0].legend(frameon=False)
axs[0,1].scatter(fields,fitted*1e6,color=B,s=45,zorder=3);ef=np.linspace(-1600,1600,100);axs[0,1].plot(ef,(mf*ef+bf)*1e6,color=B);axs[0,1].axhline(0,color=K,lw=.7);axs[0,1].axvline(0,color=K,lw=.7);axs[0,1].set(xlabel=L('电场 / V m⁻¹','Electric field / V m⁻¹'),ylabel=L('观测速度 / μm s⁻¹','Observed velocity / μm s⁻¹'),title=L('B  斜率给迁移率，截距给恒定漂移','B  Slope gives mobility; intercept gives drift'));axs[0,1].text(.06,.06,f'μ = {mf/1e-8:.5f} × 10⁻⁸ m²/(V s)\n'+L('漂移','Drift')+f' = {bf*1e6:.4f} μm/s',transform=axs[0,1].transAxes,fontsize=10,bbox={'fc':'#fcfbf7','ec':'none'})
for j,c in [(1,B),(4,R)]:axs[1,0].plot(t,residuals[j],color=c,alpha=.7,lw=.8)
axs[1,0].set(xlabel=L('时间 / s','Time / s'),ylabel=L('相位拟合残差 / rad','Phase-fit residual / rad'),title=L('C  残差揭示记录是否偏离直线','C  Residuals test the straight-line model'))
eo=.5e-8;vals=[mu,mu+eo];labels=L(['恒定背景流已扣除','还存在随电场反向的液流'],['Constant background removed','Field-dependent flow remains']);axs[1,1].barh([1,0],np.array(vals)/1e-8,color=[B,R],height=.55);axs[1,1].set_yticks([1,0],labels);axs[1,1].set(xlim=(-2.2,0),xlabel=L('从场—速度斜率得到的量 / 10⁻⁸ m² V⁻¹ s⁻¹','Field–velocity slope / 10⁻⁸ m² V⁻¹ s⁻¹'),title=L('D  反向电场不会自动消除电渗流','D  Polarity reversal alone does not remove EOF'));axs[1,1].tick_params(axis='y',labelsize=9)
for y,v in zip([1,0],vals):axs[1,1].text(v/1e-8+.05,y,f'{v/1e-8:.4f}',va='center',color='white',fontweight='bold')
save(fig,'phase-to-mobility')

Is=np.logspace(-1,2,200);lams=debye(Is)*1e9;x=np.linspace(0,40,401)
csv('screening.csv',['ionic_strength_mM','Debye_length_nm','zeta_at1nm_mV'],[Is,lams,-15*np.exp(-1/lams)])
fig,axs=plt.subplots(1,3,figsize=(14,4.8),layout='constrained')
axs[0].loglog(Is,lams,color=B,lw=2.5)
for ii in [.1,1,10,100]:axs[0].scatter(ii,debye(ii)*1e9,color=R);axs[0].annotate(f'{debye(ii)*1e9:.2f}',(ii,debye(ii)*1e9),xytext=(0,8),textcoords='offset points',ha='center',fontsize=9)
axs[0].set(xlabel=L('离子强度 / mmol L⁻¹','Ionic strength / mmol L⁻¹'),ylabel=L('Debye长度 / nm','Debye length / nm'),title=L('A  浓度百倍，长度缩短十倍','A  100× concentration gives 10× shorter range'),ylim=(.7,55))
for ii,c in zip([.1,1,10,100],[B,G,Y,R]):
 la=debye(ii)*1e9;axs[1].plot(x,-15*np.exp(-x/la),color=c,label=f'{ii:g} mM')
axs[1].axvline(1,color=K,ls='--',lw=1);axs[1].set(xlabel=L('距表面距离 / nm','Distance from surface / nm'),ylabel=L('电位 / mV','Potential / mV'),title=L('B  固定表面电位的平面模型','B  Planar model at fixed surface potential'),ylim=(-16,1));axs[1].legend(frameon=False,fontsize=9)
aa=np.logspace(0,3,180);kap=aa[:,None]/lams[None,:];im=axs[2].pcolormesh(Is,aa,np.log10(kap),cmap='viridis',shading='auto',vmin=-1.5,vmax=3);cs=axs[2].contour(Is,aa,kap,levels=[1,100],colors='white',linewidths=1.4);axs[2].clabel(cs,fmt={1:'κa = 1',100:'κa = 100'},fontsize=9,manual=[(20,2.15),(5,430)]);axs[2].set(xscale='log',yscale='log',xlabel=L('离子强度 / mmol L⁻¹','Ionic strength / mmol L⁻¹'),ylabel=L('颗粒半径 a / nm','Particle radius a / nm'),title=L('C  模型选择还取决于颗粒半径','C  Model choice also depends on radius'));fig.colorbar(im,ax=axs[2],label='log₁₀(κa)',shrink=.8)
save(fig,'salt-and-scale')

with (Path(__file__).parent/'data/mobility.csv').open(encoding='utf8') as f:rows=list(csvlib.DictReader(f))
names=[r['dataset'] for r in rows];data=np.array([[float(r[f'r{i}']) for i in range(1,7)] for r in rows]);means=data.mean(axis=1);sd=data.std(axis=1,ddof=1);components=np.array([1.39,3.40,.42,1.80]);urel=2*np.linalg.norm(components)
csv('reference_summary.csv',['dataset_index','mean_mobility_1e8','SD_of_six_aliquot_means_1e8'],[np.arange(len(names)),means,sd])
fig,axs=plt.subplots(1,2,figsize=(12.8,7.2),layout='constrained',gridspec_kw={'width_ratios':[1.3,1]});ax=axs[0];yy=np.arange(len(names));ax.axvspan(-4.9,-4.1,color=B,alpha=.1,label=L('认证值 ± U（k=2）','Certified value ± U (k=2)'));ax.axvline(-4.5,color=B,ls='--');ax.errorbar(means,yy,xerr=sd,fmt='o',color=B,ecolor=B,capsize=3,ms=4,label=L('均值 ± 1 SD','Mean ± 1 SD'))
for k in yy:ax.scatter(data[k],k+np.linspace(-.14,.14,6),s=13,color=Y,alpha=.8)
ax.set(yticks=yy,yticklabels=names,xlabel=L('迁移率 / 10⁻⁸ m² V⁻¹ s⁻¹','Mobility / 10⁻⁸ m² V⁻¹ s⁻¹'),title=L('A  真实测量：15组，每组6个取样均值','A  Measured: 15 datasets, six aliquot means each'));ax.invert_yaxis();ax.legend(frameon=False,fontsize=9,loc='lower right')
ax=axs[1];lab=L(['赋值研究','安瓿之间','短期稳定性','长期稳定性'],['Characterization','Between ampoules','Short-term stability','Long-term stability']);ax.barh(np.arange(4),components,color=[B,R,Y,G],height=.5);ax.set_yticks(np.arange(4),lab);ax.set(xlim=(0,4.4),ylim=(-1,5.8),xlabel=L('相对标准不确定度 / %','Relative standard uncertainty / %'),title=L('B  重复性以外的不确定度','B  Uncertainty beyond repeatability'))
for j,v in enumerate(components):ax.text(v+.08,j,f'{v:.2f}%',va='center')
ax.text(.1,4.3,L('认证迁移率：−4.5 ± 0.4\n单位：10⁻⁸ m²/(V s)，k = 2','Certified mobility: −4.5 ± 0.4\nUnit: 10⁻⁸ m²/(V s), k = 2'),fontsize=11,color=B)
ax.text(.1,5.25,L('由迁移率换算：ζ = −58 ± 5 mV','Converted from mobility: ζ = −58 ± 5 mV'),fontsize=11,color=K)
save(fig,'reference-and-uncertainty')

summary={'seed':820,'true_mobility_m2_Vs':mu,'fitted_mobility_m2_Vs':mf,'fitted_zeta_mV':zf*1000,'fitted_constant_drift_um_s':bf*1e6,'EOF_apparent_mobility_m2_Vs':mu+.5e-8,'Debye_length_at1mM_nm':float(debye(1)*1e9),'Debye_ratio_1_to100mM':float(debye(1)/debye(100)),'planar_zeta_at1mM_mV':float(-15*np.exp(-1/(debye(1)*1e9))),'planar_zeta_at100mM_mV':float(-15*np.exp(-1/(debye(100)*1e9))),'reference_dataset_count':len(names),'reference_aliquot_count':int(data.size),'mean_of_reference_dataset_means_1e8':float(means.mean()),'reference_Smoluchowski_mV':-4.5e-8*eta/eps*1000,'reference_Huckel_mV':-4.5e-8*3*eta/(2*eps)*1000,'expanded_relative_from_rounded_components_percent':float(urel),'phase_residual_RMS_rad':float(np.sqrt(np.mean(residuals**2)))}
(O/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
```

A comparison of two formulations can now begin with a focused question: did a coating alter interfacial electrical behavior, did salt alter interaction range, or did aggregation develop during storage? Record mobility, conversion model, ζ and its repeat distribution under matched conditions, then compare them with size and time-dependent behavior. A line of millivolt values becomes an interpretable experiment when a reader can follow the chain from optical phase through motion and model to the material question.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/P02.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Ramaye et al.: NIST SP260-208, Certification of SRM1992/ERM-FD305](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.260-208.pdf)

   Mobility certification, measured aliquot means, expanded uncertainty and conversion convention.

   Numerical values from Tables E1.1, 11 and 12 of the joint NIST/JRC report, transcribed and plotted with attribution; original artwork and prose are not reproduced.
2. [Malvern: Zeta Potential, An Introduction](https://www.malvernpanalytical.com/en/learn/knowledge-center/technical-notes/tn101104zetapotentialintroduction)

   Interfacial ions, pH and steric stabilization.
3. [IUPAC Gold Book: Electrokinetic Potential](https://goldbook.iupac.org/terms/view/E01968)

   Definition of slipping-plane electrokinetic potential.
4. [Clogston & Vermilya: NCL Method PCC-2, Measuring Zeta Potential of Nanoparticles](https://dctd.cancer.gov/drug-discovery-development/assays/nano/ncl-methods-pcc2.pdf)

   Specimens, cells, concentration, phase diagnostics and reporting conditions.
5. [Malvern: Measuring Zeta Potential Using PALS](https://www.malvernpanalytical.com/en/learn/knowledge-center/technical-notes/tn101104phaseanalysislightscattering)

   How phase slope yields velocity.
6. [Malvern: M3-PALS and Electro-osmosis](https://www.malvernpanalytical.com/en/learn/knowledge-center/application-notes/an101104zetapotentialm3-pals)

   Electro-osmosis, observation position and field-reversal dynamics.
7. [Royal Society Archives: Henry (1931) Cataphoresis Paper, RR43/57](https://makingscience.royalsociety.org/items/rr_43_57/referees-report-by-frederick-alexander-lindemann-on-a-paper-the-cataphoresis-of-suspended-particles-part-ithe-equation-of-cataphoresis-by-d-c-henry)

   Historical record of Henry’s 1931 work.
