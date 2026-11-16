# Distributions, Repeated Measurements, and Error Bars

Source: https://ml-biomat.com/tutorials/python-scientific/p17/en/
Language: en

Connect specimen points, distributions, and intervals with Seaborn; distinguish spread, precision, and independent sample size.

## Can two batches with the same mean feel different?

Suppose you are comparing two batches of material for a soft cushion. You independently manufacture twelve specimens from each batch and measure their elastic modulus, a quantity related to stiffness. Both batches have a mean of exactly 10 kPa. In the first, specimen values lie between 8 and 12 kPa; in the second, they range from 6 to 14 kPa. A user may encounter noticeably softer or stiffer individual pieces in the second batch, while a manufacturer may recognize a consistency problem. Two equally tall mean bars would hide much of this distinction. This chapter uses Seaborn to connect individual specimens, distributions, and intervals around a mean.

You can initially think of elastic modulus as a measure of resistance to deformation. We use kPa as its unit and focus on how these values are summarized and displayed. An explicitly listed teaching dataset will reveal what point plots, histograms, cumulative distributions, and boxplots retain. We will then distinguish standard deviation, standard error, and a confidence interval for the mean. The complete program preserves three instrument readings per specimen, so every step can be followed from 72 raw records to 24 specimen means and finally two group means.

Seaborn builds on Matplotlib and maps table variables to positions, colors, and groups while carrying out statistical summaries. Its convenience makes the identity of a table row especially important. Specimens, repeated readings, batches, and conditions can belong to different levels. The level supplied to a plotting function determines what a point represents, what a histogram counts, and which sample size enters an interval calculation.

## Why statisticians insist on seeing the observations

In his 1973 paper *Graphs in Statistical Analysis*, F. J. Anscombe constructed datasets with very similar numerical summaries and markedly different scatter patterns. The example became influential because it made an easily missed distinction visible. Means, variances, and fitted lines compress information without retaining the full structure of observations. Graphical analysis exposes curvature, clusters, and unusual points that can influence the choice of a statistical method. We follow that reasoning with two original teaching groups, examining the difference between having the same mean and having the same distribution.

![Following Anscombe’s emphasis on graphical inspection, two teaching groups of twelve specimens are shown as means and as individual points. Each point is a specimen’s mean of three readings; horizontal swarm displacement prevents overlap.](https://ml-biomat.com/static/tutorials/python-scientific/figures/453c480dd13bf613de41af62.svg?v=453c480dd13b)

Figure 1Following Anscombe’s emphasis on graphical inspection, two teaching groups of twelve specimens are shown as means and as individual points. Each point is a specimen’s mean of three readings; horizontal swarm displacement prevents overlap.

The left panel retains only the two means; the right gives every independent specimen its own point. Group A is concentrated near the center, while B occupies a broader range, although their centers remain aligned. A swarm plot moves overlapping points sideways so equal or similar modulus values remain visible. That horizontal displacement allocates drawing space; vertical position carries the measurement. Counting the points confirms twelve specimens per group. Such a display is particularly useful for small samples because both the value range and the number of observations remain accessible.

Computing tools increasingly turn these statistical reading habits into directly executable operations. Michael Waskom’s 2021 Seaborn paper describes the relationship between tabular data and statistical graphics: users specify how variables map to visual roles, and the library organizes grouping and graphical elements. Here, assigning `group` to categories and `modulus_kPa` to the vertical axis lets the same specimen table support several views. Changing the plot type can preserve the identity of the underlying observations.

## First establish what one point represents

Group A contains the specimen means 8, 8, 9, 9, 10, 10, 10, 10, 11, 11, 12, and 12 kPa. Group B contains 6, 6, 7, 8, 9, 10, 10, 11, 12, 13, 14, and 14 kPa. Each specimen receives three readings: 0.2 kPa below its mean, exactly at its mean, and 0.2 kPa above it. These fixed offsets make the teaching calculation inspectable. Every raw row contains group, specimen identifier, repeat identifier, and modulus. Together those fields describe where the reading belongs.

For example, specimen A01 has readings of 7.8, 8.0, and 8.2 kPa, whose average is 8.0 kPa. Repeating that operation converts 72 instrument records into 24 specimen records. If independent manufacture occurs at specimen level, the specimen is the independent unit for comparing material behavior. Readings from the same specimen share its material structure. Repeated measurement can stabilize the reading for that object while preserving its identity as one material specimen. Recording the hierarchy in columns makes it available throughout the analysis.

The program uses `groupby(['group','specimen'])` to average within each combination of group and specimen identifier. Using both fields retains the complete grouping identity. Seaborn then receives a table with one row per specimen. `x='group'` selects the category column and `y='modulus_kPa'` selects the measurement column. These strings are column names that tell the function where to find values. `hue='group'` assigns color by category, and an explicit palette dictionary keeps A and B visually consistent across every figure.

Unequal numbers of repeated readings introduce another consequence. Averaging all raw records together gives greater weight to specimens measured more often. Averaging within specimens and then across specimen means gives each independent specimen equal weight. In this example every specimen has exactly three readings, so both routes produce the same group mean. They still produce different standard errors because the number used to represent independent information differs.

## From individual specimens to bins, cumulative counts, and ranks

A histogram partitions the modulus axis into adjacent intervals and counts the specimens in each interval. Imagine sorting screws into boxes labeled by length range: the number in each box becomes a bar height. Narrow bins retain more local detail and also reveal more fluctuation from limited sampling. Wide bins produce a smoother overview while combining neighboring regions. To compare A and B, give them the same bin edges. Otherwise the interval assigned to a particular value can differ between groups, making the counts harder to compare directly.

![Four views of the same 24-specimen table: two bin widths, empirical cumulative distributions, and box summaries with all specimens. Histograms share bin edges; boxplot whiskers use the 1.5-IQR rule.](https://ml-biomat.com/static/tutorials/python-scientific/figures/62254f178873f509d8102653.svg?v=62254f178873)

Figure 2Four views of the same 24-specimen table: two bin widths, empirical cumulative distributions, and box summaries with all specimens. Histograms share bin edges; boxplot whiskers use the 1.5-IQR rule.

The upper panels change only bin width; the specimens remain the same. Intervals include the left boundary and exclude the right, with the final interval also including its right endpoint. Half-integer edges keep our integer specimen values away from boundaries. Group A has four specimens at 10 kPa, creating a prominent central count in the narrow-bin view. Wider bins combine neighboring values and emphasize concentration over a broader range. These bars show counts. A density histogram would additionally divide by sample number and bin width, so area rather than height represents a proportion.

The empirical cumulative distribution function requires no bin width. Move from left to right along the value axis and add 1/12 whenever you encounter a specimen. Tied values create a larger jump because several specimens enter at once. At 10 kPa, A has accumulated 8/12, or about 66.7%, while B has accumulated 7/12, or about 58.3%. This display directly answers how many specimens fall at or below a threshold and identifies the value associated with a particular cumulative fraction. Its steps arise naturally from a finite sample.

A boxplot compresses the ordered values further. The median marks the middle, and the first and third quartiles enclose the central half of the distribution. Common whiskers extend to the most extreme observed values within 1.5 interquartile ranges of the box, with more distant observations shown individually. Such a point identifies a relatively distant observation whose cause can be investigated using the records. Overlaying raw points is especially useful with small samples: readers see which values created the box and can recognize details hidden by a compact summary. Quantiles between finite observations require an interpolation convention; this example uses NumPy’s default linear convention.

## Standard deviation, standard error, and confidence intervals

A mean describes the center. To describe how far specimens spread around that center, calculate each deviation from the mean, square the deviations, add them, divide by the degrees of freedom, and take a square root. This gives the sample standard deviation, SD. Squaring prevents positive and negative deviations from cancelling; taking the square root restores kPa after the intermediate calculation in kPa². The denominator n−1 reflects estimating the mean from the same sample: deviations must sum to zero, so the final deviation is determined by the others.

$$
\bar x=\frac{1}{n}\sum_{i=1}^{n}x_i,\qquad s=\sqrt{\frac{\sum_{i=1}^{n}(x_i-\bar x)^2}{n-1}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/10c16af3229388fdcbca3de7.svg) | Mean modulus across three readings of independent specimen i, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Specimen index; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Independent specimen count, 12 per group; dimensionless and greater than 1 |
| ![Formula](https://ml-biomat.com/static/agent-math/7e33236199f3df8d334ffd7f.svg) | Mean across specimens of the selected group, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | Sample standard deviation SD, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | Add the indicated quantities over the specimens |
| ![Formula](https://ml-biomat.com/static/agent-math/9bcc38017e1856dc949d86bd.svg) | Square root; restores original units after squaring |

Group A sums to 120 kPa, giving 10 kPa after division by 12. Two 8s and two 12s contribute 16 kPa² of squared deviations; two 9s and two 11s contribute another 4 kPa². Thus s=√(20/11)≈1.34840 kPa. Estimating the unknown population mean from the sample consumes one degree of freedom, giving n−1 when estimating population variance.

The squared deviations sum to 20 kPa² for A and 92 kPa² for B. With twelve independent specimens in each group, the standard deviations are approximately 1.348 and 2.892 kPa. This agrees with the broader spread visible in B’s point plot. If the question concerns variability among manufactured pieces, the raw distribution and SD deserve attention. Measuring more independent specimens improves knowledge of that distribution; it does not itself make the manufactured individuals more consistent.

The standard error of the mean, SEM, concerns a different object. Imagine repeatedly drawing a batch of independent specimens by the same method and calculating a mean each time. SEM estimates the spread of those means. With independent observations drawn from one distribution, a mean generally becomes more stable as sample size grows, producing the division by the square root of n. Group A has an SEM of about 0.389 kPa, smaller than its SD. The resulting interval describes precision of the estimated mean, rather than the range occupied by most individual specimens.

$$
\mathrm{SEM}=s/\sqrt n
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dd3305e34ff527725a7a82ea.svg) | Estimated standard error of the mean of independent specimens, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | Sample standard deviation of specimen values, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Number of independent, identically distributed specimens; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/e0639947db355311e236c3a6.svg) | Square root of sample count; dimensionless |

Variances of independent identically distributed values add, and averaging divides the variance by n². The mean therefore has 1/n of the individual variance and 1/√n of its standard deviation. For A, SEM=√(20/11)/√12≈0.389249 kPa. Repeated readings from one specimen do not satisfy the independence assumption used in this count.

A 95% confidence interval for the mean multiplies SEM by an additional coefficient. Here we use a Student t interval. Twelve specimens give eleven degrees of freedom and a coefficient of approximately 2.201. Under independent, identically distributed normal sampling, this construction has an exact coverage interpretation. It also serves as an approximation when the sample mean is sufficiently close to normal. The explicit teaching values illustrate the construction. For skewed, small, or hierarchical samples, distribution and study design guide the choice of interval method.

$$
\mathrm{CI}_{95\%}=\left[\bar x-t_{0.975,n-1}\frac{s}{\sqrt n},\;\bar x+t_{0.975,n-1}\frac{s}{\sqrt n}\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/65f4735a16f924a7e46e8319.svg) | 95% Student t confidence interval for the population mean; endpoints in kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/7e33236199f3df8d334ffd7f.svg) | Sample mean, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | Sample standard deviation, kPa |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Independent sample count, 12 here; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/22ba3759c09a7ea30a432312.svg) | 0.975 quantile of the standard t distribution with n−1 degrees of freedom; dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/6cfef8857b6fd57926324bb0.svg) | Cumulative probability leaving 0.025 in the upper tail of a two-sided 95% interval; dimensionless |

Leaving 2.5% in each tail retains 95% centrally, hence the 0.975 quantile. The construction has exact coverage for independent normal samples. With n=12 the coefficient is approximately 2.200985. A’s half-width is 2.200985×0.389249≈0.856732 kPa, producing [9.143268,10.856732] kPa around its mean of 10.

The 95% refers to the long-run fraction of intervals that cover the population mean when sampling and interval construction are repeatedly performed by the same rule. An interval already calculated is fixed, as is the unknown population mean. Its width expresses uncertainty in the estimated mean under the chosen method. A caption identifying “mean ± SD,” “mean ± SEM,” or “95% t interval” gives readers the statistical object needed to interpret the bars.

## Why treating readings as specimens narrows the interval

Return to the three readings per specimen. Group A contains twelve independent specimens and thirty-six instrument records. Supplying all thirty-six readings directly to a standard-error function treats them as independent inputs and gives approximately 0.220 kPa. Averaging within specimens first gives approximately 0.389 kPa. Both means remain 10 kPa, but the interval becomes narrower. The numerical routine follows the supplied array; the shared specimen identity must enter through the data preparation or statistical model.

![Left: mean ± SD, mean ± SEM, and 95% Student t intervals based on twelve independent specimens per group. Right: the SEM produced when thirty-six repeated readings are treated as independent inputs.](https://ml-biomat.com/static/tutorials/python-scientific/figures/a38ee205e8fe130c4b2c9171.svg?v=a38ee205e8fe)

Figure 3Left: mean ± SD, mean ± SEM, and 95% Student t intervals based on twelve independent specimens per group. Right: the SEM produced when thirty-six repeated readings are treated as independent inputs.

Repeated readings resemble taking three photographs of the same object. More photographs can help describe that object clearly while its identity remains unchanged. An independent statistical unit comes from the manufacturing, sampling, or random-assignment process. Cells, animals, culture vessels, batches, and technical repeats can occupy different levels, and multiple measurements in one vessel may share environmental conditions. Retaining those levels as columns allows appropriate aggregation or a model that explicitly represents the hierarchy.

Using specimen means in this example makes each independent specimen’s contribution visible. If instrument repeatability is also a research target, plot deviations among readings of the same specimen and summarize their within-specimen variation. Material differences and instrument repeatability are both meaningful questions, each using a different component of variation. The paired SEM display makes the consequence of changing the denominator directly visible.

## A complete program with shared grouping, statistics, and figures

The program generates seventy-two readings from twenty-four fixed specimen values, then saves both the raw and specimen-level tables. Seaborn’s `barplot` calculates group means, `swarmplot` arranges specimen points, `histplot` counts observations in bins, `ecdfplot` accumulates proportions, and `boxplot` summarizes ordered values. Each call receives the same specimen table and explicit column names. The functions use Matplotlib Axes, so titles, units, and ticks can still be changed with `set`, connecting these statistical displays to the figure composition methods of the previous chapter.

The mean bars use `errorbar=None` so the opening historical concept figure concentrates on information hidden by a mean. In the third figure, NumPy and SciPy calculate SD, SEM, and t intervals explicitly, and Matplotlib draws horizontal error bars. Seaborn also offers options such as `errorbar='sd'`, `'se'`, and confidence intervals. Its confidence intervals can use bootstrap calculations, a different construction from the t interval shown here. Convenient option names still need captions that identify the method and independent unit.

### Complete Python: independent specimens, distributions, and three intervals

Generate explicit teaching readings, aggregate by specimen with pandas, draw distributions with Seaborn, and calculate statistical summaries with NumPy and SciPy.

```
"""Show distributions and distinguish specimens from repeated instrument readings."""
from pathlib import Path
import argparse,json
import numpy as np
import pandas as pd
import scipy
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import MaxNLocator
import seaborn as sns

VALUES={'A':[8,8,9,9,10,10,10,10,11,11,12,12],
        'B':[6,6,7,8,9,10,10,11,12,13,14,14]}
COLORS={'A':'#28658c','B':'#b64a35'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
    def tr(a,b):return a if zh else b
    sns.set_theme(style='whitegrid',font='DejaVu Sans',font_scale=1.1)
    plt.rcParams.update({'font.family':[name for name in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans'] if name in {f.name for f in font_manager.fontManager.ttflist}],'svg.fonttype':'none',
                        'axes.spines.top':False,'axes.spines.right':False,'grid.alpha':.18})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg');fig.savefig(args.output/f'{name}-{args.language}.png',dpi=160);plt.close(fig)
    readings=pd.DataFrame([{'group':group,'specimen':f'{group}{i+1:02}',
        'repeat':j+1,'modulus_kPa':value+offset} for group,values in VALUES.items()
        for i,value in enumerate(values) for j,offset in enumerate([-.2,0,.2])])
    specimens=readings.groupby(['group','specimen'],as_index=False)['modulus_kPa'].mean()
    readings.to_csv(args.output/'readings.csv',index=False);specimens.to_csv(args.output/'specimens.csv',index=False)
    summary={'versions':{'numpy':np.__version__,'pandas':pd.__version__,'scipy':scipy.__version__,
                         'seaborn':sns.__version__,'matplotlib':matplotlib.__version__},'groups':{}}
    for group in VALUES:
        v=specimens.loc[specimens.group==group,'modulus_kPa'].to_numpy();raw=readings.loc[readings.group==group,'modulus_kPa'].to_numpy()
        n=len(v);mean=float(v.mean());sd=float(v.std(ddof=1));se=float(stats.sem(v));critical=float(stats.t.ppf(.975,n-1))
        summary['groups'][group]={'n_specimens':n,'n_readings':len(raw),'mean_kPa':mean,'sd_kPa':sd,
             'sem_kPa':se,'t_critical':critical,'ci95_kPa':[mean-critical*se,mean+critical*se],
             'naive_reading_sem_kPa':float(stats.sem(raw)),'sum_squared_deviations_kPa2':float(np.sum((v-mean)**2)),
             'quantiles_kPa':np.quantile(v,[.25,.5,.75]).tolist(),
             'count_at_or_below_10':int(np.count_nonzero(v<=10))}
    fig,axes=plt.subplots(1,2,figsize=(12,5.5),layout='constrained')
    sns.barplot(data=specimens,x='group',y='modulus_kPa',hue='group',palette=COLORS,errorbar=None,legend=False,ax=axes[0])
    axes[0].set(title=tr('A  均值相同：两根柱子都是10','A  Same mean: both bars equal 10'),xlabel=tr('组别','Group'),ylabel=tr('平均模量 / kPa','Mean modulus / kPa'),ylim=(0,15))
    sns.swarmplot(data=specimens,x='group',y='modulus_kPa',hue='group',palette=COLORS,legend=False,size=6,ax=axes[1])
    axes[1].axhline(10,color='#71808b',ls='--',lw=1)
    axes[1].set(title=tr('B  保留样品：分布范围不同','B  Keep specimens: different distributions'),xlabel=tr('组别，每组12个样品','Group, 12 specimens each'),ylabel=tr('样品平均模量 / kPa','Specimen-mean modulus / kPa'),ylim=(0,15))
    fig.suptitle(tr('Anscombe 1973：看图能发现数值摘要隐藏的结构','Anscombe 1973: graphs reveal structure beyond summaries'),fontsize=15)
    save(fig,'history')
    fig,axes=plt.subplots(2,2,figsize=(12,9),layout='constrained')
    for ax,width in zip(axes[0],[1,4]):
        sns.histplot(data=specimens,x='modulus_kPa',hue='group',palette=COLORS,
            bins=np.arange(5.5,17.5+width,width),element='step',fill=False,common_bins=True,stat='count',ax=ax)
        ax.set(title=tr(f'箱宽 {width} kPa',f'Bin width {width} kPa'),xlabel=tr('模量 / kPa','Modulus / kPa'),ylabel=tr('样品数','Specimen count'),xlim=(5,18))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.get_legend().set_title(tr('组别','Group'))
    sns.ecdfplot(data=specimens,x='modulus_kPa',hue='group',palette=COLORS,ax=axes[1,0])
    axes[1,0].get_legend().set_title(tr('组别','Group'))
    axes[1,0].set(title=tr('经验累积分布：逐个累计样品','Empirical CDF: accumulate specimens'),xlabel=tr('模量 / kPa','Modulus / kPa'),ylabel=tr('不超过横轴值的比例','Fraction at or below x'),xlim=(5,16))
    sns.boxplot(data=specimens,x='group',y='modulus_kPa',hue='group',palette=COLORS,legend=False,width=.45,showfliers=False,ax=axes[1,1])
    sns.swarmplot(data=specimens,x='group',y='modulus_kPa',color='#20313e',size=4,ax=axes[1,1])
    axes[1,1].set(title=tr('箱线图与全部样品','Box summaries with every specimen'),xlabel=tr('组别','Group'),ylabel=tr('模量 / kPa','Modulus / kPa'))
    save(fig,'distributions')
    fig,axes=plt.subplots(1,2,figsize=(12,6),layout='constrained')
    for j,group in enumerate(VALUES):
        d=summary['groups'][group]
        for i,(label,half) in enumerate([('SD',d['sd_kPa']),('SEM',d['sem_kPa']),('95% t CI',d['ci95_kPa'][1]-10)]):
            axes[0].errorbar(10,i+j*.18,xerr=half,fmt='o',capsize=5,color=COLORS[group],label=group if i==0 else None)
        axes[1].plot([0,1],[d['sem_kPa'],d['naive_reading_sem_kPa']],'o-',color=COLORS[group],lw=2,label=group)
    axes[0].set(yticks=[.09,1.09,2.09],yticklabels=[tr('均值 ± SD','mean ± SD'),tr('均值 ± SEM','mean ± SEM'),'95% t CI'],
        xlabel=tr('模量 / kPa','Modulus / kPa'),title=tr('同一均值，三种区间含义','One mean, three interval meanings'),xlim=(6,14));axes[0].legend(frameon=False)
    axes[1].set(xticks=[0,1],xticklabels=[tr('12个独立样品','12 independent\nspecimens'),tr('36条读数\n直接计算','Treat 36 readings\nas independent')],
        ylabel=tr('计算得到的SEM / kPa','Calculated SEM / kPa'),title=tr('独立单位决定SEM的分母','Independent units determine the SEM denominator'),ylim=(0,1))
    axes[1].tick_params(axis='x',labelsize=11);axes[1].legend(frameon=False)
    save(fig,'intervals')
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary))


if __name__=='__main__':main()
```

The output reports means of 10.0 kPa for both groups, SD values of approximately 1.3484 and 2.8920 kPa, and SEM values of approximately 0.38925 and 0.83485 kPa. The 95% t intervals are approximately [9.1433, 10.8567] and [8.1625, 11.8375] kPa. The raw table has 72 rows, the specimen table has 24, and each group has twelve specimens. Matching those quantities to point counts, histogram bars, and interval endpoints provides complementary numerical and visual checks.

When adapting the program, begin with the columns identifying independent units. Confirm the number of unique specimens before selecting plotting options. A missing reading may leave the specimen mean based on fewer repeats; a missing specimen changes the independent sample count. Keeping those situations distinct makes later calculations easier to interpret. The original and aggregated CSV files provide a practical record of the transformation, while the JSON summary exposes quantities that can be compared against calculations outside the plotting library.

## Change the display while retaining specimen identity

The experiment below lets you choose a group, a histogram bin width, and SD, SEM, or a 95% t interval around the mean. Specimen points, the histogram, and the cumulative distribution update together. Intervals always use the twelve independent specimens in the selected group. First compare A with B: the mean stays fixed while the distribution broadens. Then hold A fixed and switch SD to SEM. The specimen points remain where they were; the interval around their mean changes.

### Link specimens, distributions, and intervals

All statistics use twelve independent specimen means per group. Filled points lie at or below the threshold; bin width and interval type control different summaries.

[Figure: All specimens and mean interval](https://ml-biomat.com/tutorials/python-scientific/p17/en/#P17-points)

[Figure: Histogram with fixed-origin bins](https://ml-biomat.com/tutorials/python-scientific/p17/en/#P17-hist)

[Figure: Empirical cumulative distribution and threshold fraction](https://ml-biomat.com/tutorials/python-scientific/p17/en/#P17-cdf)

Increasing bin width from 1 to 4 kPa rearranges the histogram counts while leaving the empirical cumulative distribution unchanged. This separates a change in representation from a change in data. Moving the threshold updates the cumulative marker and the count at or below that threshold. At 10 kPa, A contains eight specimens and B contains seven. You can verify those numbers by counting raw points or by multiplying the cumulative fraction by twelve.

The experiment retains every specimen throughout. In an analysis that filters observations, show the filtering rule, retained sample size, and locations of excluded observations together. As an interface gains controls, readers still need a clear route from the current display to the observations used in its calculation. Linking points, counts, and intervals provides that route.

## Let the research question choose the statistical view

For consistency among individuals, begin with raw points, distributions, and SD. For precision of an estimated mean, examine SEM or an appropriate confidence interval. For the fraction meeting a threshold, the cumulative distribution is especially direct. These views complement one another. Small samples often reward keeping individual details visible; larger samples require compression through bins, densities, or quantiles. A smooth density curve introduces a bandwidth choice: narrow bandwidths reveal more fluctuations, while wide bandwidths merge features. Its interpretation includes that estimation step.

Overlap between two mean intervals is also a different question from a specifically designed comparison between groups. Assessing a mean difference requires the uncertainty of the difference and the relationship between the groups: independent, paired, or hierarchical. Measuring the same specimen before and after treatment naturally produces paired differences that retain more information than two disconnected mean bars. Later statistical chapters develop sampling, intervals, and comparison rules. The specimen identities and distribution checks established here already provide a foundation for choosing them.

A useful caption answers three concrete questions: what one point represents, how many independent units each group contains, and how an interval is defined. Quantity names, units, and relevant conditions complete the context. Code makes the statistical and graphical steps repeatable; understanding the experimental unit and research question determines what those operations express.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P17.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Seaborn: visualizing distributions](https://seaborn.pydata.org/tutorial/distributions.html)

   Choose among bins, smoothed densities, and empirical cumulative distributions

   BSD-3-Clause; seaborn LICENSE.md
2. [Seaborn: statistical estimation and error bars](https://seaborn.pydata.org/tutorial/error_bars.html)

   Distinguish sample spread from estimation uncertainty

   BSD-3-Clause
3. [Waskom (2021), seaborn: statistical data visualization](https://joss.theoj.org/papers/10.21105/joss.03021)

   Original author account of tabular data and statistical graphics

   CC BY4.0 paper, BSD3 software
4. [Anscombe (1973), Graphs in Statistical Analysis](https://www.tandfonline.com/doi/abs/10.1080/00031305.1973.10478966)

   Original paper on numerical summaries and graphical structure

   Historical attribution; no reproduced figures or passages
5. [SciPy: standard error of the mean](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.sem.html)

   Standard-error degrees of freedom and input axes

   SciPy BSD3
6. [SciPy: Student t distribution](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.t.html)

   Construct a Student t mean interval using quantiles

   SciPy BSD3
