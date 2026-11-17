# Circular dichroism: Optical clues to protein folding

Source: https://ml-biomat.com/tutorials/experimental-methods/s05/en/
Language: en

Read ensemble conformational changes from a small polarization-dependent absorption difference, then examine concentration, reference spectra and temperature conditions.

## The protein is still present. Has its folding changed?

Heating egg white makes a structural change visible: a transparent liquid gradually becomes an opaque solid as proteins change their organization and interactions. Research often concerns earlier and subtler changes. An enzyme loses activity during storage while its solution remains clear. A protein adsorbs to a material and behaves differently even though its amount appears unchanged. The question is then not simply whether protein is present, but whether its chain retains the same arrangement. Circular dichroism, usually abbreviated CD, observes differences in the way a specimen absorbs two polarization states of light and uses them to investigate conformation.

It helps to separate levels of protein structure. Amino acids join into a chain with a particular sequence. Some portions coil into an alpha helix, while others lie alongside one another in beta sheets. These local arrangements are called secondary structure. The chain also folds into an overall organization that brings distant regions together, forming tertiary structure. Imagine a long ribbon carrying a fixed sequence of letters: the order of the letters, the local way the ribbon bends, and its overall arrangement are different descriptions. Molecular mass and protein amount alone do not tell us whether these arrangements have remained the same.

Far-ultraviolet CD commonly examines the optical response of the peptide backbone and helps compare overall secondary-structure composition. Near-ultraviolet CD uses responses from aromatic side chains and other groups in asymmetric environments to provide another view of folding. The wavelength ranges, signal sizes and specimen requirements differ. When a report states that CD detected a structural change, look for the measured range, whether the conclusion concerns shape or amplitude, and how concentration and path length were handled. These details connect the phrase structural change to an actual observation.

This chapter develops that connection from handedness and polarization to the conversion of millidegrees into a comparable structural signal. We will construct explicitly labeled teaching spectra and examine how composition, concentration error and wavelength coverage affect an analysis. A temperature series then introduces transition midpoints and the role of baselines. The goal is to read positive and negative bands as parts of a measurement chain, connecting the condition of a protein specimen to optical acquisition and a specific research decision.

## Why can opposite rotations of light see a molecule differently?

Your left hand resembles the mirror image of your right hand, but translation and rotation cannot make them coincide completely. This property is called chirality. Molecules can also be chiral, and a protein contains asymmetric environments at several organizational levels. Chirality does not simply mean that a large molecule forms a helix. A local chemical group can be chiral, and an otherwise achiral absorbing group can acquire an optical response through its asymmetric surroundings. Which electronic transition interacts with the light determines the relevant spectral region.

Light is an electromagnetic wave. To understand polarization, first follow the direction of its electric field. In linearly polarized light, that direction oscillates along a fixed orientation. At a fixed spatial position in circularly polarized light, the field direction rotates with time. Opposite rotations at the same wavelength can be absorbed slightly differently by a chiral specimen. The rotating quantity is the field direction: the beam is not physically following a spring-shaped trajectory through the liquid. Naming left and right also depends on the viewing convention, so the sign convention of an instrument should be retained consistently during analysis.

![Original field-combination and detection schematics. Dashed circles are opposite rotating components; green is their resultant. Equal amplitudes yield a line, unequal amplitudes an ellipse. C shows the functional order of modern modulated detection, connecting Cotton’s optical observation to later photoelectric measurement rather than reconstructing a particular historical device.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/47139407f1e0e757e3cf8313.svg?v=47139407f1e0)

Figure 1Original field-combination and detection schematics. Dashed circles are opposite rotating components; green is their resultant. Equal amplitudes yield a line, unequal amplitudes an ellipse. C shows the functional order of modern modulated detection, connecting Cotton’s optical observation to later photoelectric measurement rather than reconstructing a particular historical device.

Cotton's work on colored chiral solutions in the late nineteenth century connected unequal absorption of opposite circular polarizations to elliptical polarization of the emerging light. In 1950, Mitchell's discussion of a photoelectric measurement method still distinguished these two observational routes: comparing absorption of the circular components, or measuring the ellipticity that results. This history explains an initially surprising feature of modern data. An experiment concerned with an absorption difference often reports an angle. The two quantities are related descriptions of the same small optical asymmetry.

$$
\Delta A=A_L-A_R
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d5b807cb2100c99c9e97d19c.svg) | Difference in left- and right-circular absorbance, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/90999a9e9d00fa32ceb64a06.svg) | Left-circular absorbance under the instrument’s consistent handedness convention, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/5f8a382ff514ba7cfa60fce3.svg) | Right-circular absorbance, dimensionless. |

Compare absorption at the same wavelength and conditions. 0.5003−0.4997=0.0006; the sign identifies stronger absorption of one handedness rather than negative light intensity.

Suppose the left-circular absorbance is 0.5003 and the right-circular absorbance is 0.4997. Their average is close to 0.5, but the difference is only 0.0006. CD therefore extracts a small difference against a much larger background absorption. With the convention used here, positive CD means stronger left-circular absorption and negative CD means stronger right-circular absorption. A negative band does not imply negative light intensity or a sample that has negative absorption. Ordinary absorption asks how much light is lost; CD compares the losses for two polarization states.

A modern instrument can use a photoelastic modulator to change polarization rapidly and extract the detector response synchronized with that modulation. Rapid alternation helps compare the two states under similar source and specimen conditions. It still requires enough transmitted light. If the specimen absorbs almost all of the ultraviolet illumination, increasing electronic gain does not create additional photons that have passed through the specimen. This point connects path length, buffer choice and detector-voltage monitoring to the measurement principle rather than treating them as unrelated operating rules.

## Millidegrees, concentration and residues: place the curves on a common scale

Two oppositely rotating circular components with equal amplitudes can combine into linearly polarized light. If the specimen attenuates them differently, the resulting electric-field vector traces an ellipse. Ellipticity describes the ratio of the ellipse's axes through an angle. CD signals are commonly small enough to report in millidegrees, each one thousandth of a degree. For small signals, ellipticity is approximately proportional to the absorbance difference. The angle describes the polarization ellipse, not the rotation of the protein molecule or the geometrical twist of an alpha helix.

$$
\theta_{\mathrm{mdeg}}\approx32980\,\Delta A
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e32cd7c782aaca32cd9cb448.svg) | Numerical ellipticity in millidegrees, mdeg. |
| ![Formula](https://ml-biomat.com/static/agent-math/d5b807cb2100c99c9e97d19c.svg) | Difference in left- and right-circular absorbance, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/a78b5a609fa453a7cb2f8ab4.svg) | Approximate conversion factor from absorbance difference to millidegrees, mdeg. |

At small ellipticity, the circular-component amplitude difference is approximately linear in absorbance difference. The logarithmic absorption definition and radian-to-degree conversion give this coefficient. ΔA=0.0006 corresponds to about 19.788 mdeg.

Doubling the concentration of an unchanged protein generally doubles the number of absorbing molecules encountered by the light and hence the measured millidegree signal. Doubling the path length has a similar effect under suitable optical conditions. A deeper raw band can therefore mean that more protein was measured rather than that its structure changed. Structural comparisons divide out concentration and path length. Because proteins also differ in chain length, the signal is often normalized per amino-acid residue, producing mean residue ellipticity. A residue is the structural unit left when an amino acid becomes part of the chain.

$$
[\theta]_{\mathrm{MR}}=\frac{\theta_{\mathrm{mdeg}}\,M_R}{10\,c_m\,l}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b20f1a1290e61c97a2fe6f9f.svg) | Mean residue ellipticity, deg cm² dmol⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/e32cd7c782aaca32cd9cb448.svg) | Matched-blank-subtracted ellipticity, mdeg. |
| ![Formula](https://ml-biomat.com/static/agent-math/cad38889865553ac191f2a12.svg) | Mean amino-acid residue molar mass, g mol⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/46293108d95e427e874bd905.svg) | Protein mass concentration, mg mL⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/b725c065245400348075701d.svg) | Path length, cm. |
| ![Formula](https://ml-biomat.com/static/agent-math/e2574f61b59164e433af2aee.svg) | Numerical unit-conversion factor for the stated concentration, angle and molar units. |

Divide by residue concentration and path length for comparison. −20 mdeg, MR=110 g/mol, cm=0.20 mg/mL and l=0.10 cm give −11000 deg cm² dmol⁻¹. One millimeter is 0.10 cm; changing concentration units requires changing the conversion factor.

Consider a measured ellipticity of −20 mdeg, an average residue molar mass of 110 g/mol, a mass concentration of 0.20 mg/mL and a path length of 0.10 cm. The mean residue ellipticity is −11000 deg cm² dmol⁻¹. Here 0.10 cm equals 1 mm. Entering 1 cm for a 1 mm cell creates a tenfold error. If the actual concentration is 0.20 mg/mL but the calculation uses 0.25 mg/mL, the normalized amplitude becomes eighty percent of its correct value. This affects more than the visual scale because secondary-structure fits often use amplitude across the entire spectrum.

The average residue mass should be calculated from the actual sequence and molecular composition when accurate normalization is needed. Using 110 is a convenient teaching approximation; tags, modifications, unusual composition and short peptides can require more specific treatment. Concentration measurement also needs to suit the specimen. Ultraviolet absorption requires an appropriate extinction coefficient and attention to interfering species. A colorimetric assay requires checking whether the target protein and calibration standard respond similarly. A smooth CD spectrum can still be limited by a concentration error. Clear units, concentration and path length make comparisons between batches and proteins interpretable.

## Getting ultraviolet photons to the detector matters more than smoothing a curve

The far ultraviolet can provide substantial structural information while also being difficult to transmit. Protein, buffer, salts, additives and the cell all contribute to the total absorption. A shorter quartz path reduces that absorption but also reduces the CD signal. Raising protein concentration may recover signal while introducing aggregation or concentration-dependent conformation. Suitable conditions therefore depend on a combination of specimen state, total absorption and required wavelength range. Preserve the state relevant to the research question, then choose a path and buffer that allow the intended observation.

The blank must match the final solution surrounding the protein. A stock can carry salt, glycerol, reducing agents or small amounts of solvent into the measurement even after dilution. A nominally similar buffer prepared separately may leave a mismatch after subtraction. Buffer from an appropriate exchange procedure, or a blank formulated to match the final composition, better represents the optical background. Blank scans can also reveal cell contamination, placement differences or stress-related birefringence. Reproducible cell orientation reduces geometrical changes in an experiment based on a very small difference.

Many instruments record photomultiplier high tension or another gain-related quantity alongside CD. When transmitted light decreases, the detector increases gain to maintain a measurable output. This provides a practical indication of photon starvation at the low-wavelength end. Acceptable operating ranges depend on the detector and instrument; a voltage threshold specified for one model is not a universal CD criterion. A rising gain trace or strongly divergent repeat scans should prompt inspection of absorption, path length and specimen condition. Smoothing a curve changes its appearance but does not restore information that was poorly recorded.

Scan speed, integration time and spectral bandwidth work together. If the instrument travels across a broad wavelength interval during one integration period, neighboring wavelengths are mixed and features may broaden or lag. Averaging independent scans can reduce random noise, but a changing specimen contributes its evolution to that average. Retaining individual scans can reveal aggregation, settling or slow rearrangement after a temperature change. The state of a biological macromolecule during acquisition can matter more to interpretation than the number of decimal places in the final fitted result.

![Raw repeats, matched blank, blank subtraction and concentration normalization for one teaching specimen. In D, an overestimated concentration reduces amplitude to 80% of the correct value. The normalized axis unit is 10³ deg cm² dmol⁻¹. All curves come from the specified measurement model.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9ad852fa856e3cd3d21f6e35.svg?v=9ad852fa856e)

Figure 2Raw repeats, matched blank, blank subtraction and concentration normalization for one teaching specimen. In D, an overestimated concentration reduces amplitude to 80% of the correct value. The normalized axis unit is 10³ deg cm² dmol⁻¹. All curves come from the specified measurement model.

The figure places teaching sample scans, the matched background and normalization on the same page. Choosing a low-wavelength cutoff should follow the quality of the observation, not merely remove an unattractive region. The chosen range must also match the requirements of the reference set and analysis method. If a method expects shorter wavelengths, producing percentages from a narrower input range does not reconstruct the missing measurements. Spectral coverage is part of the structural analysis and should accompany the explanation of its result.

Replicate measurements answer different questions depending on how they are made. Repeating a scan without moving the same cell mainly examines short-term acquisition variability. Refilling the cell includes handling and filling effects. Preparing another protein solution also includes preparation variability. These sources need not be combined into one unexplained error bar. For a comparison of storage conditions, independent preparations and measurements at matched temperature may be more informative than many repeated scans of a single aliquot. Select repetition at the level where the research conclusion will be made.

## Structural fractions resemble color mixing, with a reference palette that matters

Consider what an ensemble fraction describes. CD collects responses from many molecules in the illuminated volume. An average helix fraction of fifty percent could mean that approximately half the residues in each molecule are helical, or it could arise from a mixture of distinct conformational populations. The average alone does not specify every molecule's state. During folding, mixing or partial aggregation, a changing spectrum can reflect rearrangement within a population or changing proportions of populations. Separation, time-resolved observation and complementary structural methods help distinguish these interpretations.

Alpha-helical proteins often show negative bands near 208 and 222 nm and a positive band at shorter wavelength. Beta-sheet-rich structures have a different characteristic response, while less regularly organized chains contribute other patterns. These landmarks develop intuition, but proteins are not mixtures of perfectly invariant pigments. Helix length, sheet geometry, side chains, solvent and interactions between structural elements can affect spectral shape. Two negative bands motivate an investigation of helical features; a single peak height does not define a universally valid helix percentage.

$$
y(\lambda)=\sum_{j=1}^{K}f_jS_j(\lambda)+r(\lambda),\qquad f_j\geq0,\quad\sum_{j=1}^{K}f_j=1
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1dc9052b8842180988a4a8b2.svg) | Specimen normalized ellipticity at wavelength λ, deg cm² dmol⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | Wavelength, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/24733a44cf365eb5e1b92574.svg) | Number of reference components, three here. |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | Component index. |
| ![Formula](https://ml-biomat.com/static/agent-math/ea0efbb08d1d6502e2a12fed.svg) | Fraction of component j, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/6ab55d9e555768c0f2cd2ac4.svg) | Reference spectrum j, in the same units as y. |
| ![Formula](https://ml-biomat.com/static/agent-math/d2c3a93795434a5ba3f1e2c2.svg) | Difference between data and mixture, including noise and unexplained contributions, in the same units as y. |

Combine reference responses by fraction. The prescribed 0.55, 0.25 and 0.20 are nonnegative and sum to one. References must suit the object and range; constructed bases here teach mixing and error propagation.

A linear-combination model offers a transparent starting point. Reference spectra are mixed in different proportions until their combination explains the observed curve. Like mixing a target color from a palette, the answer depends on the available references. Fits often constrain fractions to be nonnegative and sum to one, expressing the idea that the components form a whole. Established analysis tools use experimentally characterized reference proteins and tested algorithms. The code in this chapter instead uses three deliberately constructed basis curves to teach combination, residuals and sensitivity; those curves are not a database for analyzing real proteins.

The example prescribes fractions of 0.55 helix, 0.25 sheet and 0.20 other conformation, then adds an optical background and repeat-measurement noise. Analysis subtracts the matched blank, normalizes by concentration and path length, and estimates fractions using constrained fitting. Residuals show which wavelengths remain unexplained. Repeated noise sampling shows how reading variability affects the estimates under the chosen model. That interval does not automatically include concentration error or an unsuitable reference set. We therefore examine concentration normalization and the low-wavelength cutoff separately.

![A uses three constructed basis curves to explain mixing; B shows the fit and residual, in units of 10³ deg cm² dmol⁻¹. C changes the low-wavelength cutoff, with error bars of twice the SD from 160 specified-noise resamples. D changes only the assumed concentration. Dotted lines mark prescribed fractions; reference-library uncertainty is not part of these teaching calculations.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/3af7cf95beee2eed18b8a9c2.svg?v=3af7cf95beee)

Figure 3A uses three constructed basis curves to explain mixing; B shows the fit and residual, in units of 10³ deg cm² dmol⁻¹. C changes the low-wavelength cutoff, with error bars of twice the SD from 160 specified-noise resamples. D changes only the assumed concentration. Dotted lines mark prescribed fractions; reference-library uncertainty is not part of these teaching calculations.

## Did structure change, or did normalization change?

Change helix fraction to inspect shape, then change actual and normalization concentrations together. Next change only one concentration and compare the panels. The nonhelical remainder is divided into 55% sheet and 45% other. Reference curves are constructed teaching models; path is 0.10 cm and mean residue molar mass is 110 g/mol.

Green shows the current result. The dashed gray curve in the right panel uses the correct concentration. Its 10³ axis unit means 10³ deg cm² dmol⁻¹.

The interactive experiment changes the helix fraction and divides the remaining fraction between sheet and other conformation. It displays both raw millidegrees and normalized ellipticity. Changing concentration alters the raw signal while correctly normalized curves remain the same. Entering an incorrect normalization concentration also rescales the supposedly comparable curve. This separates two steps that are easily confused: the instrument measures an optical difference, whereas a structural fraction is an interpretation that additionally uses specimen information and a reference model.

A reference set should represent the kinds of structures being studied. A collection dominated by globular proteins may not adequately represent collagen triple helices, long coiled coils, membrane-associated proteins or particular aggregates. Similarity between reference spectra also affects discrimination. If two references resemble one another over the measured range, several nearby mixtures can produce similar fits. A broader reliable wavelength range or an independent structural observation can then be especially valuable. Sometimes a well-supported conclusion about an overall spectral change is more useful than emphasizing tiny differences in fitted percentages.

A good residual is necessary for checking a model but does not uniquely identify its components. Several combinations or reference families may reproduce a finite-noise spectrum. Conversely, a systematic residual may arise from a baseline error, concentration normalization, an omitted structural contribution or a reference mismatch. Examine where the residual occurs and which experimental change affects it. A constant offset across wavelengths suggests a different diagnostic route from a localized feature or a scale error. The aim is to use the mismatch to design a better measurement, rather than treating the fitting score as an isolated verdict.

## Follow folding with temperature: why a midpoint needs baselines

Following one wavelength saves acquisition time but discards changes in spectral shape. First record full spectra at representative temperatures, then select a sensitive wavelength with reliable transmission for a denser temperature series. An approximate common crossing point can suggest that spectral contributions compensate as populations change. It is a useful clue for a simple mixture model, although more components or compensating changes can also produce such a crossing. Examining the complete spectral series, residuals and reversibility gives a stronger connection between the data and a proposed state model.

If a protein has a useful helix-related signal at 222 nm, that wavelength can be followed while temperature increases. The signal moves from a low-temperature state toward a high-temperature state, often giving a tilted step. The two ends can themselves vary with temperature because each state has a temperature-dependent optical response. Taking the average of the lowest and highest observed values can therefore mix baseline slopes with the transition. At each temperature, compare the observation with the two state baselines expected at that same temperature.

$$
f_U(T)=\frac{y(T)-y_F(T)}{y_U(T)-y_F(T)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/38d847ee4f90227f3c1be623.svg) | Unfolded fraction in the two-state linear-response model, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | Temperature, °C in this example. |
| ![Formula](https://ml-biomat.com/static/agent-math/48104f5cab9f6f1a70ef94f5.svg) | Observed signal at T, mdeg here. |
| ![Formula](https://ml-biomat.com/static/agent-math/52bd6fd49934aeeb04b153c1.svg) | Folded-state baseline at the same temperature, mdeg. |
| ![Formula](https://ml-biomat.com/static/agent-math/a600d0bd5b133dd9faf3ebe2.svg) | Unfolded-state baseline at the same temperature, mdeg. |

Linearly interpolate between state baselines. yF=−24, yU=−2 and y=−13 give fU=0.5. Equilibrium population interpretation additionally requires reversible equilibrium behavior and an appropriate two-state model.

Suppose the folded-state baseline at a particular temperature is −24 and the unfolded-state baseline is −2, while the observed value is −13 in the same units. A two-state linear-response interpretation gives an unfolded fraction of 0.5. If equilibrium, reversibility and the two-state description apply, this identifies the transition midpoint. The teaching program generates a temperature series from an empirical sigmoid with sloping baselines and fits its midpoint and width. The width describes the temperature interval over which the signal changes; it is not itself a thermodynamic enthalpy.

![Constructed heating signals and an empirical fit include two sloping state baselines. The shifted cooling curve illustrates path dependence. The right panel normalizes between same-temperature baselines; a model fraction of 0.5 defines its midpoint. Interpreting that midpoint as equilibrium stability requires reversible equilibrium behavior.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/10922314d4d84aa9fb11d9f2.svg?v=10922314d4d8)

Figure 4Constructed heating signals and an empirical fit include two sloping state baselines. The shifted cooling curve illustrates path dependence. The right panel normalizes between same-temperature baselines; a model fraction of 0.5 defines its midpoint. Interpreting that midpoint as equilibrium stability requires reversible equilibrium behavior.

Cooling after heating provides an informative check. Recovery of the original spectrum, together with consistent curves at different scan rates or waiting times, supports an equilibrium interpretation. Separation of heating and cooling paths, cloudiness or precipitation directs attention toward slow refolding, aggregation or irreversible changes. The figure includes a deliberately shifted cooling curve to show that a similar sigmoid appearance can accompany different experimental paths. It is a constructed illustration, not a measurement of the thermal stability of a named protein.

Temperature should refer to the specimen as closely as the setup permits. A programmed block temperature and the liquid temperature may differ during rapid changes. Evaporation can increase concentration, while bubbles can alter the optical path. A sealed suitable cell, adequate equilibration and a consistent heating schedule help connect the displayed temperature to the molecular state. If a transition changes with waiting time, time becomes an experimental variable to study rather than a nuisance to hide. These observations guide whether to report a protocol-dependent transition or develop an equilibrium model.

### From repeated scans to mixture fitting and a thermal midpoint

The program constructs labeled teaching data, preserves blanks and repeat scans, evaluates concentration and wavelength sensitivity, and fits a baseline-aware empirical thermal transition. The program exports all figures and CSV files.

```
"""CD measurement and interpretation using explicit teaching models.
Run: python main.py --output results --language en
All spectra are constructed; the basis curves are not a protein reference library.
"""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import minimize,curve_fit
from scipy.special import expit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle

p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True)
zh=a.language=='zh'
def tr(z,e):return z if zh else e
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','text.color':'#263d49','axes.labelcolor':'#263d49','axes.edgecolor':'#9bacb1','svg.fonttype':'path'})
cols=['#078579','#265f85','#d6604d'];gray='#84969b';gold='#bb9033'
def save(f,n):
 f.savefig(out/f'{n}-{a.language}.svg',bbox_inches='tight');f.savefig(out/f'{n}-{a.language}.png',dpi=155,bbox_inches='tight');plt.close(f)
def title(ax,l,z,e):ax.set_title(l+'  '+tr(z,e),loc='left',weight='bold',pad=14)

# Polarization components are schematic field amplitudes, not beam trajectories.
fig,axs=plt.subplots(1,3,figsize=(12.4,4.1))
u=np.linspace(0,2*np.pi,300)
for ax,k,heading in zip(axs[:2],[1,.65],[('等幅分量 → 直线','Equal components → line'),('不等幅分量 → 椭圆','Unequal components → ellipse')]):
 x=np.cos(u)+k*np.cos(u);y=np.sin(u)-k*np.sin(u)
 ax.plot(np.cos(u),np.sin(u),color=cols[1],alpha=.4,ls='--');ax.plot(k*np.cos(u),-k*np.sin(u),color=cols[2],alpha=.4,ls='--');ax.plot(x,y,color=cols[0],lw=3)
 ax.annotate('',xy=(np.cos(.8),np.sin(.8)),xytext=(np.cos(.55),np.sin(.55)),arrowprops={'arrowstyle':'->','color':cols[1]})
 ax.annotate('',xy=(k*np.cos(.8),-k*np.sin(.8)),xytext=(k*np.cos(.55),-k*np.sin(.55)),arrowprops={'arrowstyle':'->','color':cols[2]})
 ax.set_aspect('equal');ax.set(xlim=(-2.2,2.2),ylim=(-1.4,1.4),xlabel=tr('电场分量 x（相对）','Field x (relative)'),ylabel=tr('电场分量 y（相对）','Field y (relative)'));title(ax,'A' if k==1 else 'B',*heading)
ax=axs[2];ax.axis('off');ax.set_xlim(0,5);ax.set_ylim(0,5)
for y,z,e in [(4,'选定波长与线偏振','Selected wavelength / linear polarization'),(2.8,'调制两种旋向','Modulate opposite handedness'),(1.6,'样品产生吸收差','Specimen absorbs differently'),(.4,'同步读取光电信号','Read synchronized detector signal')]:
 ax.add_patch(Rectangle((.3,y-.28),4.3,.6,fc='#e8efed',ec=gray));ax.text(2.45,y+.02,tr(z,e),ha='center',va='center',fontsize=9)
 if y>.4:ax.annotate('',xy=(2.45,y-.88),xytext=(2.45,y-.3),arrowprops={'arrowstyle':'-|>','color':cols[1]})
title(ax,'C','光电比较','Detect the difference')
fig.text(.5,.01,tr('Cotton 的吸收差与椭圆率联系，延续到光电测量。示意图不复原某台历史仪器。','Cotton linked differential absorption to ellipticity; photoelectric methods measure the difference. Conceptual apparatus, not a historical reconstruction.'),ha='center',fontsize=9)
fig.tight_layout(rect=[0,.08,1,1]);save(fig,'polarization')

# Basis units are mean residue ellipticity, deg cm^2 dmol^-1.
w=np.arange(190.,251.)
def g(mu,sd):return np.exp(-.5*((w-mu)/sd)**2)
basis=1000*np.column_stack([35*g(193,5)-23*g(208,5)-20*g(222,6),22*g(195,6)-17*g(218,8),-30*g(198,6)+3*g(220,9)])
truth=np.array([.55,.25,.20]);mre=basis@truth
concentration=.20;path=.10;mrw=110.;factor=10*concentration*path/mrw
background=.8+.01*(w-220);rng=np.random.default_rng(550)
scans=mre[:,None]*factor+background[:,None]+rng.normal(0,.25,(len(w),5))
blanks=background[:,None]+rng.normal(0,.08,(len(w),8))
corrected=scans.mean(axis=1)-blanks.mean(axis=1);normalized=corrected/factor
def fractions(y,mask=None):
 if mask is None:mask=np.ones(len(w),bool)
 X=basis[mask]/1000;target=y[mask]/1000
 r=minimize(lambda f:np.mean((X@f-target)**2),[.4,.3,.3],method='SLSQP',bounds=[(0,1)]*3,constraints=[{'type':'eq','fun':lambda f:f.sum()-1}],options={'ftol':1e-12,'maxiter':300})
 if not r.success:raise RuntimeError(r.message)
 return r.x
fit=fractions(normalized);fitted=basis@fit
fig,axs=plt.subplots(2,2,figsize=(11.6,7.6))
axs[0,0].plot(w,scans,lw=.8,alpha=.55,color=cols[1]);axs[0,0].plot(w,scans.mean(axis=1),lw=2,color=cols[1]);axs[0,0].set_ylabel(tr('原始椭圆率 / mdeg','Raw ellipticity / mdeg'));title(axs[0,0],'A','五次样品扫描','Five specimen scans')
axs[0,1].plot(w,blanks,lw=.8,alpha=.4,color=gray);axs[0,1].plot(w,blanks.mean(axis=1),color=gray,lw=2);axs[0,1].set_ylabel(tr('空白椭圆率 / mdeg','Blank ellipticity / mdeg'));title(axs[0,1],'B','匹配缓冲空白','Matched buffer blanks')
axs[1,0].plot(w,corrected,color=cols[0],lw=2);axs[1,0].set_ylabel(tr('扣空白信号 / mdeg','Blank-corrected / mdeg'));title(axs[1,0],'C','先做光学比较','Subtract before normalization')
axs[1,1].plot(w,normalized/1000,color=cols[0],lw=2,label=tr('正确浓度 0.20 mg/mL','Correct concentration 0.20 mg/mL'));axs[1,1].plot(w,normalized*.8/1000,color=cols[2],ls='--',label=tr('误用 0.25 mg/mL','Incorrectly use 0.25 mg/mL'));axs[1,1].set_ylabel(tr('平均残基椭圆率 / 10³ 单位','Mean residue ellipticity / 10³ units'));axs[1,1].legend(fontsize=8,frameon=False);title(axs[1,1],'D','归一化也会引入系统误差','Normalization can introduce bias')
for ax in axs.flat:ax.set_xlabel(tr('波长 / nm','Wavelength / nm'));ax.axhline(0,color=gray,lw=.6)
fig.tight_layout();save(fig,'measurement')

boot=np.array([fractions(mre+rng.normal(0,.25/np.sqrt(5)/factor,len(w))) for _ in range(160)])
cuts=[190,205,220];cutfit=np.array([fractions(normalized,w>=v) for v in cuts]);cutboot=np.array([[fractions(mre+rng.normal(0,.25/np.sqrt(5)/factor,len(w)),w>=v) for _ in range(160)] for v in cuts]);cutSD=np.std(cutboot,axis=1,ddof=1);scales=np.array([.8,1.,1.2]);scalefit=np.array([fractions(normalized/v) for v in scales])
fig,axs=plt.subplots(2,2,figsize=(11.6,7.8));names=[tr('螺旋','Helix'),tr('折叠','Sheet'),tr('其他','Other')]
for k in range(3):axs[0,0].plot(w,basis[:,k]/1000,color=cols[k],label=names[k])
axs[0,0].legend(frameon=False,fontsize=9);axs[0,0].set(xlabel=tr('波长 / nm','Wavelength / nm'),ylabel=tr('平均残基椭圆率 / 10³ 单位','Mean residue ellipticity / 10³ units'));title(axs[0,0],'A','构造参考，解释组合','Constructed references explain mixing')
axs[0,1].plot(w,normalized/1000,'o',ms=3,color=gray,label=tr('测量模型','Measurement model'));axs[0,1].plot(w,fitted/1000,color=cols[0],lw=2,label=tr('约束组合','Constrained mixture'));axs[0,1].plot(w,(normalized-fitted)/1000,color=cols[2],label=tr('残差','Residual'));axs[0,1].legend(frameon=False,fontsize=9);axs[0,1].set(xlabel=tr('波长 / nm','Wavelength / nm'),ylabel=tr('平均残基椭圆率 / 10³ 单位','Mean residue ellipticity / 10³ units'));title(axs[0,1],'B','拟合之外还看残差','Inspect residuals as well as fit')
for k in range(3):
 axs[1,0].errorbar(cuts,cutfit[:,k],yerr=2*cutSD[:,k],fmt='-o',capsize=4,color=cols[k],label=names[k]);axs[1,0].axhline(truth[k],color=cols[k],ls=':',alpha=.4)
 axs[1,1].plot(scales,scalefit[:,k],'-o',color=cols[k],label=names[k]);axs[1,1].axhline(truth[k],color=cols[k],ls=':',alpha=.4)
axs[1,0].set(xlabel=tr('最低使用波长 / nm','Lowest fitted wavelength / nm'),ylabel=tr('拟合比例','Fitted fraction'),ylim=(0,.75));axs[1,0].legend(frameon=False,fontsize=9);title(axs[1,0],'C','波段改变可用信息','Wavelength coverage changes information')
axs[1,1].set(xlabel=tr('采用浓度 / 实际浓度','Assumed / actual concentration'),ylabel=tr('拟合比例','Fitted fraction'),ylim=(0,1));axs[1,1].legend(frameon=False,fontsize=9);title(axs[1,1],'D','浓度误差传到结构解释','Concentration error reaches interpretation')
fig.tight_layout();save(fig,'mixture')

T=np.linspace(20,90,71)
def thermal(temp,f0,fs,u0,us,mid,width):
 unfolded=expit((temp-mid)/width);return (f0+fs*(temp-20))*(1-unfolded)+(u0+us*(temp-20))*unfolded
thermal_true=[-25,.02,-3,.01,60,4]
heating=thermal(T,*thermal_true)+rng.normal(0,.12,len(T))
params,cov=curve_fit(thermal,T,heating,p0=thermal_true,bounds=([-50,-.5,-20,-.5,35,.5],[0,.5,20,.5,80,15]),maxfev=15000)
cooling=thermal(T,-25,.02,-3,.01,57,4)
frac=expit((T-params[4])/params[5]);baselineF=params[0]+params[1]*(T-20);baselineU=params[2]+params[3]*(T-20)
fig,axs=plt.subplots(1,2,figsize=(11.6,4.8));axs[0].scatter(T,heating,s=15,color=cols[1],alpha=.6,label=tr('构造升温读数','Constructed heating readings'));axs[0].plot(T,thermal(T,*params),color=cols[1],label=tr('升温拟合','Heating fit'));axs[0].plot(T,cooling,color=cols[2],ls='--',label=tr('示意冷却路径','Illustrative cooling path'));axs[0].plot(T,baselineF,color=gray,ls=':',lw=1);axs[0].plot(T,baselineU,color=gray,ls=':',lw=1);axs[0].set(xlabel=tr('温度 / °C','Temperature / °C'),ylabel=tr('222 nm 椭圆率 / mdeg','222 nm ellipticity / mdeg'));axs[0].legend(frameon=False,fontsize=9);title(axs[0],'A','同一信号，不同温度路径','One signal, different temperature paths')
axs[1].plot(T,frac,color=cols[0],lw=3);axs[1].axhline(.5,color=gray,ls='--');axs[1].axvline(params[4],color=gray,ls='--');axs[1].text(params[4]+2,.2,tr(f'中点 {params[4]:.2f} °C',f'Midpoint {params[4]:.2f} °C'),fontsize=10);axs[1].set(xlabel=tr('温度 / °C','Temperature / °C'),ylabel=tr('基线修正后的模型展开比例','Baseline-corrected model unfolded fraction'),ylim=(-.03,1.03));title(axs[1],'B','在同温度基线之间定位','Locate between same-temperature baselines')
fig.tight_layout();save(fig,'thermal')
np.savetxt(out/'spectra.csv',np.column_stack([w,scans,blanks.mean(axis=1),corrected,normalized,fitted]),delimiter=',',header='wavelength_nm,scan1_mdeg,scan2_mdeg,scan3_mdeg,scan4_mdeg,scan5_mdeg,blank_mean_mdeg,corrected_mdeg,mean_residue_ellipticity,fitted_mean_residue_ellipticity',comments='')
np.savetxt(out/'basis.csv',np.column_stack([w,basis]),delimiter=',',header='wavelength_nm,constructed_helix,constructed_sheet,constructed_other',comments='')
np.savetxt(out/'thermal.csv',np.column_stack([T,heating,thermal(T,*params),cooling,frac]),delimiter=',',header='temperature_C,heating_mdeg,fitted_mdeg,cooling_model_mdeg,model_unfolded_fraction',comments='')
np.savetxt(out/'fraction_resampling.csv',boot,delimiter=',',header='helix,sheet,other',comments='')
summary={'delta_absorbance_example':.5003-.4997,'ellipticity_example_mdeg':32980*.0006,'normalization_example':-20*110/(10*.20*.10),'fraction_helix':float(fit[0]),'fraction_sheet':float(fit[1]),'fraction_other':float(fit[2]),'fraction_sum':float(fit.sum()),'thermal_midpoint_C':float(params[4]),'thermal_width_C':float(params[5]),'midpoint_fraction':.5,'fraction_noise_interval':np.quantile(boot,[.025,.975],axis=0).tolist(),'data_kind':'constructed teaching spectra and thermal signals; no measured protein reference library'}
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
```

The complete program exports repeated scans, blank-corrected spectra, reference combinations, fraction sensitivities and thermal curves as CSV files, together with a numerical summary. Change one condition and trace which stage it affects: raw signal, normalization, structural fitting or temperature analysis. This is more informative than editing a final percentage. For real data, retain each scan and buffer blank and enter the actual concentration, path, wavelength range and temperature information. Replace the constructed basis curves with an appropriate validated analysis framework when estimating real structural composition.

## Align the CD experiment with the research decision

Combining far- and near-ultraviolet observations can refine the question. Local backbone organization may remain while the environments around aromatic side chains change, altering near-ultraviolet CD. Some proteins contain few suitable aromatic groups, and local motion or cancellation can make their near-ultraviolet response weak. Inspect sequence and optical properties when selecting the measurement. Each spectral region also needs its own concentration and path-length treatment because the signal strengths and transmission requirements differ. A weak response becomes interpretable when both the molecular reporter and the measurement conditions are understood.

For protein variants, first compare normalized spectra in the same buffer at the same temperature, then connect those observations to thermal transitions and function. Similar far-ultraviolet spectra with different activities direct attention toward local sites, tertiary organization, binding or kinetics. Similar overall secondary structure and identical biological function are different claims. If the spectra differ substantially, examine concentration, purity, aggregation and folding conditions before connecting the difference to a sequence-dependent conformational effect. Each complementary measurement addresses a specific alternative explanation.

Protein-material interactions require particular care about what is actually in the optical path. Suspended particles scatter light, surface-bound proteins can be oriented, and films can introduce linear dichroism or birefringence into a polarization measurement. Methods developed for randomly oriented molecules in solution cannot be transferred automatically to an oriented film. Compare suitable substrate blanks and orientations and use complementary structural measurements. Specify whether the observation concerns the suspension, supernatant or surface layer. Once the object is defined, CD can be connected meaningfully to adsorption amount, microscopy or material performance.

Storage studies benefit from following several observables together. Do spectral shape, soluble protein amount and activity change under the same storage conditions? If raw millidegrees decrease, separate loss of soluble protein from a change in the structure of individual molecules. If normalized shape changes, particle-size or separation measurements can reveal whether additional populations have appeared. This combination uses CD's strength in rapidly tracking ensemble conformation while assigning concentration, aggregation and function to measurements that directly address them.

Preserve an explanation that another reader can follow: the conditions sustaining the specimen, the amount of protein in the path, the reliable wavelength range, background subtraction and normalization, the reference model and the spectral features it explains. CD turns an otherwise vague impression that a chain has changed into a comparable optical observation. It can help choose a buffer, compare variants, identify a temperature window and investigate interactions with a material. Its usefulness grows when each curve is connected to the physical question that motivated the experiment.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/S05.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Greenfield: Using circular dichroism spectra to estimate protein secondary structure](https://pmc.ncbi.nlm.nih.gov/articles/PMC2728378/)

   Mechanism, specimen conditions, units and structural fitting.

   Public author manuscript; technical reference, no figures copied.
2. [JASCO: Circular Dichroism Spectroscopy](https://jascoinc.com/learning-center/theory/spectroscopy/circular-dichroism-spectroscopy/)

   Polarization, modulated optics and uses of different spectral regions.
3. [JASCO: Circular Dichroism Tips & Tricks](https://jascoinc.com/learning-center/best-practices/circular-dichroism-tips-tricks/)

   Path length, total absorption, detector voltage and integration time.
4. [Harvard CMI: Circular Dichroism](https://cmi.hms.harvard.edu/circular-dichroism)

   Buffer matching, concentration, aggregation checks and analysis tools.
5. [Mitchell: A Photo-electric Method for Measuring Circular Dichroism](https://www.nature.com/articles/166434b0)

   The 1950 primary abstract connects differential absorption and ellipticity measurement.

   Primary historical abstract consulted; no original figures reproduced.
