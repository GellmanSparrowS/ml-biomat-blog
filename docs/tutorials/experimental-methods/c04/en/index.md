# Gel electrophoresis: Separating biomolecules in a gel

Source: https://ml-biomat.com/tutorials/experimental-methods/c04/en/
Language: en

Read position, brightness and molecular state with the right reference for each band.

## Several questions can hide inside one bright band

Suppose an enzyme has been incorporated into a hydrogel so that it can be released gradually over several days. Detecting protein in the surrounding liquid is an encouraging start, but what has actually emerged? The material might release intact enzyme, smaller fragments produced by degradation, or a mixture. In another experiment, a protein purification produces a tube of clear liquid. Its appearance reveals little about whether it contains one main component or many molecules of similar size. Gel electrophoresis turns some of these invisible differences into spatial patterns. An electric field drives charged molecules through a water-filled polymer network. Groups that migrate at different rates separate along the gel and become visible after staining or fluorescence detection. A band is the collective distribution of many molecules, rather than a photograph of an individual molecule.

The resulting image supports several distinct measurements. Band position helps estimate molecular size; the number and distribution of bands describe components resolved under the chosen conditions; calibrated band signal can estimate the amount of a component. Each question requires its own reference. A size ladder contains molecules with known sizes. An amount calibration uses known loads of the same protein. Molecular identity may be investigated through antibody recognition, mass spectrometry, or nucleic-acid sequencing. Two different proteins can migrate to the same position and appear as one band. Deciding what to do next therefore begins with the intended conclusion: size, composition, identity, or biological function. The information becomes more useful when these goals are separated before the experiment.

Nucleic-acid experiments offer a familiar parallel. PCR makes many copies of a selected DNA region, and a gel can show whether the amplified material is concentrated around the expected length or includes additional products. DNA length is commonly expressed in base pairs, abbreviated bp, with 1000 bp making 1 kb. Protein size is commonly expressed in kilodaltons, or kDa. These are different rulers, so their reference ladders are chosen separately. This chapter moves from the physical reason molecules migrate to a constructed fluorescence gel containing a size ladder, known protein loads, and an unknown sample. Position and brightness will each have a calibration that answers the appropriate question.

## From a moving liquid boundary to a molecular sieve

Early electrophoresis did not require the familiar slab gel. In his 1937 work on serum proteins, Arne Tiselius observed boundaries moving through a solution under an electric field. Changes in protein concentration changed the refractive properties of the liquid, allowing optical detection of these boundaries. His apparatus used a flattened U-shaped liquid channel and operated at about 4°C to reduce thermal convection. The problem is easy to picture: if the liquid circulates vigorously, molecular populations with different migration speeds are mixed together again. The historical principle diagram places optical observation and cooling alongside the moving boundary because successful separation requires both a driving force and control of processes that erase the resulting differences.

![Original historical and modern mechanism diagrams. Left: cooling, optical boundaries and the U-shaped liquid channel in Tiselius’s 1937 work; not a dimensional reconstruction. Right: SDS treatment and disulfide reduction are distinct.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/ea5c4e08e9bd8c98805ab831.svg?v=ea5c4e08e9bd)

Figure 1Original historical and modern mechanism diagrams. Left: cooling, optical boundaries and the U-shaped liquid channel in Tiselius’s 1937 work; not a dimensional reconstruction. Right: SDS treatment and disulfide reduction are distinct.

A gel organizes the separation space differently. Much of its volume is water, while a continuous network restricts large-scale fluid motion. Dissolved molecules can still move through the water, but their passage through the network depends on size and conformation. Imagine pulling objects of different lengths and shapes through dense vegetation: the surroundings create different resistance to motion. At molecular scales, thermal motion continually changes chain conformations and the network contains a distribution of pore sizes, rather than a regular metal mesh. Agarose and polyacrylamide are two common gel materials. Changing gel composition changes the useful size window, making gel selection a choice about which molecular differences the experiment should resolve.

A potential difference between electrodes creates an electric field. Negatively charged molecules experience a force toward the positive electrode. Resistance from the surrounding liquid rapidly establishes an approximately steady average migration speed. Electrophoretic mobility summarizes the relation between this speed and the field. The equation below uses magnitudes, with direction described separately. It represents a locally uniform field at fixed temperature and buffer conditions; actual apparatus can have spatially varying fields. This distinction explains why voltage, channel length, and run duration all belong in the experimental record. The voltage on the power-supply display is only one part of the field experienced by the sample.

$$
E=\frac{V}{L},\qquad v=\mu E,\qquad d=vt
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | Magnitude of mean electric field, V/m. |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | Magnitude of applied potential difference, V. |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Channel length across that potential difference, m. |
| ![Formula](https://ml-biomat.com/static/agent-math/6ea26af94b3e02fd7aa1d744.svg) | Magnitude of mean migration speed, m/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | Magnitude of effective electrophoretic mobility at fixed conditions, m²/(V·s). |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | Migration distance in the specified direction, m. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Run time, s. |

For a uniform field at approximately fixed temperature and mobility, speed scales with field. V=100 V, L=0.10 m, μ=2×10⁻⁸ m²/(V·s) and t=1800 s give E=1000 V/m, v=20 micrometers/s and d=36 mm.

For a 10 cm channel under 100 V, the average field is 1000 V/m. A component with an effective mobility of 2×10⁻⁸ m²/(V·s) then moves at 20 micrometers per second and travels 36 mm in 30 minutes. These values demonstrate how the units connect; the mobility is a specified example rather than a universal protein property. Doubling voltage would double speed if mobility remained unchanged. Electrical current also generates heat, however, and temperature changes can alter the migration conditions. Curved bands, excessive spreading, and inconsistent migration across lanes call for investigation of temperature distribution, buffer composition, and loading differences. A curved band should first be understood as a spatial measurement problem before assigning new molecular sizes to its different parts.

## Choose which molecular structures the experiment should preserve

The phosphate backbone of DNA usually carries negative charge. Longer chains have more charge as well as greater resistance to motion; a gel adds size-dependent constraints that allow linear fragments of different lengths to separate. Proteins present a more complicated case. Their amino-acid compositions produce different arrangements of positive and negative groups, and the net charge changes with pH. Two proteins of equal mass may therefore migrate differently in native electrophoresis because their charge and shape differ. Native conditions aim to preserve aspects of the original molecular state. Whether a particular complex remains assembled depends on the buffer, dilution, run duration, and stability of its interactions. Those conditions become part of the scientific question when the experiment asks whether a complex dissociates.

Sodium dodecyl sulfate, abbreviated SDS, is a negatively charged surfactant. It binds to many proteins and promotes unfolding, reducing differences in original shape and charge so that size becomes a major determinant of migration. PAGE means polyacrylamide gel electrophoresis. Thinking of different proteins as participants given approximately uniform equipment helps explain how an SDS-PAGE size ruler can be constructed. Actual binding behavior still depends on the molecule. Glycosylation and other unusual compositions can alter migration relative to ordinary standards. The reported result is therefore an apparent size obtained by comparison under the selected conditions. When a research question concerns modifications or precise molecular mass, this estimate can guide a complementary mass-spectrometry measurement.

Unfolding and breaking covalent connections are different operations. Two protein subunits may be linked by a disulfide bond, a covalent connection between sulfur atoms. SDS alters folding and noncovalent interactions, whereas a reducing agent breaks disulfides. Consider two 40 kDa subunits connected only by a disulfide. Under nonreducing SDS conditions, a component around 80 kDa may remain; reduction produces material around 40 kDa. The lower band contains the combined amount of the two original subunits, so half the protein has not disappeared. Comparing these conditions tests whether an observed connection depends on a disulfide. If a material introduces other covalent crosslinks, those connections must also be included in the structural explanation.

![Original conceptual diagrams, not experimental results. A assumes two 40 kDa subunits connected only by a disulfide and compares nonreducing with reducing SDS conditions. B shows conformations of equal-length DNA and why a linear ladder needs an appropriate comparison.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/3d3fef18d9f7e64610dbcec8.svg?v=3d3fef18d9f7)

Figure 2Original conceptual diagrams, not experimental results. A assumes two 40 kDa subunits connected only by a disulfide and compares nonreducing with reducing SDS conditions. B shows conformations of equal-length DNA and why a linear ladder needs an appropriate comparison.

The development of high-resolution SDS gels was closely connected to a specific biological problem. Laemmli’s 1970 work examined cleavage of structural proteins during assembly of the bacteriophage T4 head. Jonathan King, who participated in the research community involved, later described how resolving proteins in complex mixtures allowed genetic perturbations to be connected with missing or altered structural components. The useful historical lesson is an experimental relationship: a defined biological change becomes interpretable when a separation method reveals which molecular groups change with it. Comparisons of protein fragments before and after material treatment, of reduced and nonreduced samples, and of successive purification fractions use the same basic reasoning. The gel becomes informative through the contrast built into the experiment.

## Put samples, references, and controls into the same comparison

Much of a gel’s explanatory power is determined before loading. A purification study might place starting material, flow-through, wash, and elution fractions in adjacent lanes. A release study might compare the original protein, a material-only blank, and samples collected at several times. A lane is the longitudinal region originating from one loading well and should correspond to an explicitly identified sample. Equal total protein loads are often useful for comparing composition. Equal equivalents of the original culture volume may be more useful for comparing production yield. These normalizations answer different questions. Recording original sample volume and dilution prevents visually similar bands from concealing large differences in total recovered protein.

The size ladder should cover the region containing the target. A higher gel concentration generally creates a tighter sieving environment that can improve some small-molecule separations while restricting entry or separation of larger components. A gradient gel changes composition along the migration direction and can cover a broader range, but its calibration must still be established with the actual standards. For DNA, establish whether the material consists of linear fragments or circular plasmids. Open circular, supercoiled, and linear DNA of equal length can migrate differently because their conformations differ. Comparing an uncut plasmid directly with a linear DNA ladder can turn a shape difference into an apparent length difference. An appropriate linearization experiment often resolves the ambiguity more effectively than reporting additional decimal places.

Salt, solvent, and sample volume also affect the starting conditions. Salt ions conduct current, so a high local salt concentration can change the electrical and thermal environment. A large sample volume starts migration from a broad region, making neighboring components harder to resolve. Many discontinuous protein systems include a stacking region that concentrates the sample into a narrow starting zone through the behavior of different buffer ions. The analogy is arranging runners at a common starting line before comparing their speeds; the underlying mechanism involves ion migration and acid–base equilibria. Gel, sample buffer, and electrode buffer consequently form a coordinated chemical system. They should be selected together rather than treated as interchangeable accessories.

After the run, the molecules are separated but still need to be detected. Dyes differ in binding behavior, sensitivity, background, and usable linear range. Fluorescence imaging records detector response to emitted light. A dark band in a transmitted-light image instead reduces transmitted intensity, and quantitative interpretation may require conversion to optical density. The same raw grayscale subtraction does not automatically describe both measurements. The complete example here specifies linear fluorescence response for the same protein under consistent staining conditions and without detector saturation. This definition gives each calculation a clear object. When adapting the method to another instrument, the first task is to establish how that instrument’s recorded pixel values relate to the detected signal.

## Read position first: Establish a size ruler

Every band in the example image is constructed from a two-dimensional Gaussian distribution, with fixed-seed random noise and a slowly varying background. This is a teaching image rather than an experimental specimen. Its structure retains the features needed for quantitative analysis: five known sizes in the ladder, followed by a blank, standards containing 20, 40, and 80 ng of protein, and an unknown sample. The unknown has a major band around 40 kDa and a smaller component around 25 kDa. Molecular size and loaded amount are separate variables. Having both “40 kDa” and “40 ng” in the same figure is a useful exercise in distinguishing the size of one molecule from the total amount of that molecular population in a lane.

![Constructed fluorescence data, seed 640. L contains 100, 70, 40, 25 and 15 kDa markers; standard loads are 0, 20, 40 and 80 ng. U contains 55 ng major and 12 ng minor components. Dashed lines mark origin and reference front. Position and intensity are calibrated separately.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/dea64c2b4054516c4d8916f8.svg?v=dea64c2b4054)

Figure 3Constructed fluorescence data, seed 640. L contains 100, 70, 40, 25 and 15 kDa markers; standard loads are 0, 20, 40 and 80 ng. U contains 55 ng major and 12 ng minor components. Dashed lines mark origin and reference front. Position and intensity are calibrated separately.

Migration distances are measured from a common origin, such as the beginning of the resolving region. Dividing the distance from this origin to a band center by the distance to a designated reference front gives a dimensionless relative migration, Rf. The front is a reference for run progress, not a protein of known molecular size. If both distances are measured in image pixels, those units cancel; converting the photograph to millimeters is unnecessary for this ratio. A tilted image requires identification of the proper lane direction. When migration varies across the gel, nearby or repeated ladder lanes provide a better local reference than forcing all bands onto one horizontal coordinate system.

$$
R_f=\frac{d_{\mathrm{band}}}{d_{\mathrm{front}}},\qquad \log_{10}\!\left(\frac{M}{1\,\mathrm{kDa}}\right)=a+bR_f
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/2fefa7f4702f6dc2c446e8bb.svg) | Relative migration, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/02a6a84c4c5d4eb323805b4f.svg) | Distance from the common origin to band center, pixels or mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/2abe6535cfb35c678786bb92.svg) | Distance from the same origin to the reference front, in matching units. |
| ![Formula](https://ml-biomat.com/static/agent-math/34058a2a5d1de088feed7d98.svg) | Apparent protein mass calibrated against standards, kDa. |
| ![Formula](https://ml-biomat.com/static/agent-math/689da198c2dfc062dc6a4362.svg) | Empirical intercept and slope over the selected linear interval, both dimensionless. |

The distance ratio removes image scaling; mass is divided by 1 kDa before taking a logarithm. The constructed model a=2.1 and b=−1.25 gives Rf≈0.398352 for 40 kDa. Noisy ladder centers are refitted and the target is interpolated locally.

Why take the logarithm of mass? Within a useful interval for a selected gel system, a straight line often approximates the relationship between logarithmic protein mass and relative migration. This is an empirical calibration established by standards. The axis log₁₀(M/kDa) means that mass is first divided by 1 kDa to obtain a number, then expressed as a base-ten logarithm. On this ruler, 100, 10, and 1 kDa correspond to 2, 1, and 0. The constructed example uses an intercept of 2.1 and a slope of −1.25, placing 40 kDa at Rf approximately 0.398. The program locates ladder bands again in the noisy image and refits the relationship, giving an unknown major-band estimate close to 40 kDa.

Inspect the actual ladder points before accepting the fitted line. Large molecules near the top may crowd together, while small components near the front may depart from the selected approximation. A narrower calibration interval around the target or a different gel may provide a more useful ruler. Extending a fitted line far beyond the standards makes the result increasingly dependent on the assumed relationship. Broad bands also introduce uncertainty in defining the center. Comparing the peak maximum, an intensity-weighted center, and a fitted center can reveal whether the reported location depends strongly on that choice. Repeated gels show an additional source of variability. A result such as “approximately 40 kDa” then rests on observable reference relationships rather than on a familiar-looking location.

## Read brightness through background, area, and saturation

The same amount of protein can produce a taller peak when concentrated into a narrow band than when spread over a wider one. Quantitation therefore usually integrates an area containing the whole band rather than relying on the brightest pixel. Imagine measuring the volume of a small hill: height and footprint both matter. A region of interest, abbreviated ROI, defines the pixels being added. Green outlines mark the target integration region; nearby blue regions estimate background where no clear band is present. Nearby background captures local staining and illumination conditions. If background varies across an image, a value measured in a distant corner may be a poor estimate for the target. The ROI should also avoid neighboring lanes and other bands that would contribute unrelated signal.

$$
S=\sum_{p=1}^{N}(I_p-\bar B)=\sum_{p=1}^{N}I_p-N\bar B
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | Background-corrected integrated signal, counts. |
| ![Formula](https://ml-biomat.com/static/agent-math/48c7b594e8628a17b991d4e6.svg) | Pixel index within the selected region, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Number of pixels in the integration region, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/44d9fad31d63f36e8d73e778.svg) | Fluorescence count in pixel p, counts. |
| ![Formula](https://ml-biomat.com/static/agent-math/9744967524d2194c13c2ad4e.svg) | Estimated mean background per pixel at the target, counts. |

For linear fluorescence response, summation collects the band and subtraction removes expected local background. N=1107, raw sum=240000 and background=100 give 129300 net counts. A 2-count background error per pixel changes the integral by 2214 counts.

The example ROI contains 41×27, or 1107, pixels. If their summed signal were 240,000 counts and mean background were 100 counts per pixel, the background contribution would be 110,700 counts and the net integral 129,300 counts. An error of just 2 counts per pixel in the background estimate would change the result by 2214 counts. That can be a substantial fraction of a weak band. The program samples small regions above and below the target. Because the constructed background changes approximately linearly with row number, symmetric sampling helps estimate background at the band. Both the net integral and the estimated background are exported, making it possible to distinguish a change in the band from a change in its surroundings.

![A, B and D analyze the same simulated image, with one lane per standard. C models clipping of a continuous two-dimensional Gaussian with a detector ceiling of 4095 total counts and a 100-count background, followed by exposure correction. D varies the ROI half-height while retaining the background and calibration definitions.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/b8cbe1ed2fef01b2d621c00d.svg?v=b8cbe1ed2fef)

Figure 4A, B and D analyze the same simulated image, with one lane per standard. C models clipping of a continuous two-dimensional Gaussian with a detector ceiling of 4095 total counts and a 100-count background, followed by exposure correction. D varies the ROI half-height while retaining the background and calibration definitions.

A net integral is still measured in detector counts. Known loads of the same protein establish the relationship to mass. The program fits the blank and three standards, then converts the unknown major-band signal into a load close to 55 ng. To obtain concentration, divide by the volume loaded and then account for dilution. For example, 55 ng in 5 microliters corresponds to 11 ng per microliter. If the sample underwent a twofold dilution before loading, the original solution corresponds to 22 ng per microliter. Specify whether the stated volume and concentration refer to the solution before or after addition of loading buffer, since mixing changes total volume. The arithmetic follows the actual amount transferred into the lane.

$$
S=km+b_0,\qquad \hat m=\frac{S-b_0}{k},\qquad c=\frac{\hat m}{V_s}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | Net integrated signal, counts. |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | Calibration slope for the same protein at fixed exposure and staining, counts/ng. |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Known standard mass entering the lane, ng. |
| ![Formula](https://ml-biomat.com/static/agent-math/1786b0ad5e438341adfba90f.svg) | Calibration intercept, counts. |
| ![Formula](https://ml-biomat.com/static/agent-math/f35e2a884154f04380ef47f1.svg) | Estimated unknown mass entering the lane, ng. |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | Concentration of the corresponding loaded solution, ng/microliter. |
| ![Formula](https://ml-biomat.com/static/agent-math/af24cfe08968b9a399cca9b4.svg) | Loaded volume corresponding to that mass, microliters. |

Known loads of the same protein establish a response ruler in the linear range. k=2200 counts/ng, b₀=500 counts and S=121500 counts give 55 ng; 5 microliters gives 11 ng/microliter, or 22 before a twofold dilution. The program estimates its own slope and intercept from the image.

Different proteins at equal mass may stain differently because dye binding depends on molecular composition. Dividing a major-band integral by the summed integral of a lane therefore gives a signal fraction under the selected detection conditions. Interpreting that fraction as a mass fraction adds an equal-response assumption or requires appropriate response calibration. The constructed example deliberately gives the major band 55 ng, the minor band 12 ng, and both the same response per unit mass. Its major-band mass fraction is consequently 55/67, about 82.1%. In a purification study, the signal fraction can be reported directly and refined through standards, complementary detection, or a mass balance. Small fragments that have left the imaged region also affect which material belongs in the denominator.

Excessive exposure introduces a different error. Once a detector reaches its maximum recorded value, additional photons no longer increase that pixel value. In the illustrated 12-bit detector model, the ceiling is 4095 counts. The center of a bright band becomes clipped, causing a linear calibration to underestimate mass. Reducing display brightness changes appearance but cannot recover the missing counts. The interactive experiment varies protein load, exposure time, and background while showing the profile of the same Gaussian band. It uses the analytic integral of a clipped two-dimensional Gaussian to calculate the apparent mass after exposure correction. This connects a visible flat top with the quantitative loss rather than presenting saturation as an unexplained warning threshold.

The interactive model uses a shape whose clipping loss can be calculated exactly: signal decreases smoothly away from a Gaussian center, and clipping removes the central excess. Dividing the recorded net integral by its ideal value gives the retained fraction; multiplying by true mass gives apparent mass. The expression below is the integral result for a continuous two-dimensional Gaussian with constant background and a region covering the entire band. It isolates clipping itself, whereas the preceding pixel analysis also considers a finite integration region and estimated background.

$$
A=\kappa mt,\quad H=C_{\max}-B,\quad \hat m_{\mathrm{clip}}=m\begin{cases}1,&A\le H,\\ \dfrac{H}{A}\left[1+\ln\!\left(\dfrac{A}{H}\right)\right],&A>H.\end{cases}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Ideal peak signal above background, counts. |
| ![Formula](https://ml-biomat.com/static/agent-math/cb154160fd6d330501f6321c.svg) | Peak-response coefficient, 20 counts/(ng·s). |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | True loaded mass, ng. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Exposure time, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/6d6950da29507eb4f6b78d53.svg) | Recordable signal headroom above background, counts. |
| ![Formula](https://ml-biomat.com/static/agent-math/139d2bc88abb1cc4b4d82e6b.svg) | Detector ceiling, 4095 counts. |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | Constant per-pixel background, counts. |
| ![Formula](https://ml-biomat.com/static/agent-math/c6ce7831fa820eaf1c2509a4.svg) | Apparent mass from the integrated, exposure-corrected signal using the ideal linear calibration, ng. |

For a continuous 2D Gaussian, flatten the center above H and integrate over the full plane to obtain the retained fraction; ln denotes natural logarithm. m=100 ng, t=4 s and B=100 give A=8000, H=3995 and about 84.61 ng apparent mass. Background is constant, no other noise is included, and the integration region covers the entire band.

## When does a band become clipped?

Change load, exposure and background. The teaching model is a continuous 2D Gaussian fluorescence band, with peak coefficient 20 counts/(ng·s) and ceiling 4095. Its integral is corrected for exposure. Compare the linear region with clipped mass estimates.

[Figure: Interactive Gaussian band exposure and clipping](https://ml-biomat.com/tutorials/experimental-methods/c04/en/#C04-plot)

Useful exposure selection balances two observable effects. Shorter exposure protects strong bands from clipping but leaves weaker signals closer to background fluctuations. A series of exposures can reveal a region in which the background-corrected integral scales with exposure while the calculated amount remains stable. Standards and unknowns must be compared using consistent response information. If one image requires a different exposure, the correction should be supported by the detector’s linear behavior rather than assumed from the display. Inspecting raw pixel maxima alongside integrated signals is particularly helpful because an apparently smooth image may already contain clipped pixels at the centers of its brightest bands.

## Turn the image into a decision for the next experiment

The complete program starts with a two-dimensional detector-count array and preserves it before display adjustment. It then locates ladder bands, calibrates size, estimates local background, and infers loaded mass. The exported array supports recalculation, the unknown-lane profile reveals the major and minor components, and the calibration table retains both known loads and measured integrals. A separate diagnostic varies the integration region’s half-height. A narrow region misses the band tails; expanding it approaches a plateau as most of the signal is included. Expanding far enough to include another band would introduce a different component. This sensitivity check helps select an analysis region from the actual signal rather than from one visually convenient rectangle.

### Complete gel image, size calibration and band quantitation

Generates explicitly constructed 2D fluorescence data, preserves the raw array and outputs two calibrations, background analysis and clipping diagnostics.

```
"""Constructed electrophoresis images and quantitative diagnostics; no network needed."""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,Ellipse

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 zh=a.language=='zh';T=lambda z,e:z if zh else e
 plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.titlesize':13,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fcfbf7','axes.facecolor':'#fcfbf7','savefig.facecolor':'#fcfbf7'})
 B,R,G,Y='#167d9a','#d35f47','#37967d','#c49b35'
 def save(f,n):
  f.savefig(a.output/f'{n}-{a.language}.svg');f.savefig(a.output/f'{n}-{a.language}.png',dpi=145);plt.close(f)
 def text(ax,x,y,z,e,**kw):ax.text(x,y,T(z,e),**kw)
 def arrow(ax,x1,y1,x2,y2,col=B):ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops={'arrowstyle':'->','color':col,'lw':2})
 # Original historical mechanism, not an image of an actual historical experiment.
 f,axes=plt.subplots(1,2,figsize=(13.4,5.3),layout='constrained')
 for ax in axes:ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off')
 ax=axes[0];ax.set_title(T('A  1937：追踪溶液中的移动界面','A  1937: Follow a boundary in solution'),loc='left')
 ax.plot([2,2,2.4,6.6,7,7],[6.5,2,1.5,1.5,2,6.5],color='#9ac0cd',lw=30,solid_capstyle='butt');ax.plot([2,2,2.4,6.6,7,7],[6.5,2,1.5,1.5,2,6.5],color=B,lw=1)
 for y in [3.6,4.2,4.8]:ax.plot([1.62,2.38],[y,y],color=R,lw=3)
 arrow(ax,.3,4.2,3.8,4.2,G);text(ax,.15,5.1,'折射率梯度 → 光学界面','Refractive gradient → optical boundary',fontsize=10)
 text(ax,4.2,6.1,'缓冲液','Buffer',ha='center');text(ax,2,7,'−', '−',ha='center',fontsize=20);text(ax,7,7,'+', '+',ha='center',fontsize=20)
 text(ax,.3,.25,'蒂塞利乌斯：冷却至约 4°C，减小热对流\n原理图；溶液中没有凝胶筛网','Tiselius: about 4°C to suppress convection\nPrinciple diagram; no gel sieve in the liquid',fontsize=10)
 ax=axes[1];ax.set_title(T('B  现代凝胶：电驱动 + 分子筛','B  Modern gels: Electric drive + molecular sieve'),loc='left')
 ax.add_patch(Rectangle((1.6,1.4),5.8,5.3,facecolor='#e2edf0',edgecolor=B))
 for x in np.arange(1.8,7.5,.6):ax.plot([x,x],[1.4,6.7],color='#bfd3da',lw=.6)
 for y in np.arange(1.6,6.7,.5):ax.plot([1.6,7.4],[y,y],color='#bfd3da',lw=.6)
 for x in [2.7,4.5,6.3]:ax.add_patch(Rectangle((x-.45,6.2),.9,.5,fc='#fcfbf7',ec=B))
 for x,y in [(2.7,4.9),(2.7,3),(4.5,4.4),(4.5,2.1),(6.3,3.7)]:ax.plot([x-.4,x+.4],[y,y],lw=8,color=R)
 arrow(ax,8.4,6.3,8.4,2);text(ax,8.7,4,'向正极','Toward +',rotation=90,va='center')
 text(ax,1.8,.25,'SDS 改变蛋白质的电荷与形状\n还原剂另行切断二硫键','SDS changes protein charge and shape\nA reducing agent separately breaks disulfides',fontsize=10)
 save(f,'history-mechanism')
 # Constructed raw fluorescence image: all lanes share detector and dye response.
 rng=np.random.default_rng(640);yy,xx=np.mgrid[:360,:390];origin,front=25.,335.;xs=np.array([45,105,165,225,285,345]);masses=np.array([100,70,40,25,15.]);rf=(2.1-np.log10(masses))/1.25;ys=origin+(front-origin)*rf
 center=lambda m:origin+(front-origin)*(2.1-np.log10(m))/1.25
 raw=100+.03*yy+np.zeros_like(xx,dtype=float)
 def band(x,y,ng):return 20*ng*np.exp(-.5*((xx-x)/6)**2-.5*((yy-y)/3)**2)
 for y in ys:raw+=band(xs[0],y,35)
 loads=np.array([0,20,40,80,55.])
 for x,m in zip(xs[1:],loads):raw+=band(x,center(40),m)
 raw+=band(xs[-1],center(25),12);raw=np.round(np.maximum(0,raw+rng.normal(0,3,raw.shape))).astype(np.uint16)
 yc=int(round(center(40)));xhalf=20;yhalf=13
 def measure(x,y):
  cy=int(round(y));roi=raw[cy-yhalf:cy+yhalf+1,int(x)-xhalf:int(x)+xhalf+1].astype(float)
  strips=np.concatenate([raw[cy-24:cy-17,int(x)-xhalf:int(x)+xhalf+1].ravel(),raw[cy+18:cy+25,int(x)-xhalf:int(x)+xhalf+1].ravel()]);bg=float(strips.mean())
  return float(roi.sum()-roi.size*bg),bg
 results=np.array([measure(x,center(40)) for x in xs[1:]]);coef=np.polyfit(loads[:4],results[:4,0],1);estimate=(results[-1,0]-coef[1])/coef[0]
 # Locate ladder maxima from local profiles, then estimate size in the same gel.
 detected=[]
 for y in ys:
  profile=raw[:,25:66].mean(axis=1);window=np.arange(int(y)-6,int(y)+7);detected.append(window[np.argmax(profile[window])])
 detected=np.array(detected);fit=np.polyfit((detected-origin)/(front-origin),np.log10(masses),1)
 uprofile=raw[:,325:366].mean(axis=1);win=np.arange(yc-8,yc+9);uy=int(win[np.argmax(uprofile[win])]);mass_est=10**np.polyval(fit,(uy-origin)/(front-origin))
 f=plt.figure(figsize=(13.6,7.5),layout='constrained');gs=f.add_gridspec(2,2,width_ratios=[1.1,1]);ax=f.add_subplot(gs[:,0]);im=ax.imshow(raw,cmap='magma',vmin=90,vmax=1800,origin='upper');ax.set_xticks(xs,['L','0','20','40','80','U']);ax.xaxis.tick_top();ax.set_xlabel(T('标准 / ng；U = 未知样品','Standards / ng; U = unknown'));ax.xaxis.set_label_position('top');ax.set_ylabel(T('图像行 / pixel','Image row / pixel'));ax.set_title(T('A  构造的原始荧光图','A  Constructed raw fluorescence image'),loc='left',pad=48)
 ax.axhline(origin,color='white',lw=.8,ls='--');ax.axhline(front,color='white',lw=.8,ls='--');ax.add_patch(Rectangle((325,yc-yhalf),41,27,fc='none',ec='#76dccb',lw=1.6));f.colorbar(im,ax=ax,shrink=.7,label=T('探测器计数','Detector counts'))
 ax=f.add_subplot(gs[0,1]);dx=(detected-origin)/(front-origin);ax.scatter(dx,np.log10(masses),c=B);grid=np.linspace(0,.85,100);ax.plot(grid,np.polyval(fit,grid),color=B);ax.scatter((uy-origin)/(front-origin),np.log10(mass_est),c=R,zorder=4);ax.annotate(f'U: {mass_est:.1f} kDa',((uy-origin)/(front-origin),np.log10(mass_est)),xytext=(.5,1.85),arrowprops={'arrowstyle':'->','color':R});ax.set(xlabel=T('相对迁移距离 Rf','Relative migration Rf'),ylabel='log₁₀(M / kDa)',title=T('B  同一块胶的大小校准','B  Size calibration on the same gel'))
 ax=f.add_subplot(gs[1,1]);ax.plot(np.arange(360),uprofile,color=R);ax.axvspan(yc-13,yc+13,color=G,alpha=.18);ax.axvline(center(25),color=B,ls=':');ax.set(xlabel=T('图像行 / pixel','Image row / pixel'),ylabel=T('泳道平均计数','Lane-mean counts'),title=T('C  未知泳道：40 kDa 主带与 25 kDa 次带','C  Unknown lane: 40 kDa major, 25 kDa minor'))
 save(f,'gel-size')
 # Analytic integration of a clipped two-dimensional Gaussian band.
 def apparent(m,t,bg):
  amp=20*np.asarray(m)*t;cap=4095-bg;ratio=np.ones_like(amp,dtype=float);mask=amp>cap;ratio[mask]=cap/amp[mask]*(1+np.log(amp[mask]/cap));return np.asarray(m)*ratio
 f,ax=plt.subplots(2,2,figsize=(13.6,8),layout='constrained')
 crop=raw[yc-27:yc+28,320:371];ax[0,0].imshow(crop,cmap='magma',vmin=90,vmax=1800,extent=(320,371,yc+28,yc-27));ax[0,0].add_patch(Rectangle((325,yc-13),41,27,fc='none',ec=G,lw=2));
 for y in [yc-24,yc+18]:ax[0,0].add_patch(Rectangle((325,y),41,7,fc='none',ec=B,lw=2))
 ax[0,0].set(xlabel=T('图像列 / pixel','Image column / pixel'),ylabel=T('图像行 / pixel','Image row / pixel'),title=T('A  绿色积分区；蓝色背景区','A  Green integration; blue background'))
 ax[0,1].scatter(loads[:4],results[:4,0]/1000,c=B);ax[0,1].plot([0,85],np.polyval(coef,[0,85])/1000,color=B);ax[0,1].scatter(estimate,results[-1,0]/1000,c=R);ax[0,1].annotate(f'U = {estimate:.2f} ng',(estimate,results[-1,0]/1000),xytext=(12,155),arrowprops={'arrowstyle':'->','color':R});ax[0,1].set(xlabel=T('同一蛋白质的上样质量 / ng','Loaded mass of the same protein / ng'),ylabel=T('净积分 / 10³ counts','Net integral / 10³ counts'),title=T('B  背景扣除后反算质量','B  Infer mass after background subtraction'))
 ml=np.linspace(0,200,201)
 for t,c in [(1,B),(4,R),(8,Y)]:ax[1,0].plot(ml,apparent(ml,t,100),c=c,label=f'{t} s')
 ax[1,0].plot(ml,ml,'--',c='#6f7883',label=T('理想线性','Ideal linear'));ax[1,0].legend();ax[1,0].set(xlabel=T('真实上样质量 / ng','True loaded mass / ng'),ylabel=T('按曝光校正的表观质量 / ng','Exposure-corrected apparent mass / ng'),title=T('C  12 位探测器削顶造成低估','C  Clipping by a 12-bit detector causes underestimation'))
 widths=np.arange(2,23);integ=[]
 for w in widths:integ.append((raw[yc-w:yc+w+1,325:366].astype(float).sum()-(2*w+1)*41*results[-1,1]-coef[1])/coef[0])
 ax[1,1].plot(widths,integ,c=G);ax[1,1].axhline(55,c=R,ls='--');ax[1,1].set(xlabel=T('积分区域半高 / pixel','Integration half-height / pixel'),ylabel=T('未知样品估计质量 / ng','Estimated unknown mass / ng'),title=T('D  积分区太窄会漏掉带的两侧','D  A narrow region misses band tails'))
 save(f,'quantitation')
 f,axs=plt.subplots(1,2,figsize=(13.6,5.6),layout='constrained')
 for ax in axs:ax.set(xlim=(0,10),ylim=(0,9));ax.axis('off')
 ax=axs[0];ax.set_title(T('A  二硫键连接的两个 40 kDa 亚基','A  Two 40 kDa subunits joined by a disulfide'),loc='left')
 for x in [2,7]:ax.add_patch(Circle((x,7),.8,fc='#b9dbe3',ec=B));text(ax,x,7,'40','40',ha='center',va='center')
 ax.plot([2.8,6.2],[7,7],c=Y,lw=3);text(ax,4.5,7.3,'S—S','S—S',ha='center');arrow(ax,2.5,5.6,2.5,4.7);arrow(ax,7,5.6,7,4.7)
 for x,label,y in [(2.5,T('非还原 SDS','Nonreducing SDS'),3.9),(7,T('还原 SDS','Reducing SDS'),2.1)]:
  ax.add_patch(Rectangle((x-.75,1.2),1.5,3.4,fc='#e2edf0',ec=B));ax.plot([x-.5,x+.5],[y,y],lw=9,color=R);text(ax,x,.6,label,label,ha='center',fontsize=10)
 text(ax,.2,3.9,'80 kDa','80 kDa',fontsize=10);text(ax,8,2.1,'40 kDa','40 kDa',fontsize=10);text(ax,.3,8.2,'构造关系示意；假定亚基无其他共价交联','Constructed relationship; no other covalent crosslinks',fontsize=9)
 ax=axs[1];ax.set_title(T('B  同样长度的 DNA 可以有不同形状','B  DNA of equal length can have different shapes'),loc='left')
 ax.add_patch(Ellipse((2,6.7),2.4,1.4,fill=False,ec=B,lw=2));text(ax,2,5.4,'开环','Open circular',ha='center')
 x=np.linspace(0,2*np.pi,200);ax.plot(6.8+1.2*np.cos(x),6.7+.35*np.sin(3*x),c=R,lw=2);text(ax,6.8,5.4,'超螺旋','Supercoiled',ha='center')
 ax.plot([1,8],[3.4,3.4],color=G,lw=2);text(ax,4.5,2.5,'线性化后再与线性标记比较','Linearize before comparison with a linear ladder',ha='center',fontsize=10)
 text(ax,.4,.6,'形状改变摩擦与穿孔方式\n迁移快慢还取决于胶和实验条件','Conformation changes drag and pore passage\nMigration also depends on gel and run conditions',fontsize=10)
 save(f,'molecular-forms')
 np.savez_compressed(a.output/'constructed_gel.npz',raw_counts=raw,lane_centers=xs,origin=origin,front=front)
 np.savetxt(a.output/'ladder.csv',np.c_[masses,detected,(detected-origin)/(front-origin)],delimiter=',',header='mass_kDa,image_row_px,Rf',comments='')
 np.savetxt(a.output/'quantitation.csv',np.c_[loads,results],delimiter=',',header='true_mass_ng,net_integral_counts,background_counts_per_pixel',comments='')
 np.savetxt(a.output/'unknown_profile.csv',np.c_[np.arange(360),uprofile],delimiter=',',header='image_row_px,mean_counts',comments='')
 summary={'estimated_mass_kDa':float(mass_est),'estimated_load_ng':float(estimate),'calibration_slope_counts_per_ng':float(coef[0]),'calibration_intercept_counts':float(coef[1]),'image_max_counts':int(raw.max()),'ideal_Rf_40kDa':float((2.1-np.log10(40))/1.25),'field_V_per_m':1000.,'speed_um_per_s':20.,'distance_30min_mm':36.,'clipped_100ng_4s_apparent_ng':float(apparent(100.,4.,100.)),'target_mass_fraction_equal_response':55/67,'roi_pixels':41*27,'unknown_background_counts_per_pixel':float(results[-1,1])}
 (a.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
```

To adapt the example to a fluorescence gel, replace the image array and establish its bit depth, offset, saturation value, and any camera-background corrections already applied. Enter the measured ladder sizes, lane locations, origin, and reference front. Check the calibration interval against the standards, then choose amount standards matched to the unknown protein. Automated maxima still need to be compared with the image because dust, bubbles, and staining defects can also generate bright features. Retain the complete image, the mapping between lanes and samples, and any crop boundaries. These records allow another reader to follow the analysis without reconstructing what might have been removed from the displayed panel.

For the enzyme-release problem, a major band close to the original enzyme’s apparent size and an increasing recovered amount provide a reason to measure catalytic activity next. If lower-size bands accumulate, comparisons of storage conditions, protease activity, or material interactions can investigate the appearance of fragments. Include a material-only blank because leached components may influence background, staining, or loading conditions. In purification, multiply concentration by each fraction’s total volume to estimate recovery, then ask whether increasing purity is accompanied by major loss of the target. A band thus becomes the starting point for an experiment that tests a specific explanation rather than an attractive endpoint on a page.

Replication should follow the same question. Redrawing an ROI on one image explores analysis sensitivity. Loading the same solution twice adds variation from loading and separation. Independent protein preparations or separately prepared material samples include preparation and biological differences. Combining these levels into one unexplained standard deviation obscures what an error bar describes. Before measuring molecular binding, electrophoresis can assess components and degradation, while size-exclusion measurements examine aggregation in solution. Calorimetry or surface-binding measurements can then address interactions. Together, these methods connect what the sample contains, the state it occupies, and how it participates in the process being studied.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/C04.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Tiselius (1937): Electrophoresis of serum globulin](https://pmc.ncbi.nlm.nih.gov/articles/PMC1267100/)

   Original pages 1464–1465: U-shaped liquid channel, 4°C cooling and optical boundaries.
2. [King (2022): Using T4 genetics and Laemmli’s development of high-resolution SDS gel electrophoresis](https://pmc.ncbi.nlm.nih.gov/articles/PMC9576892/)

   Firsthand history connecting high-resolution gels with T4 structural-protein research.

   CC BY 4.0 article; historical reference only, no article artwork reproduced.
3. [Thermo Fisher: Overview of electrophoresis](https://www.thermofisher.com/us/en/home/life-science/protein-biology/protein-biology-learning-center/protein-biology-resource-library/pierce-protein-methods/overview-electrophoresis.html)

   Native versus SDS conditions, pore size, stacking and gel selection.
4. [Bio-Rad: A Guide to Polyacrylamide Gel Electrophoresis and Detection](https://www.bio-rad.com/webroot/web/pdf/lsr/literature/Bulletin_6040A.pdf)

   Field and Joule heating, same-gel size calibration, staining response and quantitation.
5. [QIAGEN: DNA analysis using analytical gels](https://www.qiagen.com/en-gb/knowledge-and-support/knowledge-hub/bench-guide/dna/analysing-dna/dna-analysis-using-analytical-gels)

   DNA conformation, gel concentration, sample and buffer conditions.
6. [ImageJ: Analyze menu and gel analysis](https://imagej.net/ij/docs/menus/analyze.html)

   Raw grayscale, lane profiles, region integration and background.
