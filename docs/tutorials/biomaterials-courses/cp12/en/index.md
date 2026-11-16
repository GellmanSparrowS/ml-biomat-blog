# How Flexible Chains Move and Relax

Source: https://ml-biomat.com/tutorials/biomaterials-courses/cp12/en/
Language: en

The same soft material can flow under slow loading and recoil under rapid deformation. Follow loading, waiting and release to understand stress relaxation, then connect it to segment motion, fluid coupling and entanglement. An adjustable oscillatory experiment makes storage and loss directly visible.

## Why stiffness depends on observation time

A polymer melt can slowly spread yet recoil after a rapid stretch. A pressure-sensitive adhesive must flow into surface details during contact and support load during peeling. Calling such behaviour partly solid and partly liquid does not fully explain it. The key questions are how quickly shape is changed, how long molecules need to rearrange, and whether the observation occurs before or after that rearrangement. Changing the measurement time can change the response substantially without changing the material's composition.

A flexible polymer contains many connected segments. Thermal motion can alter local positions and directions, but neighbouring segments cannot move away independently. Moving one portion affects others through connectivity. Solvent or surrounding chains provide drag, while entanglements restrict some transverse motion. Local adjustments, changes of whole-chain shape and escape from the original surrounding environment consequently occur on different timescales. Macroscopic stress records the combined memory of these motions rather than a single universal molecular clock.

Parallel-plate shear gives a clear measurement geometry. Fix the lower plate and move the upper one horizontally, displacing the top of the specimen relative to its bottom. Shear strain is displacement divided by plate separation, describing the degree of shape change. Shear stress is tangential force divided by loaded area, describing the required action per area. Normalizing force and displacement by geometry makes comparisons between specimen sizes meaningful instead of comparing raw instrument readings. The sign convention indicates the chosen shear direction rather than a distinction between stronger and weaker materials.

From force and displacement to stress and strainEq. 1

![From force and displacement to stress and strain](https://ml-biomat.com/static/agent-math/3be2687b9cfc19c20134b490.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| σ | Simple shear stress | Pa |
| F | Tangential force on the upper plate | N |
| A | Effective loaded area | m² |
| γ | Simple shear strain | 1 |
| Δx | Relative horizontal plate displacement | m |
| h | Plate separation | m |

Reading the relationshipDivision by area removes loaded-size dependence; division by gap converts displacement into relative shape change. One pascal equals one newton per square metre.

A worked exampleF=0.1 N and A=10⁻³ m² give σ=100 Pa. Displacement 10 μm across a 1 mm gap gives γ=0.01, or 1%.

ConditionsIdeal uniform parallel-plate simple shear without boundary slip; rotational geometries require their appropriate spatial conversion.

An ideal spring has stress determined by current strain and recovers when stress is removed. An ideal Newtonian viscous element has stress determined by strain rate and continues deforming under sustained load. Real polymers show recoverable and nonrecoverable contributions whose relative importance changes with time. Springs and viscous elements represent constitutive relations, not literal metal springs and pistons installed inside molecules. Their value is that they make experimentally different responses calculable before a molecular interpretation is added.

Deformation amplitude also matters. In a small-deformation range, doubling strain approximately doubles stress; disturbances imposed at different times can also be added. This is linear response. At larger deformation, orientation, chain stretching, structural change or slip may invalidate that proportionality. Linear rheology provides a clear starting point because it reads existing timescales while minimizing large changes to the structure being measured. An amplitude check therefore belongs before interpreting a frequency sweep as an intrinsic relaxation spectrum.

Temperature and material state must likewise be specified. The chain models developed below mainly concern flexible solutions or melts in which segments remain mobile. Frozen local motion in a glass, crystalline constraints and permanent elasticity of a chemically crosslinked network add other mechanisms. A polymer name alone does not identify its state. Molecular mass, concentration, temperature and crosslinking determine which dynamical description applies. These conditions allow a statement about stiffness or viscosity to become a reproducible material comparison rather than an unconditional label.

## Hold deformation and watch stress disappear

Rapidly shear a material to a small strain, then hold its shape fixed. Stress commonly decreases with time: stress relaxation. Chains initially lack time to rearrange and generate substantial stress; later rearrangement reduces the stress needed to maintain the same shape. A different experiment applies a constant small stress and measures the continuing growth of strain, called creep. The two protocols control different quantities. Their time-dependent curves are not obtained by simply taking pointwise reciprocals, even though both characterize linear response.

In his 1867 treatment of dynamics and viscosity, Maxwell introduced the idea of elastic action relaxing over a characteristic time. A spring in series with a viscous element now commonly represents the simplest Maxwell model. Series connection gives the elements equal stress and makes their strains add. Spring strain is determined by stress, whereas viscous strain rate is determined by stress. Adding the two contributions produces a relation containing both stress and its rate of change, connecting elastic storage with continuing flow.

Spring and viscous element in seriesEq. 2

![Spring and viscous element in series](https://ml-biomat.com/static/agent-math/736b77e1bfa431f4221dd472.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| γ̇ | Time rate of total shear strain | s⁻¹ |
| σ | Common shear stress in the series elements | Pa |
| σ̇ | Time rate of stress | Pa s⁻¹ |
| G₀ | Spring shear modulus | Pa |
| η | Viscous-element viscosity | Pa s |
| τ | Single Maxwell relaxation time | s |
| dot | A dot above a variable denotes a time derivative | 1 |

Reading the relationshipSeries strains add. The spring strain rate equals stress rate divided by modulus; the viscous rate equals stress divided by viscosity. Both have inverse-time units.

A worked exampleFor G₀=1,000 Pa and η=10⁴ Pa s, τ=10 s. At constant stress 100 Pa the spring strain stops changing and total strain rate is 0.01 s⁻¹.

ConditionsSmall-deformation linear single Maxwell element with constant parameters; no permanent equilibrium elasticity or large-deformation structural change.

[Figure: Maxwell series model and exponential stress relaxation](https://ml-biomat.com/tutorials/biomaterials-courses/cp12/en/#en-s2)

Figure 1 · The 1867 relaxation idea is represented by a spring and viscous element in series. At fixed total deformation the viscous element extends while the spring recoils, producing exponential stress decay. Time τ marks about 36.8% remaining stress.

At fixed total strain, the viscous element can continue extending while the spring contracts by the same amount. Stored spring stress falls at a rate proportional to its current value, producing exponential relaxation. The relaxation time is the interval for stress to fall to about 36.8% of its initial value, not a sharp time at which stress becomes exactly zero. An exponential approaches zero gradually. When an experiment regards the remaining stress as negligible depends on its signal range and resolution.

Relaxation and creep of the same modelEq. 3

![Relaxation and creep of the same model](https://ml-biomat.com/static/agent-math/e3385b37d7e181a595016644.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| G(t) | Stress divided by imposed small step strain | Pa |
| J(t) | Strain divided by imposed small step stress | Pa⁻¹ |
| G₀ | Spring or initial relaxation modulus | Pa |
| t | Time since the step | s |
| τ | Relaxation time η/G₀ | s |
| η | Viscous-element viscosity | Pa s |
| e | Base of the natural exponential | 1 |

Reading the relationshipAt fixed strain, stress loses a fixed fraction of its remaining value, giving an exponential. Fixed stress produces an immediate spring strain and continuing linear viscous deformation.

A worked exampleFor G₀=1,000 Pa, η=10⁴ Pa s and τ=10 s, G(10 s)=367.9 Pa and J(10 s)=0.002 Pa⁻¹. Their product is about 0.736, not identically one.

ConditionsTwo different ideal step experiments on the same linear Maxwell model, t≥0. Experimental loading must be sufficiently fast or included in the calculation.

The model also predicts creep. Applying stress causes an immediate spring strain followed by continued viscous deformation at constant rate. On unloading, the spring contribution recovers while accumulated viscous strain remains. One Maxwell element therefore behaves as a fluid over sufficiently long times even though it stores appreciable elastic energy over short intervals. A material with true long-time equilibrium elasticity requires a permanently load-bearing contribution. The single Maxwell element should not be made to represent that response by assigning an arbitrarily long but finite relaxation time without examining the available timescale.

The model links one well-defined timescale to experiment. It can approximate a dominant process, but a long polymer generally has many relaxation times. A pronounced relaxation tail or frequency responses incompatible with one parameter set motivates additional structurally relevant modes rather than repeated adjustment of one time constant. Model complexity should match processes that the measurements can resolve. Several mathematically convenient modes fitted to a narrow window need not identify an equal number of distinct molecular mechanisms.

An ideal step also requires experimental interpretation. A plate cannot move instantaneously. If loading time approaches the fastest relaxation times, stress can already relax while deformation is being applied. Recording the actual input and checking inertia, fixture slip and specimen edges helps separate material response from the measurement. A visually good exponential fit cannot replace knowledge of how strain was imposed. This is particularly important for soft samples, where small fixture motions can represent substantial deformation and where different loading histories can produce apparently different initial moduli.

## Separating storage and loss with oscillation

Gentle repeated shear reads the response in a reproducible oscillatory state instead of after a sudden loading event. Sinusoidal strain varies smoothly between positive and negative deformation. Angular frequency measures phase advance; it equals the number of complete cycles per second multiplied by 2π. Within linear response, stress oscillates at the same frequency but generally has a different phase. Resolving it into a part synchronous with strain and a part synchronous with strain rate defines storage and loss moduli.

Two phase components of oscillatory stressEq. 4

![Two phase components of oscillatory stress](https://ml-biomat.com/static/agent-math/96f544693a10b030eec97918.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| γ(t) | Time-dependent shear strain | 1 |
| γ₀ | Small strain amplitude | 1 |
| ω | Angular frequency, 2π times cycles per second | rad s⁻¹ |
| t | Time | s |
| σ(t) | Total steady oscillatory shear stress | Pa |
| σs(t) | Storage contribution in phase with strain | Pa |
| σl(t) | Loss contribution in phase with strain rate | Pa |
| G′ | Storage modulus at the current frequency | Pa |
| G″ | Loss modulus at the current frequency | Pa |
| sin, cos | Sine and cosine functions separated by a quarter cycle; phase ωt is in radians | 1 |

Reading the relationshipIn linear steady oscillation, stress at the same frequency resolves into sine and cosine. Strain rate is proportional to cosine, so the second component follows it.

A worked exampleFor γ₀=0.05 and G′=G″=500 Pa, phase zero gives zero strain and stress 25 Pa. At phase π/2, strain is 0.05 and stress again 25 Pa, now from storage.

ConditionsSmall-amplitude linear response after initial transients, with the displayed sine-strain phase convention.

The storage modulus characterizes response associated with energy stored and returned during a cycle; the loss modulus characterizes net cyclic loss. Both are measured in pascals because both convert strain into stress. Although connected to viscous behaviour, loss modulus is not itself viscosity. A pure spring has stress in phase with strain. A Newtonian viscous element has stress in phase with strain rate. These limits explain the decomposition, while a viscoelastic response contains both contributions at the same frequency.

Dynamic moduli of one Maxwell elementEq. 5

![Dynamic moduli of one Maxwell element](https://ml-biomat.com/static/agent-math/02a63461aca12fe86155e9f2.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| x | Product of frequency and relaxation time; not a spatial coordinate here | 1 |
| ω | Angular frequency | rad s⁻¹ |
| τ | Single relaxation time | s |
| G₀ | Elastic modulus scale | Pa |
| G′ | Storage modulus | Pa |
| G″ | Loss modulus | Pa |

Reading the relationshipInsert sinusoidal strain and the two stress components into the Maxwell relation and match sine and cosine coefficients. The product ωτ compares relaxation with oscillatory change.

A worked exampleFor G₀=1,000 Pa, ωτ=0.1 gives G′≈9.90 Pa and G″≈99.0 Pa. At ωτ=1 both equal 500 Pa; at 10 they are about 990.1 and 99.0 Pa.

ConditionsSingle linear Maxwell mode; high-frequency local glassy response, solvent background and additional modes require extra contributions.

For one Maxwell element, the decisive quantity is angular frequency times relaxation time. When this product is small, deformation is slow enough for relaxation and loss exceeds storage. When it is large, relaxation cannot keep pace and storage dominates. At a product of one the moduli are equal. This crossover belongs to the single-mode model. Broad-spectrum materials may have several crossovers or none within the measured window, so an arbitrary equality cannot always be identified with one unique material relaxation time.

[Figure: Maxwell dynamic moduli and stress-strain loop](https://ml-biomat.com/tutorials/biomaterials-courses/cp12/en/#en-s3)

One linear Maxwell element, G₀=1,000 Pa and strain amplitude γ₀=0.05. The upper graph shows frequency response for the selected relaxation time; the lower loop uses fixed axis scales and its point follows the selected phase.

Compare small ωτ, unity and large ωτ. Green is storage and orange is loss modulus; loop area corresponds to the reported per-cycle loss. Phase is controlled manually, with no autoplay.

The interaction fixes the elastic scale and small strain amplitude while varying relaxation time and frequency. It displays both moduli and the stress–strain loop. Changing phase then follows the instantaneous strain and stress around that loop. Enclosed area gives dissipated energy per volume per cycle. A spring retraces the same loading and unloading line, enclosing zero area. Loss separates those paths into a loop with finite area. This turns phase lag into an explicit energy balance and lets the numerical loss be checked against the visible response.

Stress–strain loop area per cycleEq. 6

![Stress–strain loop area per cycle](https://ml-biomat.com/static/agent-math/6d4d61ffb5d3e591856a04c1.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Wloss | Energy dissipated per volume per cycle | J m⁻³ |
| π | Circle constant, approximately 3.14159 | 1 |
| G″ | Loss modulus at the imposed frequency | Pa |
| γ₀ | Small strain amplitude | 1 |

Reading the relationshipSum stress times incremental strain around a full cycle. The storage contribution cancels and the loss contribution gives π times amplitude squared. A pascal equals a joule per cubic metre.

A worked exampleFor G″=500 Pa and γ₀=0.05, Wloss=π×500×0.0025≈3.927 J m⁻³. Halving amplitude reduces it to about 0.982 J m⁻³.

ConditionsSteady small-amplitude linear shear. Mean power additionally multiplies by cycles per second; nonlinear response requires integration of the measured loop.

A large loss modulus does not automatically imply the greatest heat generation per second. Loss per cycle also depends on strain amplitude squared, and the number of cycles per second depends on frequency. Comparing damping therefore requires amplitude, frequency and specimen volume. Raising strain amplitude from 1% to 2% quadruples loss per cycle while linear response remains valid. If larger deformation changes structure, the complete nonlinear loop must be measured rather than applying the small-amplitude formula outside its range.

A frequency sweep is thus a scan of response timescales. Slow oscillation allows adjustment; rapid oscillation leaves slower modes effectively unrelaxed within each cycle, making them mainly store energy. Frequency-dependent moduli do not mean the specimen continually changes chemical identity. They show whether its internal freedoms can respond quickly enough. Comparing these results with stress-relaxation measurements tests whether one physical account explains different loading protocols, and often reveals when a single relaxation time is too limited a description.

## Why a chain has a spectrum of relaxation times

A short bend in a long rope can be removed by adjusting a small neighbouring portion. Changing the shape of the entire rope requires coordinated motion over a larger length. A flexible molecular chain likewise changes shape on many spatial scales, while continually fluctuating under thermal motion and drag. Local modes are usually faster; modes involving long sections are slower. Different modes need not represent different chemical bonds. They can be coordinated patterns of motion involving the same set of segments.

Within linear response, adding independent Maxwell contributions produces a discrete relaxation spectrum. Each mode has a modulus weight and a relaxation time. Fast modes disappear early while slow ones generate a tail. A continuous distribution can instead be represented by an integral, which adds contributions from progressively narrower intervals. Macroscopic stress can likewise be viewed as the sum of responses left by small deformation increments throughout the past. Earlier increments have had longer to relax before the current observation.

Deformation history, relaxation spectrum and viscosityEq. 7

![Deformation history, relaxation spectrum and viscosity](https://ml-biomat.com/static/agent-math/d11527b12edec6456876947f.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| σ(t) | Current shear stress | Pa |
| K(t,t′) | Contribution density of past strain rate at t′ to current stress | Pa s⁻¹ |
| t | Current time, or waiting time in the later relations | s |
| t′ | Past time integrated over | s |
| G(t−t′) | Small-strain relaxation modulus after the indicated waiting time | Pa |
| γ̇(t′) | Strain rate at the past time | s⁻¹ |
| ∫, dt′, dt | Continuous addition over infinitesimal time intervals | Integral sign dimensionless; time increments s |
| j | Discrete relaxation-mode index | 1 |
| Gj | Nonnegative modulus weight of mode j | Pa |
| τj | Positive relaxation time of mode j | s |
| Σj | Sum over modes | 1 |
| η₀ | Steady viscosity at sufficiently low rate | Pa s |
| e | Base of the natural exponential | 1 |
| ∞ | Ideal extension to arbitrarily remote past or future | 1 |

Reading the relationshipMultiply each past strain increment by the modulus remaining after its age and sum the history. An exponential mode has time area Gjτj, so summed mode areas give zero-shear viscosity.

A worked exampleWith G₁=100 Pa, τ₁=1 s, G₂=10 Pa and τ₂=100 s, initial modulus is 110 Pa and η₀=100×1+10×100=1,100 Pa s. The weaker slow mode dominates viscosity.

ConditionsCausal linear time-translation-invariant response with initial rest or specified full history. Finite-viscosity fluid with positive modes and a convergent integral; permanent elasticity makes the infinite-time viscosity integral diverge.

The kernel in this history integral is the relaxation modulus. It specifies how much stress a small strain increment contributes after a waiting time. Material memory does not involve an active record of the past; it comes from conformations and constraints that have not yet recovered. Dividing a linear input into small increments and adding their responses predicts stress. Ageing, reaction or structural change under large deformation can make the kernel depend on more than the time difference, requiring a check of the assumed time-translation invariance.

The low-rate steady viscosity equals the area under the relaxation-modulus curve. A modest modulus persisting for a long time can add greatly to this area. A small fraction of very long chains may therefore strongly affect flow resistance while changing short-time modulus less conspicuously. Molecular-mass distribution, long branches and transient associations can all broaden the long-time tail. One mean molecular mass does not generally capture the different weights with which these structural features influence an entire rheological curve.

Inferring a relaxation spectrum from a finite frequency window is usually nonunique. Two mode sets producing nearly identical responses over that window are not distinguished by the measurements. A broader time range, comparisons among creep and relaxation, and independent molecular-mass and structural information restrict possible explanations. Fitting aims to summarize resolvable temporal structure with an adequate number of parameters and connect it to molecular mechanisms. It does not establish a new molecular motion every time a numerical spectrum displays a peak.

Modes can arise within one chain or from the multichain environment. The next steps first examine coordinated motion without significant topological constraints, then hydrodynamic coupling through solvent, and finally entangled systems whose chains cannot pass through one another. Each added physical ingredient changes drag, accessible motion or the range of coordination. Following these changes makes different molecular-mass scaling laws understandable rather than treating them as unrelated formulas that must be memorized for separate concentration regimes.

## The Rouse model: connectivity coordinates local motion

Rouse's 1953 theory of linear viscoelasticity in dilute coiling-polymer solutions divided a chain into subchains long enough to have approximately Gaussian end-to-end statistics. Coarse nodes experience local drag and thermal noise, while springs between neighbours represent conformational entropy. Each spring stands for a flexible section containing many chemical bonds, not stretching of one covalent bond. Coarse graining retains the slower motion of interest and incorporates faster local details into effective parameters such as segment length and drag.

[Figure: Low-order Rouse normal modes and their relative times](https://ml-biomat.com/tutorials/biomaterials-courses/cp12/en/#en-s5)

Figure 2 · Beads and links represent coarse nodes and Gaussian subchains. Lower curves show displacement patterns along chain index, not photographs of three physical chains. Higher modes vary more finely and have conformation times shortened approximately by p².

The simplest Rouse approximation neglects long-range dynamical coupling through fluid and the long-time topological constraints caused by chains being unable to cross. Node frictions therefore add directly. Translating the whole chain becomes harder as node count increases, reducing centre-of-mass diffusivity. Shape recovery additionally requires coordinated motion through connectivity, causing its longest time to grow more rapidly than a local node time. Normal modes resolve the coupled motions into separate patterns that each relax with their own characteristic time.

Rouse diffusion and mode timesEq. 8

![Rouse diffusion and mode times](https://ml-biomat.com/static/agent-math/4eb157dfa9b2b30b05e7e3d2.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Dcm | Whole-chain centre-of-mass diffusivity | m² s⁻¹ |
| kB | Boltzmann constant, 1.380649×10⁻²³ | J K⁻¹ |
| T | Absolute temperature | K |
| N | Effective segment or friction-node count in the large-N approximation | 1 |
| ζ | Local drag coefficient per node | N s m⁻¹ |
| b | Effective Gaussian step length | m |
| τR | Longest internal conformation-mode time | s |
| τp | Time of internal conformation mode p | s |
| p | Positive internal-mode index, in the low-order range p much smaller than N | 1 |
| π | Circle constant | 1 |

Reading the relationshipLocal drags add to Nζ. Balancing Gaussian connectivity and drag gives N² growth of internal times; normal modes give the low-order p⁻² dependence.

A worked exampleFor T=300 K, N=100, b=1 nm and ζ=10⁻¹² N s m⁻¹, Dcm≈4.14×10⁻¹¹ m² s⁻¹ and τR≈8.15×10⁻⁸ s. Mode p=2 has time about 2.04×10⁻⁸ s.

ConditionsLarge-N Gaussian unentangled chain with local drag and no long-range hydrodynamic coupling. Times describe conformation modes; particular stress correlations can have additional numerical factors.

A larger mode index represents faster variation along the chain, involving effectively shorter sections and therefore quicker relaxation. In the long-wavelength approximation, mode times decrease as the inverse square of the index. The first internal mode is slowest and describes large-scale shape recovery. Whole-chain translation is separate: it diffuses rather than relaxing toward one fixed centre-of-mass position. Measuring centre-of-mass diffusion and internal conformational relaxation independently tests whether connectivity and drag have been represented consistently.

One immediate prediction is that doubling chain length approximately halves centre-of-mass diffusivity and multiplies the longest internal time by four, provided temperature, node drag and effective segment length remain fixed. In a real chemical series, local friction can also change with molecular mass and the measurement temperature relative to glass transition. Scaling comparisons should therefore hold the material state consistent. For short chains, the Gaussian-subchain and long-wavelength approximations also need checking because too few internal units remain to support the assumed coarse description.

Although introduced for dilute solutions, neglect of hydrodynamic coupling is generally incomplete there. The Rouse model often provides a useful account of unentangled melts or scales on which relevant hydrodynamic interactions are screened. Dynamical screening differs from static excluded-volume screening. Approximately ideal chain dimensions in a melt do not eliminate all constraints from neighbouring chains or make melt dynamics identical to those of a theta solution. Static conformation and dynamical coupling must each be assessed rather than inferred automatically from one another.

The model also exposes a limit of linear theory. A Gaussian spring is mathematically extensible without bound, while a real chain has finite contour length. Strong flows that substantially extend chains require finite-extensibility effects and possibly changing friction or constraints. Linear springs are useful for small-deformation relaxation, but extending them beyond the molecular contour length removes their physical interpretation. The appropriate model depends on both the equilibrium structure and how far the experiment drives it away from that state.

## The Zimm model: coupling through the surrounding fluid

In a dilute solution, moving one segment disturbs the surrounding fluid, and that flow influences more distant segments. Even portions far apart along the molecular backbone exchange momentum through solvent, creating hydrodynamic interactions. Simply adding independent node frictions misses this collective motion. Zimm incorporated the coupling into a bead–spring description in 1956, addressing relaxation spectra relevant to dilute-solution viscoelasticity and flow birefringence. Solvent motion becomes part of the chain's dynamical coordination rather than a purely local resistance.

An order-of-magnitude picture treats large-scale coil motion as dragging a fluid region of size R. Its effective resistance grows with solvent viscosity and coil size. The time for thermal motion over a distance comparable to R consequently scales as viscosity times R cubed divided by thermal energy. This captures size dependence; coefficients depend on coil shape, size convention and the dynamical approximation. A coil cannot simply be assigned every boundary property of a solid no-slip sphere merely because both have a characteristic radius.

Size scaling of Zimm motionEq. 9

![Size scaling of Zimm motion](https://ml-biomat.com/static/agent-math/3531bcffd9af66f8b3b6144e.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| DZ | Coil diffusion scale retaining hydrodynamic coupling | m² s⁻¹ |
| τZ | Large-scale coil-relaxation time | s |
| kB | Boltzmann constant, 1.380649×10⁻²³ | J K⁻¹ |
| T | Absolute temperature | K |
| ηs | Solvent viscosity | Pa s |
| R | Consistently defined coil-size scale | m |
| ∼ | Scaling with convention-dependent coefficients omitted | 1 |

Reading the relationshipLarge-scale coil resistance grows as ηsR. Diffusing over its own size requires time of order R²/D, giving the cubic size dependence.

A worked exampleUsing unit scaling prefactors, ηs=10⁻³ Pa s, R=100 nm and T=300 K give DZ≈4.14×10⁻¹¹ m² s⁻¹ and τZ≈2.41×10⁻⁴ s. Doubling R increases time about eightfold.

ConditionsFlexible dilute coils with unscreened hydrodynamic coupling. Numbers illustrate scaling; size conventions and model coefficients must be fixed for quantitative fitting.

In a good solvent, coil size grows approximately as segment count to the power 0.588, giving a Zimm longest-time exponent about 1.764. Near theta conditions, the size exponent is approximately one half and the corresponding time exponent is three halves. Both follow from the same cubic size relation. The exponent is therefore conditional on conformation rather than a fixed numerical property of every polymer. Solvent quality sets static size, while hydrodynamic coupling translates that size into a dynamical timescale.

As concentration rises, many chains occupy the same region and the collective environment modifies solvent motion. Hydrodynamic coupling can cross over across different lengths and times. At short scales a segment may still respond to nearby solvent, while the simple dilute-solution Zimm description becomes unsuitable at larger scales. Further increases in concentration and chain length introduce significant entanglement constraints. Calling a material a solution does not select its dynamical model. Coil overlap, observation scale and solvent conditions must also be specified before assigning a scaling regime.

Scattering correlations, labelled-chain displacement and frequency response can test these descriptions. Scattering does not directly photograph every chain. It follows how concentration or conformational correlations at a selected spatial wavelength decay with time. Long wavelengths probe larger-scale motion and short wavelengths probe local changes. If one translational diffusion time cannot describe all decay scales, internal modes are contributing. Broad rheological relaxation spectra and scale-dependent scattering decay offer different views of the same hierarchy rather than competing definitions of one timescale.

Comparing Rouse and Zimm therefore asks how resistance accumulates. Rouse treats node resistance as locally additive; Zimm retains collective coupling through the fluid. Both develop statistical predictions from thermal noise, connectivity and drag, but retain different interactions. This gives molecular-mass exponents a physical origin. It also prepares the next step, where chain noncrossing changes which motions are accessible, adding a constraint that cannot be represented solely by changing solvent viscosity or replacing one local drag coefficient with another.

## How entanglements slow whole-chain relaxation

In a concentrated solution or melt of sufficiently long chains, each chain is surrounded by others. Contacts are not all permanent chemical bonds, yet chains cannot readily pass through one another. Local segments can still move, while large transverse displacement of a whole chain requires coordination with many neighbours. Representing the average topological restriction as a virtual tube gives the tube model. The tube is not a solid pore wall but an effective, time-dependent description of constraints imposed by surrounding chains.

De Gennes studied a chain moving among fixed obstacles in 1971 and developed the reptation picture: motion proceeds mainly along the chain's own curved passage, progressively withdrawing it from its original tube. Doi and Edwards connected entangled-chain dynamics to stress in concentrated polymer systems in their 1978 work. Chain ends enter new regions and erase memory of the original passage. Complete renewal takes a time that grows more strongly with chain length than unentangled conformational relaxation.

[Figure: Reptation and chain-end renewal of an effective tube](https://ml-biomat.com/tutorials/biomaterials-courses/cp12/en/#en-s7)

Figure 3 · Grey represents average topological confinement. The green chain moves along its passage and the orange end enters new space. The sketch explains tube-memory renewal; the tube is not a solid pore. Surrounding-chain motion also releases constraints in a melt.

Terminal scaling of a simple tube modelEq. 10

![Terminal scaling of a simple tube model](https://ml-biomat.com/static/agent-math/33f54d4b3892cfbb2c27844c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| τd | Terminal time to renew the original tube | s |
| τe | Time at the entanglement-strand scale | s |
| N | Effective segment count of the whole chain | 1 |
| Ne | Segment count between effective entanglement constraints | 1 |
| Dcm | Centre-of-mass diffusivity | m² s⁻¹ |
| η₀ | Zero-shear viscosity | Pa s |
| G⁰N | Rubbery plateau modulus in the intermediate-time regime | Pa |
| ∼, ∝ | Scaling and proportionality with numerical coefficients omitted | 1 |

Reading the relationshipAlong-tube drag grows with chain length and renewal of a longer passage gives a cubic time. Coil-scale displacement over that time gives N⁻² diffusion. Plateau duration times modulus sets a viscosity scale.

A worked exampleWith τe=10⁻³ s, N/Ne=10 and unit prefactor, τd=1 s. G⁰N=1,000 Pa gives η₀ of order 1,000 Pa s. Doubling chain length at fixed other conditions gives about eightfold τd and one-quarter Dcm.

ConditionsWell-entangled linear chains in simple fixed-tube reptation scaling. Constraint release, contour-length fluctuations and molecular-mass distribution modify finite-chain melt response.

The simplest fixed-tube scaling gives a terminal time proportional to chain length cubed and centre-of-mass diffusivity proportional to its inverse square. Doubling length therefore multiplies terminal time by about eight and reduces diffusivity to a quarter. In a real melt, surrounding chains also move and release constraints. Chain-end contour-length fluctuations can renew parts of the tube more quickly. These mechanisms shift effective exponents over finite molecular-mass ranges. The frequently observed viscosity exponent around 3.4 should therefore not be treated as an exact law for every entangled material.

Between completion of local motion and whole-chain escape, a material can display an approximate rubbery plateau. Plateau modulus reflects the density of effective entanglement constraints; terminal time reflects how long their memory survives. Increasing chain length primarily extends terminal relaxation and need not increase an established plateau height proportionally. A higher-molecular-mass melt can consequently have much larger viscosity with a comparatively modest change in plateau modulus. Their different molecular-mass dependences are consistent because viscosity incorporates duration as well as stress scale.

A permanently crosslinked network differs clearly from an entangled melt. Permanent connectivity supports a nonzero equilibrium shear modulus under suitable conditions. Entanglements in a linear-chain melt can eventually relax, allowing long-time flow. Long branches, rings, transient associations and mixtures of molecular masses change how constraints renew. These architectures cannot all be covered simply by inserting a different value for the same tube-escape time. Their accessible pathways and the roles of chain ends may differ qualitatively.

During processing, a long terminal time lets chains retain orientation and stress under rapid flow, influencing die swell, stretching stability and recovery across welded interfaces. Contacting polymer surfaces need chain interpenetration and cross-interface constraints to develop strength; surface contact alone does not instantly restore bulk strength. Comparing diffusion, relaxation and available processing time connects microscopic tube memory to macroscopic forming quality. It also explains why increasing molecular mass can improve some mechanical properties while making flow and interfacial healing more demanding on processing time.

## How temperature shifts the time window

Increasing temperature speeds many local segmental motions, bringing relaxations that previously required long waits into shorter observation windows. Heating and lowering observation frequency can therefore have similar effects: internal rearrangement becomes more able to keep pace with external change. Time–temperature superposition uses this connection to combine curves measured over limited instrument windows at different temperatures into a broader master curve. The method organizes time dependence rather than physically accelerating every molecular process by definition.

Its central assumption is thermorheological simplicity: relevant modes shift by approximately the same time factor while spectral shape remains similar. Segmental motion near glass transition, dissociation of temporary junctions, crystallization and phase separation may have different temperature dependences. Their combined curves may therefore resist a single horizontal shift. Overlap quality and consistency of modes must be tested rather than assuming every polymer obeys the same shifting rule. A master curve is persuasive when independent temperature ranges overlap without systematic changes of shape.

Williams, Landel and Ferry's 1955 analysis of amorphous polymers and other glass-forming liquids introduced the widely used WLF relation. A shift factor is defined here as a relaxation time at the measurement temperature divided by its value at a reference temperature. If heating accelerates relaxation, the ratio is below one. Temperature differences may be measured in kelvin or Celsius increments, provided coefficients and differences use consistent units. Absolute temperatures remain explicitly defined, and shifting conventions must be stated before comparing reported factors.

WLF temperature shift relationEq. 11

![WLF temperature shift relation](https://ml-biomat.com/static/agent-math/d33eb8ecdc009f59a7cb1e30.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| aT | Relaxation-time ratio relative to the reference temperature | 1 |
| τ(T) | Relaxation time of a corresponding mode at T | s |
| τ(Tr) | Time of the same mode at reference temperature | s |
| T | Measurement absolute temperature | K |
| Tr | Reference absolute temperature | K |
| C₁ | Fitted constant for this material and reference temperature | 1 |
| C₂ | Fitted constant with temperature-difference units | K |
| log₁₀ | Base-ten logarithm, with −1 corresponding to value0.1 | 1 |

Reading the relationshipAn empirical rational form describes strong temperature dependence beyond a single Arrhenius slope; logarithmic time ratios represent many orders of magnitude.

A worked exampleFor example fitted values C₁=10, C₂=90 K, Tr=300 K and T=310 K, log₁₀aT=−100/100=−1, so aT=0.1 and corresponding relaxation is ten times faster.

ConditionsValidated temperature interval in a thermorheologically simple state. Constants depend on material and reference temperature; do not extrapolate across structural changes or the denominator singularity.

A shift factor of 0.01 means the corresponding process takes one hundredth of its reference-temperature time. At a fixed experimental angular frequency, it corresponds to a lower effective reference frequency. Multiplying the frequency axis by this shift factor implements the stated convention. Modulus may also require a modest vertical correction involving density and temperature, so horizontal and vertical procedures should both be reported. Changing reference temperature changes the WLF constants; a familiar numerical pair is not a universal constant for all materials and reference choices.

[Figure: Frequency-axis shift direction for thermorheologically simple response](https://ml-biomat.com/tutorials/biomaterials-courses/cp12/en/#en-s8)

Figure 4 · Heating shortens relaxation, moving the same modulus feature to higher measured frequency. With aT=τ(T)/τ(Tr), heating gives aT<1 and multiplication of frequency by aT shifts the data left toward the reference. Only horizontal shifting is illustrated.

Near glass transition, a small temperature change can shift relaxation by many orders of magnitude. Room-temperature stiffness can consequently be sensitive to formulation, plasticizer and water content. Water changes solvent conditions and can alter local motion and associations, so dry and hydrated samples cannot automatically be related by one temperature correction. In semicrystalline or reacting materials, heating may change the structure itself. Thermal history and kinetic shifting must then be tracked separately to avoid combining different states as if only their clocks had changed.

A validated master curve extends the measurement window as a conditional prediction tool. Responses at service times much longer than routine experiments may be estimated using established superposition. If modes reorganize or degradation occurs across the temperature interval, the state correspondence must be rebuilt. Combining the master curve with independent temperature measurements, molecular structure and morphology helps identify which material state the extended prediction describes. The method gains practical value from these checks because they connect shifted laboratory data to the actual conditions under which the material must operate.

## Using molecular timescales in flow and processing

Whether a chain recovers during flow depends on competition between relaxation and imposed deformation. Slow changes allow it to remain near a relaxed state under the current conditions. Rapid sustained deformation accumulates orientation and stretch. Multiplying a relaxation time by shear rate gives a dimensionless comparison of these rates. Dividing relaxation time by the overall observation time describes another competition. The two can be related in suitable protocols, but they use different definitions of the external timescale and should not be treated as identical labels.

Comparing relaxation with imposed deformationEq. 12

![Comparing relaxation with imposed deformation](https://ml-biomat.com/static/agent-math/d20651f034ed1cdd4b1913a8.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Wi | Weissenberg number comparing shear rate with relaxation | 1 |
| De | Deborah number comparing relaxation with observation duration | 1 |
| γ̇ | Shear rate, using its magnitude to compare intensity | s⁻¹ |
| τ | Relaxation time of the selected relevant mode | s |
| tobs | Observation or imposed process timescale | s |

Reading the relationshipRate times time and time divided by time eliminate units, giving two different timescale comparisons. The selected mode and external process must be specified.

A worked exampleFor τ=10 s and shear rate0.2 s⁻¹, Wi=2. Observing for100 s gives De=0.1. Wi can be large while De is small because the external times being compared differ.

ConditionsOrder-of-magnitude indicators for specified flow and modes. Multiple modes, multistage processes and large deformation require fuller constitutive descriptions; no one universal critical value applies.

Many polymer liquids display an approximately constant zero-shear viscosity at low rates. At higher rates, chain orientation and constraint rearrangement can lower apparent viscosity, producing shear thinning. Extensional flow can instead generate strong tensile stress as chains stretch. Shear thinning does not necessarily mean molecular scission: after flow stops, structure can often partly or fully recover. Actual degradation requires independent molecular-mass or chemical evidence. Different flows rotate and stretch chains differently, so one shear-viscosity value cannot predict every processing operation.

A large dimensionless rate suggests that linear approximations may be inadequate, but is not one universal exact breakdown threshold. Multiple relaxation times mean different modes cease keeping pace at different rates. Deformation amplitude, flow type and finite chain length also matter. In particular, small-amplitude high-frequency oscillation can remain linear even when frequency times relaxation time is large, because the excursion remains small. Sustained deformation in steady shear is a different driving history. The longest time provides a useful first estimate; a fuller prediction needs a constitutive relation linking stress to deformation history, orientation, stretch and constraint renewal. Its chosen structural variables should correspond to mechanisms active in the material and flow being studied.

Experimental interpretation must also distinguish intrinsic response from inhomogeneous flow. Wall slip makes the imposed motion differ from deformation inside the sample. Edge fracture changes effective loaded area. Viscous heating can lower local viscosity. Observing flow and specimen edges, varying the gap and controlling temperature help determine whether a falling viscosity curve reflects molecular rearrangement or measurement conditions. Instrument sensitivity and inertia can additionally limit the usable low- and high-frequency ends for soft specimens. These checks establish the window in which molecular interpretation is justified.

For a practical material, first measure relaxation or oscillatory response at fixed temperature and small amplitude to identify resolvable timescales. Combine these with molecular mass, concentration and structure to determine where Rouse motion, Zimm coupling or entanglement constraints apply. Then compare those times with processing rate, waiting periods and cooling. This defines concrete prediction targets: how much stress survives during flow, how long recovery takes after stopping, and when chain motion can establish connections across an interface.

Long-chain dynamics is not obtained by simply enlarging a small molecule's diffusion time. Connectivity creates coordinated modes, fluid coupling changes how resistance accumulates, and topology delays complete renewal. Macroscopic rheology converts these levels into measurable stress, strain, storage and dissipation. Understanding that correspondence explains why longer chains, higher temperature or faster processing can have different consequences under different conditions. It also makes model selection a physical decision about active mechanisms and observation scales rather than a choice based solely on a material's name.
