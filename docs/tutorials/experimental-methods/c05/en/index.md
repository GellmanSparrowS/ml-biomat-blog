# ITC: Measuring molecular binding through heat

Source: https://ml-biomat.com/tutorials/experimental-methods/c05/en/
Language: en

Connect injection heats with molecular occupancy to interpret affinity, enthalpy and experimental conditions.

## Ask about molecular binding through a small amount of heat

When a drug enters a protein binding pocket, or a guest molecule enters the cavity of a cyclodextrin, interactions among molecules and surrounding water are rearranged. Researchers want to know more than whether binding occurs. What concentration occupies a substantial fraction of the available sites? How many guests can each host accommodate? Does the process release or absorb heat? Isothermal titration calorimetry, usually abbreviated ITC, follows this thermal evidence. Two solutions are mixed in a sequence of small additions at controlled temperature. The instrument records the heat associated with each addition, and the changing heat pattern is connected to a model of molecular binding.

Imagine people entering a reading room. At first, many seats are empty and new arrivals easily find a place. As the room fills, more of the additional people remain in the aisles. Molecular binding adds continual exchange: bound molecules can leave, and free molecules can enter, eventually establishing a dynamic equilibrium. If forming a bound state has a characteristic heat effect, each injection’s heat depends on how much additional binding occurs. Initially large peaks that become smaller may reflect progressive occupation of sites. Interpreting them also requires asking whether mixing itself generates heat, whether the original sample becomes diluted, and how the instrument converts thermal events into recorded numbers.

ITC is useful for examining solution affinity and thermodynamic properties together. It does not require a fluorescent label or attachment of one partner to a sensing surface. Its signal represents the combined heat effects of processes occurring in the solution, so sample purity, active fraction, and buffer composition enter the interpretation directly. Comparing hosts that bind the same guest can help explain loading and release in materials research. Comparing a protein with a defined variant can examine how a structural change influences an interaction. The constructed experiment in this chapter connects raw instrument signals, blank correction, equilibrium models, and parameter assessment, keeping each final number attached to its measurement history.

## Heat can be measured while temperature stays nearly constant

The word isothermal can suggest that no heat change occurs. Maintaining constant temperature often requires active energy compensation, much as an air conditioner can work while room temperature remains steady. An ITC sample cell sits beside a reference cell. The instrument compares their temperatures and adjusts heating power through feedback. When the sample releases heat, less compensating heater power is needed to keep the temperature difference near zero. An absorbing process requires more power. The raw trace therefore commonly shows differential power over time, rather than a solution temperature that keeps rising or falling. Power is the rate of energy transfer; heat is the energy transferred over a specified interval.

In 1989, Wiseman, Williston, Brandts, and Lin described a titration calorimeter for rapid measurements of binding constants and heats, using ribonuclease A binding to 2′-CMP as an experimental example. Their paper connected matched cells, temperature feedback, automated injections, and integration into one measurement method. It also compared curves obtained at different protein concentrations, showing that information depends on the chosen concentration range. The historical principle diagram follows this measurement logic without reconstructing the dimensions of a particular instrument. The accompanying teaching model shows how increasing ligand addition changes both the fraction of occupied sites and the fraction of ligand remaining free in solution.

![Original matched-cell and feedback schematic connected to Wiseman et al. (1989), not to scale. The constructed independent-site model at right uses different denominators: total sites and total ligand.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/5ef77dff5c797e9c2f79e38a.svg?v=5ef77dff5c79)

Figure 1Original matched-cell and feedback schematic connected to Wiseman et al. (1989), not to scale. The constructed independent-site model at right uses different denominators: total sites and total ligand.

Calibration of the heat scale is another separate step. A heater can deliver a known electrical energy pulse, allowing the recorded response area to be compared with a known input. The 1989 paper describes electrical and chemical calibration approaches. Such a check establishes how the instrument converts a thermal event into a power integral. It does not establish the concentration or activity of a particular protein, and it does not identify which chemical process generated a sample peak. Keeping instrument calibration, solution preparation, and reaction modeling distinct helps locate a discrepancy when a result changes between experiments.

After an injection, mixing, re-equilibration, and instrument feedback spread the response into a peak. Peak height depends on injection speed, mixing, and response time. The area relative to a baseline gives the heat associated with the injection. A baseline represents the power expected without that injection’s disturbance and may drift slowly rather than remain horizontal. Integration adds the differences between signal and baseline over time. A reader unfamiliar with the integral symbol can imagine cutting time into short intervals, multiplying the power difference in each interval by its duration, and adding the resulting energy contributions.

$$
q_{\mathrm{obs}}=\int_{t_a}^{t_b}[P(t)-P_0(t)]\,dt,\qquad q_{\mathrm{bind}}=q_{\mathrm{obs}}-q_{\mathrm{blank}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a0895523db4c85bc63aa1d0f.svg) | Baseline-corrected sample injection heat, microjoules. |
| ![Formula](https://ml-biomat.com/static/agent-math/7409c350063c63e2d0b0ffa5.svg) | Time and integration start/end times, seconds. |
| ![Formula](https://ml-biomat.com/static/agent-math/a3409bceea96cdc30708a469.svg) | Recorded sample differential power, microwatts. |
| ![Formula](https://ml-biomat.com/static/agent-math/88d494ac250584df35c39036.svg) | Estimated baseline power without that injection disturbance, microwatts. |
| ![Formula](https://ml-biomat.com/static/agent-math/e27726ac854afcaeac389fa8.svg) | Corresponding integrated heat in a matched blank, microjoules. |
| ![Formula](https://ml-biomat.com/static/agent-math/4db474a27f52f79f2ec60b8e.svg) | Binding-related heat after the specified blank correction, microjoules. |

Power multiplied by time gives energy, so area rather than height accumulates heat. Exothermic heat is negative here. −2 microwatts for 10 s gives −20 microjoules; first-injection binding of about −22.66 plus a +2 blank gives about −20.66 microjoules observed.

This chapter defines exothermic heat as negative and plots its power deflection downward. An average deflection of −2 microwatts over 10 seconds contributes −20 microjoules because one watt equals one joule per second. Software may instead display exothermic events upward, so the plotted sign convention should be checked first. The constructed experiment’s first injection has approximately −22.66 microjoules of binding heat plus about +2 microjoules of mixing background, producing a raw peak area near −20.66 microjoules. Separating these contributions precedes interpretation of energy per mole of binding. The reference cell provides thermal comparison; an independent ligand-into-buffer experiment measures mixing background. These are different roles.

## Count free, bound, and total molecules before interpreting affinity

Call the protein M, the added ligand L, and their complex ML. Ligand names a binding role: it may be a small molecule, nucleic acid, or another protein. The simplest model gives each protein one identical independent site. Association and dissociation continue while the composition reaches equilibrium under fixed conditions. The dissociation constant, Kᴅ, is the product of the two free concentrations divided by complex concentration at equilibrium. For the same temperature, solvent conditions, and model, a smaller Kᴅ means appreciable occupancy can be reached at a lower free-ligand concentration. Its numerical value should consequently be reported together with concentration units and experimental conditions.

$$
K_d=\frac{[M][L]}{[ML]},\qquad \theta=\frac{[ML]}{[M]+[ML]}=\frac{[L]}{K_d+[L]}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b222289350e5e9dd7c2d84e7.svg) | Dissociation constant for one independent site at fixed conditions, micromolar. |
| ![Formula](https://ml-biomat.com/static/agent-math/3124bff73534c41429e32897.svg) | Free protein concentration, micromolar. |
| ![Formula](https://ml-biomat.com/static/agent-math/8dca9e27d90e6205901ab6f2.svg) | Free ligand concentration, micromolar. |
| ![Formula](https://ml-biomat.com/static/agent-math/6710b6da8dfbf55836dd7325.svg) | Complex concentration, micromolar. |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | Fraction of protein sites occupied, dimensionless. |

Equilibrium plus protein conservation yields occupancy. Kᴅ=1 and free ligand=1 micromolar give θ=0.5. With 20 micromolar total protein, 10 micromolar ligand is bound and total ligand must be 11 micromolar.

A useful reference point is half-occupancy: for independent sites, free ligand equal to Kᴅ occupies half the sites. The word free is essential. With total protein at 20 micromolar and Kᴅ at 1 micromolar, half-occupancy means 10 micromolar ligand is already in complexes. Another 1 micromolar must remain free, so the total ligand concentration is 11 micromolar. Substituting a total concentration of 1 micromolar into the free-ligand formula would invent molecules that are unavailable for additional binding. Micromolar means micromoles per liter and counts chemical amount rather than mass. Converting it to a protein mass concentration also requires the protein’s molar mass.

ITC often binds a substantial fraction of the ligand, making simultaneous conservation and equilibrium essential. Subtract complex concentration from total site and total ligand concentrations to obtain the remaining free populations. Substitution into the dissociation-constant expression produces a quadratic equation. Of its two mathematical roots, the physical choice keeps complex concentration below either available total and makes it vanish when no ligand is present. This selection has a concrete meaning: the model cannot bind more ligand than was added or create nonexistent sites. The program evaluates an algebraically equivalent stable form to reduce loss of numerical precision when weak binding would otherwise require subtracting nearly equal numbers.

$$
S_T=nM_T,\qquad B=\frac{S_T+L_T+K_d-\sqrt{(S_T+L_T+K_d)^2-4S_TL_T}}{2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7f0fe5be3234907cb3e30d80.svg) | Total independent-site concentration, micromolar. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Effective number of identical independent sites per protein, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/92c1a28876c2005bfabddc66.svg) | Total protein concentration, micromolar. |
| ![Formula](https://ml-biomat.com/static/agent-math/4bd6f81ef8f52025128f11e2.svg) | Total ligand concentration, free plus bound, micromolar. |
| ![Formula](https://ml-biomat.com/static/agent-math/b222289350e5e9dd7c2d84e7.svg) | Dissociation constant of the identical independent sites, micromolar. |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | Bound ligand concentration, micromolar. |

Take the smaller root of KᴅB=(Sₜ−B)(Lₜ−B), keeping bound ligand below both available totals. Sₜ=20, Lₜ=11 and Kᴅ=1 micromolar give B=10 micromolar. Distinct or cooperative sites require their corresponding equilibrium model.

A mole is a way of counting particles, with one mole corresponding to about 6.022×10²³ specified entities. Concentration multiplied by volume gives chemical amount: 20 micromolar protein in a 200-microliter cell is 4 nanomoles. For a molar mass of 50,000 grams per mole, this is 1 milligram per milliliter and about 0.2 milligrams in the cell. The conversion turns concentration planning into an estimate of actual sample consumption. A smaller cell can reduce consumption, while also reducing the total number of molecules contributing to the thermal signal.

Amounts change after every addition. The teaching program uses an explicit discrete mixing protocol: remove 2 microliters from a well-mixed 200-microliter cell, then replace it with 2 microliters of 300-micromolar ligand. Each cycle retains 99% of the existing components and adds 0.6 nanomoles of ligand. After 25 injections, initial protein at 20 micromolar falls to approximately 15.56 micromolar. A real overfilled calorimeter displaces liquid continuously during injection and uses the corresponding volume-correction model. Separating withdrawal and replacement here makes conservation easy to inspect. Newly formed binding is the final bound amount minus the previous bound amount that remains after withdrawal.

$$
r=1-\frac{v}{V_0},\quad M_j=rM_{j-1},\quad L_j=rL_{j-1}+(1-r)L_s,\quad q_j=V_0\Delta H(B_j-rB_{j-1})
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | Retained fraction after withdrawal and replacement, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/6ea26af94b3e02fd7aa1d744.svg) | Volume withdrawn and then replaced each cycle, liters. |
| ![Formula](https://ml-biomat.com/static/agent-math/454606841ec20ef0f43cd9f6.svg) | Fixed active cell volume, liters. |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | Injection index; j=0 denotes the initial state. |
| ![Formula](https://ml-biomat.com/static/agent-math/f3f75911c33257cfd1ffbd74.svg) | Total protein concentrations after current and previous injections, mol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/aa1a2468e58547721f470bd0.svg) | Total ligand concentrations after current and previous injections, mol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/56d0edb2c8fe78865b80653e.svg) | Ligand concentration in syringe solution, mol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/0d29cc80036a5952d1a46d56.svg) | Equilibrium bound-ligand concentrations after current and previous injections, mol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/661ecf63746c81514ad169cb.svg) | Enthalpy per mole of newly formed binding, J/mol. |
| ![Formula](https://ml-biomat.com/static/agent-math/06a99ed1ee9cf7423b7ab887.svg) | Binding heat in the current injection, joules. |

The discrete model removes mixed solution, replaces it with ligand, then equilibrates. A 200-microliter cell with 2-microliter cycles has r=0.99; 20 micromolar protein becomes about 15.556 after 25 injections. Each 300-micromolar ligand injection adds 0.6 nmol. Code uses microliters, micromolar and kJ/mol with factor 0.001 to obtain microjoules.

The retained-complex term is especially useful for checking the calculation. Some complexes leave with the withdrawn liquid, but their removal is transport out of the cell, not a new dissociation reaction inside it. Subtracting the entire previous bound concentration would incorrectly count that transport as an endothermic chemical event. Retaining only the fraction still present establishes the starting bound population for the new equilibrium. The same logic applies to both free and bound material in the conservation calculation. This makes the model a sequence of explicit physical operations rather than a curve formula whose correction terms are difficult to interpret.

## Choose a concentration range in which the curve contains information

Consider adding ligand repeatedly to a cell containing protein. With extremely strong binding, nearly every arriving ligand binds until sites suddenly approach saturation, producing a nearly step-like curve. Capacity and heat per mole may be clear, while several very strong affinities produce almost indistinguishable steps. With weak binding, much of the ligand remains free throughout the experiment and heat changes gradually. Site number, affinity, and enthalpy can then be difficult to distinguish from one another. A curved transition in an intermediate range supplies more differentiating information. Experimental design therefore aims to sample the early region, the transition, and the approach to saturation, rather than simply maximizing the first peak.

$$
c=\frac{nM_0}{K_d}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | Design parameter combining initial concentration and affinity, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Effective number of identical independent sites, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/d0d1f9424f5849a25d3f4fc5.svg) | Initial total protein concentration in the cell, micromolar. |
| ![Formula](https://ml-biomat.com/static/agent-math/b222289350e5e9dd7c2d84e7.svg) | Dissociation constant in the same concentration units as M₀. |

Site concentration relative to dissociation constant controls transition shape. n=1, M₀=20 and Kᴅ=1 micromolar give c=20; Kᴅ=100 or 0.01 gives c=0.2 or 2000. Information also depends on heat magnitude and noise.

The dimensionless c value relates initial site concentration to Kᴅ. With one site per protein, 20-micromolar initial protein, and Kᴅ of 1 micromolar, this example has c=20. The figure compares c values of 0.2, 20, and 2000 with the other settings held fixed. Low c gives a shallow curve, high c approaches a step, and the intermediate curve has a substantial transition. A useful operating range also depends on heat magnitude, noise, solubility, and sample consumption. Lowering concentration can broaden the informative transition for strong binding but reduces heat signal. Increasing concentration for weak binding calls for checking aggregation and nonspecific interactions. The c value guides design alongside evidence about the actual sample state.

![Constructed design diagnostics. A fixes initial protein at 20 micromolar, n=1 and enthalpy at −40 kJ/mol while changing Kᴅ. B fixes n=1 and colors the RMS injection-heat residual; the white cross marks its grid minimum. Colors are not confidence regions.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/29d4a24bcc5d2da878e856a6.svg?v=29d4a24bcc5d)

Figure 2Constructed design diagnostics. A fixes initial protein at 20 micromolar, n=1 and enthalpy at −40 kJ/mol while changing Kᴅ. B fixes n=1 and colors the RMS injection-heat residual; the white cross marks its grid minimum. Colors are not confidence regions.

Concentration deserves independent attention. Total protein concentration can differ from the concentration of active binding sites if some material is denatured or aggregated. A fitted site number n can absorb concentration error, so a result of 0.8 does not imply that each molecule physically carries eight-tenths of a pocket. Compare preparation batches, independently measure concentrations, examine sample state, or exchange the roles of syringe and cell when appropriate. Ask whether these experiments can be explained consistently. Electrophoresis checks components and degradation; size-exclusion measurements examine aggregation in solution. They constrain the sample entering the calorimetric model rather than replacing the binding measurement.

Matching the two solutions is equally consequential. Differences in salt, pH, or solvent fraction can generate heat even without the target interaction. Matched buffers and a ligand-into-buffer control make these contributions observable. If background changes during the concentration sequence, correction should follow injection number or an appropriate model rather than always subtracting an arbitrary constant. Bubbles, precipitation, incomplete injection, and slow return to baseline leave clues in the raw traces. Decisions about including the first injection should follow the actual delivery record and signal. The constructed experiment introduces no special first-injection defect, so all injections remain in its analysis.

## Connect a sequence of peaks to inspectable binding parameters

The full example makes 25 injections separated by 180 seconds and generates separate sample and ligand-blank power traces. Both contain a slowly drifting baseline and fixed-seed random noise. The program fits baseline using quiet periods before injection and near the ends of injection intervals, then integrates each peak. Those selected periods must have substantially returned to baseline. If a slow process remains in the tail, treating it as background removes part of the actual signal. The enlarged first injection displays the downward sample response, upward blank response, and integrated area together, keeping the analysis connected to the measurement rather than only to a table of final parameters.

![Constructed data, seed 650. Sample and blank have independent power noise; 25 injections of 2 microliters, 180 s apart. A and B retain power and baseline; C divides by 0.6 nmol per injection; D is corrected data minus model.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/97e339defd3cac50720facce.svg?v=97e339defd3c)

Figure 3Constructed data, seed 650. Sample and blank have independent power noise; 25 injections of 2 microliters, 180 s apart. A and B retain power and baseline; C divides by 0.6 nmol per injection; D is corrected data minus model.

A small baseline displacement can accumulate into an appreciable heat error. Estimating baseline 0.001 microwatts too high over 180 seconds changes the integral by −0.18 microjoules. That exceeds the approximately 0.066-microjoule root-mean-square fit residual in this example. Baseline regions and drift models should therefore follow the raw trajectory and experimental process. Repeatedly moving a baseline toward an expected binding constant allows processing choices to steer the answer. Retaining power, baseline, and integration windows makes it possible to compare several physically justified treatments and quantify their consequences.

Subtract each blank heat from the corresponding sample heat, then divide by the amount of ligand delivered in that injection to obtain the familiar normalized titration curve. One microjoule per nanomole equals one kilojoule per mole. Here each injection adds 0.6 nanomoles, so the first binding heat of about −22.66 microjoules corresponds to approximately −37.77 kilojoules per mole of injected ligand. Its magnitude is slightly smaller than the specified binding enthalpy of 40 kilojoules per mole because not all injected ligand forms new complexes. Near saturation, progressively fewer new binding events occur per addition, and the normalized heat approaches zero.

The program fits injection heats by adjusting Kᴅ, enthalpy, and effective site number to minimize squared differences between model and data. The constructed truth is 1 micromolar, −40 kilojoules per mole, and n=1. Analysis starting from noisy power traces recovers approximately 0.995 micromolar, −39.97 kilojoules per mole, and 1.000. Omitting blank subtraction under the same fitting settings produces approximately 0.420 micromolar and −34.13 kilojoules per mole. A fitting routine can return tidy numbers while interpreting an uncorrected experimental contribution as altered binding parameters. The relevant check is whether the fitted heat represents the process named in the model.

Residuals are data minus model. Plotting them by injection reveals consecutive deviations through the transition, trends near the end, or a single unusual injection. A parameter-error landscape shows how combinations of Kᴅ and enthalpy change the discrepancy. Along a tilted low-error valley, changes in one parameter partly compensate changes in another. The displayed map fixes n=1 and shows conditional root-mean-square residuals, rather than a confidence region. The program separately performs 80 refits with a specified noise level to illustrate noise-induced parameter variation. Concentration errors, batch variation, and model choice require their own experimental or analytical treatment.

## Heat, affinity, and entropy describe different aspects of binding

Does releasing more heat necessarily mean tighter binding? Comparing enthalpy and free energy reveals why these are different questions. Enthalpy is connected to the heat effect under constant-pressure conditions. Standard binding free energy expresses the equilibrium constant on an energy scale. Entropy concerns the statistics of accessible microscopic states and includes both the binding molecules and their solvent. Binding can restrict molecular conformations and relative motion while releasing previously constrained water. These contributions combine into the overall entropy change. Describing entropy only as visible disorder is therefore a poor guide to molecular interactions in solution.

$$
\Delta G^\circ=RT\ln\!\left(\frac{K_d}{c^\circ}\right)=\Delta H^\circ-T\Delta S^\circ
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9824e74d6293e33988b52fed.svg) | Standard molar binding free-energy change, J/mol. |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | Gas constant, 8.314462618 J/(mol·K). |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | Absolute temperature, kelvin. |
| ![Formula](https://ml-biomat.com/static/agent-math/b222289350e5e9dd7c2d84e7.svg) | Dissociation constant expressed in mol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/c2b399340d1e66a535bf58cf.svg) | Standard concentration, 1 mol/L, making the logarithm argument dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/6e230c0e277e7c47581e0b74.svg) | Standard molar binding enthalpy change, J/mol. |
| ![Formula](https://ml-biomat.com/static/agent-math/e61a5fff73bfe0205f88db4f.svg) | Standard molar binding entropy change, J/(mol·K). |

Using the ideal dilute-solution concentration approximation at the specified conditions, the equilibrium constant gives standard free energy. T=298.15 K and Kᴅ=10⁻⁶ mol/L give ΔG°≈−34.248 kJ/mol. For ΔH°=−40 kJ/mol, ΔS°≈−19.292 J/(mol·K).

At 298.15 kelvin with Kᴅ=1 micromolar and a standard concentration of 1 mole per liter, standard binding free energy is approximately −34.25 kilojoules per mole. If enthalpy is −40 kilojoules per mole, the term −TΔS° is approximately +5.75 kilojoules per mole: the entropy contribution offsets part of the favorable enthalpy contribution. Another system can have the same affinity and an enthalpy of −20 kilojoules per mole, with a more favorable entropy term maintaining the same total free energy. The two systems in the figure are constructed comparisons rather than named drugs. Equal affinity does not require equal calorimetric amplitude, and one exothermic peak’s magnitude cannot by itself rank binding strength.

![Constructed thermodynamic comparison. A uses Kᴅ=1 micromolar and 298.15 K for two systems with equal standard free energy but different enthalpy and entropy terms. B distinguishes free and total ligand axes: half-occupancy at 20 micromolar protein requires 11 micromolar total ligand.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9db56b25b681e7fe0058a38f.svg?v=9db56b25b681)

Figure 4Constructed thermodynamic comparison. A uses Kᴅ=1 micromolar and 298.15 K for two systems with equal standard free energy but different enthalpy and entropy terms. B distinguishes free and total ligand axes: half-occupancy at 20 micromolar protein requires 11 micromolar total ligand.

The standard state also matters mathematically. A concentration-valued Kᴅ is divided by standard concentration before taking its natural logarithm, producing a dimensionless argument. Negative standard free energy describes binding tendency under that reference definition; actual occupancy still depends on free concentrations. At equilibrium, forward and reverse events continue while macroscopic composition remains constant. Kᴅ describes this equilibrium relation rather than the time one complex stays together. Systems with similar equilibrium affinity may have different association and dissociation rates. Surface plasmon resonance in the next chapter follows the time dimension to investigate that distinction.

Measured heat may also include proton exchange linked to binding. If complex formation takes up or releases protons, the buffer participates in associated heat effects, making observed enthalpy buffer-dependent. An ordinary ligand-into-buffer blank measures mixing without the binding partner; proton exchange triggered by binding remains coupled to the interaction itself. Comparing buffers with different ionization enthalpies at the same pH can investigate this linkage. Enthalpy is consequently the result of the specified solution process. Its sign alone does not count hydrogen bonds or uniquely assign a dominant microscopic interaction. Structural and condition-dependent experiments can test proposed molecular explanations.

The interactive experiment changes Kᴅ, enthalpy, and protein concentration separately. Hold enthalpy fixed and change Kᴅ to examine transition shape and c. Hold Kᴅ fixed and change enthalpy to examine heat magnitude and direction. Positive enthalpy can coexist with the same favorable standard free energy if the entropy term contributes appropriately. Finally, change protein concentration and consider how curve shape and material consumption change together. Separating these adjustments helps identify which independent pieces of information a titration curve can carry.

A small heat signal also deserves a specific interpretation. If enthalpy approaches zero at a particular temperature and buffer condition, appreciable binding can produce little calorimetric response. An affinity measurement based on another observable can then establish whether occupancy changes while heat remains small. A temperature or buffer series may reveal how the thermal balance changes, provided sample state remains comparable. This is why the interactive control can pass through zero enthalpy without removing the equilibrium binding model: the population relation and the observable used to detect it are different parts of the experiment.

## Change affinity, heat and concentration separately

One class of independent sites, n=1; a 200-microliter cell with 25 withdrawal/replacement cycles of 2 microliters. Syringe ligand is 15 times the initial protein concentration. Blank-corrected heat is normalized per injected ligand; temperature is 298.15 K.

[Figure: Titration curve with independently adjustable affinity, enthalpy and concentration](https://ml-biomat.com/tutorials/experimental-methods/c05/en/#C05-plot)

## Preserve the measurement inside the complete analysis

The complete program preserves raw power, fitted baselines, injection integrals, blank heats, and model predictions. Constructed data allow each stage to be compared with known values: first check amount conservation, then heat normalization, then parameter recovery in the presence of noise. The response peak has a rising and decaying shape and is normalized on the discrete time grid so its area matches the assigned heat. This response model explains how an instrument spreads an energy event across time. Inferring actual reaction rates requires separating instrument response from molecular kinetics.

### Complete power traces, injection correction and binding fits

Constructs sample and blank power with a fixed seed, integrates and corrects heat, fits independent sites, and exports raw traces, parameter landscapes and noise refits.

```
"""Constructed ITC experiment with explicit discrete withdrawal/replacement mixing."""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle

def titration(kd=1.,enthalpy=-40.,sites=1.,protein=20.,ligand=300.,cell=200.,injection=2.,number=25):
 """uM, kJ/mol, uL -> microjoules. Remove a mixed aliquot, then replace it."""
 retain=1-injection/cell;M=protein;L=0.;bound=0.;rows=[]
 for j in range(number):
  M*=retain;L=L*retain+ligand*injection/cell;S=sites*M
  # Stable quadratic root; avoids subtraction cancellation at weak binding.
  B=2*S*L/(S+L+kd+np.sqrt((S+L+kd)**2-4*S*L))
  q=cell*.001*enthalpy*(B-retain*bound)
  rows.append([j+1,M,L,B,q,L/M]);bound=B
 return np.array(rows)

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True);zh=a.language=='zh';T=lambda z,e:z if zh else e
 plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.titlesize':12,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fcfbf7','axes.facecolor':'#fcfbf7','savefig.facecolor':'#fcfbf7'})
 B,R,G,Y='#167d9a','#d35f47','#37967d','#c49b35'
 def save(f,n):f.savefig(a.output/f'{n}-{a.language}.svg');f.savefig(a.output/f'{n}-{a.language}.png',dpi=145);plt.close(f)
 truth=titration();q=truth[:,4];ratio=truth[:,5];rng=np.random.default_rng(650);time=np.arange(26*180,dtype=float);baseline=.08+.000015*time
 power=baseline.copy();blank=baseline.copy();pulse_t=np.arange(180,dtype=float);kernel=pulse_t/12**2*np.exp(-pulse_t/12);kernel/=np.trapezoid(kernel,pulse_t)
 dil=2+.02*np.arange(25)
 for i in range(25):
  sl=slice((i+1)*180,(i+2)*180);power[sl]+=(q[i]+dil[i])*kernel;blank[sl]+=dil[i]*kernel
 power+=rng.normal(0,.004,time.size);blank+=rng.normal(0,.004,time.size)
 quiet=(time<170)|((time%180)>=150);basefit=np.polyval(np.polyfit(time[quiet],power[quiet],1),time);blankfit=np.polyval(np.polyfit(time[quiet],blank[quiet],1),time)
 measured=[];control=[]
 for i in range(25):
  sl=slice((i+1)*180,(i+2)*180);measured.append(np.trapezoid(power[sl]-basefit[sl],time[sl]));control.append(np.trapezoid(blank[sl]-blankfit[sl],time[sl]))
 measured=np.array(measured);control=np.array(control);corrected=measured-control
 def fit(data):
  fun=lambda v:titration(np.exp(v[0]),v[1],v[2])[:,4]-data
  out=least_squares(fun,[0,-40,1],bounds=([-6,-150,.4],[5,-1,2]),xtol=1e-12,ftol=1e-12,gtol=1e-12)
  return np.array([np.exp(out.x[0]),out.x[1],out.x[2]])
 fitted=fit(corrected);pred=titration(*fitted)[:,4];wrong=fit(measured);rms=float(np.sqrt(np.mean((pred-corrected)**2)))
 # Independent parametric noise exercise, not variation among biological specimens.
 boots=np.array([fit(pred+rng.normal(0,.08,25)) for _ in range(80)]);ci=np.percentile(boots,[2.5,97.5],axis=0)
 f,ax=plt.subplots(1,2,figsize=(13.5,5.4),layout='constrained')
 ax[0].set(xlim=(0,10),ylim=(0,8));ax[0].axis('off');ax[0].set_title(T('A  1989：配对量热池与功率反馈','A  1989: Matched cells and power feedback'),loc='left')
 ax[0].add_patch(Rectangle((.6,1.4),8.8,4.3,fc='#e6edf0',ec=B,lw=2))
 for x,c,label in [(2.5,B,T('参比池','Reference')),(7,R,T('样品池','Sample'))]:
  ax[0].add_patch(Circle((x,3.4),1.25,fc='#fcfbf7',ec=c,lw=2));ax[0].text(x,3.4,label,ha='center',va='center');ax[0].plot([x-.6,x+.6],[2.8,2.8],c=Y,lw=4)
 ax[0].plot([7,7],[4.7,7.2],c=R,lw=3);ax[0].add_patch(Rectangle((6.6,6.3),.8,.9,fc='#f4d5cb',ec=R));ax[0].annotate('',xy=(7,4.8),xytext=(7,6),arrowprops={'arrowstyle':'->','color':R})
 ax[0].text(5,7.5,T('逐针加入结合伙伴','Inject binding partner'),ha='center');ax[0].annotate('',xy=(5.7,3.4),xytext=(3.8,3.4),arrowprops={'arrowstyle':'<->','color':G});ax[0].text(4.75,4,T('温差','ΔT'),ha='center');ax[0].text(5,.6,T('放热 → 补偿加热减少；积分得到热量','Heat release → less heater power; integrate for heat'),ha='center',fontsize=10)
 ax[1].set_title(T('B  加入的分子：先占位，后积累','B  Added molecules: Occupy, then accumulate'),loc='left');ax[1].plot(ratio,truth[:,3]/truth[:,1],c=R,lw=2,label=T('位点占据比例','Fraction of sites occupied'));ax[1].plot(ratio,(truth[:,2]-truth[:,3])/truth[:,2],c=B,lw=2,label=T('配体中游离的比例','Fraction of ligand free'));ax[1].set(xlabel=T('池内总配体 / 总蛋白质','Cell total ligand / total protein'),ylabel=T('比例','Fraction'),ylim=(0,1.05));ax[1].legend(loc='lower right');ax[1].text(.48,.35,T('Kᴅ = 1 μM；初始蛋白质 20 μM\n构造的一类独立位点模型','Kᴅ = 1 μM; initial protein 20 μM\nConstructed independent-site model'),transform=ax[1].transAxes,fontsize=10)
 save(f,'feedback-binding')
 f,axes=plt.subplots(2,2,figsize=(13.7,8.2),layout='constrained');ax=axes[0,0];ax.plot(time/60,power,c=B,lw=.8,label=T('样品','Sample'));ax.plot(time/60,blank,c=Y,lw=.7,label=T('配体 → 缓冲液','Ligand → buffer'));ax.plot(time/60,basefit,c='#60717c',ls='--',lw=1,label=T('拟合基线','Fitted baseline'));ax.set(xlabel=T('时间 / min','Time / min'),ylabel=T('差分功率 / μW','Differential power / μW'),title=T('A  原始功率：放热向下','A  Raw power: Exothermic downward'));ax.legend(fontsize=9)
 ax=axes[0,1];sl=slice(180,360);ax.plot(pulse_t,power[sl],c=B,label=T('第一针','First injection'));ax.plot(pulse_t,basefit[sl],c='#60717c',ls='--');ax.fill_between(pulse_t,power[sl],basefit[sl],color=B,alpha=.18);ax.plot(pulse_t,blank[sl],c=Y,label=T('空白','Blank'));ax.set(xlabel=T('注射后时间 / s','Time after injection / s'),ylabel=T('差分功率 / μW','Differential power / μW'),title=T('B  面积是热量；峰高还受响应时间影响','B  Area gives heat; height also depends on response'));ax.legend()
 ax=axes[1,0];mol_in=.6;ax.scatter(ratio,measured/mol_in,s=19,color=Y,label=T('未扣除空白','Before blank correction'));ax.scatter(ratio,corrected/mol_in,s=19,color=B,label=T('已扣除空白','Blank-corrected'));ax.plot(ratio,pred/mol_in,c=R,label=T('拟合','Fit'));ax.set(xlabel=T('池内总配体 / 总蛋白质','Cell total ligand / total protein'),ylabel=T('每摩尔加入配体的热量 / kJ/mol','Heat per mole of injected ligand / kJ/mol'),title=T('C  校正、归一化、拟合','C  Correct, normalize and fit'));ax.legend(fontsize=9)
 ax=axes[1,1];ax.axhline(0,c='#60717c',lw=1);ax.plot(np.arange(1,26),corrected-pred,'o-',c=G);ax.set(xlabel=T('针次','Injection'),ylabel=T('数据 − 模型 / μJ','Data − model / μJ'),title=T('D  残差是否留下系统形状','D  Does a systematic pattern remain?'))
 save(f,'thermogram-analysis')
 f,axes=plt.subplots(1,2,figsize=(13.4,5.4),layout='constrained');ax=axes[0]
 for kd,c in [(100,Y),(1,B),(.01,R)]:
  row=titration(kd);ax.plot(row[:,5],row[:,4]/.6,color=c,label=f'c = {20/kd:g}')
 ax.set(xlabel=T('池内总配体 / 总蛋白质','Cell total ligand / total protein'),ylabel=T('热量 / 加入配体量 / kJ/mol','Heat / injected ligand amount / kJ/mol'),title=T('A  平缓、可弯曲、近似阶跃','A  Shallow, curved and nearly step-like'));ax.legend();ax.text(.48,.45,T('所有曲线：ΔH = −40 kJ/mol\n位点数 n = 1','All curves: ΔH = −40 kJ/mol\nSite number n = 1'),transform=ax.transAxes,fontsize=10)
 kds=np.geomspace(.5,2,61);hs=np.linspace(-44,-36,61);err=np.array([[np.sqrt(np.mean((titration(k,h,1)[:,4]-corrected)**2)) for k in kds] for h in hs]);ax=axes[1];im=ax.pcolormesh(kds,hs,err,cmap='viridis_r',shading='auto');ax.set_xscale('log');ij=np.unravel_index(np.argmin(err),err.shape);ax.scatter(kds[ij[1]],hs[ij[0]],marker='x',c='white',s=80);ax.set(xlabel=T('解离常数 Kᴅ / μM','Dissociation constant Kᴅ / μM'),ylabel=T('焓变 ΔH / kJ/mol','Enthalpy ΔH / kJ/mol'),title=T('B  固定 n=1 的条件误差地形','B  Conditional error landscape with n=1'));f.colorbar(im,ax=ax,label=T('均方根残差 / μJ','RMS residual / μJ'))
 save(f,'design-diagnostics')
 gas=.00831446261815324;temperature=298.15;dg=gas*temperature*np.log(1e-6);f,axes=plt.subplots(1,2,figsize=(13.4,5.4),layout='constrained');ax=axes[0];positions=np.arange(3)
 for j,h in enumerate([-40,-20]):ax.bar(positions+(j-.5)*.32,[dg,h,dg-h],.30,color=[B,R][j],label=T(f'体系 {j+1}',f'System {j+1}'))
 ax.set_xticks(positions,['ΔG°','ΔH°','−TΔS°']);ax.axhline(0,c='#61758a',lw=1);ax.set(ylabel=T('摩尔能量 / kJ/mol','Molar energy / kJ/mol'),title=T('A  同一亲和力，可以有不同的热量','A  Same affinity, different heat'));ax.legend();ax.text(.04,.92,T('Kᴅ = 1 μM；T = 298.15 K','Kᴅ = 1 μM; T = 298.15 K'),transform=ax.transAxes,fontsize=10)
 ax=axes[1];L=np.geomspace(.01,200,250);M=20.;bound=2*M*L/(M+L+1+np.sqrt((M+L+1)**2-4*M*L));ax.semilogx(L,L/(1+L),c=B,label=T('横轴作为游离浓度','Axis interpreted as free concentration'));ax.semilogx(L,bound/M,c=R,label=T('横轴作为总浓度，蛋白质20 μM','Axis is total concentration; protein 20 μM'));ax.axhline(.5,c='#61758a',ls='--');ax.scatter([1,11],[.5,.5],c=[B,R],zorder=3);ax.set(xlabel=T('所采用的配体浓度 / μM','Specified ligand concentration / μM'),ylabel=T('位点占据比例','Fraction occupied'),title=T('B  游离配体与总配体是不同的横轴','B  Free ligand and total ligand differ'));ax.legend(fontsize=9,loc='upper left')
 save(f,'thermodynamics')
 np.savetxt(a.output/'thermogram.csv',np.c_[time,power,blank,basefit,blankfit],delimiter=',',header='time_s,sample_power_uW,blank_power_uW,sample_baseline_uW,blank_baseline_uW',comments='')
 np.savetxt(a.output/'injections.csv',np.c_[truth,measured,control,corrected,pred],delimiter=',',header='injection,protein_total_uM,ligand_total_uM,bound_uM,true_heat_uJ,molar_ratio,measured_heat_uJ,blank_heat_uJ,corrected_heat_uJ,fitted_heat_uJ',comments='')
 np.savetxt(a.output/'noise_refits.csv',boots,delimiter=',',header='Kd_uM,enthalpy_kJ_per_mol,site_number',comments='')
 summary={'fitted_Kd_uM':float(fitted[0]),'fitted_enthalpy_kJ_per_mol':float(fitted[1]),'fitted_site_number':float(fitted[2]),'RMS_residual_uJ':rms,'uncorrected_fit_Kd_uM':float(wrong[0]),'uncorrected_fit_enthalpy_kJ_per_mol':float(wrong[1]),'initial_c_value':20.,'standard_free_energy_kJ_per_mol':float(dg),'entropy_J_per_mol_K':float((-40-dg)/temperature*1000),'final_protein_uM':float(truth[-1,1]),'first_binding_heat_uJ':float(q[0]),'last_binding_heat_uJ':float(q[-1]),'injected_ligand_nmol':.6,'half_occupancy_free_ligand_uM':1.,'half_occupancy_total_ligand_uM_at_20uM_protein':11.,'noise_refit_95_percentile_interval':{'Kd_uM':ci[:,0].tolist(),'enthalpy_kJ_per_mol':ci[:,1].tolist(),'site_number':ci[:,2].tolist()}}
 (a.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
```

The repeated noise fits answer a narrow but useful question: if the assumed model and concentrations were correct and injection heats had the specified random variation, how much would the fitted parameters move? The exported percentile intervals describe that calculation. Independent preparations answer a broader question because they also include differences in sample composition and activity. Repeated injections from one preparation occupy an intermediate level. Naming the type of repetition beside an interval or error bar helps a reader connect the uncertainty estimate to the experimental decision it supports.

When replacing the example with measured data, establish power and time units, exothermic direction, actual injection volumes, and active cell volume before implementing the appropriate displacement correction. Active volume enters concentration and heat calculations; total liquid used for loading may also include the cell neck and filling excess. Check complete peak capture and adequate injection spacing before choosing baseline and blank treatment. Previously integrated heats can also be analyzed, while retained raw trajectories help explain unusual points. Before introducing a second class of sites, compare residuals, concentration series, and independent sample-state measurements to establish what physical question the additional parameters address.

For two material hosts binding one guest, use comparable temperature and solvent conditions and define site concentration explicitly: per host molecule, repeat unit, or independently accessible binding site. Multivalent polymers and particles can introduce multiple contacts, cooperativity, or aggregation, changing the appropriate model. A concentration series can first establish reproducible curve changes, followed by structural or particle-size measurements to distinguish binding from assembly. An empirical heat response over a specified range can also support formulation comparisons when that is the intended measurement. The research question determines the required level of model detail.

The next useful experiment often targets information missing from the present curve. A transition that is too sharp may motivate a concentration change or a competition experiment. Small signals from a stable sample may motivate redesigned concentrations and injection volumes. Batch-dependent n values direct attention toward concentration and active components. Preserve temperature, buffer composition, concentration measurements, sample preparation, and the level of replication alongside the result. Affinity and enthalpy then remain connected to molecular structure, material formulation, and subsequent kinetic measurements rather than becoming a list of values detached from their conditions.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/C05.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Wiseman et al. (1989): Rapid measurement of binding constants and heats of binding](https://web.iitd.ac.in/~nkurur/2012-13/Isem/cyl501/analbiochem179_131.pdf)

   Original matched cells, feedback power, integration and concentration design.
2. [Harvard CMI: Isothermal titration calorimetry](https://cmi.hms.harvard.edu/isothermal-titration-calorimetry)

   Sample/reference roles, buffer matching and concentration preparation.
3. [TA Instruments: Quick Start ITC, MCAPN-2016-1](https://www.tainstruments.com/pdf/literature/MCAPN-2016-1.pdf)

   Power signs, active cell volume versus loaded volume.
4. [Malvern: Best practices for ITC, Part 1](https://www.malvernpanalytical.com/en/learn/knowledge-center/insights/best-practices-for-isothermal-titration-calorimetry-to-study-binding-interactions-part-1)

   c value, sample state and matched buffers.
5. [TA Instruments: Protein-protein interactions by ITC, MC176](https://www.tainstruments.com/applications-notes/characterizing-protein-protein-interactions-by-itc-mc176/)

   Binding heat linked to solvent and proton exchange.
6. [Brautigam et al. (2016): Integration and Global Analysis of ITC Data](https://pmc.ncbi.nlm.nih.gov/articles/PMC7466939/)

   Baseline analysis, global fitting and concentration/n confounding.
