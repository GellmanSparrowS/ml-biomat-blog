# Connecting Soft and Hard Blocks: Copolymers and Elastomers

Source: https://ml-biomat.com/tutorials/biomaterials-courses/pm10/en/
Language: en

Begin with shoe-sole recovery and sustained support in a seal. Follow block self-assembly, structural measurements and elastic networks to compare molecular block systems, olefin blends and dynamic vulcanizates, connecting softness and recovery to thermoplastic processing.

## How flexible chains and firm junctions work together

A shoe sole is compressed at every step, a cable jacket must bend around corners, and a seal must keep pressing against its mating surface. All three need to deform readily while retaining shape. Conventional rubber achieves this through vulcanization, which establishes permanent molecular connections. Another route combines flexible chains with relatively firm regions that hold those chains in place during use but allow rearrangement during hot processing. This is the structural idea behind many thermoplastic elastomers. The same principles also help explain how related molecules organize into nanoscale channels, patterned films and small containers for other molecules.

A polymer molecule is a long chain of small chemical units connected by bonds. Many changes in chain shape occur through rotations around bonds without breaking the molecule. If a sequence of A units is followed by a sequence of B units, the result is an AB diblock copolymer. Putting A sequences at both ends of a B sequence gives an ABA triblock. A block is therefore a continuous section of appreciable length and distinct chemical composition. The letters do not by themselves mean hard or soft. Whether either block is glassy, rubbery or crystalline depends on its chemistry and the temperature at which it is examined.

Imagine joining a red length of cord to a blue length. Red portions prefer the company of red portions, while blue portions have a different preference, but the joining point remains intact. Two populations of separate polymer molecules may segregate into very large regions. Covalently joining the populations constrains that separation by the length of the connected chains. A covalent bond involves atoms sharing electrons; it survives the ordinary rearrangements considered here. Different compositions can consequently occupy distinct regions without simply becoming two macroscopic layers. Each connection keeps the two blocks involved in the same spatial arrangement.

Sequence and formulation describe different things. In a random copolymer, the two kinds of units are distributed along a chain. A graft copolymer has long branches attached to a backbone. A blend contains different molecular populations mixed together. Each may develop hard and soft phases, yet their connections, interfaces and load paths differ. In particular, “thermoplastic elastomer” describes a combination of mechanical and processing behavior. It does not require every member of the family to be a block copolymer. This distinction becomes important when comparing olefin blends with dynamically vulcanized materials.

Volume fraction is especially useful when discussing the shapes of domains: it tells us how much space a component must occupy. Mass fraction alone cannot provide that information when the components have different densities. Density is mass per unit volume, so dividing mass by density gives volume. The following expression converts the masses of two components into a volume fraction, a dimensionless ratio between one component’s volume and the combined volume. The densities should describe the temperature and physical states being discussed.

Convert mass composition to volume fractionEq. 1

![Convert mass composition to volume fraction](https://ml-biomat.com/static/agent-math/206cfbb24432bc4becb8918e.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| fₐ | Volume fraction of component A | 1 |
| mₐ、mᵦ | Masses of components A and B | g |
| ρₐ、ρᵦ | Densities of A and B in the states considered | g/cm³ |
| A、B | Labels for the two chemically distinct components | 1 |

Reading the relationshipMass divided by density gives volume. Dividing A volume by the sum of both volumes gives its spatial fraction.

A worked exampleWith mₐ = 40 g, ρₐ = 1.05 g/cm³, mᵦ = 60 g and ρᵦ = 0.90 g/cm³, the volumes are about 38.095 and 66.667 cm³. Thus fₐ ≈ 0.3636, or 36.36%, rather than the 40% mass fraction.

ConditionsAssumes approximately additive component volumes and densities appropriate to temperature and physical state. Solvents and additives require corresponding denominator terms or an explicit polymer-only basis.

Architecture adds another design variable. A chain may be linear, star-shaped, cyclic or highly branched. At the same A volume fraction, one long A block and several short A arms attached near one point need different amounts of space near an interface. Consequently, a molecular specification contains more than the amount of each chemical component. Connectivity determines how chains fill space and whether flexible sections can join different hard regions. Those bridges can turn local domains into a network that transmits load across an entire object.

## Why microphase separation produces spheres, cylinders, layers and networks

When contacts between A and B carry an unfavorable free-energy cost, the chains tend to reduce those contacts. Free energy combines interaction effects with the number of molecular arrangements available at a given temperature. Separating into A-rich and B-rich regions reduces unfavorable contacts, but introduces interfaces and changes the shapes available to connected chains. Very large domains would require many chains to stretch excessively. Extremely small domains would create a large total interfacial area. Competition among these costs gives domains a finite characteristic size.

Microphase-separated domains often have dimensions measured in nanometers; one nanometer is a billionth of a meter. The chains inside a domain need not possess the regular atomic arrangement of a crystal. A spherical domain can contain amorphous chains while the centers of many such spheres form a periodic array. Atomic crystallization and domain-scale ordering are therefore distinct. A sample can have regularly spaced layers without crystalline chain packing. Alternatively, one kind of domain can crystallize internally, allowing the two forms of organization to influence one another.

A dimensionless interaction parameter, χ, describes the relative preference for contacts between unlike segments. Multiplying it by the number N of reference segments in a chain gives the commonly used segregation strength χN. A longer chain accumulates the effects of many individually modest contact preferences. In 1980, Leibler developed a statistical theory of composition fluctuations in ideal AB melts and connected composition and χN to the onset of ordered structures. A phase diagram is a map of relatively stable organizations under specified conditions. It is not a fixed pattern catalogue that every commercial material must follow.

Segregation strength combines interaction and chain lengthEq. 2

![Segregation strength combines interaction and chain length](https://ml-biomat.com/static/agent-math/1f332be7fe9c8004ed4f70fb.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| N | Total number of reference segments in a chain | 1 |
| Nₐ、Nᵦ | Reference-segment counts in A and B | 1 |
| χ | Segment interaction parameter using the same reference-volume convention | 1 |
| S | Segregation strength defined here as χN | 1 |

Reading the relationshipMultiplying the interaction scale per reference segment by segment count describes its accumulation along a chain. Volume fraction and architecture remain necessary for a phase diagram.

A worked exampleFor χ = 0.050 and Nₐ = Nᵦ = 100, N = 200 and S = 10. Increasing N to 240 at fixed χ and equal-volume symmetry gives S = 12. The mean-field critical χN for ideal symmetric Gaussian AB melts is about 10.495, placing the examples on opposite sides.

Conditionsχ and N must use a consistent reference-segment convention. The value 10.495 belongs to a mean-field ideal symmetric AB melt; fluctuations, molecular asymmetry, solvent and additional interactions shift real transitions.

When A occupies a small volume fraction, roughly spherical A-rich regions can fit within a continuous B-rich matrix. Increasing the A fraction can favor cylinders, connected networks and eventually alternating layers. Near equal volumes, flat layers can accommodate chains on the two sides relatively symmetrically. This sequence builds a useful geometrical intuition, while the actual stable regions depend on interaction strength, molecular asymmetry and architecture. A domain is also not a single enormous molecule. Many molecules usually contribute blocks to it, with their connecting points distributed near its interfaces.

Identifying connected networks became an important part of the field’s history. Early electron micrographs showed interpenetrating stripes and holes, and some structures were assigned to double-diamond networks. In 1994, Hajduk and colleagues identified the double-gyroid morphology in a diblock system. Subsequent re-examination of some earlier star-block samples also changed their assignments. A double gyroid contains two separate, nonintersecting networks of the same component, intertwined through space and surrounded by a continuous matrix of the other component. Similar-looking holes in a projection can belong to very different three-dimensional connections.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pm10/en/#en-s2)

Figure 1 · Gyroid identification and subsequent reassessment by Hajduk and colleagues showed that similar projections need not share topology. The upper drawings show local coordination, not complete unit cells; the lower panel represents the need for multiple sections.

The useful lesson is to distinguish local connectivity from a complete spatial structure. An ideal gyroid network has three-connected junctions; a diamond network has four-connected junctions. Coordination provides evidence, but periodicity, symmetry and three-dimensional reconstruction are needed together. More complex branched molecules can form arrangements such as A15 and σ phases, with domains in inequivalent positions and different numbers of neighbors. These are deformable soft domains, not perfectly rigid balls of identical size. Chains stretch and interfaces reshape, creating additional packing possibilities as well as defects and variations in local dimensions.

## How solvents and thin surfaces change the organization

A melt is largely occupied by the polymers themselves. A solution adds molecules that can enter the space between chains. A solvent that interacts favorably with A but less favorably with B is selective for one block. Water provides a familiar setting for amphiphilic blocks: hydrophilic sections make favorable contacts with water, while hydrophobic sections tend to reduce their exposure. Many molecules can gather their hydrophobic blocks inward and expose hydrophilic blocks outward. The inner enriched region is called the core, and the surrounding layer of chains is the corona.

A spherical micelle has a hydrophobic core surrounded by a hydrophilic corona, but shape is not determined by water preference alone. The core must be filled, and corona chains need space to extend. Changing block lengths, concentration or solvent conditions changes the cost of interface curvature. Aggregates can become cylinders or form bilayers. Closing a bilayer into a shell produces a vesicle: water contacts both its outer and inner surfaces, with a relatively hydrophobic membrane between them. A micelle core and a vesicle’s aqueous interior are different compartments, with different opportunities for carrying guest molecules.

This organization supplies structural tools for transport and separation. Hydrophobic guests may partition into a core, water-soluble guests may occupy a vesicle cavity, and charged blocks can interact with ions. Release depends on guest–polymer interactions, membrane thickness, chain exchange and aggregate stability. Loading a molecule and allowing it to leave under the desired conditions are related but separate tasks. Dilution may change aggregate stability, salt may alter electrostatic interactions, and temperature may increase membrane mobility. Each variable can be examined through a defined experiment rather than inferred from particle shape alone.

The preparation route also matters. Slowly transferring a polymer from a good solvent into a selective solvent can give different sizes and shapes from directly adding dry polymer to water, even at the same final composition. Removing a long chain from an established core may be energetically costly. An aggregate can therefore retain a structure inherited from preparation for a long time. An equilibrium structure is favored after sufficient opportunity for rearrangement; a kinetically trapped structure retains information about the route taken. Solvent exchange, mixing and waiting conditions help explain why a particular shape persists.

Thin films add surface preferences and a finite thickness. If the substrate preferentially attracts A, an A-rich layer often forms near it. A different preference at the air interface can impose another constraint. When film thickness is close to the natural domain period, accommodating a whole number of layers may be easier than strongly stretching one layer. Terraces, islands or orientation defects can result. Changing surface affinity, thickness and annealing conditions can guide domains parallel or perpendicular to the substrate, providing a basis for transferring nanoscale patterns into another material.

Different applications exploit different kinds of continuity. Ion transport benefits from connected ion-containing regions while another phase maintains dimensions. Optical structures need both suitable dimensions and refractive-index contrast to interact selectively with light. Patterning depends on placement, spacing and defect density. An ordinary domain period of a few tens of nanometers does not automatically produce visible structural color; the dimensions must match the relevant optical conditions. Asking which phase is continuous, how large the period is, how it is oriented and where defects occur turns the broad idea of self-assembly into a specific functional mechanism.

## From scattering peaks to three-dimensional evidence

Electron microscopy reveals contrasts arising from interactions between electrons and the specimen. Selective staining can enhance contrast between blocks, while thin sections allow electrons to pass through. Dark circles may be spheres or cross-sections of cylinders. Stripes may be cylinders or obliquely sectioned layers. Orientation, section thickness and overlapping structures affect the image. Assigning a three-dimensional morphology therefore requires more than finding one attractive micrograph that resembles a familiar pattern.

Small-angle X-ray scattering provides complementary information. Waves scattered from composition variations at different positions interfere, reinforcing one another at certain angles and producing peaks. The structures of interest are larger than atomic spacings and correspond to smaller scattering angles. The scattering-vector magnitude q combines wavelength and angle into an inverse-length measure. A larger repeating distance generally produces a feature at smaller q. Once a lamellar structure and its first-order peak have been established, that peak can be converted into the repeat spacing.

Small-angle scattering and lamellar repeat spacingEq. 3

![Small-angle scattering and lamellar repeat spacing](https://ml-biomat.com/static/agent-math/64ddb2a9b9a55b9626562441.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| q | Scattering-vector magnitude | nm⁻¹ |
| θ | Half of the scattering angle 2θ | ° |
| λₓ | Incident X-ray wavelength | nm |
| D | Repeat period containing one A and one B layer | nm |
| q* | Position of the identified first-order lamellar peak | nm⁻¹ |
| π | Circle constant, approximately 3.14159 | 1 |
| sin | Sine function giving the relevant projection ratio | 1 |
| X、* | Labels for X-rays and the selected first-order peak | 1 |

Reading the relationshipq converts wavelength and angular deflection into an inverse length. A full phase cycle between lamellar repeats gives q*D = 2π, so D = 2π/q*.

A worked exampleA first-order lamellar peak at q* = 0.200 nm⁻¹ gives D = 2×3.14159/0.200 ≈ 31.42 nm. With λₓ = 0.154 nm, sin θ ≈ 0.002451, θ ≈ 0.1404° and 2θ ≈ 0.2809°.

ConditionsThe first expression gives elastic-scattering geometry; the second uses an identified first-order lamellar peak. Other lattices need their own indexing relationships, and a single peak does not establish morphology.

A lamellar period includes one A-rich layer and one B-rich layer, rather than the thickness of either alone. A period of approximately 31.42 nm would suggest roughly half that thickness for each layer if the volumes were equal and the interfaces narrow. Unequal composition or broad mixed interfaces require a more detailed interpretation. During stretching, direction-dependent peak shifts can reveal anisotropic spacing changes. Detector geometry, background and instrumental calibration also matter. The correlation length associated with peak width is not automatically the diameter of an individual domain.

Identification usually relies on several peak positions, their ratios, intensities and absences. Cylindrical arrays, lamellae and cubic networks have different allowed reflections, although orientation and measurement range can hide some of them. A productive approach proposes candidate structures and compares their expected signatures with several experimental observations. Microscopy gives local information about interfaces and connections. Scattering describes periodicity and symmetry shared by many domains. Together they place local pictures within the organization of the bulk sample.

Electron tomography collects projections while tilting a specimen and reconstructs a three-dimensional volume. Serial sectioning combined with scanning electron microscopy can reconstruct larger regions from successive slices. The result allows channels, junctions and curvature to be traced through space. Limited resolution can falsely join nearby channels, while a segmentation threshold can open or close a narrow neck. Checking reconstructed features against the original sections is consequently part of identifying topology. A network skeleton removes variations in thickness to emphasize connectivity; it does not retain the actual interfacial area or channel cross-section.

Time-resolved measurements connect structure to processing. On heating, hard-domain softening, domain mixing and crystal melting may occur at different stages. On cooling, composition segregation and chain crystallization may also follow different sequences. Increasing scattering intensity can track the development of domain order, but its normalized progress is not automatically an atomic crystalline mass fraction. Combining time-dependent scattering, thermal measurements and mechanics helps establish whether a change in stiffness comes from domain rearrangement, crystallization or the loss of load-bearing junctions. It also reveals whether the processing time was long enough to create the intended structure.

## How physical junctions turn chains into an elastic network

A free long chain generally adopts a coiled shape because many different coiled configurations are available. Stretching it restricts those possibilities. Once the force is removed, thermal motion favors renewed exploration of more configurations, producing a tendency to retract. This is entropic elasticity: entropy describes the richness of microscopic arrangements. A polymer chain is not simply a metal spring whose bonds lengthen under load. Ordinary rubbery deformation begins mainly with changing chain configuration. To preserve the shape of an object, junctions must also prevent whole chains from sliding away indefinitely.

In an ABA elastomer, A end blocks can gather into glassy hard domains while the B middle blocks remain flexible. A B block connecting two different hard domains forms a load-bearing bridge. If both ends return to the same domain, it forms a loop with a different contribution to the macroscopic network. Dangling chains have only one effective attachment, and some chains may remain ineffective as network strands. Two materials with the same hard-block fraction can therefore have different moduli and recovery because their bridge fractions, domain sizes and molecular distributions differ.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pm10/en/#en-s5)

Figure 2 · A soft chain joining distinct hard domains can act as a load-bearing bridge. Loops and dangling chains contribute differently. The drawing emphasizes connectivity; real networks contain many domains, entanglements and chain lengths.

A simple rubber-network model connects the number of active strands to stress. A mole is a counting unit containing approximately 6.022×10²³ specified objects. Here the objects are effective network strands, not individual chemical repeat units. Increasing their molar concentration places more load-bearing strands in the same volume. Absolute temperature, measured in kelvin, sets the thermal scale. Together these quantities determine the ideal network shear modulus over times for which its junctions remain stable.

Active strand density and ideal-network tensile stressEq. 4

![Active strand density and ideal-network tensile stress](https://ml-biomat.com/static/agent-math/5bc9ac86e50224fb8a7cea9a.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| G | Ideal network shear modulus | Pa |
| νₑ | Molar concentration of effective network strands | mol/m³ |
| R | Gas constant, here 8.314 | J/(mol·K) |
| T | Absolute temperature | K |
| λ | Stretch ratio, current divided by initial length | 1 |
| L、L₀ | Current and initial lengths | m |
| σₙ | Nominal tensile stress, force per initial area | Pa |
| e、N、0 | Labels for effective strands, nominal stress and initial state | 1 |
| λ⁻² | Reciprocal of the squared stretch ratio | 1 |

Reading the relationshipStrand concentration times molar thermal energy RT gives an energy per volume, equivalent to stress. Gaussian-network stretching and transverse contraction during incompressible uniaxial deformation yield λ−λ⁻².

A worked exampleFor νₑ = 100 mol/m³ and T = 298 K, G = 100×8.314×298 = 247757.2 Pa ≈ 0.2478 MPa. With L₀ = 0.050 m and L = 0.100 m, λ = 2 and σₙ = 0.2477572×(2−1/4) ≈ 0.4336 MPa.

ConditionsAn isothermal, approximately incompressible Gaussian network with junctions stable over the observation time and chains well below full extension. Domain yielding, sliding, finite extensibility and hysteresis are outside this model.

The stretch ratio is current length divided by initial length. A ratio of 2 means doubled length and 100% engineering strain, rather than 200%. The model calculates nominal tensile stress, force divided by initial area. A soft specimen generally becomes thinner when stretched, so true stress calculated using current area is different. The positive term represents the stretch-direction contribution; the negative term includes the influence of transverse contraction under constant volume. A defined network assumption is thereby translated into a numerical relationship that can be explored directly.

[Figure: Ideal-network nominal stress versus stretch ratio](https://ml-biomat.com/tutorials/biomaterials-courses/pm10/en/#en-s5)

Change active strand concentration and stretch ratio to explore ideal-network modulus and nominal stress. Temperature is fixed at 298 K; domain failure and cyclic losses are outside the plotted model.

Physical junctions have lifetimes. A hard domain may hold an end block securely during a quick movement but allow extraction or exchange over a longer interval. Heating commonly speeds rearrangement, and a solvent can enter a hard domain and reduce its stability. A material can thus recover well after a fast action yet gradually lose support during sustained compression. Thermoplastic processing makes use of the ability of junctions and domains to rearrange at elevated temperature. Depending on the material, glass softening, crystal melting or several interactions may contribute; there is no single universal unlocking temperature.

Real elastomers also show hysteresis and residual deformation. Rotating domains, sliding chains and reorganizing junctions consume energy during loading. Those paths need not reverse immediately during unloading, so the return curve differs from the loading curve. The area between them measures mechanical energy dissipated in one cycle, which can become heat or contribute to internal structural changes. Some dissipation is useful for damping. Excessive loss reduces energy return and causes heating in a component designed for rebound. Increasing effective strand density is therefore a design choice to balance with extension, fatigue resistance and processing flow.

## What the segments do in TPU, copolyester and polyamide elastomers

Thermoplastic polyurethane, or TPU, is commonly formed from a long-chain diol, a short-chain diol and a diisocyanate. A diol has two hydroxyl reaction ends; a diisocyanate has two corresponding reactive groups. Their reaction forms urethane linkages. The long-chain diol supplies relatively long, mobile soft segments, while the diisocyanate and short chain extender create denser hard sequences. A chain extender joins molecules and adjusts hard-segment structure. In ordinary linear TPU it should not automatically be described as a crosslinker creating a permanent three-dimensional network.

Hydrogen bonds and aggregation give hard segments stronger associations, and some hard domains are crystalline. A hydrogen bond is a directional attraction involving a suitable hydrogen-bearing group and a nearby group containing atoms such as oxygen or nitrogen. It helps segments associate, while remaining sensitive to temperature and environment. Soft and hard segments are not necessarily completely separated. Hard material mixed into a soft phase can restrict mobility and change its glass transition. Increasing hard-segment content often increases hardness and stiffness, but also changes connectivity and available extension. Other properties need not follow a linear composition rule.

Soft-segment chemistry strongly influences environmental response. Polyester segments contain ester groups, polyether segments contain ether linkages, and polycarbonate segments introduce another oxygen-containing connection. Ester bonds can undergo hydrolysis under moist, warm conditions, shortening chains and reducing mechanical performance. Polyether soft segments commonly improve resistance to that particular process, while oxidation, light and specific fluids introduce other considerations. Solvent swelling differs from chemical bond cleavage: swelling can sometimes reverse on drying, whereas cleavage changes the molecules. Environmental evaluation therefore benefits from measuring mass, dimensions and retained mechanical properties together.

TPU finds uses in wear surfaces, films, cables and tubing because it combines flexibility, strength, wear behavior and processability. Abrasion resistance is not a permanent ranking assigned to a polymer family. Counterface, load, speed, temperature and lubrication change the wear mechanism. Aromatic and aliphatic isocyanate structures also affect appearance after light exposure; yellowing and loss of load-bearing ability are separate observations. For contact with skin, liquids or biological environments, the particular formulation, processing residues and intended treatments belong in the assessment. The abbreviation TPU alone does not specify those conditions.

Thermoplastic copolyester elastomers, often called TPEE, commonly connect crystallizable aromatic polyester hard segments with flexible polyether segments. Hard-segment crystals act as physical junctions and reinforcement, while soft segments allow appreciable deformation at lower stress. Structures with flexible polyester soft segments also exist. Soft segments derived from poly(tetramethylene ether) glycol are common; their ether chemistry differs from the aromatic polyester hard segment. Melting the hard crystals enables flow, and cooling rebuilds organization. Cooling rate and later heat treatment can consequently alter dimensions, modulus and flex fatigue as well as appearance.

Polyamide thermoplastic elastomers use polyamide hard segments to provide hydrogen bonding and crystalline junctions, combined with polyether or flexible polyester soft segments. Polyether block amide is commonly abbreviated PEBA. Polyamide identity, soft-segment length and their ratio influence density, moisture uptake, low-temperature flexibility and recovery. Applications include repeatedly flexed tubing and lightweight resilient components. For these condensation-polymer structures, moisture control before hot processing is particularly important. Moisture plasticization during use and hydrolytic chain scission in a melt are distinct processes. Suitable drying helps retain the molecular length on which the intended behavior depends.

## Styrenic and olefin systems use different kinds of connection

Styrenic thermoplastic elastomers are often abbreviated TPS. In SBS, S denotes polystyrene end blocks and B the polybutadiene middle block. SIS instead uses a polyisoprene middle block. At suitable temperatures, polystyrene-rich domains restrain the ends while flexible middle blocks connect them into a reorganizable network. Oil, tackifying resin and other polymers can change feel, adhesion and flow. Where an additive partitions is crucial: entering the soft phase may swell that phase, while substantially softening hard domains can shorten the time for which the network sustains a load.

Selective hydrogenation of the middle block converts vulnerable carbon–carbon double bonds into more saturated structures. SEBS derived from SBS has an ethylene–butylene-type middle block; SEPS derived from SIS has an ethylene–propylene-type middle block. This improves structural stability under some oxidative and ozone-exposure conditions while retaining the styrenic end blocks. It does not mean that all aromatic rings disappear. Weathering behavior still depends on stabilizers, color, oxygen transport and temperature. Adhesion and printing also require attention to surface polarity and possible surface treatment.

Thermoplastic olefin elastomers, or TPOs, commonly combine a thermoplastic such as polypropylene with an ethylene–propylene rubber phase. The hard and soft phases can belong to different molecules. Calling them hard and soft blocks of one chain would conceal the actual structure. Rubber fraction, particle size, continuity and interfacial interactions control deformation. The thermoplastic flows during processing and supports shape again on cooling. Compositions and moduli vary widely, so a fixed rubber percentage or a single flexural-modulus threshold does not replace a description of structure and measured behavior.

Polyolefin elastomer, or POE, often refers to an elastic ethylene copolymer with a higher α-olefin. Branches interrupt regular crystallization and make the material softer. Using a particular catalyst does not automatically create clearly alternating hard and soft blocks. Olefin block copolymers, or OBCs, can instead contain continuous sequences of different crystallizability. In 2006, Arriola and colleagues reported chain-shuttling polymerization, in which growing chains move between catalysts with different monomer selectivities. Distinct sequences can thereby develop within one chain. Sequence control adds molecular connections to the broader concept of combining harder and softer phases.

Thermoplastic vulcanizates, or TPVs, take another route. The rubber phase is chemically crosslinked while the material is being mixed in the melt, a process called dynamic vulcanization. “Dynamic” means that mixing and shear continue during reaction. Breakup, coalescence and crosslinking compete, commonly producing crosslinked rubber regions in a continuous thermoplastic phase. Even at a high rubber fraction, the thermoplastic can retain connected pathways that enable hot processing. Particle size and internal crosslink density depend on formulation and processing; they are not universal constants of the TPV category.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pm10/en/#en-s7)

Figure 3 · Connections within brown regions represent rubber crosslinks; green is the continuous thermoplastic. Remolding mainly uses flow of that continuous phase and does not require breaking all rubber crosslinks. Morphology and dimensions depend on processing.

On reheating a TPV, crosslinked rubber does not melt into independent chains. The continuous thermoplastic phase flows and carries rubber regions into a new shape. Chemical crosslinking and thermoplastic processing can therefore coexist when their spatial arrangement permits it. This differs from a fully connected bulk vulcanized rubber network. Crosslinked rubber helps retain shape and can improve aspects of recovery, while measured compression set still depends on temperature, time and morphology. Repeated processing can alter chain length, stabilizer condition and phase organization, so reused material is evaluated under the intended cycle of service and remolding.

## Measure softness, recovery and long-term support separately

Pressing a surface by hand gives only a rough impression of rapid local deformation. Hardness testing specifies an indenter, load and reading time to make that observation more reproducible. Shore A and Shore D use different scales and conditions; their numbers cannot be subtracted as if they shared one linear ruler. Formulations with similar hardness can have very different tensile strength, recovery speed and wear behavior. Hardness is useful for consistency within a product series, while selecting a seal, spring-like component or cushion requires its actual deformation mode to be specified.

Elongation at break describes how far a specimen extends before failure in a particular tensile test. Elastic recovery asks where it returns after unloading. A highly extensible specimen may already have undergone substantial sliding and retain considerable extra length. A less extensible one may recover well within its smaller working cycle. Comparing footwear or flexible connectors therefore requires working strain, loading rate, cycle count and temperature, together with the unloading response. A single curve taken to rupture leaves out the time-dependent behavior that often determines performance in use.

A seal is particularly sensitive to recovery after compression. Its initial thickness is compressed to a prescribed gap, held for a specified duration and temperature, then released and allowed to recover for a defined interval. Compression set divides the thickness that remains unrecovered by the originally imposed compression. The denominator is not the original specimen thickness. Using that denominator would confuse tests with different imposed strains. A smaller result means more complete recovery under the stated procedure, while force retention during sustained compression requires a separate measurement.

Normalize compression set by imposed compressionEq. 5

![Normalize compression set by imposed compression](https://ml-biomat.com/static/agent-math/f5aa536faef46516566aae2f.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| C | Compression-set percentage under the defined procedure | % |
| h₀ | Initial thickness before compression | mm |
| hᵣ | Thickness after unloading and prescribed recovery | mm |
| hₛ | Spacer thickness during compression | mm |
| 0、r、s | Labels for initial, recovered and spacer states | 1 |

Reading the relationshipThe numerator is unrecovered thickness loss; the denominator is the originally imposed compression. Their ratio times 100% gives the fraction of imposed deformation remaining.

A worked exampleFor h₀ = 10.0 mm, hₛ = 7.5 mm and hᵣ = 9.5 mm after prescribed recovery, C = (10.0−9.5)/(10.0−7.5)×100% = 20%.

ConditionsComparisons require matched geometry, imposed compression, temperature, hold time and recovery time. This measures dimensional recovery after unloading; sustained sealing force is addressed by stress relaxation during compression.

Compression set and stress relaxation answer different questions. A specimen that recovers its shape after unloading may nevertheless have lost much of its contact force while held compressed. Conversely, some short-term residual deformation may recover after a longer wait. Seal design connects both measurements to geometry: initial squeeze, surface roughness, fluid entry and temperature cycling influence whether a leakage path develops. High short-term tensile strength does not itself determine sealing life. Useful evaluation follows the actual route by which contact and support could be lost.

Repeated motion introduces fatigue and thermal management. A small crack opens during each loading cycle, and concentrated deformation near its tip may advance it. Local dissipation also raises temperature and can accelerate physical-junction rearrangement. Adding hard material may improve initial load support while changing crack-tip deformation. Wear resistance, tear resistance, low loss and softness therefore interact. A comparison among polymer families becomes informative when specimen geometry, hardness range and test conditions are matched before structural explanations are proposed. There is no permanent ranking that applies to every TPU, TPV or TPS grade.

A complete selection route begins with the component’s action: tension, compression, bending or friction, its duration, and its temperature and fluid environment. The next step is to identify connections that remain useful over that time window, then arrange soft-segment mobility, hard-domain organization and processing accordingly. Low-temperature flexing requires sufficient soft-phase motion. Sustained warm support requires stable junctions and a suitable continuous phase. Repeated molding calls for tracking molecular and morphological changes after processing. Soft–hard combinations become useful through these measurable connections between structure, motion and the demands of a particular part.
