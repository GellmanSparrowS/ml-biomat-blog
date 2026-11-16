# Flow and Recovery: Understanding Polymer Viscoelasticity

Source: https://ml-biomat.com/tutorials/biomaterials-courses/pm12/en/
Language: en

Why does plastic deform slowly, and why does a melt remember the die it has just passed through? Begin with force, deformation and rate, then use relaxation, creep and oscillation to trace molecular timescales and connect temperature, flow instabilities and rheometry to processing.

## Why one material follows several clocks

A plastic clip can grip firmly when first assembled and lose some holding force over time. A rubber strip resists a rapid pull differently from a slow one. Molten plastic can expand sideways after leaving a narrow die. These observations connect the recovery associated with solids to the flow associated with liquids. A material can temporarily store deformation energy while dissipating energy through internal motion. This combination is viscoelasticity. Understanding its timing helps with seals, vibration damping, extrusion, fiber spinning and sustained loads.

A spring and a slowly moving piston provide useful reference behaviors. An ideal spring deforms under force and returns its stored energy when unloaded. A piston moving through a viscous fluid continues moving under sustained force, converting mechanical work into heat; removing the force does not return it automatically. Polymers contain no literal springs or pistons. The elements represent storage and flow. Connecting them reveals which parts of a loading response occur immediately, which require time, and which deformation can remain after loading ends.

Molecules contain atoms joined by chemical bonds, and polymer molecules often resemble long flexible chains. A short section changes direction through bond rotations. A larger section needs surrounding chains to make room, while the whole molecule changes position through many local adjustments. A polymer consequently possesses a range of motion times rather than one response speed. Entanglements constrain motion because long chains cannot readily pass through one another. Chemical crosslinks are persistent connections between chains. These two constraints have different consequences for long-time flow.

If observation is faster than a particular molecular motion, that motion cannot substantially relax the imposed deformation. Given enough time, it may change the stress considerably. This does not mean all molecules stop moving during a fast experiment; it means that some relevant relaxation processes remain incomplete. An uncrosslinked melt can eventually flow through whole-chain displacement, while a stable crosslinked network retains equilibrium support. Temperature, molecular length, branching, fillers and moisture shift these times. Different stiffnesses at different test speeds can therefore be understood as measurable structural responses.

Glass transition and long-time flow also need separate interpretations. Glass transition concerns whether segmental motion becomes active within the chosen observation time. Whole-chain escape from surrounding constraints generally takes longer. Crystals in a semicrystalline material provide additional fixing points, changing continuous load paths when they melt. An apparent flow temperature depends on imposed load and observation duration; an amorphous polymer need not possess a unique flow boundary analogous to a pure substance melting point. Decomposition likewise depends on both temperature and residence time. A processing window consequently balances sufficient flow against chemical stability over the actual manufacturing interval.

Rheology studies deformation and flow, including small-amplitude linear behavior and nonlinear processing that changes orientation or organization. Linear means proportionality to input amplitude and superposition of responses to small inputs. It does not mean that the response lacks time dependence. Establishing a common language for stress, deformation and rate allows sustained loading, sudden fixed deformation and repeated oscillation to be compared within one explanation.

## Separate force, deformation and the rate of deformation

Pressing a hand down on a table differs from sliding a book across it. Force divided by the area on which it acts is stress. Its perpendicular component is normal stress; its tangential component is shear stress. Different small surfaces can be imagined around a point, and each can carry forces in several directions. A complete stress state therefore requires several components. A second-order tensor organizes these components according to defined coordinate-transformation rules, commonly represented as a three-by-three array. It is more than simply a large number.

Let x denote flow direction, y the direction in which velocity changes, and z the third perpendicular direction. One convention defines σxy as force in the x direction acting on a surface whose normal points along y. Some conventions reverse the index order, making an explicit definition useful. Mass is a scalar with magnitude only. Velocity is a vector with magnitude and direction. Stress also asks which surface is being considered. Normal stress is not exclusively elastic, and shear stress is not exclusively viscous; the material relationship determines their response.

Simple shear resembles sliding the top of a stack of cards while holding the bottom fixed. Top displacement divided by the gap gives shear strain. If the top moves at constant speed, speed divided by gap gives shear rate. Strain describes accumulated deformation; rate describes how quickly more deformation is being added. A real fluid need not have a linear velocity profile. Its local rate is found by examining velocity changes between neighboring layers, a velocity gradient. Uniform-gap, no-slip plates provide the first numerical example.

Stress, strain, rate and viscosity in simple shearEq. 1

![Stress, strain, rate and viscosity in simple shear](https://ml-biomat.com/static/agent-math/aa3287b57495138534a65ea4.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| τ | Tangential shear stress | Pa |
| F | Force parallel to the plate | N |
| A | Plate–sample contact area | m² |
| γ | Shear strain | 1 |
| Δx | Top-plate displacement relative to the bottom | m |
| h | Plate gap | m |
| γ̇ | Shear strain added per second; the dot denotes a time rate | s⁻¹ |
| V | Relative top-plate speed | m/s |
| η | Shear viscosity under the specified conditions | Pa·s |
| Δ | Denotes a displacement change | 1 |

Reading the relationshipNormalize force by area, displacement by gap and speed by gap. Stress divided by rate gives the resistance associated with maintaining the flow.

A worked exampleF = 0.10 N and A = 0.001 m² give τ = 100 Pa. With h = 0.001 m and Δx = 0.0002 m, γ = 0.20. V = 0.010 m/s gives γ̇ = 10 s⁻¹ and η = 10 Pa·s.

ConditionsUniform gap, no wall slip and approximately uniform simple shear. Steady viscosity requires startup transients to decay; rate dependence is a material property.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pm12/en/#en-s2)

Figure 1 · Simple shear between plates. Horizontal arrows show velocity increasing with height. The upper plate moves while the bottom stays fixed; the sloping sides indicate shape change rather than volume compression.

Tension lengthens a specimen and commonly makes it narrower. Engineering strain uses initial length, and nominal stress uses initial cross-sectional area. At large deformation, true stress based on current area can differ substantially. Poisson’s ratio expresses transverse contraction relative to axial extension; its minus sign gives a positive value for ordinary lengthening-and-narrowing behavior. Bulk modulus measures resistance to volume change under uniform pressure. Shear modulus measures resistance to shape change. A liquid may change shape readily while remaining difficult to compress volumetrically.

Elastic responses in length, shape and volumeEq. 2

![Elastic responses in length, shape and volume](https://ml-biomat.com/static/agent-math/95a356b9ca96ce4067004a45.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| σ | Uniaxial tensile stress | MPa |
| E | Tensile elastic modulus | MPa |
| ε | Axial length change divided by initial length | 1 |
| τ | Shear stress | MPa |
| G | Shear elastic modulus | MPa |
| γ | Engineering shear strain | 1 |
| ν | Poisson ratio | 1 |
| εlat | Transverse strain, negative for contraction | 1 |
| p | Applied hydrostatic pressure increment, positive in compression | MPa |
| Kᴮ | Bulk modulus | MPa |
| ΔV、V₀ | Volume change and initial volume | m³ |
| lat、B、0 | Labels for lateral, bulk and initial state | 1 |

Reading the relationshipSmall-strain linear elasticity connects stress and strain through proportional constants. Minus signs account for lateral contraction under tension and volume reduction under positive pressure.

A worked exampleE = 3000 MPa and ε = 0.001 give σ = 3 MPa. If εlat = −0.0004, ν = 0.40. G = 1 MPa and γ = 0.02 give τ = 0.02 MPa. Kᴮ = 2000 MPa and ΔV/V₀ = −0.001 give p = 2 MPa.

ConditionsSeparate small-strain linear-elastic tests. The examples illustrate each mode independently rather than one material’s full constant set. Time dependence must be retained for viscoelastic materials.

Extension and shear are also distinct flows. In simple shear, velocity and its main gradient are perpendicular. In uniaxial extension, material farther along the stretching direction moves faster, so the velocity change is aligned with extension. Contraction entrances, film blowing, spinning and thinning liquid threads contain important extensional components. Two melts with similar shear viscosity can have different extensional viscosity and resistance to thinning. Measurements and models should match the deformation mode of the application.

Ideal linear elasticity relates stress directly to current small strain, with immediate recovery and no dissipation. Rubber can undergo much larger extension, with configurational entropy supplying an important restoring force. Entropy describes the number of available microscopic arrangements; stretching restricts those arrangements and thermal motion favors retraction. An ideal stable entropic network can become stiffer as absolute temperature increases. Real materials also undergo volume changes, hard-domain softening, crystallization and degradation. Delayed recovery and loss belong to their viscoelastic response rather than to ideal elasticity itself.

## What it means to flow more easily when sheared faster

For a Newtonian fluid at fixed temperature and pressure, shear stress is proportional to shear rate. The proportionality constant is viscosity, measured in pascal seconds. A larger viscosity requires greater stress to maintain the same rate. Water and many small-molecule liquids approximate this behavior over common experimental ranges. Polymer melts also commonly exhibit an approximately constant zero-shear viscosity at sufficiently low rates, where molecular relaxation can keep pace with the weak sustained disturbance.

At higher rates, orientation, stretching and the renewal of entanglement constraints can outpace recovery. Viscosity then decreases: shear thinning. Lower viscosity does not necessarily mean less force is needed. Stress may still increase with rate, just less rapidly than in a Newtonian proportional relationship. A power law conveniently describes a finite part of this curve through an exponent. For example, increasing rate tenfold with an exponent of one-half increases stress by the square root of ten, rather than by ten.

Power law over a finite flow rangeEq. 3

![Power law over a finite flow range](https://ml-biomat.com/static/agent-math/b9a78182046eff7fdcd11095.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| τ | Steady shear-stress magnitude | Pa |
| γ̇ | Positive shear-rate magnitude | s⁻¹ |
| K | Consistency coefficient, with units dependent on n | Pa·sⁿ |
| n | Power-law flow exponent | 1 |
| η | Shear viscosity at that rate | Pa·s |

Reading the relationshipn controls how rapidly stress rises with rate. Dividing stress by rate reduces the exponent by one, giving viscosity. For n below one, viscosity decreases with rate.

A worked exampleFor K = 1000 Pa·s⁰·⁵ and n = 0.5, γ̇ = 1 s⁻¹ gives τ = 1000 Pa and η = 1000 Pa·s. At 100 s⁻¹, τ = 10000 Pa and η = 100 Pa·s. Viscosity falls while stress rises.

ConditionsSteady isothermal flow within a suitable finite range. It does not by itself describe the low-rate plateau, startup memory, slip or instability.

A power law describes a region, not an entire flow curve. Extending a shear-thinning power law toward zero rate gives indefinitely increasing viscosity and misses the low-rate plateau. Extending it indefinitely toward high rates neglects finite molecular extension, heating and instabilities. Some models include a second high-rate plateau, but many melts encounter slip or surface and bulk instabilities first. A plateau is not universal evidence that all entanglements have disappeared. A changing dynamical constraint also does not by itself mean a molecular chain has broken.

Shear thinning describes the steady response to changing rate. Thixotropy describes structural changes with time at a given rate and subsequent rebuilding after disturbance. Both can occur together. Dense particle suspensions may instead shear thicken: increasing stress can promote frictional contacts between particles previously separated by lubrication layers. Near crowding limits, resistance rises sharply. Wyart and Cates connected this contact transition to discontinuous thickening in a 2014 model. Particle shape, surface interactions and concentration matter; one explanation based solely on liquid failing to fill gaps cannot cover every thickening system.

Non-Newtonian behavior includes more than rate-dependent viscosity. A fluid can have nearly constant steady shear viscosity over a selected range while retaining stress relaxation, extensional elasticity and normal stress differences. Nearly constant-viscosity elastic liquids are useful experimentally because they help separate viscosity variation from elastic effects. Conversely, fitting thinning with a viscosity that depends only on current rate does not automatically create memory. Such a model can reproduce steady measurements while missing recoil after flow stops. Model selection therefore asks whether loading history is represented, as well as whether the curve passes through steady data.

Molecular structure changes the whole curve. For chemically similar, narrowly distributed linear chains, zero-shear viscosity becomes particularly sensitive to molecular weight in the entangled regime. Empirical exponents around 3 to 3.4 are common over suitable ranges, while distributions and measurement windows change the result. Entanglement molecular weight characterizes a chain-constraint scale and need not equal the molecular weight at the viscosity crossover. A small population of very long chains can extend slow relaxation strongly. A broad distribution therefore cannot simply be labeled easier to process.

Long-chain branches alter relaxation routes and extensional strain hardening. Short-branch effects must be compared at matched backbone length, chemistry and temperature. Fillers can raise resistance and form shear-sensitive networks, strengthening thinning; at high concentration they may also thicken. Fillers do not universally make a material more Newtonian. Plasticizers and oils change segmental friction, interactions and effective concentration, while introducing partitioning and migration. Structural interpretation begins by stating which comparison variables are held constant.

## Fixed deformation and sustained force are different time experiments

Rapidly deforming a specimen, holding its shape and recording the decreasing force measures stress relaxation. Shape remains fixed while chains adjust internally, reducing the force needed to maintain it. Holding force or stress and observing continuing deformation measures creep. These experiments resemble clip-force retention and sustained loading, respectively. Their curves are related mathematically in linear viscoelasticity, but time-dependent modulus and compliance are generally not point-by-point reciprocals.

In 1867, Maxwell introduced stress relaxation in his work on the dynamical theory of gases, connecting short-time elasticity with long-time flow. A modern representation of a single Maxwell mode joins a spring and a viscous dashpot in series. They carry the same stress and their deformations add. After total deformation is suddenly fixed, continued dashpot motion allows the spring to retract, progressively reducing its force. The mechanical diagram represents this temporal logic; it is not a literal map of polymer molecules.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pm12/en/#en-s4)

Figure 2 · Maxwell’s relaxation idea represented by modern series elements. At fixed total deformation, dashpot motion unloads the spring. The lower curve is a normalized exponential decay, with time measured in relaxation-time units.

Stress relaxation of a single Maxwell modeEq. 4

![Stress relaxation of a single Maxwell mode](https://ml-biomat.com/static/agent-math/c6937d81d22d7f265c1d6ff7.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| τᴹ | Maxwell relaxation time | s |
| η | Dashpot viscosity parameter | Pa·s |
| G₀ | Spring shear modulus | Pa |
| G(t) | Shear relaxation modulus at time t | Pa |
| t | Time after a fixed step strain | s |
| γ₀ | Small fixed step shear strain | 1 |
| σₛ(t) | Relaxing shear stress | Pa |
| exp | Natural exponential function | 1 |
| M、0、s | Labels for Maxwell, initial parameter and shear stress | 1 |

Reading the relationshipSeries elements share stress. At fixed total strain, dashpot motion unloads the spring, giving decay proportional to the remaining stress. Viscosity divided by modulus has units of time.

A worked exampleG₀ = 100000 Pa and η = 1000000 Pa·s give τᴹ = 10 s. At γ₀ = 0.01, initial stress is 1000 Pa, falling to about 367.88 Pa after 10 s and 135.34 Pa after 20 s.

ConditionsSmall-strain isothermal single-mode linear response, with a step faster than the relaxation being studied. Distributed times or equilibrium networks require additional modes or an equilibrium spring.

Exponential decay means that equal time intervals remove equal fractions of the remaining stress. The relaxation time is the time for stress to fall to approximately 36.8% of its initial value, not an abrupt deadline at which elasticity vanishes. A mode with a 10 s relaxation time retains approximately 36.8% after 10 s and 13.5% after 20 s. Real polymers usually contain many modes arising from local motion, chain-scale movement, entanglement release and phase organization. Their measured relaxation therefore commonly spans a broader range than a single exponential.

Under constant shear stress, the spring in this series model deforms immediately while the dashpot continues moving at a constant rate. Creep has an immediate contribution and a contribution increasing with time. Unloading recovers the spring deformation, while accumulated dashpot flow remains. This result captures an uncrosslinked fluid’s long-time tendency. A solid with a stable equilibrium shape requires an additional path capable of supporting stress indefinitely, rather than placing a freely flowing dashpot in every load path.

Creep of the same Maxwell modeEq. 5

![Creep of the same Maxwell mode](https://ml-biomat.com/static/agent-math/aadbc51853abd0e0bf0dd1e6.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| J(t) | Shear creep compliance | Pa⁻¹ |
| G₀ | Spring shear modulus | Pa |
| η | Dashpot viscosity | Pa·s |
| t | Time after constant stress begins | s |
| τ₀ | Maintained shear stress | Pa |
| γ(t) | Shear strain at time t | 1 |
| 0 | Label for an initial or fixed parameter | 1 |

Reading the relationshipThe series strains add: the spring immediately contributes stress divided by modulus, while the dashpot flows at stress divided by viscosity.

A worked exampleWith G₀ = 100000 Pa, η = 1000000 Pa·s and τ₀ = 1000 Pa, initial strain is 0.010. At 20 s, J = 0.000030 Pa⁻¹ and strain is 0.030. Unloading ideally recovers 0.010 and leaves flow strain 0.020.

ConditionsLinear isothermal single-mode Maxwell fluid. J(t) is generally not the reciprocal of G(t) at the same time. Bounded long-time solid creep needs a different network arrangement.

A spring and dashpot in parallel represent delayed approach to a finite deformation. Combining modes can represent instantaneous elasticity, delayed recovery and irreversible flow separately. Such models organize experimentally testable time processes. Fitting several elements does not prove that each corresponds to a distinct molecular structure. At large strains, yielding or structural damage, parameters measured in the linear regime may change with loading history and require a corresponding nonlinear description.

The imposed input must also remain well defined. A specimen that stretches and narrows under constant force does not necessarily experience constant true stress. Grip slip can masquerade as creep, and temperature drift moves the time response. Waiting time after unloading determines how much slow recovery is captured. Specifying amplitude, temperature, hold time and recovery time separates molecular behavior from equipment, geometry and operational changes.

## Small oscillations reveal storage and loss

Instead of suddenly loading a material, a rheometer can shear it gently back and forth. A sine wave repeats smoothly; amplitude gives the maximum deformation and frequency gives cycles per second. Stress generally does not remain exactly in phase with strain. The phase difference separates recoverable storage from dissipation. Storage modulus G′ describes the component in phase with strain. Loss modulus G″ describes the component in phase with strain rate. Both have units of pascals and specify the strengths of those responses at the chosen frequency.

Storage and loss components during oscillationEq. 6

![Storage and loss components during oscillation](https://ml-biomat.com/static/agent-math/00ae61a11ac5f53251d68fb7.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| γ(t)、γ₀ | Shear strain and its amplitude | 1 |
| τ(t) | Oscillatory shear stress | Pa |
| G′ | Storage modulus at the chosen frequency | Pa |
| G″ | Loss modulus at the chosen frequency | Pa |
| ω | Angular frequency | rad/s |
| f | Cycles per second | Hz |
| t | Time | s |
| δ | Phase angle by which stress leads strain | rad, or converted to ° |
| sin、cos、tan | Sine, cosine and tangent functions describing periodicity and phase ratios | 1 |
| π | Circle constant; one cycle is 2π radians | 1 |
| ′、″ | Labels for storage and loss, not derivatives here | 1 |

Reading the relationshipStress is separated into a sine component in phase with strain and a cosine component a quarter-cycle ahead, in phase with strain rate. Their relative sizes determine the phase angle.

A worked exampleFor γ₀ = 0.01, G′ = 200000 Pa and G″ = 100000 Pa, component amplitudes are 2000 and 1000 Pa, giving total amplitude about 2236.07 Pa. tan δ = 0.5 and δ ≈ 26.565°. f = 1 Hz corresponds to ω ≈ 6.283 rad/s.

ConditionsSmall-amplitude linear steady oscillation after startup, with significant instrument inertia excluded. Moduli are reported with frequency and temperature.

Zero phase difference resembles an ideal spring. A quarter-cycle difference resembles an ideal viscous dashpot. The loss tangent is loss modulus divided by storage modulus, comparing their relative contributions at the same frequency. G′ exceeding G″ means storage dominates under those conditions; it does not classify the material as a solid at every timescale. A melt can appear elastic at high frequency and still flow over long times. Scanning frequency probes that change.

For a single Maxwell mode, angular frequency multiplied by relaxation time controls the curves. Low frequency gives the mode time to relax and leaves a small storage response. High frequency prevents substantial relaxation, so storage approaches the spring modulus. Loss reaches a maximum in the intermediate region where the two tendencies compete. The two moduli cross exactly when angular frequency times relaxation time equals one. This provides a checkable example, while crossings in a real multimode material do not automatically identify one unique molecular relaxation time.

Frequency curves for one relaxation timeEq. 7

![Frequency curves for one relaxation time](https://ml-biomat.com/static/agent-math/eea4a8af932b3c3c1f0853d2.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| x | Angular frequency times relaxation time | 1 |
| ω | Angular frequency | rad/s |
| τᴹ | Maxwell relaxation time | s |
| G₀ | Spring modulus | Pa |
| G′、G″ | Storage and loss moduli | Pa |

Reading the relationshipDimensionless x compares the driving timescale with relaxation. Low x permits relaxation; high x retains storage. At x = 1 the components are equal and this mode’s loss is maximal.

A worked exampleFor G₀ = 100000 Pa, τᴹ = 10 s and ω = 0.1 rad/s, x = 1 and both moduli are 50000 Pa. The corresponding frequency is about 0.015915 Hz. At ω = 1 rad/s, x = 10, G′ ≈ 99009.90 Pa and G″ ≈ 9900.99 Pa.

ConditionsIsothermal single Maxwell mode. Its high-frequency plateau is the spring response, not a description of the entire glassy high-frequency regime. Multimode crossings require a relaxation-spectrum interpretation.

[Figure: Storage and loss frequency curves for one Maxwell mode](https://ml-biomat.com/tutorials/biomaterials-courses/pm12/en/#en-s5)

Change relaxation time and observation frequency for the same 100 kPa Maxwell mode. Sliders span decades; outputs show actual seconds and hertz.

An amplitude sweep at fixed frequency identifies a range in which the moduli remain essentially unchanged with amplitude. Frequency scans within that range can then be interpreted primarily as changes in observation timescale. Excessive amplitude may alter filler networks, hard domains or chain orientation. The measurement then includes structural rearrangement. Low-torque sensitivity, edge integrity and high-frequency inertia also limit reliable portions of a curve. A usable window is determined jointly by specimen behavior and instrument capability.

Oscillatory complex viscosity sometimes resembles steady shear viscosity, an empirical correspondence commonly called the Cox–Merz rule. Complex viscosity includes storage and loss measured in a small periodic test. Steady shear can continually modify orientation, so the experiments are not identical by definition. Many homogeneous melts exhibit correspondence over suitable ranges. Filled networks, gels and pronounced multiphase structures may deviate. Measurements in an overlapping range establish whether the relation is useful for a particular formulation before it is extended.

Simultaneous structural measurements make rheology more specific. If a microdomain disappears on heating while low-frequency elasticity decreases, its possible role in a slow network can be investigated. If scattering shows crystals forming as modulus rises, the measurement connects crystallization to constrained chain motion. A modulus peak alone can have several origins. Evidence that structure and mechanics evolve together turns a general curve into a testable mechanism connecting molecules, phases and processing forces.

## Temperature shifts the material’s clock

Heating usually makes it easier for segments to overcome local motion barriers, accelerating many relaxation processes. If different modes accelerate by approximately the same factor, curves at different temperatures can be shifted along a logarithmic time axis to build a wider response at a reference temperature. This is time–temperature superposition. A process completed quickly at higher temperature can correspond to a longer wait at a lower reference temperature. Heating shortens the material’s relaxation times; it does not lengthen them.

In 1955, Williams, Landel and Ferry studied amorphous polymers and other glass-forming liquids and related shift factors to the difference from a reference temperature. The WLF expression remains a common description of this behavior. Here the shift factor is the relaxation time at the test temperature divided by that at the reference temperature. When heating accelerates relaxation, the ratio is smaller than one. This explicit definition determines the direction of the time shift without relying on an easily reversed verbal rule.

WLF shift and equivalent reference-temperature timeEq. 8

![WLF shift and equivalent reference-temperature time](https://ml-biomat.com/static/agent-math/7b47617b2b5a7e7abbf0d042.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| aᴛ | Temperature shift factor for relaxation time | 1 |
| τ(T)、τ(Tᵣ) | Corresponding relaxation times at test and reference temperatures | s |
| T、Tᵣ | Test and reference absolute temperatures | K |
| C₁ | Fitted coefficient for the selected reference | 1 |
| C₂ | Fitted coefficient with temperature-difference units | K |
| t、tᵣ | Time at test temperature and equivalent reference time | s |
| log₁₀ | Base-10 logarithm | 1 |
| r、T | Reference and temperature labels | 1 |

Reading the relationshipIf modes speed up by a common ratio, dividing observation time by that relaxation-time ratio gives equal progress at the reference temperature. WLF describes the temperature dependence of the ratio.

A worked exampleFor illustrative fitted C₁ = 8, C₂ = 100 K, Tᵣ = 350 K and T = 370 K, log₁₀aᴛ = −160/120 = −1.3333 and aᴛ ≈ 0.046416. Ten seconds at the test temperature corresponds to about 215.44 s at the reference.

ConditionsThermorheologically simple behavior without structural change over a verified temperature interval. Coefficients depend on reference temperature; vertical corrections may also be needed. Values illustrate the calculation rather than a commercial grade.

WLF coefficients depend on the reference temperature. Familiar classical values are not constants imposed on every material and every temperature interval. Segmental motion near glass transition, higher-temperature terminal flow and regions with changing crystals or phases may not follow the same shift. Density and thermal-energy changes can also require a vertical correction. If different frequency regions need different shifts, or the curve shape changes, that observation should be retained and its structural cause examined.

Over some temperature intervals, viscosity or relaxation time follows an Arrhenius form: overcoming effective motion barriers produces an exponential dependence on inverse absolute temperature. The effective activation energy describes sensitivity across the measured interval. It need not equal a chemical-bond dissociation energy, nor imply that an entire chain jumps into one empty hole. A ratio expression directly compares two temperatures without requiring a separately estimated prefactor.

Arrhenius temperature ratioEq. 9

![Arrhenius temperature ratio](https://ml-biomat.com/static/agent-math/25a01a08f54cd82ee84fab3d.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| η(T)、η(Tᵣ) | Viscosities at two temperatures using the same flow definition | Pa·s |
| T、Tᵣ | Test and reference absolute temperatures | K |
| Eₐ | Effective flow activation energy over the selected range | J/mol |
| R | Gas constant, here 8.314 | J/(mol·K) |
| exp | Natural exponential function | 1 |
| a、r | Activation and reference labels | 1 |

Reading the relationshipHeating reduces inverse temperature. A positive activation energy times the negative inverse-temperature difference gives a viscosity ratio below one. Taking a ratio removes the common prefactor.

A worked exampleFor Eₐ = 50000 J/mol, Tᵣ = 450 K and T = 470 K, the exponent is about −0.56870 and the viscosity ratio about 0.56626. A reference viscosity of 1000 Pa·s becomes about 566.26 Pa·s.

ConditionsApplies over a range with approximately constant effective activation energy, consistent state and flow definition. It need not describe glass-transition-region data, and Eₐ is not automatically a bond-breaking energy.

No universal boundary requires every polymer to change formulas exactly 100 degrees above glass transition. Data establish which representation remains consistent over the selected range, while checking for chemical or morphological changes during heating. Pressure can reduce available space and alter motion. Humidity and solvent uptake can plasticize a material and shift its timescales. If heating also removes water, melts crystals or degrades chains, the change is more than acceleration of an otherwise unchanged material clock.

Superposition extends accessible measurement windows when the relevant mechanisms remain consistent. Using a short high-temperature test to estimate sustained performance requires checking whether heating introduces another relaxation, reaction or interfacial damage process. A smooth assembled master curve does not by itself establish service life. A useful sequence first checks overlapping shapes, then tests the extended prediction against independent conditions. The shifted curve thereby continues to represent the same physical process.

## Rod climbing, die swell and rough surfaces reveal stored stresses in flow

A rotating rod in an ordinary liquid often produces an inertially depressed surface near the axis. Some polymer solutions instead climb up the rod. Weissenberg’s 1947 continuum discussion connected such phenomena to stresses developed during flow. Tension around circular streamlines acts somewhat like a tightening band, producing inward forces. Gravity, surface tension, viscosity and inertia together determine the surface. Climbing cannot be explained simply by a large viscosity; unequal directional stresses are central.

Normal stress differences in simple shearEq. 10

![Normal stress differences in simple shear](https://ml-biomat.com/static/agent-math/b23e5a4650fd85a77278cf9c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| N₁、N₂ | First and second normal stress differences | Pa |
| σxx、σyy、σzz | Normal stresses along x, y and z, using tensile-positive signs | Pa |
| x、y、z | Flow, velocity-gradient and third orthogonal directions | 1 |

Reading the relationshipSubtraction removes common isotropic pressure and retains directional differences generated by flow. The coordinate convention must remain fixed.

A worked exampleFor σxx = 20000 Pa, σyy = 5000 Pa and σzz = 7000 Pa, N₁ = 15000 Pa and N₂ = −2000 Pa. Subtracting 100000 Pa from every component leaves both differences unchanged.

ConditionsUses the standard simple-shear directions. Other flows require the corresponding coordinates and constitutive relation; a normal stress alone does not establish elasticity.

In defined simple-shear coordinates, differences among flow-direction, gradient-direction and third-direction normal stresses give the first and second normal stress differences. Their common isotropic pressure contribution cancels on subtraction. An ideal Newtonian fluid has no normal stress differences in simple shear, but it can have viscous normal stresses in other deformation modes. The presence of a normal stress alone therefore does not establish elasticity. Interpretation requires the flow geometry and coordinate convention.

Die swell is another expression of flow history. Contraction at an entrance and shear inside a die orient chains and store recoverable deformation. After wall constraints are removed, rearrangement can enlarge the extrudate cross-section. Velocity-profile adjustment, surface tension, drawing and cooling also affect the final size; modest swelling is not exclusive to polymers. Processing comparisons specify die geometry, temperature, flow rate, distance from the exit and any applied draw. The often stronger recoverable response of polymers makes these conditions especially influential.

Extensional stresses can maintain a liquid filament and allow a lifted stream to pull material behind it, producing phenomena such as tubeless or open-side siphoning. These effects illustrate why shear measurements cannot describe every process. Spinning needs a thread that can be drawn thin without breaking prematurely. Film blowing also needs resistance to a local thinning disturbance that would otherwise grow. Branching, molecular-weight distribution and temperature can influence extensional strain hardening differently from steady shear viscosity.

Increasing flow can produce sharkskin surface roughness, stick–slip oscillations or gross distortion, with the sequence depending on material and equipment. Contraction entrances, walls and exits provide distinct disturbance locations. Entrances impose extension, walls can undergo changes in adsorption and slip, and the surface layer must accelerate after leaving wall restraint. High-speed observations have revealed cohesive failure near the exit under some polyethylene conditions. Melt fracture therefore cannot universally be described as involving no actual material failure. Nor should every extrusion distortion be grouped under elastic turbulence.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pm12/en/#en-s7)

Figure 3 · Separate potential instability locations in extrusion. Dominant processes vary with material; surface roughness, periodic stick–slip and gross distortion require corresponding pressure, velocity and structural evidence.

Improvement begins by locating the mechanism. Exit-surface stretching suggests examining exit geometry, surface conditions and temperature distribution. Entrance concentration of stress suggests examining the contraction and its flow field. Periodic pressure changes call for simultaneous checks of slip, feeding and control behavior. Processing additives can alter wall interactions, with effects dependent on material, history and coverage. Heating may reduce some stresses but also reduce melt strength or accelerate degradation. Temperature changes are assessed together with throughput, appearance and material condition.

## How instruments turn pressure and torque into rheological curves

A capillary rheometer pushes melt through a narrow tube and measures pressure and volumetric flow. Balancing pressure force against wall shear gives wall shear stress without first assuming Newtonian behavior. Converting flow rate to wall shear rate requires the velocity profile. A Newtonian parabolic profile gives an apparent rate. For a power-law fluid, a Rabinowitsch–Mooney correction supplies the corresponding wall rate, after which wall viscosity can be calculated.

Capillary wall stress, rate and viscosityEq. 11

![Capillary wall stress, rate and viscosity](https://ml-biomat.com/static/agent-math/829cc73a0aec8bfccb3d6953.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ΔP𝑐 | Pressure drop over the fully developed capillary section | Pa |
| ΔPtot | Measured total pressure drop | Pa |
| ΔPₑ | Estimated entrance and exit contribution | Pa |
| R𝑐、L𝑐 | Capillary radius and length | m |
| Q | Volumetric flow rate | m³/s |
| τw | Wall shear-stress magnitude | Pa |
| γ̇ₐ | Apparent wall rate from the Newtonian profile | s⁻¹ |
| γ̇w | Power-law-corrected wall shear rate | s⁻¹ |
| n | Power-law exponent over the selected range | 1 |
| ηw | Shear viscosity at the wall conditions | Pa·s |
| π | Circle constant | 1 |
| c、tot、e、w、a | Labels for capillary, total, ends, wall and apparent quantity | 1 |

Reading the relationshipPressure force on the section balances wall shear force. Flow first gives a Newtonian apparent rate, then a power-law profile correction gives wall rate. Stress divided by that rate gives viscosity.

A worked exampleFor ΔPtot = 1000000 Pa, ΔPₑ = 200000 Pa, R𝑐 = 0.0005 m, L𝑐 = 0.020 m, Q = 10⁻⁸ m³/s and n = 0.5, ΔP𝑐 = 800000 Pa, τw = 10000 Pa, γ̇ₐ ≈ 101.86 s⁻¹, γ̇w ≈ 127.32 s⁻¹ and ηw ≈ 78.54 Pa·s.

ConditionsCircular steady fully developed approximately isothermal no-slip flow with negligible inertia. The rate correction applies within a suitable power-law range. End effects, slip and heating require separate treatment.

Measured pressure also includes additional losses as material enters and leaves the capillary. In 1957, Bagley examined end corrections for polyethylene flow using tubes of the same diameter but different lengths at the same flow rate. If fully developed pressure loss is proportional to length, extrapolating total pressure drop to zero length estimates the end contribution. That intercept contains entrance and any relevant exit effects in the experimental arrangement. Subtracting it before calculating wall stress avoids treating entrance extension as if it were all shear resistance inside the tube.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pm12/en/#en-s8)

Figure 4 · Illustrative data use an end contribution of 0.2 MPa and 0.04 MPa per millimeter inside the tube. The zero-length intercept estimates end effects. Matched diameter and flow and approximate linearity are central to the comparison.

This procedure has conditions. If changing length changes heating, degradation or wall slip, pressure versus length may curve. Forcing a straight fit would hide that behavior. Slip means that velocity at the wall is nonzero, so correcting a non-Newtonian no-slip profile is insufficient. Changes in diameter or surface and independent velocity measurements can help identify it. Pressure-dependent viscosity, inertia and viscous heating also matter in relevant regimes. Capillary tests approach processing rates while still requiring separation of equipment flow fields from material response.

A rotational rheometer places material between a moving tool and a stationary surface, recording speed, angular displacement, torque and normal force. With a small-angle cone and plate, both gap and local speed increase with radius, making the ideal shear rate approximately uniform. Parallel plates permit flexible gap adjustment but have a radially varying rate that requires appropriate interpretation. Cone–plate measurements are not universally correction-free: truncation gap, temperature, loading volume, edge fracture, evaporation, slip and inertia can all influence results.

Torque measures the turning action of force about an axis. The same tangential force contributes more torque when applied farther from that axis. A rotational instrument records contributions added over the entire contact surface, so conversion to local stress requires known dimensions and an appropriate stress distribution. A gap-setting error changes the inferred rate, while a difference between sample temperature and displayed temperature changes the material’s actual viscosity. Suitable reference fluids help check instrument performance. Establishing thermal stability at the target condition then makes changes in the measured curve more clearly attributable to the specimen.

Instrument choice follows the question. Rotation and oscillation address low-rate viscosity and small-amplitude relaxation. Capillaries approach extrusion shear rates. Spinning or film-stability questions call for extensional rheology as well. Overlapping regions from different instruments should be compared for the same material, with actual temperature, moisture and thermal history recorded. Samples can crosslink, crystallize or degrade while waiting inside a rheometer. Checking time stability before a scan helps determine what the later curve represents.

Three questions clarify a rheological plot: was force, deformation or rate imposed; what time or frequency was observed; and did the material retain the same structural state during measurement? With those conditions defined, the curve connects to chain motion and processing. Viscoelasticity provides measurable temporal relationships, showing when a material stores energy, when it flows and how those capabilities can be placed where an application needs them.
