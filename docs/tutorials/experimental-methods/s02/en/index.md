# Raman spectroscopy: Molecular fingerprints in scattered light

Source: https://ml-biomat.com/tutorials/experimental-methods/s02/en/
Language: en

Start with a transparent particle, follow the exchange of vibrational energy, and separate bands, background and instrument effects in a complete spectral analysis.

## How a tiny particle can reveal what it contains

Under a microscope, a transparent plastic fragment, a salt crystal and a dried protein deposit can look surprisingly similar. Their outlines reveal shape, but their chemical bonds are different. Raman spectroscopy directs light of a narrowly defined color onto a specimen, collects a small fraction of the scattered light and looks for photons whose color has changed. The color change corresponds to energy exchanged with the material. Arranging these energy changes along an axis produces a spectrum associated with molecular vibrations. Researchers use these spectra to compare regions of a hydrogel, examine mineral and organic components in bone, and investigate orientation, ordering or chemical reactions in polymers. A Raman microscope connects a visible location with information about molecular structure at that location.

The familiar phrase “molecular fingerprint” is most useful when it means a pattern of clues. A single piano note appears in many songs; identifying a song requires a sequence. Likewise, many organic compounds contain carbon–hydrogen bonds, and their bands can occur in similar spectral regions. Mixtures add overlapping contributions. An identification therefore considers several positions, shapes and relative intensities together with acquisition conditions. If rotating a fiber changes a band intensity, molecular orientation relative to the light polarization may be responsible. If the background decreases during repeated illumination, fluorescence bleaching may contribute. Understanding the measurement process helps separate these possibilities before attaching a chemical explanation to a change in the plot.

This chapter follows a practical task: resolve two neighboring Raman bands on a broad background and compare their areas. The task introduces three common puzzles. Why does the horizontal axis use cm⁻¹ rather than the laser color? Why can a taller peak contain less total signal? Why does increasing laser power sometimes improve the spectrum and sometimes distort both the sample and the detector response? The figures, calculation and interactive experiment return to these questions. The numerical exercise uses explicitly constructed peaks, background and counting noise. Its true parameters are exported with the results, allowing each processing step to be compared with something known. The same workflow can later be applied to experimental data with appropriate reference measurements.

The research question also determines where to measure. A film surface, an inclusion and a deeper layer may contain different material, just as a mineralized tissue region differs from surrounding soft tissue. A point spectrum describes the sampled region near one focus; a map organizes many point spectra by position. Ten acquisitions at the same spot characterize repeatability at that spot, whereas independently prepared specimens address variability between preparations. A useful preliminary study uses low-power measurements at selected positions to establish background and stability, followed by a defined sampling rule across independent specimens. That design connects spectral differences to the biological or materials question rather than to an accidental choice of an unusually bright location.

## From two filters to a spectrometer: finding the rare light

In 1928, C. V. Raman and K. S. Krishnan distinguished scattered light with a color different from the incident light in experiments on liquids. The discovery is easier to understand through its optical challenge than through a list of awards. If violet light enters a liquid and most collected light remains violet, how can a much weaker different color be seen? Early experiments selected an incident band and used another filter to suppress its original color in the observation path. Removing a dominant contribution made a weak contribution observable. The original diagram below explains that filtering idea and connects it with modern instrumental functions. It is a conceptual reconstruction of roles, not a scaled drawing of the historical apparatus.

![Original diagrams of early filtering and modern instrumental functions. The upper view highlights selection of shifted light; the lower view connects detected pixels to calibrated spectra. Functional paths are shown, not a scale reconstruction of a historical apparatus.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/cdbc987795c317fac9fc92a1.svg?v=cdbc987795c3)

Figure 1Original diagrams of early filtering and modern instrumental functions. The upper view highlights selection of shifted light; the lower view connects detected pixels to calibrated spectra. Functional paths are shown, not a scale reconstruction of a historical apparatus.

A modern Raman microscope commonly uses a laser to supply a narrow incident band and an objective to focus it onto the specimen and collect scattered light. A rejection filter suppresses strong Rayleigh scattering at the laser frequency. A grating then separates the remaining light by wavelength, and a detector records the signals at different positions. The grating can be imagined as an optical organizer that sends different wavelengths to different places. Initially, the detector produces pixel positions and counts. A wavelength calibration connects those pixels to wavelengths; the known laser wavelength then converts them into Raman shifts. Accurate positions on the horizontal axis and accurate relative intensities on the vertical axis are therefore separate calibration tasks.

Lasers made weak Raman signals easier to collect, while microscopes and array detectors enabled convenient spatial selection and acquisition across a spectral interval. The throughput of an instrument still varies with wavelength. A filter may transmit one region more effectively, while the grating and detector have their own response curves. Consequently, the raw ratio of widely separated bands contains both material information and the wavelength dependence of the instrument. NIST relative-intensity standards address this response correction. Checking a reference peak, such as a suitable silicon reference, helps assess the shift axis; it does not establish the relative response across the entire spectrum. A calibration record should identify which of these questions was actually tested.

Weak-light measurements also require distinguishing backgrounds with different origins. Fluorescence can form a broad slowly varying contribution; a glass substrate or culture medium may add recognizable bands; detector dark current depends on instrumental conditions; and occasional cosmic-ray events can produce isolated sharp spikes. Although all may look like unwanted signal, they call for different observations. A substrate blank helps identify substrate features, repeated short exposures help recognize isolated events, and dark measurements characterize detector contributions. Changing excitation wavelength can substantially alter fluorescence. Treating all these effects with one smoothing operation would combine different physical problems. The experimental controls should identify the relevant contribution before a numerical procedure attempts to remove it.

## A small energy exchange becomes the horizontal axis

Two atoms joined by a spring provide a useful first picture of a vibrating bond: atoms move around equilibrium positions, and stretches or changes in bond angles have characteristic motions. In a real molecule, one normal mode can involve several atoms moving together. The allowed vibrational energies are also quantized rather than freely continuous. During Raman scattering, the difference between incident and scattered photon energies corresponds to a change in the vibrational state. The virtual level shown in an energy diagram is a representation of the scattering process, not a stable electronic level where the molecule waits before emitting. Keeping this distinction clear helps separate Raman scattering from fluorescence, which follows excitation into real electronic states.

![Energy bookkeeping for three scattering processes. The index v labels the lower (0) and higher (1) vibrational states shown. Equal upward arrows indicate equal incident photon energy. Stokes scattering leaves vibrational energy in the molecule; anti-Stokes scattering removes existing vibrational energy. The dashed virtual level represents the scattering process, not a stable excited electronic state.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d12f9b5f43f851463e4de347.svg?v=d12f9b5f43f8)

Figure 2Energy bookkeeping for three scattering processes. The index v labels the lower (0) and higher (1) vibrational states shown. Equal upward arrows indicate equal incident photon energy. Stokes scattering leaves vibrational energy in the molecule; anti-Stokes scattering removes existing vibrational energy. The dashed virtual level represents the scattering process, not a stable excited electronic state.

In Rayleigh scattering, the final vibrational state matches the initial one and the photon retains its energy. In Stokes scattering, the molecule gains vibrational energy, so the outgoing photon has less energy and a longer wavelength. Anti-Stokes scattering starts from a vibrationally excited molecule, which gives energy to the outgoing photon and produces a shorter wavelength. At ordinary room temperatures, lower vibrational states are generally more populated, so routine Raman spectra often emphasize the Stokes side. Temperature changes the relative populations. Using the two sides for temperature measurement additionally requires attention to instrumental response and excitation conditions; an arbitrary ratio of raw peak heights does not isolate temperature by itself.

$$
\Delta\widetilde{\nu}=10^7\left(\frac{1}{\lambda_0}-\frac{1}{\lambda_s}\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/888f64c1ee46a39652337b29.svg) | Raman shift in cm⁻¹; positive on the Stokes side in this convention. |
| ![Formula](https://ml-biomat.com/static/agent-math/0a322167c6031b3ba1406fb9.svg) | Laser wavelength in nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/1a4fc1363bf176a12e0b860f.svg) | Scattered wavelength in nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/7d87fc730958fc67a28c903c.svg) | Conversion factor from nm⁻¹ to cm⁻¹; 1 cm = 10⁷ nm. |

Energy differences scale with differences in reciprocal wavelength, so take reciprocals before subtracting. A 1000 cm⁻¹ shift with 532 nm excitation corresponds to approximately 561.89 nm scattered light; zero shift gives the laser wavelength.

A reciprocal wavelength is called a wavenumber. With wavelength expressed in centimeters, it counts how many wavelengths fit into one centimeter, giving cm⁻¹. Laser wavelengths are usually reported in nanometers, so the conversion factor must appear when the two units are combined. For a 532 nm laser, a Stokes shift of 1000 cm⁻¹ corresponds to a scattered wavelength of approximately 561.89 nm. With a 785 nm laser, the same shift corresponds to approximately 851.87 nm. The absolute scattered color changes, but the energy difference represented by the shift stays the same. This is why peak positions acquired with different lasers can be compared on a common shift axis. Intensities still require consideration of excitation efficiency and instrumental response.

$$
\Delta E=h c\,\Delta\widetilde{\nu}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/03a061659f8f3f0ea28e1238.svg) | Vibrational energy gained by the molecule in J, for a Stokes process. |
| ![Formula](https://ml-biomat.com/static/agent-math/994427fe929fdf538d7c1be7.svg) | Planck constant, 6.62607015 × 10⁻³⁴ J·s. |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | Speed of light, here 2.99792458 × 10¹⁰ cm·s⁻¹ to match the shift unit. |
| ![Formula](https://ml-biomat.com/static/agent-math/888f64c1ee46a39652337b29.svg) | Raman shift in cm⁻¹. |

Photon energy is Planck constant times frequency, and frequency is speed of light times wavenumber. A shift of 1000 cm⁻¹ corresponds to 1.98645 × 10⁻²⁰ J, about 0.123984 eV; 1 eV = 1.602176634 × 10⁻¹⁹ J.

Some vibrations are prominent in infrared absorption and weak in Raman spectra. To understand why, consider the electron cloud surrounding a molecule. An electric field can deform this cloud slightly; polarizability describes how readily it responds. A vibration can be Raman active when that motion changes the polarizability. Infrared activity instead depends on a change in dipole moment, which describes an asymmetry in the distribution of positive and negative charge. These are different molecular properties, so the two methods emphasize different motions. Specific molecular symmetries impose more precise selection rules. For complex biological specimens, the practical lesson is that Raman and infrared measurements often provide complementary views rather than identical copies of the same chemical information.

This complementarity matters in hydrated materials. Water contributes differently to many commonly used Raman fingerprint regions than it does to strong infrared absorption regions, which can make Raman measurements attractive for some aqueous specimens. The choice still depends on concentration, fluorescence, substrate, target bands and sampling depth. A transparent hydrogel may give a weak polymer signal because relatively few target scatterers contribute within the sampled volume. Better focusing or longer collection can help in that case. A strongly fluorescent contaminant poses a different problem, for which changing excitation conditions may be more effective than collecting more of the same background. Recognizing the physical source of poor contrast gives parameter changes a clear purpose.

## Power, time, focus and specimen all enter the spectrum

Laser power and exposure time both influence the number of detected photons, but they affect the specimen differently. Higher power deposits energy more rapidly into a small region and may raise its local temperature. Longer exposure prolongs illumination and can allow bleaching, oxidation or another slow process to develop. A useful initial observation collects several short spectra at modest power and checks whether peak positions, shapes and background remain stable before increasing total acquisition time. A spectrum that changes steadily at one location is itself an experimental observation. Investigating that change can distinguish illumination-induced evolution from a simple need to collect more photons. Once stability is established, longer acquisition can be chosen for a quantitative reason.

Counting fluctuations can be understood through repeated observations. A small number of coin tosses produces a more variable fraction of heads than a large number. Independent photon arrivals likewise fluctuate, and under an ideal counting model the standard deviation is approximately the square root of the mean count. Multiplying exposure time by four multiplies the mean signal by four and its counting noise by two, improving the signal-to-noise ratio by about two. Background photons contribute their own fluctuations. Subtracting an estimated mean background later does not remove the fluctuations that occurred during detection. A corrected spectrum that sits close to zero between peaks can therefore remain noisy even when its baseline looks visually tidy.

$$
\mathrm{SNR}=\frac{S}{\sqrt{S+B+\sigma_r^2}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ae03e7fd82fc9511ad569820.svg) | Signal-to-noise ratio, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | Mean detected signal-electron count. |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | Mean background-electron count in the same sampling channel or selected integration region. |
| ![Formula](https://ml-biomat.com/static/agent-math/91fd8c3471f776b7aee7c26b.svg) | Read-noise standard deviation for the same readout region, in electron counts. |

Independent Poisson counts have variance equal to their mean; independent variances add before taking the square root. This model treats the mean background as known and omits uncertainty in a separate background estimate. For S=200 and B=800, negligible read noise gives 6.3246; the interactive model uses a read-noise standard deviation of 5 and gives 6.2470.

Suppose a selected peak interval contributes 200 signal counts and 800 background counts, with other noise terms temporarily neglected. The resulting signal-to-noise ratio is about 6.32. Increasing the exposure fourfold gives 800 signal and 3200 background counts, raising the ratio to about 12.65. The example explains the benefit of longer acquisition and also identifies another route: reducing background can improve information quality at the same illumination budget. The interactive experiment places signal counts, background counts and a detector limit on the same display. Its units refer to a defined teaching model of detected electrons, rather than the settings of a particular commercial instrument. Read the count model before transferring any number to an experimental configuration.

## Adjust acquisition conditions and observe noise and clipping

Keep composition fixed while changing power, exposure and fluorescence background. At the peak maximum, signal electrons arrive at 40 × power factor per second; background electrons arrive at 160 × background factor × power factor per second. Read noise has a standard deviation of 5 electrons. The dashed curve shows the ideal count and the solid curve shows recording with a 3000-electron limit.

[Figure: Acquisition settings and Raman peak counts](https://ml-biomat.com/tutorials/experimental-methods/s02/en/#S02-plot)

First increase exposure fourfold, then halve the background. Compare how each change affects signal-to-noise ratio and peak shape. The calculation describes one sampling channel at the peak maximum. Random fluctuations are omitted from the plot to make clipping directly visible.

Focus and sampling volume deserve equal attention. Seeing the specimen in the microscope does not guarantee that the Raman focus lies entirely in the intended phase. A covering layer, an underlying glass surface or a tilted interface can change the collected proportions. For rough or porous materials, retain the optical image, measurement positions and focusing rule. When comparing specimen groups, keep objective, polarization configuration and collection geometry consistent. If orientation is the scientific variable, deliberately rotate polarization or specimen direction and include it in the design. Controlling a physically meaningful variable allows intensity changes to be interpreted; rescaling every spectrum to the same maximum can otherwise hide the origin of those differences.

Mapping introduces a further tradeoff between spatial sampling and acquisition time. A smaller grid spacing creates more measurements but does not automatically reduce the illuminated spot. Neighboring pixels may sample strongly overlapping volumes, and a long scan can mix spatial differences with time-dependent drift. A coarse survey can locate regions of interest before a finer local scan. Repeating a reference position before and after mapping helps assess stability of the sample and instrument. Record grid spacing, objective, relevant spot conditions, exposure per point and number of repeated acquisitions. These details give a chemical map an interpretable spatial meaning and help distinguish a resolved boundary from a densely sampled transition blurred by the optical system.

## From raw counts to band areas, with each step inspectable

The numerical exercise contains three constructed bands. Two neighboring bands lie at 1000 and 1040 cm⁻¹, while a broader band lies at 1450 cm⁻¹. They are added to a slowly curved background and independent counting noise generated with a fixed random seed. The positions and widths teach separation and quantification; they are not assigned to a specific real compound. The program retains the raw spectrum, known component truth, estimated baseline and fitted result. This makes preprocessing observable: a polished corrected curve alone cannot reveal whether a weak feature has been suppressed, exaggerated or introduced by a processing choice. Comparing each transformation against the retained inputs makes those effects much easier to understand.

![Complete analysis of a constructed teaching spectrum. A compares baseline anchor selections; B separates neighboring contributions; C examines residuals; D compares estimated area ratios with the known value of 0.6. All panels come from the same execution. Model positions are not chemical assignments for an experimental material.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/be0dbe5123e9ac5535ed75ee.svg?v=be0dbe5123e9)

Figure 3Complete analysis of a constructed teaching spectrum. A compares baseline anchor selections; B separates neighboring contributions; C examines residuals; D compares estimated area ratios with the known value of 0.6. All panels come from the same execution. Model positions are not chemical assignments for an experimental material.

The first processing step estimates a quadratic background using predefined regions assumed to be free of peaks. Selecting such regions is already a scientific judgment. In an experiment it should draw on blanks, reference spectra and repeated observations, rather than on smooth appearance alone. Imagine the baseline as a gradually rising road and the peaks as hills standing on it. Measuring hill height requires estimating the road elevation beneath it. If part of a hill is mistakenly included among road measurements, the estimated road rises and the hill area shrinks. The program compares a suitable anchor selection with an intentionally contaminated selection, showing how the same raw data can yield a different area ratio.

After background subtraction, two Gaussian components are fitted together within a local interval. Here the Gaussian shape is the known teaching model: its center locates the band, its width sets its spread and its area specifies total signal. Closely spaced components can compensate for one another, so a curve that follows the observations closely does not necessarily determine every component parameter precisely. Residuals are the differences between observations and predictions. Inspect whether they fluctuate around zero or form a coherent positive or negative pattern. A structured residual can indicate an inadequate background or line shape. An isolated spike calls for inspection of individual exposures rather than automatically adding another chemical component to the model.

$$
I(x)=\frac{A}{\sigma\sqrt{2\pi}}\exp\!\left[-\frac{(x-\mu)^2}{2\sigma^2}\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/eebf2869a2c97592f992b0eb.svg) | Model band intensity at coordinate x, in counts. |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | Raman shift in cm⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Integral area of the complete model band, in counts·cm⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | Band center in cm⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | Gaussian width parameter in cm⁻¹, the standard deviation of the corresponding normalized Gaussian. |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | The constant pi, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/64460da0d752153c52e1bd62.svg) | Natural exponential; its argument is dimensionless. |

The normalization makes the integrated area equal to A, so increasing width lowers the height at fixed area. The teaching bands have areas 6000 and 3600 counts·cm⁻¹, giving an area ratio of 0.6. Widths of 9 and 14 cm⁻¹ give a height ratio of about 0.386. Experimental line shapes should reflect the relevant broadening mechanisms.

Peak height and peak area answer different questions. Spreading the same total signal across a wider interval produces a lower peak, so a height decrease may reflect broadening rather than less material. The two neighboring model bands have areas of 6000 and 3600 counts·cm⁻¹, giving a true area ratio of 0.6. Because their widths differ, their height ratio is not 0.6. Experimental integration requires consistent baseline rules, integration limits, exposure, laser power and response correction. An internal-reference ratio additionally requires a reason to expect the reference band to track the relevant sampled amount under the compared conditions. Normalization expresses a relative quantity, whose meaning depends on the denominator and on whether that denominator changes.

Repeated observations belong to different levels. Repeated acquisitions at one location estimate short-term measurement variation; different locations within one specimen describe spatial heterogeneity; independently prepared specimens support comparisons between preparations. The repeated counting-noise simulation illustrates primarily the first level. It does not represent batch-to-batch material variability. A useful experimental display can show specimen-level summaries alongside distributions of locations within each specimen. This preserves the hierarchy instead of turning all pixels into an apparently enormous number of independent samples. It also helps plan the next experiment: large within-specimen variation may justify a more deliberate spatial survey, whereas variation between independently prepared specimens motivates additional preparations and better control of the preparation process.

## A complete calculation that exposes the effect of processing choices

The following program generates the raw spectrum, two background estimates, a two-band fit, a count-versus-noise comparison, and explanatory optical and energy-level diagrams. Data are exported as CSV, numerical results as summary.json, and figures as scalable SVG files. The calculation proceeds from explicit parameters through background estimation and local fitting to a result summary. To use an experimental spectrum, replace the constructed signal with exported numerical columns while retaining the diagnostic steps. First inspect axis units, ordering and sampling intervals. Numerical integration over a nonuniform axis must use the actual coordinate values. Treating every point as equally spaced can alter an area even when the plotted curve appears unchanged.

### Construct a spectrum, estimate its baseline and compare band areas

The complete program uses NumPy, SciPy and Matplotlib to export four figures, inspectable CSV data and a numerical summary. No online data are required; a fixed seed makes the teaching spectrum reproducible.

```
"""Raman measurement and processing with explicitly constructed teaching data.

Run: python main.py --output output --language en
No experimental material or chemical identity is assigned to the model bands.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
from scipy.optimize import curve_fit

BLUE, TEAL, ORANGE, INK = '#245ca6', '#087f80', '#ce6b35', '#233446'


def band(x, area, center, sigma):
    """Area-normalized Gaussian; x, center and sigma are in cm^-1."""
    return area / (sigma * np.sqrt(2 * np.pi)) * np.exp(-.5 * ((x-center)/sigma)**2)


def two_bands(x, a1, c1, w1, a2, c2, w2):
    return band(x, a1, c1, w1) + band(x, a2, c2, w2)


def signal_to_noise(power, time, background=1):
    signal = 40 * power * time
    baseline = 160 * background * power * time
    return signal / np.sqrt(signal + baseline + 25)


def main(output, language):
    output.mkdir(parents=True, exist_ok=True)
    zh = language == 'zh'
    tr = lambda a, b: a if zh else b
    plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif':
        ['Microsoft YaHei', 'Noto Sans CJK SC', 'DejaVu Sans'], 'font.size': 11,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.labelcolor': INK, 'text.color': INK, 'svg.fonttype': 'none',
        'axes.unicode_minus': False, 'figure.facecolor': '#fbfaf6',
        'axes.facecolor': '#fbfaf6', 'savefig.facecolor': '#fbfaf6'})
    def save(fig, name):
        fig.savefig(output / f'{name}-{language}.svg', bbox_inches='tight')
        fig.savefig(output / f'{name}-{language}.png', bbox_inches='tight', dpi=140)
        plt.close(fig)
    def arrow(ax, a, b, color=INK):
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle='-|>', mutation_scale=14,
                     lw=2, color=color))

    # Figure 1: an original conceptual comparison of optical functions.
    fig, axes = plt.subplots(2, 1, figsize=(11.8, 7.2), layout='constrained')
    for ax in axes:
        ax.set(xlim=(0, 11), ylim=(-.4, 3.4)); ax.axis('off')
    ax=axes[0]; ax.set_title(tr('1928：选择入射颜色，抑制强背景',
        '1928: Select incident color and reject the dominant light'), loc='left', pad=12)
    ax.add_patch(Circle((.8,1.25),.22,color='#dfae56'))
    for angle in np.arange(0,2*np.pi,.52):
        ax.plot([.8+.3*np.cos(angle),.8+.48*np.cos(angle)],
                [1.25+.3*np.sin(angle),1.25+.48*np.sin(angle)],color='#dfae56')
    for dy,color in [(-.08,BLUE),(0,'#7850a2'),(.08,TEAL)]:arrow(ax,(1.3,1.25+dy),(2.35,1.25+dy),color)
    ax.add_patch(Rectangle((2.45,.8),.15,.9,facecolor='#7850a2',alpha=.7))
    arrow(ax,(2.65,1.25),(4.05,1.25),'#7850a2')
    ax.add_patch(Rectangle((4.1,.65),.8,1.2,facecolor='#e1efef',edgecolor=INK))
    for sx,sy in [(4.3,.85),(4.6,1.15),(4.3,1.5),(4.65,1.65)]:ax.add_patch(Circle((sx,sy),.04,color=TEAL))
    arrow(ax,(4.5,1.3),(4.5,2.25),'#7850a2')
    arrow(ax,(4.65,1.3),(4.65,2.25),TEAL)
    ax.add_patch(Rectangle((4.1,2.3),.9,.12,facecolor=TEAL,alpha=.6))
    arrow(ax,(4.65,2.5),(4.65,3.1),TEAL)
    ax.text(.8,.35,tr('光源','Light source'),ha='center',fontsize=10)
    ax.text(2.5,.35,tr('选色滤光片','Incident filter'),ha='center',fontsize=10)
    ax.text(4.5,.35,tr('液体样品','Liquid specimen'),ha='center',fontsize=10)
    ax.text(5.2,2.35,tr('抑制原色，观察弱散射','Reject original color; observe shifted light'),fontsize=10,color=TEAL)
    ax.text(6.1,1.25,tr('入射与收集方向分开\n先选光，再辨认变化',
        'Separate illumination and collection\nSelect light before comparing its color'),fontsize=12,linespacing=1.8)
    ax=axes[1];ax.set_title(tr('现代：聚焦、滤光、分光、计数','Modern: Focus, reject, disperse and count'),loc='left',pad=12)
    ax.add_patch(Rectangle((.35,1.6),1.1,.6,facecolor='#e8eff2',edgecolor=INK))
    ax.text(.9,1.9,tr('激光','Laser'),ha='center',va='center')
    arrow(ax,(1.5,1.9),(3.7,1.9),BLUE)
    ax.plot([3.7,4.15],[2.1,1.65],color=INK,lw=3)
    arrow(ax,(3.92,1.7),(3.92,.9),BLUE)
    ax.add_patch(Rectangle((3.55,.65),.8,.25,facecolor='#d5e2e8',edgecolor=INK))
    ax.plot([3.55,3.75,4.15,4.35],[.65,.42,.42,.65],color=INK)
    ax.add_patch(Rectangle((3.5,.05),1,.12,facecolor=TEAL))
    arrow(ax,(4.15,.3),(4.15,2.48),TEAL)
    ax.plot([3.95,4.35],[2.35,2.75],color=INK,lw=2)
    arrow(ax,(4.35,2.55),(5.65,2.55),TEAL)
    ax.add_patch(Rectangle((5.75,2.1),.15,.9,facecolor=TEAL,alpha=.65))
    arrow(ax,(6,2.55),(7.8,2.55),TEAL)
    ax.plot([8,8.3],[2.15,2.95],color=INK,lw=4)
    for k in range(5):ax.plot([7.96+.06*k,8.08+.06*k],[2.17+.15*k,2.15+.15*k],color='#8895a5')
    for y,col in [(2.,ORANGE),(2.5,TEAL),(3.,BLUE)]:arrow(ax,(8.35,2.55),(9.85,y),col)
    ax.add_patch(Rectangle((9.9,1.75),.24,1.5,facecolor='#e8eff2',edgecolor=INK))
    for y in np.linspace(1.8,3.2,11):ax.plot([9.9,10.14],[y,y],color='#8b98a5',lw=.7)
    ax.text(3.35,.65,tr('物镜','Objective'),ha='right',fontsize=10)
    ax.text(3.98,-.2,tr('样品','Specimen'),ha='center',fontsize=10)
    ax.text(5.82,1.7,tr('瑞利抑制','Rayleigh rejection'),ha='center',fontsize=10)
    ax.text(8.1,1.7,tr('光栅','Grating'),ha='center',fontsize=10)
    ax.text(10.02,1.3,tr('像素阵列','Pixel array'),ha='center',fontsize=10)
    ax.text(7.3,.5,tr('像素 → 波长 → 拉曼位移','Pixels → wavelength → Raman shift'),ha='center')
    save(fig,'optics')

    # Figure 2: energy bookkeeping, not a molecular potential-energy curve.
    fig,axes=plt.subplots(1,3,figsize=(11.8,4.5),layout='constrained')
    for ax,name,start,end in zip(axes,[tr('瑞利','Rayleigh'),tr('斯托克斯','Stokes'),tr('反斯托克斯','Anti-Stokes')],[0,0,1],[0,1,0]):
        ax.set(xlim=(0,3),ylim=(-.5,4.9));ax.axis('off');ax.set_title(name)
        for y in [0,1]:ax.plot([.2,2.8],[y,y],color=INK,lw=1.6)
        virtual=3+start
        ax.plot([.2,2.8],[virtual,virtual],color='#8b93a0',ls='--',lw=1.4)
        arrow(ax,(.85,start),(.85,virtual),BLUE);arrow(ax,(2.1,virtual),(2.1,end),TEAL)
        ax.text(1.5,virtual+.28,tr('虚能级（过程表示）','Virtual level (process representation)'),ha='center',fontsize=9)
        ax.text(2.7,-.32,'v = 0',ha='right',fontsize=9)
        ax.text(2.7,1.16,'v = 1',ha='right',fontsize=9)
        ax.text(.4,2.05,tr('入射','In'),color=BLUE);ax.text(2.25,2.05,tr('散射','Out'),color=TEAL)
    save(fig,'energy')

    # Independent photon counts; all generating parameters remain inspectable.
    rng=np.random.default_rng(248)
    x=np.arange(600.,1801.)
    base=110+.035*(x-600)+.000045*(x-1200)**2
    truth=two_bands(x,6000,1000,9,3600,1040,14)+band(x,12000,1450,28)
    raw=rng.poisson(base+truth).astype(float)
    anchors=(x<950)|((x>1120)&(x<1320))|(x>1560)
    contaminated=anchors|((x>1380)&(x<1520))
    fit_base=lambda m:np.polyval(np.polyfit((x[m]-1200)/600,raw[m],2),(x-1200)/600)
    good,bad=fit_base(anchors),fit_base(contaminated)
    region=(x>=950)&(x<=1120)
    def fit(background):
        return curve_fit(two_bands,x[region],(raw-background)[region],
           p0=[6000,1000,9,3600,1040,14],
           bounds=([0,990,3,0,1025,3],[20000,1010,25,20000,1055,35]),maxfev=20000)[0]
    params,biased=fit(good),fit(bad)
    model=two_bands(x[region],*params)
    residual=(raw-good)[region]-model
    np.savetxt(output/'spectrum.csv',np.column_stack([x,raw,base,truth,good,bad]),delimiter=',',
       header='shift_cm-1,raw_counts,true_background,true_bands,estimated_background,contaminated_background',comments='')
    fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
    ax=axes[0,0];ax.plot(x,raw,color='#8895a5',lw=.7,label=tr('原始计数','Raw counts'))
    ax.plot(x,good,color=TEAL,lw=2,label=tr('无峰区估计','Clean anchors'))
    ax.plot(x,bad,color=ORANGE,lw=2,label=tr('含峰区估计','Contaminated anchors'))
    ax.set(title=tr('A · 原始信号与两种基线','A · Raw signal and two baselines'),ylabel=tr('计数','Counts'));ax.legend(fontsize=9)
    ax=axes[0,1];ax.plot(x[region],(raw-good)[region],'.',ms=3,color='#8a95a5',label=tr('扣除基线','Corrected'))
    ax.plot(x[region],model,color=INK,label=tr('双峰拟合','Two-band fit'))
    ax.fill_between(x[region],band(x[region],*params[:3]),alpha=.2,color=BLUE)
    ax.fill_between(x[region],band(x[region],*params[3:]),alpha=.2,color=TEAL)
    ax.set(title=tr('B · 相邻峰分别贡献多少','B · Contributions of neighboring bands'),ylabel=tr('计数','Counts'));ax.legend(fontsize=9)
    ax=axes[1,0];ax.plot(x[region],residual,color=BLUE,lw=.9);ax.axhline(0,color=INK,lw=1)
    ax.set(title=tr('C · 残差保留处理线索','C · Residuals retain diagnostic evidence'),ylabel=tr('数据 − 拟合 / 计数','Data − fit / counts'))
    ax=axes[1,1];ratios=[.6,params[3]/params[0],biased[3]/biased[0]]
    ax.bar([0,1,2],ratios,color=['#8b98a5',TEAL,ORANGE],width=.55)
    ax.axhline(.6,color=INK,ls='--',lw=1)
    ax.set(xticks=[0,1,2],xticklabels=[tr('真值','Truth'),tr('无峰区','Clean anchors'),tr('含峰区','Contaminated')],
       ylabel=tr('第二峰面积 / 第一峰面积','Second / first band area'),title=tr('D · 基线选择改变面积比','D · Baseline choice changes the area ratio'),ylim=(0,max(.9,max(ratios)*1.2)))
    for i,v in enumerate(ratios):ax.text(i,v+.025,f'{v:.3f}',ha='center')
    for ax in [axes[0,0],axes[0,1],axes[1,0]]:ax.set_xlabel(tr('拉曼位移 / cm$^{-1}$','Raman shift / cm$^{-1}$'))
    save(fig,'processing')

    fig,axes=plt.subplots(1,2,figsize=(11.8,4.8),layout='constrained')
    t=np.linspace(.1,20,300)
    for b,color in [(1,BLUE),(.25,TEAL)]:axes[0].plot(t,signal_to_noise(1,t,b),color=color,label=tr('背景系数','Background factor')+f' {b:g}')
    axes[0].set(xlabel=tr('曝光时间 / s','Exposure time / s'),ylabel=tr('信噪比','Signal-to-noise ratio'),title=tr('A · 收集更久或降低背景','A · Collect longer or reduce background'));axes[0].legend()
    power=np.linspace(.1,5,150);time=np.linspace(.1,20,180);pp,tt=np.meshgrid(power,time)
    im=axes[1].pcolormesh(pp,tt,signal_to_noise(pp,tt),shading='auto',cmap='viridis')
    cs=axes[1].contour(pp,tt,200*pp*tt,levels=[3000],colors='white',linewidths=1.8)
    axes[1].clabel(cs,fmt={3000:tr('计数上限','Count limit')},fontsize=9)
    axes[1].set(xlabel=tr('功率系数','Power factor'),ylabel=tr('曝光时间 / s','Exposure time / s'),title=tr('B · 先确认线性记录范围','B · Identify the linear recording range'))
    fig.colorbar(im,ax=axes[1],label=tr('理想信噪比','Ideal signal-to-noise ratio'))
    save(fig,'acquisition')
    summary={'data_kind':'constructed teaching spectrum','seed':248,
      'stokes_532_nm':1/(1/532-1000/1e7),'stokes_785_nm':1/(1/785-1000/1e7),
      'energy_1000_eV':6.62607015e-34*299792458*1000*100/1.602176634e-19,
      'true_area_ratio':.6,'fitted_area_ratio':float(params[3]/params[0]),
      'contaminated_area_ratio':float(biased[3]/biased[0]),'parameters':params.tolist(),
      'snr_example_without_read_noise':float(200/np.sqrt(1000)),
      'lab_snr_default':float(signal_to_noise(1,5)),
      'residual_rms':float(np.sqrt(np.mean(residual**2)))}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en')
    args=parser.parse_args();main(args.output,args.language)
```

The fit constrains centers and widths to meaningful intervals so that an optimizer cannot explain noise by moving a component far away or assigning a negative width. Such constraints should reflect instrument resolution, expected spectral regions and the experimental question. The program retains residuals and uses fixed baseline rules, including a deliberately contaminated anchor selection as a comparison. One instructive modification is to move the broad band toward an anchor region and follow the resulting baseline and area-ratio changes. This directly tests an assumption of the procedure. It provides more insight than trying many smoothing settings and retaining whichever output looks cleanest, because the relation between a physical feature and a processing bias remains visible.

![Exposure gains and recording limits in the same counting model. Left: ideal signal-to-noise ratios for background factors 1 and 0.25. Right: conditions above the white contour exceed 3000 total peak counts. Color represents the unclipped counting model; the contour identifies where recorded values begin to diverge from it.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/90047422a994086ced88293a.svg?v=90047422a994)

Figure 4Exposure gains and recording limits in the same counting model. Left: ideal signal-to-noise ratios for background factors 1 and 0.25. Right: conditions above the white contour exceed 3000 total peak counts. Color represents the unclipped counting model; the contour identifies where recorded values begin to diverge from it.

The power–time diagram uses the same counting rules as the interactive experiment. Color represents signal-to-noise ratio, and the contour marks a selected detector-count limit. Within a linear response range and for a stable specimen, collecting more photons improves counting precision. At the limit, the recorded peak clips; further exposure cannot reconstruct the lost top of the peak. Real instruments have count limits, dark current, read noise and gain settings that differ from this teaching model. Their values can be established from instrument documentation and dark and linearity measurements before comparing acquisition strategies. The purpose of the diagram is to connect those parameters, making visible why a longer or brighter acquisition is useful only within a defined measurement regime.

A useful retained record includes raw data, acquisition conditions, references and blanks, processing parameters and the summary that supports the interpretation. These items form a traceable relationship: the reported area points to an integration interval, that interval points to the corrected spectrum, and the correction points to a baseline rule and its input measurements. If a substrate contribution is recognized later, the calculation can be repeated without guessing the original operations. This relationship also makes disagreements productive. Different researchers can compare how their anchor regions or line-shape choices affect the same observations, then determine which additional control would discriminate between the interpretations. The final graph becomes the visible end of an understandable measurement rather than an isolated picture.

## Returning the spectrum to the research question

Consider a protein-containing hydrogel whose composition may redistribute after treatment. Begin by checking that power, exposure and focusing conditions are comparable across locations, then inspect whether related bands change together. If all bands increase together, sampled volume or focus is an immediate candidate explanation. If one set changes relative to an independently justified stable reference, a compositional interpretation becomes more plausible. Map the relevant area ratio and compare it with an optical image, specimen geometry or another chemical measurement. The spatial agreement between independent observations helps determine whether a spectral contrast corresponds to an actual structural region. The conclusion develops from several compatible observations rather than from the visual prominence of one peak.

In a polymer film, changes in positions and widths may also contain information about temperature, stress or structural order. Quantitative use requires a relationship established for the relevant material and optical configuration. For example, a controlled temperature series can relate a chosen band position to temperature before an unknown state is investigated. An empirical coefficient from another material may respond to a different structure or phase. If stretching changes intensity, measurements at several polarization directions can help separate orientation from composition. If a band drifts during illumination, separate power and time series can reveal a laser-heating contribution. Each additional measurement should target an interpretation that the original spectrum alone leaves unresolved.

Surface-enhanced, resonance and coherent Raman methods extend the accessible questions while introducing additional signal-formation mechanisms. Surface-enhanced Raman measurements use effects near metallic nanostructures, including enhanced local electromagnetic fields, to strengthen selected molecular signals. Distance from an enhancing region, adsorption geometry and the distribution of those regions can strongly influence intensity. A large signal therefore reflects which molecules experience the enhancing environment as well as their abundance. Understanding sampling, response and background in ordinary Raman spectroscopy prepares a clear set of calibration questions for these methods: where enhancement occurs, which molecules contribute most strongly, and whether a reference experiences an environment comparable to the target.

When reading a Raman result, identify the energy difference on the horizontal axis, the corrections represented by the vertical axis, the physical or chemical explanation proposed for a change, and the additional observation that would distinguish alternatives. Strong overlap may motivate improved spectral resolution, reference components or a complementary spectrum. Strong spatial heterogeneity motivates a more deliberate sampling design. Raman spectroscopy is valuable because it connects molecular information with a small selected location. Understanding how that information is produced makes it possible to choose the next measurement purposefully, refine the question and use a spectrum as part of a coherent investigation.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/S02.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [C. V. Raman and the Raman Effect — ACS](https://www.acs.org/education/whatischemistry/landmarks/ramaneffect.html)

   Historical context and the filtering logic of the early Raman and Krishnan experiments.
2. [Raja and Barron: Raman Spectroscopy](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Physical_Methods_in_Chemistry_and_Nano_Science_%28Barron%29/04%3A_Chemical_Speciation/4.03%3A_Raman_Spectroscopy)

   Scattering energy diagrams, selection rules and further reading on surface-enhanced Raman spectroscopy.

   CC BY 4.0 page; cited as open reading.
3. [NIST: Raman Intensity Calibration With Glass Luminescence Standards](https://www.nist.gov/publications/raman-intensity-calibration-glass-luminescence-standards)

   Understand wavelength-dependent instrumental response and relative intensity calibration.
4. [RamanSPy: Preprocessing](https://ramanspy.readthedocs.io/en/latest/preprocessing.html)

   Open software entry point for baseline estimation, despiking, smoothing and normalization.
5. [SciPy: curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

   Nonlinear least-squares parameters, bounds and covariance documentation.
