# How a Melt Becomes an Object: Extrusion, Injection and Forming

Source: https://ml-biomat.com/tutorials/biomaterials-courses/pm14/en/
Language: en

Why do pipes, films, bottles and housings need different machines? Connect flow with shape fixation, compare extrusion and injection, calculate thickness, clamping and cooling, and follow the structures created by blowing, thermoforming, foaming and layerwise manufacturing.

## Move material into place, then make it stay

A plastic pipe must retain a consistent cross section over many meters. A phone housing needs thin walls, openings, and reinforcing ribs formed together. A bottle uses relatively little material to surround an empty space. All are polymer products, but they call for different forming methods. Process selection begins with three questions: how will material reach the required position, what force will deform it, and how will the shape survive removal or further transport? Equipment names describe different combinations of flow, heat transfer, molecular motion, and geometric constraint.

Heating gives a thermoplastic enough mobility to flow. Cooling slows molecular motion, promotes crystallization where applicable, and stabilizes the shape. Entangled chains also make the melt elastic, allowing recovery or swelling after it leaves a die. Thermosetting systems and conventional vulcanized rubbers often establish chemical crosslinks during shaping, producing networks that cannot flow away freely. Their final shape therefore depends on reaction progress as well as temperature. Heating, flowing, and cooling describe many thermoplastic processes, while other systems add chemical fixation.

Spreading warm syrup into a sheet provides a useful first analogy: arrange the material while it flows, then let it become firm. With polymers, chain orientation, crystallization, and residual stresses also need attention. Two objects with identical external dimensions can differ in warpage, transparency, or fracture behavior because they experienced different flow directions and cooling histories. Forming creates an internal structure while reproducing an external boundary.

Early plastics processing already confronted these linked requirements. The Hyatt brothers' 1872 celluloid patent combined a heated cylinder, plunger-driven transport, an outlet passage, and a closed mold, with a clamp resisting the force tending to separate the mold during filling. The apparatus differed from a modern reciprocating-screw machine, but it clearly separated softening, material delivery, and mold closure. That functional arrangement explains more about modern equipment than memorizing an invention date alone.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pm14/en/#en-s1)

Figure 1 · The Hyatt brothers’ 1872 patent combined thermal treatment, plunger delivery and mold clamping. This original functional sketch emphasizes the connected tasks rather than reproducing machine geometry.

Feedstock condition must suit the process. Hygroscopic resins need suitable drying; reinforced materials require attention to fiber breakage and orientation; heat-sensitive polymers need controlled exposure. Machine settings also differ from the states actually experienced by the material. Barrel temperature is not the temperature everywhere in the melt, hydraulic pressure is not cavity pressure, and coolant temperature is not mold-wall temperature. Identifying the measured quantity connects equipment readings to material behavior.

We will first follow continuous extrusion from a die into a long product, then examine cyclic injection into a cavity. Films, hollow objects, thermoformed sheets, foams, and additive manufacturing provide further combinations. Throughout, the useful questions are where forces act, where heat travels, where material can still move, and where structure has already become difficult to change.

## Extrusion: the die exit is an intermediate stage

An extruder continuously supplies melt to a head and a shaped die opening. A circular opening can produce a solid strand; an annular gap produces a tube; a broad narrow slit produces a sheet; and a more complex opening produces a profile. Sizing, cooling, hauling, cutting, or winding follow. The die organizes the initial flowing cross section, while downstream equipment holds the soft material until it can support the required shape. Equating the die opening with the final dimensions is therefore only a rough starting point.

Chains are sheared and stretched during passage through the die. Some recover after release from the constraint, producing die swell. A round extrudate can be wider than its opening, while a noncircular section can expand differently in different directions. Entry deformation, channel length, temperature, flow rate, and relaxation time all influence recovery. Rearrangement of the velocity profile at the exit also contributes. A resin name alone does not determine a single swelling ratio for every operating condition.

Diameter swell and area swellEq. 1

![Diameter swell and area swell](https://ml-biomat.com/static/agent-math/43f91a7aac6a58b20ce3234f.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Bᵈ | Diameter-based swell ratio | 1 |
| dₑ | Extrudate diameter at a specified position and state | mm |
| dᵈ | Circular die diameter | mm |
| Bᴬ | Extrudate-to-die cross-sectional area ratio | 1 |
| e、d、A | Labels for extrudate, die and area | 1 |

Reading the relationshipFor circular sections, area is proportional to diameter squared, so the area ratio is the square of the diameter ratio.

A worked exampleFor dᵈ = 2.0 mm and dₑ = 2.4 mm at the specified location, Bᵈ = 1.20 and Bᴬ = 1.44: diameter rises 20%, area 44%.

ConditionsCircular sections at defined measurement conditions. Record drawing, sizing and cooling states separately from free swell.

A swelling ratio must identify whether it compares diameters or areas. A 20% increase in diameter corresponds to a 44% increase in area. Measurement location matters too: dimensions immediately after exit, after free recovery, and after cooling can differ. Haul-off draws the section down, while cooling adds shrinkage. Free-extrusion swell measurements therefore describe a different condition from final dimensions on a line using traction and sizing equipment.

Pipe production places sizing and cooling devices after the annular die. Vacuum sizing or internal support helps control diameter, roundness, and wall thickness. Haul-off speed and mass output together determine how much material is assigned to each meter of product. At fixed output, faster withdrawal means less material per unit length. For a flat film of fixed width, this appears directly as reduced thickness. Thickness control connects output, density, line speed, and geometry.

Film thickness from mass conservationEq. 2

![Film thickness from mass conservation](https://ml-biomat.com/static/agent-math/74e9e74a97232270c1efc53f.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ṁ | Material mass per unit time | kg/s |
| ρ | Density at the thickness-measurement location | kg/m³ |
| b、h | Film width and single-layer thickness there | m |
| v | Line speed there | m/s |

Reading the relationshipWidth times thickness gives cross-sectional area; multiply by speed for volume flow and by density for mass flow. Rearrangement gives thickness.

A worked exampleṁ = 20 kg/h = 0.0055556 kg/s, ρ = 920 kg/m³, b = 0.50 m and v = 0.20 m/s give h = 0.000060386 m = 60.39 μm. Doubling speed with the other quantities fixed gives 30.19 μm.

ConditionsSteady uniform-equivalent flat film without trim loss. Evaluate quantities at the same section; use retained mass flow when edge trimming occurs.

The head must distribute incoming melt across the entire exit. A wide sheet die has different center and edge paths whose pressure losses need balancing. Supports in an annular head can split the melt into streams that subsequently reunite, leaving structural or visible traces. Spiral-mandrel arrangements distribute and overlap flow around the circumference. The objective is appropriate velocity, temperature, and residence history across the exit, with limited stagnation and adequate reunion of separated streams.

At high rates, an extruded surface can change from smooth to finely rough and then to larger distortions. Elastic stresses, wall slip, surface extension near the exit, and temperature contribute differently across materials and flow regimes. Flow rate, melt temperature, die pressure, and the actual surface pattern help identify the relevant mechanism. Describing every irregularity as excessive viscosity misses changes in exit stress and interfacial conditions.

Cooling on an extrusion line also develops structure. Semicrystalline polymers can nucleate and grow crystals, while stretching changes orientation and crystallization pathways. Rapid cooling often limits particular scales of crystal growth, but crystallinity, crystal size, transparency, and toughness do not follow one universal relation. Product evaluation should distinguish structures created by cooling and drawing from differences already present in the resin.

## Films: distinguish stretching in two directions

Blown-film extrusion draws a thin tubular melt away from an annular die while internal gas expands its diameter. Air cooling progressively stabilizes the tube, which is then collapsed, passed through nip rolls, and wound. It resembles an inflated balloon, but material continuously enters and leaves. Circumferential expansion and axial haul-off jointly change thickness and orientation. Bubble diameter, line speed, cooling, and extrusion output must remain coordinated.

The blow-up ratio compares bubble diameter with a reference die diameter and describes circumferential expansion. An axial draw ratio can compare downstream speed with speed at a defined reference section. The flattened width is not the bubble diameter: the two flat sides together correspond to the tube circumference, so layflat width is approximately half that circumference. Distinguishing these dimensions also prevents confusion between single-wall film thickness and the combined thickness of two collapsed layers.

Inflation, axial draw and single-wall thicknessEq. 3

![Inflation, axial draw and single-wall thickness](https://ml-biomat.com/static/agent-math/3edef1447001e77f07acc267.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| BUR | Bubble-to-reference diameter ratio | 1 |
| Dᵇ、D₀ | Bubble and reference outlet diameters | mm |
| λz | Axial speed ratio | 1 |
| vᵇ、v₀ | Speeds at stabilized bubble and reference section | m/s |
| hᵇ、h₀ | Single-wall thicknesses at the two sections | mm |
| ρᵇ、ρ₀ | Material densities at the two sections | kg/m³ |
| bflat | Layflat width of the collapsed tube | mm |
| π | Circle constant | 1 |
| b、0、z、flat | Labels for bubble, reference, axial and layflat | 1 |

Reading the relationshipThin-tube mass flow is density times circumference, wall thickness and speed. Equal flow at both sections gives the thickness relation. The two layflat sides together span the original circumference.

A worked exampleD₀ = 100 mm and Dᵇ = 250 mm give BUR = 2.5; v₀ = 0.020 m/s and vᵇ = 0.20 m/s give λz = 10. With h₀ = 1.0 mm and equal densities, hᵇ = 0.040 mm = 40 μm; bflat = 392.70 mm.

ConditionsSteady thin axisymmetric tube without mass loss. h₀ and v₀ belong to the same actual reference section; retain density changes and account for exit state when using die-gap data.

The relation treats the tube wall as thin. Circumference multiplied by thickness gives its material cross-sectional area; multiplying by speed and density gives mass flow. At unchanged density, circumferential expansion by 2.5 and axial drawing by 10 reduce thickness to one twenty-fifth of its reference value. Reference thickness and speed refer to a specified actual section. Substituting the metal die gap directly requires consideration of swelling and local flow. Conservation establishes the main connection, while cooling, stability, and output fluctuations determine the achieved thickness distribution.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pm14/en/#en-s3)

Figure 2 · Mass conservation in a thin blown-film tube. Circumferential expansion by 2.5 and an axial speed increase by 10 reduce single-wall thickness to 0.040 mm. Geometry illustrates the mechanism rather than actual wall-thickness scale.

A visible transition on a semicrystalline film bubble commonly accompanies crystallization and stabilization and is called the frost line. It is not a universal line of fixed material temperature. Cooling changes the length still available for stretching and the time available for relaxation and crystallization. Longitudinal and transverse properties change accordingly. Blow-up and draw ratios cannot increase indefinitely: bubble stability, melt strength, cooling capacity, and product requirements constrain their useful combination.

Cast film emerges from a wide slit die and contacts a chill roll that removes heat and fixes the shape. The free span before contact can narrow at its edges, and edge thickening may occur. Longitudinal drawing during casting creates some orientation, but cast film is not automatically biaxially oriented film. A subsequent process can stretch a film sequentially or simultaneously along and across the machine direction at a suitable temperature, followed by heat setting or other stabilization. Different polymers follow different structural development routes.

Orientation places more chain segments or crystalline structures along preferred directions. Strength, stiffness, tearing, and thermal shrinkage can therefore become directional. Coordinated stretching in two directions can achieve a desired balance, while maximizing longitudinal strength alone may compromise transverse tearing or dimensional stability. Orientation is also capable of relaxing when heating restores molecular mobility. Shrink films deliberately use some of this stored tendency to recover.

Multilayer coextrusion assigns different functions to different melt layers: one may support sealing, another control gas transmission, and another provide stiffness. Flow proportions, layer thicknesses, adhesion, and viscosity compatibility determine whether the arrangement remains stable. Multiple layers can improve function while complicating separation or compatibility during recycling. Film assessment therefore connects average thickness, cross-web variation, layer structure, and test direction to the intended use.

## Injection molding: filling, packing, and cooling have different jobs

Injection molding sends a charge of melt into a closed cavity, removes one or more formed parts, and repeats the cycle. In a common reciprocating-screw machine, screw rotation plasticates the pellets and accumulates melt in front of the screw, causing it to move backward. During injection, the screw moves forward to discharge that charge. A nonreturn mechanism limits backward melt leakage. Rotational plastication and axial injection perform different functions, explaining why injection and continuous extrusion machines operate differently despite both containing screws.

Melt passes through the nozzle, sprue, runners, and gate before entering the cavity. The gate connects the feed system to the part, and its position and dimensions influence filling paths, local shear, pressure loss, and closure during cooling. Cold runners solidify and are removed; hot runners retain a heated melt supply. The mold also needs guidance, venting, cooling, ejection, and sometimes movable cores. An empty cavity alone does not describe the complete tool.

During filling, melt near a cooler wall slows and forms a surface layer. Hotter interior material continues forward and turns toward the wall at the advancing front, a pattern commonly called fountain flow. Chains and fibers develop orientation that varies through the thickness. Fronts flowing around a core or arriving from separate gates can reunite in a weld region. Its strength depends on temperature, pressure, molecular interpenetration, and gas removal. A visible line alone does not establish its mechanical quality.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pm14/en/#en-s4)

Figure 3 · Conceptual fountain flow. Hotter interior melt turns outward at the front and spreads toward the walls, while cooled surface material slows, leaving through-thickness differences in chain or fiber orientation.

Gate placement also connects manufacturing with service loading. A weak joining region near a screw hole or repeatedly flexed feature can shorten the life of an otherwise acceptable-looking component. Changing the gate, local flow path, or arrangement of holes and ribs changes where fronts meet and how fibers align. Tests should load the relevant product direction and identify where damage starts, connecting a filling pattern with the function the component must perform.

As the cavity approaches full volume, control changes from primarily following filling speed to a packing and holding stage. Material continues entering through the connected melt path to compensate for volume reduction during cooling and crystallization. Once the gate freezes, increasing external hold pressure can no longer supply that cavity effectively. An appropriate melt cushion ahead of the screw preserves room for pressure transmission and additional delivery. A screw that has mechanically bottomed out cannot be assessed from its pressure setting alone.

Pressurized melt tends to separate the mold halves. The clamping system supplies an opposing force related to cavity pressure and projected area in the opening direction. Hydraulic-cylinder pressure must be converted through the relevant force and area relationship before it represents melt-side pressure, and further losses occur between nozzle and cavity. Clamp selection therefore uses an appropriate cavity-pressure estimate, rather than multiplying any available pressure display by part area.

Estimate clamping from cavity pressureEq. 4

![Estimate clamping from cavity pressure](https://ml-biomat.com/static/agent-math/03fd2e27be1792ee54ddddd9.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Fopen | Resultant mold-opening force | N |
| p̄ᶜ | Mean cavity pressure over the loaded projection | Pa |
| Aproj | Loaded projected area of all relevant cavities and runners | m² |
| Fclamp | Selected effective clamping force | N |
| k | Engineering allowance factor selected for this example | 1 |
| open、c、proj、clamp | Labels for opening, cavity, projection and clamping | 1 |

Reading the relationshipPressure is force per area. Mean pressure times projected loaded area gives the opening force, with allowance selected for the machine, tool and operating state.

A worked examplep̄ᶜ = 30 MPa = 30 × 10⁶ Pa and Aproj = 0.015 m² give Fopen = 450000 N = 450 kN. Choosing k = 1.20 for this example gives Fclamp ≥ 540 kN.

ConditionsInitial force estimate; account for pressure distribution, holding peaks, tool stiffness and machine capability. k = 1.20 is an example, not a universal setting.

Cooling begins when melt contacts the wall and overlaps filling, holding, and part of the next charge's plastication. Once the part can support removal, the mold opens and the ejection mechanism releases it. Total cycle time also includes opening, closing, ejection, and other operations, so a cooling-time calculation alone does not predict the complete machine cycle. In a multicavity tool, filling and cooling should be coordinated because the slowest or least stable location can limit the whole process.

Short shots, flash, weld marks, and burns suggest different possible mechanisms. A short shot may reflect insufficient material, premature freezing, or excessive resistance. Flash can involve clamping, tool fit, or overfilling. Trapped gas near the end of filling can be compressed and heated. Following the sequence from supply through flow, venting, holding, and cooling helps isolate causes. A purposeful adjustment changes conditions around a specific explanation, checked against both process signals and the resulting part.

## Why thick sections cool slowly and parts distort

The surface touching the mold cools first. Heat in the center must cross already cooler polymer before it can leave. Polymers generally transfer heat much less effectively than metal tools, making wall thickness influential. Doubling thickness increases both the heat to remove and the distance it must travel. For an ideal plate whose two surfaces remain at equal constant temperature, a simple conduction model predicts cooling time approximately proportional to thickness squared.

Thermal diffusivity describes how rapidly temperature differences spread out within a material and can be expressed in square millimeters per second. Consider a plate initially at uniform temperature, with both faces immediately held at a fixed mold-wall temperature and constant thermal diffusivity. We ask when its center reaches a specified target. The conduction solution contains contributions that decay at different rates; retaining the slowest contribution at later times gives a practical approximation.

Approximate cooling time at a plate centerEq. 5

![Approximate cooling time at a plate center](https://ml-biomat.com/static/agent-math/02d21896fc6d340e9db5e405.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| tᶜ | Time for the center to cool to the target | s |
| H | Full plate thickness, not half-thickness | mm |
| α | Constant thermal diffusivity | mm²/s |
| Tᵢ | Initial uniform material temperature | °C |
| Tʷ | Constant wall temperature at both faces | °C |
| Tₑ | Target center temperature | °C |
| Rᵀ | Dimensionless temperature-difference expression | 1 |
| π、ln | Circle constant and natural logarithm, which inverts exponential decay | 1 |
| c、i、w、e、T | Labels for cooling, initial, wall, target and temperature | 1 |

Reading the relationshipThe leading late-time term of one-dimensional conduction gives exponentially decaying center temperature difference, with timescale H²/α. Inverting it produces the logarithm and geometric factors.

A worked exampleFor H = 2 mm, α = 0.10 mm²/s, Tᵢ = 240°C, Tʷ = 40°C and Tₑ = 100°C, Rᵀ = 4.24413 and tᶜ = 5.85854 s. At H = 4 mm, tᶜ = 23.43417 s.

ConditionsOne-dimensional plate conduction, constant surface temperatures, uniform initial temperature and constant α; a late-time leading-term approximation requiring Tʷ < Tₑ < Tᵢ. Excludes contact resistance, latent heat and reaction heat. Predicts a center-temperature criterion, not the full machine cycle.

The natural logarithm appears because the calculation reverses an exponential decay of temperature difference to solve for time. Temperature differences use the same scale, and their ratio is dimensionless. As the target approaches wall temperature, removing the remaining difference takes progressively longer. This model predicts when an ideal plate center reaches a chosen temperature. Actual ejection also depends on stiffness, ejection forces, geometry, and residual stress; a temperature from one material heat-resistance test does not automatically define an acceptable ejection point for every component.

Initial temperature 240°C; target center 100°C; diffusivity 0.10 mm²/s. Solid line: selected wall temperature. Gray dashed line: 40°C reference.

[Figure: Plate-model cooling time versus thickness](https://ml-biomat.com/tutorials/biomaterials-courses/pm14/en/#en-s5)

Compare wall thickness and mold temperature using the plate-conduction approximation. All cases share the same target center temperature, with fixed axes showing the thickness-squared effect.

The interaction fixes initial temperature at 240°C, target center temperature at 100°C, and diffusivity at 0.10 square millimeters per second while varying thickness and wall temperature. Increasing thickness raises the time sharply. A warmer wall reduces the cooling driving force and lengthens the time to the same target. Warmer molds may nevertheless improve surface replication, welding, or crystallization, so those outcomes must be considered together. Thick bosses, rib roots, and corners can also remain hot longer than the nominal thin wall; local geometry can matter more than simply increasing coolant supply.

Cooling generally reduces volume, with crystallization providing an additional contribution in semicrystalline polymers. Packing changes how much mass remains in the cavity, but final dimensions still depend on pressure history, temperature, and structure. A shrinkage value should specify the reference tool dimension, measurement direction, elapsed time after molding, and conditioning environment. Fiber orientation can produce different longitudinal and transverse contraction, making one percentage inadequate for every region of a part.

Dimensional shrinkage and tool compensationEq. 6

![Dimensional shrinkage and tool compensation](https://ml-biomat.com/static/agent-math/04a636b0a172b3605aedc1f2.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| s | Linear shrinkage normalized by mold dimension | 1 |
| Lₘ | Mold dimension at the specified reference state | mm |
| Lₚ | Part dimension measured at defined time, environment and direction | mm |
| m、p | Mold and part labels | 1 |

Reading the relationshipNormalize the dimensional reduction by mold size. Rearrangement estimates tool size from expected shrinkage.

A worked exampleLₘ = 100 mm and Lₚ = 98.5 mm give s = 0.015 = 1.5%. For a 100 mm target and the same directional s, Lₘ = 100/0.985 = 101.523 mm.

ConditionsCompare dimensions in the same direction and defined states. Actual shrinkage varies with structure and conditions; constant s illustrates compensation.

If the center of a thick region contracts while the skin can move inward, a surface sink can form. If the skin is already stiff, an internal void may develop instead. Unequal shrinkage constrained by connected regions produces warpage and residual stress. Residual stresses remain internally balanced after external loads are removed and may relax during heating, environmental exposure, or cutting. Additional packing can reduce some sinks, while excessive packing creates other stress problems. Process and part geometry need to be developed together.

Cooling-channel layout determines where heat can actually be removed. Slender cores, deep cavities, and locally thick regions may need different arrangements. Material can also continue crystallizing, absorbing moisture, or relaxing after demolding, changing dimensions further. Precision measurements therefore use defined timing and conditions. Connecting wall design, cooling paths, tool compensation, and material state makes dimensional accuracy an interpretable outcome rather than an isolated trial value.

## Compression, calendering, and thermoforming

Compression molding places a measured charge in a cavity and closes the tool under pressure, spreading material into the required space. Thermosetting compounds commonly flow and cure in a heated tool, rubbers can vulcanize there, and heated thermoplastic composite sheets can be pressed and cooled. Chemical curing and physical cooling fix shape through different mechanisms. Charge placement, layup, and flow distance influence reinforcement orientation, joints, and local thickness.

Compression supplies force across a relatively large area, unlike injection through a small gate. For long-fiber sheets, limiting unnecessary travel helps preserve and arrange reinforcement, although material must still reach detailed regions. Venting, temperature distribution, and cure progression remain important. A formed surface does not establish that the interior has completed reaction or contains no trapped gas. Removal conditions follow the development of internal temperature and structure.

Calendering uses a sequence of rolls to turn plasticized material into continuous film or sheet, or to coat a fabric. Gaps, roll speeds, and temperatures jointly control flow and thickness. PVC sheet and rubber sheet are familiar applications, with conditions adapted to each formulation. Even a nominally fixed gap does not guarantee uniform thickness: loaded rolls deflect, temperature changes dimensions, and the material recovers after leaving the nip. Equipment compensation and online thickness measurements address these effects.

Thermoforming heats an existing sheet until it can stretch and then shapes it against a tool. Vacuum forming lowers gas pressure on one side so that higher pressure on the other pushes the sheet toward the mold. Suction is a convenient description; the physical force comes from a pressure difference. Pressure forming can add higher pressure on the opposite side, while a mechanical plug can pre-distribute the sheet into a deep cavity. Insufficient heating resists drawing, whereas overheating promotes sagging and local thinning.

Pressure-difference force in thermoformingEq. 7

![Pressure-difference force in thermoforming](https://ml-biomat.com/static/agent-math/ffa6ef4f12508e55a13a4831.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| F | Resultant pressure force on a projected flat area | N |
| Δp | Pressure difference across the sheet | Pa |
| A | Projected area considered | m² |
| phigh、plow | Higher and lower absolute gas pressures | Pa |
| Δ、high、low | Difference and high/low pressure labels | 1 |

Reading the relationshipOpposing face pressures subtract to give net pressure; multiply by projected area for the corresponding resultant force.

A worked exampleWith 100 kPa outside and 20 kPa inside, Δp = 80 kPa. At A = 0.010 m², F = 800 N. Vacuum alone against a 100 kPa atmosphere has an ideal difference limit approaching 100 kPa.

ConditionsApproximately uniform gas pressures. Membrane tension, mold contact and large deformation require additional treatment; pressure forming can increase the high-side pressure.

With ordinary atmospheric surroundings, vacuum alone has a pressure-difference limit set by the external atmosphere. A stronger pump cannot increase it without bound. Deep corners also require substantial local area expansion. Approximately constant material volume means that increased area produces reduced thickness, and regions touching a cold mold first lose their remaining stretchability sooner. Prestretching, plug assistance, and zoned heating redistribute deformation rather than merely increasing the pressure difference.

Thermoforming suits packaging trays, inserts, and many larger thin shells, using sheet feed to create contours rapidly. Peripheral trimming and thickness variation remain part of the process. Choosing between injection and thermoforming requires considering depth, detail, thickness, production volume, and material use together. Comparing the geometry and properties that each method can preserve is more useful than ranking methods with a general label of technological advancement.

## Hollow and cellular structures: involving gas

Extrusion blow molding begins with a hot tubular parison. Split mold halves close around it and pinch the ends, after which internal gas expands the soft wall against the cavity. Cooling and demolding produce a bottle, drum, or other hollow component. The parison can sag under its own weight, while inflation stretches different regions by different amounts. Parison programming adjusts thickness during extrusion to allocate more material where greater subsequent stretching is expected. The pinch-off, shoulder, and handle regions need particular attention.

Injection blow molding first creates a preform with a controlled neck and wall distribution. Injection stretch blow molding adds axial stretching by a rod alongside circumferential inflation. PET beverage bottles commonly follow this route, with preforms stretched in a suitable thermal window while orientation and crystallization develop. Blowing pressure depends on material, method, and geometry; a pressure used in one extrusion-blow example is not a universal condition. Continuous blown-film bubbles also differ from individual bottles formed inside closed tools.

Rotational molding places a measured amount of powder or liquid formulation inside a mold that rotates slowly about two directions during heating. Material repeatedly contacts the hot inner surface and progressively forms a fused wall, followed by cooling and removal. Motion under gravity and thermal contact are central; ordinary rotomolding is not a high-speed centrifugal process. Charge mass influences average thickness, while rotation pattern, temperature, and fusion time affect coverage and porosity. Large tanks and other hollow objects can use this route with suitable cycle and thermal control.

Rotational molding and slush molding are related but distinct. In a typical slush process, flowable material or powder contacts a hot tool and forms a layer; excess material that has not formed the wall is then removed before further fusion or cure. Rotational molding generally retains the measured charge to make the complete wall. Distinguishing a retained charge from excess material drained after layer formation clarifies thickness control and avoids treating every rotating or rocking tool as the same process.

Foaming creates many gas-filled cells within a polymer. A physical blowing agent may be gas dissolved in the melt that separates as pressure or other conditions change. Chemical blowing agents release gas through reaction. Cells must nucleate, grow, and become stable at an appropriate time. A melt that flows too easily may allow wall thinning, coalescence, or collapse, whereas premature solidification limits expansion. Foaming coordinates gas supply, dissolution, pressure, viscoelasticity, and cooling or cure.

Void fraction and volume expansion from densityEq. 8

![Void fraction and volume expansion from density](https://ml-biomat.com/static/agent-math/fe890bd8afce996ed813c879.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| φᵥ | Gas-filled void volume fraction | 1 |
| ρf | Bulk foam density | kg/m³ |
| ρs | Density of the corresponding solid matrix or compound | kg/m³ |
| Eᵥ | Foamed-to-solid volume ratio at equal solid mass | 1 |
| v、f、s、V | Labels for void, foam, solid and volume | 1 |

Reading the relationshipNeglecting gas mass, the density ratio gives the fraction of volume occupied by solid. The remainder is void. Equal solid mass occupies volume inversely proportional to density.

A worked exampleWith ρs = 1200 kg/m³ and ρf = 300 kg/m³, φᵥ = 0.75, or 75% void, and Eᵥ = 4. The same solid mass occupies four times its original volume.

ConditionsNegligible gas mass and a defined solid composition/density. Account for fillers, crystallinity and gas mass when significant. Density alone does not identify cell size or connectivity.

Density reduction describes the overall increase in void space but does not specify cell size, connectivity, or mechanical behavior. Open-cell structures allow gas movement through connected passages and can support acoustic absorption or permeability. Closed cells restrict such movement, while insulation still depends on solid conduction, gas, radiation, and aging. Expanded polystyrene beads subsequently fused in a mold also follow a different route from continuously extruded foam board. Density, cellular structure, skin, and loading direction belong together in a useful comparison.

## Layerwise manufacturing and process selection

Additive manufacturing divides a three-dimensional shape into layers and places or solidifies material progressively. Material extrusion deposits thermoplastic melt through a nozzle, creating adjacent paths that cool. Polymer powder-bed processes selectively fuse regions of successive powder layers. Vat photopolymerization reacts a liquid photosensitive formulation in selected regions. Their common layerwise construction uses different fixation mechanisms: melt cooling, particle fusion, or light-initiated chemistry. Feedstock selection and finishing therefore differ too.

A central issue in extrusion-based printing is whether adjacent paths develop effective joints. Newly deposited melt needs intimate contact with the previous layer, followed by chain interdiffusion while molecular mobility remains available. Rapid cooling shortens welding time; higher temperature changes shape retention and degradation risk. Semicrystalline materials add competition between crystallization and interface healing. Research connecting thermal imaging, rheological measurements, and interfacial fracture tests links visible layer boundaries to molecular motion and load-bearing performance.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pm14/en/#en-s8)

Figure 4 · Physical welding between deposited thermoplastic layers. Chain interpenetration and entanglement assist load transfer; the sketch shows molecular interpenetration rather than newly created covalent bonds.

In photopolymerization, light is absorbed as it travels through resin. The initiating system generates reactive species that connect monomers or oligomers into a network. Scanned spots and patterned exposure of an entire layer provide different illumination strategies. Resolution also depends on optical propagation, reaction spread, and resin movement. Removing uncured resin, completing suitable light or thermal treatment, and checking dimensions establish the final material state. A recognizable shape can appear before conversion and properties reach their intended values.

Polymer powder-bed manufacturing needs adequate fusion in selected regions while surrounding powder supports the object and remains removable. Particle size and shape influence spreading, temperature distribution affects fusion and warpage, and repeated heating changes unused powder's subsequent behavior. Reuse therefore requires control of powder condition. Compared with injection molding, layerwise methods reduce some dedicated-tool requirements while adding control tasks associated with interfaces, deposition paths, and local thermal histories.

Geometry and production volume provide an initial process shortlist. Continuous pipes, strands, and profiles suggest extrusion. Repeated detailed solid or thin-walled components suggest injection molding. Hollow containers invite comparisons between blow molding and rotational molding. Sheet-derived shells suggest thermoforming, while small batches with complex internal structures may suit layerwise manufacturing. The shortlist then narrows through material requirements for flow, melt strength, reaction, and cooling.

Final evaluation returns to how the product works. A dimensionally correct housing still faces assembly loads and environmental changes. Transparent packaging needs suitable thickness and transmission properties. A tank needs appropriate wall distribution and sound joining regions. Sampling direction, test temperature, conditioning, and service conditions connect processing with performance. Orientation, crystallinity, pores, and interfaces are the internal material structures performing the product's functions.

Forming a polymer object therefore involves a connected sequence of choices: when to give molecules mobility, how flow places material, when cooling, crystallization, or crosslinking fixes it, and what stresses and directions remain. This sequence provides a way to understand unfamiliar equipment and shapes through their underlying mechanisms rather than memorizing each process as an isolated name.
