# Why the Same Reaction Needs Different Reactors

Source: https://ml-biomat.com/tutorials/biomaterials-courses/pe02/en/
Language: en

A batch vessel, a continuously stirred tank and a flowing tube expose molecules to different concentrations and reaction histories. Starting with a material balance, this chapter develops reaction rates, three ideal reactor models, product selectivity and reactor combinations, showing when a larger vessel helps and when a different operating strategy matters more.

## Start by counting: where did the reactant go?

When making a pot of jam, the ingredients can be added together, stirred and heated, then poured out when the mixture is ready. A beverage factory may instead send material continuously through equipment, adding fresh feed at one end and collecting product at the other. Chemical changes can occur in both arrangements, but a small portion of material experiences a different history in each. In the pot, the ingredients largely age together. In a continuously fed vessel, newly arriving material may meet material that has already been reacting for some time. Resin manufacture, degradable polyester synthesis, polysaccharide modification and biomass processing all require decisions about these histories: how material enters, mixes, reacts and leaves.

The shape of a vessel is easy to see; the number of molecules inside it is far too large to count individually. Chemistry therefore uses the mole, a counting unit containing approximately 6.02 multiplied by ten to the power of twenty-three specified entities. A dozen means twelve objects; a mole performs a similar counting function on a molecular scale. If a vessel contains two moles of a reactant called A in one litre of liquid, its concentration is two moles per litre. Amount measures the total number, whereas concentration measures how densely that amount is distributed. Adding solvent can leave the amount of A unchanged while reducing its concentration, a distinction that matters both for reaction speed and for measuring consumption.

Imagine the reactor as a water tank with an inlet and an outlet, except that the quantity being tracked is the amount of A rather than the water level. Over a chosen interval, A increases through inflow, decreases through outflow and decreases when a reaction converts it into other chemical species. Its atoms have not disappeared; their chemical arrangement has changed. This accounting statement is called a material balance. Shortening the counting interval leads to an instantaneous rate of change, which mathematics expresses with a derivative. The three ideal reactor models developed below all start from this same balance. Their differences arise from which flow terms remain and from the concentration used to calculate reaction consumption.

The overall balance of AEq. 1

![The overall balance of A](https://ml-biomat.com/static/agent-math/b45a5ddef927d2ab142b8077.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| n_{A} | Amount of A inside the vessel | mol |
| t | Elapsed time | min |
| dn_{A}/dt | Derivative of the amount of A with respect to time: its instantaneous change rate | mol/min |
| F_{A,in}；F_{A,out} | Inlet and outlet molar flows of A; in and out identify the stream | mol/min |
| r_{A} | Positive net consumption rate of A per reacting volume | mol/(L·min) |
| V | Effective volume of reacting liquid | L |

Reading the relationshipThe left side records how quickly the amount of A changes. Inflow adds A, while outflow and reaction remove it. Multiplying consumption per volume by reacting volume gives total consumption, so every term has units of mol/min. A spatially varying rate requires integration over volume rather than an unspecified uniform value.

A worked exampleAn inlet of 0.30 mol/min, an outlet of 0.10 mol/min and a rate of 0.020 mol/(L·min) in 10 L give reaction consumption of 0.20 mol/min. The three terms sum to zero, establishing zero accumulation of A.

ConditionsA is counted as being consumed overall, and a uniform liquid-phase rate is used. Net generation from other reactions enters with the corresponding sign. Steady state sets the left side to zero; it does not make every term on the right individually zero.

A reaction rate expressed per unit volume resembles a crop yield expressed per unit area: it must be multiplied by the participating volume to obtain the total production or consumption rate. A twenty-litre vessel containing ten litres of reacting liquid uses ten litres in this liquid-phase balance. If each litre consumes 0.02 mole of A per minute, the entire liquid consumes 0.20 mole per minute. An inlet supplying 0.30 mole per minute and an outlet removing 0.10 mole per minute can balance this consumption exactly. The amount of A inside then remains constant. This is a steady state: continuing flow and continuing reaction balance one another while the individual molecules keep changing.

Comparing experiments of different sizes also requires a normalized measure. Conversion answers the question, “What fraction of the A supplied has reacted?” Zero means none has reacted, and one means all of the counted A has been consumed. A batch comparison follows the amount in the same vessel before and after reaction. A continuous steady-state comparison follows the molar flow entering and leaving per unit time. These amount or flow definitions remain useful when volume changes. Concentration differences give the same conversion only under the appropriate constant-volume or constant-volumetric-flow condition. Evaporation, feeding, gas expansion and polymerization shrinkage are all reasons to check that condition explicitly.

What is the denominator of conversion?Eq. 2

![What is the denominator of conversion?](https://ml-biomat.com/static/agent-math/098ca0dbb82183d68be1881a.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| X_{A} | Conversion of A; batch and flow label batch and steady-flow definitions | 1 |
| n_{A0}；n_{A} | Initial and current amounts of A in the same batch; 0 denotes the initial state | mol |
| F_{A0}；F_{A} | Inlet and outlet molar flows of A; 0 denotes the feed in the flow model | mol/min |
| C_{A0}；C_{A} | Corresponding initial or feed concentration, and current or outlet concentration | mol/L |

Reading the relationshipSubtract the amount remaining as A from the amount supplied, then divide by the supplied amount. Constant batch volume cancels from the amount ratio; constant volumetric flow cancels from the flow ratio. Only under those respective conditions does the concentration form follow. Multiply the dimensionless fraction by 100 to express a percentage.

A worked exampleA batch starting with 2.0 mol A and retaining 0.50 mol has conversion 0.75, or 75%. If evaporation reduces liquid volume from 2.0 L to 1.0 L, concentration changes from 1.0 to 0.50 mol/L. The resulting 50% concentration reduction differs from the actual 75% amount conversion.

ConditionsThe flow definition uses a steady-state balance with specified inlet and outlet. The last line applies to constant-volume batches or equal inlet and outlet volumetric flows. The simple examples contain no additional source of A from another feed or net reaction.

The identity of the counted entity also matters. During polymerization, conversion might describe consumed monomer molecules or reacted functional groups. These need not have the same denominator. A functional group is a local chemical structure able to undergo a particular reaction, such as a hydroxyl or carboxyl group, and a single molecule can carry several such groups. The number of polymer chains, their lengths and the formation of a connected network are additional questions. We will first use a single reactant A to establish clear material accounting, then connect consumption to desired products. This keeps a high monomer conversion from being confused with an automatic guarantee of the required material structure or performance.

## What sets the speed: concentration, temperature and reaction order

Pumps and flow meters can control the inlet and outlet terms of the balance, but the reaction term requires chemical kinetics. Kinetics describes how rapidly a transformation proceeds and how that speed changes with conditions. Holding temperature and other relevant variables fixed, we can measure the consumption rate at several concentrations of A. If doubling the concentration doubles the rate, a first-order relation may describe that range. If doubling it produces four times the rate, a second-order relation may apply. “First order” and “second order” name concentration exponents. They do not rank the sophistication of a reaction, nor do they automatically reveal the number of molecules involved in each elementary event.

How concentration enters a rate lawEq. 3

![How concentration enters a rate law](https://ml-biomat.com/static/agent-math/596ce0b6c23e68e3e124433c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| r_{A} | Positive consumption rate of A | mol/(L·min) |
| C_{A} | Concentration of A | mol/L |
| m | Reaction order with respect to A: the concentration exponent | 1 |
| k | Rate constant at the specified temperature; its units depend on m | (mol/L)^(1−m)/min |

Reading the relationshipThe exponent measures sensitivity to concentration. For m equal to one, doubling concentration doubles the rate; for m equal to two, it multiplies the rate by four. The units of k complete the concentration-power units to produce mol/(L·min). Rate constants for different orders cannot be compared as identical dimensional quantities merely because their numerical values match.

A worked exampleWith k=0.10 min⁻¹ and C_A=2.0 mol/L, the first-order rate is 0.20 mol/(L·min). A second-order constant of 0.050 L/(mol·min) gives the same initial rate. Halving concentration reduces the two rates to 0.10 and 0.050 mol/(L·min), respectively.

ConditionsThis is a single power-law approximation at fixed temperature and other relevant conditions. Kinetic evidence determines m. Changing concentrations of other reactants, catalysts or active centres belong in the full rate relation.

Products of concentrations have an intuitive starting point. Suppose two molecular species must meet before they have an opportunity to react. Keeping one population fixed while increasing the other creates more possible encounters. In a dilute, uniform system with a sufficiently simple mechanism, the rate may be proportional to both concentrations. If the two concentrations remain equal while decreasing together, their product appears as a concentration squared. Real mechanisms can also involve active-site formation, intermediate conversion or catalyst deactivation. Measured orders can consequently be fractional or negative. The overall chemical equation records the amounts transformed before and after reaction; its coefficients cannot generally replace experimental information about the rate law.

Polymerization illustrates why this distinction is useful. Step-growth reactions often involve encounters between two functional groups, whereas radical polymerization includes initiation, chain propagation and termination. Its monomer consumption also depends on the population of active chain ends. Calling every polymerization a second-order reaction would hide these differences. Even within one system, increasing viscosity can alter molecular transport and radical termination, so a simple rate relation measured early in the process may need revision later. The first- and second-order examples below are specified models for learning reactor calculations. A practical calculation should use the rate law appropriate to the reaction mechanism and the concentration range being considered.

Temperature does more than make molecules move a little faster. In his [1889 discussion of acid-catalyzed cane-sugar inversion](https://doi.org/10.1515/zpch-1889-0116), Arrhenius considered why a modest temperature increase could produce a much larger increase in reaction speed. He connected this sensitivity to a temperature-dependent population capable of reacting. A modern energy-barrier diagram provides a useful way to picture the issue: molecular rearrangement usually passes through configurations that are harder to reach than the starting state, and temperature changes the statistical opportunities to reach them. The hill in the diagram represents an energy change, rather than a literal obstacle inside the vessel.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe02/en/#en-s2)

Figure 1 · The question addressed by Arrhenius connects to a modern barrier picture: temperature changes access to reactive states. The schematic illustrates the concept; an apparent activation energy is determined from the temperature dependence of measured rates.

Comparing rates at two temperaturesEq. 4

![Comparing rates at two temperatures](https://ml-biomat.com/static/agent-math/62baf120047bcd9dd7c7824e.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| k(T) | Rate constant at temperature T | set by reaction order |
| A₀ | Arrhenius pre-exponential factor | same as k |
| E_{a} | Apparent activation energy | J/mol |
| R_{g} | Molar gas constant, approximately 8.314 | J/(mol·K) |
| T；T₁；T₂ | Absolute temperature and the two comparison temperatures | K |
| exp(z) | Exponential function with natural base e; z is a dimensionless argument | 1 |

Reading the relationshipDividing activation energy by R_gT gives a dimensionless ratio used in the exponential multiplier. For an interval with approximately constant pre-exponential factor and activation energy, the pre-exponential factor cancels in the two-temperature ratio. Temperatures are in kelvin: add 273.15 to degrees Celsius before substitution.

A worked exampleFor E_a=50,000 J/mol, increasing temperature from 300 to 310 K gives an exponent of approximately 0.647 and a rate-constant ratio of 1.91. A value of 0.10 min⁻¹ at 300 K becomes approximately 0.191 min⁻¹ at 310 K.

ConditionsApply within a temperature interval where the mechanism and fitted parameters remain appropriate. If concentrations also change, the actual rate still includes their contribution. Transport limitation or a mechanism change can alter the observed temperature dependence.

The exponential in the Arrhenius relation can initially look unfamiliar. An exponential describes a multiplicative change: changing temperature adjusts the rate constant by a factor, rather than adding a fixed increment. Engineers often compare the rate constants at two temperatures instead of separately calculating a large pre-exponential factor and a small exponential term. In this ratio, the pre-exponential factor cancels under the stated approximation. The worked example shows that the effect of a ten-degree temperature rise depends on both the starting absolute temperature and the apparent activation energy. The familiar suggestion that a reaction doubles in speed for every ten-degree rise is therefore a possible local approximation, rather than a fixed rule for all reactions.

For such a rate law to describe the local chemical process, mixing and temperature must be represented appropriately. A stirring shaft turning in a viscous liquid does not establish that a newly added drop has already mixed at the molecular scale. If much of the reaction happens before the drop disperses, local concentrations help determine the products. Ideal reactor models simplify these spatial details in explicit ways so that the effects of flow and reaction time become easier to see. They provide quantitative comparison models. Applying them involves checking whether mixing times, heat transfer and diffusion support the chosen assumptions; the word “ideal” describes those assumptions rather than an inherent property of real equipment.

## Time in a batch: why the last fraction takes longer

A batch reactor has no material flow across its boundary during the reaction stage. Feed is charged first, and the mixture is removed after reaching the intended state. Setting the inlet and outlet terms to zero leaves reaction as the cause of reactant loss. If liquid volume is constant, the amount balance can be written directly as a concentration change. Each small increase in conversion takes a small interval of time, and that interval is inversely related to the consumption rate at that stage. The integral sign adds these intervals along the reaction path. It plays the same accounting role as dividing a journey into short sections and using the speed on each section to determine total travel time.

Adding the time required for each small conversion stepEq. 5

![Adding the time required for each small conversion step](https://ml-biomat.com/static/agent-math/7cbbbb9fa5300fc0c7298196.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| t | Reaction time to the target conversion | min |
| C_{A0} | Initial concentration of A | mol/L |
| X_{A} | Target conversion of A | 1 |
| ξ；dξ | Conversion used as the integration variable, and a small increment in it | 1 |
| r_{A}(ξ) | Positive consumption rate of A at that conversion | mol/(L·min) |
| ∫₀ˣ | Integral summing contributions from zero conversion to the target | complete expression gives min |

Reading the relationshipInitial concentration multiplied by a conversion increment gives the concentration consumed over that step. Dividing by the current rate gives its required time. Integration adds all steps. The variable ξ distinguishes the changing conversion along the path from the final target X_A.

A worked exampleFor a constant zero-order rate of 0.020 mol/(L·min) and initial concentration 1.0 mol/L, 50% conversion consumes 0.50 mol/L and requires 25 min. A declining rate must instead be included at each stage of the integration.

ConditionsA uniform constant-volume batch with no inlet or outlet and zero initial conversion. The rate must be known along the operating path. Time-dependent temperature or other changing states must be included in the associated kinetic equations.

A first-order reaction makes this journey particularly easy to picture. In each short interval, the same fraction of the A currently present reacts. At the start, much A remains, so the absolute amount consumed per minute is large. Later, less remains, and the absolute decrease becomes smaller. Repeated removal in proportion to the remaining population produces exponential decay. A second-order reaction is more sensitive to concentration: when half the original concentration remains, its rate falls to one quarter of the initial value. Its curve therefore develops a slow tail more strongly. The two shapes reflect how reaction opportunities depend on concentration, even when the vessel and starting conditions otherwise look similar.

Remaining concentration for first- and second-order modelsEq. 6

![Remaining concentration for first- and second-order models](https://ml-biomat.com/static/agent-math/cffcedee089f9b91b1e3c0ba.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| C_{A}；C_{A0} | Current and initial concentrations of A | mol/L |
| X_{A} | Conversion of A | 1 |
| t | Reaction time | min |
| k₁ | First-order rate constant; 1 identifies the model order | min⁻¹ |
| k₂ | Second-order rate constant; 2 identifies the model order | L/(mol·min) |
| e | Base of the natural exponential, approximately 2.71828 | 1 |

Reading the relationshipA first-order process removes a fixed fraction of the current amount over each small interval, producing exponential decay. Integrating the concentration-squared second-order balance gives the growing denominator. Both k₁t and k₂C_A0t are dimensionless, and both remaining fractions equal one at zero time.

A worked exampleWith C_A0=1 mol/L, k₁=0.10 min⁻¹ and k₂=0.10 L/(mol·min), the initial rates match. After 10 min the remaining fractions are 0.3679 and 0.5000. Reaching 90% conversion requires 23.03 min for the first-order model and 90 min for the second-order model.

ConditionsUniform isothermal constant-volume batches with a single irreversible reaction obeying the stated order. Here k₁ and k₂ label two alternative models; in the later consecutive network the subscripts instead identify successive steps.

The time spent in the final part of the reaction can be calculated separately. With a first-order rate constant of 0.10 per minute, reaching 90 percent conversion takes about twenty-three minutes; reaching 99 percent takes about forty-six. The extra nine percentage points require another twenty-three minutes because this stage again removes 90 percent of the amount present at its beginning. For a second-order model with the same initial fractional consumption rate, progressing from 90 to 99 percent conversion is much more time-consuming. In the figure, the vertical axis is the remaining concentration divided by its starting value. Reaching a remaining fraction of 0.10 corresponds to 90 percent conversion.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe02/en/#en-s3)

Figure 2 · The models start at the same consumption rate, but the second-order reaction slows more strongly as concentration falls. The plotted quantity is the remaining fraction; conversion is one minus that fraction.

This slowing helps explain why high conversion often becomes a production bottleneck. To reduce residual monomer to a very low level, a process can continue reacting or, at an appropriate stage, separate some of the remaining small molecules. The time and energy requirements of these routes differ. Step-growth polymerization often requires very high functional-group conversion to obtain long chains, so late-stage reaction speed matters alongside the balance of reactive groups and the effects of small-molecule byproducts on equilibrium. Temperature, catalysts and feed schedules can all be adjusted, but each adjustment should be connected to the relevant mechanism. A flattening concentration curve alone does not identify which change will be most effective.

At identical temperature, initial concentration and rate law, the ideal batch reaction time contains no vessel-volume term. A one-litre and a hundred-litre batch can therefore follow the same concentration history within that model. Scaling up nevertheless changes the available heat-transfer area per unit volume, mixing distances and the flow generated by an agitator. Conditions that remain nearly uniform in a small flask may develop appreciable differences in a large vessel. The volume-independent kinetic time is useful precisely because it separates two questions: how long the chemistry needs under specified conditions, and what the larger equipment must accomplish to maintain those conditions throughout the material.

The end of reaction time is also not the immediate beginning of the next batch. Charging, heating, discharging and cleaning occupy equipment, so production capacity must be calculated over the complete operating cycle. A reaction lasting twenty-three minutes with ten minutes of auxiliary operations uses thirty-three minutes per cycle. This extra time will be included when batch and continuous options are compared later. For now, the central picture is that the material in a batch travels together from high to low concentration, with the duration of each stage determined by the corresponding reaction rate. The vessel does not expose the whole batch to the final low concentration from the outset.

## Reacting in flow: the tank and the tube

A tank can maintain a constant liquid volume while receiving and discharging equal volumetric flows. In an ideal continuously stirred tank reactor, complete mixing means that fresh feed rapidly joins the uniform contents. The outlet samples those contents, so its concentration equals the concentration throughout the tank. Fresh reactant does not first spend time reacting in an isolated region at its original feed concentration. It immediately enters an environment containing product and solvent. Under steady operation, the average concentration and temperature at each position remain constant with clock time, even though the molecules occupying those positions continually change. This is the flow model commonly abbreviated as CSTR.

The steady tank balance is consequently straightforward: the moles of A entering per minute, minus those leaving per minute, equal the amount consumed per minute throughout the reacting volume. Dividing that volume by the volumetric flow gives a time quantity called space time. For a constant-density, steady system with constant volume and all fluid participating in the flow, it also equals the mean residence time. A mean of twenty minutes does not assign twenty minutes to every molecule. A perfectly mixed outlet removes a sample of old and new material, so some molecules leave quickly while others remain longer. This distinction becomes particularly relevant when an intermediate product can undergo further reaction.

A stirred tank reacts at its outlet concentrationEq. 7

![A stirred tank reacts at its outlet concentration](https://ml-biomat.com/static/agent-math/3c3d0aff047c703b5401944b.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| τ | Space time based on inlet volumetric flow | min |
| V | Effective reacting-liquid volume | L |
| q | Constant inlet and outlet volumetric flow | L/min |
| C_{A0}；C_{A} | Feed concentration, and the common tank/outlet concentration | mol/L |
| r_{A}(C_{A}) | Positive consumption rate evaluated at the uniform tank concentration | mol/(L·min) |
| X_{A} | Conversion of A | 1 |
| k | First-order rate constant in the last line | min⁻¹ |

Reading the relationshipZero steady-state accumulation makes the inlet–outlet molar-flow difference equal total consumption. Dividing by the common flow gives space time as concentration loss divided by the tank reaction rate. Substituting first-order kinetics and rearranging yields the last line. Larger kτ gives more reaction within the available flow timescale.

A worked exampleFor V=10 L and q=1 L/min, τ=10 min. With k=0.20 min⁻¹, kτ=2 and conversion is 2/3, approximately 66.7%. A feed concentration of 1 mol/L gives an outlet near 0.333 mol/L.

ConditionsIdeal complete mixing, constant temperature and density, steady operation and unchanged volumetric flow. The last line additionally assumes a single irreversible first-order reaction. Identifying space time with mean residence time also requires all counted volume to participate in flow.

A plug-flow reactor uses a different picture. Imagine the fluid in a tube as a succession of thin slices moving forward. Each slice is uniform across the tube, and neighboring slices do not mix backward or forward along the flow direction. Reactant is progressively consumed as a slice travels, giving high concentration upstream and lower concentration downstream. During steady operation, a measurement made at one fixed location remains constant with clock time. A spatially changing concentration and a time-independent reading at a fixed position can therefore coexist. The first describes the journey of material; the second describes the stationary concentration pattern established by continuous operation.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe02/en/#en-s4)

Figure 3 · Complete mixing gives fresh and older material a common concentration. Ideal plug flow preserves concentration variation along the flow direction. Dots represent reactant A schematically rather than as a molecular count to scale.

Adding reaction time along a tubeEq. 8

![Adding reaction time along a tube](https://ml-biomat.com/static/agent-math/a8aadc1fe45582ce3b9d0de2.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| τ | Space time: effective reacting volume divided by volumetric flow | min |
| C_{A0} | Feed concentration of A | mol/L |
| X_{A} | Outlet conversion of A | 1 |
| ξ；dξ | Changing conversion along the tube and its small increment | 1 |
| r_{A}(ξ) | Positive consumption rate at the corresponding position and conversion | mol/(L·min) |
| ∫ | Integral adding the time contributions of small reaction segments | complete expression gives min |
| k | First-order rate constant | min⁻¹ |
| e | Base of the natural exponential | 1 |

Reading the relationshipEach fluid slice progressively reacts, with local consumption determined by its concentration. Summing small residence-time increments along the path gives the same integral form as the constant-volume batch calculation. First-order kinetics therefore retain exponential decay, with space time replacing elapsed batch time.

A worked exampleFor k=0.20 min⁻¹ and τ=10 min, conversion is 1−e⁻², approximately 86.5%. This uses the same rate constant and feed conditions as the 66.7% stirred-tank result at equal space time.

ConditionsIsothermal, constant-density, steady ideal plug flow, uniform across each section with no axial backmixing and zero inlet conversion. The last line applies to a single irreversible first-order reaction.

The chemical age of each plug-flow slice increases along the tube. Under constant temperature and density, and with the same initial state, the slice follows the same concentration history as an ideal batch. Elapsed batch time is replaced by the residence time accumulated along the flow path. For a simple reaction that becomes faster at higher reactant concentration, the upstream region uses the high feed concentration to react rapidly. A completely mixed tank, by comparison, uses its entire volume at the lower outlet concentration. For a first-order reaction reaching 90 percent conversion, plug flow requires a space time of about 2.3 times the inverse rate constant, whereas a single stirred tank requires nine times that inverse constant.

A physical tube does not automatically establish plug flow. Viscous fluid can move faster near the centre and more slowly near the wall, while a real stirred vessel can contain short-circuiting paths, poorly exchanged regions or incomplete local mixing. In 1953, Danckwerts organized the distribution of time spent in continuous-flow systems into a framework that could be measured and compared using tracers. That development made departures from the ideal pictures experimentally accessible. Here the two ideal limits provide the starting point; residence-time distributions can then refine the description. Model choice should follow the histories experienced by the material, rather than whether the equipment resembles a barrel or a tube.

### Allocating the same total volume

[Figure: Allocating the same total volume](https://ml-biomat.com/tutorials/biomaterials-courses/pe02/en/#en-s4)

An isothermal constant-density irreversible first-order reaction. k is the first-order rate constant and τ is total space time; their product is dimensionless. More tanks redistribute a fixed total volume.

Increasing reaction strength in the interaction increases all three conversions and lengthens their bars, but by different amounts. This dimensionless parameter multiplies the first-order rate constant by the total space time. It compares how quickly chemistry consumes reactant with how much time the equipment provides. When the product is small, little reaction occurs in any of the three arrangements. At larger values, the concentration histories produced by backmixing make a more visible difference. A fair comparison keeps feed conditions, temperature and total reacting volume fixed. Otherwise, an improvement obtained by doubling one vessel's size could be mistakenly attributed entirely to its flow pattern.

## Connecting reactors: cascades, parallel paths and recycle

A single completely mixed tank operating at low outlet concentration subjects its whole volume to the slow final stage of reaction. A natural alternative divides the total volume among several tanks in series. The first processes more concentrated feed, and subsequent tanks continue consuming the remaining reactant. Each tank is still internally uniform, but concentration differences between tanks are retained. Fresh material is no longer immediately mixed with the final product of the entire system. The sequence creates concentration steps along the flow path. Under the corresponding constant-temperature, constant-density conditions, increasing the number of smaller steps progressively approaches the continuous concentration variation of plug flow.

Equal tanks in series: decreasing concentration stage by stageEq. 9

![Equal tanks in series: decreasing concentration stage by stage](https://ml-biomat.com/static/agent-math/19a36b57e7802176679fce2c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| C_{A,N} | Concentration of A leaving tank N | mol/L |
| C_{A0} | Concentration entering the first tank | mol/L |
| N | Number of equal-volume tanks in series, a positive integer | 1 |
| k | Common first-order rate constant | min⁻¹ |
| τ_{tot} | Total effective volume divided by the common volumetric flow | min |
| X_{A,N} | Overall conversion after N tanks | 1 |

Reading the relationshipEach tank has one Nth of the total space time. A first-order stirred tank divides its inlet concentration by one plus k times its own space time. Repeating the same division N times gives the negative Nth power. Holding total space time fixed compares different allocations of the same combined volume.

A worked exampleFor k=0.20 min⁻¹ and τ_tot=10 min, N=1, 2 and 5 give conversions of 66.7%, 75.0% and 81.4%. To reach 90% at k=0.10 min⁻¹ and 1 L/min flow, three equal tanks require about 34.63 L in total.

ConditionsSteady isothermal constant-density operation with a single irreversible first-order reaction, equal perfectly mixed tanks and no additional interstage feeds or withdrawals.

Consider a total space time of ten minutes and a first-order rate constant of 0.20 per minute. A single tank gives about 67 percent conversion, two equal tanks in series give 75 percent, five give about 81 percent and plug flow gives about 86 percent. Total volume is unchanged: adding stages redistributes the volume rather than creating extra residence time. Alternatively, a target conversion can be fixed and the required total volume calculated for each arrangement. The figure compares concentration steps for one tank, two tanks and a longer cascade. It shows which portions of the system still operate at relatively high reactant concentration.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe02/en/#en-s5)

Figure 4 · Equal-volume tanks in series produce descending concentration steps for a first-order reaction. All rows use the same total space time; the upper left starts at inlet fraction one and the baseline is zero. Additional stages retain more reacting volume at higher concentration.

Parallel operation serves a different purpose. Total feed is divided among separate branches, processed independently and then recombined. If each branch receives flow in proportion to its volume, the branches have equal space times. Identical ideal tanks in parallel can then give the same conversion as a single tank with the same combined volume. Advantages may involve maintenance, manageable equipment size or changes in production load, rather than an inherent increase in conversion. Unequal flow allocation needs separate attention: one branch may carry material through too quickly while another holds it longer. Their outlet concentrations must be combined using flow-weighted amounts, rather than an unweighted arithmetic average.

Another arrangement sends part of a tube's outlet back to its inlet. This recycle stream mixes with fresh feed and dilutes its reactant concentration with material that has already reacted. For a fixed-volume, fixed-temperature reactor carrying out a simple positive-order reaction, more recycle shortens each passage through the reaction section while allowing material repeated passages. Both effects belong in the calculation. With strong recycle, the inlet and outlet concentrations of the reaction section become similar, and the behavior approaches that of a completely mixed tank. Recycle can also help real equipment maintain flow or transfer heat; those practical benefits should be distinguished from the concentration effect predicted by the ideal kinetic model.

Recycle mixing and the time for one passageEq. 10

![Recycle mixing and the time for one passage](https://ml-biomat.com/static/agent-math/f0dfd117e4fc7ae3a9b8c48f.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ℛ | Returned flow divided by fresh-feed flow | 1 |
| q_{R}；q₀ | Recycle and fresh-feed volumetric flows | L/min |
| C_{A0}；C_{A1}；C_{Af} | Concentrations in fresh feed, the mixed reactor inlet and the reactor outlet | mol/L |
| V | Effective volume of the reaction section | L |
| τ_{pass} | Space time for one passage through the reaction section | min |

Reading the relationshipAt the mixing point, incoming A per minute is the sum carried by fresh and returned streams. Dividing by total flow gives the mixed concentration. The reaction section carries 1+ℛ times the fresh flow, shortening its single-pass space time. That time differs from the system space time based on fresh feed.

A worked exampleWith ℛ=2, C_A0=1.0 mol/L and C_Af=0.10 mol/L, the mixed inlet is 0.40 mol/L. For V=10 L and q₀=1 L/min, the single-pass space time is 10/3 min, approximately 3.33 min.

ConditionsA constant-density steady recycle with additive volumes, a nonseparating splitter and negligible reaction at the mixing point. The example specifies outlet concentration to illustrate mixing. Complete design also solves the reaction-section kinetics for that concentration.

The denominator of a recycle ratio must be stated. Some conventions divide returned flow by fresh feed, while others divide it by the total flow entering the reaction section. Their numerical values differ. Here the ratio means returned volumetric flow divided by fresh volumetric flow. A recycle ratio of two therefore mixes one part fresh feed with two parts returned material, and the reaction section carries three times the fresh-feed flow. With one litre per minute of fresh feed and ten litres of effective reactor volume, the space time based on fresh feed remains ten minutes, while the time for a single passage through the reaction section is only about 3.3 minutes.

The order of connected reactor types can also matter. For an irreversible first-order reaction at a common temperature, exchanging the order of one plug-flow section and one stirred tank does not change the final remaining fraction. Each section multiplies its inlet concentration by a fixed factor, and those two factors commute. For a second-order reaction, the dependence on the concentration entering each section is nonlinear, so rearranging the sections can change the result. Parallel side reactions and consecutive reactions add product-distribution questions. Rules for equipment combinations should therefore be derived from the specified balance and kinetics rather than taken from a single ranking of reactor drawings.

## After the reactant disappears: steering it toward the desired product

Suppose A can form a desired product P or an unwanted product S. Conversion alone now leaves out an important part of the result. Consuming ninety of one hundred initial units while making only forty-five units of P differs substantially from consuming the same ninety while making eighty-one units of P. Selectivity describes the fraction of reacted feed directed toward the desired product. Yield describes the fraction of the original feed recovered as that product. To make the counting transparent, the following networks assume that one unit of A forms one unit of P or S. A reaction with different stoichiometric coefficients requires the appropriate conversion between these amounts.

Instantaneous selectivity, overall selectivity and yieldEq. 11

![Instantaneous selectivity, overall selectivity and yield](https://ml-biomat.com/static/agent-math/eafce064e00abe980a6060bc.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| β | Instantaneous fraction of parallel reaction directed toward P | 1 |
| r_{P}；r_{S} | Rates of formation of P and S from A | mol/(L·min) |
| S̄_P | Overall fraction of reacted A recovered as P | 1 |
| Y_{P} | Yield of P relative to initial or inlet A | 1 |
| C_{P} | Obtained P concentration, with no P initially or in the feed | mol/L |
| C_{A0}；C_{A} | Initial or inlet A concentration, and current or outlet concentration | mol/L |
| X_{A} | Conversion of A | 1 |

Reading the relationshipThe first line compares competing parallel rates at one instant or location. The second divides obtained P by consumed A; the third divides P by initial A. Multiplying the reacted fraction by the desired-product fraction within that reacted material gives the yield relative to the original feed.

A worked exampleStarting from 1.0 mol/L A and ending with 0.10 mol/L A and 0.72 mol/L P gives 90% conversion, 80% overall selectivity and 72% yield. Instantaneous parallel rates of 0.03 and 0.01 mol/(L·min) give 75% instantaneous selectivity, which need not equal the accumulated 80% value.

ConditionsOne unit of A forms one unit of P or S, with no initial or feed product. Concentration forms apply to constant-volume batches or constant-volumetric-flow steady systems. The first line describes parallel pathways. The last two also describe networks consuming P further; its net formation rate is then not an always-positive branching fraction.

Two parallel pathways resemble a branching route: at each instant, some reacting A flows toward P and some toward S, and the relative rates determine instantaneous selectivity. If the desired pathway is second order in A while the side pathway is first order, raising A concentration increases the desired rate more strongly. Reversing those orders can make a lower A concentration favorable. The relatively low, uniform concentration in a stirred tank may therefore help suppress a particular side reaction. Earlier, reactor volume was compared for a single reaction and a conversion target. Once the objective includes where the consumed reactant goes, the preferred concentration history can change.

With two reactants, feed scheduling can control their concentrations separately. If the desired pathway is more sensitive to A, while the unwanted pathway is more sensitive to B, one possible strategy is to keep A relatively abundant and feed B slowly so that it is consumed soon after arrival. This is a semibatch operation: the reacting contents receive additional material during the reaction, and their volume may increase. The amount balance must then be used instead of automatically retaining the constant-volume batch formula. Slow addition is beneficial only when its effect on the competing rate laws supports the desired outcome. The relevant issue is the concentration history established for each reactant.

A second common network converts A into P and then converts P into S. If P is the target, stopping too early leaves much unreacted A, while stopping too late loses P that has already formed. Undercooking and overcooking offer a familiar picture of formation followed by deterioration, although a real chemical application needs its actual steps identified. Collecting a useful intermediate or a particular range of degradation fragments may involve this kind of competition. The rate of change of P equals its formation rate minus its further-consumption rate. Its concentration reaches a maximum when those two rates become equal, even while A continues to disappear.

Peak timing for an intermediate in two consecutive stepsEq. 12

![Peak timing for an intermediate in two consecutive steps](https://ml-biomat.com/static/agent-math/0debb041ecff33a6fb89d9eb.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| C_{P}；C_{A0} | Intermediate P concentration and initial A concentration | mol/L |
| k₁；k₂ | First-order rate constants for A forming P and P forming S | min⁻¹ |
| k | Common rate constant when the two steps are equal | min⁻¹ |
| t；t_* | Reaction time and time at maximum P concentration | min |
| e；ln | Natural exponential base and its inverse function, the natural logarithm | 1 |

Reading the relationshipP forms from A while continuing toward S. Inserting the exponential decay of A into the formation-minus-consumption balance for P gives the difference of two exponentials. Setting the rate of change of P to zero gives the peak time. Equal rates use the continuous limiting expression in the third line rather than division of nearly zero differences.

A worked exampleFor k₁=0.10 min⁻¹ and k₂=0.050 min⁻¹, the peak occurs at 13.86 min and P reaches 50% of initial A. If both constants are 0.10 min⁻¹, the peak occurs at 10 min and reaches 1/e, approximately 36.8%.

ConditionsIsothermal constant-volume A→P→S with only A initially, two irreversible first-order steps and one-to-one stoichiometry. Applies to an ideal batch; residence time replaces t for plug flow under the same conditions.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe02/en/#en-s6)

Figure 5 · Composition for consecutive first-order A→P→S. At every time the three fractions sum to one. The P maximum occurs when formation and consumption balance, while A continues to decrease.

When both first-order steps have the same rate constant, the model predicts a maximum P concentration of only about 37 percent of the initial A concentration. This ceiling follows from the specified competing steps. Raising it calls for changing their relative speeds, removing P as it forms or establishing another chemical pathway. In a continuously stirred tank, newly formed P remains mixed with the reacting contents and can continue toward S. For the same first-order consecutive network and the same A conversion, ideal plug flow generally preserves a larger amount of the intermediate. The comparison can be traced to the different reaction histories experienced by material in the two flow patterns.

An intermediate formed and consumed in a stirred tankEq. 13

![An intermediate formed and consumed in a stirred tank](https://ml-biomat.com/static/agent-math/c73b2063832a2a7d49238138.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| C_{A}；C_{P} | Tank and outlet concentrations of A and P | mol/L |
| C_{A0} | Feed concentration of A | mol/L |
| k₁；k₂ | First-order rate constants for A→P and P→S | min⁻¹ |
| τ | Space time: effective tank volume divided by volumetric flow | min |

Reading the relationshipThe A balance gives the first relation. With no P in the feed, reaction formation must replace both P leaving in the outlet and P converting to S. Substituting the A concentration into the steady P balance yields the two denominator factors, reflecting A depletion and further P consumption.

A worked exampleFor k₁=0.10 min⁻¹, k₂=0.050 min⁻¹ and τ=10 min, the remaining A fraction is 0.50 and the P yield is 0.333. At the same A conversion, batch or plug flow reaches a P fraction near 0.414 after 6.93 min.

ConditionsIsothermal constant-density steady ideal mixing, feed containing only A and inert components, and two irreversible one-to-one first-order steps A→P→S.

### When to collect the intermediate

[Figure: When to collect the intermediate](https://ml-biomat.com/tutorials/biomaterials-courses/pe02/en/#en-s6)

An ideal isothermal constant-volume batch, initially containing only A, with irreversible first-order A→P→S. The first constant k₁ is fixed at 0.10 min⁻¹; k₂ is the second-step constant. The vertical dashed line marks the selected time.

Temperature can alter these competitions as well. If two parallel pathways follow Arrhenius relations, the pathway with the larger apparent activation energy is usually more temperature-sensitive. Greater sensitivity does not mean it is faster at every temperature, because its pre-exponential factor and concentration dependence also matter. A consecutive network requires tracking both the formation and loss of P. Heating may move its peak to an earlier time without increasing the peak height. The interactive graph changes the second-step rate relative to the first. Comparing the position and height of the P peak with the composition at a chosen observation time makes the distinction between extensive reaction and abundant desired product visible.

## Reactions can run backward: equilibrium and the other role of temperature

The main examples so far use one-way arrows, but many bond-forming and bond-breaking processes can proceed in both directions. In a simplified condensation, A and B form P and a small molecule S; P and S can also react to regenerate A and B. Initially, little product is present and the forward process dominates. As products accumulate, the reverse rate becomes more important. Chemical equilibrium is reached when equal amounts transform in the two directions per unit time, leaving the macroscopic composition unchanged. This differs from the steady state of a flowing reactor. Equilibrium concerns opposing chemical processes, whereas a reactor steady state concerns the combined balance of flow and reaction.

Nineteenth-century chemists progressively separated the extent a reaction reaches from the speed at which it proceeds. Van 't Hoff's [1884 Studies in Chemical Dynamics](https://dbc.library.uu.nl/handle/20.500.14918/319162) brought reaction progress, equilibrium and temperature relationships into a connected framework. That distinction helps explain an apparently contradictory observation: a temperature increase can bring a system to equilibrium sooner while lowering the equilibrium product fraction of an exothermic reaction. Rate describes the journey toward the final composition. Equilibrium describes the point where opposing processes balance under specified conditions. The two questions require different quantities even though temperature can influence both.

Composition where forward and reverse rates balanceEq. 14

![Composition where forward and reverse rates balance](https://ml-biomat.com/static/agent-math/ff7d35957a83758442e9c973.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| r_{A} | Net consumption rate of A: forward minus reverse rate | mol/(L·min) |
| k_{f}；k_{r} | Second-order constants for forward A+B→P+S and reverse reaction | L/(mol·min) |
| C_{A}；C_{B}；C_{P}；C_{S} | Concentrations of the four species | mol/L |
| K | Dimensionless equilibrium constant in this ideal-mixture model | 1 |
| X_{A,e} | Equilibrium conversion of A; e identifies equilibrium | 1 |
| √K | Nonnegative square root of K | 1 |

Reading the relationshipAt zero net rate, forward and reverse concentration products balance. Starting from equal A and B concentrations with no P or S gives equal reactant depletion and equal product formation. The equilibrium ratio becomes the square of converted fraction divided by unconverted fraction. Taking the positive square root and rearranging yields the last line.

A worked exampleFor K=9 the square root is 3, so equilibrium conversion is 3/4, or 75%. Starting with 1 mol/L each of A and B gives 0.25 mol/L each reactant and 0.75 mol/L each product. Their concentration-product ratio is 0.75²/0.25²=9.

ConditionsA simple reversible reaction represented by the stated forward and reverse laws, at constant volume with ideal mixing. The last line additionally requires equal initial A and B and no initial products. Standard-concentration factors cancel for this two-to-two stoichiometry. General nonideal equilibria use activities; arbitrary empirical rate-constant ratios are not automatically thermodynamic equilibrium constants.

For the simple model with equal initial amounts of A and B and no initial products, an equilibrium constant of nine gives 75 percent equilibrium conversion, rather than 90 percent. Both P and S increase as reaction proceeds, while both A and B decrease. The equilibrium expression therefore contains two products of concentrations. Taking the square root recovers the corresponding ratio for one matched pair. Unequal initial reactant amounts, some S already present or appreciable departures from ideal mixing change this simplified result. The more general calculation retains the complete material balance and, where needed, uses activities to describe chemically effective concentrations.

How temperature shifts equilibriumEq. 15

![How temperature shifts equilibrium](https://ml-biomat.com/static/agent-math/5d5d038f121e33c7af2eef97.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| K(T₁)；K(T₂) | Equilibrium constants at the two temperatures, using the same standard-state convention | 1 |
| T₁；T₂ | Two absolute temperatures being compared | K |
| ΔH° | Standard molar reaction enthalpy; negative for an exothermic reaction | J/mol |
| R_{g} | Molar gas constant, approximately 8.314 | J/(mol·K) |
| ln | Natural logarithm, the inverse of the exponential function | 1 |

Reading the relationshipThe logarithm records the relative change in equilibrium constant. Raising temperature decreases 1/T. For negative reaction enthalpy, the right side is negative and the equilibrium constant decreases. Exponentiating the calculated logarithmic ratio gives the multiplier relating the two constants.

A worked exampleFor ΔH° approximately −20,000 J/mol, heating from 300 to 310 K gives a right-hand side near −0.259 and a K ratio near 0.772. An initial K of 9 becomes about 6.95. Under the preceding equation’s initial-mixture assumptions, equilibrium conversion is then about 72.5%.

ConditionsStandard reaction enthalpy is approximately constant over the interval, with a consistent standard-state definition of K. Wider intervals may require its temperature dependence. The equation concerns equilibrium position; kinetics determine the time needed to approach it.

The reaction enthalpy in the van 't Hoff relation describes the thermal effect of the specified transformation at the stated reference conditions. A positive value corresponds to an endothermic reaction and a negative value to an exothermic one. This quantity has a different role from the activation energy in the Arrhenius relation. Activation energy characterizes the temperature sensitivity associated with crossing the reaction barrier; reaction enthalpy concerns the energy difference between reactant and product states. A mountain route helps distinguish its highest point from the height difference between its starting and ending locations. A journey ending downhill can still require an initial climb. Quantitative use requires values appropriate to the actual reaction and temperature interval.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe02/en/#en-s7)

Figure 6 · An ideal equimolar example with equilibrium constant nine and initial A and B concentrations of 1 mol/L each. The connection between kinetics and equilibrium discussed in van ’t Hoff’s 1884 work is illustrated by ongoing transformations that balance in amount.

For a condensation that generates a small molecule, removing water or another byproduct can reduce the reverse reaction and allow additional forward conversion. The composition has changed; the operation has not made a catalyst increase the equilibrium constant. A catalyst provides another reaction pathway and can accelerate approach to equilibrium, while the equilibrium position at the same temperature remains determined by thermodynamics. In a viscous polymer system, the small byproduct must also move from the interior to a surface and then enter the gas phase. Mixing, surface renewal, vacuum operation and devolatilization can therefore become part of the strategy for advancing an equilibrium-limited reaction.

A practical temperature program often accommodates several needs. At lower temperature, equilibrium may favor the desired composition but reaction may proceed slowly. At higher temperature, reaction can accelerate while reverse reaction, degradation or unwanted pathways also become more important. Staged operation can assign different tasks to different parts of the process: substantial conversion may first occur under readily mixed conditions, followed by a stage designed to remove small molecules efficiently. The intended change should be named at each step, whether it concerns chemical rate, equilibrium composition, transport distance or residence time. A complicated process then becomes a connected set of effects that can be calculated and investigated separately.

## From calculation to choice: building a reactor proposal

Consider a specified comparison: an isothermal, constant-density, irreversible first-order reaction has a rate constant of 0.10 per minute, the feed is one litre per minute, and the desired conversion is 90 percent. With no side reaction included, plug flow requires about 23.03 litres of effective reacting volume, whereas a single stirred tank requires ninety litres. Three equal stirred tanks in series require about 34.63 litres in total, or 11.54 litres each. All three results use the same reaction and feed conditions. The comparison therefore isolates how backmixing changes the volume needed to achieve the conversion target, rather than mixing together changes in equipment size and chemistry.

A batch option still needs about 23.03 minutes of reaction time to reach the same conversion, but auxiliary operations must be included to match the average processing target of one litre per minute. If charging, discharging and other necessary operations take ten minutes per cycle, a single ideal batch vessel must process about 33.03 litres per batch to reach that average throughput. The calculated volume is the effective liquid charge. The geometric vessel capacity is a further design question involving the required operating space. Omitting auxiliary time would overstate the average production capacity available from the batch arrangement.

Including auxiliary operations in average throughputEq. 16

![Including auxiliary operations in average throughput](https://ml-biomat.com/static/agent-math/3545d03e7287b9886044d0a2.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| q̄_batch | Long-run average liquid volume processed per minute | L/min |
| V_{b} | Effective processed volume per batch | L |
| t_{r} | Reaction time per batch to the target state | min |
| t_{a} | Auxiliary time per batch, without double-counting reaction time | min |

Reading the relationshipProcessed volume divided by complete cycle time gives average throughput. The denominator includes the stages occupying the same equipment. Operations performed in parallel by different equipment require the actual schedule to define the cycle rather than automatic addition of every duration.

A worked exampleWith 23.03 min reaction time, 10.00 min auxiliary time and 33.03 L per batch, average throughput is 1.00 L/min. Keeping the charge at 23.03 L would give only about 0.697 L/min over the complete cycle.

ConditionsIdentical repeated cycles in one item of equipment operating through the stated sequential stages. V_b is effective processed volume; geometric capacity and operating space are separate design quantities.

Volume is one part of a reactor proposal. A viscous feed may require substantial pressure drop to maintain flow through a tube. A strongly exothermic reaction requires enough heat removal to maintain the temperature used in the kinetic calculation. A product whose formulation must be tracked batch by batch may fit a batch production arrangement. If the desired product is an intermediate, its yield curve should accompany the conversion curve. Biobased monomers and degradable materials may also introduce heat-sensitive structures, solvent compatibility or final-residue requirements. Each consideration should connect to a physical or chemical process so that the equipment choice becomes an explainable decision.

The same reasoning sequence works for a new reaction. Identify whether the counted entity is a monomer, functional group or intermediate, and write its flow and reaction balance. State how the rate depends on concentration and temperature, and whether volume changes. Then give each candidate reactor its corresponding material history and calculate conversion, desired-product fraction and throughput. Negative concentrations, conversion fractions above one or an unconverted mixture of seconds and minutes in rate constants point back to definitions and units. Units are part of the reasoning: they reveal whether a term represents an amount, an amount per time or an amount per volume per time.

Consider: does splitting one tank into two parallel tanks raise conversion?

If total effective volume and total feed flow remain fixed, and each branch receives half the volume and half the flow, each branch has the same space time as the original tank. At the same temperature and feed composition, identical ideal stirred tanks then give the same outlet concentration as before, and recombining the streams preserves it. In a series arrangement, the first outlet instead becomes the second inlet. The concentration history changes, allowing a simple positive-order reaction to reach a higher conversion at the same combined volume.

Consider: why can higher conversion reduce intermediate yield?

In the consecutive network where A forms P and P forms S, more time consumes additional A but also consumes P. Beyond the P maximum, waiting longer raises A conversion while lowering the yield of P. Move the observation time to either side of the peak in the interactive graph and compare the remaining A and the accumulated P. The exercise shows why a goal such as “increase the extent of reaction” should also identify the chemical species that the process is intended to preserve.

With these balances in place, the internal organization of more complicated equipment becomes readable. Some regions maintain high concentration, some mix material of different ages, some remove products, and some mainly extend waiting time. The three ideal reactor models establish several basic histories that material can experience. Combining them with kinetics, selectivity and equilibrium explains why the same chemical transformation may call for different equipment and provides a common language for studying real flow, heat transfer and industrial polymerization processes.
