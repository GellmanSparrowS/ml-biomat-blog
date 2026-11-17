# NMR: From nuclear spins to molecular structure

Source: https://ml-biomat.com/tutorials/experimental-methods/s06/en/
Language: en

Use real ethanol peak records to connect spin, chemical shift, coupling, time signals and integration, then extend the reasoning to polymers and proteins.

## How are the molecules connected inside a transparent solution?

Two clear liquids can look identical while containing very different molecules. A polymer solution may remain clear after a reaction that changes only a fraction of its side groups. Infrared spectroscopy can identify features associated with particular bonds, and chromatography can separate components. Nuclear magnetic resonance adds information about chemical environments, connections and relative amounts by observing atomic nuclei in a magnetic field. The name may recall magnetic resonance imaging in a hospital. Both methods share the physics of nuclear spins and magnetic resonance, but molecular spectroscopy focuses on chemical differences rather than constructing an image of locations inside the body.

Nuclear magnetic resonance is abbreviated NMR. A common proton spectrum observes hydrogen nuclei, while carbon spectra often observe the isotope carbon-13. Different nuclei have different spin properties and abundances, so they do not all contribute equally to the experiment. A useful first picture is a set of channels reporting molecular environments. Different environments respond at different positions, interactions split some channels into several lines, and areas can report relative numbers under appropriate conditions. The next step is to understand how these features arise from the actual measurement.

Ethanol provides a manageable example. It contains a methyl group, a methylene group and a hydroxyl group, conventionally written CH₃, CH₂ and OH. This small molecule connects chemical environment, splitting and integration while also introducing solvent exchange and referencing. We will read an open ethanol entry from BMRB and plot its deposited peak positions, heights and group integrals. A separate constructed time signal will explain Fourier transformation. The experimental records and teaching models serve different purposes, and an idealized line shape will remain clearly distinct from the deposited measurements.

The chapter moves from spins in a magnetic field through chemical shifts, couplings and time-domain signals to specimen preparation and quantitative acquisition. It then extends the reasoning to polymers, proteins and multidimensional spectra. This order lets you judge what a spectrum measures before memorizing a long table of chemical-shift ranges. It also helps identify which setting affects a comparison and which additional experiment could establish a missing connection.

## The field creates a difference; a radiofrequency pulse makes it observable

Spin is a quantum property of a nucleus, rather than a classical sphere rotating about its axis. Some nuclei also have a magnetic moment and interact with an applied magnetic field. For a spin-one-half nucleus, the field separates two spin energy levels. At thermal equilibrium, the lower-energy level contains slightly more nuclei. This small population difference produces a net magnetization when many nuclei are observed together. Placing a specimen in the magnet does not align every nucleus perfectly in one direction.

The behavior of the overall magnetization can be understood partly through a precession analogy. A tilted spinning top precesses around the vertical; magnetization also has a precession frequency in a magnetic field. This analogy describes collective motion without replacing the quantum description of nuclear spin. A radiofrequency magnetic field matched to the resonance can rotate the magnetization. A short pulse creates a transverse component whose subsequent motion induces an electrical signal in a receiving coil. The instrument detects the collective response of a large population, rather than photographing individual nuclei.

$$
\nu_0=\frac{\gamma}{2\pi}B_0
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/73e82b44155602b2e23ac25f.svg) | Larmor resonance frequency, Hz. |
| ![Formula](https://ml-biomat.com/static/agent-math/7db9474e1e95a533a1714618.svg) | Gyromagnetic ratio, rad s⁻¹ T⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | Pi, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/5926b97aed9157f3038e191c.svg) | Static magnetic-field strength, T. |

Interaction between magnetic moment and field sets the principal precession scale. For protons, γ/(2π)≈42.577 MHz/T, giving about 400.2238 MHz at 9.4 T; small environmental corrections produce chemical shifts.

![Original nuclear-induction schematic connects field, specimen, radiofrequency coil and reception, illustrating the physical relationship central to the 1946 work. The right panel uses the approximate proton gyromagnetic ratio; 9.4 T gives 400.22 MHz without specimen-specific electronic-shielding corrections.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/02022dd6bbecb0cb5c13aa14.svg?v=02022dd6bbec)

Figure 1Original nuclear-induction schematic connects field, specimen, radiofrequency coil and reception, illustrating the physical relationship central to the 1946 work. The right panel uses the approximate proton gyromagnetic ratio; 9.4 T gives 400.22 MHz without specimen-specific electronic-shielding corrections.

In 1946, Bloch and collaborators and Purcell and collaborators published independent observations of nuclear magnetic responses in condensed matter. Their approaches emphasized nuclear induction and resonance absorption, respectively, while addressing the same underlying phenomenon. Later observations that the same nucleus resonates at slightly different positions in different compounds turned a measurement of nuclear magnetism into a probe of chemical environment. The Fourier-transform magnetic-resonance work of Ernst and Anderson in 1966 then connected a pulsed time-domain observation to a broad frequency spectrum.

A “400 MHz NMR instrument” is normally named for the proton frequency at its magnetic field, not the frequency of every observed nucleus. For protons, the approximate proportionality is 42.577 MHz per tesla, so 9.4 T corresponds to about 400.22 MHz. Carbon-13 has a different gyromagnetic ratio and operates at another frequency in the same magnet. A stronger field increases chemical-shift separations expressed in hertz, while the useful separation of real signals also depends on linewidth, the specimen and acquisition conditions.

The strong static magnetic field remains present around the instrument. Follow the facility's requirements for metal objects, implanted devices and sample containers before approaching or inserting a specimen. For spectral interpretation, field uniformity within the specimen is especially important. If identical chemical environments at different positions experience different fields, their responses spread across a range of frequencies. Shimming adjusts the field distribution to reduce this contribution to broadening. The resulting line shape can then more closely reflect molecular relaxation and the intended experiment.

## Chemical shift: why use ppm, and why does the axis increase to the left?

Prepare a homogeneous solution in an appropriate solvent, use a clean tube of the required dimensions, and allow temperature to stabilize. Undissolved particles, bubbles and an unsuitable liquid column can disturb the local field and reduce reproducibility. A deuterated solvent reduces the overwhelming proton background of ordinary solvent and can provide a deuterium signal for field locking. Locking stabilizes the field, whereas referencing defines the chemical-shift origin. Residual solvent protons, water and impurities can still produce peaks. Identify those contributions before assigning every additional line to the target compound.

A nucleus does not experience the external field in isolation. The surrounding electrons respond to the field and modify the local magnetic environment. Different chemical structures therefore produce different resonance positions. The CH₂ group next to oxygen in ethanol and the more distant CH₃ group have different environments. Chemical shift expresses their frequency offset from a reference, divided by the reference frequency and scaled in parts per million. This normalization makes results from instruments with different magnetic fields easier to compare.

$$
\delta=10^6\frac{\nu-\nu_{\mathrm{ref}}}{\nu_{\mathrm{ref}}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e5b7c4267da3b3fe02d6ae1a.svg) | Numerical chemical shift in ppm. |
| ![Formula](https://ml-biomat.com/static/agent-math/5064898bae7c73820eaab47c.svg) | Target resonance frequency, Hz. |
| ![Formula](https://ml-biomat.com/static/agent-math/6a066baf94a113b7f4f0c8e7.svg) | Corresponding reference frequency, Hz. |
| ![Formula](https://ml-biomat.com/static/agent-math/93f6f3a1cafe345159e21225.svg) | Factor expressing the frequency ratio in parts per million. |

Compare target with reference and normalize by the field-dependent frequency scale. One ppm is 400 Hz at 400 MHz and 600 Hz at 600 MHz; 2 ppm is 800 or 1200 Hz. Solvent, temperature and referencing conditions must be matched or specified.

On a 400 MHz instrument, one ppm corresponds to 400 Hz; on a 600 MHz instrument, it corresponds to 600 Hz. Two environments separated by 2 ppm are therefore separated by 800 Hz on the first instrument and 1200 Hz on the second. Their ppm separation remains approximately the same while the hertz separation increases. Traditional NMR plots put higher chemical shifts on the left, so the horizontal values decrease toward the right. Read the tick labels before interpreting the direction of a change.

The reference is part of the experiment. Aqueous samples commonly use DSS, while TMS is familiar in organic solvents. Appropriate residual-solvent signals or an instrument referencing procedure can also establish the scale. Solvent, temperature, acidity and molecular interactions can change chemical shifts, so a database value should be read with its conditions. BMRB entry bmse000297 records 100 mM ethanol in D₂O at 298 K and pH 7.4, referenced to DSS and measured at approximately 400 MHz.

![Real public records from BMRB bmse000297, DOI 10.13018/BMSE000297, Madison Metabolomics Consortium. A and B preserve seven transition positions and heights; C preserves group integrals, with ratio about 1.4978. Conditions: 100 mM in D₂O, 298 K, pH 7.4, DSS reference. Sticks do not specify measured linewidth. Data used under BMRB public-domain policy.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/b9aa4a2be4d111d332fee26a.svg?v=b9aa4a2be4d1)

Figure 2Real public records from BMRB bmse000297, DOI 10.13018/BMSE000297, Madison Metabolomics Consortium. A and B preserve seven transition positions and heights; C preserves group integrals, with ratio about 1.4978. Conditions: 100 mM in D₂O, 298 K, pH 7.4, DSS reference. Sticks do not specify measured linewidth. Data used under BMRB public-domain policy.

The entry's assignment table places methylene protons near 3.645 ppm and methyl protons near 1.175 ppm. Its one-dimensional peak-group records use approximately 3.641 and 1.170 ppm. Atom assignments, group centers and individual split lines are different layers of a record, so their last digits need not match exactly. The figure preserves seven deposited transition positions and heights as vertical sticks and separately displays the two deposited integrals. A stick table supplies no continuous line shape or linewidth; those quantities will be assigned explicitly in the later teaching simulation.

Ethanol contains six hydrogens, so why do the main integrals here correspond to five? The hydroxyl hydrogen exchanges with the solvent and can be replaced by deuterium in D₂O. Its proton response also depends strongly on exchange conditions. The experiment observes the nuclei visible under the specified conditions, rather than assigning one peak automatically to every hydrogen in a molecular formula. Exchangeable hydrogens in proteins create related considerations. Solvent choice affects both the background and which atomic sites remain observable.

## Several lines can belong to one chemical environment

Why can several hydrogens share one chemical shift? Chemical symmetry is one reason, and molecular motion can also average environments. If positions exchange rapidly on the timescale relevant to their frequency difference, the observed response can approach an average. Slower exchange may broaden or separate features. Peak count therefore depends on molecular behavior and experimental conditions as well as a static structural drawing. In a variable-temperature experiment, consider solubility, chemical equilibria, exchange and temperature calibration together. A changing pattern becomes mechanistically useful when these accompanying changes are accounted for.

The ethanol methyl group commonly gives a triplet and the methylene group a quartet. These splittings arise mainly from scalar spin-spin coupling transmitted through chemical bonds. Different states of neighboring spins create several allowed transition frequencies for the observed group. In a simple first-order case, coupling to n equivalent spin-one-half neighbors produces n+1 lines. The methyl group has two neighboring methylene hydrogens, while the methylene group has three neighboring methyl hydrogens. Count the relevant equivalent coupled nuclei, rather than every atom that happens to be spatially nearby.

A triplet often approaches a 1:2:1 intensity pattern and a quartet a 1:3:3:1 pattern because the neighboring spin-state combinations occur with different multiplicities. The central categories have more combinations, much like grouping several binary outcomes by their total. This picture explains familiar simple patterns but is not a universal recipe for complex spectra. When the frequency separation of interacting environments becomes comparable to their coupling, strong-coupling effects can alter line positions and intensities. A more complete spin-system treatment is then needed.

The coupling constant, usually called J, is expressed in hertz. For the same molecular system and environment, it generally does not scale with magnetic field in the way that chemical-shift separation in hertz does. A splitting of about 7.1 Hz corresponds to approximately 0.0178 ppm at 400 MHz and 0.0118 ppm at 600 MHz. Increasing the field narrows the apparent coupling separation on a ppm axis while increasing the frequency separation of different chemical environments. Distinguish these scales when comparing instruments or interpreting an expanded multiplet.

Integration should cover the whole multiplet. The three methyl lines together represent three hydrogens, while the four methylene lines together represent two, giving an approximate 3:2 area ratio under suitable quantitative conditions. Line count and nucleus count are therefore different. The public ethanol entry records group integrals of 180.16 and 120.28, giving a ratio of approximately 1.498. This example connects chemical structure, the mechanism of splitting and area information without equating the number of visible lines with the number of hydrogen environments.

## Record a fading ensemble in time, then separate its frequencies

Acquisition duration and the interval between samples control different aspects of frequency information. A longer record helps distinguish nearby frequencies; a shorter sampling interval allows a wider frequency range. A resonance outside the selected receiver window can fold into an incorrect apparent location through aliasing, analogous to a filmed wheel appearing to rotate backward. Set the spectral window to include the relevant signals, reference and useful baseline regions, then expand the interesting region during analysis. Restricting acquisition too tightly around one expected peak can conceal the information needed to interpret it.

After a pulse, the receiver records an oscillating signal that decays with time, called the free induction decay or FID. Different resonances resemble instruments playing different pitches together: the first recording is their combined performance. Fourier transformation separates that time-domain signal into frequency components, producing spectral peaks. The musical comparison concerns frequency decomposition; the actual signal is electrical at radiofrequencies. The receiver commonly mixes it with a reference frequency, so the recorded oscillations represent frequency offsets rather than a plot directly sampled at several hundred megahertz.

$$
s(t)=\sum_j A_j\exp\!\left(-\frac{t}{T_{2,j}^{*}}\right)\exp\!\left[i(2\pi f_jt+\phi_j)\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a2e2af48082172a695b27ad4.svg) | Complex FID in relative signal units; real and imaginary parts represent two receiver components. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time after the pulse, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | Resonance-component index. |
| ![Formula](https://ml-biomat.com/static/agent-math/cb2c27f1e1ca2cb88caf17da.svg) | Initial amplitude of component j, same units as s. |
| ![Formula](https://ml-biomat.com/static/agent-math/819a2589289afcba11f6e5ce.svg) | Effective transverse decay time, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/ea0efbb08d1d6502e2a12fed.svg) | Frequency offset from the receiver carrier, Hz. |
| ![Formula](https://ml-biomat.com/static/agent-math/d417405b726871d27d560b21.svg) | Initial phase, rad. |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Imaginary unit, i²=−1, combining quadrature receiver components. |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | Pi, dimensionless. |

Sum rotating, decaying responses. With A=1, f=10 Hz, phase zero and T₂*=0.20 s, t=0.10 s completes one cycle and gives approximately 0.6065. This independent-exponential model requires extensions for complex exchange or strong coupling.

The complex notation keeps two receiver components, separated by a quarter cycle, in one expression. Think of the real part as a cosine channel and the imaginary part as a sine channel. This preserves both amplitude and phase without introducing a new physical substance. Each component's frequency controls peak position, its decay affects linewidth, and its phase determines the mixture of absorptive and dispersive line shapes after transformation. Correct phasing makes integration act on the intended absorption-like signal instead of including positive and negative distortions around a peak.

$$
\Delta\nu_{1/2}=\frac{1}{\pi T_2^{*}},\qquad \Delta\nu_{\mathrm{window}}=\frac{1}{\pi T_2^{*}}+L_B
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/411288fdedf35db5f14fc88d.svg) | Full width at half maximum of an ideal Lorentzian absorption line, Hz. |
| ![Formula](https://ml-biomat.com/static/agent-math/72f68daae778569b46b086fb.svg) | Exponential transverse decay time, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/d4f59fee1d2180f7d0e23a22.svg) | Full width after exponential weighting, Hz. |
| ![Formula](https://ml-biomat.com/static/agent-math/5a55bb6d12cadf2847f816c2.svg) | Additional broadening for the exponential window exp(−πLBt), Hz. |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | Pi, dimensionless. |

Fourier transformation of exponential decay gives a Lorentzian; multiplying exponentials adds decay rates. T₂*=0.20 s gives 1.59155 Hz, increasing to 4.59155 Hz with 3 Hz broadening. Finite acquisition, phase and other line-shape contributions affect real observations.

![A separately constructed first-order ethanol-like model uses 3:2 total areas, 7.1 Hz coupling and T₂*=0.20 s. A shows the real FID; B transforms the same data; C adds 3 Hz exponential broadening; D compares actual acquisition durations with equal zero filling. This is not the BMRB raw time-domain experiment.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/875a240f5de93ce7be89ac1d.svg?v=875a240f5de9)

Figure 3A separately constructed first-order ethanol-like model uses 3:2 total areas, 7.1 Hz coupling and T₂*=0.20 s. A shows the real FID; B transforms the same data; C adds 3 Hz exponential broadening; D compares actual acquisition durations with equal zero filling. This is not the BMRB raw time-domain experiment.

The effective transverse decay time T₂* includes molecular relaxation and contributions such as magnetic-field inhomogeneity. An ideal exponential decay produces a Lorentzian line. At T₂*=0.20 s, its full width at half maximum is approximately 1.59 Hz. A faster decay produces a broader frequency response. Acquisition duration also matters: a 2 s recording has an original frequency-grid spacing of about 0.5 Hz, whereas 0.25 s gives about 4 Hz. Appending zeros creates a denser interpolated frequency grid without extending the time actually observed.

A window function deliberately changes the weighting of time points. Multiplying an FID by a decaying exponential suppresses the later, often noise-dominated part while making the effective decay faster and the lines broader. This is a physical and mathematical tradeoff between signal-to-noise and resolution. The code shows unweighted and broadened spectra and enlarges two nearby teaching lines. Excessive smoothing can merge distinguishable components, while emphasizing the late signal can amplify noise and truncation ripples. Processing choices should follow the question being asked of the spectrum.

## Separate two neighboring resonances

Two teaching environments have equal areas and a fixed separation of 0.020 ppm. Change proton operating frequency, effective transverse decay time and processing broadening to inspect linewidth and separation in hertz. The ideal Lorentzian model includes no coupling or noise.

Light curves are the components; the dark curve is their sum. Total area is preserved. The reported full width belongs to each individual component; the mixed envelope width should not be substituted into the single-line formula.

The interactive experiment combines the separation of two equal-area lines with magnetic field, T₂* and additional exponential broadening. At fixed separation in ppm, changing the field changes the separation in hertz. Changing T₂* changes linewidth according to the decay model. The depth of the valley helps visualize whether the two responses remain distinguishable. Real resolution also includes noise, sampling, phase and coupled-spin behavior. The model isolates how field strength, coherence lifetime and processing each act on a pair of neighboring frequencies.

The time record should also be inspected before transformation. A truncated signal can end while coherent oscillations remain, introducing frequency-domain ringing. A receiver overload can distort the beginning of the FID, and an incorrect digital-filter treatment can introduce a phase problem. Some irregular spectra therefore originate before peak picking or baseline correction. Retaining the original time data preserves the opportunity to revisit these steps. A final image alone cannot recover the acquisition history that determined its frequency information.

## Before areas become amounts, allow magnetization to recover

Peak height and area answer different questions. If the same signal is spread over a broader frequency range, its maximum decreases while its complete area can remain unchanged. For equal-area Lorentzian peaks, doubling linewidth approximately halves the height. Comparing heights would then suggest a loss of material even though the modeled nucleus count is unchanged. Integration adds the response over frequency and is closer to an amount measure when boundaries, baseline and overlap are handled appropriately. The database stores heights and integrals separately for this reason, and the real-data figure preserves that distinction.

A pulse changes magnetization, and longitudinal magnetization gradually returns toward equilibrium before the next excitation. This recovery is characterized by T₁, distinct from T₂ or T₂*, which describe transverse coherence decay. If pulses repeat too quickly, some environments are excited again before they have recovered. Different T₁ values then suppress signals by different fractions. Peak positions and shapes can look convincing while their area ratio is biased. Quantitative NMR requires acquisition conditions that make the responses being compared appropriately proportional to their nucleus counts.

$$
\frac{M_z(T_R)}{M_0}=1-\exp\!\left(-\frac{T_R}{T_1}\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6e0da5546ff4ab95a469ed95.svg) | Longitudinal magnetization after TR following complete saturation, same units as M₀. |
| ![Formula](https://ml-biomat.com/static/agent-math/d0d1f9424f5849a25d3f4fc5.svg) | Equilibrium longitudinal magnetization, magnetization units. |
| ![Formula](https://ml-biomat.com/static/agent-math/2d2c1f807c495a8c8c5b65ee.svg) | Recovery or repetition time in the ideal model, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/d3e6eda1d26b8ec9a05d7509.svg) | Longitudinal recovery time constant, s. |

The difference from equilibrium decays exponentially. TR=T₁ restores 63.212%, and TR=5T₁ restores 99.326%. Actual repeated-excitation response depends on flip angle, acquisition and delay.

In an ideal single-exponential recovery from complete saturation, waiting one T₁ restores about 63.2 percent of the equilibrium magnetization, while waiting five T₁ restores about 99.3 percent. If two signals have T₁ values of 1 and 3 s and the repetition interval is 1 s, their recovery fractions are approximately 0.632 and 0.283. Their ratio is substantially distorted. Flip angle, acquisition time and delay all contribute to a real repeated-pulse experiment. Measure relevant T₁ values or verify that extending the repetition interval stabilizes the ratio required for quantification.

$$
c_x=c_r\,\frac{I_x/n_x}{I_r/n_r}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8fb2d8dc0b2a5dd5e304e5a9.svg) | Analyte and calibrant concentrations in the same units, mmol/L here. |
| ![Formula](https://ml-biomat.com/static/agent-math/3c884cfbe6a36b0e2dde4337.svg) | Analyte and calibrant multiplet integrals on a common scale. |
| ![Formula](https://ml-biomat.com/static/agent-math/3aa2459b6287126e02028e14.svg) | Number of nuclei contributed per analyte or calibrant molecule to the chosen group, dimensionless. |

Divide area by nuclei per molecule, then compare the molecule-proportional responses. Ix=120, nx=3, Ir=80, nr=2 and cr=5 mmol/L give cx=5 mmol/L. Comparable response, adequate recovery, resolved assignments and calibrant purity are required.

A calibrant of known concentration converts nucleus-normalized integral ratios into concentration ratios. Suppose the target integral is 120 and represents three protons per molecule, while the calibrant integral is 80 and represents two. Dividing by their nucleus counts gives 40 for each. If the calibrant is 5 mmol/L, the target is also 5 mmol/L. A useful calibrant is compatible, stable, of known purity and spectrally separated from the analyte. A chemical-shift reference sets a frequency origin; a quantitative calibrant establishes amount. Their roles remain distinct even when one compound can serve both.

![Teaching model of recovery from ideal complete saturation. Two environments have T₁ of 1 s and 3 s and a true nucleus-count ratio of 3/2. Short repetition converts unequal recovery into integral-ratio bias. Equal excitation and detection efficiencies isolate why quantitative acquisition must consider recovery time.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/8dd736bb64a9fb3d7f432378.svg?v=8dd736bb64a9)

Figure 4Teaching model of recovery from ideal complete saturation. Two environments have T₁ of 1 s and 3 s and a true nucleus-count ratio of 3/2. Short repetition converts unequal recovery into integral-ratio bias. Equal excitation and detection efficiencies isolate why quantitative acquisition must consider recovery time.

Integration boundaries and the baseline influence the result. A narrow region misses line tails, while a broad region can include neighboring peaks or baseline offsets. Define consistent multiplet boundaries across a comparison. Solvent suppression can reveal signals obscured by strong solvent response but may also affect nearby analyte resonances. Routine proton-decoupled carbon spectra have additional intensity dependencies, including relaxation and nuclear Overhauser effects, so their heights or areas should not automatically be read like a quantitative proton spectrum. Decide the quantitative objective before selecting pulses, delays and processing.

### Read real peak records, construct an FID and examine processing and quantification

The program reads positions, heights and integrals from the bundled original NMR-STAR record and separately builds labeled time-signal and recovery models, exporting every figure and table.

```
"""Real BMRB peak records and separate NMR time-domain teaching models.
python main.py --output results --language en
Data: BMRB bmse000297, DOI 10.13018/BMSE000297, public-domain archive.
The generated FIDs are simulations; they are not the deposited raw experiment.
"""
from pathlib import Path
import argparse,json,re,shlex
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Ellipse

p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True);zh=a.language=='zh'
def tr(z,e):return z if zh else e
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','text.color':'#263d49','axes.labelcolor':'#263d49','axes.edgecolor':'#9bacb1','svg.fonttype':'path'})
blue,teal,coral,gold,gray='#265f85','#078579','#d6604d','#bb9033','#84969b'
def save(f,n):
 for item in f.findobj(matplotlib.text.Text):
  value=item.get_text()
  for old,new in [('₂',r'$_2$'),('₃',r'$_3$'),('₁',r'$_1$'),('⁻¹',r'$^{-1}$')]:value=value.replace(old,new)
  item.set_text(value)
 f.savefig(out/f'{n}-{a.language}.svg',bbox_inches='tight');f.savefig(out/f'{n}-{a.language}.png',dpi=155,bbox_inches='tight');plt.close(f)
def title(ax,l,z,e):ax.set_title(l+'  '+tr(z,e),loc='left',weight='bold',pad=14)

text=(Path(__file__).parent/'data'/'bmse000297.str').read_text(encoding='utf8')
frame=text.split('save_spectral_peak_1H',1)[1].split('\nsave_',1)[0]
def table(category):
 for content in re.findall(r'loop_\s*(.*?)\s*stop_',frame,re.S):
  tokens=shlex.split(content);n=0
  while n<len(tokens) and tokens[n].startswith('_'):n+=1
  columns=tokens[:n]
  if columns and columns[0].startswith(category+'.'):
   assert (len(tokens)-n)%n==0
   return [dict(zip(columns,tokens[i:i+n])) for i in range(n,len(tokens),n)]
 raise ValueError(category)
pos={r['_Spectral_transition_char.Spectral_transition_ID']:float(r['_Spectral_transition_char.Chem_shift_val']) for r in table('_Spectral_transition_char')}
height={r['_Spectral_transition_general_char.Spectral_transition_ID']:float(r['_Spectral_transition_general_char.Intensity_val']) for r in table('_Spectral_transition_general_char')}
areas={r['_Peak_general_char.Peak_ID']:float(r['_Peak_general_char.Intensity_val']) for r in table('_Peak_general_char')}
lines=np.array([[pos[k],height[k]] for k in pos]);actual_ratio=areas['2']/areas['1']

fig,axs=plt.subplots(1,2,figsize=(11.6,5.2));ax=axs[0];ax.set_xlim(0,10);ax.set_ylim(0,7);ax.axis('off')
ax.add_patch(Rectangle((.2,.5),1.4,5.9,fc='#dce5e8',ec=gray));ax.add_patch(Rectangle((8.4,.5),1.4,5.9,fc='#dce5e8',ec=gray));ax.text(.9,3.4,'N',ha='center',fontsize=20);ax.text(9.1,3.4,'S',ha='center',fontsize=20)
for y in [1.6,3.4,5.2]:ax.annotate('',xy=(8.1,y),xytext=(1.9,y),arrowprops={'arrowstyle':'->','color':gray,'lw':1})
ax.add_patch(Rectangle((4.65,1.2),.7,4.8,fc='#e9f4f2',ec=teal,lw=2));ax.text(5,6.3,tr('样品管','Sample tube'),ha='center',fontsize=10)
for y in np.linspace(2.4,4.7,5):ax.add_patch(Ellipse((5,y),2,.35,fill=False,ec=blue,lw=1.8))
ax.plot([6,7,7],[3.5,3.5,.6],color=blue,lw=2);ax.text(6.3,.25,tr('射频脉冲 / 感应接收','RF pulse / induction receiver'),ha='center',fontsize=9)
title(ax,'A','核感应的实验关系','Nuclear-induction experiment')
ax=axs[1];B=np.linspace(0,12,100);ax.plot(B,42.577*B,color=teal,lw=3);ax.scatter([9.4],[42.577*9.4],color=coral,s=55,zorder=3);ax.annotate('9.4 T → 400.22 MHz',(9.4,42.577*9.4),xytext=(3,460),arrowprops={'arrowstyle':'->','color':gray},fontsize=10);ax.set(xlabel=tr('磁场 / T','Magnetic field / T'),ylabel=tr('质子共振频率 / MHz','Proton resonance frequency / MHz'),xlim=(0,12),ylim=(0,540));title(ax,'B','磁场决定主要频率尺度','Field sets the principal frequency scale')
fig.text(.5,.01,tr('1946 年凝聚态核磁研究连接磁场、射频与感应信号。原创功能示意，非历史设备复原。','The 1946 condensed-matter experiments connected field, radiofrequency and induction. Original functional schematic, not a historical reconstruction.'),ha='center',fontsize=9);fig.tight_layout(rect=[0,.08,1,1]);save(fig,'induction')

fig,axs=plt.subplots(1,3,figsize=(12.2,4.5),gridspec_kw={'width_ratios':[1,1,.9]})
for ax,mask,lim,z,e in [(axs[0],lines[:,0]>2,(3.70,3.58),'CH$_2$：四条分裂线','CH$_2$: four split lines'),(axs[1],lines[:,0]<2,(1.23,1.10),'CH$_3$：三条分裂线','CH$_3$: three split lines')]:
 v=lines[mask];ax.vlines(v[:,0],0,v[:,1],color=blue if mask[0] else teal,lw=3);ax.scatter(v[:,0],v[:,1],s=22,color=blue if mask[0] else teal);ax.set(xlim=lim,ylim=(0,36),xlabel=tr('化学位移 / ppm','Chemical shift / ppm'),ylabel=tr('记录的峰高 / 原条目单位','Deposited peak height / entry units'));title(ax,'A' if ax is axs[0] else 'B',z,e)
axs[2].bar([0,1],[areas['1'],areas['2']],color=[blue,teal],width=.6);axs[2].set(xticks=[0,1],xticklabels=['CH$_2$','CH$_3$'],ylabel=tr('记录的峰组积分 / 原条目单位','Deposited group integral / entry units'),ylim=(0,220));axs[2].text(0,areas['1']+4,f"{areas['1']:.2f}",ha='center');axs[2].text(1,areas['2']+4,f"{areas['2']:.2f}",ha='center');title(axs[2],'C',f'面积比 {actual_ratio:.4f}',f'Area ratio {actual_ratio:.4f}')
fig.text(.5,.01,tr('真实峰表：BMRB bmse000297 · D$_2$O，100 mM，298 K，pH 7.4，DSS 参照。竖线不表示实测线宽。','Real peak records: BMRB bmse000297 · D$_2$O, 100 mM, 298 K, pH 7.4, DSS reference. Sticks do not specify measured linewidth.'),ha='center',fontsize=9);fig.tight_layout(rect=[0,.08,1,1]);save(fig,'ethanol')

# Construct a first-order ethanol-like FID with known areas and relaxation.
mhz=400.;carrier=2.4;j=7.1;dt=1/4000;N=8192;t=np.arange(N)*dt
freq=np.r_[((1.170-carrier)*mhz)+j*np.array([-1,0,1]),((3.641-carrier)*mhz)+j*np.array([-1.5,-.5,.5,1.5])]
amplitude=np.r_[3*np.array([1,2,1])/4,2*np.array([1,3,3,1])/8];T2=.2
fid=np.sum(amplitude[:,None]*np.exp(2j*np.pi*freq[:,None]*t[None,:])*np.exp(-t[None,:]/T2),axis=0)
rng=np.random.default_rng(560);noisy=fid+.015*(rng.normal(size=N)+1j*rng.normal(size=N))
def fft(data,lb=0):
 v=data.copy()*np.exp(-np.pi*lb*t[:len(data)]);v[0]*=.5
 f=np.fft.fftshift(np.fft.fftfreq(32768,dt));s=2*dt*np.fft.fftshift(np.fft.fft(v,n=32768)).real
 return f/mhz+carrier,s
ppm,spectrum=fft(noisy);_,broadened=fft(noisy,3);_,ideal=fft(fid)
group=lambda low,high:np.trapezoid(ideal[(ppm>=low)&(ppm<=high)],x=ppm[(ppm>=low)&(ppm<=high)]*mhz)
simratio=group(.8,1.5)/group(3.3,4.0)
fig,axs=plt.subplots(2,2,figsize=(11.6,7.7))
mask=t<.06;axs[0,0].plot(t[mask]*1000,noisy.real[mask],color=blue,lw=.9);axs[0,0].set(xlabel=tr('脉冲后时间 / ms','Time after pulse / ms'),ylabel=tr('FID 实部 / 相对单位','Real FID / relative units'));title(axs[0,0],'A','先记录时间合奏','Record the time-domain ensemble')
axs[0,1].plot(ppm,spectrum,color=teal,lw=1);axs[0,1].set(xlim=(4.1,.7),xlabel=tr('化学位移 / ppm','Chemical shift / ppm'),ylabel=tr('频谱密度 / 相对单位 Hz$^{-1}$','Spectral density / relative units Hz$^{-1}$'));title(axs[0,1],'B','傅里叶变换分开频率','Fourier transform separates frequencies')
axs[1,0].plot(ppm,spectrum,color=teal,label=tr('不加窗','Unweighted'));axs[1,0].plot(ppm,broadened,color=coral,label=tr('额外展宽 3 Hz','Additional 3 Hz broadening'));axs[1,0].set(xlim=(1.23,1.11),xlabel=tr('化学位移 / ppm','Chemical shift / ppm'),ylabel=tr('频谱密度 / 相对单位 Hz$^{-1}$','Spectral density / relative units Hz$^{-1}$'));axs[1,0].legend(frameon=False,fontsize=9);title(axs[1,0],'C','光滑与分辨率一起改变','Smoothing changes resolution')
shortN=1000;_,short=fft(fid[:shortN]);axs[1,1].plot(ppm,ideal,color=teal,label=tr('2.048 s 记录','2.048 s acquisition'));axs[1,1].plot(ppm,short,color=gold,label=tr('0.250 s 记录，同样补零','0.250 s, same zero filling'));axs[1,1].set(xlim=(1.23,1.11),xlabel=tr('化学位移 / ppm','Chemical shift / ppm'),ylabel=tr('频谱密度 / 相对单位 Hz$^{-1}$','Spectral density / relative units Hz$^{-1}$'));axs[1,1].legend(frameon=False,fontsize=9);title(axs[1,1],'D','补零没有延长观察时间','Zero filling does not extend observation')
fig.tight_layout();save(fig,'processing')

TR=np.linspace(.01,18,400);rec1=1-np.exp(-TR/1);rec3=1-np.exp(-TR/3);biased=1.5*rec1/rec3
fig,axs=plt.subplots(1,2,figsize=(11.6,4.7));axs[0].plot(TR,rec1,color=teal,label='T$_1$ = 1 s');axs[0].plot(TR,rec3,color=blue,label='T$_1$ = 3 s');axs[0].axhline(1-np.exp(-5),color=gray,ls=':',label='99.326%');axs[0].set(xlabel=tr('重复间隔 / s','Repetition interval / s'),ylabel=tr('恢复磁化 / 平衡磁化','Recovered / equilibrium magnetization'),ylim=(0,1.05));axs[0].legend(frameon=False,fontsize=9);title(axs[0],'A','不同环境恢复速度不同','Environments recover at different rates')
axs[1].plot(TR,biased,color=coral,lw=3);axs[1].axhline(1.5,color=gray,ls='--',label=tr('真实核数比 3/2','True nucleus-count ratio 3/2'));axs[1].set(xlabel=tr('重复间隔 / s','Repetition interval / s'),ylabel=tr('受恢复影响的积分比','Recovery-biased integral ratio'));axs[1].legend(frameon=False,fontsize=9);title(axs[1],'B','位置正确，面积仍可偏差','Correct positions can accompany biased areas')
fig.tight_layout();save(fig,'recovery')
np.savetxt(out/'deposited_transitions.csv',lines,delimiter=',',header='chemical_shift_ppm,deposited_height',comments='')
np.savetxt(out/'deposited_integrals.csv',np.array([[3.641,areas['1'],2],[1.170,areas['2'],3]]),delimiter=',',header='group_shift_ppm,deposited_integral,assigned_proton_count',comments='')
np.savetxt(out/'simulated_fid.csv',np.column_stack([t,noisy.real,noisy.imag]),delimiter=',',header='time_s,real,imaginary',comments='')
np.savetxt(out/'simulated_spectra.csv',np.column_stack([ppm,spectrum,broadened,short]),delimiter=',',header='chemical_shift_ppm,unweighted,broadened_3Hz,short_record',comments='')
summary={'proton_frequency_at_9_4T_MHz':42.577*9.4,'deposited_transition_count':len(lines),'deposited_area_ratio':actual_ratio,'simulated_area_ratio':float(simratio),'linewidth_T2star_02_Hz':1/(np.pi*.2),'recovery_at_5T1':float(1-np.exp(-5)),'biased_ratio_TR1':float(1.5*(1-np.exp(-1))/(1-np.exp(-1/3))),'example_concentration_mM':5*(120/3)/(80/2),'raw_frequency_spacing_Hz':1/(N*dt),'data_kind':{'peak_records':'real BMRB bmse000297 data','FID_and_recovery':'constructed teaching models'}}
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
```

The complete program reads the bundled BMRB NMR-STAR file offline, extracts the deposited transitions and integrals, and separately constructs controlled FIDs, window-function comparisons and recovery-bias plots. It retains the original database record and exports convenient tables. Heights, integrals and chemical shifts are read from their corresponding data categories rather than interchanged. The simulated linewidth, noise and acquisition duration are explicit. Each numerical result can therefore be traced to either an experimental record or a stated model assumption.

## From ethanol to polymers and proteins

The observed nucleus can also follow the research question. Fluorine-19 in a fluorinated material or phosphorus-31 in phosphate-containing groups may provide a more direct view than a crowded proton spectrum. Solvent, frequency window, referencing and quantitative acquisition must then be selected for that nucleus. Choosing a reporter with fewer interfering components can be more effective than forcing every proton peak apart. Chemical assignment still matters: the appearance of a new resonance by itself does not identify a particular reaction product.

For a side-group reaction, an unreacted functional-group signal may decrease while a stable backbone signal remains. Normalize each integral by the nuclei contributed per relevant unit, then compare the ratios before and after reaction. This helps separate a change in solution concentration from chemical conversion. If reaction also changes solubility or creates overlapping product signals, additional separation or assignment information is needed. A useful conversion result identifies the chosen signals, their nucleus-count normalization and the material fraction entering the measurement. Those definitions make the reported percentage reproducible and chemically meaningful.

Polymer NMR often compares monomer composition, side-group conversion, end groups or local sequence arrangements. After selecting separated, assigned signals, divide integrals by the number of nuclei contributed by each repeat unit before calculating composition. End-group estimates of chain length require special attention because the end-group signal can be much weaker than the repeat-unit signal. Trace impurities or baseline errors can then have a large effect. The number and chemical integrity of end groups must also be known. Complete dissolution determines whether the solution spectrum represents the whole material or only its soluble fraction.

Larger molecules tumble more slowly in solution, and their signals may broaden and overlap. An additional frequency dimension spreads relationships that would otherwise crowd a single horizontal axis. COSY-type experiments connect proton responses through coupling, HSQC links hydrogen and suitable directly bonded heteronuclear responses, and NOE-related experiments can provide information about spatial proximity. These experiments report different physical relationships. An intersection in a two-dimensional plot does not by itself establish an arbitrary bond. Choose the experiment according to the type of connection needed.

Protein structure determination combines many assignments and distance or orientation restraints with molecular geometry. A displayed NMR structural ensemble represents conformations permitted by the observations and calculation procedure. Its spread also depends on restraint coverage and the method used; its members are not automatically successive frames of a molecular movie. Investigating dynamics uses dedicated relaxation, exchange or other time-sensitive experiments. NMR can study both structure and motion, but the two questions require different observables and models.

Solids retain different molecular motions and anisotropic interactions, often requiring magic-angle spinning and appropriate pulse sequences to manage broadening. Solubility, the need to preserve solid organization, and whether the question concerns composition or local motion help determine the choice between solution and solid-state NMR. The most useful outcome is an explicit set of assignments and amount definitions: which nuclei produce each signal, how referencing was done, how many nuclei each integral represents, and which experiment supports each proposed connection. These details turn spectral peaks into evidence about molecular organization and material change.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/S06.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [BMRB: Ethanol bmse000297](https://bmrb.io/metabolomics/mol_summary/show_data.php?id=bmse000297)

   Real ethanol peak records, assignments, integrals and specimen conditions.

   Public-domain archive data; DOI 10.13018/BMSE000297; Madison Metabolomics Consortium.
2. [BMRB: About and distribution policy](https://bmrb.io/bmrb/)

   Public-domain data policy and database citation.

   Archive data public domain; BMRB states shared wwPDB usage policy.
3. [Oxford NMR: Classic NMR Papers](https://nmr.chem.ox.ac.uk/classic-nmr-papers)

   Primary-paper index for 1946 NMR, chemical shifts and 1966 Fourier-transform methods.

   Historical bibliography; original figures.
4. [UCSB NMR: Chemical Shift Referencing](https://nmr.chem.ucsb.edu/protocols/refppm.html)

   Chemical-shift definition, references and conditions.
5. [Oxford NMR: Quantitative NMR Spectroscopy](https://nmr.chem.ox.ac.uk/sites/g/files/vzsiac2831/files/nmrchem/documents/media/quantitative_nmr.pdf)

   Recovery time, integration, phase and quantitative calibrants.
6. [Oxford NMR: Processing Techniques](https://nmr.chem.ox.ac.uk/sites/g/files/vzsiac2831/files/nmrchem/documents/media/processing-techniques.pdf)

   Signal-to-noise and broadening tradeoff of exponential weighting.

   Copyright author; technical reference, no source figures reproduced.
7. [Iowa State CIF: NMR Coupling Constants](https://www.cif.iastate.edu/nmr/nmr-tutorials/couplingconstants)

   Coupling ranges for different bonding relationships and hertz units.
