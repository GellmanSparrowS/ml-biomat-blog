# From Wet Pellets to a Clean Melt: Drying and Devolatilization

Source: https://ml-biomat.com/tutorials/biomaterials-courses/pe01/en/
Language: en

A polymer pellet that looks dry may still hold water or solvent inside. Follow a small molecule's route out to understand diffusion, humidity, heat, thin films, and bubbles, then explore how thickness, air conditions, and melt viscosity change the rate of removal.

## Where water hides, and why it needs to leave

Hang a wet towel in moving air and the visible surface water disappears first. The towel can still feel cool and damp afterward because water remains between its fibers and inside them. Polymer pellets can behave in a similar way, although much of their water is invisible. Pellets that look dry may still produce bubbles, silvery surface streaks, or chain degradation when melted. Two different effects are involved. Water becoming vapor can disturb flow and appearance during shaping, while water reacting with susceptible chemical bonds can shorten the polymer chains themselves. Drying therefore aims to establish a suitable, consistent moisture state before the next operation, rather than simply making the outside of the pellets look dry.

The first distinction concerns location. A droplet resting on a pellet surface and a water molecule inside the polymer have different routes out. The droplet can evaporate directly from the surface. An internal molecule must first move through the environment between the chains, reach the surface, and then enter the gas. Some polymers contain polar groups that interact readily with water, such as amide groups. Polarity means that electric charge is distributed unevenly within a molecule, giving particular regions a greater tendency to interact with water. These interactions influence both water uptake and mobility. Consequently, pellets of two polymers can have the same size and experience the same surrounding air while absorbing and releasing water quite differently.

[Figure: Water location and migration](https://ml-biomat.com/tutorials/biomaterials-courses/pe01/en/#en-s1)

Figure 1 · Surface water and internal water have different paths to travel. Blue marks represent water molecules or droplets at schematic scales; the arrows connect internal diffusion, interface transfer, and removal by the gas.

Water is not the only small molecule that may need to leave. Residual monomer, solvent, and volatile reaction products can also remain in a polymer. A monomer is a small molecule used to build a chain; material that has not joined a chain may persist after polymerization. A solvent may have helped dissolve or mix the reactants during manufacture. Removing volatile components is called devolatilization and is often performed on a melt, concentrated solution, or dispersion. Drying and devolatilization have different practical requirements, but both ask how an internal molecule reaches an interface and then leaves it. Removing vapor from the surrounding gas does not, by itself, shorten the route that the molecule must travel inside the material.

Before asking how much water remains, choose a consistent definition. Consider a sample containing 98 grams of dry polymer and 2 grams of water. Dividing water mass by total sample mass gives the wet-basis moisture content. Dividing water mass by dry-polymer mass gives the dry-basis moisture content. These describe the same sample but produce slightly different numbers. During drying, the dry-polymer mass often remains approximately constant while the total wet-sample mass decreases, making the dry basis particularly convenient for material balances. Either grams or kilograms can be used, provided that the numerator and denominator use the same unit. Their units then cancel, leaving a dimensionless ratio.

Two moisture definitions, two denominatorsEq. 1

![Two moisture definitions, two denominators](https://ml-biomat.com/static/agent-math/ed648b6f5de0d3ad341dabe5.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| w | Wet-basis moisture, referred to total wet mass | 1 |
| X | Dry-basis moisture, referred to dry-polymer mass | 1 |
| m_{w} | Water mass; subscript w identifies water | kg |
| m_{p} | Dry-polymer mass; subscript p identifies polymer | kg |

Reading the relationshipDivide the water mass by the chosen reference mass. The polymer accounts for a fraction 1−w of the wet sample, so expressing the same water relative to dry polymer requires division by 1−w. Enter w as a fraction between zero and one. X is a water-to-dry-polymer ratio and may exceed one. Divide percentage values by 100 first.

A worked exampleFor 98 kg dry polymer and 2 kg water, the wet sample weighs 100 kg. Thus w=0.02, or 2%, whereas X=2/98≈0.020408, or 2.0408% on a dry basis. The difference comes from the denominator, not from a different sample.

ConditionsThe sample is divided into dry polymer and water. If other volatile components are present, specify how they enter the chosen reference mass.

Small moisture contents are also reported as percentages, parts per thousand, or parts per million. A percentage multiplies the mass ratio by one hundred. Mass ppm multiplies it by one million and tells us how many mass parts of water occur in one million mass parts of the specified sample. A wet-basis moisture content of 0.02%, for example, is 200 mass ppm, not 20 ppm. When comparing measurements, identify the denominator, whether the test measures water or all volatile material, and when the sample was taken. A loss-of-mass measurement may include solvent as well as water, whereas a water-specific method addresses a more narrowly defined quantity.

## Why molecules move from the interior toward the outside

Place a small drop of food coloring gently in still water. Even without stirring, the color gradually spreads. Individual molecules continually change position through thermal motion; they do not know which direction is less crowded. However, the darker region contains more dye molecules per unit volume. During a given time, more molecules are therefore likely to cross an imaginary boundary from the concentrated side than from the dilute side in the opposite direction. Motion occurs both ways, while the imbalance produces a net transfer. When the concentration becomes uniform, molecular motion continues. What disappears is the average difference between the two opposing transfers.

In 1855, [Adolf Fick](https://doi.org/10.1002/andp.18551700105) expressed diffusion as a quantitative relationship. Instead of tracking every molecule, he related concentration changes over distance to the amount passing through a cross section. The mathematical idea resembles the description of heat flowing from warmer to colder regions: identify a spatial difference and determine the transport associated with it. During drying, the polymer interior may remain relatively rich in water while dry gas removes water from its surface. A concentration profile develops across the material. A steeper profile means a greater concentration difference over the same distance, which generally supports a larger diffusion flux under otherwise unchanged conditions.

[Figure: Fick diffusion and concentration gradient](https://ml-biomat.com/tutorials/biomaterials-courses/pe01/en/#en-s2)

Figure 2 · Fick’s relationship connects spatial concentration differences with net transfer. The upper diagram shows motion in both directions; the lower one represents the concentration gradient as a slope. The modern schematic explains the diffusion problem formulated in 1855.

Concentration here means the amount of a substance per unit volume, expressed, for example, in moles per cubic meter. The mole is a counting unit for large numbers of microscopic entities: one mole contains approximately 6.022×10²³ specified entities. If the entities are water molecules, one mole of water has a mass of about 18 grams. Molar flux is the net amount crossing a unit area per unit time. It differs from the total transfer rate. A small window and a large opening can have similar transfer per square meter while allowing very different total quantities through. Multiplying flux by the available area gives the amount passing through the whole interface each second.

From a concentration gradient to a transfer rateEq. 2

![From a concentration gradient to a transfer rate](https://ml-biomat.com/static/agent-math/81e511cb20f8f054041978da.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| J | Net molar diffusion flux in the chosen positive direction | mol m⁻² s⁻¹ |
| D | Diffusion coefficient | m² s⁻¹ |
| C | Molar concentration of the diffusing component | mol m⁻³ |
| x | Position along the diffusion direction | m |
| dC/dx | Local spatial gradient of concentration | mol m⁻⁴ |
| A | Area normal to the transfer direction | m² |
| ṅ | Amount transfer rate across the complete area; the dot denotes a time rate | mol s⁻¹ |

Reading the relationshipThe gradient describes the spatial difference that drives transport, and D describes mobility within the material. Their product gives transfer per unit area; the minus sign directs diffusion toward lower concentration. Multiplication by area A gives the total rate.

A worked exampleA linear concentration drop from 2 to 0 mol/m³ across 1 mm gives a gradient of −2000 mol/m⁴. With D=10⁻¹⁰ m²/s, J=2×10⁻⁷ mol/(m²·s). Across 0.01 m², the total rate is 2×10⁻⁹ mol/s.

ConditionsThis is a one-dimensional Fickian description, with a uniform flux used to calculate the total rate. A spatially varying flux requires summing contributions over the area. Transport by bulk flow is accounted for separately.

The derivative in this expression can be understood as a slope. Choose two nearby positions, subtract their concentrations, and divide by their separation to obtain an average rate of spatial change. Making the separation progressively smaller gives the local concentration gradient. The minus sign establishes a consistent direction convention. If concentration decreases from left to right, the gradient is negative; the net movement of water is toward the right and its flux should be positive. The minus sign does not make the diffusion coefficient negative. That coefficient describes mobility under specified material, temperature, and composition conditions; it is not a number determined solely by the name of the diffusing molecule.

The same diffusion-coefficient notation can represent different molecular journeys. In a dilute gas, a molecule travels between collisions and changes direction when it collides. The mean distance between successive collisions with other molecules is its mean free path. At the same temperature, lowering pressure in a sufficiently dilute gas increases molecular separation and usually lengthens this path, allowing faster gas diffusion. Temperature also changes thermal speeds. This describes diffusion relative to the bulk gas motion. If a pump also carries the gas away, molecular displacement includes that additional convective motion.

In a liquid, neighbouring molecules are close together, so migration resembles making progress through a crowd whose members continually rearrange. For a dilute suspension of approximately spherical solutes large enough for the surrounding liquid to behave as a continuum, viscous drag competes with thermal motion: larger particles and more viscous solvents generally mean slower diffusion at the same temperature. This is the physical starting point of the Stokes–Einstein description. Within that regime, doubling solvent viscosity while keeping particle size and temperature unchanged predicts half the diffusion coefficient. A small molecule comparable in size to the solvent, strong binding, or a complicated local structure requires a more specific account of its surroundings. Dye diffusion in water, nanoparticle diffusion in a dilute suspension, and monomer migration through a concentrated polymer cannot all be inferred from one bulk-viscosity measurement.

A porous solid adds pore walls and a connected network of passages. When the gas mean free path is much smaller than the pore diameter, most encounters along the journey are with other molecules. Narrower pores, or a sufficiently reduced pressure and longer free path, make encounters with the walls more frequent. Gas transport dominated by those wall collisions is called Knudsen diffusion. Dividing mean free path by pore diameter gives the Knudsen number, which indicates the relative importance of the collision mechanisms; both contribute in the intermediate region. Even rapid migration within an individual pore need not give rapid release from an entire pellet. Passages may wind, connect poorly or end without reaching the outside. Porosity describes how much volume is occupied by pores, while a transport tortuosity factor represents impediments associated with winding, orientation and constrictions. They describe different aspects of the route.

From transport inside pores to bulk-area fluxEq. 3

![From transport inside pores to bulk-area flux](https://ml-biomat.com/static/agent-math/ec742f119788ca5f4dcb2ff9.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Kn | Knudsen number, comparing mean free path with pore diameter | 1 |
| λ | Mean free path between gas-molecule collisions; use the same length unit as pore diameter | m |
| d_{p} | Representative pore diameter; p denotes pore here | m |
| ε | Volume fraction of connected pores participating in transport | 1 |
| 𝒯 | Transport tortuosity factor used here, at least1; not simply the geometric path-length ratio | 1 |
| D_{pore} | In-pore diffusivity, incorporating the relevant gas-molecule and wall-collision effects for a gas | m² s⁻¹ |
| D_{eff} | Effective diffusivity referred to pore concentration gradient and whole-material cross section | m² s⁻¹ |
| J_{bulk} | Net molar flux per total cross-sectional area, including solid area | mol m⁻² s⁻¹ |
| ΔC_{pore} | Outlet minus inlet pore concentration; positive direction runs from inlet to outlet | mol m⁻³ |
| L | Material thickness along the macroscopic transport direction | m |

Reading the relationshipFree path divided by pore diameter compares travel between molecular collisions with wall spacing. Porosity reduces available space and tortuous paths further reduce transport, giving the factor ε/𝒯. Multiplication by concentration difference per distance gives bulk-area flux; the minus sign makes it point down the concentration gradient.

A worked exampleFor λ=70 nm and d_p=7 nm, Kn=10 and wall collisions are important. Take D_pore=10⁻⁶ m²/s, already including wall effects, ε=0.30 and 𝒯=3: D_eff=10⁻⁷ m²/s. At L=1 mm=10⁻³ m with inlet and outlet pore concentrations1 and0 mol/m³, ΔC_pore/L=−1000 mol/m⁴ and J_bulk=10⁻⁴ mol/(m²·s).

ConditionsKn identifies gas transport regimes inside pores. The last two relations estimate steady dilute-species diffusion in a homogeneous connected network filled with one fluid, without bulk flow, using approximately constant coefficients and gradient in the chosen direction. Adsorption, surface diffusion and evolving porosity are absent. Transient calculations must also include storage in the pores; this D_eff is not directly interchangeable with dense-material diffusivity. A different tortuosity convention requires the corresponding coefficient relation.

Migration through a dense polymer does not require a visibly open passage connecting its interior to the outside. A small molecule can first dissolve in the material, then move between nearby positions as thermal motion of chain segments temporarily makes local space available. Imagine finding the next gap among pieces of furniture that keep moving: these openings are not permanent tunnels. Crystalline regions commonly restrict transport, while segmental motion, local free volume and intermolecular attractions influence pathways through the amorphous regions. Heating or absorption of water or solvent may increase segmental mobility and make diffusivity depend on water content. The early and late stages of drying a pellet can therefore have different migration rates. Flow through connected gas-filled pores, diffusion through liquid-filled pores, and dissolution followed by migration through a dense polymer need to be identified separately.

[Figure: Molecular diffusion in gas liquid pores and dense polymer](https://ml-biomat.com/tutorials/biomaterials-courses/pe01/en/#en-s2)

Figure 3 · Gas collisions, liquid rearrangement, a connected pore network and polymer-segment motion provide different transport environments. Orange dots or lines mark a tracked molecule or its route. Local gaps in dense polymers change with segment motion rather than forming permanent open channels.

Air moving past a pellet adds another transport mechanism. The gas as a whole carries water vapor away after the water has entered it; this is convection. Convection and diffusion can occur simultaneously, rather like a passenger walking inside a train while the train itself moves. Increasing airflow can remove vapor from near the surface and reduce the external transport resistance. Once the slowest step is diffusion inside the pellet, however, additional airflow may bring progressively smaller improvements. To distinguish insufficient gas renewal from slow internal migration, follow the entire route rather than treating drying as a single, undivided event.

## Why a thinner material can dry much faster

Early in drying, the surface water concentration may fall quickly while the interior stays comparatively wet. Concentration then varies with time as well as position. Imagine dividing the material into many thin layers. If more water leaves one layer than enters it, the amount stored there decreases. If more enters than leaves, water accumulates. Combining this material balance with Fick's relationship gives the diffusion equation. It uses the present concentration profile to determine which regions will lose water most rapidly next, providing a description of the gradual drying of the interior. The equation is therefore a bookkeeping statement about moving molecules as well as a mathematical model.

How a concentration profile changes with timeEq. 4

![How a concentration profile changes with time](https://ml-biomat.com/static/agent-math/1caaffcf2229f9c3923e179a.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| C | Molar concentration of water in the material | mol m⁻³ |
| t | Time since the start of drying | s |
| x | Position across the slab thickness | m |
| D | Constant diffusion coefficient | m² s⁻¹ |
| ∂C/∂t | Rate of concentration change at a fixed position | mol m⁻³ s⁻¹ |
| ∂²C/∂x² | Spatial change of the concentration slope, or curvature | mol m⁻⁵ |

Reading the relationshipThe symbol ∂ means changing one variable while holding the other fixed. The right side compares concentration slopes at neighboring positions and therefore reflects the difference between inflow and outflow. The left side records local accumulation. Combining material conservation with Fickian flux explains why concentration peaks gradually flatten.

A worked exampleAt a point where the concentration curvature is −10⁶ mol/m⁵ and D=10⁻¹⁰ m²/s, the instantaneous concentration-change rate is −10⁻⁴ mol/(m³·s). The negative sign means local water loss. This is the rate for the current profile; it changes as that profile evolves.

ConditionsThe geometry and D are fixed, diffusion is one-dimensional, and bulk flow and internal reactions are absent. Predicting a particular curve additionally requires an initial profile and boundary conditions.

A particularly useful result concerns the relationship between diffusion distance and time. Random motion includes backward as well as forward steps. Molecules do not travel like cars moving steadily along a highway, where doubling the distance simply doubles the travel time. With an unchanged diffusion coefficient, allowing diffusion to affect a region twice as far away requires roughly four times the time. In a slab drying from both faces, the most distant point lies at the center, so the half-thickness is the natural length scale. For a spherical pellet, the radius is commonly used. Geometry changes the precise numerical factors but preserves the central dependence on distance squared.

Diffusion time grows with distance squaredEq. 5

![Diffusion time grows with distance squared](https://ml-biomat.com/static/agent-math/b089d515c1b7b93cffbf85b0.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| t_{D} | Diffusion time scale based on the chosen length | s |
| L | Characteristic path; the half-thickness for a slab drying from both faces | m |
| D | Diffusion coefficient | m² s⁻¹ |

Reading the relationshipIn the diffusion equation, the temporal change scales as a concentration difference divided by time, while the spatial term scales as that difference divided by distance squared. Equating the scales cancels the concentration difference and gives L²/D. The time to a particular residual fraction additionally depends on geometry and boundary conditions.

A worked exampleFor L=0.5 mm=5×10⁻⁴ m and D=10⁻¹¹ m²/s, t_D=25000 s≈6.94 h. Increasing L to 1 mm at the same D gives 100000 s≈27.8 h, four times the original scale.

ConditionsThis scale compares processes governed by internal diffusion with a representative D. A specified drying endpoint requires the corresponding concentration solution.

This relationship explains why spreading a melt into a thin film, atomizing a liquid into droplets, or preventing particles from agglomerating can substantially improve removal. Geometry affects two distinct features: the exposed area per amount of material and the greatest distance an internal molecule must travel to reach an interface. More area provides additional exits, while a shorter path reduces the time needed to reach an exit. The two effects are related but should not be merged into a single quantity. Roughening the surface of a large pellet can increase its external area without greatly reducing the distance from its center. A surface that looks open or irregular is therefore not sufficient evidence of rapid internal drying.

[Figure: Slab concentration profiles during drying](https://ml-biomat.com/tutorials/biomaterials-courses/pe01/en/#en-s3)

Figure 4 · Three concentration profiles from the constant-diffusivity slab model. Position runs from one surface through the center to the other. All curves solve the same diffusion equation, showing the earlier change near the surfaces.

To turn this reasoning into a curve, consider a slab of fixed thickness. Its initial moisture distribution is uniform, both faces maintain the same constant surface concentration from the start of drying, and the internal diffusion coefficient is constant. The average moisture content gradually approaches the equilibrium value associated with those surfaces. The series solution below separates the changing profile into modes that decay at different rates. The summation sign instructs us to add their contributions. This resembles combining musical tones, except that the quantities being added are concentration patterns. Many modes are needed to describe the sharp early changes near the surfaces. Later, the rapidly decaying modes contribute little and the slowest mode controls the tail.

The average moisture remaining in a slabEq. 6

![The average moisture remaining in a slab](https://ml-biomat.com/static/agent-math/b9129ec1e9832c4fb123e44e.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| q(t) | Average remaining fraction relative to surface equilibrium | 1 |
| C̄(t) | Slab-average concentration at time t; the bar denotes an average | mol m⁻³ |
| C₀ | Uniform initial concentration | mol m⁻³ |
| Cₛ | Concentration maintained at both surfaces | mol m⁻³ |
| D | Constant diffusion coefficient | m² s⁻¹ |
| t | Time since drying began | s |
| L | Slab half-thickness | m |
| j | Mode index starting at zero | 1 |
| Σ、∞ | Sum all modes j=0,1,2,...; ∞ denotes an infinite sequence | 1 |
| π | The constant pi, approximately 3.14159 | 1 |
| exp(u) | The exponential function e raised to u; a more negative argument gives a smaller value | 1 |

Reading the relationshipSubtracting the surface-equilibrium concentration and dividing by the initial excess puts different initial moisture levels on the same fractional scale. Each term represents a decaying diffusion mode. Higher mode numbers have larger decay coefficients. The combination Dt/L² is dimensionless, as an exponential argument must be.

A worked exampleWith L=0.5 mm, D=10⁻¹¹ m²/s, and t=2 h, Dt/L²=0.288 and the series gives q≈0.398. For a nearly zero surface concentration, about 39.8% of the initial average moisture remains. This does not mean a wet-basis moisture content of 39.8%.

ConditionsThe initial concentration is uniform, both faces maintain the same Cₛ from t=0, D and geometry are constant, and surface transfer resistance is neglected. The exact series equals 1 at t=0; the interactive plot uses that initial limit.

### Change thickness and diffusivity to explore drying

[Figure: Average remaining moisture against drying time](https://ml-biomat.com/tutorials/biomaterials-courses/pe01/en/#en-s3)

Curves use the slab solution with constant diffusivity and fixed concentrations at both faces. The time axis remains 0–24 hours; the orange dashed line marks 10% remaining and the dot marks the selected time.

When moving the thickness slider, first compare the time required to reach the same remaining fraction, then compare the remaining fractions at a fixed time. These answer different questions: how long must each sample wait to become equally dry, and which sample is wetter after the same two-hour period? A single percentage cannot replace both comparisons. Real pellets may also involve external transfer resistance, changing temperature, pores, and concentration-dependent diffusivity. Those effects can be incorporated when needed. The ideal slab already reveals a frequently overlooked size effect and gives us a clear reference against which to understand more complicated shapes and drying conditions.

## How dry air determines the attainable moisture level

Clothes can retain a damp feel after hanging for a long time in humid weather. The issue is not simply slower removal: the surrounding gas also influences where water remains at equilibrium. Water molecules continually exchange between the polymer and the air. At equilibrium, the average transfers balance, even though the polymer may still contain water. Calling this quantity the equilibrium moisture content separates two questions. Diffusion controls how quickly equilibrium is approached, while the equilibrium relationship determines the endpoint. If the required moisture level lies below the equilibrium value for the current environment, waiting longer will not achieve it. The gas humidity, temperature, or another relevant equilibrium condition must change.

Relative humidity compares the actual water-vapor partial pressure with the saturation vapor pressure of water at the same temperature. A partial pressure is the contribution of one gas component to the total gas pressure. Saturation vapor pressure describes the pressure of water vapor in equilibrium with liquid water at the specified temperature. It generally increases as temperature rises. Thus, heating a gas without adding or removing water, at approximately constant total pressure, lowers its relative humidity without eliminating the water it carries per unit mass of dry gas. Heating and dehumidifying perform different tasks. This is why hot air and dry air must be considered separately when analyzing a drying system.

Relative humidity compares actual and saturation pressuresEq. 7

![Relative humidity compares actual and saturation pressures](https://ml-biomat.com/static/agent-math/71506bc53a584b59d2cdb85f.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| RH | Relative humidity as a fraction; multiply by 100 for percent | 1 |
| p_{w} | Partial pressure of water vapor | Pa |
| p_{sat}(T) | Saturation vapor pressure of water at temperature T | Pa |
| T | Temperature at which saturation pressure is evaluated | K |

Reading the relationshipBoth numerator and denominator are pressures. Their ratio measures how close the vapor is to saturation at that temperature. Changing T changes the denominator, so relative humidity alone cannot establish whether gases at different temperatures carry the same amount of water.

A worked exampleIf p_sat=5000 Pa at a chosen temperature and p_w=1000 Pa, RH=0.20, or 20%. If heating raises p_sat to 10000 Pa while p_w remains unchanged, RH becomes 10%. These specified pressure values illustrate how the ratio changes.

ConditionsThe gas is close to ideal, with vapor in equilibrium with liquid water at the same temperature as the reference. If total pressure changes, account for the accompanying change in water partial pressure.

[Figure: Humidity changes on heating without removing water](https://ml-biomat.com/tutorials/biomaterials-courses/pe01/en/#en-s4)

Figure 5 · Relative humidity compared using two specified sets of pressures. Dark bars show actual water-vapor pressure and pale bars show saturation pressure. Heating changes the saturation reference without removing the water.

Dew point provides another way to describe the moisture in a gas. Cool the gas at a specified pressure: the temperature at which condensation first appears is its dew point. A lower dew point generally corresponds to a lower water-vapor partial pressure. This description helps separate how hot the gas currently is from how much water it actually carries. A drying system may first pass air through an adsorbent to remove water and then heat that air before sending it into a hopper. The returning humid air can be treated and circulated again. Following these separate functions explains why the heater temperature alone cannot establish whether sufficiently dry gas is being supplied throughout the operation.

Inside a polymer, a water molecule no longer has only other water molecules as its neighbors. Its interactions with the polymer and the arrangements available after mixing jointly determine its chemical potential. As a first interpretation, chemical potential is the free-energy change associated with adding a small amount of a particular substance. Sustained net migration stops when that potential is equal on both sides of an interface. During the 1940s, Flory and Huggins independently developed statistical descriptions of polymer mixing that accounted for a chain occupying many connected positions. Applied to drying, this idea offers a simplified link between the humidity of the gas and the amount of water held inside a polymer.

Linking humidity and internal water with a mixing modelEq. 8

![Linking humidity and internal water with a mixing model](https://ml-biomat.com/static/agent-math/86a0b1c9cecd808a78cbcb34.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| RH | Equilibrium relative humidity as a fraction | 1 |
| φ_{w} | Volume fraction of water in the polymer phase | 1 |
| N | Number of lattice sites occupied by a polymer molecule relative to one site per water molecule | 1 |
| χ | Water–polymer interaction parameter in the model | 1 |
| ln | Natural logarithm, the inverse of the exponential function | 1 |

Reading the relationshipThe first term concerns arrangements on mixing, the middle term accounts for the size difference between water and chains, and the last describes energetic effects of unlike contacts. Phase equilibrium links water activity in the polymer to relative humidity in the gas, giving dimensionless logarithms on both sides.

A worked exampleFor an illustrative lattice system with φ_w=0.01, N=1000, and χ=0.5, the right side is approximately −3.1261. Thus RH=exp(−3.1261)≈0.0439, or 4.39%. The calculation demonstrates the model; material-specific sorption behavior determines appropriate parameters.

ConditionsThis uses a binary incompressible Flory–Huggins lattice model with a composition-independent representative χ and an approximately ideal gas. Specific adsorption, nonequilibrium glassy behavior, or strong specific interactions require an appropriate extension.

The volume fraction in this equation differs from the mass fractions defined earlier. To estimate occupied volumes from weighed amounts of water and polymer, their densities are also needed. The interaction parameter is not a universal numerical scale of polarity; it depends on the chosen components, temperature, and model. Strong specific interactions, glassy-state hysteresis, or distinct adsorption sites can require a different sorption description and experimental data. These conditions tell us how to use the equation: first identify how the material holds water, then determine how changing the surrounding humidity shifts the equilibrium. They also keep a convenient mathematical expression connected to the actual physical state of the sample.

## Following the heat as water leaves

Moving air over wet skin feels cool because evaporation absorbs energy. During polymer drying, hot gas similarly transfers energy to the material. Some raises the material temperature, while some supplies the energy needed to vaporize water. When free liquid continually replenishes the surface and the external heat- and mass-transfer conditions remain approximately steady, the evaporation rate may remain nearly constant. This is the constant-rate period. The surface is often cooler than the hot gas because evaporation continually consumes incoming heat. Such a period is not obligatory for every polymer pellet: a hygroscopic pellet without a continuous surface-water layer may be governed mainly by internal transport from the beginning.

Once the surface is no longer continuously wet, the supply of internal water becomes increasingly important and the drying curve enters a falling-rate period. As moisture decreases, the effective migration path, local free volume, and molecular interactions can change further, so the rate need not decline according to a single fixed constant. At the same time, a smaller portion of the supplied energy is consumed by evaporation, and the material temperature often approaches that of the surrounding gas. Hot outlet air does not therefore prove that the interior is fully dry, and a rising pellet temperature does not establish uniform moisture throughout it. Temperature and mass-change observations are more informative when interpreted together.

Estimating the energy needed for vaporizationEq. 9

![Estimating the energy needed for vaporization](https://ml-biomat.com/static/agent-math/2f87b08cda94fea82fba7fd4.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Q_{vap} | Energy needed to vaporize the specified water amount | kJ |
| m_{evap} | Mass of water to be vaporized and removed | kg |
| Δh_{vap} | Vaporization enthalpy per mass; Δ denotes a difference between vapor and liquid states | kJ kg⁻¹ |

Reading the relationshipIf every kilogram requires the same representative vaporization energy, multiplying that energy by the number of kilograms gives the total vaporization contribution. Material and equipment heating, together with other energy flows, are added separately in the complete balance.

A worked exampleFor m_evap=2 kg and Δh_vap=2300 kJ/kg, Q_vap=4600 kJ=4.6 MJ. Supplying this contribution alone at an effective 1 kW requires 4600 s, or about 1.28 h, because 1 kW is 1 kJ per second.

ConditionsA representative vaporization enthalpy is used for the chosen temperature range, with additional desorption enthalpy excluded. This is one contribution to a complete system energy balance.

Improving the drying rate requires separate consideration of heat and mass transfer. Increasing the temperature difference can strengthen heat input. Suitable airflow and surface renewal can remove vapor. Shortening internal paths accelerates diffusion, while lowering gas moisture helps maintain the driving force. A temperature increase may also raise the diffusion coefficient, but it can accelerate oxidation, degradation, or other unwanted reactions. Softened pellets may stick together and form agglomerates with longer internal paths. Selecting conditions therefore requires attention to the material's state and how it changes with temperature, rather than treating every available control as something that should simply be increased.

Equipment geometry expresses these choices. A fluidized bed uses upward gas flow to keep particles moving and improve gas–particle contact. A spray dryer divides a liquid feed into small droplets, exchanging a short internal path for faster moisture removal. Pneumatic drying uses flowing gas to transport and disperse particles. Each arrangement suits different feed forms and requires attention to fine-particle recovery, sticking, and residence time. Hopper drying of pellets before melt processing emphasizes the distribution of gas through the bed and whether every portion of material receives sufficient, reasonably uniform exposure. Behind the equipment names lies the same task: provide workable routes for heat to enter and small molecules to leave.

## How volatile molecules escape from a melt

A polymer melt is much more viscous than water. Picture a flowing assembly of long, interpenetrating chains, with small molecules moving through a local environment that continually changes. Reducing the partial pressure of a volatile component in the surrounding gas favors its transfer from the melt into that gas, but a vacuum pump primarily changes the external conditions. In a thick mass of melt, the deepest molecules still have a long route to an interface. Industrial devolatilization therefore often combines reduced pressure with thinning, dispersion, mixing, and surface renewal. Geometry improves the internal route while the gas-side conditions sustain the tendency of the volatile material to leave.

Thin-film devolatilization makes this reasoning visible. Moving wipers or rotating disks spread the melt into thin layers and continually bring fresh material close to a surface. A strand devolatilizer forms narrow streams of melt with more exposed area, while a vented screw provides gas-removal zones during conveying and mixing. Renewing a surface means changing which material lies near the gas, rather than creating material from nothing. As volatile content, composition, and temperature change, melt viscosity can change too, coupling flow, heat transfer, and devolatilization. Following the melt path and the vapor path separately through a drawing often reveals more than memorizing the name of the machine.

[Figure: Thin-film transport and bubble pressure](https://ml-biomat.com/tutorials/biomaterials-courses/pe01/en/#en-s6)

Figure 6 · A thin film shortens the internal route, while a bubble adds an interface inside the material. The Young–Laplace relationship sets the static pressure requirement; viscous flow additionally influences the growth rate.

A second route creates bubbles inside the melt, adding internal gas–liquid interfaces. A bubble does not necessarily grow merely because gas is present. The surrounding melt exerts pressure, curvature introduces a surface-tension contribution, and expansion requires the viscous material to move. In the early nineteenth century, Young and Laplace connected the pressure difference across a curved interface with its curvature. That insight explains droplets and capillary effects and also shows why a very small bubble needs a larger internal pressure to persist. For a spherical bubble, the pressure difference needed to balance surface tension increases as the radius decreases.

A curved interface requires a pressure differenceEq. 10

![A curved interface requires a pressure difference](https://ml-biomat.com/static/agent-math/1fdcc8566c6c9bf8386f1a17.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| p_{B} | Pressure inside the spherical bubble | Pa |
| p_{L} | Liquid pressure immediately outside the interface | Pa |
| γ | Gas–liquid interfacial tension | N m⁻¹ |
| R | Bubble radius | m |

Reading the relationshipA sphere has equal curvature in two perpendicular directions, giving the factor 2. Interfacial tension divided by radius has pressure units: N/m divided by m is N/m², or Pa. A smaller radius therefore requires a larger pressure difference for the same tension.

A worked exampleWith γ=0.03 N/m and R=10 μm=10⁻⁵ m, the pressure difference is 6000 Pa, or 6 kPa. At R=100 μm it falls to 600 Pa.

ConditionsA single spherical gas–liquid interface is static or quasistatic and has approximately uniform γ. A film with two interfaces or a rapidly moving interface requires its corresponding mechanical relationship.

The pressure threshold introduced by surface tension helps explain why nucleation can be important in devolatilization. Existing cavities, particle surfaces, or small quantities of entrained gas can sometimes provide starting points for bubbles. Once growth begins, however, volatile molecules must still reach the bubble, and its pressure changes with temperature, composition, and volume. If the melt is temporarily approximated as a Newtonian liquid of constant viscosity and inertia is neglected, a simple growth relationship follows from balancing viscous resistance against the pressure driving force. Newtonian means that, within this model, shear stress is proportional to shear rate and the proportionality coefficient is the viscosity.

Pressure and viscous resistance determine the growth rateEq. 11

![Pressure and viscous resistance determine the growth rate](https://ml-biomat.com/static/agent-math/c46f2d771d281dfb676521f8.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| R | Current bubble radius | m |
| t | Time | s |
| dR/dt | Instantaneous rate of change of bubble radius | m s⁻¹ |
| p_{B}、p_{L} | Bubble pressure and pressure in the surrounding melt far from the interface | Pa |
| γ | Gas–liquid interfacial tension | N m⁻¹ |
| η | Dynamic viscosity of the Newtonian liquid | Pa s |

Reading the relationshipThe pressure difference drives expansion, tension resists creating interface, and viscosity sets the resistance to surrounding liquid motion. A positive numerator gives growth and a negative one gives shrinkage. The factor 4 comes from the velocity field for spherical incompressible viscous flow.

A worked exampleSet p_B−p_L=10000 Pa, R=10 μm, γ=0.03 N/m, and η=1000 Pa·s. The numerator is 0.10−0.06=0.04 N/m, giving dR/dt=10⁻⁵ m/s, or 10 μm/s. This is an instantaneous rate at the specified current state.

ConditionsAn isolated spherical bubble is surrounded by an incompressible Newtonian liquid of constant viscosity, with inertia and elastic stresses neglected. The current pressure difference is an input; a full growth trajectory also needs gas-state, heat-transfer, and mass-transfer relations.

### Will the bubble grow or shrink?

[Figure: Bubble radius, its rate of change, and the critical radius](https://ml-biomat.com/tutorials/biomaterials-courses/pe01/en/#en-s6)

The diagram shows the instantaneous rate at the selected state. Pressure difference is an independently specified input; predicting a full growth history also requires tracking gas amount and heat.

In the interactive diagram, hold pressure difference and surface tension constant while increasing the initial radius. Watch where the predicted behavior changes from shrinkage to growth. Then change viscosity alone and observe how it modifies the rate without directly changing the static pressure threshold. Real polymer melts can retain elastic memory, exhibit rate-dependent viscosity, and contain interacting bubbles. The isolated spherical-bubble relationship is useful for understanding the roles and dimensions of the separate terms. It also explains why a photograph full of bubbles cannot establish removal efficiency: the volatile material must enter those bubbles, and the bubbles must ultimately escape instead of remaining trapped in the product.

## Removing monomer from an aqueous dispersion

Some polymer products consist of fine particles dispersed in water, as in certain latex systems. Residual monomer can be distributed among the polymer particles, the water, and the gas. Introducing gas or steam creates bubbles and fresh interfaces. Volatile material transfers from the surrounding liquid into the bubbles and leaves with the gas; this operation is called stripping. A useful drawing must follow the complete route of a monomer molecule, rather than merely showing a large bubble. The molecule first moves from the particle interior to its surface, enters the water, crosses a local liquid-side transfer region, and finally enters the bubble.

This sequence resembles a journey with several transfers, each with its own capacity. Stirring can improve mixing in the water, and many smaller bubbles can provide a larger total contact area. Yet if most monomer remains deep inside polymer particles, internal diffusion at the start of the route may still control the overall removal rate. Partitioning between polymer and water matters as well. A substance that prefers the polymer phase requires an equilibrium relationship to determine the particle-surface condition even when its concentration in the water is already low. Resistances can only be compared or combined consistently when their driving forces are expressed on a compatible concentration or chemical-potential basis.

[Figure: The complete stripping path through polymer water and gas](https://ml-biomat.com/tutorials/biomaterials-courses/pe01/en/#en-s7)

Figure 7 · Monomer moves through the particle, water, and bubble before leaving the equipment. Stirring, bubble area, and internal diffusion influence different parts of the route. Volatile recovery completes the process.

Transfer near a spherical bubble differs geometrically from transfer near a flat surface. The farther we move from the bubble, the larger the surrounding spherical area becomes. Under approximately steady conditions, the same total amount passes through each sphere per unit time, but the flux per unit area changes with distance. Fick's relationship and mass conservation yield a simple result for transfer to a fixed-radius spherical interface in a quiescent, effectively infinite liquid. The rate for one sphere is proportional to its radius. Dividing a fixed total gas volume into many smaller spheres also changes bubble number and total area, so a single large bubble and a cloud of smaller bubbles must be treated as different comparisons.

Transfer from a quiescent liquid to a spherical interfaceEq. 12

![Transfer from a quiescent liquid to a spherical interface](https://ml-biomat.com/static/agent-math/0de1e4fcb9fcc618694451a3.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ṅ | Total molar rate into the spherical interface | mol s⁻¹ |
| D | Diffusion coefficient of the component in the liquid | m² s⁻¹ |
| R | Fixed radius of the spherical interface | m |
| C∞ | Concentration far from the interface; ∞ indicates the distant region | mol m⁻³ |
| Cₛ | Concentration maintained at the spherical interface | mol m⁻³ |
| π | The constant pi | 1 |

Reading the relationshipAt steady state, the same total amount crosses every concentric sphere. Increasing area with radius squared makes the concentration gradient vary with distance. Integrating the profile, evaluating its surface gradient, and multiplying by the sphere area gives a total rate proportional to radius.

A worked exampleFor D=10⁻⁹ m²/s, R=0.5 mm=5×10⁻⁴ m, and C∞−Cₛ=1 mol/m³, ṅ≈6.28×10⁻¹² mol/s. This is one fixed spherical interface; the total for many bubbles also depends on their number and whether their diffusion fields overlap.

ConditionsThe radius is fixed, the liquid boundary is sufficiently distant, D is constant, and the concentration field is steady with no convection. Growing or moving bubbles need transient or convective descriptions.

How the concentration field develops also depends on what happens when the clock starts. Suppose the liquid is initially uniform at its far-field dissolved concentration. At time zero, the concentration at a fixed spherical surface is suddenly lowered and then held constant. A steep change develops immediately next to the surface, while distant liquid has had little time to respond. The affected region is called a diffusion layer. It is not a membrane with a sharp edge, but a region where concentration has departed appreciably from its initial value. Initially this region is much thinner than the sphere radius, so the surface looks locally flat. As the affected distance grows, the increase of spherical area with distance becomes increasingly important to transport.

Diffusion develops around a fixed sphereEq. 13

![Diffusion develops around a fixed sphere](https://ml-biomat.com/static/agent-math/00c366e1fb255ba3196e384b.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| J_{in}(t) | Net flux from the surrounding liquid into the sphere, positive inward | mol m⁻² s⁻¹ |
| D | Constant diffusivity of the species in the surrounding liquid | m² s⁻¹ |
| C∞ | Initially uniform liquid concentration, also maintained far away; ∞ denotes the distant liquid | mol m⁻³ |
| C_{s} | Surface concentration held constant from time zero; s denotes surface | mol m⁻³ |
| R | Fixed sphere radius | m |
| t | Positive elapsed time since the surface concentration changed | s |
| ṅ(t) | Net molar rate received by the whole sphere; dot denotes amount per time | mol s⁻¹ |
| t_{D} | Time scale for diffusion to affect distances comparable to the radius | s |
| π, √ | π is approximately3.14159; the square root turns πDt from an area into a length | π is dimensionless; √(πDt) has unit m |

Reading the relationshipThe spherically symmetric diffusion solution gives a surface gradient equal to the concentration difference times two inverse lengths. The1/R term comes from spherical geometry;1/√(πDt) comes from the newly developing diffusion layer that thickens with time. Multiply by D for flux and by sphere area4πR² for total rate. Length squared divided by diffusivity gives a time scale, not the time to a specified steady-state accuracy.

A worked exampleFor D=10⁻⁹ m²/s, R=5×10⁻⁴ m and C∞−C_s=1 mol/m³, t_D=250 s. At t=250 s, √(πDt)=8.862×10⁻⁴ m, giving2000+1128.4 m⁻¹ in brackets. Thus J_in≈3.128×10⁻⁶ mol/(m²·s) and ṅ≈9.83×10⁻¹² mol/s, versus the steady6.28×10⁻¹² mol/s. At t=25000 s, ṅ≈6.64×10⁻¹² mol/s.

ConditionsFixed radius and D, an infinite liquid without convection or bulk reaction. Initially every point outside the surface has concentration C∞. Subsequently the surface remains at C_s and the far field at C∞; C∞>C_s gives inward transfer. The surface change is instantaneous and the flux expression applies for t>0. Finite outer boundaries, evolving radius or evolving surface concentration require the corresponding transient model.

The expression separates surface flux into two contributions. The first is the steady spherical result. The second decreases with the inverse square root of time, retaining the effect of establishing a concentration field from an initially uniform liquid. With the same radius of 0.5 millimetres and diffusivity of 10⁻⁹ square metres per second, radius squared divided by diffusivity gives a time scale of 250 seconds. At 250 seconds the total rate is still about 56.4% above its steady value. A diffusion layer comparable in thickness to the radius therefore does not yet mean a small steady-state error. At 25000 seconds the excess is about 5.64%, bringing the result closer to the steady limit. Choosing an acceptable difference determines when that simpler calculation becomes useful.

[Figure: Transient spherical diffusion rate approaching its steady limit](https://ml-biomat.com/tutorials/biomaterials-courses/pe01/en/#en-s7)

Figure 8 · The curve uses the fixed-sphere solution after a surface-concentration step. Both axes are dimensionless: total rate divided by its steady value, and time divided by t_D. Adjacent horizontal ticks differ tenfold. The scale t_D is radius squared divided by liquid diffusivity; the stated seconds correspond to radius 0.5 mm and diffusivity 10⁻⁹ m²/s.

Approach to a steady state means that the concentration gradient and flux near the sphere progressively approach their steady values. An infinite liquid cannot finish adjusting everywhere at any finite time. As time approaches zero, the ideal expression gives an increasingly large instantaneous flux because the surface concentration changes abruptly and there is no interfacial resistance. A real interface takes time to establish. If a bubble moves, grows appreciably, or accumulates enough material to change its surface equilibrium concentration, the flow, interface position and concentration conditions must evolve together. The fixed-sphere result isolates the role of the developing diffusion layer and helps identify when those additional processes matter.

Stripping also depends on gas–liquid equilibrium. The driving force for leaving the liquid depends on the volatile component's partial pressure inside the bubble, and continued gas renewal helps sustain transfer. Steam may supply heat as well as contribute to gas composition, but it also changes the water balance, condensation load, and thermal history of the material. After leaving the main vessel, the volatile components generally need to be condensed, separated, or recovered. A material balance remains incomplete if it considers the polymer residue but ignores where the exiting gas goes. Feed, product, exhaust, and condensate belong on the same overall flow diagram.

## Combining amount, time, and equipment in one problem

Consider a 100-kilogram wet-polymer batch with an initial wet-basis moisture content of 2%, to be reduced to 0.02%. The initial batch contains 2 kilograms of water and 98 kilograms of dry polymer. Because the target percentage refers to the final wet-sample mass, the final water amount must be determined using the unchanged 98-kilogram dry mass and the target ratio together. It is approximately 0.0196 kilograms, so about 1.9804 kilograms of water must leave. Multiplying the original 100 kilograms directly by the target percentage gives a close result here, but that approximation relies on the small moisture fraction. Identifying the conserved dry mass gives a calculation that remains logically consistent.

Now consider time. At a fixed temperature, suppose the material can be approximated as a slab drying from both faces, with a half-thickness of 0.5 millimeters and a diffusion coefficient of 10⁻¹¹ square meters per second. Assume that the surface moisture concentration remains close to zero. The diffusion time scale is about 6.94 hours. The slab model predicts roughly 5.9 hours to reach 10% of the initial average moisture and about 12.4 hours to reach 1%. These numbers describe the same model used earlier and reveal its long drying tail. Doubling the half-thickness under otherwise identical conditions increases the time to the same remaining fraction by approximately fourfold, even when the surrounding gas is very dry.

Finally, examine energy and the wider process. Using an illustrative vaporization enthalpy of 2300 kilojoules per kilogram of water, removing approximately 1.98 kilograms requires about 4555 kilojoules, or 4.56 megajoules, for vaporization alone. The real system also heats the polymer and equipment and accommodates other energy flows. If observed drying takes much longer than the ideal model predicts, examine the actual pellet temperature, gas humidity, airflow distribution, agglomeration, and whether diffusivity changes as moisture falls. This approach connects measurable observations with specific physical steps rather than forcing every discrepancy into a single adjustable parameter.

Think it through: why does doubling airflow not necessarily halve drying time?

Airflow primarily affects gas renewal and heat and mass transfer near the surface. If those steps were slow, additional airflow can substantially improve drying. If the surface is already maintained sufficiently dry and the limiting step is internal diffusion, more airflow does little to shorten the internal route. Compare the drying curves before and after the change, and use particle size and temperature observations to identify the controlling process. An approximately proportional response within one operating range does not establish that the same response continues indefinitely.

Think it through: if heating lowers relative humidity, where did the water go?

If no water is added, removed, or condensed during heating, the gas composition can remain approximately unchanged at nearly constant total pressure. Relative humidity falls because its denominator, the saturation vapor pressure at the new temperature, increases. The gas has not lost water; it is farther from saturation at that temperature. This is why a drying system needs separate attention to temperature and dew point. They describe different aspects of the gas and cannot be substituted for one another.

With these ideas in place, a piece of drying or devolatilization equipment can be read through three connected questions: where the small molecules start, which distances and interfaces they must cross, and what carries them away afterward. A material balance establishes how much must leave. Transport and phase equilibrium determine how quickly removal can proceed and what residual level can be approached. Energy balances and material behavior then guide the choice of a workable process. Pellets, films, bubbles, and aqueous dispersions look very different, but this sequence of physical questions connects them within one understandable framework.
