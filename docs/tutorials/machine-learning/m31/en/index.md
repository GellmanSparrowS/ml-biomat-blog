# Boosted trees: how successive corrections build a strong model

Source: https://ml-biomat.com/tutorials/machine-learning/m31/en/
Language: en

From the changing weights of eight observations to actual XGBoost, LightGBM and CatBoost training, ranking and explanation.

## The next tree repairs what the current model leaves behind

Editing an article often proceeds in stages: organize the argument, add missing explanations, then repair passages that remain unclear. Each pass builds on the existing result instead of averaging several independently written articles. Boosting adopts a related sequential idea. Begin with a simple prediction and train another small model to address what the current predictor has not resolved. The final result adds their contributions. Compared with the preceding forest chapter, the important difference is dependence between successive rounds, making both step size and total number of steps central design choices.

The chapter follows the problems motivating the methods. AdaBoost changes observation weights so that difficult cases receive more attention. Gradient boosting defines the required correction through a loss gradient, extending the same representation to regression, classification and ranking. XGBoost, LightGBM and CatBoost further address regularization, computational resources and categorical information. Understanding these connections turns software names into combinations of statistical objectives and engineering choices rather than interchangeable black boxes.

Five implementations run on 1,800 explicitly generated classification records: 1,080 for training, 360 for validation and 360 for testing. Inputs comprise ten numerical features and a four-level category derived from intervals of the first numerical feature. The category provides another representation rather than independent information. A separate regression experiment exposes residual corrections, and a query-grouped ranking experiment changes the objective. Timing and memory figures come from actual isolated worker processes. The complete script reproduces the generators, parameters and outputs.

## How do difficult observations gain attention?

AdaBoost starts with uniform observation weights, fits a relatively simple classifier and measures its weighted error. A more accurate classifier receives greater influence in the final combination. Misclassified observations gain relative weight so that the next learner pays more attention to them. Freund and Schapire's 1990s work linked multiplicative weight updates with boosting, developed systematically in their 1997 paper. The procedure adapts to observed learner performance instead of requiring advance knowledge of how accurate every weak learner will be.

$$
\epsilon_m=\sum_{i=1}^nD_m(i)\mathbf1[h_m(x_i)\ne y_i],\quad \alpha_m=\frac{\eta}{2}\ln\frac{1-\epsilon_m}{\epsilon_m},\quad D_{m+1}(i)=\frac{D_m(i)e^{-\alpha_m y_i h_m(x_i)}}{Z_m}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/37e7ea7e1e209c402bf2fd4c.svg) | Observation count, observation index and boosting round. |
| ![Formula](https://ml-biomat.com/static/agent-math/93bb4b0cd18cb095f786f05f.svg) | Input vector, true label and current weak prediction; labels and outputs here are −1 or +1. |
| ![Formula](https://ml-biomat.com/static/agent-math/646aa1b9dab853028ed79067.svg) | Normalized observation weight and weighted error, unitless; weights sum to one and error lies strictly between zero and one. |
| ![Formula](https://ml-biomat.com/static/agent-math/c403c2cd2df430316dafa77f.svg) | Positive learning rate and round voting coefficient, unitless, in the symmetric binary convention. |
| ![Formula](https://ml-biomat.com/static/agent-math/a5e38d0246c5845c201ae32e.svg) | Normalization denominator, indicator and natural logarithm; Z sums all unnormalized updated weights. |

With two mistakes among eight equally weighted observations, error is 1/4. At learning rate one, alpha=ln(3)/2≈0.5493. Correct weights multiply by 1/√3 and mistaken weights by √3; normalization gives six weights of 1/12 and two of 1/4, still summing to one.

Suppose eight observations initially have weight 1/8 and a weak classifier misses two. Its weighted error is 1/4. Under the symmetric binary coefficient convention, its voting coefficient is approximately 0.5493. After normalization, each mistaken observation receives weight 1/4 and each of the six correct observations receives 1/12. The two groups now carry equal total weight. No new raw data have appeared; the learner is viewing the same records under a changed distribution. The update resembles reallocating practice time toward material that remains difficult.

This attention can also chase corrupted labels or extreme noise. Repeatedly increasing the weight of a mislabeled observation may make later learners pay a growing price for an impossible correction. Inspect high-weight observations to distinguish rare important cases from labeling or measurement problems. A learning rate reduces each contribution, while weak-tree depth changes the structure available in one round. The code uses scikit-learn's SAMME implementation with decision stumps. The hand calculation uses a symmetric binary expression with a different coefficient scale but a corresponding relative weight-update mechanism.

## How one boosting round reallocates attention

Eight records initially have weight 1/8. Change the stump threshold, direction and learning rate to inspect mistake weights and total weight. Orange marks errors; blue marks correct predictions.

[Figure: True labels, stump predictions and normalized weights](https://ml-biomat.com/tutorials/machine-learning/m31/en/#M31-plot)

The interactive experiment fixes eight labels and lets you choose stump threshold, direction and update strength. It shows mistakes above and before-and-after weights below. Error one half gives a zero coefficient: the rule offers no useful directional advantage. Error above one half gives a negative coefficient, equivalent to using the rule in reverse; a training implementation can explicitly flip or reject it. Watching total weight remain one checks the normalization and gives a concrete meaning to the exponential update.

## From mistakes to a direction that reduces loss

Regression does not divide observations simply into correct and incorrect cases, so a more general correction is needed. Under squared loss, observed minus predicted response points toward the missing amount: a prediction short by two needs a positive correction; an excess of one needs a negative correction. Fit a regression tree to these residuals and add a fraction of its prediction to the current model. The initial predictor is commonly the loss-minimizing constant, which is the training mean under squared loss. This gives the most direct introduction to gradient boosting.

$$
r_{im}=-\left.\frac{\partial\ell(y_i,F)}{\partial F}\right|_{F=F_{m-1}(x_i)},\qquad F_m(x)=F_{m-1}(x)+\eta h_m(x)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/93519422cf83110abebee704.svg) | Observation index, round, arbitrary input, observed input and response. |
| ![Formula](https://ml-biomat.com/static/agent-math/4a689e31890fc97c95f6af0b.svg) | Previous and updated raw prediction functions and a tree fitted to negative gradients; classification F is a score, not a probability. |
| ![Formula](https://ml-biomat.com/static/agent-math/8338dc4c5daca5f09e7fb996.svg) | Per-observation loss, negative-gradient pseudo-residual and positive learning rate; the numerical example is dimensionless. |

For squared loss (y−F)²/2, differentiating with respect to F gives F−y, so the negative gradient is y−F. Targets (2,5) and predictions (3,3) give residuals (−1,2). If the tree fits them exactly, learning rate 0.1 produces (2.9,3.2). Logistic negative gradients are y−p, while updates still act on raw scores.

![Squared-loss boosting on the same 100 generated observations: initial mean, first residual tree, shrunken contribution and predictions after one, ten and sixty rounds.](https://ml-biomat.com/static/tutorials/machine-learning/figures/5d850b076095d5afe3424ef2.svg?v=5d850b076095)

Figure 1Squared-loss boosting on the same 100 generated observations: initial mean, first residual tree, shrunken contribution and predictions after one, ten and sixty rounds.

The generating regression combines a sine relationship with a linear term and Gaussian noise of standard deviation 0.18. The upper panels display the initial mean, residuals with the first fitted tree, and the 15% contribution actually added. The lower panels compare one, ten and sixty depth-two trees. Individually piecewise-constant corrections accumulate into a useful approximation of a smooth relationship. The initial residuals sum to approximately zero because the starting constant is their sample mean, providing an independently checkable numerical identity in the script.

Other differentiable losses require fitting a negative gradient, which need not equal the raw response residual. For binary log loss as a function of a raw score, the negative gradient is label minus current probability. The new tree nevertheless updates the raw score, after which a sigmoid produces probability. Adding that correction directly to probability changes the optimization problem. Friedman's 2001 gradient-boosting work framed boosting as incremental optimization in function space, connecting the loss, base learner and step search through one general construction.

A smaller learning rate makes a more cautious correction and usually requires more rounds. Depth controls the interactions expressible in one tree, while row and feature sampling add randomness. These choices interact, so tree count is not an independent accuracy dial. Early stopping selects a useful iteration using validation loss, potentially ending improvement attempts even while training loss continues to fall. Because validation has selected the stopping position, the final test remains outside both fitting and that selection.

![Training and validation log loss for five fixed configurations. AdaBoost retains 400 rounds; its validation curve is descriptive. GBDT, XGBoost, LightGBM and CatBoost select round counts using validation loss. Test records supply the final evaluation.](https://ml-biomat.com/static/tutorials/machine-learning/figures/ab7a48473e87ea741f35f762.svg?v=ab7a48473e87)

Figure 2Training and validation log loss for five fixed configurations. AdaBoost retains 400 rounds; its validation curve is descriptive. GBDT, XGBoost, LightGBM and CatBoost select round counts using validation loss. Test records supply the final evaluation.

The AdaBoost curve contains a useful detail: after roughly 40 rounds, both training and validation log loss rise. The plotted quantity is log loss of the probabilities returned by the library. AdaBoost’s weighted classification updates and exponential-loss interpretation concern a different quantity. The scikit-learn implementation used here divides the trees’ weighted votes by their total weight before converting the normalized score into probabilities. Adding a tree changes both the votes and this denominator. Classification decisions and probability confidence can therefore change differently. Keeping the actual 400-round result lets us compare accuracy with probability loss and examine the distinction between choosing a class and assigning a well-calibrated probability.

## XGBoost makes a correction cheap to compare

XGBoost computes first and second derivatives of the current loss for each observation. The gradient indicates a correction direction; curvature describes how that local slope changes. Penalties on leaf count and leaf scores are added to the approximate objective. Summing gradients and curvatures within a leaf gives a simple expression for its optimal score. A proposed split can therefore be evaluated from left and right aggregate statistics rather than repeatedly solving a separate full optimization over every candidate leaf value.

$$
G_j=\sum_{i\in I_j}g_i,\quad H_j=\sum_{i\in I_j}h_i,\quad \widetilde L=\sum_{j=1}^J\left[G_jw_j+\frac12(H_j+\lambda)w_j^2\right]+\gamma J,\quad w_j^*=-\frac{G_j}{H_j+\lambda}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7e0420234890d636d2d9da42.svg) | Leaf index, leaf count, observations assigned to a leaf and observation index. |
| ![Formula](https://ml-biomat.com/static/agent-math/c1606c14eceb60340c079e42.svg) | First and second loss derivatives with respect to the current raw score and their leaf sums; h_i here is curvature, unlike the tree h_m above. |
| ![Formula](https://ml-biomat.com/static/agent-math/e33da962e40c68b8cfe7df9d.svg) | Leaf score update, nonnegative L2 penalty, nonnegative leaf-count penalty and quadratic approximate objective; dimensionless classification loss with H_j+lambda>0. |

Expand the round loss to second order around previous predictions and omit constants independent of the new tree. For a fixed structure, setting each leaf derivative to zero gives its optimal score. G=−3, H=2 and lambda=1 give w=1 and quadratic contribution −1.5. With gamma=0.2, the one-leaf objective increment is −1.3.

This is a local approximation around current predictions, not a claim that every model globally has one quadratic objective. For squared loss the second-order structure is already exact; other losses rely on controlling how the local approximation is used. Leaf-score penalties suppress excessive corrections, minimum child weight constrains splits with too little accumulated curvature, and a gain threshold requires a new branch to improve the objective enough. Each parameter acts at a specific part of tree construction. Identifying that part is more useful than treating all settings as anonymous knobs in a search.

Sparse features and missingness also affect construction. A split can learn a default direction for missing observations according to the training objective. The interpretation of an absent sparse entry depends on the input representation and missing-value settings; numerical zero and missingness are not interchangeable. Here categories are one-hot encoded on training data and numerical inputs remain dense to make encoding choices explicit. Current XGBoost supports other categorical paths too. Recording the chosen path is more accurate than presenting one-hot encoding as its only capability.

The experiment uses histogram tree construction, aggregating continuous values into bins. Histograms are therefore not an exclusive modern feature of LightGBM. Compare actual settings rather than historical brand descriptions. XGBoost runs with a 400-round cap, depth three and learning rate 0.05, selecting 159 rounds through validation. Test accuracy is 91.11% and log loss about 0.241. These characterize the specified configuration. A subsequent comparison can allocate equal development budgets to depth, regularization and sampling searches rather than deriving a universal software ranking from one fit.

A learned default direction for missing values has a practical interpretation. A missing recent-purchase amount may mean no purchase history or a field that was never collected. Replacing both with zero merges those situations with an actual zero-valued purchase. A tree supporting missing branches compares the loss obtained by sending missing observations left or right and stores the preferred direction for prediction. That direction reflects training-time missingness. If a collection change suddenly makes many records incomplete, evaluate the affected missingness patterns separately: the prediction routine still runs, but the event represented by its input has changed.

## LightGBM combines histograms with selective leaf growth

A continuous feature may contain thousands of unique values, making a scan of all potential thresholds expensive. Histogram construction assigns values to fewer bins and accumulates gradients, curvatures and counts. Cumulative sums then compare cuts between bins. After splitting a parent, subtracting one child's histogram from the parent's yields the other child's histogram. Fewer bins commonly save work and storage while reducing threshold resolution. The resulting accuracy-resource trade-off can be measured rather than inferred from a generic claim that discretization is faster.

![Level-wise growth expands nodes at the same depth, producing a relatively balanced structure. Original Microsoft / LightGBM figure, MIT license, unmodified.](https://ml-biomat.com/static/tutorials/machine-learning/figures/dcf2230660f312997cedae6d.png?v=dcf2230660f3)

Figure 3Level-wise growth expands nodes at the same depth, producing a relatively balanced structure. Original Microsoft / LightGBM figure, MIT license, unmodified.

![Leaf-wise growth expands the leaf with the greatest current gain without requiring equal branch depth; depth and leaf-count constraints serve different purposes. Original Microsoft / LightGBM figure, MIT license, unmodified.](https://ml-biomat.com/static/tutorials/machine-learning/figures/4bf21a9a4d94fadbc76331d0.png?v=4bf21a9a4d94)

Figure 4Leaf-wise growth expands the leaf with the greatest current gain without requiring equal branch depth; depth and leaf-count constraints serve different purposes. Original Microsoft / LightGBM figure, MIT license, unmodified.

The original documentation diagrams compare growth orders. Level-wise growth expands nodes at a given depth. Leaf-wise growth repeatedly chooses the leaf expected to provide the greatest loss decrease, potentially following one branch much deeper than another. At a fixed leaf count, this can concentrate computation where further partitioning is useful, while creating deep local rules on small datasets. LightGBM provides leaf-count, depth and minimum-leaf-data controls. Here leaves are capped at eight and depth at three to make structural scale explicit, rather than depicting one growth order as universally preferable.

The LightGBM research also includes gradient-based sampling and exclusive feature bundling. GOSS retains high-gradient observations and samples lower-gradient observations with adjusted weights, directing work toward records requiring larger corrections. EFB combines sparse features that rarely take nonzero values simultaneously, reducing the effective feature count. They address row and column costs respectively and differ from ordinary uniform subsampling. Version, boosting configuration and data determine the actual path. This experiment uses an ordinary GBDT configuration and does not attribute its measured runtime to GOSS being enabled.

Categorical splits can organize categories using training-objective statistics and search partitions of category sets instead of assigning an artificial numerical order. The example declares a pandas categorical column and fixes its vocabulary from training data for validation and testing. Validation selects 135 rounds, giving 91.11% test accuracy and log loss about 0.248. With small data, overhead and system scheduling can substantially affect short timings. The figure therefore defines the measurement, and increasing dataset size with repeated runs offers a more informative investigation of when implementation differences dominate.

A leaf budget clarifies the growth preference. Suppose one available split reduces loss by ten units and another by one unit. With room for one additional leaf, a gain-driven procedure chooses the first split. It compares all eligible leaves again in the next round, so one branch can deepen repeatedly. Level-wise growth instead allocates expansion opportunities across a depth. Deep leaves supported by few observations can encode very specific rules. Minimum leaf counts and minimum summed curvature constrain this local evidence, whereas learning-rate shrinkage reduces a whole tree contribution. These controls address different aspects of model flexibility.

## Category statistics without reading an observation's own answer

Replacing a category name with its mean target seems like an efficient numerical encoding but can leak labels. If a category occurs once, its target mean is the observation's own answer. Repeated categories still allow each label to influence its own input representation, making training encodings more informed than future encodings. CatBoost's ordered target statistics use only preceding observations of the same category under an ordering, together with prior smoothing. The current label therefore does not directly enter the statistic used to represent that observation.

$$
c_i=\frac{\sum_{j\in P_i}y_j+a p_0}{|P_i|+a}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8491503cb3d88ee63e629414.svg) | Current and earlier record indices, preceding records sharing the same category in a permutation, and their count; the current record is excluded. |
| ![Formula](https://ml-biomat.com/static/agent-math/2568d99f80750234e016f162.svg) | Binary target, prior positive rate, positive prior pseudocount and smoothed category encoding; targets and rates are unitless. |

For successive targets 1,0,1 in one category with prior 0.5 and a=1, the first encoding is 0.5, the second (1+0.5)/2=0.75, and the third (1+0+0.5)/3=0.5. A target never enters its own encoding. This simplifies ordered target statistics; CatBoost uses multiple statistics and permutations.

For three occurrences of one category with labels 1,0,1, prior mean 0.5 and prior strength one, the teaching statistic is 0.5,0.75 and 0.5 in sequence. The first observation has no earlier same-category data and uses the prior. The second can use the first label, and the third can use the first two. The full-category mean 2/3 incorporates every observation's own answer and is a different construction. Actual CatBoost offers several statistic types and combinations; this example isolates exclusion of the current label and smoothing toward a prior.

Ordered boosting and ordered category statistics are related but act on different objects. The former uses corresponding prefix models to form correction signals and reduce prediction shift associated with dependence on a sample's own target. The latter transforms categorical inputs. The script explicitly selects Ordered boosting, passes the category column directly and sets one_hot_max_size to two so the four-level category takes a statistical encoding path. Common symmetric trees share a split across nodes at one depth, supporting regular structure and efficient prediction; other growth policies are also available, making the actual parameters part of the model description.

Validation selects 219 depth-three trees, producing 92.5% accuracy and log loss about 0.230. The Ordered configuration takes noticeably longer than the other configurations in this CPU experiment, an actual trade-off retained in the resource figure. More observations, higher-cardinality categories or another growth policy can change the relationship. Ordered processing also does not replace chronological evaluation. “Earlier” in a random permutation is not the historical past. Forecasting future records still requires actual time constraints on training, categorical statistics and validation information.

## The complete workflow is the comparison unit

All five implementations share training, validation and test indices and a cap of 400 rounds. AdaBoost uses depth-one stumps and learning rate 0.1, retaining all 400 rounds as a fixed baseline. Its validation curve describes training behavior and does not select the number of rounds. The other classifiers use depth three and learning rate 0.05. LightGBM permits eight leaves, and CatBoost uses Ordered boosting. Conventional GBDT fits all 400 rounds and selects iteration 174 on its validation curve, while XGBoost, LightGBM and CatBoost use validation loss and patience 25 to select their round counts. This aligns data and some resource limits while retaining explicit method configurations. A best-performance comparison should additionally equalize tuning trials or wall-clock budgets rather than treating equal round caps as equal search effort.

![Accuracy and log loss on the same 360 test records, with actual separate-process fitting-and-curve time and peak resident memory. Resource measurements include the specified software runtime; each language was run separately.](https://ml-biomat.com/static/tutorials/machine-learning/figures/c0bddc2f9e4bf08c2b253413.svg?v=c0bddc2f9e4b)

Figure 5Accuracy and log loss on the same 360 test records, with actual separate-process fitting-and-curve time and peak resident memory. Resource measurements include the specified software runtime; each language was run separately.

Test accuracies are approximately 84.72%, 91.39%, 91.11%, 91.11% and 92.5% for AdaBoost, GBDT, XGBoost, LightGBM and CatBoost respectively. The stronger baselines differ by only a few observations, making log loss and resource cost useful companions. Encoding paths preserve the same raw information. Both the one-hot vocabulary and the LightGBM category vocabulary come from training records. CatBoost receives raw category strings and learns categorical statistics from training records. All four categories, A, B, C and D, occur in this training set. When categories follow real chronology or a user contributes several records, the split protocol must change from the independent generated-row setting used here.

The timer includes fitting, validation-curve computation and test prediction, but excludes Python imports. Memory is peak resident memory of each isolated worker process, including imported libraries and runtime allocations. Starting a fresh process per implementation prevents previously retained fitted models from altering later baselines. The language versions are executed separately, so short resource measurements can differ; they are not repeated-run benchmark rankings. Deployment-oriented work can add median fitting time over repetitions, fixed-batch prediction throughput and serialized model size, with explicit thread and hardware conditions.

Early stopping is hyperparameter selection. Test labels should not enter the evaluation set used to stop training, category statistics should not include test targets, and imputation or vocabulary learning belongs on the training side. After selecting a round count, a predefined procedure may refit on combined training and validation observations, then use the reserved test set. Alternatively, retaining the current training fit makes it directly comparable to the displayed validation curve. Recording the final training range explains why a refitted model can differ from the development-stage numerical result.

Validation curves contain sampling variation, especially when a validation set contains few positive cases. Round 135 can outperform round 134 because probabilities moved slightly for a handful of observations. Define the primary metric and patience beforehand, then inspect whether a broader part of the curve is stable. Repeatedly changing those rules in response to test scores turns the test set into another development set. Saved learning curves also reveal whether an expensive fit stopped prematurely or spent many rounds making tiny gains. Once a candidate procedure is selected, evaluate it on independent observations or on a split reflecting the intended deployment.

## The trees still add, but the correction target changes

Regression, classification and ranking share the additive-tree representation while using different losses to determine corrections. Squared regression addresses numerical discrepancy; classification log loss addresses probability-label disagreement; ranking concerns relative order within a query. Treating candidates from different queries as ordinary classification rows loses the competing set. Query members should also remain together during splitting. The separate experiment creates eighty queries with eight candidates each, trains on sixty queries, tests on twenty new queries and actually fits XGBRanker.

Relevance grades range from zero to three, assigned from an explicit latent utility with noise. NDCG converts grades into gains, discounts gains at later positions and divides by the score of the best possible ordering for the same query. Placing highly relevant candidates near the top lets a reader encounter useful results earlier and raises the score. Burying those candidates lowers the score even when the list contains the same items. This experiment evaluates the first five positions separately for each query, then averages the 20 test-query scores to obtain approximately 0.961. Adding a constant to every score within one query leaves its ordering unchanged, so a raw ranking score should not be read as a comparable relevance probability across queries. Ranking-tree updates address relative order within a query. Placing a highly relevant candidate below a less relevant one creates a comparison to correct, and NDCG-related weights reflect how a swap affects ranking quality. Trees fit these update signals from the features and progressively change candidate scores. The reported @5 specifies the evaluation cutoff; training uses the rank:ndcg objective shown in the code. Exposure, sampled comparisons and feedback sources determine which preferences enter the updates.

$$
\operatorname{DCG@K}=\sum_{r=1}^{K}\frac{2^{g_r}-1}{\log_2(r+1)},\qquad \operatorname{NDCG@K}=\frac{\operatorname{DCG@K}}{\operatorname{IDCG@K}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7f10a207433df574f151b37b.svg) | Number of retained positions and one-based rank index, both dimensionless counts; K does not exceed the query candidate count. |
| ![Formula](https://ml-biomat.com/static/agent-math/3f8ef56587f0ba25bd66e77f.svg) | Relevance grade at rank r and its exponential gain. Grades 0, 1, 2 and 3 correspond to gains 0, 1, 3 and 7; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/80e2f3a4c89172264f530f4a.svg) | Base-2 logarithmic discount: 1 at the first position and about 1.585 at the second. A larger denominator reduces the contribution of a later position. |
| ![Formula](https://ml-biomat.com/static/agent-math/cecbf47d4b809626cad8fea7.svg) | Discounted cumulative gain, its ideal value after ordering the same query candidates by decreasing grade, and their ratio; dimensionless. The evaluation assigns NDCG zero when the ideal gain is zero. |

Consider two candidates with grades 3 and 1. Putting grade 1 first gives DCG@2=1+7/log2(3)≈5.4165. The ideal order gives IDCG@2=7+1/log2(3)≈7.6309, so NDCG@2≈0.7098; the ideal order scores 1. The full experiment converts grades into gains before passing them to ndcg_score, then averages NDCG@5 over 20 test queries to obtain approximately 0.961.

![Largest XGBoost feature contributions for one test observation, in raw log-odds units. In the complete output, all feature contributions plus the baseline sum to the raw score, giving probability about 0.1732.](https://ml-biomat.com/static/tutorials/machine-learning/figures/f38fdc12b68148411d30998f.svg?v=f38fdc12b681)

Figure 6Largest XGBoost feature contributions for one test observation, in raw log-odds units. In the complete output, all feature contributions plus the baseline sum to the raw score, giving probability about 0.1732.

$$
z=\phi_0+\sum_{j=1}^d\phi_j,\qquad p=\frac{1}{1+e^{-z}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a78d8c046bf3647434fdc286.svg) | Encoded feature count, feature index, baseline and feature contributions to the raw score; all in dimensionless log-odds units. |
| ![Formula](https://ml-biomat.com/static/agent-math/464baf38a8828b3364b642c3.svg) | Raw binary score, positive probability and exponential base under the logistic link. |

A baseline −1 and contributions 0.5 and −0.2 give z=−0.7, hence p≈0.3318. Transforming each contribution to a probability and adding does not preserve the relation. The actual example has z≈−1.56295 and p≈0.17322, with additive discrepancy about 2.38×10⁻⁷.

XGBoost can also produce additive feature contributions for an observation. The figure displays major contributions on the raw log-odds scale. All feature contributions plus the baseline sum to approximately −1.563, which the sigmoid converts to probability 0.1732. The code uses the same iteration range as early-stopped prediction and checks the contribution sum against the raw score; the discrepancy is about 2.4×10⁻⁷, consistent with floating-point arithmetic. Only the largest terms are displayed for readability, while the reconstruction includes every smaller term too.

These contributions decompose the fitted model's score relative to its explanation background. A positive contribution is not a positive causal effect in the world. One-hot contributions can be grouped by their original category variable, while dependent inputs and background definitions still affect interpretation. The zero line describes contribution direction, and the complete probability also depends on the baseline and all remaining terms. Making that relationship explicit turns the plot into an inspectable explanation of a prediction rather than a plausible-looking set of colored bars.

### Complete experiment: five boosters, residuals, ranking and contributions

Uses NumPy, pandas, Matplotlib, scikit-learn, XGBoost, LightGBM and CatBoost. Run python main.py --output results --language en. Five classifiers run in separate processes; outputs include arrays, learning curves, numerical summaries and every original figure in this chapter.

```
"""Five real boosting implementations; isolated worker resource measurements."""
from pathlib import Path
import argparse,json,sys,subprocess,time,os,ctypes
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import AdaBoostClassifier,GradientBoostingClassifier,GradientBoostingRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,log_loss,ndcg_score
from xgboost import XGBClassifier,XGBRanker,DMatrix
from lightgbm import LGBMClassifier,early_stopping,log_evaluation
from catboost import CatBoostClassifier

def peak_rss_mb():
    if os.name=='nt':
        class Counters(ctypes.Structure):
            _fields_=[('cb',ctypes.c_ulong),('PageFaultCount',ctypes.c_ulong)]+[(n,ctypes.c_size_t) for n in ['PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage']]
        c=Counters();c.cb=ctypes.sizeof(c);handle=ctypes.windll.kernel32.GetCurrentProcess;handle.restype=ctypes.c_void_p
        fun=ctypes.windll.psapi.GetProcessMemoryInfo;fun.argtypes=[ctypes.c_void_p,ctypes.POINTER(Counters),ctypes.c_ulong];fun.restype=ctypes.c_int
        if not fun(handle(),ctypes.byref(c),c.cb):raise OSError('Process memory counter failed')
        return c.PeakWorkingSetSize/1024**2
    import resource
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024**2 if sys.platform=='darwin' else 1024)

def worker(name,datafile,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);a=np.load(datafile);X=a['X'];cat=a['category'];y=a['y'];tr=a['train'];va=a['validation'];te=a['test']
    enc=OneHotEncoder(handle_unknown='ignore',sparse_output=False).fit(cat[tr,None]);Z=np.c_[X,enc.transform(cat[:,None])]
    frame=pd.DataFrame(X,columns=[f'x{j}' for j in range(X.shape[1])]);frame['category']=cat
    lframe=frame.copy();dtype=pd.CategoricalDtype(categories=sorted(np.unique(cat[tr])));lframe['category']=lframe['category'].astype(dtype)
    curves={};start=time.perf_counter()
    if name=='AdaBoost':
        model=AdaBoostClassifier(estimator=DecisionTreeClassifier(max_depth=1),n_estimators=400,learning_rate=.1,random_state=31);model.fit(Z[tr],y[tr]);prob=model.predict_proba(Z[te]);rounds=len(model.estimators_)
        curves={'train':[log_loss(y[tr],p) for p in model.staged_predict_proba(Z[tr])],'validation':[log_loss(y[va],p) for p in model.staged_predict_proba(Z[va])]}
    elif name=='GBDT':
        model=GradientBoostingClassifier(n_estimators=400,learning_rate=.05,max_depth=3,random_state=31);model.fit(Z[tr],y[tr]);vcur=[log_loss(y[va],p) for p in model.staged_predict_proba(Z[va])];rounds=int(np.argmin(vcur))+1
        curves={'train':[log_loss(y[tr],p) for p in model.staged_predict_proba(Z[tr])],'validation':vcur};prob=next(p for i,p in enumerate(model.staged_predict_proba(Z[te]),1) if i==rounds)
    elif name=='XGBoost':
        model=XGBClassifier(n_estimators=400,max_depth=3,learning_rate=.05,subsample=.85,colsample_bytree=.85,tree_method='hist',n_jobs=2,random_state=31,eval_metric='logloss',early_stopping_rounds=25,reg_lambda=1.)
        model.fit(Z[tr],y[tr],eval_set=[(Z[tr],y[tr]),(Z[va],y[va])],verbose=False);prob=model.predict_proba(Z[te]);rounds=model.best_iteration+1;ev=model.evals_result();curves={'train':ev['validation_0']['logloss'],'validation':ev['validation_1']['logloss']}
    elif name=='LightGBM':
        model=LGBMClassifier(n_estimators=400,max_depth=3,num_leaves=8,learning_rate=.05,n_jobs=2,random_state=31,verbosity=-1)
        xt=lframe.iloc[tr];yt=y[tr];xv=lframe.iloc[va];yv=y[va]
        model.fit(xt,yt,eval_X=(xt,xv),eval_y=(yt,yv),eval_names=['train','validation'],eval_metric='binary_logloss',callbacks=[early_stopping(25,verbose=False),log_evaluation(0)]);prob=model.predict_proba(lframe.iloc[te]);rounds=model.best_iteration_;curves={'train':model.evals_result_['train']['binary_logloss'],'validation':model.evals_result_['validation']['binary_logloss']}
    else:
        model=CatBoostClassifier(iterations=400,depth=3,learning_rate=.05,loss_function='Logloss',random_seed=31,thread_count=2,verbose=False,allow_writing_files=False,boosting_type='Ordered',one_hot_max_size=2)
        model.fit(frame.iloc[tr],y[tr],cat_features=['category'],eval_set=(frame.iloc[va],y[va]),early_stopping_rounds=25,use_best_model=True);prob=model.predict_proba(frame.iloc[te]);rounds=model.tree_count_;ev=model.get_evals_result();curves={'train':ev['learn']['Logloss'],'validation':ev['validation']['Logloss']}
    elapsed=time.perf_counter()-start;peak=peak_rss_mb();result={'name':name,'test_accuracy':float(accuracy_score(y[te],prob.argmax(1))),'test_log_loss':float(log_loss(y[te],prob)),'selected_rounds':int(rounds),'fit_and_curve_seconds':elapsed,'worker_peak_rss_mb':peak,'curves':curves}
    if name=='XGBoost':
        booster=model.get_booster();dm=DMatrix(Z[te[:1]]);contrib=booster.predict(dm,pred_contribs=True,iteration_range=(0,rounds))[0];margin=float(booster.predict(dm,output_margin=True,iteration_range=(0,rounds))[0]);result['contribution_sum_error']=float(abs(contrib.sum()-margin));result['example_margin']=margin;result['example_probability']=float(prob[0,1]);result['contributions']=contrib.tolist();result['feature_names']=[f'x{j}' for j in range(X.shape[1])]+enc.get_feature_names_out(['category']).tolist()+['bias'];model.save_model(out/'model.ubj')
    (out/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf8');np.save(out/'test_probability.npy',prob)

def main(output,language):
    out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh';rng=np.random.default_rng(31)
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False})
    def t(z,e):return z if zh else e
    def save(f,n):f.savefig(out/f'{n}-{language}.svg',bbox_inches='tight');plt.close(f)
    X,y=make_classification(n_samples=1800,n_features=10,n_informative=5,n_redundant=2,class_sep=1.,flip_y=.03,random_state=31)
    category=np.array(['A','B','C','D'])[np.digitize(X[:,0],[-.7,0,.7])];idx=np.arange(1800);tr,tmp=train_test_split(idx,test_size=.4,stratify=y,random_state=31);va,te=train_test_split(tmp,test_size=.5,stratify=y[tmp],random_state=31)
    datafile=out/'classification_data.npz';np.savez(datafile,X=X,category=category,y=y,train=tr,validation=va,test=te)
    results={}
    for name in ['AdaBoost','GBDT','XGBoost','LightGBM','CatBoost']:
        dest=out/'workers'/name;run=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker',name,'--data',str(datafile),'--output',str(dest)],capture_output=True,text=True)
        if run.returncode:raise RuntimeError(f'{name} failed:\n{run.stderr}')
        results[name]=json.loads((dest/'summary.json').read_text())
    # Gradient boosting for a known continuous relationship, exposing component trees.
    xr=np.sort(rng.uniform(-2,2,100));yr=np.sin(2*xr)+.25*xr+rng.normal(0,.18,100);reg=GradientBoostingRegressor(n_estimators=60,learning_rate=.15,max_depth=2,random_state=31).fit(xr[:,None],yr);grid=np.linspace(-2,2,300);staged=list(reg.staged_predict(grid[:,None]));initial=float(yr.mean());first=reg.estimators_[0,0].predict(grid[:,None]);residual=yr-initial
    fig=plt.figure(figsize=(12,6),layout='constrained');gs=fig.add_gridspec(2,3)
    ax=fig.add_subplot(gs[0,0]);ax.scatter(xr,yr,s=12,color='#167d87');ax.axhline(initial,color='#d48745');ax.set(title=t('初始常数预测','Initial constant prediction'),xlabel='x',ylabel='y')
    ax=fig.add_subplot(gs[0,1]);ax.scatter(xr,residual,s=12,color='#167d87');ax.plot(grid,first,color='#d48745');ax.axhline(0,color='#a3b7c1',lw=.7);ax.set(title=t('第一棵树拟合残差','First tree fits residuals'),xlabel='x',ylabel=t('残差','Residual'))
    ax=fig.add_subplot(gs[0,2]);ax.plot(grid,.15*first,color='#d48745');ax.set(title=t('加入15%的树贡献','Add 15% of the tree contribution'),xlabel='x',ylabel=t('新增预测','Added prediction'))
    for ax,n in zip([fig.add_subplot(gs[1,j]) for j in range(3)],[1,10,60]):ax.scatter(xr,yr,s=9,color='#9bb1bd');ax.plot(grid,np.sin(2*grid)+.25*grid,'--',color='#263d4b');ax.plot(grid,staged[n-1],color='#167d87');ax.set(title=f'{n} '+t('棵树','trees'),xlabel='x',ylabel='y')
    save(fig,'residual_steps')
    fig,axs=plt.subplots(1,2,figsize=(11,4.4),layout='constrained');colors=['#9b6b89','#b78a44','#167d87','#5275a3','#7648a0']
    for (name,r),color in zip(results.items(),colors):
        axs[0].plot(np.arange(1,len(r['curves']['validation'])+1),r['curves']['validation'],label=name,color=color);axs[1].plot(np.arange(1,len(r['curves']['train'])+1),r['curves']['train'],label=name,color=color)
    axs[0].set(title=t('验证集概率对数损失','Validation probability log loss'),xlabel=t('树数','Tree count'),ylabel=t('对数损失（nat）','Log loss (nats)'));axs[1].set(title=t('训练集概率对数损失','Training probability log loss'),xlabel=t('树数','Tree count'),ylabel=t('对数损失（nat）','Log loss (nats)'));axs[0].legend();save(fig,'curves')
    fig,axs=plt.subplots(2,2,figsize=(11,7),layout='constrained');names=list(results)
    for ax,key,label in zip(axs.ravel(),['test_accuracy','test_log_loss','fit_and_curve_seconds','worker_peak_rss_mb'],[t('测试准确率','Test accuracy'),t('测试对数损失（nat）','Test log loss (nats)'),t('拟合与曲线计算时间（秒）','Fit and curve-computation time (s)'),t('独立进程峰值RSS（MiB）','Isolated-process peak RSS (MiB)')]):
        values=[results[n][key] for n in names];ax.barh(names,values,color=colors);ax.set(xlabel=label);ax.invert_yaxis();ax.set_xlim(0,max(values)*1.18)
        for i,v in enumerate(values):ax.text(v,i,f' {v:.3f}' if key!='worker_peak_rss_mb' else f' {v:.1f}',va='center',fontsize=10)
    save(fig,'comparison')
    r=results['XGBoost'];con=np.array(r['contributions']);order=np.argsort(np.abs(con[:-1]))[::-1][:7];fig,ax=plt.subplots(figsize=(9,4.6),layout='constrained');ax.barh(np.arange(len(order)),con[order],color=np.where(con[order]>=0,'#d48745','#167d87'));ax.set_yticks(np.arange(len(order)),np.array(r['feature_names'])[order]);ax.axvline(0,color='#7d97a4');ax.set(xlabel=t('原始分数贡献（log-odds）','Raw-score contribution (log odds)'),title=t('同一个测试样本：贡献相加得到原始分数','One test observation: contributions add to the raw score'));ax.invert_yaxis();save(fig,'contributions')
    # Query-disjoint ranking: each query contains eight candidates, relevance0..3.
    qx=rng.normal(size=(80,8,4));utility=2*qx[:,:,0]-qx[:,:,1]+.4*rng.normal(size=(80,8));rel=np.empty((80,8),int)
    for q in range(80):rel[q,np.argsort(utility[q])]=np.repeat(np.arange(4),2)
    ranker=XGBRanker(n_estimators=60,max_depth=3,learning_rate=.1,objective='rank:ndcg',tree_method='hist',n_jobs=2,random_state=31)
    ranker.fit(qx[:60].reshape(-1,4),rel[:60].ravel(),qid=np.repeat(np.arange(60),8));rs=ranker.predict(qx[60:].reshape(-1,4)).reshape(20,8);ranking=float(ndcg_score(2**rel[60:]-1,rs,k=5))
    summary={'train_n':len(tr),'validation_n':len(va),'test_n':len(te),'numeric_features':10,'categories':4,'models':{n:{k:v for k,v in r.items() if k not in ['curves','contributions','feature_names']} for n,r in results.items()},'regression_initial_residual_sum':float(residual.sum()),'xgb_contribution_sum_error':results['XGBoost']['contribution_sum_error'],'ranking_train_queries':60,'ranking_test_queries':20,'ranking_candidates_per_query':8,'ranking_ndcg5':ranking}
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');np.savez(out/'regression_ranking_data.npz',x=xr,y=yr,rank_X=qx,rank_relevance=rel,rank_prediction=rs)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--language',choices=['zh','en'],default='en');ap.add_argument('--worker');ap.add_argument('--data');a=ap.parse_args()
    if a.worker:worker(a.worker,a.data,a.output)
    else:main(a.output,a.language)
```

Continue through a sequence of checkable operations: calculate one weight update, follow one negative-gradient correction, identify the validation-selected iteration, then sum contributions back to an actual prediction. Algorithms, implementations and task objectives occupy different places in this chain. For new data, establish response type, category structure and deployment split before assigning a comparison budget to candidate implementations. The resulting measurements can then guide the next research decision.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M31.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Freund & Schapire (1997), A Decision-Theoretic Generalization of On-Line Learning and an Application to Boosting](https://www.schapire.net/papers/FreundSc95.pdf)

   Research background for multiplicative weights and AdaBoost.
2. [Friedman (2001), Greedy Function Approximation: A Gradient Boosting Machine](https://www.cmi.ac.in/~madhavan/courses/dmml2025/literature/Friedman-Gradient-Boosting-Machine-2001.pdf)

   Gradient boosting in function space.
3. [XGBoost — Introduction to Boosted Trees](https://xgboost.readthedocs.io/en/stable/tutorials/model.html)

   Second-order expansion, leaf scores and regularization.

   Apache-2.0 project; technical reference
4. [LightGBM — Features](https://lightgbm.readthedocs.io/en/stable/Features.html)

   Histograms, leaf-wise growth and the two original tree-growth figures.

   MIT; Microsoft and LightGBM developers
5. [LightGBM (2017)](https://proceedings.neurips.cc/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html)

   Original paper introducing GOSS and EFB.
6. [CatBoost — Transforming categorical features to numerical features](https://catboost.ai/docs/en/concepts/algorithm-main-stages_cat-to-numberic)

   Categorical statistics and priors.
7. [CatBoost: unbiased boosting with categorical features](https://arxiv.org/abs/1706.09516)

   Distinction between ordered boosting and categorical processing.
8. [LightGBM license](https://github.com/microsoft/LightGBM/blob/master/LICENSE)

   Full MIT license for the original figures.

   MIT
