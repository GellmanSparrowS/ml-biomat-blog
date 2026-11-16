# Why Processes Have a Direction: Irreversibility and Dissipation

Source: https://ml-biomat.com/tutorials/biomaterials-courses/cp11/en/
Language: en

Tea cools, dye spreads, and a flowing polymer converts mechanical work into heat. Energy conservation alone does not prohibit the reverse processes, so where does their direction come from? Connect particle counting and random motion to entropy, diffusion, heat flow and viscous dissipation, distinguishing equilibrium from continuously driven materials.

## What energy conservation leaves to explain

A cup of hot tea cools on a table while its surroundings receive heat. The same energy could, in an accounting sense, move from cooler air into the tea and make it hotter without violating conservation. Yet this is not a routinely observed spontaneous process. Similarly, a drop of ink spreads through still water and almost never gathers back into the original drop. Conservation says that energy cannot appear or disappear, but does not by itself determine how energy and matter are distributed or which processes are likely.

An irreversible process cannot be undone for both system and environment merely by reversing the external operation. Stirring a viscous liquid converts organized mechanical motion into molecular motion and heat. Turning the paddle in the opposite direction generally supplies more work instead of recovering all the previously generated heat. A reversible process is an ideal limit in which every step departs infinitesimally from equilibrium and an infinitesimal change can retrace the path for system and surroundings together. Slowness alone does not establish reversibility: friction or a finite chemical-potential difference can still generate dissipation.

Thermodynamics describes this direction using entropy, a state quantity measured in joules per kelvin. Entropy concerns the microscopic states compatible with macroscopic constraints, rather than visual tidiness or disorder. For a large reservoir held at constant temperature, receiving a small quantity of heat increases its entropy by that heat divided by absolute temperature. Absolute temperature is measured in kelvin; Celsius values cannot be inserted into the denominator. The same joule of heat produces a larger entropy change in a colder reservoir than in a hotter one.

Entropy change for hot-to-cold heat transferEq. 1

![Entropy change for hot-to-cold heat transfer](https://ml-biomat.com/static/agent-math/51c09c055cbe934e395ff866.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ΔStot | Total entropy change of the two reservoirs | J K⁻¹ |
| Q | Positive heat transferred from the hot reservoir | J |
| Tc | Absolute temperature of the cold reservoir | K |
| Th | Absolute temperature of the hot reservoir, Th>Tc | K |
| Δ | Final minus initial change | 1 |

Reading the relationshipThe hot reservoir loses Q/Th and the cold one gains Q/Tc. Their sum is positive because reciprocal cold temperature is greater.

A worked exampleFor Q=100 J, Th=310 K and Tc=300 K, ΔStot=100×(1/300−1/310)≈0.01075 J K⁻¹.

ConditionsDirect heat exchange between large nearly constant-temperature reservoirs without work conversion. Appreciable temperature changes require incremental or integral evaluation using instantaneous temperature.

A quantity of heat moving from a hot reservoir to a cold one therefore increases their combined entropy. A refrigerator can move heat in the opposite direction by consuming work and rejecting additional heat to its environment. Including the power supply and surroundings preserves the total entropy condition. The entropy of one subsystem can decrease when compensated by sufficient environmental increase. Cooling and crystallization, construction of cellular structures and separation of mixtures must all be evaluated with their actual exchanges rather than by examining the subsystem alone.

For a system exchanging no matter, entropy rate can be divided into entropy carried across the boundary by heat and entropy generated internally by irreversible processes. A rate is a change divided by a short time interval, taken in the limit of sufficiently small intervals. It measures how much changes per second, rather than how much entropy currently exists. When matter also crosses the boundary, it carries entropy and additional inflow and outflow terms are required. This distinction makes the balance usable for both laboratory samples and operating material devices.

Entropy exchange and internal productionEq. 2

![Entropy exchange and internal production](https://ml-biomat.com/static/agent-math/f6865789cb05052a642e40fb.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| S | System entropy | J K⁻¹ |
| t | Time | s |
| dS/dt | Instantaneous rate of system entropy change | W K⁻¹ |
| α | Index of heat-exchange boundary channels | 1 |
| Σα | Sum over heat-exchange channels | 1 |
| Q̇α | Heat rate through channel α, positive into the system | W |
| Tα | Absolute temperature at that exchange boundary | K |
| Ṡi | Internal entropy-production rate | W K⁻¹ |

Reading the relationshipEntropy crosses boundaries with heat and is produced by internal irreversible processes. A dot and d/dt denote rates; internal production is nonnegative in macroscopic thermodynamics.

A worked exampleIf internal production is 0.02 W K⁻¹ and 6 W of heat leaves through a 300 K boundary, entropy flow is −6/300=−0.02 W K⁻¹, giving zero system entropy rate.

ConditionsNo matter exchange and a consistent assignment of boundary temperatures and internal dissipation. Matter exchange adds entropy carried by material flows.

A steadily operating device can maintain nearly constant internal temperature and composition while producing entropy and exporting it continuously. A state that no longer changes with time need not be equilibrium. A film held between hot and cold ends can maintain a stationary temperature profile with ongoing heat flow and entropy production. The statistical question developed next is how this macroscopic direction remains compatible with microscopic particles that continue moving and can move in either direction. Equilibrium, steady operation and a single momentarily unchanging measurement must be distinguished throughout that discussion.

## How many microscopic arrangements lie behind a macrostate

Imagine equal left and right chambers containing ten particles given distinguishable labels for counting. Each particle may be on either side, so a description recording only side membership has 2 to the tenth power, or 1,024, microscopic arrangements. A macroscopic measurement that records only the number on the left combines many arrangements into one class. All ten on the left corresponds to one arrangement, whereas five on each side corresponds to 252 choices. Labels aid counting without implying different chemical properties.

Why are there 252 balanced arrangements? Selecting the first left-hand particle offers ten choices, the next nine, and so on until five are chosen. Permutations within the selected group and the remaining group do not change membership and must be divided out. Factorial notation abbreviates multiplication of an integer by all positive integers below it. The resulting combination count grows rapidly with particle number. Near-even populations correspond to vastly more arrangements than extreme separation, providing a concrete starting point for a statistical explanation of equilibrium.

Counting entropy of left-right populationsEq. 3

![Counting entropy of left-right populations](https://ml-biomat.com/static/agent-math/29f615a35d7ea4eb2277ea24.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Ω(n) | Number of assignments with exactly n particles on the left | 1 |
| N | Total particle count | 1 |
| n | Left-side particle count | 1 |
| ! | Factorial, multiplying positive integers down to one, with 0!=1 | 1 |
| SB | Boltzmann entropy for the selected population macrovariable | J K⁻¹ |
| kB | Boltzmann constant, 1.380649×10⁻²³ | J K⁻¹ |
| ln | Natural logarithm, converting multiplication of independent counts to entropy addition | 1 |

Reading the relationshipChoose n particles for the left, dividing out permutations within each side that leave membership unchanged. Only side-occupation entropy is counted; unchanged contributions add a constant.

A worked exampleFor N=10 and n=5, Ω=10!/(5!5!)=252 and SB/kB=ln252≈5.529. For n=10, Ω=1 and this occupation entropy is zero.

ConditionsEqual-volume symmetric noninteracting chambers with labels used for configuration counting. This is the entropy of the chosen coarse variable, not arbitrary single-trajectory total entropy production.

Boltzmann's 1877 work connected thermal equilibrium, probability and the number of microscopic arrangements. Taking a logarithm has a physical advantage: independent systems have multiplying arrangement counts, while their entropies add because the logarithm of a product is a sum. The displayed formula uses modern conventional notation for this idea. Large entropy does not mean individual particles try to create disorder. It means that more microscopic configurations realize the corresponding macroscopic conditions, given the specified constraints and state-counting convention.

[Figure: Macroscopic populations and arrangement counts for ten particles](https://ml-biomat.com/tutorials/biomaterials-courses/cp11/en/#en-s2)

Figure 1 · Ten labelled particles have 1,024 side assignments. Five on each side has 252 assignments, while all on one specified side has one. The diagram makes Boltzmann counting directly checkable without treating macrostates as equally probable.

Counting alone does not determine dynamics. If the partition is impermeable, the many balanced arrangements cannot be reached from an initial state with every particle on the left. Motion rules must permit exchange, while barriers, freezing or additional conserved quantities can restrict accessible configurations. Macroscopic direction emerges from accessible-state weights, actual dynamics and preparation together. Knowing which count is largest does not by itself determine how quickly a system approaches it. That requires kinetic information about how states connect and how often transitions occur.

Observation scale also matters. For a complete isolated classical system following appropriate Hamiltonian dynamics, a sufficiently detailed position-and-momentum distribution has a conserved fine-grained Gibbs entropy. A macroscopic description retains only a few variables, such as density and temperature, and groups many microscopic details together. This is coarse graining. Correlations can develop at increasingly fine scales that the macroscopic measurements cannot reconstruct. Reversibility at the detailed level and growing coarse-grained entropy can therefore coexist without assigning contradictory motion rules to the same particles.

The explanation does not say that ignorance itself makes matter change. Initially confining gas to one chamber is a real low-entropy preparation. After the partition is opened, the overwhelming majority of microscopic states compatible with that preparation evolve toward nearly uniform macroscopic populations. Reversing the full motion would require much more than turning the vessel around: all relevant correlated degrees of freedom would need a highly special arrangement. Initial preparation and typicality give the statistical direction its reproducible experimental meaning. They also explain why the existence of mathematically possible reverse trajectories does not make ordinary mixing equally likely to undo itself.

## Two chambers: mean relaxation and individual fluctuations

Paul and Tatiana Ehrenfest used a simple two-container random model in 1907 to discuss irreversibility and recurrence. Randomly moving a particle from one container to the other can make the populations more balanced or less balanced in an individual step. When the left side contains many particles, however, more particles are available to leave it. Excess occupation consequently tends to decrease. Bidirectional microscopic moves are fully compatible with a definite direction for the average behaviour of many particles.

Here the model uses a continuous-time symmetric version. Each particle switches to the other chamber at the same rate k, independently of the others. The unit of k is inverse seconds, expressing the switching tendency per particle per unit time. With n particles on the left, the total rightward rate is proportional to n, while the leftward rate is proportional to N minus n. Their difference determines decay of the mean population imbalance. Equilibrium has a mean left fraction of one half, not an absence of continuing jumps.

Mean relaxation between symmetric chambersEq. 4

![Mean relaxation between symmetric chambers](https://ml-biomat.com/static/agent-math/118ff6555acdde962b4d4427.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| 〈f(t)〉 | Mean left fraction over repeated realizations | 1 |
| f | Fraction of particles on the left | 1 |
| f₀ | Initial left fraction | 1 |
| A | Initial fraction deviation from one half | 1 |
| n | Left particle count | 1 |
| N | Total particle count | 1 |
| k | Switching rate to the opposite side per particle | s⁻¹ |
| t | Elapsed time | s |
| e | Base of the natural exponential, about 2.71828 | 1 |

Reading the relationshipSubtracting rightward rate kn from leftward rate k(N−n) makes the mean deviation from one half decay at rate 2k. The exponent 2kt is dimensionless.

A worked exampleFor f₀=0.9 and k=1 s⁻¹, at t=1 s the mean is 0.5+0.4e⁻²≈0.5541. It equals 0.9 at t=0 and approaches 0.5 at long times.

ConditionsIndependent particles undergoing symmetric equal-rate continuous-time two-state transitions without interactions. Individual trajectories differ from the mean curve.

Exponential relaxation follows because a larger imbalance produces a larger correcting net exchange. When the imbalance becomes small, its mean correction also becomes small. Equal time intervals remove the same fraction of the remaining imbalance, rather than the same fixed particle count. An exponential is the continuous form of repeated proportional reduction. The displayed mean describes averaging over many independent repetitions. A single trajectory fluctuates around it and is not required to decrease smoothly at every step, even when the initial imbalance is substantial.

[Figure: Random left-fraction trace and mean relaxation](https://ml-biomat.com/tutorials/biomaterials-courses/cp11/en/#en-s3)

Time is measured in units of 1/k. Each advance uses the exact endpoint transition probability for symmetric continuous-time switching; points record interval-end populations. Advance up to 50 time units, then reset or choose another trajectory.

Green is one random realization, orange the theoretical ensemble mean, and the dashed line the equilibrium fraction one half. Changing N or initial fraction prepares a new system; advance buttons continue its trace. Each observation is user-controlled, with no autoplay.

Begin with 90% of particles on the left and advance the process, comparing the realized trace with the mean curve. Then choose an initial fraction of 50%. The mean remains horizontal while the actual count still fluctuates. Finally compare small and larger particle populations. Absolute fluctuations in count increase with size, whereas relative fluctuations in fraction decrease. At equilibrium the left count is binomial, with standard deviation equal to square root N divided by two. The corresponding fraction has standard deviation one divided by twice square root N.

Population dependence of equilibrium fluctuationsEq. 5

![Population dependence of equilibrium fluctuations](https://ml-biomat.com/static/agent-math/49e56a09aec35bb65463c7b8.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| sd | Standard deviation, square root of mean squared deviation | 1 |
| n | Equilibrium left particle count | 1 |
| f | Equilibrium left fraction n/N | 1 |
| N | Total independent particle count | 1 |
| √ | Square-root operation | 1 |

Reading the relationshipEach independent particle has left probability one half and occupancy variance one quarter. Adding N variances gives N/4; taking a square root gives count standard deviation, then dividing by N gives fraction standard deviation.

A worked exampleFor N=100, count standard deviation is 5 and fraction standard deviation 0.05. For N=400 they are 10 and 0.025: absolute fluctuations grow while relative fluctuations shrink.

ConditionsEquilibrium distribution in equal-volume chambers with independent noninteracting particles. A finite trajectory gives a sample standard deviation with sampling variation.

The inverse-square-root decrease of relative fluctuations depends on approximate particle independence. Particles moving in groups, sharing slow environmental disturbances or approaching a critical state with long-range correlations no longer provide independent information. Adding particles may then average away fluctuations less effectively than in the ideal model. Spatial and temporal correlations must be measured to identify how many approximately independent contributions remain. Each visible particle cannot automatically be treated as an independent statistical sample, even when a microscope resolves its position clearly.

The display also evaluates a macroscopic counting entropy from the current left and right populations. This quantity can decrease temporarily along an individual trajectory, particularly in a small system. It is a Boltzmann entropy using chamber population as the coarse variable, distinct from total stochastic entropy production along a path including environmental exchange. Maintaining that distinction reconciles mean relaxation, reverse fluctuations in small systems and the macroscopic second law. A downward segment in this particular entropy trace is not by itself a measurement of total entropy production.

A finite model can eventually revisit a strongly imbalanced state. The equilibrium probability that all particles occupy one specified side is 2 to the power minus N, falling rapidly with population. For N=20 it is approximately one in a million; for N=100 it is about 7.9 times 10 to the minus 31. A probability is not itself a waiting time, which also depends on switching rates and correlations. Nevertheless, the comparison explains why visible fluctuations in small systems very rarely appear as spontaneous reconcentration of an entire macroscopic body. Recurrence and practical irreversibility concern different scales of probability and observation time.

## From random motion to the diffusion equation

The two-chamber model records only two populations. Dividing space into many neighbouring cells and allowing particles to move randomly between nearby locations leads to a concentration field describing mean local occupancy. Concentration can be expressed as particle count or amount of substance per volume. This section uses moles per cubic metre; one mole contains 6.02214076 times 10 to the 23 specified entities. The counting convention does not alter the diffusion picture, but fluxes and constants must use matching units throughout a calculation.

Particles cross an imaginary surface in both directions. The more concentrated side generally supplies more crossing particles, producing a net flux toward lower concentration. Flux means amount passing per area per time, not the velocity of one particle. In his 1855 work on liquid diffusion, Fick related flux to concentration gradient through an analogy with heat conduction. A gradient measures how rapidly concentration changes in space; in one dimension, concentration difference divided by distance approximates it. This converts the qualitative imbalance of crossings into a measurable transport relation.

One-dimensional Fick diffusion fluxEq. 6

![One-dimensional Fick diffusion flux](https://ml-biomat.com/static/agent-math/b2680b31137b012649701172.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| J | Amount flux, positive along increasing x | mol m⁻² s⁻¹ |
| D | Diffusion coefficient | m² s⁻¹ |
| c | Amount concentration | mol m⁻³ |
| x | Spatial coordinate | m |
| ∂c/∂x | Local spatial concentration rate at fixed time | mol m⁻⁴ |

Reading the relationshipBidirectional random exchange leaves a net imbalance when neighbouring concentrations differ. Flux is proportional to a local gradient; positive D and the minus sign direct net flow down it.

A worked exampleA decrease from 1 to 0 mol m⁻³ over 1 mm gives gradient about −1,000 mol m⁻⁴. With D=10⁻⁹ m² s⁻¹, J=10⁻⁶ mol m⁻² s⁻¹ toward increasing x.

ConditionsLocal linear concentration-driven diffusion in a homogeneous medium without advection or additional coupled driving. Nonideal or charged systems require appropriate chemical and electrical potentials.

The negative sign belongs to the homogeneous ideal-diffusion model being written, rather than asserting that all matter always moves down its concentration gradient. Charged species also respond to electrical fields. In nonideal mixtures the driving force involves chemical potential, and temperature gradients can couple to composition transport. During some phase-separation processes, material can move toward greater concentration while lowering the complete free energy. Before using the Fick form, ask whether concentration alone adequately represents the relevant thermodynamic driving force under the stated conditions.

A flux relation alone does not determine how concentration changes with time. Consider a thin volume element. More entering through its left face than leaving through its right produces accumulation; greater outflow produces depletion. This is conservation of matter, like balancing inflow and outflow from a tank. Shrinking the slice thickness gives the relation between concentration rate and the spatial rate of change of flux. Inserting Fick's law yields the diffusion equation. Its second spatial derivative describes concentration-curve curvature and determines whether a location receives net inflow or loses material.

Diffusion equation from material conservationEq. 7

![Diffusion equation from material conservation](https://ml-biomat.com/static/agent-math/0e4542caba3d68337c3422c7.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| c | Local amount concentration | mol m⁻³ |
| t | Time | s |
| J | Amount flux along x | mol m⁻² s⁻¹ |
| x | Spatial coordinate | m |
| D | Constant diffusion coefficient | m² s⁻¹ |
| ∂c/∂t | Concentration time rate at fixed position | mol m⁻³ s⁻¹ |
| ∂J/∂x | Spatial rate of change of flux | mol m⁻³ s⁻¹ |
| ∂²c/∂x² | Second spatial derivative or curvature of concentration | mol m⁻⁵ |

Reading the relationshipAccumulation in a small volume equals inflow minus outflow, so a flux increasing with x depletes concentration. Inserting constant-D Fick transport gives the second line.

A worked exampleAt curvature −10⁶ mol m⁻⁵ and D=10⁻⁹ m² s⁻¹, the local concentration rate is −10⁻³ mol m⁻³ s⁻¹, indicating a falling concentration peak.

ConditionsOne dimension with constant D and no reaction, advection or volume change; initial and boundary conditions are required. Spatially varying D requires retaining the flux-divergence form.

[Figure: Net flux from concentration imbalance and a spreading peak](https://ml-biomat.com/tutorials/biomaterials-courses/cp11/en/#en-s4)

Figure 2 · Particles cross in both directions, with concentration imbalance producing a net flux. Conserved-area Gaussian profiles below illustrate ordinary diffusive broadening: peak height falls as width grows. This is a mechanism schematic without material-specific axis values.

The top of a local concentration peak supplies both sides and falls, while neighbouring troughs fill. Fine spatial variations consequently disappear faster than broad ones. A characteristic diffusion time grows as the square of distance: at fixed diffusivity, increasing membrane thickness tenfold increases the corresponding time scale about one hundredfold. A thin hydrogel can therefore respond much faster than a thick piece of the same chemistry. Comparing release rates requires geometry as well as material identity, particularly when the diffusion path changes during swelling.

Boundary conditions determine the particular diffusion problem. A sealed boundary permits no net flux across it, allowing concentration to become uniform within the accessible space. Reservoirs maintaining different concentrations at opposite ends support a sustained flux. An absorbing boundary removes arriving particles. Initial concentration, specimen dimensions and boundary exchange jointly determine the process. Reactive or degrading materials additionally require generation and consumption terms in the conservation law. Keeping those contributions explicit separates chemical conversion from spatial redistribution, even when both change the measured concentration at the same location.

## Why thermal fluctuations and drag are connected

Small particles suspended in water move irregularly even without a sustained external force. Einstein's 1905 work connected Brownian motion to molecular thermal motion, osmotic pressure and diffusion, making visible particle displacement a quantitative probe of molecular behaviour. Water molecules strike from different directions and their forces do not cancel exactly over short intervals. Meanwhile, motion relative to the liquid produces viscous drag. Random forcing and resistance arise from the same surrounding medium and cannot be specified independently without regard to equilibrium.

At times longer than momentum relaxation, before boundaries restrict displacement, ordinary diffusion can have zero mean displacement along one direction while mean-square displacement continues growing. Squaring each displacement before averaging over particles or repeated trajectories prevents positive and negative motions from cancelling. Its dimension is length squared, explaining why a diffusion coefficient has units of area per time. A mean-square displacement proportional to time corresponds to a root-mean-square displacement growing as the square root of time, not linearly like uniform motion.

Brownian diffusion and dragEq. 8

![Brownian diffusion and drag](https://ml-biomat.com/static/agent-math/720c101dd3bb356949ec1606.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| 〈[Δx(t)]²〉 | Mean-square displacement along one coordinate | m² |
| Δx(t) | Position change after elapsed time t | m |
| 〈 〉 | Average over independent trajectories or a suitable ensemble | 1 |
| D | Translational diffusion coefficient | m² s⁻¹ |
| t | Displacement lag time | s |
| kB | Boltzmann constant, 1.380649×10⁻²³ | J K⁻¹ |
| T | Bath absolute temperature | K |
| ζ | Linear drag coefficient: resistance magnitude divided by speed | N s m⁻¹ |

Reading the relationshipVariances of independent diffusive increments add, making mean-square displacement grow with time. Thermal-equilibrium matching of noise and drag gives D=kBT/ζ.

A worked exampleFor T=300 K and ζ=4.141947×10⁻⁹ N s m⁻¹, D=10⁻¹² m² s⁻¹. At t=1 s, one-coordinate mean-square displacement is 2 μm² and root-mean-square displacement about 1.414 μm.

ConditionsHomogeneous thermal-equilibrium medium, linear drag and ordinary drift-free diffusion beyond inertial relaxation and before confinement. Total three-dimensional mean-square displacement is 6Dt.

The drag coefficient relates the magnitude of low-speed resistance to speed and is measured in newton seconds per metre. Greater drag gives slower diffusion at the same temperature. Increasing temperature strengthens thermal fluctuations when other conditions are fixed. This is a specific fluctuation–dissipation connection. A model containing drag without thermal noise would let the particle settle incorrectly into complete rest. Noise without the matching dissipation would likewise fail to maintain the proper thermal-equilibrium distribution. Their relation is part of thermodynamic consistency rather than an adjustable visual feature of a trajectory.

[Figure: Brownian trajectory and linear one-coordinate mean-square displacement](https://ml-biomat.com/tutorials/biomaterials-courses/cp11/en/#en-s5)

Figure 3 · The upper schematic trace distinguishes endpoint displacement from total path length. Below, one-dimensional ensemble mean-square displacement grows linearly with lag time in ordinary diffusion. A single trajectory need not trace a smooth line.

For a sphere much larger than molecular dimensions with a no-slip surface, low-Reynolds-number Stokes drag further connects diffusivity to liquid viscosity. Nearby walls, concentrated suspensions, viscoelastic surroundings and nonspherical shapes modify resistance and temporal correlations. Polymer chains additionally possess internal motion: segments can move locally before the entire centre of mass reaches its longer-time diffusion regime. A displacement measurement must therefore identify whether it follows a particle centre, polymer centre of mass or labelled segment. These coordinates can have different time dependences in the same specimen.

Pauses or backward steps in a trace do not immediately establish trapping. Ordinary random motion already moves both ways. Testing restricted diffusion requires multiple trajectories and statistics across several time intervals. A long-time plateau in mean-square displacement may reflect confinement or a finite cage. Growth slower than linear over an interval may involve viscoelastic memory or obstacles. Instrument resolution and motion blur also need attention so that a measurement timescale is not mistaken for a material mechanism. Different physical pictures should be compared using the same observable and observation window.

Random motion still permits precise predictions. Initial conditions and environment determine probability distributions, mean-square displacements and correlation times that can be tested through repeated measurements. Randomness is part of the object being described, rather than a reason to stop explaining it. Drug transport through a network, molecular motion within a membrane and particle probes of local viscoelasticity all benefit from this statistical description because its predictions correspond directly to measurable quantities. The same framework also clarifies which additional information is needed when ordinary diffusion ceases to apply.

## How heat and material flows become coupled

Real materials often experience several driving forces together. A temperature gradient produces heat flow and may also separate mixture components. A concentration difference drives matter and can accompany additional heat transport. Describing such coupling begins by pairing fluxes with thermodynamic forces. A force here need not be a mechanical force measured in newtons. It can involve spatial differences in reciprocal temperature or chemical potential, defined so that each flux–force product has units of entropy-production rate.

In one-dimensional heat conduction, heat flows toward lower temperature, while the thermodynamic force can be chosen as the gradient of reciprocal temperature. These point in the same direction, giving a nonnegative product. Isothermal material transport can use minus the chemical-potential gradient divided by temperature. Chemical potential is the free-energy change associated with adding an amount of material and incorporates concentration, interactions and appropriate external-field effects. Correct force definitions place distinct transport processes into one entropy-production framework instead of treating every gradient as interchangeable.

Onsager's 1931 work on reciprocal relations showed that cross-response coefficients have a definite connection near equilibrium when microscopic reversibility and appropriate variable definitions apply. Material transport caused by a temperature difference and heat transport caused by the corresponding material driving force are not unrelated phenomena. Reciprocity provides information beyond the requirement that total entropy production be nonnegative. It also requires dynamical conditions more specific than the second law alone. This makes it a powerful constraint on coupled transport rather than a consequence of energy accounting by itself.

Linear response of two coupled fluxesEq. 9

![Linear response of two coupled fluxes](https://ml-biomat.com/static/agent-math/81cc6e6acd179b4b2d0623f4.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Jq | Heat flux with a specified energy convention | W m⁻² |
| Jn | Amount flux | mol m⁻² s⁻¹ |
| Xq | Reciprocal-temperature gradient conjugate to heat flux | K⁻¹ m⁻¹ |
| Xn | Conjugate material force; at fixed temperature, minus chemical-potential gradient divided by temperature | J mol⁻¹ K⁻¹ m⁻¹ |
| Lqq | Direct heat-response coefficient | W K m⁻¹ |
| Lqn, Lnq | Cross coefficients using matched conjugate definitions | mol K m⁻¹ s⁻¹ |
| Lnn | Direct material-response coefficient | mol² K J⁻¹ m⁻¹ s⁻¹ |
| σs | Entropy-production rate per volume | W K⁻¹ m⁻³ |

Reading the relationshipNear equilibrium, expand fluxes linearly in small forces. Summing conjugate flux–force products gives entropy production; suitable microscopic reversibility additionally yields reciprocity.

A worked exampleFor Jq=0.2 W m⁻², Xq=0.01 K⁻¹ m⁻¹, Jn=10⁻⁶ mol m⁻² s⁻¹ and Xn=100 J mol⁻¹ K⁻¹ m⁻¹, σs=0.002+0.0001=0.0021 W K⁻¹ m⁻³.

ConditionsOne-dimensional local linear response, matched conjugate definitions, no time-reversal-odd external field and equal time-reversal parity of the relevant state variables. The symmetric coefficient part must be positive semidefinite; general fields require Onsager–Casimir relations.

Linear response expands fluxes around equilibrium and retains the leading terms proportional to small forces. The material need not be simple at every scale; the investigated perturbation must be small enough that coefficients remain approximately constant. Strong fields, evolving structure or marked shear thinning generally require extensions. Reciprocity also depends on how variables transform under time reversal. With a magnetic field or another time-reversal-odd control, the Onsager–Casimir form includes field reversal and parity signs rather than an unconditional equality at the same field.

Comparing cross coefficients experimentally requires matching flux and force definitions. Whether heat flux has had a transported-energy contribution subtracted, and whether chemical potential is stated per particle or per mole, affects numerical values and units. Comparing two differently defined slopes directly can mistake a convention change for failure of reciprocity. A sound procedure first writes the entropy-producing flux–force pairs and then relates experimental control variables to those quantities. The conversion is part of the scientific comparison, not a cosmetic change of symbols.

Coupling explains an apparently surprising possibility: one flux can run against its own driving force while another process supplies energy, with the total entropy production remaining nonnegative. Thermoelectric devices, membrane transport and electrochemical processes can transfer energy this way. The sign of one isolated product cannot characterize dissipation of the whole device. All coupled processes must be included to evaluate refrigeration, separation or conversion efficiency. A locally uphill process is compatible with a globally dissipative operation when the energy and entropy balances include its driving source.

In polymers, coupling coefficients may depend on concentration, orientation and temperature. An aligned liquid-crystal polymer can transport heat or matter differently along different directions. Swelling changes membrane thickness and therefore the macroscopic transport rate. Such effects can sometimes be treated with local linear relations, or may require evolving structural variables. Thermodynamics constrains allowed relations and signs, while experiments or microscopic models determine the material-specific coefficients. This division of roles makes the framework useful without pretending that an entropy inequality supplies every kinetic parameter.

## Viscous dissipation and sustained steady states

Place a polymer liquid between two plates, fix the lower plate and move the upper one. Adjacent liquid layers then slide at different speeds. Shear rate measures the velocity change across the perpendicular direction and has units of inverse seconds. Shear stress is tangential force per area, measured in pascals. For a Newtonian liquid, stress is proportional to shear rate, with viscosity as the proportionality coefficient. The moving plate continuously performs work. When that work is not stored in another form, it ultimately becomes heat.

Dissipation power in Newtonian shearEq. 10

![Dissipation power in Newtonian shear](https://ml-biomat.com/static/agent-math/299699fbd37d4e3be0ac5da3.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| τ | Shear stress | Pa |
| η | Nonnegative Newtonian viscosity | Pa s |
| γ̇ | Simple shear rate, velocity gradient across layers | s⁻¹ |
| pdiss | Mechanical dissipation power per volume | W m⁻³ |

Reading the relationshipTangential force per area times relative speed gives power; dividing by layer volume gives stress times shear rate. Newtonian substitution produces a square, so reversed shear still dissipates.

A worked exampleFor η=10 Pa s and shear rate 2 s⁻¹, τ=20 Pa and pdiss=40 W m⁻³. At −2 s⁻¹, stress is −20 Pa while dissipation remains 40 W m⁻³.

ConditionsSimple shear of a Newtonian liquid without additional recoverable storage. For viscoelastic materials, subtract stored-energy rate from mechanical input to identify dissipation.

Reversing the shear direction reverses both stress and shear rate, leaving their product positive. Back-and-forth stirring therefore does not cancel dissipation. At approximately constant viscosity, increasing shear rate raises dissipated power per volume as its square. A viscous melt flowing quickly through a narrow die can generate enough local heat to affect temperature and flow properties. Isothermal modelling and nearly adiabatic processing require different energy balances even if their instantaneous velocity fields initially look similar.

Polymer liquids often retain elastic memory, temporarily storing part of the work in chain conformation or orientation. Releasing a suddenly stretched material can recover some energy through recoil, while internal friction converts another part into heat. Instantaneous stress times deformation rate is then mechanical input power, not automatically irreversible dissipation at every moment. The rate of recoverable stored-energy change must be subtracted to identify the dissipative remainder. Over a complete cycle returning stored energy to its initial value, net mechanical input more directly measures loss.

[Figure: Mechanical input, recoverable storage and heat removal](https://ml-biomat.com/tutorials/biomaterials-courses/cp11/en/#en-s7)

Figure 4 · A viscoelastic material partitions work into stored-energy change and dissipation. Stored energy can be recovered during recoil; dissipated energy is transferred as heat. Constant-temperature operation requires heat removal and does not imply zero dissipation.

This distinction gives dissipative material a precise experimental meaning. Damping materials use energy loss during repeated motion to reduce amplitude, while elastic storage controls phase and restoring force. If heat cannot escape quickly, temperature changes alter relaxation times. Comparing materials therefore requires matched frequency, temperature and deformation amplitude. A material that flows readily under slow deformation may appear much stiffer during a fast impact because internal relaxation competes with observation time. Energy storage, loss and heat removal must be considered together to predict repeated operation.

A driven steady state connects these processes. Continuous boundary work accompanied by adequate heat removal can maintain nearly constant temperature with ongoing dissipation. Similarly, supplying reactants and removing products can sustain constant concentrations with nonzero reaction flux through a chemical network. Stationarity means macroscopic quantities no longer accumulate. Equilibrium additionally requires the corresponding net irreversible fluxes to vanish. Looking for continuous inputs and outputs is a direct experimental way to distinguish them, especially when a single snapshot shows no visible change.

Spatial order does not imply low dissipation. Regular convection, persistently rotating orientational structures and collective motion in active matter can all rely on continuing energy supply. Entropy production depends on fluxes and forces, not on whether a pattern looks tidy. Conversely, a motionless specimen with nonuniform concentration may remain far from equilibrium because its dynamics are extremely slow. Direction of change, spatial pattern and relaxation speed are related but separately measurable properties. Keeping them distinct prevents an attractive image or a stationary signal from being mistaken for a complete thermodynamic diagnosis.

## Turning the direction of change into testable questions

A reliable first step in studying irreversibility is to draw the system boundary. Is the object a particle, particle plus solvent, or the full assembly including reservoirs and power supplies? Changing the boundary reallocates internal entropy change and exchanged entropy, while the complete conservation and entropy balances must stay consistent. A falling concentration inside a membrane can reflect outward diffusion, reaction or dilution as the membrane swells. Identifying conserved quantities and exchange routes comes before assigning a mechanism to the observed change.

The second step separates individual trajectories from statistics across repeated experiments. Over short intervals, a small particle may move against an applied force, and some entropy changes in small systems may temporarily be negative. Stochastic thermodynamics extends work, heat and entropy to individual trajectories under suitable dynamical conditions and uses fluctuation relations to connect forward and reverse statistical weights. Seifert's 2005 trajectory formulation included both system and environmental contributions to total entropy production, bringing such fluctuations and the average second law into a consistent description.

These relations express direction through probability distributions and average constraints rather than removing it. Forward and reverse preparations, possible reversal of a driving protocol and the definition of the environment must be explicit. Fluctuation relations derived under different conditions are not interchangeable. The two-chamber interaction already illustrates fluctuations of a macroscopic counting variable. Interpreting its displayed entropy as total stochastic entropy production would require additional definitions of distributions and environmental exchange. Matching the measured quantity to the theoretical one is essential before testing a particular relation.

The third step checks timescales. Molecular collisions, momentum relaxation, local diffusion, whole-chain relaxation and specimen-wide thermal equilibration can differ by many orders of magnitude. Treating a polymer as an instantaneously equilibrated liquid before its internal modes relax can make a fitted viscosity or diffusivity depend on the measurement window. Local equilibrium assumes that a small region relaxes internally while larger-scale temperature or concentration changes slowly. The region must be spatially small compared with those variations yet contain enough particles for meaningful thermodynamic averages.

The fourth step measures driving forces together with responses. Observing a material flux alone does not reveal whether concentration, electrical potential, temperature or pressure drives it. A temperature rise alone does not distinguish external heating, chemical heat release and viscous dissipation. Measuring relevant gradients, boundary inputs and changes in stored energy allows alternatives to be compared within the same balance. Before adopting linear response, vary the driving amplitude and test whether the inferred coefficient remains approximately constant rather than naming the model from a single perturbation.

For a polymer during processing or operation, ask which quantities are stored, which cross the boundary, which internal modes remain unrelaxed and which processes continuously generate heat. These questions connect molecular motion to temperature, velocity, concentration and stress. They also explain the prominence of memory in polymers: a connected chain contains many coupled freedoms, and completion of local motion does not imply restoration of equilibrium for the whole molecule. Measurements at different times can therefore probe distinct stages of one relaxation process.

Macroscopic irreversibility becomes a calculable physical problem through these connections. Motion among accessible states usually carries a specially prepared distribution toward more common macroscopic arrangements. Thermodynamic constraints organize direction, while kinetics determines speed. Small-system fluctuations and driven steady states show how the framework operates under different conditions. This foundation leads directly to the dynamics of long chains, the gradual disappearance of stress and the changing stiffness and flow response of materials observed over different timescales.
