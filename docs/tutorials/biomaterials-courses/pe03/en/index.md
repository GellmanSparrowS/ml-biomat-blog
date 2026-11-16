# Why Material Spends Different Amounts of Time in the Same Reactor

Source: https://ml-biomat.com/tutorials/biomaterials-courses/pe03/en/
Language: en

An average of ten minutes in a heated vessel does not give every portion of material ten minutes of treatment. Following a tracer from entry to exit reveals how residence times are distributed, measured and calculated, and how these flow histories affect conversion, polymer chain lengths and latex particle sizes.

## What different histories hide inside a ten-minute average?

Place a batch of biscuits in an oven together and remove them together ten minutes later, and their heating times are approximately equal. Now imagine a continuous conveyor on which some biscuits take a shortcut while others make a detour. An average of ten minutes can conceal both underheated and overheated portions. Flowing polymer solutions, emulsions and melts can experience comparable differences, although their routes are hidden inside the equipment. For heat-sensitive monomers, intermediates that continue reacting or materials that degrade with prolonged exposure, these differences can be more informative than a single average. Residence-time analysis provides a way to describe them quantitatively.

Residence time is the interval between a specified portion of material crossing a defined inlet and leaving through a defined outlet. Imagine marking a group of fluid elements entering at the same instant, then recording when those marks emerge. Some appear quickly, some near the average time and some much later, forming a tail. Plotting the fraction leaving within each time interval gives a residence-time distribution. The inlet and outlet boundaries need to be specified first. If a long sampling tube sits between the vessel and the detector, the measured interval includes that tube as well as the vessel, unless its contribution is separately accounted for.

A discrete example makes the idea concrete. Suppose one hundred equal portions of tracer enter together: twenty leave near five minutes, sixty near ten minutes and twenty near fifteen minutes. Their mean is ten minutes, but this result differs from all one hundred portions leaving at exactly ten minutes. To calculate the mean, multiply each time by its corresponding fraction and add the contributions. A more abundant group has greater influence. Similar weighted averages appear in particle-size and molecular-weight analysis, but their weights may be based on particle number, mass or signal intensity. Identifying what supplies the weight is part of understanding any reported average.

Density counts intervals; the cumulative curve adds themEq. 1

![Density counts intervals; the cumulative curve adds them](https://ml-biomat.com/static/agent-math/bb993a9a0f5a41ecfdfd107b.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| t | Elapsed time from marking the inlet | min |
| E(t) | Outlet residence-time probability density | min⁻¹ |
| F(t) | Cumulative fraction that has left by time t | 1 |
| u；du | Time variable inside the integral and its small interval width | min |
| dt | A small time interval | min |
| ∫；∞ | The integral sums small areas; infinity extends the count over all departure times | the integrated fraction is dimensionless |

Reading the relationshipDensity multiplied by a time width gives the fraction leaving within that interval, so inverse minutes cancel minutes. The first integral adds all departure fractions to one. The second stops at the specified time t. The variable u distinguishes times inside the sum from its upper limit.

A worked exampleAn average density of 0.08 min⁻¹ between 5 and 6 min means about 8% leaves during that minute. Cumulative values F(5)=0.30 and F(6)=0.38 give the same 8% difference.

ConditionsThe population is marked at a common inlet time, residence times are nonnegative, and all material is ultimately counted at the specified outlet. An ordinary continuous density height is not a point probability. Ideal plug flow uses a delta distribution for its concentrated response.

For continuously varying time, the height of a density curve is not the probability of leaving at one exact instant. Height multiplied by a small time width gives the fraction leaving within that interval. The area under the entire curve is one, representing all of the counted material eventually leaving. The vertical axis therefore has inverse-time units, such as per minute. A cumulative distribution answers a different question directly: what fraction has already left by a specified time? It progresses from zero toward one. The density and cumulative curves describe the same population; one shows the contribution of each short interval, and the other adds all preceding contributions.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe03/en/#en-s1)

Figure 1 · Example: three tanks in series with a 10 min total mean. The shaded density area from 8 to 12 min equals the cumulative-fraction difference between those times. Density height alone is not a departure probability.

The spread of histories also needs a measure. Subtract the mean from each residence time to obtain its deviation. Positive and negative deviations would cancel, so square them before taking their weighted average. This gives the variance, with units of time squared. Taking its square root gives the standard deviation, returning to ordinary time units. In the five-, ten- and fifteen-minute example, the mean is ten minutes, the variance is ten square minutes and the standard deviation is approximately 3.16 minutes. Each operation has a counting purpose: variance measures the typical squared distance from the mean while retaining the fractions of material represented by each time.

Mean, variance and standard deviationEq. 2

![Mean, variance and standard deviation](https://ml-biomat.com/static/agent-math/29cb55c5b252c411e0930335.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| t | Elapsed time from marking the inlet | min |
| t̄ | Mean residence time of the distribution | min |
| E(t) | Outlet residence-time probability density | min⁻¹ |
| σ_{t}² | Residence-time variance: the mean squared deviation | min² |
| σ_{t} | Residence-time standard deviation | min |
| dt；∫；∞ | Small time width, integration over all times and an infinite upper limit | set by the integrand |
| √ | Nonnegative square root, restoring time units from squared-time units | gives min in the final line |

Reading the relationshipEach time is weighted by the corresponding material fraction. Variance first subtracts the mean and squares the deviation, preventing early and late differences from cancelling. Its square root gives a spread with the same units as mean time.

A worked exampleFractions of 20%, 60% and 20% at 5, 10 and 15 min give a 10 min mean. Weighted squared deviations give 0.2×25+0.6×0+0.2×25=10 min². The standard deviation is √10≈3.16 min.

ConditionsThe corresponding first and second moments must exist. A long-tailed distribution can have a finite mean but no finite variance. A finite recording window yields statistics of the data actually captured in that window.

To compare equipment with different overall processing speeds, use each system's mean time as its time unit. A portion that stays twice the mean has dimensionless time two; one that stays half the mean has dimensionless time 0.5. Rescaling the horizontal axis requires a corresponding change in density height so that the total area remains one. Dividing variance by mean time squared gives a relative measure of spread. This comparison is useful, but it still does not replace the full curve. Two distributions with the same mean and variance can differ in shape, with one containing two peaks and another having a pronounced late tail.

Using mean residence time as the time unitEq. 3

![Using mean residence time as the time unit](https://ml-biomat.com/static/agent-math/ae56b292ff2cb8f5ee9fb9e5.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| t | Elapsed time from marking the inlet | min |
| t̄ | Mean residence time of the distribution | min |
| θ | Dimensionless time, actual time divided by mean time | 1 |
| E(t) | Outlet residence-time probability density | min⁻¹ |
| E_θ(θ) | Probability density on the dimensionless-time axis | 1 |
| σ_{t}² | Dimensional time variance | min² |
| σ_θ² | Dimensionless-time variance | 1 |

Reading the relationshipRescaling the horizontal axis changes each interval width. Multiplying density by the mean time preserves the fraction represented by its area. Variance contains squared time deviations, so it is divided by mean time squared.

A worked exampleA 10 min mean and 5 min standard deviation give variance 25 min² and dimensionless variance 0.25. A time of 20 min corresponds to θ=2. A density of 0.01 min⁻¹ there becomes E_θ=0.10.

ConditionsThe mean is positive and finite; a variance ratio also requires finite variance. Dimensionless variance has no universal upper bound of one.

## Marking the fluid: measuring a distribution with tracers

Adding a little color to the inlet of a transparent vessel and watching for its appearance at the outlet captures the basic idea of a tracer experiment. Measurements can use a suitable dye, salt, fluorescent molecule or another detectable marker, depending on the fluid and detector. A useful tracer follows the phase being studied, is added in a small enough amount to avoid appreciably changing density, viscosity or flow, and remains detectable without reacting, adsorbing or settling. Choosing the tracer means making its history representative of the material of interest. Otherwise the experiment may mainly measure a new interaction introduced by the marker itself.

In his [1953 study of continuous-flow systems](https://doi.org/10.1016/0009-2509%2853%2980001-1), Danckwerts organized the different times spent inside equipment into distribution functions that could be defined, measured and used in calculations. This approach made it possible to test ideal pictures such as complete mixing and plug flow without first mapping every internal fluid path. A short tracer input and its full outlet response turn a broad question about flow quality into more specific ones: how much material leaves early, what is the mean time, and which portions remain unusually long? The experimental response can then guide the choice of a flow model.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe03/en/#en-s2)

Figure 2 · A tracer-pulse schematic connects Danckwerts’s analysis of continuous-flow histories to measurable quantities. The device and curves explain the experimental logic and do not reproduce a particular historical apparatus.

The pulse method introduces a known amount of tracer over a short interval and then records outlet concentration. At constant volumetric flow, concentration multiplied by the volume leaving during a small interval gives the amount of tracer leaving in that interval. Summing over the complete response checks how much of the injected tracer has been recovered. Dividing each interval's amount by the total recovered amount produces a distribution. Material accounting is the foundation; normalization converts quantities to fractions. Normalizing a truncated curve does not restore its missing tail, and normalizing a response affected by wall adsorption does not remove that interaction.

Converting outlet concentration to departure fractionsEq. 4

![Converting outlet concentration to departure fractions](https://ml-biomat.com/static/agent-math/bc41e3ce1f4a5affe43f07cd.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| M_{rec} | Total tracer mass recovered at the outlet | mg |
| q | Constant outlet volumetric flow | L/min |
| c(t)；c(u) | Background-corrected outlet tracer mass concentration | mg/L |
| t | Elapsed time from marking the inlet | min |
| u；dt；du | Integration time variable and small time intervals | min |
| E(t) | Outlet residence-time probability density | min⁻¹ |
| ∫；∞ | Integral covering the response from injection through its complete tail | flow times the concentration integral gives mg |

Reading the relationshipConcentration times flow is tracer mass leaving per minute. Multiplication by an interval gives its departing mass. Integrating gives total recovery, and dividing by this mass gives the departure density. Constant flow cancels, allowing normalization of the concentration curve alone.

A worked exampleAn outlet concentration integral of 20 mg·min/L at 0.50 L/min corresponds to 10 mg recovered tracer. An instantaneous concentration of 1.0 mg/L gives density 0.050 min⁻¹.

ConditionsA short pulse, stable flow and an inert tracer representative of the fluid. Compare recovered and injected masses. If a tail is missing or tracer is irreversibly lost, normalization by recovered mass describes the recorded population; the corresponding experimental information must be completed.

Background signal should be measured before injection and subtracted during analysis. Even a small persistent background can contribute appreciably when integrated over a long recording. Detector response time, sampling-line volume and input-pulse width also matter. An injection lasting two minutes produces an outlet width containing both the spread already present at the inlet and the spread introduced by the equipment. Measuring inlet and outlet signals allows the known input to be included in response analysis. Alternatively, injection can be made much shorter than the flow timescale to be resolved. A narrow pulse is an approximation whose quality depends on that comparison.

The step method changes the input in another way. At a defined starting time, the inlet tracer concentration rises from zero to a fixed value while total flow remains unchanged. If the equipment initially contains none of that tracer, outlet concentration gradually approaches the inlet value. Under linear tracer conditions, the outlet-to-inlet concentration ratio gives the cumulative distribution. The picture resembles a vessel gradually being replaced by newly marked fluid. A ratio of 0.8 corresponds to a cumulative fraction of 80 percent. Pulse input directly reveals the density shape, whereas step input directly reveals the cumulative curve; the two representations are mathematically connected.

Reading a cumulative distribution from a step responseEq. 5

![Reading a cumulative distribution from a step response](https://ml-biomat.com/static/agent-math/bd8e365a8181a696a94c7616.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| F(t) | Cumulative fraction that has left by time t | 1 |
| c_{out}(t) | Background-corrected outlet concentration following the step | mg/L |
| c₀ | Constant inlet tracer concentration after the step | mg/L |
| E(t) | Outlet residence-time probability density | min⁻¹ |
| t | Elapsed time from marking the inlet | min |
| dF/dt | Instantaneous change rate of cumulative fraction with time | min⁻¹ |

Reading the relationshipAfter the inlet is switched to a constant tracer concentration, the emerging marked fraction gives the cumulative response. Dividing by inlet concentration produces a fraction from zero to one. Its increase per unit time is the density, expressed as the time derivative of the cumulative function.

A worked exampleFor a 2.0 mg/L inlet step and a 1.6 mg/L outlet reading at 10 min, F(10)=0.80. A local cumulative increase of about 0.03 per minute corresponds to density about 0.03 min⁻¹.

ConditionsInitially tracer-free equipment, a step from zero to a fixed inlet concentration, unchanged total flow and linear time-invariant tracer transport. Differentiating noisy measurements requires attention to resolution and smoothing.

Integration and differentiation behave differently when applied to measured data. Adding small areas under a density curve to obtain a cumulative curve tends to smooth local noise. Differentiating a cumulative curve compares small differences between neighboring measurements and can amplify noise. Selecting the experimental input therefore involves detector resolution and sampling interval as well as the physical process. Tracer recovery, flow stability and the duration of tail recording should remain part of the experimental analysis. Together with the curve, they help establish which features describe the fluid and which could arise from measurement or tracer behavior.

## One tank, many tanks and a train of fluid slices

Consider an ideal completely mixed tank with fixed volume and equal inlet and outlet flows. After a small tracer pulse is instantly mixed into it, the outlet removes the same fraction of the tank's contents during each short interval. Initially much tracer is present, so much leaves per unit time. Later less remains, and the amount leaving becomes smaller. Removal proportional to the remaining quantity produces exponential decay. Because entering material immediately joins the whole tank, the ideal model permits some tracer to appear at the outlet almost immediately and a small amount to remain after many mean residence times. Its broad time distribution follows directly from the mixing assumption.

The exponential residence-time distribution of complete mixingEq. 6

![The exponential residence-time distribution of complete mixing](https://ml-biomat.com/static/agent-math/a85e2087224ca40516d3156a.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| τ | Space time, equal to mean residence time in this model | min |
| V | Effective volume fully participating in flow and mixing | L |
| q | Constant volumetric flow | L/min |
| t̄ | Mean residence time of the distribution | min |
| t | Elapsed time from marking the inlet | min |
| E(t) | Outlet residence-time probability density | min⁻¹ |
| F(t) | Cumulative fraction that has left by time t | 1 |
| σ_{t}² | Residence-time variance | min² |
| e；exp | Natural exponential base and exponential-function notation | 1 |

Reading the relationshipComplete mixing removes a fixed fraction of the remaining tracer per unit time, giving exponential decay. The factor 1/τ normalizes total density area to one. Integration gives the cumulative curve; its first and second moments give mean τ and variance τ².

A worked exampleFor V=10 L and q=1 L/min, τ=10 min. Cumulative departure is approximately 0.632 at 10 min, 0.865 at 20 min and 0.950 at 30 min. Standard deviation is 10 min.

ConditionsConstant-volume, constant-density steady ideal mixing, with all effective volume exchanged and no tracer reaction or adsorption. Steady state describes the underlying flow; the tracer-pulse response itself changes with time.

For a ten-minute mean, ten minutes is not the time by which exactly half has left. Approximately 63.2 percent has emerged, leaving about 36.8 percent still inside. Recovering 95 percent takes roughly three mean residence times. A ten-minute mean results from the weighted combination of many early departures and a smaller number of later ones. The density curve is nonzero from the starting instant in this ideal model. Real equipment may add a finite transport delay from the inlet to the region sampled by the outlet, so that immediate response should be understood as a property of the ideal mixing limit.

Now divide the same total volume among several equal tanks in series. Material must pass through each one, so its total history combines several waiting times. The mean time per tank decreases while the total mean remains unchanged. Extremely short and extremely long total histories become less common. One stage may happen to be passed quickly, but the remaining stages still take time; a long stay in one stage does not require equally long stays in the others. As the number of equal stages rises, the overall distribution becomes more concentrated around its mean. The model makes precise how a cascade can reduce the spread without increasing total volume.

How equal tanks in series narrow the distributionEq. 7

![How equal tanks in series narrow the distribution](https://ml-biomat.com/static/agent-math/88af164d6822a82688bce0bb.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| N | Number of equal perfectly mixed tanks in series, a positive integer | 1 |
| θ | Time divided by total mean residence time | 1 |
| E_θ | Density on the dimensionless-time axis | 1 |
| E(t) | Outlet residence-time probability density | min⁻¹ |
| t̄ | Mean residence time of the distribution | min |
| t | Elapsed time from marking the inlet | min |
| σ_{t}²；σ_θ² | Dimensional time variance and dimensionless variance | min² and 1, respectively |
| (N−1)! | Factorial multiplying integers from 1 through N−1; 0! is defined as 1 | 1 |
| e；exp | Natural exponential base and exponential-function notation | 1 |

Reading the relationshipTotal residence time adds N well-mixed waiting stages. Each has one Nth of the total mean, and the independent stage variances add, giving the inverse-N total variance. The first line gives the resulting shape. At N=1 it recovers the single-tank exponential, including its limiting value at θ=0.

A worked exampleFor a 10 min total mean and N=4, variance is 25 min² and standard deviation is 5 min. With N=2 at θ=1, E_θ=4e⁻²≈0.541, giving E(10)≈0.0541 min⁻¹.

ConditionsFixed total effective volume and flow, equal completely mixed tanks, and no interstage feed, selective separation or additional delay. A fitted equivalent tank count needs its own model interpretation.

### Narrowing a distribution at the same mean

[Figure: Narrowing a distribution at the same mean](https://ml-biomat.com/tutorials/biomaterials-courses/pe03/en/#en-s3)

Equal perfectly mixed tanks at constant flow. Changing tank count keeps total mean time fixed. Density area represents departing material fraction; the plotted time range extends to four times the mean.

The interactive graph holds total mean time fixed while changing the number of equal tanks. A single-tank curve is largest at the earliest times and has a long tail. Curves for two or more tanks first rise and then fall, with a peak whose position changes as stages are added. A taller peak does not mean more total material: the narrowing curve retains unit area. For a ten-minute total mean, one tank has a ten-minute standard deviation, whereas four equal tanks in series have a five-minute standard deviation. When real equipment is represented by an equivalent number of tanks, that fitted number need not equal the physical count of vessels.

Ideal plug flow is the limiting picture in which all material entering at the same instant leaves after the same time. Its spread is zero. The cumulative curve remains zero until that time and then jumps to one. Its density requires a concentrated distribution with unit area and vanishing width, rather than an ordinary finite-height curve. This mathematical object is the Dirac delta distribution. Its defining role is what happens when it is integrated. A vertical arrow labeled with unit area is a useful drawing convention, preserving the meaning without pretending that the arrow height is an ordinary measurable density value.

All material arrives after the same intervalEq. 8

![All material arrives after the same interval](https://ml-biomat.com/static/agent-math/37b8acb357aca271c7c8502d.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| E(t) | Outlet residence-time probability density | min⁻¹ |
| t | Elapsed time from marking the inlet | min |
| τ | Residence time shared by all material | min |
| δ(t−τ) | Dirac delta distribution concentrated at τ with unit integrated area | min⁻¹ |
| F(t) | Cumulative fraction that has left by time t | 1 |
| t̄ | Mean residence time of the distribution | min |
| σ_{t}² | Residence-time variance | min² |

Reading the relationshipNo marked material leaves before τ, and all leaves at τ, producing a step in the cumulative curve. The delta distribution preserves the unit area of this concentrated departure. Every time equals the mean, so all deviations and the variance are zero.

A worked exampleAt τ=10 min, cumulative departure remains zero through 9.9 min and is one at and after 10 min. A stirred tank with the same mean has released only about 63.2% by 10 min.

ConditionsIdeal plug flow with identical transit times and no axial backmixing or other time dispersion. The delta is used through its integral properties rather than as an ordinary finite-height density.

These models establish a shared comparison language. Relative variance equals one for complete mixing, the inverse of tank count for an equal-tank cascade and zero for plug flow. This range is not a universal upper bound for all flow distributions. A system in which some material rapidly passes through while another portion remains for a very long time can have relative variance greater than one. Some idealized long-tail models do not have a finite variance at all. A measured value above one calls for examination of flow, tail recording and tracer behavior, rather than automatic rejection because it exceeds the single-tank result.

## Fast and slow lanes in a tube: why laminar flow has a long tail

A straight tube does not ensure that all material reaches the end together. In viscous flow, fluid near the wall is strongly affected by the boundary, while fluid near the centre can move faster. Fully developed laminar flow of a Newtonian fluid in a circular tube has a parabolic velocity profile: speed is highest at the centre and decreases toward zero at a no-slip wall. Newtonian behavior means that shear stress is proportional to shear rate, with constant viscosity in this description. Many polymer melts are shear-thinning, so the Newtonian profile is a defined reference model for learning how a velocity difference becomes a residence-time difference.

During the 1840s, [Poiseuille's experiments on liquid flow through fine glass tubes](https://www.bibnum.education.fr/sites/default/files/168-textepoiseuille.pdf) systematically varied pressure, tube length, diameter and temperature. Controlled tubing provided a way to investigate questions connected with flow through very small blood vessels and established important foundations for viscous transport. Viewed through a velocity profile, these experiments also motivate a distinction between total flow and local speed. Different parts of a cross-section contribute different flow amounts. The transit time of a molecule depends on where it moves and whether it exchanges between faster and slower streamlines during its passage.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe03/en/#en-s4)

Figure 3 · A modern schematic of fully developed Newtonian circular-tube flow. Poiseuille’s fine-tube experiments examined flow under controlled conditions; the velocity profile further explains different centre and near-wall transit times.

Different speeds across the same tube sectionEq. 9

![Different speeds across the same tube section](https://ml-biomat.com/static/agent-math/5fcd6523ed6b8165939e96c1.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| v(r) | Axial velocity at radial distance r | m/min |
| v_{max} | Maximum velocity at the tube centreline | m/min |
| r；R | Radial distance from the centreline and internal tube radius | m |
| v̄ | Cross-section-averaged axial velocity | m/min |
| L | Length of the fully developed flow section | m |
| τ | Space time of the section, also its mean residence time in this model | min |

Reading the relationshipThe parabolic profile is fastest at the centre and zero at the wall. Averaging velocity over annular areas gives half the maximum speed. Volume equals section area times length and flow equals area times mean speed; their ratio cancels the area to give space time.

A worked exampleFor L=1 m and mean speed 0.10 m/min, τ=10 min. Centre speed is 0.20 m/min and centre transit time is 5 min. At r/R=0.5, speed is 0.75 of the centre value, or 0.15 m/min.

ConditionsFully developed steady incompressible Newtonian laminar flow in a straight circular tube with a no-slip wall. The subsequent time distribution additionally assumes no exchange between radial streamlines. Non-Newtonian liquids require the appropriate velocity profile.

In the Newtonian model, mean velocity is half the centreline velocity. Material close to the centre therefore first reaches the outlet at half the mean residence time. A ten-minute mean corresponds to an earliest arrival near five minutes, with no outlet tracer before that time in the idealized model. Near-wall material moves slowly and arrives later, generating a tail. To calculate the fraction already discharged by a given time, each streamline must be weighted by the volume it carries. Counting only the corresponding cross-sectional area would be incorrect because a faster region transports more material through its area during the same interval.

The flow-weighted residence-time distribution of laminar flowEq. 10

![The flow-weighted residence-time distribution of laminar flow](https://ml-biomat.com/static/agent-math/4b9e2e3348d1b7c3a524779c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| F(t) | Cumulative fraction that has left by time t | 1 |
| E(t) | Outlet residence-time probability density | min⁻¹ |
| t | Elapsed time from marking the inlet | min |
| τ | Mean time of this laminar-flow model, equal to section volume divided by flow | min |
| τ/2 | Minimum transit time along the fastest centre streamline | min |

Reading the relationshipBy time t, only streamlines fast enough to cross the tube length within t have arrived. Summing their volumetric flows and dividing by total flow gives the cumulative fraction. Its time derivative gives density. Squared time divided by cubed time correctly produces inverse-time units.

A worked exampleFor τ=10 min, F is zero before 5 min, 0.75 at 10 min and 0.9375 at 20 min. The density at 10 min is 100/(2×1000)=0.050 min⁻¹.

ConditionsFully developed Newtonian circular-tube flow with no radial mixing or diffusion. The inlet pulse marks streamlines uniformly in concentration, and departure is weighted by outlet flow. This ideal model has finite mean but divergent second moment and variance. Real radial exchange changes the tail.

For a ten-minute mean, approximately 93.75 percent has left by twenty minutes. Although most material has emerged, the final small fraction remains influential for certain statistics. The ideal model with no radial exchange has a finite mean but a second moment that continues increasing as the upper integration time grows. Its variance is therefore not finite. Streamlines arbitrarily close to the wall provide arbitrarily long transit times, even though their flow contribution becomes small. Radial diffusion, finite development regions, other transport effects and the experimental recording window change the late behavior in practice. The example shows how an explicit modeling assumption can strongly affect a distribution tail.

A molecule that moves across the tube radius does not remain in one fast or slow lane throughout its journey. Molecular diffusion, turbulent motion or static mixing elements can produce exchanges that alter the no-exchange distribution. A non-Newtonian liquid can have a different velocity-profile shape. In a dispersion, particles may also settle, migrate or spend time at a wall. Choosing a model therefore involves the fluid properties, equipment dimensions, flow regime and tracked entity together. A high viscosity or long tube, considered alone, does not establish the whole residence-time model.

The same reasoning helps interpret melt extrusion and heat exchange. An extruder contains screw-driven motion, channels, leakage and local recirculation, rather than simply a straight circular passage. The circular-tube formula cannot describe all of those paths by itself. An outlet tracer response can nevertheless compare material histories at different screw speeds, feed rates or screw configurations. For material sensitive to prolonged heating, the fraction remaining beyond a relevant exposure time may be more closely connected to damage than the mean alone. Residence-time analysis directs attention to that fraction while the thermal history identifies how strongly it is affected.

## Predicting reaction: when mixing information is also needed

Once different residence times are known, a natural prediction is to calculate the reaction outcome after five, ten or fifteen minutes and average those outcomes using the corresponding material fractions. For an isothermal irreversible first-order reaction, this directly gives the remaining outlet fraction: each reactant's survival follows the same exponential dependence on elapsed reaction time. Evaluate the exponential at each time first, then apply the distribution weight. This is generally different from inserting the mean time into the exponential. For a nonlinear function, averaging the input before calculation and averaging the calculated outputs are different operations.

Calculate survival at each time, then averageEq. 11

![Calculate survival at each time, then average](https://ml-biomat.com/static/agent-math/a1cc00b973b02e1f2ebdbae8.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| C_{A,out}；C_{A0} | Mean outlet A concentration and constant inlet concentration | mol/L |
| k | Irreversible first-order rate constant | min⁻¹ |
| t | Elapsed time from marking the inlet | min |
| E(t) | Outlet residence-time probability density | min⁻¹ |
| X_{A} | Outlet conversion of A | 1 |
| dt；∫；∞ | Small time interval, weighted integration over the full distribution and its infinite upper limit | the complete remaining fraction is dimensionless |
| e；exp | Natural exponential base and exponential-function notation | 1 |

Reading the relationshipFirst-order survival after time t is the exponential of −kt. Weighting it by the fraction with that time and integrating gives the mean remaining fraction. The average of these exponential values is generally different from the exponential evaluated at mean time because the exponential is nonlinear.

A worked exampleFor k=0.10 min⁻¹ and mean time 10 min, plug flow gives remaining fraction e⁻¹≈0.368 and conversion 63.2%. Integrating over the stirred-tank exponential time distribution gives remaining fraction 0.50 and conversion 50%.

ConditionsIsothermal constant-density linear first-order consumption, constant inlet composition and an RTD representative of reactant transport. Dependence on other concentrations, path-dependent temperature or differences between tracked and reacting phases require the corresponding kinetic and transport information.

For a ten-minute mean and a first-order rate constant of 0.10 per minute, ideal plug flow gives approximately 63.2 percent conversion while complete mixing gives 50 percent. Their mean times match, but the histories differ. All plug-flow material experiences ten minutes, whereas the tank includes many early departures and some late ones. Early material retains substantial reactant. Material that has already stayed a long time has little reactant left for additional waiting to consume. Long and short histories therefore do not compensate symmetrically. This is a concrete reason for including a residence-time distribution in reaction prediction.

For a second-order or more complicated reaction, the molecular contact between material of different ages also matters. Two portions can each stay ten minutes without mixing throughout those ten minutes. They may remain in separate droplets or exchange molecules rapidly until their concentrations become uniform. A complete-segregation model treats each small fluid element as a batch evolving with its own age and combines the outputs only afterward. A micromixed system continuously brings molecules of different ages into contact. Even with the same outlet residence-time distribution, these arrangements can give different outcomes for nonlinear kinetics because their local concentration histories differ.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe03/en/#en-s5)

Figure 4 · The upper equal-volume portions retain separate concentrations; the lower sketch shows the same total material after uniform mixing. Vessel shapes are not volume-scaled. For second-order kinetics, the mean local concentration squared differs from the square of mean concentration.

Averaging squares versus squaring the averageEq. 12

![Averaging squares versus squaring the average](https://ml-biomat.com/static/agent-math/98435a497b9242c61286c58c.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| C₁；C₂ | A concentrations in two equal-volume elements | mol/L |
| k | Second-order consumption rate constant | L/(mol·min) |
| r̄_separate | Instantaneous consumption rate averaged over total volume when the elements react separately | mol/(L·min) |
| r_{mixed} | Instantaneous rate after the two elements are uniformly mixed | mol/(L·min) |

Reading the relationshipSeparated elements react according to their individual squared concentrations, followed by equal-volume averaging. Complete mixing averages concentration first and then squares it. Squaring emphasizes the higher concentration, so the two operation orders can differ. This is a local comparison of micromixing at the same mean concentration.

A worked exampleFor C₁=0, C₂=2 mol/L and k=0.10 L/(mol·min), separated elements give an average rate of 0.20 mol/(L·min). After mixing, the rate is 0.10 mol/(L·min). Both cases have mean concentration 1 mol/L.

ConditionsEqual volumes at the same temperature and second-order rate constant, comparing instantaneous consumption with additive volumes. Full outlet conversion still requires integration along the actual mixing and reaction histories.

A simple example reveals the difference without a complicated flow field. Take equal volumes of two liquids, one with zero A and the other with two moles per litre. Their combined mean concentration is one mole per litre. If second-order reaction occurs separately, the mean concentration squared is two in the corresponding concentration-squared units. If the liquids are first completely mixed, the square of their uniform concentration is one. At the same second-order rate constant, the initial total consumption rates differ by a factor of two. The difference arises from the distribution of molecular encounter opportunities. First-order kinetics are linear in concentration, so those two averaging operations give the same instantaneous result.

A tracer should usually remain chemically unchanged, but reacting fluid can still have a meaningful residence-time distribution. If reaction strongly changes viscosity, density, phase state or flow, the distribution should be measured or modeled under conditions representative of the reacting process. If those properties and flow remain comparable, an inert tracer can provide relevant flow information. The additional requirement is to connect that information to reaction and mixing. When temperature also differs between paths, elapsed time alone does not specify the complete reaction history. The temperature experienced along each path may need to be included as well.

Emulsions and suspensions require a further distinction between the continuous phase and particles. A dissolved tracer may follow water accurately while failing to represent the history of every polymer particle. If particles are born, aggregate, break apart or are selectively retained, their outlet age distribution needs to be distinguished from the residence-time distribution of fluid injected at the inlet. The tracked object in the experiment should correspond to the reacting object in the model. Water-soluble reactants, polymer chains, latex particles and droplets can require different information about motion, exchange and the creation or loss of entities.

## The age of a chain and the age of a portion of fluid

Polymers introduce another meaning of time. A portion of fluid staying in a vessel for ten minutes does not imply that every chain in it grows continuously for ten minutes. A chain may be initiated after entry, grow briefly, terminate and then continue moving with the fluid without further propagation. Another chain may retain a reactive end for much longer. In step-growth polymerization, two existing molecules can join into a longer one, making it difficult to assign the resulting chain a simple independent clock beginning at one monomer's entry. Fluid age, active-chain lifetime and the time over which molecular structure develops are related but distinct quantities.

Consider ideal linear step-growth polymerization first. Reactive functional groups are local structures capable of forming connections. Each effective intermolecular link reduces the number of separate molecules by one, while the counted structural units are conserved. With balanced functional-group amounts, linear chains and no ring formation, counting these connections gives a relation between functional-group conversion and number-average degree of polymerization. This average describes how many counted units belong to a randomly selected molecule. As reaction approaches completion, fewer separate molecules remain, so the average number of units per molecule becomes large. The result follows from molecule counting before any detailed chain-length distribution is introduced.

A common reaction time still allows a chain-length distributionEq. 13

![A common reaction time still allows a chain-length distribution](https://ml-biomat.com/static/agent-math/0c41cc5a69f69180294d261e.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| P_ℓ | Probability that a randomly selected chain contains ℓ units, a number fraction | 1 |
| ℓ | Number of units in a chain, a positive integer | 1 |
| X_{n} | Number-average degree of polymerization: mean counted units per molecule | 1 |
| p | Conversion of reactive functional groups | 1 |
| Đ | Molar-mass dispersity | 1 |
| M_{n}；M_{w} | Number-average and mass-weighted-average molar masses | g/mol |

Reading the relationshipThe first line multiplies the probability of ℓ−1 consecutive connections by the probability of stopping, giving the number-fraction length distribution. Each intermolecular link reduces molecule count, connecting the unreacted functional-group fraction to the remaining number of molecules and hence X_n. Random joining also produces a distribution. Mass weighting emphasizes longer chains, making M_w exceed M_n. For the ideal distribution with common unit mass and negligible end-group mass, their ratio approaches 1+p.

A worked exampleAt p=0.90, X_n=10 and dispersity is approximately 1.90. At p=0.99, X_n=100 and dispersity is approximately 1.99. Mean chain length rises strongly while dispersity approaches two rather than one.

ConditionsIdeal linear step growth with balanced functional groups, equal reactivity and no cyclization or branching. The molar-mass dispersity uses equal or equivalent structural-unit masses and negligible end-group mass. It is not a universal distribution for mixed ages or other mechanisms.

Flory's [1936 analysis of molecular-size distributions in linear condensation polymers](https://doi.org/10.1021/ja01301a016) showed that chain lengths remain statistically distributed even when functional groups have equal reactivity and all material experiences the same operating time. An average of one hundred units does not give every molecule exactly one hundred units. Random joining creates different lengths, and the corresponding ideal-model dispersity approaches two as conversion approaches one. Narrowing the residence-time distribution can therefore reduce differences introduced by unequal histories without eliminating the distribution generated by the polymerization mechanism itself. These two contributions should be distinguished when interpreting a narrower product distribution.

[Figure: diagram](https://ml-biomat.com/tutorials/biomaterials-courses/pe03/en/#en-s6)

Figure 5 · Ideal step-growth chain-length variation. The lower plot shows number fractions for the first twenty lengths at conversion 0.8; a small remaining fraction belongs to longer chains. A shared operating time removes age differences without making random joining produce identical chain lengths.

A different simplified picture applies when active centres are long-lived, initiation is nearly simultaneous, and chain transfer and termination are weak. Each active chain can add monomer at approximately the same mean rate, so a longer growth interval gives a larger mean chain length. If monomer concentration stays nearly constant over the interval, the mean number of added units is proportional to growth time. Different active growth durations can then directly introduce additional chain-length variation. A polymerization label alone does not establish a long lifetime: coordination polymerization, for example, can include appreciable chain transfer. The relevant mechanism and its timescales must determine which picture applies.

Mean growth of a long-lived active chainEq. 14

![Mean growth of a long-lived active chain](https://ml-biomat.com/static/agent-math/2905c5f39a14a8df3cb69ded.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ⟨n(t_{g})⟩ | Mean unit count per active chain after growth time t_g; brackets denote averaging | 1 |
| n₀ | Unit count at the start of the growth clock | 1 |
| k_{p} | Propagation rate constant | L/(mol·min) |
| C_{M} | Approximately constant monomer concentration | mol/L |
| t_{g} | Time during which the chain remains active and grows | min |

Reading the relationshipThe mean addition rate per active chain is k_p times monomer concentration, in units per minute. Multiplying a constant rate by growth time gives added units, which are added to the starting count. This clock begins when active growth begins and need not equal the fluid time measured from the equipment inlet.

A worked exampleFor illustrative values n₀=1, k_p=2 L/(mol·min) and C_M=0.50 mol/L, the mean rate is one added unit per minute. Mean counts are eleven after 10 min and twenty-one after 20 min.

ConditionsA simplified chain-growth process with approximately constant monomer concentration, long-lived active centres and negligible transfer or termination. Random addition can still produce chain-to-chain differences. The equation describes a mean rather than identical lengths for every chain.

In conventional radical polymerization, an individual growing radical often lives for much less time than the mean residence time of the equipment. Its chain length is mainly determined by propagation competing with termination and transfer while it is active. The later time spent moving through the vessel after termination is a different interval. Nevertheless, changing residence time can change monomer concentration, initiator concentration and temperature, which in turn alter those competitions. Chain length is therefore not generally obtained by multiplying fluid residence time by one fixed growth speed, but neither is molecular weight universally independent of reactor residence time.

A terminated chain can also participate in later chemistry. Transfer to polymer can create a new active site on an existing chain and lead to branching. A longer stay can increase opportunities for such later changes, although a high-molecular-weight shoulder in a chromatogram does not uniquely identify long-chain branching. Composition differences, aggregation, calibration and other structural effects can influence the signal. Combining flow-history measurements with kinetics and independent structural characterization helps connect a particular part of the residence history to a particular molecular change. The distribution then becomes one component of a mechanistic interpretation rather than a stand-alone structural diagnosis.

## Why growing latex particles still have different sizes

Emulsion polymerization distributes much of the reaction among small polymer particles in water. Each particle can be pictured as a tiny compartment receiving monomer, converting it to polymer and increasing in size. The full process also involves particle nucleation, radical entry and exit, monomer partitioning and stabilization. To isolate the effect of residence-time variation, first choose a clearly specified seeded-particle model. Particles enter with the same size, their number is unchanged by new nucleation or aggregation, and every particle has the same constant net volume-growth rate during the interval being considered. This model separates unequal time histories from other sources of particle differences.

Monomer entering a particle and polymer being formed are different quantities. Incoming monomer can accumulate unreacted inside a swollen particle or be consumed by polymerization. Describing total swollen-particle volume requires accounting for that monomer inventory and associated volume changes. Here the model explicitly tracks the particle volume corresponding to newly formed polymer, assuming approximately constant polymer density and sufficient monomer supply for steady growth. Polymer mass added per minute divided by density then gives polymer volume added per minute. Defining the tracked volume makes it possible to connect growth and residence time without silently equating monomer transport with polymer production.

Mapping time variation into particle-volume variationEq. 15

![Mapping time variation into particle-volume variation](https://ml-biomat.com/static/agent-math/0143b0e2e4755a02c68d00e7.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| V_{p}(t) | Particle volume corresponding to polymer mass after elapsed time t | μm³ |
| V_{p0} | Common initial polymer volume of all entering seeds | μm³ |
| H | Constant net polymer-volume growth rate per particle | μm³/min |
| t | Elapsed time from marking the inlet | min |
| t̄ | Mean residence time of the distribution | min |
| V̄_p | Number-average polymer volume of exiting particles | μm³ |
| σ_{V}² | Number-weighted particle-volume variance | μm⁶ |
| σ_{t}² | Residence-time variance of these particles | min² |

Reading the relationshipLinear growth maps each minute to the same added volume. Averaging retains the common initial volume and replaces time by its mean. Each volume deviation equals H times a time deviation; squaring and averaging gives H² times time variance. Volume variance has squared-volume units, μm⁶.

A worked exampleFor V_p0=0.004 μm³, H=0.0004 μm³/min and mean time 10 min, mean volume is 0.008 μm³. A single-tank time variance of 100 min² gives volume variance 0.000016 μm⁶. Two equal tanks in series reduce it to 0.000008 μm⁶.

ConditionsIdentical entering seeds, no new nucleation, aggregation, breakup or selective retention, particles following the stated RTD and a common constant H. Volume is polymer mass divided by approximately constant density. Swollen volume including unreacted monomer requires an additional balance.

In this linear-growth model, each extra minute adds the same volume increment. Mean particle volume therefore depends on mean residence time, while volume variation scales the time variation by the growth rate. Two systems with equal mean time can have equal mean particle volume but different volume spreads. Replacing one completely mixed tank with two equal tanks in series, at fixed combined volume and flow, halves the residence-time variance and hence halves the particle-volume variance. The reduction applies to variance. Standard deviation becomes the square root of one half of its original value, approximately 70.7 percent, rather than becoming half as large.

### Same mean volume, different volume spread

[Figure: Same mean volume, different volume spread](https://ml-biomat.com/tutorials/biomaterials-courses/pe03/en/#en-s7)

Total mean time is 10 min and initial polymer volume 0.004 μm³. Identical seeds, constant particle number, no aggregation or nucleation, and constant growth rate. The cumulative curve is number-weighted. Reported radius belongs to a sphere with the mean volume.

Volume is not radius. The volume of a sphere is proportional to the cube of its radius, so an eightfold volume increase doubles the radius. Converting the mean volume into the radius of a sphere gives an equivalent radius for a sphere with that mean volume. It generally differs from the arithmetic mean of all particle radii. This distinction becomes more noticeable for broad distributions. Instruments may weight particles by scattering intensity or mass, giving larger particles different emphasis. Comparing model and measurement begins by matching the size definition and averaging convention, rather than placing two quantities both called “average diameter” side by side.

Volume and radius are related by a cubeEq. 16

![Volume and radius are related by a cube](https://ml-biomat.com/static/agent-math/d952532ef3bf00ebcd2a3d45.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| V_{p} | Volume of one spherical particle | μm³ |
| R_{p} | Radius of that particle | μm |
| π | Circle constant, approximately 3.14159 | 1 |
| (…)^(1/3) | Cube root, finding a length whose cube equals the enclosed volume quantity | result is μm here |

Reading the relationshipScaling a sphere changes its size in three spatial directions, so volume is proportional to radius cubed. Inverting the relation requires a cube root. Transforming each particle and then averaging generally differs from transforming mean volume because the cube root is nonlinear.

A worked exampleA volume of 0.008 μm³ corresponds to radius approximately 0.124 μm, or 124 nm, and diameter approximately 248 nm. Raising volume eightfold to 0.064 μm³ doubles the radius.

ConditionsSpherical geometry, with radius and volume describing the same particle boundary. A dry-polymer equivalent radius should be distinguished from measured hydrodynamic radius or swollen particle size.

Why can particles with equal reaction times still differ in size? Residence time is only one contributor. Initial seeds can differ, particles can capture radicals at different rates, monomer availability can vary with position and new particles can continue to form. If two particles combine, particle number changes along with size, so the simple picture of one entering particle growing independently needs an additional aggregation process. In continuous emulsion polymerization, reactor arrangements, feed strategies and particle-generation mechanisms are connected. Modeling flow time together with particle kinetics makes these connections explicit and helps identify which distribution the experiment should measure.

The interactive calculation first answers a bounded physical question: with identical entering seeds, equal total mean residence time and a constant polymer-volume growth rate, how much does increasing the number of stages reduce volume variation caused by different residence times? After establishing that contribution, experimentally relevant nucleation, aggregation or growth-rate variation can be added and their effects compared. Each parameter then corresponds to a mechanism. A narrower particle-size distribution becomes a result whose origin can be followed, rather than an unexplained consequence attributed to adding another vessel.

## Turning an outlet curve into a useful decision

Suppose a pulse experiment gives a small early outlet peak, a main peak and a long late tail. First examine the inlet pulse and sampling system to establish whether they account for the early feature. Then consider whether fast pathways coexist with slowly exchanging regions. A model containing a bypass and retained region can generate a similar response, but one curve may not uniquely determine the internal geometry. Changing flow rate, agitation or equipment connections can reveal which part of the response changes with which intervention. Combining those observations with equipment structure gives a stronger physical interpretation of the curve.

The relation between mean time and effective volume supplies another clue. For steady constant-density flow, with the tracked material participating throughout the volume and the tracer representing that phase, mean residence time equals effective volume divided by volumetric flow. A much larger geometric volume may indicate weakly exchanged space, incomplete tracer access or an inadequately recorded tail. Conversely, adsorption at a wall can lengthen the response so that the measured time includes a tracer-specific delay. These possibilities correspond to different physical processes. Examining them individually is more informative than assigning every discrepancy to a single label such as dead volume.

Finite sampling also affects calculation. A recorded concentration is a value at one time, whereas the quantity to sum is the tracer amount carried out over a represented interval. Small trapezoidal areas can approximate the integral for equally spaced measurements. Unequal intervals require retaining their individual widths. These areas become the weights for calculating mean and variance. A weak late signal is multiplied by a large time or time squared, so tail truncation can strongly affect the resulting statistics. Plotting the fraction of injected tracer recovered as recording duration increases can help determine an adequate experimental duration.

The final process metric should connect to the material change of interest. For incompletely reacted material, examine the early-exit fraction and use appropriate kinetics to estimate residual reactant. For thermal degradation or discoloration, investigate the late-exposure fraction and include temperature histories where relevant. For latex particle-size variation, combine residence time with particle growth and number accounting. Means, variances, quantile times and complete response curves each provide useful information. The mechanism governing the material outcome should guide which measure becomes central to the comparison.

Consider: does equal mean residence time imply equal conversion?

Mean time alone is insufficient. For a first-order reaction, each time-dependent remaining fraction is weighted by the residence-time distribution. At a ten-minute mean and rate constant of 0.10 min⁻¹, complete mixing and plug flow give 50% and approximately 63.2% conversion. Nonlinear reactions additionally require a description of microscopic mixing. In the tanks-in-series interaction, keep mean time fixed and observe how narrowing the distribution changes the early-exit population.

Consider: if two tanks halve volume variance, must radius variance also halve?

With constant particle-volume growth, volume depends linearly on time, so its variance is directly proportional to time variance. Radius is a cube-root transformation of volume. Calculating radius variance therefore requires transforming the complete volume distribution and evaluating its moments, or using a stated narrow-distribution approximation. Equal mean volume does not automatically establish equal mean radius either.

A residence-time curve compresses many hidden journeys inside equipment into measurable time information. Its interpretation rests on several connections: area represents a material fraction, weights define the kind of average, and flow history combines with reaction mechanism to determine products. Following those connections turns a tracer response into questions about whether reactant has enough time to transform, whether some material remains too long, and at which stage differences between molecules or particles arise.
