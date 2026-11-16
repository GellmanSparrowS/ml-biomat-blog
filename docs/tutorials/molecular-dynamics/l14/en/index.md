# Rare Changes: Free Energy and Sampling

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l14/en/
Language: en

Start from gaps in direct sampling, reconstruct free energy with overlapping umbrella windows, and interpret sampling variation alongside molecular structure.

## How long must we wait for a rare change?

A drug molecule entering a membrane from water, an ion passing through a narrow channel and a polymer segment leaving a surface can all present the same difficulty: molecules keep moving, yet the particular change of interest scarcely occurs. Certain intermediate arrangements are rarely visited at the chosen temperature, so most of a trajectory is spent in more accessible regions. Playing the movie faster only changes viewing speed. More integration steps increase the observation time, but when the required waiting time greatly exceeds the available calculation, we need a strategy that deliberately samples the difficult regions.

Imagine surveying activity across a city by following one pedestrian who spends most of the day near home. The nearby streets become thoroughly documented, while distant districts remain barely observed. Molecular motion has no personal preferences, but statistical weights and barriers likewise produce uneven visits. Our target is the relative probability of positions under specified conditions, extending beyond the places thoroughly explored by one finite record. A free-energy profile expresses these probability differences on an energy scale. The analogy concerns uneven coverage; the molecular calculation supplies the actual thermodynamic weights and a way to correct deliberate changes in sampling.

We begin with a simple three-dimensional particle system. A repulsive external potential occupies the middle of the box, while particles retain short-range mutual repulsion. With a low external barrier, direct position sampling reaches the central region. Raising the barrier leaves gaps in a record of the same duration. We then add a controllable spring to one tagged particle and let it fluctuate near several positions, creating overlapping observation windows. Knowing how each spring changes the probabilities allows us to combine these records into a profile for the original system without that extra spring. Sampling difficulty becomes a problem with observable stages.

The central region is defined mathematically, making the sampling method easy to inspect. A membrane calculation would explicitly model lipids, water and the target molecule. Polymer desorption would require its multiple contacts, solvent and surface structure. Here the coordinate is the x position of one particle, with the other two directions free to fluctuate. Every step follows that coordinate: measuring it, restraining it and checking the surrounding sampling. This connection between a physical question and its selected coordinate provides the foundation for choosing variables in more complex systems, where many arrangements may share one reported position.

Two questions should be distinguished at the outset: how probable a position is, and how long movement between positions takes. A free-energy profile primarily addresses the first as a projection of equilibrium statistics. Motion times also depend on friction, diffusion and other changes along the pathway. Adding a spring deliberately alters the tagged particle’s dynamics, and a window trajectory measures the distribution under that restraint. An actual crossing-rate study can build on a well-sampled profile and add appropriate dynamical measurements, connecting thermodynamic preference and motion time to their respective observations.

Follow one continuous chain of ideas through the lesson: count visits, understand their relationship to free energy, improve coverage using a known additional interaction, and check whether the windows form a coherent statistical whole. The numerical solver comes after these physical relationships. Complete inputs, analysis and actual results appear together, supporting either a fresh run or inspection of the existing records. Pay particular attention to positions with no observations. Their location directs the next simulations and distinguishes measured information from the visual continuity that a plotting routine could otherwise supply.

## From visit counts to free energy: why a logarithm?

Divide the x axis into equal-width bins, like counting stations spaced uniformly along a road. Each saved position adds one count to its bin. Dividing a bin count by the total number of observations gives its probability; dividing again by bin width gives probability density. Probability is dimensionless, whereas density along x has inverse-length units. Halving the bin width generally reduces counts per bin without similarly changing the density of a smooth distribution. This distinction allows comparisons between plots with different binning and keeps a display choice separate from the material property being estimated.

Bin probability and probability densityEq. 1

![Bin probability and probability density](https://ml-biomat.com/static/agent-math/342ab69e242acd5019c6939f.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Hₖ | Visit count in bin k | 1 |
| N | Total number of observations | 1 |
| k, xₖ | Bin index and centre coordinate | 1, Å |
| Pₖ | Probability of that bin | 1 |
| p(xₖ) | Estimated probability density near the bin centre | Å⁻¹ |
| Δx | Common bin width | Å |
| =, ≈, /, Δ | Equality, approximation, division; Δ denotes interval width | 1 |

Reading the relationshipCount divided by total count gives a fraction; dividing by width makes density times width recover the bin probability.

A worked exampleFour of twenty records in a bin of width 0.5 Å give P=0.2 and p≈0.4 Å⁻¹.

ConditionsUse the same coordinate and observation conditions with equal-width bins; the density approximation depends on bin resolution.

Suppose sufficiently sampled equal-width intervals near position A occur ten times less often than those near position B under stable conditions. Statistical mechanics expresses that probability ratio exponentially in a free-energy difference, so inversion introduces a natural logarithm. The minus sign assigns higher free energy to the less probable position: a ratio below one has a negative logarithm, which becomes positive after multiplication by the minus sign. Temperature sets the conversion from a dimensionless logarithm to energy. We use molar energies and therefore RT; an energy expressed in joules per particle instead uses the Boltzmann constant times temperature.

Relative PMF from a probability ratioEq. 2

![Relative PMF from a probability ratio](https://ml-biomat.com/static/agent-math/e27a8ed8ae3ba1317078d846.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ΔA | Molar PMF difference relative to the reference | kcal mol⁻¹ |
| x, xᵣₑ𝒻 | Selected and reference positions | Å |
| p(x), p(xᵣₑ𝒻) | Probability densities with the same definition | Å⁻¹ |
| R | Gas constant, 0.00198720426 | kcal mol⁻¹ K⁻¹ |
| T | Absolute temperature | K |
| ln | Natural logarithm of a positive dimensionless ratio | 1 |
| =, −, /, ×, Δ | Equality, negation, division, multiplication and difference; RT is a product | 1 |

Reading the relationshipTaking the logarithm of the equilibrium exponential probability relation gives a free-energy difference; the minus sign assigns higher PMF to lower probability.

A worked exampleAt 119.8 K with density ratio 0.1, RT≈0.238067 kcal/mol and ΔA≈0.548170 kcal/mol.

ConditionsEquilibrium distribution along the same Cartesian coordinate at the same temperature and fixed N/V; both densities are positive and use consistent units.

At 119.8 K, RT is approximately 0.2381 kcal/mol. A tenfold probability difference gives about 0.5482 kcal/mol, while a hundredfold difference gives twice that value. One hundred is the product of two tens, and a logarithm turns multiplication into addition. Probability can therefore span many orders of magnitude while remaining readable on a free-energy axis. The ratio must compare quantities with the same definition and units. A density per ångström and a density per nanometre first require a common length unit before their numerical values are divided.

Free energy incorporates the degrees of freedom absent from the horizontal axis. At a selected x position, a particle can still move in y and z, and its neighbours have many possible arrangements. Those possibilities contribute to the statistical weight of x. A profile therefore generally differs from the potential energy of one configuration. Energy cost and the number of available arrangements jointly determine visitation. We calculate a potential of mean force, or PMF, along Cartesian x at fixed particle number and volume in a thermostatted environment. This identifies both the controlled conditions and the projected variable.

The coordinate also changes geometrical counting. Equal intervals on a line differ from spherical shells with equal radial thickness: shells farther from the centre have larger volume. A distribution of intermolecular distances therefore requires attention to shell volume and the intended reference. This lesson keeps Cartesian x and equal-width bins throughout. Likewise, comparing whole states requires summing probabilities over their defined regions before forming a ratio. The depth of one plotted minimum describes local coordinate density; the probability of an extended region includes both its depth and its width, with all configurations assigned to that region.

A free-energy zero is arbitrary because probability ratios determine only differences. Shifting the entire curve upward leaves every pairwise difference unchanged. Our analysis sets the mean profile over −26≤x<−22 Å to zero and measures the mean central plateau over −2≤x<2 Å relative to it. Chronological subsets and resampled profiles use the same reference rule. The reported plateau height is thus a difference between interval-averaged PMF values. A free-energy difference between the complete central and left states would instead be obtained by integrating probability over their regions.

## Direct observation: what remains empty after four nanoseconds?

The periodic box measures 100 by 30 by 100 Å and contains two hundred particles. Their mass is 39.948 g/mol, with repulsive length scale σ=3.405 Å and energy scale ε=0.238 kcal/mol. The pair interaction is WCA: Lennard-Jones truncated at its minimum and shifted there to retain the repulsive portion. These familiar atomic-scale parameters define a repulsive-particle model in the imposed external field. The temperature is 119.8 K, time step 2 fs and Langevin damping time 500 fs. A 100 ps preparation precedes a 4 ns production observation.

Two arctangent functions define the central external potential. An arctangent smoothly compresses a changing argument into a bounded range. Placing two such transitions near −10 and 10 Å and subtracting them creates a high middle plateau with lower outer regions. The parameter δ=1 Å sets the transition width, while U₀ controls the energy scale. The actual height also includes the difference between the arctangents, so U₀ itself is not the plateau height relative to the exterior. Evaluating the function at the positions of interest makes the input’s meaning concrete.

Central repulsive potential and its forceEq. 3

![Central repulsive potential and its force](https://ml-biomat.com/static/agent-math/b868d4bb7059d69e11b1cd36.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| U(x), U₀ | External potential and its energy-scale coefficient | kcal mol⁻¹ |
| Fₓ | Force along x from the potential, equal to −dU/dx | kcal mol⁻¹ Å⁻¹ |
| x | Particle x coordinate | Å |
| a | Transition-location parameter, 10 Å here | Å |
| δ | Transition width, 1 Å here | Å |
| arctan | Inverse tangent of a dimensionless argument, using radians | 1 |
| =, +, −, /, ², [, ], 1 | Equality, addition/subtraction, division, square, grouping and the constant one; adjacent quantities multiply | 1 |

Reading the relationshipSubtracting two smooth transitions creates a central plateau. The negative position derivative gives force, pointing opposite an increasing potential.

A worked exampleFor U₀=2.38 kcal/mol, a=10 Å and δ=1 Å, U(0)≈7.002568 kcal/mol and Fₓ(0)=0.

ConditionsThe external field applied to every particle here; its zero follows this function, and differences between intervals are evaluated separately.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l14/en/#en-s3)

Figure 2 · Pointwise evaluation of the two external potentials. Arrows show outward force near the edges; the full arctangent expression determines the central height.

The associated force is the negative position derivative of the potential. Near the comparatively flat central plateau the force is small; at the edges, where energy changes strongly, it pushes particles toward the lower outer regions. The complete input specifies both this force and its energy function. The low-barrier branch uses U₀=1.5ε and the high-barrier branch U₀=10ε, retaining particle number, cell and temperature. The result plots a profile reconstructed from observed occupancy alongside the analytically evaluated external potential, linking what was imposed with the distribution actually sampled by interacting particles.

### Complete low-barrier direct sampling

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

variable sigma equal 3.405
variable epsilon equal 0.238
variable U0 equal 1.5*${epsilon}
variable dlt equal 1.0
variable x0 equal 10.0

units real
atom_style atomic
pair_style lj/cut $(2^(1/6)*v_sigma)
pair_modify shift yes
boundary p p p

region myreg block -50 50 -15 15 -50 50
create_box 1 myreg
create_atoms 1 random 200 34134 myreg overlap 3 maxtry 50

mass * 39.948
pair_coeff * * ${epsilon} ${sigma}

variable U atom ${U0}*atan((x+${x0})/${dlt})-${U0}*atan((x-${x0})/${dlt})
variable F atom ${U0}/((x-${x0})^2/${dlt}^2+1)/${dlt}-${U0}/((x+${x0})^2/${dlt}^2+1)/${dlt}
fix myadf all addforce v_F 0.0 0.0 energy v_U

fix mynve all nve
fix mylgv all langevin 119.8 119.8 500 30917

region mymes block -${x0} ${x0} INF INF INF INF
variable n_center equal count(all,mymes)
thermo_style custom step temp etotal v_n_center
thermo 2000


timestep 2.0
run 50000
reset_timestep 0

thermo 20000
compute cTemp all temp
variable T equal c_cTemp
variable clock equal time
variable population equal count(all,mymes)
fix record all ave/time 1000 1 1000 v_clock v_T v_population file population.dat format " %.15g"
dump trajectory all custom 10000 trajectory.lammpstrj id type x y z vx vy vz ix iy iz
dump_modify trajectory sort id


compute cc1 all chunk/atom bin/1d x 0.0 2.0
fix myac all ave/chunk 100 20000 2000000 &
    cc1 density/number file free-sampling.dat

run 2000000

write_restart final.restart
write_data final.data
```

100 ps preparation and 4 ns production, saving spatial density and central population.

### Complete high-barrier direct sampling

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

variable sigma equal 3.405
variable epsilon equal 0.238
variable U0 equal 10*${epsilon}
variable dlt equal 1.0
variable x0 equal 10.0

units real
atom_style atomic
pair_style lj/cut $(2^(1/6)*v_sigma)
pair_modify shift yes
boundary p p p

region myreg block -50 50 -15 15 -50 50
create_box 1 myreg
create_atoms 1 random 200 34134 myreg overlap 3 maxtry 50

mass * 39.948
pair_coeff * * ${epsilon} ${sigma}

variable U atom ${U0}*atan((x+${x0})/${dlt})-${U0}*atan((x-${x0})/${dlt})
variable F atom ${U0}/((x-${x0})^2/${dlt}^2+1)/${dlt}-${U0}/((x+${x0})^2/${dlt}^2+1)/${dlt}
fix myadf all addforce v_F 0.0 0.0 energy v_U

fix mynve all nve
fix mylgv all langevin 119.8 119.8 500 30917

region mymes block -${x0} ${x0} INF INF INF INF
variable n_center equal count(all,mymes)
thermo_style custom step temp etotal v_n_center
thermo 2000


timestep 2.0
run 50000
reset_timestep 0

thermo 20000
compute cTemp all temp
variable T equal c_cTemp
variable clock equal time
variable population equal count(all,mymes)
fix record all ave/time 1000 1 1000 v_clock v_T v_population file population.dat format " %.15g"
dump trajectory all custom 10000 trajectory.lammpstrj id type x y z vx vy vz ix iy iz
dump_modify trajectory sort id


compute cc1 all chunk/atom bin/1d x 0.0 2.0
fix myac all ave/chunk 100 20000 2000000 &
    cc1 density/number file free-sampling.dat

run 2000000

write_restart final.restart
write_data final.data
```

Change the external-potential amplitude while retaining the observation definitions.

### Observed direct-sampling coverage

Four nanoseconds for each barrier. Upper markers/solid lines derive from measured density; dashed curves show the external potential. Lower curves show central population.

Open LAMMPS free-energy case: 200 LJ particles at 119.8 K under an x-dependent external potential. Low/high barriers sampled for 4 ns each; 15 original and 32 additional umbrella windows sampled for 400 ps each.

[Download reference data and complete inputs (ZIP) 1.04 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-free-energy-reference-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l14/en/#en-s3)

Native 4 ns direct sampling under low and high barriers, showing spatial density and central population.

In the low-barrier record, all x bins used for the density calculation receive visits, and the central region contains about 1.31 particles on average. The high-barrier record observes no particles in the central −10 to 10 Å region at the saved population times, with zero-density bin centres from −9 to 9 Å. Those observations provide no positive probability estimate there. The analysis leaves the corresponding profile blank because the logarithm of zero has no finite value. Adding an arbitrary small count would make the apparent height depend on that addition rather than the measured visits.

Four nanoseconds sounds brief but already contains two million integration steps. A calculation can perform many updates while scarcely visiting the process of interest. The particles also continue moving when the centre is unvisited: collisions, diffusion and temperature fluctuations persist in the outer regions. Movement of the system and coverage of the target coordinate are therefore separate observations. Displaying the spatial density together with the central-population time record makes this distinction visible and identifies where additional windows should concentrate their sampling effort.

Periodicity also determines what the two outer regions mean. A particle can cross a box boundary from one side to the other, so the low-potential regions connect around the periodic edge. The central high-potential region is the low-probability coordinate range studied here. The measured object is its occupancy profile, within this geometry. A membrane-translocation study would define the coordinate along the membrane normal while jointly specifying periodic repetitions, solution reservoirs and the intended pathway. Understanding the simple example’s geometry makes these later choices more explicit.

## Arranging observation windows around rare positions

Umbrella sampling adds a known potential that makes an otherwise rarely visited region easier to observe, then removes its statistical effect in analysis. Torrie and Valleau’s 1977 work discussed deliberately selected sampling distributions for free-energy estimation and tested the approach on Lennard-Jones systems. The practical idea is to sample a convenient distribution when the target distribution is difficult, provided their relationship can be calculated. Computational effort is thereby assigned to regions that need information, rather than requiring one freely evolving trajectory to explore every relevant position on its own.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l14/en/#en-s4)

Figure 1 · Umbrella sampling in 1977, biomolecular WHAM in 1992 and solution/error analysis in 2012 address reconstruction of target statistics from deliberately altered sampling.

We select one tagged particle and add a harmonic spring only along x. The spring has a centre c; its added energy grows with squared displacement, and its restoring force grows linearly with displacement. Changing c creates different windows. Within a window, the particle still fluctuates around a mean position while the other 199 particles continue moving. The observation is therefore a distribution rather than one fixed coordinate. Freezing the tagged particle at its centre would remove the positional fluctuations needed to measure the window’s width and overlap with neighbouring observations.

Umbrella spring, restoring force and flat-region widthEq. 4

![Umbrella spring, restoring force and flat-region width](https://ml-biomat.com/static/agent-math/ee38039566c7e968cbff208b.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Wᵢ | Added spring potential in window i | kcal mol⁻¹ |
| kᵢ | Spring coefficient of that window | kcal mol⁻¹ Å⁻² |
| x, cᵢ | Tagged-particle position and restraint centre | Å |
| Fᵢᵇⁱᵃˢ | Restoring force along x from the spring | kcal mol⁻¹ Å⁻¹ |
| s𝒻ₗₐₜ | Position standard deviation in a harmonic window on a flat original potential | Å |
| R, T | Gas constant and temperature | kcal mol⁻¹ K⁻¹, K |
| i, bias, flat | Window index and labels for bias and a flat original potential | 1 |
| =, 1/2, −, ², √, /, × | Equality, one-half, subtraction/negation, square, square root, division and multiplication | 1 |

Reading the relationshipThe negative derivative of harmonic energy gives a linear restoring force. On a flat original potential, its Boltzmann distribution is Gaussian with variance RT/k.

A worked exampleAt k=0.5 kcal/(mol Å²) and x−c=1 Å, W=0.25 kcal/mol and F=−0.5 kcal/(mol Å). At 119.8 K, sflat≈0.690025 Å.

ConditionsOnly x is restrained. The width expression assumes a flat original potential and a sufficiently wide domain; slopes and interactions alter actual distributions.

[Figure: External potential and biased Boltzmann position distribution](https://ml-biomat.com/tutorials/molecular-dynamics/l14/en/#en-s4)

One-dimensional Boltzmann quadrature at 119.8 K on −32 to 32 Å with a 0.05 Å grid, omitting pair interactions.

Change centre, spring strength or original potential to inspect the shift and width of a one-dimensional reference distribution, evaluated by Boltzmann quadrature with the shown field and spring.

The spring tether command uses one-half times k times squared displacement. Some software or potential styles absorb that one-half into their coefficient, so analysis must follow the actual command convention. NULL values for y and z exclude those directions from the spring distance and force; the final zero specifies zero equilibrium displacement. Numerical zeros in place of NULL would also restrain transverse position and change the sampling problem. This distinction matters for membrane passage and surface desorption, where lateral motion can contribute to the number of accessible molecular arrangements.

### Complete original fifteen-window input

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

variable sigma equal 3.405
variable epsilon equal 0.238
variable U0 equal 10*${epsilon}
variable dlt equal 1.0
variable x0 equal 10.0
variable k equal 0.5

units real
atom_style atomic
pair_style lj/cut $(2^(1/6)*v_sigma)
pair_modify shift yes
boundary p p p

region myreg block -50 50 -15 15 -50 50
create_box 2 myreg
create_atoms 2 single 0 0 0
create_atoms 1 random 199 34134 myreg overlap 3 maxtry 50

mass * 39.948
pair_coeff * * ${epsilon} ${sigma}
group topull type 2

variable U atom ${U0}*atan((x+${x0})/${dlt})-${U0}*atan((x-${x0})/${dlt})
variable F atom ${U0}/((x-${x0})^2/${dlt}^2+1)/${dlt}-${U0}/((x+${x0})^2/${dlt}^2+1)/${dlt}
fix myadf all addforce v_F 0.0 0.0 energy v_U

fix mynve all nve
fix mylgv all langevin 119.8 119.8 500 30917

thermo 5000


timestep 2.0
run 50000

dump trajectory all custom 5000 umbrella.lammpstrj id type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
variable a loop 15
label loop
variable xdes equal 4*${a}-32
variable xave equal xcm(topull,x)
fix mytth topull spring tether ${k} ${xdes} NULL NULL 0
run 20000

fix myat1 all ave/time 100 1 100 v_xave v_xdes file umbrella-sampling.${a}.dat format " %.15g"
run 200000
unfix myat1
write_data window-${a}.data
write_restart window-${a}.restart
next a
jump SELF loop
```

Restrain only tagged-particle x and save instantaneous position every 0.2 ps.

The original fifteen centres run from −28 to 28 Å at 4 Å spacing, with spring constant 0.5 kcal/(mol Å²). Each centre receives 40 ps of preparation and 400 ps of sampling, saving position every 0.2 ps. The ave/time setting takes one value per output, so these are instantaneous coordinates. Averaging many positions before histogramming would narrow the distribution: it would describe fluctuations of a time-averaged coordinate rather than the coordinate distribution required for this PMF. The recording settings thus determine the physical observable passed to analysis.

In a flat region, the harmonic distribution has standard deviation equal to the square root of RT/k. At this temperature and k=0.5, that estimate is about 0.690 Å. A spacing of 4 Å is therefore several distribution widths and may leave little shared sampling. This suggests a practical tradeoff: a stiffer spring holds the particle closer to the selected region but narrows its distribution, requiring closer centres. A softer spring broadens sampling but can allow the underlying potential slope to displace the particle substantially. Actual coordinate histograms reveal both effects.

The tagged particle responds jointly to the external potential, pair interactions and added spring. Its mean position consequently need not equal the restraint centre, particularly near a steep external slope. An evenly spaced list of input centres therefore does not itself establish evenly distributed coverage. We save actual means, widths and counts, then decide where additional windows are useful. The next figure supplies a concrete example: a centre near −8 Å produces a distribution whose particle spends most of its time substantially farther out.

## Windows need shared observations: using overlap to add sampling

Local maps need shared landmarks to form one larger map. Umbrella distributions similarly need shared coordinate regions to establish their relative statistical weights. A simple overlap measure first normalizes both histograms, takes the smaller probability in each bin, and sums these minima. Identical distributions give one; distributions with no common occupied bin give zero. The measure describes the shared part of the observed histograms, and it depends on bin width and sampling duration. It is useful for locating gaps, while the complete physical sampling still includes variables beyond the displayed coordinate.

Histogram overlap between two windowsEq. 5

![Histogram overlap between two windows](https://ml-biomat.com/static/agent-math/ff7836ba66a7699584caedd2.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Oᵢⱼ | Overlap between windows i and j, from zero to one | 1 |
| Hᵢₖ, Hⱼₖ | Counts in bin k for the two windows | 1 |
| Nᵢ, Nⱼ | Total record counts in the two windows | 1 |
| i, j, k | Window indices i/j and bin index k | 1 |
| Σ, min | Sum over bins; take the smaller normalized probability in each bin | 1 |
| =, /, (, ) | Equality, division and grouping | 1 |

Reading the relationshipThe probability shared within a bin is bounded by the smaller contribution; summing gives the total shared histogram mass.

A worked exampleFor distributions (0.6,0.4) and (0.3,0.7), overlap is 0.3+0.4=0.7.

ConditionsUse identical bins, nonnegative counts and positive totals; this measures coverage of the observed coordinate.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l14/en/#en-s5)

Figure 3 · Gaussian windows of equal width with 4 Å and 2 Å centre spacing. Closer centres increase the shared coordinate region.

### Coverage before and after added windows

Common 0.1 Å bins. The lower panel orders forty-seven windows by measured mean position; white points mark input centres.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l14/en/#en-s5)

Observed coverage of 15 original and 47 combined windows in common 0.1 Å bins; restraint centres and measured positions are shown separately.

The original fifteen histograms show several neighbouring regions that barely connect. Windows centred at −8 and 8 Å have observed means near −10.84 and 10.83 Å because the external slope and spring jointly determine their preferred positions. Placing an input centre on a slope does not ensure that the particle explores the intended region. Simply connecting window labels would conceal the missing statistical links. In the coverage map, each row displays one window and brightness marks its actual occupancy, making gaps easier to identify than from a table of prescribed centres alone.

The added simulations first place fourteen midpoints between the original centres, retaining k=0.5. Eighteen additional windows then cover the two slopes at 0.5 Å spacing with a stiffer coefficient of 2.0 kcal/(mol Å²). Their flat-potential width estimate is about 0.345 Å, accompanied by closer centre spacing. The two adjustments serve different purposes: midpoints connect sparsely covered regions, while stiffer springs improve control of positions on the slopes. The final set contains forty-seven windows, each with 400 ps of coordinate records and the same temperature and underlying particle interactions.

### Fourteen midpoint windows

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

variable sigma equal 3.405
variable epsilon equal 0.238
variable U0 equal 10*${epsilon}
variable dlt equal 1.0
variable x0 equal 10.0
variable k equal 0.5

units real
atom_style atomic
pair_style lj/cut $(2^(1/6)*v_sigma)
pair_modify shift yes
boundary p p p

region myreg block -50 50 -15 15 -50 50
create_box 2 myreg
create_atoms 2 single 0 0 0
create_atoms 1 random 199 34134 myreg overlap 3 maxtry 50

mass * 39.948
pair_coeff * * ${epsilon} ${sigma}
group topull type 2

variable U atom ${U0}*atan((x+${x0})/${dlt})-${U0}*atan((x-${x0})/${dlt})
variable F atom ${U0}/((x-${x0})^2/${dlt}^2+1)/${dlt}-${U0}/((x+${x0})^2/${dlt}^2+1)/${dlt}
fix myadf all addforce v_F 0.0 0.0 energy v_U

fix mynve all nve
fix mylgv all langevin 119.8 119.8 500 30918

thermo 5000


timestep 2.0
run 50000

dump trajectory all custom 5000 umbrella.lammpstrj id type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
variable a loop 14
label loop
variable xdes equal 4*${a}-30
variable xave equal xcm(topull,x)
fix mytth topull spring tether ${k} ${xdes} NULL NULL 0
run 20000

fix myat1 all ave/time 100 1 100 v_xave v_xdes file umbrella-sampling.${a}.dat format " %.15g"
run 200000
unfix myat1
write_data window-${a}.data
write_restart window-${a}.restart
next a
jump SELF loop
```

Add k=0.5 windows between the original centres.

### Eighteen dense slope windows

```
# LAMMPS Input File
# Licensed under CC BY 4.0
# A Set of Tutorials for the LAMMPS Simulation Package (LiveCoMS, 2025)
# By Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.33011/livecoms.6.1.3037
# Find more on GitHub: https://github.com/lammpstutorials

variable sigma equal 3.405
variable epsilon equal 0.238
variable U0 equal 10*${epsilon}
variable dlt equal 1.0
variable x0 equal 10.0
variable k equal 2.0

units real
atom_style atomic
pair_style lj/cut $(2^(1/6)*v_sigma)
pair_modify shift yes
boundary p p p

region myreg block -50 50 -15 15 -50 50
create_box 2 myreg
create_atoms 2 single 0 0 0
create_atoms 1 random 199 34134 myreg overlap 3 maxtry 50

mass * 39.948
pair_coeff * * ${epsilon} ${sigma}
group topull type 2

variable U atom ${U0}*atan((x+${x0})/${dlt})-${U0}*atan((x-${x0})/${dlt})
variable F atom ${U0}/((x-${x0})^2/${dlt}^2+1)/${dlt}-${U0}/((x+${x0})^2/${dlt}^2+1)/${dlt}
fix myadf all addforce v_F 0.0 0.0 energy v_U

fix mynve all nve
fix mylgv all langevin 119.8 119.8 500 30919

thermo 5000


timestep 2.0
run 50000

dump trajectory all custom 5000 umbrella.lammpstrj id type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
variable a index 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
variable centerlist index -11.0 -10.5 -10.0 -9.5 -9.0 -8.5 -8.0 -7.5 -7.0 7.0 7.5 8.0 8.5 9.0 9.5 10.0 10.5 11.0
label loop
variable xdes equal ${centerlist}
variable xave equal xcm(topull,x)
fix mytth topull spring tether ${k} ${xdes} NULL NULL 0
run 20000

fix myat1 all ave/time 100 1 100 v_xave v_xdes file umbrella-sampling.${a}.dat format " %.15g"
run 200000
unfix myat1
write_data window-${a}.data
write_restart window-${a}.restart
next a centerlist
jump SELF loop
```

Add k=2.0 windows at 0.5 Å spacing on both slopes.

The analysis uses 0.1 Å bins and orders windows by their measured mean positions. After supplementation, the smallest overlap between neighbouring distributions in that ordering is about 0.110, and the complete set is connected under the chosen overlap criterion. The original fifteen windows form several weakly connected parts. The new records establish continuous statistical contact along x, while the original plot explains where and why calculations were added. At another temperature or barrier shape, observed distributions should again guide centre spacing and spring strength, since the same input grid need not retain the same coverage.

Overlap in one dimension leaves another question: which other structures occur at the same x? A protein side chain may have alternative rotamers, water may organize differently, or a polymer may retain distinct contact patterns. Two windows can cover the same x interval while remaining in different hidden arrangements. Chronological comparisons and surrounding-particle motion help inspect the present simple model. Complex biomolecular studies can add structural observables, alternative initial conformations or preparations from opposite directions, providing observations of environmental adjustment as well as coverage of the selected coordinate.

Each added window retains its own identity. Centre, spring coefficient, temperature, preparation duration and recording interval define its observation distribution. Missing one can lead to incorrect combination weights. The complete analysis checks recorded centre columns against the parameter table and verifies the step spacing of saved coordinates. Folder names organize files, while calculations rely on explicit parameters. A changed spring coefficient requires matching updates to both simulation input and analysis metadata. Renaming a folder alone changes neither the applied force nor the physical information available to the reconstruction.

## Removing the spring’s statistical effect

Within one window, the original positional probability is multiplied by the spring’s exponential weight and then normalized. Positions with larger spring penalties become less common in that window. Recovering their original relative probability requires reversing that known penalty. For two positions within one window, the unknown normalization cancels, yielding a direct correction of the probability ratio. This explains the need to retain k, the centre and the one-half convention accurately. They enter an exponential, so a relatively modest energy-definition error can produce a substantial error in statistical weighting.

Recovering the original probability ratio within one windowEq. 6

![Recovering the original probability ratio within one window](https://ml-biomat.com/static/agent-math/90f92608a84692880bd989c1.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| p(x), p(y) | Original-system probability densities without the added spring | Å⁻¹ |
| pᵢ(x), pᵢ(y) | Biased densities in window i | Å⁻¹ |
| x, y | Two values of the same one-dimensional coordinate; y here labels the second value | Å |
| Wᵢ(x), Wᵢ(y) | Added spring energies at those values | kcal mol⁻¹ |
| β | Inverse molar thermal energy | mol kcal⁻¹ |
| R, T | Gas constant and temperature | kcal mol⁻¹ K⁻¹, K |
| exp | Exponential function of a dimensionless argument | 1 |
| =, /, −, ×, [, ], 1 | Equality, division, subtraction, multiplication, grouping and the constant one | 1 |

Reading the relationshipThe biased density is proportional to the original density times exp(−βW). Taking a within-window ratio cancels its normalizer and yields the correction.

A worked exampleA biased ratio exp(−1) and bias-energy difference RT give original ratio exp(−1)×exp(1)=1.

ConditionsCompare densities from the same window, temperature and coordinate; both positions are sampled and the bias is defined through that coordinate.

Different windows have different normalization constants, which shared sampling helps determine. The weighted histogram analysis method, WHAM, combines all windows through coupled self-consistency relations. Combined counts and known biases estimate the original probability, while that probability in turn determines each window’s normalization. Satisfying both requirements gives a consistent reconstruction. The local-map analogy now concerns jointly aligning the information shared between views. Mathematically, the quantities being adjusted are probability normalizers constrained by measured counts and known potentials, rather than arbitrary shifts applied to experimental curves.

WHAM self-consistency for probabilities and window normalizersEq. 7

![WHAM self-consistency for probabilities and window normalizers](https://ml-biomat.com/static/agent-math/425dba864c798cd4b67cd857.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Pₖ | Unbiased probability in bin k | 1 |
| Hᵢₖ, Nᵢ | Window-i bin count and total count | 1 |
| i, k, xₖ | Window index, bin index and bin centre | 1, 1, Å |
| fᵢ | Dimensionless normalization parameter for window i | 1 |
| Wᵢ(xₖ) | Window-i bias energy at the bin centre | kcal mol⁻¹ |
| β | 1/(RT), inverse molar thermal energy | mol kcal⁻¹ |
| Σᵢ, Σₖ | Sums over windows and bins | 1 |
| exp, ln | Exponential and natural logarithm, with dimensionless arguments | 1 |
| =, /, −, ×, [, ], 1 | Equality, division, subtraction/negation, multiplication, grouping and one | 1 |

Reading the relationshipCombine counts while accounting for known biases, and recompute window normalizers from the recovered probabilities. Both relations connect the distributions consistently.

A worked exampleFor two unbiased windows of 50 records each, with 10 and 30 counts in one bin, fᵢ=0 and Pₖ=40/100=0.4.

ConditionsCounts-based WHAM for one underlying system at one temperature with equal-width bins and connected coverage. Bias is evaluated at bin centres; correlation is assessed separately through time blocks.

In 1992, Kumar, Rosenberg, Bouzida, Swendsen and Kollman formulated weighted-histogram relations for complex biomolecular Hamiltonians and demonstrated a PMF for the sugar-ring pseudorotation phase angle in deoxyadenosine. A sugar ring can change its puckering through coordinated out-of-plane atomic displacements. An angular variable summarizes that collective rearrangement, projecting many coordinates into one sampling coordinate. This historical application connects the tagged-particle position used here with internal conformational questions in biomolecules, while preserving the common requirements of known bias potentials, overlapping observations and a clearly defined coordinate.

In the equations, Pₖ is the probability of equal-width bin k and sums to one. Hᵢₖ counts visits from window i, Nᵢ is that window’s total number of records, Wᵢ is its known spring energy, β is the reciprocal of RT, and fᵢ is a dimensionless normalization parameter. Every exponential therefore has a dimensionless argument. The program determines these parameters, converts probabilities to the PMF and sets the specified reference zero. Relating each quantity to its data column matters more than memorizing a solver name, because numerical optimization cannot repair incorrect coefficients or coordinate units.

Direct iteration is one solution method; an equivalent likelihood-optimization formulation provides another. Zhu and Hummer’s 2012 work discussed efficient optimization together with statistical errors and sampling of hidden degrees of freedom. The complete program here uses a damped Newton method and then substitutes its result back into the self-consistency relations. The forty-seven-window calculation took twelve iterations, with normalized probabilities summing to approximately one and a residual near 1.5×10⁻¹². That residual measures numerical solution accuracy. The amount and quality of trajectory sampling require their own observations, independently of how precisely the equations are solved.

### Complete WHAM and sampling analysis

```
"""Reconstruct the Cartesian-x PMF from instantaneous umbrella coordinates.

Usage: python analyze_wham.py records --output figures --language en
Use --refined other_records when the 32 added windows live in another folder.
Requires NumPy and Matplotlib. Energies are kcal/mol; positions are Angstrom.
The binned WHAM likelihood follows Zhu & Hummer, JCC 33, 453 (2012),
doi:10.1002/jcc.21989. This implementation uses a damped Newton solve.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

R = 0.00198720425864083
TEMPERATURE = 119.8
RT = R * TEMPERATURE


def logsumexp(a, axis=0):
    top = np.max(a, axis=axis, keepdims=True)
    return np.squeeze(top + np.log(np.sum(np.exp(a-top), axis=axis,
                                         keepdims=True)), axis=axis)


def wham(hist, centers, springs, x, initial=None):
    """Solve counts-based WHAM; f_i are dimensionless log normalizers."""
    total = hist.sum(axis=0)
    keep = total > 0
    count = total[keep]
    n = hist.sum(axis=1)
    if np.any(n == 0):
        raise ValueError("An umbrella window has no samples in the histogram.")
    bias = 0.5 * springs[:, None] * (x[None, keep]-centers[:, None])**2 / RT
    base = np.log(n)[:, None] - bias
    f = np.zeros(len(n)) if initial is None else initial.copy()
    f -= f[0]

    def objective(v, derivatives=False):
        logits = base + v[:, None]
        denominator = logsumexp(logits)
        value = count @ denominator - n @ v
        if not derivatives:
            return value
        membership = np.exp(logits-denominator)
        weighted = membership * count
        expected = weighted.sum(axis=1)
        grad = expected-n
        hess = np.diag(expected) - weighted @ membership.T
        return value, grad, hess, denominator

    for iteration in range(300):
        value, grad, hess, denominator = objective(f, True)
        residual = np.max(np.abs(grad)/n)
        if residual < 2e-10:
            break
        # Fix the additive gauge by holding f[0] at zero.
        step = np.linalg.solve(hess[1:, 1:], -grad[1:])
        if np.max(np.abs(step)) > 20:
            step *= 20 / np.max(np.abs(step))
        slope = grad[1:] @ step
        scale = 1.0
        while scale > 2**-30:
            candidate = f.copy()
            candidate[1:] += scale*step
            # A tiny allowance avoids stagnation at machine-precision objective.
            if objective(candidate) <= value + 1e-4*scale*slope + 1e-9:
                f = candidate
                break
            scale *= 0.5
        else:
            raise RuntimeError("WHAM line search failed.")
    else:
        raise RuntimeError("WHAM failed the gradient convergence criterion.")
    probability = np.zeros(len(x))
    logp = np.log(count)-denominator
    logp -= logsumexp(logp)
    probability[keep] = np.exp(logp)
    new_f = -logsumexp(logp[None, :] - bias, axis=1)
    new_f -= new_f[0]
    fixed_point_error = float(np.max(np.abs(new_f-f)))
    if fixed_point_error > 1e-7:
        raise RuntimeError("WHAM self-consistency check failed.")
    pmf = np.full(len(x), np.nan)
    pmf[keep] = -RT*np.log(probability[keep])
    # All curves share the same left reference interval, not their noisy minima.
    reference = (x >= -26) & (x < -22)
    pmf -= np.nanmean(pmf[reference])
    return pmf, f, dict(iterations=iteration+1,
                        relative_gradient=float(residual),
                        fixed_point_error=fixed_point_error,
                        probability_sum=float(probability.sum()))


def correlation_factor(values):
    """Initial-positive ACF estimate in saved-frame units; diagnostic only."""
    y = values-values.mean()
    size = 1 << (2*len(y)-1).bit_length()
    spectrum = np.fft.rfft(y, n=size)
    acf = np.fft.irfft(spectrum*spectrum.conjugate(), n=size)[:len(y)]
    acf /= np.arange(len(y), 0, -1)
    acf /= acf[0]
    stop = np.flatnonzero(acf[1:] <= 0)
    end = int(stop[0]+1) if len(stop) else min(500, len(y)//4)
    return float(max(1.0, 1+2*acf[1:end].sum()))


def overlap_matrix(hist):
    normalized = hist / hist.sum(axis=1, keepdims=True)
    return np.minimum(normalized[:, None, :], normalized[None, :, :]).sum(axis=2)


def component_sizes(overlap, threshold=0.005):
    remaining = set(range(len(overlap)))
    sizes = []
    while remaining:
        todo = [remaining.pop()]
        size = 0
        while todo:
            i = todo.pop()
            size += 1
            neighbors = remaining.intersection(np.flatnonzero(overlap[i] > threshold))
            todo.extend(neighbors)
            remaining.difference_update(neighbors)
        sizes.append(size)
    return sorted(sizes, reverse=True)


def load_windows(baseline, refined):
    windows = []
    grids = [(baseline/'umbrella-original-grid', np.arange(-28, 29, 4), 0.5),
             (refined/'midpoints', np.arange(-26, 27, 4), 0.5),
             (refined/'steep-regions',
              np.r_[np.arange(-11, -6.99, 0.5), np.arange(7, 11.01, 0.5)], 2.0)]
    for folder, centers, spring in grids:
        for number, center in enumerate(centers, 1):
            data = np.loadtxt(folder/f'umbrella-sampling.{number}.dat')
            if not np.allclose(data[:, 2], center):
                raise ValueError("Recorded center differs from its metadata.")
            if not np.all(np.diff(data[:, 0]) == 100):
                raise ValueError("Expected instantaneous coordinates every 200 fs.")
            windows.append(dict(center=float(center), spring=spring,
                                values=data[:, 1], stage=folder.name))
    return windows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('records', type=Path)
    parser.add_argument('--refined', type=Path)
    parser.add_argument('--output', type=Path, default=Path('figures'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    parser.add_argument('--bootstrap', type=int, default=80)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    zh = args.language == 'zh'
    def tr(a, b): return a if zh else b
    installed = {f.name for f in font_manager.fontManager.ttflist}
    fonts = ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC',
             'WenQuanYi Zen Hei', 'DejaVu Sans']
    plt.rcParams.update({'font.family': [f for f in fonts if f in installed],
                         'font.size': 13, 'axes.titlesize': 15,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'svg.fonttype': 'path', 'axes.unicode_minus': False,
                         'figure.facecolor': '#fbfaf6', 'axes.facecolor': '#fbfaf6'})
    windows = load_windows(args.records, args.refined or args.records)
    xdata = [w['values'] for w in windows]
    centers = np.array([w['center'] for w in windows])
    springs = np.array([w['spring'] for w in windows])
    edges = np.linspace(-32, 32, 641)
    x = (edges[1:]+edges[:-1])/2
    hist = np.array([np.histogram(v, edges)[0] for v in xdata])
    if not np.array_equal(hist.sum(axis=1), [len(v) for v in xdata]):
        raise ValueError("Extend the histogram range to include every sample.")
    overlap = overlap_matrix(hist)
    original = np.arange(15)
    if component_sizes(overlap) != [47]:
        raise ValueError("The umbrella overlap graph is disconnected.")
    pmf, solution, solver = wham(hist, centers, springs, x)
    halves = []
    for part in range(2):
        hh = np.array([np.histogram(np.array_split(v, 2)[part], edges)[0]
                       for v in xdata])
        halves.append(wham(hh, centers, springs, x, solution)[0])
    quarters = []
    for part in range(4):
        hh = np.array([np.histogram(np.array_split(v, 4)[part], edges)[0]
                       for v in xdata])
        quarters.append(wham(hh, centers, springs, x, solution)[0])
    # Resample contiguous 20 ps blocks independently within each window.
    # 2000 points form 20 blocks of 100 saved frames; the final point is omitted
    # only in the bootstrap so all blocks have the same duration and weight.
    rng = np.random.default_rng(14027)
    blocks = [np.array([np.histogram(v[j:j+100], edges)[0]
                        for j in range(0, 2000, 100)]) for v in xdata]
    bootstrap = []
    for repeat in range(args.bootstrap):
        sampled = np.array([b[rng.integers(0, 20, 20)].sum(axis=0) for b in blocks])
        if component_sizes(overlap_matrix(sampled)) != [47]:
            raise ValueError("A block resample has disconnected sampling support.")
        bootstrap.append(wham(sampled, centers, springs, x, solution)[0])
    boot = np.array(bootstrap)
    # The displayed coordinate interval is covered by every resampled profile.
    display = (x >= -28) & (x <= 28)
    if not np.isfinite(boot[:, display]).all():
        raise ValueError("A displayed PMF bin is empty in a block resample.")
    lower, upper = np.full(len(x), np.nan), np.full(len(x), np.nan)
    lower[display], upper[display] = np.percentile(boot[:, display], [2.5, 97.5], axis=0)
    g = np.array([correlation_factor(v) for v in xdata])
    plateau = (x >= -2) & (x < 2)
    barrier = float(np.nanmean(pmf[plateau]))
    barrier_boot = np.mean(boot[:, plateau], axis=1)
    mean_x = np.array([v.mean() for v in xdata])
    ordered = np.argsort(mean_x)
    adjacent = overlap[ordered[:-1], ordered[1:]]
    def save(fig, name):
        fig.savefig(args.output/f'{name}-{args.language}.svg', bbox_inches='tight')
        fig.savefig(args.output/f'{name}-{args.language}.png', dpi=150, bbox_inches='tight')
        plt.close(fig)

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), layout='constrained')
    density_summary = {}
    for stage, color, label, scale in [('free-low', '#167d84', tr('低势垒', 'Low barrier'), 1.5),
                                       ('free-high', '#c16b3d', tr('高势垒', 'High barrier'), 10)]:
        rows = np.loadtxt(args.records/stage/'free-sampling.dat', skiprows=4)
        position, density = rows[:, 1], rows[:, 3]
        ref = density[(position >= -46) & (position <= -34)].mean()
        measured = np.full(len(position), np.nan)
        valid = density > 0
        measured[valid] = -RT*np.log(density[valid]/ref)
        axes[0].plot(position, measured, 'o-', ms=4, color=color, label=label)
        u = scale*0.238*(np.arctan(position+10)-np.arctan(position-10))
        u -= u[(position >= -46) & (position <= -34)].mean()
        axes[0].plot(position, u, '--', color=color, alpha=0.65)
        population = np.loadtxt(args.records/stage/'population.dat')
        axes[1].plot(population[:, 1]/1e6, population[:, 3], color=color,
                     alpha=0.8, linewidth=1, label=label)
        density_summary[stage] = {'zero_density_bin_centers_A': position[~valid].tolist(),
                                  'mean_center_population': float(population[:, 3].mean()),
                                  'density_integral_particles': float((density*6000).sum())}
    axes[0].set(xlabel=tr('位置 x / Å', 'Position x / Å'),
                ylabel=tr('相对自由能 / kcal mol⁻¹', 'Relative free energy / kcal mol⁻¹'),
                title=tr('4 ns 无偏采样：实线来自占据概率，虚线是外势',
                         '4 ns unbiased sampling: probability profiles and external potentials'))
    axes[0].legend(frameon=False)
    axes[1].set(xlabel=tr('生产阶段时间 / ns', 'Production time / ns'),
                ylabel=tr('中央区粒子数', 'Particles in central region'),
                title=tr('中央区：−10 Å < x < 10 Å', 'Central region: −10 Å < x < 10 Å'))
    axes[1].legend(frameon=False)
    save(fig, 'free-sampling-limit')

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), layout='constrained')
    for i in original:
        axes[0].plot(x, hist[i]/hist[i].sum()/0.1, lw=1.3)
    axes[0].set(xlim=(-32, 32), ylabel=tr('概率密度 / Å⁻¹', 'Probability density / Å⁻¹'),
                title=tr('原来的 15 个窗口：势垒斜坡附近出现覆盖缺口',
                         'Original 15 windows: coverage gaps around the barrier slopes'))
    image = axes[1].imshow(hist[ordered]/hist[ordered].sum(axis=1)[:, None]/0.1,
                           origin='lower', aspect='auto', extent=(-32, 32, -0.5, 46.5),
                           cmap='viridis', vmin=0, vmax=1.4)
    axes[1].plot(centers[ordered], np.arange(47), 'w.', ms=3,
                 label=tr('约束中心', 'Restraint centers'))
    axes[1].set(xlabel=tr('位置 x / Å', 'Position x / Å'),
                ylabel=tr('按平均位置排列的窗口', 'Windows ordered by mean position'),
                title=tr('补充到 47 个窗口后的真实覆盖', 'Observed coverage with 47 windows'))
    axes[1].legend(frameon=True, loc='upper left', facecolor='#263d4d', labelcolor='white')
    fig.colorbar(image, ax=axes[1], label=tr('概率密度 / Å⁻¹', 'Probability density / Å⁻¹'))
    save(fig, 'umbrella-coverage')

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), layout='constrained')
    external = 2.38*(np.arctan(x+10)-np.arctan(x-10))
    external -= external[(x >= -26) & (x < -22)].mean()
    axes[0].fill_between(x[display], lower[display], upper[display], color='#167d84', alpha=0.22,
                         label=tr('20 ps 分块重采样 95% 区间', '95% interval from 20 ps block resampling'))
    axes[0].plot(x[display], pmf[display], color='#167d84', label=tr('47 窗口 WHAM', '47-window WHAM'))
    axes[0].plot(x[display], external[display], '--', color='#c16b3d',
                 label=tr('外势：稀薄极限的参照', 'External potential: dilute-limit reference'))
    for i, half in enumerate(halves):
        axes[1].plot(x[display], half[display], label=tr(f'每窗第 {i+1} 个 200 ps',
                                                       f'{"First" if i == 0 else "Second"} 200 ps in each window'))
    for ax in axes:
        ax.set(xlabel=tr('位置 x / Å', 'Position x / Å'),
               ylabel=tr('PMF / kcal mol⁻¹', 'PMF / kcal mol⁻¹'))
        ax.legend(frameon=False, fontsize=12)
    axes[0].set_title(tr('相对于左侧 −26 至 −22 Å 区间的自由能',
                         'Free energy relative to the left interval, −26 to −22 Å'))
    axes[1].set_title(tr('时间分段：分别重建两段记录的轮廓',
                         'Chronological split: two separately reconstructed profiles'))
    save(fig, 'umbrella-pmf')

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8), layout='constrained')
    for spring, color in [(0.5, '#163840'), (2.0, '#c16b3d')]:
        selected = springs == spring
        axes[0].scatter(mean_x[selected], g[selected], color=color, s=35,
                        label=f'k = {spring:g} kcal mol⁻¹ Å⁻²')
    axes[0].legend(frameon=False, fontsize=11)
    axes[0].set(xlabel=tr('窗口平均位置 / Å', 'Window mean position / Å'),
                ylabel=tr('初始正值相关因子 g', 'Initial-positive correlation factor g'),
                title=tr('相邻 0.2 ps 记录的相关性', 'Correlation between 0.2 ps records'))
    axes[1].hist(barrier_boot, bins=15, color='#167d84', alpha=0.8)
    axes[1].axvline(barrier, color='#c16b3d', lw=2,
                    label=tr('全记录结果', 'Full-record estimate'))
    axes[1].set(xlabel=tr('中央平台与左侧之差 / kcal mol⁻¹',
                         'Central plateau minus left reference / kcal mol⁻¹'),
                ylabel=tr('重采样次数', 'Resample count'),
                title=tr(f'{args.bootstrap} 次连续分块重采样',
                         f'{args.bootstrap} contiguous-block resamples'))
    axes[1].legend(frameon=False)
    save(fig, 'umbrella-statistics')
    summary = {'temperature_K': TEMPERATURE, 'RT_kcalmol': RT,
               'window_count': len(windows), 'samples_per_window': [len(v) for v in xdata],
               'bin_width_A': 0.1, 'solver': solver,
               'original_overlap_components': component_sizes(overlap[np.ix_(original, original)]),
               'refined_overlap_components': component_sizes(overlap),
               'minimum_adjacent_overlap_by_sample_mean': float(adjacent.min()),
               'central_plateau_minus_left_kcalmol': barrier,
               'block_bootstrap': {'samples': args.bootstrap, 'seed': 14027,
                                   'block_ps': 20, 'blocks_per_window': 20,
                                   'interval_percentiles': [2.5, 97.5],
                                   'plateau_interval_kcalmol': np.percentile(barrier_boot, [2.5, 97.5]).tolist(),
                                   'conditional_scope': 'Resampling recorded 20 ps segments within each window; fixed model, windows and initial trajectories.'},
               'half_plateaus_kcalmol': [float(np.mean(h[plateau])) for h in halves],
               'quarter_plateaus_kcalmol': [float(np.mean(h[plateau])) for h in quarters],
               'correlation_factor_range': [float(g.min()), float(g.max())],
               'external_reference_plateau_kcalmol': float(external[plateau].mean()),
               'unbiased': density_summary,
               'window_statistics': [{'center_A': w['center'], 'spring_kcalmolA2': w['spring'],
                                      'mean_A': float(v.mean()), 'sd_A': float(v.std(ddof=1)),
                                      'correlation_factor': float(g[i])}
                                     for i, (w, v) in enumerate(zip(windows, xdata))]}
    (args.output/'wham_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf8')
    np.savetxt(args.output/'pmf.csv', np.c_[x, pmf, lower, upper, external, *halves],
               delimiter=',', header='x_A,pmf_kcalmol,lower_2p5,upper_97p5,external,first_half,second_half', comments='')
    np.savetxt(args.output/'window_overlap.csv', overlap, delimiter=',')
    print(json.dumps({k: summary[k] for k in ['window_count', 'solver',
                                            'central_plateau_minus_left_kcalmol', 'block_bootstrap']}))


if __name__ == '__main__':
    main()
```

Check windows, overlap and self-consistency, compute chronological profiles and contiguous-block resamples, and export four panels.

The reconstructed central plateau is about 6.8321 kcal/mol above the left reference interval. The external-potential function, evaluated over the same intervals with the same zero, gives about 6.8954 kcal/mol. Their proximity is consistent with the strong role of the external field in this relatively dilute system; pair repulsion, finite sampling and binning also enter the measured profile. Both curves are calculated separately. For biomaterials with more complex environmental rearrangement and conformational multiplicity, this comparison helps explain why a potential of mean force is obtained from statistical sampling rather than one imposed potential alone.

### Reconstructed PMF and chronological subsets

The mean over −26 to −22 Å sets the zero. Shading gives pointwise 95% percentiles from 20 ps blocks of the recorded trajectories; the lower panel uses the first and second 200 ps separately.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l14/en/#en-s6)

Profiles share a zero defined by the same left-hand interval. Eighty resamples of contiguous 20 ps blocks and separate reconstructions of the first/second 200 ps are shown.

## What remains to check after obtaining a smooth profile?

Each window contains 2,001 position records, yet positions separated by 0.2 ps are usually related because motion is continuous. Photographing a particle again before it explores a new neighbourhood does not provide a wholly independent configuration. More frequent output resolves motion better without necessarily increasing independent information in proportion. The analysis reports an initial-positive positional autocorrelation estimate, with factors around 1.9 to 7.5 in these windows. This diagnoses correlations in the saved coordinate. PMF sampling variability is then assessed by resampling contiguous pieces of trajectory, retaining short-time structure within each piece.

First divide each window chronologically into two approximately 200 ps portions and reconstruct the complete profile from each. Their plateau differences are about 6.8498 and 6.8137 kcal/mol using the same left reference. Four chronological portions give approximately 6.9905, 6.7411, 6.8329 and 6.7947 kcal/mol. These values expose time variation: shorter subsets fluctuate more and may reveal persistent drift. Chronological comparison preserves the order within every window, allowing early and late observations to be examined together instead of relying solely on a profile produced after all records have been pooled.

A complementary check divides the first 2,000 records of each window into twenty contiguous blocks of one hundred records, corresponding to 20 ps per block. A resample draws twenty blocks with replacement from that window’s own set and combines their counts. This is done separately for all forty-seven windows before solving WHAM again. Some blocks appear twice and others are absent, representing variability within the finite observed collection. The extra final record is omitted only for equal-length resampling; the full profile still uses all 2,001 records from every window.

### Correlation and variability of the plateau difference

Left: positional-correlation diagnostic. Right: plateau differences from eighty contiguous-block resamples of records with the same model and window arrangement.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l14/en/#en-s7)

Positional-correlation diagnostics and the block-resampled plateau difference for the same model, windows and recorded time series.

Eighty contiguous-block resamples give central-plateau percentiles of approximately 6.7131 and 6.9990 kcal/mol at 2.5% and 97.5%. The plotted band uses corresponding percentiles at each coordinate. It describes finite-sampling variation conditional on this model, window arrangement and recorded trajectories. Changing the force field, temperature or initially occupied hidden conformations introduces further variation that calls for its own comparisons. A study can add independently initialized window runs and compare block lengths, checking the stability of these intervals. The 20 ps choice should likewise be reconsidered when the important motions become slower.

The level of replication matters. Eighty resampled curves come from one original collection of records; they are not eighty complete simulations initialized in different environments. Resampling uses existing temporal pieces to characterize a form of variability, while new initial structures require new trajectories. Difficult biomolecular studies can prepare windows from association and separation directions or from distinct side-chain states, retaining those runs as independent replicates. Chronological analysis within each replicate and comparisons between replicates then separate local temporal correlation from the effects of alternative initial structures.

Computational effort can then follow the diagnosis. Missing shared visits call for added centres or adjusted springs. Continuous coverage with a slowly drifting window calls for longer preparation or alternative initial states. Stable windows with a broad plateau interval call for more effective observation time in the contributing regions. Each added calculation addresses an identifiable issue. Presenting coverage, chronological profiles and resampling together allows the next step to follow those observations, rather than treating a visually smooth final curve as the sole measure of a completed calculation.

## Turning the example into a biomaterials pathway study

The complete run script generates low-barrier sampling, high-barrier sampling, the original fifteen umbrellas, added midpoints and dense slope windows in separate directories. One analysis program reads the resulting records. Retain the original coordinate files together with the final PMF, since centre checks, histogram overlap and chronological subsets all depend on them. A changed temperature requires a matching RT in analysis. Changing unit systems requires consistent transformations of length, spring coefficient and energy. Following a plotted quantity back through its records and physical input is the organizing structure of the complete exercise.

### Run all sampling stages and analyse

```
#!/usr/bin/env bash
set -euo pipefail
lmp=${LAMMPS:-lmp}
export OMP_NUM_THREADS=1
for stage in free-low free-high umbrella-original-grid midpoints steep-regions; do
  mkdir -p "$stage"
  cp "$stage.lmp" "$stage/input.lmp"
  ( cd "$stage"; "$lmp" -in input.lmp -log simulation.log > stdout.log 2>&1 )
done
python analyze_wham.py . --output figures --language en
python analyze_wham.py . --output figures --language zh
```

Each of five sampling stages has its own directory; the final commands generate both plot languages.

Replacing the tagged particle with a drug molecule suggests its centre-of-mass position along a membrane normal as an initial candidate coordinate. Molecular orientation, hydrogen bonding and local membrane structure must also adjust within each window. Water can leave the molecule’s neighbourhood as it enters the membrane, and nearby lipids can rearrange; these environmental changes contribute to the PMF. A lower portion of the profile can involve favourable interactions and the multiplicity of accessible arrangements. Recording hydration, contacts and orientation alongside position helps connect the one-dimensional curve with a specific molecular process.

For polymer desorption, centre-of-mass height may combine several distinct states. At the same average height, one end may have lifted, the middle may form an arch while both ends remain attached, or only a few contacts may remain. Trajectory inspection can distinguish these structures before adding contact number, free-end height or chain size as supplementary coordinates. A useful variable separates the states relevant to the question while allowing surrounding structures at similar coordinate values to interconvert. Ease of calculation provides a starting point; a clear connection with the physical change supports interpretation.

Final comparisons require consistent state definitions. To compare adsorption of one chain on two surfaces, use matched temperature, solvent conditions, contact definitions and reference regions, then calculate the relevant local PMFs or complete adsorption-state probabilities. Increasing chain length adds internal conformations and contact combinations, so the required sampling duration may also change. Keeping the surface, molecular structure and sampling conditions explicit makes differences between profiles traceable to the material factors being varied, instead of combining changed physics with changed definitions in the same comparison.

A free-energy curve can now be read as a sequence of concrete observations. The horizontal axis specifies a change, the vertical axis relates probability to temperature, windows identify where records were collected, overlap connects local observations, and time analysis describes variation in the available sampling. Linking these quantities to structures explains why molecules favour particular regions and guides the next observations. The following lesson extends the same reasoning to comparisons between groups of simulations, including independent preparations, matched conditions and the statistical unit used to report a difference.

## Further Reading and Open Materials

- [Tutorial 7: Free energy calculation](https://lammpstutorials.github.io/sphinx/build/html/tutorial7/free-energy-calculation.html) · Simon Gravelle, Cecilia M. S. Alvares, Jacob R. Gissinger, Axel Kohlmeyer · CC BY 4.0; original input headers retained

  Original repulsive-particle, central-field, direct-sampling and umbrella workflow.

  Pinned source dd3dce70; x-only restraint, instantaneous positions, 32 added windows, original statistical analysis and diagrams.
- [fix spring command](https://docs.lammps.org/fix_spring.html) · LAMMPS developers · Official documentation; command semantics cited

  One-half spring energy and NULL-axis conventions.

  Symbol explanations and an adjustable one-dimensional distribution exercise.
- [Nonphysical sampling distributions in Monte Carlo free-energy estimation: Umbrella sampling (1977)](https://doi.org/10.1016/0021-9991%2877%2990121-8) · G. M. Torrie and J. P. Valleau · Research article citation; no original image/text copied

  History of chosen sampling distributions and LJ validation.

  Original conceptual history diagram.
- [The weighted histogram analysis method for free-energy calculations on biomolecules. I. The method (1992)](https://doi.org/10.1002/jcc.540130812) · Shankar Kumar, John M. Rosenberg, Djamal Bouzida, Robert H. Swendsen, Peter A. Kollman · Research article citation; no original image/text copied

  WHAM and the historical deoxyadenosine sugar-pseudorotation application.

  Connect probability counts, self-consistency and biomolecular coordinates.
- [Convergence and error estimation in free energy calculations using the weighted histogram analysis method (2012)](https://doi.org/10.1002/jcc.21989) · Fangqiang Zhu and Gerhard Hummer · Research article citation; original equations used for independently written analysis

  WHAM optimization, self-consistency and sampling diagnostics.

  Independent Newton implementation, chronological subsets and contiguous-block resampling; numerical result separately checked by fixed-point iteration.
