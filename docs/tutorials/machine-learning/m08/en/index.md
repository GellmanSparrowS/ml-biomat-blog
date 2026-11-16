# What changes when we intervene? Causal inference and experimental design

Source: https://ml-biomat.com/tutorials/machine-learning/m08/en/
Language: en

From the umbrella paradox to randomization, observational adjustment, natural experiments and power.

## What would the same customer have done without a coupon?

A shop finds that customers who redeem a coupon spend more than customers who do not. Increasing coupon distribution seems an obvious next step, until we ask what the recipients would have spent without the offer. Frequent shoppers may be more likely to receive a coupon and already have larger shopping baskets. The observed difference then combines the effect of the offer with differences between people. A prediction model can use coupon status to forecast spending. Deciding whether to distribute more coupons asks a different question: how would changing the distribution policy change spending?

Potential outcomes make that question precise by describing the result for the same unit under two alternative treatments. Only one outcome is observed; the other is counterfactual. Neyman's 1923 work on agricultural experiments organized comparisons around the potential yields of plots under different varieties, a structure preserved in its 1990 English translation. A plot, a shopper and a machine present the same basic problem: we cannot observe the same unit fully experiencing two mutually exclusive conditions at the same time. Randomization and other causal designs provide ways to estimate comparisons despite that missing observation.

$$
Y_i=T_iY_i(1)+(1-T_i)Y_i(0),\quad \tau_i=Y_i(1)-Y_i(0),\quad \tau=\mathbb E[\tau_i]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e237eb39dd0ac5fddf41116f.svg) | Unit index and binary treatment indicator; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/47c4ee00ae1de0cd2e269513.svg) | Treated and untreated potential outcomes, and observed outcome; outcome units. |
| ![Formula](https://ml-biomat.com/static/agent-math/ed1b2a0aa311d96ecb05967c.svg) | Individual effect, target-population average effect, and expectation over that population; outcome units. |

Potential spending of 12 and 9 gives effect 3. Treatment reveals 12 and control reveals 9. The identity uses consistency for the specified treatment version.

The coupon experiment in this chapter has an explicit synthetic mechanism. Six pretreatment features are uniformly distributed between −2 and 2. The first feature affects assignment, the untreated outcome and the treatment effect. The effect ranges from approximately zero to two outcome units, with population average one. The simulator stores both potential outcomes, while each estimator sees only the outcome corresponding to the assigned treatment. This separation lets us follow an observational analysis and still use the known generating mechanism to locate errors. A finite sample has its own average effect, which can differ slightly from the generating population average.

A useful causal question also specifies treatment versions, the target population, the outcome window and possible interactions between units. A minimum-spend coupon and an unconditional discount are different treatments; same-day spending and seven-day spending are different outcomes. If family members share coupons, one person's assignment can change another person's outcome. Assignment at household level or an explicit interference model would then fit the question better. These details define the quantity being estimated. They are as much a part of the calculation as the final regression coefficient.

## Draw why the comparison groups differ

Rain increases both umbrella use and the chance of getting wet. Umbrella users can therefore have a higher observed wetting rate even when umbrellas protect people under the same weather conditions. A causal graph draws three relationships: rain to umbrella use, rain to wetting, and umbrella use to wetting. Rain is a common cause that creates a backdoor path between treatment and outcome. Comparing umbrella users and nonusers within the same weather, then combining those comparisons using the target population's weather proportions, removes the composition difference due to this measured common cause.

$$
\mathbb E[Y\mid\operatorname{do}(T=t)]=\sum_x\mathbb E[Y\mid T=t,X=x]P(X=x)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3ba0d89b068fe27c0c672309.svg) | Outcome, treatment variable and assigned treatment value; outcome measurement units, categorical treatment. |
| ![Formula](https://ml-biomat.com/static/agent-math/93ff10e0b86ffafa9dd3c1c4.svg) | Pretreatment adjustment variable, category and target-population probability; dimensionless probability. |
| ![Formula](https://ml-biomat.com/static/agent-math/8bf285eaef0939b34185f166.svg) | Conditional expectation, sum over categories and intervention; this sum is for discrete X. |

Under graphical adjustment, overlap and consistency, combine stratum means using target proportions. Umbrella risks 0.4/0.01 weighted by 0.3/0.7 give 0.127; no umbrella gives 0.3×0.9+0.7×0.02=0.284.

## Observe umbrella users, or intervene on the same population

Change rain prevalence, selection and protection. Observation compares self-selected groups; intervention retains the same weather composition and cuts the incoming rain-to-umbrella arrow.

[Figure: Causal graph and wetting probabilities](https://ml-biomat.com/tutorials/machine-learning/m08/en/#M08-plot)

Every probability in the interaction is a displayed teaching assumption. Initially, 30% of days are rainy; umbrella use is 90% on rainy days and 10% on dry days. On rainy days, umbrellas reduce the wetting probability from 0.9 to 0.4. Umbrella users are heavily concentrated among rainy days, giving an observed wetting rate near 0.320, compared with 0.060 among nonusers. Setting umbrella use for the same target population instead gives rates 0.127 and 0.284, a difference of −0.157. The interaction changes group composition and the incoming arrow together, so the distinction is visible in both numbers and mechanism.

Adjustment follows relationships, rather than a rule to include every available column. Pretreatment common causes usually need adjustment. A mediator lies on a causal pathway after treatment; controlling it changes the effect being estimated. A collider receives arrows from two variables. For example, technical ability and a referral may both influence interview selection. Restricting analysis to interviewed applicants can create an association between ability and referrals even if they were initially independent. Selection, mediation and confounding thus require different reasoning. Measuring more variables helps when we also understand where they belong in the process.

![DoWhy example graph showing treatment, outcome and other causal variables.](https://ml-biomat.com/static/tutorials/machine-learning/figures/d16bf35d97928117c6aae74d.png?v=d16bf35d9792)

Figure 1Original DoWhy causal-graph example: trace the common causes, instrument, treatment and outcome. PyWhy/DoWhy project, MIT license, unmodified.

The public DoWhy graph places common causes, an instrument, treatment and outcome in one picture. Reading each arrow is a useful preparation for analysis: the graph expresses assumptions about mechanisms, identification asks whether the target follows from those assumptions and observed data, and estimation chooses a numerical procedure. When a common cause is missing, a productive next step is to measure it or find a different assignment mechanism. Increasing the predictive capacity of a regression model changes how observed relationships are fitted; acquiring the missing causal information requires a change in measurement or design.

## How random assignment creates a comparison

Randomized experiments make assignment independent of pretreatment potential outcomes by design. Across repetitions of the randomization, population differences between groups cancel on average, allowing a difference in group means to estimate an average effect. A particular finite experiment can still have imbalances in age, demand or baseline performance. Assignment records, implementation checks and uncertainty calculations remain part of the analysis. Stratified randomization assigns within important categories; cluster randomization assigns households, classrooms or stores. The uncertainty calculation must follow that assignment unit, because several people in the same assigned cluster do not provide several independent assignments.

$$
\widehat\tau=\overline Y_1-\overline Y_0,\qquad \widehat{\operatorname{SE}}=\sqrt{s_1^2/n_1+s_0^2/n_0}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a62f35d39c75449fe5e10640.svg) | Estimated effect and sample outcome mean in group g=0 or 1; outcome units. |
| ![Formula](https://ml-biomat.com/static/agent-math/ed135ab2bddd4999f47e8a94.svg) | Within-group sample variance and independent-unit count; squared outcome units and counts. |
| ![Formula](https://ml-biomat.com/static/agent-math/e06a2e9c61e7893c25a5dab9.svg) | Estimated standard error of an independent two-group mean difference; outcome units. |

Independent group-mean variances add. Means 5 and 3, sample variances 4 and 9, and 100 people each give effect 2 and SE √0.13≈0.361. Cluster designs require assignment-level variance calculations.

A public historical trial connects raw counts to interpretable effect scales. The 1989 final Physicians' Health Study report recorded 139 myocardial infarctions among 11,037 male physicians assigned aspirin and 239 among 11,034 assigned placebo. The corresponding crude event fractions are about 12.59 and 21.66 per thousand, a difference of −9.07 per thousand and a crude ratio near 0.581. Our code calculates these summaries directly from the reported counts. The paper also contains adjusted analyses and follow-up information, which produce different statistical quantities. Keeping the calculation attached to its denominator makes the comparison easy to reconstruct.

Assignment, actual uptake and sustained use should be recorded separately. Comparing randomized groups estimates an intention-to-treat effect, including the adherence patterns that occurred in the trial. Selecting only people who followed the treatment introduces self-selection again. A coupon likewise moves through assignment, notification, claiming and purchase. The policy may control the first step, while later steps depend on customers. Choosing the controllable action and stating whether the comparison concerns assigned customers, claimants or users keeps the estimated effect connected to the decision the experiment was designed to inform.

## Matching and weighting reshape observational comparisons

When random assignment is unavailable, matching searches for comparable units using recorded pretreatment features. Here, the three relevant features are standardized, and each treated record is paired with its nearest untreated neighbor, allowing replacement. Averaging the resulting differences targets the average treatment effect among treated people, ATT. If people with larger effects are more likely to receive treatment, ATT differs from the whole-population ATE. The different target is substantive: the question becomes what treatment did for those who received it. Comparing that answer with the population ATE as if both were estimates of the same quantity would confuse population composition with estimator error.

A propensity score is the probability of receiving treatment given pretreatment features. Inverse-probability weighting gives more influence to treated people who were unlikely to be treated, and to untreated people who were unlikely to remain untreated. This reconstructs more comparable weighted populations. It requires both treatment options to occur in relevant feature regions, along with sufficient measured common causes. A region containing almost exclusively treated people yields large weights for its few controls. Restricting the target to a supported population or gathering additional controls addresses that information shortage directly.

$$
e_i=P(T_i=1\mid X_i),\qquad\widehat\tau_{\rm IPW}=\frac1n\sum_{i=1}^n\left[\frac{T_iY_i}{e_i}-\frac{(1-T_i)Y_i}{1-e_i}\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/abc3f76f8225d9caf149a4a3.svg) | Unit index, sample size, binary treatment, outcome and pretreatment feature vector; outcome measurement units. |
| ![Formula](https://ml-biomat.com/static/agent-math/e6d27b68a3f1be1ab997a076.svg) | Treatment probability conditional on features; dimensionless and between zero and one; fitted probabilities are used in estimation. |
| ![Formula](https://ml-biomat.com/static/agent-math/30f485c2b5f41881b79cd1a9.svg) | Inverse-probability weighted average effect and sum over units; outcome units. |

Assignment probability e cancels weight 1/e. For two treated outcomes 4,6 and two controls 2,4, all with e=0.5, the estimate is (8+12−4−8)/4=2. Identification uses consistency, conditional exchangeability and positivity.

![Propensity overlap, six-feature balance and ATE estimates for the same 3,000 records. Dashed line: generating population ATE=1; AIPW interval: approximate influence-score 95% interval.](https://ml-biomat.com/static/tutorials/machine-learning/figures/dffa1f45943ce729ddbba6f5.svg?v=dffa1f45943c)

Figure 2Propensity overlap, six-feature balance and ATE estimates for the same 3,000 records. Dashed line: generating population ATE=1; AIPW interval: approximate influence-score 95% interval.

The synthetic sample contains 3,000 records, with 1,490 treated and 1,510 controls. The unadjusted mean difference is about 2.249, ordinary IPW gives 0.979, and the Hájek version, which normalizes each group's weights separately, gives 0.924. The generating population ATE is one. The first feature's absolute standardized mean difference falls from approximately 0.687 to 0.0065. The figure shows propensity overlap and balance across all six measured features, allowing the effect estimate to be read alongside the comparisons that support it. The completeness of the common-cause measurements is assessed through design knowledge and sensitivity analysis.

Nearest-neighbor matching estimates ATT at approximately 1.226, compared with the simulator's treated-sample effect of 1.204. Both exceed the population ATE, as expected when the first feature increases both treatment probability and treatment benefit. The number of matched pairs is also different from the number of distinct independent controls: replacement lets a single control contribute to several differences. Standard errors need to handle that dependence. The saved matching indices let readers inspect reuse directly rather than treating every pair as an independent observation simply because it occupies a separate row.

## Use prediction models to estimate treatment effects

Machine learning can predict treatment probability and predict outcomes separately under treatment and control. Causal estimators arrange these predictions into particular correction formulas. Augmented IPW first predicts a treatment contrast for every unit, then adds propensity-weighted residual corrections based on the observed treatment and outcome. It combines outcome regression with weighting. Double robustness describes a consistency property under suitable conditions when one of the two nuisance-model families is correct. In finite samples, prediction errors and extreme weights still affect precision; the property concerns how estimation behaves under specified model conditions rather than the ranking of estimates in every dataset.

$$
\widehat\tau_{\rm AIPW}=\frac1n\sum_i\left[\widehat m_1(X_i)-\widehat m_0(X_i)+\frac{T_i(Y_i-\widehat m_1(X_i))}{\widehat e_i}-\frac{(1-T_i)(Y_i-\widehat m_0(X_i))}{1-\widehat e_i}\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/82967c0626fb473fc2c047fb.svg) | Unit index, sample count, features, binary treatment and observed outcome. |
| ![Formula](https://ml-biomat.com/static/agent-math/2d470acda069ebd1f6d52cd3.svg) | Out-of-fold estimated outcome mean for treatment t and propensity; outcome units and dimensionless probability. |
| ![Formula](https://ml-biomat.com/static/agent-math/4b2f5c53de0b7adc153583bf.svg) | Augmented-IPW average effect and sum over all units; outcome units. |

Start with the predicted contrast, then correct with observed residuals. A treated unit with m1=5, m0=3, e=0.5 and Y=6 contributes 2+(6−5)/0.5=4. Average all scores. Double robustness is a model-consistency property under suitable conditions.

Cross-fitting supplies every record with nuisance predictions made by models that did not train on that record. The code splits the data into five folds, fits propensity and outcome models on four, predicts the held-out fold, and combines the out-of-fold predictions. AIPW is approximately 0.945, with an influence-score-based approximate 95% interval from 0.858 to 1.033. Ordinary IPW happens to be closer to one in this particular sample. Repeated samples and changes to nuisance-model specifications help assess precision and robustness beyond this single realized error.

Double machine learning uses an orthogonalization approach. Predict the conditional means of outcome and treatment, subtract them, and explain residual outcome variation using residual treatment variation. The code represents the conditional effect as a linear function of the first feature. Its fitted intercept is about 0.937 and slope about 0.531, compared with generating values one and 0.5. The first feature has population mean zero, so the intercept is the population ATE in this construction. Averaging the fitted function over a different target population would generally yield a different average effect.

$$
\widetilde Y_i=Y_i-\widehat m(X_i),\quad \widetilde T_i=T_i-\widehat e(X_i),\quad\widehat{\boldsymbol\theta}=\arg\min_{\theta_0,\theta_1}\sum_i[\widetilde Y_i-\widetilde T_i(\theta_0+\theta_1X_{i0})]^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3caa0fc11feacec3e9107dc0.svg) | Unit index, six-dimensional feature vector and first feature; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/9cd0ac3ebae962df3781b107.svg) | Outcome, treatment, out-of-fold conditional means and residuals; Y quantities in outcome units, T quantities dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/d5760dc4f1c7b29e4955d631.svg) | Conditional-effect intercept, slope, two-parameter estimate, minimizer and unit sum; parameters have outcome units for dimensionless features. |

Remove predictable background through conditional means. Residual T=0.4, X0=1 and θ=(1,0.5) predict residual outcome 0.4×1.5=0.6. The specified linear effect is fitted by least squares on two residual-design columns.

![Left: generating and DML conditional effects. Right: ATE and treated-population ATT with their corresponding targets; the two bars concern different populations.](https://ml-biomat.com/static/tutorials/machine-learning/figures/987e310878fe3a69f72ecbc0.svg?v=987e310878fe)

Figure 3Left: generating and DML conditional effects. Right: ATE and treated-population ATT with their corresponding targets; the two bars concern different populations.

Effect heterogeneity asks who changes more because of treatment, which differs from asking who has a larger outcome to begin with. A high-spending customer whose purchases barely respond to a coupon differs from a moderate-spending customer with a large response. A conditional average effect describes a subgroup defined by features; its estimate does not reveal each person's two exact potential outcomes. Policy selection and subgroup predictions need evaluation matched to the intended decision. Stating the population, effect-function assumptions and evaluation design gives prediction models a clear role in causal research.

## An instrument offers another source of assignment variation

Participation in training may depend on motivation, which also affects later performance and is incompletely measured. Suppose a randomly sent encouragement changes participation. It may serve as an instrument if it changes participation, is independent of the relevant latent causes, and influences the outcome only through training. The last condition is an exclusion restriction. If the encouragement itself motivates additional study among people who never attend, that restriction fails. The useful variation comes from this collection of mechanisms; correlation between the proposed instrument and participation is only one component.

$$
\widehat\tau_{\rm IV}=\frac{\overline Y_{Z=1}-\overline Y_{Z=0}}{\overline T_{Z=1}-\overline T_{Z=0}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b317ec89cfcc2f4f9f025e45.svg) | Binary instrument, actual treatment and outcome; Z/T dimensionless, Y in outcome units. |
| ![Formula](https://ml-biomat.com/static/agent-math/92ff81cb81b642357084631d.svg) | Outcome means and treatment fractions within instrument group z=0 or 1. |
| ![Formula](https://ml-biomat.com/static/agent-math/e02ece28c9c8e3120f322e0f.svg) | Wald effect estimate in outcome units; denominator is the first-stage difference. |

An outcome increase 0.6 and treatment-rate increase 0.3 give effect 2. Causal interpretation uses independence, exclusion, relevance and suitable effect or monotonicity assumptions. A small denominator amplifies random differences.

The experiment generates randomized encouragement while allowing hidden motivation to influence participation and outcome. The treatment effect is exactly two. Strong encouragement changes participation by about 0.284 and produces a Wald estimate near 2.340. Weak encouragement changes participation by only 0.0238 and produces an estimate near 6.047. In this finite sample, the encouragement groups retain about 0.0965 difference in the non-treatment component of the outcome. Dividing that fluctuation by a small first-stage difference amplifies it. Examining first-stage strength and using uncertainty methods appropriate for weak instruments therefore addresses a visible numerical mechanism.

With heterogeneous effects, a binary instrument commonly identifies a local average treatment effect for compliers under independence, exclusion, relevance and monotonicity conditions. Compliers are people whose treatment changes from absent to present because of encouragement. Each person's single observed assignment does not disclose that latent compliance type completely. If encouragement increases participation for some people and decreases it for others, monotonicity needs reconsideration. Reporting the population represented by the estimate alongside the number is essential to deciding which policy changes that estimate can inform.

## Find comparisons in time changes and thresholds

When one region introduces a policy, difference-in-differences compares its before-after change with the contemporaneous change in an untreated region. Initial outcome levels may differ. The key assumption is that, without the policy, changes would have followed parallel trends. The synthetic treated group begins at a higher level, both groups rise by 0.8 per period, and the policy effect is three. Difference-in-differences returns approximately 2.998. A comparison of levels retains the initial gap; comparing changes and subtracting them removes a stable group difference.

$$
\widehat\tau_{\rm DiD}=(\overline Y_{1,\rm post}-\overline Y_{1,\rm pre})-(\overline Y_{0,\rm post}-\overline Y_{0,\rm pre})
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/2424bfc0d9d3e719fec7ec75.svg) | Mean outcome for group g=1 treated or 0 control and period s=pre or post; outcome units. |
| ![Formula](https://ml-biomat.com/static/agent-math/2bdddcb4db2b6c0ec4f34ca8.svg) | Difference-in-differences effect estimate; outcome units. |

A treated change 10→15 and control change 6→8 give 5−2=3. Untreated parallel trends remove shared changes and fixed group gaps. The code averages two periods before and after, separated by two time units, so an extra 0.7 trend creates bias 1.4.

![Left: treatment-rate changes under strong and weak instruments. Middle: four-period means under parallel and differential trends. Right: 1,624 records within bandwidth 0.4 and a local linear discontinuity fit.](https://ml-biomat.com/static/tutorials/machine-learning/figures/62e9f57b0ce3491e9816030f.svg?v=62e9f57b0ce3)

Figure 4Left: treatment-rate changes under strong and weak instruments. Middle: four-period means under parallel and differential trends. Right: 1,624 records within bandwidth 0.4 and a local linear discontinuity fit.

Adding an untreated extra trend of 0.7 per period to the treated group changes the estimate to approximately 4.398: the differential trend becomes part of the apparent policy effect. Multiple pretreatment periods, prespecified placebo dates and institutional knowledge help evaluate the parallel-trends argument. Similar pre-policy trends do not force the unobserved post-policy trajectory to remain similar. With staggered adoption, conventional two-way fixed-effect regressions can also mix cohort and time-specific effects. Defining the comparison group and target for each adoption cohort makes that design easier to interpret.

Regression discontinuity finds a local comparison near an assignment threshold. Applicants just below and just above an eligibility score may be similar, although their treatment opportunities change abruptly. If potential outcomes are continuous at the cutoff and units cannot precisely manipulate which side they occupy, a local outcome jump identifies an effect at that threshold. The code generates a jump of 1.5 and fits separate local lines through a treatment indicator and side-specific slope. A bandwidth of 0.4 uses 1,624 observations and estimates a jump near 1.427.

Bandwidths of 0.2 and 0.8 produce approximately 1.423 and 1.490. A narrower window is more local but has fewer observations; a wider window contains more information while relying more on the chosen functional shape. Applied work examines score density, pretreatment covariate continuity and other policies sharing the threshold. If eligibility increases treatment probability rather than switching everyone from untreated to treated, a fuzzy discontinuity uses a ratio of jumps. Both designs begin with a local population near the cutoff; extrapolation to distant scores requires additional structure.

## Turn assumption changes into inspectable scenarios

Measured balance, a complex estimator and a large dataset address different issues from the completeness of common-cause adjustment. Sensitivity analysis asks a concrete question: how strongly would an omitted factor need to influence assignment and outcome to change the estimate? A separate simulation creates a known factor U and initially withholds it from the estimator. Its effect on the outcome increases across scenarios while the true treatment effect remains one. Omitting U moves the estimated effect from approximately 1.001 to 3.392; including U gives about 1.025 throughout.

![Left: adjusted and omitted-factor regression effects as the hidden mechanism strengthens. Right: crude event fractions in the two randomized groups in the 1989 final report; labels show event counts and assigned denominators.](https://ml-biomat.com/static/tutorials/machine-learning/figures/89cd322ac51c2eff6f4fc2fe.svg?v=89cd322ac51c)

Figure 5Left: adjusted and omitted-factor regression effects as the hidden mechanism strengthens. Right: crude event fractions in the two randomized groups in the 1989 final report; labels show event counts and assigned denominators.

Here U is a disclosed variable in a simulator, used to show a mechanism. In an actual study, measurements, external evidence or expert ranges can help define sensitivity parameters and identify which ranges alter a decision. Placebo outcomes, pretreatment outcomes, false policy dates and negative controls look for patterns inconsistent with a causal account. An apparent effect before a policy begins, for example, motivates checks for differential trends, anticipation or incorrect time alignment. Each diagnostic is most useful when its result leads to a specific investigation.

DoWhy organizes work into modeling, identification, estimation and refutation checks. Passing a particular check means the tested perturbation or implication did not expose the corresponding problem. The next record should connect that check to its assumption and practical action: measure a particular common cause, extend overlap in a feature region, investigate a period's trend, or redesign assignment. This makes uncertainty in the causal account operational. It also keeps the roles of substantive knowledge, experimental design and statistical computation visible throughout the analysis.

## Decide how large a change the experiment should detect

If conversion currently averages 10% and a useful improvement is 12%, the target is a two-percentage-point absolute increase. Sample-size planning uses that difference, the baseline probability, an allowed type-I error rate and desired power. Power is the probability that a prespecified test detects an effect of the chosen magnitude when it is present. For independent participants, equal group sizes, a two-sided 5% test and 80% power, the normal approximation gives approximately 3,841 people per arm. Smaller target effects generally require substantially more people; the figure uses a logarithmic sample-size axis to make the growth legible.

$$
n\approx\frac{[z_{1-\alpha/2}\sqrt{2\bar p(1-\bar p)}+z_{1-\beta}\sqrt{p_0(1-p_0)+p_1(1-p_1)}]^2}{(p_1-p_0)^2},\quad\bar p=(p_0+p_1)/2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6368178ee6d1c0d30add9a37.svg) | Independent participants per arm, control and treatment probabilities, and their average; counts and dimensionless probabilities. |
| ![Formula](https://ml-biomat.com/static/agent-math/1eb80413bb0a95188b8354e3.svg) | Two-sided type-I error, type-II error and power; probabilities. |
| ![Formula](https://ml-biomat.com/static/agent-math/86b5d956b90b25e300aeff00.svg) | Quantile q of the standard normal distribution; dimensionless. |

This normal approximation plans equal independent binomial groups. With p0=0.10, p1=0.12, α=0.05 and power 0.8, z≈1.960 and 0.842 give 3,841 people per arm after rounding up. Clustered or repeated measurements use corresponding design variances.

![Left: equal-arm sample sizes at baseline 10%, two-sided 5% testing and 80% power, on a log axis. Right: 14 recruitment days plus seven days for outcome maturation.](https://ml-biomat.com/static/tutorials/machine-learning/figures/ae637d98200b35211d23727c.svg?v=ae637d98200b)

Figure 6Left: equal-arm sample sizes at baseline 10%, two-sided 5% testing and 80% power, on a log axis. Right: 14 recruitment days plus seven days for outcome maturation.

At 1,000 new eligible participants per day, approximately 7,682 participants require eight days by count alone. Because conversion may vary across weekdays, the example schedules recruitment over two full weeks. With an outcome defined over the seven days following assignment, the last recruits need another seven days, making day 21 the complete-outcome date. Counts refer to independently assigned participants, rather than repeated visits by the same person. Clustering, attrition, repeated observations and choosing among multiple outcomes each call for corresponding changes to design and analysis.

Repeatedly checking an ordinary fixed-sample test and stopping at the first significant result changes its error rate. A fixed-sample design or a sequential procedure with planned boundaries provides an explicit stopping rule. Primary outcome, analysis population, assignment unit, treatment version, follow-up window and minimum meaningful effect together define when the experiment answers its question. Data monitoring in historical randomized trials was also a design activity. The practical lesson is to decide how evidence will trigger a decision before watching a sequence of fluctuating results.

## Give every estimate a question that can be repeated

The complete program saves potential outcomes, observed outcomes, out-of-fold predictions, matching indices and results from the different designs. Hold the generating mechanism fixed to compare estimators, then change one identification condition to see how a particular error appears. When reading any estimate, keep its population, treatment and outcome window alongside its source of comparison: random assignment, measured common causes, encouragement, time trends or a threshold. These coordinates turn a bare number into a result that can guide the next measurement or decision.

### Complete experiment: adjustment, DML, IV, DiD, RD and power

Run python main.py --output results --language en. Data use a fixed synthetic seed, plus four public final-report counts. Outputs include five figure groups, complete arrays and summary.json, preserving fold assignments and matching indices.

```
"""Causal designs with known synthetic effects and one public aggregate experiment."""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.special import expit
from scipy.stats import norm
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from threadpoolctl import threadpool_limits
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def ols(X,y):
 b=np.linalg.lstsq(X,y,rcond=None)[0];r=y-X@b;s2=r@r/(len(y)-X.shape[1]);cov=s2*np.linalg.inv(X.T@X);return b,np.sqrt(np.diag(cov))

def crossfit(X,T,Y,seed=8):
 e=np.zeros(len(T));m0=np.zeros(len(T));m1=np.zeros(len(T));m=np.zeros(len(T));fold=np.zeros(len(T),int)
 for k,(train,test) in enumerate(StratifiedKFold(5,shuffle=True,random_state=seed).split(X,T)):
  prop=LogisticRegression(C=10,max_iter=1000).fit(X[train],T[train]);e[test]=prop.predict_proba(X[test])[:,1];fold[test]=k
  for group,dest in [(0,m0),(1,m1)]:
   ind=train[T[train]==group];model=HistGradientBoostingRegressor(max_iter=120,max_leaf_nodes=9,l2_regularization=2,random_state=seed).fit(X[ind],Y[ind]);dest[test]=model.predict(X[test])
  model=HistGradientBoostingRegressor(max_iter=120,max_leaf_nodes=9,l2_regularization=2,random_state=seed).fit(X[train],Y[train]);m[test]=model.predict(X[test])
 return e,m0,m1,m,fold

def n_per_arm(p0,p1,alpha=.05,power=.8):
 p=(p0+p1)/2;return float(((norm.ppf(1-alpha/2)*np.sqrt(2*p*(1-p))+norm.ppf(power)*np.sqrt(p0*(1-p0)+p1*(1-p1)))/(p1-p0))**2)

def main(out,lang):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);zh=lang=='zh';L=lambda z,e:z if zh else e;rng=np.random.default_rng(8)
 plt.rcParams.update({'font.family':'Microsoft YaHei' if zh else 'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','axes.unicode_minus':False})
 def save(fig,name):fig.savefig(out/f'{name}-{lang}.svg',bbox_inches='tight');plt.close(fig)
 n=3000;X=rng.uniform(-2,2,(n,6));true_e=expit(.6*X[:,0]-.4*X[:,1]);T=rng.binomial(1,true_e);tau=1+.5*X[:,0];noise=rng.normal(0,1,n);Y0=2+1.5*X[:,0]+X[:,1]**2+np.sin(X[:,2])+noise;Y1=Y0+tau;Y=np.where(T,Y1,Y0)
 e,m0,m1,m,fold=crossfit(X,T,Y);e=np.clip(e,.001,.999);phi=m1-m0+T*(Y-m1)/e-(1-T)*(Y-m0)/(1-e);aipw=float(phi.mean());aipw_se=float(phi.std(ddof=1)/np.sqrt(n));ipw=float(np.mean(T*Y/e-(1-T)*Y/(1-e)));hajek=float(np.sum(T*Y/e)/np.sum(T/e)-np.sum((1-T)*Y/(1-e))/np.sum((1-T)/(1-e)));naive=float(Y[T==1].mean()-Y[T==0].mean())
 residual_T=T-e;residual_Y=Y-m;design=np.c_[residual_T,residual_T*X[:,0]];dml=np.linalg.lstsq(design,residual_Y,rcond=None)[0];dml_ate=float(dml[0]);cate=dml[0]+dml[1]*X[:,0]
 # Nearest-neighbor matching with replacement estimates ATT for treated records.
 scaled=StandardScaler().fit_transform(X[:,:3]);treated=np.flatnonzero(T==1);controls=np.flatnonzero(T==0);nearest=NearestNeighbors(n_neighbors=1).fit(scaled[controls]).kneighbors(scaled[treated],return_distance=False)[:,0];matched=controls[nearest];att=float(np.mean(Y[treated]-Y[matched]));true_att=float(tau[treated].mean())
 def smd(weights):
  mean1=np.average(X[T==1],axis=0,weights=weights[T==1]);mean0=np.average(X[T==0],axis=0,weights=weights[T==0]);return (mean1-mean0)/np.sqrt((X[T==1].var(0,ddof=1)+X[T==0].var(0,ddof=1))/2)
 w=np.where(T==1,1/e,1/(1-e));before=smd(np.ones(n));after=smd(w)
 fig,axs=plt.subplots(1,3,figsize=(15,4.8),layout='constrained');axs[0].hist(e[T==0],bins=25,alpha=.5,density=True,label=L('未分配券','No coupon'),color='#237b94');axs[0].hist(e[T==1],bins=25,alpha=.5,density=True,label=L('分配券','Coupon'),color='#d87430');axs[0].set(xlabel=L('折外倾向概率','Out-of-fold propensity'),ylabel=L('密度','Density'),title=L('两组的共同支持','Overlap between groups'));axs[0].legend(fontsize=9)
 axs[1].plot(abs(before),range(6),'o-',label=L('调整前','Before'));axs[1].plot(abs(after),range(6),'s-',label=L('IPW调整后','After IPW'));axs[1].axvline(.1,color='#aab7bf',ls=':');axs[1].set(yticks=range(6),yticklabels=[f'x{j}' for j in range(6)],xlabel=L('绝对标准化均值差','Absolute standardized mean difference'),title=L('观测变量的平衡','Balance of observed covariates'));axs[1].legend(fontsize=9)
 names=['Naive','IPW','Hajek','AIPW','DML'];vals=[naive,ipw,hajek,aipw,dml_ate];axs[2].barh(names,vals,color=['#aab7bf']+['#237b94']*4);axs[2].axvline(1,color='#d87430',ls='--',label=L('生成总体ATE=1','Generating population ATE=1'));axs[2].errorbar(aipw,3,xerr=1.96*aipw_se,fmt='none',color='#263744',capsize=4);axs[2].set(xlabel=L('结果单位的平均处理效应','Average treatment effect in outcome units'));axs[2].legend(fontsize=8);save(fig,'adjustment')
 fig,axs=plt.subplots(1,2,figsize=(11,4.4),layout='constrained');xx=np.linspace(-2,2,100);axs[0].plot(xx,1+.5*xx,color='#d87430',label=L('生成效应','Generating effect'));axs[0].plot(xx,dml[0]+dml[1]*xx,'--',color='#237b94',label=L('折外残差DML','Cross-fitted residual DML'));axs[0].set(xlabel='x0',ylabel=L('条件平均处理效应','Conditional average treatment effect'));axs[0].legend();axs[1].bar(['ATE','ATT'],[aipw,att],color=['#237b94','#609b6d']);axs[1].scatter([0,1],[1,true_att],marker='_',s=500,color='#d87430',linewidth=3,label=L('对应真实目标','Corresponding true target'));axs[1].set(ylabel=L('结果单位','Outcome units'),title=L('人群变了，目标也变了','A different population changes the target'));axs[1].legend(fontsize=9);save(fig,'heterogeneity')
 # Three distinct identification designs, each with an explicit known mechanism.
 N=4000;U=rng.normal(size=N);Z=rng.binomial(1,.5,N);eps=rng.normal(size=N);outcome_noise=rng.normal(size=N);iv={}
 for strength in [1.,.05]:
  treatment=(strength*Z+.8*U+eps>0).astype(int);outcome=2*treatment+U+outcome_noise;first=float(treatment[Z==1].mean()-treatment[Z==0].mean());reduced=float(outcome[Z==1].mean()-outcome[Z==0].mean());iv[str(strength)]={'first_stage':first,'reduced_form':reduced,'wald_effect':reduced/first}
 G=np.repeat([0,1],400);time=np.arange(-2,2);panel_noise=rng.normal(0,.5,(800,4));did={};panel={}
 for trend in [0.,.7]:
  yy=10+2*G[:,None]+.8*time[None,:]+3*G[:,None]*(time>=0)[None,:]+trend*G[:,None]*time[None,:]+panel_noise;means=np.array([yy[G==g].mean(0) for g in [0,1]]);effect=float((means[1,2:].mean()-means[1,:2].mean())-(means[0,2:].mean()-means[0,:2].mean()));did[str(trend)]=effect;panel[str(trend)]=means
 running=rng.uniform(-1,1,N);D=(running>=0).astype(int);outcome=1+2*running+1.5*D+rng.normal(0,.4,N);rd={}
 for bandwidth in [.2,.4,.8]:
  use=abs(running)<=bandwidth;rdX=np.c_[np.ones(use.sum()),running[use],D[use],running[use]*D[use]];b,se=ols(rdX,outcome[use]);rd[str(bandwidth)]={'n':int(use.sum()),'jump':float(b[2]),'se':float(se[2])}
 fig,axs=plt.subplots(1,3,figsize=(15,4.7),layout='constrained');axs[0].bar([0,1],[iv['1.0']['first_stage'],iv['0.05']['first_stage']],color=['#237b94','#d87430']);axs[0].set(xticks=[0,1],xticklabels=[L('强鼓励','Strong encouragement'),L('弱鼓励','Weak encouragement')],ylabel=L('第一阶段处理率差','First-stage treatment-rate difference'));axs[0].set_title(L('工具变量先改变处理','Instrument first changes treatment'))
 for tr,style in [('0.0','-'),('0.7','--')]:
  for g,c in [(0,'#83949e'),(1,'#237b94')]:axs[1].plot(time,panel[tr][g],style+'o',color=c,label=(L('对照','Control') if g==0 else L('处理','Treated'))+f' trend={tr}')
 axs[1].axvline(-.5,color='#d87430',ls=':');axs[1].set(xlabel=L('时期','Period'),ylabel=L('平均结果','Mean outcome'),title=L('DiD与平行趋势','DiD and parallel trends'));axs[1].legend(fontsize=7)
 use=abs(running)<=.4;axs[2].scatter(running[use],outcome[use],s=5,c=np.where(D[use],'#d87430','#237b94'),alpha=.25);b,_=ols(np.c_[np.ones(use.sum()),running[use],D[use],running[use]*D[use]],outcome[use]);
 for side,interval in [(0,[-.4,0]),(1,[0,.4])]:
  rx=np.linspace(*interval,100);axs[2].plot(rx,b[0]+b[1]*rx+b[2]*side+b[3]*rx*side,color='#263744')
 axs[2].set(xlabel=L('运行变量距阈值','Running variable relative to cutoff'),ylabel=L('结果','Outcome'),title=L('RD：阈值附近的跳跃','RD: a jump near the cutoff'));save(fig,'designs')
 # Sensitivity demonstration: a generated omitted U is known to the simulator.
 Xs=rng.normal(size=3000);Us=rng.normal(size=3000);Ts=(.8*Xs+Us+rng.normal(size=3000)>0).astype(int);sn=rng.normal(size=3000);sens=[]
 for gamma in [0,.5,1,1.5,2]:
  ys=Ts+2*Xs+gamma*Us+sn;omit,_=ols(np.c_[np.ones(3000),Ts,Xs],ys);full,_=ols(np.c_[np.ones(3000),Ts,Xs,Us],ys);sens.append({'hidden_effect':gamma,'omitted_U':float(omit[1]),'included_U':float(full[1])})
 # Public aggregate facts from the 1989 FINAL PHS report; crude summaries, not its adjusted analysis.
 count1,n1,count0,n0=139,11037,239,11034;p1=count1/n1;p0=count0/n0;rdiff=p1-p0;se=np.sqrt(p1*(1-p1)/n1+p0*(1-p0)/n0);rr=p1/p0
 fig,axs=plt.subplots(1,2,figsize=(11,4.5),layout='constrained');axs[0].plot([v['hidden_effect'] for v in sens],[v['omitted_U'] for v in sens],'o-',label=L('遗漏U','U omitted'),color='#d87430');axs[0].plot([v['hidden_effect'] for v in sens],[v['included_U'] for v in sens],'s-',label=L('调整U','U adjusted'),color='#237b94');axs[0].axhline(1,color='#83949e',ls=':');axs[0].set(xlabel=L('隐藏U对结果的生成系数','Generating outcome coefficient of hidden U'),ylabel=L('处理效应估计','Treatment-effect estimate'),title=L('敏感性情景：改变未测量机制','Sensitivity scenarios: change the omitted mechanism'));axs[0].legend(fontsize=9)
 axs[1].bar([0,1],[1000*p0,1000*p1],color=['#83949e','#237b94']);axs[1].set(xticks=[0,1],xticklabels=[L('安慰剂组','Placebo group'),L('随机分配阿司匹林组','Assigned aspirin group')],ylabel=L('每千名分配者的事件数','Events per 1,000 assigned participants'),title=L('1989报告：原始事件比例','1989 report: crude event fractions'));axs[1].text(0,1000*p0+.4,f'{count0}/{n0}',ha='center');axs[1].text(1,1000*p1+.4,f'{count1}/{n1}',ha='center');axs[1].set_ylim(0,26);save(fig,'sensitivity_trial')
 differences=np.linspace(.005,.05,100);sizes=np.array([n_per_arm(.1,.1+d) for d in differences]);required=int(np.ceil(n_per_arm(.1,.12)));days=int(np.ceil(2*required/1000));recruitment=max(14,int(np.ceil(days/7)*7));fig,axs=plt.subplots(1,2,figsize=(11,4.5),layout='constrained');axs[0].plot(100*differences,sizes,color='#237b94');axs[0].scatter([2],[required],c='#d87430');axs[0].set(yscale='log',xlabel=L('绝对提升（百分点）','Absolute increase (percentage points)'),ylabel=L('每组所需人数','Required participants per arm'),title=L('基线10%，双侧5%，功效80%','Baseline 10%, two-sided 5%, power 80%'));axs[1].broken_barh([(0,recruitment)],(15,8),facecolors='#237b94');axs[1].broken_barh([(recruitment,7)],(15,8),facecolors='#d87430');axs[1].set(xlim=(0,recruitment+8),ylim=(5,32),yticks=[],xlabel=L('天数','Days'),title=L('招募覆盖两周，再等待7天结局','Recruit over two weeks, then mature 7-day outcomes'));axs[1].text(recruitment/2,19,L('招募','Recruit'),ha='center',va='center',color='white');axs[1].text(recruitment+3.5,19,L('结局成熟','Maturation'),ha='center',va='center',color='white',fontsize=9);save(fig,'power_duration')
 summary={'n':n,'treated_n':int(T.sum()),'controls_n':int((1-T).sum()),'true_population_ate':1,'true_sample_ate':float(tau.mean()),'naive_difference':naive,'ipw_ate':ipw,'hajek_ate':hajek,'aipw_ate':aipw,'aipw_se':aipw_se,'aipw_ci95':[aipw-1.96*aipw_se,aipw+1.96*aipw_se],'dml_intercept':float(dml[0]),'dml_slope':float(dml[1]),'matching_att':att,'true_sample_att':true_att,'propensity_min':float(e.min()),'propensity_max':float(e.max()),'absolute_smd_before':abs(before).tolist(),'absolute_smd_after':abs(after).tolist(),'iv':iv,'did':did,'rd':rd,'sensitivity':sens,'trial':{'treated_events':count1,'treated_n':n1,'control_events':count0,'control_n':n0,'total_n':n1+n0,'crude_risk_difference':rdiff,'crude_risk_ratio':rr,'binomial_difference_ci95':[rdiff-1.96*se,rdiff+1.96*se]},'power_per_arm':required,'raw_recruitment_days':days,'planned_recruitment_days':recruitment,'outcome_window_days':7,'planned_complete_day':recruitment+7}
 summary.update({'crossfit_fold_counts':np.bincount(fold).tolist(),'potential_effect_identity_error':float(np.max(abs(Y1-Y0-tau))),'did_trend_bias':did['0.7']-did['0.0']})
 np.savez_compressed(out/'experiment_data.npz',X=X,treatment=T,outcome=Y,potential_y0=Y0,potential_y1=Y1,true_effect=tau,propensity=e,crossfit_fold=fold,aipw_scores=phi,matched_control_indices=matched,rd_running=running,rd_outcome=outcome);(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args()
 with threadpool_limits(limits=1):main(a.output,a.language)
```

For a new problem, define the potential outcomes and target population, draw the mechanisms of assignment and outcome, select a design that identifies the target, and use estimation and uncertainty calculations that match that design. Sensitivity analysis then explores the assumptions most relevant to the decision. Machine learning helps fit complex predictive relationships; research design explains which intervention questions those relationships answer. Keeping both contributions explicit provides a coherent route from an association in a table to a defensible causal argument.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M08.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Neyman (1923; English translation 1990), On the Application of Probability Theory to Agricultural Experiments](https://ics.uci.edu/~sternh/courses/265/neyman_statsci1990.pdf)

   Historical structure of potential outcomes and randomized agricultural experiments.

   Primary reference; no article figure reproduced
2. [DoWhy — User guide](https://www.pywhy.org/dowhy/main/user_guide/)

   Graphs, identification, estimation and refutation.

   MIT project; original graph attributed
3. [DoWhy repository](https://github.com/py-why/dowhy)

   Original causal graph and repository MIT license.

   MIT
4. [EconML — Double Machine Learning](https://econml.azurewebsites.net/spec/estimation/dml.html)

   Residualization, cross-fitting and heterogeneous effects.
5. [Causal Inference for the Brave and True — Regression Discontinuity](https://matheusfacure.github.io/python-causality-handbook/16-Regression-Discontinuity-Design.html)

   Local comparisons near a cutoff and bandwidth.

   Open tutorial; linked reference
6. [Final report on the aspirin component of the ongoing Physicians’ Health Study (1989)](https://www.urmc.rochester.edu/MediaLibraries/URMCMedia/neurology/documents/PHS.pdf)

   Table 1 counts 139/11037 and 239/11034; our figure recomputes crude proportions.

   Primary paper; aggregate numerical facts, no figure or prose reproduced
