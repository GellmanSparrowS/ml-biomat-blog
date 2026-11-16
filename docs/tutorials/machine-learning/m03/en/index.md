# Can the score be trusted? Evaluation and experimental design

Source: https://ml-biomat.com/tutorials/machine-learning/m03/en/
Language: en

From perfect recognition of familiar objects to detecting none of the rare events, design tests that answer the practical question.

## An examination should resemble the future job

A defect detector scores 99% accuracy on test images. That appears promising, but suppose six photographs were taken of each component and five entered training while the sixth entered testing. The model may recognize an individual component's surface pattern rather than the distinction between defective and acceptable components. Its score then addresses a different problem from inspecting entirely new components. Evaluation begins by defining what “new” means: another record from a familiar object, an unfamiliar object, a later time, or a different instrument and location. That definition comes before choosing a metric.

Training data determine model parameters. Validation data guide preprocessing, algorithm and hyperparameter choices. Test data assess an already specified workflow. Their roles depend on which results influence decisions, not merely on file names. If inspecting test errors leads to a feature change, those observations have joined development. Continuing development is useful, and a new independent evaluation set can assess the revised procedure. A clear experimental design traces information: which observations entered each fit, which results guided each choice, and which results assess the whole process at the end.

Two explicit generators organize this chapter. The first creates six similar records for each of 120 objects and assigns random object-level classes, exposing the benefit of recognizing identity. The second creates 2,400 independent rare-event observations for studying scores, thresholds, costs and uncertainty. The datasets answer separate questions; the grouped-data effect and the rare-event metrics should not be presented as one combined result. The complete code retains generation rules, split indices and individual predictions, allowing every summary and figure to be recalculated.

## Rows, objects and time imply different questions

A random split is appropriate when observations are approximately independent and future observations come from a comparable population. Stratification approximately preserves class proportions, preventing a small class from disappearing by chance, but still splits rows. When several rows belong to one person, specimen or video, stratification does not prevent identity information crossing the boundary. Group splitting assigns the whole object to one side. If deployment concerns unfamiliar institutions, the group may need to be the institution. The prediction objective and data-generating process determine the grouping unit, rather than whichever split yields the highest score.

![Left: six records for each of the first twelve objects. Blue shows test rows and all rows belonging to test objects; grouped splitting aligns them. Right: test accuracy over twenty actual splits.](https://ml-biomat.com/static/tutorials/machine-learning/figures/878659a3c0b0ff995cd73229.svg?v=878659a3c0b0)

Figure 1Left: six records for each of the first twelve objects. Blue shows test rows and all rows belonging to test objects; grouped splitting aligns them. Right: test accuracy over twenty actual splits.

Each object in the first experiment has eight fixed features and six records with small perturbations. Classes are assigned randomly to objects. A nearest-neighbor model averages 100% accuracy over twenty random row splits because a test record almost always finds a training record from the same object. Holding out entire objects gives mean accuracy 44.5%. There is no designed relationship between the features and a new object's class, so performance fluctuates around chance; finite objects and repeated splits do not force an observed mean of exactly 50%. The contrast separates recognizing familiar identities from generalizing to new objects.

A time split trains on the past and evaluates on the future. Randomly shuffling dates in a sales forecast lets future trends enter training and changes the information available relative to deployment. Rolling evaluation can expand the training window or keep its length fixed to emphasize recent conditions. If a target summarizes the next seven days, labels near the split boundary overlap in calendar time, requiring an appropriate gap. The gap should follow the target window and information delay. Removing a date column alone cannot remove future information already encoded in other features.

Preprocessing can leak information too. Selecting the most target-correlated features using all observations before cross-validation lets validation labels guide the representation. Imputing from a whole-dataset mean lets future observations affect the transformation. A Pipeline refits learned preprocessing together with the model inside each training fold. A physically defined unit conversion can be fixed in advance; a data-estimated scale, encoding or selection needs an explicit account of which samples it used. Treating the entire learned workflow as the estimator makes this information flow easier to inspect.

## Cross-validation also needs protection from selection

K-fold cross-validation partitions development data into K parts, training on K−1 parts and validating on the remaining part in turn. Different observations receive a validation role, and choices depend less on one accidental split. The training sets overlap substantially, so the K scores are not K independent experiments. Applying an ordinary independent-sample formula can therefore produce an unjustifiably narrow confidence interval. Cross-validation organizes fitting and comparison; the statistical interpretation of its scores still depends on the dependence introduced by the splitting scheme.

Trying many parameter configurations and reporting the best validation score includes the winning configuration's favorable noise. Cawley and Talbot's 2010 study analyzed this form of overfitting in model selection: a finite-data validation criterion can itself be overoptimized. Nested cross-validation separates the work. Within each outer training set, an inner search selects parameters. The selected procedure is then evaluated on the outer test fold, which did not participate in that search. The outer scores assess the selection procedure, rather than retrospectively treating the chosen parameter as though it had been specified before seeing the data.

The example performs a three-fold inner search over four regularization settings on 1,440 training records. Four outer folds yield average-precision scores of approximately 0.134, 0.242, 0.170 and 0.217. Their spread reflects the difficulty of evaluating rare events with finite samples. A separate set of 480 validation records selects an action threshold, and the final 480 records assess the fixed model and threshold. The threshold and ablation experiments use a logistic model with C=1 fixed in advance. Nested search separately demonstrates a full parameter-selection procedure on the same training data; its selected estimator does not replace that fixed model. Outer-fold scores therefore evaluate the search procedure, while the 480 test records evaluate the fixed model and decision rule.

Grouping and temporal constraints should hold at inner and outer levels. A grouped outer split does not justify allowing the same object across inner folds. With limited computation, begin with a small predeclared search and a few reasonable models, then expand promising regions under an explicit budget. Candidate sets, budgets and primary metrics belong in the comparison design. Repeatedly viewing a small validation set while inventing new approaches also expands the effective search. Retaining unsuccessful configurations and selection rules makes the final conclusion correspond to the experiment actually performed.

## A metric specifies how errors are counted

Regression predicts a continuous quantity. Mean absolute error shares the target unit and describes average discrepancy. Root mean squared error also returns to the original unit but emphasizes large discrepancies. For errors of one, one, one and nine, MAE is three and RMSE is about 4.58. R squared instead compares squared error against a constant based on the test-set mean; it can be negative when the model does worse than that benchmark on the evaluated sample. Percentage errors become unstable near zero targets, so metric choice should consider whether zero has a meaningful interpretation.

$$
\operatorname{MAE}=\frac1n\sum_i|y_i-\widehat y_i|,\quad\operatorname{RMSE}=\sqrt{\frac1n\sum_i(y_i-\widehat y_i)^2},\quad R^2=1-\frac{\sum_i(y_i-\widehat y_i)^2}{\sum_i(y_i-\overline y)^2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/532fd9de01c5518cbb6ef73b.svg) | Test sample count and observation index, unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/bc34a3022c550d4606408025.svg) | Observation, prediction and test-observation mean in the same target units. |
| ![Formula](https://ml-biomat.com/static/agent-math/6db5824810b0dc847a6952b1.svg) | Mean absolute and root mean squared error, both in target units. |
| ![Formula](https://ml-biomat.com/static/agent-math/12373d1e32275b1b5a25ca4b.svg) | Dimensionless relative squared-error score; the expression requires a nonconstant test target. |

Errors 1,1,1,9 have MAE 3 and mean square 21, giving RMSE≈4.58. A residual sum of squares 12 against a mean-baseline sum 8 gives R²=−0.5.

Classification distinguishes four outcomes. A true positive detects an actual event; a false positive raises an alarm without an event; a false negative misses an event; a true negative correctly stays quiet. Precision asks what fraction of alarms are real, whereas recall asks what fraction of actual events were found. Their denominators differ. F1 combines precision and recall through a harmonic mean but does not include true negatives or automatically encode a practical cost. In multiclass settings, macro averaging weights classes equally, micro averaging pools counts, and frequency-weighted averaging follows class prevalence. State which population receives which weight.

$$
\operatorname{precision}=\frac{TP}{TP+FP},\quad\operatorname{recall}=\frac{TP}{TP+FN},\quad F_1=\frac{2TP}{2TP+FP+FN}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5c6fbc7d3eeff17e6d411272.svg) | True-positive, false-positive, false-negative and true-negative observation counts, unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/5da11f9b5e39e563d6d0093a.svg) | Precision, recall and F1, ranging from 0 to 1; zero denominators require an explicit convention. |

With TP=14, FP=58 and FN=17, precision is 14/72≈0.1944, recall 14/31≈0.4516 and F1=28/103≈0.2718. The denominators 72 and 31 refer to alerts and actual events respectively.

Ranking concerns useful results near the top of a finite list, such as the ten search results a reader will inspect. Precision@k counts the relevant fraction among the first k positions; Recall@k measures how much of the relevant set was recovered. NDCG discounts lower-ranked results and normalizes by the ideal ordering, so placing the most useful result first differs from placing it tenth. Evaluation also needs a candidate universe and a definition of observable relevance. An unclicked item may never have been exposed; treating it as a confirmed negative can mix the display mechanism with user preference.

$$
\operatorname{DCG}@k=\sum_{r=1}^k\frac{2^{g_r}-1}{\log_2(r+1)},\qquad\operatorname{NDCG}@k=\frac{\operatorname{DCG}@k}{\operatorname{IDCG}@k}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/542032cf3c2e3bf464d7b459.svg) | Cutoff and rank index beginning at 1. |
| ![Formula](https://ml-biomat.com/static/agent-math/57b0453fa50cc773dbe10a6f.svg) | Nonnegative graded relevance at rank r; this formula uses exponential gain, unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/cecbf47d4b809626cad8fea7.svg) | Discounted cumulative gain, its ideal maximum for the same relevance labels, and normalized gain; zero IDCG requires a defined no-relevance convention. |
| ![Formula](https://ml-biomat.com/static/agent-math/14ae3fefbbf822ee29c5d5c8.svg) | Base-two logarithm, increasing the discount at later positions. |

For relevance order (0,1), DCG@2=1/log₂3≈0.6309. Ideal order (1,0) has IDCG=1, giving NDCG≈0.6309. The ideal order itself scores 1.

ROC-AUC and average precision use continuous scores to evaluate ranking across thresholds. The ROC horizontal axis divides false positives by all negative observations, so a small rate can still imply many false alarms when negatives are abundant. A precision–recall curve directly shows the fraction of alerts that are real events. Average precision weights precision by increases in recall and is not numerically identical to trapezoidal integration of a PR curve. Here the test positive fraction is about 6.46%, ROC-AUC is 0.763 and AP is 0.175. Their differing scales reflect different questions, not a reason to report whichever looks largest.

## How 93.5% accuracy can detect no events

The rare-event test set contains 31 positive observations among 480 records. Predicting negative for every record already achieves 93.54% accuracy. At the default threshold of 0.5, the fitted logistic regression does exactly that, missing every event. The result identifies a mismatch between the default decision threshold and the intended use. The model still assigns different probabilities to observations, and their ranking contains information. A threshold can therefore be selected on validation data according to action costs, instead of treating high accuracy as evidence of useful event detection.

$$
C(t)=c_{FP}FP(t)+c_{FN}FN(t),\qquad t^*=\frac{c_{FP}}{c_{FP}+c_{FN}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/621165602b9172491c95f47c.svg) | Decision threshold and total error cost; scores≥t trigger positive decisions, with stated cost units. |
| ![Formula](https://ml-biomat.com/static/agent-math/31d949ea1f6e1748f611c952.svg) | False-positive and false-negative counts at the threshold. |
| ![Formula](https://ml-biomat.com/static/agent-math/bab89fdc9fbcb80ac2f93ac8.svg) | Positive cost per false alarm and missed event, in cost units per event. |
| ![Formula](https://ml-biomat.com/static/agent-math/9a7778e03e3c5bdd4653d82c.svg) | Theoretical threshold for calibrated probabilities, fixed error costs and zero correct-decision cost; distinct from the empirical validation threshold. |

With 58 false alarms and 17 misses at costs 1 and 10, total cost is 228. The theoretical threshold 1/11≈0.0909 compares action cost (1−p)cFP with inaction cost pcFN. Empirical validation here selects 0.14.

![Left: probabilities for 480 test records. Center: cost over 480 validation records and the selected threshold 0.14. Right: test precision–recall curve; the dashed line marks prevalence.](https://ml-biomat.com/static/tutorials/machine-learning/figures/91d2b3e7281e5e0925d7bd2d.svg?v=91d2b3e7281e)

Figure 2Left: probabilities for 480 test records. Center: cost over 480 validation records and the selected threshold 0.14. Right: test precision–recall curve; the dashed line marks prevalence.

Assign one cost unit to a false alarm and ten to a missed event. Searching thresholds on the validation set selects 0.14. Applying that fixed threshold to the test set yields fourteen detections, seventeen misses and 58 false alarms, with cost 228. The default threshold costs 310. Lowering the threshold improves this specific objective while requiring more alerts to be processed. Detection, alert count and cost should be read together rather than retaining only the number that improved. If each alert requires human review, the 58 false alarms represent a concrete additional workload.

When probabilities are calibrated, error costs are constant and correct decisions cost zero, comparing the expected cost of acting against not acting gives a theoretical threshold. Empirical validation selection instead uses the observed cost curve and can accommodate imperfect calibration. Both approaches need a definition of where costs came from and whether event prevalence changes after deployment. If prevalence falls, the fraction of true events among alerts can decrease even when conditional discrimination remains similar. Calibration, distribution shift and threshold updates are developed further in the reliability chapter.

## Turn a threshold into a cost ledger

Twenty fixed observations, colored by true class. Scores at or above the dashed threshold trigger alerts. Probability is unitless; matrix entries count records; costs use illustrative units.

[Figure: Scores, confusion matrix and costs](https://ml-biomat.com/tutorials/machine-learning/m03/en/#M03-plot)

The interactive example contains twenty fixed scores and labels. Moving the threshold changes which observations trigger an action without retraining their scores. Changing the missed-event cost leaves the confusion matrix unchanged but alters the cost ledger. Separating these effects distinguishes an improved predictive model from a different decision rule applied to the same model. When no alert is issued, precision has a zero denominator and the interface displays it as undefined. This describes the decision accurately rather than assigning an arbitrary zero or one that could be mistaken for measured performance.

## Should the next step add data or change the model?

A learning curve compares training and validation performance across training-set sizes. With little data, a high training score and low validation score may move closer together as more data reduce sensitivity to individual observations. If both curves plateau at a low level, collecting more of the same observations may offer less benefit than improving the representation, model form or labels. The curve is not an automatic diagnosis, but it converts “try more training” into a more specific experiment. Its interpretation also depends on whether the score reflects the application's actual objective.

![Learning curves for logistic regression and a decision tree using 1,440 development records. Points are three-fold means and shading is one between-fold standard deviation. Splits and the AP metric are shared.](https://ml-biomat.com/static/tutorials/machine-learning/figures/9c76cd59324105d05822def5.svg?v=9c76cd593241)

Figure 3Learning curves for logistic regression and a decision tree using 1,440 development records. Points are three-fold means and shading is one between-fold standard deviation. Splits and the AP metric are shared.

The experiment compares logistic regression with an unrestricted decision tree using the same three training-side folds and AP on both axes. A tree can fit its training observations very closely while retaining a large gap to validation. Logistic regression imposes a more restricted form and does not reach the same near-perfect training score. Shading shows one standard deviation across three folds, describing split variability rather than a 95% confidence interval. Positive-event counts also change with training size, so apparent curve fluctuations should be interpreted alongside the scarcity of those observations.

Bias and variance provide a more systematic language. Under squared loss, at a fixed input, average predictions over many independently drawn training sets. The difference between that average and the true conditional mean contributes bias; variation of predictions around their average contributes variance; observation randomness contributes irreducible noise. This decomposition depends on the loss and the source of randomness. A single training–validation gap is not itself a direct measurement of estimator variance. Flexible models may reduce representation bias while increasing sensitivity, and regularization, ensembles and additional data affect different parts of that trade-off.

An ablation evaluates a specific component, such as a feature group, augmentation rule or network block. Keep splits, budgets, metrics and selection procedures aligned except for the factor being studied; when each method is retuned, report the allocation of tuning resources. Here a twelve-feature model is compared with a model retaining only the first three features. Both are refitted, then their individual Brier losses are compared on the same test records. The experiment concerns the predictive contribution of the retained feature set. It does not identify a causal effect of an individual feature.

## Magnitude, stability and a statistical test answer different questions

A score depends on training observations, test observations and any randomized fitting procedure. Before averaging repetitions, identify what was repeated: initialization, training sampling or test-object sampling. Each exposes a different uncertainty. The example fixes the two fitted models and draws 2,000 paired bootstrap samples from the 480 test records. The same sampled indices are applied to both models, retaining their observation-by-observation correspondence. This estimates test-sampling variation conditional on the fitted models. Including training uncertainty would require a repeated workflow that also refits the models.

$$
B=\frac1n\sum_i(p_i-y_i)^2,\qquad\overline d=\frac1n\sum_i\left[(p_i^{\rm reduced}-y_i)^2-(p_i^{\rm full}-y_i)^2\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/532fd9de01c5518cbb6ef73b.svg) | Test record count and index; correlated objects require grouped resampling. |
| ![Formula](https://ml-biomat.com/static/agent-math/043e1e9a3c94510bfcdeec48.svg) | Predicted positive probability and binary observed label, unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/8d1edb3e2ede488762ecd888.svg) | Mean squared probability error and paired reduced-minus-full difference, both unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/d9b761f767dac28327d36769.svg) | Separate fits using 3 and 12 features, evaluated on matched test observations. |

For a positive observation, probabilities 0.4 and 0.7 give losses 0.36 and 0.09 and a difference 0.27. For a negative observation, square each predicted probability. Paired resampling uses the same indices for both models.

![Left: paired test-record bootstrap of Brier differences for two fixed fitted models, with 2,000 replicates and percentile endpoints in orange. Right: four explicitly illustrative p-values and Holm adjustment, separate from the computed experiment on the left.](https://ml-biomat.com/static/tutorials/machine-learning/figures/3f58498fba502767a988b2c5.svg?v=3f58498fba50)

Figure 4Left: paired test-record bootstrap of Brier differences for two fixed fitted models, with 2,000 replicates and percentile endpoints in orange. Right: four explicitly illustrative p-values and Holm adjustment, separate from the computed experiment on the left.

The mean Brier loss of the reduced model minus that of the full model is approximately 0.00347. Its percentile bootstrap interval is about 0.000046 to 0.00715, with positive values favoring the full model's probability forecasts. Yet both models predict no positive events at threshold 0.5. Their decisions are identical, leaving no discordant pairs for a paired classification test; the code returns p=1. These outcomes are compatible: probability estimates changed without crossing the action threshold. A comparison must therefore specify whether it concerns probabilities, ranking, actions or cost before choosing a test.

An effect size states how much changed, such as missed events avoided per thousand records or a reduction in average loss. A confidence interval describes precision under a specified sampling procedure. A p-value describes the probability, under the stated null hypothesis and test conditions, of a statistic at least as extreme as the observed one. It is neither the probability that the null hypothesis is true nor a measure of practical value. If records are correlated within objects, bootstrap objects together. If the intended conclusion concerns retrained models, repeat fitting rather than only resampling fixed predictions.

Testing many models, metrics and subgroups increases the chance of obtaining a small p-value by accident. Four illustrative values in the plot are 0.001, 0.018, 0.04 and 0.3. Holm adjustment orders them and accounts for the remaining comparisons, producing 0.004, 0.054, 0.08 and 0.3. It controls the probability of at least one false rejection within the chosen family. A broad exploratory search may instead use an appropriate false-discovery-rate procedure. Defining primary comparisons in advance and retaining the scope of exploratory comparisons keeps statistical conclusions connected to the original question.

## Why can finite observations tell us about future errors?

Learning theory formalizes a practical concern: how far can observed training error be from expected error on new observations from the same distribution? The PAC viewpoint separates an acceptable approximation error from an acceptable failure probability. Connected to Valiant's 1984 work on learnability, it asks for a sufficiently accurate rule with high probability under explicit assumptions rather than perfection on every possible sample. Computational efficiency is another part of learnability: an existence guarantee does not automatically supply a fast executable algorithm for finding the desired rule.

$$
R(h)\le\widehat R_n(h)+\sqrt{\frac{\ln(2|\mathcal H|/\delta)}{2n}}\qquad\text{for all }h\in\mathcal H
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/233c3fbb57e116ed8a26799e.svg) | A classification rule, a fixed finite candidate family and its size. |
| ![Formula](https://ml-biomat.com/static/agent-math/23a91d1904bf8a4deea703bf.svg) | Expected population 0/1 loss and empirical mean 0/1 loss on n IID observations, both unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/33a17c452e0b6e09211ac3be.svg) | Sample count and failure probability between 0 and 1; the bound holds simultaneously with probability at least 1−delta. |
| ![Formula](https://ml-biomat.com/static/agent-math/aefc7a76c9ed1e58f8195e33.svg) | Natural logarithm; the expression combines a bounded-loss Hoeffding bound and union bound. |

With 100 candidates, n=1000 and delta=0.05, the allowance is √(ln4000/2000)≈0.0644. Concentration controls deviations for one rule; adding failure probabilities across candidates gives a bound valid throughout the search family.

The finite-class bound displays three relationships. More independent observations tighten the bound. A larger candidate set creates more opportunities to select an accidentally favorable rule. Requiring higher confidence enlarges the uncertainty allowance. With one hundred candidate rules, one thousand observations and failure probability 0.05, the additional term is approximately 0.0644. It is often wider than the observed discrepancy because it simultaneously covers all candidates and many possible data distributions. Independent, identically distributed observations and bounded loss are essential to the stated form; it does not repair the identity leakage demonstrated earlier.

A continuously parameterized model has infinitely many candidates, making a simple rule count unhelpful. VC dimension instead asks how many suitably chosen points a classifier family can label in every possible binary way. A one-direction threshold on a real line can shatter one point but not two ordered points. Lines in a plane can shatter three noncollinear points, while no arrangement of four points permits every labeling to be separated. This measures the expressive capacity of a family and is related to, but not universally identical to, its number of parameters. It turns an intuition about flexibility into an analyzable object.

Theory and empirical assessment perform complementary jobs. Bounds explain relationships among sample size, complexity and confidence. Group tests, time tests, cost curves and error inspection examine the concrete task. The complete workflow connects them: define the future observation before choosing a split; define the action before choosing a metric and threshold; then use repetitions and paired comparisons to describe the magnitude and variability of differences. Evaluation becomes evidence for the next experimental decision rather than a solitary number on a leaderboard.

### Complete evaluation: splits, thresholds, learning curves and paired comparisons

Requires NumPy, SciPy, scikit-learn and Matplotlib. Run python main.py --output results --language en. Generation, splitting, fitting, bootstrap and plotting are included; summary.json and experiment_data.npz retain results.

```
"""Evaluation protocols, thresholds and repeated comparisons on known generators."""
import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split,GroupShuffleSplit,StratifiedKFold,GridSearchCV,cross_val_score,learning_curve
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,average_precision_score,roc_auc_score,precision_recall_curve,confusion_matrix
from scipy.stats import binomtest

def main(output,language):
 out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh';rng=np.random.default_rng(33)
 plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False})
 def t(z,e):return z if zh else e
 def save(fig,n):fig.savefig(out/f'{n}-{language}.svg',bbox_inches='tight');plt.close(fig)
 # Object identity has no relation to its assigned class, but repeated views reveal identity.
 identities=rng.normal(0,3,(120,8));labels=rng.integers(0,2,120);groups=np.repeat(np.arange(120),6)
 Xg=identities[groups]+rng.normal(0,.12,(720,8));yg=labels[groups];random_scores=[];group_scores=[];split_examples=[]
 for seed in range(20):
  tr,te=train_test_split(np.arange(720),test_size=.25,random_state=seed,stratify=yg)
  gt,ge=next(GroupShuffleSplit(n_splits=1,test_size=.25,random_state=seed).split(Xg,yg,groups))
  for dest,a,b in [(random_scores,tr,te),(group_scores,gt,ge)]:
   m=make_pipeline(StandardScaler(),KNeighborsClassifier(n_neighbors=1));m.fit(Xg[a],yg[a]);dest.append(accuracy_score(yg[b],m.predict(Xg[b])))
  if seed==0:split_examples=[te,ge]
 fig=plt.figure(figsize=(11,5),layout='constrained');gs=fig.add_gridspec(1,2,width_ratios=[1.3,1]);ax=fig.add_subplot(gs[0,0]);matrix=np.zeros((4,72));
 for k,idx in enumerate(split_examples):
  matrix[k*2]=np.isin(np.arange(72),idx);matrix[k*2+1]=np.isin(groups[:72],groups[idx])
 ax.imshow(matrix,aspect='auto',cmap='Blues',vmin=0,vmax=1);ax.set_yticks(range(4),[t('随机：测试行','Random: test rows'),t('随机：测试对象的全部行','Random: rows of test objects'),t('分组：测试行','Grouped: test rows'),t('分组：测试对象的全部行','Grouped: rows of test objects')]);ax.set(xlabel=t('前12个对象，每个6行','First 12 objects, six rows each'));ax.set_xticks(np.arange(2.5,72,6),np.arange(12));
 for x in np.arange(5.5,72,6):ax.axvline(x,color='white',lw=1)
 ax=fig.add_subplot(gs[0,1]);ax.boxplot([random_scores,group_scores],tick_labels=[t('随机行','Random rows'),t('新对象','New objects')],showmeans=True);ax.set(ylim=(0,1.05),ylabel=t('测试准确率','Test accuracy'));ax.grid(axis='y',alpha=.2);save(fig,'splits')
 # A distinct independent-row rare-event classification experiment.
 X,y=make_classification(n_samples=2400,n_features=12,n_informative=5,n_redundant=2,weights=[.94,.06],flip_y=.01,class_sep=1.,random_state=33)
 idx=np.arange(len(y));tr,tmp=train_test_split(idx,test_size=.4,stratify=y,random_state=33);va,te=train_test_split(tmp,test_size=.5,stratify=y[tmp],random_state=33)
 model=make_pipeline(StandardScaler(),LogisticRegression(C=1,max_iter=1000));model.fit(X[tr],y[tr]);pv=model.predict_proba(X[va])[:,1];pt=model.predict_proba(X[te])[:,1]
 thresholds=np.linspace(0,1,201);fn_cost=10
 def counts(a,b,q):tn,fp,fn,tp=confusion_matrix(a,b>=q,labels=[0,1]).ravel();return {'tn':int(tn),'fp':int(fp),'fn':int(fn),'tp':int(tp),'cost':int(fp+fn_cost*fn)}
 costs=[counts(y[va],pv,q)['cost'] for q in thresholds];qstar=float(thresholds[np.argmin(costs)]);test_default=counts(y[te],pt,.5);test_selected=counts(y[te],pt,qstar)
 precision,recall,_=precision_recall_curve(y[te],pt)
 fig,axs=plt.subplots(1,3,figsize=(12,3.8),layout='constrained');axs[0].hist([pt[y[te]==0],pt[y[te]==1]],bins=np.linspace(0,1,21),stacked=True,color=['#167d87','#d48745'],label=['0','1']);axs[0].axvline(qstar,color='#523e67',ls='--');axs[0].set(xlabel=t('测试预测概率','Test predicted probability'),ylabel=t('样本数','Observations'));axs[0].legend(title=t('真实类别','True class'))
 axs[1].plot(thresholds,costs,color='#167d87');axs[1].axvline(qstar,color='#d48745',ls='--');axs[1].set(xlabel=t('候选阈值','Candidate threshold'),ylabel=t('验证集成本：FP+10FN','Validation cost: FP+10FN'))
 axs[2].plot(recall,precision,color='#167d87');axs[2].axhline(y[te].mean(),ls='--',color='#9aabb4');axs[2].set(xlabel=t('召回率','Recall'),ylabel=t('精确率','Precision'),xlim=(0,1),ylim=(0,1.02));save(fig,'threshold')
 # Nested tuning estimates the entire selection procedure on training data only.
 inner=StratifiedKFold(3,shuffle=True,random_state=34);outer=StratifiedKFold(4,shuffle=True,random_state=35)
 search=GridSearchCV(make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000)),{'logisticregression__C':[.01,.1,1,10]},cv=inner,scoring='average_precision',n_jobs=1)
 nested=cross_val_score(search,X[tr],y[tr],cv=outer,scoring='average_precision');search.fit(X[tr],y[tr])
 sizes=np.array([.15,.3,.5,.75,1]);curves={};fig,axs=plt.subplots(1,2,figsize=(11,4),layout='constrained')
 for ax,(name,est) in zip(axs,[('Logistic',make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000))),('Tree',DecisionTreeClassifier(random_state=33))]):
  ns,train,valid=learning_curve(est,X[tr],y[tr],cv=inner,train_sizes=sizes,scoring='average_precision',shuffle=True,random_state=33,n_jobs=1)
  for vals,label,col in [(train,t('训练','Train'),'#d48745'),(valid,t('验证','Validation'),'#167d87')]:
   ax.plot(ns,vals.mean(1),'o-',label=label,color=col);ax.fill_between(ns,vals.mean(1)-vals.std(1),vals.mean(1)+vals.std(1),alpha=.15,color=col)
  ax.set(title=name,xlabel=t('每折训练样本数','Training observations per fold'),ylabel=t('平均精确率 AP','Average precision'),ylim=(0,1.02));ax.legend();curves[name]={'sizes':ns.tolist(),'train':train.tolist(),'validation':valid.tolist()}
 save(fig,'learning')
 # Paired test-object bootstrap, conditional on the fitted models.
 ablated=make_pipeline(StandardScaler(),LogisticRegression(C=1,max_iter=1000));ablated.fit(X[tr,:3],y[tr]);pa=ablated.predict_proba(X[te,:3])[:,1]
 full_loss=(pt-y[te])**2;abl_loss=(pa-y[te])**2;dif=abl_loss-full_loss;boot=[]
 for _ in range(2000):b=rng.integers(0,len(te),len(te));boot.append(dif[b].mean())
 ci=np.quantile(boot,[.025,.975]);b=int(np.sum((pt>=.5)==y[te]) - np.sum(((pt>=.5)==y[te])&((pa>=.5)==y[te])))
 c=int(np.sum((pa>=.5)==y[te]) - np.sum(((pt>=.5)==y[te])&((pa>=.5)==y[te])))
 pvalue=float(binomtest(b,b+c,.5).pvalue) if b+c else 1.
 rawp=np.array([.001,.018,.04,.3]);order=np.argsort(rawp);adj_sorted=np.maximum.accumulate(rawp[order]*(len(rawp)-np.arange(len(rawp))));holm=np.empty_like(rawp);holm[order]=np.minimum(adj_sorted,1)
 fig,axs=plt.subplots(1,2,figsize=(11,3.8),layout='constrained');axs[0].hist(boot,bins=35,color='#167d87',alpha=.85);axs[0].axvline(0,color='#6a7783',ls='--');axs[0].axvline(ci[0],color='#d48745');axs[0].axvline(ci[1],color='#d48745');axs[0].set(xlabel=t('删减模型−完整模型：Brier差','Reduced minus full model: Brier difference'),ylabel=t('重抽样次数','Bootstrap replicates'))
 axs[1].plot(np.arange(1,5),rawp,'o-',label=t('原始p值（教学示例）','Raw p-values (illustration)'),color='#167d87');axs[1].plot(np.arange(1,5),holm,'s-',label='Holm',color='#d48745');axs[1].axhline(.05,color='#6a7783',ls='--');axs[1].set(xlabel=t('检验编号','Test index'),ylabel='p',xticks=[1,2,3,4],ylim=(0,.35));axs[1].legend();save(fig,'uncertainty')
 summary={'group_random_accuracy_mean':float(np.mean(random_scores)),'group_heldout_accuracy_mean':float(np.mean(group_scores)),'train_n':len(tr),'validation_n':len(va),'test_n':len(te),'test_positive_n':int(y[te].sum()),'threshold':qstar,'default':test_default,'selected':test_selected,'always_negative_accuracy':float(1-y[te].mean()),'test_roc_auc':float(roc_auc_score(y[te],pt)),'test_average_precision':float(average_precision_score(y[te],pt)),'nested_average_precision':nested.tolist(),'best_inner_ap':float(search.best_score_),'brier_difference':float(dif.mean()),'brier_bootstrap95':ci.tolist(),'mcnemar_discordant':[b,c],'mcnemar_exact_p':pvalue,'holm_p':holm.tolist(),'learning_curves':curves}
 (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');np.savez(out/'experiment_data.npz',X=X,y=y,train=tr,validation=va,test=te,probability=pt,ablated_probability=pa,group_X=Xg,group_y=yg,groups=groups,bootstrap=np.array(boot))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--language',choices=['zh','en'],default='en');a=ap.parse_args();main(a.output,a.language)
```

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M03.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [scikit-learn — Cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)

   Grouped, stratified and temporal splitting.

   BSD-3-Clause
2. [scikit-learn — Model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)

   Precise definitions of classification, regression and ranking metrics.

   BSD-3-Clause
3. [Cawley & Talbot (2010), Over-fitting in Model Selection](https://www.jmlr.org/papers/volume11/cawley10a/cawley10a.pdf)

   Overfitting the model-selection process itself.
4. [MIT — Learnability and VC Dimension](https://gradml.mit.edu/supervised/learnability_and_vc/)

   PAC learning, finite families and VC dimension.
5. [Columbia — Introduction to PAC Learning](https://www.cs.columbia.edu/~aho/cs3261/Lectures/L22-Introduction_to_PAC_Learning.html)

   Historical learnability question and computational efficiency.
