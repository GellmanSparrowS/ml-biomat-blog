# Protein adsorption: A material’s first encounter with a biological environment

Source: https://ml-biomat.com/tutorials/experimental-methods/p05/en/
Language: en

Follow injection and rinsing to distinguish protein arrival, departure, coupled water and functional presentation.

## The surface a cell meets may already wear a protein layer

When a newly prepared material enters serum-containing culture medium, its interfacial environment begins to change. Proteins approach the material, remain briefly or bind more persistently, and may change orientation or expose previously sheltered regions. A cell-culture substrate may benefit from accessible adhesion sites, whereas a blood-contacting device or analytical sensor may benefit from reduced accumulation of unwanted proteins. The question therefore extends beyond the chemical identity of the original material. In the liquid used for its application, what protein layer forms, how quickly does it develop and how much remains after rinsing?

Adsorption describes enrichment near an interface. Absorption instead emphasises entry into the interior of a material; both can occur in a porous solid or permeable hydrogel. Proteins are also more complicated than equal-sized rigid balls. Their amino-acid chains fold into structures with different charged, water-compatible and water-avoiding regions. Near a solid, electrostatic interactions, hydrogen bonding, dispersion interactions and changes in water and ion organisation all contribute. A flexible object with several different contact faces is a useful analogy: changing its pose can alter both the contact area and the functional regions presented to the surrounding solution. That picture helps explain why surface amount, orientation and biological activity are related but distinct observations.

This chapter follows a practical flow experiment. Buffer first establishes a baseline, a known protein concentration is introduced, and the flow then returns to the same buffer without protein. The resulting time trace is a sensorgram. Optical and acoustic measurements read different physical consequences of layer formation. We will connect those signals to capacity, rates and retained amount, with calculations that show exactly what each quantity means. Surfaces with the same final amount can develop at different rates, and the same acoustic mass can contain different proportions of protein and coupled water. Defining the research question first makes the choice of signal and model more useful.

## From finite adsorption sites to molecules that change a surface

In his 1932 Nobel lecture, Langmuir described how industrial vacuum techniques helped make surface experiments quantitative. Controlled gases, cleanable filaments and measurements sensitive to small changes in gas quantity supported comparisons under defined conditions. The single-layer adsorption model offers a clear starting picture: a surface contains a finite number of positions, each empty or occupied, while molecules continually arrive and leave. The grid in the original diagram illustrates this idea. It does not imply that an actual protein-coated material is a perfectly regular checkerboard. The purpose is to establish a countable relationship among arrival, empty positions and departure before asking which additional processes an experiment reveals.

Biological molecules add another level. Leo Vroman's 1962 study examined wettability after proteins adsorbed onto hydrophilic and hydrophobic solids, directing attention toward the properties presented by the resulting layer. Adsorbed protein changes what the surrounding liquid encounters, so the initial material chemistry is one part of an evolving interface. In mixed solutions, concentrations, diffusion and interactions also influence composition over time. Early arrivals may be displaced, remain attached or rearrange. A purified single-protein experiment helps isolate a specified interaction, while experiments with complex biological fluids approach the intended application. Together they provide a progression from controlled mechanisms toward realistic mixtures.

![Original conceptual diagrams of arrival/departure at finite sites, protein orientation and water, and a shearing quartz resonator with coupled layer. These connect Langmuir surface studies, Vroman’s 1962 wetting study and Sauerbrey’s 1959 frequency–mass relation; not to scale.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/27e870e6b14f3473ae1c4e86.svg?v=27e870e6b14f)

Figure 1Original conceptual diagrams of arrival/departure at finite sites, protein orientation and water, and a shearing quartz resonator with coupled layer. These connect Langmuir surface studies, Vroman’s 1962 wetting study and Sauerbrey’s 1959 frequency–mass relation; not to scale.

In 1959 Sauerbrey related the frequency change of a quartz resonator to the added mass of a thin layer. Quartz is piezoelectric: electric fields can produce deformation, and deformation can generate electrical signals. A sensor uses a thin quartz disk oscillating in shear at high frequency. Material attached to its surface changes the response. Dissipation monitoring subsequently added information about how quickly oscillation decays after the drive is stopped. Three ideas consequently meet in a modern adsorption experiment: finite-site kinetics describes exchange, biological surface studies focus attention on the state of the adsorbed layer, and sensitive instruments provide a continuous interfacial signal.

A useful research sequence begins with a planar model surface of well-defined chemistry and thickness, then transfers comparable chemistry to the actual device or scaffold. The planar sensor offers a more clearly defined area and flow environment. A porous scaffold adds internal area, diffusion paths and potentially retained liquid. When their values differ, first identify the denominator: projected area, accessible internal area or material mass. The model experiment can clarify particular interactions, while the real geometry tests their consequences under application conditions. The connection becomes stronger when the measurement definitions remain explicit through that transfer.

## What optical and acoustic instruments actually detect

Surface plasmon resonance, or SPR, detects changes in the optical environment close to a metal film. Refractive index describes how light propagates through a medium. When protein accumulates near the surface and replaces part of the volume previously occupied by water, the local refractive-index profile changes and the instrumental response shifts. The first recorded quantity is normally a response in instrumental units. For a given system, proportionality to bound material supports kinetic analysis. Converting to absolute mass additionally requires an appropriate optical model or calibration. The constructed example uses an already calibrated equivalent areal mass so that quantities can be compared directly, without declaring one universal response-unit-to-mass conversion for all materials.

Quartz crystal microbalance with dissipation monitoring, QCM-D, records changes in resonance frequency and energy loss. A frequency decrease commonly accompanies added load, while dissipation reports altered loss during oscillation. For a thin, rigid and firmly coupled film, the Sauerbrey relation converts frequency shift normalised by harmonic number into mass per area. Harmonics are different resonant modes of the same system: a 5-megahertz fundamental can be measured at odd multiples such as the third and fifth. Similar normalised shifts across harmonics and small dissipation changes help assess a simple rigid-layer interpretation, together with film thickness, uniformity and liquid conditions.

$$
\Gamma_Q=-C_Q\frac{\Delta f_n}{n}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ea099b4870b360b7240fa408.svg) | Sauerbrey acoustic areal mass change, ng/cm². |
| ![Formula](https://ml-biomat.com/static/agent-math/5246fed9d112b38b3d16f46c.svg) | Mass coefficient for 5 MHz fundamental quartz, 17.7 ng/(cm²·Hz). |
| ![Formula](https://ml-biomat.com/static/agent-math/dd14ee12476c7cb989d35bb4.svg) | Shift from baseline at harmonic n, Hz. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Odd harmonic number, dimensionless, such as five. |

Applies to thin, rigid, firmly coupled layers with a matched liquid baseline. A fifth-harmonic shift of −50 Hz gives 177 ng/cm²; retain the coupled-water meaning of acoustic load in liquid.

For a 5-megahertz quartz sensor, the commonly used coefficient is 17.7 nanograms per square centimetre per hertz. A fifth-harmonic shift of minus 50 hertz is first divided by five, giving minus 10 hertz. Applying the negative coefficient gives 177 nanograms per square centimetre. Omitting harmonic normalisation would introduce a factor of five. In liquid, the acoustically coupled load also includes water that moves with the layer, whether directly associated with molecules, trapped within the structure or coupled through fluid motion. Acoustic areal mass can therefore differ from an optical estimate of protein mass. For example, 200 nanograms per square centimetre of protein accompanied by 300 of coupled water gives 500 in the ideal rigid-coupling limit.

$$
\Gamma_Q=\Gamma_p+\Gamma_w=\Gamma_p(1+h)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ea099b4870b360b7240fa408.svg) | Total acoustic areal mass in an ideal rigid-coupling limit, ng/cm². |
| ![Formula](https://ml-biomat.com/static/agent-math/84290949f1b09115dbf4d4de.svg) | Protein areal mass, ng/cm². |
| ![Formula](https://ml-biomat.com/static/agent-math/79041d57b32a3efcee507dc2.svg) | Areal mass of water moving with the film, ng/cm². |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | Water-to-protein mass ratio, dimensionless. |

A teaching limit of additive coupled mass, not an inversion of soft-film viscoelasticity. Γp=200 and h=1.5 give Γw=300 and total 500 ng/cm².

A soft layer can deform during oscillation, adding viscoelastic contributions to its frequency response. Several harmonics of frequency and dissipation can then be analysed with a model of the film and surrounding liquid to estimate thickness or mechanical properties. Multiplying every frequency shift by a mass coefficient hides that model choice inside a seemingly simple number. Increased dissipation supplies information about energy loss; identifying a unique protein conformation requires additional evidence. Optical–acoustic comparisons are most informative when surface chemistry, buffer, temperature, flow and observation time are matched. Then differences can be connected more clearly to the two measurement principles.

Areal mass is useful because the exposed area is part of the experiment. A total of 100 nanograms on one square centimetre and the same total on ten square centimetres represent different average coverages. Conversely, a rough material may provide more accessible area than its flat outline suggests. Report which area enters the denominator, and distinguish a uniform-film model from a physically uniform layer. These choices are particularly consequential when moving from a smooth sensor coating to particles, fibres or porous constructs.

## Turning an injection into an interpretable time record

A flow experiment begins with stable buffer. The buffer controls pH, salt modifies interactions between charged species, and temperature affects protein state, liquid properties and sensor response. Match the sample formulation to the running buffer. Otherwise switching solutions can produce a step through bulk refractive-index change or through viscosity and density changes, even before substantial adsorption occurs. That step may disappear abruptly when buffer returns. Bubbles can introduce more dramatic disturbances and alter the effective contact area. Prepare solutions according to instrument requirements, avoid bubbles and establish baseline stability over the time scale that the intended measurement will use.

A reference channel records contributions that accompany the experiment but are not the targeted surface interaction. In SPR binding measurements it may have no active ligand while sharing other preparation steps. In materials adsorption studies the comparison surface should have a similarly explicit purpose. A reference is not simply an arbitrary surface assumed to bind nothing. If sample and reference channels respond differently to solution changes, nonspecific adsorption or temperature, subtraction leaves a difference. Blank-buffer injections help identify shared injection and drift features. The useful question is which physical contribution a chosen control is designed to remove.

![Constructed data: A sample/reference channels, B five corrected concentration traces and shared fit, C residuals, D protein mass versus rigid-limit coupled mass with water/protein mass ratio 1.5. Vertical lines mark injection start and rinse at 180 s.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/867368957aee5b70741a4a52.svg?v=867368957aee)

Figure 2Constructed data: A sample/reference channels, B five corrected concentration traces and shared fit, C residuals, D protein mass versus rigid-limit coupled mass with water/protein mass ratio 1.5. Vertical lines mark injection start and rinse at 180 s.

The constructed data make this visible. The sample channel contains protein areal mass, a bulk step during injection, slow drift and noise. The reference contains the same bulk step and drift with its own noise. After subtraction, the pre-injection average sets the zero level. Reference subtraction does not remove all random noise because the two channels have independent fluctuations; it removes their shared systematic contributions. The program retains both original channels and the corrected trace, allowing a spike to be traced back to sample, reference or their difference. Saving only a smoothed corrected curve would lose that distinction.

Injection lasts 180 seconds, followed by rinsing until 600 seconds. During association, arrival and departure occur simultaneously. During ideal rinsing, free concentration close to the surface rapidly approaches zero and the trace mainly reports departure. If departing molecules remain nearby and bind again, the apparent decay slows. Varying flow, lowering binding-site density or changing flow geometry can investigate transport and rebinding. Flow must also remain compatible with sample stability and instrument operation. Record it as an experimental condition, and examine whether fitted rate constants remain consistent across appropriate transport controls.

Preparation variability belongs in the same record. Independent surface preparations reveal differences in coating quality and available sites, while multiple injections on one surface test repeatability and regeneration. A sample that aggregates during storage can introduce species with different sizes and multivalent contacts. Concentration errors propagate into association and affinity estimates, even when the time trace looks smooth. Checking protein condition and preparing the concentration series carefully therefore contributes directly to the meaning of the kinetic parameters.

## Deriving a simple curve from empty and occupied positions

Let the surface have a fixed maximum capacity, with some fraction occupied at any instant. Arrival should depend on solution concentration because more nearby molecules offer more opportunities to contact the surface. It should also depend on remaining empty positions. Departure should depend on occupied amount because an empty surface has no adsorbed molecule available to leave. Subtracting departure from arrival gives a single-site kinetic model. Its assumptions are equivalent sites, independent occupancy, a known concentration at the surface and no additional conformational transition or multilayer growth. Each mathematical term then corresponds to a concrete molecular event rather than appearing as an unexplained fitting expression.

$$
\frac{d\Gamma}{dt}=k_{\mathrm{on}}c(\Gamma_{\max}-\Gamma)-k_{\mathrm{off}}\Gamma,\quad K_D=\frac{k_{\mathrm{off}}}{k_{\mathrm{on}}},\quad\Gamma_{\mathrm{eq}}=\Gamma_{\max}\frac{c}{c+K_D}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b5919a287af415ef85d8991d.svg) | Current protein areal mass, ng/cm². |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | Free protein concentration near surface, μmol/L; equal to bulk concentration in the example. |
| ![Formula](https://ml-biomat.com/static/agent-math/96b11419ef9b145692736b96.svg) | Single-site model capacity, 300 ng/cm². |
| ![Formula](https://ml-biomat.com/static/agent-math/451c8ed5e76589b3848476d8.svg) | Association rate constant, (μmol/L)⁻¹s⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/1c651848773cdeda67716da2.svg) | Departure rate constant, s⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/a443778a30c5870335c56f4d.svg) | Equilibrium dissociation constant, μmol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/ff8de87dac4fb31350383329.svg) | Equilibrium areal mass at the given concentration, ng/cm². |

Model of equivalent independent sites without extra state transitions and with sufficiently rapid transport. kon=0.02 and koff=0.002 give KD=0.1 μmol/L. At c=KD, half capacity is occupied: 150 ng/cm².

At equilibrium, arrival and departure balance. Average coverage stops increasing, although individual molecules continue exchanging. Equilibrium occupied fraction increases with concentration and reaches one half when concentration equals the dissociation constant. The example specifies association constant 0.02 per micromolar per second and dissociation constant 0.002 per second. Their ratio is 0.1 micromolar. With capacity 300 nanograms per square centimetre, sufficiently long exposure at 0.1 micromolar therefore gives 150. Sufficient exposure is a real time condition: after the chosen 180-second injection, the amount is only about 76.99. Treating that finite-time endpoint as an equilibrium value would change the interpretation of a concentration curve.

$$
\Gamma(t)=\begin{cases}\Gamma_{\mathrm{eq}}[1-e^{-(k_{\mathrm{on}}c+k_{\mathrm{off}})t}],&0\le t\le t_i,\\\Gamma(t_i)e^{-k_{\mathrm{off}}(t-t_i)},&t>t_i,\end{cases}\qquad t_{1/2}=\frac{\ln2}{k_{\mathrm{off}}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b07e3ee7455065c1715113d8.svg) | Protein areal mass at time t, ng/cm². |
| ![Formula](https://ml-biomat.com/static/agent-math/ff8de87dac4fb31350383329.svg) | Equilibrium areal mass for injection concentration, ng/cm². |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time from injection start, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/d66c51d3359af66c3f0dc0c5.svg) | End of injection and start of rinse, 180 s. |
| ![Formula](https://ml-biomat.com/static/agent-math/451c8ed5e76589b3848476d8.svg) | Association rate constant, (μmol/L)⁻¹s⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | Injection concentration, μmol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/1c651848773cdeda67716da2.svg) | Departure rate constant, s⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/8c3b402073bc1431c5892dfd.svg) | Time from rinse start for amount to halve, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | Base of natural exponentials, dimensionless. |

Initially empty surface, constant injection concentration, and approximately zero free concentration during rinse. Defaults give 76.9872 ng/cm² at 180 s, 33.2362 at 600 s and rinse half-life 346.574 s.

During rinsing, when free concentration near the surface can be approximated as zero, the remaining amount decays exponentially. A departure constant of 0.002 per second gives a half-life of about 346.57 seconds. The clock for that decay starts when rinsing starts, not when sample injection starts. Thus 600 seconds in the example corresponds to 420 seconds of rinsing and about 33.24 nanograms per square centimetre remaining. Multiplying both rate constants by three preserves their ratio but speeds both approach to equilibrium and subsequent departure. Affinity and speed therefore describe different features: two interactions can have the same equilibrium preference yet run on different time scales.

![A equilibrium occupancy, B rates changed together at fixed KD=0.1 μM, C rinse decay normalised to its initial value. Affinity, formation speed and retained fraction are distinguished.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/81326e2fb58c8df29ec4f456.svg?v=81326e2fb58c)

Figure 3A equilibrium occupancy, B rates changed together at fixed KD=0.1 μM, C rinse decay normalised to its initial value. Affinity, formation speed and retained fraction are distinguished.

The program fits all time points from five concentrations together, sharing association rate, departure rate and capacity. Noisy observations yield approximately 0.02005 per micromolar per second, 0.001998 per second and 299.61 nanograms per square centimetre, respectively, with dissociation constant about 0.09964 micromolar. Different concentrations help separate capacity from arrival rate, while rinsing helps identify departure. Plot residuals against time. Persistent deviations around switching or throughout one phase point toward a missing process. Before adding arbitrary parameters, examine concrete possibilities such as buffer mismatch, transport, heterogeneous sites or protein aggregation.

The independent-site model also clarifies experimental information requirements. If every concentration is far below the dissociation constant and the injection is very short, the response is nearly an initial straight rise. Several parameter combinations can produce a similar slope. Concentrations spanning the transition and traces with resolved curvature provide additional information. A longer rinse helps distinguish a slow departure process from an almost constant offset. Instrument sampling should resolve those changes, while baseline stability should be evaluated over the same duration. Good parameter estimation begins with the time and concentration range of the experiment.

## Reading a real thin layer in terms of water and modelling

The next figure redraws published summary data from Kobayashi and colleagues in 2018. Bovine serum albumin, BSA, or fibronectin, FN, adsorbed onto oxidised polystyrene, and a Voigt model of QCM-D signals estimated layer thickness. At 20 degrees Celsius, mean thicknesses were 4.5 and 13.8 nanometres; at 37 degrees they were 4.2 and 10.3. Error bars are standard deviations of three experiments. The plot preserves reported summaries rather than inventing individual observations from their means and deviations. Read model thickness, substrate and temperature together, rather than treating a value as a universal molecular diameter.

![Published experimental summaries redrawn from Kobayashi et al., Int. J. Mol. Sci. 19, 1516 (2018), Table 2, doi:10.3390/ijms19051516, CC BY 4.0. QCM-D/Voigt-model thicknesses for BSA and FN on oxidised polystyrene. Points are means; bars are standard deviations of three experiments. Individual observations have not been reconstructed.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/a3e744ec4b459d9768534e05.svg?v=a3e744ec4b45)

Figure 4Published experimental summaries redrawn from Kobayashi et al., Int. J. Mol. Sci. 19, 1516 (2018), Table 2, doi:10.3390/ijms19051516, CC BY 4.0. QCM-D/Voigt-model thicknesses for BSA and FN on oxidised polystyrene. Points are means; bars are standard deviations of three experiments. Individual observations have not been reconstructed.

A solution-depletion experiment offers another route when real-time interface sensing is unavailable. Measure protein concentration before and after contact, then use solution volume to calculate the missing amount. Vessel adsorption, evaporation and sampling losses enter the same balance. Suppose 100 microlitres initially contains 20 micrograms of protein and loses 0.2 micrograms after contacting a material with area one square centimetre. The inferred amount is 200 nanograms per square centimetre, but the concentration difference is only one percent of the starting amount. Preparation and assay precision therefore matter strongly. A matched vessel without the material estimates container losses. When surface uptake is small relative to the amount in solution, direct interface sensing can resolve the change more effectively.

Fluorescent labelling supplies spatial information by attaching a light-emitting group to protein and imaging its distribution. Quantification then depends on labelling ratio, bleaching and environmental effects on fluorescence, as well as any alteration of molecular interactions caused by the label. Mixing labelled and unlabelled protein while maintaining consistent total concentration and labelled fraction helps define a comparison. The best choice depends on whether the question concerns spatial distribution, real-time kinetics or total quantity. These signals complement one another because they observe different aspects of the same developing layer.

Adsorbed-layer thickness and molecular length are different quantities. Proteins can lie down, tilt or extend, with water occupying part of the layer. Incomplete coverage can also be represented by an effective uniform-layer response. Thickness comparisons consequently benefit from information about areal mass, continuity and the density or optical parameters used in the model. The plotted scale is instructive: layers of a few or a few tens of nanometres are below the direct resolving power of ordinary optical microscopy, yet suitable interface-sensitive measurements can provide quantitative descriptions. The model identifies which aspect of that thin region the reported number represents.

For cell adhesion, total protein amount is one step in a longer chain. Cell receptors recognise accessible molecular regions. A layer with unchanged mass can present different biological activity if important sites are hidden or altered. Combine quantity measurements with an appropriate site-recognising antibody experiment, enzyme activity, spectroscopy or cellular response when those questions matter. For low-fouling materials, compare retention in mixtures, temperatures and contact times relevant to use. Each additional observation should state whether it addresses amount, composition, structure or function, so that complementary measurements extend the explanation rather than repeat the same information.

Rinsing defines the retained amount operationally. Gentle buffer flow measures material remaining under that condition. Changing salt, pH or adding a competitor creates a different retention experiment. Drying before weighing or imaging can alter the organisation of a hydrated layer, so identify wet and dry states clearly. For a reusable sensor, compare baseline and capacity over repeated adsorption–rinse cycles to reveal progressive residue or loss of activity. The time trace then connects to performance during repeated use, rather than remaining a single isolated exposure.

## Interactive experiment: equal affinity with different rates

The interactive plot uses the same single-site model with adjustable concentration, association rate and departure rate. Capacity remains 300 nanograms per square centimetre. First keep both rates fixed and increase concentration: association rises faster and equilibrium occupancy increases. Next multiply both rates by the same factor. The dissociation constant stays unchanged, while the curve approaches its target and decays more quickly. Finally decrease departure rate alone and examine retained fraction after rinsing. The plot displays the 180-second endpoint and the amount at 600 seconds, separating equilibrium capacity, finite-time uptake and retention after a specified rinse.

## Interactive: adsorption and rinsing

The solid line is finite-time uptake; the dashed line is the equilibrium target at injection concentration. Rinsing starts at 180 s.

[Figure: Adsorption time trace](https://ml-biomat.com/tutorials/experimental-methods/p05/en/#P05-plot)

At the default concentration of 0.1 micromolar, equal to the specified dissociation constant, the equilibrium target is 150 nanograms per square centimetre. The observed model trajectory is still below that target at 180 seconds. Raising concentration to 0.4 micromolar moves the target to 240 and increases the approach rate. Both consequences follow from the arrival term, concentration multiplied by empty capacity. At the beginning of rinsing, concentration is switched to zero and fractional decay depends on the departure constant. Dividing each concentration trace by its own rinse-start value therefore produces the same normalised decay under this model. Divergence in experimental normalised traces motivates checks of rebinding, heterogeneous sites or state changes.

Use the time cursor to compare a curve during injection with the same curve after buffer replacement. A displayed equilibrium target refers to the injection concentration; it is not a second prediction that adsorption remains at that level during rinsing. During rinsing the surrounding free concentration changes, and the target state changes with it. This distinction connects an experimental operation, switching a valve, to a change in the terms of the kinetic equation. It is also why a complete sensorgram is more informative than a single endpoint taken without its exposure history.

## Complete analysis: retain channels and test the model

The complete program constructs association and rinse traces at five concentrations, adds shared bulk shifts and drift with independent noise, performs reference subtraction and baseline correction, and fits shared parameters. Optimisation uses logarithms of the parameters so that rates and capacity stay positive. This numerical parameterisation preserves the physical equation. The program separately recovers parameters from noise-free observations and checks quantities that can be calculated by hand: half occupancy, rinse half-life and conversion of a fifth-harmonic frequency shift. Original sample and reference channels, corrected curves, predictions and specified teaching curves are all exported.

### Complete Python: referencing and multiconcentration kinetics

Generate checkable constructed traces, fit shared positive parameters, and redraw explicitly licensed published summaries.

```
"""Protein adsorption: reversible kinetics, referencing and hydrated mass.
Constructed observations are distinct from the bundled published summary table.
Run: python main.py --output results --language en
"""
from pathlib import Path
import argparse,json,csv
import numpy as np
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Ellipse,Circle

def coverage(time,concentration,kon=.02,koff=.002,capacity=300.,injection=180.):
    t=np.asarray(time,dtype=float);rate=kon*concentration+koff
    eq=capacity*kon*concentration/rate
    end=eq*(-np.expm1(-rate*injection))
    return np.where(t<0,0,np.where(t<=injection,eq*(-np.expm1(-rate*np.maximum(t,0))),end*np.exp(-koff*np.maximum(t-injection,0))))

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();o=a.output;o.mkdir(parents=True,exist_ok=True)
    tr=lambda z,e:z if a.language=='zh' else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fbfcfc','savefig.facecolor':'#fbfcfc','text.color':'#18344a'})
    blue='#186c94';green='#188777';orange='#d27839';purple='#8a5d92'
    def save(f,n):f.savefig(o/f'{n}-{a.language}.svg',bbox_inches='tight');f.savefig(o/f'{n}-{a.language}.png',bbox_inches='tight',dpi=150);plt.close(f)
    rng=np.random.default_rng(1805);time=np.arange(-60,602,2.);conc=np.array([.025,.05,.1,.2,.4]);truth=np.array([coverage(time,c) for c in conc]);bulk=np.array([25*(c/.1)*((time>=0)&(time<180)) for c in conc]);drift=.008*(time+60)
    reference=bulk+drift+rng.normal(0,.8,truth.shape);raw=truth+bulk+drift+rng.normal(0,1.2,truth.shape)
    corrected=raw-reference;corrected-=corrected[:,time<0].mean(axis=1,keepdims=True)
    def residual(logp):
        k1,k2,cap=np.exp(logp);return (np.array([coverage(time,c,k1,k2,cap) for c in conc])-corrected).ravel()
    fit=least_squares(residual,np.log([.015,.003,280.]));kon,koff,cap=np.exp(fit.x);pred=np.array([coverage(time,c,kon,koff,cap) for c in conc])
    noiseless=least_squares(lambda x:(np.array([coverage(time,c,*np.exp(x)) for c in conc])-truth).ravel(),np.log([.015,.003,280.]))
    base=coverage(time,.1);hydration=1.5;acoustic=base*(1+hydration);df5=-5*acoustic/17.7
    summary={'fit_kon_uM_inv_s_inv':float(kon),'fit_koff_s_inv':float(koff),'fit_capacity_ng_cm2':float(cap),'fit_KD_uM':float(koff/kon),'fit_rmse_ng_cm2':float(np.sqrt(np.mean((pred-corrected)**2))),
    'specified_KD_uM':.1,'equilibrium_at_KD_ng_cm2':150.,'mass_at_180s_ng_cm2':float(coverage(180,.1)),'mass_at_600s_ng_cm2':float(coverage(600,.1)),
    'rinse_half_life_s':float(np.log(2)/.002),'sauerbrey_5th_minus50Hz_ng_cm2':177.,'hydrated_mass_for_200_ng_cm2':500.,
    'noiseless_fit_kon':float(np.exp(noiseless.x[0])),'noiseless_fit_koff':float(np.exp(noiseless.x[1])),'noiseless_fit_capacity':float(np.exp(noiseless.x[2])),'data_kind':'Constructed kinetics; published table summarized separately'}
    (o/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    rows=np.vstack([np.column_stack([np.full(len(time),c),time,raw[i],reference[i],corrected[i],pred[i],truth[i]]) for i,c in enumerate(conc)])
    np.savetxt(o/'data.csv',rows,delimiter=',',header='concentration_uM,time_s,raw_equivalent_ng_cm2,reference_equivalent_ng_cm2,corrected_ng_cm2,fit_ng_cm2,specified_ng_cm2',comments='')
    np.savetxt(o/'acoustic.csv',np.column_stack([time,base,acoustic,df5]),delimiter=',',header='time_s,protein_ng_cm2,rigid_limit_coupled_ng_cm2,delta_f5_Hz',comments='')
    tab=list(csv.DictReader((Path(__file__).parent/'data/kobayashi2018-table2.csv').open(encoding='utf8')))
    fig,axs=plt.subplots(1,3,figsize=(14.5,4.5))
    for ax in axs:ax.set_xlim(0,10);ax.set_ylim(0,6);ax.axis('off')
    ax=axs[0];ax.add_patch(Rectangle((.4,1),9.2,.6,facecolor='#a7b8c0'))
    for j in range(8):
        ax.add_patch(Rectangle((.7+j*1.1,1.6),.85,.45,facecolor='white',edgecolor=blue))
        if j in [0,2,3,6]:ax.add_patch(Circle((1.1+j*1.1,2.45),.4,color=green))
    ax.annotate('',xy=(5.6,2.3),xytext=(5.6,4.1),arrowprops={'arrowstyle':'<->','color':orange,'lw':2});ax.text(5,5,tr('Langmuir：有限位置与动态平衡','Langmuir: finite sites and exchange'),ha='center',fontsize=10);ax.text(5,.25,tr('位置可空出，也可被占据','Sites can be empty or occupied'),ha='center',fontsize=10)
    ax=axs[1];ax.add_patch(Rectangle((.5,1),9,.6,facecolor='#a7b8c0'));ax.add_patch(Ellipse((3,2.3),3,.9,angle=10,facecolor=green));ax.add_patch(Ellipse((7,2.7),1.4,2.1,facecolor=orange))
    for x,y in [(2,2.8),(3,3),(4,2.7),(6.3,3.6),(7,3.9),(7.7,3.5)]:ax.add_patch(Circle((x,y),.17,color='#82c5df'))
    ax.text(5,5,tr('Vroman，1962：吸附改变润湿','Vroman, 1962: adsorption alters wetting'),ha='center',fontsize=9);ax.text(5,.25,tr('取向、暴露基团与周围水','Orientation, exposed groups and water'),ha='center',fontsize=9)
    ax=axs[2];ax.add_patch(Rectangle((1,1.4),8,.6,facecolor='#b6cbd1'));ax.add_patch(Rectangle((1,2),8,.15,color=orange));
    for x in [2,4,6,8]:ax.add_patch(Ellipse((x,2.5),1.1,.6,facecolor=green))
    ax.annotate('',xy=(8,1),xytext=(2,1),arrowprops={'arrowstyle':'<->','color':blue,'lw':2});ax.text(5,5,tr('Sauerbrey，1959：频率与附加质量','Sauerbrey, 1959: frequency and added mass'),ha='center',fontsize=9);ax.text(5,.25,tr('石英作剪切振动，膜随其运动','Quartz shears; coupled film moves with it'),ha='center',fontsize=9);save(fig,'history')
    fig,axs=plt.subplots(2,2,figsize=(12,8.7));aa,bb,cc,dd=axs.ravel();i=2
    aa.plot(time,raw[i],color=blue,label=tr('样品通道','Sample channel'));aa.plot(time,reference[i],color=orange,label=tr('参考通道','Reference channel'));aa.legend(fontsize=9);aa.set_title(tr('A  体相阶跃与漂移叠加','A  Bulk step and drift are superposed'),loc='left');aa.set_ylabel(tr('等效面密度 / ng/cm²','Equivalent areal mass / ng/cm²'))
    for j,c in enumerate(conc):bb.scatter(time[::5],corrected[j,::5],s=9,alpha=.55);bb.plot(time,pred[j],label=f'{c:g} μM')
    bb.legend(fontsize=8,ncol=2);bb.set_title(tr('B  多浓度共享动力学参数','B  Concentrations share kinetic parameters'),loc='left');bb.set_ylabel(tr('蛋白质面密度 / ng/cm²','Protein areal mass / ng/cm²'))
    for j in range(5):cc.plot(time,corrected[j]-pred[j],lw=.7,alpha=.65)
    cc.axhline(0,color='#a1abb2');cc.set_title(tr('C  保留全部拟合残差','C  Retain all fit residuals'),loc='left');cc.set_ylabel(tr('残差 / ng/cm²','Residual / ng/cm²'))
    dd.plot(time,base,color=green,label=tr('蛋白质质量','Protein mass'));dd.plot(time,acoustic,color=blue,label=tr('刚性极限耦合质量','Rigid-limit coupled mass'));dd.legend(fontsize=9);dd.set_title(tr('D  耦合水改变声学质量定义','D  Coupled water changes acoustic mass'),loc='left');dd.set_ylabel(tr('面密度 / ng/cm²','Areal mass / ng/cm²'))
    for ax in axs.ravel():ax.axvline(0,color='#b3bec4',ls=':');ax.axvline(180,color='#b3bec4',ls=':');ax.set_xlabel(tr('时间 / s','Time / s'))
    fig.tight_layout();save(fig,'sensorgrams')
    fig,axs=plt.subplots(1,3,figsize=(14,4.5));cc=np.logspace(-3,1,200);axs[0].semilogx(cc,cc/(cc+.1),color=blue);axs[0].axvline(.1,color=orange,ls='--');axs[0].axhline(.5,color='#a1abb2',ls=':');axs[0].set_xlabel(tr('浓度 / μmol/L','Concentration / μmol/L'));axs[0].set_ylabel(tr('平衡覆盖分数','Equilibrium occupied fraction'));axs[0].set_title(tr('A  半占据对应KD','A  Half occupancy at KD'),loc='left')
    for k,col in [(.001,blue),(.002,orange),(.006,green)]:axs[1].plot(time,coverage(time,.1,k*10,k)/300,color=col,label=f'koff={k:g} s⁻¹')
    axs[1].set_xlabel(tr('时间 / s','Time / s'));axs[1].set_ylabel(tr('占据分数','Occupied fraction'));axs[1].set_title(tr('B  相同KD，不同速度','B  Same KD, different rates'),loc='left');axs[1].legend(fontsize=8)
    rinse=np.linspace(0,600,200)
    for k,col in [(.001,blue),(.002,orange),(.006,green)]:axs[2].plot(rinse,np.exp(-k*rinse),color=col)
    axs[2].set_xlabel(tr('冲洗经过时间 / s','Elapsed rinse time / s'));axs[2].set_ylabel(tr('相对冲洗开始的保留分数','Fraction retained from start of rinse'));axs[2].set_title(tr('C  冲洗读取离开速度','C  Rinse reads the departure rate'),loc='left');fig.tight_layout();save(fig,'kinetics')
    fig,axs=plt.subplots(1,2,figsize=(11.8,4.8))
    for ax,protein in zip(axs,['BSA','FN']):
        rr=[r for r in tab if r['protein']==protein];x=np.array([float(r['temperature_C']) for r in rr]);y=np.array([float(r['thickness_mean_nm']) for r in rr]);err=np.array([float(r['thickness_sd_nm']) for r in rr]);ax.errorbar(x,y,yerr=err,fmt='o',ms=9,capsize=5,color=green if protein=='BSA' else blue);ax.set_xticks([20,37]);ax.set_xlim(15,42);ax.set_ylim(0,16);ax.set_xlabel(tr('温度 / °C','Temperature / °C'));ax.set_ylabel(tr('Voigt模型厚度 / nm','Voigt-model thickness / nm'));ax.set_title(protein+' · '+tr('氧化聚苯乙烯','Oxidized polystyrene'),loc='left');ax.text(.04,.08,tr('均值±标准差；n=3','Mean ± SD; n=3'),transform=ax.transAxes,fontsize=10)
    fig.suptitle(tr('Kobayashi等，2018，表2数据重绘 · CC BY 4.0','Kobayashi et al., 2018, Table 2 redrawn · CC BY 4.0'),fontsize=12);fig.tight_layout();save(fig,'published')
    print(json.dumps(summary))

if __name__=='__main__':main()
```

Read the results from signal to interpretation. Check the pre-injection zero and any remaining switching step, compare rising traces across concentration, inspect decay under matched rinsing, and then examine fitted parameters. The acoustic example is explicitly a rigid-coupling limit illustrating protein and water mass definitions. The published table separately retains its model, surface, temperature, sample number and reuse licence. Constructed data supply a calculation whose starting truth is known, while the published experiment supplies a real research scale. Applied to a new material, the same sequence turns the observation that something accumulated at a surface into specific evidence about formation rate, retention, composition and function.

Changing one assumption at a time is a useful extension. Add an unmatched bulk offset to the reference, shorten the rinse or remove the highest concentration, then observe which residual pattern or fitted parameter changes. Keep those modifications labelled as constructed experiments. Their purpose is to learn how information enters an inference, so that preparation, controls and sampling can be chosen deliberately when actual protein solutions and surfaces are measured.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/P05.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Irving Langmuir — Surface Chemistry, Nobel lecture (1932)](https://www.nobelprize.org/uploads/2018/06/langmuir-lecture.pdf)

   Primary historical account of vacuum, filament experiments and monolayer ideas.

   Historical facts paraphrased; no lecture figures reproduced.
2. [Leo Vroman — Effect of Adsorbed Proteins on the Wettability of Hydrophilic and Hydrophobic Solids (1962)](https://www.nature.com/articles/196476a0)

   Historical study of wettability after protein adsorption.
3. [NPTEL — Langmuir adsorption assumptions](https://archive.nptel.ac.in/content/storage2/courses/103104045/lecture25/25_6.htm)

   Equivalent independent sites and the monolayer model.
4. [Biolin Scientific — QCM-D measurement](https://www.biolinscientific.com/measurements/qcm-d)

   Piezoelectricity, harmonics, frequency and dissipation.
5. [Biolin Scientific — The QCM-D principle](https://www.biolinscientific.com/faq/the-qcm-d-principle)

   Optical/acoustic mass and coupled water.
6. [Biolin Scientific — Sauerbrey equation](https://www.biolinscientific.com/blog/what-is-the-sauerbrey-equation)

   1959 relation, coefficient 17.7 and rigid-film conditions.
7. [Cytiva — Kinetics and affinity measurements with Biacore systems](https://cdn.cytivalifesciences.com/api/public/content/digi-33041-pdf)

   Reference surfaces, mass transport, concentration series and kinetic design.
8. [Harvard CMI — Surface plasmon resonance](https://cmi.hms.harvard.edu/surface-plasmon-resonance)

   Refractive index, ligand, analyte and response units.
9. [Kobayashi et al. — Temperature and serum protein adsorption (2018)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5983614/)

   Actual Table 2 QCM-D/Voigt thickness summaries with surface, temperature and n.

   CC BY 4.0; numeric table transcribed and bilingual chart redrawn; attribution and licence included.
