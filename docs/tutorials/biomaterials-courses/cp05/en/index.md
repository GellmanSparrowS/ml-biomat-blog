# Many Chains Together: Blending, Microphases and Crystallization

Source: https://ml-biomat.com/tutorials/biomaterials-courses/cp05/en/
Language: en

Two polymers can form a uniform material or separate into domains. Connecting unlike blocks within each molecule can instead produce organized layers and cylinders. Follow these phenomena from the free energy of mixing to microphase separation and folded-chain crystals, and see how connectivity, interfaces and conformation organize a material.

## From a mixed liquid to a solid polymer

When two portions of water are poured together, their original boundary quickly disappears. Oil and water behave differently: shaking creates small droplets, but these can merge again. Two molten polymers face a similar choice, although their molecules are much longer and their motion is slower. A freshly extruded transparent film may look uniform and become cloudy after storage or reheating. An impact-resistant plastic can appear uniform while containing many rubber particles. Understanding a collection of chains therefore requires three separate questions: do its molecules favour mixing, how large are its internal regions, and has the structure had time to change? These questions concern thermodynamics, spatial organization and time. A single visual observation cannot answer all three.

A polymer consists of repeated units joined by chemical bonds. The bonds preserve connections between neighbours, while rotations around suitable bonds allow the chain to bend. In a dense material, each chain is surrounded by segments belonging to other chains. The material looks continuous, but each molecule retains its identity. A blend is a material containing two or more polymers; the word does not require molecular-scale miscibility. A phase is a region whose properties are reasonably uniform at the relevant observation scale. A blend may contain two phases with different compositions, and each phase may contain some of the other polymer. Reading “blend” as “uniform mixture” would skip the structural question that needs investigation.

Observation scale matters. A nanometre is one billionth of a metre, comparable to several small molecules. A micrometre is one millionth of a metre and can contain many polymer chains. A material with domains much smaller than visible wavelengths can remain transparent, as can one whose two phases have closely matched refractive indices. Conversely, cloudiness can come from crystals, voids or a rough surface. It need not indicate separation of two polymers. Transparency is therefore a useful clue that becomes a structural interpretation when combined with scattering, microscopy and thermal analysis.

There is another way to organize a material: chemically connect two long sequences with different properties. A molecule containing an A sequence followed by a B sequence is an AB diblock copolymer. A block is a continuous run of units, rather than an alternating A–B sequence. If A–B contacts are unfavourable, similar segments still tend to gather together. Their junction, however, prevents the two blocks from travelling to opposite ends of the specimen. Separation can then occur over a finite distance, creating alternating layers, cylinders or spherical domains. The same chemical preference produces different spatial outcomes when molecular connectivity changes.

Crystallization introduces another organizational question. Even a material containing a single polymer can arrange some of its segments into a regular lattice. Many segments inside a crystal share ordered orientations and spacings, while chains outside it can bend, pass through disordered regions or connect another crystal. A common polymer solid is consequently semicrystalline: crystalline and amorphous regions coexist. Blending changes which species are neighbours. Microphase organization also depends on which species are connected. Crystallization additionally requires regular packing. Distinguishing these questions gives each free-energy calculation a clear physical target.

A static theory of many chains seeks favourable arrangements at a specified temperature, pressure and composition. Static does not mean that molecules have stopped moving. Individual segments can move continually while average composition and average crystalline structure remain steady. Processing also requires a timescale: how long can a melt reorganize before cooling prevents further motion? Thermodynamics identifies the favourable direction, while dynamics determines how far the material moves in the available time. Their combination explains why the same formulation can develop different properties under different cooling and annealing conditions.

[Figure: Three forms of many-chain organization](https://ml-biomat.com/tutorials/biomaterials-courses/cp05/en/#en-s1)

Figure 1 · Top: independent species can occupy separate enriched regions. Middle: diblock junctions constrain separation. Bottom: ordered stems form a local crystal. These drawings compare connectivity and ordering rather than successive snapshots of one material.

## Why a single chain remains useful in a crowded material

Imagine placing a very small amount of polymer in a good solvent. Solvent penetrates each coil, and different coils are mostly far apart. Segments cannot occupy the same space. This excluded-volume effect makes a sufficiently long flexible chain more expanded than a simple random walk. As more polymer is added, the spatial envelopes of the coils begin to overlap. It is their open envelopes that overlap: atoms do not acquire permission to pass through one another. A coil contains considerable space that solvent and neighbouring chains can occupy. A concentrated solution should therefore not be pictured as a bag of impenetrable balls of yarn.

In a semidilute solution, consider a small region within a correlation length. A subchain there still responds strongly to its own excluded volume and resembles a chain in a good solvent. Enlarge the observation region, and many segments from other chains enter the picture. If a selected chain adds segments locally, neighbouring chains generally surrender some of that space, while total concentration resists a large change. The surroundings therefore constrain the tendency of one isolated chain to expand continually. Screening names this reduction of the effective interaction: a collective response changes long-distance chain statistics.

Treat each correlated region as a blob, and the whole chain becomes a path made from connected blobs. Different statistics inside and between blobs allow local self-avoidance and an approximately random walk at larger distances to coexist. A blob is an observation unit used for coarse graining. It has no physical shell, and its segments need not number exactly the same as those in every other blob. The useful distinction is one of scale. An interaction that matters at a nanometre need not influence chain shape in precisely the same way at every larger distance.

Removing almost all solvent produces a dense amorphous melt. In a homogeneous melt of sufficiently long, flexible, linear chains, large-scale conformations often approach ideal-chain statistics: the mean-square end-to-end distance grows approximately in proportion to the number of statistical segments. This does not turn a melt into a dilute solution or make atomic volume vanish. Near-ideal behaviour in a dilute theta solution results from a balance of effective two-body interactions. Near-ideal behaviour in a melt comes from screening in a dense, nearly incompressible environment. Similar size relationships can thus emerge from different physical circumstances.

Screening also leaves the inability of chains to pass through one another intact. A chain may resemble a random walk in its static size while its motion is strongly constrained by entanglements. Many flexible ropes in one box provide a useful distinction: the space occupied by a rope and the time needed to pull it out are separate questions. Entanglements in a real melt are not permanent knots. They are constraints created by surrounding chains, and they renew as those chains move. A relatively simple equilibrium conformation can therefore coexist with a viscosity that increases rapidly with chain length.

This picture provides a practical starting point for blend theory. For two interpenetrating species of flexible chains, estimate contacts from average concentrations and then compare the free energies of different compositions. Local structure still matters. Short chains, interfaces, strong stiffness, electric charge and different chain topologies can each alter the simple dense-chain picture. Before averaging away degrees of freedom, identify the chain architecture, density and distance scale of the material under discussion. The resulting approximation then has a specific physical purpose rather than being a label applied to every polymer melt.

## Why long chains reduce the entropic reward for mixing

To decide whether mixing is favourable, contact energy and freedom of arrangement must be compared on a common scale. At fixed temperature and pressure, that scale is Gibbs free energy. Contact energy describes the cost or benefit of changing molecular neighbours. Entropy counts the microscopic arrangements compatible with the same macroscopic conditions. Mixing generally increases the number of arrangements and therefore gains entropy. A higher temperature gives the same entropy change greater weight in free energy. A tendency toward lower free energy expresses these energetic and statistical preferences together; it does not imply that molecules deliberately seek a destination.

The essential feature of chain mixing is that segment positions are not independent. Placing one hundred separate beads differs from placing the same beads after threading them onto a string. Moving one connected unit usually requires cooperation from its neighbours. Each repeat unit cannot therefore be counted as a separate small molecule. In 1941–1942, Flory and Huggins independently developed lattice-based theories of polymer solutions that included this disparity in molecular size. A lattice divides space into equal sites for counting. It does not claim that molecules in a liquid actually occupy a permanent crystalline grid.

In a simple model for two flexible polymers, each A chain occupies a connected set of sites, and each B chain is treated similarly. Let the specimen contain M sites, with a fraction φ occupied by A and the remainder by B. If an A chain occupies 100 sites, 10,000 A sites correspond to just 100 molecules that can be rearranged as connected objects. The mixing-entropy contribution consequently contains inverse chain lengths. This explains a common observation: small molecules receive a substantial entropic reward for mixing, whereas long chains receive less reward per occupied site. The same unfavourable contact energy can then overcome it more easily.

Mixing free energy per siteEq. 1

![Mixing free energy per site](https://ml-biomat.com/static/agent-math/81881ba39c97a13ea346f42f.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| g | Mixing free energy normalized by thermal energy per site | 1 |
| φ | Volume fraction of A; 1−φ is the fraction of B | 1 |
| ΔGmix | Gibbs free-energy change relative to separated pure components | J |
| M | Total number of reference sites | 1 |
| kB | Boltzmann constant, 1.380649×10⁻²³ | J K⁻¹ |
| T | Absolute temperature | K |
| NA, NB | Numbers of sites occupied by an A chain and a B chain | 1 |
| χ | Effective unlike-contact parameter in thermal-energy units | 1 |
| ln | Natural logarithm, base e; converts multiplication of independent arrangement counts into addition | 1 |

Reading the relationshipThe first two terms count arrangements of connected chains; dividing by chain length accounts for fewer independently placed molecules. The final term estimates contacts using the mean A–B neighbour probability φ(1−φ).

A worked exampleFor NA=NB=100, φ=0.50 and χ=0.01, g=0.01 ln(0.5)+0.0025=−0.004431. This value is dimensionless; multiplying by M kB T gives joules.

ConditionsMean-field lattice model of an incompressible binary flexible-chain mixture with a common reference-site volume and composition-independent χ. At a pure-component endpoint, use the limit φ lnφ→0.

The natural logarithm converts multiplication of arrangement counts into addition of entropy. If two independent choices each have several possibilities, their total number of combinations is the product of those counts; their entropies should add. A logarithm supplies exactly that relationship. A fraction between zero and one has a negative logarithm, so both combinatorial terms lower the mixing free energy. The interaction parameter χ expresses the average cost of unlike contacts relative to like contacts, measured in thermal-energy units. Positive χ penalizes unlike contacts in this model; negative χ favours them. An experimentally inferred effective χ can also incorporate local structure and noncombinatorial entropy, rather than representing a single bond energy.

For two polymers with 100 sites per chain, mixed in equal volume fractions, the two combinatorial terms sum to approximately −0.00693. With χ equal to 0.01, the contact term is 0.0025, giving a total of −0.00443. The uniform mixture therefore has a lower free energy than two completely pure components. However, the material has another option: two phases, each containing some of the other species. Their combined free energy may be even lower. A negative mixing free energy answers one comparison; full phase equilibrium requires comparing every allowed distribution of composition.

Chain length must therefore accompany any interpretation of χ. Increasing both chain lengths tenfold reduces the combinatorial terms tenfold, while the contact term per site remains unchanged. Molecular-scale miscibility becomes harder to maintain. Comparisons of χ and chain length between polymers must also use a consistent reference-site volume. Changing the volume represented by one segment changes both the count and the parameter, so one number cannot be compared independently of that convention. Formulations can improve unlike contacts through specific interactions, or employ compatibilizers that reside preferentially near an interface. A compatibilizer may reduce dispersed-domain size and strengthen interfacial bonding while leaving two phases present. A more useful blend and a thermodynamically single-phase material are separate, experimentally meaningful design goals.

## Reading phase separation from a free-energy curve

Plot the volume fraction of A horizontally and the mixing free energy per site vertically. The resulting curve compares possible organizations of the material. A uniform specimen is represented by one point. If the material separates into two compositions, its overall composition must remain fixed, and its free energy is the volume-weighted average of the two phase values. Geometrically, that average lies on the straight line joining the two points. If the line lies below the uniform-state curve at the overall composition, separating into those phases can lower the free energy.

Equilibrium coexistence is determined by a line tangent to the curve at two compositions: the common tangent. Tangency means that transferring a small amount of either component between the phases offers no further reduction in total free energy. Equivalently, each component has the same chemical potential in both phases. Chemical potential is the free-energy change caused by adding a small amount of a species at fixed temperature and pressure; it provides a thermodynamic criterion for migration. The tangent endpoints specify phase compositions. Overall composition determines the amount of each phase without changing those endpoints at a fixed temperature.

Suppose the coexisting phases have A fractions of 0.20 and 0.80. An overall fraction of 0.50 requires equal amounts of both phases. At an overall fraction of 0.35, the A-rich phase occupies one quarter and the A-poor phase three quarters: multiplying 0.80 by one quarter and 0.20 by three quarters gives a sum of 0.35. This lever rule expresses conservation of both components. Volume fractions can be weighted directly in an approximately incompressible model with a common reference-site volume. If actual mixing changes volume appreciably, an appropriate mass or amount-of-substance balance must be used instead.

A more local question asks whether a uniform state resists an extremely small composition fluctuation. Increase composition slightly in one region and decrease it in an adjacent region, preserving the overall amount. Where the free-energy curve bends upward, this perturbation raises the average free energy and is opposed. Where it bends downward, the same perturbation lowers free energy and has a driving force to grow. The second derivative describes this curvature. One derivative gives the local slope; a second asks how that slope changes with composition. Its sign distinguishes the two physical cases.

Local stability against small composition fluctuationsEq. 2

![Local stability against small composition fluctuations](https://ml-biomat.com/static/agent-math/8b51f3a95b06902b05caa1cd.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| g | Mixing free energy per site in thermal units | 1 |
| φ | A volume fraction; 1−φ is the B volume fraction | 1 |
| g″, d²g/dφ² | Second derivative of g with respect to φ, the free-energy curvature | 1 |
| NA, NB | Reference-site counts per chain of each species | 1 |
| χ | Composition-independent contact parameter | 1 |

Reading the relationshipDifferentiate the mixing free energy twice. For a small fluctuation that preserves overall composition, first-order changes cancel; the second-order contribution is set by curvature, positive for resistance and negative for growth.

A worked exampleAt NA=NB=100 and φ=0.5, g″=0.04−2χ. It is 0.02 for χ=0.01, −0.02 for χ=0.03, and zero for χ=0.02.

ConditionsTests local stability of a uniform state against infinitesimal composition perturbations. Global coexistence also requires a common tangent. A composition-dependent χ introduces additional derivatives.

The boundary of zero local curvature is the spinodal. The coexistence boundary found by the common tangent is the binodal. Between them, a uniform state resists small fluctuations but can be replaced by a sufficiently large nucleus of another phase: it is metastable. In the negative-curvature region, small composition fluctuations can grow, providing the thermodynamic condition for spinodal decomposition. Interfaces still cost energy, and diffusion still takes time. Local instability does not instantly divide a specimen into two large pieces. It identifies the initial driving force; pattern wavelength and growth rate additionally require spatial gradients and a law of motion.

Mean-field critical point of a binary blendEq. 3

![Mean-field critical point of a binary blend](https://ml-biomat.com/static/agent-math/d8ef7db9c5249446bcbf08d9.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| φc | A volume fraction at the critical point | 1 |
| χc | Critical contact parameter | 1 |
| NA, NB | Reference-site counts per chain of each species | 1 |
| √ | Square root; for example √100=10 | 1 |

Reading the relationshipAt the critical point, coexisting compositions merge and the second and third free-energy derivatives both vanish. The third derivative fixes composition; the zero-curvature condition then gives χc.

A worked exampleNA=NB=100 gives φc=0.5 and χc=0.02. For NA=100 and NB=400, φc=20/(10+20)=2/3 and χc=(0.1+0.05)²/2=0.01125.

ConditionsApplies to the binary incompressible Flory–Huggins mean-field model with composition-independent χ. Critical fluctuations and nonideal volume response affect quantitative phase diagrams.

For equal chain lengths, the critical composition is one half, and a chain length of 100 gives a critical χ of 0.02. Longer chains lower this threshold, consistent with the reduced combinatorial reward for mixing. At the critical point, the two coexisting compositions merge and composition fluctuations become correlated over increasingly large distances. The interaction below changes chain length and χ while displaying the free-energy curve and local curvature. Lengthen the chains at fixed χ, then increase χ at fixed chain length. These two operations show how reduced combinatorial benefit and increased contact cost can independently change stability.

[Figure: Free-energy curve for a symmetric polymer blend](https://ml-biomat.com/tutorials/biomaterials-courses/cp05/en/#en-s4)

Vary chain length, contact parameter and selected composition to inspect free energy, the common tangent and local curvature. Both species have equal chain lengths and χ is composition independent. Free energy is normalized per site in thermal units. Sliders change equilibrium comparisons rather than playing a dynamical trajectory.

## Allowing the melt to change volume: equations of state

The lattice model fills every site and treats total volume as unchanged by mixing. That makes the roles of connectivity and contacts particularly clear. Real liquids, however, expand on heating and compress under pressure. Their mixture volume may differ from the sum of the pure-component volumes. Available space around molecules affects motion and contacts, so volume response can contribute to mixing free energy rather than remaining an incidental experimental number. In polymer blends, it can change how temperature and pressure influence miscibility.

An equation of state relates pressure, volume and temperature. For a fixed amount of one substance, measurements of volume at different temperatures and pressures establish its volumetric response. The thermal expansion coefficient gives the fractional volume increase per degree of heating. The compressibility gives the fractional volume decrease for an increase in pressure. Fractional change is important: a large vessel naturally undergoes a larger absolute volume change than a drop of the same material. Dividing by the original volume allows the material property to be compared independently of specimen size.

Volume response to temperature and pressureEq. 4

![Volume response to temperature and pressure](https://ml-biomat.com/static/agent-math/0199891444a751fbe2e57666.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| αP | Volumetric thermal expansion coefficient at constant pressure | K⁻¹ |
| κT | Isothermal compressibility | Pa⁻¹ |
| V | Specimen volume for a fixed amount of substance | m³ |
| T | Absolute temperature | K |
| P | Pressure | Pa |
| ∂V/∂T, ∂V/∂P | Partial derivatives: local rates of volume change while holding the subscripted variable fixed | m³ K⁻¹ and m³ Pa⁻¹, respectively |

Reading the relationshipDivision by volume gives fractional change. An ordinary stable liquid contracts under pressure, so the minus sign makes compressibility positive. A partial derivative specifies that only one control variable changes.

A worked exampleIf αP=5×10⁻⁴ K⁻¹, heating by 10 K gives an approximately 0.5% volume increase when the coefficient is nearly constant. If κT=5×10⁻¹⁰ Pa⁻¹, adding 10 MPa gives an approximately 0.5% decrease.

ConditionsThe definitions describe local response. The examples use small-change linear approximations at fixed amount of substance without crossing a phase transition.

In his liquid-state work of the 1960s, Flory incorporated pure-component volume and thermal responses into mixture calculations, extending a description based on lattice combinations and a contact parameter. The idea is to describe how each pure liquid changes with temperature and pressure before asking how mixing perturbs those states. A small mixing-volume change therefore does not by itself imply a zero noncombinatorial entropy contribution. Different component responses to temperature and pressure can still alter free energy and shift phase equilibrium.

It is useful here to avoid picturing free volume as a permanent array of holes. Molecules keep moving, and locally available space changes with them. Free volume is an effective description of available motion in particular models, with a definition that depends on the theory. Drawing it as fixed bubbles can suggest that an ordinary dense melt consists of solid polymer and vacuum pores. The directly measurable quantities are total volume, expansion, compression and changes on mixing. Those data constrain whichever liquid model is being used.

One familiar temperature trend is improved mixing on heating: thermal motion gives the combinatorial contribution greater importance, and the mixture becomes single-phase above an upper critical solution temperature. Other systems separate on heating and exhibit a lower critical solution temperature. Their behaviour can involve temperature-dependent specific interactions, solvation, volume response and noncombinatorial entropy, with the mechanism depending on chemistry. Always writing χ as a positive constant divided by temperature builds one type of temperature dependence into the model in advance. Examine the measured phase diagram first, and state whether the effective parameter depends on temperature, pressure and composition.

For practical interpretation, the fixed-lattice result answers a first question: do chain length and unlike contacts explain the main trend? If temperature or pressure effects require more detail, pure-component pressure–volume–temperature data and mixing-volume measurements add independent constraints. Additional complexity then has a defined purpose. Each extra parameter corresponds to a physical response that can be discussed and measured, rather than serving only to bring one fitted curve closer to one collection of data points.

## Why connected blocks form microphases

Now replace two independent molecular species with A and B blocks belonging to the same molecule. Unlike contacts can still raise free energy, and configurational freedom remains important. Macroscopic separation, however, meets an unavoidable constraint: every A block is tethered to a B block. If all A material moved to one side of the specimen and all B material to the other, almost every chain would need to reach the interface from inside those regions. That arrangement becomes impossible to sustain as specimen size increases. A workable organization repeats A-rich and B-rich regions over finite distances, placing most junctions near their interfaces.

This finite-scale separation is microphase separation. It differs from small droplets temporarily arrested by rapidly cooling an ordinary blend. Under suitable conditions, block connectivity allows an ordered structure with a finite spacing to be an equilibrium arrangement. In a symmetric diblock, similar block volume fractions suit alternating layers. When one block occupies less volume, minority cylinders or spheres can distribute space and stretching more effectively. Other compositions and conditions permit interconnected curved networks. Selecting a morphology requires comparing several free-energy contributions, rather than deciding which drawing looks most regular.

The central competition setting the size is between interfacial cost and chain stretching. Combining small domains into larger ones reduces A–B interface per unit volume and lowers its contact cost. Thicker domains, however, require chains attached near the interface to stretch further to fill the interior, reducing their accessible conformations. Very fine structures have excessive interface; very coarse structures require excessive stretching. An intermediate period can therefore minimize free energy. This converts a molecular connectivity constraint into a route for designing structures on scales of tens of nanometres, with the actual dimension dependent on chain length, stiffness and interactions.

[Figure: Competition of interfacial area and chain stretching in lamellae](https://ml-biomat.com/tutorials/biomaterials-courses/cp05/en/#en-s6)

Figure 2 · Green and orange represent regions enriched in different blocks; dark points mark junctions. Fine layers have more interface per volume, whereas coarse layers require chains to reach farther from the interface. Balancing the costs can select a finite period.

In 1980, Leibler analysed composition fluctuations in a uniform diblock melt according to their spatial wavelength. An ordinary blend can favour separation over ever larger distances, while a diblock can respond most strongly near a finite wavelength. A regular spacing thus becomes a calculable stability question. For an equal-volume, statistically symmetric diblock in mean-field theory, a familiar reference is the disordered-state instability near χN = 10.495. Here N counts the entire diblock chain using a consistent reference-segment volume. Fluctuations, finite chain length and asymmetry affect the actual order–disorder transition, so the model must accompany the number.

A segregation-strength reference for symmetric diblocksEq. 5

![A segregation-strength reference for symmetric diblocks](https://ml-biomat.com/static/agent-math/b6d9d329fe9d13ffe87ee2be.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Λ | Segregation strength on the whole-chain scale | 1 |
| χ | A–B interaction parameter for the chosen reference segment | 1 |
| N | Number of reference segments in the entire AB chain, the sum for both blocks | 1 |
| ΛMF | Mean-field disordered-state instability threshold for a statistically symmetric diblock; MF means mean field | 1 |
| ≃ | Approximately equal under the specified model and approximation | 1 |

Reading the relationshipχ measures a contact penalty at the reference-segment scale; multiplying by chain length gives its whole-chain strength. The value 10.495 comes from mean-field stability analysis of symmetric-diblock composition fluctuations.

A worked exampleFor χ=0.02 and N=400, Λ=8. Increasing N to 600 at unchanged χ gives Λ=12, above this mean-field reference.

ConditionsIncompressible diblock melt with equal A and B volume fractions and symmetric chain statistics. Fluctuations, finite chain length and asymmetry affect the actual order–disorder transition.

This also explains why χ alone is insufficient. A local contact preference accumulates along a chain, making longer chains more prone to distinct compositional domains. Longer chains also often move more slowly, so reaching an ordered state can require longer annealing. Thermoplastic elastomers exploit this organization by using harder domains as reversible physical junctions and softer connecting segments to permit deformation. Heating can soften the hard regions or alter their organization, enabling processing. Microphase separation supplies the structural basis; service temperature and recovery also depend on glass transitions, crystallization and the stability of the connecting domains.

Scattering helps identify the structure. A larger spatial period generally places its principal peak at a smaller scattering-vector magnitude. Relative positions of several peaks can distinguish candidate organizations such as layers and cylinders. Microscopy provides local geometry, but circles in a two-dimensional section may represent spheres or cross-sections through cylinders. Combining the overall periodicity measured by scattering with local images turns an observation of stripes or spots into an evidence-based interpretation of three-dimensional organization.

## How a long chain enters a thin crystal

Slowly cooling a crystallizable polymer melt allows some chain segments to develop regular packing. Order can provide more favourable contacts and packing between neighbours, but it also reduces the conformations available to the chain. Crystallization is therefore another competition between energy and entropy. At high temperature, the melt receives a strong free-energy benefit from configurational freedom. At sufficiently lower temperature, favourable crystalline packing can prevail. Chemical structure must also permit repeated ordering: side-group regularity, branching and copolymer sequence can all alter that ability.

Polymer crystallization posed a geometrical puzzle. A molecule can be very long, while a polymer single crystal can be a thin platelet. In 1957, Keller combined electron microscopy with selected-area electron diffraction to investigate polyethylene platelets. Microscopy established the shape; diffraction established the direction of chain axes within the lattice. Together they indicated that the axes ran mainly through the platelet thickness even though molecular contour lengths were much greater. This strongly supported chain folding: a molecule could cross the platelet, turn back and enter the ordered region again. Related studies by Fischer and Till in the same year also advanced this understanding.

[Figure: Platelet geometry and chain-axis reasoning associated with Keller’s study](https://ml-biomat.com/tutorials/biomaterials-courses/cp05/en/#en-s7)

Figure 3 · Keller’s 1957 study combined platelet shape with electron-diffraction orientation. A thickness far smaller than molecular contour length, with chain axes crossing the thickness, supports chain folding. Here ℓ marks thickness; real surfaces can also contain loops, chain ends and segments entering amorphous regions.

A folded-chain drawing need not mean that every molecule makes identical, tightly spaced hairpin turns. Crystal surfaces can contain loops of different sizes, chain ends and segments extending into amorphous regions, depending on formation conditions. The important geometrical conclusion is that one long molecule can contribute several crystalline stems while linking crystalline and amorphous regions. Tie chains joining different lamellae help transmit load. Toughness therefore depends on amorphous material and effective intercrystalline connections as well as the crystalline fraction itself.

For a quantitative comparison, define the free-energy reduction per unit volume on converting melt into a large crystal. Near the equilibrium melting temperature, treating the fusion enthalpy and entropy as approximately constant gives a driving force that rises approximately linearly with undercooling. Lower temperature below the equilibrium melting point generally increases the bulk reward for crystallization. Yet a new crystal must also create surfaces. Their area is particularly large relative to volume for a small crystal, creating an interfacial cost that initially opposes its formation.

Bulk crystallization benefit from undercoolingEq. 6

![Bulk crystallization benefit from undercooling](https://ml-biomat.com/static/agent-math/25b01084f54b0d6896157a81.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Δgv | Melt free-energy density minus crystal free-energy density, positive when crystallization is favoured | J m⁻³ |
| Δhf | Fusion enthalpy per unit volume near the equilibrium melting point | J m⁻³ |
| T | Absolute specimen temperature | K |
| Tm∞ | Equilibrium melting temperature of a bulk crystal with negligible surface effects | K |
| ≃ | Approximately equal | 1 |

Reading the relationshipThe free-energy difference equals the enthalpy difference minus temperature times the entropy difference. Equality of bulk phase free energies at melting expresses fusion entropy as fusion enthalpy divided by melting temperature, giving the linear undercooling approximation.

A worked exampleWith Δhf=1×10⁸ J m⁻³, Tm∞=400 K and T=360 K, Δgv=1×10⁷ J m⁻³. At 340 K, the estimate is 1.5×10⁷ J m⁻³.

ConditionsNear the equilibrium melting point, neglecting enthalpy and entropy changes caused by heat-capacity differences and using a consistent volume basis.

Consider a thin lamella whose broad-face area is much larger than its squared thickness, and retain the cost of its two fold surfaces. Crystal volume per unit broad-face area equals the thickness. The bulk free-energy benefit therefore increases with thickness, while the two-surface cost remains constant in this simplified comparison. Their sum explains why a very thin crystal is less stable near the bulk melting point than a thick one. This is an equilibrium surface correction. It has not yet determined which thickness a real growth process will select.

Bulk and surface contributions of a lamellaEq. 7

![Bulk and surface contributions of a lamella](https://ml-biomat.com/static/agent-math/48ac3bced10b427a03dc2a54.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ΔGlam | Free-energy change on forming a lamella from melt | J |
| A | Area of one broad lamellar face | m² |
| ℓ | Lamellar thickness | m |
| Δgv | Bulk free-energy benefit per unit crystal volume | J m⁻³ |
| σe | Free energy per unit area of one fold surface | J m⁻² |

Reading the relationshipVolume equals area times thickness, so the bulk contribution per area is −ℓΔgv. Two broad faces each contribute σe, giving 2σe. A negative total favours formation of that lamella.

A worked exampleFor ℓ=10 nm=1×10⁻⁸ m, Δgv=1×10⁷ J m⁻³ and σe=0.05 J m⁻², the sum is −0.1+0.1=0 J m⁻². At 20 nm it is −0.1 J m⁻².

ConditionsFlat lamella with two equivalent broad faces, neglecting relatively small edge and strain contributions. This equilibrium comparison does not determine nucleation rate or growth-selected thickness.

After cooling, many polymers contain lamellae growing outward from nucleation sites and collectively forming spherulites. Their bright and dark textures under crossed polarizers reflect the anisotropic optical response of ordered material. A roughly spherical overall organization does not mean that every chain lies fully extended along a radius. Amorphous layers separate lamellae, and the lamellae can branch and twist. Together they form a texture visible at a larger scale. Crystal lattice, lamella and spherulite are different structural levels; a single unspecified “crystal size” can combine mechanisms that need to be distinguished.

## Connecting equilibrium structure to real materials

Equating the bulk reward of a thin crystal with its surface cost gives a thickness-dependent melting temperature. Thinner lamellae carry a larger fold-surface contribution per unit crystal volume and consequently melt at a lower temperature. This is the lamellar form of the Gibbs–Thomson relation. It links an accessible thermal observation to a structural scale that is harder to measure separately for every lamella. The same chemical polymer can therefore show different melting behaviour when its lamellar thickness distribution changes.

Lamellar thickness and melting temperatureEq. 8

![Lamellar thickness and melting temperature](https://ml-biomat.com/static/agent-math/0f061297046f50a2eee9200a.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Tm(ℓ) | Melting temperature of a lamella of thickness ℓ | K |
| Tm∞ | Bulk equilibrium melting temperature with negligible surface effects | K |
| ℓ | Lamellar thickness | m |
| σe | Fold-surface free energy per area | J m⁻² |
| Δhf | Fusion enthalpy per volume | J m⁻³ |
| ≃ | Approximately equal within the surface-correction model | 1 |

Reading the relationshipBalance the bulk reward against the two fold-surface costs and substitute the linear undercooling relation. The ratio of σe to ℓΔhf is dimensionless; greater surface cost or smaller thickness lowers melting temperature.

A worked exampleFor Tm∞=400 K, σe=0.05 J m⁻² and Δhf=10⁸ J m⁻³, ℓ=10 nm gives 360 K and ℓ=20 nm gives 380 K. The large-thickness limit approaches 400 K.

ConditionsLamellar surface-equilibrium approximation with absolute temperature and parameters for a consistent crystal form. Recrystallization during heating, defects and distributions require experiment-specific interpretation.

As an illustrative calculation, take a bulk melting temperature of 400 K, a volumetric fusion enthalpy of one hundred million joules per cubic metre, and a fold-surface free energy of 0.05 joules per square metre. At a thickness of 10 nanometres, the fractional surface correction is 0.10, giving an estimated melting temperature of 360 K. At 20 nanometres, the correction halves and the estimate becomes 380 K. Absolute temperature is required because the temperature factor in free energy starts at the thermodynamic zero; substituting Celsius values into the ratio would be incorrect. These numbers demonstrate the thickness effect. A particular polymer requires its own parameters and consistent definitions of the crystal surfaces.

[Figure: Thickness-dependent melting in the lamellar Gibbs–Thomson model](https://ml-biomat.com/tutorials/biomaterials-courses/cp05/en/#en-s8)

Figure 4 · Calculated with the example parameters: bulk melting point 400 K, fold-surface free energy 0.05 J m⁻², and volumetric fusion enthalpy 10⁸ J m⁻³. Thickness and absolute temperature are plotted. The curve represents a surface correction without heating-induced reorganization kinetics.

Differential scanning calorimetry observes melting and crystallization through the heat flow needed to maintain the specimen and a reference on the same heating program. Dividing the net heat under a melting peak by specimen mass gives a specific fusion enthalpy. Comparing it with a fully crystalline reference of the same crystal form estimates crystallinity. If cold crystallization occurs during heating, some initially disordered material forms new crystals and subsequently contributes to melting absorption. Its crystallization heat must therefore be subtracted when estimating initial crystallinity. A specimen containing filler or other components also requires normalization by the mass fraction of the polymer being examined.

Two melting peaks need not indicate two different polymers. Different lamellar thicknesses can melt separately, crystals can reorganize during heating, and more than one crystal form may be present. Similarly, two glass transitions in a blend commonly indicate amorphous regions with different local mobility, but their positions and resolution also depend on mutual dissolution, interfacial fraction and measurement frequency. Interpret an experimental signal through the quantity actually measured, then combine it with scattering or morphology. This avoids mechanically assigning one structural label to every observed peak.

Blending, microphase separation and crystallization can also compete within one specimen. A component that crystallizes first may reject another component into the amorphous material and change the composition of the remaining melt. Microphase separation occurring first may confine a crystallizable block to thin layers or small domains, altering nucleation and growth. Formulation supplies the molecules, while cooling sequence determines the structural path they follow. Record temperature history and holding times, and observe compositional separation and crystal formation separately, to establish how an earlier organization influences a later one.

A concrete design problem brings these ideas together: a film should remain soft yet retain its shape at its service temperature. First consider whether soft and hard components have contacts favourable enough for uniform mixing, then whether a separate hard phase is needed to provide connections. With block connectivity, examine domain spacing and hard-domain stability. With crystalline reinforcement, examine lamellae, crystallinity and tie chains, comparing the target temperature with the actual melting range. This approach assigns a physical task and measurable quantities to each structural option rather than assuming one organization is best in advance.

Connectivity runs through the complete picture. It reduces the independent-molecule mixing entropy, prevents macroscopic separation of tethered blocks, links crystals through amorphous segments, and makes structural change take appreciable time. A material can simultaneously contain nearly ideal large-scale chain conformations, distinct compositional domains and locally ordered crystal lattices. Each description answers a question at a different scale. Connecting chain, domain, lamella and macroscopic property turns “can these polymers be mixed?” into “how can these molecules be organized into a material that performs a particular task?”
