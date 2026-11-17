# TGA: Composition and stability in changing mass

Source: https://ml-biomat.com/tutorials/experimental-methods/t02/en/
Language: en

Account for every lost portion, from water, char and ash to stability governed by temperature and time.

## When a material becomes lighter, what has actually left?

A biopolymer film containing mineral particles raises several practical questions. How much water has it absorbed? What fraction is organic? What remains after heating? One weighing gives a total, rather like weighing a packed suitcase without learning the separate contributions of clothes, a water bottle and metal fittings. Thermogravimetric analysis turns weighing into a continuous observation. A specimen follows a prescribed temperature and atmosphere while a balance records its changing mass. Evaporation, decomposition and oxidation can produce descending regions separated by plateaus. Their usefulness comes from connecting each change to the experimental conditions and chemical processes, rather than reading only the final percentage.

The method is commonly abbreviated TGA, and the mass trace is called a TG curve. Its measured quantity differs from differential scanning calorimetry. DSC follows energy entering or leaving the specimen; TGA follows mass remaining in the pan. Ice absorbs energy when it melts, yet the mass can remain constant if the water stays in the container. Mass falls when water escapes as vapor. Polymer glass transitions and melting can likewise occur with little mass change. A horizontal TG trace therefore describes stable mass over that interval, while internal rearrangement may still occur. Comparing heat flow and mass on a common temperature axis helps distinguish an endothermic event associated with volatilization from a phase change that retains material.

Materials applications include volatile content in coatings, organic and inorganic fractions in composites, and differences between inert and oxidizing conditions. Biological materials bring questions about water in dried scaffolds, organic matrix in mineralized tissue substitutes and water incorporated into pharmaceutical crystals. Even the word water can hide several environments. Surface moisture, water within pores and crystallographic water need not leave in the same way. Temperature regions provide clues, while chemical assignment becomes stronger when composition, reaction stoichiometry and evolved-gas measurements agree. Coupling the outlet to infrared spectroscopy or mass spectrometry adds information about what leaves, complementing the balance measurement of how much leaves.

Keep one question in mind throughout the chapter: was a particular lost portion present as that substance in the original specimen, or was it created during heating and released later? The answer changes calculations of polymer, carbon black and ash. We use a constructed specimen with a known recipe so that every mass contribution has an explicit destination. Calcium oxalate monohydrate then provides a chemically defined example in which a formula predicts the heights of mass-loss steps. Finally, changing heating rate and holding time reveals why a quoted decomposition temperature needs an accompanying experimental program. The chapter develops these as connected decisions, from selecting a specimen state to deciding which additional measurement would resolve an ambiguity.

## The thermobalance: continuous weighing in a controlled environment

In an interrupted gravimetric experiment, a substance is heated, cooled, removed and weighed before heating resumes. This produces useful individual points, but cooling and transfer interrupt the process and may allow moisture or oxygen to enter. Early twentieth-century thermobalance work by Honda, Saito and others connected continuous weighing with controlled heating and atmosphere. Saito’s early paper discussed different gases, continuous temperature ramps and staged holds. The historical advance was therefore more than increased balance sensitivity. It made the timing and environment of each weighing part of a recorded experiment. The present instrument inherits that idea: a mass value becomes interpretable because the temperature, elapsed time and gas conditions are known alongside it.

A modern thermobalance combines a sensitive balance, specimen pan, furnace, temperature sensor and gas system. The specimen transfers its load through a support to the balance, while the furnace executes the temperature program. Gas establishes a chemical environment and carries away evolved products. The lever arrangement in the figure is an original principle diagram, not a reconstruction of a particular historical apparatus; actual instruments use several suspension and feedback geometries. Nitrogen is commonly used to investigate pyrolysis, decomposition under oxygen-poor conditions. Air can subsequently oxidize some carbonaceous residue. Different traces under these atmospheres arise because chemical pathways change, rather than because one universal curve has simply shifted sideways.

![Original principle diagram connecting to early continuous thermobalance work by Honda and Saito; not to scale or a copy of a historical instrument. Right: the constructed specimen’s temperature and atmosphere program.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/a934dd292007fa895683c9ff.svg?v=a934dd292007)

Figure 1Original principle diagram connecting to early continuous thermobalance work by Honda and Saito; not to scale or a copy of a historical instrument. Right: the constructed specimen’s temperature and atmosphere program.

The surrounding gas also affects the balance. Temperature-dependent density changes buoyancy, flowing gas can exert mechanical forces, and switching between nitrogen and air may create a short transient. An empty-pan run using the corresponding pan, flow, ramp and switch sequence helps characterize these backgrounds. Taring a kitchen bowl provides a useful analogy, except that the environment around this bowl changes throughout the experiment: the correction is a time-dependent trace rather than a single number. Preserve the blank record and inspect the gas-switch region in particular. A brief feature appearing in both specimen and blank records suggests an instrumental contribution that should be examined before assigning a new chemical component.

Loading geometry matters as well. A deep powder bed can develop temperature differences and require evolved gases to travel farther than a thin layer of the same mass. Pan material, lid arrangement, particle size, flow and temperature program should therefore be chosen for the question and recorded with the result. Hygroscopic samples add another variable: the interval between weighing and starting the run can change the initial water content. Comparisons between scaffolds should begin by specifying an equivalent initial condition, such as as-received material, equilibration at a selected humidity or a common drying treatment. Matching that condition gives the normalization denominator a consistent physical meaning. A reproducible experiment starts before the furnace is switched on, because sampling and conditioning determine which material enters the measurement.

## Read the mass steps before interpreting derivative peaks

Mass can also increase. Oxidation of some metal powders incorporates oxygen into a retained solid, producing an upward trace. Simultaneous oxidation and volatilization give a net signal that may even appear temporarily flat. Small net change therefore need not mean little reaction. Inspect atmosphere, plausible chemistry and the blank together, then examine whether an oxide forms or a buoyancy contribution explains the observation. Retaining a signed mass trace is particularly useful when opposing processes overlap.

Mass is often normalized so that the initial specimen represents one hundred percent. If an independently weighed specimen starts at 10 mg and later contains 9.2 mg, its remaining fraction is ninety-two percent and its accumulated loss is eight percent. Normalization makes different loading amounts easier to compare, but it does not remove differences in initial condition. Someone who first dries the same specimen has selected a different starting object. A reported twenty-percent residue should therefore be identified as a fraction of the original wet specimen, the dry material or a selected component. The calculation makes a chosen denominator explicit; it does not automatically harmonize experiments that started with different specimens.

$$
w(t)=\frac{m(t)}{m_0},\qquad L_{a\to b}=\frac{m(t_a)-m(t_b)}{m_0}\times100\%
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/270613e026ede7b90829cf4d.svg) | Remaining mass fraction at time t, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/1c845ebfe8aa7560445baa5c.svg) | Background-corrected specimen mass, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/2fae4459b565e480de0d463f.svg) | Specimen mass in the defined initial state, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/7409c350063c63e2d0b0ffa5.svg) | Time and selected stage limits, min. |
| ![Formula](https://ml-biomat.com/static/agent-math/3b6a7273a3af8b17fc5a7bab.svg) | Stage loss as a percentage of initial mass, percent. |

A common denominator makes stages portions of one initial mass. m0=10 mg and a decrease from 10 to 9.2 mg give 8% loss and remaining fraction 0.92. Percentages using different stage denominators cannot be added directly.

The teaching specimen starts at 10 mg. It is heated in nitrogen at ten degrees Celsius per minute to 600 °C, held there and switched to air at minute seventy. Its prescribed starting composition is 0.8 mg water, 6 mg polymer, 1.2 mg added carbon and 2 mg stable inorganic material. After the low-temperature event about 9.2 mg remains; after inert pyrolysis about 3.8 mg remains; after the air stage the residue approaches 2 mg. The calculated fractions are approximately 8.01%, 53.99%, 18.00% and 20.00%. Small departures from exact values result from constructed noise and finite averaging intervals. Initially call these low-temperature loss, nitrogen-stage loss, air-stage loss and final residue. Chemical names require the additional reasoning developed below.

The steepest descending region of a TG trace corresponds to the greatest loss per unit time. Differentiating mass with respect to time produces a rate; this chapter adds a minus sign so that loss peaks point upward. The resulting curve is commonly called DTG. Software conventions vary: the sign may be reversed, and the vertical axis may use milligrams per minute, percent per minute or percent per degree. Read the unit before interpreting a peak. A constant heating rate connects time and temperature derivatives during a ramp. During an isothermal hold, however, temperature is fixed while reaction continues. Time is then the natural coordinate for displaying the process, including oxidation after a gas change.

$$
r_t=-\frac{1}{m_0}\frac{dm}{dt},\qquad r_T=-\frac{1}{m_0}\frac{dm}{dT},\qquad r_t=\beta r_T,\quad\beta=\frac{dT}{dt}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d2410ee324d5f3cc2de959fa.svg) | Initial-mass-normalized loss rate, min⁻¹; multiply by 100 for percent/min. |
| ![Formula](https://ml-biomat.com/static/agent-math/78c3388d05455d424532a900.svg) | Loss rate per temperature interval, K⁻¹ or °C⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/9a358ffe402fdf3c4c31be5d.svg) | Current and initial masses, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time, min. |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | Temperature, °C or K with consistent interval units. |
| ![Formula](https://ml-biomat.com/static/agent-math/f27acf6959fc15846a7239da.svg) | Heating rate, K/min or °C/min. |

The chain rule multiplies the change per degree by the temperature change per minute. A 10 mg specimen losing 0.2 mg/min has a normalized time rate of 0.02 min⁻¹, or 2%/min. At a heating rate of 10 K/min, this becomes 0.002 K⁻¹, or 0.2%/K. During an isothermal hold the heating rate is zero, so the time derivative is the appropriate rate.

![Simulated thermogravimetric data, seed 720, with an initial mass of 10 mg. All percentages use that initial mass. The blank follows the same temperature and atmosphere program, and the DTG sign convention makes mass loss positive. Cubic local-polynomial windows contain 7, 21 or 61 points; at 0.05 min sampling intervals, they span 0.3, 1.0 or 3.0 min.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/884b79e1262fa1ae328e5814.svg?v=884b79e1262f)

Figure 2Simulated thermogravimetric data, seed 720, with an initial mass of 10 mg. All percentages use that initial mass. The blank follows the same temperature and atmosphere program, and the DTG sign convention makes mass loss positive. Cubic local-polynomial windows contain 7, 21 or 61 points; at 0.05 min sampling intervals, they span 0.3, 1.0 or 3.0 min.

Differentiation emphasizes small differences between neighboring points. A visually smooth mass trace can consequently produce a noisy derivative. The example compares Savitzky–Golay local-polynomial windows spanning approximately 0.3, 1.0 and 3.0 minutes. A shorter window retains more fluctuations; a longer window broadens the abrupt air-stage onset and can produce overshoot around sharp changes. Select smoothing by comparing the original trace, sampling interval and duration of the scientific event. Stable features should survive reasonable processing choices. Peak count is not an automatic component count: several reactions may overlap into one maximum, and one substance may undergo dehydration, chain cleavage and oxidation in successive regions. Reading TG and DTG together preserves the distinction between the amount lost and the rate at which it leaves.

## Char changes the composition calculation

Calling the entire nitrogen-stage loss polymer content would give approximately fifty-four percent in this example, below the true sixty percent. The model polymer retains one tenth of its original mass as char. That newly formed 0.6 mg remains in the pan alongside the original 1.2 mg added carbon, and both are consumed in the air stage. Calling all eighteen percent of the air-stage loss original carbon black would therefore overestimate the added carbon. Every step is a valid mass account, but assigning a chemical name requires a reaction path. Early loss is not automatically identical to polymer, and later oxidative loss is not automatically identical to carbon that was present before heating.

An independently established char yield can separate these contributions. If nine tenths of a polymer’s original mass becomes volatile products under the matched conditions, a measured pyrolysis loss of 5.4 mg corresponds to 6 mg original polymer. Its remaining 0.6 mg char is subtracted from the 1.8 mg oxidative loss, leaving 1.2 mg original added carbon. The char yield is additional chemical information, not a freely adjusted parameter extracted from the same two losses. A suitable comparison polymer should be measured under matching conditions, with attention to changes caused by fillers, crosslinking or atmosphere. Those changes can alter the relation between initial polymer mass and retained char.

$$
m_p=\frac{\Delta m_{\mathrm{py}}}{1-y},\qquad m_c=\Delta m_{\mathrm{ox}}-y m_p
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/63b17c0ff2d1bd233aeb8ba3.svg) | Initial polymer mass, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/5b5b59c6334e2c66dd05e12e.svg) | Pyrolysis loss assigned to volatile polymer products, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/1d9b846cface9f9348e4081a.svg) | Polymer char mass divided by initial polymer mass under matched conditions, dimensionless and independently specified. |
| ![Formula](https://ml-biomat.com/static/agent-math/da91b33ee64dd3e861a37f01.svg) | Original added carbon mass in the model, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/bc150985325e893d423793e2.svg) | Combined loss of new char and original carbon on complete oxidation, mg. |

Assume that the pyrolysis loss consists of volatile products from the polymer, that the original carbon survives pyrolysis, and that the oxidation stage consumes all carbon without other mass changes. A pyrolysis loss of 5.4 mg with a char yield of 0.1 corresponds to 6 mg of initial polymer. This polymer produces 0.6 mg of char; subtracting it from the 1.8 mg oxidation loss leaves 1.2 mg of originally added carbon.

![Simulated mass balance for a mixture containing 60% polymer, 8% water, 12% added carbon and 20% stable inorganic material. A polymer char yield of 0.1 produces char equal to 6% of the initial mixture mass. The right panel holds the stage losses at 54% and 18% while varying the independently specified char yield, showing how this assumption changes the inferred composition.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/84e508189e7a1a1953d0b45d.svg?v=84e508189e7a)

Figure 3Simulated mass balance for a mixture containing 60% polymer, 8% water, 12% added carbon and 20% stable inorganic material. A polymer char yield of 0.1 produces char equal to 6% of the initial mixture mass. The right panel holds the stage losses at 54% and 18% while varying the independently specified char yield, showing how this assumption changes the inferred composition.

The right-hand plot increases the assumed char yield while keeping the two measured stage losses fixed. Inferred polymer content rises, while inferred original carbon content falls. This is a family of mass balances consistent with the same observations. The simple model requires a char yield no greater than one quarter to keep the inferred added carbon nonnegative. That algebraic boundary is not a known material property. Instead, the family of solutions identifies useful next measurements: a corresponding polymer without added carbon, or another technique that distinguishes the residue’s chemical origin. A well-chosen control supplies the missing information more directly than adding decimal places to the same TG curve.

Final residue also needs a reaction-based name. In this example the 2 mg inorganic component is deliberately defined as stable, so completion of the air stage recovers its original mass. Real carbonates can release carbon dioxide, metals can gain oxygen and some inorganic compounds can volatilize or react. Their final residues may therefore represent products rather than unchanged starting filler. The normalization basis creates a separate distinction: 2 mg is twenty percent of the initial 10 mg, but approximately 21.74% of the 9.2 mg dry specimen. Both values answer useful questions when their denominators are explicit. Keep the chemical identity question and the normalization question separate rather than treating either as a software setting.

## What substances can occupy the same residue?

The simulated mixture contains 8% water, 60% polymer, 12% original carbon and 20% stable inorganic material. Vary polymer char yield and air-stage completion to inspect the difference between oxidative loss and original carbon, and between final residue and original mineral.

[Figure: Mass account for char yield and oxidation completion](https://ml-biomat.com/tutorials/experimental-methods/t02/en/#T02-plot)

The interactive experiment fixes the original polymer, carbon and mineral fractions while varying polymer char yield, the fraction of carbon consumed in air and total loading. Begin with complete oxidation, then reduce its completion. Final residue now includes unburned carbon as well as mineral. Reaching the last recorded point is not the same as reaching the intended chemical endpoint. Changing loading scales the model’s milligram values while leaving percentages unchanged. If real normalized results depend strongly on loading, investigate thermal gradients, gas access and completion. This comparison turns a simple slider into a diagnostic question about the physical experiment rather than a cosmetic alteration of the plot.

## A chemical formula predicts the mass steps

Before calculating a hydrate number, establish whether one formula adequately describes the starting powder. Another salt or adsorbed liquid contributes additional loss. Structural comparisons and conditioning controls help distinguish these possibilities. The chemical formula supplies a predicted mass ratio; the experiment tests agreement. Disagreement directs attention to extra components, overlapping reactions or incomplete conversion rather than being resolved by rounding a calculated water count to the nearest convenient integer.

Calcium oxalate monohydrate provides a chemically defined example of sequential mass loss. Its formula, CaC₂O₄·H₂O, includes water as part of the crystal composition rather than an arbitrary surface droplet. Under suitable conditions, the sequence includes dehydration, conversion of oxalate to carbonate and conversion of carbonate to oxide. The associated evolved species involve water, carbon monoxide and carbon dioxide. Writing both the retained solid and the departing material establishes the mass account before a curve is interpreted. Atomic weights then connect a seemingly abstract percentage step to a definite amount of chemical matter, making stoichiometry an independent check on the measurement.

Using approximate atomic weights of 40.078 for calcium, 12.011 for carbon, 15.999 for oxygen and 1.008 for hydrogen gives a formula mass of 146.111 g/mol for the monohydrate. Each mole contains 18.015 g water, so complete dehydration predicts about 12.33% loss. Subsequent release of one mole of CO and one mole of CO₂ corresponds to approximately 19.17% and 30.12% of the original hydrate mass, leaving about 38.38% CaO. All percentages here use the same initial denominator and sum to one hundred percent. If each stage were instead normalized by its immediately preceding plateau, the percentages would change and could no longer be added as portions of one original mass.

![Stoichiometric mass model of calcium oxalate monohydrate. Steps use initial hydrate mass and the stated approximate atomic weights. Curve shapes and transition temperatures are constructed, not measured.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/be4920ee8621bf40d0298888.svg?v=be4920ee8621)

Figure 4Stoichiometric mass model of calcium oxalate monohydrate. Steps use initial hydrate mass and the stated approximate atomic weights. Curve shapes and transition temperatures are constructed, not measured.

The calculation can also run backward to estimate the number of waters of crystallization. Picture the hydrate as an anhydrous unit of known mass plus an unknown number of water molecules. Adding water increases both the water contribution and the total formula mass, so multiplying a measured percentage by the anhydrous mass alone does not finish the calculation. Solving the mass-fraction relation gives the expression below. A water-loss fraction near 0.1233 and an anhydrous calcium oxalate formula mass of 128.096 g/mol recover approximately one water per unit. This inference assumes that the selected loss is principally water, the starting solid composition is known and dehydration can be distinguished from other decomposition.

$$
f_w=\frac{n_w M_w}{M_a+n_w M_w},\qquad n_w=\frac{f_w M_a}{M_w(1-f_w)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/40240877de058d73b2fe4254.svg) | Water mass fraction in the initial hydrate, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/5b794cb38c00fee5cea77f6d.svg) | Number of water molecules per anhydrous formula unit, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/584328b60ee68abee6861462.svg) | Molar mass of water, 18.015 g/mol here. |
| ![Formula](https://ml-biomat.com/static/agent-math/acae10568b66868832f17363.svg) | Molar mass of the anhydrous formula unit, 128.096 g/mol here. |

Water contributes to both numerator and total-mass denominator. Solving the fraction gives the hydration number. fw=18.015/146.111≈0.1232967 gives nw=1. The selected loss must correspond to that hydrate’s water and be separated from other volatile or decomposition contributions.

The illustrated step heights follow that stoichiometry, whereas curve shapes and transition temperatures are constructed. In actual measurements, loading, pan geometry, gas, heating rate and the definition of onset affect observed temperatures. A published multi-laboratory calcium oxalate study examines such protocol differences, emphasizing why measurements should share definitions before numerical comparison. For an unknown biomineralized specimen, a similar low-temperature loss might include surface moisture or retained solvent. Humidity conditioning, evolved-gas identification and solid-state structural measurements can separate those contributions. The formula-based calculation then refers to a particular chemical species rather than assigning every low-temperature milligram to crystallographic water. Matching the mass result to the chemical question is the central task, even when the arithmetic itself is short.

## Why faster heating can make a material appear more stable

Common thermal-stability descriptors include the temperature at five-percent initial mass loss and the temperature of a DTG maximum. These are convenient comparisons under a common program, but both contain information about elapsed time. Imagine identical specimens heated at five and twenty degrees per minute. On reaching the same temperature, the faster specimen has spent less time in all preceding temperature intervals. Even with identical reaction kinetics, less conversion may have accumulated, so a higher temperature is required to reach the selected fraction. Instrument and specimen temperature lag can add another shift. A temperature read from a programmed scan consequently combines chemical kinetics with the schedule used to reveal them.

To isolate the time effect, we use a constructed single-step first-order model. At any instant, reaction rate is proportional to the fraction still unconverted, while an Arrhenius expression describes the temperature-dependent rate constant. First order names this mathematical dependence; it does not assert that a real polymer decomposes through only one elementary chemical event. Conversion refers to the complete mass change of the selected reaction, rather than treating permanent ash as material that must eventually disappear. Activation energy describes the temperature sensitivity of rate and is a different physical quantity from the reaction heat measured by calorimetry. These definitions allow a small model to illuminate one mechanism without confusing its parameters with directly measured composition.

$$
\alpha=\frac{m_s-m(t)}{m_s-m_f},\qquad\frac{d\alpha}{dt}=k(T)(1-\alpha),\qquad k(T)=A\exp\!\left(-\frac{E_a}{RT}\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | Converted fraction of the selected reaction, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/f38b34c4861f4340ecef52cd.svg) | Masses at the start and complete end of the selected reaction, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/1c845ebfe8aa7560445baa5c.svg) | Mass at time t, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time, min. |
| ![Formula](https://ml-biomat.com/static/agent-math/fc90edd0d6c7e9e5eceaaa94.svg) | First-order rate constant at temperature T, min⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Prefactor, 10¹⁰ min⁻¹ in this model. |
| ![Formula](https://ml-biomat.com/static/agent-math/fc22571629d5ee46df4d11e5.svg) | Arrhenius activation energy, 140000 J/mol in the model. |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | Gas constant 8.314462618 J/(mol·K). |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | Absolute temperature, kelvin. |

In this single-step first-order model, the reaction rate is proportional to the unconverted fraction, and the final mass must correspond to complete conversion. At 300 °C, or 573.15 K, the fixed Arrhenius parameters give a rate constant of about 0.00174261 min⁻¹. Starting from zero conversion, a 60 min hold gives 1 − exp(−0.00174261 × 60), approximately 0.09928 or 9.93%. The model describes one reaction step without diffusion control.

![Constructed single-step first-order kinetics, A=10¹⁰ min⁻¹ and Ea=140 kJ/mol. Left changes only heating rate; right holds at 300 °C. Heat-transfer lag and diffusion are not included.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/35f0c1de56c6869c0a8d0e21.svg?v=35f0c1de56c6)

Figure 5Constructed single-step first-order kinetics, A=10¹⁰ min⁻¹ and Ea=140 kJ/mol. Left changes only heating rate; right holds at 300 °C. Heat-transfer lag and diffusion are not included.

The model uses a prefactor of ten billion per minute and an activation energy of 140 kJ/mol. At heating rates of 5, 10 and 20 °C/min, five-percent conversion occurs near 340.78, 355.61 and 371.15 °C, respectively. Neither the material nor its kinetic parameters changed; only the time spent crossing each temperature interval changed. Conversely, holding the model at 300 °C gives about 9.93% conversion after sixty minutes and 46.60% after six hours. A temperature well below the ramp’s five-percent-conversion temperature can therefore accumulate substantial change over a longer exposure. The comparison explains why one scan temperature cannot substitute for a time-dependent service question.

For a short processing step, investigate atmospheres and residence times related to that process. For storage or service, obtain isothermal evidence over relevant temperatures and times and examine whether the reaction pathway remains comparable. Multiple heating rates help expose kinetic differences, but overlapping reactions, diffusion constraints and changing oxygen access can require a more detailed model. Define the baseline, reaction interval, atmosphere and total conversion before choosing a kinetic analysis. A flat-looking late segment does not automatically establish complete conversion if the reaction has merely slowed. With these choices explicit, improved stability has a precise meaning: later mass loss under a matched ramp, or greater retained mass after a specified exposure. Those are related but distinct experimental questions.

## Turn a curve into a result that supports the next experiment

Onset also needs an operational definition. An extrapolated intersection between a baseline and a descending tangent differs from the temperature at five-percent accumulated loss. A little water or solvent can supply that first five percent before substantial backbone decomposition. Define the loss of interest before selecting an onset descriptor, and retain the conditioning and geometric definition when comparing results.

The complete program starts from a known mass inventory and constructs raw balance readings, an empty-pan background, three derivative-smoothing choices and an atmosphere switch. It exports pointwise time, temperature, mass and derivative data, alongside plateau averages and composition calculations. Separate outputs address hydrate stoichiometry and first-order kinetics, keeping amount, chemical identity and elapsed time connected to their respective calculations. Each constructed trace retains its generation conditions. Changing one parameter reveals its effect without presenting the result as an observed property of a real material. The figures shown above are the program’s actual outputs, so numerical statements can be traced back to exported values rather than reconstructed from a picture.

### Complete thermogravimetry, char accounting and time-effect analysis

Exports raw/blank/corrected mass, three derivatives, hydrate stoichiometry, ramp and isothermal kinetics, and five bilingual figures.

```
"""TGA mass accounting, derivatives, hydrate stoichiometry and rate effects.

All traces are constructed teaching models, not measurements of a real specimen.
Run: python main.py --output results --language en
"""
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.special import expit
from scipy.signal import savgol_filter
from scipy.integrate import cumulative_trapezoid
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

P=argparse.ArgumentParser();P.add_argument('--output',type=Path,required=True)
P.add_argument('--language',choices=['zh','en'],default='en');args=P.parse_args()
OUT=args.output;OUT.mkdir(parents=True,exist_ok=True);ZH=args.language=='zh'
def L(z,e):return z if ZH else e
plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],
 'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
 'axes.facecolor':'#fcfbf7','figure.facecolor':'#fcfbf7','svg.fonttype':'none',
 'axes.labelcolor':'#20333e','text.color':'#20333e','axes.titleweight':'bold'})
B='#167d9a';R='#d35f47';G='#37967d';Y='#c49b35';K='#20333e'
def save(fig,name):
 for ext in ['svg','png']:fig.savefig(OUT/f'{name}-{args.language}.{ext}',dpi=145,bbox_inches='tight')
 plt.close(fig)
def csv(name,headers,cols):np.savetxt(OUT/name,np.column_stack(cols),delimiter=',',header=','.join(headers),comments='',fmt='%.10g')
def frac(x,center,width):
 a=expit((x-center)/width);a0=expit((x[0]-center)/width)
 return (a-a0)/(1-a0)

rng=np.random.default_rng(720)
t=np.arange(0,95.0001,.05);T=np.minimum(25+10*t,600)
water=frac(T,95,12);pyro=frac(T,350,18)
burn=np.where(t>=70,1-np.exp(-.5*np.maximum(t-70,0)),0)
true=10-.8*water-5.4*pyro-1.8*burn
blank=.028+.00008*(T-25)+.00012*t+.025*np.exp(-np.maximum(t-70,0)/.25)*(t>=70)
raw=true+blank+rng.normal(0,.0015,t.size)
blank_record=blank+rng.normal(0,.001,t.size);corrected=raw-blank_record
m0=10.0 # Independent initial mass, mg; every percentage uses this denominator.
plateau=lambda mask:float(np.mean(corrected[mask]))
dry=plateau((T>=180)&(T<=220));inert=plateau((t>=60)&(t<=68));ash=plateau(t>=90)
losses=np.array([m0-dry,dry-inert,inert-ash,ash])/m0*100
dtg={w:-savgol_filter(corrected,w,3,deriv=1,delta=.05)/m0*100 for w in [7,21,61]}
polymer=(dry-inert)/.9;carbon=inert-ash-.1*polymer
csv('tga_scan.csv',['time_min','temperature_C','true_mass_mg','raw_mass_mg','blank_mass_mg','corrected_mass_mg','dtg_window7_percent_per_min','dtg_window21_percent_per_min','dtg_window61_percent_per_min'],[t,T,true,raw,blank_record,corrected,dtg[7],dtg[21],dtg[61]])

# Figure 1: original explanatory apparatus, not a historical reconstruction.
fig,axs=plt.subplots(1,2,figsize=(12,4.9),gridspec_kw={'width_ratios':[1.1,1]},layout='constrained')
a=axs[0];a.set(xlim=(0,10),ylim=(0,8));a.axis('off')
a.add_patch(Rectangle((3.7,1.1),3.2,3.6,fill=False,ec=R,lw=3))
a.add_patch(Rectangle((4,1.4),2.6,3,fill=False,ec=R,lw=1,ls='--'))
a.plot([2,7.5],[6.4,6.4],color=K,lw=3)
a.add_patch(Polygon([[4.4,5.9],[5,6.4],[5.6,5.9]],color=K))
a.plot([2.4,2.4],[6.4,5.3],color=K);a.add_patch(Rectangle((1.7,4.9),1.4,.4,color=B))
a.plot([5.3,5.3],[6.4,3.6],color=K,lw=1.5)
a.add_patch(Polygon([[4.7,3.6],[4.9,3.2],[5.7,3.2],[5.9,3.6]],fc=Y,ec=K))
a.annotate('',xy=(4.2,2.1),xytext=(2.1,2.1),arrowprops={'arrowstyle':'->','color':G,'lw':2})
a.annotate('',xy=(8.4,4.2),xytext=(6.7,4.2),arrowprops={'arrowstyle':'->','color':G,'lw':2})
a.text(1.9,1.4,L('受控气体入口','Controlled gas'),color=G,ha='center')
a.text(8,4.7,L('排出气体','Evolved gas'),color=G,ha='center')
a.text(2.4,7,L('质量读数','Mass readout'),ha='center')
a.text(5.3,2.7,L('坩埚与样品','Pan + specimen'),ha='center',fontsize=9)
a.text(7.2,2.5,L('炉体','Furnace'),color=R)
a.text(5,.25,L('连续称量：把“加热后再称”变为一条轨迹\n原理示意；联系 Honda 与 Saito 的早期热天平工作','Continuous weighing replaces interrupted heat–cool–weigh cycles\nPrinciple diagram; early thermobalance work of Honda and Saito'),ha='center',fontsize=9)
a.set_title(L('A  质量、温度、气氛同时记录','A  Mass, temperature and atmosphere'))
a=axs[1];a.plot(t,T,color=R,lw=2);a.set(xlabel=L('时间 / min','Time / min'),ylabel=L('程序温度 / °C','Programmed temperature / °C'),ylim=(0,670))
a.axvspan(0,70,color=B,alpha=.08);a.axvspan(70,95,color=G,alpha=.12)
a.axvline(70,color=G,ls='--');a.text(25,110,L('氮气','Nitrogen'),color=B);a.text(79,110,L('空气','Air'),color=G)
a.annotate(L('600 °C 保温','600 °C hold'),xy=(65,600),xytext=(38,470),arrowprops={'arrowstyle':'->','color':K})
a.set_title(L('B  构造样品的实验程序','B  Program for the teaching specimen'));save(fig,'balance-history')

fig,axs=plt.subplots(2,2,figsize=(12,8.4),layout='constrained')
a=axs[0,0];a.plot(t,100*raw/m0,color=Y,lw=1,label=L('原始','Raw'));a.plot(t,100*corrected/m0,color=B,lw=1.2,label=L('减去空坩埚','Blank corrected'))
a.axvline(70,color=G,ls='--');a.set(xlabel=L('时间 / min','Time / min'),ylabel=L('剩余质量 / 初始质量 %','Remaining mass / initial mass %'),title=L('A  同时保留原始与校正轨迹','A  Preserve raw and corrected traces'));a.legend(frameon=False)
a=axs[0,1];a.plot(t,blank_record,color=Y,lw=1);a.axvline(70,color=G,ls='--');a.set(xlim=(66,75),xlabel=L('时间 / min','Time / min'),ylabel=L('空坩埅读数 / mg','Empty-pan reading / mg'),title=L('B  换气也会推动天平读数','B  A gas switch also moves the balance'))
a=axs[1,0]
for w,c in [(7,'#a8b8bf'),(21,B),(61,R)]:a.plot(t,dtg[w],color=c,lw=1,label=L(f'{(w-1)*.05:.1f} min 窗口',f'{(w-1)*.05:.1f} min window'))
a.set(xlim=(66,78),xlabel=L('时间 / min','Time / min'),ylabel=L('失重速率 / % 初始质量·min⁻¹','Mass-loss rate / % initial mass min⁻¹'),title=L('C  导数放大噪声，平滑改变尖锐转折','C  Derivatives amplify noise; smoothing changes corners'));a.legend(frameon=False,fontsize=9)
a=axs[1,1];labels=L(['低温失重','氮气热解','空气中失重','最终残余'],['Low-T loss','N₂ pyrolysis','Air-stage loss','Final residue'])
a.bar(labels,losses,color=[B,R,K,Y]);a.set(ylabel=L('初始质量的百分比 / %','Percent of initial mass / %'),ylim=(0,65),title=L('D  先得到操作定义的四份质量','D  Four operationally defined mass fractions'))
for i,v in enumerate(losses):a.text(i,v+1,f'{v:.2f}',ha='center')
save(fig,'mass-derivative')

y=np.linspace(0,.25,151);inferred_poly=54/(1-y);inferred_carbon=18-y*inferred_poly
fig,axs=plt.subplots(1,2,figsize=(12,5),layout='constrained')
a=axs[0];parts=[(8,B,L('水 8','Water 8')),(54,R,L('挥发产物 54','Volatile products 54')),(6,'#bfa5a0',L('新生成炭 6','New char 6')),(12,K,L('原有炭黑 12','Added carbon 12')),(20,Y,L('矿物残余 20','Mineral residue 20'))]
left=0
for value,c,label in parts:a.barh(.5,value,left=left,color=c,height=.35);a.text(left+value/2,.76,label,rotation=45,ha='left',fontsize=9);left+=value
a.set(xlim=(0,105),ylim=(0,1.65),yticks=[],xlabel=L('初始质量的百分比 / %','Percent of initial mass / %'),title=L('A  60% 聚合物留下了 6% 炭','A  60% polymer leaves 6% char'))
a.annotate(L('空气阶段一起烧掉：18%','Consumed together in air: 18%'),xy=(70,.30),xytext=(43,.06),arrowprops={'arrowstyle':'->','color':K},fontsize=9)
a=axs[1];a.plot(y,inferred_poly,color=R,lw=2,label=L('推算聚合物','Inferred polymer'));a.plot(y,inferred_carbon,color=K,lw=2,label=L('推算原有炭黑','Inferred added carbon'));a.axvline(.1,color=B,ls='--');a.scatter([.1,.1],[60,12],c=[R,K]);a.set(xlabel=L('独立给定的聚合物残炭比例 y','Independently specified polymer char yield y'),ylabel=L('初始样品质量的百分比 / %','Percent of initial specimen mass / %'),ylim=(0,76),title=L('B  相同失重分配，可有不同原始组成','B  Same stage losses, different original compositions'));a.legend(frameon=False)
save(fig,'char-composition')

# Stoichiometry uses rounded standard atomic weights, g/mol.
Ca,C,O,H=40.078,12.011,15.999,1.008
MW=Ca+2*C+5*O+2*H;waterMW=2*H+O;coMW=C+O;co2MW=C+2*O;oxideMW=Ca+O
stoich=np.array([waterMW,coMW,co2MW,oxideMW])/MW*100
Th=np.linspace(25,900,1751)
hm=100-stoich[0]*frac(Th,170,12)-stoich[1]*frac(Th,500,18)-stoich[2]*frac(Th,750,22)
csv('hydrate.csv',['temperature_C','constructed_remaining_percent'],[Th,hm])
fig,axs=plt.subplots(1,2,figsize=(12,5),layout='constrained')
a=axs[0];a.plot(Th,hm,color=B,lw=2);a.set(xlabel=L('温度 / °C','Temperature / °C'),ylabel=L('初始质量的百分比 / %','Percent of initial mass / %'),ylim=(30,105),title=L('A  化学计量规定台阶高度','A  Stoichiometry fixes step heights'))
for x,z,lab in [(220,91,'H₂O'),(560,72,'CO'),(810,48,'CO₂')]:a.text(x,z,lab,color=R)
a.text(75,40,L('曲线为构造模型，转变温度并非测量结果','Constructed curve; transition temperatures are not measurements'),fontsize=8)
a=axs[1];a.axis('off');a.set(xlim=(0,1),ylim=(0,1));a.set_title(L('B  从反应式核对每一份质量','B  Account for every portion by reaction'))
for yy,formula,note,c in [(.86,'CaC₂O₄·H₂O',f'{MW:.3f} g/mol',K),(.64,'CaC₂O₄',L(f'失水 {stoich[0]:.3f}%',f'Water loss {stoich[0]:.3f}%'),B),(.42,'CaCO₃',L(f'释放 CO：{stoich[1]:.3f}%',f'CO loss: {stoich[1]:.3f}%'),R),(.20,'CaO',L(f'释放 CO₂：{stoich[2]:.3f}%；余 {stoich[3]:.3f}%',f'CO₂ loss: {stoich[2]:.3f}%; residue {stoich[3]:.3f}%'),Y)]:
 a.text(.06,yy,formula,fontsize=17,color=c,va='center');a.text(.06,yy-.07,note,fontsize=10)
 if yy>.2:a.annotate('',xy=(.82,yy-.14),xytext=(.82,yy),arrowprops={'arrowstyle':'->','color':K})
save(fig,'hydrate-stoichiometry')

Ea=140000.;Af=1e10;Rg=8.314462618
Tk=np.linspace(298.15,923.15,6251);Tc=Tk-273.15;k=Af*np.exp(-Ea/(Rg*Tk))
rates={};metrics={}
for rate in [5,10,20]:
 hazard=cumulative_trapezoid(k/rate,Tk,initial=0);alpha=-np.expm1(-hazard);rates[rate]=alpha
 metrics[str(rate)]={'T5_C':float(np.interp(.05,alpha,Tc)),'peak_C':float(Tc[np.argmax(k*(1-alpha))])}
ti=np.linspace(0,360,721);ki=Af*np.exp(-Ea/(Rg*573.15));ai=-np.expm1(-ki*ti)
csv('kinetics.csv',['temperature_C','conversion_5Kmin','conversion_10Kmin','conversion_20Kmin'],[Tc,rates[5],rates[10],rates[20]])
csv('isothermal.csv',['time_min','conversion_at300C'],[ti,ai])
fig,axs=plt.subplots(1,2,figsize=(12,5),layout='constrained')
a=axs[0]
for rate,c in [(5,B),(10,R),(20,G)]:a.plot(Tc,100*(1-rates[rate]),color=c,lw=2,label=f'{rate} °C/min')
a.set(xlim=(300,520),ylim=(0,105),xlabel=L('温度 / °C','Temperature / °C'),ylabel=L('未反应份额 / %','Unreacted fraction / %'),title=L('A  同一动力学，快扫曲线更靠右','A  Same kinetics; faster ramps shift right'));a.legend(frameon=False)
a=axs[1];a.plot(ti,100*ai,color=B,lw=2);a.scatter([60,360],100*(-np.expm1(-ki*np.array([60,360]))),color=R);a.set(xlabel=L('在 300 °C 保持的时间 / min','Hold time at 300 °C / min'),ylabel=L('转化比例 / %','Converted fraction / %'),title=L('B  较低温度也会累积反应','B  A lower temperature still accumulates reaction'));a.text(15,100*ai[-1]*.73,L('单步一阶构造模型\nA = 10¹⁰ min⁻¹，Eₐ = 140 kJ/mol','Constructed single-step first-order model\nA = 10¹⁰ min⁻¹; Eₐ = 140 kJ/mol'),fontsize=9)
save(fig,'rate-and-hold')

summary={'data_kind':'constructed teaching datasets','seed':720,'initial_mass_mg':m0,
 'dry_plateau_mg':dry,'inert_plateau_mg':inert,'final_plateau_mg':ash,
 'water_loss_percent':float(losses[0]),'pyrolysis_loss_percent':float(losses[1]),'air_loss_percent':float(losses[2]),'residue_percent':float(losses[3]),
 'char_corrected_polymer_percent':float(polymer/m0*100),'char_corrected_added_carbon_percent':float(carbon/m0*100),
 'ideal_dry_basis_residue_percent':2/9.2*100,'hydrate_water_loss_percent':float(stoich[0]),'hydrate_total_mass_percent':float(stoich.sum()),
 'hydrate_formula_mass_g_per_mol':MW,'hydrate_water_number':float((stoich[0]/100)*(MW-waterMW)/(waterMW*(1-stoich[0]/100))),
 'T5_5Kmin_C':metrics['5']['T5_C'],'T5_10Kmin_C':metrics['10']['T5_C'],'T5_20Kmin_C':metrics['20']['T5_C'],
 'isothermal_rate_at300C_per_min':float(ki),'isothermal_60min_conversion_percent':float(-np.expm1(-ki*60)*100),'isothermal_360min_conversion_percent':float(ai[-1]*100),
 'char_ambiguity_upper_y':18/(54+18)}
assert abs(sum(losses)-100)<1e-12
assert abs(polymer-6)<.03 and abs(carbon-1.2)<.03
assert abs(stoich.sum()-100)<1e-12 and abs(summary['hydrate_water_number']-1)<1e-12
assert metrics['5']['T5_C']<metrics['10']['T5_C']<metrics['20']['T5_C']
assert np.all(np.diff(ai)>=0)
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
```

Keep both the time and temperature columns: temperature locates events during a ramp, while time distinguishes successive events during holds and gas switches. Together they describe the complete program.

Inspect the raw trace first, then ask whether the blank changes at the same time. Choose plateau intervals that are sufficiently stable and chemically meaningful before calculating fractions. Averaging several points reduces some random fluctuation, but adjacent points may be correlated and share one loading and baseline error. They are not independent specimens. A comparison between formulations benefits from independently prepared replicates and a description of between-specimen variation. A question about plateau-boundary selection instead calls for changing the integration or averaging intervals and inspecting sensitivity. Keeping these checks distinct shows which uncertainty each addresses. Likewise, derivative smoothing should be varied around a justified setting while the underlying mass account remains visible.

For a water-containing mineral–biopolymer scaffold, a clear analysis can state the initial condition, temperature and gas program, low-temperature loss, pyrolysis residue and post-oxidation residue, followed by the chemical information used for composition conversion. Unknown char yield motivates an appropriate polymer control. Suspected crystallographic water motivates stoichiometric and evolved-gas checks. A processing-stability question motivates holds at relevant residence times. The retained specimen or final residue may also be examined by complementary structural or elemental methods when its identity matters. These choices make each experiment answer a specific unresolved question. TGA then becomes a method for understanding composition, reaction and timescale, rather than a procedure for reporting how much remains after heating.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/T02.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Saito: A New Method of Studying Thermal Decomposition of Substances](https://www.jstage.jst.go.jp/article/pjab1912/2/2/2_2_58/_pdf/-char/en)

   Early continuous-weighing, atmosphere and hold experiments.
2. [Sircar: Composition Analysis of Rubber by Thermogravimetry, TA083](https://www.tainstruments.com/pdf/literature/TA083.pdf)

   Rubber composition, char and carbon-black distinctions.
3. [NETZSCH: TGA Measurements by Means of the BeFlat Correction](https://analyzing-testing.netzsch.com/en-AU/application-literature/tga-measurements-by-means-of-the-beflat-correction/)

   Buoyancy, gas flow and matched blanks.
4. [NETZSCH: TGA Measurements on Calcium Oxalate Monohydrate](https://analyzing-testing.netzsch.com/en/application-literature/tga-measurements-on-calcium-oxalate-monohydrate)

   Sequential calcium oxalate solids and evolved species.
5. [Suzanne et al.: A Round-Robin Study on Decomposition of Calcium Oxalate Monohydrate by Thermogravimetry](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=935144)

   Loading, pans, onset definitions and interlaboratory comparison.
6. [NETZSCH Kinetics Neo: Master Plot Verification](https://kinetics.netzsch.com/en/learn/master-plot)

   Arrhenius form and conditions for single-step interpretation.
7. [NETZSCH Kinetics Neo: Conversion for Incomplete Measured Data](https://kinetics.netzsch.com/en/learn/how-to-calculate-conversion-for-incomplete-measured-data)

   Conversion and complete mass-change definitions.
8. [TA Instruments: High Resolution Thermogravimetric Analysis, TA023](https://www.tainstruments.com/pdf/literature/TA023.pdf)

   Loading, rate and holds affecting event separation.
