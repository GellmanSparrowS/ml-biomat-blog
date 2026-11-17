# SPR: Watching binding and dissociation in real time

Source: https://ml-biomat.com/tutorials/experimental-methods/c06/en/
Language: en

Connect optics, references and time traces to molecular affinity, kinetics and transport.

## Does strong binding also mean a long stay?

Imagine choosing an antibody for a blood-testing device. During a short contact period it must capture a scarce target protein, and during the subsequent buffer wash it should retain enough target to produce a useful measurement. Two antibodies may bind the same amount after a long incubation yet behave differently during this sequence. One reaches that amount quickly; another approaches it slowly. A third captures molecules rapidly but also releases them rapidly. Surface plasmon resonance, or SPR, records the interaction as a continuous time trace. Response usually rises while analyte passes over a binding surface and falls after analyte-free buffer replaces the sample. These time-dependent changes are central to capture assays, molecular screening and the design of functional interfaces.

The surface might carry antibodies, receptors, nucleic acids or selected chemical groups. The immobilized partner is usually called the ligand, while the partner delivered in solution is the analyte. These names describe experimental roles: reversing which partner is immobilized reverses the roles. Before interpreting a curve, identify the immobilized material, the flowing material and its concentration. Protein adsorption onto a biomaterial and specific binding of a purified protein to an immobilized receptor can both produce rising signals, but the surface composition and the research question differ. Understanding those differences is part of understanding the measurement.

A reading room with a fixed number of seats provides a useful starting analogy. People outside encounter empty seats, while seated people eventually leave. The final occupancy depends on both arrival and departure. If both processes become ten times faster, the eventual occupied fraction can remain unchanged even though the room fills and empties much faster. Affinity describes the equilibrium preference at a specified concentration; kinetics describes the rates of approaching and leaving that state. Later, an interactive experiment holds affinity fixed while changing both rates together, making this distinction visible rather than leaving it as terminology.

The direct SPR signal is an optical response to the environment near a surface. Interpreting it as molecular binding requires connections between optics, surface chemistry and transport through solution. We will follow a constructed dataset from raw solvent steps through reference subtraction and a shared kinetic fit, then introduce a near-surface supply problem that changes the apparent behavior. The resulting affinity is therefore associated with an observable time course and a specified experimental arrangement. This perspective is particularly useful when a software table contains precise-looking numbers but the practical decision concerns capture during the first minute or retention during a later wash.

## Turning a change at a metal film into a time record

Light reaching a metal film can do more than undergo ordinary reflection. With a suitable thin film, polarization and incidence angle, prism-coupled light can excite collective electronic oscillations near the metal interface. Coupling energy into this surface mode produces a minimum in reflected intensity at a particular angle. The location of that minimum depends on the optical environment on either side of the film and is sensitive to the region close to its exposed surface. Molecules accumulating there change the local refractive index and shift the resonance. Tracking the optical change continuously produces a record of interfacial events that would otherwise be difficult to see directly.

In 1983, Liedberg, Nylander and Lundström demonstrated surface plasmon resonance for gas detection and biosensing, including interactions between an immunoglobulin layer and antibodies. Their biological experiments already contained several ideas familiar in modern sensor studies: change solution concentration, observe the time-dependent response and compare antibodies to investigate selectivity. The historical advance was to turn an interface's optical sensitivity into a means of observing biological interactions. Controlled flow systems, temperature regulation, automatic injections and analysis software subsequently made such observations easier to reproduce and compare.

The original schematic below connects this history to the optical mechanism. It represents a prism, metal film and molecular layer without reproducing an historical photograph or measured spectrum. The two resonance profiles are conceptual shapes illustrating a positional shift. Actual instruments may follow angle, wavelength or another related optical quantity and report the change in response units, RU. Converting an optical response into surface mass requires an appropriate relationship for the sensor and the material's refractive-index increment. A convenient protein mass conversion should therefore be associated with its measurement conditions rather than applied indiscriminately to every surface or molecule.

![Original prism-coupling and metal-film schematic connected to the 1983 SPR biosensing experiments; not to scale. Conceptual resonance profiles illustrate a positional shift, not measured angular spectra or a full electromagnetic calculation.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/04a019b831206eacf41158ac.svg?v=04a019b83120)

Figure 1Original prism-coupling and metal-film schematic connected to the 1983 SPR biosensing experiments; not to scale. Conceptual resonance profiles illustrate a positional shift, not measured angular spectra or a full electromagnetic calculation.

Refractive-index sensitivity explains why references remain essential even though binding is observed without adding a fluorescent label. Salt, glycerol or dimethyl sulfoxide differences between sample and running buffer can change the optical environment as the sample enters the flow cell. Temperature changes, nonspecific adsorption and altered hydration can also contribute. A sharp injection step may therefore reflect a bulk solution difference, while a gradually accumulating response that persists during washing invites further comparison with appropriate controls. The direction of the optical change does not by itself identify its molecular cause.

Flow delivers analyte toward the sensing region, but molecules still have to reach the surface through the local concentration field. When binding consumes nearby analyte faster than transport replenishes it, the free concentration next to the binding sites becomes lower than the nominal injected concentration. Three parts of the experiment now meet in the same curve: optics detects the local environment, accessible sites determine binding opportunities, and transport determines how much free analyte is locally available. Keeping these parts separate conceptually makes it easier to recognize which experimental adjustment could explain a surprising trace.

## Understanding the rates behind the rising and falling curve

Begin with identical, independent surface sites, one analyte molecule per site, a near-surface free concentration equal to the delivered concentration, and response proportional to bound amount. When many sites are empty, association has many opportunities. As sites fill, the number of opportunities falls. At the same time, some bound molecules dissociate. The net rate of response change is the rate of new binding minus the rate of loss. This balance is more useful than memorizing an exponential curve because it states the assumptions to examine when an experiment behaves differently.

$$
\frac{dR}{dt}=k_{\mathrm{on}}C(R_{\max}-R)-k_{\mathrm{off}}R
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | Binding response, RU. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time, seconds. |
| ![Formula](https://ml-biomat.com/static/agent-math/451c8ed5e76589b3848476d8.svg) | Association rate constant, L/(mol·s), or M⁻¹ s⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | Near-surface free analyte concentration, equal to the delivered concentration in this model, mol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/005e161a184834c885d95173.svg) | Analyte response when all effective sites are occupied, RU. |
| ![Formula](https://ml-biomat.com/static/agent-math/1c651848773cdeda67716da2.svg) | Dissociation rate constant, s⁻¹. |

Identical independent sites, 1:1 binding, proportional response and prompt local supply. Empty sites control association; bound sites control departure. With kₒₙ=2×10⁵, C=10⁻⁸ mol/L and Rmax=120 RU, initial R=0 gives 0.24 RU/s.

The association rate constant contains inverse concentration and inverse time in its units: doubling free analyte concentration doubles the encounter contribution at each empty site in this model. The dissociation rate constant contains inverse time because the probability of departure is proportional to the population already bound. Consider an association constant of 200,000 per molar per second, a dissociation constant in the kinetic sense of 0.002 per second, an analyte concentration of 10 nM and a capacity of 120 RU. Initially all sites are available, giving a response increase of 0.24 RU per second. There is initially no bound population to lose. Both terms contribute as binding develops.

$$
K_D=\frac{k_{\mathrm{off}}}{k_{\mathrm{on}}},\quad R_{\mathrm{eq}}=\frac{R_{\max}C}{K_D+C},\quad k_{\mathrm{obs}}=k_{\mathrm{on}}C+k_{\mathrm{off}},\quad R(t)=R_{\mathrm{eq}}(1-e^{-k_{\mathrm{obs}}t})
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a443778a30c5870335c56f4d.svg) | Equilibrium dissociation constant, mol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/1c651848773cdeda67716da2.svg) | Dissociation rate constant, s⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/451c8ed5e76589b3848476d8.svg) | Association rate constant, L/(mol·s). |
| ![Formula](https://ml-biomat.com/static/agent-math/98fcf8602db40c1c0cc09549.svg) | Equilibrium binding response at the specified concentration, RU. |
| ![Formula](https://ml-biomat.com/static/agent-math/005e161a184834c885d95173.svg) | Analyte response at full effective-site occupancy, RU. |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | Constant free analyte concentration, mol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/557e93507479e84f43d62190.svg) | Observed approach rate, s⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/a187b42ecc9ef443adcbc568.svg) | Response at time t after association begins on an initially empty surface, RU. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time since injection begins, seconds. |

Setting net rate to zero gives equilibrium; solving the constant-concentration rate equation gives the approach. kₒₙ=2×10⁵ and kₒff=0.002 give Kᴅ=10 nM. C=10 nM and Rmax=120 give Req=60 RU, kobs=0.004 s⁻¹ and R≈30.795 RU at 180 s.

Equilibrium does not mean that molecules stop moving. It means that association and dissociation balance on average. The chosen rates give an equilibrium dissociation constant of 10 nM. At a free concentration of 10 nM, half the sites are occupied, so equilibrium response is 60 RU. Reaching that response takes time. Here the approach rate is 0.004 per second, corresponding to a 250-second time scale. After only 180 seconds of injection, response is about 30.79 RU. The maximum seen at the end of an injection can therefore be an imposed stopping point rather than saturation or equilibrium.

When analyte-free buffer replaces the sample and free analyte near the surface is removed promptly, the association term vanishes. Dissociation then removes a fraction of the remaining bound population during each short interval. The response declines exponentially rather than losing the same number of response units every second. Its half-life is the time needed to lose half the starting bound population. In this model the half-life is independent of starting response, but it depends directly on the dissociation rate. This is an intuitive quantity for an assay that must survive several minutes of washing.

$$
R(\tau)=R_0e^{-k_{\mathrm{off}}\tau},\qquad t_{1/2}=\frac{\ln 2}{k_{\mathrm{off}}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/93f17ccb2498eb79f09caaf2.svg) | Binding response at time τ after washing begins, RU. |
| ![Formula](https://ml-biomat.com/static/agent-math/31e316fb976f1ca84f57e4cb.svg) | Binding response at the start of washing, RU. |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | Time after washing begins, seconds. |
| ![Formula](https://ml-biomat.com/static/agent-math/1c651848773cdeda67716da2.svg) | Dissociation rate constant, s⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/8c3b402073bc1431c5892dfd.svg) | Time for binding response to fall to half its value at wash onset, seconds. |

Prompt removal of free analyte and no rebinding leave first-order dissociation. kₒff=0.002 s⁻¹ gives a half-life of 346.574 s and retention exp(−0.84)=0.431711 after 420 s. At 0.02 s⁻¹, half-life is 34.657 s.

The half-life here is about 346.6 seconds. Multiplying both rate constants by ten preserves the 10 nM equilibrium dissociation constant but shortens the half-life to about 34.7 seconds and speeds the approach to equilibrium. The interactive experiment separates affinity, a common rate multiplier and analyte concentration. Keep affinity and concentration fixed while changing the multiplier: the equilibrium reference line stays in place while the time trace changes. Then change concentration, which affects both equilibrium occupancy and the approach rate. This is why a concentration series provides more information than repeated observations at a single concentration.

## Same affinity, different time courses

Independent 1:1 sites with capacity 120 RU; a 180-second injection is followed by analyte-free buffer. Hold Kᴅ and concentration fixed while changing the common rate multiplier, comparing the time trace with the equilibrium line.

[Figure: Kinetic time trace and equilibrium response](https://ml-biomat.com/tutorials/experimental-methods/c06/en/#C06-plot)

## Good curves begin with the surface and the sample

Immobilization should make binding sites accessible while keeping the surface stable throughout the experiment. Covalent attachment, tag capture and other affinity-based methods produce different orientations and distances from the sensor. A large quantity of immobilized protein can still provide few active sites if important binding faces are blocked. Multivalent analytes may contact neighboring ligands simultaneously, producing behavior that depends on surface spacing as well as individual molecular interactions. Lower ligand loading can help reveal simpler binding kinetics and reduce local depletion, while the remaining signal must still be sufficient for the intended measurement.

The response accumulated during ligand immobilization and the maximum response from subsequent analyte binding are different quantities. The latter also depends on analyte molecular mass, binding stoichiometry, the accessible fraction of ligand and optical response properties. Equating the two responses would impose the wrong capacity before fitting even begins. A practical analysis may estimate analyte capacity as a shared parameter and then compare it with the surface design. If different concentrations require markedly different capacities to fit, surface activity, sample state and the assumed interaction model deserve closer examination.

Concentration must also describe the molecular species relevant to binding. Total protein concentration can differ from the concentration of active monomer, while aggregates can alter both effective concentration and valency. Sample and running buffers should be closely matched, particularly for components with strong refractive-index effects. Small differences in dimethyl sulfoxide concentration are a familiar reason to perform solvent correction in small-molecule work. A useful concentration series spans the anticipated dissociation constant and extends below and above it, allowing the curves to constrain the rising phase, equilibrium trend and capacity together.

A reference surface should reproduce the support, coupling chemistry and nonspecific interactions of the active surface as closely as practical while removing the specific interaction of interest. An empty support is convenient but may not reproduce adsorption onto an immobilized protein layer. An unrelated reference protein introduces its own charge, loading and stability considerations. Reference subtraction is therefore a matched measurement of selected contributions, and its usefulness depends on the match. Blank injection cycles, usually involving running buffer, record repeatable valve-switching, fluidic and surface disturbances that remain after the channel subtraction.

Contact time, wash time and cycle order belong to experimental design as much as concentration does. Very slow dissociation observed over a short window can appear almost horizontal, providing little information about its slope. Very fast association can overlap with the delivery and mixing transient. Repeating an intermediate concentration and inserting blank cycles helps reveal progressive loss of surface activity or drifting baselines. If regeneration is needed between cycles, it should remove retained analyte while preserving ligand function. Reviewing traces in their actual experimental order often reveals such changes earlier than inspecting the final parameter table alone.

## From four raw records to shared molecular parameters

The complete example constructs five analyte concentrations from 1 to 100 nM, with 180 seconds of association and 420 seconds of washing. For each concentration it retains the sample response on the active and reference surfaces, plus the corresponding active and reference responses during a blank cycle. The active sample channel contains binding, a 12 RU solvent step, slow drift and a short injection disturbance. The reference has the same solvent step and drift. An additional active-surface disturbance is deliberately made repeatable in the blank cycle, illustrating why a single channel subtraction can leave a systematic feature.

$$
R_{\mathrm{corr}}=(R_{\mathrm{active}}-R_{\mathrm{ref}})_{\mathrm{sample}}-(R_{\mathrm{active}}-R_{\mathrm{ref}})_{\mathrm{blank}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f3aa7cba0902d6a924f22a23.svg) | Double-referenced response, RU. |
| ![Formula](https://ml-biomat.com/static/agent-math/583d6435926c509afd302f04.svg) | Active-surface channel response, RU. |
| ![Formula](https://ml-biomat.com/static/agent-math/f556b6dcf070fc7983979795.svg) | Reference-surface channel response, RU. |
| ![Formula](https://ml-biomat.com/static/agent-math/ea4973df6ab1d58c52662533.svg) | Subscript identifying the analyte injection cycle. |
| ![Formula](https://ml-biomat.com/static/agent-math/4e1cf44e3abaae399d3584a3.svg) | Subscript identifying the matched blank injection cycle. |

Align injection times, match bulk contributions with the reference and repeatable artifacts with the blank, then subtract the pre-injection mean. Active=45, reference=13, blank active=2 and blank reference=1 RU give 31 RU. Four independent channels with noise SD 0.2 RU combine to about 0.4 RU.

First subtract the reference channel from the active sample channel to remove common solvent and drift contributions. Then subtract the active-minus-reference difference from the blank cycle to remove the repeatable injection disturbance. Finally, subtract the pre-injection mean to establish a zero baseline. The enlarged early-time panel shows these changes on the same scale. Each raw channel contains independent noise with a standard deviation of 0.2 RU. Combining four such records with positive or negative signs produces a standard deviation of approximately 0.4 RU. Correction reduces systematic bias while combining the noise of the measurements used in the correction.

![Constructed data, seed 660. Five concentrations share intrinsic rates and a capacity of 120 RU. A retains solvent steps; B compares deviations before and after double referencing; C shows corrected records and global fits; D is data minus model. Each original channel has noise SD 0.2 RU.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/f82b34801ffc22bc242127a4.svg?v=f82b34801ffc)

Figure 2Constructed data, seed 660. Five concentrations share intrinsic rates and a capacity of 120 RU. A retains solvent steps; B compares deviations before and after double referencing; C shows corrected records and global fits; D is data minus model. Each original channel has noise SD 0.2 RU.

Baseline subtraction also has a statistical consequence. The pre-injection average is estimated from a finite number of noisy observations. Subtracting that average shifts every point in the same cycle together, creating a small shared component of uncertainty. A smooth fitted curve can therefore be supported by many time points without those points constituting equally many independent experimental repeats. Repeated injections assess cycle reproducibility; independently prepared surfaces address variation in immobilization; independently prepared samples address another part of the experiment. Selecting the repeat that matches the intended comparison gives an uncertainty statement a clear experimental meaning. The constructed example uses one explicitly specified noise model so that the effects of four-channel subtraction remain easy to follow. When comparing real candidates, retain both the fitted traces and the repeat-level parameter estimates so that differences in reproducibility remain visible alongside differences in the mean result.

The five corrected curves are then fitted together with shared association rate, dissociation rate and capacity. Sharing parameters follows the design: the surface, analyte, temperature and buffer are the same while analyte concentration changes. The fit recovers an association rate of approximately 201,179 per molar per second, a dissociation rate of 0.0019996 per second, an equilibrium dissociation constant of 9.94 nM and a capacity of 119.78 RU. These values are close to the parameters used to construct the data. The comparison checks whether the stated analysis recovers known quantities under its own specified measurement model.

Residuals, defined as data minus model, reveal features that a fitted overlay can conceal. A curved residual throughout association suggests a missing time-dependent process. A narrow feature at injection switching directs attention to delivery delay or bulk correction. Systematic disagreement concentrated at high concentrations invites tests of transport, nonspecific adsorption or concentration-dependent aggregation. The example's RMS residual is about 0.401 RU, consistent with the scale expected from four independent noisy channels. This response-space discrepancy is distinct from an uncertainty interval on affinity. Uncertainty in concentration or surface activity requires additional analysis beyond reading the residual magnitude.

A deliberate alternative analysis takes the response at 180 seconds from each curve and treats those points as equilibrium measurements. Allowing capacity to vary gives an apparent dissociation constant of about 35.16 nM and a capacity of 145.37 RU. Fixing capacity at its true value of 120 RU still gives about 22.96 nM. The direction and size of such errors depend on concentration coverage and constraints; these numbers describe this constructed example. The important observation is that a smooth endpoint fit can accompany incorrect parameters. Whether equilibrium was reached has to be assessed from the original time course.

![Constructed models. A has the same rate ratio, Kᴅ=10 nM, but different time courses; the equilibrium response is 60 RU. B shows the error from treating 180-second endpoints as equilibrium, fitting both Kᴅ and capacity.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/b36af15238ae0f6e1627682a.svg?v=b36af15238ae)

Figure 3Constructed models. A has the same rate ratio, Kᴅ=10 nM, but different time courses; the equilibrium response is 60 RU. B shows the error from treating 180-second endpoints as equilibrium, fitting both Kᴅ and capacity.

## Why the concentration at the surface can differ from the syringe

Return to the reading room, but now give it a narrow entrance corridor. A crowd outside does not guarantee that people reach empty seats immediately. In SPR, transport limitation occurs when local binding consumes analyte faster than it is replenished. The free concentration near the sites falls below the bulk concentration. Fitting a simple model that substitutes the injected concentration for the local concentration can then interpret the slower response as slower intrinsic association. Increasing exchange or lowering site density changes supply or demand, respectively, providing experimental ways to investigate this distinction.

The example divides solution into a bulk region and a near-surface region. Bulk concentration is 30 nM during injection and zero during washing. Near-surface concentration is determined by exchange with the bulk, removal through binding and return through dissociation. Surface occupancy is expressed as a fraction, allowing binding and local mass conservation to be written together. An equivalent site concentration converts the surface inventory into the concentration scale of the chosen near-surface volume. With a larger inventory, the same fractional occupancy change consumes more free analyte. This model parameter is distinct from an optical response measured in RU.

$$
\frac{d\theta}{dt}=k_{\mathrm{on}}C_s(1-\theta)-k_{\mathrm{off}}\theta,\qquad \frac{dC_s}{dt}=k_{\mathrm{tr}}(C_b-C_s)-\Gamma\frac{d\theta}{dt}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | Fraction of sites occupied, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time, seconds. |
| ![Formula](https://ml-biomat.com/static/agent-math/451c8ed5e76589b3848476d8.svg) | Intrinsic association rate constant, L/(mol·s). |
| ![Formula](https://ml-biomat.com/static/agent-math/1c651848773cdeda67716da2.svg) | Intrinsic dissociation rate constant, s⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/59e6f76fe7f807e8f04f82ec.svg) | Free analyte concentration in the near-surface compartment, mol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/9a2c7455873446449e6636a4.svg) | Bulk analyte concentration, mol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/0403bdc848dfd0bb7d52ccc7.svg) | Exchange rate in this two-compartment model, s⁻¹, not volumetric flow. |
| ![Formula](https://ml-biomat.com/static/agent-math/b5919a287af415ef85d8991d.svg) | Total site inventory expressed per near-surface compartment volume, mol/L. |

Local mass balance subtracts binding consumption from exchange supply; negative occupancy change releases analyte. Cb=30 nM, Cs=0 and ktr=0.005 s⁻¹ give initial supply 0.15 nM/s. With Γ=200 nM, an occupancy increase of 0.01 consumes 2 nM of local free analyte.

The figure compares high capacity with slow exchange, high capacity with fast exchange, and low capacity with slow exchange. All three retain identical intrinsic association and dissociation constants. Only exchange or equivalent site concentration changes. In the high-capacity, slow-exchange case, free analyte near the surface is about 4.40 nM after 180 seconds, far below the 30 nM bulk concentration. Lower capacity reduces local consumption; faster exchange replenishes the local region more effectively. Curves are plotted as occupancy fractions so the comparison does not confuse a larger surface inventory with a larger fraction occupied.

![Constructed two-compartment model with fixed intrinsic rates. Equivalent site concentration is 200 or 2 nM; exchange rate is 0.005 or 0.5 per second. A compares occupancy fractions; C normalizes each curve to occupancy at wash onset. Residual local analyte can continue binding during slow exchange.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/b9c54a16c5fdbc078f156145.svg?v=b9c54a16c5fd)

Figure 4Constructed two-compartment model with fixed intrinsic rates. Equivalent site concentration is 200 or 2 nM; exchange rate is 0.005 or 0.5 per second. A compares occupancy fractions; C normalizes each curve to occupancy at wash onset. Residual local analyte can continue binding during slow exchange.

When washing starts, bulk concentration becomes zero, but the near-surface region does not empty instantly. Molecules leaving sites can also bind again before being carried away. In the high-capacity, slow-exchange case, occupancy briefly continues to increase after the switch, and after 420 seconds it is approximately 1.040 times its value at the start of washing. This ratio above one arises from the remaining local analyte and rebinding; the model does not create additional molecules. The simple exponential model with prompt removal retains only about 0.432 over the same period. A slowly falling trace can therefore reflect local transport as well as the intrinsic departure rate.

Multivalent attachment and transport-mediated rebinding can coexist, but they call for different comparisons. Multivalency concerns connections between one analyte and multiple sites; local rebinding concerns the fate of analyte that has become free near the surface. Changing ligand density, comparing monovalent fragments, adjusting flow conditions and extending observation time provide complementary information. Adding model parameters may improve a curve fit without identifying a unique microscopic mechanism. A stronger interpretation connects a proposed mechanism with an experimental change that specifically tests its predicted behavior.

## Reconstruct the analysis and choose the next experiment

The program below preserves the path from four raw channel records to the fitted parameter table. It exports time, original responses, corrected responses and fitted values for each concentration, along with occupancy and near-surface concentration from the transport model. Optical profiles and sensorgrams are explicitly constructed teaching examples, and a fixed random seed makes processing comparisons reproducible. Numerical integration asks what curve follows from specified transport and binding parameters. Least-squares fitting asks which parameters explain a collection of observed responses. These are related but different computational tasks.

A useful first pass through the code follows the 10 nM injection. Locate the solvent step in the active channel, perform the two subtractions and inspect why response at 180 seconds is only about 30.79 RU. Next multiply both kinetic rate constants by ten and observe an unchanged 60 RU equilibrium level with a tenfold shorter dissociation half-life. Finally inspect near-surface concentration in the transport output to understand why new binding can continue after bulk washing starts. The three exercises separate optical correction, equilibrium versus kinetics, and transport versus intrinsic chemistry.

### Complete SPR double referencing, kinetic fitting and transport comparison

Constructs and retains four-channel records, performs global fitting and a premature-endpoint comparison, then integrates a two-compartment transport model. Exports raw arrays, concentration-specific CSVs, parameters and figures.

```
"""Constructed SPR sensorgrams, double referencing and kinetic/transport diagnostics."""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import least_squares,curve_fit
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon,Circle

def response(t,concentration,kon=2e5,koff=.002,capacity=120.,contact=180.):
 t=np.asarray(t);c=concentration*1e-9;rate=kon*c+koff;equilibrium=capacity*kon*c/rate
 assoc=equilibrium*(-np.expm1(-rate*np.maximum(t,0)));end=equilibrium*(-np.expm1(-rate*contact))
 return np.where(t<0,0,np.where(t<=contact,assoc,end*np.exp(-koff*np.maximum(t-contact,0))))

def transport(exchange,site_equivalent,concentration=30.,contact=180.,stop=600.):
 """exchange: s^-1; site_equivalent: mol/L of near-surface compartment."""
 def rhs(bulk):
  def f(t,y):
   theta,cs=y;binding=2e5*cs*(1-theta)-.002*theta
   return [binding,exchange*(bulk-cs)-site_equivalent*binding]
  return f
 a=solve_ivp(rhs(concentration*1e-9),(0,contact),[0,0],t_eval=np.arange(contact+1),rtol=1e-9,atol=[1e-11,1e-16])
 b=solve_ivp(rhs(0),(contact,stop),a.y[:,-1],t_eval=np.arange(contact,stop+1),rtol=1e-9,atol=[1e-11,1e-16])
 return np.r_[a.t,b.t[1:]],np.c_[a.y,b.y[:,1:]]

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True);T=lambda z,e:z if a.language=='zh' else e
 plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.titlesize':12,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fcfbf7','axes.facecolor':'#fcfbf7','savefig.facecolor':'#fcfbf7'})
 B,R,G,Y='#167d9a','#d35f47','#37967d','#c49b35';cols=[B,G,Y,R,'#775f91']
 def save(f,n):f.savefig(a.output/f'{n}-{a.language}.svg');f.savefig(a.output/f'{n}-{a.language}.png',dpi=145);plt.close(f)
 rng=np.random.default_rng(660);t=np.arange(-30,601,dtype=float);cs=np.array([1,3,10,30,100.]);binding=np.array([response(t,c) for c in cs]);on=(t>=0)&(t<180);bulk=12*on;drift=.5+.005*(t+30)
 artifact=np.where(t>=0,1.5*np.exp(-np.maximum(t,0)/8),0)-np.where(t>=180,1.2*np.exp(-np.maximum(t-180,0)/8),0)
 active=binding+bulk+drift+artifact+rng.normal(0,.2,binding.shape);reference=np.broadcast_to(bulk+drift,binding.shape)+rng.normal(0,.2,binding.shape)
 blankactive=np.broadcast_to(drift+artifact,binding.shape)+rng.normal(0,.2,binding.shape);blankref=np.broadcast_to(drift,binding.shape)+rng.normal(0,.2,binding.shape)
 single=active-reference;corrected=single-(blankactive-blankref);corrected-=corrected[:,t<0].mean(axis=1,keepdims=True)
 def residual(p):return (np.array([response(t,c,*np.exp(p)) for c in cs])-corrected).ravel()
 fitted=least_squares(residual,np.log([2e5,.002,120]),bounds=(np.log([1e3,1e-5,10]),np.log([1e8,1,1000])),xtol=1e-12,ftol=1e-12,gtol=1e-12)
 kon,koff,cap=np.exp(fitted.x);prediction=np.array([response(t,c,kon,koff,cap) for c in cs]);kd=koff/kon*1e9
 endpoint=binding[:,t==180].ravel();eqfun=lambda c,k,r:r*c/(k+c);wrong,_=curve_fit(eqfun,cs,endpoint,p0=[20,130],bounds=(0,np.inf));earlyfixed,_=curve_fit(lambda c,k:eqfun(c,k,120),cs,endpoint,p0=[20],bounds=(0,np.inf))
 # Optical curves below are conceptual Lorentzian sketches, not Maxwell solutions.
 f,axes=plt.subplots(1,2,figsize=(13.5,5.5),layout='constrained');ax=axes[0];ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off');ax.set_title(T('A  1983：薄金属膜把结合变成光学变化','A  1983: Thin metal films turn binding into an optical change'),loc='left')
 ax.add_patch(Polygon([[1,4.5],[9,4.5],[5,.8]],fc='#dce9ed',ec=B));ax.add_patch(Rectangle((1,4.5),8,.2,fc=Y));ax.add_patch(Rectangle((1,4.7),8,2,fc='#e6f0ee',ec=G));ax.annotate('',xy=(8.5,6.3),xytext=(1.5,6.3),arrowprops={'arrowstyle':'->','color':G,'lw':2});ax.text(5,7.1,T('溶液流动；表面附近折射率改变','Flowing solution; refractive index changes near the surface'),ha='center',fontsize=10)
 for x in [2,3.5,5,6.5,8]:
  ax.plot([x,x],[4.7,5.1],c=B,lw=2);ax.add_patch(Circle((x,5.3),.22,fc=B))
 for x in [3.5,6.5]:ax.add_patch(Circle((x,5.67),.18,fc=R))
 ax.annotate('',xy=(5,4.5),xytext=(2,1.7),arrowprops={'arrowstyle':'->','color':R,'lw':2});ax.annotate('',xy=(8,1.7),xytext=(5,4.5),arrowprops={'arrowstyle':'->','color':R,'lw':2});ax.plot([5,5],[2.5,4.5],ls=':',c='#657785');ax.text(2,1.1,T('入射光','Incident light'),ha='center');ax.text(8,1.1,T('反射光','Reflected light'),ha='center');ax.text(5,.05,T('棱镜耦合原理图；尺寸不按比例','Prism-coupling principle; not to scale'),ha='center',fontsize=10)
 ax=axes[1];angle=np.linspace(69.5,71,500)
 for center,c,l in [(70.2,B,T('结合前','Before binding')),(70.35,R,T('近表面环境变化后','After near-surface change'))]:ax.plot(angle,1-.75*.12**2/((angle-center)**2+.12**2),c=c,label=l)
 ax.annotate('',xy=(70.35,.2),xytext=(70.2,.2),arrowprops={'arrowstyle':'->','color':G,'lw':2});ax.set(xlabel=T('入射角 / degree','Incidence angle / degree'),ylabel=T('相对反射强度','Relative reflected intensity'),title=T('B  共振谷的位置移动','B  The resonance minimum shifts'),ylim=(.1,1.05));ax.legend(fontsize=9);ax.text(.04,.025,T('示意轮廓；非实测角谱','Conceptual profiles; not measured angle spectra'),transform=ax.transAxes,fontsize=9)
 save(f,'optics-history')
 f,axes=plt.subplots(2,2,figsize=(13.7,8.3),layout='constrained');j=2;ax=axes[0,0];ax.plot(t,active[j],c=B,label=T('活性表面','Active surface'));ax.plot(t,reference[j],c=Y,label=T('参照表面','Reference surface'));ax.plot(t,binding[j],c=R,ls='--',label=T('构造结合真值','Constructed binding truth'));ax.set(xlabel=T('时间 / s','Time / s'),ylabel=T('响应 / RU','Response / RU'),title=T('A  10 nM：结合与溶剂阶跃叠在一起','A  10 nM: Binding plus solvent steps'));ax.legend(fontsize=9)
 ax=axes[0,1];sl=(t>=-10)&(t<=45);ax.plot(t[sl],single[j,sl]-binding[j,sl],c=Y,label=T('参照相减后 − 真值','Reference-subtracted minus truth'));ax.plot(t[sl],corrected[j,sl]-binding[j,sl],c=B,label=T('再扣空白后 − 真值','Double-referenced minus truth'));ax.axhline(0,c='#647681',lw=1);ax.set(xlabel=T('时间 / s','Time / s'),ylabel=T('剩余偏差 / RU','Remaining deviation / RU'),title=T('B  空白周期去除重复进样扰动','B  Blank cycles remove repeatable injection artifacts'));ax.legend(fontsize=9)
 ax=axes[1,0]
 for i,c in enumerate(cs):ax.plot(t,corrected[i],c=cols[i],lw=.7,alpha=.65,label=f'{c:g} nM');ax.plot(t,prediction[i],c=cols[i],lw=1.4)
 ax.axvline(180,c='#647681',ls='--',lw=1);ax.set(xlabel=T('时间 / s','Time / s'),ylabel=T('双参照校正响应 / RU','Double-referenced response / RU'),title=T('C  多浓度共享一组动力学参数','C  Concentrations share kinetic parameters'));ax.legend(ncol=2,fontsize=9)
 ax=axes[1,1]
 for i,c in enumerate(cs):ax.plot(t,corrected[i]-prediction[i],c=cols[i],lw=.55,alpha=.55)
 ax.axhline(0,c='#647681',lw=1);ax.set(xlabel=T('时间 / s','Time / s'),ylabel=T('数据 − 模型 / RU','Data − model / RU'),title=T('D  从残差检查遗漏的时间结构','D  Inspect residuals for missing time structure'))
 save(f,'reference-kinetics')
 f,axes=plt.subplots(1,2,figsize=(13.6,5.5),layout='constrained');ax=axes[0]
 for rate,c in [(1,B),(10,R)]:ax.plot(t,response(t,10,2e5*rate,.002*rate),c=c,label=T(f'速率 ×{rate}',f'Rates ×{rate}'))
 ax.axhline(60,c='#647681',ls=':',label=T('平衡响应 60 RU','Equilibrium: 60 RU'));ax.axvline(180,c='#647681',ls='--');ax.set(xlabel=T('时间 / s','Time / s'),ylabel=T('结合响应 / RU','Binding response / RU'),title=T('A  同为 Kᴅ=10 nM，不同的到达与离开','A  Both Kᴅ=10 nM, different arrival and departure'));ax.legend(fontsize=9)
 ax=axes[1];grid=np.geomspace(.3,300,200);ax.semilogx(grid,eqfun(grid,10,120),c=B,label=T('真正的平衡关系','True equilibrium'));ax.scatter(cs,endpoint,c=R,label=T('180 s 时的端点','Endpoints at 180 s'));ax.semilogx(grid,eqfun(grid,*wrong),c=R,ls='--',label=T('将端点误作平衡拟合','Premature equilibrium fit'));ax.set(xlabel=T('分析物浓度 / nM','Analyte concentration / nM'),ylabel=T('响应 / RU','Response / RU'),title=T('B  停止进样不等于达到平衡','B  Injection end is not equilibrium'));ax.legend(fontsize=9);ax.text(.04,.53,T(f'端点拟合 Kᴅ = {wrong[0]:.1f} nM\nRmax = {wrong[1]:.1f} RU',f'Endpoint fit Kᴅ = {wrong[0]:.1f} nM\nRmax = {wrong[1]:.1f} RU'),transform=ax.transAxes,fontsize=10)
 save(f,'affinity-versus-time')
 cases=[(.005,2e-7,R,T('高容量，慢交换','High capacity, slow exchange')),(.5,2e-7,B,T('高容量，快交换','High capacity, fast exchange')),(.005,2e-9,G,T('低容量，慢交换','Low capacity, slow exchange'))];traces=[];f,axes=plt.subplots(2,2,figsize=(13.6,8.1),layout='constrained')
 for k,g,c,l in cases:
  tt,yy=transport(k,g);traces.append((tt,yy));axes[0,0].plot(tt,yy[0],c=c,label=l);axes[0,1].plot(tt,yy[1]*1e9,c=c);axes[1,0].semilogy(tt[180:]-180,yy[0,180:]/yy[0,180],c=c)
 for ax in axes[0]:ax.axvline(180,c='#647681',ls='--',lw=1);ax.set_xlabel(T('时间 / s','Time / s'))
 axes[0,0].set(ylabel=T('位点占据比例','Fraction occupied'),title=T('A  固定内在速率，改变运输条件','A  Same intrinsic rates, different transport'));axes[0,0].legend(fontsize=9)
 axes[0,1].plot([0,180,180,600],[30,30,0,0],c='#647681',ls=':',label=T('主体溶液','Bulk solution'));axes[0,1].set(ylabel=T('近表面游离浓度 / nM','Near-surface free concentration / nM'),title=T('B  消耗与释放改变近表面浓度','B  Uptake and release alter local concentration'));axes[0,1].legend(fontsize=9)
 axes[1,0].plot(np.arange(421),np.exp(-.002*np.arange(421)),c='#647681',ls='--',label=T('没有再结合的指数解离','Exponential decay without rebinding'));axes[1,0].set(xlabel=T('洗脱开始后时间 / s','Time after wash begins / s'),ylabel=T('相对于洗脱起点的占据','Occupancy relative to start of wash'),title=T('C  邻近分析物再结合会拖慢下降','C  Rebinding slows the apparent decay'));axes[1,0].legend(fontsize=8)
 ax=axes[1,1];ax.axis('off');ax.set(xlim=(0,10),ylim=(0,7));ax.add_patch(Rectangle((1,4.4),8,1.5,fc='#deebe6',ec=G));ax.add_patch(Rectangle((1,2.2),8,1.5,fc='#dce9ee',ec=B));ax.text(5,5.15,T('主体浓度 Cb：进样 30 nM，洗脱 0','Bulk Cb: 30 nM during injection, 0 during wash'),ha='center',fontsize=10);ax.text(5,2.95,T('近表面浓度 Cs：运输与结合共同决定','Near-surface Cs: exchange plus binding'),ha='center',fontsize=10);ax.annotate('',xy=(5,4.35),xytext=(5,3.75),arrowprops={'arrowstyle':'<->','color':R,'lw':2});ax.text(5,.6,T('容量：200 或 2 nM 的等效位点浓度\n交换速率：0.005 或 0.5 s⁻¹；非直接流速','Capacity: 200 or 2 nM equivalent sites\nExchange: 0.005 or 0.5 s⁻¹; not a direct flow rate'),ha='center',fontsize=10);ax.set_title(T('D  两区域教学模型','D  Two-compartment teaching model'),loc='left')
 save(f,'transport-rebinding')
 np.savez_compressed(a.output/'constructed_sensorgrams.npz',time_s=t,concentration_nM=cs,binding_truth_RU=binding,active_RU=active,reference_RU=reference,blank_active_RU=blankactive,blank_reference_RU=blankref,corrected_RU=corrected,fitted_RU=prediction)
 for i,c in enumerate(cs):np.savetxt(a.output/f'sensorgram_{c:g}nM.csv',np.c_[t,active[i],reference[i],blankactive[i],blankref[i],corrected[i],prediction[i]],delimiter=',',header='time_s,active_RU,reference_RU,blank_active_RU,blank_reference_RU,corrected_RU,fitted_RU',comments='')
 np.savetxt(a.output/'transport.csv',np.c_[traces[0][0],*[arr for tt,yy in traces for arr in [yy[0],yy[1]*1e9]]],delimiter=',',header='time_s,high_slow_theta,high_slow_Cs_nM,high_fast_theta,high_fast_Cs_nM,low_slow_theta,low_slow_Cs_nM',comments='')
 summary={'fitted_kon_M_inv_s_inv':float(kon),'fitted_koff_s_inv':float(koff),'fitted_Kd_nM':float(kd),'fitted_capacity_RU':float(cap),'residual_RMS_RU':float(np.sqrt(np.mean((prediction-corrected)**2))),'half_life_s':float(np.log(2)/.002),'fast_half_life_s':float(np.log(2)/.02),'equilibrium_at_10nM_RU':60.,'response_at_180s_10nM_RU':float(response(180,10)),'premature_endpoint_Kd_nM':float(wrong[0]),'premature_endpoint_capacity_RU':float(wrong[1]),'premature_fixed_capacity_Kd_nM':float(earlyfixed[0]),'high_slow_retained_after_420s':float(traces[0][1][0,-1]/traces[0][1][0,180]),'no_rebinding_retained_after_420s':float(np.exp(-.002*420)),'high_slow_Cs_at_180s_nM':float(traces[0][1][1,180]*1e9)}
 (a.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
```

For antibody selection, the next comparison should match the actual assay sequence. Short-contact assays benefit from comparing captured amount within the available contact time. Wash-intensive assays require retention over the relevant washing interval, together with checks that surface density and local rebinding are appropriate to the intended device. For antifouling materials, comparing surface treatments across selected proteins and buffers may make total adsorption and release behavior more useful than forcing every trace into a single-site kinetic constant. The experimental question determines which part of the time record deserves attention.

A comparable SPR result includes the immobilized partner, analyte state, concentration series, temperature, buffer, loading, referencing procedure, contact and wash periods, and analysis model. The fitted quantities describe interactions under those conditions. Combining SPR with solution measurements such as isothermal titration calorimetry connects time-dependent behavior with heat and equilibrium information, while offering a way to examine effects of immobilization. Reading the curve carefully turns an optical time trace into a basis for the next sample preparation, surface design or experimental comparison.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/C06.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Harvard CMI: Surface plasmon resonance](https://cmi.hms.harvard.edu/surface-plasmon-resonance)

   Refractive-index response, immobilized ligand, references and matched solvent.
2. [Liedberg, Nylander & Lundström (1983): Surface plasmon resonance for gas detection and biosensing](https://bdt.semi.ac.cn/download/0.143812733726721.pdf)

   Original immunobinding and concentration-dependent time records.
3. [Biacore T200 Getting Started Handbook](https://cmi.hms.harvard.edu/sites/g/files/omnuum4016/files/cmi/files/biacoret200_gettingstarted_handbook.pdf)

   References, blank cycles, regeneration and concentration series.
4. [Cytiva: Kinetics and affinity measurements with Biacore systems](https://cdn.cytivalifesciences.com/api/public/content/digi-33041-pdf)

   Concentration design, transport and equilibrium analysis.
5. [Biacore Insight Evaluation Software User Manual, 29287248 AH](https://d3.cytivalifesciences.com/prod/IFU/29287248.pdf)

   Equal affinity with different rates, residuals and kinetic models.
