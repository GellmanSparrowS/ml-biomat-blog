# UV–visible absorption: Turning light into concentration

Source: https://ml-biomat.com/tutorials/experimental-methods/s03/en/
Language: en

Connect changing color to transmission and absorbance, then build a complete quantification through calibration, dilution and optical-error analysis.

## A solution becomes paler: how many molecules remain?

Add a drop of colored solution to water, then keep adding water. The color becomes paler. Our eyes can compare the change but cannot readily assign a concentration, and they cannot see absorption in the ultraviolet. A UV–visible spectrophotometer turns this familiar observation into a measurement: select a wavelength, compare the light transmitted by a blank and a sample, and relate the difference to concentration. This supports measurements of a drug in a release medium, direct or colorimetric estimates of protein content, and comparisons of transmission through films. These applications share optical principles while requiring different chemical conditions, sample preparation and calibration. Understanding that shared measurement makes it easier to choose the appropriate experiment.

A sample appears colored because different wavelengths have different chances of reaching the observer. When a solution absorbs one region of visible light, the remaining transmitted or scattered wavelengths combine to produce its observed color. A blue appearance therefore does not mean that absorption occurs only in the blue region. Ultraviolet absorption can occur in a solution that appears completely colorless. A spectrum records wavelength on the horizontal axis and an optical response on the vertical axis, preserving more information than a color name. Reading the full spectrum reveals the target band, a sloping background or a shape change after dilution. Those patterns often reveal problems that remain hidden when only one numerical reading is recorded.

This chapter follows a reproducible dye-quantification exercise. A set of known standards establishes a calibration line. A sample diluted fivefold is then measured and its original concentration calculated. Stray light and a scattering contribution are subsequently introduced to examine why high absorbance and turbidity can bias the same calculation. The spectra and calibration readings are explicitly constructed teaching data, with their parameters and random seed retained in the program. They allow the prescribed concentration, optical-model response and calculated result to be inspected together. The exercise separates three tasks that are often compressed into one button: measuring light, fitting a mathematical relationship and interpreting what that relationship says about the specimen.

An absorbance reading does not by itself identify the concentration of a particular substance. The detector initially measures arriving light. Molecular absorption, particle scattering, marks on a cuvette and other solutes can all reduce that light. Assigning the reduction to a target requires a suitable wavelength, matched blank, appropriate standards and stable chemical conditions. A molecule may absorb differently when free, bound to a protein or present in another acid–base form. A more precise analytical question is therefore the concentration of a specified chemical form under specified conditions. This framing turns an everyday comparison of color into an experiment whose result can be connected to the molecular state that the researcher wants to measure.

## Why quartz and photoelectric detection changed chemical analysis

Color comparison long preceded electronic spectrophotometers, but visual judgments depend on illumination, observer and reference. Separating wavelengths and measuring transmitted light electrically made quantitative comparisons more stable. The Beckman DU, introduced in 1941, is an important example in this development. Quartz optics extended measurements into the near ultraviolet. Quartz was a functional choice: ordinary glass absorbs strongly in parts of the ultraviolet, potentially attenuating the beam before it reaches the specimen. The accessible measurement region therefore depends on both electronics and every material in the optical path. The original explanatory drawing below connects that historical materials choice with the practical selection of a cuvette and optical configuration today.

![The historical role of quartz connects to modern spectrophotometry. The original upper diagram shows band selection, specimen and photoelectric detection as functions. The lower diagram compares blank and sample at equal path length; arrow widths indicate intensity qualitatively.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/f88dd44a72ce4b08d1093a7b.svg?v=f88dd44a72ce)

Figure 1The historical role of quartz connects to modern spectrophotometry. The original upper diagram shows band selection, specimen and photoelectric detection as functions. The lower diagram compares blank and sample at equal path length; arrow widths indicate intensity qualitatively.

In a common scanning arrangement, a source supplies a broad range of wavelengths. A monochromator uses a grating or prism together with slits to select a narrower band, which passes through the sample before reaching the detector. Changing the selected wavelength constructs a spectrum. An array instrument can arrange these functions differently: broad-band light passes through the sample first, then disperses across detector positions so that multiple wavelengths are recorded together. Recognizing both arrangements avoids assuming that every spectrophotometer has the same optical sequence. Their shared task is to determine how much light arrives from the sample and reference at the corresponding wavelengths, with a defined spectral bandwidth and detection response.

A single-beam instrument commonly records the blank and sample sequentially. A double-beam arrangement provides sample and reference paths to help follow changes such as source drift. A reference path does not replace a chemically appropriate blank. If the sample contains salts and buffer, the blank should usually include the corresponding solvent and non-target components. A colorimetric assay may require all relevant reagents except the target, taken through the same treatment and timing. The blank is designed to cancel shared contributions, rather than to declare any inconvenient signal zero. The chemical distinction between target response and background remains part of the experimental design, even when optical referencing is automated.

A cuvette may look like a simple container, yet it determines path length and contributes to background. Path length is the distance traveled through the specimen, often nominally 1 cm in a standard cuvette but different in microvolume devices, flow cells or microplates. For ultraviolet measurements, check transmission of the container at the intended wavelengths. Keep the optical faces clean and consistently oriented, and fill the cell sufficiently to cover the beam. Bubbles change propagation, fingerprints add optical loss, and an insufficient liquid level allows part of the beam to cross air. Stabilizing these direct influences on the optical path makes subsequent discussion of small concentration differences much more meaningful.

A negative absorbance can also be understood through the reference relationship. A reading of −0.01 means that corrected sample intensity is approximately 1.023 times the blank intensity; it does not imply a negative number of absorbing molecules. Small random fluctuations can cross zero when the response is close to the blank. A consistently negative spectral region instead motivates remeasuring the blank, checking or exchanging cuvettes, and comparing sample and reference solvent compositions. If the blank contains an absorber absent from the sample, the reference itself loses more light. Identifying which conditions actually changed between the two measurements preserves the experimental information in the anomaly and provides a reasoned basis for subsequent treatment of the readings.

## Why use a logarithm? Each layer acts on the light that remains

Imagine a uniform solution divided into many identical thin layers. If each layer transmits nine tenths of the light arriving at it, the first leaves 0.9 of the original beam, the second leaves 0.9 times 0.9, and the next multiplies by 0.9 again. The absolute amount removed decreases along the path because later layers receive less light. The transmitted fraction per identical layer stays the same. This is the intuitive origin of exponential attenuation. Increasing concentration adds absorbers within the same distance; increasing path length adds more layers. If molecular absorption properties and propagation conditions remain constant, both changes affect the transmission in a related way.

![Three identical teaching layers each transmit half the light: 1000, 500, 250 and 125 illustrate multiplication of transmission fractions. The right panel shows the same relationship as additive absorbance. Counts and layers are explanatory models.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/8fbfb65f064591d791abffaf.svg?v=8fbfb65f0645)

Figure 2Three identical teaching layers each transmit half the light: 1000, 500, 250 and 125 illustrate multiplication of transmission fractions. The right panel shows the same relationship as additive absorbance. Counts and layers are explanatory models.

$$
T=\frac{I}{I_0},\qquad A=-\log_{10}T
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | Transmittance, dimensionless; percent transmission is 100T%. |
| ![Formula](https://ml-biomat.com/static/agent-math/112feff6b4d0334226e24d5c.svg) | Sample intensity at the intended wavelength after appropriate dark correction, in the same units as I₀. |
| ![Formula](https://ml-biomat.com/static/agent-math/6e4f2807ce72e4cab3957130.svg) | Intended-light intensity through the matched blank after appropriate dark correction. |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Absorbance, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/be8ebdecd039424afe275a60.svg) | Base-ten logarithm. |

Transmission fractions multiply across uniform layers; logarithms turn the product into a sum. T=0.5 gives A=0.30103; two identical layers give T=0.25 and A=0.60206. Sample and blank require comparable detection conditions.

Transmittance is the ratio of sample-transmitted intensity to blank-transmitted intensity. It is usually calculated as a fraction and multiplied by 100 when displayed as a percentage. Absorbance takes the negative base-ten logarithm of that fraction, turning multiplicative attenuation into an additive quantity. A transmittance of 0.5 corresponds to an absorbance of approximately 0.301. Passing through another identical layer gives a transmittance of 0.25 and an absorbance of approximately 0.602. The two absorbances add just as the two transmissions multiply. Taking the logarithm adds no new physical information; it chooses a representation that makes the relationship with concentration and path length easier to use and test.

$$
A=\varepsilon l c
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Absorbance, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/9bc08d537f481d038b7b8b9d.svg) | Molar absorptivity for the specified wavelength, chemical form and environment, in L·mol⁻¹·cm⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/b725c065245400348075701d.svg) | Path length through the sample in cm. |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | Target concentration in mol·L⁻¹. |

This relationship assumes stable absorption properties, a sufficiently narrow band and a uniform sample with scattering appropriately addressed. An absorptivity of 50000, path of 1 cm and concentration of 10 μmol/L = 10⁻⁵ mol/L give A=0.5 and T=0.31623. Expressed per μmol/L, the numerical slope is 0.05 rather than 50000.

Molar absorptivity describes how strongly a particular chemical form absorbs at a particular wavelength and under specified conditions. Its units must match concentration and path length. With concentration in mol·L⁻¹ and length in cm, the coefficient is expressed in L·mol⁻¹·cm⁻¹, so their product is dimensionless. Suppose the coefficient is 50000 L·mol⁻¹·cm⁻¹, concentration is 10 μmol·L⁻¹ and path length is 1 cm. Absorbance is then 0.5, corresponding to approximately 31.6% transmission. The prefix μ means one millionth: 10 μmol·L⁻¹ is 0.000010 mol·L⁻¹. Writing this conversion before substitution prevents a millionfold mistake while also showing why the unit convention belongs to the formula.

This quantitative relationship connects to molecular energy states. Absorbing a photon means gaining energy compatible with an allowed transition; UV–visible absorption commonly involves electronic states. Molecular structure and chemical environment affect transition energies and strengths, so absorptivity depends on wavelength and may change with pH, binding or solvent. Quantification often uses a wavelength where target absorption is strong, background is modest and the chemical form is stable. A broad band maximum also has a practical advantage: a small wavelength-setting change has a relatively small first-order effect on absorbance there. The choice still needs to account for overlapping species, optical bandwidth and instrument performance in the selected region.

## From standards to an unknown: giving a straight line experimental meaning

A known absorptivity can support direct concentration estimation, but many analytical tasks use standards to establish an experimental calibration. Standards and unknowns should share solvent, reagents, reaction time, container and wavelength so that equal target concentrations produce comparable responses. The example uses six levels, 0, 2, 4, 8, 12 and 16 μmol·L⁻¹, with three constructed replicate readings at each level. Replicates expose scatter within a level; multiple levels test the response shape across the intended range. The range should encompass the expected unknown readings. Diluting an unknown into a verified range generally provides a stronger connection to the standards than extending a fitted line far beyond them.

$$
A=mc+b,\qquad c_{\mathrm{stock}}=D\frac{A_u-b}{m}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Standard absorbance, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Calibration slope, in L·μmol⁻¹ here. |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | Standard concentration in μmol·L⁻¹ here. |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Calibration intercept, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/8734e10f39fb90d4cce9d728.svg) | Absorbance of the diluted unknown, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | Dilution factor, final volume divided by transferred stock volume, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/e4cc5ee38ac5d83177d5a1ad.svg) | Stock concentration in μmol·L⁻¹. |

Subtract the modeled intercept, divide by slope to obtain diluted concentration, then multiply by the dilution factor. Aᵤ=0.39, b=0.02 and m=0.05 give 7.4 μmol/L; D=5 gives 37 μmol/L stock. Program readings include noise and differ slightly from this ideal arithmetic example.

The slope gives the average absorbance change for a one-unit concentration increase. The intercept is the response predicted at zero concentration. Even after blank subtraction, random variation or residual background can produce a small nonzero intercept. Forcing a line through the origin simply for visual neatness changes the calculation; a zero-intercept model should follow from the method definition and blank evidence. The example retains the intercept, plots every reading and displays residuals, which are observed minus fitted values. A coherent pattern, such as positive residuals at the ends and negative values in the middle, reveals curvature more clearly than a high correlation coefficient. The line earns its analytical role through these observations.

![Standards, unknown and uncertainty propagation use one constructed dataset. A places the unknown within the standard range; B retains pointwise residuals; C propagates reading error with standard concentrations and dilution fixed; D shows back-calculation. The dashed 37 μmol/L line is the prescribed stock concentration; the interval is a model quantile interval.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/501813b0b1cbe937de8e333b.svg?v=501813b0b1cb)

Figure 3Standards, unknown and uncertainty propagation use one constructed dataset. A places the unknown within the standard range; B retains pointwise residuals; C propagates reading error with standard concentrations and dilution fixed; D shows back-calculation. The dashed 37 μmol/L line is the prescribed stock concentration; the interval is a model quantile interval.

To calculate an unknown concentration, subtract the intercept from its absorbance and divide the remaining response by the slope. The constructed diluted sample has a prescribed concentration of 7.4 μmol·L⁻¹. Because it was prepared by fivefold dilution, the original prescribed concentration is 37 μmol·L⁻¹. Simulated measurement noise produces a small difference between that value and the calculated estimate, which appears in the figure and summary. The units provide an independent check: absorbance divided by absorbance per μmol·L⁻¹ yields μmol·L⁻¹. Multiplication by a dimensionless dilution factor leaves concentration units unchanged. Following this sequence helps detect an omitted dilution correction or a correction applied twice.

The dilution factor is final volume divided by transferred original volume. Taking 200 μL of stock and making the total volume 1000 μL gives a factor of five. Adding 1000 μL to that aliquot instead produces 1200 μL and a factor of six. Record the final volume explicitly. For serial dilution, multiply the individual dilution factors. Serial standards can also share an error inherited from an earlier preparation, so their concentration errors are not necessarily independent. A precise assay therefore considers the preparation chain as well as the optical readings. Measuring a common stock many times cannot reveal that its labeled concentration was offset by a preparation error shared by every aliquot.

Uncertainty can arise from replicate unknown readings, fitted slope and intercept, standard concentration, pipetting, final volume and completion of a chemical reaction. The program illustrates a defined part of this picture. With standard concentrations and dilution factor fixed, it estimates reading variation from calibration residuals, repeatedly generates calibration and unknown readings, refits the line and calculates an original concentration. The resulting distribution describes propagation under that stated noise model. A real experiment can extend it to include concentration and volume uncertainty. The number of decimal places printed by software is a formatting choice; the measurement model and its inputs determine the precision that a concentration estimate can reasonably express.

## Strong absorption and turbidity create different problems

As absorbance increases, fewer photons at the selected wavelength reach the detector. At absorbance 1 the transmittance is 10%; at 2 it is 1%; at 3 it is 0.1%. A small additional optical contribution can then become a large fraction of the detected light. Stray light includes light reaching the detector outside the spectral region selected by the monochromator. It can make transmission appear greater than it is and therefore make absorbance appear lower. As the desired transmitted beam approaches the stray-light background, increasing concentration produces progressively less change in the reading. The measured response approaches a ceiling and a calibration that would otherwise be linear bends downward.

$$
A_{\mathrm{meas}}=-\log_{10}\!\left(\frac{10^{-A_{\mathrm{true}}}+s}{1+s}\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/484437b4906af10337d8a00b.svg) | Measured absorbance with stray light, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/8a413ff8e77959d2570fd134.svg) | True absorbance for intended-wavelength light alone, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | Stray intensity divided by intended blank intensity, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/be8ebdecd039424afe275a60.svg) | Base-ten logarithm. |

Both sample and blank receive the same additional light, assumed unattenuated by the target, so s enters numerator and denominator. At Atrue=3 and s=0.001, the reading is about 2.6994. At arbitrarily high concentration the limit is log₁₀[(1+s)/s], about 3.0004. Actual stray-light spectra and attenuation depend on the instrument and specimen.

The simple model adds the same stray intensity to the sample and blank readings and assumes the target does not attenuate that stray contribution. If stray intensity is 0.1% of the blank intensity at the intended wavelength, a true absorbance of 3 leaves an intended transmitted beam of exactly the same size as the stray contribution. Combining them produces a measured absorbance near 2.699 rather than 3. At still higher concentrations, the reading approaches approximately 3.0004. This calculation explains why a strongly absorbing sample is often diluted or measured with a shorter path. The interactive display varies concentration, path length and stray fraction independently so that the departure from the ideal line can be traced to each setting.

## Why can absorbance level off while concentration increases?

Molar absorptivity at the selected wavelength is 50000 L·mol⁻¹·cm⁻¹. Change concentration, path length and an unabsorbed stray-light fraction to compare an ideal line with the instrumental model. The point marks the selected concentration. True transmission is displayed alongside absorbance to connect the logarithmic reading with a light-intensity ratio.

[Figure: Effects of concentration, path length and stray light on absorbance](https://ml-biomat.com/tutorials/experimental-methods/s03/en/#S03-plot)

Set concentration to 60 μmol·L⁻¹, then reduce path length from 1 cm to 0.2 cm. More intended light passes through the shorter path, reducing the relative contribution of stray light. The model compares optical effects in a uniform clear solution with a fixed chemical form.

Turbidity instead changes the direction in which light travels. Particles scatter some light outside the detector’s collection geometry, also reducing the recorded transmission. Assigning that loss entirely to molecular absorption can overestimate the target concentration. Optical-density measurements of cell or bacterial suspensions are therefore often used as specifically calibrated turbidity indicators, with a meaning different from single-solute absorption in a clear solution. For a materials-release medium, compare full-spectrum backgrounds and consider observations before and after an appropriate separation step. The separation itself may remove target molecules along with particles. The procedure should follow whether the intended quantity is the dissolved fraction, a free fraction or the total material present.

Chemical changes create another route to altered response by changing absorptivity. Acid–base indicators provide a familiar example: their forms have different colors. If dilution changes pH or binding equilibrium, concentration and spectral shape can change together, and a simple proportional rescaling may fail. Comparing concentration-normalized spectra at several dilutions tests whether peak positions and relative shapes remain consistent. In a buffered assay, standards and samples should reach comparable measurement conditions. Separating optical nonlinearity, scattering and chemical-form changes gives follow-up experiments a clear purpose. Their effects may coexist, but each hypothesis predicts a different response to a controlled change in path length, separation procedure or solution composition.

![Two distinct model deviations. Left: unabsorbed stray light produces a high-absorbance ceiling; s is its intensity relative to the intended blank light. Right: a constructed absorption band and an inverse-fourth-power wavelength-dependent scattering loss illustrate full-spectrum diagnostics using an additive apparent-attenuation approximation.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/1c6f97caec3ccce256320fc0.svg?v=1c6f97caec3c)

Figure 4Two distinct model deviations. Left: unabsorbed stray light produces a high-absorbance ceiling; s is its intensity relative to the intended blank light. Right: a constructed absorption band and an inverse-fourth-power wavelength-dependent scattering loss illustrate full-spectrum diagnostics using an additive apparent-attenuation approximation.

## A complete calculation with concentration and diagnostic plots together

The complete program generates teaching readings for standards and an unknown, fits an intercept-bearing calibration, plots pointwise residuals and propagates reading uncertainty into a distribution of original concentration. It also calculates transmission through successive layers, the high-absorbance effect of stray light, and a model absorption band with a wavelength-dependent scattering background. Outputs include bilingual figures, a standards CSV, a spectrum CSV and a numerical summary. A fixed seed makes the numerical exercise reproducible. When inserting experimental observations, retain concentration units, blank treatment and dilution records alongside the measured values. Replacing only a column of numbers without its measurement definitions can leave a program that runs successfully while calculating the wrong analytical quantity.

### From standard readings to stock concentration and diagnostic figures

The complete program constructs labeled teaching data, calibrates, back-calculates through dilution and propagates reading error, exporting CSV files, a numerical summary and all four figures.

```
"""UV-visible calibration with a declared teaching dataset and optical models.

Run: python main.py --output output --language en
Concentrations are in micromoles per liter unless explicitly stated otherwise.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch

BLUE,TEAL,ORANGE,INK='#245ca6','#087f80','#ce6b35','#233446'


def measured_absorbance(true_absorbance,stray_fraction):
    """Equal unattenuated stray intensity enters sample and blank readings."""
    return -np.log10((10.**(-np.asarray(true_absorbance))+stray_fraction)/(1+stray_fraction))


def main(output,language):
    output.mkdir(parents=True,exist_ok=True);zh=language=='zh';tr=lambda a,b:a if zh else b
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','Noto Sans CJK SC','DejaVu Sans'],
        'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none',
        'axes.unicode_minus':False,'figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6',
        'savefig.facecolor':'#fbfaf6','text.color':INK,'axes.labelcolor':INK})
    def save(fig,name):
        for ext in ['svg','png']:fig.savefig(output/f'{name}-{language}.{ext}',bbox_inches='tight',dpi=140)
        plt.close(fig)
    def arrow(ax,start,end,color=BLUE,lw=2):
        ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=13,lw=lw,color=color))

    # Original historical-principle illustration, without copied apparatus art.
    fig,axes=plt.subplots(2,1,figsize=(11.8,6.8),layout='constrained')
    ax=axes[0];ax.axis('off');ax.set(xlim=(0,11),ylim=(0,3.2))
    ax.set_title(tr('石英让光路进入紫外：1941 年 DU 仪器的一个关键选择','Quartz opens the ultraviolet: a key choice in the 1941 DU instrument'),loc='left')
    ax.add_patch(Circle((.8,1.6),.22,color='#dfae56'));arrow(ax,(1.1,1.6),(2.5,1.6),INK)
    ax.add_patch(Polygon([[2.6,1.1],[3.3,1.1],[2.95,2.35]],closed=True,facecolor='#d9e8ec',edgecolor=INK))
    for y,color in [(1.2,ORANGE),(1.7,TEAL),(2.2,'#7850a2')]:arrow(ax,(3.1,1.65),(4.65,y),color)
    ax.plot([4.8,4.8],[.8,1.55],color=INK,lw=4);ax.plot([4.8,4.8],[1.85,2.6],color=INK,lw=4)
    arrow(ax,(4.95,1.7),(6.2,1.7),TEAL)
    ax.add_patch(Rectangle((6.3,1.1),.8,1.2,facecolor='#b9d7ce',edgecolor=INK))
    arrow(ax,(7.2,1.7),(8.7,1.7),TEAL,lw=1)
    ax.add_patch(Rectangle((8.8,1.25),.7,.9,facecolor='#e1e8ed',edgecolor=INK))
    for x,label in [( .8,tr('光源','Source')),(2.95,tr('分光','Disperse')),(4.8,tr('狭缝选色','Select band')),(6.7,tr('样品','Sample')),(9.15,tr('光电检测','Photoelectric detector'))]:ax.text(x,.5,label,ha='center',fontsize=10)
    ax.text(6.1,2.75,tr('功能示意；不按历史装置尺寸绘制','Functional illustration, not a scale drawing of the historical device'),fontsize=9,ha='center')
    ax=axes[1];ax.axis('off');ax.set(xlim=(0,11),ylim=(0,2.7));ax.set_title(tr('相同光路长度，比较空白与样品','Compare blank and specimen at the same path length'),loc='left')
    for y,label,color,width in [(1.9,tr('空白','Blank'),'#eef2f3',2.8),(.7,tr('样品','Sample'),'#a9cebf',1.3)]:
        arrow(ax,(1,y),(4.1,y),BLUE)
        ax.add_patch(Rectangle((4.2,y-.36),1.4,.72,facecolor=color,edgecolor=INK));ax.text(4.9,y,label,ha='center',va='center')
        arrow(ax,(5.7,y),(8.5,y),TEAL,lw=width)
        ax.add_patch(Rectangle((8.6,y-.3),.55,.6,facecolor='#e1e8ed',edgecolor=INK))
    ax.text(2.5,2.4,tr('相同入射条件','Same illumination'),ha='center')
    ax.text(7.1,2.4,tr('比较透过光强','Compare transmitted light'),ha='center')
    ax.text(4.9,.08,tr('光程 l','Path length l'),ha='center')
    save(fig,'optics')

    fig,axes=plt.subplots(1,2,figsize=(11.8,4.8),layout='constrained')
    ax=axes[0];ax.axis('off');ax.set(xlim=(-.4,5),ylim=(0,3.6));ax.set_title(tr('A · 相同薄层让透过比例相乘','A · Equal layers multiply transmission'),loc='left')
    for i in range(3):
        ax.add_patch(Rectangle((i*1.3+.7,.8),.4,1.7,facecolor=TEAL,alpha=.35,edgecolor=TEAL))
        ax.text(i*1.3+.9,.45,tr('一层','One layer'),ha='center')
    for i,count in enumerate([1000,500,250,125]):
        x=i*1.3+.2;arrow(ax,(x-.35,1.65),(x+.35,1.65),BLUE,lw=max(.8,count/260))
        ax.text(x,2.8,str(count),ha='center',color=BLUE)
    ax.text(2,3.25,tr('光子数比例示意','Illustrative photon-count ratios'),ha='center',fontsize=10)
    ax.text(2,.05,tr('0.5 × 0.5 × 0.5 = 0.125','0.5 × 0.5 × 0.5 = 0.125'),ha='center')
    ax=axes[1];layers=np.arange(0,7);a=-np.log10(.5)*layers
    ax.plot(layers,a,'o-',color=TEAL,label=tr('吸光度相加','Absorbances add'))
    ax.set(xlabel=tr('相同薄层数','Number of identical layers'),ylabel=tr('吸光度','Absorbance'),title=tr('B · 对数把连乘变成相加','B · Logarithms turn products into sums'))
    for n in [1,2,3]:ax.annotate(f'T={.5**n:g}',(n,a[n]),xytext=(8,-20),textcoords='offset points',fontsize=9)
    ax.legend();save(fig,'layers')

    rng=np.random.default_rng(530)
    levels=np.array([0,2,4,8,12,16.]);c=np.repeat(levels,3)
    a=.02+.05*c+rng.normal(0,.006,len(c))
    m,b=np.polyfit(c,a,1);residual=a-(m*c+b)
    sigma=float(np.sqrt(np.sum(residual**2)/(len(c)-2)))
    unknown=.02+.05*7.4+rng.normal(0,.006,3);dilution=5
    estimate=float(dilution*(unknown.mean()-b)/m)
    samples=[]
    for _ in range(3000):
        ym=m*c+b+rng.normal(0,sigma,len(c));mm,bb=np.polyfit(c,ym,1)
        yu=unknown.mean()+rng.normal(0,sigma,3).mean();samples.append(dilution*(yu-bb)/mm)
    samples=np.asarray(samples);lo,hi=np.quantile(samples,[.025,.975])
    np.savetxt(output/'calibration.csv',np.column_stack([c,a,m*c+b,residual]),delimiter=',',
       header='concentration_umol_L,absorbance,fitted_absorbance,residual',comments='')
    np.savetxt(output/'unknown.csv',unknown,delimiter=',',header='absorbance',comments='')
    np.savetxt(output/'propagated_concentration.csv',samples,delimiter=',',header='original_concentration_umol_L',comments='')
    fig,axes=plt.subplots(2,2,figsize=(12,7.8),layout='constrained')
    grid=np.linspace(0,16,200)
    axes[0,0].scatter(c,a,s=30,color=BLUE,label=tr('标准读数','Standard readings'))
    axes[0,0].plot(grid,m*grid+b,color=TEAL,label=tr('带截距拟合','Fit with intercept'))
    axes[0,0].scatter([(unknown.mean()-b)/m],[unknown.mean()],marker='D',s=60,color=ORANGE,label=tr('未知液','Unknown'))
    axes[0,0].set(title=tr('A · 标准与未知在同一量尺上','A · Standards and unknown on one scale'),xlabel=tr('浓度 / μmol L$^{-1}$','Concentration / μmol L$^{-1}$'),ylabel=tr('吸光度','Absorbance'));axes[0,0].legend(fontsize=9)
    axes[0,1].scatter(c,residual,color=BLUE);axes[0,1].axhline(0,color=INK,lw=1)
    axes[0,1].set(title=tr('B · 残差检查线性关系','B · Residuals check the linear relationship'),xlabel=tr('浓度 / μmol L$^{-1}$','Concentration / μmol L$^{-1}$'),ylabel=tr('测量 − 拟合','Observed − fitted'))
    axes[1,0].hist(samples,bins=42,color=TEAL,alpha=.8,density=True)
    axes[1,0].axvline(37,color=INK,ls='--',label=tr('设定值 37','Prescribed 37'))
    axes[1,0].axvline(estimate,color=ORANGE,label=f'{estimate:.2f}')
    axes[1,0].set(title=tr('C · 读数误差传播到原液浓度','C · Reading error propagates to stock concentration'),xlabel=tr('原液浓度 / μmol L$^{-1}$','Stock concentration / μmol L$^{-1}$'),ylabel=tr('概率密度 / (μmol L$^{-1}$)$^{-1}$','Density / (μmol L$^{-1}$)$^{-1}$'));axes[1,0].legend(fontsize=9)
    ax=axes[1,1];ax.axis('off');ax.set_title(tr('D · 逐步反算，保留单位','D · Back-calculate while retaining units'),loc='left')
    lines=[tr('未知液平均吸光度','Mean unknown absorbance')+f'  {unknown.mean():.4f}',
       tr('斜率','Slope')+f'  {m:.5f}  A / (μmol/L)',tr('截距','Intercept')+f'  {b:.5f}',
       tr('稀释液浓度','Diluted concentration')+f'  {estimate/5:.3f} μmol/L',
       tr('乘稀释倍数 5','Multiply dilution factor 5'),tr('原液浓度','Stock concentration')+f'  {estimate:.3f} μmol/L',
       tr('模型中 95% 分位区间','Model 95% quantile interval')+f'  [{lo:.2f}, {hi:.2f}]']
    for i,line in enumerate(lines):ax.text(.04,.9-i*.13,line,fontsize=10,transform=ax.transAxes)
    save(fig,'calibration')

    wave=np.linspace(350,750,801);absorption=.7*np.exp(-.5*((wave-530)/32)**2);scatter=.15*(530/wave)**4
    np.savetxt(output/'spectrum.csv',np.column_stack([wave,absorption,scatter,absorption+scatter]),delimiter=',',
       header='wavelength_nm,constructed_absorption,constructed_scattering_loss,total_apparent_absorbance',comments='')
    fig,axes=plt.subplots(1,2,figsize=(11.8,4.8),layout='constrained');true=np.linspace(0,5,301)
    axes[0].plot(true,true,color=INK,ls='--',label=tr('理想响应','Ideal response'))
    for s,col in [(.0001,BLUE),(.001,TEAL),(.01,ORANGE)]:axes[0].plot(true,measured_absorbance(true,s),color=col,label=f's = {s:g}')
    axes[0].set(xlabel=tr('真实吸光度','True absorbance'),ylabel=tr('测得吸光度','Measured absorbance'),title=tr('A · 杂散光使高吸收响应弯曲','A · Stray light bends high-absorbance response'));axes[0].legend(fontsize=9)
    axes[1].plot(wave,absorption,color=TEAL,label=tr('构造吸收峰','Constructed absorption'))
    axes[1].plot(wave,scatter,color=ORANGE,label=tr('构造散射背景','Constructed scattering loss'))
    axes[1].plot(wave,absorption+scatter,color=BLUE,label=tr('总表观响应','Total apparent response'))
    axes[1].set(xlabel=tr('波长 / nm','Wavelength / nm'),ylabel=tr('表观吸光度','Apparent absorbance'),title=tr('B · 全谱帮助发现不同贡献','B · Full spectra expose different contributions'));axes[1].legend(fontsize=9)
    save(fig,'diagnostics')
    summary={'data_kind':'constructed teaching calibration and optical models','seed':530,
       'absorbance_T05':float(-np.log10(.5)),'transmission_A05':float(10**(-.5)),
       'slope':float(m),'intercept':float(b),'unknown_diluted_estimate':estimate/5,
       'unknown_stock_estimate':estimate,'stock_true':37.,'reading_sigma':sigma,
       'stock_interval_reading_model':[float(lo),float(hi)],
       'stray_001_at_true3':float(measured_absorbance(3,.001)),
       'stray_001_plateau':float(np.log10(1001))}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args()
    main(args.output,args.language)
```

The calibration points receive equal weight here, corresponding to approximately equal absorbance-error variance across the modeled range. If repeated measurements reveal substantially different variances, a weighted fit can use that information. The weights should follow observations or an appropriate noise model. Down-weighting a high-concentration region with systematic curvature does not restore the physical assumptions of a linear calibration. A more direct response is to investigate the cause, establish a suitable range again and dilute unknowns into that range. Fitting strategy and experimental conditions should be considered together. A numerical method becomes useful when its assumptions match what the instrument and specimen are doing, rather than when it merely produces an attractive line.

The uncertainty calculation treats repeated readings as repeated observations, not as independently prepared specimens. It fixes standard concentrations and the dilution factor, then simulates reading noise, refits and back-calculates. One useful extension gives the mother solution one shared concentration perturbation and individual transfers their own volume perturbations. This reveals how correlated preparation errors move an entire calibration together. It also explains why additional readings cannot remove a common stock-concentration offset. Such an extension has a physical interpretation: the variables correspond to identifiable preparation steps. Adding arbitrary noise to every point independently would miss that relationship and could misrepresent which additional experimental effort would improve the result.

The final display should keep standards, fitted response and residuals connected. Marking the unknown on the calibration plot makes interpolation versus extrapolation visible. A concentration distribution or interval should say whether it describes reading variability, model-based propagation or differences between independent specimens. These meanings are distinct even if their error bars look similar. For full spectra, preserve wavelength units and blank treatment; for normalized comparisons, retain the information needed to recover original intensity. A readable plot is one in which the audience can identify both the pattern and the quantity behind each mark. The exported tables make those relationships inspectable without requiring the reader to infer them from the code.

## Choosing the next measurement in materials and biology

In a release experiment, optical quantification belongs to a longer calculation: remove an aliquot, measure concentration and convert it to released mass. If fresh medium replaces the removed volume, cumulative release must include material taken away at previous sampling times. This chapter supplies concentration in the measured aliquot; cumulative mass additionally requires each sampling volume and the vessel volume. Adsorption to the container, target degradation and scattering from carrier fragments may affect the response. Controls for release medium, unloaded carrier and target standard can separate these contributions. Spike-recovery measurements at suitable concentrations test whether the sample matrix changes analytical response. Connecting these steps allows an absorption spectrum to support an interpretation of the carrier’s release behavior.

Direct ultraviolet protein measurement and colorimetric protein assays emphasize different chemistry. Direct absorption depends on the relevant molecular groups and their environments, so different proteins can have different responses. A colorimetric assay converts an interaction or reaction into visible absorption and is affected by reagent compatibility, reaction time and the chosen standard protein. Method selection starts with the intended quantity: total protein, a particular purified protein or a relative change within a mixture. If molecular identity must be resolved, separation, immunochemical recognition or mass spectrometry can add information beyond an absorption value. The analytical question, rather than availability of a familiar instrument, determines which combination of observations is most informative.

For films and porous materials, transmission, reflection and scattering also need distinct treatment. A conventional transmission geometry records the light reaching the detector within its collection angle. Surface reflection and diffuse scattering change that amount. An integrating sphere can collect a wider angular range and support further separation of contributions. Before transferring a solution-calibration argument to a solid, examine whether path length, surface condition and collection geometry support the same model. Placing a material in the instrument yields a curve, but interpreting that curve requires knowing which light was collected and which left the collection path. The vertical axis then becomes a description of a defined optical experiment.

A quantitative result can be traced backward through four objects: the original concentration depends on a dilution, the diluted concentration depends on a calibration, the calibration response depends on wavelength and blank, and the light change depends on specimen state. An unknown above the verified range suggests a suitable dilution or shorter path. A shape change after dilution directs attention to chemical form and matrix. A broad scattering background requires a clear definition of dissolved versus particle-containing material. Each response chooses an observable variable that can distinguish a cause. In this way, the familiar observation of changing color develops into a layered research method whose calculations remain connected to the physical and chemical measurement.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/S03.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Raja and Barron: UV-Visible Spectroscopy](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Physical_Methods_in_Chemistry_and_Nano_Science_%28Barron%29/04%3A_Chemical_Speciation/4.04%3A_UV-Visible_Spectroscopy)

   Absorption relationships, common optical arrangements and wavelength selection.

   CC BY 4.0 page; open further reading.
2. [Agilent: Understanding Your UV-visible Spectroscopy System](https://www.agilent.com/Library/usermanuals/Public/G1115-90041_UnderstandingGP.pdf)

   Chapter 1 on dark signal, reference and absorbance; chapter 5 on calibration and back-calculation.
3. [Shimadzu: What is stray light?](https://www.ssi.shimadzu.com/service-support/faq/uv-vis/resolution-and-stray-light/3/index.html)

   Definition of stray light and response deviations at high absorbance.
4. [Smithsonian: Beckman DU Spectrophotometer](https://americanhistory.si.edu/collections/object/nmah_378)

   Historical record of the 1941 DU and its quartz optics.
5. [Beckman Foundation: Spectrophotometer](https://www.beckman-foundation.org/about-foundation/inventions/spectrophotometer/)

   History of instrumental development and ultraviolet analytical applications.
