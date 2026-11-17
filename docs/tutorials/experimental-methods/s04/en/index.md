# Fluorescence spectroscopy: Intensity, lifetime and molecular environment

Source: https://ml-biomat.com/tutorials/experimental-methods/s04/en/
Language: en

A dimmer sample may contain fewer emitters or different energy-relaxation pathways. Connect intensity, lifetime and optical transmission.

## When a sample becomes dimmer, what changed?

A fluorescently labeled protein shines brightly in water. After a piece of hydrogel is added, the solution becomes dimmer. One attractive explanation is that the gel has captured some of the protein. Several other changes can produce the same observation: the dye may encounter a different molecular environment, the gel may absorb the excitation light, or particles may scatter emitted light away from the detector. A useful fluorescence experiment separates these possibilities. The first question is therefore not simply how bright the sample looks, but which physical step connects the object of interest to the photons being counted.

Fluorescence begins when a molecule absorbs light and enters an excited electronic state. Some of that excitation energy can subsequently leave as a new photon. The emitted photon is usually lower in energy than the absorbed photon, which makes it possible to separate illumination from emission using optical filters. A familiar fluorescent highlighter seems unusually vivid because it adds emitted light to reflected light. A biological experiment uses the same principle to distinguish a labeled molecule from its surroundings, while a materials experiment can use the emission spectrum or its timing to probe the environment around a dye.

The light-emitting molecular unit is called a fluorophore. It may be a small organic dye, part of a fluorescent protein, or a structural feature already present in the sample. Attaching a fluorophore to a protein introduces a label whose position and number matter. A dye on a binding surface can alter molecular recognition; several dyes close together can interact; free dye left after labeling contributes signal without reporting the protein. Before turning brightness into an amount, establish what actually carries the label, how much unbound label remains, and whether the labeled object retains the behavior being investigated.

This chapter follows a single experimental puzzle: why did the fluorescence decrease? We will compare changes in molecular number, excited-state relaxation and optical transmission. Steady-state measurements count emission accumulated over a measurement interval. Time-resolved measurements follow how the probability of emission changes after excitation. Combining these two views gives a more informative experiment than treating intensity as an isolated number. The complete example later in the chapter includes a real fluorescent-protein structure and constructed photon-counting data, so structural evidence and numerical teaching models remain clearly identified.

## From Stokes's observation to a protein that protects its own light source

In 1852, George Gabriel Stokes used the term fluorescence while studying substances that changed the apparent refrangibility of light. The central observation was that illuminating a material with one spectral region could produce light in another. This difference remains a practical foundation of the modern experiment. An excitation filter selects the light sent toward the specimen, and an emission filter rejects much of that illumination while transmitting a chosen portion of the fluorescence. The separation between excitation and emission is useful because the illumination can be much stronger than the signal being sought.

The familiar shift toward longer emission wavelengths reflects energy lost between absorption and emission. An excited molecule can quickly redistribute energy among vibrations and exchange energy with surrounding molecules before a photon is released. A useful analogy is arriving at an upper floor and walking down a few steps before taking a lift back down: the final return covers less energy than the initial ascent. The analogy concerns energy differences rather than a literal path through space. Molecular electronic states and vibrational levels determine the possible transitions, and the surrounding medium influences how readily different relaxation routes occur.

A striking biological example is green fluorescent protein. In the 1996 structural study represented by PDB entry 1EMA, the fluorescent molecular group lies inside a barrel formed by eleven strands of the protein chain. A central helix runs through the barrel, placing the chromophore in a protected molecular setting. The structure makes an important point visible: a fluorophore does not work independently of its surroundings. The protein fold helps define the chemical and mechanical environment that allows the chromophore to emit. Changing nearby interactions can change the optical behavior even when the number of protein molecules stays constant.

![Two principal-coordinate projections of real PDB 1EMA crystallographic coordinates. Color follows sequence; red points mark CRO chromophore atoms. Sequence gaps are not bridged. This engineered GFP structure was published in 1996 at 1.90 Å resolution. Coordinates CC0; Ormö et al., Science, DOI 10.1126/science.273.5280.1392.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/905d3906122e14d3e39867f9.svg?v=905d3906122e)

Figure 1Two principal-coordinate projections of real PDB 1EMA crystallographic coordinates. Color follows sequence; red points mark CRO chromophore atoms. Sequence gaps are not bridged. This engineered GFP structure was published in 1996 at 1.90 Å resolution. Coordinates CC0; Ormö et al., Science, DOI 10.1126/science.273.5280.1392.

The figure uses the openly available atomic coordinates of 1EMA. This is an engineered GFP structure with a threonine-containing chromophore precursor, determined at 1.90 Å resolution; it is not presented as the sequence of every naturally occurring fluorescent protein. The backbone trace and highlighted chromophore are calculated from those coordinates. A trace helps reveal the enclosing architecture, while a second view helps locate the chromophore within it. The drawing is a representation of a crystal structure, rather than a photograph or a measurement of a molecule moving in solution.

The same environmental argument applies to materials. Embedding a dye in a polymer can restrict its rotation, alter local polarity, change access to oxygen, or bring neighboring dyes close together. Each change can affect competing relaxation pathways. A dye that brightens inside a rigid material may be reporting restricted motion rather than a larger dye concentration. This is why fluorescent probes can be valuable sensors: their response can connect a molecular environment to an optical signal. To use that connection quantitatively, the relevant environmental variable must be calibrated while other influential variables are controlled or measured.

## Brightness and lifetime describe different parts of the same competition

A Jablonski diagram arranges molecular states vertically by energy. Absorption is drawn upward because the molecule gains energy. Rapid vibrational relaxation brings the excited population toward lower vibrational levels of an excited electronic state. Fluorescence is one possible downward transition, while nonradiative relaxation transfers energy without producing the measured fluorescence photon. The diagram is a map of competing routes, not a time trace and not a drawing of the physical locations of electrons. Arrow length represents an energy difference; a wavy arrow usually identifies a nonradiative route.

![Original energy-level and spectral schematics. S₀ and S₁ denote the ground and first excited singlet states; horizontal levels represent vibrations. Energy lost before fluorescence shifts emission toward longer wavelength. The right-hand bands are constructed examples, not measured 1EMA spectra.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/0cd25e4ba0047a0939dc3f6d.svg?v=0cd25e4ba004)

Figure 2Original energy-level and spectral schematics. S₀ and S₁ denote the ground and first excited singlet states; horizontal levels represent vibrations. Energy lost before fluorescence shifts emission toward longer wavelength. The right-hand bands are constructed examples, not measured 1EMA spectra.

The fluorescence quantum yield answers a counting question: among the photons absorbed by the fluorophores, what fraction eventually produces fluorescence photons? A yield of 0.60 means an average of sixty fluorescence photons for every hundred absorbed photons under the specified conditions. It does not mean that sixty percent of the lamp output reaches the detector. Much of the illumination may miss the sample, much of the fluorescence travels outside the collection angle, and filters and detectors have their own efficiencies. Those losses belong to the optical measurement chain, whereas quantum yield describes the emission probability after absorption.

$$
\Phi_F=\frac{N_{\mathrm{em}}}{N_{\mathrm{abs}}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/640affc4e10d6a3e71336f70.svg) | Fluorescence quantum yield, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/179ba6249c87305283cae0ec.svg) | Number of fluorescence photons emitted under the specified conditions. |
| ![Formula](https://ml-biomat.com/static/agent-math/7e580857aa2a9a5ffee93726.svg) | Number of excitation photons absorbed by the relevant fluorophores. |

The yield compares emitted and absorbed photon numbers; optical collection efficiency is separate. An average of 60 fluorescence photons for 100 absorbed photons gives 0.60.

Imagine an excited population in a room with two exits. One exit releases a fluorescence photon; the other transfers energy through nonradiative processes. If each excited molecule has a constant chance per unit time of using either exit, the remaining population decreases exponentially. The fluorescence lifetime describes the characteristic time of that decrease. It is an average waiting-time parameter for the population under this model, rather than a promise that every molecule emits after exactly the same delay. Some events occur early and others later, producing a distribution of photon arrival times.

$$
\tau=\frac{1}{k_f+k_{nr}},\qquad \Phi_F=\frac{k_f}{k_f+k_{nr}}=k_f\tau
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | Single-exponential excited-state lifetime; ns when rates are in ns⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/eb0658bce80f3e4e9eccf061.svg) | Fluorescence radiative rate constant, ns⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/03b58580d0df47598b5c77c3.svg) | Combined nonradiative relaxation rate constant, ns⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/640affc4e10d6a3e71336f70.svg) | Fluorescence quantum yield, dimensionless. |

Independent constant relaxation rates add; the radiative share gives emission probability. With kf=0.15 and knr=0.10 ns⁻¹, τ=4 ns and ΦF=0.60. Raising knr to 0.35 ns⁻¹ gives τ=2 ns and ΦF=0.30.

For a radiative rate of 0.15 ns⁻¹ and a nonradiative rate of 0.10 ns⁻¹, the total escape rate is 0.25 ns⁻¹. Its reciprocal gives a lifetime of 4 ns, and the radiative share gives a quantum yield of 0.60. If an additional process increases the total nonradiative rate to 0.35 ns⁻¹ while the radiative rate stays unchanged, the lifetime becomes 2 ns and the yield becomes 0.30. The excited population leaves more quickly, and a smaller fraction leaves by emitting fluorescence. These numbers will reappear in the decay example and the interactive experiment.

Changing the number of identical fluorophores has a different effect. Under weak excitation, doubling their number doubles the expected fluorescence signal but leaves their individual relaxation rates unchanged. The decay shape and lifetime can therefore remain the same. An optical filter placed after the sample can also lower the detected intensity without changing the lifetime. Conversely, two environments can produce the same quantum yield with different total rates and therefore different lifetimes. Intensity and lifetime are related through a physical model; neither is a universal substitute for the other.

## Follow the light before interpreting the curve

A conventional solution fluorometer often collects emission approximately at right angles to the excitation beam. This geometry reduces the amount of directly transmitted illumination entering the emission optics. It does not eliminate all scattered light: dust, aggregates, cuvette scratches and interfaces can redirect excitation toward the detector. A matched solvent blank shows contributions from the solvent and optical arrangement, while an unlabeled specimen reveals its own fluorescence and scattering. The appropriate controls depend on the object being studied. A clear buffer is not a complete background match for a cloudy suspension.

An emission scan holds the excitation wavelength fixed and records signal while the detection wavelength changes. An excitation scan holds the detection band fixed and changes the illumination wavelength. The latter can resemble an absorption spectrum when the same emitting species dominates and the instrument response has been corrected, but the experiment detects the pathway that leads to the chosen emission. A material that absorbs strongly without producing that emission can appear in an absorption spectrum and contribute little to the excitation spectrum. Reading the axis labels therefore identifies which optical question was actually asked.

Slit widths select a tradeoff between collected light and spectral discrimination. A wider band usually admits more photons but combines a broader range of wavelengths. Detector gain changes the relationship between photons and recorded electrical output; exposure or integration time changes how many events are accumulated. If these settings vary between specimens, raw numbers may not be directly comparable. Relative fluorescence units still have a precise operational meaning when acquisition settings and corrections are recorded. The word relative does not remove the need to explain the measurement scale.

Time-correlated single-photon counting adds a second axis. Repeated excitation pulses provide a timing reference, and the instrument records the delay between a pulse and a detected photon. Many repetitions build a histogram of these delays. Each time bin contains a photon count, so it has both a time position and counting uncertainty. Detection probabilities must be appropriate for the acquisition method; excessive count rates can distort the timing distribution. A background measurement estimates counts that do not belong to the desired decay, including dark counts and unrelated emission.

$$
C(t)=C_0e^{-t/\tau}+B
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c4e857df82e09ece3691e350.svg) | Expected photon count in the bin at delay t. |
| ![Formula](https://ml-biomat.com/static/agent-math/8e1f255f71ebe5898eee968b.svg) | Decay amplitude at the chosen time origin, in counts. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Delay relative to the selected origin, ns. |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | Lifetime, ns. |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | Constant expected background count per bin. |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | Base of the natural exponential, dimensionless. |

A constant total rate removes the same fraction of excited population in equal intervals. C₀=1000, τ=4 ns and B=5 give about 372.88 counts at t=4 ns. Instrument response convolves this curve. The code uses a 0.6 ns origin for tail amplitude, separating the amplitude convention from timing.

The instrument also broadens an ideal instantaneous event. Its response includes the excitation pulse width, detector timing and electronics. The measured decay is the underlying emission response blurred by this instrument response and combined with background. When the lifetime is comfortably longer than that response, a suitably chosen late portion may approximate an exponential tail. When the two timescales are similar, fitting should explicitly include the response through reconvolution. Moving the fit start provides a useful diagnostic: a result that changes strongly when early bins are excluded may be responding to timing structure rather than a single physical lifetime.

A mixed specimen can contain several emitting environments. Its decay may then contain several components or a continuous distribution of rates. An average lifetime is meaningful only with its definition: a coefficient-weighted average and a photon-weighted average emphasize components differently. Additional fitted exponentials do not automatically identify additional chemical species, because different models can describe similar finite-noise curves. Connect a model to independent information such as known components, environmental changes, spectra or a controlled titration. The research question determines which level of description is useful.

## Separate fewer emitters from faster energy loss

Quenching describes a decrease in fluorescence caused by processes that reduce emission. In dynamic quenching, an excited fluorophore encounters another species and loses excitation through an additional nonradiative route. More quencher increases the collision-related escape rate. In an ideal homogeneous system with unchanged absorption and radiative rate, intensity and lifetime decrease together according to the Stern–Volmer relationship. The relationship becomes understandable once the extra escape rate is added to the existing rates, rather than memorized as a line fitted to a titration.

$$
\frac{F_0}{F}=\frac{\tau_0}{\tau}=1+k_q\tau_0[Q]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5d9e14fe75a38925a319a02a.svg) | Fluorescence intensities without and with quencher, in common units and optical conditions. |
| ![Formula](https://ml-biomat.com/static/agent-math/fae386ec28f71b21891ce220.svg) | Lifetimes without and with quencher, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/0360f5bd937533952ffbd944.svg) | Bimolecular dynamic-quenching rate constant, L·mol⁻¹·s⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/b53c8032c8dea25111a89d21.svg) | Quencher concentration, mol·L⁻¹. |

Pure homogeneous dynamic quenching adds kq[Q], with absorption, fluorophore amount and radiative rate fixed. kq=5×10⁹, τ₀=4×10⁻⁹ s and [Q]=0.05 mol/L give a ratio of 2 and τ=2 ns. Measuring both intensity and lifetime tests this model.

Take an unquenched lifetime of 4 ns and a bimolecular quenching rate constant of 5 × 10⁹ L mol⁻¹ s⁻¹. At a quencher concentration of 0.05 mol/L, the added decay rate is 2.5 × 10⁸ s⁻¹, equal to the original total decay rate. The lifetime becomes 2 ns and the ideal fluorescence intensity falls by a factor of two. This numerical example assumes the quencher does not substantially change excitation absorption, detector collection, fluorophore concentration or other relaxation mechanisms. Those assumptions identify which controls make a Stern–Volmer plot interpretable.

## Separate three reasons for becoming dimmer

First reduce molecular amount, then restore it and add dynamic quencher, then reduce only transmission of emitted light. Compare absolute intensity and individually normalized decays: which operation changes the molecular waiting time? The model assumes one emitting environment, weak excitation and ideal optical attenuation.

The gray dashed curve is the initial 4 ns state. Integrated signal is relative amount × quantum yield × optical transmission. Normalization removes amplitude differences caused by amount and optical collection.

The interactive experiment separates molecular amount, dynamic quenching and optical transmission. Reducing the amount lowers the whole signal while preserving its normalized time profile. Adding quencher changes the rate of the profile as well as its integrated area. Reducing transmission after emission changes the number of detected photons without changing the molecular lifetime. Compare both the absolute curve and the normalized curve: normalization makes timing easier to compare but intentionally removes information about overall brightness. The numerical readout preserves that missing information.

Static quenching involves a different arrangement, such as formation of a nonfluorescent ground-state complex. The remaining uncomplexed molecules may retain their original lifetime even as the total intensity decreases. Optical attenuation can produce a superficially similar intensity-lifetime pattern. Absorption spectra, concentration dependence and binding measurements help distinguish the two. Photobleaching introduces another timescale: irreversible photochemical changes reduce the emitting population over the duration of illumination. A decline over seconds of exposure is different from an excited-state decay occurring over nanoseconds after each pulse.

Inner-filter effects arise when excitation is substantially attenuated inside the sample or emitted light is reabsorbed before reaching the detector. A concentrated solution may therefore increase less than expected in brightness and can even become dimmer as more fluorophore is added. For a simple right-angle observation centered in a rectangular cuvette, a midpoint approximation illustrates the two attenuation paths. It is useful for understanding why absorption at both excitation and emission wavelengths matters. Actual corrections depend on the collection volume, geometry, spectral bandwidth and the sample's optical properties.

$$
F_{\mathrm{obs}}\approx F_{\mathrm{ideal}}\,10^{-(A_{\mathrm{ex}}+A_{\mathrm{em}})/2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6801b4fb188ade5ad0c3a6a0.svg) | Observed intensity with inner-filter attenuation, relative units. |
| ![Formula](https://ml-biomat.com/static/agent-math/779a333ebe703b3b7c55e3ce.svg) | Ideal intensity without excitation/emission attenuation inside the sample, same units. |
| ![Formula](https://ml-biomat.com/static/agent-math/19bd174de2b2325f0a926e4c.svg) | Absorbances at excitation and emission wavelengths over the full cuvette path, dimensionless. |

For midpoint collection in a rectangular cuvette, excitation and emission each travel half a full path, so their transmissions multiply. Aex=0.40 and Aem=0.20 give 10⁻⁰·³≈0.5012. Actual observation volume and geometry determine the appropriate integration or correction.

When excitation absorbance is 0.40 and emission absorbance is 0.20 across the full cuvette path, the midpoint factor is approximately 0.50. In that model, half of the ideal fluorescence reaches the selected observation pathway. Diluting a concentrated sample and checking whether a properly scaled spectrum converges toward a common shape is often more informative than applying a large correction without checking the geometry. A matched dilution sequence also helps reveal concentration-dependent aggregation or chemistry, which will not necessarily disappear through an optical correction alone.

## A complete example: count photons, fit a decay and inspect the assumptions

The program below draws the real 1EMA structure from the bundled coordinate file and independently constructs two fluorescence-decay experiments. The decay data are teaching simulations, not measurements made on the 1EMA crystal. Their prescribed lifetimes are 4 and 2 ns. A narrow response function broadens the excitation timing, a constant background adds counts, and Poisson sampling produces fluctuations appropriate to a counting model. Keeping the generating assumptions visible lets us test whether the analysis recovers the intended timescale and where the fit begins to depend on an acquisition choice.

![Constructed 4 ns and 2 ns photon-count experiments. A retains counts and fits after 1.2 ns; B subtracts background and divides by fitted amplitude; C scales residuals by estimated count SD; D changes fit start, with parameter standard errors from fit covariance. Data include a 0.12 ns response width and Poisson fluctuations.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/38a8f8b245a9f5e4ebef8f82.svg?v=38a8f8b245a9)

Figure 3Constructed 4 ns and 2 ns photon-count experiments. A retains counts and fits after 1.2 ns; B subtracts background and divides by fitted amplitude; C scales residuals by estimated count SD; D changes fit start, with parameter standard errors from fit covariance. Data include a 0.12 ns response width and Poisson fluctuations.

The analysis fits an exponential plus a background to a tail region that begins after the main instrument response. It reports fitted lifetimes, draws residuals and repeats the fit with several starting times. Residuals are the observed counts minus the fitted counts, scaled by the estimated counting noise. Random-looking fluctuations of an appropriate size are consistent with the selected description; a systematic early feature points toward an omitted response contribution. At late times, background becomes a larger share of the measured signal, so keeping fewer bins can also reduce the information available for estimating the decay.

### From real protein coordinates to photon counts and lifetime diagnostics

The complete program reads bundled 1EMA coordinates offline, separately constructs count data, fits decays and checks fit-start sensitivity, exporting every figure and CSV. Real structure and simulated counts are distinguished.

```
"""Fluorescence: real PDB structure and explicitly constructed photon-count data.

Run: python main.py --output results --language en
Dependencies: numpy, scipy, matplotlib. No network access is needed.
1EMA coordinates: PDB archive CC0; Ormo et al., Science (1996),
https://doi.org/10.1126/science.273.5280.1392 .
"""
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

P = argparse.ArgumentParser()
P.add_argument("--output", type=Path, default=Path("results"))
P.add_argument("--language", choices=["zh", "en"], default="en")
args = P.parse_args()
OUT = args.output
OUT.mkdir(parents=True, exist_ok=True)
ZH = args.language == "zh"
def tr(zh, en): return zh if ZH else en
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Microsoft YaHei", "DejaVu Sans"],
    "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
    "axes.labelcolor": "#263d49", "text.color": "#263d49", "axes.edgecolor": "#9bacb1",
    "figure.facecolor": "#fbfaf6", "axes.facecolor": "#fbfaf6", "svg.fonttype": "path"})
BLUE, TEAL, CORAL, GOLD, GRAY = "#265f85", "#078579", "#d6604d", "#ba8e2f", "#81949a"
def save(fig, name):
    fig.savefig(OUT / f"{name}-{args.language}.svg", bbox_inches="tight")
    fig.savefig(OUT / f"{name}-{args.language}.png", dpi=155, bbox_inches="tight")
    plt.close(fig)
def panel(ax, letter, title):
    ax.set_title(f"{letter}  {title}", loc="left", weight="bold", pad=14)

# Preserve the real coordinate file; the plotted traces stop at sequence gaps.
atoms, chromophore = [], []
for line in (Path(__file__).parent / "data" / "1EMA.pdb").read_text().splitlines():
    if line[:6].strip() not in {"ATOM", "HETATM"} or line[21] != "A":
        continue
    xyz = [float(line[30:38]), float(line[38:46]), float(line[46:54])]
    if line[17:20] == "CRO": chromophore.append(xyz)
    if line[12:16].strip() == "CA": atoms.append((int(line[22:26]), xyz))
ca = np.array([a[1] for a in atoms]); seq = np.array([a[0] for a in atoms])
cro = np.array(chromophore)
center = ca.mean(axis=0)
# A principal-coordinate projection shows the architecture without inventing atoms.
_, _, basis = np.linalg.svd(ca - center, full_matrices=False)
ca_p = (ca - center) @ basis.T; cro_p = (cro - center) @ basis.T
fig, axs = plt.subplots(1, 2, figsize=(11.6, 5.3))
for ax, dims, letter, title in zip(axs, [(0,1),(1,2)], ["A","B"],
    [tr("沿长轴展开的侧视", "Side view along the long dimension"), tr("沿长轴观察的端视", "End view along the long dimension")]):
    for i in range(len(seq)-1):
        if seq[i+1]-seq[i] == 1:
            ax.plot(ca_p[i:i+2,dims[0]], ca_p[i:i+2,dims[1]], lw=2.1, alpha=.8,
                    color=plt.cm.viridis(i/(len(seq)-1)))
    ax.scatter(cro_p[:,dims[0]], cro_p[:,dims[1]], s=42, color=CORAL, edgecolor="white", lw=.4,
               label=tr("发色团原子", "Chromophore atoms"), zorder=5)
    ax.set_aspect("equal"); ax.set_xlabel(tr("投影坐标 / Å", "Projected coordinate / Å")); ax.set_ylabel(tr("投影坐标 / Å", "Projected coordinate / Å"))
    panel(ax, letter, title); ax.legend(loc="lower left", fontsize=9)
fig.suptitle(tr("GFP 结构 1EMA：真实坐标，原创投影 · 1996", "GFP structure 1EMA: real coordinates, original projection · 1996"), fontsize=15, weight="bold")
fig.text(.5,.01,tr("链 A 的 Cα 轨迹；缺失或非连续残基处断开。CRO 以原子点显示。", "Chain-A Cα trace; gaps are not bridged. CRO is shown as atomic positions."),ha="center",fontsize=10)
fig.tight_layout(rect=[0,.10,1,.94]); save(fig,"structure")

# A conceptual energy diagram: its level spacings are not measured GFP energies.
fig, axs=plt.subplots(1,2,figsize=(11.6,5.2),gridspec_kw={"width_ratios":[1.15,1]})
ax=axs[0];ax.set_xlim(0,10);ax.set_ylim(-.4,5.2);ax.axis("off")
for y in [0,.4,.8]:ax.plot([.5,4.5],[y,y],color=BLUE,lw=2)
for y in [3,3.4,3.8,4.2]:ax.plot([.5,7.8],[y,y],color=BLUE,lw=2)
def arrow(a,b,c):ax.annotate("",xy=b,xytext=a,arrowprops={"arrowstyle":"-|>","color":c,"lw":2.5})
arrow((1.2,0),(1.2,4.2),BLUE);arrow((1.8,4.2),(3.5,3),GOLD);arrow((4.2,3),(4.2,.4),TEAL)
yy=np.linspace(3,0,150);xx=6.5+.16*np.sin(np.linspace(0,10*np.pi,150));ax.plot(xx,yy,color=CORAL,lw=2.3)
ax.text(.05,-.2,r"$S_0$",fontsize=14);ax.text(.05,4.7,r"$S_1$",fontsize=14)
ax.text(.95,2,tr("吸收", "Absorb"),rotation=90,ha="right",color=BLUE)
ax.text(2.1,4.5,tr("振动弛豫", "Vibrational relaxation"),fontsize=10,color=GOLD)
ax.text(4.45,1.5,tr("荧光", "Fluorescence"),rotation=90,va="center",color=TEAL)
ax.text(7.1,1.5,tr("非辐射\n失能", "Nonradiative\nrelaxation"),va="center",fontsize=10,color=CORAL)
panel(ax,"A",tr("Stokes 位移的能量路径", "Energy paths behind the Stokes shift"))
w=np.linspace(380,680,500);exc=np.exp(-.5*((w-470)/22)**2);emi=np.exp(-.5*((w-535)/30)**2)
axs[1].fill_between(w,exc,color=BLUE,alpha=.17);axs[1].plot(w,exc,color=BLUE,label=tr("激发", "Excitation"))
axs[1].fill_between(w,emi,color=TEAL,alpha=.17);axs[1].plot(w,emi,color=TEAL,label=tr("发射", "Emission"))
axs[1].annotate("",xy=(535,1.05),xytext=(470,1.05),arrowprops={"arrowstyle":"<->","color":GRAY})
axs[1].text(502.5,1.1,tr("65 nm（示意）", "65 nm (schematic)"),ha="center",fontsize=10)
axs[1].set(xlim=(380,680),ylim=(0,1.3),xlabel=tr("波长 / nm", "Wavelength / nm"),ylabel=tr("归一化谱强度", "Normalized spectral intensity"));axs[1].legend(frameon=False)
panel(axs[1],"B",tr("分开照明与发射", "Separate illumination and emission"))
fig.text(.5,.01,tr("原理模型；不代表 1EMA 的实测光谱。纵向能级位置表示相对能量。", "Conceptual model, not measured spectra of 1EMA. Vertical energy levels show relative energy."),ha="center",fontsize=10)
fig.tight_layout(rect=[0,.06,1,1]);save(fig,"pathways")

# Two constructed experiments. Time is in ns. The IRF is normalized discretely.
rng=np.random.default_rng(540)
t=np.arange(0,30.0001,.05)
irf=np.exp(-.5*((t-.6)/.12)**2);irf/=irf.sum()
lifetimes=[4.,2.];counts=[];fits=[];sensitivity=[]
def tail(x, amplitude, lifetime, background):return amplitude*np.exp(-(x-.6)/lifetime)+background
for tau in lifetimes:
    expected=np.convolve(1800*np.exp(-t/tau),irf,mode="full")[:len(t)]+5
    observed=rng.poisson(expected);counts.append(observed)
    results=[]
    for start in [.35,.6,.9,1.2,2,4,6]:
        mask=t>=start
        p,cov=curve_fit(tail,t[mask],observed[mask],p0=[1800,tau,5],sigma=np.sqrt(np.maximum(observed[mask],1)),
            absolute_sigma=True,bounds=([0,.1,0],[10000,20,100]),maxfev=15000)
        results.append([start,p[1],np.sqrt(cov[1,1])])
        if start==1.2:fits.append(p)
    sensitivity.append(np.array(results))
fig,axs=plt.subplots(2,2,figsize=(11.6,8.1))
for i,(tau,y,p,col) in enumerate(zip(lifetimes,counts,fits,[TEAL,CORAL])):
    label=tr(f"设定 {tau:g} ns；拟合 {p[1]:.3f} ns",f"Set {tau:g} ns; fit {p[1]:.3f} ns")
    axs[0,0].scatter(t[::3],y[::3],s=9,alpha=.4,color=col)
    mask=t>=1.2;axs[0,0].plot(t[mask],tail(t[mask],*p),color=col,lw=2,label=label)
    norm=(y-p[2])/p[0];axs[0,1].plot(t,norm,color=col,alpha=.7,label=tr(f"{tau:g} ns 组",f"{tau:g} ns group"))
    residual=(y[mask]-tail(t[mask],*p))/np.sqrt(np.maximum(y[mask],1));axs[1,0].plot(t[mask],residual,color=col,alpha=.65,lw=.7)
    ss=sensitivity[i];axs[1,1].errorbar(ss[:,0],ss[:,1],yerr=ss[:,2],color=col,marker="o",capsize=3,label=label)
    axs[1,1].axhline(tau,color=col,ls=":",alpha=.5)
axs[0,0].axvspan(0,1.2,color=GRAY,alpha=.1);axs[0,0].legend(fontsize=9,frameon=False)
axs[0,0].set(xlabel=tr("延迟 / ns","Delay / ns"),ylabel=tr("每时间格计数","Counts per time bin"),xlim=(0,25))
axs[0,1].set(xlabel=tr("延迟 / ns","Delay / ns"),ylabel=tr("扣背景后除以拟合振幅","Background-subtracted / fitted amplitude"),xlim=(0,15));axs[0,1].legend(fontsize=9,frameon=False)
axs[1,0].axhline(0,color=GRAY,lw=1);axs[1,0].set(xlabel=tr("延迟 / ns","Delay / ns"),ylabel=tr("残差 / 估计计数标准差","Residual / estimated count SD"))
axs[1,1].set(xlabel=tr("拟合起点 / ns","Fit starting time / ns"),ylabel=tr("拟合寿命 / ns","Fitted lifetime / ns"));axs[1,1].legend(fontsize=9,frameon=False)
for ax,l,z,e in zip(axs.flat,"ABCD",["保留光子量级","比较衰减形状","检查加权残差","改变拟合起点"],["Retain the count scale","Compare decay shape","Inspect weighted residuals","Change the fit start"]):panel(ax,l,tr(z,e))
fig.tight_layout();save(fig,"decays")

q=np.linspace(0,.1,200);ratio=1+20*q
c=np.linspace(0,50,200);ideal=c*.6;observed=ideal*10**(-(.05*c+.02*c)/2)
fig,axs=plt.subplots(1,2,figsize=(11.6,4.8))
axs[0].plot(q,ratio,color=TEAL,lw=3,label=tr("动态：强度比与寿命比","Dynamic: intensity and lifetime ratios"))
axs[0].plot(q,np.ones_like(q),color=CORAL,lw=2,ls="--",label=tr("纯光学衰减：寿命比","Pure optical attenuation: lifetime ratio"))
axs[0].set(xlabel=tr("猝灭剂浓度 / mol L$^{-1}$","Quencher / mol L$^{-1}$"),ylabel=tr("无猝灭值 / 当前值","Unquenched value / current value"));axs[0].legend(fontsize=9,frameon=False)
axs[1].plot(c,ideal,color=GRAY,ls="--",label=tr("理想浓度响应","Ideal concentration response"));axs[1].plot(c,observed,color=BLUE,lw=3,label=tr("加入内滤的中点近似","With midpoint inner-filter approximation"))
axs[1].set(xlabel=tr("浓度 / μmol L$^{-1}$","Concentration / μmol L$^{-1}$"),ylabel=tr("相对荧光信号","Relative fluorescence signal"));axs[1].legend(fontsize=9,frameon=False)
panel(axs[0],"A",tr("强度与寿命是否一起改变？","Do intensity and lifetime change together?"));panel(axs[1],"B",tr("浓度增加也可能变暗","More concentrated can become dimmer"))
fig.tight_layout();save(fig,"diagnostics")
np.savetxt(OUT/"decay_counts.csv",np.column_stack([t,*counts]),delimiter=",",header="delay_ns,counts_tau4,counts_tau2",comments="")
np.savetxt(OUT/"fit_sensitivity.csv",np.vstack([np.column_stack([np.full(len(s),tau),s]) for tau,s in zip(lifetimes,sensitivity)]),delimiter=",",header="true_tau_ns,start_ns,fitted_tau_ns,standard_error_ns",comments="")
np.savetxt(OUT/"inner_filter.csv",np.column_stack([c,ideal,observed]),delimiter=",",header="concentration_uM,ideal_relative_signal,attenuated_relative_signal",comments="")
summary={"tau_unquenched_ns":1/(.15+.1),"yield_unquenched":.15/(.15+.1),"tau_quenched_ns":1/(.15+.1+5*.05),
    "yield_quenched":.15/(.15+.1+5*.05),"fit_tau4_ns":float(fits[0][1]),"fit_tau2_ns":float(fits[1][1]),
    "chromophore_atoms":len(cro),"backbone_CA_atoms":len(ca),"inner_filter_factor_A04_A02":10**(-.3),
    "data_kind":{"structure":"real crystallographic PDB 1EMA coordinates","decays":"constructed Poisson teaching data"}}
(OUT/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf8")
print(json.dumps(summary,indent=2))
```

The figure includes absolute counts and a background-subtracted normalized view. The absolute view preserves how much signal was collected; the normalized view emphasizes shape. Two curves can overlap after normalization while their integrated photon counts differ substantially. The start-time sensitivity panel keeps this distinction connected to the fitting task. A useful working region has sufficient separation from the instrument response and enough remaining counts to constrain the parameters. The exact region depends on the response width, the lifetime, the background and the statistical precision of the recorded data.

In a Poisson model, the variance of a count equals its expected value. Bright early bins and dim late bins therefore have different absolute uncertainties. The example uses count-dependent weights as an approximation appropriate to these relatively populated bins. For sparse measurements, an explicit Poisson likelihood provides a more direct statistical description. In either case, replacing the constructed arrays with an instrument export requires understanding its time-bin width, repetition period, response measurement and background. Similar file layouts do not establish equivalent experiments.

![Ideal dynamic quenching changes intensity and lifetime together, while pure optical attenuation preserves lifetime. The right panel uses a cuvette-midpoint inner-filter approximation: more concentration increases emitters but attenuates excitation and emission, producing a maximum through competition. Both panels are specified explanatory models.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/ed157303c182f034fe87dceb.svg?v=ed157303c182)

Figure 4Ideal dynamic quenching changes intensity and lifetime together, while pure optical attenuation preserves lifetime. The right panel uses a cuvette-midpoint inner-filter approximation: more concentration increases emitters but attenuates excitation and emission, producing a maximum through competition. Both panels are specified explanatory models.

The final figure compares the ideal intensity and lifetime ratios for dynamic quenching, then shows how inner-filter attenuation changes a concentration series. These calculations organize follow-up experiments. A matched decrease in intensity and lifetime supports testing an additional excited-state relaxation route. A decrease in intensity with stable lifetime directs attention toward amount, static association, photobleaching or optical collection. Absorption measurements, dilution sequences, illumination-time records and binding controls each address a different part of that list. The value of the model lies in choosing observations that separate explanations.

## Choose the object that the fluorescence will represent

Comparisons across days benefit from a stable reference. Detector sensitivity varies with wavelength, and source output or optical alignment can change with time. Wavelength calibration, relative spectral-response correction and a reference specimen examine different parts of the measurement chain. Lifetime work also needs an appropriate timing response or lifetime reference. The solvent, temperature and storage of a reference affect its behavior, so naming the dye alone does not fully specify the comparison. Interleaving reference measurements with specimens helps distinguish instrument drift from a change in the material.

Acquisition order matters for the same reason. If low-concentration specimens are always measured first and high-concentration specimens last, changing source output or cumulative exposure can become entangled with concentration. Interleave groups, repeat a fixed specimen during the sequence, and record exposure time. Oxygen can influence some relaxation and photochemical pathways, so sealing, opening or degassing the container may also alter the response. These choices connect experimental control to the original question: the variable being studied should be separated from conditions that otherwise change alongside it.

For protein adsorption, a decrease in solution fluorescence can indicate removal of labeled protein from solution, but adsorption can also change the dye's environment. Measuring the supernatant, surface-associated material and an appropriate eluate can connect the signal to a mass balance. If solution intensity alone is used to estimate adsorption, establish the response of free dye and labeled protein in the presence of the material. Check whether the material introduces absorption, scattering or fluorescence. Labeling ratio and removal of unbound dye belong to the same quantitative chain as the calibration curve.

An environmental probe deliberately uses a different chain. Suppose its lifetime responds to viscosity. First establish that response in controlled reference environments and examine the effects of temperature, polarity and binding. Inside a cell or hydrogel, the probe may occupy several environments, so a spatially averaged result combines those locations. Imaging, spectra and time-resolved detection can provide complementary information about the mixture. The selected probe, its localization and its calibration determine the physical meaning of the readout alongside the instrument's spatial or temporal resolution.

Multicolor experiments add spectral overlap. A detection channel may collect emission from more than one dye, and one excitation band may excite several components. Single-label controls measure how each component contributes to each channel; an unlabeled control reveals autofluorescence. If energy transfer between fluorophores is the subject, direct excitation, spectral bleed-through and donor-to-acceptor amounts must be considered separately. A shorter donor lifetime can help investigate energy transfer, while a dimmer donor channel and brighter acceptor channel alone still require controls connecting those changes to the proposed pathway.

A clear fluorescence result tells the reader what emits, how it is excited, which photons are collected, and whether the reported quantity represents amount, spectral shape or timing. Steady-state spectra emphasize absorption, emission and background. Lifetime measurements emphasize time response, photon counts and the decay model. Biological and materials applications add the behavior of the label and its surroundings. These connections make fluorescence rewarding: one optical experiment can reveal molecular organization, local environment or biological activity when the route from the physical object to the recorded signal is made explicit.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/S04.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Molecular Probes Handbook: Introduction to Fluorescence Techniques](https://www.thermofisher.com/us/en/home/references/molecular-probes-the-handbook/introduction-to-fluorescence-techniques.html)

   Quantum yield, spectra, photobleaching and inner-filter effects.
2. [Molecular Expressions: Introduction to Fluorescence](https://micro.magnet.fsu.edu/primer/techniques/fluorescence/fluorescenceintro.html)

   Stokes 1852 terminology, energy levels and lifetime.
3. [Ormö et al.: Crystal structure of GFP; PDB 1EMA](https://www.rcsb.org/structure/1EMA)

   1996 crystal structure, engineered sequence and chromophore environment.

   PDB archive coordinates CC0; entry paper DOI 10.1126/science.273.5280.1392.
4. [RCSB PDB: Data usage policies](https://www.rcsb.org/pages/policies)

   Terms for reuse of PDB coordinate data.

   PDB archive data CC0.
5. [NISTIR 7457: Recommendations and Guidelines for Standardization of Fluorescence Spectroscopy](https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir7457.pdf)

   Measurement framework for instrument, specimen and spectral correction.

   US government technical reference.
6. [Margineanu: Calibration approaches for fluorescence lifetime applications using time-domain measurements](https://pmc.ncbi.nlm.nih.gov/articles/PMC11969142/)

   Instrument response, reference dyes and time-domain photon counting.

   CC BY 4.0 article; no source figures reproduced.
