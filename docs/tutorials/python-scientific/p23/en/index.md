# Regression, Experimental Batches, and Model Diagnostics

Source: https://ml-biomat.com/tutorials/python-scientific/p23/en/
Language: en

Separate within-batch trends, batch baselines, and single-observation influence in eighteen traceable readings.

## Why can two increasing batches produce a decreasing pooled trend?

When adjusting formulation concentration, we often ask how much the material response changes per unit increase. Plotting every observation and fitting a straight line seems to answer that question. Experiments, however, are commonly performed in batches with different raw-material states, preparation conditions, or measurement baselines. If the higher concentrations happen to belong to the batch with lower overall readings, the pooled line reflects both concentration variation and batch differences.

This chapter uses eighteen explicitly constructed teaching readings. Batch A has three independent specimens at each of 1, 2, and 3 mmol/L; batch B has three at each of 4, 5, and 6 mmol/L. Within both batches, the response center rises by 2 kPa per 1 mmol/L increase. Batch B is shifted downward by 10 kPa. The three readings at each concentration receive offsets of −0.4, 0, and 0.4 kPa, retaining visible scatter within a condition. Every numerical result can therefore be traced to the construction.

We will use statsmodels to fit pooled and batch-adjusted models, establish the comparison represented by each coefficient, and inspect residuals and a controlled single-point perturbation. The route starts with the geometry of the observations, turns that geometry into columns of numbers, and then examines how software assigns a coefficient to each column.

## The historical aggregation problem also appears in scatterplots

In 1951, E. H. Simpson examined interaction and conditional relationships in contingency tables, showing why the handling of grouping information matters for interpretation. Those tables count categories, whereas this chapter uses continuous concentration and response. The shared issue is visible: when observations from different backgrounds are combined, between-group positions can dominate within-group variation. The historical discussion encourages examination of sample composition before interpretation of an overall trend.

![The same eighteen observations under pooled and batch-adjusted models. Colors identify batches; within-batch lines span observed concentrations only. Both panels share the response scale.](https://ml-biomat.com/static/tutorials/python-scientific/figures/fb1eef63baecddd2c1665ada.svg?v=fb1eef63baec)

Figure 1The same eighteen observations under pooled and batch-adjusted models. Colors identify batches; within-batch lines span observed concentrations only. Both panels share the response scale.

The pooled least-squares line has a slope of approximately −0.5714 kPa·L/mmol. Retaining batch gives two within-batch slopes of +2. These results answer different comparisons. The pooled model describes the overall relationship in this particular mixture of observations; the batch model estimates the concentration relationship while holding batch fixed. The comparison required by the research question determines which background information the model needs to retain.

Imagine two staircases at different elevations. Each rises as you move to the right, but the second staircase sits much lower. A line connecting the left of the first to the right of the second can slope downward. Batch acts like baseline elevation and concentration like position along the stairs. The analogy makes the structure visible, while the actual inference rests on the observations and the specified model.

The concentration ranges do not overlap here. The common slope is estimated from the three levels within each batch, while the batch contrast relies on the common straight-line form. A real experiment can compare batches more directly by including shared concentrations and matched controls. Such overlap reduces reliance on extrapolated shape and makes differences in batch-specific slopes easier to inspect.

Batch centers make the reversal decomposable. A has mean concentration 2 mmol/L and mean response 14 kPa, whereas B has mean concentration 5 mmol/L and mean response 10 kPa. The line connecting these centers slopes downward, while observations around each center trend upward. The pooled fit incorporates both sources of variation. Here equal batch sizes and a substantial vertical shift allow the between-batch direction to dominate the pooled slope.

## Give concentration and batch separate columns and explicit units

The pooled model gives every observation a common intercept and a concentration contribution. Adding batch introduces an indicator equal to 1 for batch B and 0 for batch A. It acts as a switch: A receives no added term, while B receives a fixed offset. This numerical encoding preserves category membership without treating A and B as values on a continuous scale.

$$
y_i=\beta_0+\beta_1c_i+\gamma z_i+\varepsilon_i
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a51d7c6c42d3bb0b61f865ba.svg) | Response of specimen i, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Specimen index, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/29928b2adca455a1420619c0.svg) | Specimen concentration, mmol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/51874f02b4c579417c89ce04.svg) | Batch indicator: 0 for A and 1 for B, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/a5318f0ad2a783837b048ae3.svg) | Batch A intercept, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/d05dff35bcc6d68d1a8ec42a.svg) | Common concentration slope within a batch, kPa·L/mmol. |
| ![Formula](https://ml-biomat.com/static/agent-math/7db9474e1e95a533a1714618.svg) | Baseline shift of B relative to A, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/df6c5ac19bbf29886eee1c95.svg) | Departure of the observation from the model center, kPa. |

With β₀ = 10 kPa, β₁ = 2 kPa·L/mmol, and γ = −10 kPa, batch B at 5 mmol/L has center 10 + 2 × 5 − 10 = 10 kPa. Its readings 9.6, 10, and 10.4 kPa correspond to departures of −0.4, 0, and 0.4 kPa.

The fitted A intercept is 10 kPa, the concentration coefficient is 2 kPa·L/mmol, and the B shift is −10 kPa. A specimen in A at 2 mmol/L has a predicted center of 10 + 2 × 2 = 14 kPa. A specimen in B at 5 mmol/L has a center of 10 + 2 × 5 − 10 = 10 kPa. Multiplying coefficient units by their variables makes every additive contribution have units of kPa, providing a useful consistency check.

The intercept refers to zero concentration, while the data begin at 1 mmol/L. Here it first serves to position a line. Replacing concentration with concentration minus a reference value can make the intercept correspond to a more relevant condition without changing predictions. Switching the reference batch likewise changes coefficient representation: with B as the baseline, A's relative shift becomes +10 kPa and both predicted lines remain identical.

A common concentration coefficient assumes parallel batch lines. If batches can respond differently to concentration, an interaction between concentration and the batch indicator adds a slope difference for B. This adds another parameter requiring support from the observations. The scientific mechanism and the plotted structure help decide whether that flexibility is needed.

A “linear model” is primarily linear in its unknown coefficients. A curved concentration response could be represented by adding a concentration-squared column with another coefficient, while retaining linear-regression computation. Coefficient interpretation would then change, and a single constant would no longer describe the local response rate with concentration. Establishing the simple model first and adding terms with a specific purpose keeps the interpretation readable as the model becomes more flexible.

## The formula becomes a matrix; fitting minimizes squared residuals

The statsmodels formula `response ~ concentration + C(batch)` places the response on the left and explanatory terms on the right. The tilde separates those roles, the plus adds a model term, and `C(batch)` explicitly treats batch as categorical. A formula includes an intercept by default and uses a reference category, avoiding redundant inclusion of every category indicator together with that intercept.

$$
\mathrm{SSE}=\sum_{i=1}^{N}(y_i-\hat y_i)^2=\sum_{i=1}^{N}r_i^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/54f0a043833cd180cb4470f2.svg) | Residual sum of squares, kPa²; least squares selects coefficients minimizing it. |
| ![Formula](https://ml-biomat.com/static/agent-math/738f6e53c5d5b713b7e0925a.svg) | N is the total of 18 specimens; i indexes them from 1 to N, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/e1db53f60a4ee89f7d43e0d6.svg) | Observed and fitted responses, both kPa; the hat marks a fitted value. |
| ![Formula](https://ml-biomat.com/static/agent-math/3a3efe8d09f46a481b251330.svg) | Observation minus prediction, kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | Sum squared residuals over all specimens. |

Three residuals at one concentration are −0.4, 0, and 0.4 kPa, contributing 0.32 kPa². Six conditions give 1.92 kPa², matching the batch fit. Signed residuals remain useful for examining the direction of departures.

The resulting design matrix contains three columns: an all-ones intercept column, a zero-or-one indicator for B, and concentration. Each row belongs to one specimen. Multiplying its entries by their coefficients and adding gives the prediction. Fitting chooses coefficients that minimize the sum of eighteen squared observation-minus-prediction differences. Squaring prevents positive and negative residuals from canceling and gives larger departures more influence on the objective.

`smf.ols(...).fit()` performs ordinary least squares. The program independently passes the generated matrix to NumPy's `lstsq` and verifies the same coefficients. Inspecting column names matters because formula-writing order need not match matrix order. Here the columns are intercept, B indicator, and concentration. Reading parameters by name avoids confusing a baseline shift with a slope.

The pooled residual sum of squares is approximately 104.7771 kPa², compared with 1.92 kPa² for the batch model. The latter can be checked directly from the specified offsets: six concentration conditions each contribute 0.16 + 0 + 0.16 = 0.32 kPa². Adding parameters generally reduces training-data squared error, so model choice also considers scientific meaning, sample structure, and behavior on new observations.

The all-ones intercept column becomes clear by examining individual rows. A specimen in A at 2 mmol/L has row [1, 0, 2]. Multiplication by intercept 10, B shift −10, and slope 2 gives 14. A specimen in B at 5 mmol/L has row [1, 1, 5], giving 10. These columns let categories and continuous variables enter the same calculation. They also explain why including an indicator for every batch usually requires changing the intercept convention to avoid redundant baseline information.

## Subtract batch means to see the within-batch comparison

The adjusted concentration coefficient can be recovered through a simple transformation. Calculate mean concentration and response separately for each batch, then subtract the appropriate pair of means from each observation. A is centered at (2 mmol/L, 14 kPa) and B at (5 mmol/L, 10 kPa). After subtraction, both groups surround the origin. Their overall height and position differences are removed, leaving within-batch variation visible.

![An original illustration of aggregation and grouping using the chapter data. Diamonds mark batch means at left. At right, each observation is centered within its batch; circles and crosses distinguish overlapping groups. Within-batch variation determines the common slope.](https://ml-biomat.com/static/tutorials/python-scientific/figures/909b1e068dc7420003cc1f2d.svg?v=909b1e068dc7)

Figure 2An original illustration of aggregation and grouping using the chapter data. Diamonds mark batch means at left. At right, each observation is centered within its batch; circles and crosses distinguish overlapping groups. Within-batch variation determines the common slope.

$$
\tilde c_i=c_i-\bar c_{g(i)},\quad\tilde y_i=y_i-\bar y_{g(i)},\quad\hat\beta_1=\frac{\sum_i\tilde c_i\tilde y_i}{\sum_i\tilde c_i^2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ca87a2688e1a8b679e738314.svg) | i is a specimen index and g(i) its batch A or B. |
| ![Formula](https://ml-biomat.com/static/agent-math/4ee6cc894911be326cbd4ad7.svg) | Original concentration, its batch mean, and centered concentration, all mmol/L. |
| ![Formula](https://ml-biomat.com/static/agent-math/e0dac0e62b851aa1eaef0194.svg) | Original response, its batch mean, and centered response, all kPa. |
| ![Formula](https://ml-biomat.com/static/agent-math/3c61858a79b95932ea457c4e.svg) | Estimated common within-batch slope, kPa·L/mmol. |
| ![Formula](https://ml-biomat.com/static/agent-math/5ca220bf09b42c86c851749f.svg) | Sum over all 18 specimens. |

Each batch has three repeats of concentration deviations −1, 0, and 1 mmol/L, giving denominator 12 (mmol/L)². Products with response deviations sum to 24 kPa·mmol/L; balanced ±0.4 kPa offsets cancel. The ratio is 2 kPa·L/mmol, matching the fit with batch intercepts.

For a common-slope model with separate batch intercepts, these centered coordinates give the same slope of 2. Concentration deviations within each batch are −1, 0, and 1 mmol/L, each repeated three times. Response-center deviations are −2, 0, and 2 kPa, with the balanced small offsets added. Summing products of horizontal and vertical deviations and dividing by the sum of squared horizontal deviations recovers the within-group relationship independently of the formula interface.

“Adjusting for batch” therefore has a specific meaning: account for each batch's baseline, then compare concentration differences within batches. Data support remains essential. If each batch had only one concentration, the two effects could not be separately identified from those observations. An unrecorded factor that changes with concentration needs attention through design, measurement, or a further model. The coefficient is interpreted in terms of the variation actually available.

Centering also reveals how concentration positions contribute to estimating a slope. At the mean concentration of a batch, centered concentration is zero, so that observation contributes zero directly to the slope numerator. It still helps locate the batch center and characterize scatter. Concentrations farther from the center supply greater horizontal spread and are particularly informative about slope. Covering a useful concentration range and adding repeats at one concentration improve different aspects of the design.

## Residuals reveal structure; influence identifies records to investigate

A residual plot isolates each point's vertical departure from the model. The pooled model leaves pronounced structure within both batches. Adding batch returns the residuals to the specified −0.4, 0, and 0.4 kPa offsets. In actual data, curvature can suggest an unsuitable linear shape, expanding scatter can suggest a changing error scale, and runs of similarly signed time-ordered residuals can suggest correlation. Diagnostics identify structure that deserves a scientific explanation.

![Top panels compare original pooled and batch residuals. Bottom panels add 6 kPa to specimen 18, calculate Cook distances, and refit to inspect slope sensitivity. Leaving out 18 is a diagnostic comparison.](https://ml-biomat.com/static/tutorials/python-scientific/figures/74c28e4a437743d12e6b6c15.svg?v=74c28e4a4377)

Figure 3Top panels compare original pooled and batch residuals. Bottom panels add 6 kPa to specimen 18, calculate Cook distances, and refit to inspect slope sensitivity. Leaving out 18 is a diagnostic comparison.

The program makes one traceable perturbation: add 6 kPa to specimen 18 while retaining the other seventeen readings. The adjusted concentration coefficient rises from 2 to 2.5, showing how a reading at the edge of the concentration range can influence a slope. Cook's distance summarizes a single observation's effect on fitted values; specimen 18 has a value of approximately 1.1487. It points toward a record worth checking through the original measurement, specimen conditions, and an independent repeat.

Leverage describes how unusual an observation's explanatory-variable position is. A residual describes its response departure. A point can be far out in concentration yet follow the fitted line closely, or occupy an ordinary concentration while departing strongly in response. Their impacts differ. Cook's distance incorporates both position and residual, giving information beyond a ranking of the largest responses. The program saves leverage, residual, and Cook's distance with each specimen index.

A diagnostic refit leaving out specimen 18 gives a slope of approximately 1.95862. This is slightly below the original 2 because the unperturbed specimen 18 already carried a +0.4 kPa offset. The refit is a sensitivity analysis demonstrating dependence on that observation. Data corrections follow examination of records and a defined processing rule; the full-data fit and the sensitivity result can both be retained.

Investigating an unusual observation can follow a concrete sequence: confirm the specimen identifier against the original file, inspect units and transcription, review instrument and preparation records, and repeat the measurement when appropriate. A confirmed entry error receives a documented correction; a genuine specimen difference becomes a feature needing explanation. Sensitivity analysis quantifies how strongly the result depends on that observation, while the experimental record determines the meaning of that dependence.

## A complete program with named coefficients and traceable diagnostics

The example keeps data construction, both fits, the centered-coordinate check, and the perturbation in one file. `params` contains named coefficients, `fittedvalues` predicts each observed specimen, `resid` gives corresponding residuals, and `get_influence` supplies diagnostics. New conditions are passed to `predict` as a DataFrame containing concentration and batch, preserving the original category coding.

### Complete example: formula regression, batch centering, and observation influence

Running creates two specimen tables, diagnostics, a numerical summary, and three figures. All teaching observations are explicitly generated in the program.

```
"""Fit concentration trends while preserving experimental batch identity."""
from pathlib import Path
import argparse,json
import numpy as np
import pandas as pd
import statsmodels
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
COLORS={'A':'#28658c','B':'#c26835'}


def data(offset=-10.,perturbation=0.):
    rows=[]
    for batch,levels in [('A',[1.,2.,3.]),('B',[4.,5.,6.])]:
        for concentration in levels:
            for residual in [-.4,0.,.4]:
                rows.append({'specimen':len(rows)+1,'batch':batch,'concentration':concentration,
                    'response':10+2*concentration+(offset if batch=='B' else 0)+residual})
    frame=pd.DataFrame(rows);frame.loc[17,'response']+=perturbation
    return frame


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    zh=args.language=='zh';tr=lambda z,e:z if zh else e;available={f.name for f in font_manager.fontManager.ttflist}
    plt.rcParams.update({'font.family':[f for f in ['Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','SimHei','DejaVu Sans'] if f in available],'font.size':12,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'grid.alpha':.15})
    def save(fig,name):
        fig.savefig(args.output/f'{name}-{args.language}.svg');fig.savefig(args.output/f'{name}-{args.language}.png',dpi=160);plt.close(fig)
    frame=data();pooled=smf.ols('response ~ concentration',data=frame).fit();adjusted=smf.ols('response ~ concentration + C(batch)',data=frame).fit()
    design=adjusted.model.exog;independent=np.linalg.lstsq(design,frame.response.to_numpy(),rcond=None)[0]
    assert np.allclose(independent,adjusted.params.to_numpy())
    centered=frame[['concentration','response']]-frame.groupby('batch')[['concentration','response']].transform('mean')
    centered_slope=float(np.dot(centered.concentration,centered.response)/np.dot(centered.concentration,centered.concentration))
    changed=data(perturbation=6.);changed_fit=smf.ols('response ~ concentration + C(batch)',data=changed).fit();influence=changed_fit.get_influence();without=smf.ols('response ~ concentration + C(batch)',data=changed.iloc[:-1]).fit()
    frame.to_csv(args.output/'specimens.csv',index=False);changed.to_csv(args.output/'perturbed-specimens.csv',index=False)
    diagnostics=pd.DataFrame({'specimen':changed.specimen,'fitted':changed_fit.fittedvalues,'residual':changed_fit.resid,'leverage':influence.hat_matrix_diag,'cooks_distance':influence.cooks_distance[0]});diagnostics.to_csv(args.output/'diagnostics.csv',index=False)
    fig,ax=plt.subplots(1,2,figsize=(12,5.8),layout='constrained')
    for batch,group in frame.groupby('batch'):
        for a in ax:a.scatter(group.concentration,group.response,color=COLORS[batch],label=tr(f'批次{batch}',f'Batch {batch}'),s=45)
        x=np.linspace(group.concentration.min(),group.concentration.max(),100);prediction=adjusted.predict(pd.DataFrame({'concentration':x,'batch':batch}));ax[1].plot(x,prediction,color=COLORS[batch],lw=2)
    x=np.linspace(1,6,200);ax[0].plot(x,pooled.predict(pd.DataFrame({'concentration':x})),color='#20313e',lw=2,label=tr('合并直线','Pooled line'))
    for a in ax:a.set(xlabel=tr('浓度 / mmol·L⁻¹','Concentration / mmol·L⁻¹'),ylabel=tr('响应 / kPa','Response / kPa'),ylim=(6.5,17));a.legend(frameon=False,fontsize=10);a.grid()
    ax[0].set_title(tr('合并所有点：斜率 −0.5714','All points pooled: slope −0.5714'));ax[1].set_title(tr('保留批次：共同斜率 +2','Retain batch: common slope +2'));save(fig,'regression')
    fig,ax=plt.subplots(2,2,figsize=(12,9),layout='constrained')
    for j,model in enumerate([pooled,adjusted]):
        for batch,group in frame.groupby('batch'):ax[0,j].scatter(group.concentration,model.resid.loc[group.index],color=COLORS[batch],s=42,label=batch)
        ax[0,j].axhline(0,color='#20313e',lw=1);ax[0,j].set(xlabel=tr('浓度 / mmol·L⁻¹','Concentration / mmol·L⁻¹'),ylabel=tr('残差 / kPa','Residual / kPa'),title=tr('合并模型的残差','Pooled-model residuals') if j==0 else tr('批次模型的残差','Batch-model residuals'));ax[0,j].legend(frameon=False)
    ax[1,0].bar(changed.specimen,influence.cooks_distance[0],color=[COLORS[b] for b in changed.batch]);ax[1,0].set(xticks=[1,3,6,9,12,15,18],xlabel=tr('试样编号','Specimen index'),ylabel=tr('Cook距离，无量纲','Cook distance, dimensionless'),title=tr('给18号读数增加6 kPa后','After adding 6 kPa to specimen 18'))
    slopes=[adjusted.params['concentration'],changed_fit.params['concentration'],without.params['concentration']]
    ax[1,1].scatter([0,1,2],slopes,s=65,color=['#20313e','#b64a35',COLORS['A']]);ax[1,1].plot([0,1,2],slopes,color='#8f9ca5',lw=1);ax[1,1].set(xlim=(-.5,2.5),xticks=[0,1,2],xticklabels=[tr('原数据','Original'),tr('18号+6','18 + 6'),tr('逐一检查：\n去掉18号','Diagnostic refit:\nleave out 18')],ylabel=tr('浓度系数 / kPa·L·mmol⁻¹','Concentration coefficient / kPa·L·mmol⁻¹'),title=tr('读数影响通过重新拟合核对','Check influence by refitting'))
    for a in ax.flat:a.grid(axis='y')
    save(fig,'diagnostics')
    fig,ax=plt.subplots(1,2,figsize=(12,5.8),layout='constrained')
    for batch,group in frame.groupby('batch'):
        ax[0].scatter(group.concentration,group.response,color=COLORS[batch],label=batch,s=40)
        ax[0].scatter(group.concentration.mean(),group.response.mean(),marker='D',s=100,edgecolor='#20313e',color=COLORS[batch])
        c=centered.loc[group.index];ax[1].scatter(c.concentration,c.response,color=COLORS[batch],s=55 if batch=='A' else 25,marker='o' if batch=='A' else 'x',label=batch)
    ax[0].plot([2,5],[14,10],color='#71808b',ls='--',label=tr('批次均值之间的方向','Direction between batch means'))
    ax[0].set(xlabel=tr('原浓度 / mmol·L⁻¹','Original concentration / mmol·L⁻¹'),ylabel=tr('原响应 / kPa','Original response / kPa'),title=tr('组间位置改变合并趋势','Between-group positions change the pooled trend'))
    ax[1].plot([-1.1,1.1],[-2.2,2.2],color='#20313e',label=tr('批次中心化斜率2','Within-batch centered slope 2'))
    ax[1].set(xlabel=tr('浓度 − 批次均值 / mmol·L⁻¹','Concentration − batch mean / mmol·L⁻¹'),ylabel=tr('响应 − 批次均值 / kPa','Response − batch mean / kPa'),title=tr('减去各批次均值，显出组内变化','Subtract each batch mean to expose within-group change'))
    for a in ax:a.legend(frameon=False,fontsize=9);a.grid()
    save(fig,'history')
    summary={'versions':{'numpy':np.__version__,'pandas':pd.__version__,'statsmodels':statsmodels.__version__,'matplotlib':matplotlib.__version__},'n':len(frame),
        'pooled_slope':float(pooled.params['concentration']),'pooled_intercept':float(pooled.params['Intercept']),'adjusted_slope':float(adjusted.params['concentration']),'adjusted_intercept_A':float(adjusted.params['Intercept']),'batch_B_shift':float(adjusted.params['C(batch)[T.B]']),
        'pooled_sse':float(pooled.ssr),'adjusted_sse':float(adjusted.ssr),'centered_slope':centered_slope,'design_columns':adjusted.model.exog_names,
        'perturbed_slope':float(changed_fit.params['concentration']),'leave18out_slope':float(without.params['concentration']),'specimen18_cook':float(influence.cooks_distance[0][-1]),'specimen18_leverage':float(influence.hat_matrix_diag[-1])}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary))


if __name__=='__main__':main()
```

Two specimen tables preserve the original observations and the version with 6 kPa added to specimen 18. The diagnostic table stores the specimen index, prediction, residual, leverage, and Cook's distance. The numerical summary retains the coefficients and squared-error totals discussed here. Statsmodels also provides standard errors, intervals, and tests, whose interpretation depends on the error structure. The balanced offsets in this teaching dataset are explicitly constructed, so the emphasis is on coefficients, fitting geometry, and sensitivity.

With experimental data, check missing values, category spelling, and units before fitting, and identify the rows actually used. Categories “A” and “A ” can become different groups, while mixed concentration units alter coefficient scales. Saving the cleaned input together with the result keeps the interpretation connected to specimens rather than leaving only a few numbers from a model summary.

## Move a batch, then trace the effect of one observation

The experiment changes B's overall offset, the additional perturbation of specimen 18, and the choice of pooled or batch model. The main view shows all eighteen observations and current fitted lines. A residual view shows departures for the same points. A coefficient view compares the pooled slope, the batch-adjusted slope, and the adjusted slope after leaving out specimen 18. All views are recalculated from the same observations.

### Batch, concentration, and a traceable specimen

[Figure: Observations and fitted lines](https://ml-biomat.com/tutorials/python-scientific/p23/en/#P23-data)

[Figure: Residuals of the same specimens](https://ml-biomat.com/tutorials/python-scientific/p23/en/#P23-residual)

[Figure: Slopes from three fits](https://ml-biomat.com/tutorials/python-scientific/p23/en/#P23-coefficients)

Blue identifies A and orange B; a black ring marks the traced specimen. Batch lines span observed concentrations only. The lower-right panel retains a leave-18-out diagnostic comparison.

Move B's shift from −10 kPa toward zero. The batches approach one shared trend, the pooled slope rises toward 2, and the within-batch slope stays at 2. Restore the −10 kPa shift and add 6 kPa to specimen 18, then examine how both models and that point's residual respond. Selecting a specimen highlights it in both scatterplots and displays its concentration, observation, and prediction.

The leave-18-out result is always shown as a diagnostic comparison; it does not remove a point from the main dataset. This keeps the full fit visible alongside its sensitivity. An unusual reading can first be located in a graph and then investigated through the experimental record, producing a clearer scientific judgment than automatic deletion.

Trace specimen 18 through the original equation. Before perturbation, it belongs to B, has concentration 6 mmol/L, and reads 12.4 kPa. The adjusted model predicts 12 kPa, giving a residual of 0.4 kPa. After adding 6 kPa, the fit itself changes. Its new residual is therefore not simply the old residual plus 6, because the prediction has moved too. This distinguishes the imposed change in an observation from the departure remaining after refitting.

## A regression statement should identify the conditions of comparison

The result can be expressed as follows: under the parallel-line model, a 1 mmol/L concentration increase within the same batch corresponds to a 2 kPa increase in mean response, with B shifted by −10 kPa relative to A. The statement specifies conditions, units, and comparison. Reporting only that “the coefficient is 2” leaves the model, batch adjustment, and concentration units unstated.

Regression can describe associations, predict responses at specified conditions, adjust recorded background differences, and assess sensitivity to particular observations. Establishing a causal effect of changing concentration additionally relies on randomization, controls, or another design that separates jointly changing factors. Keeping these tasks clear makes model coefficients useful language connecting data, experimental conditions, and scientific interpretation.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P23.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [statsmodels 0.14.6: Fitting models using formulas](https://www.statsmodels.org/v0.14.6/example_formulas.html)

   Formula semantics for categories, intercepts, and interactions.

   BSD-3-Clause; technical reference
2. [statsmodels: OLS](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLS.html)

   Ordinary least squares and the design-matrix interface.

   BSD-3-Clause; technical reference
3. [statsmodels: OLSInfluence](https://www.statsmodels.org/stable/generated/statsmodels.stats.outliers_influence.OLSInfluence.html)

   Leverage, Cook distance, and observation sensitivity.

   BSD-3-Clause; technical reference
4. [Simpson (1951): The Interpretation of Interaction in Contingency Tables](https://doi.org/10.1111/j.2517-6161.1951.tb00088.x)

   Original discussion of grouping, aggregation, and conditional relationships; continuous data and figures here are original.

   Copyrighted article; historical reference only
