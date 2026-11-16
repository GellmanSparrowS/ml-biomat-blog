# How Radicals Make Different Materials: From Active Chains to Industrial Particles

Source: https://ml-biomat.com/tutorials/biomaterials-courses/pe07/en/
Language: en

Films, rigid housings and fibres can all begin with radical reactions. Follow propagation, transfer, phase separation and particle formation to understand how rate, chain length and manufacturing history become material properties.

## One way of growing chains, many kinds of material

A flexible packaging film, an impact-resistant appliance housing and a fibre drawn into a fine thread can all begin with the same broad reaction class: free-radical polymerization. A radical carries an unpaired electron and can react with a suitable monomer's carbon–carbon double bond, attaching that monomer to a growing chain. Knowing that these materials are radical-polymerization products does not yet explain their differences. Monomer structure determines which chemical fragments remain after connection. The reaction environment influences chain length, branching, particles and phase domains, while separation and processing carry these structures into the finished article.

Start with the history of one chain. An initiator generates radicals by thermal decomposition or another suitable reaction. The fraction that successfully starts chain growth contributes to effective initiation. After an active end adds a monomer, the new chain end remains active and can add another; this is propagation. Two active ends can meet and join, leaving a single molecule without those active ends, a process called termination by combination. Alternatively, hydrogen transfer between them can deactivate both while leaving two molecules, called termination by disproportionation. Termination refers to the active chains involved, not to the end of the entire reactor batch. Other chains can still initiate, propagate or terminate.

In chain transfer, a growing chain takes an atom or group from another molecule. Growth of the original molecule stops, while a new radical appears elsewhere. If that radical can start further polymerization, reaction activity continues. A relay offers a useful analogy: propagation resembles one runner continuing forward, while transfer hands the baton to another runner. The handover need not remove activity from the system, but it fixes the length reached by the original molecule. If the new active site appears on an existing polymer, subsequent growth can create a branch, making transfer particularly important to material architecture.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe07/en/#en-s1)

Figure 1 · Propagation, combination and transfer followed by reinitiation. Mayo’s1943 transfer relationship explains how activity can continue while the length of an individual molecule is fixed. Line lengths and colours distinguish paths rather than molecular dimensions.

Manufacture must also decide where these events happen. Bulk polymerization uses monomer and the polymer being formed as the main reaction material. Solution polymerization introduces a solvent that dissolves the relevant components. Suspension polymerization disperses monomer into relatively large droplets, allowing many droplets to react within water. In conventional emulsion polymerization, much of the growth instead occurs in small polymer particles, while larger monomer droplets commonly serve as reservoirs. Water alone does not distinguish the processes: suspension and emulsion can both contain it, yet differ in initiator location, particle formation and the principal reaction locus.

The chapter follows activity, heat and structure. A simplified model first connects rate with chain length; polyethylene, toughened polystyrene, poly(vinyl chloride), polyacrylonitrile and ABS then show how these ideas enter different manufacturing routes. Material residence time also differs from the active lifetime of a single chain. A parcel can remain in a reactor for a substantial period while many short-lived active chains are generated and terminated within it. Separating these two times explains why extending reaction time usually increases conversion without making every individual chain grow continuously throughout the extra interval.

## A faster reaction can make shorter chains

In a uniform reaction liquid at approximately constant temperature, adding initiator often accelerates polymerization because more active chains are generated per unit time. Those chains also encounter one another more readily and terminate. Imagine participants continuously entering a room and leaving when they meet in pairs. Faster entry increases the number present, but not in direct proportion, because opportunities for pairwise encounters grow more strongly with population. In the simplest steady-state approximation, generation and disappearance of active chains nearly balance, producing the familiar square-root relationship.

Concentrations and rates count specified entities. One mole represents approximately 6.022×10²³ entities, much as a dozen represents twelve, but on a scale convenient for molecules. A monomer concentration of 5 mol/L means five moles of monomer in each litre of reaction liquid. Active-chain concentration counts chains that still carry radicals and excludes chains whose activity has terminated. Rate adds time: mol/(L·s) specifies the molar amount generated or consumed per litre each second. A rate coefficient connects concentrations with that rate, and its units must match how many concentration factors are multiplied. Identifying whether a quantity counts initiator, monomer or active ends, then checking its volume and time basis, makes the concentration-squared term for encounters between two radicals easier to understand.

Balancing effective initiation, termination and growthEq. 1

![Balancing effective initiation, termination and growth](https://ml-biomat.com/static/agent-math/04e13f82a04294ce755444e2.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| R_{i} | Rate of effective chain-radical generation | mol L⁻¹ s⁻¹ |
| f | Initiation efficiency, the fraction of primary radicals that initiate successfully | 1 |
| k_{d} | First-order initiator decomposition coefficient | s⁻¹ |
| [I], [M] | Initiator and monomer molar concentrations; brackets denote molar amount per volume | mol L⁻¹ |
| R_{t,loss} | Rate of radical disappearance by termination | mol L⁻¹ s⁻¹ |
| k_{t} | Termination coefficient defined for pair-encounter events | L mol⁻¹ s⁻¹ |
| c_{R} | Total concentration of active chain radicals | mol L⁻¹ |
| k_{p} | Propagation rate coefficient | L mol⁻¹ s⁻¹ |
| R_{p} | Rate of monomer consumption by propagation | mol L⁻¹ s⁻¹ |
| √, c_{R}² | Positive square root; radical concentration multiplied by itself describes pairwise encounters | as defined |

Reading the relationshipOne initiator decomposition generates two primary radicals, with efficiency selecting the useful fraction. Each bimolecular termination consumes two radicals. Equating generation and loss and taking the positive square root gives c_R; monomer encounters with active ends give propagation.

A worked exampleFor f=0.6, k_d=10⁻⁵ s⁻¹, [I]=0.01 mol/L and k_t=10⁷ L/(mol·s), c_R=7.746×10⁻⁸ mol/L. With k_p=500 L/(mol·s) and [M]=5 mol/L, R_p=1.936×10⁻⁴ mol/(L·s).

ConditionsHomogeneous, isothermal conditions with representative coefficients and slowly changing radical concentration. Oxygen inhibition, diffusion limitation and other activity-changing reactions are omitted. The k_t convention must match the factor of two in radical loss.

The consequence is useful: with the model's other conditions fixed, a fourfold increase in initiator concentration approximately doubles polymerization rate rather than quadrupling it. Meanwhile, four times as many chains are started per unit time, but only twice as much monomer is incorporated. The average amount assigned to each active-chain history therefore decreases. Kinetic chain length counts propagation steps per effective initiation event. The final number-average degree of polymerization additionally depends on termination mode. Combination joins two growth histories into one molecule, whereas disproportionation leaves two molecules, so their molecular counting differs.

In 1943, Frank Mayo investigated solvent reactions with radicals during styrene polymerization and related chain transfer to molecular size. The underlying idea is that each sequence of monomer additions has some chance of ending growth of the current molecule, with different transfer routes adding separate opportunities. Under suitable conditions, these contributions add to the reciprocal of average chain length. The reciprocal is intuitive: shorter chains mean that a given amount of monomer has been divided among more molecules. [Mayo's chain-transfer study](https://pubs.acs.org/doi/10.1021/ja01252a021) connected the molecular handover of activity to measurable molecular mass.

Chain transfer increases the number of moleculesEq. 2

![Chain transfer increases the number of molecules](https://ml-biomat.com/static/agent-math/1b7058d764e73d3e8f4d8d91.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ν | Kinetic chain length: mean propagation events per effective initiation | 1 |
| R_{p}, R_{i} | Propagation consumption and effective initiation rates | mol L⁻¹ s⁻¹ |
| X_{n} | Number-average degree of polymerization, monomer units per polymer molecule | 1 |
| C_{M}, C_{S}, C_{I} | Transfer constants to monomer, solvent or specified transfer agent, and initiator | 1 |
| [M], [S], [I] | Molar concentrations of monomer, solvent or transfer agent, and initiator | mol L⁻¹ |
| j, k_{tr,j}, k_{p} | j labels the transfer target; corresponding transfer and propagation coefficients | 1; L mol⁻¹ s⁻¹ |
| 1/X_{n} | Reciprocal degree of polymerization, measuring molecules per incorporated monomer unit | 1 |

Reading the relationshipCombination joins two kinetic growth histories into one molecule, giving X_n≈2ν without transfer. Transfer divides the same incorporated monomer among more molecules; each route adds to reciprocal chain length according to its competition with propagation.

A worked exampleUsing the preceding parameters, ν≈1613.74 and X_n≈3227.49 without transfer. A total transfer contribution of 0.001 reduces X_n to approximately 763.45.

ConditionsCombination termination, low or moderate conversion and rapid reinitiation after transfer, omitting complex branching from transfer to polymer and other chain-scission processes. Disproportionation-dominated termination instead contributes 1/ν.

### Adjust rate and chain length

[Figure: Adjust rate and chain length](https://ml-biomat.com/tutorials/biomaterials-courses/pe07/en/#en-s2)

Homogeneous isothermal model with combination termination and rapid reinitiation after transfer. Monomer 5 mol/L, reference initiator 0.01 mol/L, efficiency 0.6, decomposition coefficient 10⁻⁵ s⁻¹, propagation coefficient 500 and termination coefficient 10⁷ L/(mol·s). Transfer is the sum of the three contributions in the equation. Axes stay fixed.

The interaction separates initiation from transfer. First hold the transfer contribution fixed and increase initiator: the ideal rate rises while chain length falls. Then hold initiator fixed and increase opportunities for transfer followed by successful reinitiation. Chain length decreases, while total radical concentration and rate remain unchanged in this simplified model. Some actual transfer reactions produce radicals that react only slowly, causing retardation; their subsequent chemistry must then be included. The comparison shows how making a reaction faster and making its molecules shorter can be coupled, while also being adjustable through different elementary processes.

Initiator supply changes with time as well. Thermal initiators are often characterized by a half-life: at a specified temperature, one half-life reduces the remaining undecomposed amount by half. A half-life is not a fixed label independent of temperature. Industrial formulations may combine initiators with different decomposition rates to match activity supply to a reaction history, or add initiator at several stages. Each change affects both heat release and chain structure. This makes additional initiator a process choice with several consequences, rather than a way to raise output without changing anything else.

Half-life describes decomposition at a specified temperatureEq. 3

![Half-life describes decomposition at a specified temperature](https://ml-biomat.com/static/agent-math/b54a729cc5ac12b1fb527618.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| [I](t), [I]_0 | Undecomposed initiator concentration at time t and initially | mol L⁻¹ |
| t, t_{1}/2 | Elapsed time and half-life | s |
| k_{d} | First-order decomposition coefficient at the specified temperature | s⁻¹ |
| e, exp | Natural-exponential base, approximately 2.718; exponential decay follows loss proportional to the remaining amount | 1 |
| ln2 | Natural logarithm of 2, approximately 0.6931; the inverse of natural exponentiation | 1 |

Reading the relationshipLoss per time is proportional to undecomposed concentration, giving exponential decay. Setting the remaining concentration to half its initial value and taking the natural logarithm gives the half-life.

A worked exampleFor k_d=10⁻⁵ s⁻¹, half-life is approximately 69315 s, or 19.25 h. After two half-lives the undecomposed concentration is one quarter of its initial value.

ConditionsConstant temperature, first-order decomposition and approximately fixed volume without added feed. Changing temperature or continuous feeding requires temperature-dependent k_d and material flow.

As polymer accumulates, viscosity can rise strongly and make encounters between active ends more difficult, reducing termination. If monomer still reaches those ends readily, propagation continues, radical concentration rises and the reaction can accelerate. This autoacceleration is commonly called the gel effect, even when no permanent crosslinked network has formed. At still higher conversion, monomer motion may also become restricted and the reaction enters another regime. Extending an early-stage constant-rate-coefficient model across the whole conversion range would miss these changes. Temperature, viscosity and heat transfer need to be followed together.

## The flexibility of polyethylene film begins with branches

One industrial route to low-density polyethylene uses dense ethylene under high pressure for radical polymerization. The monomer still contains two carbons, but pressure changes density, the reaction environment and monomer–polymer phase behaviour. The reaction and separation sections serve different purposes. Reaction requires conditions suited to growth and heat transfer; downstream pressure reduction and related operations separate monomer-rich and polymer-rich streams, followed by monomer recovery, devolatilization and pellet production. Pressure therefore helps organize both reaction and separation, rather than simply compressing the equipment contents.

A long tubular reactor can contain several initiation positions or temperature zones. After initiator enters at one location, polymerization heat raises temperature. Cooling and changing reactant conditions subsequently lower it; another addition can establish a further reaction zone. Multiple temperature peaks reflect local activity supply, heat generation and removal together. Higher temperature also affects transfer, branching and molecular-mass distribution, so maximizing temperature is not equivalent to optimizing the product. Multiple zones distribute related tasks along the process, with cooling and material transport matched to each part.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe07/en/#en-s3)

Figure 2 · Staged initiation can create several temperature peaks. Intramolecular transfer and transfer to polymer contribute to different branching structures, which affect packing and melt motion. The temperature path is a qualitative process illustration.

Radical ethylene polymerization is especially useful for seeing how propagation and transfer jointly shape a chain. An active chain end can abstract hydrogen from a nearby position on the same molecule, moving activity from the end to an internal site. Subsequent monomer addition can create a short branch; this intramolecular process is often called backbiting. Transfer to another polymer molecule can instead create a growing site on an existing macromolecule and generate a longer branch. Branch length and distribution also depend on subsequent reactions, so a simple label such as “branched” does not describe all relevant architectures.

Short branches resemble small side shoots on a long cord: they interfere with close packing of the backbone and alter crystallization and density. In many polyethylene systems this helps create a more flexible material. Sufficiently long branches can participate in entanglements, changing how a melt carries and redistributes stress during stretching. These effects are relevant to melt strength in film blowing and foaming. Crystallization, light scattering, molecular mass and processing history jointly affect transparency, so more branching does not move every property in the same direction. Branch type becomes useful information when connected to a specific physical process.

Activation energy describes how sensitively a reaction rate depends on temperature. A mountain-pass analogy gives a starting picture: before reactants become products, their atoms and electrons must reach arrangements that are relatively difficult to access. Thermal motion continually explores states, and changing temperature changes access to a reaction pathway. The Arrhenius relation expresses this temperature dependence exponentially. With otherwise comparable conditions, a larger apparent activation energy usually means greater temperature sensitivity. It is a parameter inferred from rates over a stated range and need not equal the energy of a single chemical bond. Dividing the transfer and propagation relations produces the difference between their apparent activation energies in the expression below. Temperature is in kelvin, obtained by adding 273.15 to a Celsius value; the difference between inverse temperatures combines with energy and the gas constant to make a dimensionless exponent.

Temperature changes the competition between transfer and growthEq. 4

![Temperature changes the competition between transfer and growth](https://ml-biomat.com/static/agent-math/43cb691bb8a8373ae42c7d73.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| C(T), C(T_{0}) | Transfer constant for a specified route at T and reference T₀ | 1 |
| k_{tr}, k_{p} | Specified transfer and propagation coefficients | L mol⁻¹ s⁻¹ |
| E_{tr}, E_{p} | Corresponding apparent activation energies | J mol⁻¹ |
| R | Gas constant, using 8.314 | J mol⁻¹ K⁻¹ |
| T, T_{0} | Absolute temperature and reference temperature | K |
| exp | Natural exponential function with a dimensionless argument | 1 |

Reading the relationshipApply Arrhenius temperature dependences separately to transfer and propagation and divide. Prefactors cancel in the relative ratio. The difference in activation energies determines the competition.

A worked exampleIf E_tr−E_p=20000 J/mol, heating from 400 K to 420 K gives C(T)/C(T₀)≈1.332, a roughly 33% increase in competition relative to propagation.

ConditionsFixed prefactors and apparent activation energies over the compared range, for the same transfer route. Pressure, composition and phase changes require separate treatment.

Comparing temperature effects on growth and transfer requires their respective rate dependences. If a transfer route has a higher activation energy than propagation, heating can make that transfer relatively more competitive. Initiator decomposition, pressure, monomer concentration and other transfer routes may change at the same time, however. A product also experiences a distribution of temperatures and residence histories. Average molecular mass, short branches and long branches therefore need separate descriptions. Temperature measurement, feed allocation and cooling ultimately influence flexibility, strength and processing behaviour through these molecular events.

## How soft particles help a hard plastic absorb impact

Polystyrene is relatively stiff, but some applications require more energy absorption during a collision. One route to high-impact polystyrene begins by dissolving polybutadiene rubber in styrene and then polymerizing the styrene. Flexible macromolecules are therefore present before the new polymer forms. As polystyrene accumulates, changing compatibility and viscosity lead to regions with different compositions. Such a phase domain is a region with relatively consistent composition and properties at a particular scale. It is not an individual molecule, and it need not be visible to the naked eye.

Grafting occurs during the reaction: some polystyrene chains become chemically connected to polybutadiene backbones. These connections influence the interface and attachment between the phases. As polymerization proceeds, an initially continuous rubber-rich environment becomes dispersed rubber particles, while polystyrene forms the continuous matrix. This change is phase inversion. Polystyrene regions can also become enclosed within the rubber particles, producing the multilevel structure often called a salami morphology. Grafting, agitation, proportions and reaction history all influence it. The conversion at inversion is consequently formulation-dependent rather than a universal percentage.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe07/en/#en-s4)

Figure 3 · Qualitative HIPS evolution connected to Fischer and Hellmann’s microscopy study. Rubber particles after inversion can enclose polystyrene regions, producing multilevel structure. Stages depend on composition and reaction history rather than a universal conversion threshold.

In 1996, Fischer and Hellmann combined polymerization experiments with electron microscopy to examine how phase patterns developed with composition and graft architecture. Subsequent studies compared effects of initiator, agitation and rubber content on particle morphology. An instructive result is that the final arrangement of mixed polymers reflects more than equilibrium compatibility: it preserves aspects of how the polymers were generated, separated and stirred during reaction. The [study of HIPS phase-pattern evolution](https://pubs.acs.org/doi/10.1021/ma950779a) made chemical reaction and microscopic structure parts of the same observable process.

Under load, soft particles alter the surrounding stress distribution and can promote energy-consuming processes such as cavitation, crazing and shear yielding. A craze contains small voids and load-bearing fibrils; it is more structured than an empty crack. Shear yielding involves substantial plastic shear deformation. Suitable particles and interfaces can spread deformation over a larger region, allowing more energy to be absorbed before fracture. Increasing rubber content may also reduce stiffness or particular strength measures. Improved impact resistance and improved performance in every mechanical test are therefore different claims.

From force and extension to stress and strainEq. 5

![From force and extension to stress and strain](https://ml-biomat.com/static/agent-math/0110f3380308eb20fb6bb884.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| σ | Engineering tensile stress | Pa |
| F | Tensile force | N |
| A_{0} | Initial specimen cross-sectional area | m² |
| ε | Engineering tensile strain | 1 |
| ΔL, L_{0} | Gauge extension and initial gauge length | m |
| E | Small-strain tensile modulus under the stated test conditions | Pa |
| dσ/dε | Local change in stress per change in strain, the curve slope | Pa |

Reading the relationshipNormalize by initial area and length to obtain force per area and relative extension. The small-strain slope measures stress needed for a given small deformation.

A worked exampleAn initial area of 10 mm² under 100 N gives 10 MPa. A 50 mm gauge extending 0.25 mm gives strain 0.005; if this interval is linear through the origin, the modulus is 2 GPa.

ConditionsEngineering measures use initial geometry. Modulus is defined over a stated small-strain interval, temperature and loading rate. True stress and strain use different geometric definitions at large deformation.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe07/en/#en-s4)

Figure 4 · Qualitative stress–strain shapes on common axes, with dots marking fracture. They distinguish stiffness, stress level and tensile work without representing a particular material grade. Rubber toughening changes dissipation; impact and fracture properties use their corresponding tests.

Before interpreting a mechanical curve, check whether its vertical axis shows force or stress and whether its horizontal axis shows extension or strain. Dividing force by initial cross-sectional area gives engineering stress; dividing extension by initial gauge length gives engineering strain. These normalizations reduce direct specimen-size effects under stated test conditions. The initial small-deformation slope characterizes stiffness, while maximum stress and extension at break describe other properties. Elasticity concerns recovery on unloading. Under suitable conditions, the area within the elastic range represents recoverable stored energy, rather than serving as a definition of elasticity itself.

What energy the area under a curve representsEq. 6

![What energy the area under a curve represents](https://ml-biomat.com/static/agent-math/59a816ceae6ace3e49b24223.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| W | Mechanical work in the tensile process up to break | J |
| u, du | Extension integration variable and a small extension increment | m |
| F(u) | Tensile force as a function of extension | N |
| ΔL_{b}, ε_{b} | Extension and engineering strain at break; b denotes break | m; 1 |
| A_{0}, L_{0} | Initial cross-sectional area and gauge length | m²; m |
| w | Tensile work normalized by initial gauge volume | J m⁻³ |
| σ(ε), dε | Engineering stress as a function of engineering strain, and a small strain increment | Pa; 1 |
| ∫ | Integral, summing small force–displacement or stress–strain contributions; geometrically the area under the curve | as defined |

Reading the relationshipWork in a small displacement is force times displacement. Summing gives total work. Substituting engineering stress and strain gives the stress–strain area per initial volume.

A worked exampleA linear segment with modulus 2 GPa ending at strain 0.02 has triangular area 0.5×2×10⁹×0.02²=4×10⁵ J/m³. For an initial volume 10⁻⁴m³, the corresponding work is 40 J.

ConditionsDisplacement corresponds to the stated gauge segment, excluding deformation work in the test machine and other components. Tensile absorption depends on test conditions; notched impact and fracture toughness have their own definitions.

The area under an entire tensile curve can represent work done to failure or, after normalization by initial volume, tensile energy absorption per volume. Notched impact tests, fracture-toughness tests and slow tensile tests use different loading, geometries and crack conditions, and their results have different meanings and sometimes different units. When comparing toughening in HIPS or ABS, read the test together with its result. This explains why a soft phase can be useful and which structural parameters need adjustment for an application, without treating all numbers called “toughness” as interchangeable.

## A suspended monomer droplet develops internal structure

Suspension polymerization of vinyl chloride can be understood as many small reaction units surrounded by water. Sparingly water-soluble vinyl chloride is dispersed into droplets by agitation. An oil-soluble initiator largely enters those droplets, while stabilizers in the aqueous phase help maintain dispersion. Agitation can break larger droplets and also bring droplets into collisions that may cause coalescence. Final size reflects competition between these processes. Water facilitates heat removal, but does not ensure that each droplet remains internally uniform or that water quantity alone determines particle size.

Newly formed poly(vinyl chloride) has limited solubility in its monomer, so polymer-rich regions develop inside the droplets. Small particles form, aggregate and join into grains with internal pores and multiple structural levels. One visible suspension-resin grain can contain many smaller primary particles and their aggregates. Pores influence residual-monomer removal, subsequent entry of additives and absorption during processing. External grain shape, internal porosity and chemical chain length belong to different scales; they cannot all be described as the same kind of particle growth.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe07/en/#en-s5)

Figure 5 · Hierarchical suspension-PVC structure. Orange indicates monomer-rich material and small orange dots the initiating component; teal regions indicate polymer-rich material. Actual primary particles, aggregates and grains occupy different scales determined by formation history.

During a typical stage, it is useful to consider gas, aqueous, monomer-rich and monomer-swollen polymer-rich phases. Swelling means that small molecules enter a polymer and change its volume and mobility. Monomer partitioning depends on intermolecular interactions as well as concentration. Fugacity expresses chemical potential in a pressure-like form, allowing comparison of the tendency of a component to transfer between phases. At phase equilibrium under specified temperature and pressure, the fugacity of a particular component is equal across the coexisting phases.

A first interpretation of chemical potential is the change in free energy when a small amount of a species is added to a particular environment at fixed temperature and pressure. Free energy combines energetic effects with the possibilities for molecular arrangements and helps determine the direction of redistribution. If the same species has different chemical potentials on two sides, transfer from the higher side to the lower can reduce the total free energy. At equilibrium that net driving force disappears. Fugacity expresses this comparison in a convenient pressure-like form: concentrations can differ between phases even while the chemical potential of the species is equal.

Phase equilibrium links pressure with monomer stateEq. 7

![Phase equilibrium links pressure with monomer state](https://ml-biomat.com/static/agent-math/26744b3f1bee000cc8bc5b61.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| f_{m}^(α), f_{m}^(β) | Fugacity of monomer m in phases α and β; superscripts label phases rather than powers | kPa |
| g, p | Superscripts denoting gas and polymer-rich phases | 1 |
| ϕ_m, y_{m} | Gas-phase monomer fugacity coefficient and mole fraction; varphi differs from the volume fraction used later | 1 |
| P, p_{m} | Total gas pressure and monomer partial pressure, p_m=y_mP | kPa |
| a_{m} | Monomer activity relative to pure liquid monomer at the same temperature | 1 |
| p_{m}^sat(T), T | Pure-monomer saturation vapour pressure at absolute temperature T | kPa; K |

Reading the relationshipEqual chemical potentials at equilibrium can be expressed as equal fugacities on a common basis. For an approximately ideal vapour and small liquid pressure correction, partial pressure relative to pure-monomer vapour pressure approximately equals activity.

A worked exampleIf saturation vapour pressure at a chosen temperature is 500 kPa and monomer activity is 0.8, the approximation gives a monomer partial pressure of 400 kPa. Other gas partial pressures add to the total.

ConditionsPhases close to equilibrium on a common chemical-potential basis. The approximate pressure relation omits vapour nonideality and the liquid Poynting correction. Example values illustrate the relation rather than specify vinyl-chloride properties at a particular temperature.

At low monomer concentration in water, Henry's law can connect aqueous concentration with monomer partial pressure over an appropriate range. Partial pressure is one component's contribution to total gas pressure, which may also include water vapour and other gases. Monomer interactions with long chains in the polymer-rich phase require a different description. Activity combines composition and interaction effects into an effective-concentration measure relative to a chosen standard state. Unit activity means that the chemical potential matches that standard state; it does not mean that every possible concentration measure equals one.

Monomer partitioning into dilute aqueous solutionEq. 8

![Monomer partitioning into dilute aqueous solution](https://ml-biomat.com/static/agent-math/0f942b9285d1deafd6547e79.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| c_{m,w} | Aqueous monomer molar concentration; w labels the water phase | mol L⁻¹ |
| k_{H} | Henry solubility coefficient defined here as concentration divided by pressure | mol L⁻¹ kPa⁻¹ |
| p_{m} | Monomer partial pressure in the equilibrated gas | kPa |

Reading the relationshipIn the dilute range at a specified temperature, dissolved concentration is approximately proportional to gas partial pressure. The proportionality coefficient depends on substance and temperature.

A worked exampleWith k_H=2×10⁻⁵ mol/(L·kPa) and p_m=500 kPa, c_m,w=0.010 mol/L. Converting pressure to pascals requires a matching coefficient conversion.

ConditionsDilute solution at a specified temperature and near phase equilibrium. Henry constants use several conventions, including reciprocals; definitions and units must match the data.

Monomer activity in a long-chain environmentEq. 9

![Monomer activity in a long-chain environment](https://ml-biomat.com/static/agent-math/cf0973d086b94b45906b73ea.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| a_{m} | Monomer activity relative to pure monomer | 1 |
| φ_{m} | Monomer volume fraction within the polymer-rich phase | 1 |
| 1−φ_{m} | Polymer volume fraction in that phase | 1 |
| χ | Flory–Huggins interaction parameter describing the interaction contribution to mixing | 1 |
| ln | Natural logarithm, inverse of the natural exponential | 1 |

Reading the relationshipMixing long chains and small molecules has an asymmetric molecular count and hence mixing entropy, together with an interaction contribution. Differentiating mixing free energy for the monomer chemical potential and taking the long-chain limit gives this activity approximation.

A worked exampleAt φ_m=0.40 and χ=0.84, ln a_m≈ln 0.4+0.6+0.84×0.6²≈−0.01389, so a_m≈0.9862. Activity and volume fraction differ substantially.

ConditionsBinary Flory–Huggins description in the long-chain limit, with representative χ over the composition interval. Phase equilibrium additionally requires the stable branch. Vitrification, finite chain length and composition-dependent parameters need fuller treatment.

While an almost pure monomer-rich phase remains, it acts as a reservoir, exchanging monomer with the other phases and helping maintain their monomer state. At nearly constant temperature with sufficiently rapid exchange, monomer partial pressure can remain approximately steady over part of the reaction. Once that reservoir is exhausted, continuing polymerization lowers monomer content in the polymer-rich phase and pressure begins to fall. This transition provides useful process information, but its conversion depends on temperature, composition, partitioning and volume. Reservoir depletion and increasing diffusion resistance can be related without being identical events; a pressure change alone does not replace a kinetic assessment.

After grain formation, residual monomer is recovered through operations including stripping, followed by solid–liquid separation and drying. True density relates mass to the volume of the material itself, whereas bulk density includes spaces between packed grains. The same resin can therefore have different bulk densities. Adsorption, solubility and interfacial behaviour of stabilizers influence grain development, so a single surface-tension value cannot predict all porosity. Distinguishing chain structure, internal grain structure and powder packing explains why several operations after polymerization remain directly connected to product quality.

## How polyacrylonitrile travels from reaction liquid to fibre

Polyacrylonitrile manufacture closely connects polymerization with spinning. Its chains retain many nitrile groups, written —C≡N: C and N denote carbon and nitrogen, three lines represent the carbon–nitrogen triple bond, and the initial single line attaches the group to the backbone. Uneven electron distribution gives this group polarity, influencing interactions between chains and between the polymer and a solvent. A medium that keeps the polymer dissolved permits homogeneous solution polymerization, after which suitable concentration, purification and formulation can produce a spinning dope. The solvent does more than reduce viscosity: it carries heat, changes the reaction environment and may participate in chain transfer. Solvent choice therefore has to serve reaction, fibre formation and recovery together.

An alternative route allows polymer to precipitate as it forms, producing dispersed solid particles. Monomer distribution in the starting medium does not guarantee that the emerging long chains will remain soluble. Increasing chain length changes mixing thermodynamics and can cause precipitation. The product can be stripped of monomer, washed and separated, then dissolved in an appropriate solvent for spinning. Separation provides an opportunity to adjust impurity content, while grain compactness, drying history and interchain association influence redissolution. Adding a washing stage does not automatically improve every quality attribute.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe07/en/#en-s6)

Figure 6 · Material exchange in PAN wet spinning. Dope enters a coagulation bath, where solvent and nonsolvent diffuse in opposite directions and a fibre develops. Teal strands represent forming filaments, not individual molecules.

During wet spinning, the dope passes through spinneret holes into a coagulation bath. Solvent diffuses outward and nonsolvent enters, progressively removing the conditions that sustain a uniform polymer solution. Fibre structure develops during this exchange. A loose collection of cords coming together as their surroundings change offers a rough analogy, but the actual process combines diffusion, phase separation, flow and stretching. A rapidly formed dense surface layer can hinder internal exchange, while phase separation at different internal scales can create voids. The fibre is established over a continuous solvent-exchange history rather than instantaneously frozen at the spinneret exit.

Small comonomer contents can also adjust interchain interactions, processability and later reactions. For carbon-fibre precursors, the copolymer structure must be considered in relation to nitrile-associated reactions and heat release during stabilization. Other fibre applications may emphasize dyeing, softness or a processing window. The role of a comonomer should therefore be connected to composition and use. Molecular mass and its distribution from solution or precipitation polymerization likewise depend on initiation, termination, transfer and phase partitioning, rather than following a fixed ranking based only on the two process names.

At the flowsheet level, directly obtaining a spinnable solution can avoid a drying and redissolution cycle. Isolating the polymer first instead provides a separate opportunity for washing and storage. Both routes must address solvent recovery and residual monomer. Defects, orientation and pores in the eventual fibre depend on chain length together with dope uniformity, filtration, coagulation and drawing. After learning polymerization and shaping separately, connecting them again explains why a small upstream change can become significant within a very fine filament.

## Small particles change how often radicals meet

Water, a hydrophobic monomer, surfactant and a suitable initiator system can organize reaction at a finer scale than suspension droplets. Surfactants generally contain both water-affine and oil-affine parts and adsorb at interfaces. Under suitable conditions and concentrations, they also form micelles, small self-assembled aggregates of surfactant molecules. A micelle differs from a polymer particle that already contains macromolecular chains. In conventional emulsion polymerization, monomer droplets often provide a reservoir, monomer travels through the aqueous phase into smaller particles, and activity develops through aqueous reactions and radical entry.

Harkins presented a systematic account of emulsion-polymerization mechanisms in 1947. In 1948, Smith and Ewart examined radical kinetics in separated reaction loci. The significance of separation is direct: radicals in different particles cannot meet and terminate as they would in one homogeneous solution. Entry into the same particle, or processes involving exit and re-entry, change the opportunities for encounters. A particle therefore holds monomer and polymer while also regulating activity survival. The [early mechanistic work on emulsions](https://pubs.acs.org/doi/10.1021/ja01198a053) connected colloidal organization with polymerization rate.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe07/en/#en-s7)

Figure 7 · Compartmentalized reaction loci emphasized by Harkins and Smith–Ewart. The upper diagram distinguishes a monomer reservoir from polymer particles; the lower diagram shows ideal switching between zero and one active radical. Small orange dots denote activity; many inactive chains may exist in a particle.

One instructive limit allows a particle to contain zero or one active radical most of the time. Entry of a second radical is followed by very fast termination of the pair. A particle can contain many inactive polymer chains; the zero-or-one count concerns active radicals only. If entry into inactive and active particles is equally likely and radical exit is neglected, particles switch between inactive and active states, with a long-term mean activity near one half. This is an average over many particles or repeated histories, not half of a physically divided radical.

Emulsion rate from activity inside particlesEq. 10

![Emulsion rate from activity inside particles](https://ml-biomat.com/static/agent-math/f6935b4fb7f4c975d6fadc18.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| R_{p} | Monomer consumption rate per litre of total dispersion | mol L⁻¹ s⁻¹ |
| k_{p} | Propagation coefficient inside particles | L mol⁻¹ s⁻¹ |
| [M]_p | Monomer concentration per particle-phase volume; p labels the particles | mol L⁻¹ |
| n̄ | Mean active-radical count per particle | 1 |
| N_{p} | Particle count per litre of total dispersion | L⁻¹ |
| N_{A} | Avogadro constant, 6.02214076×10²³, converting particle counts to molar amounts | mol⁻¹ |

Reading the relationshipk_p[M]_p gives mean additions per radical per second. Multiply by radicals per particle and particles per litre, then divide by the Avogadro constant to convert monomer counts to moles.

A worked exampleFor k_p=500 L/(mol·s), [M]_p=5 mol/L, n̄=0.5 and N_p=10¹⁷ L⁻¹, R_p≈2.076×10⁻⁴ mol/(L·s). Doubling particle count at fixed other quantities doubles the rate.

ConditionsRepresentative common intraparticle conditions and growth mainly within particles. Significant aqueous growth, size distributions or transfer limitations require extensions. Internal concentration and particle count per dispersion volume use distinct volume bases.

Switching between zero and one radicalEq. 11

![Switching between zero and one radical](https://ml-biomat.com/static/agent-math/fd571ca938bdc56fb66644d5.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| p_{1}(t) | Probability of one active radical at time t, also the fraction of a large particle population in that state | 1 |
| 1−p_{1} | Fraction of particles without an active radical | 1 |
| a | Radical entry rate per particle, assumed identical in both states | s⁻¹ |
| b | Exit rate of the active radical from a particle | s⁻¹ |
| t, dp_{1}/dt | Time and instantaneous rate of probability change | s; s⁻¹ |
| n̄, p_{1},∞ | Mean active count per particle and long-time single-radical probability;∞ denotes the long-time limit | 1 |
| e | Natural-exponential base; decay describes approach to the stationary state | 1 |

Reading the relationshipEmpty particles gain a radical at rate a. Occupied particles become empty after entry-triggered rapid pair termination or radical exit. Solving this gain–loss balance for an initially empty population gives exponential approach to the stationary state.

A worked exampleAt a=0.1 s⁻¹ and b=0, stationary p₁=0.5 and its value at 20 s is approximately 0.49084. With b=0.2 s⁻¹, stationary p₁=0.25 and the 20 s value is approximately 0.24992.

ConditionsTermination is sufficiently fast when two radicals coexist, allowing a zero/one model. Entry and exit rates are constant and the initial population inactive. Higher occupancies, coupled re-entry and changing particle sizes require an expanded state model.

### Follow an initially inactive particle population

[Figure: Follow an initially inactive particle population](https://ml-biomat.com/tutorials/biomaterials-courses/pe07/en/#en-s7)

Zero–one model with equal entry rates for inactive and active particles and rapid termination after a second radical enters. Initially all particles are inactive. Propagation coefficient 500 L/(mol·s), internal monomer 5 mol/L and 10¹⁷ particles per litre of total dispersion. Curves are deterministic state fractions versus time.

In the interaction, increasing entry rate brings the population toward its stationary state faster. Allowing active radicals to leave particles can lower mean occupancy below one half. Different particle sizes, monomers and initiation conditions can also permit several radicals in a particle, requiring a fuller occupancy distribution. Emulsion polymerization can sometimes combine a high reaction rate with high molecular mass because particle number, internal monomer concentration and termination opportunities provide controls different from those in a homogeneous liquid. Emulsion does not generally mean slow reaction, and one-half occupancy is not a universal constant.

Particles can also form through more than one route. Radical entry into micelles can initiate particle formation, while aqueous oligomers may form new particles after reaching insufficient solubility. Surfactant-free emulsions further show that micelles are not a necessary starting point for every nucleation process. Critical micelle concentration depends on temperature, electrolyte and surfactant properties. Ionic surface layers affect particle approach through charge and ion distributions; nonionic chains can provide steric stabilization. Both depend on adsorption. Electrolytes can promote coagulation in some systems, with the response determined by the stabilization mechanism rather than a universal salt-operated switch.

## ABS brings grafting, particles and a matrix together

The name ABS derives from acrylonitrile, butadiene and styrene, yet its industrial structure is commonly more elaborate than a single random chain of three monomers. One familiar emulsion route first makes polybutadiene latex, then polymerizes styrene and acrylonitrile in the presence of the rubber particles. Some new polymer forms grafted structures, while another portion becomes free styrene–acrylonitrile copolymer, or SAN. Grafted material helps organize the connection between rubber and the harder surrounding phase; free SAN can supply much of the continuous matrix. SAN can also be prepared separately and combined through suitable mixing and processing to adjust composition.

Rubber-particle size and size distribution, rubber content, grafting, and SAN composition and molecular mass jointly influence deformation and processing. Combining different rubber-particle sizes can promote useful energy-dissipation processes at different scales, but spacing, interfaces and matrix yielding must be considered as well. Increasing rubber can improve impact resistance under certain conditions while reducing stiffness or heat resistance. Unsaturation in the rubber phase also affects weathering, linking formulation with service environment. One particle diameter or rubber fraction therefore provides only part of a material comparison.

An emulsion product normally leaves reaction as a latex, a dispersion of polymer particles in liquid. If the intended use needs that dispersed form, further formulation addresses stability, film formation and residual components. A dry-resin product instead can require coagulation, washing, dewatering, drying and melt mixing. Each operation changes residual surfactant, water, monomer and particle contact. For biologically related uses, monomer identity, residual small molecules, extractables and final surface state all enter material design. Polymerizing in water does not perform those quality-control tasks by itself.

The word latex also needs its object specified. Natural-rubber latex originates in a biological secretion and can contain accompanying proteins and other substances. A synthetic polymer latex describes a manufactured particle dispersion, with different chemistry and accompanying components. Similarly, a suspension-resin grain, an emulsion-polymer particle and the powder formed by coagulating latex belong to different formation stages. Knowing the history of a particle helps explain its surface, pores, dispersion stability and subsequent processing behaviour.

The routes now connect at several levels. Low-density polyethylene uses pressure, temperature and transfer to shape branching. HIPS develops grafting and phase morphology during polymerization. Suspension PVC links internal grain structure with monomer partitioning. PAN connects reaction solution to spinning, while emulsion ABS combines compartmentalized activity with rubber particles and a grafted matrix. Their shared radical chemistry is organized into different spaces and histories. Understanding a process makes it possible to follow a macroscopic property back to the molecular events, phase structures and manufacturing stages that jointly produced it.

Consider: why are monomer droplets in water and polymer latex particles in water different reaction units?

Suspension droplets commonly contain both the main monomer supply and an oil-soluble initiator. Their interiors can undergo bulk-like chain growth together with precipitation and aggregation. Small particles in conventional emulsion polymerization instead sustain reaction through monomer supply, radical entry and exit, and intraparticle termination, while larger monomer droplets often serve as reservoirs. Both are dispersed in water, but their reaction loci, activity supply and transport paths differ, requiring different kinetic and particle-formation descriptions.
