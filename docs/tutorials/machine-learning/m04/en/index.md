# Explain predictions with regression, neighbors and Bayes

Source: https://ml-biomat.com/tutorials/machine-learning/m04/en/
Language: en

Read coefficients and residuals, then choose models for probabilities, counts and partially observed lifetimes.

## Begin with a prediction you can inspect

To forecast a shop's electricity consumption, a useful starting point adds contributions from opening hours, temperature and expected visitors. It may not immediately produce the most accurate forecast, but it permits concrete questions. How much does another opening hour change the prediction? Which days have large residuals? What value does the program insert when a feature is missing? Simple models expose the relationships between parameters, predictions and errors. Establishing such a baseline before trying a more complicated method makes it possible to identify what the added complexity actually solves.

This chapter moves from continuous predictions to classes and probabilities. Ordinary least squares, ridge regression and Lasso share a weighted-sum structure. Logistic regression converts a linear score into a probability. Nearest neighbors consult similar observations, while naive Bayes compares how likely different classes are to produce the observed features. Finally, counts and event times show why an ordinary straight line is not appropriate for every target. Poisson regression handles nonnegative counts, and survival analysis retains information from observations that ended before the event occurred.

The experiments use explicitly generated datasets so that their underlying relationships are known. Regression inputs include two strongly correlated features and randomly hidden measurements. Classification uses noisy interlocking moons. Counts follow an exponential mean, while component lifetimes are combined with independent observation deadlines. Each experiment answers its own question. Improvements refer to that generator and split rather than defining a permanent ranking of algorithms. Changing noise, correlation or observation duration provides controlled ways to investigate when the conclusions change.

## How does a line choose where to pass?

Linear regression expresses a prediction as weighted features plus an intercept. “Linear” primarily describes dependence on parameters. A model can include temperature squared or a product of two features and remain linear in their coefficients once those transformed inputs have been constructed. A coefficient describes the prediction change for a one-unit increase in its input while the model's other inputs remain fixed. That is a conditional relationship inside the model. If two real features always move together, changing only one may describe a situation outside the observed data region.

$$
\widehat y_i=b+\sum_{j=1}^p w_jx_{ij},\qquad r_i=y_i-\widehat y_i,\qquad\min_{b,\mathbf w}\sum_{i=1}^n r_i^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dbf1dc27226e2761db070ccb.svg) | Training sample count, feature count and their indices, unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/29313d2a94e65ab63aa973ae.svg) | Feature j of observation i and its weight; weight units are response units divided by feature units. |
| ![Formula](https://ml-biomat.com/static/agent-math/e6ed5d7ae8fdea0b1ed63fdc.svg) | Observed response, prediction, intercept and residual, all in response units. |
| ![Formula](https://ml-biomat.com/static/agent-math/1e6e60d2bfa1e755c04f563b.svg) | The p-vector of weights and minimization of summed squared residuals. |

For observations (2,4,6), a constant fit predicts mean 4, giving residuals (−2,0,2) and sum of squares 8. Constant 3 gives 1+1+9=11. The mean is the least-squares solution.

A residual is the observation minus its prediction, represented by a vertical displacement from a fitted curve. Least squares adds squared residuals and finds coefficients minimizing the total. Squaring prevents positive and negative errors from canceling and gives large discrepancies greater influence. For a constant prediction it selects the sample mean. For a line it chooses slope and intercept jointly. Geometrically, collect observations into one long vector: fitting projects that vector onto the space spanned by the feature columns. The resulting prediction is the closest point in that space under squared distance.

Using squared loss does not require every dataset to be exactly Gaussian. Independent Gaussian noise assumptions enter when interpreting least squares as maximum likelihood for a particular probability model. If noise variance changes with the inputs, a linear mean relation may still be useful, while coefficient standard errors and intervals require corresponding treatment. Large outliers receive substantial weight after squaring. Inspect residuals and original observations to determine whether they reflect genuine unusual conditions, measurement problems or structure missing from the model.

![Residuals for ninety shared test observations from three complete preprocessing–regression pipelines. Axes use generating-response units; color is the unmasked original feature x₀. The zero line helps reveal systematic discrepancies.](https://ml-biomat.com/static/tutorials/machine-learning/figures/c7b3100a1e8152726b72e14e.svg?v=c7b3100a1e81)

Figure 1Residuals for ninety shared test observations from three complete preprocessing–regression pipelines. Axes use generating-response units; color is the unmasked original feature x₀. The zero line helps reveal systematic discrepancies.

The experiment uses 210 training records and ninety test records. Its generating mean is twenty plus three effective linear feature contributions, with independent Gaussian noise of standard deviation 1.4. Random masking hides 147 entries among ten columns. Test RMSE is approximately 1.439 for ordinary least squares,1.414 for ridge and 1.386 for Lasso. Residual plots place predictions horizontally and observed-minus-predicted responses vertically, with color showing the first original feature. Curvature suggests omitted mean structure, while a spreading fan suggests changing variability. A single aggregate error cannot reveal these patterns.

## Stabilizing competing explanations

When two feature columns are nearly identical, many coefficient combinations produce similar predictions. For two closely agreeing thermometers, raising one coefficient while lowering the other may barely change their combined contribution. Small data perturbations can then cause large coefficient changes. Ridge regression penalizes squared coefficient magnitudes, making extreme compensating values expensive and encouraging smoother sharing of contributions. It usually shrinks coefficients continuously rather than setting them exactly to zero. This can stabilize prediction and estimation in some ill-conditioned or high-variance problems.

$$
J_{\rm Ridge}=\sum_i r_i^2+\alpha_R\sum_j w_j^2,\qquad J_{\rm Lasso}=\frac1{2n}\sum_i r_i^2+\alpha_L\sum_j|w_j|
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/479702a85ff3aefeab1ac2f7.svg) | Objective conventions of the two scikit-learn regressors here; intercepts are unpenalized and objectives have squared-response units. |
| ![Formula](https://ml-biomat.com/static/agent-math/864236b792cc24b490570b22.svg) | Residuals, weights, count and indices as defined above; standardized features make weights carry response units. |
| ![Formula](https://ml-biomat.com/static/agent-math/5e6bedf18d4ad0c1bae9a982.svg) | Nonnegative penalties; alpha_R is dimensionless here and alpha_L has response units, so their numerical values are not directly comparable. |

With residual sum 10, n=5 and weights (2,−1), ridge alpha_R=1 gives objective 15; Lasso alpha_L=1 gives objective 4. Their scales differ, so 15 versus 4 is not a model-performance comparison.

Lasso replaces the squared penalty with a sum of absolute coefficients, allowing some coefficients to become exactly zero. Tibshirani's 1996 paper brought shrinkage and variable selection into one formulation: retain useful fit while constructing a compact representation. A zero coefficient depends on the candidate features, their scales and the penalty. Among strongly correlated variables, choosing one and dropping another does not establish that the omitted variable has no real-world role. The two may simply provide very similar predictive information. Sparsity describes the fitted representation under its particular conditions.

![Coefficient paths computed on unmasked training features, distinct from the missing-data evaluation in Figure 1. Lines correspond to features; the models use different loss-scaling conventions for alpha.](https://ml-biomat.com/static/tutorials/machine-learning/figures/eb64fb4f166e6cc9d66ebe69.svg?v=eb64fb4f166e)

Figure 2Coefficient paths computed on unmasked training features, distinct from the missing-data evaluation in Figure 1. Lines correspond to features; the models use different loss-scaling conventions for alpha.

Each curve shows one feature coefficient as penalty strength increases. To isolate correlated-feature behavior, these paths use the unmasked ten-column generating data for the training observations. The preceding residual figure instead uses masked data with imputation. Ridge penalization suppresses the overall L2 norm of the coefficient vector. When two features are highly correlated, their contributions can be redistributed, so an individual coefficient need not decrease monotonically: the x₀ curve here first rises and then falls. Lasso paths can also reach exact zero. The two library implementations use different scaling conventions for the squared-error term, so matching numerical alpha values do not represent matched penalty strengths. Read each horizontal axis as a within-method progression, rather than comparing identically positioned points as equivalent settings.

The evaluated missing-data pipelines add ten missingness indicators, producing twenty input columns. Five-fold training-side validation selects ridge alpha 10 and Lasso alpha 0.1. Lasso retains seven nonzero coefficients, including three missingness indicators. The random-missingness generator assigns those indicators no true predictive role; their fitted values reflect finite data and the selected penalty. Distinguishing selection from discovery is essential when interpreting sparse models. Repeated splits and selection frequencies can investigate stability rather than treating one sparse coefficient table as a definitive mechanism.

## The steps before the model also learn from data

Feature engineering represents raw records in a form suited to the question. Encoding day of year directly from one to 365 makes late December appear far from early January; sine and cosine features express periodicity. Arbitrary codes 1,2,3 for unordered categories introduce nonexistent distances, while one-hot encoding avoids that order. An interaction feature lets the effect of temperature depend on humidity. Each transformation adds a structural assumption. Begin with the problem and measurement process, then compare representations using training-side evaluation rather than treating a long feature list as inherently informative.

A missing measurement is not zero. Replacing an absent temperature with zero can invent a cold event. Here a training median fills each missing value, and an indicator records that it was originally missing. The model can distinguish an observed near-median value from an imputed one. Median imputation is an explicit baseline; it does not recover the lost measurement. If missingness depends on equipment condition or the target, that process itself merits attention. New missingness patterns at prediction time also require checking that transformed columns and categories remain consistent with training.

A Pipeline binds imputation, scaling and fitting into one estimator. Each cross-validation fit learns medians, means and standard deviations from its training fold before transforming validation observations. Scaling matters especially for ridge and Lasso because penalties act directly on coefficients. Changing an input unit changes the coefficient needed to represent the same effect and can otherwise create an accidental penalty advantage. In nearest-neighbor models, scaling changes distances and therefore which observations are selected as neighbors. The same preprocessing step serves different mathematical roles in the two model families.

To express a standardized linear model in original units, divide each standardized coefficient by its training feature standard deviation and adjust the intercept for the means. Predictions after this conversion should match the original Pipeline observation by observation. This makes a useful verification exercise. With interactions, polynomial terms or missingness indicators, identify the exact feature associated with each coefficient: it may describe temperature squared or missing temperature, not temperature itself. Generating final feature names before interpreting coefficients prevents a printed vector of numbers from acquiring misleading labels.

## Turning a score into a class probability

Ordinary linear regression applied directly to binary labels can predict values below zero or above one. Logistic regression retains a linear score but maps it through an S-shaped function into the probability interval. A zero score gives probability 0.5; large positive and negative scores approach one and zero. Fitting minimizes the logarithmic loss of a Bernoulli model, explaining why a method named regression commonly serves classification. Producing a probability does not settle the action threshold. The default 0.5 threshold is one decision rule, and the task may justify another.

$$
z=b+\mathbf w^\top\mathbf x,\quad p=\frac1{1+e^{-z}},\quad\log\frac p{1-p}=z,\quad\ell=-y\log p-(1-y)\log(1-p)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a6645a980453d409ae0c7963.svg) | Input vector, matching weights, intercept and score; the score is dimensionless, with weights canceling input units. |
| ![Formula](https://ml-biomat.com/static/agent-math/537df2def454b5181de4f6e6.svg) | Positive-class probability and binary label, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/d733275f6c334d150d24653e.svg) | Per-observation Bernoulli negative log likelihood, exponential base and natural logarithm; loss is in nats. |

Score 0 gives p=0.5; score ln 3 gives p=0.75 and odds 3. For label 1 the loss is −ln 0.75≈0.2877; for label 0 it is −ln 0.25≈1.3863.

The linear relationship is on log odds. Odds divide event probability by nonevent probability; increasing one input by a unit multiplies the modeled odds by the exponential of its coefficient. It does not add a constant amount to probability. Near 0.5 the sigmoid is steep, so a score change alters probability more than it does near zero or one. Multiclass softmax jointly normalizes several scores to obtain class probabilities. Their relative values matter, while adding the same constant to every score leaves the probabilities unchanged.

![Shared noisy-moon generator and split. Backgrounds are fitted positive probabilities, solid lines are 0.5 boundaries, and points are 180 test observations. Flexible kNN decisions and finite-vote probabilities require separate evaluation.](https://ml-biomat.com/static/tutorials/machine-learning/figures/9bf922613c8bbc8147a6f8e6.svg?v=9bf922613c8b)

Figure 3Shared noisy-moon generator and split. Backgrounds are fitted positive probabilities, solid lines are 0.5 boundaries, and points are 180 test observations. Flexible kNN decisions and finite-vote probabilities require separate evaluation.

The comparison uses the same 420 training points and 180 test points for three classifiers. Interlocking moons have a nonlinear relationship, while ordinary logistic regression supplies a linear boundary and obtains 86.67% test accuracy. Adding appropriate nonlinear features can allow a model linear in its parameters to draw a curved boundary; kernel methods or neural networks provide other representations. Distinguish linear dependence on parameters from a straight line in the original coordinates, and keep representation selection on the training side of the evaluation workflow.

Probability quality also involves calibration: among observations assigned probability 0.8, do approximately 80% become positive over repeated comparable cases? Logistic regression is a useful probabilistic baseline, but omitted features, regularization, sampling proportions and distribution change affect calibration. Accuracy mainly concerns thresholded decisions, whereas logarithmic loss penalizes confident errors. The nearest-neighbor results next demonstrate why these metrics can rank two fitted models differently. Reading both prevents an improvement in discrete classification from being mistaken for an improvement in every use of the probabilities.

## Ask nearby observations, or compare class-generating mechanisms

k-nearest neighbors stores training observations, finds the k closest to a new input, and votes or averages their targets. Classification probabilities can use the class fractions among neighbors; regression averages their numerical responses. Small k follows local structure but is sensitive to individual noisy observations. Large k smooths the answer while potentially crossing genuine boundaries. Distance weighting emphasizes closer neighbors, but the distance must still be meaningful. In high dimensions, many irrelevant coordinates jointly influence distance, making feature selection, scaling and reduction important parts of the method.

With k=15, test accuracy is 93.89%, higher than ordinary logistic regression. Log loss is approximately 0.719, worse than logistic regression's 0.286. A finite neighbor vote can report exact zero or one probabilities, and a mistaken certainty incurs a very large logarithmic cost. The library clips probabilities numerically to retain finite values. This experiment suggests separate checks: inspect neighbors when seeking useful local classification, and investigate smoothing or calibration when probabilities will support risk and cost calculations. Classification accuracy and probability quality require their own evaluation.

$$
P(Y=c\mid\mathbf x)=\frac{\pi_c\prod_{j=1}^p q_j(x_j\mid c)}{\sum_{a=1}^{K}\pi_a\prod_{j=1}^p q_j(x_j\mid a)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f7fab13bb77748ab95824423.svg) | Class variable, candidate class, normalization index and class count. |
| ![Formula](https://ml-biomat.com/static/agent-math/9de4251bb30f6f1c6ecb6e56.svg) | Feature vector, feature j, dimension and feature index; here p denotes dimension rather than the previous probability. |
| ![Formula](https://ml-biomat.com/static/agent-math/ce006fb0b9eacb74e0eab1c1.svg) | Class prior and class-conditional feature probability or density; continuous densities have inverse-feature units that cancel in normalization. |
| ![Formula](https://ml-biomat.com/static/agent-math/40622fb44b3838693d5fff08.svg) | Posterior class probability, unitless; the product follows the conditional-independence assumption. |

With equal priors, feature probabilities 0.8 and 0.6 in class 1 and 0.2 and 0.3 in class 0 give unnormalized scores 0.24 and 0.03. The class 1 posterior is 0.24/0.27≈0.8889.

Naive Bayes follows a different route. Estimate how common each class is and how likely its features are within that class, then combine the evidence. The simplifying assumption is conditional independence of features given the class, replacing a high-dimensional joint distribution with a product of one-dimensional terms. GaussianNB uses class-conditional Gaussian distributions for continuous features. MultinomialNB is often appropriate for nonnegative word counts, and BernoulliNB represents feature presence or absence. Matching the input interpretation to the likelihood is more consequential than selecting a familiar function name.

Strongly correlated words can cause similar evidence to be counted repeatedly, producing overly confident probabilities even when class decisions remain useful. Count models also need smoothing so that an unseen class-word combination does not multiply a whole document likelihood by zero. GaussianNB obtains 86.67% accuracy and log loss around 0.298 on the moon data. These classes do not follow independent within-class Gaussian coordinates. Their fitted boundaries therefore show how modeling assumptions influence geometry, not merely another function call producing a percentage.

## Count targets need an appropriate mean structure

Daily visitor arrivals and hourly failure counts are nonnegative integers. An unrestricted linear prediction may assign them negative means. Generalized linear models separate three choices: the response distribution, a linear predictor formed from inputs, and a link connecting the conditional mean to that predictor. Gaussian linear regression uses an identity link, Bernoulli logistic regression a logit link, and Poisson regression commonly a logarithmic link. Adapting the response model can therefore preserve the transparent weighted-sum structure while respecting a different target type.

$$
Y\mid x\sim\operatorname{Poisson}(\mu),\qquad\log\mu=\beta_0+\beta_1x,\qquad\mu=e^{\beta_0+\beta_1x}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ae046271dd751e178814d5e7.svg) | Nonnegative integer count per fixed observation window and a dimensionless input. |
| ![Formula](https://ml-biomat.com/static/agent-math/75d2faaecd7646e08d872763.svg) | Positive conditional mean count, treated as a dimensionless number with fixed exposure. |
| ![Formula](https://ml-biomat.com/static/agent-math/134310dd50a86cb19a5b5082.svg) | Intercept and slope for the log mean; both dimensionless with the input scale here. |
| ![Formula](https://ml-biomat.com/static/agent-math/c1afb732f9f6f9c82d604b05.svg) | The observation follows the stated Poisson distribution, whose conditional variance also equals mu. |

With coefficients 0.5 and 0.8, x=0 gives mean exp(0.5)≈1.649. Increasing x by 1 multiplies the mean by exp(0.8)≈2.226. Observed counts are integers while their mean need not be.

![Poisson counts in equal exposure windows: held-out observations, known generating mean, Poisson GLM and OLS predictions. Response is count per window; input is dimensionless.](https://ml-biomat.com/static/tutorials/machine-learning/figures/e7ea79dc705842ea823cea09.svg?v=e7ea79dc7058)

Figure 4Poisson counts in equal exposure windows: held-out observations, known generating mean, Poisson GLM and OLS predictions. Response is count per window; input is dimensionless.

Four hundred inputs correspond to equal observation windows. Their generating mean is exp(0.5+0.8x), and observations are drawn from the corresponding Poisson distributions. Fitting 300 records estimates an intercept of approximately 0.449 and slope 0.757. Finite observations and count variation explain why they differ from the generating values. The plot places held-out counts, the known mean, the Poisson fit and an ordinary line together. Conditional Poisson variance equals its mean; substantially greater observed variability motivates examining omitted factors, overdispersion or a more suitable response distribution.

Counts collected over different exposure durations need corresponding treatment. Two hours naturally permit more failures than half an hour, even at the same rate. Express expected count as exposure times rate. Under a log link, log exposure enters as a known offset. This differs from treating duration as an unconstrained feature whose coefficient is estimated. Distinguishing a fixed exposure coefficient from a freely fitted effect preserves the intended model. Equal-length windows in this experiment isolate the role of the link before introducing the additional exposure issue.

## What do we learn when failure has not yet been observed?

In a lifetime test, some components fail before observation ends and others remain operational. The latter lifetimes are neither zero, equal to the observation duration, nor infinite. We know that they exceed a particular time. This is right censoring, requiring both an observed duration and an indicator of whether an event actually occurred at its endpoint. Discarding censored components overrepresents early failures. Treating their observation deadlines as failure times invents premature events. A time-to-event analysis retains the partial information that ordinary regression would misinterpret.

Kaplan and Meier's 1958 incomplete-observation problem asks how to estimate the proportion remaining event-free beyond a given time. At every event time, count the risk set: observations still followed and still event-free immediately before that time. Divide the number surviving that step by the number at risk, then multiply these successive conditional proportions. Censoring does not cause an immediate downward step, but the censored observation leaves later risk sets. This product-limit construction turns an apparently abstract survival function into a sequence of small, inspectable calculations.

$$
\widehat S(t)=\prod_{t_j\le t}\left(1-\frac{d_j}{n_j}\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/00cba27d47f7255c4c5fcff0.svg) | Estimated event-free survival beyond time t; time is in hours and probability is unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/7de582841847008ad5e72738.svg) | Distinct event time and its index; factors occur only at event times. |
| ![Formula](https://ml-biomat.com/static/agent-math/9eb35de5f12a2aa16d422828.svg) | Events at time t_j and observations at risk immediately before it, unitless counts. |
| ![Formula](https://ml-biomat.com/static/agent-math/eddaa20e15661440b4bf8d78.svg) | Multiply conditional survival fractions over event times, under suitable independent-censoring conditions. |

For endpoints 2,3,4,5 hours, with hour 3 censored and others events, the first factor is 3/4. Hour 3 removes an at-risk observation without a drop. Hour 4 contributes 1/2, giving 3/8; the final event reduces the estimate to zero.

![Left: observed timelines for the first twelve components, with events as circles and censoring as ticks. Right: Kaplan–Meier for eighty components against the generating survival with mean ten hours. Small ticks indicate censoring.](https://ml-biomat.com/static/tutorials/machine-learning/figures/c200f049964175495cf08198.svg?v=c200f0499641)

Figure 5Left: observed timelines for the first twelve components, with events as circles and censoring as ticks. Right: Kaplan–Meier for eighty components against the generating survival with mean ten hours. Small ticks indicate censoring.

The experiment draws lifetimes from an exponential distribution with mean ten hours and independently draws observation deadlines uniformly between two and eighteen hours. It produces fifty observed events and thirty censored records. The first panel displays twelve component timelines; the second compares estimated and generating survival curves. Independent censoring allows the observed risk set to represent the relevant surviving population. If equipment close to failure is particularly likely to lose its records, censoring changes that representation, motivating a model of recording conditions or a revised monitoring design.

Survival probability is the probability that the event has not occurred by time t. Hazard is a conditional instantaneous event rate among those still surviving at t and has inverse-time units; it is not a probability at one exact instant. Covariates such as temperature and load can enter models such as Cox proportional hazards or accelerated failure time models. The former describes hazard ratios, while the latter describes stretches or contractions of the time scale. Their assumptions and time-specific evaluation matter when moving beyond the descriptive curve. Feeding censored durations into ordinary regression loses the event-status distinction.

## Maintain a risk set by hand

Checked means an event; unchecked means censoring. All four components enter at hour 0. Risk counts and survival update together.

[Figure: Risk set and survival probability](https://ml-biomat.com/tutorials/machine-learning/m04/en/#M04-plot)

| Time (hours) | At risk | Events | Survival |
| --- | --- | --- | --- |

The interactive example fixes four observation endpoints at two, three, four and five hours. Change whether each endpoint represents an event or censoring and inspect the risk counts, survival factors and cumulative curve together. By default the third-hour endpoint is censored. One event among four at hour two gives survival 3/4; at hour four only two remain at risk, and one event reduces cumulative survival to 3/8. Incomplete lifetimes thus contribute usable information through a calculation that can be verified without accepting the estimator as a black box.

## Choose a baseline that reveals the next useful experiment

For continuous targets, begin with regression coefficients and residuals, then compare ridge and Lasso when correlation, dimensionality or stability matter. For classification, use logistic regression to inspect a linear score, neighbors to inspect local geometry, and naive Bayes to inspect simplified class-conditional assumptions. Counts and censored times require an appropriate target model first. These methods are different hypotheses to test, rather than positions on a simple-to-advanced leaderboard. A useful starting model makes the next improvement understandable.

### Complete example: basic model families and censoring

Requires NumPy, Matplotlib and scikit-learn. Run python main.py --output results --language en. Generators, pipelines, training-side search, test outputs and five figure groups share the script; KM includes a four-observation hand check.

```
"""Interpretable baseline models and explicit censoring on seeded teaching data."""
import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split,GridSearchCV,KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler,PolynomialFeatures
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression,Ridge,Lasso,LogisticRegression,PoissonRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import mean_squared_error,accuracy_score,log_loss

def kaplan_meier(duration,event):
 times=np.unique(duration[event]);survival=1.;ys=[];risk=[];deaths=[]
 for tm in times:
  n=int(np.sum(duration>=tm));d=int(np.sum((duration==tm)&event));survival*=1-d/n;ys.append(survival);risk.append(n);deaths.append(d)
 return np.r_[0,times],np.r_[1,ys],risk,deaths

def main(output,language):
 out=Path(output);out.mkdir(parents=True,exist_ok=True);rng=np.random.default_rng(44);zh=language=='zh'
 plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False})
 def t(z,e):return z if zh else e
 def save(f,n):f.savefig(out/f'{n}-{language}.svg',bbox_inches='tight');plt.close(f)
 # Regression: a known mean relation with correlated measurements and missing values.
 X=rng.normal(size=(300,10));X[:,1]=X[:,0]+rng.normal(0,.08,300);truth=np.array([2.,0.,-1.5,1.,0.,0.,0.,0.,0.,0.]);y=20+X@truth+rng.normal(0,1.4,300)
 missing=rng.random(X.shape)<.06;Xm=X.copy();Xm[missing]=np.nan;tr,te=train_test_split(np.arange(300),test_size=.3,random_state=44)
 cv=KFold(5,shuffle=True,random_state=44);results={};fits={}
 for name,est,grid in [('OLS',LinearRegression(),None),('Ridge',Ridge(),{'ridge__alpha':[.01,.1,1,10,100]}),('Lasso',Lasso(max_iter=10000),{'lasso__alpha':[.001,.01,.05,.1,.3]})]:
  pipe=make_pipeline(SimpleImputer(strategy='median',add_indicator=True),StandardScaler(),est)
  fitted=GridSearchCV(pipe,grid,cv=cv,scoring='neg_mean_squared_error') if grid else pipe;fitted.fit(Xm[tr],y[tr]);pred=fitted.predict(Xm[te]);best=fitted.best_estimator_ if grid else fitted
  results[name]={'test_rmse':float(np.sqrt(mean_squared_error(y[te],pred))),'selected':fitted.best_params_ if grid else {},'coefficients':best[-1].coef_.tolist(),'nonzero_coefficients':int(np.sum(np.abs(best[-1].coef_)>1e-9))};fits[name]=(best,pred)
 fig,axs=plt.subplots(1,3,figsize=(12,3.7),layout='constrained')
 for ax,(name,(m,pred)) in zip(axs,fits.items()):
  ax.scatter(pred,y[te]-pred,c=X[te,0],cmap='viridis',s=19,alpha=.8);ax.axhline(0,color='#d48745');ax.set(title=f'{name}: RMSE={results[name]["test_rmse"]:.3f}',xlabel=t('预测响应','Predicted response'),ylabel=t('观测−预测','Observed minus predicted'));ax.set_ylim(-5.5,5.5)
 fig.colorbar(axs[0].collections[0],ax=axs,shrink=.8,label=t('特征x₀（无量纲）','Feature x₀ (dimensionless)'));save(fig,'residuals')
 clean=StandardScaler().fit_transform(X[tr]);alphas=np.logspace(-3,2,60);paths={};fig,axs=plt.subplots(1,2,figsize=(11,4),layout='constrained')
 for ax,(name,cls) in zip(axs,[('Ridge',Ridge),('Lasso',Lasso)]):
  coefs=np.array([cls(alpha=a,max_iter=10000).fit(clean,y[tr]).coef_ for a in alphas]);paths[name]=coefs
  for j in range(10):ax.semilogx(alphas,coefs[:,j],label=f'x{j}',lw=2 if j<4 else .8,alpha=1 if j<4 else .5)
  ax.set(title=name,xlabel=t('惩罚参数 alpha（各模型约定不同）','Penalty alpha (model conventions differ)'),ylabel=t('标准化特征的系数','Coefficient of standardized feature'));ax.axhline(0,color='#b0c2cb',lw=.7)
 axs[1].legend(ncol=2,fontsize=9);save(fig,'regularization')
 # Identical held-out moon observations for three basic classifiers.
 Xc,yc=make_moons(n_samples=600,noise=.25,random_state=44);ct,ce=train_test_split(np.arange(600),test_size=.3,stratify=yc,random_state=44)
 gx,gy=np.meshgrid(np.linspace(-1.8,2.8,230),np.linspace(-1.3,1.9,160));grid=np.c_[gx.ravel(),gy.ravel()];class_results={};fig,axs=plt.subplots(1,3,figsize=(12,3.7),layout='constrained')
 for ax,(name,clf) in zip(axs,[('Logistic',LogisticRegression()),('kNN k=15',KNeighborsClassifier(n_neighbors=15)),('Gaussian NB',GaussianNB())]):
  pipe=make_pipeline(StandardScaler(),clf);pipe.fit(Xc[ct],yc[ct]);prob=pipe.predict_proba(Xc[ce])[:,1];field=pipe.predict_proba(grid)[:,1].reshape(gx.shape);ax.contourf(gx,gy,field,levels=np.linspace(0,1,11),cmap='RdBu_r',alpha=.6);ax.contour(gx,gy,field,levels=[.5],colors='#243b49',linewidths=1.2);ax.scatter(*Xc[ce].T,c=yc[ce],cmap='RdBu_r',edgecolor='white',linewidths=.4,s=17);ax.set(title=name,xlabel='x₀',ylabel='x₁');class_results[name]={'accuracy':float(accuracy_score(yc[ce],prob>=.5)),'log_loss':float(log_loss(yc[ce],np.c_[1-prob,prob]))}
 fig.colorbar(axs[0].collections[0],ax=axs,shrink=.8,label=t('正类预测概率','Predicted positive probability'));save(fig,'classification')
 # Poisson response: expected count exp(0.5+0.8*x), one equal exposure unit each.
 xp=rng.uniform(-2,2,400);mu=np.exp(.5+.8*xp);yp=rng.poisson(mu);pr,pe=train_test_split(np.arange(400),test_size=.25,random_state=44)
 pm=PoissonRegressor(alpha=0,max_iter=1000).fit(xp[pr,None],yp[pr]);lm=LinearRegression().fit(xp[pr,None],yp[pr]);xx=np.linspace(-2,2,250)
 fig,ax=plt.subplots(figsize=(8,4),layout='constrained');ax.scatter(xp[pe],yp[pe],alpha=.5,s=20,color='#536e80',label=t('测试计数','Test counts'));ax.plot(xx,np.exp(.5+.8*xx),'--',color='#111827',label=t('生成均值','Generating mean'));ax.plot(xx,pm.predict(xx[:,None]),color='#167d87',lw=2,label='Poisson GLM');ax.plot(xx,lm.predict(xx[:,None]),color='#d48745',label='OLS');ax.set(xlabel=t('无量纲输入','Dimensionless input'),ylabel=t('每个等长观察窗的计数','Count per equal observation window'));ax.legend();save(fig,'poisson')
 # Independent right censoring of exponential lifetimes, time unit: hours.
 lifetime=rng.exponential(10,80);censor=rng.uniform(2,18,80);duration=np.minimum(lifetime,censor);event=lifetime<=censor;tm,surv,risk,deaths=kaplan_meier(duration,event);truegrid=np.linspace(0,20,200)
 fig=plt.figure(figsize=(11,4.5),layout='constrained');gs=fig.add_gridspec(1,2,width_ratios=[1,1.25]);ax=fig.add_subplot(gs[0,0]);
 for i in range(12):ax.plot([0,duration[i]],[i,i],color='#96aeb8');ax.scatter(duration[i],i,marker='o' if event[i] else '|',s=60,color='#d48745' if event[i] else '#167d87')
 ax.set(xlabel=t('观察时间（小时）','Observed time (hours)'),ylabel=t('前12个部件','First 12 components'),title=t('圆点：事件；竖线：删失','Circle: event; tick: censoring'));ax=fig.add_subplot(gs[0,1]);ax.step(np.r_[tm,duration.max()],np.r_[surv,surv[-1]],where='post',color='#167d87',lw=2,label='Kaplan–Meier');ax.plot(truegrid,np.exp(-truegrid/10),'--',color='#34495e',label=t('生成生存函数','Generating survival'))
 censor_surv=np.array([surv[np.searchsorted(tm,d,side='right')-1] for d in duration[~event]]);ax.scatter(duration[~event],censor_surv,marker='|',color='#167d87',label=t('删失','Censored'));ax.set(xlabel=t('时间（小时）','Time (hours)'),ylabel=t('生存概率 S(t)','Survival probability S(t)'),ylim=(0,1.03));ax.legend();save(fig,'survival')
 hand_t=np.array([2.,3.,4.,5.]);hand_e=np.array([1,0,1,1],dtype=bool);ht,hs,_,_=kaplan_meier(hand_t,hand_e)
 summary={'regression_train':len(tr),'regression_test':len(te),'regression':results,'missing_cells':int(missing.sum()),'classification_train':len(ct),'classification_test':len(ce),'classification':class_results,'poisson_intercept':float(pm.intercept_),'poisson_slope':float(pm.coef_[0]),'survival_n':len(duration),'events':int(event.sum()),'censored':int((~event).sum()),'km_hand_times':ht.tolist(),'km_hand_survival':hs.tolist()}
 (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');np.savez(out/'experiment_data.npz',X=X,X_missing=Xm,y=y,train=tr,test=te,X_class=Xc,y_class=yc,class_train=ct,class_test=ce,lifetime=lifetime,censor=censor,duration=duration,event=event,poisson_x=xp,poisson_y=yp)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--language',choices=['zh','en'],default='en');a=ap.parse_args();main(a.output,a.language)
```

The complete example includes generators, missing-value handling, cross-validation, predictions and figures. Increase feature correlation and inspect coefficient stability; increase moon noise and compare changes in accuracy and log loss; then shorten observation deadlines and inspect how additional censoring affects the survival-curve tail. Change one major factor at a time while retaining split rules and seeds. Each run then answers a defined question instead of becoming a succession of algorithm names whose effects are difficult to disentangle.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M04.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [scikit-learn — Linear Models](https://scikit-learn.org/stable/modules/linear_model.html)

   Least squares, regularization, logistic regression and GLMs.

   BSD-3-Clause
2. [scikit-learn — Nearest Neighbors](https://scikit-learn.org/stable/modules/neighbors.html)

   Neighbors, metrics and dimensionality.

   BSD-3-Clause
3. [scikit-learn — Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html)

   Conditional independence and feature distributions.

   BSD-3-Clause
4. [Tibshirani (1996), Regression Shrinkage and Selection via the Lasso](https://www2.stat.duke.edu/courses/Spring06/sta395/tibshirani.pdf)

   Original study joining shrinkage and variable selection.
5. [Kaplan & Meier (1958), Nonparametric Estimation from Incomplete Observations](https://web.stanford.edu/~lutian/coursepdf/KMpaper.pdf)

   Incomplete observations and the product-limit estimator.
