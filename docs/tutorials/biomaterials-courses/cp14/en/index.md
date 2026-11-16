# How Patterns Emerge: Instability and Length-Scale Selection

Source: https://ml-biomat.com/tutorials/biomaterials-courses/cp14/en/
Language: en

A uniform polymer solution can develop connected domains, a flat film can open holes, and two blocks of one chain can organize into nanoscale stripes. Follow the amplification of small fluctuations, competition between length scales and eventual retention of structure to understand why patterns emerge and how processing changes them.

## A pattern describes how material is distributed

To make a porous membrane, one can begin with a uniform polymer solution and then change temperature or the surrounding solvent. Polymer-rich and polymer-poor regions may subsequently become walls and channels. A transparent coating often needs to avoid this same segregation because refractive-index differences scatter light. Whether a pattern is useful therefore depends on its function. Connected pores support transport, a continuous dense layer supports a barrier, and regular nanoscale domains can guide later fabrication. The first scientific question is which physical quantity varies across the sample, rather than whether the image looks attractive or complicated.

For a binary mixture, divide the volume occupied by component A in a small region by that region's total volume. The result is a volume fraction between zero and one. A constant value everywhere describes uniform composition; slightly higher and lower values describe a concentration fluctuation. The averaging region must contain enough molecules to have a smooth concentration, yet remain small enough to resolve the structure of interest. Film thickness is another possible varying quantity. A film may have identical chemistry everywhere while material flows from thinner places to thicker ones. Similar dark and light patches in images can consequently reflect quite different physical variables.

An external groove can impose a pattern, while a nearly uniform sample can also develop one without a prewritten template. Such spontaneous development still needs a seed. Thermal motion, tiny thickness variations and imperfect boundaries all provide disturbances. What matters is whether a disturbance disappears or grows. A small displacement of a ball from the bottom of a bowl is restored, whereas displacement from a local summit increases. Material stability has a related meaning, with an additional constraint: concentration cannot increase everywhere without bringing in matter. Enrichment must be accompanied by depletion elsewhere. This conservation requirement changes which spatial variations can develop rapidly.

Length-scale selection contains three distinct questions. The fastest-growing wavelength determines the spacing most readily visible at an early stage. Domain merger and interface motion may then increase that spacing. A competing effect from chain connectivity, surfaces, elasticity or sustained driving can finally support a persistent finite scale. Naming the spacing in the first clear photograph an equilibrium period skips the second and third questions. In processing, the retained structure can instead be the one present when cooling slows motion dramatically. Its interpretation requires both a time for structure to evolve and a time at which that evolution becomes experimentally inaccessible.

We will follow a binary polymer mixture through free energy, matter conservation and spatial fluctuations before comparing block copolymers and reaction–diffusion systems. This route makes it possible to explain why a small variation grows while recognizing that stripes and spots need not share one origin. Space in these models means actual positions in a specimen, and wavelengths can be extracted from microscopy or scattering. The purpose of the equations is to connect a measurable spacing and growth rate to material properties. A useful model also identifies the stage of evolution during which that connection applies, so that early amplification, later coarsening and final retention remain experimentally distinguishable.

## Why free-energy curvature controls a fluctuation

At a specified temperature, a mixture's free energy combines the energetic consequences of molecular contacts with the number of accessible arrangements. Imagine equal small boxes, each internally uniform, and draw the free-energy density as a function of their composition. The height of the curve gives a state's cost. Its slope describes the change produced by a small composition adjustment. Its curvature describes how that slope changes. A derivative formalizes a change divided by a very small input interval, taken locally; a second derivative applies the same operation to the slope. These ideas make stability a quantitative question rather than a visual impression.

Start with two boxes at the same composition and transfer a small amount of A from one to the other. Their volume fractions increase and decrease by equal amounts, preserving the total. The first-order free-energy changes cancel. The leading remaining contribution depends on curvature and the square of the composition change. Positive curvature makes the pair more costly, resisting a small separation. Negative curvature lowers its combined free energy and creates a tendency for the variation to grow. This is the local thermodynamic condition inside a spinodal region. The historical term spinodal does not refer to the turning of electron spins in this application.

Positive curvature can also occur where a sufficiently large separation into two phases would eventually lower free energy. Small disturbances then decay, but a large enough region of a new phase can overcome the cost of its interface and grow. This is nucleation, a different route from immediate amplification of small fluctuations in the negative-curvature region. A curvature test asks about local stability. A common tangent to the full free-energy curve identifies equilibrium coexisting compositions. Local resistance to small changes therefore needs to be distinguished from having the lowest possible free energy among all compositions and combinations of phases available to the specimen.

Differences between neighboring boxes also carry an interfacial cost. If a fixed composition difference occurs across a shorter distance, the spatial gradient becomes larger and molecular surroundings change more abruptly. In their 1958 treatment of nonuniform systems, Cahn and Hilliard systematically incorporated a gradient contribution so that interface width followed from an energetic competition. The expression below uses volume fraction and free energy per unit volume. Integration adds contributions from small volume elements. Squaring the gradient ensures that reversing the direction of a composition variation does not turn an interfacial penalty into an energetic reward.

Free energy of a nonuniform mixtureEq. 1

![Free energy of a nonuniform mixture](https://ml-biomat.com/static/agent-math/61f159650ae99118aa714ae4.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| F | Total specimen free energy | J |
| ψ | Free-energy density including local and gradient contributions | J m⁻³ |
| V,dV | Specimen volume and infinitesimal volume element | m³ |
| ∫V | Volume integral adding local contributions | 1 |
| φ | Local volume fraction of component A | 1 |
| f(φ) | Homogeneous free-energy density at composition φ | J m⁻³ |
| κ | Positive composition-gradient coefficient | J m⁻¹ |
| ∇φ | Spatial gradient of volume fraction | m⁻¹ |
| \|∇φ\|² | Sum of squared gradient components | m⁻² |

Reading the relationshipAdd local composition cost and the penalty for spatial variation. A positive squared-gradient contribution penalizes sharp transitions; integration converts density to total energy.

A worked exampleWith κ=10⁻¹¹ J m⁻¹ and gradient magnitude 10⁶ m⁻¹, the gradient energy density is 5 J m⁻³. Uniformly occupying 10⁻¹² m³, it contributes 5×10⁻¹² J.

ConditionsIsothermal binary mixture with a smooth concentration field and constant isotropic κ; surface preference, elasticity and external fields require additional terms.

[Figure: Two widths for the same composition transition](https://ml-biomat.com/tutorials/biomaterials-courses/cp14/en/#en-s2)

Figure 1 · Original model diagram illustrating the Cahn–Hilliard gradient-energy idea. Position is horizontal and volume fraction vertical; both profiles connect the same endpoints. Broadening reduces gradient cost but places more material at intermediate compositions, so both contributions set interface width.

The expression combines two tendencies. Local free energy may favor enrichment and depletion, whereas a positive gradient coefficient resists rapid spatial changes. Subdivision into ever finer regions is consequently not automatically favorable: finer regions bring more interfaces or larger gradients. An interface becomes a finite transition rather than an infinitely thin mathematical cut. A smooth concentration curve describes an average over many molecules within that transition, not the boundary of an individual molecule. This interpretation also fixes the model's resolution. If a proposed pattern approaches molecular dimensions, a continuum gradient expansion needs reassessment, even when the same algebra still produces a numerical answer.

## Moving matter down a free-energy gradient

Free energy alone does not say how rapidly a pattern appears. We also need a law for movement. Imagine exchanging a small amount of the components between neighboring positions while preserving total volume. The sensitivity of free energy to that local composition adjustment defines the potential driving exchange. Here μ is a composition-conjugate potential per reference volume, measured in joules per cubic metre. Its normalization differs from a chemical potential quoted per mole. Parameters must use the same convention throughout a calculation. The local contribution is the free-energy slope, while the gradient contribution makes the neighboring concentration profile relevant to the driving force.

Composition-conjugate potential per reference volumeEq. 2

![Composition-conjugate potential per reference volume](https://ml-biomat.com/static/agent-math/1e17bb454068f67161b2d821.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| μ | Potential density conjugate to local composition change | J m⁻³ |
| f′(φ) | First derivative of free-energy density with respect to dimensionless volume fraction | J m⁻³ |
| φ | Local volume fraction | 1 |
| κ | Constant gradient-energy coefficient | J m⁻¹ |
| ∇²φ | Sum of second spatial derivatives | m⁻² |

Reading the relationshipA small composition variation gives f′ from the local term; spatial integration by parts gives −κ∇²φ from the gradient term, with boundary conditions removing the extra boundary contribution.

A worked exampleIf f′=2 J m⁻³, κ=10⁻¹¹ J m⁻¹ and ∇²φ=−10¹¹ m⁻², then μ=2−(−1)=3 J m⁻³. Peak-like curvature raises the local potential.

ConditionsUses the volume normalization of E1; μ is not a molar chemical potential. Constant κ and periodic or appropriate natural boundary conditions.

The Laplacian in this expression is easiest to understand in one dimension. It is the second spatial derivative, indicating whether a point resembles the top of a peak or the bottom of a valley relative to nearby positions. In several dimensions, add second derivatives along each coordinate direction. A straight ramp has a gradient but no local curvature, whereas a concentration maximum has a negative second derivative. The interfacial contribution therefore depends on more than the concentration at one isolated point. This influence of the surrounding profile follows from the energetic connection between adjacent regions in the gradient term.

Composition flux measures the volume of a component passing through unit area per unit time, giving units of metres per second. Choose it opposite to the potential gradient and multiply by a positive mobility to obtain a linear dissipative transport law. Next balance a small box: concentration rises if inflow exceeds outflow, and falls in the opposite case. Combining this conservation statement with the potential gives the concentration evolution commonly called the Cahn–Hilliard equation. It can describe transport from lower to higher concentration because the potential gradient, rather than concentration gradient alone, determines the direction of movement under these conditions.

Conserved dissipative transportEq. 3

![Conserved dissipative transport](https://ml-biomat.com/static/agent-math/c4be1ae218b5b114c1c25ba0.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| 𝐉φ | Component-volume flux vector | m s⁻¹ |
| M | Positive composition mobility | m⁵ J⁻¹ s⁻¹ |
| μ | Composition-conjugate potential density | J m⁻³ |
| ∇μ | Spatial potential gradient | J m⁻⁴ |
| φ | Local volume fraction | 1 |
| t | Time | s |
| ∂φ/∂t | Time rate of volume fraction at fixed position | s⁻¹ |
| ∇· | Divergence measuring net outward flow per volume | m⁻¹ |

Reading the relationshipFlux points down the potential gradient. Concentration growth equals inflow minus outflow, so enrichment has a corresponding source of matter.

A worked exampleIn one dimension, M=10⁻¹⁵ m⁵ J⁻¹ s⁻¹ and ∂μ/∂x=10⁶ J m⁻⁴ give Jφ=−10⁻⁹ m s⁻¹, directed toward decreasing x.

ConditionsIsothermal dissipative composition model without bulk advection or reaction. M may vary spatially; the later linear-growth calculation takes it constant.

With closed or periodic boundaries, material leaving one location enters another and the mean composition stays constant. Substituting the evolution law into the rate of change of free energy gives the dissipation relation below. Its right-hand side is minus an integral of positive mobility times a squared gradient, so it cannot be positive. At fixed temperature without external driving, this model uses the free energy available for rearrangement. An increasingly visible pattern can therefore accompany a continuously decreasing free energy. Spatial uniformity is not always the minimum-free-energy state, and visual complexity is not a direct measure of thermodynamic cost.

Free-energy dissipation in a closed systemEq. 4

![Free-energy dissipation in a closed system](https://ml-biomat.com/static/agent-math/a98b7487933e4ef1499b79c8.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| dF/dt | Time rate of total free energy | J s⁻¹ |
| F | Total free energy | J |
| t | Time | s |
| M | Positive mobility | m⁵ J⁻¹ s⁻¹ |
| ∇μ | Spatial composition-potential gradient | J m⁻⁴ |
| \|∇μ\|² | Squared gradient magnitude | J² m⁻⁸ |
| ∫V,dV | Integrate over specimen volume | Integral sign: 1; dV: m³ |
| ≤ | Less than or equal to | 1 |

Reading the relationshipSubstitute conserved dynamics into the free-energy rate and integrate by parts. Closed or periodic boundaries remove boundary terms, leaving a negative square.

A worked exampleFor uniform M=10⁻¹⁵ and |∇μ|=10⁶ in the units listed, over volume 10⁻¹² m³, dF/dt=−10⁻¹⁵ J s⁻¹.

ConditionsFixed temperature, closed or periodic boundaries, no external work input, using E1–E3 with compatible natural boundary conditions.

In polymers, mobility depends on chain length, entanglements, local composition and temperature. A constant mobility first isolates the competition between stability and spatial scale. In an actual specimen, a polymer-rich region may become very viscous and substantially slow further rearrangement. Bulk fluid motion can also transport the concentration field, requiring an advective term in the conservation law. These additions preserve the need for matter balance while changing growth rates and later structures. The relevant observation time and flow conditions should therefore be part of a model's physical definition, along with its free-energy parameters, when connecting the calculation to a particular experiment.

## Selecting the wavelength that grows first

Representing a smooth concentration profile as a combination of waves is a useful way to study its early evolution. A cosine wave has regularly spaced enriched peaks and depleted valleys. Its positive and negative parts average to zero, so adding it to uniform composition preserves the mean. Wavelength is the distance between adjacent peaks. Wavenumber describes how rapidly the wave's phase changes with position. Across one wavelength the phase advances by a complete turn, or 2π radians, making wavenumber equal to 2π divided by wavelength. A large wavenumber describes fine variation; a small one describes broad variation.

For a small fluctuation, expand the local free-energy curve around the initial composition and retain terms linear in amplitude in the evolution law. Different waves then grow or decay independently for a time, each amplitude acquiring an exponential factor. Positive growth rate amplifies a wave, while negative rate suppresses it. Substitution of a cosine into the evolution law is particularly simple: each pair of spatial derivatives introduces minus the wavenumber squared. This gives the growth-rate expression below without first solving an entire irregular concentration pattern. The calculation asks which existing small disturbance has the strongest initial amplification.

Growth rate of a small concentration waveEq. 5

![Growth rate of a small concentration wave](https://ml-biomat.com/static/agent-math/449c141fd0d1ca698eb382c9.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| δφ | Small volume-fraction departure from the initial uniform state | 1 |
| A₀ | Initial amplitude | 1 |
| e^{ωt} | Exponential time factor with natural base e | 1 |
| ω | Exponential amplitude growth rate, possibly negative | s⁻¹ |
| t | Time | s |
| cos | Cosine with phase in radians | 1 |
| q | Spatial wavenumber | m⁻¹ |
| x | Position coordinate | m |
| M | Constant mobility | m⁵ J⁻¹ s⁻¹ |
| a | Free-energy-density curvature at initial composition | J m⁻³ |
| f″ | Second derivative with respect to volume fraction | J m⁻³ |
| φ₀ | Initial mean volume fraction | 1 |
| κ | Gradient-energy coefficient | J m⁻¹ |
| ℓ | Wavelength | m |
| π | Circle constant | 1 |

Reading the relationshipLinearization relates potential fluctuations to curvature and the gradient term. Each pair of spatial derivatives of cosine gives −q², with conserved dynamics supplying an additional q².

A worked exampleIn normalized units, M=1, a=−1, κ=1 and q=0.5 give ω=0.1875. Initial amplitude 0.005 becomes 0.005e^0.375≈0.007275 at t=2.

ConditionsSmall fluctuations, constant coefficients, no flow and one x-directed mode. Reference length, time and energy-density scales have been divided out in the normalized example.

With positive free-energy curvature, every nonzero wavenumber decays. Negative curvature allows a band of lower wavenumbers to grow, while sufficiently short waves remain suppressed by the gradient penalty. Extremely long waves pay little gradient energy, but matter must redistribute over a long distance. Conserved dynamics makes their growth slow. The fastest-growing wavelength lies between these limits, neither too sharp nor too broad. Zero wavenumber would change the average composition rather than make an alternating pattern. Its growth rate is exactly zero in this closed-system model, expressing conservation in the language of spatial waves.

Unstable band and fastest early scaleEq. 6

![Unstable band and fastest early scale](https://ml-biomat.com/static/agent-math/ef508809ca0f3884ffbec405.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| qc | Upper edge of the unstable wavenumber band | m⁻¹ |
| q* | Fastest-growing continuum wavenumber | m⁻¹ |
| ℓ* | Corresponding wavelength | m |
| a | Negative initial free-energy curvature | J m⁻³ |
| κ | Positive gradient-energy coefficient | J m⁻¹ |
| √ | Positive square root | 1 |
| π | Circle constant | 1 |

Reading the relationshipZero growth gives the band edge. Differentiating growth rate with respect to wavenumber and taking its positive maximum gives the fastest mode.

A worked exampleFor a=−10³ J m⁻³ and κ=10⁻¹¹ J m⁻¹, qc=10⁷ m⁻¹, q*=7.071×10⁶ m⁻¹ and ℓ*≈0.889 μm.

ConditionsRequires a<0, κ>0 and M>0 in early linear continuum dynamics. Growth occurs for 0<q<qc, with neutral edges; finite samples require allowed discrete modes.

[Figure: Comparison of long, intermediate and short waves](https://ml-biomat.com/tutorials/biomaterials-courses/cp14/en/#en-s4)

Figure 2 · Concentration varies along the horizontal direction. Conserved transport slows long waves, gradient energy suppresses short waves, and an intermediate wave can grow fastest. Equal drawn amplitudes isolate wavelength; actual rates depend on curvature, mobility and gradient coefficient.

The interactive model below divides length, time and free-energy density by fixed reference quantities, so the displayed parameters are dimensionless. It keeps the same linear growth equation and a deliberately small initial amplitude. Change curvature to create or remove the unstable band, change the gradient coefficient to move the preferred wavelength, and choose individual spatial modes to compare their amplitudes. The time control shows early linear evolution without saturation or coarsening. Mean composition is 0.5, and each allowed mode fits an integer number of complete waves into a periodic domain of length 20. The small-amplitude range keeps the interpretation consistent.

All parameters use fixed reference scales; mean composition 0.5, domain length 20, initial amplitude 0.005.

[Figure: Growth-rate spectrum and selected concentration wave](https://ml-biomat.com/tutorials/biomaterials-courses/cp14/en/#en-s4)

The upper vertical axis is fixed from −1 to 1.3; more negative rates lie below it and remain available in the feedback. Grey is the initial wave and green the current wave. No autoplay.

Change curvature and gradient cost to compare the continuum optimum with modes allowed in a finite domain. This interaction shows small-amplitude linear growth, with amplitude below approximately 0.048; it does not simulate later coarsening.

The continuum optimum need not fit exactly inside a finite sample. A periodic domain permits only discrete wavenumbers, so their actual growth rates must be compared to identify the fastest allowed mode. Fixed-composition or preferential boundaries change the allowed profiles again. This distinction explains how the observed spacing in a small specimen can jump between possibilities even when the continuum optimum varies smoothly. Once amplitudes become large, the free-energy curvature cannot remain fixed at its initial value and waves begin to interact. Full nonlinear evolution then replaces the independent-wave approximation. Extending the exponential expression to negative concentration or volume fraction above one would exceed its physical range rather than predict a new material state.

The fastest-growing mode is not necessarily the first to become visible. A surface defect may initially excite another mode strongly enough that it reaches the microscope's detection threshold earlier despite its lower growth rate. Comparing changes at several times separates initial amplitude from amplification rate. Thermal fluctuations generally contain many scales, whereas an imposed striped template can favor a particular one. A template therefore influences orientation and the starting point of competition without necessarily changing the material's own free-energy curvature. Both the initial profile and its time-dependent evolution are needed to distinguish these effects.

## Why early patterns coarsen or retain a finite scale

As concentration fluctuations become large, enriched and depleted regions approach their respective phase compositions, with narrower transition layers between them. A further route to lower free energy is to reduce total interfacial area. Small regions can disappear, larger regions can grow, and neighboring regions can merge after contact. Their characteristic size then increases with time, a process called coarsening. This does not require the two components to mix again. It may proceed while the compositions within both phases are already fairly well established. Composition inside a domain and distance between domains are separate observables and can evolve on different time scales.

For sparse droplets, a smaller droplet has greater curvature, and the interface can raise the potential for exchange of its material. Transfer through the surrounding continuous phase then feeds larger droplets, providing one ripening mechanism. Motion that brings droplets into contact and lets them fuse provides another. A connected, bicontinuous structure can also change through interface-driven fluid flow. These mechanisms involve different transport distances, resistances and geometries. A time power law from one idealized model cannot therefore be assigned to every polymer separation image. Identifying the operative mechanism requires observations of structural change together with the conditions controlling transport and motion.

Slow polymer dynamics makes apparent cessation of change particularly important to interpret carefully. On cooling, an enriched phase may vitrify; an entangled network or crystalline region may also restrict rearrangement. Such processes preserve an existing structure without necessarily making its spacing an equilibrium period. If modest reheating restarts domain growth, the earlier arrest had a kinetic contribution. Conversely, convergence from different initial patterns toward a similar period, followed by recovery after disturbances, supports a finite scale maintained by thermodynamic competition. Because experiments observe a finite time window, temperature and waiting-time histories form part of the physical description of a retained pattern.

Block copolymers provide a clear mechanism for a finite equilibrium scale. A and B blocks are covalently connected within each molecule. Unfavorable contacts promote local separation, while connectivity makes macroscopic separation require excessive chain extension. For a simplified lamellar structure, increasing the period reduces interfacial cost per chain but increases stretching cost. The model below represents these contributions as an inverse period and a squared period, respectively. Its coefficients collect effects of composition, interfacial tension and chain statistics. It explains a competition in scale; a complete morphology diagram must additionally compare geometries such as spheres, cylinders and layers, with their different packing constraints.

Period selection by interface and chain stretchingEq. 7

![Period selection by interface and chain stretching](https://ml-biomat.com/static/agent-math/b4c4e0b0149119c5323307d7.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Fc | Scale-dependent free energy per chain | J |
| d | Lamellar period | m |
| As | Positive interfacial-cost coefficient | J m |
| Bs | Positive stretching-cost coefficient | J m⁻² |
| d* | Energy-minimizing period in this scale model | m |
| 1/3 | Cube-root power | 1 |

Reading the relationshipLarger period decreases interfacial cost and increases stretching cost. Setting the derivative −As/d²+2Bsd to zero balances their slopes.

A worked exampleAs=2×10⁻²⁹ J m and Bs=10⁻⁵ J m⁻² give d*=10 nm. The contributions are 2×10⁻²¹ and 10⁻²¹ J, totaling 3×10⁻²¹ J per chain.

ConditionsIllustrative scale model at fixed composition and lamellar geometry, positive coefficients and applicable stretching approximation; a full block-copolymer phase diagram requires more detail.

[Figure: Ordinary coarsening and finite-period connected blocks](https://ml-biomat.com/tutorials/biomaterials-courses/cp14/en/#en-s5)

Figure 3 · Upper rows illustrate coarsening with time. Below, white lines indicate connections between unlike blocks across interfaces. Lamellar geometry isolates the scale competition; ordinary blends can also form droplets or bicontinuous structures.

The preferred period follows when the slopes of the two energetic contributions cancel. It is not an independently chosen attractive spacing. Increasing the interfacial penalty favors a larger period, while increasing the stretching penalty favors a smaller one. This balance differs both from the fastest early wavelength in an ordinary blend and from a spacing retained by vitrification. All three situations may occur sequentially during processing: an early scale develops, the structure adjusts toward another scale, and arrested motion preserves some remaining defects and incomplete relaxation. The final micrograph therefore records both the available energetic competition and the route by which the sample reached its present state.

Structures with similar spacing may have very different connectivity. The continuous phase around isolated droplets can span the sample, whereas a bicontinuous morphology can provide spanning paths in both phases. If transport must occur through an enriched phase, isolated droplets and continuous channels have different consequences. Changing composition often changes interface area, curvature and connectivity together, so a target mean pore size is only part of the design. Combining spacing measurements with three-dimensional connectivity or permeability measurements connects a selected structural scale to its intended transport function.

## How diffusion can participate in pattern formation

Diffusion is often understood as removing differences: a drop of dye spreads and its concentration peak flattens. For one stable concentration field, this is a useful picture. If two substances influence one another's production and consumption, however, diffusion also changes how their feedback operates at different positions. In his 1952 investigation of chemical morphogenesis, Turing identified the possibility that a uniform reacting state could resist a spatially uniform disturbance yet become unstable to particular spatial wavelengths when diffusion rates differ. The stability change belongs to the combined reaction and transport system, rather than to diffusion considered in isolation.

Imagine a local change that reinforces itself while also promoting a suppressing influence. Suppression then acts back on the original change. If the suppressing influence spreads farther, competition near a peak differs from competition at more distant locations and may leave a finite spacing. Local reinforcement and longer-range suppression provide a useful mental picture, although actual reaction networks do not always separate into one simple activator and one inhibitor. Establishing this instability in a specific system still requires the responses of reaction rates to concentration and the relevant diffusion coefficients. The labels alone cannot determine whether a growing spatial mode exists.

[Figure: Coupled reaction feedback and unequal spreading scales](https://ml-biomat.com/tutorials/biomaterials-courses/cp14/en/#en-s6)

Figure 4 · Upper arrows show cross-feedback in the example: u promotes v and v suppresses u. Lower profiles illustrate different spreading scales over the same time, with position horizontal. Full stability also depends on self-response terms; unequal widths alone do not establish pattern formation.

To calculate how transport changes feedback, let u and v be small departures of two concentrations from a uniform steady state, each divided by a reference concentration to make it dimensionless. A departure can be negative while the actual concentration remains positive. Linearizing reaction rates near the steady state gives four coefficients describing how each departure affects its own rate of change and that of the other variable. Adding ordinary diffusion produces the equations below. They describe the initial perturbation stage. Complete chemical kinetics must also provide the later nonlinear saturation and the physical details of material supply and removal.

Reaction feedback with unequal diffusion ratesEq. 8

![Reaction feedback with unequal diffusion rates](https://ml-biomat.com/static/agent-math/9d810056c58c4066e49c5292.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| u,v | Normalized small concentration departures from a uniform steady state | 1 |
| ∂t | Partial time derivative at fixed position | s⁻¹ |
| a,b,c,d | Linear reaction-response coefficients; d here is not a period | s⁻¹ |
| Du,Dv | Positive diffusivities of the two substances | m² s⁻¹ |
| ∇² | Sum of second spatial derivatives | m⁻² |

Reading the relationshipRetain the linear reaction response to small departures and add ordinary diffusion. A common exponential spatial-wave mode replaces the Laplacian by minus wavenumber squared.

A worked exampleFor a=1,b=−2,c=2,d=−3 s⁻¹, homogeneous growth has a repeated root −1 s⁻¹. With Du=1,Dv=20 μm² s⁻¹ and q=0.5 μm⁻¹, self-coefficients become 0.75 and −8 s⁻¹. Growth rate σ obeys σ²+(7.25 s⁻¹)σ−2 s⁻²=0, with positive root 0.2661 s⁻¹.

ConditionsSmall departures near a uniform reacting steady state, constant coefficients and no cross-diffusion. Signed u and v are departures from positive concentrations, not a complete saturating reaction model.

Choose a=1, b=−2, c=2 and d=−3, all in inverse seconds. Without spatial variation, both coupled growth rates equal −1 per second, so small disturbances eventually decay. Next choose diffusion coefficients of 1 and 20 square micrometres per second. For wavenumber 0.5 per micrometre, diffusion reduces the two self-response coefficients to 0.75 and −8 per second while leaving cross-coupling unchanged. Substituting a common exponential time factor gives a quadratic equation for growth rate, with one root approximately positive 0.266 per second. Spatial transport has changed the balance of feedback enough to create a growing mode around the formerly stable uniform state.

Each diffusion term in this example still smooths its own concentration field. Growth arises from the coupled system; diffusion does not independently carry either component up its concentration gradient. If the two diffusivities were identical, their effect on any spatial wave would be a common negative shift of all reaction growth rates. Diffusion could not generate this two-variable linear instability from a stable reaction state. Sustained chemical patterns also require appropriate reaction conditions and supplies of matter or energy. Passive polymer demixing can proceed while free energy decreases, so a visual resemblance between its spots and a chemical pattern does not establish a Turing mechanism. The required feedback and transport measurements supply the distinction.

## How boundaries, defects and processing select the outcome

An early linear calculation identifies competing wavelengths but does not uniquely determine a complete final pattern. As amplitude grows, local concentrations must stay inside their physically allowed range and different waves cease to evolve independently. Growth of one mode changes the environment experienced by others. Stripe orientation, connectivity and defects must also adjust. Nonlinear competition and geometrical organization therefore intervene between the fastest-growing wavenumber and a real two- or three-dimensional morphology. The mode that grows first may influence subsequent development, but it can also be replaced while the sample reorganizes toward another arrangement compatible with its constraints.

Consider the amplitude of one selected mode. Adding a suppressing contribution proportional to its cube gives a simple example of saturation. At small amplitude the linear growth term dominates. At larger amplitude the cubic contribution catches up, leaving a finite steady amplitude. Preserving positive–negative symmetry is useful because interchanging the peaks and valleys of a wave corresponds to changing phase and should not arbitrarily change its growth law in this symmetric example. Such an amplitude equation explains the logic of saturation. It describes an already selected mode, however, and does not by itself choose every possible wavelength or remove the defects of a spatial pattern.

Saturation of a selected modeEq. 9

![Saturation of a selected mode](https://ml-biomat.com/static/agent-math/7f5e377feba33abe432ba6ce.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| A | Signed dimensionless amplitude of a selected mode | 1 |
| t | Time | s |
| dA/dt | Amplitude time derivative | s⁻¹ |
| ε | Linear growth coefficient | s⁻¹ |
| g | Positive nonlinear saturation coefficient | s⁻¹ |
| \|A*\| | Magnitude of a nonzero steady amplitude | 1 |
| √ | Positive square root | 1 |

Reading the relationshipLinear amplification balances cubic suppression at finite amplitude. Equating the terms and dividing by nonzero A gives A²=ε/g.

A worked exampleWith ε=0.04 s⁻¹ and g=4 s⁻¹, the steady magnitude is 0.1. At A=0.05 the rate is 0.002−0.0005=0.0015 s⁻¹.

ConditionsSymmetric near-threshold example for one mode, g>0; nonzero steady formula requires ε>0. It does not replace a spatially conserved concentration model or describe mode competition.

Boundaries influence patterns through concrete physical preferences. A wall favoring A enriches the nearby region and may promote layers parallel to the surface. Opposite preferences at two walls impose competing requirements on a thin film and can change its layer count and defects. If the sample width accommodates an integer number of natural periods, a continuous arrangement is easier to achieve. A mismatch of half a period requires stretching, reorientation or defects. A boundary is consequently part of the energetic and geometrical problem rather than an incidental frame around an image. Its influence is especially strong in films, pores and small devices with large surface-to-volume ratios.

Defects are places where an ordered arrangement cannot join smoothly, such as a stripe ending within the sample or regions of different orientation meeting. Their removal requires material transport and chain rearrangement, sometimes much slower than local phase separation. Numerous defects can therefore indicate ongoing relaxation or persistent incompatibility imposed by boundaries. Watching where defects move, merge and remain over time helps distinguish these situations. In a material intended to provide continuous transport channels, the connecting role of a few defects may affect performance more strongly than the mean period. A length-scale measurement alone does not fully describe that functional geometry.

Processing rate selects a route as well. Rapid cooling can bring many small fluctuations into an unstable region nearly together, whereas slowly changing conditions allow earlier structures more time to adjust. Solvent evaporation creates composition and temperature differences through thickness. A surface layer may become viscous while the interior still flows, leaving a depth-dependent morphology. Designing uniform pores or aligned layers therefore requires comparing the rate of external change with chain diffusion, interface motion and solvent transport. A final temperature alone will often fail to reproduce the process. The sequence of conditions and the time available at each stage are active variables in the formation of the finished material.

## Inferring mechanism from images and time series

When examining a material image, first establish what its contrast represents. Electron microscopy may show composition, staining or surface topography. Polarized images may combine orientation and thickness, while optical turbidity reflects scattering from refractive-index variations. Treating every contrast as concentration would mix distinct mechanisms. Independent checks of composition, thickness or orientation give domain size, connectivity and regularity a definite physical object. For porous materials, adjacency within a two-dimensional section must also be distinguished from genuine connectivity in three dimensions. Two channels that seem to meet in projection may pass at different depths, while disconnected-looking sections may join elsewhere in the volume.

A characteristic scale can be estimated from distances between neighboring peaks or by comparing the whole image with waves of different directions and wavelengths. A strong match produces a larger signal near the corresponding wavenumber. Scattering likewise provides peaks related to spatial correlations. Converting peak position to wavelength requires 2π divided by wavenumber, rather than simply its reciprocal, because wavenumber is defined using radians per length. A broad peak suggests a range of scales or a limited correlation distance; a sharp one concentrates periodic information. Orientation distributions, instrumental resolution and the finite field of view also influence peak shape and need consideration when comparing specimens.

Converting a spectral peak into spacingEq. 10

![Converting a spectral peak into spacing](https://ml-biomat.com/static/agent-math/72bf9de79da6523217155b9f.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ℓpeak | Characteristic spacing estimated from peak position | m |
| qpeak | Peak wavenumber defined in radians per length | m⁻¹ |
| π | Circle constant | 1 |

Reading the relationshipA wavelength accumulates 2π radians of phase, giving spacing 2π/q. A measurement quoted in cycles per length uses a different convention.

A worked exampleqpeak=0.20 nm⁻¹ gives ℓpeak≈31.4 nm. A shift to 0.10 nm⁻¹ increases the spacing to 62.8 nm.

ConditionsThe peak must correspond to the spatial correlation of interest; shape factors, multiple structural levels and orientation averaging require analysis of the full spectrum.

Time series are especially informative. Early signals at different wavenumbers growing at fixed respective rates can be compared with a linear growth spectrum. A peak moving toward smaller wavenumber indicates increasing characteristic size. A stationary peak position with changing intensity or width can instead reflect stronger composition contrast, improved orientation or fewer defects. For small concentration waves under the appropriate scattering approximation, intensity is proportional to amplitude squared. An exponential intensity growth rate must therefore be divided by two to infer the amplitude growth rate. This conversion requires the corresponding scattering and linear-response conditions, rather than automatic substitution of an instrument's slope into the amplitude equation.

Thin-film dewetting illustrates a sequence of evolving structures. In a 1992 study of polystyrene films, Reiter described hole formation, growing rims that meet, and subsequent breakup of rim structures into droplets. Putting these stages on a time line shows that hole spacing, cellular-structure size and droplet spacing are not one permanently fixed length. Film thickness is a conserved field in this setting, while substrate interactions and surface tension contribute to evolution. Locating where holes first appear, assessing correlations with defects and comparing early spatial spectra can help distinguish nucleation from a continuous instability. The final droplet image alone does not specify the initial route.

The final step is to translate a proposed mechanism into conditions that an experiment can change. Testing how incompatibility or gradient cost affects an early scale requires controlled changes in quench depth while tracking transport conditions. Testing kinetic arrest requires waiting, reheating and waiting again. Testing boundary selection requires changes in thickness or surface preference. Testing reaction–diffusion requires reaction-feedback and transport measurements for the participating substances. Each experiment connects a specific causal relation to an observable response. A material pattern then becomes a measurable and designable structure whose growth rate, spacing, connectivity and retention mechanism jointly determine its practical function. Recording these quantities together is more informative than assigning a mechanism from appearance alone.

The observation window needs checking as well. An image containing only two periods is sensitive to cropping and edges, while a period represented by only two or three pixels is poorly resolved. A wider field of view and finer spatial resolution solve different problems; comparing magnifications over overlapping scales helps address both. Imaging several positions also tests whether a pattern near a surface defect represents the bulk specimen. These checks do not change the physical model, but they determine whether an experiment can distinguish two nearby candidate wavelengths reliably.
