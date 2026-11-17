# Swelling: How water enters a polymer network

Source: https://ml-biomat.com/tutorials/experimental-methods/e01/en/
Language: en

Connect dry and wet masses, reference states, network connectivity and the hydrated conditions in which biomaterials are used.

## When a dressing absorbs water, more than its weight changes

Place a dry hydrogel in water and it may expand like a sponge. The resemblance is useful, but the internal processes deserve a closer look. In a sponge, much of the water occupies visible or microscopic pores. In many hydrogels, water also enters the spaces between polymer chains and changes how those chains are arranged. For a wound dressing, this affects fluid uptake. For a cartilage substitute, it changes dimensions and load-bearing behavior. For a cell-culture substrate, it can change the mechanical environment experienced by cells. A swelling experiment turns these changes into comparable records of mass, volume and time.

Imagine a fishing net made from interconnected rubber bands. Small water molecules can enter the net, while its junctions prevent every long chain from wandering away independently. The analogy separates absorption, swelling and dissolution. Absorption concerns liquid entering the material; swelling concerns the resulting increase in size; dissolution involves material dispersing into the surrounding liquid. A real gel can absorb water while also releasing unconnected chains or undergoing chemical degradation. A single final weighing therefore combines several possible events. A useful experiment follows the specimen from a clearly defined starting state and identifies which substances remain at the end.

The everyday expression “absorbs ten times its weight” illustrates why definitions matter. One person may divide wet mass by dry mass, another may divide absorbed water by dry mass, and a third may mean a volume increase. A specimen that starts with 0.10 g of dry polymer and reaches a wet mass of 1.00 g has a wet-to-dry mass ratio of ten, a water-to-dry mass ratio of nine, and a water mass fraction of 90%. All three numbers describe the same specimen. Reading the numerator and denominator is more informative than immediately ranking the reported numbers.

This chapter follows the specimen through its experiment: why the network takes up water, how balance readings become meaningful ratios, how immersion and drying should be organized, and what a time curve reveals. Reproducible constructed data support the calculations. A separate figure from an openly licensed research paper shows actual measurements, including finite sampling and differences between formulations. The aim is to connect an observation such as “this formulation swells more” to a particular reference state and environment, then decide what that change means for the intended application.

## Water enters while the network pulls back

Water molecules and polymer chains continually move through thermal motion. When the polymer is compatible with water, mixing offers many possible molecular arrangements, together with interactions such as hydrogen bonding. An analogy is people moving between connected rooms: opening additional accessible space changes how they distribute themselves. The more precise thermodynamic quantity is chemical potential, which describes the change in free energy when a small amount of a substance is added. A difference in the chemical potential of water between the inside and outside provides a driving force for exchange. Swelling approaches equilibrium as the relevant driving forces balance.

The network resists unlimited expansion. As connected chains stretch farther apart, they lose some of the coiled arrangements available to them, producing an elastic tendency to retract. Mixing favors expansion, while network elasticity opposes it. Junctions may be covalent bonds, ionic associations, hydrogen-bonded regions, crystallites or reversible protein interactions. Their stability depends on time and environment. An alginate network may change when competing ions alter its junctions; a physical gelatin network responds to temperature. Consequently, placing a gel “in water” is an incomplete experimental description: temperature and liquid composition participate in the experiment.

In 1943, Flory and Rehner developed a statistical-mechanical treatment combining solvent mixing with the elasticity of cross-linked networks, including systems such as vulcanized rubber. Its lasting contribution was to connect visible swelling to molecular connectivity. Modern hydrogels may also contain fixed charges, proteins, several junction types and strongly heterogeneous structures. The historical connection helps explain why a swelling result can inform network science, while the actual material determines which model is appropriate. Before converting swelling into a cross-link density, identify the network, the reference state and the assumptions used to represent its chains.

![Network schematic comparing free and substrate-constrained swelling. Blue circles represent water; the historical note connects mixing and elasticity in the 1943 theory.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/8d8ad6ed6a38d9570c8002ea.svg?v=8d8ad6ed6a38)

Figure 1Network schematic comparing free and substrate-constrained swelling. Blue circles represent water; the historical note connects mixing and elasticity in the 1943 theory.

Charged networks introduce another contribution. Charges fixed to polymer chains require mobile ions nearby to maintain electroneutrality. Ion distributions inside and outside can therefore differ and contribute to osmotic swelling. Adding salt often reduces this contribution in some ionic gels, but the response also depends on ion valence, specific binding and acid–base chemistry. Describing the effect as salt simply making water heavier misses the mechanism. The relevant changes concern ion distribution and network interactions. The same formulation may reach different equilibrium states in pure water, saline and culture medium, even when the initial specimen dimensions are identical.

Boundary conditions are equally important. A homogeneous, freely floating gel can expand in three directions. If its lower face adheres to glass, in-plane expansion is constrained and thickness and internal stress evolve differently. The network diagram illustrates how a similar tendency to absorb solvent produces different shapes under different restraints. This matters in cell experiments because culture gels are often attached to a substrate, whereas samples used for weighing may be free discs. Connecting their behavior requires carrying the boundary condition into the interpretation rather than treating attachment as a minor preparation detail.

## From balance readings to water content and volume

Start by giving each mass a precise meaning. Dry mass is the mass assigned to the dry network material. Wet mass is the mass after removing external liquid without squeezing liquid out of the specimen. Their difference represents retained liquid, provided unaccounted material loss and solute deposition have been addressed. Dividing wet mass by dry mass gives grams of wet specimen per gram of dry material. Subtracting one gives grams of absorbed liquid per gram of dry material. The gram units cancel, making the ratio dimensionless, although writing g/g can help readers remember its physical interpretation.

$$
Q_m=\frac{m_w}{m_d},\qquad q=\frac{m_w-m_d}{m_d}=Q_m-1,\qquad w_w=\frac{m_w-m_d}{m_w}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f827cd558a9b7c38c0686e49.svg) | Wet-to-dry mass ratio, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/9e9540cabe39a83b8900158e.svg) | Wet specimen mass after removing external liquid, g. |
| ![Formula](https://ml-biomat.com/static/agent-math/db3c43bdda65842442677c7c.svg) | Reference dry polymer mass, g. |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | Retained-liquid-to-dry mass ratio, dimensionless, often written g/g. |
| ![Formula](https://ml-biomat.com/static/agent-math/5e5b197dd107c875b96b8f1b.svg) | Water mass fraction in the wet specimen, dimensionless; multiply by 100 for percent. |

For 0.10 g dry mass and 1.00 g wet mass, Qm=10, q=9 and ww=0.90. The mass difference represents liquid when dry composition and material loss are included in the mass accounting.

The water mass fraction uses wet mass as its denominator and lies between zero and one. For 0.10 g dry polymer and 1.00 g wet specimen, nine tenths of the wet mass is water. Reporting 900% instead describes water relative to dry polymer, rather than the fraction of the wet specimen occupied by water mass. Confusion often starts when a table heading such as “swelling percentage” is copied without its definition. Keeping the original dry and wet masses allows the same dataset to be recalculated under another clearly stated convention, rather than leaving only an ambiguous percentage.

Density provides the bridge from mass to volume. Density means mass per unit volume, so dividing mass by density gives volume. If dry polymer is denser than water, equal masses of polymer and water occupy different volumes. The wet-to-dry volume ratio can consequently exceed the wet-to-dry mass ratio. The following conversion assumes approximately additive polymer and solvent volumes, dry mass corresponding to polymer, and densities appropriate to the composition and temperature. Materials containing substantial inorganic filler, closed pores or pronounced mixing contraction require additional components in this accounting. Those components have their own volumes and should be represented explicitly.

$$
Q_V=\frac{m_d/\rho_p+(m_w-m_d)/\rho_s}{m_d/\rho_p}=1+\frac{\rho_p}{\rho_s}(Q_m-1),\qquad \phi_p=\frac{1}{Q_V}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0c8e72b6b5d491a201d0a4d9.svg) | Wet-volume-to-dry-polymer-volume ratio, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/db3c43bdda65842442677c7c.svg) | Dry polymer mass, g. |
| ![Formula](https://ml-biomat.com/static/agent-math/9e9540cabe39a83b8900158e.svg) | Wet specimen mass, g. |
| ![Formula](https://ml-biomat.com/static/agent-math/e04e40ff4b2959cf46147e6c.svg) | Dry polymer density, g/cm³. |
| ![Formula](https://ml-biomat.com/static/agent-math/72df456d8963cb97ca755642.svg) | Solvent density, g/cm³. |
| ![Formula](https://ml-biomat.com/static/agent-math/f827cd558a9b7c38c0686e49.svg) | Wet-to-dry mass ratio, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/68346d656e91e3fc34903833.svg) | Polymer volume fraction in the wet specimen, dimensionless. |

Mass divided by density gives volume, and the component volumes are added under the volume-additivity approximation. Qm=10, ρp=1.2 g/cm³ and ρs=1.0 g/cm³ give QV=11.8 and φp≈0.08475.

![Composition and three ratios for one teaching specimen: 0.10 g dry polymer and 0.90 g internal water. The volume ratio uses the stated densities.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/8410d0ed19f4ef9651e5d5fb.svg?v=8410d0ed19f4)

Figure 2Composition and three ratios for one teaching specimen: 0.10 g dry polymer and 0.90 g internal water. The volume ratio uses the stated densities.

With polymer density 1.2 g/cm³ and water density 1.0 g/cm³, the example contains about 0.0833 cm³ of dry polymer and 0.900 cm³ of water. Their total is about 0.9833 cm³. Dividing by the dry polymer volume gives a volume ratio of 11.8 and a polymer volume fraction of approximately 0.08475. This volume fraction differs from the polymer mass fraction of 0.10. Models concerned with chain spacing, transport and network structure often require volume fraction. Inserting mass fraction in its place changes the physical meaning even though both numbers are dimensionless.

For homogeneous, freely swelling material that expands equally in every direction, the linear stretch is the cube root of the volume ratio. Length, width and height each acquire the same factor, and multiplying the three factors gives the change in volume. A volume ratio of 11.8 therefore corresponds to a linear factor of about 2.277 relative to the dry state. Many gels already contain abundant water when prepared. Their preparation-to-equilibrium stretch instead uses the volume ratio between those two hydrated states. A substrate-attached layer generally requires separate thickness and in-plane measurements because its directional stretches differ.

$$
\lambda=\left(\frac{V}{V_0}\right)^{1/3},\qquad \lambda_{\mathrm{dry}}=Q_V^{1/3}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/98a445be63a324ba80515c96.svg) | Isotropic linear stretch relative to the chosen reference state, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | Current volume, cm³. |
| ![Formula](https://ml-biomat.com/static/agent-math/454606841ec20ef0f43cd9f6.svg) | Reference-state volume, cm³. |
| ![Formula](https://ml-biomat.com/static/agent-math/2b72c1ebdf16f54dc902b630.svg) | Isotropic stretch relative to the dry state, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/0c8e72b6b5d491a201d0a4d9.svg) | Wet-to-dry-polymer volume ratio, dimensionless. |

During isotropic free swelling, three linear factors multiply to λ³. QV=11.8 gives λ≈2.277 relative to the dry state; substrate constraints require directional treatment.

## Make immersion and weighing a connected measurement

Define the comparison before choosing the procedure. A dressing study may emphasize uptake within a specified time and retention under compression. A culture-substrate study should consider culture temperature, medium and attachment. A network study needs either prior extraction of soluble material or a parallel measurement of what is lost. Once the question is clear, specimen dimensions, bath volume, sampling times and reference mass have a shared purpose. The resulting measures need not be collapsed into one universal ranking of swelling performance: a high equilibrium uptake and a fast response may benefit different applications.

Give every independent specimen an identifier and its own dry mass. Thickness affects the distance over which water must travel, while edge damage can accelerate entry or release fragments. Record thickness and diameter along with mass. Specimens need not have perfectly identical dry masses, but normalize each one before calculating the group mean. Adding all wet masses and dividing by the sum of all dry masses produces a dry-mass-weighted ratio; it answers a different statistical question from the ordinary mean of individual ratios. The example retains each trajectory so that an unusual result can be traced to its specimen.

The immersion bath should maintain the intended environment. A gel may release salts, acids, residual monomer or soluble polymer. In a small bath, those substances can alter external composition and feed back into swelling. A cover reduces evaporation, and temperature control stabilizes both equilibrium and transport. Record the volume and timing of medium changes when they are used; retaining the same bath is also a design choice worth specifying. For ion-sensitive or pH-sensitive networks, measuring pH or conductivity before and after immersion can explain a mass trend that otherwise appears inconsistent with the formulation.

A drop clinging to the surface is different from liquid retained within the network. Gentle contact with absorbent paper, a fixed draining interval or another evaluated method can remove external liquid, but the contact pattern and duration should remain consistent. Strong pressure can expel internal water, while a long delay allows evaporation. Comparing repeated handling of representative specimens helps identify a reproducible procedure. Record the empty weighing container as well. If the specimen remains on glass during weighing, subtract the support and account for liquid retained on exposed portions of the support rather than assigning it to the gel.

Drying determines what the denominator contains. Oven drying, vacuum drying and freeze-drying impose different temperature and structural histories. Choose a procedure compatible with material stability and check mass stability through successive weighings. Buffer salts and other nonvolatile solutes can remain after the water disappears. When polymer dry mass is required, options include controlled desalting, blank measurements of residual solids or independent compositional analysis, while checking whether the treatment also removes network material. “Constant dry mass” and “pure polymer mass” describe different conditions. Recognizing that distinction prevents a reproducible weighing procedure from producing a systematically misleading denominator.

## Rate, equilibrium and thickness tell different stories

The time schedule must also account for handling. Removing, blotting, weighing and returning several specimens can spread their actual observation times over minutes. That difference matters for a rapidly absorbing thin film. Staggering immersion starts, recording individual timestamps or assigning separate specimens to each time point can make the comparison clearer. Separate specimens avoid repeated handling effects, while following the same specimen preserves its complete individual trajectory. These designs answer related but different questions. Choose the arrangement before beginning and preserve actual elapsed time, rather than replacing it with an ideal schedule after measurement.

A familiar swelling curve rises rapidly and then approaches a plateau. Initially, the inside and outside differ strongly, and the surface encounters the liquid first. As water enters, transport distances and driving forces change. A plateau means that mass changes become small over the chosen observation interval and measurement precision. Define an operational equilibrium criterion using successive measurements, a relative-change threshold and a time interval. Simply immersing every material for one day does not establish the same state. Ongoing degradation or extraction may keep the curve evolving; dry mass and specimen appearance then help interpret the wet-mass record.

The code uses a single-exponential approach to equilibrium to separate two readily understood features: how much uptake is eventually reached and how quickly it is approached. The constructed curve begins at mass ratio three, approaches ten and has a time parameter of 45 minutes. One time parameter corresponds to about 63.2% of the total change, rather than complete equilibration. Three time parameters correspond to approximately 95%. The expression is a useful description of a curve dominated by one apparent timescale and an empirical basis for comparisons. Its fitted time parameter acquires a transport interpretation only after the appropriate physical model is established.

$$
Q_m(t)=Q_0+(Q_\infty-Q_0)\left(1-e^{-t/\tau}\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/38da52f1cae2f9d507f1a8ad.svg) | Model wet-to-dry mass ratio at time t, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/60aeca77be2527e34462d75b.svg) | Initial mass ratio, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/dc1bd1301b77fa0c9082a354.svg) | Long-time model mass ratio, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Elapsed time, min. |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | Single-exponential time parameter, min. |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | Base of the natural exponential, approximately 2.71828, dimensionless. |

This empirical model makes the remaining change decay at a constant relative rate. For Q0=3, Q∞=10 and τ=45 min, the ratio at 45 min is approximately 7.42484, corresponding to 63.212% of the total change.

![Constructed records connect raw wet masses, individual normalization, fitting and residuals. Error bars are between-specimen SD. The lower-right panel changes the model timescale to illustrate thickness-squared scaling.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/6d71f4866a0dcab1e41b18f2.svg?v=6d71f4866a0d)

Figure 3Constructed records connect raw wet masses, individual normalization, fitting and residuals. Error bars are between-specimen SD. The lower-right panel changes the model timescale to illustrate thickness-squared scaling.

The first panel shows raw wet masses for three specimens. The next panel shows the mean after individual normalization, with standard deviations between specimens. Those bars describe the dispersion of three independent specimen ratios at a given time, rather than the balance specification or three copies of one reading. The fit uses the mean ratio at each time, while the residual panel plots observed minus fitted values. A pattern with early observations mostly above the line and late observations mostly below it suggests that one timescale is combining distinct processes. Sampling around the changing curvature can help identify what the model misses.

A thickness comparison is especially useful for investigating transport. For diffusion-controlled or certain poroelastic processes, characteristic time scales with the square of a characteristic distance when geometry, boundary conditions and effective transport properties remain comparable. Molecules repeatedly change direction through thermal motion, so reaching twice the distance requires a longer exploration rather than twice the straight-line travel time. The illustrated model assigns 45 minutes to a 1 mm specimen and 180 minutes to a 2 mm specimen. This scaling guides a sampling schedule and suggests a testable hypothesis about the process controlling the response.

$$
\tau\propto\frac{L^2}{D},\qquad \frac{\tau_2}{\tau_1}=\left(\frac{L_2}{L_1}\right)^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7a8cd924f632d8dad8901100.svg) | Characteristic time and the times for two geometrically similar specimens, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/8e40a7acd8098e65ecb98265.svg) | Transport distance and its values for the two specimens, m. |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | Effective transport coefficient, m²/s. |
| ![Formula](https://ml-biomat.com/static/agent-math/d9c6c40f15e6a090e4bcafe4.svg) | Means proportional to; the geometry factor depends on boundary conditions. |

Under diffusion or corresponding poroelastic scaling with comparable geometry, boundaries and D, doubling distance increases time fourfold. The teaching curves use 45 and 180 min for 1 and 2 mm specimens; this scaling alone does not determine D.

A dense surface layer, directional structure or slow network relaxation can change the thickness dependence. A film exposed on both faces also differs from a film sealed against glass on one face. Estimating a diffusion coefficient from a fitted time requires a solution appropriate to the geometry, boundaries and coupled mechanics. Here the square scaling explains a trend; the separate diffusion and permeation chapter develops direct transport measurements. Keeping these tasks distinct is productive: an empirical fit summarizes the observed shape, while a mechanistic model connects that shape to internal material properties through explicit assumptions.

## Expose measurement bias, then examine published data

The last displayed digit of a balance matters in relation to specimen size. A 1 mg mass error has a different relative effect on 10 mg and 100 mg dry specimens. Checking balance performance, limiting drafts and static electricity, and reducing exposure to air help stabilize readings. Additional independent specimens reveal variation in the material itself. Measuring handling repeatability separately from between-specimen variation identifies where an improvement is needed: in the weighing procedure, in environmental control, or in the consistency of material preparation. More repeated readings of one specimen cannot substitute for independent specimens when estimating material variability.

A small mass bias can produce a noticeable ratio error. For a specimen containing 0.10 g dry polymer, an extra 20 mg of external liquid changes a true wet-to-dry mass ratio of ten to 10.2. If the wet mass is still 1.00 g but the dried residue contains 10 mg of extra salt, dividing by that inflated denominator gives about 9.09. The two effects act in opposite directions and can even compensate. An apparently plausible number therefore does not identify a correct procedure. The artifact figure varies surface liquid and salt separately, making their respective effects visible.

![Constructed weighing biases: external liquid increases wet mass, while residual salt increases dry mass. Each panel changes one bias; dashed lines show the unbiased ratio of ten.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/01553b5deb7f89a78a16de02.svg?v=01553b5deb7f)

Figure 4Constructed weighing biases: external liquid increases wet mass, while residual salt increases dry mass. Each panel changes one bias; dashed lines show the unbiased ratio of ten.

The interactive experiment keeps the underlying specimen fixed at 0.10 g polymer and 0.90 g internal water. You change external liquid left during wet weighing and salt remaining during dry weighing. The network's actual hydration stays constant while its calculated ratio changes. Try finding a combination where the two biases nearly cancel and the display returns to ten, then set either bias to zero. This demonstrates why a target-looking number is less useful than measurements tied to known substances. Blank controls, consistent liquid removal and compositional checks assign a clear interpretation to each balance reading.

## Change weighing bias for the same gel

The specimen always contains 0.10 g polymer and 0.90 g internal water. Change external liquid and dry salt residue to compare apparent and true mass ratios.

[Figure: True and apparent mass ratios](https://ml-biomat.com/tutorials/experimental-methods/e01/en/#E01-plot)

Published experiments add another layer of interpretation. Subramani and colleagues studied substrate-attached polyacrylamide gels, following swelling over time alongside mechanical changes. The reproduced figure preserves the original axes, measurements and error bars. Different formulations show different time responses: some change appreciably over earlier intervals while others remain more stable. The vertical axis represents the paper's volumetric swelling ratio, derived from wet and dry masses and densities. It should therefore be read as a volume ratio rather than a water mass percentage. The bilingual caption explains its role while retaining the original scientific figure.

![Published experimental Figure 4 from Subramani et al. (2020), Frontiers in Materials, DOI 10.3389/fmats.2020.00212, CC BY 4.0. A spans longer times and B shorter times; the vertical axis is the paper’s volumetric swelling ratio and error bars are SD. Scientific content is unchanged; an outer bilingual title and credit are added. Original labels remain in English.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/82a59faa93d2c82e071be117.svg?v=82a59faa93d2)

Figure 5Published experimental Figure 4 from Subramani et al. (2020), Frontiers in Materials, DOI 10.3389/fmats.2020.00212, CC BY 4.0. A spans longer times and B shorter times; the vertical axis is the paper’s volumetric swelling ratio and error bars are SD. Scientific content is unchanged; an outer bilingual title and credit are added. Original labels remain in English.

Read this published figure in the same sequence as the constructed example. First inspect the time span, then the vertical-axis definition and reference state, then the independent specimens behind each point. Only after those checks should you compare formulations. Overlapping error bars are not a complete statistical test, and nonoverlap alone does not explain a mechanism. For a cell-culture application, the useful next comparison links swelling to mechanical measurements made at corresponding states. The dimensions and stiffness relevant to cells are those present during culture, which may differ from the values measured immediately after preparing the gel.

## Turn a mass record into a result that supports the next experiment

Another distinction concerns structural scale. The mesh size in a network model describes a statistical spacing associated with chains and junctions. Large pores in a dried micrograph can also reflect freezing, phase separation or specimen preparation. The two observations can be studied together, but their names do not establish equivalence. To understand whether a protein can move through a hydrated network, combine swelling with tracer diffusion, adsorption and molecular-size information. Those measurements address the environment experienced by the moving molecule more directly than enlarging a photograph of pores after the water has been removed.

The complete program preserves the intermediate steps between weighing and interpretation. It assigns separate dry masses to three specimens, generates a fixed teaching time series with small weighing fluctuations, and calculates individual wet-to-dry ratios before the group mean and standard deviation. It then fits the equilibrium ratio and time parameter. The exported table contains raw wet masses, mean ratios, standard deviations and fitted values, allowing another reader to reconstruct a figure or change the fitting interval. A fixed random seed makes repeated execution reproduce the same teaching records, so hand calculations can be compared directly with the saved output.

### Complete Python: Swelling mass accounting, fitting and bias diagnostics

Execution exports raw masses, normalized results, fit parameters and all five figures. The published image and license notice are bundled; execution requires no network.

```
"""Mass/volume swelling and a constructed time series; includes a licensed published figure."""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle,FancyArrowPatch

def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def uptake(t,initial,equilibrium,time_scale):
    return initial+(equilibrium-initial)*(1-np.exp(-np.asarray(t)/time_scale))

def ratios(dry,wet,rho_polymer=1.2,rho_water=1.):
    mass=wet/dry
    volume=1+rho_polymer/rho_water*(mass-1)
    return {'mass_ratio':mass,'water_per_dry':mass-1,'water_fraction':1-1/mass,
            'volume_ratio':volume,'polymer_volume_fraction':1/volume,'isotropic_stretch':volume**(1/3)}

def main(output,language):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    from matplotlib import font_manager
    fonts={x.name for x in font_manager.fontManager.ttflist};font=next((f for f in ['Microsoft YaHei','Noto Sans CJK SC','SimHei'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[font,'DejaVu Sans'] if language=='zh' else ['DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','axes.prop_cycle':plt.cycler(color=['#186e83','#cd803f','#8160a1','#3c8a6a'])})
    tr=lambda z,e:z if language=='zh' else _label(e)
    def save(fig,name):
        fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    result=ratios(.1,1.)
    rng=np.random.default_rng(101)
    times=np.array([0,5,10,20,30,45,60,90,120,180,240.])
    dry=np.array([.098,.102,.100]);truth=uptake(times,3,10,45)
    wet=dry[:,None]*truth+rng.normal(0,.003,(3,len(times)))
    observed=wet/dry[:,None];mean=observed.mean(0);sd=observed.std(0,ddof=1)
    fit,cov=curve_fit(lambda t,qinf,tau:uptake(t,3,qinf,tau),times,mean,p0=[9,40],bounds=([3,1],[20,1000]))
    prediction=uptake(times,3,*fit);smooth=np.linspace(0,240,400)
    np.savetxt(output/'swelling.csv',np.column_stack([times,*wet,mean,sd,prediction]),delimiter=',',header='time_min,wet_g_1,wet_g_2,wet_g_3,mean_mass_ratio,sd_mass_ratio,fitted_ratio',comments='')
    np.savetxt(output/'dry_masses.csv',dry,delimiter=',',header='dry_mass_g',comments='')
    fig,ax=plt.subplots(1,3,figsize=(12,4.4));nodes=np.array([[0,0],[1,0],[2,0],[0,1],[1,1],[2,1],[0,2],[1,2],[2,2]],float)
    for k,stretch in enumerate([1,1.65,1.65]):
        a=ax[k];a.set_aspect('equal');a.axis('off');coords=nodes*stretch
        if k==2:coords[:,0]=nodes[:,0]
        for i,j in [(0,1),(1,2),(3,4),(4,5),(6,7),(7,8),(0,3),(3,6),(1,4),(4,7),(2,5),(5,8)]:
            a.plot(coords[[i,j],0],coords[[i,j],1],color='#186e83',lw=3)
        a.scatter(*coords.T,s=35,color='#cd803f',zorder=3)
        for x,y in [(0.5,.5),(1.5,.5),(.5,1.5),(1.5,1.5)]:a.add_patch(Circle((x*(stretch if k<2 else 1),y*stretch),.12,color='#a2cdd9'))
        if k==2:a.plot([-.3,2.3],[-.15,-.15],color='#707c82',lw=7)
        a.set(xlim=(-.5,3.8),ylim=(-.6,3.8));a.set_title(tr(['A  制备时的网络','B  自由溶胀','C  底面固定'][k],['A  As-prepared network','B  Free swelling','C  Substrate constraint'][k]),loc='left')
    fig.text(.5,.01,tr('1943：Flory 与 Rehner 将溶剂混合与网络弹性放进同一理论。','1943: Flory and Rehner joined solvent mixing with network elasticity.'),ha='center');save(fig,'network')
    fig,ax=plt.subplots(1,2,figsize=(11,4.5));ax[0].bar(tr(['干聚合物','水'],['Dry polymer','Water']),[.1,.9],color=['#cd803f','#186e83']);ax[0].set(ylabel=tr('质量 / g','Mass / g'),title=tr('A  湿样品 1.00 g 的组成','A  Composition of a 1.00 g wet specimen'))
    labels=tr(['湿 / 干质量','吸水 / 干质量','湿 / 干体积'],['Wet / dry mass','Water / dry mass','Wet / dry volume']);ax[1].barh(labels,[10,9,11.8],color=['#186e83','#3c8a6a','#8160a1']);ax[1].set(xlabel=tr('比值 / 无量纲','Ratio / dimensionless'),title=tr('B  三个分母明确的量','B  Three explicitly defined ratios'),xlim=(0,14))
    for i,v in enumerate([10,9,11.8]):ax[1].text(v+.15,i,f'{v:g}',va='center')
    fig.tight_layout();save(fig,'ratios')
    fig,ax=plt.subplots(2,2,figsize=(11,7.3));ax=ax.ravel()
    for i in range(3):ax[0].plot(times,wet[i],'.-',alpha=.7,label=f'{i+1}: {dry[i]:.3f} g')
    ax[0].set(title=tr('A  三份样品的原始湿质量','A  Raw wet masses of three specimens'),ylabel=tr('湿质量 / g','Wet mass / g'));ax[0].legend(fontsize=9)
    ax[1].errorbar(times,mean,yerr=sd,fmt='o',ms=4,label=tr('均值 ± 样品间 SD','Mean ± between-specimen SD'));ax[1].plot(smooth,uptake(smooth,3,*fit),label=tr('单指数拟合','Single-exponential fit'));ax[1].set(title=tr('B  先逐样品归一化，再汇总','B  Normalize each specimen before averaging'),ylabel=tr('湿 / 干质量比','Wet / dry mass ratio'));ax[1].legend(fontsize=9)
    ax[2].axhline(0,color='#707c82',lw=.8);ax[2].plot(times,mean-prediction,'o-');ax[2].set(title=tr('C  残差检查','C  Residual inspection'),ylabel=tr('观测值 − 拟合值','Observed − fitted'))
    for h in [.5,1,2]:ax[3].plot(smooth,uptake(smooth,3,10,45*h*h),label=f'{h:g} mm')
    ax[3].set(title=tr('D  固定几何假设下的厚度效应','D  Thickness effect under fixed geometry'),ylabel=tr('模型质量比','Model mass ratio'));ax[3].legend()
    for a in ax:a.set_xlabel(tr('时间 / min','Time / min'))
    fig.tight_layout();save(fig,'kinetics')
    fig,ax=plt.subplots(1,2,figsize=(11,4.5));film=np.linspace(0,.05,100);salt=np.linspace(0,.02,100)
    ax[0].plot(film*1000,(1+film)/.1);ax[0].set(xlabel=tr('残留表面液体 / mg','Residual surface liquid / mg'),ylabel=tr('计算质量比','Calculated mass ratio'),title=tr('A  表面液体抬高分子','A  Surface liquid raises the numerator'))
    ax[1].plot(salt*1000,1/(.1+salt),color='#cd803f');ax[1].set(xlabel=tr('干燥后残留盐 / mg','Salt remaining after drying / mg'),ylabel=tr('计算质量比','Calculated mass ratio'),title=tr('B  残留盐抬高分母','B  Residual salt raises the denominator'))
    for a in ax:a.axhline(10,color='#707c82',ls='--');a.grid(alpha=.15)
    fig.tight_layout();save(fig,'artifacts')
    from PIL import Image
    published=np.asarray(Image.open(Path(__file__).with_name('subramani2020-figure4.webp')))
    fig,ax=plt.subplots(figsize=(11,4.8));ax.imshow(published);ax.axis('off');ax.set_title(tr('真实实验：固定在基底上的凝胶随时间溶胀','Published measurements: swelling of substrate-attached gels'),pad=14)
    fig.text(.5,.015,'Subramani et al. (2020), Figure 4 · Frontiers in Materials · CC BY 4.0',ha='center',fontsize=9);save(fig,'published')
    summary={'worked_example':result,'fit':{'equilibrium_mass_ratio':float(fit[0]),'time_scale_min':float(fit[1])},'checks':{'initial_ratio':float(uptake(0,3,10,45)),'one_time_scale_fraction':float((uptake(45,3,10,45)-3)/7),'fourfold_time_scale_at_double_thickness':4.,'surface_20mg_ratio':10.2,'salt_10mg_ratio':1/.11}}
    assert abs(result['volume_ratio']-11.8)<1e-12
    assert abs(result['water_fraction']-.9)<1e-12
    assert abs(summary['checks']['one_time_scale_fraction']-(1-np.exp(-1)))<1e-12
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--language',choices=['zh','en'],default='zh');args=parser.parse_args();main(args.output,args.language)
```

Begin with three values that can be checked without fitting: mass ratio ten, water mass fraction 0.90 and volume ratio 11.8 for the specified densities. Next inspect whether the fitted parameters are close to the values used to construct the example. Try removing the latest observations and refitting. When only the early rising section is recorded, equilibrium uptake and the time parameter can compensate for one another, making the plateau less firmly determined. Earlier observations help resolve fast changes; longer observation helps locate the plateau. These are different improvements because they supply different information to the experiment.

A useful report is organized around a specific application. For two dressings, show independent uptake trajectories, uptake at a relevant time, the eventual state and liquid retention under compression. For culture substrates, connect attachment, medium, dimensional change and mechanical state. Define mass or volume ratios in the figure caption and retain the underlying dry and wet masses with specimen identifiers. Describe how the measured change affects material selection. This connects a graph to an experimental decision rather than ending with a single large absorption number that cannot be compared across preparation histories or environmental conditions.

Swelling leads naturally to the next experiment. If a material loses dry mass during immersion, some polymer may have remained outside the connected network and been extracted, or the network itself may have changed. Gel-fraction measurements shift attention from retained water to the dry material remaining after a defined extraction. The two experiments complement one another: first establish how much network remains, then determine how much liquid that network absorbs. Together they clarify the relationships among cross-linking, dissolution and degradation and establish a mass basis for later release and transport measurements.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/E01.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Subramani et al. (2020). The Influence of Swelling on Elastic Properties of Polyacrylamide Hydrogels](https://www.frontiersin.org/journals/materials/articles/10.3389/fmats.2020.00212/full)

   Volume conversion, substrate constraints and measured swelling; Figure 4 reproduced under its license.

   CC BY 4.0; Figure 4 credited in caption and bundled notice.
2. [Flory and Rehner (1943). Statistical Mechanics of Cross-Linked Polymer Networks II. Swelling](https://doi.org/10.1063/1.1723792)

   Historical original paper connecting mixing and network elasticity.
3. [Sheth et al. Measurement of Hydrogel Swelling Ratio and Mesh Size](https://bio-protocol.org/exchange/minidetail?id=4024598&type=30)

   Distinguishes as-prepared, swollen and dry states, including ongoing degradation.

   CC BY as stated for the extracted research method; no figure reused.
4. [Sheth et al. (2019). Predicting Drug Release From Degradable Hydrogels Using Fluorescence Correlation Spectroscopy and Mathematical Modeling](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2019.00410/full)

   Connects swelling to molecular transport and degradation.
5. [SciPy: curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

   Bounded nonlinear fitting and parameter interpretation.
