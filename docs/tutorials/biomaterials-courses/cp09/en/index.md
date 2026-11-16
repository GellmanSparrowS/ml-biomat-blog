# From Branches to Gels: Fractals, Percolation and Networks

Source: https://ml-biomat.com/tutorials/biomaterials-courses/cp09/en/
Language: en

Why can a liquid become a connected load-bearing material? How does a sparse set of conducting fillers span a specimen? Begin with shapes that remain irregular under magnification, then follow connection, mechanical support and solvent uptake to distinguish gel formation from gel-volume transitions.

## What a spanning path can change

An uncured resin flows down a cup. After reaction proceeds, a molecular network can extend across the specimen even though its overall composition has changed little. Adding conducting particles to an insulating polymer can likewise produce a pronounced resistance decrease near a certain loading. The first example concerns chemical connections and sustained mechanical support; the second concerns electrical paths. Both raise a geometrical question: when do many locally connected units form a cluster that extends through a whole sample?

A cluster is a set of units mutually reachable through the permitted connections. Two nearby particles need not be electrically connected. Two interpenetrating polymer chains need not share a permanent chemical junction. Network analysis therefore starts by specifying nodes and connections. For a chemical gel, nodes can represent branching or crosslink positions, with intervening strands represented by edges. For a conducting composite, nodes can represent fillers, while an edge satisfies a chosen contact-resistance or tunnelling criterion. Changing the connection rule changes the network being studied.

Connectivity is also distinct from rigidity. A large framework made from slender rods and freely rotating hinges may span a table yet fold easily in some directions. A flexible polymer network resists deformation because junctions constrain motion and deformation changes available chain conformations. Rigidity in a particle framework additionally depends on contact directions, bending constraints and mechanical balance. A single connected route may carry current; stabilizing a three-dimensional shape requires suitable mechanical constraints. The associated thresholds can be close or separate in particular models.

Time belongs in the definition of connection. Reversible hydrogen bonds or ionic pairs can constrain chains like junctions over short intervals, then dissociate and rearrange over longer ones. Tilting a container for seconds and leaving it inclined for hours can consequently give different impressions of flow. Equilibrium elasticity of a permanent chemical network differs from finite-frequency elasticity of a transient network. Measuring a storage modulus at one frequency does not make every temporary contact a permanent crosslink. The lifetime of a junction must be compared with the observation time.

Three questions organize this chapter: how a complicated cluster occupies space, how random connections create a spanning structure, and how an existing network supports load and takes up solvent. The first calls for fractals and scale, the second for probability and percolation, and the third for chain entropy and free energy. These questions are related but have different observables. A branching micrograph alone does not determine gel point, elastic modulus and swelling ratio together. Separating the concepts identifies which additional measurement would answer each question.

A real material may contain one large network alongside many unattached molecular clusters. In a suitable solvent, the free fraction can gradually be extracted while the network swells and retains overall connectivity. The remaining gel fraction measures the mass incorporated into the insoluble network; the extracted sol fraction measures material outside it. When spanning connectivity first appears, all molecules need not already belong to that network. Gelation therefore need not resemble the simultaneous locking of every molecule. The coexistence of network and soluble clusters is a structural feature with direct consequences for extraction, mechanical strength and subsequent swelling measurements.

## How fractal dimension describes an open structure

A long ruler used along a winding coastline skips small inlets. A shorter ruler follows more detail and may give a greater total length. In his 1967 discussion of coastline length and statistical self-similarity, Mandelbrot emphasized the role of measurement scale. The useful idea is to replace a vague statement that a shape is complicated with a testable question: how does measured length, enclosed mass or covering-box count change when observation scale changes? A fractal description concerns scaling rather than merely an irregular appearance.

Start with uniform objects. Doubling the observation radius along a slender straight line approximately doubles included mass. In a uniform sheet, area and mass increase fourfold. Inside a uniform three-dimensional solid they increase eightfold. These changes follow the first, second and third powers of length. For a cluster containing branches and voids, mass can grow at a rate between such cases. Its mass fractal dimension is the exponent describing that growth, quantifying how effectively the cluster fills space over the specified range.

Mass growth with observation scaleEq. 1

![Mass growth with observation scale](https://ml-biomat.com/static/agent-math/54a1bfd782d41b2983bfb42e.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| M(r) | Mean cluster mass within radius r | kg |
| M₀ | Mass scale associated with reference length a | kg |
| r | Observation radius | m |
| a | Reference microscopic length | m |
| df | Mass fractal dimension | 1 |
| ≃ | Approximation over a specified scale range | 1 |

Reading the relationshipThe ratio r/a is dimensionless. The exponent determines mass multiplication as length increases, describing space filling. Averaging generally uses multiple centres or clusters.

A worked exampleFor df=1.5, increasing r from 10a to 20a multiplies mass by 2^1.5≈2.83. A mass of 1 ng becomes about 2.83 ng.

ConditionsStatistically self-similar mass distribution above the local-unit scale and below cluster or correlation-length cutoffs, with a consistent mass-measurement definition.

The exponent does not create an additional spatial direction. A planar cluster with mass dimension 1.7 still lies in a two-dimensional plane. The value describes how accumulated mass increases with radius. Taking logarithms of mass and radius turns a power law into an approximately straight relation whose slope gives the exponent. Logarithms convert multiplicative changes of scale into additive distances on the graph. If every doubling of radius produces approximately a tripling of mass, the exponent is close to log 3 divided by log 2. No coordinate has acquired a fractional physical direction.

The Sierpiński triangle provides a directly checkable geometrical example. Divide a filled triangle into four triangles with half the original side length, remove the central one, and repeat on the three survivors. At each step there are three similar copies, each reduced by a factor of two in length. These two numbers determine the dimension. This mathematical construction has exact self-similarity, whereas coastlines and polymer clusters are generally statistically self-similar and only over a finite range. Individual branches need not reproduce one another exactly.

Dimension from similar copiesEq. 2

![Dimension from similar copies](https://ml-biomat.com/static/agent-math/ce70315e7b500615f1db7ff3.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| df | Dimension of the self-similar construction | 1 |
| m | Number of similar copies retained at each step | 1 |
| b | Ratio of original to copy length, greater than one | 1 |
| ln | Natural logarithm, converting multiplicative scaling into addition | 1 |

Reading the relationshipA length ratio b corresponds to m copies, so b^df=m. Taking logarithms solves for the exponent; any common logarithm base gives the same ratio.

A worked exampleThe Sierpiński triangle has m=3 and b=2, giving df=ln3/ln2≈1.585. Four half-side copies of a filled square give ln4/ln2=2.

ConditionsIdeal self-similar constructions with appropriately separated copies. General images require measured scaling rather than a visually guessed copy count.

[Figure: First three construction levels of the Sierpiński triangle](https://ml-biomat.com/tutorials/biomaterials-courses/cp09/en/#en-s2)

Figure 1 · This original geometrical construction shows exact self-similarity through three half-size copies per step. Real materials generally exhibit statistical self-similarity between particle and specimen cutoffs. Empty area increases with iteration; dimension describes the scaling relation.

A fractal dimension need not always be noninteger, and a picture does not possess one uniquely defined complexity number. Mass dimension, boundary dimension and box-counting dimension answer different questions. They coincide for some ideal constructions, but material measurements must specify the definition. Box counting overlays grids with progressively smaller cells, counts cells intersecting the structure, and examines the scale dependence. Counting a filled region instead of its outline changes the quantity. Image threshold, pixel size and field of view also affect the usable interval and should be checked before comparing images.

For a polymer or particle cluster, scales below a lower cutoff resolve individual segments or particles, so the same power law no longer applies. Beyond an upper cutoff, the cluster is a finite object, or many clusters together form an approximately uniform medium. A convincing dimensional analysis identifies an interval between these limits and checks whether its slope persists across fields of view or samples. A nearly straight line over a narrow interval can describe a local trend. A claim spanning many scales requires correspondingly broader measurements. This practical distinction makes fractal analysis useful for aggregation and network structure without turning every rough-looking image into the same kind of object.

## Random connections and the percolation threshold

Treat every intersection of square graph paper as a node, allow only horizontal and vertical nearest-neighbour connections, and retain each edge independently with probability p. This defines a simple bond-percolation model. Probability p does not require every finite drawing to contain exactly that fraction of edges. It gives each candidate edge the same chance of being retained, so individual samples fluctuate. Randomly retaining nodes instead, then connecting adjacent retained nodes, defines site percolation and generally changes the threshold.

Broadbent and Hammersley's 1957 work organized questions of access through random media into percolation theory. The fluid can mean liquid in pores or an abstract transferable quantity; the essential question is which connections the medium permits. At small p, a large network generally contains finite small clusters. Increasing p creates larger clusters that merge until connections can extend arbitrarily far. The probability parameter at which an infinite connected structure first becomes possible defines a percolation threshold. An infinite network is an analytical limit, whereas every experimental specimen has specified dimensions and boundaries.

For independent nearest-neighbour bond percolation on the infinite two-dimensional square lattice, the threshold is exactly one half; Kesten proved this result in 1980. At exactly one half this model has no infinite cluster. The threshold separates the behaviours on either side rather than already containing a finite infinite-cluster fraction. The value belongs to this precisely defined model. A different lattice, correlated edges or site rather than bond occupation can change it. A finite grid can occasionally span from left to right below one half, or fail to span in one realization above it. The infinite-system threshold and the first spanning value in one finite realization are different quantities, even when they are studied with the same drawing rules.

[Figure: Random bonds and left-to-right spanning on a finite grid](https://ml-biomat.com/tutorials/biomaterials-courses/cp09/en/#en-s3)

20×16 nodes, open boundaries, all nodes present, independently retained nearest-neighbour bonds. Green marks spanning clusters; without spanning, orange marks the largest cluster.

At fixed realization, increasing p only adds connections. New realizations expose finite-sample variation at the same probability. The realized edge fraction need not equal the specified probability exactly.

All nodes remain present in the interaction; only edges change. For a fixed random realization, every candidate edge receives a random number between zero and one in advance and appears when its number is smaller than p. Increasing p therefore only adds edges and never removes existing ones. This coupling lets you follow a particular cluster merger and identify a new connection that completes a left-to-right route. Choosing another realization can change the shape and spanning outcome at the same p, exposing the randomness of a finite sample.

First lower p to zero and inspect the isolated nodes. Then raise it to one and check that the grid is connected. Next, near 0.5, repeatedly choose a new realization and compare spanning and nonspanning samples. Read largest-cluster fraction separately from the spanning indicator. A large cluster need not reach the specified opposite sides, whereas a relatively slender cluster can span first. For real specimens, specify the direction of spanning and whether boundaries are open or periodically connected. These choices define the observation rather than merely decorate the diagram.

To estimate large-system behaviour, repeat realizations at several grid sizes and plot spanning probability against p. A jump in one picture is not a fixed material constant. The crossover generally sharpens as size increases, with details influenced by dimension, shape and boundaries. In actual polymers, chain connectivity, diffusion and reaction chemistry constrain junction locations, so connections are not usually fully independent. The square-lattice model isolates the collective consequences of connectivity and supplies a clear reference against which more specific network models can be compared.

## How to average over clusters

When a liquid contains many small clusters and a few large ones, mean cluster size has no unique meaning. Randomly choosing a cluster gives every cluster equal probability. Randomly choosing a unit and asking how large its cluster is makes larger clusters more likely because they contain more units. The first is a number average over clusters; the second is weighted by unit count. They answer different experimental questions, much as selecting a school at random differs from selecting a student and asking the size of that student's school.

Suppose two clusters contain 1 and 99 identical units. Their number-average size is 50. A randomly selected unit has a 1% probability of belonging to the one-unit cluster and a 99% probability of belonging to the 99-unit cluster. The expected size is consequently 0.01 times 1 plus 0.99 times 99, or 98.02. The large cluster raises this weighted average, but the answer is not simply the largest size, 99. Writing the sampling procedure explicitly explains why an extra factor of cluster size enters the numerator of the corresponding sum.

Two cluster averagesEq. 3

![Two cluster averages](https://ml-biomat.com/static/agent-math/8136f1fcc1ea835c13f6d7f8.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Sₙ | Mean unit count for a randomly selected cluster | 1 |
| Sw | Mean cluster size seen by a randomly selected unit | 1 |
| s | Number of units in a cluster class | 1 |
| nₛ | Number of clusters containing s units | 1 |
| Σₛ | Sum over all included cluster sizes | 1 |

Reading the relationshipClusters receive equal weight in cluster sampling. Unit sampling adds a factor s to the probability of encountering a size-s cluster, producing s² in the numerator.

A worked exampleFor one 1-unit and one 99-unit cluster, Sₙ=(1+99)/2=50 and Sw=(1²+99²)/(1+99)=98.02.

ConditionsEqual-mass units. Critical finite-cluster averages exclude the infinite or designated spanning cluster by an explicit convention, consistently in both sums.

Percolation theory commonly excludes the infinite cluster when evaluating this weighted mean, focusing on finite clusters. On a finite graph, an analysis must state how a designated spanning cluster is excluded or which alternative finite-size convention it uses. The purpose is to follow growing finite fluctuation structures rather than allow a macroscopic cluster to dominate the sum. The fraction of units in the infinite cluster is described separately. One observable concerns the remaining finite clusters; the other measures the newly formed macroscopic connected component.

Near threshold, clusters of many sizes coexist and a description based on one typical small aggregate becomes inadequate. A connectivity correlation length characterizes the spatial range over which separated nodes remain correlated through membership of a finite cluster. It is not a cluster mass. A long slender cluster can reach far while containing much less material than a compact object of the same extent. The fractal structure of a critical cluster relates mass growth to spatial range, bringing fractal geometry and percolation together at this point.

Connectivity scaling near thresholdEq. 4

![Connectivity scaling near threshold](https://ml-biomat.com/static/agent-math/d9418a93fffc84cd4e39cde3.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| P∞ | Fraction of units belonging to the infinite cluster | 1 |
| A | Nonuniversal order-parameter amplitude | 1 |
| p | Independent bond-retention probability | 1 |
| pc | Infinite-system percolation threshold | 1 |
| β | Critical exponent of infinite-cluster fraction | 1 |
| ξ | Connectivity correlation length of finite clusters | m |
| ξ₀ | Length amplitude, potentially different on the two sides | m |
| ν | Correlation-length critical exponent | 1 |
| \|p−pc\| | Nonnegative distance from threshold | 1 |

Reading the relationshipPower laws separate exponents and amplitudes: the macroscopic cluster grows on the upper side while the correlation range increases toward threshold.

A worked exampleFor ordinary two-dimensional percolation, β=5/36 and ν=4/3. Halving distance from threshold on one side multiplies P∞ above threshold by about 0.908 and ξ by about 2.52. Ratios eliminate amplitudes.

ConditionsThe first relation applies only for p>pc. Critical scaling range and appropriate infinite-size limit; finite specimens, other dimensions and correlated connections require separate treatment.

These power laws describe a range sufficiently close to threshold but not yet cut off by specimen size. Once the correlation length approaches the sample width, further approach to threshold cannot produce a literally infinite length in that specimen. Filler-size distributions, correlated connections and spatial dimension also affect which critical exponents apply. Conductivity, gel fraction and elastic modulus are different observables. Their changes near a common transition do not justify assigning them the same exponent. Transport and mechanics introduce information beyond cluster membership.

Data analysis can therefore begin with a concrete question. To determine how much material joins the large network, measure gel fraction or a matching connectivity fraction. To characterize finite aggregates, determine their size distribution and weighted mean. To study electrical transport, include connection resistances and conductivity. Reporting number and weighted averages together can reveal the influence of rare large clusters more clearly than an unspecified mean diameter. Once every quantity has an explicit sampling interpretation, scaling relations become comparable statements about material structure rather than interchangeable fitting formulas.

## How branching reactions form a chemical gel

Joining the ends of linear chains often creates longer lines. Branching requires units capable of connecting in more than two directions. A unit with f reactive groups has functionality f. Entering it along an existing bond uses one group for the incoming connection, leaving f minus one groups that may lead onward. If each remaining group reacts independently with probability p, the mean number of onward branches is p times f minus one. This elementary count captures the essential logic of an ideal gel point.

Flory studied size distributions and gelation of three-dimensional branched polymers in 1941. Stockmayer developed a statistical theory of branched-chain size distributions in 1943. The tree approximation treats connections as extending branches without closed loops. If each step produces fewer than one new branch on average, growth usually terminates. Above one, a persistent macroscopic connected structure can become possible. This yields a critical conversion for an ideal equal-functionality system. The infinite molecule is a statistical description of a macroscopic network, not a requirement for literally infinite matter inside an experimental vessel.

Ideal gel point for tree-like branchingEq. 5

![Ideal gel point for tree-like branching](https://ml-biomat.com/static/agent-math/7454b084fe001d2b77ddd53c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| B | Mean onward branches after entering a unit along a bond | 1 |
| p | Independent group-reaction probability or conversion | 1 |
| f | Identical functionality of each unit | 1 |
| Bc | Critical mean onward branch count | 1 |
| pc | Ideal critical conversion | 1 |

Reading the relationshipOne group is used by the incoming bond, leaving f−1, each continuing with probability p. One onward branch on average marks the branching threshold.

A worked exampleFor f=3, p=0.4 gives B=0.8 and p=0.6 gives B=1.2, with pc=0.5. For f=4, pc=1/3.

ConditionsEqual reactivity and functionality, independent reaction and tree limit without intramolecular loops, f>2. Mixed functionality and complementary-group stoichiometry require extended branching statistics.

[Figure: Flory–Stockmayer ideal branching and a closed loop](https://ml-biomat.com/tutorials/biomaterials-courses/cp09/en/#en-s5)

Figure 2 · Top: an original schematic of the 1941–1943 branching-statistics argument. Entering a trifunctional unit leaves two potential onward connections, each continuing with probability p. Bottom: a loop consumes connection opportunities, motivating a check of the ideal tree approximation.

For trifunctional units the ideal threshold is one half, and for tetrafunctional units it is one third. These values follow from different onward branch counts; they do not replace the gel point of an arbitrary formulation. If two complementary group types must react, such as A with B, their separate conversions and stoichiometric ratio must be followed. A broad functionality distribution gives highly functional units greater influence. Two distributions with the same mean functionality need not share a gel point because following a bond already weights the probability of encountering a unit by its functionality.

Intramolecular cyclization is a central check on the tree approximation. When a reactive group bonds to another group already in the same cluster, it consumes reactive sites without necessarily merging previously separate clusters. It can create a redundant path or a small loop with limited contribution to macroscopic elasticity. Relative to the idealization in which every reaction joins different clusters, this changes gel formation and effective network density. Dilution, short linking chains and reaction geometry can all alter the probability of loop formation. Counting reactive groups alone is therefore insufficient to determine network topology.

Conversion also differs from elapsed time. Here p is the fraction of groups that have reacted, not the time since mixing. Temperature, catalyst, diffusion and reagent depletion together determine how p evolves. Two systems can reach the same conversion at different times, or develop different spatial connection patterns at similar conversion. Comparing a spectroscopic measurement of reactive-group consumption with rheological measurements of gel formation tests how efficiently chemical reaction creates connections between distinct clusters. The comparison is especially informative when reaction becomes limited by motion within a growing network.

Further reaction after gelation often incorporates more material and introduces more constraints, but modulus need not increase in direct proportion to every additional bond. A bond inside an already well-connected local loop acts differently from one that incorporates a free large cluster into the load-bearing network. Explaining a formulation's mechanical performance thus requires moving from how many reactions occurred to where their connections lie and whether they transmit load. Branching statistics identify the onset of connectivity; network mechanics links that structure to material properties.

## Which parts of a spanning network carry load

Walking through a branching network from left to right reveals dead ends, loops that offer alternative routes, and narrow links whose removal separates the two sides. Identifying the relevant backbone, the part able to participate in transmission between the specified boundaries, is an important step toward understanding performance. The backbone depends on the boundary conditions and process. A dangling branch can belong to a spanning cluster without carrying steady two-terminal direct current. The same branch can still affect dynamic mechanical dissipation, entanglement or local motion.

[Figure: Two-terminal network backbone and dangling branches](https://ml-biomat.com/tutorials/biomaterials-courses/cp09/en/#en-s6)

Figure 3 · Green provides routes between boundaries. Orange belongs to the same cluster but carries no ideal steady two-terminal direct current. The diagram separates connectivity from transport roles; flexible-chain load transmission additionally requires constraints and deformation rules.

In a permanent flexible-chain network, deformation changes the distribution of strand end-to-end distances and reduces available conformations, producing entropic elasticity. Adding many strand contributions gives a modulus approximately proportional to the density of elastically active strands times thermal energy. The count concerns strands between effective constraints that participate in deformation, not all chemical bonds or monomers. Thousands of covalent bonds along one chain maintain molecular connectivity; they cannot each be counted as an independent rubber spring contributing separately to the macroscopic modulus.

Entropic-elasticity scale of active strandsEq. 6

![Entropic-elasticity scale of active strands](https://ml-biomat.com/static/agent-math/c208f2fa9c946f945d085386.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| G | Elastic modulus for small shear deformation | Pa |
| νe | Elastically active strand count per current volume | m⁻³ |
| kB | Boltzmann constant, 1.380649×10⁻²³ | J K⁻¹ |
| T | Absolute temperature | K |

Reading the relationshipA constrained strand contributes a thermal-energy-scale deformation free energy. Strand density times energy gives energy per volume, equivalent to pressure.

A worked exampleFor νe=10²⁵ m⁻³ and T=300 K, G≈4.14×10⁴ Pa=41.4 kPa. Doubling active-strand density doubles the estimate at otherwise fixed conditions.

ConditionsRubbery Gaussian flexible strands at small strain, as a scaling or ideal affine estimate. Junction fluctuations, defects, swelling reference state and other stiffness mechanisms affect coefficients and applicability.

This relation explains why increasing effective crosslink density generally raises small-strain rubber modulus at fixed polymer mass: more constrained elastic strands act within the same volume. Very short nearly extended strands, glassy segmental response, crystalline regions and filler contacts can introduce other stiffness contributions or change applicability. Whether junctions follow the macroscopic deformation affinely and whether they fluctuate also affects numerical factors. The effective strand density must be interpreted consistently with the chosen network model rather than inferred by counting every chemical junction indiscriminately.

Networks just above connectivity threshold deserve particular attention. A newly spanning structure can contain many dangling ends, narrow connecting links and highly nonuniform density, giving much weaker mechanical support than a uniform network. A few well-placed additional connections may suppress easy rotation or distribute load, whereas many ineffective small loops may do much less. Predicting modulus from the number of drawn lines overlooks redundant paths, chain flexibility and spatial constraints. Different mechanisms call for structural measures that match the physical process being investigated.

Conducting composites display a related hierarchy. Spanning determines whether an allowed long-range route exists, while individual edge resistances and their series and parallel combinations determine current. A connected network can still conduct poorly if a few crucial contacts have high resistance. For fluid flow through porous matter, narrow pore throats and path tortuosity similarly matter. Percolation supplies the framework for whether routes form; transport or mechanical equations then determine how much they carry. The geometrical question and the constitutive question become complementary rather than interchangeable.

Experiments can therefore combine gel fraction, swelling and small-amplitude modulus. A high gel fraction indicates that more material belongs to the insoluble component but does not alone establish a high active-strand density. Large swelling can reflect sparse network constraints or strong ionic osmotic forces. Modulus also depends on measurement temperature and frequency. Together these observables help distinguish network content, mechanical constraints and solvent driving forces. Using them in combination provides a more informative structural picture than asking one reported number to represent every aspect of network formation.

## Why a network swells without expanding indefinitely

When a dry crosslinked network enters a suitable solvent, solvent molecules penetrate, segment separation grows and specimen volume increases. An uncrosslinked soluble polymer of the same chemistry may instead disperse into separate molecules. Crosslinks maintain overall connectivity while allowing substantial solvent uptake and imposing an elastic cost of expansion. Flory and Rehner's 1943 swelling theory combined mixing free energy with network elasticity to make this competition calculable. The chemical affinity for solvent and the mechanical constraints of the network enter the same equilibrium problem.

Defining a swelling ratio requires specifying the quantities compared. A volume ratio divides wet total volume by dry polymer volume. A mass ratio compares masses and requires density information for conversion to volume. Some reports instead divide absorbed-solvent mass by dry-polymer mass, giving a value one less than wet mass divided by dry mass. If component volumes are approximately additive and polymer is retained, polymer volume fraction is the reciprocal of the volume swelling ratio. This connects concentration to macroscopic dimensions through an explicit material balance.

Volume, concentration and linear swellingEq. 7

![Volume, concentration and linear swelling](https://ml-biomat.com/static/agent-math/7bd5cc3407c4db8cbf86c8e8.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| QV | Swelling ratio relative to dry-polymer volume | 1 |
| V | Total swollen volume | m³ |
| Vp | Volume of retained dry polymer | m³ |
| φp | Polymer volume fraction in the swollen state | 1 |
| λ | Isotropic linear stretch relative to the dry reference shape | 1 |
| 1/3 | Cube-root exponent because volume multiplies three lengths | 1 |

Reading the relationshipApproximate volume additivity gives the reciprocal concentration relation. Equal stretch in three directions gives volume ratio λ³.

A worked exampleWith Vp=1 cm³ and V=8 cm³, QV=8, φp=0.125 and λ=2. A cube of dry side 1 cm reaches side 2 cm.

ConditionsNo polymer loss and approximately additive component volumes. The final relation additionally requires free isotropic swelling; constrained layers require directional stretches.

An eightfold volume increase produces only a twofold length increase under uniform expansion in all directions because volume multiplies three lengths. Treating the volume ratio as linear stretch substantially overestimates deformation. A coating or constrained gel cannot freely expand in every direction, so more volume change may appear in the permitted directions. One isotropic stretch ratio then cannot describe them all. Constraints belong in the size prediction itself rather than being added after interpreting the result.

Osmotic pressure provides an intuitive account of the swelling drive. Mixing encourages solvent to enter the polymer region, while stretching the network raises its free energy and supplies a restoring contribution. A charged network also requires equilibrium of mobile-ion chemical potentials and electroneutrality. An excess internal concentration of mobile ions often produces additional swelling pressure. Added external salt changes that concentration difference and electrical interactions. Water uptake in an ionic gel is therefore determined by more than crosslink density, even when the permanent network chemistry stays the same.

Pressure balance at swelling equilibriumEq. 8

![Pressure balance at swelling equilibrium](https://ml-biomat.com/static/agent-math/1f82723e30653ee0bcaf9212.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Πtot | Net swelling pressure, positive toward expansion | Pa |
| Πmix | Polymer-solvent mixing contribution | Pa |
| Πel | Network-elastic contribution, negative when restoring | Pa |
| Πion | Osmotic contribution of mobile ions | Pa |
| Πext | Opposing external pressure contribution with a consistent reference | Pa |

Reading the relationshipEach term expresses a volume-driving contribution to free energy. Zero net drive at equilibrium combines solvent exchange and mechanical balance.

A worked exampleWith mixing 100 kPa, elasticity −80 kPa, ions zero and external pressure 20 kPa, the net is 100−80+0−20=0 kPa. Raising mixing to 110 kPa at fixed other terms initially gives +10 kPa.

ConditionsQuasistatic equilibrium decomposition with a consistent solvent-reservoir reference. Terms change with volume and environment and must be reevaluated during swelling. The additional ionic term is zero for the neutral nonionic case.

Pressure measures a free-energy change per change of volume. A positive swelling pressure favours expansion. At equilibrium, driving and restoring contributions cancel under the specified external conditions. For a network exchanging solvent with a reservoir, the condition expresses equality of solvent chemical potentials together with mechanical equilibrium. A free-energy model must include the external solvent or salt reservoir consistently, avoiding subtraction of the same pressure twice. Keeping track of the reservoir clarifies which quantities are controlled while the gel volume changes.

The network's preparation reference state also matters. Chains crosslinked in abundant solvent have a different reference conformation from chains crosslinked dry and subsequently swollen. Similar dry-polymer contents need not therefore give identical elastic responses or equilibrium volumes. Temperature and solvent changes can additionally alter mixing interactions. Inferring crosslink density from one swelling measurement requires solvent conditions, reference state and an elastic model, rather than an unconditional empirical constant. Preparation and measurement conditions jointly determine the meaning of the inferred value.

Equilibrium also takes time. Solvent must diffuse through the network and stresses must redistribute. Thick specimens generally take longer than thin ones to become uniform. A dense surface layer formed during initial collapse can slow exchange further. A mass change measured after a few minutes can combine transport kinetics with the thermodynamic endpoint. Tracking mass and dimensions until they stabilize, and checking thickness dependence, helps separate how fast the network responds from the volume it ultimately prefers.

## Gel formation and gel-volume transitions

An already crosslinked gel can shrink substantially when temperature, solvent composition or salt concentration changes while retaining network connectivity. This differs from initial network formation from free molecules. Gelation concerns whether a connected structure is established; a gel-volume transition concerns which volume minimizes the free energy of an existing network. The former changes connectivity, whereas the latter can occur with approximately unchanged topology. This distinction explains why a gel may repeatedly take up and release solvent without rebuilding all its crosslinks in each cycle.

Tanaka's 1978 report of gel collapse and a critical endpoint helped establish the study of gel-volume transitions. Changes in temperature and surrounding-fluid composition allowed a pre-existing polyacrylamide network to move between larger and smaller volumes. Under suitable conditions, the corresponding free-energy landscape can contain two local minima: a solvent-rich swollen state and a more polymer-rich collapsed state. External conditions change their relative depths. When the preferred minimum switches, equilibrium volume can jump even though the network remains connected throughout the transition.

[Figure: Two free-energy minima and network volumes in a gel transition](https://ml-biomat.com/tutorials/biomaterials-courses/cp09/en/#en-s8)

Figure 4 · Two free-energy minima represent collapsed and swollen states of one network; external conditions can exchange their stability. The equal-depth landscape is conceptual, with no experimental axis values. Lower diagrams retain the same connectivity while changing dimensions.

The landscape distinguishes continuous from discontinuous responses. A minimum that moves smoothly produces continuous volume change. Two separated minima exchanging stability produce a discontinuous jump. Near a critical endpoint the distinction between states vanishes and response and fluctuations can grow strongly. In a real specimen, surface layers, friction, defects and solvent diffusion influence the observed path. Heating and cooling can consequently yield different apparent transition positions. Hysteresis contains information about barriers and kinetics and must be interpreted together with waiting time rather than treated as an equilibrium state variable.

Common thermoresponsive hydrogels also involve temperature-dependent interactions between polymer and water. Hydrophobicity is more informative than a statement that certain molecules repel water, and it cannot universally be assigned to entropy alone. Solvent-cavity formation, local water structure, interfacial area and interaction energy contribute to solvation free energy. Their enthalpic and entropic components depend on temperature, solute size and chemical environment. Lum, Chandler and Weeks' 1999 theory explicitly distinguished small- and large-scale hydrophobic solvation, emphasizing why scale and conditions matter when explaining aggregation or collapse.

Variable volume can drive valve opening, surface deformation, changes in drug-diffusion pathways or soft-actuator motion. Design requires equilibrium volume contrast, response time, mechanical support and cycling stability together. Increased crosslinking commonly strengthens constraints but can reduce available swelling. Thinner specimens often exchange solvent more quickly while changing available force and deformation geometry. Structure, thermodynamics and transport jointly determine device behaviour. A single transition temperature therefore does not capture all the relevant performance, even when it is reproducibly measured.

A connected measurement sequence can characterize a new gel. First determine the extractable sol and retained network fractions to identify the connected material. Next allow mass and dimensions to stabilize under fixed conditions to obtain equilibrium swelling. Then vary temperature or salt concentration while following volume to distinguish smooth response from jumps. Finally measure modulus and relaxation in the corresponding states. These measurements describe structure, equilibrium and time response of the same network rather than using gel as a condition-free label for different observations.

From an individual branch to a spanning cluster and then a solvent-filled load-bearing network, the recurring issue is how connections restrict freedom. Fractal geometry describes their spatial distribution. Percolation explains how random local connections create long-range access. Network elasticity and swelling free energy describe the response once that connected structure exists. Keeping these levels explicit joins shape, reaction conversion and macroscopic performance into an explanation that can be calculated and tested through distinct but complementary experiments.
