# Stress relaxation: Why force falls at fixed deformation

Source: https://ml-biomat.com/tutorials/experimental-methods/m05/en/
Language: en

Use force decay at fixed deformation to understand rearrangement, loading time, relaxation timescales and persistent resistance around cells.

## Why can the force change while the length stays fixed?

Stretch a soft elastic strip and hold your hands still. The initial tension may gradually become less noticeable even though the distance between your hands has not changed. A gasket confined inside a fixed gap, a dressing attached to moving skin and a hydrogel surrounding a cell can encounter related situations. Their shape is constrained while the internal load is redistributed. A stress-relaxation experiment turns that redistribution into a time record. It asks how rapidly resistance decreases, how much remains at long times and whether those changes affect contact pressure, mechanical support or the environment around a cell.

This experiment differs from hanging a constant weight from a strip and watching it lengthen. With a constant weight, force is controlled and deformation increases: that response is called creep. In stress relaxation, deformation is controlled and force changes. Imagine either pulling with a steady effort and observing how far something moves, or holding it at a fixed position and measuring the effort required to keep it there. Both experiments involve time, but the constraint imposed by the apparatus is different. Identifying the controlled input and the measured response is the first step toward interpreting either curve.

A falling force does not necessarily mean that the specimen has fractured. Polymer segments can rearrange, temporary junctions can dissociate and reform, and liquid can migrate through a hydrated network. These processes redistribute stress while the specimen remains connected. Grip slip, temperature changes and gradual drying can also change the measured force. The experimental task is to connect that force record to actual deformation, environmental conditions and structural observations. A descending trace becomes informative when its physical origin can be examined through these accompanying measurements.

We begin with a uniformly stretched specimen at small deformation. Nominal stress is force divided by original cross-sectional area. Engineering strain is the increase in gauge length divided by original gauge length. These definitions remove simple size effects from the comparison. A 20 mm gauge length extended by 0.4 mm has a strain of 2%. A force of 0.018 N acting on an original area of 10 mm² gives a stress of 1.8 kPa. In calculations, 2% is entered as 0.02. Multiplying stress in kPa by area in mm² requires a factor of 0.001 to obtain force in newtons.

$$
\sigma=\frac{F}{A_0},\qquad\varepsilon=\frac{L-L_0}{L_0},\qquad E_{\mathrm{rel}}(t)=\frac{\sigma(t)}{\varepsilon_0}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | Nominal tensile stress, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | Tensile force, N. |
| ![Formula](https://ml-biomat.com/static/agent-math/0c430ee48d22be2e69d0f3ad.svg) | Original cross-sectional area, m². |
| ![Formula](https://ml-biomat.com/static/agent-math/9bc08d537f481d038b7b8b9d.svg) | Engineering strain, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Current gauge length, m. |
| ![Formula](https://ml-biomat.com/static/agent-math/973a201db437d1c712202461.svg) | Original gauge length, m. |
| ![Formula](https://ml-biomat.com/static/agent-math/d392a7d1ae884b61e2eb5f45.svg) | Linear relaxation modulus, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time from an ideal strain step, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | Applied and held step strain, dimensionless. |

Uniform uniaxial small deformation. The relaxation-modulus definition assumes an initially unstressed specimen and an ideal step; finite loading requires its actual history. L0 = 20 mm and L = 20.4 mm give a strain of 0.02; F = 0.018 N and A0 = 10 mm² give 1800 Pa and a modulus of 90 kPa.

Small deformation is an experimental condition to examine, rather than a universal percentage applicable to every soft material. Repeat the test at several modest strains and compare stress divided by strain. Overlapping curves support a linear description within that tested range; systematic changes with amplitude motivate an amplitude-dependent analysis. The constructed records in this chapter obey a linear model so that loading history and timescale can be studied separately. For an actual material, the amplitude comparison should precede the choice of constitutive model.

## From molecular motion to a spring that gradually recoils

A useful historical connection begins with Maxwell’s 1867 work on gas dynamics. His investigation linked microscopic motion to macroscopic quantities such as stress and included the idea of a finite response time. The Maxwell model subsequently used in viscoelasticity places elastic storage and time-dependent flow along one load-bearing path. The broader lesson is that the present deformation may be insufficient to specify the present stress: the way the material reached its state also matters. The illustration below uses a modern mechanical analogy to explain this connection; it is not a reconstruction of a historical instrument.

Consider an ideal spring first. Increasing its extension increases its restoring force, while holding its extension keeps that force constant. A viscous piston, often represented as a dashpot, behaves differently: its resistance depends on the rate of motion. Moving faster requires more force. An ideal dashpot has no elastic restoring force determined solely by its position. Connecting the spring and dashpot end to end gives the spring a support that can move gradually. At fixed total extension, the dashpot extends while the spring recoils, so the force carried by their shared path decreases.

The exponential response follows from that arrangement. Elements in series carry the same stress, and their strains add. When total strain is fixed, any additional dashpot strain must be balanced by decreasing spring strain. Larger stress drives faster dashpot motion and faster spring recoil. As stress decreases, the redistribution slows down. Thus the amount lost during a short interval is proportional to the amount still present. Repeated fractional decrease produces an exponential curve, unlike a straight line that subtracts the same absolute amount every second.

$$
\dot\sigma+\frac{\sigma}{\tau}=E\dot\varepsilon,\qquad\tau=\frac{\eta}{E},\qquad\sigma(t)=\sigma(0)e^{-t/\tau}\quad(\dot\varepsilon=0)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | Stress in one Maxwell arm, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/e4e6fee55eb022e9924b6563.svg) | Time rate of stress, kPa/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | Spring modulus of this arm, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/9bc08d537f481d038b7b8b9d.svg) | Total strain of this arm, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/f89ba6efd1616ab8c8ae4551.svg) | Total strain rate, s⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | Dashpot viscosity, kPa s. |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | Arm relaxation time, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Elapsed time during the hold, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/5d675645d5125886ba434eba.svg) | Arm stress at the start of the hold, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | Base of the natural exponential, dimensionless. |

Series elements share stress and add strains; spring recoil compensates dashpot extension during a hold. η = 80 kPa s and E = 40 kPa give τ = 2 s; an initial arm stress of 0.8 kPa leaves 0.294304 kPa after 2 s.

The time constant gives this rate a physical scale. After one time constant, approximately 37% of the initial stress in that arm remains; after three, approximately 5% remains. This statement concerns the relaxing arm, rather than total specimen stress including any permanent load-bearing contribution. A viscosity of 80 kPa s combined with an arm modulus of 40 kPa gives a time constant of 2 s. Higher viscosity slows redistribution. With viscosity unchanged, a stronger spring provides a greater restoring drive and shortens the corresponding time constant.

![Original history and model diagrams: the molecular-motion/macroscopic-response question in Maxwell’s 1867 work; a modern series spring–dashpot analogy and parallel system with an equilibrium branch. These are mechanical analogies, not molecular structures or reconstructed apparatus.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/aa556da31b69d6a4a88abda1.svg?v=aa556da31b69)

Figure 1Original history and model diagrams: the molecular-motion/macroscopic-response question in Maxwell’s 1867 work; a modern series spring–dashpot analogy and parallel system with an equilibrium branch. These are mechanical analogies, not molecular structures or reconstructed apparatus.

A single Maxwell arm eventually releases all its stress, whereas many crosslinked materials retain a sustained load. Adding a spring in parallel represents that persistent contribution. Parallel paths experience the same strain, and their stresses add. Additional Maxwell arms can represent processes occurring on different timescales. The three paths shown here describe equilibrium support, faster relaxation and slower relaxation. These elements characterize a mechanical response. Assigning one fitted dashpot to a particular molecular bond requires additional evidence from chemistry, temperature dependence or independent structural measurements.

## Separate the amount of relaxation from its speed

Imagine an apparatus that changes strain instantaneously from zero to 2% and then holds it constant. Initially, the springs in all Maxwell arms carry load because their dashpots have not yet moved appreciably. The initial modulus is therefore the sum of all spring moduli. At sufficiently long times, the relaxing arms contribute progressively less, leaving the equilibrium spring. Between these limits, the individual exponential contributions add. The vertical change describes how much load-bearing capacity can redistribute, while the horizontal timescales describe how quickly the redistribution occurs.

$$
E(t)=E_\infty+\sum_{i=1}^{2}E_i e^{-t/\tau_i},\quad\sigma_{\mathrm{step}}(t)=\varepsilon_0E(t),\quad E_0=E_\infty+E_1+E_2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fff42b0e3f57a0075d95d7d8.svg) | Relaxation modulus for an ideal step, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/e3bc601649bd36677658617e.svg) | Equilibrium modulus, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Maxwell-arm index 1 or 2, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/25faaa3257b422e0c57c5010.svg) | Spring modulus of arm i, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/b8f98758746427e2aa1a5880.svg) | Relaxation time of arm i, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time after applying the step, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | Base of the natural exponential. |
| ![Formula](https://ml-biomat.com/static/agent-math/1bd58ca256010ed07317aabf.svg) | Step-response stress, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | Held step strain, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/89ba16e9e7f11a7da33694e2.svg) | Instantaneous modulus, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/de4ed77abe73974794d51c59.svg) | Spring moduli of the two Maxwell arms, kPa. |

Parallel paths share strain and add stresses, with linear parameters at fixed temperature. E∞ = 20, E1 = 40 and E2 = 30 kPa, with τ1 = 2 s, τ2 = 40 s and ε0 = 0.02, give E0 = 90 kPa, an initial stress of 1.8 kPa and an equilibrium stress of 0.4 kPa.

Our specified material has an equilibrium modulus of 20 kPa, a fast arm of 40 kPa with a 2 s time constant, and a slow arm of 30 kPa with a 40 s time constant. The instantaneous modulus is 90 kPa. At 2% strain, the ideal initial stress is 1.8 kPa and the equilibrium stress is 0.4 kPa. By 2 s, the fast arm has lost a substantial fraction of its stress while the slow arm retains most of its contribution. Resolving the contributions explains a steep early decrease followed by a long tail without attributing that tail to an instrument that has somehow failed to finish moving.

A logarithmic time axis helps display processes separated in time. On a linear axis extending over several hundred seconds, the first few seconds occupy very little space. A logarithmic axis gives comparable width to each tenfold interval. Where the graph includes zero hold time, we use an axis that is linear near zero and logarithmic farther away, retaining the event at the start of the hold. Read the tick labels carefully: equal horizontal spacing can indicate multiplication of time rather than addition of equal seconds. Changing the display coordinates does not change the actual time values used in fitting.

Normalizing stress by its initial value gives a curve starting at one, which is convenient for comparing relative relaxation but hides absolute load capacity. Materials beginning at 10 kPa and 1 kPa can both retain half their stress after a minute while exerting very different forces. Keep the original stress record and specify whether normalization uses an ideal step value, the actual measured peak or a value at a prescribed time. Altering that denominator alone changes the reported relaxation fraction of the same observation.

A half-relaxation time also needs an explicit definition. If the final stress plateau lies above half the initial total stress, the total signal never crosses the half-height line. The relaxing portion can nevertheless decrease by half. For one exponential arm, subtracting the plateau gives a half-decay time of approximately 0.693 times its time constant. With several arms, a half-decay time reflects their combined contributions. It remains a useful comparison under specified conditions, but it does not directly identify every underlying timescale.

## Relaxation begins before the apparatus reaches its target

A real apparatus has a finite speed. Reaching the same 2% strain might take 1 s or 20 s. This period of increasing strain is the loading ramp. An arm that relaxes appreciably in 2 s has already redistributed much of its load during a 20 s ramp. When the apparatus enters the hold, that arm contributes far less stress than it would immediately after an ideal step. Saving only the hold and treating its first point as the instantaneous response omits the relaxation that occurred while loading.

To calculate a finite ramp, imagine adding many small strain increments. Earlier increments have had longer to relax, while newly applied increments retain more stress. Summing their present contributions gives the total response. For a constant strain rate, this sum can be expressed as an integral and evaluated explicitly. Two clocks matter: loading time measured from the beginning of the ramp, and hold time measured from reaching the target strain. Combining these events into an ambiguous time origin changes the interpretation of the peak and early decay.

$$
\varepsilon(t)=\varepsilon_0\min(t/t_r,1),\quad\sigma(t)=E_\infty\varepsilon(t)+\sum_{i=1}^{2}\sigma_i(t),\qquad\sigma_i(t)=\begin{cases}E_i\varepsilon_0\frac{\tau_i}{t_r}(1-e^{-t/\tau_i})&0\leq t\leq t_r\\ E_i\varepsilon_0\frac{\tau_i}{t_r}(1-e^{-t_r/\tau_i})e^{-(t-t_r)/\tau_i}&t\geq t_r\end{cases}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dd72237021aa073cc29bdada.svg) | Current engineering strain, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | Final target strain, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time from ramp start, s, t≥0. |
| ![Formula](https://ml-biomat.com/static/agent-math/ce7b3f4467a12e80e6af8d40.svg) | Positive duration of the constant-rate ramp, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/6a05d6e83f4c2e8f52c235d7.svg) | Minimum of the arguments, holding strain after reaching the target. |
| ![Formula](https://ml-biomat.com/static/agent-math/ff305b24b1ce5e15f22817d6.svg) | Total nominal stress, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/e3bc601649bd36677658617e.svg) | Equilibrium spring modulus, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Arm index 1 or 2. |
| ![Formula](https://ml-biomat.com/static/agent-math/1d11eec53e2e8f271603794c.svg) | Stress in Maxwell arm i, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/25faaa3257b422e0c57c5010.svg) | Spring modulus of arm i, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/b8f98758746427e2aa1a5880.svg) | Relaxation time of arm i, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | Base of the natural exponential. |

A constant-rate ramp from zero stress followed by fixed strain; sum the decaying contributions of all strain increments. With moduli of 20, 40 and 30 kPa, relaxation times of 2 and 40 s, and ε0 = 0.02, peak stress is 1.622113 kPa for tr = 1 s and 0.952160 kPa for tr = 20 s. The quantity t − tr in the second branch is hold time.

With the specified parameters, a 1 s ramp reaches a peak stress of approximately 1.622 kPa, whereas a 20 s ramp reaches approximately 0.952 kPa. Both finish at the same strain. After the 20 s ramp, the fast arm contributes an apparent modulus of only about 4 kPa, compared with its specified spring modulus of 40 kPa. The slow arm contributes about 23.61 kPa, and the equilibrium contribution remains 20 kPa. Dividing this measured peak by strain therefore gives approximately 47.61 kPa rather than the instantaneous 90 kPa.

![The same 2% target strain produces different peaks for two ramp durations. Middle-panel time starts with loading; the bottom panel starts at the end of the 20 s ramp and separates equilibrium, fast and slow contributions. All values are calculated from the specified model.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/74bb8a7112d4d470320079ca.svg?v=74bb8a7112d4)

Figure 2The same 2% target strain produces different peaks for two ramp durations. Middle-panel time starts with loading; the bottom panel starts at the end of the 20 s ramp and separates equilibrium, fast and slow contributions. All values are calculated from the specified model.

A subtle point is that, for this linear model and an exact constant-rate ramp, each arm retains its original decay time during the subsequent hold. The ramp changes the amplitude at the start of the hold; it does not automatically change a 2 s physical time constant into another value. A two-exponential fit to ideal hold data can recover the correct timescales while underestimating arm moduli. Once a fast contribution falls below the noise, or the real loading contains overshoot, timescale identification also becomes difficult. Amplitude suppression and loss of identifiable information are related but distinct effects.

Record actual local strain, force and time throughout loading and holding. Rapid motion can produce inertial oscillation, while slow motion can obscure fast processes. Choosing a ramp requires matching instrument capability to the material timescale. An elastic reference can help examine the imposed motion, and repeated tests at different ramp durations can separate loading effects from material changes. If the measured strain is not a straight ramp, use the recorded history as the model input and update the arm stresses numerically. There is no requirement to discard the real history in favor of a more convenient ideal one.

## Make the changing force interpretable

A tensile relaxation setup needs a driven grip, a force transducer and a way to measure deformation within the specimen gauge region. Fixing crosshead position does not always fix local gauge length. The frame and grips also deform, and the specimen can slip at its attachments. As force decreases, elastic deformation stored in the apparatus recovers, potentially changing specimen extension during the nominal hold. Optical markers or an extensometer can verify what is actually held constant. A compression experiment instead requires attention to contact, friction and the particular geometry used to convert displacement into deformation.

The initial condition belongs to the loading history. Pre-stretching, repeated conditioning, immersion time and recovery since a previous test affect whether the specimen begins close to an unstressed state. The model here starts from rest with zero stress. An experiment with preload should retain both that preload and its duration. Preload can remove slack but can also allow fast relaxation before the formal measurement begins. Defining the zero, preload and waiting sequence is more informative than shifting every curve vertically until its beginning looks the same.

Temperature and hydration deserve simultaneous attention. A soft specimen can dry over several hundred seconds, while a transducer that has not thermally stabilized can drift. Such changes occupy the same part of the record often assigned to slow relaxation. Monitor temperature, use suitable fluid or humidity control, and observe an unloaded or stable-reference baseline over a comparable duration. When the tail is comparable to baseline drift, improving environmental control and force resolution is more useful than adding another exponential term. Fluid-bath measurements should also account for buoyancy and additional forces at liquid contacts.

Choose sampling around the expected timescales. Identifying a 2 s process requires sufficiently dense records near loading. Estimating a 40 s process and its eventual plateau requires a longer hold. The example combines dense early sampling with more widely spaced late observations. Equal weight per point means that densely sampled intervals exert more influence on the fit, so sampling and weighting should be considered together. When measurement uncertainty varies between observations or experiments, explicit uncertainty-based weights can express those differences.

Hydrated gels can combine network viscoelasticity with fluid redistribution. Changing specimen size, drainage boundaries and loading geometry helps investigate the contributions. A structural rearrangement timescale and a diffusion time governed by drainage distance may respond differently to such changes. An exponential-looking trace alone does not identify a molecular reaction. A strong thickness dependence motivates examination of poroelastic or transport models, while systematic effects of temperature and chemical architecture can guide tests of segmental motion or reversible junctions. These comparisons give a fitted time parameter a more specific physical context.

## What can fitting recover from the available record?

The computation generates 1 s and 20 s ramp experiments with a known small noise level. Both use the same material parameters, and the fit includes their loading and holding stages together. The faster ramp preserves information about the fast arm that is weakened in the slower test. The long hold helps identify the slow arm and equilibrium contribution. The calculation asks whether one parameter set explains two known input histories. It retains observed values, fitted values and their differences so the answer can be inspected beyond a single goodness-of-fit number.

A residual plot shows observed minus fitted stress against time. Differences scattered around zero at approximately the noise scale indicate that the model captures the main trends of these constructed records. Consecutive deviations of one sign near the end of loading, or a persistent curved tail, suggest examining the time origin, strain history, baseline or an omitted process. An aggregate error can average over these localized structures. Keeping the residual plot reveals where agreement is strong and where a more specific explanation is needed.

![Finite-ramp joint fit, residuals, arm amplitudes and observation-window comparison for constructed data. Panel c shows suppression of original arm moduli when a hold is treated as a step. Panel d compares equal initial moduli but different long-time plateaus. Points are constructed observations; lines are model responses.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/fea81796025e0dad321d6da9.svg?v=fea81796025e)

Figure 3Finite-ramp joint fit, residuals, arm amplitudes and observation-window comparison for constructed data. Panel c shows suppression of original arm moduli when a hold is treated as a step. Panel d compares equal initial moduli but different long-time plateaus. Points are constructed observations; lines are model responses.

The amplitude comparison deliberately uses the same 20 s hold record. The correct model knows that reaching the final strain required 20 s. The alternative treatment regards the beginning of the hold as an instantaneous step. Its fitted arm amplitudes approach the contributions remaining after the ramp, rather than the original spring moduli. Placing these results beside each other shows how a processing assumption changes parameter meaning. A numerically close fit can answer a different physical question from the one the researcher intended.

The equilibrium plateau introduces a separate observation-window problem. The alternative parameter set shown in the figure has the same initial modulus and a similar early response but approaches a different long-time plateau. Observing only the first 5 s reveals little of that difference. Extending the record to hundreds of seconds separates the curves. If the application concerns contact pressure after hours, a few seconds of measurements need a corresponding extension in observation. Adding more fitted arms cannot manufacture the missing long-time information and can instead allow parameters to compensate for each other.

Separate variation among independent specimens from noise within one record. A thousand time points from one specimen are not a thousand independent samples of the material population. Fit several specimens separately to examine distributions of initial modulus, equilibrium contribution and timescales. Assessing uncertainty should preserve the relevant experimental unit and time correlation. Randomly resampling individual points can break the structure of correlated noise and create an overly narrow impression of parameter precision.

## Changing the controlled quantity changes the time response

To compare creep and relaxation, simplify the material to an equilibrium spring of 20 kPa in parallel with one Maxwell arm of 40 kPa and a relaxation time of 2 s. At fixed strain, total stress decreases as the Maxwell arm releases its contribution. At fixed total stress, load released by that arm must transfer to the equilibrium spring, so total strain increases. The difference is therefore more than a new vertical-axis label: the constraint on internal load redistribution has changed.

$$
J(t)=\frac{\varepsilon(t)}{\sigma_0}=\frac{1}{E_\infty}\left(1-\frac{E_1}{E_0}e^{-t/\tau_c}\right),\qquad E_0=E_\infty+E_1,\quad\tau_c=\tau\frac{E_0}{E_\infty}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/70f3dc39744c98269cbe57ad.svg) | Creep compliance of a one-arm standard linear solid, kPa⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time after an ideal stress step, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/dd72237021aa073cc29bdada.svg) | Current strain, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/465ea137606b4c7e2067f528.svg) | Applied and held stress, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/e3bc601649bd36677658617e.svg) | Positive equilibrium spring modulus, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/4527c7825889bcd00202ef22.svg) | Spring modulus of the sole Maxwell arm, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/89ba16e9e7f11a7da33694e2.svg) | Instantaneous modulus of this one-arm model, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | Maxwell-arm relaxation time, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/ba485d6196375f39459ba480.svg) | Creep retardation time under fixed stress, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | Base of the natural exponential. |

This is a separate one-arm example, not a direct substitution for the earlier two-arm model. Under constant total stress, released arm load transfers to the equilibrium spring. E∞ = 20 kPa, E1 = 40 kPa and τ = 2 s give τc = 6 s and J(2) = 0.0261156 kPa⁻¹, while 1/E(2) = 0.0288058 kPa⁻¹.

The creep retardation time of this one-arm solid is 6 s, compared with its 2 s relaxation time. Their ratio equals the initial modulus divided by the equilibrium modulus, which is three. At 2 s, creep compliance is approximately 0.02612 kPa⁻¹. Taking the reciprocal of the relaxation modulus at the same instant gives approximately 0.02881 kPa⁻¹. The values differ. At the instantaneous and long-time limits, both experiments approach their corresponding elastic responses and the reciprocal relation is recovered. The intermediate difference results from the evolving history and constraint.

![Separate one-arm standard linear solid with E∞ = 20, E1 = 40 kPa and τ=2 s. Creep compliance under fixed stress differs from the pointwise inverse relaxation modulus at intermediate times; creep retardation time is 6 s.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d3db85e820e59c0b972b635f.svg?v=d3db85e820e5)

Figure 4Separate one-arm standard linear solid with E∞ = 20, E1 = 40 kPa and τ=2 s. Creep compliance under fixed stress differs from the pointwise inverse relaxation modulus at intermediate times; creep retardation time is 6 s.

Predicting deformation under a fixed load from a relaxation test therefore requires an appropriate constitutive conversion, followed by comparison with creep measurements. Taking the reciprocal of every point on a relaxation curve gives the wrong intermediate response. For a material with several arms, the conversion involves coupled processes and is usually convenient to perform numerically. Start from the prescribed input history and calculate the response, rather than treating two quantities at the same clock time as if the material were a static spring.

The two experiments are valuable partners. A model that describes both declining force at fixed strain and increasing strain at fixed force provides a clearer interpretation of its parameters. If incompatible parameter sets are needed, examine specimen state, amplitude range, geometry and control quality. Applications that alternate between sustained load and displacement constraints require the whole sequence to be included. A material does not erase its prior loading history when the apparatus changes control mode.

## Connect the curve to a material’s task over time

In biomaterials, relaxation poses an engaging question: if two matrices are equally stiff initially, do cells experience the same resistance later? Cells exert forces through adhesions, and the surrounding network can maintain resistance or rearrange. In their 2016 alginate-hydrogel study, Chaudhuri and colleagues examined relaxation alongside initial modulus, adhesion-ligand density and other controlled variables in three-dimensional culture. This development expanded the mechanical description of a cellular environment from a single initial stiffness to a response that evolves over time.

An adhesion ligand is a molecular site through which a cell can attach to its surroundings. Faster redistribution of network stress changes the persistence of resistance after cellular force is applied and can affect local matrix remodeling. The figure uses constructed curves with equal initial moduli but different relaxation times, together with an original network sketch, to explain that comparison. These are conceptual illustrations rather than cell measurements. Cell type, culture dimensionality, ligand presentation and degradation conditions remain variables to match when designing a specific biological comparison.

![Original conceptual illustration: two specified models share initial and equilibrium moduli, while both timescales are five times larger in the slower model. Cell and junction sketches explain sustained traction and network rearrangement, rather than measured cells or predicted morphology.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9f6a9762184d7004f05fbf0b.svg?v=9f6a9762184d)

Figure 5Original conceptual illustration: two specified models share initial and equilibrium moduli, while both timescales are five times larger in the slower model. Cell and junction sketches explain sustained traction and network rearrangement, rather than measured cells or predicted morphology.

The same reasoning applies to seals and flexible devices. A gasket installed at fixed compression must retain sufficient contact pressure for the relevant temperature and duration. A soft support touching tissue may need to reduce sustained pressure while preserving structural support. There is no single preferred direction for relaxation speed across these uses. Express the functional requirement in terms of force, deformation and time, then choose the initial modulus, sustained contribution and timescales that address that requirement.

### Complete Python: finite ramps, shared-parameter fitting and creep

Two constructed records share a material model; retain raw quantities, fitted responses, residuals and one-arm creep results.

```
"""Stress relaxation with measured finite ramps and a generalized Maxwell model.
All numerical records are constructed teaching data, with fixed random seed.
python main.py --output results --language en
"""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import least_squares
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,FancyArrowPatch

PARAM=np.array([20.,40.,30.,2.,40.])  # kPa,kPa,kPa,s,s
EPS=.02
def response(t,ramp,q=PARAM,eps=EPS):
    """Uniaxial stress in kPa from initially unstressed material, t in seconds."""
    t=np.asarray(t,dtype=float);Ein,E1,E2,tau1,tau2=q
    u=np.minimum(np.maximum(t,0),ramp);hold=np.maximum(t-ramp,0)
    strain=eps*u/ramp;stress=Ein*strain
    for modulus,tau in [(E1,tau1),(E2,tau2)]:
        stress=stress+modulus*eps*tau/ramp*(-np.expm1(-u/tau))*np.exp(-hold/tau)
    return stress
def step(t,q=PARAM):
    Ein,E1,E2,tau1,tau2=q;t=np.asarray(t)
    return Ein+E1*np.exp(-t/tau1)+E2*np.exp(-t/tau2)
def apparent(q,ramp):
    Ein,E1,E2,t1,t2=q
    return np.array([Ein,E1*t1/ramp*(-np.expm1(-ramp/t1)),E2*t2/ramp*(-np.expm1(-ramp/t2)),t1,t2])

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();o=a.output;o.mkdir(parents=True,exist_ok=True);tr=lambda z,e:z if a.language=='zh' else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fbfcfc','savefig.facecolor':'#fbfcfc','text.color':'#18344a'})
    B='#186c94';G='#188777';O='#d27839';P='#8a5d92';K='#18344a'
    def save(f,n):
        f.savefig(o/f'{n}-{a.language}.svg',bbox_inches='tight');f.savefig(o/f'{n}-{a.language}.png',bbox_inches='tight',dpi=150);plt.close(f)
    rng=np.random.default_rng(1905);records=[]
    for ramp in [1.,20.]:
        t=np.unique(np.r_[np.linspace(0,ramp,51),ramp+np.geomspace(.05,400,180)])
        true=response(t,ramp);obs=true+rng.normal(0,.003,len(t));records.append((ramp,t,true,obs))
    def residual(q):return np.concatenate([response(t,r,q)-y for r,t,truth,y in records])
    fit=least_squares(residual,[18,35,33,3,35],bounds=([.1,.1,.1,.1,10],[100,200,200,10,200]),xtol=1e-13,ftol=1e-13,gtol=1e-13);assert fit.success
    q=fit.x
    r,t,true,y=records[1];mask=t>=r;h=t[mask]-r
    naive=least_squares(lambda v:EPS*step(h,v)-y[mask],[20,4,24,2,40],bounds=([.1,.01,.01,.1,10],[100,200,200,10,200]),xtol=1e-13,ftol=1e-13,gtol=1e-13);assert naive.success
    tt=np.linspace(0,20,401)
    sol=solve_ivp(lambda time,s:np.array([40.,30.])*EPS/20-s/np.array([2.,40.]),[0,20],[0,0],t_eval=tt,rtol=1e-11,atol=1e-13)
    ode=20*EPS*tt/20+sol.y.sum(axis=0);ode_error=float(np.max(np.abs(ode-response(tt,20))))
    # F1: original conceptual history and a matched mechanical network.
    f,ax=plt.subplots(1,3,figsize=(14,5),layout='constrained')
    for aa in ax:aa.set(xlim=(0,10),ylim=(0,10));aa.axis('off')
    ax[0].set_title(tr('a  1867：响应需要时间','a  1867: response takes time'))
    ax[0].add_patch(Rectangle((1,3),8,4,fill=False,ec=B,lw=2))
    for x,y,dx,dy in [(2,4,.8,.4),(4,5,-.7,.8),(6,4.3,.6,-.5),(8,6,-.8,-.4),(3,6,.6,.4),(7,5.8,-.7,-.8)]:
        ax[0].add_patch(Circle((x,y),.19,color=G));ax[0].annotate('',(x+dx,y+dy),(x,y),arrowprops={'arrowstyle':'->','color':G})
    ax[0].text(5,2,tr('Maxwell的气体动力学问题','Maxwell’s gas-dynamics question'),ha='center',fontsize=11)
    ax[0].text(5,1.2,tr('分子运动与宏观应力的联系','Molecular motion and macroscopic stress'),ha='center',fontsize=10)
    def spring(aa,x0,x1,y,color=B):
        x=np.linspace(x0+.18,x1-.18,13);ys=y+np.r_[0,np.tile([.35,-.35],5),.35,0]
        aa.plot([x0,x0+.18],[y,y],color=color,lw=2);aa.plot(x,ys,color=color,lw=2);aa.plot([x1-.18,x1],[y,y],color=color,lw=2)
    def dash(aa,x0,x1,y):
        aa.plot([x0,x0+.3],[y,y],color=G,lw=2)
        aa.plot([x1-.3,x0+.3,x0+.3,x1-.3],[y+.4,y+.4,y-.4,y-.4],color=G,lw=2)
        aa.plot([x1-.8,x1-.8],[y-.3,y+.3],color=G,lw=2);aa.plot([x1-.8,x1],[y,y],color=G,lw=2)
    ax[1].set_title(tr('b  串联：形变可以重新分配','b  Series: deformation can redistribute'))
    spring(ax[1],1,4,5);dash(ax[1],4,8.5,5)
    ax[1].text(2.5,6.2,'E',ha='center');ax[1].text(6.2,6.2,'η',ha='center')
    ax[1].text(5,3.5,tr('总伸长固定，弹簧逐渐回缩','Fixed total extension; spring recoils'),ha='center',fontsize=10)
    ax[1].text(5,2.5,'τ = η / E',ha='center',fontsize=15)
    ax[2].set_title(tr('c  并联：不同时间尺度分担载荷','c  Parallel: several load-bearing timescales'))
    ax[2].plot([1,1],[2.5,7.5],color=K,lw=2);ax[2].plot([9,9],[2.5,7.5],color=K,lw=2)
    spring(ax[2],1,9,7.5);spring(ax[2],1,4,5);dash(ax[2],4,9,5);spring(ax[2],1,4,2.5);dash(ax[2],4,9,2.5)
    ax[2].text(5,8.4,'E∞ = 20 kPa',ha='center');ax[2].text(5,5.9,'E₁ = 40 kPa, τ₁ = 2 s',ha='center',fontsize=10);ax[2].text(5,3.4,'E₂ = 30 kPa, τ₂ = 40 s',ha='center',fontsize=10)
    ax[2].text(5,.9,tr('现代力学类比；不是分子结构图','Modern mechanical analogy, not molecular structure'),ha='center',fontsize=9)
    save(f,'history')
    # F2: measured input and resulting load are inseparable.
    f,ax=plt.subplots(3,1,figsize=(11,10),layout='constrained');ts=np.linspace(0,100,1501)
    for ramp,c in [(1,B),(20,O)]:
        lab=tr('加载','Ramp')+f' {ramp:g} s';ax[0].plot(ts,100*EPS*np.minimum(ts/ramp,1),color=c,label=lab)
        ax[1].plot(ts,response(ts,ramp),color=c,label=lab)
    ax[0].set(xlabel=tr('从加载开始的时间 / s','Time from ramp start / s'),ylabel=tr('应变 / %','Strain / %'),xlim=(0,30));ax[0].legend()
    ax[1].plot(ts,EPS*step(ts),'--',color=G,label=tr('理想瞬时阶跃','Ideal instantaneous step'));ax[1].axhline(.4,color='#81939e',ls=':');ax[1].set(xlabel=tr('从加载开始的时间 / s','Time from ramp start / s'),ylabel=tr('应力 / kPa','Stress / kPa'));ax[1].legend()
    hold=np.linspace(0,120,600);app=apparent(PARAM,20)
    ax[2].stackplot(hold,np.full_like(hold,.4),EPS*app[1]*np.exp(-hold/2),EPS*app[2]*np.exp(-hold/40),colors=[G,B,O],alpha=.8,labels=[tr('长期分支','Equilibrium'),tr('快分支','Fast arm'),tr('慢分支','Slow arm')]);ax[2].set(xlabel=tr('20 s加载结束后的保持时间 / s','Hold time after the 20 s ramp / s'),ylabel=tr('应力分担 / kPa','Stress contributions / kPa'));ax[2].legend(loc='upper right',ncol=3)
    for aa,title in zip(ax,[tr('a  两次实验达到相同2%应变','a  Both experiments reach 2% strain'),tr('b  加载期间已经发生松弛','b  Relaxation starts during loading'),tr('c  保持阶段的不同承载路径','c  Load-bearing paths during the hold')]):aa.set_title(title,loc='left')
    save(f,'ramp')
    # F3: fitted results, residuals, and an exact explanation of apparent amplitudes.
    f,ax=plt.subplots(2,2,figsize=(13,9),layout='constrained')
    for r,t,true,y in records:
        c=B if r==1 else O;h=t-r;sel=h>=0;ax[0,0].scatter(h[sel],y[sel],s=9,color=c,alpha=.45);ax[0,0].plot(h[sel],response(t[sel],r,q),color=c,label=f'{r:g} s '+tr('加载','ramp'));ax[0,1].scatter(h[sel],(y-response(t,r,q))[sel]*1000,s=8,color=c,alpha=.55)
    ax[0,0].set_xscale('symlog',linthresh=.1);ax[0,1].set_xscale('symlog',linthresh=.1)
    ax[0,0].set(xlabel=tr('保持时间 / s','Hold time / s'),ylabel=tr('应力 / kPa','Stress / kPa'));ax[0,0].legend();ax[0,1].axhline(0,color=K,lw=1);ax[0,1].set(xlabel=tr('保持时间 / s','Hold time / s'),ylabel=tr('观测−拟合 / Pa','Observed − fitted / Pa'))
    ix=np.arange(3);ax[1,0].bar(ix-.24,PARAM[:3],.24,color=G,label=tr('指定模型','Specified'));ax[1,0].bar(ix,q[:3],.24,color=B,label=tr('有限加载联合拟合','Joint finite-ramp fit'));ax[1,0].bar(ix+.24,naive.x[:3],.24,color=O,label=tr('20 s保持段当作阶跃','20 s hold treated as a step'));ax[1,0].set(xticks=ix,xticklabels=['E∞','E₁','E₂'],ylabel=tr('分支模量 / kPa','Arm modulus / kPa'));ax[1,0].legend(fontsize=8.7)
    window=np.linspace(0,300,601);alt=np.array([5,40,45,2,60]);ax[1,1].plot(window,step(window),color=B,label='E∞=20, E₂=30, τ₂=40');ax[1,1].plot(window,step(window,alt),'--',color=P,label='E∞=5, E₂=45, τ₂=60');ax[1,1].axvspan(0,5,color=O,alpha=.2,label=tr('只观察前5 s','Only the first 5 s'));ax[1,1].set(xlabel=tr('理想阶跃后的时间 / s','Time after ideal step / s'),ylabel=tr('松弛模量 / kPa','Relaxation modulus / kPa'));ax[1,1].legend(fontsize=8.7)
    for aa,title in zip(ax.flat,[tr('a  两条输入历史共同识别模型','a  Joint fit to two input histories'),tr('b  残差保留时间结构供检查','b  Residuals reveal time structure'),tr('c  忽略加载会低估分支幅值','c  Ignoring the ramp suppresses amplitudes'),tr('d  短窗口看不清长期平台','d  A short window misses the plateau')]):aa.set_title(title,loc='left')
    save(f,'fit')
    # F4: an independent one-arm solid compares two controlled experiments.
    time=np.linspace(0,25,501);Er=20+40*np.exp(-time/2);J=(1-2/3*np.exp(-time/6))/20
    f,ax=plt.subplots(1,2,figsize=(12,4.8),layout='constrained');ax[0].plot(time,Er,color=B);ax[0].axhline(20,color=G,ls=':');ax[0].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('松弛模量 / kPa','Relaxation modulus / kPa'),title=tr('a  保持应变：应力逐渐减小','a  Fixed strain: stress decreases'))
    ax[1].plot(time,J,color=G,label=tr('蠕变柔量 J(t)','Creep compliance J(t)'));ax[1].plot(time,1/Er,'--',color=O,label='1 / E(t)');ax[1].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('柔量 / kPa⁻¹','Compliance / kPa⁻¹'),title=tr('b  保持应力：时间尺度也改变','b  Fixed stress: the timescale changes'));ax[1].legend();save(f,'creep')
    # F5: original conceptual link to time-dependent cell environments, no cell measurements.
    f,ax=plt.subplots(1,3,figsize=(14,4.6),layout='constrained');bt=np.geomspace(.05,300,400)
    for factor,c,lab in [(1,B,tr('较快','Faster')),(5,P,tr('较慢','Slower'))]:
        bq=PARAM.copy();bq[3:]*=factor;ax[0].semilogx(bt,step(bt,bq)/90,color=c,label=lab)
    ax[0].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('归一化模量 E(t)/E(0)','Normalized modulus E(t)/E(0)'),title=tr('a  相同初始模量，不同持续阻力','a  Same initial modulus, different persistence'));ax[0].legend()
    for aa,title,col in [(ax[1],tr('b  细胞通过黏附点牵拉网络','b  A cell pulls through adhesions'),B),(ax[2],tr('c  接点重排改变周围的应力','c  Junction rearrangement changes stress'),P)]:
        aa.set(xlim=(-3,3),ylim=(-3,3),aspect='equal');aa.axis('off');aa.set_title(title,fontsize=11)
        theta=np.linspace(0,2*np.pi,60);aa.fill(.9*np.cos(theta),.55*np.sin(theta),color='#e4b6a3');aa.add_patch(Circle((0,0),.24,color='#9a6d91'))
        for ang in np.linspace(0,2*np.pi,9)[:-1]:
            x,y=2.5*np.cos(ang),2.5*np.sin(ang);cx,cy=.9*np.cos(ang),.55*np.sin(ang);mx,my=(x+cx)/2,(y+cy)/2
            if aa is ax[2]:mx+=.18*np.sin(3*ang);my+=.16*np.cos(2*ang)
            aa.plot([cx,mx,x],[cy,my,y],color=col,lw=1.8);aa.add_patch(Circle((mx,my),.09,fc=O));aa.annotate('',(cx*.82,cy*.82),(cx*1.6,cy*1.6),arrowprops={'arrowstyle':'->','color':K})
        aa.text(0,-2.9,tr('机制示意，非显微观测','Mechanistic sketch, not microscopy'),ha='center',fontsize=9)
    save(f,'biology')
    arr=np.concatenate([np.c_[np.full(len(t),r),t,EPS*np.minimum(t/r,1),true,y,response(t,r,q),y*.01] for r,t,true,y in records])
    np.savetxt(o/'data.csv',arr,delimiter=',',header='ramp_s,time_s,strain,true_stress_kPa,observed_stress_kPa,fitted_stress_kPa,observed_force_N',comments='')
    np.savetxt(o/'parameters.csv',np.c_[PARAM,q,naive.x],delimiter=',',header='specified,finite_ramp_fit,hold_as_step_fit',comments='')
    np.savetxt(o/'creep.csv',np.c_[time,Er,J,1/Er],delimiter=',',header='time_s,relaxation_kPa,creep_compliance_per_kPa,inverse_relaxation_per_kPa',comments='')
    app20=apparent(PARAM,20);out={'specified_E0_kPa':90.,'specified_Einf_kPa':20.,'step_initial_stress_kPa':1.8,'equilibrium_stress_kPa':.4,'ramp1_peak_kPa':float(response(1,1)),'ramp20_peak_kPa':float(response(20,20)),'ramp20_apparent_E1_kPa':float(app20[1]),'ramp20_apparent_E2_kPa':float(app20[2]),'ramp20_apparent_E0_kPa':float(app20[:3].sum()),'fit_Einf_kPa':float(q[0]),'fit_E1_kPa':float(q[1]),'fit_E2_kPa':float(q[2]),'fit_tau1_s':float(q[3]),'fit_tau2_s':float(q[4]),'naive_E0_kPa':float(naive.x[:3].sum()),'naive_tau1_s':float(naive.x[3]),'naive_tau2_s':float(naive.x[4]),'residual_rms_Pa':float(np.sqrt(np.mean(residual(q)**2))*1000),'ode_max_error_kPa':ode_error,'one_arm_retardation_s':6.,'one_arm_J_at2_per_kPa':float((1-2/3*np.exp(-2/6))/20),'one_arm_inverseE_at2_per_kPa':float(1/(20+40*np.exp(-1))),'force_at_equilibrium_N':.004}
    (o/'summary.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out))
if __name__=='__main__':main()
```

The complete program generates two input histories, saves the corresponding strain, stress and force records, fits shared parameters and produces the displayed figures. An independent differential-equation calculation checks the finite-ramp expression. When substituting experimental data, retain continuous time, actual local strain and force before and after the ramp. Check area and units before deciding whether the constant-rate formula fits the measured loading. For a complicated strain history, the arm equations can be integrated directly using the observed changes instead of deleting the loading stage and resetting time.

The interactive experiment combines ramp duration, the fast-arm time constant and observation time. First keep material parameters fixed and increase the ramp from 1 s to 20 s to inspect the peak change. Then keep loading duration fixed and vary the fast timescale to see which processes the apparatus can preserve at the start of the hold. The display reports both the fraction of target strain reached and current stress, distinguishing ongoing loading from an established hold. At long observation times, the curves approach the same equilibrium contribution.

## Interactive: how much relaxation occurs during loading?

Keep E∞ = 20, E₁ = 40 and E₂ = 30 kPa, with τ₂ = 40 s and a target strain of 2%. Time starts when loading begins. Vary the ramp and fast process to compare strain, stress and peak response.

[Figure: Strain and stress versus time](https://ml-biomat.com/tutorials/experimental-methods/m05/en/#M05-plot)

Plan a relaxation study around the deformation and duration relevant to its use, then measure the actual loading history and examine amplitude range, environment and independent-specimen variation. Interpret original stress, normalized response and residuals together. Improve loading and early sampling when fast processes are poorly resolved; extend the hold and stabilize the baseline when the plateau is uncertain. To connect a fitted timescale to molecular rearrangement or liquid migration, add temperature, size or structural comparisons. Each adjustment supplies an observable that makes the time-dependent behavior more informative.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/M05.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Royal Society — Maxwell’s other equations](https://royalsociety.org/blog/2015/09/maxwells-other-equations/)

   Historical connection between Maxwell’s1867 gas dynamics and finite response times.
2. [Roylance — Engineering Viscoelasticity](https://ocw.mit.edu/courses/3-11-mechanics-of-materials-fall-1999/d173f95347f59d59dd9b7387ab4303e7_MIT3_11F99_visco.pdf)

   Series/parallel models, creep conversion, constant-rate loading and hereditary superposition.

   MIT OpenCourseWare; reference only,
3. [Bower — Small-Strain Viscoelastic Materials](https://solidmechanics.org/Text/Chapter3_6/Chapter3_6.php)

   Loading history, temperature and relaxation/creep definitions.

   Public textbook reference; no figures reproduced.
4. [TA Instruments RH111 — Linear Viscoelastic Region in Creep and Stress Relaxation](https://www.tainstruments.com/applications-notes/determining-the-linear-viscoelastic-region-in-creep-and-stress-relaxation-tests/)

   Checking linear amplitude ranges using normalized transient curves.

   Instrument application note; reference only.
5. [Chaudhuri et al. — Hydrogels with tunable stress relaxation regulate stem cell fate and activity](https://backoffice.biblio.ugent.be/download/8692536/8692544)

   Separately designing initial modulus and relaxation in the2016 study of three-dimensional alginate cell culture.

   Public author manuscript; technical reference, no figures/data reproduced.
6. [Righi and Balbi — Foundations of viscoelasticity and application to soft tissues mechanics](https://arxiv.org/abs/2108.08078)

   Further reading on nonlinear soft tissue models and finite ramps beyond linear theory.

   Open preprint; reference only, no figures reproduced.
