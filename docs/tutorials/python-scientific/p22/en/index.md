# Statistical Reasoning from Finite Samples

Source: https://ml-biomat.com/tutorials/python-scientific/p22/en/
Language: en

Connect observations, sampling distributions, and confidence intervals through the same traceable data.

## What do ten measured specimens tell us about the rest?

Suppose a material property usually varies around 20 kPa. Ten specimens give a mean of 18.65 kPa. The difference is worth examining, but it first raises a sampling question: has the population level changed, or did these ten specimens happen to be low? Statistical methods incorporate what could happen if another group were sampled. They connect the observed table to the population that the table is intended to represent.

We use a fully specified teaching population: independent readings follow a normal distribution with mean 20 kPa and standard deviation 4 kPa. Its bell-shaped density makes readings near 20 more common and distant readings less common. The program generates 200 groups of up to 50 specimens. Known population parameters let us inspect the estimation procedure directly. Within each group, however, both the mean and the spread are estimated from that group's observations.

SciPy will calculate standard errors, t confidence intervals, and one-sample t tests. Each result will be interpreted alongside the original readings. Three objects need to remain distinct: variation among specimens, variation of sample means across repeated sampling, and an interval estimating the population mean. Their separation gives the statistical output a clear connection to the scientific question.

## Decide what one observation represents

Measuring one specimen three times differs from measuring three independent specimens once each. The former mainly reveals measurement variation on that specimen; the latter also captures variation between specimens. For a population of materials, an independently prepared specimen is often the relevant sampling unit. Counting repeated readings from one specimen as independent specimens enlarges the apparent sample size and can make uncertainty in the mean look too small.

The array has 200 rows and 50 columns. Each row is an independent sampling experiment, and each column contains one independent specimen reading within that experiment. To examine groups of ten, take the first ten columns and average across columns. For groups of thirty, keep those ten and add twenty more. Sample sizes within one row are therefore nested and comparable; different rows remain independently generated sampling experiments.

A fixed random seed makes the 200 groups reproducible, ensuring that the text, figures, and interaction use the same numbers. It fixes a simulated dataset, while the statistical population remains the specified normal model. Another seed would give another collection of samples and slightly different observed coverage. The long-run behavior of a method concerns many possible samples, rather than a privileged choice of seed.

In actual research, sampling must also match the target population. Choosing only easily reached locations may miss spatial differences within a batch. A sampling plan can instead specify locations, batch proportions, and independently prepared units, retaining this information in the table. More rows increase the amount of recorded data, while more relevant independent information improves estimation of the intended population.

Independence can be understood through a ruler that is shifted for everyone. If a calibration error raises all readings together, averaging many readings does not automatically cancel that shared shift. The square-root reduction in standard error relies on independent random variation. Shared batches, repeated measurements on one specimen, and common time-period effects need representation through design, calibration, or a suitable model. Understanding the sources of error therefore matters more than applying the same formula to an ever-larger row count.

## Standard deviation describes specimens; standard error describes a mean

Begin with five readings that are easy to check: 16, 18, 20, 22, and 24 kPa. Their mean is 20 kPa. Deviations from the mean are −4, −2, 0, 2, and 4 kPa, whose squares sum to 40 kPa². Dividing by the sample size minus one, or 4, gives a sample variance of 10 kPa². Its square root is a standard deviation of approximately 3.1623 kPa, describing dispersion of the specimens around their common sample mean.

$$
\bar x=\frac{1}{n}\sum_{i=1}^{n}x_i,\qquad s=\sqrt{\frac{\sum_{i=1}^{n}(x_i-\bar x)^2}{n-1}},\qquad \mathrm{SEM}=\frac{s}{\sqrt n}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/10c16af3229388fdcbca3de7.svg) | Reading from independent specimen i, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/9ec0d2298548e930111bc32b.svg) | i is a specimen index and n the number of independent specimens; both dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/7e33236199f3df8d334ffd7f.svg) | Sample mean, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | Sample standard deviation, kPa; divisor n−1 estimates population variance. |
| ![Formula](https://ml-biomat.com/static/agent-math/dd3305e34ff527725a7a82ea.svg) | Estimated standard error of a mean under independent identically distributed sampling, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/e8ca563c8033303e110f807c.svg) | Summation and nonnegative square root. Squared deviations have units kPa²; taking the root returns kPa. |

For 16, 18, 20, 22, and 24 kPa, the mean is 20 and squared deviations sum to 40 kPa². Thus s = √(40/4) = √10 ≈ 3.162278 kPa and SEM = √10/√5 = √2 ≈ 1.414214 kPa. The first describes individual spread; the second estimates variation among repeated-sample means.

The standard error divides that standard deviation by the square root of sample size. It is approximately 1.4142 kPa here. Under independent, identically distributed sampling, this estimates the scale on which a sample mean varies. High and low specimen readings partly cancel during averaging, making means more stable than individual readings. Increasing sample size fourfold roughly halves the standard error when population variability remains similar, illustrating the substantial effort often needed to improve precision.

![The same normal teaching population: ten independent readings in the first group appear at left; 200 group means form the histogram at right with 0.5 kPa bins. Red identifies the left-hand group mean.](https://ml-biomat.com/static/tutorials/python-scientific/figures/9695ac7ad0de2a2e67f6d584.svg?v=9695ac7ad0de)

Figure 1The same normal teaching population: ten independent readings in the first group appear at left; 200 group means form the histogram at right with 0.5 kPa bins. Red identifies the left-hand group mean.

The left panel shows ten original readings from one group; the right shows means from all 200 groups. Their vertical axes have different roles: the left still measures kPa, while the right counts groups whose means fall in a given interval. Compressing the left-hand group into one mean makes it contribute one position to the right-hand distribution. This transformation from one group to one summary is the entry point to a sampling distribution.

`stats.sem` uses `ddof=1` by default. NumPy's `std` instead defaults to `ddof=0`, so that parameter must be set explicitly to reproduce the calculation above. It determines the divisor applied to squared deviations and reflects whether the calculation describes all the values at hand or estimates a population variance from a limited sample.

The sample standard deviation changes between experiments too. A group that happens to contain many readings close to its mean produces a smaller estimated spread and standard error. A more dispersed group produces larger values. Although the simulated population standard deviation is fixed at 4 kPa, the estimates from individual groups need not equal 4. Interval width therefore depends both on sample size and on the observations actually obtained; n alone cannot specify the exact length of every interval.

## Student's small-sample problem: the spread is estimated too

The 1908 paper *The Probable Error of a Mean*, published under the name Student, addressed a central difficulty: with few observations, the sample mean varies, and the standard deviation used to judge that variation is itself unstable. Its introduction places the problem among chemical, biological, and agricultural experiments that are difficult to repeat extensively. Small material batches pose the same practical issue: limited data must locate a center and provide a scale for judging that center.

If the population standard deviation were known precisely, it could directly scale a mean's departure from a reference. Research commonly substitutes a sample standard deviation. The denominator then varies with the sample, producing heavier tails in the standardized statistic. The t distribution accounts for this additional variation. Its degrees of freedom are the sample size minus one in the present problem. With more observations, the estimate of spread stabilizes and the t distribution approaches the standard normal.

![Student’s small-sample problem shown through densities and critical multipliers. Each left-hand density integrates to 1; red tails mark a combined 5% for 4 degrees of freedom. The right panel uses SciPy quantiles for 95% intervals.](https://ml-biomat.com/static/tutorials/python-scientific/figures/4b2e1fd86bf627f9f778fe1d.svg?v=4b2e1fd86bf6)

Figure 2Student’s small-sample problem shown through densities and critical multipliers. Each left-hand density integrates to 1; red tails mark a combined 5% for 4 degrees of freedom. The right panel uses SciPy quantiles for 95% intervals.

Areas under these density curves represent probabilities; a curve's height at one point is not the probability of that exact value. The red t curve has four degrees of freedom, corresponding to five independent observations, and heavier tails than the dashed normal curve. Containing the middle 95% requires limits of approximately ±2.776 for this t distribution, compared with ±1.960 for the standard normal. Multiplying by the same standard error therefore produces a wider interval.

The loss of one degree of freedom has a simple explanation. Once the sample mean is fixed, the deviations from that mean must sum to zero. Knowing four of five deviations determines the fifth, leaving four independently varying deviations. Mean and spread are thus estimated from the same finite information, which is exactly the issue motivating the small-sample adjustment.

## A confidence interval is a rule used across repeated samples

A mean gives a central estimate, and a confidence interval displays its precision. For independent normal observations with unknown population variance, extend the sample mean in both directions by a t critical multiplier times the standard error. Greater specimen dispersion increases the standard error and widens the interval. More independent observations generally reduce the standard error, while the critical multiplier also moves toward its normal-distribution value.

$$
\mathrm{CI}_{1-\alpha}=\left[\bar x-q_{1-\alpha/2,n-1}\frac{s}{\sqrt n},\;\bar x+q_{1-\alpha/2,n-1}\frac{s}{\sqrt n}\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ef3c902b8343b9c13d7ced08.svg) | Population-mean interval with confidence level 1−α; both endpoints are in kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | Combined tail probability, dimensionless; 0.05 for a 95% interval. |
| ![Formula](https://ml-biomat.com/static/agent-math/a8d6097212e39d5151b95ed9.svg) | Quantile at cumulative probability 1−α/2 of a t distribution with n−1 degrees of freedom, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/91dad9a192a1a10a4a3490bc.svg) | Sample mean and standard deviation in kPa; n is a dimensionless independent-specimen count. |

For the five-point example, n = 5 and α = 0.05 give q ≈ 2.776445. Multiplying by SEM = √2 kPa gives a half-width of 3.926486 kPa, so the interval is [16.073514, 23.926486] kPa. Each tail contains 2.5% reference probability, hence the 0.975 quantile.

For the five hand-calculated readings, the 95% half-width is 2.776445 multiplied by 1.414214, or approximately 3.926486 kPa. The interval therefore runs from approximately 16.073514 to 23.926486 kPa. Its target is the population mean. Predicting the next specimen requires accounting for specimen-level variability as well, using a prediction interval or another appropriate calculation. An interval for a mean narrows with more data even though individual specimens continue to vary.

The 95% level describes the repeated sampling and interval construction rule. If the same conditions were repeatedly used to draw new samples and calculate new intervals, about 95% of those intervals would cover the fixed population mean in the long run. The observed interval is one realization of that rule. In the figure, a vertical line always marks the same population mean, 20 kPa; sample-dependent interval centers and widths move around it.

![The first 40 groups show 95% t intervals against the fixed mean of 20 kPa; red intervals miss that value. Coverage at right uses all 200 groups for each sample size. Sample sizes share prefixes within each row.](https://ml-biomat.com/static/tutorials/python-scientific/figures/a7e824212c384a7d8205415b.svg?v=a7e824212c38)

Figure 3The first 40 groups show 95% t intervals against the fixed mean of 20 kPa; red intervals miss that value. Coverage at right uses all 200 groups for each sample size. Sample sizes share prefixes within each row.

For groups of ten in the fixed dataset, 188 of the 200 nominal 95% intervals cover 20 kPa, an observed coverage of 94%. A theoretical confidence level and the fraction in a finite simulation can differ, just as 200 coin tosses need not give exactly 100 heads. Raising confidence to 99% widens each interval and increases coverage. The tradeoff between coverage and precision should be connected to what the study needs to determine.

Across these 200 groups, the average 95% interval width is approximately 9.0435 kPa for five specimens and 2.2634 kPa for fifty. Two effects contribute to the reduction: standard error decreases with sample size, and the larger t multiplier needed for small samples also declines. These widths summarize the specified population and simulation, making design precision comparable. Planning an experiment can use the same framework with anticipated specimen variability and a target interval width.

## Compare a mean with a specified reference

Some questions come with a specific reference, such as a process target of 20 kPa. A one-sample t test starts from the null hypothesis that the population mean equals that reference, then measures the observed departure in standard-error units. Dividing a difference by its standard error gives a dimensionless statistic, allowing measurements with different units to use the same t reference distribution. More extreme departures occur less frequently under the specified null model and sampling conditions.

$$
t_{\mathrm{obs}}=\frac{\bar x-\mu_0}{s/\sqrt n}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fec9b3a28810ab0be441f7e3.svg) | Observed t statistic, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/7e33236199f3df8d334ffd7f.svg) | Current sample mean, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/ca57ac9e96d5d1c8997d7034.svg) | Population mean specified by the null hypothesis, 20 kPa here. |
| ![Formula](https://ml-biomat.com/static/agent-math/913e236aa6d008dc21044e37.svg) | s is sample standard deviation (kPa), n the independent-specimen count; s/√n is the standard error (kPa). |

The first group of ten gives (18.653641 − 20)/0.994789 ≈ −1.353412. The sign places the mean below the reference; the magnitude counts standard errors. The two tails at least as extreme under a t distribution with 9 degrees of freedom give p ≈ 0.208936.

The first group of ten has a mean of approximately 18.653641 kPa and a standard error of 0.994789 kPa, giving t ≈ −1.353412. A two-sided test includes both tails at least this far from zero and gives p ≈ 0.208936. This area asks how frequently repeated samples would produce a standardized departure at least as extreme if the population mean were 20 kPa. The observed difference in kPa remains part of the scientific result alongside that model-based probability.

The same sample gives a 95% confidence interval from approximately 16.403271 to 20.904010 kPa, including 20. For the same two-sided t method, exclusion of the reference from a 95% interval corresponds to rejection at the 5% level. The interval additionally shows a range of mean values compatible with the data under the method. Read the central difference, interval width, and p value together. A question about being sufficiently close to a target calls for a meaningful tolerance and an equivalence-analysis design.

The comparison and its direction should follow from the research question before analysis. A two-sided question concerns either direction of departure, while a one-sided question concerns a previously specified direction. Choosing the favored direction after seeing the data changes the sampling rule. Multiple comparisons or repeated checking followed by optional stopping also alter overall error probabilities. These choices belong to the study design alongside the individual function call.

The two-tail probability can also be connected directly to the interval rule. Moving a proposed reference mean farther from the sample mean increases its standardized distance and reduces the corresponding tail area. Fix an error-probability level, then collect all reference means that the two-sided test would retain: the result is the corresponding confidence interval. Both tools use the same reference distribution, while one emphasizes a particular proposed value and the other emphasizes a range compatible with the observations.

## A complete program that connects every interval to its sample

The program creates one fixed 200 × 50 array and analyzes the first 5, 10, 30, and 50 observations of each row. `stats.ttest_1samp(..., axis=1)` treats each row as an experiment and returns 200 test statistics. Its `confidence_interval` method constructs the intervals. The program also recomputes their endpoints directly from t quantiles and standard errors, checking that the two paths agree.

### Complete example: fixed samples, t intervals, and coverage

Running generates all samples, numerical summaries, and three scientific figures. SciPy intervals are checked against explicit quantile calculations.

```
"""Study sample means, Student intervals, and repeated-sampling coverage."""
from pathlib import Path
import argparse,json
import numpy as np
import scipy
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
SEED=20261114
MU,SIGMA=20.,4.
BLUE,RED,INK='#28658c','#b64a35','#20313e'


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    zh=args.language=='zh';tr=lambda z,e:z if zh else e
    available={f.name for f in font_manager.fontManager.ttflist};plt.rcParams.update({'font.family':[f for f in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans'] if f in available],'font.size':12,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'grid.alpha':.15})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg');fig.savefig(args.output/f'{name}-{args.language}.png',dpi=160);plt.close(fig)
    bank=np.random.default_rng(SEED).normal(MU,SIGMA,size=(200,50));cases={};critical={}
    for n in [5,10,30,50]:
        samples=bank[:,:n];test=stats.ttest_1samp(samples,MU,axis=1)
        for confidence in [.9,.95,.99]:
            interval=test.confidence_interval(confidence_level=confidence);means=samples.mean(axis=1);sem=stats.sem(samples,axis=1);q=float(stats.t.ppf((1+confidence)/2,n-1));critical[f'{n}_{confidence}']=q
            assert np.allclose(interval.low,means-q*sem)
            cases[f'{n}_{confidence}']={'coverage_count':int(np.sum((interval.low<=MU)&(MU<=interval.high))),
                'mean_interval_width_kPa':float(np.mean(interval.high-interval.low)),
                'selected_mean_kPa':float(means[0]),'selected_sem_kPa':float(sem[0]),'selected_low_kPa':float(interval.low[0]),'selected_high_kPa':float(interval.high[0]),
                'selected_t':float(test.statistic[0]),'selected_p':float(test.pvalue[0])}
    hand=np.array([16,18,20,22,24.]);hand_sem=float(stats.sem(hand));hand_q=float(stats.t.ppf(.975,4));hand_test=stats.ttest_1samp(hand,20.)
    np.savetxt(args.output/'samples.csv',bank,delimiter=',',header=','.join(f'specimen_{i+1}' for i in range(50)),comments='')
    bank_data={'samples':bank.tolist(),'critical':critical,'population_mean_kPa':MU,'population_sd_kPa':SIGMA,'seed':SEED}
    (args.output/'sample-bank.json').write_text(json.dumps(bank_data),encoding='utf-8')
    n=10;sample=bank[0,:n];means=bank[:,:n].mean(axis=1);test=stats.ttest_1samp(bank[:,:n],MU,axis=1);ci=test.confidence_interval();covers=(ci.low<=MU)&(MU<=ci.high)
    fig,ax=plt.subplots(1,2,figsize=(12,5.8),layout='constrained')
    ax[0].scatter(np.arange(1,n+1),sample,color=BLUE,s=55);ax[0].axhline(sample.mean(),color=BLUE,label=tr('该组样本均值','This sample mean'));ax[0].axhline(MU,color=INK,ls='--',label=tr('规定总体均值20 kPa','Defined population mean 20 kPa'))
    ax[0].set(xlabel=tr('独立试样编号','Independent specimen index'),ylabel=tr('教学读数 / kPa','Teaching reading / kPa'),title=tr('一组10个试样，保留每个读数','One group of ten specimens, all readings visible'),xticks=[1,3,5,7,10]);ax[0].legend(frameon=False,fontsize=10);ax[0].grid()
    ax[1].hist(means,bins=np.arange(15,25.5,.5),color='#b6d0df',edgecolor='white');ax[1].axvline(MU,color=INK,ls='--');ax[1].axvline(sample.mean(),color=RED,label=tr('左图这一组的均值','Mean of the group shown at left'))
    ax[1].set(xlabel=tr('每组的样本均值 / kPa','Sample mean of each group / kPa'),ylabel=tr('组数','Number of groups'),title=tr('200组独立抽样，形成均值分布','200 independent groups form a mean distribution'));ax[1].legend(frameon=False,fontsize=10);save(fig,'sampling')
    fig,ax=plt.subplots(1,2,figsize=(12,5.8),layout='constrained');x=np.linspace(-5,5,1001)
    ax[0].plot(x,stats.norm.pdf(x),color=INK,ls='--',label=tr('标准正态','Standard normal'))
    for df,color in [(4,RED),(49,BLUE)]:ax[0].plot(x,stats.t.pdf(x,df),color=color,label=f't, df = {df}')
    mask=np.abs(x)>=hand_q;ax[0].fill_between(x,0,stats.t.pdf(x,4),where=mask,color=RED,alpha=.2);ax[0].set(xlabel=tr('标准化统计量，无量纲','Standardized statistic, dimensionless'),ylabel=tr('概率密度','Probability density'),title=tr('Student（1908）：小样本还要估计波动','Student (1908): small samples also estimate spread'));ax[0].legend(frameon=False,fontsize=10)
    ns=np.arange(3,61);qs=stats.t.ppf(.975,ns-1);ax[1].plot(ns,qs,color=RED,lw=2);ax[1].axhline(stats.norm.ppf(.975),color=INK,ls='--');ax[1].scatter([5,50],stats.t.ppf(.975,np.array([4,49])),color=RED)
    ax[1].annotate('n = 5: 2.776',(5,hand_q),xytext=(11,3.2),arrowprops={'arrowstyle':'-','color':RED});ax[1].set(xlabel=tr('每组独立试样数 n','Independent specimens per group, n'),ylabel=tr('95%区间的临界倍数','Critical multiplier for a 95% interval'),title=tr('样本增多，临界倍数逐渐靠近1.96','With more observations, the multiplier approaches 1.96'));ax[1].grid();save(fig,'history')
    fig,ax=plt.subplots(1,2,figsize=(12,8.4),layout='constrained',gridspec_kw={'width_ratios':[1.5,1]})
    for i in range(40):ax[0].plot([ci.low[i],ci.high[i]],[i+1,i+1],color=BLUE if covers[i] else RED,lw=1.8);ax[0].scatter(means[i],i+1,color=BLUE if covers[i] else RED,s=14)
    ax[0].axvline(MU,color=INK,ls='--');ax[0].invert_yaxis();ax[0].set(xlabel=tr('均值与95%置信区间 / kPa','Mean and 95% confidence interval / kPa'),ylabel=tr('独立抽样组编号','Independent sample-group index'),title=tr('展示前40组：区间随样本变化','First 40 groups: intervals vary across samples'))
    counts=[cases[f'{n}_0.95']['coverage_count'] for n in [5,10,30,50]]
    ax[1].bar([0,1,2,3],np.array(counts)/2,color=BLUE,width=.55);ax[1].axhline(95,color=RED,ls='--',label=tr('设定置信水平95%','Nominal confidence 95%'))
    for i,count in enumerate(counts):ax[1].text(i,max(97,count/2+2),f'{count}/200',ha='center',fontsize=11)
    ax[1].set(xticks=[0,1,2,3],xticklabels=[5,10,30,50],ylim=(0,105),xlabel=tr('每组试样数 n','Specimens per group, n'),ylabel=tr('覆盖20 kPa的比例 / %','Intervals covering 20 kPa / %'),title=tr('全部200组的实际覆盖率','Observed coverage over all 200 groups'));ax[1].legend(frameon=False,fontsize=9);save(fig,'coverage')
    summary={'versions':{'numpy':np.__version__,'scipy':scipy.__version__,'matplotlib':matplotlib.__version__},'seed':SEED,'groups':200,'cases':cases,
        'hand_mean_kPa':float(hand.mean()),'hand_sd_kPa':float(hand.std(ddof=1)),'hand_sem_kPa':hand_sem,'hand_critical95':hand_q,'hand_halfwidth95_kPa':hand_q*hand_sem,'hand_t':float(hand_test.statistic),'hand_p':float(hand_test.pvalue)}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary))


if __name__=='__main__':main()
```

`samples.csv` preserves all readings, `sample-bank.json` contains the same data and critical values for the interaction, and `summary.json` records coverage counts, average interval widths, and first-group results. Coverage is calculated by comparing both endpoints with the known value of 20 kPa. A mean merely lying close to the reference line is a different criterion. The known teaching population makes direct coverage evaluation possible.

Begin with the five-point check: mean 20, standard deviation √10, and standard error √2. Then inspect the first simulated group. Array orientation is particularly important. Averaging across a row summarizes specimens within an experiment; averaging down a column combines the same numbered position across experiments. Both return numbers, but only an operation matching the sampling unit answers the intended question.

## Link a sample, its mean, and its confidence interval

The experiment retains exactly the same 200 groups as Python. Choose a sample size and confidence level, then move the group index. The views show every reading in the selected group, its mean among all 200 group means, and its page of forty intervals. A thicker line highlights the selected group, and red marks an interval that misses 20 kPa. The displayed coverage always uses all 200 groups; showing forty at a time keeps individual intervals readable.

### One concrete sample among 200 experiments

[Figure: Forty traceable sample-mean intervals](https://ml-biomat.com/tutorials/python-scientific/p22/en/#P22-intervals)

[Figure: All readings in the selected sample](https://ml-biomat.com/tutorials/python-scientific/p22/en/#P22-sample)

[Figure: Distribution of all 200 sample means](https://ml-biomat.com/tutorials/python-scientific/p22/en/#P22-means)

Dashed lines mark the defined mean of 20 kPa. Red intervals miss it. The upper panel displays forty groups per page; reported coverage always uses all 200 groups.

Keep one group selected and increase its sample size from 5 to 50. Observe how the additional readings change both the mean and interval. Larger samples generally improve precision, while a particular mean need not move toward 20 at every increase. Next keep sample size fixed and change confidence from 95% to 99%. Readings and means remain the same, while the critical multiplier and interval width change. These operations separately alter the amount of data and the estimation rule.

Find a red interval and inspect its sample. Its mean may lie well to one side of 20, or its estimated spread may be relatively small. Failure to cover the true mean is an expected possibility under repeated sampling. Inspecting such groups gives the frequency interpretation substance and demonstrates why complete readings and sampling information are useful companions to interval estimates.

A normal population was chosen so that the small-sample t assumptions and the validation experiment align exactly. With actual observations, inspect points, histograms, and quantile plots alongside the measurement mechanism. Five points provide limited information about skew or tail behavior. Process knowledge, additional independent specimens, and an analysis suited to the research question can strengthen that assessment. Simulation is useful for changing such conditions individually and examining how an estimation rule responds.

## Write the statistical result back into the scientific question

Report a mean together with the number of independent specimens, measurement units, dispersion, and interval definition. For example, this teaching model produces a group of ten with mean 18.654 kPa and a 95% t interval of 16.403–20.904 kPa. An actual report would identify its material population, sampling design, and treatment conditions, allowing readers to understand what kind of objects the mean represents.

Choose a method after examining how the data were produced. Paired before-and-after measurements can be analyzed through within-pair differences; multiple preparation batches retain their batch structure; strong skew or a few extreme readings call for attention to distribution shape and an appropriate estimator. Statistical tools are useful because they connect sampling, estimation, and judgment. A clear result supplies numbers while also showing how independent information produced them.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P22.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [SciPy: ttest_1samp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_1samp.html)

   One-sample testing, independent observations, and the confidence-interval interface.

   BSD-3-Clause; technical reference
2. [SciPy: Student t distribution](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.t.html)

   Degrees of freedom, quantiles, and probability density.

   BSD-3-Clause; technical reference
3. [SciPy: sem](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.sem.html)

   Standard error and degrees-of-freedom adjustment.

   BSD-3-Clause; technical reference
4. [Student (1908), The Probable Error of a Mean](https://en.wikisource.org/wiki/The_Probable_Error_of_a_Mean)

   Original discussion of small-sample means and estimated spread; figures are original calculations.

   Public-domain original; historical reference
