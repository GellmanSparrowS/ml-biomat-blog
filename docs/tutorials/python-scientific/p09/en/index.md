# Random Numbers and Measurement Variability

Source: https://ml-biomat.com/tutorials/python-scientific/p09/en/
Language: en

Repeat complete measurement procedures to distinguish random spread, fixed bias, and shared conditions.

## What does taking more measurements improve?

Repeatedly measure the same thin sheet with a thickness gauge and the display may vary around 1.18, 1.23, and 1.20 mm. Averaging sixteen readings usually produces a more stable result than selecting one reading. But if the instrument consistently reads 0.03 mm too high, repetition preserves that bias. This chapter uses NumPy to generate readings under explicitly defined rules and makes both effects visible. We compare averages of one, four, sixteen, and sixty-four readings, then add fixed bias and a shared session offset to identify which error component additional readings can reduce.

The example specifies a true sheet thickness of 1.20 mm and an individual-reading standard deviation of 0.04 mm. The program simulates 4000 experiments, each containing up to 64 readings. These are simulated values from a defined mathematical model. Specifying the truth and variation allows us to compare random outcomes with analytical relationships. In an actual experiment, the relevant variation would be estimated from the instrument, calibration records, and measurement conditions. Simulation first separates the mechanisms so their effects on an average can be understood individually.

Two counts have different meanings: readings within one experiment and simulated repetitions of the complete experiment. The first determines how many observations contribute to a particular mean. The second determines how clearly we can examine the distribution of possible means. Copying one sixteen-reading record 4000 times does not produce 4000 independent experiments. Here each row receives newly generated readings and represents a fresh measurement procedure. Defining these axes extends the preceding chapter’s habit of connecting array dimensions to the objects being studied.

## A random variable describes a possible reading

A random variable is a numerical rule for an outcome that has not yet been observed. Let X represent the next thickness reading; after measurement, it takes a particular value. To simulate that reading, we need a distribution describing which outcomes occur more or less frequently. This chapter adopts a normal distribution as its explicit teaching model. Values near the center are common, and values far from the center are less common. Measurement errors do not automatically follow a normal distribution merely because they come from an instrument; the distribution is a modeling choice.

Generate a standard normal value Z with center zero and standard deviation one, multiply it by 0.04 mm, and add 1.20 mm. Multiplication sets the fluctuation scale, while addition sets the center. If Z happens to be −0.5, the reading is 1.20−0.5×0.04=1.18 mm. If Z is 1.5, the reading is 1.26 mm. Z is dimensionless, while its multiplying scale has units of millimeters. This separation of distribution shape and physical scale keeps the interpretation clear when changing the instrument’s variability.

$$
X=\mu+\sigma Z,\qquad Z\sim\mathcal{N}(0,1)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/46833dd7644e5c60bb4525fe.svg) | One thickness reading, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | Specified distribution center, 1.20 mm here |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | Standard deviation of independent reading variation, 0.04 mm here |
| ![Formula](https://ml-biomat.com/static/agent-math/2ff8585a9cda3f4625f17d79.svg) | Standard-normal random value, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/be802d478d02bfa3ac2b08b1.svg) | Follows a normal distribution with mean 0 and variance 1; both parameters dimensionless |

Multiplying a standard draw by a length scale and adding the center gives a dimensional reading. For Z=−0.5, X=1.20+0.04×(−0.5)=1.18 mm.

A standard deviation describes distribution width, not a maximum permitted error. A scale of 0.04 mm does not confine every reading to 1.16–1.24 mm. Under this ideal normal model, that interval contains approximately 68% of the probability; more distant readings remain possible. Squaring the standard deviation gives the variance, whose units are mm². Variance is convenient when combining independent contributions. Taking its square root at the end restores the original measurement unit, making the resulting spread easier to interpret.

A histogram divides the thickness axis into intervals and counts the readings in each. With counts on the vertical axis, the bar heights sum to the number of readings. With probability density, the bar areas sum to one. This chapter uses density to compare sample distributions and theoretical curves in the same coordinates. Since the horizontal unit is mm, the vertical unit is mm⁻¹; multiplying them gives dimensionless probability. A density can exceed one when observations are concentrated within a narrow range. Probability is represented by area, not by the curve’s height at a single point.

$$
f(x)=\frac{1}{\sigma\sqrt{2\pi}}\exp\!\left[-\frac{(x-\mu)^2}{2\sigma^2}\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | A possible thickness value, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/93f888a1ee0b7da5e29f442f.svg) | Probability density, mm⁻¹; area over an interval gives probability |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | Normal-distribution center, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | Normal standard deviation, mm; strictly positive for this formula |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | Pi, approximately 3.14159, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/38c5da563ad696bdc123bf67.svg) | Exponential function with base e; u denotes its dimensionless bracketed argument |

With μ=1.20 mm and σ=0.04 mm, the exponent at x=1.20 mm is zero, giving 1/(0.04√(2π))≈9.974 mm⁻¹. Density may exceed 1 because probability accumulates density over a thickness interval. At σ=0 the distribution is concentrated at one point and this density formula is not used.

The exponent first measures displacement from the center in standard-deviation units, making its argument dimensionless, and then suppresses distant values. The factor in front adjusts the overall height so the full area is one. A smaller standard deviation makes the curve narrower and therefore taller. The increasingly high peaks in the averaging plots show precisely this redistribution of area. Histogram bin width also affects appearance. Shared binning or an explicit description of the bins helps distinguish a change in plotting choices from a change in the measurement model.

For a concrete histogram calculation, suppose 40 of 200 means fall in an interval 0.01 mm wide. The empirical probability of that interval is 40/200=0.20. On a density axis its height is 0.20/0.01=20 mm⁻¹. Although the height is 20, its area is 0.20. Halving the bin width redistributes observations among narrower bars and can change their heights, while the total histogram area remains one. This connects three common vertical-axis choices: counts, proportions, and densities.

## Make a random calculation repeatable and adjustable

The expression `rng = np.random.default_rng(2026)` creates a random-number generator object. It maintains an internal state and advances that state as values are drawn. The seed 2026 determines the starting state; it is a chosen integer with no statistical significance as a calendar year. The call `rng.normal(0, 1, size=(4000,64))` then creates a standard-normal array with 4000 rows and 64 columns. Its first arguments set center and standard deviation, while size sets the output shape. Passing a generator to functions keeps the source of randomness explicit.

These computer-generated values are pseudorandom: a deterministic algorithm produces them with statistical properties suitable for sampling. Repeating the same initialization and call sequence can reconstruct a simulation and make changes inspectable. Fixing a seed neither validates the chosen distribution nor forces a finite sample to have exactly the theoretical mean. A seed establishes the execution starting point. Measurement definitions, analytical relationships, and actual observations address whether the model answers the research question.

Creating another generator with the same seed restarts the same sequence. If a loop creates `default_rng(2026)` at the beginning of every simulated experiment, its rows can become identical, giving the appearance of many repetitions without new observations. Create a generator once and draw the required arrays, as this example does, or explicitly design multiple random streams. Call order matters too: drawing extra values earlier may alter later state. A reproducible calculation therefore retains the code and sampling shapes along with the seed.

The program records the NumPy version, actual bit-generator name, seed, and array sizes. It also saves the generated standard-normal values so parameter comparisons can reuse exactly the same draws. Algorithms and versions can evolve, so these details jointly describe a long-lived computational record. The browser experiment uses two sets of values generated by the complete Python program. Selecting a seed chooses a set; changing physical parameters reuses that set. This makes a parameter’s effect easier to distinguish from a newly sampled fluctuation.

## Monte Carlo turns possible experiments into computable objects

Monte Carlo methods simulate many possible processes according to probability rules and summarize their outcomes. In his first-person retrospective published in 1987, Metropolis described how statistical sampling developed alongside early electronic computing. His 1949 paper with Ulam, *The Monte Carlo Method*, presented the approach in the methodological literature. Electronic computers made large collections of simulated histories practical, allowing samples to investigate problems that were difficult to solve directly. The same organizing idea appears here: repeat a complete procedure and study the distribution of its results.

![Original Monte Carlo process diagram: sixteen readings and a mean for the first eight experiments, then a distribution of 4000 means. All values are simulated from the specified normal model.](https://ml-biomat.com/static/tutorials/python-scientific/figures/d0f5396f01429f87cd917ee8.svg?v=d0f5396f0142)

Figure 1Original Monte Carlo process diagram: sixteen readings and a mean for the first eight experiments, then a distribution of 4000 means. All values are simulated from the specified normal model.

The upper panels expose the first eight simulated experiments. Each row contains sixteen readings; color shows the displacement from the specified truth in micrometers, and the adjacent bar shows that row’s mean displacement. Because 1 mm equals 1000 μm, the individual fluctuation scale of 0.04 mm corresponds to 40 μm. Averaging positive and negative deviations often leaves a smaller mean deviation. The lower panel collects all 4000 row means. It describes how the average could vary if the full sixteen-reading experiment were performed again.

The construction does not turn repeated measurements into additional independent specimens. It simulates new measurement procedures at the same true thickness, initially with independent reading fluctuations within each procedure and fresh draws between procedures. Studying manufacturing differences among sheets would require another component describing differences in their true thicknesses and an axis identifying sheets. A larger random array cannot replace a definition of the experimental unit. Its dimensions gain statistical meaning from the process that generated their entries.

Common random draws are useful for comparing parameters. Adding 0.03 mm to every reading must add 0.03 mm to each experimental mean. Keeping the original fluctuations lets us verify that shift one experiment at a time. Generating new fluctuations after every parameter change would mix the parameter effect with fresh sampling variation. Here we first hold draws fixed to inspect a mechanism, then choose another seed to see whether the same pattern persists. These operations serve different purposes: paired parameter comparison and examination of sampling variability.

## Why an average is more stable

A mean adds the n readings in one experiment and divides their sum by n. When readings have the same center and variance and are mutually independent, the variance of their sum is the sum of their variances. Dividing the sum by n divides its variance by n², leaving the individual variance divided by n. Taking the square root gives the standard deviation of the mean, also called its standard error: individual standard deviation divided by √n. This explains both the square root and the role of independence. Readings that move together introduce covariance terms and change the variance of the sum.

$$
\bar X_r=\frac{1}{n}\sum_{j=1}^{n}X_{rj},\qquad \operatorname{SD}(\bar X)=\frac{\sigma}{\sqrt n}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a934d6a2da636a96d533bf97.svg) | Reading j of complete experiment r, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/945c1a122d82e7eb08609a35.svg) | Mean thickness of experiment r, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/c9b8c7a8cde7033169f76cde.svg) | Experiment and reading indices, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Positive integer number of readings per experiment, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/67b782d816a5bbd0406cf935.svg) | Sum the n readings within one experiment |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | Finite standard deviation of independent, identically distributed readings, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/e7f0c1878f989135224d5a4c.svg) | Standard deviation of mean thickness across complete repeated experiments, mm |

Independent readings have summed variance nσ². Dividing by n divides variance by n², leaving σ²/n. Its square root is the standard error. At σ=0.04 mm and n=16, 0.04/4=0.01 mm.

With an individual standard deviation of 0.04 mm, averages of four readings have standard deviation 0.02 mm; averages of sixteen have 0.01 mm; averages of sixty-four have 0.005 mm. Halving this fluctuation scale requires four times as many independent readings, rather than twice as many. The right panel uses logarithmic coordinates so equal ratios occupy equal distances, while labels still show actual reading counts and millimeters. The left panel places all four mean distributions over the same thickness range, expressing the reduction directly through their widths.

![Step lines show simulated density histograms; smooth lines show analytical normal densities. Right-hand points are observed standard deviations across 4000 simulations.](https://ml-biomat.com/static/tutorials/python-scientific/figures/28082d3cf644f00b30e17958.svg?v=28082d3cf644)

Figure 2Step lines show simulated density histograms; smooth lines show analytical normal densities. Right-hand points are observed standard deviations across 4000 simulations.

The simulation yields standard deviations of approximately 0.040070, 0.020117, 0.010034, and 0.004980 mm. They are close to the analytical values but need not equal them exactly. The 4000 simulated means are themselves a finite sample, so their estimated spread fluctuates. Increasing the number of simulated experiments estimates that distribution more steadily. Increasing the number of readings within an experiment changes the mean distribution being studied. These are different ways of doing more work; separating them prevents computational repetition from being confused with improved measurement precision.

Under the independent normal model used here, the mean is itself exactly normally distributed; a very large n is unnecessary for that result. More generally, means of independent, identically distributed observations with finite variance approach a normal distribution under the corresponding central-limit conditions as n grows. The square-root relationship for the mean’s standard deviation does not itself require the original observations to be normal. Keeping normality, independence, and finite variance separate helps identify what needs revision when observations are skewed or correlated.

A smaller standard error describes a distribution over repeated experiments. It does not guarantee that every additional reading moves one particular cumulative mean closer to the truth. The next reading may move the current mean inward or outward. The situation resembles a coin-toss proportion that tends toward balance overall while individual tosses still move it in either direction. The claim concerns a narrowing range of possible averages. One result that happens to land near the center does not replace examination of the distribution.

The standard deviation of the readings and the standard error of their mean also answer different questions. The former describes how much individual readings vary; the latter describes how much an average varies between repetitions of the complete experiment. Reporting the latter as though it were the spread of individual measurements makes the observations appear more tightly clustered than they are. Before drawing an error bar, identify whether its unit of repetition is a reading, a session mean, or a separate specimen. The same unit, millimeters, does not make these quantities interchangeable.

## Why fixed bias and shared offsets remain in an average

First add a fixed 0.03 mm to every reading. Regardless of the number averaged, that term remains in the mean. The sixteen-reading mean distribution moves from around 1.20 to around 1.23 mm while retaining a standard deviation near 0.01 mm. Close agreement among repeated results describes repeatability; displacement of the center from the specified truth describes the added fixed bias. The example makes width and center separately observable, so a tidy cluster of readings does not automatically imply accurate calibration.

Now consider an offset introduced by mounting or zero adjustment at the beginning of each measurement session. It affects every reading in that session equally but changes when a new session begins. Give this shared component a standard deviation of 0.03 mm. The sixteen readings within a session shift together. Each still has its independent 0.04 mm fluctuation, but repeatedly reading under the same shared condition does not cancel the common offset. Here a session means a set of measurements sharing a mounting or zero condition.

$$
X_{rj}=\mu+b+\sigma Z_{rj}+\tau U_r,\qquad \operatorname{SD}(\bar X)=\sqrt{\frac{\sigma^2}{n}+\tau^2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a934d6a2da636a96d533bf97.svg) | Reading j in session r, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | Specified true thickness, 1.20 mm |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Fixed bias shared by all readings, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/ca41d625ee47e9b98c95d9a8.svg) | Independent reading standard deviation, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/9eaf25a888dbfdc9822c18d9.svg) | Independent standard-normal variable for each reading, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/cc8fa09795c279ec6e225353.svg) | Standard deviation of the shared offset between sessions, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/efc46a95815086e114611e76.svg) | Standard-normal variable shared within session r, dimensionless; independent of all Z and other sessions |
| ![Formula](https://ml-biomat.com/static/agent-math/fafca02cde4303b92d177576.svg) | Session index, reading index, and readings per session, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/e7f0c1878f989135224d5a4c.svg) | Standard deviation of session means when sessions are repeated, mm |

Averaging retains the common term τU_r. Fixed bias b shifts the center without changing standard deviation. With σ=0.04 mm, τ=0.03 mm, n=16, √(0.0016/16+0.0009)=0.0316228 mm.

With sixteen readings, the independent component contributes a mean standard deviation of 0.01 mm, while the shared component contributes 0.03 mm. Because the two components are independent in the model, add their variances and then take a square root, obtaining approximately 0.031623 mm. Adding the standard deviations directly would incorrectly give 0.04 mm. Across 4000 simulated experiments, the observed standard deviation is approximately 0.031028 mm, differing because of finite sampling. The right panel increases the number of readings within the same session: the independent contribution shrinks, while the shared component retains its 0.03 mm scale.

![Fixed bias shifts the mean distribution. A shared session offset broadens it and remains when readings within that session are averaged.](https://ml-biomat.com/static/tutorials/python-scientific/figures/a7111bc2f81d4cbbe63d874e.svg?v=a7111bc2f81d)

Figure 3Fixed bias shifts the mean distribution. A shared session offset broadens it and remains when readings within that session are averaged.

This distinction informs experimental design. If common mounting conditions dominate variation, taking more readings under one mounting and repeating the mounting procedure provide different information. Independent sessions help estimate between-session variation. Calibration records help identify fixed bias. Repeated readings within a session reveal short-term reading fluctuations. Retain session, specimen, and reading identifiers so these levels can later be summarized separately. They are complementary parts of a measurement design rather than interchangeable counts of repeated work.

The model makes both individual fluctuations and session offsets normal, with an identical shared effect on all readings in a session. Actual measurements may instead show gradually increasing drift, correlations that decay with time separation, or occasional outliers. Time-ordered residual plots, calibration experiments, and measurement steps help select an appropriate model. The fully shared offset provides a clear first example of how dependence changes averaging; it does not merge all forms of correlation into the same mechanism.

## The complete simulation and its actual outputs

The complete program separates standard random values from physical parameters. It generates a 4000-by-64 array of independent standard-normal draws, followed by a 4000-by-1 array of session draws. The singleton column broadcasts along each experiment’s reading direction. Each choice of n uses the first n readings of the same row, making the four designs paired comparisons. Within each design there are still 4000 freshly generated experiments. Plain Python summation and squared deviations independently check NumPy’s means and sample standard deviations.

### Complete program: readings, mean distributions, and error mechanisms

Saves generated arrays, two interactive draw sets, numerical summaries, and three figures.

```
"""Simulate repeated thickness readings and distinguish noise, bias, and shared offsets."""
from pathlib import Path
import argparse
import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

MU=1.2
SIGMA=.04
TRIALS=4000
MAX_READINGS=64

def draws(seed):
    rng=np.random.default_rng(seed)
    individual=rng.normal(0,1,size=(TRIALS,MAX_READINGS))
    common=rng.normal(0,1,size=(TRIALS,1))
    return individual,common,type(rng.bit_generator).__name__

def scalar_sd(values):
    average=math.fsum(float(v) for v in values)/len(values)
    return math.sqrt(math.fsum((float(v)-average)**2 for v in values)/(len(values)-1))

def density(x,center,sd):
    return np.exp(-.5*((x-center)/sd)**2)/(sd*np.sqrt(2*np.pi))

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('output'));p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    z,c,bitgen=draws(2026);readings=MU+SIGMA*z
    sizes=[1,4,16,64];means={n:readings[:,:n].mean(axis=1) for n in sizes}
    empirical={n:float(means[n].std(ddof=1)) for n in sizes};theory={n:SIGMA/math.sqrt(n) for n in sizes}
    shared_means=(MU+SIGMA*z[:,:16]+.03*c).mean(axis=1)
    biased_means=means[16]+.03
    assert np.allclose(means[16],[math.fsum(float(x) for x in row)/16 for row in readings[:,:16]])
    for n in sizes:assert math.isclose(empirical[n],scalar_sd(means[n]),rel_tol=1e-12)
    assert math.isclose(float(biased_means.std(ddof=1)),empirical[16],rel_tol=1e-12)
    assert math.isclose(float(biased_means.mean()-means[16].mean()),.03,abs_tol=1e-12)
    zh=args.language=='zh';tr=lambda a,b:a if zh else b;colors=['#28648a','#467a62','#b85336','#7b5c90']
    fonts={f.name for f in font_manager.fontManager.ttflist};family=next((f for f in ['Microsoft YaHei','Noto Sans CJK SC','DejaVu Sans'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[family,'DejaVu Sans'] if zh else ['DejaVu Sans','Arial'],'font.size':12,'axes.titlesize':14,'axes.titleweight':'bold','axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','text.color':'#172b36'})
    def save(fig,n):
        fig.savefig(args.output/f'{n}-{args.language}.svg',bbox_inches='tight');fig.savefig(args.output/f'{n}-{args.language}.png',dpi=170,bbox_inches='tight');plt.close(fig)

    fig=plt.figure(figsize=(12.5,7.8),layout='constrained');gs=fig.add_gridspec(2,2,width_ratios=[3,1],height_ratios=[1,.85]);ax=fig.add_subplot(gs[0,0]);dev=1000*(readings[:8,:16]-MU);im=ax.imshow(dev,cmap='RdBu_r',vmin=-100,vmax=100,aspect='auto');ax.set(xticks=np.arange(0,16,3),xticklabels=np.arange(1,17,3),yticks=range(8),yticklabels=np.arange(1,9),xlabel=tr('同一次实验里的读数编号','Reading number within an experiment'),ylabel=tr('重新开展的实验编号','Repeated experiment'),title=tr('a  蒙特卡洛：按同一规则生成许多完整实验','a  Monte Carlo: generate complete repeated experiments'));fig.colorbar(im,ax=ax,pad=.02).set_label(tr('读数减去真值 / μm','Reading minus truth / μm'))
    im.set_clim(-20*math.ceil(float(np.abs(dev).max())/20),20*math.ceil(float(np.abs(dev).max())/20))
    ax=fig.add_subplot(gs[0,1]);ax.barh(np.arange(8),1000*(means[16][:8]-MU),color=colors[0]);ax.set_ylim(7.5,-.5);ax.axvline(0,color='#607078',lw=1);ax.set(yticks=np.arange(8),yticklabels=np.arange(1,9),xlabel=tr('均值偏离 / μm','Mean offset / μm'),title=tr('b  每行得到一个均值','b  One mean per row'))
    ax=fig.add_subplot(gs[1,:]);ax.hist(means[16],bins=np.arange(1.15,1.251,.004),density=True,color=colors[0],alpha=.4,edgecolor='#fbfaf6');xx=np.linspace(1.15,1.25,500);ax.plot(xx,density(xx,MU,.01),color=colors[0],lw=2.2,label=tr('模型：均值标准差0.01 mm','Model: mean SD 0.01 mm'));ax.axvline(MU,color='#172b36',ls='--',label=tr('设定真值1.20 mm','Specified truth 1.20 mm'));ax.set(xlabel=tr('每次16个读数的平均厚度 / mm','Mean thickness of 16 readings / mm'),ylabel=tr('概率密度 / mm⁻¹','Probability density / mm⁻¹'),title=tr('c  4000个模拟均值形成分布；上图只展示前8次','c  Distribution of 4000 simulated means; above shows the first 8'));ax.legend(fontsize=11);ax.grid(alpha=.1)
    save(fig,'monte-carlo-history')

    fig=plt.figure(figsize=(12.5,6.7),layout='constrained');gs=fig.add_gridspec(1,2,width_ratios=[1.4,1]);ax=fig.add_subplot(gs[0]);bins=np.arange(.99,1.411,.005);xx=np.linspace(1,1.4,700)
    for n,col in zip(sizes,colors):ax.hist(means[n],bins=bins,density=True,histtype='step',lw=1.5,color=col,alpha=.6);ax.plot(xx,density(xx,MU,theory[n]),color=col,lw=2,label=f'n = {n}')
    ax.set(xlabel=tr('一次实验的平均厚度 / mm','Mean thickness in one experiment / mm'),ylabel=tr('概率密度 / mm⁻¹','Probability density / mm⁻¹'),xlim=(1.04,1.36),title=tr('a  读数越多，均值分布越窄','a  More readings narrow the mean distribution'));ax.legend();ax.grid(alpha=.12)
    ax=fig.add_subplot(gs[1]);nn=np.arange(1,65);ax.plot(nn,SIGMA/np.sqrt(nn),color=colors[0],lw=2,label=tr('解析关系 σ/√n','Analytical σ/√n'));ax.scatter(sizes,[empirical[n] for n in sizes],s=65,color=colors[2],zorder=3,label=tr('4000次模拟的标准差','SD across 4000 simulations'));ax.set_xscale('log',base=2);ax.set_yscale('log',base=2);ax.set_xticks([1,4,16,64],[1,4,16,64]);ax.set_yticks([.005,.01,.02,.04],['0.005','0.010','0.020','0.040']);ax.set(xlabel=tr('每次实验的读数数目 n','Readings per experiment n'),ylabel=tr('均值标准差 / mm','Standard deviation of the mean / mm'),title=tr('b  四倍读数，使标准差减半','b  Four times as many halves the SD'));ax.legend(loc='lower left',fontsize=10);ax.grid(alpha=.15)
    save(fig,'averaging-distributions')

    fig=plt.figure(figsize=(12.5,7),layout='constrained');gs=fig.add_gridspec(1,2,width_ratios=[1.35,1]);ax=fig.add_subplot(gs[0]);xx=np.linspace(1.05,1.4,600)
    scenarios=[(means[16],MU,.01,colors[0],tr('独立噪声','Independent noise')),(biased_means,MU+.03,.01,colors[2],tr('再加固定偏差0.03 mm','Add fixed bias 0.03 mm')),(shared_means,MU,math.sqrt(.001),colors[1],tr('会话偏移标准差0.03 mm','Session offset SD 0.03 mm'))]
    for values,center,sd,col,label in scenarios:ax.hist(values,bins=np.arange(1.04,1.411,.005),density=True,histtype='step',color=col,alpha=.5);ax.plot(xx,density(xx,center,sd),color=col,lw=2,label=label)
    ax.axvline(MU,color='#172b36',ls='--',lw=1.5);ax.set(xlabel=tr('16个读数的平均厚度 / mm','Mean thickness of 16 readings / mm'),ylabel=tr('概率密度 / mm⁻¹','Probability density / mm⁻¹'),xlim=(1.08,1.35),title=tr('a  分布变窄，与中心正确是两件事','a  A narrow distribution can have a shifted center'));ax.legend(fontsize=10);ax.grid(alpha=.12)
    ax=fig.add_subplot(gs[1]);nn=np.arange(1,257);ax.plot(nn,SIGMA/np.sqrt(nn),color=colors[0],lw=2,label=tr('只有独立噪声','Independent noise only'));ax.plot(nn,np.sqrt(SIGMA**2/nn+.03**2),color=colors[1],lw=2,label=tr('加会话共有偏移','With shared session offset'));ax.axhline(.03,color=colors[1],ls=':',label=tr('共有部分：0.03 mm','Shared component: 0.03 mm'));ax.set_xscale('log',base=2);ax.set_xticks([1,4,16,64,256],[1,4,16,64,256]);ax.set(xlabel=tr('同一会话的读数数目 n','Readings within one session n'),ylabel=tr('均值标准差 / mm','Standard deviation of the mean / mm'),ylim=(0,.055),title=tr('b  重复读数无法消除共有偏移','b  Repeated readings retain a shared offset'));ax.legend(fontsize=10);ax.grid(alpha=.12);save(fig,'bias-and-shared-offset')
    lab={}
    for seed in [2026,2027]:
        zi,ci,_=draws(seed);lab[str(seed)]={'individual':zi[:200].tolist(),'common':ci[:200,0].tolist()}
    (args.output/'lab-draws.json').write_text(json.dumps(lab,separators=(',',':')),encoding='utf8')
    np.savez_compressed(args.output/'simulation.npz',individual_standard=z,session_standard=c,readings_mm=readings)
    summary={'model':{'true_thickness_mm':MU,'individual_sd_mm':SIGMA,'trials':TRIALS,'maximum_readings':MAX_READINGS,'seed':2026,'bit_generator':bitgen,'numpy_version':np.__version__},'mean_sd':{str(n):{'empirical_mm':empirical[n],'analytic_mm':theory[n],'mean_mm':float(means[n].mean())} for n in sizes},'n16_scenarios':{'unbiased':{'mean_mm':float(means[16].mean()),'sd_mm':empirical[16]},'fixed_bias':{'mean_mm':float(biased_means.mean()),'sd_mm':float(biased_means.std(ddof=1))},'shared_offset':{'mean_mm':float(shared_means.mean()),'sd_mm':float(shared_means.std(ddof=1)),'analytic_sd_mm':math.sqrt(.001)}},'first_trial_n16_mean_mm':float(means[16][0]),'first_trial_readings_mm':readings[0,:16].tolist()}
    (args.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary['mean_sd'],indent=2));print(json.dumps(summary['n16_scenarios'],indent=2))

if __name__=='__main__':main()
```

The numerical summary records model parameters, version, bit generator, four mean standard deviations, and three error scenarios. For sixteen readings, the average across 4000 experimental means is approximately 1.200244 mm. Adding fixed bias changes it to 1.230244 mm while preserving the distribution standard deviation, approximately 0.010034 mm. With shared offsets, the overall average is approximately 1.200503 mm but the distribution is substantially wider. These outputs distinguish location from spread and can be recalculated from the saved arrays.

The file `simulation.npz` stores standard random arrays and complete readings, while `summary.json` stores readable numerical summaries. The three figures explain repeated experiments, averaging counts, and error mechanisms. Retained draws allow another calculation to compare the same sampled cases. The code’s `ddof=1` computes a sample standard deviation across 4000 experimental means. That empirical spread differs in role from the model’s directly specified individual-reading standard deviation of 0.04 mm.

The mean is taken along axis 1 because that axis contains readings within an experiment. The expression `readings[:,:16].mean(axis=1)` reduces each row to one result and returns 4000 means, one per complete experiment. Using axis 0 would instead return sixteen results, each averaging the same reading position across experiments. That answers a different question and does not produce the required distribution of experimental means. The later standard deviation summarizes the one-dimensional collection of 4000 means, so the two stages act on clearly distinguished statistical objects.

## Adjust repetition, independent fluctuation, and shared conditions separately

The experiment uses 200 simulated experiments generated by the Python program, each with up to 64 standard draws. Select one experiment to inspect its readings and mean in the scatter plot. The adjacent histogram displays all 200 means. Change the reading count to compare analytical standard error with the observed distribution width. Add fixed bias to move the center, then add session variation to see why the distribution remains wide. All parameters have explicit units, and plots and summaries are calculated from the same values.

### Experiment: which variation does averaging reduce?

200 complete simulated experiments. Keep standard draws fixed while changing parameters; select another seed to inspect new draws.

[Figure: Readings and mean of one experiment](https://ml-biomat.com/tutorials/python-scientific/p09/en/#P09-readings)

[Figure: 200 means and their analytical distribution](https://ml-biomat.com/tutorials/python-scientific/p09/en/#P09-distribution)

Begin with independent standard deviation 0.04 mm and both other components zero. Change from four readings to sixteen and verify that the analytical standard error falls from 0.02 to 0.01 mm. Keep sixteen readings and add fixed bias 0.03 mm: every mean shifts, while their spread stays the same. Restore zero bias and add session standard deviation 0.03 mm, then examine the variation remaining with sixty-four readings. These comparisons point to distinct experimental actions: collect independent readings, calibrate the center, and control or independently repeat shared conditions.

The browser retains the first 200 simulated experiments for individual inspection, while the chapter figures use all 4000. Their empirical standard deviations can therefore differ slightly. The analytical standard error depends only on the model parameters and reading count. Compare both seeds to observe this difference while checking that the analytical value remains unchanged. More simulated repetitions stabilize the estimated distribution; a new seed exposes the sampling variation already present in that estimate.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P09.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [NumPy — Random Generator](https://numpy.org/doc/2.4/reference/random/generator.html)

   Generators, seeds, and output shapes

   BSD-3-Clause
2. [NumPy — Generator.normal](https://numpy.org/doc/2.4/reference/random/generated/numpy.random.Generator.normal.html)

   Normal sampling parameters and interface

   BSD-3-Clause
3. [NumPy — Random compatibility policy](https://numpy.org/doc/2.4/reference/random/compatibility.html)

   Version, call sequence, and random-stream reproducibility

   BSD-3-Clause
4. [NIST/SEMATECH — Normal Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3661.htm)

   Statistical definitions of density, location, and standard deviation

   US government handbook; factual reference
5. [N. Metropolis — The Beginning of the Monte Carlo Method (1987)](https://mcnp-green.lanl.gov/pdf_files/Article_1987_LAS_Metropolis_125--130.pdf)

   First-person history of statistical sampling and early electronic computing

   Public LANL archival article; factual paraphrase and original figures
