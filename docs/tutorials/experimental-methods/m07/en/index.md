# DMA: Reading viscoelasticity through oscillation

Source: https://ml-biomat.com/tutorials/experimental-methods/m07/en/
Language: en

Use two waveforms to understand storage, loss and phase, then connect fixtures and amplitude to spectra, loop energy and time–temperature superposition.

## Why slow pressing and rapid vibration feel different

A rubber shoe sole must support body weight while dissipating some mechanical energy at impact. A vibration pad must isolate a machine's motion while retaining enough load-bearing stiffness. A soft tissue scaffold encounters different timescales of cell traction and body movement. Each application asks how a material responds to repeated deformation: how much of the force is associated with elastic shape change, and how much is associated with internal motion and energy dissipation? Dynamic mechanical analysis, or DMA, answers this question by imposing small oscillations at a controllable pace. Its result is a response that depends on frequency, temperature and material state, rather than a hardness number detached from its conditions.

Imagine repeatedly pushing and pulling a door fitted with both a spring and a hydraulic closer. The spring's resistance depends mainly on how far the door has moved. The closer also responds to how quickly it moves. As the door passes its central position, displacement may be small while speed is greatest, placing the two contributions at different moments in the cycle. DMA uses this timing difference to separate the stress into a component synchronized with strain and a component shifted by a quarter-cycle. Storage modulus and loss modulus describe the sizes of these components. We will calculate them from complete waveforms rather than treating them as unexplained software outputs.

The oscillation need not be visible to the eye. A film with a 10 mm gauge length undergoing a strain amplitude of 0.2% moves through a displacement amplitude of just 0.020 mm, or 20 μm. The instrument must measure force, displacement and their timing at this scale, making gripping, dimensional measurements and phase calibration important. The same material can be tested in tension, compression, bending or shear, with different geometry conversions and modulus names. This chapter follows small-amplitude tension to establish one clear measurement geometry before transferring the reasoning to other fixtures. The illustrations distinguish what the instrument directly measures from the properties subsequently calculated.

![Original conceptual view from fixtures to signals. Film tension and three-point bending require different geometry conversions. Displacement, force and timing are recorded together. The drawn bending shape illustrates the loading mode rather than a measured displacement field.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/f5086ada5378f91327a564c0.svg?v=f5086ada5378)

Figure 1Original conceptual view from fixtures to signals. Film tension and three-point bending require different geometry conversions. Displacement, force and timing are recorded together. The drawn bending shape illustrates the loading mode rather than a measured displacement field.

## Fixtures define the deformation and sensors reveal the response

A DMA instrument combines a drive that applies periodic force or displacement, sensors that record the response, a fixture and a chamber controlling temperature or another environmental variable. Films and fibers often suit tension fixtures. Stiffer bars can be tested in three-point bending or cantilever bending, while soft blocks may suit compression or shear. The aim is stable specimen deformation with force and displacement inside the instrument's reliable measurement range. An extremely soft hydrogel placed in a fixture intended for bending hard plastics may produce a numerical result dominated by contact and gripping. Selecting the fixture is therefore part of defining the experiment's physical question.

In tension, force divided by cross-sectional area gives stress, and extension divided by gauge length gives strain. Bending also depends on beam length, width and thickness because material farther from the neutral plane experiences greater tension or compression. Common beam descriptions contain a cubic dependence on thickness, strongly amplifying thickness errors. A slightly warped specimen, uneven thickness or incorrectly recorded support span can produce a systematic modulus shift. Measuring dimensions at several positions addresses these errors directly. A sophisticated molecular interpretation is useful only after the geometry used to convert force and displacement has been checked.

A film in tension often needs a small static preload to prevent slack or buckling during the cycle. Compression requires stable contact without precompressing the specimen enough to substantially alter its pores or network. Preload and dynamic amplitude are distinct conditions. For hydrogels and tissues, hydration, immersion, temperature and equilibration time also belong in the experimental record. During a temperature sweep, the specimen takes time to reach the chamber temperature; its interior may temporarily differ from the sensor reading. Faster heating and thicker specimens make this difference more relevant. Choosing equilibration and heating conditions is consequently part of controlling the material state being measured.

Before a main sweep, vary oscillation amplitude at a selected temperature and frequency. A region in which the moduli remain approximately independent of amplitude is the linear viscoelastic range. At very small amplitudes, force or displacement can approach the noise floor. At large amplitudes, network rearrangement, slip, changing contact or damage can alter the response. Choose an amplitude within a reproducible plateau that still provides an adequate signal. This plateau is a property of the stated conditions, not a permanent label attached to the material. It can shift with temperature, frequency and hydration, so substantial changes in these conditions justify checking it again.

The instrument itself has inertia, compliance and time delays. Calibration with empty fixtures or reference materials helps identify these contributions, especially at high frequency or when the specimen is very soft. If the true phase difference is small, even a modest timing error between sensors can substantially affect the loss modulus. Raw waveforms reveal clipping, drift and higher harmonics, respectively suggesting range, baseline or nonlinear-response issues. Retaining raw signals alongside exported moduli makes an unusual data point traceable to the measurements that produced it. It also allows the assumptions used by an analysis routine to be examined directly.

Estimate signal size before testing. A cross-sectional area of 1 mm² and the example's stress amplitude of approximately 14422 Pa give a force amplitude of approximately 0.0144 N. A 10 mm gauge length at 0.2% strain amplitude gives a displacement amplitude of 20 μm. Comparing these estimates with sensor resolution and range helps assess the chosen geometry. A larger area increases force, and a longer gauge increases displacement at the same strain, but dimensions also affect mounting stability and temperature uniformity. Choose them for the actual fixture and specimen, rather than maximizing signal without considering the rest of the experiment.

## Read storage and loss from two sine waves

A circular motion provides a useful picture of a sine wave. Imagine a point moving uniformly around a circle and record its vertical position. The result rises and falls periodically. One complete turn corresponds to one cycle. Frequency counts cycles per second and is measured in hertz; angular frequency counts radians per second. A complete turn contains 2π radians, explaining the conversion between the two descriptions. Programming-library trigonometric functions use radians, so an angle stated in degrees must be converted before entering those functions. The same care is needed when an instrument exports frequency in Hz but a model expects angular frequency in rad/s.

$$
\varepsilon(t)=\varepsilon_0\sin(\omega t),\qquad \omega=2\pi f,\qquad P=\frac{1}{f}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dd72237021aa073cc29bdada.svg) | Engineering strain at time t, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | Strain amplitude, dimensionless; 0.2% corresponds to 0.002. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/2cb3a34686b80c6ea9a5a2e4.svg) | Angular frequency, rad/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | Frequency, Hz, or cycles per second. |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | Duration of one complete cycle, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | The circle constant, approximately 3.14159, dimensionless. |

A sine function describes repeated oscillation. At 10 rad/s, frequency is 10/(2π)≈1.592 Hz and the period is approximately 0.6283 s. A strain amplitude of 0.002 over a 10 mm initial gauge length corresponds to a 0.020 mm displacement amplitude.

When strain varies sinusoidally, a linear viscoelastic material produces a steady-state stress oscillating at the same frequency, with its peak occurring at a different time. In the convention used here, stress leads strain by a positive phase angle; equivalently, strain lags stress. Phase measures a time difference using the cycle as its ruler. A stress peak occurring a quarter-cycle before the strain peak corresponds to a 90° phase difference. An in-phase response resembles an ideal spring, while a quarter-cycle difference resembles an ideal viscous element. Real materials commonly lie between these limits, with the angle changing as the observation frequency changes.

Expanding the phase-shifted stress produces a sine term synchronized with strain and a cosine term synchronized with the rate of strain. Sine and cosine act like two perpendicular measuring directions, allowing the contributions to be identified separately. Dividing the first coefficient by strain amplitude gives storage modulus; dividing the second gives loss modulus. The single and double primes distinguish these two quantities. They are not derivatives and do not refer to first and second experimental runs. The decomposition follows from the geometry of periodic signals, giving the software outputs a direct connection to observable waveforms.

$$
\sigma(t)=\varepsilon_0\!\left[E^{\prime}\sin(\omega t)+E^{\prime\prime}\cos(\omega t)\right],\quad E^{\prime}=\frac{\sigma_0}{\varepsilon_0}\cos\delta,\quad E^{\prime\prime}=\frac{\sigma_0}{\varepsilon_0}\sin\delta,\quad \tan\delta=\frac{E^{\prime\prime}}{E^{\prime}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ff305b24b1ce5e15f22817d6.svg) | Periodic stress, Pa; used for a steady small-amplitude linear response. |
| ![Formula](https://ml-biomat.com/static/agent-math/465ea137606b4c7e2067f528.svg) | Total stress amplitude, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | Strain amplitude, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/aafc579e21c51bd7eea76db7.svg) | Tensile storage modulus, Pa; the prime is a label. |
| ![Formula](https://ml-biomat.com/static/agent-math/cc2062badd373b0f0dcf4479.svg) | Tensile loss modulus, Pa; the double prime is a label. |
| ![Formula](https://ml-biomat.com/static/agent-math/e5b7c4267da3b3fe02d6ae1a.svg) | Phase angle by which stress leads strain; trigonometric functions use rad. |
| ![Formula](https://ml-biomat.com/static/agent-math/7cfe4f0d59119c3e45744c16.svg) | Loss factor, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/2cb3a34686b80c6ea9a5a2e4.svg) | Angular frequency, rad/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time, s. |

A phase-leading sine separates into an in-phase sine component and a quadrature cosine component. For E′=6 MPa and E″=4 MPa, tanδ=2/3 and δ≈33.69°. At a strain amplitude of 0.002, total stress amplitude is approximately 14422 Pa.

For a storage modulus of 6 MPa, loss modulus of 4 MPa and strain amplitude of 0.002, the in-phase stress amplitude is 12000 Pa and the cosine-component amplitude is 8000 Pa. The total stress amplitude is the square root of the sum of their squares, approximately 14422 Pa. The components do not reach their maxima at the same moment, so adding them to obtain 20000 Pa would be incorrect. The loss factor is 4/6, approximately 0.667, and the phase angle is approximately 33.69°. These values connect the waveforms, elliptical loop and energy calculation throughout the example.

![Strain and stress from one constructed experiment at 0.2% strain amplitude and 10 rad/s. The stress contains fixed-seed noise and a 120 Pa baseline offset. The fit estimates sine, cosine and constant coefficients together.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/3ba96265a394da0686dbfe66.svg?v=3ba96265a394)

Figure 2Strain and stress from one constructed experiment at 0.2% strain amplitude and 10 rad/s. The stress contains fixed-seed noise and a 120 Pa baseline offset. The fit estimates sine, cosine and constant coefficients together.

Retain the deformation mode when discussing a modulus. Tension and appropriate compression or bending measurements usually report E′ and E″, whereas shear reports G′ and G″. The quantities share stress units but describe different deformation modes. Conversion between tensile and shear moduli requires the relevant continuum assumptions and a suitable Poisson-ratio relation. Strongly anisotropic fibers, complex porous structures and heterogeneous tissues may not satisfy a simple conversion. Treating a number from one geometry as a direct measurement in another geometry can therefore discard important information about how the specimen carried the load.

## Fold the time axis into a loop and see the dissipated energy

A waveform plot places strain and stress separately against time. Another view uses strain as the horizontal coordinate and simultaneous stress as the vertical coordinate, connecting points in time order. A purely elastic material travels back and forth along a straight line: energy supplied during loading returns during unloading. A linear viscoelastic material generally traces an ellipse, taking different paths during loading and unloading. Its enclosed area corresponds to mechanical energy dissipated per cycle per unit volume. This stress–strain Lissajous view turns the timing difference between signals into a visible geometric area.

Why does that area represent energy? Force multiplied by displacement is work. Stress multiplied by strain is work divided by specimen volume. Summing small products of stress and strain change around one cycle gives the loop integral. Use dimensionless strain, such as 0.002, in this calculation rather than the plotted percent value of 0.2. Integrating directly in percent coordinates introduces a factor of one hundred. With stress in pascals, the resulting energy density can be expressed in Pa, equivalent to J/m³. This dimensional check links the geometry of the plot to the mechanical meaning of its area.

$$
W_{\mathrm{diss}}=\oint\sigma\,\mathrm{d}\varepsilon=\pi E^{\prime\prime}\varepsilon_0^2,\qquad W_{\mathrm{ref}}=\frac12 E^{\prime}\varepsilon_0^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/338bcad567736ca2de614709.svg) | Dissipated energy density per cycle, J/m³. |
| ![Formula](https://ml-biomat.com/static/agent-math/f028f6920f65d3c579388781.svg) | Integration around one complete stress–strain cycle. |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | Instantaneous stress, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/69d9e6d74063f2d3721f88c4.svg) | An infinitesimal engineering-strain change, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | The circle constant, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/cc2062badd373b0f0dcf4479.svg) | Loss modulus, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/aafc579e21c51bd7eea76db7.svg) | Storage modulus, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/d803bb703ed4a2c6ec1d36b1.svg) | Strain amplitude, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/a9ccced5783ddc69fc9d8592.svg) | Conventional elastic energy scale defined from storage modulus, J/m³. |

These expressions describe small-amplitude steady sinusoidal linear response. Stress multiplied by strain has energy-per-volume dimensions. E″=4000000 Pa and ε₀=0.002 give π×4000000×0.002²≈50.27 J/m³ dissipated per cycle. E′=6000000 Pa gives an elastic reference scale of 12 J/m³.

In the numerical example, a loss modulus of 4000000 Pa and strain amplitude of 0.002 produce a dissipated energy density of approximately 50.27 J/m³ per cycle. Doubling strain amplitude within the same linear range leaves the moduli unchanged but increases dissipation fourfold: both force amplitude and displacement amplitude increase. The storage modulus gives a conventional elastic energy scale of 12 J/m³. The loss factor compares moduli; it is not the percentage of input energy lost. Interpreting a loss factor of 0.667 as 66.7% energy loss mixes different definitions. The explicit loop calculation keeps each quantity connected to its actual meaning.

![The theoretical stress–strain loop encloses approximately 50.27 J/m³ dissipated per cycle; use dimensionless strain when calculating its area. Residuals of the noisy fit are arranged by phase on the right. Shading spans twice the prescribed noise standard deviation.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/ab08598d452c80a2d33d426c.svg?v=ab08598d452c)

Figure 3The theoretical stress–strain loop encloses approximately 50.27 J/m³ dissipated per cycle; use dimensionless strain when calculating its area. Residuals of the noisy fit are arranged by phase on the right. Shading spans twice the prescribed noise standard deviation.

The loop also offers a diagnostic shape. Small-amplitude steady sinusoidal loading produces an ellipse for a linear response. Pronounced corners, flattened sides or failure of successive cycles to overlap suggest checking nonlinearity, contact slip, baseline drift or an evolving material. System inertia can also alter phase at higher frequency, so the interpretation should incorporate instrument calibration. A larger area indicates more dissipation at the stated amplitude and frequency. Selecting a damping material additionally requires stiffness, working temperature, permissible deformation and heating to be considered. A single loss-factor ranking would hide these separate aspects of performance.

Dissipation can also be expressed per unit time. At 50.27 J/m³ per cycle and approximately 1.592 cycles per second, average dissipated power density is about 80 W/m³. This multiplies energy per cycle by cycles per second for steady repeated oscillation. It does not directly give temperature rise, which also depends on heat capacity, conduction and heat transfer to the surroundings. If sustained oscillation heats the specimen, its moduli may change in response, coupling thermal and mechanical behavior. Stabilizing specimen temperature therefore helps comparisons between frequencies represent the same material state rather than different degrees of self-heating.

## Change the pace and ask whether molecular motion can keep up

During slow deformation, many internal motions have time to occur. During rapid repeated deformation, the load direction may reverse before those adjustments are complete. Multiplying angular frequency by an internal relaxation time gives a dimensionless number comparing the two clocks. A small value means the internal process is fast relative to the imposed change. A large value means it is slow and approximately frozen within each cycle. Sweeping frequency while retaining the same material parameters is therefore like observing the material through different time windows. Processes that were combined in a single measurement can emerge as distinct features of the spectrum.

The teaching model contains an equilibrium spring in parallel with a Maxwell branch. The equilibrium spring preserves low-frequency stiffness. The spring and viscous element within the Maxwell branch share the response differently at different frequencies. At low frequency, viscous motion has time to release stress in that branch. At high frequency, the branch behaves more like an additional spring, raising storage modulus toward a higher plateau. Loss modulus peaks between the two limits because the external pace and internal adjustment time are then comparable. This is a clear starting point for understanding frequency spectra; real polymers often contain several such time-dependent processes.

$$
E^{\prime}(\omega)=E_{\mathrm{eq}}+E_1\frac{(\omega\tau)^2}{1+(\omega\tau)^2},\qquad E^{\prime\prime}(\omega)=E_1\frac{\omega\tau}{1+(\omega\tau)^2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a6bcebecca57a8b130798178.svg) | Storage modulus at angular frequency ω, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/e627d8d9ef684b3751f55a4f.svg) | Loss modulus at angular frequency ω, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/d8d43630c801e4462b1455e5.svg) | Equilibrium-spring modulus, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/4527c7825889bcd00202ef22.svg) | Spring modulus of the Maxwell branch, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/2cb3a34686b80c6ea9a5a2e4.svg) | Angular frequency, rad/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | Relaxation time of this Maxwell branch, s; distinct from creep retardation time. |

The equilibrium spring and Maxwell branch are in parallel, so their stresses add. With Eeq=2 MPa, E₁=8 MPa, τ=0.1 s and ω=10 rad/s, ωτ=1 and the moduli are E′=6 MPa and E″=4 MPa. The low-frequency storage plateau is 2 MPa; the high-frequency limit is 10 MPa.

Choose an equilibrium modulus of 2 MPa, branch modulus of 8 MPa and relaxation time of 0.1 s. At an angular frequency of 10 rad/s, corresponding to about 1.592 Hz, the dimensionless product is exactly one. The branch contributes 4 MPa to storage and 4 MPa to loss. Adding the equilibrium spring gives the 6 MPa and 4 MPa used in the preceding waveform example. This also shows why the loss peak, a crossing of the two moduli and the loss-factor peak need not occur at the same frequency. The equilibrium spring changes the denominator and plateau structure, so different spectral features require their own interpretation.

## Interactive experiment: Frequency, amplitude and the material clock

Watch the stress–strain loop. Frequency or relaxation time changes the moduli; changing amplitude within the linear model changes energy while retaining the moduli.

[Figure: Stress–strain loop](https://ml-biomat.com/tutorials/experimental-methods/m07/en/#M07-plot)

The interactive display combines the stress–strain loop with calculated moduli. Change frequency first and watch both the loop slope and opening. Then change strain amplitude alone: moduli remain fixed in the linear model while loop area changes with amplitude squared. Finally vary relaxation time to compare what the same external frequency means for different internal material clocks. Parameters, units and calculations match the chapter's equations. Adjusting these controls separately distinguishes a faster oscillation, a larger deformation and a slower material process, three changes that are easy to conflate when looking only at a final curve.

A frequency sweep also consumes experimental time. At a low frequency, even one cycle can last a long time, and several cycles may be needed to reach steady behavior. Meanwhile the specimen may dry, age, continue curing or recover its structure. Different results for increasing- and decreasing-frequency sweeps therefore justify checking whether the material changes during the experiment. Logarithmically spaced points can first cover a broad range, followed by denser sampling near a transition. This strategy preserves an overall view while concentrating observation time where additional resolution answers a specific question.

## Temperature changes the molecular clock

Heating commonly speeds segmental motion. A given oscillation frequency at a higher temperature may therefore correspond to a slower observation at a lower temperature. Twentieth-century polymer research developed this connection into time–temperature superposition: spectra at different temperatures can be shifted horizontally toward a reference temperature when their shapes are compatible. The relation published by Williams, Landel and Ferry in 1955 became a widely used description of the connection between temperature and relaxation speed in many glass-forming systems. Its historical significance lies in connecting experimentally accessible short windows with a wider range of material dynamics.

$$
\log_{10}a_T=-\frac{C_1(T-T_r)}{C_2+(T-T_r)},\qquad \tau(T)=a_T\tau(T_r),\qquad f_r=a_Tf
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/93f58a7269ddba173c110888.svg) | Horizontal shift factor relative to the reference temperature, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/be8ebdecd039424afe275a60.svg) | Base-ten logarithm. |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | Specimen temperature, here in °C. |
| ![Formula](https://ml-biomat.com/static/agent-math/1240a9baf3662030a4316b2e.svg) | Reference temperature, here in °C. |
| ![Formula](https://ml-biomat.com/static/agent-math/d959d9fd17553ff38c0ee430.svg) | WLF parameter, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/0c52ac7e99d50739d28c6ed2.svg) | WLF parameter with the same unit as the temperature difference, here °C. |
| ![Formula](https://ml-biomat.com/static/agent-math/7e17a6485dc3092a405bf22d.svg) | Relaxation time at temperature T, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/9c19e2c0b19966180a0b5b02.svg) | Relaxation time at the reference temperature, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | Measured frequency, Hz. |
| ![Formula](https://ml-biomat.com/static/agent-math/ace823c9792eb2dad5fee165.svg) | Equivalent frequency shifted to the reference temperature, Hz. |

Here aT is defined as a ratio of relaxation times, requiring compatible spectrum shapes under a consistent time shift. With teaching parameters C₁=8, C₂=80 °C and Tr=20 °C, T=40 °C gives log₁₀aT=−1.6 and aT≈0.0251. A reference relaxation time of 0.1 s becomes approximately 0.00251 s.

The example chooses a reference temperature of 20 °C and teaching parameters of 8 and 80 °C. Raising temperature to 40 °C gives a base-ten logarithm of the shift factor of −1.6, so the shift factor is approximately 0.0251. A reference relaxation time of 0.1 s then becomes approximately 0.00251 s at the higher temperature. The calculated spectra coincide after the corresponding horizontal frequency shift. These curves deliberately satisfy the model assumptions. The selected parameters are not universal constants for every polymer. An experimental application should state the reference temperature, fitted parameters and temperature range together.

![Frequency spectra, phase and time–temperature superposition come from the same standard linear solid. The lower panels use teaching parameters in the 1955 WLF relation to show how temperature changes the molecular clock, then apply the corresponding frequency shifts to form a master curve. Constructed model data.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/1d658a98828b0dffa4886ab7.svg?v=1d658a98828b)

Figure 4Frequency spectra, phase and time–temperature superposition come from the same standard linear solid. The lower panels use teaching parameters in the 1955 WLF relation to show how temperature changes the molecular clock, then apply the corresponding frequency shifts to form a master curve. Constructed model data.

Some systems do not permit every process to align using one set of shift factors. Crystallization, phase separation, continuing network reaction or changing water content can alter spectrum shape. Different temperature sensitivities among relaxation processes can do the same. Retaining such differences often reveals more about the material than forcing a smooth master curve. Compare overlapping frequency intervals and check whether storage and loss align simultaneously. DSC, mass measurements or structural characterization can then help investigate the origin of a mismatch. A shift is a physical hypothesis about how timescales change, rather than a purely graphical operation.

DMA is also used to identify mechanical changes around the glass transition. As segmental motion becomes more active, storage modulus commonly decreases while loss modulus and loss factor may pass through peaks. The onset of the storage decrease, the loss-modulus peak and the loss-factor peak are different definitions and generally give different temperatures. Frequency, heating rate, thermal history and hydration also affect the reading. Compare specimens using the same criterion under matching conditions. Discussing a DMA feature alongside the heat-capacity change measured by DSC can be informative when the distinct processes observed by the two methods remain explicit.

Water- or solvent-containing materials introduce another issue during temperature sweeps: composition may change. Water loss can stiffen some networks and alter phase organization or internal friction, so a scanned specimen may differ from its starting state. Comparing heating with cooling, or a first scan with a second, and checking mass or hydration under corresponding conditions helps distinguish reversible changes from reorganization. Biological tissues may additionally undergo thermal denaturation. The resulting temperature response can then be interpreted alongside the specimen's chemical and biological state, rather than assuming that every shift reflects a change in molecular motion alone.

## Calculate moduli from complete waveforms and connect them to use

The program generates strain and stress waveforms from known moduli and adds stress noise using a fixed seed. The analysis does not simply read back the generating parameters. It fits the noisy stress with sine, cosine and constant terms by least squares. The constant absorbs a baseline offset, while the other coefficients divided by strain amplitude give the two moduli. Pointwise data, fitted parameters, phase angle, loop integral and theoretical energy are exported together. Every final value can therefore be traced back to the waveform. These are explicitly constructed teaching records, allowing calculation errors to be distinguished from unknown properties of an experimental specimen.

Using complete cycles helps because ideal sine and cosine cross-contributions cancel over complete periods. Least squares can also analyze a record that does not align exactly with whole cycles, provided timing and frequency are retained correctly and drift or transients are checked. Immediately after applying a new frequency, the material may not yet have reached periodic steady state, so early cycles differ from later ones. Comparing amplitude and phase over successive cycles provides a concrete criterion for selecting an analysis interval. A visually smooth waveform alone does not establish that the response is stationary.

### Complete example: Waveform decomposition and loop energy

Fit noisy stress with sine, cosine and constant terms, independently integrate energy per cycle, and generate spectra with temperature shifts. All data are explicitly constructed and exported by the program.

```
"""DMA from complete waveforms: original constructed data and SI-unit analysis."""
from pathlib import Path
import argparse, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch


def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def moduli(omega, tau=0.1, equilibrium=2e6, branch=8e6):
    x=np.asarray(omega)*tau
    return equilibrium+branch*x*x/(1+x*x), branch*x/(1+x*x)


def shift_factor(temperature, reference=20., c1=8., c2=80.):
    difference=np.asarray(temperature)-reference
    return 10.**(-c1*difference/(c2+difference))


def main(output, language):
    from matplotlib import font_manager
    output.mkdir(parents=True,exist_ok=True)
    fonts={f.name for f in font_manager.fontManager.ttflist}
    cjk=next((n for n in ['Microsoft YaHei','Noto Sans CJK SC','SimHei'] if n in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':cjk if language=='zh' else 'DejaVu Sans','font.size':11,
      'svg.fonttype':'none','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,
      'axes.prop_cycle':plt.cycler(color=['#186e83','#cc7d3d','#8160a1','#3e876d']),
      'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5'})
    tr=lambda zh,en:zh if language=='zh' else _label(en)
    def save(fig,name):fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    omega,amplitude=10.,.002;storage,loss=moduli(omega)
    time=np.linspace(0,8*np.pi/omega,1600,endpoint=False)
    strain=amplitude*np.sin(omega*time)
    true_stress=amplitude*(storage*np.sin(omega*time)+loss*np.cos(omega*time))
    noise_sd=100.;offset=120.
    observed=true_stress+offset+np.random.default_rng(707).normal(0,noise_sd,time.size)
    design=np.c_[np.sin(omega*time),np.cos(omega*time),np.ones(time.size)]
    coefficients=np.linalg.lstsq(design,observed,rcond=None)[0]
    fit_storage,fit_loss=coefficients[:2]/amplitude
    predicted=design@coefficients;residual=observed-predicted
    phase=np.linspace(0,2*np.pi,2001)
    loop_strain=amplitude*np.sin(phase)
    loop_stress=amplitude*(storage*np.sin(phase)+loss*np.cos(phase))
    energy=float(np.pi*loss*amplitude**2)
    integrated=float(np.trapezoid(loop_stress,loop_strain))
    summary={'data_kind':'constructed teaching experiment','seed':707,
      'storage_Pa':float(storage),'loss_Pa':float(loss),'tan_delta':float(loss/storage),
      'phase_degrees':float(np.degrees(np.arctan2(loss,storage))),
      'energy_per_cycle_J_m3':energy,'integrated_energy_J_m3':integrated,
      'power_density_W_m3':energy*omega/(2*np.pi),'shift_at_40C':float(shift_factor(40)),
      'fitted_storage_Pa':float(fit_storage),'fitted_loss_Pa':float(fit_loss),
      'fitted_offset_Pa':float(coefficients[2]),'residual_sd_Pa':float(np.std(residual,ddof=3))}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    np.savetxt(output/'waveforms.csv',np.c_[time,strain,true_stress,observed,predicted,residual],delimiter=',',comments='',header='time_s,strain,true_stress_Pa,observed_stress_Pa,fitted_stress_Pa,residual_Pa')
    frequencies=np.geomspace(.01,100,241);w=2*np.pi*frequencies;sp,lp=moduli(w)
    np.savetxt(output/'spectrum.csv',np.c_[frequencies,sp,lp,lp/sp],delimiter=',',comments='',header='frequency_Hz,storage_Pa,loss_Pa,tan_delta')

    fig,axes=plt.subplots(1,3,figsize=(12,4.4),layout='constrained')
    for ax in axes:ax.set(xlim=(0,10),ylim=(0,10));ax.axis('off')
    a,b,c=axes
    a.set_title(tr('A  薄膜拉伸','A  Film tension'),loc='left',fontweight='bold')
    for y in [1.5,7.6]:a.add_patch(Rectangle((2.5,y),5,.8,facecolor='#8b9aa1'))
    a.add_patch(Rectangle((4,2.3),2,5.3,facecolor='#badbd9',edgecolor='#186e83',lw=2))
    a.add_patch(FancyArrowPatch((8,2.2),(8,7.8),arrowstyle='<->',mutation_scale=14,color='#cc7d3d',lw=2))
    a.text(8.5,5,tr('标距','Gauge'),rotation=90,ha='center');a.text(5,.35,tr('力 ÷ 面积 → 应力','Force ÷ area → stress'),ha='center',fontsize=10)
    b.set_title(tr('B  三点弯曲','B  Three-point bending'),loc='left',fontweight='bold')
    xs=np.linspace(1,9,101);ys=5-.8*np.sin(np.pi*(xs-1)/8)
    b.plot(xs,ys,color='#186e83',lw=8)
    for x in [1,9]:b.add_patch(Polygon([[x-.6,3.7],[x+.6,3.7],[x,4.8]],facecolor='#8b9aa1'))
    b.add_patch(FancyArrowPatch((5,8),(5,4.5),arrowstyle='-|>',mutation_scale=18,color='#cc7d3d',lw=2))
    b.text(5,2.6,tr('跨度、厚度决定换算','Span and thickness enter conversion'),ha='center',fontsize=10)
    b.text(5,.35,tr('图为变形与夹持概念示意','Conceptual deformation and fixture'),ha='center',fontsize=9)
    c.set_title(tr('C  同时记录两个信号','C  Record two signals together'),loc='left',fontweight='bold')
    for y,text,color in [(7,tr('位移 → 应变','Displacement → strain'),'#186e83'),(4.8,tr('力 → 应力','Force → stress'),'#cc7d3d'),(2.6,tr('时间差 → 相位','Time difference → phase'),'#8160a1')]:
        c.add_patch(Rectangle((.4,y-.4),9,1.3,facecolor='white',edgecolor=color,lw=1.5));c.text(4.9,y+.25,text,ha='center',va='center',fontsize=11)
    c.text(5,.35,tr('环境：温度、湿度、浸液','Environment: temperature, humidity, liquid'),ha='center',fontsize=9)
    save(fig,'measurement')

    fig,axs=plt.subplots(2,1,figsize=(11,6),sharex=True,layout='constrained')
    mask=time<2*2*np.pi/omega
    axs[0].plot(time[mask],strain[mask]*100,color='#186e83',lw=2.3)
    axs[0].set(ylabel=tr('应变 / %','Strain / %'),title=tr('A  受控应变：幅值 0.2%','A  Controlled strain: amplitude 0.2%'))
    axs[1].scatter(time[mask][::4],observed[mask][::4]/1000,s=9,color='#a9b5b7',label=tr('含噪声信号','Noisy signal'))
    axs[1].plot(time[mask],predicted[mask]/1000,color='#cc7d3d',lw=2,label=tr('正弦与余弦分解拟合','Sine–cosine fit'))
    axs[1].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('应力 / kPa','Stress / kPa'),title=tr('B  应力提前：相位约 33.69°','B  Stress leads: phase approximately 33.69°'))
    for ax in axs:ax.axhline(0,color='#b5c0c3',lw=.8);ax.grid(axis='x',alpha=.15)
    axs[1].legend(frameon=False,fontsize=9,ncols=2);save(fig,'waveforms')

    fig,axs=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
    axs[0].fill(loop_strain*100,loop_stress/1000,color='#186e83',alpha=.16)
    axs[0].plot(loop_strain*100,loop_stress/1000,color='#186e83',lw=2)
    axs[0].plot(loop_strain*100,storage*loop_strain/1000,color='#cc7d3d',ls='--',label=tr('储能分量','Storage contribution'))
    axs[0].set(xlabel=tr('应变 / %','Strain / %'),ylabel=tr('应力 / kPa','Stress / kPa'),title=tr('A  回线面积：50.27 J/m³ / 周期','A  Loop area: 50.27 J/m³ per cycle'));axs[0].legend(frameon=False,fontsize=9)
    axs[1].scatter((omega*time)%(2*np.pi),residual,s=7,alpha=.45,color='#8160a1')
    axs[1].axhline(0,color='#818e94',lw=1);axs[1].axhspan(-200,200,color='#8160a1',alpha=.08)
    axs[1].set(xlabel=tr('周期内相位 / rad','Phase within cycle / rad'),ylabel=tr('残差 / Pa','Residual / Pa'),title=tr('B  残差保留了周期结构吗','B  Does residual structure follow the cycle?'))
    save(fig,'energy')

    fig,axs=plt.subplots(2,2,figsize=(12,8.2),layout='constrained')
    axs[0,0].loglog(frequencies,sp/1e6,label="E′",lw=2);axs[0,0].loglog(frequencies,lp/1e6,label="E″",lw=2)
    axs[0,0].axvline(omega/(2*np.pi),color='#8d999e',ls=':',lw=1)
    axs[0,0].set(xlabel=tr('频率 / Hz','Frequency / Hz'),ylabel=tr('模量 / MPa','Modulus / MPa'),title=tr('A  单一松弛过程与平衡弹簧','A  One relaxation process and equilibrium spring'));axs[0,0].legend(frameon=False)
    axs[0,1].semilogx(frequencies,np.degrees(np.arctan2(lp,sp)),color='#8160a1',lw=2)
    axs[0,1].set(xlabel=tr('频率 / Hz','Frequency / Hz'),ylabel=tr('相位角 / °','Phase angle / °'),title=tr('B  相位随观察节奏变化','B  Phase depends on the observation pace'))
    for temp,color in [(0,'#186e83'),(20,'#cc7d3d'),(40,'#3e876d')]:
        at=shift_factor(temp);_,loss_t=moduli(w,tau=.1*at)
        axs[1,0].loglog(frequencies,loss_t/1e6,label=f'{temp} °C',color=color,lw=2)
        axs[1,1].loglog(frequencies*at,loss_t/1e6,color=color,lw=2,ls=['-',':','--'][temp//20],label=f'{temp} °C')
    axs[1,0].set(xlabel=tr('频率 / Hz','Frequency / Hz'),ylabel=tr('损耗模量 / MPa','Loss modulus / MPa'),title=tr('C  1955 WLF 关系：温度改变时钟','C  The 1955 WLF relation: changing the clock'));axs[1,0].legend(frameon=False,fontsize=9)
    axs[1,1].set(xlabel=tr('平移后频率 aT·f / Hz','Shifted frequency aT·f / Hz'),ylabel=tr('损耗模量 / MPa','Loss modulus / MPa'),title=tr('D  一致平移后形成主曲线','D  Consistent shifts produce a master curve'));axs[1,1].legend(frameon=False,fontsize=9)
    for ax in axs.flat:ax.grid(alpha=.13,which='major')
    save(fig,'spectrum')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en')
    a=p.parse_args();main(a.output,a.language)
```

After running the example, check that the noise-free moduli are 6 MPa and 4 MPa, the loss factor is two-thirds, the phase is approximately 33.69° and theoretical dissipation is approximately 50.27 J/m³ per cycle. Numerical integration should approach the theoretical energy as the time step becomes finer. Compare the noisy fit with the generating values and inspect residuals for periodic structure. Oscillations at twice or three times the applied frequency suggest further examination of nonlinear response or signal distortion. A numerical check with a physical meaning is more informative than confirming that a program successfully produced a curve.

For material selection, return storage modulus, loss modulus and loss factor to the intended conditions. A larger loss factor can result from greater loss or from lower storage modulus, with different implications for supporting a load. Tissue scaffolds additionally require consideration of cellular loading timescales, culture state and measurement geometry. Vibration pads require the relevant loading mode, operating frequency and temperature rise. A report retaining fixture, dimensions, preload, dynamic amplitude, frequency, temperature program, environment and independently tested specimen count presents the spectrum as evidence for a clearly defined material state.

Creep and DMA now connect time-domain and frequency-domain descriptions. Creep follows how deformation accumulates under a sustained load; DMA follows how a periodic response differs in phase from the imposed motion. Both study viscoelasticity, with different time windows, controlled quantities and analysis conditions. The next chapter transfers the phase concept to rotational and oscillatory rheology of liquids, pastes and gels, adding shear rate, yielding, wall slip and geometry selection. Understanding the path from raw signals to physical quantities makes those new instruments easier to approach: the essential question remains what was controlled, what was measured and how the two were related.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/M07.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [TA Instruments — DMA Basic Theory and Applications](https://www.tainstruments.com/wp-content/uploads/2020_DMA_Online_Training_Part_1.pdf)

   Instrument signals, phase, fixtures and linear amplitude ranges.
2. [TA Instruments — Introduction to DMA of Polymer Solids](https://www.tainstruments.com/applications-notes/introduction-to-dynamic-mechanical-analysis-and-its-application-to-testing-of-polymer-solids/)

   Storage/loss definitions and alternative glass-transition criteria.
3. [RepTate — LVE Theories](https://reptate.readthedocs.io/manual/Applications/LVE/Theory/theory.html)

   Frequency responses of Maxwell modes.
4. [RepTate — TTS Theories](https://reptate.readthedocs.io/manual/Applications/TTS/Theory/theory.html)

   Shift-factor definitions, reference temperature and spectrum-shape comparisons.
5. [Williams, Landel and Ferry (1955) — Temperature Dependence of Relaxation Mechanisms](https://doi.org/10.1021/ja01619a008)

   Original WLF paper and historical context.
6. [NumPy — numpy.linalg.lstsq](https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html)

   Least-squares interface used for the sine–cosine decomposition.
