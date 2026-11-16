# How Reactors Shape Materials: Flow, Mixing and Scale-Up

Source: https://ml-biomat.com/tutorials/biomaterials-courses/pe05/en/
Language: en

Why can the same formulation produce a different material in different equipment? Follow the reactants through vessels, tubes, films and screws, then explore how flow, heat transfer and mechanical action change during scale-up.

## A formulation needs a suitable journey

When making batter, the same flour and water can leave different-sized lumps depending on addition order, stirring and resting time. Polymer manufacture also depends on processing history, although the changes involve molecular bonding, heat transfer, phase formation and long-chain motion across several scales. A formulation specifies the ingredients. Equipment and operation determine where those ingredients meet, how temperature develops, how small molecules escape and whether the material can still move after its viscosity rises. A reactor therefore does more than contain a reaction: it provides a controlled journey through which the material acquires its structure.

That journey can remain visible in the final product. A small fraction held too long in a hot region may undergo chain scission or discoloration. Monomers that fail to mix quickly near a feed point can form chains with locally different compositions. Frequent droplet coalescence in a suspension can change the size of the resulting particles. The same nominal chemistry can operate in different vessel shapes, but its temperature, concentration and flow distributions need not be the same. Understanding a reactor starts with how it organizes those distributions, before memorizing equipment names.

Three material states provide useful starting points. A low-viscosity solution is relatively easy to circulate with an impeller, and the moving liquid transports heat towards the wall. A dispersion containing particles or droplets also needs appropriate suspension and size control: weak circulation can allow settling, while strong local stresses can break aggregates or change droplets. A viscous melt behaves more like thick syrup. Much of it may fail to move with a small impeller, and material near the wall may renew slowly. These systems give different meanings to “good mixing.” Equipment selection becomes clearer once the desired physical result is specified.

The early discovery of polyethylene illustrates how apparatus opens access to new chemical conditions. In 1933, Reginald Gibson and Eric Fawcett obtained a waxy polymer of ethylene during high-pressure experiments. Surviving apparatus includes a pressure vessel, pressurizing components and temperature-control equipment, showing how the discovery depended on achievable physical conditions as well as starting chemicals. Subsequent polyethylene manufacture developed different routes in which reaction mechanism, catalyst and equipment were designed together. The historical lesson is the connection between a material and its accessible pressure–temperature environment, rather than a particular experimental condition as a universal recipe.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe05/en/#en-s1)

Figure 1 · A modern functional schematic related to the discovery of polyethylene: pressurization, measurement, containment and temperature control act together. The components are organized by function to show how apparatus maintains the reaction conditions.

A polymerization unit can be read by tracing three routes. The material route includes feed, reaction space, product and volatile outlets. The energy route includes heating, cooling and mechanical work. The motion route includes bulk circulation, local shear and surface renewal. Then ask how these routes change as polymerization proceeds: viscosity, density, phase state and heat generation can all evolve. A flow pattern that works early in the process may become ineffective later. This is one reason industrial manufacture often uses different equipment for successive stages of material formation.

## Vessels, tubes and columns create different residence histories

A stirred vessel is readily pictured as a pot with an impeller circulating its contents and a wall or coil transferring heat. Batch operation charges a quantity of material, allows it to react and then discharges it. Continuous operation feeds and withdraws material at the same time. In a well-mixed continuous vessel, newly entering material quickly encounters material that has already spent time reacting. The outlet consequently contains a range of residence histories. Batch and continuous describe operating modes; perfect mixing is a flow approximation. The external shape alone establishes neither mode nor ideal flow behaviour.

The simplest time scale divides the volume held in the equipment by the volume flowing through it each second. A larger water tank requires more time to pass an amount equal to its contents at the same flow rate. This ratio is called space time. Under appropriate density and effective-volume conditions it also gives mean residence time, but the mean does not imply that every parcel remains for exactly that duration. Bypasses, slowly exchanged regions, recirculation and velocity differences spread the histories. Choosing a reactor therefore requires attention to the distribution as well as its average.

Volume and throughput define a time scaleEq. 1

![Volume and throughput define a time scale](https://ml-biomat.com/static/agent-math/31049458aee149618e22e158.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| τ | Space time | s |
| V | Effective reaction volume occupied by material | L |
| q | Volumetric feed flow at the corresponding conditions | L s⁻¹ |

Reading the relationshipDividing inventory volume by volume entering each second gives the time to pass an amount equal to the inventory. It uses net throughput, not repeated internal impeller pumping.

A worked exampleAn effective volume of 100 L at 0.5 L/s gives 200 s, or about 3.33 min. Doubling flow to 1 L/s at the same volume gives 100 s.

ConditionsIt corresponds to mean residence time for steady, approximately constant-density flow that accesses the stated effective volume. The residence distribution additionally reflects flow structure, backmixing and poorly exchanged regions.

Vertical stirred vessels offer a compact arrangement. Horizontal equipment can maintain a shallower layer of viscous material and use a rotor to expose and renew a larger surface. Horizontal orientation alone does not establish effective devolatilization: fill level, vapour space, rotor geometry and vacuum conditions matter. For a process that must remove water, solvent or residual monomer, interfacial area can be as important as reaction volume. Filling the vessel more completely increases material inventory but may reduce the space needed for vapour movement and surface renewal.

A tubular reactor carries material along an extended path. Separate sections can exchange heat or receive additional feed. A narrow tube provides a relatively large heat-transfer area per unit volume, useful for some strongly heat-releasing processes. Increasing viscosity raises flow resistance, however, and deposits can narrow the passage. The ideal plug-flow model assumes synchronized forward motion across each section, whereas real tubes can have velocity profiles, axial mixing and radial temperature differences. A tube may contain no moving impeller yet still include static mixing elements that use pressure-driven flow to divide and rearrange the material.

A loop reactor joins tubing into a circulating path. A pump repeatedly moves material around the loop while fresh feed enters, product leaves and heat is exchanged. Circulation flow is generally different from net production flow; one parcel can complete many circuits before leaving. Strong circulation helps transport particles and renew fluid at heat-transfer surfaces. The overall residence behaviour may resemble a mixed system more closely than a single-pass ideal tube. Treating every tubular geometry as plug flow would overlook recirculation, which is central to this equipment's operation.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe05/en/#en-s2)

Figure 2 · Four ways to organize material movement. Arrows show main transport or circulation and P marks the loop pump. Geometry and flow tasks are shown; actual mixing and residence distributions depend on internals and operation.

A polymerization column uses height to organize a continuous process. Material can move mainly under gravity and pass through zones with different temperatures or internal components. Agitators, distributors and withdrawal equipment affect radial mixing and axial backmixing, so a column is not automatically an ideal plug-flow reactor either. As chains grow and viscosity rises, the bottom section may require stronger discharge equipment. An extended vertical path helps arrange a sequence of treatments. Its success depends on whether material actually encounters the intended sequence and whether heat and volatile products can leave each region effectively.

## Renewing surfaces when the material becomes viscous

A viscous polymer can flow under mechanical forcing while small molecules inside it still take a long time to reach a free surface. Imagine a volatile substance dispersed through a large mass of thick syrup. Molecules near the surface can escape first, whereas those deep inside have a longer transport path. Spreading the same material into a thin layer shortens that path and increases surface area per unit volume. Thin-film equipment uses both effects, replacing a large bulk region with films that are continually formed and renewed.

The characteristic diffusion time scales with the square of distance. Under otherwise equal conditions, reducing a transport distance tenfold can reduce the corresponding diffusion time a hundredfold. The square reflects random molecular motion: molecules take many steps in changing directions, so net displacement grows more slowly than total path length. A film therefore helps by shortening the distance to an interface rather than by automatically making each molecule move faster. Temperature and composition can also change the diffusion coefficient, but these are separate contributions that can be analysed alongside geometry.

A thin layer shortens the diffusion pathEq. 2

![A thin layer shortens the diffusion path](https://ml-biomat.com/static/agent-math/0255f6c14ccc65e878c39c65.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| t_{D} | Characteristic diffusion time scale | s |
| ℓ | Representative diffusion distance | m |
| D | Molecular diffusion coefficient under the stated material conditions | m² s⁻¹ |
| ∼ | Scaling relation; geometry and the chosen removal fraction determine the prefactor | 1 |
| ℓ² | Distance squared, meaning distance multiplied by itself | m² |

Reading the relationshipMean-square displacement in random molecular motion grows with time, so the time associated with a longer distance scales with distance squared. Different diffusion boundaries give different prefactors while retaining this length-squared scale.

A worked exampleFor D = 10⁻¹⁰ m²/s, a 1 mm distance gives a time scale of 10000 s; 0.1 mm gives 100 s. These compare scales rather than specifying an exact removal fraction.

ConditionsA representative constant diffusion coefficient and diffusion-dominated internal transport. Surface resistance, concentration-dependent D, bubbles and convection enter a fuller devolatilization model.

A wiped-film unit uses rotating elements to distribute material near a heated or cooled wall and renew the film. Rotor clearance, feed rate, viscosity and the vapour generated determine continuity, thickness and residence time. “Wiping” does not necessarily mean hard metal contact with the wall; designs can use contacting elements or a controlled clearance. Such equipment can remove volatile substances while reaction continues in the renewed layer. It is particularly useful when a process must combine high viscosity with the removal of small molecules from the polymer-rich phase.

A rotating-disc polymerization unit lifts melt from a pool onto discs or related elements. Films form on their surfaces before returning to the bulk or moving onward. Repeated lifting, spreading and drainage create fresh gas–liquid interface. When polymerization produces small molecules that must escape, this interface connects chemistry directly to mass transfer. Disc spacing, immersion, rotational speed and inventory affect the renewal process. Adding discs or increasing speed changes mechanical load, splashing, foaming and actual film thickness as well, so performance follows from the resulting flow rather than from component count alone.

In early polyester work, Wallace Carothers and Julian Hill found that water generated during chain formation limited further growth. Improving its removal allowed longer molecules to form. The chemistry links molecules bearing reactive groups at both ends, while the small product molecule can participate in the reverse process. Removing it changes the conditions for continued reaction. This history makes the contribution of equipment concrete: molecular structure determines what can react, and separation helps determine how far chain growth proceeds. Modern viscous polycondensation equipment combines reaction, interfacial renewal and small-molecule removal in the same spirit.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe05/en/#en-s3)

Figure 3 · Early polyester work connected small-molecule removal with chain growth. A thin layer shortens internal diffusion paths while the vapour side must also carry material away. This modern equipment schematic connects reaction equilibrium with transport paths.

A screw extruder brings another type of motion into reaction engineering. Rotating screws convey melt through a barrel, while particular elements promote distributive mixing, local deformation or material hold-up. Barrel sections can have different temperatures, and vents allow volatile substances to leave. When grafting, chain extension or another chemical transformation takes place inside, the processing machine also acts as a reactor. It can continuously handle viscous material and connect reaction with shaping or pelletizing. The process must coordinate reaction time, residence-time distribution, heat transfer and mechanical exposure, all of which contain more information than screw speed alone.

## Pressure, sealing and heat transfer belong together

Pressure can first be understood as normal force per unit area. Pressurized fluid acts on the vessel wall, end closures, connections and seal surfaces. Material and structural design transmit those forces. The pressure reference also matters. Absolute pressure is measured from vacuum, whereas gauge pressure is measured relative to the surrounding atmosphere. Phase-equilibrium and gas-state relationships generally use absolute pressure; mechanical loading across a wall depends strongly on the pressure difference. Confusing the references can make the same numerical value describe different physical states.

A thicker wall changes its load-carrying behaviour but also changes resistance to heat flow. Temperature can vary across a thick wall, so cooling the outer surface does not immediately produce an identical inner-surface response. Vessel materials also face corrosion, temperature and repeated loading. Thermal conductivity is consequently one consideration within a wider structural choice. High pressure does not prescribe one universal cooling arrangement. Jackets, internal surfaces, feed cooling and other routes depend on geometry, properties and process requirements. Similar-looking vessels can still send heat along quite different paths.

Seals can be distinguished by whether the adjoining components move relative to each other. Covers and flanges generally involve static sealing. A rotating shaft crossing the vessel boundary creates a dynamic sealing problem. The moving connection must restrict leakage while managing friction, wear and temperature; particles or solidifying material can affect performance. Magnetic drives change the connection between the rotating parts and the surroundings, while still requiring suitable torque transmission, thermal management and material compatibility. Sealing maintains the reaction environment while the equipment exchanges material, energy and mechanical motion with the outside.

A heat exchanger is a broad category, and a condenser is one member of it. Heat exchange may involve sensible heating or cooling, phase change, or both. Jackets, half-pipe jackets and internal coils transfer energy through a separating wall. A condenser turns vapour into liquid and releases the latent heat previously absorbed in vaporization. Wall-transfer power depends on conductance and temperature difference. Where stream temperatures vary along the equipment, the average driving force must reflect that variation. The useful temperature range of water, steam or a thermal oil also depends on pressure, phase state and equipment conditions.

From heat-transfer area to thermal powerEq. 3

![From heat-transfer area to thermal power](https://ml-biomat.com/static/agent-math/b8a35f04cd791b6f7c2b5ae9.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Q | Heat-transfer power in the stated direction | W |
| U | Overall heat-transfer coefficient | W m⁻² K⁻¹ |
| A | Effective area on the same basis as U | m² |
| ΔT_{eff} | Effective temperature difference appropriate to the flow and temperature distribution | K |

Reading the relationshipTransfer capacity per area and temperature difference, multiplied by area and driving difference, gives power. For nearly uniform temperatures on each side use their difference; for changing stream temperatures use an average appropriate to the exchanger flow arrangement.

A worked exampleFor U = 300 W/(m²·K), A = 2 m² and an effective difference of 20 K, Q = 12000 W, or 12 kW. Halving U through deposition halves the power if other conditions remain unchanged.

ConditionsU and the effective driving difference are representative over the interval. Phase change, fouling and properties enter the appropriate transfer model. Multipass or complex exchangers need the corresponding temperature-difference correction.

A condenser can have two distinct roles in a polymerization process. Part of the vessel liquid may evaporate, condense externally and return as reflux. This removes heat externally while maintaining the inventory of the returned components. If the purpose is to remove a polycondensation product or residual monomer, condensed liquid may instead be collected and withdrawn. Both flowsheets show vapour entering a condenser, but the destination of the condensate changes composition and reaction equilibrium. Reading the process therefore requires following the liquid after condensation as well as following the incoming vapour.

Latent heat and coolant warmingEq. 4

![Latent heat and coolant warming](https://ml-biomat.com/static/agent-math/58043c27dd7b0c983148d026.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Q_{cond} | Heat released by vapour condensation | W |
| ṁ_v | Mass condensation rate; the dot denotes amount per time | kg s⁻¹ |
| L_{v} | Magnitude of latent heat of vaporization at the relevant pressure and temperature | J kg⁻¹ |
| Q_{c} | Sensible heat absorbed by the coolant | W |
| ṁ_c | Coolant mass flow | kg s⁻¹ |
| c_{p,c} | Coolant specific heat capacity | J kg⁻¹ K⁻¹ |
| T_{c,o}, T_{c,i} | Coolant outlet and inlet temperatures | K |

Reading the relationshipCondensed mass per second times energy released per kilogram gives latent-heat power. Coolant mass flow times specific heat and temperature rise gives sensible uptake. At steady state with negligible other heat flows, the two powers balance.

A worked exampleA condensation rate of 0.01 kg/s with latent heat 2000 kJ/kg releases 20 kW. A coolant of specific heat 4 kJ/(kg·K) warming by 10 K needs a mass flow of 0.5 kg/s to absorb that power.

ConditionsThe first line approximates the latent contribution alone; vapour desuperheating, condensate subcooling and mixture condensation need additional terms. The second uses a single-phase coolant with approximately constant specific heat.

Whether vapour or coolant occupies the tube side of an exchanger depends on pressure drop, cleaning, corrosion, operating pressure and drainage. Vertical and horizontal arrangements also affect condensate drainage and gas–liquid interaction. Noncondensable gases can accumulate near condensing surfaces and add thermal and mass-transfer resistance. Removing these gases and draining liquid effectively help preserve usable area. These details explain why two units with the same nominal surface area can deliver different heat-removal rates in an actual process.

## Moving colour around is only part of mixing

A drop of dye in clear water can form ribbons that travel around the vessel during gentle stirring. The liquid is moving, yet regions of different concentration remain distinct. Further stretching and folding make the ribbons thinner, allowing molecular diffusion to erase differences over shorter distances. Mixing is therefore a connected sequence: bulk flow transports material, deformation divides and thins composition regions, and molecular motion completes local homogenization. A visually uniform colour does not necessarily establish uniformity at every small region where a rapid reaction is taking place.

In his pipe-flow experiments published in 1883, Osborne Reynolds used a fine coloured stream in transparent flowing water to make changes in motion visible. The band could remain orderly or become distorted and dispersed, depending on velocity, tube size and fluid viscosity. The Reynolds number brought these influences together so that flows at different scales could be compared. The experiment's power was to reveal an internal motion through an observable pattern. In a stirred vessel, impeller size and the motion generated by rotation provide corresponding length and velocity scales, leading to an impeller Reynolds number.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe05/en/#en-s5)

Figure 4 · Reynolds’ coloured-band experiments made flow states observable. These conceptual patterns show the difference between orderly transport and transverse mixing. Pipe and stirred flows use their respective velocity and length scales, with transition conditions determined experimentally.

Comparing stirred flow on one scaleEq. 5

![Comparing stirred flow on one scale](https://ml-biomat.com/static/agent-math/042af8e81da83fc97f9b036e.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Re_{M} | Impeller Reynolds number | 1 |
| ρ | Fluid density | kg m⁻³ |
| n | Impeller rotational frequency in revolutions per second | s⁻¹ |
| d | Impeller diameter | m |
| η | Newtonian dynamic viscosity, or an apparent viscosity under explicitly stated conditions | Pa s |

Reading the relationshipUsing a velocity proportional to nd and length d compares inertial and viscous scales. Density times frequency times diameter squared has the same units as dynamic viscosity, giving a dimensionless ratio.

A worked exampleFor ρ = 1000 kg/m³, n = 5 s⁻¹, d = 0.1 m and η = 0.001 Pa·s, Re_M = 50000. Changing only viscosity to 10 Pa·s reduces it to 5, giving very different flow behaviour at the same speed.

ConditionsFlow regime also depends on geometry and boundaries; pipe-flow transition values do not transfer directly to stirred vessels. Non-Newtonian liquids need a rheological description matched to the stirring conditions.

At lower Reynolds number, viscous effects are strong and flow can be smooth and orderly. At higher values, inertia is more prominent and complex turbulent motions may develop. Turbulence helps transfer large-scale differences to finer scales, but molecular diffusion still completes composition mixing at the smallest relevant scale. A viscous material can also mix effectively through organized stretching and folding without strong turbulence. Conversely, a visibly agitated vessel can retain slowly renewed regions. Mixing quality depends on the time needed to reach different locations and remove local differences, rather than on how active the free surface appears.

Chemical reaction introduces a competition between times. If two ingredients react immediately upon contact, they may form a particular structure or byproduct near the feed point before becoming well distributed. Later bulk mixing cannot automatically rearrange the bonds already formed into the structure expected from the average formulation. A slower reaction allows more time for homogenization. Comparing mixing and reaction times explains why feed position, addition rate and impeller arrangement can alter a product. Local monomer ratios, crosslinker concentrations and initiator distributions can all leave structural consequences through this route.

Mixing time can be measured by introducing a small tracer and recording how concentration or conductivity at several locations approaches its final value. The definition of “sufficiently mixed” must be specified, for example requiring all monitored signals to enter and remain within a chosen band around their final values. Sensor position, number and response affect the reported time. A mixing-time value is therefore most useful together with its measurement definition. For dispersions, settling, droplet breakup and particle-size changes require additional observations; one tracer-homogenization measurement does not represent all mixing objectives.

## Impeller shape changes the route through the liquid

Motion in a cylindrical vessel can be described as axial, radial and tangential: along the shaft, towards or away from the axis, and around the axis. These are coordinate directions used to describe the same moving liquid. If the contents mainly rotate with the impeller while axial and radial exchange remain weak, a conspicuous surface vortex can coexist with poor exchange elsewhere. Baffles often interrupt bulk rotation and redirect return flow. Their effects depend on flow regime, impeller and vessel geometry, and they also influence particle encounters and cleaning access.

Propellers and many pitched-blade impellers produce strong axial circulation, pushing liquid upward or downward with a return flow elsewhere. A flat-blade disc turbine typically produces a prominent radial discharge that divides into upper and lower circulation loops after reaching the wall. These are characteristic patterns rather than exact velocity fields determined by a name. Blade angle, diameter, bottom clearance, baffles and gas loading modify the flow. Comparing impellers starts with the objective: broad circulation, gas dispersion, particle suspension or intense local deformation. The geometry can then be assessed against that specific task.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe05/en/#en-s6)

Figure 5 · Typical flow tasks. Arrows emphasize main transport directions; actual three-dimensional flow depends on blade angle, baffles, fill level and rheology. The lower panel emphasizes ribbon-type axial exchange rather than exact manufacturing geometry.

Highly viscous liquids often need close-clearance anchors, frames or helical ribbons. Anchor and frame elements sweep a large cross-section and help renew near-wall material. A helical ribbon promotes axial transport and return flow between different heights. Its outer radius is compared with the vessel's inner radius, keeping radius and diameter distinct. A small clearance concentrates relative motion over a short distance, producing stronger local deformation. Whole-vessel circulation still depends on the complete geometry, however; vigorous motion around the wall alone does not establish good exchange in the central region.

Local shear is easy to picture using two parallel plates. Keep the lower plate fixed and move the upper plate. Layers of liquid between them have different velocities, and shear rate describes how rapidly velocity changes across the gap. In a Newtonian fluid, shear stress is proportional to shear rate, with dynamic viscosity as the proportionality coefficient. Shear stress is force parallel to a small surface per unit area, whereas normal stress acts perpendicular to that surface. Polymer liquids can develop additional normal stresses and elastic recovery, reflecting the storage and release of deformation energy by long chains.

How a velocity difference produces shear stressEq. 6

![How a velocity difference produces shear stress](https://ml-biomat.com/static/agent-math/0d35ed83b7248e1d574dfb2c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| γ̇ | Shear rate in simple shear; the dot denotes deformation rate | s⁻¹ |
| u, y | Velocity parallel to the plates and coordinate normal to them | m s⁻¹; m |
| du/dy | Change of velocity with normal distance, the velocity gradient | s⁻¹ |
| Δu, h | Relative plate velocity and gap thickness | m s⁻¹; m |
| τ_{xy} | Shear stress in the x direction on a surface normal to y, using the convention stated here | Pa |
| η | Dynamic viscosity | Pa s |
| F_{t}, A_{s} | Tangential force and the area over which it acts | N; m² |

Reading the relationshipNeighbouring layers move at different velocities. Velocity difference divided by separation measures deformation rate. Newtonian shear stress is proportional to that rate, while force per area supplies its mechanical definition.

A worked exampleA relative velocity of 0.1 m/s across 0.001 m gives 100 s⁻¹. At viscosity 2 Pa·s the shear stress is 200 Pa; over 0.01 m² this corresponds to a 2 N tangential force.

ConditionsSimple plate shear with an approximately linear velocity profile and Newtonian viscosity. It provides a local scale for mixer clearances. Shear thinning, elasticity and normal stresses require a fuller constitutive description.

A full three-dimensional stress description must identify both the orientation of a small surface and the direction of force acting on it. This is why stress components carry two indices. One identifies a surface direction and the other a force direction; different texts can use different index-order conventions, so the convention should be stated when needed. For equipment interpretation, the essential point is that the same fluid element can experience tangential dragging and normal loading. Impeller regions, narrow clearances and bulk return flows have different stress distributions, giving particles, droplets and chains different mechanical histories.

These distinctions matter for biomaterials as well as synthetic polymers. Breaking a rigid aggregate may require strong local action. Preserving soft microcapsules, cells or some protein assemblies requires attention to peak stresses, exposure time, interfaces and repeated visits to strongly deformed regions. Ordinary stirring does not affect every protein in the same way, and mean power alone cannot predict every kind of damage. Relating object size and structure to its flow history makes the mixing objective more specific and supports a more suitable choice of impeller or reactor configuration.

## Where the motor's work goes

Turning an impeller requires torque, the rotational action transmitted by the shaft. Torque multiplied by angular velocity gives mechanical power. If speed is stated as revolutions per second, it must be converted using the angle covered in one revolution. Electrical input power, shaft power and power actually transferred to the liquid differ because bearings and transmission components consume part of the input. A mixing-energy comparison therefore needs a defined boundary. The work transferred into the relevant fluid region is the quantity directly connected to its circulation, deformation and mechanical heating.

From torque to power delivered to the fluidEq. 7

![From torque to power delivered to the fluid](https://ml-biomat.com/static/agent-math/a43db9568f12480ba8fae0dd.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| P_{shaft} | Mechanical shaft power at the measurement location | W |
| n | Shaft frequency in revolutions per second | s⁻¹ |
| M | Torque transmitted at that shaft section | N m |
| π, 2π | Circle constant; radians per revolution | 1 |
| P | Mechanical power delivered to the fluid within the stated boundary | W |
| P_{loss} | Mechanical losses between the measurement section and the fluid | W |

Reading the relationshipWork per revolution is 2πM. Multiplying by revolutions per second gives power. Subtracting losses outside the fluid gives the portion entering the material.

A worked exampleAt n = 5 s⁻¹ and M = 2 N·m, shaft power is about 62.83 W. If mechanical losses within the stated boundary are 12.83 W, fluid power is 50.0 W.

ConditionsSpeed and torque use corresponding instantaneous values or suitable averages. Electrical motor input also includes electrical losses and requires conversion before being treated as shaft power.

Mechanical energy first supports motion and deformation and is eventually converted to heat through viscous dissipation. That eventual conversion does not make the intervening mixing unimportant: circulation and stretching occur while energy is being transferred. In a viscous material, mechanical heating can become a substantial part of the temperature balance. Barrel or jacket temperature then differs from the actual material temperature. Reactive extrusion particularly benefits from examining torque, throughput and temperature together, because increasing speed can improve distribution, shorten some residence histories and increase mechanical energy input at the same time.

Rushton, Costich and Everett's 1950 work on impeller power characteristics helped organize mixing data into comparable forms. Dividing power by a particular combination of density, rotational speed and impeller diameter defines the power number, which can then be related to Reynolds number and geometry. This separates major size and speed effects while retaining differences between impeller structures. Under geometrically similar, fully turbulent conditions, a given configuration can have an approximately constant power number over an appropriate range. The resulting relationship is especially useful for understanding how changing diameter and speed affects power demand.

Organizing power by flow scalesEq. 8

![Organizing power by flow scales](https://ml-biomat.com/static/agent-math/21ac489831fc61c31e35ad8b.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| N_{P} | Power number | 1 |
| P | Mechanical power delivered to the fluid | W |
| ρ, n, d | Density, rotational frequency and impeller diameter | kg m⁻³; s⁻¹; m |
| Re_{M} | Impeller Reynolds number | 1 |
| K_{L} | Laminar power coefficient for the specified geometry | 1 |
| η | Newtonian dynamic viscosity | Pa s |
| n³, d⁵ | Frequency cubed and diameter to the fifth power; exponents indicate repeated multiplication | s⁻³; m⁵ |

Reading the relationshipThe combination ρn³d⁵ has power units. Dividing by it gives the dimensionless power number. In fully turbulent flow at fixed geometry N_P can be approximately constant; in laminar flow it often varies inversely with Re_M, leading to different speed and size powers.

A worked exampleFor N_P = 5, ρ = 1000 kg/m³, n = 5 s⁻¹ and d = 0.1 m, P = 6.25 W. Within a constant-N_P range, doubling speed alone increases power eightfold.

ConditionsUse the relationship appropriate to the flow regime and coefficients for the actual impeller and vessel. Gassing, large free-surface deformation, baffle changes and non-Newtonian rheology can alter power behaviour.

High power does not necessarily mean rapid circulation throughout the vessel. One impeller can concentrate strong deformation in a small region, while another moves a larger volume at similar power. Pumping flow describes the liquid volume crossing a specified impeller-discharge section each second. It differs from net reactor throughput because the same material can pass the impeller repeatedly. A local pump analogy can also assign a head, representing mechanical energy per unit fluid weight. This head describes energy transfer; it does not directly measure the degree of molecular-scale mixing.

Circulation flow and pumping energyEq. 9

![Circulation flow and pumping energy](https://ml-biomat.com/static/agent-math/bf78b77520726963f66d5a3c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| q_{p} | Volumetric flow through the stated impeller-discharge section | m³ s⁻¹ |
| N_{Q} | Pumping number for the geometry and flow regime | 1 |
| n, d | Impeller frequency and diameter | s⁻¹; m |
| H | Mechanical energy per unit fluid weight, expressed as head | m |
| N_{H} | Head coefficient for the local pumping analogy | 1 |
| g | Gravitational acceleration, approximately 9.81 | m s⁻² |
| P_{h} | Hydraulic mechanical-energy flux across the specified pumping boundary | W |
| ρ | Liquid density | kg m⁻³ |

Reading the relationshipVelocity scale nd times area scale d² gives a flow scale. Head is energy per weight, so velocity squared divided by g has the required length units. Mass flow ρq_p times energy per mass gH gives hydraulic power.

A worked exampleWith N_Q = 0.7, n = 5 s⁻¹ and d = 0.1 m, q_p = 0.0035 m³/s. If N_H = 2, H is about 0.0510 m; at ρ = 1000 kg/m³, P_h is about 1.75 W.

ConditionsPumping and head coefficients require specified flow and measurement definitions. P_h is a local energy flux and need not equal total shaft power because other flow and dissipation contributions exist. Head is not a measure of micromixing.

Vessel volume divided by pumping flow provides a circulation time scale. It estimates how long an amount equal to the vessel contents takes to pass the chosen discharge section. Homogenization can require several circuits, and short return paths or slowly exchanged zones can alter the relationship. Pumping and dissipation therefore describe different aspects of the flow. Equipment comparison often needs pumping rate, power, measured mixing time and the response of the material being processed. A single power-per-volume value cannot make different flow patterns equivalent for every purpose.

Circulation time and measured mixing timeEq. 10

![Circulation time and measured mixing time](https://ml-biomat.com/static/agent-math/bbbdb6b44e96ce9e31904ad0.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| t_{circ} | Time scale for a vessel-volume amount to pass the impeller discharge | s |
| V | Liquid hold-up volume | m³ |
| q_{p} | Impeller pumping flow | m³ s⁻¹ |
| t_{mix} | Mixing time to the stated uniformity criterion | s |
| C_{m} | Empirical multiplier set by geometry, addition and measurement criterion | 1 |

Reading the relationshipVolume divided by internal pumping flow gives a circulation scale. Repeated circuits, flow splitting and local renewal determine homogenization; an experimentally established multiplier relates this scale to a mixing criterion.

A worked exampleWith V = 0.020 m³ and q_p = 0.004 m³/s, the circulation scale is 5 s. If the particular equipment and measurement criterion give C_m = 4, mixing time is about 20 s.

ConditionsThe second line is a condition-specific correlation, with no universal number of circuits assumed. Solid suspension, droplet size and reactive micromixing need their own assessments.

For continuous extrusion or another continuous viscous-material process, dividing net mechanical power delivered to the material by mass throughput gives specific mechanical energy. It expresses the energy received per kilogram and helps compare operation at different production rates. At a given power, reducing throughput increases energy per unit mass. Peak local stress and residence-time distribution still depend on equipment geometry. The quantity is useful for connecting energy consumption to material heating and for explaining why throughput, screw elements and rotation rate affect products in different ways.

Mechanical energy per kilogram of materialEq. 11

![Mechanical energy per kilogram of material](https://ml-biomat.com/static/agent-math/cd46f0ec3cc02c83a31fbf8c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| SME | Specific net mechanical energy input | J kg⁻¹ |
| P_{net} | Net mechanical power delivered to the material under consideration | W |
| ṁ | Continuous material mass throughput | kg s⁻¹ |
| ΔT_{mech} | Temperature-rise scale if all this mechanical energy becomes material sensible heat | K |
| c_{p} | Material specific heat capacity | J kg⁻¹ K⁻¹ |

Reading the relationshipEnergy delivered per second divided by mass passing per second gives energy per mass. Dividing again by energy needed per kilogram per kelvin gives the corresponding adiabatic sensible-heat scale.

A worked exampleFor P_net = 2 kW and throughput 0.01 kg/s, SME = 200 kJ/kg. At c_p = 2 kJ/(kg·K), complete retention as sensible heat corresponds to 100 K. Actual temperature also follows heat exchange, reaction and phase changes.

ConditionsUse steady operation or matched average power and flow. The temperature expression isolates the mechanical-energy scale and excludes reaction heat, external exchange and phase changes.

Using power, pumping flow and specific energy together leads to practical questions with measurable answers. A need for more global circulation may favour a change in impeller type or size. Breaking aggregates may call for controlled local deformation. Excessive temperature may arise from greater reaction heat, poorer removal or excessive mechanical input. Tracing each possibility to the quantity that represents it turns equipment comparison from a contest over motor size into an examination of the motion required for the intended material.

## Why scale-up cannot keep everything unchanged

Scaling every dimension of a small vessel by the same factor changes volume, surface area, velocity and energy demand together. Geometric similarity preserves ratios such as impeller diameter to vessel diameter and liquid height to vessel diameter. It does not by itself preserve dynamic behaviour. Even for the same liquid, different choices of rotational speed make Reynolds number, tip speed, power per volume and circulation time follow different scaling laws. Scale-up starts by identifying which process feature matters most, then examining the consequences for the other quantities.

Keeping Reynolds number constant requires speed to fall rapidly as the impeller grows. Keeping tip speed constant requires rotational frequency to fall inversely with diameter. Keeping power per volume constant under fully turbulent, constant-power-number conditions gives a different and less steep reduction. The requirements follow from different physical relationships and generally cannot all be satisfied during scale-up. Holding rotational frequency fixed is another choice, but it increases tip speed and power per volume, changing both mechanical demand and the material's exposure.

Different scale-up criteria require different speedsEq. 12

![Different scale-up criteria require different speeds](https://ml-biomat.com/static/agent-math/08a3f82a5078b579593f0ebb.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| S, a | Linear scale and frequency ratios; subscripts 1 and 2 denote original and enlarged equipment | 1 |
| d, n | Impeller diameter and rotational frequency | m; s⁻¹ |
| Re_{M} | Impeller Reynolds number | 1 |
| P, V | Fluid mechanical power and hold-up volume | W; m³ |
| P/V | Mechanical power per volume | W m⁻³ |
| u_{tip} | Impeller tip speed, circumference πd times frequency n | m s⁻¹ |
| q_{p}, t_{circ} | Pumping flow and circulation time scale | m³ s⁻¹; s |
| a³, S², S³, S⁵ | Powers of speed and size ratios inherited from the corresponding physical relations | 1 |

Reading the relationshipGeometric similarity makes volume scale as S³. Taking ratios of Reynolds, power, pumping and velocity relations cancels common properties and coefficients. Set the desired ratio to one and solve for the required frequency ratio.

A worked exampleAt S = 5, constant Reynolds number requires a = 1/25; constant tip speed requires a = 1/5; constant power per volume requires a = 5 to the power −2/3, approximately 0.342. The last choice gives 125 times total power, about 1.71 times tip speed and 2.92 times circulation time.

ConditionsGeometric similarity, identical density and viscosity, approximately fixed power and pumping numbers in the fully turbulent regime, and matching fill proportions. Recalculate properties and flow coefficients when these conditions change.

### Choose what to preserve during scale-up

[Figure: Choose what to preserve during scale-up](https://ml-biomat.com/tutorials/biomaterials-courses/pe05/en/#en-s8)

Original impeller diameter 0.1 m, vessel diameter and liquid height both 0.3 m, frequency 5 s⁻¹. Density 1000 kg/m³, viscosity 0.001 Pa·s, power number 5 and pumping number 0.7. Comparison assumes geometric similarity, equal properties and constant fully turbulent coefficients. Circulation time is volume divided by pumping flow; measured mixing time has its own criterion.

Set the linear scale factor to five in the interaction. Volume then increases by a factor of one hundred and twenty-five. First hold Reynolds number constant and observe the reduction in power per volume and the increase in circulation time. Then hold power per volume constant and compare tip speed and total power. A ratio of one means unchanged, ten means tenfold and one-tenth means one-tenth of the original value. The example uses one geometrically similar, fully turbulent impeller family with fixed power and pumping numbers, so the differences arise directly from scaling. If properties or flow regime change, those coefficients must be updated too.

The ratio of pumping flow to head is sometimes used as another similarity condition. With constant gravity and the same correlation forms, it is proportional to impeller diameter divided by rotational frequency. Preserving it therefore gives yet another speed–size relationship. The ratio has units, and neither of its components completely specifies mixing quality, so its meaning depends on the stated comparison. For a particular polymerization, preserving droplet size, achieving a specified mixing time or controlling local stress can be a more direct objective than preserving an unexplained ratio.

Heat introduces another scale dependence. Geometrically similar enlargement reduces external wall area per unit volume. Even if mechanical power per volume is held constant, reaction heat and changing viscosity can alter actual transfer. Additional heat-transfer area, external circulation, staged reaction or a changed feed history can address these changes. Volatile-removal processes must also scale surface renewal and vapour handling. Process scale-up thus reorganizes the relative times of reaction, transport, energy exchange and mechanical action, rather than simply running a larger vessel at a familiar speed.

Three products illustrate the resulting choices. A water-based latex needs effective circulation, dispersion stability and heat removal. A viscous polyester that must continuously release small molecules needs film renewal, transport on the vacuum side and a suitable chain thermal history. A melt undergoing rapid graft modification needs chemistry coordinated with screw transport, local mixing and vent position. All belong to polymer manufacture, yet they call for different process arrangements. The value of the reactor lies in creating the particular journey that produces the desired structure and properties.
