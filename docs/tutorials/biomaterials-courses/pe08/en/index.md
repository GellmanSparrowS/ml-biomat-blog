# From Molecular Connections to Material Behaviour: Making Polyesters, Polyurethanes and Polyolefins

Source: https://ml-biomat.com/tutorials/biomaterials-courses/pe08/en/
Language: en

Why do clothes, cushions and pipes need different molecular connections? Count reactive groups, follow chain growth in polycondensation and the formation of polyurethane elastomers and foams, then enter catalysts and particles to see how reaction and diffusion shape materials.

## Three ways of connecting molecules, seen in clothes, cushions and pipes

A polyester shirt, a sofa cushion and a plastic water pipe appear to have little in common. The shirt needs material that can be spun into fine fibres, the cushion must compress and recover, and the pipe must retain its shape while carrying internal pressure for a long time. Long molecular chains lie behind all three, but chain length is only the beginning of the explanation. The connections within a chain, the remaining reactive groups, the arrangement of side groups and the combination of mobile and fixed regions all influence performance. These differences also explain why manufacture requires different reactors, separation steps and ways of measuring ingredients.

Imagine a molecule as a component with particular connection points. These are **functional groups**, groups of atoms with characteristic chemical reactivity. A hydroxyl group contains oxygen and hydrogen and is written —OH; a carboxyl group is —COOH; an amino group is —NH₂. A component with two suitable connections can join a linear chain, whereas three or more provide opportunities for branching. Functionality counts the groups able to participate in the particular reaction being considered. It does not count every atom in the molecule, and several oxygen atoms do not necessarily mean several reactive connections. Temperature, catalysts and the surrounding molecular structure also affect whether a group reacts.

In **step growth**, monomers can join monomers, short chains can join short chains, and longer chains can continue joining through their ends. Polycondensation belongs to this broad class and commonly produces small molecules such as water, methanol or ethylene glycol. Step-growth polyaddition also joins complementary groups, but its principal bond-forming step releases no small molecule. The reaction of isocyanate and hydroxyl groups in polyurethane formation is an example. Coordination polymerization, by contrast, commonly involves chain growth: monomers arrive at a metal active centre and insert successively into the growing metal–carbon bond. Whether small molecules are released and how a chain grows are therefore separate questions.

A surprising feature of step growth is that an apparently advanced reaction can still leave fairly short average chains. Start with one thousand bifunctional components and allow each connection to join two previously separate molecules. Every successful connection reduces the molecular count by one while preserving the number of components. After nine hundred connections, one hundred molecules remain, containing an average of ten components each. Another ninety connections leave ten molecules with an average length of one hundred. Counting this way makes high conversion concrete: the small fraction of groups still unconnected can determine whether average chain length increases by another order of magnitude.

Mean chain length from molecular countingEq. 1

![Mean chain length from molecular counting](https://ml-biomat.com/static/agent-math/ae3c0ca9dfefe52aa1144845.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| X_{n} | Number-average degree of polymerization, counting each original bifunctional component as one unit | 1 |
| N_{0}, N | Initial component count and remaining molecule count, excluding released condensate molecules | 1 |
| p | Fraction of functional groups reacted in the balanced bifunctional system | 1 |

Reading the relationshipEach intermolecular connection reduces molecular count while preserving component count. N₀(1−p) molecules remain; dividing total components by that count gives the mean size.

A worked exampleWith N₀=1000 and p=0.90, 100 molecules remain and X_n=10. At p=0.99, 10 remain and X_n=100. Conversion here counts reacted groups, not the fraction of original monomer molecules that have disappeared.

ConditionsLinear bifunctional components with balanced complementary groups, or AB components; intermolecular linking without cyclization, scission or monofunctional capping. Acid and alcohol residues each count as a unit, so a chemical repeat may contain two units.

[Carothers discussed polymers and polyfunctionality in 1936](https://pubs.rsc.org/en/content/articlehtml/1936/tf/tf9363200039), connecting the number of reactive groups with the formation of large molecules. In the same year, Flory investigated molecular-size distributions in linear condensation polymers. Such work moved synthesis beyond obtaining a viscous substance towards explaining its molecular population and chain lengths. The diagram below makes the counting visible. New lines represent chemical bonds, and components remain identifiable within a chain; they have not simply accumulated into an unconnected cluster.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe08/en/#en-s1)

Figure 1 · From 8 components to 2 chains: each intermolecular link removes one molecule from the count. Carothers and Flory’s 1936 work connected functionality and molecular populations with step growth. Equal-sized chains illustrate the counting; a real reaction produces a distribution.

The counting basis for degree of polymerization must also be stated. For a component carrying both complementary groups, one component may correspond to one structural unit. For a diacid and a diol, however, the acid residue and alcohol residue each count as a component in the argument above, while a complete chemical repeat commonly contains both. Converting degree of polymerization into molar mass therefore requires the mean residue mass appropriate to this convention, together with end-group contributions. Otherwise, a correct conversion calculation can still produce a molar mass that is wrong by approximately a factor of two.

## Why polyester chain growth depends on removing small molecules

Polyethylene terephthalate, usually abbreviated PET, is used in polyester textiles and many transparent beverage bottles. Its name points to its two building components: terephthalic acid supplies two carboxyl groups, and ethylene glycol supplies two hydroxyl groups. Ethylene glycol has one hydroxyl at each end and can connect different acid components. Ordinary ethanol has only one hydroxyl and acts more like an end cap in this reaction; it cannot replace ethylene glycol as the connecting diol. Aromatic rings give parts of the chain rigidity, while ester connections link them into long molecules that can later be stretched, oriented and crystallized.

Locally, a carboxyl group reacts with a hydroxyl group to form an ester connection and water. The reverse process is possible too: water participates in ester hydrolysis and breaks a connection. Chemical equilibrium means that the average forward and reverse rates are equal under the specified conditions, rather than that molecular activity has stopped. Continuously removing water changes the composition and allows further ester formation. Clearing away a component that enables the reverse process is a useful analogy, but water does not mechanically block a connector; chemical potentials determine the reaction's tendency.

Esterification equilibrium and removal of waterEq. 2

![Esterification equilibrium and removal of water](https://ml-biomat.com/static/agent-math/df59ac80f018ec443aa0a461.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| R, R′ | Organic residues not drawn in full; the prime distinguishes the two residues | 1 |
| COOH, OH, COO | Chemical notation for carboxyl, hydroxyl and ester connections | 1 |
| H₂O | Water; subscript 2 denotes two hydrogen atoms | 1 |
| ⇌, K | Reversible reaction; equilibrium constant at a specified temperature and standard states | 1 |
| a_{ester}, a_{water}, a_{acid}, a_{alcohol} | Activities of ester, water, acid and alcohol relative to their standard states | 1 |

Reading the relationshipAt equilibrium the product-to-reactant activity ratio equals K. Removing water initially lowers this ratio and allows further esterification. A catalyst primarily changes the rate of approaching equilibrium.

A worked exampleFor an illustrative K=4, ester and water activities of 0.8 and 0.2 and acid and alcohol activities of 0.2 give a ratio of 4. Reducing water activity to 0.02 before other values adjust gives 0.4, driving further compositional change.

ConditionsA local esterification step; real polyester systems include different end groups and ester interchange. Activity depends on composition and interactions and cannot generally be replaced by mass fraction. Water removal also requires transport.

Two common feed routes illustrate this chemistry. Direct esterification begins with terephthalic acid and ethylene glycol, producing hydroxylethyl-ended oligomers while removing water. The alternative starts from dimethyl terephthalate, which undergoes ester interchange with ethylene glycol and releases methanol. Bis(2-hydroxyethyl) terephthalate, abbreviated BHET, is a useful intermediate structure to recognize. An industrial continuous esterification stream, however, generally contains oligomers with different lengths and end groups, and subsequent processing need not isolate pure BHET. Further polycondensation joins reactive ends through reactions including ester interchange, releasing ethylene glycol for removal.

As chains grow, the melt becomes more viscous, and a second difficulty joins the need for reactive ends to meet: small molecules must escape. A bubble rising slowly through thick syrup helps convey the difficulty of transport, but in a polyester melt ethylene glycol must also migrate molecularly through liquid to a gas–liquid interface. Lowering gas pressure can reduce the interfacial concentration of the volatile component and increase the outward driving force. Spreading the melt into thinner films and continually renewing its surface shortens the internal transport distance. Vacuum and surface renewal therefore address different aspects of the same removal task and are often used together.

To describe this migration quantitatively, first count how many molecules occupy a specified volume. The mole is a chemical counting unit containing approximately 6.022 × 10²³ specified entities; for ethylene glycol, those entities are ethylene-glycol molecules. Molar mass gives the mass of one mole, so dividing mass by molar mass gives the amount in moles. Dividing that amount by volume gives the amount concentration. For example, 100 moles of one component in a cubic metre of liquid corresponds to 100 mol/m³. This counts the chosen component, rather than every molecule in the liquid. Comparing its concentration inside the melt with that near the surface provides a way to describe the outward driving force.

Driving force and travel distance both affect removalEq. 3

![Driving force and travel distance both affect removal](https://ml-biomat.com/static/agent-math/8eb192705efc27ba0ff60c8d.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| J | Net outward molar flux from bulk liquid to its surface | mol m⁻² s⁻¹ |
| k_{L} | Mass-transfer coefficient based on liquid concentration difference | m s⁻¹ |
| c_{b}, c_{s} | Small-molecule concentrations in bulk liquid and at the liquid-side surface | mol m⁻³ |
| t_{D} | Characteristic diffusion time over distance L | s |
| L, D | Representative diffusion distance and diffusivity | m; m² s⁻¹ |
| ∼, L² | Order-of-magnitude scaling; distance multiplied by itself | 1; m² |

Reading the relationshipThe concentration difference drives transport, and the coefficient converts it to molar amount per area per time. Diffusive distance grows with the square root of time, giving a time scale proportional to distance squared.

A worked exampleWith k_L=10⁻⁵ m/s and c_b−c_s=100 mol/m³, J=10⁻³ mol/(m²·s). For D=10⁻¹⁰ m²/s, L=1 mm gives a time scale of 10000 s, whereas L=0.1 mm gives 100 s.

ConditionsLocal mass-transfer description and a diffusion-dominated time-scale estimate, not a complete devolatilization time. Convection, surface renewal, phase equilibrium and composition-dependent diffusivity influence the actual process.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe08/en/#en-s2)

Figure 2 · Early mixing and later surface renewal serve different duties. The lower comparison shows the time-scale change for a tenfold shorter diffusion path. Geometry is illustrative; equipment and conditions depend on the process.

Staging the reactors now has a physical explanation. Early material flows relatively easily, allowing stirred vessels to provide mixing and prepolycondensation. Later horizontal, disc or film-forming equipment can continually expose new surfaces in the viscous material. Heating must maintain the required melt state and support evaporation, while excessive high-temperature exposure increases opportunities for chain scission, colour formation and other secondary chemistry. A catalyst accelerates bond formation but cannot replace removal of small molecules. Adding more catalyst therefore does not automatically overcome a transport limitation.

Some products undergo **solid-state polycondensation**. The polymer is first made into sufficiently crystallized pellets and then treated below the melting region, at a temperature that still permits segmental movement in amorphous regions. Dry inert gas or vacuum removes the reaction products. Solid state describes the pellet retaining its overall shape; it does not mean that all chain segments are immobile or that end groups can no longer meet. Large pellets create longer internal diffusion paths, whereas insufficiently stable pellets can stick together. Temperature, crystallinity, particle size and gas conditions must consequently work together to preserve pellet form while increasing chain length.

Water becomes important again during subsequent processing. PET pellets need controlled moisture content before remelting because hydrolysis at elevated temperature can shorten chains that were carefully built during synthesis, changing melt viscosity and product behaviour. Water removal during esterification, ethylene-glycol removal during polycondensation and drying before processing occur in different equipment, yet all help create and preserve the intended molecular connections. Whether the final object is a transparent bottle or an oriented crystalline fibre additionally depends on cooling, stretching and chain organization; the name PET alone does not determine its morphology.

## Balancing nylon end groups and scheduling a second connection in polyester

The two sixes in nylon 66 refer to the six carbon atoms in hexamethylenediamine and the six in adipic acid. Amino groups at the diamine's ends react with carboxyl groups at the acid's ends to form amide connections and release water. The diamine here is hexamethylenediamine, rather than the two-carbon ethylenediamine. Amide groups also participate in hydrogen bonding between chains. Long covalent chains, intermolecular interactions and later orientation together help fibres carry tensile loads, while repeated bending depends on segmental mobility and internal organization as well.

Equal numbers of complementary groups matter more than equal ingredient masses. Adipic acid and hexamethylenediamine have different molar masses, so one kilogram of each does not provide equal carboxyl and amino populations. Divide each ingredient mass by its own molar mass, then multiply by the relevant number of groups per molecule to compare the molar amounts of carboxyl and amino groups. Preparing nylon salt of controlled composition, and measuring its acid–base balance, helps turn this molecular requirement into a manageable intermediate that can be measured and transported.

A slight excess of one group type can leave enough unmatched chain ends to limit growth. In the following expression, A denotes the less abundant group and B the more abundant, so their initial ratio never exceeds one. Conversion is defined for the limiting A groups. Even when almost all A groups react, excess B groups remain. Raw-material evaporation, monofunctional impurities and side reactions involving end groups can therefore alter the effective balance. An accurate initial weighing is important, but it is not the whole history of the groups available during polymerization.

How group imbalance limits chain lengthEq. 4

![How group imbalance limits chain length](https://ml-biomat.com/static/agent-math/8648e704fda97e97b38d731f.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| N_{A,0}, N_{B,0} | Initial counts of limiting A and excess B groups; 0 indicates the initial state | 1 |
| r | Initial complementary-group ratio | 1 |
| p_{A} | Fraction of A groups reacted | 1 |
| X_{n} | Number-average degree of polymerization in original bifunctional-component units | 1 |

Reading the relationshipInitial molecular count is half the total group count. Reacted A groups count intermolecular connections. Dividing the initial component count by the remaining molecular count gives the result.

A worked exampleAt r=1 and p_A=0.99, X_n=100. With r=0.98 at the same conversion, X_n=50. Even as p_A approaches 1, the limiting mean length at r=0.98 is 99.

ConditionsBifunctional AA and BB components with only A–B linking and no cyclization, scission or extra capping. Losses and impurities alter effective group counts; at equal amounts the expression reduces to 1/(1−p_A).

### High conversion, but how long are the chains?

[Figure: High conversion, but how long are the chains?](https://ml-biomat.com/tutorials/biomaterials-courses/pe08/en/#en-s3)

Linear bifunctional AA/BB system without cyclization or extra capping. Teal uses the selected group ratio; orange uses balanced groups. Mean length counts original molecular components. Vertical intervals are tenfold and horizontal values are conversion percentages.

First keep the complementary group numbers equal and move conversion from ninety-nine to ninety-nine point nine percent. Then set the group ratio to 0.98 and examine the restriction at high conversion. The displayed degree of polymerization is the average number of original components per molecule, rather than the compulsory length of every individual molecule. Applied to nylon production, this calculation explains why water removal, end-group analysis and recovery of volatile components belong together. Removing water supports further reaction, whereas losing diamine with the vapour can shift an initially suitable group balance.

Nylon salt solution is commonly concentrated before forming oligomers under controlled temperature and pressure, followed by progressive pressure reduction, water removal and further polycondensation. Retaining pressure early can limit rapid loss of water and volatile ingredients; removing water later supports higher conversion. Exact temperature, pressure and residence time depend on equipment, end-group targets and product grade. The useful way to read the process is to ask why conditions change from one stage to the next. Solid-state post-treatment can provide further chain growth when required while preserving pellet form.

Unsaturated polyester separates two connection tasks. First, diacids or anhydrides react with diols to form relatively short ester-containing chains, incorporating carbon–carbon double bonds through components such as maleic or fumaric structures. Second, those double bonds participate in radical reactions with a reactive diluent such as styrene, establishing connections between polyester chains. Styrene reduces viscosity before cure and becomes part of the network during cure; it is therefore not an ordinary solvent intended to evaporate completely. This sequence lets a resin wet glass fibres while fluid and then form a load-bearing body in the mould.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe08/en/#en-s3)

Figure 3 · Complementary groups explain nylon stoichiometry above; the lower diagram shows a second reaction connecting unsaturated polyester chains. Dots and dashed lines identify sites and connectivity, not a full mechanism or actual network morphology.

Peroxides supply radicals, suitable promoter systems alter radical-generation rates, and oxygen can slow cure near an exposed surface. Temperature, formulation, thickness and heat removal together determine gelation and subsequent curing. Gelation marks the emergence of a network spanning the sample and the loss of ordinary sustained liquid flow; many double bonds can still remain unreacted. Glass fibres carry substantial tensile load, while cured resin positions the fibres and transfers stress between them. Wetting and interface quality are therefore as important as simply completing a chemical reaction. The sequence of oligomer formation followed by network formation matches the practical need to shape first and carry loads afterwards.

## Why polyurethane formulation counts hydroxyl groups as well as mass

Polyurethane can appear as a shoe-sole elastomer, a flexible foam or a hard coating. Its common chemical feature is the urethane connection, usually formed by reacting an isocyanate group, —NCO, with a hydroxyl group, —OH. Carbon, nitrogen and oxygen in the isocyanate group are bonded in a particular arrangement; reaction with an alcohol reorganizes atoms into a new connection without releasing water in the principal bond-forming step. A molecule carrying two isocyanates and another carrying two hydroxyls can build a linear chain through repeated reactions. Higher functionality provides additional opportunities for branching and network formation.

Hydroxyl and amino groups form different connectionsEq. 5

![Hydroxyl and amino groups form different connections](https://ml-biomat.com/static/agent-math/e3817df10c7916b4d753f386.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| R, R′ | Organic residues preserved on the corresponding sides of the reaction | 1 |
| NCO, OH, NH₂ | Isocyanate, hydroxyl and primary amino groups | 1 |
| NH–CO–O, NH–CO–NH | Urethane and urea connections; carbon and oxygen in CO are double bonded | 1 |
| → | Direction of the net bond-forming reaction shown | 1 |

Reading the relationshipBoth reactions incorporate the existing atoms. Alcohol supplies an oxygen-side connection, while amine supplies a nitrogen-side connection. The corresponding residues remain, without release of a condensate in these principal steps.

A worked exampleThrough the first route, 0.10 mol hydroxyl consumes 0.10 mol NCO and forms 0.10 mol urethane connections. Through the second principal route, 0.10 mol primary amino groups similarly consumes 0.10 mol NCO to form urea connections.

ConditionsLocal reactions without specifying whether residues belong to long chains. Multifunctional components can continue reacting; subsequent reactions of existing urethane or urea with NCO require separate accounting.

[Otto Bayer's 1947 paper on diisocyanate polyaddition](https://onlinelibrary.wiley.com/doi/10.1002/ange.19470590901) described this synthetic approach, with associated early patent work dating to 1937. The conceptual change was that long-chain synthesis could use complementary groups that add directly, without requiring a condensate to be continually removed at each principal connection. Molecular structure, functionality and group balance became powerful ways to alter material form. The same underlying reaction could be organized into linear molecules, chains with soft and hard segments, or three-dimensional networks, rather than producing one material with a fixed set of properties.

Common diisocyanates include toluene diisocyanate (TDI), methylene diphenyl diisocyanate (MDI), hexamethylene diisocyanate (HDI) and isophorone diisocyanate (IPDI). The first two contain aromatic rings; the latter two use nonaromatic open-chain and cyclic frameworks, respectively. These structures influence reactivity, molecular shape and the product's response to light and heat. Polyols offer another range of choices: small diols, long flexible polyether diols, polyester diols, polycarbonate diols and appropriately modified vegetable-oil polyols. Plant origin identifies a carbon source; it does not mean an unmodified oil necessarily contains enough hydroxyl groups for the intended reaction. The actual reactive population must still be measured. With a long-chain polyol, both its chain length and its mean hydroxyl functionality matter.

The **hydroxyl number** expresses hydroxyl content per gram as the mass of potassium hydroxide having the same equivalent amount. This is a measurement convention, not an instruction to put that much potassium hydroxide into the formulation. A larger hydroxyl number means more hydroxyl equivalents per unit mass. Whether that reflects shorter molecules or higher functionality requires further structural information. For a molecule with exactly two hydroxyls, making the chain longer spreads those two groups over more mass and lowers the hydroxyl number. A population with three or more hydroxyls per molecule cannot be assigned the same chain length from hydroxyl number alone.

Converting hydroxyl number into reactive groupsEq. 6

![Converting hydroxyl number into reactive groups](https://ml-biomat.com/static/agent-math/4aa2880ee33e1a5f198cdeb7.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| H_{OH} | Hydroxyl number: equivalent milligrams of KOH per gram of sample | mg KOH g⁻¹ |
| f_{OH} | Number-average hydroxyl functionality per molecule | 1 |
| M_{n} | Number-average molar mass of the polyol | g mol⁻¹ |
| m | Mass of the polyol sample | g |
| n_{OH} | Molar amount of hydroxyl groups in the sample | mol |
| 56 100 | Approximate KOH molar mass, 56.1 g/mol, expressed in mg/mol | mg mol⁻¹ |

Reading the relationshipDivide hydroxyl moles per mole of molecules by molecular molar mass to obtain groups per gram, then express them as KOH equivalents. Multiplying hydroxyl number by sample mass and dividing by KOH molar mass reverses that conversion.

A worked exampleAn ideal diol with f_OH=2 and M_n=2000 g/mol has H_OH=56.1 mg KOH/g. A 100 g sample contains 0.100 mol hydroxyl groups and 0.050 mol molecules.

ConditionsThe first expression requires consistent molecular and hydroxyl counting, with analytical corrections for other reactive constituents. In a distribution f_OH is a number average; a nominal functionality cannot be assigned arbitrarily to a complex mixture.

All ingredients consuming isocyanate must be included in the group balance. In a simplified formulation containing polyol and water as a chemical blowing agent, water is not an inert diluent. Its complete pathway to a urea connection and carbon dioxide consumes two isocyanate groups per water molecule. The isocyanate index compares supplied NCO equivalents with the theoretical requirement, conventionally assigning one hundred to equality. This is useful formulation bookkeeping, but it is not itself a measure of crosslink density. Functionality, conversion and secondary reactions still determine the eventual network.

Isocyanate index for a polyol–water formulationEq. 7

![Isocyanate index for a polyol–water formulation](https://ml-biomat.com/static/agent-math/14633e0b5e3977ab98a5ea04.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| n_{req} | Theoretical NCO-group requirement for the reactions included | mol |
| n_{OH}, n_{water} | Moles of hydroxyl groups and water molecules | mol |
| n_{NCO} | Moles of NCO groups supplied | mol |
| I_{NCO} | Isocyanate index, equal to 100 when supply equals requirement | 1 |
| 2, 100 | Two NCO groups consumed per water molecule; conventional index multiplier | 1 |

Reading the relationshipEach hydroxyl consumes one NCO to form urethane. Water followed by amine-to-urea conversion consumes two NCO groups, so requirements are added before comparison with supply.

A worked exampleWith 0.100 mol hydroxyl and 0.100 mol water, 0.300 mol NCO is required. Supplying 0.315 mol NCO gives an index of 105. These are NCO-group moles, not diisocyanate-molecule moles.

ConditionsThis formulation counts only polyol, water and the principal reactions shown. Amine extenders, other active hydrogens and other consumption routes add their appropriate requirements. Index does not directly specify crosslink density.

A prepolymer route first reacts some ingredients to form relatively short chains retaining reactive ends, then extends them using a diol or diamine. Diol extension creates additional urethane connections; diamine reacting with isocyanate creates urea connections. Materials containing both are often called polyurethane–ureas. Prepolymer formation helps organize reaction speed, segment distribution and mixing viscosity, but the remaining end-group population must be known at each stage. A one-shot route instead mixes the relevant ingredients directly under suitable conditions, requiring metering, mixing and reaction rates to work together. It is more than simply omitting the waiting time between additions.

Catalysts alter the relative rates of competing pathways. Some systems favour network formation, while others favour water-related blowing chemistry; choice also depends on the product, processing window and compatibility. Components of functionality three or greater provide possible network junctions. Further reaction of isocyanates with existing urethane or urea groups can also produce allophanate or biuret connections. Bifunctional ingredients are therefore a starting point for understanding a linear polymer. Whether a real product behaves as a thermoplastic additionally depends on other crosslinking routes and on which structural constraints are reversible at processing temperature.

## Turning the same chemistry into elastomers, foams and water dispersions

Imagine flexible cord sections connected between relatively stable junctions. Pulling aligns previously bent sections, while release allows them to return to a wider range of bent conformations; the junctions prevent all the cords from sliding away. In a polyurethane elastomer, soft segments commonly provide mobile chain sections, while harder segment aggregates, crystals or chemical crosslinks supply constraints. Real molecules explore conformations through thermal motion and interactions. The cord analogy is useful specifically for understanding how deformable sections and structure-preserving junctions cooperate.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe08/en/#en-s5)

Figure 4 · From Bayer’s polyaddition route to segmented-polyurethane design. Mobile segments change conformation between constraints of different physical or chemical origins. Hydrogen and covalent bonds are not drawn at atomic scale.

Hard-segment regions in thermoplastic polyurethane can establish physical connections through hydrogen bonding and ordered association. Suitable heating weakens these constraints and allows processing flow; cooling rebuilds them. A thermoset instead contains a spanning covalent network and does not become an ordinary freely flowing thermoplastic melt upon heating. Service temperature matters in either case. Frozen, glassy soft segments make a material harder, whereas inadequate constraint from the fixed regions permits permanent deformation. Elastic behaviour must therefore be related to the actual temperature and structural transitions, rather than inferred simply from the name rubber or polyurethane.

Shape memory adds a further sequence. A material is deformed while sufficiently mobile, held under constraint during cooling, and allowed to freeze a temporary shape. Reheating restores the mobility needed for a stable network or structure to guide recovery. An ordinary rubber band recoils immediately after release, whereas a shape-memory material can postpone recovery until thermal triggering. The distinction lies in the order of deformation, fixing and recovery. Products that shrink when heated need not all use the same shape-memory mechanism.

Foam manufacture must coordinate gas generation with formation of a supporting skeleton. Isocyanate first reacts with water through an unstable intermediate, releasing carbon dioxide and producing an amine; the amine consumes another isocyanate to form a urea connection. Water consequently changes both gas quantity and solid chemistry. If gas appears before sufficient support develops, cells can merge or collapse. If the network stiffens too early, expansion is restricted. Foam stabilizers, mixing, heat removal and mould constraints all affect this timing, so foaming is considerably more than introducing air into an already finished plastic.

Water changes both gas amount and the solid skeletonEq. 8

![Water changes both gas amount and the solid skeleton](https://ml-biomat.com/static/agent-math/99104da560cdaca8d361cd3f.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| R, NCO | Organic residue and isocyanate group; CO denotes a carbonyl double bond | 1 |
| H₂O, CO₂ | Water and carbon dioxide; subscripts count atoms | 1 |
| n_{CO}₂, n_{water} | Moles of generated carbon dioxide and water reacting through this pathway | mol |
| V_{g} | Gas volume at the specified temperature and pressure | L |
| R (gas) | Gas constant, here 8.314 L·kPa/(mol·K), distinct in context from chemical residue R | L kPa mol⁻¹ K⁻¹ |
| T, P | Absolute temperature and absolute pressure | K; kPa |

Reading the relationshipThe net reaction retains water hydrogens in the urea connection and releases one carbon with two oxygens as CO₂. The other NCO contributes the urea carbonyl. Once gas moles are known, the ideal-gas relation estimates volume.

A worked exampleUsing a rounded water molar mass of 18 g/mol, 1.8 g water yields 0.100 mol CO₂ and consumes 0.200 mol NCO. At 300 K and 100 kPa the ideal-gas volume is 2.4942 L.

ConditionsComplete water conversion through the stated pathway and approximately ideal gas. Dissolution, escape, cooling contraction and mechanical constraints mean calculated gas volume is not automatically final foam volume.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe08/en/#en-s5)

Figure 5 · Polyurethane chemical blowing couples gas release with urea formation. Cells can merge, rupture and connect as the skeleton develops, so cell count is not conserved. Real sizes depend on formulation and processing.

Flexible foams often use longer, lower-functionality polyols and develop many connected cells, allowing gas movement and skeleton bending during compression. Rigid insulating foams commonly have greater network constraint and more closed cells; both cell gas and solid structure influence heat transfer. Open or closed cells are not determined by a single ingredient alone, because stabilization and rupture of cell films also matter. Chemical blowing generates gas by reaction, whereas physical blowing can use vaporization of a low-boiling component. A formulation can combine both. An ideal-gas calculation estimates gas amount, but final foam volume also depends on dissolution, temperature, pressure, gas loss and skeleton shrinkage.

In reaction injection moulding, accurately metered low-viscosity components mix rapidly, enter a mould and grow, extend or crosslink there. The mould defines shape while affecting heat removal and cure. Previously manufactured thermoplastic polyurethane pellets can instead be melted again for extrusion or injection moulding. These are different routes: one mainly manages melt flow and cooling, while the other must fit mixing, filling and chemical reaction into the same time window. Recognizing the difference helps explain why similar final objects can require very different machinery.

Waterborne polyurethane raises a different question: how can hydrophobic chains form a stable dispersion in water? One common route incorporates an internal emulsifying component such as dimethylolpropionic acid. Its two hydroxyl groups participate in chain formation, while neutralization of its carboxyl group creates ionic functionality that helps stabilize dispersed particles. Chain extension and solvent removal are then arranged to produce a coating dispersion. Water surrounds the particles as the continuous phase; the individual polymer chains need not be molecularly dissolved in it. During film formation, water leaves and particles approach, deform and form a continuous layer, with polymer mobility influencing that process.

Coatings intended for storage before reaction can use blocked isocyanates to reduce end-group reactivity temporarily, recovering useful reactivity under appropriate heating conditions. Other systems create additional connections through reactions involving groups such as epoxides. Such approaches control when and where reactions occur. Considered alongside foams and water dispersions, polyurethane formulation becomes a set of connected design decisions: available end groups, structural constraints, gas generation and dispersion stability are each arranged to suit the intended manufacturing process.

## How a catalyst gives polypropylene a regular spatial sequence

Ethylene and propylene both contain a carbon–carbon double bond. Ethylene is relatively symmetric around its double-bond carbons, whereas propylene carries an additional methyl group. When the double bond contributes to the backbone, that group remains beside it. A regular sequence of spatial configurations can help the chain pack periodically into a crystal. These are **configurational** differences, whose alteration generally involves changing chemical bonds. Bending an existing chain through single-bond rotations instead changes its conformation. Keeping the two distinct explains why chains move and bend in a melt without automatically converting atactic polypropylene into isotactic polypropylene.

During the 1950s, Ziegler developed metal-compound systems for ethylene polymerization, enabling relatively linear polyethylene under conditions different from the high-pressure radical route. [Natta recalled in his Nobel lecture](https://www.nobelprize.org/uploads/2018/06/natta-lecture.pdf) that his 1954 investigations of propylene and other monomers produced fractions differing in crystallizability. Some separated fractions had similar molar masses but different abilities to crystallize, directing attention to spatial chain structure. X-ray diffraction helped identify ordered structures. The important reasoning is that similar composition and molecular size can still produce different behaviour when spatial configurations differ.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe08/en/#en-s6)

Figure 6 · Natta connected crystallization differences with stereoregularity through separation and structure analysis. Methyl groups on alternate backbone carbons show repeated, alternating and irregular configurations. This comparison projection is not a straight-chain conformation.

Coordination insertion can be understood locally. A growing chain is attached to a metal active centre. An approaching monomer coordinates to that centre and then inserts between metal and chain, extending the backbone while leaving a centre able to accept another monomer. Ligands or the surrounding solid surface favour some approach geometries over others and thereby influence the configuration produced by propylene insertion. A catalyst does not comb an entire chain straight. It biases individual bond-forming choices, and repeated local choices produce the stereoregularity measured in the final polymer.

In an agreed chain-projection convention, isotactic polypropylene has repeated relative configurations, syndiotactic polypropylene has regular alternation, and atactic polypropylene lacks such an extended regular sequence. Drawing side groups above or below a line is a comparison device, not a claim that real chains remain flat. A chain can adopt a helical conformation inside a crystal, and crystalline regions coexist with amorphous material. Explaining a property consequently requires several steps: local insertion choice, stereochemical sequence, crystal organization and then mechanical, thermal and processing behaviour.

Conventional heterogeneous Ziegler–Natta catalysts can contain active centres in different environments. Single-site systems such as appropriate metallocenes make the centres' chemical environments more uniform, helping control comonomer incorporation and chain-length distribution. Single site describes relative uniformity of site type; it does not mean there is only one centre in a reactor or that all chains start and stop together. Transfer, changes in activity, temperature and transport can still influence the product population. Catalyst structure and reactor environment must therefore be considered together when explaining a resin's properties.

## Why polyolefins use slurry, solution and gas-phase processes

The physical state of polyethylene or polypropylene in a reactor determines how heat and monomer reach reaction sites. Insoluble but potentially swollen polymer particles dispersed in a liquid form a slurry. Chains molecularly dissolved under the chosen temperature and solvent conditions form a solution. Gas-phase processes bring gaseous monomer into contact with polymer particles, using fluidization or circulation in relevant designs. A solid particle can still be swollen by monomer or solvent, while a uniform-looking solution can be very viscous. These actual states are more informative about equipment duties than the process names alone.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe08/en/#en-s7)

Figure 7 · Comparison of slurry, solution and gas–particle states. Adjacent descriptions distinguish particle and chain marks; arrows indicate circulation or gas flow. The diagrams explain process duties rather than specify plant piping.

A slurry loop uses a circulation pump to move particles and diluent rapidly through a pipe circuit, removing polymerization heat through cooled walls. Feeds commonly include monomer, catalyst, selected comonomer and hydrogen for chain-length adjustment. Particles grow as polymer forms, and slurry is withdrawn continuously or periodically. Pressure reduction flashes volatile components away from solid polymer; further purging and devolatilization reduce residues, while recovered monomer and diluent are treated for reuse. Growing polymer surrounds and redistributes supported catalyst material, linking final particle morphology with the initial catalyst and its fragmentation behaviour.

A stirred slurry route provides mixing with impellers and can connect several reactors in series. Different hydrogen, comonomer and other conditions in successive stages allow different chain populations to form within one process. Hydrogen commonly reduces mean chain length through transfer, with sensitivity depending on the catalyst. Comonomers alter short-branch abundance and distribution. A reactor cascade offers independent design choices, but simply placing vessels in series does not automatically create two molar-mass peaks. The stages must actually produce distinguishable populations in suitable proportions. Solid–liquid separation, oligomer handling and solvent recovery are then organized around the resulting material state.

Solution polymerization retains growing chains in a hot solution and is useful for certain more highly copolymerized, less crystalline polyolefins. It must manage reaction heat and viscosity increasing with polymer concentration, followed by solvent and monomer recovery through operations such as flashing and devolatilization. Gas-phase processing instead uses circulating gas to supply monomer and remove heat, reducing large liquid-solvent separation duties. Heat and mass transfer within and around particles remain important. Each route has product and equipment conditions for which it is suitable, and a resin family can be manufactured by more than one route.

In bulk-slurry polypropylene processing, liquid propylene acts as both reactant and dispersing medium. Polymer particles form within it, and evaporation, condensation and return of monomer can help remove reaction heat. Flashing the discharged material recovers unreacted propylene. Early catalyst systems required more downstream work to remove residues and unwanted atactic material; highly active, stereoselective systems simplified some of these separations. Solvent extraction of atactic polypropylene is therefore useful for understanding process development, rather than a fixed sequence that every modern plant must reproduce.

Whatever the route, feed purity affects active-centre behaviour. Water, oxygen or other strongly interacting impurities can alter or terminate activity, making purification and controlled transfer part of maintaining reaction conditions. At the appropriate stage, remaining activity is quenched, volatile material removed and stabilizers incorporated before pelletization. Finished pellets thus represent more than completion of polymerization: a reactive chemical system has been converted into material with controlled composition, morphology and storage behaviour.

## How chain length, branches and populations shape processing and use

Straight sticks of similar length generally stack more neatly than irregular branches. Polyethylene crystallization likewise depends on chain regularity, although molecular chains bend and crystallization also involves folding, incorporation of segments and cooling rate. Short branches disturb regular packing, and greater comonomer incorporation commonly reduces density and crystallinity. How branches are distributed between molecules changes the combination of harder and softer populations. Two resins with the same mean density can therefore differ in melting and processing behaviour because their composition distributions, long branches and molar-mass distributions differ.

High-density polyethylene, HDPE, generally has relatively high crystallinity and stiffness. Linear low-density polyethylene, LLDPE, introduces short branches through copolymerization, whereas low-density polyethylene conventionally called LDPE uses the radical route and has a more complex combination of short and long branches. Polyolefin elastomers often use greater comonomer incorporation and suitable sequence distributions to reduce crystallinity, allowing mobile segments to deform while remaining crystals or other constraints maintain connections. Their sequences and morphologies vary; not every product is the same explicitly segmented hard–soft block copolymer. Transparency also depends on crystal size, surface and thickness, so lower density alone does not guarantee a clearer object under all conditions.

There is more than one average chain size. Number-average molar mass gives each molecule equal weight. Weight-average molar mass gives larger molecules greater influence according to their mass contribution. A few very long cords mixed with many short ones illustrate why an average per cord differs from an average weighted by each cord's share of total mass. The ratio of these two averages is dispersity, which describes one aspect of distribution width. Different distribution shapes can share the same ratio, however, so it cannot replace the full distribution curve.

Number average, weight average and dispersityEq. 9

![Number average, weight average and dispersity](https://ml-biomat.com/static/agent-math/a34a8dc86d77502ffd093028.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| i, Σ_{i} | i labels a molecular-size group; the sum adds contributions from every group | 1 |
| N_{i} | Molecular count in group i | 1 |
| M_{i}, M_{n}, M_{w} | Group molar mass, number-average molar mass and weight-average molar mass | g mol⁻¹ |
| M_{i}² | Molar mass squared, giving the mass weighting for heavier groups | g² mol⁻² |
| Đ | Dispersity, the ratio of weight to number average | 1 |

Reading the relationshipThe number average gives every molecule equal counting weight. Weight-average weights are proportional to group mass N_iM_i, producing M_i squared in its numerator. Their ratio is dimensionless.

A worked exampleFor equal molecular counts at 20000 and 100000 g/mol, M_n=60000 g/mol, M_w≈86667 g/mol and Đ≈1.444.

ConditionsUse consistent molar masses and counts for the same complete molecular population. Equal dispersities can describe different distribution shapes; blends and branched systems require further structural information.

For sufficiently entangled, structurally comparable linear polyethylene melts, zero-shear viscosity is highly sensitive to molar mass. Zero shear describes sufficiently slow flow that the equilibrium entanglement structure is not substantially disturbed. Longer chains generally need more time to relax their surrounding constraints, making the melt harder to move under a small applied stress. A power-law comparison shows why doubling chain size can increase viscosity by much more than twofold. Its exponent applies within an appropriate structural and distribution range, rather than directly comparing arbitrary long-branched resins.

Why longer chains strongly increase low-rate viscosityEq. 10

![Why longer chains strongly increase low-rate viscosity](https://ml-biomat.com/static/agent-math/bd62b98812599f40f11f04cb.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| η_{0,1}, η_{0,2} | Zero-shear viscosities of two structurally comparable systems; 0 denotes the low-rate limit | Pa s |
| M_{w,1}, M_{w,2} | Corresponding weight-average molar masses | g mol⁻¹ |
| 1, 2, 3.4 | 1 and 2 label the systems; 3.4 is the exponent in this empirical scaling relation | 1 |

Reading the relationshipLong entangled chains relax their constraints slowly. A ratio removes the common prefactor at matched temperature and comparable structure, showing sensitivity to molar-mass changes.

A worked exampleDoubling weight-average molar mass gives a viscosity ratio of approximately 2³·⁴=10.56. An initial 1000 Pa·s would correspond to about 10560 Pa·s.

ConditionsComparison of well-entangled linear melts at equal temperature and similar chemistry and distribution. Strong shear, long branching or substantial distribution changes require a more complete description.

Extension and shear must also be distinguished in processing. Film blowing, foaming and some extrusion operations require sufficient support as a melt stretches; long branches can alter extensional viscosity and strain hardening, influencing bubble stability. Flow through a die must meanwhile remain compatible with pressure and energy requirements. LLDPE is widely used in extrusion processes including blown and cast film. Particular grades may need different conditions, die designs or blends, but one extensional curve cannot justify declaring the whole family unsuitable for extrusion. Selection must match flow mode, equipment and product requirements.

Bimodal and multimodal HDPE distribute tasks among chain populations. A lower-molar-mass fraction supports processing flow, while a higher-molar-mass fraction with suitable comonomer incorporation can improve intercrystalline connectivity and resistance to slow crack growth. More crystalline material contributes stiffness, but calling HDPE simply hard and brittle ignores grade, temperature, notches and loading time. Pressure-pipe classifications come from specified long-term performance evaluation, rather than from the word bimodal alone. Synthesis provides structural design tools; measurements matched to the intended application determine which product is appropriate.

A single-site catalyst does not automatically yield dispersity exactly equal to one. Even if all centres have identical growth opportunities, a fixed probability of transfer after each addition naturally creates chains of different lengths. The following simple probability model explains why an ideal transfer-controlled distribution approaches dispersity two at large mean chain length. A value near one requires additional kinetic conditions, such as nearly synchronized initiation and little transfer. Uniform site chemistry, uniform growth histories and uniform final chain lengths are different requirements.

Identical growth opportunities still create a distributionEq. 11

![Identical growth opportunities still create a distribution](https://ml-biomat.com/static/agent-math/300e39f733d11faac54d0f95.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| x | Number of monomer units in a chain, a positive integer | 1 |
| P(x) | Number probability that a randomly selected chain has exactly x units | 1 |
| q, 1−q | Fixed probability of ending a molecule by transfer after an addition, and probability of continuing | 1 |
| X_{n}, Đ | Number-average chain length and molar-mass dispersity | 1 |
| (1−q)^(x−1) | Probability of continuing x−1 times under independent choices | 1 |

Reading the relationshipLength x requires x−1 continuations followed by termination of that molecule with probability q. Multiplication gives its probability; averaging the first and second length moments over all positive integers gives mean length and dispersity.

A worked exampleAt q=0.01, X_n=100 and Đ=1.99. A more uniform q from consistent sites does not remove random differences in when molecular growth ends.

ConditionsIdeal geometric distribution with constant conditions and 0<q≤1, independent choices and negligible end-group mass in the molar-mass moments. Synchronized initiation with little transfer produces a different growth history.

## Inside a particle: competition between reaction and diffusion

A polyolefin particle is not a miniature vessel with identical concentration everywhere. Monomer travels from surrounding gas or liquid to the particle surface, through internal pores and potentially through swollen polymer surrounding a catalyst fragment before reaching an active centre. Supplying a city district and then delivering into individual rooms offers an analogy: open roads do not guarantee an unobstructed final passage. Real diffusion is driven by concentration differences rather than delivery workers. The useful correspondence is the hierarchy of distances and transport resistances in series.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe08/en/#en-s9)

Figure 8 · Two scales of a multigrain model and an enlarged core–shell unit. Shell diffusion feeds reaction near the core. R_c and R_p denote core and outer radii; c_c and c_l are their surface concentrations, defined beside the equations.

A multigrain model represents a larger polymer particle as an assembly of smaller units containing catalyst material and surrounding polymer. It translates internal structure into concentrations and transport parameters. For a thin volume inside the larger particle, monomer accumulation equals diffusive inflow minus outflow and reaction consumption. Spherical surface area increases with radius, so equal radial distances do not correspond to equal areas available for transport. That geometry produces the radius-squared terms in spherical diffusion. Understanding inflow, outflow and consumption first makes the differential equation a readable conservation statement.

Monomer conservation inside a larger particleEq. 12

![Monomer conservation inside a larger particle](https://ml-biomat.com/static/agent-math/2bee2b64733a27c2434a2c76.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| c(r,t), c_{b} | Internal monomer concentration and prescribed outer-surface concentration | mol m⁻³ |
| r, R | Radial position measured from the centre and larger-particle radius | m |
| t, D_{eff} | Time and effective diffusivity | s; m² s⁻¹ |
| q_{v} | Local monomer consumption per total particle volume, potentially concentration dependent | mol m⁻³ s⁻¹ |
| ∂c/∂t, ∂c/∂r | Concentration-change rate at fixed position; radial concentration gradient at fixed time | mol m⁻³ s⁻¹; mol m⁻⁴ |
| r², ∂/∂r | Radial scaling of spherical area; operation of taking a radial derivative | m²; m⁻¹ |

Reading the relationshipThe diffusion term gives net inflow into a thin shell, reaction removes monomer, and the left side records accumulation. Zero centre gradient expresses spherical symmetry; the surface condition specifies the supplied concentration.

A worked exampleIf net diffusive inflow is momentarily zero and q_v=2 mol/(m³·s), the initial local concentration rate is −2 mol/(m³·s). If these conditions remain approximately constant for 0.5 s, concentration falls by about 1 mol/m³.

ConditionsFixed radius, spherical symmetry and representative constant D_eff, with consistent volume bases. A transient solution also requires c(r,0); substantial external-film resistance requires a different surface boundary condition.

To isolate the innermost competition, fix a spherical catalyst core and its polymer shell. Let the shell transport monomer without reacting, and represent consumption near the core by a first-order coefficient referred to core volume. Once a quasi-steady profile is established, the same total molar rate crosses every spherical surface. Local flux must therefore be multiplied by surface area before it can be compared with total consumption. Integrating the shell concentration gradient gives the transport relation between outer surface and core; equating that transport with reaction determines the concentration actually available at the active region.

Shell supply equals consumption near the coreEq. 13

![Shell supply equals consumption near the core](https://ml-biomat.com/static/agent-math/9b935f8a77981e4f61094d69.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| j_{D}, j_{R} | Total molar rates of diffusion supply and reaction consumption, not flux per area | mol s⁻¹ |
| D_{p} | Monomer diffusivity in the swollen polymer shell | m² s⁻¹ |
| c_{l}, c_{c} | Outer-shell and core-surface concentrations on the same phase basis | mol m⁻³ |
| R_{c}, R_{p} | Core radius and outer polymer-shell radius, with R_p>R_c | m |
| k_{eff} | Effective first-order consumption coefficient referred to core volume | s⁻¹ |
| π, 4πR_{c}³/3 | Pi, approximately 3.14159; spherical-core volume | 1; m³ |

Reading the relationshipQuasi-steady transport has the same total rate across every sphere. Multiplying the local gradient flux by 4πr² and integrating radially gives shell resistance. Core volume times apparent volumetric reaction rate gives consumption; equality determines the interfacial concentration.

A worked exampleFor R_c=1 μm, R_p=3 μm, D_p=10⁻¹¹ m²/s, c_l=100 mol/m³ and k_eff=300 s⁻¹, c_c≈13.0435 mol/m³ and both routes give approximately 1.639×10⁻¹⁴ mol/s.

ConditionsIsothermal quasi-steady transport through a fixed spherical shell without shell reaction. Consumption near the core is represented by a first-order rate referred to core volume, omitting external-film and partition resistance.

The most useful result collects several parameters into a dimensionless competition measure. A large diffusivity replenishes depletion more readily. A larger core or stronger reaction coefficient increases demand relative to supply, and a thicker shell adds resistance. Combining these effects predicts how far the core concentration falls below the outer concentration. This is depletion of local monomer supply, rather than a chemical change to catalyst activity caused by an impurity. Distinguishing the two helps identify what changes in temperature, particle size or pore structure are actually improving.

A dimensionless measure of shell transport limitationEq. 14

![A dimensionless measure of shell transport limitation](https://ml-biomat.com/static/agent-math/0621b33e388bbb007ee7a993.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Da_{s} | Dimensionless Damköhler-type parameter comparing core consumption with shell supply | 1 |
| k_{eff}, D_{p} | Core-volume-based first-order consumption coefficient and shell diffusivity | s⁻¹; m² s⁻¹ |
| R_{c}, R_{p} | Catalyst-core and outer-shell radii | m |
| c_{c}, c_{l} | Core-surface and outer-shell concentrations on the same phase basis | mol m⁻³ |
| R_{c}², 1−R_{c}/R_{p} | Squared core radius; geometric factor describing shell extent | m²; 1 |

Reading the relationshipEquating shell supply and consumption and collecting terms in c_c gives the concentration ratio. Larger Da_s means stronger consumption relative to transport and greater local depletion.

A worked exampleFor the preceding parameters, Da_s=6.6667 and c_c/c_l=0.130435. A tenfold increase in D_p lowers Da_s to 0.66667 and raises the ratio to 0.6000.

ConditionsSame fixed-shell, quasi-steady and first-order assumptions. Shell resistance vanishes as R_p approaches R_c. Larger-particle pores, heating, growth and active-centre deactivation are not included.

### Compare reaction demand with diffusive supply

[Figure: Compare reaction demand with diffusive supply](https://ml-biomat.com/tutorials/biomaterials-courses/pe08/en/#en-s9)

Fixed 1 μm core and 100 mol/m³ outer-shell concentration. Core consumption is first order per core volume; the shell has no reaction. Heating, external films and partitioning are omitted. Diffusivity runs from 10⁻¹² to 10⁻¹⁰ m²/s on a multiplicative scale. Plot limits stay fixed.

Hold the reaction coefficient fixed and increase diffusivity in the interaction, watching the core concentration approach the outer value. Then keep diffusivity fixed and increase the reaction coefficient, comparing local concentration with total reaction rate. A stronger reaction can lower local concentration while still increasing total consumption, although the increase becomes progressively smaller. The horizontal axis runs from the core surface to the outer polymer surface, and the vertical axis shows actual monomer concentration. The profile is generally curved because the same total flow passes through spherical surfaces of different areas.

Real particles grow, fragment and change pore structure, and their internal temperature can differ from the surrounding fluid. Diffusivity and reaction coefficients can therefore vary with time and position. Larger-scale pore transport and external gas- or liquid-film resistance may also need to be calculated. At the start, a concentration field is still developing, so a quasi-steady expression does not describe the complete initial transient. This simplified model makes one resistance explicit and calculable before additional structure is introduced, keeping the meaning of each parameter connected to a physical process.

Chains formed at different locations can experience different monomer concentrations, hydrogen concentrations and temperatures. Together with site type and starting time, these histories generate different molecular populations. Comparing growth over a time interval also requires consistent counting: total monomer moles must be compared with moles of active chains, while concentrations must share a volume basis. Treating the molar rate through a sphere directly as a concentration-change rate loses a volume factor. Across the chapter, formulation, catalysis, heat transfer and mass transfer all participate in forming molecular structure. Fibres, foams, films and pipes carry the combined consequences of those local processes.
