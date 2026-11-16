# Trees and forests: combining different decision rules

Source: https://ml-biomat.com/tutorials/machine-learning/m30/en/
Language: en

Read a split, then investigate ensembles through actual tree diversity, out-of-bag records and correlated features.

## How can one question at a time produce a complex decision?

When choosing fruit, a person may check color, firmness and surface damage in sequence, changing the next question according to the previous answer. A decision tree expresses this conditional reasoning as a computable structure. Each internal node asks whether a feature crosses a threshold and sends the observation down one branch. A leaf returns class proportions or an average response. Instead of forcing the whole input space into one straight boundary, the tree can use different rules in different regions. Threshold effects and conditional feature relationships therefore fit naturally into its representation.

Readability changes rapidly with tree size. A two-level tree can be inspected rule by rule, while a tree with hundreds of leaves is difficult to understand visually. Slightly changing the training observations can also change an early split and much of the resulting structure. A forest uses these differences: grow many trees from altered data and feature choices, then combine predictions. This chapter first calculates an individual split, then examines constraints on a tree, useful sources of diversity and why duplicating the same tree many times provides no comparable benefit.

Two tasks organize the figures. Noisy moons illustrate a depth-two tree and its partition of feature space. A separate dataset of one thousand observations and nine features compares predictors, with one feature nearly duplicating another. Every evaluated method shares 750 training records and 250 test records. Accuracy, probability log loss and out-of-bag estimates remain available together. This connects readable rules with actual computation and independent testing, rather than using an attractive tree drawing as a substitute for a performance assessment.

## Follow a prediction through the tree and into feature space

Begin at the root and read its feature and threshold. A satisfied condition follows the left branch; otherwise take the right, repeating until a leaf is reached. Training class counts in that leaf determine its estimated probability. With uniform observation weights, eighty positives and twenty negatives give a positive probability of 0.8. A regression leaf usually returns its target mean. The output remains constant within a leaf region, making a standard CART tree a piecewise-constant approximation. It does not automatically fit a new sloping regression surface inside every leaf.

![A depth-two classifier fitted to 200 moon observations. Nodes display thresholds, Gini, counts, class distributions and decisions; this small tree explains structure.](https://ml-biomat.com/static/tutorials/machine-learning/figures/4d34378ce7a0446782df46f0.svg?v=4d34378ce7a0)

Figure 1A depth-two classifier fitted to 200 moon observations. Nodes display thresholds, Gini, counts, class distributions and decisions; this small tree explains structure.

Nodes display their condition, impurity, sample count and class distribution. Counts show how many records support a rule; distributions show how mixed the resulting group remains. Two leaves predicting the same class can still have very different proportions, such as 51% and 98%. These proportions are estimated from the training observations reaching each leaf. Small leaves fluctuate substantially, and a pure leaf's zero or one probability can be costly when a new observation disagrees. Later log-loss results expose those confident mistakes even when overall class accuracy looks reasonable.

![Left: piecewise-constant probability regions of the same small tree. Right: all five split errors for six regression observations, minimized at 3.5.](https://ml-biomat.com/static/tutorials/machine-learning/figures/6bccfe73fcbd136c133ee39f.svg?v=6bccfe73fcbd)

Figure 2Left: piecewise-constant probability regions of the same small tree. Right: all five split errors for six regression observations, minimized at 3.5.

In the coordinate plane, every split cuts along one feature axis. Leaf regions become rectangles or intersections of axis-aligned conditions, and additional depth creates more regions to approximate a curved boundary. A strictly monotonic feature transformation changes numerical thresholds while preserving order, so many splits still separate the same records. Trees therefore usually depend less on standardization than distance-based models. Missing-value treatment, categorical encoding and floating-point effects can nevertheless change the actual computation and should be checked in the chosen implementation.

CART chooses the best available local feature-threshold split at the current node, then recurses into its children. This is greedy search rather than enumeration of all possible complete trees. Two nearly equivalent early choices can lead to quite different downstream structures. Interpreting a tree consequently involves more than displaying the final diagram. Its rules arise from a particular sample and a local optimization procedure; repeated fits can reveal whether the important early decisions remain stable under plausible data variation.

Piecewise-constant predictions also determine extrapolation. If every training temperature is below 40 degrees Celsius, inputs of 45 and 60 degrees may follow the same rightmost path and receive the same leaf value. When the application requires continuation of a physical trend, consider a model with that trend structure or a tree variant fitting a regression inside leaves, then evaluate outside the original range. Averaging many ordinary trees does not create a mechanism that was absent from their leaves. Inspecting feature ranges and terminal rules reveals this behavior before a forecast is used in a different operating regime.

## What makes one cut better than another?

A classification node is highly mixed when its classes are equally common and relatively pure when almost all observations share one class. Gini impurity is the probability that two independently drawn labels from the node's class proportions disagree. It equals 0.5 for equally frequent binary classes and zero for a pure node. Entropy measures mixing through logarithmic information instead. The criteria can choose different individual splits, but both compare the parent with the sample-weighted average impurity of its children.

$$
G=1-\sum_{c=1}^Kp_c^2,\quad H=-\sum_{c=1}^Kp_c\log_2p_c,\quad\Delta I=I_P-\frac{n_L}{n_P}I_L-\frac{n_R}{n_P}I_R
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/162b3577db3a5ef438ec5a18.svg) | Gini impurity and class entropy; G is unitless, H is in bits, and 0log0 is zero. |
| ![Formula](https://ml-biomat.com/static/agent-math/23101535a78b5a0b7f96efde.svg) | Class count, class index and node class proportions, summing to one. |
| ![Formula](https://ml-biomat.com/static/agent-math/0f60d2a597bb8013e28d25d3.svg) | Parent, left and right nodes and their counts; child counts sum to the parent count. |
| ![Formula](https://ml-biomat.com/static/agent-math/cc87fcda8a2145b3494ee548.svg) | Impurities under one shared criterion and their reduction, for uniformly weighted classification; the gain has criterion units. |

A parent with five positives and five negatives has G=0.5. Children with 1/4 and 4/1 class counts each have G=0.32, so gain is 0.18. Entropy falls from 1 bit to about 0.7219 bits, giving gain 0.2781 bits.

Weighting by child size matters. A split producing a pure group of two while leaving 98 mixed observations should not assign that tiny group half of the decision weight. Weighting by sample fractions evaluates the improvement across all observations. Information gain subtracts weighted child entropy from parent entropy; Gini reduction performs the analogous calculation with Gini values. With observation weights, weighted totals replace raw counts. A cost-sensitive weighting scheme can therefore change the direction in which a tree grows, not merely the final label reported by a fixed tree.

Regression has no class proportions, so a split can instead compare squared deviations from the mean within each child. The right panel uses six ordered inputs with responses 1,1,2,6,7,7. Splitting at 3.5 leaves means 4/3 and 20/3 and a total within-child sum of squares 4/3. Other candidate thresholds have larger errors. This small example explains why the regression tree separates low and high responses and identifies the observations and squared differences behind the phrase “variance reduction.”

$$
\operatorname{SSE}(A)=\sum_{i\in A}(y_i-\overline y_A)^2,\quad\operatorname{gain}=\operatorname{SSE}(P)-\operatorname{SSE}(L)-\operatorname{SSE}(R)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/54be1efeb49676ff8c1329e5.svg) | A node observation set and parent, left and right sets. |
| ![Formula](https://ml-biomat.com/static/agent-math/42ee64482fbba1d88dd2092a.svg) | Observation index, response and within-node response mean, with response units. |
| ![Formula](https://ml-biomat.com/static/agent-math/74e6b44ae4fc5c77f51ba9ee.svg) | Within-node squared-error sum and its decrease, in squared-response units. |

For targets(1,1,2,6,7,7), parent mean 4 gives SSE 44. The two three-point means are 4/3 and 20/3, each with SSE 2/3. Their sum is 4/3 and the reduction 128/3≈42.6667.

Impurity improvement is a training objective rather than a generalization score. Unrestricted splitting can eventually isolate individual observations, drive training impurity to zero and encode measurement noise as rules. Continuous-feature candidates generally lie between adjacent distinct values. Features with many distinct values offer more opportunities to find an apparently favorable split, influencing impurity-based importance. Independent permutation assessment and the dependence among features therefore belong alongside accumulated training improvement when interpreting a variable's contribution.

The same impurity framework extends to many classes by including every class proportion. Digits or multiple fault categories therefore require no separate geometric principle. Class weights change those proportions and split decisions: increasing the weight of rare faults makes their separation more influential. It also changes the weighted proportions reported by leaves. If the intended output is an event probability in the deployment population, evaluate those probabilities against the actual population mix and suitable calibration observations. Weighting a learning objective and estimating an unweighted population frequency are different statistical operations, even when both calculations use the same tree structure.

## When should a tree stop growing?

Maximum depth limits questions along a root-to-leaf path. Minimum leaf size requires each terminal rule to retain enough observations. Maximum leaf count limits the number of final regions. These controls address rule length, local support and total complexity, so depth alone is incomplete. One deep branch may cover few records, while a shallower but broad tree can still have many leaves. Read the structure together with the number of observations supporting its terminal decisions.

$$
R_\alpha(T)=R(T)+\alpha|\mathcal L(T)|
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b5a8a6e0c58abbfa6ec2dcd0.svg) | Candidate tree, leaf set and leaf count. |
| ![Formula](https://ml-biomat.com/static/agent-math/586d0d3d830f3827601c2df2.svg) | Sample-weighted training impurity across leaves, using one consistent classification criterion. |
| ![Formula](https://ml-biomat.com/static/agent-math/e8e41357d56827d913d4f97e.svg) | Nonnegative complexity price per leaf and total objective, in the corresponding impurity units. |

A ten-leaf tree with risk 0.10 and a four-leaf tree with risk 0.16 have objectives 0.15 and 0.18 at alpha 0.005. At alpha 0.02 they become 0.30 and 0.24, favoring the smaller tree.

Cost-complexity pruning compares the training error added by removing a subtree against the number of leaves removed. Larger penalties make retaining each leaf more expensive. The example generates candidate pruning strengths only from training data and selects among them by three-fold training-side validation; the 250 test records remain outside that process. The full tree has 59 leaves and the selected tree eleven. Test accuracy increases from 85.6% to 88.4%, while log loss falls from about 5.19 to 0.479. Pruning reduces some extreme, incorrect probabilities as well as changing class decisions.

The experiment does not require pruning to improve every dataset. Abundant observations and a complex real boundary may make aggressive pruning discard useful structure. Validation chooses a trade-off under the current conditions. A development-derived candidate path and its inner best score serve selection; independent testing evaluates the resulting workflow. To study variation in that selection procedure, place it inside an outer evaluation loop rather than repeatedly changing the pruning range after viewing the same test outcomes.

The interactive example isolates one local choice. Ten ordered labels remain fixed while you move a split and switch between Gini and entropy. The display updates child observations, class fractions and weighted improvement. An extreme split can create a tiny pure child with little overall gain; a more central split that separates the classes can improve the whole node more substantially. Building this numerical intuition makes the many individual decisions inside a complete tree easier to interpret.

## How much does this split improve?

Ten observations are ordered by feature values 1 through 10 and colored by true class. Each bar shows weighted impurity reduction for one candidate cut.

[Figure: Node split and impurity gain](https://ml-biomat.com/tutorials/machine-learning/m30/en/#M30-plot)

## Resampling makes unstable trees complement one another

A bootstrap sample draws n times with replacement from n training records. Some observations appear repeatedly, while others are absent. Each resample changes the empirical distribution and potentially the tree's splits. Bagging applies this procedure to many base estimators and combines their outputs. Regression generally averages predictions; classification can vote or average probabilities. The implementation here averages class probabilities from its trees. If individual trees respond strongly to sample perturbations and those responses are not perfectly synchronized, averaging can reduce their variability.

$$
P(\text{record omitted})=\left(1-\frac1n\right)^n\approx e^{-1},\quad\mathbb E[N_{\rm OOB}]=B\left(1-\frac1n\right)^n
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7650612bb33f7ec603d9bbfb.svg) | Original training-record count and number of independently bootstrapped trees. |
| ![Formula](https://ml-biomat.com/static/agent-math/c44375a21549caa3f590b2e2.svg) | Number of trees that omitted a given training record, measured in trees. |
| ![Formula](https://ml-biomat.com/static/agent-math/4f4d0e8dc3cc1608cce6e48f.svg) | Probability, expectation and exponential base; the approximation applies for large n. |

Each draw misses the specified record with probability 1−1/n. Multiplying over n independent replacement draws gives the omission probability. For n750 and B120, the expected count is 44.116 trees; one tree uses roughly 63.2% distinct records.

Breiman's 1996 bagging work and 2001 random-forest study explored an initially surprising possibility: instability of an individual learner can provide material for a better combined predictor. If every resample produces identical predictions, averaging one hundred copies changes nothing. If deviations partly cancel, the aggregate becomes more stable. Independent measurements offer a useful analogy, provided we also ask whether the observers share the same miscalibrated instrument. A shared error survives the increase in observer count.

$$
\operatorname{Var}\!\left(\frac1B\sum_{b=1}^B Z_b\right)=\rho\sigma^2+\frac{1-\rho}{B}\sigma^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6ed376fee9c98c195228f7c6.svg) | Number and index of predictors and random prediction at the same input, in response units. |
| ![Formula](https://ml-biomat.com/static/agent-math/0b55f8c2ddff1b47486bb264.svg) | Common prediction variance and common pairwise correlation; variance has squared-response units and correlation is unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/24a405123360399a5aca597f.svg) | Variance over the specified data/model randomness in this equal-variance, equal-correlation teaching model. |

For variance 1 and ten predictors, zero correlation gives average variance 0.1, while correlation 0.3 gives 0.37. Increasing to one hundred predictors gives 0.307; the shared 0.3 component remains.

Under the simplifying conditions of equal prediction variances and equal pairwise correlations, the variance expression separates the effects of adding trees and reducing correlation. Increasing tree count only reduces the part that can average away; the correlated component remains as a floor. Real trees need not satisfy these equalities exactly, but the calculation provides a clear design direction. Bagging is often useful for high-variance deep trees. An already stable base estimator may change little under resampling and gain correspondingly little from averaging.

With 120 bagged trees, test accuracy is 89.2%, compared with 85.6% for the unpruned single tree. Out-of-bag accuracy is 92.0%, different from the independent test result because both the evaluated observations and the number of contributing trees differ. Averaging probabilities also does not ensure that every metric improves equally: bagging log loss is approximately 0.653, higher than the pruned tree's 0.479. Retaining those outcomes reveals whether an ensemble improved discrete decisions, probability estimates or both.

Variation among trees describes changes caused by resampling and feature randomization for the available dataset. Future observation noise, collecting an entirely new training dataset and changes in the input population are additional sources of uncertainty. When the objective is a prediction interval with a stated coverage, define which source and prediction target the interval concerns, then use a corresponding probabilistic or calibration procedure. Plotting quantiles across tree predictions describes disagreement among ensemble members. A separate construction is needed to turn that disagreement into an interval designed to cover future observations under stated conditions.

## Why restrict the features considered at each node?

Different bootstrap samples may still select the same dominant feature at the root, producing similar tree structures. A random forest adds another source of variation: at each node, randomly select a subset of candidate features and search for a split within that subset. Some trees temporarily lack the strongest feature and must exploit alternatives. Randomness is useful only through its consequences; too few candidates can weaken every tree. Inspect individual performance, error similarity and final ensemble performance together rather than treating maximum diversity as the goal.

![Left: seven configurations on the same 250 test observations. Right: individual accuracy, ensemble accuracy and measured error correlation across feature-subset sizes.](https://ml-biomat.com/static/tutorials/machine-learning/figures/c4d98598ad1d451c06b6d64f.svg?v=c4d98598ad1d)

Figure 3Left: seven configurations on the same 250 test observations. Right: individual accuracy, ensemble accuracy and measured error correlation across feature-subset sizes.

The example considers one, three or all nine features per node. Mean individual-tree accuracies are approximately 79.7%,84.9% and 85.2%, while mean pairwise correlations of test-error indicators are 0.224,0.323 and 0.431. Forest accuracies are 91.6%,92.0% and 88.8%. On this split the intermediate setting balances individual ability and diversity. The plotted correlations are an empirical teaching diagnostic over 250 test observations, distinct from the specifically defined theoretical strength and correlation quantities in Breiman's paper. Their shared idea is to examine predictive ability and dependence jointly.

Adding trees mainly reduces Monte Carlo variation in an average prediction, while consuming memory and prediction time. It does not alter local fitting capacity in the same way as continually deepening a single tree. Feature-subset size, minimum leaf size, sample fraction and depth change the base estimators themselves. Fix these settings first and inspect whether out-of-bag performance and predictions stabilize as trees are added. Grouped and temporal applications still need deployment-matched evaluation; random resampling does not automatically remove observation dependence.

A path through one tree explains that tree's decision, not the entire forest's calculation. For an individual observation, inspect distributions of reached leaf probabilities or an appropriate local explanation of the average predictor. For global behavior, examine feature importance, partial responses and grouped errors. State which object an explanation concerns: a base tree, an aggregated prediction or a population-level relationship. A visually convenient representative tree should not silently stand in for an ensemble whose predictions arise from many different paths.

## What can observations omitted from a tree tell us?

A training record absent from one tree's bootstrap sample is out of bag for that tree. Predict the record using only trees that did not train on it, then aggregate such predictions across records. This provides an internal evaluation signal while using the data for training across the ensemble. With 750 training observations and 120 trees, the experiment averages 44.04 out-of-bag trees per record, close to the theoretical expectation 44.12. The histogram displays the full count distribution instead of pretending every record receives exactly the same number of evaluation trees.

![Left: impurity importance and test permutation accuracy decrease, which use different definitions; error bars show standard deviation over ten permutations. Right: out-of-bag tree counts across 120 bootstrap samples.](https://ml-biomat.com/static/tutorials/machine-learning/figures/c7f17eebee3d0dcc50cbb0b1.svg?v=c7f17eebee3d)

Figure 4Left: impurity importance and test permutation accuracy decrease, which use different definitions; error bars show standard deviation over ten permutations. Right: out-of-bag tree counts across 120 bootstrap samples.

The isolation unit is a record. If related records from the same object remain in the sampled training data, holding out one row does not withhold object identity. Out-of-bag estimates are therefore useful internal diagnostics under the relevant independent-record assumptions, while unfamiliar-object or future-time deployment needs the corresponding external split. Repeatedly choosing many settings from out-of-bag scores also turns that signal into a tuning resource. An independent assessment of the selected workflow retains its role after that selection.

Impurity importance accumulates training impurity reductions credited to each splitting feature and normalizes the totals. It is convenient but can favor features offering many candidate thresholds and distribute contributions across correlated variables. Permutation importance instead shuffles a feature on a specified evaluation set and measures the score decrease, asking how much the fitted model relies on that feature under the evaluated distribution. It does not retrain the model. Because shuffling changes relationships among features, the intervention used for a highly dependent dataset needs an explicit definition.

Feature x₈ is x₀ plus small noise. Permuting them separately decreases accuracy by only 0.6 and 0.36 percentage points on average, because the unaltered counterpart retains similar information. Permuting the two together with one shared row permutation decreases accuracy by 10.24 points. The difference reflects distinct questions: whether one column is replaceable versus whether the pair carries useful information. It is not a failed arithmetic addition of individual importance scores. Dependence structure and perturbation design belong next to every interpretation of these values.

Resource use follows the actual tree structures. Predicting one observation traverses a path in every tree, so both tree count and path length contribute to work. Stored nodes, feature indices and thresholds occupy memory. With the same number of trees, a larger minimum leaf size often reduces the number of nodes; equal tree counts therefore do not establish equal cost. Record model size, repeated batch prediction timings and held-out quality together. Separate one-time fitting cost from repeated serving cost, since a model trained once and queried millions of times faces a different trade-off from a frequently refitted exploratory analysis.

## Random thresholds, direct voting and a learned combination

Extra Trees introduces randomized candidate thresholds and selects a useful split among them. A common implementation uses the full training set by default rather than bootstrap samples, so its randomness differs from a conventional random forest. Random thresholds reduce search and similarity but may weaken individual trees; the practical outcome depends on the data structure. Here 120 Extra Trees attain 92.4% accuracy, one additional correct test record compared with the forest's 92.0%. Their log losses are about 0.369 and 0.241 respectively, again showing that a small accuracy difference does not settle every predictive use.

Voting can combine different model families. Hard voting combines class decisions, while soft voting averages probabilities; incompatible calibration can make unweighted averaging less useful. Stacking learns a second-level combination from first-level outputs. Its crucial training inputs are predictions made when the corresponding observation was absent from the base learner's training set. The code uses three-fold out-of-fold predictions to train a logistic-regression combiner, then fits base learners on all training data for final testing. Feeding their in-sample predictions directly to the combiner would give it unrealistically optimistic inputs.

The base set contains logistic regression, fifteen-neighbor classification and an eighty-tree random forest. Soft voting achieves 89.6% test accuracy and stacking 92.0%, with stacking log loss approximately 0.234. The model families are shared, but the combination rules differ. Adding more predictors and learning how to combine them are therefore separate choices. The configurations are evaluated together on one held-out set. If these observations guide further changes, treat the comparison as development evidence and arrange another final assessment for the revised procedure.

### Complete experiment: trees, forests, voting and stacking

Requires NumPy, Matplotlib and scikit-learn. Run python main.py --output results --language en for four figure groups, summary.json and experiment_data.npz containing inputs and splits.

```
"""Inspect CART, bootstrap diversity and honest stacking on seeded data."""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification,make_moons
from sklearn.tree import DecisionTreeClassifier,plot_tree
from sklearn.ensemble import BaggingClassifier,RandomForestClassifier,ExtraTreesClassifier,VotingClassifier,StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split,GridSearchCV,StratifiedKFold
from sklearn.metrics import accuracy_score,log_loss
from sklearn.inspection import permutation_importance

def main(output,language):
 out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh';rng=np.random.default_rng(30)
 plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False})
 def t(z,e):return z if zh else e
 def save(f,n):f.savefig(out/f'{n}-{language}.svg',bbox_inches='tight');plt.close(f)
 Xm,ym=make_moons(n_samples=200,noise=.22,random_state=30);small=DecisionTreeClassifier(max_depth=2,random_state=30).fit(Xm,ym)
 fig,ax=plt.subplots(figsize=(12,5.6),layout='constrained');annotations=plot_tree(small,feature_names=['x₀','x₁'],class_names=['0','1'],filled=True,rounded=True,fontsize=11,ax=ax)
 if zh:
  for annotation in annotations:annotation.set_text(annotation.get_text().replace('gini','基尼').replace('samples','样本数').replace('value','类别计数').replace('True','是').replace('False','否').replace('class','预测类'))
 save(fig,'tree')
 gx,gy=np.meshgrid(np.linspace(-1.7,2.7,160),np.linspace(-1.2,1.7,140));grid=np.c_[gx.ravel(),gy.ravel()];fig,axs=plt.subplots(1,2,figsize=(11,4.2),layout='constrained');axs[0].contourf(gx,gy,small.predict_proba(grid)[:,1].reshape(gx.shape),levels=np.linspace(0,1,11),cmap='RdBu_r',alpha=.6);axs[0].scatter(*Xm.T,c=ym,cmap='RdBu_r',s=15,edgecolor='white',lw=.3);axs[0].set(xlabel='x₀',ylabel='x₁',title=t('深度2分类树的矩形区域','Rectangular regions of a depth 2 tree'))
 xr=np.arange(1,7);yr=np.array([1.,1.,2.,6.,7.,7.]);cuts=np.arange(1.5,6,1);loss=[]
 for cut in cuts:
  left=yr[xr<=cut];right=yr[xr>cut];loss.append(float(np.sum((left-left.mean())**2)+np.sum((right-right.mean())**2)))
 axs[1].plot(cuts,loss,'o-',color='#167d87');axs[1].set(xlabel=t('回归树候选阈值','Regression-tree candidate threshold'),ylabel=t('两侧平方残差和','Within-child squared-error sum'),xticks=cuts);axs[1].axvline(3.5,color='#d48745',ls='--');fig.colorbar(axs[0].collections[0],ax=axs[0],shrink=.8,label=t('正类概率','Positive probability'));save(fig,'splits')
 X,y=make_classification(n_samples=1000,n_features=8,n_informative=4,n_redundant=2,n_clusters_per_class=2,class_sep=1.,flip_y=.04,shuffle=False,random_state=30);X=np.c_[X,X[:,0]+rng.normal(0,.03,len(X))];tr,te=train_test_split(np.arange(1000),test_size=.25,stratify=y,random_state=30)
 cv=StratifiedKFold(3,shuffle=True,random_state=30);full=DecisionTreeClassifier(random_state=30).fit(X[tr],y[tr]);alphas=full.cost_complexity_pruning_path(X[tr],y[tr]).ccp_alphas;subset=np.unique(np.quantile(alphas,np.linspace(0,.9,12)))
 search=GridSearchCV(DecisionTreeClassifier(random_state=30),{'ccp_alpha':subset},cv=cv,scoring='accuracy');search.fit(X[tr],y[tr]);pruned=search.best_estimator_
 base=[('lr',make_pipeline(StandardScaler(),LogisticRegression(max_iter=1500))),('knn',make_pipeline(StandardScaler(),KNeighborsClassifier(n_neighbors=15))),('rf',RandomForestClassifier(n_estimators=80,max_features=3,random_state=30,n_jobs=1))]
 models={'Tree':full,'Pruned tree':pruned,'Bagging':BaggingClassifier(estimator=DecisionTreeClassifier(),n_estimators=120,oob_score=True,random_state=30,n_jobs=1),'Random forest':RandomForestClassifier(n_estimators=120,max_features=3,oob_score=True,random_state=30,n_jobs=1),'Extra Trees':ExtraTreesClassifier(n_estimators=120,max_features=3,random_state=30,n_jobs=1),'Soft vote':VotingClassifier(estimators=base,voting='soft',n_jobs=1),'Stacking':StackingClassifier(estimators=base,final_estimator=LogisticRegression(),cv=cv,n_jobs=1)}
 results={}
 for name,m in models.items():
  m.fit(X[tr],y[tr]);p=m.predict_proba(X[te]);results[name]={'test_accuracy':float(accuracy_score(y[te],p.argmax(1))),'test_log_loss':float(log_loss(y[te],p)),'oob_accuracy':float(m.oob_score_) if hasattr(m,'oob_score_') else None}
 diversity=[]
 for mf in [1,3,9]:
  rf=RandomForestClassifier(n_estimators=120,max_features=mf,oob_score=True,random_state=30,n_jobs=1).fit(X[tr],y[tr]);errs=np.array([e.predict(X[te])!=y[te] for e in rf.estimators_],dtype=float);cc=np.corrcoef(errs);pair=float(cc[np.triu_indices_from(cc,1)].mean());diversity.append({'max_features':mf,'mean_tree_accuracy':float(1-errs.mean()),'error_correlation':pair,'forest_accuracy':float(rf.score(X[te],y[te])),'oob_accuracy':float(rf.oob_score_)})
 fig,axs=plt.subplots(1,2,figsize=(11,4.2),layout='constrained');positions=np.arange(len(results));axs[0].barh(positions,[r['test_accuracy'] for r in results.values()],color=['#a1b7c3','#a1b7c3','#167d87','#167d87','#167d87','#d48745','#d48745']);axs[0].set_yticks(positions,list(results));axs[0].set(xlim=(0,1.03),xlabel=t('独立测试准确率','Held-out accuracy'));axs[0].invert_yaxis()
 for key,label,col in [('mean_tree_accuracy',t('单树平均准确率','Mean individual accuracy'),'#d48745'),('forest_accuracy',t('森林准确率','Forest accuracy'),'#167d87'),('error_correlation',t('树错误相关系数','Tree-error correlation'),'#795e86')]:axs[1].plot([d['max_features'] for d in diversity],[d[key] for d in diversity],'o-',label=label,color=col)
 axs[1].set(xlabel=t('每个节点候选特征数','Candidate features per node'),ylabel=t('无量纲','Dimensionless'),xticks=[1,3,9],ylim=(0,1));axs[1].legend();save(fig,'ensemble')
 rf=models['Random forest'];perm=permutation_importance(rf,X[te],y[te],n_repeats=10,random_state=30,scoring='accuracy',n_jobs=1);joint=[]
 for _ in range(10):xp=X[te].copy();order=rng.permutation(len(te));xp[:,[0,8]]=xp[order][:,[0,8]];joint.append(rf.score(X[te],y[te])-rf.score(xp,y[te]))
 oob=np.zeros(len(tr),int)
 for sample in models['Bagging'].estimators_samples_:oob+=~np.isin(np.arange(len(tr)),sample)
 fig,axs=plt.subplots(1,2,figsize=(11,4.2),layout='constrained');j=np.arange(9);axs[0].bar(j-.2,rf.feature_importances_,.4,label=t('不纯度贡献','Impurity contribution'),color='#167d87');axs[0].bar(j+.2,perm.importances_mean,.4,yerr=perm.importances_std,label=t('测试置换准确率下降','Test permutation accuracy drop'),color='#d48745');axs[0].set(xlabel=t('特征编号（x₈近似复制x₀）','Feature index (x₈ nearly copies x₀)'),ylabel=t('各自定义的无量纲量','Dimensionless, different definitions'),xticks=j);axs[0].legend(fontsize=9)
 axs[1].hist(oob,bins=np.arange(oob.min()-.5,oob.max()+1.5,2),color='#167d87');expected=120*(1-1/len(tr))**len(tr);axs[1].axvline(expected,color='#d48745',ls='--',label=t('理论期望','Expected count'));axs[1].set(xlabel=t('一条训练记录的袋外树数','OOB trees for a training observation'),ylabel=t('训练记录数','Training observations'));axs[1].legend();save(fig,'importance')
 summary={'train_n':len(tr),'test_n':len(te),'features':X.shape[1],'models':results,'pruning_alpha':float(search.best_params_['ccp_alpha']),'full_leaves':int(full.get_n_leaves()),'pruned_leaves':int(pruned.get_n_leaves()),'diversity':diversity,'mean_oob_trees':float(oob.mean()),'expected_oob_trees':expected,'joint_x0_x8_permutation_drop':float(np.mean(joint)),'individual_x0_drop':float(perm.importances_mean[0]),'individual_x8_drop':float(perm.importances_mean[8]),'regression_split_losses':loss,'best_regression_split':float(cuts[np.argmin(loss)]),'best_regression_sse':min(loss)}
 (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');np.savez(out/'experiment_data.npz',X=X,y=y,train=tr,test=te,moon_X=Xm,moon_y=ym,oob_counts=oob,permutation_drops=perm.importances,regression_x=xr,regression_y=yr)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--language',choices=['zh','en'],default='en');a=ap.parse_args();main(a.output,a.language)
```

Three questions organize the next experiments. If rules are too fragmented, examine pruning and leaf support. If trees make overly similar errors, change feature or observation sampling. If explanations depend on correlated variables, compare individual and grouped perturbations. Each change corresponds to inspectable structure and a numerical outcome. Trees and forests thus provide not only competitive predictions but also intermediate objects that help connect complex tabular relationships to concrete follow-up decisions.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M30.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [scikit-learn — Decision Trees](https://scikit-learn.org/stable/modules/tree.html)

   CART criteria, node constraints and pruning.

   BSD-3-Clause
2. [scikit-learn — Ensemble Methods](https://scikit-learn.org/stable/modules/ensemble.html)

   Bagging, forests, Extra Trees and out-of-fold stacking.

   BSD-3-Clause
3. [Breiman (2001), Random Forests](https://www.stat.berkeley.edu/~breiman/randomforest2001.pdf)

   Research context for strength, correlation and out-of-bag estimates.
