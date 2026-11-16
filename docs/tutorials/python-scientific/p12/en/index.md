# What a Grouped Average Actually Answers

Source: https://ml-biomat.com/tutorials/python-scientific/p12/en/
Language: en

Follow readings, specimens, and formulations to understand grouping, weights, missingness, and reshaping.

## Why does measuring one specimen more often change the average?

When comparing two water-absorbing materials, we may ask which formulation absorbs more water on average. Putting every reading into a table and calculating a mean by formulation seems sufficient. Yet if one specimen has three readings and another has one, the first contributes three numbers to that calculation. Two levels are involved: how many specimens were prepared independently, and how many technical readings were recorded for each specimen. Both deserve to be recorded, but a single ambiguous “sample size” cannot describe them adequately. This chapter introduces grouped calculations in pandas while tracing the object and weight behind each average.

The explicitly constructed teaching dataset contains three independently prepared specimens for each of formulations A and B. Their identifiers are A01–A03 and B01–B03. A01 has readings 2.0 and 2.2; A02 has 2.8; A03 has 3.0, 3.2, and 3.4. B01 has 2.0 and 2.2, B02 has 2.5 and 2.7, and B03 has 2.9. Each number is a water uptake q under the same specified immersion conditions, expressed as grams of absorbed water per gram of dry material, or g/g. Six specimens therefore generate eleven readings. Readings sharing an identifier describe repeated observations of the same specimen state. An experimental protocol would also maintain that state during weighing and record immersion time, temperature, and removal of surface liquid.

For example, a specimen with a dry mass of 0.50 g and a wet mass of 1.55 g contains 1.05 g of absorbed water under the measurement definition. Dividing by its dry mass gives q=2.1 g/g. This normalizes different specimen sizes to a common dry-material basis. It differs from the percentage of the wet material that is water, which uses wet mass in the denominator. Defining how a column is measured and what one row represents gives the later grouping a stable scientific meaning.

$$
q=\frac{m_{\mathrm{wet}}-m_{\mathrm{dry}}}{m_{\mathrm{dry}}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9dc96195196376263c1f2c83.svg) | Water uptake normalized by dry mass, g/g; a dimensionless mass ratio with its basis retained |
| ![Formula](https://ml-biomat.com/static/agent-math/2bf977fe0b88c7538b19851d.svg) | Wet mass in the specified measurement state, g |
| ![Formula](https://ml-biomat.com/static/agent-math/22b087ed9f064a584dfccac0.svg) | Dry-material mass, g, positive |

Subtract dry mass from wet mass to obtain absorbed water under the measurement definition, then divide using matching mass units. With wet mass 1.55 g and dry mass 0.50 g, q=(1.55−0.50)/0.50=2.1 g/g. Each gram of dry material corresponds to 2.1 g of absorbed water. Measurement state and surface-liquid handling are consistent across specimens.

By the end of the chapter, you will convert a reading table into a specimen table with valid counts, then into a formulation comparison. You will also return each specimen's mean to its original readings to examine within-specimen departures. The complete example saves these intermediate tables alongside the final means, allowing a changed result to be traced through identifiers rather than leaving its cause hidden inside one summary number.

## Break a large table into smaller questions, then combine the answers

On paper, a natural approach is to place readings with the same specimen identifier in a pile, calculate a mean for each pile, and arrange the six answers in a new table. Splitting that table by formulation gives another level of summary. This involves splitting, applying a calculation, and combining results. Grouping determines which observations belong together; it does not require their next operation to be a mean. The same collection could be counted, inspected for its maximum, or compared with its own baseline.

Hadley Wickham's 2011 paper described the split–apply–combine strategy systematically, using baseball records and spatial-temporal ozone data to illustrate reusable computational organization. The paper accompanied the R package plyr. Its relevance here is the organization of calculations into explicit steps. In pandas, `groupby` provides a corresponding way to name the grouping keys and then choose the data column and operation. The original diagram below follows this chapter's constructed readings; every intermediate number can be checked against the input.

![Six constructed A readings illustrate split–apply–combine. The intermediate table retains three specimen identities; the final denominator counts specimens.](https://ml-biomat.com/static/tutorials/python-scientific/figures/67a097d5c38b3f407969c2ea.svg?v=67a097d5c38b)

Figure 1Six constructed A readings illustrate split–apply–combine. The intermediate table retains three specimen identities; the final denominator counts specimens.

Notice that the meaning of one row changes at each stage. The first table has one row per reading, the middle table has one row per specimen, and the last table has one row per formulation. A shorter table contains an intentional summary of detail. Keeping identifiers and valid counts alongside that summary makes the compression interpretable: a reader can see which information remains and which questions require returning to the preceding table.

This pattern also appears in microscopy, tensile measurements, and biological experiments. An image may contain several particles, one specimen may have several images, and a preparation batch may contain several specimens. Sketching these levels before choosing grouping keys clarifies the analysis. Giving particles, images, specimens, or batches equal weight produces different interpretations. Software can execute each rule consistently, while the research question identifies the level that should contribute equally to the comparison.

## Grouping keys identify objects; selected columns contain the quantities

The input table uses `formulation` for the material formulation, `specimen` for its identifier, `reading` for the within-specimen reading number, and `q` for water uptake. Formulation and specimen identify experimental objects; reading numbers help trace records; water uptake is the physical quantity being averaged. An identifier written with digits does not become a meaningful measurement merely because its data type is numerical. Averaging reading numbers 1, 2, and 3 gives 2, but tells us nothing about water uptake.

`table.groupby(['formulation', 'specimen'], as_index=False)` groups by the combination of formulation and specimen. The two names inside the list define a joint key, rather than two unrelated collections of groups. Rows belong together when both labels match. Our specimen identifiers are already globally unique, but including formulation keeps the experimental hierarchy visible in the output. If separate batches reuse a specimen name such as “01,” the batch identifier must also participate in the key to distinguish those physical objects.

The following `agg` call uses named aggregation. `q_mean=('q', 'mean')` takes a mean from the q column and names the output q_mean. `rows=('q', 'size')` counts all rows, while `valid=('q', 'count')` counts nonmissing q values. These columns describe the result and its numerical support together. `as_index=False` keeps grouping labels as ordinary columns, convenient for displaying the table, saving CSV, and grouping it again.

A01's readings reduce to 2.1, A02 remains 2.8, and A03 becomes 3.2. The three B specimen means are 2.1, 2.6, and 2.9. The new table has six rows. Grouping this table by formulation gives each specimen one representative value. Input rows need not be adjacent for grouping to work, and rearranging their order does not change these means. If the output should follow the order in which groups first appear, `sort=False` expresses that display choice; labels continue to determine membership.

## Every averaging weight belongs to a particular object

The six readings for A sum to 16.6 g/g. Dividing by six gives approximately 2.7667 g/g. Taking the three specimen means first instead gives (2.1+2.8+3.2)/3=2.7000 g/g. Both routes perform explicit arithmetic, but the first gives equal weight to readings and the second gives equal weight to specimens. A03 supplies three readings, receiving half the total weight in the direct average. A02 supplies one, receiving one sixth. In the specimen-level average they each receive one third.

$$
\begin{aligned}\bar q_j&=\frac{1}{n_j}\sum_{i=1}^{n_j}q_{ij},\qquad \bar q_{\mathrm{equal}}=\frac{1}{J}\sum_{j=1}^{J}\bar q_j\\ \bar q_{\mathrm{rows}}&=\frac{\sum_{j=1}^{J}n_j\bar q_j}{\sum_{j=1}^{J}n_j}\end{aligned}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b3f5a274db5824837fd8be6c.svg) | Valid uptake reading i of specimen j, g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | Reading and specimen indices, dimensionless integers |
| ![Formula](https://ml-biomat.com/static/agent-math/3a84ce73458078ab383399f3.svg) | Number of valid readings for specimen j, a positive dimensionless integer |
| ![Formula](https://ml-biomat.com/static/agent-math/70f3dc39744c98269cbe57ad.svg) | Number of specimens with valid means in the formulation, positive and dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/5756278ec076431a907dc307.svg) | Mean of valid readings for specimen j, g/g; the bar denotes a mean |
| ![Formula](https://ml-biomat.com/static/agent-math/9e66413b5e17439d8aa63259.svg) | Formulation mean with equal weight per valid specimen, g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/30e030e3c27645d3136ff08b.svg) | Formulation mean with equal weight per valid reading, g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | Sum over the indicated index range |

Multiplying a specimen mean by its valid count recovers its reading sum. The second line therefore equals the sum of all valid readings divided by their total count. For A, counts are 2,1,3 and specimen means are 2.1,2.8,3.2. The row mean is (2×2.1+1×2.8+3×3.2)/6≈2.7667; the equal-specimen mean is (2.1+2.8+3.2)/3=2.7. Both have units g/g. A specimen with no valid reading remains registered but is absent from the J-term sum.

![Left: readings and specimen means marked by short black lines. Middle: weights sum to one separately within each formulation. Right: row-weighted and equal-specimen means share the uptake scale.](https://ml-biomat.com/static/tutorials/python-scientific/figures/bef0af6db7b6dbd7fb8e7378.svg?v=bef0af6db7b6)

Figure 2Left: readings and specimen means marked by short black lines. Middle: weights sum to one separately within each formulation. Right: row-weighted and equal-specimen means share the uptake scale.

Imagine distributing speaking time among the specimens. Averaging readings gives each record the same short turn, so a specimen with more records speaks longer overall. Summarizing specimens first lets each form a representative answer and then speak once. The analogy explains the weight allocation, while the scientific question determines which allocation is useful. A comparison of independently prepared materials normally retains the specimen level. A question specifically about all readings from a defined measurement process can use that process as its target, provided the allocation of readings is also described.

Keeping six copies of A01's two existing records provides a purely computational experiment: it adds neither material nor new measurements. A01's mean stays at 2.1, and A's equal-specimen mean stays at 2.7. The mean over rows, however, drops to 2.35. The calculation is transparent: A01 now contributes twelve readings with a total of 25.2, while the other two specimens contribute four readings totaling 12.4. Dividing 37.6 by sixteen gives 2.35. Duplicate imports can therefore change an analysis through weights even when no individual numerical value has been edited.

The two means agree whenever all specimens have equal valid reading counts, and can also coincide for particular arrangements of values. Numerical agreement does not eliminate the need to identify the observation unit. Genuine technical repeats can reveal reading variability or improve precision for a given specimen; they do not increase the number of independently prepared specimens. Weighting by measurement precision can be useful when its variance and correlation model is specified. Merely weighting by row count incorporates assumptions that need to match the actual measurement process.

## A missing value changes the denominator and sometimes removes a specimen mean

Suppose A02's only q value was not recorded. Its row and identifier remain, but q is missing. Its size is one, count is zero, and specimen mean is missing. A still has three registered specimens, but only two have computable means. The equal-specimen result becomes (2.1+3.2)/2=2.65 g/g. Reporting this as “the mean of three specimens” would conflate registration with numerical participation. The program therefore keeps both specimens and valid_specimens, distinguishing the number registered from the number contributing a valid representative value.

![Left: existing A01 records are copied while specimen count stays fixed. Right: missing A02 q leaves a registered row but zero valid numerical values.](https://ml-biomat.com/static/tutorials/python-scientific/figures/1cd94131485c50495871e2e5.svg?v=1cd94131485c)

Figure 3Left: existing A01 records are copied while specimen count stays fixed. Right: missing A02 q leaves a registered row but zero valid numerical values.

The default pandas `mean` skips missing numerical values and divides by the number of valid values. This allows a partially observed group to produce a summary, while the experimental record explains why values are missing. A failed file save, a broken specimen, and a value below a detection limit can call for different analysis decisions. This example preserves the missing state and reports its valid count. Filling A02 with zero would instead assert a measured absence of water uptake, changing the equal-specimen average to approximately 1.7667. That is a change in the input's meaning, not simply a different table format.

A missing grouping label creates a separate issue. If a row has no formulation label, default grouping excludes it from the formulation summaries. The main grouping calls use `dropna=False` to keep missing labels as a group that can be investigated. That choice is distinct from how a mean treats a missing numerical q. In practice, inspect blank labels, spelling, and surrounding spaces before counting groups. The strings “B” and “B ” differ and are not automatically combined because they look similar on screen.

The formulation table also retains the sample standard deviation of specimen means. This describes dispersion between specimen representatives, rather than repeated reading variation within one specimen. For A's means 2.1, 2.8, and 3.2, the mean is 2.7. Squared departures sum to 0.62; dividing by two and taking the square root gives approximately 0.5568 g/g. One valid specimen is insufficient for this sample standard deviation, so its value remains missing. Reporting zero would suggest an observed absence of between-specimen variation. Reading the mean, spread, and valid count together makes the summary's actual content clear.

$$
s_q=\sqrt{\frac{\sum_{j=1}^{J}(\bar q_j-\bar q_{\mathrm{equal}})^2}{J-1}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d6959d02159dd0ada26992e7.svg) | Sample standard deviation among valid specimen means, g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/5756278ec076431a907dc307.svg) | Mean reading for valid specimen j, g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/9e66413b5e17439d8aa63259.svg) | Equal-weight mean of these J specimen means, g/g |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | Valid-specimen index, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/70f3dc39744c98269cbe57ad.svg) | Number of valid specimens, dimensionless; at least two are required |
| ![Formula](https://ml-biomat.com/static/agent-math/a532e06315851dc3910227b7.svg) | Degrees of freedom in the deviations after estimating their mean from the same data |
| ![Formula](https://ml-biomat.com/static/agent-math/e8ca563c8033303e110f807c.svg) | Sum squared deviations, then take the square root to recover the original units |

Measure departures of specimen means from their shared center. Their deviations sum to zero, leaving J−1 degrees of freedom. A's deviations are −0.6,0.1,0.5 g/g, with squared sum 0.62; s_q=√(0.62/2)≈0.556776 g/g. This describes dispersion of specimen representatives. Interpreting the variance as a population estimate additionally requires independent specimens with comparable sampling distributions.

## Keep a summary table, and return group baselines to the original records

The six-row aggregate is convenient for comparing specimens. Sometimes, however, we want all eleven original readings with an additional column containing each reading's specimen mean. `transform('mean')` performs that task: it calculates within groups and returns the result aligned to the original rows. Both A01 rows receive 2.1, and all three A03 rows receive 3.2. The output still has eleven entries, so it can be assigned as a new column without manually copying values or assuming that a summary row position identifies an input row.

Subtracting the specimen-mean column from q gives within-specimen departures. A01 yields −0.1 and +0.1; A03 yields −0.2, 0, and +0.2. These describe where a particular reading lies relative to the other readings of that specimen. Departures sum to approximately zero within each group because of the definition of the mean. This checks alignment and arithmetic, rather than establishing instrument calibration or the absence of a systematic offset. A common upward shift in every reading disappears when those readings are centered on their own mean.

The output shape helps distinguish the operations. `agg` reduces each group to a summary row; `transform` returns a group-derived value for every original row. Filtering can retain complete groups that satisfy a stated condition, such as at least two valid technical readings. Such a condition should follow a defined quality rule, with excluded specimens recorded. Removing a group under that rule and removing individual readings under a numerical threshold produce different collections of experimental objects.

`pivot` addresses a different need: place specimens in rows and reading numbers in columns so that A03's three readings appear side by side. It rearranges values without deciding how duplicate cells should be combined. In the initial table, each specimen–reading combination occurs once, permitting a direct pivot. After copying A01, the combination is no longer unique. The copy identifier must then join the key, or the data must first be summarized by an explicit rule. A01's empty third column in the original wide table means that no third reading exists. It differs from a third reading that actually measured zero uptake.

## A complete program retaining each level from reading to formulation

The program starts from the `READINGS` dictionary. Each key identifies a specimen and each value is its list of technical readings. `make_table` expands this nested structure into rows with formulation, reading number, and copy number. The defaults copies=1 and missing=False reproduce the eleven original teaching records. The optional parameters explore weighting and missingness while preserving the original lists. Starting each calculation from the same explicit inputs makes the effect of a single change traceable.

`summarize` returns three objects: the specimen table, formulation table, and reading table augmented with within-specimen baselines. Its first aggregation summarizes specimens; its second summarizes formulations. Row means are calculated separately and mapped into the comparison table by formulation label. Label correspondence keeps A's result attached to A even if a table has been sorted. The next chapter extends this principle to combining several tables, where an explicit identity key continues to carry the relationship.

### Run the complete example

Use an environment with pandas, NumPy, and Matplotlib; replace en with zh for Chinese figures.

```
python main.py --output results --language en
```

### From readings to specimens and formulations

READINGS contains all constructed inputs. make_table builds records, summarize retains the aggregation levels, and plot_all produces the figures.

```
"""Follow technical readings through specimen and formulation summaries.

The values are constructed teaching data. Copying A01 readings below is a
weighting experiment; the copies are not additional physical measurements.
Run: python main.py --output results --language en
"""
from pathlib import Path
import argparse
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

READINGS = {'A01': [2.0, 2.2], 'A02': [2.8], 'A03': [3.0, 3.2, 3.4],
            'B01': [2.0, 2.2], 'B02': [2.5, 2.7], 'B03': [2.9]}
BLUE, ORANGE, INK = '#235f83', '#bd5838', '#1e303c'


def make_table(copies=1, missing=False):
    records = []
    for specimen, values in READINGS.items():
        for copy in range(copies if specimen == 'A01' else 1):
            for reading, value in enumerate(values, 1):
                records.append({'formulation': specimen[0], 'specimen': specimen,
                                'reading': reading, 'copy': copy + 1,
                                'q': np.nan if missing and specimen == 'A02' else value})
    return pd.DataFrame(records)


def summarize(table):
    specimens = (table.groupby(['formulation', 'specimen'], as_index=False, dropna=False)
                 .agg(q_mean=('q', 'mean'), rows=('q', 'size'), valid=('q', 'count')))
    formulations = (specimens.groupby('formulation', as_index=False, dropna=False)
                    .agg(q_equal=('q_mean', 'mean'), specimens=('specimen', 'size'),
                         valid_specimens=('q_mean', 'count'), sd_specimens=('q_mean', 'std')))
    row_means = table.groupby('formulation', dropna=False)['q'].mean()
    # Map by category label. Position alone is not a group identifier.
    formulations['q_rows'] = formulations['formulation'].map(row_means)
    traced = table.copy()
    traced['specimen_mean'] = traced.groupby('specimen')['q'].transform('mean')
    traced['within_specimen'] = traced['q'] - traced['specimen_mean']
    return specimens, formulations, traced


def plot_all(table, specimens, groups, output, language):
    zh = language == 'zh'
    tr = lambda z, e: z if zh else e
    available = {f.name for f in font_manager.fontManager.ttflist}
    fonts = [f for f in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','DejaVu Sans'] if f in available]
    plt.rcParams.update({'font.family': fonts if zh else ['DejaVu Sans'], 'font.size': 12,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'svg.fonttype': 'none', 'axes.unicode_minus': False})
    def save(fig, name):
        for ext in ['svg', 'png']:
            fig.savefig(output / f'{name}-{language}.{ext}', dpi=165, bbox_inches='tight')
        plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(13.8, 5.3), gridspec_kw={'width_ratios':[1.2, .9, 1]}, layout='constrained')
    for i, row in specimens.iterrows():
        values = table.loc[table.specimen == row.specimen, 'q'].to_numpy()
        offsets = np.linspace(-.14,.14,len(values)) if len(values)>1 else [0]
        axes[0].scatter(values, i+np.array(offsets), color=BLUE if row.formulation=='A' else ORANGE, s=45)
        axes[0].plot([row.q_mean-.03, row.q_mean+.03], [i,i], color=INK, lw=3)
    axes[0].set(yticks=range(6), yticklabels=specimens.specimen, xlabel='q / g g⁻¹',
                title=tr('a  11条读数，6个独立试样','a  11 readings, 6 independent specimens'))
    axes[0].invert_yaxis();axes[0].grid(axis='x',alpha=.15)
    axes[1].barh(np.arange(6)-.15, specimens.valid/np.repeat([6,5],3), height=.28,color=BLUE,label=tr('逐读数权重','Reading weights'))
    axes[1].barh(np.arange(6)+.15, np.ones(6)/3, height=.28,color=ORANGE,label=tr('试样等权','Equal specimens'))
    axes[1].set(yticks=range(6),yticklabels=specimens.specimen,xlim=(0,.62),xlabel=tr('配方内权重，无量纲','Weight within formulation'),title=tr('b  谁在平均值中占得更多','b  Who receives more weight'))
    axes[1].invert_yaxis();axes[1].legend(loc='lower right',fontsize=9)
    for i,row in groups.iterrows():
        axes[2].plot([i-.13,i+.13],[row.q_rows,row.q_equal],color='#9aa6ad',lw=1.5)
        axes[2].scatter(i-.13,row.q_rows,color=BLUE,s=65,label=tr('逐读数','Readings') if i==0 else None)
        axes[2].scatter(i+.13,row.q_equal,color=ORANGE,s=65,label=tr('试样等权','Equal specimens') if i==0 else None)
        axes[2].annotate(f'{row.q_rows:.4f}',(i-.13,row.q_rows),xytext=(-2,12),textcoords='offset points',ha='right',fontsize=10)
        axes[2].annotate(f'{row.q_equal:.4f}',(i+.13,row.q_equal),xytext=(2,-20),textcoords='offset points',ha='left',fontsize=10)
    axes[2].set(xticks=[0,1],xticklabels=['A','B'],xlim=(-.6,1.6),ylim=(2.25,2.95),ylabel='q / g g⁻¹',xlabel=tr('配方','Formulation'),title=tr('c  两个明确的平均问题','c  Two explicit averaging questions'))
    axes[2].legend(loc='upper right',fontsize=9);axes[2].grid(axis='y',alpha=.15)
    save(fig,'units-and-weights')

    fig,ax=plt.subplots(figsize=(13.5,6.4));ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
    ax.text(.02,.94,tr('2011：把分组计算组织成可复用的步骤','2011: organize grouped computation into reusable steps'),fontsize=19,weight='bold')
    ax.text(.02,.86,tr('Wickham的 split–apply–combine 思路；下方用本节构造读数演示。','Wickham’s split–apply–combine strategy, illustrated with this chapter’s constructed readings.'),fontsize=12)
    boxes=[(.02,.08,.25,.66),(.36,.08,.27,.66),(.73,.08,.25,.66)]
    for x,y,w,h in boxes:ax.add_patch(plt.Rectangle((x,y),w,h,facecolor='#edf3f4',edgecolor='#c5d2d9'))
    for x1,x2 in [(.28,.35),(.64,.72)]:ax.annotate('',xy=(x2,.43),xytext=(x1,.43),arrowprops={'arrowstyle':'->','lw':2,'color':INK})
    ax.text(.04,.68,tr('分开：按试样身份','Split: by specimen'),fontsize=14,weight='bold')
    ax.text(.04,.56,'A01   2.0, 2.2\nA02   2.8\nA03   3.0, 3.2, 3.4',fontsize=15,linespacing=2,va='top')
    ax.text(.04,.15,tr('6条A配方读数','6 readings for A'),fontsize=13)
    ax.text(.38,.68,tr('计算：每个试样一个均值','Apply: specimen mean'),fontsize=13,weight='bold')
    ax.text(.38,.56,'A01   (2.0+2.2)/2 = 2.1\nA02   2.8/1 = 2.8\nA03   (3.0+3.2+3.4)/3 = 3.2',fontsize=12.5,linespacing=2.3,va='top')
    ax.text(.38,.18,tr('保留编号\n与有效读数数','Retain identifiers\nand valid reading counts'),fontsize=12,va='top')
    ax.text(.75,.68,tr('合并：试样汇总表','Combine: summaries'),fontsize=13,weight='bold')
    ax.text(.75,.56,'A01   2.1\nA02   2.8\nA03   3.2',fontsize=14,linespacing=1.6,va='top')
    ax.plot([.75,.96],[.30,.30],color='#9baeb7',lw=1)
    ax.text(.75,.25,tr('下一轮：按配方再分组','Next grouping: formulation'),fontsize=12)
    ax.text(.75,.16,'A: (2.1+2.8+3.2)/3 = 2.7',fontsize=12)
    save(fig,'split-apply-combine')

    fig,axes=plt.subplots(1,2,figsize=(12.5,5.5),layout='constrained')
    copies=range(1,7);curve=[]
    for k in copies:
        _,g,_=summarize(make_table(k));curve.append(g.loc[g.formulation=='A','q_rows'].iloc[0])
    axes[0].plot(list(copies),curve,'o-',lw=2.5,color=BLUE,label=tr('逐读数平均','Mean over rows'))
    axes[0].axhline(2.7,color=ORANGE,lw=2.2,label=tr('3个试样等权','3 equally weighted specimens'))
    axes[0].set(xticks=list(copies),xlabel=tr('A01两条记录的保留份数 k','Copies k of the two A01 records'),ylabel='A: q / g g⁻¹',ylim=(2.1,2.9),title=tr('a  复制记录改变权重','a  Copied records change weights'))
    axes[0].legend(frameon=False);axes[0].grid(alpha=.15)
    absent=make_table(missing=True);s,g,t=summarize(absent)
    counts=pd.DataFrame({'rows':s.rows.to_numpy(),'valid':s.valid.to_numpy()},index=s.specimen)
    im=axes[1].imshow(counts,cmap='Blues',vmin=0,vmax=3,aspect='auto')
    axes[1].set(xticks=[0,1],xticklabels=[tr('行数 size','Rows: size'),tr('有效数 count','Valid: count')],yticks=range(6),yticklabels=counts.index,title=tr('b  A02缺失时，行仍然存在','b  An A02 row remains when q is missing'))
    for i in range(6):
        for j in range(2):axes[1].text(j,i,int(counts.iloc[i,j]),ha='center',va='center',fontsize=19,color='white' if counts.iloc[i,j]>=2 else INK)
    cb=fig.colorbar(im,ax=axes[1],ticks=[0,1,2,3],shrink=.75);cb.set_label(tr('条数','Count'))
    save(fig,'copies-and-missing')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('results'));parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    table=make_table();specimens,groups,traced=summarize(table)
    # A pivot rearranges unique cells. It does not select or average duplicates.
    wide=table.pivot(index='specimen',columns='reading',values='q')
    assert abs(groups.loc[0,'q_rows']-83/30)<1e-12
    assert abs(groups.loc[0,'q_equal']-27/10)<1e-12
    assert abs(groups.loc[1,'q_rows']-123/50)<1e-12
    assert abs(groups.loc[1,'q_equal']-38/15)<1e-12
    assert np.allclose(traced.groupby('specimen').within_specimen.sum(),0)
    _,missing_groups,_=summarize(make_table(missing=True))
    _,copied_groups,_=summarize(make_table(copies=6))
    for name,data in [('readings',table),('specimens',specimens),('formulations',groups),('trace',traced)]:data.to_csv(args.output/f'{name}.csv',index=False)
    wide.to_csv(args.output/'wide.csv')
    summary={'versions':{'pandas':pd.__version__,'numpy':np.__version__},'rows':len(table),'specimens':len(specimens),'A_row_mean':float(groups.q_rows.iloc[0]),'A_equal_mean':float(groups.q_equal.iloc[0]),'B_row_mean':float(groups.q_rows.iloc[1]),'B_equal_mean':float(groups.q_equal.iloc[1]),'A_missing_equal':float(missing_groups.q_equal.iloc[0]),'A_missing_valid_specimens':int(missing_groups.valid_specimens.iloc[0]),'A_six_copies_row_mean':float(copied_groups.q_rows.iloc[0]),'A_six_copies_equal_mean':float(copied_groups.q_equal.iloc[0]),'A_specimen_sd':float(groups.sd_specimens.iloc[0])}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    plot_all(table,specimens,groups,args.output,args.language)
    print(json.dumps(summary))


if __name__=='__main__':main()
```

The output contains readings.csv with eleven input rows, specimens.csv with six specimen summaries, formulations.csv with two formulation summaries, trace.csv with original readings and their centered departures, and wide.csv with a specimen-by-reading layout. A's two means are approximately 2.7667 and 2.7000; B's are 2.4600 and 2.5333. The program checks that centered departures sum to zero and uses explicit fractions to verify the principal means. Inspect how row counts and column names change across these files, then follow the corresponding function calls.

To adapt the example, first standardize column names and units and establish the range over which specimen identifiers are unique. Reading numbers can repeat because many specimens have a first reading. A specimen name reused on different dates or in different batches needs the relevant batch information in its key. Intermediate tables also support collaboration: another researcher can inspect the readings behind a specimen mean without rerunning every figure. A figure's reported n can come from an explicitly defined valid_specimens column rather than being guessed during plotting.

## Change the record structure and trace what moves

The experiment retains the same six specimens. Select one and follow its readings, representative mean, and two within-formulation weights. Then increase the number of copies of A01's two existing records. Every copy contains 2.0 and 2.2, so its specimen mean remains fixed. The reading points spread along their display offsets while the weight bars and A's row-weighted mean change together. The neighboring curve shows the full range from one to six copies, with the current choice marked, placing each individual adjustment in a broader numerical pattern.

### Trace an average back to its readings

Added copies repeat A01’s existing 2.0 and 2.2 readings. Select a specimen and compare its two weights.

[Figure: Specimen readings and means](https://ml-biomat.com/tutorials/python-scientific/p12/en/#P12-readings)

[Figure: Two within-formulation weighting rules](https://ml-biomat.com/tutorials/python-scientific/p12/en/#P12-weights)

[Figure: Record copies and two means](https://ml-biomat.com/tutorials/python-scientific/p12/en/#P12-curve)

Blue weights valid readings equally; orange weights specimens with valid means equally. Missing values remain missing, and copies do not add independent specimens.

At six copies, A01 supplies twelve of A's sixteen valid readings and receives weight 0.75 in the row-based calculation. Its equal-specimen weight remains one third. Marking A02 missing leaves two specimens with valid means, so A01 and A03 each receive one half and the equal-specimen mean becomes 2.65. The table still records A02's one row and zero valid values, distinguishing its continued registration from its contribution to the present numerical summary. Reset returns to the eleven original readings.

A useful experimental result can state the hierarchy directly: “Technical readings were first averaged within each specimen; the three independently prepared specimens of each formulation were then weighted equally.” This specifies the objects, order of calculation, and specimen count in one sentence. pandas turns that rule into repeatable operations, while raw records, intermediate tables, and plotted points preserve its interpretation. When formulation details, batches, and other measurements are joined next, the same identity keys ensure that additional information reaches the correct specimen.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P12.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [pandas: Group by — split-apply-combine](https://pandas.pydata.org/docs/user_guide/groupby.html)

   Official guide to grouping keys, missing labels, aggregation, and transformation.

   pandas BSD 3-Clause; API reference, original lesson prose/code/data.
2. [pandas: Summary statistics](https://pandas.pydata.org/docs/getting_started/intro_tutorials/06_calculate_statistics.html)

   Summarize selected numerical columns and distinguish size from count.

   pandas BSD 3-Clause; API reference, original lesson prose/code/data.
3. [pandas: GroupBy.aggregate](https://pandas.pydata.org/docs/reference/api/pandas.api.typing.DataFrameGroupBy.aggregate.html)

   Named aggregation and output column definitions.

   pandas BSD 3-Clause; API reference, original lesson prose/code/data.
4. [pandas: GroupBy.transform](https://pandas.pydata.org/docs/reference/api/pandas.api.typing.DataFrameGroupBy.transform.html)

   Return aligned group-derived results for the original rows.

   pandas BSD 3-Clause; API reference, original lesson prose/code/data.
5. [pandas: DataFrame.pivot](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pivot.html)

   Unique cells and reshaping without implicit aggregation.

   pandas BSD 3-Clause; API reference, original lesson prose/code/data.
6. [Wickham (2011): The Split-Apply-Combine Strategy for Data Analysis](https://www.jstatsoft.org/article/view/v040i01)

   Original paper on computational organization; chapter figures and data are original.

   JSS original article; historical reference, no reproduced figure or text.
