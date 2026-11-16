# When Reactions Heat Themselves: Thermal Balance and Stability in Polymerization

Source: https://ml-biomat.com/tutorials/biomaterials-courses/pe04/en/
Language: en

Start with a cup of curing resin and follow heat generation, transfer and reactant consumption. Historical insights, heat-flow diagrams and adjustable reactor models explain temperature recovery, state changes, polymerization autoacceleration and the consequences of scale-up.

## Why a cup of resin can keep getting hotter

A freshly mixed two-part resin can have quite different temperature histories when spread as a thin layer and when left in a deep cup. The thin layer has a large surface through which to exchange heat with its surroundings. Heat generated near the centre of the cup has a longer route to escape. At first, neither sample may show much change. Later, the resin in the cup warms and cures faster. Two processes are interacting: a chemical reaction releases energy, and that energy changes the reaction rate. Understanding this interaction explains why a process that behaves gently in a small container needs a fresh assessment of cooling and feeding when transferred to a larger vessel.

Temperature and heat must first be distinguished. Temperature describes a thermal state; heat is energy transferred because of a temperature difference. Raising a large tank of liquid by ten degrees requires far more energy than raising a small cup by the same amount. Heat capacity describes how much energy a system takes up for a given temperature increase. Water has a relatively large specific heat capacity, so heating a given mass of water requires substantial energy. A reaction mixture has its own heat capacity, contributed by solvent, monomer, polymer and sometimes the vessel wall. A thermometer measures temperature at a particular location. Its reading does not directly reveal the rate of heat generation throughout the vessel or the chemical energy still available for release.

Reaction heat also requires a molecular explanation. Breaking a chemical bond costs energy, whereas forming a bond releases energy. The net balance of all changes between reactants and products determines whether a reaction absorbs or releases heat. Polymerization joins small molecules into chains, but its heat effect varies with monomer structure, temperature and reaction pathway. Reaction enthalpy describes the heat associated with a specified amount of reaction under the stated conditions. By convention, an exothermic reaction has a negative reaction enthalpy. Taking its negative value therefore gives a positive heat-release quantity, which can be multiplied by the amount reacting each second.

From reaction rate to heat-generation powerEq. 1

![From reaction rate to heat-generation power](https://ml-biomat.com/static/agent-math/c924a8838a5d3e4bdbc52d75.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Q_{gen} | Heat-generation power | J s⁻¹ = W |
| ΔH_{r} | Molar reaction enthalpy for the stated reaction basis; negative for an exothermic reaction | J mol⁻¹ |
| r | Reaction-extent rate per mixture volume | mol L⁻¹ s⁻¹ |
| V | Reaction volume on the same basis as r | L |

Reading the relationshipMultiplying rate by volume gives moles of reaction per second; multiplying by heat per mole gives power. If the rate is defined by monomer consumption, enthalpy must use the same monomer basis. The minus sign makes exothermic generation positive.

A worked exampleWith ΔH_r = −70 kJ/mol, r = 0.002 mol/(L·s) and V = 10 L, consumption is 0.020 mol/s and generation is 1.4 kJ/s, or 1.4 kW.

ConditionsHere r is a volume-averaged rate. For several reactions, calculate and sum their contributions, retaining heat-absorbing reactions as negative generation terms.

The phrase “each second” matters. Suppose a batch releases one million joules in total. Spreading that release over an hour and concentrating it into ten seconds impose very different demands on cooling. The first corresponds to an average power of less than three hundred watts; the second reaches one hundred thousand watts. The total energy is unchanged, but the required rate of removal is very different. Temperature control therefore depends on when and where heat appears, as well as on the total reaction heat. An induction period, polymerization autoacceleration or a change in feed rate can reshape the heat-release curve. A table of reaction enthalpies alone cannot describe that evolving demand.

Imagine a vessel whose contents are well mixed. Reaction supplies heat, a jacket transfers heat to a coolant, and a continuous stream of colder feed must be warmed. Outgoing material carries energy away. If liquid evaporates, the departing vapour can remove latent heat as well. An energy balance places these contributions on the same basis. The amount left over changes the temperature of the vessel contents. In the following expression every term is a power, measured as joules per second, so the terms can be added and subtracted consistently. A constant temperature means that the energy flows currently balance; the reaction can still be proceeding rapidly.

The transient energy balanceEq. 2

![The transient energy balance](https://ml-biomat.com/static/agent-math/10898808a384d5a1009f0cae.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| C_{th} | Effective thermal capacity of the represented system | J K⁻¹ |
| T, T_{j}, T_{f} | Bulk reactor, effective jacket and feed temperatures | K |
| t, dT/dt | Time and instantaneous temperature-change rate; d denotes an infinitesimal change | s; K s⁻¹ |
| Q_{gen} | Net power generated by all included reactions | W |
| U | Overall heat-transfer coefficient based on area A | W m⁻² K⁻¹ |
| A | Effective heat-transfer area | m² |
| ρ | Liquid density on a litre-volume basis | kg L⁻¹ |
| c_{p} | Specific heat capacity at constant pressure | J kg⁻¹ K⁻¹ |
| q | Inlet and outlet volumetric flow rate | L s⁻¹ |
| Q_{other} | Other net heat-removal power, such as evaporation | W |

Reading the relationshipTemperature difference times UA gives wall-transfer power. The mass flow ρq multiplied by heat capacity and stream temperature difference gives sensible heat transport. Dividing the remaining power by thermal capacity gives the temperature-change rate. A hotter feed or jacket naturally makes its term a heat input.

A worked exampleFor a 20 kJ/K thermal capacity, 2 kW generation, 1 kW wall removal, 0.4 kW stream removal and 0.1 kW other removal leave 0.5 kW. The instantaneous warming rate is 0.025 K/s; unchanged rates for one minute would give a 1.5 K rise.

ConditionsThe liquid is well mixed, approximately constant in volume and properties, with approximately equal inlet and outlet mass flow. Include wall heat capacity only when its temperature follows the represented bulk sufficiently closely. Add external heating, stirring power and phase changes when needed.

Temperature rises when generation exceeds removal and falls when removal exceeds generation. Energy conservation gives this direction of motion, but it does not yet tell us whether a disturbance will grow. We must ask what happens after the temperature rises by one degree: how much more heat is generated, and how much more is removed? Comparing those increments reveals whether the change corrects itself or reinforces itself. Thermal stability is a property of this feedback around a particular state, rather than a property captured by a single temperature printed beside a material name.

## The route that heat takes out of a reactor

A cooling jacket can be pictured as a flowing layer wrapped around the vessel, but heat does not jump directly from the centre of the reaction liquid into that layer. It travels from the bulk liquid towards the inner wall, crosses the metal and then passes into the coolant. Deposited polymer can add another barrier. The situation resembles a route composed of several narrow passages: the overall carrying capacity depends on all of them. Widening a section that was already easy to cross may have little effect on the whole route. The passage here is a route for energy; the liquid itself does not have to pass through the metal.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe04/en/#en-s2)

Figure 1 · Heat passes through the liquid-side region, wall, any deposit and coolant-side region. Thicknesses are schematic. The total resistance is the sum of the parts; improving a major resistance usually has the greatest effect on this path.

An overall heat-transfer coefficient combines these contributions. For a relatively thin wall, with nearly equal inner and outer areas, the thermal resistances per unit area can be added. Their reciprocal gives the overall coefficient. A larger resistance allows less heat through at a given temperature difference. High metal conductivity and a thinner wall favour heat transfer, although vessel thickness also has pressure and structural requirements. Liquid-side flow, deposits and coolant conditions often change during operation. Writing the resistance contributions separately helps identify which part of the path actually limits removal and which improvement is likely to make a difference.

Thermal resistances in seriesEq. 3

![Thermal resistances in series](https://ml-biomat.com/static/agent-math/0bde2342ff220fe39083ea57.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| U | Overall heat-transfer coefficient | W m⁻² K⁻¹ |
| h_{i}, h_{o} | Inner-fluid and outer-coolant heat-transfer coefficients | W m⁻² K⁻¹ |
| ℓ_w | Wall thickness | m |
| λ_{w} | Wall thermal conductivity | W m⁻¹ K⁻¹ |
| R_{f} | Combined fouling/deposit resistance on the same area basis | m² K W⁻¹ |
| 1/U | Total resistance per unit area; reciprocal notation connects resistance to conductance | m² K W⁻¹ |

Reading the relationshipThe same steady heat flow crosses each layer, and the required temperature drops add. Hence the resistances add. Wall thickness divided by conductivity has the same resistance units as reciprocal convective coefficients.

A worked exampleWith h_i = 500 and h_o = 1000 W/(m²·K), wall thickness 0.005 m, conductivity 15 W/(m·K) and R_f = 0.0005 m²·K/W, total resistance is 0.003833 m²·K/W and U is about 261 W/(m²·K).

ConditionsThis expression uses a thin wall with nearly equal inside and outside areas. Thick cylinders or different area bases require area ratios and the cylindrical radial-conduction resistance.

Stirring does more than distribute reactants. If liquid remains beside the wall for a long time, a region with a temperature different from that of the bulk can develop. Stirring renews this liquid and carries energy towards the wall. An impeller may produce vigorous circulation in a low-viscosity fluid, yet the same speed can produce a very different flow after polymer concentration rises. Chain growth therefore connects chemistry to heat transfer: it changes the reaction environment and can also make heat harder to remove. Under some conditions both changes push the temperature upwards, so measuring reaction kinetics without considering evolving transport can miss an important part of the process.

Rotational speed by itself is a poor way to compare different vessels. Small and large impellers rotating at the same frequency move liquid over different distances. Water and a concentrated syrup can have similar densities but quite different flow behaviour. Engineers organize these effects using dimensionless groups built from density, viscosity, speed, size, heat capacity and thermal conductivity. Their units cancel, leaving ratios that compare physical mechanisms. The Reynolds number compares inertial and viscous effects. The Prandtl number compares momentum diffusion with thermal diffusion. The Nusselt number relates convective heat transfer to conduction across a chosen length scale.

Dimensionless groups for stirred heat transferEq. 4

![Dimensionless groups for stirred heat transfer](https://ml-biomat.com/static/agent-math/fb5b30bea56515eac208fc98.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Re_{M}, Pr, Nu | Impeller Reynolds, Prandtl and Nusselt numbers | 1 |
| ρ | Liquid density, using cubic metres in this equation | kg m⁻³ |
| n | Rotational frequency in revolutions per second, not angular velocity in radians | s⁻¹ |
| d, D_{v} | Impeller diameter and the vessel diameter used by the correlation | m |
| η, η_{w} | Dynamic viscosities evaluated at bulk and wall temperatures | Pa s |
| c_{p} | Specific heat capacity | J kg⁻¹ K⁻¹ |
| λ_{l} | Liquid thermal conductivity | W m⁻¹ K⁻¹ |
| h_{i} | Liquid-side heat-transfer coefficient | W m⁻² K⁻¹ |
| B, a, b, c | Fitted coefficient and exponents for the relevant geometry and flow range; powers generalize repeated multiplication | 1 |

Reading the relationshipUnits cancel within each group. They compare inertia with viscosity, momentum with thermal diffusion, and actual heat transfer with reference conduction. The last line is an empirical correlation form; the viscosity ratio accounts for differing bulk and near-wall properties.

A worked exampleFor ρ = 1000 kg/m³, n = 2 s⁻¹, d = 0.1 m and η = 0.1 Pa·s, Re_M = 200. With c_p = 2000 J/(kg·K) and λ_l = 0.2 W/(m·K), Pr = 1000. If h_i = 100 W/(m²·K) and D_v = 0.3 m, Nu = 150.

ConditionsCorrelation constants must match geometry and flow regime. Non-Newtonian materials need a viscosity appropriate to the shear conditions or a dedicated correlation. The example calculates the groups without assuming unknown correlation constants.

A correlation among these groups is not a set of universal constants. Impeller geometry, baffles, vessel proportions, heating or cooling direction and the range of flow conditions affect its coefficients and exponents. Polymer solutions may also be shear thinning: their apparent viscosity changes with the imposed rate of deformation. In that case, the viscosity used to describe the stirred region needs a clear definition. A value measured under one slow-flow condition cannot simply represent every location. These considerations explain why increasing speed sometimes improves cooling strongly, sometimes produces only a small gain and sometimes encounters power or mechanical constraints first.

The coolant is also a flowing material with finite heat capacity. It warms as it moves through the jacket, and insufficient flow can produce a substantial difference between its inlet and outlet temperatures. Treating jacket temperature as a fixed value is useful for building an initial model. A more detailed calculation can then include coolant flow and its changing temperature. Knowing where each temperature is measured is as important as knowing the overall transfer coefficient. The bulk reaction liquid, inner wall, outer wall and coolant generally have different temperatures; those differences provide the driving force that carries energy along the route.

## Why some temperature disturbances recover and others grow

Early combustion research faced a puzzling observation: a reaction could proceed slowly at a given surrounding temperature, yet accelerate sharply when the vessel or its cooling conditions changed. In the 1920s and 1930s, Nikolai Semenov developed thermal-explosion theory by considering internally generated heat together with heat lost to the vessel surroundings. Recalling this work in his Nobel lecture, he emphasized that self-heating conditions depend on reaction kinetics, mixture composition and heat dissipation. The insight is useful for polymerization as well. It turns a seemingly sudden acceleration into a feedback process whose contributing mechanisms can be identified and calculated.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe04/en/#en-s3)

Figure 2 · The geometry behind thermal-explosion theory, redrawn in modern dimensionless form. On identical scales, increasing the generation parameter raises the exponential curve until the two intersections merge and disappear.

First allow only temperature to vary, while temporarily holding reactant concentration and other conditions fixed. Over many useful temperature intervals, a rate constant follows an Arrhenius relationship. Temperature must be expressed in kelvin because the exponential compares an activation-energy scale with thermal energy. A ten-kelvin rise near three hundred kelvin can produce a substantial rate increase. A larger activation energy generally gives stronger temperature sensitivity under the same comparison conditions. The conditions matter: the mechanism and the rate expression must remain applicable over the temperature interval being examined.

Temperature sensitivity of the rate constantEq. 5

![Temperature sensitivity of the rate constant](https://ml-biomat.com/static/agent-math/398667b6f80163979fb7b723.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| k(T), k_* | Rate constant at T and reference value at T_* | Depends on rate order; s⁻¹ for the first-order example |
| T, T_* | Actual and reference absolute temperatures | K |
| E_{a} | Activation energy | J mol⁻¹ |
| R_{g} | Gas constant, approximately 8.314 | J mol⁻¹ K⁻¹ |
| exp, ln | Natural exponential and logarithm, inverse functions; the exponent is dimensionless | 1 |
| d ln k/dT | Relative temperature sensitivity; formally the derivative of ln(k/k_*) | K⁻¹ |

Reading the relationshipTaking the ratio of Arrhenius expressions at two temperatures removes the prefactor. Differentiating the logarithm gives the relative rate-constant change per small temperature increase.

A worked exampleWith E_a/R_g = 10000 K, T_* = 350 K and k_* = 0.010 s⁻¹, k at 360 K is about 0.0221 s⁻¹. Near 350 K the relative sensitivity is approximately 0.0816 K⁻¹.

ConditionsThe mechanism and approximate activation energy remain applicable over the chosen interval. Overall polymerization rate also depends on concentrations, termination, diffusion and phase state.

Plot heat-generation and heat-removal power against temperature. Their intersections represent equal generation and removal. Starting at one intersection, imagine a small upward temperature displacement. If removal increases more than generation, the extra removal tends to cool the system back. If generation increases more, the resulting heat surplus drives it further away. A curve's slope expresses how much its vertical quantity changes for a small horizontal change. Comparing slopes therefore describes the response near an intersection in this model with a single temperature variable. The same comparison also works for a small downward displacement.

Small-disturbance recovery in a one-variable modelEq. 6

![Small-disturbance recovery in a one-variable model](https://ml-biomat.com/static/agent-math/1fcfcec719f4e47a56481145.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ε | Small temperature displacement from the equilibrium, positive or negative | K |
| t | Time | s |
| C_{th} | Thermal capacity | J K⁻¹ |
| Q_{gen}′, Q_{rem}′ | Generation and removal slopes with respect to temperature at the intersection; primes denote derivatives | W K⁻¹ |
| τ_{rel} | Small-disturbance decay time when the stated inequality holds | s |
| ≈, > | Approximately equal and greater than; the approximation retains terms linear in the disturbance | 1 |

Reading the relationshipAt equilibrium the powers balance. Approximate each nearby power by its equilibrium value plus slope times displacement. Their difference gives the first line. A negative net slope cools a positive displacement and warms a negative displacement.

A worked exampleFor C_th = 20 kJ/K, removal slope 0.3 kW/K and generation slope 0.1 kW/K, the decay time is 100 s. A 2 K initial displacement becomes about 0.736 K after 100 s in the linear approximation.

ConditionsThis is a small-disturbance result for a model with temperature as the only independent dynamic variable. Independent concentration, jacket or controller responses require coupled dynamic analysis.

The feedback becomes especially clear after choosing convenient temperature and time scales. Divide the temperature rise by a scale associated with reaction temperature sensitivity, and divide elapsed time by the vessel's thermal relaxation time. The resulting model contains a parameter comparing initial heat generation with cooling capacity. Its exponential curve describes the increase in generation caused by thermal feedback, while a straight line describes removal driven by the temperature difference. Removing units in this way preserves the competition between mechanisms and allows systems with different physical sizes and parameter values to be compared on one graph.

A scaled thermal-feedback modelEq. 7

![A scaled thermal-feedback model](https://ml-biomat.com/static/agent-math/748d63a0994891f692d936d8.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| T_{b} | Temperature-difference scale, not bulk temperature | K |
| R_{g}, E_{a} | Gas constant and activation energy | J mol⁻¹ K⁻¹; J mol⁻¹ |
| T_{j}, T | Fixed surrounding/jacket temperature and uniform reaction temperature | K |
| θ | Dimensionless temperature rise above the surroundings | 1 |
| UA | Overall heat-transfer conductance, coefficient times area | W K⁻¹ |
| C_{th}, t | Thermal capacity and actual time | J K⁻¹; s |
| s | Dimensionless time; the variable s is distinct from the second as a unit | 1 |
| Q_{0} | Generation at the surrounding temperature for fixed reactant conditions | W |
| δ | Ratio of reference generation to removal capacity on the chosen temperature scale | 1 |
| e, dθ/ds | Euler number, about 2.718; rate of change of scaled temperature with scaled time | 1 |

Reading the relationshipExpand the Arrhenius exponent near the surrounding temperature for a relatively small temperature rise, giving generation approximately Q_0 exp(θ). Dividing the energy balance by UA T_b turns removal into θ and accumulation into a derivative with respect to scaled time.

A worked exampleFor T_j = 300 K and E_a/R_g = 9000 K, T_b = 10 K. With C_th = 20 kJ/K, UA = 0.2 kW/K and Q_0 = 0.6 kW, δ = 0.30. Scaled time s = 1 represents 100 s, and θ = 1 represents a 10 K rise.

ConditionsUniform temperature, fixed surroundings, constant thermal capacity and conductance, with little reactant depletion over the interval. Larger rises, phase changes or substantial depletion require the unexpanded kinetics and fuller balance.

For a sufficiently small generation parameter, the curves have two intersections. The lower-temperature state attracts nearby temperature trajectories. The higher-temperature state acts as a boundary: beyond it, generation in the model grows faster than removal. As the parameter increases, the intersections approach each other and merge in a tangent contact. Beyond that point, the low-temperature equilibrium no longer exists. At tangency, the curves have both the same height and the same slope. Applying those two conditions gives the critical value below. The number belongs to this scaled approximation; its derivation explains the feedback more usefully than treating it as a universal temperature limit.

Where the two intersections mergeEq. 8

![Where the two intersections merge](https://ml-biomat.com/static/agent-math/0be03ff928656a32b2742baa.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| δ, δ_{c} | Generation parameter and its critical value in the scaled model | 1 |
| θ_{c} | Dimensionless temperature rise at tangency | 1 |
| e | Base of natural exponentials, approximately 2.718 | 1 |
| e⁻¹ | Reciprocal of e | 1 |

Reading the relationshipThe first line equates generation and removal; the second equates their slopes. Identical left sides imply a critical scaled rise of one. Substitution gives the parameter 1/e.

A worked exampleAt δ = 0.30 the lower intersection is about θ = 0.4894 and the upper one about 1.7813. At δ = 0.40, the parameter exceeds the critical value and this simplified model has no intersection.

ConditionsThe critical value belongs to the preceding one-temperature approximation. It is dimensionless; actual critical conditions depend on the material and equipment parameters used to form it.

### Following a temperature displacement

[Figure: Following a temperature displacement](https://ml-biomat.com/tutorials/biomaterials-courses/pe04/en/#en-s3)

Semenov approximation with uniform temperature, fixed reactant conditions and constant cooling conductance. The upper axes are fixed; trajectories end at θ = 4. The variable s is dimensionless time, distinct from seconds. Critical δ is 1/e.

In the interactive figure, keep the initial temperature rise small and increase the generation parameter to see the lower intersection disappear. Then choose a parameter with two intersections and move the initial temperature to either side of the upper one. These experiments distinguish two causes of acceleration. External conditions may change until an equilibrium ceases to exist, or unchanged conditions may still permit a starting state outside the region attracted to the lower equilibrium. Once a trajectory rises sharply, a real mixture can undergo reactant depletion, boiling, viscosity changes or additional reactions. Those mechanisms enter a more complete material and energy balance for the later evolution.

## Continuous feed changes the shape of heat generation

Holding reactant concentration fixed made the origin of thermal feedback clear. In a continuous stirred tank, concentration usually changes with temperature: faster reaction consumes more reactant and leaves less in the vessel. Think of a workshop receiving raw material at a steady rate. Faster machines reduce the inventory waiting inside. Even infinitely fast machines cannot process more material each minute than the supply provides over sustained operation. A continuous reactor has the same supply constraint. It prevents the steady-state heat-generation curve from increasing exponentially without limit as temperature rises.

To calculate the effect, consider a well-mixed liquid of approximately constant density and volume, with one reactant consumed by a first-order reaction. First order means that the consumption rate per unit volume is proportional to reactant concentration; it is an explicit example, rather than a rule for all polymerizations. Space time equals vessel volume divided by volumetric flow rate. At steady state, incoming material balances outgoing material and reaction consumption. We can therefore calculate the vessel concentration corresponding to each temperature and insert it into the heat-release expression. The resulting curve follows the steady material balance as temperature is varied.

Feed-limited heat generation at steady stateEq. 9

![Feed-limited heat generation at steady state](https://ml-biomat.com/static/agent-math/0fd953b469d3c3627b17c636.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| τ, V, q | Space time, reactor volume and volumetric flow | s; L; L s⁻¹ |
| C_{s}(T), C_{f} | Steady vessel concentration at a given temperature and feed concentration | mol L⁻¹ |
| k(T), T | First-order rate constant and absolute temperature | s⁻¹; K |
| Q_{gen,s} | Heat generation calculated along the steady material balance | W |
| ΔH_{r} | Reaction enthalpy per mole of reactant consumed | J mol⁻¹ |
| →, ≫ | Approaches and much greater than; kτ is dimensionless reaction intensity | 1 |

Reading the relationshipAt steady state, inflow minus outflow equals consumption. Rearranging gives concentration, which is inserted into heat generation. Very rapid reaction consumes nearly all incoming reactant, so generation approaches feed molar flow times heat per mole.

A worked exampleFor V = 10 L, q = 0.1 L/s, C_f = 1 mol/L and k = 0.01 s⁻¹, τ = 100 s and steady concentration is 0.5 mol/L. If −ΔH_r = 200 kJ/mol, generation is 10 kW and the feed-limited upper value is 20 kW.

ConditionsA constant-density, well-mixed, irreversible first-order single reaction with approximately constant heat effect. This is a steady concentration curve; transient concentration follows the dynamic material balance.

At low temperature, reaction is slow, most of the feed leaves unreacted and heat generation is small. In an intermediate region, conversion rises strongly with temperature and the generation curve becomes steep. At higher temperature, conversion is already close to one. Increasing the rate constant cannot make the sustained consumption rate exceed the rate at which reactant enters. Generation consequently approaches a plateau set by the feed. Cooling and sensible heat carried by the streams can give a straight removal line under constant-property assumptions. That line may intersect the curved generation relation once or, for suitable parameters, three times. The number of intersections follows from the model and its parameters.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe04/en/#en-s4)

Figure 3 · A continuous-reactor example connected to van Heerden’s analysis of autothermic processes. Generation follows the steady first-order balance, using the adjacent model parameters. For this parameter set, A and C are locally stable in the full dynamics and B is unstable.

In his 1953 study of autothermic processes, C. van Heerden examined how reaction heat can sustain operation and how different operating states can arise. Autothermic operation means that generated heat meets the relevant thermal demand; it does not require perfect isolation from the surroundings. One useful consequence is that the same external conditions can permit different steady states, with the startup history helping determine which is reached. This gives meaning to ignition, extinction and hysteresis in reactor analysis. Ignition can describe a jump from a low-rate branch to a high-rate branch without a visible flame, while extinction describes the reverse change.

Changing jacket temperature usually shifts the removal line. Changing total heat-transfer capacity usually changes its slope. Changing feed flow is more involved: it alters the sensible heat carried by the streams, the space time, the steady concentration and the maximum feed-limited heat release. Both the generation and removal descriptions must therefore be recalculated when flow changes. Keeping an old generation curve fixed while changing flow can give a misleading prediction. A useful operating choice considers product requirements, attainable states and the size of disturbances the process can tolerate, rather than automatically selecting the hottest intersection.

An endothermic reaction offers a helpful comparison. If increasing temperature accelerates a heat-absorbing reaction, the extra reaction consumes more heat and tends to oppose warming. A complete process can nevertheless include heater-control delays, catalyst changes or additional reactions. Its response follows from the actual material and energy relationships. Stability describes motion near a state; product quality, degradation and pressure are other properties to examine alongside it. Keeping these questions distinct makes the word “stable” scientifically useful: a state can attract nearby trajectories while still being unsuitable for the material being manufactured.

## Temperature and concentration evolve together

A steady-state graph shows possible destinations but does not fully describe the journey. Suppose a brief heat input raises a stirred tank's temperature. Concentration cannot instantly jump to the steady value associated with that new temperature. Reaction and replacement by the flowing feed take time. At the same temperature, a vessel freshly filled with reactant and a vessel that has been operating at low reactant concentration can therefore generate very different heat powers. This is why a generation curve constructed along the steady material balance cannot by itself represent every transient state.

For the first-order example, write one time-dependent relationship for concentration and another for temperature. Concentration changes through incoming feed, outgoing flow and reaction consumption. Temperature changes through stream enthalpy, reaction heat and jacket transfer. The reaction rate constant in both relationships depends on temperature, while the heat-release term also depends on concentration. The equations must therefore be evaluated together. A derivative still means the current rate of change: calculate both rates from the present state, advance in time and repeat. This constructs a trajectory in which material consumption and heating influence one another continuously.

Coupled concentration and temperature dynamicsEq. 10

![Coupled concentration and temperature dynamics](https://ml-biomat.com/static/agent-math/9598e2f4f9a203309f7628d3.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| C, C_{f} | Vessel and feed reactant concentrations | mol L⁻¹ |
| T, T_{f}, T_{j} | Vessel, feed and jacket temperatures | K |
| t, τ | Actual time and space time V/q | s |
| k(T) | Arrhenius-dependent first-order rate constant | s⁻¹ |
| β | Temperature-rise coefficient per concentration of reactant consumed | K L mol⁻¹ |
| γ | Thermal response-rate coefficient for jacket transfer | s⁻¹ |
| ΔH_{r} | Molar reaction enthalpy | J mol⁻¹ |
| ρc_{p} | Volumetric heat capacity of the liquid | J L⁻¹ K⁻¹ |
| U, A, V | Overall coefficient, transfer area and liquid volume | W m⁻² K⁻¹; m²; L |
| dC/dt, dT/dt | Instantaneous concentration and temperature-change rates | mol L⁻¹ s⁻¹; K s⁻¹ |

Reading the relationshipThe first equation is a material balance per unit volume. Dividing the energy balance by liquid thermal capacity gives the second, with every term a temperature-change rate. Temperature changes k and concentration changes generation, so both derivatives use C and T from the same instant.

A worked exampleTake τ = 100 s, β = 200 K·L/mol, γ = 0.01 s⁻¹, C_f = 1 mol/L and T_f = T_j = 300 K. At T = 350 K and k = 0.01 s⁻¹, both derivatives vanish for C = 0.5 mol/L. At the same temperature with C = 1 mol/L, temperature rises at 1 K/s and concentration falls at 0.01 mol/(L·s).

ConditionsConstant volume and properties, a single well-mixed liquid phase, fixed flow and jacket temperature, with wall thermal storage and phase changes omitted. Interactive values define a teaching model rather than a formulation for a particular material.

The coupled description also clarifies the reach of a slope test. If concentration adjusts much faster than temperature, eliminating it in favour of its corresponding steady value can yield a useful one-variable approximation. If the response times are comparable, the full two-variable dynamics matter. A trajectory can overshoot, undergo damped oscillations or, for some parameters, develop sustained oscillation. In 1974, A. Uppal, W. H. Ray and A. B. Poore classified dynamic behaviour in stirred tanks carrying out a single first-order reaction, including concentration and temperature trajectories. Retaining the second variable preserves a physical fact: changing the material inventory requires time.

The next interaction uses an explicitly stated set of teaching parameters with consistent vessel volume, feed flow, heat capacity and reaction kinetics. It displays steady generation and removal alongside the temperature and concentration histories from a selected initial state. Coolant temperature is an external condition; initial temperature and concentration define the starting point. When changing these controls, observe separately whether the intersections move and whether the trajectory changes. Stability labels at the intersections are calculated from the small-disturbance response of the same coupled equations, rather than assigned solely from the visual slope ordering on the steady graph.

### One reactor, different starts and cooling conditions

[Figure: One reactor, different starts and cooling conditions](https://ml-biomat.com/tutorials/biomaterials-courses/pe04/en/#en-s5)

Model parameters: V = 10 L, q = 0.1 L/s, C_f = 1 mol/L, T_f = 300 K, ρc_p = 1 kJ/(L·K), −ΔH_r = 200 kJ/mol and UA = 0.1 kW/K. At 350 K, k = 0.01 s⁻¹; E_a/R_g = 10000 K. Material and energy equations are integrated together, with no phase change or feedback controller.

Begin with a relatively cool initial state containing abundant reactant, then increase the initial temperature. Under the same coolant conditions, different starts can approach different branches. A large initial chemical inventory can also produce a temporary peak hotter than the eventual steady state. That peak matters because an acceptable final temperature does not describe the entire startup path. Lower the initial concentration and compare the change in the peak. This separates the effect of temperature-sensitive kinetics from the amount of reactant still available to release heat.

Temperature control introduces further response times. A sensor detects change, a controller moves a valve, coolant flow responds and heat travels through the wall. Increasing heat-transfer capacity changes the energy balance; improving sensing and control response helps detect and address deviations sooner. These are different interventions. A temperature set point alone says little about the available transfer area, coolant condition or stored reactant. Understanding a transient ultimately connects three questions: where is the system now, how quickly is it changing, and how much more reaction heat can still appear?

## Why polymerization can accelerate as the liquid thickens

Free-radical polymerization involves three useful actions to distinguish: generating reactive radicals, adding monomer to growing chains and ending a chain's ability to grow. Monomers are relatively small reactive molecules, whereas active chains become progressively longer. Two active chains can terminate when they meet, through combination or other terminating reactions. Such encounters depend on motion through the surrounding mixture. Increasing viscosity makes long-chain encounters harder, but it need not slow the movement of small monomers by the same factor. Propagation and termination can therefore respond quite differently to the developing polymer environment.

In 1948, Ernst Trommsdorff, Herbert Köhle and Paul Lagally examined sharp acceleration during methyl methacrylate polymerization. Their explanation emphasized how dissolved polymer hindered encounters between growing chains and suppressed termination while monomer could still reach active chain ends. Active centres accumulated and the total propagation rate increased. The phenomenon is commonly called the gel effect or autoacceleration. The historical name does not require a chemically crosslinked, three-dimensional network to have formed. The mechanism concerns changing mobility and the relative rates of growth and termination.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe04/en/#en-s6)

Figure 4 · Trommsdorff, Köhle and Lagally’s methyl methacrylate work helped establish this explanation. The diagram contrasts restricted encounters between long chains with continued monomer supply; lines illustrate the mechanism rather than measured trajectories.

A simple radical population balance makes the argument quantitative. When radical generation approximately balances radical loss by bimolecular termination, the radical concentration depends on both the initiation rate and the termination rate constant. Lowering the termination constant while temporarily holding other quantities fixed increases the active-centre concentration. Polymerization rate depends on both active centres and available monomer, so it can rise. The square root appears because termination requires two radicals to meet and its loss rate depends on the square of radical concentration. Later, monomer depletion or restricted segmental motion can reduce propagation, so an earlier acceleration need not continue throughout conversion.

How slower termination increases active chainsEq. 11

![How slower termination increases active chains](https://ml-biomat.com/static/agent-math/969aabcb5bce9b1ca7ac4290.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| R_{i} | Effective radical-generation rate | mol L⁻¹ s⁻¹ |
| k_{t} | Bimolecular termination constant, using two radicals lost per event | L mol⁻¹ s⁻¹ |
| C_{R} | Active radical concentration | mol L⁻¹ |
| R_{p} | Monomer-consumption rate | mol L⁻¹ s⁻¹ |
| k_{p} | Propagation rate constant | L mol⁻¹ s⁻¹ |
| C_{M} | Monomer concentration | mol L⁻¹ |
| √, ≈ | Nonnegative square root and approximate equality; the root solves a quadratic balance | 1 |

Reading the relationshipUnder a quasi-steady radical balance, generation approximately matches termination loss. Encounters involve radical pairs, giving the concentration-squared dependence. Each active centre propagates at frequency k_p C_M; multiplication by centre concentration gives total monomer consumption.

A worked exampleFor R_i = 2×10⁻⁷ mol/(L·s) and k_t = 10⁷ L/(mol·s), C_R = 10⁻⁷ mol/L. With k_p = 10³ L/(mol·s) and C_M = 5 mol/L, R_p = 5×10⁻⁴ mol/(L·s). Reducing only k_t to one percent increases both C_R and R_p tenfold.

ConditionsA simplified homogeneous quasi-steady radical model with the stated termination convention. Transport limitations, scavengers, chain transfer and transient radical populations require appropriate extensions.

Mobility-driven autoacceleration can combine with thermal acceleration. Reduced termination raises heat generation. Warming then changes initiation, propagation and termination rate constants. Meanwhile, the increasingly viscous liquid may transfer heat to the vessel wall less effectively. To identify which mechanism begins the change, compare temperature, conversion, viscosity and heat flow over time. A rate increase observed under closely controlled constant temperature helps distinguish mobility-related autoacceleration from an increase caused simply by warming. Separating the mechanisms is valuable when constructing a model that should remain useful after vessel size or cooling conditions change.

An induction period can precede rapid growth. Some radical scavengers consume newly generated radicals, delaying the accumulation of growing chains. As their trapping capacity is depleted, polymer growth becomes more prominent. Initiator concentration also changes as the initiator decomposes, so radical supply need not be constant. The next relations describe first-order initiator decomposition and then treat effective trapping capacity as an inventory. The number of radicals that one inhibitor molecule can consume depends on its chemistry. Counting effective trapping equivalents keeps molecular concentration distinct from the number of radicals that can still be captured.

Initiator supply changes with timeEq. 12

![Initiator supply changes with time](https://ml-biomat.com/static/agent-math/8d11528721e698231031ec72.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| C_{I}(t), C_{I0} | Current and initial initiator concentrations | mol L⁻¹ |
| k_{d} | First-order decomposition constant | s⁻¹ |
| t | Time | s |
| f | Fraction of generated radicals that effectively initiate | 1 |
| R_{i} | Effective radical-generation rate | mol L⁻¹ s⁻¹ |
| e, 2 | Natural exponential base; stoichiometric number of two primary radicals per decomposition | 1 |

Reading the relationshipFirst-order decomposition removes a fraction proportional to the remaining initiator, giving exponential decay. Multiplying decomposition events by two radicals and the effective fraction gives the useful radical supply.

A worked exampleWith C_I0 = 0.01 mol/L, k_d = 0.001 s⁻¹ and f = 0.5, initial R_i is 10⁻⁵ mol/(L·s). After 1000 s, about 36.8% of initiator remains and R_i is about 3.68×10⁻⁶ mol/(L·s).

ConditionsConstant temperature and first-order decomposition with two primary radicals per initiator molecule. When temperature changes, k_d changes with time. Other initiation mechanisms need their corresponding generation laws.

Induction as depletion of trapping capacityEq. 13

![Induction as depletion of trapping capacity](https://ml-biomat.com/static/agent-math/cd6a904bafbfedad71660f31.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| B(t), B_{0} | Current and initial effective trapping-site capacity in radical equivalents | mol L⁻¹ |
| R_{i}, u, t | Radical-generation rate, integration time variable and elapsed time | mol L⁻¹ s⁻¹; s; s |
| ∫ | Integral, adding radical amounts generated in successive short time intervals | 1 |
| C_{R}, C_{M} | Active radical and monomer concentrations | mol L⁻¹ |
| k_{B}, k_{p} | Effective site-capture and propagation constants | L mol⁻¹ s⁻¹ |
| R_{p} | Monomer-consumption rate | mol L⁻¹ s⁻¹ |
| t_{ind} | Approximate exhaustion time under constant radical supply | s |

Reading the relationshipWhen capture dominates, each effectively generated radical consumes approximately one trapping equivalent. Balancing generation with site capture gives the quasi-steady radical population. Under constant supply, inventory divided by consumption rate gives exhaustion time.

A worked exampleFor B_0 = 0.001 mol/L and approximately constant R_i = 10⁻⁵ mol/(L·s), the estimated induction time is 100 s. After 50 s, capacity is 0.0005 mol/L; under otherwise unchanged capture-dominated conditions, radical concentration is twice its initial value.

ConditionsIndependent effective trapping sites, little early monomer consumption and capture-dominated radical loss. Include bimolecular termination near exhaustion. Real multistep inhibitors need chemically appropriate capacity and rate definitions.

As trapping capacity approaches exhaustion, a capture-dominated rate expression predicts a sharp increase. At this stage, the balance must include bimolecular termination together with propagation and changing concentrations. A denominator approaching zero marks the end of the simplified balance's useful regime; the actual rate is determined by the newly important processes. Oxygen and other inhibition systems also have chemistry-dependent effects, so an induction period cannot generally be reduced to the time needed for dissolved oxygen to escape. A quiet initial temperature trace may accompany depletion of a chemical inventory that controls later growth. Explaining that inventory makes the subsequent heat peak understandable.

## Small particles in water reorganize reaction and heat transfer

Emulsion polymerization distributes reaction among many polymer particles in an aqueous phase. Larger monomer droplets can serve as reservoirs. A small dissolved fraction moves through water and enters growing polymer particles, while radical entry, exit and termination determine the number of active chains in each particle. The aqueous phase helps carry heat away, and a relatively low bulk viscosity can support effective stirring. The main reaction locations are growing polymer particles, which have a different role from the monomer-storage droplets. Distinguishing reservoir, transport route and reaction location is the starting point for understanding why the kinetics differ from those of a homogeneous liquid.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe04/en/#en-s7)

Figure 5 · The 1948 emulsion-polymerization theory made separated reaction loci central to the kinetics. Monomer droplets, dissolved monomer and polymer particles have distinct roles. Sizes and separations identify the objects and are not drawn to scale.

In 1948, Wendell Smith and Roswell Ewart analysed emulsion-polymerization kinetics by considering radicals distributed among separate reaction loci. They examined cases with different average radical populations per locus. Under some conditions, a particle often alternates between containing no active chain and containing one, giving an average near one-half. No particle literally contains half a chain; the value is an average over particles or time. Compartmentalization changes how radicals can encounter each other. Using only a bulk-averaged radical concentration in a homogeneous termination expression can consequently lose the particle-scale structure that controls the process.

Adding the active chains across particlesEq. 14

![Adding the active chains across particles](https://ml-biomat.com/static/agent-math/b7e9884b8fc805a2ad1f4edf.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| R_{p,mix} | Monomer-consumption rate per total mixture volume | mol L⁻¹ s⁻¹ |
| k_{p} | Propagation constant inside particles | L mol⁻¹ s⁻¹ |
| C_{M,p} | Monomer concentration per particle-phase volume | mol L⁻¹ |
| N_{p} | Number of reaction particles per litre of total mixture | L⁻¹ |
| n̄ | Mean active radical count per particle | 1 |
| N_{A} | Avogadro constant, approximately 6.022×10²³, converting counts to moles | mol⁻¹ |

Reading the relationshipk_p C_M,p is the mean monomer-addition frequency per active centre. Multiply by active centres per particle and particles per mixture volume, then divide by Avogadro constant to convert the molecular count rate into moles.

A worked exampleFor k_p = 1000 L/(mol·s), C_M,p = 5 mol/L, N_p = 10¹⁷ L⁻¹ and n̄ = 0.5, R_p,mix is about 4.15×10⁻⁴ mol/(L·s). At −ΔH_r = 70 kJ/mol, this corresponds to approximately 29.1 W per litre of mixture.

ConditionsA dispersion described by representative particle monomer concentration and mean radical occupancy. Sum over particle populations when heterogeneity is important. An occupancy of 0.5 belongs to particular kinetic conditions.

A typical batch emulsion polymerization is often described through particle formation, an approximately constant-rate interval and a later period of declining monomer supply. During nucleation, increasing particle number can increase total heat generation. In an intermediate interval, particle number, monomer concentration within particles and mean radical occupancy can all remain approximately constant, producing a rate plateau. The plateau alone does not establish monomer-diffusion control. It can arise even when transport supplies monomer quickly enough. Identifying the controlling step requires comparing supply with consumption and examining the response to changes in mixing, particle size or monomer conditions.

A first estimate of monomer supply to a spherical particle uses steady diffusion. Concentration is higher far from the particle than at its surface, so monomer moves towards it. Solving the radial diffusion problem gives a total arrival rate proportional to diffusion coefficient, radius and concentration difference. This rate is an amount per particle per second. A flux per unit surface area is a different quantity and requires division by particle area. Multiplying total arrival rate by reaction heat per mole gives the heat-generation power that would accompany immediate consumption of the arriving monomer in a transport-limited case.

Supply and heat removal for one particleEq. 15

![Supply and heat removal for one particle](https://ml-biomat.com/static/agent-math/d01f7c18dd1ca8490d9eae21.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| j | Total molar arrival rate to one spherical particle | mol s⁻¹ |
| π | Circle constant, approximately 3.1416 | 1 |
| D | Monomer diffusion coefficient in the surrounding medium | m² s⁻¹ |
| r_{p} | Particle radius | m |
| C_{b}, C_{s} | Far-field and particle-surface monomer concentrations, both per cubic metre | mol m⁻³ |
| Q_{p,gen}, Q_{p,rem} | Single-particle generation and outward heat-transfer powers | W |
| ΔH_{r} | Reaction enthalpy per mole consumed | J mol⁻¹ |
| h | Particle-surface heat-transfer coefficient | W m⁻² K⁻¹ |
| T_{s}, T_{b} | Particle surface and bulk-fluid temperatures | K |

Reading the relationshipThe first line is the steady spherical-diffusion result, already integrated over the surface. The second assumes arriving monomer is consumed by the stated reaction. The third multiplies spherical area by heat-transfer coefficient and temperature difference.

A worked exampleFor D = 10⁻⁹ m²/s, r_p = 10⁻⁷ m and a 1 mol/m³ concentration difference, j is about 1.26×10⁻¹⁵ mol/s. At 70 kJ/mol, generation is about 8.80×10⁻¹¹ W. With h = 10⁶ W/(m²·K), balancing it requires a surface temperature difference of about 0.00070 K.

ConditionsAn isolated sphere in an effectively unbounded medium with constant D and steady external diffusion. Flow, interacting concentration fields, internal pores and internal temperature gradients require corresponding models. The example supplies h independently.

A porous solid catalyst introduces related transport questions, with an additional distinction between the external fluid layer and internal pores. Reactant can cross an outer boundary layer and diffuse into pores before reaching active sites. Heat then travels outwards. The surface can be hotter than the bulk fluid, and the interior can have its own temperature profile. A steady bulk thermometer reading therefore describes a different location from a microscopic hot region. Rate definitions also need a consistent volume basis: a rate per unit catalyst volume and one per unit reactor volume require different multipliers. Particle volume or number should enter the conversion between them only once.

Diffusion in liquids depends on viscosity and molecular size as well as absolute temperature. Heating changes viscosity, and polymerization changes the medium itself. A diffusion-limited generation curve is consequently not generally a straight line in temperature. When monomer droplets disappear, monomer concentration within particles can decline and reduce both rate and heat flow. At the same time, increasing internal viscosity and glass formation can alter propagation and termination. A water-based dispersion provides useful heat-management conditions, but a complete explanation still connects intraparticle reaction, transport between phases and cooling of the whole reactor.

## Scaling up starts with the heat still available

A modest instantaneous heat-release rate has more than one possible explanation. The reaction may be nearly complete, or it may temporarily be limited by temperature, radical supply or mixing while substantial reactant remains. Estimating the remaining reaction potential distinguishes these situations. An adiabatic temperature rise divides the heat still available from reaction by the system's heat capacity. It asks how much the temperature would rise if that heat were temporarily retained. The calculation connects chemical inventory to a temperature scale and gives information that a present thermometer reading alone cannot supply.

Converting remaining reaction heat into a temperature riseEq. 16

![Converting remaining reaction heat into a temperature rise](https://ml-biomat.com/static/agent-math/1d56394f8ac6781e0c1ad45e.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ΔT_{ad} | Adiabatic rise associated with remaining reaction potential | K |
| ΔH_{r} | Reaction enthalpy on the stated molar reactant basis | J mol⁻¹ |
| n_{remain} | Remaining amount capable of undergoing the stated reaction | mol |
| C_{th} | Total heat capacity of included material and thermally participating components | J K⁻¹ |
| ≈ | Approximation using constant heat capacity and reaction enthalpy | 1 |

Reading the relationshipRemaining moles times heat per mole gives available energy. Dividing by energy required per kelvin gives a temperature difference.

A worked exampleFor 2 mol remaining reactant, 70 kJ/mol heat release and 10 kJ/K effective heat capacity, the adiabatic rise is about 14 K. At the same reactive inventory with 20 kJ/K heat capacity, it becomes 7 K.

ConditionsCompletion of the stated reaction without external heat loss, with approximately constant enthalpy and heat capacity. Reversible equilibrium, other reactions, boiling, phase changes or strongly variable properties require an updated energy allocation.

This calculation also explains how a diluent or water changes a thermal history. Additional material contributes heat capacity and may change reactant concentration and reaction rate. At the same total heat release, a larger heat capacity gives a smaller temperature increase. Formulation, phase behaviour and downstream separation can change as well, so heat capacity is one consideration among several in choosing a composition. Over a large temperature range, variable specific heat, evaporation and other phase changes must enter the balance. A constant-property calculation provides an energy scale under its stated assumptions, which can then be refined as the physical description becomes more detailed.

Geometric scale-up changes the balance between heat-producing volume and heat-removing area. Doubling every linear dimension of a similar vessel increases volume eightfold but surface area only fourfold. If reaction rate per unit volume stays the same, generation increases eightfold. If heat-transfer coefficient and temperature difference remain unchanged, removal through the corresponding surface increases only fourfold. Available area per unit volume therefore falls. This unequal scaling is why temperature-control experience in a small cup cannot simply be multiplied by the ratio of batch masses to predict a larger vessel.

Volume and area scale differentlyEq. 17

![Volume and area scale differently](https://ml-biomat.com/static/agent-math/ca20ed82e92ad89dbe24b082.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| V, A, R | Volume, exchanging surface area and radius of an ideal spherical vessel | m³; m²; m |
| π | Circle constant | 1 |
| A/V | Surface area per unit volume | m⁻¹ |
| τ_{th} | Thermal relaxation time without reaction under linear heat transfer | s |
| ρ, c_{p} | Density and specific heat capacity, using cubic metres for density here | kg m⁻³; J kg⁻¹ K⁻¹ |
| U | Overall heat-transfer coefficient | W m⁻² K⁻¹ |

Reading the relationshipSphere area grows with radius squared and volume with radius cubed, leaving an inverse-radius area-to-volume ratio. Thermal capacity divided by conductance gives a cooling response time, which increases with radius for similar spheres at fixed properties and U.

A worked exampleIncreasing radius from 0.1 m to 0.2 m reduces A/V from 30 m⁻¹ to 15 m⁻¹. For ρc_p = 2×10⁶ J/(m³·K) and U = 200 W/(m²·K), the reaction-free relaxation time increases from about 333 s to 667 s.

ConditionsThe sphere illustrates the geometry; for other similar shapes, area scales with the square of linear size and volume with its cube. Actual scale-up can change U, mixing, effective area and rate, which must be assessed separately.

Several process choices follow from these relationships. Internal coils, external circulation through a heat exchanger or additional effective surface provide more routes for heat to leave. Staged or continuous monomer addition changes the reactive inventory and the time distribution of generation. Solvent selection, dispersion and stirring influence heat capacity, reaction and transport together. Each choice also affects the material. Slow feeding can change copolymer composition or chain structure; intense shear can affect dispersed particles; external circulation changes flow and residence histories. Thermal management is therefore part of manufacturing the polymer, with consequences for both process behaviour and product properties.

Calorimetry connects the energy balance to measurement. Reaction calorimetry can maintain a chosen temperature while measuring the heat that must be removed, producing a time-resolved heat-release rate. Adiabatic or near-adiabatic calorimetry follows self-heating with relatively little external heat loss. Combining these measurements with conversion, feed records and heat capacity helps separate energy already released from energy still available. For polymers, relating heat flow to viscosity, molar-mass distribution or particle structure reveals whether a thermal change is altering production rate, material structure or both.

The original cup of resin can now be understood through a complete causal sequence. Reaction produces a net energy release. Finite cooling allows temperature to rise. Temperature and viscosity modify reaction and heat transfer, while remaining reactant determines the energy still available. Replacing a thin layer with a deep cup changes geometry and cooling. Changing initial temperature changes both the starting state and kinetics. Changing feed strategy changes inventory and timing. Identifying these effects separately and then returning them to the same energy balance makes thermal-stability diagrams readable and explains their direct relevance to polymer manufacture.
