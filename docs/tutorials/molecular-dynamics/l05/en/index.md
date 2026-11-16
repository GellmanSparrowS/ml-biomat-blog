# Representing a Molecule in a Computer

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l05/en/
Language: en

Use a short PEG chain to connect atomic identity, connectivity, parameters, and conformation before inserting it into water.

## Start with a flexible chain and distinguish its identities

A piece of string can curl around a finger or lie straight across a table. Its shape changes while its connections remain the same: the middle has not become an end, and neighbouring sections have not separated. A polymer has a related property. It bends and turns in water and may extend under a pulling force, while the atoms joined by covalent bonds retain their connectivity. Representing this object in a computer requires both its identity and its current shape. We will use that distinction to turn the independently moving particles of earlier lessons into a molecule with a defined chemical structure.

Our molecule is a short polyethylene glycol chain, abbreviated PEG, with a hydroxyl group at each end. Its repeating backbone contains carbon–carbon–oxygen connections. PEG appears in hydrophilic coatings, formulations, and hydrogel materials, making its behaviour in water relevant to familiar material questions. We use eight repeat units so that the backbone, ends, and solvent can be inspected within a small system. Its formula is C₁₆H₃₄O₉, represented by fifty-nine explicit atoms. Chain length matters: it changes the relative importance of the ends and the available conformations. The particular short molecule, rather than every material bearing the name PEG, is our defined object.

Three complementary information cards help organize the description. An identity card records atom types, masses, and partial charges. A connectivity card records bonds, three-atom angles, and four-atom torsional interactions. A position card records the current coordinates. Identity and connectivity contribute to the computational model, while coordinates specify one conformation of that model. Confusing the cards leads to predictable mistakes. Two nearby atoms need not share a covalent bond, and two atoms belonging to the same element need not have identical force-field parameters. Reading the cards together explains both what remains fixed and what can change during motion.

We follow a complete preparation sequence. A three-atom water template introduces coordinates, types, charges, and connections. The same reading method then applies to the fifty-nine-atom PEG template and its parameters. Finally, the chain is inserted into prepared water, overlapping molecules are removed, and the combined system adjusts. A complete Python program turns the actual template records into inspectable figures, while the simulation results show what happened during preparation. This connects numerical input with the molecular picture and subsequent observations, so that a visually plausible structure can also be explained through the definitions that generated it.

The distinction also prepares us for biological macromolecules. Proteins have connected amino-acid backbones, glycans depend on the locations of branches, and nucleic acids have directional connections that organize sequence and conformation. Their chemistry differs, but every example requires separating identity, connectivity, and three-dimensional arrangement. PEG provides an accessible starting point because its repeating backbone and terminal groups are recognizable, while its flexibility allows many shapes. Once those shapes are understood as configurations of one specified molecular object, the same questions can be carried into more complicated systems without treating every structure file as an entirely new kind of problem.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l05/en/#en-s1)

Figure 1 · The repeat formula describes composition; connections and coordinates describe identity and current conformation.

## Why being connected was once a scientific question

Drawing covalent links between polymer repeat units now seems natural. Early polymer science had to establish what such materials consisted of. Were their high viscosities, slow diffusion, and unusual solution behaviour consequences of aggregates of small molecules, or of genuinely long covalent structures? Both descriptions could produce a large-looking object, yet implied different responses to dilution, chemical transformation, and motion. Similar appearance did not establish identical internal organization. That historical question remains useful when reading a molecular model: the connections represented by a picture must be distinguished from atoms that merely happen to occupy neighbouring positions.

Staudinger's 1920 paper on polymerization connected the interpretation of macromolecular materials with long covalent structures. For this lesson, its useful consequence is to define a molecule through connectivity rather than as a collection of nearby spheres. Two schematic objects can consequently have similar outlines but different permitted motions. Members of an aggregate can separate, whereas a chain with fixed connections changes shape through coordinated bond lengths, angles, and torsions. The diagram illustrates these two structural ideas. [Staudinger, 1920](https://doi.org/10.1002/cber.19200530627)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l05/en/#en-s2)

Figure 2 · Conceptual comparison of structural ideas: similar outlines can contain different connectivity.

In the molecular dynamics model used here, the connectivity card is not inferred afresh at every step. Listed bonds supply energy terms, allowing connected atoms to fluctuate around preferred separations while adjacent bonds bend and twist. When two unconnected atoms approach, their nonbonded interaction changes their forces without automatically adding an entry to the bond list. A chain extending in water is therefore a question directly expressed by this model. Monomers polymerizing into a chain require additional definitions for bond formation and its reaction model. Changing the physical process changes the information that the calculation must contain.

An element and an atom type also identify different things. The element specifies chemical identity, such as carbon or oxygen. A type associates a local environment with force-field parameters. An internal ether oxygen in PEG connects two carbons, whereas a terminal hydroxyl oxygen connects a carbon and a hydrogen. Both are oxygen, but their environments differ. This example labels them OE and OAlc, with water oxygen labelled OW. The names make the categories readable; the model still obtains numerical behaviour from masses, charges, and interactions. A recognizable label is a route to a parameter definition, rather than a substitute for it.

An atom ID has another purpose: it uniquely identifies one atom, like an individual entry in an address book. A type is a shared category, while a molecule ID groups atoms belonging to the same molecular object. Many hydrogens can have one type and distinct atom IDs; one molecule contains several types. These distinctions later determine how trajectories are read. Follow an ID to track the same atom through time, select a type to examine a category, and use molecular membership to reconstruct an entire object. Each operation answers a different question even when all three identifiers appear on the same row.

Preparation therefore begins with mutually checkable relationships. The formula supplies composition, the connection graph supplies molecular organization, the parameters supply energy rules, and coordinates supply geometry. Each layer can reveal a problem hidden from another. A correct total atom count can coexist with a hydrogen attached to the wrong oxygen. A correct bond list can accompany crowded initial coordinates. The inspection program develops these checks separately and then connects them. This makes a successful file read one useful technical step within a larger physical explanation of the molecular model.

## Read a molecular template through three atoms

Open water.mol. Its header declares three atoms, two bonds, and one angle, followed by sections named Coords, Types, Charges, Bonds, and Angles. Coords gives a template-local ID followed by three coordinates. Types associates those IDs with parameter categories. Charges supplies partial charges. Bonds and Angles use the same IDs to identify connected atoms. Rather than guessing the molecule from visible distances, the file preserves these relationships explicitly. LAMMPS can subsequently copy the template and assign identities within the complete system. The template thus defines a reusable molecular object while the construction command determines where particular copies are placed.

### Complete flexible-water template

```
# LAMMPS Molecule File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

3 atoms
2 bonds
1 angles

Coords

1 0 0 0 # H2O O
2 1.012 0 0	# H2O H
3 -0.4 0.929 0 # H2O H

Types

1 OW
2 HW
3 HW

Charges

1 -0.82 # H2O O (SPC/Fw)
2 0.41 # H2O H (SPC/Fw)
3 0.41 # H2O H (SPC/Fw)

Bonds

1 OW-HW 1 2
2 OW-HW 1 3

Angles

1 HW-OW-HW 2 1 3
```

IDs link coordinates, types, charges, and geometric interactions.

The oxygen is placed at the origin, with the two hydrogens extending in different directions. Atom one is OW and atoms two and three are HW. The bonds connect one to two and one to three. The angle entry uses the order two, one, three, placing atom one at its vertex. Hold two pencils with one end of each touching: the angle between them resembles this three-atom geometry. Opening the angle changes the hydrogen–hydrogen distance even when both oxygen–hydrogen lengths remain fixed. Bond length and bond angle therefore describe distinct geometric changes, which need distinct definitions in a flexible molecular model.

The oxygen charge is −0.82 and each hydrogen charge is +0.41, expressed in elementary-charge units e. Adding the charges gives zero for the whole molecule. Spatially separated positive and negative sites still interact with other molecules in an orientation-dependent way. The same sum checks the charge of a larger system. Adding a charged end group, changing protonation, or introducing ions changes particular entries and potentially the total. A charge sum is straightforward to calculate and useful for checking composition, while the location of each charge remains equally important for understanding the interaction it produces.

Sum atomic charges to obtain molecular chargeEq. 1

![Sum atomic charges to obtain molecular charge](https://ml-biomat.com/static/agent-math/40b8f735ba087efc6ef1863c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Q | Total charge of a molecule or chosen atom group | e |
| qᵢ | Partial charge assigned to atom i | e |
| N, i | Atom count and summation index | 1 |
| Σ, = | Sum charges from index 1 through N; equality defines the total | 1 |

Reading the relationshipCharge adds algebraically, retaining its sign. Spatially separated partial charges can coexist with overall neutrality.

A worked exampleSPC/Fw charges of −0.82, +0.41, +0.41 in units e give Q=0. The 59 PEG template charges also sum to zero within floating-point rounding.

ConditionsPartial charges belong to the specified model. Net-charge checks and spatial charge distributions provide complementary information.

The PEG template extends the same organization to fifty-nine atoms, fifty-eight bonds, one hundred and four angles, and one hundred and sixteen dihedral records. A connected graph without a cycle has one fewer edge than vertices, so its atom and bond counts provide a useful relationship to inspect. A graph cycle is different from a chain curling into a ring-shaped arrangement in space. Unless its ends are actually connected, the curled chain can still have a tree-like connection graph. Our program traverses the bond list to check connectivity rather than treating the count relationship alone as proof that every atom belongs to one molecule.

### Complete PEG molecular template

```
# LAMMPS Molecule File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

# PEG molecule

59 atoms
58 bonds
104 angles
116 dihedrals

Coords

1 -3.0661409 -3.1122069 -1.2331413
2 -3.0905955 -3.1901295 -0.3069935
3 -1.7871211 -3.4628029 0.1677571
4 -1.7892607 -3.9757321 1.1640826
5 -1.4364998 -2.4400568 0.4558979
6 -0.9585523 -4.2486658 -0.9052389
7 -1.5905948 -5.0815649 -1.3120303
8 -0.0526673 -4.7456765 -0.4700128
9 -0.63208 -3.3539891 -2.0115812
10 0.2145577 -4.0010762 -2.9207664
11 -0.3729619 -4.5629487 -3.6922491
12 1.0240761 -4.5117416 -2.3388433
13 0.9711505 -2.8357534 -3.5251923
14 0.3408715 -1.9581318 -3.822669
15 1.6180273 -3.1186311 -4.3940263
16 1.8975644 -2.4613039 -2.5075514
17 3.0585685 -1.8075132 -3.006783
18 2.8443427 -0.8083913 -3.4607034
19 3.6249113 -2.4323449 -3.7466593
20 3.992363 -1.7272376 -1.8733916
21 4.9511518 -1.186389 -2.07637
22 4.254519 -2.795933 -1.6625937
23 3.423965 -1.0901105 -0.7496133
24 3.8947239 -1.659389 0.516987
25 3.9258208 -0.8841055 1.3251652
26 4.9554296 -2.0063238 0.4150401
27 3.0359709 -2.8971462 1.0103722
28 3.8185678 -3.6568248 1.2752906
29 2.4917984 -3.195833 0.0744643
30 2.0725911 -2.848428 2.0760021
31 1.638817 -1.4838974 2.5253139
32 2.5752075 -1.0062795 2.9080422
33 0.9012089 -1.6500344 3.3573053
34 0.8815328 -0.5306711 1.5538689
35 0.5519052 -1.1815579 0.7041188
36 1.6224746 0.2331944 1.1997508
37 -0.2989756 -0.0199954 2.1694908
38 -0.3033598 1.4095408 2.1280825
39 0.0521263 1.761717 1.1273303
40 0.4747811 1.7876458 2.8392599
41 -1.6030958 1.9523106 2.4553161
42 -1.5646386 2.9988577 2.8519616
43 -1.9732467 1.2583804 3.2576206
44 -2.5225735 1.8953969 1.3081864
45 -3.3669469 3.0741107 1.0973018
46 -3.0220368 3.8450892 1.8318384
47 -4.4858675 3.0095129 1.1439484
48 -3.0599689 3.6382723 -0.3005937
49 -3.982976 3.5193791 -0.9249329
50 -2.1988642 3.09917 -0.7700861
51 -2.7010767 5.025878 -0.199455
52 -1.3877664 5.5169363 -0.1698399
53 -0.8882234 5.1431508 -1.0995853
54 -0.935725 4.957068 0.6896982
55 -1.3304483 7.055419 0.0381237
56 -2.0611646 7.6166778 -0.601446
57 -0.3436857 7.3639388 -0.3955144
58 -1.5631742 7.5380082 1.3714558
59 -2.4256234 7.9039402 1.5299768

Types

1 H 
2 OAlc 
3 CPos 
4 HC 
5 HC 
6 C 
7 HC 
8 HC 
9 OE 
10 C 
11 HC 
12 HC 
13 C 
14 HC 
15 HC 
16 OE 
17 C 
18 HC 
19 HC 
20 C 
21 HC 
22 HC 
23 OE 
24 C 
25 HC 
26 HC 
27 C 
28 HC 
29 HC 
30 OE 
31 C 
32 HC 
33 HC 
34 C 
35 HC 
36 HC 
37 OE 
38 C 
39 HC 
40 HC 
41 C 
42 HC 
43 HC 
44 OE 
45 C 
46 HC 
47 HC 
48 C 
49 HC 
50 HC 
51 OE 
52 C 
53 HC 
54 HC 
55 CPos 
56 HC 
57 HC 
58 OAlc 
59 H 

Charges

1 0.211 
2 -0.328 
3 -0.019 
4 0.093 
5 0.093 
6 -0.063 
7 0.079 
8 0.079 
9 -0.295 
10 -0.021 
11 0.084 
12 0.084 
13 -0.023 
14 0.083 
15 0.083
16 -0.283 
17 -0.023 
18 0.083 
19 0.083 
20 -0.023 
21 0.083
22 0.083 
23 -0.283 
24 -0.023 
25 0.082 
26 0.082 
27 -0.023 
28 0.082 
29 0.082 
30 -0.283 
31 -0.023 
32 0.082 
33 0.082 
34 -0.023 
35 0.082 
36 0.082 
37 -0.283 
38 -0.023 
39 0.082 
40 0.083
41 -0.023 
42 0.083 
43 0.083 
44 -0.283 
45 -0.023 
46 0.083 
47 0.083
48 -0.021 
49 0.084 
50 0.084 
51 -0.295 
52 -0.063 
53 0.079 
54 0.079 
55 -0.019 
56 0.093 
57 0.093 
58 -0.328 
59 0.211 

Bonds

1 g18 13 16 
2 g18 16 17 
3 g18 20 23 
4 g18 23 24 
5 g18 27 30 
6 g18 30 31 
7 g18 34 37 
8 g18 37 38 
9 g18 41 44 
10 g18 44 45 
11 g18 48 51 
12 g18 51 52 
13 g18 6 9 
14 g18 9 10 
15 g26 17 20 
16 g26 24 27 
17 g26 31 34 
18 g26 38 41 
19 g27 10 13 
20 g27 3 6 
21 g27 45 48 
22 g27 52 55 
23 g4 10 11 
24 g4 10 12 
25 g4 13 14 
26 g4 13 15 
27 g4 17 18 
28 g4 17 19 
29 g4 20 21 
30 g4 20 22 
31 g4 24 25 
32 g4 24 26 
33 g4 27 28 
34 g4 27 29 
35 g4 3 4 
36 g4 3 5 
37 g4 31 32 
38 g4 31 33 
39 g4 34 35 
40 g4 34 36 
41 g4 38 39 
42 g4 38 40 
43 g4 41 42 
44 g4 41 43 
45 g4 45 46 
46 g4 45 47 
47 g4 48 49 
48 g4 48 50 
49 g4 52 53 
50 g4 52 54 
51 g4 55 56 
52 g4 55 57 
53 g4 6 7 
54 g4 6 8 
55 g56 2 3 
56 g56 55 58 
57 g71 1 2 
58 g71 58 59 

Angles

1 g102 14 13 16 
2 g102 15 13 16 
3 g102 2 3 4 
4 g102 2 3 5 
5 g102 21 20 23 
6 g102 22 20 23 
7 g102 23 24 25 
8 g102 23 24 26 
9 g102 30 31 32 
10 g102 30 31 33 
11 g102 35 34 37 
12 g102 36 34 37 
13 g102 37 38 39 
14 g102 37 38 40 
15 g102 4 3 5 
16 g102 4 3 6 
17 g102 44 45 46 
18 g102 44 45 47 
19 g102 5 3 6 
20 g102 52 55 56 
21 g102 52 55 57 
22 g102 56 55 57 
23 g102 56 55 58 
24 g102 57 55 58 
25 g12 1 2 3 
26 g12 13 16 17 
27 g12 20 23 24 
28 g12 27 30 31 
29 g12 34 37 38 
30 g12 41 44 45 
31 g12 48 51 52 
32 g12 55 58 59 
33 g12 6 9 10 
34 g13 10 13 16 
35 g13 16 17 20 
36 g13 17 20 23 
37 g13 23 24 27 
38 g13 3 6 9 
39 g13 30 31 34 
40 g13 31 34 37 
41 g13 37 38 41 
42 g13 38 41 44 
43 g13 44 45 48 
44 g13 45 48 51 
45 g13 51 52 55 
46 g13 9 10 13 
47 g14 11 10 12 
48 g14 14 13 15 
49 g14 18 17 19 
50 g14 21 20 22 
51 g14 25 24 26 
52 g14 28 27 29 
53 g14 32 31 33 
54 g14 35 34 36 
55 g14 39 38 40 
56 g14 42 41 43 
57 g14 46 45 47 
58 g14 49 48 50 
59 g14 51 52 53 
60 g14 51 52 54 
61 g14 53 52 54 
62 g14 7 6 8 
63 g14 7 6 9 
64 g14 8 6 9 
65 g15 2 3 6 
66 g15 3 6 7 
67 g15 3 6 8 
68 g15 52 55 58 
69 g15 53 52 55 
70 g15 54 52 55 
71 g51 10 13 14 
72 g51 10 13 15 
73 g51 11 10 13 
74 g51 12 10 13 
75 g51 16 17 18 
76 g51 16 17 19 
77 g51 17 20 21 
78 g51 17 20 22 
79 g51 18 17 20 
80 g51 19 17 20 
81 g51 24 27 28 
82 g51 24 27 29 
83 g51 25 24 27 
84 g51 26 24 27 
85 g51 28 27 30 
86 g51 29 27 30 
87 g51 31 34 35 
88 g51 31 34 36 
89 g51 32 31 34 
90 g51 33 31 34 
91 g51 38 41 42 
92 g51 38 41 43 
93 g51 39 38 41 
94 g51 40 38 41 
95 g51 42 41 44 
96 g51 43 41 44 
97 g51 45 48 49 
98 g51 45 48 50 
99 g51 46 45 48 
100 g51 47 45 48 
101 g56 49 48 51 
102 g56 50 48 51 
103 g56 9 10 11 
104 g56 9 10 12 

Dihedrals

1 g23 1 2 3 6 
2 g23 10 13 16 17 
3 g23 13 16 17 20 
4 g23 17 20 23 24 
5 g23 20 23 24 27 
6 g23 27 30 31 34 
7 g23 3 6 9 10 
8 g23 31 34 37 38 
9 g23 34 37 38 41 
10 g23 38 41 44 45 
11 g23 41 44 45 48 
12 g23 45 48 51 52 
13 g23 48 51 52 55 
14 g23 52 55 58 59 
15 g23 6 9 10 13 
16 g34 2 3 6 9 
17 g34 51 52 55 58 
18 g46 16 17 20 23 
19 g46 30 31 34 37 
20 g46 37 38 41 44 
21 g46 44 45 48 51 
22 g46 9 10 13 16 
23 glj14 1 2 3 4 
24 glj14 1 2 3 5 
25 glj14 11 10 13 14 
26 glj14 11 10 13 15 
27 glj14 11 10 13 16 
28 glj14 12 10 13 14 
29 glj14 12 10 13 15 
30 glj14 12 10 13 16 
31 glj14 13 16 17 18 
32 glj14 13 16 17 19 
33 glj14 14 13 16 17 
34 glj14 15 13 16 17 
35 glj14 16 17 20 21 
36 glj14 16 17 20 22 
37 glj14 18 17 20 21 
38 glj14 18 17 20 22 
39 glj14 18 17 20 23 
40 glj14 19 17 20 21 
41 glj14 19 17 20 22 
42 glj14 19 17 20 23 
43 glj14 2 3 6 7 
44 glj14 2 3 6 8 
45 glj14 20 23 24 25 
46 glj14 20 23 24 26 
47 glj14 21 20 23 24 
48 glj14 22 20 23 24 
49 glj14 23 24 27 28 
50 glj14 23 24 27 29 
51 glj14 25 24 27 28 
52 glj14 25 24 27 29 
53 glj14 26 24 27 28 
54 glj14 26 24 27 29 
55 glj14 27 30 31 32 
56 glj14 27 30 31 33 
57 glj14 28 27 30 31 
58 glj14 29 27 30 31 
59 glj14 30 31 34 35 
60 glj14 30 31 34 36 
61 glj14 32 31 34 35 
62 glj14 32 31 34 36 
63 glj14 32 31 34 37 
64 glj14 33 31 34 35 
65 glj14 33 31 34 36 
66 glj14 33 31 34 37 
67 glj14 34 37 38 39 
68 glj14 34 37 38 40 
69 glj14 35 34 37 38 
70 glj14 36 34 37 38 
71 glj14 37 38 41 42 
72 glj14 37 38 41 43 
73 glj14 39 38 41 42 
74 glj14 39 38 41 43 
75 glj14 39 38 41 44 
76 glj14 4 3 6 7 
77 glj14 4 3 6 8 
78 glj14 4 3 6 9 
79 glj14 40 38 41 42 
80 glj14 40 38 41 43 
81 glj14 40 38 41 44 
82 glj14 41 44 45 46 
83 glj14 41 44 45 47 
84 glj14 42 41 44 45 
85 glj14 43 41 44 45 
86 glj14 44 45 48 49 
87 glj14 44 45 48 50 
88 glj14 46 45 48 49 
89 glj14 46 45 48 50 
90 glj14 46 45 48 51 
91 glj14 47 45 48 49 
92 glj14 47 45 48 50 
93 glj14 47 45 48 51 
94 glj14 48 51 52 53 
95 glj14 48 51 52 54 
96 glj14 49 48 51 52 
97 glj14 5 3 6 7 
98 glj14 5 3 6 8 
99 glj14 5 3 6 9 
100 glj14 50 48 51 52 
101 glj14 51 52 55 56 
102 glj14 51 52 55 57 
103 glj14 53 52 55 56 
104 glj14 53 52 55 57 
105 glj14 53 52 55 58 
106 glj14 54 52 55 56 
107 glj14 54 52 55 57 
108 glj14 54 52 55 58 
109 glj14 56 55 58 59 
110 glj14 57 55 58 59 
111 glj14 6 9 10 11 
112 glj14 6 9 10 12 
113 glj14 7 6 9 10 
114 glj14 8 6 9 10 
115 glj14 9 10 13 14 
116 glj14 9 10 13 15 
```

All atoms, bonds, angles, and dihedrals are listed explicitly; types map to parameters.inc.

Count connections in a connected acyclic moleculeEq. 2

![Count connections in a connected acyclic molecule](https://ml-biomat.com/static/agent-math/06af21f58d192d5a49dedea3.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Nbond | Number of graph edges, representing distinct bonded pairs | 1 |
| Natom | Number of vertices, representing explicit atoms | 1 |
| −, 1, = | Subtract one, a dimensionless constant; equality gives the tree count | 1 |

Reading the relationshipStarting from one atom, attaching each new atom by one bond adds one vertex and one edge. Without cycles, edges remain one fewer than vertices.

A worked exampleWater has 3 atoms and 2 bonds; this PEG has 59 atoms and 58 bonds. A graph traversal additionally checks that each is one connected component.

ConditionsApplies to a connected acyclic graph. Rings, multiple molecules, and networks have corresponding graph relationships; a curved spatial shape does not itself create a graph cycle.

Angle and dihedral counts depend on more than the backbone length. Explicit hydrogens form branches, generating different three- and four-atom paths, while the force field determines which interactions are listed and how they are parameterized. For four sequentially connected atoms, the first three define one plane and the last three another. Their relative orientation defines a dihedral angle. Rotation about the middle bond can change an endpoint's direction considerably while leaving nearby bond lengths close to their preferred values. Combining many such local rotations gives a flexible chain its range of overall shapes.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l05/en/#en-s3)

Figure 3 · Geometric illustration of bond length, angle and dihedral. Translucent triangles mark the two three-atom planes sharing the highlighted 2–3 bond; φ describes the angle between these planes.

A molecule template and a complete-system data file serve different roles. The template describes an object to be placed or copied. A data file additionally describes the box, system-wide IDs, molecular membership, and the complete set of interactions. With atom_style full, an ordinary Atoms record contains atom ID, molecule ID, type, charge, and three coordinates; optional image flags describe periodic images. Interpret a row through its section and atom style before assigning meanings to its columns. This prevents local template IDs from being mistaken for permanent IDs in a solution and ensures that copied molecules remain distinct objects.

## Which geometric change does each energy term measure?

Connectivity identifies linked atoms without yet specifying how they move. A practical model assigns energy rules to different changes. Deviating from a preferred bond length has a cost, deviating from a preferred angle has another, and rotation about a bond passes through a periodic energy landscape. Together with nonbonded interactions, these terms define potential energy and forces. Separate terms are a way of organizing the model rather than physically isolating each motion: moving one atom can alter several bonds, angles, and nonbonded distances at once. Its final force combines the contributions from all the relevant changes.

The LAMMPS harmonic bond potential is a parabola around an equilibrium distance. Subtract that distance from the current bond length to obtain extension or compression. Squaring makes either direction contribute a positive energy cost, and a coefficient determines the cost's magnitude. A spring is a useful analogy, provided its coefficient convention is checked. In this LAMMPS command, the familiar factor of one half is already incorporated into K. A stiffness copied from a formula that keeps the half explicitly therefore requires conversion. Matching units is necessary, but the algebraic definition must match as well.

Energy and restoring force of a LAMMPS harmonic bondEq. 3

![Energy and restoring force of a LAMMPS harmonic bond](https://ml-biomat.com/static/agent-math/d55282782159f711c94f7c1c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Ub | Energy of one harmonic bond | kcal mol⁻¹ |
| Kb | LAMMPS coefficient including the conventional factor of one half | kcal mol⁻¹ Å⁻² |
| r, r₀ | Current and equilibrium bond lengths | Å |
| Fr | Radial force defined positive toward increasing length | kcal mol⁻¹ Å⁻¹ |
| ², −, =, ×, 2 | Squaring gives both compression and extension a cost; the minus sign directs force down the energy gradient; equality defines; adjacent factors multiply; 2 comes from the quadratic slope | 1 |

Reading the relationshipMultiply squared extension by the coefficient to obtain energy. Its slope is 2Kb(r−r0); negate it for the radial restoring force.

A worked exampleFor water Kb=529.581 and r0=1.012 Å, r=1.032 Å gives extension 0.020 Å, Ub=0.2118324 kcal/mol and Fr=−21.18324 kcal/(mol Å), directed toward shortening.

ConditionsThis is the harmonic contribution for a fixed bond. Other terms contribute to total atomic forces; the model retains connectivity through this potential.

The curve also explains the restoring force. If the bond is stretched, increasing its length raises energy, so the force tends to shorten it. Compression reverses that direction. The slope of the parabola introduces a factor of two, and the negative sign in the force–energy relationship directs motion toward decreasing energy. Without calculus, estimate the slope by slightly increasing the distance, calculating the corresponding energy change, and dividing by the distance increment. The general relation between force and energy from the third lesson now describes a specific bonded coordinate and explains how its parameter enters motion.

The angle potential has a similar squared form, with an additional unit conversion. Its equilibrium angle is entered in degrees, but angular deviations are evaluated internally in radians. A radian measures an arc length divided by its circle's radius: half a revolution is π radians or 180 degrees. A five-degree deviation is therefore approximately 0.08727 radians before entering the energy expression. Substituting five directly would enlarge the squared contribution by more than three thousand. Understanding this conversion turns what looks like a formatting detail into a substantial physical distinction in the calculated forces and energies.

Convert angular deviations to radians before evaluating energyEq. 4

![Convert angular deviations to radians before evaluating energy](https://ml-biomat.com/static/agent-math/376f11665921ded0ea330039.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Δθdeg | Current angle minus equilibrium angle in degrees | ° |
| Δθrad | The same angular deviation in radians | rad |
| Kθ | Angular potential coefficient | kcal mol⁻¹ rad⁻² |
| Uθ | Energy of this angle term | kcal mol⁻¹ |
| π, 180, /, ², =, × | π radians equals 180 degrees; divide and multiply to convert, then square; equality defines; adjacent factors multiply | 1 |

Reading the relationshipDegrees and radians describe the same geometry. The coefficient uses squared radians, so the angular deviation must use that convention.

A worked exampleFor water Kθ=37.95 and equilibrium angle 113.24°, a current 118.24° gives 5°=0.0872665 rad and approximately 0.28901 kcal/mol.

ConditionsThis is the LAMMPS harmonic angle convention: equilibrium input in degrees, internal angular calculation in radians.

The dihedral command needs its own formula despite sharing the word harmonic. Here, dihedral_style harmonic uses a periodic cosine expression rather than the quadratic form used for bonds and angles. After a complete revolution, the geometry repeats, so the energy must repeat too. The integer n controls the number of repetitions in a turn, d selects the placement of peaks and valleys, and K sets the energy scale. Some terms in this example have threefold periodicity. The distribution of the complete molecule still depends on all other energy terms and its solvent, so a minimum of one torsional term does not identify the chain's only conformation.

How a periodic torsion produces several preferred anglesEq. 5

![How a periodic torsion produces several preferred angles](https://ml-biomat.com/static/agent-math/a44eeef478426e584c2c40d3.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Uφ | Energy contribution of one dihedral term | kcal mol⁻¹ |
| Kφ | Coefficient setting the periodic energy scale | kcal mol⁻¹ |
| φ | Dihedral angle defined by four sequentially bonded atoms | rad |
| n | Integer multiplicity | 1 |
| d | Either +1 or −1, selecting the cosine sign | 1 |
| cos, 1, +, [ ], =, × | Cosine repeats periodically; 1 is a constant; addition and brackets combine terms; equality defines; adjacent factors multiply | 1 |

Reading the relationshipA full turn repeats the geometry and cosine. Multiplicity changes repeats per turn; the coefficient and sign set scale and phase.

A worked exampleFor PEG g23, Kφ=0.3011, d=1, n=3. At 0°, U=0.6022 kcal/mol; at 60°, U=0 because cos 180°=−1; at 120°, U returns to 0.6022.

ConditionsThis is one periodic term. Numerical cosine uses radians; the complete conformation includes other bonded and nonbonded contributions.

Analytic parameter exercise: select a geometric term and evaluate its energy response.

[Figure: Analytic bonded potential and selected geometry](https://ml-biomat.com/tutorials/molecular-dynamics/l05/en/#en-s4)

Three analytic terms use parameters from this example. The vertical scale adapts to the selected term while retaining energy units.

The interactive figure varies a bond length, bond angle, or torsion and evaluates the corresponding energy using a particular parameter from this example. It gives each parameter a visible geometric meaning. Apply that observation to PEG: many torsions can reorganize as the chain extends, moving its ends farther apart while individual covalent bond lengths fluctuate over a smaller range. Overall extension therefore does not require every bond to stretch by the same factor. The seventh lesson examines actual trajectories to distinguish these scales through terminal separation, radius of gyration, and local angular motion.

## Read parameters together with units and pairing rules

The parameters.inc file collects type labels, masses, and interaction coefficients. Its label map assigns the eight atom categories used by PEG and water. Masses are supplied by type, while charges reside in the per-atom template entries. A mass table consequently does not define water completely, and copying pair_coeff lines does not replace the Charges section. Follow a label from the template to its parameter entry and then to the selected functional form. This establishes which mathematical expression receives each number and keeps chemical identity connected to the particular calculation being performed.

### Complete parameters and type labels

```
# LAMMPS Include File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

labelmap atom 1 OE 2 C 3 HC 4 H 5 CPos 6 OAlc 7 OW 8 HW
labelmap bond 1 g4 2 g18 3 g26 4 g27 5 g56 6 g71 7 OW-HW
labelmap angle 1 g12 2 g13 3 g14 4 g15 5 g51 6 g56 7 g102 8 HW-OW-HW
labelmap dihedral 1 g23 2 g34 3 g46 4 glj14

mass OE 15.9994 # PEG O (GROMOS 54A7)
mass C 12.011 # PEG C (GROMOS 54A7)
mass HC 1.008 # PEG H (GROMOS 54A7)
mass H 1.008 # PEG H (GROMOS 54A7)
mass CPos 12.011 # PEG C (GROMOS 54A7)
mass OAlc 15.9994 # PEG O (GROMOS 54A7)
mass OW 15.9994 # H2O O (SPC/Fw)
mass HW 1.008 # H2O H (SPC/Fw)

pair_coeff OE OE 0.2526 2.8492
pair_coeff C C 0.0663 3.5812
pair_coeff HC HC 0.0283 2.3734
pair_coeff H H 0.0 0.0
pair_coeff CPos CPos 0.2450 2.8114
pair_coeff OAlc OAlc 0.1195 3.1000
pair_coeff OW OW 0.155 3.165
pair_coeff HW HW 0.0 0.0

bond_coeff g4 1109.2926 1.12
bond_coeff g18 399.7916 1.43
bond_coeff g26 299.8440 1.52
bond_coeff g27 400.0343 1.53
bond_coeff g56 310.7075 1.41
bond_coeff g71 179.2543 0.971
bond_coeff OW-HW 529.581 1.012

angle_coeff g12 47.6940 109.5
angle_coeff g13 55.1271 109.5
angle_coeff g14 47.6350 109.6
angle_coeff g15 55.1139 111.0
angle_coeff g51 54.9931 110.3
angle_coeff g56 180.4602 109.0
angle_coeff g102 30.1731 110.0
angle_coeff HW-OW-HW 37.95 113.24

dihedral_coeff g23 0.3011 1 3
dihedral_coeff g34 1.4149 1 3
dihedral_coeff g46 0.2390 -1 3
dihedral_coeff glj14 0.0 1 1
```

Interpret coefficients with the example functional forms and real units.

The real unit system uses ångströms for length, femtoseconds for time, kilocalories per mole for energy, kelvin for temperature, and atmospheres for pressure. A one-femtosecond step is therefore entered as 1.0, while a temperature of 300 means 300 K and pressure one means one atmosphere. The temperature one used in our earlier reduced LJ model had another scale; the bare numbers cannot be compared. Reading a bond coefficient as kilocalories per mole per squared ångström also makes a dimensional check possible: multiplying by a squared length deviation must recover an energy. The unit system gives each numerical field its physical context.

Convert the molecular force unit to piconewtonsEq. 6

![Convert the molecular force unit to piconewtons](https://ml-biomat.com/static/agent-math/80ada808bc3f7ad515f86d61.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| kcal, mol, Å | Kilocalorie, mole, and ångström; the example energy and length units | units |
| NA | Avogadro constant 6.02214076×10²³ | mol⁻¹ |
| N, pN | Newton and piconewton; 1 pN=10⁻¹²N | force units |
| 4184, 10⁻¹⁰ | 4184 joules per kilocalorie and 10⁻¹⁰ metres per ångström | J/kcal; m/Å |
| =, ≈, /, × | Equality converts units; approximate equality rounds the final digits; divide as shown; multiplication combines the denominator | 1 |

Reading the relationshipDivide molar energy by Avogadro’s constant to obtain a single-interaction energy, then divide by length in metres to obtain newtons.

A worked example1 kcal/(mol Å) is approximately 69.477 pN and 10 kcal/(mol Å) approximately 694.77 pN. Conversion changes the unit expression while preserving the physical force.

ConditionsApplies to forces in units real; convert the molar energy convention consistently to an atom-level expression.

SPC/Fw retains changes in water bond lengths and angles. Wu, Tepper, and Voth's 2006 study connected molecular geometry parameters with collective liquid properties, including diffusion and dielectric response. Small intramolecular changes could therefore influence the behaviour of many surrounding molecules. Our parameter set uses an oxygen charge of −0.82e, an equilibrium O–H distance of 1.012 Å, and an equilibrium angle of 113.24 degrees. These define this particular flexible model. Equilibrium parameters differ from individual instantaneous measurements, since thermal motion and neighbouring molecules contribute to the distribution of internal geometries. [Wu, Tepper and Voth, 2006](https://doi.org/10.1063/1.2136877)

The supplied PEG parameters derive from GROMOS54A7 and are combined with SPC/Fw in this explicit teaching model. We retain that combination to study topology, solvent preparation, and imposed-force response. A quantitative question about chain dimensions or force spectroscopy additionally calls for evaluating its PEG–water interactions against hydration, density, chain-size, or force–extension observations under the intended conditions. The object being evaluated is the complete interaction combination rather than its family name alone. That distinction also provides a constructive route to improvement: identify the observable requiring a better description, then trace which interactions influence it.

Bonded neighbours require particular nonbonded rules. A directly connected pair has a 1–2 relationship; pairs connected by two or three bonds are called 1–3 and 1–4. The labels describe distance through the graph rather than separations of one, two, or three ångströms. Because bonded terms already account for parts of intramolecular energetics, force fields prescribe exclusions or scaled nonbonded interactions for these pairs. Our input sets LJ weights to 0, 0, and 0.5, Coulomb weights to 0, 0, and 1, and retains the angle yes rule. These settings form part of the molecular definition alongside the connection records.

The angle yes option further relates 1–3 exclusions to explicitly listed angles and dihedrals. An inspection must therefore consider both graph paths and the specified interaction lists rather than deriving every calculation from path length alone. The general lesson is to carry the conventions together: local geometric potentials, special-neighbour weights, LJ mixing, and charges jointly define the model. Changing the solvent or transferring molecular parameters calls for checking each relevant convention. Modifying a number that resembles an interaction strength can otherwise alter an internal balance that depended on several coordinated definitions.

## Give an inserted molecule actual space in the solvent

Preparation starts with a rectangular box measuring sixty by thirty by thirty ångströms, or six by three by three nanometres. Storage is reserved for eight atom types, seven bond types, eight angle types, and four dihedral types. These are parameter categories rather than counts of particles or connections already present. A library establishes categories before filling its shelves; similarly, seven hundred copied waters share two atom types and a common O–H bond type. The distinction between categories and instances explains why a short coefficient table can describe a system containing thousands of atoms.

The molecule command reads a template, and create_atoms places copies into the system. Its leading zero is a type offset, retaining the template's existing type correspondence; it does not require system atom IDs to remain one, two, and three. The random-placement seeds control position and orientation choices, while overlap and maxtry set contact checks and permitted insertion attempts. Read the actual created count because a finite number of attempts can fail to place every requested molecule. Composition influences the later mass and density, making the construction output an important part of interpreting the initial state.

### Construct and prepare seven hundred water molecules

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

units real
atom_style full
bond_style harmonic
angle_style harmonic
dihedral_style harmonic
pair_style lj/cut/coul/long 10
kspace_style ewald 1e-5
special_bonds lj 0.0 0.0 0.5 coul 0.0 0.0 1.0 angle yes

region box block -30 30 -15 15 -15 15
  create_box 8 box &
  bond/types 7 &
  angle/types 8 &
  dihedral/types 4 &
  extra/bond/per/atom 3 &
  extra/angle/per/atom 6 &
  extra/dihedral/per/atom 10 &
  extra/special/per/atom 14

include parameters.inc

molecule h2omol water.mol
create_atoms 0 random 700 87910 NULL mol h2omol 454756 overlap 1.0 maxtry 50

group H2O type OW HW
minimize 1.0e-4 1.0e-6 100 1000
reset_timestep 0

fix mynpt all npt temp 300 300 100 iso 1 1 1000


thermo 500
thermo_style custom step temp etotal vol density


# Numerical diagnostics; all energies are whole-system kcal/mol.
compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cPress all pressure cTemp
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE
variable K equal c_cKE
variable E equal c_cPE+c_cKE
variable P equal c_cPress
variable V equal vol
variable rho equal density
thermo_style custom step time c_cTemp c_cPE c_cKE etotal c_cPress vol density
thermo_modify norm no
thermo 250
fix record all ave/time 50 1 50 v_clock v_T v_U v_K v_E v_P v_V v_rho file water-thermo.dat format " %.15g"
dump trajectory all custom 250 water.lammpstrj id mol type q x y z vx vy vz ix iy iz
dump_modify trajectory sort id

timestep 1.0
run 15000

write_restart water.restart
# write_data water.data # uncomment to write a .data file as well
write_data water.data
```

Run lmp -in water.lmp and inspect actual creation counts and numeric records.

The water undergoes a geometric minimization followed by fifteen picoseconds of isotropic NPT preparation. All three directions scale together, preserving the rectangular aspect ratio while changing volume, with targets of 300 K and one atmosphere. The water input uses Ewald for long-range electrostatics, whereas the combined system subsequently uses PPPM with the stated accuracy settings. Both account for the long-range contribution of periodic charges; switching the numerical summation method does not change water's chemical composition. The recorded temperature and density show how this particular preparation interval proceeds, rather than relying on its stage name to describe the outcome.

One PEG template is then placed near the box centre. Existing waters have not made room in advance, so some lie too close to the inserted atoms. Overlap deletion uses mol yes to remove complete water molecules. Deleting only a nearby hydrogen would disrupt molecular composition, connectivity, and charge. The inspection therefore checks the remaining waters, total atoms, and connections again. The overlap distance is a construction choice designed to produce a usable starting arrangement; the number removed depends on the actual positions. This connects a geometric preparation rule to a composition change that can be verified in the resulting system.

### Insert PEG and remove overlapping whole waters

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

kspace_style pppm 1e-5
read_restart water.restart

molecule pegmol peg.mol
create_atoms 0 single 0 0 0 mol pegmol 454756

group PEG type C CPos H HC OAlc OE

delete_atoms overlap 2.0 H2O PEG mol yes


fix mynpt all npt temp 300 300 100 x 1 1 1000
fix myrct PEG recenter 0 0 0 shift all
timestep 1.0

thermo 500

# Numerical diagnostics; all energies are whole-system kcal/mol.
compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cPress all pressure cTemp
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE
variable K equal c_cKE
variable E equal c_cPE+c_cKE
variable P equal c_cPress
variable V equal vol
variable rho equal density
thermo_style custom step time c_cTemp c_cPE c_cKE etotal c_cPress vol density
thermo_modify norm no
thermo 250
compute rg PEG gyration
fix record all ave/time 50 1 50 v_clock v_T v_U v_K v_E v_P v_V v_rho c_rg file merge-thermo.dat format " %.15g"
dump trajectory all custom 250 merge.lammpstrj id mol type q x y z vx vy vz ix iy iz
dump_modify trajectory sort id
dump chain PEG custom 50 merge-peg.lammpstrj id mol type q xu yu zu vx vy vz
dump_modify chain sort id

run 10000

write_restart merge.restart
# write_data merge.data # uncomment to write a .data file as well
write_data merge.data
```

After water.lmp, run lmp -in merge.lmp using its checkpoint in the same directory.

The ten-picosecond preparation after insertion allows pressure coupling along x while retaining the y and z dimensions. Its volume response therefore differs from the earlier isotropic stage. The input also recentres the PEG centre of mass at the origin by translating all atoms. That shared translation preserves internal distances, angles, and chain dimensions, making the trajectory suitable for conformational analysis. Laboratory-frame translational diffusion requires a record that retains the corresponding overall motion. Coordinate processing should follow the observable: centring provides a convenient view, while the meaning of any displacement measurement still depends on which motion has been retained.

Separating preparation stages helps distinguish causes of change. First the water adjusts its volume, then the chain is inserted and crowded contacts are removed, and finally the combined model explores temperature, volume, and conformation. If the chain initially extends, examine overlap, local solvent space, and coordinate processing before assigning all of that change to a material property. The subsequent time record shows whether other shapes continue to be explored. This establishes a clearer baseline for pulling: distinguish the chain's unforced motion from the response that appears after an external force is applied.

## Make connection tables, structural pictures, and records agree

The complete program below turns the templates into readable structural descriptions. It parses coordinates, types, charges, and connections by section, then checks referenced IDs, duplicates, and the declared counts. It constructs a graph and follows bonds from one atom to determine whether the whole PEG belongs to one connected object. Element counts, atom categories, graph degrees, and total charge are collected separately. A graph degree counts an atom's bonded partners and helps distinguish terminal hydrogens, backbone oxygens, and carbon environments. Together these observations connect the file's detailed records to the short molecule described in the text.

### Complete Python: templates, parameter curves, and preparation records

```
#!/usr/bin/env python3
"""Inspect the supplied PEG/water templates and plot actual preparation records.

python inspect_molecule.py --input . --run . --output figures --language en
Requires NumPy and Matplotlib. --input holds peg.mol and water.mol; --run holds
water-thermo.dat, merge-thermo.dat, and merge.data from the preparation commands.
"""
from pathlib import Path
from collections import Counter, deque
import argparse
import json
import re
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


ELEMENT = {'OE': 'O', 'OAlc': 'O', 'OW': 'O', 'C': 'C', 'CPos': 'C',
           'HC': 'H', 'H': 'H', 'HW': 'H'}


def molecule(path):
    counts, sections = {}, {}
    current = None
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.split('#', 1)[0].strip()
        if not line:
            continue
        match = re.fullmatch(r'(\d+) (atoms|bonds|angles|dihedrals)', line)
        if match:
            counts[match[2]] = int(match[1])
        elif line in ('Coords', 'Types', 'Charges', 'Bonds', 'Angles', 'Dihedrals'):
            current = line
            sections[current] = []
        elif current:
            sections[current].append(line.split())
    for key in ('Coords', 'Types', 'Charges', 'Bonds', 'Angles'):
        if key not in sections:
            raise ValueError(f'{path.name}: missing {key}.')
    ids = [int(row[0]) for row in sections['Coords']]
    if len(ids) != counts['atoms'] or len(set(ids)) != len(ids):
        raise ValueError('Atom count or unique IDs do not agree.')
    coords = {int(row[0]): np.array(row[1:], dtype=float) for row in sections['Coords']}
    types = {int(row[0]): row[1] for row in sections['Types']}
    charges = {int(row[0]): float(row[1]) for row in sections['Charges']}
    if set(coords) != set(types) or set(coords) != set(charges):
        raise ValueError('Position, type, and charge IDs disagree.')
    if any(value.shape != (3,) or not np.all(np.isfinite(value)) for value in coords.values()):
        raise ValueError('Each atom requires three finite coordinates.')
    graph = {atom: set() for atom in ids}
    connections = {}
    for section, noun, width in [('Bonds', 'bonds', 2), ('Angles', 'angles', 3), ('Dihedrals', 'dihedrals', 4)]:
        records = sections.get(section, [])
        if len(records) != counts.get(noun, 0):
            raise ValueError(f'{section} count differs from the header.')
        if len({int(row[0]) for row in records}) != len(records):
            raise ValueError(f'Duplicate IDs in {section}.')
        connections[section] = []
        for row in records:
            atoms = [int(x) for x in row[2:]]
            if len(atoms) != width or len(set(atoms)) != width or not set(atoms).issubset(coords):
                raise ValueError(f'Invalid reference in {section}.')
            connections[section].append((row[1], atoms))
            if section == 'Bonds':
                first, second = atoms
                if second in graph[first]:
                    raise ValueError('Repeated physical bond.')
                graph[first].add(second)
                graph[second].add(first)
    for section in ('Angles', 'Dihedrals'):
        for _, atoms in connections[section]:
            if any(v not in graph[u] for u, v in zip(atoms, atoms[1:])):
                raise ValueError(f'{section} does not follow bonded atoms.')
    unseen = set(ids)
    components = []
    while unseen:
        start = next(iter(unseen))
        queue, seen = deque([start]), {start}
        while queue:
            for neighbour in graph[queue.popleft()]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        components.append(len(seen))
        unseen -= seen
    summary = {'counts': counts, 'type_counts': dict(Counter(types.values())),
               'element_counts': dict(Counter(ELEMENT[t] for t in types.values())),
               'total_charge_e': float(sum(charges.values())), 'component_sizes': components,
               'cycle_rank': counts['bonds'] - counts['atoms'] + len(components),
               'degree_counts': dict(Counter(len(x) for x in graph.values()))}
    return coords, types, connections, summary


def thermo(path, columns):
    values = np.loadtxt(path, comments='#', ndmin=2)
    if values.shape[1] != columns or not np.all(np.isfinite(values)):
        raise ValueError(f'Expected {columns} finite columns in {path.name}.')
    if len(values) < 2 or np.any(np.diff(values[:, 1]) <= 0):
        raise ValueError('Recorded times must increase strictly.')
    return values


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path('.'))
    parser.add_argument('--run', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path, default=Path('figures'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args()
    coords, types, links, peg = molecule(args.input / 'peg.mol')
    _, _, _, water = molecule(args.input / 'water.mol')
    if peg['element_counts'] != {'H': 34, 'O': 9, 'C': 16}:
        raise ValueError('PEG composition differs from C16H34O9.')
    if peg['component_sizes'] != [59] or peg['cycle_rank'] != 0:
        raise ValueError('Expected a single acyclic PEG connection graph.')
    if abs(peg['total_charge_e']) > 1e-8 or abs(water['total_charge_e']) > 1e-8:
        raise ValueError('A template is not electrically neutral.')
    water_record = thermo(args.run / 'water-thermo.dat', 9)
    merge_record = thermo(args.run / 'merge-thermo.dat', 10)
    data = (args.run / 'merge.data').read_text(encoding='utf-8')
    match = re.search(r'^\s*(\d+) atoms\s*$', data, re.M)
    if not match:
        raise ValueError('Missing prepared-system atom count.')
    final_atoms = int(match[1])
    if (final_atoms - 59) % 3:
        raise ValueError('Prepared count cannot contain PEG and complete three-site waters.')
    retained_water = (final_atoms - 59) // 3
    summary = {'PEG': peg, 'water': water, 'prepared_atoms': final_atoms,
               'retained_water_molecules': retained_water,
               'removed_water_molecules': 700 - retained_water,
               'preparation_final_time_ps': float(merge_record[-1, 1] / 1000),
               'preparation_final_density_g_cm3': float(merge_record[-1, 8])}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'molecule_summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    with (args.output / 'template_bonds.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['bond_type', 'atom1', 'atom2', 'template_length_A'])
        for kind, (i, j) in links['Bonds']:
            writer.writerow([kind, i, j, float(np.linalg.norm(coords[i] - coords[j]))])
    zh = args.language == 'zh'
    tr = lambda a, b: a if zh else b
    plt.rcParams.update({'font.family': ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC', 'WenQuanYi Zen Hei', 'DejaVu Sans'] if zh else 'DejaVu Sans',
        'font.size': 14, 'svg.fonttype': 'path', 'axes.spines.top': False, 'axes.spines.right': False,
        'figure.facecolor': '#f8f7f2', 'axes.facecolor': '#f8f7f2', 'savefig.facecolor': '#f8f7f2'})
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.5), constrained_layout=True)
    colors = {'H': '#94a7aa', 'C': '#254953', 'O': '#bd6541'}
    for _, (i, j) in links['Bonds']:
        pair = np.array([coords[i], coords[j]])
        axes[0].plot(pair[:, 0], pair[:, 1], color='#8d9b98', lw=1.4, zorder=1)
    for element in ('H', 'C', 'O'):
        positions = np.array([coords[i] for i in coords if ELEMENT[types[i]] == element])
        axes[0].scatter(positions[:, 0], positions[:, 1], s=35 if element == 'H' else 95,
                        color=colors[element], label=element, zorder=2)
    axes[0].set(xlabel='x / Å', ylabel='y / Å', aspect='equal',
                title=tr('模板坐标与真实键表：xy投影', 'Template coordinates and listed bonds\nxy projection'))
    axes[0].legend(frameon=False, ncol=3, loc='upper right')
    labels = list(peg['type_counts'])
    bars = axes[1].bar(labels, [peg['type_counts'][x] for x in labels], color='#167d84', width=.65)
    axes[1].bar_label(bars, padding=4)
    axes[1].set(ylabel=tr('原子数', 'Atom count'), ylim=(0, max(peg['type_counts'].values())*1.2),
                title=tr('同一个元素可以分成不同原子类型', 'One element can have\nseveral atom types'))
    fig.savefig(args.output/'template-inspection.svg');fig.savefig(args.output/'template-inspection.png', dpi=180);plt.close(fig)
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.9), constrained_layout=True)
    distance = np.linspace(.90, 1.12, 200)
    axes[0].plot(distance, 529.581*(distance-1.012)**2, color='#167d84')
    axes[0].set(xlabel='r / Å', ylabel='U / kcal mol⁻¹', title=tr('SPC/Fw氧—氢键项', 'SPC/Fw O–H bond term'))
    angle = np.linspace(95, 130, 200)
    axes[1].plot(angle, 37.95*np.deg2rad(angle-113.24)**2, color='#bd6541')
    axes[1].set(xlabel='θ / °', ylabel='U / kcal mol⁻¹', title=tr('SPC/Fw角项', 'SPC/Fw angle term'))
    phi = np.linspace(-180, 180, 361)
    axes[2].plot(phi, .3011*(1+np.cos(3*np.deg2rad(phi))), color='#466eaa')
    axes[2].set(xlabel='φ / °', ylabel='U / kcal mol⁻¹', title=tr('PEG g23扭转项', 'PEG g23 torsional term'))
    fig.savefig(args.output/'parameter-curves.svg');fig.savefig(args.output/'parameter-curves.png', dpi=180);plt.close(fig)
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True, constrained_layout=True)
    fields = [(2, tr('温度 / K', 'Temperature / K')), (8, tr('密度 / g cm⁻³', 'Density / g cm⁻³')),
              (7, tr('体积 / Å³', 'Volume / Å³'))]
    for ax, (column, label) in zip(axes, fields):
        ax.plot(water_record[:,1]/1000, water_record[:,column], color='#167d84', label=tr('纯水：各向同性NPT', 'Water: isotropic NPT'))
        ax.plot(merge_record[:,1]/1000, merge_record[:,column], color='#bd6541', label=tr('加入PEG：x方向NPT', 'Inserted PEG: x-only NPT'))
        ax.axvline(15, color='#687b80', ls=':', lw=1)
        ax.set_ylabel(label);ax.grid(axis='y',alpha=.2)
    axes[0].axhline(300,color='#687b80',ls='--',lw=1)
    axes[0].legend(frameon=False,fontsize=12,loc='best')
    axes[-1].set_xlabel(tr('从建水阶段起算的物理时间 / ps', 'Physical time from the water stage / ps'))
    fig.savefig(args.output/'preparation-records.svg');fig.savefig(args.output/'preparation-records.png', dpi=180);plt.close(fig)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
```

Run the command in the header; --language zh or en controls labels. Keep the inputs and records in the example directory.

The structure figure uses the template's actual coordinates and draws links from its bond table. Hydrogen atoms can be shown smaller to reveal the backbone while remaining fully included in counts and calculations. A category panel makes six PEG atom types visibly different from fifty-nine PEG atoms. Nearby points in a projection can still be far apart along the viewing direction, so geometric checks use all three coordinate components. The picture helps locate a feature, while numerical measurements establish its physical meaning. Reading both together is more informative than choosing between a purely visual inspection and an unreadable list of coordinates.

### The actual PEG template and parameter responses

Structure and counts come from peg.mol; parameter curves evaluate the analytic expressions used in this example. They describe the starting template and individual energy rules.

LAMMPS 30 Sep 2026 Update 1; the open PEG/SPC-Fw example by Gravelle and colleagues, at 300 K in real units. The original staged preparation and constant-force pulling protocol is retained with added numerical records.

[Download reference data and complete inputs (ZIP) 4.47 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-peg-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l05/en/#en-s7)

Actual xy projection of the 59 atoms and 58 covalent bonds in peg.mol, alongside counts by atom type. Types distinguish local chemical environments, so one element can have several types.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l05/en/#en-s7)

Analytic energy terms using the example parameters: SPC/Fw O–H bond and H–O–H angle, and the PEG g23 torsion. Angular arguments are converted to radians in the energy calculation; each panel isolates one term.

Parameter curves are calculated point by point from the actual bond and angle coefficients. They describe the response of a single term and can be traced directly to the input table. Starting bond lengths measured in a template may be close to their equilibrium parameters or displaced from them; other interactions and thermal motion subsequently affect their distributions. We therefore distinguish a parameter's preferred distance, a measured template distance, and a time-dependent trajectory distance. All three are lengths, but they belong to different levels of the description. Keeping them separate prevents a coordinate snapshot from being mistaken for a force-field definition.

The preparation results separately read the actual water-stage and merged-system records. Temperature, density, and volume are plotted against physical time in panels that retain each stage's conditions. The water-only count, the additional PEG atoms, and the waters removed during insertion can be reconciled with the resulting data file. A trajectory player then helps inspect molecular integrity, solvent surroundings, and the periodic display. Numerical summaries and animation have complementary roles: one fixes counts and definitions, while the other makes spatial organization and motion accessible. Their agreement connects composition, geometry, and dynamics within the same model.

### Recorded preparation of water and the inserted chain

Initially 700 waters; removing 30 overlapping whole waters leaves 670 waters and 59 PEG atoms. Isotropic NPT covers 0–15 ps and x-only NPT covers 15–25 ps.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l05/en/#en-s7)

Actual preparation records. Isotropic NPT with 700 waters covers 0–15 ps. After inserting PEG and removing 30 overlapping waters, x-only NPT covers 15–25 ps with 670 waters and 59 PEG atoms. The volume changes reflect these different cell-control conditions.

Construction initially placed 700 complete waters. Inserting PEG and removing 30 overlapping waters left 670 water molecules plus 59 PEG atoms, or 2069 atoms altogether. The 25 ps preparation endpoint has a mass density of 0.94018 g/cm³. Subsequent fixed-volume conformational observations inherit this specific starting state; evaluating equilibrium density at the target conditions calls for continuing the volume and density observations. These counts and stage conditions also identify the solvent environment associated with the chain dimensions examined in the seventh lesson.

### The short PEG chain in water

Actual 15–25 ps preparation after insertion. PEG and solvent are translated together in the simulation to centre the chain, preserving its internal conformation.

Try a short reasoning exercise. Changing a PEG atom's type to water oxygen can preserve atom count and connectivity while altering its mass or interactions. Renumbering that atom and consistently updating every reference can instead preserve the physical model. The contrast identifies different levels of checking. Byte identity and numbering describe file relationships; chemical identity, geometry, and parameters describe physical relationships. Understanding a molecular model means tracing how its fields enter the calculation, so that a modification can be explained by what it changes rather than merely by whether the edited file opens successfully.

## Turn a template into a research object with stated conditions

The PEG now has complementary descriptions. Its formula specifies composition, its graph defines connectivity, parameters determine forces, coordinates give a conformation, and solvent and run settings establish observation conditions. A later comparison should identify which description changes. Adding repeat units changes size and connectivity. Replacing an end group changes a local chemical environment and perhaps charge. Changing temperature changes thermal conditions, while applying force changes the driving. Separating those operations makes an observed difference traceable to a defined cause and keeps the molecular object recognizable throughout an increasingly complex study.

A useful beginner exercise follows one water hydrogen through the complete calculation. Find its ID, type, and charge, locate its bond to oxygen, find that bond's coefficient in parameters.inc, and calculate its energy at a chosen separation. Repeat the exercise for an ether oxygen in PEG. Only basic arithmetic and an understanding of the file relationships are needed, yet the exercise covers a central part of much larger models: every interaction should be traceable to specified information. The formulas become useful explanations of those records rather than an independent collection of symbols to memorize.

For a new material, formulate a measurable question before expanding the model. Hydration of a modified surface requires its chemical connections and charges together with a definition of water occupancy near it. Comparing chain flexibility requires consistent conditions and observations of internal rotations and overall size. Crosslinked elasticity additionally requires specifying which chain segments are connected. The model becomes a concrete expression of the question through atoms, connections, and environment. This approach helps choose relevant observations and shows which preparation and parameter checks support their interpretation.

The next lesson focuses on water and ions. Knowing where charges reside, how molecular connectivity constrains motion, and how coefficients enter energy expressions prepares us to distinguish water representations and understand local ionic environments. The seventh lesson then returns to this PEG to follow its shape and pulling response through actual trajectories. Defining molecular identity first gives each later movement an object whose composition, connections, and interactions can be explained.

## Further Reading and Open Materials

- [Polymer in water; A Set of Tutorials for the LAMMPS Simulation Package](https://lammpstutorials.github.io/sphinx/build/html/tutorial3/polymer-in-water.html) · Simon Gravelle; Cecilia M. S. Alvares; Jacob R. Gissinger; Axel Kohlmeyer · CC BY4.0

  PEG/SPC-Fw templates, parameters, and water/insertion workflow.

  Retains model and preparation stages; adds numeric records, bilingual explanations, template inspections, and figures.
- [Über Polymerisation](https://doi.org/10.1002/cber.19200530627) · Hermann Staudinger · Scientific citation; no reproduced figure

  Historical context for long covalent structures.

  Independent conceptual diagram of connectivity.
- [Flexible simple point-charge water model with improved liquid-state properties](https://doi.org/10.1063/1.2136877) · Yujie Wu; Harald L. Tepper; Gregory A. Voth · Scientific citation; no reproduced figure

  SPC/Fw and the physical role of geometry parameters.

  Explained through the supplied template.
- [Definition and testing of the GROMOS force-field versions 54A7 and 54B7](https://doi.org/10.1007/s00249-011-0700-9) · Nathan Schmid and colleagues · Scientific citation; no reproduced figure

  Background of the parent parameter family.

  Distinguishes the specific teaching combination from the parent family.
- [LAMMPS: molecule](https://docs.lammps.org/molecule.html) · LAMMPS developers · Technical reference

  Check input fields, potential forms, and interaction conventions.

  Independent explanations, worked examples, and diagrams.
- [LAMMPS: atom_style](https://docs.lammps.org/atom_style.html) · LAMMPS developers · Technical reference

  Check input fields, potential forms, and interaction conventions.

  Independent explanations, worked examples, and diagrams.
- [LAMMPS: bond_harmonic](https://docs.lammps.org/bond_harmonic.html) · LAMMPS developers · Technical reference

  Check input fields, potential forms, and interaction conventions.

  Independent explanations, worked examples, and diagrams.
- [LAMMPS: angle_harmonic](https://docs.lammps.org/angle_harmonic.html) · LAMMPS developers · Technical reference

  Check input fields, potential forms, and interaction conventions.

  Independent explanations, worked examples, and diagrams.
- [LAMMPS: dihedral_harmonic](https://docs.lammps.org/dihedral_harmonic.html) · LAMMPS developers · Technical reference

  Check input fields, potential forms, and interaction conventions.

  Independent explanations, worked examples, and diagrams.
- [LAMMPS: special_bonds](https://docs.lammps.org/special_bonds.html) · LAMMPS developers · Technical reference

  Check input fields, potential forms, and interaction conventions.

  Independent explanations, worked examples, and diagrams.
