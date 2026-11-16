# A Chain Meets Itself and Its Solvent: Excluded Volume

Source: https://ml-biomat.com/tutorials/biomaterials-courses/cp04/en/
Language: en

Why does the same long molecule expand in one liquid, contract in another, or make a solution turn cloudy? Starting with the space occupied by a flexible chain, this chapter connects molecular contacts to coil size, mixing, osmotic pressure and concentration.

## The same chain in a different liquid

Place a drop of water on a dry cotton cloth and it spreads through spaces between fibres. Disperse a small amount of a water-soluble polymer in water and, after sufficient mixing and equilibration, the liquid may become noticeably more viscous. Both observations involve water and long molecules, but they concern different levels of structure. Cellulose chains in cotton are organized into fibres by crystallinity and intermolecular interactions. Water entering the fabric does not mean that individual cellulose chains have dissolved. In a polymer solution, by contrast, a dissolved chain is surrounded by solvent and continually changes its shape through thermal motion. This freely fluctuating chain is the starting point for the discussion.

Imagine a molecular chain as a flexible cord assembled from many short connected pieces. Its total length along the cord stays fixed, while the space it occupies can change greatly. A cord resting loosely on a table and the same cord gathered into a small ball have different spatial dimensions. At the molecular scale, thermal motion continually rearranges the chain, while the surrounding liquid changes the relative likelihood of different arrangements. A molecule does not choose a comfortable pose. Shapes that allow more microscopic variations, or that provide more favourable molecular contacts, occur more often in the statistical population. The quantity of interest is therefore the distribution of shapes and its characteristic size, rather than a predetermined path followed by one molecule.

Dissolution and swelling also need to be separated. Sugar molecules disperse in water, and many soluble polymers can similarly disperse as individual chains. If enough permanent links connect the polymer chains, however, the chains cannot leave independently. Solvent entering that connected structure usually expands the network and produces a solvent-rich gel. Expansion of a single coil and swelling of a gel both involve polymer–solvent interactions, but a gel also experiences the elastic constraint of its network. Understanding the individual chain first makes it easier to see what additional physics appears in an absorbent resin, a protein gel or a piece of rubber immersed in a solvent.

The words good and poor describe a solvent's effect on a particular polymer under specified conditions. They are not permanent quality ratings assigned to the liquid. A liquid can expand one kind of chain and promote aggregation of another; changing temperature or composition can also change the behaviour of the same polymer–solvent pair. A useful comparison of coil sizes therefore specifies chain chemistry, chain length, temperature and concentration together. This prevents a larger spatial size from being mistaken for a larger number of chemical units. The chain may contain exactly the same units while arranging them over a larger volume.

[Figure: Conformations at the same chain length under three solvent conditions](https://ml-biomat.com/tutorials/biomaterials-courses/cp04/en/#en-s1)

Figure 1 · A flexible chain of fixed length can have different conformational distributions. The diagram compares spatial expansion while chemical connectivity remains unchanged.

## A chain cannot freely pass through itself

An ideal-chain model replaces a chemically complicated molecule with a sequence of statistical segments. Each segment represents a short portion of chain whose local bending behaviour has already been incorporated into an effective length, denoted by b. The number of such segments is N. A statistical segment is generally neither a single chemical bond nor necessarily one repeat unit. With an appropriate coarse description, sufficiently separated segment directions become approximately independent. The chain can then be treated as a random walk. Its end-to-end vector has a direction, whereas the distance between its ends does not. Averaging vectors can produce cancellation; averaging squared distances preserves information about how far the chain typically extends.

The characteristic size of an ideal chainEq. 1

![The characteristic size of an ideal chain](https://ml-biomat.com/static/agent-math/f55f080b601cbb7baed9bab7.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| R₀ | Root-mean-square end-to-end distance of the ideal chain | m |
| R | End-to-end distance in one conformation | m |
| ⟨R²⟩₀ | Mean squared distance over ideal-chain conformations | m² |
| b | Statistical segment length incorporating local flexibility | m |
| N | Number of statistical segments | 1 |

Reading the relationshipSquaring before averaging prevents opposite directions from cancelling the measure of size. The final square root restores units of length. Independent isotropic segment directions make the mean squared contributions add, giving N contributions of b².

A worked exampleFor b=1 nm and N=1000, the square root of 1000 is approximately 31.6, giving R₀≈31.6 nm. The contour length is 1000 nm, much larger than the typical end-to-end distance because the chain changes direction. The result describes a population of conformations rather than every individual snapshot.

ConditionsApplies to sufficiently long ideal flexible chains described by independent statistical segments, with local stiffness incorporated into b.

The simplification has an important feature: the calculation does not separately reject every configuration in which distant segments occupy the same position. Real atoms take up space. At very short separations, their electronic structures and short-range repulsion make further approach energetically expensive. A cord that turns back toward a part of the table it already occupies must avoid the existing cord. The analogous molecular constraint is called excluded volume. It does more than restrict the angle between neighbouring segments. Parts that are far apart along the chain can still influence one another when folding brings them close in three-dimensional space.

Why does this restriction usually expand a chain in a dilute good solvent? Imagine adding another step to a chain that has already taken many steps. A step toward the interior of the existing coil is more likely to encounter an occupied region. A step outward is more likely to find free space. As the constraint accumulates, compact configurations are rejected more strongly, and the remaining population is more expanded on average. This does not mean that every individual configuration is larger than every ideal-chain configuration. Nor does it mean that the chain becomes a rigid rod. It remains a fluctuating coil, but its distribution of sizes shifts toward larger values.

The phrase long-range interaction needs careful interpretation here. It refers to separation along the sequence of connected segments. Segment one hundred and segment one thousand can be far apart along the contour yet touch after the chain folds. The hard repulsion itself still acts over a short physical distance. Confusing these two distances would suggest an unusual force reaching across an entire coil. The actual reason a polymer behaves differently is that local contact restrictions are transmitted through a long connected object, changing the collection of shapes available to that whole object.

Spatial dimension changes the probability of such encounters. A chain confined to a plane has fewer ways to avoid an occupied region than one that can also move above or below it. Two-dimensional and three-dimensional self-avoiding chains consequently have different size laws. Mathematicians can also study four or more spatial dimensions. An extra dimension in that calculation is an additional independent spatial coordinate, not simply time appended to ordinary space. As dimension increases, random paths generally find it easier to avoid meeting again. This observation became an important bridge between polymer statistics and the physics of critical phenomena.

## Solvent changes contacts and possibilities

Hard spatial exclusion alone cannot explain every polymer solution. When two segments approach, they replace previous contacts: some segment–solvent contacts disappear, while segment–segment and solvent–solvent contacts become more common. The relevant energetic quantity is the change in this whole set of contacts. Asking only whether one particular interaction is strong misses the comparison. Rearranging people around a table provides a useful analogy: the new seating pattern changes both the neighbours who are brought together and those who are separated. Molecular contacts involve dispersion forces, dipoles, hydrogen bonding and other interactions, and their net effect depends on temperature and environment.

Mixing also changes the number of possible arrangements. Two colours of loose beads confined to opposite halves of a box have fewer possible placements than beads allowed throughout the box. Statistical physics describes the contribution from the number of accessible states through entropy. A polymer introduces a crucial restriction because its beads are connected. A segment cannot exchange places independently while ignoring the rest of its chain. Consequently, the entropy gained by mixing polymer with solvent cannot be calculated by pretending that every segment is a separate small molecule. Connectivity reduces the number of independently movable objects.

During 1941–1942, Maurice Huggins and Paul Flory independently developed lattice descriptions of long-chain solutions. A lattice does not imply that a liquid contains permanent square compartments. It is a counting device: equal-volume sites record how solvent molecules and connected polymer segments occupy space. This translates the statement that a molecule is long into a restriction requiring it to occupy many connected sites. The entropy of mixing and the energy of changed contacts can then be placed in a common expression. The diagram illustrates that historical conceptual step. The polymer is not simply an enlarged small molecule; its internal connections alter the number of arrangements.

[Figure: Lattice illustration of the arrangement constraints imposed by connectivity](https://ml-biomat.com/tutorials/biomaterials-courses/cp04/en/#en-s3)

Figure 2 · The Flory–Huggins lattice idea: the same number of orange sites is occupied, but connected segments cannot choose their positions independently. Pale green sites represent solvent.

Mixing free energy in a lattice modelEq. 2

![Mixing free energy in a lattice model](https://ml-biomat.com/static/agent-math/3d9fc91049e24dbb4490fd3e.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ΔGmix | Change in Gibbs free energy on mixing | J |
| nsite | Total number of lattice sites | 1 |
| kB | Boltzmann constant relating temperature to molecular thermal energy | J·K⁻¹ |
| T | Absolute temperature | K |
| φ | Polymer volume fraction | 1 |
| m | Sites occupied by one polymer molecule in this lattice model | 1 |
| χ | Effective parameter describing unlike versus like contacts in thermal units | 1 |
| ln | Natural logarithm | 1 |

Reading the relationshipDividing by the number of sites and by thermal energy gives a dimensionless change per site. Connectivity introduces the factor 1/m in the polymer mixing term. The second term counts solvent arrangements, and the final term estimates contact contributions from the fractions of both components. The lattice occupancy m is distinguished from the statistical-segment count N.

A worked exampleFor φ=0.10, m=100 and χ=0.40, the three terms are approximately −0.00230, −0.09482 and +0.03600, summing to −0.06113. This uniform mixed state lies below the chosen separated-pure-component reference. Determining whether two mixed phases are still preferred requires comparing alternative combinations of compositions.

ConditionsUses equal-volume sites, approximate incompressibility and average contacts; χ is an effective parameter under the specified conditions.

The natural logarithm can initially be understood as an operation that turns products of statistical possibilities into quantities that can be added. A fraction between zero and one has a negative logarithm. The two mixing-entropy contributions therefore lower the free energy of mixing, whereas energetically unfavourable contacts can raise it. Free energy combines the consequences of energy and entropy into a common comparison. Under specified temperature, pressure and total composition, equilibrium favours the state with the lower appropriate free energy. The expression is useful because it identifies competing contributions and shows why the independent translational contribution from a long chain becomes small when counted per occupied site.

A single fixed value of χ cannot describe every feature of a solution with strong hydrogen bonding, charged groups, specific binding sites or a structurally complex solvent. χ is an effective parameter that collects microscopic details into a simpler description, and it can depend on temperature and composition. Changing salt concentration or acidity may alter the charge and association of proteins, polysaccharides or synthetic polyelectrolytes. These changes then alter effective contacts. To use the model sensibly, identify which interactions the description retains and which environmental conditions are fixed. A changing fitted parameter should then be related back to a molecular mechanism, rather than treated as a universal property of the polymer alone.

## Balancing expansion against the cost of stretching

Return now to a single long chain in dilute solution. Compressing its coil into a small region raises the frequency of segment contacts. Expanding it very strongly requires many segment directions to cooperate and removes many possible bends. Both extremes therefore carry a cost, and the characteristic size emerges from a competition between them. An influential argument due to Flory estimates contacts using the average segment density inside the coil instead of following every individual contact. It then combines that estimate with the statistical elastic cost of expanding an ideal chain. The resulting model is simple enough to expose the physical balance directly.

Statistical elasticity can be understood with a sequence of freely rotating short rods. When the rods point in many directions, there are many ways to arrange them. Requiring the two ends of the complete sequence to be far apart forces many rods to point in similar directions, reducing the number of available combinations. A restoring tendency thus appears even if the chemical bonds themselves have not been stretched like metal springs. It arises because more strongly bent configurations are collectively more numerous. Temperature enters through the thermal energy scale, which converts an entropy loss into a free-energy cost. The spring in this argument describes the statistics of chain conformations, rather than the extension of one chemical bond.

Expansion competes with segment contactsEq. 3

![Expansion competes with segment contacts](https://ml-biomat.com/static/agent-math/17ee653c95fc8111aae7ddbb.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| F(R) | Conformational free energy as a function of size R, omitting constants independent of R | J |
| R | Characteristic coil size | m |
| kB | Boltzmann constant | J·K⁻¹ |
| T | Absolute temperature | K |
| N | Number of statistical segments | 1 |
| b | Statistical segment length | m |
| v | Effective two-body excluded-volume parameter | m³ |

Reading the relationshipThe average segment density is of order N/R³. Pair contacts scale with its square; multiplying by coil volume gives N²/R³. The elastic term grows with R² because expansion reduces the available conformations. Both terms are dimensionless after division by kBT; replacing a detailed envelope by R³ belongs to the mean-field approximation.

A worked exampleWith b=1 nm, N=1000 and v=1 nm³, the terms at R=30 nm are approximately 1.35 and 18.52. At R=60 nm they are 5.40 and 2.31. Expansion reduces crowding while increasing the elastic cost. At R=100 nm the elastic term reaches 15 and the contact term is 0.50, showing why the total does not decrease indefinitely.

ConditionsA scaling estimate for a flexible long chain in a dilute three-dimensional good solvent, with positive v. Additional contributions matter near theta conditions or in compact globules.

Picture the total free energy as a curve with a valley. At small R, the coil is crowded and its interaction term is large. At large R, the statistical elastic term becomes large. The bottom of the valley identifies the model's preferred size. Mathematically, a derivative describes how rapidly the curve's height changes when its horizontal coordinate changes slightly. At a smooth minimum, moving a little in either direction has no first-order advantage, so the slope is zero. If only the dependence on chain length is needed, balancing the orders of magnitude of the two competing terms gives the same scaling result without requiring every numerical coefficient.

Flory scaling of coil size in a good solventEq. 4

![Flory scaling of coil size in a good solvent](https://ml-biomat.com/static/agent-math/0cc2e0327efa6966640f57f0.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| R | Characteristic coil size | m |
| b | Statistical segment length | m |
| N | Number of statistical segments | 1 |
| v | Positive effective excluded volume | m³ |
| ∼ | Scaling proportionality with numerical prefactors omitted | 1 |

Reading the relationshipMinimizing the previous expression makes the fifth power of R proportional to vb²N³. Taking the fifth root gives this scaling form. The ratio v/b³ is dimensionless, leaving units of length. The expression retains parameter dependence without treating the mean-field numerical prefactor as universal.

A worked exampleSet b=1 nm and v/b³=1, and choose unit prefactor for a scaling comparison. N=1000 then gives about 63.1 nm. Increasing N tenfold multiplies size by 10 to the power three fifths, approximately 3.98. An ideal chain grows by the square root of ten, approximately 3.16. Ratios expose the role of the exponent more directly than one absolute size.

ConditionsThree-dimensional long-chain mean-field scaling in a good solvent; more precise self-avoiding statistics give an exponent close to 0.588.

[Figure: The sum of elastic and contact free energies has a minimum](https://ml-biomat.com/tutorials/biomaterials-courses/cp04/en/#en-s4)

Figure 3 · The free-energy curve is normalized by its minimum and by the size at that minimum. Compression raises the contact cost; expansion raises the conformational cost; the sum has an intermediate minimum.

The most useful conclusion is how size grows when the chain contains more segments. In a three-dimensional good solvent, the Flory estimate gives a power of three fifths; more precise statistics for long self-avoiding chains give an exponent of about 0.588. Both exceed the ideal-chain exponent of one half. The accumulated effect of excluded volume therefore becomes more evident as chain length increases. An exponent of one third describes a compact globule whose internal density remains approximately fixed. These exponents compare size changes across a population of chain lengths. They do not imply that every short real chain must lie exactly on a power law with a coefficient equal to one.

The mean-field picture also reveals what the calculation leaves out. Segment density varies throughout a real coil, and contact events are correlated. A segment occupying one region changes the probability of finding other segments nearby. Replacing all of those local fluctuations with a single average density provides a transparent approximation, but a more detailed treatment is needed near theta conditions, for short chains or for especially specific interactions. The purpose of learning the balance is to acquire a way of reasoning about scales and trends. A clear scaling law becomes useful when its physical assumptions remain attached to it, rather than when its exponent is treated as a universal size prescription for every polymer.

## Theta conditions: cancellation without disappearing atoms

Suppose a change in solvent or temperature strengthens the effective attraction between segments. The expansion promoted by spatial exclusion then weakens. Near a particular condition, effective two-body attraction and repulsion compensate, and long chains approach ideal-chain size scaling. This is the theta condition. Effective is an essential word: solvent molecules may be omitted from the drawing of the chain, but they participate in contact exchange and in the free-energy balance. Atoms retain their finite size, and segments do not become capable of occupying precisely the same microscopic space. What cancels is a net contribution after interactions and solvent effects have been statistically combined.

The effective excluded-volume parameter v measures the net statistical cost of close pair contacts. Positive v suppresses close approach and promotes expansion; negative v favours close approach and can promote contraction. When v is close to zero, the two-body contribution is small. These signs do not assign a negative geometrical volume to an atom. They compare the statistical weighting of nearby configurations with and without the effective interaction. A discount can cancel part of a bill without removing the goods from the shopping bag. In a similar way, cancellation in a statistical interaction parameter does not remove the physical size of the segments.

Relating excluded volume to solvent qualityEq. 5

![Relating excluded volume to solvent quality](https://ml-biomat.com/static/agent-math/51f91487c83013fd627c9728.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| v | Effective two-body excluded volume | m³ |
| vs | Reference volume of a segment in the chosen coarse-grained lattice | m³ |
| χ | Effective polymer–solvent contact parameter | 1 |

Reading the relationshipExpanding the lattice mixing free energy at low polymer concentration gives a quadratic term containing 1−2χ. This combines occupancy repulsion and contact attraction into one coefficient. The reference volume vs supplies units of volume. Its value follows the coarse-graining convention and need not equal the cube of the statistical segment length.

A worked exampleFor vs=1 nm³, χ=0.30 gives v≈0.40 nm³. At χ=0.50 the two-body approximation gives zero. At χ=0.70 it gives v≈−0.40 nm³. The negative value means that effective contacts favour approach; it does not describe a negative geometrical segment volume.

ConditionsAn approximate relation in a simple lattice mean-field description. Experimental theta conditions involve the long-chain limit and the second virial coefficient; χ may depend on composition.

Experimentally, theta conditions are often identified by a second osmotic virial coefficient that approaches zero. As the next section explains, the first osmotic term counts independently translating molecules, while the second records effective interactions between them. Removing that second contribution therefore has a clear experimental meaning. Finite chain length, end effects and higher-order interactions can still produce corrections. Treating theta conditions as a well-defined long-chain reference is more useful than imagining an instant at which every real interaction disappears. This reference helps separate local chain flexibility from additional expansion caused by the surrounding solvent.

An athermal solvent model is different from a theta solvent. In the athermal approximation, the energetic change on mixing is taken to vanish, while hard occupancy restrictions remain. Such a chain normally displays self-avoiding expansion. An athermal environment is not equivalent to vacuum. Theta conditions instead involve compensation between attractive and repulsive contributions at the effective two-body level. In vacuum, a chain has no surrounding solvent, and its internal attractions, temperature and chemical structure determine its conformation. The absence of solvent alone does not establish athermal self-avoiding behaviour. Each environment can be modelled, but the retained interactions must be identified correctly.

Under still poorer solvent conditions, a chain can form a denser globule, and multiple chains may aggregate or separate into regions of different composition. Single-chain collapse and macroscopic phase separation are related phenomena, but they are not the same observable. The first concerns the dimensions of an individual chain; the second concerns differences in average composition between regions. Protein folding introduces additional sequence-specific contacts, directional hydrogen bonding and preferred local structures. It is therefore more detailed than the globule formation of a chemically uniform flexible chain. The general collapse picture provides a starting point to which those biological features can be added.

## Measuring a coil that cannot be seen directly

A polymer coil in solution is generally too small to resolve with an ordinary light microscope, but it influences both the surrounding liquid and an applied probe. Those influences provide indirect measurements of molecular size and interactions. Osmosis offers an accessible example. A membrane separates pure solvent from a polymer solution and allows solvent molecules, but not polymer chains, to pass. Solvent can enter the solution compartment and establish a difference in liquid level. Applying an additional pressure to the solution side can stop the net transfer. The extra pressure required at equilibrium is the osmotic pressure.

Saying that the polymer simply pulls water through the membrane misses part of the thermodynamics. Solvent has different chemical potentials on the two sides because mixing changes its free-energy contribution. Pressure also changes the solvent's chemical potential. Equilibrium occurs when these effects balance. In a sufficiently dilute solution, interactions between polymer molecules make only a small correction, and the leading osmotic term mainly counts independently translating chains. Equal masses of shorter chains contain more separate molecules than equal masses of longer chains. They therefore give a larger contribution to this leading term, even though the total mass of polymer is unchanged.

Reading molecular counting and interactions from osmotic pressureEq. 6

![Reading molecular counting and interactions from osmotic pressure](https://ml-biomat.com/static/agent-math/4e8ab656a8329f811906bad8.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Π | Osmotic pressure | Pa |
| Rg | Molar gas constant, not the radius of gyration here | J·mol⁻¹·K⁻¹ |
| T | Absolute temperature | K |
| c | Polymer mass concentration | kg·m⁻³ |
| Mn | Number-average molar mass | kg·mol⁻¹ |
| A₂ | Second virial coefficient defined using mass concentration | m³·mol·kg⁻² |
| ⋯ | Terms of higher order in concentration | mol·m⁻³ |

Reading the relationshipDividing c by Mn gives moles of chains per volume; multiplication by RgT gives the ideal dilute-solution pressure. A₂c² is the leading interaction correction, with higher concentration powers capturing further contributions. Both sides have units of moles per volume. Mass concentration and segment number density therefore cannot be interchanged without conversion.

A worked exampleAt T=298 K, c=1 kg/m³ and Mn=100 kg/mol, with A₂ set to zero, the chain concentration is 0.010 mol/m³. Multiplying by 8.314 J/(mol·K) and 298 K gives about 24.8 Pa. Halving Mn at the same mass concentration doubles the leading pressure because there are twice as many independent chains.

ConditionsA dilute-solution equilibrium virial expansion with a membrane permeable to solvent but retaining polymer; the number of terms retained must match the concentration range.

The second virial coefficient A₂ supplies the first correction beyond independent molecular counting. A positive value raises the osmotic pressure relative to the leading dilute-solution term at the same mass concentration; a negative value changes it in the opposite direction. Dividing a series of low-concentration measurements by concentration and extrapolating toward zero concentration separates the intercept associated with number-average molar mass from the initial slope associated with A₂. This provides an experimental route to distinguish molecular mass from effective interactions. At higher concentrations, additional terms become important. The fitted concentration interval must then be chosen to match the level of approximation used in the analysis.

Viscosity supplies another window into the coil. During slow flow through a narrow tube, added chains disturb the surrounding velocity field and change the resistance to flow. Comparing the solution with pure solvent and then extrapolating to vanishing polymer concentration isolates a contribution per unit polymer mass, called intrinsic viscosity. Despite its name, its units are volume divided by mass, rather than the pascal-second units of ordinary dynamic viscosity. The distinction follows directly from dividing a relative viscosity increase by mass concentration. A larger coil can influence a larger hydrodynamic region, although its detailed effect also depends on shape and on how easily solvent moves through that region.

Intrinsic viscosity: flow influence per unit polymer massEq. 7

![Intrinsic viscosity: flow influence per unit polymer mass](https://ml-biomat.com/static/agent-math/14c3e8d6a7f5a101e8b9cdc3.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| [η] | Intrinsic viscosity; brackets denote this particular quantity | m³·kg⁻¹ |
| η(c) | Zero-shear dynamic viscosity of the solution at concentration c | Pa·s |
| ηs | Dynamic viscosity of the pure solvent at the same temperature | Pa·s |
| c | Polymer mass concentration | kg·m⁻³ |
| lim c→0 | Limit obtained by extrapolating low-concentration measurements toward zero | — |

Reading the relationshipSubtract solvent viscosity and divide by it to obtain a dimensionless relative increase. Dividing that increase by mass concentration gives a contribution per unit concentration. Extrapolation toward zero reduces interchain contributions and explains why intrinsic viscosity has units of volume per mass.

A worked exampleIf the viscosity increase is 2% at c=0.10 kg/m³, the reduced value at that concentration is 0.02/0.10=0.20 m³/kg. Measurements at lower concentrations and extrapolation are needed to determine [η]. The single value 0.20 m³/kg is one point in that extrapolation, not automatically the limiting result.

ConditionsCompare stable dilute solutions under matching temperature and solvent conditions at sufficiently low shear rate.

For one polymer in a specified solvent at a fixed temperature, intrinsic viscosity often follows an approximate power law over a useful molar-mass range. The Mark–Houwink relation connects an accessible flow measurement with the mass scale of the chains, but its coefficient and exponent must be determined for that particular system. If the sample contains many chain lengths, viscosity measures a viscosity-average molar mass: an average weighted by the contribution to viscosity. It generally differs from the number-average molar mass obtained from osmotic measurements. Two different reported averages for the same polydisperse sample therefore need not mean that one instrument is wrong. The measurements assign different weights to the chain-length distribution. This distinction becomes especially useful when degradation, fractionation or blending changes the distribution rather than merely shifting every chain length by the same factor.

A power law connecting intrinsic viscosity and molar massEq. 10

![A power law connecting intrinsic viscosity and molar mass](https://ml-biomat.com/static/agent-math/12769af35b6e1f1422a23dcc.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| [η] | Intrinsic viscosity | m³·kg⁻¹ |
| K | Coefficient for the specified polymer, solvent, temperature and unit convention | (m³·kg⁻¹)/(kg·mol⁻¹)^a |
| Mη | Viscosity-average molar mass | kg·mol⁻¹ |
| a | Mark–Houwink exponent | 1 |
| ν | Chain-size scaling exponent | 1 |

Reading the relationshipFor a flexible chain whose hydrodynamic motion approximately entrains its coil volume, intrinsic viscosity scales as that volume divided by chain mass. Cubing the size introduces 3ν, while dividing by mass subtracts one power, giving a≈3ν−1. This supplies a physical interpretation; K and a are established for the actual system.

A worked exampleFor a=0.8 within the selected system and molar-mass range, doubling viscosity-average molar mass multiplies intrinsic viscosity by 2 to the power 0.8, approximately 1.74. K cancels in this ratio, provided both measurements share the same K and a.

ConditionsA dilute-solution relation for a specified system; the connection between a and ν assumes flexible, approximately non-draining coils.

Light and neutron scattering obtain spatial information from the dependence of scattered intensity on angle. A probe with a known wavelength receives contributions from different positions within the sample. These contributions can reinforce or partially cancel one another, so their angular pattern contains information about distances. Neutron measurements can also exploit the contrast between hydrogen and deuterium to distinguish selected chains among chemically similar neighbours. Different methods observe different responses. Used together, they help distinguish a change in coil size from a change in molar-mass distribution, aggregation or solvent properties. An increased viscosity alone cannot separate all of these contributions.

## When coils overlap: concentration introduces a new scale

Dilute does not simply mean a small mass percentage. It means that different coils are usually well separated. A long chain resembles a very sparse cloud: solvent fills much of the volume inside its spatial envelope, while segments occupy only a fraction. Many long-chain coils can consequently overlap even when polymer contributes a small proportion of the solution's mass. To decide whether a solution is dilute, compare the mass of one chain with the typical spatial volume occupied by that chain in the chosen solvent. A single concentration threshold cannot apply to all chain lengths, chemistries and solvent conditions.

Estimating overlap from coil volumeEq. 8

![Estimating overlap from coil volume](https://ml-biomat.com/static/agent-math/ad9aa8333c188188c84ae081.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| c* | Overlap scale expressed as mass concentration | kg·m⁻³ |
| M | Molar mass of the chains being compared | kg·mol⁻¹ |
| NA | Avogadro constant | mol⁻¹ |
| Rgyr | Radius of gyration describing segment positions around the centre of mass | m |
| π | The circle constant pi | 1 |

Reading the relationshipM/NA is the mass of one chain. Dividing by a spherical envelope based on its radius of gyration gives the concentration at which each envelope contains about one chain. A real coil has no fixed spherical boundary, so the numerical prefactor depends on the convention used for its size.

A worked exampleFor M=100 kg/mol and Rgyr=20 nm, the spherical envelope is about 3.35×10⁻²³ m³ and one chain has mass 1.66×10⁻²² kg. The estimated c* is about 4.96 kg/m³, or 4.96 g/L. Doubling the radius at fixed chain mass reduces the estimate by a factor of eight.

ConditionsUseful for a characteristic overlap scale in a relatively narrow chain-length distribution; broad distributions involve different overlap scales for different chains.

The overlap concentration is a scale estimate, not a claim that every coil suddenly touches its neighbours like identical hard spheres. Coil boundaries fluctuate, and a sample may contain a distribution of chain lengths. Overlap means that their spatial segment distributions begin to interpenetrate substantially. As concentration rises, a segment increasingly encounters segments belonging to other chains as well as distant portions of its own chain. The environment created by those neighbouring chains screens the effective excluded-volume interaction on larger length scales. This is a collective effect of the surrounding polymer, rather than a change that makes individual atoms occupy less space.

[Figure: Coil overlap and correlation blobs in dilute and semidilute solutions](https://ml-biomat.com/tutorials/biomaterials-courses/cp04/en/#en-s7)

Figure 4 · As coil envelopes interpenetrate, neighbouring chains influence larger-scale statistics. The dashed circle indicates a correlation-length scale ξ, rather than a physical membrane.

A useful description divides a chain into correlation blobs. A blob is not a newly created chemical particle. It is a scale of observation. Inside its characteristic size, the chain retains self-avoiding statistics similar to those of a dilute good-solvent chain. At larger scales, neighbouring chains contribute strongly to the environment and screened statistics emerge. The characteristic blob size is denoted by ξ and called the correlation length. This picture preserves the distinction between local and global behaviour. It explains more than the statement that excluded volume has disappeared, because the same chain can obey different statistical descriptions when viewed at different magnifications.

Correlation length in a semidilute solutionEq. 9

![Correlation length in a semidilute solution](https://ml-biomat.com/static/agent-math/5f4ccffdf02a0e00cb67e53f.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ξ | Correlation-blob size | m |
| Rgyr | Dilute good-solvent radius-of-gyration scale for the chain | m |
| c | Current polymer mass concentration | kg·m⁻³ |
| c* | Overlap concentration using the same size convention | kg·m⁻³ |
| ν | Chain-size exponent within a blob | 1 |
| ∼ | Scaling relation with numerical prefactors omitted | 1 |

Reading the relationshipWithin a blob, chain size retains good-solvent scaling, while its average segment concentration is of the same order as the solution concentration. Combining those requirements eliminates the number of segments per blob and gives the concentration exponent. The ratio c/c* is dimensionless, and the negative exponent makes the correlation length decrease with concentration.

A worked exampleUsing ν=3/5 gives an exponent of −3/4. For Rgyr=20 nm and c/c*=10, with unit scaling prefactor, ξ≈20×10⁻³ᐟ⁴ nm≈3.56 nm. The blob is smaller than the dilute coil, indicating that neighbouring chains influence its larger internal scales.

ConditionsFor three-dimensional flexible polymers in the good-solvent semidilute regime, with correlation length larger than the local segment scale; highly concentrated or specifically associating systems require a modified description.

Pierre-Gilles de Gennes made extensive use of scaling and correlation-length arguments in polymers and other soft materials. His 1991 Nobel lecture discussed how relatively small changes in molecular constraints can produce substantial macroscopic changes. The method relevant here is to identify the length scale controlling the behaviour, instead of beginning with a description of every atom. In a semidilute solution, increasing concentration reduces the correlation length. The region over which a chain behaves approximately like an isolated expanded chain therefore becomes smaller. Osmotic pressure, scattering and chain dimensions can then be interpreted through related physical scales.

Overlap, entanglement and gelation answer different questions. Overlap concerns the interpenetration of coil volumes. Entanglement concerns topological restrictions on large-scale chain motion and therefore involves time as well as geometry. Gelation concerns a connected network that persists over the observation period. A solution can have overlapping coils without showing a strong entanglement plateau or a persistent gel network. Static measurements describe spatial organization; dynamical and mechanical measurements show how long that organization constrains motion. Keeping these distinctions separate makes it possible to explain why a highly viscous polymer solution can still flow slowly.

## Reading size, interactions and concentration together

Imagine three solutions containing the same polymer with the same chain length and polymer mass concentration, but different solvent conditions. Chains in the first are expanded, those in the second are near theta conditions, and those in the third tend to contract. For an individual chain this produces different characteristic dimensions. For a collection of chains, the more expanded coils occupy larger spatial envelopes and therefore reach overlap more readily at the same mass concentration. Solvent quality changes both the statistics of a single molecule and the classification of the whole solution as dilute or semidilute. These two consequences follow from the same change in spatial size.

The interactive plot compares three size-scaling laws. Change the number of segments and observe how ideal chains, good-solvent chains and compact globules respond to a tenfold increase in chain length. To isolate the role of the exponent, the plot uses a segment length of 1 nm and sets the proportionality coefficient to one for each curve. It is therefore a comparison of scaling models. Selecting a solvent condition highlights the corresponding curve and reports the current characteristic size. For a particular material, the statistical segment length and prefactor must be established from its chemistry or from measurements.

[Figure: Logarithmic plot of coil size against segment count](https://ml-biomat.com/tutorials/biomaterials-courses/cp04/en/#en-s8)

Vary chain length to compare three scaling laws. On logarithmic axes, a power law becomes a straight line whose slope is the size exponent.

Now turn the ideas into a materials question. Suppose the viscosity of a solution of a water-soluble long-chain polymer decreases markedly on cooling. Does this immediately show that the chemical chains have broken? Several possibilities must be distinguished. The chains could contract because solvent quality changes; the solvent's own viscosity could change; molar mass could genuinely change; or aggregation could alter the measured response. Establishing chain scission requires molar-mass information and comparisons under matching solvent conditions. Reversibility on returning to the original temperature provides a useful clue, but it should be interpreted together with the other measurements rather than as a complete diagnosis by itself.

Another useful question is why longer chains can have such a strong effect on flow. At fixed polymer mass, longer chains mean fewer independently translating molecules, so the leading ideal osmotic contribution decreases. At the same time, each chain influences a larger spatial region, the overlap concentration falls, and constraints during flow can become more pronounced. There is no contradiction. Osmotic molecular counting and viscous resistance describe different responses. Identifying the observable before choosing the relevant structural scale is an essential habit when using equations to explain a material.

A practical reasoning sequence begins by specifying polymer chemistry, solvent, temperature, mass concentration and the range of chain lengths. Next ask whether local flexibility makes a flexible-chain description appropriate, and whether charges or specific associations require additional physics. Compare coil size with the overlap concentration to choose between dilute and semidilute descriptions. Finally identify what osmotic pressure, scattering or viscosity measures in the chosen model. This produces an explanation that suggests a useful next measurement. It is more informative than saying that interactions have simply become stronger, because it identifies which interaction, which scale and which observable are involved.

Consider: what happens to the estimated overlap concentration if the radius of gyration doubles?

Keep the chain's molar mass fixed and use the same spherical-envelope convention. Envelope volume is proportional to the cube of the radius, so doubling the radius increases that volume eightfold. The estimated overlap concentration therefore falls to one eighth of its original value. Deciding whether a solution is dilute consequently requires the coil size under the actual solvent conditions. Most of the added envelope volume is occupied by solvent; the result does not mean that the solid volume of polymer material has increased eightfold.

Consider: why can a polymer still show distinctly polymeric behaviour under theta conditions?

Theta conditions suppress the leading effective two-body interaction contribution; they do not disconnect the chain into separate small molecules. The molecule still has a long contour, a large population of connected conformations and motion on timescales unlike those of small solutes. Local stiffness, molar-mass distribution, higher-order interactions and concentration also remain relevant. Nearly ideal size statistics can therefore coexist with strongly polymeric flow, diffusion and mixing behaviour.
