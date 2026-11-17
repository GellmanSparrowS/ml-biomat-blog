# DSC: What happens when materials absorb and release heat

Source: https://ml-biomat.com/tutorials/experimental-methods/t01/en/
Language: en

Read steps and peaks in heat flow, connecting thermal history and scan rate with molecular structure.

## Why does a plastic soften, and why does a protein unfold?

Chocolate loses its shape in a warm hand. A transparent plastic sheet may become easier to bend before undergoing a more obvious change in shape. A heated protein solution may recover its function after cooling, or it may leave aggregates that do not readily return to their original state. All these events involve energy and molecular motion, but they are different processes. Differential scanning calorimetry, or DSC, observes heat absorbed or released while temperature follows a controlled program. It helps identify the temperature range of a change, the associated heat and the effects of processing or storage history.

For polymers, DSC is widely used to compare crystallinity, glass transitions, melting and curing. A biodegradable scaffold subjected to different cooling conditions can retain the same chemical composition while developing different chain arrangements, with consequences for mechanical behavior and water access. For biological macromolecules, thermal scans can reveal transitions in proteins, nucleic acids and lipids, allowing comparisons among buffers and formulations. The useful question is broader than finding a single heat-resistance temperature: which processes occur along the selected temperature path, and how do they relate to the material's intended use?

Heating water offers a starting analogy. Raising a larger quantity of water through the same temperature interval takes more energy. Once boiling occurs, additional energy can instead support a change of state. DSC likewise separates energy needed for temperature change from energy associated with a transition, but uses a small specimen, a controlled program and comparison with a reference. The height of a baseline, a step and a peak therefore carry different information. Calling every feature a melting peak would discard much of what the experiment can reveal.

We first connect the instrument to its heat-flow signal, then analyze a clearly constructed polymer-composite example involving a glass transition, peak integration and mass normalization. Heating-rate effects are compared with published indium calibration results that retain their reported uncertainty intervals. Finally, protein unfolding shows why a similar-looking endotherm can require different preparation and interpretation. Throughout the chapter, each curve feature is connected to a specific energy contribution rather than treated as a shape to label.

## How two small containers reveal a heat difference

Differential refers to comparison between sample and reference, scanning to a programmed temperature change, and calorimetry to measuring heat exchange. In many solid-material experiments, a specimen is placed in a small pan and compared with a matched empty pan. Both follow the same temperature program, but the sample side adds the material's heat capacity and transition heat. Comparing their heat requirements reduces common contributions from containers and the instrument. Solution calorimeters used for proteins often employ liquid cells with a matched buffer reference; the measurement logic is related, while construction and sensitivity are adapted to the specimen.

A 1962 patent filed by Watson and O'Neill described a clear control principle for differential microcalorimetry. One feedback loop made the average sample and reference temperature follow a program, while another adjusted the difference in applied power to keep their temperatures nearly equal. Recording that power difference connected compensation for the sample's thermal behavior with a quantitative signal. This history clarifies why measuring a temperature difference and measuring the power needed to remove a temperature difference are distinct operations. It also explains the connection between an integrated power signal and transition energy.

![Original principle diagrams. A connects to Watson and O’Neill’s power-compensation patent filed in 1962; B shows the alternative heat-flux measurement chain. Not to scale; no patent figure reproduced.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/02ca3acbd5b44f8ae7a25363.svg?v=02ca3acbd5b4)

Figure 1Original principle diagrams. A connects to Watson and O’Neill’s power-compensation patent filed in 1962; B shows the alternative heat-flux measurement chain. Not to scale; no patent figure reproduced.

Heat-flux DSC uses another common implementation. Sample and reference exchange heat with a shared source through characterized thermal paths. Sensors measure a temperature difference, which calibration converts into differential heat flow. Both heat-flux and power-compensation instruments require appropriate temperature calibration, heat-flow or enthalpy calibration and baseline treatment. The two original diagrams distinguish these principles rather than combining all instruments into a single imagined design. Before calculating anything, establish whether the exported ordinate is milliwatts, watts per gram or an already converted heat-capacity quantity.

Heat flow is energy transferred per unit time. This chapter plots endothermic, heat-absorbing events upward and exothermic events downward; other software can use the opposite convention. A 5 mg sample with a specific heat of 1.5 joules per gram per kelvin requires approximately 1.25 milliwatts simply to follow a heating rate of 10 kelvin per minute. That background exists even without melting, crystallization or chemical reaction. Additional thermal events appear on top of it, creating the features that analysis must distinguish.

$$
\dot Q_{\mathrm{base}}=m c_p\beta,\qquad \beta=\frac{dT}{dt}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8988d245a3957f245c21d13b.svg) | Sample heating heat flow without transition heat, watts. |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Specimen mass, grams. |
| ![Formula](https://ml-biomat.com/static/agent-math/3dd37e60d36899a1d25331ba.svg) | Specific heat capacity at constant pressure, J/(g·K). |
| ![Formula](https://ml-biomat.com/static/agent-math/f27acf6959fc15846a7239da.svg) | Heating rate, K/s; Celsius and kelvin intervals have equal magnitude. |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | Temperature; differences may be expressed in K or °C. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time, seconds. |

Energy per gram per degree multiplied by mass and degrees per second gives energy per second. m=0.005 g, cp=1.5 J/(g·K) and β=10/60 K/s give 0.00125 W, or 1.25 mW. This is the approximately uniform-temperature background without transition heat.

Specific heat is heat capacity per unit mass. Multiplying it by specimen mass gives the heat capacity of the specimen. Celsius and kelvin temperature intervals have the same numerical size, so 10 degrees Celsius per minute and 10 kelvin per minute describe the same ramp. Thermodynamic relationships involving absolute temperature, however, require kelvin. Another useful distinction separates programmed furnace temperature from actual sample temperature. Heat transfer among source, pan, specimen and sensor takes time, and the corresponding lag becomes increasingly relevant as the program changes faster.

## Steps and peaks tell different molecular stories

A polymer can contain relatively ordered crystalline regions and amorphous regions lacking long-range regular arrangement. The glass transition mainly concerns segmental motion in the amorphous material. At low temperature, some collective local rearrangements are too slow to occur on the observation time scale. Heating allows those motions to respond, often changing stiffness and specific heat. In DSC, the result commonly appears as a baseline step. This is different from all molecules changing from solid to liquid at once, which is why a glass-transition temperature should be associated with the measurement time scale and analysis definition.

The example represents the glass transition with a smooth step centered at 60 degrees Celsius and a specific-heat increase of 0.35 joules per gram per kelvin. We explicitly report the step midpoint. Other procedures use an extrapolated onset, an inflection point or another defined criterion, and the resulting temperatures need not be identical. Storage in a glassy state can produce enthalpic relaxation, followed by an additional recovery endotherm near the step during reheating. Such a feature reflects thermal history and does not automatically identify a small population of melting crystals.

Melting destroys crystalline order and absorbs heat, whereas crystallization usually releases heat as more ordered arrangements develop. Some polymers cool so quickly that chains cannot organize extensively. During subsequent heating, they acquire enough mobility to crystallize before reaching their melting range. This exothermic event is called cold crystallization even though the instrument is heating. Integrating only the later melting peak counts crystals present initially together with crystals formed during the scan. The distinction matters whenever the research question concerns the specimen's starting structure.

Peak position, onset and area serve different purposes. The peak temperature marks the strongest heat-flow feature under the selected conditions. An extrapolated onset describes a geometrically defined beginning. The area accumulates energy. Distributions of crystal size, crystal perfection and rearrangement can broaden polymer melting or produce shoulders. Two apparent peaks can also involve recrystallization followed by remelting rather than two chemical components. Comparisons of cooling history, heating rate and independent structural measurements help distinguish these possibilities more effectively than assigning a chemical name to every shoulder.

Biological samples introduce further mechanisms. Protein unfolding changes internal contacts and interactions with solvent, potentially generating a strong endotherm. Lipid membranes can undergo transitions in chain ordering. These events share heat exchange with polymer melting but not necessarily its molecular mechanism. DSC provides a common energetic measurement while the sample and its history determine the appropriate structural question. A productive interpretation first identifies the thermal contribution and then connects it with evidence about the molecular process.

## The specimen's past and the scan speed both enter the result

Before a piece of material reaches the pan, it has already experienced processing, cooling, deformation, storage and possibly water uptake. The first heating scan retains effects of that history and is useful for asking what state the received specimen occupies. Melting a suitable material, cooling it through a common program and reheating can instead compare behavior after a specified shared history. The second scan answers a different question rather than automatically providing a more authentic result. If heating causes degradation, crosslinking or another irreversible chemical change, even the composition can differ between scans.

Weighing determines normalization, while specimen geometry influences heat transfer. The portion loaded should represent the material being compared, and its recorded mass should correspond to what actually enters the instrument. Appropriate contact between a thin specimen and the pan improves thermal coupling; thick or irregular packing can introduce temperature gradients. Pan material, lid, sealing and atmosphere should suit the event of interest. Volatile components introduce mass escape and pressure considerations, oxidation studies require defined gas conditions, and hygroscopic samples require a meaningful moisture state. Matching sample and reference pans also affects startup behavior and the baseline.

Temperature and heat scales require separate calibration relationships. A reference transition temperature checks the temperature axis. Known transition enthalpy, accurate reference mass and a defined integration procedure check the energy scale. Indium is commonly used for these purposes. The published NIST data below show estimates at several nominal heating rates. The plotted values are Table 4 posterior means and 95% credible intervals from the report's model. The 28.58 joules per gram value at zero rate is an extrapolated equilibrium estimate, not a melting scan conducted without raising temperature.

![A is a constructed 8-second first-order thermal response with complete transition heat about 45 J/g. B redraws public values from Fortin et al., NIST SP 260-242, Table 4: posterior means and reported 95% credible bounds. Zero rate is an extrapolation. NIST government research data, credited with original values retained.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/1d088b70794ab063ce1a3265.svg?v=1d088b70794a)

Figure 2A is a constructed 8-second first-order thermal response with complete transition heat about 45 J/g. B redraws public values from Fortin et al., NIST SP 260-242, Table 4: posterior means and reported 95% credible bounds. Zero rate is an extrapolation. NIST government research data, credited with original values retained.

The lag diagnostic deliberately preserves the total energy of an isolated event when its entire response is integrated. Delayed heat is redistributed in time rather than removed. A narrow integration window can nevertheless miss the delayed tail and produce a smaller area, especially for a faster scan. This distinction suggests a practical check: compare the complete response over a sufficiently broad interval before interpreting a reduced area as a change in material composition. Conversely, broadening the window indefinitely can include another transition or an increasingly uncertain background. An appropriate interval is supported by the return to a defensible baseline and by knowledge of nearby processes. Plotting the chosen boundaries with the curve makes that judgment inspectable. In the example, all three rate curves are integrated over the same broad temperature range, which extends well beyond the end of the delayed response.

Heating rate changes how much time the specimen spends in each temperature interval. Faster scanning often produces a larger heat-flow peak because energy is exchanged over a shorter time. It can also make thermal response lag more visible. Our constructed diagnostic applies an eight-second first-order response to a melting event with an integrated heat of 45 joules per gram. At 5, 10 and 20 degrees Celsius per minute, peak temperatures are approximately 165.65, 166.25 and 167.25 degrees Celsius. The peak positions differ while complete integration remains close to 45 joules per gram. Real materials can additionally change their crystallization or reaction pathway with scan rate.

Start comparisons with common conditions, then vary factors that test a specific explanation. Smaller specimens and slower ramps investigate thermal lag. Defined cooling programs investigate crystallization history. Unexpected endotherms invite checks of moisture and specimen mass before and after the experiment. Preserve the full traces rather than retaining only automatically assigned temperatures. This allows the effects of thermal history, transfer and molecular transformation to be examined against the actual sequence of measurements.

## From milliwatts to heat per gram and crystalline fraction

The polymer example uses a hypothetical 5 mg composite containing a polymer mass fraction of 0.8 and an inert filler fraction of 0.2. Heating proceeds from 20 to 200 degrees Celsius at 10 degrees per minute. The constructed signal includes a glass-transition step near 60 degrees, a cold-crystallization exotherm near 110 degrees and a melting endotherm near 165 degrees. Input cold-crystallization and melting heats are 20 and 45 joules per gram of the whole composite, respectively. The values explain analysis and do not describe a measured commercial polymer.

![Constructed hypothetical composite, seed 710, mass 5 mg, heating rate 10 °C/min and polymer mass fraction 0.8. Endothermic is upward. A retains specific-heat background; B fits the glass-step midpoint; C marks integration regions; D distinguishes normalization bases.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/03a6ddd2bb2116d2917e902d.svg?v=03a6ddd2bb21)

Figure 3Constructed hypothetical composite, seed 710, mass 5 mg, heating rate 10 °C/min and polymer mass fraction 0.8. Endothermic is upward. A retains specific-heat background; B fits the glass-step midpoint; C marks integration regions; D distinguishes normalization bases.

The program first subtracts the constructed instrument background. A local fit around the glass transition recovers a midpoint of approximately 60.005 degrees Celsius and a specific-heat step of 0.3505 joules per gram per kelvin. At higher temperatures, selected sidebands define a linear baseline, and the cold-crystallization and melting regions are integrated separately. Because the horizontal axis is temperature, the initial area has units of power times temperature. Dividing by heating rate converts the temperature interval into elapsed time; power integrated over time becomes energy. Division by specimen mass then produces a specific enthalpy.

$$
\Delta h=\frac{1}{m}\int_{t_a}^{t_b}[\dot Q(t)-\dot Q_0(t)]\,dt=\frac{1}{m\beta}\int_{T_a}^{T_b}[\dot Q(T)-\dot Q_0(T)]\,dT
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a7f92a6abd1defda3a545b43.svg) | Transition enthalpy normalized by specimen mass, J/g. |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Specimen mass used for normalization, grams. |
| ![Formula](https://ml-biomat.com/static/agent-math/cee984b0ecbc9ab32f893bae.svg) | Sample heat flow after instrument-background correction, watts. |
| ![Formula](https://ml-biomat.com/static/agent-math/fd724bd870304f04c8bb030e.svg) | Estimated specimen baseline without the transition, watts. |
| ![Formula](https://ml-biomat.com/static/agent-math/7409c350063c63e2d0b0ffa5.svg) | Time and integration limits, seconds. |
| ![Formula](https://ml-biomat.com/static/agent-math/536ddb365f804465fe425907.svg) | Temperature and corresponding limits, °C or K with consistent interval units. |
| ![Formula](https://ml-biomat.com/static/agent-math/f27acf6959fc15846a7239da.svg) | Constant heating rate, K/s. |

Power integrated over time gives heat; under a constant ramp dt=dT/β. An endothermic area of 0.0375 W·K, m=0.005 g and β=1/6 K/s gives 45 J/g. Convert minutes or milliwatts consistently before applying the expression.

The numerical results are approximately 45.03 joules per gram for melting and 19.74 for cold crystallization. Differences from the input values arise from noise, finite integration windows and peak tails influencing the selected baseline bands. A baseline estimates the heat flow that would remain without the transition. Moving it by only 0.01 milliwatt across a 40-degree integration interval changes enthalpy by 0.48 joules per gram under the example's mass and rate conditions. That scale can be more informative than visual agreement when comparing small differences between specimens.

Initial crystallinity requires two further definitions. Melting consumes heat associated with crystals present initially and those formed during heating, so an appropriate initial-crystallinity estimate subtracts the positive magnitude of cold-crystallization heat. Also, the measured peak areas here are normalized by total composite mass, while the desired crystalline fraction refers to the polymer component. Dividing by polymer mass fraction converts the denominator accordingly. This mass balance assumes that filler contributes no overlapping transition, the relevant events can be separated and the reference fusion enthalpy suits the polymer and crystal form.

$$
X_c=\frac{\Delta h_m-\Delta h_{cc}}{w_p\Delta h_m^\circ}\times100\%
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9452df3acfb36a01b9d75cca.svg) | Initial crystalline mass fraction within the polymer component, percent. |
| ![Formula](https://ml-biomat.com/static/agent-math/45af6b60faf81f9352c1a2a6.svg) | Positive melting heat per total composite mass, J/g specimen. |
| ![Formula](https://ml-biomat.com/static/agent-math/428a3c64b2d849b0d41d859f.svg) | Positive magnitude of cold-crystallization exotherm, J/g specimen. |
| ![Formula](https://ml-biomat.com/static/agent-math/59c3b11c729fa3704eef4875.svg) | Polymer mass fraction in the specimen, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/37c105232a9ed6408e184706.svg) | Fully crystalline reference fusion enthalpy appropriate to polymer and crystal form, J/g polymer. |

Subtract the heat associated with crystals formed during the scan, then divide by the polymer mass fraction and the heat of fusion of the crystalline reference. Hypothetical melting and cold-crystallization heats of 45 and 20 J/g of specimen, a polymer mass fraction of 0.8 and a reference value of 100 J/g of polymer give an initial crystallinity of 31.25%. This calculation assumes separable events, no overlapping filler transition and a suitable crystalline reference.

There are two separate baseline questions in this calculation. The instrument blank describes an offset associated with the measurement system and containers. The transition baseline describes the sample's heat capacity in the absence of the event being integrated. Removing the former does not remove the latter. In the constructed example, heat capacity is nearly linear across the higher-temperature sidebands, so a linear local estimate is useful. A specimen whose heat capacity changes across melting can require a different baseline construction. Comparing plausible baselines and reporting how much the integral changes connects the numerical sensitivity to the physical assumption being made.

For clarity, the hypothetical fully crystalline reference polymer is assigned a fusion enthalpy of 100 joules per gram of polymer. Using ideal inputs, 45 minus 20 gives 25 joules per gram of composite associated with initial crystals. Dividing by 0.8 gives 31.25 joules per gram of polymer, and comparison with the reference gives 31.25% initial polymer crystallinity. The actual processing result is approximately 31.62%. The three bars compare melting alone, subtraction of cold crystallization and polymer-mass normalization. Each change corresponds to a specific physical definition rather than a cosmetic correction.

The interactive experiment changes specimen mass, heating rate and baseline offset while keeping ideal specific melting heat constant. A larger specimen or faster ramp produces a taller milliwatt peak. Correct conversion by mass and rate returns approximately the same heat per gram. Introducing a small baseline offset reveals how one instrumental discrepancy affects different specimen masses and scan rates differently. The exercise separates a visually large peak from a large energy requirement per unit material.

## Does a taller peak mean more heat per gram?

The fusion enthalpy is fixed at 45 J/g, the peak center at 165 °C and the width parameter at 5 °C. Integration covers 145–185 °C. Change mass and rate, then the estimated-baseline offset from the true baseline; a positive offset means the baseline estimate is too high.

[Figure: Effects of mass, rate and baseline on heat flow and integration](https://ml-biomat.com/tutorials/experimental-methods/t01/en/#T01-plot)

## Connecting a protein endotherm with the unfolded population

In protein-solution measurements, solvent heat capacity greatly exceeds the small differential contribution from protein. Matching the sample and reference buffers is therefore especially important. Final dialysis buffer or a suitable chromatography flow-through can help produce an appropriate reference. Protein concentration, effective cell volume and molecular mass determine conversion from total heat to enthalpy per mole of protein. Adsorption, precipitation or aggregation can alter the molecular population participating in the scan. Observations of solution state, repeat scans and post-scan behavior provide useful context for the thermal trace.

Consider a reversible two-state equilibrium in which each protein is folded or unfolded. For this teaching model, unfolding enthalpy is approximately constant over the temperature range and the heat-capacity difference between states is set to zero. The unfolded fraction rises with temperature and equals one half at a midpoint of 60 degrees Celsius. The model makes a direct connection between a changing molecular population and excess heat capacity. A real protein can contain several domains, intermediate states or aggregation pathways, which call for descriptions informed by the observed behavior.

$$
K(T)=\exp\!\left[-\frac{\Delta H}{R}\left(\frac{1}{T}-\frac{1}{T_m}\right)\right],\qquad f_U(T)=\frac{K(T)}{1+K(T)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5287b9b7382426f155625e11.svg) | Equilibrium unfolded-to-folded population ratio, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | Absolute temperature, kelvin. |
| ![Formula](https://ml-biomat.com/static/agent-math/661ecf63746c81514ad169cb.svg) | Approximately constant molar unfolding enthalpy in the model, J/mol. |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | Gas constant, 8.314462618 J/(mol·K). |
| ![Formula](https://ml-biomat.com/static/agent-math/d02c1a55a2052315ebe68af2.svg) | Model midpoint temperature with equal populations, kelvin. |
| ![Formula](https://ml-biomat.com/static/agent-math/38d847ee4f90227f3c1be623.svg) | Fraction of molecules unfolded, dimensionless. |

Reversible equilibrium two-state model with constant enthalpy and zero heat-capacity difference. Integrating the van’t Hoff relation relative to the midpoint gives the population ratio. At T=Tm=333.15 K, K=1 and unfolded fraction=0.5. Aggregation and intermediates are separate processes.

When a small temperature increase causes some molecules to unfold, the calorimeter must provide their additional unfolding heat. The region where unfolded fraction changes rapidly therefore produces an excess heat-capacity peak. Integrating that heat capacity over temperature accumulates transition heat. The model assigns an unfolding enthalpy of 200 kilojoules per mole. Integration from 20 to 100 degrees Celsius gives about 199.90 kilojoules per mole, slightly below the full value because the finite temperature limits retain very small deviations from the completely folded and unfolded limits.

$$
C_{p,\mathrm{ex}}=\Delta H\frac{df_U}{dT}=\frac{\Delta H^2}{RT^2}f_U(1-f_U),\qquad \Delta H_{\mathrm{cal}}=\int_{T_a}^{T_b}C_{p,\mathrm{ex}}\,dT
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/496ef11b49251e78d3f0c9e2.svg) | Excess molar heat capacity after state-baseline subtraction, J/(mol·K). |
| ![Formula](https://ml-biomat.com/static/agent-math/661ecf63746c81514ad169cb.svg) | Molar unfolding enthalpy in the two-state model, J/mol. |
| ![Formula](https://ml-biomat.com/static/agent-math/9fd90fe44c80ea5fc0ca6d2e.svg) | Unfolded fraction, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/536ddb365f804465fe425907.svg) | Absolute temperature and integration limits, kelvin. |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | Gas constant, J/(mol·K). |
| ![Formula](https://ml-biomat.com/static/agent-math/7fbff5e5f098490dbfa519f3.svg) | Calorimetric enthalpy integrated over the selected range, J/mol. |

The increase in unfolded fraction per degree, multiplied by the molar unfolding enthalpy, gives the excess heat capacity. An unfolding enthalpy of 200000 J/mol, a midpoint of 333.15 K and an unfolded fraction of 0.5 give about 10.84 kJ/(mol·K) at the midpoint. Integration from 20 to 100 °C gives about 199.90 kJ/mol; the finite interval excludes the small tails outside those temperatures.

![Constructed reversible two-state protein model, midpoint 333.15 K, unfolding enthalpy 200 kJ/mol and zero heat-capacity difference between states. The dashed rescan merely illustrates 20% population recovery, not a particular aggregation mechanism.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/00a728d0a8927803a44ea7f2.svg?v=00a728d0a892)

Figure 4Constructed reversible two-state protein model, midpoint 333.15 K, unfolding enthalpy 200 kJ/mol and zero heat-capacity difference between states. The dashed rescan merely illustrates 20% population recovery, not a particular aggregation mechanism.

Rescanning connects an event during heating with recovery during cooling. If the sample returns sufficiently to its starting state, a repeat scan can show a similar transition heat. Partial recovery can reduce the area. The dashed curve illustrates a specimen with only 20% of molecules recovered, without claiming a specific aggregation mechanism. Similar rescans support recovery, while scan-rate and concentration comparisons help assess whether the equilibrium description is appropriate. A process can be reproducible yet still lag behind equilibrium during a rapid temperature program.

Read peak position together with area, width and recovery. A buffer change may raise a transition temperature while changing other features, each describing another aspect of behavior. Formulation research also considers long-term change at the intended storage temperature, activity retention and aggregation kinetics. A peak temperature from one heating experiment is therefore connected to a defined thermal path, whereas shelf-life requires observations of the relevant processes over time. Combining DSC with structural, activity and particle-size measurements makes the formulation comparison more informative.

## Use the complete calculation to design a comparison

The complete program produces four figure groups, point-by-point polymer scan data, peak temperatures and integrated heat at several rates, plus protein unfolded fractions and excess heat capacities. The indium table accompanies the example and is read directly to redraw the published estimates and intervals. Constructed teaching data and published statistical results are explicitly distinguished. The former isolate variables and test calculations; the latter show how actual metrology research reports rate effects and uncertainty. All data needed for execution are bundled, so the analysis can run offline.

### Complete heat-flow, crystallinity and protein-unfolding analysis

Performs baseline treatment, step fitting, integration and mass normalization; compares scan rates with published indium estimates and exports figures and pointwise results.

```
"""DSC: constructed heat-flow analysis plus published NIST indium estimates."""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.special import expit
from scipy.optimize import curve_fit
from scipy.signal import lfilter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle

def gaussian(x,center,width):return np.exp(-.5*((x-center)/width)**2)/(width*np.sqrt(2*np.pi))
def cp_model(t,a,b,step,tg,width):return a+b*(t-20)+step*expit((t-tg)/width)
def lagged_peak(t,rate,mass_mg=5,heat=45,tau=8):
 beta=rate/60;ideal=mass_mg*beta*heat*gaussian(t,165,5);alpha=np.exp(-(t[1]-t[0])/beta/tau);return ideal,lfilter([1-alpha],[1,-alpha],ideal)
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True);T=lambda z,e:z if a.language=='zh' else e
 plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.titlesize':12,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fcfbf7','axes.facecolor':'#fcfbf7','savefig.facecolor':'#fcfbf7'})
 B,R,G,Y='#167d9a','#d35f47','#37967d','#c49b35'
 def save(f,n):f.savefig(a.output/f'{n}-{a.language}.svg');f.savefig(a.output/f'{n}-{a.language}.png',dpi=145);plt.close(f)
 t=np.linspace(20,200,3601);mass=.005;beta=10/60;cp=cp_model(t,1.2,.002,.35,60,1.5);instrument=.03+.0001*t;baseline=1000*mass*beta*cp;cc=-20*gaussian(t,110,7);melt=45*gaussian(t,165,5);rng=np.random.default_rng(710);raw=instrument+baseline+1000*mass*beta*(cc+melt)+rng.normal(0,.002,len(t));corrected=raw-instrument
 mask=(t>=40)&(t<=80);params,_=curve_fit(cp_model,t[mask],corrected[mask]/(1000*mass*beta),p0=[1.2,.002,.35,60,1.5]);estimated_cp=cp_model(t,*params)
 # Local baselines use transition-free sidebands. The ideal heat-capacity trend is linear well above Tg.
 side=((t>=85)&(t<=90))|((t>=132)&(t<=138))|((t>=140)&(t<=145))|((t>=185)&(t<=195));poly=np.polyfit(t[side],corrected[side],1);local=np.polyval(poly,t);excess=corrected-local
 mcc=(t>=90)&(t<=132);mm=(t>=145)&(t<=185);hcc=-np.trapezoid(excess[mcc],t[mcc])/(1000*mass*beta);hm=np.trapezoid(excess[mm],t[mm])/(1000*mass*beta);xc=(hm-hcc)/(.8*100)*100
 f,axes=plt.subplots(1,2,figsize=(13.7,5.4),layout='constrained')
 for ax in axes:ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off')
 ax=axes[0];ax.set_title(T('A  1962：分别调节功率，保持两侧等温','A  1962: Adjust power to equalize temperatures'),loc='left');ax.add_patch(Rectangle((.7,1.8),8.6,5,fc='#edf0ee',ec='#7e929d'))
 for x,label,col in [(1.5,T('样品','Sample'),R),(6,T('参比','Reference'),B)]:
  ax.add_patch(Rectangle((x,4),2.5,1.3,fc='#e0e7e8',ec=col));ax.text(x+1.25,4.65,label,ha='center');ax.plot([x+.2,x+.6,x+1,x+1.4,x+1.8,x+2.2],[3,3.5,3,3.5,3,3.5],c=col,lw=2);ax.annotate('',xy=(x+1.25,4),xytext=(x+1.25,3.55),arrowprops={'arrowstyle':'->','color':col});ax.text(x+1.25,2.4,T('独立加热器','Separate heater'),ha='center',fontsize=10)
 ax.text(5,6.1,T('温度反馈 → 差分功率','Temperature feedback → differential power'),ha='center',fontsize=11);ax.text(5,.6,T('Watson 与 O’Neill 的功率补偿思想\n原创原理图，非专利图复制','Watson and O’Neill: power-compensation concept\nOriginal schematic, not a patent-figure reproduction'),ha='center',fontsize=10)
 ax=axes[1];ax.set_title(T('B  另一种实现：共同热源与热流通路','B  Another implementation: shared source and heat paths'),loc='left');ax.add_patch(Rectangle((1,1.8),8,1,fc='#ead4ba',ec=Y));ax.text(5,2.3,T('受程序控制的热源','Programmed heat source'),ha='center')
 for x,label,col in [(1.5,T('样品','Sample'),R),(6,T('参比','Reference'),B)]:
  ax.add_patch(Rectangle((x,4.2),2.5,1.3,fc='#e0e7e8',ec=col));ax.text(x+1.25,4.85,label,ha='center');ax.annotate('',xy=(x+1.25,4.2),xytext=(x+1.25,2.9),arrowprops={'arrowstyle':'->','color':col,'lw':3})
 ax.text(5,6.4,T('测量温差，经标定得到热流差','Measure temperature difference; calibrate to heat flow'),ha='center',fontsize=10);ax.text(5,.6,T('热流型 DSC：原理示意，尺寸不按比例','Heat-flux DSC: principle schematic, not to scale'),ha='center',fontsize=10);save(f,'instrument-history')
 f,axes=plt.subplots(2,2,figsize=(13.7,8.4),layout='constrained');ax=axes[0,0];ax.plot(t,raw,c=B,label=T('原始构造信号','Constructed raw signal'));ax.plot(t,baseline+instrument,c='#6b7f8a',ls='--',label=T('无转变热的基线','Baseline without transition heat'));ax.set(xlabel=T('温度 / °C','Temperature / °C'),ylabel=T('热流 / mW；吸热向上','Heat flow / mW; endothermic up'),title=T('A  台阶、放热峰与吸热峰','A  Step, exotherm and endotherm'));ax.legend(fontsize=9)
 ax=axes[0,1];ax.scatter(t[mask][::8],corrected[mask][::8]/(1000*mass*beta),s=8,c=Y,label=T('表观比热','Apparent specific heat'));ax.plot(t[mask],estimated_cp[mask],c=B,label=T('台阶拟合','Step fit'));ax.axvline(params[3],c=R,ls='--');ax.set(xlabel=T('温度 / °C','Temperature / °C'),ylabel=T('比热 / J/(g·K)','Specific heat / J/(g·K)'),title=T(f'B  玻璃化台阶中点 {params[3]:.2f} °C',f'B  Glass-step midpoint {params[3]:.2f} °C'));ax.legend(fontsize=9)
 ax=axes[1,0];ax.plot(t,excess,c=B);ax.fill_between(t,0,excess,where=mcc,color=G,alpha=.3,label=T(f'冷结晶 {hcc:.2f} J/g',f'Cold crystallization {hcc:.2f} J/g'));ax.fill_between(t,0,excess,where=mm,color=R,alpha=.3,label=T(f'熔融 {hm:.2f} J/g',f'Melting {hm:.2f} J/g'));ax.set(xlim=(80,195),xlabel=T('温度 / °C','Temperature / °C'),ylabel=T('扣基线热流 / mW','Baseline-subtracted heat flow / mW'),title=T('C  积分面积需除以升温速率','C  Temperature-axis area needs the heating rate'));ax.legend(fontsize=9)
 ax=axes[1,1];labels=[T('熔融直接比值','Melting alone'),T('扣冷结晶，样品基准','Subtract cold\ncrystallization'),T('再按聚合物质量归一','Polymer-mass\nnormalization')];vals=[hm/100*100,(hm-hcc)/100*100,xc];ax.bar(range(3),vals,color=[R,Y,B],width=.58);ax.set_xticks(range(3),labels,fontsize=9);ax.set(ylabel=T('计算结果 / %','Calculated result / %'),ylim=(0,65),title=T('D  分母改变，物理含义也改变','D  The denominator changes the meaning'))
 for i,v in enumerate(vals):ax.text(i,v+1,f'{v:.2f}%',ha='center',fontsize=10)
 save(f,'heat-flow-analysis')
 nist=np.genfromtxt(Path(__file__).parent/'data/nist_indium_table4.csv',delimiter=',',names=True);f,axes=plt.subplots(1,2,figsize=(13.7,5.5),layout='constrained');rate_rows=[]
 for rate,col in [(5,G),(10,B),(20,R)]:
  ideal,measured=lagged_peak(t,rate);peak=float(t[np.argmax(measured)]);heat=float(np.trapezoid(measured,t)/(1000*mass*(rate/60)));rate_rows.append([rate,peak,heat]);axes[0].plot(t,measured,c=col,label=T(f'{rate} °C/min；峰 {peak:.2f} °C',f'{rate} °C/min; peak {peak:.2f} °C'))
 axes[0].set(xlim=(145,190),xlabel=T('程序温度 / °C','Program temperature / °C'),ylabel=T('转变热流 / mW','Transition heat flow / mW'),title=T('A  构造模型：8 s 热响应滞后','A  Constructed model: 8-second thermal response'));axes[0].legend(fontsize=9)
 ax=axes[1];mean=nist['posterior_mean_J_per_g'];ax.errorbar(nist['heating_rate_C_per_min'],mean,yerr=[mean-nist['lower95_J_per_g'],nist['upper95_J_per_g']-mean],fmt='o',color=B,capsize=4);ax.axhline(28.58,c=G,ls=':',label=T('零速率外推 28.58 J/g','Zero-rate extrapolation: 28.58 J/g'));ax.set(xlabel=T('名义升温速率 / °C/min','Nominal heating rate / °C/min'),ylabel=T('熔融焓估计 / J/g','Estimated fusion enthalpy / J/g'),title=T('B  真实公开结果：NIST 铟标准物质','B  Published results: NIST indium reference material'));ax.legend(fontsize=9,loc='upper left');ax.text(.25,.05,T('表 4 后验均值与 95% 可信区间\n不是五条原始扫描的峰面积','Table 4 posterior means and 95% credible intervals\nNot peak areas from five individual scans'),transform=ax.transAxes,fontsize=9);save(f,'scan-rate-calibration')
 pt=np.linspace(20,100,1601);kel=pt+273.15;H=200000.;Tm=333.15;gas=8.31446261815324;frac=expit(-H/gas*(1/kel-1/Tm));cex=H**2/(gas*kel**2)*frac*(1-frac)/1000;integral=np.trapezoid(cex,pt)
 f,axes=plt.subplots(1,2,figsize=(13.7,5.4),layout='constrained');ax=axes[0];ax.plot(pt,frac,c=B,label=T('展开比例','Unfolded fraction'));ax.axvline(60,c='#71818b',ls=':');ax.axhline(.5,c='#71818b',ls=':');ax.set(xlabel=T('温度 / °C','Temperature / °C'),ylabel=T('展开分子比例','Fraction unfolded'),title=T('A  构造的可逆两态平衡','A  Constructed reversible two-state equilibrium'));ax.legend(fontsize=10)
 ax=axes[1];ax.plot(pt,cex,c=R,label=T('首次扫描 / 完全恢复后的复扫','First scan / rescan after full recovery'));ax.plot(pt,.2*cex,c=B,ls='--',label=T('仅 20% 分子恢复的复扫示意','Illustrative rescan with only 20% recovered'));ax.fill_between(pt,0,cex,color=R,alpha=.1);ax.set(xlabel=T('温度 / °C','Temperature / °C'),ylabel=T('过量摩尔热容 / kJ/(mol·K)','Excess molar heat capacity / kJ/(mol·K)'),title=T('B  面积计热，复扫考察恢复','B  Area measures heat; rescanning probes recovery'));ax.legend(fontsize=8);ax.text(.04,.65,T(f'20–100 °C 积分：{integral:.2f} kJ/mol\n参数 ΔH=200 kJ/mol；ΔCp=0',f'Integral, 20–100 °C: {integral:.2f} kJ/mol\nModel ΔH=200 kJ/mol; ΔCp=0'),transform=ax.transAxes,fontsize=9);save(f,'protein-unfolding')
 np.savetxt(a.output/'polymer_scan.csv',np.c_[t,(t-20)/beta,raw,instrument,corrected,baseline,local,excess],delimiter=',',header='temperature_C,time_s,raw_mW,instrument_mW,corrected_mW,true_cp_baseline_mW,fitted_local_baseline_mW,excess_mW',comments='');np.savetxt(a.output/'scan_rate.csv',rate_rows,delimiter=',',header='rate_C_per_min,peak_temperature_C,integrated_heat_J_per_g',comments='');np.savetxt(a.output/'protein.csv',np.c_[pt,frac,cex,.2*cex],delimiter=',',header='temperature_C,unfolded_fraction,excess_Cp_kJ_per_mol_K,rescan20percent_kJ_per_mol_K',comments='')
 summary={'glass_midpoint_C':float(params[3]),'specific_heat_step_J_per_g_K':float(params[2]),'melting_heat_J_per_g_sample':float(hm),'cold_crystallization_heat_J_per_g_sample':float(hcc),'initial_polymer_crystallinity_percent':float(xc),'ideal_initial_polymer_crystallinity_percent':31.25,'baseline_offset_heat_error_J_per_g':.01/1000*40/beta/mass,'protein_unfolded_fraction_at_60C':float(frac[np.argmin(abs(pt-60))]),'protein_integrated_heat_kJ_per_mol':float(integral),'nist_zero_rate_enthalpy_J_per_g':float(mean[0]),'rate_peak_temperatures_C':[row[1] for row in rate_rows],'rate_integrals_J_per_g':[row[2] for row in rate_rows]};(a.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
```

After a first run, check the units before changing the model. Convert 5 mg to 0.005 g and 10 kelvin per minute to one sixth kelvin per second. Confirm the factor of one thousand between milliwatts and watts. Then vary the baseline intervals and inspect the cold-crystallization area and initial-crystallinity estimate. This is more useful than reporting additional fitted decimal places. Finally compare the three scan-rate curves: peak height and peak temperature differ, while correctly converted full integrals remain similar. Shape and accumulated energy can be examined separately.

A controlled comparison also distinguishes numerical sensitivity from specimen variability. Changing integration limits on the same trace probes the analysis procedure. Scanning separate pieces from one material probes spatial or sampling variation. Preparing independent batches probes manufacturing or formulation variation. These comparisons answer different questions even when all produce a spread of enthalpy values. Store the definition of each repeat alongside its result. For a heterogeneous composite, sampling position and polymer fraction may explain more variation than the instrument's short-term noise, so repeating the same calculation many times cannot replace representative sampling.

For biodegradable materials prepared under different cooling conditions, preserve the first scan as a measurement of the actual processing state and add common-history rescans to compare subsequent behavior. Interpret differences with the known component fractions and crystallization events. For protein buffer screening, combine thermal traces with recovery, concentration and scan-rate comparisons, then connect promising conditions to activity and storage experiments. If the main question is whether heating removes water, solvent or decomposition products, thermogravimetric analysis in the next chapter directly follows mass and adds another evidence channel.

A reproducible DSC result identifies specimen mass and state, pan and atmosphere, temperature program, scan number, endothermic direction, baseline and integration limits, and the normalization denominator. A glass-transition temperature specifies its assessment method. Crystallinity specifies reference fusion enthalpy and polymer mass basis. Protein enthalpy specifies concentration and molar conversion. Together with the complete curve, these definitions turn an isolated peak into information that can connect processing, structure and practical use.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/T01.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Watson & O’Neill: Differential microcalorimeter, US3263484A](https://patents.google.com/patent/US3263484A/en)

   Power-compensation feedback and history.
2. [TA Instruments: Interpreting Unexpected Events and Transitions in DSC Results, TA039](https://www.tainstruments.com/pdf/literature/TA039.pdf)

   Moisture, relaxation, thermal history and baselines.
3. [TA Instruments: DSC and MDSC Online Training, Applications](https://www.tainstruments.com/wp-content/uploads/2020-DSC-Online-Training-Part-2-1.pdf)

   Peak areas, cold crystallization and crystal reorganization.
4. [TA Instruments: Determination of Polymer Crystallinity by DSC, TA123](https://www.tainstruments.com/applications-notes/thermal-analysis-application-brief-determination-of-polymer-crystallinity-by-dsc/)

   Heat-flux principle and common-history comparisons.
5. [Malvern: DSC Theory and Practice](https://www.malvernpanalytical.com/en/learn/knowledge-center/whitepapers/wp140701-dsc-theory-and-practice)

   Matched buffers, unfolding heat capacity, rescans and rate dependence.
6. [Fortin et al. (2024): NIST SP260-242, Indium SRM2232a](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.260-242.pdf)

   Published indium estimates and credible intervals from Table 4.

   NIST-authored U.S. government research; Table 4 numeric values redrawn with credit, no third-party artwork reused.
7. [NIST: Copyrights and Disclaimers](https://www.nist.gov/copyrights-disclaimers)

   Reuse and credit for public government research information.
