# From One State to Many Possibilities: Phase Space, Probability and Ensembles

Source: https://ml-biomat.com/tutorials/biomaterials-courses/cp02/en/
Language: en

Knowing where a chain or particle is does not fully determine its next motion, and one observation need not give a stable material property. Begin with position and momentum, build state space and probability averages, and distinguish ensembles through energy, thermal contact and particle exchange. A slow-jump model then connects equilibrium probabilities with finite observation times.

## What must be known to predict motion

Attach an object to a small spring, displace it and release it. When it passes through the equilibrium position it may be moving left or right; position alone does not uniquely determine where it goes next. A complete mechanical state also requires motion, usually represented in classical mechanics by momentum rather than velocity. For simple translation, momentum is mass times velocity. At a fixed mass, greater momentum magnitude means faster motion, while its sign records direction along a chosen coordinate. Position and momentum together distinguish states that look identical in a photograph but have different immediate futures.

Let q be displacement from equilibrium and p its associated momentum. The ideal frictionless spring has kinetic energy of motion and potential energy of deformation. Kinetic energy increases with momentum squared, and spring potential energy increases with displacement squared. Equal leftward and rightward displacements therefore have the same elastic cost. Potential energy is determined by the current configuration and specified interactions. For this conservative force, it does not depend on the path taken to reach the position. Even this small system is sufficient to connect the idea of a state to its energy and the rule governing its subsequent motion.

Hamiltonian of a one-dimensional ideal oscillatorEq. 1

![Hamiltonian of a one-dimensional ideal oscillator](https://ml-biomat.com/static/agent-math/7851a130b4966888e3a569de.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| H | Total mechanical energy | J |
| q | Displacement from equilibrium | m |
| p | Conjugate momentum, here mass times velocity | kg m s⁻¹ |
| m | Oscillating mass | kg |
| k | Spring stiffness, not Boltzmann’s constant | N m⁻¹ |

Reading the relationshipKinetic energy is p²/(2m) and linear-spring energy kq²/2; their sum gives the energy of this frictionless conservative system.

A worked examplem=1 kg, k=4 N m⁻¹, q=0.1 m and p=0.2 kg m s⁻¹ give kinetic and potential energies 0.02 J each, totaling 0.04 J.

ConditionsOne-dimensional linear spring without friction, with fixed mass and stiffness. General Hamiltonians need not separate in this form.

A derivative expresses the local rate at which energy changes with a variable. Differentiating with respect to momentum gives the position's rate of change. Differentiating with respect to position and changing sign gives the restoring force, or rate of momentum change. These are Hamilton's canonical equations for the spring. Hamilton's 1834 work developed a route for organizing dynamics through energy and canonical variables, later providing an important foundation for statistical descriptions of many degrees of freedom. The formalism is useful because one energy function can generate a coordinated set of motion equations rather than separate unrelated rules for each variable.

Generating motion from energyEq. 2

![Generating motion from energy](https://ml-biomat.com/static/agent-math/3638add1f8b5ef2bae2167a6.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| q,p | Position and conjugate momentum | q: m; p: kg m s⁻¹ |
| q̇ | Time derivative of position, or velocity | m s⁻¹ |
| ṗ | Time derivative of momentum, or force | N |
| H | Hamiltonian | J |
| ∂H/∂p | Partial energy derivative in momentum at fixed position | m s⁻¹ |
| ∂H/∂q | Partial energy derivative in position at fixed momentum | N |
| m | Mass | kg |
| k | Spring stiffness | N m⁻¹ |

Reading the relationshipCanonical equations use local energy gradients to determine position and momentum rates; the negative potential gradient gives restoring force.

A worked exampleUsing m=1, k=4, q=0.1 and p=0.2 in the preceding units gives q̇=0.2 m s⁻¹ and ṗ=−0.4 N.

ConditionsFinal equalities use the oscillator of E1. Dots denote trajectory time derivatives; partial differentiation holds the other independent canonical variable fixed.

The word partial in partial derivative means that other independent variables are held fixed while one variable changes. Differentiation with respect to p here holds q fixed, and differentiation with respect to q holds p fixed. A time derivative instead follows change along the actual trajectory. Distinguishing them shows how the equations combine the shape of an energy function with movement through states. For more general coordinates, constraints or electromagnetic coupling, momentum need not have the simple relation to velocity used here. The Hamiltonian also need not separate into a momentum-only term plus a position-only term in every conservative description.

The same construction extends to a polymer model retaining coordinates and momenta of many beads. An effective bead may represent a group of atoms rather than one chemical particle, so forces and parameters must match that resolution. If surrounding solvent is omitted, drag and random forces make the retained beads an open effective system. Their mechanical energy alone is then not generally conserved. Identifying what has been retained and what exchanges energy with it comes before choosing a dynamical or statistical description. This boundary between a full microscopic model and a reduced model will remain important when defining ensembles and interpreting entropy.

## Phase space maps complete states

Use spring displacement as a horizontal coordinate and momentum as a vertical coordinate. One point records both numbers and represents a complete state. As the object moves, the point follows a curve in phase space. This is not the object's path across the laboratory: the object moves along a line, while its phase-space description requires two coordinates. Without friction, total energy stays constant and the trajectory follows an ellipse defined by the energy equation. Momentum vanishes at the left and right turning points. Near the central position, its magnitude is larger because energy is stored predominantly in motion.

[Figure: Opposite momenta on an oscillator energy ellipse](https://ml-biomat.com/tutorials/biomaterials-courses/cp02/en/#en-s2)

Figure 1 · At fixed energy the oscillator follows an ellipse in q–p phase space. Orange points share position but have opposite momenta. Axes are separately scaled; the ellipse has maximum |q|≈0.1414 m and |p|≈0.2828 kg m s⁻¹.

A degree of freedom is an independent coordinate needed to specify configuration. A free point particle in three dimensions needs three position coordinates. N such particles need 3N, and their conjugate momenta give a phase space of 6N dimensions. Rigid connections, fixed bond lengths and other constraints reduce the independent count. An axisymmetric rigid rod requires three coordinates for its centre and two angles for its axis if rotation about that axis is not distinguished. If axial spin is an independently relevant motion, its corresponding state variables must be included. The degree count follows the physical resolution and constraints rather than the object's name alone.

A high-dimensional state space does not place the specimen in extra physical dimensions. It records many independent numerical quantities simultaneously. Ten free beads in a three-dimensional model may have a sixty-dimensional phase space while their container remains three-dimensional. Drawing one or two coordinates is a projection, and different complete states may project onto the same point. Crossings seen in that projection therefore need not mean that deterministic dynamics gives one complete state two futures. Omitted coordinates or momenta may distinguish the apparently coincident points. This is why a visually simple observable may not provide a complete state description.

Under smooth Hamiltonian dynamics, a cloud of initial states may stretch and distort while preserving its fine phase-space volume, the Liouville volume-preservation property. The volume concerns canonical positions and momenta together, not the physical specimen volume or a projected image area. A probability distribution can develop fine structure and complicated geometry while retaining this property. Friction, random external driving or reduction to only some variables changes the question, and volume behavior in the retained space must then be examined separately. Confusing these different volumes would obscure the relation between microscopic reversible evolution and a reduced statistical description.

The state map puts accessible possibilities and actual evolution into one framework. Energy, connectivity and boundaries restrict the available region, while dynamics determines movement within it. Statistics must additionally assign weights to the states. Knowing which states are allowed does not establish how readily a particular experiment reaches them. Probabilities, ensembles and observation times address that distinction. The map is therefore a basis for statistical reasoning rather than a replacement for it, and it makes explicit both the variables retained in the model and the constraints defining the system being studied.

## Using probabilities and probability densities

For individually numbered states, assign a probability to each state i. Probabilities must be nonnegative and sum to one over an exhaustive mutually exclusive set, a requirement called normalization. If an observable has different values in different states, multiply each value by its probability and add to obtain its mean. The mean need not be a value ever observed individually. Equal-probability readings of zero and ten give mean five even though every measurement returns zero or ten. The average describes repeated observations rather than an unrecognized intermediate state, a distinction that matters when interpreting molecular populations or switches between conformations.

Normalization, mean and varianceEq. 3

![Normalization, mean and variance](https://ml-biomat.com/static/agent-math/0a411e34e2bff3b0b2160a38.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| i | Index over an exhaustive mutually exclusive state set | 1 |
| pi | Nonnegative probability of state i | 1 |
| Σi | Sum over all listed states | 1 |
| A,Ai | Observable and its state-i value; force in this example | N |
| 〈A〉 | Probability-weighted mean | N |
| Var(A) | Mean squared departure from the mean | N² |

Reading the relationshipProbabilities sum to one. They weight the average, while squared departures retain fluctuation magnitude without cancellation of signs.

A worked exampleTwo states with forces 0 N and 10 N, each probability 0.5, give mean 5 N, variance 25 N² and standard deviation 5 N.

ConditionsDiscrete states or specified state bins. Other observables keep their own units in the mean and squared units in the variance.

Fluctuations describe how far observations lie from the mean. Subtract the mean, square to prevent cancellation of signs, and average with the probabilities to obtain the variance. Its square root is the standard deviation and has the same units as the observable. A constant reading of five and alternating zero-or-ten readings have the same mean but different variability. For single-molecule measurements, small samples and materials near a transition, fluctuations often contain important mechanistic information. They should not automatically be treated as unwanted measurement error. Instrument noise and fluctuations of the physical system need to be distinguished through the measurement design.

Continuous states cannot each be assigned the same finite probability, since summing infinitely many such points would fail. Instead use a probability density. The probability of a small region is approximately density times its size, and integrating over the full allowed region gives one. Integration can be understood as dividing a region into small pieces, adding their probability contributions and refining the pieces. Density units are reciprocal to the units of the space's volume element. A density value may consequently exceed one without violating any probability rule; only the integrated probability must remain between zero and one.

Probability density in a two-dimensional phase spaceEq. 4

![Probability density in a two-dimensional phase space](https://ml-biomat.com/static/agent-math/3199506b93df0edb596a0f2a.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| dP | Probability contribution of an infinitesimal phase-space region | 1 |
| ρ(q,p) | Probability density relative to dq dp | (J s)⁻¹ |
| q,dq | Position and infinitesimal interval | m |
| p,dp | Momentum and infinitesimal interval | kg m s⁻¹ |
| ∫ | Integral over the full allowed phase-space region | 1 |

Reading the relationshipDensity times phase area gives probability. Integrating adds all region contributions and normalizes to one.

A worked exampleA uniform rectangle with Δq=0.2 m and Δp=0.4 kg m s⁻¹ has area 0.08 J s and density 12.5 (J s)⁻¹; half its area has probability 0.5.

ConditionsContinuous density for one position–momentum pair. Higher dimensions require the corresponding volume element and consistent transformation of density.

In the spring's two-dimensional phase space, a rectangle of displacement width 0.2 metres and momentum width 0.4 kilogram metres per second has phase area 0.08 joule seconds. A uniform normalized distribution on it has density 12.5 per joule second. Half the rectangle still carries probability 0.5. The number 12.5 is not a probability above one hundred percent; it must be multiplied by a phase area. Changing coordinate units changes the numerical density but not the probability of the same physical region. This provides a useful check on normalization and on the consistency of coordinate transformations.

Polymer problems often divide a continuous conformation space into identifiable regions before collecting their probabilities. Regions might represent endpoint-distance intervals, ranges of helical content or binding states. They should be mutually exclusive and exhaustive for the chosen state set, or any omitted portion must be identified. Writing the probability-weighted average explicitly also identifies which states affect an experiment and which contribute most strongly. Phase-space geometry and its probability distribution now jointly determine a measurable quantity. The distribution carries information beyond the list of permitted states, allowing two preparations of the same mechanical system to have different statistical properties.

## Why time averages and ensemble averages differ

Following one specimen continuously and averaging its readings over an interval gives a time average. Preparing many independent specimens under the same macroscopic conditions, observing them at one instant and averaging gives an ensemble average. An ensemble does not require physically placing all those specimens in one container. It represents possible systems with the same laws and specified conditions but different microscopic states. Gibbs's 1902 treatise systematically developed this framework, organizing thermodynamic constraints and state probabilities together. The distinction between averages becomes practical whenever samples move slowly among states or experiments compare repeated preparations with one long record.

Averaging along one history or across specimensEq. 5

![Averaging along one history or across specimens](https://ml-biomat.com/static/agent-math/b4c93d6dc6676bbad98d602e.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Ātime | Time average of one record | same as A |
| tobs | Total observation duration | s |
| A(t) | Observable at time t | units of the selected observable |
| t,dt | Time and infinitesimal time interval | s |
| ∫ | Accumulate readings over time | 1 |
| 〈A〉ens | Ensemble average under the specified distribution | same as A |
| pi,Ai | State probability and corresponding observable value | pi: 1; Ai: same as A |
| Σi | Sum over the listed states | 1 |

Reading the relationshipTime averaging weights by duration; ensemble averaging weights by state probability. Their agreement depends on distribution, dynamics and observation time.

A worked exampleA switch spending 3 s in B during a 10 s record has time-average indicator 0.3 when B=1 and A=0. An ensemble with half its specimens in B has mean 0.5.

ConditionsAn adequately resolved sampled record approximates the time integral. Equality of finite-time and ensemble averages is not assumed.

[Figure: Boundaries and exchanges for three ensembles](https://ml-biomat.com/tutorials/biomaterials-courses/cp02/en/#en-s4)

Figure 2 · Each box represents a possible system in its ensemble, with many such states defining a distribution. Arrows identify permitted exchange types, which occur in both directions. E is energy, V volume, N particle number, T temperature and μ chemical potential per particle.

Equality of the two averages requires dynamical conditions. For an appropriate stationary distribution, ergodicity makes long-time averages agree with ensemble averages for typical initial states. It does not require visiting every point of a continuous space within finite time, nor does it follow simply from waiting for an unspecified interval. Accessible regions may be disconnected or joined by barriers crossed only rarely. In the latter case a system can be ergodic in an asymptotic mathematical sense while an experiment remains confined to one region. A useful discussion therefore specifies the distribution, the observable and the actual observation time.

An ensemble average also does not automatically guarantee numerical accuracy. Too few independent samples, an incorrect initial distribution or state-dependent detection can bias it. Repeatedly preparing specimens trapped in the same local state does not repair failure to sample another relevant class of states. Slow polymer relaxation, folding barriers and entanglement constraints make preparation history and waiting time part of the statistical problem. Identify the target distribution and check whether the sampling represents it before relying on either average. Increasing the sample count improves precision only for the distribution actually sampled, which may still differ systematically from the desired one.

Random conformation changes can be used to sample a distribution. The 1953 work of Metropolis, both Rosenbluths and both Tellers provided a classic method for sampling interacting systems according to equilibrium weights. In a fixed-length chain ensemble, every sample retains the same segment count. Allowing length to change requires a separately defined statistical model. Local rotations or exchanges must produce the correct weights and connect the relevant state regions. Satisfying an acceptance-probability rule alone does not ensure that the available moves can reach every necessary conformation. Connectivity of the sampling process and its equilibrium weighting are related but distinct requirements.

Lattice self-avoiding chains make the distinction concrete. If each step always attempts one of four directions equally and any collision restarts the whole chain, successful fixed-length direction sequences have equal original weights. Choosing instead only among currently available directions gives history-dependent branching counts and can introduce growth bias requiring correction. In either method, a sampling step is not normally one second of molecular motion. It is first a way to explore a probability distribution. Only physically calibrated kinetic rules justify interpreting the sequence as real-time evolution, an important distinction when comparing an equilibrium conformation calculation with a measured relaxation curve.

## The microcanonical ensemble for an isolated system

If a system exchanges neither energy nor particles with its surroundings and has a fixed container with time-independent interactions, total energy can serve as a constraint. A statistical description then concentrates on accessible states near that energy, defining a microcanonical ensemble. Measurements have finite energy resolution, so it is useful to consider a thin energy shell rather than count a single exact continuous energy value as though it were a discrete state. The shell should be narrow enough to preserve the macroscopic conditions of interest while containing the microscopic states needed for the chosen statistical description.

Microcanonical weights in an energy shellEq. 6

![Microcanonical weights in an energy shell](https://ml-biomat.com/static/agent-math/39d8ba9466cd8137ed479307.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| pi | Probability of microstate i within the energy shell | 1 |
| Ω(E,ΔE) | Equal-weight state count in the defined energy shell | 1 |
| E | Lower energy boundary of the shell | J |
| ΔE | Positive shell energy width | J |
| S | Microcanonical entropy | J K⁻¹ |
| kB | Boltzmann constant, 1.380649×10⁻²³ | J K⁻¹ |
| ln | Natural logarithm | 1 |

Reading the relationshipCount and normalize equally weighted states within the prescribed energy shell; their logarithmic count gives entropy.

A worked exampleFor eight equally weighted discrete states, each probability is 1/8 and S=kB ln8≈2.871×10⁻²³ J K⁻¹.

ConditionsIsolated equilibrium at fixed volume and particle number. Applies inside E≤Ei<E+ΔE, with zero probability outside; continuum systems need consistent phase measure and state counting.

Equal weighting applies to allowed microstates defined with a consistent phase-space measure. It does not imply uniformity in every projected coordinate. An oscillator moves slowly near its turning points and spends more time there, making its position distribution nonuniform. Geometry and speed connect the energy curve to its projection onto the position axis. Reading equal energy-state weighting as equal probability for all positions would lose that connection. An energy shell or the corresponding induced energy-surface measure preserves the relationship between counting and dynamics. Even a simple oscillator therefore illustrates why the measure used to define a probability matters.

Macroscopic thermodynamic quantities can be obtained from the constrained state set. As energy, volume or particle number changes, the number of accessible states changes and so does entropy. Energy allocation between systems brought into contact is related to how their combined state count grows. Temperature is consequently not just a renamed kinetic-energy value; it is also connected to the energy dependence of the state count. Simple classical systems obeying equipartition relate mean kinetic energy directly to temperature. Frozen quantum degrees of freedom, interactions and constraints require the appropriate statistical treatment rather than unconditional application of that simple relation.

For an ideal frictionless spring, specifying total energy without specifying oscillation phase permits an ensemble distributed around one energy orbit. This differs from specifying energy, position and momentum completely for one state. The ensemble reflects a distribution over states; the fully specified state follows a definite deterministic trajectory in the model. Such distributions and their entropies can be discussed even for one particle. Small particle number changes fluctuation magnitudes and possible thermodynamic approximations, but does not make probability or statistical mechanics meaningless. It instead makes the definition of states and the measurement protocol especially visible.

Polymer experiments commonly exchange heat with their surroundings, so perfect isolation is often an idealization. The microcanonical viewpoint remains useful because the specimen together with a sufficiently large environment can be treated as a larger isolated system. The specimen's own equilibrium weights can then be derived from the number of environment states compatible with each specimen energy. The exponential probabilities in the next ensemble are thus connected to a physical counting argument rather than chosen arbitrarily. Defining the boundary between specimen and environment makes different ensembles expressions of the same statistical logic under different conditions of exchange.

## Why a heat bath produces Boltzmann weights

Place a specimen in contact with a large heat bath, allowing energy exchange while keeping specimen volume and particle number fixed. Specimen energy fluctuates, but the bath is large enough that its temperature changes negligibly in those exchanges. This defines a canonical ensemble. Treating specimen plus bath as isolated, any energy gained by the specimen is lost by the bath. The bath has different numbers of states at different energies, changing the relative probability of specimen states. Expanding the bath entropy near its initial energy produces the exponential Boltzmann weight. Thermal equilibrium thus determines a particular distribution through counting of the larger combined system.

Canonical Boltzmann weightsEq. 7

![Canonical Boltzmann weights](https://ml-biomat.com/static/agent-math/71ee666700d9456c659e7489.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| β | Inverse thermal energy | J⁻¹ |
| kB | Boltzmann constant | J K⁻¹ |
| T | Absolute heat-bath temperature | K |
| Z | Partition function summing microstate weights | 1 |
| i | Index of a complete microstate | 1 |
| Ei | Microstate energy | J |
| e | Natural-exponential base | 1 |
| Σi | Sum over all allowed states | 1 |
| pi | Normalized state probability | 1 |

Reading the relationshipThe change in bath state count with exchanged energy produces exponential weights. Dividing by their sum normalizes the probabilities.

A worked exampleOne zero-energy state and three states at energy 2kBT give Z=1+3e⁻²≈1.4060 and total upper-level probability 3e⁻²/Z≈0.2888.

ConditionsEquilibrium at fixed T,V,N with a weakly coupled large bath. The discrete form counts microstates; degeneracy requires individual counting or a multiplicity factor.

An exponential requires a dimensionless argument, so energy is divided by Boltzmann's constant times absolute temperature. Boltzmann's constant is 1.380649 times ten to the minus twenty-three joules per kelvin; at three hundred kelvin the thermal-energy scale is about 4.14 times ten to the minus twenty-one joules. The partition function adds weights of all microstates to normalize their probabilities. It is generally not the unweighted number of states. Only special circumstances, such as equal appropriately zero-referenced energies for all included states, reduce it directly to simple counting. Keeping this distinction clear prevents an energy-dependent normalization from being interpreted as a bare multiplicity.

If several microstates share an energy, their probabilities must be added to obtain the probability of that energy level. Suppose the lower level has one state and a higher level has three, separated by two thermal-energy units. Each higher state has weight the exponential of minus two relative to the lower state. Adding all three gives a total higher-level probability of about 0.289. Although each higher-energy state is individually less probable, its three realizations make a substantial combined contribution. This distinction between a microstate and an energy-level population is especially important for molecules with many conformations or symmetry-related arrangements.

From probabilities to energy, entropy and free energyEq. 8

![From probabilities to energy, entropy and free energy](https://ml-biomat.com/static/agent-math/39da3ed95b5cb6206a4b6f80.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| U | Mean internal energy | J |
| F | Helmholtz free energy | J |
| S | Statistical entropy | J K⁻¹ |
| pi,Ei | State probability and energy | pi: 1; Ei: J |
| i,Σi | Microstate index and summation | 1 |
| kB | Boltzmann constant | J K⁻¹ |
| T | Absolute temperature | K |
| Z | Canonical partition function | 1 |
| ln | Natural logarithm, with zero-probability terms contributing zero by continuity | 1 |

Reading the relationshipInternal energy averages state energies. Substituting logarithms of Boltzmann probabilities into entropy gives F=U−TS and the relation between F and Z.

A worked exampleFor two equally probable zero-energy states, Z=2,U=0,S=kB ln2. At T=300 K, F≈−2.871×10⁻²¹ J, consistent with F=U−TS.

ConditionsCanonical equilibrium with fixed T,V,N and consistent energy reference and state counting. Absolute continuum entropy requires the corresponding physical phase-space measure.

The partition function also links probabilities to thermodynamics. Its natural logarithm gives free energy, internal energy is probability weighted, and entropy averages logarithms of probabilities. A more spread-out distribution generally involves more accessible information, but thermodynamic comparisons require consistent state definitions and constraints. The entropy expression vanishes for a single certain state and reduces to Boltzmann counting for equally likely states. A zero-probability term contributes zero through its continuous limit. These relations explain how a statistical model can predict both populations and thermodynamic quantities without treating them as disconnected measurements requiring unrelated assumptions.

Constructing a partition function from continuous classical phase space also requires a physical counting scale and consistent treatment of identical-particle indistinguishability. Standard expressions contain phase-space units set by Planck's constant and corrections for permutations of identical particles. These factors matter for absolute free energies, entropies and chemical potentials. Arbitrarily dividing a continuous distribution into bins and calling its binned entropy an absolute thermodynamic entropy would mix resolution changes into a physical result. The discrete examples here enumerate their states explicitly, making normalization and entropy directly checkable. A continuum model needs the corresponding measure specified with equal care.

## Particle exchange brings chemical potential into probability

Some systems exchange matter as well as heat. An adsorption site can bind or release a molecule from solution, particle number in a small solution region fluctuates through diffusion, and a polymer gel can absorb or release solvent. Equilibrium with large thermal and particle reservoirs is often described by a grand canonical ensemble at fixed temperature, volume and chemical potential. Particle number is no longer identical in every state. It fluctuates among allowed values, so a state must specify both how many particles are present and their internal microscopic arrangement. This extends the ensemble description without changing the basic requirement to normalize probabilities over all allowed possibilities.

Chemical potential measures the marginal change of an appropriate free energy when particles are added under specified thermodynamic conditions. Per-particle chemical potential has units of joules; a molar chemical potential has joules per mole, and the conventions are related by Avogadro's constant. It is not the kinetic energy currently carried by one particle, nor is it determined by concentration alone. Temperature, interactions and the reference convention also enter. During equilibrium exchange, the reservoir's chemical potential determines the statistical tendency to add or remove particles from the system, making it the appropriate control variable for the exchange process.

Grand canonical weights with particle exchangeEq. 9

![Grand canonical weights with particle exchange](https://ml-biomat.com/static/agent-math/789a5923e22e8a1c897d7114.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Ξ | Grand partition function over particle numbers and internal states | 1 |
| N | Fluctuating system particle number | 1 |
| i | Microstate index at fixed N | 1 |
| ΣN,Σi | Sum over allowed particle numbers and internal states | 1 |
| β | 1/(kBT), inverse thermal energy | J⁻¹ |
| EiN | Energy of microstate i with N particles | J |
| μ | Chemical potential per particle | J |
| PiN | Joint probability of that particle number and state | 1 |
| e | Natural-exponential base | 1 |

Reading the relationshipThe reservoir contribution of supplying particles enters with sample energy, and normalization covers both particle count and configuration.

A worked exampleIf only an empty state N=0,E=0 and an occupied state N=1,E=μ are allowed, both weights are one, Ξ=2 and each probability is 0.5.

ConditionsEquilibrium with large thermal and particle reservoirs at fixed T,V,μ; identical-particle counting must be consistent across N.

Energy minus chemical potential times particle number combines the sample's energy cost with the reservoir contribution of supplying those particles. The grand partition function sums over particle numbers and their internal states. For one site that can be empty or occupied, choose zero empty-state energy and occupied-state energy ε. Their weight ratio is the exponential of minus the difference between ε and chemical potential divided by thermal energy. Raising chemical potential or lowering the occupied-state energy both increase occupancy. The same energy difference controls these two changes in the simplest model, providing a direct bridge between reservoir conditions and a measurable bound fraction.

Occupancy of one empty-or-filled siteEq. 10

![Occupancy of one empty-or-filled site](https://ml-biomat.com/static/agent-math/220214c7cfd8b4a3a6250bc3.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Pocc | Probability that one particle occupies the site | 1 |
| ε | Occupied-state energy relative to the empty state | J |
| μ | Reservoir chemical potential per particle | J |
| kB | Boltzmann constant | J K⁻¹ |
| T | Absolute temperature | K |
| e | Natural-exponential base | 1 |

Reading the relationshipNormalize the empty weight one and occupied weight exp[−(ε−μ)/(kBT)] to obtain occupancy.

A worked exampleFor ε−μ=2kBT, Pocc=1/(1+e²)≈0.1192. For ε=μ, Pocc=0.5.

ConditionsOne particle at most, one empty and one occupied realization, no neighbor interactions. This can describe a classical independent adsorption site.

If occupied-state energy equals chemical potential, empty and occupied states each have probability one half. If the occupied energy exceeds chemical potential by two thermal-energy units, occupancy is about 0.119. This assumes one realization of each state and no interactions with neighboring sites. Multiple binding arrangements or cooperative and repulsive interactions change the state count and energies accordingly. The simple site model therefore explains a basic trend while identifying the physical additions needed for more complex adsorption or binding. A measured occupancy curve can then be used to test those additions rather than treating every deviation as a change in one unexplained fitting parameter.

Ensembles are not competing categories of material. They describe the same physical system under different exchange constraints. For suitable macroscopic short-range systems in a thermodynamic limit, many local or mean properties can agree across ensembles. Energy and particle-number fluctuations can still differ substantially in finite systems. Measuring a small specimen with fixed particle number and a region that freely exchanges particles asks different questions. Ensemble choice should therefore follow what the experiment permits to be exchanged and which average or fluctuation it needs to predict. This keeps the statistical boundary conditions connected to the actual physical preparation and measurement.

## The same equilibrium can have very different waiting times

Equilibrium probabilities describe how states are populated in the long run but do not determine transition speed. Suppose a molecule has conformations A and B, with B higher in energy. Thermal equilibrium balances probability flux from A to B against flux from B to A, linking the ratio of transition rates to the energy difference. Multiplying both rates by the same small factor lengthens waiting times without changing their ratio or the final populations. Energy differences and crossing barriers therefore play different roles: one controls relative equilibrium occupation, while the other can strongly control how rapidly that occupation is established.

Balanced probability flux for two equilibrium statesEq. 11

![Balanced probability flux for two equilibrium states](https://ml-biomat.com/static/agent-math/3efaac888735ede182d778c9.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| PAeq,PBeq | Equilibrium probabilities of states A and B | 1 |
| kAB,kBA | Transition rates from A to B and B to A | s⁻¹ |
| ΔE | EB−EA, the state energy difference | J |
| kB | Boltzmann constant | J K⁻¹ |
| T | Absolute temperature | K |
| e | Natural-exponential base | 1 |

Reading the relationshipDirectional probability flux equals occupation times escape rate. At equilibrium the fluxes balance and agree with Boltzmann populations under equal state multiplicities.

A worked exampleFor ΔE=kBT, PBeq/PAeq=e⁻¹≈0.3679 and PBeq≈0.2689. Rates kAB=0.04979 and kBA=0.13534 s⁻¹ have the same ratio.

ConditionsOne realization per state, thermal equilibrium and continuous-time Markov jumps. Additional driving or multiplicities require modifications.

[Figure: Two-state energies and a transition-energy barrier](https://ml-biomat.com/tutorials/biomaterials-courses/cp02/en/#en-s8)

Figure 3 · Energy is vertical and a schematic conformation coordinate horizontal. The difference between A and B minima sets equal-multiplicity equilibrium populations, while transition energy E‡ relative to each starting state affects escape. Horizontal spacing is not a molecular-distance measurement.

The interaction uses an explicit two-state jump model. Divide the energy difference by thermal energy to define δ, and introduce a nonnegative barrier parameter B that slows both directions. The base attempt rate is one per second. Directional rates have different exponential factors but retain the required equilibrium ratio. Waiting times for jumps follow exponential distributions, expressing a fixed instantaneous escape tendency while the system remains in a state. A jump is not guaranteed at regularly spaced times. After entering the other state, the appropriate escape rate determines the next waiting time. The model has a physical time unit because those kinetic rates have been specified.

Example rates with an adjustable barrierEq. 12

![Example rates with an adjustable barrier](https://ml-biomat.com/static/agent-math/1d8d6a16103303ca45a3707f.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| δ | Dimensionless energy difference | 1 |
| EA,EB | Energies of the two states | J |
| kB | Boltzmann constant | J K⁻¹ |
| T | Absolute temperature | K |
| kAB,kBA | Directional transition rates | s⁻¹ |
| k₀ | Common attempt rate, set to 1 in the interaction | s⁻¹ |
| B | Barrier above the higher-energy state divided by kBT; distinct from state label B | 1 |
| max | Take the larger of the two inputs | 1 |
| e | Natural-exponential base | 1 |

Reading the relationshipSet transition energy to the higher state energy plus BkBT. Subtracting each starting-state energy gives activation factors and guarantees rate ratio e⁻δ.

A worked exampleFor δ=1,B=2,k₀=1 s⁻¹, kAB=e⁻³≈0.049787 s⁻¹ and kBA=e⁻²≈0.135335 s⁻¹. Increasing B by one divides both rates by e without changing equilibrium populations.

ConditionsIllustrative thermally activated Markov model with B≥0 and constant attempt rate; individual molecular kinetics can require different prefactors and mechanisms.

If every independent specimen starts in A, the ensemble probability of B begins at zero and approaches its equilibrium value. The sum of the directional rates sets its relaxation time. One specimen, however, can only be in A or B and produces an irregular step-like record of jumps. Divide its total residence time in B by the observation duration to obtain its time-averaged occupancy. That quantity generally does not equal the ensemble probability exactly at an arbitrary finite instant. The latter compares many specimens at one time; the former accumulates occupation along one history. Their differences are visible even with exact knowledge of the model's rates.

Relaxation of a two-state ensembleEq. 13

![Relaxation of a two-state ensemble](https://ml-biomat.com/static/agent-math/1c15e0924f9216bd1b67d27e.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| p* | Equilibrium probability of B | 1 |
| kAB,kBA | Positive directional transition rates | s⁻¹ |
| τ | Relaxation time of B probability | s |
| PB(t) | Ensemble probability of B at time t | 1 |
| p₀ | Initial B probability, zero for all A and one for all B | 1 |
| t | Time since preparation | s |
| e | Natural-exponential base | 1 |

Reading the relationshipProbability changes by A-to-B inflow minus B-to-A outflow, producing a linear equation whose solution approaches equilibrium exponentially.

A worked exampleFor δ=0,B=2,k₀=1 s⁻¹, p*=0.5 and τ=e²/2≈3.6945 s. Starting all in A gives PB(τ)=0.5(1−e⁻¹)≈0.3161.

ConditionsTwo-state continuous-time dynamics with constant rates and a specified initial ensemble. A single trajectory’s cumulative time average differs from PB(t).

[Figure: Single jump record and probability averages](https://ml-biomat.com/tutorials/biomaterials-courses/cp02/en/#en-s8)

k₀=1 s⁻¹. Above is one random history. Below, green is ensemble probability, orange its cumulative B residence fraction, and grey dashed the equilibrium probability. The full record is 200 s; the vertical line marks the cumulative observation window. No autoplay.

Energy gap changes equilibrium populations; a common barrier changes recovery speed. Compare fast and slow jumps at fixed gap to distinguish finite-time occupation, instantaneous ensemble probability and long-term equilibrium.

Keep the energy difference at zero and increase the barrier. Equilibrium B probability remains one half, but at a high barrier a two-hundred-second record may contain no jumps. Changing the prepared state from A to B can then give very different observed occupancies. Generating another random realization shows variation between repeated experiments. Lowering the barrier permits more exchanges, improving long-time sampling of equilibrium. Both model rates remain positive, so each state remains accessible in the long-time limit. The finite-observation discrepancy comes from a record short relative to relaxation, rather than a permanent disconnection between state regions.

Preparation at equilibrium differs from beginning in a specified state. To generate an equilibrium ensemble, initial states should themselves be drawn from equilibrium probabilities. The interaction deliberately starts all specimens in one selected state to display relaxation. Protein switching, adsorption–desorption and local chain-relaxation records likewise require energy difference, barriers, preparation and record length to be considered together. Fitting final occupancy alone cannot determine transition speed. Combining populations with waiting-time observations gives information that neither measurement supplies by itself, and helps separate a changed thermodynamic preference from a changed kinetic obstacle to reaching it.

## Entropy, coarse graining and finite specimens

Probability entropy depends on a distribution rather than being an ordinary function of one instantaneous mechanical coordinate. A single particle can have a distribution over positions or energy states and therefore a statistical entropy; many particles are not a prerequisite for defining it. With a specified model and counting convention, entropy is a state quantity determined by the distribution. It differs from the particular process used to reach an equilibrium state, although a process can change both state and distribution. Independence from path does not mean that entropy cannot change when temperature, volume or energy changes.

For two independent subsystems, joint probabilities are products of their separate probabilities. The logarithm turns those products into sums, making their entropies additive. Correlated subsystems have additional information in their joint distribution, so adding marginal entropies without examining the correlation does not give the full entropy. Macroscopic short-range systems usually have good extensivity when boundary effects are relatively small: increasing material amount approximately scales entropy proportionally. Length itself does not scale with material amount for every geometry and is not universally an extensive thermodynamic variable. Temperature and pressure are familiar intensive quantities, distinguished by their behavior under system scaling rather than by informal descriptions of size.

Coarse graining merges unresolved details into larger state cells or fewer variables. It may use spatial boxes, finite measurement times or replacement of many atoms by effective chain segments. The coarse distribution retains information at selected scales while losing details inside cells or among eliminated variables. Under Hamiltonian evolution, a fine distribution can stretch into increasingly thin structures that fixed-resolution observations no longer resolve. Fine and coarse entropies can consequently evolve differently. Thermodynamic irreversibility also involves initial conditions, environment and observational scale. A single word such as disorder cannot replace this physical account of what information is retained and how the system evolves.

[Figure: Fine and coarse displays of the same regional probabilities](https://ml-biomat.com/tutorials/biomaterials-courses/cp02/en/#en-s9)

Figure 4 · Dark and light fine cells above have different probability densities. Below, each group of four becomes one coarse cell with the same total probability but unresolved internal differences. The diagram changes resolution rather than representing a physical time step.

Larger coarse cells are not automatically better. Very small cells may have too little data and mostly remain empty, while overly large cells merge interfaces, binding states or slow structures relevant to the question. Resolution should preserve the target phenomenon and account for memory in the retained dynamics. If eliminated degrees of freedom relax slowly, a memoryless evolution law may be inadequate, requiring additional variables or memory terms. The value of coarse graining lies in retaining the predictive relations needed for a problem, with calibration against experiments or a more detailed model. Resolution and dynamical assumptions must therefore be chosen together.

The thermodynamic limit usually increases particle number and volume together while holding density and other intensive conditions fixed. It helps define sharp transitions and stable macroscopic relations, but finite-system statistics remain meaningful. Averages over a small number of independent objects tend to fluctuate more, and correlations change the effective number of independent samples. In single-molecule and nanoscale measurements, distributions, variances, correlation times and preparation conditions often give a more complete description than one mean. Improving precision requires more effectively independent information, not merely a faster sampling rate along the same strongly correlated record.

Phase space specifies what a state contains. An ensemble assigns weights under defined exchange constraints. Dynamics determines how an observation explores those possibilities. Together they explain stable macroscopic properties with continuing microscopic fluctuations, as well as historical differences retained when waiting is too short. Keeping state definitions, normalization, model conditions and time scales explicit makes statistical mechanics applicable to real polymer shapes, thermal behavior and motion. An average then becomes part of a physical explanation connected to preparation and measurement, rather than a formal number whose relevance is assumed from its mathematical appearance.
