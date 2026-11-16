# From Materials Observations to an Inspectable Analysis

Source: https://ml-biomat.com/tutorials/python-scientific/p29/en/
Language: en

Connect real adsorption observations to parameters, residuals, and further measurements; compare model shape and pressure coverage.

## Turning an adsorption curve into an inspectable materials result

How does an air-purification material hold gas at its surface? Molecules arrive, remain for a while, and leave again. The amount retained at a particular temperature and pressure matters for the quantity of adsorbent required, its surface properties, and its operating conditions. An experiment often begins with a modest table: set a pressure and record an adsorbed amount. Analysis then asks how the amount changes, which curve describes the observations, and what its parameters help us understand. This chapter develops that table into a complete project with fitted parameters, residuals, uncertainty intervals, and a comparison of pressure coverage.

We use the 14 observed values in Misra1a, a NIST Statistical Reference Dataset from a 1978 dental study of monomolecular adsorption. Pressure is the predictor and volume is the response. The record specifies these variables but does not identify their physical units, so the figures retain “recorded pressure unit” and “recorded volume unit.” These definitions are sufficient to reproduce the numerical analysis and compare its parameters. Converting the results to pascals or millilitres requires the unit definitions from the experimental record. Such information belongs at the start of an analysis because it determines how results can be compared with another experiment.

The project combines pandas for tables, NumPy for array arithmetic, SciPy for estimation and uncertainty, and Matplotlib for presentation. Each library handles part of the same chain of evidence. A table row becomes a plotted point; the points together determine a curve; each difference between point and curve becomes a residual. You can follow any number through this chain without memorizing every function in advance. Ideas from [reading tables](https://ml-biomat.com/tutorials/python-scientific/p11/en/) and [fitting and residuals](https://ml-biomat.com/tutorials/python-scientific/p19/en/) reappear here in one scientific task.

## Establishing what one row actually records

The supplied `Misra1a.dat` is a plain text file. Its introductory portion describes variables, the reference model, and numerical results; the observations follow later. The first numerical column is volume and the second is pressure. Assuming that the first column must be the horizontal coordinate could still produce a smooth graph, while quietly changing the research question. The program locates the explicit heading above the numerical table, reads whitespace-separated values, and assigns the names `volume` and `pressure`. Those names preserve scientific meaning throughout the calculation, rather than relying on a memory of what column zero probably contains.

The first row records volume 10.07 at pressure 77.6. The final row records volume 81.78 at pressure 760.0. These are observations at 14 pressure conditions, rather than 14 repeats at one condition. We check the number of rows, finite positive values, and uniqueness of pressure, then sort by pressure. Sorting gives a line a consistent direction and gives “the first six observations” a precise meaning: the six lowest-pressure conditions. It also prevents the physical interpretation of a subset from depending on an accidental file order.

After checking numbers, read the scatter plot itself. Pressure rises by roughly a factor of 9.8 while volume rises by about 8.1, so the response is beginning to flatten. The curve at the largest observed pressure is still clearly increasing. A seating area offers a useful analogy: many vacant seats initially make it easy to accommodate arrivals, while fewer vacancies later reduce the increase in occupancy. Adsorption also involves molecular interactions, temperature, and a continuing balance between arrival and departure. The model must specify which of those details it retains and which conditions allow the simplification.

![Observed pressure–volume values, exponential fit, and approximate mean-curve interval; shared-axis residuals reveal small structured discrepancies.](https://ml-biomat.com/static/tutorials/python-scientific/figures/e525276930e5670dce427882.svg?v=e525276930e5)

Figure 1Observed pressure–volume values, exponential fit, and approximate mean-curve interval; shared-axis residuals reveal small structured discrepancies.

The upper panel places observations beside the fitted curve. The lower panel uses the same pressure coordinate to magnify their small differences. In the upper panel, many discrepancies are smaller than the plotted symbols. Below, residuals are mostly positive at low pressure, negative through the middle, and positive again near the high end. The two panels answer different questions: one shows the overall response, while the other reveals how the selected mathematical shape systematically departs from it.

## From surface sites to equations: two different routes toward saturation

In his 1918 study of gas adsorption on glass, mica, and platinum, Langmuir connected adsorption with molecular layers and a finite surface. A familiar simplified model treats the surface as equivalent sites, each accommodating at most one molecule, with adsorption and desorption balanced at steady state. If the occupied fraction is θ, the vacant fraction is 1−θ. More gas and more vacancies promote adsorption, while desorption occurs from occupied sites. At fixed temperature, with approximately equivalent sites and negligible interactions between neighboring adsorbates, this balance gives the following relation.

$$
\theta=\frac{KP}{1+KP},\qquad V=A\theta=\frac{AKP}{1+KP}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/06e47e2878930095abe73547.svg) | occupied fraction of sites, from zero to one, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | pressure, recorded pressure unit |
| ![Formula](https://ml-biomat.com/static/agent-math/24733a44cf365eb5e1b92574.svg) | Langmuir equilibrium parameter, inverse recorded pressure unit |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | saturation volume of this model, recorded volume unit |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | predicted adsorbed volume, recorded volume unit |

Adsorption is proportional to pressure times vacant fraction, while desorption is proportional to occupied fraction. Equating the rates and writing their coefficient ratio as K gives θ. Multiplication by the full-occupancy volume A gives V. For an illustrative A=100 volume units, K=0.002 inverse pressure units, and P=500 pressure units, KP=1, θ=1/2, and V=50 volume units. The simplification assumes fixed temperature, equivalent sites, and at most one molecule per site.

The two parameters provide different scales. A sets the eventual plateau height; K sets the pressure scale over which the curve approaches it. Setting KP to one gives half the capacity, so 1/K is the model’s half-saturation pressure. The surface illustration contains nine sites, five occupied, to explain occupancy and vacancy. Those nine sites are a conceptual picture rather than a replacement for the 14 experimental observations. A site belongs to a microscopic description; the observed volume is a collective response from many molecules. Keeping those scales distinct makes the connection between diagram and equation easier to follow.

![Finite-site surface diagram and actual fits of two functions. Shading marks observed pressure coverage; the remainder shows mathematical extrapolation.](https://ml-biomat.com/static/tutorials/python-scientific/figures/e98bd719ec90396b23bff2c6.svg?v=e98bd719ec90)

Figure 2Finite-site surface diagram and actual fits of two functions. Shading marks observed pressure coverage; the remainder shows mathematical extrapolation.

NIST specifies a different numerical reference model for Misra1a: an exponential saturation curve. It also begins at zero and approaches a plateau, but bends differently between those limits. The certified reference values let us check whether we have solved a particular mathematical problem correctly. Choosing a mathematical problem that describes a material also requires examining residuals and the physical conditions behind the model. We therefore reproduce the specified exponential fit first, then fit the Langmuir function to the same observations for comparison.

$$
\widehat V(P)=A\left(1-e^{-kP}\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8a576b30f1fc1047cbfe6275.svg) | predicted mean volume at pressure P, recorded volume unit; the hat denotes prediction |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | asymptotic capacity in the exponential model, recorded volume unit |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | pressure-scale parameter of the exponential model, inverse recorded pressure unit |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | pressure, recorded pressure unit |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | base of the natural exponential, approximately 2.71828, dimensionless |

The product kP is dimensionless and can appear in an exponent. At zero pressure the bracket is zero; at increasing pressure the exponential tends to zero and the prediction approaches A. For an illustrative A=100 volume units, k=0.002 inverse pressure units, and P=500 pressure units, kP=1 and the prediction is 100×(1−e⁻¹)≈63.2121 volume units, distinct from the Langmuir value 50 for the analogous example.

Here k multiplies pressure, so its unit is inverse pressure. A similar exponential expression describing time dependence could instead involve a coefficient measured in inverse seconds. Similar-looking functions do not automatically give their parameters the same physical meaning. In the code, `-np.expm1(-k * pressure)` evaluates one minus an exponential. The dedicated `expm1` function calculates an exponential minus one accurately when its argument is small, reducing the loss of precision that can occur when subtracting two nearby numbers. It is a small but useful connection between the written formula and the arithmetic performed by the computer.

## Letting all observations determine the parameters

Imagine moving the fitted curve by hand. Increasing A raises predictions, while reducing k can pull predictions at lower pressures back down. The parameters can compensate for one another, which makes visual adjustment ambiguous. Least squares defines a specific objective. Evaluate the prediction at every measured pressure, subtract prediction from observation to obtain a residual, square each residual, and add the squares. Squaring prevents positive and negative differences from canceling and assigns a larger cost to larger discrepancies.

$$
r_i=V_i-\widehat V(P_i),\qquad \mathrm{RSS}=\sum_{i=1}^{n}r_i^2,\qquad s=\sqrt{\frac{\mathrm{RSS}}{n-2}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9ec0d2298548e930111bc32b.svg) | observation index and count, dimensionless; n=14 here |
| ![Formula](https://ml-biomat.com/static/agent-math/538402917df2dc5b1bae4c8e.svg) | pressure and volume of observation i, in their respective recorded units |
| ![Formula](https://ml-biomat.com/static/agent-math/1bb2f4fa5d74eb43925bfa72.svg) | predicted volume at that pressure, recorded volume unit |
| ![Formula](https://ml-biomat.com/static/agent-math/3a3efe8d09f46a481b251330.svg) | observed minus predicted residual, recorded volume unit |
| ![Formula](https://ml-biomat.com/static/agent-math/b50b0236980ee4169c09fda4.svg) | sum of squared residuals, squared recorded volume unit |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | residual standard deviation, recorded volume unit; the denominator subtracts two estimated parameters |
| ![Formula](https://ml-biomat.com/static/agent-math/df10424aca79108f20c06f2f.svg) | summation sign: add the squared residual for each observation from 1 through n |

Squaring prevents positive and negative deviations from canceling. The first residual is 10.07−9.98626636≈0.08373364 volume units and contributes about 0.00701132 squared volume units. All 14 terms sum to 0.12455138894. Division by 14−2=12 and a square root give s≈0.10187876 volume units. Equal weights treat volume errors as comparable in scale, with pressure taken as given in the fit.

The record provides no point-specific measurement standard deviations, so this analysis uses equal weights. This treats volume errors as having a comparable scale and takes measured pressure as given in the fit. An experiment with substantial pressure uncertainty calls for a model of both measurement axes. When reliable observation-specific standard deviations are available, `sigma` can supply weights. Weighting should reflect measurement meaning, rather than an attempt to suppress inconvenient observations. Here the residual standard deviation is the square root of RSS divided by 12: 14 observations minus two estimated parameters.

`curve_fit` receives a function that predicts volume from pressure and parameters, the pressure array, the volume array, and initial parameter values. We start at A=250 and k=0.0005, require positive parameters, and use `x_scale` to indicate their characteristic numerical magnitudes. A is on the order of hundreds while k is on the order of a few ten-thousandths. Moving both by an equal numerical step would have very unequal consequences. Scaling helps the search navigate these magnitudes; it does not change the residual sum of squares being minimized.

The program also supplies a Jacobian: the sensitivity of each predicted value to a small change in each parameter. Think of it as a table of local directions available to the solver. How much would a prediction change if A increased a little? What if k increased? For the exponential model, the derivative with respect to A is one minus the exponential; the derivative with respect to k is A times pressure times the exponential. These become the two columns returned by the code. Using the program does not require learning all of optimization first, but understanding where those columns come from helps check signs, units, and array shapes.

## Running the project and following one number

Keep `main.py` and `data/Misra1a.dat` in the supplied relative arrangement and run the command below. It creates a result table, a numerical summary, and three figure groups. `--output` selects the results directory and `--language` selects the figure language. The program reads the observations once, fits each of the two models using six through fourteen points, and writes all 18 states into the interaction data. The downloadable analysis and the parameter comparisons on this page therefore share the same definitions.

### Run the project

Replace en with zh to generate Chinese figures.

```
python main.py --output results --language en
```

### Complete adsorption analysis: data, two fits, intervals, and figures

Read the supplied 14 observations, reproduce the numerical reference, and calculate 18 coverage states.

```
"""Analyze the observed NIST Misra1a adsorption data and fitting range."""
from pathlib import Path
from io import StringIO
import argparse
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import t
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle, Rectangle



def available_plot_fonts():
    """Choose installed fonts; keep a Latin fallback on every platform."""
    choices = ["Noto Sans CJK SC", "Noto Sans SC", "Microsoft YaHei", "SimHei", "DejaVu Sans"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    return [name for name in choices if name in installed]



def exponential(pressure, capacity, scale):
    return -capacity * np.expm1(-scale * pressure)


def langmuir(pressure, capacity, scale):
    return capacity * scale * pressure / (1 + scale * pressure)


def jacobian(pressure, capacity, scale, model):
    if model == 'exponential':
        return np.column_stack((-np.expm1(-scale * pressure),
                                capacity * pressure * np.exp(-scale * pressure)))
    denominator = 1 + scale * pressure
    return np.column_stack((scale * pressure / denominator,
                            capacity * pressure / denominator**2))


def load_data(path):
    raw = path.read_bytes()
    text = raw.decode('ascii')
    # The first Data heading describes variables; the second starts the numbers.
    numeric = text.split('Data:   y               x', 1)[1]
    frame = pd.read_csv(StringIO(numeric), sep=r'\s+', names=['volume', 'pressure'])
    if len(frame) != 14 or not np.isfinite(frame.to_numpy()).all():
        raise ValueError('Expected 14 finite observations')
    if frame.pressure.duplicated().any() or (frame <= 0).any().any():
        raise ValueError('Expected positive values and unique pressures')
    return frame.sort_values('pressure').reset_index(drop=True), hashlib.sha256(raw).hexdigest()


def fit(frame, count, model, grid):
    pressure = frame.pressure.to_numpy(dtype=float)
    volume = frame.volume.to_numpy(dtype=float)
    function = exponential if model == 'exponential' else langmuir
    parameters, covariance = curve_fit(
        function, pressure[:count], volume[:count], p0=[250, .0005],
        jac=lambda x, a, k: jacobian(x, a, k, model), bounds=(0, np.inf),
        x_scale=[250, .0005], ftol=1e-13, xtol=1e-13, gtol=1e-13,
        max_nfev=10000)
    residuals = volume - function(pressure, *parameters)
    rss = float(residuals[:count] @ residuals[:count])
    gradient = jacobian(grid, *parameters, model)
    variance = np.einsum('ij,jk,ik->i', gradient, covariance, gradient)
    half_width = t.ppf(.975, count - 2) * np.sqrt(np.maximum(0, variance))
    standard_error = np.sqrt(np.diag(covariance))
    return {'model': model, 'count': count, 'max_pressure': float(pressure[count-1]),
            'capacity': float(parameters[0]), 'scale': float(parameters[1]),
            'standard_errors': standard_error.tolist(),
            'correlation': float(covariance[0, 1] / np.prod(standard_error)),
            'rss': rss, 'residual_sd': float(np.sqrt(rss / (count-2))),
            'residuals': residuals.tolist(), 'prediction': function(grid, *parameters).tolist(),
            'mean_ci_half_width': half_width.tolist()}


def figures(frame, states, grid, output, language):
    zh = language == 'zh'
    tr = lambda a, b: a if zh else b
    plt.rcParams.update({'font.family': available_plot_fonts(),
                         'font.size': 13, 'axes.spines.top': False,
                         'axes.spines.right': False, 'svg.fonttype': 'none',
                         'axes.unicode_minus': False})
    blue, orange, green = '#205b8c', '#bd5535', '#2b7c73'
    p, v = frame.pressure.to_numpy(), frame.volume.to_numpy()
    full = next(s for s in states if s['count'] == 14 and s['model'] == 'exponential')
    other = next(s for s in states if s['count'] == 14 and s['model'] == 'langmuir')
    xlabel = tr('压力 / 原记录压力单位', 'Pressure / recorded pressure unit')
    ylabel = tr('体积 / 原记录体积单位', 'Volume / recorded volume unit')

    def save(fig, name):
        for suffix in ['svg', 'png']:
            fig.savefig(output / f'{name}-{language}.{suffix}', dpi=160,
                        facecolor='#faf9f5', bbox_inches='tight')
        plt.close(fig)

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True,
                             gridspec_kw={'height_ratios': [2.2, 1]}, layout='constrained')
    selected = grid <= 800
    prediction, half = np.array(full['prediction']), np.array(full['mean_ci_half_width'])
    axes[0].fill_between(grid[selected], (prediction-half)[selected],
                         (prediction+half)[selected], color=blue, alpha=.2,
                         label=tr('均值曲线的近似95%区间', 'Approximate 95% interval for the mean curve'))
    axes[0].plot(grid[selected], prediction[selected], color=blue, lw=2.5,
                 label=tr('指数模型拟合', 'Exponential model fit'))
    axes[0].scatter(p, v, s=56, facecolor='#faf9f5', edgecolor=orange,
                    linewidth=2, zorder=3, label=tr('14个观测值', '14 observed values'))
    axes[0].set(ylabel=ylabel, title=tr('观测与曲线：体积增加逐渐放缓',
                                      'Observations and curve: volume increases more slowly'))
    axes[0].legend(loc='upper left', fontsize=12)
    axes[1].axhline(0, color='#667782', lw=1)
    axes[1].stem(p, full['residuals'], linefmt=blue, markerfmt='o', basefmt=' ')
    axes[1].set(xlabel=xlabel, ylabel=tr('残差 / 体积单位', 'Residual / volume unit'),
                title=f"RSS = {full['rss']:.8f};  " + tr('自由度 = 12', 'degrees of freedom = 12'))
    save(fig, 'fit-and-residuals')

    fig = plt.figure(figsize=(13, 8), layout='constrained')
    gs = fig.add_gridspec(2, 2, width_ratios=[1.35, 1])
    ax = fig.add_subplot(gs[:, 0]); top = fig.add_subplot(gs[0, 1]); bottom = fig.add_subplot(gs[1, 1])
    capacities = np.linspace(210, 270, 180)
    scales = np.linspace(.000475, .00064, 180)
    aa, kk = np.meshgrid(capacities, scales)
    rss = np.sum((v[:, None, None] - exponential(p[:, None, None], aa, kk))**2, axis=0)
    filled = ax.contourf(aa, kk*1000, np.log10(rss/full['rss']),
                         levels=np.linspace(0, 4, 17), cmap='cividis', extend='max')
    ax.plot(full['capacity'], full['scale']*1000, '*', color=orange, ms=16)
    ax.set(xlabel=tr('容量参数 A / 体积单位', 'Capacity parameter A / volume unit'),
           ylabel=tr('尺度参数 k / 10⁻³ 压力单位⁻¹', 'Scale parameter k / 10⁻³ pressure unit⁻¹'),
           title=tr('同一批数据形成狭长的参数谷', 'A narrow parameter valley for the same data'))
    fig.colorbar(filled, ax=ax, label='log₁₀(RSS / RSSmin)', shrink=.7)
    subset = [s for s in states if s['model'] == 'exponential']
    for axis, key, index, factor, label in [(top, 'capacity', 0, 1, 'A'),
                                            (bottom, 'scale', 1, 1000, 'k × 1000')]:
        axis.errorbar([s['max_pressure'] for s in subset],
                       [s[key]*factor for s in subset],
                       yerr=[s['standard_errors'][index]*factor for s in subset],
                       color=blue, marker='o', capsize=3)
        axis.axhline(full[key]*factor, color=orange, ls='--')
        axis.set(ylabel=(tr('A / 体积单位','A / volume unit') if key=='capacity'
                         else tr('k / 10⁻³ 压力单位⁻¹','k / 10⁻³ pressure unit⁻¹')))
    top.set_title(tr('逐步纳入高压力观测\n误差棒为1 SE',
                     'Include higher-pressure observations\nBars show 1 SE'), fontsize=13)
    bottom.set_xlabel(tr('拟合范围的最大压力 / 原单位',
                         'Maximum fitted pressure / recorded unit'))
    save(fig, 'parameter-coverage')

    fig = plt.figure(figsize=(13, 8), layout='constrained')
    gs = fig.add_gridspec(2, 2, height_ratios=[.85, 1.35], width_ratios=[1, 1])
    surface = fig.add_subplot(gs[0, 0]); explanation = fig.add_subplot(gs[0, 1])
    curve = fig.add_subplot(gs[1, :])
    for axis in [surface, explanation]:
        axis.set(xlim=(0, 10), ylim=(0, 4)); axis.axis('off')
    surface.add_patch(Rectangle((.4, .5), 9, .65, facecolor='#ccd5d8'))
    occupied = {0, 2, 3, 6, 8}
    for i in range(9):
        surface.add_patch(Rectangle((.6+i, 1.15), .65, .12, color=blue))
        if i in occupied:
            surface.add_patch(Circle((.925+i, 1.65), .32, facecolor=orange))
    surface.annotate('', xy=(1.925, 1.5), xytext=(1.925, 3.3),
                     arrowprops={'arrowstyle': '->', 'lw': 2, 'color': blue})
    surface.annotate('', xy=(6.925, 3.3), xytext=(6.925, 2.1),
                     arrowprops={'arrowstyle': '->', 'lw': 2, 'color': orange})
    surface.text(.4, 3.75, tr('有限位点：空位吸附，已占位点脱附',
                             'Finite sites: adsorption and desorption'), fontsize=14)
    surface.text(.4, .05, tr('位点占据示意：5个占据，4个空位',
                            'Site occupancy: five occupied, four vacant'), fontsize=12)
    explanation.text(.2, 3.5, 'Langmuir, 1918', fontsize=19, weight='bold')
    explanation.text(.2, 2.55, tr('单层、等价位点、动态平衡',
                                 'Monolayer, equivalent sites, dynamic balance'), fontsize=14)
    explanation.text(.2, 1.55, r'$V=A K P/(1+K P)$', fontsize=21, color=green)
    explanation.text(.2, .3, tr('指数曲线采用另一种函数形状；分别检验',
                               'The exponential curve has a different shape'), fontsize=13)
    curve.axvspan(0, p.max(), color='#d8e2e7', alpha=.7,
                   label=tr('观测覆盖范围', 'Observed pressure coverage'))
    curve.plot(grid, full['prediction'], color=blue, lw=2.5,
                label=tr('指数模型', 'Exponential') + f"; RSS={full['rss']:.3f}")
    curve.plot(grid, other['prediction'], color=green, lw=2.5, ls='--',
                label=f"Langmuir; RSS={other['rss']:.3f}")
    curve.scatter(p, v, color=orange, s=25, zorder=3)
    curve.set(xlabel=xlabel, ylabel=ylabel, xlim=(0, grid.max()),
                title=tr('越过观测区间，模型形状的差别逐渐放大',
                         'Model shapes diverge beyond the observations'))
    curve.legend(loc='lower right', fontsize=12)
    save(fig, 'surface-and-extrapolation')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('results'))
    parser.add_argument('--language', choices=['zh', 'en'], default='en')
    args = parser.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    frame, checksum = load_data(Path(__file__).resolve().parent / 'data' / 'Misra1a.dat')
    grid = np.linspace(0, 4000, 401)
    states = [fit(frame, count, model, grid) for model in ['exponential', 'langmuir']
              for count in range(6, 15)]
    full = next(s for s in states if s['model'] == 'exponential' and s['count'] == 14)
    assert np.allclose([full['capacity'], full['scale']],
                       [238.94212918, .00055015643181], rtol=2e-8, atol=0)
    assert abs(full['rss'] - .12455138894) < 1e-10
    frame['fitted_volume'] = exponential(frame.pressure.to_numpy(), full['capacity'], full['scale'])
    frame['residual'] = frame.volume - frame.fitted_volume
    frame.to_csv(args.output / 'observations-and-fit.csv', index=False)
    data = {'pressure': frame.pressure.tolist(), 'volume': frame.volume.tolist(),
            'grid': grid.tolist(), 'states': states}
    (args.output / 'lab-data.json').write_text(json.dumps(data), encoding='utf8')
    summary = {'observations': len(frame), 'data_sha256': checksum,
               'units': {'pressure': 'recorded pressure unit, SI identity unspecified',
                         'volume': 'recorded volume unit, SI identity unspecified'},
               'exponential': {k: v for k, v in full.items()
                               if k not in ['prediction', 'mean_ci_half_width', 'residuals']},
               'langmuir_rss': states[-1]['rss'],
               'first_residual': float(frame.residual.iloc[0]),
               'observed_fraction_of_capacity': float(frame.volume.max()/full['capacity']),
               'states': len(states)}
    (args.output / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf8')
    figures(frame, states, grid, args.output, args.language)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
```

When reading the program, first follow data through `main`, then return to individual functions. `load_data` returns the named table and a checksum of the input bytes. `fit` accepts a point count and model name and returns parameters, residuals, intervals, and predictions. `figures` organizes already-computed quantities into views. The final `observations-and-fit.csv` retains pressure and observed volume and adds fitted volume and residual. Original observations and derived values remain neighbors in the same row, making inspection straightforward while preserving a starting point for another model.

For example, the predicted volume in the first row is approximately 9.986266. Subtracting it from the observed 10.07 gives residual 0.083734. Squaring all 14 residuals and summing gives 0.12455138894, matching NIST’s reference for the exponential model. A is approximately 238.942129 and k approximately 0.0005501564. Assertions in the program repeat these comparisons when it runs. Together they check that reading the file, defining the model, and solving the numerical problem have stayed connected. Reversed columns, a missing minus sign, or the wrong model function would break that connection.

## Reading residuals and relationships between parameters

The exponential parameter standard errors are approximately 2.7070 and 0.0000072669. They describe the sensitivity of the estimated parameters to observation variation under the current model and error assumptions. The program obtains a covariance matrix from a local linear approximation around the fitted solution. It propagates that covariance to predictions at each pressure and multiplies the resulting standard error by a t-distribution coefficient with the appropriate degrees of freedom. The shaded band is an approximate 95% interval for the mean response curve. Predicting a new individual measurement also requires accounting for that measurement’s own random variation, so a prediction interval is generally wider.

Two separate standard errors do not tell the whole story. The parameter correlation here is about −0.9988. Along one narrow direction, larger A and smaller k can still produce a curve close to the observations. The figure evaluates RSS over a grid of parameter combinations. Darker colors indicate smaller residual sums. Its horizontal coordinate is A and its vertical coordinate is k: each location represents a complete candidate curve, not one experimental observation. The long narrow valley makes parameter compensation visible and explains why retaining covariance or the complete fit record is valuable when reporting the parameters.

![Left: RSS evaluated across parameter combinations. Right: refits as higher-pressure observations are included; bars show one parameter standard error.](https://ml-biomat.com/static/tutorials/python-scientific/figures/f000fe37c35133d8c82ddce0.svg?v=f000fe37c351)

Figure 3Left: RSS evaluated across parameter combinations. Right: refits as higher-pressure observations are included; bars show one parameter standard error.

The residual plot also raises a question separate from numerical precision. The exponential fit produces grouped positive and negative residuals. Fitting the Langmuir function to the same 14 observations gives RSS approximately 0.0564193, compared with 0.1245514 for the exponential model. Both functions have two parameters. With the present equal weighting and pressure coverage, the Langmuir shape follows these volume observations more closely. Assessing its surface-site interpretation additionally involves temperature, equilibrium conditions, and surface information. The direct evidence in the fitted record is the size and pressure dependence of each model’s discrepancy from the observations.

This distinction explains how reproducing reference parameters and searching for a suitable materials model can both be productive. The first uses a fixed problem to check calculation; the second examines whether the problem formulation captures the experimental response. Scientific analysis requires both: solve the stated problem correctly, then use residuals to reconsider the chosen function when appropriate. A convergence message tells us that a numerical search has stopped. Pointwise residuals and the range of observations help us understand the curve it found.

## Expanding the pressure range and watching capacity change

Fit only the first six low-pressure observations, then progressively include higher-pressure points. This makes data coverage tangible: the observations remain unchanged, while the subset determining the parameters changes. The curve view always retains all 14 observations. Included points are colored and excluded points remain gray. The residual view shows how the current fit predicts observations that have not yet been included. Extending the displayed pressure axis to 4000 reveals the gradual divergence of the two function shapes beyond the measured range.

### See how coverage constrains a curve

[Figure: Curve, mean interval, and included and excluded observations](https://ml-biomat.com/tutorials/python-scientific/p29/en/#P29-curve)

[Figure: Residuals at all 14 observations](https://ml-biomat.com/tutorials/python-scientific/p29/en/#P29-residual)

[Figure: Capacity versus fitted pressure coverage](https://ml-biomat.com/tutorials/python-scientific/p29/en/#P29-path)

Orange points enter the fit; gray points remain for coverage comparison. Volume and pressure axes retain their recorded units.

Begin with the exponential model and six points. Observe the estimated A, then increase the count to fourteen while following the parameter path and gray residuals. At low pressure the curve is close to a straight line and mainly determines the initial slope, the product of A and k. Higher-pressure points add curvature information that helps distinguish a higher capacity with slower growth from a lower capacity with faster growth. Inferring the shape of a hill from a short stretch of road offers an analogy: local slope is relatively easy to observe, while a distant plateau requires a longer route to constrain its height.

Even with all observations included, the largest recorded volume, 81.78, is only about 34.2% of the exponential capacity estimate. The observations still lie on a visibly rising part of the curve. A further experiment aimed at capacity could extend pressure coverage within the material’s and apparatus’s operating conditions, look for a developing plateau, and repeat selected pressures to estimate volume variability. The value 4000 on the page is a mathematical extension of the displayed function. An experimental pressure limit would instead follow from material stability, equipment capability, and the research question. The comparison helps identify which part of the response needs additional measurement.

The 18 displayed states were actually fitted with SciPy by the downloadable example. The page selects the appropriate state for the chosen model and point count. Curves, residuals, the parameter path, and the fitted pressure range update together. Gray points remain observations already present in the dataset but excluded from the current fit. This experiment extends coverage along pressure rather than randomly separating training and test sets. It explores how parameters and extrapolation depend on the measured range; a particular state can be recorded and reproduced in Python.

## Preparing a result that another analysis can build on

A useful materials result allows a reader to locate the object of study, data range, mathematical definition, and key numerical findings together. Here a concise report could say: equal-weight least squares applied to the 14 pressure–volume observations in Misra1a gives A=238.9421, k=0.0005501564, and RSS=0.12455139 for the specified exponential model; a Langmuir fit to the same observations gives RSS=0.05641930. Parameters retain the recorded units, and the largest observed volume is approximately 34.2% of the exponential capacity estimate. These statements connect the calculation to the object and its interpretation and point naturally to the corresponding table and figures.

Keep original data unchanged, save predictions and residuals point by point, record parameter definitions in the summary, and retain coordinates, units, and interval meanings in figures. New pressure observations can then be added as new records and the analysis rerun, instead of manually adjusting a curve toward new points. If new measurements provide point-specific standard deviations, connect them to weighted fitting. If temperature becomes a main research variable, add it as an explicit table column, organize observations into isothermal conditions, and compare how parameters change with temperature. Each extension corresponds to a specific data field or model condition.

This project brings the libraries together in a real analysis: pandas preserves observation meaning, NumPy implements the model as array arithmetic, SciPy estimates parameters and local uncertainty, and Matplotlib shows broad trends alongside small departures. The enduring practice is to begin with an interpretable observation and connect it step by step to a model, a number, and a subsequent measurement. That gives a reader enough information to continue the analysis as well as understand its fitted curve.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P29.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [NIST StRD: Misra1a](https://www.itl.nist.gov/div898/strd/nls/data/misra1a.shtml)

   Fourteen observed adsorption values and certified results for the specified exponential model.

   NIST Standard Reference Database 140; free SRD with NIST SRD terms and source attribution.
2. [NIST SRD copyright and licensing](https://www.nist.gov/open/copyright-fair-use-and-licensing-statements-srd-data-software-and-technical-series-publications)

   Copyright and usage terms for Standard Reference Data.

   NIST official SRD terms; SRD is a distinct category under 15 USC 290e.
3. [SciPy curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

   Official use of parameter scaling, Jacobians, covariance, and nonlinear fitting.

   SciPy BSD-3-Clause; original chapter implementation.
4. [Langmuir (1918), The Adsorption of Gases on Plane Surfaces of Glass, Mica and Platinum](https://pubs.acs.org/jacsat/article/40/9/1361/430014/THE-ADSORPTION-OF-GASES-ON-PLANE-SURFACES-OF-GLASS)

   Historical context for surface sites and monolayer adsorption.

   Scientific historical citation; original explanatory diagram.
5. [NIST StRD background](https://www.nist.gov/itl/sed/statistical-reference-datasets/strd-background-information)

   Purpose of reference datasets in checking numerical statistical accuracy.

   Official NIST information.
