# From Observations to Models: Fitting and Residuals

Source: https://ml-biomat.com/tutorials/python-scientific/p19/en/
Language: en

Use a stress-relaxation curve to understand how parameters, residuals, and observation time shape a fit.

## Begin with a soft material held at a fixed stretch

Stretch a soft rubber strip a little and hold it at that length. The pulling force often decreases gradually even though the strip remains stretched. Different parts of the material are rearranging internally. An experiment can record the force needed to maintain the deformation and divide it by a specified cross-sectional area to obtain stress as a function of time. Two useful questions follow: how quickly does the stress decrease, and how much remains after a long time? Fitting expresses these questions as parameters with units, allowing changes in different samples to be compared. This chapter uses an explicitly constructed teaching dataset to develop a model, fit it with SciPy, inspect residuals, and examine the effect of observation time.

Keep three objects separate from the beginning. Observations are the recorded numbers, shown as points. A model is a function that calculates stress at a supplied time, shown as a continuous curve. Parameters determine the particular shape of that function. Two curves may both fall toward a plateau while completing most of their decrease over a few seconds or over tens of seconds. A parameter gives that difference a numerical expression. Evaluating the function takes time as input and returns model stress. Fitting reverses the direction of the problem: it uses the observed records to search for parameters that bring the function close to those records.

The example contains 25 records from 0 to 12 s, separated by 0.5 s. Its ideal curve begins at 2.8 kPa and approaches a plateau of 0.4 kPa, with a time scale of 3 s. A small, explicitly listed perturbation is then added to each point. The kilopascal, abbreviated kPa, is a unit of stress and pressure. Every record can be traced to the stated curve and its perturbation. Knowing the generating rule, then treating its parameters as unknown, helps us distinguish two questions: whether the numerical method solves a known problem correctly, and whether the available observations distinguish one parameter combination from another.

Fitting resembles reconstructing a route from a set of landmarks. The landmark locations are the data, the allowed route shapes are the model, and a few adjustable controls are the parameters. How the route passes between landmarks depends on the chosen structure. Passing through every landmark exactly may sacrifice the pattern that the route was intended to describe. We will therefore read the curve together with the deviations it leaves behind. The prerequisites are arrays that store numbers, functions that repeat a calculation, and the meaning of plot coordinates. Exponentials and least squares will be developed within the example.

## Give amplitude, time scale, and plateau separate roles

A simple relaxation model separates stress into a decaying part and a persistent plateau. The decaying part is initially large and then decreases exponentially. Exponential change means that equal time intervals multiply the remaining decaying part by the same factor; they do not subtract the same amount of stress. Compound interest also repeatedly multiplies a quantity by a factor, but here the factor is below one and the quantity decreases. The resulting curve falls quickly at first and then becomes progressively flatter. One exponential is a useful description when a single main time scale organizes the observed relaxation.

$$
s(t)=A\exp(-t/\tau)+b
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a2e2af48082172a695b27ad4.svg) | Model stress at time t, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time after holding deformation, s |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | Initial excess stress above the plateau, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | Positive relaxation time, s; the Greek letter tau |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Long-time plateau stress, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/64460da0d752153c52e1bd62.svg) | Exponential function with base e; dimensionless input and output |

Because t and τ have the same units, their ratio is dimensionless. For A=2.4 kPa, τ=3 s, and b=0.4 kPa, t=0 gives exp(0)=1 and stress 2.8 kPa. At t=3 s, exp(−1)≈0.367879, giving 2.4×0.367879+0.4≈1.28291 kPa. The exponential part decreases while b remains fixed; one τ describes one dominant relaxation time scale.

A and b both have stress units and can therefore be added. Dividing time t by time scale τ cancels the units before the result enters the exponential. This check has a practical purpose. If the time array is in seconds but the numerical value of τ is supplied in minutes without conversion, the program still evaluates a curve, although its time scale has changed. A larger τ gives a smaller t/τ at the same observation time, so the exponential decreases more slowly. At t=τ, about 36.8% of the initial decaying part remains. This fraction refers to the excess above the plateau; the plateau itself does not participate in that proportional decrease.

![Three parameters have distinct observable roles: A sets the initial excess above the plateau, τ sets the time scale, and b sets the long-time plateau. The curve uses A=2.4 kPa, τ=3 s, and b=0.4 kPa.](https://ml-biomat.com/static/tutorials/python-scientific/figures/9ee8c3c8fe8c78216a3fcb05.svg?v=9ee8c3c8fe8c)

Figure 1Three parameters have distinct observable roles: A sets the initial excess above the plateau, τ sets the time scale, and b sets the long-time plateau. The curve uses A=2.4 kPa, τ=3 s, and b=0.4 kPa.

The initial stress is A+b. Treating the first observed stress directly as A would include the plateau in the amplitude. Likewise, the last observation at 12 s still contains a small decaying contribution as well as its perturbation. Treating that point as the exact plateau would carry both into b. The first and last records are useful for initial estimates; the complete fit uses all records to adjust those estimates. In the generating example, A=2.4 kPa and b=0.4 kPa together produce an initial model stress of 2.8 kPa, while retaining distinct meanings.

The model also belongs to a set of experimental conditions. Temperature, imposed deformation, and material state are treated as stable over the observation interval, and one τ describes the dominant change. Two well-separated relaxation processes could produce an early rapid decrease followed by a much slower one. A changing temperature could also affect the apparent time scale. Experimental records and residual patterns help distinguish these possibilities. Giving parameters physical meanings connects model selection, observation planning, and the interpretation of numerical results.

## Turn closeness to the data into a computable requirement

A chosen parameter combination supplies a model value at every observation time. Subtract the model value from the observation to obtain a residual. Positive residuals place observations above the curve; negative residuals place them below. Their signs are valuable because a sustained sequence of positive residuals reveals an interval in which the model is systematically low. To compare parameter combinations, we also need to combine the 25 residuals into an objective. Least squares uses their squared sum, preventing positive and negative deviations from cancelling and assigning a greater cost to larger departures.

$$
r_i=y_i-s(t_i),\qquad Q=\sum_{i=1}^{n}r_i^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Observation index from 1 to n; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Number of fitted observations; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/d66c51d3359af66c3f0dc0c5.svg) | Time of observation i, s |
| ![Formula](https://ml-biomat.com/static/agent-math/a51d7c6c42d3bb0b61f865ba.svg) | Observed stress for record i, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/ff229aed753b3375e39a6524.svg) | Model stress at the same time, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/3a3efe8d09f46a481b251330.svg) | Residual, observed minus model stress, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/4be111afe7c23428ae5024a8.svg) | Sum of squared residuals, also SSE, kPa² |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | Sum the following terms over the observation index |

A positive residual places an observation above the curve. Residuals 0.03, −0.02, and 0.01 kPa add to 0.02 kPa, but their squares sum to 0.0009+0.0004+0.0001=0.0014 kPa². Squaring prevents cancellation and gives larger departures a greater cost. The equal-weight sum suits observations with common units and comparable error scales; model comparisons use the same records.

The word “least” describes a specific numerical task: search within the chosen model and permitted parameter range for a smaller squared-error sum. It does not require the curve to pass through every point. When observations contain small perturbations, a curve describing their common tendency usually passes through the point cloud. Adding increasingly flexible parameters can reduce the objective further, even allowing a separate adjustment for each point, but then the parameters cease to summarize a shared process. Here three parameters explain 25 observations together, while the residuals retain the part left unexplained.

An equal-weight squared sum also encodes a choice: departures of the same stress magnitude incur the same cost. This suits records with comparable error scales. If some measurements are more precise than others, divide each residual by its measurement-error standard deviation before squaring. A departure is then assessed relative to the usual error size of that measurement. The standard deviation describes a measurement's variability; it is different from the magnitude of the reading. Using the reading itself as its standard deviation would introduce another weighting scheme that needs a separate justification.

$$
Q_w=\sum_{i=1}^{n}\left(\frac{r_i}{\sigma_i}\right)^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/387edda104c523c662ff5727.svg) | Residual sum of squares weighted by measurement standard deviations; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/9ec0d2298548e930111bc32b.svg) | Observation index and total count; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/3a3efe8d09f46a481b251330.svg) | Residual for observation i, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/1d11eec53e2e8f271603794c.svg) | Known or externally estimated error standard deviation for observation i, kPa |

A 0.04 kPa residual with a 0.02 kPa standard deviation has ratio 2 and contributes 4. The same residual with a 0.08 kPa standard deviation has ratio 0.5 and contributes 0.25. The comparison is relative to each measurement precision. This expression treats errors as uncorrelated; correlated errors call for a full covariance matrix. The explicit teaching perturbations here have no separately supplied instrument standard deviations, so the executed example uses equal weights.

The executed example uses equal weights because its teaching perturbations are listed explicitly and no separate instrument standard deviations are supplied. In an experiment, calibration or repeated measurements can provide an error scale for weighting. Errors can also be correlated: a slowly drifting instrument may produce several successive deviations in the same direction, so those records contain partly repeated information. A full error covariance matrix can describe that relationship. Plotting residuals in time order is a useful first step because drift, an omitted plateau, and an isolated unusual point leave different visible structures.

## Use SciPy while keeping the calculation understandable

An important development in scientific software has been the connection of established numerical methods to consistent array and function interfaces. In their 2020 overview, SciPy developers describe the project's development from its early release to version 1.0 in 2017, bringing together optimization, integration, signal processing, and other methods. Today a NumPy array can hold observation times, a Python function can express the model, and SciPy can adjust its parameters. This organization leaves more attention for the experimental question and the interpretation of results while preserving an executable calculation. The diagram makes this connection concrete using the chapter’s 25 observations: three candidate time scales generate curves, array subtraction gives pointwise residuals, and squared residuals produce a comparable objective. At each fixed time scale, linear least squares re-solves A and b; the star identifies the bounded curve_fit result.

![SciPy methods illustrated with this chapter’s 25 teaching observations: A and b re-solved at fixed τ=2, 3, and 5 s, pointwise residuals, and their sum of squares. The lower-right profile re-solves both linear coefficients at every τ; the star marks the bounded curve_fit result. SciPy connects these array and function operations to reusable numerical algorithms.](https://ml-biomat.com/static/tutorials/python-scientific/figures/6efdd65b63e912b9c110ad46.svg?v=6efdd65b63e9)

Figure 2SciPy methods illustrated with this chapter’s 25 teaching observations: A and b re-solved at fixed τ=2, 3, and 5 s, pointwise residuals, and their sum of squares. The lower-right profile re-solves both linear coefficients at every τ; the star marks the bounded curve_fit result. SciPy connects these array and function operations to reusable numerical algorithms.

`curve_fit` first needs a model function. Its first argument is the independent variable, time here; subsequent arguments are amplitude, time scale, and plateau in that order. It also needs time and stress arrays with equal lengths and matching order. Sorting time requires the same rearrangement of stress. The argument `p0=[2., 2., .3]` supplies a starting point, with units kPa, s, and kPa. It tells the algorithm which curve to begin from without fixing the answer there. The `bounds` argument supplies allowed parameter ranges. This example keeps amplitude and plateau nonnegative and time scale positive.

Imagine numerical search on an error landscape. A location corresponds to a parameter combination, and its height is the residual sum of squares. The algorithm investigates how nearby changes can lower the objective and updates the parameters accordingly. A poor initial region, parameters differing by many orders of magnitude, or many combinations producing similar curves can make the search harder. Consistent units, manageable scales, and curve-based starting estimates clarify the numerical problem. Read convergence information together with parameter values, proximity to bounds, and residuals; a returned array is one part of the result.

The returned `popt` array follows the parameter order in the model function. The `pcov` matrix estimates parameter covariance using a local linear approximation. Taking square roots of diagonal entries gives corresponding local parameter standard deviations with their appropriate units. “Local” means that the objective surface near the best fit is approximated by a simpler shape. When the data constrain a combination of parameters more strongly than its individual components, those parameters can be strongly correlated. A few standard deviations may conceal that relationship. Profiling will expose it by changing one parameter and reoptimizing the others.

## Run the complete example and inspect what the curve leaves behind

The script below contains data generation, two model fits, parameter profiles, four figures, and a numerical summary. The `relaxation` function expresses the model, `profile` solves two coefficients at a fixed τ, and `main` organizes the calculation and output. All figures and data are written to the selected output directory. The CSV retains each time, stress, and teaching perturbation. Use `--language zh` or `--language en` to choose the language inside figures. The plotting backend writes files directly, so inspect the generated figures and summary after execution.

### Complete example: curves, residuals, profiles, and independent numerical checks

The script directly uses NumPy, SciPy, and Matplotlib. Explicit perturbations, the model, native fitting, independent profiling, and four figures are in one file; outputs include CSV data and a numerical summary.

```
"""Fit an explicitly defined relaxation dataset and inspect residuals and profiles."""
from pathlib import Path
import argparse
import json
import numpy as np
import scipy
from scipy.optimize import curve_fit, minimize_scalar
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

BLUE, RED, INK, GRAY = "#28658c", "#b64a35", "#202e39", "#71808b"


def relaxation(t, amplitude, tau, baseline):
    return amplitude * np.exp(-np.asarray(t) / tau) + baseline


def profile(t, observed, tau):
    """Solve the two linear coefficients at a fixed positive time scale."""
    design = np.column_stack((np.exp(-t / tau), np.ones_like(t)))
    amplitude, baseline = np.linalg.lstsq(design, observed, rcond=None)[0]
    residual = observed - design @ np.array([amplitude, baseline])
    return float(residual @ residual), float(amplitude), float(baseline)


def main(output, language):
    output.mkdir(parents=True, exist_ok=True)
    zh = language == "zh"
    def tr(a, b): return a if zh else b
    plt.rcParams.update({"font.family": [name for name in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans'] if name in {f.name for f in font_manager.fontManager.ttflist}],
        "font.size": 11, "axes.labelsize": 12, "axes.titlesize": 13,
        "axes.titleweight": "bold", "axes.spines.top": False,
        "axes.spines.right": False, "text.color": INK, "svg.fonttype": "none",
        "svg.hashsalt": "P19", "savefig.facecolor": "white"})
    t = np.arange(25, dtype=float) / 2
    noise = np.array([.04,-.03,.02,-.05,.01,.03,-.02,.04,-.01,-.03,
                     .02,-.04,.03,0,-.02,.01,.03,-.01,-.03,.02,-.01,.03,-.02,.01,-.02])
    truth = np.array([2.4, 3., .4])
    y = relaxation(t, *truth) + noise
    popt, pcov = curve_fit(relaxation, t, y, p0=[2., 2., .3],
        bounds=([0., .1, 0.], [10., 20., 3.]), xtol=1e-12, ftol=1e-12, gtol=1e-12)
    def zero_baseline(time, amplitude, tau): return relaxation(time, amplitude, tau, 0.)
    pzero, _ = curve_fit(zero_baseline, t, y, p0=[2., 3.],
        bounds=([0., .1], [10., 20.]), xtol=1e-12, ftol=1e-12, gtol=1e-12)
    residual = y - relaxation(t, *popt)
    residual_zero = y - zero_baseline(t, *pzero)
    tau_grid = np.linspace(1., 7., 301)
    profiles = {}
    for end in (3., 6., 12.):
        use = t <= end
        solution = minimize_scalar(lambda tau: profile(t[use], y[use], tau)[0],
                                   bounds=(1., 7.), method="bounded",
                                   options={"xatol": 1e-12})
        loss, amp, base = profile(t[use], y[use], solution.x)
        profiles[str(int(end))] = {"n": int(use.sum()), "tau_s": float(solution.x),
            "amplitude_kPa": amp, "baseline_kPa": base, "sse_kPa2": loss,
            "curve": [profile(t[use], y[use], q)[0] for q in tau_grid]}
    clean, _ = curve_fit(relaxation, t, relaxation(t, *truth), p0=[2., 2., .3],
                        bounds=([0., .1, 0.], [10., 20., 3.]),
                        xtol=1e-12, ftol=1e-12, gtol=1e-12)
    assert np.max(np.abs(clean-truth)) < 1e-8
    assert abs(profiles["12"]["tau_s"] - popt[1]) < 1e-5
    assert residual @ residual < residual_zero @ residual_zero
    dense = np.linspace(0, 12, 400)
    def save(fig, name):
        fig.savefig(output / f"{name}-{language}.svg", metadata={"Date": None})
        fig.savefig(output / f"{name}-{language}.png", dpi=180)
        plt.close(fig)
    fig, ax = plt.subplots(figsize=(11.5, 5.5), layout="constrained")
    ax.plot(dense, relaxation(dense, *truth), color=BLUE, lw=2.5)
    ax.axhline(.4, color=GRAY, ls="--", lw=1)
    ax.vlines(3, 0, relaxation(3, *truth), color=RED, ls="--")
    ax.scatter([0,3], relaxation(np.array([0,3]), *truth), color=RED, zorder=4)
    ax.annotate("A + b = 2.8 kPa", (0,2.8), xytext=(1.3,2.65),
                arrowprops={"arrowstyle":"->", "color":GRAY})
    ax.annotate(tr("t = τ：超出平台的部分剩下约36.8%", "t = τ: 36.8% of the initial excess remains"),
                (3,relaxation(3,*truth)), xytext=(4.4,1.75),
                arrowprops={"arrowstyle":"->", "color":RED}, color=RED)
    ax.text(8,.23,"b = 0.4 kPa",color=GRAY)
    ax.set(xlim=(-.2,12),ylim=(0,3.1),xlabel=tr("时间 / s","Time / s"),
           ylabel=tr("应力 / kPa","Stress / kPa"),
           title=tr("参数把曲线拆成高度、时间尺度和平台", "Parameters separate amplitude, time scale, and plateau"))
    save(fig,"parameters")
    fig, axes = plt.subplots(2,2,figsize=(12.3,8.2),sharex=True,sharey="row",
                             gridspec_kw={"height_ratios":[2.1,1]},layout="constrained")
    for j,(parameters,errors,title) in enumerate([(popt,residual,tr("带平台的指数模型","Exponential with a plateau")),
         (np.r_[pzero,0.],residual_zero,tr("强制平台为零","Plateau fixed to zero"))]):
        axes[0,j].scatter(t,y,s=27,color=INK,label=tr("教学数据","Teaching data"),zorder=3)
        axes[0,j].plot(dense,relaxation(dense,*parameters),color=BLUE if j==0 else RED,lw=2,
                       label=tr("拟合曲线","Fitted curve"))
        axes[0,j].set_title(title,loc="left")
        axes[0,j].legend(frameon=False,fontsize=10)
        axes[0,j].set_ylim(0,3.05)
        axes[1,j].axhline(0,color=GRAY,lw=1)
        axes[1,j].vlines(t,0,errors,color=BLUE if j==0 else RED,lw=1.5)
        axes[1,j].scatter(t,errors,color=BLUE if j==0 else RED,s=20)
        axes[1,j].set(xlabel=tr("时间 / s","Time / s"),ylim=(-.3,.3))
        axes[1,j].text(.96,.94,f"SSE = {errors @ errors:.5f} kPa²",transform=axes[1,j].transAxes,
                        va="top",ha="right",bbox={"fc":"white","ec":"none","alpha":.9},fontsize=10)
    axes[0,0].set_ylabel(tr("应力 / kPa","Stress / kPa"))
    axes[1,0].set_ylabel(tr("观测 − 拟合 / kPa","Observed − fitted / kPa"))
    save(fig,"residuals")
    fig, axes = plt.subplots(1,2,figsize=(12.3,5.7),layout="constrained")
    colors=[RED,GRAY,BLUE]
    for end,color in zip((3,6,12),colors):
        p=profiles[str(end)]
        axes[0].plot(tau_grid,np.asarray(p["curve"])-p["sse_kPa2"],color=color,lw=2,
                     label=f"0–{end} s; n={p['n']}")
        axes[0].scatter([p["tau_s"]],[0],color=color,s=35,zorder=4)
    axes[0].set(xlabel=tr("固定的时间尺度 τ / s","Fixed time scale τ / s"),
        ylabel=tr("相对最小值增加的SSE / kPa²","SSE above its minimum / kPa²"),ylim=(-.015,.6),
        title=tr("观测窗口决定谷底有多清楚","The observation window shapes the valley"))
    axes[0].legend(frameon=False)
    axes[1].scatter(t,y,color=INK,s=25,zorder=4)
    for tau,color in zip((2.,3.,5.),(RED,BLUE,GRAY)):
        _,amplitude,baseline=profile(t[t<=3],y[t<=3],tau)
        axes[1].plot(dense,relaxation(dense,amplitude,tau,baseline),color=color,lw=2,label=f"τ = {tau:g} s")
    axes[1].axvspan(0,3,color="#eaf1f5",zorder=0)
    axes[1].set(xlabel=tr("时间 / s","Time / s"),ylabel=tr("应力 / kPa","Stress / kPa"),
                title=tr("只用前3秒拟合，向后外推","Fit the first 3 seconds, then extrapolate"),ylim=(-.6,3.1))
    axes[1].legend(frameon=False)
    save(fig,"profiles")
    fig,axes=plt.subplot_mosaic([['curves','curves'],['residuals','objective']],
                                figsize=(12.3,9),layout='constrained')
    axes['curves'].scatter(t,y,color=INK,s=24,zorder=5,label=tr('25个教学观测值','25 teaching observations'))
    candidate_sse=[]
    for tau,color in zip((2.,3.,5.),(RED,BLUE,GRAY)):
        loss,amp,base=profile(t,y,tau);candidate_sse.append(loss)
        axes['curves'].plot(dense,relaxation(dense,amp,tau,base),color=color,lw=2,
                            label=f'τ={tau:g} s; A={amp:.3f} kPa; b={base:.3f} kPa')
        axes['residuals'].plot(t,y-relaxation(t,amp,tau,base),'o-',color=color,ms=3,
                               lw=1.3,label=f'τ={tau:g} s')
    axes['curves'].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('应力 / kPa','Stress / kPa'),
                       title=tr('A  函数接口：每个候选τ都生成一条完整曲线','A  Function interface: each candidate τ generates a complete curve'))
    axes['curves'].legend(frameon=False,fontsize=10,ncols=2)
    axes['residuals'].axhline(0,color=INK,lw=1)
    axes['residuals'].set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('观测 − 模型 / kPa','Observed − model / kPa'),
                          title=tr('B  数组相减：逐点计算残差','B  Array subtraction: pointwise residuals'))
    axes['residuals'].legend(frameon=False)
    axes['objective'].plot(tau_grid,profiles['12']['curve'],color=INK,lw=1.7)
    axes['objective'].scatter([2,3,5],candidate_sse,c=[RED,BLUE,GRAY],s=55,zorder=5)
    axes['objective'].scatter([popt[1]],[residual@residual],marker='*',color='#d19a24',s=150,zorder=6,
                              label=tr('有边界curve_fit结果','Bounded curve_fit result'))
    axes['objective'].set(xlabel=tr('固定的τ / s','Fixed τ / s'),ylabel='SSE / kPa²',
                          title=tr('C  数值搜索：定位平方和的低处','C  Numerical search: locate a lower sum of squares'))
    axes['objective'].legend(frameon=False,fontsize=10)
    for a in axes.values():a.grid(alpha=.14)
    fig.suptitle(tr('SciPy：数组、模型函数与数值求解在同一问题中相接',
                     'SciPy: arrays, model functions, and numerical solvers meet'),fontsize=16)
    save(fig,"history")
    np.savetxt(output/"relaxation.csv",np.c_[t,y,noise],delimiter=",",comments="",
               header="time_s,stress_kPa,teaching_perturbation_kPa",fmt="%.12g")
    summary={"data_kind":"defined teaching model plus explicit perturbations", "n":len(t),
        "truth":{"amplitude_kPa":2.4,"tau_s":3.,"baseline_kPa":.4},
        "fit":{"amplitude_kPa":float(popt[0]),"tau_s":float(popt[1]),"baseline_kPa":float(popt[2]),
               "sse_kPa2":float(residual@residual),"residual_sd_kPa":float(np.sqrt(residual@residual/(len(t)-3))),
               "local_parameter_std":np.sqrt(np.diag(pcov)).tolist()},
        "zero_baseline":{"amplitude_kPa":float(pzero[0]),"tau_s":float(pzero[1]),
                         "sse_kPa2":float(residual_zero@residual_zero)},
        "profiles":{k:{q:v for q,v in p.items() if q!="curve"} for k,p in profiles.items()},
        "noise_free_max_abs_error":float(np.max(np.abs(clean-truth))),
        "profile_native_tau_difference_s":float(abs(profiles["12"]["tau_s"]-popt[1])),
        "versions":{"numpy":np.__version__,"scipy":scipy.__version__,"matplotlib":matplotlib.__version__}}
    (output/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    (output/"profile-data.json").write_text(json.dumps({"tau_s":tau_grid.tolist(),"profiles":profiles}),encoding="utf-8")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=Path("output"))
    parser.add_argument("--language",choices=["zh","en"],default="en")
    args=parser.parse_args()
    main(args.output,args.language)
```

The calculation gives A≈2.40810 kPa, τ≈2.97543 s, and b≈0.40224 kPa, with a residual sum of squares of approximately 0.01679233 kPa². These estimates are close to the generating values 2.4 kPa, 3 s, and 0.4 kPa without matching them exactly, because fitting uses the perturbed observations. The script also removes the perturbations and recovers the known generating parameters with the same fitting call. The largest absolute parameter discrepancy is then approximately 4.4×10⁻¹⁶, at floating-point rounding scale. The two calculations answer different questions: the first shows parameter estimation in perturbed data, and the second checks numerical consistency on a problem with a known answer.

![The same 25 teaching observations are fitted with and without a plateau. Curves occupy the upper row; residual panels share one vertical scale. The zero-plateau model leaves structured early, middle, and late deviations. Each vertical line retains its observation time.](https://ml-biomat.com/static/tutorials/python-scientific/figures/6c774d8735e3e251a9c90811.svg?v=6c774d8735e3)

Figure 3The same 25 teaching observations are fitted with and without a plateau. Curves occupy the upper row; residual panels share one vertical scale. The zero-plateau model leaves structured early, middle, and late deviations. Each vertical line retains its observation time.

Fixing the plateau to zero instead gives τ≈4.97216 s and increases the squared-error sum to 0.37693015 kPa². To accommodate late observations that remain above zero, the fitted curve decreases more slowly overall. It then lies too high through much of the middle interval and too low toward the end. The residual panel makes this structure clear: positive values first, a sustained negative section, and positive values again later. The zero-plateau model struggles to describe the early, middle, and late observations simultaneously. Residuals from the plateau model fluctuate around zero with a much smaller magnitude. Shared axis limits make this difference directly comparable.

Residual size can also be summarized in the same units as stress. Divide the squared-error sum by the number of observations minus the number of fitted parameters, then take the square root. The resulting residual standard-deviation estimate is easier to compare with the variability of an individual observation than a squared sum is. It still belongs beside the residual plot because one number cannot preserve a sequence of positive or negative deviations. With 25 observations and three parameters, the example has 22 residual degrees of freedom and a residual scale of about 0.02763 kPa. Residual scale describes variation around a curve; parameter standard deviations describe local uncertainty in estimated parameters.

$$
s_r=\sqrt{\frac{Q}{n-p}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/516137c2821586f22d9e1cae.svg) | Estimated residual standard deviation, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/4be111afe7c23428ae5024a8.svg) | Sum of squared residuals, kPa² |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Observation count; dimensionless, 25 here |
| ![Formula](https://ml-biomat.com/static/agent-math/48c7b594e8628a17b991d4e6.svg) | Number of fitted parameters; dimensionless, 3 here |

Fitting uses p parameter directions, so the residual scale uses n−p. With 25 records, 3 parameters, and Q=0.0167923269 kPa², sqrt(0.0167923269/22)=0.02762766 kPa. Its statistical interpretation assumes independent errors, an appropriate mean model, and equal variance; for nonlinear models this is a usual local approximation. It differs from the standard deviation of a fitted parameter.

## Why a longer observation interval can add different information

Suppose the instrument records only the first 3 s. The early decrease is visible, but the curve has not approached its plateau closely. A lower plateau with slower decay or a higher plateau with faster decay may both pass through nearly the same early points. Parameters can compensate for each other. Weak identifiability means that the available observations distinguish some parameter choices poorly; it is a relationship between the data and the model. Sampling the same short interval more densely adds mainly early-time information. Extending observations toward the plateau adds a different part of the curve's shape.

A profile calculation reveals this compensation systematically. Fix τ at 3 s. The exponential value at every observation time is now known. Call these values z, and the model becomes a straight line in z, with amplitude as its slope and plateau as its intercept. A linear least-squares solution gives the best A and b at this fixed τ. Change τ to 3.1 s and solve A and b again. Repeating the procedure produces a curve showing the smallest squared-error sum attainable at each τ. This is the objective profile for the time scale.

$$
z_i=\exp(-t_i/\tau),\quad A=\frac{\sum_i(z_i-\bar z)(y_i-\bar y)}{\sum_i(z_i-\bar z)^2},\quad b=\bar y-A\bar z
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/51874f02b4c579417c89ce04.svg) | Exponential value for observation i at a fixed τ; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/1cedf803e310ed61a4074c0b.svg) | Observation time and fixed time scale, s |
| ![Formula](https://ml-biomat.com/static/agent-math/a51d7c6c42d3bb0b61f865ba.svg) | Observed stress, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/0c0542cabaa03a20baa1420d.svg) | Arithmetic mean of the z values; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/b95acd43e540455890524d58.svg) | Arithmetic mean observed stress, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/95c6ae2cac80faa066eac4ee.svg) | Least-squares amplitude and plateau at this fixed τ, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/5ca220bf09b42c86c851749f.svg) | Sum over all currently included observations |

At fixed τ, the model is a straight line Az+b in z. A divides joint variation in z and y by variation in z; b places the line through their mean point. For an algebraic example z=[1,0.5,0] and y=[2.8,1.6,0.4] kPa, means are 0.5 and 1.6, numerator 1.2 kPa, denominator 0.5, hence A=2.4 kPa and b=0.4 kPa. Here z=0 is the limiting value of exponential decay, used for simple arithmetic; finite-time values are positive. The calculation requires some variation in z.

The Python script solves the two-column design matrix with `np.linalg.lstsq`. The browser experiment uses the means and sums in the displayed expression. These are different computational routes to the same linear problem. A one-dimensional minimization then finds the profile valley. For the full dataset it gives τ≈2.975432546 s, differing from native `curve_fit` by about 1.4×10⁻⁹ s. One route adjusts all three parameters together; the other eliminates two linear coefficients before searching the remaining time scale. Their agreement supplies a useful numerical cross-check.

![Left: each fixed τ is followed by a fresh fit of A and b. Each SSE profile is shifted by its own minimum to compare its shape. Right: three fixed-τ curves use only observations from 0–3 s; curves outside the shaded interval are extrapolations. These profiles allow an unrestricted b, including negative extrapolated plateaus.](https://ml-biomat.com/static/tutorials/python-scientific/figures/70a709ebbeb1fcc24cac22e9.svg?v=70a709ebbeb1)

Figure 4Left: each fixed τ is followed by a fresh fit of A and b. Each SSE profile is shifted by its own minimum to compare its shape. Right: three fixed-τ curves use only observations from 0–3 s; curves outside the shaded interval are extrapolations. These profiles allow an unrestricted b, including negative extrapolated plateaus.

In the left panel, the profile for 0–3 s is relatively flat near its minimum: many time scales attain similar objectives. The 0–12 s profile has a more sharply defined valley. Each profile has its own minimum subtracted, so the figure compares the cost of moving away from that window's best time scale rather than total error across different sample counts. In the right panel, all three curves fit only the first 3 s. They remain close in the shaded region and separate when extrapolated. The profile calculation allows b to vary freely to reveal parameter compensation, so some time scales produce negative plateaus. If the physical problem requires a nonnegative plateau, apply that same constraint within profiling and interpret the resulting constrained valley.

## Read the curve, residuals, and error landscape together

The experiment below lets you change τ while recalculating the best A and b after every change. The main panel displays the current curve and all 25 observations. Shading marks the interval included in fitting, and hollow points retain observations beyond it. The residual panel shows residuals for included observations. The profile panel shows the entire profile for the same observation window, marking the currently selected τ in red. Together, the panels answer where the curve changes, which records deviate, and how the combined objective changes. The profile axis shows squared error for the selected window and rescales when that window changes.

## Change the time scale and watch parameters compensate

A and b are refitted after every change in fixed τ. All three views use the same teaching data. Filled points enter the fit; hollow points show extrapolation. A and b are unrestricted here, so the plateau can be negative. Residual and SSE axes rescale when the observation window changes; read their ticks as well as their shapes.

[Figure: Fitted curve, included interval, and extrapolation records](https://ml-biomat.com/tutorials/python-scientific/p19/en/#P19-curve)

[Figure: Signed residuals for the included observations](https://ml-biomat.com/tutorials/python-scientific/p19/en/#P19-residual)

[Figure: Minimum sum of squared residuals at different fixed time scales](https://ml-biomat.com/tutorials/python-scientific/p19/en/#P19-profile)

Begin with the 12 s window and change τ from 3 to 5 s. Amplitude and plateau change too, compensating as well as they can for the new time scale; the residuals show the structure that remains after compensation. Keep τ at 5 s and shorten the window to 3 s. The early points and curve now appear closer, and the profile valley becomes flatter. The later hollow points reveal the difference between extrapolation and the full record. Keeping those observations visible distinguishes “excluded from this fit” from “never observed.” Reset returns to τ=3 s and a 12 s window for comparison with the original setting.

A slider position is not automatically an optimum. The red point identifies the current fixed τ, while A and b are fitted conditionally on that choice. The profile valley identifies the best region in the time-scale search. The same distinction matters when a research analysis fixes a parameter from earlier literature: the remaining coefficients belong to a conditional fit. Releasing all parameters creates a different estimation problem. State which quantities were fixed and which were estimated so another reader can reproduce the same curve and interpret its parameters correctly.

## Return the fitted numbers to the experimental question

An interpretable fit retains its observation interval, model, parameter units, and residuals. The present result can be stated fully: an equal-weight single-exponential model with a plateau fitted to 25 teaching observations from 0–12 s gives a time scale of approximately 2.975 s and plateau of approximately 0.402 kPa, with residual scale approximately 0.0276 kPa. Readers can identify the model and time range associated with those numbers and inspect whether organized variation remains. Reporting a long decimal by itself loses the information that gives the value meaning.

Residual structures can guide concrete next steps. A slow drift suggests checking baseline stability and environmental conditions. Concentrated early departures suggest examining whether loading has finished and whether the time origin is aligned. A rapid early process followed by a slower one motivates comparing physically interpretable multiple-process descriptions and collecting observations across their respective time scales. When parameters compensate strongly, a longer observation window or an independent plateau measurement can add more information than extra optimization iterations.

The same reasoning can support reaction concentration, a local release stage, cooling, or instrument response, with a model chosen for each question. In cooling, for example, a plateau may represent environmental temperature, amplitude an initial temperature difference, and time scale the relevant heat-transfer conditions. Units, boundary conditions, measurement errors, and mechanism must follow the application. A Python function expresses these choices precisely, SciPy solves the resulting numerical problem, and curves with residuals connect the solution back to an observable scientific process.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P19.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [SciPy: curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

   Model functions, parameter bounds, sigma, and local covariance.

   SciPy BSD-3 documentation; original teaching dataset and explanations
2. [SciPy: Optimization tutorial](https://docs.scipy.org/doc/scipy/tutorial/optimize.html)

   Least-squares problems and numerical optimization interfaces.

   SciPy BSD-3 documentation
3. [NIST/SEMATECH: Least Squares](https://www.itl.nist.gov/div898/handbook/pmd/section4/pmd431.htm)

   Mathematical reference for squared error, linear coefficient solutions, and residual scale.
4. [Virtanen et al. (2020), SciPy 1.0](https://arxiv.org/abs/1907.10121)

   A computing-history and methods overview written by SciPy developers.

   CC BY 4.0; facts paraphrased, original diagram
