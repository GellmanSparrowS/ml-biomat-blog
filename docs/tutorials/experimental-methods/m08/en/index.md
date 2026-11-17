# Rotational and oscillatory rheology: From flow to gel networks

Source: https://ml-biomat.com/tutorials/experimental-methods/m08/en/
Language: en

Separate viscosity, shear thinning, wall slip and structural recovery, and connect rheological curves to formulation, processing and biomaterial questions.

## From whether a material pours to how it flows and recovers

Honey, toothpaste, protein solutions and hydrogels can all appear thick, yet the reasons for their behavior differ. Honey flows continuously, toothpaste may retain its shape under a small disturbance, some polymer solutions become easier to move as stirring increases, and an injectable gel may need to regain support after passing through a needle. Rotational and oscillatory rheology separates these experiences into measurable questions. How does resistance change with flow rate? How much stress is associated with storage and loss during gentle back-and-forth shear? How quickly does structure recover after strong shearing? These questions connect formulation to processing, delivery and the conditions of actual use.

Picture sliding the upper cards in a deck sideways. Each layer moves relative to the one below, changing the stack's shape rather than translating every card together. Neighboring liquid layers can likewise have different velocities. Velocity change divided by the distance between layers defines a shear rate. A rotational rheometer places a specimen between plates, a cone and a plate, or concentric cylinders, imposes motion by rotation and measures the resisting torque. The directly observed quantities are angle, angular speed and torque. Shear stress and shear rate follow from a geometry-dependent conversion, which is part of the scientific interpretation rather than a detail hidden inside the software.

This measurement approach has longstanding biological connections. In 1923, du Noüy described a viscometer intended for colloidal and physiological liquids, including small volumes of serum, with attention to changes over time and temperature. The same practical issues remain relevant to protein formulations, cell suspensions and bioinks: sample volume may be limited, the specimen may evolve, and the measurement must separate material behavior from handling effects. Modern instruments add precise control and varied loading programs, while retaining the same fundamental question. What flow and what specimen state produced the resistance being measured?

![Original principle diagrams of parallel plates, cone-and-plate and concentric cylinders. Geometry determines shear distribution. The historical note connects rotational measurement with 1923 work on small physiological-fluid samples.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/14a2c14b2f410bba90429fa2.svg?v=14a2c14b2f41)

Figure 1Original principle diagrams of parallel plates, cone-and-plate and concentric cylinders. Geometry determines shear distribution. The historical note connects rotational measurement with 1923 work on small physiological-fluid samples.

## Choose the geometry before interpreting the reported quantities

The simplest picture uses two parallel plates, with the lower plate stationary and the upper plate translating at a constant speed. If liquid adheres to both surfaces and the steady velocity profile is linear, the velocity difference divided by the gap is the shear rate. Shear stress is tangential force per area, while viscosity describes the stress required to sustain a unit shear rate. Its unit, Pa·s, combines stress and time. Viscosity differs from density: density describes mass in a volume, whereas viscosity describes resistance to relative motion between neighboring fluid layers. A heavy liquid need not be a highly viscous one.

The reciprocal second in shear rate describes how quickly relative deformation accumulates; it does not count rotor revolutions. A top-plate speed of 1 mm/s across a 1 mm planar gap gives a rate of 1 s⁻¹. Halving the gap while holding speed fixed doubles the rate. A liquid with viscosity 2 Pa·s then experiences shear stresses of 2 Pa and 4 Pa respectively. This example connects speed, distance and resistance. It also explains why a reported rotational speed without geometry does not establish the actual shear experienced by the sample.

$$
\dot\gamma=\frac{U}{h},\qquad \sigma=\eta\dot\gamma
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/eda43fd5c758e326ab3f7398.svg) | Shear rate in simple planar flow, s⁻¹; the dot indicates a rate of change. |
| ![Formula](https://ml-biomat.com/static/agent-math/c3ae10e66e0dee45c359329a.svg) | Difference between wall velocities, m/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | Distance between walls, m. |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | Shear stress, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | Newtonian viscosity, Pa·s. |

For no-slip steady planar flow with a linear velocity profile, U=0.001 m/s and h=0.001 m give 1 s⁻¹. With η=2 Pa·s, stress is 2 Pa. Rotational geometries require their corresponding radius and torque conversions.

A rotating parallel plate adds an important geometric feature. At a fixed angular speed, linear speed increases with distance from the axis, so shear rate varies across the radius. Software may report an edge or otherwise specified rate and process torque using the corresponding assumptions. A cone-and-plate arrangement makes the gap increase with radius, producing approximately uniform shear over most of the sample under small-angle, correctly set and ideal-flow conditions. Concentric cylinders confine liquid to an annular space and suit many low-viscosity specimens that might otherwise escape a plate gap. The geometries therefore differ in how the specimen experiences shear, not simply in container shape.

For particle- or cell-containing samples, compare the gap with the largest particles or aggregates. A narrow gap can compress particles, trap them or modify local flow, adding geometric confinement to the measured resistance. The small region near a cone tip deserves particular attention. Increasing gap can make it harder to retain the sample, and low-viscosity liquids may become more susceptible to inertia or secondary flows. Consider particle size, sample volume, viscosity range, temperature changes and the desired shear-rate range together. This makes geometry selection a deliberate part of the experiment rather than a standard fixture choice followed by attempts to explain every unusual curve.

Loading the specimen already applies shear. Extrusion, pipetting, lowering the upper tool and trimming the edge may temporarily disrupt a fragile network. The rest after loading should therefore reflect structural recovery. Parallel plates require correct zero-gap setting and a specimen edge matching the effective measurement radius. Overfilling or underfilling changes torque conversion. Bubbles reduce contact, evaporation changes concentration, and edge fracture can remove part of the sample from uniform shearing. Observing the edge together with normal force and torque helps connect these events to anomalies in the measured curve.

Comparisons between formulations benefit from matching loading order, preshear, rest and temperature history. Preshear can establish a consistent starting state but may also change a network irreversibly, so its use should follow the research purpose. For a mixture that begins gelling immediately, record the time between mixing and measurement. For a material examined after extrusion, define the extrusion and recovery history. These times identify which structural state actually reached the instrument. They can explain why nominally identical compositions produce different responses, and help distinguish a preparation effect from an intrinsic difference between formulations.

A reference liquid with known viscosity at a defined temperature helps separate instrument and geometry issues from complex material behavior. Choose a reference covering a suitable torque range and match its stated temperature. If the reference also shows unexpected rate dependence, investigate range, inertia, temperature and loading first. A larger plate radius generally strengthens torque signals, while changing edge conditions and sample requirements. Calibration and specimen-specific method selection solve different questions: whether the instrument measures accurately, and whether the selected geometry and program describe the intended material response.

## Separate shear thinning, yielding and time dependence

At a specified temperature and composition, a Newtonian liquid has an approximately rate-independent viscosity and stress proportional to shear rate. A shear-thinning material has decreasing apparent viscosity as rate increases, potentially associated with chain orientation, aggregate rearrangement or other internal processes. Apparent here means viscosity defined as the current stress divided by the current shear rate; the term does not make the measurement less real. Stress may continue increasing while viscosity decreases. Moving the material faster still usually requires a larger force, but that force rises less rapidly than it would for a constant-viscosity reference.

A Carreau-type teaching model makes the transition between low and high rates visible. It has a low-rate viscosity plateau, a thinning region and a second plateau approached at sufficiently high rate. A time parameter sets the approximate onset of the transition, while an exponent controls the intermediate change. This is a timescale in an empirical response model and should not automatically be identified as the unique relaxation time of an individual molecular chain. The model summarizes the data compactly. Connecting its parameters to a microscopic mechanism requires complementary information about molecular weight, structure and the specimen's other properties.

$$
\eta(\dot\gamma)=\eta_\infty+(\eta_0-\eta_\infty)\left[1+(t_c\dot\gamma)^2\right]^{(n-1)/2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/55ca2da5874834a3d36c10a9.svg) | Model viscosity at the stated shear rate, Pa·s. |
| ![Formula](https://ml-biomat.com/static/agent-math/eda43fd5c758e326ab3f7398.svg) | Shear rate, s⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb4e0ab9086f7736b32cea50.svg) | Zero-rate limiting viscosity, Pa·s. |
| ![Formula](https://ml-biomat.com/static/agent-math/b784e2ff514e8c900372c5f3.svg) | High-rate limiting viscosity, Pa·s; ∞ denotes a limit. |
| ![Formula](https://ml-biomat.com/static/agent-math/2641a2efcec4baa36ea120b6.svg) | Time parameter controlling the transition location, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Intermediate-response exponent, dimensionless; this example uses 0<n<1. |

Use η₀=10 Pa·s, η∞=0.1 Pa·s, tc=2 s and n=0.4. The zero-rate limit is 10 Pa·s; viscosity at 1 s⁻¹ is approximately 6.209 Pa·s. The product tc×shear rate is dimensionless.

![One constructed flow dataset viewed as viscosity and stress. Noisy relative-error data and a Carreau fit appear on the left; stress can continue rising during shear thinning on the right. The Newtonian reference viscosity is 10 Pa·s.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/04ec6b13e7b557b7187caef4.svg?v=04ec6b13e7b5)

Figure 2One constructed flow dataset viewed as viscosity and stress. Noisy relative-error data and a Carreau fit appear on the left; stress can continue rising during shear thinning on the right. The Newtonian reference viscosity is 10 Pa·s.

When appreciable sustained flow begins after a sufficiently large applied action, yielding becomes relevant. The static yield response of a rested specimen during startup can differ from the dynamic yield behavior of a specimen already flowing. Waiting time, loading program and the selected criterion all affect the reported value. A low-rate extrapolated intercept is therefore not automatically a unique material constant. Combining stress-controlled creep, different rest periods and steady-flow measurements helps define which process the reported yield value describes. For an injectable gel, these distinctions can connect separately to the resistance to starting an injection and to maintaining it.

Shear thinning describes rate dependence, while thixotropy involves a time-dependent structural change with recovery. A direct question is whether viscosity continues changing after shear rate is held fixed. A loop between increasing- and decreasing-rate sweeps can reflect time dependence, but can also include temperature changes, evaporation or transient flow that has not stabilized. Vary point duration, compare sweep directions and inspect fixed-rate time records to investigate these possibilities. Low-rate points often require longer observation. A large number of closely spaced points with insufficient holding time can produce a visually detailed curve whose physical meaning remains poorly defined.

The constructed flow dataset spans six decades of shear rate, so logarithmic axes make both the low-rate plateau and high-rate transition readable. Equal distances on the horizontal axis represent equal ratios rather than equal rate differences. Fitting is performed in log viscosity because the constructed noise has an approximately constant relative magnitude. If an actual instrument instead has approximately fixed torque noise, low-stress observations can have larger relative uncertainty, requiring a different weighting scheme. The choice of fitting coordinates should therefore be discussed alongside the measurement's error model, rather than selected solely because one plot looks straighter.

Relate fitted plateaus to the measured range as well. If every observation lies in the intermediate thinning region, different low-rate plateaus and timescales may generate almost identical curves. Predictions outside the observed interval can then depend strongly on parameter choice. Longer measurements at sufficiently low rates, or independent information constraining a parameter, add useful evidence. The constructed example deliberately spans a broad range to reveal both sides of the transition. With measured data, display the actual coverage together with the fitted curve so that observations and model extensions remain distinguishable.

Zero-shear viscosity is the limit as shear rate approaches zero, rather than zero stress divided by zero rate for a stationary sample. A sufficiently low-rate plateau can support that limit, or a model compatible with the observations can estimate it. Either approach needs an observation duration that separates steady behavior from slow evolution. A logarithmic axis never contains zero, so even its leftmost plotted point represents a finite rate. Keeping this distinction clear separates a limiting parameter returned by software from a quantity directly sampled by the instrument. It also explains why slow measurements can remain essential even when a smooth fitted curve is already available.

## Is the material thinning, or is it sliding at the wall?

Imagine pushing a piece of gelatin with your palm. When your hand grips the surface, the gelatin deforms internally. A thin water layer may instead let the hand slide while the gelatin moves much less. A rheometer can encounter the same distinction: some plate motion is consumed by interface slip, and the rest produces bulk shear. Dividing total plate speed by gap then overestimates the internal shear rate and underestimates viscosity. Gels, suspensions and emulsions are among the systems in which this possibility deserves attention. The instrument measures transmitted resistance; it does not independently guarantee that every imposed displacement entered the sample's interior.

A specific model clarifies gap dependence. Assume a Newtonian bulk liquid with equal slip lengths at both walls. A slip length relates interfacial sliding to the internal velocity gradient and can be visualized by extending the linear fluid profile beyond a wall. With slip at both surfaces, total motion is distributed across bulk deformation and two interfaces. The effective velocity-change distance is consequently the physical gap plus twice the slip length. This yields a testable prediction: the same bulk liquid can appear less viscous in a narrower gap. The prediction arises from an explicit velocity profile, not from changing the liquid's intrinsic viscosity.

$$
\dot\gamma_{\mathrm{bulk}}=\frac{U}{h+2b},\qquad \eta_{\mathrm{app}}=\eta\frac{h}{h+2b},\qquad v_s=b\dot\gamma_{\mathrm{bulk}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/67700e02cb2f499190a144e7.svg) | True shear rate within the bulk liquid, s⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/c3ae10e66e0dee45c359329a.svg) | Difference between wall velocities, m/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | Physical gap, m. |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Equal slip length at each wall, m. |
| ![Formula](https://ml-biomat.com/static/agent-math/78a927dab1b242ae576337ff.svg) | Apparent viscosity using wall speed divided by gap as the rate, Pa·s. |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | Newtonian bulk viscosity, Pa·s. |
| ![Formula](https://ml-biomat.com/static/agent-math/45519a4b53cded8c1e2b5bac.svg) | Magnitude of slip velocity at either wall, m/s. |

Assume equal Navier slip at both walls, Newtonian bulk behavior and steady planar flow. For η=2 Pa·s, h=1 mm and b=0.2 mm, apparent viscosity is 2×1/(1+0.4)=1.428571 Pa·s. Use consistent length units within the expression.

![A planar Newtonian model with Navier slip at both walls. Velocity differences remain at the walls on the left. The right panel shows apparent gap dependence at a fixed true viscosity of 2 Pa·s. Curves are calculated from the stated model.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/299249a275ac5049377bd50b.svg?v=299249a275ac)

Figure 3A planar Newtonian model with Navier slip at both walls. Velocity differences remain at the walls on the left. The right panel shows apparent gap dependence at a fixed true viscosity of 2 Pa·s. Curves are calculated from the stated model.

For a bulk viscosity of 2 Pa·s, a gap of 1 mm and a slip length of 0.2 mm at each wall, the apparent viscosity is approximately 1.429 Pa·s. Increasing gap to 2 mm raises it to approximately 1.667 Pa·s while leaving bulk viscosity unchanged. Such gap dependence is a useful diagnostic clue. Real samples can also change structure, temperature or particle confinement when gap changes, so comparisons should include surface roughness and time history. Roughened plates, patterned plates or a vane can reduce particular forms of slip, while their effects on local flow must also be considered.

## Interactive experiment: How much motion enters the fluid bulk?

Bulk viscosity remains 2 Pa·s. Change gap, slip length and wall speed to inspect the velocity profile and viscosity inferred under a no-slip assumption.

[Figure: Fluid velocity profile](https://ml-biomat.com/tutorials/experimental-methods/m08/en/#M08-plot)

The interactive display separates wall motion into a fluid velocity profile and slip at the two ends. Set slip length to zero first and confirm that apparent viscosity becomes independent of gap. Increase slip length and observe the wall–fluid velocity differences. Then vary gap and compare reported viscosity with the true internal shear rate. The example uses planar, uniform and steady Newtonian flow to isolate the diagnostic logic. Non-Newtonian samples or more complicated rotational geometries require the corresponding flow relations, while preserving the underlying question: how much of the tool's motion actually deformed the sample?

## Gently reverse shear and watch a network form

A rotational rheometer can oscillate through a small angle instead of turning continuously. In small-amplitude shear, stress separates into components synchronized with strain and shifted by a quarter-cycle, giving shear storage and loss moduli. This is the same phase decomposition used in DMA, with the deformation mode changed to shear. An amplitude sweep helps establish a linear range; a frequency sweep describes behavior across timescales; a time sweep follows gel formation, recovery or aging. Matching the sweep type to the research question prevents a single fixed-frequency result from carrying more interpretation than its measurement provides.

$$
\gamma(t)=\gamma_0\sin(\omega t),\qquad \sigma(t)=\gamma_0\!\left[G^{\prime}\sin(\omega t)+G^{\prime\prime}\cos(\omega t)\right],\qquad \tan\delta=\frac{G^{\prime\prime}}{G^{\prime}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/29b9e33d3a0db087be052d2e.svg) | Shear strain, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/97e4157d29a2b15aac854b6c.svg) | Shear-strain amplitude, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/ff305b24b1ce5e15f22817d6.svg) | Shear stress, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/85160d4b7cf0a0fe234b2a1a.svg) | Shear storage modulus, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/d513ad606518673291bd21cf.svg) | Shear loss modulus, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/2cb3a34686b80c6ea9a5a2e4.svg) | Angular frequency, rad/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/e5b7c4267da3b3fe02d6ae1a.svg) | Phase by which stress leads strain, rad. |
| ![Formula](https://ml-biomat.com/static/agent-math/7cfe4f0d59119c3e45744c16.svg) | Loss factor, dimensionless. |

These relations apply to steady small-amplitude linear shear. With G′=100 Pa, G″=50 Pa and strain amplitude 0.01, the two stress-component amplitudes are 1 Pa and 0.5 Pa; the loss factor is 0.5.

For a gelling system, storage and loss moduli are often plotted against time, with their crossing used as a convenient process marker. The meaning of that crossing depends on measurement frequency. A more physical critical-gel criterion compares several frequencies: at an appropriate critical state, both moduli follow the same frequency power law, making the loss factor approximately independent of frequency. Work by Winter and Chambon on crosslinking polymers in the 1980 s established this frequency structure as an important way to examine the gel point. The question advances from which line lies above the other to how the response is organized across timescales.

$$
G^{\prime}=Q\omega^n\cos\!\left(\frac{n\pi}{2}\right),\qquad G^{\prime\prime}=Q\omega^n\sin\!\left(\frac{n\pi}{2}\right),\qquad \tan\delta=\tan\!\left(\frac{n\pi}{2}\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/85160d4b7cf0a0fe234b2a1a.svg) | Storage modulus of the critical power-law model, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/d513ad606518673291bd21cf.svg) | Loss modulus of the critical power-law model, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/4be111afe7c23428ae5024a8.svg) | Positive coefficient of this frequency model, Pa·sⁿ. |
| ![Formula](https://ml-biomat.com/static/agent-math/2cb3a34686b80c6ea9a5a2e4.svg) | Angular frequency, rad/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Critical power-law exponent, dimensionless, 0<n<1; independent of the earlier Carreau-model exponent. |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | Circle constant, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/e5b7c4267da3b3fe02d6ae1a.svg) | Phase angle, rad. |

The moduli share the same frequency factor, which cancels in their ratio. The loss factor is therefore frequency-independent. At n=0.4, tanδ≈0.7265; at n=0.5 it equals one and the moduli coincide.

![Three critical power-law models illustrate the frequency structure behind the Winter–Chambon criterion. Storage and loss share an exponent and a frequency-independent ratio. The curves coincide only at exponent 0.5. Constructed spectra compare the criteria.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/2563acf1e6d9d80fd130818a.svg?v=2563acf1e6d9)

Figure 4Three critical power-law models illustrate the frequency structure behind the Winter–Chambon criterion. Storage and loss share an exponent and a frequency-independent ratio. The curves coincide only at exponent 0.5. Constructed spectra compare the criteria.

The three constructed critical spectra use different power-law exponents. At an exponent of 0.5, storage and loss coincide. At 0.4, storage remains greater; at 0.7, loss remains greater. In all three examples, the loss factor is independent of frequency. Equality of the two moduli is therefore a special case rather than a universal definition of gelation. An experimental test requires an accessible frequency range, linear amplitudes and a sufficiently stable state during measurement. If reaction is rapid, a sequential frequency sweep can confuse time evolution with frequency dependence, making acquisition timing part of the criterion's practical application.

For a cell-containing bioink, a larger small-amplitude storage modulus can help describe shape support at rest, while passage through a needle usually involves deformation beyond that linear regime. Steady flow, startup and recovery measurements need to be connected when discussing processing and shape retention. Forces acting on cells also depend on needle geometry, flow rate and local flow structure. A material modulus alone does not determine cell viability. Rheology helps define the mechanical environment, and cellular assays examine the biological response. Connecting them at their respective scales makes their roles in a research argument clear.

Read ratios alongside absolute magnitudes. Two specimens can share a loss factor of 0.5 while having storage moduli of 100 Pa and 10000 Pa. Their modulus ratios match, yet the latter requires one hundred times the stress for the same small shear strain. Normalizing curves helps compare shapes but hides this load-bearing difference. Retaining both actual moduli and relative ratios describes how strongly the material resists deformation and how its response components are divided. The same principle supports reporting recovery fractions together with the underlying viscosity values.

## Turn recovery after strong shear into useful information

A three-interval experiment first measures an initial state under gentle shear or small-amplitude oscillation, then applies strong shearing, and finally returns to the original gentle conditions to follow recovery. Matching the first and third conditions matters: otherwise the changed reading may simply reflect a different shear rate. The strong interval should relate to the intended use, perhaps approximating part of mixing, coating or extrusion, while retaining its actual imposed history. Report the time needed to reach a specified recovery fraction or the fraction reached at a specified time. These definitions connect the result to a use window more directly than a general statement that the material recovers.

The teaching example introduces a structural variable between zero and one to represent relative structural integrity within a model. Rest or gentle shear allows rebuilding, while stronger shear accelerates breakdown. Both processes operate together, with their competition setting the eventual state. This variable is internal to the teaching model; it is not a crosslink fraction measured directly by the instrument. The program maps it linearly to viscosity to show how a finite rebuilding time produces a gradual rise in the third interval. Real specimens may contain several recovery processes, so observations should guide the complexity used to describe them.

$$
\frac{\mathrm{d}q}{\mathrm{d}t}=\frac{1-q}{t_r}-k|\dot\gamma|q,\qquad \eta(t)=\eta_{\min}+(\eta_{\max}-\eta_{\min})q(t)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | Relative structural integrity in the teaching model, dimensionless, 0≤q≤1. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/b6e2c601f1fac12ffd56a65e.svg) | Rate of change of the structural variable, s⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/ce7b3f4467a12e80e6af8d40.svg) | Structural rebuilding time parameter, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | Shear-breakdown coefficient, dimensionless in this expression. |
| ![Formula](https://ml-biomat.com/static/agent-math/eda43fd5c758e326ab3f7398.svg) | Shear rate, s⁻¹; absolute-value bars retain its magnitude. |
| ![Formula](https://ml-biomat.com/static/agent-math/149f9d508f1c76e4c344a227.svg) | Viscosity associated with the structural model, Pa·s. |
| ![Formula](https://ml-biomat.com/static/agent-math/60fc16ed766ca41bd115bfae.svg) | Viscosity at zero structural variable, Pa·s. |
| ![Formula](https://ml-biomat.com/static/agent-math/a98e02d685fd171c3442f4f7.svg) | Viscosity at unit structural variable, Pa·s. |

The first term rebuilds structure and the second breaks it down under shear. For tr=60 s and k=0.01, equilibrium q is approximately 0.01639 at 100 s⁻¹ and 0.9434 at 0.1 s⁻¹. The program uses the analytical solution within each constant-rate interval.

![An independent structural-kinetics teaching model uses 0.1 s⁻¹, 100 s⁻¹ and 0.1 s⁻¹ for gentle observation, strong shearing and recovery. Viscosity is mapped from this model’s structural variable; this is a separate model from the earlier Carreau fluid.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/a001cf0535a5b23635928da2.svg?v=a001cf0535a5)

Figure 5An independent structural-kinetics teaching model uses 0.1 s⁻¹, 100 s⁻¹ and 0.1 s⁻¹ for gentle observation, strong shearing and recovery. Viscosity is mapped from this model’s structural variable; this is a separate model from the earlier Carreau fluid.

The example uses a low rate of 0.1 s⁻¹, a high rate of 100 s⁻¹, a 30 s high-shear interval and 150 s of subsequent low-shear recovery. The response does not return immediately to its initial value because rebuilding takes time and even the gentle shear retains a small breakdown contribution. Complete rest would change both the equilibrium structural state and the recovery trajectory. When reporting a percentage, specify whether its denominator is the initial steady value, an initial instantaneous reading or another reference. Otherwise matching percentages can describe different comparisons, making apparently similar recovery claims difficult to interpret.

A rising recovery trace should also be separated from concentration increase through evaporation, cooling or continuing chemical crosslinking. A solvent trap, stable temperature and a time-matched control that avoids strong shearing help distinguish these contributions. If processing changes the specimen permanently, the subsequent curve describes a new state. If rest progressively returns it toward its original response, reversible structural recovery becomes an appropriate question. Repeated three-interval tests can additionally reveal accumulated changes over successive processing events, which matters for repeated coating, printing and cyclic use.

## Keep measurement definitions in the code and connect conclusions to use

The complete program contains independent constructed examples with separate purposes. Carreau flow data teach fitting and the relation between stress and viscosity. A constant-viscosity slip model explains gap diagnostics. Structural kinetics illustrates three-interval recovery. Critical-gel spectra compare power-law exponents. These are not four processing methods applied to a single material record; each example declares its own parameters and assumptions. The arrangement lets each plot answer one identifiable question and avoids assigning a single model physical capabilities it does not possess simply to display more phenomena.

### Complete example: Flow, slip, recovery and critical spectra

Four independent constructed models address fitting, gap diagnostics, recovery and critical-gel criteria, with their parameters and outputs retained explicitly.

```
"""Rotational rheometry: constructed flow, slip, recovery and critical-gel examples."""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Rectangle,FancyArrowPatch


def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def carreau(rate,eta0=10.,eta_inf=.1,time_scale=2.,exponent=.4):
    return eta_inf+(eta0-eta_inf)*(1+(time_scale*np.asarray(rate))**2)**((exponent-1)/2)


def apparent_viscosity(gap_mm,slip_mm=.2,eta=2.):
    return eta*np.asarray(gap_mm)/(np.asarray(gap_mm)+2*slip_mm)


def structure_segment(t,initial,rate,recovery_time=60.,breakdown=.01):
    speed=1/recovery_time+breakdown*rate
    equilibrium=(1/recovery_time)/speed
    return equilibrium+(initial-equilibrium)*np.exp(-speed*np.asarray(t))


def main(output,language):
    from matplotlib import font_manager
    output.mkdir(parents=True,exist_ok=True)
    fonts={f.name for f in font_manager.fontManager.ttflist};font=next((x for x in ['Microsoft YaHei','Noto Sans CJK SC','SimHei'] if x in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[font,'DejaVu Sans'] if language=='zh' else ['DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','axes.prop_cycle':plt.cycler(color=['#186e83','#cd803f','#8160a1','#3c8a6a'])})
    tr=lambda z,e:z if language=='zh' else _label(e)
    def save(fig,name):fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    rate=np.geomspace(.001,1000,181);true_eta=carreau(rate)
    observed_eta=true_eta*np.exp(np.random.default_rng(808).normal(0,.025,rate.size))
    def model(lograte,*p):return np.log(carreau(np.exp(lograte),np.exp(p[0]),np.exp(p[1]),np.exp(p[2]),p[3]))
    fit,cov=curve_fit(model,np.log(rate),np.log(observed_eta),p0=[np.log(10),np.log(.1),np.log(2),.4],bounds=([np.log(1),np.log(.001),np.log(.01),.05],[np.log(100),np.log(1),np.log(100),.95]))
    fit_values=[*np.exp(fit[:3]),fit[3]];predicted=carreau(rate,*fit_values)
    t1=np.linspace(0,60,121,endpoint=False);l1=structure_segment(t1,1,.1)
    start2=float(structure_segment(60,1,.1));t2=np.linspace(60,90,61,endpoint=False);l2=structure_segment(t2-60,start2,100)
    start3=float(structure_segment(30,start2,100));t3=np.linspace(90,240,301);l3=structure_segment(t3-90,start3,.1)
    times=np.r_[t1,t2,t3];structure=np.r_[l1,l2,l3];rates=np.r_[np.full(t1.size,.1),np.full(t2.size,100),np.full(t3.size,.1)];eta_time=.1+9.9*structure
    summary={'data_kind':'independent constructed teaching models','carreau_zero_rate_eta_Pa_s':float(carreau(0)),'carreau_eta_at_1_Pa_s':float(carreau(1)),
     'apparent_eta_1mm_Pa_s':float(apparent_viscosity(1)),'slip_fraction_1mm':.2/1.4,'critical_gel_tan_delta_n04':float(np.tan(.4*np.pi/2)),
     'structure_at_90s':start3,'structure_at_240s':float(l3[-1]),'fitted':dict(zip(['eta0_Pa_s','eta_inf_Pa_s','time_scale_s','exponent'],map(float,fit_values)))}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    np.savetxt(output/'flow.csv',np.c_[rate,true_eta,observed_eta,predicted,rate*observed_eta],delimiter=',',comments='',header='shear_rate_s_inverse,true_eta_Pa_s,observed_eta_Pa_s,fitted_eta_Pa_s,observed_stress_Pa')
    np.savetxt(output/'recovery.csv',np.c_[times,rates,structure,eta_time],delimiter=',',comments='',header='time_s,shear_rate_s_inverse,structure_fraction,viscosity_Pa_s')

    fig,axes=plt.subplots(1,3,figsize=(12,4.5),layout='constrained')
    for ax in axes:ax.set(xlim=(0,10),ylim=(0,10));ax.axis('off')
    a,b,c=axes
    a.set_title(tr('A  平行板','A  Parallel plates'),loc='left',fontweight='bold')
    for y in [3,6]:a.add_patch(Rectangle((1,y),8,.6,facecolor='#85969e'))
    a.add_patch(Rectangle((1,3.6),8,2.4,facecolor='#c0ddda',alpha=.85));a.add_patch(FancyArrowPatch((2,7.5),(8,7.5),arrowstyle='-|>',mutation_scale=16,color='#cc803f',lw=2))
    a.text(5,1.6,tr('间隙可调；剪切速率随半径变化','Adjustable gap; shear rate varies with radius'),ha='center',fontsize=9)
    b.set_title(tr('B  锥板','B  Cone and plate'),loc='left',fontweight='bold')
    b.add_patch(Rectangle((1,3),8,.6,facecolor='#85969e'));b.add_patch(Polygon([[1,4.8],[5,4],[9,4.8]],facecolor='#85969e'))
    b.add_patch(Polygon([[1,3.6],[9,3.6],[9,4.8],[5,4],[1,4.8]],facecolor='#c0ddda',alpha=.8));b.text(5,1.6,tr('小锥角；理想条件下剪切近均匀','Small cone angle; nearly uniform ideal shear'),ha='center',fontsize=9)
    c.set_title(tr('C  同轴圆筒与生物流体','C  Concentric cylinders and biofluids'),loc='left',fontweight='bold')
    c.add_patch(Rectangle((1.5,2.8),7,4.8,facecolor='#c0ddda',edgecolor='#85969e',lw=3));c.add_patch(Rectangle((3.4,4),3.2,4.2,facecolor='#85969e'));c.plot([5,5],[8.2,9],color='#85969e',lw=5)
    c.text(5,1.3,tr('1923：du Noüy 关注血清等小体积样品','1923: du Noüy studied small-volume biofluids'),ha='center',fontsize=9)
    fig.suptitle(tr('现代测量几何与生物流体黏度研究的联系','Modern measurement geometries and their connection to biofluid viscosity'),fontsize=10,y=-.01)
    save(fig,'geometry')

    fig,axs=plt.subplots(1,2,figsize=(12,4.7),layout='constrained')
    axs[0].loglog(rate,observed_eta,'o',ms=3,alpha=.5,label=tr('构造观测','Constructed observations'));axs[0].loglog(rate,predicted,lw=2,label=tr('Carreau 拟合','Carreau fit'))
    axs[0].set(xlabel=tr('剪切速率 / s⁻¹','Shear rate / s⁻¹'),ylabel=tr('黏度 / Pa·s','Viscosity / Pa·s'),title=tr('A  降低的黏度与两个平台','A  Falling viscosity and two plateaus'));axs[0].legend(frameon=False,fontsize=9)
    axs[1].loglog(rate,rate*true_eta,lw=2,label=tr('同一材料的应力','Stress for the same material'));axs[1].loglog(rate,rate*10,ls='--',lw=1.5,label=tr('10 Pa·s 牛顿参照','Newtonian reference, 10 Pa·s'))
    axs[1].set(xlabel=tr('剪切速率 / s⁻¹','Shear rate / s⁻¹'),ylabel=tr('剪切应力 / Pa','Shear stress / Pa'),title=tr('B  黏度下降时，应力仍可上升','B  Stress can rise while viscosity falls'));axs[1].legend(frameon=False,fontsize=9)
    for ax in axs:ax.grid(alpha=.13)
    save(fig,'flow')

    fig,axs=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
    y=np.linspace(0,1,101);b=.2;h=1.;vel=(b+y*h)/(h+2*b)
    axs[0].plot(y,y,'--',label=tr('无滑移','No slip'),color='#9aabb0');axs[0].plot(vel,y,lw=3,label=tr('两壁滑移','Slip at both walls'))
    axs[0].plot([0,vel[0]],[0,0],color='#cc803f',lw=4);axs[0].plot([vel[-1],1],[1,1],color='#cc803f',lw=4)
    axs[0].set(xlabel=tr('流体速度 / 上壁速度','Fluid velocity / top-wall velocity'),ylabel=tr('高度 / 间隙','Height / gap'),title=tr('A  运动分给了界面与体相','A  Motion is shared by interfaces and bulk'));axs[0].legend(frameon=False,fontsize=9)
    gaps=np.linspace(.2,2,201)
    for slip in [0,.1,.2,.4]:axs[1].plot(gaps,apparent_viscosity(gaps,slip),lw=2,label=f'b={slip} mm')
    axs[1].set(xlabel=tr('间隙 / mm','Gap / mm'),ylabel=tr('表观黏度 / Pa·s','Apparent viscosity / Pa·s'),title=tr('B  真实黏度相同，间隙依赖不同','B  Same bulk viscosity, different gap dependence'));axs[1].legend(frameon=False,fontsize=9)
    save(fig,'slip')

    fig,axs=plt.subplots(2,1,figsize=(11,6.4),sharex=True,layout='constrained',gridspec_kw={'height_ratios':[1,2]})
    axs[0].step(times,rates,where='post',color='#cc803f',lw=2);axs[0].set_yscale('log');axs[0].set(ylabel=tr('剪切速率 / s⁻¹','Shear rate / s⁻¹'),title=tr('A  低剪切—高剪切—低剪切','A  Low shear – high shear – low shear'))
    axs[1].plot(times,eta_time,lw=2.5);axs[1].axvspan(60,90,color='#cc803f',alpha=.1)
    axs[1].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('模型黏度 / Pa·s','Model viscosity / Pa·s'),title=tr('B  恢复有自己的时间尺度','B  Recovery has its own timescale'))
    save(fig,'recovery')

    fig,axes=plt.subplots(1,3,figsize=(12,4.2),layout='constrained');w=np.geomspace(.1,100,150)
    for ax,n in zip(axes,[.4,.5,.7]):
        gp=100*w**n*np.cos(n*np.pi/2);gpp=100*w**n*np.sin(n*np.pi/2)
        ax.loglog(w,gp,lw=2,label='G′');ax.loglog(w,gpp,'--',lw=2,label='G″');ax.set(xlabel=tr('角频率 / rad·s⁻¹','Angular frequency / rad·s⁻¹'),ylabel=tr('模量 / Pa','Modulus / Pa'),title=f'n={n}; tan δ={np.tan(n*np.pi/2):.3f}');ax.legend(frameon=False,fontsize=9)
    fig.suptitle(tr('临界凝胶的频率判据：同一幂律，不要求处处 G′=G″','Critical-gel frequency criterion: a common power law, not universal G′=G″'),fontsize=13)
    save(fig,'gel')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();main(a.output,a.language)
```

After running the program, check the zero-rate plateau of 10 Pa·s, the slip-affected apparent viscosity of approximately 1.429 Pa·s at a 1 mm gap, and the critical loss factor of approximately 0.727 for an exponent of 0.4. Change noise to investigate fitting stability, alter gap and slip length to examine geometry effects, and vary rebuilding time to explore recovery. The exported flow.csv and recovery.csv retain quantities with explicit units, while summary.json contains numerical checks. Before inserting an instrument export, identify its column names, units, geometry definition and loading history, then replace the corresponding example rather than mixing unrelated records.

Choose reported metrics according to the intended use. Pumping calls for flow resistance at specified rate and temperature. Retaining shape after placement calls for elasticity, yielding or creep over the relevant duration. Reuse after processing calls for recovery and repeated-treatment information. Report geometry, gap, surface condition, loading and waiting times, temperature control, sweep program and independent specimen count. Instrument names identify the tool used; measurement definitions and physical interpretation identify the question the curve answers. Together they turn a visually appealing graph into evidence that another researcher can understand and compare.

Preserve differences between independent specimens in the presentation. Dozens of frequency points from one loading describe one specimen under different conditions. Curves from independent preparations and loadings additionally describe repeatability of formulation and handling. Thin lines can show individual measurements, accompanied by summaries at defined conditions and an explanation of whether error bars represent standard deviation, standard error or another interval. Evolving specimens also need a consistent time origin. This presentation distinguishes curve detail, repeatability and formulation differences without treating dense sampling as a large number of independent experiments.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/M08.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [TA Instruments — Core Rheometry: Yield Stress, Time-dependency, and Rheometry Tips](https://www.tainstruments.com/applications-notes/core-rheometry-yield-stress-time-dependency-and-rheometry-tips-rh146/)

   Experimental design for flow, thixotropy and wall slip.
2. [TA Instruments — Yield Stress and Time-Dependency: Practical Rheology](https://www.tainstruments.com/applications-notes/yield-stress-time-dependency-practical-rheology-rh151/)

   Distinguishing wall slip from apparent differences caused by time dependence.
3. [Anton Paar — Avoid Measurement Errors in Rheometry](https://wiki.anton-paar.com/ie-en/avoid-measurement-errors-in-rheometry/)

   Geometry, loading, instrument range, evaporation and edge observation.
4. [P. Lecomte du Noüy (1923) — A New Viscometer](https://pmc.ncbi.nlm.nih.gov/articles/PMC2140572/)

   Historical viscosity measurements of small physiological-fluid samples.
5. [Winter and Chambon (1986) — Analysis of Linear Viscoelasticity of a Crosslinking Polymer at the Gel Point](https://doi.org/10.1122/1.549853)

   Original study of the critical-gel frequency criterion.
6. [Yucel et al. — Direct Observation of Early-Time Hydrogelation in β-Hairpin Peptide Self-Assembly](https://pmc.ncbi.nlm.nih.gov/articles/PMC2630258/)

   Frequency dependence and gel criteria in a biomolecular self-assembly system.
7. [RepTate — LVE Theories](https://reptate.readthedocs.io/manual/Applications/LVE/Theory/theory.html)

   Further reading on linear viscoelastic spectra and Carreau–Yasuda models.
8. [SciPy — curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

   Fit bounds, error weighting and parameter interpretation.
