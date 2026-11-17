# Creep testing: Slow deformation under a constant load

Source: https://ml-biomat.com/tutorials/experimental-methods/m06/en/
Language: en

Follow a slowly sinking cushion into compliance, delayed recovery and viscous flow, then test a material model against a complete loading–unloading record.

## Why a soft material keeps changing under the same load

Place a heavy book on a soft cushion. The cushion sinks immediately, and may continue to become thinner while the book stays in place. The book has not become heavier, so what is still changing? The same question matters for load-bearing hydrogels, adhesive joints, polymer pipes and tissue scaffolds. A material that has an appropriate shape immediately after loading may have a different shape several hours later. A creep experiment turns this everyday observation into a defined measurement: at a stated temperature, hydration condition and approximately constant stress, how does deformation develop with time? The useful answer separates immediate softness, the rate of subsequent change and the amount of recovery after unloading.

The word constant deserves attention. Hanging a weight usually keeps the force constant. Stress also depends on the area carrying that force. In a small-deformation tensile experiment, engineering stress uses the initial cross-sectional area, so constant force produces constant engineering stress. If the specimen becomes appreciably thinner, the true stress acting on its current area increases. The experiment then differs from one performed at constant true stress. Compression introduces related changes in area, barreling and friction at the loading plates. Beginning within an experimentally established linear range helps separate time dependence from changes in geometry. Larger deformations can then be investigated with the appropriate mechanical description.

A different experiment holds the cushion at a fixed compressed thickness and follows the gradual decrease in supporting force. That is stress relaxation: deformation is controlled and force is observed. Creep controls stress and observes deformation. The two experiments ask different questions of the same material and provide complementary information, but taking the reciprocal of every point on one curve does not generally produce the other curve. Identifying what the instrument actually controls is therefore the first step in reading a viscoelastic measurement. This chapter uses tensile quantities. Shear creep follows the same reasoning with shear stress, shear strain and shear compliance, while retaining the correct geometry throughout the calculation.

![The measurement chain and spring–dashpot language of constant-force creep. The left panel identifies force control, gauge length and the load cell; the right combines immediate elasticity, delayed recovery and flow. The historical line connects the response models with the development of rheology. Original conceptual illustration.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/78e2ccda79d8218c67cdf42d.svg?v=78e2ccda79d8)

Figure 1The measurement chain and spring–dashpot language of constant-force creep. The left panel identifies force control, gauge length and the load cell; the right combines immediate elasticity, delayed recovery and flow. The historical line connects the response models with the development of rheology. Original conceptual illustration.

## Springs, dashpots and the time a material needs

An ideal spring extends immediately when a force is applied and returns when that force is removed. A piston moving through a viscous liquid takes time to travel and keeps moving under a sustained force. Drawn together, these elements provide a language for materials with time-dependent responses. Nineteenth-century developments in elasticity and viscous mechanics supported the later Maxwell and Kelvin families of models. By the founding of the Society of Rheology in 1929, phenomena observed in rubber, asphalt, paint and biological materials were increasingly discussed within a shared field. The mechanical elements in the illustration represent response laws; they do not imply that a polymer contains miniature metal springs and hydraulic cylinders.

Real polymers offer several reasons for delayed motion. Chain segments rotate, contacts between chains rearrange, and reversible junctions open and close. Hydrogels add another route: water redistributes through the network or leaves the specimen. Imagine several people pulling a flexible net. The cords tighten quickly, but the people need time to rearrange their positions; water trapped in the net adds a further delay as it moves. The analogy helps distinguish processes that occur on different timescales. Determining which process dominates a particular experiment requires information about specimen dimensions, temperature, solvent conditions and complementary measurements. The creep curve first describes a macroscopic response over the time window actually observed.

A simple delayed-recovery element places a spring and dashpot in parallel, so they undergo the same extension. At the beginning of loading, the dashpot resists rapid motion. As it moves, the spring carries an increasing share of the load and the extension approaches a limit. Connecting this element in series with another spring adds an immediate elastic response. Adding a further dashpot in series allows sustained flow. Series elements carry the same stress, and their deformations add. This mechanical arrangement explains why the compliance expression later in the chapter contains a sum of three contributions: each term represents a distinct part of the total extension.

Some materials require several delayed elements because local segments, entanglements and junctions rearrange at different rates. Before introducing more elements, ask whether the recorded experiment can distinguish them. A one-minute observation gives little information about two processes that both need hours to develop. Likewise, an instrument that takes five seconds to reach the target force provides little direct information about a response lasting a tenth of a second. The time window and signal quality should support the complexity of the model. Understanding one delayed element first makes a distribution of retardation times much easier to interpret than starting with a long list of fitted parameters.

## From force and length to a comparable compliance

A creep instrument or a mechanical tester operating in force control records load, displacement and time. The initial length determines how much strain corresponds to a given extension. The initial cross-sectional area determines how widely a force is distributed. Geometry must therefore enter the calculation before different specimens can be compared. Consider a specimen with an initial gauge length of 20 mm and a cross-sectional area of 10 mm². A tensile force of 0.005 N produces an engineering stress of 500 Pa. An extension of 0.40 mm corresponds to a strain of 0.020, or 2%. Converting the area to 0.000010 m² is essential: the squared unit is an easy place to lose a factor during hand calculations.

$$
\sigma_0=\frac{F}{A_0},\qquad \varepsilon(t)=\frac{L(t)-L_0}{L_0},\qquad J(t)=\frac{\varepsilon(t)}{\sigma_0}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/465ea137606b4c7e2067f528.svg) | Constant engineering stress in Pa; subscript 0 identifies the imposed level. |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | Tensile force in N. |
| ![Formula](https://ml-biomat.com/static/agent-math/0c430ee48d22be2e69d0f3ad.svg) | Initial cross-sectional area in m². |
| ![Formula](https://ml-biomat.com/static/agent-math/dd72237021aa073cc29bdada.svg) | Engineering strain at time t, dimensionless; multiply by 100 to display percent. |
| ![Formula](https://ml-biomat.com/static/agent-math/4310de27232c5927c847a9aa.svg) | Gauge length at time t in m. |
| ![Formula](https://ml-biomat.com/static/agent-math/973a201db437d1c712202461.svg) | Initial gauge length in m. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Elapsed time since loading in s. |
| ![Formula](https://ml-biomat.com/static/agent-math/78711ccf7196ae9599387d2a.svg) | Creep compliance within the linear regime in Pa⁻¹. |

Force divided by area gives force per area; extension divided by initial length gives relative extension. 0.005 N / 0.000010 m² = 500 Pa; 0.40 mm / 20 mm = 0.020; compliance is therefore 0.020 / 500 = 0.000040 Pa⁻¹.

Compliance means the amount of strain produced by a unit of stress. Suppose two specimens experience the same stress of 500 Pa. At 60 seconds, their strains are 0.02 and 0.04. Their compliances at that time are respectively 0.000040 Pa⁻¹ and 0.000080 Pa⁻¹, so the second specimen deforms more readily. Although compliance has the reciprocal units of a modulus, a creep compliance is not generally the point-by-point reciprocal of a relaxation modulus. The two measurements impose different histories. A simple reciprocal relation applies directly in special cases such as a purely elastic material. Keeping the loading history attached to the quantity prevents a unit-based shortcut from becoming a physical mistake.

Distinguish percent from percentage points when reading the axes. A strain increasing from 1% to 2% increases by one percentage point and by 100% relative to its initial value. The residual plot uses percentage points to show the vertical distance between observations and predictions. Compliance calculations always use dimensionless strains such as 0.01 and 0.02. Maintaining this distinction across tables, equations and captions prevents a one-percent deformation from being entered as a full unit of extension. This simple check is particularly useful when studying small deformations in soft specimens.

The linear range can be assessed with a practical comparison. Under otherwise matching environmental and waiting conditions, measure several small stress levels and divide each strain curve by its applied stress. If the resulting compliance curves coincide within experimental variation, the assumption that doubling stress doubles strain is supported over that range. A systematic stress dependence can arise from nonlinear rearrangement, but also from grip slip, changing contact or damage. Higher stress produces a larger signal and may improve resolution, while also increasing the chance of changing the structure being measured. Selecting a load is consequently a reasoned balance between signal quality and the mechanical regime relevant to the question.

Specimen preparation also enters the numerical result. For a hydrogel, identify the equilibration liquid, temperature, soaking history and whether the measurement is performed under immersion. Surface drying can otherwise add a concentration change to the long-time response. For a film, record cutting direction and thickness variation because orientation and thickness errors affect the inferred stress. Measure dimensions at several positions. Displacement between grips may include deformation of the machine frame, so direct measurement within the specimen gauge length is valuable when available. A rigid reference specimen helps estimate system compliance and distinguish the instrument contribution from the initial movement of the material.

A reproducible starting condition is equally important. A newly mounted specimen may contain slack, incomplete contact or prestrain introduced by the grips. The instrument's displayed zero is not automatically the material's unloaded state. A documented small preload can establish contact, followed by a stated waiting period until displacement changes more slowly. Save force and displacement together when applying the target load. The force record reveals rise time, overshoot and stability, helping distinguish a material response from a controller approaching its target. If the preload already produces appreciable creep, include that earlier loading history in the analysis rather than redefining it away.

## Separating immediate deformation, delayed deformation and flow

A three-contribution linear model connects these ideas to an entire experiment. Its first term appears immediately upon loading. Its second term grows gradually toward a limit. Its third term increases at a constant rate for as long as the stress is maintained. The exponential can be understood as the fraction of an adjustment that remains unfinished: over equal time intervals, the remaining fraction decreases by the same proportion. The response therefore changes rapidly at first and more slowly later. The parameter τ is a retardation time. At one τ, approximately 63.2% of the delayed response has developed; at three τ, approximately 95.0% has developed. It is a characteristic timescale, not a moment at which every change suddenly ends.

$$
J(t)=J_0+J_1\!\left(1-e^{-t/\tau}\right)+\frac{t}{\eta_0},\qquad \varepsilon(t)=\sigma_0J(t)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/78711ccf7196ae9599387d2a.svg) | Creep compliance following a loading step, Pa⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/a994f358d07ca2f1e8d481af.svg) | Instantaneous compliance, Pa⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/56837856c14a72566e349ad4.svg) | Additional compliance approached by the delayed-recovery element, Pa⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time after loading, s; this expression uses t≥0. |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | Retardation time, s; the parallel element’s viscosity divided by its elastic modulus. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb4e0ab9086f7736b32cea50.svg) | Terminal viscosity of the series flow dashpot, Pa·s. |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | Base of the natural exponential, approximately 2.71828, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/465ea137606b4c7e2067f528.svg) | Constant engineering stress, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/dd72237021aa073cc29bdada.svg) | Engineering strain, dimensionless. |

Series elements carry the same stress and their strains add; t/τ in the exponential must be dimensionless. With J₀=0.000020 Pa⁻¹, J₁=0.000040 Pa⁻¹, τ=40 s and η₀=20000000 Pa·s, a 500 Pa stress held for 180 s produces a pre-unloading strain of approximately 0.034278, or 3.428%.

The teaching example uses an instantaneous compliance of 0.000020 Pa⁻¹, a delayed compliance of 0.000040 Pa⁻¹, a retardation time of 40 s and a terminal viscosity of 20000000 Pa·s. At a stress of 500 Pa, the immediate strain is 1.00%. After holding for 180 s, the strain just before unloading is about 3.428%. The immediate contribution is 1.00 percentage point, the delayed contribution is about 1.978 percentage points, and the flowing contribution is 0.450 percentage points. Decomposing the total reveals that a single rising curve can contain both recoverable deformation and deformation that remains permanently in this model. The plotted components use exactly these parameters.

A rising late-time curve does not by itself identify steady flow. If a retardation time is much longer than the observation window, its exponential contribution looks nearly linear within the available interval and can resemble a viscous term. A longer hold, a recovery segment, or changes in temperature and specimen dimensions provide additional information. Conversely, an approximately horizontal final segment indicates slow growth within the measured window. Predicting a much longer service period requires evidence relevant to that period. Expressing the result at a defined time, rather than assigning a vague label such as durable, makes the measurement easier to connect to an engineering or biological use.

![Component contributions and the full creep–recovery curve generated from one parameter set. The stacked contributions sum to the pre-unloading strain. Unloading at 180 s produces immediate recoil followed by approach to a 0.450% model residual. Constructed teaching data at 500 Pa engineering stress.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/00a36c20df6cf48ed55d444c.svg?v=00a36c20df6c)

Figure 2Component contributions and the full creep–recovery curve generated from one parameter set. The stacked contributions sum to the pre-unloading strain. Unloading at 180 s produces immediate recoil followed by approach to a 0.450% model residual. Constructed teaching data at 500 Pa engineering stress.

The fit uses positive parameters to preserve the physical meanings of compliance, viscosity and time. In the program, logarithms of the parameters are fitted and then converted back to their original units. This also helps numerical optimization deal with parameters whose magnitudes differ greatly. Least squares seeks parameters that reduce the differences between observations and predictions, but an attractive overlap between two curves does not establish that every parameter is separately well determined. If two parameters compensate for one another while leaving the predicted curve almost unchanged, their individual estimates can vary considerably. Residuals, uncertainty scales and sensitivity to the fitted time interval are therefore part of the interpretation.

Units provide another check on the model. A compliance expressed in kPa⁻¹ has a numerical value one thousand times its value in Pa⁻¹: 0.000040 Pa⁻¹ equals 0.040 kPa⁻¹. The same strain is divided by a smaller numerical stress when stress is expressed in kilopascals. Terminal viscosity, by contrast, has units of stress multiplied by time; Pa·s and Pa/s describe different quantities. Converting every input to one consistent unit system before fitting, and changing display units only when plotting, avoids a calculation that runs successfully while its parameters are wrong by a thousandfold. Checking that all terms have compatible units also clarifies why they can be added.

## Remove the load and follow what remains

The recovery segment asks a further question: how much of the accumulated deformation was temporary? Under linear superposition, removing a load at a chosen time is equivalent to adding a stress step of equal magnitude and opposite sign. The original loading event retains its own history; the later negative step begins a second history that offsets it. The resulting deformation is the difference between compliance responses with two different starting times. No advanced calculus is needed to understand the construction. Every change in stress has its own clock. With several loading steps, calculate the contribution of each change using its elapsed time, then add the contributions.

$$
\varepsilon(t)=\sigma_0\!\left[J(t)-J(t-t_h)\right]\quad(t\geq t_h),\qquad \varepsilon_{\mathrm{res},\infty}=\frac{\sigma_0t_h}{\eta_0}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dd72237021aa073cc29bdada.svg) | Engineering strain after unloading, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/465ea137606b4c7e2067f528.svg) | Constant engineering stress before unloading, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/70f3dc39744c98269cbe57ad.svg) | The creep-compliance function defined above, Pa⁻¹. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time from the original loading event, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/87a9fd0f547cfac0b56c2382.svg) | Holding duration and unloading time, s. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb4e0ab9086f7736b32cea50.svg) | Terminal viscosity, Pa·s. |
| ![Formula](https://ml-biomat.com/static/agent-math/6b812d82bdc604fb38d896f1.svg) | Residual strain after complete recovery in the model, dimensionless; ∞ denotes the long-time limit. |

Unloading adds a negative stress step, whose response is subtracted under linear superposition. At 500 Pa for 180 s with a terminal viscosity of 20000000 Pa·s, the long-time residual is 500×180/20000000=0.0045, or 0.450%. The immediate elastic contribution recovers at unloading; the delayed contribution then continues to recover.

When the example is unloaded at 180 s, the immediate elastic contribution first decreases by 1.00 percentage point. The delayed contribution then recovers progressively. At sufficiently long recovery times, the model retains a strain of 0.450%, produced by the series flow dashpot during the hold. Doubling the holding time while retaining the same parameters doubles that residual. A model without the flow contribution would eventually return to zero. In an experiment, a reported residual strain is always read after a specified recovery duration. The value measured after 240 s of recovery and the infinite-time limit extrapolated from a model are different quantities; both become useful when their definitions are stated explicitly.

In a hydrated material, slow recovery may also involve water re-entering the specimen. If doubling thickness increases the recovery time by roughly a factor of four, a diffusion-like or poroelastic process becomes a useful mechanism to investigate. The squared-distance scaling is a clue that must be considered together with drainage boundaries and material structure. Grip slip produces a different kind of residual deformation and can be investigated using specimen markers, repeated loading or alternative gripping conditions. The recovery segment is valuable because specimens with similar loading curves may show distinctly different behavior after the external force is removed.

Incomplete recovery should also be distinguished from structural damage. Some materials normally accommodate chain sliding or the reformation of junctions, leaving a stable new shape. Others may develop cracks, interfacial debonding or broken network connections. These processes can all leave residual deformation while producing different subsequent load-bearing behavior. After recovery, apply the same small load again and compare the immediate compliance and the entire second response. Microscopy or mass measurements can provide additional evidence about what changed. This repeated measurement connects the residual shape with structural behavior instead of using a single final displacement to assign a general judgment to the material.

## Interactive experiment: Change the loading history and follow recovery

Adjust the three sliders to compare peak strain, recoil and long-time residual. Parameters follow the chapter’s linear teaching model; strain is displayed in percent.

[Figure: Creep and recovery curve](https://ml-biomat.com/tutorials/experimental-methods/m06/en/#M06-plot)

The interactive experiment adjusts stress, holding time and retardation time independently. First keep the material parameters fixed and double stress: the peak and residual strains should both double in this linear model. Next extend the holding time at fixed stress. The delayed contribution approaches saturation, while the flow contribution continues to accumulate. Finally change the retardation time and compare the speed of recovery. The display implements the stated equations, so every visible change can be checked numerically. Whether a real specimen follows this linear relation over a chosen stress range is assessed with the multiple-load comparison described earlier. The interaction makes that testable assumption visible.

## Fit the record while keeping the diagnostic information

The complete example begins with a creep–recovery record generated from known parameters, then adds measurement noise using a fixed random seed. This construction lets each stage of the calculation be checked against a known answer. The exported table retains time, stress, theoretical strain and noisy strain, giving every plotted point an explicit origin. Only the loading segment is fitted. The recovery segment is then predicted from those fitted parameters. This separation helps distinguish reproducing a familiar curve from capturing a relation that carries over to a different part of the loading history. The results are a controlled numerical teaching experiment, rather than measurements from a particular material.

The program plots residuals alongside the fitted response. A residual is the observed strain minus the predicted strain. Residuals scattered around zero without a clear pattern indicate that the model describes the main shape at the present noise scale. Residuals that remain positive early and negative later can indicate an omitted time process, but may also reveal that a finite loading ramp was treated as an instantaneous step. Recording the actual force rise helps separate these explanations. For a slowly loading instrument, the measured stress history can be represented by many small steps and processed with the same superposition idea. That approach preserves the experiment's history instead of hiding it through an unexplained deletion of early points.

![The loading segment is fitted and the recovery segment is predicted. Residuals are observations minus predictions; shading spans twice the prescribed noise standard deviation in strain percentage points. All observations are constructed from the stated model plus fixed-seed noise.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/82c34c3c282778a22f76612b.svg?v=82c34c3c2827)

Figure 3The loading segment is fitted and the recovery segment is predicted. Residuals are observations minus predictions; shading spans twice the prescribed noise standard deviation in strain percentage points. All observations are constructed from the stated model plus fixed-seed noise.

Parameter uncertainty from a fit differs from uncertainty in the experimental inputs. The local parameter standard errors in this example arise from sensitivity near the fitted solution and the stated noise level. They describe statistical variation for this model and this observation window. A systematic thickness error of 10%, however, affects stress and compliance together and is not removed by collecting more time points. Testing independently prepared specimens reveals variation in the material and its preparation. Reanalyzing a single record mainly investigates the stability of the calculation. Keeping these levels separate avoids counting hundreds of correlated time samples as hundreds of independent material specimens.

Sampling also determines which details remain visible. Retain sufficiently dense records near loading and unloading, where the response changes fastest. A display may show fewer points in a slowly varying late segment while preserving the complete underlying data. Instrument smoothing often correlates neighboring errors, so confidence intervals based on independent white noise may no longer describe the record. The example deliberately uses independent constructed noise, giving its local standard errors a clear teaching interpretation. For measurements, unloaded records, stable segments and independently tested specimens help characterize the relevant error structure. A smooth line can aid reading; the original points and processing choices preserve the basis for interpreting time dependence.

### Complete example: Predict recovery from a creep record

The program uses consistent SI units and exports constructed noisy data, fitted parameters, numerical checks and four figures. It fits the loading segment and evaluates predictions during recovery.

```
"""Creep and recovery: a reproducible constructed experiment in SI units."""
from pathlib import Path
import argparse, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from scipy.optimize import curve_fit


def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def compliance(t, j0, j1, tau, eta):
    t = np.asarray(t, dtype=float)
    return j0 + j1 * (-np.expm1(-t / tau)) + t / eta


def response(t, stress, hold, pars):
    """Right-continuous response: a negative stress step begins at hold."""
    t = np.asarray(t, dtype=float)
    result = stress * compliance(t, *pars)
    unload = t >= hold
    result[unload] -= stress * compliance(t[unload] - hold, *pars)
    return result


def fit_loading(t, strain, stress, noise):
    def model(times, *log_parameters):
        return stress * compliance(times, *np.exp(log_parameters))
    logs, covariance = curve_fit(
        model, t, strain, p0=np.log([2e-5, 4e-5, 40, 2e7]),
        sigma=np.full(t.size, noise), absolute_sigma=True,
        bounds=(np.log([1e-7, 1e-7, 0.5, 1e5]),
                np.log([1e-2, 1e-2, 2e4, 1e11])), maxfev=20000)
    parameters = np.exp(logs)
    standard_error = parameters * np.sqrt(np.diag(covariance))
    return parameters, standard_error


def setup(language):
    from matplotlib import font_manager
    names = {f.name for f in font_manager.fontManager.ttflist}
    cjk = next((n for n in ['Microsoft YaHei', 'Noto Sans CJK SC', 'SimHei'] if n in names), 'DejaVu Sans')
    plt.rcParams.update({'font.family': cjk if language == 'zh' else 'DejaVu Sans',
        'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False,
        'axes.labelcolor': '#213342', 'text.color': '#213342',
        'axes.prop_cycle': plt.cycler(color=['#176c83', '#d4813d', '#7d5ea4', '#3c8a6a']),
        'svg.fonttype': 'none', 'figure.facecolor': '#faf9f5',
        'axes.facecolor': '#faf9f5', 'savefig.facecolor': '#faf9f5',
        'axes.unicode_minus': False})
    return lambda zh, en: zh if language == 'zh' else _label(en)


def main(output, language):
    output.mkdir(parents=True, exist_ok=True)
    tr = setup(language)
    seed, stress, hold, noise = 604, 500., 180., 0.0001
    parameters = np.array([2e-5, 4e-5, 40., 2e7])
    times = np.r_[np.linspace(0, hold, 121, endpoint=False), np.linspace(hold, 420, 121)]
    truth = response(times, stress, hold, parameters)
    observed = truth + np.random.default_rng(seed).normal(0, noise, times.size)
    loading = times < hold
    fitted, errors = fit_loading(times[loading], observed[loading], stress, noise)
    predicted = response(times, stress, hold, fitted)
    residual = observed - predicted
    np.savetxt(output / 'data.csv', np.c_[times, np.where(loading, stress, 0), truth, observed],
        delimiter=',', header='time_s,stress_Pa,theoretical_strain,observed_strain', comments='')
    peak = float(stress * compliance(hold, *parameters))
    summary = {'data_kind': 'constructed teaching experiment', 'seed': seed,
        'instantaneous_strain': float(stress*parameters[0]),
        'peak_strain_before_unload': peak,
        'permanent_strain': float(stress*hold/parameters[3]),
        'retardation_fraction_at_tau': float(1-np.exp(-1)),
        'fitted': dict(zip(['j0_Pa_inverse','j1_Pa_inverse','tau_s','eta_Pa_s'], map(float,fitted))),
        'local_standard_errors': dict(zip(['j0_Pa_inverse','j1_Pa_inverse','tau_s','eta_Pa_s'], map(float,errors))),
        'recovery_rmse_strain': float(np.sqrt(np.mean(residual[~loading]**2)))}
    (output/'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf8')

    def save(fig, name):
        fig.savefig(output / f'{name}-{language}.svg', bbox_inches='tight')
        plt.close(fig)

    # Original conceptual drawing: history and mechanical response share symbols.
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), layout='constrained', gridspec_kw={'width_ratios':[1.05,1.25]})
    a, b = axes
    for ax in axes: ax.set(xlim=(0,10),ylim=(0,10));ax.axis('off')
    a.set_title(tr('A  从恒力到长度变化','A  Constant force, changing length'),loc='left',fontweight='bold')
    a.add_patch(Rectangle((2,8),4,.45,color='#7b8990'))
    a.add_patch(Rectangle((3.25,3.5),1.5,4.5,facecolor='#b9d7d9',edgecolor='#176c83',lw=2))
    a.add_patch(Rectangle((2.5,2.8),3,.6,color='#7b8990'))
    a.add_patch(FancyArrowPatch((4,2.7),(4,.7),arrowstyle='-|>',mutation_scale=19,lw=2,color='#d4813d'))
    a.annotate(tr('固定端','Fixed grip'),(6.1,8.2),fontsize=11)
    a.annotate(tr('试样标距','Gauge length'),(5.2,5.8),fontsize=11)
    a.annotate(tr('载荷传感器','Load cell'),(5.8,3.0),fontsize=11)
    a.text(4,.3,tr('控制力，记录伸长与时间','Control force; record extension and time'),ha='center',fontsize=10)
    b.set_title(tr('B  三种响应的机械语言','B  A mechanical language for three responses'),loc='left',fontweight='bold')
    def spring(x1,x2,y,color):
        xs=np.linspace(x1,x2,17);ys=np.full(17,y);ys[1:-1]=y+np.tile([.35,-.35],8)[:15]
        b.plot(xs,ys,color=color,lw=2)
    def dashpot(x1,x2,y,color):
        b.plot([x1,x1+.6],[y,y],color=color,lw=2)
        b.plot([x1+.6,x1+.6,x2-.5,x2-.5],[y+.4,y-.4,y-.4,y+.4],color=color,lw=2)
        b.plot([x1+1,x1+1],[y-.3,y+.3],color=color,lw=2)
        b.plot([x1+1,x2],[y,y],color=color,lw=2)
    spring(.3,2.3,6.8,'#176c83'); b.text(1.3,8,tr('立即弹性','Immediate elasticity'),ha='center')
    b.plot([2.3,3,3],[6.8,6.8,7.8],color='#213342'); b.plot([3,3],[6.8,5.8],color='#213342')
    spring(3,5.3,7.8,'#7d5ea4');dashpot(3,5.3,5.8,'#7d5ea4')
    b.plot([5.3,5.3,6],[7.8,6.8,6.8],color='#213342');b.plot([5.3,5.3],[5.8,6.8],color='#213342')
    dashpot(6,8.5,6.8,'#d4813d')
    b.text(4.2,9.1,tr('延迟恢复','Delayed recovery'),ha='center');b.text(7.3,8,tr('持续流动','Ongoing flow'),ha='center')
    b.text(.4,3.6,tr('十九世纪：弹性与黏性模型','19th century: elastic and viscous models'),fontsize=11)
    b.annotate('',(8.7,2.7),(.4,2.7),arrowprops={'arrowstyle':'->','color':'#7b8990'})
    b.text(.4,1.7,tr('1929：流变学会成立','1929: Society of Rheology founded'),fontsize=11)
    b.text(.4,.45,tr('原创概念示意；串联单元的变形相加','Original conceptual diagram; series deformations add'),fontsize=9,color='#62747d')
    save(fig,'mechanism')

    fig, axs = plt.subplots(1,2,figsize=(12,4.7),layout='constrained')
    t=np.linspace(0,hold,301)
    components=[np.full_like(t,stress*parameters[0]*100),stress*parameters[1]*(-np.expm1(-t/parameters[2]))*100,stress*t/parameters[3]*100]
    labels=[tr('立即弹性','Immediate elastic'),tr('延迟恢复部分','Delayed recoverable'),tr('黏性流动','Viscous flow')]
    axs[0].stackplot(t,*components,labels=labels,alpha=.7)
    axs[0].set(xlabel=tr('加载时间 / s','Loading time / s'),ylabel=tr('应变 / %','Strain / %'),title=tr('A  卸载前的三部分贡献','A  Three contributions before unloading'))
    axs[0].legend(frameon=False,fontsize=9,loc='upper left')
    axs[1].plot(times,truth*100,lw=2.5);axs[1].axvline(hold,color='#777',ls=':',lw=1)
    axs[1].axhline(summary['permanent_strain']*100,color='#d4813d',ls='--',label=tr('长期残余 0.450%','Long-time residual 0.450%'))
    axs[1].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('应变 / %','Strain / %'),title=tr('B  蠕变与卸载恢复','B  Creep and recovery'))
    axs[1].legend(frameon=False,fontsize=9); save(fig,'components')

    fig,axs=plt.subplots(2,1,figsize=(11,6.3),layout='constrained',sharex=True,gridspec_kw={'height_ratios':[2,1]})
    axs[0].scatter(times[::3],observed[::3]*100,s=13,color='#899b9e',label=tr('构造观测值','Constructed observations'))
    axs[0].plot(times[loading],predicted[loading]*100,color='#176c83',lw=2,label=tr('加载段拟合','Fit to loading'))
    axs[0].plot(times[~loading],predicted[~loading]*100,color='#d4813d',lw=2,label=tr('恢复段预测','Predicted recovery'))
    axs[0].set(ylabel=tr('应变 / %','Strain / %'),title=tr('A  用加载段预测恢复段','A  Predict recovery from the loading fit'))
    axs[0].legend(frameon=False,ncols=3,fontsize=9)
    axs[1].axhspan(-noise*200,noise*200,color='#176c83',alpha=.1,label=tr('±2 倍设定噪声标准差','±2 prescribed noise standard deviations'))
    axs[1].axhline(0,color='#738087',lw=1);axs[1].scatter(times,residual*100,s=10,color='#176c83')
    axs[1].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('残差 / 百分点','Residual / percentage points'))
    axs[1].legend(frameon=False,fontsize=9); save(fig,'diagnostics')

    fig,axs=plt.subplots(1,2,figsize=(12,4.6),layout='constrained')
    for st in [250,500,750]:
        axs[0].plot(t,st*compliance(t,*parameters)*100,lw=2,label=f'{st} Pa')
    axs[0].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('应变 / %','Strain / %'),title=tr('A  线性模型中的载荷比例','A  Stress proportionality in the linear model'));axs[0].legend(frameon=False)
    for tau,col in [(20,'#176c83'),(40,'#d4813d'),(80,'#7d5ea4')]:
        p=parameters.copy();p[2]=tau;axs[1].plot(times,response(times,stress,hold,p)*100,lw=2,color=col,label=f'τ = {tau} s')
    axs[1].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('应变 / %','Strain / %'),title=tr('B  改变时间尺度，残余极限相同','B  Different retardation times, same residual limit'));axs[1].legend(frameon=False)
    save(fig,'design')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en')
    args=parser.parse_args();main(args.output,args.language)
```

After running the example, inspect the exported data table first. Time is in seconds, stress is in pascals and strain is dimensionless; multiplying strain by 100 is a plotting conversion to percent. Next compare the immediate strain, pre-unloading strain and long-time residual in summary.json with the hand calculations. Examine whether the fitted timescale is close to the generating value. Then change the noise, shorten the hold or remove the recovery observations and study parameter stability. Replacing constructed data with an instrument export now has a clear procedure: preserve time and load history, unify units, and choose a response model consistent with the measurement geometry.

## Design the measurement around the intended use

For a tissue scaffold that must retain pore space under a small sustained load, deformation over several hours and subsequent recovery may be central. For a pressure-sensitive adhesive in a joint, accumulated displacement and stress dependence may matter more. A soft sealing material may require temperature cycles, contact with a working liquid and repeated loading. The same creep instrument can support these studies, but the duration, load and shape metric should follow the intended use. Even the axes become an expression of the research question: strain after a specified hold answers a different practical question from the initial compliance or the residual after recovery.

Temperature often changes the speed of molecular motion substantially. Time–temperature superposition attempts to shift curves measured at different temperatures along the time axis to build a broader observation window. It works when the relevant processes change compatibly with temperature and when the material does not undergo interfering changes such as crystallization, phase separation or drying. Compare curve shapes and overlapping intervals before interpreting shift factors. A high-temperature short experiment becomes a useful predictor of a cooler, longer experiment through this physical validation. Testing predictions within an overlapping time interval provides a practical first step before extending the range of application.

A use requirement can be translated into a directly checkable criterion. Suppose a joint allows an engineering strain of 4% after a specified load has been held for 180 s. The example's predicted 3.428% meets that particular deformation requirement. If the permitted residual after full recovery is 0.2%, the predicted 0.450% instead suggests increasing terminal viscosity, shortening the sustained loading period or changing the structure. The two criteria assess different aspects of performance, so improving one does not automatically improve the other. Once the criteria are explicit, the creep record becomes evidence for a design choice rather than a competition to find the flattest-looking curve.

![Changing load and changing timescale have different consequences. Stress and strain scale proportionally in the linear model on the left. Changing retardation time on the right changes recovery speed, while matching stress, hold and terminal viscosity retain the same residual limit. Teaching-model curves.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9612ea6e88839c289b165848.svg?v=9612ea6e8883)

Figure 4Changing load and changing timescale have different consequences. Stress and strain scale proportionally in the linear model on the left. Changing retardation time on the right changes recovery speed, while matching stress, hold and terminal viscosity retain the same residual limit. Teaching-model curves.

A useful report retains specimen geometry, environment, loading rise time, holding and recovery durations, stress level and the number of independently tested specimens. Give axes with clear units and identify what any error bars describe. Report compliance at selected times, peak strain, residual strain after a specified recovery period and model parameters supported by the observations. These quantities connect the material response to actual use conditions. Dynamic mechanical analysis, introduced next, asks a different version of the same time-dependent question: repeated small oscillations reveal how stress and strain differ in phase and how energy is stored or dissipated. Creep and oscillatory testing use different loading languages to study the same material's response over time.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/M06.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [David Roylance — Linear Viscoelasticity](https://eng.libretexts.org/Bookshelves/Mechanical_Engineering/Mechanics_of_Materials_%28Roylance%29/05:_General_Stress_Analysis/5.04:_Linear_Viscoelasticity)

   Foundational reading on elastic and viscous elements and loading history.
2. [RepTate — Creep Theories](https://reptate.readthedocs.io/manual/Applications/Creep/Theory/theory.html)

   Definitions of retardation modes, instantaneous compliance and terminal viscosity.
3. [RepTate — Tutorial Creep Application](https://reptate.readthedocs.io/manual/Applications/Creep/Tutorial/tutorialGUICreep.html)

   Further practice with creep-data import, views and fitting.
4. [Society of Rheology — History](https://www.societyofrheology.org/history)

   History of the Society of Rheology and its scientific community.

   Historical reference; original illustration.
5. [SciPy — curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

   Least squares, parameter bounds and covariance interpretation.
6. [RepTate — TTS Theories](https://reptate.readthedocs.io/manual/Applications/TTS/Theory/theory.html)

   Further reading on time–temperature superposition and shift factors.
