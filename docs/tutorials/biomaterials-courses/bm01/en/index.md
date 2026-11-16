# From Amino Acids to Proteins: How Sequence Becomes Structure

Source: https://ml-biomat.com/tutorials/biomaterials-courses/bm01/en/
Language: en

Starting with changes in tofu, hair and egg white, explore amino acids, peptide bonds, sequences and folding. Follow the history of sequencing and structural chemistry to understand helices, sheets, molecular connections, and how proteins become functional molecules and materials.

## Tofu, hair and a shared molecular question

Heated soy milk can become a piece of tofu that you can pick up with chopsticks. Hair changes its feel when it becomes wet, yet does not dissolve as quickly as sugar. An egg white turns from transparent to white during cooking and is difficult to return to its original flowing state. Proteins are involved in all three examples, but saying that a substance contains protein does not explain its behavior. We need to ask which small units make up its molecules, how those units are connected, how a chain folds in water, and what happens when many chains meet. This chapter follows that route from visible changes in materials to molecular structure. It will help you identify the particular level that changes when you read about denaturation, an increase in secondary structure, or the formation of a protein network.

Think of a molecule as a collection of atoms connected by chemical bonds. Atoms share electrons in a covalent bond, and changing such a bond generally requires more than rearranging many of the weaker interactions between molecules. Cutting a protein chain into shorter peptides therefore involves changing particular covalent connections. Proteins are one family of biological macromolecules. Other familiar families include polysaccharides made from sugar units and DNA and RNA made from nucleotides. All can be long molecules, but they use different building units and connections. Their size is molecular: a protein several nanometers across remains invisible to the unaided eye, although it contains many atoms compared with a water molecule. A nanometer is one billionth of a meter, a convenient unit for describing many molecular structures.

The terms biological macromolecule and biomaterial address different questions. The former identifies a molecular family and its biological chemistry; the latter commonly concerns a material's interactions with biological systems or its intended use. A protein may function as an enzyme inside a cell, or it may assemble into a film, fiber or hydrogel. A synthetic polymer can also be designed for contact with a biological system. Moving from protein chemistry to materials science therefore requires attention to both individual molecules and their collective organization. The firmness of tofu depends strongly on a network formed by many protein molecules. The shapes of the chains, the density and nature of their connections, and the water retained between them can all affect the final texture.

Proteins can be classified by shape, composition or function, but each classification provides a different view of the same object. Myoglobin is relatively compact, while collagen forms elongated structures that help support tissues. Some proteins also associate with metal ions, carbohydrates or other nonprotein components; heme in hemoglobin is an important example. A compact shape does not by itself guarantee high water solubility, and an elongated shape does not automatically imply insolubility. Surface chemistry, the solution and intermolecular interactions also matter. We will connect these differences to side-chain chemistry, backbone motion and assembly, so that classification becomes a starting point for explaining behavior rather than a list of names to memorize.

[Figure: An alpha carbon bonded to an amino group, carboxyl group, hydrogen and side chain R](https://ml-biomat.com/tutorials/biomaterials-courses/bm01/en/#en-s1)

Figure 1 · A free α-amino acid in a common near-neutral ionic form. The shared backbone provides the connection chemistry; side chain R provides chemical differences.

## How amino acids become a chain with a direction

The α-amino acids used in ordinary proteins share a common framework. A central α-carbon is connected to an amino group, a carboxyl group, a hydrogen atom and a side chain. The side chain is often written as R, which is a placeholder for a group that differs between amino acids. Glycine has a hydrogen at this position, alanine has a methyl group, and lysine has a longer side chain ending in an amino group that can accept a proton. The shared framework resembles a standard connector, while the side chains resemble different components attached to that connector. Common connection chemistry allows a long chain to form; different side chains change local size, interaction with water, charge and reactivity.

These connections also have a three-dimensional arrangement. The four bonds around the α-carbon point approximately toward the corners of a tetrahedron. When four different groups are attached, two mirror-image arrangements are possible that cannot be made identical by rotating the whole molecule, much like left and right hands. This property is chirality, and the two arrangements are called enantiomers. Most such residues in ordinary proteins have the L configuration. L and D identify arrangements through a historical reference convention based on the small molecule glyceraldehyde. They do not name the direction in which an entire chain coils, and the letter L alone does not specify the direction in which a substance rotates polarized light. Glycine has two identical hydrogens on its α-carbon, so it lacks the four-different-groups condition: this carbon is not a chiral center and has no corresponding L/D enantiomeric pair. This distinction explains why replacing an amino acid by its opposite configuration can change recognition or local folding while leaving its atomic composition and mass unchanged.

The amino and carboxyl groups in a structural drawing do not retain the same charge in every solution. Protons can move between a group and its aqueous surroundings, and pH describes an aspect of the acidity of those surroundings. A lower pH generally corresponds to a higher hydrogen-ion activity. Under common near-neutral conditions, the α-amino group of a free amino acid is predominantly positively charged, while its α-carboxyl group is predominantly negatively charged. One molecule can therefore carry both positive and negative charges. Having a net charge of zero does not mean that every part is uncharged. A balanced account can still contain many incoming and outgoing payments; similarly, a molecule's local charge distribution still influences its contacts with water, ions and neighboring molecules.

A peptide bond joins the carboxyl portion of one amino acid to the amino portion of another, producing an amide connection. If we count atoms starting with free amino acids, each new connection leaves the product with the composition of one fewer water molecule than the combined starting molecules. The connected unit is consequently called an amino-acid residue: it is no longer an intact free amino acid. Cells make proteins using ribosomes, transfer RNAs and activated substrates; they do not simply heat a beaker of free amino acids to drive off water. The water bookkeeping here explains the difference in composition before and after connection, including why adding free-amino-acid molar masses directly would give the wrong molar mass for a peptide.

Accounting for mass when a chain formsEq. 1

![Accounting for mass when a chain forms](https://ml-biomat.com/static/agent-math/d2400d0c9746b0a28879187a.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Mchain | Molar mass of the linear peptide | g mol⁻¹ |
| N | Number of amino-acid residues | 1 |
| i | Residue index running from 1 to N | 1 |
| Mi | Molar mass of the free amino acid at position i | g mol⁻¹ |
| MH₂O | Molar mass of water, approximately 18.015 | g mol⁻¹ |
| Σ | Sum over the molar masses at all positions | — |

Reading the relationshipConnecting N units into one open chain requires N−1 links, so the combined free-amino-acid composition loses N−1 water equivalents. A mole counts 6.02214076×10²³ specified entities; g mol⁻¹ is mass per mole.

A worked exampleGlycine is approximately 75.07 g mol⁻¹ and alanine 89.09 g mol⁻¹. Their dipeptide has one peptide bond, giving 75.07+89.09−18.015=146.145 g mol⁻¹. Reversing their order preserves this mass but changes the sequence.

ConditionsThis expression describes an unmodified linear peptide. Cyclization, terminal blocking, disulfides and other modifications require their additional composition changes to be included. The cellular reaction pathway is a separate description from this atom balance.

An ordinary linear peptide with unmodified ends retains an amino terminus and a carboxyl terminus, called the N terminus and C terminus. By convention, a sequence is written from N to C. Glycine followed by alanine is therefore a different sequence from alanine followed by glycine, even though both contain the same numbers of the two residues and have the same total mass. Their direction and terminal neighbors differ. Three-letter abbreviations such as Gly and Ala are convenient for short examples, while G and A are compact one-letter codes. The letters identify residues; they are not direct pictures of shape or charge. Explaining a sequence's behavior requires translating those identities back into the chemistry of its side chains.

A few concrete side-chain properties provide a useful foundation. Exposing a largely nonpolar hydrocarbon group to water changes the organization of nearby water. Charged groups interact with opposite charges and can have their electrostatic effects screened by dissolved ions. Hydroxyl and amide groups can participate in hydrogen bonding. Two cysteine thiol groups can form a disulfide bond under suitable oxidizing conditions. Glycine is small and can occupy some backbone conformations that are difficult for bulkier residues. Proline connects its side chain back to the backbone nitrogen, restricting rotation and changing the ability of that position to donate a hydrogen bond. Such categories help explain particular contacts; they are not permanent labels saying that a residue always stabilizes or always disrupts a structure.

A group's charge can also change as its surroundings change. To make this quantitative, consider a single independent acidic site that exchanges between a protonated form and a deprotonated form. Its pKₐ identifies the acidity at which the two forms have equal populations under the corresponding approximation. The difference between pH and pKₐ indicates which form is more abundant. The model below turns qualitative terms such as more acidic and more basic into a population fraction. When many sites interact, or when a group is buried within a protein, its effective pKₐ must be reconsidered. This dependence on surroundings is one reason why the same residue can behave differently in different proteins.

The deprotonated fraction of one acidic siteEq. 2

![The deprotonated fraction of one acidic site](https://ml-biomat.com/static/agent-math/9e8327e185259aa409db3ffc.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| θ | Fraction in the deprotonated form, from 0 to 1 | 1 |
| pH | Measure of the solution hydrogen-ion activity | 1 |
| pKₐ | Negative base-10 logarithm of the site dissociation constant | 1 |
| 10ˣ | Base-10 exponential; increasing x by 1 multiplies it by ten | 1 |

Reading the relationshipThe protonated and deprotonated fractions of one independent site sum to one. Acid–base equilibrium sets their ratio, and normalizing by their combined population gives θ. At pH=pKₐ, the denominator is two and the two forms are equally populated.

A worked exampleFor pKₐ=4.0 at pH=5.0, θ=1/(1+0.1)≈0.909: about 90.9% of sites are deprotonated. At pH=3.0, θ=1/(1+10)≈0.091, or about 9.1%.

ConditionsThis model treats one independent acidic site with the corresponding dilute-solution approximation at fixed temperature. Local surroundings and interactions between sites can shift its actual pKₐ.

## Why order matters: insulin and overlapping fragments

Imagine completely breaking down two short peptides and finding that each contains four lysines and four leucines. Composition analysis tells us which units are present and how many there are, but not which units are neighbors. One sequence could place all the lysines in its first half and all the leucines in its second half; another could alternate them. The overall composition is the same, yet charge and nonpolar groups are distributed differently along the chain. This can change both intramolecular contacts and the way chains associate. The comparison resembles making different sentences from the same letters, although chemical sequences are additionally constrained by three-dimensional geometry, solvent and temperature. A string of letters alone does not supply a unique drawing of the folded molecule.

In the middle of the twentieth century, whether a protein possessed a definite residue sequence was an experimental question. [Frederick Sanger's work on insulin](https://www.nobelprize.org/uploads/2018/06/sanger-lecture.pdf) addressed its actual chemical connections: identify chain ends, break the chains into manageable fragments, and use overlaps between fragments produced by different cleavage methods to reconstruct their order. Insulin contains two peptide chains connected through particular disulfide bonds. Determining the residue sequence of each chain therefore had to be followed by identifying which cysteines were linked. The approach made it possible to describe a protein as a specific sequence and connection pattern, rather than treating it as an undifferentiated collection of complex biological material.

[Figure: AGK and GKVE overlap at GK and combine to AGKVE](https://ml-biomat.com/tutorials/biomaterials-courses/bm01/en/#en-s3)

Figure 2 · The logic of overlapping fragments, illustrated with the teaching peptide AGKVE. Information from two cleavage patterns constrains the order in the original chain.

A short example illustrates fragment assembly. Suppose one treatment produces AGK and another produces GKVE. Their shared GK suggests the combined sequence AGKVE. Real experiments must also address repeated sequences, incomplete cleavage, chemical modifications and mixtures of fragments, so several complementary observations are needed. The central task is not to sort fragments by length. It is to find a complete arrangement consistent with terminal identities, fragment compositions and overlapping sequences at the same time. Mapping disulfide bonds introduces another requirement: these connections must be preserved or changed in a controlled way during analysis. Otherwise, the sequence of each chain may be known while the connections within or between the chains remain uncertain.

Simple counting shows why the number of possible sequences becomes large so quickly. If each position can independently contain any of 20 common residues, adding one position multiplies the existing number of sequences by 20. This is the multiplication rule: the choices at one position combine with all the choices at the next. The count does not claim that every sequence can be made by a cell, folds stably, or performs a useful function. It quantifies the chemical variety hidden behind the phrase “chains of the same length.” Length, composition, sequence and chemical modification consequently need to be described separately when comparing proteins.

Counting sequences of the same lengthEq. 3

![Counting sequences of the same length](https://ml-biomat.com/static/agent-math/b3d587f455f86dc20013d6a1.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Ω | Number of possible sequences | 1 |
| q | Number of allowed residue types at each position | 1 |
| N | Number of positions in the sequence | 1 |
| qᴺ | Product of N factors of q, combining choices position by position | 1 |

Reading the relationshipThe first position has q choices. Each can be combined with q choices at the second position, giving q×q. Repeating the same reasoning for N positions produces the exponent. The sequences are directional.

A worked exampleWith 20 common residue types and five positions, there are 20⁵=3,200,000 formal choices. Allowing only G and A gives 2⁵=32 choices at the same length.

ConditionsPositions are chosen independently, residues may repeat, and neither total composition nor function is constrained. Fixing the number of each residue requires a different count.

### Same composition, different neighbors

[Figure: Peptide sequence and neighboring residue pairs](https://ml-biomat.com/tutorials/biomaterials-courses/bm01/en/#en-s3)

Change the arrangement to see how neighbors change while composition remains constant.

The effect of changing a single residue depends on its structural and functional setting. A substitution in an enzyme's active site may change a chemical step. Replacing a small buried residue with a much larger one may alter local packing. A substitution in a flexible region distant from important contacts may have a smaller effect. A useful explanation follows a specific chain of reasoning: what changed in side-chain chemistry, which contacts were affected, and which measurable property responds? This is more informative than treating every mutation as general damage to the protein. It also reveals the additional levels of organization between a molecular change and a change in the mechanical behavior of a bulk material.

## A chain can rotate, but it cannot pass through itself

A string of beads is useful for counting residues, but can suggest that every connection rotates as freely as a loose joint. Electron distribution around the peptide bond gives the amide connection partial double-bond character. The associated atoms tend toward a nearly planar arrangement, and rotation about the peptide bond is strongly restricted. Adjacent peptide planes mainly change their relative orientation through two backbone rotations near the α-carbon. The angle φ describes rotation about N—Cα, while ψ describes rotation about Cα—C′, where C′ is the carbonyl carbon. Rotation about the peptide bond itself is commonly described by ω. Connecting each name to the corresponding chemical bond is more useful than memorizing angles alone: the available rotations determine where atoms move when the chain bends.

[Figure: A peptide backbone showing phi, psi, omega and the peptide-plane region](https://ml-biomat.com/tutorials/biomaterials-courses/bm01/en/#en-s4)

Figure 3 · The angles φ and ψ describe two different backbone bonds. Peptide planarity and atomic size jointly constrain available conformations.

To visualize a dihedral angle, imagine two stiff pieces of paper joined along one edge. Folding them around that edge changes the angle between their planes. Four consecutive atoms similarly define two planes, and the angle between those planes is a dihedral angle. Angles are often reported in degrees, with 360° representing one complete turn. Writing a rotational coordinate between −180° and 180° simply cuts the same circle at a chosen location. Consequently, 179° and −179° are close in physical orientation rather than widely separated states. Recognizing this periodicity helps when reading plots of protein backbone angles and prevents an ordinary numerical difference from being mistaken for a large structural change.

Even where a single bond permits rotation, the finite sizes of neighboring atoms restrict the available angles. Bringing atoms too close together causes a steep increase in energy, so a chain cannot pass through itself like a line with no thickness. Plotting φ on one axis and ψ on the other allows different combinations to be checked for steric clashes. This is the geometric idea behind a Ramachandran plot. It converts many three-dimensional exclusion problems into a two-dimensional map: different local structures tend to occupy different regions, and glycine and proline have distinctive allowed regions because of their side-chain geometry. The regions describe local backbone conformations, not complete classes of protein function.

Most peptide bonds adopt a trans configuration, but different connections do not all have identical behavior. Peptide bonds preceding proline merit particular attention because of their cis–trans populations, and interconversion can influence folding kinetics. Flexibility also comes from more than the main chain. Many side chains contain additional rotatable bonds and can explore alternative orientations. A folding fan offers a useful comparison: its ribs constrain the principal movement, while smaller decorations attached to it may move independently. Proteins likewise combine backbone and side-chain motions. A structural image is a description of the molecule under particular conditions, rather than proof that every atom remains fixed at one position.

## How local connections produce helices and sheets

When neighboring residues repeatedly adopt similar backbone angles, a chain can form a regular local structure. In an α-helix, the backbone winds around an axis and many carbonyl groups and amide hydrogens form a repeating hydrogen-bond arrangement. A hydrogen bond can initially be understood as a directional attraction between an appropriate donor and acceptor with suitable electrical and geometric properties. It is generally weaker than a backbone covalent bond, but a coordinated network of hydrogen bonds influences structural stability. In a standard α-helix, the carbonyl group of residue i can hydrogen-bond to the backbone N—H of residue i+4. Here i is simply a position number; i+4 means four residues farther along the sequence, not a different chemical species.

In 1951, [Linus Pauling, Robert Corey and Herman Branson](https://doi.org/10.1073/pnas.37.4.205) proposed helical configurations consistent with peptide planarity, bond lengths, bond angles and hydrogen bonding. Their approach illustrates how a molecular model can be built: respect the local geometry established from smaller molecules, then seek arrangements that can repeat continuously without severe clashes. The usual modern geometric description of an α-helix is approximately 3.6 residues per turn, with about 0.15 nm of axial advance per residue. A complete turn does not have to contain an integer number of residues. Moving one residue along a chain and rotating once around an axis are different repetitions, much as stair spacing and viewing direction need not repeat at the same interval.

[Figure: Schematic hydrogen-bond organization along a helix and between antiparallel strands](https://ml-biomat.com/tutorials/biomaterials-courses/bm01/en/#en-s5)

Figure 4 · Two organizations of secondary structure. The helix is represented by a backbone trace; β-strand arrows point from N to C. Dashed lines emphasize the connectivity of the hydrogen-bond networks.

Measuring length along the helix axisEq. 4

![Measuring length along the helix axis](https://ml-biomat.com/static/agent-math/68d93cbe492c7ce3e4b4b25b.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Lα | Axial separation of the first and last residue Cα positions | nm |
| N | Number of residues in the regular α-helical segment | 1 |
| h | Axial advance per neighboring residue, approximately 0.15 nm | nm |

Reading the relationshipN residue positions contain N−1 neighboring intervals, each advancing h along the axis. This measures the axial projection, not the longer path traced bond by bond along the winding backbone.

A worked exampleTwelve residues have eleven axial intervals, giving Lα≈11×0.15=1.65 nm. Adding one residue while retaining the regular helix increases the axial separation by approximately 0.15 nm.

ConditionsThe calculation uses the average geometry of an ideal regular α-helix. Curvature, terminal geometry and local angular variation alter actual lengths.

A β-sheet uses a different arrangement. Individual backbone segments adopt relatively extended, slightly zigzagging β-strand conformations, and neighboring strands hydrogen-bond into a sheet. In a structural cartoon, an arrow for a β-strand normally points from N to C. Neighboring arrows that point in the same direction are parallel; those pointing in opposite directions are antiparallel. A sheet can contain mixed directions, and its strands may be distant portions of one chain folded back on itself or portions of different chains. The zigzag backbone places side chains approximately on alternating faces of a sheet. Residue order can therefore create different chemical characteristics on its two surfaces, providing a concrete connection between sequence and local surface properties.

Helices and sheets must be joined by turns and connecting segments. A β-turn is commonly described using four consecutive residues; some turn geometries allow a hydrogen bond between the carbonyl of the first residue and the N—H of the fourth. Longer connecting regions that do not form regular helices or sheets are often called loops. The word loop primarily describes a chain returning through space; it does not necessarily mean that its chemical backbone has closed into a ring. Turns and loops join structural elements and can participate in binding or opening and closing motions. Some are flexible, while others have well-defined conformations stabilized by their surroundings. Irregular secondary structure therefore does not automatically mean an absence of structure or function.

Secondary structure describes local backbone and hydrogen-bond organization rather than assigning one label to an entire protein. A protein can contain α-helices, β-sheets, turns and flexible regions at the same time. Similar local helices may also appear in proteins with very different jobs. Thinking of these local structures as parts of a larger assembly prepares us to discuss tertiary structure. However, the parts belong to a continuous chemical chain: their lengths, sequence order and orientations are constrained by the whole molecule. They are not independent blocks that can be rearranged on a tabletop without affecting the connections between them.

## The complete molecule: water, contacts and free energy

Tertiary structure usually describes the overall three-dimensional arrangement of one protein chain. It includes the proximity of sequence-distant segments, which side chains are buried or exposed, and how local structural elements are positioned relative to one another. The concept applies to compact proteins as well as to chains with elongated regions or several domains. A domain is a region that forms a relatively coherent structural unit; flexible segments may connect it to other regions. A complex containing several polypeptide chains also requires a description of the positions and contacts of its subunits, called quaternary structure. Subunits can associate through noncovalent interactions and can additionally be joined by covalent crosslinks.

[Figure: A comparison of sequence, local structure, a complete chain and a multichain assembly](https://ml-biomat.com/tutorials/biomaterials-courses/bm01/en/#en-s6)

Figure 5 · Four levels of description, from sequence to assembly. Each level identifies a kind of structural question rather than requiring a protein to be globular.

Water is an active participant in folding. Exposing nonpolar side chains to water versus bringing them together changes the organization of the surrounding water and the free energy of the system, contributing to the hydrophobic effect. This effect is not a fixed “hydrophobic bond” that can be drawn in the same way as a peptide bond. Hydrogen bonding, electrostatics, close packing and van der Waals interactions must also be considered. Whether a contact is favorable depends partly on the protein–water, water–water and other contacts that it replaces. For example, a group may already form hydrogen bonds with water before folding. The energetic advantage of forming an internal hydrogen bond cannot then be assessed simply by counting the new lines drawn inside the folded protein.

Folding usually reduces the number of conformations available to a chain while changing its molecular contacts and the surrounding solvent. Free energy allows these changes to be compared using a common thermodynamic quantity. Enthalpy helps account for energy and pressure–volume contributions, whereas entropy concerns the number and distribution of accessible states. Temperature sets the weight of the entropy contribution in the free energy. A meaningful comparison between folded and unfolded states includes the protein and the solvent affected by it. This explains the competition between favorable contacts and a broad choice of conformations, as well as why temperature, salt concentration and solvent composition can change which conformations are most often observed.

Comparing contacts and accessible statesEq. 5

![Comparing contacts and accessible states](https://ml-biomat.com/static/agent-math/457fd2f0164cda28650c6274.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Δ | Value in the folded ensemble minus that in the unfolded ensemble | — |
| G | Gibbs free energy expressed per mole of protein | J mol⁻¹ |
| H | Enthalpy of the corresponding system | J mol⁻¹ |
| S | Entropy including protein and affected solvent | J mol⁻¹ K⁻¹ |
| T | Absolute temperature, Celsius temperature plus 273.15 | K |
| fold | Subscript identifying the folding comparison | — |

Reading the relationshipAt fixed temperature and pressure, free energy compares states. Folding changes contacts and the states available to protein and solvent. Multiplying entropy by T gives the same energy units as enthalpy. Negative ΔGfold means the folded ensemble has lower free energy.

A worked exampleAt a specified temperature, take ΔHfold=−30 kJ mol⁻¹, ΔSfold=−0.080 kJ mol⁻¹ K⁻¹ and T=298 K. Then ΔGfold=−30−298×(−0.080)=−6.16 kJ mol⁻¹. The negative value favors the folded ensemble under these conditions.

ConditionsCompare states under the same temperature, pressure and composition conditions. The example parameters apply at that temperature; changing temperature requires consideration of changes in enthalpy, entropy and heat capacity.

A free-energy difference can also be related to observed populations. Consider a sufficiently simple protein that can be approximated, under specified conditions, as occupying a folded ensemble or an unfolded ensemble. Each ensemble can contain many similar microscopic conformations. At equilibrium, the lower-free-energy ensemble is favored, but thermal motion permits occupation of the other ensemble as well. The exponential relation below gives their populations in this two-state approximation. It translates “more stable” into “more frequently occupied under these conditions.” If important intermediate states or aggregates are present, they must be included in the state description rather than forced into the same two categories.

From free-energy difference to folded fractionEq. 6

![From free-energy difference to folded fraction](https://ml-biomat.com/static/agent-math/0d98ee0ad8f7299acf852aa8.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| pF | Equilibrium fraction in the folded ensemble | 1 |
| ΔGfold | Molar free energy of folded minus unfolded ensembles | J mol⁻¹ |
| R | Molar gas constant, approximately 8.314 | J mol⁻¹ K⁻¹ |
| T | Absolute temperature | K |
| exp(x) | Natural exponential eˣ, where e is approximately 2.718 | 1 |
| F | Label for the folded ensemble | — |

Reading the relationshipEquilibrium statistics relates the population ratio to the free-energy difference measured against the thermal scale RT. The two fractions sum to one, and normalization gives this expression. ΔGfold/(RT) is dimensionless, as required for an exponential argument.

A worked exampleWith T=298 K and ΔGfold=−5.0 kJ mol⁻¹=−5000 J mol⁻¹, the exponent is approximately −2.02 and pF≈0.883, or about 88.3%. Equal free energies give a zero exponent and a 50:50 population.

ConditionsThis is an equilibrium two-state model with the internal conformational contributions included in each ensemble free energy. It describes populations rather than folding rates or intermolecular aggregation.

For materials, we must further distinguish stability within an individual chain from organization between chains. A protein can retain its folded structure while making new surface contacts that create a network. It can also unfold partially, expose previously buried groups, and form new intermolecular connections. Gelation, fiber assembly and increasing turbidity describe collective changes at different scales. They are related to secondary and tertiary structure but are not the same observables. When a material becomes stiffer, useful questions concern which connections increased, how chain motion became restricted and how water was redistributed. These questions identify mechanisms more precisely than assuming that the proteins simply folded better.

## Can an unfolded chain return? Denaturation and its surroundings

Protein denaturation usually means a substantial change in spatial organization, often accompanied by a change in function. It differs from hydrolyzing the peptide bonds and directly breaking the primary structure. Heating, changing acidity, changing solvent or adding particular reagents can alter interactions supporting the original conformation. During egg cooking, many proteins unfold and associate into a network that scatters light, producing the familiar white, solid appearance. Cooling does not automatically remove the new intermolecular contacts or spatial constraints. Restoring the original temperature restores one external condition, but does not necessarily restore the original molecular relationships or the pathways by which chains can explore conformations.

[Christian Anfinsen's experiments on ribonuclease](https://www.nobelprize.org/uploads/2018/06/anfinsen-lecture.pdf) asked a more specific question: if the sequence remains intact, can an active structure return after folding interactions have been altered and subsequently restored under appropriate conditions? Denaturing conditions and reduction of disulfide bonds changed the structure, after which the recovery of activity was examined as those conditions were removed. The results supported a connection between sequence and an accessible active conformation in a defined environment, and helped establish folding as a physicochemical process. The lesson is that sequence and surroundings together determine the available interactions and energy relationships, rather than that all proteins immediately and completely refold on their own outside a cell.

[Figure: The experimental logic of an active folded state, an unfolded reduced state and refolding after restoration of conditions](https://ml-biomat.com/tutorials/biomaterials-courses/bm01/en/#en-s7)

Figure 6 · The central comparison in ribonuclease refolding: preserve chain order, alter and restore folding conditions, and test activity. The schematic shows a subset of disulfide contacts.

Refolding involves both the stability of possible states and the routes by which they can be reached. A thermodynamically favorable state can be difficult to reach quickly if a chain becomes trapped by inappropriate contacts, incorrect disulfide bonds or intermolecular aggregation. In cells, molecular chaperones and other systems help certain proteins avoid unsuitable interactions or pass through necessary folding steps. Some proteins also require partners, cofactors, a membrane environment or chemical modifications to function. Conversely, a native protein need not be a nearly motionless compact structure. Some proteins or regions naturally occupy broad conformational distributions, and this flexibility contributes to recognition and regulation. A discussion of the appropriate structure should therefore include the function and environment being considered.

The relationship between temperature and protein stability is also more complex than assuming that colder always means more stable. Heating changes thermal motion and the contributions of different interactions; cooling can also change the hydrophobic effect and the balance of free energy. Different proteins respond differently, so their behavior is interpreted together with measurements. Salts likewise act through more than one route: they can screen charges and influence solvent properties and intermolecular contacts. An especially useful habit for a beginner is to read a protein's name together with its solution conditions. A folded fraction measured once does not by itself describe the same protein at a different temperature, acidity or concentration.

## Using structural levels to explain an observation

Return to the example of a protein material. Suppose two solutions at the same protein concentration receive different treatments: one remains fluid while the other forms a gel. Begin by asking whether molecular identity changed through chain cleavage, covalent crosslinking or chemical modification. Then ask how local helices, sheets and overall folding changed. Finally, examine whether the molecules established a network of connections spanning the sample. These are different levels of description and usually require complementary observations. An increase in a particular secondary-structure fraction helps characterize local organization, while a spanning network requires information about larger-scale structure and mechanical response.

Different measurements resemble different ways of examining a folded-paper object. Mass and composition analysis identify the available components and their amounts; sequence analysis identifies order along the chain. Spectroscopy can be sensitive to particular local structures and environments. Scattering and microscopy describe organization at different length scales, while mechanical measurements show how a material transmits force and stores or dissipates work. You do not need to memorize the operating details of every instrument to begin reasoning about proteins. The useful question is what a signal responds to directly. For example, more helices in a drawing become a quantitative statement about a sample only when that drawing is connected to a defined structural measurement and analysis.

A few questions help separate these levels. Does equal mass establish equal sequence? If all peptide bonds remain intact, must the original function remain? If a complex separates into subunits, must each subunit lose its secondary structure at the same time? These questions distinguish composition, chemical connectivity, spatial organization and assembly state. Material behavior frequently depends on several of these levels together. Defining them separately and then tracing the relationships between them makes it possible to explain which part of a treatment changed the final behavior.

Explore the answers: equal mass, the same chain and the same structure

Equal mass can correspond to different sequences: glycine–alanine and alanine–glycine are simple examples. Preserving peptide bonds preserves the main-chain connections, but the protein can still unfold, aggregate or lose a suitable binding site. Dissociation changes the relationship between subunits. Individual subunits may retain their folds or may change because their structures depend on the missing contacts. A well-organized explanation first identifies the observed level and then states which structural or environmental conditions are needed to interpret it.

A protein can now be understood simultaneously as a directional chemical chain, a set of geometrically constrained rotating connections, a three-dimensional molecule moving in its surroundings, and a component of a larger material network. Sequence specifies possible local interactions, the environment changes their relative importance, and assembly connects single-molecule behavior to larger scales. When studying peptide synthesis, protein purification, enzyme catalysis or silk fibers, the same reasoning remains useful: identify the connections, contacts and states that change, and explain how those changes affect the measured property.
